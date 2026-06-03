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

// Pre-built book-graph model + per-student session overlay (shipped seed/book.db,
// copied to a writable path at startup). Replaces the old on-demand log model.
import { copyFileSync, existsSync } from "node:fs";
import {
  openDb as openBookGraph, chaptersTree, structureSummary, searchConcepts,
  getContentNode, getPrereqGraph, attachPrereqGraph, startSession, logOnNode,
  studentStruggles,
} from "./bookgraph.mjs";

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

const projects = LIB.projects;
const projectBySlug = new Map(projects.map((p) => [p.slug, p]));

// lesson id -> { ...lesson, chapter_id, chapter_title_ar }
const lessonById = new Map();
for (const ch of LIB.chapters) {
  for (const ls of ch.lessons) {
    lessonById.set(ls.id, { ...ls, chapter_id: ch.id, chapter_title_ar: ch.title_ar });
  }
}

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

// Pre-built book graph (shipped read-only as seed/book.db) → writable copy so
// per-student session logs can be written (Cloud Run fs is ephemeral). Honors
// BOOKGRAPH_DB (defaults to /tmp/book.db). Disabled gracefully so the video/
// content tools still work if it fails.
const BOOKGRAPH_GUIDE = `Decompose the concept into its prerequisite graph for an 18-year-old: layer by layer,
descend from the physics concept into the underlying math, justify why each node needs the one
beneath it, and STOP at the floor "equation/variable literacy" (a symbol stands for a number, =
means both sides are equal). ~6-10 nodes, one Arabic check question per node, one floor node.`;
let bookgraph = null;
try {
  const SEED = join(HERE, "seed", "book.db");
  const DBPATH = process.env.BOOKGRAPH_DB || "/tmp/book.db";
  if (!existsSync(DBPATH) && existsSync(SEED)) copyFileSync(SEED, DBPATH);
  bookgraph = openBookGraph(DBPATH);
  console.log(`book-graph model ready (db: ${DBPATH})`);
} catch (e) {
  console.error(`book-graph model disabled: ${e.message}`);
}

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

  // === Book-graph model: pre-built prerequisite graph + per-student overlay ===
  // find_book_concept → get_prereq_graph (pre-built; or decompose on demand +
  // save_prereq_graph) → log_struggle per node → get_student_status for gaps.
  const _bgOff = () => text("سجل الخبرة غير متاح حاليًا.", { error: "book-graph unavailable" });
  const _NODE = z.object({ concept: z.string(), layer: z.number().optional(), is_floor: z.boolean().optional(), check_question: z.string().optional() });
  const _EDGE = z.object({ concept: z.string(), requires: z.string(), why: z.string().optional() });

  registerAppTool(
    server,
    "find_book_concept",
    {
      title: "Find a law/concept node in the book",
      description:
        "Search the book's laws/key-concepts by Arabic or English keyword. Returns matches with their " +
        "content_node_id, lesson, type, and whether a pre-built prerequisite graph exists. Call get_prereq_graph next.",
      inputSchema: { query: z.string() },
      outputSchema: { matches: z.any() },
      _meta: {},
    },
    async ({ query }) => {
      if (!bookgraph) return _bgOff();
      const rows = searchConcepts(bookgraph, query).map((r) => ({
        content_node_id: r.content_node_id, lesson: r.lesson, type: r.type,
        name: (r.text || "").slice(0, 80), has_prereq_graph: !!r.has_prereqs,
      }));
      return text(`${rows.length} matches for "${query}"`, { matches: rows });
    }
  );

  registerAppTool(
    server,
    "get_prereq_graph",
    {
      title: "Get a concept's prerequisite graph (pre-built, or decompose on demand)",
      description:
        "For a content_node_id, return its prerequisite graph: nodes (each with a prereq_node_id, layer, " +
        "is_floor, check_question) + edges. Teach from the floor up; after each check question call log_struggle with " +
        "that node's prereq_node_id. If no pre-built graph exists, returns has_prereqs:false + a decomposition guide — " +
        "decompose it yourself and call save_prereq_graph.",
      inputSchema: { content_node_id: z.number() },
      outputSchema: { has_prereqs: z.boolean(), concept: z.any(), nodes: z.any(), edges: z.any(), decomposition_guide: z.any(), next_teacher_action: z.string() },
      _meta: {},
    },
    async ({ content_node_id }) => {
      if (!bookgraph) return _bgOff();
      const cn = getContentNode(bookgraph, content_node_id);
      if (!cn) return text("no such content node", { has_prereqs: false, concept: null, nodes: [], edges: [], decomposition_guide: null, next_teacher_action: "find_concept_again" });
      if (cn.has_prereqs) {
        const g = getPrereqGraph(bookgraph, content_node_id);
        return text(`prereq graph: ${g.nodes.length} nodes`, { has_prereqs: true, concept: cn.text?.slice(0, 80), nodes: g.nodes, edges: g.edges, decomposition_guide: null, next_teacher_action: "teach_from_floor_up_then_log_each_check" });
      }
      return text("no pre-built graph — decompose on demand", { has_prereqs: false, concept: cn.text?.slice(0, 80), nodes: [], edges: [], decomposition_guide: BOOKGRAPH_GUIDE, next_teacher_action: "decompose_then_call_save_prereq_graph" });
    }
  );

  registerAppTool(
    server,
    "save_prereq_graph",
    {
      title: "Save an on-demand prerequisite graph (fallback)",
      description:
        "Persist a prerequisite graph YOU decomposed for a content node that had none, so it joins the " +
        "shared graph (grows it). Idempotent.",
      inputSchema: { content_node_id: z.number(), nodes: z.array(_NODE), edges: z.array(_EDGE) },
      outputSchema: { saved: z.boolean(), nodes: z.number() },
      _meta: {},
    },
    async ({ content_node_id, nodes, edges }) => {
      if (!bookgraph) return _bgOff();
      attachPrereqGraph(bookgraph, content_node_id, { nodes, edges });
      return text(`saved ${nodes.length} prereq nodes`, { saved: true, nodes: nodes.length });
    }
  );

  registerAppTool(
    server,
    "log_struggle",
    {
      title: "Log a student's pass/struggle on a graph node (the session overlay)",
      description:
        "Record this student's outcome on a book-graph node, ON THE LINK between their session and that " +
        "node. ref_kind 'prereq' (a prereq_node_id from get_prereq_graph) or 'content' (a content_node_id). One " +
        "session_id per chat. outcome 'passed' or 'struggled'.",
      inputSchema: {
        student_id: z.string(), session_id: z.string(), ref_kind: z.enum(["prereq", "content"]),
        ref_id: z.number(), outcome: z.enum(["passed", "struggled"]),
      },
      outputSchema: { logged: z.boolean(), next_teacher_action: z.string() },
      _meta: {},
    },
    async ({ student_id, session_id, ref_kind, ref_id, outcome }) => {
      if (!bookgraph) return _bgOff();
      startSession(bookgraph, session_id, student_id);
      logOnNode(bookgraph, { session_id, ref_kind, ref_id, outcome });
      return text(`logged ${outcome}`, { logged: true, next_teacher_action: outcome === "struggled" ? "teach_this_node_now" : "advance" });
    }
  );

  registerAppTool(
    server,
    "get_student_status",
    {
      title: "Get everything a student has struggled on (across sessions)",
      description:
        "Read back this student's logged struggles against book-graph nodes, so you start from their actual " +
        "gaps. Speak in concept names; never show ids.",
      inputSchema: { student_id: z.string() },
      outputSchema: { struggles: z.any() },
      _meta: {},
    },
    async ({ student_id }) => {
      if (!bookgraph) return _bgOff();
      const s = studentStruggles(bookgraph, student_id);
      return text(`${s.length} logged struggle(s)`, { struggles: s });
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
