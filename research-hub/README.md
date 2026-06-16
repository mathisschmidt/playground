# Research Hub

A self-adapting viewer for research CSVs. Drop any CSV (companies, products,
papers, whatever an LLM generated for you) into `data/` and the hub renders it
with a layout that fits the content — no per-dataset code required.

## How it adapts

The Python backend profiles every column and assigns it a **type** and a
**semantic role**; the Vue frontend picks UI from those roles:

| Detected             | Rendered as                                  |
| -------------------- | -------------------------------------------- |
| Mostly-unique text   | Card title                                   |
| Low-cardinality text | Colour-coded chips + facet filters + charts  |
| Long free text       | Card description                             |
| URLs                 | Clickable links                              |
| Years / numbers      | Metric badges, range KPI, timeline chart     |
| Other short text     | Subtitle / detail rows                       |

Each dataset gets three views — **Cards**, **Table** (sortable), and
**Insights** (distribution charts) — plus full-text search and faceted
filters with live counts.

## Stack

- **Backend** — Python, FastAPI (`backend/`): discovers `data/*.csv`, profiles
  columns, serves JSON and the built frontend.
- **Frontend** — Vue 3, Vite, Tailwind CSS v4, vue-router (`frontend/`).

## Run it

```bash
# 1. backend deps (once)
pip install -r backend/requirements.txt

# 2. frontend build (once per frontend change)
cd frontend && npm install && npm run build && cd ..

# 3. serve everything on http://localhost:8000
cd backend && uvicorn app.main:app --port 8000
```

Or just `./run.sh`.

### Development mode (hot reload)

```bash
cd backend && uvicorn app.main:app --reload --port 8000   # terminal 1
cd frontend && npm run dev                                # terminal 2 → http://localhost:5173
```

The Vite dev server proxies `/api` to the backend.

## Docker

A multi-stage build produces one image that serves both the API and the built
UI. Configure everything through environment variables — copy `.env.example`
to `.env` and edit, or set them in Portainer.

### Production (single container)

```bash
cp .env.example .env          # optional — sensible defaults exist
docker compose up -d --build  # -> http://localhost:8000 (HUB_PORT)
```

The `data/` folder is mounted into the container (`HUB_DATA_PATH`), so you can
drop new CSVs in and they appear immediately — no rebuild.

### Development (hot reload, two containers)

```bash
docker compose -f docker-compose.dev.yml up --build
# UI with hot reload -> http://localhost:5173
# API                -> http://localhost:8000
```

### Tests

```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
# runs pytest in the backend image; the exit code reflects pass/fail
```

### Portainer

1. **Stacks → Add stack → Repository** (point at this repo, compose path
   `research-hub/docker-compose.yml`) — or use the **Web editor** and paste the
   file.
2. Add the variables from `.env.example` under **Environment variables**
   (at minimum set `HUB_PORT` and, if you want a host folder for CSVs,
   `HUB_DATA_PATH`).
3. **Deploy the stack.** The container has a healthcheck on `/api/health`, so
   Portainer shows it as healthy once it's up.

### Environment variables

| Variable                     | Default          | Purpose                                   |
| ---------------------------- | ---------------- | ----------------------------------------- |
| `RESEARCH_HUB_TITLE`         | `Research Hub`   | UI / API title                            |
| `RESEARCH_HUB_CORS_ORIGINS`  | `*`              | Allowed CORS origins (comma-separated)    |
| `RESEARCH_HUB_DATA_DIR`      | `/app/data`      | Where the backend reads CSVs (in-container)|
| `HUB_PORT`                   | `8000`           | Published host port (production)          |
| `HUB_DATA_PATH`              | `./data`         | Host folder mounted as the dataset dir    |
| `HUB_IMAGE`                  | `research-hub:latest` | Image tag                            |
| `HUB_CONTAINER_NAME`         | `research-hub`   | Container name                            |
| `HUB_RESTART`                | `unless-stopped` | Restart policy                            |
| `HUB_WEB_PORT`               | `5173`           | Vite UI port (dev)                        |
| `HUB_API_PORT`               | `8000`           | Backend port (dev)                        |

## Adding a dataset

Copy a CSV into `data/` — that's it. The first row must be the header.
Refresh the hub and it appears on the home page, profiled and rendered.

## API

- `GET /api/health` — liveness + dataset count (used by the Docker healthcheck)
- `GET /api/datasets` — list of datasets with row counts and columns
- `GET /api/datasets/{slug}` — rows + column profiles for one dataset
