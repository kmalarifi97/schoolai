#!/usr/bin/env python3
"""Build a single silent preview mp4 per concept: concat the 12 rendered
beat clips and burn Arabic subtitles timed to each clip's own duration.
No audio (TTS deferred). Uses jrottenberg/ffmpeg:latest via Docker.

Usage: build_silent_preview.py <slug> <ClassPrefix> <voice_root> <out_dir>
  e.g. ... cavendish Cavendish /Users/khalid-dev/manim/voice \
           /Users/khalid-dev/physics-E2-library/scripts/concepts/02_cavendish
"""
import json, subprocess, sys, pathlib, tempfile, os

slug, prefix, voice_root, out_dir = sys.argv[1:5]
voice_root = pathlib.Path(voice_root)
out_dir = pathlib.Path(out_dir)
HOST_MOUNT = "/Users/khalid-dev"
FFMPEG = "jrottenberg/ffmpeg:latest"


def hp(p):  # host path -> container path under /host
    return "/host" + str(pathlib.Path(p).resolve())[len(HOST_MOUNT):]


ar = json.loads((voice_root / f"narration_{slug}_ar.json").read_text())
N = len(ar)  # beat count derived from narration (handles 12, 25, etc.)

clips = [voice_root / "scenes" / "media" / "videos" / f"{slug}_b{i}" /
         "720p30" / f"{prefix}S1B{i}.mp4" for i in range(1, N + 1)]
for c in clips:
    if not c.exists():
        sys.exit(f"MISSING clip: {c}")

# 1) probe all 12 durations in one container
probe_cmd = "; ".join(
    f'ffprobe -v error -show_entries format=duration -of '
    f'default=nw=1:nk=1 "{hp(c)}"' for c in clips)
out = subprocess.run(
    ["docker", "run", "--rm", "-v", f"{HOST_MOUNT}:/host",
     "--entrypoint", "sh", FFMPEG, "-c", probe_cmd],
    capture_output=True, text=True)
durs = [float(x) for x in out.stdout.split()]
if len(durs) != N:
    sys.exit(f"probe failed: got {len(durs)} durations\n{out.stderr[-800:]}")


def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


# 2) ASS with each Arabic line spanning its clip
header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
ScaledBorderAndShadow: yes
WrapStyle: 0
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Arabic,Arial Unicode MS,30,&H00FFFFFF,&H000000FF,&H00000000,&HC0000000,0,0,0,0,100,100,0,0,1,2.0,0,2,80,80,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines, cursor = [header], 0.0
for i in range(1, N + 1):
    d = durs[i - 1]
    txt = ar[f"s1_b{i}"].replace("\n", " ").strip()
    lines.append(
        f"Dialogue: 0,{fmt(cursor)},{fmt(cursor + d)},Arabic,,0,0,0,,{txt}\n")
    cursor += d
ass_path = out_dir / f"{slug}_ar.ass"
ass_path.write_text("".join(lines), encoding="utf-8")

# 3) concat list
concat_path = out_dir / f"{slug}_concat.txt"
concat_path.write_text(
    "".join(f"file '{hp(c)}'\n" for c in clips), encoding="utf-8")

silent = out_dir / f"{slug}_silent_nosub.mp4"
final = out_dir / f"{slug}_silent_subs.mp4"

# 4) concat (-c copy)
subprocess.run(
    ["docker", "run", "--rm", "-v", f"{HOST_MOUNT}:/host",
     FFMPEG, "-y", "-f", "concat", "-safe", "0",
     "-i", hp(concat_path), "-c", "copy", "-an", hp(silent)],
    check=True, capture_output=True, text=True)

# 5) burn Arabic subs, no audio
r = subprocess.run(
    ["docker", "run", "--rm", "-v", f"{HOST_MOUNT}:/host",
     FFMPEG, "-y", "-i", hp(silent),
     "-vf", f"subtitles={hp(ass_path)}",
     "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
     hp(final)],
    capture_output=True, text=True)
if not final.exists():
    sys.exit(f"burn failed:\n{r.stderr[-1200:]}")

print(f"OK {slug}: total={cursor:.1f}s  ->  {final}  "
      f"({final.stat().st_size//1024} KB)")
