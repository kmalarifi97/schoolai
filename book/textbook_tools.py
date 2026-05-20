"""Textbook tools: chapters, lessons, individual pages, and chapter
opener illustrations."""

from __future__ import annotations

import os
from typing import Any

from mcp.types import CallToolResult

from .. import auth, book_catalog, responses


def _base_url() -> str:
    base = os.environ.get("PUBLIC_BASE_URL")
    if base:
        return base.rstrip("/")
    host = os.environ.get("HOST", "127.0.0.1")
    port = os.environ.get("PORT", "8000")
    if host in ("0.0.0.0", "::"):
        host = "127.0.0.1"
    return f"http://{host}:{port}"


def _page_url(page_number: int) -> str:
    return auth.with_token(f"{_base_url()}/pages/{page_number}.pdf")


def _opener_url(filename: str) -> str:
    return auth.with_token(f"{_base_url()}/openers/{filename}")


def _chapter_summary(chap: dict[str, Any]) -> dict[str, Any]:
    opener = book_catalog.opener_for_chapter(chap["id"])
    return {
        "id": chap["id"],
        "title_ar": chap.get("title_ar"),
        "title_en": chap.get("title_en"),
        "summary_ar": chap.get("summary"),
        "start_page": chap.get("start_page"),
        "end_page": chap.get("end_page"),
        "key_terms": chap.get("key_terms", []),
        "lesson_count": len(chap.get("lessons") or []),
        "opener_url": _opener_url(opener.filename) if opener else None,
        "first_page_url": _page_url(chap["start_page"]) if chap.get("start_page") else None,
    }


def _lesson_summary(chap: dict[str, Any], lesson: dict[str, Any]) -> dict[str, Any]:
    start = lesson.get("start_page")
    end = lesson.get("end_page")
    pages = []
    if start and end:
        for p in range(start, min(end, start + 3) + 1):
            pages.append({"page_number": p, "primary_url": _page_url(p)})
    return {
        "id": lesson.get("id"),
        "title_ar": lesson.get("title_ar"),
        "title_en": lesson.get("title_en"),
        "summary_ar": lesson.get("summary"),
        "objectives": lesson.get("objectives", []),
        "key_terms": lesson.get("key_terms", []),
        "start_page": start,
        "end_page": end,
        "page_count": (end - start + 1) if (start and end) else None,
        "first_pages": pages,
        "chapter_id": chap["id"],
        "chapter_title_ar": chap.get("title_ar"),
        "chapter_title_en": chap.get("title_en"),
    }


# ---------------------------------------------------------------------------
# Tools.
# ---------------------------------------------------------------------------

def list_chapters() -> CallToolResult:
    chs = book_catalog.chapters()
    payload = {
        "render_as": "chapter_list",
        "count": len(chs),
        "book": book_catalog.book_metadata(),
        "chapters": [_chapter_summary(c) for c in chs],
    }
    return responses.widget_result(payload)


def get_chapter(chapter_id: int) -> CallToolResult:
    chap = book_catalog.get_chapter(int(chapter_id))
    if not chap:
        return responses.widget_result(
            responses.error(
                f"No chapter with id {chapter_id}. "
                f"Valid ids: 1..{len(book_catalog.chapters())}.",
                code="chapter_not_found",
            ),
            is_error=True,
        )
    payload = _chapter_summary(chap)
    payload.update(
        {
            "render_as": "chapter_detail",
            "lessons": [
                _lesson_summary(chap, L) for L in chap.get("lessons") or []
            ],
        }
    )
    return responses.widget_result(payload)


def get_lesson(lesson_id: str) -> CallToolResult:
    pair = book_catalog.get_lesson(str(lesson_id))
    if not pair:
        return responses.widget_result(
            responses.error(
                f"No lesson with id '{lesson_id}'. "
                "Lesson ids look like '1-1', '2-3'.",
                code="lesson_not_found",
            ),
            is_error=True,
        )
    chap, lesson = pair
    payload = _lesson_summary(chap, lesson)
    payload["render_as"] = "lesson_summary"
    return responses.widget_result(payload)


def get_page(page_number: int) -> CallToolResult:
    try:
        n = int(page_number)
    except (TypeError, ValueError):
        return responses.widget_result(
            responses.error("page_number must be an integer.", code="bad_request"),
            is_error=True,
        )
    book = book_catalog.book_metadata()
    total = int(book.get("total_pdf_pages") or 242)
    if not (1 <= n <= total):
        return responses.widget_result(
            responses.error(
                f"page_number out of range (1..{total}).",
                code="page_out_of_range",
            ),
            is_error=True,
        )
    # Identify chapter/lesson context.
    chap_id = None
    lesson_id = None
    chap_title_ar = None
    lesson_title_ar = None
    for c in book_catalog.chapters():
        if c.get("start_page", 0) <= n <= c.get("end_page", 0):
            chap_id = c["id"]
            chap_title_ar = c.get("title_ar")
            for L in c.get("lessons") or []:
                if L.get("start_page", 0) <= n <= L.get("end_page", 0):
                    lesson_id = L.get("id")
                    lesson_title_ar = L.get("title_ar")
                    break
            break

    path = book_catalog.page_pdf_path(n)
    payload = {
        "render_as": "page_card",
        "page_number": n,
        "title_ar": f"صفحة {n}",
        "primary_url": _page_url(n),
        "content_type": "application/pdf",
        "chapter_id": chap_id,
        "chapter_title_ar": chap_title_ar,
        "lesson_id": lesson_id,
        "lesson_title_ar": lesson_title_ar,
        "available": path.exists(),
    }
    return responses.widget_result(payload)


def get_chapter_opener(chapter_id: int) -> CallToolResult:
    try:
        cid = int(chapter_id)
    except (TypeError, ValueError):
        return responses.widget_result(
            responses.error("chapter_id must be an integer.", code="bad_request"),
            is_error=True,
        )
    chap = book_catalog.get_chapter(cid)
    if not chap:
        return responses.widget_result(
            responses.error(
                f"No chapter with id {cid}.", code="chapter_not_found"
            ),
            is_error=True,
        )
    opener = book_catalog.opener_for_chapter(cid)
    if not opener:
        return responses.widget_result(
            responses.error(
                f"No opener image available for chapter {cid}. "
                "Mount /content with the openers/ directory to enable.",
                code="opener_missing",
            ),
            is_error=True,
        )
    payload = {
        "render_as": "image_card",
        "title_ar": f"افتتاحية الفصل {cid} — {chap.get('title_ar')}",
        "title_en": chap.get("title_en"),
        "primary_url": _opener_url(opener.filename),
        "content_type": "image/jpeg",
        "chapter_id": cid,
        "page_number": opener.page_number,
    }
    return responses.widget_result(payload)
