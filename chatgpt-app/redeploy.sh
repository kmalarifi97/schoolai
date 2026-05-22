#!/usr/bin/env bash
# Code-only redeploy of the MCP server (no video/asset uploads — those already
# live in the bucket). Use this while iterating on server.js / instructions.
# Run from the repo root:  bash chatgpt-app/redeploy.sh
set -euo pipefail

PROJECT="training-network-sa"
REGION="me-central1"
SERVICE="physics2-mcp"
BUCKET="${PROJECT}-physics-videos"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

gcloud run deploy "$SERVICE" \
  --source "$ROOT/chatgpt-app" \
  --region "$REGION" --project "$PROJECT" \
  --allow-unauthenticated \
  --set-env-vars "PUBLIC_VIDEO_BASE=https://storage.googleapis.com/${BUCKET}" \
  --quiet

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"
echo
echo "Done. Connector URL: ${URL}/mcp"
