"""Export the full Physics 2 library for the ChatGPT App's MCP server.

Pulls from the repo's source-of-truth manifests and writes one JSON the Node
server reads at startup. Re-run whenever the manifests change.

    python3 chatgpt-app/build_app_data.py

Sources:
    scripts/structure.json                 chapters -> lessons (summary, objectives, key_terms, pages)
    scripts/concept_library_beats_v2.json   concepts + intuition narration beats
    scripts/projects/*/*.json               homework-story projects + beats
    web/backend/catalog.py                   resolves which concepts/projects have a video + PhET links

Writes: chatgpt-app/data/library.json
"""
import glob
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = ROOT / "scripts"
sys.path.insert(0, str(ROOT / "web" / "backend"))

from catalog import build  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "data" / "library.json"


def _beats_text(beats):
    return [b["text"].strip() for b in (beats or []) if b.get("text", "").strip()]


def main():
    struct = json.load(open(S / "structure.json", encoding="utf-8"))
    v2 = json.load(open(S / "concept_library_beats_v2.json", encoding="utf-8"))
    catalog, _ = build()

    beats_by_slug = {c["slug"]: _beats_text(c.get("beats")) for c in v2["concepts"]}

    # concept slug -> {has_video, phet}, plus chapter/lesson titles, from the catalog
    cat_concept = {}
    phet_for = {}
    for pj in catalog.get("projects", []):
        for slug in pj.get("combines", []):
            phet_for.setdefault(slug, pj.get("phet"))
    for ch in catalog["chapters"]:
        for ls in ch["lessons"]:
            for c in ls["concepts"]:
                cat_concept[c["slug"]] = {
                    "has_video": bool(c.get("video")),
                    "chapter_title_ar": ch["title_ar"],
                    "lesson_title_ar": ls["title_ar"],
                }

    # --- concepts (flat, by slug) ---
    concepts = {}
    for c in v2["concepts"]:
        slug = c["slug"]
        meta = cat_concept.get(slug, {})
        concepts[slug] = {
            "slug": slug,
            "concept_ar": c["concept_ar"],
            "concept_en": c["concept_en"],
            "chapter": c["chapter"],
            "chapter_title_ar": meta.get("chapter_title_ar", ""),
            "lesson": c["lesson"],
            "lesson_title_ar": meta.get("lesson_title_ar", ""),
            "pages": next((x["pages"] for ch in catalog["chapters"] for ls in ch["lessons"]
                           for x in ls["concepts"] if x["slug"] == slug), ""),
            "has_video": meta.get("has_video", False),
            "phet": phet_for.get(slug),
            "handoff_ar": beats_by_slug.get(slug, [""])[-1] if beats_by_slug.get(slug) else "",
            "beats": beats_by_slug.get(slug, []),
        }

    # --- chapters -> lessons (TOC with the textbook knowledge) ---
    concepts_by_lesson = {}
    for slug, c in concepts.items():
        concepts_by_lesson.setdefault(c["lesson"], []).append(slug)

    chapters = []
    for ch in struct["chapters"]:
        lessons = []
        for ls in ch.get("lessons", []):
            lessons.append({
                "id": ls["id"],
                "title_ar": ls.get("title_ar", ""),
                "title_en": ls.get("title_en", ""),
                "start_page": ls.get("start_page"),
                "end_page": ls.get("end_page"),
                "summary": ls.get("summary", ""),
                "objectives": ls.get("objectives", []),
                "key_terms": ls.get("key_terms", []),
                "concepts": [
                    {"slug": s, "concept_ar": concepts[s]["concept_ar"],
                     "has_video": concepts[s]["has_video"]}
                    for s in concepts_by_lesson.get(ls["id"], [])
                ],
            })
        chapters.append({
            "id": ch["id"],
            "title_ar": ch["title_ar"],
            "title_en": ch["title_en"],
            "start_page": ch.get("start_page"),
            "end_page": ch.get("end_page"),
            "summary": ch.get("summary", ""),
            "key_terms": ch.get("key_terms", []),
            "lessons": lessons,
        })

    # --- projects (homework stories) ---
    projects = []
    for pjf in sorted(glob.glob(str(S / "projects/*/*.json"))):
        d = json.load(open(pjf, encoding="utf-8"))
        slug = d["slug"]
        has_video = bool(glob.glob(str(pathlib.Path(pjf).parent / f"{slug}_full_voiced_subs.mp4")))
        cat_pj = next((p for p in catalog.get("projects", []) if p["slug"] == slug), {})
        projects.append({
            "slug": slug,
            "project_ar": d.get("project_ar", ""),
            "project_en": d.get("project_en", ""),
            "persona": d.get("persona", ""),
            "phet": cat_pj.get("phet"),
            "concepts_combined": d.get("concepts_combined", []),
            "ending_hint": d.get("ending_hint", ""),
            "has_video": has_video,
            "beats": _beats_text(d.get("beats")),
        })

    book = struct["book"]
    library = {
        "book": {
            "title_ar": book["title_ar"], "title_en": book["title_en"],
            "edition": book["edition"], "publisher": book["publisher"],
            "pages": book["total_pdf_pages"], "page_note": book.get("notes", ""),
        },
        "chapters": chapters,
        "concepts": concepts,
        "projects": projects,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(library, ensure_ascii=False, indent=2), encoding="utf-8")
    nv = sum(c["has_video"] for c in concepts.values())
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  {len(chapters)} chapters, "
          f"{sum(len(c['lessons']) for c in chapters)} lessons, "
          f"{len(concepts)} concepts ({nv} with video), {len(projects)} projects")


if __name__ == "__main__":
    main()
