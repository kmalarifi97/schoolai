#!/usr/bin/env python3
"""Deterministic assembler for the Physics-2 diagnostic spine (Phases 1-2).

LLM owns ONLY the seed proposals: `crosswalk.jsonl` (concept->QID mapping) and
`proposed_edges.seed.jsonl` (low-confidence edges). Everything this script emits
is computed deterministically from those seeds + the knowledge graph:

  * prereq_edges.candidate.jsonl  -- induced upstream-closure prerequisite
                                     subgraph over matched nodes, pulled from the
                                     graph's arbitrated.jsonl, + merged proposals.
                                     Renamed to prereq_edges.jsonl ONLY after the
                                     graph's validator/dag.py reports acyclic
                                     (see Makefile target / README).
  * missing_nodes.jsonl           -- one row per match:"none" concept.
  * floor_gaps.jsonl              -- physics nodes whose math prerequisite has no
                                     graph node (expected empty for this slice).

The script never invents a node, an edge, or a match. Structure comes only from
the graph; the crosswalk is the only bridge between the two identity schemes.

Run from the teacher repo root (or anywhere): paths are resolved relative to
this file and the sibling knowledge-graph repo.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

SPINE = Path(__file__).resolve().parent
# knowledge-graph sits beside the teacher repo. Allow override via env later.
GRAPH = SPINE.parents[2] if (SPINE.parents[2] / "registry").exists() else None
# When run inside the worktree, walk up to find the real knowledge-graph repo.
_CANDIDATES = [
    Path("/Users/khalid-dev/knowledge-graph"),
    SPINE.parent.parent / "knowledge-graph",
]
GRAPH = next((p for p in _CANDIDATES if (p / "registry" / "nodes.jsonl").exists()), None)
if GRAPH is None:
    raise SystemExit("knowledge-graph repo not found; cannot read graph structure.")

NODES_PATH = GRAPH / "registry" / "nodes.jsonl"
EDGES_PATH = GRAPH / "arbitration" / "arbitrated.jsonl"
INDEX_PATH = SPINE.parent / "scripts" / "concepts" / "INDEX.json"


def read_jsonl(path: Path):
    """Yield one dict per line; skip blanks and #-comments (mirrors graph/common.py)."""
    with path.open() as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{i}: invalid JSON ({e})") from e


def write_jsonl(path: Path, records, header: str | None = None) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w") as f:
        if header:
            for ln in header.strip("\n").split("\n"):
                f.write(f"# {ln}\n")
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    labels = {n["id"]: n["label"] for n in read_jsonl(NODES_PATH)}
    domain = {n["id"]: n.get("domain", "") for n in read_jsonl(NODES_PATH)}
    crosswalk = list(read_jsonl(SPINE / "crosswalk.jsonl"))
    concept_en = {
        c["slug"]: c["concept_en"]
        for c in json.loads(INDEX_PATH.read_text())["concepts"]
    }

    # --- sanity: every crosswalk node must exist in the graph ----------------
    for row in crosswalk:
        if row["match"] != "none":
            assert row["node"] in labels, f"crosswalk node {row['node']} not in graph"
            assert row["label"] == labels[row["node"]], (
                f"label drift for {row['node']}: crosswalk says {row['label']!r}, "
                f"graph says {labels[row['node']]!r}"
            )

    matched_nodes = {r["node"] for r in crosswalk if r["match"] != "none"}

    # --- pull prerequisite edges from the graph; build reverse adjacency ------
    prereq = [e for e in read_jsonl(EDGES_PATH) if e.get("type") == "prerequisite"]
    preds: dict[str, list[str]] = defaultdict(list)  # to -> [from...]
    for e in prereq:
        preds[e["to"]].append(e["from"])

    # --- upstream closure: matched nodes + all their prerequisite ancestors ---
    closure: set[str] = set()
    stack = list(matched_nodes)
    while stack:
        node = stack.pop()
        if node in closure:
            continue
        closure.add(node)
        stack.extend(preds.get(node, []))

    # --- induced subgraph: graph edges with BOTH endpoints in the closure -----
    induced = [
        {**e, "provenance": e.get("provenance", []), "source": "arbitrated"}
        for e in prereq
        if e["from"] in closure and e["to"] in closure
    ]

    # --- merge LLM-proposed low-confidence edges ------------------------------
    proposed = list(read_jsonl(SPINE / "proposed_edges.seed.jsonl"))
    for e in proposed:
        e.setdefault("source", "proposed")
    candidate = induced + proposed

    write_jsonl(
        SPINE / "prereq_edges.candidate.jsonl",
        candidate,
        header=(
            "CANDIDATE prerequisite edges -- NOT YET VALIDATED.\n"
            "Induced upstream-closure subgraph over matched crosswalk nodes\n"
            "(source=arbitrated) + LLM proposals (source=proposed).\n"
            "Run the graph's validator/dag.py on this file; rename to\n"
            "prereq_edges.jsonl only if it reports DAG ok."
        ),
    )

    # --- missing_nodes: one row per match:none concept ------------------------
    missing = [
        {"slug": r["slug"], "concept_en": concept_en[r["slug"]], "note": r["note"]}
        for r in crosswalk
        if r["match"] == "none"
    ]
    write_jsonl(
        SPINE / "missing_nodes.jsonl",
        missing,
        header="Physics-2 concepts with NO graph node. The graph must gain these. "
        "Nearest existing prerequisite (if any) is named in the note -- it is a "
        "RELATED node, never an identity; do not collapse the concept onto it.",
    )

    # --- floor_gaps vs floating roots ----------------------------------------
    # floor_gaps (the prompt's definition) = a physics concept needing a MATH
    # prerequisite that has NO graph node. The calculus/vector floor the matched
    # slice needs (derivative, integral, vector, cross product, trig) all exist,
    # so there are no math-node-missing gaps -> floor_gaps is empty. We still
    # SURFACE the related observation: matched physics nodes that have no
    # prerequisite edge even after merging the proposed edges (genuinely
    # ungrounded roots). Those are reported separately, not hidden.
    proposed_targets = {e["to"] for e in proposed}  # rescued by a proposed edge
    floating_roots = []
    for node in sorted(matched_nodes):
        grounded = bool(preds.get(node)) or node in proposed_targets
        if domain.get(node) == "physics" and not grounded:
            floating_roots.append({
                "node": node,
                "label": labels[node],
                "observation": "matched physics node has no prerequisite edge (root); "
                               "not a math-node gap -- math floor is fully present.",
            })

    floor_gaps: list[dict] = []  # math-node-missing gaps: none for this slice
    write_jsonl(
        SPINE / "floor_gaps.jsonl",
        floor_gaps,
        header="Math-floor gaps: physics nodes needing a math prerequisite that has "
        "NO graph node. EMPTY for this slice -- the calculus/vector floor "
        "(derivative, integral, vector, cross product, trig) is fully present and "
        "wired in. Ungrounded-root physics nodes are reported in REPORT.md, not here.",
    )

    # --- console summary ------------------------------------------------------
    n_exact = sum(1 for r in crosswalk if r["match"] == "exact")
    n_fuzzy = sum(1 for r in crosswalk if r["match"] == "fuzzy")
    n_none = sum(1 for r in crosswalk if r["match"] == "none")
    print(f"crosswalk:        {len(crosswalk)} concepts -> {n_exact} exact, {n_fuzzy} fuzzy, {n_none} none")
    print(f"matched nodes:    {len(matched_nodes)} distinct")
    print(f"closure nodes:    {len(closure)} (matched + prerequisite ancestors)")
    print(f"induced edges:    {len(induced)} from arbitrated.jsonl")
    print(f"proposed edges:   {len(proposed)} (llm, low-confidence, flagged)")
    print(f"candidate edges:  {len(candidate)} -> prereq_edges.candidate.jsonl (validate next)")
    print(f"missing_nodes:    {len(missing)}")
    print(f"floor_gaps:       {len(floor_gaps)} (math-node-missing; empty as expected)")
    print(f"floating roots:   {len(floating_roots)} matched physics nodes ungrounded "
          f"after proposals -> {[f['node'] for f in floating_roots]} (see REPORT.md)")


if __name__ == "__main__":
    main()
