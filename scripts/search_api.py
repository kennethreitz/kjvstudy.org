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
Uses granian for performance.
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

    static_dir = str(PROJECT_ROOT / "kjvstudy_org" / "static")

    subprocess.run([
        sys.executable, "-m", "granian",
        "kjvstudy_org.server:app",
        "--interface", "asgi",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--workers", str(workers),
        "--respawn-failed-workers",
        "--access-log",
        "--static-path-route", "/static",
        "--static-path-mount", static_dir,
        "--static-path-expires", "86400",
    ])
