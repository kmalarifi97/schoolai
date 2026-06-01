// End-to-end test on the REAL Junyi graph: auto-pick a skill that has a
// prerequisite chain, simulate a quiz (fail it + fail one deep prereq, pass the
// rest), call the MCP diagnose tool, and translate hashed ids back to names.
import { readFileSync } from "node:fs";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const g = JSON.parse(readFileSync(new URL("../graph/junyi.graph.json", import.meta.url), "utf8"));
const name = new Map(g.nodes.map((n) => [n.id, n.name]));
const prereqOf = new Map(g.nodes.map((n) => [n.id, []]));
for (const e of g.edges) prereqOf.get(e.target).push(e.source);

// pick the target with the most direct prerequisites (richest chain to diagnose)
const failed = [...prereqOf.entries()].sort((a, b) => b[1].length - a[1].length)[0][0];
const prereqs = prereqOf.get(failed);
const failDeepPrereq = prereqs[0];                 // also fail one prerequisite
const passed = prereqs.slice(1);                   // pass the others

console.log("simulated quiz:");
console.log("  FAILED:", name.get(failed));
console.log("  FAILED (a prerequisite):", name.get(failDeepPrereq));
console.log("  passed:", passed.slice(0, 4).map((id) => name.get(id)).join(" | "), passed.length > 4 ? `(+${passed.length - 4})` : "");

const client = new Client({ name: "junyi-real-test", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(new URL(process.env.MCP_URL || "http://localhost:4100/mcp")));
const res = await client.callTool({
  name: "diagnose_student_from_quiz",
  arguments: { passed, failed: [failed, failDeepPrereq] },
});
const sc = res.structuredContent;
console.log("\nMCP diagnosis:");
console.log("  next_teacher_action:", sc.next_teacher_action);
console.log("  summary:", sc.summary);
for (const f of sc.failed) {
  console.log(`  • ${name.get(f.skill.id) || f.skill.name}`);
  console.log(`      root cause: ${f.rootCause ? (name.get(f.rootCause.id) || f.rootCause.name) : "(probe untested)"}`);
}
await client.close();
console.log("\nREAL graph: MCP -> GraphQL -> diagnosis OK");
