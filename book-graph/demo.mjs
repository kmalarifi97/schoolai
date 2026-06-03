// End-to-end demo:
//   (1) the book/chapter/lesson/page/content structure,
//   (2) two real book items' full prerequisite graphs (to the floor + check Qs),
//   (3) a student session logging a struggle against a book-graph node + read-back.
//
//   node demo.mjs        (run `node build.mjs` first)

import {
  openDb, structureSummary, chaptersTree, contentNodesWithPrereqs, getContentNode,
  getPrereqGraph, startSession, logOnNode, sessionLogs, studentStruggles,
} from "./db.mjs";

const db = openDb();
const line = (s) => console.log("\n──────── " + s + " ────────");

line("1) BOOK STRUCTURE (book → chapters → lessons → pages → content nodes)");
const sum = structureSummary(db);
console.log(`book: ${sum.book}`);
console.log(`chapters ${sum.chapters} · lessons ${sum.lessons} · pages ${sum.pages} · content nodes ${sum.content_nodes}`);
console.log("content node types (book-derived):", sum.by_type.map((t) => `${t.type}=${t.c}`).join(", "));
console.log("\nchapters → lessons (pages / content nodes):");
let curCh = null;
for (const r of chaptersTree(db)) {
  if (r.number !== curCh) { console.log(`  ch.${r.number}  ${r.chapter}`); curCh = r.number; }
  console.log(`      ${r.code}  ${r.lesson}   (${r.pages} pages, ${r.nodes} nodes)`);
}

line("2) ATTACHED PREREQUISITE GRAPHS (content nodes that have prerequisites)");
const withPre = contentNodesWithPrereqs(db);
console.log(`${withPre.length} content nodes carry a prerequisite graph:`);
for (const c of withPre) console.log(`  #${c.id} [${c.type}, lesson ${c.lesson}] ${c.text.slice(0, 70)}`);

function printPrereqGraph(cnId) {
  const cn = getContentNode(db, cnId);
  const g = getPrereqGraph(db, cnId);
  console.log(`\n  ▼ content node #${cnId} [${cn.type}] — ${cn.text.slice(0, 80)}`);
  const byLayer = {};
  for (const n of g.nodes) (byLayer[n.layer] ??= []).push(n);
  for (const L of Object.keys(byLayer).sort()) {
    console.log(`    layer ${L}${byLayer[L][0].is_floor ? " (FLOOR)" : ""}:`);
    for (const n of byLayer[L]) console.log(`      • ${n.concept}\n          check: ${n.check_question}`);
  }
  console.log("    prerequisite edges (concept ⟶ needs ⟶ prerequisite):");
  for (const e of g.edges) console.log(`      ${e.concept}  ⟶  ${e.requires}   (${e.why})`);
}

line("2a) FULL PREREQ GRAPH — Newton's law of universal gravitation");
const grav = withPre.find((c) => c.text.includes("الجذب الكوني")) || withPre[1];
printPrereqGraph(grav.id);

line("2b) FULL PREREQ GRAPH — Angular velocity");
const ang = withPre.find((c) => c.type === "key_term") || withPre[2];
printPrereqGraph(ang.id);

line("3) STUDENT SESSION OVERLAY — log a struggle against a book-graph node, read back");
const student = "student_01";
const session = "sess-2024-001"; // one chat = one session id
startSession(db, session, student);
console.log(`student ${student} started session ${session} studying "${grav.text.slice(0, 50)}"`);

// reference real book-graph nodes and log struggle/mastery ON THE LINK
const preId = (cnId, concept) => db.prepare(`SELECT id FROM prereq_nodes WHERE content_node_id=? AND concept=?`).get(cnId, concept)?.id;
const events = [
  ["content", grav.id, "struggled", `the law itself (#${grav.id})`],
  ["prereq", preId(grav.id, "inverse-square law (F ∝ 1/r²)"), "struggled", "prereq: inverse-square law"],
  ["prereq", preId(grav.id, "division"), "struggled", "prereq: division"],
  ["prereq", preId(grav.id, "addition"), "passed", "prereq: addition"],
];
for (const [kind, id, outcome, label] of events) {
  logOnNode(db, { session_id: session, ref_kind: kind, ref_id: id, outcome });
  console.log(`  logged ${outcome.toUpperCase().padEnd(9)} on ${label}`);
}

line("read back — this session's logs (joined to the referenced book-graph nodes)");
for (const r of sessionLogs(db, session)) console.log(`  ${r.outcome.padEnd(9)} [${r.ref_kind}] ${r.node}`);

line("read back — everything this STUDENT has struggled on (across their sessions)");
for (const r of studentStruggles(db, student)) console.log(`  session ${r.session_id}: [${r.ref_kind}] ${r.node}`);

console.log("\nEND-TO-END: OK");
db.close();
