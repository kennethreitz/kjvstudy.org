import hashlib
import json
import os
import re
import random
import time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path as PathLib

from fastapi import FastAPI, HTTPException, Request, Query, Path
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .kjv import bible, VerseReference
from .cross_references import get_cross_references
from .reading_plans import get_plan, get_all_plans, get_plan_summary
from .topics import get_all_topics, get_topic_with_text, search_topics
from .interlinear_loader import get_interlinear_data, has_interlinear_data, get_all_interlinear_verses, preload_data, find_verses_by_strongs, count_strongs_occurrences
from .strongs import format_strongs_entry, search_strongs, get_all_strongs
from .books import get_book_data, has_book_data

# Import from modular packages
from .routes import (
    api_router,
    resources_router,
    family_tree_router,
    study_guides_router,
    commentary_router,
    stories_router,
    utility_router,
    bible_router, init_bible_commentary,
    reading_plans_router,
    topics_router,
    strongs_router,
    timeline_router,
    about_router,
    main_router,
    misc_router, init_search_family_tree,
)
from .routes.commentary import (
    generate_commentary,
    generate_chapter_overview,
    generate_book_commentary,
    generate_word_study_sidenotes,
)
from .utils.books import normalize_book_name, OT_BOOKS, NT_BOOKS
from .utils.helpers import (
    create_slug, get_verse_text, get_related_content,
    get_chapter_popularity_score, get_chapter_popularity_explanation,
    is_verse_reference, parse_verse_reference
)
from .utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf, render_html_to_pdf_async
from .utils.search import perform_full_text_search
from .utils.family_tree import search_family_tree


# Note: Helper functions (create_slug, normalize_book_name, get_related_content,
# get_chapter_popularity_score, get_chapter_popularity_explanation, get_verse_text,
# is_verse_reference, parse_verse_reference, perform_full_text_search, etc.)
# are now imported from utils modules above.


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    # Initialize search index for fast searches
    from .utils.search import ensure_search_index
    ensure_search_index()

    if os.getenv("PRELOAD_INTERLINEAR", "false").lower() == "true":
        preload_data()
    yield
    # Shutdown (nothing needed currently)


app = FastAPI(
    title="KJV Study API",
    description="RESTful API for accessing King James Bible verses, chapters, and study resources",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Include the API router (routes defined in routes/api.py)
app.include_router(api_router)

# Include the resources router (biblical resources, defined in routes/resources.py)
app.include_router(resources_router)

# Include the family tree router
app.include_router(family_tree_router)

# Include the study guides router
app.include_router(study_guides_router)

# Include the commentary router
app.include_router(commentary_router)

# Include the stories router
app.include_router(stories_router)

# Include the utility router (sitemap, robots.txt, health)
app.include_router(utility_router)

# Include the Bible router (book, chapter, verse, interlinear routes)
app.include_router(bible_router)

# Include the reading plans router
app.include_router(reading_plans_router)

# Include the topics router
app.include_router(topics_router)

# Include the Strong's Concordance router
app.include_router(strongs_router)

# Include the timeline router
app.include_router(timeline_router)

# Include the about router
app.include_router(about_router)

# Include the main router (homepage, books, resources)
app.include_router(main_router)

# Include the misc router (search, interlinear, random-verse, verse-of-the-day)
app.include_router(misc_router)


# Custom OpenAPI schema to only include /api routes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Filter paths to only include /api routes
    filtered_paths = {
        path: path_item
        for path, path_item in openapi_schema["paths"].items()
        if path.startswith("/api/")
    }

    openapi_schema["paths"] = filtered_paths
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Caching middleware for performance optimization
class CacheControlMiddleware(BaseHTTPMiddleware):
    """Add cache control headers to responses for better performance."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path = request.url.path

        # No caching for API endpoints and dynamic content
        if path.startswith("/api/") or path in ["/verse-of-the-day", "/random-verse"]:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        # Static files (CSS, JS, images) - cache 1 year, but ONLY on success.
        # Never cache a 404/500 as immutable, or a transient outage poisons the
        # client cache for a year.
        elif path.startswith("/static/"):
            if response.status_code < 400:
                response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
            else:
                response.headers["Cache-Control"] = "no-store"
        # Bible content (verses, chapters, books) - cache 1 week
        elif any(x in path for x in ["/book/", "/chapter/", "/verse/"]):
            response.headers["Cache-Control"] = "public, max-age=604800"
        # Study resources and special pages - cache 1 day
        elif any(x in path for x in ["/study-guides/", "/topics/", "/reading-plans/",
                                      "/biblical-", "/names-of-god", "/parables/",
                                      "/the-twelve-apostles/", "/women-of-the-bible/",
                                      "/tetragrammaton", "/commentary/"]):
            response.headers["Cache-Control"] = "public, max-age=86400"
        # Homepage - cache 1 hour
        elif path == "/":
            response.headers["Cache-Control"] = "public, max-age=3600"
        # Main sections - cache 1 hour
        elif path in ["/books", "/search", "/resources", "/strongs"]:
            response.headers["Cache-Control"] = "public, max-age=3600"
        # Sitemap and robots.txt - cache 1 day
        elif path in ["/sitemap.xml", "/robots.txt"]:
            response.headers["Cache-Control"] = "public, max-age=86400"
        # Default - cache 10 minutes
        else:
            response.headers["Cache-Control"] = "public, max-age=600"

        return response


# Bot detection and logging middleware
class BotLoggerMiddleware(BaseHTTPMiddleware):
    """Log requests from bots/crawlers only"""

    # Common bot identifiers to detect
    BOT_IDENTIFIERS = [
        'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider',
        'yandexbot', 'facebookexternalhit', 'twitterbot', 'rogerbot',
        'linkedinbot', 'embedly', 'quora link preview', 'showyoubot',
        'outbrain', 'pinterest', 'slackbot', 'vkshare', 'w3c_validator',
        'redditbot', 'applebot', 'whatsapp', 'flipboard', 'tumblr',
        'bitlybot', 'skypeuripreview', 'nuzzel', 'discordbot',
        'telegrambot', 'perplexitybot', 'amazonbot', 'claudebot',
        'anthropic-ai', 'gptbot', 'chatgpt-user', 'ccbot',
        'diffbot', 'bytespider', 'petalbot'
    ]

    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("user-agent", "").lower()

        # Check if this is a bot
        is_bot = any(bot in user_agent for bot in self.BOT_IDENTIFIERS)

        if is_bot:
            # Extract the bot name for cleaner logging
            bot_name = next((bot for bot in self.BOT_IDENTIFIERS if bot in user_agent), "unknown bot")
            print(f"[BOT] {bot_name}")

        response = await call_next(request)
        return response


# Rate limiting middleware — per-IP request throttle
class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory per-IP rate limiter using a sliding window."""

    def __init__(self, app, requests_per_second: float = 10.0):
        super().__init__(app)
        self.rate = requests_per_second
        # {ip: (token_count, last_refill_time)}
        self._buckets: dict[str, tuple[float, float]] = {}
        self._max_tokens = requests_per_second * 5  # burst allowance

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and local/test clients
        if request.url.path == "/health":
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        if ip in ("127.0.0.1", "testclient"):
            return await call_next(request)
        now = time.monotonic()

        tokens, last = self._buckets.get(ip, (self._max_tokens, now))
        elapsed = now - last
        tokens = min(self._max_tokens, tokens + elapsed * self.rate)

        if tokens < 1.0:
            return JSONResponse(
                {"detail": "Too many requests"},
                status_code=429,
                headers={"Retry-After": "1"},
            )

        self._buckets[ip] = (tokens - 1.0, now)

        # Periodic cleanup — evict stale entries every ~1000 requests
        if len(self._buckets) > 5000:
            cutoff = now - 60
            self._buckets = {
                k: (t, ts) for k, (t, ts) in self._buckets.items() if ts > cutoff
            }

        return await call_next(request)


# Request timeout middleware — kill requests that take too long
class TimeoutMiddleware(BaseHTTPMiddleware):
    """Cancel requests that exceed a time limit."""

    def __init__(self, app, timeout_seconds: float = 30.0):
        super().__init__(app)
        self.timeout = timeout_seconds

    async def dispatch(self, request: Request, call_next):
        import asyncio
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            return JSONResponse(
                {"detail": "Request timeout"},
                status_code=504,
            )


# Add GZip compression middleware (compress responses > 1000 bytes)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add caching middleware
app.add_middleware(CacheControlMiddleware)

# Add bot logging middleware
app.add_middleware(BotLoggerMiddleware)

# Add rate limiting (10 req/s per IP, burst of 50)
app.add_middleware(RateLimitMiddleware, requests_per_second=10.0)

# Add request timeout (30 seconds max, 60 for PDFs handled by route-level timeout)
app.add_middleware(TimeoutMiddleware, timeout_seconds=30.0)


# Set up Jinja2 templates and static files
current_dir = PathLib(__file__).parent
static_dir = current_dir / "static"

from .routes._templates import templates

# Register custom Jinja2 filters
from .jinja_filters import register_filters
register_filters(templates.env)

# Add global template variables
templates.env.globals['disable_analytics'] = os.getenv("DISABLE_ANALYTICS", "false").lower() == "true"

# Cache-busting for static files using file modification time
import hashlib
_static_hashes = {}

def static_hash(filename):
    """Generate a short hash based on file modification time for cache busting."""
    if filename not in _static_hashes:
        filepath = static_dir / filename
        if filepath.exists():
            mtime = int(filepath.stat().st_mtime)
            _static_hashes[filename] = hashlib.md5(str(mtime).encode()).hexdigest()[:8]
        else:
            _static_hashes[filename] = "0"
    return _static_hashes[filename]

templates.env.globals['static_hash'] = static_hash
templates.env.globals['resource_pdf_available'] = WEASYPRINT_AVAILABLE
templates.env.globals['github_repo_url'] = "https://github.com/kennethreitz/kjvstudy.org"

# Serve /static from the app itself so styling works under any ASGI server
# (uvicorn, granian, etc.). In production Granian also mounts /static via its
# own --static-path-route and short-circuits before reaching this app, so this
# mount is a harmless fallback there but the source of truth for `uvicorn`.
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize commentary functions for the Bible route module
init_bible_commentary(generate_commentary, generate_chapter_overview, generate_book_commentary, generate_word_study_sidenotes)



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom error handler that renders our error template"""
    if exc.status_code == 404:
        books = bible.get_books()
        return templates.TemplateResponse(
            request,
            "error.html",
            {
                "status_code": exc.status_code,
                "detail": exc.detail,
                "books": books,
            },
            status_code=exc.status_code,
        )

    # For other errors, use the default handler
    return await http_exception_handler(request, exc)



# Initialize the search_family_tree function in misc routes
init_search_family_tree(search_family_tree)
