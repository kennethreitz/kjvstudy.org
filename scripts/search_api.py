#!/usr/bin/env python3
"""FastAPI sidecar for kjvstudy.org static site deployment.

Handles routes that can't be pre-rendered as static HTML:
  - /search and /api/search (dynamic query)
  - /api/* (JSON API endpoints)
  - /*/pdf (on-demand PDF generation)
  - /random-verse (server-side redirect fallback)
  - /verse-of-the-day (redirect to today's date)
  - /og/* (dynamic OG images)

Runs on port 8001, proxied by nginx.
Uses gunicorn with uvicorn workers for resilience.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.server import app  # noqa: E402, F401

if __name__ == "__main__":
    port = int(os.getenv("SIDECAR_PORT", "8001"))
    workers = int(os.getenv("SIDECAR_WORKERS", "1"))

    subprocess.run([
        sys.executable, "-m", "gunicorn",
        "kjvstudy_org.server:app",
        "--worker-class", "uvicorn.workers.UvicornWorker",
        "--bind", f"0.0.0.0:{port}",
        "--workers", str(workers),
        "--max-requests", "1000",
        "--max-requests-jitter", "200",
        "--timeout", "60",
        "--graceful-timeout", "10",
        "--forwarded-allow-ips", "*",
        "--log-level", "warning",
        "--access-logfile", "-",
    ])
