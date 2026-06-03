# book-graph — shared book graph + per-student session overlay

Two things, built from the real physics book (`../chatgpt-app/data/`):

## Part 1 — the book graph (shared, stable)
Built from `library.json` (chapters→lessons) + `lesson_pages/<code>.json` (pages→blocks):

```
book → chapters → lessons → pages → content_nodes (typed)
```

- **Content-node types are book-derived**, not a forced list: `question, paragraph,
  figure, equation, heading, question_set, key_term, margin_note, worked_example,
  objectives, table` (detected from each block's own `type`).
- Content that **has prerequisites** (laws / key concepts — judged) gets its **own
  prerequisite graph attached to that node**, decomposed layer by layer down to the
  **floor (equation/variable literacy)**, with **one check question per prereq node**.
- Prereqs are **NOT deduplicated** across content nodes (intended for this phase):
  if "division" is a prerequisite for three laws, it appears three times.

Authored prereq graphs live in `prereqs.mjs` (Kepler's third law, Newton's
universal gravitation, angular velocity). Add more by the same pattern.

## Part 2 — the session / student overlay (per student, references the book graph)
```
student → sessions → session_logs → reference → shared book-graph node
```
- A student has many **sessions** (one chat = one session id), kept separate.
- A session **references** book-graph node ids (it does not copy them); the
  struggle/mastery is logged **on the link** (`session_logs.ref_kind + ref_id + outcome`).
- A log can reference either a `content` node or a `prereq` node.

## Run
```bash
node build.mjs      # ingest the book + attach prereq graphs   (npm run build)
node demo.mjs       # structure + 2 full prereq graphs + a session logging a struggle
```

Build summary: **6 chapters · 13 lessons · 187 pages · 1,748 content nodes**;
3 content nodes carry full prerequisite graphs.

## Storage
Node built-in `node:sqlite` (same family as graph-log), file at `data/book.db`
(gitignored, rebuilt by `build.mjs`). Honors `BOOKGRAPH_DB`.

- `db.mjs` — schema + functions (book graph + prereqs + session overlay)
- `prereqs.mjs` — authored prerequisite graphs (anchored to real content nodes)
- `build.mjs` — ingest the book JSON, attach prereq graphs
- `demo.mjs` — end-to-end demonstration
