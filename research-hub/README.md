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

## Adding a dataset

Copy a CSV into `data/` — that's it. The first row must be the header.
Refresh the hub and it appears on the home page, profiled and rendered.

## API

- `GET /api/datasets` — list of datasets with row counts and columns
- `GET /api/datasets/{slug}` — rows + column profiles for one dataset
