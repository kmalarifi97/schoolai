// GraphQL HTTP server over the prerequisite graph — the "graph DB" endpoint.
// Minimal: POST /graphql {query, variables}. No extra web framework.

import { createServer } from "node:http";
import { graphql } from "graphql";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { createGraphStore } from "./graphStore.mjs";
import { buildSchema } from "./schema.mjs";

const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..");
const GRAPH_PATH = process.env.GRAPH_PATH || join(ROOT, "graph", "seed.graph.json");
const PORT = Number(process.env.PORT || 4000);

const store = createGraphStore(GRAPH_PATH);
const schema = buildSchema(store);

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (c) => (data += c));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

export const httpServer = createServer(async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "content-type");
  res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
  if (req.method === "OPTIONS") return res.writeHead(204).end();

  if (req.method === "GET" && req.url === "/") {
    return res
      .writeHead(200, { "content-type": "text/plain" })
      .end(`graph-tutor GraphQL. POST /graphql\nGraph: ${GRAPH_PATH}\nNodes: ${store.allNodes().length}  Edges: ${store.allEdges().length}`);
  }
  if (req.url !== "/graphql" || req.method !== "POST") {
    return res.writeHead(404, { "content-type": "text/plain" }).end("POST /graphql");
  }

  try {
    const { query, variables, operationName } = JSON.parse((await readBody(req)) || "{}");
    if (!query) return res.writeHead(400, { "content-type": "application/json" }).end(JSON.stringify({ errors: [{ message: "missing query" }] }));
    const result = await graphql({ schema, source: query, variableValues: variables, operationName });
    res.writeHead(200, { "content-type": "application/json" }).end(JSON.stringify(result));
  } catch (err) {
    res.writeHead(400, { "content-type": "application/json" }).end(JSON.stringify({ errors: [{ message: String(err?.message || err) }] }));
  }
});

// start only when run directly (not when imported by smoke test)
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  httpServer.listen(PORT, () => {
    console.log(`graph-tutor GraphQL on http://localhost:${PORT}/graphql`);
    console.log(`graph: ${GRAPH_PATH} (${store.allNodes().length} nodes, ${store.allEdges().length} edges)`);
  });
}
