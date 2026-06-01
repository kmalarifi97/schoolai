// Build the Physics-2 prerequisite graph in graph-tutor format from the existing
// validated spine in ../chatgpt-app/data/spine/. Unlike the Junyi PoC graph,
// these nodes are NAMED concepts (Wikidata-backed) with real multi-hop depth.
//
// Source of truth: chatgpt-app/data/spine/prereq_edges.jsonl (from = prerequisite,
// to = dependent) — identical edge semantics to ours (source = prerequisite).
// Node labels: Wikidata English labels (fetched once via wbgetentities, baked in
// here so the build needs no network). The old KST app stays untouched.

import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..");
const SPINE = join(ROOT, "..", "chatgpt-app", "data", "spine");
const OUT = join(ROOT, "graph", "physics2.graph.json");

// Wikidata English labels for the 19 spine nodes (fetched from wbgetentities).
const LABEL = {
  Q29175: "derivative", Q11465: "velocity", Q11402: "force", Q42213: "work",
  Q11348: "function", Q246639: "limit", Q80091: "integral", Q44528: "vector",
  Q178192: "cross product", Q11471: "time", Q48103: "torque",
  Q46276: "kinetic energy", Q11382: "conservation of energy",
  Q155640: "potential energy", Q11423: "mass", Q41273: "momentum",
  Q2305665: "conservation of momentum",
  Q134465: "Newton's law of universal gravitation", Q161635: "angular velocity",
};
// Rough subject grouping so the graph carries an "area" (math foundation vs physics).
const MATH = new Set(["Q29175", "Q11465", "Q11348", "Q246639", "Q80091", "Q44528", "Q178192", "Q11471"]);

const rd = (p) => readFileSync(p, "utf8").split("\n").filter((l) => l.trim() && !l.startsWith("#")).map((l) => JSON.parse(l));
const edgesIn = rd(join(SPINE, "prereq_edges.jsonl")).filter((e) => (e.type || "prerequisite") === "prerequisite");

// optional curriculum metadata (lesson / book pages) per node, via crosswalk -> concepts
let conceptBySlug = {};
try { conceptBySlug = JSON.parse(readFileSync(join(SPINE, "concepts.json"), "utf8")); } catch {}
const nodeMeta = new Map();
try {
  for (const r of rd(join(SPINE, "crosswalk.jsonl"))) {
    if (r.node && r.slug && conceptBySlug[r.slug]) {
      const c = conceptBySlug[r.slug];
      if (!nodeMeta.has(r.node)) nodeMeta.set(r.node, { lesson: c.lesson || null, book_pages: c.book_pages || null });
    }
  }
} catch {}

const ids = [...new Set(edgesIn.flatMap((e) => [e.from, e.to]))];
const nodes = ids.map((id) => ({
  id,
  name: LABEL[id] || id,
  area: MATH.has(id) ? "math-foundation" : "physics",
  ...(nodeMeta.get(id) || {}),
}));
const edges = edgesIn.map((e) => ({
  source: e.from, target: e.to,
  confidence: e.confidence ?? null,
}));

const graph = {
  meta: {
    source: "physics2-spine",
    note: "Named-concept prerequisite graph from chatgpt-app/data/spine. edge {source,target}: source is a prerequisite of target.",
    edge_semantics: "edge {source, target}: source is a PREREQUISITE of target.",
  },
  nodes,
  edges,
};
writeFileSync(OUT, JSON.stringify(graph, null, 2));
console.log(`[physics2] wrote ${OUT}  (${nodes.length} nodes, ${edges.length} edges)`);
console.log(`[physics2] named: ${nodes.filter((n) => n.name !== n.id).length}/${nodes.length}`);
