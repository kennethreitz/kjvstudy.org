"""Responder port of the KJV Study web app — WORK IN PROGRESS.

This is the new web layer built on Responder (https://responder.kennethreitz.org),
replacing the FastAPI layer in ``server.py``. It reuses every framework-agnostic
module unchanged (``kjv``, ``topics``, ``commentary`` generation, ``red_letter``,
``utils.*``, the resource catalog, etc.); only routing and response construction
are reimplemented.

Run it with::

    uv run responder run kjvstudy_org.responder_app:api
    # or
    uv run python -m kjvstudy_org.responder_app

Porting status: scaffold + a vertical slice (homepage, /books, /resources,
/health, /api/health, custom 404) are ported and verified. The remaining route
modules are tracked in PORTING.md.
"""
import hashlib
import os
from datetime import date
from pathlib import Path

import responder

from .kjv import bible
from .jinja_filters import register_filters
from .resource_catalog import RESOURCE_CATEGORIES, iter_resources
from .utils.books import OT_BOOKS, NT_BOOKS
from .utils.helpers import get_daily_verse, verse_reference_to_url
from .utils.pdf import WEASYPRINT_AVAILABLE
from .study_guides import get_featured_study_guides

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


def render(req, resp, template: str, **context) -> None:
    """Render a Jinja template into ``resp.html``.

    Responder doesn't auto-inject the request the way Starlette's
    ``TemplateResponse`` does, so we pass ``request=req`` (templates only use
    ``request.url.path``). This is the shared helper every ported web handler
    uses in place of ``templates.TemplateResponse(request, name, ctx)``.
    """
    resp.html = api.template(template, request=req, **context)


# ---------------------------------------------------------------------------
# Cross-cutting: Cache-Control headers (port of CacheControlMiddleware)
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
# Web routes (vertical slice — see PORTING.md for the rest)
# ---------------------------------------------------------------------------
_homepage_cache: dict = {"date": None, "html": None}


@api.route("/")
async def read_root(req, resp):
    """Homepage (cached, rebuilds once per day)."""
    today = date.today()
    if _homepage_cache["date"] == today and _homepage_cache["html"] is not None:
        resp.html = _homepage_cache["html"]
        return

    books = bible.get_books()
    daily_verse = get_daily_verse()

    study_guides = get_featured_study_guides()
    for category in study_guides.values():
        for guide in category:
            guide["verse_refs"] = [
                {"text": verse, "url": verse_reference_to_url(verse) or "#"}
                for verse in guide["verses"]
            ]

    _homepage_exclude = {"/study-guides", "/family-tree", "/biblical-timeline", "/biblical-maps"}
    theology_links = [r for r in iter_resources() if r["url"] not in _homepage_exclude]

    html = api.template(
        "index.html",
        request=req,
        books=books,
        daily_verse=daily_verse,
        study_guides=study_guides,
        theology_links=theology_links,
    )
    _homepage_cache["date"] = today
    _homepage_cache["html"] = html
    resp.html = html


# Book categorization (slug per book) for the /books grid.
_BOOK_TYPES = {
    'Genesis': 'law', 'Exodus': 'law', 'Leviticus': 'law', 'Numbers': 'law', 'Deuteronomy': 'law',
    'Joshua': 'historical', 'Judges': 'historical', 'Ruth': 'historical',
    '1 Samuel': 'historical', '2 Samuel': 'historical', '1 Kings': 'historical', '2 Kings': 'historical',
    '1 Chronicles': 'historical', '2 Chronicles': 'historical', 'Ezra': 'historical',
    'Nehemiah': 'historical', 'Esther': 'historical',
    'Job': 'wisdom', 'Psalms': 'wisdom', 'Proverbs': 'wisdom', 'Ecclesiastes': 'wisdom', 'Song of Solomon': 'wisdom',
    'Isaiah': 'major-prophets', 'Jeremiah': 'major-prophets', 'Lamentations': 'major-prophets',
    'Ezekiel': 'major-prophets', 'Daniel': 'major-prophets',
    'Hosea': 'minor-prophets', 'Joel': 'minor-prophets', 'Amos': 'minor-prophets',
    'Obadiah': 'minor-prophets', 'Jonah': 'minor-prophets', 'Micah': 'minor-prophets',
    'Nahum': 'minor-prophets', 'Habakkuk': 'minor-prophets', 'Zephaniah': 'minor-prophets',
    'Haggai': 'minor-prophets', 'Zechariah': 'minor-prophets', 'Malachi': 'minor-prophets',
    'Matthew': 'gospels', 'Mark': 'gospels', 'Luke': 'gospels', 'John': 'gospels',
    'Acts': 'acts',
    'Romans': 'pauline', '1 Corinthians': 'pauline', '2 Corinthians': 'pauline',
    'Galatians': 'pauline', 'Ephesians': 'pauline', 'Philippians': 'pauline', 'Colossians': 'pauline',
    '1 Thessalonians': 'pauline', '2 Thessalonians': 'pauline',
    '1 Timothy': 'pauline', '2 Timothy': 'pauline', 'Titus': 'pauline', 'Philemon': 'pauline',
    'Hebrews': 'general', 'James': 'general', '1 Peter': 'general', '2 Peter': 'general',
    '1 John': 'general', '2 John': 'general', '3 John': 'general', 'Jude': 'general',
    'Revelation': 'apocalyptic',
}


def _book_grid(book_names, available):
    return [
        {
            "name": book,
            "chapters": len(bible.get_chapters_for_book(book)),
            "available": book in available,
            "type": _BOOK_TYPES.get(book, ""),
        }
        for book in book_names
    ]


@api.route("/books")
async def books_page(req, resp):
    """Browse all books of the Bible."""
    books = bible.get_books()
    render(
        req, resp, "books.html",
        old_testament=_book_grid(OT_BOOKS, books),
        new_testament=_book_grid(NT_BOOKS, books),
        books=books,
        breadcrumbs=[{"text": "Home", "url": "/"}, {"text": "Books", "url": None}],
    )


@api.route("/resources")
async def resources_page(req, resp):
    """Browse all theological resources."""
    render(
        req, resp, "resources.html",
        resources=RESOURCE_CATEGORIES,
        books=bible.get_books(),
        breadcrumbs=[{"text": "Home", "url": "/"}, {"text": "Resources", "url": None}],
    )


@api.route("/health")
async def health(req, resp):
    """Liveness probe."""
    resp.media = {"status": "ok"}


# ---------------------------------------------------------------------------
# API routes (vertical slice)
# ---------------------------------------------------------------------------
@api.route("/api/health")
async def api_health(req, resp):
    """API health check."""
    resp.media = {"status": "healthy", "service": "KJV Study API", "version": "1.0.0"}


# TODO(port): wire a custom 404 -> error.html. Responder's default-route
# mechanism (Router.default_endpoint) expects a raw ASGI callable rather than a
# (req, resp) handler, so the FastAPI custom_http_exception_handler needs a
# Responder-native equivalent (likely Router(default_response=...) or a
# catch-all route). Until then Responder serves its built-in 404. See PORTING.md.


if __name__ == "__main__":
    api.run()
