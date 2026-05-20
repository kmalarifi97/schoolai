# Build brief — Concept 01: Kepler's Laws → Newton's Universal Gravitation

**Arabic:** قوانين كبلر وقانون الجذب الكوني
**Status:** shipped-external  |  **Beats:** n/a (shipped — reuse existing)

## Book grounding
- Book: Physics 2 - Secondary Education - Pathways System - Year 2 (1447 / 2025)
- Chapter 1 — Gravitation / الجاذبية
- Lesson 1-1 — Planetary Motion and Gravitation / حركة الكواكب والجاذبية
- **PDF pages: 9–17** in `../../../book/فيزياء ثاني ثنوي.pdf` (PDF page == printed page)
- Read these pages first. The video introduces the concept; it must stay faithful to how the book frames it. It must NOT solve the book's problems — students do that.

### Lesson objectives (from the book)
- الربط بين قوانين كبلر وقانون الجذب الكوني
- حساب الزمن الدوري ومقدار السرعة المدارية
- وصف أهمية تجربة كافندش

### Key terms to honor
- القانون الأول لكبلر
- القانون الثاني لكبلر
- القانون الثالث لكبلر
- قوة الجاذبية
- قانون الجذب الكوني (العام)

## What to build
- One short concept-spark video: `gravitation_full_voiced_subs.mp4`
- Beats are in `gravitation.json` → `beats[]` (id / text / visual). English narration, Arabic subs burned in, pure #000000 void.
- `[Hold Ns in silence]` markers in a beat's visual mean exactly that: hold the frame, no narration.
- Pipeline + conventions: `manim/CLAUDE.md` (Standard pipeline section). Slug = `gravitation`.
- Video shipped externally; pull in / re-derive only if asked.

## Hand-off contract
Deliver `gravitation_full_voiced_subs.mp4` in this directory. Tone is non-negotiable: silence is content, kitchen-table-warm, concept before equations, no worked problems, no hype.
