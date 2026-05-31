// MCP server for the Physics 2 ChatGPT App (Apps SDK).
//
// Read tools (text the model reasons over):
//   get_toc()                 ordered chapters -> lessons (for "first lesson", browsing)
//   get_lesson(lesson)        full lesson: summary, objectives, key terms, pages, concepts
//   get_concept(concept)      concept detail incl. the intuition narration beats
//   find_concept(query)       keyword search
//   list_projects()           homework-story projects
//   get_project(project)      project detail incl. beats
//   read_lesson_pages(lesson) full per-page textbook content (vision-once JSON)
//   find_question(lesson,...)  resolve "سؤال 8 صفحة 17" to the exact question
// Diagnostic tutoring tools (KST — teach the student's gap, not ToC order):
//   run_diagnostic_tutoring_step(...)        PREFERRED: drives the whole loop
//   choose_next_diagnostic_question(resp)    pick the next question (asked inline)
//   grade_diagnostic_answer(item,answer)     grading context (assistant judges)
//   diagnose_student_gap_from_answers(resp)  locate the gap -> lesson to teach
// Show tools (in-chat widgets):
//   show_prerequisite_video(lesson) lesson's foundation/teaser video (kind:foundation)
//   show_concept_video(concept)   concept intuition video player
//   show_project_video(project)   project (homework story) video player
//
// Videos live in one public bucket (PUBLIC_VIDEO_BASE):
//   concept video : <base>/<slug>.mp4
//   project video : <base>/projects/<slug>.mp4

import { createServer } from "node:http";
import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";

import { createDiagnostics } from "./kst.js";

const HERE = dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT ?? 8787);
const MCP_PATH = "/mcp";
const VIDEO_WIDGET = "ui://widget/concept-video.html";

const BASE = (process.env.PUBLIC_VIDEO_BASE || "").replace(/\/+$/, "");
const conceptVideoUrl = (slug) => (BASE ? `${BASE}/${slug}.mp4` : null);
const projectVideoUrl = (slug) => (BASE ? `${BASE}/projects/${slug}.mp4` : null);

const videoHtml = readFileSync(join(HERE, "public", "video-widget.html"), "utf8");
const LIB = JSON.parse(readFileSync(join(HERE, "data", "library.json"), "utf8"));

// Server-level guidance (the teaching persona + lesson flow) sent to the client
// in the initialize handshake — the connector-native stand-in for a system prompt.
const INSTRUCTIONS = readFileSync(join(HERE, "instructions.md"), "utf8");

// Extracted per-page lesson content (vision-once). lesson_id -> lesson object.
const lessonPages = {};
const LP_DIR = join(HERE, "data", "lesson_pages");
for (const f of readdirSync(LP_DIR)) {
  if (!f.endsWith(".json") || f === "lesson_pages.schema.json" || f.includes(".reference.")) continue;
  try {
    const d = JSON.parse(readFileSync(join(LP_DIR, f), "utf8"));
    if (d.lesson_id) lessonPages[d.lesson_id] = d;
  } catch (e) {
    console.error(`skip ${f}: ${e.message}`);
  }
}

const concepts = LIB.concepts; // { slug: {...} }
const conceptList = Object.values(concepts);

// KST diagnostic engine (JS port of spine/kst.py). Reads the bundled spine data
// (data/spine/*.jsonl + concepts.json). Loaded once; gracefully disabled if the
// spine data is absent so the rest of the tutor still works.
let diagnostics = null;
try {
  diagnostics = createDiagnostics({ spineDir: join(HERE, "data", "spine") });
  console.log(`KST diagnostics ready: ${diagnostics._struct.states.length} knowledge states`);
} catch (e) {
  console.error(`KST diagnostics disabled: ${e.message}`);
}
const projects = LIB.projects;
const projectBySlug = new Map(projects.map((p) => [p.slug, p]));

// lesson id -> { ...lesson, chapter_id, chapter_title_ar }
const lessonById = new Map();
for (const ch of LIB.chapters) {
  for (const ls of ch.lessons) {
    lessonById.set(ls.id, { ...ls, chapter_id: ch.id, chapter_title_ar: ch.title_ar });
  }
}

// slug -> Arabic concept name (for student-facing diagnosis messages).
const conceptArBySlug = new Map();
for (const ch of LIB.chapters)
  for (const ls of ch.lessons)
    for (const c of ls.concepts || [])
      if (c.slug && (c.ar || c.concept_ar)) conceptArBySlug.set(c.slug, c.ar || c.concept_ar);

// item_id -> the full question (so diagnostic tools can return the prompt inline,
// no follow-up find_question needed) + lesson misconceptions for grading feedback.
const questionById = new Map();
const misconceptionsByLesson = new Map();
function collectQuestions(node, out) {
  if (Array.isArray(node)) { for (const x of node) collectQuestions(x, out); return; }
  if (node && typeof node === "object") {
    if (node.type === "question" || node.qkind) out.push(node);
    for (const v of Object.values(node)) collectQuestions(v, out);
  }
}
for (const [lid, lp] of Object.entries(lessonPages)) {
  if (Array.isArray(lp.common_misconceptions_ar)) misconceptionsByLesson.set(lid, lp.common_misconceptions_ar);
  const acc = [];
  collectQuestions(lp.pages, acc);
  for (const q of acc) if (q.id) questionById.set(q.id, { ...q, lesson: lid });
}

// Build the inline question payload the model asks the student verbatim.
function questionPayload(itemId) {
  const q = questionById.get(itemId);
  if (!q) return { item_id: itemId };
  return {
    item_id: itemId, lesson: q.lesson, page: q.page, printed_number: q.printed_number,
    qkind: q.qkind, prompt_ar: q.prompt_ar,
    options_ar: q.options_ar || null, given_ar: q.given_ar || null,
  };
}
const conceptName = (slug, en) => conceptArBySlug.get(slug) || en || slug;

const lc = (s) => (s || "").toString().toLowerCase();

function resolveConcept(q) {
  const query = lc(q).trim();
  if (!query) return null;
  if (concepts[query]) return concepts[query];
  return (
    conceptList.find(
      (c) =>
        lc(c.slug).includes(query) ||
        lc(c.concept_ar).includes(query) ||
        lc(c.concept_en).includes(query) ||
        lc(c.lesson_title_ar).includes(query)
    ) || null
  );
}

function resolveProject(q) {
  const query = lc(q).trim();
  if (!query) return null;
  if (projectBySlug.has(query)) return projectBySlug.get(query);
  return (
    projects.find(
      (p) =>
        lc(p.slug).includes(query) ||
        lc(p.project_ar).includes(query) ||
        lc(p.project_en).includes(query)
    ) || null
  );
}

function conceptWidgetPayload(c) {
  const url = c.has_video ? conceptVideoUrl(c.slug) : null;
  return {
    slug: c.slug,
    concept_ar: c.concept_ar,
    concept_en: c.concept_en,
    chapter_title_ar: c.chapter_title_ar,
    lesson_title_ar: c.lesson_title_ar,
    pages: c.pages,
    phet: c.phet || null,
    video_url: url,
    message: url ? null : "فيديو هذا المفهوم قيد الإعداد.",
  };
}

function projectWidgetPayload(p) {
  const url = p.has_video ? projectVideoUrl(p.slug) : null;
  return {
    slug: p.slug,
    concept_ar: p.project_ar,
    concept_en: p.project_en,
    chapter_title_ar: "",
    lesson_title_ar: p.persona || "",
    pages: "",
    phet: p.phet || null,
    video_url: url,
    message: url ? null : "فيديو هذا المشروع قيد الإعداد.",
  };
}

// Tools that declare an outputSchema must return structuredContent on every
// path (including not-found), so pass a schema-shaped object as the 2nd arg.
const text = (t, structured) =>
  structured
    ? { content: [{ type: "text", text: t }], structuredContent: structured }
    : { content: [{ type: "text", text: t }] };

function createPhysicsServer() {
  const server = new McpServer(
    { name: "physics2-tutor", version: "0.3.0" },
    { instructions: INSTRUCTIONS }
  );

  // ---- UI resources ----
  registerAppResource(server, "concept-video", VIDEO_WIDGET, {}, async () => ({
    contents: [{ uri: VIDEO_WIDGET, mimeType: RESOURCE_MIME_TYPE, text: videoHtml }],
  }));

  // ---- get_toc ----
  registerAppTool(
    server,
    "get_toc",
    {
      title: "Get the Physics 2 table of contents",
      description:
        "Return the ordered curriculum: chapters → lessons (with id, titles, " +
        "page range, and concept slugs). ALWAYS resolve lesson order here for " +
        "requests like 'the first lesson', 'next lesson', or 'chapter 2'. The " +
        "first lesson is chapters[0].lessons[0] (1-1). Each lesson has an " +
        "`available` flag (and `available_lessons` lists the ready ones); only " +
        "those can actually be taught from the book now. Never start a different " +
        "lesson unless the student explicitly asks, and never jump to a concept " +
        "just because it has a video.",
      inputSchema: {},
      outputSchema: {
        book: z.object({ title_ar: z.string(), pages: z.number() }),
        available_lessons: z.array(z.string()),
        chapters: z.array(z.any()),
      },
      _meta: {},
    },
    async () => {
      const toc = LIB.chapters.map((ch) => ({
        chapter: ch.id,
        title_ar: ch.title_ar,
        title_en: ch.title_en,
        pages: `${ch.start_page}-${ch.end_page}`,
        lessons: ch.lessons.map((ls) => ({
          lesson: ls.id,
          title_ar: ls.title_ar,
          pages: `${ls.start_page}-${ls.end_page}`,
          concepts: ls.concepts.map((c) => c.slug),
          // available = its textbook content is extracted and teachable now
          available: !!lessonPages[ls.id],
        })),
      }));
      const available = toc.flatMap((ch) => ch.lessons.filter((l) => l.available).map((l) => l.lesson));
      const lines = toc.flatMap((ch) => [
        `الفصل ${ch.chapter}: ${ch.title_ar} (ص ${ch.pages})`,
        ...ch.lessons.map(
          (l) => `  • الدرس ${l.lesson}: ${l.title_ar} (ص ${l.pages})${l.available ? " ✅ متوفر" : " (قيد الإعداد)"}`
        ),
      ]);
      lines.push("", `الدروس المتوفرة للدراسة الآن: ${available.join("، ") || "(لا يوجد بعد)"}`);
      return {
        content: [{ type: "text", text: lines.join("\n") }],
        structuredContent: {
          book: { title_ar: LIB.book.title_ar, pages: LIB.book.pages },
          available_lessons: available,
          chapters: toc,
        },
      };
    }
  );

  // ---- get_lesson ----
  registerAppTool(
    server,
    "get_lesson",
    {
      title: "Get a lesson's content",
      description:
        "Full content for one lesson by its id (e.g. '1-1'): Arabic summary, " +
        "learning objectives, key terms, book page range, and the concepts it " +
        "covers. Use this when the student wants to study a specific lesson.",
      inputSchema: { lesson: z.string().min(1).describe("Lesson id, e.g. '1-1'") },
      outputSchema: { lesson: z.any() },
      _meta: {},
    },
    async ({ lesson }) => {
      const ls = lessonById.get(lesson.trim());
      if (!ls) return text(`لا يوجد درس بالمعرّف "${lesson}". استخدم get_toc لرؤية الدروس.`, { lesson: null });
      const lines = [
        `الدرس ${ls.id}: ${ls.title_ar} (${ls.title_en})`,
        `الفصل ${ls.chapter_id}: ${ls.chapter_title_ar} — صفحات ${ls.start_page}-${ls.end_page}`,
        "",
        ls.summary,
        "",
        ls.objectives.length ? "الأهداف:\n" + ls.objectives.map((o) => `- ${o}`).join("\n") : "",
        ls.key_terms.length ? "المصطلحات:\n" + ls.key_terms.map((t) => `- ${t}`).join("\n") : "",
        ls.concepts.length ? "المفاهيم: " + ls.concepts.map((c) => `${c.concept_ar} (${c.slug})`).join("، ") : "",
      ].filter(Boolean);
      return { content: [{ type: "text", text: lines.join("\n") }], structuredContent: { lesson: ls } };
    }
  );

  // ---- get_concept ----
  registerAppTool(
    server,
    "get_concept",
    {
      title: "Get a concept (with its intuition script)",
      description:
        "Detail for one concept by slug or name: Arabic/English names, its " +
        "lesson and book pages, the PhET simulation link, video availability, " +
        "and the full intuition narration 'beats'. Use the beats to explain in " +
        "the same intuition-first spirit — these stop before the algebra; guide " +
        "the student to solve problems themselves, do not solve for them.",
      inputSchema: { concept: z.string().min(1).describe("Concept slug or Arabic/English name") },
      outputSchema: { concept: z.any() },
      _meta: {},
    },
    async ({ concept }) => {
      const c = resolveConcept(concept);
      if (!c) return text(`لم أجد مفهومًا باسم "${concept}".`, { concept: null });
      const lines = [
        `${c.concept_ar} (${c.concept_en}) — slug: ${c.slug}`,
        `الفصل ${c.chapter}: ${c.chapter_title_ar} · الدرس ${c.lesson}: ${c.lesson_title_ar} · صفحات ${c.pages}`,
        c.has_video ? "يتوفر فيديو حدسي." : "الفيديو قيد الإعداد.",
        c.phet ? `محاكاة PhET: ${c.phet}` : "",
        "",
        c.beats.length ? "نص الحدس:\n" + c.beats.map((b) => `• ${b}`).join("\n") : "",
      ].filter(Boolean);
      return { content: [{ type: "text", text: lines.join("\n") }], structuredContent: { concept: c } };
    }
  );

  // ---- find_concept ----
  registerAppTool(
    server,
    "find_concept",
    {
      title: "Search concepts by keyword",
      description:
        "Search the concept library by an Arabic or English keyword. Returns " +
        "matching concepts (slug, names, lesson, video flag). For browsing the " +
        "whole course or ordinal lessons, prefer get_toc.",
      inputSchema: { query: z.string().min(1).describe("Arabic or English keyword") },
      outputSchema: { concepts: z.array(z.any()) },
      _meta: {},
    },
    async ({ query }) => {
      const q = lc(query).trim();
      const hits = conceptList
        .filter(
          (c) =>
            lc(c.slug).includes(q) ||
            lc(c.concept_ar).includes(q) ||
            lc(c.concept_en).includes(q) ||
            lc(c.lesson_title_ar).includes(q)
        )
        .map((c) => ({
          slug: c.slug, concept_ar: c.concept_ar, concept_en: c.concept_en,
          lesson: c.lesson, lesson_title_ar: c.lesson_title_ar, has_video: c.has_video,
        }));
      const t = hits.length
        ? hits.map((c) => `• ${c.concept_ar} (${c.concept_en}) — slug: ${c.slug}`).join("\n")
        : `لا توجد مفاهيم مطابقة لـ "${query}".`;
      return { content: [{ type: "text", text: t }], structuredContent: { concepts: hits } };
    }
  );

  // ---- list_projects ----
  registerAppTool(
    server,
    "list_projects",
    {
      title: "List homework-story projects",
      description:
        "Return the applied homework-story projects, each combining several " +
        "concepts around a PhET simulation (slug, Arabic/English title, persona, " +
        "combined concepts, video flag).",
      inputSchema: {},
      outputSchema: { projects: z.array(z.any()) },
      _meta: {},
    },
    async () => {
      const list = projects.map((p) => ({
        slug: p.slug, project_ar: p.project_ar, project_en: p.project_en,
        persona: p.persona, concepts_combined: p.concepts_combined, has_video: p.has_video,
      }));
      const t = list.map((p) => `• ${p.project_ar} — slug: ${p.slug}`).join("\n");
      return { content: [{ type: "text", text: t }], structuredContent: { projects: list } };
    }
  );

  // ---- get_project ----
  registerAppTool(
    server,
    "get_project",
    {
      title: "Get a project (with its story beats)",
      description:
        "Detail for one homework-story project by slug or name: title, persona, " +
        "PhET simulation, the concepts it combines, video availability, and the " +
        "full story narration beats.",
      inputSchema: { project: z.string().min(1).describe("Project slug or name") },
      outputSchema: { project: z.any() },
      _meta: {},
    },
    async ({ project }) => {
      const p = resolveProject(project);
      if (!p) return text(`لم أجد مشروعًا باسم "${project}".`, { project: null });
      const lines = [
        `${p.project_ar} (${p.project_en}) — slug: ${p.slug}`,
        p.persona ? `الشخصية: ${p.persona}` : "",
        p.phet ? `محاكاة PhET: ${p.phet}` : "",
        p.concepts_combined.length ? `يجمع المفاهيم: ${p.concepts_combined.join("، ")}` : "",
        p.has_video ? "يتوفر فيديو." : "الفيديو قيد الإعداد.",
        "",
        p.beats.length ? "القصة:\n" + p.beats.map((b) => `• ${b}`).join("\n") : "",
      ].filter(Boolean);
      return { content: [{ type: "text", text: lines.join("\n") }], structuredContent: { project: p } };
    }
  );

  // ---- show_concept_video ----
  registerAppTool(
    server,
    "show_concept_video",
    {
      title: "Show a concept's intuition video",
      description:
        "Display the short intuition video for one concept inside an in-chat " +
        "player, with its name, lesson, pages, and PhET link. Accepts a slug or " +
        "name. The video is a SHORT APPETIZER/TEASER built to spark curiosity and " +
        "give a first intuitive glimpse — use it to OPEN a concept and hook the " +
        "student, then teach the real content from the book (read_lesson_pages). " +
        "It is the way in, not the lesson itself.",
      inputSchema: { concept: z.string().min(1).describe("Concept slug or name") },
      outputSchema: {
        slug: z.string().optional(), concept_ar: z.string().optional(),
        concept_en: z.string().optional(), chapter_title_ar: z.string().optional(),
        lesson_title_ar: z.string().optional(), pages: z.string().optional(),
        phet: z.string().nullable().optional(), video_url: z.string().nullable().optional(),
        message: z.string().nullable().optional(),
      },
      _meta: { ui: { resourceUri: VIDEO_WIDGET } },
    },
    async ({ concept }) => {
      const c = resolveConcept(concept);
      if (!c) return { ...text(`لم أجد مفهومًا باسم "${concept}".`), structuredContent: { message: `لم أجد "${concept}".` } };
      const payload = conceptWidgetPayload(c);
      const note = payload.video_url
        ? `يعرض فيديو: ${c.concept_ar} (${c.concept_en}).`
        : `${c.concept_ar}: ${payload.message}`;
      return { content: [{ type: "text", text: note }], structuredContent: payload };
    }
  );

  // ---- show_prerequisite_video ----
  registerAppTool(
    server,
    "show_prerequisite_video",
    {
      title: "Show a lesson's prerequisite (foundation) video",
      description:
        "Open the foundational intuition video a lesson should START with — the " +
        "mental-model 'appetizer' (kind: foundation) that builds intuition and " +
        "sparks curiosity BEFORE any equation or book content. Pass a lesson id " +
        "(e.g. '1-1'); returns the in-chat player for that lesson's prerequisite " +
        "video. Use this to OPEN a lesson before teaching from the book; for " +
        "lesson 1-1 it is the gravity-intuition video. If a lesson has no " +
        "foundation video, it says so.",
      inputSchema: { lesson: z.string().min(1).describe("Lesson id, e.g. '1-1'") },
      outputSchema: {
        slug: z.string().optional(), concept_ar: z.string().optional(),
        concept_en: z.string().optional(), chapter_title_ar: z.string().optional(),
        lesson_title_ar: z.string().optional(), pages: z.string().optional(),
        phet: z.string().nullable().optional(), video_url: z.string().nullable().optional(),
        message: z.string().nullable().optional(),
      },
      _meta: { ui: { resourceUri: VIDEO_WIDGET } },
    },
    async ({ lesson }) => {
      const lid = lesson.trim();
      const found = conceptList.find((c) => c.kind === "foundation" && c.lesson === lid);
      if (!found) {
        const msg = `لا يوجد فيديو تمهيدي (نموذج ذهني) للدرس "${lesson}".`;
        return { ...text(msg), structuredContent: { message: msg } };
      }
      const payload = conceptWidgetPayload(found);
      const note = payload.video_url
        ? `الفيديو التمهيدي للدرس ${lid}: ${found.concept_ar} — افتتح به الحصة ثم انتقل إلى الكتاب.`
        : `${found.concept_ar}: ${payload.message}`;
      return { content: [{ type: "text", text: note }], structuredContent: payload };
    }
  );

  // ---- show_project_video ----
  registerAppTool(
    server,
    "show_project_video",
    {
      title: "Show a project's video",
      description:
        "Display a homework-story project video inside the in-chat player, with " +
        "its title, persona, and PhET link. Accepts a project slug or name.",
      inputSchema: { project: z.string().min(1).describe("Project slug or name") },
      outputSchema: {
        slug: z.string().optional(), concept_ar: z.string().optional(),
        concept_en: z.string().optional(), chapter_title_ar: z.string().optional(),
        lesson_title_ar: z.string().optional(), pages: z.string().optional(),
        phet: z.string().nullable().optional(), video_url: z.string().nullable().optional(),
        message: z.string().nullable().optional(),
      },
      _meta: { ui: { resourceUri: VIDEO_WIDGET } },
    },
    async ({ project }) => {
      const p = resolveProject(project);
      if (!p) return { ...text(`لم أجد مشروعًا باسم "${project}".`), structuredContent: { message: `لم أجد "${project}".` } };
      const payload = projectWidgetPayload(p);
      const note = payload.video_url
        ? `يعرض مشروع: ${p.project_ar}.`
        : `${p.project_ar}: ${payload.message}`;
      return { content: [{ type: "text", text: note }], structuredContent: payload };
    }
  );

  // ---- read_lesson_pages ----
  registerAppTool(
    server,
    "read_lesson_pages",
    {
      title: "Read a lesson's full textbook content",
      description:
        "Return the structured, page-by-page content of a lesson's textbook " +
        "pages by lesson id (e.g. '1-1'): headings, paragraphs, equations (LaTeX), " +
        "tables, figure descriptions, worked examples, key terms, and every " +
        "question. This is the real book text the student is studying — call it " +
        "before explaining ANY lesson, teach ONLY from what it returns, and cite " +
        "page numbers. If it reports the lesson is unavailable, tell the student " +
        "it isn't ready yet and suggest an available lesson — do NOT improvise " +
        "textbook content from your own knowledge.",
      inputSchema: { lesson: z.string().min(1).describe("Lesson id, e.g. '1-1'") },
      outputSchema: { lesson: z.any() },
      _meta: {},
    },
    async ({ lesson }) => {
      const lp = lessonPages[lesson.trim()];
      if (!lp) {
        const have = Object.keys(lessonPages).sort().join(", ") || "(none yet)";
        return text(`محتوى الدرس "${lesson}" غير متوفر بعد. الدروس المتوفرة: ${have}.`, { lesson: null });
      }
      const lines = [`الدرس ${lp.lesson_id}: ${lp.title_ar} (${lp.title_en}) — صفحات ${lp.page_range.start}-${lp.page_range.end}`];
      if (lp.lesson_summary_ar) lines.push("", lp.lesson_summary_ar);
      for (const pg of lp.pages) {
        lines.push("", `— صفحة ${pg.page} —`);
        for (const b of pg.blocks) {
          if (b.type === "heading") lines.push(`## ${b.text_ar}`);
          else if (b.type === "objectives") lines.push("الأهداف: " + b.items_ar.join(" · "));
          else if (b.type === "paragraph") lines.push(b.text_ar);
          else if (b.type === "equation") lines.push(`[معادلة] ${b.latex}` + (b.caption_ar ? ` — ${b.caption_ar}` : ""));
          else if (b.type === "figure") lines.push(`[${b.label_ar}] ${b.description_ar}`);
          else if (b.type === "table") lines.push(`[جدول] ${b.caption_ar || ""} (${b.rows.length} صفوف)`);
          else if (b.type === "key_term") lines.push(`[مصطلح] ${b.term_ar}: ${b.definition_ar}`);
          else if (b.type === "margin_note") lines.push(`[ملاحظة] ${b.text_ar}`);
          else if (b.type === "worked_example") lines.push(`[مثال محلول${b.printed_number ? " " + b.printed_number : ""}] ${b.prompt_ar}`);
          else if (b.type === "question_set") lines.push(`[${b.title_ar}] ${b.questions.map((q) => `(${q.printed_number}) ${q.prompt_ar}`).join("  ")}`);
        }
      }
      return { content: [{ type: "text", text: lines.join("\n") }], structuredContent: { lesson: lp } };
    }
  );

  // ---- find_question ----
  registerAppTool(
    server,
    "find_question",
    {
      title: "Find a specific textbook question",
      description:
        "Resolve a teacher/student reference like 'سؤال 8 صفحة 17' to the exact " +
        "question. Provide the lesson id, and the printed number and/or page. " +
        "Returns the matching question(s) with prompt, given data, and subparts.",
      inputSchema: {
        lesson: z.string().min(1).describe("Lesson id, e.g. '1-1'"),
        number: z.string().optional().describe("Printed question number, e.g. '8'"),
        page: z.number().int().optional().describe("Printed page number"),
      },
      outputSchema: { questions: z.array(z.any()) },
      _meta: {},
    },
    async ({ lesson, number, page }) => {
      const lp = lessonPages[lesson.trim()];
      if (!lp) return text(`محتوى الدرس "${lesson}" غير متوفر بعد.`, { questions: [] });
      const all = [];
      for (const pg of lp.pages)
        for (const b of pg.blocks)
          if (b.type === "question_set") all.push(...b.questions);
          else if (b.type === "question") all.push(b);
      const hits = all.filter(
        (q) =>
          (number == null || String(q.printed_number) === String(number)) &&
          (page == null || q.page === page)
      );
      const t = hits.length
        ? hits.map((q) => `(${q.printed_number}، ص ${q.page}) ${q.prompt_ar}`).join("\n")
        : `لم أجد سؤالًا مطابقًا في الدرس ${lesson}.`;
      return { content: [{ type: "text", text: t }], structuredContent: { questions: hits } };
    }
  );

  // === KST diagnostic tutoring tools ===
  // The deployed extraction has NO answer key, so correctness is the assistant's
  // judgment; these tools own question SELECTION, STATE, and gap DIAGNOSIS, and
  // each output names the next teacher action so the model is never lost.
  const RESPONSE = z.object({ item_id: z.string(), correct: z.boolean() });
  const MIN_DIAGNOSTIC_QS = 4;

  // ---- run_diagnostic_tutoring_step (orchestrator — preferred) ----
  registerAppTool(
    server,
    "run_diagnostic_tutoring_step",
    {
      title: "Run one step of diagnostic tutoring (preferred)",
      description:
        "Use this to drive an interactive study session. It decides the next " +
        "tutoring action from the diagnostic state so far: ask another diagnostic " +
        "question, or diagnose the gap and teach. This is the PREFERRED tool for " +
        "KST-based tutoring — prefer it over calling the individual tools.\n" +
        "When: the student starts studying, says 'where do I start?', asks for " +
        "general review, or seems unsure.\n" +
        "How: first call with responses:[] (and the student's message). It returns " +
        "next_action:'ask_question' with the full question — ask the student that " +
        "question verbatim and wait. When they answer, YOU judge correct/incorrect " +
        "(there is no answer key), then call this tool again passing the SAME " +
        "responses you got back in internal_state PLUS last_question_item_id and " +
        "was_correct. After enough questions it returns next_action:'teach_gap' " +
        "with the lesson to teach.\n" +
        "Do NOT use when the student explicitly asks for a specific lesson and " +
        "doesn't want diagnosis — teach that lesson directly. Never expose tool " +
        "names, item_ids, or KST internals to the student.",
      inputSchema: {
        responses: z.array(RESPONSE).optional().describe("Running answers; pass back what you received in internal_state.responses"),
        last_question_item_id: z.string().optional().describe("item_id of the question the student just answered"),
        was_correct: z.boolean().optional().describe("Your judgment of that answer (true = correct or strong-partial)"),
        student_message: z.string().optional().describe("The student's latest message, for tone only"),
      },
      outputSchema: {
        next_action: z.string(),
        message_to_student_ar: z.string(),
        question: z.any().optional(),
        after_answer_call: z.string().optional(),
        gap: z.any().optional(),
        prerequisite: z.any().optional(),
        tool_to_call_next: z.any().optional(),
        internal_state: z.any(),
        diagnostic: z.any().optional(),
      },
      _meta: {},
    },
    async ({ responses, last_question_item_id, was_correct, student_message }) => {
      if (!diagnostics) return text("محرّك التشخيص غير متوفر حاليًا.", { next_action: "unavailable", message_to_student_ar: "", internal_state: { responses: [] } });
      const resp = [...(responses || [])];
      if (last_question_item_id && typeof was_correct === "boolean" && !resp.some((r) => r.item_id === last_question_item_id))
        resp.push({ item_id: last_question_item_id, correct: was_correct });

      const nextId = resp.length < MIN_DIAGNOSTIC_QS ? diagnostics.suggestNext(resp).next_item?.item_id : null;
      if (nextId) {
        const first = resp.length === 0;
        const out = {
          next_action: "ask_question",
          message_to_student_ar: first
            ? "خلنا نبدأ بسؤال بسيط أعرف منه نقطة انطلاقك المناسبة:"
            : "تمام، سؤال آخر يساعدني أحدّد من أين نبدأ:",
          question: questionPayload(nextId),
          after_answer_call: "run_diagnostic_tutoring_step",
          internal_state: { responses: resp },
        };
        return { content: [{ type: "text", text: out.message_to_student_ar }], structuredContent: out };
      }

      // enough evidence -> diagnose and route to teaching
      const d = diagnostics.diagnose(resp);
      const base = { internal_state: { responses: resp }, diagnostic: { confidence: d.confidence, structural_gap: d.structural_gap } };
      if (d.status === "no_gap") {
        const msg = "ما ظهرت فجوة واضحة فيما قيّمناه — نقدر نكمل بالدرس التالي أو نتعمّق أكثر.";
        return { content: [{ type: "text", text: msg }], structuredContent: { ...base, next_action: "advance_to_next_lesson", message_to_student_ar: msg } };
      }
      if (d.teach_kind === "prerequisite") {
        const mot = d.teach?.motivates;
        const msg = `قبل ${mot?.concept_en || "المفهوم المطلوب"}، يبدو أن الأساس الذي نقوّيه أولًا هو ${d.gap_label}.`;
        const out = { ...base, next_action: "teach_prerequisite_first", message_to_student_ar: msg,
          prerequisite: { node: d.gap_node, label: d.gap_label, motivates: mot },
          tool_to_call_next: mot?.lesson ? { name: "read_lesson_pages", arguments: { lesson: mot.lesson } } : null };
        return { content: [{ type: "text", text: msg }], structuredContent: out };
      }
      const cAr = conceptName(d.slug, d.concept_en);
      const msg = `واضح أن أنسب نقطة نبدأ منها هي ${cAr} — الدرس ${d.lesson}.`;
      const out = { ...base, next_action: "teach_gap", message_to_student_ar: msg,
        gap: { slug: d.slug, lesson: d.lesson, book_pages: d.book_pages, concept_ar: cAr, concept_en: d.concept_en },
        tool_to_call_next: { name: "read_lesson_pages", arguments: { lesson: d.lesson } } };
      return { content: [{ type: "text", text: msg }], structuredContent: out };
    }
  );

  // ---- choose_next_diagnostic_question (KST half-split) ----
  registerAppTool(
    server,
    "choose_next_diagnostic_question",
    {
      title: "Choose the next diagnostic question for the student",
      description:
        "Use this when a student starts a study session, asks 'where should I " +
        "start?', asks for general review, or seems unsure. It picks the ONE " +
        "diagnostic question that best reveals the student's current knowledge gap " +
        "(KST half-split) and returns the full question text. Ask the returned " +
        "question to the student verbatim and wait for their answer — do not " +
        "explain the lesson yet.\n" +
        "Example: User: 'أريد مراجعة الزخم.' → call with responses:[] → ask the " +
        "returned prompt_ar.\n" +
        "Do NOT use after the student has answered enough questions and " +
        "diagnose_student_gap_from_answers has returned a lesson (that would loop). " +
        "Prefer run_diagnostic_tutoring_step, which manages this whole loop.",
      inputSchema: {
        responses: z.array(RESPONSE).optional().describe("Answers gathered so far (omit or [] to start)"),
      },
      outputSchema: {
        next_teacher_action: z.string(),
        message_to_student_ar: z.string(),
        question: z.any().nullable(),
        after_answer_call: z.string().optional(),
        responses_so_far: z.number(),
      },
      _meta: {},
    },
    async ({ responses }) => {
      if (!diagnostics) return text("محرّك التشخيص غير متوفر حاليًا.", { next_teacher_action: "unavailable", message_to_student_ar: "", question: null, responses_so_far: 0 });
      const resp = responses || [];
      const id = diagnostics.suggestNext(resp).next_item?.item_id;
      if (!id) {
        const out = { next_teacher_action: "ready_to_diagnose", message_to_student_ar: "كفى أسئلة — لنحدّد نقطة البداية.",
          question: null, after_answer_call: "diagnose_student_gap_from_answers", responses_so_far: resp.length };
        return { content: [{ type: "text", text: out.message_to_student_ar }], structuredContent: out };
      }
      const out = { next_teacher_action: "ask_student_this_question",
        message_to_student_ar: resp.length ? "سؤال آخر:" : "لنبدأ بسؤال تشخيصي بسيط:",
        question: questionPayload(id), after_answer_call: "grade_diagnostic_answer", responses_so_far: resp.length };
      return { content: [{ type: "text", text: `اطرح على الطالب: ${out.question.prompt_ar}` }], structuredContent: out };
    }
  );

  // ---- grade_diagnostic_answer (grading-context helper; assistant judges) ----
  registerAppTool(
    server,
    "grade_diagnostic_answer",
    {
      title: "Get grading context for a student's diagnostic answer",
      description:
        "Use this immediately after the student answers a diagnostic question, to " +
        "grade it well and give good feedback. NOTE: the textbook extraction has " +
        "no answer key, so this tool does not auto-grade — it returns the question, " +
        "its options/given data, and the lesson's common misconceptions, and YOU " +
        "decide correct / partial / incorrect from the student's reasoning and " +
        "units. Treat a weak partial as incorrect for diagnosis. Then record the " +
        "result as {item_id, correct} and continue via run_diagnostic_tutoring_step " +
        "(or diagnose_student_gap_from_answers). Give the student gentle feedback " +
        "using the misconceptions; never hand them the full solution outright.",
      inputSchema: {
        item_id: z.string().describe("The diagnostic question's item_id"),
        student_answer: z.string().optional().describe("The student's answer (for your judgment)"),
      },
      outputSchema: {
        requires_assistant_judgment: z.boolean(),
        question: z.any(),
        common_misconceptions_ar: z.array(z.string()),
        how_to_grade_ar: z.string(),
        after_grading: z.any(),
        teacher_feedback_hint_ar: z.string(),
      },
      _meta: {},
    },
    async ({ item_id }) => {
      const q = questionById.get(item_id);
      const out = {
        requires_assistant_judgment: true,
        question: questionPayload(item_id),
        common_misconceptions_ar: (q && misconceptionsByLesson.get(q.lesson)) || [],
        how_to_grade_ar:
          "لا يوجد مفتاح إجابة في الكتاب. احكم بنفسك: صحيح / جزئي / خطأ بناءً على منطق الطالب ووحداته؛ واعتبر الجزئي الضعيف خطأً لأغراض التشخيص.",
        after_grading: {
          record_answer_as: { item_id, correct: "true إن كانت صحيحة أو جزئية قوية، وإلا false" },
          then_call: "run_diagnostic_tutoring_step (مرّر responses محدّثة مع last_question_item_id و was_correct)",
        },
        teacher_feedback_hint_ar:
          "إن أخطأ الطالب صحّح بلطف مستعينًا بالمفاهيم الخاطئة الشائعة أعلاه، بسؤال أو تلميح، دون إعطاء الحل كاملًا.",
      };
      return { content: [{ type: "text", text: "قيّم إجابة الطالب بنفسك (لا يوجد مفتاح إجابة)، ثم سجّل النتيجة وتابع." }], structuredContent: out };
    }
  );

  // ---- diagnose_student_gap_from_answers (KST gap location) ----
  registerAppTool(
    server,
    "diagnose_student_gap_from_answers",
    {
      title: "Diagnose the student's gap from their diagnostic answers",
      description:
        "Use this after the student has answered diagnostic questions, to identify " +
        "the best concept/lesson to teach next based on their correct/incorrect " +
        "answers (Knowledge Space Theory over the prerequisite graph) — so you " +
        "teach the student's actual gap, not table-of-contents order. Pass " +
        "responses:[{item_id, correct}]. It returns the gap with its slug, lesson, " +
        "and book pages; then teach that lesson via read_lesson_pages, telling the " +
        "student e.g. 'نقطة انطلاقك المناسبة هي حفظ الزخم'. If teach_kind is " +
        "'prerequisite', the gap is a foundational idea with no lesson — start " +
        "there, motivated by the concept it unlocks.\n" +
        "Do NOT use when the student explicitly asked for a specific lesson and " +
        "doesn't want diagnosis — teach that lesson directly. Do not show KST " +
        "internals or tool names to the student. Prefer run_diagnostic_tutoring_step.",
      inputSchema: {
        responses: z.array(RESPONSE).describe("Answers gathered: item_id + whether correct"),
      },
      outputSchema: {
        next_teacher_action: z.string(),
        student_facing_reason_ar: z.string(),
        gap: z.any().nullable(),
        prerequisite: z.any().optional(),
        tool_to_call_next: z.any().nullable(),
        status: z.string(),
        teach_kind: z.string().optional(),
        confidence: z.number().optional(),
        structural_gap: z.any().optional(),
      },
      _meta: {},
    },
    async ({ responses }) => {
      if (!diagnostics) return text("محرّك التشخيص غير متوفر حاليًا.", { next_teacher_action: "unavailable", student_facing_reason_ar: "", gap: null, tool_to_call_next: null, status: "unavailable" });
      const d = diagnostics.diagnose(responses || []);
      const common = { status: d.status, teach_kind: d.teach_kind, confidence: d.confidence, structural_gap: d.structural_gap };
      if (d.status === "no_gap") {
        const msg = "ما ظهرت فجوة واضحة فيما قيّمناه — نقدر نكمل بالدرس التالي.";
        return { content: [{ type: "text", text: msg }], structuredContent: { ...common, next_teacher_action: "advance_to_next_lesson", student_facing_reason_ar: msg, gap: null, tool_to_call_next: null } };
      }
      if (d.teach_kind === "prerequisite") {
        const mot = d.teach?.motivates;
        const msg = `قبل ${mot?.concept_en || "المفهوم المطلوب"}، الأساس الذي نقوّيه أولًا هو ${d.gap_label}.`;
        const out = { ...common, next_teacher_action: "teach_prerequisite_first", student_facing_reason_ar: msg,
          gap: null, prerequisite: { node: d.gap_node, label: d.gap_label, motivates: mot },
          tool_to_call_next: mot?.lesson ? { name: "read_lesson_pages", arguments: { lesson: mot.lesson } } : null };
        return { content: [{ type: "text", text: msg }], structuredContent: out };
      }
      const cAr = conceptName(d.slug, d.concept_en);
      const msg = `واضح أن أنسب نقطة نبدأ منها هي ${cAr}.`;
      const out = { ...common, next_teacher_action: "teach_gap_lesson", student_facing_reason_ar: msg,
        gap: { slug: d.slug, lesson: d.lesson, book_pages: d.book_pages, concept_ar: cAr, concept_en: d.concept_en },
        tool_to_call_next: { name: "read_lesson_pages", arguments: { lesson: d.lesson } } };
      return { content: [{ type: "text", text: `${msg} الدرس ${d.lesson} (صفحات ${d.book_pages}).` }], structuredContent: out };
    }
  );

  return server;
}

const httpServer = createServer(async (req, res) => {
  if (!req.url) return res.writeHead(400).end("Missing URL");
  const url = new URL(req.url, `http://${req.headers.host ?? "localhost"}`);

  if (req.method === "OPTIONS" && url.pathname === MCP_PATH) {
    return res
      .writeHead(204, {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type, mcp-session-id",
        "Access-Control-Expose-Headers": "Mcp-Session-Id",
      })
      .end();
  }

  if (req.method === "GET" && url.pathname === "/") {
    return res.writeHead(200, { "content-type": "text/plain" }).end("Physics 2 MCP server. POST /mcp");
  }

  // We run stateless JSON mode (POST only) and do NOT offer a server-initiated
  // SSE stream. Answer GET/DELETE on /mcp with 405 immediately — otherwise the
  // transport dangles an open GET stream and ChatGPT drops the connector.
  if (url.pathname === MCP_PATH && (req.method === "GET" || req.method === "DELETE")) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    return res.writeHead(405, { allow: "POST", "content-type": "text/plain" }).end("Method Not Allowed; use POST");
  }

  if (url.pathname === MCP_PATH && req.method === "POST") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");

    const server = createPhysicsServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => {
      transport.close();
      server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (err) {
      console.error("MCP request error:", err);
      if (!res.headersSent) res.writeHead(500).end("Internal server error");
    }
    return;
  }

  res.writeHead(404).end("Not Found");
});

httpServer.listen(PORT, () => {
  console.log(`Physics 2 MCP server on http://localhost:${PORT}${MCP_PATH}`);
  if (!BASE) console.log("  PUBLIC_VIDEO_BASE unset — asset URLs will be null until set.");
});
