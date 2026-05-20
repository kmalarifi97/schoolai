# Gravity Series — Project Notes

This directory is a Manim animation pipeline for an explainer documentary about gravity. The current finished work is **Scene 1 (26 beats)** of the "gravity v2" script, delivered as `voice/gravity2_full_voiced.mp4` with English narration.

If you're a new Claude session reading this: the *what* is in the code, but the *why* and the *gotchas* are below. Read this first.

---

## Project layout

- `gravity2_s1b1.py` ... `gravity2_s1b26.py` — original (silent, with subtitles) beat-by-beat scripts. These were the v2 first pass; left in place for reference. Do NOT edit them for new work.
- `voice/scenes/b1.py` ... `b26.py` — **current canonical voiced beats**. Subtitles removed, durations locked to audio, uses `grav_helpers.py`. This is the working set.
- `voice/scenes/grav_helpers.py` — shared helpers (`make_rock`, `make_sun`, `make_fabric_3d`, `bowling_ball`, `make_earth`). New beats should import from here, not redefine.
- `voice/narration_en.json` / `voice/narration_ar.json` — narration text per beat keyed by id.
- `voice/generate_tts_en.py` / `voice/generate_tts.py` — OpenAI TTS callers. The English script holds the full voice-direction `instructions`.
- `voice/audio_en/` — final per-beat mp3s. `voice/audio/` was the Arabic experiment (scrapped, see below).
- `voice/voiced/voiced_b{N}.mp4` — per-beat video+audio muxed files.
- `voice/gravity2_full_voiced.mp4` — **archived on 2026-05-13** at `/Users/khalid-dev/school-ai/gravity2_full_voiced.mp4` (top level of `school-ai/`, sibling of `cars_full_voiced_subs.mp4`, `paperclip_full_voiced_subs.mp4`, `pendulum_full_voiced_subs.mp4`, `rocket_full_voiced.mp4`). **Each video in `school-ai/` has a sibling `.json` with the same basename containing the beat-by-beat script** (`[{"id": "s1_bN", "text": "...", "visual": "..."}, ...]`). When adding a new video here, drop the `.json` next to it. The gravity one is at `/Users/khalid-dev/school-ai/gravity2_full_voiced.json`.

`trig_relationships.py`, `water_cycle.py`, `scenes.py` — earlier unrelated demos. Untouched by Scene 1 work.

---

## Tone and visual contract (NOT obvious from code)

The voice script the user signed off on is in `voice/generate_tts_en.py` as the `INSTRUCTIONS` string. The core principle: **"silence is content."** Slow, kitchen-table-warm, curious-not-excited. Not announcer cadence, not documentary-narrator gravitas. Read that string before generating any new TTS — it's the audio's "design system."

Visual conventions across the series:
- Background: pure `#000000` ("VOID"). Don't change this — it's the project's signature.
- Rocks have fixed identities by seed: `seed=7` = big rock, `seed=13` = small rock. Reuse those seeds for callbacks (b1, b2, b4, b5, b8, b18, b25). The merged-clump rock is `seed=101`.
- Original rock positions: `BIG_POS = [-2.0, 0.50, 0]`, `SMALL_POS = [1.9, -0.35, 0]`. `SMALL_FINAL` (after b5 contact) = `BIG_POS - unit(BIG-SMALL) * 1.10`. These are sacred across beats.
- Solar-system view uses `[0,0,0]` as sun center. Planets in `PLANET_SPECS` are spread for visual balance, not astronomical accuracy.
- Font for any Text is `font="sans"`. Without this, Manim's default fallback collapses kerning (saw it as "upandrises" in earlier work).
- Subtitles are intentionally REMOVED from the voiced version. Voice carries the script. If a user asks to put them back, ask whether they want them; they were deliberately omitted to give visuals breathing room.

---

## TTS — what we learned the hard way

- **OpenAI TTS (`gpt-4o-mini-tts`) is excellent for English, mediocre for Arabic.** The voices were trained primarily on English; in Arabic they apply English intonation patterns to Arabic phonemes and sound robotic. Don't suggest OpenAI TTS for Arabic narration.
- **For Arabic, use Microsoft Edge TTS (`edge-tts` Python lib) — free, native Arabic neural voices** like `ar-SA-HamedNeural`, `ar-SA-ZariyahNeural`. We didn't end up using it (user switched to English) but it's the right call for any Arabic work.
- The `instructions` field on `gpt-4o-mini-tts` is powerful for English but caused the Arabic to insert awkward pauses ("trust the silence" was over-applied). Keep instructions language-aware if generating multiple languages.
- Audio durations for the current English narration are in `voice/durations_en.txt`. Re-measure with `av.open(path).duration / 1e6` if regenerating.

---

## Sync workflow (the order matters)

When updating narration or visuals, the dependency order is strict:

1. Edit `voice/narration_en.json`.
2. Regenerate TTS → `voice/audio_en/b{N}.mp3`.
3. **Measure each audio's duration first.** Then update the matching `voice/scenes/b{N}.py` so the beat's total runtime ≈ `audio_duration + 0.5` (tail buffer).
4. Re-render with Docker (`docker run --rm -v "$PWD":/manim manimcommunity/manim:stable manim -qm bN.py S1BN`). Working dir must be `voice/scenes/`.
5. Mux audio onto video with `jrottenberg/ffmpeg:latest` (manim image does NOT include ffmpeg; this caught us once).
6. Concat all 26 voiced clips → `gravity2_full_voiced.mp4`.

Never adjust video durations first and re-record audio to match — voice is the pacing driver, video flexes around it.

---

## Manim gotchas observed (these will bite again)

- `np.convolve(..., mode="wrap")` does NOT exist. The rock smoothing uses an explicit `(i-1)%n` / `(i+1)%n` rolling average. Don't "simplify" it back.
- `set_opacity(x)` on a closed `VMobject` (e.g. a `CurvedArrow`) fills it like a crescent. To dim a curve, use `set_fill(opacity=0).set_stroke(..., opacity=x)`. Bit us in `water_cycle.py`.
- `Text.to_edge(RIGHT)` clips long formulas. Use `mob.scale_to_fit_width(N).move_to([x, y, 0])` for anything formula-shaped.
- `ArcBetweenPoints(start, end, angle)`: negative `angle` curves clockwise from start→end. For a mug handle bulging right from a body's right edge: start at `body.get_right() + DOWN*0.38`, end at `body.get_right() + UP*0.38`, `angle=-PI*0.95`.
- LaTeX is available in `manimcommunity/manim:stable`, so `MathTex` works (used in b19).
- For animations on multiple mobjects in `self.play`, each gets its own `run_time` if specified; otherwise the play-level `run_time` applies to all.

---

## The 3D fabric (b20–b26)

The `make_fabric_3d` helper deliberately combines four cues for "this is a 3D gravity well, not a 2D bent grid":
1. **Strong trapezoidal perspective** — `top_w` much smaller than `bottom_w` (e.g. 3.0 vs 11.0).
2. **Latitude lines fade toward the back** — opacity ramps from 0.30 at top to 0.85 at bottom.
3. **Concentric foreshortened contour rings** around the dip (y-axis squashed to 0.32×) make the bowl read as a bowl. This is the single most important visual addition vs. the old flat-trapezoid grid.
4. **Gaussian dip** with `dip_depth ≈ 1.5` and `dip_width ≈ 1.55`. Going deeper than ~1.7 starts to clip the bottom of frame.

The user explicitly asked for "top and bottom" visibility of the gravity effect. The contour rings + perspective combo is what delivered that. Don't strip them down to "simplify."

---

## Docker setup — what runs where

This project uses Docker as a tool, not as a runtime. **The codebase is plain files on the host Mac at `/Users/khalid-dev/manim/`.** Containers are spun up on demand for tasks that need heavy dependencies (Manim, ffmpeg), then disposed (`--rm`). Nothing persists inside containers; everything is read/written through bind mounts.

### Runs on host (your Mac, no Docker)
- All Python scripts that call APIs or do file management: `voice/generate_tts_en.py`, `voice/generate_tts.py`, `voice/build_subtitles.py`. They use the host's Python 3 + `openai` library (`pip install --user openai`).
- All file editing, JSON reading, key/env management.

### Runs in Docker
- **Manim renders** → `manimcommunity/manim:stable`
  - Why containerized: Manim needs LaTeX, Cairo, OpenGL stack, fonts. We don't want those system-level on the Mac.
  - Pattern: `docker run --rm -v "$PWD":/manim manimcommunity/manim:stable manim -qm file.py SceneName`
  - Working dir must be the directory holding the `.py` file (e.g. `voice/scenes/`).
  - Output lands at `<cwd>/media/videos/<file_stem>/720p30/<SceneName>.mp4`.
  - The `-qm` flag = 720p @ 30fps medium quality. Use `-qh` for 1080p, `-qk` for 4k.
  - This image also has `pyav` (the `av` Python module), so it doubles as our frame-extraction container.
- **ffmpeg operations (mux audio, concat, burn subtitles)** → `jrottenberg/ffmpeg:latest`
  - Why a different image: the manim image does NOT have ffmpeg installed (confirmed). Don't try `--entrypoint ffmpeg` on it; it fails.
  - Pattern: `docker run --rm -v "$PWD":/work -v /tmp:/tmp jrottenberg/ffmpeg:latest -i /work/... -c copy /work/output.mp4`
  - Mount `/tmp` if your concat list file lives there.

### Pitfalls
- The Bash tool's `$PWD` resolves to the host's current dir. If you run a Docker command from the wrong directory, the bind mount won't include the files you need. **Always `cd` to the right directory first** (e.g. `cd /Users/khalid-dev/manim/voice/scenes` before rendering).
- Re-rendering is the slow step (~30s/beat × 26 = ~13 min). Mux + concat are seconds. So plan accordingly when iterating.
- `--rm` deletes the container after the run; don't expect state to carry over.

### Frame extraction shortcut
For quickly checking what a rendered frame looks like:
```bash
docker run --rm -v "$PWD":/manim --entrypoint python3 manimcommunity/manim:stable -c "
import av, pathlib
c = av.open('/manim/path/to.mp4')
frames = [f for f in c.decode(video=0)]; c.close()
frames[int(timestamp_sec * fps)].to_image().save('/manim/check.png')
"
```
Then `Read` the PNG. This is faster and more reliable than ffmpeg for single frames.

---

## User preferences observed in this session

- Wants the work to ship, not theorize. When given multiple options, picks one and moves. Don't over-explain trade-offs more than once.
- Prefers terse responses with a clear next step.
- Asked for visuals that "read at a glance" — strong perspective on the fabric, deep dips, no ambiguity about what's being shown.
- Removed subtitles in favor of voice. Voice IS the script.
- Iterates by saying `next` for incremental progress, `go` when ready for batch work. Respect the cadence they set in the moment.
- Uses both English and Arabic comfortably; will switch mid-conversation if a path isn't working.

---

## Standard pipeline for a new explainer (proven; do not reinvent)

This is the workflow validated by four scenes built after gravity2 (rocket, pendulum, cars, paperclip — Newton's 3rd, energy conservation, kinetic energy, E=mc²). Treat it as the default for any new explainer the user pastes a JSON storyboard for. Don't redesign it; tighten it.

### Naming convention (per new scene)

Pick a short scene slug (`rocket`, `pendulum`, `cars`, etc.) and use it everywhere:

- `voice/narration_{slug}_en.json` — `{ "s1_b1": "...", ... }`. Beat ids match the user's storyboard JSON.
- `voice/narration_{slug}_ar.json` — Arabic translations, same keys. Same Gulf-leaning literary style as `narration_ar.json` (em-dashes for mid-thought pauses, short fragments, no formal MSA stiffness).
- `voice/scenes/{slug}_helpers.py` — visual primitives for *this scene only*. Don't pollute `grav_helpers.py`.
- `voice/scenes/{slug}_b{N}.py` — one Python file per beat, classes `{Slug}S1B{N}` (e.g. `RocketS1B1`, `PendulumS1B14`). Same import pattern as `voice/scenes/b1.py`. The N is 1-indexed and matches the JSON `s1_b{N}` key.
- `voice/scenes/render_all_{slug}.sh` — sequential Docker render of all beats, logs to `render_{slug}.log`.
- `voice/generate_tts_{slug}_en.py` — sibling of `generate_tts_en.py`, points at the new JSON + writes to `voice/audio_{slug}_en/`.
- `voice/scenes/mux_voiced_{slug}.sh` — measures durations, pads, writes to `voice/voiced_{slug}/voiced_{slug}_b{N}.mp4`, dumps `voice/durations_{slug}_en.txt`.
- `voice/build_subtitles_{slug}.py` — parallel of `build_subtitles.py`, parameterized for this slug. Writes `voice/subs_{slug}_ar.ass`.
- `voice/scenes/concat_burn_{slug}.sh` — concat the per-beat voiced mp4s then burn Arabic subs in. Writes `voice/{slug}_full_voiced.mp4` and `voice/{slug}_full_voiced_subs.mp4`.

### Order of operations

1. **Save narration JSONs** (en + ar). Translate immediately — don't defer the Arabic; user's stated preference is voiced English + burned-in Arabic subs.
2. **Build `{slug}_helpers.py`** — every primitive your scenes will need (figures, props, label helpers). Sanity-check with a single test scene that renders all primitives in one frame and extract a PNG via the pyav-in-Docker trick. Look at it. Fix anything that doesn't read.
3. **Write all `{slug}_b{N}.py` scene files.** Estimate per-beat duration from character count × 0.072 + 1.5s tail (min 2.5s). Don't try to nail audio durations — the mux step handles drift.
4. **Launch render + TTS in parallel.** Render takes ~30s/beat × N beats; TTS takes ~2s/beat. Use Bash `run_in_background: true` for both, then `until` loop to wait on the combined condition.
5. **Mux per-beat.** The mux script uses `tpad` on video + `apad` on audio with 999s padding then `-t TARGET` to clip — TARGET = max(video_dur, audio_dur) + 0.3s tail. No scene re-render needed when audio is off from estimate. Uses `ffprobe` (NOT `ffmpeg -i`) for duration measurement — see "Pitfalls" below.
6. **Build subtitles + concat-burn.** `build_subtitles_{slug}.py` runs inside the Docker manim image (it needs `av`). Concat uses `-c copy`; subtitle burn re-encodes video only and copies audio.
7. **Copy final to `~/school-ai/`.** That's the user's collection directory. Drop `{slug}_full_voiced_subs.mp4` (or `_full_voiced.mp4` if no subs) there.
8. **Add a sibling JSON to `~/school-ai/`.** The user wants the original storyboard (the JSON they pasted, with `id`/`text`/`visual` per beat) saved as `~/school-ai/{slug}_full_voiced_subs.json` next to the mp4. Same filename base, `.json` extension.

### Deliverable destination

- `~/school-ai/` — final mp4 + sibling storyboard JSON. **This is the only place the user looks.** Don't leave them hunting in `voice/`.
- `voice/{slug}_full_voiced_subs.mp4` is the canonical source; the copy in `~/school-ai/` is what the user opens.

### Confirm-by-default user preferences (carry these forward)

- **English voice + Arabic subs burned in** is the default deliverable shape. Don't ship voiced-without-subs as final unless the user says so. The rocket video shipped without Arabic subs because the subtitle pipeline wasn't yet proven — it is now.
- **One final video, not a folder of clips.** The per-beat mp4s are intermediates.
- **Don't ask which app to open in.** `open path/to/file.mp4` (default QuickTime) is fine.
- **Default voice = `onyx`** via `gpt-4o-mini-tts`. The `INSTRUCTIONS` string in `generate_tts_en.py` is the audio "design system" — silence is content, kitchen-table warm, not announcer. Reuse it verbatim per new scene unless the topic genuinely needs a different register (e.g. the gym/work-vs-effort scene wanted a slightly more pointed tone — adjust `INSTRUCTIONS` last paragraph, not the whole thing).
- **Voice quality could be upgraded** to ElevenLabs if asked. Onyx is the baseline.
- **Background music** is not in the project. Suggest a public-domain ambient track at low gain (-20 dB) only if asked.

---

## Bugs / pitfalls observed (these will bite again)

In addition to the Manim gotchas listed earlier:

- **`ffmpeg -i FILE` with no output exits non-zero.** Combined with `set -o pipefail`, this kills duration-probe scripts silently. Always use `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 FILE`. (Bit us once during the first cars mux.)
- **Fontconfig errors during subtitle burn are cosmetic.** `Cannot load default config file: No such file: (null)` warnings appear inside `jrottenberg/ffmpeg:latest` when burning ASS subtitles. The fallback font handles Arabic correctly — verify with a frame extraction (`av.open(...).decode(video=0)`) before assuming the warnings broke anything.
- **Manim's `ArrowTriangleFilledTip.hex` crash.** Some animation patterns (uncertain which exact combo — happened in the gym scene render) trigger `AttributeError: ArrowTriangleFilledTip object has no attribute 'hex'`. If a render crashes with this, the offending scene's Arrow likely had an unusual color-handling path. Fix by setting the arrow's color explicitly with a Manim color constant or hex string before using `.animate.set_*`, rather than letting the tip inherit. The gym scene was unfinished due to this; a re-render after fixing the offending beat(s) should complete it.
- **`-c copy` concat warns about non-monotonic DTS.** Harmless — the per-beat audio streams have tiny timestamp gaps. Output plays fine. Don't try to "fix" it by re-encoding the concat.
- **Estimated durations drift from real TTS.** Most beats end up within ~1–2 s of estimate; landing beats ("Wrong.", "Zero.") often run shorter than the estimate gives them. The mux pad-and-clip approach absorbs this without re-rendering. Only worth re-rendering a beat if the mismatch is >3 s AND the held-final-frame reads awkward.
- **Pasted storyboard JSON sometimes contains characters that break JSON parsing** if dropped directly into a `Write` call (smart quotes, em-dashes inside string literals). Confirm `python3 -m json.tool` parses your file before generating TTS off it.

---

## Open / possible next work

- **Finish the gym (work-vs-effort) scene.** All 31 scene files exist, narration JSONs (en + ar) exist, TTS audio exists at `voice/audio_gym_en/`. The render crashed mid-batch on the ArrowTriangleFilledTip bug. Re-render after the fix and run the rest of the pipeline.
- **Retro-fit Arabic subs onto `rocket_full_voiced.mp4`.** It shipped without them (subtitle pipeline wasn't proven yet at the time). Now that `pendulum`, `cars`, `paperclip` all have subs burned in, the rocket video is the only one in `~/school-ai/` without subs — bring it to parity. Need to write `narration_rocket_ar.json` (27 entries) and run the existing pipeline.
- **Scene 2 of the gravity script** still doesn't exist if the user wants to continue that series.

---

## User preferences for future videos (carry these forward)

These are durable defaults the user wants applied to any new gravity-series videos or follow-up explainers. Not visible in the code — confirm-by-default rather than re-asking each time.

- **Voice + subtitles combo:** **English narration with Arabic subtitles burned into the video.** The English voice is the audio track (Onyx via OpenAI TTS is the established baseline). The Arabic translation appears as on-screen subtitles, RTL, positioned bottom-center. This is the user's preferred bilingual format. Now proven end-to-end on pendulum/cars/paperclip — see the "Standard pipeline" section above.

- **One final video, not a folder of clips.** The *workflow* renders per-beat for sync precision, but the *deliverable* is a single concatenated mp4. Don't ship a folder of clips unless explicitly asked. Don't make the user click through `next next next` on individual previews unless they ask for that cadence — default to building the full thing and opening it.

## API key handling

- The user keeps `OPENAI_API_KEY` in their shell environment (`~/.zshrc`) so all scripts pick it up automatically. **Never paste a key into chat, never write it to project files, never inline it on the command line in scripts that will live in git.**
- The Bash tool runs in a non-interactive shell that doesn't source `~/.zshrc`. To pick up the user's key, prefix Python invocations with `zsh -ic '...'` (interactive shell sources zshrc): `zsh -ic 'cd /Users/khalid-dev/manim/voice && python3 generate_tts_{slug}_en.py all'`.
- If a future session needs to verify the key is set without exposing it: `zsh -ic 'if [ -n "${OPENAI_API_KEY:-}" ]; then echo "set, length=${#OPENAI_API_KEY}"; else echo "missing"; fi'` (prints length only — a `sk-proj-...` key is 164 chars).
- Reading or echoing the key value itself is blocked by policy. Don't attempt to work around it.
- If the user pastes a key in chat by mistake (this happened once on 2026-05-12): tell them to revoke it immediately at https://platform.openai.com/api-keys and create a fresh one to put in `~/.zshrc`. Do NOT use the pasted key, and do NOT persist it to disk — the security policy correctly blocks that.
- Pasted keys in chat history are considered compromised. Treat them as historical only.
