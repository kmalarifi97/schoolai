"""Build ASS subtitle file for the latentheat scene from narration_latentheat_ar.json."""

import json
from pathlib import Path
import av

HERE = Path(__file__).parent
NARRATION = json.loads((HERE / "narration_latentheat_ar.json").read_text())
VOICED_DIR = HERE / "voiced_latentheat"
AUDIO_DIR  = HERE / "audio_latentheat_en"
N_BEATS    = 12


def dur(path):
    c = av.open(str(path)); d = float(c.duration) / 1_000_000.0; c.close(); return d


def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def main():
    cursor = 0.0; events = []
    for i in range(1, N_BEATS + 1):
        bid = f"s1_b{i}"
        video_dur = dur(VOICED_DIR / f"voiced_latentheat_b{i}.mp4")
        audio_dur = dur(AUDIO_DIR / f"{bid}.mp3")
        start = cursor; end = cursor + audio_dur
        text = NARRATION[bid].replace("\n", " ").strip()
        events.append((start, end, text))
        cursor += video_dur

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

    lines = [header]
    for start, end, text in events:
        lines.append(f"Dialogue: 0,{fmt(start)},{fmt(end)},Arabic,,0,0,0,,{text}\n")
    (HERE / "subs_latentheat_ar.ass").write_text("".join(lines), encoding="utf-8")
    print(f"wrote subs_latentheat_ar.ass with {len(events)} entries, total {cursor:.2f}s")


if __name__ == "__main__":
    main()
