# NEXT TASK — visualize the book graph in a dedicated tool ("go" to run)

When the user says **"go"**, execute this. Goal: load the live Cloud Run graph into
a DEDICATED graph-visualization tool. Do NOT hand-build a custom web viz — the only
code allowed is a small one-off EXPORT script; the visualization itself must be an
existing tool (Neo4j or simpler).

## The data to visualize
SQLite at `book-graph/seed/book.db` (same graph baked into the live Cloud Run image;
rebuild with `node book-graph/build.mjs`). Tables:
- `content_nodes(id, lesson_id, page_id, type, text, has_prereqs)` — 1748 nodes
- `prereq_nodes(id, content_node_id, concept, layer, is_floor, check_question)` — 597
- `prereq_edges(id, content_node_id, concept, requires, why)` — 712
- book structure: `book/chapters/lessons/pages`; session overlay: `sessions/session_logs`
Most worth viewing: the **74 prerequisite graphs** (a concept content node → its
prereq_nodes by layer → down to the `equation/variable literacy` floor).

## On "go"
1. Write a one-off `book-graph/export_graph.mjs` that emits BOTH:
   - `book-graph/export/graph.graphml` (nodes + edges) for Gephi / Cytoscape / yEd
   - `book-graph/export/neo4j.cypher` (CREATE statements) for Neo4j Browser/Desktop/Aura
   Default scope = the prereq graphs: each covered concept content node + its
   prereq_nodes (carry concept, layer, is_floor, check_question) + prereq_edges
   (concept ⟶ requires). Optionally include chapters→lessons→concept as an outer layer.
2. Detect the least-friction working tool, in order, and use it:
   a. `timeout 2 docker info` — if the daemon is UP NOW, run a Neo4j container,
      load `neo4j.cypher` via `cypher-shell -u neo4j -p graphtutor123`, `open http://localhost:7474`.
      (NOTE: Docker Desktop's daemon did NOT start earlier this project — likely still down.)
   b. else if Neo4j Desktop / `cypher-shell` present → use it.
   c. else if Gephi present (`/Applications/Gephi.app`) → `open -a Gephi book-graph/export/graph.graphml`.
   d. else recommend ONE and produce the export so it's import-ready: simplest =
      `brew install --cask gephi` (no account, no Docker); alt = Neo4j Aura Free (hosted) or Neo4j Desktop.
3. Keep it light; per standing preference, delegate substantive work to a subagent/Workflow.

## Current state (post-merge)
- ONE live connector: `book-tutor-mcp` → https://book-tutor-mcp-be2zley2na-ww.a.run.app/mcp
  (15 tools, pure pre-built model, tested OK). `graph-log-mcp` deleted.
- `main` = add0b86. Working tree should be clean.
- Standing user pref: fan out to subagents/Workflow to conserve main context; token cost OK.
