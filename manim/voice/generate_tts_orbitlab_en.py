"""Generate English TTS for the orbitlab project-story (24 beats)."""

import json
import os
import sys
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).parent
NARRATION = json.loads((HERE / "narration_orbitlab_en.json").read_text())
OUTPUT_DIR = HERE / "audio_orbitlab_en"
OUTPUT_DIR.mkdir(exist_ok=True)

VOICE = os.environ.get("TTS_VOICE", "onyx")
MODEL = "gpt-4o-mini-tts"

INSTRUCTIONS = """
Mindset: silence is content. This is a story, not a lecture. We are
watching Sami, not being taught at. Slow is correct. You are thinking
out loud, across a kitchen table, to one friend who is curious. Warm and
patient — not an announcer, not a documentarian, not a textbook.

Pacing: default slower than feels natural. Trust the silence. Period is a
full stop. Em-dash (—) is a mid-thought reconsideration: brief pause with
a slight pitch lift, then continue. Short lines like "One goal." or
"Wrong." are landing beats — give them air before and after, not energy.

Tone: curiosity, not excitement. Sami's failed attempts (it crashes, it
flies off) should be said plainly, with quiet sympathy, not drama. The
closing callbacks (b21-b24) are a soft remembering — almost to yourself
— not a recap.

Avoid: announcer cadence, falling-tone conclusiveness, performative
warmth, over-articulated consonants, sweeping emphasis across sentences.
""".strip()


def generate(beat_id: str):
    text = NARRATION[beat_id]
    out_path = OUTPUT_DIR / f"{beat_id}.mp3"
    client = OpenAI()
    response = client.audio.speech.create(
        model=MODEL,
        voice=VOICE,
        input=text,
        instructions=INSTRUCTIONS,
    )
    out_path.write_bytes(response.content)
    print(f"  {beat_id}: {len(text):3d} chars -> {out_path.name}")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    arg = sys.argv[1]
    if arg == "all":
        for beat_id in NARRATION.keys():
            generate(beat_id)
    else:
        generate(arg)


if __name__ == "__main__":
    main()
