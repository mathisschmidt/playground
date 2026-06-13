"""Research Hub API: serves every CSV dropped into the data/ folder,
profiled so the frontend can pick an appropriate rendering."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .profiler import profile_file, read_csv

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
FRONTEND_DIST = ROOT / "frontend" / "dist"

app = FastAPI(title="Research Hub", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def humanize(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def list_csv_files() -> dict[str, Path]:
    if not DATA_DIR.exists():
        return {}
    return {slugify(p.stem): p for p in sorted(DATA_DIR.glob("*.csv"))}


@app.get("/api/datasets")
def datasets() -> list[dict]:
    out = []
    for slug, path in list_csv_files().items():
        header, rows = read_csv(path)
        out.append(
            {
                "slug": slug,
                "title": humanize(slug),
                "file": path.name,
                "rowCount": len(rows),
                "columns": header,
                "modified": datetime.fromtimestamp(
                    path.stat().st_mtime, tz=timezone.utc
                ).isoformat(),
            }
        )
    return out


@app.get("/api/datasets/{slug}")
def dataset(slug: str) -> dict:
    path = list_csv_files().get(slug)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Unknown dataset: {slug}")
    payload = profile_file(path)
    payload["slug"] = slug
    payload["title"] = humanize(slug)
    payload["file"] = path.name
    return payload


# In production, serve the built frontend from the same server. Unknown
# paths fall back to index.html so vue-router deep links work.
if FRONTEND_DIST.exists():

    class SpaStaticFiles(StaticFiles):
        async def get_response(self, path, scope):
            try:
                response = await super().get_response(path, scope)
            except StarletteHTTPException as exc:
                if exc.status_code != 404:
                    raise
                return await super().get_response("index.html", scope)
            if response.status_code == 404:
                response = await super().get_response("index.html", scope)
            return response

    app.mount("/", SpaStaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
