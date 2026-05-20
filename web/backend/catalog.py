"""Build the library catalog (chapters → lessons → concept videos, + projects)
from the existing JSON manifests. Resolves slug → mp4 path. No copying."""
import json, glob, os, pathlib

# LIB_ROOT lets Docker mount the repo at an arbitrary path (e.g. /lib).
ROOT = pathlib.Path(os.environ.get("LIB_ROOT")
                    or pathlib.Path(__file__).resolve().parents[2])
S = ROOT / "scripts"

PHET = {
    "skatepark": "https://phet.colorado.edu/en/simulations/energy-skate-park-basics",
    "collisionlab": "https://phet.colorado.edu/en/simulations/collision-lab",
    "orbitlab": "https://phet.colorado.edu/en/simulations/gravity-and-orbits",
    "balancerig": "https://phet.colorado.edu/en/simulations/balancing-act",
    "springdrop": "https://phet.colorado.edu/en/simulations/masses-and-springs",
    "thermalbudget": "https://phet.colorado.edu/en/simulations/energy-forms-and-changes",
}

_video_index = {}   # ("concept"|"project", slug) -> absolute mp4 path


def _first(pattern):
    f = sorted(glob.glob(pattern))
    return f[0] if f else None


def build():
    """Return (catalog_dict, video_index)."""
    struct = json.load(open(S / "structure.json"))
    v2 = json.load(open(S / "concept_library_beats_v2.json"))
    idx = {c["slug"]: c for c in json.load(open(S / "concepts/INDEX.json"))["concepts"]}
    book = struct["book"]

    lessons_meta = {}
    for ch in struct["chapters"]:
        for ls in ch.get("lessons", []):
            lessons_meta[ls["id"]] = ls

    # concepts grouped chapter -> lesson
    grouped = {}
    for c in v2["concepts"]:
        slug = c["slug"]
        nn = idx.get(slug, {})
        dname = pathlib.Path(nn.get("dir", "")).name
        mp4 = _first(str(S / "concepts" / dname / f"{slug}_full_voiced_subs.mp4")) if dname else None
        if mp4:
            _video_index[("concept", slug)] = mp4
        grouped.setdefault(c["chapter"], {}).setdefault(c["lesson"], []).append({
            "slug": slug,
            "ar": c["concept_ar"],
            "en": c["concept_en"],
            "pages": nn.get("book_pages", ""),
            "handoff": c["beats"][-1]["text"] if c.get("beats") else "",
            "status": c["status"],
            "video": bool(mp4),
        })

    chapters = []
    for ch in struct["chapters"]:
        cid = ch["id"]
        if cid not in grouped:
            continue
        lessons = []
        for lid, items in sorted(grouped[cid].items()):
            lm = lessons_meta.get(lid, {})
            lessons.append({
                "id": lid,
                "title_ar": lm.get("title_ar", ""),
                "title_en": lm.get("title_en", ""),
                "start_page": lm.get("start_page"),
                "end_page": lm.get("end_page"),
                "concepts": items,
            })
        chapters.append({
            "id": cid,
            "title_ar": ch["title_ar"],
            "title_en": ch["title_en"],
            "lessons": lessons,
        })

    # concept slug -> chapter (to dock projects onto the book)
    concept_chapter = {c["slug"]: c["chapter"] for c in v2["concepts"]}

    projects = []
    for pj in sorted(glob.glob(str(S / "projects/*/*.json"))):
        d = json.load(open(pj))
        slug = d["slug"]
        mp4 = _first(str(pathlib.Path(pj).parent / f"{slug}_full_voiced_subs.mp4"))
        if mp4:
            _video_index[("project", slug)] = mp4
        combined = d.get("concepts_combined", [])
        # chapter this project belongs to = chapter of its first combined concept
        first_slug = combined[0].split("(")[0].split("_", 1)[-1].strip() if combined else ""
        ch_for = concept_chapter.get(first_slug)
        projects.append({
            "slug": slug,
            "ar": d.get("project_ar", ""),
            "en": d.get("project_en", ""),
            "persona": d.get("persona", ""),
            "sim": d.get("phet_sim", "").split("(")[0].strip(),
            "phet": PHET.get(slug, "https://phet.colorado.edu"),
            "combines": [x.split("(")[0].split("_", 1)[-1].strip() for x in combined],
            "chapter": ch_for,
            "video": bool(mp4),
        })

    pdf = _first(str(ROOT / "book" / "*.pdf"))
    if pdf:
        _video_index[("book", "_")] = pdf

    catalog = {
        "book": {
            "title_ar": book["title_ar"], "title_en": book["title_en"],
            "edition": book["edition"], "publisher": book["publisher"],
            "pages": book["total_pdf_pages"],
            "has_pdf": bool(pdf),
            "page_note": book.get("notes", ""),
        },
        "chapters": chapters,
        "projects": projects,
        "counts": {
            "concepts": sum(len(l["concepts"]) for c in chapters for l in c["lessons"]),
            "projects": len(projects),
        },
    }
    return catalog, _video_index
