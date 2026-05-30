"""Read-only, GPT-facing API for the Custom GPT Action.

These endpoints expose curriculum *metadata* only (concept names, lessons,
pages, PhET links) — never the gated mp4/PDF streams. They are safe to call
without a user login. Optional shared-secret guard via the GPT_API_KEY env var
(sent by the Action as the `X-API-Key` header); if unset, endpoints are open.

Mounted by app.py:  app.include_router(make_router(CATALOG))
"""
import json
import os
import pathlib
import sys
import time

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

GPT_API_KEY = os.environ.get("GPT_API_KEY", "").strip()

# The diagnostic spine (KST engine) lives in the repo, mounted at LIB_ROOT in
# Docker. Import the pure engine from there; it has stdlib-only dependencies.
LIB_ROOT = pathlib.Path(os.environ.get("LIB_ROOT")
                        or pathlib.Path(__file__).resolve().parents[2])
_SPINE_DIR = LIB_ROOT / "spine"
if str(_SPINE_DIR) not in sys.path:
    sys.path.insert(0, str(_SPINE_DIR))

try:
    import diagnose as _spine          # noqa: E402  spine/diagnose.py
    _SPINE_OK = True
except Exception as _e:                # spine not present -> diagnose route 503s
    _spine = None
    _SPINE_OK = False
    _SPINE_ERR = str(_e)

# Response log: seed of real calibration data. The repo mount is read-only, so
# default to a writable path and degrade gracefully rather than 500.
_RESPONSES_LOG = pathlib.Path(
    os.environ.get("SPINE_RESPONSES") or "/tmp/spine_responses.jsonl"
)


def _log_responses(student_id, responses):
    """Append (student_id, item_id, correct, ts) rows. Returns count or -1."""
    ts = time.time()
    try:
        _RESPONSES_LOG.parent.mkdir(parents=True, exist_ok=True)
        with _RESPONSES_LOG.open("a") as f:
            for r in responses:
                f.write(json.dumps({
                    "student_id": student_id, "item_id": r.get("item_id"),
                    "correct": bool(r.get("correct")), "ts": ts,
                }, ensure_ascii=False) + "\n")
        return len(responses)
    except OSError:
        return -1  # read-only / unwritable; diagnosis still returned


class _Response(BaseModel):
    item_id: str
    correct: bool


class _DiagnoseBody(BaseModel):
    student_id: str = "anon"
    responses: list[_Response] = []


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

    @router.post("/diagnose", operation_id="diagnoseGap",
                 summary="Diagnose the student's knowledge gap from their answers")
    async def diagnose_gap(body: _DiagnoseBody, x_api_key: str = Header(default="")):
        """Run the KST diagnostic engine on a student's item responses and return
        the located gap: the concept to teach next, its slug, lesson, and book
        pages. Call this at session start or on a topic request, then teach the
        returned lesson from the book — diagnosis chooses WHAT to teach, replacing
        table-of-contents order. Body: {student_id, responses:[{item_id,correct}]}.
        """
        _check_key(x_api_key)
        if not _SPINE_OK:
            raise HTTPException(503, f"diagnostic spine unavailable: {_SPINE_ERR}")
        resp = [r.model_dump() for r in body.responses]
        logged = _log_responses(body.student_id, resp)
        result = _spine.diagnose(resp, root=str(LIB_ROOT))
        result["logged"] = logged if logged >= 0 else False
        return result

    @router.post("/next-item", operation_id="nextItem",
                 summary="Pick the single most informative next item to ask")
    async def next_item(body: _DiagnoseBody, x_api_key: str = Header(default="")):
        """Adaptive questioning (KST half-split rule): given the answers so far,
        return the single most informative item to ask next, so the tutor can
        narrow the gap one question at a time instead of a fixed batch."""
        _check_key(x_api_key)
        if not _SPINE_OK:
            raise HTTPException(503, f"diagnostic spine unavailable: {_SPINE_ERR}")
        resp = [r.model_dump() for r in body.responses]
        return {"next_item": _spine.next_item_for(resp, root=str(LIB_ROOT))}

    return router
