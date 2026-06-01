// Tiny static server for the graph viewer. Serves the viewer HTML at / and the
// current graph JSON at /graph.json (GRAPH_PATH, default the built Junyi graph).
import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..");
const GRAPH_PATH = process.env.GRAPH_PATH || join(ROOT, "graph", "junyi.graph.json");
const PORT = Number(process.env.WEB_PORT || 4200);

createServer((req, res) => {
  const url = (req.url || "/").split("?")[0];
  try {
    if (url === "/" || url === "/index.html") {
      res.writeHead(200, { "content-type": "text/html; charset=utf-8" })
         .end(readFileSync(join(ROOT, "public", "graph-viewer.html")));
      return;
    }
    if (url === "/graph.json") {
      res.writeHead(200, { "content-type": "application/json; charset=utf-8" })
         .end(readFileSync(GRAPH_PATH));
      return;
    }
    res.writeHead(404, { "content-type": "text/plain" }).end("Not found");
  } catch (e) {
    res.writeHead(500, { "content-type": "text/plain" }).end(String(e?.message || e));
  }
}).listen(PORT, () => {
  console.log(`graph viewer  ->  http://localhost:${PORT}`);
  console.log(`serving graph: ${GRAPH_PATH}`);
});
