# graph-tutor — direct prerequisite-graph tutor (GraphQL + MCP)

A proof-of-concept that **replaces the KST engine with direct graph traversal.**
The prerequisite graph is explicit, so diagnosing a student is just: walk the
edges backward from each failed skill to the prerequisites they haven't mastered.

```
Junyi dataset ──build──> prerequisite graph (JSON)
                              │
                       GraphQL server  (the "graph DB" API)  ── src/graphqlServer.mjs
                              │  diagnose(passed, failed) query = backward traversal
                       MCP server (wired DIRECTLY to GraphQL) ── src/mcpServer.mjs
                              │
                          ChatGPT / LLM
```

No state-space search, no bitmasks, no 31-node ceiling. The old KST app under
`../chatgpt-app/` is left fully intact — this is a separate, parallel stack.

## Layout

```
graph-tutor/
├── graph/
│   ├── seed.graph.json          small hand-built DAG so the stack runs now
│   └── build_junyi_graph.mjs    empirical graph builder (run when Junyi CSVs are on disk)
├── src/
│   ├── graphStore.mjs           loads a graph + traversal/diagnosis (pluggable: swap for Neo4j)
│   ├── schema.mjs               GraphQL schema + resolvers (the diagnose query)
│   ├── graphqlServer.mjs        HTTP GraphQL endpoint  (POST /graphql)
│   ├── mcpServer.mjs            MCP server -> calls the GraphQL endpoint  (POST /mcp)
│   ├── smoke.mjs                schema/diagnosis unit checks (no network)
│   └── clientTest.mjs           real MCP client e2e (MCP -> GraphQL -> graph)
└── package.json
```

## Edge semantics

An edge `{source, target}` means **`source` is a prerequisite of `target`**
(master `source` before `target`). "Prerequisites of X" = sources of edges whose
target is X (walk edges in reverse). This matches the empirical rule
`A → B when P(A|B) > 0.9 AND P(B|A) < 0.5` (A is the prerequisite).

## Run

```bash
npm install
npm run smoke                 # offline logic check
npm run graphql               # GraphQL on :4000  (POST /graphql)
npm run mcp                   # MCP on :4100 (POST /mcp) -> GraphQL on :4000
node src/clientTest.mjs       # end-to-end via a real MCP client
```

Point the GraphQL server at a different graph with `GRAPH_PATH=...`.
Point the MCP server at a different GraphQL with `GRAPHQL_URL=...`.

## Diagnosis logic (the design decision that matters)

Root cause prefers **confirmed** gaps over **unknown** ones: among a failed
skill's prerequisites we never assert a gap on a skill we didn't test. We pick
the **deepest skill the student actually failed** (most foundational confirmed
weakness) to teach first. If only *untested* prerequisites remain, we don't
guess — we tell the teacher to **quiz the nearest unknown(s)** to locate the gap.

## Building the real graph from Junyi

Dataset (non-commercial / research-only):
https://www.kaggle.com/datasets/junyiacademy/learning-activity-public-dataset-by-junyi-academy
Preprocessing reference: https://github.com/bigdata-ustc/EduData

```bash
LOG_CSV=Log_Problem.csv EXERCISE_CSV=Info_Content.csv \
  COL_STUDENT=uuid COL_EXERCISE=ucid COL_OUTCOME=is_correct \
  EX_COL_ID=ucid EX_COL_SKILL=topic EX_COL_AREA=area \
  node graph/build_junyi_graph.mjs
# writes graph/junyi.graph.json (+ .vs_expert.json comparison)

GRAPH_PATH=graph/junyi.graph.json npm run graphql   # serve the real graph
```

The builder: aggregates exercises to skills, marks mastery at ≥80%, computes
pairwise conditional mastery **only over students who attempted both skills**,
draws edges on the asymmetry, flags cycles, and emits a comparison against
Junyi's own expert area map. Confirm the column names it prints before trusting
the output (Junyi exports vary).

## Scale note

`graphStore` holds the graph in memory and traverses in JS — fine for a PoC and
for graphs far larger than KST's 31-node limit. For a production graph DB with
native traversal, reimplement `graphStore.mjs` against **Neo4j** (a backward
prerequisite walk is one Cypher `MATCH (p)-[:PREREQUISITE*]->(failed)` query);
the GraphQL layer above does not change.
