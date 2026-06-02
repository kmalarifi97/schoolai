"""Read-only, GPT-facing API for the Custom GPT Action.

These endpoints expose curriculum *metadata* only (concept names, lessons,
pages, PhET links) — never the gated mp4/PDF streams. They are safe to call
without a user login. Optional shared-secret guard via the GPT_API_KEY env var
(sent by the Action as the `X-API-Key` header); if unset, endpoints are open.

Mounted by app.py:  app.include_router(make_router(CATALOG))
"""
import os

from fastapi import APIRouter, Header, HTTPException, Query

GPT_API_KEY = os.environ.get("GPT_API_KEY", "").strip()


def _check_key(x_api_key: str):
    if GPT_API_KEY and x_api_key != GPT_API_KEY:
        raise HTTPException(401, "مفتاح غير صالح / invalid API key")


def _flatten(catalog):
    """catalog -> (concepts_by_slug, ordered_list, concept->phet map)."""
    # concept slug -> PhET sim, via the projects that combine it
    phet_for = {}
    for pj in catalog.get("projects", []):
        for slug in pj.get("combines", []):
            phet_for.setdefault(slug, pj.get("phet"))

    by_slug, ordered = {}, []
    for ch in catalog["chapters"]:
        for ls in ch["lessons"]:
            for c in ls["concepts"]:
                rec = {
                    "slug": c["slug"],
                    "concept_ar": c["ar"],
                    "concept_en": c["en"],
                    "chapter": ch["id"],
                    "chapter_title_ar": ch["title_ar"],
                    "lesson": ls["id"],
                    "lesson_title_ar": ls["title_ar"],
                    "pages": c.get("pages", ""),
                    "status": c.get("status", ""),
                    "video_available": bool(c.get("video")),
                    "handoff_ar": c.get("handoff", ""),
                    "phet_sim": phet_for.get(c["slug"]),
                }
                by_slug[c["slug"]] = rec
                ordered.append(rec)
    return by_slug, ordered, phet_for


def make_router(catalog):
    by_slug, ordered, _ = _flatten(catalog)
    router = APIRouter(prefix="/gpt", tags=["gpt"])

    @router.get("/concepts", operation_id="listConcepts",
                summary="List every concept in the Physics 2 curriculum")
    async def list_concepts(x_api_key: str = Header(default="")):
        """Return all 26 concepts with their Arabic/English names, chapter,
        lesson, book pages, and whether an intuition video exists. Use this to
        browse the curriculum or map a topic to its concept slug."""
        _check_key(x_api_key)
        return {"count": len(ordered), "concepts": ordered}

    @router.get("/concepts/{slug}", operation_id="getConcept",
                summary="Get one concept by its slug")
    async def get_concept(slug: str, x_api_key: str = Header(default="")):
        """Full detail for a single concept: names, location in the book,
        the 'handoff' line that ends its intuition video, video availability,
        and the matching PhET simulation link when one exists."""
        _check_key(x_api_key)
        rec = by_slug.get(slug)
        if not rec:
            raise HTTPException(404, "لا يوجد مفهوم بهذا المعرّف / unknown slug")
        return rec

    @router.get("/search", operation_id="searchCurriculum",
                summary="Search concepts by Arabic or English keyword")
    async def search(q: str = Query(..., description="Arabic or English search term"),
                     x_api_key: str = Header(default="")):
        """Find concepts whose Arabic name, English name, or slug contains the
        query. Use this to locate the right concept for a student's question."""
        _check_key(x_api_key)
        ql = q.strip().lower()
        hits = [r for r in ordered
                if ql in r["concept_ar"].lower()
                or ql in r["concept_en"].lower()
                or ql in r["slug"].lower()
                or ql in r["lesson_title_ar"].lower()]
        return {"query": q, "count": len(hits), "concepts": hits}

    return router
