# graph-log — empty experience log + on-demand LLM decomposition

The new model. The graph database **starts empty** and only **logs student
experience**; it is not a pre-authored map and there is **no traversal engine**.
All analysis and personalization is the **LLM's** job. When a student asks about
a topic, the LLM decomposes it into its prerequisite graph on demand (layer by
layer, descending from the topic into the underlying math, stopping at
equation/variable literacy). The topic graph is the same for everyone; only the
pass/struggle log is per student.

```
student asks a topic
  → LLM decomposes it  (decompose.mjs: DECOMPOSITION_PROMPT, Kepler example baked in)
  → store the decomposition           (db.storeDecomposition)
  → log the student's pass/struggle    (db.logOutcome)  ← the only thing that grows
  → read the student's status          (db.topicStatusForStudent)  → LLM personalizes
```

## Run the demo

```bash
node demo.mjs        # or: npm run demo
```

Shows: empty DB → decompose "Kepler's third law" → store the layered graph → log
one student's passes/struggles → read back their gaps (division, ratio,
proportionality) → DB filled from empty.

## Pieces

- `db.mjs` — the log store (Node built-in SQLite, zero install). Tables: `topics`,
  `nodes`, `edges`, `logs`. Starts empty; fills as students learn.
- `decompose.mjs` — the LLM decomposition: `DECOMPOSITION_PROMPT` (with the Kepler
  worked example baked in so the LLM imitates the depth and stopping point), the
  `KEPLER` example as data, and `decompose(topic, { llm })` — pass a real LLM in
  production; offline it returns the baked example.
- `demo.mjs` — the end-to-end run.

## Wiring a real LLM

`decompose(topic, { llm })` takes `llm: async (prompt, topic) => jsonString`.
Point it at Claude/OpenAI (send `DECOMPOSITION_PROMPT` + the topic, parse the
returned JSON). Nothing else changes — storage and logging are LLM-agnostic.

## Storage choice

Node's built-in `node:sqlite` — a real embedded DB file with zero dependencies.
The data file (`data/`) is gitignored; the DB is created empty on first run.
