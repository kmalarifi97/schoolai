#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
cd "$(dirname "$0")"
PROJ_VOICE="$(cd .. && pwd)"

LIST=/tmp/skatepark_voiced_concat_list.txt
: > "$LIST"
for i in $(seq 1 25); do
  f="$PROJ_VOICE/voiced_skatepark/voiced_skatepark_b${i}.mp4"
  [ ! -f "$f" ] && { echo "MISSING $f"; exit 1; }
  echo "file '/work/voiced_skatepark/voiced_skatepark_b${i}.mp4'" >> "$LIST"
done

docker run --rm -v "$PROJ_VOICE":/work -v /tmp:/tmp jrottenberg/ffmpeg:latest \
  -y -hide_banner -loglevel warning \
  -f concat -safe 0 -i /tmp/skatepark_voiced_concat_list.txt \
  -c copy -movflags +faststart \
  /work/skatepark_full_voiced.mp4
echo "intermediate concat: skatepark_full_voiced.mp4"

docker run --rm -v "$PROJ_VOICE":/work jrottenberg/ffmpeg:latest \
  -y -hide_banner -loglevel warning \
  -i /work/skatepark_full_voiced.mp4 \
  -vf "ass=/work/subs_skatepark_ar.ass" \
  -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 20 \
  -c:a copy -movflags +faststart \
  /work/skatepark_full_voiced_subs.mp4
echo "wrote $PROJ_VOICE/skatepark_full_voiced_subs.mp4"
ls -la "$PROJ_VOICE/skatepark_full_voiced_subs.mp4"
