#!/usr/bin/env python3
"""Phase 6 glue: turn a student's answers into a teachable gap.

Loads the spine (structure + items + calibration + crosswalk + concept index),
runs the deterministic KST engine (kst.py), and maps the located gap node back to
a Physics-2 lesson the tutor can teach.

Pure-ish: reads files under a root dir, no network, no mutation. The backend
imports `diagnose` and `next_item_for`; logging lives in the backend, not here.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

import kst


def _root(root=None) -> Path:
    if root:
        return Path(root)
    env = os.environ.get("LIB_ROOT")
    if env and (Path(env) / "spine").exists():
        return Path(env)
    return Path(__file__).resolve().parent.parent  # repo root


def _read_jsonl(path: Path):
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield json.loads(line)


@lru_cache(maxsize=8)
def load_spine(root_str: str):
    """Load everything once per root. Cached; safe to call per request."""
    root = Path(root_str)
    spine = root / "spine"
    edges = list(_read_jsonl(spine / "prereq_edges.jsonl"))
    structure = kst.knowledge_states(edges)

    items_rows = list(_read_jsonl(spine / "items.jsonl"))
    items = {r["item_id"]: r["node"] for r in items_rows}
    item_meta = {r["item_id"]: r for r in items_rows}
    calib = {r["item_id"]: {"slip": r["slip"], "guess": r["guess"]}
             for r in _read_jsonl(spine / "calibration.jsonl")}

    crosswalk = list(_read_jsonl(spine / "crosswalk.jsonl"))
    node_to_slugs = {}
    for r in crosswalk:
        if r["match"] != "none" and r["node"]:
            node_to_slugs.setdefault(r["node"], []).append(r["slug"])

    index = json.loads((root / "scripts" / "concepts" / "INDEX.json").read_text())
    concept = {c["slug"]: c for c in index["concepts"]}

    # node labels (best-effort; graph repo may not be mounted in prod)
    labels = {}
    for cand in (Path("/Users/khalid-dev/knowledge-graph/registry/nodes.jsonl"),
                 root.parent / "knowledge-graph" / "registry" / "nodes.jsonl"):
        if cand.exists():
            labels = {n["id"]: n["label"] for n in _read_jsonl(cand)}
            break

    # forward adjacency for "nearest downstream concept" search
    succ = {}
    for e in edges:
        if e.get("type", "prerequisite") == "prerequisite":
            succ.setdefault(e["from"], []).append(e["to"])

    return {
        "structure": structure, "items": items, "item_meta": item_meta,
        "calib": calib, "node_to_slugs": node_to_slugs, "concept": concept,
        "labels": labels, "succ": succ,
    }


def _teach_target(node, sp):
    """Map a node to a teachable concept. Returns (kind, payload)."""
    slugs = sp["node_to_slugs"].get(node)
    if slugs:
        # matched concept node -> teach it. (May be a collapse, e.g. PE -> gravpe+elasticpe.)
        out = []
        for s in slugs:
            c = sp["concept"].get(s, {})
            out.append({"slug": s, "concept_en": c.get("concept_en"),
                        "lesson": c.get("lesson"), "book_pages": c.get("book_pages")})
        return "concept", out
    # math-floor / primitive node: find nearest downstream matched concept to motivate it.
    seen, frontier = {node}, list(sp["succ"].get(node, []))
    while frontier:
        nxt = frontier.pop(0)
        if nxt in seen:
            continue
        seen.add(nxt)
        if nxt in sp["node_to_slugs"]:
            s = sp["node_to_slugs"][nxt][0]
            c = sp["concept"].get(s, {})
            return "prerequisite", {
                "node": node, "label": sp["labels"].get(node, node),
                "motivates": {"slug": s, "concept_en": c.get("concept_en"),
                              "lesson": c.get("lesson"), "book_pages": c.get("book_pages")},
            }
        frontier.extend(sp["succ"].get(nxt, []))
    return "prerequisite", {"node": node, "label": sp["labels"].get(node, node),
                            "motivates": None}


def _teaching_target(g, sp):
    """The node to actually teach: the most foundational UNMET node that (a) maps
    to a teachable Physics-2 concept and (b) is implicated in the student's
    failure (is itself failed, or lies on a path to a failed concept). This
    anchors teaching to nodes we have items+lessons for, instead of asserting an
    unfalsifiable gap at an untestable math-floor node. Falls back to the KST
    structural gap when nothing teachable is implicated.
    """
    struct = sp["structure"]
    mastered = g["map_state"]
    failed = frozenset(g["failed_nodes"])
    teachable = set(sp["node_to_slugs"])
    implicated = [n for n in teachable
                  if n not in mastered and (n in failed or struct.reaches(n, failed))]
    if implicated:
        return min(implicated, key=lambda n: (struct.depth[n], n))
    return g["primary_gap"]


def diagnose(responses, root=None):
    """responses: list of {"item_id":.., "correct":bool}. Returns the gap report."""
    sp = load_spine(str(_root(root)))
    pairs = [(r["item_id"], bool(r["correct"])) for r in responses]
    g = kst.locate_gap(sp["structure"], pairs, sp["items"], sp["calib"])

    structural = g["primary_gap"]               # KST-pure foundational fringe gap
    target = _teaching_target(g, sp)            # teachable, implicated node to teach
    result = {
        "gap_node": target,
        "gap_label": sp["labels"].get(target, target) if target else None,
        "confidence": round(g["confidence"], 4),
        "n_states": g["n_states"],
        "structural_gap": ({"node": structural, "label": sp["labels"].get(structural, structural)}
                           if structural else None),
        "failed_nodes": [{"node": n, "label": sp["labels"].get(n, n)} for n in g["failed_nodes"]],
        "fringe": [{"node": n, "label": sp["labels"].get(n, n)} for n in g["fringe"]],
        "responses_used": sum(1 for i, _ in pairs if sp["items"].get(i)),
        "responses_ignored": sum(1 for i, _ in pairs if not sp["items"].get(i)),
    }
    if target is None:
        result["status"] = "no_gap"
        result["message"] = "No gap located: the student's mastery spans the assessed spine."
        return result

    kind, payload = _teach_target(target, sp)
    result["status"] = "gap_located"
    result["teach_kind"] = kind  # "concept" (teach a lesson) | "prerequisite" (math floor)
    result["teach"] = payload
    if kind == "concept":
        primary = payload[0]
        result["slug"] = primary["slug"]
        result["lesson"] = primary["lesson"]
        result["book_pages"] = primary["book_pages"]
        result["concept_en"] = primary["concept_en"]
        if len(payload) > 1:
            result["note"] = ("teaching node maps to multiple collapsed concepts; "
                              f"candidates: {[p['slug'] for p in payload]}")
    else:
        result["note"] = ("gap is a prerequisite/math-floor node with no Physics-2 "
                           "lesson; teach the prerequisite, motivated by the concept it unlocks.")
    if structural and structural != target:
        result.setdefault("note", "")
        caveat = (f" KST structural gap is deeper ({sp['labels'].get(structural, structural)}); "
                  "intermediate nodes carry no items, so the teachable target is reported. "
                  "Low confidence reflects sparse item coverage.")
        result["note"] = (result["note"] + caveat).strip()
    return result


def next_item_for(responses, root=None):
    """Adaptive single-item selection (half-split). Returns an item_id or None."""
    sp = load_spine(str(_root(root)))
    pairs = [(r["item_id"], bool(r["correct"])) for r in responses]
    item_id = kst.next_item(sp["structure"], pairs, sp["items"], sp["calib"])
    if not item_id:
        return None
    m = sp["item_meta"].get(item_id, {})
    return {"item_id": item_id, "lesson": m.get("lesson"),
            "node": m.get("node"), "qkind": m.get("qkind"),
            "printed_number": m.get("printed_number")}


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    # smoke test: a student weak on momentum.
    sp = load_spine(str(_root()))
    mom_items = [i for i, n in sp["items"].items() if n == "Q2305665"][:6]
    grav_items = [i for i, n in sp["items"].items() if n == "Q134465"][:4]
    resp = [{"item_id": i, "correct": True} for i in grav_items] + \
           [{"item_id": i, "correct": False} for i in mom_items]
    print(json.dumps(diagnose(resp), ensure_ascii=False, indent=2))
