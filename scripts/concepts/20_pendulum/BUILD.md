# Build brief — Concept 20: Conservation of Mechanical Energy

**Arabic:** حفظ الطاقة الميكانيكية
**Status:** shipped  |  **Beats:** n/a (shipped — reuse existing)

## Book grounding
- Book: Physics 2 - Secondary Education - Pathways System - Year 2 (1447 / 2025)
- Chapter 5 — Energy and Its Conservation / الطاقة وحفظها
- Lesson 5-2 — Conservation of Energy / حفظ الطاقة
- **PDF pages: 141–163** in `../../../book/فيزياء ثاني ثنوي.pdf` (PDF page == printed page)
- Read these pages first. The video introduces the concept; it must stay faithful to how the book frames it. It must NOT solve the book's problems — students do that.

### Lesson objectives (from the book)
- حل مسائل باستخدام قانون حفظ الطاقة
- تحليل التصادمات لإيجاد التغير في الطاقة الحركية

### Key terms to honor
- قانون حفظ الطاقة
- الطاقة الميكانيكية
- التصادم فوق المرن
- التصادم المرن
- التصادم العديم المرونة

## What to build
- One short concept-spark video: `pendulum_full_voiced_subs.mp4`
- Beats are in `pendulum.json` → `beats[]` (id / text / visual). English narration, Arabic subs burned in, pure #000000 void.
- `[Hold Ns in silence]` markers in a beat's visual mean exactly that: hold the frame, no narration.
- Pipeline + conventions: `manim/CLAUDE.md` (Standard pipeline section). Slug = `pendulum`.
- This concept is already shipped — video copied into this directory; rebuild only if asked.

## Hand-off contract
Deliver `pendulum_full_voiced_subs.mp4` in this directory. Tone is non-negotiable: silence is content, kitchen-table-warm, concept before equations, no worked problems, no hype.
