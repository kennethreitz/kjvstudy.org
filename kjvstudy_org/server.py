import hashlib
import json
import os
import re
import random
from datetime import datetime, timedelta
from pathlib import Path as PathLib
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, Query, Path
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse
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
from .interlinear_loader import get_interlinear_data, has_interlinear_data, get_all_interlinear_verses, preload_data

# Import from modular packages
from .routes import (
    api_router,
    resources_router, init_resources_templates,
    family_tree_router, init_family_tree_templates,
    study_guides_router, init_study_guides_templates,
)
from .utils.books import normalize_book_name, OT_BOOKS, NT_BOOKS
from .utils.helpers import (
    create_slug, get_verse_text, get_related_content,
    get_chapter_popularity_score, get_chapter_popularity_explanation,
    get_daily_verse, FEATURED_VERSES, is_verse_reference, parse_verse_reference
)
from .utils.search import perform_full_text_search

try:
    from ged4py import GedcomReader
except ImportError:
    GedcomReader = None


# Note: Helper functions (create_slug, normalize_book_name, get_related_content,
# get_chapter_popularity_score, get_chapter_popularity_explanation, get_verse_text,
# is_verse_reference, parse_verse_reference, perform_full_text_search, etc.)
# are now imported from utils modules above.


app = FastAPI(
    title="KJV Study API",
    description="RESTful API for accessing King James Bible verses, chapters, and study resources",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Include the API router (routes defined in routes/api.py)
app.include_router(api_router)

# Include the resources router (biblical resources, defined in routes/resources.py)
app.include_router(resources_router)

# Include the family tree router
app.include_router(family_tree_router)

# Include the study guides router
app.include_router(study_guides_router)


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
        if request.url.path.startswith("/api/") or request.url.path == "/verse-of-the-day":
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
        elif request.url.path in ["/", "/books", "/search", "/resources", "/concordance"]:
            response.headers["Cache-Control"] = "public, max-age=3600"  # 1 hour
        # Sitemap and robots.txt - cache for 1 day
        elif request.url.path in ["/sitemap.xml", "/robots.txt"]:
            response.headers["Cache-Control"] = "public, max-age=86400"
        # Default - cache for 10 minutes
        else:
            response.headers["Cache-Control"] = "public, max-age=600"

        return response


# Add GZip compression middleware (compress responses > 500 bytes)
app.add_middleware(GZipMiddleware, minimum_size=500)

# Add caching middleware
app.add_middleware(CacheControlMiddleware)


# Set up Jinja2 templates and static files
current_dir = PathLib(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Register custom Jinja2 filters
templates.env.filters['slugify'] = create_slug

# Initialize templates for route modules
init_resources_templates(templates)
init_family_tree_templates(templates)
init_study_guides_templates(templates)

# Load Scofield commentary for cross-references
scofield_commentary = {}
try:
    scofield_path = static_dir / "scofield_commentary.json"
    with open(scofield_path, 'r') as f:
        scofield_commentary = json.load(f)
except Exception as e:
    print(f"Warning: Could not load Scofield commentary: {e}")


@app.on_event("startup")
async def startup_event():
    """Initialize app on startup - preload data if enabled"""
    if os.getenv("PRELOAD_INTERLINEAR", "false").lower() == "true":
        preload_data()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom error handler that renders our error template"""
    if exc.status_code == 404:
        books = list(bible.iter_books())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": exc.status_code,
                "detail": exc.detail,
                "books": books,
            },
            status_code=exc.status_code,
        )

    # For other errors, use the default handler
    return await http_exception_handler(request, exc)


@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, q: str = Query(None, description="Search query")):
    """Search page with results (includes Bible verses and family tree)"""
    books = list(bible.iter_books())
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
        "search.html",
        {
            "request": request,
            "query": q or "",
            "results": search_results,
            "family_tree_results": family_tree_results,
            "books": books,
            "total_results": len(search_results) + len(family_tree_results),
            "is_direct_verse": is_direct_verse
        }
    )

@app.get("/concordance", response_class=HTMLResponse)
def concordance_page(request: Request, word: str = Query(None, description="Word to look up")):
    """Concordance page showing all occurrences of a word"""
    books = list(bible.iter_books())

    if not word or len(word.strip()) < 2:
        return templates.TemplateResponse(
            "concordance.html",
            {
                "request": request,
                "books": books,
                "word": word or "",
                "total_occurrences": 0,
                "occurrences_by_book": {},
                "books_with_word": []
            }
        )

    search_word = word.strip()
    occurrences = []
    occurrences_by_book = {}
    books_with_word = set()

    # Search through all verses
    import re
    # Create a word boundary pattern for exact word matching
    # This handles punctuation and word boundaries properly
    pattern = re.compile(r'\b' + re.escape(search_word) + r'\b', re.IGNORECASE)

    # Use bible.iter_verses() to iterate through all verses
    for verse in bible.iter_verses():
        # Check if the word appears in this verse
        if pattern.search(verse.text):
            # Highlight the word in the text
            highlighted_text = pattern.sub(
                lambda m: f'<span class="highlight">{m.group()}</span>',
                verse.text
            )

            occurrence = {
                'book': verse.book,
                'chapter': verse.chapter,
                'verse': verse.verse,
                'text': verse.text,
                'highlighted_text': highlighted_text
            }

            occurrences.append(occurrence)
            books_with_word.add(verse.book)

            # Group by book
            if verse.book not in occurrences_by_book:
                occurrences_by_book[verse.book] = []
            occurrences_by_book[verse.book].append(occurrence)

    return templates.TemplateResponse(
        "concordance.html",
        {
            "request": request,
            "books": books,
            "word": search_word,
            "total_occurrences": len(occurrences),
            "occurrences_by_book": occurrences_by_book,
            "books_with_word": sorted(books_with_word)
        }
    )


@app.get("/interlinear", response_class=HTMLResponse)
def interlinear_landing_page(request: Request):
    """Landing page explaining interlinear Bible study"""
    books = list(bible.iter_books())

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
        "interlinear_landing.html",
        {
            "request": request,
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
def random_verse(request: Request):
    """Redirect to a random Bible verse"""
    # Get all books
    all_books = list(bible.iter_books())

    # Pick a random book
    book = random.choice(all_books)

    # Get all chapters for this book
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    # Pick a random chapter
    chapter = random.choice(chapters)

    # Get all verses for this chapter
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]

    # Pick a random verse
    verse = random.choice(verses)

    # Redirect to the verse page
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}/verse/{verse.verse}")


@app.get("/verse-of-the-day", response_class=HTMLResponse)
def verse_of_the_day_page(request: Request):
    """Verse of the day page"""
    books = list(bible.iter_books())
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
        "verse_of_the_day.html",
        {
            "request": request,
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

# Cache for sitemap to avoid regenerating on every request
_sitemap_cache = None
_sitemap_cache_date = None


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
                    # Store both the full name and potential variations
                    _name_to_person_id_cache[name.lower()] = person_id

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


@app.get("/biblical-timeline", response_class=HTMLResponse)
def biblical_timeline_page(request: Request):
    """Biblical timeline page showing major biblical events chronologically"""
    books = list(bible.iter_books())

    # Define biblical timeline events
    timeline_events = {
        "Creation and Early History": [
            {
                "title": "Creation of the World",
                "date": "11,013 BC",
                "alt_dates": "Ussher/Scofield: 4004 BC",
                "description": "God (אֱלֹהִים, <em>Elohim</em>—the plural of majesty) creates (<em>bara</em>, ברא—to bring into existence ex nihilo) the heavens and earth in six sequential days, establishing the sabbath pattern. The Hebrew <em>Bereshit</em> (בְּרֵאשִׁית, 'In the beginning') opens Scripture with God's sovereign act of creation, speaking all things into being by His Word (דָּבָר, <em>davar</em>). The creation account reveals God's triune nature (Genesis 1:26, 'Let us make man'), His absolute power, and His purposeful design. The six-day creation culminates in humanity made in the <em>imago Dei</em> (image of God), establishing man as God's vice-regent over creation and anticipating the incarnation of the eternal Word.",
                "verses": [
                    {"reference": "Genesis 1:1", "text": "In the beginning God created the heaven and the earth."},
                    {"reference": "Genesis 1:31", "text": "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day."}
                ]
            },
            {
                "title": "The Fall of Man",
                "date": "11,013 BC",
                "alt_dates": "Ussher/Scofield: 4004 BC",
                "description": "The serpent (נָחָשׁ, <em>nachash</em>—identified in Revelation 12:9 as Satan) deceives Eve, and Adam willfully transgresses God's command, introducing sin (חַטָּאת, <em>chattah</em>) and death (מָוֶת, <em>mavet</em>) into creation. This cosmic rebellion fractures humanity's relationship with God, necessitating expulsion from Eden and the curse upon creation. Yet God immediately announces the <em>protoevangelium</em> (first gospel)—the promise that the woman's seed would crush the serpent's head (Genesis 3:15), foreshadowing Christ's victory over Satan. The Fall establishes the theological foundation for understanding sin's universal guilt, humanity's depravity, and the absolute necessity of divine redemption through a substitute—themes pervading all Scripture.",
                "verses": [
                    {"reference": "Genesis 3:6", "text": "And when the woman saw that the tree was good for food, and that it was pleasant to the eyes, and a tree to be desired to make one wise, she took of the fruit thereof, and did eat, and gave also unto her husband with her; and he did eat."},
                    {"reference": "Genesis 3:23", "text": "Therefore the LORD God sent him forth from the garden of Eden, to till the ground from whence he was taken."}
                ]
            },
            {
                "title": "Cain and Abel",
                "date": "c. 10900 BC",
                "alt_dates": "Ussher/Scofield: c. 3900 BC",
                "description": "The first murder demonstrates sin's rapid progression—from rebellion against God to violence against man. Cain's offering of agricultural produce contrasts with Abel's blood sacrifice from the flock, establishing the biblical principle that 'without shedding of blood is no remission' (Hebrews 9:22). Abel's faith-based sacrifice (Hebrews 11:4) typifies Christ, the Lamb slain from the foundation of the world, while Cain prefigures those who approach God through works rather than grace. God's marking of Cain reveals both judgment and mercy, as He restrains complete vengeance while establishing that blood guilt cries out for justice—a cry ultimately answered at Calvary.",
                "verses": [
                    {"reference": "Genesis 4:8", "text": "And Cain talked with Abel his brother: and it came to pass, when they were in the field, that Cain rose up against Abel his brother, and slew him."}
                ]
            },
            {
                "title": "The Great Flood",
                "date": "4,990 BC",
                "alt_dates": "Ussher/Scofield: 2348 BC",
                "description": "As humanity's wickedness reaches catastrophic proportions—'every imagination of the thoughts of his heart was only evil continually' (Genesis 6:5)—God executes universal judgment through the <em>mabbul</em> (מַבּוּל, deluge), destroying all flesh except Noah's family. The Flood demonstrates God's holiness that cannot tolerate sin, yet also His grace in preserving a remnant through the ark (תֵּבָה, <em>tevah</em>). Noah's ark typifies Christ as the sole means of salvation, the rainbow covenant establishes God's promise never again to destroy earth by flood, and the event prefigures the final judgment by fire. Peter explicitly connects the Flood to baptism (1 Peter 3:20-21) and end-times eschatology (2 Peter 3:5-7).",
                "verses": [
                    {"reference": "Genesis 7:17", "text": "And the flood was forty days upon the earth; and the waters increased, and bare up the ark, and it was lift up above the earth."},
                    {"reference": "Genesis 8:20", "text": "And Noah builded an altar unto the LORD; and took of every clean beast, and of every clean fowl, and offered burnt offerings on the altar."}
                ]
            }
        ],
        "The Patriarchs": [
            {
                "title": "Call of Abraham",
                "date": "c. 2500 BC",
                "alt_dates": "Ussher: 1921 BC • Scofield: 1996 BC",
                "description": "YHWH calls Abram (אַבְרָם, 'exalted father,' later Abraham, אַבְרָהָם, 'father of multitudes') from Ur of the Chaldees to Canaan, establishing the Abrahamic Covenant—foundational to all subsequent redemptive history. God's unconditional promise includes land (Canaan), seed (innumerable descendants), and blessing (to all nations through Abraham's seed). This covenant, confirmed by blood ritual (Genesis 15) and the sign of circumcision (בְּרִית מִילָה, <em>brit milah</em>), establishes Israel's election and foreshadows justification by faith alone (Genesis 15:6, cited in Romans 4:3, Galatians 3:6). Abraham's call initiates the progressive revelation of redemption, ultimately fulfilled in Christ, Abraham's seed (Galatians 3:16).",
                "verses": [
                    {"reference": "Genesis 12:1", "text": "Now the LORD had said unto Abram, Get thee out of thy country, and from thy kindred, and from thy father's house, unto a land that I will shew thee."},
                    {"reference": "Genesis 12:7", "text": "And the LORD appeared unto Abram, and said, Unto thy seed will I give this land: and there builded he an altar unto the LORD, who appeared unto him."}
                ]
            },
            {
                "title": "Birth of Isaac",
                "date": "c. 2400 BC",
                "alt_dates": "Ussher/Scofield: 1896 BC",
                "description": "God fulfills His covenant promise by miraculously granting Abraham and Sarah a son in their old age—Sarah ninety, Abraham one hundred—demonstrating that divine purposes depend not on human ability but divine power. Isaac (יִצְחָק, <em>Yitzchak</em>, 'laughter') embodies the promise, prefiguring Christ as the child of promise, the beloved son whom the father willingly offers (Genesis 22). The Akedah (עֲקֵדָה, binding of Isaac) establishes substitutionary atonement theology, as God provides a ram in Isaac's place, declaring 'Jehovah-Jireh' (יְהוָה יִרְאֶה, 'the LORD will provide')—ultimately fulfilled when God provides His own Son as substitute for sinners.",
                "verses": [
                    {"reference": "Genesis 21:2", "text": "For Sarah conceived, and bare Abraham a son in his old age, at the set time of which God had spoken to him."}
                ]
            },
            {
                "title": "Jacob and Esau",
                "date": "c. 2340 BC",
                "alt_dates": "Ussher/Scofield: 1836 BC",
                "description": "Isaac's twin sons embody sovereign election and its mysterious purposes. God's pre-temporal choice—'Jacob have I loved, but Esau have I hated' (Malachi 1:2-3, cited Romans 9:13)—establishes that salvation depends on divine mercy, not human merit or effort. Jacob (יַעֲקֹב, 'heel-catcher' or 'supplanter'), despite his scheming nature, receives the covenant blessing, demonstrating grace to the undeserving. His wrestling with God at Peniel transforms him into Israel (יִשְׂרָאֵל, 'God prevails' or 'he struggles with God'), establishing the name by which God's covenant people would be known. The twelve sons of Jacob/Israel become the patriarchs of the twelve tribes.",
                "verses": [
                    {"reference": "Genesis 25:23", "text": "And the LORD said unto her, Two nations are in thy womb, and two manner of people shall be separated from thy bowels; and the one people shall be stronger than the other people; and the elder shall serve the younger."}
                ]
            },
            {
                "title": "Joseph in Egypt",
                "date": "c. 2200 BC",
                "alt_dates": "Ussher/Scofield: 1706 BC",
                "description": "Joseph's life epitomizes divine providence working through human sin to accomplish redemptive purposes. Sold into Egyptian slavery by jealous brothers, Joseph's suffering and subsequent exaltation to Pharaoh's right hand typifies Christ's humiliation and glorification. His statement to his brothers—'ye thought evil against me; but God meant it unto good, to bring to pass, as it is this day, to save much people alive' (Genesis 50:20)—encapsulates the theological principle of divine sovereignty over human evil. Joseph preserves Jacob's family during famine, positioning Israel in Egypt where they multiply into a nation, setting the stage for the Exodus and establishing patterns of redemption through suffering.",
                "verses": [
                    {"reference": "Genesis 41:40", "text": "Thou shalt be over my house, and according unto thy word shall all my people be ruled: only in the throne will I be greater than thou."},
                    {"reference": "Genesis 50:20", "text": "But as for you, ye thought evil against me; but God meant it unto good, to bring to pass, as it is this day, to save much people alive."}
                ]
            }
        ],
        "Egypt and the Exodus": [
            {
                "title": "Israelites in Egyptian Bondage",
                "date": "c. 1800-1500 BC",
                "alt_dates": "Ussher/Scofield: c. 1600-1491 BC",
                "description": "As Israel multiplies in Egypt, fulfilling God's promise to Abraham, a new Pharaoh 'which knew not Joseph' enslaves them with cruel bondage (עֲבֹדָה, <em>avodah</em>), forcing them to build treasure cities. The oppression intensifies through infanticide—Pharaoh commands Hebrew midwives to kill male children—yet God preserves His people, and they multiply abundantly. This bondage establishes the theological pattern of redemption from slavery, prefiguring humanity's bondage to sin and Satan from which only divine intervention can deliver. The groaning (אָנַח, <em>anach</em>) of Israel reaches God, who remembers His covenant with Abraham, Isaac, and Jacob, setting in motion the Exodus—Scripture's central redemptive event.",
                "verses": [
                    {"reference": "Exodus 1:13-14", "text": "And the Egyptians made the children of Israel to serve with rigour: And they made their lives bitter with hard bondage, in morter, and in brick, and in all manner of service in the field: all their service, wherein they made them serve, was with rigour."}
                ]
            },
            {
                "title": "Birth of Moses",
                "date": "1571 BC",
                "alt_dates": "Ussher/Scofield: 1571 BC",
                "description": "God raises Moses (מֹשֶׁה, <em>Mosheh</em>, 'drawn out') to deliver Israel from bondage. His miraculous preservation in the Nile's bulrushes, adoption by Pharaoh's daughter, and education in Egyptian wisdom prepare him for covenant mediation. After forty years in Pharaoh's court and forty years as shepherd in Midian, God appears to Moses in the burning bush, revealing the Tetragrammaton (יהוה, YHWH) and commissioning him to confront Pharaoh. Moses' reluctance, Aaron's assistance, and the signs given demonstrate that divine calling equips despite human inadequacy. Moses typifies Christ as prophet, deliverer, and mediator of the covenant.",
                "verses": [
                    {"reference": "Exodus 2:10", "text": "And the child grew, and she brought him unto Pharaoh's daughter, and he became her son. And she called his name Moses: and she said, Because I drew him out of the water."}
                ]
            },
            {
                "title": "The Exodus from Egypt",
                "date": "1491 BC",
                "alt_dates": "Ussher/Scofield: 1491 BC",
                "description": "Through ten plagues demonstrating YHWH's supremacy over Egyptian gods, God breaks Pharaoh's will and delivers Israel from bondage. The Passover (פֶּסַח, <em>Pesach</em>)—lamb's blood on doorposts protecting from judgment—establishes the foundational type of Christ our Passover, sacrificed for us (1 Corinthians 5:7). The Red Sea crossing, where Israel passes through on dry ground while Egypt's army drowns, constitutes new creation imagery (baptismal waters of death and resurrection). This central Old Testament event establishes redemption theology: God delivers His people not by their merit but by His power, through blood sacrifice and sovereign intervention.",
                "verses": [
                    {"reference": "Exodus 12:37", "text": "And the children of Israel journeyed from Rameses to Succoth, about six hundred thousand on foot that were men, beside children."},
                    {"reference": "Exodus 14:21", "text": "And Moses stretched out his hand over the sea; and the LORD caused the sea to go back by a strong east wind all that night, and made the sea dry land, and the waters were divided."}
                ]
            },
            {
                "title": "Giving of the Law at Sinai",
                "date": "1491 BC",
                "alt_dates": "Ussher/Scofield: 1491 BC",
                "description": "At Mount Sinai (הַר סִינַי, <em>Har Sinai</em>), YHWH descends in fire and smoke, establishing the Mosaic Covenant through the Decalogue (עֲשֶׂרֶת הַדִּבְּרוֹת, <em>Aseret ha-Dibrot</em>, Ten Commandments) and comprehensive Torah. The covenant, mediated through Moses, establishes Israel as God's treasured possession (סְגֻלָּה, <em>segullah</em>), a kingdom of priests and holy nation. While the Abrahamic covenant was unconditional promise, the Mosaic covenant is conditional—'if ye will obey my voice indeed, and keep my covenant' (Exodus 19:5). The Law reveals God's holiness, exposes human sinfulness, and serves as παιδαγωγός (<em>paidagogos</em>, schoolmaster) to bring us to Christ (Galatians 3:24).",
                "verses": [
                    {"reference": "Exodus 19:20", "text": "And the LORD came down upon mount Sinai, on the top of the mount: and the LORD called Moses up to the top of the mount; and Moses went up."},
                    {"reference": "Exodus 20:1-2", "text": "And God spake all these words, saying, I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage."}
                ]
            }
        ],
        "Conquest and Judges": [
            {
                "title": "Conquest of Canaan",
                "date": "1491 BC",
                "alt_dates": "Ussher/Scofield: 1451 BC",
                "description": "Under Joshua (יְהוֹשֻׁעַ, <em>Yehoshua</em>, 'YHWH saves'—Greek Ἰησοῦς, Jesus), Israel crosses the Jordan and conquers Canaan, fulfilling God's promise to Abraham four centuries earlier. The miraculous fall of Jericho's walls demonstrates that victory comes not through military might but divine intervention—Israel marches, priests blow rams' horns (שׁוֹפָר, <em>shofar</em>), and God brings judgment. Joshua's leadership typifies Christ: both bear the same name (YHWH saves), both lead God's people into rest, both execute divine judgment on God's enemies. The <em>herem</em> (חֵרֶם, devoted destruction) of Canaanite cities, though troubling to modern sensibilities, reveals God's holy wrath against sin and foreshadows final judgment. Rahab's salvation by the scarlet cord prefigures salvation through Christ's blood.",
                "verses": [
                    {"reference": "Joshua 6:20", "text": "So the people shouted when the priests blew with the trumpets: and it came to pass, when the people heard the sound of the trumpet, and the people shouted with a great shout, that the wall fell down flat, so that the people went up into the city, every man straight before him, and they took the city."}
                ]
            },
            {
                "title": "Period of the Judges",
                "date": "1400-1050 BC",
                "alt_dates": "Ussher/Scofield: 1400-1050 BC",
                "description": "Following Joshua's death, Israel enters a dark cycle described in Judges: 'Every man did that which was right in his own eyes' (Judges 21:25). The recurring pattern—sin, oppression, crying out, deliverance—demonstrates humanity's persistent rebellion and God's patient mercy. YHWH raises <em>shofetim</em> (שֹׁפְטִים, judges)—charismatic deliverers like Deborah, Gideon, Jephthah, and Samson—who temporarily deliver Israel from oppressors (Philistines, Midianites, Ammonites). Yet these judges, though Spirit-empowered, remain flawed instruments, pointing forward to the need for a perfect King-Judge. The period reveals Israel's desperate need for monarchy under God, setting the stage for David and ultimately the Messianic King who judges righteously and delivers permanently.",
                "verses": [
                    {"reference": "Judges 2:16", "text": "Nevertheless the LORD raised up judges, which delivered them out of the hand of those that spoiled them."}
                ]
            }
        ],
        "The Kingdom Period": [
            {
                "title": "Saul Becomes King",
                "date": "1095 BC",
                "alt_dates": "Ussher/Scofield: 1095 BC",
                "description": "When Israel demands a king 'like all the nations' (1 Samuel 8:5), rejecting YHWH's direct rule, God gives them Saul (שָׁאוּל, <em>Shaul</em>, 'asked for')—impressive in stature, from Benjamin, anointed (מָשַׁח, <em>mashach</em>) by Samuel. Yet Saul's reign demonstrates the tragedy of partial obedience and self-reliance. His unauthorized sacrifice at Gilgal, his incomplete destruction of Amalek, and his jealous persecution of David reveal that outward qualifications mean nothing without heart obedience. God's rejection of Saul—'I have rejected him from reigning over Israel' (1 Samuel 16:1)—establishes that true kingship requires submission to divine authority. Saul's torment by an evil spirit and eventual suicide at Mount Gilboa warn against the danger of losing God's anointing through persistent disobedience.",
                "verses": [
                    {"reference": "1 Samuel 10:1", "text": "Then Samuel took a vial of oil, and poured it upon his head, and kissed him, and said, Is it not because the LORD hath anointed thee to be captain over his inheritance?"}
                ]
            },
            {
                "title": "David Becomes King",
                "date": "1055 BC",
                "alt_dates": "Ussher/Scofield: 1055 BC",
                "description": "David (דָּוִד, <em>David</em>, 'beloved'), anointed as youth while tending sheep, becomes Israel's greatest king and establishes the messianic dynasty. Though 'a man after God's own heart' (1 Samuel 13:14), David's greatness lies not in sinlessness but in genuine repentance when confronted with sin. God establishes the Davidic Covenant (2 Samuel 7)—promising David's throne, kingdom, and dynasty would endure forever—fulfilled ultimately in Christ, 'son of David, son of Abraham' (Matthew 1:1). David conquers Jerusalem, making it Israel's capital; brings the ark into the city; and receives the promise that his seed would build God's house. The Psalms David authored provide the hymnal of Scripture, expressing the full range of human emotion brought before God in worship, lament, and praise.",
                "verses": [
                    {"reference": "2 Samuel 5:3", "text": "So all the elders of Israel came to the king to Hebron; and king David made a league with them in Hebron before the LORD: and they anointed David king over Israel."}
                ]
            },
            {
                "title": "Solomon's Reign and Temple",
                "date": "1015-975 BC",
                "alt_dates": "Ussher: 1015-975 BC • Scofield: 1004-964 BC",
                "description": "Solomon (שְׁלֹמֹה, <em>Shlomo</em>, from שָׁלוֹם <em>shalom</em>, 'peace'), David's son, receives unprecedented wisdom from God and constructs the Temple (בֵּית הַמִּקְדָּשׁ, <em>Beit HaMikdash</em>)—fulfilling David's desire and God's promise. The Temple, with its Holy of Holies housing the Ark of the Covenant, becomes the locus of God's presence among His people, where sacrifice atones for sin and the high priest enters annually on Yom Kippur. Solomon's prayer at the Temple dedication (1 Kings 8) acknowledges that even this magnificent structure cannot contain the infinite God, yet God promises to meet His people there. However, Solomon's many foreign wives turn his heart toward idolatry (1 Kings 11), demonstrating that even great wisdom cannot substitute for covenant faithfulness. His apostasy sows seeds for the kingdom's division.",
                "verses": [
                    {"reference": "1 Kings 6:14", "text": "So Solomon built the house, and finished it."},
                    {"reference": "1 Kings 3:12", "text": "Behold, I have done according to thy words: lo, I have given thee a wise and an understanding heart; so that there was none like thee before thee, neither after thee shall any arise like unto thee."}
                ]
            },
            {
                "title": "Division of the Kingdom",
                "date": "975 BC",
                "alt_dates": "Ussher: 975 BC • Scofield: 975 BC",
                "description": "Solomon's son Rehoboam foolishly rejects the counsel of elders, declaring 'my little finger shall be thicker than my father's loins' (1 Kings 12:10), prompting ten northern tribes to revolt under Jeroboam. The united kingdom fractures into Israel (northern ten tribes, capital Samaria) and Judah (southern tribes of Judah and Benjamin, capital Jerusalem). Jeroboam immediately establishes idolatry, erecting golden calves at Dan and Bethel to prevent northern Israelites from worshiping in Jerusalem—'It is too much for you to go up to Jerusalem' (1 Kings 12:28). This schism fulfills prophetic judgment on Solomon's apostasy while demonstrating the bitter fruit of compromised worship. The divided monarchy persists until Assyria destroys Israel (722 BC) and Babylon conquers Judah (586 BC), vindicating the prophets' warnings that covenant unfaithfulness brings exile.",
                "verses": [
                    {"reference": "1 Kings 12:16", "text": "So when all Israel saw that the king hearkened not unto them, the people answered the king, saying, What portion have we in David? neither have we inheritance in the son of Jesse: to your tents, O Israel: now see to thine own house, David. So Israel departed unto their tents."}
                ]
            }
        ],
        "Exile and Return": [
            {
                "title": "Fall of Northern Kingdom",
                "date": "722 BC",
                "alt_dates": "Ussher/Scofield: 721 BC",
                "description": "After two centuries of apostasy—worshiping the golden calves, Baal, and Asherah—the northern kingdom falls to Assyria under Shalmaneser V and Sargon II. The ten tribes are deported to Assyria and Mesopotamia, effectively disappearing from history as the 'lost tribes.' Scripture records the theological verdict: 'For the children of Israel walked in all the sins of Jeroboam which he did; they departed not from them; until the LORD removed Israel out of his sight' (2 Kings 17:22-23). The Assyrians repopulate Samaria with foreigners who intermarry with remaining Israelites, creating the Samaritan people—despised by Jews in Jesus' time. The northern kingdom's destruction vindicates the prophets (Hosea, Amos) who warned that covenant breaking brings covenant curses (Deuteronomy 28). Israel's exile demonstrates God's holiness that cannot tolerate persistent idolatry.",
                "verses": [
                    {"reference": "2 Kings 17:6", "text": "In the ninth year of Hoshea the king of Assyria took Samaria, and carried Israel away into Assyria, and placed them in Halah and in Habor by the river of Gozan, and in the cities of the Medes."}
                ]
            },
            {
                "title": "Fall of Southern Kingdom",
                "date": "586 BC",
                "alt_dates": "Ussher: 586 BC • Scofield: 587 BC",
                "description": "Despite Judah's reforming kings (Hezekiah, Josiah), persistent apostasy under Manasseh and others seals Jerusalem's fate. Nebuchadnezzar of Babylon besieges Jerusalem, destroys Solomon's Temple, and deports the population to Babylon—fulfilling Jeremiah's prophecy of seventy years' captivity. The Temple's destruction marks the end of the sacrificial system and the Davidic monarchy's suspension. Yet even in judgment, God preserves a remnant, as Daniel, Ezekiel, and other exiles maintain covenant faithfulness in foreign lands. The <em>galut</em> (גָּלוּת, exile) becomes formative for Jewish identity and theology. Ezekiel's vision of dry bones (Ezekiel 37) promises future restoration, while Jeremiah announces a New Covenant (Jeremiah 31:31-34) superior to the Mosaic system—fulfilled in Christ's blood. Exile reveals that external covenant signs mean nothing without internal heart transformation.",
                "verses": [
                    {"reference": "2 Kings 25:9", "text": "And he burnt the house of the LORD, and the king's house, and all the houses of Jerusalem, and every great man's house burnt he with fire."}
                ]
            },
            {
                "title": "Return from Exile",
                "date": "538 BC",
                "alt_dates": "Ussher/Scofield: 536 BC",
                "description": "Precisely seventy years after the first deportation (Daniel 9:2), Cyrus the Persian—whom Isaiah prophesied by name two centuries earlier (Isaiah 44:28)—conquers Babylon and issues a decree permitting Jews to return and rebuild the Temple. This remarkable fulfillment of prophecy demonstrates God's sovereignty over pagan empires and His faithfulness to covenant promises. Zerubbabel leads the first return (Ezra 1-6), rebuilding the Temple despite opposition from Samaritans. Ezra later returns with religious reforms (Ezra 7-10), and Nehemiah rebuilds Jerusalem's walls (Nehemiah 1-6). Though the Second Temple lacks the ark and visible שְׁכִינָה (<em>Shekinah</em>, divine glory), and the Davidic monarchy remains suspended, the return from exile fulfills God's promise through Jeremiah. The restoration sets the stage for Messiah's coming—Jesus appears in this rebuilt Temple, declaring it 'my Father's house' (John 2:16).",
                "verses": [
                    {"reference": "Ezra 1:3", "text": "Who is there among you of all his people? his God be with him, and let him go up to Jerusalem, which is in Judah, and build the house of the LORD God of Israel, (he is the God,) which is in Jerusalem."}
                ]
            }
        ],
        "New Testament Era": [
            {
                "title": "Birth of Jesus Christ",
                "date": "7 BC",
                "alt_dates": "Ussher/Scofield: 4 BC",
                "description": "'When the fulness of the time was come, God sent forth his Son, made of a woman, made under the law' (Galatians 4:4)—Jesus (Ἰησοῦς, Greek form of Hebrew יְהוֹשֻׁעַ <em>Yeshua</em>, 'YHWH saves') is born in Bethlehem, fulfilling Micah 5:2. The virgin birth (Isaiah 7:14) demonstrates His divine nature—conceived by the Holy Spirit in Mary's womb, He is <em>Immanuel</em> (עִמָּנוּ אֵל, 'God with us'). Born under Augustus Caesar's census, in David's city, to a virgin of David's line, Jesus fulfills centuries of messianic prophecy. His birth unites deity and humanity in one person—the hypostatic union—making Him the perfect mediator between God and man. Angels announce 'good tidings of great joy' (Luke 2:10), shepherds worship, and magi present gifts befitting a king. Yet Herod's infanticide forces the holy family to flee to Egypt, fulfilling Hosea 11:1: 'Out of Egypt have I called my son.'",
                "verses": [
                    {"reference": "Luke 2:11", "text": "For unto you is born this day in the city of David a Saviour, which is Christ the Lord."},
                    {"reference": "Matthew 1:21", "text": "And she shall bring forth a son, and thou shalt call his name JESUS: for he shall save his people from their sins."}
                ]
            },
            {
                "title": "Ministry of Jesus",
                "date": "c. 30-33 AD",
                "alt_dates": "Ussher/Scofield: c. 27-30 AD",
                "description": "Following baptism by John and forty days' temptation in the wilderness, Jesus begins His public ministry proclaiming 'The time is fulfilled, and the kingdom of God is at hand' (Mark 1:15). His three-year ministry demonstrates His messianic credentials through σημεῖα (<em>semeia</em>, signs/miracles)—healing the sick, casting out demons, raising the dead, controlling nature—proving He is Israel's promised King. Jesus calls twelve apostles, teaches in parables, confronts Pharisaic legalism, and claims divine prerogatives (forgiving sins, claiming equality with the Father, accepting worship). His 'I AM' statements (John 6-15) identify Him with YHWH. The Sermon on the Mount reveals the kingdom's radical ethics; His table fellowship with sinners demonstrates grace; His cleansing of the Temple asserts messianic authority. Yet Israel's leaders reject Him, setting in motion the divine plan of redemption through the cross.",
                "verses": [
                    {"reference": "Mark 1:15", "text": "And saying, The time is fulfilled, and the kingdom of God is at hand: repent ye, and believe the gospel."}
                ]
            },
            {
                "title": "Crucifixion and Resurrection",
                "date": "c. 33 AD",
                "alt_dates": "Ussher/Scofield: 30 AD",
                "description": "On Passover (פֶּסַח, <em>Pesach</em>), Christ our Passover is sacrificed—arrested, tried by Sanhedrin and Pilate, mocked, scourged, and crucified at Golgotha. The sinless Son of God bears humanity's sin, enduring divine wrath as substitute (2 Corinthians 5:21). His cry 'It is finished' (τετέλεσται, <em>tetelestai</em>, 'paid in full,' John 19:30) declares sin's debt satisfied. The Temple veil tears (Matthew 27:51), symbolizing access to God through Christ's blood. Buried in Joseph's tomb, Jesus conquers death on the third day, rising bodily—the ἀπαρχή (<em>aparche</em>, firstfruits) of resurrection (1 Corinthians 15:20). His resurrection vindicates His claims, defeats Satan and death, and guarantees believers' future resurrection. Christ appears to disciples, proving His bodily resurrection, then ascends to the Father's right hand, where He intercedes as eternal High Priest (Hebrews 7:25).",
                "verses": [
                    {"reference": "1 Corinthians 15:3-4", "text": "For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures."}
                ]
            },
            {
                "title": "Day of Pentecost",
                "date": "c. 33 AD",
                "alt_dates": "Ussher/Scofield: 30 AD",
                "description": "Fifty days after Christ's resurrection, on the Jewish feast of Pentecost (Πεντηκοστή, <em>Pentekosté</em>, from פֶּנְטֵקוֹסְט <em>Shavuot</em>, Feast of Weeks), the Holy Spirit descends with 'a sound from heaven as of a rushing mighty wind' (Acts 2:2), filling 120 disciples gathered in Jerusalem's upper room. The Spirit's coming fulfills Joel 2:28-29 and Christ's promise of the παράκλητος (<em>parakletos</em>, Comforter/Advocate). Empowered disciples speak in foreign tongues (γλῶσσαι, <em>glossai</em>), reversing Babel's judgment and enabling gospel proclamation to Jews gathered from every nation. Peter preaches Christ crucified and risen—3,000 believe and are baptized, forming the nucleus of the ἐκκλησία (<em>ekklesia</em>, Church). Pentecost marks the Church's birth, the New Covenant's full inauguration, and the Spirit's permanent indwelling of believers—the down payment (ἀρραβών, <em>arrabon</em>) guaranteeing future glorification.",
                "verses": [
                    {"reference": "Acts 2:4", "text": "And they were all filled with the Holy Ghost, and began to speak with other tongues, as the Spirit gave them utterance."}
                ]
            },
            {
                "title": "Paul's Missionary Journeys",
                "date": "c. 47-60 AD",
                "alt_dates": "Ussher/Scofield: c. 45-58 AD",
                "description": "Paul (Παῦλος, <em>Paulos</em>, formerly Saul—converted on the Damascus road), commissioned as apostle to the Gentiles (Galatians 2:7-8), conducts three missionary journeys throughout Asia Minor, Greece, and Macedonia, establishing churches and writing epistles that form much of the New Testament. His gospel proclamation—justification by faith alone through Christ alone—liberates Gentiles from requiring circumcision and Torah observance for salvation, fulfilling God's promise to bless all nations through Abraham's seed (Galatians 3:8, 16). The Jerusalem Council (Acts 15) affirms grace over law. Paul's sufferings (beatings, shipwrecks, imprisonments) demonstrate apostolic credibility. His letters to churches (Romans, Corinthians, Galatians, Ephesians, Philippians, Colossians, Thessalonians) and individuals (Timothy, Titus, Philemon) establish Christian doctrine—salvation by grace through faith, the Church as Christ's body, sanctification through the Spirit, and the blessed hope of Christ's παρουσία (<em>parousia</em>, return).",
                "verses": [
                    {"reference": "Acts 13:2", "text": "As they ministered to the Lord, and fasted, the Holy Ghost said, Separate me Barnabas and Saul for the work whereunto I have called them."}
                ]
            }
        ]
    }

    # Chronological methodology note
    chronology_note = """<strong>Chronological Methodology:</strong> This timeline uses the Masoretic text with a gap-allowing
    interpretation of Genesis 5 and 11 genealogies. The Hebrew word 'begat' (<em>yalad</em>, יָלַד) may indicate either
    direct father-son relationships or ancestral lines with generational gaps. Direct father-son relationships are identified
    by textual markers such as 'he named him' or 'he called him' (e.g., Adam naming Seth in Genesis 5:3, Noah naming his sons
    in Genesis 5:32). Absent such indicators, 'begat' may mean 'was an ancestor of,' allowing for gaps in the genealogies.
    This yields dates of approximately 11,013 BC for Creation and 4,990 BC for the Flood.<br><br>
    <strong>Alternative Chronologies:</strong> Other prominent biblical chronologies use strict successive reckoning without
    allowing genealogical gaps. <strong>Ussher's Chronology</strong> (1650), found in many KJV margins, calculates 4004 BC
    for Creation and 2348 BC for the Flood. <strong>Scofield's Chronology</strong> (1909, revised 1917), featured in the
    influential Scofield Reference Bible used by evangelicals for generations, similarly dates Creation to 4004 BC and the
    Flood to 2348 BC, with some variations in later patriarchal dates. All three methods use the same Masoretic text but
    differ in their interpretation of genealogical relationships. Historical dates from the Assyrian and Babylonian periods
    (8th-6th centuries BC) are confirmed by archaeological and extra-biblical sources across all chronologies."""

    # Chronology comparison data for table
    chronology_comparison = [
        {"event": "Creation/Adam", "masoretic": "11,013 BC", "ussher": "4004 BC", "scofield": "4004 BC"},
        {"event": "The Flood", "masoretic": "4,990 BC", "ussher": "2348 BC", "scofield": "2348 BC"},
        {"event": "Call of Abraham", "masoretic": "c. 2500 BC", "ussher": "1921 BC", "scofield": "1996 BC"},
        {"event": "The Exodus", "masoretic": "c. 1491 BC", "ussher": "1491 BC", "scofield": "1491 BC"},
        {"event": "Solomon's Temple", "masoretic": "c. 1015 BC", "ussher": "1015 BC", "scofield": "1004 BC"},
        {"event": "Fall of Jerusalem", "masoretic": "586 BC", "ussher": "586 BC", "scofield": "587 BC"},
        {"event": "Birth of Christ", "masoretic": "7 BC", "ussher": "4 BC", "scofield": "4 BC"},
    ]

    return templates.TemplateResponse(
        "biblical_timeline.html",
        {
            "request": request,
            "books": books,
            "timeline_events": timeline_events,
            "chronology_note": chronology_note,
            "chronology_comparison": chronology_comparison,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Timeline", "url": None}
            ]
        }
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



@app.get("/sitemap.xml", response_class=Response)
def sitemap():
    """Generate comprehensive sitemap.xml with all URLs (cached daily)"""
    global _sitemap_cache, _sitemap_cache_date

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Return cached sitemap if it's from today
    if _sitemap_cache is not None and _sitemap_cache_date == current_date:
        return Response(content=_sitemap_cache, media_type="application/xml")

    # Generate new sitemap
    base_url = "https://kjvstudy.org"

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/search</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/books</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/study-guides</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/reading-plans</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/topics</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/resources</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/verse-of-the-day</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/concordance</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/interlinear</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-maps</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/family-tree</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-timeline</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-angels</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-prophets</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/names-of-god</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/tetragrammaton</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/parables</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-covenants</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/the-twelve-apostles</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/women-of-the-bible</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-festivals</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

    # Study guide slugs - dynamically extract from study_guides dictionary
    for category in study_guides.values():
        for guide in category:
            slug = guide["slug"]
            sitemap_xml += f"""    <url>
        <loc>{base_url}/study-guides/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    # Reading plan IDs
    reading_plan_ids = [
        "chronological", "one-year", "new-testament", "gospels-acts",
        "psalms-proverbs", "pentateuch", "prophets", "paul-epistles"
    ]
    for plan_id in reading_plan_ids:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/reading-plans/{plan_id}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    # Topic names
    topics = get_all_topics()
    for topic_name in topics.keys():
        sitemap_xml += f"""    <url>
        <loc>{base_url}/topics/{topic_name}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    # Biblical angels, prophets, names of God, parables, covenants, apostles, women, festivals slugs
    angel_slugs = ["michael", "gabriel", "lucifer", "abaddon"]
    for slug in angel_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-angels/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    prophet_slugs = ["moses", "elijah", "isaiah", "jeremiah", "ezekiel", "daniel", "jonah", "john-the-baptist"]
    for slug in prophet_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-prophets/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    god_name_slugs = ["elohim", "yahweh", "adonai", "el-shaddai", "yahweh-jireh", "yahweh-rapha", "yahweh-nissi", "yahweh-shalom", "yahweh-tsidkenu", "yahweh-shammah"]
    for slug in god_name_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/names-of-god/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    parable_slugs = ["sower", "wheat-tares", "mustard-seed", "good-samaritan", "prodigal-son", "lost-sheep", "talents", "wise-foolish-builders"]
    for slug in parable_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/parables/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    covenant_slugs = ["noahic", "abrahamic", "mosaic", "davidic", "new-covenant"]
    for slug in covenant_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-covenants/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    apostle_slugs = ["peter", "andrew", "james-son-of-zebedee", "john", "philip", "bartholomew", "thomas", "matthew", "james-son-of-alphaeus", "thaddaeus", "simon-zealot", "judas-iscariot"]
    for slug in apostle_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/the-twelve-apostles/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    women_slugs = ["eve", "sarah", "rebekah", "rachel", "miriam", "deborah", "ruth", "hannah", "esther", "mary-mother-of-jesus", "mary-magdalene", "martha"]
    for slug in women_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/women-of-the-bible/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    festival_slugs = ["passover", "unleavened-bread", "firstfruits", "pentecost", "trumpets", "atonement", "tabernacles"]
    for slug in festival_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-festivals/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    # Add all book URLs
    books = list(bible.iter_books())
    for book in books:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

        # Add book commentary URLs
        sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/commentary</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Add all chapter URLs and verse URLs for each book
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
        for chapter in chapters:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""
            # Add chapter commentary
            sitemap_xml += f"""    <url>
        <loc>{base_url}/commentary/{book}/{chapter}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""

            # Add all verse URLs for this chapter
            verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
            for verse_num in range(1, len(verses) + 1):
                sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}/verse/{verse_num}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.5</priority>
    </url>
"""

    sitemap_xml += "</urlset>"

    # Cache the generated sitemap
    _sitemap_cache = sitemap_xml
    _sitemap_cache_date = current_date

    return Response(content=sitemap_xml, media_type="application/xml")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    books = list(bible.iter_books())
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
        "index.html", {"request": request, "books": books, "daily_verse": daily_verse, "study_guides": study_guides}
    )


@app.get("/books", response_class=HTMLResponse)
def books_page(request: Request):
    """Browse all books of the Bible"""
    books = list(bible.iter_books())

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
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book_name]
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
        "books.html",
        {
            "request": request,
            "old_testament": old_testament,
            "new_testament": new_testament,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/reading-plans", response_class=HTMLResponse)
def reading_plans_page(request: Request):
    """Browse Bible reading plans"""
    books = list(bible.iter_books())
    plans = get_plan_summary()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": None}
    ]

    return templates.TemplateResponse(
        "reading_plans.html",
        {
            "request": request,
            "plans": plans,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/reading-plans/{plan_id}", response_class=HTMLResponse)
def reading_plan_detail(request: Request, plan_id: str):
    """View a specific reading plan"""
    books = list(bible.iter_books())
    plan = get_plan(plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": "/reading-plans"},
        {"text": plan["name"], "url": None}
    ]

    return templates.TemplateResponse(
        "reading_plan_detail.html",
        {
            "request": request,
            "plan": plan,
            "plan_id": plan_id,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/topics", response_class=HTMLResponse)
def topics_page(request: Request):
    """Browse topical index of Bible themes"""
    books = list(bible.iter_books())
    topics = get_all_topics()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": None}
    ]

    return templates.TemplateResponse(
        "topics.html",
        {
            "request": request,
            "topics": topics,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/resources", response_class=HTMLResponse)
def resources_page(request: Request):
    """Browse all theological resources"""
    books = list(bible.iter_books())

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
                "count": "Maps & places"
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
                "description": "Family trees and lineages traced through Scripture",
                "count": "Family trees"
            }
        ],
        "Study Tools": [
            {
                "name": "Study Guides",
                "url": "/study-guides",
                "description": "In-depth guides for studying biblical books, themes, and doctrines",
                "count": "Multiple guides"
            },
            {
                "name": "Parenting",
                "url": "/topics/Parenting",
                "description": "Biblical principles for raising children in the nurture and admonition of the Lord",
                "count": "6 subtopics"
            }
        ]
    }

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Resources", "url": None}
    ]

    return templates.TemplateResponse(
        "resources.html",
        {
            "request": request,
            "resources": resources,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/topics/{topic_name}", response_class=HTMLResponse)
def topic_detail(request: Request, topic_name: str):
    """View verses for a specific topic"""
    books = list(bible.iter_books())
    topic = get_topic(topic_name)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": "/topics"},
        {"text": topic_name, "url": None}
    ]

    return templates.TemplateResponse(
        "topic_detail.html",
        {
            "request": request,
            "topic": topic,
            "topic_name": topic_name,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@app.get("/book/{book}", response_class=HTMLResponse)
def read_book(request: Request, book: str):
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}", status_code=301)

    books = list(bible.iter_books())
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

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

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": None}
    ]

    return templates.TemplateResponse(
        "book.html",
        {
            "request": request,
            "book": book,
            "chapters": chapters,
            "books": books,
            "chapter_popularity": chapter_popularity,
            "chapter_explanations": chapter_explanations,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            **commentary_data
        },
    )


@app.get("/book/{book}/commentary", response_class=HTMLResponse)
def book_commentary(request: Request, book: str):
    """Generate comprehensive commentary for an entire book"""
    try:
        books = list(bible.iter_books())
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )

        # Generate comprehensive book commentary
        commentary_data = generate_book_commentary(book, chapters)

        return templates.TemplateResponse(
            "book_commentary.html",
            {
                "request": request,
                "book": book,
                "chapters": chapters,
                "books": books,
                **commentary_data
            },
        )
    except Exception as e:
        print(f"Error in book_commentary route for {book}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

        # Return a simple error page instead of 500
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Sorry, there was an error loading the commentary for {book}. Please try again later.",
                "book": book,
                "books": list(bible.iter_books()) if 'bible' in globals() else []
            },
            status_code=500
        )


@app.get("/book/{book}/{chapter}")
def redirect_chapter_legacy(book: str, chapter: int):
    """Redirect legacy chapter URLs to correct format"""
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}", status_code=301)

@app.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
def read_chapter(request: Request, book: str, chapter: int):
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}", status_code=301)

    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

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
    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)
        # Add word study sidenotes
        commentary['word_studies'] = generate_word_study_sidenotes(verse.text, book, chapter, verse.verse)
        # Add cross-references with proper URLs
        cross_refs = get_cross_references(book, chapter, verse.verse)
        commentary['cross_references'] = [
            {
                'text': ref['ref'],
                'url': f"/book/{ref['ref'].rsplit(' ', 1)[0]}/chapter/{ref['ref'].rsplit(' ', 1)[1].split(':')[0]}/verse/{ref['ref'].rsplit(' ', 1)[1].split(':')[1]}" if ' ' in ref['ref'] and ':' in ref['ref'] else '#',
                'context': ref['note']
            }
            for ref in cross_refs
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
        "chapter.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter
        }
    )


@app.get("/book/{book}/chapter/{chapter}/verse/{verse_num}", response_class=HTMLResponse)
def read_verse(request: Request, book: str, chapter: int, verse_num: int):
    """Display a single verse with detailed commentary"""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/verse/{verse_num}", status_code=301)

    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

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

    return templates.TemplateResponse(
        "verse.html",
        {
            "request": request,
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
            "related_content": related_content
        }
    )


@app.get("/commentary/{book}/{chapter}", response_class=HTMLResponse)
def commentary(request: Request, book: str, chapter: int):
    """Generate AI-powered commentary for a specific chapter"""
    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

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

    # Generate AI commentary for each verse
    commentaries = {}
    for verse in verses:
        commentaries[verse.verse] = generate_commentary(book, chapter, verse)

    # Generate chapter overview
    chapter_overview = generate_chapter_overview(book, chapter, verses)

    return templates.TemplateResponse(
        "commentary.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview
        },
    )


def escape_jinja2_syntax(text):
    """Escape Jinja2 syntax in text to prevent template parsing errors"""
    if not text:
        return text
    
    # Escape Jinja2 block tags
    text = text.replace('{%', '&#123;&#37;')
    text = text.replace('%}', '&#37;&#125;')
    
    # Escape Jinja2 variable tags
    text = text.replace('{{', '&#123;&#123;')
    text = text.replace('}}', '&#125;&#125;')
    
    # Escape Jinja2 comment tags
    text = text.replace('{#', '&#123;&#35;')
    text = text.replace('#}', '&#35;&#125;')
    
    return text

def link_bible_references(text):
    """Convert Bible references in text to clickable links

    Handles formats like:
    - Genesis 6:8
    - 1 John 4:8
    - Romans 5:1
    - Ephesians 2:8-10
    - Matthew 5:3-12
    """
    import re

    # Pattern matches book names (including numbered books) + chapter + verse (with optional range)
    # Examples: "Genesis 6:8", "1 John 4:8", "Romans 5:1", "Ephesians 2:8-10"
    pattern = r'\b((?:[123]\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def replace_reference(match):
        book_name = match.group(1)  # e.g., "Genesis", "1 John", "Song of Solomon"
        chapter = match.group(2)    # e.g., "6"
        verse_start = match.group(3)  # e.g., "8"
        verse_end = match.group(4)  # e.g., "10" (optional)

        # Full matched text (e.g., "Genesis 6:8" or "Romans 5:1-5")
        full_ref = match.group(0)

        # Create the link URL (link to the first verse in the range)
        url = f'/book/{book_name}/chapter/{chapter}/verse/{verse_start}'

        # Return the linked reference
        return f'<a href="{url}">{full_ref}</a>'

    # Replace all matches
    linked_text = re.sub(pattern, replace_reference, text)
    return linked_text


def generate_word_study_sidenotes(verse_text, book, chapter, verse_num):
    """Generate Hebrew/Greek/Aramaic word study sidenotes for key terms in the verse

    Uses intelligent selection to show only 1-2 word studies per verse, creating variety
    across chapters rather than showing every theological term.
    """
    verse_lower = verse_text.lower()

    # Determine if Old Testament (Hebrew/Aramaic) or New Testament (Greek)
    ot_books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
                "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
                "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
                "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
                "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]

    is_ot = book in ot_books

    # Comprehensive word study database
    word_studies = {
        # Divine names and titles
        "god": {
            "ot": {"term": "אֱלֹהִים", "translit": "Elohim", "meaning": "God (plural of majesty)", "note": "The Hebrew <strong>Elohim</strong> (אֱלֹהִים) is a plural form denoting majesty and fullness of deity. Though grammatically plural, it takes singular verbs when referring to the one true God, suggesting the Trinity's plurality within unity."},
            "nt": {"term": "Θεός", "translit": "Theos", "meaning": "God", "note": "The Greek <strong>Theos</strong> (Θεός) refers to deity, used both for the one true God and false gods. Context determines whether it denotes the Father specifically or the Godhead generally."}
        },
        "lord": {
            "ot": {"term": "יְהוָה / אֲדֹנָי", "translit": "YHWH / Adonai", "meaning": "The LORD / Lord", "note": "When 'LORD' appears in small capitals, it represents the Tetragrammaton <strong>YHWH</strong> (יְהוָה), God's personal covenant name meaning 'I AM.' When 'Lord' appears normally, it's <strong>Adonai</strong> (אֲדֹנָי), meaning 'my Lord,' emphasizing sovereignty."},
            "nt": {"term": "Κύριος", "translit": "Kurios", "meaning": "Lord, Master", "note": "The Greek <strong>Kurios</strong> (Κύριος) means 'lord' or 'master,' used both for human masters and divinely for God the Father and Jesus Christ. Its application to Jesus affirms His deity, as it translates YHWH in the Septuagint."}
        },
        "love": {
            "ot": {"term": "אַהֲבָה / חֶסֶד", "translit": "Ahavah / Chesed", "meaning": "Love / Loyal-love", "note": "Hebrew uses <strong>ahavah</strong> (אַהֲבָה) for love generally, but the covenant term <strong>chesed</strong> (חֶסֶד) describes God's steadfast, loyal love—faithful covenant commitment beyond mere emotion."},
            "nt": {"term": "ἀγάπη", "translit": "Agape", "meaning": "Divine love", "note": "The Greek <strong>agape</strong> (ἀγάπη) denotes self-sacrificial, unconditional love—the highest form of love, characterizing God's nature (1 John 4:8) and the love Christians are called to demonstrate."}
        },
        "faith": {
            "ot": {"term": "אֱמוּנָה", "translit": "Emunah", "meaning": "Faithfulness, trust", "note": "The Hebrew <strong>emunah</strong> (אֱמוּנָה) encompasses both faith and faithfulness—trusting God and being trustworthy. It implies steadfast reliability, as in 'The just shall live by his faith' (Habakkuk 2:4)."},
            "nt": {"term": "πίστις", "translit": "Pistis", "meaning": "Faith, belief, trust", "note": "The Greek <strong>pistis</strong> (πίστις) denotes faith, belief, or trust—confidence in God's character and promises. It's both intellectual assent and relational trust, central to justification (Romans 5:1)."}
        },
        "grace": {
            "ot": {"term": "חֵן", "translit": "Chen", "meaning": "Grace, favor", "note": "The Hebrew <strong>chen</strong> (חֵן) means grace or favor—unmerited kindness bestowed by a superior. Noah 'found grace in the eyes of the LORD' (Genesis 6:8), receiving undeserved favor."},
            "nt": {"term": "χάρις", "translit": "Charis", "meaning": "Grace, favor", "note": "The Greek <strong>charis</strong> (χάρις) denotes unmerited divine favor—God's kindness toward the undeserving. Salvation is 'by grace through faith' (Ephesians 2:8), not human merit."}
        },
        "mercy": {
            "ot": {"term": "רַחֲמִים", "translit": "Rachamim", "meaning": "Compassion, mercy", "note": "The Hebrew <strong>rachamim</strong> (רַחֲמִים) derives from 'womb' (<em>rechem</em>), suggesting tender, maternal compassion. God's mercies are 'new every morning' (Lamentations 3:23), showing His compassionate nature."},
            "nt": {"term": "ἔλεος", "translit": "Eleos", "meaning": "Mercy, compassion", "note": "The Greek <strong>eleos</strong> (ἔλεος) denotes compassionate mercy—pity for those in distress. God is 'rich in mercy' (Ephesians 2:4), withholding deserved punishment and granting undeserved kindness."}
        },
        "righteous": {
            "ot": {"term": "צַדִּיק", "translit": "Tzaddik", "meaning": "Righteous one", "note": "The Hebrew <strong>tzaddik</strong> (צַדִּיק) describes one who is righteous, just, or lawful—conforming to God's standard. From the root <em>tzedek</em> (צֶדֶק), meaning righteousness or justice."},
            "nt": {"term": "δίκαιος", "translit": "Dikaios", "meaning": "Righteous, just", "note": "The Greek <strong>dikaios</strong> (δίκαιος) means righteous or just—conforming to God's standard. Christ's righteousness is imputed to believers through faith (Romans 4:5), making them legally righteous before God."}
        },
        "salvation": {
            "ot": {"term": "יְשׁוּעָה", "translit": "Yeshuah", "meaning": "Salvation, deliverance", "note": "The Hebrew <strong>yeshuah</strong> (יְשׁוּעָה) means salvation or deliverance—rescue from danger or enemies. This is the root of 'Jesus' (<em>Yeshua</em>), meaning 'YHWH saves.'"},
            "nt": {"term": "σωτηρία", "translit": "Soteria", "meaning": "Salvation, deliverance", "note": "The Greek <strong>soteria</strong> (σωτηρία) denotes salvation, deliverance, or preservation—rescue from sin's penalty and power. It encompasses justification, sanctification, and glorification."}
        },
        "redeem": {
            "ot": {"term": "גָּאַל", "translit": "Gaal", "meaning": "To redeem, act as kinsman-redeemer", "note": "The Hebrew <strong>gaal</strong> (גָּאַל) means to redeem or act as kinsman-redeemer (<em>go'el</em>)—buying back family property or relatives. It foreshadows Christ redeeming His people through His blood."},
            "nt": {"term": "λυτρόω", "translit": "Lutroo", "meaning": "To redeem, ransom", "note": "The Greek <strong>lutroo</strong> (λυτρόω) means to redeem or ransom—purchasing freedom by paying a price. Christ redeemed us 'with the precious blood' (1 Peter 1:18-19), the ransom for sin."}
        },
        "covenant": {
            "ot": {"term": "בְּרִית", "translit": "Berit", "meaning": "Covenant, treaty", "note": "The Hebrew <strong>berit</strong> (בְּרִית) denotes a covenant—a binding agreement, often ratified by blood sacrifice. God's covenants (Abrahamic, Mosaic, Davidic) structure redemptive history, culminating in the New Covenant."},
            "nt": {"term": "διαθήκη", "translit": "Diatheke", "meaning": "Covenant, testament", "note": "The Greek <strong>diatheke</strong> (διαθήκη) means covenant or testament—a binding arrangement. The New Covenant (Jeremiah 31:31-34) is ratified by Christ's blood, surpassing the old (Hebrews 8:6-13)."}
        },
        "glory": {
            "ot": {"term": "כָּבוֹד", "translit": "Kavod", "meaning": "Glory, weight, honor", "note": "The Hebrew <strong>kavod</strong> (כָּבוֹד) literally means 'weight' or 'heaviness,' metaphorically denoting glory, honor, or majesty. God's glory (<em>Shekinah</em>) filled the tabernacle (Exodus 40:34) and temple (1 Kings 8:11)."},
            "nt": {"term": "δόξα", "translit": "Doxa", "meaning": "Glory, majesty, splendor", "note": "The Greek <strong>doxa</strong> (δόξα) means glory, splendor, or magnificence—the radiant manifestation of God's perfection. Christ revealed the Father's glory: 'we beheld his glory' (John 1:14)."}
        },
        "holy": {
            "ot": {"term": "קָדוֹשׁ", "translit": "Qadosh", "meaning": "Holy, set apart", "note": "The Hebrew <strong>qadosh</strong> (קָדוֹשׁ) means holy or set apart—separated from common use for God's purposes. God is 'the Holy One of Israel,' utterly distinct from creation in moral perfection."},
            "nt": {"term": "ἅγιος", "translit": "Hagios", "meaning": "Holy, sacred, set apart", "note": "The Greek <strong>hagios</strong> (ἅγιος) denotes holiness—moral purity and separation unto God. Believers are called 'saints' (<em>hagioi</em>), those set apart for God through Christ's sanctifying work."}
        },
        "peace": {
            "ot": {"term": "שָׁלוֹם", "translit": "Shalom", "meaning": "Peace, wholeness, prosperity", "note": "The Hebrew <strong>shalom</strong> (שָׁלוֹם) encompasses peace, wholeness, completeness, and welfare—not merely absence of conflict but positive flourishing. God is <em>Jehovah-Shalom</em>, 'the LORD is Peace' (Judges 6:24)."},
            "nt": {"term": "εἰρήνη", "translit": "Eirene", "meaning": "Peace, harmony", "note": "The Greek <strong>eirene</strong> (εἰρήνη) means peace or harmony—both the inner tranquility of reconciliation with God and relational harmony. Christ is 'our peace' (Ephesians 2:14), reconciling us to God."}
        },
        "spirit": {
            "ot": {"term": "רוּחַ", "translit": "Ruach", "meaning": "Spirit, wind, breath", "note": "The Hebrew <strong>ruach</strong> (רוּחַ) means spirit, wind, or breath—invisible but powerful. It describes both the Holy Spirit and the human spirit. God's Spirit gives life and empowers His people."},
            "nt": {"term": "πνεῦμα", "translit": "Pneuma", "meaning": "Spirit, wind, breath", "note": "The Greek <strong>pneuma</strong> (πνεῦμα) means spirit, wind, or breath—the immaterial aspect of persons. The Holy Spirit (<em>Pneuma Hagion</em>) is the third person of the Trinity, dwelling in believers."}
        },
        "wisdom": {
            "ot": {"term": "חָכְמָה", "translit": "Chokhmah", "meaning": "Wisdom, skill", "note": "The Hebrew <strong>chokhmah</strong> (חָכְמָה) denotes wisdom—practical skill in living righteously. 'The fear of the LORD is the beginning of wisdom' (Proverbs 9:10), grounding all true knowledge in reverence for God."},
            "nt": {"term": "σοφία", "translit": "Sophia", "meaning": "Wisdom, insight", "note": "The Greek <strong>sophia</strong> (σοφία) means wisdom or insight—skillful living and right judgment. Christ is 'the wisdom of God' (1 Corinthians 1:24), and God gives wisdom liberally to those who ask (James 1:5)."}
        },
        "truth": {
            "ot": {"term": "אֱמֶת", "translit": "Emet", "meaning": "Truth, faithfulness", "note": "The Hebrew <strong>emet</strong> (אֱמֶת) means truth or faithfulness—reliability and conformity to reality. God is true (<em>emet</em>), utterly faithful to His word and character."},
            "nt": {"term": "ἀλήθεια", "translit": "Aletheia", "meaning": "Truth, reality", "note": "The Greek <strong>aletheia</strong> (ἀλήθεια) denotes truth or reality—that which corresponds to actuality. Jesus declared, 'I am the way, the truth, and the life' (John 14:6), embodying ultimate reality."}
        },
        "sin": {
            "ot": {"term": "חַטָּאת", "translit": "Chatta'ah", "meaning": "Sin, missing the mark", "note": "The Hebrew <strong>chatta'ah</strong> (חַטָּאת) means sin—missing the mark of God's standard. It encompasses rebellion, transgression, and falling short of divine holiness."},
            "nt": {"term": "ἁμαρτία", "translit": "Hamartia", "meaning": "Sin, missing the mark", "note": "The Greek <strong>hamartia</strong> (ἁμαρτία) means sin—missing the target of God's perfection. 'All have sinned and fall short of the glory of God' (Romans 3:23), requiring Christ's atoning sacrifice."}
        },
        "kingdom": {
            "ot": {"term": "מַלְכוּת", "translit": "Malkhut", "meaning": "Kingdom, reign, royal power", "note": "The Hebrew <strong>malkhut</strong> (מַלְכוּת) denotes kingdom or royal rule—the realm and reign of a king. God's kingdom represents His sovereign rule over all creation."},
            "nt": {"term": "βασιλεία", "translit": "Basileia", "meaning": "Kingdom, reign", "note": "The Greek <strong>basileia</strong> (βασιλεία) means kingdom—both the realm ruled and the exercise of royal authority. The 'kingdom of God' is central to Jesus' teaching, representing God's saving rule breaking into history."}
        },
        "sacrifice": {
            "ot": {"term": "זֶבַח", "translit": "Zevach", "meaning": "Sacrifice, offering", "note": "The Hebrew <strong>zevach</strong> (זֶבַח) denotes a sacrifice or offering—an animal slaughtered for worship. Old Testament sacrifices foreshadowed Christ, 'the Lamb of God' (John 1:29)."},
            "nt": {"term": "θυσία", "translit": "Thusia", "meaning": "Sacrifice, offering", "note": "The Greek <strong>thusia</strong> (θυσία) means sacrifice or offering. Christ offered Himself as the perfect sacrifice 'once for all' (Hebrews 10:10), ending the need for repeated animal sacrifices."}
        },
        "word": {
            "ot": {"term": "דָּבָר", "translit": "Davar", "meaning": "Word, thing, matter", "note": "The Hebrew <strong>davar</strong> (דָּבָר) means word, thing, or matter—God's creative and authoritative speech. 'By the word of the LORD were the heavens made' (Psalm 33:6)."},
            "nt": {"term": "λόγος", "translit": "Logos", "meaning": "Word, reason, message", "note": "The Greek <strong>Logos</strong> (Λόγος) means word, reason, or message—the rational principle underlying reality. John identifies Christ as the eternal Logos: 'In the beginning was the Word' (John 1:1)."}
        },
        "church": {
            "nt": {"term": "ἐκκλησία", "translit": "Ekklesia", "meaning": "Assembly, church", "note": "The Greek <strong>ekklesia</strong> (ἐκκλησία) means assembly or called-out ones—the gathering of believers. Christ builds His church (Matthew 16:18), the body of Christ comprising all the redeemed."}
        },
        "baptize": {
            "nt": {"term": "βαπτίζω", "translit": "Baptizo", "meaning": "To baptize, immerse", "note": "The Greek <strong>baptizo</strong> (βαπτίζω) means to dip, immerse, or baptize. Christian baptism symbolizes identification with Christ's death, burial, and resurrection (Romans 6:3-4)."}
        },
        "gospel": {
            "nt": {"term": "εὐαγγέλιον", "translit": "Euangelion", "meaning": "Good news, gospel", "note": "The Greek <strong>euangelion</strong> (εὐαγγέλιον) means good news or gospel—the message of salvation through Christ's death and resurrection. It's 'the power of God unto salvation' (Romans 1:16)."}
        },

        # Worship and Religious Practice
        "worship": {
            "ot": {"term": "שָׁחָה", "translit": "Shachah", "meaning": "To bow down, worship", "note": "The Hebrew <strong>shachah</strong> (שָׁחָה) means to bow down or prostrate oneself in worship—physical expression of reverence and submission to God. True worship involves both outward posture and inward devotion."},
            "nt": {"term": "προσκυνέω", "translit": "Proskuneo", "meaning": "To worship, bow down", "note": "The Greek <strong>proskuneo</strong> (προσκυνέω) means to worship or pay homage—literally 'to kiss toward.' Jesus taught that true worshipers must worship 'in spirit and in truth' (John 4:24)."}
        },
        "prayer": {
            "ot": {"term": "תְּפִלָּה", "translit": "Tefillah", "meaning": "Prayer, intercession", "note": "The Hebrew <strong>tefillah</strong> (תְּפִלָּה) means prayer or intercession—communion with God through petition and praise. Solomon's temple was to be 'a house of prayer for all people' (Isaiah 56:7)."},
            "nt": {"term": "προσευχή", "translit": "Proseuche", "meaning": "Prayer, petition", "note": "The Greek <strong>proseuche</strong> (προσευχή) denotes prayer—communication with God. Believers are exhorted to 'pray without ceasing' (1 Thessalonians 5:17) and 'in everything by prayer and supplication' present requests to God (Philippians 4:6)."}
        },
        "praise": {
            "ot": {"term": "הָלַל", "translit": "Halal", "meaning": "To praise, celebrate", "note": "The Hebrew <strong>halal</strong> (הָלַל) means to praise or celebrate boisterously—the root of 'Hallelujah' (praise YHWH). The Psalms overflow with calls to praise God for His character and works."},
            "nt": {"term": "αἰνέω", "translit": "Aineo", "meaning": "To praise, extol", "note": "The Greek <strong>aineo</strong> (αἰνέω) means to praise or extol—expressing admiration and gratitude. The early church devoted themselves to 'praising God' (Acts 2:47) continually."}
        },
        "temple": {
            "ot": {"term": "הֵיכָל", "translit": "Heikhal", "meaning": "Temple, palace", "note": "The Hebrew <strong>heikhal</strong> (הֵיכָל) denotes God's temple or palace—the sacred dwelling place where God's presence resided. Solomon's temple was the center of Israel's worship until its destruction."},
            "nt": {"term": "ναός", "translit": "Naos", "meaning": "Temple, sanctuary", "note": "The Greek <strong>naos</strong> (ναός) means temple or inner sanctuary. Paul declares believers are 'the temple of the living God' (2 Corinthians 6:16), individually (1 Corinthians 6:19) and corporately as the church."}
        },
        "altar": {
            "ot": {"term": "מִזְבֵּחַ", "translit": "Mizbeach", "meaning": "Altar, place of sacrifice", "note": "The Hebrew <strong>mizbeach</strong> (מִזְבֵּחַ) means altar—from the root 'to slaughter.' Altars were places where sacrifices were offered to God, pointing forward to Christ's ultimate sacrifice."},
            "nt": {"term": "θυσιαστήριον", "translit": "Thusiastērion", "meaning": "Altar", "note": "The Greek <strong>thusiastērion</strong> (θυσιαστήριον) denotes an altar for sacrifice. Hebrews 13:10 declares 'We have an altar' from which temple priests cannot eat—referring to Christ's sacrifice outside the camp."}
        },
        "priest": {
            "ot": {"term": "כֹּהֵן", "translit": "Kohen", "meaning": "Priest", "note": "The Hebrew <strong>kohen</strong> (כֹּהֵן) denotes a priest—one who mediates between God and people through sacrifices and intercession. Aaron and his descendants served as Israel's priests, foreshadowing Christ the Great High Priest."},
            "nt": {"term": "ἱερεύς", "translit": "Hiereus", "meaning": "Priest", "note": "The Greek <strong>hiereus</strong> (ἱερεύς) means priest. Christ is our eternal High Priest (Hebrews 4:14) after the order of Melchizedek, and believers form a 'royal priesthood' (1 Peter 2:9)."}
        },

        # Spiritual Beings and Realms
        "angel": {
            "ot": {"term": "מַלְאָךְ", "translit": "Mal'akh", "meaning": "Angel, messenger", "note": "The Hebrew <strong>mal'akh</strong> (מַלְאָךְ) means angel or messenger—a heavenly being sent by God. Angels serve as God's messengers, worship Him, and minister to believers (Hebrews 1:14)."},
            "nt": {"term": "ἄγγελος", "translit": "Angelos", "meaning": "Angel, messenger", "note": "The Greek <strong>angelos</strong> (ἄγγελος) means angel or messenger. Angels announced Christ's birth (Luke 2:9-14), ministered to Him (Matthew 4:11), and will accompany His return (Matthew 25:31)."}
        },
        "heaven": {
            "ot": {"term": "שָׁמַיִם", "translit": "Shamayim", "meaning": "Heaven, sky", "note": "The Hebrew <strong>shamayim</strong> (שָׁמַיִם) means heaven or sky—God's dwelling place and the realm above earth. 'The heaven, even the heavens, are the LORD's' (Psalm 115:16), yet 'the heaven of heavens cannot contain Him' (1 Kings 8:27)."},
            "nt": {"term": "οὐρανός", "translit": "Ouranos", "meaning": "Heaven, sky", "note": "The Greek <strong>ouranos</strong> (οὐρανός) denotes heaven—God's throne and the believer's eternal home. Jesus taught His disciples to pray 'Our Father which art in heaven' (Matthew 6:9) and promised to prepare a place there (John 14:2)."}
        },
        "earth": {
            "ot": {"term": "אֶרֶץ", "translit": "Eretz", "meaning": "Earth, land", "note": "The Hebrew <strong>eretz</strong> (אֶרֶץ) means earth or land—the physical world God created. 'The earth is the LORD's, and the fulness thereof' (Psalm 24:1), given to humanity as stewards."},
            "nt": {"term": "γῆ", "translit": "Gē", "meaning": "Earth, land", "note": "The Greek <strong>gē</strong> (γῆ) denotes earth or land. While believers are 'strangers and pilgrims on the earth' (Hebrews 11:13), they await 'new heavens and a new earth' (2 Peter 3:13) where righteousness dwells."}
        },

        # Human Nature and Faculties
        "soul": {
            "ot": {"term": "נֶפֶשׁ", "translit": "Nephesh", "meaning": "Soul, life, self", "note": "The Hebrew <strong>nephesh</strong> (נֶפֶשׁ) denotes the soul or life—the immaterial essence of a person. It represents the whole person, their desires, emotions, and will. God breathed into man and he became 'a living soul' (Genesis 2:7)."},
            "nt": {"term": "ψυχή", "translit": "Psuche", "meaning": "Soul, life, self", "note": "The Greek <strong>psuche</strong> (ψυχή) means soul or life—the seat of emotions and will. Jesus asked, 'What shall it profit a man, if he shall gain the whole world, and lose his own soul?' (Mark 8:36)."}
        },
        "heart": {
            "ot": {"term": "לֵב", "translit": "Lev", "meaning": "Heart, mind, will", "note": "The Hebrew <strong>lev</strong> (לֵב) denotes the heart—the center of thought, emotion, and will. God commanded Israel to 'love the LORD thy God with all thine heart' (Deuteronomy 6:5), and He promised a 'new heart' (Ezekiel 36:26)."},
            "nt": {"term": "καρδία", "translit": "Kardia", "meaning": "Heart, mind, inner self", "note": "The Greek <strong>kardia</strong> (καρδία) means heart—the inner person, seat of thoughts and affections. 'Out of the abundance of the heart the mouth speaketh' (Matthew 12:34), and believers must guard their hearts (Proverbs 4:23)."}
        },
        "flesh": {
            "ot": {"term": "בָּשָׂר", "translit": "Basar", "meaning": "Flesh, body", "note": "The Hebrew <strong>basar</strong> (בָּשָׂר) means flesh or body—humanity's physical, mortal nature. 'All flesh is grass' (Isaiah 40:6), emphasizing human frailty and mortality before the eternal God."},
            "nt": {"term": "σάρξ", "translit": "Sarx", "meaning": "Flesh, sinful nature", "note": "The Greek <strong>sarx</strong> (σάρξ) denotes flesh—both physical body and fallen human nature opposed to God. Paul contrasts walking 'after the flesh' versus 'after the Spirit' (Romans 8:4-5). The Word became flesh (John 1:14) in the incarnation."}
        },
        "mind": {
            "nt": {"term": "νοῦς", "translit": "Nous", "meaning": "Mind, understanding", "note": "The Greek <strong>nous</strong> (νοῦς) means mind or understanding—the faculty of thought and perception. Believers are to be transformed by the 'renewing of your mind' (Romans 12:2) and have 'the mind of Christ' (1 Corinthians 2:16)."}
        },

        # Spiritual States and Actions
        "blessing": {
            "ot": {"term": "בְּרָכָה", "translit": "Berakhah", "meaning": "Blessing, prosperity", "note": "The Hebrew <strong>berakhah</strong> (בְּרָכָה) means blessing—divine favor bringing prosperity and well-being. God blessed Abraham to be a blessing (Genesis 12:2), and obedience brings blessing while disobedience brings curse (Deuteronomy 28)."},
            "nt": {"term": "εὐλογία", "translit": "Eulogia", "meaning": "Blessing, praise", "note": "The Greek <strong>eulogia</strong> (εὐλογία) denotes blessing—divine favor or words of praise. Believers are blessed with 'all spiritual blessings in heavenly places in Christ' (Ephesians 1:3) and called to 'bless them which persecute you' (Romans 12:14)."}
        },
        "hope": {
            "ot": {"term": "תִּקְוָה", "translit": "Tikvah", "meaning": "Hope, expectation", "note": "The Hebrew <strong>tikvah</strong> (תִּקְוָה) means hope or expectation—confident trust in God's promises. 'Happy is he that hath the God of Jacob for his help, whose hope is in the LORD his God' (Psalm 146:5)."},
            "nt": {"term": "ἐλπίς", "translit": "Elpis", "meaning": "Hope, expectation", "note": "The Greek <strong>elpis</strong> (ἐλπίς) denotes hope—confident expectation of good. This hope is 'an anchor of the soul' (Hebrews 6:19), grounded in Christ's resurrection and the believer's future inheritance (1 Peter 1:3-4)."}
        },
        "joy": {
            "ot": {"term": "שִׂמְחָה", "translit": "Simchah", "meaning": "Joy, gladness", "note": "The Hebrew <strong>simchah</strong> (שִׂמְחָה) means joy or gladness—deep delight in God. 'The joy of the LORD is your strength' (Nehemiah 8:10), and God's presence brings 'fulness of joy' (Psalm 16:11)."},
            "nt": {"term": "χαρά", "translit": "Chara", "meaning": "Joy, gladness", "note": "The Greek <strong>chara</strong> (χαρά) denotes joy—deep spiritual gladness. This joy is a fruit of the Spirit (Galatians 5:22), independent of circumstances. Jesus promised that His joy would remain in believers, making their joy full (John 15:11)."}
        },
        "fear": {
            "ot": {"term": "יִרְאָה", "translit": "Yirah", "meaning": "Fear, reverence", "note": "The Hebrew <strong>yirah</strong> (יִרְאָה) means fear or reverence—awe and respect before God. 'The fear of the LORD is the beginning of wisdom' (Proverbs 9:10), combining reverent awe with trust in God's goodness."},
            "nt": {"term": "φόβος", "translit": "Phobos", "meaning": "Fear, reverence", "note": "The Greek <strong>phobos</strong> (φόβος) means fear—both terror and reverential awe. While perfect love casts out servile fear (1 John 4:18), believers are to 'fear God, and give glory to him' (Revelation 14:7) with holy reverence."}
        },

        # Religious Roles
        "prophet": {
            "ot": {"term": "נָבִיא", "translit": "Navi", "meaning": "Prophet, spokesman", "note": "The Hebrew <strong>navi</strong> (נָבִיא) means prophet—one who speaks God's word to the people. Prophets received divine revelation and declared God's message, often calling Israel to repentance and foretelling future events."},
            "nt": {"term": "προφήτης", "translit": "Prophētēs", "meaning": "Prophet", "note": "The Greek <strong>prophētēs</strong> (προφήτης) denotes a prophet—one who speaks forth God's message. Jesus was recognized as 'a prophet mighty in deed and word' (Luke 24:19), fulfilling and surpassing the prophetic office."}
        },
        "apostle": {
            "nt": {"term": "ἀπόστολος", "translit": "Apostolos", "meaning": "Apostle, sent one", "note": "The Greek <strong>apostolos</strong> (ἀπόστολος) means apostle or sent one—an authorized messenger. The twelve apostles were chosen by Christ and empowered as His witnesses, laying the foundation of the church (Ephesians 2:20)."}
        },
        "disciple": {
            "nt": {"term": "μαθητής", "translit": "Mathētēs", "meaning": "Disciple, learner", "note": "The Greek <strong>mathētēs</strong> (μαθητής) means disciple or learner—one who follows a teacher. Jesus called His followers to deny themselves, take up their cross, and follow Him (Matthew 16:24), learning from Him continually."}
        },

        # Law and Judgment
        "law": {
            "ot": {"term": "תּוֹרָה", "translit": "Torah", "meaning": "Law, instruction", "note": "The Hebrew <strong>Torah</strong> (תּוֹרָה) means law or instruction—God's revealed will for His people. The Law includes moral, civil, and ceremonial commandments, revealing God's character and humanity's need for a Savior."},
            "nt": {"term": "νόμος", "translit": "Nomos", "meaning": "Law", "note": "The Greek <strong>nomos</strong> (νόμος) denotes law—particularly the Mosaic law. While believers are not under law but under grace (Romans 6:14), Christ fulfilled the law (Matthew 5:17) and wrote it on believers' hearts (Hebrews 8:10)."}
        },
        "judgment": {
            "ot": {"term": "מִשְׁפָּט", "translit": "Mishpat", "meaning": "Judgment, justice", "note": "The Hebrew <strong>mishpat</strong> (מִשְׁפָּט) means judgment or justice—God's righteous decisions and ordinances. God is the Judge of all the earth who 'shall do right' (Genesis 18:25), executing perfect justice."},
            "nt": {"term": "κρίσις", "translit": "Krisis", "meaning": "Judgment, decision", "note": "The Greek <strong>krisis</strong> (κρίσις) denotes judgment—evaluation and sentence. All will stand before God's judgment seat (Romans 14:10), and Christ has been appointed Judge of the living and dead (Acts 10:42)."}
        },
        "wrath": {
            "ot": {"term": "אַף", "translit": "Aph", "meaning": "Wrath, anger", "note": "The Hebrew <strong>aph</strong> (אַף) literally means 'nose' or 'nostrils,' idiomatically expressing wrath or anger—God's righteous indignation against sin. Yet God is 'slow to anger' (Exodus 34:6) and 'abundant in mercy.'"},
            "nt": {"term": "ὀργή", "translit": "Orgē", "meaning": "Wrath, anger", "note": "The Greek <strong>orgē</strong> (ὀργή) means wrath—settled, righteous anger against sin. Believers are 'saved from wrath through him' (Romans 5:9), as Christ bore God's wrath on the cross, satisfying divine justice."}
        },

        # Eschatological Terms
        "resurrection": {
            "nt": {"term": "ἀνάστασις", "translit": "Anastasis", "meaning": "Resurrection, rising", "note": "The Greek <strong>anastasis</strong> (ἀνάστασις) means resurrection—rising from death to life. Christ's resurrection is the 'firstfruits' (1 Corinthians 15:20), guaranteeing believers' future bodily resurrection and victory over death."}
        },
        "eternal": {
            "ot": {"term": "עוֹלָם", "translit": "Olam", "meaning": "Eternal, everlasting", "note": "The Hebrew <strong>olam</strong> (עוֹלָם) means eternal or everlasting—time stretching beyond human comprehension. God is the 'everlasting God' (Genesis 21:33), and His covenant love endures forever."},
            "nt": {"term": "αἰώνιος", "translit": "Aiōnios", "meaning": "Eternal, everlasting", "note": "The Greek <strong>aiōnios</strong> (αἰώνιος) denotes eternal or everlasting—unending duration. Believers possess 'eternal life' (John 3:16) now and will dwell with God eternally, while the impenitent face 'eternal punishment' (Matthew 25:46)."}
        },
        "life": {
            "ot": {"term": "חַיִּים", "translit": "Chayyim", "meaning": "Life, living", "note": "The Hebrew <strong>chayyim</strong> (חַיִּים) means life—existence, vitality, and well-being. God is the source of all life, and He offers 'the fountain of life' (Psalm 36:9) to those who seek Him."},
            "nt": {"term": "ζωή", "translit": "Zōē", "meaning": "Life", "note": "The Greek <strong>zōē</strong> (ζωή) denotes life—particularly spiritual and eternal life. Jesus declared 'I am the way, the truth, and the life' (John 14:6) and came that believers 'might have life, and have it more abundantly' (John 10:10)."}
        },
        "death": {
            "ot": {"term": "מָוֶת", "translit": "Mavet", "meaning": "Death", "note": "The Hebrew <strong>mavet</strong> (מָוֶת) means death—the cessation of physical life and separation from God. Death entered through sin (Genesis 2:17), but God promises deliverance: 'O death, I will be thy plagues' (Hosea 13:14)."},
            "nt": {"term": "θάνατος", "translit": "Thanatos", "meaning": "Death", "note": "The Greek <strong>thanatos</strong> (θάνατος) denotes death—both physical death and spiritual separation from God. Christ conquered death through His resurrection, making death merely a transition for believers: 'to be absent from the body, and to be present with the Lord' (2 Corinthians 5:8)."}
        },

        # Additional Key Terms
        "blood": {
            "ot": {"term": "דָּם", "translit": "Dam", "meaning": "Blood", "note": "The Hebrew <strong>dam</strong> (דָּם) means blood—representing life itself. 'The life of the flesh is in the blood' (Leviticus 17:11), and blood was required for atonement, foreshadowing Christ's sacrifice."},
            "nt": {"term": "αἷμα", "translit": "Haima", "meaning": "Blood", "note": "The Greek <strong>haima</strong> (αἷμα) denotes blood. Christ's blood 'cleanseth us from all sin' (1 John 1:7), securing 'eternal redemption' (Hebrews 9:12) through His once-for-all sacrifice. Believers have been 'purchased with his own blood' (Acts 20:28)."}
        },
        "power": {
            "ot": {"term": "כֹּחַ", "translit": "Koach", "meaning": "Power, strength", "note": "The Hebrew <strong>koach</strong> (כֹּחַ) means power or strength—ability to accomplish. God's power is infinite: 'Hast thou not known? hast thou not heard, that the everlasting God, the LORD, the Creator of the ends of the earth, fainteth not, neither is weary?' (Isaiah 40:28)."},
            "nt": {"term": "δύναμις", "translit": "Dunamis", "meaning": "Power, ability", "note": "The Greek <strong>dunamis</strong> (δύναμις) denotes power or ability—the source of 'dynamite.' The gospel is 'the power of God unto salvation' (Romans 1:16), and believers receive power when the Holy Spirit comes upon them (Acts 1:8)."}
        },
        "name": {
            "ot": {"term": "שֵׁם", "translit": "Shem", "meaning": "Name, reputation", "note": "The Hebrew <strong>shem</strong> (שֵׁם) means name—representing character, authority, and reputation. God's name is holy (Leviticus 20:3), and He promised Abraham 'I will make thy name great' (Genesis 12:2)."},
            "nt": {"term": "ὄνομα", "translit": "Onoma", "meaning": "Name, authority", "note": "The Greek <strong>onoma</strong> (ὄνομα) denotes name or authority. At Jesus' name 'every knee should bow' (Philippians 2:10), and 'there is none other name under heaven given among men, whereby we must be saved' (Acts 4:12)."}
        }
    }

    # First, collect all potential word studies in this verse
    potential_sidenotes = []
    for word, studies in word_studies.items():
        if word in verse_lower:
            # Use appropriate testament
            study = studies.get('ot' if is_ot else 'nt', studies.get('ot') or studies.get('nt'))
            if study:
                potential_sidenotes.append({
                    "word": word.title(),
                    "term": study['term'],
                    "translit": study['translit'],
                    "meaning": study['meaning'],
                    "note": link_bible_references(study['note'])
                })

    # Intelligently select only 1-2 word studies per verse to avoid repetition
    # Use verse position to determine which studies to show
    if not potential_sidenotes:
        return []

    # Deterministic selection based on verse number for consistency
    # Show sidenotes on every other verse (verses 1, 3, 5, 7, etc.)
    # This ensures roughly 50% of verses show studies while being predictable
    if verse_num % 2 == 0:
        return []  # Skip even-numbered verses

    import random
    random.seed(f"{book}{chapter}{verse_num}")

    # Show 1-2 sidenotes max
    # Every 3rd odd verse (1, 7, 13, etc.) gets 2 sidenotes, others get 1
    max_sidenotes = 2 if (verse_num % 6 == 1) else 1

    # Randomly select which word studies to show from those available
    selected = random.sample(potential_sidenotes, min(max_sidenotes, len(potential_sidenotes)))
    return selected


def generate_commentary(book, chapter, verse):
    """Generate AI-powered commentary for a specific verse"""
    # Enhanced commentary database for major chapters
    enhanced_commentary = {
        "Genesis": {
            1: {
                1: {
                    "analysis": """<strong>In the beginning God created the heaven and the earth.</strong> This majestic opening declares the fundamental truth of biblical theology: God is the sovereign Creator of all that exists. The Hebrew word <em>bereshit</em> (בְּרֵאשִׁית) means "in beginning" without the definite article, suggesting not merely a temporal starting point but the absolute origin of all created reality.<br><br>The verb <em>bara</em> (בָּרָא, "created") appears exclusively with God as its subject in Scripture, denoting divine creative activity that brings something entirely new into existence. This distinguishes biblical creation from ancient Near Eastern myths where gods merely reshape pre-existing matter. The phrase "the heaven and the earth" (<em>hashamayim ve'et ha'aretz</em>) is a Hebrew merism expressing the totality of creation—all realms, visible and invisible.<br><br>Theologically, this verse establishes: (1) God's transcendence—He exists before and apart from creation; (2) God's omnipotence—He speaks reality into being; (3) the contingency of creation—all depends on God for existence; and (4) the purposefulness of creation—it originates from divine will, not chance or necessity.""",
                    "historical": """Genesis 1:1 stands in stark contrast to ancient Near Eastern creation accounts like the Babylonian <em>Enuma Elish</em> or the Egyptian creation myths. While these portrayed creation as resulting from conflicts between deities, Genesis presents a sovereign God who creates effortlessly by divine decree. This would have been revolutionary to ancient readers accustomed to polytheistic cosmogonies.<br><br>The Hebrew text's literary structure suggests careful composition rather than primitive mythology. The absence of theogony (origin of gods) and theomachy (conflict between gods) distinguishes Genesis from its contemporary literature. Archaeological discoveries of creation tablets from Mesopotamia (dating to 2000-1500 BCE) reveal that Genesis addresses similar questions but provides radically different answers about the nature of God, humanity, and the cosmos.<br><br>For the Israelites emerging from Egyptian bondage, this truth that their God created everything would have been profoundly liberating—the gods of Egypt were mere creations, not creators.""",
                    "questions": [
                        "How does the doctrine of creation ex nihilo (from nothing) shape our understanding of God's relationship to the universe?",
                        "What are the implications of God creating by His word alone for our understanding of the power of divine speech throughout Scripture?",
                        "How does Genesis 1:1 provide the foundation for a biblical worldview distinct from both ancient mythology and modern materialism?"
                    ]
                },
                26: {
                    "analysis": """<strong>Let us make man in our image, after our likeness.</strong> This pivotal verse introduces humanity's creation with striking theological significance. The plural "Let us" has generated extensive theological discussion. While some see this as a plural of majesty (royal we), the most compelling interpretation recognizes an intra-Trinitarian conversation, especially given New Testament revelation (John 1:1-3, Colossians 1:16).<br><br>The Hebrew words <em>tselem</em> (צֶלֶם, "image") and <em>demuth</em> (דְּמוּת, "likeness") are essentially synonymous, together emphasizing humanity's unique status as God's representatives. This image encompasses: (1) rational and moral capacities, (2) relational nature, (3) creative abilities, (4) dominion over creation, and (5) spiritual dimension. Importantly, the image of God is not something humans possess but something they <em>are</em>.<br><br>The immediate context links the image to dominion—humans are God's vice-regents on earth. This establishes human dignity, purpose, and responsibility. Every human bears this image, making human life sacred and murder heinous (Genesis 9:6). The fall damages but does not eliminate this image (James 3:9).""",
                    "historical": """The concept of humans as divine images was revolutionary in the ancient Near East. While other cultures depicted only kings as divine images, Genesis democratizes this honor—all humans bear God's image regardless of social status. In Egypt, the Pharaoh was considered the living image of the gods, while in Mesopotamia, only kings were called divine images. Genesis radically declares that every human, from the greatest to the least, shares this extraordinary dignity.<br><br>Ancient creation accounts typically portrayed humans as afterthoughts or slaves to the gods. The Babylonian <em>Atrahasis Epic</em> describes humans created to relieve the gods of burdensome labor. By contrast, Genesis presents humans as the crown of creation, specially crafted by God's own hands and breath. This would have been profoundly counter-cultural to ancient readers familiar with their insignificance in other religious systems.""",
                    "questions": [
                        "How does the image of God distinguish humans from animals and what implications does this have for bioethics?",
                        "In what ways does understanding humans as God's image-bearers shape our view of human rights and social justice?",
                        "How should the doctrine of imago Dei influence our approach to race relations, disability, and the value of human life at all stages?"
                    ]
                }
            }
        },
        "John": {
            3: {
                16: {
                    "analysis": """<strong>For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.</strong> This verse, often called the "Gospel in miniature," encapsulates the entire biblical narrative of redemption. The Greek construction emphasizes the manner and extent of God's love: <em>houtōs</em> (οὕτως, "so" or "in this way") points not merely to degree but to the specific manner—through sacrificial giving.<br><br>The phrase "only begotten" (<em>monogenēs</em>, μονογενής) literally means "one of a kind" or "unique," emphasizing Christ's distinctive relationship to the Father rather than necessarily temporal generation. This word appears five times in John's writings (John 1:14, 18; 3:16, 18; 1 John 4:9), always highlighting Christ's unique divine sonship.<br><br>"The world" (<em>kosmos</em>, κόσμος) in John's Gospel typically refers to fallen humanity in rebellion against God (John 1:10; 15:18-19). That God loves <em>this</em> world—hostile, rebellious, and alienated—demonstrates the radical nature of divine grace. The purpose clause reveals God's desire: not condemnation but salvation, not death but eternal life.""",
                    "historical": """Jesus spoke these words to Nicodemus, a Pharisee and member of the Sanhedrin, during a nighttime conversation that reveals the tension surrounding Jesus' ministry. Nicodemus represented the religious elite who struggled to understand Jesus' revolutionary teachings about spiritual rebirth and salvation.<br><br>The context of Jesus' statement connects to the bronze serpent incident (Numbers 21:4-9), which Jesus had just referenced. In the wilderness, when venomous serpents bit the Israelites, God commanded Moses to make a bronze serpent and lift it up on a pole. Anyone who looked upon it would live. This historical parallel illustrates how Christ, lifted up on the cross, becomes the means of salvation for all who look to Him in faith.<br><br>For first-century Jews, the concept of God's love extending to "the world" (including Gentiles) was revolutionary. Jewish thought generally emphasized God's special love for Israel, making this universal scope of divine love a radical departure that would later become central to Paul's Gentile mission.""",
                    "questions": [
                        "How does the phrase 'God so loved the world' challenge both ancient Jewish particularism and modern religious exclusivism?",
                        "What does it mean that God 'gave' His Son, and how does this relate to theories of atonement and sacrifice?",
                        "How should we understand 'eternal life' not just as quantity but quality of existence, beginning now rather than only in the future?"
                    ]
                }
            }
        },
        "Romans": {
            8: {
                28: {
                    "analysis": """<strong>And we know that all things work together for good to them that love God, to them who are the called according to his purpose.</strong> This beloved verse provides profound comfort while requiring careful theological understanding. The verb "work together" (<em>synergei</em>, συνεργεῖ) suggests a divine orchestration where even disparate events collaborate toward God's ultimate purpose.<br><br>The phrase "all things" (πάντα) is comprehensive yet must be understood within context. Paul doesn't claim all things are inherently good, but that God sovereignly works through all circumstances—including suffering, persecution, and even human sin—to accomplish His redemptive purposes for His people. The "good" (<em>agathon</em>, ἀγαθόν) here refers to conformity to Christ's image (v.29), not necessarily temporal comfort or prosperity.<br><br>The verse contains two crucial qualifications: (1) "to them that love God"—demonstrating genuine saving faith, and (2) "the called according to his purpose"—referring to God's eternal elective purpose. These aren't two different groups but describe the same people from human (love) and divine (calling) perspectives.""",
                    "historical": """Romans 8:28 appears within Paul's exposition of Christian suffering and hope. The Roman church, composed of both Jewish and Gentile believers, faced mounting persecution under Nero's increasingly hostile policies toward Christians. Paul wrote Romans around 57 CE, just a few years before Nero's great persecution that would claim many Christian lives.<br><br>The broader context of Romans 8 addresses the tension between present suffering and future glory (vv. 18-30). Early Christians needed assurance that their current tribulations served God's redemptive purposes rather than indicating divine abandonment. This verse would have provided crucial comfort to believers facing social ostracism, economic hardship, and physical persecution for their faith.""",
                    "questions": [
                        "How do we reconcile God's sovereignty in 'working all things together for good' with human responsibility and the reality of evil?",
                        "What practical difference should this verse make in how Christians respond to suffering, disappointment, and apparent setbacks?",
                        "How does understanding our identity as 'called according to his purpose' provide security and hope in uncertain circumstances?"
                    ]
                }
            }
        },
        "Psalms": {
            23: {
                1: {
                    "analysis": """<strong>The Lord is my shepherd; I shall not want.</strong> This opening declaration establishes both the fundamental relationship (Lord as shepherd, believer as sheep) and its primary consequence (complete sufficiency). The Hebrew word for "Lord" here is <em>Yahweh</em> (יהוה), the covenant name of God, emphasizing not just divine power but divine faithfulness to His promises.<br><br>The metaphor of God as shepherd was deeply rooted in Hebrew thought and ancient Near Eastern royal ideology. Kings were often called shepherds of their people (Ezekiel 34:1-10). David, himself a shepherd before becoming king, understood both the tender care and protective authority required. The verb "shepherd" (<em>ra'ah</em>, רעה) implies not passive watching but active guidance, protection, and provision.<br><br>The phrase "I shall not want" (<em>lo echsar</em>, לא אחסר) uses a strong Hebrew negative, meaning "I shall certainly not lack." This isn't a promise of luxury but of sufficiency—every true need will be met. The psalmist's confidence rests not in circumstances but in the character and commitment of his divine Shepherd.""",
                    "historical": """Psalm 23 likely originates from David's experience as both shepherd and king. Archaeological evidence reveals that shepherding in ancient Palestine required constant vigilance against predators (lions, bears, wolves) and environmental dangers (cliffs, sudden storms, poisonous plants). Shepherds risked their lives for their flocks, often sleeping in caves or under stars to guard against night attacks.<br><br>The psalm's imagery would have resonated powerfully with David's original audience, many of whom lived in pastoral settings. The metaphor also connected to Israel's understanding of God's relationship with the nation—He had shepherded them out of Egypt, through the wilderness, and into the Promised Land. Royal psalms often used shepherd imagery to describe ideal kingship (Psalm 78:70-72).<br><br>For exiled or oppressed Israelites in later periods, this psalm provided comfort by affirming God's continued care despite apparent abandonment. The shepherd metaphor assured them that their divine King remained attentive to their needs even in foreign lands.""",
                    "questions": [
                        "How does understanding God as our shepherd change our perspective on guidance, protection, and provision in daily life?",
                        "What does it mean practically to 'not want' when we clearly experience desires and needs that seem unmet?",
                        "How does the personal, intimate nature of this psalm ('my shepherd') balance with understanding God's universal sovereignty?"
                    ]
                }
            }
        },
        "1 Corinthians": {
            13: {
                4: {
                    "analysis": """<strong>Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up.</strong> Paul begins his poetic description of love with two positive qualities followed by four negative ones. The Greek word <em>agape</em> (ἀγάπη), translated "charity" in the KJV, represents divine love characterized by self-sacrificial commitment rather than emotional feeling or romantic attraction.<br><br>"Suffereth long" (<em>makrothymei</em>, μακροθυμεῖ) literally means "long-tempered" or "slow to anger," describing patience with people rather than circumstances. This patience isn't passive endurance but active forbearance that continues loving despite provocation. "Is kind" (<em>chresteuetai</em>, χρηστεύεται) appears only here in the New Testament, emphasizing active benevolence that seeks others' welfare.<br><br>The four negatives reveal what love never does: it doesn't envy (<em>ou zeloi</em>), doesn't boast (<em>ou perpereuetai</em>), doesn't act arrogantly (<em>ou physioutai</em>), and doesn't behave inappropriately. These contrasts address specific problems Paul observed in Corinth: jealousy over spiritual gifts, boasting about wisdom or status, and prideful behavior that disrupted fellowship.""",
                    "historical": """The Corinthian church was deeply divided by issues of status, spiritual gifts, and personal preferences. Wealthy members looked down on poorer believers, different factions claimed superiority based on their favorite teachers (Paul, Apollos, Cephas), and some boasted about having more impressive spiritual gifts like tongues or prophecy.<br><br>First-century Corinth was a cosmopolitan commercial center where social status, rhetorical skill, and impressive displays of wisdom or power determined social standing. The Roman patronage system created obvious hierarchies, and Greek philosophical schools competed for intellectual supremacy. Into this context, Paul introduces a radically different value system based on self-sacrificial love rather than self-promotion.<br><br>Paul's description of love directly challenges Corinthian culture: instead of self-assertion, love seeks others' good; instead of competing for honor, love rejoices in others' success; instead of demanding rights, love willingly suffers inconvenience for others' benefit.""",
                    "questions": [
                        "How does Paul's definition of love challenge modern cultural understandings of love as primarily emotional or romantic?",
                        "Which of these characteristics of love do you find most challenging to practice consistently, and why?",
                        "How might the church today address conflicts and divisions by applying these principles of love?"
                    ]
                }
            }
        },
        "Matthew": {
            5: {
                3: {
                    "analysis": """<strong>Blessed are the poor in spirit: for theirs is the kingdom of heaven.</strong> This opening beatitude establishes the fundamental character of kingdom citizens. The Greek <em>makarios</em> (μακάριος, "blessed") denotes not temporary happiness but objective divine favor and ultimate well-being. The "poor in spirit" (<em>ptōchoi tō pneumati</em>, πτωχοὶ τῷ πνεύματι) describes those who recognize their spiritual bankruptcy before God.<br><br>The word <em>ptōchoi</em> refers to abject poverty—those who must beg to survive. Spiritually, it describes complete dependence on God's mercy rather than self-righteousness or merit. This poverty of spirit stands opposite to Pharisaic pride and self-sufficiency. The present tense "theirs is" indicates immediate possession of the kingdom, not just future hope.<br><br>Jesus radically reverses worldly values: those the world considers unsuccessful (the spiritually poor) are declared blessed by God. This beatitude forms the foundation for all others, as spiritual poverty is the prerequisite for receiving God's grace.""",
                    "historical": """The Sermon on the Mount was delivered to Jesus' disciples with crowds listening (Matthew 5:1-2). In first-century Palestine, poverty was widespread, and religious leaders often taught that prosperity indicated divine blessing while poverty suggested divine disfavor. The Pharisees emphasized righteous works and religious achievement as means of gaining God's approval.<br><br>Jesus' audience would have included many literally poor people who struggled under Roman taxation and religious obligations. The concept of being "poor in spirit" would have resonated with those who felt spiritually inadequate compared to the religious elite. This teaching directly challenged the prevailing theology that equated material and spiritual prosperity with divine favor.<br><br>The beatitudes as a whole present kingdom ethics that contrast sharply with both Roman imperial values (strength, conquest, honor) and Jewish religious expectations (law-keeping, prosperity, national restoration).""",
                    "questions": [
                        "How does recognizing our spiritual poverty before God change our approach to righteousness and religious achievement?",
                        "What practical steps can believers take to maintain a 'poor in spirit' attitude in a culture that promotes self-sufficiency?",
                        "How does this beatitude challenge both religious pride and secular humanism's emphasis on human potential?"
                    ]
                },
                8: {
                    "analysis": """<strong>Blessed are the pure in heart: for they shall see God.</strong> This beatitude addresses the inner nature that God requires for relationship with Him. The Greek <em>katharos</em> (καθαρός, "pure") originally meant clean from dirt or unmixed, like pure metals without alloy. Applied to the heart (<em>kardia</em>, καρδία), it describes undivided loyalty and moral integrity—a heart free from duplicity, hypocrisy, and mixed motives.<br><br>Purity of heart encompasses both moral cleanness and single-minded devotion to God. It's not sinless perfection but sincere, undivided commitment without hidden agendas or secret sins. The "heart" in Hebrew thought represents the center of personality—intellect, emotions, and will united in purpose.<br><br>The promise "they shall see God" (<em>theon opsontai</em>, θεὸν ὄψονται) refers to both present spiritual vision and future beatific vision. Only the pure in heart can truly perceive God's nature and works. Sin creates spiritual cataracts that prevent clear vision of divine truth and beauty.""",
                    "historical": """Jewish purity laws emphasized external ceremonial cleanness through ritual washings, dietary restrictions, and avoidance of ceremonial defilement. The Pharisees had developed elaborate systems for maintaining ritual purity while often neglecting inner spiritual condition. Jesus consistently emphasized that external religious observance without internal transformation was insufficient.<br><br>The concept of "seeing God" was particularly significant to first-century Jews who believed that no one could see God and live (Exodus 33:20). Yet the Old Testament promised that the pure would see God (Psalm 24:3-4), creating tension between divine transcendence and the possibility of intimate knowledge of God.<br><br>This beatitude would have shocked Jesus' audience by suggesting that moral and spiritual purity, rather than ritual observance, determines one's ability to perceive and commune with God.""",
                    "questions": [
                        "How does Jesus' emphasis on purity of heart challenge both legalistic religion and antinomian attitudes toward holiness?",
                        "What are the barriers to purity of heart in contemporary culture, and how can believers cultivate undivided devotion to God?",
                        "How does the promise of 'seeing God' provide motivation for pursuing holiness and moral integrity?"
                    ]
                }
            },
            6: {
                9: {
                    "analysis": """<strong>Our Father which art in heaven, Hallowed be thy name.</strong> This opening address establishes the fundamental relationship and priority in prayer. "Our Father" (<em>Pater hēmōn</em>, Πάτερ ἡμῶν) was revolutionary in its intimacy—while Jews acknowledged God as Father of the nation, Jesus taught individual believers to approach God with filial confidence. The Aramaic <em>Abba</em> behind this Greek reflects intimate family relationship.<br><br>"Which art in heaven" (<em>ho en tois ouranois</em>, ὁ ἐν τοῖς οὐρανοῖς) balances intimacy with reverence, acknowledging God's transcendence and sovereign authority. This phrase prevents presumptuous familiarity while maintaining relational warmth.<br><br>"Hallowed be thy name" (<em>hagiasthētō to onoma sou</em>, ἁγιασθήτω τὸ ὄνομά σου) uses the passive voice, recognizing that ultimately God hallows His own name through His actions. The aorist imperative suggests both an ongoing desire and an eschatological hope for universal recognition of God's holiness.""",
                    "historical": """Jewish prayer in the first century typically began with elaborate titles acknowledging God's transcendence and holiness. The most common address was "Blessed art Thou, O Lord our God, King of the universe." Jesus' use of "Father" would have been startling in its simplicity and intimacy, though some Jewish prayers did refer to God as Father of Israel.<br><br>The Kaddish prayer, central to Jewish liturgy, included the petition "May His great name be sanctified and hallowed," showing that the concept of hallowing God's name was familiar to Jewish worshipers. However, Jesus places this petition in the context of individual, intimate prayer rather than formal liturgy.<br><br>The family structure in ancient Mediterranean culture made the father the source of honor, provision, and protection for the household. Jesus' teaching that believers could approach the sovereign God as "Father" implied both tremendous privilege and serious responsibility.""",
                    "questions": [
                        "How does understanding God as 'our Father' change the way we approach prayer, worship, and obedience?",
                        "What does it mean practically to 'hallow' God's name in contemporary culture, and how do our lives contribute to this?",
                        "How does the balance between intimacy ('Father') and reverence ('in heaven') inform healthy Christian spirituality?"
                    ]
                },
                11: {
                    "analysis": """<strong>Give us this day our daily bread.</strong> This petition addresses humanity's fundamental dependence on God for sustenance. The Greek <em>artos</em> (ἄρτος, "bread") represents basic nourishment, standing for all necessities of life. The qualifier <em>epiousios</em> (ἐπιούσιος, "daily") is rare in ancient literature, possibly meaning "sufficient for today," "for the coming day," or "necessary for existence."<br><br>This request acknowledges human dependence while modeling contentment with basic provisions rather than luxury or excess. The petition follows immediately after seeking God's kingdom and righteousness, suggesting that material needs, while legitimate, are secondary to spiritual priorities.<br><br>The present imperative "give" (<em>dos</em>, δός) indicates ongoing dependence rather than one-time provision. The plural "us" emphasizes communal concern—followers of Jesus pray not just for personal needs but for the community's welfare.""",
                    "historical": """In ancient Palestine, daily bread was literally a daily concern for most people. Laborers were typically paid at the end of each workday (Leviticus 19:13), and families often lived from day to day without significant food storage. Bread was the staple food, representing up to 70% of caloric intake for ordinary people.<br><br>The wilderness wandering provided the theological background for this petition, where Israel learned to depend on God for daily manna (Exodus 16). They could not hoard manna—it spoiled if kept overnight (except on the Sabbath), teaching complete dependence on God's daily provision.<br><br>Jewish blessings over bread acknowledged God as the source of provision: "Blessed art Thou, O Lord our God, King of the universe, who bringest forth bread from the earth." Jesus' prayer reflects this understanding while emphasizing ongoing dependence rather than accumulated wealth.""",
                    "questions": [
                        "How does praying for 'daily bread' challenge consumer culture's emphasis on accumulation and security through material wealth?",
                        "What does it mean to depend on God for daily provision in developed economies where food security seems guaranteed?",
                        "How should the plural 'us' in this petition influence Christian attitudes toward global hunger and economic inequality?"
                    ]
                }
            },
            28: {
                19: {
                    "analysis": """<strong>Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost.</strong> The Great Commission establishes the church's universal mission. "Go ye therefore" (<em>poreuthentes oun</em>, πορευθέντες οὖν) connects this command to Jesus' declaration of universal authority (v.18). The participle suggests "as you go" or "going," indicating that evangelism occurs through normal life activities, not just formal missions.<br><br>"Teach all nations" more literally reads "make disciples of all nations" (<em>mathēteusate panta ta ethnē</em>, μαθητεύσατε πάντα τὰ ἔθνη). The term <em>ethnē</em> refers to people groups, not just political entities. This universality breaks down Jewish-Gentile barriers and extends salvation to every cultural and ethnic group.<br><br>The Trinitarian baptismal formula "in the name of the Father, and of the Son, and of the Holy Ghost" uses the singular "name" (<em>onoma</em>, ὄνομα), suggesting the unity of the three persons in one divine essence. This represents the clearest Trinitarian statement in the Gospels.""",
                    "historical": """This commission was given to the eleven disciples on a mountain in Galilee (Matthew 28:16), fulfilling Jesus' promise to meet them there (26:32, 28:10). The mountain setting echoes other significant biblical revelations and commissions, particularly Moses receiving the law on Mount Sinai.<br><br>At this time, Jewish understanding generally limited God's full salvation to Israel, though they acknowledged righteous Gentiles could be saved. Jesus' command to make disciples of "all nations" would have been revolutionary, expanding the scope of salvation beyond ethnic and religious boundaries that had defined Jewish identity for centuries.<br><br>The early church initially struggled with this universal mandate, as seen in Peter's vision (Acts 10) and the Jerusalem Council (Acts 15). The inclusion of Gentiles without requiring circumcision and law-keeping represented a fundamental shift in understanding God's redemptive purposes.""",
                    "questions": [
                        "How does the Great Commission challenge both religious exclusivism and cultural relativism in contemporary missions?",
                        "What does 'making disciples' involve beyond initial evangelism, and how should this shape church ministry strategies?",
                        "How does the Trinitarian baptismal formula inform our understanding of conversion as incorporation into the divine community?"
                    ]
                }
            }
        },
        "Luke": {
            2: {
                14: {
                    "analysis": """<strong>Glory to God in the highest, and on earth peace, good will toward men.</strong> The angelic proclamation announces the cosmic significance of Christ's birth. "Glory to God in the highest" (<em>doxa en hypsistois theō</em>, δόξα ἐν ὑψίστοις θεῷ) declares that Christ's incarnation supremely manifests God's glory—His character, power, and purposes. The superlative "highest" emphasizes the ultimate nature of this glorification.<br><br>"Peace on earth" (<em>epi gēs eirēnē</em>, ἐπὶ γῆς εἰρήνη) refers to the comprehensive well-being that Messiah brings—not mere absence of conflict but wholeness, harmony, and reconciliation between God and humanity. This peace fulfills prophetic promises of the Prince of Peace (Isaiah 9:6) who would establish everlasting peace.<br><br>"Good will toward men" (<em>en anthrōpois eudokia</em>, ἐν ἀνθρώποις εὐδοκία) better translates as "among people with whom [God] is pleased" or "people of [God's] good pleasure." This emphasizes divine initiative in salvation rather than general human goodwill.""",
                    "historical": """The angelic announcement came to shepherds keeping watch over their flocks by night, likely during lambing season when shepherds maintained constant vigilance. Shepherds were generally despised in first-century Jewish society, considered ceremonially unclean due to their work and unable to maintain ritual purity. Yet God chose them as the first recipients of the Messiah's birth announcement.<br><br>The proclamation echoes imperial Roman announcements of the emperor's birth or victories, which were called "gospel" (<em>euangelion</em>) and promised peace throughout the empire. The angels' message presents Jesus as the true king whose birth brings authentic peace, contrasting with Pax Romana maintained through military force.<br><br>Bethlehem's significance as David's birthplace would have been profound for Jewish hearers, as Messianic expectations focused on the Davidic covenant and promises of an eternal kingdom. The humble circumstances of Jesus' birth would have seemed paradoxical given royal expectations.""",
                    "questions": [
                        "How does God's choice to announce the Messiah's birth to shepherds challenge human concepts of status and importance?",
                        "What is the relationship between the 'glory to God' and 'peace on earth' announced by the angels, and how are these connected through Christ?",
                        "How does the biblical concept of peace differ from contemporary secular understandings of peace and conflict resolution?"
                    ]
                }
            },
            15: {
                11: {
                    "analysis": """<strong>A certain man had two sons.</strong> This simple opening to the parable of the prodigal son establishes the family context that drives the entire narrative. The "certain man" represents God the Father, whose character is revealed through his treatment of both sons. The "two sons" represent two fundamentally different approaches to relationship with God—one openly rebellious, the other outwardly compliant but inwardly resentful.<br><br>The parable structure follows the classic pattern of Jesus' teaching stories: a realistic scenario that suddenly takes an unexpected turn, challenging conventional wisdom and revealing kingdom values. The father's response to both sons defies cultural expectations and reveals the radical nature of divine grace.<br><br>This introduction sets up the central tension of the parable: how divine love responds to both flagrant sin and self-righteous legalism. Both sons are alienated from the father despite their different behaviors, suggesting that external conformity without heart transformation is as problematic as open rebellion.""",
                    "historical": """The parable was told in response to Pharisees and scribes criticizing Jesus for eating with tax collectors and sinners (Luke 15:1-2). In first-century Jewish culture, table fellowship implied acceptance and approval, making Jesus' behavior scandalous to religious leaders who maintained strict separation from the ceremonially unclean.<br><br>The family dynamics described would have been familiar to Jesus' audience. Younger sons typically received one-third of the inheritance, while the eldest received a double portion. Requesting inheritance while the father lived was culturally unthinkable—equivalent to wishing the father dead. The father's granting this request would have shocked listeners.<br><br>The parable addresses the fundamental Jewish struggle with Gentile inclusion in God's kingdom. The religious leaders (represented by the elder son) resented God's acceptance of sinners without requiring full proselyte conversion and law observance.""",
                    "questions": [
                        "How do both sons in the parable represent different forms of alienation from the father, and what does this teach about human relationship with God?",
                        "What does the father's character in this parable reveal about God's nature that challenges both legalistic and antinomian approaches to faith?",
                        "How should this parable shape Christian attitudes toward both open sinners and self-righteous religious people?"
                    ]
                }
            }
        },
        "Ephesians": {
            2: {
                8: {
                    "analysis": """<strong>For by grace are ye saved through faith; and that not of yourselves: it is the gift of God.</strong> This verse provides the theological foundation of Protestant soteriology. "By grace" (<em>tē chariti</em>, τῇ χάριτι) emphasizes the instrumental cause of salvation—God's unmerited favor is the means by which salvation occurs. Grace is not merely divine attitude but active divine power working salvation.<br><br>"Through faith" (<em>dia pisteōs</em>, διὰ πίστεως) identifies faith as the channel through which grace is received. Faith is not a work that earns salvation but the empty hand that receives God's gift. The prepositions distinguish grace as the efficient cause and faith as the instrumental cause of salvation.<br><br>"Not of yourselves" (<em>ouk ex hymōn</em>, οὐκ ἐξ ὑμῶν) explicitly denies human contribution to salvation. The pronoun "that" (<em>touto</em>, τοῦτο) likely refers to the entire salvation process, not just faith, emphasizing that salvation in its entirety—including the faith to receive it—originates from God.""",
                    "historical": """Paul wrote Ephesians during his Roman imprisonment (c. 60-62 CE) to address Gentile Christians who had been brought into the covenant community alongside Jewish believers. The letter addresses the theological implications of Jew-Gentile unity in the church and the foundation of this new community in God's grace rather than ethnic identity or law-keeping.<br><br>The emphasis on salvation by grace alone would have been particularly significant for Gentile converts who might have felt pressure to adopt Jewish customs or might have wondered about their standing before God without adherence to the Mosaic law. This passage provides assurance that their salvation rests on divine grace alone.<br><br>The concept of grace as divine gift contrasts with Greco-Roman reciprocal gift-giving, where gifts created obligations and expectations of return. Paul emphasizes that God's grace creates no obligation because it cannot be repaid—it is pure gift motivated by divine love.""",
                    "questions": [
                        "How does understanding salvation as entirely God's gift affect human pride and the tendency toward spiritual self-righteousness?",
                        "What is the relationship between faith and works if salvation is by grace alone, and how does this understanding shape Christian living?",
                        "How should the doctrine of salvation by grace alone influence evangelism and the church's approach to social action?"
                    ]
                }
            },
            6: {
                10: {
                    "analysis": """<strong>Finally, my brethren, be strong in the Lord, and in the power of his might.</strong> This verse introduces Paul's teaching on spiritual warfare with an emphasis on divine empowerment. "Be strong" (<em>endunamousthe</em>, ἐνδυναμοῦσθε) is a present passive imperative, indicating ongoing empowerment that comes from God rather than human effort. The passive voice emphasizes that strength comes from outside ourselves.<br><br>"In the Lord" (<em>en kyriō</em>, ἐν κυρίῳ) identifies the sphere and source of strength—union with Christ provides access to divine power. This prepositional phrase indicates not just help from God but participation in divine life and power through spiritual union.<br><br>"The power of his might" (<em>tō kratei tēs ischyos autou</em>, τῷ κράτει τῆς ἰσχύος αὐτοῦ) uses two Greek words for power, emphasizing the overwhelming nature of God's strength. <em>Kratos</em> refers to dominion and rule, while <em>ischys</em> refers to inherent strength and ability.""",
                    "historical": """Paul writes from Roman imprisonment, where he would have observed the military equipment and discipline of Roman soldiers daily. His use of military metaphors draws from this immediate context to describe spiritual realities. Roman soldiers were renowned for their discipline, training, and equipment that made them nearly invincible in battle.<br><br>The Ephesian Christians lived in a city dominated by magical practices, occult arts, and pagan spirituality. Acts 19 describes how many converted Christians burned their magic books publicly. In this context, Paul's teaching about spiritual warfare would have been particularly relevant as new believers faced real spiritual opposition.<br><br>The emphasis on divine strength rather than human ability would have resonated with converts from both Jewish and pagan backgrounds, who might have been tempted to rely on their own religious practices, moral efforts, or spiritual techniques rather than on God's power.""",
                    "questions": [
                        "How does understanding spiritual strength as coming 'in the Lord' change approaches to Christian discipline and spiritual growth?",
                        "What are the practical implications of relying on 'the power of his might' rather than human willpower in spiritual battles?",
                        "How should awareness of spiritual warfare influence daily Christian living and decision-making?"
                    ]
                }
            }
        },
        "Philippians": {
            4: {
                13: {
                    "analysis": """<strong>I can do all things through Christ which strengtheneth me.</strong> This beloved verse is often misunderstood when separated from its context of contentment in various circumstances. "I can do all things" (<em>panta ischyō</em>, πάντα ἰσχύω) refers specifically to Paul's ability to be content in any situation—abundance or need, plenty or hunger. The "all things" refers to all circumstances, not all tasks or ambitions.<br><br>"Through Christ" (<em>en tō endunamounti me</em>, ἐν τῷ ἐνδυναμοῦντι με) literally reads "in the one strengthening me." The present participle indicates ongoing, continuous empowerment. Christ doesn't merely help Paul but provides the very strength and ability to respond appropriately to life's varied circumstances.<br><br>The context emphasizes supernatural contentment that transcends natural human responses to hardship or prosperity. This strength enables believers to maintain spiritual equilibrium regardless of external conditions, finding sufficiency in Christ rather than circumstances.""",
                    "historical": """Paul wrote Philippians from Roman imprisonment, likely the house arrest described in Acts 28. Despite uncertain prospects and physical limitations, Paul demonstrates the contentment he describes. The Philippian church had sent financial support through Epaphroditus, prompting Paul's discussion of contentment and gratitude.<br><br>Ancient Stoic philosophy emphasized contentment and emotional equilibrium, but achieved through human reason and willpower. Paul presents a fundamentally different approach—contentment through divine empowerment rather than philosophical detachment. This would have been a striking contrast for readers familiar with Stoic teaching.<br><br>The historical context of imprisonment, where Paul lacked control over his circumstances, provides the perfect backdrop for demonstrating that true strength and contentment come from spiritual resources rather than favorable external conditions.""",
                    "questions": [
                        "How does understanding this verse in the context of contentment change its application from achieving goals to accepting circumstances?",
                        "What is the difference between Stoic self-sufficiency and Christian contentment through Christ's strength?",
                        "How can believers cultivate the kind of contentment Paul describes while still pursuing legitimate goals and improvements?"
                    ]
                }
            }
        },
        "Hebrews": {
            11: {
                1: {
                    "analysis": """<strong>Now faith is the substance of things hoped for, the evidence of things not seen.</strong> This verse provides the classic biblical definition of faith, describing both its nature and function. "Substance" (<em>hypostasis</em>, ὑπόστασις) literally means "that which stands under" or foundation, indicating that faith provides objective reality to hoped-for things, not merely subjective confidence. Faith gives substance to future promises, making them present realities in the believer's experience.<br><br>"Evidence" (<em>elegchos</em>, ἔλεγχος) refers to proof or conviction that establishes truth. Faith provides convincing evidence of invisible spiritual realities, functioning like a divine radar that detects what natural senses cannot perceive. This evidence is not emotional feeling but objective spiritual perception.<br><br>The verse establishes faith as the bridge between visible and invisible realms, enabling believers to live based on divine promises rather than immediate circumstances. Faith makes the future present and the invisible visible, providing the foundation for the life of obedience described in the following examples.""",
                    "historical": """Hebrews was written to Jewish Christians facing persecution and temptation to return to Judaism. The recipients were wavering in their commitment to Christ, discouraged by suffering and the apparent delay of promised blessings. In this context, the definition of faith addresses their need for perseverance based on unseen realities.<br><br>The concept of faith as "substance" would have resonated with readers familiar with both Greek philosophical concepts and Hebrew understanding of God's covenant faithfulness. The author uses sophisticated Greek terminology to explain Hebrew concepts of trust and faithfulness to God.<br><br>Chapter 11 follows this definition with examples from Jewish history, demonstrating that faith has always been the operating principle for God's people. These examples would have encouraged wavering Jewish Christians by showing that their ancestors also lived by faith in God's promises rather than visible fulfillment.""",
                    "questions": [
                        "How does faith as 'substance' and 'evidence' differ from mere wishful thinking or blind belief?",
                        "What role should faith play in decision-making when circumstances seem to contradict God's promises?",
                        "How can believers develop the kind of faith that makes unseen realities more real than visible circumstances?"
                    ]
                }
            },
            12: {
                1: {
                    "analysis": """<strong>Wherefore seeing we also are compassed about with so great a cloud of witnesses, let us lay aside every weight, and the sin which doth so easily beset us, and let us run with patience the race that is set before us.</strong> This verse applies the examples of faith from chapter 11 to encourage perseverance. The "cloud of witnesses" (<em>nephos martyrōn</em>, νέφος μαρτύρων) refers to the heroes of faith who provide testimony to God's faithfulness, not spectators watching our performance. Their lives bear witness to the reliability of faith.<br><br>"Lay aside every weight" (<em>apothemenoi ogan</em>, ἀποθέμενοι ὄγκον) uses athletic imagery of runners removing unnecessary clothing and weights. "Weight" refers to anything that hinders spiritual progress—not necessarily sin but anything that slows spiritual advancement. The definite article before "sin" (<em>tēn hamartian</em>, τὴν ἁμαρτίαν) may refer to a specific besetting sin or the principle of sin itself.<br><br>"Run with patience" (<em>di' hypomonēs trechōmen</em>, δι' ὑπομονῆς τρέχωμεν) combines active effort with patient endurance. The Christian life requires both sustained effort and patient persistence, like a long-distance race rather than a sprint.""",
                    "historical": """The athletic imagery would have been familiar to first-century readers who knew Greek Olympic games and local athletic competitions. Athletes trained rigorously, maintained strict diets, and competed naked to avoid any hindrance. This imagery emphasized the dedication and focus required for Christian living.<br><br>The original recipients faced mounting persecution and social pressure to abandon their Christian faith. Some were wavering, discouraged by suffering and the apparent delay of Christ's return. The author uses the metaphor of a race to encourage persistence despite difficulties.""",
                    "questions": [
                        "How do the 'witnesses' from Hebrews 11 provide encouragement for contemporary believers facing spiritual challenges?",
                        "What specific 'weights' and 'sins' might hinder spiritual progress in modern Christian living?",
                        "How does understanding the Christian life as a long-distance race change approaches to spiritual discipline and perseverance?"
                    ]
                }
            }
        },
        "Isaiah": {
            53: {
                5: {
                    "analysis": """<strong>But he was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed.</strong> This verse stands at the heart of the Suffering Servant song, providing the clearest Old Testament prophecy of substitutionary atonement. The four Hebrew verbs describe the Servant's suffering: "wounded" (<em>mecholal</em>, מְחֹלָל) from piercing, "bruised" (<em>medukka</em>, מְדֻכָּא) from crushing, bearing "chastisement" (<em>musar</em>, מוּסָר), and providing healing through "stripes" (<em>chaburah</em>, חַבּוּרָה).<br><br>The preposition "for" (<em>min</em>, מִן) indicates substitution—the Servant suffers in place of others. "Our transgressions" and "our iniquities" emphasize that the suffering is vicarious, not for the Servant's own sins. The parallel structure reinforces that the Servant's suffering directly addresses human sin and its consequences.<br><br>"The chastisement of our peace" indicates that the punishment necessary for reconciliation fell upon the Servant rather than the guilty parties. The word "peace" (<em>shalom</em>, שָׁלוֹם) encompasses complete well-being and restoration of relationship with God.""",
                    "historical": """Isaiah prophesied during the 8th century BCE, addressing Judah's spiritual crisis and the threat of Assyrian invasion. The Suffering Servant songs (Isaiah 42, 49, 50, 52-53) present a figure who would accomplish what Israel failed to do—be a light to the nations and bring salvation to the ends of the earth.<br><br>Ancient Near Eastern cultures understood vicarious suffering and substitutionary rituals, but typically involved animals or slaves substituting for the guilty. The concept of a righteous individual voluntarily suffering for others' sins was unprecedented in scope and significance.<br><br>Jewish interpretation historically applied this passage to the nation of Israel or to righteous individuals within Israel. However, the New Testament writers consistently identified Jesus as the fulfillment of this prophecy, seeing in His crucifixion the precise fulfillment of Isaiah's description.""",
                    "questions": [
                        "How does Isaiah 53:5 explain the mechanism by which Christ's suffering accomplishes human salvation?",
                        "What does the emphasis on 'our' transgressions and iniquities reveal about human responsibility and divine grace?",
                        "How should understanding Christ as the Suffering Servant shape Christian responses to persecution and suffering?"
                    ]
                }
            }
        },
        "Jeremiah": {
            29: {
                11: {
                    "analysis": """<strong>For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end.</strong> This beloved promise reveals God's benevolent intentions toward His people during their darkest hour. "I know" (<em>yadati</em>, יָדַעְתִּי) indicates intimate, personal knowledge—God is fully aware of His plans and their ultimate purpose. The Hebrew word for "thoughts" (<em>machashavot</em>, מַחֲשָׁבוֹת) can mean plans, intentions, or purposes, emphasizing divine deliberation and planning.<br><br>"Thoughts of peace" (<em>machshevot shalom</em>, מַחְשְׁבוֹת שָׁלוֹם) uses <em>shalom</em> in its fullest sense—not mere absence of conflict but comprehensive well-being, prosperity, and harmonious relationship with God. This directly contrasts with the "evil" (<em>ra'ah</em>, רָעָה) or calamity that the people were experiencing in exile.<br><br>"An expected end" (<em>acharit vetikvah</em>, אַחֲרִית וְתִקְוָה) literally means "a future and a hope." This phrase promises both temporal restoration and ultimate eschatological fulfillment, giving hope beyond immediate circumstances.""",
                    "historical": """Jeremiah spoke these words to the Jewish exiles in Babylon around 597-586 BCE, during one of the darkest periods in Jewish history. The temple had been destroyed, Jerusalem lay in ruins, and the covenant people found themselves in pagan lands, wondering if God had abandoned His promises.<br><br>False prophets in Babylon were promising immediate return and quick restoration, creating false hope and preventing the exiles from settling and building productive lives. Jeremiah's message required them to accept their situation while trusting God's long-term purposes—a difficult but necessary perspective.<br><br>The 70-year exile period mentioned in the broader context (v.10) corresponded to the sabbath years Israel had failed to observe (2 Chronicles 36:21), showing that even judgment served God's righteous purposes and would ultimately lead to restoration.""",
                    "questions": [
                        "How should believers understand God's 'plans for peace' when experiencing difficult circumstances or apparent setbacks?",
                        "What is the relationship between trusting God's ultimate purposes and taking practical action in challenging situations?",
                        "How does this promise apply to individual believers versus the corporate people of God, and what are the implications for personal application?"
                    ]
                }
            }
        },
        "Proverbs": {
            3: {
                5: {
                    "analysis": """<strong>Trust in the Lord with all thine heart; and lean not unto thine own understanding.</strong> This foundational proverb establishes the proper relationship between human reason and divine revelation. "Trust" (<em>batach</em>, בָּטַח) means to feel secure, confident, or safe—not mere intellectual assent but complete reliance. The phrase "with all thine heart" (<em>bekhol libbekha</em>, בְּכָל־לִבֶּךָ) demands total commitment, engaging the entire personality rather than partial allegiance.<br><br>"The Lord" uses the covenant name <em>Yahweh</em> (יהוה), emphasizing relationship with the God who has revealed Himself and proven faithful to His promises. This trust is not blind faith but confidence based on God's character and past faithfulness.<br><br>"Lean not unto thine own understanding" (<em>al tishaen</em>, אַל־תִּשָּׁעֵן) literally means "do not support yourself upon" human wisdom. This doesn't eliminate human reason but subordinates it to divine revelation. The contrast between "all your heart" and "your own understanding" emphasizes comprehensive trust versus limited human perspective.""",
                    "historical": """Proverbs 3 forms part of Solomon's wisdom literature, written during Israel's golden age when wisdom and learning flourished. The historical Solomon gathered wisdom from various sources while maintaining that true wisdom begins with fear of the Lord (Proverbs 1:7).<br><br>Ancient Near Eastern wisdom literature typically emphasized human observation and practical experience as the source of wisdom. While Proverbs incorporates practical wisdom, it uniquely subordinates human understanding to divine revelation, setting Hebrew wisdom apart from contemporary cultures.<br><br>The proverb addresses the perpetual human tendency to rely on limited understanding rather than trusting divine guidance. This would have been particularly relevant for a young king like Solomon, who needed wisdom beyond human capability to govern God's people effectively.""",
                    "questions": [
                        "How do believers balance using God-given rational abilities while trusting God rather than human understanding?",
                        "What are the practical implications of trusting God 'with all your heart' in decision-making and life planning?",
                        "How does this proverb address the contemporary tension between secular education and biblical faith?"
                    ]
                }
            }
        },
        "James": {
            1: {
                2: {
                    "analysis": """<strong>My brethren, count it all joy when ye fall into divers temptations.</strong> This counterintuitive command challenges natural human responses to difficulty. "Count it" (<em>hēgēsasthe</em>, ἡγήσασθε) means to consider, regard, or evaluate—a deliberate mental process rather than emotional feeling. The aorist imperative suggests a decisive choice to view trials from God's perspective.<br><br>"All joy" (<em>pasan charan</em>, πᾶσαν χαράν) doesn't mean partial happiness but complete joy. This joy isn't based on the trials themselves but on their ultimate purpose and results. The joy comes from understanding God's purposes in allowing difficulties.<br><br>"When ye fall into" (<em>hotan peripesēte</em>, ὅταν περιπέσητε) uses a verb meaning to fall around or encounter unexpectedly. "Divers temptations" (<em>peirasmois poikilois</em>, πειρασμοῖς ποικίλοις) refers to various trials or tests—circumstances that reveal and develop character rather than enticements to sin.""",
                    "historical": """James wrote to Jewish Christians scattered throughout the Roman Empire, likely during the persecution following Stephen's martyrdom (Acts 8:1). These believers faced both external persecution for their faith and internal struggles with favoritism, worldliness, and spiritual immaturity.<br><br>The recipients would have been familiar with Jewish understanding that suffering could serve divine purposes. The Old Testament taught that God tested His people to refine their faith (Deuteronomy 8:2-3), but James applies this principle to the new covenant community.<br><br>The early church's experience of persecution created a practical need for understanding how to respond to trials. James provides theological framework for viewing suffering as beneficial rather than merely enduring it passively.""",
                    "questions": [
                        "How can believers cultivate joy in trials without minimizing real pain or adopting superficial optimism?",
                        "What is the difference between trials that test faith and temptations that lead to sin, and how should responses differ?",
                        "How does understanding trials as having divine purpose change practical responses to unexpected difficulties?"
                    ]
                }
            }
        }
    }

    # Check for enhanced commentary first
    if book in enhanced_commentary and chapter in enhanced_commentary[book] and verse.verse in enhanced_commentary[book][chapter]:
        commentary_data = enhanced_commentary[book][chapter][verse.verse]
        return {
            "analysis": commentary_data["analysis"],
            "historical": commentary_data["historical"],
            "questions": commentary_data["questions"],
            "cross_references": generate_cross_references(book, chapter, verse.verse, verse.text)
        }

    # Special case for Revelation 1
    if book == "Revelation" and chapter == 1:
        # Dictionary of specialized commentary for Revelation 1
        revelation1_commentary = {
            1: {
                "analysis": """This opening verse establishes the divine origin of the Apocalypse (from Greek ἀποκάλυψις/<em>apokalypsis</em>, meaning "unveiling" or "revelation"). The chain of revelation is significant: from God, to Christ, to angel, to John, to the churches—establishing divine authority and authenticity. The phrase "things which must shortly come to pass" (ἃ δεῖ γενέσθαι ἐν τάχει) indicates both urgency and certainty, though not necessarily immediacy in human time scales. The Greek term ἐν τάχει can indicate rapidity of execution once something begins rather than imminence.<br><br>The phrase "signified it by his angel" uses the Greek ἐσήμανεν (from σημαίνω/<em>sēmainō</em>), literally meaning "to show by signs," hinting at the symbolic nature of the visions to follow. This carefully constructed introduction establishes: divine origin, Christological mediation, angelic communication, apostolic witness, and ecclesiastical destination.""",
                "historical": """During the reign of Emperor Domitian (81-96 CE), imperial cult worship intensified throughout the Roman Empire. Domitian demanded to be addressed as "Lord and God" (<em>dominus et deus noster</em>), and erected statues of himself for veneration. Christians who refused to burn incense to the emperor or participate in imperial festivals faced economic sanctions, social ostracism, and sometimes execution.<br><br>Patmos, where John received this revelation, was a small, rocky island about 37 miles southwest of Miletus in the Aegean Sea. Roman authorities used such islands as places of exile for political prisoners. John identifies himself as there "for the word of God, and for the testimony of Jesus Christ" (v.9), indicating his exile was punishment for his Christian witness.<br><br>The seven churches addressed were located along a Roman postal route in the province of Asia (western Turkey), each facing unique local challenges while sharing the broader imperial context of Roman domination and pressure to compromise.""",
                "questions": [
                    "How does the concept of divine revelation through a chain of transmission (God→Christ→angel→John→churches) shape your understanding of biblical authority?",
                    "In what ways does the description of Jesus 'signifying' the revelation suggest an approach to interpreting the symbolic language throughout the book?",
                    "How should we understand the timeframe indicated by 'shortly come to pass' given that nearly 2,000 years have passed? What different interpretive approaches address this apparent tension?",
                    "How might John's emphasis on the divine origin of this revelation have strengthened the resolve of persecuted believers in Asia Minor?"
                ],
                "cross_references": [
                    {"text": "Daniel 2:28-29", "url": "/book/Daniel/chapter/2#verse-28", "context": "Things revealed about the latter days"},
                    {"text": "John 15:15", "url": "/book/John/chapter/15#verse-15", "context": "Christ revealing the Father's will"},
                    {"text": "Amos 3:7", "url": "/book/Amos/chapter/3#verse-7", "context": "God revealing secrets to prophets"},
                    {"text": "2 Peter 1:20-21", "url": "/book/2 Peter/chapter/1#verse-20", "context": "Divine origin of prophecy"}
                ]
            },
            4: {
                "analysis": """This verse begins the formal epistolary greeting to the seven churches of Asia Minor. The trinitarian formula is striking and unique: the eternal Father ("who is, who was, and who is to come"), the sevenfold Spirit "before his throne," and Jesus Christ (fully described in v.5).<br><br>The description of God as "who is, who was, and who is to come" (ὁ ὢν καὶ ὁ ἦν καὶ ὁ ἐρχόμενος) forms a deliberate adaptation of God's self-revelation in Exodus 3:14. While Greek would normally render the divine name with "who was, who is, and who will be," John alters the final element to emphasize not just God's future existence but His active coming to establish His kingdom.<br><br>The "seven Spirits before his throne" has been interpreted in several ways: (1) the sevenfold manifestation of the Holy Spirit based on Isaiah 11:2-3, (2) the seven archangels of Jewish apocalyptic tradition, or (3) the perfection and completeness of the Holy Spirit. The context strongly suggests this refers to the Holy Spirit in His perfect fullness, as this forms part of the trinitarian greeting. The number seven appears 54 times in Revelation, consistently symbolizing divine completeness and perfection.""",
                "historical": """The seven churches addressed—Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, and Laodicea—were actual congregations in Asia Minor (modern western Turkey). They existed along a natural circular mail route approximately 100 miles in diameter.<br><br>Each city had distinctive characteristics:<br>• <strong>Ephesus</strong>: A major commercial center with the Temple of Artemis (one of the Seven Wonders of the ancient world)<br>• <strong>Smyrna</strong>: A beautiful port city known for emperor worship and fierce loyalty to Rome<br>• <strong>Pergamum</strong>: The provincial capital with an enormous altar to Zeus and a temple to Asclepius (god of healing)<br>• <strong>Thyatira</strong>: Known for trade guilds that posed idolatry challenges for Christians<br>• <strong>Sardis</strong>: Former capital of Lydia, known for wealth and textile industry<br>• <strong>Philadelphia</strong>: The youngest and smallest city, subject to earthquakes<br>• <strong>Laodicea</strong>: A banking center known for eye medicine and black wool<br><br>These churches represented the spectrum of faith communities, facing various challenges: persecution, false teaching, moral compromise, spiritual apathy, and economic pressure to participate in trade guild idolatry. Though historically specific, they also represent the complete church throughout history (seven symbolizing completeness).""",
                "questions": [
                    "What does the description of God as 'who is, who was, and who is to come' reveal about divine nature and how does this differ from Greek philosophical conceptions of deity?",
                    "How does John's adaptation of the divine name from Exodus 3:14 emphasize God's active involvement in human history?",
                    "What theological significance might the order of the Trinity in this greeting have (Father, Spirit, Son) compared to more common formulations?",
                    "How might the believers in these seven diverse churches have found comfort in being addressed collectively under divine blessing?",
                    "What might the image of the 'seven Spirits before his throne' suggest about the Holy Spirit's relationship to both the Father and the churches?"
                ],
                "cross_references": [
                    {"text": "Exodus 3:14", "url": "/book/Exodus/chapter/3#verse-14", "context": "God as the 'I AM'"},
                    {"text": "Isaiah 11:2-3", "url": "/book/Isaiah/chapter/11#verse-2", "context": "Seven aspects of the Spirit"},
                    {"text": "Zechariah 4:2-10", "url": "/book/Zechariah/chapter/4#verse-2", "context": "Seven lamps as the eyes of the LORD"},
                    {"text": "2 Corinthians 13:14", "url": "/book/2 Corinthians/chapter/13#verse-14", "context": "Trinitarian blessing"}
                ]
            },
            7: {
                "analysis": """This powerful verse serves as the central proclamation of Christ's eschatological return, combining two profound Old Testament prophecies in a remarkable synthesis: Daniel 7:13 ("coming with clouds") and Zechariah 12:10 ("they shall look upon me whom they have pierced").<br><br>The declaration begins dramatically with "Behold" (Ἰδού/<em>idou</em>), demanding attention to this climactic event. The "clouds" (νεφελῶν/<em>nephelōn</em>) evoke both the Old Testament theophany tradition where clouds symbolize divine presence (Exodus 13:21, 19:9) and Daniel's vision of the Son of Man coming with clouds to receive dominion and glory.<br><br>The universal witness to Christ's return ("every eye shall see him") emphasizes its public, unmistakable nature, contrasting with His first coming in relative obscurity. The specific mention of "they which pierced him" (ἐξεκέντησαν/<em>exekentēsan</em>, a direct reference to the crucifixion) and the mourning of "all kindreds of the earth" introduces a tension between judgment and potential repentance.<br><br>The verse concludes with divine affirmation—"Even so, Amen"—combining Greek (ναί/<em>nai</em>) and Hebrew (ἀμήν/<em>amēn</em>) expressions of certainty, emphasizing this event's absolute inevitability across all cultures.""",
                "historical": """For Christians facing persecution under Domitian (81-96 CE), this proclamation of Christ's return as cosmic Lord would provide profound hope and perspective. Roman imperial ideology presented the emperor as divine ruler whose reign brought global peace (<em>pax Romana</em>). Imperial propaganda celebrated the emperor's <em>parousia</em> (arrival) to cities with elaborate ceremonies.<br><br>This verse subverts those imperial claims by declaring Jesus—not Caesar—as the true cosmic sovereign whose <em>parousia</em> will bring history to its climax. The language of "tribes of the earth mourning" (πᾶσαι αἱ φυλαὶ τῆς γῆς) echoes Roman triumphal processions where conquered peoples mourned as the victorious emperor processed through Rome.<br><br>For Jewish readers, the combination of Daniel 7:13 and Zechariah 12:10 was especially significant. While first-century Judaism typically separated the Messiah's coming from Yahweh's coming, John merges these, presenting Jesus as fulfilling both messianic hope and divine visitation. This would be both challenging and transformative for Jewish believers.<br><br>Archaeological evidence from the seven cities addressed shows extensive emperor worship installations. In Pergamum stood a massive temple to Augustus; in Ephesus was the Temple of Domitian with a 23-foot statue of the emperor. Against these claims of imperial divinity, the vision of Christ's return asserted true divine sovereignty.""",
                "questions": [
                    "How does the merging of Daniel 7:13 and Zechariah 12:10 transform our understanding of both prophecies, and what does this tell us about Christ's identity?",
                    "What is the significance of the universal nature of Christ's return—that 'every eye shall see him'—in contrast to claims of secret or localized appearances?",
                    "How might the phrase 'all kindreds of the earth shall wail because of him' be understood—is this solely judgment, or might it include elements of repentance and recognition?",
                    "In what ways does the certainty of Christ's return as cosmic Lord challenge contemporary 'empires' and power structures?",
                    "How should the tension between Christ's first coming in humility and His second coming in glory shape our understanding of God's redemptive work?"
                ],
                "cross_references": [
                    {"text": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "context": "Son of Man coming with clouds"},
                    {"text": "Zechariah 12:10-14", "url": "/book/Zechariah/chapter/12#verse-10", "context": "Looking on him whom they pierced"},
                    {"text": "Matthew 24:30-31", "url": "/book/Matthew/chapter/24#verse-30", "context": "Christ's return with clouds and angels"},
                    {"text": "1 Thessalonians 4:16-17", "url": "/book/1 Thessalonians/chapter/4#verse-16", "context": "The Lord's descent from heaven"},
                    {"text": "John 19:34-37", "url": "/book/John/chapter/19#verse-34", "context": "Christ pierced on the cross"}
                ]
            },
            13: {
                "analysis": """This verse begins the extraordinary Christophany—the vision of the glorified Christ among the lampstands. The description combines elements of royal, priestly, prophetic, and divine imagery in a stunning portrait of Christ's transcendent glory.<br><br>The phrase "one like unto the Son of man" (ὅμοιον υἱὸν ἀνθρώπου) deliberately echoes Daniel 7:13-14, where the "Son of Man" comes with clouds and receives everlasting dominion. This title, Jesus' favorite self-designation in the Gospels, here takes on its full apocalyptic significance.<br><br>The clothing described has dual significance: the "garment down to the foot" (ποδήρη/<em>podērē</em>) recalls the high priest's robe (Exodus 28:4, 39:29) while the "golden girdle" or sash around the chest rather than waist suggests royal dignity. In combining these images, Christ is presented as both King and High Priest in the order of Melchizedek (Hebrews 7).<br><br>His position "in the midst of the seven lampstands" is theologically significant, showing Christ's immediate presence with and authority over the churches. The lampstands (later identified as the seven churches) allude to both the tabernacle menorah (Exodus 25:31-40) and Zechariah's vision (Zechariah 4:2-10), suggesting the churches' function as light-bearers in the world under Christ's oversight.""",
                "historical": """In the Greco-Roman world of the late first century, this vision would have provided a stunning contrast to imperial imagery. Roman emperors were typically portrayed in statuary and coinage with idealized, youthful features, wearing the purple toga of authority, and often with radiate crowns suggesting solar divinity.<br><br>Domitian particularly promoted his divine status, having himself addressed as <em>dominus et deus noster</em> ("our lord and god"). In the provincial capital Pergamum (one of the seven churches addressed), a massive temple complex dedicated to emperor worship dominated the acropolis, visible throughout the city.<br><br>The Jewish community would have recognized multiple elements from prophetic tradition. The figure combines features from Ezekiel's vision of God's glory (Ezekiel 1:26-28), Daniel's "Ancient of Days" and "Son of Man" (Daniel 7:9-14, 10:5-6), and various theophany accounts. This deliberate merging of divine imagery with the human "Son of Man" figure creates one of the New Testament's most explicit presentations of Christ's deity.<br><br>Archaeological excavations at Ephesus (another of the seven churches) have uncovered a 23-foot statue of Emperor Domitian that once stood in his temple. John's vision provides the ultimate counter-imperial image: Christ as the true divine sovereign standing among His churches, outshining all imperial pretensions.""",
                "questions": [
                    "How does this vision of the glorified Christ compare with other portraits in Scripture, such as the transfiguration (Matthew 17:1-8) or Isaiah's throne room vision (Isaiah 6:1-5)?",
                    "What theological significance does Christ's position 'in the midst of the seven lampstands' have for our understanding of His relationship to the church?",
                    "How does the combination of royal, priestly, and divine imagery shape our understanding of Christ's multifaceted identity and work?",
                    "In what ways might this vision of Christ have challenged first-century believers' perspectives and provided comfort during persecution?",
                    "How should this majestic portrayal of Christ influence our worship and daily discipleship today?"
                ],
                "cross_references": [
                    {"text": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "context": "Son of Man vision"},
                    {"text": "Ezekiel 1:26-28", "url": "/book/Ezekiel/chapter/1#verse-26", "context": "Throne vision of divine glory"},
                    {"text": "Exodus 28:4, 39:29", "url": "/book/Exodus/chapter/28#verse-4", "context": "High priestly garments"},
                    {"text": "Hebrews 4:14-16", "url": "/book/Hebrews/chapter/4#verse-14", "context": "Christ as High Priest"},
                    {"text": "Zechariah 4:2-10", "url": "/book/Zechariah/chapter/4#verse-2", "context": "Vision of the lampstand"}
                ]
            },
            18: {
                "analysis": """This triumphant declaration by the risen Christ contains some of the most profound Christological statements in Scripture. The opening "I am" (ἐγώ εἰμι/<em>egō eimi</em>) echoes God's self-revelation to Moses (Exodus 3:14) and continues John's high Christology throughout Revelation.<br><br>The phrase "he that liveth, and was dead" encapsulates the central paradox of Christian faith—Christ's death and resurrection. The Greek construction (ὁ ζῶν, καὶ ἐγενόμην νεκρὸς) emphasizes the contrast between His eternal living nature and the historical fact of His death. The perfect tense of "am alive" (ζῶν εἰμι) indicates a past action with continuing results—He lives now because He conquered death.<br><br>The declaration "I am alive forevermore" (ζῶν εἰμι εἰς τοὺς αἰῶνας τῶν αἰώνων) asserts Christ's eternal existence, while "Amen" provides divine self-affirmation.<br><br>The climactic statement about possessing "the keys of hell and of death" (τὰς κλεῖς τοῦ θανάτου καὶ τοῦ ᾅδου) draws on ancient imagery where keys symbolize authority and control. In Jewish apocalyptic literature, these keys belonged exclusively to God. Christ now claims this divine prerogative, declaring His absolute sovereignty over mortality and the afterlife—the ultimate source of human fear.""",
                "historical": """For Christians facing potential martyrdom under Domitian's persecution, this verse would provide extraordinary comfort and courage. The Roman Empire's ultimate weapon against dissidents was death, but Christ's declaration neutralizes this threat by asserting His authority over death itself.<br><br>In Greco-Roman culture, Hades (ᾅδης, translated as "hell" in KJV) was understood as the realm of the dead, ruled by the god of the same name. Various mystery religions promised initiates privileged treatment in the afterlife, while imperial propaganda sometimes suggested the emperor controlled the destiny of subjects even after death.<br><br>Archaeological findings from the period show funerary inscriptions often expressing hopelessness regarding death. A common epitaph read "I was not, I became, I am not, I care not." Against this cultural backdrop of either fear or nihilism toward death, Christ's claim to hold death's keys would be revolutionary.<br><br>In Jewish tradition, Isaiah 22:22 presents God giving the "key of the house of David" to Eliakim, symbolizing transferred authority. The early church would understand Christ's possession of death's keys as fulfillment of His promise to Peter about the "keys of the kingdom" (Matthew 16:19)—but here magnified to cosmic proportions.<br><br>For the seven churches receiving this revelation—some already experiencing martyrdom (like Antipas in Pergamum, 2:13)—this verse transformed their understanding of persecution. Death was no longer defeat but transition into the realm still under Christ's authority.""",
                "questions": [
                    "How does Christ's claim to possess 'the keys of hell and of death' transform our understanding of mortality and the afterlife?",
                    "In what ways does the paradox of Christ who died yet lives forever challenge both ancient and modern conceptions of divine nature?",
                    "How might believers facing persecution or martyrdom throughout history have drawn strength from this verse?",
                    "What practical implications does Christ's victory over death have for disciples facing suffering, bereavement, or their own mortality?",
                    "How does this verse relate to Paul's teaching that 'the last enemy to be destroyed is death' (1 Corinthians 15:26)?"
                ],
                "cross_references": [
                    {"text": "Isaiah 22:22", "url": "/book/Isaiah/chapter/22#verse-22", "context": "The key of David symbolizing authority"},
                    {"text": "Romans 6:9-10", "url": "/book/Romans/chapter/6#verse-9", "context": "Christ dies no more, death has no dominion"},
                    {"text": "1 Corinthians 15:54-57", "url": "/book/1 Corinthians/chapter/15#verse-54", "context": "Death is swallowed up in victory"},
                    {"text": "Hebrews 2:14-15", "url": "/book/Hebrews/chapter/2#verse-14", "context": "Christ destroys death and delivers from its fear"},
                    {"text": "Hosea 13:14", "url": "/book/Hosea/chapter/13#verse-14", "context": "Prophecy of ransom from death and redemption from the grave"}
                ]
            }
        }

        # If we have special commentary for this verse, use it
        if verse.verse in revelation1_commentary:
            return revelation1_commentary[verse.verse]

        # For other verses in Revelation 1, use enhanced but generalized commentary
        analysis = f"This verse is part of John's apocalyptic vision of the glorified Christ. The symbolism connects to Old Testament prophetic tradition, particularly from Daniel and Ezekiel, while revealing Christ's divine nature and authority. The imagery of {get_key_phrase(verse.text.lower())} contributes to the overall majestic portrayal."

        historical = f"Written during a time of imperial persecution under Domitian, this vision would have encouraged believers to remain faithful despite opposition. The apocalyptic imagery draws on Jewish prophetic traditions while speaking to the specific challenges faced by first-century Christians in Asia Minor."

        questions = [
            "How does this verse contribute to the overall portrayal of Christ in Revelation 1?",
            "What symbolic elements in this verse connect to Old Testament prophecy?",
            "How might this imagery have strengthened the faith of persecuted believers?",
            "What does this revelation tell us about Christ's relationship to the Church?"
        ]

        # Generate cross-references specific to Revelation imagery
        cross_refs = [
            {"text": "Daniel 7:9-14", "url": "/book/Daniel/chapter/7#verse-9", "context": "Ancient of Days and Son of Man vision"},
            {"text": "Ezekiel 1:26-28", "url": "/book/Ezekiel/chapter/1#verse-26", "context": "Divine throne vision"},
            {"text": "Isaiah 6:1-5", "url": "/book/Isaiah/chapter/6#verse-1", "context": "Throne room vision"}
        ]

        return {
            "analysis": analysis,
            "historical": historical,
            "questions": random.sample(questions, 3),
            "cross_references": cross_refs[:2]  # Limit to 2 references
        }

    # For all other books/chapters, use enhanced theological analysis
    verse_text = verse.text.lower()
    verse_number = verse.verse

    # Generate sophisticated analysis based on biblical themes and context
    theme = get_enhanced_theological_theme(verse_text, book)
    key_concept = extract_theological_concept(verse_text, book)
    literary_context = analyze_literary_context(book, chapter)

    # Create rich, scholarly analysis
    analysis_templates = [
        f"This verse develops the {theme} theme central to {book}. The concept of <strong>{key_concept}</strong> reflects {get_theological_significance(book, theme)}. {get_literary_analysis(verse_text, book, literary_context)} The original language emphasizes {get_linguistic_insight(verse_text, book)}, providing deeper understanding of the author's theological intention.",

        f"Within the broader context of {book}, this passage highlights {theme} through {get_rhetorical_device(verse_text)}. The theological weight of <strong>{key_concept}</strong> {get_doctrinal_significance(key_concept, book)}. This verse contributes to the book's overall argument by {get_structural_purpose(book, chapter, verse_number)}.",

        f"The {theme} theme here intersects with {get_biblical_theology_connection(theme, book)}. Biblical theology recognizes this as part of {get_canonical_development(theme)}. The phrase emphasizing <strong>{key_concept}</strong> {get_systematic_theology_insight(key_concept)} and connects to the broader scriptural witness about {get_cross_biblical_theme(theme)}."
    ]

    historical_templates = [
        f"The historical context of {get_detailed_time_period(book)} provides crucial background for understanding this verse. {get_comprehensive_historical_context(book)} The {get_cultural_background(book, verse_text)} would have shaped how the original audience understood {key_concept}. Archaeological and historical evidence reveals {get_archaeological_insight(book, theme)}.",

        f"This passage must be understood within {get_socio_political_context(book)}. The author writes to address {get_historical_audience_situation(book, chapter)}, making the emphasis on {theme} particularly relevant. Historical documents from this period show {get_historical_parallel(book, key_concept)}, illuminating the verse's original impact.",

        f"The literary and historical milieu of {get_literary_historical_context(book)} shapes this text's meaning. {get_historical_theological_development(book, theme)} Understanding {get_ancient_worldview_context(book)} helps modern readers appreciate why the author emphasizes {key_concept} in this particular way."
    ]

    question_templates = [
        f"How does the {theme} theme in this verse connect to the overarching narrative of Scripture, and what does this reveal about God's character and purposes?",
        f"In what ways does understanding {key_concept} in its original context challenge or deepen contemporary Christian thinking about {theme}?",
        f"How might the original audience's understanding of {key_concept} differ from modern interpretations, and what bridges can be built between ancient meaning and contemporary application?",
        f"What systematic theological implications arise from this verse's treatment of {theme}, and how does it contribute to a biblical theology of {get_related_doctrine(theme)}?",
        f"How does this verse's literary context within {book} chapter {chapter} illuminate its theological significance, and what does this teach us about biblical interpretation?",
        f"What practical applications emerge from understanding {theme} as presented in this verse, particularly in light of {get_contemporary_relevance(theme, key_concept)}?",
        f"How does this passage contribute to our understanding of {get_biblical_theological_trajectory(theme)}, and what implications does this have for Christian discipleship?",
        f"In what ways does this verse's emphasis on {key_concept} address {get_contemporary_theological_challenge(theme)}, and how should the church respond?"
    ]

    # Generate cross-references with variety per verse
    cross_refs = get_enhanced_cross_references(book, chapter, verse_number, verse_text, theme, key_concept)

    # Return a dictionary with enhanced commentary components
    return {
        "analysis": random.choice(analysis_templates),
        "historical": random.choice(historical_templates),
        "questions": random.sample(question_templates, 3),
        "cross_references": cross_refs
    }


def get_enhanced_theological_theme(verse_text, book):
    """Extract primary theological theme from verse text considering book context"""
    themes = {
        # Core theological themes
        "salvation": ["save", "redeem", "deliver", "rescue", "forgive", "justify", "sanctify"],
        "covenant": ["covenant", "promise", "faithful", "oath", "testament", "pledge"],
        "kingdom of God": ["kingdom", "reign", "rule", "throne", "dominion", "authority"],
        "divine love": ["love", "mercy", "compassion", "grace", "kindness", "tender"],
        "faith and obedience": ["faith", "believe", "trust", "obey", "follow", "serve"],
        "judgment and justice": ["judge", "justice", "righteous", "condemn", "punish", "wrath"],
        "worship and praise": ["worship", "praise", "glory", "honor", "magnify", "exalt"],
        "suffering and persecution": ["suffer", "afflict", "persecute", "trial", "tribulation"],
        "hope and restoration": ["hope", "restore", "renew", "heal", "comfort", "peace"],
        "wisdom and understanding": ["wise", "wisdom", "understand", "knowledge", "discern"],
        "creation and providence": ["create", "made", "form", "establish", "sustain", "provide"],
        "sin and rebellion": ["sin", "transgress", "rebel", "iniquity", "evil", "wicked"]
    }

    # Book-specific theme adjustments
    book_themes = {
        "Genesis": ["creation and providence", "covenant", "divine love"],
        "Psalms": ["worship and praise", "divine love", "suffering and persecution"],
        "Romans": ["salvation", "faith and obedience", "judgment and justice"],
        "John": ["divine love", "salvation", "faith and obedience"],
        "Revelation": ["kingdom of God", "judgment and justice", "hope and restoration"]
    }

    primary_themes = book_themes.get(book, list(themes.keys())[:3])

    for theme in primary_themes:
        if any(word in verse_text for word in themes[theme]):
            return theme

    # Fallback to most common theme for the book
    return primary_themes[0] if primary_themes else "divine love"

def extract_theological_concept(verse_text, book):
    """Extract key theological concept from verse"""
    concepts = ["grace", "faith", "love", "righteousness", "salvation", "redemption",
               "covenant", "kingdom", "glory", "peace", "wisdom", "truth", "life",
               "hope", "mercy", "justice", "holiness", "forgiveness", "eternal life"]

    for concept in concepts:
        if concept in verse_text:
            return concept

    # Extract meaningful phrases if no single concept found
    if "lord" in verse_text or "god" in verse_text:
        return "divine sovereignty"
    elif "people" in verse_text or "nation" in verse_text:
        return "covenant community"
    else:
        return "divine revelation"

def analyze_literary_context(book, chapter):
    """Provide literary context for the book and chapter"""
    contexts = {
        "Genesis": f"foundational narrative establishing God's relationship with creation and humanity",
        "Psalms": f"worship literature expressing the full range of human experience before God",
        "Romans": f"systematic theological exposition of the gospel",
        "John": f"theological biography emphasizing Jesus' divine identity",
        "Revelation": f"apocalyptic literature revealing God's ultimate victory",
        "1 Corinthians": f"pastoral letter addressing practical Christian living issues",
        "Matthew": f"gospel presenting Jesus as the fulfillment of Jewish Messianic hope"
    }
    return contexts.get(book, f"biblical literature contributing to the canon's theological witness")

def get_theological_significance(book, theme):
    """Get theological significance of theme within book context"""
    significance_map = {
        ("Genesis", "creation and providence"): "God's absolute sovereignty over all existence",
        ("Psalms", "worship and praise"): "the proper human response to God's character and works",
        ("Romans", "salvation"): "justification by faith as the foundation of Christian hope",
        ("John", "divine love"): "the essential nature of God revealed through Christ",
        ("Revelation", "kingdom of God"): "the ultimate establishment of divine rule over creation"
    }
    key = (book, theme)
    return significance_map.get(key, f"the development of {theme} within biblical theology")

def get_doctrinal_significance(concept, book):
    """Provide doctrinal significance of theological concept"""
    return f"connects to fundamental Christian doctrine about {concept}, contributing to our understanding of God's nature and relationship with humanity"

def get_enhanced_cross_references(book, chapter, verse_number, verse_text, theme, concept):
    """Generate enhanced cross-references based on theme and concept with variety"""
    # Expanded pool of cross-references for each theme
    theme_refs = {
        "salvation": [
            {"text": "Romans 10:9", "url": "/book/Romans/chapter/10#verse-9", "context": "Confession and faith"},
            {"text": "Ephesians 2:8-9", "url": "/book/Ephesians/chapter/2#verse-8", "context": "Salvation by grace"},
            {"text": "Acts 4:12", "url": "/book/Acts/chapter/4#verse-12", "context": "No other name"},
            {"text": "Titus 3:5", "url": "/book/Titus/chapter/3#verse-5", "context": "Not by works"},
            {"text": "John 3:16", "url": "/book/John/chapter/3#verse-16", "context": "God's love and salvation"}
        ],
        "divine love": [
            {"text": "1 John 4:8", "url": "/book/1 John/chapter/4#verse-8", "context": "God is love"},
            {"text": "Romans 5:8", "url": "/book/Romans/chapter/5#verse-8", "context": "Love in Christ's death"},
            {"text": "Jeremiah 31:3", "url": "/book/Jeremiah/chapter/31#verse-3", "context": "Everlasting love"},
            {"text": "John 15:13", "url": "/book/John/chapter/15#verse-13", "context": "Greater love"}
        ],
        "faith and obedience": [
            {"text": "Hebrews 11:1", "url": "/book/Hebrews/chapter/11#verse-1", "context": "Definition of faith"},
            {"text": "James 2:17", "url": "/book/James/chapter/2#verse-17", "context": "Faith and works"},
            {"text": "Proverbs 3:5-6", "url": "/book/Proverbs/chapter/3#verse-5", "context": "Trust in the Lord"},
            {"text": "John 14:15", "url": "/book/John/chapter/14#verse-15", "context": "Love and obedience"}
        ],
        "covenant": [
            {"text": "Genesis 17:7", "url": "/book/Genesis/chapter/17#verse-7", "context": "Everlasting covenant"},
            {"text": "Jeremiah 31:31", "url": "/book/Jeremiah/chapter/31#verse-31", "context": "New covenant"},
            {"text": "Hebrews 8:6", "url": "/book/Hebrews/chapter/8#verse-6", "context": "Better covenant"}
        ],
        "kingdom of God": [
            {"text": "Matthew 6:33", "url": "/book/Matthew/chapter/6#verse-33", "context": "Seek first the kingdom"},
            {"text": "Luke 17:21", "url": "/book/Luke/chapter/17#verse-21", "context": "Kingdom within you"},
            {"text": "Colossians 1:13", "url": "/book/Colossians/chapter/1#verse-13", "context": "Transferred to kingdom"}
        ]
    }

    # Get available references for the theme
    available_refs = theme_refs.get(theme, [
        {"text": "Psalm 119:105", "url": "/book/Psalms/chapter/119#verse-105", "context": "Word is a lamp"},
        {"text": "2 Timothy 3:16", "url": "/book/2 Timothy/chapter/3#verse-16", "context": "All Scripture inspired"},
        {"text": "Isaiah 40:8", "url": "/book/Isaiah/chapter/40#verse-8", "context": "Word stands forever"},
        {"text": "Matthew 24:35", "url": "/book/Matthew/chapter/24#verse-35", "context": "Words not pass away"}
    ])

    # Use verse number to create variety - different verses get different refs
    import random
    random.seed(f"{book}{chapter}{verse_number}")  # Deterministic but varied per verse
    selected = random.sample(available_refs, min(2, len(available_refs)))

    return selected


def get_literary_analysis(verse_text, book, literary_context):
    """Provide literary analysis of the verse within its context"""
    if "lord" in verse_text or "god" in verse_text:
        return f"The divine name or title here functions within {literary_context} to establish theological authority and covenantal relationship."
    elif any(word in verse_text for word in ["love", "mercy", "grace"]):
        return f"The emotional and relational language employed here is characteristic of {literary_context}, emphasizing the personal nature of divine-human relationship."
    else:
        return f"The literary structure and word choice here contribute to {literary_context}, advancing the author's theological argument."

def get_linguistic_insight(verse_text, book):
    """Provide insight into original language significance"""
    insights = {
        "lord": "the covenant name Yahweh, emphasizing God's faithfulness to His promises",
        "love": "agape in Greek contexts or hesed in Hebrew, indicating covenantal loyalty",
        "faith": "pistis in Greek, encompassing both belief and faithfulness",
        "salvation": "soteria in Greek or yeshua in Hebrew, indicating deliverance and wholeness",
        "grace": "charis in Greek or hen in Hebrew, emphasizing unmerited divine favor"
    }

    for word, insight in insights.items():
        if word in verse_text:
            return insight
    return "careful word choice that would have carried specific theological weight for the original audience"

def get_rhetorical_device(verse_text):
    """Identify rhetorical or literary devices in the verse"""
    if "like" in verse_text or "as" in verse_text:
        return "simile or metaphorical language"
    elif any(word in verse_text for word in ["all", "every", "none", "nothing"]):
        return "universal language and absolute statements"
    elif "?" in verse_text:
        return "rhetorical questioning that engages the reader"
    else:
        return "declarative statements that establish theological truth"

def get_structural_purpose(book, chapter, verse_number):
    """Explain how the verse functions structurally within the book"""
    if verse_number == 1:
        return f"introducing key themes that will be developed throughout {book}"
    elif chapter == 1:
        return f"establishing foundational concepts crucial to {book}'s theological argument"
    else:
        return f"building upon previous themes while advancing the overall message of {book}"

def get_biblical_theology_connection(theme, book):
    """Connect the theme to broader biblical theology"""
    connections = {
        "salvation": "the metanarrative of redemption running from Genesis to Revelation",
        "divine love": "God's covenantal faithfulness demonstrated throughout salvation history",
        "kingdom of God": "the progressive revelation of God's rule from creation to consummation",
        "covenant": "God's relationship with His people from Abraham through the new covenant",
        "faith and obedience": "the proper human response to divine revelation across Scripture"
    }
    return connections.get(theme, "the broader canonical witness to God's character and purposes")

def get_canonical_development(theme):
    """Describe how the theme develops across the biblical canon"""
    developments = {
        "salvation": "a unified storyline from the promise in Genesis 3:15 to its fulfillment in Christ",
        "divine love": "progressive revelation from covenant love in the Old Testament to agape love in the New",
        "kingdom of God": "development from creation mandate through Davidic kingdom to eschatological fulfillment",
        "covenant": "evolution from creation covenant through Abrahamic, Mosaic, Davidic, to new covenant"
    }
    return developments.get(theme, "progressive revelation that finds its culmination in Christ")

def get_systematic_theology_insight(concept):
    """Provide systematic theological perspective on the concept"""
    insights = {
        "grace": "relates to the doctrine of soteriology and God's unmerited favor in salvation",
        "faith": "central to epistemology and the means by which humans receive divine revelation",
        "love": "fundamental to theology proper, revealing God's essential nature and character",
        "salvation": "encompasses justification, sanctification, and glorification in the ordo salutis",
        "kingdom": "relates to eschatology and the ultimate purpose of God's redemptive plan"
    }
    return insights.get(concept, "contributes to our systematic understanding of Christian doctrine")

def get_cross_biblical_theme(theme):
    """Identify how the theme appears across Scripture"""
    cross_biblical = {
        "salvation": "God's saving work from the Exodus to the cross",
        "divine love": "hesed in the Old Testament and agape in the New Testament",
        "kingdom of God": "God's reign from creation through the millennial kingdom",
        "covenant": "God's relational commitment from Noah to the new covenant"
    }
    return cross_biblical.get(theme, "God's consistent character and purposes")

def get_detailed_time_period(book):
    """Provide detailed historical time period for the book"""
    periods = {
        "Genesis": "the patriarchal period (c. 2000-1500 BCE) and primeval history",
        "Exodus": "the period of Egyptian bondage and wilderness wandering (c. 1440-1400 BCE)",
        "Psalms": "the monarchic period, particularly David's reign (c. 1000-970 BCE)",
        "Romans": "the early imperial period under Nero (c. 57 CE)",
        "John": "the late first century during increasing tension between synagogue and church",
        "Revelation": "the Domitian persecution period (c. 95 CE)"
    }
    return periods.get(book, "the biblical period relevant to this book's composition")

def get_comprehensive_historical_context(book):
    """Provide comprehensive historical background"""
    contexts = {
        "Genesis": "The ancient Near Eastern world with its creation myths, flood narratives, and patriarchal social structures provided the cultural backdrop against which God's revelation stands in stark contrast.",
        "Romans": "The Roman Empire at its height, with sophisticated legal systems, diverse religious practices, and increasing Christian presence in major urban centers shaped Paul's theological arguments.",
        "Psalms": "The Israelite monarchy with its temple worship, court life, and constant military threats created the liturgical and emotional context for these prayers and praises."
    }
    return contexts.get(book, "The historical and cultural milieu of the biblical world informed the author's theological expression and the audience's understanding.")

def get_archaeological_insight(book, theme):
    """Provide relevant archaeological insight"""
    insights = {
        ("Genesis", "creation and providence"): "Ancient Near Eastern creation texts like Enuma Elish provide comparative context for understanding Genesis's unique theological perspective",
        ("Romans", "salvation"): "Inscriptions from Corinth and Rome reveal the social dynamics and religious pluralism that shaped early Christian communities",
        ("Psalms", "worship and praise"): "Temple archaeology and ancient musical instruments illuminate the liturgical context of Israelite worship"
    }
    key = (book, theme)
    return insights.get(key, "Archaeological discoveries continue to illuminate the historical context of biblical texts")

def get_related_doctrine(theme):
    """Identify related systematic theology doctrines"""
    doctrines = {
        "salvation": "soteriology and the doctrine of salvation",
        "divine love": "theology proper and the doctrine of God",
        "kingdom of God": "eschatology and the doctrine of last things",
        "covenant": "theology of covenant and God's relational commitment"
    }
    return doctrines.get(theme, "fundamental Christian doctrine")

def get_contemporary_relevance(theme, concept):
    """Identify contemporary relevance and application"""
    relevance = {
        "salvation": "addressing questions of religious pluralism and the exclusivity of Christ",
        "divine love": "responding to cultural confusion about the nature of love and relationships",
        "kingdom of God": "providing hope in times of political and social upheaval",
        "faith and obedience": "challenging cultural relativism with objective truth claims"
    }
    return relevance.get(theme, "contemporary challenges facing the church and individual believers")

def get_cultural_background(book, verse_text):
    """Provide cultural background relevant to the verse"""
    backgrounds = {
        "Genesis": "ancient Near Eastern cosmology and patriarchal society",
        "Matthew": "first-century Palestinian Jewish culture under Roman occupation",
        "Romans": "Greco-Roman urban culture with diverse religious and philosophical influences",
        "Psalms": "ancient Israelite worship practices and court culture",
        "John": "late first-century Jewish-Christian tensions and Hellenistic thought"
    }
    return backgrounds.get(book, "the cultural context of the biblical world")

def get_socio_political_context(book):
    """Provide socio-political context for the book"""
    contexts = {
        "Genesis": "the tribal and clan-based society of the ancient Near East",
        "Matthew": "Roman imperial rule over Jewish Palestine with messianic expectations",
        "Romans": "the cosmopolitan capital of the Roman Empire with diverse populations",
        "Psalms": "the Israelite monarchy with its court politics and military conflicts",
        "Revelation": "imperial persecution under Domitian's demand for emperor worship"
    }
    return contexts.get(book, "the political and social structures of the biblical period")

def get_historical_audience_situation(book, chapter):
    """Describe the specific situation of the original audience"""
    situations = {
        "Genesis": "the foundational narrative for Israel's identity and relationship with God",
        "Matthew": "Jewish Christians seeking to understand Jesus as Messiah",
        "Romans": "a mixed congregation of Jewish and Gentile believers in the imperial capital",
        "Psalms": "worshipers in the temple and those seeking God in times of distress",
        "Revelation": "persecuted Christians in Asia Minor facing pressure to compromise"
    }
    return situations.get(book, "believers seeking to understand God's will and purposes")

def get_historical_parallel(book, concept):
    """Provide historical parallels that illuminate the concept"""
    parallels = {
        "salvation": "rescue narratives from ancient literature that would resonate with the audience",
        "kingdom": "imperial and royal imagery familiar to subjects of ancient monarchies",
        "covenant": "treaty language and adoption practices from the ancient world",
        "love": "patron-client relationships and family loyalty concepts"
    }
    return parallels.get(concept, "cultural practices and social structures that would have been familiar to the original readers")

def get_literary_historical_context(book):
    """Provide literary and historical context combined"""
    contexts = {
        "Genesis": "ancient Near Eastern narrative literature addressing origins and identity",
        "Matthew": "Jewish biographical literature presenting Jesus as the fulfillment of Scripture",
        "Romans": "Hellenistic epistolary literature with sophisticated theological argumentation",
        "Psalms": "ancient Near Eastern poetry and hymnic literature for worship",
        "Revelation": "Jewish apocalyptic literature using symbolic imagery to convey hope"
    }
    return contexts.get(book, "the literary conventions and historical circumstances of biblical literature")

def get_historical_theological_development(book, theme):
    """Describe how the theme developed historically within the book's context"""
    developments = {
        ("Genesis", "creation and providence"): "The development from creation to divine election established God's sovereign care over history",
        ("Romans", "salvation"): "Paul's systematic presentation built upon centuries of Jewish understanding about righteousness and divine justice",
        ("Psalms", "worship and praise"): "Israel's liturgical traditions developed through centuries of temple worship and personal devotion"
    }
    key = (book, theme)
    return developments.get(key, f"The historical development of {theme} within the theological tradition of {book}")

def get_ancient_worldview_context(book):
    """Provide ancient worldview context"""
    worldviews = {
        "Genesis": "a worldview where divine beings actively governed natural and historical processes",
        "Matthew": "a worldview expecting divine intervention through a promised Messiah",
        "Romans": "a worldview shaped by both Jewish monotheism and Greco-Roman philosophical thought",
        "Psalms": "a worldview centered on covenant relationship between God and His people"
    }
    return worldviews.get(book, "the ancient worldview that shaped the author's theological expression")

def get_biblical_theological_trajectory(theme):
    """Describe the biblical theological trajectory of the theme"""
    trajectories = {
        "salvation": "from physical deliverance in the Old Testament to spiritual redemption in the New",
        "kingdom of God": "from earthly theocracy through Davidic kingdom to eschatological fulfillment",
        "divine love": "from covenant faithfulness to sacrificial love demonstrated in Christ",
        "faith and obedience": "from law observance to faith in Christ as the means of righteousness"
    }
    return trajectories.get(theme, "the progressive revelation of God's purposes throughout Scripture")

def get_contemporary_theological_challenge(theme):
    """Identify contemporary theological challenges addressed by the theme"""
    challenges = {
        "salvation": "religious pluralism and questions about the necessity of Christ",
        "divine love": "the problem of evil and suffering in light of God's goodness",
        "kingdom of God": "the apparent delay of Christ's return and God's justice",
        "faith and obedience": "the relationship between faith and works in salvation"
    }
    return challenges.get(theme, "questions about God's character and purposes in the modern world")

def generate_chapter_overview(book, chapter, verses):
    """Generate an AI-powered overview of the entire chapter"""
    # Special case for Revelation 1
    if book == "Revelation" and chapter == 1:
        return """
    <p><strong>Revelation 1</strong> is the magnificent apocalyptic introduction to the final book of the Bible, often called the <em>Apocalypse</em> (from the Greek ἀποκάλυψις, meaning "unveiling" or "revelation"). Written during the reign of Emperor Domitian (c. 95 CE) when imperial persecution was intensifying, this chapter presents John's vision of the glorified Christ and establishes the divine authority behind the revelations that follow.</p>

    <p>The author identifies himself as "John" (verse 1:1, 1:4, 1:9), traditionally understood to be the Apostle John, though some scholars propose it may be another John known as "John the Elder." He was exiled to Patmos, a small rocky island in the Aegean Sea about 37 miles southwest of Miletus, "for the word of God, and for the testimony of Jesus Christ" (verse 9).</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Literary Structure and Context</h4>

    <p>Revelation belongs to the apocalyptic genre, characterized by symbolic visions, supernatural beings, cosmic conflict, and the ultimate triumph of good over evil. This literary form was especially meaningful during times of persecution, offering hope through coded imagery that conveyed God's sovereignty over earthly powers.</p>

    <p>This chapter establishes several literary patterns that will repeat throughout the book:</p>
    <ul>
        <li>The <strong>number seven</strong> (7 churches, 7 spirits, 7 golden lampstands, 7 stars) symbolizing divine completeness and perfection</li>
        <li><strong>Divine titles</strong> expressing eternal nature ("Alpha and Omega," "First and Last," "Beginning and End")</li>
        <li><strong>Old Testament allusions</strong>, particularly to Daniel, Ezekiel, and Isaiah</li>
        <li><strong>Paradoxical imagery</strong> ("a Lamb as it had been slain" appears later but is foreshadowed by Christ who died yet lives)</li>
    </ul>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Chapter Structure</h4>

    <ol>
        <li><strong>Prologue (Verses 1-3)</strong>: Establishes the divine source and purpose of the revelation, promising blessing to those who read, hear, and keep these prophecies. The phrase "the time is at hand" creates eschatological urgency.</li>

        <li><strong>Epistolary Greeting (Verses 4-8)</strong>: John addresses the seven churches of Asia Minor with a trinitarian blessing. This section contains the first of seven beatitudes in Revelation (verse 3) and introduces Christ with titles emphasizing His eternal nature, redemptive work, and future return.</li>

        <li><strong>John's Commissioning Vision (Verses 9-16)</strong>: The exiled apostle receives his commission on "the Lord's day" (the first Christian use of this term in literature). Christ appears in transcendent glory among seven golden lampstands, with imagery drawing heavily from Daniel 7:13-14, Daniel 10:5-6, and Ezekiel 1:24-28. Each symbolic element (white hair, flaming eyes, bronze feet, thunderous voice) reveals an aspect of Christ's divine nature and authority.</li>

        <li><strong>Christ's Self-Revelation and Command (Verses 17-20)</strong>: After John falls "as dead" before the vision (compare with Isaiah 6:5, Ezekiel 1:28, Daniel 10:8-9), Christ identifies Himself as the eternal living one who conquered death. He commands John to write what he sees, explaining the mystery of the seven stars (angels/messengers of the churches) and seven lampstands (the churches themselves).</li>
    </ol>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Historical Context</h4>

    <p>Emperor Domitian (reigned 81-96 CE) intensified emperor worship throughout the Roman Empire, demanding to be addressed as "Lord and God" (<em>dominus et deus</em>). Christians who refused to participate in imperial cult rituals faced economic marginalization (foreshadowing the "mark of the beast"), social ostracism, and sometimes execution.</p>

    <p>The seven churches addressed were located on a Roman postal route in Asia Minor (modern Turkey), each facing unique challenges:</p>
    <ul>
        <li><strong>Ephesus</strong>: A major commercial center with the Temple of Artemis</li>
        <li><strong>Smyrna</strong>: Known for intense emperor worship and Jewish opposition to Christians</li>
        <li><strong>Pergamum</strong>: Center of emperor worship with a large altar to Zeus</li>
        <li><strong>Thyatira</strong>: Known for trade guilds that posed idolatry challenges</li>
        <li><strong>Sardis</strong>: Former capital of Lydia, known for complacency</li>
        <li><strong>Philadelphia</strong>: Smallest city, facing Jewish opposition</li>
        <li><strong>Laodicea</strong>: Wealthy banking center known for lukewarm water supply</li>
    </ul>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>Revelation 1 establishes several profound theological truths:</p>

    <ol>
        <li><strong>High Christology</strong>: Christ is portrayed with divine attributes and titles previously reserved for Yahweh in the Old Testament. This establishes one of the earliest and clearest presentations of Christ's deity in Christian literature.</li>

        <li><strong>Divine Sovereignty</strong>: Despite the apparent triumph of evil powers (Roman persecution), God remains enthroned and history moves toward His predetermined conclusion.</li>

        <li><strong>Trinitarian Framework</strong>: The greeting in verses 4-5 includes all three persons of the Trinity, with the unusual description of the Holy Spirit as "the seven spirits before his throne" (possibly referring to Isaiah 11:2-3 or Zechariah 4:1-10).</li>

        <li><strong>Church Identity</strong>: The churches are represented as lampstands with Christ moving among them, suggesting both their mission to bear light and Christ's evaluative presence.</li>

        <li><strong>Victory Through Suffering</strong>: John, a "companion in tribulation" (verse 9), writes from exile, establishing that God's revelation comes in the midst of, not despite, suffering. Christ is identified as one who "loved us, and washed us from our sins in his own blood" (verse 5), linking redemption to sacrificial suffering.</li>
    </ol>

    <p>When studying Revelation 1, it's essential to approach the text with awareness of its apocalyptic genre, historical context, and symbolic language. The chapter forms the foundation for understanding the entire book, introducing themes, symbols, and theological concepts that will be developed throughout the subsequent visions.</p>

    <p>For believers under persecution, whether in the first century or today, this chapter offers the profound assurance that Christ – the Alpha and Omega, the First and Last – remains sovereign over history and present with His church through all tribulations.</p>
    """

    # Genesis 1 - Creation
    if book == "Genesis" and chapter == 1:
        return """
    <p><strong>Genesis 1</strong> is the majestic opening of Scripture, presenting the foundational account of creation. In stately, liturgical prose, this chapter establishes God as the sovereign Creator who brings order from chaos through the power of His word. The Hebrew title <em>Bereshit</em> ("In the beginning") captures the cosmic scope of this narrative, which addresses the fundamental questions of human existence: Where did we come from? Who is God? What is humanity's purpose?</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Literary Structure</h4>

    <p>The chapter follows a carefully crafted seven-day structure, with each day building upon the previous in a divine architectural plan:</p>

    <ol>
        <li><strong>Day 1 (verses 3-5)</strong>: Light separated from darkness, establishing day and night</li>
        <li><strong>Day 2 (verses 6-8)</strong>: The firmament (sky) dividing waters above from waters below</li>
        <li><strong>Day 3 (verses 9-13)</strong>: Dry land appearing, vegetation created</li>
        <li><strong>Day 4 (verses 14-19)</strong>: Sun, moon, and stars placed in the firmament</li>
        <li><strong>Day 5 (verses 20-23)</strong>: Sea creatures and birds created</li>
        <li><strong>Day 6 (verses 24-31)</strong>: Land animals created, then humanity as the pinnacle</li>
        <li><strong>Day 7 (2:1-3)</strong>: God rests, sanctifying the Sabbath</li>
    </ol>

    <p>Note the parallel structure: Days 1-3 establish <em>realms</em> (light, sky, land), while Days 4-6 populate those realms with <em>rulers</em> (luminaries, birds/fish, animals/humans). This literary symmetry emphasizes divine order and purposefulness.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Creative Word</h4>

    <p>The repeated phrase "And God said" (Hebrew <em>vayomer Elohim</em>) occurs ten times, corresponding to the Ten Commandments and emphasizing creation by divine fiat. God speaks, and reality conforms to His word. This establishes several crucial theological principles:</p>

    <ul>
        <li><strong>Divine transcendence</strong>: God exists independently of creation and is not identified with nature (contra pagan cosmologies)</li>
        <li><strong>Purposeful design</strong>: Creation is intentional, not accidental or chaotic</li>
        <li><strong>Inherent goodness</strong>: Seven times God declares creation "good" (<em>tov</em>), culminating in "very good" (<em>tov meod</em>) after creating humanity</li>
        <li><strong>Word and power</strong>: God's word accomplishes what it declares (cf. Isaiah 55:11, John 1:1-3)</li>
    </ul>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Humanity in God's Image</h4>

    <p>The climax arrives in verses 26-28 with humanity's creation. Unlike other creatures, humans are made "in our image, after our likeness" (<em>b'tzelem Elohim</em>). This <em>imago Dei</em> establishes humanity's unique dignity and role:</p>

    <ul>
        <li><strong>Relational capacity</strong>: Able to know and commune with God</li>
        <li><strong>Moral agency</strong>: Responsible to God's commands</li>
        <li><strong>Creative reflection</strong>: Called to exercise dominion and stewardship</li>
        <li><strong>Gender complementarity</strong>: "Male and female created he them" (verse 27) - both equally bear God's image</li>
    </ul>

    <p>The dual mandate given to humanity in verses 28-30 includes both procreation ("be fruitful and multiply") and stewardship ("have dominion"), establishing human vocation as both relational and responsible.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Historical and Ancient Near Eastern Context</h4>

    <p>Genesis 1 emerged in a world filled with competing creation narratives. Unlike the Babylonian <em>Enuma Elish</em> (with its violent divine conflicts) or Egyptian cosmologies (with multiple creator deities), Genesis presents:</p>

    <ul>
        <li><strong>Monotheism</strong>: One God, not a pantheon</li>
        <li><strong>Creation ex nihilo</strong>: God creates from nothing, not from pre-existing divine matter</li>
        <li><strong>De-divinization of nature</strong>: Sun, moon, and stars are created objects, not gods to worship</li>
        <li><strong>Human dignity</strong>: All people bear God's image, not just kings or priests</li>
    </ul>

    <p>These distinctions were revolutionary in the ancient world and remain foundational to Judeo-Christian thought.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>This chapter establishes the theological foundation for the entire biblical narrative:</p>

    <ol>
        <li><strong>God's sovereignty</strong>: The Creator has ultimate authority over His creation</li>
        <li><strong>Creation's dependence</strong>: All things exist by God's sustaining power</li>
        <li><strong>Order from chaos</strong>: God brings <em>cosmos</em> (order) from <em>tohu vabohu</em> (formless void)</li>
        <li><strong>Sabbath rest</strong>: God's rest establishes a pattern for human worship and rest</li>
        <li><strong>Christological foreshadowing</strong>: The Word through whom all things were made (John 1:1-3; Colossians 1:16)</li>
    </ol>

    <p>Genesis 1 is not merely ancient cosmology but enduring theology: the declaration that the universe is not random, humanity is not accidental, and God is intimately involved with His creation. Whether read as literal history, literary framework, or theological proclamation, this chapter affirms the essential truth that "in the beginning God" – and that makes all the difference.</p>
    """

    # Psalm 23 - The Shepherd Psalm
    if book == "Psalms" and chapter == 23:
        return """
    <p><strong>Psalm 23</strong> is perhaps the most beloved passage in all of Scripture, memorized and recited at bedsides, in hospital rooms, at funerals, and in moments of crisis across millennia. This brief six-verse psalm, attributed to David, presents God as the good shepherd who cares for His people with tender provision, faithful guidance, and protective presence.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Literary Structure and Imagery</h4>

    <p>The psalm divides naturally into two complementary images:</p>

    <ol>
        <li><strong>The Shepherd (verses 1-4)</strong>: God as the caring shepherd tending His flock</li>
        <li><strong>The Host (verses 5-6)</strong>: God as the generous host welcoming His guest</li>
    </ol>

    <p>Both metaphors emphasize God's provision, protection, and intimate care, but from different angles – pastoral and domestic.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Shepherd Metaphor (Verses 1-4)</h4>

    <p><strong>"The LORD is my shepherd; I shall not want"</strong> (verse 1) – The opening declaration establishes a personal relationship. Not merely "the LORD is <em>a</em> shepherd," but "<em>my</em> shepherd." The Hebrew <em>Yahweh ro'i</em> emphasizes covenant intimacy. The result? "I shall not want" – complete sufficiency in God's care.</p>

    <p><strong>"He maketh me to lie down in green pastures"</strong> (verse 2) – Sheep only lie down when four conditions are met: they are not hungry, not afraid, not bothered by pests, and not in conflict with other sheep. The good shepherd ensures all these needs are met. Green pastures (<em>ne'ot deshe</em>) were precious in the arid Palestinian landscape, signifying abundant provision.</p>

    <p><strong>"He leadeth me beside the still waters"</strong> (verse 2) – Literally "waters of rest" (<em>mei menuchot</em>). Sheep fear fast-moving water and will not drink from turbulent streams. The shepherd finds calm pools where the flock can safely drink. This speaks to God's wisdom in providing rest and refreshment suited to our nature.</p>

    <p><strong>"He restoreth my soul"</strong> (verse 3) – The Hebrew <em>naphshi yeshobeb</em> suggests returning, refreshing, or reviving. When sheep wander or fall, the shepherd restores them to the path. This is both physical revival and spiritual renewal.</p>

    <p><strong>"He leadeth me in the paths of righteousness for his name's sake"</strong> (verse 3) – The shepherd doesn't merely find <em>any</em> path but <em>right</em> paths (<em>ma'gelei-tsedeq</em>) – straight tracks that lead to good destinations. God's guidance reflects His character ("for his name's sake") – He is faithful to His nature as the good shepherd.</p>

    <p><strong>"Yea, though I walk through the valley of the shadow of death"</strong> (verse 4) – The famous <em>gey tsalmaveth</em>, literally "valley of deep darkness" or "death-shadow." Palestinian shepherds led flocks through narrow ravines where danger lurked – predators, bandits, treacherous footing. Yet the psalmist declares "I will fear no evil: for thou art with me." Not because danger is absent, but because the shepherd is present.</p>

    <p><strong>"Thy rod and thy staff they comfort me"</strong> (verse 4) – The rod (<em>shevet</em>) was a club for defense against predators. The staff (<em>mish'enah</em>) was a long crook for guiding and rescuing sheep. Both instruments of the shepherd's care bring comfort – God both protects and guides.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Host Metaphor (Verses 5-6)</h4>

    <p><strong>"Thou preparest a table before me in the presence of mine enemies"</strong> (verse 5) – The imagery shifts to God as generous host. In ancient Near Eastern culture, to share a meal meant covenant relationship and protection. God provides abundant hospitality even while enemies threaten – demonstrating His power to protect and His commitment to bless.</p>

    <p><strong>"Thou anointest my head with oil"</strong> (verse 5) – Anointing honored special guests. Olive oil soothed sun-parched skin and signified joy and celebration. God doesn't merely provide necessities but lavishes honor and refreshment on His people.</p>

    <p><strong>"My cup runneth over"</strong> (verse 5) – Not just full, but overflowing (<em>revayah</em>). This speaks to God's abundant, excessive generosity – more than sufficient, more than expected.</p>

    <p><strong>"Surely goodness and mercy shall follow me all the days of my life"</strong> (verse 6) – The Hebrew <em>tov vachesed</em> ("goodness and covenant love") will <em>pursue</em> the psalmist. The verb <em>radaph</em> suggests active pursuit – God's blessings chase after His people. This continues "all the days of my life" – from now until death.</p>

    <p><strong>"And I will dwell in the house of the LORD for ever"</strong> (verse 6) – The ultimate confidence: eternal residence in God's presence. Whether understood as temple worship in this life or heavenly dwelling in the next, the psalmist's hope terminates in unending communion with God.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">David's Pastoral Background</h4>

    <p>If David authored this psalm (as the superscription indicates), his firsthand experience as a shepherd in Bethlehem's fields informs every image. He had protected sheep from lions and bears (1 Samuel 17:34-37), led them through dangerous terrain, and knew the shepherd's heart. Yet he also knew what it meant to be shepherded by God – through exile, persecution by Saul, personal failure, and restoration.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological and Christological Significance</h4>

    <p>Psalm 23 establishes several enduring theological truths:</p>

    <ol>
        <li><strong>God's personal care</strong>: The LORD knows and tends each individual within His flock</li>
        <li><strong>Sufficient provision</strong>: God supplies all needs according to His wisdom</li>
        <li><strong>Faithful guidance</strong>: God leads in paths that reflect His righteous character</li>
        <li><strong>Protective presence</strong>: God's companionship in danger brings courage</li>
        <li><strong>Abundant blessing</strong>: God gives not merely enough but more than enough</li>
        <li><strong>Eternal hope</strong>: God's care extends beyond this life into eternity</li>
    </ol>

    <p>The New Testament reveals the ultimate fulfillment in Jesus Christ, who declared "I am the good shepherd" (John 10:11, 14). He is the shepherd who "giveth his life for the sheep," who knows His own and is known by them, and who promises that no one can snatch His sheep from His hand (John 10:28-29). Hebrews 13:20 calls Him "that great shepherd of the sheep," and 1 Peter 2:25 identifies Him as "the Shepherd and Bishop of your souls."</p>

    <p>For believers facing the valley of death's shadow – whether literal death, devastating loss, chronic suffering, or spiritual darkness – Psalm 23 offers the comfort that has sustained God's people for three millennia: "Thou art with me." In the end, the psalm's power rests not in the beauty of its poetry or the familiarity of its words, but in the character of the Shepherd it proclaims.</p>
    """

    # John 3 - Born Again, God So Loved the World
    if book == "John" and chapter == 3:
        return """
    <p><strong>John 3</strong> contains some of the most memorable and theologically profound verses in Scripture, including the famous John 3:16 – "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life." This chapter records Jesus' nighttime conversation with Nicodemus about spiritual rebirth and presents the gospel message in its clearest, most concise form.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Nicodemus: The Seeker in the Night (Verses 1-21)</h4>

    <p>Nicodemus is introduced as "a man of the Pharisees" and "a ruler of the Jews" (verse 1), making him a member of the Sanhedrin, the Jewish ruling council. He comes to Jesus "by night" – perhaps to avoid public scrutiny, or symbolizing his spiritual darkness seeking the light. He addresses Jesus respectfully as "Rabbi" and acknowledges Him as "a teacher come from God," evidenced by His miraculous signs (verse 2).</p>

    <p><strong>The New Birth (Verses 3-8)</strong></p>

    <p>Jesus' response is startling and direct: "Verily, verily, I say unto thee, Except a man be born again, he cannot see the kingdom of God" (verse 3). The phrase "born again" translates Greek <em>gennēthē anōthen</em>, which can mean either "born again" or "born from above." Both meanings are significant – salvation requires both a second birth and a birth originating from God.</p>

    <p>Nicodemus misunderstands, thinking of physical rebirth (verse 4), but Jesus clarifies: "Except a man be born of water and of the Spirit, he cannot enter into the kingdom of God" (verse 5). The interpretation of "water and Spirit" has been debated:</p>

    <ul>
        <li><strong>Natural and spiritual birth</strong>: "Water" = physical birth, "Spirit" = spiritual birth</li>
        <li><strong>Ezekiel's prophecy</strong>: Referring to Ezekiel 36:25-27 where God promises cleansing water and a new spirit</li>
        <li><strong>Baptism and Spirit</strong>: Christian baptism and Holy Spirit regeneration</li>
        <li><strong>Word and Spirit</strong>: The cleansing word of God (John 15:3; Ephesians 5:26) and the Spirit's work</li>
    </ul>

    <p>Jesus distinguishes between physical and spiritual generation: "That which is born of the flesh is flesh; and that which is born of the Spirit is spirit" (verse 6). Human effort cannot produce spiritual life – only the Spirit can regenerate.</p>

    <p>The wind metaphor in verses 7-8 illustrates the Spirit's sovereignty: "The wind bloweth where it listeth, and thou hearest the sound thereof, but canst not tell whence it cometh, and whither it goeth: so is every one that is born of the Spirit." The same Greek word <em>pneuma</em> means both "wind" and "spirit." Like wind, the Spirit's work is real but mysterious, sovereign but evident in its effects.</p>

    <p><strong>The Bronze Serpent Typology (Verses 14-15)</strong></p>

    <p>Jesus refers to Numbers 21:4-9, where Moses lifted up a bronze serpent in the wilderness. Israelites dying from serpent bites were healed by looking at the bronze serpent on the pole. Similarly, "even so must the Son of man be lifted up: That whosoever believeth in him should not perish, but have eternal life" (verses 14-15).</p>

    <p>This is the first explicit reference in John's Gospel to Jesus' crucifixion ("lifted up"). The parallel is profound:</p>

    <ul>
        <li>Both involve being lifted up on a pole/cross</li>
        <li>Both require simple faith (looking/believing)</li>
        <li>Both offer salvation from death</li>
        <li>Both demonstrate God's provision for desperate need</li>
    </ul>

    <p><strong>John 3:16-17: The Gospel in Miniature</strong></p>

    <p>Martin Luther called John 3:16 "the gospel in miniature" or "the Bible in a nutshell." It contains the essential elements of the Christian message:</p>

    <ul>
        <li><strong>God's character</strong>: "For God so loved" – divine love as motivation</li>
        <li><strong>Love's scope</strong>: "the world" – universal offer, not limited to Israel</li>
        <li><strong>Love's cost</strong>: "he gave his only begotten Son" – the supreme sacrifice</li>
        <li><strong>Salvation's condition</strong>: "that whosoever believeth in him" – faith, not works</li>
        <li><strong>Alternative destinies</strong>: "should not perish, but have everlasting life" – two eternal outcomes</li>
    </ul>

    <p>Verse 17 clarifies God's intent: "For God sent not his Son into the world to condemn the world; but that the world through him might be saved." Jesus' first coming was for salvation, not judgment (though judgment results from rejecting Him, verses 18-19).</p>

    <p><strong>Light and Darkness (Verses 19-21)</strong></p>

    <p>Jesus explains why some reject the light: "And this is the condemnation, that light is come into the world, and men loved darkness rather than light, because their deeds were evil" (verse 19). The problem isn't intellectual but moral – people prefer darkness because it hides their evil deeds. "For every one that doeth evil hateth the light, neither cometh to the light, lest his deeds should be reproved" (verse 20). Conversely, "he that doeth truth cometh to the light, that his deeds may be made manifest, that they are wrought in God" (verse 21).</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">John the Baptist's Final Testimony (Verses 22-36)</h4>

    <p>The chapter concludes with John the Baptist's gracious response to his decreasing prominence as Jesus' ministry grows. When his disciples express concern about Jesus' increasing popularity (verses 25-26), John responds with humility and joy:</p>

    <p><strong>"He must increase, but I must decrease"</strong> (verse 30) – This is the proper attitude of every believer and minister: Christ must have preeminence.</p>

    <p>John's final testimony (verses 31-36) includes profound Christological affirmations:</p>

    <ul>
        <li><strong>Christ's origin</strong>: "He that cometh from above is above all" (verse 31)</li>
        <li><strong>Christ's testimony</strong>: He speaks what He has seen and heard (verse 32)</li>
        <li><strong>God's authentication</strong>: "He whom God hath sent speaketh the words of God: for God giveth not the Spirit by measure unto him" (verse 34)</li>
        <li><strong>The Father's love</strong>: "The Father loveth the Son, and hath given all things into his hand" (verse 35)</li>
        <li><strong>Eternal consequences</strong>: "He that believeth on the Son hath everlasting life: and he that believeth not the Son shall not see life; but the wrath of God abideth on him" (verse 36)</li>
    </ul>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>John 3 establishes essential Christian doctrines:</p>

    <ol>
        <li><strong>Necessity of regeneration</strong>: No one enters God's kingdom without spiritual rebirth</li>
        <li><strong>Sovereignty of the Spirit</strong>: Salvation is God's work, not human achievement</li>
        <li><strong>Centrality of the cross</strong>: Christ must be "lifted up" for salvation</li>
        <li><strong>Universality of God's love</strong>: The gospel extends to "the world," not just one nation</li>
        <li><strong>Exclusivity of Christ</strong>: Eternal life comes only through faith in God's Son</li>
        <li><strong>Human responsibility</strong>: People must believe or face condemnation</li>
        <li><strong>Moral dimension of unbelief</strong>: Rejection of Christ is moral, not merely intellectual</li>
    </ol>

    <p>Nicodemus appears twice more in John's Gospel – defending Jesus before the Sanhedrin (7:50-51) and helping Joseph of Arimathea bury Jesus (19:39). These references suggest he eventually became a secret disciple, demonstrating that even a hesitant seeker in the night can find the light of the world.</p>
    """

    # Romans 8 - No Condemnation
    if book == "Romans" and chapter == 8:
        return """
    <p><strong>Romans 8</strong> is often considered the pinnacle of Paul's theological exposition in Romans, presenting the Christian life empowered by the Holy Spirit and secured by God's unchangeable love. After establishing human sinfulness (1:18-3:20), justification by faith (3:21-5:21), sanctification and the struggle with sin (6:1-7:25), Paul now presents the glorious reality of life in the Spirit.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">No Condemnation for Those in Christ (Verses 1-4)</h4>

    <p>The chapter opens with one of Scripture's most comforting declarations: "There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the Spirit" (verse 1). The word "therefore" connects to chapter 7's struggle with indwelling sin. Despite ongoing moral struggle, believers face "no condemnation" (<em>ouden katakrima</em>) – no judicial verdict of guilt, no punishment, no separation from God.</p>

    <p>Why? "For the law of the Spirit of life in Christ Jesus hath made me free from the law of sin and death" (verse 2). A new <em>principle</em> or <em>power</em> ("law") operates in believers – the Spirit's life-giving power liberates from sin and death's enslaving power.</p>

    <p>Verses 3-4 explain the theological basis: "For what the law could not do, in that it was weak through the flesh, God sending his own Son in the likeness of sinful flesh, and for sin, condemned sin in the flesh: That the righteousness of the law might be fulfilled in us, who walk not after the flesh, but after the Spirit." The Law couldn't save because human weakness prevented obedience. So God sent His Son "in the likeness of sinful flesh" (truly human yet without sin) to condemn sin through His death, enabling the Law's righteous requirement to be fulfilled in Spirit-empowered believers.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Life in the Spirit vs. Life in the Flesh (Verses 5-11)</h4>

    <p>Paul contrasts two ways of life:</p>

    <ul>
        <li><strong>Those "after the flesh"</strong>: Mind the things of the flesh, hostile to God, cannot please God, headed toward death (verses 5-8)</li>
        <li><strong>Those "after the Spirit"</strong>: Mind the things of the Spirit, subject to God's law, pleasing to God, possess spiritual life (verses 5-6, 9)</li>
    </ul>

    <p>"But ye are not in the flesh, but in the Spirit, if so be that the Spirit of God dwell in you" (verse 9). The presence of the Spirit is the defining mark of believers. "Now if any man have not the Spirit of Christ, he is none of his" – not a Christian at all.</p>

    <p>Verses 10-11 present resurrection hope: Though the body is dead because of sin, the Spirit gives life. And "if the Spirit of him that raised up Jesus from the dead dwell in you, he that raised up Christ from the dead shall also quicken your mortal bodies by his Spirit that dwelleth in you" (verse 11). The same Spirit who raised Jesus will resurrect believers.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Sons of God Led by the Spirit (Verses 12-17)</h4>

    <p>Paul describes the believer's relationship to God as adoption: "For ye have not received the spirit of bondage again to fear; but ye have received the Spirit of adoption, whereby we cry, Abba, Father" (verse 15). The Spirit enables intimate address to God as "Abba" (Aramaic for "Father" or "Daddy"), the same term Jesus used (Mark 14:36).</p>

    <p>"The Spirit itself beareth witness with our spirit, that we are the children of God" (verse 16) – internal assurance that we belong to God.</p>

    <p>"And if children, then heirs; heirs of God, and joint-heirs with Christ; if so be that we suffer with him, that we may be also glorified together" (verse 17). As God's children, believers are heirs of all God's promises, sharing Christ's inheritance. But heirship includes suffering before glory – a crucial connection Paul develops next.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Present Suffering and Future Glory (Verses 18-25)</h4>

    <p>"For I reckon that the sufferings of this present time are not worthy to be compared with the glory which shall be revealed in us" (verse 18). Paul doesn't minimize suffering but puts it in eternal perspective – future glory far outweighs present pain.</p>

    <p>Remarkably, "the whole creation groaneth and travaileth in pain together until now" (verse 22), subjected to futility because of human sin (verse 20), awaiting "the glorious liberty of the children of God" (verse 21). Creation itself will be liberated when God's children are fully revealed.</p>

    <p>Meanwhile, "we ourselves groan within ourselves, waiting for the adoption, to wit, the redemption of our body" (verse 23). Christians experience the Spirit as <em>firstfruits</em> – the initial installment guaranteeing full harvest. We await complete adoption: bodily resurrection.</p>

    <p>"For we are saved by hope" (verse 24) – not yet possessing what we hope for, but confidently waiting.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Spirit's Help in Prayer (Verses 26-27)</h4>

    <p>In our weakness, "the Spirit itself maketh intercession for us with groanings which cannot be uttered" (verse 26). When we don't know how to pray, the Spirit intercedes according to God's will (verse 27). This is profound comfort – our inadequate prayers are perfected by the Spirit's intercession.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Golden Chain of Salvation (Verses 28-30)</h4>

    <p>"And we know that all things work together for good to them that love God, to them who are the called according to his purpose" (verse 28). Not that all things <em>are</em> good, but God works all things <em>together</em> for good for His people.</p>

    <p>Verses 29-30 present salvation's unbreakable chain:</p>

    <ol>
        <li><strong>Foreknew</strong>: God knew His people beforehand in intimate, electing love</li>
        <li><strong>Predestined</strong>: Predetermined to be conformed to Christ's image</li>
        <li><strong>Called</strong>: Effectually summoned to salvation</li>
        <li><strong>Justified</strong>: Declared righteous through Christ</li>
        <li><strong>Glorified</strong>: Past tense for future event – so certain it's as good as done</li>
    </ol>

    <p>Those God foreknew will certainly be glorified – no one drops out of this chain.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Triumph of God's Love (Verses 31-39)</h4>

    <p>Paul concludes with a magnificent doxology of rhetorical questions celebrating believers' security:</p>

    <p><strong>"If God be for us, who can be against us?"</strong> (verse 31) – If the Almighty is our ally, no enemy can prevail.</p>

    <p><strong>"He that spared not his own Son, but delivered him up for us all, how shall he not with him also freely give us all things?"</strong> (verse 32) – God gave the greatest gift (His Son); He'll certainly give lesser gifts.</p>

    <p><strong>"Who shall lay any thing to the charge of God's elect?"</strong> (verse 33) – No accusation stands since "It is God that justifieth."</p>

    <p><strong>"Who is he that condemneth?"</strong> (verse 34) – No condemnation is possible since Christ died, rose, and intercedes for us.</p>

    <p><strong>"Who shall separate us from the love of Christ?"</strong> (verse 35) – Paul lists seven potential separators: tribulation, distress, persecution, famine, nakedness, peril, sword. These were real experiences for early Christians (verse 36 quotes Psalm 44:22). Yet "in all these things we are more than conquerors through him that loved us" (verse 37). Not merely conquerors but <em>hyper-conquerors</em> (<em>hypernikōmen</em>).</p>

    <p>The chapter crescendos with Paul's absolute conviction (verses 38-39): "For I am persuaded, that neither death, nor life, nor angels, nor principalities, nor powers, nor things present, nor things to come, Nor height, nor depth, nor any other creature, shall be able to separate us from the love of God, which is in Christ Jesus our Lord."</p>

    <p>Ten potential separators – nothing in all creation can sever believers from God's love in Christ. This is the Christian's unshakeable confidence.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>Romans 8 establishes crucial doctrines:</p>

    <ol>
        <li><strong>Justification's permanence</strong>: No condemnation for those in Christ</li>
        <li><strong>The Spirit's indwelling</strong>: Defining mark of Christians</li>
        <li><strong>Adoption into God's family</strong>: Believers are children and heirs</li>
        <li><strong>Suffering as path to glory</strong>: Present pain doesn't negate future hope</li>
        <li><strong>Creation's redemption</strong>: Cosmic restoration coming</li>
        <li><strong>Divine sovereignty in salvation</strong>: God's purpose guarantees completion</li>
        <li><strong>Eternal security</strong>: Nothing can separate believers from God's love</li>
    </ol>

    <p>For Christians facing suffering, doubt, or spiritual attack, Romans 8 provides rock-solid assurance: God is for us, Christ intercedes for us, the Spirit helps us, and nothing can separate us from divine love. This is the gospel's triumph song.</p>
    """

    # 1 Corinthians 13 - The Love Chapter
    if book == "1 Corinthians" and chapter == 13:
        return """
    <p><strong>1 Corinthians 13</strong>, often called "the Love Chapter," is one of the most eloquent and beloved passages in all of Scripture. Frequently read at weddings, this chapter actually addresses a church wracked by division, pride, and spiritual immaturity. Paul interrupts his discussion of spiritual gifts (chapters 12-14) to present love as "a more excellent way" (12:31) – the indispensable foundation for all Christian life and ministry.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Supremacy of Love (Verses 1-3)</h4>

    <p>Paul begins with three hyperbolic contrasts showing that even the most spectacular spiritual achievements are worthless without love:</p>

    <p><strong>Eloquence without love is noise</strong> (verse 1): "Though I speak with the tongues of men and of angels, and have not charity, I am become as sounding brass, or a tinkling cymbal." The Greek word <em>agapē</em> (translated "charity" in KJV, "love" in modern versions) denotes self-giving, sacrificial love – not mere emotion or attraction. Without this love, even supernatural eloquence becomes irritating noise – like the clanging brass gongs and cymbals used in pagan worship at Corinth.</p>

    <p><strong>Spiritual gifts without love are nothing</strong> (verse 2): "And though I have the gift of prophecy, and understand all mysteries, and all knowledge; and though I have all faith, so that I could remove mountains, and have not charity, I am nothing." Prophecy, supernatural knowledge, even mountain-moving faith (cf. Matthew 17:20) – all amount to zero without love. The most impressive spiritual powers become spiritually bankrupt when divorced from love.</p>

    <p><strong>Sacrifice without love gains nothing</strong> (verse 3): "And though I bestow all my goods to feed the poor, and though I give my body to be burned, and have not charity, it profiteth me nothing." Even extreme acts of generosity (total divestment of possessions) and ultimate martyrdom (self-immolation) yield no spiritual profit without love as motivation. This is startling – even good deeds done without love are spiritually worthless.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Character of Love (Verses 4-7)</h4>

    <p>Having established love's supremacy, Paul defines love not abstractly but practically, through fifteen specific characteristics (primarily verbs, not adjectives – love is active, not passive). These qualities directly address the Corinthians' specific problems:</p>

    <p><strong>What love does</strong>:</p>
    <ul>
        <li><strong>"Charity suffereth long"</strong> – Patient endurance under provocation (the Corinthians were quick to take offense)</li>
        <li><strong>"is kind"</strong> – Actively benevolent and gracious (Greek <em>chrēsteuomai</em>, sharing root with Christ)</li>
        <li><strong>"rejoiceth not in iniquity, but rejoiceth in the truth"</strong> – Takes no pleasure in others' failures but celebrates truth and righteousness</li>
        <li><strong>"Beareth all things"</strong> – Covers or protects (either bears up under difficulty or covers others' faults)</li>
        <li><strong>"believeth all things"</strong> – Trusts, gives benefit of doubt, doesn't assume the worst</li>
        <li><strong>"hopeth all things"</strong> – Remains optimistic about people and circumstances</li>
        <li><strong>"endureth all things"</strong> – Perseveres under pressure without giving up</li>
    </ul>

    <p><strong>What love doesn't do</strong>:</p>
    <ul>
        <li><strong>"envieth not"</strong> – No jealousy over others' blessings or advantages (a major Corinthian problem)</li>
        <li><strong>"vaunteth not itself"</strong> – Doesn't boast or brag (addressed to a boastful church: 1:29, 3:21, 4:7)</li>
        <li><strong>"is not puffed up"</strong> – Not arrogant or inflated with pride (Corinth's cardinal sin: 4:6, 18-19, 5:2, 8:1)</li>
        <li><strong>"doth not behave itself unseemly"</strong> – Not rude, disgraceful, or shameful (cf. their disorderly worship: 11:2-34, 14:40)</li>
        <li><strong>"seeketh not her own"</strong> – Doesn't insist on its own way (vs. their selfish individualism: 10:24, 33)</li>
        <li><strong>"is not easily provoked"</strong> – Not irritable or quick-tempered (literally "not sharp" or "bitter")</li>
        <li><strong>"thinketh no evil"</strong> – Doesn't keep a mental ledger of wrongs suffered</li>
    </ul>

    <p>This description is both personally convicting and remarkably applicable to the Corinthians' specific issues: pride (puffed up), factionalism (envy), litigation (easily provoked), disorder (unseemly behavior), and division over spiritual gifts.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Permanence of Love (Verses 8-13)</h4>

    <p>"Charity never faileth" (verse 8) – Love never falls, never fails, never ends. It's eternal, unlike spiritual gifts which are temporary:</p>

    <ul>
        <li><strong>Prophecies</strong> will be done away</li>
        <li><strong>Tongues</strong> will cease</li>
        <li><strong>Knowledge</strong> will vanish away</li>
    </ul>

    <p>Why? Because "we know in part, and we prophesy in part. But when that which is perfect is come, then that which is in part shall be done away" (verses 9-10). Current spiritual knowledge is fragmentary, like a child's understanding (verse 11) or seeing through a dim, ancient bronze mirror (verse 12). But when Christ returns and we see Him face to face, partial knowledge gives way to complete understanding.</p>

    <p>The famous verse 12 captures this beautifully: "For now we see through a glass, darkly; but then face to face: now I know in part; but then shall I know even as also I am known." Corinthian bronze mirrors gave only dim, unclear reflections compared to seeing directly. Similarly, our current knowledge is clouded compared to the crystal clarity we'll have in eternity. Yet even now, God knows us fully – and then we'll know as we are known.</p>

    <p>The chapter concludes with the triad: "And now abideth faith, hope, charity, these three; but the greatest of these is charity" (verse 13). These three Christian virtues endure into eternity (unlike temporary gifts), but love is supreme because:</p>

    <ul>
        <li>Faith will become sight (2 Corinthians 5:7)</li>
        <li>Hope will be realized (Romans 8:24-25)</li>
        <li>Love will continue forever in perfected form</li>
    </ul>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Context in 1 Corinthians</h4>

    <p>Chapter 13 sits strategically between Paul's discussion of the body of Christ and spiritual gifts (chapter 12) and proper use of tongues and prophecy (chapter 14). The Corinthians were obsessed with showy spiritual gifts, especially tongues, creating competition and division. Paul demonstrates that without love, even the most spectacular gifts are spiritually worthless.</p>

    <p>This addresses their core problem: immaturity (3:1-3). Despite possessing spiritual gifts (1:7), they remained "carnal, and walk as men" (3:3) – characterized by envy, strife, and divisions. True spiritual maturity isn't measured by miraculous abilities but by Christlike love.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological and Practical Significance</h4>

    <p>First Corinthians 13 establishes several crucial truths:</p>

    <ol>
        <li><strong>Love as the supreme virtue</strong>: Greater than faith or hope, more important than any spiritual gift</li>
        <li><strong>Love as proof of maturity</strong>: The defining mark of spiritual growth</li>
        <li><strong>Love as God's nature</strong>: This chapter describes not merely ideal human behavior but God's character revealed in Christ (1 John 4:8, 16)</li>
        <li><strong>Love as eternally enduring</strong>: The one thing that survives into eternity unchanged</li>
        <li><strong>Love as practical, not sentimental</strong>: Defined by actions and attitudes, not feelings</li>
    </ol>

    <p>When read carefully, this chapter becomes Christ's autobiography. Every characteristic Paul lists describes Jesus perfectly: patient, kind, not envious or boastful or proud, never rude or self-seeking, not easily angered, keeping no record of wrongs, never delighting in evil but rejoicing with truth, always protecting, trusting, hoping, and persevering.</p>

    <p>The challenge for readers – whether Corinthian or contemporary – is to embody this love. Not through human effort alone (which inevitably fails) but through the Spirit's transforming work (Galatians 5:22 lists love as the Spirit's first fruit). This isn't a checklist for self-improvement but a portrait of Christ to which believers are being conformed (Romans 8:29).</p>

    <p>In a church culture (then and now) often enamored with gifts, experiences, knowledge, and achievements, 1 Corinthians 13 redirects focus to what truly matters: love. For "if I have not love, I am nothing... I gain nothing." But with love as the foundation, all spiritual gifts find their proper purpose: building up the body of Christ in unity and maturity.</p>
    """

    # John 1 - The Word Became Flesh
    if book == "John" and chapter == 1:
        return """
    <p><strong>John 1</strong> opens with one of the most theologically profound prologues in Scripture. Unlike the synoptic Gospels which begin with genealogies (Matthew, Luke) or John the Baptist's ministry (Mark), John's Gospel begins before creation itself: "In the beginning was the Word." This chapter establishes Christ's deity, preexistence, incarnation, and mission, while introducing key witnesses to His identity.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Eternal Word (Verses 1-5)</h4>

    <p><strong>"In the beginning was the Word"</strong> (verse 1) – These opening words echo Genesis 1:1 ("In the beginning God created"), but with a crucial difference: Genesis describes creation's beginning; John describes what already existed before creation. The imperfect tense "was" (<em>ēn</em>) indicates continuous existence – the Word had no beginning but eternally was.</p>

    <p><strong>"The Word was with God, and the Word was God"</strong> (verse 1) – Two staggering affirmations in one breath. The Word (<em>ho logos</em>) existed in relationship with God (Greek <em>pros ton theon</em> suggests "face to face with God") while simultaneously being God Himself. This establishes both distinction (the Word is with God) and identity (the Word is God) – foundational to Trinitarian theology.</p>

    <p>Why "Word" (<em>logos</em>)? This term was rich with meaning for both Jewish and Greek audiences:</p>
    <ul>
        <li>For Jews: God's creative word in Genesis ("God said"), the personified Wisdom of Proverbs 8, the Torah as God's revealed word</li>
        <li>For Greeks: The rational principle ordering the cosmos, the mediator between transcendent deity and material creation</li>
        <li>For John: The perfect term to express how God communicates and reveals Himself – through Christ</li>
    </ul>

    <p><strong>"All things were made by him"</strong> (verse 3) – The Word is creator, not creature. "Without him was not any thing made that was made" – absolute statement excluding no created thing. This refutes any notion that Christ is a created being. If it was created, Christ created it.</p>

    <p><strong>"In him was life; and the life was the light of men"</strong> (verse 4) – The Word possesses life inherently, not derivatively. This life illuminates humanity – spiritual, moral, intellectual enlightenment. Yet "the darkness comprehended it not" (verse 5) – darkness neither overcame nor understood the light. This introduces the Gospel's light/darkness motif (3:19-21, 8:12, 12:35-36, 12:46).</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Witness of John the Baptist (Verses 6-8, 15, 19-34)</h4>

    <p>John the Baptist appears as the first witness to Christ's identity. "There was a man sent from God, whose name was John" (verse 6) – in stark contrast to the Word who eternally was, John has a beginning; he was sent. His mission? "To bear witness of the Light, that all men through him might believe" (verse 7). John himself wasn't the light but a pointer to the light.</p>

    <p>When religious authorities interrogate John (verses 19-28), he consistently deflects attention from himself to Christ:</p>
    <ul>
        <li>"I am not the Christ" (verse 20)</li>
        <li>Not Elijah or "that prophet" (verse 21)</li>
        <li>Just "the voice of one crying in the wilderness" (verse 23, quoting Isaiah 40:3)</li>
        <li>"I baptize with water: but there standeth one among you, whom ye know not... whose shoe's latchet I am not worthy to unloose" (verses 26-27)</li>
    </ul>

    <p>The next day, seeing Jesus approach, John declares: "Behold the Lamb of God, which taketh away the sin of the world" (verse 29). This title combines Isaiah's suffering servant (Isaiah 53:7) with the Passover lamb (Exodus 12) – Jesus is the sacrifice who removes (Greek <em>airō</em>: lifts up and carries away) the world's sin.</p>

    <p>John testifies to witnessing the Spirit descend "like a dove" and remain on Jesus (verses 32-33) – the divine authentication. His conclusion: "I saw, and bare record that this is the Son of God" (verse 34).</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Incarnation (Verses 9-14)</h4>

    <p>Verses 9-11 describe humanity's tragic response to the Light: "He was in the world, and the world was made by him, and the world knew him not. He came unto his own, and his own received him not." The Creator entered His creation, yet creation failed to recognize Him. He came to His own people (Israel), yet they rejected Him.</p>

    <p>But not all rejected Him: "But as many as received him, to them gave he power to become the sons of God, even to them that believe on his name" (verse 12). Those who receive Christ gain the right/authority (<em>exousia</em>) to become God's children – not through natural descent or human will, but through divine birth (verse 13). This is spiritual regeneration, being "born again" (cf. John 3:3-8).</p>

    <p>Verse 14 presents the incarnation with stunning simplicity: "And the Word was made flesh, and dwelt among us." The eternal, divine Word became <em>sarx</em> (flesh) – fully human. "Dwelt" (<em>eskēnōsen</em>) literally means "tabernacled" – the Word pitched His tent among humanity, evoking God's presence in the wilderness tabernacle (Exodus 40:34-35).</p>

    <p>"And we beheld his glory, the glory as of the only begotten of the Father, full of grace and truth" (verse 14). Eyewitnesses saw divine glory revealed in human flesh – the same glory that filled the tabernacle now manifest in Christ. "Only begotten" (<em>monogenēs</em>) emphasizes Jesus' unique relationship to the Father – not "only created" but "uniquely generated," eternally begotten.</p>

    <p>"Full of grace and truth" – grace (<em>charis</em>) is God's unmerited favor; truth (<em>alētheia</em>) is reality, faithfulness, reliability. These aren't opposing qualities but complementary expressions of God's character. Verse 17 contrasts Moses' law (which came through a mediator) with Jesus' grace and truth (which came directly through Him).</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The First Disciples (Verses 35-51)</h4>

    <p>John recounts Jesus' first disciples being called:</p>

    <ol>
        <li><strong>Two of John's disciples</strong> (likely Andrew and John the author) follow Jesus after hearing John's testimony. They spend the day with Him (verse 39) – transformative hours that changed their lives.</li>
        <li><strong>Andrew</strong> finds his brother Simon and declares: "We have found the Messias" (verse 41). Jesus renames Simon "Cephas" (Peter, "rock") – significant since ancient names conveyed identity and destiny.</li>
        <li><strong>Philip</strong> is directly called by Jesus (verse 43) and immediately seeks Nathanael.</li>
        <li><strong>Nathanael</strong> is skeptical ("Can there any good thing come out of Nazareth?" – verse 46) until Jesus demonstrates supernatural knowledge. Jesus sees Nathanael "under the fig tree" before Philip called him (verse 48) – possibly seeing not just physically but into Nathanael's heart/character. Convinced, Nathanael confesses: "Rabbi, thou art the Son of God; thou art the King of Israel" (verse 49).</li>
    </ol>

    <p>Jesus promises Nathanael (and all disciples): "Hereafter ye shall see heaven open, and the angels of God ascending and descending upon the Son of man" (verse 51). This alludes to Jacob's ladder (Genesis 28:12) with a crucial difference: angels ascend and descend not on a ladder but on the Son of Man – Jesus Himself is the connection between heaven and earth, the mediator between God and humanity.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>John 1 establishes foundational Christian theology:</p>

    <ol>
        <li><strong>Christ's full deity</strong>: The Word was God, creator of all things, possessing eternal life</li>
        <li><strong>Christ's full humanity</strong>: The Word became flesh and dwelt among us</li>
        <li><strong>Christ's preexistence</strong>: He existed before creation, eternally with the Father</li>
        <li><strong>Christ's creative power</strong>: All things were made through Him</li>
        <li><strong>Christ's revelatory role</strong>: He makes the invisible God known (verse 18)</li>
        <li><strong>Christ's saving work</strong>: The Lamb who takes away the world's sin</li>
        <li><strong>Spiritual rebirth</strong>: Becoming God's children through believing in Christ's name</li>
        <li><strong>Incarnation's purpose</strong>: To reveal God's glory, grace, and truth</li>
    </ol>

    <p>This chapter answers the fundamental question: Who is Jesus? The answer reverberates through every verse: He is the eternal Word, Creator God, life and light of humanity, the incarnate revelation of the Father, the Lamb of God, the Son of God, the King of Israel, the Messiah. John's Gospel will spend the next 20 chapters unpacking these magnificent opening declarations, showing through signs, teachings, and ultimately death and resurrection that Jesus is indeed who John 1 proclaims Him to be.</p>
    """

    # Matthew 5 - The Sermon on the Mount (Beatitudes)
    if book == "Matthew" and chapter == 5:
        return """
    <p><strong>Matthew 5</strong> opens the Sermon on the Mount (chapters 5-7), Jesus' longest and most famous discourse. Delivered early in His ministry to crowds gathering on a Galilean hillside, this sermon presents the ethics and character of the kingdom of heaven – a radical reorientation of values that contrasts sharply with both prevailing religious practice and secular culture.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Beatitudes (Verses 3-12)</h4>

    <p>Jesus begins with nine "blessed" statements (Greek <em>makarios</em>, meaning "happy," "fortunate," or "flourishing"). Unlike worldly values that celebrate power, wealth, and self-assertion, Jesus pronounces blessing on the seemingly unfortunate:</p>

    <ol>
        <li><strong>"Blessed are the poor in spirit: for theirs is the kingdom of heaven"</strong> (verse 3) – Not economically poor but spiritually bankrupt, recognizing their need for God. These possess the kingdom because they know they can't earn it.</li>

        <li><strong>"Blessed are they that mourn: for they shall be comforted"</strong> (verse 4) – Those who grieve over sin (their own and the world's) will receive God's comfort. This isn't mere sadness but godly sorrow (2 Corinthians 7:10).</li>

        <li><strong>"Blessed are the meek: for they shall inherit the earth"</strong> (verse 5) – Meekness isn't weakness but strength under control (cf. Moses in Numbers 12:3). The meek don't grasp for power yet will inherit everything (cf. Psalm 37:11).</li>

        <li><strong>"Blessed are they which do hunger and thirst after righteousness: for they shall be filled"</strong> (verse 6) – Intense craving for right standing with God and righteous living will be satisfied. This isn't casual interest but desperate need.</li>

        <li><strong>"Blessed are the merciful: for they shall obtain mercy"</strong> (verse 7) – Those who show compassion to others will receive God's mercy (cf. Matthew 6:14-15, 18:23-35).</li>

        <li><strong>"Blessed are the pure in heart: for they shall see God"</strong> (verse 8) – Moral purity, undivided loyalty, single-minded devotion to God leads to knowing Him intimately. This references Psalm 24:3-4 and anticipates seeing God face-to-face (1 John 3:2).</li>

        <li><strong>"Blessed are the peacemakers: for they shall be called the children of God"</strong> (verse 9) – Not merely peacekeepers but those actively reconciling others to God and each other. This reflects God's character (Romans 5:1, 2 Corinthians 5:18-19).</li>

        <li><strong>"Blessed are they which are persecuted for righteousness' sake: for theirs is the kingdom of heaven"</strong> (verse 10) – Suffering for doing right (not for being obnoxious) brings blessing. Persecution confirms kingdom citizenship.</li>

        <li><strong>"Blessed are ye, when men shall revile you, and persecute you, and shall say all manner of evil against you falsely, for my sake"</strong> (verses 11-12) – Direct application to disciples: expect insults, persecution, and slander. Yet "rejoice, and be exceeding glad: for great is your reward in heaven: for so persecuted they the prophets which were before you." Persecution places believers in the prophets' company.</li>
    </ol>

    <p>These Beatitudes describe kingdom citizens – not steps to salvation but characteristics of those who've received God's grace. They're counter-cultural then and now, reversing worldly values.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Salt and Light (Verses 13-16)</h4>

    <p>Jesus gives disciples two metaphors defining their mission:</p>

    <p><strong>"Ye are the salt of the earth"</strong> (verse 13) – Salt preserves, flavors, and in ancient times was used in purification and covenant-making (Leviticus 2:13). Disciples preserve society from moral decay, add "flavor" to bland existence, and represent God's covenant. But "if the salt have lost his savour... it is thenceforth good for nothing, but to be cast out, and to be trodden under foot of men." Tasteless salt is useless – so are ineffective disciples.</p>

    <p><strong>"Ye are the light of the world"</strong> (verse 14) – Echoing Jesus' own identity (John 8:12), disciples reflect His light. "A city that is set on an hill cannot be hid" (verse 14) – visibility is inevitable, not optional. "Neither do men light a candle, and put it under a bushel, but on a candlestick; and it giveth light unto all that are in the house" (verse 15) – lamps exist to illuminate, not be hidden.</p>

    <p>"Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven" (verse 16) – Good works should be visible (contrary to modern privatized faith) but the goal is glorifying God, not self-promotion.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Christ and the Law (Verses 17-20)</h4>

    <p>Anticipating objections that His teaching undermines the Law, Jesus clarifies: "Think not that I am come to destroy the law, or the prophets: I am not come to destroy, but to fulfil" (verse 17). He doesn't abolish but completes, accomplishes, and brings to full meaning.</p>

    <p>"For verily I say unto you, Till heaven and earth pass, one jot or one tittle shall in no wise pass from the law, till all be fulfilled" (verse 18) – The smallest Hebrew letter (yod, <em>jot</em>) and the tiniest stroke distinguishing letters (<em>tittle</em>) remain valid. The Law's moral principles are eternally binding.</p>

    <p>"For I say unto you, That except your righteousness shall exceed the righteousness of the scribes and Pharisees, ye shall in no case enter into the kingdom of heaven" (verse 20) – Shocking statement since Pharisees were renowned for scrupulous law-keeping. But Jesus demands heart transformation, not mere external compliance. The following "antitheses" ("Ye have heard... but I say") demonstrate this deeper righteousness.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">The Antitheses: Deeper Righteousness (Verses 21-48)</h4>

    <p>Jesus presents six contrasts between superficial law-keeping and heart righteousness:</p>

    <p><strong>1. Murder and Anger (verses 21-26)</strong> – The Law forbids murder, but Jesus condemns the anger that produces it. "Whosoever is angry with his brother without a cause shall be in danger of the judgment" (verse 22). Insulting language ("Raca," "fool") reveals murderous hearts. Therefore, reconcile with offended brothers before offering worship (verses 23-24) – relationship trumps ritual.</p>

    <p><strong>2. Adultery and Lust (verses 27-30)</strong> – The Law forbids adultery, but Jesus condemns lustful looking: "Whosoever looketh on a woman to lust after her hath committed adultery with her already in his heart" (verse 28). The solution is radical: "If thy right eye offend thee, pluck it out... if thy right hand offend thee, cut it off" (verses 29-30). Jesus isn't commanding literal self-mutilation but emphasizing that nothing is too precious to sacrifice to avoid sin.</p>

    <p><strong>3. Divorce (verses 31-32)</strong> – The Law permitted divorce (Deuteronomy 24:1), but Jesus restricts it to cases of sexual immorality (<em>porneia</em>). Easy divorce treating spouses as disposable violates God's design for marriage permanence (cf. Matthew 19:3-9).</p>

    <p><strong>4. Oaths (verses 33-37)</strong> – The Law required keeping oaths, but Jesus prohibits oath-taking entirely: "Swear not at all" (verse 34). Complex oath formulae created loopholes allowing people to break promises while technically complying. Instead: "let your communication be, Yea, yea; Nay, nay: for whatsoever is more than these cometh of evil" (verse 37). Simple honesty eliminates need for oaths.</p>

    <p><strong>5. Retaliation (verses 38-42)</strong> – The Law limited vengeance to proportional justice ("eye for eye, tooth for tooth" – Exodus 21:24), but Jesus commands non-retaliation: "resist not evil: but whosoever shall smite thee on thy right cheek, turn to him the other also" (verse 39). Being sued for your coat? Give your cloak too (verse 40). Forced to carry a load one mile? Go two (verse 41). Give to those who ask (verse 42). This isn't endorsing injustice but refusing to perpetuate cycles of revenge.</p>

    <p><strong>6. Love for Enemies (verses 43-48)</strong> – The Law commanded loving neighbors, but rabbis inferred hating enemies was permissible. Jesus commands: "Love your enemies, bless them that curse you, do good to them that hate you, and pray for them which despitefully use you, and persecute you" (verse 44). Why? "That ye may be the children of your Father which is in heaven: for he maketh his sun to rise on the evil and on the good, and sendeth rain on the just and on the unjust" (verse 45). God shows indiscriminate kindness – His children should too.</p>

    <p>"For if ye love them which love you, what reward have ye? do not even the publicans the same?" (verse 46). Reciprocal love is common; enemy love is divine. "Be ye therefore perfect, even as your Father which is in heaven is perfect" (verse 48) – the goal is God's own perfect character, complete love that includes even enemies.</p>

    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>

    <p>Matthew 5 establishes crucial truths:</p>

    <ol>
        <li><strong>Kingdom values reverse worldly values</strong>: The blessed are the poor in spirit, mourners, meek, persecuted</li>
        <li><strong>Disciples are world-impacting</strong>: Salt and light influencing society</li>
        <li><strong>Christ fulfills the Law</strong>: He doesn't abolish but brings to completion</li>
        <li><strong>Righteousness is internal</strong>: Heart transformation, not mere external compliance</li>
        <li><strong>God's standard is perfection</strong>: Like the Father Himself</li>
        <li><strong>Love extends to enemies</strong>: Reflecting God's indiscriminate grace</li>
    </ol>

    <p>This chapter confronts both legalism (external rule-keeping) and antinomianism (lawless grace). Jesus raises the bar impossibly high – who can achieve this righteousness? No one through human effort. This drives us to the gospel: Christ perfectly fulfilled these demands, and through faith in Him, His righteousness becomes ours (2 Corinthians 5:21). The Sermon isn't a ladder to climb but a mirror revealing our need for grace and a portrait of Christ-likeness to which the Spirit conforms believers.</p>
    """

    # Simulated chapter overview for other chapters
    themes = [get_theme(v.text.lower()) for v in verses[:5]]  # Sample themes from the first few verses
    unique_themes = list(set(themes))[:3]  # Get up to 3 unique themes

    chapter_type = get_chapter_type(book, chapter)
    time_period = get_time_period(book)
    historical_context = get_historical_context(book)

    overview = f"""
    <p><strong>{book} {chapter}</strong> is a {chapter_type} chapter in the {get_testament_for_book(book)} that explores themes of {', '.join(unique_themes)}.
    Written during {time_period}, this chapter should be understood within its historical context: {historical_context}</p>

    <p>The chapter can be divided into several sections:</p>

    <ol>
        <li><strong>Verses 1-{min(5, len(verses))}</strong>: Introduction and setting the context</li>
        {'<li><strong>Verses 6-' + str(min(12, len(verses))) + '</strong>: Development of key themes</li>' if len(verses) > 5 else ''}
        {'<li><strong>Verses 13-' + str(min(20, len(verses))) + '</strong>: Central message and teachings</li>' if len(verses) > 12 else ''}
        {'<li><strong>Verses ' + str(min(21, len(verses))) + '-' + str(len(verses)) + '</strong>: Conclusion and application</li>' if len(verses) > 20 else ''}
    </ol>

    <p>This chapter is significant because it {get_chapter_significance(book, chapter)}.
    When studying this passage, it's important to consider both its immediate context within {book}
    and its broader place in the scriptural canon.</p>
    """

    return overview


def parse_cross_reference(ref_string):
    """Parse a cross-reference string like 'John 1:1-3' or 'Genesis 3:15' into structured data"""
    try:
        # Handle verse ranges like "John 1:1-3" or simple refs like "John 1:1"
        match = re.match(r'(.+?)\s+(\d+):(\d+)(?:-(\d+))?', ref_string.strip())
        if not match:
            return None

        ref_book = match.group(1).strip()
        ref_chapter = int(match.group(2))
        ref_verse_start = int(match.group(3))
        ref_verse_end = int(match.group(4)) if match.group(4) else ref_verse_start

        # Create the display text and URL
        if ref_verse_end > ref_verse_start:
            text = f"{ref_book} {ref_chapter}:{ref_verse_start}-{ref_verse_end}"
        else:
            text = f"{ref_book} {ref_chapter}:{ref_verse_start}"

        url = f"/book/{ref_book}/chapter/{ref_chapter}#verse-{ref_verse_start}"

        return {
            "text": text,
            "url": url,
            "context": None  # Will be populated from theme or left empty
        }
    except Exception as e:
        print(f"Error parsing cross-reference '{ref_string}': {e}")
        return None


def generate_cross_references(book, chapter, verse, verse_text):
    """Generate cross-references for a verse using Scofield commentary when available"""

    # First, try to get cross-references from Scofield commentary
    if book in scofield_commentary:
        if str(chapter) in scofield_commentary[book]:
            if str(verse) in scofield_commentary[book][str(chapter)]:
                verse_data = scofield_commentary[book][str(chapter)][str(verse)]
                if "cross_references" in verse_data and verse_data["cross_references"]:
                    # Parse the Scofield cross-references
                    references = []
                    for ref_string in verse_data["cross_references"][:4]:  # Limit to 4 references
                        parsed_ref = parse_cross_reference(ref_string)
                        if parsed_ref:
                            references.append(parsed_ref)

                    if references:
                        return references

    # Fall back to thematic cross-references if no Scofield data
    # Dictionary of sample cross-references by theme with actual verse texts
    theme_references = {
        "salvation": [
            {"book": "John", "chapter": 3, "verse": 16, "context": "God's love and salvation", "verse_text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."},
            {"book": "Romans", "chapter": 10, "verse": 9, "context": "Confession and belief for salvation", "verse_text": "That if thou shalt confess with thy mouth the Lord Jesus, and shalt believe in thine heart that God hath raised him from the dead, thou shalt be saved."},
            {"book": "Ephesians", "chapter": 2, "verse": 8, "context": "Salvation by grace through faith", "verse_text": "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God:"}
        ],
        "faith": [
            {"book": "Hebrews", "chapter": 11, "verse": 1, "context": "Definition of faith", "verse_text": "Now faith is the substance of things hoped for, the evidence of things not seen."},
            {"book": "James", "chapter": 2, "verse": 17, "context": "Faith and works", "verse_text": "Even so faith, if it hath not works, is dead, being alone."},
            {"book": "Romans", "chapter": 1, "verse": 17, "context": "The righteous shall live by faith", "verse_text": "For therein is the righteousness of God revealed from faith to faith: as it is written, The just shall live by faith."}
        ],
        "love": [
            {"book": "1 Corinthians", "chapter": 13, "verse": 4, "context": "Characteristics of love", "verse_text": "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up,"},
            {"book": "1 John", "chapter": 4, "verse": 8, "context": "God is love", "verse_text": "He that loveth not knoweth not God; for God is love."},
            {"book": "John", "chapter": 15, "verse": 13, "context": "Greatest form of love", "verse_text": "Greater love hath no man than this, that a man lay down his life for his friends."}
        ],
        "judgment": [
            {"book": "Matthew", "chapter": 25, "verse": 31, "context": "Final judgment", "verse_text": "When the Son of man shall come in his glory, and all the holy angels with him, then shall he sit upon the throne of his glory:"},
            {"book": "Romans", "chapter": 2, "verse": 1, "context": "Judging others", "verse_text": "Therefore thou art inexcusable, O man, whosoever thou art that judgest: for wherein thou judgest another, thou condemnest thyself; for thou that judgest doest the same things."},
            {"book": "Revelation", "chapter": 20, "verse": 12, "context": "Judgment according to deeds", "verse_text": "And I saw the dead, small and great, stand before God; and the books were opened: and another book was opened, which is the book of life: and the dead were judged out of those things which were written in the books, according to their works."}
        ],
        "creation": [
            {"book": "Genesis", "chapter": 1, "verse": 1, "context": "Creation of heavens and earth", "verse_text": "In the beginning God created the heaven and the earth."},
            {"book": "Psalm", "chapter": 19, "verse": 1, "context": "Heavens declare God's glory", "verse_text": "The heavens declare the glory of God; and the firmament sheweth his handywork."},
            {"book": "Colossians", "chapter": 1, "verse": 16, "context": "All things created through Christ", "verse_text": "For by him were all things created, that are in heaven, and that are in earth, visible and invisible, whether they be thrones, or dominions, or principalities, or powers: all things were created by him, and for him:"}
        ],
        "prayer": [
            {"book": "Matthew", "chapter": 6, "verse": 9, "context": "The Lord's Prayer", "verse_text": "After this manner therefore pray ye: Our Father which art in heaven, Hallowed be thy name."},
            {"book": "1 Thessalonians", "chapter": 5, "verse": 17, "context": "Pray without ceasing", "verse_text": "Pray without ceasing."},
            {"book": "James", "chapter": 5, "verse": 16, "context": "Prayer of the righteous", "verse_text": "Confess your faults one to another, and pray one for another, that ye may be healed. The effectual fervent prayer of a righteous man availeth much."}
        ],
        "wisdom": [
            {"book": "Proverbs", "chapter": 9, "verse": 10, "context": "Beginning of wisdom", "verse_text": "The fear of the Lord is the beginning of wisdom: and the knowledge of the holy is understanding."},
            {"book": "James", "chapter": 1, "verse": 5, "context": "Ask God for wisdom", "verse_text": "If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."},
            {"book": "1 Corinthians", "chapter": 1, "verse": 25, "context": "God's wisdom vs man's", "verse_text": "Because the foolishness of God is wiser than men; and the weakness of God is stronger than men."}
        ],
        "hope": [
            {"book": "Romans", "chapter": 15, "verse": 13, "context": "God of hope", "verse_text": "Now the God of hope fill you with all joy and peace in believing, that ye may abound in hope, through the power of the Holy Ghost."},
            {"book": "Hebrews", "chapter": 6, "verse": 19, "context": "Hope as anchor", "verse_text": "Which hope we have as an anchor of the soul, both sure and stedfast, and which entereth into that within the veil;"},
            {"book": "1 Peter", "chapter": 1, "verse": 3, "context": "Living hope", "verse_text": "Blessed be the God and Father of our Lord Jesus Christ, which according to his abundant mercy hath begotten us again unto a lively hope by the resurrection of Jesus Christ from the dead,"}
        ],
        "peace": [
            {"book": "John", "chapter": 14, "verse": 27, "context": "Christ's peace", "verse_text": "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid."},
            {"book": "Philippians", "chapter": 4, "verse": 7, "context": "Peace that passes understanding", "verse_text": "And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus."},
            {"book": "Isaiah", "chapter": 26, "verse": 3, "context": "Perfect peace", "verse_text": "Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee."}
        ]
    }

    # Identify themes in the verse text
    verse_themes = []
    for theme in theme_references.keys():
        if theme in verse_text or random.random() < 0.2:  # Randomly include some themes
            verse_themes.append(theme)

    # If no themes match, pick a random theme
    if not verse_themes:
        verse_themes = [random.choice(list(theme_references.keys()))]

    # Get references for identified themes
    references = []
    for theme in verse_themes[:2]:  # Limit to two themes
        theme_refs = theme_references[theme]
        for ref in random.sample(theme_refs, min(2, len(theme_refs))):
            # Skip self-references
            if ref["book"] == book and ref["chapter"] == chapter and ref["verse"] == verse:
                continue

            references.append({
                "text": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "url": f"/book/{ref['book']}/chapter/{ref['chapter']}#verse-{ref['verse']}",
                "context": ref["context"],
                "verse_text": ref["verse_text"]
            })

    # Ensure we have at least one reference
    if not references:
        references.append({
            "text": "John 1:1",
            "url": "/book/John/chapter/1#verse-1",
            "context": "Related teaching",
            "verse_text": "In the beginning was the Word, and the Word was with God, and the Word was God."
        })

    return references


def get_theme(text):
    """Extract a thematic element from text"""
    themes = [
        "redemption", "salvation", "faith", "obedience", "love",
        "judgment", "mercy", "grace", "wisdom", "creation",
        "covenant", "holiness", "righteousness", "truth", "hope",
        "sacrifice", "worship", "prayer", "discipleship", "fellowship"
    ]

    # First check if any themes appear directly in the text
    for theme in themes:
        if theme in text:
            return theme

    # Otherwise return a random theme
    return random.choice(themes)


def get_key_phrase(text):
    """Extract a key phrase from the text"""
    # Split the text into phrases
    phrases = text.replace(".", ". ").replace(";", "; ").replace(":", ": ").split()

    # Select a phrase of 3-5 words if the text is long enough
    if len(phrases) > 5:
        start = random.randint(0, len(phrases) - 5)
        length = random.randint(3, min(5, len(phrases) - start))
        return " ".join(phrases[start:start+length])
    else:
        # If text is short, just return a portion of it
        return text[:min(len(text), 30)]


def get_language_feature(text):
    """Identify a language feature"""
    features = [
        "metaphorical language", "symbolic imagery", "parallelism",
        "rhetorical questioning", "imperative form", "poetic structure",
        "narrative technique", "prophetic language", "didactic teaching",
        "pastoral guidance", "theological explanation", "eschatological reference"
    ]
    return random.choice(features)


def get_literary_device(text):
    """Identify a literary device"""
    devices = [
        "metaphor", "simile", "allusion", "personification", "hyperbole",
        "chiasm", "merism", "synecdoche", "parallelism", "inclusio",
        "rhetorical question", "allegory", "symbolic language", "irony"
    ]

    # Special case for Revelation text which is highly symbolic
    if "throne" in text.lower() or "lamb" in text.lower() or "seal" in text.lower():
        return "apocalyptic symbolism"

    return random.choice(devices)


def get_concept(text):
    """Identify a theological concept"""
    concepts = [
        "divine sovereignty", "human responsibility", "covenant faithfulness",
        "sacrificial atonement", "spiritual renewal", "moral obligation",
        "divine justice", "eschatological hope", "messianic expectation",
        "communal worship", "spiritual discipline", "ethical living",
        "divine revelation", "prophetic fulfillment", "kingdom ethics"
    ]
    return random.choice(concepts)


def get_cultural_element(text):
    """Identify a cultural element"""
    elements = [
        "religious practice", "social custom", "cultural tradition",
        "political structure", "economic system", "family relationship",
        "legal requirement", "worship ritual", "purity regulation",
        "agricultural reference", "military imagery", "architectural feature"
    ]
    return random.choice(elements)




def get_chapter_type(book, chapter):
    """Identify the type of chapter"""
    # Simplified mapping of books to primary genre
    book_genres = {
        # Torah
        "Genesis": "narrative",
        "Exodus": "narrative with legal sections",
        "Leviticus": "legal and ritual",
        "Numbers": "mixed narrative and legal",
        "Deuteronomy": "sermonic and legal",

        # Historical
        "Joshua": "historical narrative",
        "Judges": "cyclical narrative",
        "Ruth": "historical narrative",
        "1 Samuel": "biographical narrative",
        "2 Samuel": "biographical narrative",
        "1 Kings": "historical narrative",
        "2 Kings": "historical narrative",
        "1 Chronicles": "historical and genealogical",
        "2 Chronicles": "historical narrative",
        "Ezra": "historical narrative",
        "Nehemiah": "historical memoir",
        "Esther": "historical narrative",

        # Wisdom
        "Job": "wisdom dialogue",
        "Psalms": "poetic and liturgical",
        "Proverbs": "wisdom sayings",
        "Ecclesiastes": "philosophical reflection",
        "Song of Solomon": "poetic love song",

        # Prophetic
        "Isaiah": "prophetic oracle",
        "Jeremiah": "prophetic oracle",
        "Lamentations": "funeral dirge",
        "Ezekiel": "prophetic vision",
        "Daniel": "apocalyptic and narrative",
        "Hosea": "prophetic oracle",
        "Joel": "prophetic oracle",
        "Amos": "prophetic oracle",
        "Obadiah": "prophetic oracle",
        "Jonah": "prophetic narrative",
        "Micah": "prophetic oracle",
        "Nahum": "prophetic oracle",
        "Habakkuk": "prophetic dialogue",
        "Zephaniah": "prophetic oracle",
        "Haggai": "prophetic oracle",
        "Zechariah": "prophetic vision",
        "Malachi": "prophetic disputation",

        # Gospels
        "Matthew": "biographical gospel",
        "Mark": "action-oriented gospel",
        "Luke": "historical gospel",
        "John": "theological gospel",

        # Acts
        "Acts": "historical narrative",

        # Epistles
        "Romans": "theological epistle",
        "1 Corinthians": "pastoral epistle",
        "2 Corinthians": "apologetic epistle",
        "Galatians": "polemical epistle",
        "Ephesians": "theological epistle",
        "Philippians": "friendship epistle",
        "Colossians": "christological epistle",
        "1 Thessalonians": "eschatological epistle",
        "2 Thessalonians": "eschatological epistle",
        "1 Timothy": "pastoral epistle",
        "2 Timothy": "pastoral epistle",
        "Titus": "pastoral epistle",
        "Philemon": "personal epistle",
        "Hebrews": "homiletical epistle",
        "James": "wisdom epistle",
        "1 Peter": "pastoral epistle",
        "2 Peter": "polemical epistle",
        "1 John": "theological epistle",
        "2 John": "pastoral epistle",
        "3 John": "personal epistle",
        "Jude": "polemical epistle",

        # Apocalyptic
        "Revelation": "apocalyptic vision"
    }

    # Special cases for specific chapters
    special_chapters = {
        ("Genesis", 1): "creation account",
        ("Genesis", 3): "fall narrative",
        ("Exodus", 20): "legal covenant",
        ("Leviticus", 16): "ritual instruction",
        ("Deuteronomy", 28): "covenant blessing and curse",
        ("Joshua", 1): "commissioning narrative",
        ("Judges", 2): "paradigmatic narrative",
        ("1 Samuel", 16): "anointing narrative",
        ("2 Samuel", 7): "covenant narrative",
        ("Psalms", 1): "wisdom psalm",
        ("Psalms", 22): "lament psalm",
        ("Psalms", 23): "shepherd psalm",
        ("Psalms", 24): "royal psalm",
        ("Psalms", 25): "prayer psalm",
        ("Psalms", 26): "trust psalm",
        ("Psalms", 27): "hope psalm",
        ("Psalms", 28): "deliverance psalm",
        ("Psalms", 29): "praise psalm",
        ("Psalms", 30): "joy psalm",
        ("Psalms", 31): "suffering psalm",
        ("Psalms", 32): "wisdom psalm",
        ("Psalms", 33): "praise psalm",
        ("Psalms", 34): "praise psalm",
        ("Psalms", 35): "praise psalm",
        ("Psalms", 36): "praise psalm"
    }

def generate_chapter_overview(book, chapter, verses):
    """Generate an AI-powered overview of the entire chapter"""
    # Simulated chapter overview
    themes = [get_theme(v.text.lower()) for v in verses[:5]]  # Sample themes from the first few verses
    unique_themes = list(set(themes))[:3]  # Get up to 3 unique themes

    chapter_type = get_chapter_type(book, chapter)
    time_period = get_time_period(book)
    historical_context = get_historical_context(book)

    overview = f"""
    <p><strong>{book} {chapter}</strong> is a {chapter_type} chapter in the {get_testament_for_book(book)} that explores themes of {', '.join(unique_themes)}.
    Written during {time_period}, this chapter should be understood within its historical context: {historical_context}</p>

    <p>The chapter can be divided into several sections:</p>

    <ol>
        <li><strong>Verses 1-{min(5, len(verses))}</strong>: Introduction and setting the context</li>
        {'<li><strong>Verses 6-' + str(min(12, len(verses))) + '</strong>: Development of key themes</li>' if len(verses) > 5 else ''}
        {'<li><strong>Verses 13-' + str(min(20, len(verses))) + '</strong>: Central message and teachings</li>' if len(verses) > 12 else ''}
        {'<li><strong>Verses ' + str(min(21, len(verses))) + '-' + str(len(verses)) + '</strong>: Conclusion and application</li>' if len(verses) > 20 else ''}
    </ol>

    <p>This chapter is significant because it {get_chapter_significance(book, chapter)}.
    When studying this passage, it's important to consider both its immediate context within {book}
    and its broader place in the scriptural canon.</p>
    """

    return overview


def generate_cross_references(book, chapter, verse, verse_text):
    """Generate simulated cross-references for a verse"""
    # Dictionary of sample cross-references by theme
    theme_references = {
        "salvation": [
            {"book": "John", "chapter": 3, "verse": 16, "context": "God's love and salvation"},
            {"book": "Romans", "chapter": 10, "verse": 9, "context": "Confession and belief for salvation"},
            {"book": "Ephesians", "chapter": 2, "verse": 8, "context": "Salvation by grace through faith"}
        ],
        "faith": [
            {"book": "Hebrews", "chapter": 11, "verse": 1, "context": "Definition of faith"},
            {"book": "James", "chapter": 2, "verse": 17, "context": "Faith and works"},
            {"book": "Romans", "chapter": 1, "verse": 17, "context": "The righteous shall live by faith"}
        ],
        "love": [
            {"book": "1 Corinthians", "chapter": 13, "verse": 4, "context": "Characteristics of love"},
            {"book": "1 John", "chapter": 4, "verse": 8, "context": "God is love"},
            {"book": "John", "chapter": 15, "verse": 13, "context": "Greatest form of love"}
        ],
        "judgment": [
            {"book": "Matthew", "chapter": 25, "verse": 31, "context": "Final judgment"},
            {"book": "Romans", "chapter": 2, "verse": 1, "context": "Judging others"},
            {"book": "Revelation", "chapter": 20, "verse": 12, "context": "Judgment according to deeds"}
        ],
        "creation": [
            {"book": "Genesis", "chapter": 1, "verse": 1, "context": "Creation of heavens and earth"},
            {"book": "Psalm", "chapter": 19, "verse": 1, "context": "Heavens declare God's glory"},
            {"book": "Colossians", "chapter": 1, "verse": 16, "context": "All things created through Christ"}
        ]
    }

    # Identify themes in the verse text
    verse_themes = []
    for theme in theme_references.keys():
        if theme in verse_text or random.random() < 0.2:  # Randomly include some themes
            verse_themes.append(theme)

    # If no themes match, pick a random theme
    if not verse_themes:
        verse_themes = [random.choice(list(theme_references.keys()))]

    # Get references for identified themes
    references = []
    for theme in verse_themes[:2]:  # Limit to two themes
        theme_refs = theme_references[theme]
        for ref in random.sample(theme_refs, min(2, len(theme_refs))):
            # Skip self-references
            if ref["book"] == book and ref["chapter"] == chapter and ref["verse"] == verse:
                continue

            references.append({
                "text": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "url": f"/book/{ref['book']}/chapter/{ref['chapter']}#verse-{ref['verse']}",
                "context": ref["context"]
            })

    # Ensure we have at least one reference
    if not references:
        random_book = random.choice(["Matthew", "John", "Romans", "Psalms", "Proverbs"])
        references.append({
            "text": f"{random_book} 1:1",
            "url": f"/book/{random_book}/chapter/1#verse-1",
            "context": "Related teaching"
        })

    return references


def get_theme(text):
    """Extract a thematic element from text"""
    themes = [
        "redemption", "salvation", "faith", "obedience", "love",
        "judgment", "mercy", "grace", "wisdom", "creation",
        "covenant", "holiness", "righteousness", "truth", "hope",
        "sacrifice", "worship", "prayer", "discipleship", "fellowship"
    ]

    # First check if any themes appear directly in the text
    for theme in themes:
        if theme in text:
            return theme

    # Otherwise return a random theme
    return random.choice(themes)


def get_key_phrase(text):
    """Extract a key phrase from the text"""
    # Split the text into phrases
    phrases = text.replace(".", ". ").replace(";", "; ").replace(":", ": ").split()

    # Select a phrase of 3-5 words if the text is long enough
    if len(phrases) > 5:
        start = random.randint(0, len(phrases) - 5)
        length = random.randint(3, min(5, len(phrases) - start))
        return " ".join(phrases[start:start+length])
    else:
        # If text is short, just return a portion of it
        return text[:min(len(text), 30)]


def get_language_feature(text):
    """Identify a language feature"""
    features = [
        "metaphorical language", "symbolic imagery", "parallelism",
        "rhetorical questioning", "imperative form", "poetic structure",
        "narrative technique", "prophetic language", "didactic teaching",
        "pastoral guidance", "theological explanation", "eschatological reference"
    ]
    return random.choice(features)


def get_literary_device(text):
    """Identify a literary device"""
    devices = [
        "metaphor", "simile", "allusion", "personification", "hyperbole",
        "chiasm", "merism", "synecdoche", "parallelism", "inclusio",
        "rhetorical question", "allegory", "symbolic language", "irony"
    ]
    return random.choice(devices)


def get_concept(text):
    """Identify a theological concept"""
    concepts = [
        "divine sovereignty", "human responsibility", "covenant faithfulness",
        "sacrificial atonement", "spiritual renewal", "moral obligation",
        "divine justice", "eschatological hope", "messianic expectation",
        "communal worship", "spiritual discipline", "ethical living",
        "divine revelation", "prophetic fulfillment", "kingdom ethics"
    ]
    return random.choice(concepts)


def get_cultural_element(text):
    """Identify a cultural element"""
    elements = [
        "religious practice", "social custom", "cultural tradition",
        "political structure", "economic system", "family relationship",
        "legal requirement", "worship ritual", "purity regulation",
        "agricultural reference", "military imagery", "architectural feature"
    ]
    return random.choice(elements)


def get_time_period(book):
    """Return the historical time period for a book"""
    time_periods = {
        # Torah
        "Genesis": "the patriarchal period (c. 2000-1700 BCE)",
        "Exodus": "the Egyptian bondage and wilderness wandering (c. 1446-1406 BCE)",
        "Leviticus": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Numbers": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Deuteronomy": "the end of the wilderness wandering (c. 1406 BCE)",

        # Historical books
        "Joshua": "the conquest of Canaan (c. 1406-1375 BCE)",
        "Judges": "the pre-monarchic period (c. 1375-1050 BCE)",
        "Ruth": "the period of the Judges (c. 1100 BCE)",
        "1 Samuel": "the transition to monarchy (c. 1050-1010 BCE)",
        "2 Samuel": "David's reign (c. 1010-970 BCE)",
        "1 Kings": "Solomon's reign and the divided kingdom (c. 970-853 BCE)",
        "2 Kings": "the divided and exilic periods (c. 853-560 BCE)",
        "1 Chronicles": "the post-exilic reflection on David's reign (c. 430-400 BCE)",
        "2 Chronicles": "the post-exilic reflection on the monarchy (c. 430-400 BCE)",
        "Ezra": "the post-exilic return (c. 458-440 BCE)",
        "Nehemiah": "the rebuilding of Jerusalem (c. 445-420 BCE)",
        "Esther": "the Persian period (c. 483-473 BCE)",

        # Wisdom literature
        "Job": "the patriarchal period (literary composition later)",
        "Psalms": "various periods (c. 1000-400 BCE)",
        "Proverbs": "primarily Solomon's reign (c. 970-930 BCE)",
        "Ecclesiastes": "likely Solomon's reign (c. 970-930 BCE)",
        "Song of Solomon": "Solomon's reign (c. 970-930 BCE)",

        # Major Prophets
        "Isaiah": "the Assyrian and pre-exilic periods (c. 740-680 BCE)",
        "Jeremiah": "the final years of Judah and early exile (c. 627-580 BCE)",
        "Lamentations": "just after Jerusalem's fall (c. 586 BCE)",
        "Ezekiel": "the Babylonian exile (c. 593-570 BCE)",
        "Daniel": "the Babylonian and Persian periods (c. 605-530 BCE)",

        # Minor Prophets
        "Hosea": "the final years of the northern kingdom (c. 755-710 BCE)",
        "Joel": "possibly post-exilic period (uncertain date)",
        "Amos": "the prosperous period of Jeroboam II (c. 760-750 BCE)",
        "Obadiah": "possibly after Jerusalem's fall (c. 586 BCE)",
        "Jonah": "the Assyrian period (c. 780-750 BCE)",
        "Micah": "the late 8th century BCE (c. 735-700 BCE)",
        "Nahum": "shortly before Nineveh's fall (c. 630-610 BCE)",
        "Habakkuk": "the neo-Babylonian rise to power (c. 605-597 BCE)",
        "Zephaniah": "during Josiah's reign (c. 640-609 BCE)",
        "Haggai": "the early post-exilic period (c. 520 BCE)",
        "Zechariah": "the early post-exilic period (c. 520-480 BCE)",
        "Malachi": "the mid-5th century BCE (c. 460-430 BCE)",

        # Gospels and Acts
        "Matthew": "the late first century CE (c. 80-90 CE)",
        "Mark": "the mid first century CE (c. 65-70 CE)",
        "Luke": "the late first century CE (c. 80-85 CE)",
        "John": "the late first century CE (c. 90-95 CE)",
        "Acts": "the late first century CE (c. 80-85 CE)",

        # Pauline Epistles
        "Romans": "Paul's third missionary journey (c. 57 CE)",
        "1 Corinthians": "Paul's third missionary journey (c. 55 CE)",
        "2 Corinthians": "Paul's third missionary journey (c. 55-56 CE)",
        "Galatians": "either before or after the Jerusalem Council (c. 48-55 CE)",
        "Ephesians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Philippians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Colossians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "1 Thessalonians": "Paul's second missionary journey (c. 50-51 CE)",
        "2 Thessalonians": "shortly after 1 Thessalonians (c. 50-51 CE)",
        "1 Timothy": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "2 Timothy": "during Paul's second Roman imprisonment (c. 66-67 CE)",
        "Titus": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "Philemon": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Hebrews": "before Jerusalem's destruction (c. 60-70 CE)",

        # General Epistles
        "James": "the early church period (c. 45-50 CE)",
        "1 Peter": "during Nero's persecution (c. 62-64 CE)",
        "2 Peter": "shortly before Peter's death (c. 65-68 CE)",
        "1 John": "the late first century CE (c. 85-95 CE)",
        "2 John": "the late first century CE (c. 85-95 CE)",
        "3 John": "the late first century CE (c. 85-95 CE)",
        "Jude": "the late first century CE (c. 65-80 CE)",

        # Apocalyptic
        "Revelation": "the end of the first century CE (c. 95 CE)"
    }

    return time_periods.get(book, "the biblical period")


def get_historical_context(book):
    """Return historical context for a book"""
    historical_contexts = {
        # Torah
        "Genesis": "The ancient Near Eastern world was filled with competing creation narratives and flood stories.",
        "Exodus": "Egypt was the dominant superpower with a complex polytheistic religion and a god-king pharaoh.",
        "Leviticus": "The ritual systems addressed were designed to distinguish Israel from surrounding Canaanite practices.",
        "Numbers": "The wilderness journey occurred between Egypt's dominance and the Canaanite tribal systems.",
        "Deuteronomy": "Moses delivered these speeches as Israel prepared to enter a land filled with different Canaanite city-states.",

        # Historical books
        "Joshua": "Canaan was fragmented into city-states with various tribal alliances and religious practices.",
        "Judges": "Without central leadership, Israel faced constant threats from surrounding peoples like the Philistines and Midianites.",
        "Ruth": "During the tribal confederacy period, local customs and family laws were paramount for survival.",
        "1 Samuel": "Israel transitioned from tribal confederacy to monarchy while facing Philistine military pressure.",
        "2 Samuel": "David established Jerusalem as the capital during a time of regional power vacuum.",
        "1 Kings": "Solomon's reign represented Israel's golden age, with international trade and diplomatic relations.",
        "2 Kings": "The divided kingdoms faced threats from rising empires: Assyria and later Babylon.",
        "1 Chronicles": "Written after exile to reestablish national identity through connection to David's lineage.",
        "2 Chronicles": "Written to remind returning exiles of their temple-centered worship and Davidic heritage.",
        "Ezra": "The Persian Empire allowed religious freedom while maintaining political control.",
        "Nehemiah": "Persian authorities permitted Jerusalem's rebuilding under local leadership with imperial oversight.",
        "Esther": "Jews in diaspora faced both integration opportunities and threats within the vast Persian Empire.",

        # Wisdom literature
        "Job": "Ancient wisdom traditions often wrestled with the problem of suffering and divine justice.",
        "Psalms": "Temple worship utilized these compositions across various periods of Israel's history.",
        "Proverbs": "Ancient Near Eastern wisdom literature was common in royal courts for training officials.",
        "Ecclesiastes": "Royal wisdom reflections paralleled other ancient Near Eastern philosophical works.",
        "Song of Solomon": "Ancient Near Eastern love poetry often used agricultural and royal imagery.",

        # Major Prophets
        "Isaiah": "Addressed Judah during Assyria's rise, Babylon's threat, and anticipated restoration.",
        "Jeremiah": "Prophesied during Judah's final years as Babylon became the dominant power.",
        "Lamentations": "Written amid the devastating aftermath of Jerusalem's destruction by Babylon.",
        "Ezekiel": "Ministered to exiles in Babylon with visions of God's glory and future restoration.",
        "Daniel": "Demonstrates faithful living under foreign rule during the Babylonian and Persian empires.",

        # Minor Prophets
        "Hosea": "Israel faced imminent threat from Assyria while engaging in Canaanite religious syncretism.",
        "Joel": "Addressed a community devastated by natural disaster as a sign of divine judgment.",
        "Amos": "Economic prosperity masked serious social injustice and religious hypocrisy.",
        "Obadiah": "Edom's betrayal of Judah during Jerusalem's fall heightened ancient tribal hostilities.",
        "Jonah": "Nineveh was the capital of the feared Assyrian Empire, Israel's enemy.",
        "Micah": "Rural communities suffered while urban elites prospered during Assyria's regional dominance.",
        "Nahum": "Nineveh's anticipated fall would end a century of Assyrian oppression.",
        "Habakkuk": "Babylon's rise to power raised questions about God using pagan nations as instruments.",
        "Zephaniah": "Josiah's reforms occurred against the backdrop of Assyria's decline and Babylon's rise.",
        "Haggai": "Economic hardship and political uncertainty complicated the returning exiles' rebuilding efforts.",
        "Zechariah": "Persian support for temple rebuilding came with continued imperial control.",
        "Malachi": "Post-exilic community struggled with religious apathy and intermarriage challenges.",

        # Gospels and Acts
        "Matthew": "Written when Christianity was separating from Judaism following Jerusalem's destruction.",
        "Mark": "Composed during or just after Nero's persecution when eyewitnesses were disappearing.",
        "Luke": "Written when Christians needed to understand their place in the Roman world.",
        "John": "Addressed late first-century challenges from both Judaism and emerging Gnostic thought.",
        "Acts": "Chronicles Christianity's spread across the Roman Empire despite official and unofficial opposition.",

        # Pauline Epistles
        "Romans": "Christians in Rome navigated tensions between Jewish and Gentile believers under imperial watch.",
        "1 Corinthians": "The church existed in a prosperous, cosmopolitan, morally permissive Roman colony.",
        "2 Corinthians": "Paul defended his apostleship against challenges in a culture valuing rhetorical prowess.",
        "Galatians": "Gentile believers faced pressure to adopt Jewish practices for full acceptance.",
        "Ephesians": "Ephesus was a major center of pagan worship, particularly of the goddess Artemis.",
        "Philippians": "The church in this Roman colony maintained partnership with Paul despite his imprisonment.",
        "Colossians": "Syncretistic philosophy threatened to compromise the sufficiency of Christ.",
        "1 Thessalonians": "New believers faced persecution from both Jewish opposition and pagan neighbors.",
        "2 Thessalonians": "Confusion about Christ's return caused some believers to abandon daily responsibilities.",
        "1 Timothy": "False teaching in Ephesus required organizational and doctrinal clarification.",
        "2 Timothy": "Paul's final imprisonment occurred during intensified persecution under Nero.",
        "Titus": "Cretan culture's negative reputation required special attention to Christian character.",
        "Philemon": "Roman slavery was addressed through Christian principles without direct confrontation.",
        "Hebrews": "Jewish Christians faced persecution pressure to return to Judaism's legal protections.",

        # General Epistles
        "James": "Early Jewish believers struggled to live out faith amid economic hardship and discrimination.",
        "1 Peter": "Christians throughout Asia Minor faced growing social hostility and potential persecution.",
        "2 Peter": "False teachers exploited Christian freedom for immoral purposes and denied divine judgment.",
        "1 John": "Early Gnostic ideas threatened the understanding of Christ's incarnation and redemption.",
        "2 John": "Itinerant teachers required careful vetting as false teaching spread through hospitality networks.",
        "3 John": "Power struggles in local churches complicated missionary support and fellowship.",
        "Jude": "Libertine teaching undermined moral standards by distorting grace.",

        # Apocalyptic
        "Revelation": "Emperor worship intensified under Domitian, pressuring Christians to compromise their exclusive loyalty to Christ."
    }

    return historical_contexts.get(book, "This text emerged within the historical context of ancient religious traditions.")


def get_chapter_type(book, chapter):
    """Identify the type of chapter"""
    # Simplified mapping of books to primary genre
    book_genres = {
        # Torah
        "Genesis": "narrative",
        "Exodus": "narrative with legal sections",
        "Leviticus": "legal and ritual",
        "Numbers": "mixed narrative and legal",
        "Deuteronomy": "sermonic and legal",

        # Historical
        "Joshua": "historical narrative",
        "Judges": "cyclical narrative",
        "Ruth": "historical narrative",
        "1 Samuel": "biographical narrative",
        "2 Samuel": "biographical narrative",
        "1 Kings": "historical narrative",
        "2 Kings": "historical narrative",
        "1 Chronicles": "historical and genealogical",
        "2 Chronicles": "historical narrative",
        "Ezra": "historical narrative",
        "Nehemiah": "historical memoir",
        "Esther": "historical narrative",

        # Wisdom
        "Job": "wisdom dialogue",
        "Psalms": "poetic and liturgical",
        "Proverbs": "wisdom sayings",
        "Ecclesiastes": "philosophical reflection",
        "Song of Solomon": "poetic love song",

        # Prophetic
        "Isaiah": "prophetic oracle",
        "Jeremiah": "prophetic oracle",
        "Lamentations": "funeral dirge",
        "Ezekiel": "prophetic vision",
        "Daniel": "apocalyptic and narrative",
        "Hosea": "prophetic oracle",
        "Joel": "prophetic oracle",
        "Amos": "prophetic oracle",
        "Obadiah": "prophetic oracle",
        "Jonah": "prophetic narrative",
        "Micah": "prophetic oracle",
        "Nahum": "prophetic oracle",
        "Habakkuk": "prophetic dialogue",
        "Zephaniah": "prophetic oracle",
        "Haggai": "prophetic oracle",
        "Zechariah": "prophetic vision",
        "Malachi": "prophetic disputation",

        # Gospels
        "Matthew": "biographical gospel",
        "Mark": "action-oriented gospel",
        "Luke": "historical gospel",
        "John": "theological gospel",

        # Acts
        "Acts": "historical narrative",

        # Epistles
        "Romans": "theological epistle",
        "1 Corinthians": "pastoral epistle",
        "2 Corinthians": "apologetic epistle",
        "Galatians": "polemical epistle",
        "Ephesians": "theological epistle",
        "Philippians": "friendship epistle",
        "Colossians": "christological epistle",
        "1 Thessalonians": "eschatological epistle",
        "2 Thessalonians": "eschatological epistle",
        "1 Timothy": "pastoral epistle",
        "2 Timothy": "pastoral epistle",
        "Titus": "pastoral epistle",
        "Philemon": "personal epistle",
        "Hebrews": "homiletical epistle",
        "James": "wisdom epistle",
        "1 Peter": "pastoral epistle",
        "2 Peter": "polemical epistle",
        "1 John": "theological epistle",
        "2 John": "pastoral epistle",
        "3 John": "personal epistle",
        "Jude": "polemical epistle",

        # Apocalyptic
        "Revelation": "apocalyptic vision"
    }

    # Special cases for specific chapters
    special_chapters = {
        ("Genesis", 1): "creation account",
        ("Genesis", 3): "fall narrative",
        ("Exodus", 20): "legal covenant",
        ("Leviticus", 16): "ritual instruction",
        ("Deuteronomy", 28): "covenant blessing and curse",
        ("Joshua", 1): "commissioning narrative",
        ("Judges", 2): "paradigmatic narrative",
        ("1 Samuel", 16): "anointing narrative",
        ("2 Samuel", 7): "covenant narrative",
        ("Psalms", 1): "wisdom psalm",
        ("Psalms", 22): "lament psalm",
        ("Psalms", 23): "trust psalm",
        ("Isaiah", 53): "suffering servant oracle",
        ("Matthew", 5): "ethical teaching",
        ("John", 1): "theological prologue",
        ("Romans", 8): "theological exposition",
        ("1 Corinthians", 13): "hymn to love",
        ("Revelation", 1): "apocalyptic vision"
    }

    # Check if this is a special chapter
    if (book, chapter) in special_chapters:
        return special_chapters[(book, chapter)]

    # Otherwise return the general book genre
    return book_genres.get(book, "scriptural")


def get_testament_for_book(book):
    """Determine if a book is in the Old or New Testament"""
    old_testament = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi"
    ]

    return "Old Testament" if book in old_testament else "New Testament"


def get_chapter_significance(book, chapter):
    """Generate significance explanation for a chapter"""
    significance_templates = [
        "provides essential context for understanding God's covenant relationship with His people",
        "reveals key aspects of God's character through divine actions and declarations",
        "establishes important theological principles that resonate throughout Scripture",
        "addresses timeless questions about faith, suffering, and divine purpose",
        "offers practical wisdom for godly living in a fallen world",
        "demonstrates God's faithfulness despite human unfaithfulness",
        "contributes to the biblical metanarrative of redemption",
        "foreshadows Christ's work through typology and prophetic elements",
        "illustrates divine judgment and mercy in response to human actions",
        "provides guidance for worship and spiritual devotion"
    ]

    # Special significance for specific chapters
    special_significance = {
        ("Genesis", 1): "establishes the foundational doctrine of creation and God's sovereignty",
        ("Genesis", 3): "introduces the fall of humanity and the need for redemption",
        ("Exodus", 20): "presents the Decalogue (Ten Commandments) as the cornerstone of biblical law",
        ("Leviticus", 16): "details the Day of Atonement ritual that prefigures Christ's sacrificial work",
        ("Isaiah", 53): "provides the clearest Old Testament prophecy of the Messiah's suffering",
        ("Matthew", 5): "presents Jesus' ethical teaching in the Sermon on the Mount",
        ("John", 3): "contains the essential gospel message of salvation by faith",
        ("Romans", 8): "articulates the doctrines of justification, sanctification, and glorification",
        ("1 Corinthians", 15): "defends the resurrection as central to Christian faith",
        ("Revelation", 1): "introduces apocalyptic visions that reveal Christ's ultimate victory and sovereignty"
    }

    if (book, chapter) in special_significance:
        return special_significance[(book, chapter)]
    else:
        return random.choice(significance_templates)


def generate_book_commentary(book, chapters):
    """Generate comprehensive commentary for an entire book"""
    # Get basic book information
    testament = get_testament_for_book(book)
    time_period = get_time_period(book)
    genre = get_book_genre(book)

    # Generate tags based on themes and genre
    tags = generate_book_tags(book, genre)

    # Generate introduction based on book
    introduction = generate_book_introduction(book)

    # Generate historical context
    historical_context = generate_historical_context(book)

    # Generate literary features
    literary_features = generate_literary_features(book, genre)

    # Generate key themes
    themes = generate_book_themes(book)

    # Generate theological significance
    theological_significance = generate_theological_significance(book)

    # Generate contemporary application
    application = generate_book_application(book)

    # Generate key highlights from the book
    highlights = generate_book_highlights(book, chapters)

    # Generate book outline
    outline = generate_book_outline(book, chapters)

    # Generate cross-references to other books
    cross_references = generate_book_cross_references(book)

    # Generate chapter summaries with key verses
    chapter_summaries = generate_chapter_summaries(book, chapters)

    return {
        "testament": testament,
        "time_period": time_period,
        "genre": genre,
        "tags": tags,
        "introduction": introduction,
        "historical_context": historical_context,
        "literary_features": literary_features,
        "themes": themes,
        "theological_significance": theological_significance,
        "application": application,
        "highlights": highlights,
        "outline": outline,
        "cross_references": cross_references,
        "chapter_summaries": chapter_summaries
    }


def generate_book_application(book):
    """Generate contemporary application for a book"""
    # Simple implementation for now
    applications = {
        "Exodus": """
        <p>Exodus provides enduring insights that apply to contemporary life:</p>

        <h3>Divine Deliverance</h3>
        <p>The exodus story reminds us that God sees and responds to the suffering of His people. In a world where many experience various forms of bondage—whether addiction, oppression, or spiritual darkness—Exodus testifies that God is a deliverer. The pattern of redemption from Egypt foreshadows Christ's greater deliverance from sin, offering hope to those in seemingly impossible situations and affirming that liberation comes through divine intervention, not merely human effort.</p>

        <h3>Identity Formation</h3>
        <p>Israel's transformation from slaves to "a kingdom of priests and a holy nation" (Exodus 19:6) parallels the Christian's new identity in Christ. This theme addresses contemporary questions of personal identity, reminding believers that they are defined not by past bondage or present circumstances but by covenant relationship with God. The corporate identity of Israel also speaks to the church's collective identity as God's people set apart for divine purposes in a secular world.</p>

        <h3>Law and Grace</h3>
        <p>The law given at Sinai provides ethical guidance while demonstrating humanity's need for grace. This balanced perspective challenges both legalism (reducing faith to rule-keeping) and antinomianism (disregarding moral standards). The law in Exodus shows that freedom is not lawlessness but rather the liberty to live according to God's design. For Christians, the moral principles underlying the law continue to provide wisdom for ethical decision-making, even as we recognize Christ as the law's fulfillment.</p>

        <h3>Divine Presence</h3>
        <p>The tabernacle established the profound truth that God desires to dwell among His people. In an age of spiritual disconnection and isolation, this theme reminds us that God is not distant but seeks communion with humanity. The elaborate preparations for God's presence in Exodus highlight both divine holiness and divine nearness. For Christians, this anticipates the incarnation ("the Word became flesh and tabernacled among us") and the indwelling of the Holy Spirit, assuring believers of God's abiding presence through all circumstances.</p>
        """,

        "Genesis": """
        <p>Genesis provides enduring insights that apply to contemporary life:</p>

        <h3>Human Identity and Purpose</h3>
        <p>In a culture often confused about human identity and value, Genesis reminds us that all people bear God's image (Genesis 1:26-27). This foundational truth addresses issues of racism, sexism, abortion, euthanasia, and other ethical concerns by establishing the inherent dignity of every human life. It also counters contemporary nihilism by affirming that human life has divinely-given purpose and meaning.</p>

        <h3>Environmental Stewardship</h3>
        <p>Genesis establishes humans as God's representatives who are to "rule over" creation while simultaneously being charged to "work and take care of" the garden (Genesis 1:28, 2:15). This balanced perspective avoids both exploitative domination and nature worship, providing a theological foundation for responsible environmental stewardship that honors the Creator by caring for His creation.</p>

        <h3>Marriage and Family</h3>
        <p>The creation account establishes marriage as a divine institution uniting male and female in a complementary relationship (Genesis 2:18-25). This foundational teaching informs Christian understanding of gender, sexuality, marriage, and family life. Genesis also honestly portrays family dysfunction, showing the consequences of polygamy, favoritism, deception, and rivalry, providing negative examples that warn against similar patterns.</p>

        <h3>Faith Amid Trials</h3>
        <p>The patriarchs' journeys demonstrate faith amid uncertainty, disappointment, and waiting. Abraham's willingness to leave homeland security for an unknown destination (Genesis 12:1-4) and to trust God's promise despite apparent impossibility (Genesis 15:6) exemplifies the faith journey. Joseph's declaration that "God meant it for good" despite his brothers' evil intentions (Genesis 50:20) provides a profound theology of suffering that acknowledges pain while trusting divine purpose.</p>
        """
    }

    # Default application based on testament and genre
    if book not in applications:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        if testament == "Old Testament":
            return """
            <p>This book provides valuable insights for contemporary application:</p>

            <h3>Understanding God's Character</h3>
            <p>The book reveals aspects of God's nature that remain relevant for today's believers. These divine attributes provide the foundation for theology, worship, and spiritual formation. Understanding God's character shapes our expectations, prayers, and relationship with Him.</p>

            <h3>Covenant Faithfulness</h3>
            <p>God's commitment to His covenant promises demonstrates His trustworthiness and faithfulness. This encourages believers to trust God's promises today and to model similar faithfulness in relationships and commitments. The covenant pattern also informs our understanding of baptism and communion as signs of the new covenant.</p>

            <h3>Ethical Guidance</h3>
            <p>While specific applications may require contextual adaptation, the book's ethical principles provide timeless guidance for moral decision-making. These principles address relationships, justice, integrity, and other aspects of personal and community life. They challenge contemporary cultural values that contradict biblical standards.</p>

            <h3>Spiritual Formation</h3>
            <p>The examples of both faithfulness and failure provide learning opportunities for spiritual development. These biblical accounts invite self-examination and encourage growth in godly character. They remind believers that spiritual formation involves both divine grace and human responsibility.</p>
            """
        else:  # New Testament
            return """
            <p>This book provides valuable insights for contemporary application:</p>

            <h3>Christlike Character</h3>
            <p>The book's portrayal of Jesus and teaching about Him provides the pattern for Christian character and conduct. This Christlikeness manifests in relationships, attitudes, speech, and actions. The transformative power of the gospel enables believers to grow in resembling Christ.</p>

            <h3>Church Life and Mission</h3>
            <p>Principles for healthy church community address worship, leadership, conflict resolution, and mutual edification. These guidelines help contemporary churches maintain biblical faithfulness while addressing current challenges. They also inform the church's missional engagement with surrounding culture.</p>

            <h3>Spiritual Warfare</h3>
            <p>The book acknowledges the reality of spiritual conflict and provides resources for overcoming evil. This perspective balances awareness of spiritual opposition with confidence in Christ's victory. It helps believers recognize and resist temptation while avoiding both naive dismissal and unhealthy obsession with demonic activity.</p>

            <h3>Eschatological Hope</h3>
            <p>The anticipation of Christ's return and the fulfillment of God's promises provides perspective for current circumstances. This hope sustains believers through suffering and shapes priorities and decisions. It balances engagement with present responsibilities and anticipation of future glory.</p>
            """

    return applications.get(book, """
                <p>The book provides enduring insights that profoundly apply to contemporary life, offering divine wisdom for navigating the complexities of modern existence:</p>

                <h3>Spiritual Formation and Discipleship</h3>
                <p>The book offers comprehensive guidance for spiritual growth, character development, and deepening relationship with God. These insights help believers develop authentic faith that withstands cultural pressures, intellectual challenges, and personal trials. The principles for prayer, worship, Scripture study, and spiritual disciplines provide practical pathways for communion with God. The book demonstrates how divine truth transforms the heart, renews the mind, and shapes behavior according to God's righteous standards. Contemporary disciples can apply these insights to develop spiritual maturity, overcome sinful patterns, and cultivate the fruit of the Spirit in daily life.</p>

                <h3>Community Living and Relational Wisdom</h3>
                <p>The book provides profound principles for building healthy relationships, resolving conflicts, and fostering mutual edification within Christian community. These insights address contemporary challenges in marriage and family life, church relationships, workplace dynamics, and social interactions. The book demonstrates how the gospel transforms relationships by promoting forgiveness, humility, service, and sacrificial love. Modern believers can apply these principles to strengthen marriages, raise children according to biblical values, build authentic friendships, and create communities characterized by grace, truth, and mutual support.</p>

                <h3>Ethical Decision-Making and Moral Clarity</h3>
                <p>The book establishes timeless moral principles and decision-making frameworks that help believers navigate complex ethical dilemmas in contemporary society. These guidelines address issues like business ethics, medical decisions, political engagement, environmental stewardship, and social justice concerns. The book demonstrates how divine law reflects God's character and promotes human flourishing, providing objective moral standards that transcend cultural relativism. Contemporary Christians can apply these insights to make decisions that honor God, benefit others, and maintain personal integrity in morally ambiguous situations.</p>

                <h3>Hope, Perseverance, and Eternal Perspective</h3>
                <p>The book provides profound encouragement for facing suffering, maintaining faith during trials, and trusting in God's sovereign purposes even when circumstances seem hopeless. These insights address contemporary struggles with anxiety, depression, injustice, persecution, and existential questions about life's meaning. The book demonstrates how divine promises sustain believers through difficult seasons and how eternal perspective transforms present priorities. Modern disciples can apply these truths to develop resilience, find purpose in suffering, maintain joy amid difficulties, and live with confident hope in God's ultimate victory over evil.</p>

                <h3>Cultural Engagement and Missional Living</h3>
                <p>The book offers wisdom for engaging contemporary culture with gospel truth while maintaining distinct Christian identity and values. These insights help believers navigate secularization, pluralism, technological advancement, and social change without compromising biblical fidelity. The book demonstrates how Christians can serve as salt and light in their communities, workplaces, and spheres of influence. Contemporary believers can apply these principles to engage in meaningful dialogue with unbelievers, advocate for justice and righteousness, and demonstrate the transforming power of the gospel through word and deed.</p>

                <h3>Stewardship and Resource Management</h3>
                <p>The book establishes comprehensive principles for managing time, talents, and treasures as faithful stewards of God's gifts. These insights address contemporary challenges related to materialism, financial planning, career choices, and resource allocation. The book demonstrates how biblical stewardship involves using all resources to glorify God and serve others rather than merely accumulating wealth or pursuing personal advancement. Modern Christians can apply these principles to develop healthy attitudes toward money, make wise investment decisions, practice generous giving, and use their skills and opportunities to advance God's kingdom.</p>

                <h3>Leadership and Influence</h3>
                <p>The book provides timeless principles for exercising godly leadership and positive influence in family, church, workplace, and community contexts. These insights address contemporary leadership challenges including authority and submission, servant leadership, decision-making processes, and accountability structures. The book demonstrates how biblical leadership involves sacrificial service, moral integrity, visionary thinking, and empowering others for ministry and service. Contemporary leaders can apply these principles to lead with humility and wisdom, develop others' potential, create healthy organizational cultures, and use their influence to promote justice and righteousness.</p>
                """)


def generate_book_highlights(book, chapters):
    """Generate key highlights from a book"""
    # Simple highlights based on book
    # In a real implementation, this would be much more detailed and accurate
    highlights = []

    if book == "Genesis":
        highlights = [
            {"reference": "Genesis 1:1", "description": "The foundational statement of God's creative activity", "url": "/book/Genesis/chapter/1#verse-1", "text": get_verse_text("Genesis", 1, 1)},
            {"reference": "Genesis 1:26-27", "description": "Creation of humanity in God's image", "url": "/book/Genesis/chapter/1#verse-26", "text": get_verse_text("Genesis", 1, 26)},
            {"reference": "Genesis 3:15", "description": "First messianic prophecy (the protoevangelium)", "url": "/book/Genesis/chapter/3#verse-15", "text": get_verse_text("Genesis", 3, 15)},
            {"reference": "Genesis 12:1-3", "description": "God's covenant call and promise to Abraham", "url": "/book/Genesis/chapter/12#verse-1", "text": get_verse_text("Genesis", 12, 1)},
            {"reference": "Genesis 22:1-18", "description": "Abraham's faith demonstrated in offering Isaac", "url": "/book/Genesis/chapter/22#verse-1", "text": get_verse_text("Genesis", 22, 1)},
        ]
    elif book == "Exodus":
        highlights = [
            {"reference": "Exodus 3:14", "description": "God's self-revelation as 'I AM WHO I AM'", "url": "/book/Exodus/chapter/3#verse-14", "text": get_verse_text("Exodus", 3, 14)},
            {"reference": "Exodus 12:1-30", "description": "Institution of the Passover", "url": "/book/Exodus/chapter/12#verse-1", "text": get_verse_text("Exodus", 12, 1)},
            {"reference": "Exodus 14:13-31", "description": "Crossing of the Red Sea", "url": "/book/Exodus/chapter/14#verse-13", "text": get_verse_text("Exodus", 14, 13)},
            {"reference": "Exodus 20:1-17", "description": "The Ten Commandments", "url": "/book/Exodus/chapter/20#verse-1", "text": get_verse_text("Exodus", 20, 1)},
            {"reference": "Exodus 25:8", "description": "Command to build the tabernacle", "url": "/book/Exodus/chapter/25#verse-8", "text": get_verse_text("Exodus", 25, 8)},
            {"reference": "Exodus 34:6-7", "description": "Revelation of God's character and attributes", "url": "/book/Exodus/chapter/34#verse-6", "text": get_verse_text("Exodus", 34, 6)}
        ]
    elif book == "Revelation":
        highlights = [
            {"reference": "Revelation 1:8", "description": "God as Alpha and Omega, encompassing all history", "url": "/book/Revelation/chapter/1#verse-8", "text": get_verse_text("Revelation", 1, 8)},
            {"reference": "Revelation 4-5", "description": "Throne room vision with the Lamb who was slain", "url": "/book/Revelation/chapter/4#verse-1", "text": get_verse_text("Revelation", 4, 1)},
            {"reference": "Revelation 12", "description": "Cosmic conflict between the woman and the dragon", "url": "/book/Revelation/chapter/12#verse-1", "text": get_verse_text("Revelation", 12, 1)},
            {"reference": "Revelation 19:11-16", "description": "Christ's return as conquering King", "url": "/book/Revelation/chapter/19#verse-11", "text": get_verse_text("Revelation", 19, 11)},
            {"reference": "Revelation 20:11-15", "description": "Final judgment at the great white throne", "url": "/book/Revelation/chapter/20#verse-11", "text": get_verse_text("Revelation", 20, 11)},
            {"reference": "Revelation 21:1-5", "description": "New heaven and new earth with God dwelling with His people", "url": "/book/Revelation/chapter/21#verse-1", "text": get_verse_text("Revelation", 21, 1)}
        ]
    else:
        # Generate some general highlights based on chapter count
        chapter_count = len(chapters)
        if chapter_count > 0:
            highlights.append({"reference": f"{book} 1:1", "description": "Opening statement establishing key themes", "url": f"/book/{book}/chapter/1#verse-1", "text": get_verse_text(book, 1, 1)})

        if chapter_count > 5:
            highlights.append({"reference": f"{book} {chapter_count//4}:1", "description": "Important development in the book's message", "url": f"/book/{book}/chapter/{chapter_count//4}#verse-1", "text": get_verse_text(book, chapter_count//4, 1)})

        if chapter_count > 10:
            highlights.append({"reference": f"{book} {chapter_count//2}:1", "description": "Central teaching or turning point", "url": f"/book/{book}/chapter/{chapter_count//2}#verse-1", "text": get_verse_text(book, chapter_count//2, 1)})

        if chapter_count > 15:
            highlights.append({"reference": f"{book} {3*chapter_count//4}:1", "description": "Application of key principles", "url": f"/book/{book}/chapter/{3*chapter_count//4}#verse-1", "text": get_verse_text(book, 3*chapter_count//4, 1)})

        if chapter_count > 0:
            highlights.append({"reference": f"{book} {chapter_count}:1", "description": "Concluding summary or final exhortation", "url": f"/book/{book}/chapter/{chapter_count}#verse-1", "text": get_verse_text(book, chapter_count, 1)})

    return highlights


def generate_book_outline(book, chapters):
    """Generate an outline for a book"""
    # Simple outline based on book
    # In a real implementation, this would be much more detailed and accurate

    if book == "Genesis":
        return [
            {
                "title": "Primeval History (1-11)",
                "items": [
                    {"text": "Creation of the universe and humanity", "reference": "Genesis 1-2", "url": "/book/Genesis/chapter/1"},
                    {"text": "Fall and its immediate consequences", "reference": "Genesis 3-5", "url": "/book/Genesis/chapter/3"},
                    {"text": "Judgment of the flood and new beginning", "reference": "Genesis 6-9", "url": "/book/Genesis/chapter/6"},
                    {"text": "Table of nations and tower of Babel", "reference": "Genesis 10-11", "url": "/book/Genesis/chapter/10"}
                ]
            },
            {
                "title": "Abraham Cycle (12-25)",
                "items": [
                    {"text": "Call and covenant promises", "reference": "Genesis 12-15", "url": "/book/Genesis/chapter/12"},
                    {"text": "Covenant confirmation and Sodom's destruction", "reference": "Genesis 16-19", "url": "/book/Genesis/chapter/16"},
                    {"text": "Isaac's birth and testing of Abraham", "reference": "Genesis 20-22", "url": "/book/Genesis/chapter/20"},
                    {"text": "Death of Sarah and marriage of Isaac", "reference": "Genesis 23-25", "url": "/book/Genesis/chapter/23"}
                ]
            },
            {
                "title": "Jacob Cycle (25-36)",
                "items": [
                    {"text": "Jacob and Esau: birth and birthright", "reference": "Genesis 25-27", "url": "/book/Genesis/chapter/25"},
                    {"text": "Jacob's exile and marriages", "reference": "Genesis 28-30", "url": "/book/Genesis/chapter/28"},
                    {"text": "Return to Canaan and reconciliation", "reference": "Genesis 31-33", "url": "/book/Genesis/chapter/31"},
                    {"text": "Dinah incident and covenant renewal", "reference": "Genesis 34-36", "url": "/book/Genesis/chapter/34"}
                ]
            },
            {
                "title": "Joseph Story (37-50)",
                "items": [
                    {"text": "Joseph sold into slavery", "reference": "Genesis 37-38", "url": "/book/Genesis/chapter/37"},
                    {"text": "Joseph's imprisonment and rise to power", "reference": "Genesis 39-41", "url": "/book/Genesis/chapter/39"},
                    {"text": "Brothers' journeys to Egypt and testing", "reference": "Genesis 42-44", "url": "/book/Genesis/chapter/42"},
                    {"text": "Reconciliation and settlement in Egypt", "reference": "Genesis 45-47", "url": "/book/Genesis/chapter/45"},
                    {"text": "Jacob's blessings and death", "reference": "Genesis 48-50", "url": "/book/Genesis/chapter/48"}
                ]
            }
        ]
    elif book == "Exodus":
        return [
            {
                "title": "Israel in Egypt (1-12)",
                "items": [
                    {"text": "Oppression and Moses' birth", "reference": "Exodus 1-2", "url": "/book/Exodus/chapter/1"},
                    {"text": "Moses' call and confrontation with Pharaoh", "reference": "Exodus 3-6", "url": "/book/Exodus/chapter/3"},
                    {"text": "Plagues on Egypt", "reference": "Exodus 7-10", "url": "/book/Exodus/chapter/7"},
                    {"text": "Passover and Exodus", "reference": "Exodus 11-12", "url": "/book/Exodus/chapter/11"}
                ]
            },
            {
                "title": "Journey to Sinai (13-19)",
                "items": [
                    {"text": "Crossing the Red Sea", "reference": "Exodus 13-15", "url": "/book/Exodus/chapter/13"},
                    {"text": "Wilderness provisions and challenges", "reference": "Exodus 16-17", "url": "/book/Exodus/chapter/16"},
                    {"text": "Jethro's advice and arrival at Sinai", "reference": "Exodus 18-19", "url": "/book/Exodus/chapter/18"}
                ]
            },
            {
                "title": "Covenant at Sinai (20-24)",
                "items": [
                    {"text": "Ten Commandments", "reference": "Exodus 20", "url": "/book/Exodus/chapter/20"},
                    {"text": "Book of the Covenant", "reference": "Exodus 21-23", "url": "/book/Exodus/chapter/21"},
                    {"text": "Covenant confirmation", "reference": "Exodus 24", "url": "/book/Exodus/chapter/24"}
                ]
            },
            {
                "title": "Tabernacle Instructions (25-31)",
                "items": [
                    {"text": "Tabernacle furnishings", "reference": "Exodus 25-27", "url": "/book/Exodus/chapter/25"},
                    {"text": "Priesthood and offerings", "reference": "Exodus 28-30", "url": "/book/Exodus/chapter/28"},
                    {"text": "Craftsmen and Sabbath regulations", "reference": "Exodus 31", "url": "/book/Exodus/chapter/31"}
                ]
            },
            {
                "title": "Covenant Violation and Renewal (32-34)",
                "items": [
                    {"text": "Golden calf incident", "reference": "Exodus 32", "url": "/book/Exodus/chapter/32"},
                    {"text": "Moses' intercession", "reference": "Exodus 33", "url": "/book/Exodus/chapter/33"},
                    {"text": "Covenant renewal", "reference": "Exodus 34", "url": "/book/Exodus/chapter/34"}
                ]
            },
            {
                "title": "Tabernacle Construction (35-40)",
                "items": [
                    {"text": "Gathering materials", "reference": "Exodus 35-36", "url": "/book/Exodus/chapter/35"},
                    {"text": "Making furnishings and priestly garments", "reference": "Exodus 37-39", "url": "/book/Exodus/chapter/37"},
                    {"text": "Tabernacle completion and divine glory", "reference": "Exodus 40", "url": "/book/Exodus/chapter/40"}
                ]
            }
        ]
    else:
        # Generate a simple outline based on chapter count
        chapter_count = len(chapters)
        section_count = min(4, max(2, chapter_count // 5))  # Between 2 and 4 sections

        chapters_per_section = chapter_count // section_count
        outline = []

        for i in range(section_count):
            start_chapter = i * chapters_per_section + 1
            end_chapter = min(chapter_count, (i + 1) * chapters_per_section)

            if i == 0:
                title = "Introduction and Background"
            elif i == section_count - 1:
                title = "Conclusion and Final Exhortations"
            else:
                title = f"Main Section {i}"

            items = []
            for j in range(min(4, end_chapter - start_chapter + 1)):
                chapter_num = start_chapter + j
                items.append({
                    "text": f"Chapter {chapter_num}",
                    "reference": f"{book} {chapter_num}",
                    "url": f"/book/{book}/chapter/{chapter_num}"
                })

            outline.append({
                "title": f"{title} ({start_chapter}-{end_chapter})",
                "items": items
            })

        return outline


def generate_book_cross_references(book):
    """Generate cross-references to other books"""
    # Simple cross-references based on book
    # In a real implementation, this would be much more detailed and accurate

    cross_refs = []

    if book == "Genesis":
        cross_refs = [
            {"reference": "John 1:1-3", "url": "/book/John/chapter/1#verse-1", "description": "Echoes Genesis 1:1, revealing Christ's role in creation"},
            {"reference": "Romans 4:1-25", "url": "/book/Romans/chapter/4#verse-1", "description": "Develops Abraham's faith as pattern for justification"},
            {"reference": "Galatians 3:6-29", "url": "/book/Galatians/chapter/3#verse-6", "description": "Connects Abrahamic covenant to salvation in Christ"},
            {"reference": "Hebrews 11:8-22", "url": "/book/Hebrews/chapter/11#verse-8", "description": "Celebrates faith of Abraham, Isaac, Jacob, and Joseph"},
            {"reference": "1 Peter 3:20", "url": "/book/1 Peter/chapter/3#verse-20", "description": "References Noah's flood as type of baptism"}
        ]
    elif book == "Exodus":
        cross_refs = [
            {"reference": "John 1:14-18", "url": "/book/John/chapter/1#verse-14", "description": "The Word 'tabernacled' among us, echoing Exodus 40"},
            {"reference": "1 Corinthians 5:7", "url": "/book/1 Corinthians/chapter/5#verse-7", "description": "Christ as our Passover lamb"},
            {"reference": "Hebrews 9:1-28", "url": "/book/Hebrews/chapter/9#verse-1", "description": "Tabernacle symbolism fulfilled in Christ"},
            {"reference": "1 Peter 2:9-10", "url": "/book/1 Peter/chapter/2#verse-9", "description": "Church as royal priesthood, echoing Exodus 19:5-6"},
            {"reference": "Revelation 15:3", "url": "/book/Revelation/chapter/15#verse-3", "description": "The song of Moses sung in heaven"}
        ]
    elif book == "Revelation":
        cross_refs = [
            {"reference": "Daniel 7:1-28", "url": "/book/Daniel/chapter/7#verse-1", "description": "Provides imagery for beasts and Son of Man"},
            {"reference": "Ezekiel 1:4-28", "url": "/book/Ezekiel/chapter/1#verse-4", "description": "Influences throne room vision"},
            {"reference": "Isaiah 6:1-7", "url": "/book/Isaiah/chapter/6#verse-1", "description": "Parallels heavenly worship scenes"},
            {"reference": "Zechariah 4:1-14", "url": "/book/Zechariah/chapter/4#verse-1", "description": "Background for lampstands imagery"},
            {"reference": "Matthew 24:29-31", "url": "/book/Matthew/chapter/24#verse-29", "description": "Jesus' teaching on His return"}
        ]
    else:
        # Generate basic cross-references based on testament
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            cross_refs = [
                {"reference": "Matthew 5:17-20", "url": "/book/Matthew/chapter/5#verse-17", "description": "Jesus fulfills the Law and Prophets"},
                {"reference": "Romans 15:4", "url": "/book/Romans/chapter/15#verse-4", "description": "Old Testament written for our instruction"},
                {"reference": "1 Corinthians 10:1-11", "url": "/book/1 Corinthians/chapter/10#verse-1", "description": "Old Testament examples as warnings"},
                {"reference": "2 Timothy 3:16-17", "url": "/book/2 Timothy/chapter/3#verse-16", "description": "Scripture's inspiration and usefulness"},
                {"reference": "Hebrews 1:1-2", "url": "/book/Hebrews/chapter/1#verse-1", "description": "God's revelation in the prophets and in His Son"}
            ]
        else:  # New Testament
            cross_refs = [
                {"reference": "Psalm 110:1-7", "url": "/book/Psalms/chapter/110#verse-1", "description": "Messianic psalm frequently quoted in NT"},
                {"reference": "Isaiah 53:1-12", "url": "/book/Isaiah/chapter/53#verse-1", "description": "Suffering servant prophecy fulfilled in Christ"},
                {"reference": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "description": "Son of Man receiving everlasting dominion"},
                {"reference": "Joel 2:28-32", "url": "/book/Joel/chapter/2#verse-28", "description": "Prophecy of Spirit's outpouring"},
                {"reference": "Malachi 3:1", "url": "/book/Malachi/chapter/3#verse-1", "description": "Prophecy of messenger preparing the way"}
            ]

    return cross_refs


def generate_chapter_summaries(book, chapters):
    """Generate chapter summaries with key verses"""
    # Simple chapter summaries based on book and chapter count
    # In a real implementation, this would be much more detailed and accurate

    summaries = {}

    # Special case for Genesis 1
    if book == "Genesis" and 1 in chapters:
        summaries[1] = {
            "summary": "God creates the universe, earth, and all living things in six days, culminating with the creation of humanity in His image. Each creative act is pronounced 'good,' with the completed creation declared 'very good.'",
            "key_verses": [
                {
                    "verse_num": 1,
                    "brief": "The foundational declaration of God's creative act",
                    "text": "In the beginning God created the heaven and the earth.",
                    "url": "/book/Genesis/chapter/1#verse-1",
                    "comment": "This opening verse establishes monotheism and God's role as Creator, contrasting with ancient Near Eastern creation myths involving multiple deities and preexisting matter."
                },
                {
                    "verse_num": 26,
                    "brief": "Creation of humans in God's image",
                    "text": "And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth, and over every creeping thing that creepeth upon the earth.",
                    "url": "/book/Genesis/chapter/1#verse-26",
                    "comment": "This verse establishes the unique status of humans as God's image-bearers, with both dignity and responsibility. The plural 'us' has been interpreted variously as divine deliberation, royal plural, or early hint of trinitarian reality."
                },
                {
                    "verse_num": 31,
                    "brief": "God's evaluation of creation as very good",
                    "text": "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day.",
                    "url": "/book/Genesis/chapter/1#verse-31",
                    "comment": "The divine evaluation affirms creation's inherent goodness, establishing that evil comes not from God's creative act but from subsequent corruption. This verse provides the foundation for a positive Christian view of the material world."
                }
            ]
        }

    # Generate simple summaries for all chapters
    for ch in chapters:
        if ch not in summaries:
            # Create a generic summary
            summary = f"Chapter {ch} of {book} continues the narrative with important developments and teachings."

            # Create some generic key verses
            key_verses = []
            if ch > 0:
                key_verses.append({
                    "verse_num": 1,
                    "brief": "Opening verse of the chapter",
                    "text": get_verse_text(book, ch, 1),
                    "url": f"/book/{book}/chapter/{ch}#verse-1",
                    "comment": f"This verse begins chapter {ch} and establishes its context and direction."
                })

                if ch % 2 == 0:  # Add another key verse for even-numbered chapters
                    verse_num = min(ch, 10)
                    key_verses.append({
                        "verse_num": verse_num,
                        "brief": f"Key teaching in verse {verse_num}",
                        "text": f"[Text of {book} {ch}:{verse_num}]",
                        "url": f"/book/{book}/chapter/{ch}#verse-{verse_num}",
                        "comment": f"This verse contains significant content related to the chapter's main themes."
                    })

            summaries[ch] = {
                "summary": summary,
                "key_verses": key_verses
            }

    return summaries


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "kjv-study"}


@app.get("/robots.txt", response_class=Response)
def robots_txt():
    """Generate robots.txt for search engine crawlers"""
    robots_content = """User-agent: *
Allow: /
Disallow: /api/

# Sitemap location
Sitemap: https://kjvstudy.org/sitemap.xml

# Crawl delay (be nice to our servers)
Crawl-delay: 1
"""
    return Response(content=robots_content, media_type="text/plain")


def generate_literary_features(book, genre):
    """Generate commentary on literary features of a book"""

    # Default features based on genre
    if "narrative" in genre.lower():
        return f"""
        <p>{book} employs narrative techniques characteristic of biblical historiography. The book uses plot development, characterization, dialogue, and setting to convey both historical events and theological meaning. Narratives in {book} are carefully structured to highlight divine providence and human response.</p>

        <h3>Structure</h3>
        <p>The narrative structure of {book} involves a clear progression with rising and falling action, climactic moments, and resolution. The author selectively includes details that advance the theological purpose while maintaining historical accuracy.</p>

        <h3>Literary Devices</h3>
        <p>Common literary devices in {book} include:</p>
        <ul>
            <li><strong>Repetition</strong> - Key phrases and motifs recur to emphasize important themes</li>
            <li><strong>Type-scenes</strong> - Conventional scenarios (e.g., encounters at wells, divine calls) that evoke specific expectations</li>
            <li><strong>Inclusio</strong> - Framing sections with similar language to create literary units</li>
            <li><strong>Chiasm</strong> - Mirror-image structures that highlight central elements</li>
        </ul>

        <p>These narrative techniques guide the reader's interpretation and highlight theological significance within historical events.</p>
        """
    elif "epistle" in genre.lower():
        return f"""
        <p>{book} follows the conventions of ancient letter-writing while adapting them for theological instruction. The epistle combines formal elements of Greco-Roman correspondence with Jewish expository methods to communicate Christian teaching.</p>

        <h3>Structure</h3>
        <p>The epistle follows a typical pattern including:</p>
        <ul>
            <li><strong>Opening</strong> - Sender, recipients, and greeting (often theologically expanded)</li>
            <li><strong>Thanksgiving/Prayer</strong> - Expressing gratitude and/or intercession for recipients</li>
            <li><strong>Body</strong> - Doctrinal exposition followed by practical application</li>
            <li><strong>Closing</strong> - Final exhortations, greetings, and benediction</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>The epistle employs various rhetorical techniques including:</p>
        <ul>
            <li><strong>Diatribe</strong> - Dialogue with imaginary opponent through questions and answers</li>
            <li><strong>Paraenesis</strong> - Moral exhortation often through contrasting vices and virtues</li>
            <li><strong>Examples</strong> - Drawing on biblical figures or contemporary situations as models</li>
            <li><strong>Metaphors</strong> - Extended comparisons that illustrate theological concepts</li>
        </ul>

        <p>These epistolary features reflect both Greco-Roman rhetorical education and Jewish interpretive traditions adapted for Christian purposes.</p>
        """
    elif "wisdom" in genre.lower() or "poetry" in genre.lower():
        return f"""
        <p>{book} exemplifies biblical wisdom literature and poetic expression. The book uses carefully crafted language, figurative speech, and structural patterns to convey insights about divine order and human experience.</p>

        <h3>Poetic Structure</h3>
        <p>The poetry in {book} primarily employs parallelism, where successive lines relate to each other in various ways:</p>
        <ul>
            <li><strong>Synonymous parallelism</strong> - Second line restates the first with similar meaning</li>
            <li><strong>Antithetic parallelism</strong> - Second line contrasts with the first</li>
            <li><strong>Synthetic parallelism</strong> - Second line develops or completes the first</li>
            <li><strong>Emblematic parallelism</strong> - One line uses a metaphor to illustrate the other</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>{book} employs numerous literary techniques including:</p>
        <ul>
            <li><strong>Imagery</strong> - Vivid sensory language drawing on nature, daily life, and cultural practices</li>
            <li><strong>Metaphor and simile</strong> - Comparisons that illuminate abstract concepts</li>
            <li><strong>Acrostic patterns</strong> - Alphabetical arrangements that structure content</li>
            <li><strong>Personification</strong> - Abstract qualities given human attributes (particularly wisdom)</li>
        </ul>

        <p>These poetic features create aesthetic beauty while making the wisdom more memorable and impactful.</p>
        """
    elif "prophetic" in genre.lower():
        return f"""
        <p>{book} employs the distinctive literary forms of biblical prophecy. The book combines poetic expression, symbolic actions, and visionary experiences to communicate divine messages with both immediate and future significance.</p>

        <h3>Prophetic Forms</h3>
        <p>{book} includes various prophetic forms:</p>
        <ul>
            <li><strong>Oracle</strong> - Divine speech introduced by "Thus says the LORD" or similar formula</li>
            <li><strong>Woe oracle</strong> - Judgment pronouncement beginning with "Woe to..."</li>
            <li><strong>Lawsuit</strong> - Covenant litigation using legal metaphors with witnesses, evidence, and verdict</li>
            <li><strong>Vision report</strong> - Account of prophetic visions with interpretation</li>
            <li><strong>Symbolic action</strong> - Prophetic performance conveying message visually</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>Prophetic literature in {book} employs various techniques:</p>
        <ul>
            <li><strong>Metaphor and simile</strong> - Comparing Israel to unfaithful spouse, vineyard, etc.</li>
            <li><strong>Hyperbole</strong> - Deliberate exaggeration for rhetorical effect</li>
            <li><strong>Merism</strong> - Expressing totality through contrasting pairs</li>
            <li><strong>Wordplay</strong> - Puns and sound associations (particularly in Hebrew)</li>
        </ul>

        <p>These prophetic literary features combine aesthetic power with rhetorical force to call for response to divine revelation.</p>
        """
    elif "apocalyptic" in genre.lower():
        return f"""
        <p>{book} exemplifies apocalyptic literature with its distinctive symbolic imagery and visionary framework. The book uses heavily symbolic language, cosmic dualism, and revelatory encounters to unveil spiritual realities and future events.</p>

        <h3>Apocalyptic Features</h3>
        <p>Key characteristics of {book} as apocalyptic literature include:</p>
        <ul>
            <li><strong>Symbolic visions</strong> - Elaborate imagery requiring interpretation</li>
            <li><strong>Heavenly mediators</strong> - Angels explaining visions to the recipient</li>
            <li><strong>Cosmic dualism</strong> - Sharp contrast between good/evil, present age/age to come</li>
            <li><strong>Deterministic view</strong> - History moving toward predetermined divine conclusion</li>
            <li><strong>Pseudonymity</strong> - Attribution to ancient figure (in non-canonical apocalypses)</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>Apocalyptic literature in {book} employs various techniques:</p>
        <ul>
            <li><strong>Symbolism</strong> - Numbers, colors, and animals representing spiritual realities</li>
            <li><strong>Mythic imagery</strong> - Drawing on cosmic battle motifs and ancient Near Eastern symbols</li>
            <li><strong>Recapitulation</strong> - Same events described from different perspectives</li>
            <li><strong>Intercalation</strong> - Interrupting one sequence with another for theological purposes</li>
        </ul>

        <p>These apocalyptic features enable the communication of transcendent realities that defy literal description and provide hope in times of crisis.</p>
        """
    elif "gospel" in genre.lower():
        return f"""
        <p>{book} represents the distinctive gospel genre—a theological biography focusing on Jesus' life, teaching, death, and resurrection. The book combines narrative elements, discourse material, and passion account to proclaim Jesus' identity and significance.</p>

        <h3>Structure</h3>
        <p>{book} organizes its material with theological purpose, including:</p>
        <ul>
            <li><strong>Prologue</strong> - Introducing theological themes and Jesus' identity</li>
            <li><strong>Ministry narrative</strong> - Accounts of teachings, miracles, and encounters</li>
            <li><strong>Discourse sections</strong> - Extended teaching blocks on various themes</li>
            <li><strong>Passion narrative</strong> - Detailed account of Jesus' final days, death, and resurrection</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>The gospel employs various techniques including:</p>
        <ul>
            <li><strong>Inclusio</strong> - Framing devices marking literary units</li>
            <li><strong>Chiasm</strong> - Mirror structures highlighting central elements</li>
            <li><strong>Typology</strong> - Presenting Jesus as fulfilling Old Testament patterns</li>
            <li><strong>Irony</strong> - Contrasts between appearance and reality, human and divine perspectives</li>
            <li><strong>Parables</strong> - Figurative stories conveying kingdom truths</li>
        </ul>

        <p>These gospel features combine to present Jesus Christ as the fulfillment of God's promises and the decisive revelation of God's salvation.</p>
        """
    else:
        return f"""
        <p>{book} employs various literary techniques and structural elements to communicate its message effectively. The book's form serves its function, using appropriate conventions to convey its theological content.</p>

        <h3>Structure</h3>
        <p>The book demonstrates intentional organization, with distinct sections addressing different aspects of its theme. Transitions between sections are marked by shifts in topic, audience, or literary form.</p>

        <h3>Literary Devices</h3>
        <p>The book employs various literary techniques including:</p>
        <ul>
            <li><strong>Imagery</strong> - Concrete pictures that convey abstract concepts</li>
            <li><strong>Repetition</strong> - Key terms and phrases that emphasize important themes</li>
            <li><strong>Contrast</strong> - Opposing concepts to highlight distinctions</li>
            <li><strong>Figurative language</strong> - Metaphors and similes that illuminate meaning</li>
        </ul>

        <p>These literary features enhance the book's communicative power and contribute to its enduring significance in the biblical canon.</p>
        """


def generate_book_themes(book):
    """Generate themes for a book"""

    # Book-specific themes
    themes = {
        "Exodus": """
        <p>Exodus develops several major theological themes that shape the biblical narrative:</p>

        <h3>Divine Deliverance</h3>
        <p>The central event of Exodus—Israel's liberation from Egyptian bondage—establishes God as the deliverer who sees affliction, hears cries, and acts powerfully to save. The exodus event becomes paradigmatic in Scripture, referenced repeatedly as the definitive display of God's redemptive power. This deliverance comes through both supernatural intervention (plagues, Red Sea crossing) and human agency (Moses' leadership), establishing a pattern where God typically works through human instruments while maintaining divine sovereignty.</p>

        <h3>Covenant Relationship</h3>
        <p>Exodus transforms God's covenant with the patriarchs into a formalized national covenant at Sinai. This covenant establishes Israel's special status as God's "treasured possession," "kingdom of priests," and "holy nation" (Exodus 19:5-6). The covenant includes mutual commitments: God promises His presence and protection, while Israel commits to exclusive worship and ethical living. This formalized relationship provides the framework for understanding subsequent interactions between God and Israel throughout the Old Testament.</p>

        <h3>Divine Revelation</h3>
        <p>Throughout Exodus, God progressively reveals Himself through words and actions. The book records direct divine speech, mediated revelation through Moses, and physical manifestations of divine presence (burning bush, pillar of cloud/fire, Sinai theophany). The revelation culminates in the giving of the law, which discloses God's will for human conduct, and the tabernacle instructions, which provide the means for divine-human communion. This theme emphasizes that God desires to be known and has taken initiative to make Himself known.</p>

        <h3>Divine Presence</h3>
        <p>The tabernacle establishment addresses the fundamental question of how a holy God can dwell among an unholy people. The elaborate preparation for God's presence—with specific architecture, furnishings, priesthood, and sacrificial system—highlights both divine holiness and divine desire for communion. The book concludes with God's glory filling the tabernacle, visibly confirming His presence among Israel. This theme of divine presence continues throughout Scripture, reaching its culmination in the incarnation of Christ and the indwelling of the Holy Spirit.</p>

        <h3>Worship and Holiness</h3>
        <p>Exodus establishes Israel's identity as a worshiping community set apart for divine service. The initial demand to Pharaoh was for Israel's release to worship, and the book culminates with worship regulations and structures. The law and tabernacle system emphasize the importance of approaching God on His terms rather than through human innovation. The repeated call to holiness—separation from other nations and consecration to God—establishes that authentic worship involves both specific religious practices and comprehensive ethical living.</p>
        """,

        "Genesis": """
        <p>Genesis establishes the foundational theological themes that undergird the entire biblical narrative, introducing concepts that find their ultimate fulfillment in Christ and the new creation:</p>

        <h3>Divine Sovereignty and Creative Order</h3>
        <p>Genesis opens with the most profound theological statement in human literature: "In the beginning God created the heavens and the earth" (1:1). This declaration establishes God's absolute sovereignty over all reality and His role as the ultimate source of all existence. The creation account reveals God's transcendence (existing before and beyond creation), His immanence (intimately involved in creation's details), and His wisdom (creating with purpose and design). Unlike ancient Near Eastern cosmogonies that depict creation through divine conflict and struggle, Genesis presents creation through divine fiat—God speaks and reality responds. The repeated phrase "and God saw that it was good" establishes the inherent goodness of creation and God's pleasure in His work. The creation's movement from chaos to order, darkness to light, emptiness to fullness reveals divine purpose and design that points toward ultimate restoration in the new heaven and earth.</p>

        <h3>The Imago Dei and Human Dignity</h3>
        <p>The creation of humanity "in the image of God" (1:26-27) represents one of Scripture's most profound anthropological statements. This divine image distinguishes humans from all other creatures, conferring unique dignity, responsibility, and capacity for relationship with the divine. The image encompasses intellectual faculties (knowledge and reason), moral capacity (ability to distinguish good from evil), spiritual nature (capacity for fellowship with God), creative ability (reflecting divine creativity), and dominion mandate (representing God's rule over creation). The dual nature of humanity as both physical (formed from dust) and spiritual (breathed with divine breath) establishes the holistic view of human nature that pervades Scripture. The divine blessing to "be fruitful and multiply" establishes marriage and family as fundamental divine institutions, while the cultural mandate to "subdue and have dominion" establishes work and cultural development as expressions of divine calling.</p>

        <h3>The Fall and Total Depravity</h3>
        <p>Genesis 3 records the catastrophic entrance of sin into God's perfect creation, fundamentally altering human nature and the entire cosmic order. The temptation narrative reveals sin's essential character as distrust of God's word, pride of life, and desire for autonomous moral authority. The consequences of the fall are comprehensive: spiritual death (broken fellowship with God), physical death (mortality entering human experience), relational discord (conflict between man and woman), cosmic disruption (creation subjected to futility), and moral corruption (the heart's inclination toward evil). The progression of sin from Genesis 3 through 11 demonstrates sin's exponential expansion from individual transgression (Adam and Eve) to fraternal violence (Cain and Abel) to civilizational corruption (the flood generation) to collective rebellion (Tower of Babel). Yet even in judgment, divine grace appears through promised redemption (3:15), protective mercy (3:21), and preserving covenant (8:20-9:17).</p>

        <h3>Covenant Theology and Redemptive Promise</h3>
        <p>Genesis introduces the fundamental covenant structure that governs God's relationship with humanity throughout Scripture. The Adamic covenant establishes the original relationship between God and humanity in Eden. After the fall, the Noahic covenant establishes divine commitment to preserve creation despite human sinfulness. The Abrahamic covenant (Genesis 12, 15, 17, 22) forms the foundational charter for God's redemptive work, encompassing promises of land (representing divine provision), descendants (representing divine blessing), and universal blessing through Abraham's offspring (representing divine mission). The covenant includes both conditional elements (requiring faith and obedience) and unconditional elements (dependent solely on divine faithfulness). The ritual ratification in Genesis 15, where God alone passes between the divided animals, emphasizes the covenant's unilateral character and divine guarantee. This covenant framework establishes the theological foundation for understanding Israel's election, the Mosaic law, the Davidic dynasty, and ultimately the new covenant in Christ.</p>

        <h3>Divine Providence and Human Responsibility</h3>
        <p>Genesis masterfully balances divine sovereignty with genuine human responsibility, particularly evident in the Joseph narrative (chapters 37-50). Joseph's declaration that "you meant it for evil, but God meant it for good" (50:20) articulates the biblical doctrine of providence—God's superintending control over human events to accomplish His purposes without violating human freedom or responsibility. The patriarchal narratives demonstrate how God works through human choices, cultural circumstances, family dynamics, and even sinful actions to fulfill His covenant promises. This theme addresses fundamental questions about divine justice, human freedom, suffering's purpose, and history's meaning. The providence theme assures believers that divine purposes will ultimately prevail while maintaining human accountability for moral choices.</p>

        <h3>Protoevangelium and Redemptive Hope</h3>
        <p>Genesis 3:15, traditionally called the protoevangelium ("first gospel"), introduces the theme of redemptive hope that sustains the entire biblical narrative. The promise that the woman's offspring will crush the serpent's head while suffering a heel wound establishes the pattern of redemption through suffering that culminates in Christ's victory over Satan through the cross. This theme develops through the promise to Abraham that all nations will be blessed through his offspring (12:3, 22:18), connecting universal human need with particular divine provision. The recurring theme of the chosen younger son (Abel over Cain, Isaac over Ishmael, Jacob over Esau, Joseph over his brothers) points toward God's gracious election and the reversal of natural expectations through divine intervention.</p>

        <h3>Typological Patterns and Christological Anticipation</h3>
        <p>Genesis establishes numerous typological patterns that point forward to Christ and New Testament realities. Adam serves as a type of Christ as the federal head of humanity, though in antithetical contrast (Romans 5:12-21). The sacrificial system beginning with Abel's acceptable offering and culminating in Abraham's willingness to sacrifice Isaac prefigures substitutionary atonement. Joseph functions as a type of Christ in his rejection by brothers, suffering for others' sins, exaltation to divine right hand, provision during famine, and reconciliation with those who betrayed him. The recurring theme of the bride obtained through service (Isaac and Rebekah, Jacob and Rachel) points toward Christ's obtaining His bride the church through His service unto death. These typological patterns demonstrate the organic unity of Scripture and God's consistent redemptive method throughout history.</p>

        <h3>Worship and Spiritual Response</h3>
        <p>Genesis establishes fundamental principles for approaching God through worship, beginning with the contrast between Cain's rejected offering and Abel's accepted sacrifice. The book reveals the necessity of approaching God according to divine prescription, the centrality of sacrifice in bridging the gap between sinful humanity and holy God, and the importance of faith in making worship acceptable. The patriarchal altar-building and name-calling (calling on the name of the LORD) establish patterns of covenantal worship that will be formalized in the Mosaic system. The recurring theme of pilgrimage (Abraham's journey to the promised land, Jacob's wrestling with God, Joseph's faith concerning his bones) establishes the spiritual principle that faith involves leaving the familiar to follow divine promise toward ultimate fulfillment.</p>
        """,

        "Revelation": """
        <p>Revelation develops several major themes that bring the biblical narrative to its climactic conclusion:</p>

        <h3>Divine Sovereignty</h3>
        <p>God's absolute sovereignty over history and creation stands as the book's foundation. Despite apparent chaos and the temporary triumph of evil, the heavenly throne room scenes (Revelation 4-5) establish that God remains in control. This sovereignty provides assurance that evil will not ultimately prevail and that God's purposes will be accomplished.</p>

        <h3>Christ's Identity and Victory</h3>
        <p>Revelation presents a multifaceted portrait of Christ as the glorified Lord (Revelation 1), the slaughtered but victorious Lamb (Revelation 5), and the conquering King (Revelation 19). This theme celebrates Christ's completed work at the cross while anticipating His final triumph over all evil forces. The paradoxical image of the slain Lamb who conquers is particularly significant.</p>

        <h3>Faithful Witness Amid Persecution</h3>
        <p>The call to faithful endurance despite suffering runs throughout the letters to the seven churches (Revelation 2-3) and the visions that follow. Martyrdom is presented not as defeat but as victory that follows Christ's pattern. The book encourages persecuted believers that their suffering is temporary and meaningful within God's larger purposes.</p>

        <h3>Judgment and Salvation</h3>
        <p>The theme of divine judgment appears in the seals, trumpets, and bowls (Revelation 6-16), demonstrating God's holy response to evil and vindication of His people. Simultaneously, the book emphasizes salvation for those who remain faithful, portrayed through images of sealing, palm branches, white robes, and the Lamb's book of life.</p>

        <h3>New Creation</h3>
        <p>The climactic vision of new heavens and earth (Revelation 21-22) completes the biblical narrative that began in Genesis. This theme emphasizes the comprehensive scope of redemption—not merely saving souls but renewing creation. The new Jerusalem represents the perfect communion between God and His people in a restored creation free from sin and death.</p>
        """,

        "Romans": """
        <p>Romans systematically develops several interconnected theological themes:</p>

        <h3>Universal Sinfulness</h3>
        <p>Paul establishes that all humanity—both Jews and Gentiles—stands guilty before God (Romans 1:18-3:20). This universal sinfulness demonstrates the need for a salvation that comes by faith rather than works of the law. Paul's analysis of sin goes beyond individual acts to the underlying condition of rebellion against God.</p>

        <h3>Justification by Faith</h3>
        <p>The letter's central theme presents justification as God's declaration of righteousness for those who believe in Christ (Romans 3:21-5:21). This righteousness comes not through law-keeping but through faith in Christ's atoning work. Paul demonstrates this principle from Scripture (Abraham's example) and through the contrast between Adam and Christ.</p>

        <h3>New Life in the Spirit</h3>
        <p>Romans explores how believers are freed from sin's dominion to live in the power of the Spirit (Romans 6-8). This progressive sanctification involves dying to sin, serving in the Spirit's newness, and experiencing adoption as God's children. The Spirit's indwelling enables believers to fulfill the law's righteous requirement through transformed hearts.</p>

        <h3>God's Faithfulness to Israel</h3>
        <p>Paul addresses the theological problem of Israel's unbelief (Romans 9-11), affirming God's sovereignty in election while maintaining human responsibility. He argues that God has not rejected His people but has always worked through a faithful remnant. The temporary hardening of Israel serves God's purpose of bringing salvation to the Gentiles, but ultimately "all Israel will be saved."</p>

        <h3>Transformed Relationships</h3>
        <p>The letter's ethical section (Romans 12-15) shows how theological truth transforms relationships with other believers, enemies, civil authorities, and those with whom believers have conscience disagreements. The gospel creates a new community that embodies sacrificial love, harmony amid diversity, and consideration for others' consciences.</p>
        """
    }

    # Default themes based on testament and genre
    if book not in themes:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        if testament == "Old Testament":
            if "law" in genre.lower() or "torah" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Revelation and Law</h3>
                <p>God reveals His character and will through direct instruction, establishing the covenant relationship with His people. The law provides guidance for worshiping the true God, maintaining covenant relationships, and expressing gratitude for redemption.</p>

                <h3>Holiness and Separation</h3>
                <p>God calls His people to be set apart from surrounding nations through distinctive worship, ethical standards, and cultural practices. This separation preserves Israel's unique identity and witness in a polytheistic world.</p>

                <h3>Covenant Faithfulness</h3>
                <p>The relationship between God and Israel is formalized through covenant commitments with promises for obedience and consequences for disobedience. This covenant structure shapes Israel's national identity and religious practices.</p>

                <h3>Sacrificial System</h3>
                <p>Various offerings and rituals provide means of atonement, purification, and communion with God. This sacrificial system acknowledges human sinfulness while providing divinely established means of maintaining relationship with God.</p>
                """
            elif "historical" in genre.lower() or "narrative" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Providence</h3>
                <p>God sovereignly works through historical circumstances and human decisions to accomplish His purposes. Even through times of difficulty and apparent setbacks, God remains active in guiding history toward His intended outcomes.</p>

                <h3>Covenant Fidelity</h3>
                <p>The book traces God's faithfulness to His covenant promises despite human failings. This covenant relationship forms the framework for understanding Israel's successes, failures, and responsibilities.</p>

                <h3>Leadership and Authority</h3>
                <p>Various leaders demonstrate both positive and negative examples of exercising authority. Their successes and failures reveal principles of godly leadership and the consequences of abusing power.</p>

                <h3>Obedience and Blessing</h3>
                <p>The narrative demonstrates connections between faithfulness to God's commands and experiencing His blessing. Conversely, disobedience leads to various forms of judgment and discipline.</p>
                """
            elif "wisdom" in genre.lower() or "poetry" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Wisdom</h3>
                <p>True wisdom begins with reverence for God and aligns human understanding with divine perspective. This wisdom provides insight for navigating life's complexities and making decisions that honor God.</p>

                <h3>Creation's Order</h3>
                <p>The book reflects on patterns and principles embedded in the created order. By observing these patterns, humans can better understand how to live in harmony with God's design.</p>

                <h3>Human Experience</h3>
                <p>The text honestly addresses the full range of human emotions, questions, and struggles. This realistic portrayal validates authentic expression while directing these experiences toward God.</p>

                <h3>Ethical Living</h3>
                <p>Practical guidance for relationships, speech, work, and character development demonstrates how divine wisdom applies to everyday decisions and interactions.</p>
                """
            elif "prophetic" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Judgment</h3>
                <p>God's righteous response to persistent sin demonstrates His holiness and justice. This judgment particularly addresses covenant violations, idolatry, social injustice, and religious hypocrisy.</p>

                <h3>Repentance and Restoration</h3>
                <p>God's judgment aims at restoration, with calls to return to covenant faithfulness. The book presents God's willingness to forgive and restore those who genuinely repent.</p>

                <h3>The Day of the LORD</h3>
                <p>The prophetic anticipation of divine intervention brings both judgment for the wicked and vindication for the faithful. This eschatological focus places present circumstances in the context of God's ultimate purposes.</p>

                <h3>Messianic Hope</h3>
                <p>Promises of a coming deliverer point toward God's ultimate solution to human sin and suffering. These messianic prophecies maintain hope even in the darkest circumstances.</p>
                """
            else:
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Revelation</h3>
                <p>God communicates His character, will, and purposes through various means. This revelation provides the basis for knowing and responding to God appropriately.</p>

                <h3>Covenant Relationship</h3>
                <p>The formal relationship between God and His people establishes mutual commitments and expectations. This covenant framework shapes Israel's understanding of their identity and mission.</p>

                <h3>Human Responsibility</h3>
                <p>People are accountable for their response to divine revelation. The book explores the consequences of both obedience and disobedience to God's commands.</p>

                <h3>Divine Faithfulness</h3>
                <p>Despite human failures, God remains faithful to His promises and purposes. This divine commitment provides hope and confidence in God's ultimate redemptive work.</p>
                """
        else:  # New Testament
            if "gospel" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus is presented in various aspects of His identity and work—Son of God, Son of Man, Messiah, Savior, and Lord. These titles and roles reveal Jesus' unique relationship with the Father and His mission of redemption.</p>

                <h3>Kingdom of God</h3>
                <p>Jesus' proclamation and demonstration of God's reign reveals both its present reality and future consummation. The kingdom manifests in Jesus' teaching, miracles, exorcisms, and community formation.</p>

                <h3>Discipleship</h3>
                <p>Following Jesus involves more than intellectual assent, requiring transformed values, priorities, and relationships. True disciples demonstrate faith, obedience, and willingness to sacrifice.</p>

                <h3>Fulfillment</h3>
                <p>Jesus fulfills Old Testament prophecies, patterns, and promises, demonstrating continuity in God's redemptive plan. This fulfillment confirms Jesus' messianic identity and mission.</p>
                """
            elif "epistle" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus Christ's person and work form the foundation for Christian faith and practice. The book explores aspects of Christ's identity, incarnation, atoning death, resurrection, and present ministry.</p>

                <h3>Soteriology</h3>
                <p>Salvation through Christ involves multiple dimensions including justification, reconciliation, redemption, and sanctification. This salvation comes by grace through faith and transforms believers' identity and destiny.</p>

                <h3>Ecclesiology</h3>
                <p>The church as Christ's body has both unity and diversity, with various gifts contributing to the community's health and mission. Members have mutual responsibilities and share a common identity in Christ.</p>

                <h3>Ethics</h3>
                <p>Christian behavior flows from gospel transformation rather than mere rule-keeping. Ethical instructions address relationships, attitudes, speech, and conduct as expressions of new life in Christ.</p>
                """
            elif "apocalyptic" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Sovereignty</h3>
                <p>God remains in control despite apparent chaos and evil's temporary triumph. The heavenly perspective reveals that history moves according to divine purpose toward a predetermined conclusion.</p>

                <h3>Spiritual Conflict</h3>
                <p>The visible struggle between good and evil reflects a deeper cosmic conflict between God and Satan. This spiritual warfare affects both individuals and societies.</p>

                <h3>Faithful Witness</h3>
                <p>Believers are called to maintain loyalty to Christ despite persecution. This faithful testimony may involve suffering but ultimately participates in Christ's victory.</p>

                <h3>Final Judgment and Renewal</h3>
                <p>History culminates in divine judgment of evil and renewal of creation. This eschatological hope provides perspective and encouragement during present trials.</p>
                """
            else:
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus Christ's identity and work form the center of Christian faith. The book explores aspects of His person, ministry, and continuing significance for believers.</p>

                <h3>Soteriology</h3>
                <p>Salvation through Christ transforms believers' standing before God and daily experience. This redemptive work addresses sin's penalty, power, and ultimately its presence.</p>

                <h3>Ecclesiology</h3>
                <p>The church as God's people has a distinct identity and mission in the world. The community of believers demonstrates and proclaims God's redemptive purpose.</p>

                <h3>Eschatology</h3>
                <p>God's future promises provide hope and shape present priorities. The anticipated return of Christ and consummation of God's kingdom give perspective to current circumstances.</p>
                """

    return themes.get(book, """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Revelation</h3>
                <p>God communicates His character, will, and purposes through various means. This revelation provides the basis for knowing and responding to God appropriately.</p>

                <h3>Covenant Relationship</h3>
                <p>The formal relationship between God and His people establishes mutual commitments and expectations. This covenant framework shapes understanding of identity and mission.</p>

                <h3>Human Responsibility</h3>
                <p>People are accountable for their response to divine revelation. The book explores the consequences of both obedience and disobedience to God's commands.</p>

                <h3>Divine Faithfulness</h3>
                <p>Despite human failures, God remains faithful to His promises and purposes. This divine commitment provides hope and confidence in God's ultimate redemptive work.</p>
                """)


def generate_theological_significance(book):
    """Generate theological significance for a book"""

    # Book-specific theological significance
    theological = {
        "Exodus": """
        <p>Exodus develops several foundational theological concepts that influence the rest of Scripture:</p>

        <h3>Doctrine of God</h3>
        <p>Exodus significantly advances biblical revelation about God's nature and character. Through His self-disclosure to Moses as "I AM WHO I AM" (Exodus 3:14), God reveals His self-existence, self-sufficiency, and eternal presence. The divine name YHWH (the LORD) becomes central to Israel's understanding of God. Throughout Exodus, God demonstrates His attributes: power through plagues and miracles, faithfulness to covenant promises, justice in judgment on Egypt, mercy toward Israel despite their complaints, and holiness that requires mediated approach. The tension between divine transcendence (God's separateness on the mountain) and immanence (His dwelling among Israel) provides a balanced theology.</p>

        <h3>Doctrine of Salvation</h3>
        <p>The exodus event establishes the paradigm for understanding salvation throughout Scripture. It demonstrates that redemption begins with divine initiative and grace, not human merit. The Passover ritual, with its sacrificial lamb and blood protection, introduces substitutionary atonement concepts later fulfilled in Christ. Salvation in Exodus includes both deliverance from (Egyptian bondage) and deliverance to (covenant relationship and service). This holistic understanding counters reductionist views of salvation and highlights that redemption has both individual and corporate dimensions.</p>

        <h3>Doctrine of Covenant</h3>
        <p>Exodus develops the covenant concept introduced in Genesis, now expanded to include an entire nation. The Sinai covenant follows the pattern of ancient suzerain-vassal treaties, with historical prologue, stipulations, blessings/curses, and ratification ceremony. This covenant establishes Israel's unique relationship with God as a "kingdom of priests" (Exodus 19:5-6) and introduces the concept of covenant law as the grateful response to divine deliverance rather than a means of earning favor. The broken and renewed covenant (Exodus 32-34) demonstrates that divine faithfulness transcends human failure.</p>

        <h3>Doctrine of Worship</h3>
        <p>The tabernacle instructions and construction (Exodus 25-40) establish principles for appropriate worship. These include the need for divine prescription rather than human innovation, the centrality of sacrifice for approaching God, the role of designated mediators (priests), and the importance of visual symbols. The detailed regulations communicate both divine holiness and gracious accommodation to human limitations. The tabernacle system foreshadows Christ's greater fulfillment as sacrifice, priest, and meeting place between God and humanity.</p>
        """,

        "Genesis": """
        <p>Genesis establishes the foundational theological architecture for understanding the character of God, the nature of humanity, the origin of sin, and the hope of redemption. Every major doctrine of Scripture finds its seedbed in Genesis, making it indispensable for systematic theology:</p>

        <h3>Doctrine of God: Trinitarian Hints and Divine Attributes</h3>
        <p>Genesis reveals the one true God as utterly distinct from the polytheistic deities of surrounding nations. The Hebrew word Elohim (plural in form but singular in meaning) combined with the divine plurality statements ("Let us make man in our image," 1:26; "the man has become like one of us," 3:22; "let us go down," 11:7) provide early hints of the Trinity that will be fully revealed in the New Testament. God appears as self-existent ("I AM," implied in His eternal nature), transcendent (existing before and beyond creation), yet immanent (walking in the garden, speaking with the patriarchs). His attributes emerge progressively: omnipotence (creating by divine fiat), omniscience (knowing human thoughts and future events), omnipresence (seeing Hagar in the wilderness), immutability (His promises endure across generations), holiness (requiring justice for sin), and love (providing redemption and covenant relationship).</p>

        <h3>Doctrine of Humanity: Imago Dei and Constitutional Nature</h3>
        <p>The creation of humanity in God's image (1:26-27) establishes the fundamental theological anthropology for all Scripture. The image of God encompasses several dimensions: structural (possessing rational, moral, and spiritual capacities that reflect divine nature), functional (exercising dominion as God's representatives), and relational (designed for fellowship with God and others). Humans are created as psychosomatic unities—both material (formed from dust) and spiritual (breathed with divine breath)—establishing the biblical view of holistic human nature that opposes both materialistic reductionism and Platonic dualism. The divine blessing to "be fruitful and multiply" establishes marriage as a divine institution, while the cultural mandate to "subdue and rule" establishes work and cultural development as expressions of image-bearing.</p>

        <h3>Doctrine of Sin: Origin, Nature, and Consequences</h3>
        <p>Genesis 3 provides the biblical account of sin's entry into God's perfect creation, establishing the theological framework for understanding human moral corruption. Sin is presented not as metaphysical necessity but as historical catastrophe resulting from human choice to distrust God's word and seek autonomous moral authority. The consequences are comprehensive: spiritual death (broken fellowship with God), eventual physical death, relational discord (conflict between man and woman, parents and children), cosmic disruption (creation subjected to futility), and moral corruption (the heart's inclination toward evil). The progression from Genesis 3-11 demonstrates sin's exponential expansion from individual transgression to civilizational corruption, while the genealogies reveal death's universal reign over humanity.</p>

        <h3>Doctrine of Salvation: Protoevangelium and Covenant Grace</h3>
        <p>Genesis 3:15 introduces the protoevangelium ("first gospel"), promising that the woman's offspring will ultimately defeat the serpent though suffering in the process. This establishes the fundamental pattern of redemption through substitutionary suffering that culminates in Christ's work. The covenants with Noah and Abraham develop the theology of divine grace, revealing God's unilateral commitment to bless humanity despite their sinfulness. The Abrahamic covenant (Genesis 12, 15, 17, 22) establishes the framework for understanding election, calling, justification by faith, and the ultimate blessing of all nations through Abraham's offspring—promises fulfilled in Christ and extended to the church.</p>

        <h3>Doctrine of Providence: Divine Sovereignty and Human Responsibility</h3>
        <p>The Joseph narrative (chapters 37-50) provides the most extensive treatment of divine providence in Scripture, demonstrating how God sovereignly accomplishes His purposes through human choices without violating genuine human freedom or moral responsibility. Joseph's declaration that "you meant it for evil, but God meant it for good" (50:20) articulates the theological principle that God can use even sinful human actions to accomplish His redemptive purposes. This establishes the biblical framework for understanding suffering, divine justice, historical meaning, and ultimate hope while maintaining human accountability.</p>

        <h3>Doctrine of Worship: Acceptable Approach to God</h3>
        <p>Genesis establishes fundamental principles for approaching the holy God through worship. The contrast between Cain's rejected offering and Abel's accepted sacrifice introduces the necessity of approaching God according to divine prescription rather than human innovation, the centrality of substitutionary sacrifice in bridging the gap between sinful humanity and holy God, and the importance of faith in making worship acceptable to God. The patriarchal practice of altar-building and "calling on the name of the LORD" establishes covenantal worship patterns that prefigure the formal Mosaic system while emphasizing the primacy of faith and divine grace.</p>

        <h3>Doctrine of Eschatology: Promise and Ultimate Fulfillment</h3>
        <p>Genesis introduces the eschatological tension between promise and fulfillment that drives the entire biblical narrative. The promise of land to Abraham and his descendants points beyond geographical inheritance to the ultimate inheritance of the new earth. The promise of numerous offspring points beyond biological descendants to the spiritual offspring of faith from all nations. The promise that all nations will be blessed through Abraham's offspring points to the universal scope of redemption accomplished through Christ. The recurring theme of pilgrimage (Abraham's journey, Jacob's wrestling, Joseph's faith concerning his bones) establishes the spiritual principle that faith involves living in light of divine promises not yet fully realized.</p>

        <h3>Doctrine of Salvation</h3>
        <p>While Genesis does not fully develop soteriology, it lays essential groundwork through the first messianic prophecy (Genesis 3:15) and the covenant with Abraham. God's promise that Abraham's seed would bless all nations (Genesis 12:3, 22:18) becomes the foundation for understanding Christ's work. Genesis establishes the pattern of salvation by faith, particularly through Abraham who "believed God, and it was credited to him as righteousness" (Genesis 15:6).</p>

        <h3>Doctrine of Covenant</h3>
        <p>Genesis introduces divine covenants as the framework for God's relationship with humanity. The Noahic covenant (Genesis 9) establishes God's commitment to creation's stability, while the Abrahamic covenant (Genesis 12, 15, 17) introduces God's election of a particular family for universal blessing.</p>
        """
    }

    # Generate generic theological significance if specific content isn't available
    if book not in theological:
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            theological_content = f"""
            <p>{book} contributes significantly to biblical theology in several areas:</p>

            <h3>Understanding of God</h3>
            <p>The book reveals aspects of God's character and ways of working in history. Through divine actions, declarations, and interactions with humanity, {book} deepens our understanding of God's attributes and purposes.</p>

            <h3>Covenant Relationship</h3>
            <p>The book develops aspects of God's covenant relationship with Israel, showing both divine faithfulness and the consequences of human response. These covenant dynamics establish patterns that inform later biblical theology and find fulfillment in Christ.</p>

            <h3>Ethical Framework</h3>
            <p>Through both explicit commands and narrative examples, {book} contributes to the biblical understanding of righteous living. These ethical principles reflect God's character and establish standards that remain relevant for moral formation.</p>

            <h3>Messianic Anticipation</h3>
            <p>Various passages in {book} contribute to the developing messianic hope in Scripture. These elements find ultimate fulfillment in Christ, demonstrating the progressive nature of divine revelation and the unity of God's redemptive plan.</p>
            """
            return theological_content
        else:  # New Testament
            theological_content = f"""
            <p>{book} contributes significantly to biblical theology in several areas:</p>

            <h3>Christology</h3>
            <p>The book develops understanding of Jesus Christ's person and work, exploring aspects of His identity, mission, and continuing significance. These christological insights inform Christian faith and practice.</p>

            <h3>Soteriology</h3>
            <p>The book articulates aspects of salvation accomplished through Christ and applied by the Holy Spirit. This soteriological teaching addresses the full scope of redemption—past, present, and future.</p>

            <h3>Ecclesiology</h3>
            <p>Through both instruction and example, {book} shapes understanding of the church's nature, purpose, and practices. These ecclesiological insights guide Christian community life and mission.</p>

            <h3>Eschatology</h3>
            <p>The book contributes to biblical teaching about last things, including Christ's return, resurrection, judgment, and the new creation. This eschatological perspective provides hope and shapes present Christian living.</p>
            """
            return theological_content

    return theological.get(book, """
                <p>The book develops several significant theological concepts:</p>

                <h3>Divine Revelation</h3>
                <p>God communicates His character, will, and purposes through various means. This revelation provides the basis for knowing and responding to God appropriately.</p>

                <h3>Covenant Relationship</h3>
                <p>The formal relationship between God and His people establishes mutual commitments and expectations. This covenant framework shapes understanding of identity and mission.</p>

                <h3>Human Responsibility</h3>
                <p>People are accountable for their response to divine revelation. The book explores the consequences of both obedience and disobedience to God's commands.</p>

                <h3>Divine Faithfulness</h3>
                <p>Despite human failures, God remains faithful to His promises and purposes. This divine commitment provides hope and confidence in God's ultimate redemptive work.</p>
                """)


def generate_book_tags(book, genre):
    """Generate tags for a book based on its themes and genre"""
    # Base tags on genre
    genre_tags = {
        "narrative": ["Historical", "Narrative", "Story"],
        "law": ["Law", "Torah", "Covenant"],
        "poetry": ["Poetry", "Wisdom", "Lyrical"],
        "prophecy": ["Prophecy", "Prophetic", "Oracle"],
        "apocalyptic": ["Apocalyptic", "Symbolic", "Visionary"],
        "epistle": ["Epistle", "Letter", "Instruction"],
        "gospel": ["Gospel", "Biography", "Testimony"],
        "wisdom": ["Wisdom", "Proverb", "Teaching"]
    }

    # Book-specific tags
    book_specific_tags = {
        "Genesis": ["Creation", "Patriarchs", "Covenant", "Origins"],
        "Exodus": ["Deliverance", "Law", "Tabernacle", "Moses"],
        "Leviticus": ["Holiness", "Sacrifice", "Priesthood", "Ritual"],
        "Numbers": ["Wilderness", "Journey", "Census", "Rebellion"],
        "Deuteronomy": ["Covenant", "Law", "Moses", "Instruction"],
        "Joshua": ["Conquest", "Promised Land", "Leadership", "Victory"],
        "Judges": ["Cycle", "Deliverance", "Apostasy", "Tribalism"],
        "Ruth": ["Loyalty", "Redemption", "Kinsman-Redeemer", "Foreigner"],
        "1 Samuel": ["Kingship", "Saul", "David", "Transition"],
        "2 Samuel": ["David", "Kingdom", "Covenant", "Kingship"],
        "1 Kings": ["Solomon", "Temple", "Division", "Kings"],
        "2 Kings": ["Kings", "Prophets", "Exile", "Judgment"],
        "1 Chronicles": ["David", "Genealogy", "Temple", "Worship"],
        "2 Chronicles": ["Temple", "Kings", "Worship", "Reformation"],
        "Ezra": ["Return", "Restoration", "Temple", "Law"],
        "Nehemiah": ["Rebuilding", "Walls", "Reform", "Leadership"],
        "Esther": ["Providence", "Deliverance", "Courage", "Identity"],
        "Job": ["Suffering", "Wisdom", "Righteousness", "Divine Justice"],
        "Psalms": ["Worship", "Praise", "Lament", "Prayer"],
        "Proverbs": ["Wisdom", "Instruction", "Conduct", "Character"],
        "Ecclesiastes": ["Meaning", "Vanity", "Wisdom", "Purpose"],
        "Song of Solomon": ["Love", "Marriage", "Devotion", "Relationship"],
        "Isaiah": ["Holiness", "Messiah", "Judgment", "Restoration"],
        "Jeremiah": ["Judgment", "Covenant", "Restoration", "Prophet"],
        "Lamentations": ["Grief", "Judgment", "Mercy", "Destruction"],
        "Ezekiel": ["Glory", "Vision", "Judgment", "Restoration"],
        "Daniel": ["Kingdom", "Sovereignty", "Faithfulness", "Prophecy"],
        "Hosea": ["Faithfulness", "Covenant", "Redemption", "Apostasy"],
        "Joel": ["Day of the LORD", "Judgment", "Restoration", "Spirit"],
        "Amos": ["Justice", "Judgment", "Righteousness", "Prophecy"],
        "Obadiah": ["Judgment", "Pride", "Edom", "Restoration"],
        "Jonah": ["Mercy", "Mission", "Repentance", "Compassion"],
        "Micah": ["Justice", "Judgment", "Messiah", "Covenant"],
        "Nahum": ["Judgment", "Nineveh", "Justice", "Vengeance"],
        "Habakkuk": ["Faith", "Justice", "Sovereignty", "Questioning"],
        "Zephaniah": ["Day of the LORD", "Judgment", "Remnant", "Restoration"],
        "Haggai": ["Temple", "Priorities", "Restoration", "Blessing"],
        "Zechariah": ["Messiah", "Vision", "Restoration", "Future"],
        "Malachi": ["Covenant", "Faithfulness", "Offering", "Messenger"],
        "Matthew": ["Kingdom", "Messiah", "Fulfillment", "Teaching"],
        "Mark": ["Servant", "Action", "Suffering", "Discipleship"],
        "Luke": ["Savior", "Universal", "Social Justice", "Holy Spirit"],
        "John": ["Belief", "Life", "Word", "Signs"],
        "Acts": ["Church", "Holy Spirit", "Mission", "Growth"],
        "Romans": ["Righteousness", "Faith", "Grace", "Salvation"],
        "1 Corinthians": ["Unity", "Wisdom", "Gifts", "Love"],
        "2 Corinthians": ["Ministry", "Reconciliation", "Generosity", "Weakness"],
        "Galatians": ["Freedom", "Grace", "Faith", "Law"],
        "Ephesians": ["Unity", "Church", "Grace", "Spiritual Warfare"],
        "Philippians": ["Joy", "Humility", "Unity", "Contentment"],
        "Colossians": ["Supremacy", "Completeness", "Wisdom", "Freedom"],
        "1 Thessalonians": ["Encouragement", "Hope", "Faith", "Return"],
        "2 Thessalonians": ["Judgment", "Work", "Hope", "Perseverance"],
        "1 Timothy": ["Leadership", "Church Order", "Sound Doctrine", "Godliness"],
        "2 Timothy": ["Endurance", "Scripture", "Faithfulness", "Legacy"],
        "Titus": ["Good Works", "Leadership", "Sound Doctrine", "Grace"],
        "Philemon": ["Reconciliation", "Forgiveness", "Brotherhood", "Transformation"],
        "Hebrews": ["Superiority", "Faith", "Perseverance", "Covenant"],
        "James": ["Works", "Faith", "Wisdom", "Speech"],
        "1 Peter": ["Suffering", "Holiness", "Hope", "Identity"],
        "2 Peter": ["Knowledge", "False Teaching", "Day of the Lord", "Growth"],
        "1 John": ["Love", "Truth", "Fellowship", "Assurance"],
        "2 John": ["Truth", "Love", "Discernment", "Hospitality"],
        "3 John": ["Hospitality", "Truth", "Example", "Leadership"],
        "Jude": ["Contending", "Faith", "False Teaching", "Judgment"],
        "Revelation": ["Victory", "Judgment", "Worship", "New Creation"]
    }

    # Combine tags
    tags = []

    # Add genre tags
    for key in genre_tags.keys():
        if key in genre.lower():
            tags.extend(genre_tags[key])
            break

    # Add book-specific tags
    if book in book_specific_tags:
        tags.extend(book_specific_tags[book])

    # Return unique tags
    return list(set(tags))


def get_book_genre(book):
    """Return the literary genre of a book"""
    genres = {
        # Torah
        "Genesis": "Narrative with genealogy",
        "Exodus": "Narrative with law",
        "Leviticus": "Law and ritual instruction",
        "Numbers": "Narrative with law and census",
        "Deuteronomy": "Sermonic law",

        # Historical books
        "Joshua": "Historical narrative",
        "Judges": "Cyclical historical narrative",
        "Ruth": "Historical narrative",
        "1 Samuel": "Historical narrative",
        "2 Samuel": "Historical narrative",
        "1 Kings": "Historical narrative",
        "2 Kings": "Historical narrative",
        "1 Chronicles": "Historical narrative with genealogy",
        "2 Chronicles": "Historical narrative",
        "Ezra": "Historical narrative",
        "Nehemiah": "Historical narrative with memoir",
        "Esther": "Historical narrative",

        # Wisdom literature
        "Job": "Wisdom literature with poetic dialogue",
        "Psalms": "Poetry and liturgy",
        "Proverbs": "Wisdom literature",
        "Ecclesiastes": "Wisdom literature with philosophical reflection",
        "Song of Solomon": "Poetry and love song",

        # Major Prophets
        "Isaiah": "Prophetic literature with poetry",
        "Jeremiah": "Prophetic literature with biography",
        "Lamentations": "Poetic lament",
        "Ezekiel": "Prophetic literature with apocalyptic elements",
        "Daniel": "Narrative with apocalyptic visions",

        # Minor Prophets
        "Hosea": "Prophetic literature",
        "Joel": "Prophetic literature",
        "Amos": "Prophetic literature",
        "Obadiah": "Prophetic literature",
        "Jonah": "Prophetic narrative",
        "Micah": "Prophetic literature",
        "Nahum": "Prophetic literature",
        "Habakkuk": "Prophetic literature with dialogue",
        "Zephaniah": "Prophetic literature",
        "Haggai": "Prophetic literature",
        "Zechariah": "Prophetic literature with apocalyptic visions",
        "Malachi": "Prophetic literature with disputation",

        # Gospels
        "Matthew": "Gospel narrative",
        "Mark": "Gospel narrative",
        "Luke": "Gospel narrative with historiography",
        "John": "Gospel narrative with theology",

        # Acts
        "Acts": "Historical narrative",

        # Pauline Epistles
        "Romans": "Epistle with systematic theology",
        "1 Corinthians": "Epistle",
        "2 Corinthians": "Epistle",
        "Galatians": "Epistle",
        "Ephesians": "Epistle",
        "Philippians": "Epistle",
        "Colossians": "Epistle",
        "1 Thessalonians": "Epistle",
        "2 Thessalonians": "Epistle",
        "1 Timothy": "Pastoral epistle",
        "2 Timothy": "Pastoral epistle",
        "Titus": "Pastoral epistle",
        "Philemon": "Personal epistle",
        "Hebrews": "Epistle with sermonic elements",

        # General Epistles
        "James": "Epistle with wisdom elements",
        "1 Peter": "Epistle",
        "2 Peter": "Epistle",
        "1 John": "Epistle with theological discourse",
        "2 John": "Brief epistle",
        "3 John": "Brief epistle",
        "Jude": "Epistle",

        # Apocalyptic
        "Revelation": "Apocalyptic literature with epistle elements"
    }

    return genres.get(book, "Biblical literature")


def generate_book_introduction(book):
    """Generate introduction for a book"""
    # You would implement detailed logic here based on the book
    # This is a simplified version that would be expanded

    introductions = {
        "Genesis": """
        <p>Genesis stands as the magnificent opening movement of God's eternal symphony, establishing the foundational truths upon which all subsequent Scripture builds. The Hebrew title <em>Bereshith</em> ("In the beginning") and the Greek <em>Genesis</em> ("origin" or "generation") both capture the book's essential character as the account of beginnings—the universe, life, humanity, sin, redemption, and the covenant people of God. Traditionally attributed to Moses, who received both direct revelation and ancient records under divine inspiration, Genesis spans an extraordinary chronological range from creation (circa 4000 BCE) to Israel's settlement in Egypt (circa 1700 BCE), encompassing more historical time than any other biblical book.</p>

        <p>As the foundational document of the Pentateuch (Torah), Genesis establishes the theological architecture for understanding God's character, His relationship with creation, and His redemptive purposes. The book introduces and develops the great themes that echo throughout Scripture: divine sovereignty and human responsibility, creation and fall, judgment and grace, covenant faithfulness and human unfaithfulness, promise and fulfillment, election and mission. Every major theological concept in Scripture finds its seedbed in Genesis, making it indispensable for biblical theology.</p>

        <p>The literary structure of Genesis reveals careful theological artistry. The primeval history (chapters 1-11) addresses universal human concerns through a series of escalating crises: creation and fall (1-3), fratricide and civilization's corruption (4-6), judgment and new beginning through the flood (7-9), and the scattering at Babel (10-11). These narratives establish fundamental truths about God's nature, human nature, sin's consequences, and divine grace. The patriarchal narratives (chapters 12-50) then focus the universal scope onto God's particular covenant relationship with Abraham and his descendants, tracing the development of promise through four generations: Abraham (12-25), Isaac (25-26), Jacob (27-36), and Joseph (37-50).</p>

        <p>Genesis presents God as the sovereign Creator who speaks the universe into existence, the holy Judge who responds to sin with righteous judgment, the gracious Redeemer who provides covering for human shame and promises ultimate victory over evil, and the faithful Covenant-maker who binds Himself by promise to bless all nations through Abraham's offspring. The book's doctrine of humanity reveals both the dignity of image-bearing and the devastation of the fall, establishing the theological tension that drives the entire biblical narrative toward its resolution in Christ.</p>

        <p>Archaeological discoveries have illuminated many aspects of Genesis's ancient Near Eastern background while highlighting its distinctive theological perspectives. Unlike contemporaneous creation myths that depict chaotic divine conflicts, Genesis presents ordered creation by divine fiat. Where ancient flood stories feature capricious gods, Genesis reveals moral judgment and gracious preservation. The patriarchal narratives reflect accurate knowledge of second-millennium customs, geography, and social structures, supporting their historical reliability while emphasizing their theological significance.</p>

        <p>The book's theological significance extends far beyond historical narrative. Genesis provides the foundation for understanding the Trinity (with hints of divine plurality in creation), the nature of marriage and family, the origin and consequence of sin, the principle of substitutionary sacrifice, the covenant of grace, election and calling, divine providence, and eschatological hope. New Testament authors repeatedly return to Genesis for theological foundation, citing it more than any other Old Testament book except Psalms and Isaiah.</p>
        """,

        "Exodus": """
        <p>Exodus stands as one of the most theologically significant and historically foundational books in Scripture, chronicling the birth of Israel as a nation and establishing paradigms of redemption that resonate throughout biblical revelation. The Hebrew title <em>Shemoth</em> ("Names") reflects the book's opening genealogical connection to Genesis, while the Greek <em>Exodus</em> ("going out") captures the central redemptive event that defines Israel's identity and God's character as Redeemer. Traditionally attributed to Moses, who was uniquely qualified as both participant and recipient of divine revelation, Exodus spans approximately 80-90 years from Israel's oppression in Egypt through their formative period at Mount Sinai.</p>

        <p>As the pivotal second movement of the Pentateuch, Exodus transforms the family narrative of Genesis into the national epic of Israel, establishing the theological foundations for understanding covenant relationship, redemptive deliverance, divine law, and theocratic worship. The book's tri-partite structure reveals divine purpose: redemption from bondage (chapters 1-15), preparation for covenant (chapters 16-18), and establishment of covenant relationship with its attendant law and worship system (chapters 19-40). This structure establishes the biblical pattern of salvation (deliverance), sanctification (preparation), and service (covenant worship).</p>

        <p>The theological significance of Exodus cannot be overstated. It introduces the divine name YHWH with unprecedented fullness, revealing God's self-existence, covenant faithfulness, and redemptive character. The book establishes fundamental doctrines: the nature of divine calling and commissioning (Moses' burning bush encounter), the reality of spiritual warfare (the plagues as assault on Egyptian deities), the principle of substitutionary redemption (Passover), the nature of divine judgment and mercy (Red Sea deliverance), the character of divine law as expression of divine holiness, and the necessity of mediated approach to the holy God (priesthood and sacrificial system).</p>

        <p>Exodus profoundly shapes biblical understanding of redemption through its typological richness. The Passover lamb prefigures Christ as the Lamb of God, the Red Sea crossing anticipates baptism and deliverance from sin's dominion, the wilderness journey represents the believer's pilgrimage, manna symbolizes dependence on divine provision (fulfilled in Christ as bread of life), and the tabernacle system establishes the theology of divine presence, substitutionary sacrifice, and priestly mediation that finds ultimate fulfillment in Christ's work.</p>

        <p>Archaeological discoveries have confirmed many details of Exodus while illuminating its ancient Near Eastern context. The oppression narrative reflects accurate knowledge of Egyptian building projects, administrative practices, and social conditions during the New Kingdom period. The wilderness itinerary contains authentic geographical and topographical details. The tabernacle construction accounts demonstrate intimate familiarity with ancient craftsmanship and religious practices. Yet Exodus consistently presents Israel's experience as unique, emphasizing YHWH's supremacy over all competing claims to deity.</p>

        <p>The book's literary artistry enhances its theological message through careful structuring, vivid imagery, and dramatic tension. The plague narrative builds inexorably toward the climactic Passover, each plague demonstrating YHWH's sovereignty over a particular aspect of Egyptian religion. The Sinai theophany combines awesome transcendence with gracious covenant-making. The golden calf apostasy and subsequent restoration reveal both human sinfulness and divine mercy, establishing the pattern of covenant violation and renewal that characterizes Israel's subsequent history.</p>

        <p>Exodus establishes Israel's constitutional framework through the Mosaic Law, which encompasses moral principles (Ten Commandments), civil legislation (Book of the Covenant), and ceremonial regulations (tabernacle laws). This comprehensive legal system distinguishes Israel from surrounding nations while reflecting universal moral principles rooted in divine character. The law serves multiple purposes: revealing God's holiness, exposing human sinfulness, providing social order, and pointing toward ultimate redemption through the sacrificial system.</p>

        <p>The tabernacle, described in extraordinary detail, serves as the book's climax and theological center. Its elaborate construction demonstrates several crucial truths: God's desire to dwell among His people, the necessity of approaching the holy God according to divine prescription, the centrality of substitutionary sacrifice, the importance of priestly mediation, and the symbolic nature of worship that points beyond itself to eternal realities. The tabernacle's completion and the descent of divine glory (40:34-38) fulfills God's promise to dwell among His people and provides the theological foundation for understanding divine presence throughout Scripture.</p>
        """,

        "Revelation": """
        <p>Revelation stands as the magnificent crescendo of biblical revelation, the ultimate unveiling of God's eternal purposes and the triumphant conclusion of redemptive history. The Greek title <em>Apokalypsis</em> ("apocalypse" or "unveiling") captures the book's essential character as divine disclosure of hidden realities, while its alternative designation as "The Revelation of Jesus Christ" emphasizes both its christocentric focus and its origin in the risen Lord Himself. Written by John the Apostle during his exile on Patmos around 95 CE under Emperor Domitian's persecution, this prophetic masterpiece addresses seven churches in Asia Minor while providing a cosmic perspective on the spiritual warfare underlying human history and the certain victory of God's kingdom.</p>

        <p>As the Bible's primary apocalyptic work, Revelation employs the sophisticated literary conventions of Jewish apocalyptic literature while transcending them through its uncompromising Christian theology. The book operates on multiple levels simultaneously: it functions as an epistle to first-century churches, a prophecy concerning future events, and an apocalyptic vision of eternal realities. Its complex symbolic system draws from an extraordinary range of Old Testament sources—particularly Daniel, Ezekiel, Isaiah, and Zechariah—creating an intricate tapestry of intertextual allusions that requires deep biblical literacy to fully appreciate. The book contains over 400 Old Testament allusions while never directly quoting any passage, demonstrating the author's profound scriptural knowledge and sophisticated literary technique.</p>

        <p>The theological architecture of Revelation reveals careful structural design built around the number seven (appearing 54 times), symbolizing divine perfection and completeness. The book unfolds through a series of interconnected septets: seven churches (2-3), seven seals (6-8), seven trumpets (8-11), seven bowls (16), and seven beatitudes scattered throughout. This numerical symbolism extends to other significant numbers: twelve (representing the people of God), three and a half or 42 months or 1,260 days (representing the period of tribulation), and 144,000 (the symbolic number of the redeemed). These numerical patterns create a liturgical rhythm that enhances the book's use in worship while reinforcing its theological themes.</p>

        <p>Revelation's christology reaches the pinnacle of New Testament development, presenting Christ in multiple roles: the risen Lord walking among the lampstands (1), the slain Lamb who is worthy to open the sealed scroll (5), the conquering Lion of Judah (5), the faithful and true witness (19), the Word of God clothed in a robe dipped in blood (19), and the Alpha and Omega who makes all things new (21-22). This multifaceted portrait integrates Christ's first advent in humility with His second advent in glory, His sacrificial death with His royal victory, His identification with human suffering with His cosmic sovereignty. The famous image of the Lamb standing as though slain (5:6) paradoxically combines vulnerability and power, revealing that ultimate victory comes through redemptive suffering.</p>

        <p>The book's treatment of eschatology addresses both individual and cosmic destiny while maintaining productive tension between already/not yet fulfillment. The heavenly throne room scenes (4-5) establish God's eternal sovereignty and the Lamb's worthiness to execute divine purposes. The judgment sequences (seals, trumpets, bowls) reveal God's progressive response to persistent evil while maintaining space for repentance. The fall of Babylon (17-18) symbolizes the collapse of all systems opposed to God's rule. The millennium (20) represents the establishment of divine righteousness, however interpreted. The new heaven and earth (21-22) envision the ultimate transformation of creation into God's eternal dwelling place with His people.</p>

        <p>Archaeological and historical research has illuminated Revelation's first-century context while confirming its accurate knowledge of imperial ideology and local conditions. The seven cities addressed were major centers along the Roman postal route in Asia Minor, each facing specific challenges from emperor worship, trade guild requirements, and social pressure to compromise Christian distinctives. Emperor Domitian's demand for divine honors created particular tension for Christians whose exclusive loyalty to Christ as Lord conflicted with imperial claims to divinity. The book's political symbolism, while encoded for protection, clearly presents Christ as the true Caesar and God's kingdom as the ultimate imperium.</p>

        <p>The literary artistry of Revelation employs sophisticated techniques including chiastic structure, recapitulation, progressive parallelism, and telescoping visions. The trumpet and bowl judgments follow similar patterns while intensifying in severity. The woman clothed with the sun (12) and the harlot Babylon (17) present contrasting images of faithful and unfaithful community. The marriage supper of the Lamb (19) and the holy city descending from heaven (21) provide climactic images of consummated union between God and His people. These literary patterns reinforce the book's theological message while creating memorable imagery for liturgical and devotional use.</p>

        <p>Revelation's influence on Christian thought, worship, and culture has been immeasurable, inspiring countless artistic works, musical compositions, architectural designs, and theological reflections. Its hymnic passages have enriched Christian liturgy from ancient times, while its vivid imagery has provided hope for persecuted believers throughout church history. The book's emphasis on divine sovereignty provides comfort in times of chaos, its call to faithful witness challenges complacency, and its vision of ultimate renewal sustains hope for cosmic restoration.</p>

        <p>The theological synthesis of Revelation brings the entire biblical narrative to its intended conclusion, resolving the tensions introduced in Genesis and developed throughout Scripture. The tree of life, lost in Eden, reappears in the new Jerusalem. The curse pronounced after the fall is finally removed. The scattered nations of Babel are gathered in harmonious worship. The promise to Abraham that all nations would be blessed through his offspring finds ultimate fulfillment as the nations walk by the light of the Lamb. Death, the last enemy, is finally destroyed. The dwelling of God is with humanity, and they shall be His people, and God Himself will be with them and be their God—the ultimate fulfillment of the covenant promise that echoes throughout Scripture.</p>
        """
    }

    # Get a template introduction based on genre if specific introduction isn't available
    if book not in introductions:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        # Generate a generic introduction based on testament and genre
        if "narrative" in genre.lower():
            intro = f"""
            <p>{book} is a narrative book in the {testament} that recounts key historical events and developments in Israel's history. The book contains important stories, characters, and events that contribute to the broader biblical narrative and redemptive history.</p>

            <p>As with other biblical narratives, {book} combines historical reporting with theological interpretation, showing how God works through historical circumstances and human actions to accomplish His purposes. The narrative demonstrates divine providence, human responsibility, and the consequences of both obedience and disobedience.</p>

            <p>Throughout {book}, readers can observe God's faithfulness to His covenant promises despite human failings and opposition. The book's events establish important precedents and patterns that inform biblical theology and provide context for understanding later Scriptural developments.</p>
            """
        elif "epistle" in genre.lower():
            intro = f"""
            <p>{book} is an epistle (letter) in the {testament} written to address specific circumstances, challenges, and questions in the early Christian church. The letter combines theological instruction with practical exhortation, demonstrating the connection between Christian doctrine and everyday living.</p>

            <p>Like other New Testament epistles, {book} addresses particular situations while establishing principles with broader application. The letter reflects the apostolic authority of its author and the normative teaching of the early church, contributing to the development of Christian theology and practice.</p>

            <p>Throughout {book}, readers can observe the practical outworking of the gospel in community life, personal ethics, and spiritual development. The letter demonstrates how Christ's finished work transforms individual believers and reshapes their relationships and priorities.</p>
            """
        elif "prophetic" in genre.lower() or "prophecy" in genre.lower():
            intro = f"""
            <p>{book} is a prophetic book in the {testament} that communicates divine messages of warning, judgment, and hope to God's people. The prophecies combine historical relevance to their original audience with enduring theological significance and, in some cases, messianic predictions.</p>

            <p>Like other biblical prophetic literature, {book} addresses covenant violations, calls for repentance, and proclaims both divine judgment and promised restoration. The prophecies demonstrate God's righteousness, sovereignty over history, and faithful commitment to His covenant purposes.</p>

            <p>Throughout {book}, readers encounter powerful imagery, poetic language, and symbolic actions that reinforce the prophetic message. The book reveals God's perspective on historical events and human affairs, often challenging conventional wisdom and cultural assumptions.</p>
            """
        elif "wisdom" in genre.lower():
            intro = f"""
            <p>{book} is a wisdom book in the {testament} that addresses life's fundamental questions and provides guidance for righteous living. The book explores themes of divine order, human experience, and practical ethics, offering insights for navigating the complexities of human existence.</p>

            <p>Like other biblical wisdom literature, {book} emphasizes the fear of the Lord as the foundation of true wisdom and contrasts the paths of wisdom and folly. The book demonstrates how reverence for God leads to discernment, virtue, and ultimately flourishing.</p>

            <p>Throughout {book}, readers encounter profound reflections on creation's order, human limitations, moral principles, and life's meaning. The book bridges theological truth and practical living, showing how divine wisdom applies to everyday decisions and relationships.</p>
            """
        elif "gospel" in genre.lower():
            intro = f"""
            <p>{book} is a gospel account in the {testament} that presents the life, ministry, death, and resurrection of Jesus Christ. The book combines historical reporting with theological interpretation, portraying Jesus as the fulfillment of Old Testament promises and the inaugurator of God's kingdom.</p>

            <p>Like other canonical gospels, {book} selectively records Jesus' words and deeds to communicate His identity and significance. The narrative demonstrates Jesus' divine authority, redemptive mission, and transformative teaching, inviting readers to respond in faith.</p>

            <p>Throughout {book}, readers encounter Jesus' interactions with various individuals and groups, His powerful parables and discourses, and the climactic events of His passion and resurrection. The book establishes the historical foundation for Christian faith while interpreting Jesus' significance for all humanity.</p>
            """
        elif "apocalyptic" in genre.lower():
            intro = f"""
            <p>{book} is an apocalyptic book in the {testament} that unveils spiritual realities and future events through symbolic visions and prophetic declarations. The book employs rich imagery and symbolic language to communicate divine perspective on history, cosmic conflict, and ultimate outcomes.</p>

            <p>Like other biblical apocalyptic literature, {book} addresses contexts of suffering and persecution, offering hope through the assurance of God's sovereignty and eventual triumph. The visions demonstrate the temporary nature of evil powers and the certainty of divine judgment and redemption.</p>

            <p>Throughout {book}, readers encounter dramatic portrayals of spiritual warfare, divine intervention, and eschatological consummation. The book provides a cosmic framework for understanding present trials and maintaining faithful endurance through the assurance of God's ultimate victory.</p>
            """
        else:
            intro = f"""
            <p>{book} is an important book in the {testament} that contributes significantly to the biblical canon. The book addresses themes and concerns relevant to its original audience while establishing principles and patterns with enduring theological significance.</p>

            <p>As with other biblical literature, {book} combines historical awareness with divine inspiration, communicating God's truth through human language and cultural forms. The book demonstrates the progressive nature of divine revelation and its adaptation to specific historical contexts.</p>

            <p>Throughout {book}, readers can trace important developments in the biblical narrative and theological understanding. The book provides essential insights for comprehending God's character, purposes, and relationship with humanity.</p>
            """

        return intro

    return introductions[book]


def generate_historical_context(book):
    """Generate historical context for a book"""
    historical_contexts = {
        "Genesis": """
        <p>Genesis was compiled and written by Moses around 1440-1400 BCE according to traditional attribution, though the events it records span an extraordinary chronological range from creation to approximately 1700 BCE when Israel settled in Egypt. The book was composed for the Israelites after their exodus from Egypt as they prepared to enter the Promised Land, providing them with their theological and historical foundation as the people of God. Archaeological evidence and textual analysis support Mosaic authorship while allowing for minor editorial updates during later periods.</p>

        <h3>Ancient Near Eastern Cultural Milieu</h3>
        <p>The world of Genesis was dominated by sophisticated civilizations in Mesopotamia, Egypt, and Canaan, each contributing to the complex cultural matrix within which the patriarchs lived and moved. The Sumerian civilization (c. 3500-2000 BCE) had established urban centers, developed cuneiform writing, created elaborate temple complexes (ziggurats), and produced extensive literature including creation myths, flood narratives, and wisdom literature. The Akkadian Empire (c. 2334-2154 BCE) unified Mesopotamia under Sargon and his successors, creating the first multi-ethnic empire and spreading Semitic languages throughout the region.</p>

        <p>Egypt during the patriarchal period experienced the grandeur of the Old Kingdom (c. 2686-2181 BCE) with its pyramid construction, followed by the Middle Kingdom (c. 2055-1650 BCE) when the patriarchs likely entered Egypt. Egyptian religion was sophisticated and pervasive, with elaborate funeral practices, temple rituals, and a complex pantheon headed by Ra, Ptah, and Amun. The pharaoh was considered divine, creating a theological environment radically different from the monotheism of the patriarchs.</p>

        <h3>Comparative Literature and Distinctive Theology</h3>
        <p>Genesis shares certain structural and thematic similarities with ancient Near Eastern literature while maintaining fundamental theological distinctions. The Enuma Elish (Babylonian creation epic) describes creation through divine conflict and the establishment of Marduk's supremacy, contrasting sharply with Genesis's peaceful creation through divine fiat. The Epic of Gilgamesh contains a flood narrative (Utnapishtim) with remarkable parallels to Noah's account, yet the biblical version emphasizes moral judgment and divine covenant rather than capricious divine annoyance.</p>

        <p>The Atrahasis Epic provides another flood account emphasizing overpopulation and divine irritation, while Genesis focuses on moral corruption and divine justice. Sumerian King Lists mention extraordinarily long lifespans for antediluvian rulers, paralleling Genesis's pre-flood longevity accounts. The Mesopotamian creation account in Genesis 2 uses geographical references (Tigris, Euphrates, Pishon, Gihon) that reflect intimate knowledge of ancient river systems and geography.</p>

        <h3>Archaeological Illumination</h3>
        <p>Archaeological discoveries have dramatically illuminated the Genesis narratives while confirming their historical reliability. The Nuzi tablets (15th-14th centuries BCE) reveal social customs that precisely match patriarchal practices: adoption procedures, inheritance laws, marriage customs, and property transactions described in Genesis. The Mari archives (18th century BCE) document the semi-nomadic lifestyle, tribal movements, and personal names that characterize the patriarchal period.</p>

        <p>Excavations at sites like Ur, Haran, Shechem, Hebron, and Beersheba have revealed extensive Middle Bronze Age occupation during the patriarchal period. The discovery of the Ebla tablets (c. 2400-2250 BCE) has provided numerous parallels to early Genesis, including place names, personal names, and cultural practices. Egyptian records from the Middle Kingdom period document Asiatic immigration into Egypt, providing the historical context for Jacob's family settlement in Goshen.</p>

        <h3>Religious and Social Context</h3>
        <p>The religious environment of the ancient Near East was thoroughly polytheistic, with elaborate temple systems, professional priesthoods, and complex mythologies explaining natural phenomena and human existence. Each city-state typically had a patron deity with associated temples, festivals, and ritual requirements. The concept of covenant relationships between deities and peoples was common, though these typically involved mutual obligations and were often temporary or conditional.</p>

        <p>Social structures were hierarchical and patriarchal, with extended family units (bet ab - "father's house") forming the basic social unit. Marriage customs included bride-price, polygamy among the wealthy, and complex inheritance laws favoring male primogeniture. The practice of adoption was common for childless couples, and the rights of the firstborn carried significant legal and social weight. Genesis accurately reflects these cultural patterns while subverting them through divine election and covenant promise.</p>

        <h3>Linguistic and Literary Features</h3>
        <p>Genesis exhibits archaic Hebrew linguistic features consistent with early composition, including ancient poetic structures (like Jacob's blessing in chapter 49), primitive narrative techniques, and vocabulary that reflects contact with both Mesopotamian and Egyptian cultures. The use of different divine names (Elohim, YHWH, El Shaddai) reflects sophisticated theological understanding rather than documentary fragmentation, as each name emphasizes different aspects of divine character appropriate to specific contexts.</p>

        <p>The toledot ("generations") structure that organizes Genesis reflects ancient genealogical and historiographical practices found throughout the ancient Near East. The narrative's concern with genealogy, chronology, and geographical precision demonstrates the author's intent to provide historical rather than merely mythological material. The literary artistry evident in the patriarchal narratives—including wordplay, symmetry, and thematic development—reveals sophisticated compositional technique consistent with ancient scribal education.</p>

        <h3>Cultural Background</h3>
        <p>The patriarchs (Abraham, Isaac, and Jacob) lived as semi-nomadic herdsmen, moving between established city-states in Canaan. Their lifestyle involved seasonal migration with flocks and herds, establishing temporary settlements, and digging wells. Kinship ties were paramount, with extended family groups (clans) forming the basic social unit.</p>

        <p>Marriage customs included bride prices, arranged marriages, and occasionally polygamy, especially when a first wife was barren. Inheritance typically passed to the firstborn son, though Genesis records several instances where this pattern was divinely overturned.</p>

        <h3>Archaeological Insights</h3>
        <p>Archaeological discoveries have illuminated many aspects of the Genesis narratives. Excavations at sites like Ur (Abraham's birthplace) reveal a sophisticated urban center. Tablets from Mari and Nuzi document social customs similar to those practiced by the patriarchs, including adoption agreements, surrogacy arrangements, and covenant ceremonies.</p>

        <p>Egypt's Middle Kingdom period (2040-1782 BCE) provides the likely background for Joseph's rise to prominence. Historical records show that Semitic people did indeed achieve high positions in Egyptian administration, and periods of famine are documented in Egyptian history.</p>
        """,

        "Exodus": """
        <p>Exodus emerges from the historical setting of Egyptian dominance and Israelite oppression during the second millennium BCE. Traditional dating places the exodus event around 1446 BCE (based on 1 Kings 6:1), though some scholars prefer a later date around 1270-1260 BCE during Rameses II's reign.</p>

        <h3>Egyptian Background</h3>
        <p>The Egypt of Exodus was a sophisticated civilization with monumental architecture, complex religious systems, and highly centralized government. The unnamed pharaoh likely ruled during Egypt's New Kingdom period (1550-1070 BCE), a time of imperial expansion and extensive building projects requiring massive labor forces. Egyptian records confirm the use of Semitic slaves for construction, and archaeological evidence from sites like Pi-Rameses aligns with biblical descriptions of brick-making with straw.</p>

        <p>Egyptian religion centered on a vast pantheon of deities associated with natural forces. The pharaoh claimed divine status as the incarnation of Horus and son of Ra, providing context for the cosmic theological conflict underlying the plagues, each targeting specific Egyptian gods. This religious background illuminates why Pharaoh repeatedly hardened his heart despite mounting evidence of YHWH's superior power.</p>

        <h3>Israelite Situation</h3>
        <p>The Israelites had grown from Jacob's family of 70 persons to a multitude large enough to threaten Egyptian security (Exodus 1:7-10). Archaeological evidence from the eastern Nile Delta (biblical Goshen) confirms Semitic settlements during this period. Their transition from honored guests (due to Joseph's position) to enslaved laborers likely occurred with a dynastic change—"a new king...who did not know about Joseph" (Exodus 1:8).</p>

        <p>The forced labor conditions described in Exodus are consistent with Egyptian practices for foreign populations. Israelite identity during this period was primarily tribal and familial rather than national. The exodus event would become foundational for their emerging national identity and self-understanding as a people set apart by divine election and deliverance.</p>

        <h3>Wilderness Context</h3>
        <p>The Sinai Peninsula, where Israel journeyed after leaving Egypt, was sparsely populated and largely controlled by Egypt through mining operations and military outposts. The harsh desert environment required divine provision for survival, emphasizing Israel's dependence on God. Egyptian records confirm the presence of Semitic peoples in this region during the second millennium BCE.</p>

        <p>Mount Sinai (possibly Jebel Musa in traditional identification) provided an appropriately awesome setting for divine revelation. The theophanic manifestations described in Exodus—thunder, lightning, earthquake, fire, and cloud—align with the dramatic landscape of the Sinai mountains. This wilderness experience would become paradigmatic for Israel's understanding of pilgrimage, testing, and dependence on divine grace.</p>
        """,

        "Leviticus": """
        <p>Leviticus was written by Moses during Israel's wilderness sojourn at Mount Sinai (c. 1446-1406 BCE). The book contains instructions given while the Israelites camped at Sinai for approximately eleven months, between their arrival and departure recorded in Exodus and Numbers respectively.</p>

        <h3>Ancient Near Eastern Worship</h3>
        <p>Leviticus addresses Israel's worship in a world dominated by elaborate pagan ritual systems. Surrounding Canaanite religions involved child sacrifice, temple prostitution, and syncretistic practices mixing agricultural fertility concerns with worship. Egyptian religion featured complex ritual systems managed by professional priestly classes, while Mesopotamian cultures maintained elaborate temple complexes with detailed sacrificial regulations.</p>

        <p>Archaeological discoveries at sites like Ugarit have revealed ritual texts paralleling some Levitical procedures while highlighting distinctive differences. Israel's sacrificial system emphasized moral purity and covenant relationship rather than manipulation of divine powers for agricultural fertility or military success.</p>

        <h3>Socio-Religious Context</h3>
        <p>The tabernacle system described in Leviticus provided Israel with a portable worship center suitable for wilderness conditions and eventual settlement in Canaan. This mobility distinguished Israel's worship from the fixed temple complexes typical of ancient Near Eastern religions tied to specific geographical locations.</p>

        <p>The holiness code (Leviticus 17-26) addressed Israel's need for distinctive identity amid Canaanite influences. These laws governed diet, sexual practices, social relationships, and religious observances, creating clear boundaries between Israel and surrounding peoples while emphasizing ethical behavior as worship expression.</p>
        """,

        "Numbers": """
        <p>Numbers covers approximately 38 years of Israel's wilderness wandering (c. 1446-1408 BCE), from the organization at Sinai through arrival at the plains of Moab. The book records two generations: the exodus generation that died in the wilderness due to unbelief, and their children who would enter the Promised Land.</p>

        <h3>Wilderness Geography</h3>
        <p>The Sinai Peninsula provided a harsh training ground for transforming escaped slaves into a military and religious community. The region's scarce water sources, extreme temperatures, and limited vegetation required constant dependence on divine provision. Egyptian texts confirm knowledge of wilderness routes and oasis locations that align with biblical descriptions.</p>

        <p>The wilderness setting isolated Israel from cultural contamination while providing space for national formation. The forty-year duration allowed time for the slave mentality to die out and for new leadership to emerge under divine instruction.</p>

        <h3>Political Context</h3>
        <p>Israel's wilderness journey occurred during Egyptian dominance over Canaan and the Transjordan. The encounters with Edom, Moab, and Ammon reflect complex kinship relationships and territorial disputes typical of the Late Bronze Age. The victory over Sihon and Og represents Israel's first military successes against established kingdoms, demonstrating divine enablement for conquest.</p>
        """,

        "Deuteronomy": """
        <p>Deuteronomy records Moses' final speeches to Israel on the plains of Moab (c. 1406 BCE) as they prepared to enter Canaan under Joshua's leadership. The setting emphasizes transition between generations and leadership, with explicit preparation for life in the Promised Land.</p>

        <h3>Treaty Form</h3>
        <p>Deuteronomy follows the structure of ancient Near Eastern suzerain-vassal treaties, particularly Hittite forms from the second millennium BCE. This includes historical prologue, stipulations, blessings and curses, and provisions for covenant renewal. This format would have been familiar to ancient audiences and emphasizes the covenant relationship between God and Israel.</p>

        <h3>Canaanite Context</h3>
        <p>The warnings against Canaanite religious practices in Deuteronomy reflect archaeological knowledge of Late Bronze Age Canaanite culture. Excavations at sites like Hazor, Megiddo, and Lachish reveal the sophisticated urban civilization Israel would encounter. Canaanite religion involved Baal worship, Asherah poles, high places, and child sacrifice—practices explicitly forbidden in Deuteronomy.</p>

        <p>The transition from nomadic to settled life required new legal and social structures. Deuteronomy's laws address agricultural life, urban governance, military organization, and judicial procedures appropriate for the sedentary lifestyle Israel would adopt in Canaan.</p>
        """,

        "Joshua": """
        <p>Joshua records Israel's conquest and settlement of Canaan (c. 1406-1375 BCE) during the Late Bronze Age collapse. Archaeological evidence suggests widespread destruction of Canaanite cities during this period, though dating and attribution remain debated among scholars.</p>

        <h3>Canaanite Civilization</h3>
        <p>Late Bronze Age Canaan consisted of independent city-states with sophisticated urban centers, advanced metallurgy, and international trade connections. The Amarna Letters from Egypt reveal political instability and frequent warfare among Canaanite rulers, creating opportunities for Israelite settlement.</p>

        <p>Canaanite religion centered on fertility deities like Baal and Asherah, with worship involving ritual prostitution, child sacrifice, and seasonal festivals. Archaeological discoveries at Ugarit provide extensive documentation of Canaanite mythology and ritual practices that Joshua's conquest aimed to eliminate.</p>

        <h3>Military Context</h3>
        <p>Bronze Age warfare typically involved siege techniques, chariot warfare, and professional armies. Israel's success despite inferior technology and numbers emphasizes divine enablement. The destruction of Jericho and Ai demonstrates unconventional military tactics guided by divine strategy rather than standard Bronze Age siege methods.</p>
        """,

        "Judges": """
        <p>Judges covers the period from Joshua's death to Samuel's ministry (c. 1375-1050 BCE), characterized by political decentralization, religious syncretism, and cyclical foreign oppression. This era represents Israel's troubled transition from conquest to monarchy.</p>

        <h3>Iron Age Transition</h3>
        <p>The Judges period coincides with the Late Bronze Age collapse and emergence of Iron Age technology. The Philistine settlement in coastal Canaan brought advanced military technology and political organization that challenged Israelite tribal confederation. Archaeological evidence shows Philistine material culture distinct from both Canaanite and Israelite traditions.</p>

        <h3>Tribal Society</h3>
        <p>Israel during Judges maintained a decentralized tribal confederation without central authority. This system worked during external threats (when judges provided temporary leadership) but failed to maintain covenant faithfulness during peaceful periods. The repeated cycle of apostasy, oppression, repentance, and deliverance reflects the instability of pre-monarchic Israel.</p>

        <p>Archaeological surveys reveal scattered highland settlements consistent with early Israelite material culture. These small, agricultural communities lacked the urban sophistication of Canaanite city-states but demonstrated gradual territorial expansion and cultural development.</p>
        """,

        "Ruth": """
        <p>Ruth is set during the Judges period (c. 1100 BCE) but was likely written later, possibly during David's reign or the early monarchy. The story provides insight into rural life, legal customs, and social relationships during Israel's pre-monarchic period.</p>

        <h3>Agricultural Context</h3>
        <p>The narrative reflects the agricultural rhythms of ancient Palestine, with barley and wheat harvests providing seasonal structure. The gleaning laws mentioned in Ruth demonstrate social welfare provisions protecting widows, orphans, and foreigners. Archaeological evidence confirms agricultural practices described in the book.</p>

        <h3>Legal Background</h3>
        <p>The kinsman-redeemer (goel) institution reflected in Ruth represents ancient Near Eastern family law designed to preserve property within clan structures. Similar legal concepts appear in Mesopotamian law codes, though Israel's implementation emphasized covenant community values and care for vulnerable members.</p>
        """,

        "1 Samuel": """
        <p>1 Samuel covers Israel's transition from tribal confederation to monarchy (c. 1050-1010 BCE), focusing on Samuel's judgeship, Saul's reign, and David's rise. This period represents fundamental changes in Israel's political and religious structure.</p>

        <h3>Philistine Pressure</h3>
        <p>The Philistines arrived in Canaan around 1200 BCE as part of the Sea Peoples movement. They established a pentapolis (five-city confederation) along the coastal plain and maintained technological superiority through iron weapons and military organization. Philistine pressure forced Israel to abandon tribal confederation in favor of centralized monarchy.</p>

        <h3>Religious Transition</h3>
        <p>The capture of the ark (1 Samuel 4) and destruction of Shiloh marked the end of the tabernacle period and transition to new worship arrangements. Samuel's circuit ministry and David's eventual establishment of Jerusalem as the religious center reflect changing religious organization during this period.</p>
        """,

        "2 Samuel": """
        <p>2 Samuel records David's reign over Judah (seven years) and united Israel (thirty-three years, c. 1010-970 BCE). This period marked Israel's emergence as a regional power and the establishment of Jerusalem as the political and religious center.</p>

        <h3>Political Context</h3>
        <p>David's reign occurred during a power vacuum in the ancient Near East. Egyptian and Mesopotamian empires were weak, allowing Israel to expand and control trade routes. Archaeological evidence from sites like Megiddo and Hazor shows destruction levels consistent with Davidic expansion.</p>

        <h3>Jerusalem's Significance</h3>
        <p>David's capture of Jerusalem from the Jebusites provided a neutral capital between northern and southern tribes. The city's strategic location, defensible position, and lack of tribal associations made it ideal for unifying the kingdom. Archaeological excavations in Jerusalem continue to illuminate David's city.</p>
        """,

        "1 Kings": """
        <p>1 Kings covers Solomon's reign and the kingdom's division (c. 970-853 BCE), from Israel's golden age through the beginning of the divided monarchy. This period saw unprecedented prosperity followed by civil war and political fragmentation.</p>

        <h3>Solomon's Golden Age</h3>
        <p>Solomon's reign represented ancient Israel's apex of wealth, wisdom, and international prestige. Archaeological evidence from Megiddo, Hazor, and Gezer confirms Solomonic building projects. The temple construction utilized Phoenician expertise and materials, reflecting Israel's integration into international trade networks.</p>

        <h3>Division Context</h3>
        <p>The kingdom's division resulted from economic burdens, tribal tensions, and religious issues. The northern kingdom (Israel) controlled more territory and trade routes but lacked Jerusalem's religious legitimacy. The southern kingdom (Judah) maintained Davidic succession and temple worship but had limited economic resources.</p>
        """,

        "2 Kings": """
        <p>2 Kings chronicles the divided monarchy through both kingdoms' destruction (c. 853-560 BCE), ending with Jehoiachin's release from Babylonian prison. This period witnessed the rise of Assyrian and Babylonian empires that ultimately conquered both Israel and Judah.</p>

        <h3>Assyrian Period</h3>
        <p>Assyrian expansion westward began seriously under Shalmaneser III (858-824 BCE). The northern kingdom fell to Assyria in 722 BCE under Sargon II, with massive deportation of population. Assyrian records confirm biblical accounts of tribute payments and military campaigns.</p>

        <h3>Babylonian Conquest</h3>
        <p>Nebuchadnezzar II's campaigns against Judah (605, 597, 586 BCE) culminated in Jerusalem's destruction and exile. Babylonian records document these campaigns, while archaeological evidence from sites like Lachish confirms the destruction described in 2 Kings.</p>
        """,

        "1 Chronicles": """
        <p>1 Chronicles was written during the post-exilic period (c. 430-400 BCE) to encourage returning exiles by emphasizing David's legacy, temple worship, and covenant promises. The author (traditionally identified as Ezra) reinterpreted Israel's history for a community rebuilding their identity.</p>

        <h3>Post-Exilic Context</h3>
        <p>The Persian Empire's policy of religious tolerance allowed Jewish return and temple reconstruction. However, the community faced challenges including limited resources, hostile neighbors, and questions about identity and divine favor. Chronicles addresses these concerns by emphasizing continuity with pre-exilic Israel.</p>
        """,

        "2 Chronicles": """
        <p>2 Chronicles continues the post-exilic reinterpretation of Israel's monarchy, focusing on temple worship, religious reforms, and God's faithfulness despite national failure. The book concludes with Cyrus's decree allowing Jewish return, providing hope for restoration.</p>

        <h3>Temple Focus</h3>
        <p>The chronicler's emphasis on temple worship addressed post-exilic concerns about proper religious observance. The detailed attention to Solomon's temple construction and various reforming kings provided models for the rebuilt temple community under Persian rule.</p>
        """,

        "Ezra": """
        <p>Ezra records the first return from Babylonian exile under Zerubbabel (538 BCE) and Ezra's later mission (458 BCE). These events occurred during Persian rule when Cyrus's policy allowed subjugated peoples to return to their homelands and rebuild their temples.</p>

        <h3>Persian Administration</h3>
        <p>The Persian Empire governed through local authorities while maintaining overall control. The Elephantine Papyri provide contemporary documentation of Jewish communities under Persian rule, including religious practices and administrative procedures that illuminate Ezra's narrative.</p>

        <h3>Religious Restoration</h3>
        <p>Ezra's emphasis on law observance and separation from foreign wives addressed identity preservation concerns. The small Jewish community in Judah needed clear boundaries to maintain covenant distinctiveness while living under foreign rule.</p>
        """,

        "Nehemiah": """
        <p>Nehemiah records the rebuilding of Jerusalem's walls (445 BCE) and subsequent reforms under Nehemiah's governorship. This occurred during Artaxerxes I's reign when Persian policy supported local reconstruction projects that enhanced imperial security.</p>

        <h3>Political Context</h3>
        <p>Nehemiah's position as cupbearer to Artaxerxes provided access to imperial authority. The wall rebuilding faced opposition from neighboring officials who feared Jewish resurgence might threaten their territorial interests. Archaeological evidence confirms destruction and rebuilding of Jerusalem's fortifications during this period.</p>
        """,

        "Esther": """
        <p>Esther is set during the reign of Ahasuerus (Xerxes I, 486-465 BCE) in the Persian capital of Susa. The story addresses the situation of Jews who remained in the diaspora rather than returning to Judah, showing God's providential care for scattered covenant people.</p>

        <h3>Persian Court Life</h3>
        <p>Archaeological excavations at Susa have revealed the magnificent palace complex described in Esther. Persian administrative records document the complex bureaucracy and communication systems that feature in the narrative. The book accurately reflects Persian customs, titles, and governmental procedures.</p>
        """,

        "Job": """
        <p>Job's setting reflects the patriarchal period (c. 2000-1800 BCE), though the book's composition may be later. The story occurs in the land of Uz, possibly in northern Arabia or southern Syria, among pastoral peoples contemporary with Abraham.</p>

        <h3>Wisdom Literature Context</h3>
        <p>Job belongs to the international wisdom tradition evident throughout the ancient Near East. Similar wisdom texts from Egypt, Mesopotamia, and Canaan address suffering, divine justice, and human limitations. However, Job's monotheistic framework and covenant context distinguish it from its international parallels.</p>
        """,

        "Psalms": """
        <p>The Psalms were composed over many centuries, from Moses (Psalm 90) through the post-exilic period. Many psalms are attributed to David (c. 1000 BCE), reflecting his role in organizing Israel's worship and his personal spiritual journey.</p>

        <h3>Temple Worship</h3>
        <p>Many psalms were composed for temple worship, with musical notations and liturgical arrangements. The temple musicians and Levitical choirs used psalms in daily offerings, festival celebrations, and special occasions. Archaeological discoveries of musical instruments illuminate the performance context.</p>
        """,

        "Proverbs": """
        <p>Proverbs primarily originates from Solomon's reign (c. 970-930 BCE), though it includes collections from other periods. Solomon's international connections facilitated exchange with wisdom traditions from Egypt, Mesopotamia, and other cultures, while maintaining distinctive Israelite theological perspective.</p>

        <h3>Royal Wisdom</h3>
        <p>Ancient Near Eastern courts maintained wisdom traditions for training officials and governing effectively. Egyptian wisdom texts like the Instruction of Amenemhope show similarities to Proverbs 22:17-24:22, illustrating international wisdom exchange while highlighting Israel's unique covenant context.</p>
        """,

        "Ecclesiastes": """
        <p>Ecclesiastes reflects the wisdom tradition associated with Solomon, though its date and authorship remain debated. The book addresses questions of meaning and purpose that arose during periods of prosperity and philosophical reflection, possibly during the post-exilic period.</p>

        <h3>Philosophical Context</h3>
        <p>The book's existential questions parallel concerns found in ancient Near Eastern wisdom literature, particularly texts addressing life's apparent meaninglessness and the human search for purpose. However, Ecclesiastes maintains a distinctive theological framework emphasizing divine sovereignty and human limitation.</p>
        """,

        "Song of Solomon": """
        <p>Song of Solomon is traditionally attributed to Solomon (c. 970-930 BCE) and reflects ancient Near Eastern love poetry traditions. The pastoral and royal imagery suggests composition during Israel's monarchic period when such literary forms flourished.</p>

        <h3>Literary Context</h3>
        <p>Ancient Near Eastern love poetry from Egypt and Mesopotamia provides cultural background for understanding the Song's imagery and conventions. However, the Song's celebration of monogamous love contrasts with the polygamous practices common in ancient royal courts.</p>
        """,

        "Isaiah": """
        <p>Isaiah prophesied during the reigns of Uzziah, Jotham, Ahaz, and Hezekiah (c. 740-680 BCE), a period of Assyrian expansion and threat to Judah. The book addresses multiple historical contexts spanning from the eighth century through the post-exilic period.</p>

        <h3>Assyrian Crisis</h3>
        <p>Isaiah's ministry occurred during Assyria's westward expansion under Tiglath-Pileser III, Sargon II, and Sennacherib. The Assyrian siege of Jerusalem (701 BCE) forms a crucial backdrop for Isaiah's prophecies. Assyrian records confirm their campaigns against Judah and Jerusalem's remarkable survival.</p>

        <h3>International Context</h3>
        <p>Isaiah's prophecies against foreign nations reflect the complex international situation during the eighth-seventh centuries BCE. The rise and fall of Damascus, Samaria, Egypt, Babylon, and other powers provide historical framework for understanding Isaiah's oracles.</p>
        """,

        "Jeremiah": """
        <p>Jeremiah prophesied during Judah's final decades (c. 627-580 BCE), from Josiah's reign through the Babylonian exile. His ministry spanned the crucial transition from Assyrian to Babylonian dominance and witnessed Jerusalem's destruction.</p>

        <h3>Babylonian Period</h3>
        <p>Jeremiah's prophecies reflect the rising Babylonian threat under Nabopolassar and Nebuchadnezzar II. The Babylonian Chronicles provide contemporary documentation of campaigns against Judah, confirming biblical accounts of sieges, deportations, and Jerusalem's destruction.</p>

        <h3>Social Context</h3>
        <p>Jeremiah addressed a society facing political collapse, religious corruption, and social injustice. The reforms of Josiah had failed to produce lasting change, and subsequent kings pursued policies that accelerated national destruction. Jeremiah's personal suffering paralleled the nation's experience of judgment and exile.</p>
        """,

        "Lamentations": """
        <p>Lamentations was written shortly after Jerusalem's destruction (586 BCE), possibly by Jeremiah or a contemporary eyewitness. The book reflects the immediate aftermath of Babylonian conquest, with vivid descriptions of siege conditions, destruction, and exile.</p>

        <h3>Babylonian Siege</h3>
        <p>The siege of Jerusalem lasted approximately 18 months (588-586 BCE), creating conditions of extreme famine and desperation described in Lamentations. Archaeological evidence from Jerusalem shows destruction layers consistent with Babylonian assault, including arrowheads, burned structures, and evidence of rapid abandonment.</p>

        <h3>Ancient Lament Tradition</h3>
        <p>Lamentations follows ancient Near Eastern traditions of city laments found in Mesopotamian literature. Similar texts mourning destroyed cities provide cultural context for understanding the book's literary form while highlighting its unique theological perspective on divine judgment and hope.</p>
        """,

        "Ezekiel": """
        <p>Ezekiel prophesied among the Babylonian exiles (593-570 BCE) after being deported in 597 BCE with King Jehoiachin. His ministry occurred in Tel-abib near the Kebar Canal, addressing both exiles in Babylon and conditions in Jerusalem before its final destruction.</p>

        <h3>Exile Context</h3>
        <p>Babylonian policy involved deporting skilled workers and leaders while leaving agricultural workers in the land. The exile community in Babylon maintained some autonomy under appointed leaders but faced questions about identity, hope, and God's presence outside the Promised Land.</p>

        <h3>Mesopotamian Influence</h3>
        <p>Ezekiel's visionary language reflects familiarity with Mesopotamian art and mythology, particularly in throne visions and cosmic imagery. However, the prophet adapts these cultural forms to communicate distinctly Israelite theological content about divine sovereignty and restoration.</p>
        """,

        "Daniel": """
        <p>Daniel spans the Babylonian and early Persian periods (605-530 BCE), from Nebuchadnezzar's reign through Cyrus's conquest of Babylon. The book addresses Jewish faithfulness under foreign rule and divine sovereignty over international affairs.</p>

        <h3>Babylonian Court</h3>
        <p>The Babylonian court maintained international character with officials from various conquered territories. Training programs for foreign youth in Babylonian language and culture provided paths for advancement while testing loyalty to foreign gods and customs.</p>

        <h3>Persian Transition</h3>
        <p>Cyrus's conquest of Babylon (539 BCE) marked a significant policy shift toward religious tolerance and cultural restoration. The Persian administration utilized existing governmental structures while allowing conquered peoples to return to their homelands and rebuild their temples.</p>
        """,

        "Hosea": """
        <p>Hosea prophesied in the northern kingdom during its final decades (c. 755-710 BCE), particularly during the reigns of Jeroboam II and his successors. The prophet witnessed Israel's prosperity, political instability, and eventual destruction by Assyria.</p>

        <h3>Northern Kingdom Decline</h3>
        <p>After Jeroboam II's death (753 BCE), Israel experienced rapid political deterioration with six kings in twenty years, including four assassinations. This instability, combined with Assyrian pressure and religious syncretism, created the crisis Hosea addressed.</p>
        """,

        "Joel": """
        <p>Joel's date remains uncertain, with proposals ranging from the ninth to fourth centuries BCE. The locust plague and drought described may reflect actual natural disasters that prompted reflection on divine judgment and eschatological hope.</p>

        <h3>Agricultural Context</h3>
        <p>Joel's imagery draws heavily on Palestine's agricultural cycles and vulnerability to natural disasters. Locust swarms, drought, and crop failure represented existential threats to ancient agricultural communities, making them effective metaphors for divine judgment.</p>
        """,

        "Amos": """
        <p>Amos prophesied during the prosperous reigns of Jeroboam II in Israel and Uzziah in Judah (c. 760-750 BCE). Despite external prosperity, both kingdoms faced internal social injustice and religious corruption that Amos vigorously denounced.</p>

        <h3>Economic Prosperity</h3>
        <p>Archaeological evidence from sites like Samaria confirms the luxury and international trade that characterized this period. However, this prosperity was unevenly distributed, creating the social stratification and oppression that Amos condemned.</p>
        """,

        "Obadiah": """
        <p>Obadiah addresses Edom's betrayal of Judah, most likely during the Babylonian siege and destruction of Jerusalem (586 BCE). Edom's cooperation with Babylon and expansion into southern Judah created lasting animosity reflected in the prophecy.</p>

        <h3>Edomite Relations</h3>
        <p>Despite kinship ties through Esau and Jacob, Edom and Israel maintained complex and often hostile relationships. Edom's strategic location controlling trade routes between Arabia and the Mediterranean made it a significant regional power.</p>
        """,

        "Jonah": """
        <p>Jonah is set during the Assyrian period (c. 780-750 BCE) when Nineveh served as a major Assyrian center. The historical Jonah prophesied during Jeroboam II's reign, though the book's composition may be later.</p>

        <h3>Assyrian Context</h3>
        <p>Nineveh's repentance, while temporary, reflects documented instances of religious and moral reform in Assyrian history. The city's great size and importance described in Jonah align with archaeological evidence of Assyrian urban development.</p>
        """,

        "Micah": """
        <p>Micah prophesied during the reigns of Jotham, Ahaz, and Hezekiah (c. 735-700 BCE), contemporary with Isaiah but addressing rural concerns in Judah's Shephelah region. His ministry spanned the Assyrian crisis and siege of Jerusalem.</p>

        <h3>Rural Perspective</h3>
        <p>Micah's rural origin in Moresheth-gath provided perspective on how royal policies and international conflicts affected agricultural communities. His concern for social justice reflects the impact of urbanization and commercialization on traditional rural life.</p>
        """,

        "Nahum": """
        <p>Nahum prophesied shortly before Nineveh's fall to the Babylonian-Median coalition (612 BCE). The prophecy celebrates the end of Assyrian oppression that had dominated the Near East for over a century.</p>

        <h3>Assyrian Decline</h3>
        <p>Assyria's rapid collapse after Ashurbanipal's death (627 BCE) surprised the ancient world. Internal strife, Babylonian rebellion, and Median pressure combined to destroy what had seemed an invincible empire.</p>
        """,

        "Habakkuk": """
        <p>Habakkuk prophesied during the neo-Babylonian rise to power (c. 605-597 BCE), possibly during Jehoiakim's reign. The prophet witnessed Babylon's emergence as the dominant power that would execute judgment on Judah.</p>

        <h3>Babylonian Expansion</h3>
        <p>Nebuchadnezzar's campaigns westward brought Babylonian power to Palestine for the first time. The defeat of Egypt at Carchemish (605 BCE) established Babylonian control over the Levant and posed direct threat to Judah.</p>
        """,

        "Zephaniah": """
        <p>Zephaniah prophesied during Josiah's reign (640-609 BCE), possibly before or during the king's religious reforms. The prophecy addresses religious syncretism and social corruption that characterized Judah before Josiah's reformation efforts.</p>

        <h3>Reform Context</h3>
        <p>Josiah's reforms (622 BCE) addressed many issues Zephaniah raised, including removal of foreign religious practices, destruction of high places, and restoration of proper temple worship. Archaeological evidence confirms cult object destruction during this period.</p>
        """,

        "Haggai": """
        <p>Haggai prophesied during the early post-exilic period (520 BCE) under Persian rule, encouraging completion of the second temple. His ministry occurred during Darius I's reign when internal Persian conflicts delayed reconstruction projects.</p>

        <h3>Temple Rebuilding</h3>
        <p>Work on the second temple had stalled due to opposition from local inhabitants and economic difficulties. Haggai's prophecies provided divine mandate for resuming construction despite challenging circumstances.</p>
        """,

        "Zechariah": """
        <p>Zechariah was contemporary with Haggai (520-480 BCE), prophesying during temple reconstruction and early Persian period. His visions addressed questions about divine presence, future hope, and messianic expectations in the post-exilic community.</p>

        <h3>Post-Exilic Hopes</h3>
        <p>The small, struggling post-exilic community needed encouragement about God's future plans. Zechariah's messianic prophecies provided hope for ultimate restoration beyond the modest circumstances of Persian-period Judah.</p>
        """,

        "Malachi": """
        <p>Malachi prophesied during the mid-5th century BCE (c. 460-430 BCE), possibly contemporary with Ezra and Nehemiah's reforms. The prophecy addresses religious apathy and moral decline in the post-exilic community.</p>

        <h3>Religious Decline</h3>
        <p>Several generations after return from exile, religious enthusiasm had waned. Priests offered defective sacrifices, people withheld tithes, and intermarriage threatened covenant distinctiveness. Malachi's stern warnings addressed these compromises.</p>
        """,

        "Matthew": """
        <p>Matthew was written for Jewish Christians, likely in the 80s CE after Jerusalem's destruction. The gospel addresses questions about Jesus' relationship to Jewish law, prophecy, and institutions while explaining the church's mission to Gentiles.</p>

        <h3>Post-70 CE Context</h3>
        <p>Jerusalem's destruction forced redefinition of Judaism and Jewish Christianity. Matthew demonstrates Jesus' fulfillment of Old Testament prophecy while explaining why the church, not the temple, represents God's continuing presence among His people.</p>
        """,

        "Mark": """
        <p>Mark was written during or shortly after Nero's persecution (c. 65-70 CE), possibly in Rome for Gentile Christians facing martyrdom. The gospel emphasizes Jesus' suffering and calls disciples to similar faithful endurance.</p>

        <h3>Persecution Context</h3>
        <p>Nero's persecution (64-68 CE) represented the first systematic imperial attack on Christianity. Mark's emphasis on Jesus' suffering death and resurrection provided theological framework for understanding Christian martyrdom as participation in Christ's victory.</p>
        """,

        "Luke": """
        <p>Luke wrote for Gentile Christians (c. 80-85 CE), possibly in Greece or Asia Minor. The gospel demonstrates Christianity's universal scope while addressing questions about the church's relationship to Judaism and the Roman Empire.</p>

        <h3>Gentile Mission</h3>
        <p>By the 80s CE, Christianity had spread throughout the Roman Empire with largely Gentile membership. Luke's gospel validates this development by showing Jesus' concern for outcasts, foreigners, and social minorities from the beginning of His ministry.</p>
        """,

        "John": """
        <p>John was written in the 90s CE, likely in Ephesus, addressing challenges from both Jewish opposition and emerging Gnostic thought. The gospel presents Jesus' divine identity and incarnation against those who denied His true humanity or deity.</p>

        <h3>Late First-Century Challenges</h3>
        <p>By the 90s CE, Christianity faced sophisticated theological challenges. Jewish synagogues had excluded Christians, while Greek philosophical thought questioned the incarnation. John's high Christology addressed both challenges.</p>
        """,

        "Acts": """
        <p>Acts was written as Luke's second volume (c. 80-85 CE), tracing Christianity's expansion from Jerusalem to Rome. The book addresses questions about the church's identity, mission, and relationship to both Judaism and the Roman Empire.</p>

        <h3>Imperial Context</h3>
        <p>Acts presents Christianity as politically harmless to Rome while theologically distinct from Judaism. This apologetic purpose reflects the church's need to establish legal and social legitimacy within the Roman system.</p>
        """,

        "Romans": """
        <p>Romans was written from Corinth (c. 57 CE) as Paul prepared for his Jerusalem visit and planned mission to Spain. The letter addresses theological questions about salvation, law, and God's plan for Jews and Gentiles.</p>

        <h3>Jewish-Gentile Relations</h3>
        <p>The Roman church included both Jewish and Gentile Christians with potential tensions over law observance, food regulations, and calendar observances. Romans addresses these practical issues through theological exposition.</p>
        """,

        "1 Corinthians": """
        <p>1 Corinthians was written from Ephesus (c. 55 CE) to address specific problems in the Corinthian church. The letter responds to reports and questions about divisions, immorality, lawsuits, marriage, idol food, worship practices, and resurrection.</p>

        <h3>Corinthian Context</h3>
        <p>Corinth was a cosmopolitan Roman colony known for commerce, religious diversity, and moral permissiveness. The church faced challenges adapting Christian ethics to this culturally complex environment.</p>
        """,

        "2 Corinthians": """
        <p>2 Corinthians was written after a painful visit to Corinth (c. 55-56 CE), defending Paul's apostolic authority against opponents who questioned his credentials and methods. The letter reveals the emotional intensity of Paul's relationship with the church.</p>

        <h3>Apostolic Opposition</h3>
        <p>Paul faced challenges from "super-apostles" who promoted different gospel presentations and questioned his apostolic authority. This opposition reflected broader first-century disputes about Christian leadership and authentic gospel proclamation.</p>
        """,

        "Galatians": """
        <p>Galatians was written to churches in central Asia Minor, addressing the Judaizing controversy about Gentile requirements for circumcision and law observance. The letter's date depends on whether it addresses north or south Galatian churches.</p>

        <h3>Judaizing Controversy</h3>
        <p>The question of Gentile obligations to Jewish law represented a fundamental issue for early Christianity. Galatians provides Paul's theological defense of salvation by faith alone against those requiring law observance for full church membership.</p>
        """,

        "Ephesians": """
        <p>Ephesians was written during Paul's Roman imprisonment (c. 60-62 CE), possibly as a circular letter to Asian churches. The letter develops themes of church unity, spiritual warfare, and God's eternal plan for Jews and Gentiles.</p>

        <h3>Asian Ministry</h3>
        <p>Paul's three-year ministry in Ephesus had established churches throughout the Asian province. Ephesians reflects mature theological reflection on the nature and mission of the church in this diverse cultural environment.</p>
        """,

        "Philippians": """
        <p>Philippians was written from Roman imprisonment (c. 60-62 CE) to thank the church for financial support and address concerns about Paul's circumstances and false teaching. The letter reveals warm relationships between Paul and this supporting congregation.</p>

        <h3>Partnership in Ministry</h3>
        <p>Philippi was a Roman colony populated by military veterans with strong imperial loyalty. The church's financial support of Paul's mission demonstrated Christian commitment that transcended local political pressures.</p>
        """,

        "Colossians": """
        <p>Colossians was written during Paul's imprisonment (c. 60-62 CE) to address syncretistic philosophy threatening the church. The letter emphasizes Christ's supremacy over all spiritual powers and philosophical systems.</p>

        <h3>Syncretistic Threats</h3>
        <p>The Lycus Valley's religious environment included mystery religions, Jewish mysticism, and Greek philosophy. The "Colossian heresy" apparently combined elements from these traditions, requiring Paul's assertion of Christ's absolute supremacy.</p>
        """,

        "1 Thessalonians": """
        <p>1 Thessalonians was written from Corinth (c. 50-51 CE) shortly after Paul's ministry in Thessalonica. The letter addresses concerns about persecution, moral purity, and questions about Christ's return and the fate of deceased believers.</p>

        <h3>Thessalonian Ministry</h3>
        <p>Paul's brief ministry in Thessalonica (Acts 17) was cut short by Jewish opposition, leaving new converts with incomplete instruction. The letter provides encouragement and clarification for a young church facing persecution.</p>
        """,

        "2 Thessalonians": """
        <p>2 Thessalonians was written shortly after the first letter (c. 50-51 CE) to address continued concerns about Christ's return. Some believers had abandoned work expecting immediate parousia, while others questioned whether the day of the Lord had already occurred.</p>

        <h3>Eschatological Confusion</h3>
        <p>Misunderstanding about the timing of Christ's return created practical problems in the church. Paul provides correction about end-time events while emphasizing responsible living in the present age.</p>
        """,

        "1 Timothy": """
        <p>1 Timothy was written after Paul's release from Roman imprisonment (c. 62-64 CE) as he continued mission work. The letter addresses church organization, leadership qualifications, and response to false teaching in Ephesus.</p>

        <h3>Church Development</h3>
        <p>As churches matured, they needed formal leadership structures and procedures for maintaining orthodoxy. The pastoral epistles address these institutional developments in early Christianity.</p>
        """,

        "2 Timothy": """
        <p>2 Timothy was written during Paul's final imprisonment (c. 66-67 CE) as a farewell letter to his protégé. The letter emphasizes faithful ministry continuation despite persecution and personal abandonment.</p>

        <h3>Final Persecution</h3>
        <p>Paul's second Roman imprisonment occurred during intensified persecution under Nero. The letter reflects awareness of approaching martyrdom and concern for ministry continuation through faithful disciples.</p>
        """,

        "Titus": """
        <p>Titus was written during Paul's ministry in Crete (c. 62-64 CE) to provide guidance for church organization and pastoral challenges. The letter addresses the notorious moral problems of Cretan culture and their impact on church life.</p>

        <h3>Cretan Context</h3>
        <p>Crete's reputation for dishonesty and moral laxity required special attention to Christian character and conduct. Titus addresses these cultural challenges through emphasis on good works and sound doctrine.</p>
        """,

        "Philemon": """
        <p>Philemon was written during Paul's Roman imprisonment (c. 60-62 CE) to request forgiveness for Onesimus, a runaway slave who had become a Christian. The letter addresses slavery within Christian relationships.</p>

        <h3>Slavery Context</h3>
        <p>Roman slavery was widespread and legally protected, making Paul's request for Onesimus's reception revolutionary. The letter demonstrates Christian principles transforming social relationships without directly attacking institutional structures.</p>
        """,

        "Hebrews": """
        <p>Hebrews was written before Jerusalem's destruction (c. 60-70 CE) to Jewish Christians tempted to abandon Christianity for Judaism. The letter demonstrates Christ's superiority to all Old Testament institutions and personalities.</p>

        <h3>Jewish Christian Crisis</h3>
        <p>Jewish Christians faced persecution from both Jewish and Roman authorities, creating temptation to return to Judaism's legal protection. Hebrews argues that Christianity represents the fulfillment, not abandonment, of Jewish faith.</p>
        """,

        "James": """
        <p>James was written by Jesus' brother to Jewish Christians, possibly before 50 CE. The letter addresses practical Christian living with emphasis on faith demonstrated through works, concern for the poor, and control of speech.</p>

        <h3>Early Jewish Christianity</h3>
        <p>James reflects early Jewish Christian communities that maintained strong connections to Jewish ethical traditions while developing distinctively Christian practices and beliefs.</p>
        """,

        "1 Peter": """
        <p>1 Peter was written to Christians in Asia Minor during Nero's persecution (c. 62-64 CE). The letter encourages believers facing suffering while providing guidance for Christian conduct in a hostile environment.</p>

        <h3>Imperial Persecution</h3>
        <p>Nero's persecution marked the beginning of systematic imperial opposition to Christianity. 1 Peter provides theological framework for understanding Christian suffering as participation in Christ's redemptive work.</p>
        """,

        "2 Peter": """
        <p>2 Peter was written shortly before Peter's martyrdom (c. 65-68 CE) to warn against false teachers who denied Christ's return and promoted moral libertinism. The letter emphasizes the certainty of divine judgment.</p>

        <h3>False Teaching</h3>
        <p>Second-generation Christianity faced challenges from teachers who exploited Christian freedom for immoral purposes and questioned eschatological expectations. 2 Peter addresses these theological and ethical deviations.</p>
        """,

        "1 John": """
        <p>1 John was written in the 90s CE to address challenges from those who denied Christ's true humanity while claiming superior spiritual knowledge. The letter emphasizes love, truth, and assurance in response to these Gnostic-like ideas.</p>

        <h3>Proto-Gnostic Challenge</h3>
        <p>Early Gnostic thought questioned the incarnation and promoted salvation through special knowledge rather than faith and love. 1 John counters these ideas with emphasis on Christ's true humanity and the centrality of love.</p>
        """,

        "2 John": """
        <p>2 John was written to warn against extending hospitality to traveling teachers who denied Christ's true humanity. The brief letter addresses practical issues of discernment and church protection against false doctrine.</p>

        <h3>Traveling Teachers</h3>
        <p>Early Christianity depended on traveling missionaries and teachers, creating vulnerability to false doctrine spread through hospitality networks. 2 John provides guidance for maintaining doctrinal integrity while practicing Christian hospitality.</p>
        """,

        "3 John": """
        <p>3 John was written to address conflict between itinerant missionaries and local church leaders. The letter reveals tensions between apostolic authority and emerging local church autonomy in late first-century Christianity.</p>

        <h3>Church Authority</h3>
        <p>As apostolic leadership passed away, questions arose about authority structures in local churches. 3 John illustrates conflicts between traditional apostolic oversight and local leadership autonomy.</p>
        """,

        "Jude": """
        <p>Jude was written by Jesus' brother to address false teachers who exploited Christian freedom for immoral purposes. The letter warns against antinomian tendencies that threatened Christian community integrity.</p>

        <h3>Libertine Teaching</h3>
        <p>Some teachers distorted grace doctrine to justify immoral behavior, claiming spiritual freedom from moral constraints. Jude vigorously opposes this antinomian interpretation of Christian liberty.</p>
        """,

        "Revelation": """
        <p>Revelation was written during the reign of Emperor Domitian (81-96 CE), according to early church tradition as recorded by Irenaeus. The author, John, was exiled to the island of Patmos "because of the word of God and the testimony of Jesus" (1:9), indicating persecution for his Christian witness. The book addresses seven actual churches in the Roman province of Asia (western Turkey).</p>

        <h3>Roman Imperial Context</h3>
        <p>The late first century was marked by increasing imperial persecution of Christians. Domitian intensified emperor worship throughout the Roman Empire, demanding to be addressed as "Lord and God" (<em>dominus et deus noster</em>). He established an imperial cult with temples and statues dedicated to his worship. Christians who refused to participate in emperor worship faced economic sanctions, social ostracism, and sometimes execution.</p>

        <p>The province of Asia, where the seven churches were located, was particularly zealous in emperor worship. Ephesus, Smyrna, and Pergamum all had temples dedicated to the imperial cult. Pergamum is specifically mentioned as the place "where Satan's throne is" (2:13), likely referring to its prominence in emperor worship or its massive altar to Zeus.</p>

        <h3>Church Situation</h3>
        <p>The seven churches addressed in Revelation faced varying challenges. Some endured direct persecution (Smyrna, Philadelphia), while others struggled with false teaching (Ephesus, Pergamum, Thyatira), spiritual apathy (Sardis), or lukewarm commitment (Laodicea). Economic pressures pushed some believers toward compromise, as participation in trade guilds often required involvement in pagan rituals.</p>

        <p>Jewish communities in these cities sometimes opposed Christian groups, as mentioned regarding Smyrna and Philadelphia (2:9, 3:9). This created additional social pressure for Jewish Christians caught between their ethnic heritage and new faith.</p>

        <h3>Archaeological Evidence</h3>
        <p>Archaeological excavations have confirmed details about the seven cities addressed in Revelation. Laodicea's lukewarm water came from aqueducts carrying water from hot springs that cooled during transit. The city was indeed wealthy, with a banking industry and medical school known for eye salve. Philadelphia was subject to frequent earthquakes, as alluded to in the promise of a pillar that would never be shaken (3:12).</p>

        <p>Ephesus was home to the Temple of Artemis (Diana), one of the Seven Wonders of the ancient world. Excavations have uncovered a massive theater (Acts 19) and evidence of the city's prominence and wealth. Sardis' reputation as a city that appeared alive but was actually in decline is confirmed by archaeological evidence of its diminishing importance in the late first century.</p>
        """
    }

    # Generate a generic historical context if specific context isn't available
    if book not in historical_contexts:
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            # Determine approximate time period
            period = "pre-exilic"  # Default
            if book in ["Ezra", "Nehemiah", "Esther", "Haggai", "Zechariah", "Malachi"]:
                period = "post-exilic"
            elif book in ["Jeremiah", "Lamentations", "Ezekiel", "Daniel"]:
                period = "exilic"

            context = f"""
            <p>{book} was composed during the {period} period of Israel's history. The book reflects the historical circumstances, cultural influences, and theological concerns of its time.</p>

            <h3>Historical Setting</h3>
            <p>The book emerges from a context where Israel's covenant relationship with God shaped its national identity and religious practices. The surrounding nations, with their polytheistic worship and imperial ambitions, provided both cultural pressure and political threats that influenced Israel's historical experience.</p>

            <p>The religious life of Israel centered around the covenant, Law, and (depending on the period) the temple, with prophets calling the people back to covenant faithfulness and warning of judgment for persistent disobedience.</p>

            <h3>Cultural Background</h3>
            <p>The cultural world of {book} involved agricultural societies organized around tribal and kinship relationships, with increasing urbanization and social stratification over time. Religious practices permeated daily life, and interaction with surrounding cultures created ongoing tension between assimilation and distinctive identity.</p>

            <p>Archaeological discoveries have illuminated many aspects of daily life, religious practices, and historical events mentioned in {book}, providing background context for understanding its narratives and teachings.</p>
            """
        else:  # New Testament
            context = f"""
            <p>{book} was written during the first century CE, within the context of the early Christian church developing under Roman imperial rule. The book reflects the historical circumstances, cultural influences, and theological concerns of this formative period.</p>

            <h3>Roman Imperial Context</h3>
            <p>The Roman Empire provided the overarching political structure for the New Testament world, with its system of provinces, client kingdoms, and military presence. The Pax Romana (Roman Peace) enabled travel and communication throughout the Mediterranean world, facilitating the spread of Christianity while also presenting challenges through imperial ideology and occasional persecution.</p>

            <h3>Religious Environment</h3>
            <p>The religious landscape included Judaism with its various sects (Pharisees, Sadducees, Essenes), Greco-Roman polytheism, mystery religions, and philosophical schools. Early Christianity emerged within this complex environment, defining its identity in relation to Judaism while addressing Gentile converts from pagan backgrounds.</p>

            <p>Archaeological discoveries, historical documents, and cultural studies have illuminated many aspects of daily life, religious practices, and social structures in the first-century world, providing valuable context for understanding {book}.</p>
            """

        return context

    return historical_contexts.get(book, """
        <p>This book was written within the historical context of ancient religious traditions and cultural developments. The book reflects the circumstances, influences, and concerns of its time period while establishing principles with enduring significance.</p>

        <h3>Historical Setting</h3>
        <p>The book emerges from a context where covenant relationship with God shaped religious identity and practices. The surrounding nations and cultures provided both challenges and opportunities that influenced the historical experience of God's people.</p>

        <h3>Cultural Background</h3>
        <p>The cultural world involved societies organized around religious, social, and political structures that shaped daily life and community relationships. Archaeological discoveries have illuminated many aspects of this historical context.</p>
        """)
