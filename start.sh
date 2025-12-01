#!/bin/sh
set -e

WORKERS=${WORKERS:-1}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

# Run the app directly with uvicorn (no nginx proxy)
exec uv run uvicorn kjvstudy_org.server:app \
    --host "${HOST}" \
    --port "${PORT}" \
    --workers "${WORKERS}" \
    --proxy-headers
