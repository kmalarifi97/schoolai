#!/usr/bin/env bash
# Concat all 14 voiced newton beats, then burn the Arabic subtitle file onto
# the result. Output: voice/newton_full_voiced_subs.mp4
set -euo pipefail
export LC_ALL=C
cd "$(dirname "$0")"
PROJ_VOICE="$(cd .. && pwd)"

# 1. concat to an intermediate (no subs)
LIST=/tmp/newton_voiced_concat_list.txt
: > "$LIST"
for i in $(seq 1 11); do
  f="$PROJ_VOICE/voiced_newton/voiced_newton_b${i}.mp4"
  [ ! -f "$f" ] && { echo "MISSING $f"; exit 1; }
  echo "file '/work/voiced_newton/voiced_newton_b${i}.mp4'" >> "$LIST"
done

docker run --rm \
  -v "$PROJ_VOICE":/work \
  -v /tmp:/tmp \
  jrottenberg/ffmpeg:latest \
  -y -hide_banner -loglevel warning \
  -f concat -safe 0 -i /tmp/newton_voiced_concat_list.txt \
  -c copy -movflags +faststart \
  /work/newton_full_voiced.mp4
echo "intermediate concat: newton_full_voiced.mp4"

# 2. burn subs onto the concatenated file
docker run --rm \
  -v "$PROJ_VOICE":/work \
  jrottenberg/ffmpeg:latest \
  -y -hide_banner -loglevel warning \
  -i /work/newton_full_voiced.mp4 \
  -vf "ass=/work/subs_newton_ar.ass" \
  -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 20 \
  -c:a copy -movflags +faststart \
  /work/newton_full_voiced_subs.mp4

echo "wrote $PROJ_VOICE/newton_full_voiced_subs.mp4"
ls -la "$PROJ_VOICE/newton_full_voiced_subs.mp4"
