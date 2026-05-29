"""Generate raw.ass and isolated.ass over 3 representative Arabic test lines.

Header/style copied verbatim from build_subtitles_angular.py, including the
production Style fontname "Arial Unicode MS". We mount the host's real
Arial Unicode.ttf (whose fontconfig family IS "Arial Unicode MS") into the
container via a minimal fonts.conf, so libass resolves the exact production font.
Everything (PlayResX 1280, PlayResY 720, fontsize 30, alignment 2, margins,
outline, etc.) is identical to production.
"""

from pathlib import Path
from bidi_isolate import isolate_ltr

HERE = Path(__file__).parent

LINES = [
    "في الفيديو السابق رأينا الكواكب تنزلق في مداراتها على انحناء الفضاء. عطارد قريبٌ سريع، ونبتون بعيدٌ بطيء.",
    "جرّب نسبة المسافتين: r_A على r_B — كم مرّةً يبعد A أكثر من B.",
    "فما فائدتها؟ اعرف بُعد كوكب، فتتنبّأ بطول سنته. كوكبٌ يكشف عن آخر — لا كتلته ولا شكل مساره (mass, path).",
]

# Each line shown for 2s, sequentially, total 6s (matches the 6s background).
TIMINGS = [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0)]

# Production header verbatim from build_subtitles_angular.py, fontname swapped
# to the mounted ArialUnicode font.
HEADER = """[Script Info]
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


def fmt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build(transform):
    out = [HEADER]
    for (start, end), text in zip(TIMINGS, LINES):
        out.append(
            f"Dialogue: 0,{fmt(start)},{fmt(end)},Arabic,,0,0,0,,{transform(text)}\n"
        )
    return "".join(out)


def main():
    (HERE / "raw.ass").write_text(build(lambda s: s), encoding="utf-8")
    (HERE / "isolated.ass").write_text(build(isolate_ltr), encoding="utf-8")
    print("wrote raw.ass and isolated.ass")


if __name__ == "__main__":
    main()
