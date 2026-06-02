// End-to-end demo of the new model:
//   empty DB → student asks a topic → LLM decomposes it → struggles logged
//   against the nodes → show the logged result (the gaps the LLM would teach).
//
// Runs offline: decompose() returns the baked Kepler example (the stand-in for
// the LLM's output). With a real LLM wired in, only that one call changes.
//
//   node graph-log/demo.mjs

import { rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { openDb, storeDecomposition, getTopic, logOutcome, topicStatusForStudent, counts } from "./db.mjs";
import { decompose } from "./decompose.mjs";

const DB_PATH = fileURLToPath(new URL("data/demo.db", import.meta.url));
rmSync(DB_PATH, { force: true }); // fresh, so the demo starts from a truly EMPTY graph

const db = openDb(DB_PATH);
const line = (s) => console.log("\n──────── " + s + " ────────");

line("1) The graph database starts EMPTY");
console.log(counts(db)); // { topics: 0, nodes: 0, edges: 0, logs: 0 }

line("2) Student asks about a topic → the LLM decomposes it on demand");
const topic = "Kepler's third law";
const student = "student_01";
const decomposition = await decompose(topic); // offline: baked Kepler; prod: LLM via DECOMPOSITION_PROMPT
const stored = storeDecomposition(db, topic, decomposition);
console.log(`stored "${topic}": ${stored.nodes} nodes, ${stored.edges} edges`);

line("3) The topic graph (same for everyone), by layer");
const g = getTopic(db, topic);
const byLayer = {};
for (const n of g.nodes) (byLayer[n.layer] ??= []).push(n.concept + (n.is_floor ? " [FLOOR]" : ""));
for (const L of Object.keys(byLayer).sort()) console.log(`  layer ${L}: ${byLayer[L].join(", ")}`);
console.log("  prerequisite edges:");
for (const e of g.edges) console.log(`    ${e.concept}  ⟶ needs ⟶  ${e.requires}   (${e.why})`);

line("4) Log THIS student's experience against the nodes (passed / struggled)");
const outcomes = [
  ["addition", "passed"], ["multiplication", "passed"], ["powers/exponents", "passed"],
  ["equation/variable literacy", "passed"], ["constant", "passed"],
  ["division", "struggled"], ["ratio", "struggled"], ["proportionality", "struggled"],
];
for (const [concept, outcome] of outcomes) {
  logOutcome(db, { student_id: student, topic, concept, outcome });
  console.log(`  logged: ${student} ${outcome.toUpperCase().padEnd(9)} ${concept}`);
}

line("5) Read back — this student's status on the topic (what the LLM personalizes from)");
const status = topicStatusForStudent(db, student, topic);
for (const s of status) {
  const mark = s.latest_outcome === "struggled" ? "✗ struggled" : s.latest_outcome === "passed" ? "✓ passed" : "· untested";
  console.log(`  [L${s.layer}] ${s.concept.padEnd(28)} ${mark}`);
}
const gaps = status.filter((s) => s.latest_outcome === "struggled").map((s) => s.concept);
console.log(`\n  → ${student}'s logged gaps in "${topic}": ${gaps.join(", ")}`);
console.log(`  → The LLM teaches the deepest of these first, then climbs back up to "${topic}".`);

line("DB filled from empty");
console.log(counts(db));
console.log("\nEND-TO-END: OK");
db.close();
