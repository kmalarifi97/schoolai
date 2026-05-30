#!/usr/bin/env python3
"""Assemble the CONCEPT-tagged item bank from the agent tag outputs (verify step).

LLM agents proposed per-question tags in spine/_tag_out/batch_*.jsonl. This script
is the deterministic verifier/assembler: it validates every tag against the fixed
valid node set, force-fits nothing, and emits:

  * items.jsonl            -- concept items (node in valid set) + non-assessing
                              (node=null). The KST-usable bank. The ONLY null
                              nodes are non-assessing questions.
  * items_needing_node.jsonl -- questions that test a real concept with NO node
                              (the 15 missing). Demand signal for new nodes.
  * items_unresolved.jsonl -- ONLY non-assessing questions (instructions, open
                              reflection) -- not "failed to tag".

Validation: every items.jsonl node is in the valid set; coverage == all 688
questions tagged exactly once; no node outside the valid set anywhere.
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path

SPINE = Path(__file__).resolve().parent
REPO = SPINE.parent
LP = REPO / "chatgpt-app" / "data" / "lesson_pages"

def read_jsonl(p):
    for line in Path(p).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield json.loads(line)

def walkq(o, acc):
    if isinstance(o, dict):
        if o.get("type") == "question" or "qkind" in o: acc.append(o)
        for v in o.values(): walkq(v, acc)
    elif isinstance(o, list):
        for v in o: walkq(v, acc)

def main():
    ns = json.loads((SPINE / "tag_nodeset.json").read_text())
    valid = {n["node"] for n in ns["valid_nodes"]}
    slug2node = {n["slug"]: n["node"] for n in ns["valid_nodes"]}
    missing_keys = {m["key"] for m in ns["missing_concepts"]}

    # original questions -> metadata + the authoritative id set
    meta = {}
    for f in sorted(LP.glob("[0-9]*.json")):
        d = json.loads(f.read_text()); qs = []; walkq(d["pages"], qs)
        for q in qs:
            meta[q["id"]] = {"lesson": d["lesson_id"], "qkind": q.get("qkind", ""),
                             "printed_number": q.get("printed_number", ""), "page": q.get("page")}
    all_ids = set(meta)

    # collect tags
    tags = {}; errors = []; dupes = []
    for bf in sorted((SPINE / "_tag_out").glob("batch_*.jsonl")):
        for rec in read_jsonl(bf):
            qid = rec.get("id")
            if qid not in all_ids:
                errors.append(f"{bf.name}: unknown id {qid}"); continue
            if qid in tags:
                dupes.append(qid); continue
            node = rec.get("node")
            if node in ("null", "", "None"): node = None
            # tolerate slug-as-node
            if node and node not in valid and node in slug2node:
                node = slug2node[node]
            sec = rec.get("secondary")
            if sec in ("null", "", "None"): sec = None
            if sec and sec not in valid and sec in slug2node: sec = slug2node[sec]
            needs = rec.get("needs_concept") or None
            non = bool(rec.get("non_assessing"))
            # validate
            if node is not None and node not in valid:
                errors.append(f"{qid}: node {node!r} not in valid set"); node = None
            if sec is not None and sec not in valid:
                sec = None
            tags[qid] = {"node": node, "secondary": sec, "needs_concept": needs,
                         "non_assessing": non, "reason": rec.get("reason", "")}

    missing_ids = all_ids - set(tags)
    if missing_ids: errors.append(f"{len(missing_ids)} questions never tagged: {sorted(missing_ids)[:8]}...")
    if dupes: errors.append(f"{len(dupes)} duplicate tags: {sorted(set(dupes))[:8]}...")

    # assemble
    items, needing, unresolved = [], [], []
    cov = Counter(); need_cov = Counter()
    for qid in sorted(all_ids):
        m = meta[qid]; t = tags.get(qid, {"node": None, "non_assessing": True,
                                          "needs_concept": None, "secondary": None, "reason": "UNTAGGED"})
        base = {"item_id": qid, "lesson": m["lesson"], "qkind": m["qkind"],
                "printed_number": m["printed_number"], "page": m["page"]}
        if t["node"]:
            items.append({**base, "node": t["node"], "secondary": t["secondary"],
                          "resolution": "concept", "flag": False})
            cov[t["node"]] += 1
            if t["secondary"]: cov[t["secondary"]] += 0  # secondary not counted as primary
        elif t["needs_concept"]:
            key = t["needs_concept"]
            needing.append({"item_id": qid, "lesson": m["lesson"], "qkind": m["qkind"],
                            "needs_concept": key, "reason": t.get("reason", "")})
            need_cov[key] += 1
        else:  # non-assessing
            items.append({**base, "node": None, "secondary": None,
                          "resolution": "non_assessing", "flag": True})
            unresolved.append({"item_id": qid, "lesson": m["lesson"], "qkind": m["qkind"],
                               "reason": t.get("reason", "non-assessing")})

    def write(p, rows, header):
        with open(p, "w") as f:
            for ln in header.strip("\n").split("\n"): f.write(f"# {ln}\n")
            for r in rows: f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")

    write(SPINE / "items.jsonl", items,
          "CONCEPT-tagged KST item bank. node = the concept each question TESTS "
          "(per-question, not per-lesson). The ONLY null-node rows are "
          "resolution=non_assessing. Force-fit nothing; SPINE:* nodes are "
          "collapse-splits pending a prereq-DAG entry.")
    write(SPINE / "items_needing_node.jsonl", needing,
          "Questions testing a concept with NO node (the 15 missing). Demand "
          "signal: which missing nodes are worth adding. Not force-fit.")
    write(SPINE / "items_unresolved.jsonl", unresolved,
          "ONLY non-assessing questions (pure instructions, open reflection, lab "
          "steps) -- NOT questions we failed to tag.")

    # ---- validation ----
    bad = [it for it in items if it["node"] is not None and it["node"] not in valid]
    null_nonassess = [it for it in items if it["node"] is None and it["resolution"] != "non_assessing"]
    print("=== VALIDATION ===")
    print(f"coverage: {len(tags)}/{len(all_ids)} tagged; errors: {len(errors)}")
    for e in errors[:10]: print("  !", e)
    print(f"items.jsonl rows: {len(items)} (concept {sum(1 for i in items if i['node'])}, "
          f"non_assessing {sum(1 for i in items if not i['node'])})")
    print(f"bad nodes in items.jsonl: {len(bad)}   illegal nulls: {len(null_nonassess)}")
    print(f"items_needing_node: {len(needing)}   items_unresolved(non-assessing): {len(unresolved)}")
    ok = not errors and not bad and not null_nonassess and not missing_ids
    print("RESULT:", "PASS" if ok else "FAIL")

    # ---- the number that matters: per-node counts ----
    print("\n=== PER-NODE ITEM COUNT (primary) ===")
    label = {n["node"]: n["en"] for n in ns["valid_nodes"]}
    low = []
    for n in ns["valid_nodes"]:
        c = cov.get(n["node"], 0)
        flag = "  <-- FEWER THAN 3" if c < 3 else ""
        if c < 3: low.append(n["node"])
        print(f"  {n['node']:22s} {label[n['node']][:34]:34s} {c}{flag}")
    print(f"\nconcepts with <3 items (KST cannot reliably diagnose): {len(low)} -> {low}")
    print("\n=== items_needing_node demand (missing concepts) ===")
    for k, c in need_cov.most_common():
        print(f"  {k:22s} {c}")
    print(f"total questions demanding a missing node: {sum(need_cov.values())}")
    return ok

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
