"""Main page routes - homepage, books browser, and resources."""
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..kjv import bible
from ..resource_catalog import RESOURCE_CATEGORIES, iter_resources
from ..utils.books import OT_BOOKS, NT_BOOKS
from ..utils.helpers import get_daily_verse, verse_reference_to_url
from .study_guides import get_featured_study_guides
from ._templates import templates

router = APIRouter()

# Server-side cache for homepage (rebuilds once per day)
_homepage_cache = {"date": None, "html": None}


# =============================================================================
# Routes
# =============================================================================

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    today = date.today()
    if _homepage_cache["date"] == today and _homepage_cache["html"] is not None:
        return HTMLResponse(content=_homepage_cache["html"], headers={"Cache-Control": "public, max-age=3600"})

    books = bible.get_books()
    daily_verse = get_daily_verse()

    # Curated homepage study-guide cards, content sourced from the catalog
    study_guides = get_featured_study_guides()

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

    # Doctrine/people resources for the homepage grid, from the shared catalog.
    # Excludes items already surfaced in the Study Resources / Interactive
    # Resources sections above (study guides, family tree, timeline, maps).
    _homepage_exclude = {"/study-guides", "/family-tree", "/biblical-timeline", "/biblical-maps"}
    theology_links = [r for r in iter_resources() if r["url"] not in _homepage_exclude]

    html = templates.get_template("index.html").render(
        {"request": request, "books": books, "daily_verse": daily_verse,
         "study_guides": study_guides, "theology_links": theology_links}
    )
    _homepage_cache["date"] = today
    _homepage_cache["html"] = html
    return HTMLResponse(content=html, headers={"Cache-Control": "public, max-age=3600"}
    )


@router.get("/books", response_class=HTMLResponse)
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
        for book in OT_BOOKS
    ]

    new_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in NT_BOOKS
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


@router.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    """Browse all theological resources"""
    books = bible.get_books()

    # Single source of truth: the shared resource catalog
    resources = RESOURCE_CATEGORIES

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
