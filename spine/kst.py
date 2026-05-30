#!/usr/bin/env python3
"""Knowledge Space Theory engine for the Physics-2 diagnostic spine (Phase 5).

Pure functions, stdlib only. Two inputs kept strictly separate, exactly as KST
requires:

  * STRUCTURE  — which knowledge states are possible. Derived ONLY from the
                 prerequisite DAG (the graph). See `knowledge_states`.
  * CALIBRATION — per-item slip/guess. Derived ONLY from response data (the
                 dataset / defaults). Passed in as a dict, never inferred here.

The engine combines structure + calibration + a student's answers to locate the
gap. It is the deterministic authority; the LLM never decides the structure.

Algorithms (cited to Doignon & Falmagne, *Knowledge Spaces* / *Learning Spaces*):
  * knowledge_states  -> the knowledge structure as the family of order ideals
                         (downward-closed sets) of the prerequisite order. For a
                         partial order this family is a quasi-ordinal knowledge
                         space, closed under union and intersection (Birkhoff's
                         representation; D&F ch. 3).
  * p_correct         -> Basic Local Independence Model (BLIM): a single item's
                         response depends only on whether its node is in the
                         state, via that item's slip (beta) and guess (eta).
                         (D&F ch. 11 / Falmagne-Doignon BLIM.)
  * posterior         -> Bayesian update of the likelihood over states given
                         observed responses (the stochastic assessment kernel,
                         D&F ch. 13 / ch. 10 questioning).
  * next_item         -> half-split questioning rule: ask the item whose
                         predicted P(correct) under the current belief is closest
                         to 1/2 (maximally informative single question).
  * locate_gap        -> the outer fringe of the most likely state: the nodes a
                         learner is "ready to learn" (all prerequisites mastered,
                         node itself not). The fringe is the teachable gap.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass


# ----------------------------------------------------------------------------
# Structure: prerequisite order -> knowledge states (order ideals)
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Structure:
    nodes: tuple                      # all node ids
    preds: dict                       # node -> frozenset(direct prerequisites)
    succ: dict                        # node -> frozenset(direct successors)
    depth: dict                       # node -> topological depth (roots = 0)
    states: tuple                     # tuple of frozensets, the knowledge states

    def reaches(self, src, targets):
        """True if any node in `targets` is reachable from src via successors."""
        if src in targets:
            return True
        seen, stack = {src}, list(self.succ.get(src, ()))
        while stack:
            n = stack.pop()
            if n in targets:
                return True
            if n not in seen:
                seen.add(n)
                stack.extend(self.succ.get(n, ()))
        return False


def _direct_preds(nodes, edges):
    preds = {n: set() for n in nodes}
    for e in edges:
        if e.get("type", "prerequisite") != "prerequisite":
            continue
        preds[e["to"]].add(e["from"])
    return {n: frozenset(p) for n, p in preds.items()}


def _depths(nodes, preds):
    depth, seen = {}, {}

    def d(n, stack=()):
        if n in depth:
            return depth[n]
        if not preds[n]:
            depth[n] = 0
            return 0
        depth[n] = 1 + max(d(p) for p in preds[n])
        return depth[n]

    for n in nodes:
        d(n)
    return depth


def knowledge_states(edges, nodes=None, max_states=200_000):
    """Enumerate the knowledge structure: all downward-closed sets of the
    prerequisite order. A set K is a state iff every node in K has all of its
    prerequisites in K (you cannot know a thing without its prerequisites).

    Raises ValueError if the count would exceed `max_states` (caller should then
    restrict the structure to a relevant sub-order; see diagnose.py).
    """
    if nodes is None:
        nodes = []
        seen = set()
        for e in edges:
            for x in (e["from"], e["to"]):
                if x not in seen:
                    seen.add(x)
                    nodes.append(x)
    nodes = tuple(nodes)
    preds = _direct_preds(nodes, edges)

    # BFS over ideals: start from the empty state, add any node all of whose
    # prerequisites are already present. Every ideal is reachable this way (add
    # elements along any linear extension).
    empty = frozenset()
    states = {empty}
    frontier = [empty]
    while frontier:
        K = frontier.pop()
        for n in nodes:
            if n in K:
                continue
            if preds[n] <= K:
                K2 = K | {n}
                if K2 not in states:
                    states.add(K2)
                    frontier.append(K2)
                    if len(states) > max_states:
                        raise ValueError(
                            f"knowledge structure exceeds {max_states} states; "
                            "restrict to a sub-order before enumerating."
                        )
    depth = _depths(nodes, preds)
    succ = {n: set() for n in nodes}
    for n in nodes:
        for p in preds[n]:
            succ[p].add(n)
    succ = {n: frozenset(s) for n, s in succ.items()}
    # Stable ordering: by size then by sorted contents.
    ordered = tuple(sorted(states, key=lambda s: (len(s), sorted(s))))
    return Structure(nodes=nodes, preds=preds, succ=succ, depth=depth, states=ordered)


# ----------------------------------------------------------------------------
# Response model (BLIM) + Bayesian assessment
# ----------------------------------------------------------------------------

def p_correct(node_in_state: bool, slip: float, guess: float) -> float:
    """BLIM: P(correct | state). Knows the node -> 1-slip; doesn't -> guess."""
    return (1.0 - slip) if node_in_state else guess


def posterior(structure: Structure, responses, items, calib, prior=None):
    """Bayesian posterior over knowledge states given observed responses.

    responses : iterable of (item_id, correct: bool)
    items     : item_id -> node id (the node the item assesses; None items skipped)
    calib     : item_id -> {"slip":.., "guess":..}
    prior     : optional state -> weight; defaults to uniform.
    Returns: dict state(frozenset) -> normalized probability.
    """
    states = structure.states
    if prior is None:
        post = {K: 1.0 / len(states) for K in states}
    else:
        Z = sum(prior.values())
        post = {K: prior.get(K, 0.0) / Z for K in states}

    for item_id, correct in responses:
        node = items.get(item_id)
        if node is None:
            continue  # unresolved/ambiguous item carries no structural signal
        c = calib.get(item_id, {"slip": 0.10, "guess": 0.10})
        slip, guess = c["slip"], c["guess"]
        new = {}
        for K, w in post.items():
            if w == 0.0:
                new[K] = 0.0
                continue
            p = p_correct(node in K, slip, guess)
            lik = p if correct else (1.0 - p)
            new[K] = w * lik
        Z = sum(new.values())
        if Z <= 0:
            # Degenerate (impossible under model); keep prior rather than divide by 0.
            continue
        post = {K: w / Z for K, w in new.items()}
    return post


def predicted_p_correct(structure, post, item_id, items, calib):
    """Belief-weighted P(correct) for an item under the current posterior."""
    node = items.get(item_id)
    if node is None:
        return None
    c = calib.get(item_id, {"slip": 0.10, "guess": 0.10})
    return sum(w * p_correct(node in K, c["slip"], c["guess"])
               for K, w in post.items())


def next_item(structure, responses, items, calib, asked=()):
    """Half-split rule: among unasked, resolvable items, pick the one whose
    predicted P(correct) is closest to 0.5 (the most informative question)."""
    post = posterior(structure, responses, items, calib)
    asked = set(asked) | {r[0] for r in responses}
    best, best_gap = None, 2.0
    for item_id, node in items.items():
        if node is None or item_id in asked:
            continue
        p = predicted_p_correct(structure, post, item_id, items, calib)
        gap = abs(0.5 - p)
        if gap < best_gap:
            best, best_gap = item_id, gap
    return best


def map_state(structure, post):
    """Maximum-a-posteriori knowledge state."""
    return max(post.items(), key=lambda kv: (kv[1], -len(kv[0])))[0]


def outer_fringe(structure, state):
    """Nodes the learner is ready to learn: not yet known, all prereqs known."""
    return [n for n in structure.nodes
            if n not in state and structure.preds[n] <= state]


def marginal_mastery(structure, post):
    """Per-node P(node is in the student's state)."""
    m = defaultdict(float)
    for K, w in post.items():
        for n in K:
            m[n] += w
    return {n: m.get(n, 0.0) for n in structure.nodes}


def locate_gap(structure, responses, items, calib, confident=0.0):
    """Locate the diagnostic gap.

    Returns dict with the MAP state, its outer fringe, the primary gap (most
    foundational fringe node = lowest topological depth), per-node mastery, and a
    confidence = posterior mass on the MAP state.
    """
    post = posterior(structure, responses, items, calib)
    K = map_state(structure, post)
    fringe = outer_fringe(structure, K)

    # Nodes the student demonstrably failed (an item on them answered wrong).
    failed = frozenset(structure_node for (item_id, correct) in responses
                       if not correct and (structure_node := items.get(item_id)))

    # Primary gap: the most foundational unmet prerequisite ON THE PATH to a
    # concept the student actually failed. This avoids sending a student who
    # missed momentum to an unrelated root (e.g. Potential energy) when the
    # posterior is diffuse because intermediate nodes carry no items. If nothing
    # failed (or no fringe node leads to a failure), fall back to global depth.
    def rank(n):
        return (0 if (failed and structure.reaches(n, failed)) else 1,
                structure.depth[n], n)
    primary = min(fringe, key=rank) if fringe else None

    return {
        "map_state": K,
        "fringe": fringe,
        "primary_gap": primary,
        "confidence": post.get(K, 0.0),
        "failed_nodes": sorted(failed),
        "mastery": marginal_mastery(structure, post),
        "n_states": len(structure.states),
    }
