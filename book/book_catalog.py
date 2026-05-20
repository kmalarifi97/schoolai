"""Textbook catalog: loads structure.json (chapters → lessons) and
resolves on-disk paths for per-page PDFs and chapter-opener JPGs.

Structure of the Saudi Year-2 secondary physics textbook (6 chapters,
13 lessons, pp 1–242). The taxonomy lives in `structure.json` (in
git); the page renders and opener images come from the `/content`
runtime mount (gitignored binaries).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

CONTENT_ROOT = Path(os.environ.get("CONTENT_ROOT", "/content"))
BAKED_CONTENT_ROOT = Path("/app/baked_content")

PAGES_DIR = CONTENT_ROOT / "pages"
OPENERS_DIR = CONTENT_ROOT / "openers"
TOC_DIR = CONTENT_ROOT / "toc_preview"


def _find_structure() -> Path:
    for root in (BAKED_CONTENT_ROOT, CONTENT_ROOT):
        p = root / "structure.json"
        if p.exists():
            return p
    return BAKED_CONTENT_ROOT / "structure.json"


@lru_cache(maxsize=1)
def structure() -> dict[str, Any]:
    return json.loads(_find_structure().read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def chapters() -> list[dict[str, Any]]:
    return list(structure().get("chapters") or [])


def get_chapter(chapter_id: int) -> dict[str, Any] | None:
    for c in chapters():
        if c["id"] == chapter_id:
            return c
    return None


def get_lesson(lesson_id: str) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Return `(chapter, lesson)` for the given lesson id (e.g. '1-1'),
    or None if not found."""
    for c in chapters():
        for L in c.get("lessons") or []:
            if L.get("id") == lesson_id:
                return c, L
    return None


@dataclass(frozen=True)
class OpenerCandidate:
    path: Path
    page_number: int

    @property
    def filename(self) -> str:
        return self.path.name


@lru_cache(maxsize=1)
def all_openers() -> list[OpenerCandidate]:
    """Discover the chapter opener JPGs (filenames look like
    `p008-1.jpg`). Sorted by page number."""
    out: list[OpenerCandidate] = []
    if not OPENERS_DIR.exists():
        return out
    for p in OPENERS_DIR.glob("p*.jpg"):
        m = re.match(r"p(\d+)", p.stem)
        if not m:
            continue
        out.append(OpenerCandidate(path=p, page_number=int(m.group(1))))
    return sorted(out, key=lambda o: o.page_number)


def opener_for_chapter(chapter_id: int) -> OpenerCandidate | None:
    """Pick the opener image whose page sits within (or closest to)
    the chapter's start_page."""
    chap = get_chapter(chapter_id)
    if not chap:
        return None
    openers = all_openers()
    if not openers:
        return None
    start = chap["start_page"]
    end = chap.get("end_page", start)
    # First, an opener at or just after start_page
    for o in openers:
        if start <= o.page_number <= end:
            return o
    return min(openers, key=lambda o: abs(o.page_number - start))


def page_pdf_path(page_number: int) -> Path:
    return PAGES_DIR / f"page_{page_number:03d}.pdf"


def opener_jpg_path(filename: str) -> Path:
    # Defensive: only accept names matching the known pattern.
    if not re.fullmatch(r"p\d{3}-\d+\.jpg", filename):
        raise ValueError(f"unsafe opener filename: {filename!r}")
    return OPENERS_DIR / filename


def book_metadata() -> dict[str, Any]:
    return structure().get("book") or {}
