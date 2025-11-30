import hashlib
import json
import os
import re
import random
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path as PathLib
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, Query, Path
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .kjv import bible, VerseReference
from .cross_references import get_cross_references
from .reading_plans import get_plan, get_all_plans, get_plan_summary
from .topics import get_all_topics, get_topic, search_topics
from .interlinear_loader import get_interlinear_data, has_interlinear_data, get_all_interlinear_verses, preload_data, find_verses_by_strongs, count_strongs_occurrences
from .strongs import format_strongs_entry, search_strongs, get_all_strongs
from .books import get_book_data, has_book_data

# Import from modular packages
from .routes import (
    api_router, init_api_templates,
    resources_router, init_resources_templates,
    family_tree_router, init_family_tree_templates,
    study_guides_router, init_study_guides_templates,
    commentary_router, init_commentary_templates,
    stories_router, init_stories_templates,
    utility_router,
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
    get_daily_verse, FEATURED_VERSES, is_verse_reference, parse_verse_reference
)
from .utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf, render_html_to_pdf_async
from .utils.search import perform_full_text_search

try:
    from ged4py import GedcomReader
except ImportError:
    GedcomReader = None


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
    """Add cache control headers to responses for better performance"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Skip caching for API endpoints and dynamic content
        if request.url.path.startswith("/api/") or request.url.path in ["/verse-of-the-day", "/random-verse"]:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        # Static files (CSS, JS, images) - cache for 1 year
        elif request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        # Bible content (verses, chapters, books) - cache for 1 week (rarely changes)
        elif any(x in request.url.path for x in ["/book/", "/chapter/", "/verse/"]):
            response.headers["Cache-Control"] = "public, max-age=604800"  # 1 week
        # Study resources and special pages - cache for 1 day
        elif any(x in request.url.path for x in ["/study-guides/", "/topics/", "/reading-plans/",
                                                   "/biblical-", "/names-of-god", "/parables/",
                                                   "/the-twelve-apostles/", "/women-of-the-bible/",
                                                   "/tetragrammaton", "/commentary/"]):
            response.headers["Cache-Control"] = "public, max-age=86400"  # 1 day
        # Homepage and main sections - cache for 1 hour
        elif request.url.path in ["/", "/books", "/search", "/resources", "/strongs"]:
            response.headers["Cache-Control"] = "public, max-age=3600"  # 1 hour
        # Sitemap and robots.txt - cache for 1 day
        elif request.url.path in ["/sitemap.xml", "/robots.txt"]:
            response.headers["Cache-Control"] = "public, max-age=86400"
        # Default - cache for 10 minutes
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
        'anthropic-ai', 'gptbot', 'chatgpt-user', 'ccbot', 'claudebot',
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


# Add GZip compression middleware (compress responses > 500 bytes)
app.add_middleware(GZipMiddleware, minimum_size=500)

# Add caching middleware
app.add_middleware(CacheControlMiddleware)

# Add bot logging middleware
app.add_middleware(BotLoggerMiddleware)


# Set up Jinja2 templates and static files
current_dir = PathLib(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Register custom Jinja2 filters
templates.env.filters['slugify'] = create_slug

# Add global template variables
templates.env.globals['disable_analytics'] = os.getenv("DISABLE_ANALYTICS", "false").lower() == "true"

# Initialize mistune for markdown rendering
import mistune

# Create mistune instance for full markdown (with paragraphs)
_markdown = mistune.create_markdown(escape=False, hard_wrap=False)

# Create inline renderer for markdown without paragraph wrapping
_inline_markdown = mistune.create_markdown(
    renderer=mistune.HTMLRenderer(escape=False),
    plugins=['strikethrough']
)

def markdown_inline(text):
    """Convert inline markdown to HTML (bold, italic, etc. - no paragraph wrapping)."""
    if not text:
        return text
    # Render and strip any outer <p> tags that mistune might add
    html = _inline_markdown(text).strip()
    if html.startswith('<p>') and html.endswith('</p>'):
        html = html[3:-4]
    return html

def markdown_to_html(text):
    """Convert markdown to HTML (bold, italic, paragraphs, etc.)."""
    if not text:
        return text
    return _markdown(text).strip()

templates.env.filters['md'] = markdown_to_html
templates.env.filters['mdi'] = markdown_inline

# Initialize templates for route modules
init_api_templates(templates)
init_resources_templates(templates)
init_family_tree_templates(templates)
init_study_guides_templates(templates)
init_commentary_templates(templates)
init_stories_templates(templates)

# Load Scofield commentary for cross-references
scofield_commentary = {}
try:
    scofield_path = static_dir / "scofield_commentary.json"
    with open(scofield_path, 'r') as f:
        scofield_commentary = json.load(f)
except Exception as e:
    print(f"Warning: Could not load Scofield commentary: {e}")


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


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = Query(None, description="Search query")):
    """Search page with results (includes Bible verses and family tree)"""
    books = bible.get_books()
    search_results = []
    family_tree_results = []
    is_direct_verse = False

    if q and len(q.strip()) >= 2:
        # Search Bible verses
        search_results = perform_full_text_search(q.strip())
        # Check if this was a direct verse reference match
        if search_results and len(search_results) == 1 and search_results[0].get("score") == 100.0:
            is_direct_verse = True

        # Also search family tree (limit to 5 results)
        family_tree_results = search_family_tree(q.strip(), limit=5)

    return templates.TemplateResponse(
            request,
            "search.html",
            {
            "query": q or "",
            "results": search_results,
            "family_tree_results": family_tree_results,
            "books": books,
            "total_results": len(search_results) + len(family_tree_results),
            "is_direct_verse": is_direct_verse
        }
    )

@app.get("/interlinear", response_class=HTMLResponse)
async def interlinear_landing_page(request: Request):
    """Landing page explaining interlinear Bible study"""
    books = bible.get_books()

    # Featured verses with interlinear data
    featured_verses = [
        {"reference": "John 3:16", "url": "/book/John/chapter/3/verse/16", "note": "God's love for the world"},
        {"reference": "Genesis 1:1", "url": "/book/Genesis/chapter/1/verse/1", "note": "In the beginning"},
        {"reference": "Psalm 23:1", "url": "/book/Psalms/chapter/23/verse/1", "note": "The Lord is my shepherd"},
        {"reference": "Romans 8:28", "url": "/book/Romans/chapter/8/verse/28", "note": "All things work together for good"},
        {"reference": "Matthew 28:19", "url": "/book/Matthew/chapter/28/verse/19", "note": "The Great Commission"},
        {"reference": "1 Corinthians 13:4", "url": "/book/1 Corinthians/chapter/13/verse/4", "note": "Love is patient"},
    ]

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Interlinear", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "interlinear_landing.html",
            {
            "books": books,
            "featured_verses": featured_verses,
            "breadcrumbs": breadcrumbs
        }
    )


def verse_reference_to_url(reference: str):
    """Convert a verse reference to a URL path.

    Examples:
        "John 3:16" -> "/book/John/chapter/3/verse/16"
        "Romans 8:38-39" -> "/book/Romans/chapter/8#verse-38-39"
        "Ephesians 2:8-9" -> "/book/Ephesians/chapter/2#verse-8-9"
    """
    # Pattern: Book Chapter:Verse or Book Chapter:Verse-Verse
    match = re.match(r'^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$', reference.strip())
    if not match:
        return None

    book = match.group(1).strip()
    chapter = match.group(2)
    verse_start = match.group(3)
    verse_end = match.group(4)

    if verse_end:
        # Verse range - link to chapter with anchor
        return f"/book/{book}/chapter/{chapter}#verse-{verse_start}-{verse_end}"
    else:
        # Single verse - link to verse page
        return f"/book/{book}/chapter/{chapter}/verse/{verse_start}"

@app.get("/random-verse")
async def random_verse(request: Request):
    """Redirect to a random Bible verse"""
    # Get all books
    all_books = bible.get_books()

    # Pick a random book
    book = random.choice(all_books)

    # Get all chapters for this book
    chapters = bible.get_chapters_for_book(book)

    # Pick a random chapter
    chapter = random.choice(chapters)

    # Get all verses for this chapter
    verses = bible.get_verses_by_book_chapter(book, chapter)

    # Pick a random verse
    verse = random.choice(verses)

    # Redirect to the verse page with cache control headers to ensure fresh random verse each time
    response = RedirectResponse(url=f"/book/{book}/chapter/{chapter}/verse/{verse.verse}", status_code=302)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/verse-of-the-day", response_class=HTMLResponse)
async def verse_of_the_day_page(request: Request):
    """Verse of the day page"""
    books = bible.get_books()
    daily_verse = get_daily_verse()

    # Generate past 30 days of verses
    past_verses = []
    today = datetime.now()
    for i in range(1, 31):  # Past 30 days (not including today)
        past_date = today - timedelta(days=i)
        date_str = past_date.strftime("%Y-%m-%d")
        verse = get_daily_verse(date_str)
        past_verses.append(verse)

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Verse of the Day", "url": "/verse-of-the-day"}
    ]

    return templates.TemplateResponse(
            request,
            "verse_of_the_day.html",
            {
            "books": books,
            "daily_verse": daily_verse,
            "past_verses": past_verses,
            "breadcrumbs": breadcrumbs
        }
    )

# Note: API routes have been moved to routes/api.py and are included via app.include_router(api_router)


def expand_book_abbreviation(abbrev):
    """Expand common Bible book abbreviations to full names"""
    abbreviations = {
        "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy",
        "Josh": "Joshua", "Judg": "Judges", "1 Sam": "1 Samuel", "2 Sam": "2 Samuel",
        "1 Kgs": "1 Kings", "2 Kgs": "2 Kings", "1 Chr": "1 Chronicles", "2 Chr": "2 Chronicles",
        "Neh": "Nehemiah", "Esth": "Esther", "Ps": "Psalms", "Prov": "Proverbs",
        "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah", "Jer": "Jeremiah",
        "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
        "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah", "Mic": "Micah",
        "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai",
        "Zech": "Zechariah", "Mal": "Malachi",
        "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
        "Rom": "Romans", "1 Cor": "1 Corinthians", "2 Cor": "2 Corinthians",
        "Gal": "Galatians", "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians",
        "1 Thess": "1 Thessalonians", "2 Thess": "2 Thessalonians",
        "1 Tim": "1 Timothy", "2 Tim": "2 Timothy", "Titus": "Titus", "Phlm": "Philemon",
        "Heb": "Hebrews", "Jas": "James", "1 Pet": "1 Peter", "2 Pet": "2 Peter",
        "1 John": "1 John", "2 John": "2 John", "3 John": "3 John", "Jude": "Jude",
        "Rev": "Revelation"
    }
    return abbreviations.get(abbrev, abbrev)


def parse_verses_from_notes(note_text):
    """Parse Bible verse references from GEDCOM NOTE fields"""
    if not note_text:
        return []

    verses = []
    # Match patterns like "Gen 4:1  Text here"
    import re
    pattern = r'([123]?\s?[A-Za-z]+)\s+(\d+):(\d+)\s+(.+?)(?=(?:[123]?\s?[A-Za-z]+\s+\d+:)|$)'

    matches = re.finditer(pattern, note_text, re.DOTALL)
    for match in matches:
        book_abbrev = match.group(1).strip()
        chapter = match.group(2)
        verse = match.group(3)
        text = match.group(4).strip()

        # Clean up text (remove line breaks and extra spaces)
        text = ' '.join(text.split())

        # Expand book abbreviation
        book_full = expand_book_abbreviation(book_abbrev)

        verses.append({
            "reference": f"{book_full} {chapter}:{verse}",
            "text": text
        })

    return verses


def parse_gedcom_to_tree_data(gedcom_path):
    """Parse GEDCOM file into our family tree format"""
    tree_data = {}
    
    # Parse with ged4py using the file path directly
    gedcom = GedcomReader(str(gedcom_path))

    # First pass: collect all individuals
    for record in gedcom.records0():
        if record.tag == 'INDI':
            person_id = str(record.xref_id).replace('@', '').replace('#', '').lower()

            # Get person name
            name = "Unknown"
            title = "Biblical Figure"
            for sub in record.sub_records:
                if sub.tag == 'NAME':
                    # Handle case where sub.value might be a tuple
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    name_value = str(value).replace('/', '').strip()
                    name = ' '.join(name_value.split())
                    break

            # Get occupation/title from OCCU tag
            for sub in record.sub_records:
                if sub.tag == 'OCCU':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    title = str(value)
                    break

            # Get notes for description and parse verses
            description = f"Biblical figure from {name}'s genealogy"
            note_verses = []
            for sub in record.sub_records:
                if sub.tag == 'NOTE':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    note_text = str(value)
                    description = note_text
                    # Parse verses from the note
                    note_verses = parse_verses_from_notes(note_text)
                    break

            # Get birth and death dates
            birth_year = "Unknown"
            death_year = "Unknown"
            age_at_death = "Unknown"
            
            for sub in record.sub_records:
                if sub.tag == 'BIRT':
                    for date_sub in sub.sub_records:
                        if date_sub.tag == 'DATE':
                            value = date_sub.value[0] if isinstance(date_sub.value, tuple) else date_sub.value
                            birth_year = str(value)
                elif sub.tag == 'DEAT':
                    for date_sub in sub.sub_records:
                        if date_sub.tag == 'DATE':
                            value = date_sub.value[0] if isinstance(date_sub.value, tuple) else date_sub.value
                            death_year = str(value)

            # Calculate age if we have both birth and death years
            if birth_year != "Unknown" and death_year != "Unknown":
                try:
                    birth_num = int(birth_year.split()[0]) if birth_year.split() else 0
                    death_num = int(death_year.split()[0]) if death_year.split() else 0
                    if death_num > birth_num:
                        age_at_death = f"{death_num - birth_num} years"
                except (ValueError, IndexError):
                    pass

            # Combine manually defined verses with verses from GEDCOM notes
            manual_verses = get_biblical_verses(name)
            all_verses = note_verses if note_verses else manual_verses

            person_data = {
                "name": name,
                "title": title,
                "description": description,
                "children": [],
                "parents": [],
                "siblings": [],
                "spouse": None,
                "verses": all_verses,
                "birth_year": birth_year,
                "death_year": death_year,
                "age_at_death": age_at_death
            }

            tree_data[person_id] = person_data

    # Second pass: collect family relationships
    for record in gedcom.records0():
        if record.tag == 'FAM':
            husband_id = None
            wife_id = None
            children = []

            for sub in record.sub_records:
                if sub.tag == 'HUSB':
                    # Handle case where sub.value might be a tuple
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    husband_id = str(value).replace('@', '').replace('#', '').lower()
                elif sub.tag == 'WIFE':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    wife_id = str(value).replace('@', '').replace('#', '').lower()
                elif sub.tag == 'CHIL':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    child_id = str(value).replace('@', '').replace('#', '').lower()
                    children.append(child_id)

            # Set spouse relationships
            if husband_id and husband_id in tree_data and wife_id and wife_id in tree_data:
                tree_data[husband_id]["spouse"] = tree_data[wife_id]["name"]
                tree_data[wife_id]["spouse"] = tree_data[husband_id]["name"]

            # Set parent-child relationships
            for child_id in children:
                if child_id in tree_data:
                    if husband_id and husband_id in tree_data:
                        tree_data[husband_id]["children"].append(child_id)
                        if husband_id not in tree_data[child_id]["parents"]:
                            tree_data[child_id]["parents"].append(husband_id)
                    if wife_id and wife_id in tree_data:
                        tree_data[wife_id]["children"].append(child_id)
                        if wife_id not in tree_data[child_id]["parents"]:
                            tree_data[child_id]["parents"].append(wife_id)

    # Third pass: calculate siblings
    # Siblings are people who share at least one parent
    for person_id, person in tree_data.items():
        siblings_set = set()

        # Find all people who share a parent with this person
        for parent_id in person["parents"]:
            if parent_id in tree_data:
                # Get all children of this parent
                for sibling_id in tree_data[parent_id]["children"]:
                    # Don't include the person themselves
                    if sibling_id != person_id:
                        siblings_set.add(sibling_id)

        # Convert set to list and store
        person["siblings"] = list(siblings_set)

    # Calculate generations using BFS from root people (those with no parents)
    generations = {}
    for person_id, person in tree_data.items():
        person["generation"] = None

    # Find root people (no parents)
    roots = [pid for pid, person in tree_data.items() if len(person["parents"]) == 0]

    # BFS to assign generation numbers (from Adam forward)
    queue = [(pid, 1) for pid in roots]
    visited = set()

    while queue:
        person_id, gen_num = queue.pop(0)
        if person_id in visited:
            continue
        visited.add(person_id)

        if person_id in tree_data:
            tree_data[person_id]["generation"] = gen_num

            # Add to generations dict
            if gen_num not in generations:
                generations[gen_num] = []
            generations[gen_num].append(person_id)

            # Add children to queue
            for child_id in tree_data[person_id]["children"]:
                if child_id not in visited:
                    queue.append((child_id, gen_num + 1))

    # Calculate Kekulé numbers (Ahnentafel numbering) from Christ
    # Find Jesus in the tree
    jesus_id = None
    for person_id, person in tree_data.items():
        if person["name"].lower() in ["jesus", "jesus christ", "christ"]:
            jesus_id = person_id
            break

    # Initialize all kekule_number to None
    for person_id, person in tree_data.items():
        person["kekule_number"] = None

    if jesus_id:
        # Kekulé numbering: person #1, father #2, mother #3
        # For person #n: father = 2n, mother = 2n+1
        # Work backwards from Christ using BFS
        queue = [(jesus_id, 1)]
        visited_reverse = set()

        while queue:
            person_id, kekule_num = queue.pop(0)
            if person_id in visited_reverse:
                continue
            visited_reverse.add(person_id)

            if person_id in tree_data:
                tree_data[person_id]["kekule_number"] = kekule_num

                # Get parents
                parents = tree_data[person_id]["parents"]

                # Assign Kekulé numbers to parents
                # Father = 2n (even), Mother = 2n+1 (odd)
                # We need to determine which parent is father/mother
                for i, parent_id in enumerate(parents):
                    if parent_id not in visited_reverse:
                        # Heuristic: check if parent has "male" indicators or is listed first
                        # For biblical genealogy, typically father is listed first
                        if i == 0:  # First parent = father
                            queue.append((parent_id, kekule_num * 2))
                        else:  # Second parent = mother
                            queue.append((parent_id, kekule_num * 2 + 1))

    return tree_data, generations


# Cache for family tree data to avoid reloading on every request
_family_tree_cache = None
_family_tree_generations_cache = None
_name_to_person_id_cache = None


def get_family_tree_data():
    """Load and cache family tree data (returns tree_data and generations)"""
    global _family_tree_cache, _family_tree_generations_cache, _name_to_person_id_cache

    if _family_tree_cache is None:
        static_dir = PathLib(__file__).parent / "static"
        gedcom_path = static_dir / "adameve.ged"

        if gedcom_path.exists():
            try:
                tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
                _family_tree_cache = tree_data
                _family_tree_generations_cache = generations

                # Build name to person_id mapping (case-insensitive)
                _name_to_person_id_cache = {}
                for person_id, person in tree_data.items():
                    name = person["name"]
                    # Store the full name
                    _name_to_person_id_cache[name.lower()] = person_id

                    # Handle compound names like "Sarai or Sarah" - split and store both
                    if " or " in name.lower():
                        name_variants = [n.strip() for n in name.split(" or ")]
                        for variant in name_variants:
                            if variant:  # Skip empty strings
                                _name_to_person_id_cache[variant.lower()] = person_id

            except Exception:
                _family_tree_cache = {}
                _family_tree_generations_cache = {}
                _name_to_person_id_cache = {}
        else:
            _family_tree_cache = {}
            _family_tree_generations_cache = {}
            _name_to_person_id_cache = {}

    return _family_tree_cache, _family_tree_generations_cache


def get_person_name_mapping():
    """Get the name to person ID mapping (ensures data is loaded first)"""
    # Trigger loading if needed
    get_family_tree_data()
    return _name_to_person_id_cache


def search_family_tree(query: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Search family tree for people matching the query.
    Returns list of matching people with their info.
    """
    results = []
    if not query or len(query.strip()) < 2:
        return results

    try:
        # Use cached family tree data
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            return results

        # Search for people
        query_lower = query.lower().strip()
        for person_id, person in family_tree_data.items():
            if query_lower in person["name"].lower():
                results.append({
                    "type": "person",
                    "id": person_id,
                    "name": person["name"],
                    "generation": person.get("generation"),
                    "birth_year": person.get("birth_year", "Unknown"),
                    "death_year": person.get("death_year", "Unknown"),
                    "url": f"/family-tree/person/{person_id}",
                    "description": f"Generation {person.get('generation', '?')} from Adam"
                })

        # Sort by relevance (exact matches first, then alphabetically)
        results.sort(key=lambda x: (
            0 if x["name"].lower() == query_lower else 1,
            x["name"]
        ))

        # Limit results if specified
        if limit is not None:
            return results[:limit]
        return results

    except Exception:
        return results


def link_person_names_in_text(text: str) -> str:
    """
    Find person names and verse references in text and link them.
    Links person names to family tree pages and verse references to verse pages.
    Avoids linking content that's already inside HTML tags.
    """
    if not text:
        return text

    # First, link verse references (e.g., "Genesis 3:15", "1 Samuel 2:1")
    # Pattern matches: Book name + chapter:verse
    verse_pattern = r'\b((?:1|2|3)\s)?([A-Z][a-z]+(?:\s+of\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def verse_replace_callback(match):
        matched_text = match.group(0)
        start_pos = match.start()

        # Check if we're inside an HTML tag
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')

        if last_lt > last_gt:
            return matched_text

        if last_lt != -1:
            tag_content = text[last_lt:start_pos]
            if 'href=' in tag_content or 'src=' in tag_content:
                return matched_text

        # Extract parts
        number_prefix = match.group(1) or ''  # "1 ", "2 ", etc.
        book_name = match.group(2)  # Main book name
        chapter = match.group(3)
        verse_start = match.group(4)
        verse_end = match.group(5)  # May be None

        # Construct full book name
        full_book = (number_prefix + book_name).strip()

        # Link to the first verse in the range
        return f'<a href="/book/{full_book}/chapter/{chapter}/verse/{verse_start}">{matched_text}</a>'

    text = re.sub(verse_pattern, verse_replace_callback, text)

    # Then, link person names to family tree
    name_to_id = get_person_name_mapping()

    if not name_to_id:
        return text

    # Sort names by length (longest first) to handle multi-word names correctly
    sorted_names = sorted(name_to_id.keys(), key=len, reverse=True)

    # Process each name
    for name_lower in sorted_names:
        person_id = name_to_id[name_lower]

        # Create a case-insensitive regex pattern with word boundaries
        # This will match the name but not if it's inside an HTML tag
        name_pattern = re.escape(name_lower)

        # Use a callback function to avoid replacing text inside HTML tags
        def replace_callback(match):
            matched_text = match.group(0)
            # Check if this match is inside an HTML tag
            start_pos = match.start()

            # Look backwards to see if we're inside a tag
            text_before = text[:start_pos]
            last_lt = text_before.rfind('<')
            last_gt = text_before.rfind('>')

            # If the last '<' is more recent than the last '>', we're inside a tag
            if last_lt > last_gt:
                return matched_text

            # Also check if we're inside an href or other attribute
            if last_lt != -1:
                tag_content = text[last_lt:start_pos]
                if 'href=' in tag_content or 'src=' in tag_content:
                    return matched_text

            # Safe to link
            return f'<a href="/family-tree/person/{person_id}">{matched_text}</a>'

        # Use word boundaries and case-insensitive matching
        pattern = r'\b' + name_pattern + r'\b'
        text = re.sub(pattern, replace_callback, text, flags=re.IGNORECASE)

    return text


# Register the custom Jinja2 filter for linking person names in templates
templates.env.filters['link_names'] = link_person_names_in_text


def link_verse_references_in_text(text):
    """Automatically link verse references in text (e.g., 'Genesis 1:1', 'Hebrews 9:22')"""
    if not text:
        return text

    # Pattern to match verse references like "Genesis 1:1", "1 Corinthians 5:7", "Romans 4:3"
    # Matches: BookName Chapter:Verse or BookName Chapter:Verse-Verse
    pattern = r'\b((?:1|2|3)\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def replace_reference(match):
        number_prefix = match.group(1) or ''  # "1 ", "2 ", "3 " or empty
        book_name = match.group(2)  # "Corinthians", "Kings", "Genesis"
        chapter = match.group(3)
        verse_start = match.group(4)
        verse_end = match.group(5)  # Could be None if no range

        # Construct full book name
        full_book = (number_prefix + book_name).strip()
        full_reference = match.group(0)

        # Check if this match is inside an HTML tag
        start_pos = match.start()
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')

        # If inside a tag, don't replace
        if last_lt > last_gt:
            return full_reference

        # Also check if we're inside an href or other attribute
        if last_lt != -1:
            tag_content = text[last_lt:start_pos]
            if 'href=' in tag_content or 'src=' in tag_content:
                return full_reference

        # Create link to verse page
        url = f'/book/{full_book}/chapter/{chapter}/verse/{verse_start}'
        return f'<a href="{url}">{full_reference}</a>'

    return re.sub(pattern, replace_reference, text)


# Register the verse reference linking filter
templates.env.filters['link_verses'] = link_verse_references_in_text


def inject_word_markers(text, word_studies, verse_num):
    """Inject sidenote markers into verse text next to annotated words"""
    if not word_studies:
        return text

    # Process each word study
    for idx, study in enumerate(word_studies, 1):
        word = study['word']
        # Create the sidenote marker HTML
        marker = f'<label for="sn-{verse_num}-word-{idx}" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-{verse_num}-word-{idx}" class="margin-toggle"/><span class="sidenote"><strong>{word}:</strong> {study["term"]} (<em>{study["translit"]}</em>). {study["note"]}</span>'

        # Find and replace the word with word + marker
        # Use a more precise replacement to avoid replacing partial matches
        import re
        # Match the word with word boundaries, but NOT if followed by possessive 's
        # This prevents breaking up "LORD'S" into "LORD" + "'S"
        pattern = re.compile(r'\b(' + re.escape(word) + r')(?!\'[sS])\b', re.IGNORECASE)
        text = pattern.sub(r'\1' + marker, text, count=1)

    return text

templates.env.filters['inject_word_markers'] = inject_word_markers


def red_letter(text, book, chapter, verse_num):
    """Wrap the words of Christ in red letter span tags"""
    from .red_letter import wrap_red_letter_text

    return wrap_red_letter_text(text, book, chapter, verse_num)

templates.env.filters['red_letter'] = red_letter


def format_numbered_lists(text):
    """Convert (1), (2), etc. patterns into HTML ordered lists"""
    import re

    # Pattern to find all numbered items like (1), (2), etc.
    item_pattern = r'\((\d+)\)\s*'

    # Find all numbered markers
    markers = list(re.finditer(item_pattern, text))

    if len(markers) < 2:
        return text

    # Check if markers are sequential starting from 1
    numbers = [int(m.group(1)) for m in markers]
    if numbers[0] != 1:
        return text

    # Find the longest sequential run starting from 1
    seq_length = 1
    for i in range(1, len(numbers)):
        if numbers[i] == seq_length + 1:
            seq_length += 1
        else:
            break

    if seq_length < 2:
        return text

    # Use only the sequential markers
    markers = markers[:seq_length]

    # Extract content for each item
    list_items = []
    for i, marker in enumerate(markers):
        start = marker.end()  # After the (N) marker

        if i + 1 < len(markers):
            # Content ends where next marker begins
            end = markers[i + 1].start()
        else:
            # Last item - find where it ends (next sentence or end of reasonable content)
            # Look for a period followed by a capital letter (new sentence) or end of text
            remaining = text[start:]
            # Find the end of this list item - look for period followed by space and capital
            # or semicolon, but capture meaningful content
            end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining)
            if end_match:
                end = start + end_match.start() + 1  # Include the period
            else:
                end = len(text)

        item_text = text[start:end].strip()
        # Clean up trailing punctuation
        item_text = item_text.rstrip(';,.')
        # Clean up trailing "and"
        if item_text.endswith(' and'):
            item_text = item_text[:-4]

        list_items.append(f'<li>{item_text}</li>')

    # Build the HTML list
    html_list = '<ol>' + ''.join(list_items) + '</ol>'

    # Find where to insert the list
    list_start = markers[0].start()

    # Find where the list content ends
    last_marker = markers[-1]
    last_item_start = last_marker.end()
    remaining_after_last = text[last_item_start:]

    # Find end of last item
    end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining_after_last)
    if end_match:
        list_end = last_item_start + end_match.start() + 1
    else:
        list_end = len(text)

    # Replace the numbered list portion with HTML
    after_list = text[list_end:].strip()
    if after_list:
        result = text[:list_start] + html_list + '</p><p>' + after_list
    else:
        result = text[:list_start] + html_list

    return result

templates.env.filters['format_lists'] = format_numbered_lists

def number_format(value):
    """Format a number with commas (e.g., 31102 -> 31,102)"""
    return f"{value:,}"

templates.env.filters['number_format'] = number_format


def linkify_strongs(text):
    """Convert Strong's references like G1234 or H5678 to links."""
    import re
    if not text:
        return text
    # Match G or H followed by digits, optionally in parentheses with Greek/Hebrew text
    pattern = r'\b([GH])(\d+)\b'
    def replace(match):
        prefix = match.group(1)
        num = match.group(2)
        return f'<a href="/strongs/{prefix}{num}" class="strongs-ref">{prefix}{num}</a>'
    return re.sub(pattern, replace, text)

templates.env.filters['linkify_strongs'] = linkify_strongs


def get_biblical_timeline_context():
    """
    Load comprehensive biblical timeline data from JSON file.

    Returns tuple of (timeline_events, introduction, chronology_note, chronology_comparison, conclusion)
    """
    # Load timeline data from JSON file
    data_dir = PathLib(__file__).parent / "data"
    timeline_path = data_dir / "biblical_timeline.json"

    with open(timeline_path, 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)

    timeline_events = timeline_data.get("timeline_events", {})
    introduction = timeline_data.get("introduction", "")
    chronology_note = timeline_data.get("chronology_note", "")
    chronology_comparison = timeline_data.get("chronology_comparison", [])
    conclusion = timeline_data.get("conclusion", "")

    return timeline_events, introduction, chronology_note, chronology_comparison, conclusion


@app.get("/biblical-timeline", response_class=HTMLResponse)
def biblical_timeline_page(request: Request):
    """Biblical timeline page showing major biblical events chronologically"""
    books = bible.get_books()

    timeline_events, introduction, chronology_note, chronology_comparison, conclusion = get_biblical_timeline_context()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Resources", "url": "/resources"},
        {"text": "Biblical Timeline", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "biblical_timeline.html",
            {
            "books": books,
            "timeline_events": timeline_events,
            "introduction": introduction,
            "chronology_note": chronology_note,
            "chronology_comparison": chronology_comparison,
            "conclusion": conclusion,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE
        }
    )


@app.get("/biblical-timeline/pdf")
async def biblical_timeline_pdf():
    """Generate PDF export for the biblical timeline."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    timeline_events, introduction, chronology_note, chronology_comparison, conclusion = get_biblical_timeline_context()

    html_content = templates.get_template("biblical_timeline_pdf.html").render(
        timeline_events=timeline_events,
        introduction=introduction,
        chronology_note=chronology_note,
        chronology_comparison=chronology_comparison,
        conclusion=conclusion
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=biblical-timeline.pdf"}
    )


def get_biblical_verses(name):
    """Get relevant Bible verses for a person based on their name"""
    verse_map = {
        "Adam": [
            {"reference": "Genesis 2:7", "text": "And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul."},
            {"reference": "Genesis 1:27", "text": "So God created man in his own image, in the image of God created he him; male and female created he them."}
        ],
        "Eve": [
            {"reference": "Genesis 2:22", "text": "And the rib, which the LORD God had taken from man, made he a woman, and brought her unto the man."},
            {"reference": "Genesis 3:20", "text": "And Adam called his wife's name Eve; because she was the mother of all living."}
        ],
        "Cain": [
            {"reference": "Genesis 4:1", "text": "And Adam knew Eve his wife; and she conceived, and bare Cain, and said, I have gotten a man from the LORD."},
            {"reference": "Genesis 4:8", "text": "And Cain talked with Abel his brother: and it came to pass, when they were in the field, that Cain rose up against Abel his brother, and slew him."}
        ],
        "Abel": [
            {"reference": "Genesis 4:2", "text": "And she again bare his brother Abel. And Abel was a keeper of sheep, but Cain was a tiller of the ground."},
            {"reference": "Genesis 4:4", "text": "And Abel, he also brought of the firstlings of his flock and of the fat thereof. And the LORD had respect unto Abel and to his offering:"}
        ],
        "Seth": [
            {"reference": "Genesis 4:25", "text": "And Adam knew his wife again; and she bare a son, and called his name Seth: For God, said she, hath appointed me another seed instead of Abel, whom Cain slew."},
            {"reference": "Genesis 5:3", "text": "And Adam lived an hundred and thirty years, and begat a son in his own likeness, after his image; and called his name Seth:"}
        ],
        "Enoch": [
            {"reference": "Genesis 5:21", "text": "And Enoch lived sixty and five years, and begat Methuselah:"},
            {"reference": "Genesis 5:24", "text": "And Enoch walked with God: and he was not; for God took him."}
        ],
        "Noah": [
            {"reference": "Genesis 6:8", "text": "But Noah found grace in the eyes of the LORD."},
            {"reference": "Genesis 7:1", "text": "And the LORD said unto Noah, Come thou and all thy house into the ark; for thee have I seen righteous before me in this generation."}
        ],
        "Methuselah": [
            {"reference": "Genesis 5:25", "text": "And Methuselah lived an hundred eighty and seven years, and begat Lamech:"},
            {"reference": "Genesis 5:27", "text": "And all the days of Methuselah were nine hundred sixty and nine years: and he died."}
        ]
    }
    
    return verse_map.get(name, [])


def get_daily_verse(date_str=None):
    """Get the verse of the day based on a specific date (or current date if not provided)"""
    # Use date as seed for consistent daily verse
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    seed = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % 1000000

    # Featured verses for rotation
    featured_verses = [
        ("John", 3, 16),
        ("Jeremiah", 29, 11),
        ("Philippians", 4, 13),
        ("Romans", 8, 28),
        ("Proverbs", 3, 5),
        ("Isaiah", 41, 10),
        ("Matthew", 11, 28),
        ("1 John", 4, 19),
        ("Psalms", 23, 1),
        ("2 Corinthians", 5, 17),
        ("Ephesians", 2, 8),
        ("Romans", 10, 9),
        ("1 Peter", 5, 7),
        ("James", 1, 5),
        ("Philippians", 4, 19),
        ("Psalms", 119, 105),
        ("Matthew", 6, 33),
        ("Romans", 12, 2),
        ("1 Corinthians", 13, 13),
        ("Galatians", 5, 22),
        ("Hebrews", 11, 1),
        ("1 Thessalonians", 5, 18),
        ("Psalms", 46, 1),
        ("Isaiah", 40, 31),
        ("Matthew", 5, 16),
        ("Romans", 15, 13),
        ("Colossians", 3, 23),
        ("1 John", 1, 9),
        ("Psalms", 37, 4),
        ("Proverbs", 27, 17)
    ]

    # Select verse based on seed
    verse_index = seed % len(featured_verses)
    book, chapter, verse = featured_verses[verse_index]

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        # Fallback to John 3:16
        book, chapter, verse = "John", 3, 16
        verse_text = bible.get_verse_text(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": verse_text,
        "reference": f"{book} {chapter}:{verse}",
        "date": date_str
    }



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    books = bible.get_books()
    daily_verse = get_daily_verse()

    # Define study guide categories
    study_guides = {
        "Foundational Studies": [
            {
                "title": "New Believer's Guide",
                "description": "Essential truths for new Christians",
                "slug": "new-believer",
                "verses": ["John 3:16", "Romans 10:9", "1 John 1:9", "2 Corinthians 5:17"]
            },
            {
                "title": "Salvation by Grace",
                "description": "Understanding God's gift of salvation",
                "slug": "salvation",
                "verses": ["Ephesians 2:8-9", "Romans 3:23", "Romans 6:23", "Titus 3:5"]
            },
            {
                "title": "The Gospel Message",
                "description": "The good news of Jesus Christ",
                "slug": "gospel",
                "verses": ["1 Corinthians 15:3-4", "Romans 1:16", "Mark 16:15", "Acts 4:12"]
            }
        ],
        "Character & Living": [
            {
                "title": "Fruits of the Spirit",
                "description": "Developing Christian character",
                "slug": "fruits-spirit",
                "verses": ["Galatians 5:22-23", "1 Corinthians 13:4-7", "Philippians 4:8", "Colossians 3:12-14"]
            },
            {
                "title": "Prayer & Faith",
                "description": "Growing in prayer and trust",
                "slug": "prayer-faith",
                "verses": ["Matthew 6:9-13", "1 Thessalonians 5:17", "Hebrews 11:1", "James 1:6"]
            },
            {
                "title": "Christian Living",
                "description": "Walking as followers of Christ",
                "slug": "christian-living",
                "verses": ["Romans 12:1-2", "1 Peter 2:9", "Matthew 5:14-16", "Philippians 2:14-16"]
            }
        ],
        "Biblical Themes": [
            {
                "title": "God's Love",
                "description": "Understanding the depth of God's love",
                "slug": "gods-love",
                "verses": ["1 John 4:8", "John 3:16", "Romans 8:38-39", "1 John 3:1"]
            },
            {
                "title": "Hope & Comfort",
                "description": "Finding hope in difficult times",
                "slug": "hope-comfort",
                "verses": ["Romans 15:13", "2 Corinthians 1:3-4", "Psalm 23:4", "Isaiah 41:10"]
            },
            {
                "title": "Wisdom & Guidance",
                "description": "Seeking God's wisdom for life",
                "slug": "wisdom-guidance",
                "verses": ["Proverbs 3:5-6", "James 1:5", "Psalm 119:105", "Proverbs 27:17"]
            }
        ],
        "Doctrinal Studies": [
            {
                "title": "The Trinity",
                "description": "Understanding God as Father, Son, and Holy Spirit",
                "slug": "trinity",
                "verses": ["Matthew 28:19", "2 Corinthians 13:14", "1 Peter 1:2", "John 14:16-17"]
            },
            {
                "title": "The Resurrection",
                "description": "Christ's victory over death and our hope",
                "slug": "resurrection",
                "verses": ["1 Corinthians 15:20-22", "Romans 6:4-5", "John 11:25-26", "1 Thessalonians 4:16-17"]
            },
            {
                "title": "Heaven & Eternity",
                "description": "Our eternal home with God",
                "slug": "heaven-eternity",
                "verses": ["Revelation 21:1-4", "John 14:2-3", "Philippians 3:20-21", "1 Corinthians 2:9"]
            }
        ],
        "Family & Relationships": [
            {
                "title": "Biblical Marriage",
                "description": "God's design for marriage",
                "slug": "biblical-marriage",
                "verses": ["Ephesians 5:22-33", "Genesis 2:24", "1 Corinthians 7:3-5", "Hebrews 13:4"]
            },
            {
                "title": "Raising Children",
                "description": "Biblical principles for parenting",
                "slug": "raising-children",
                "verses": ["Proverbs 22:6", "Ephesians 6:4", "Deuteronomy 6:6-7", "Colossians 3:21"]
            },
            {
                "title": "Money & Stewardship",
                "description": "Biblical wisdom on finances",
                "slug": "money-stewardship",
                "verses": ["Malachi 3:10", "Luke 16:10-11", "1 Timothy 6:10", "Proverbs 3:9-10"]
            }
        ]
    }

    # Process verse references to add URLs
    for category in study_guides.values():
        for guide in category:
            guide['verse_refs'] = [
                {
                    'text': verse,
                    'url': verse_reference_to_url(verse) or '#'
                }
                for verse in guide['verses']
            ]

    return templates.TemplateResponse(
        request, "index.html", {"books": books, "daily_verse": daily_verse, "study_guides": study_guides}
    )


@app.get("/books", response_class=HTMLResponse)
async def books_page(request: Request):
    """Browse all books of the Bible"""
    books = bible.get_books()

    # Define book categories with types
    book_types = {
        # Old Testament
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
        # New Testament
        'Matthew': 'gospels', 'Mark': 'gospels', 'Luke': 'gospels', 'John': 'gospels',
        'Acts': 'acts',
        'Romans': 'pauline', '1 Corinthians': 'pauline', '2 Corinthians': 'pauline',
        'Galatians': 'pauline', 'Ephesians': 'pauline', 'Philippians': 'pauline', 'Colossians': 'pauline',
        '1 Thessalonians': 'pauline', '2 Thessalonians': 'pauline',
        '1 Timothy': 'pauline', '2 Timothy': 'pauline', 'Titus': 'pauline', 'Philemon': 'pauline',
        'Hebrews': 'general', 'James': 'general', '1 Peter': 'general', '2 Peter': 'general',
        '1 John': 'general', '2 John': 'general', '3 John': 'general', 'Jude': 'general',
        'Revelation': 'apocalyptic'
    }

    # Organize books by testament
    old_testament_books = [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
        '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
        'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
        'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
        'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'
    ]

    new_testament_books = [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
        '1 John', '2 John', '3 John', 'Jude', 'Revelation'
    ]

    # Get chapter counts for each book
    def get_chapter_count(book_name):
        chapters = bible.get_chapters_for_book(book_name)
        return len(chapters)

    old_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in old_testament_books
    ]

    new_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in new_testament_books
    ]

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "books.html",
            {
            "old_testament": old_testament,
            "new_testament": new_testament,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/reading-plans", response_class=HTMLResponse)
async def reading_plans_page(request: Request):
    """Browse Bible reading plans"""
    books = bible.get_books()
    plans = get_plan_summary()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "reading_plans.html",
            {
            "plans": plans,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/reading-plans/{plan_id}", response_class=HTMLResponse)
async def reading_plan_detail(request: Request, plan_id: str):
    """View a specific reading plan"""
    books = bible.get_books()
    plan = get_plan(plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": "/reading-plans"},
        {"text": plan["name"], "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "reading_plan_detail.html",
            {
            "plan": plan,
            "plan_id": plan_id,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/reading-plans/{plan_id}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


@app.get("/reading-plans/{plan_id}/pdf")
async def reading_plan_pdf(plan_id: str):
    """Generate a PDF export for a reading plan."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    html_content = templates.get_template("reading_plan_pdf.html").render(plan=plan)
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"reading-plan-{plan_id}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/topics", response_class=HTMLResponse)
async def topics_page(request: Request):
    """Browse topical index of Bible themes"""
    books = bible.get_books()
    topics = get_all_topics()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "topics.html",
            {
            "topics": topics,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE
        }
    )


@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    """Browse all theological resources"""
    books = bible.get_books()

    # Organize resources into categories
    resources = {
        "People": [
            {
                "name": "Biblical Prophets",
                "url": "/biblical-prophets",
                "description": "Explore the prophetic ministry throughout Scripture, from Isaiah to Malachi",
                "count": "9 prophets"
            },
            {
                "name": "The Twelve Apostles",
                "url": "/the-twelve-apostles",
                "description": "The twelve disciples chosen by Jesus to be witnesses of His ministry",
                "count": "12 apostles"
            },
            {
                "name": "Women of the Bible",
                "url": "/women-of-the-bible",
                "description": "Notable women of Scripture and their significance in redemptive history",
                "count": "12 women"
            }
        ],
        "Theology": [
            {
                "name": "Biblical Angels",
                "url": "/biblical-angels",
                "description": "Angelic beings mentioned in Scripture, including Michael, Gabriel, and the heavenly host",
                "count": "12 entries"
            },
            {
                "name": "The Tetragrammaton",
                "url": "/tetragrammaton",
                "description": "The sacred four-letter name of God (YHWH) and its profound significance",
                "count": "Deep dive"
            },
            {
                "name": "Names of God",
                "url": "/names-of-god",
                "description": "The revelation of God's names throughout Scripture and their meanings",
                "count": "14 names"
            },
            {
                "name": "Parables of Jesus",
                "url": "/parables",
                "description": "The parables spoken by Christ to illustrate spiritual truths",
                "count": "11 parables"
            },
            {
                "name": "Miracles of Jesus",
                "url": "/miracles-of-jesus",
                "description": "Signs and wonders manifesting divine authority over nature, disease, demons, and death",
                "count": "35+ miracles"
            },
            {
                "name": "I Am Statements",
                "url": "/i-am-statements",
                "description": "The seven 'I Am' statements of Jesus in John's Gospel revealing His divine nature",
                "count": "7 statements"
            },
            {
                "name": "The Beatitudes",
                "url": "/beatitudes",
                "description": "The blessings proclaimed by Jesus in the Sermon on the Mount",
                "count": "8 beatitudes"
            },
            {
                "name": "Ten Commandments",
                "url": "/ten-commandments",
                "description": "The moral law given by God to Moses on Mount Sinai",
                "count": "10 commandments"
            },
            {
                "name": "Armor of God",
                "url": "/armor-of-god",
                "description": "The spiritual equipment for warfare described in Ephesians 6",
                "count": "7 pieces"
            },
            {
                "name": "Prayers of the Bible",
                "url": "/prayers-of-the-bible",
                "description": "Sacred prayers from the Psalms, Jesus, Paul, and the early church",
                "count": "20+ prayers"
            },
            {
                "name": "Biblical Covenants",
                "url": "/biblical-covenants",
                "description": "Divine covenants established between God and His people",
                "count": "7 covenants"
            },
            {
                "name": "Fruits of the Spirit",
                "url": "/fruits-of-the-spirit",
                "description": "The nine graces of Galatians 5:22-23 manifested in believers through the Holy Spirit",
                "count": "9 fruits"
            }
        ],
        "Systematic Theology": [
            {
                "name": "The Trinity",
                "url": "/trinity",
                "description": "The mystery of God revealed as Father, Son, and Holy Spirit—three Persons, one God",
                "count": "4 categories"
            },
            {
                "name": "Christology",
                "url": "/christology",
                "description": "The Person and work of Jesus Christ—His deity, humanity, and offices",
                "count": "4 categories"
            },
            {
                "name": "Pneumatology",
                "url": "/pneumatology",
                "description": "The doctrine of the Holy Spirit—His Person, deity, and work in believers",
                "count": "4 categories"
            },
            {
                "name": "Soteriology",
                "url": "/soteriology",
                "description": "The doctrine of salvation—from election to glorification",
                "count": "5 categories"
            },
            {
                "name": "Ecclesiology",
                "url": "/ecclesiology",
                "description": "The doctrine of the Church—its nature, mission, and governance",
                "count": "4 categories"
            },
            {
                "name": "Eschatology",
                "url": "/eschatology",
                "description": "The doctrine of last things—Christ's return, judgment, and eternal state",
                "count": "5 categories"
            },
            {
                "name": "The Kingdom of God",
                "url": "/kingdom-of-god",
                "description": "God's sovereign reign inaugurated in Christ and consummated at His return",
                "count": "5 categories"
            },
            {
                "name": "Types and Shadows",
                "url": "/types-and-shadows",
                "description": "Old Testament persons, events, and institutions that prefigure Christ",
                "count": "5 categories"
            },
            {
                "name": "Messianic Prophecies",
                "url": "/messianic-prophecies",
                "description": "Old Testament prophecies fulfilled in Jesus Christ",
                "count": "5 categories"
            },
            {
                "name": "The Blood in Scripture",
                "url": "/blood-in-scripture",
                "description": "The theology of blood, sacrifice, and redemption throughout Scripture",
                "count": "5 categories"
            },
            {
                "name": "Names and Titles of Christ",
                "url": "/names-of-christ",
                "description": "The names and titles ascribed to Jesus revealing His Person and work",
                "count": "5 categories"
            },
            {
                "name": "Spirits & Demons",
                "url": "/spirits-and-demons",
                "description": "Biblical demonology—Satan, evil spirits, Legion, and spiritual warfare",
                "count": "7 categories"
            },
            {
                "name": "Personifications",
                "url": "/personifications",
                "description": "Abstract concepts given human form—Wisdom, Folly, Death, Sin, and more",
                "count": "6 categories"
            },
            {
                "name": "Bibliology",
                "url": "/bibliology",
                "description": "The Doctrine of Scripture—inspiration, authority, sufficiency, and preservation",
                "count": "4 categories"
            },
            {
                "name": "Theology Proper",
                "url": "/theology-proper",
                "description": "The Attributes of God—His incommunicable and communicable perfections",
                "count": "4 categories"
            },
            {
                "name": "Anthropology",
                "url": "/anthropology",
                "description": "The Doctrine of Man—creation, constitution, and condition of humanity",
                "count": "4 categories"
            },
            {
                "name": "Hamartiology",
                "url": "/hamartiology",
                "description": "The Doctrine of Sin—its origin, nature, transmission, and consequences",
                "count": "4 categories"
            },
            {
                "name": "Providence",
                "url": "/providence",
                "description": "Divine Providence—God's preservation, governance, and concurrence in all things",
                "count": "4 categories"
            },
            {
                "name": "Grace",
                "url": "/grace",
                "description": "The Doctrine of Grace—common grace, effectual grace, election, and perseverance",
                "count": "4 categories"
            },
            {
                "name": "Justification",
                "url": "/justification",
                "description": "The Doctrine of Justification—declared righteous through faith in Christ alone",
                "count": "4 categories"
            },
            {
                "name": "Sanctification",
                "url": "/sanctification",
                "description": "The Doctrine of Sanctification—progressive holiness through the Spirit",
                "count": "4 categories"
            },
            {
                "name": "Law and Gospel",
                "url": "/law-and-gospel",
                "description": "The distinction between Law and Gospel—God's demands and His gracious provision",
                "count": "4 categories"
            },
            {
                "name": "Worship",
                "url": "/worship",
                "description": "The Doctrine of Worship—regulative principle, elements, and the heart of worship",
                "count": "4 categories"
            }
        ],
        "History & Culture": [
            {
                "name": "Biblical Festivals",
                "url": "/biblical-festivals",
                "description": "The appointed feasts and holy days ordained in the Law of Moses",
                "count": "7 festivals"
            },
            {
                "name": "Biblical Geography",
                "url": "/biblical-maps",
                "description": "Locations mentioned in Scripture and their historical significance",
                "count": "Maps & places",
                "badge": "Interactive"
            },
            {
                "name": "Biblical Timeline",
                "url": "/biblical-timeline",
                "description": "Chronological overview of biblical events from Creation to Revelation",
                "count": "Timeline"
            },
            {
                "name": "Genealogies",
                "url": "/family-tree",
                "description": "Interactive family tree from Adam to Jesus Christ with detailed person profiles",
                "count": "160+ people",
                "badge": "Interactive"
            }
        ],
        "Study Tools": [
            {
                "name": "Study Guides",
                "url": "/study-guides",
                "description": "In-depth guides for studying biblical books, themes, and doctrines",
                "count": "Multiple guides"
            }
        ]
    }

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Resources", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "resources.html",
            {
            "resources": resources,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/topics/{topic_name}", response_class=HTMLResponse)
async def topic_detail(request: Request, topic_name: str):
    """View verses for a specific topic"""
    books = bible.get_books()
    topic = get_topic(topic_name)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": "/topics"},
        {"text": topic_name, "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "topic_detail.html",
            {
            "topic": topic,
            "topic_name": topic_name,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/topics/{topic_name}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


@app.get("/topics/{topic_name}/pdf")
async def topic_detail_pdf(topic_name: str):
    """Generate a PDF export for a topic detail page."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    topic = get_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    html_content = templates.get_template("topic_pdf.html").render(
        topic=topic,
        topic_name=topic_name,
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{topic_name}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/book/{book}", response_class=HTMLResponse)
async def read_book(request: Request, book: str):
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}", status_code=301)

    books = bible.get_books()
    chapters = bible.get_chapters_for_book(book)

    if not chapters:
        raise HTTPException(
            status_code=404,
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )

    # Generate commentary data for the book page
    commentary_data = generate_book_commentary(book, chapters)

    # Calculate popularity scores for each chapter
    chapter_popularity = {}
    chapter_explanations = {}
    for chapter in chapters:
        chapter_popularity[chapter] = get_chapter_popularity_score(book, chapter)
        chapter_explanations[chapter] = get_chapter_popularity_explanation(book, chapter)

    # Get book introduction data if available
    book_intro = get_book_data(book) if has_book_data(book) else None

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "book.html",
            {
            "book": book,
            "chapters": chapters,
            "books": books,
            "chapter_popularity": chapter_popularity,
            "chapter_explanations": chapter_explanations,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "book_intro": book_intro,
            **commentary_data
        },
    )


@app.get("/book/{book}/pdf")
async def book_pdf(request: Request, book: str):
    """Generate a PDF export for an entire Bible book."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/pdf", status_code=301)

    chapters = bible.get_chapters_for_book(book)
    if not chapters:
        raise HTTPException(
            status_code=404,
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )

    chapters_data = []
    total_verses = 0
    for chapter_num in chapters:
        verses = bible.get_verses_by_book_chapter(book, chapter_num)
        if not verses:
            continue
        total_verses += len(verses)
        chapters_data.append({
            "chapter": chapter_num,
            "verses": verses
        })

    if not chapters_data:
        raise HTTPException(
            status_code=404,
            detail=f"No verses found for the book '{book}'."
        )

    # Get book introduction data if available
    book_intro = get_book_data(book) if has_book_data(book) else None

    html_content = templates.get_template("book_pdf.html").render(
        book=book,
        chapters=chapters_data,
        chapter_count=len(chapters_data),
        verse_count=total_verses,
        book_intro=book_intro,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(book)}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/book/{book}/commentary")
def book_commentary_redirect(book: str):
    """Redirect old book commentary URLs to book page"""
    return RedirectResponse(url=f"/book/{book}", status_code=301)


@app.get("/book/{book}/{chapter}")
def redirect_chapter_legacy(book: str, chapter: int):
    """Redirect legacy chapter URLs to correct format"""
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}", status_code=301)

@app.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
async def read_chapter(request: Request, book: str, chapter: int):
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )



    # Generate AI commentary for the chapter
    commentaries = {}
    shown_words = set()  # Track which words have already been shown in this chapter
    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)
        # Add word study sidenotes (avoiding repetition within chapter)
        word_studies = generate_word_study_sidenotes(verse.text, book, chapter, verse.verse, shown_words)
        commentary['word_studies'] = word_studies
        # Track which words were shown
        for study in word_studies:
            shown_words.add(study['word'].lower())
        # Add cross-references with proper URLs, grouped by description
        cross_refs = get_cross_references(book, chapter, verse.verse)

        # Group cross-references by their description/note
        from collections import defaultdict
        grouped_refs = defaultdict(list)
        for ref in cross_refs:
            description = ref['note'] if ref['note'] else 'Related'
            url = f"/book/{ref['ref'].rsplit(' ', 1)[0]}/chapter/{ref['ref'].rsplit(' ', 1)[1].split(':')[0]}/verse/{ref['ref'].rsplit(' ', 1)[1].split(':')[1]}" if ' ' in ref['ref'] and ':' in ref['ref'] else '#'
            grouped_refs[description].append({
                'text': ref['ref'],
                'url': url
            })

        # Convert to list of groups for template
        commentary['cross_reference_groups'] = [
            {'description': desc, 'refs': refs}
            for desc, refs in grouped_refs.items()
        ]
        commentaries[verse.verse] = commentary

    # Generate chapter overview
    chapter_overview = generate_chapter_overview(book, chapter, verses)

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "chapter.html",
            {
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "pdf_available": WEASYPRINT_AVAILABLE
        }
    )


@app.get("/book/{book}/chapter/{chapter}/pdf")
async def chapter_pdf(request: Request, book: str, chapter: int):
    """Generate a PDF export for a specific Bible chapter."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/pdf", status_code=301)

    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        raise HTTPException(
            status_code=404,
            detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
        )

    # Generate commentaries with cross-references and word studies for PDF
    commentaries = {}
    shown_words = set()
    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)
        # Add word study sidenotes (avoiding repetition within chapter)
        word_studies = generate_word_study_sidenotes(verse.text, book, chapter, verse.verse, shown_words)
        commentary['word_studies'] = word_studies
        for study in word_studies:
            shown_words.add(study['word'].lower())

        # Add cross-references grouped by description
        from collections import defaultdict
        cross_refs = get_cross_references(book, chapter, verse.verse)
        grouped_refs = defaultdict(list)
        for ref in cross_refs:
            description = ref['note'] if ref['note'] else 'Related'
            grouped_refs[description].append(ref['ref'])

        commentary['cross_reference_groups'] = [
            {'description': desc, 'refs': refs}
            for desc, refs in grouped_refs.items()
        ]
        commentaries[verse.verse] = commentary

    html_content = templates.get_template("chapter_pdf.html").render(
        book=book,
        chapter=chapter,
        verses=verses,
        verse_count=len(verses),
        commentaries=commentaries,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(book)}-chapter-{chapter}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/book/{book}/chapter/{chapter}/interlinear/pdf")
async def chapter_interlinear_pdf(book: str, chapter: int):
    """Generate PDF export for interlinear chapter view."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/interlinear/pdf", status_code=301)

    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(status_code=404, detail=f"The book '{book}' was not found.")
        else:
            raise HTTPException(status_code=404, detail=f"Chapter {chapter} of {book} was not found.")

    # Get interlinear data for each verse
    verses_with_interlinear = []
    for verse in verses:
        interlinear_words = get_interlinear_data(book, chapter, verse.verse)
        verses_with_interlinear.append({
            'verse': verse,
            'interlinear_words': interlinear_words or []
        })

    # Determine if OT or NT for language badge
    is_old_testament = book in OT_BOOKS

    html_content = templates.get_template("chapter_interlinear_pdf.html").render(
        book=book,
        chapter=chapter,
        verses_with_interlinear=verses_with_interlinear,
        is_old_testament=is_old_testament
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{book.lower().replace(' ', '-')}-{chapter}-interlinear.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/book/{book}/chapter/{chapter}/interlinear", response_class=HTMLResponse)
async def read_chapter_interlinear(request: Request, book: str, chapter: int):
    """Display a chapter with interlinear Hebrew/Greek for every verse"""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/interlinear", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Get interlinear data for each verse
    verses_with_interlinear = []
    for verse in verses:
        interlinear_words = get_interlinear_data(book, chapter, verse.verse)
        verses_with_interlinear.append({
            'verse': verse,
            'interlinear_words': interlinear_words or []
        })

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": f"/book/{book}/chapter/{chapter}"},
        {"text": "Interlinear", "url": None}
    ]

    # Determine if OT or NT for language badge
    ot_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
                '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
                'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes',
                'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel',
                'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
                'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']
    is_old_testament = book in ot_books

    return templates.TemplateResponse(
        request,
        "chapter_interlinear.html",
        {
            "book": book,
            "chapter": chapter,
            "verses_with_interlinear": verses_with_interlinear,
            "books": books,
            "chapters": chapters,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "is_old_testament": is_old_testament,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/book/{book}/chapter/{chapter}/interlinear/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


@app.get("/book/{book}/chapter/{chapter}/verse/{verse_num}/pdf")
async def verse_pdf(book: str, chapter: int, verse_num: int):
    """Generate PDF export for a single verse with commentary."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/verse/{verse_num}/pdf", status_code=301)

    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    verses = bible.get_verses_by_book_chapter(book, chapter)
    if not verses:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter} of {book} was not found.")

    # Find the specific verse
    verse = None
    for v in verses:
        if v.verse == verse_num:
            verse = v
            break

    if not verse:
        raise HTTPException(status_code=404, detail=f"Verse {verse_num} not found in {book} {chapter}.")

    # Generate commentary
    try:
        commentary = generate_commentary(book, chapter, verse)
    except Exception:
        commentary = None

    # Get cross-references
    cross_refs = get_cross_references(book, chapter, verse_num)

    # Get interlinear data
    interlinear_words = get_interlinear_data(book, chapter, verse_num)

    # Determine if OT
    is_ot = book in OT_BOOKS

    html_content = templates.get_template("verse_pdf.html").render(
        book=book,
        chapter=chapter,
        verse_num=verse_num,
        verse_text=verse.text,
        commentary=commentary,
        cross_references=cross_refs,
        interlinear_words=interlinear_words,
        is_old_testament=is_ot
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{book.lower().replace(' ', '-')}-{chapter}-{verse_num}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/book/{book}/chapter/{chapter}/verse/{verse_num}", response_class=HTMLResponse)
async def read_verse(request: Request, book: str, chapter: int, verse_num: int):
    """Display a single verse with detailed commentary"""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/verse/{verse_num}", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Find the specific verse
    verse = None
    for v in verses:
        if v.verse == verse_num:
            verse = v
            break

    if not verse:
        raise HTTPException(
            status_code=404,
            detail=f"Verse {verse_num} not found in {book} {chapter}. This chapter has {len(verses)} verses."
        )

    # Generate commentary for this verse
    try:
        commentary = generate_commentary(book, chapter, verse)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error generating commentary for {book} {chapter}:{verse_num}: {e}")
        commentary = None

    # Get cross-references for this verse
    cross_refs = get_cross_references(book, chapter, verse_num)

    # Check if interlinear data is available and load it
    has_interlinear = has_interlinear_data(book, chapter, verse_num)
    interlinear_words = get_interlinear_data(book, chapter, verse_num) if has_interlinear else None

    # Get related content for internal linking
    related_content = get_related_content(book, chapter, verse_num)

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": f"/book/{book}/chapter/{chapter}"},
        {"text": f"Verse {verse_num}", "url": None}
    ]

    # Determine if Old Testament for interlinear styling
    is_ot = book in OT_BOOKS

    return templates.TemplateResponse(
            request,
            "verse.html",
            {
            "book": book,
            "chapter": chapter,
            "verse_num": verse_num,
            "verse_text": verse.text,
            "commentary": commentary,
            "cross_references": cross_refs,
            "total_verses": len(verses),
            "books": books,
            "chapters": chapters,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "current_verse": verse_num,
            "has_interlinear": has_interlinear,
            "interlinear_words": interlinear_words,
            "related_content": related_content,
            "is_old_testament": is_ot,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/book/{book}/chapter/{chapter}/verse/{verse_num}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


# =============================================================================
# Strong's Concordance Routes
# =============================================================================

@app.get("/strongs", response_class=HTMLResponse)
async def strongs_index(request: Request, q: str = None):
    """Strong's Concordance search and lookup page."""
    results = []
    if q:
        results = search_strongs(q, language="both", limit=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_index.html",
        {
            "query": q or "",
            "results": results,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/strongs/hebrew", response_class=HTMLResponse)
async def strongs_hebrew_index(request: Request, page: int = 1):
    """Paginated index of all Hebrew Strong's entries."""
    data = get_all_strongs("hebrew", page=page, per_page=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": "Hebrew", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_language_index.html",
        {
            "language": "Hebrew",
            "language_code": "hebrew",
            "entries": data["entries"],
            "page": data["page"],
            "total_pages": data["total_pages"],
            "total": data["total"],
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/strongs/greek", response_class=HTMLResponse)
async def strongs_greek_index(request: Request, page: int = 1):
    """Paginated index of all Greek Strong's entries."""
    data = get_all_strongs("greek", page=page, per_page=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": "Greek", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_language_index.html",
        {
            "language": "Greek",
            "language_code": "greek",
            "entries": data["entries"],
            "page": data["page"],
            "total_pages": data["total_pages"],
            "total": data["total"],
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/strongs/{strongs_number}", response_class=HTMLResponse)
async def strongs_entry(request: Request, strongs_number: str):
    """View a single Strong's concordance entry."""
    import re

    entry = format_strongs_entry(strongs_number)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Strong's number '{strongs_number}' not found"
        )

    # Find all verses containing this Strong's number
    verse_occurrences = find_verses_by_strongs(strongs_number, limit=10000)
    total_occurrences = len(verse_occurrences)

    # Fetch full verse text for each occurrence and highlight the word
    for occ in verse_occurrences:
        verse_text = bible.get_verse_text(occ["book"], occ["chapter"], occ["verse"])
        if verse_text:
            # Highlight the English word in the verse text
            english_word = occ.get("english", "")
            if english_word and english_word in verse_text:
                occ["verse_text"] = verse_text.replace(
                    english_word,
                    f'<mark>{english_word}</mark>',
                    1  # Only highlight first occurrence
                )
            else:
                occ["verse_text"] = verse_text
        else:
            occ["verse_text"] = ""

    # Extract and fetch related Strong's entries from derivation
    related_entries = []
    if entry.get("derivation"):
        # Find all Strong's references like H1234 or G5678
        strongs_refs = re.findall(r'([HG])(\d+)', entry["derivation"])
        seen = set()
        for prefix, num in strongs_refs:
            ref = f"{prefix}{num}"
            if ref.upper() != strongs_number.upper() and ref not in seen:
                seen.add(ref)
                related = format_strongs_entry(ref)
                if related:
                    related_entries.append(related)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": strongs_number.upper(), "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_entry.html",
        {
            "entry": entry,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "verse_occurrences": verse_occurrences,
            "total_occurrences": total_occurrences,
            "related_entries": related_entries
        }
    )
