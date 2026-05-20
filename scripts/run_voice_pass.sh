#!/usr/bin/env bash
# Full voice pass: TTS -> mux -> subtitles -> concat-burn -> deliver, per slug.
# Continues on per-slug failure; logs a summary. Run from repo root.
set -uo pipefail
export LC_ALL=C
REPO=/Users/khalid-dev/physics-E2-library
VOICE=$REPO/manim/voice
LOG=$REPO/scripts/voice_pass.log
: > "$LOG"

# slug : dest_dir  (cavendish lives in the other tree, handled separately)
declare -a SLUGS=(
  "gfield:scripts/concepts/03_gfield"
  "equivalence:scripts/concepts/05_equivalence"
  "angular:scripts/concepts/06_angular"
  "torque:scripts/concepts/07_torque"
  "centerofmass:scripts/concepts/08_centerofmass"
  "fictitious:scripts/concepts/09_fictitious"
  "impulse:scripts/concepts/10_impulse"
  "momentumcons:scripts/concepts/11_momentumcons"
  "workenergy:scripts/concepts/12_workenergy"
  "power:scripts/concepts/14_power"
  "machines:scripts/concepts/15_machines"
  "efficiency:scripts/concepts/16_efficiency"
  "gravpe:scripts/concepts/17_gravpe"
  "elasticpe:scripts/concepts/18_elasticpe"
  "rotke:scripts/concepts/19_rotke"
  "collisions:scripts/concepts/21_collisions"
  "tempvsthermal:scripts/concepts/22_tempvsthermal"
  "heattransfer:scripts/concepts/23_heattransfer"
  "specificheat:scripts/concepts/24_specificheat"
  "latentheat:scripts/concepts/25_latentheat"
  "thermolaws:scripts/concepts/26_thermolaws"
  "skatepark:scripts/projects/01_skatepark_energy_audit"
)

ok=0; fail=0
for entry in "${SLUGS[@]}"; do
  slug="${entry%%:*}"; dest="$REPO/${entry##*:}"
  echo "=== $slug ===" | tee -a "$LOG"
  {
    cd "$VOICE" || exit 1
    zsh -ic "python3 generate_tts_${slug}_en.py all" \
      && bash "scenes/mux_voiced_${slug}.sh" \
      && docker run --rm -v "$VOICE":/work --entrypoint python3 \
           manimcommunity/manim:stable "/work/build_subtitles_${slug}.py" \
      && bash "scenes/concat_burn_${slug}.sh"
  } >> "$LOG" 2>&1
  final="$VOICE/${slug}_full_voiced_subs.mp4"
  if [ -f "$final" ]; then
    mkdir -p "$dest"; cp "$final" "$dest/"
    echo "OK   $slug -> $dest/${slug}_full_voiced_subs.mp4 ($(du -h "$final"|cut -f1))" | tee -a "$LOG"
    ok=$((ok+1))
  else
    echo "FAIL $slug (see log)" | tee -a "$LOG"
    fail=$((fail+1))
  fi
done
echo "=== VOICE PASS DONE: ok=$ok fail=$fail ===" | tee -a "$LOG"
