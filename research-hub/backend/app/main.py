"""Research Hub API: serves every CSV dropped into the data/ folder,
profiled so the frontend can pick an appropriate rendering."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .profiler import profile_file, read_csv

ROOT = Path(__file__).resolve().parents[2]

# Configuration (all overridable via environment, e.g. in Docker / Portainer).
DATA_DIR = Path(os.environ.get("RESEARCH_HUB_DATA_DIR", ROOT / "data"))
FRONTEND_DIST = Path(
    os.environ.get("RESEARCH_HUB_FRONTEND_DIST", ROOT / "frontend" / "dist")
)
APP_TITLE = os.environ.get("RESEARCH_HUB_TITLE", "Research Hub")
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get("RESEARCH_HUB_CORS_ORIGINS", "*").split(",")
    if o.strip()
] or ["*"]

app = FastAPI(title=APP_TITLE, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "title": APP_TITLE,
        "dataDir": str(DATA_DIR),
        "datasets": len(list_csv_files()),
    }


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


MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB


@app.post("/api/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)) -> dict:
    """Accept a CSV upload and save it into the data directory."""
    name = Path(file.filename or "").name
    if not name.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")

    content = await file.read()
    if not content.strip():
        raise HTTPException(status_code=400, detail="The file is empty")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 25 MB)")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    if "," not in text.splitlines()[0]:
        raise HTTPException(
            status_code=400, detail="First row must be a comma-separated header"
        )

    # Sanitise the filename and avoid silently overwriting an existing dataset.
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", name[:-4]).strip("-_") or "dataset"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dest = DATA_DIR / f"{safe}.csv"
    n = 2
    while dest.exists():
        dest = DATA_DIR / f"{safe}-{n}.csv"
        n += 1
    dest.write_bytes(content)

    slug = slugify(dest.stem)
    return {"slug": slug, "title": humanize(slug), "file": dest.name}


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
