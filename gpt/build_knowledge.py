"""Export the curriculum + concept library into clean Markdown the Custom GPT
can ingest as Knowledge files. Source of truth stays in scripts/*.json — re-run
this whenever those change.

    python3 gpt/build_knowledge.py

Writes:
    gpt/knowledge/curriculum.md        chapters -> lessons (summary, objectives, key terms)
    gpt/knowledge/concept_library.md   one section per concept (ar/en, lesson, intuition script)
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = ROOT / "scripts"
OUT = pathlib.Path(__file__).resolve().parent / "knowledge"


def build_curriculum():
    d = json.load(open(S / "structure.json", encoding="utf-8"))
    b = d["book"]
    lines = [
        f"# {b['title_ar']}",
        f"_{b['title_en']} — {b['edition']} — {b['publisher']}_",
        "",
        f"إجمالي الصفحات: {b['total_pdf_pages']}. أرقام الصفحات هنا تطابق صفحات الكتاب المطبوع.",
        "",
        "هذا الملف هو خريطة المنهج: الفصول ثم الدروس مع الملخص والأهداف والمصطلحات.",
        "استشهد دائمًا بالفصل/الدرس ورقم الصفحة عند الإجابة.",
        "",
    ]
    for c in d["chapters"]:
        lines.append(f"## الفصل {c['id']}: {c['title_ar']} ({c['title_en']})")
        lines.append(f"الصفحات {c['start_page']}–{c['end_page']}")
        lines.append("")
        if c.get("summary"):
            lines.append(c["summary"])
            lines.append("")
        for term in c.get("key_terms", []):
            lines.append(f"- {term}")
        if c.get("key_terms"):
            lines.append("")
        for l in c.get("lessons", []):
            lines.append(f"### الدرس {l['id']}: {l['title_ar']} ({l['title_en']})")
            lines.append(f"الصفحات {l['start_page']}–{l['end_page']}")
            lines.append("")
            if l.get("summary"):
                lines.append(l["summary"])
                lines.append("")
            for obj in l.get("objectives", []):
                lines.append(f"- هدف: {obj}")
            for term in l.get("key_terms", []):
                lines.append(f"- مصطلح: {term}")
            lines.append("")
    return "\n".join(lines)


def build_concepts():
    d = json.load(open(S / "concept_library_beats_v2.json", encoding="utf-8"))
    lines = [
        f"# {d['library']}",
        "",
        "## فلسفة الشرح",
        d.get("model", ""),
        "",
        f"النبرة: {d.get('tone','')}",
        "",
        "كل مفهوم له فيديو حدسي قصير يبني الفكرة ويتوقف قبل الجبر؛ الطالب يحلّ المعادلات بنفسه.",
        "النصوص أدناه هي 'نص الحدس' لكل مفهوم — استخدمها لتشرح بنفس الروح، ولا تحوّلها إلى مسائل محلولة.",
        "",
    ]
    for c in d["concepts"]:
        lines.append(f"## [{c['order']:02d}] {c['concept_ar']}")
        lines.append(f"_{c['concept_en']}_")
        lines.append(
            f"الفصل {c['chapter']} · الدرس {c['lesson']} · slug: `{c['slug']}` · "
            f"الحالة: {c['status']}"
        )
        lines.append("")
        if c.get("beats"):
            lines.append("نص الحدس (كما يُروى في الفيديو):")
            lines.append("")
            for beat in c["beats"]:
                txt = beat.get("text", "").strip()
                if txt:
                    lines.append(f"> {txt}")
            lines.append("")
        else:
            lines.append("_(الفيديو قيد الإعداد — اشرح المفهوم بنفس الفلسفة الحدسية.)_")
            lines.append("")
    return "\n".join(lines)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "curriculum.md").write_text(build_curriculum(), encoding="utf-8")
    (OUT / "concept_library.md").write_text(build_concepts(), encoding="utf-8")
    for f in sorted(OUT.glob("*.md")):
        print(f"wrote {f.relative_to(ROOT)}  ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
