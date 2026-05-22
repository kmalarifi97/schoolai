#!/usr/bin/env bash
# One-shot deploy of the Physics 2 ChatGPT App.
#   - enables APIs
#   - creates a public videos bucket + uploads the 25 concept mp4s (as <slug>.mp4)
#   - deploys the MCP server to Cloud Run
# Run from the repo root:  bash chatgpt-app/deploy.sh
set -euo pipefail

PROJECT="training-network-sa"
REGION="me-central1"
BUCKET="${PROJECT}-physics-videos"        # globally unique via project id
SERVICE="physics2-mcp"
VIDEO_BASE="https://storage.googleapis.com/${BUCKET}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Project: $PROJECT  Region: $REGION  Bucket: $BUCKET"

echo "==> [1/5] Enabling APIs…"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com storage.googleapis.com --project "$PROJECT"

echo "==> [2/5] Creating bucket (ok if it already exists)…"
gcloud storage buckets create "gs://${BUCKET}" \
  --project "$PROJECT" --location "$REGION" --uniform-bucket-level-access \
  || echo "    (bucket exists, continuing)"

echo "==> [3/5] Uploading concept videos as <slug>.mp4…"
for f in "$ROOT"/scripts/concepts/*/*_full_voiced_subs.mp4; do
  base="$(basename "$f")"
  slug="${base%_full_voiced_subs.mp4}"
  gcloud storage cp "$f" "gs://${BUCKET}/${slug}.mp4" --project "$PROJECT"
done

echo "==> [4/5] Making bucket public-read + CORS…"
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member=allUsers --role=roles/storage.objectViewer --project "$PROJECT"
gcloud storage buckets update "gs://${BUCKET}" \
  --cors-file="$ROOT/chatgpt-app/cors.json" --project "$PROJECT"

echo "==> [5/5] Deploying MCP server to Cloud Run…"
gcloud run deploy "$SERVICE" \
  --source "$ROOT/chatgpt-app" \
  --region "$REGION" --project "$PROJECT" \
  --allow-unauthenticated \
  --set-env-vars "PUBLIC_VIDEO_BASE=${VIDEO_BASE}" \
  --quiet

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format='value(status.url)')"
echo
echo "================================================================"
echo "  Done. Connector URL for ChatGPT:  ${URL}/mcp"
echo "  Videos:                            ${VIDEO_BASE}/<slug>.mp4"
echo "================================================================"
