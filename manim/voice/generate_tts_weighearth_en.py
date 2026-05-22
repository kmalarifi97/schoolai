"""
Generate English TTS for the weighearth scene (8 beats).
Same model/voice/instructions as generate_tts_en.py.
"""

import json
import os
import sys
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).parent
NARRATION = json.loads((HERE / "narration_weighearth_en.json").read_text())
OUTPUT_DIR = HERE / "audio_weighearth_en"
OUTPUT_DIR.mkdir(exist_ok=True)

VOICE = os.environ.get("TTS_VOICE", "onyx")
MODEL = "gpt-4o-mini-tts"

INSTRUCTIONS = """
Mindset: silence is content. The script is short on purpose; each line needs
room to land. Slow is correct. You are not narrating a video. You are thinking
out loud, across a kitchen table, to one friend who is curious. Warm and
patient, like a Udacity-style instructor who is audibly interested in what
they're saying — not an announcer, not a documentarian, not a textbook.

Pacing: default slower than feels natural. Trust the silence. Period is a
full stop. Em-dash (—) is a mid-thought reconsideration: brief pause with a
slight pitch lift, then continue. Single-word or very short lines like
"Watch." are landing beats — give them air before and after, not energy.

Tone: curiosity, not excitement. Conversational, not casual. Every word is
chosen. The "you" voice is intimate, not theatrical — talking to one person,
not an audience.

Avoid: announcer cadence, falling-tone conclusiveness ("…and that's why…"),
performative warmth ("So, my friends…"), over-articulated consonants,
sweeping emphasis across whole sentences.
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
        print(__doc__)
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "all":
        for beat_id in NARRATION.keys():
            generate(beat_id)
    else:
        generate(arg)


if __name__ == "__main__":
    main()
