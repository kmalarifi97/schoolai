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

**The `text` field is the ENGLISH narration.** This pipeline's spoken track is
English (see the Audience note). `text` is what the TTS voices and what sets the
timing clock. The Arabic فصحى line is a *parallel subtitle track* — same beat
`id`, supplied in `narration_<slug>_ar.json`, not in this object. When authoring,
write the English narration here and provide the matching Arabic subtitle line
per beat alongside.

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

1. **Resume + earn the measurement** — open on the teaser's final image, then
   raise the *student's own* question — the one that makes measuring feel
   necessary. Do **not** announce the destination ("now let's measure," "into
   the lab"); that's the equation-mode version of reading the next slide aloud,
   and it leaves the student performing steps without knowing why. Instead
   surface the mystery the equation resolves — *"every planet has its own orbit
   and its own year; is that chaos, or is distance secretly tied to time?"* —
   and let the need to measure fall out of it. End on the question, not the
   instruction.
2. **What-can-we-measure beat** — name the handful of real, observable
   quantities before any symbol appears. Grounds the symbols in things.
3. **One beat per parameter** — *the core of the skill.* Introduce each symbol
   only after the thing it names is on screen, and say what it stands for in
   plain words. `r` is "how wide the orbit is," not "the radius variable." Then
   **vary it live** (see principle 2): drag the parameter up and down and let
   the object respond on screen, so the symbol is felt as a knob, not read as a
   label.
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
2. **Bind each parameter to a live behavior — make the symbol a knob.** A
   parameter only becomes meaningful when the student watches the object
   *respond* to it. Don't label `r` on a frozen orbit; **vary it** — drag `r`
   bigger and let the orbit balloon outward, smaller and let it shrink in. Turn
   the symbol up and down and animate what changes (bigger/smaller,
   faster/slower, stronger/weaker). This live mapping — symbol ↔ visible
   behavior — is the single highest-leverage move in an equation video, because
   it converts an arbitrary letter into a thing the student has *operated*. Put
   it in the `visual` field of every parameter beat: state the static label,
   then sweep the value and show the consequence.
3. **Operations carry meaning too.** Story the ratio, the power, the equals.
   "Cube vs. square" should land as *a specific lopsidedness the student can
   state* (double the distance and the year more-than-doubles), not as "raised
   to the third power." These are best shown the same way as principle 2 — by
   sweeping a value and watching the mismatch.
4. **Subscripts are instances, not decoration.** Bind them to concrete cases so
   the student stops reading them as noise.
5. **Build, don't present.** Assemble the equation live. A formula that appears
   whole reads as authority handed down; one that is constructed reads as
   something the student could have found.
6. **Honor the equation's epistemic status.** An *empirical* law (a pattern in
   data, like Kepler's 3rd) describes; it does not explain. You may borrow the
   teaser's intuition to make it *feel* inevitable — but don't claim the
   intuition *derives* it. Save the real "why" for the later *causal* equation
   (e.g. Newton's law deriving Kepler's), and say so honestly. Flag this
   distinction to the user when it applies.
7. **Link to the teaser explicitly.** Open and close on its image (the callback
   beat), and in the system mark the equation concept as building on the
   teaser (see below).

## Staging: split the frame, bind by color

Keep the **equation on one side and the world on the other**, both on screen at
once for the whole scene. The equation is not a payoff card revealed at the end;
it's a **scoreboard the student watches fill in**. The link between the two
halves is **color**: when you explain a parameter, highlight the symbol in the
equation *and* its referent in the world in the **same color** (e.g. red), at
the same moment. `r` turns red in the formula while the orbit's radius turns red
on the other side — together. When you sweep the knob (principle 2), both red
elements move in step. When you compare two cases, give each case its own tint
(A blue, B green) and carry that tint into the subscripts. This synchronized,
persistent highlight is what makes *"this symbol is that thing"* unmissable —
much stronger than a label or an arrow. State the layout (which side holds what)
and the matched color in the `visual` field of every parameter beat.

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
  { "id": "s2_b1", "text": "Last time, you saw planets slide into their orbits, down the bend in space. But look closer. Every planet keeps its own orbit, its own year. Mercury races in close. Neptune crawls far out. Is that just chaos — or is distance secretly setting the year?", "visual": "Resume the teaser's curved-space bend. Several planets orbit — inner ones fast and tight, outer ones slow and wide. A question mark, then the frame splits: planets LEFT, a blank equation frame fading in on the RIGHT (the rule we're hunting)." },
  { "id": "s2_b3", "text": "Start with what you can measure. How far the planet sits from the sun. Call it r — the size of the orbit itself.", "visual": "LEFT: a line from sun to planet. The line AND the r-slot in the RIGHT equation glow red together. Sweep r larger — the orbit balloons out, red line lengthening; smaller — it shrinks; the red r grows and shrinks in step." },
  { "id": "s2_b5", "text": "Now take two planets, not one. A and B. Not cryptic symbols — two worlds, held side by side. Earth and Mars.", "visual": "LEFT splits into two mini-systems: planet A (blue tint), planet B (green tint), each with its own r and T. The subscripts in the equation pick up the same tints." },
  { "id": "s2_b10", "text": "Why cubed, why squared? Double a planet's distance, and its year more than doubles. The exponents are exactly how much more.", "visual": "Sweep r ×2 on the LEFT: the orbit doubles (³ pulse on r) but the period stretches to ~2.8× (² pulse on T). The two reds grow at visibly different rates." },
  { "id": "s2_b11", "text": "Remember the bend. The farther out, the gentler the slope, the slower the roll. This equation is that bend — written in numbers.", "visual": "The RIGHT equation slides over the teaser's bend; a far planet rolls slowly down a gentle slope, a near one whips around a steep one." }
]
```

Note: `b1` resumes the teaser (no new hook); `b3`/`b5` story a parameter and a
subscript; `b10` stories the *operations* (cube vs. square as a felt mismatch);
`b11` is the callback. The full scene fills in the remaining parameters (`T`,
the two ratios) and the assemble beat between these.

## Audience note: narration is English, subtitles are Arabic

The spoken track for this library is **English** — OpenAI `gpt-4o-mini-tts`,
voice `onyx`, driven by a fixed voice-direction prompt (slow, "thinking out loud
across a kitchen table," curiosity-not-excitement). So a beat's **`text` field
is the English narration** that the TTS speaks and that sets the clock — write it
in that warm, patient, "you"-voice register, matching the teaser. The **Arabic
فصحى** version is a *separate, parallel subtitle track* (`narration_<slug>_ar.json`),
burned in as RTL subtitles timed to the English audio. So produce **two lines per
beat**: the English narration (the `text` field) and the matching Arabic فصحى
subtitle. Keep symbols and equations in standard Latin notation (r, T, θ, ω) in
both. (The فصحى rule governs the subtitles and the tutor chat, not the audio.)

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
