#!/usr/bin/env bash
# Download the Junyi Academy dataset from Kaggle, unzip it, and print every
# CSV's header + first rows so we can map columns before building the graph.
#
# Requires Kaggle credentials (your account — no anonymous download):
#   either ~/.kaggle/kaggle.json  (chmod 600), or env KAGGLE_USERNAME + KAGGLE_KEY.
# Get the token at https://www.kaggle.com/settings -> "Create New API Token".
#
# Dataset is non-commercial / research-only. Output goes to graph/junyi_raw/
# (gitignored). Usage:  bash graph/fetch_junyi.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
RAW="$HERE/junyi_raw"
KAGGLE="$HOME/Library/Python/3.13/bin/kaggle"
[ -x "$KAGGLE" ] || KAGGLE="$(command -v kaggle || true)"
DATASET="junyiacademy/learning-activity-public-dataset-by-junyi-academy"

if [ -z "${KAGGLE:-}" ]; then echo "!! kaggle CLI not found"; exit 1; fi
if [ ! -f "$HOME/.kaggle/kaggle.json" ] && [ -z "${KAGGLE_KEY:-}" ]; then
  echo "!! No Kaggle credentials. Put kaggle.json at ~/.kaggle/ (chmod 600) or export KAGGLE_USERNAME/KAGGLE_KEY."
  exit 1
fi

mkdir -p "$RAW"
echo "[fetch] downloading $DATASET (large — multiple GB) ..."
"$KAGGLE" datasets download -d "$DATASET" -p "$RAW" --unzip

echo; echo "[files]"; ls -lah "$RAW"
echo; echo "[headers + first 3 rows of each CSV]"
for f in "$RAW"/*.csv; do
  [ -f "$f" ] || continue
  echo "=== $(basename "$f") ==="
  head -n 4 "$f"
  echo
done
echo "[next] run the builder with column names matching the headers above, e.g.:"
echo "  LOG_CSV=$RAW/Log_Problem.csv EXERCISE_CSV=$RAW/Info_Content.csv \\"
echo "    COL_STUDENT=uuid COL_EXERCISE=ucid COL_OUTCOME=is_correct \\"
echo "    EX_COL_ID=ucid EX_COL_SKILL=topic EX_COL_AREA=area \\"
echo "    node $HERE/build_junyi_graph.mjs"
