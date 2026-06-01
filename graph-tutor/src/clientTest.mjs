// End-to-end MCP test using the real SDK client (does the proper handshake,
// exactly like ChatGPT). Verifies: list tools, and the full
// MCP -> GraphQL -> graph diagnosis path. Run with both servers up.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const url = new URL(process.env.MCP_URL || "http://localhost:4100/mcp");
const client = new Client({ name: "graph-tutor-test", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(url));

const tools = await client.listTools();
console.log("tools:", tools.tools.map((t) => t.name).join(", "));

const res = await client.callTool({
  name: "diagnose_student_from_quiz",
  arguments: { passed: ["kinematics", "derivatives", "vectors"], failed: ["work_energy", "forces"] },
});
const sc = res.structuredContent;
console.log("\ntext:", res.content[0].text);
console.log("next_teacher_action:", sc.next_teacher_action);
for (const f of sc.failed)
  console.log(` - ${f.skill.name} => root: ${f.rootCause ? f.rootCause.name : "(probe)"}\n     ${f.recommendation}`);

await client.close();
console.log("\nMCP -> GraphQL -> graph: OK");
