"""Minimal FastAPI backend for the Physics 2 library.

- Pre-seeded users (users.json), no signup.
- Signed token auth (stdlib hmac, no extra deps).
- Catalog JSON built from the repo's manifests.
- Range-capable mp4 streaming; <video> auth via ?t= token query param.

Run:  uvicorn app:app --reload --port 8000   (from web/backend/)
"""
import base64, hashlib, hmac, json, os, pathlib, time

from fastapi import FastAPI, HTTPException, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response, StreamingResponse

from catalog import build

HERE = pathlib.Path(__file__).resolve().parent
SECRET = (os.environ.get("APP_SECRET")
          or (HERE / ".secret").read_text().strip()
          if (HERE / ".secret").exists() else None)
if not SECRET:
    SECRET = base64.urlsafe_b64encode(os.urandom(32)).decode()
    (HERE / ".secret").write_text(SECRET)

USERS = {u["username"]: u for u in json.load(open(HERE / "users.json"))["users"]}
TOKEN_TTL = 60 * 60 * 12  # 12h

CATALOG, VIDEOS = build()

app = FastAPI(title="Physics 2 Library")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


def _sign(username: str) -> str:
    payload = base64.urlsafe_b64encode(
        json.dumps({"u": username, "exp": int(time.time()) + TOKEN_TTL}).encode()
    ).decode()
    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def _verify(token: str):
    try:
        payload, sig = token.split(".", 1)
        good = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, good):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload))
        if data["exp"] < time.time():
            return None
        return USERS.get(data["u"])
    except Exception:
        return None


def _auth(token):
    user = _verify(token or "")
    if not user:
        raise HTTPException(401, "غير مُصرّح — سجّل الدخول")
    return user


@app.post("/api/login")
async def login(body: dict):
    u = USERS.get((body or {}).get("username", ""))
    if not u or u["password"] != (body or {}).get("password", ""):
        raise HTTPException(401, "اسم المستخدم أو كلمة المرور غير صحيحة")
    return {"token": _sign(u["username"]),
            "user": {"name": u["name"], "role": u["role"], "username": u["username"]}}


@app.get("/api/me")
async def me(authorization: str = Header(default="")):
    u = _auth(authorization.replace("Bearer ", ""))
    return {"name": u["name"], "role": u["role"], "username": u["username"]}


@app.get("/api/library")
async def library(authorization: str = Header(default="")):
    _auth(authorization.replace("Bearer ", ""))
    return JSONResponse(CATALOG)


def _ranged(path: str, request: Request, media_type: str):
    """Manual HTTP Range so the browser PDF viewer and <video> can seek."""
    p = pathlib.Path(path)
    size = p.stat().st_size
    rng = request.headers.get("range")
    if rng and rng.startswith("bytes="):
        s, _, e = rng[6:].partition("-")
        start = int(s) if s else 0
        end = int(e) if e else size - 1
        end = min(end, size - 1)
        start = min(start, end)
        length = end - start + 1

        def it():
            with open(p, "rb") as f:
                f.seek(start)
                left = length
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    left -= len(chunk)
                    yield chunk
        return StreamingResponse(it(), status_code=206, media_type=media_type,
            headers={"Content-Range": f"bytes {start}-{end}/{size}",
                     "Accept-Ranges": "bytes", "Content-Length": str(length)})
    return FileResponse(path, media_type=media_type,
                        headers={"Accept-Ranges": "bytes"})


@app.get("/api/video/{kind}/{slug}")
async def video(kind: str, slug: str, request: Request, t: str = Query(default="")):
    _auth(t)  # <video> can't set headers — token via ?t=
    path = VIDEOS.get((kind, slug))
    if not path or not pathlib.Path(path).exists():
        raise HTTPException(404, "المقطع غير موجود")
    return _ranged(path, request, "video/mp4")


@app.get("/api/book")
async def book(request: Request, t: str = Query(default="")):
    _auth(t)
    path = VIDEOS.get(("book", "_"))
    if not path or not pathlib.Path(path).exists():
        raise HTTPException(404, "الكتاب غير موجود")
    return _ranged(path, request, "application/pdf")


@app.get("/api/health")
async def health():
    return {"ok": True, **CATALOG["counts"]}
