// KST diagnostic engine — JavaScript port of spine/kst.py + spine/diagnose.py,
// for the Node MCP server (Cloud Run can't run the Python engine).
//
// Source of truth is the Python engine + its unit tests (spine/test_kst.py).
// This port is faithful and validated against it (see kst.test.mjs): knowledge
// structure = order ideals of the prerequisite DAG; BLIM slip/guess response
// model; Bayesian posterior over states; outer-fringe gap location; half-split
// next-item. Structure comes ONLY from prereq_edges; calibration ONLY from
// calibration.jsonl — the two KST inputs stay separate.
//
// States are represented as integer bitmasks over the node set (<= ~31 nodes).

import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

function readJsonl(path) {
  const out = [];
  for (const line of readFileSync(path, "utf8").split("\n")) {
    const s = line.trim();
    if (!s || s.startsWith("#")) continue;
    out.push(JSON.parse(s));
  }
  return out;
}

// ---- structure: prerequisite DAG -> knowledge states (order ideals) ----
function buildStructure(edges) {
  const order = [];
  const seen = new Set();
  for (const e of edges) {
    if ((e.type || "prerequisite") !== "prerequisite") continue;
    for (const x of [e.from, e.to]) if (!seen.has(x)) { seen.add(x); order.push(x); }
  }
  const idx = new Map(order.map((n, i) => [n, i]));
  const n = order.length;
  const predMask = new Array(n).fill(0);
  for (const e of edges) {
    if ((e.type || "prerequisite") !== "prerequisite") continue;
    predMask[idx.get(e.to)] |= 1 << idx.get(e.from);
  }
  // children adjacency (successors)
  const children = Array.from({ length: n }, () => []);
  for (let j = 0; j < n; j++)
    for (let i = 0; i < n; i++)
      if ((predMask[j] >> i) & 1) children[i].push(j);
  // topological depth
  const depth = new Array(n).fill(-1);
  const dfsDepth = (i) => {
    if (depth[i] >= 0) return depth[i];
    let d = 0;
    for (let p = 0; p < n; p++) if ((predMask[i] >> p) & 1) d = Math.max(d, 1 + dfsDepth(p));
    return (depth[i] = d);
  };
  for (let i = 0; i < n; i++) dfsDepth(i);

  // enumerate ideals via BFS: add a node iff all its prereqs are present
  const states = new Set([0]);
  const frontier = [0];
  while (frontier.length) {
    const k = frontier.pop();
    for (let i = 0; i < n; i++) {
      if ((k >> i) & 1) continue;
      if ((predMask[i] & k) === predMask[i]) {
        const k2 = k | (1 << i);
        if (!states.has(k2)) { states.add(k2); frontier.push(k2); }
      }
    }
  }
  return { order, idx, n, predMask, children, depth, states: [...states] };
}

function reaches(struct, src, targetSet) {
  if (targetSet.has(src)) return true;
  const seen = new Set([src]);
  const stack = [...struct.children[src]];
  while (stack.length) {
    const x = stack.pop();
    if (targetSet.has(x)) return true;
    if (!seen.has(x)) { seen.add(x); for (const c of struct.children[x]) stack.push(c); }
  }
  return false;
}

// ---- BLIM + Bayesian assessment ----
const pCorrect = (inState, slip, guess) => (inState ? 1 - slip : guess);

function posterior(struct, responses, items, calib) {
  const states = struct.states;
  let post = new Map(states.map((s) => [s, 1 / states.length]));
  for (const [itemId, correct] of responses) {
    const node = items.get(itemId);
    if (node == null) continue;
    const i = struct.idx.get(node);
    const c = calib.get(itemId) || { slip: 0.1, guess: 0.1 };
    const next = new Map();
    let Z = 0;
    for (const [k, w] of post) {
      const inState = i !== undefined && ((k >> i) & 1) === 1;
      const p = pCorrect(inState, c.slip, c.guess);
      const lik = correct ? p : 1 - p;
      const v = w * lik;
      next.set(k, v); Z += v;
    }
    if (Z <= 0) continue;
    for (const [k, v] of next) next.set(k, v / Z);
    post = next;
  }
  return post;
}

function predictedPCorrect(struct, post, itemId, items, calib) {
  const node = items.get(itemId);
  if (node == null) return null;
  const i = struct.idx.get(node);
  const c = calib.get(itemId) || { slip: 0.1, guess: 0.1 };
  let s = 0;
  for (const [k, w] of post) {
    const inState = i !== undefined && ((k >> i) & 1) === 1;
    s += w * pCorrect(inState, c.slip, c.guess);
  }
  return s;
}

function mapState(post) {
  let best = 0, bestKey = [-1, 0];
  for (const [k, w] of post) {
    const key = [w, -popcount(k)];
    if (key[0] > bestKey[0] || (key[0] === bestKey[0] && key[1] > bestKey[1])) { best = k; bestKey = key; }
  }
  return best;
}
const popcount = (x) => { let c = 0; while (x) { x &= x - 1; c++; } return c; };

function outerFringe(struct, mask) {
  const out = [];
  for (let i = 0; i < struct.n; i++)
    if (!((mask >> i) & 1) && (struct.predMask[i] & mask) === struct.predMask[i]) out.push(i);
  return out;
}

function locateGap(struct, responses, items, calib) {
  const post = posterior(struct, responses, items, calib);
  const K = mapState(post);
  const fringe = outerFringe(struct, K);
  const failed = new Set();
  for (const [itemId, correct] of responses) {
    if (correct) continue;
    const node = items.get(itemId);
    if (node != null && struct.idx.has(node)) failed.add(struct.idx.get(node));
  }
  const rank = (i) => [failed.size && reaches(struct, i, failed) ? 0 : 1, struct.depth[i], i];
  let primary = null;
  for (const i of fringe) {
    if (primary === null) { primary = i; continue; }
    const a = rank(i), b = rank(primary);
    if (a[0] < b[0] || (a[0] === b[0] && (a[1] < b[1] || (a[1] === b[1] && a[2] < b[2])))) primary = i;
  }
  return { post, K, fringe, primary, failed: [...failed], confidence: post.get(K) || 0 };
}

function nextItemIdx(struct, responses, items, calib, asked) {
  const post = posterior(struct, responses, items, calib);
  const seen = new Set(asked);
  for (const [id] of responses) seen.add(id);
  let best = null, bestGap = 2;
  for (const [itemId, node] of items) {
    if (node == null || seen.has(itemId)) continue;
    const p = predictedPCorrect(struct, post, itemId, items, calib);
    const gap = Math.abs(0.5 - p);
    if (gap < bestGap) { best = itemId; bestGap = gap; }
  }
  return best;
}

// ---- diagnostics facade (mirrors spine/diagnose.py) ----
export function createDiagnostics({ spineDir }) {
  const edges = readJsonl(join(spineDir, "prereq_edges.jsonl"));
  const struct = buildStructure(edges);
  // slug -> {concept_en, lesson, book_pages}, the 26 curriculum concepts
  // (from INDEX.json; library.json only carries the 6 video concepts).
  const concepts = JSON.parse(readFileSync(join(spineDir, "concepts.json"), "utf8"));

  const itemRows = readJsonl(join(spineDir, "items.jsonl"));
  const items = new Map(itemRows.map((r) => [r.item_id, r.node ?? null]));
  const itemMeta = new Map(itemRows.map((r) => [r.item_id, r]));
  const calib = new Map(
    readJsonl(join(spineDir, "calibration.jsonl")).map((r) => [r.item_id, { slip: r.slip, guess: r.guess }])
  );

  const crosswalk = readJsonl(join(spineDir, "crosswalk.jsonl"));
  const nodeToSlugs = new Map();
  const label = new Map();
  for (const r of crosswalk) {
    if (r.match !== "none" && r.node) {
      if (!nodeToSlugs.has(r.node)) nodeToSlugs.set(r.node, []);
      nodeToSlugs.get(r.node).push(r.slug);
      if (r.label) label.set(r.node, r.label);
    }
  }
  const teachableIdx = new Set(
    [...nodeToSlugs.keys()].filter((nd) => struct.idx.has(nd)).map((nd) => struct.idx.get(nd))
  );
  const nodeOf = (i) => struct.order[i];
  const labelOf = (nd) => label.get(nd) || nd;
  const conceptInfo = (slug) => {
    const c = concepts[slug] || {};
    return { slug, concept_en: c.concept_en, lesson: c.lesson, book_pages: c.book_pages };
  };

  function teachTarget(nodeIdx) {
    const nd = nodeOf(nodeIdx);
    const slugs = nodeToSlugs.get(nd);
    if (slugs && slugs.length) return { kind: "concept", payload: slugs.map(conceptInfo) };
    // floor node: nearest downstream teachable concept
    const seen = new Set([nodeIdx]);
    const q = [...struct.children[nodeIdx]];
    while (q.length) {
      const j = q.shift();
      if (seen.has(j)) continue;
      seen.add(j);
      const s = nodeToSlugs.get(nodeOf(j));
      if (s && s.length) return { kind: "prerequisite", payload: { node: nd, label: labelOf(nd), motivates: conceptInfo(s[0]) } };
      for (const c of struct.children[j]) q.push(c);
    }
    return { kind: "prerequisite", payload: { node: nd, label: labelOf(nd), motivates: null } };
  }

  function teachingTarget(g) {
    const mastered = g.K;
    const failed = new Set(g.failed);
    let best = null;
    for (const i of teachableIdx) {
      if ((mastered >> i) & 1) continue;
      if (failed.has(i) || (failed.size && reaches(struct, i, failed))) {
        if (best === null || struct.depth[i] < struct.depth[best] || (struct.depth[i] === struct.depth[best] && i < best)) best = i;
      }
    }
    return best !== null ? best : g.primary;
  }

  function diagnose(responses) {
    const resp = responses.map((r) => [r.item_id, !!r.correct]);
    const g = locateGap(struct, resp, items, calib);
    const used = resp.filter(([id]) => items.get(id) != null).length;
    const result = {
      n_states: struct.states.length,
      confidence: Math.round(g.confidence * 1e4) / 1e4,
      responses_used: used,
      responses_ignored: resp.length - used,
      structural_gap: g.primary != null ? { node: nodeOf(g.primary), label: labelOf(nodeOf(g.primary)) } : null,
      failed_nodes: g.failed.map((i) => ({ node: nodeOf(i), label: labelOf(nodeOf(i)) })),
      fringe: g.fringe.map((i) => ({ node: nodeOf(i), label: labelOf(nodeOf(i)) })),
    };
    const target = teachingTarget(g);
    if (target == null) {
      return { ...result, status: "no_gap", gap_node: null,
        message: "No gap located: the student's mastery spans the assessed spine." };
    }
    const tt = teachTarget(target);
    result.gap_node = nodeOf(target);
    result.gap_label = labelOf(nodeOf(target));
    result.status = "gap_located";
    result.teach_kind = tt.kind;
    result.teach = tt.payload;
    if (tt.kind === "concept") {
      const primary = tt.payload[0];
      Object.assign(result, { slug: primary.slug, lesson: primary.lesson,
        book_pages: primary.book_pages, concept_en: primary.concept_en });
      if (tt.payload.length > 1) result.note = `teaching node maps to multiple collapsed concepts: ${tt.payload.map((p) => p.slug).join(", ")}`;
    } else {
      result.note = "gap is a prerequisite/math-floor node with no Physics-2 lesson; teach the prerequisite, motivated by the concept it unlocks.";
    }
    const structuralNode = result.structural_gap && result.structural_gap.node;
    if (structuralNode && structuralNode !== result.gap_node) {
      result.note = ((result.note || "") +
        ` KST structural gap is deeper (${result.structural_gap.label}); intermediate nodes carry no items, so the teachable target is reported. Low confidence reflects sparse item coverage.`).trim();
    }
    return result;
  }

  function suggestNext(responses) {
    const resp = responses.map((r) => [r.item_id, !!r.correct]);
    const id = nextItemIdx(struct, resp, items, calib, []);
    if (!id) return { next_item: null };
    const m = itemMeta.get(id) || {};
    return { next_item: { item_id: id, lesson: m.lesson, node: m.node, qkind: m.qkind, printed_number: m.printed_number } };
  }

  return { diagnose, suggestNext, _struct: struct, _items: items, _calib: calib };
}
