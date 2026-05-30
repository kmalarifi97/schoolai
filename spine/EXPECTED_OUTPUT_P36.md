# Diagnostic Spine — Expected Output (Phases 3–6)

Written **before** generation. Path chosen: **A — prove the loop on the matched
11 concepts** (9 distinct nodes). Built on the validated Phase-1/2 spine.

## Data reality (discovered, surfaced — differs from the build prompt)

The prompt assumed each question carries `concept_tags` + `difficulty`. Survey of
all **688 questions** across 13 lessons found:

| field | coverage | consequence |
|---|---|---|
| `id`, `printed_number`, `qkind` | 688/688 | usable |
| `concept_tags` | **6/688** (Arabic free-text, not slugs) | **cannot** link items by tag |
| `difficulty` | **0/688** | no real difficulty; derive a qkind proxy, flagged |

`qkind ∈ {conceptual 292, numerical 343, mcq 37, graph 16}` — no `true_false`.

**Item→concept link falls back to lesson-level** (INDEX.json maps concept→lesson).
Resolution quality is graded and surfaced, never force-fit:

| resolution | meaning | lessons | items |
|---|---|---|---|
| `lesson-exact` | lesson has exactly 1 concept, and it's matched | 2-1, 2-2, 3-2 | 125 |
| `lesson-single-matched` | lesson has 1 matched concept + other (unmatched) concepts | 1-1, 5-2, 6-1 | 145 |
| `lesson-ambiguous` | lesson has ≥2 matched concept-nodes → cannot uniquely resolve | 4-1, 5-1 | 41 |
| `unresolved` | lesson has 0 matched concepts | 1-2, 2-3, 3-1, 4-2, 6-2 | 377 |

Expected: **~270 items resolve to a single matched node** (exact + single),
**41 ambiguous** (node=null, candidate_nodes listed), **377 unresolved**
(node=null). Ambiguous + unresolved are flagged, not dropped.

## Files (Phases 3–4, under `spine/`)

| File | Contract |
|---|---|
| `items.jsonl` | 688 rows: `{item_id, lesson, qkind, printed_number, page, node, resolution, candidate_nodes, flag}`. node=null when unresolved/ambiguous. |
| `items_unresolved.jsonl` | the flagged subset (resolution ∈ {ambiguous, unresolved}) for review. |
| `calibration.jsonl` | 688 rows: `{item_id, slip, guess, source}`. No dataset provided at runtime → **all `source:"default"`**, slip 0.10, guess by qkind (mcq 0.25, else 0.05; true_false 0.50 if seen). Flagged: borrowed=0. |
| `build_items.py` | deterministic assembler (items + calibration from lessons + crosswalk + INDEX). |

## Phase 5 — KST engine (`spine/kst.py`, pure stdlib)

- `knowledge_states(edges)` — the knowledge structure: all downward-closed sets
  (order ideals) of the prerequisite DAG. Closed under ∪/∩ (quasi-ordinal space,
  Birkhoff). Implements Doignon & Falmagne ch. 10 structure.
- BLIM response model (`p_correct`): item on node n → `1−slip` if n∈state else
  `guess`. (Basic Local Independence Model.)
- `posterior(responses)` — Bayesian update of a uniform prior over states given
  observed (item, correct) pairs.
- `next_item(responses)` — half-split questioning rule: pick the unasked item
  whose P(correct) under the current belief is closest to 0.5 (most informative).
- `locate_gap(responses)` — from the MAP state, return the **outer fringe** (nodes
  whose prerequisites are all known but which are not), primary gap = the most
  foundational (lowest topological depth).
- **Unit test (`spine/test_kst.py`)** on the 5-node chain
  Function→Derivative→Velocity→Momentum→Conservation: a simulated student who
  knows Function+Derivative but not Velocity must be located with gap=Velocity.
  Run before any backend wiring. Expected: PASS.

State-count guard: the engine prints the structure size; if ideals explode it
restricts to the sub-structure spanned by the answered items' nodes + ancestors.

## Phase 6 — diagnose endpoint + loop closure

- `spine/diagnose.py`: `diagnose(responses, root)` → loads spine, runs kst, maps
  the gap node back through the crosswalk to a teachable concept and returns
  `{gap_node, gap_label, slug, lesson, book_pages, concept_en, confidence,
  fringe, note}`. If the gap is a math-floor node (no Physics-2 lesson), it is
  reported as a prerequisite gap with the nearest downstream concept named.
- Backend `POST /gpt/diagnose` (added to `gpt_api.py` so it exports into the
  Action schema): body `{student_id, responses:[{item_id, correct}]}` → logs each
  response, returns the diagnosis. Read-only repo mount means logging writes to an
  env-configurable path (`SPINE_RESPONSES`, default a writable volume) with
  graceful degradation (`logged:false` rather than 500).
- `spine/responses.jsonl` (or the volume): `{student_id, item_id, correct, ts}` —
  the seed of real calibration data.
- `gpt/action_schema.json` regenerated via `export_action_schema.py` (adds the
  diagnose path).
- `gpt/instructions.md` rewired: on session start / topic request, call
  `diagnose` first, then teach the returned gap's lesson from the book — the
  book-grounded teaching behavior itself is unchanged; only *what* it teaches is
  now diagnosis-chosen.

## Verification

- `python3 spine/test_kst.py` → PASS on the 5-node chain.
- `python3 spine/build_items.py` → 688 items, ~270 resolved, calibration 688.
- `python3 -c "diagnose(simulated)"` smoke test returns a momentum/energy gap.
- Backend route reachable via the running Docker stack (`web-backend`), schema
  re-exported. DAG/Phase-1-2 outputs untouched.

## Honest limitations carried forward (in REPORT)

1. Items link by lesson, not concept — 41 ambiguous, 377 unresolved.
2. Difficulty is a qkind proxy, not measured.
3. Calibration is 100% default (no open dataset wired) — slip/guess uninformed.
4. Response logging needs a writable mount in production.
These are exactly the per-item-replaceable seams Phase 4/6 anticipated; none is
hidden.
