// Gap-closing tutor — MCP server wired to the GraphQL graph DB.
//
// Mission: find the prerequisite blocking a failed skill, teach it first, verify
// it closed, then return to the failed skill. Built on ChatGPT's 5-tool design,
// corrected for what is actually graph-backed vs. LLM work:
//
//   GRAPH-BACKED (real GraphQL traversal):
//     • diagnose_blocking_prerequisites  -> diagnose(passed, failed) query
//     • choose_gap_finding_quiz          -> skill.prerequisites (which skills to assess)
//   LLM-DRIVEN (no DB query — thin self-guiding scaffolds, labeled as such):
//     • plan_gap_closing_lesson
//     • check_gap_closure
//   ORCHESTRATOR (only its diagnose branch hits the DB):
//     • run_gap_closing_tutoring_step   [preferred]
//
// Tools speak in CONCEPT NAMES. Internal skill IDs are resolved here and never
// exposed to the student. Graph is shallow-aware: focus on the single blocking
// prerequisite and shared root causes, not long remediation paths.

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
const out = (text, structured) => ({ content: [{ type: "text", text }], structuredContent: structured });

// ---- concept-name <-> internal-id resolution (IDs never leave this module) ----
async function nameMaps() {
  const d = await gql(`{ skills { id name } }`);
  const n2i = new Map(), i2n = new Map();
  for (const s of d.skills) { n2i.set(s.name.toLowerCase().trim(), s.id); i2n.set(s.id, s.name); }
  return { n2i, i2n, skills: d.skills };
}
function resolve(n2i, name) {
  if (!name) return null;
  const k = String(name).toLowerCase().trim();
  if (n2i.has(k)) return n2i.get(k);                              // exact
  for (const [nm, id] of n2i) if (nm.startsWith(k) || k.startsWith(nm)) return id; // prefix
  for (const [nm, id] of n2i) if (nm.includes(k) || k.includes(nm)) return id;     // contains
  return null;
}

// ---- the one real diagnosis query, reshaped into concept-name space ----
async function diagnoseByName(passedNames, failedNames) {
  const { n2i, i2n } = await nameMaps();
  const toId = (arr) => (arr || []).map((n) => ({ name: n, id: resolve(n2i, n) }));
  const passed = toId(passedNames), failed = toId(failedNames);
  const unresolved = [...passed, ...failed].filter((x) => !x.id).map((x) => x.name);
  const d = await gql(
    `query($p:[ID!]!,$f:[ID!]!){ diagnose(passed:$p, failed:$f){
        summary
        failed { skill{id name} rootCause{id name} recommendation
                 chain { skill{id name} status depth } } } }`,
    { p: passed.filter((x) => x.id).map((x) => x.id), f: failed.filter((x) => x.id).map((x) => x.id) }
  );
  // reshape: per failed concept + detect a SHARED root cause across failures
  const perFailed = d.diagnose.failed.map((f) => ({
    failed_concept: f.skill.name,
    blocking_prerequisite: f.rootCause ? f.rootCause.name : null,
    why_teach_this_first: f.rootCause
      ? `The failure in "${f.skill.name}" traces back to "${f.rootCause.name}", a prerequisite the student also missed — teach it first.`
      : `"${f.skill.name}" has no confirmed unmet prerequisite yet — its prerequisites were not tested.`,
    short_chain: f.rootCause ? [f.rootCause.name, f.skill.name] : [f.skill.name],
    confidence: f.rootCause ? "high" : "low",
  }));
  const counts = new Map();
  for (const f of perFailed) if (f.blocking_prerequisite) {
    if (!counts.has(f.blocking_prerequisite)) counts.set(f.blocking_prerequisite, []);
    counts.get(f.blocking_prerequisite).push(f.failed_concept);
  }
  let shared = null;
  for (const [pre, blocked] of counts) if (blocked.length >= 2 && (!shared || blocked.length > shared.blocked_concepts.length))
    shared = { concept_name: pre, blocked_concepts: blocked,
      why_it_blocks_learning: `Several failed concepts (${blocked.join(", ")}) all rest on "${pre}". Fixing this one foundation unblocks all of them.`,
      recommended_first_teaching_focus: pre };
  return { perFailed, shared, unresolved, summary: d.diagnose.summary };
}

function createServer_() {
  const server = new McpServer({ name: "graph-tutor-gap-closing", version: "0.2.0" });

  // ========== 1. diagnose_blocking_prerequisites  (REAL graph tool) ==========
  server.registerTool(
    "diagnose_blocking_prerequisites",
    {
      title: "Diagnose the prerequisite blocking the student's failed skills",
      description:
        "GRAPH-BACKED. Use this once the student has answered diagnostic questions and you know which " +
        "concepts they PASSED and which they FAILED. It walks the prerequisite graph backward from each " +
        "failed concept and returns the unmet prerequisite to teach first (the root cause), preferring a " +
        "prerequisite the student actually failed over one never tested. It also surfaces a SHARED root " +
        "cause when several failures collapse to one missing foundation.\n" +
        "Do NOT call before you have pass/fail evidence. Speak to the student only in concept names — never " +
        "reveal IDs, graph edges, or probabilities. Explain results as 'teach X first, because your error " +
        "traces back to it.'",
      inputSchema: {
        passed: z.array(z.string()).optional().describe("Concept names the student got right"),
        failed: z.array(z.string()).optional().describe("Concept names the student got wrong"),
      },
      outputSchema: {
        next_teacher_action: z.string(), student_facing_summary: z.string(), diagnosis_summary: z.string(),
        shared_root_cause: z.any().nullable(), failed_concepts: z.any(), unresolved_concepts: z.any(),
        tool_to_call_next: z.any(),
      },
    },
    async ({ passed, failed }) => {
      const r = await diagnoseByName(passed, failed);
      const action = r.shared ? "teach_shared_root_cause"
        : r.perFailed.some((f) => f.blocking_prerequisite) ? "teach_single_root_cause"
        : "ask_more_diagnostic_questions";
      const teachFirst = r.shared ? r.shared.concept_name
        : r.perFailed.find((f) => f.blocking_prerequisite)?.blocking_prerequisite;
      const sf = r.shared
        ? `أكثر من خطأ يرجع إلى أساس واحد: «${r.shared.concept_name}». نبدأ منه أولًا.`
        : teachFirst ? `نقطة البداية المناسبة هي «${teachFirst}» قبل العودة لما أخطأت فيه.`
        : "نحتاج أسئلة إضافية لنحدّد بالضبط أين الفجوة.";
      const o = {
        next_teacher_action: action, student_facing_summary: sf,
        diagnosis_summary: r.summary, shared_root_cause: r.shared, failed_concepts: r.perFailed,
        unresolved_concepts: r.unresolved,
        tool_to_call_next: teachFirst
          ? { name: "plan_gap_closing_lesson", arguments: { root_cause_concept_name: teachFirst } }
          : { name: "choose_gap_finding_quiz", reason: "not enough evidence yet" },
      };
      return out(sf, o);
    }
  );

  // ========== 2. choose_gap_finding_quiz  (graph supplies WHICH skills) ==========
  server.registerTool(
    "choose_gap_finding_quiz",
    {
      title: "Choose which skills to quiz to find the blocking gap",
      description:
        "GRAPH-BACKED for skill SELECTION (question text is LLM-generated). Use this when a student asks for " +
        "help with a topic, fails a problem, says they're confused, or asks 'where do I start?'. Given a " +
        "target concept, it returns that concept PLUS its prerequisites — the set of skills to assess so you " +
        "can locate the missing foundation. You write the actual questions (one per skill) and ask them " +
        "naturally; the graph only decides WHAT to test. After the student answers, judge pass/fail per " +
        "concept and call diagnose_blocking_prerequisites.\n" +
        "Do NOT use if the student explicitly wants a specific lesson with no diagnosis. Never show IDs.",
      inputSchema: {
        target_skill_name: z.string().describe("The concept the student wants help with"),
        max_questions: z.number().optional().describe("Cap on skills to assess (default 5)"),
      },
      outputSchema: {
        next_teacher_action: z.string(), student_facing_intro: z.string(), quiz_focus: z.any(),
        skills_to_assess: z.any(), question_text_source: z.string(), after_student_answers: z.any(),
      },
    },
    async ({ target_skill_name, max_questions }) => {
      const { n2i, i2n } = await nameMaps();
      const id = resolve(n2i, target_skill_name);
      if (!id) return out(`لم أجد المفهوم «${target_skill_name}» في الخريطة.`,
        { next_teacher_action: "ask_clarifying_question", student_facing_intro: "", quiz_focus: null,
          skills_to_assess: [], question_text_source: "none", after_student_answers: null });
      const d = await gql(`query($id:ID!){ skill(id:$id){ name prerequisites(recursive:true){ id name } } }`, { id });
      const cap = max_questions || 5;
      // assess the target first, then its nearest prerequisites
      const pre = d.skill.prerequisites.slice(0, Math.max(0, cap - 1));
      const skills = [{ concept_name: d.skill.name, role: "target" },
        ...pre.map((p) => ({ concept_name: p.name, role: "prerequisite" }))];
      const o = {
        next_teacher_action: "ask_diagnostic_questions",
        student_facing_intro: "خلنا نبدأ بأسئلة قصيرة عشان أعرف وين بالضبط النقطة اللي نحتاج نقويها.",
        quiz_focus: { target_concept: d.skill.name,
          why_this_quiz: `"${d.skill.name}" depends on ${pre.length} earlier skill(s); testing them locates the gap.` },
        skills_to_assess: skills,
        question_text_source: "llm_generated",  // NOTE: no question bank on this graph — you write the questions
        after_student_answers: { tool_to_call_next: "diagnose_blocking_prerequisites",
          pass_fail_format: { passed: ["concept names"], failed: ["concept names"] } },
      };
      return out(`Assess these concepts: ${skills.map((s) => s.concept_name).join(", ")}`, o);
    }
  );

  // ========== 3. plan_gap_closing_lesson  (LLM-driven — NOT a DB query) ==========
  server.registerTool(
    "plan_gap_closing_lesson",
    {
      title: "Plan a short lesson that closes the root-cause gap",
      description:
        "LLM-DRIVEN (no graph query). Use this after diagnose_blocking_prerequisites names a root-cause " +
        "prerequisite. It returns a self-guiding scaffold: teach the prerequisite first with a short micro-" +
        "lesson and a check question, then bridge back to the originally failed concept. YOU write the actual " +
        "explanation; this tool only structures the teaching move and names the next action.\n" +
        "Do NOT produce a full chapter summary, and do NOT jump to the failed skill before teaching the " +
        "prerequisite. Keep it short and focused on unblocking.",
      inputSchema: {
        root_cause_concept_name: z.string(),
        blocked_concept_name: z.string().optional(),
        student_goal: z.string().optional(),
      },
      outputSchema: {
        next_teacher_action: z.string(), implemented_by: z.string(), why_this_first: z.string(),
        micro_lesson: z.any(), bridge_back_to_failed_skill: z.any(), tool_to_call_next: z.any(),
      },
    },
    async ({ root_cause_concept_name, blocked_concept_name }) => {
      const o = {
        next_teacher_action: "teach_root_cause_first",
        implemented_by: "assistant (LLM) — this tool does not query the graph; it scaffolds your teaching",
        why_this_first: blocked_concept_name
          ? `"${blocked_concept_name}" depends on "${root_cause_concept_name}"; closing the prerequisite unblocks it.`
          : `Teach "${root_cause_concept_name}" first as the missing foundation.`,
        micro_lesson: {
          concept_to_teach: root_cause_concept_name,
          teaching_goal: `Student can use "${root_cause_concept_name}" correctly in one simple case.`,
          steps: [{ step_title: "Intuition first", teacher_explanation: "(you write: one concrete idea, no jargon)",
            check_question: "(you write: one short question that proves understanding)",
            expected_understanding: "(what a correct answer shows)" }],
        },
        bridge_back_to_failed_skill: blocked_concept_name
          ? { blocked_concept: blocked_concept_name,
              bridge_explanation: `Once the check passes, connect "${root_cause_concept_name}" back to "${blocked_concept_name}".`,
              when_to_bridge: "after the student answers the check question correctly" }
          : null,
        tool_to_call_next: { name: "check_gap_closure", when: "after teaching and asking the check question" },
      };
      return out(`Teach "${root_cause_concept_name}" first, then bridge back.`, o);
    }
  );

  // ========== 4. check_gap_closure  (LLM-driven — NOT a DB query) ==========
  server.registerTool(
    "check_gap_closure",
    {
      title: "Decide whether the prerequisite gap is now closed",
      description:
        "LLM-DRIVEN (no graph query). Use this after you taught the root-cause prerequisite and the student " +
        "answered a check question. YOU judge the answer (there is no answer key); this tool structures the " +
        "decision and names the next action: return to the originally failed skill if closed, reteach more " +
        "simply if still open, or ask another check. Do NOT mark the gap closed just because you explained " +
        "it — the student must demonstrate it.",
      inputSchema: {
        root_cause_concept_name: z.string(), blocked_concept_name: z.string().optional(),
        student_answer: z.string().optional(), expected_understanding: z.string().optional(),
        your_judgment: z.enum(["closed", "still_open", "uncertain"]).optional()
          .describe("Your assessment of the student's answer; drives the returned next action"),
      },
      outputSchema: {
        next_teacher_action: z.string(), implemented_by: z.string(), gap_status: z.string(),
        if_closed: z.any(), if_still_open: z.any(), tool_to_call_next: z.any(),
      },
    },
    async ({ root_cause_concept_name, blocked_concept_name, your_judgment }) => {
      const status = your_judgment || "uncertain";
      const action = status === "closed" ? "return_to_blocked_skill"
        : status === "still_open" ? "reteach_root_cause" : "ask_another_check";
      const o = {
        next_teacher_action: action,
        implemented_by: "assistant (LLM) judges correctness — this tool does not grade",
        gap_status: status,
        if_closed: status === "closed" && blocked_concept_name
          ? { bridge_to_blocked_skill: `Reconnect "${root_cause_concept_name}" to "${blocked_concept_name}" and resume it.` }
          : null,
        if_still_open: status === "still_open"
          ? { reteach_focus: root_cause_concept_name, hint: "Use a simpler, more concrete example, then re-check." }
          : null,
        tool_to_call_next: status === "closed"
          ? { name: "run_gap_closing_tutoring_step", when: "to resume the originally failed skill" }
          : { name: "plan_gap_closing_lesson", when: "to reteach the prerequisite" },
      };
      return out(`Gap status: ${status} -> ${action}`, o);
    }
  );

  // ========== 5. run_gap_closing_tutoring_step  (orchestrator — preferred) ==========
  server.registerTool(
    "run_gap_closing_tutoring_step",
    {
      title: "Run one step of the gap-closing tutoring loop (preferred)",
      description:
        "PREFERRED tool for a tutoring session. It drives one step of the loop and tells you exactly what to " +
        "do next: pick which skills to quiz, diagnose the blocking prerequisite (the only step that queries " +
        "the graph), plan the root-cause lesson, check closure, or return to the failed skill. Pass the " +
        "running session_state back each call. Always follow next_teacher_action. Never expose IDs, graph " +
        "internals, probabilities, or tool names to the student; speak in concept names.\n" +
        "Do NOT use if the student refuses diagnosis and only wants a direct explanation.",
      inputSchema: {
        student_message: z.string().optional(),
        session_state: z.object({
          student_goal: z.string().optional(), target_concept: z.string().optional(),
          passed: z.array(z.string()).optional(), failed: z.array(z.string()).optional(),
          current_root_cause: z.string().optional(), current_blocked_concept: z.string().optional(),
          last_student_answer: z.string().optional(), gap_judgment: z.enum(["closed", "still_open", "uncertain"]).optional(),
        }).optional(),
      },
      outputSchema: {
        next_teacher_action: z.string(), message_to_student: z.string(), why_this_action: z.string(),
        graph_backed_step: z.boolean(), skills_to_assess: z.any(), diagnosis: z.any(),
        teaching_plan: z.any(), updated_session_state: z.any(), tool_to_call_next: z.any(),
      },
    },
    async ({ student_message, session_state }) => {
      const s = session_state || {};
      const passed = s.passed || [], failed = s.failed || [];
      const base = { skills_to_assess: null, diagnosis: null, teaching_plan: null, graph_backed_step: false,
        updated_session_state: { ...s, passed, failed } };

      // (a) closure judged closed -> return to failed skill  [LLM step]
      if (s.current_root_cause && s.gap_judgment === "closed") {
        const blocked = s.current_blocked_concept;
        return out("نرجع الآن للمهارة الأساسية.", { ...base,
          next_teacher_action: "return_to_blocked_skill",
          message_to_student: blocked ? `ممتاز، ثبّتنا الأساس. نرجع الآن إلى «${blocked}».` : "ممتاز، نكمل.",
          why_this_action: "Prerequisite gap closed; resume the originally failed concept.",
          updated_session_state: { ...s, current_root_cause: undefined, current_blocked_concept: undefined },
          tool_to_call_next: null });
      }
      // (b) prerequisite taught + answer given -> check closure  [LLM step]
      if (s.current_root_cause && s.last_student_answer) {
        return out("نقيّم إجابة الطالب على الأساس.", { ...base,
          next_teacher_action: "check_gap_closure",
          message_to_student: "", why_this_action: "Student answered the check question; judge if the gap is closed.",
          tool_to_call_next: { name: "check_gap_closure", arguments: { root_cause_concept_name: s.current_root_cause,
            blocked_concept_name: s.current_blocked_concept, student_answer: s.last_student_answer } } });
      }
      // (c) have evidence, no root cause yet -> DIAGNOSE  [GRAPH step]
      if (failed.length) {
        const r = await diagnoseByName(passed, failed);
        const teachFirst = r.shared ? r.shared.concept_name
          : r.perFailed.find((f) => f.blocking_prerequisite)?.blocking_prerequisite;
        if (teachFirst) {
          const blocked = r.shared ? r.shared.blocked_concepts[0] : r.perFailed.find((f) => f.blocking_prerequisite)?.failed_concept;
          return out(`نبدأ من «${teachFirst}».`, { ...base, graph_backed_step: true,
            next_teacher_action: "teach_root_cause",
            message_to_student: `نقطة البداية المناسبة هي «${teachFirst}» قبل العودة إلى «${blocked}».`,
            why_this_action: "Failure traces back to this prerequisite in the graph.",
            diagnosis: { root_cause_concept: teachFirst, blocked_concepts: r.shared ? r.shared.blocked_concepts : [blocked],
              shared: !!r.shared },
            updated_session_state: { ...s, passed, failed, current_root_cause: teachFirst, current_blocked_concept: blocked },
            tool_to_call_next: { name: "plan_gap_closing_lesson", arguments: { root_cause_concept_name: teachFirst, blocked_concept_name: blocked } } });
        }
        // diagnosed but no confirmed prereq -> need more questions
        return out("نحتاج أسئلة إضافية.", { ...base, graph_backed_step: true,
          next_teacher_action: "ask_more_diagnostic_questions",
          message_to_student: "نحتاج سؤالًا أو سؤالين إضافيين لتحديد الأساس الناقص.",
          why_this_action: "Failed skill's prerequisites were not tested; gather more evidence.",
          tool_to_call_next: { name: "choose_gap_finding_quiz", arguments: { target_skill_name: failed[0] } } });
      }
      // (d) no evidence yet -> choose a quiz around the target  [GRAPH step: which skills]
      if (s.target_concept) {
        const { n2i } = await nameMaps();
        const id = resolve(n2i, s.target_concept);
        if (id) {
          const d = await gql(`query($id:ID!){ skill(id:$id){ name prerequisites(recursive:true){ name } } }`, { id });
          const skills = [{ concept_name: d.skill.name, role: "target" },
            ...d.skill.prerequisites.slice(0, 4).map((p) => ({ concept_name: p.name, role: "prerequisite" }))];
          return out("نبدأ بأسئلة تشخيصية قصيرة.", { ...base, graph_backed_step: true,
            next_teacher_action: "ask_diagnostic_question",
            message_to_student: "خلنا نبدأ بأسئلة قصيرة أعرف منها نقطة انطلاقك.",
            why_this_action: "Locate the gap by testing the target and its prerequisites.",
            skills_to_assess: skills,
            tool_to_call_next: { name: "diagnose_blocking_prerequisites", when: "after the student answers" } });
        }
      }
      // (e) nothing to go on -> clarify
      return out("نحتاج تحديد الموضوع.", { ...base,
        next_teacher_action: "ask_clarifying_question",
        message_to_student: "أي موضوع أو مهارة تحب نركّز عليها؟",
        why_this_action: "No target concept or evidence yet." , tool_to_call_next: null });
    }
  );

  return server;
}

const httpServer = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  res.setHeader("Access-Control-Allow-Origin", "*");
  if (req.method === "OPTIONS" && url.pathname === MCP_PATH)
    return res.writeHead(204, { "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id", "Access-Control-Expose-Headers": "Mcp-Session-Id" }).end();
  if (req.method === "GET" && url.pathname === "/")
    return res.writeHead(200, { "content-type": "text/plain" }).end(`graph-tutor gap-closing MCP. POST ${MCP_PATH}\nGraphQL: ${GRAPHQL_URL}`);
  if (url.pathname === MCP_PATH && (req.method === "GET" || req.method === "DELETE"))
    return res.writeHead(405, { allow: "POST", "content-type": "text/plain" }).end("Method Not Allowed; use POST");
  if (url.pathname === MCP_PATH && req.method === "POST") {
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");
    const server = createServer_();
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

httpServer.listen(PORT, () => {
  console.log(`graph-tutor gap-closing MCP on http://localhost:${PORT}${MCP_PATH}`);
  console.log(`-> GraphQL backend: ${GRAPHQL_URL}`);
});
