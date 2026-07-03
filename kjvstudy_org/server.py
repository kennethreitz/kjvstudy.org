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
import json
import os
from pathlib import Path

import responder
from responder.ext.ratelimit import RateLimiter

from .jinja_filters import register_filters
from .kjv import bible
from .utils.pdf import WEASYPRINT_AVAILABLE
from .routes import register_all

_DIR = Path(__file__).parent
_STATIC_DIR = _DIR / "static"
_TEMPLATES_DIR = _DIR / "templates"


def _allowed_hosts():
    """Hostnames accepted by the app (Host-header injection guard).

    Comma-separated via ``ALLOWED_HOSTS``; unset means all hosts, so local
    dev and the test client keep working without configuration.
    """
    hosts = os.getenv("ALLOWED_HOSTS", "")
    return [h.strip() for h in hosts.split(",") if h.strip()] or None


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
    # The KJV text never changes: hash GET responses so revalidating clients
    # get 304s instead of full page bodies.
    auto_etag=True,
    security_headers=True,
    allowed_hosts=_allowed_hosts(),
    enable_logging=True,
    metrics_route="/metrics",
    health_route="/health",
    # Sessions are unused; disable them entirely (Responder 5.0.0+).
    sessions=False,
)

api.add_health_check("bible", lambda: bible.get_verse_count() == 31102)
api.add_health_check("books", lambda: len(bible.get_books()) == 66)


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

    if (
        path.startswith("/api/")
        or path in ("/verse-of-the-day", "/random-verse", "/health", "/metrics")
    ):
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
# Rate limiting & bot logging (before-request hooks)
# ---------------------------------------------------------------------------
# 100 requests per sliding 10-second window per client — the same average as
# the old token bucket (10 req/s, burst headroom). Keyed by X-Forwarded-For
# since production sits behind a reverse proxy.
_limiter = RateLimiter(requests=100, period=10, trust_proxy_headers=True)

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


@api.route(before_request=True)
async def operational_hooks(req, resp):
    """Log known crawlers; rate-limit everyone but local/monitoring traffic."""
    ua = req.headers.get("user-agent", "").lower()
    bot = next((b for b in BOT_IDENTIFIERS if b in ua), None)
    if bot:
        api.log.info("[BOT] %s", bot)

    if req.url.path in ("/health", "/metrics"):
        return
    if req.client and req.client[0] in ("127.0.0.1", "::1", "testclient"):
        return
    await _limiter.acheck(req, resp)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
register_all(api)


# ---------------------------------------------------------------------------
# OpenAPI schema scope
# ---------------------------------------------------------------------------
# Responder auto-documents *every* route in the OpenAPI spec, including
# all the HTML page routes. Keep the spec limited to the JSON API: exclude any
# route whose path does not start with "/api".
for _route in api.router.routes:
    _path = str(getattr(_route, "path_template", getattr(_route, "route", "")) or "")
    if _path.startswith("/api"):
        continue
    _endpoint = getattr(_route, "endpoint", None)
    if _endpoint is not None:
        _endpoint._include_in_schema = False


# ---------------------------------------------------------------------------
# Error pages: branded HTML for web paths, JSON for the API
# ---------------------------------------------------------------------------
# Unmatched routes raise HTTPException(404), which lands here via the
# exception middleware; handlers that 404 themselves render their own pages
# (see routes/_helpers.abort_404).
# The handlers set resp.content + resp.mimetype (rather than resp.media /
# resp.html) because the exception-handler adapter only forwards the headers
# derived from the body — the content path is the one that carries Content-Type.
def _error_response(req, resp, status_code, detail):
    resp.status_code = status_code
    if req.url.path.startswith("/api/"):
        resp.content = json.dumps({"detail": detail})
        resp.mimetype = "application/json"
        return
    try:
        resp.content = api.template(
            "error.html", request=req,
            status_code=status_code, detail=detail, books=bible.get_books(),
        )
        resp.mimetype = "text/html"
    except Exception:  # never let the error page itself take the response down
        resp.content = detail
        resp.mimetype = "text/plain"


@api.exception_handler(404)
async def not_found(req, resp, exc):
    _error_response(req, resp, 404, "Not Found")


@api.exception_handler(500)
async def server_error(req, resp, exc):
    _error_response(req, resp, 500, "Internal Server Error")


if __name__ == "__main__":
    # Serve with Granian (the production server) — consistent with main.py,
    # the Dockerfile, and docker-compose. Responder's api.run() would use uvicorn.
    from .main import main
    main()
