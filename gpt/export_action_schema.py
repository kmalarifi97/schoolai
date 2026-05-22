"""Export the OpenAPI schema for the Custom GPT **Action**.

Imports the FastAPI app, keeps only the read-only `/gpt/*` endpoints, injects
the public server URL, and writes a self-contained schema you paste into the
GPT editor's Actions box.

    PUBLIC_API_URL=https://api.example.com python3 gpt/export_action_schema.py

If PUBLIC_API_URL is unset, a clearly-marked placeholder is written — replace
it before publishing (ChatGPT cannot reach localhost).

Writes: gpt/action_schema.json
"""
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "web" / "backend"))

import app as backend  # noqa: E402  (needs sys.path tweak above)

PLACEHOLDER = "https://REPLACE-WITH-YOUR-DEPLOYED-API.example.com"
OUT = pathlib.Path(__file__).resolve().parent / "action_schema.json"


def main():
    schema = backend.app.openapi()

    # Keep only the GPT-facing, read-only routes.
    schema["paths"] = {p: v for p, v in schema["paths"].items() if p.startswith("/gpt")}

    url = os.environ.get("PUBLIC_API_URL", "").strip() or PLACEHOLDER
    schema["servers"] = [{"url": url}]
    schema["info"]["title"] = "Physics 2 Library — GPT Action"
    schema["info"]["description"] = (
        "Read-only curriculum metadata for the Physics 2 tutor GPT: list and "
        "search concepts, and resolve a concept to its lesson, book pages, and "
        "PhET simulation link."
    )

    OUT.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  (server: {url})")
    if url == PLACEHOLDER:
        print("  NOTE: placeholder server — set PUBLIC_API_URL and re-run before publishing.")


if __name__ == "__main__":
    main()
