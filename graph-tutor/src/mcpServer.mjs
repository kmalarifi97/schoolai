// MCP server wired DIRECTLY to the GraphQL graph endpoint.
// The LLM (ChatGPT custom app) calls these tools; each tool issues a GraphQL
// query against the graph DB. No KST engine — diagnosis is graph traversal,
// served by the `diagnose` GraphQL query. Tool outputs are self-guiding (they
// name the next teacher action) in the same spirit as the old app.

import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const GRAPHQL_URL = process.env.GRAPHQL_URL || "http://localhost:4000/graphql";
const MCP_PATH = "/mcp";
const PORT = Number(process.env.MCP_PORT || 4100);

async function gql(query, variables) {
  const r = await fetch(GRAPHQL_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (j.errors) throw new Error(j.errors.map((e) => e.message).join("; "));
  return j.data;
}

const text = (t, structured) => ({ content: [{ type: "text", text: t }], structuredContent: structured });

function createGraphTutorServer() {
  const server = new McpServer({ name: "graph-tutor", version: "0.1.0" });

  // ---- list_skills ----
  server.registerTool(
    "list_skills",
    {
      title: "List the skills in the prerequisite graph",
      description:
        "Use this when starting a session or building a diagnostic quiz, to see " +
        "the available skills and how they connect. Returns each skill with its " +
        "direct prerequisites. Do not dump the whole list to the student; use it " +
        "to choose which skills to quiz.",
      inputSchema: {},
      outputSchema: { skills: z.any(), count: z.number() },
    },
    async () => {
      const d = await gql(`{ skills { id name prerequisites { id name } dependents { id name } } }`);
      return text(`${d.skills.length} skills in the graph.`, { skills: d.skills, count: d.skills.length });
    }
  );

  // ---- get_skill_prerequisites ----
  server.registerTool(
    "get_skill_prerequisites",
    {
      title: "Get the prerequisite chain for one skill",
      description:
        "Use this to see what a skill depends on before teaching it. Pass the " +
        "skill id; set recursive:true for the full upstream chain. Teach from the " +
        "earliest unmet prerequisite forward.",
      inputSchema: {
        id: z.string().describe("Skill id (from list_skills)"),
        recursive: z.boolean().optional().describe("true = full upstream chain; false = direct prerequisites only"),
      },
      outputSchema: { skill: z.any(), prerequisites: z.any() },
    },
    async ({ id, recursive }) => {
      const d = await gql(
        `query($id:ID!,$r:Boolean){ skill(id:$id){ id name prerequisites(recursive:$r){ id name } } }`,
        { id, r: !!recursive }
      );
      if (!d.skill) return text(`لا يوجد مهارة بهذا المعرّف: ${id}`, { skill: null, prerequisites: [] });
      return text(
        `"${d.skill.name}" يعتمد على: ${d.skill.prerequisites.map((p) => p.name).join("، ") || "لا متطلبات"}.`,
        { skill: { id: d.skill.id, name: d.skill.name }, prerequisites: d.skill.prerequisites }
      );
    }
  );

  // ---- diagnose_student_from_quiz (the core tool) ----
  server.registerTool(
    "diagnose_student_from_quiz",
    {
      title: "Diagnose student weaknesses from quiz results (preferred)",
      description:
        "Use this after a student takes a short diagnostic quiz across several " +
        "skills. Pass the skill ids they PASSED and the ids they FAILED. The graph " +
        "is traversed backward from each failed skill to find the prerequisites the " +
        "student has not mastered, and returns the root cause to teach first plus " +
        "the chain back up to the failed skill. Teach the rootCause first, then " +
        "climb the chain. Never expose skill ids or graph internals to the student; " +
        "speak in concepts.",
      inputSchema: {
        passed: z.array(z.string()).optional().describe("Skill ids the student answered correctly"),
        failed: z.array(z.string()).optional().describe("Skill ids the student got wrong"),
      },
      outputSchema: {
        next_teacher_action: z.string(),
        summary: z.string(),
        failed: z.any(),
      },
    },
    async ({ passed, failed }) => {
      const d = await gql(
        `query($p:[ID!]!,$f:[ID!]!){
           diagnose(passed:$p, failed:$f){
             summary
             failed {
               skill { id name }
               rootCause { id name }
               recommendation
               chain { skill { id name } status depth }
               notMastered { skill { id name } status depth }
             }
           }
         }`,
        { p: passed || [], f: failed || [] }
      );
      const diag = d.diagnose;
      const action = diag.failed.some((f) => f.rootCause) ? "teach_root_cause_first" : "review_failed_skills_directly";
      return text(diag.summary, { next_teacher_action: action, summary: diag.summary, failed: diag.failed });
    }
  );

  return server;
}

const httpServer = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  res.setHeader("Access-Control-Allow-Origin", "*");

  if (req.method === "OPTIONS" && url.pathname === MCP_PATH) {
    return res
      .writeHead(204, {
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type, mcp-session-id",
        "Access-Control-Expose-Headers": "Mcp-Session-Id",
      })
      .end();
  }
  if (req.method === "GET" && url.pathname === "/") {
    return res.writeHead(200, { "content-type": "text/plain" }).end(`graph-tutor MCP. POST ${MCP_PATH}\nGraphQL: ${GRAPHQL_URL}`);
  }
  if (url.pathname === MCP_PATH && (req.method === "GET" || req.method === "DELETE")) {
    return res.writeHead(405, { allow: "POST", "content-type": "text/plain" }).end("Method Not Allowed; use POST");
  }
  if (url.pathname === MCP_PATH && req.method === "POST") {
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
    const server = createGraphTutorServer();
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.on("close", () => { transport.close(); server.close(); });
    try {
      transport.onerror = (e) => console.error("transport.onerror:", e?.message || e);
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (err) {
      console.error("handleRequest threw:", err?.stack || err);
      if (!res.headersSent) res.writeHead(500, { "content-type": "text/plain" }).end(String(err?.message || err));
    }
    return;
  }
  res.writeHead(404, { "content-type": "text/plain" }).end("Not found");
});

httpServer.listen(PORT, () => {
  console.log(`graph-tutor MCP on http://localhost:${PORT}${MCP_PATH}`);
  console.log(`-> GraphQL backend: ${GRAPHQL_URL}`);
});
