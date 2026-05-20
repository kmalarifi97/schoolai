# Physics 2 Library — web app

Minimal **FastAPI** backend + **Next.js** frontend. Login-gated, pre-seeded users.
Videos are streamed from the existing `scripts/concepts/**` and `scripts/projects/**`
mp4s — nothing is copied or duplicated.

## Run with Docker (one command) — recommended

```bash
cd web
docker compose up -d --build
```
- Frontend → **http://localhost:3000** (log in, e.g. `demo` / `demo`)
- Backend debug API → http://localhost:8090  (host 8000 was taken by another app)
- The repo is mounted read-only into the backend at `/srv/lib`; videos stream from there. Nothing copied.
- Stop: `docker compose down`

> Note: the repo must be mounted at `/srv/lib` (NOT `/lib` — that would shadow the
> container's system libraries). `LIB_ROOT` env points the backend at it.

## Run without Docker (two terminals)

**Backend**
```bash
cd web/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app:app --port 8000   # http://localhost:8000
```

**Frontend**
```bash
cd web/frontend
npm install
npm run dev                          # http://localhost:3000
```

Open http://localhost:3000 → log in.

## Pre-seeded users

Edit `web/backend/users.json` (no self-registration). Defaults:

| username | password | role |
|---|---|---|
| teacher | phys2-teacher | teacher |
| student1 | phys2-1 | student |
| student2 | phys2-2 | student |
| student3 | phys2-3 | student |
| demo | demo | student |

## How it fits together

- `web/backend/catalog.py` builds the catalog from `scripts/structure.json`,
  `concept_library_beats_v2.json`, `concepts/INDEX.json`, and the project JSONs —
  same data wiring as `scripts/build_site.py`. Re-run nothing; it reads live on start.
- Auth = stdlib HMAC-signed token (12 h), secret auto-generated to `web/backend/.secret`.
- `<video>` auth uses `?t=<token>` (browsers can't set headers on media elements).
- The frontend proxies `/api/*` → backend (`next.config.js`), so everything is same-origin.

## Notes
- `gfield` & `cavendish` concept subtitles are Gulf-style (predate the فصحى standard);
  every other video is فصحى. Re-translate + rerun their subtitle/concat step to fix.
- For production: set `APP_SECRET`, build the frontend (`npm run build && npm start`),
  put the backend behind a real ASGI server / reverse proxy.
