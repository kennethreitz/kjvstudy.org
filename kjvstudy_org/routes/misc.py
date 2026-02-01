"""Miscellaneous routes - search, interlinear, random verse, verse of the day, red letter, OG images."""
import hashlib
import random
import re
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query, Request, Path
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from ..kjv import bible
from ..red_letter import load_red_letter_verses
from ..utils.search import perform_full_text_search
from ..og_image import get_cached_or_generate

router = APIRouter()
templates = None

# Will be set by init_search_family_tree()
_search_family_tree_fn = None


def init_templates(t: Jinja2Templates):
    """Initialize templates for misc routes."""
    global templates
    templates = t


def init_search_family_tree(fn):
    """Initialize the search_family_tree function from server.py."""
    global _search_family_tree_fn
    _search_family_tree_fn = fn


# =============================================================================
# Helper Functions
# =============================================================================

def _load_featured_verses():
    """Load featured verses from JSON file."""
    import json
    from pathlib import Path
    data_file = Path(__file__).parent.parent / "data" / "featured_verses.json"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f).get("verses", [])
    return []


def get_daily_verse(date_str=None):
    """Get the verse of the day based on a specific date (or current date if not provided).

    Uses calendar-based selection: verses are organized by month theme, so
    January dates get January-themed verses, December dates get Advent verses, etc.
    """
    if date_str is None:
        date_obj = datetime.now()
        date_str = date_obj.strftime("%Y-%m-%d")
    else:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Load featured verses from JSON file
    featured_verses = _load_featured_verses()

    if not featured_verses:
        # Fallback if file not found
        featured_verses = [{"book": "John", "chapter": 3, "verse": 16}]

    # Use day of year for calendar-based selection (1-365/366)
    # This ensures January verses appear in January, December verses in December, etc.
    day_of_year = date_obj.timetuple().tm_yday  # 1-366
    verse_index = (day_of_year - 1) % len(featured_verses)  # 0-364
    verse_data = featured_verses[verse_index]
    book = verse_data["book"]
    chapter = verse_data["chapter"]
    verse = verse_data["verse"]
    devotional = verse_data.get("devotional")

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        # Fallback to John 3:16
        book, chapter, verse = "John", 3, 16
        verse_text = bible.get_verse_text(book, chapter, verse)
        devotional = None

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": verse_text,
        "reference": f"{book} {chapter}:{verse}",
        "date": date_str,
        "devotional": devotional
    }


# =============================================================================
# Routes
# =============================================================================

def parse_strongs_number(query: str) -> str | None:
    """Parse a Strong's number query and return the redirect URL, or None."""
    if not query:
        return None
    query = query.strip()
    # Match H1, H1234, G1, G5678, etc. (case insensitive)
    match = re.match(r'^([HhGg])(\d+)$', query)
    if match:
        prefix = match.group(1).upper()
        number = match.group(2)
        return f'/strongs/{prefix}{number}'
    return None


@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = Query(None, description="Search query")):
    """Search page with results (includes Bible verses and family tree)"""
    # Check if query is a Strong's number - redirect if so
    if q:
        strongs_url = parse_strongs_number(q)
        if strongs_url:
            return RedirectResponse(url=strongs_url, status_code=302)

    books = bible.get_books()
    search_results = []
    family_tree_results = []
    is_direct_verse = False

    if q and len(q.strip()) >= 2:
        # Search Bible verses (cap at 50 to keep template rendering fast)
        search_results = perform_full_text_search(q.strip(), limit=50)
        # Check if this was a direct verse reference match
        if search_results and len(search_results) == 1 and search_results[0].get("score") == 100.0:
            is_direct_verse = True

        # Also search family tree (limit to 5 results)
        if _search_family_tree_fn:
            family_tree_results = _search_family_tree_fn(q.strip(), limit=5)

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Search", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "search.html",
            {
            "query": q or "",
            "results": search_results,
            "family_tree_results": family_tree_results,
            "books": books,
            "total_results": len(search_results) + len(family_tree_results),
            "is_direct_verse": is_direct_verse,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/interlinear", response_class=HTMLResponse)
async def interlinear_landing_page(request: Request):
    """Landing page explaining interlinear Bible study"""
    books = bible.get_books()

    # Featured verses with interlinear data
    featured_verses = [
        {"reference": "John 3:16", "url": "/book/John/chapter/3/verse/16#interlinear", "note": "God's love for the world"},
        {"reference": "Genesis 1:1", "url": "/book/Genesis/chapter/1/verse/1#interlinear", "note": "In the beginning"},
        {"reference": "Psalm 23:1", "url": "/book/Psalms/chapter/23/verse/1#interlinear", "note": "The Lord is my shepherd"},
        {"reference": "Romans 8:28", "url": "/book/Romans/chapter/8/verse/28#interlinear", "note": "All things work together for good"},
        {"reference": "Matthew 28:19", "url": "/book/Matthew/chapter/28/verse/19#interlinear", "note": "The Great Commission"},
        {"reference": "1 Corinthians 13:4", "url": "/book/1 Corinthians/chapter/13/verse/4#interlinear", "note": "Love is patient"},
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


@router.get("/random-verse")
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


@router.get("/verse-of-the-day")
async def verse_of_the_day_redirect():
    """Redirect to today's verse of the day (prevents caching, allows bookmarking)."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    return RedirectResponse(url=f"/verse-of-the-day/{today_str}", status_code=302)


@router.get("/verse-of-the-day/{date}", response_class=HTMLResponse)
async def verse_of_the_day_page(request: Request, date: str):
    """Verse of the day page for a specific date."""
    books = bible.get_books()

    # Parse the date
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # Invalid date format, redirect to today
        return RedirectResponse(url="/verse-of-the-day", status_code=302)

    date_str = current_date.strftime("%Y-%m-%d")
    daily_verse = get_daily_verse(date_str)

    # Calculate prev/next dates for navigation
    prev_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Generate past 30 days of verses (from the viewed date)
    past_verses = []
    for i in range(1, 31):  # Past 30 days (not including current)
        past_date = current_date - timedelta(days=i)
        past_date_str = past_date.strftime("%Y-%m-%d")
        verse = get_daily_verse(past_date_str)
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
            "breadcrumbs": breadcrumbs,
            "prev_date": prev_date,
            "next_date": next_date,
            "is_today": date_str == today_str
        }
    )


@router.get("/stars", response_class=HTMLResponse)
async def stars_page(request: Request):
    """Stars page - displays user's saved starred pages from localStorage"""
    books = bible.get_books()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Stars", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "stars.html",
        {
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/red-letter", response_class=HTMLResponse)
async def red_letter_page(
    request: Request,
    book: Optional[str] = Query(None, description="Filter by book"),
    page: int = Query(1, ge=1, description="Page number")
):
    """Red Letter Edition - Words of Christ page"""
    books = bible.get_books()
    red_letter_data = load_red_letter_verses()

    # Build list of all red letter verses
    all_verses = []
    by_book = {}

    for verse_ref, christ_words in red_letter_data.items():
        # Parse the reference (format: "Book Chapter:Verse")
        parts = verse_ref.rsplit(' ', 1)
        if len(parts) != 2:
            continue

        book_name = parts[0]
        chapter_verse = parts[1].split(':')
        if len(chapter_verse) != 2:
            continue

        try:
            chapter_num = int(chapter_verse[0])
            verse_num = int(chapter_verse[1])
        except ValueError:
            continue

        # Count by book
        by_book[book_name] = by_book.get(book_name, 0) + 1

        # Apply book filter if specified
        if book and book_name != book:
            continue

        # Get the verse text
        verse_text = bible.get_verse_text(book_name, chapter_num, verse_num)
        if not verse_text:
            continue

        all_verses.append({
            "reference": verse_ref,
            "book": book_name,
            "chapter": chapter_num,
            "verse": verse_num,
            "text": verse_text,
            "christ_words": christ_words,
            "is_full_verse": christ_words == "full"
        })

    # Sort by book order, then chapter, then verse
    book_order = {b: i for i, b in enumerate(books)}
    all_verses.sort(key=lambda v: (book_order.get(v["book"], 999), v["chapter"], v["verse"]))

    # Pagination
    per_page = 50
    total = len(all_verses)
    total_pages = (total + per_page - 1) // per_page
    page = min(page, total_pages) if total_pages > 0 else 1
    offset = (page - 1) * per_page
    verses = all_verses[offset:offset + per_page]

    # Stats
    total_all = len(red_letter_data)
    full_verses = sum(1 for v in red_letter_data.values() if v == "full")
    partial_verses = total_all - full_verses

    # Sort books by count for sidebar
    books_with_counts = sorted(by_book.items(), key=lambda x: x[1], reverse=True)

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Red Letter", "url": "/red-letter"}
    ]
    if book:
        breadcrumbs.append({"text": book, "url": None})

    return templates.TemplateResponse(
        request,
        "red_letter.html",
        {
            "books": books,
            "verses": verses,
            "total": total,
            "total_all": total_all,
            "full_verses": full_verses,
            "partial_verses": partial_verses,
            "books_with_counts": books_with_counts,
            "selected_book": book,
            "page": page,
            "total_pages": total_pages,
            "per_page": per_page,
            "breadcrumbs": breadcrumbs
        }
    )


# =============================================================================
# Dynamic OG Image Generation
# =============================================================================

@router.get("/og/verse/{book}/{chapter}/{verse}.png", response_class=Response)
async def og_image_verse(
    book: str = Path(..., description="Book name"),
    chapter: int = Path(..., description="Chapter number"),
    verse: int = Path(..., description="Verse number")
):
    """Generate OG image for a specific verse."""
    import asyncio

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        # Return default image if verse not found
        from pathlib import Path as PathLib
        default_path = PathLib(__file__).parent.parent / "static" / "og-image.png"
        content = await asyncio.to_thread(default_path.read_bytes)
        return Response(content=content, media_type="image/png")

    title = f"{book} {chapter}:{verse}"
    cache_key = f"verse:{book}:{chapter}:{verse}"

    # Run CPU-bound image generation in thread pool to avoid blocking
    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="King James Version",
        verse_text=verse_text,
        page_type="verse"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )


@router.get("/og/chapter/{book}/{chapter}.png", response_class=Response)
async def og_image_chapter(
    book: str = Path(..., description="Book name"),
    chapter: int = Path(..., description="Chapter number")
):
    """Generate OG image for a chapter."""
    import asyncio

    # Get first verse as preview
    verse_text = bible.get_verse_text(book, chapter, 1)

    title = f"{book} {chapter}"
    cache_key = f"chapter:{book}:{chapter}"

    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="King James Version",
        verse_text=verse_text[:150] + "..." if verse_text and len(verse_text) > 150 else verse_text,
        page_type="chapter"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )


@router.get("/og/book/{book}.png", response_class=Response)
async def og_image_book(book: str = Path(..., description="Book name")):
    """Generate OG image for a book."""
    import asyncio

    title = book
    cache_key = f"book:{book}"

    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="King James Version Bible",
        page_type="book"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )


@router.get("/og/topic/{topic}.png", response_class=Response)
async def og_image_topic(topic: str = Path(..., description="Topic name")):
    """Generate OG image for a topic."""
    import asyncio
    from urllib.parse import unquote

    topic_name = unquote(topic)

    title = topic_name
    cache_key = f"topic:{topic_name}"

    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="Topical Bible Study",
        page_type="topic"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )


@router.get("/og/story/{slug}.png", response_class=Response)
async def og_image_story(slug: str = Path(..., description="Story slug")):
    """Generate OG image for a Bible story."""
    import asyncio
    import json
    from pathlib import Path as PathLib

    # Load story data to get title
    stories_file = PathLib(__file__).parent.parent / "data" / "stories.json"
    title = slug.replace("-", " ").title()  # Fallback

    if stories_file.exists():
        with open(stories_file, "r", encoding="utf-8") as f:
            stories_data = json.load(f)
            for story in stories_data.get("stories", []):
                if story.get("slug") == slug:
                    title = story.get("title", title)
                    break

    cache_key = f"story:{slug}"

    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="Bible Stories",
        page_type="story"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )


@router.get("/og/guide/{slug}.png", response_class=Response)
async def og_image_guide(slug: str = Path(..., description="Study guide slug")):
    """Generate OG image for a study guide."""
    import asyncio

    title = slug.replace("-", " ").title()  # Fallback title
    cache_key = f"guide:{slug}"

    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle="Bible Study Guide",
        page_type="guide"
    )

    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )
