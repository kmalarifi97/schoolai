// Build the shared book graph from the real book JSON, then attach the authored
// prerequisite graphs (with check questions) to their content nodes.
//   node build.mjs
//
// Source of truth: ../chatgpt-app/data/library.json (chapters→lessons index) +
// ../chatgpt-app/data/lesson_pages/<code>.json (pages→typed blocks).

import { readFileSync, readdirSync, existsSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import {
  openDb, reset, setBook, addChapter, addLesson, addPage, addContentNode,
  findContentNode, getContentNode, attachPrereqGraph, structureSummary,
} from "./db.mjs";
import { PREREQ_GRAPHS } from "./prereqs.mjs";

const CG = (p) => fileURLToPath(new URL(`../chatgpt-app/data/${p}`, import.meta.url));
const lib = JSON.parse(readFileSync(CG("library.json"), "utf8"));

const textOf = (b) => {
  switch (b.type) {
    case "heading": return b.text_ar || b.text_en || "";
    case "paragraph": case "margin_note": return b.text_ar || "";
    case "objectives": return (b.items_ar || []).join(" • ");
    case "key_term": return `${b.term_ar || ""}${b.term_en ? ` (${b.term_en})` : ""} — ${b.definition_ar || ""}`;
    case "equation": return `${b.caption_ar || ""} | ${b.latex || ""}`;
    case "worked_example": return `${b.printed_number || ""}: ${b.prompt_ar || ""}`;
    case "question": return `${b.printed_number || ""}: ${b.prompt_ar || ""}`;
    case "question_set": return b.title_ar || "مجموعة أسئلة";
    case "figure": return `${b.label_ar || ""}: ${b.description_ar || ""}`;
    case "table": return b.caption_ar || "جدول";
    default: return b.text_ar || b.caption_ar || "";
  }
};

// Fresh DB each build so content-node ids are deterministic (1…N) and stable —
// the generated prereq graphs reference content nodes by id.
const DBP = process.env.BOOKGRAPH_DB || fileURLToPath(new URL("data/book.db", import.meta.url));
rmSync(DBP, { force: true });
const db = openDb();
setBook(db, 1, lib.book?.title_ar || lib.book?.title || "الفيزياء 2");

let ord = 0;
function walk(node, lesson_id, page_id) {
  if (Array.isArray(node)) { for (const x of node) walk(x, lesson_id, page_id); return; }
  if (node && typeof node === "object") {
    if (node.type) addContentNode(db, { lesson_id, page_id, type: node.type, ordinal: ord++, block_id: node.id, text: textOf(node) });
    for (const v of Object.values(node)) walk(v, lesson_id, page_id);
  }
}

for (const ch of lib.chapters) {
  addChapter(db, { id: ch.id, book_id: 1, number: ch.id, title_ar: ch.title_ar, title_en: ch.title_en });
  for (const ls of ch.lessons) {
    const lesson_id = addLesson(db, { chapter_id: ch.id, code: ls.id, title_ar: ls.title_ar, title_en: ls.title_en, page_range: `${ls.start_page}-${ls.end_page}` });
    let lp;
    try { lp = JSON.parse(readFileSync(CG(`lesson_pages/${ls.id}.json`), "utf8")); } catch { continue; }
    for (const pg of lp.pages || []) {
      const page_id = addPage(db, lesson_id, pg.page ?? pg.page_number);
      ord = 0;
      walk(pg.blocks, lesson_id, page_id);
    }
  }
}

// Resolve an anchor to a real content node, relaxing the match if needed.
function resolveAnchor(a) {
  return findContentNode(db, a)
    || findContentNode(db, { lessonCode: a.lessonCode, like: a.like })
    || findContentNode(db, { type: a.type, like: a.like })
    || findContentNode(db, { like: a.like });
}

console.log("=== attaching prerequisite graphs ===");
for (const pg of PREREQ_GRAPHS) {
  const cn = resolveAnchor(pg.anchor);
  if (!cn) { console.warn(`  ✗ "${pg.name}": no content node matched anchor ${JSON.stringify(pg.anchor)}`); continue; }
  attachPrereqGraph(db, cn.id, { nodes: pg.nodes, edges: pg.edges });
  console.log(`  ✓ "${pg.name}" → content_node #${cn.id} [${cn.type}, lesson ${pg.anchor.lessonCode}]  (${pg.nodes.length} prereq nodes, ${pg.edges.length} edges)`);
}

// load fan-out-authored prereq graphs (generated/*.json), attached by content_node_id
const GEN = fileURLToPath(new URL("generated", import.meta.url));
let gG = 0, gN = 0, gFail = 0;
if (existsSync(GEN)) {
  for (const f of readdirSync(GEN).filter((x) => x.endsWith(".json")).sort()) {
    let arr;
    try { arr = JSON.parse(readFileSync(join(GEN, f), "utf8")); } catch { console.warn(`  ✗ ${f}: invalid JSON`); gFail++; continue; }
    if (!Array.isArray(arr)) continue;
    for (const g of arr) {
      if (!g.content_node_id || !Array.isArray(g.nodes) || !Array.isArray(g.edges) || !getContentNode(db, g.content_node_id)) { gFail++; continue; }
      attachPrereqGraph(db, g.content_node_id, { nodes: g.nodes, edges: g.edges });
      gG++; gN += g.nodes.length;
    }
  }
  console.log(`\n=== attached ${gG} fan-out-authored prereq graphs (${gN} prereq nodes)${gFail ? `, ${gFail} skipped` : ""} ===`);
}

console.log("\n=== book graph summary ===");
console.log(structureSummary(db));
const pn = db.prepare(`SELECT COUNT(*) c FROM prereq_nodes`).get().c;
const pe = db.prepare(`SELECT COUNT(*) c FROM prereq_edges`).get().c;
console.log(`prereq graphs: ${structureSummary(db).with_prereqs} · prereq nodes: ${pn} · prereq edges: ${pe}`);
db.close();
console.log("\nbuild OK");
