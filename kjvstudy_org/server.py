"""KJV Study web app, built on Responder (https://responder.kennethreitz.org).

Every framework-agnostic module is reused unchanged; routing and response
construction live here and in ``kjvstudy_org/routes/``. The ASGI app
is the module-level ``api``.

Run it::

    uv run granian kjvstudy_org.server:api --interface asgi --reload
    # or
    uv run python -m kjvstudy_org.server
"""
import hashlib
import os
from pathlib import Path

import responder
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .jinja_filters import register_filters
from .utils.pdf import WEASYPRINT_AVAILABLE
from .routes import register_all

_DIR = Path(__file__).parent
_STATIC_DIR = _DIR / "static"
_TEMPLATES_DIR = _DIR / "templates"


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
api = responder.API(
    title="KJV Study API",
    version="1.0.0",
    description=(
        "RESTful API for accessing King James Bible verses, chapters, "
        "and study resources"
    ),
    templates_dir=str(_TEMPLATES_DIR),
    static_dir=str(_STATIC_DIR),
    static_route="/static",
    openapi="3.0.2",
    docs_route="/api/docs",
    openapi_route="/api/openapi.json",
    gzip=True,
    request_id=True,
    request_timeout=30.0,
    problem_details=True,
    # Sessions are unused; disable them entirely (Responder 5.0.0+).
    sessions=False,
)


# ---------------------------------------------------------------------------
# Jinja environment: reuse the app's custom filters and globals
# ---------------------------------------------------------------------------
_env = api.templates._env
register_filters(_env)

_static_hashes: dict[str, str] = {}


def static_hash(filename: str) -> str:
    """Short content hash (by mtime) for cache-busting static asset URLs."""
    if filename not in _static_hashes:
        filepath = _STATIC_DIR / filename
        if filepath.exists():
            mtime = int(filepath.stat().st_mtime)
            _static_hashes[filename] = hashlib.md5(str(mtime).encode()).hexdigest()[:8]
        else:
            _static_hashes[filename] = "0"
    return _static_hashes[filename]


_env.globals["static_hash"] = static_hash
_env.globals["disable_analytics"] = os.getenv("DISABLE_ANALYTICS", "false").lower() == "true"
_env.globals["resource_pdf_available"] = WEASYPRINT_AVAILABLE
_env.globals["github_repo_url"] = "https://github.com/kennethreitz/kjvstudy.org"


# ---------------------------------------------------------------------------
# Cache-Control headers (port of CacheControlMiddleware)
# ---------------------------------------------------------------------------
@api.after_request()
def cache_control(req, resp):
    """Attach Cache-Control headers based on the request path."""
    path = req.url.path

    if path.startswith("/api/") or path in ("/verse-of-the-day", "/random-verse"):
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
    elif path.startswith("/static/"):
        if (resp.status_code or 200) < 400:
            resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            resp.headers["Cache-Control"] = "no-store"
    elif any(x in path for x in ("/book/", "/chapter/", "/verse/")):
        resp.headers["Cache-Control"] = "public, max-age=604800"
    elif any(x in path for x in (
        "/study-guides/", "/topics/", "/reading-plans/", "/biblical-",
        "/names-of-god", "/parables/", "/the-twelve-apostles/",
        "/women-of-the-bible/", "/tetragrammaton", "/commentary/",
    )):
        resp.headers["Cache-Control"] = "public, max-age=86400"
    elif path == "/":
        resp.headers["Cache-Control"] = "public, max-age=3600"
    elif path in ("/books", "/search", "/resources", "/strongs"):
        resp.headers["Cache-Control"] = "public, max-age=3600"
    elif path in ("/sitemap.xml", "/robots.txt"):
        resp.headers["Cache-Control"] = "public, max-age=86400"
    else:
        resp.headers["Cache-Control"] = "public, max-age=600"


# ---------------------------------------------------------------------------
# Operational middleware (ports of BotLogger / RateLimit / Timeout)
# ---------------------------------------------------------------------------
class BotLoggerMiddleware(BaseHTTPMiddleware):
    """Log requests from known bots/crawlers."""

    BOT_IDENTIFIERS = [
        'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider',
        'yandexbot', 'facebookexternalhit', 'twitterbot', 'rogerbot',
        'linkedinbot', 'embedly', 'quora link preview', 'showyoubot',
        'outbrain', 'pinterest', 'slackbot', 'vkshare', 'w3c_validator',
        'redditbot', 'applebot', 'whatsapp', 'flipboard', 'tumblr',
        'bitlybot', 'skypeuripreview', 'nuzzel', 'discordbot',
        'telegrambot', 'perplexitybot', 'amazonbot', 'claudebot',
        'anthropic-ai', 'gptbot', 'chatgpt-user', 'ccbot',
        'diffbot', 'bytespider', 'petalbot',
    ]

    async def dispatch(self, request, call_next):
        ua = request.headers.get("user-agent", "").lower()
        bot = next((b for b in self.BOT_IDENTIFIERS if b in ua), None)
        if bot:
            print(f"[BOT] {bot}")
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory per-IP sliding-window rate limiter."""

    def __init__(self, app, requests_per_second: float = 10.0):
        super().__init__(app)
        self.rate = requests_per_second
        self._buckets: dict[str, tuple[float, float]] = {}
        self._max_tokens = requests_per_second * 5

    async def dispatch(self, request, call_next):
        import time
        if request.url.path == "/health":
            return await call_next(request)
        ip = request.client.host if request.client else "unknown"
        if ip in ("127.0.0.1", "testclient"):
            return await call_next(request)
        now = time.monotonic()
        tokens, last = self._buckets.get(ip, (self._max_tokens, now))
        tokens = min(self._max_tokens, tokens + (now - last) * self.rate)
        if tokens < 1.0:
            return JSONResponse({"detail": "Too many requests"}, status_code=429,
                                headers={"Retry-After": "1"})
        self._buckets[ip] = (tokens - 1.0, now)
        if len(self._buckets) > 5000:
            cutoff = now - 60
            self._buckets = {k: (t, ts) for k, (t, ts) in self._buckets.items() if ts > cutoff}
        return await call_next(request)


api.add_middleware(RateLimitMiddleware, requests_per_second=10.0)
api.add_middleware(BotLoggerMiddleware)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
register_all(api)


# ---------------------------------------------------------------------------
# OpenAPI schema scope
# ---------------------------------------------------------------------------
# Responder 5.0.0 auto-documents *every* route in the OpenAPI spec, including
# all the HTML page routes. Keep the spec limited to the JSON API: exclude any
# route whose path does not start with "/api".
for _route in api.router.routes:
    _path = str(getattr(_route, "path_template", getattr(_route, "route", "")) or "")
    if _path.startswith("/api"):
        continue
    _endpoint = getattr(_route, "endpoint", None)
    if _endpoint is not None:
        _endpoint._include_in_schema = False


# Custom 404. Use the router's default_endpoint (an ASGI callable that fires
# only after every route AND mount has missed — so it does not shadow /static).
# Branded error page for web paths, JSON for the API. Mirrors
# server.custom_http_exception_handler.
from .kjv import bible
from starlette.requests import Request as _StarletteRequest
from starlette.responses import HTMLResponse as _HTMLResponse, JSONResponse as _JSONResponse


async def _not_found(scope, receive, send):
    path = scope.get("path", "")
    if path.startswith("/api/"):
        response = _JSONResponse({"detail": "Not Found"}, status_code=404)
    else:
        request = _StarletteRequest(scope, receive)
        html = api.template(
            "error.html", request=request,
            status_code=404, detail="Not Found", books=bible.get_books(),
        )
        response = _HTMLResponse(html, status_code=404)
    await response(scope, receive, send)


api.router.default_endpoint = _not_found


if __name__ == "__main__":
    # Serve with Granian (the production server) — consistent with main.py,
    # the Dockerfile, and docker-compose. Responder's api.run() would use uvicorn.
    from .main import main
    main()
