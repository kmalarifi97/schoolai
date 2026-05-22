---
name: equation-storyboard
description: >-
  Design the script + visual beats for an EQUATION explainer video — the
  equation-mode counterpart to the concept-mode `lesson-storyboard` skill, for
  the same Manim/TTS pipeline. Use this whenever the lesson centers on a
  formula and the goal is to "story" the equation and each of its parameters so
  the symbols stop feeling like weird codes (what does r mean, why a subscript
  A, why cubed, what is the ratio saying). Trigger on: writing beats/narration
  for an equation or formula, "explain this equation," "story the parameters,"
  breaking a formula into an explainer video, or continuing a concept/teaser
  video into the quantitative part. Especially use this when the equation video
  should build on an earlier intuition/teaser video rather than stand alone —
  even if the user just says "now do the equation" after a concept storyboard.
  For pure intuition videos with no equation, use `lesson-storyboard` instead.
---

# Equation Storyboard

This is the **equation-mode** sibling of `lesson-storyboard`. Both feed the same
pipeline (script → TTS → Manim → composite) and share the same beat schema and
beat-level writing rules. The difference is structural, and it matters:

- **`lesson-storyboard` (concept mode)** builds intuition from nothing: open on
  the smallest version of the phenomenon, earn the question, bridge by analogy,
  callback. It is a *standalone* dramatic arc.
- **`equation-storyboard` (this skill)** does **not** rebuild that arc. An
  equation video is a **continuation** — "taking the teaser into the
  laboratory." The student already *felt* the idea in a concept/teaser video;
  now you walk them up to the workbench to *measure* it. So the equation
  storyboard opens on the teaser's closing image and resolves back to it.

If you try to force the concept-mode dramatic opening onto an equation, you get
a weaker remake of the teaser. Don't. Resume, don't restart.

## The core mental model: an equation describes; intuition explains

A formula tells you *how much*, never *why*. The "why" lives in the prior
concept video. So the equation storyboard's job is not to motivate the
phenomenon (already done) — it is to make every symbol **mean something the
student can picture**, and to show how the symbols lock together into the rule.
The win condition: by the last beat, the student can look at the bare equation
and narrate it back in plain words.

## Schema (identical to lesson-storyboard)

Output is a JSON array, one object per beat:

```json
{
  "id": "s2_b1",
  "text": "What the narrator says — one breath, 1–3 short conversational sentences.",
  "visual": "Plain-language on-screen description for the Manim agent — concrete objects, motions, positions."
}
```

Use the scene index to signal continuation: if the teaser was scene 1, the
equation scene is **`s2_*`**. This is a real cue, not cosmetic — it tells the
downstream agents (and the human) that this clip plays *after* the teaser.

## What this skill keeps from lesson-storyboard

The beat-level writing rules are the same and still govern every `text` field:

- **Concrete openings**, the **"you" voice**, **one new element per beat**,
  **short sentences**, conversational-not-casual, and **no textbook voice**.
- **The closing callback** (concept mode's principle 5) is still mandatory —
  here it's how you re-link to the teaser.

Read `lesson-storyboard`'s beat-level rules if you need them in full; they are
not repeated here.

## What this skill drops, and why

- **No new hook beat.** Concept mode opens on the smallest version of the law to
  break a scale assumption. The equation video skips this — the hook already
  happened. Opening with another dramatic cold-open competes with the teaser
  and wastes the student's attention. Start by *resuming*.
- **No "earn the phenomenon."** The student already wants this. You only need to
  earn the *measurement* ("feeling it isn't enough — let's measure it").

## Equation-mode structure (the beats that should be present)

Not a rigid template, but an equation storyboard usually needs these, roughly in
order. The middle (one beat per parameter) is the heart.

1. **Resume beat** — open on the teaser's final image; pivot from *feeling* to
   *measuring*. ("You felt why it happens. Feeling isn't enough. Into the lab.")
2. **What-can-we-measure beat** — name the handful of real, observable
   quantities before any symbol appears. Grounds the symbols in things.
3. **One beat per parameter** — *the core of the skill.* Introduce each symbol
   only after the thing it names is on screen, and say what it stands for in
   plain words. `r` is "how wide the orbit is," not "the radius variable."
4. **Demystify subscripts/indices** — `A` and `B` aren't arcana; they're "two
   real worlds you're holding side by side." Make them concrete (Earth, Mars).
5. **Story the operations, not just the letters** — a ratio is "how many times
   bigger"; an exponent is a *rhythm* or *mismatch*, not decoration. This is
   where most equation explainers fail: they read the letters and ignore the
   `³`, the `/`, the `=`.
6. **Assemble beat** — build the equation piece by piece on screen and let the
   `=` snap shut. Don't present the finished formula and then dissect it;
   construct it so the student watches it cohere.
7. **Callback beat** — return to the teaser's image with the equation overlaid:
   *"this equation is that bend, written in numbers."*
8. **Landing beat** — recap each symbol in one line so the bare equation is now
   readable: "r = orbit width, T = the planet's year, A and B = two worlds, the
   exponents = the rhythm."

## Principles specific to equations

1. **A symbol is a nickname, not a code.** Always say the plain-word meaning
   *before* using the letter, and ideally show the thing first. The student
   should never meet `T` as "T"; they meet "the planet's year," which we'll
   *call* `T`.
2. **Operations carry meaning too.** Story the ratio, the power, the equals.
   "Cube vs. square" should land as *a specific lopsidedness the student can
   state* (double the distance and the year more-than-doubles), not as "raised
   to the third power."
3. **Subscripts are instances, not decoration.** Bind them to concrete cases so
   the student stops reading them as noise.
4. **Build, don't present.** Assemble the equation live. A formula that appears
   whole reads as authority handed down; one that is constructed reads as
   something the student could have found.
5. **Honor the equation's epistemic status.** An *empirical* law (a pattern in
   data, like Kepler's 3rd) describes; it does not explain. You may borrow the
   teaser's intuition to make it *feel* inevitable — but don't claim the
   intuition *derives* it. Save the real "why" for the later *causal* equation
   (e.g. Newton's law deriving Kepler's), and say so honestly. Flag this
   distinction to the user when it applies.
6. **Link to the teaser explicitly.** Open and close on its image (principle 7
   above), and in the system mark the equation concept as building on the
   teaser (see below).

## System linking (this pipeline)

The equation scene is bound to its teaser, not free-floating:

- Mark the equation concept `builds_on: "<teaser-slug>"` in the data so the
  copilot's flow is **show teaser → walk the equation beats → state it formally
  from the book → homework.**
- **A new render may not be needed.** Because the beats are a tutor-readable
  script, the copilot can *narrate* them right after playing the teaser, with no
  separate Manim render. The teaser stays the only video; the equation "lab" is
  guided narration linked to it. (If a render is wanted later, the beats are
  already render-ready — that's the point of keeping the schema identical.)

## Worked example — Kepler's 3rd, "into the laboratory"

Equation: $\left(\frac{r_A}{r_B}\right)^3 = \left(\frac{T_A}{T_B}\right)^2$, as a
continuation of a "what is gravity / spacetime" teaser.

```json
[
  { "id": "s2_b1", "text": "في الفيديو السابق شعرتَ لماذا تدور الكواكب: الكتلة تُحني الفضاء، فتنزلق الأجسام في مداراتها. لكنّ الشعور وحده لا يكفي. هيّا إلى المختبر.", "visual": "The curved-space bend from the teaser's final shot. Camera pulls back through it into an old observatory: telescope, a notebook of numbers." },
  { "id": "s2_b3", "text": "الأوّل: بُعد الكوكب عن الشمس. نسمّيه r، نصف قطر المدار — ببساطة: ما اتّساع الدائرة التي يرسمها الكوكب.", "visual": "A line stretches from the sun to the planet, labeled r. The orbit circle glows." },
  { "id": "s2_b5", "text": "أمّا A وB فليسا رمزين غامضين؛ هما كوكبان نضع أحدهما بجانب الآخر لنقارن — كالأرض والمرّيخ.", "visual": "Two planets appear side by side, tagged A and B." },
  { "id": "s2_b10", "text": "ضاعِف بُعد الكوكب، فلن تتضاعف سنته. بل تطول أكثر. الأُسّان 3 و2 هما اللذان يضبطان هذا التفاوت بدقّة.", "visual": "Distance doubles (×2) with a «³» pulse; the period stretches by ~2.8× with a «²» pulse, numbers shown." },
  { "id": "s2_b11", "text": "تذكّر انحناء الفضاء: كلّما ابتعد الكوكب، لان المنحدر، فتمهّل دورانه. هذه المعادلة هي ذلك المنحدر، مكتوبًا بالأرقام.", "visual": "Return to the teaser's bend: a far planet rolls slowly down a gentle slope, a near one whips around a steep one." }
]
```

Note: `b1` resumes the teaser (no new hook); `b3`/`b5` story a parameter and a
subscript; `b10` stories the *operations* (cube vs. square as a felt mismatch);
`b11` is the callback. The full scene fills in the remaining parameters (`T`,
the two ratios) and the assemble beat between these.

## Audience note

Default to **Arabic فصحى (MSA)** for the narration `text` (Saudi grade-11
Physics 2). Keep symbols and equations in the usual Latin/standard notation
(r, T, θ, ω). If the equation video continues an existing teaser, ask whether to
match the teaser's language for seamless continuity.

## What to hand the user

1. A short paragraph (3–6 sentences) on the structural choices: what the
   equation is *about*, which teaser it resumes, how each parameter is storied,
   and — if it's an empirical law — an honesty flag about description vs.
   explanation (principle 5).
2. The storyboard JSON array.
3. A one-line offer: wire it into the data (`builds_on`), write the next
   equation, or revise this one.

Build scene by scene for multi-equation lessons; the per-equation review is
where the editorial work happens.
