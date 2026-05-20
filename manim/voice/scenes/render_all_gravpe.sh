#!/usr/bin/env bash
# Render all 12 gravpe beat scenes
set -uo pipefail
cd "$(dirname "$0")"
LOG=render_gravpe.log
: > "$LOG"
for i in $(seq 1 12); do
  CLASS="GravpeS1B${i}"
  FILE="gravpe_b${i}.py"
  echo "=== [$(date +%H:%M:%S)] Rendering $CLASS ===" | tee -a "$LOG"
  docker run --rm -v "$PWD":/manim manimcommunity/manim:stable \
    manim -qm "$FILE" "$CLASS" >> "$LOG" 2>&1
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "!! FAILED: $CLASS (exit $rc)" | tee -a "$LOG"
  else
    echo "ok: $CLASS" | tee -a "$LOG"
  fi
done
echo "=== DONE at $(date +%H:%M:%S) ===" | tee -a "$LOG"
