# Item Bank — Concept Re-Tagging Report

**Status: item bank re-tagged per-QUESTION by concept. Validation PASS.**
(Earlier phase reports: `REPORT_phase1-2.md`, `REPORT_P36.md`.)

The old `items.jsonl` linked each question to its *lesson*, so 418/688 had
`node:null` and were useless to KST. This pass re-tags each question by the
concept it actually **tests**, read from `prompt_ar`. Discipline kept: 19 LLM
agents proposed tags (one per batch, reading every question); deterministic code
(`build_items_concept.py`) verified every tag against a fixed node set, force-fit
nothing, and emitted the bank. **688/688 tagged, 0 validation errors.**

## Valid node set (the only allowed tags)

The 7 matched-concept QIDs **plus** the 4 collapse-split nodes (spine-local until
the prereq DAG gains them): `SPINE:translational_ke`, `SPINE:rotational_ke`,
`SPINE:gravitational_pe`, `SPINE:elastic_pe`. Defined in `tag_nodeset.json`.

## THE NUMBER THAT MATTERS — per-node item count (primary tag)

| node | concept | items | flag |
|---|---|---:|---|
| Q42213 | Work & work-energy theorem | **67** | |
| Q134465 | Newton's gravitation / Kepler | **59** | |
| Q2305665 | Conservation of momentum | **56** | |
| Q48103 | Torque & lever arm | **47** | |
| Q11382 | Conservation of mechanical energy | **46** | |
| Q161635 | Angular motion / velocity | **31** | |
| SPINE:gravitational_pe | Gravitational PE (mgh) | **22** | |
| SPINE:translational_ke | Translational KE (½mv²) | **16** | |
| Q11466 | Temperature vs thermal energy | **13** | |
| SPINE:elastic_pe | Elastic PE (½kx²) | **6** | |
| SPINE:rotational_ke | Rotational KE (½Iω²) | **0** | ⚠ **<3 items** |

**Concepts KST cannot yet reliably diagnose (< 3 items): 1 — `rotational_ke` (0).**
The book has no question that *primarily* tests rotational KE (its items get
framed via moment of inertia / angular motion). Needs generated items, or accept
it as non-diagnosable until the book yields more.

## items_needing_node — demand for the 15 missing nodes

**271 questions** test a real concept that has **no node**. They were routed to
`items_needing_node.jsonl` (not force-fit). Demand ranking — this says which
missing nodes are worth adding first:

| missing concept | questions demanding it |
|---|---:|
| impulse | 51 |
| power | 36 |
| specific_heat | 34 |
| thermo_laws | 24 |
| machines | 23 |
| latent_heat | 23 |
| collisions | 21 |
| efficiency | 14 |
| center_of_mass | 12 |
| gravitational_field | 11 |
| heat_transfer | 8 |
| primitive (force/velocity only) | 5 |
| fictitious_force | 4 |
| cavendish | 3 |
| weightlessness | 2 |

**impulse (51), power (36), specific_heat (34)** are the highest-value nodes to
add next — adding impulse alone would make 51 currently-unusable questions
diagnosable.

## Before → after

| | old (lesson-level) | new (per-question) |
|---|---|---|
| questions with a usable node | 270 | **363** |
| nodes that have items | 6 | **10** of 11 |
| ambiguous/unresolved nulls | 418 | **0** (271 → demand signal, 54 → non-assessing) |
| `items_unresolved.jsonl` | mixed (force-fail) | **only 54 genuinely non-assessing** |

## Output files

- `items.jsonl` — **417 rows**: 363 concept items (node set) + 54 non-assessing
  (node=null). The ONLY null nodes are `resolution:non_assessing`. Each concept
  row carries `node`, optional `secondary`, `qkind`, `lesson`, `page`.
- `items_needing_node.jsonl` — **271 rows**, each with the `needs_concept` key.
- `items_unresolved.jsonl` — **54 rows**, non-assessing only (instructions,
  open reflection, lab steps).
- `tag_nodeset.json` — the valid node set + missing-concept keys.
- `_tag_out/batch_*.jsonl` — the raw per-agent proposals (audit trail).

## Validation (deterministic)

```
coverage: 688/688 tagged; errors: 0
items.jsonl: 417 rows (concept 363, non_assessing 54)
bad nodes in items.jsonl: 0   illegal nulls: 0
RESULT: PASS
```
Every `items.jsonl` node is in the valid set; the only null nodes are
non-assessing; every one of the 688 questions is tagged exactly once.
`python3 spine/test_kst.py` → 5/5 PASS; `diagnose` loads the new bank without
error (momentum-weak → momentumcons / lesson 3-2).

## Scope honored / carried forward

- **Not modified:** the KST engine (`kst.py`), the diagnose endpoint, the graph.
  This was tagging only. `build_items.py` (the old lesson-level assembler) is
  superseded by `build_items_concept.py` — do not re-run the former or it will
  overwrite `items.jsonl` with the lesson-level version.
- **Carried forward:** the 4 `SPINE:*` split nodes are tagged but are **not yet
  in `prereq_edges.jsonl`**, so their items load but aren't diagnosable until a
  Phase-2 expansion adds those nodes + edges (separate task — would also let
  `gravitational_pe`/`elastic_pe`/`translational_ke` items drive diagnosis). The
  7 real-QID nodes are fully diagnosable now.
- Calibration (`calibration.jsonl`) is keyed by `item_id` and unchanged; still
  covers all questions.
