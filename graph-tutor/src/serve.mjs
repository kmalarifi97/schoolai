// Combined entrypoint for hosting (Cloud Run): one container, two listeners.
//   - GraphQL graph DB on internal localhost:4000 (not public)
//   - MCP server on the public $PORT (Cloud Run injects PORT, default 8080)
// The MCP tools call the GraphQL endpoint over localhost. Env is set BEFORE the
// modules are imported, because each reads its config at import time.

process.env.GRAPH_PATH = process.env.GRAPH_PATH || "graph/physics2.graph.json";
process.env.GRAPHQL_URL = "http://localhost:4000/graphql";
process.env.MCP_PORT = process.env.PORT || process.env.MCP_PORT || "8080";

const { httpServer: graphql } = await import("./graphqlServer.mjs");
await new Promise((resolve) => graphql.listen(4000, resolve));
console.log(`internal GraphQL on :4000  (graph: ${process.env.GRAPH_PATH})`);

// importing the MCP server starts it listening on MCP_PORT (= public $PORT)
await import("./mcpServer.mjs");
