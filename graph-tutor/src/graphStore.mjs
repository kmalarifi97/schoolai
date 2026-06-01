// graphStore — loads a prerequisite graph (JSON) and answers traversal +
// diagnosis queries by walking the edges directly. No KST state space, no
// bitmasks: the graph is explicit, so diagnosis is just backward traversal.
//
// Edge semantics: {source, target} means source is a PREREQUISITE of target.
// "prerequisites of X" = sources of edges whose target is X (walk edges in
// reverse, recursively). This module is the single source of truth the GraphQL
// resolvers and (indirectly) the MCP tools sit on top of.
//
// Pluggable by design: swap loadGraph() for a Neo4j-backed implementation and
// the GraphQL layer above does not change.

import { readFileSync } from "node:fs";

export function createGraphStore(graphPath) {
  const raw = JSON.parse(readFileSync(graphPath, "utf8"));
  const nodes = new Map(raw.nodes.map((n) => [n.id, n]));
  const edges = raw.edges.slice();

  // adjacency: prereqOf[target] = [source...]  (target's direct prerequisites)
  //            unlocks[source]  = [target...]  (skills that depend on source)
  const prereqOf = new Map([...nodes.keys()].map((id) => [id, []]));
  const unlocks = new Map([...nodes.keys()].map((id) => [id, []]));
  for (const e of edges) {
    if (!nodes.has(e.source) || !nodes.has(e.target)) continue;
    prereqOf.get(e.target).push(e.source);
    unlocks.get(e.source).push(e.target);
  }

  const node = (id) => nodes.get(id) || null;
  const allNodes = () => [...nodes.values()];
  const allEdges = () => edges;

  // direct or recursive prerequisites of `id`, nearest-first (BFS).
  function prerequisitesOf(id, { recursive = false } = {}) {
    if (!nodes.has(id)) return [];
    if (!recursive) return prereqOf.get(id).map(node);
    const out = [];
    const seen = new Set([id]);
    let layer = prereqOf.get(id).slice();
    while (layer.length) {
      const next = [];
      for (const p of layer) {
        if (seen.has(p)) continue;
        seen.add(p);
        out.push(node(p));
        next.push(...prereqOf.get(p));
      }
      layer = next;
    }
    return out;
  }

  function dependentsOf(id) {
    if (!nodes.has(id)) return [];
    return unlocks.get(id).map(node);
  }

  // cycle check (the empirical builder should emit a DAG; verify anyway).
  function findCycles() {
    const WHITE = 0, GRAY = 1, BLACK = 2;
    const color = new Map([...nodes.keys()].map((id) => [id, WHITE]));
    const cycles = [];
    const stack = [];
    const visit = (u) => {
      color.set(u, GRAY); stack.push(u);
      for (const v of unlocks.get(u)) {
        if (color.get(v) === GRAY) cycles.push([...stack.slice(stack.indexOf(v)), v]);
        else if (color.get(v) === WHITE) visit(v);
      }
      stack.pop(); color.set(u, BLACK);
    };
    for (const id of nodes.keys()) if (color.get(id) === WHITE) visit(id);
    return cycles;
  }

  // ---- diagnosis: direct graph traversal ----
  // Given quiz results (passed / failed skill ids), for each FAILED skill walk
  // its prerequisite chain backward and surface the prerequisites the student
  // has NOT mastered. status: "failed" (also missed) > "untested" (unknown) >
  // "passed" (fine). Root cause = the deepest not-mastered prerequisite —
  // teach that first, then climb back to the failed skill.
  function diagnose({ passed = [], failed = [] } = {}) {
    const passedSet = new Set(passed.filter((id) => nodes.has(id)));
    const failedSet = new Set(failed.filter((id) => nodes.has(id)));
    const statusOf = (id) =>
      passedSet.has(id) ? "passed" : failedSet.has(id) ? "failed" : "untested";

    const perFailed = [...failedSet].map((failId) => {
      // BFS back over prerequisites, recording depth.
      const chain = [];
      const seen = new Set([failId]);
      let depth = 0;
      let layer = prereqOf.get(failId).slice();
      while (layer.length) {
        depth += 1;
        const next = [];
        for (const p of layer) {
          if (seen.has(p)) continue;
          seen.add(p);
          chain.push({ id: p, name: node(p).name, status: statusOf(p), depth });
          next.push(...prereqOf.get(p));
        }
        layer = next;
      }
      const notMastered = chain.filter((c) => c.status !== "passed");
      const failName = node(failId).name;

      // Root cause prefers CONFIRMED gaps (failed) over UNKNOWN ones (untested):
      // we never assert a gap on a skill we didn't test. Among confirmed failures
      // we pick the DEEPEST — the most foundational confirmed weakness, taught
      // first. If only untested prerequisites remain, we don't guess: we tell the
      // teacher to probe the nearest unknown(s) instead.
      const failedPrereqs = notMastered.filter((c) => c.status === "failed");
      let rootCause = null;
      let recommendation;
      if (failedPrereqs.length) {
        rootCause = failedPrereqs.reduce((a, b) => (b.depth > a.depth ? b : a));
        recommendation = `Before retrying "${failName}", master "${rootCause.name}" first — it is the deepest prerequisite the student failed.`;
      } else if (notMastered.length) {
        const minDepth = Math.min(...notMastered.map((c) => c.depth));
        const nearest = notMastered.filter((c) => c.depth === minDepth);
        recommendation = `"${failName}" failed, but its prerequisites were not tested. Quiz ${nearest.map((n) => `"${n.name}"`).join(", ")} to locate the actual gap.`;
      } else {
        recommendation = `"${failName}" has no unmet prerequisites in the graph — review the skill itself directly.`;
      }

      return {
        skill: node(failId),
        rootCause: rootCause ? node(rootCause.id) : null,
        chain,            // prerequisites, nearest-first, with status + depth
        notMastered,      // subset that blocks progress
        recommendation,
      };
    });

    const blocked = perFailed.filter((f) => f.rootCause).length;
    const summary =
      failedSet.size === 0
        ? "No failed skills supplied — nothing to diagnose."
        : `${failedSet.size} failed skill(s); ${blocked} traced to an unmet prerequisite.`;

    return { failed: perFailed, summary };
  }

  return {
    meta: raw.meta || {},
    node,
    allNodes,
    allEdges,
    prerequisitesOf,
    dependentsOf,
    findCycles,
    diagnose,
  };
}
