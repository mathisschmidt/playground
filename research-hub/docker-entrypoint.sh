#!/bin/sh
# Sync bundled datasets into the (possibly volume-mounted) data dir so CSVs
# committed to the repo show up on redeploy, without clobbering user uploads.
set -e

DATA_DIR="${RESEARCH_HUB_DATA_DIR:-/app/data}"
SEED_DIR="/app/seed-data"

mkdir -p "$DATA_DIR"
if [ -d "$SEED_DIR" ]; then
  for f in "$SEED_DIR"/*.csv; do
    [ -e "$f" ] || continue
    base=$(basename "$f")
    if [ ! -e "$DATA_DIR/$base" ]; then
      cp "$f" "$DATA_DIR/$base"
      echo "[entrypoint] seeded dataset: $base"
    fi
  done
fi

exec "$@"
