# Physics 2 — ChatGPT App (Apps SDK / MCP)

> ⚠️ **INACTIVE / LEGACY (superseded).** This KST-based stack is preserved but no
> longer the active tutor. The current approach is the explicit prerequisite-graph
> tutor in [`../graph-tutor/`](../graph-tutor/) (graph → GraphQL → MCP, diagnosis by
> direct graph traversal). Nothing here is deleted; this app remains runnable for
> reference and can be reactivated, but new work happens in `graph-tutor/`.

An MCP server that gives ChatGPT an **in-chat video-player widget** for the
Physics 2 concept library. Two tools:

- `find_concept(query)` — search concepts by Arabic/English keyword (text only).
- `show_concept_video(concept)` — render the player widget for one concept,
  with its name, lesson, book pages, and PhET simulation link.

```
ChatGPT ──/mcp──> server.js (Cloud Run) ──renders──> video-widget.html (iframe)
                                                       │
                       <video src> ──loads──> PUBLIC_VIDEO_BASE/<slug>.mp4 (GCS)
```

ChatGPT renders the widget but never hosts the video — the `<video>` loads from
`PUBLIC_VIDEO_BASE`, which must be a public URL (a GCS bucket; see below).

## Layout

```
chatgpt-app/
├── server.js                MCP server (/mcp), tools + widget resource
├── package.json
├── Dockerfile               Cloud Run image
├── build_app_data.py        regenerates data/concepts.json from scripts/*.json
├── data/concepts.json       26 concepts (generated)
└── public/video-widget.html the in-chat player UI
```

Regenerate the data after editing the curriculum manifests:

```bash
python3 chatgpt-app/build_app_data.py
```

## Run locally

```bash
cd chatgpt-app
npm install
PUBLIC_VIDEO_BASE="https://storage.googleapis.com/<bucket>" npm start
# -> http://localhost:8787/mcp
```

Test the protocol with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector@latest --server-url http://localhost:8787/mcp --transport http
```

To try it inside ChatGPT during development, tunnel the port and add it as a
connector (ChatGPT → Settings → Apps & Connectors → Advanced → developer mode →
Create connector → paste the `https://…/mcp` URL):

```bash
ngrok http 8787
```

## Deploy (Cloud Run)

```bash
gcloud run deploy physics2-mcp \
  --source chatgpt-app \
  --region me-central1 \
  --allow-unauthenticated \
  --set-env-vars PUBLIC_VIDEO_BASE=https://storage.googleapis.com/<bucket>
```

Use the resulting `https://…/mcp` URL as the connector in ChatGPT.

## Videos (GCS)

The widget needs the mp4s public. Upload the 25 concept videos, named
`<slug>.mp4`, to a bucket and make them readable + CORS-enabled for ChatGPT's
iframe origin. A helper script lives in `../scripts` once the bucket is chosen.
