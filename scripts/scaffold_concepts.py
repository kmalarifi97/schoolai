#!/usr/bin/env python3
"""Scaffold one self-contained build directory per concept.

Reads (never modifies) concept_library_beats_v2.json + structure.json.
Writes scripts/concepts/NN_slug/ for each of the 26 concepts:
  - <slug>.json   : concept + beats + book page reference + objectives/key terms
  - BUILD.md      : human/agent build brief
  - the video     : copied in for shipped concepts; render target named for to-build
"""
import json, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent          # physics-E2-library/
SCRIPTS = ROOT / "scripts"
OUT = SCRIPTS / "concepts"
VIDEOS = ROOT / "videos"

lib = json.load(open(SCRIPTS / "concept_library_beats_v2.json"))
struct = json.load(open(SCRIPTS / "structure.json"))
book = struct["book"]
pdf_rel = "../../../book/فيزياء ثاني ثنوي.pdf"   # shared 92MB PDF, not duplicated

# lesson id -> {pages, titles, objectives, key_terms, chapter titles}
lessons = {}
for ch in struct["chapters"]:
    for ls in ch.get("lessons", []):
        lessons[ls["id"]] = {
            "chapter_id": ch["id"],
            "chapter_title_en": ch["title_en"],
            "chapter_title_ar": ch["title_ar"],
            "lesson_title_en": ls["title_en"],
            "lesson_title_ar": ls["title_ar"],
            "start_page": ls["start_page"],
            "end_page": ls["end_page"],
            "objectives": ls.get("objectives", []),
            "key_terms": ls.get("key_terms", []),
            "lesson_summary_ar": ls.get("summary", ""),
        }

OUT.mkdir(exist_ok=True)
manifest = []

for c in lib["concepts"]:
    n = c["order"]
    slug = c["slug"]
    dname = f"{n:02d}_{slug}"
    d = OUT / dname
    d.mkdir(exist_ok=True)

    L = lessons.get(c["lesson"], {})
    video_name = f"{slug}_full_voiced_subs.mp4"

    # ---- video handling ----
    video_status = "to-build"
    src = VIDEOS / video_name
    if c["status"] == "shipped" and src.exists():
        shutil.copy2(src, d / video_name)
        video_status = "present (copied from videos/)"
    elif c["status"] == "shipped-external":
        video_status = "shipped externally — see source field, not in this repo"

    pkg = {
        "order": n,
        "slug": slug,
        "concept_en": c["concept_en"],
        "concept_ar": c["concept_ar"],
        "status": c["status"],
        "source": c.get("source"),
        "book": {
            "title_ar": book["title_ar"],
            "title_en": book["title_en"],
            "edition": book["edition"],
            "pdf": pdf_rel,
            "page_note": book["notes"],
            "chapter": L.get("chapter_id"),
            "chapter_title_en": L.get("chapter_title_en"),
            "chapter_title_ar": L.get("chapter_title_ar"),
            "lesson": c["lesson"],
            "lesson_title_en": L.get("lesson_title_en"),
            "lesson_title_ar": L.get("lesson_title_ar"),
            "pages": f"{L.get('start_page')}-{L.get('end_page')}",
            "start_page": L.get("start_page"),
            "end_page": L.get("end_page"),
            "lesson_objectives": L.get("objectives", []),
            "lesson_key_terms": L.get("key_terms", []),
        },
        "video": {
            "target_filename": video_name,
            "status": video_status,
        },
        "production": {
            "model": lib["model"],
            "tone": lib["tone"],
            "visual_signature": lib["visual_signature"],
        },
        "beats": c["beats"],
    }
    json.dump(pkg, open(d / f"{slug}.json", "w"), ensure_ascii=False, indent=2)

    nb = len(c["beats"])
    brief = f"""# Build brief — Concept {n:02d}: {c['concept_en']}

**Arabic:** {c['concept_ar']}
**Status:** {c['status']}  |  **Beats:** {nb if nb else 'n/a (shipped — reuse existing)'}

## Book grounding
- Book: {book['title_en']} ({book['edition']})
- Chapter {L.get('chapter_id')} — {L.get('chapter_title_en')} / {L.get('chapter_title_ar')}
- Lesson {c['lesson']} — {L.get('lesson_title_en')} / {L.get('lesson_title_ar')}
- **PDF pages: {L.get('start_page')}–{L.get('end_page')}** in `{pdf_rel}` (PDF page == printed page)
- Read these pages first. The video introduces the concept; it must stay faithful to how the book frames it. It must NOT solve the book's problems — students do that.

### Lesson objectives (from the book)
""" + "\n".join(f"- {o}" for o in L.get("objectives", [])) + f"""

### Key terms to honor
""" + "\n".join(f"- {k}" for k in L.get("key_terms", [])) + f"""

## What to build
- One short concept-spark video: `{video_name}`
- Beats are in `{slug}.json` → `beats[]` (id / text / visual). English narration, Arabic subs burned in, pure #000000 void.
- `[Hold Ns in silence]` markers in a beat's visual mean exactly that: hold the frame, no narration.
- Pipeline + conventions: `manim/CLAUDE.md` (Standard pipeline section). Slug = `{slug}`.
- {"This concept is already shipped — video copied into this directory; rebuild only if asked." if c['status']=='shipped' else "Video shipped externally; pull in / re-derive only if asked." if c['status']=='shipped-external' else "Produce the video here."}

## Hand-off contract
Deliver `{video_name}` in this directory. Tone is non-negotiable: silence is content, kitchen-table-warm, concept before equations, no worked problems, no hype.
"""
    open(d / "BUILD.md", "w").write(brief)

    manifest.append({
        "dir": f"concepts/{dname}",
        "order": n, "slug": slug, "concept_en": c["concept_en"],
        "chapter": L.get("chapter_id"), "lesson": c["lesson"],
        "book_pages": f"{L.get('start_page')}-{L.get('end_page')}",
        "status": c["status"], "beats": nb, "video": video_name,
    })

json.dump(
    {"library": lib["library"], "source_of_truth": "scripts/concept_library_beats_v2.json",
     "note": "Per-concept build packages. The v2 file remains the single editable source; these are derived. Re-run scaffold_concepts.py to regenerate.",
     "concepts": manifest},
    open(OUT / "INDEX.json", "w"), ensure_ascii=False, indent=2)

print(f"scaffolded {len(manifest)} concept dirs under {OUT}")
for m in manifest:
    print(f"  {m['dir']:<28} ch{m['chapter']} {m['lesson']:<4} p{m['book_pages']:<8} {m['status']:<15} beats={m['beats']}")
