# Diagnostic Spine — Expected Output (Phases 1–2 only)

Written **before** generation, per the build prompt. This is the contract the
generated files must satisfy, and the document the human reviews before any
engine (Phases 3–6) is built on top of the mapping.

Scope: **Physics 2 only**. Phases run this session: **1 (crosswalk) and 2
(prerequisite DAG) ONLY.** Halt after Phase 2 for review.

Two repos, two identities, one bridge:
- Teacher: `scripts/concepts/INDEX.json` → 26 concept `slug`s.
- Graph: `/Users/khalid-dev/knowledge-graph/registry/nodes.jsonl` → 54
  Wikidata-anchored `QID` nodes; `arbitration/arbitrated.jsonl` → 56
  prerequisite edges (+5 is-a).

Hard rules honored: graph = structure (never invented), dataset = calibration
(not in scope this session). LLM proposes the crosswalk + low-confidence edges;
**deterministic code** assembles the induced subgraph and the DAG validator
(the graph repo's own `validator/dag.py`, run in its Docker container) is the
final authority. Nothing is force-fit; every gap is surfaced to an explicit
file.

---

## Files this session will produce (all under `spine/`)

| File | Owner | Contract |
|---|---|---|
| `crosswalk.jsonl` | LLM-proposed | 26 rows, one per concept. `{slug,node,label,match,note}`. `match ∈ {exact,fuzzy,none}`. |
| `missing_nodes.jsonl` | derived | one row per `match:"none"` concept — concepts the graph must gain. |
| `proposed_edges.seed.jsonl` | LLM-proposed | low-confidence prerequisite edges among matched nodes, flagged for review. |
| `prereq_edges.jsonl` | deterministic | induced upstream-closure subgraph from `arbitrated.jsonl` + merged proposals. **Emitted only after `validator/dag.py` returns acyclic.** |
| `floor_gaps.jsonl` | surfaced | physics nodes whose math prerequisite has no graph node. |
| `build_spine.py` | deterministic | reproducible assembler: crosswalk + graph → prereq_edges + missing_nodes + floor_gaps. LLM owns only the seed `crosswalk.jsonl` / `proposed_edges.seed.jsonl`. |
| `REPORT.md` | summary | counts, the alignment verdict, what review must decide. |

---

## Phase 1 — Expected crosswalk (the proposal under review)

Tally: **4 exact · 7 fuzzy · 15 none**. The high `none` count is the headline
finding — it is exactly the "many come back none" signal the prompt says must be
seen before building an engine. Cause: the graph models the *physics primitives*
(force, energy, momentum, torque, velocity) and the *math floor*, but not the
Physics-2 textbook's experiment/application/thermal concepts.

| # | slug | match | node | node label | note |
|---|---|---|---|---|---|
| 1 | gravitation | exact | Q134465 | Newton's law of universal gravitation | Kepler's-laws framing has no node; anchors to the law |
| 2 | cavendish | none | — | — | experiment to measure G; no node |
| 3 | gfield | none | — | — | gravitational field strength g; distinct from the force law |
| 4 | weightless | none | — | — | weightlessness/free-fall; no node |
| 5 | equivalence | none | — | — | equivalence principle; no node |
| 6 | angular | fuzzy | Q161635 | Angular velocity | concept covers angular displ/vel/accel; only ang. velocity has a node |
| 7 | torque | exact | Q48103 | Torque | — |
| 8 | centerofmass | none | — | — | centre of mass & stability; no node |
| 9 | fictitious | none | — | — | centrifugal/Coriolis; no node |
| 10 | impulse | none | — | — | impulse J=∫F dt; distinct from momentum; no node |
| 11 | momentumcons | exact | Q2305665 | Conservation of momentum | — |
| 12 | workenergy | fuzzy | Q42213 | Work (physics) | theorem links work↔ΔKE; anchors to Work |
| 13 | cars | exact | Q46276 | Kinetic energy | — |
| 14 | power | none | — | — | P=dW/dt; no node |
| 15 | machines | none | — | — | simple machines / mechanical advantage; no node |
| 16 | efficiency | none | — | — | machine efficiency; no node |
| 17 | gravpe | fuzzy | Q155640 | Potential energy | gravitational PE — a kind of PE; collapses onto generic PE |
| 18 | elasticpe | fuzzy | Q155640 | Potential energy | elastic PE — also collapses onto generic PE (see collapse note) |
| 19 | rotke | fuzzy | Q46276 | Kinetic energy | rotational KE=½Iω²; collapses onto generic KE |
| 20 | pendulum | fuzzy | Q11382 | Conservation of energy | "conservation of mechanical energy"; anchors to cons. of energy |
| 21 | collisions | none | — | — | elastic/inelastic collisions; no node |
| 22 | tempvsthermal | fuzzy | Q11466 | Temperature | contrasts temperature vs thermal energy; thermal-energy node absent |
| 23 | heattransfer | none | — | — | conduction/convection/radiation; no node |
| 24 | specificheat | none | — | — | specific heat capacity; no node |
| 25 | latentheat | none | — | — | latent heat; no node |
| 26 | thermolaws | none | — | — | laws of thermodynamics & entropy; no node |

**Collapse warning (surfaced, not hidden):** two pairs of distinct concepts map
to one node each — {gravpe, elasticpe}→Q155640, {cars, rotke}→Q46276. KST will
treat each pair as a single knowledge state until the graph gains
gravitational-PE / elastic-PE / rotational-KE nodes. Recorded in `REPORT.md`.

Every `fuzzy` row is flagged for human review.

## Phase 1 — Expected `missing_nodes.jsonl` (15 rows)

cavendish, gfield, weightless, equivalence, centerofmass, fictitious, impulse,
power, machines, efficiency, collisions, heattransfer, specificheat, latentheat,
thermolaws — each with the slug, the concept label, and a one-line note on what
node the graph should gain. **No node is invented** to absorb these.

---

## Phase 2 — Expected prerequisite DAG

Node set = the **9 distinct matched nodes** plus their **transitive prerequisite
ancestors** in the graph (the chain down to the math floor that KST needs to
locate where knowledge breaks):

Matched: Q134465, Q161635, Q48103, Q2305665, Q42213, Q46276, Q155640, Q11382, Q11466.
Closure adds: Q11348 (Function), Q246639 (Limit), Q29175 (Derivative),
Q80091 (Integral), Q44528 (Euclidean vector), Q178192 (Cross product),
Q11471 (Time), Q11423 (Mass), Q11465 (Velocity), Q11402 (Force), Q41273 (Momentum).
→ **20 nodes total.**

**Existing edges pulled from `arbitrated.jsonl` (≈20 prerequisite edges):** the
induced subgraph on those 20 nodes — e.g. Function→Limit→Derivative→Velocity,
Vector→Force, Force/Integral→Work→KE→ConsE, PE→ConsE, Mass/Velocity→Momentum→
ConsMom, Cross/Force→Torque, Mass/Force→UnivGravitation.

**LLM-proposed low-confidence edges (`proposed_edges.seed.jsonl`, flagged):**
Angular velocity (Q161635) arrives with **no** prerequisite edge in the graph —
it floats. Mirror velocity's grounding: `Time→Q161635`, `Derivative→Q161635`,
`Euclidean vector→Q161635` (conf 0.5, provenance `llm-proposed`). Temperature
(Q11466) is left an isolated root (foundational in the thermo unit; no forced
physics prerequisite).

**`floor_gaps.jsonl`: expected empty.** Every math prerequisite the matched
physics nodes need (derivative, integral, vector, cross product, trig) already
has a node and is wired in. The genuine structural gaps are the 15 missing
*physics* nodes (in `missing_nodes.jsonl`) and the missing angular-displacement /
angular-acceleration nodes (noted in `REPORT.md`), not the math floor.

**Validation gate:** the combined edge set (~23 prerequisite edges) is written to
a temp file, the graph repo's `validator/dag.py` is run on it **inside the `kg`
Docker container**, and `prereq_edges.jsonl` is emitted only if it reports
`DAG ok`. Adding the angular edges introduces no cycle (Q161635 has no outgoing
edge in this set), so `DAG ok: 23 prerequisite edges, 20 nodes` is expected.

---

## Alignment verdict (what review must decide)

11/26 concepts map to the graph (4 exact + 7 fuzzy); 15 do not. The matched 11
form a coherent, acyclic spine grounded all the way to the math floor — enough to
prove the diagnostic loop on the gravitation→momentum→energy chain. But **before
Phases 3–6**, review must decide whether to (a) grow the graph with the 15
missing nodes + the 2 collapse-splits + angular-displacement/acceleration, or
(b) prove the engine on the matched spine first and backfill. This document
exists so that decision is made on seen data, not discovered mid-engine.
