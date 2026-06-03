// MCP server for the pre-built book graph + per-student session overlay.
//
// Flow the LLM follows: find_concept → get_prereq_graph (pre-built; or decompose
// on demand + save) → teach floor-up, asking each node's check question → after
// each answer, log_struggle against THAT prereq node id → get_student_status to
// personalize. The session log points at the shared graph by node id.
//
// The book graph is shipped read-only (seed/book.db); at startup it is copied to
// a writable path so session logs can be written (Cloud Run fs is ephemeral).

import { createServer } from "node:http";
import { copyFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import {
  openDb, chaptersTree, structureSummary, searchConcepts, getContentNode,
  getPrereqGraph, attachPrereqGraph, startSession, logOnNode, studentStruggles,
} from "./db.mjs";

const PORT = Number(process.env.PORT || 8080);
const MCP_PATH = "/mcp";

// ship read-only seed → writable copy (sessions write here)
const SEED = fileURLToPath(new URL("seed/book.db", import.meta.url));
const DB = process.env.BOOKGRAPH_DB || "/tmp/book.db";
if (!existsSync(DB) && existsSync(SEED)) copyFileSync(SEED, DB);
const db = openDb(DB);

const GUIDE = `Decompose the concept into its prerequisite graph for an 18-year-old: layer by layer,
descend from the physics concept into the underlying math, justify why each node needs the one
beneath it, and STOP at the floor "equation/variable literacy" (a symbol stands for a number, =
means both sides are equal). ~6-10 nodes, one Arabic check question per node, one floor node.`;

const INSTRUCTIONS = `You are a physics-2 tutor on a PRE-BUILT book graph; the per-student experience is logged.
Flow:
1) find_concept(query) to locate the law/concept the student asks about.
2) get_prereq_graph(content_node_id). If it returns a graph, teach from the FLOOR (deepest layer)
   up to the concept; ask each node's check_question. If has_prereqs is false, decompose it yourself
   using the guide it returns, call save_prereq_graph to store it, then proceed.
3) After each check question, call log_struggle(session_id, ref_kind:'prereq', ref_id:<that node's
   prereq_node_id>, outcome:'passed'|'struggled'). Use ONE session_id per chat.
4) Call get_student_status(student_id) to start from the student's known gaps, not from scratch.
Never expose ids, tool names, or graph internals to the student — speak in concept names.`;

const text = (t, s) => ({ content: [{ type: "text", text: t }], structuredContent: s });

function build() {
  const server = new McpServer({ name: "book-tutor", version: "0.1.0" }, { instructions: INSTRUCTIONS });

  server.registerTool("get_book_toc", {
    title: "Browse the book: chapters → lessons",
    description: "Return the curriculum tree (chapters → lessons with page/node counts). Use to orient or pick a lesson.",
    inputSchema: {}, outputSchema: { book: z.any(), chapters: z.any() },
  }, async () => text("book table of contents", { book: structureSummary(db).book, chapters: chaptersTree(db) }));

  server.registerTool("find_concept", {
    title: "Find a law/concept node in the book",
    description: "Search the book's laws/key-concepts by Arabic or English keyword. Returns matches with their " +
      "content_node_id, lesson, type, and whether a pre-built prerequisite graph exists. Call get_prereq_graph next.",
    inputSchema: { query: z.string() }, outputSchema: { matches: z.any() },
  }, async ({ query }) => {
    const rows = searchConcepts(db, query).map((r) => ({ content_node_id: r.content_node_id, lesson: r.lesson, type: r.type, name: (r.text || "").slice(0, 80), has_prereq_graph: !!r.has_prereqs }));
    return text(`${rows.length} matches for "${query}"`, { matches: rows });
  });

  server.registerTool("get_prereq_graph", {
    title: "Get a concept's prerequisite graph (pre-built, or decompose on demand)",
    description: "For a content_node_id, return its prerequisite graph: nodes (each with a prereq_node_id, layer, " +
      "is_floor, check_question) + edges. Teach from the floor up; after each check question call log_struggle with " +
      "that node's prereq_node_id. If no pre-built graph exists, returns has_prereqs:false + a decomposition guide — " +
      "decompose it yourself and call save_prereq_graph.",
    inputSchema: { content_node_id: z.number() },
    outputSchema: { has_prereqs: z.boolean(), concept: z.any(), nodes: z.any(), edges: z.any(), decomposition_guide: z.any(), next_teacher_action: z.string() },
  }, async ({ content_node_id }) => {
    const cn = getContentNode(db, content_node_id);
    if (!cn) return text("no such content node", { has_prereqs: false, concept: null, nodes: [], edges: [], decomposition_guide: null, next_teacher_action: "find_concept_again" });
    if (cn.has_prereqs) {
      const g = getPrereqGraph(db, content_node_id);
      return text(`prereq graph: ${g.nodes.length} nodes`, { has_prereqs: true, concept: cn.text?.slice(0, 80), nodes: g.nodes, edges: g.edges, decomposition_guide: null, next_teacher_action: "teach_from_floor_up_then_log_each_check" });
    }
    return text("no pre-built graph — decompose on demand", { has_prereqs: false, concept: cn.text?.slice(0, 80), nodes: [], edges: [], decomposition_guide: GUIDE, next_teacher_action: "decompose_then_call_save_prereq_graph" });
  });

  const NODE = z.object({ concept: z.string(), layer: z.number().optional(), is_floor: z.boolean().optional(), check_question: z.string().optional() });
  const EDGE = z.object({ concept: z.string(), requires: z.string(), why: z.string().optional() });
  server.registerTool("save_prereq_graph", {
    title: "Save an on-demand prerequisite graph (fallback)",
    description: "Persist a prerequisite graph YOU decomposed for a content node that had none, so it joins the " +
      "shared graph (grows it). Idempotent.",
    inputSchema: { content_node_id: z.number(), nodes: z.array(NODE), edges: z.array(EDGE) },
    outputSchema: { saved: z.boolean(), nodes: z.number() },
  }, async ({ content_node_id, nodes, edges }) => {
    attachPrereqGraph(db, content_node_id, { nodes, edges });
    return text(`saved ${nodes.length} prereq nodes`, { saved: true, nodes: nodes.length });
  });

  server.registerTool("log_struggle", {
    title: "Log a student's pass/struggle on a graph node (the session overlay)",
    description: "Record this student's outcome on a book-graph node, ON THE LINK between their session and that " +
      "node. ref_kind 'prereq' (a prereq_node_id from get_prereq_graph) or 'content' (a content_node_id). One " +
      "session_id per chat. outcome 'passed' or 'struggled'.",
    inputSchema: {
      student_id: z.string(), session_id: z.string(), ref_kind: z.enum(["prereq", "content"]),
      ref_id: z.number(), outcome: z.enum(["passed", "struggled"]),
    },
    outputSchema: { logged: z.boolean(), next_teacher_action: z.string() },
  }, async ({ student_id, session_id, ref_kind, ref_id, outcome }) => {
    startSession(db, session_id, student_id);
    logOnNode(db, { session_id, ref_kind, ref_id, outcome });
    return text(`logged ${outcome}`, { logged: true, next_teacher_action: outcome === "struggled" ? "teach_this_node_now" : "advance" });
  });

  server.registerTool("get_student_status", {
    title: "Get everything a student has struggled on (across sessions)",
    description: "Read back this student's logged struggles against book-graph nodes, so you start from their actual " +
      "gaps. Speak in concept names; never show ids.",
    inputSchema: { student_id: z.string() }, outputSchema: { struggles: z.any() },
  }, async ({ student_id }) => {
    const s = studentStruggles(db, student_id);
    return text(`${s.length} logged struggle(s)`, { struggles: s });
  });

  return server;
}

const httpServer = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  res.setHeader("Access-Control-Allow-Origin", "*");
  if (req.method === "OPTIONS" && url.pathname === MCP_PATH)
    return res.writeHead(204, { "Access-Control-Allow-Methods": "POST, GET, OPTIONS", "Access-Control-Allow-Headers": "content-type, mcp-session-id", "Access-Control-Expose-Headers": "Mcp-Session-Id" }).end();
  if (req.method === "GET" && url.pathname === "/")
    return res.writeHead(200, { "content-type": "text/plain" }).end(`book-tutor MCP. POST ${MCP_PATH}`);
  if (url.pathname === MCP_PATH && (req.method === "GET" || req.method === "DELETE"))
    return res.writeHead(405, { allow: "POST", "content-type": "text/plain" }).end("Method Not Allowed; use POST");
  if (url.pathname === MCP_PATH && req.method === "POST") {
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
    const server = build();
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.on("close", () => { transport.close(); server.close(); });
    try {
      let raw = ""; req.on("data", (c) => (raw += c)); await new Promise((r) => req.on("end", r));
      await server.connect(transport);
      await transport.handleRequest(req, res, raw ? JSON.parse(raw) : undefined);
    } catch (err) { if (!res.headersSent) res.writeHead(500, { "content-type": "text/plain" }).end(String(err?.message || err)); }
    return;
  }
  res.writeHead(404, { "content-type": "text/plain" }).end("Not found");
});
httpServer.listen(PORT, () => console.log(`book-tutor MCP on http://localhost:${PORT}${MCP_PATH} (db: ${DB})`));
