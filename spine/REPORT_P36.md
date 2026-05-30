# Diagnostic Spine — Phases 3–6 Report

**Status: Phases 3–6 built and verified on the matched 11 concepts (Path A).**
The full loop runs: answers → KST diagnosis → located gap → teachable lesson.

Built on the validated Phase-1/2 spine. KST owns structure (graph) + calibration
(dataset/defaults) separately, exactly as required.

## What was built

| Phase | Output | Verified |
|---|---|---|
| 3 — item bank | `items.jsonl` (688), `items_unresolved.jsonl` (418) | 270 resolve to a single matched node |
| 4 — calibration | `calibration.jsonl` (688) | all `source:default` (no dataset wired) — flagged |
| 5 — KST engine | `kst.py`, `test_kst.py` | **5/5 unit tests pass** on the Function→Derivative→Velocity→Momentum→Conservation chain |
| 6 — endpoint | `diagnose.py`, `POST /gpt/diagnose`, `POST /gpt/next-item`, response logging, `action_schema.json`, `instructions.md` | **live route test via FastAPI TestClient: 200, gap→momentumcons/3-2** |

Engine facts: real spine = 19 nodes → **1,079 knowledge states** (exact Bayesian,
no approximation). BLIM slip/guess response model; half-split adaptive questioning;
gap = outer fringe of the MAP state.

## Verification (no Docker required)

```
python3 spine/test_kst.py        # 5/5 PASS
python3 spine/build_items.py     # 688 items, 270 resolved
python3 spine/diagnose.py        # smoke: momentum-weak -> momentumcons (3-2)
```
Live route, through the real FastAPI app (TestClient):
`POST /gpt/diagnose {grav correct, momentum wrong}` → `200`, `gap_node Q2305665`,
`slug momentumcons`, `lesson 3-2`, `book_pages 74-95`, `logged 10`, plus
`structural_gap = Function` with a sparse-coverage caveat. `/gpt/next-item` → 200.
Existing `/api/*` and `/gpt/concepts|search` routes unaffected.

## Honest findings & limitations (surfaced, not hidden)

1. **Items link by lesson, not concept_tags.** The questions do **not** carry
   usable `concept_tags` (6/688) or `difficulty` (0/688) — contrary to the build
   prompt's assumption. Linking is therefore lesson-level:
   - 270 items → single matched node (`lesson-exact` 125 + `lesson-single-matched` 145)
   - 41 items `lesson-ambiguous` (≥2 matched concepts in the lesson → node=null, candidates listed)
   - 377 items `unresolved` (lesson has no matched concept → node=null)
   Item coverage exists for 6 of 9 matched nodes; Work/KE/PE fall in ambiguous
   lessons (4-1, 5-1) and currently carry no clean items. All flagged in
   `items_unresolved.jsonl`, none dropped.
2. **Difficulty is a qkind proxy, not measured** (no difficulty in source).
3. **Calibration is 100% default** — no open dataset (ASSISTments/Eedi) was
   provided at runtime, so slip=0.10 / guess-by-qkind for every item, `source:
   default`. Per-item replaceable when real data arrives (the response log is the
   seed).
4. **Sparse items can't localize deep gaps.** Intermediate/math-floor nodes have
   no book items, so a student failing momentum yields a diffuse posterior. The
   engine reports the KST `structural_gap` (e.g. Function, low confidence) but the
   `gap_node`/teach target is the most-foundational *teachable, implicated*
   concept (momentumcons). This is a documented coverage limit, not a bug.
5. **Response logging needs a writable mount.** The repo is mounted read-only at
   `/srv/lib`; logging writes to `SPINE_RESPONSES` (a writable named volume
   `spine_responses` added to `web/docker-compose.yml`), degrading to
   `logged:false` rather than erroring.

## Deploy note (Docker)

`web/backend/gpt_api.py` is **baked into the backend image** (not bind-mounted),
so the new routes require a backend image **rebuild** to go live:
`cd web && docker compose up -d --build backend`. The diagnostic spine itself
(`spine/**`) is read live from the mounted repo. A rebuild needs network for
`pip install`; it was not possible in this sandbox, so Phase 6 was validated via
FastAPI TestClient instead of a live container. The `/gpt` Action schema is
regenerated (`gpt/export_action_schema.py`) and includes the two new paths.

## Files added/changed

Added: `spine/{kst.py, test_kst.py, diagnose.py, build_items.py, items.jsonl,
items_unresolved.jsonl, calibration.jsonl, EXPECTED_OUTPUT_P36.md, REPORT_P36.md}`.
Changed: `web/backend/gpt_api.py` (+diagnose/next-item routes, logging),
`web/docker-compose.yml` (+writable responses volume), `gpt/action_schema.json`
(+2 paths), `gpt/instructions.md` (diagnosis-first lesson selection).

## Next (not done)

- Wire a real calibration dataset (replace defaults per item).
- Grow item coverage for Work/KE/PE (resolve the ambiguous lessons) — or split
  the collapsed concept nodes (Phase 2 decision 2).
- Accumulate `responses.jsonl` → re-estimate slip/guess from real students.
