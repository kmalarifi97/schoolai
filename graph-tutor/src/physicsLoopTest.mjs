// End-to-end gap-closing loop on the Physics-2 graph, via a real MCP client.
// Scenario: student fails conservation of momentum AND kinetic energy AND their
// shared math foundation "vector" (passes mass, time). The graph should surface
// "vector" as the SHARED blocking root cause.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const c = new Client({ name: "physics-loop", version: "1.0.0" });
await c.connect(new StreamableHTTPClientTransport(new URL(process.env.MCP_URL || "http://localhost:4100/mcp")));
const call = async (n, a) => (await c.callTool({ name: n, arguments: a })).structuredContent;
const line = (s) => console.log("\n──────── " + s + " ────────");
const PASSED = ["mass", "time"], FAILED = ["conservation of momentum", "kinetic energy", "vector"];

console.log("tools:", (await c.listTools()).tools.map((t) => t.name).join(", "));

line("1) choose_gap_finding_quiz (target: conservation of momentum)");
const quiz = await call("choose_gap_finding_quiz", { target_skill_name: "conservation of momentum", max_questions: 5 });
console.log("next_action:", quiz.next_teacher_action, "| question source:", quiz.question_text_source);
console.log("assess:", quiz.skills_to_assess.map((s) => `${s.concept_name}(${s.role})`).join(" | "));

line("2) diagnose_blocking_prerequisites");
const diag = await call("diagnose_blocking_prerequisites", { passed: PASSED, failed: FAILED });
console.log("next_action:", diag.next_teacher_action);
console.log("student-facing:", diag.student_facing_summary);
console.log("shared_root_cause:", diag.shared_root_cause ? `${diag.shared_root_cause.concept_name} → [${diag.shared_root_cause.blocked_concepts.join(", ")}]` : "(none)");
for (const f of diag.failed_concepts) console.log(`  • ${f.failed_concept}: teach "${f.blocking_prerequisite}" first [${f.confidence}] chain: ${f.short_chain.join(" → ")}`);
const teachFirst = diag.shared_root_cause?.concept_name || diag.failed_concepts.find((f) => f.blocking_prerequisite)?.blocking_prerequisite;
console.log("→ teach first:", teachFirst, "| next tool:", diag.tool_to_call_next?.name);

line("3) plan_gap_closing_lesson (LLM scaffold)");
const plan = await call("plan_gap_closing_lesson", { root_cause_concept_name: teachFirst, blocked_concept_name: "conservation of momentum" });
console.log("next_action:", plan.next_teacher_action, "|", plan.implemented_by);
console.log("why first:", plan.why_this_first);

line("4) check_gap_closure (assistant judged 'closed')");
const chk = await call("check_gap_closure", { root_cause_concept_name: teachFirst, blocked_concept_name: "conservation of momentum", your_judgment: "closed" });
console.log("gap_status:", chk.gap_status, "→ next_action:", chk.next_teacher_action);

line("5) run_gap_closing_tutoring_step (orchestrator)");
const step = await call("run_gap_closing_tutoring_step", { session_state: { target_concept: "conservation of momentum", passed: PASSED, failed: FAILED } });
console.log("next_action:", step.next_teacher_action, "| graph_backed_step:", step.graph_backed_step);
console.log("message:", step.message_to_student);
console.log("diagnosis:", JSON.stringify(step.diagnosis));
console.log("→ next tool:", step.tool_to_call_next?.name, JSON.stringify(step.tool_to_call_next?.arguments || {}));

await c.close();
console.log("\nPHYSICS-2 gap-closing loop: OK");
