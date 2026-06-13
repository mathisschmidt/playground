#!/usr/bin/env bash
# Build the frontend (if needed) and serve the hub on http://localhost:8000
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d frontend/node_modules ]; then
  (cd frontend && npm install)
fi
(cd frontend && npm run build)

pip install -q -r backend/requirements.txt
cd backend && exec uvicorn app.main:app --port 8000
