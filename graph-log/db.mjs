// The graph database — an EMPTY experience log that fills as students learn.
// It is NOT a pre-authored map and there is NO traversal engine. It stores only:
//   (a) a topic's decomposition (the prerequisite graph the LLM produced), and
//   (b) per-student pass/struggle logs against those nodes.
// Backed by Node's built-in SQLite (zero install). Starts empty on first run.

import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_DB = fileURLToPath(new URL("data/tutor.db", import.meta.url));

export function openDb(path = DEFAULT_DB) {
  if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
  const db = new DatabaseSync(path);
  db.exec(`
    CREATE TABLE IF NOT EXISTS topics (
      topic TEXT PRIMARY KEY,
      created_at TEXT
    );
    -- a node = one concept in a topic's decomposition (layer 0 = the topic itself,
    -- higher layer = deeper prerequisite; is_floor = the stopping point).
    CREATE TABLE IF NOT EXISTS nodes (
      topic TEXT, concept TEXT, layer INTEGER, is_floor INTEGER DEFAULT 0,
      PRIMARY KEY (topic, concept)
    );
    -- an edge = "concept REQUIRES prerequisite" (why explains the dependency).
    CREATE TABLE IF NOT EXISTS edges (
      topic TEXT, concept TEXT, requires TEXT, why TEXT,
      PRIMARY KEY (topic, concept, requires)
    );
    -- per-student experience log against decomposed nodes.
    CREATE TABLE IF NOT EXISTS logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      student_id TEXT, topic TEXT, concept TEXT,
      outcome TEXT CHECK (outcome IN ('passed','struggled')),
      ts TEXT
    );
  `);
  return db;
}

// Store the LLM's decomposition for a topic (idempotent — re-storing replaces it).
// The topic graph is the SAME for everyone; only logs are per-student.
export function storeDecomposition(db, topic, { nodes, edges }, now = new Date().toISOString()) {
  db.prepare(`INSERT INTO topics(topic, created_at) VALUES(?, ?)
              ON CONFLICT(topic) DO NOTHING`).run(topic, now);
  const insNode = db.prepare(`INSERT INTO nodes(topic, concept, layer, is_floor) VALUES(?,?,?,?)
                              ON CONFLICT(topic, concept) DO UPDATE SET layer=excluded.layer, is_floor=excluded.is_floor`);
  for (const n of nodes) insNode.run(topic, n.concept, n.layer ?? 0, n.is_floor ? 1 : 0);
  const insEdge = db.prepare(`INSERT INTO edges(topic, concept, requires, why) VALUES(?,?,?,?)
                              ON CONFLICT(topic, concept, requires) DO UPDATE SET why=excluded.why`);
  for (const e of edges) insEdge.run(topic, e.concept, e.requires, e.why || null);
  return { topic, nodes: nodes.length, edges: edges.length };
}

export function getTopic(db, topic) {
  const t = db.prepare(`SELECT topic, created_at FROM topics WHERE topic=?`).get(topic);
  if (!t) return null;
  const nodes = db.prepare(`SELECT concept, layer, is_floor FROM nodes WHERE topic=? ORDER BY layer, concept`).all(topic);
  const edges = db.prepare(`SELECT concept, requires, why FROM edges WHERE topic=?`).all(topic);
  return { topic, nodes, edges };
}

// Log a student's outcome on one concept. outcome ∈ {passed, struggled}.
export function logOutcome(db, { student_id, topic, concept, outcome, ts = new Date().toISOString() }) {
  db.prepare(`INSERT INTO logs(student_id, topic, concept, outcome, ts) VALUES(?,?,?,?,?)`)
    .run(student_id, topic, concept, outcome, ts);
}

export function getStudentLog(db, student_id) {
  return db.prepare(`SELECT topic, concept, outcome, ts FROM logs WHERE student_id=? ORDER BY ts`).all(student_id);
}

// The personalization the LLM reads: for a topic, each node + this student's
// latest outcome on it (null = not yet attempted). The LLM decides what to do.
export function topicStatusForStudent(db, student_id, topic) {
  return db.prepare(`
    SELECT n.concept, n.layer, n.is_floor,
           (SELECT outcome FROM logs l WHERE l.student_id=? AND l.topic=n.topic AND l.concept=n.concept
            ORDER BY l.ts DESC LIMIT 1) AS latest_outcome
    FROM nodes n WHERE n.topic=? ORDER BY n.layer, n.concept
  `).all(student_id, topic);
}

export function counts(db) {
  return {
    topics: db.prepare(`SELECT COUNT(*) c FROM topics`).get().c,
    nodes: db.prepare(`SELECT COUNT(*) c FROM nodes`).get().c,
    edges: db.prepare(`SELECT COUNT(*) c FROM edges`).get().c,
    logs: db.prepare(`SELECT COUNT(*) c FROM logs`).get().c,
  };
}
