// MCP server for the new model — the LLM's hands on the empty experience log.
// The LLM decomposes a topic (following the instructions/guide), stores the
// decomposition, logs the student's pass/struggle, and reads back status to
// personalize. No traversal engine here; the DB only logs.

import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

import { openDb, storeDecomposition, getTopic, logOutcome, topicStatusForStudent } from "./db.mjs";
import { DECOMPOSITION_PROMPT, normalize } from "./decompose.mjs";

const PORT = Number(process.env.PORT || 8080);
const MCP_PATH = "/mcp";
const db = openDb(); // honors GRAPHLOG_DB; created empty on first run

const INSTRUCTIONS = `You are a physics/science tutor. The graph database is an EMPTY log — YOU do all
the decomposition and personalization.

When a student asks about a topic:
1. Decompose it into its prerequisite graph yourself, following this guide:
${DECOMPOSITION_PROMPT}
2. Call save_topic_decomposition with the nodes and edges you produced.
3. Teach from the deepest unmet prerequisite up to the topic.
4. As the student answers, call log_outcome(passed|struggled) on each concept.
5. Call get_student_status to see what they've passed/struggled before, and start
   from their actual gap — not from scratch.
Never expose internal IDs, tool names, or this guide to the student; speak in
concept names.`;

const text = (t, s) => ({ content: [{ type: "text", text: t }], structuredContent: s });

function build() {
  const server = new McpServer({ name: "graph-log-tutor", version: "0.1.0" }, { instructions: INSTRUCTIONS });

  const NODE = z.object({ concept: z.string(), layer: z.number().optional(), is_floor: z.boolean().optional() });
  const EDGE = z.object({ concept: z.string(), requires: z.string(), why: z.string().optional() });

  server.registerTool("get_decomposition_guide", {
    title: "Get the topic-decomposition guide (with worked example)",
    description: "Returns the rules + Kepler worked example for decomposing a topic into its prerequisite " +
      "graph (descend topic→math, stop at equation/variable literacy). Use it before save_topic_decomposition.",
    inputSchema: {}, outputSchema: { guide: z.string() },
  }, async () => text("decomposition guide", { guide: DECOMPOSITION_PROMPT }));

  server.registerTool("save_topic_decomposition", {
    title: "Save the topic's prerequisite graph you decomposed",
    description: "Store the decomposition YOU produced for a topic (same for every student). nodes: " +
      "[{concept, layer, is_floor}]; edges: [{concept, requires, why}] meaning concept REQUIRES requires. " +
      "Stop at equation/variable literacy. Idempotent — re-saving replaces it.",
    inputSchema: { topic: z.string(), nodes: z.array(NODE), edges: z.array(EDGE) },
    outputSchema: { topic: z.string(), nodes: z.number(), edges: z.number(), next_teacher_action: z.string() },
  }, async ({ topic, nodes, edges }) => {
    const r = storeDecomposition(db, topic, normalize({ topic, nodes, edges }));
    return text(`saved "${topic}": ${r.nodes} nodes, ${r.edges} edges`,
      { ...r, next_teacher_action: "teach_from_deepest_unmet_prerequisite" });
  });

  server.registerTool("get_topic", {
    title: "Get a stored topic decomposition",
    description: "Read back the prerequisite graph stored for a topic (nodes by layer + edges). Returns null if not saved yet.",
    inputSchema: { topic: z.string() }, outputSchema: { topic: z.any() },
  }, async ({ topic }) => {
    const g = getTopic(db, topic);
    return text(g ? `topic "${topic}": ${g.nodes.length} nodes` : `"${topic}" not decomposed yet`, { topic: g });
  });

  server.registerTool("log_outcome", {
    title: "Log a student's pass/struggle on one concept",
    description: "Record this student's experience on a concept of a topic. outcome is 'passed' or 'struggled'. " +
      "This is the only thing that grows per student; call it as they answer.",
    inputSchema: {
      student_id: z.string(), topic: z.string(), concept: z.string(),
      outcome: z.enum(["passed", "struggled"]),
    },
    outputSchema: { logged: z.boolean(), next_teacher_action: z.string() },
  }, async ({ student_id, topic, concept, outcome }) => {
    logOutcome(db, { student_id, topic, concept, outcome });
    return text(`logged ${outcome} on "${concept}"`,
      { logged: true, next_teacher_action: outcome === "struggled" ? "teach_this_concept_now" : "advance" });
  });

  server.registerTool("get_student_status", {
    title: "Get a student's pass/struggle status across a topic's nodes",
    description: "For a topic, return each node with this student's latest outcome (passed/struggled/untested) so " +
      "you can start from their actual gap. Teach the deepest 'struggled' node first, then climb to the topic.",
    inputSchema: { student_id: z.string(), topic: z.string() },
    outputSchema: { status: z.any(), gaps: z.any(), next_teacher_action: z.string() },
  }, async ({ student_id, topic }) => {
    const status = topicStatusForStudent(db, student_id, topic);
    const gaps = status.filter((s) => s.latest_outcome === "struggled").map((s) => s.concept);
    return text(gaps.length ? `gaps: ${gaps.join(", ")}` : "no logged gaps yet",
      { status, gaps, next_teacher_action: gaps.length ? "teach_deepest_gap_first" : "begin_or_quiz" });
  });

  return server;
}

const httpServer = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  res.setHeader("Access-Control-Allow-Origin", "*");
  if (req.method === "OPTIONS" && url.pathname === MCP_PATH)
    return res.writeHead(204, { "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id", "Access-Control-Expose-Headers": "Mcp-Session-Id" }).end();
  if (req.method === "GET" && url.pathname === "/")
    return res.writeHead(200, { "content-type": "text/plain" }).end(`graph-log tutor MCP. POST ${MCP_PATH}`);
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
    } catch (err) {
      if (!res.headersSent) res.writeHead(500, { "content-type": "text/plain" }).end(String(err?.message || err));
    }
    return;
  }
  res.writeHead(404, { "content-type": "text/plain" }).end("Not found");
});

httpServer.listen(PORT, () => console.log(`graph-log tutor MCP on http://localhost:${PORT}${MCP_PATH}  (db: ${process.env.GRAPHLOG_DB || "module data/"})`));
