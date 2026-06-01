// Gap-closing graph layer for the Physics-2 app.
//
// Reuses the SAME validated prerequisite spine the KST engine uses
// (data/spine/prereq_edges.jsonl) but exposes the gap-closing view ChatGPT's
// 5-tool design wants: diagnosis from PASSED/FAILED concept names via backward
// traversal, returning the blocking prerequisite (root cause) and the shared
// root cause when several failures collapse to one missing foundation.
//
// In-process (no GraphQL/HTTP) — this is one MCP service. Concept names in,
// concept names out; internal Wikidata IDs never leave this module.

import { readFileSync } from "node:fs";
import { join } from "node:path";

// Wikidata English labels for the 19 spine nodes (so the math-foundation nodes,
// which have no crosswalk label, still read as real concepts).
const WIKILABEL = {
  Q29175: "derivative", Q11465: "velocity", Q11402: "force", Q42213: "work",
  Q11348: "function", Q246639: "limit", Q80091: "integral", Q44528: "vector",
  Q178192: "cross product", Q11471: "time", Q48103: "torque",
  Q46276: "kinetic energy", Q11382: "conservation of energy",
  Q155640: "potential energy", Q11423: "mass", Q41273: "momentum",
  Q2305665: "conservation of momentum",
  Q134465: "Newton's law of universal gravitation", Q161635: "angular velocity",
};

const readJsonl = (p) =>
  readFileSync(p, "utf8").split("\n").filter((l) => l.trim() && !l.startsWith("#")).map((l) => JSON.parse(l));

export function createGapGraph(spineDir) {
  const edges = readJsonl(join(spineDir, "prereq_edges.jsonl"))
    .filter((e) => (e.type || "prerequisite") === "prerequisite");

  const ids = [...new Set(edges.flatMap((e) => [e.from, e.to]))];
  const name = new Map(ids.map((id) => [id, WIKILABEL[id] || id]));
  // crosswalk labels supplement any node we don't have a Wikidata label for
  try {
    for (const r of readJsonl(join(spineDir, "crosswalk.jsonl")))
      if (r.node && r.label && !WIKILABEL[r.node]) name.set(r.node, r.label);
  } catch {}

  const n2i = new Map();
  for (const [id, nm] of name) n2i.set(nm.toLowerCase().trim(), id);
  for (const id of ids) n2i.set(id.toLowerCase(), id); // accept a raw Q-id too

  // prereqOf[target] = [source...]   (target's direct prerequisites)
  const prereqOf = new Map(ids.map((id) => [id, []]));
  for (const e of edges) prereqOf.get(e.to).push(e.from);

  const resolve = (concept) => {
    if (!concept) return null;
    const k = String(concept).toLowerCase().trim();
    if (n2i.has(k)) return n2i.get(k);
    for (const [nm, id] of n2i) if (nm.startsWith(k) || k.startsWith(nm)) return id;
    for (const [nm, id] of n2i) if (nm.includes(k) || k.includes(nm)) return id;
    return null;
  };
  const nameOf = (id) => name.get(id) || id;

  function prerequisitesOf(concept, { recursive = false } = {}) {
    const id = resolve(concept);
    if (!id) return [];
    if (!recursive) return prereqOf.get(id).map(nameOf);
    const acc = [], seen = new Set([id]);
    let layer = prereqOf.get(id).slice();
    while (layer.length) {
      const next = [];
      for (const p of layer) { if (seen.has(p)) continue; seen.add(p); acc.push(nameOf(p)); next.push(...prereqOf.get(p)); }
      layer = next;
    }
    return acc;
  }

  // Diagnose from passed/failed CONCEPT names. Root cause = the deepest
  // prerequisite the student actually FAILED (confirmed) — never an untested one.
  function diagnose(passedNames = [], failedNames = []) {
    const passed = new Set(passedNames.map(resolve).filter(Boolean));
    const failed = new Set(failedNames.map(resolve).filter(Boolean));
    const unresolved = [...passedNames, ...failedNames].filter((n) => !resolve(n));
    const statusOf = (id) => (passed.has(id) ? "passed" : failed.has(id) ? "failed" : "untested");

    const perFailed = [...failed].map((failId) => {
      const chain = []; const seen = new Set([failId]); let depth = 0;
      let layer = prereqOf.get(failId).slice();
      while (layer.length) {
        depth++; const next = [];
        for (const p of layer) { if (seen.has(p)) continue; seen.add(p); chain.push({ id: p, status: statusOf(p), depth }); next.push(...prereqOf.get(p)); }
        layer = next;
      }
      const failedPre = chain.filter((c) => c.status === "failed");
      const root = failedPre.length ? failedPre.reduce((a, b) => (b.depth > a.depth ? b : a)) : null;
      return {
        failed_concept: nameOf(failId),
        blocking_prerequisite: root ? nameOf(root.id) : null,
        why_teach_this_first: root
          ? `The failure in "${nameOf(failId)}" traces back to "${nameOf(root.id)}", a prerequisite the student also missed.`
          : `"${nameOf(failId)}" has no confirmed unmet prerequisite — its prerequisites were not tested.`,
        short_chain: root ? [nameOf(root.id), nameOf(failId)] : [nameOf(failId)],
        confidence: root ? "high" : "low",
      };
    });

    const counts = new Map();
    for (const f of perFailed) if (f.blocking_prerequisite) {
      if (!counts.has(f.blocking_prerequisite)) counts.set(f.blocking_prerequisite, []);
      counts.get(f.blocking_prerequisite).push(f.failed_concept);
    }
    let shared = null;
    for (const [pre, blocked] of counts)
      if (blocked.length >= 2 && (!shared || blocked.length > shared.blocked_concepts.length))
        shared = {
          concept_name: pre, blocked_concepts: blocked,
          why_it_blocks_learning: `Several failed concepts (${blocked.join(", ")}) all rest on "${pre}". Fixing this one foundation unblocks them.`,
          recommended_first_teaching_focus: pre,
        };

    const confirmed = perFailed.filter((f) => f.blocking_prerequisite).length;
    const summary = failed.size === 0 ? "No failed concepts supplied."
      : `${failed.size} failed concept(s); ${confirmed} traced to an unmet prerequisite.`;
    return { perFailed, shared, unresolved, summary };
  }

  return { resolve, nameOf, prerequisitesOf, diagnose, names: () => [...name.values()] };
}
