#!/usr/bin/env bash
# Incremental update: upload the project videos + textbook PDF (the 25 concept
# videos are already in the bucket), then redeploy the MCP server with the new
# tool set. Run from the repo root:  bash chatgpt-app/update.sh
set -euo pipefail

PROJECT="training-network-sa"
REGION="me-central1"
BUCKET="${PROJECT}-physics-videos"
SERVICE="physics2-mcp"
VIDEO_BASE="https://storage.googleapis.com/${BUCKET}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> [1/2] Uploading project videos -> projects/<slug>.mp4 …"
for f in "$ROOT"/scripts/projects/*/*_full_voiced_subs.mp4; do
  base="$(basename "$f")"
  slug="${base%_full_voiced_subs.mp4}"
  gcloud storage cp "$f" "gs://${BUCKET}/projects/${slug}.mp4" --project "$PROJECT"
done

echo "==> [2/2] Redeploying MCP server …"
gcloud run deploy "$SERVICE" \
  --source "$ROOT/chatgpt-app" \
  --region "$REGION" --project "$PROJECT" \
  --allow-unauthenticated \
  --set-env-vars "PUBLIC_VIDEO_BASE=${VIDEO_BASE}" \
  --quiet

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"
echo
echo "================================================================"
echo "  Updated. Connector URL:  ${URL}/mcp"
echo "  (Refresh the connector in ChatGPT → Settings → Connectors.)"
echo "================================================================"
