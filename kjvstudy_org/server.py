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
from .topics import get_all_topics, get_topic_with_text, search_topics
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
    bible_router, init_bible_templates, init_bible_commentary,
    reading_plans_router, init_reading_plans_templates,
    topics_router, init_topics_templates,
    strongs_router, init_strongs_templates,
    timeline_router, init_timeline_templates,
    about_router, init_about_templates,
    main_router, init_main_templates,
    misc_router, init_misc_templates, init_search_family_tree,
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
from .jinja_filters import register_filters
register_filters(templates.env)

# Add global template variables
templates.env.globals['disable_analytics'] = os.getenv("DISABLE_ANALYTICS", "false").lower() == "true"

# Initialize templates for route modules
init_api_templates(templates)
init_resources_templates(templates)
init_family_tree_templates(templates)
init_study_guides_templates(templates)
init_commentary_templates(templates)
init_stories_templates(templates)
init_bible_templates(templates)
init_bible_commentary(generate_commentary, generate_chapter_overview, generate_book_commentary, generate_word_study_sidenotes)
init_reading_plans_templates(templates)
init_topics_templates(templates)
init_strongs_templates(templates)
init_timeline_templates(templates)
init_about_templates(templates)
init_main_templates(templates)
init_misc_templates(templates)

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


# Initialize the search_family_tree function in misc routes
init_search_family_tree(search_family_tree)
