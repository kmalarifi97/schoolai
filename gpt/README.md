# Physics 2 — Custom GPT

Everything needed to publish a study tutor as a **Custom GPT** on ChatGPT.
Knowledge files are generated from the repo's source-of-truth JSON.

## Build the knowledge files

```bash
python3 gpt/build_knowledge.py
```

Produces:
- `gpt/knowledge/curriculum.md` — chapters → lessons (summaries, objectives, key terms, page numbers)
- `gpt/knowledge/concept_library.md` — 26 concepts with their intuition scripts

Re-run whenever `scripts/structure.json` or `scripts/concept_library_beats_v2.json` change.

## Create the GPT (in ChatGPT)

Requires a **ChatGPT Plus / Team / Enterprise** account.

1. Go to **chatgpt.com → Explore GPTs → Create**, open the **Configure** tab.
2. **Name:** e.g. `معلّم الفيزياء 2`. Add a description and an icon.
3. **Instructions:** paste the body of [`instructions.md`](instructions.md).
4. **Conversation starters:** the four lines in [`conversation-starters.md`](conversation-starters.md).
5. **Knowledge:** upload
   - `gpt/knowledge/curriculum.md`
   - `gpt/knowledge/concept_library.md`
   - `book/فيزياء ثاني ثنوي.pdf` (the textbook)
6. **Capabilities:** Web Search optional; Code Interpreter optional. No Action yet (see below).
7. Test with a few prompts, then **Publish** (Only me / Anyone with link / Store).

## The Action (code is ready — just needs a public URL)

The backend already exposes read-only, GPT-safe endpoints (defined in
`web/backend/gpt_api.py`, mounted in `app.py`):

| Endpoint | operationId | Returns |
|---|---|---|
| `GET /gpt/concepts` | `listConcepts` | all 26 concepts (ar/en, chapter, lesson, pages, video flag) |
| `GET /gpt/concepts/{slug}` | `getConcept` | one concept + handoff line + PhET link |
| `GET /gpt/search?q=` | `searchCurriculum` | concept matches for an Arabic/English term |

These return **metadata only** — never the login-gated mp4/PDF streams. An
optional shared secret guards them: set `GPT_API_KEY=...` on the server and
configure the Action's auth as **API Key**, custom header `X-API-Key`. Leave
`GPT_API_KEY` unset to keep them open.

### Generate the Action schema

```bash
PUBLIC_API_URL=https://your-deployed-api python3 gpt/export_action_schema.py
```

Writes [`gpt/action_schema.json`](action_schema.json) (OpenAPI 3.1, `/gpt/*`
only, with your server URL baked in). In the GPT editor → **Actions** → **Add
actions**, paste that schema.

### Remaining steps (need deployment, not code)

1. Deploy `web/backend` at a **public HTTPS URL** (ChatGPT can't reach localhost).
2. Re-run the export with the real `PUBLIC_API_URL`, paste `action_schema.json`.
3. Host [`privacy.md`](privacy.md) at a public URL and enter it as the GPT's
   privacy policy (required to publish a GPT with an Action).

Until deployed, the GPT runs knowledge-only and can still name the relevant
concept video from `concept_library.md`.
