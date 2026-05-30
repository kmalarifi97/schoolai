# Diagnostic Spine — Phase 1–2 Report

**Status: Phases 1 (crosswalk) and 2 (prerequisite DAG) complete. Halted for
review, per run config (Phases 3–6 NOT started this session).**

Scope: Physics 2 only. Both repos read OK (teacher + knowledge-graph). All
structure pulled from the graph; nothing invented. DAG validated by the graph's
own `validator/dag.py`, run inside its `kg` Docker container.

## Numbers

| Metric | Value |
|---|---|
| Concepts crosswalked | 26 |
| → exact | 4 (gravitation, torque, momentumcons, cars) |
| → fuzzy | 7 (angular, workenergy, gravpe, elasticpe, rotke, pendulum, tempvsthermal) |
| → none | 15 |
| Distinct matched graph nodes | 9 |
| Prereq closure (matched + ancestors) | 20 nodes |
| Prereq edges from graph (`source=arbitrated`) | 20 |
| Proposed edges (`source=proposed`, llm, flagged) | 3 |
| **DAG validation** | **`DAG ok: 23 prerequisite edges, 19 nodes`, exit 0** |
| missing_nodes (concepts the graph must gain) | 15 |
| floor_gaps (math node missing) | 0 |
| Ungrounded matched roots | 2 (Temperature, Potential energy) |

## Alignment verdict

**11 of 26 concepts (42%) map to the graph; 15 do not.** This is the headline
finding the prompt asked to surface before any engine is built. The matched 11
form a coherent, acyclic spine grounded to the math floor
(Function→Limit→Derivative/Integral→…→Work→KE→Conservation; Vector→Force→Torque;
Mass/Velocity→Momentum→Conservation; Mass/Force→Universal gravitation) — enough
to prove the diagnostic loop on the gravitation→momentum→energy chain.

The 15 unmatched concepts are not a graph defect — the graph deliberately models
physics *primitives* and the math floor, not the textbook's experiment /
application / thermal-engineering concepts. They cluster:

- **Gravitation applications** (cavendish, gfield, weightless, equivalence) —
  downstream of Q134465.
- **Rotational/dynamics applications** (centerofmass, fictitious).
- **Momentum/energy quantities** (impulse, power, machines, efficiency,
  collisions) — each has a real *prerequisite* in the graph but is not identical
  to it.
- **Thermal physics** (heattransfer, specificheat, latentheat, thermolaws) —
  the graph has only Q11466 Temperature; the whole thermal vertical is absent.

## Decisions for review (do not let convenience redefine the asset)

1. **15 force-fit temptations rejected — confirm.** An independent audit pass
   proposed collapsing 9 of the `none` concepts onto *related* nodes
   (impulse→Momentum, power→Work, collisions→Conservation of momentum,
   latentheat→Temperature, thermolaws→Energy, …). All were rejected: those are
   prerequisites/siblings, not identities, and collapsing them would diagnose the
   wrong gap (e.g. a student missing *impulse* flagged as missing *momentum*; or
   *latent heat* — energy at **constant** temperature — mapped to Temperature).
   `missing_nodes.jsonl` records the nearest related node per concept so the edge
   is pre-identified when the node is created. **Review: confirm none of these 15
   should instead be a fuzzy identity match.**

2. **2 concept-pair collapses** (surfaced, not hidden): {gravpe, elasticpe} both
   → Q155640 Potential energy; {cars, rotke} both → Q46276 Kinetic energy. KST
   will treat each pair as one knowledge state until the graph gains
   gravitational-PE / elastic-PE / rotational-KE nodes. **Review: split now, or
   accept the collapse for the first engine pass?**

3. **rotke under-grounded:** rotational KE genuinely needs Moment of inertia
   (Q165618) + Angular velocity (Q161635), but maps to generic KE, so those
   prerequisites are not expressed. Tied to decision 2.

4. **3 proposed edges (flagged, conf 0.5):** Angular velocity (Q161635) arrived
   with **no** prerequisite edge in the graph. Proposed Time→, Derivative→,
   Euclidean-vector→Q161635, mirroring how linear velocity is wired. **Review:
   accept into the graph proper (arbitration), or keep spine-local?**

5. **2 ungrounded roots:** Temperature (Q11466) and Potential energy (Q155640)
   have no prerequisite edge. Temperature is additionally **edge-isolated** in
   this slice (it neither requires nor enables any matched node — hence the
   validator counts 19 edge-nodes, not 20). For Physics 2 these are arguably
   legitimate entry points, but KST cannot locate a gap *below* a root. **Review:
   acceptable as foundational, or do they need grounding?**

6. **Angular sub-concepts missing nodes:** the `angular` concept covers angular
   displacement / velocity / acceleration, but only angular velocity has a node.
   Not a math-floor gap; a candidate for `missing_nodes` if the graph expands.

7. **floor_gaps is empty — confirm interpretation.** Every math prerequisite the
   matched physics nodes need (derivative, integral, vector, cross product, trig)
   already has a node and is wired in. The "math floor" limitation the prompt
   anticipated does **not** bite this slice; the real gaps are missing *physics*
   nodes (above), not missing math nodes.

## Files

| File | Rows | Owner |
|---|---|---|
| `crosswalk.jsonl` | 26 | LLM-proposed (fuzzy rows flagged) |
| `missing_nodes.jsonl` | 15 | derived from `none` rows; nearest related node in note |
| `proposed_edges.seed.jsonl` | 3 | LLM-proposed, low-confidence, flagged |
| `prereq_edges.jsonl` | 23 | deterministic; **emitted only after DAG ok** |
| `prereq_edges.candidate.jsonl` | 23 | pre-validation intermediate |
| `floor_gaps.jsonl` | 0 | header-only; no math-node gaps |
| `build_spine.py` | — | deterministic assembler (re-runnable) |
| `EXPECTED_OUTPUT.md` | — | the contract, written before generation |

## Reproduce

```bash
# 1. assemble (deterministic) from the LLM seeds + the graph
python3 spine/build_spine.py
# 2. validate the DAG in the graph repo's Docker container (final authority)
SPINE=$(cd spine && pwd)
cd /Users/khalid-dev/knowledge-graph
docker compose run --rm -v "$SPINE":/spine kg python -m validator.dag /spine/prereq_edges.candidate.jsonl
# -> DAG ok: 23 prerequisite edges, 19 nodes   (then rename candidate -> prereq_edges.jsonl)
```

## What is NOT done (next session, after review)

Phases 3–6: item bank from `lesson_pages/*.json` → calibration (borrowed/default)
→ KST engine in Python (tested on the Function→Derivative→Velocity→Momentum→
Conservation chain) → `diagnose` endpoint + response logging + rewire
`gpt/instructions.md`. None started, per run config.
