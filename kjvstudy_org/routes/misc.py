"""Miscellaneous routes - search, interlinear, random verse, verse of the day, red letter."""
import hashlib
import random
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..kjv import bible
from ..red_letter import load_red_letter_verses
from ..utils.search import perform_full_text_search

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


# =============================================================================
# Routes
# =============================================================================

@router.get("/search", response_class=HTMLResponse)
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


@router.get("/verse-of-the-day", response_class=HTMLResponse)
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
