#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
cd "$(dirname "$0")"
PROJ_VOICE="$(cd .. && pwd)"

OUT_DIR="$PROJ_VOICE/voiced_tempvsthermal"
mkdir -p "$OUT_DIR"
TAIL=0.30

probe() {
  docker run --rm -v "$PROJ_VOICE":/work --entrypoint ffprobe \
    jrottenberg/ffmpeg:latest \
    -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    "/work/$1"
}

DUR_LIST="$PROJ_VOICE/durations_tempvsthermal_en.txt"
: > "$DUR_LIST"

for i in $(seq 1 12); do
  CLASS="TempvsthermalS1B${i}"
  VIDEO="scenes/media/videos/tempvsthermal_b${i}/720p30/${CLASS}.mp4"
  AUDIO="audio_tempvsthermal_en/s1_b${i}.mp3"
  OUT="voiced_tempvsthermal/voiced_tempvsthermal_b${i}.mp4"

  [ ! -f "$PROJ_VOICE/$VIDEO" ] && { echo "MISSING video: $VIDEO"; exit 1; }
  [ ! -f "$PROJ_VOICE/$AUDIO" ] && { echo "MISSING audio: $AUDIO"; exit 1; }

  V_DUR=$(probe "$VIDEO")
  A_DUR=$(probe "$AUDIO")
  TARGET=$(awk -v v="$V_DUR" -v a="$A_DUR" -v t="$TAIL" \
                'BEGIN{m=(v>a)?v:a; printf "%.3f", m+t}')

  printf "s1_b%d  %.3f  %.3f  %.3f\n" "$i" "$V_DUR" "$A_DUR" "$TARGET" >> "$DUR_LIST"
  echo "b${i}: video=${V_DUR}s audio=${A_DUR}s -> target=${TARGET}s"

  docker run --rm -v "$PROJ_VOICE":/work jrottenberg/ffmpeg:latest \
    -hide_banner -loglevel warning -y \
    -i "/work/$VIDEO" -i "/work/$AUDIO" \
    -filter_complex "[0:v]tpad=stop_mode=clone:stop_duration=999[v];[1:a]apad=pad_dur=999[a]" \
    -map "[v]" -map "[a]" -t "$TARGET" \
    -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 20 \
    -c:a aac -b:a 160k -movflags +faststart \
    "/work/$OUT"
done
echo "wrote $DUR_LIST"
ls "$OUT_DIR" | wc -l
