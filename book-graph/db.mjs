// Storage for (1) the shared, stable BOOK GRAPH built from the physics book, and
// (2) the per-student SESSION overlay that references book-graph nodes.
// Node built-in SQLite (same family as graph-log). Honors BOOKGRAPH_DB.
//
// Book graph:  book → chapters → lessons → pages → content_nodes (typed).
//   A content node that has prerequisites gets its OWN prereq graph attached
//   (prereq_nodes + prereq_edges), each prereq node carrying a check question.
//   Prereqs are NOT deduplicated across content nodes (intended for this phase).
// Session overlay:  student → sessions → session_logs, where a log REFERENCES a
//   book-graph node id and records the struggle/mastery ON THAT LINK.

import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_DB = process.env.BOOKGRAPH_DB || fileURLToPath(new URL("data/book.db", import.meta.url));

export function openDb(path = DEFAULT_DB) {
  if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
  const db = new DatabaseSync(path);
  db.exec(`
    -- shared book graph --------------------------------------------------------
    CREATE TABLE IF NOT EXISTS book     (id INTEGER PRIMARY KEY, title TEXT);
    CREATE TABLE IF NOT EXISTS chapters (id INTEGER PRIMARY KEY, book_id INTEGER, number INTEGER, title_ar TEXT, title_en TEXT);
    CREATE TABLE IF NOT EXISTS lessons  (id INTEGER PRIMARY KEY AUTOINCREMENT, chapter_id INTEGER, code TEXT, title_ar TEXT, title_en TEXT, page_range TEXT);
    CREATE TABLE IF NOT EXISTS pages    (id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER, page_number INTEGER);
    CREATE TABLE IF NOT EXISTS content_nodes (
      id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER, page_id INTEGER,
      type TEXT, ordinal INTEGER, block_id TEXT, text TEXT, has_prereqs INTEGER DEFAULT 0
    );
    -- prerequisite graph attached to one content node (NOT deduped) ------------
    CREATE TABLE IF NOT EXISTS prereq_nodes (
      id INTEGER PRIMARY KEY AUTOINCREMENT, content_node_id INTEGER,
      concept TEXT, layer INTEGER, is_floor INTEGER DEFAULT 0, check_question TEXT
    );
    CREATE TABLE IF NOT EXISTS prereq_edges (
      id INTEGER PRIMARY KEY AUTOINCREMENT, content_node_id INTEGER,
      concept TEXT, requires TEXT, why TEXT
    );
    -- per-student session overlay ---------------------------------------------
    CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY);
    CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, student_id TEXT, started_at TEXT);
    -- struggle/mastery on the LINK between a session and a referenced node.
    -- ref_kind ∈ {'content','prereq'}; ref_id → content_nodes.id | prereq_nodes.id
    CREATE TABLE IF NOT EXISTS session_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT,
      ref_kind TEXT, ref_id INTEGER, outcome TEXT CHECK (outcome IN ('passed','struggled')), ts TEXT
    );
  `);
  return db;
}

// ---- book-graph build (used by build.mjs) ----
export const reset = (db) => db.exec(`DELETE FROM book; DELETE FROM chapters; DELETE FROM lessons; DELETE FROM pages; DELETE FROM content_nodes; DELETE FROM prereq_nodes; DELETE FROM prereq_edges;`);
export const setBook = (db, id, title) => db.prepare(`INSERT OR REPLACE INTO book(id,title) VALUES(?,?)`).run(id, title);
export const addChapter = (db, { id, book_id, number, title_ar, title_en }) =>
  db.prepare(`INSERT OR REPLACE INTO chapters(id,book_id,number,title_ar,title_en) VALUES(?,?,?,?,?)`).run(id, book_id, number, title_ar, title_en);
export const addLesson = (db, { chapter_id, code, title_ar, title_en, page_range }) =>
  Number(db.prepare(`INSERT INTO lessons(chapter_id,code,title_ar,title_en,page_range) VALUES(?,?,?,?,?)`).run(chapter_id, code, title_ar, title_en, page_range).lastInsertRowid);
export const addPage = (db, lesson_id, page_number) =>
  Number(db.prepare(`INSERT INTO pages(lesson_id,page_number) VALUES(?,?)`).run(lesson_id, page_number).lastInsertRowid);
export const addContentNode = (db, { lesson_id, page_id, type, ordinal, block_id, text }) =>
  Number(db.prepare(`INSERT INTO content_nodes(lesson_id,page_id,type,ordinal,block_id,text) VALUES(?,?,?,?,?,?)`).run(lesson_id, page_id, type, ordinal, block_id || null, text || null).lastInsertRowid);

// Attach a prerequisite graph (with check questions) to a content node.
export function attachPrereqGraph(db, content_node_id, { nodes, edges }) {
  db.prepare(`UPDATE content_nodes SET has_prereqs=1 WHERE id=?`).run(content_node_id);
  const insN = db.prepare(`INSERT INTO prereq_nodes(content_node_id,concept,layer,is_floor,check_question) VALUES(?,?,?,?,?)`);
  for (const n of nodes) insN.run(content_node_id, n.concept, n.layer ?? 0, n.is_floor ? 1 : 0, n.check_question || null);
  const insE = db.prepare(`INSERT INTO prereq_edges(content_node_id,concept,requires,why) VALUES(?,?,?,?)`);
  for (const e of edges) insE.run(content_node_id, e.concept, e.requires, e.why || null);
}

// Find a content node by a text/type/lesson hint (used to anchor a prereq graph).
export const findContentNode = (db, { lessonCode, type, like }) =>
  db.prepare(`SELECT cn.* FROM content_nodes cn JOIN lessons l ON l.id=cn.lesson_id
              WHERE (? IS NULL OR l.code=?) AND (? IS NULL OR cn.type=?) AND (? IS NULL OR cn.text LIKE ?)
              ORDER BY cn.id LIMIT 1`).get(lessonCode ?? null, lessonCode ?? null, type ?? null, type ?? null, like ?? null, like ? `%${like}%` : null);

// ---- queries ----
export const structureSummary = (db) => ({
  book: db.prepare(`SELECT title FROM book LIMIT 1`).get()?.title,
  chapters: db.prepare(`SELECT COUNT(*) c FROM chapters`).get().c,
  lessons: db.prepare(`SELECT COUNT(*) c FROM lessons`).get().c,
  pages: db.prepare(`SELECT COUNT(*) c FROM pages`).get().c,
  content_nodes: db.prepare(`SELECT COUNT(*) c FROM content_nodes`).get().c,
  by_type: db.prepare(`SELECT type, COUNT(*) c FROM content_nodes GROUP BY type ORDER BY c DESC`).all(),
  with_prereqs: db.prepare(`SELECT COUNT(*) c FROM content_nodes WHERE has_prereqs=1`).get().c,
});
export const chaptersTree = (db) => db.prepare(`
  SELECT c.number, c.title_ar AS chapter, l.code, l.title_ar AS lesson,
    (SELECT COUNT(*) FROM pages p WHERE p.lesson_id=l.id) AS pages,
    (SELECT COUNT(*) FROM content_nodes cn WHERE cn.lesson_id=l.id) AS nodes
  FROM chapters c JOIN lessons l ON l.chapter_id=c.id ORDER BY c.number, l.code`).all();
export const getContentNode = (db, id) => db.prepare(`SELECT * FROM content_nodes WHERE id=?`).get(id);
export const getPrereqGraph = (db, content_node_id) => ({
  nodes: db.prepare(`SELECT concept, layer, is_floor, check_question FROM prereq_nodes WHERE content_node_id=? ORDER BY layer, id`).all(content_node_id),
  edges: db.prepare(`SELECT concept, requires, why FROM prereq_edges WHERE content_node_id=?`).all(content_node_id),
});
export const contentNodesWithPrereqs = (db) => db.prepare(`
  SELECT cn.id, cn.type, cn.text, l.code AS lesson FROM content_nodes cn JOIN lessons l ON l.id=cn.lesson_id
  WHERE cn.has_prereqs=1 ORDER BY cn.id`).all();

// ---- session overlay ----
export const ensureStudent = (db, id) => db.prepare(`INSERT OR IGNORE INTO students(id) VALUES(?)`).run(id);
export function startSession(db, session_id, student_id, ts = new Date().toISOString()) {
  ensureStudent(db, student_id);
  db.prepare(`INSERT OR IGNORE INTO sessions(id,student_id,started_at) VALUES(?,?,?)`).run(session_id, student_id, ts);
  return session_id;
}
// Log struggle/mastery ON THE LINK between a session and a referenced book node.
export const logOnNode = (db, { session_id, ref_kind, ref_id, outcome, ts = new Date().toISOString() }) =>
  db.prepare(`INSERT INTO session_logs(session_id,ref_kind,ref_id,outcome,ts) VALUES(?,?,?,?,?)`).run(session_id, ref_kind, ref_id, outcome, ts);

// Read a session's logs joined back to the referenced book-graph nodes.
export const sessionLogs = (db, session_id) => db.prepare(`
  SELECT sl.ref_kind, sl.ref_id, sl.outcome, sl.ts,
    CASE sl.ref_kind WHEN 'prereq' THEN (SELECT concept FROM prereq_nodes WHERE id=sl.ref_id)
                     ELSE (SELECT type||': '||substr(text,1,60) FROM content_nodes WHERE id=sl.ref_id) END AS node
  FROM session_logs sl WHERE sl.session_id=? ORDER BY sl.ts`).all(session_id);

// All of a student's struggles across their sessions (overlay read-back).
export const studentStruggles = (db, student_id) => db.prepare(`
  SELECT s.id AS session_id, sl.ref_kind, sl.ref_id, sl.outcome,
    CASE sl.ref_kind WHEN 'prereq' THEN (SELECT concept FROM prereq_nodes WHERE id=sl.ref_id)
                     ELSE (SELECT type FROM content_nodes WHERE id=sl.ref_id) END AS node
  FROM sessions s JOIN session_logs sl ON sl.session_id=s.id
  WHERE s.student_id=? AND sl.outcome='struggled' ORDER BY s.id, sl.ts`).all(student_id);
