#!/usr/bin/env python3
"""Phase 3-4 assembler: book questions -> KST item bank + calibration.

Deterministic. Reads the extracted lessons (NEVER writes them), the Phase-1
crosswalk, and INDEX.json, and emits:

  * items.jsonl            -- one row per question, linked to a concept node
                              where resolvable (see resolution grades below).
  * items_unresolved.jsonl -- the flagged subset (ambiguous / unresolved).
  * calibration.jsonl      -- per-item slip/guess.

DATA REALITY (surfaced, not hidden): the questions do NOT carry usable
`concept_tags` (6/688) or `difficulty` (0/688). Items are therefore linked at
LESSON granularity via INDEX.json (concept -> lesson), and the resolution grade
records how trustworthy each link is. Nothing is force-fit to a single node.

Resolution grades:
  lesson-exact          lesson has exactly one concept and it is matched -> node
  lesson-single-matched lesson has one matched concept (+ other unmatched) -> node
  lesson-ambiguous      lesson has >=2 matched concept-nodes -> node=null, candidates
  unresolved            lesson has zero matched concepts -> node=null

Calibration: no open dataset provided at runtime -> ALL source="default".
  slip = 0.10 ; guess by qkind: mcq 0.25, true_false 0.50, else 0.05.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

SPINE = Path(__file__).resolve().parent
REPO = SPINE.parent
LESSONS = REPO / "chatgpt-app" / "data" / "lesson_pages"
INDEX = REPO / "scripts" / "concepts" / "INDEX.json"

GUESS_BY_QKIND = {"mcq": 0.25, "true_false": 0.50}
GUESS_DEFAULT = 0.05
SLIP_DEFAULT = 0.10


def read_jsonl(path):
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield json.loads(line)


def write_jsonl(path, rows, header=None):
    with path.open("w") as f:
        if header:
            for ln in header.strip("\n").split("\n"):
                f.write(f"# {ln}\n")
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    return len(rows)


def walk_questions(obj):
    out = []
    if isinstance(obj, dict):
        if obj.get("type") == "question" or "qkind" in obj:
            out.append(obj)
        for v in obj.values():
            out += walk_questions(v)
    elif isinstance(obj, list):
        for v in obj:
            out += walk_questions(v)
    return out


def main():
    concepts = json.loads(INDEX.read_text())["concepts"]
    lesson_of = {c["slug"]: c["lesson"] for c in concepts}
    concepts_in_lesson = defaultdict(list)
    for c in concepts:
        concepts_in_lesson[c["lesson"]].append(c["slug"])

    crosswalk = {r["slug"]: r for r in read_jsonl(SPINE / "crosswalk.jsonl")}
    # matched concept-nodes present in each lesson
    lesson_nodes = {}
    for lesson, slugs in concepts_in_lesson.items():
        nodes = []
        for s in slugs:
            row = crosswalk.get(s)
            if row and row["match"] != "none":
                nodes.append(row["node"])
        lesson_nodes[lesson] = sorted(set(nodes))

    items, unresolved, calibration = [], [], []
    cov = Counter()
    res_counts = Counter()

    for f in sorted(LESSONS.glob("[0-9]*.json")):
        data = json.loads(f.read_text())
        lesson = data["lesson_id"]
        n_concepts = len(concepts_in_lesson.get(lesson, []))
        matched = lesson_nodes.get(lesson, [])
        for q in walk_questions(data):
            qid = q["id"]
            qkind = q.get("qkind", "")
            node = None
            candidates = []
            if len(matched) == 1:
                node = matched[0]
                resolution = "lesson-exact" if n_concepts == 1 else "lesson-single-matched"
            elif len(matched) >= 2:
                resolution = "lesson-ambiguous"
                candidates = matched
            else:
                resolution = "unresolved"
            flag = resolution in ("lesson-ambiguous", "unresolved")

            item = {
                "item_id": qid,
                "lesson": lesson,
                "qkind": qkind,
                "printed_number": q.get("printed_number", ""),
                "page": q.get("page"),
                "node": node,
                "resolution": resolution,
                "candidate_nodes": candidates,
                "flag": flag,
            }
            items.append(item)
            res_counts[resolution] += 1
            if node:
                cov[node] += 1
            if flag:
                unresolved.append({k: item[k] for k in
                                   ("item_id", "lesson", "qkind", "resolution", "candidate_nodes")})

            guess = GUESS_BY_QKIND.get(qkind, GUESS_DEFAULT)
            calibration.append({
                "item_id": qid,
                "slip": SLIP_DEFAULT,
                "guess": guess,
                "source": "default",
                "note": "no open dataset wired; flat default. Replaceable per-item by real data.",
            })

    write_jsonl(SPINE / "items.jsonl", items,
                header="KST item bank from book questions. node=null when the lesson "
                "does not resolve to a single matched concept (see resolution/flag). "
                "Items are linked by LESSON, not concept_tags (those are absent); "
                "nothing is force-fit.")
    write_jsonl(SPINE / "items_unresolved.jsonl", unresolved,
                header="Flagged items: ambiguous (>=2 matched concepts in the lesson) "
                "or unresolved (0 matched concepts). For review; not dropped.")
    write_jsonl(SPINE / "calibration.jsonl", calibration,
                header="Per-item slip/guess. source=default for ALL (no open dataset "
                "provided at runtime). slip=0.10; guess by qkind. Borrowed=0 -- flagged.")

    # ---- summary ------------------------------------------------------------
    labels = {}
    nodes_path = next((p for p in [Path("/Users/khalid-dev/knowledge-graph/registry/nodes.jsonl")]
                       if p.exists()), None)
    if nodes_path:
        labels = {n["id"]: n["label"] for n in read_jsonl(nodes_path)}
    print(f"questions -> items: {len(items)}")
    for r in ("lesson-exact", "lesson-single-matched", "lesson-ambiguous", "unresolved"):
        print(f"  {r:22s}: {res_counts[r]}")
    resolved = res_counts['lesson-exact'] + res_counts['lesson-single-matched']
    print(f"resolved to a single node: {resolved}   flagged: {len(unresolved)}")
    print(f"calibration rows: {len(calibration)} (all source=default)")
    print("item coverage per node:")
    for node, c in sorted(cov.items(), key=lambda kv: -kv[1]):
        print(f"  {node:10s} {labels.get(node,''):28s} {c}")


if __name__ == "__main__":
    main()
