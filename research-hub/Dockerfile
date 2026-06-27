# syntax=docker/dockerfile:1

# ---------- Stage 1: build the Vue frontend ----------
FROM node:22-alpine AS frontend
WORKDIR /build/frontend

# Install deps first for better layer caching.
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build
# -> produces /build/frontend/dist

# ---------- Stage 2: Python backend (also used for dev & test) ----------
FROM python:3.11-slim AS backend-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    RESEARCH_HUB_DATA_DIR=/app/data \
    RESEARCH_HUB_FRONTEND_DIST=/app/frontend/dist \
    PORT=8000

WORKDIR /app

# Backend dependencies (+ pytest for the test stage/target).
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt pytest httpx

COPY backend/ ./backend/
COPY data/ ./data/

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser
WORKDIR /app/backend

EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

# ---------- Stage 3: production image (API + built UI) ----------
FROM backend-base AS runtime

USER root

# Built frontend from stage 1 (served by the backend).
COPY --from=frontend --chown=appuser:appuser /build/frontend/dist /app/frontend/dist

# Keep a pristine copy of the bundled datasets; the entrypoint syncs any that
# are missing into the data volume on start, so repo CSVs appear on redeploy.
COPY --chown=appuser:appuser data/ /app/seed-data/
COPY --chown=appuser:appuser docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen(f\"http://127.0.0.1:{os.environ.get('PORT','8000')}/api/health\")" || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
