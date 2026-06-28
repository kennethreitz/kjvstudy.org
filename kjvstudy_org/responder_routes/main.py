"""Main pages — homepage, books browser, resources. (Responder port of routes/main.py)

This module is the REFERENCE for porting the other route modules: define
handlers, then register them on the passed ``api`` in ``register(api)``.
"""
from datetime import date

from ..kjv import bible
from ..resource_catalog import RESOURCE_CATEGORIES, iter_resources
from ..utils.books import OT_BOOKS, NT_BOOKS
from ..utils.helpers import get_daily_verse, verse_reference_to_url
from ..study_guides import get_featured_study_guides
from ._helpers import render

# Server-side cache for the homepage (rebuilds once per day).
_homepage_cache = {"date": None, "html": None}

# Book categorization (CSS slug per book) for the /books grid.
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


def register(api):
    @api.route("/")
    async def read_root(req, resp):
        """Homepage (cached, rebuilds once per day)."""
        today = date.today()
        if _homepage_cache["date"] == today and _homepage_cache["html"] is not None:
            resp.html = _homepage_cache["html"]
            return

        study_guides = get_featured_study_guides()
        for category in study_guides.values():
            for guide in category:
                guide["verse_refs"] = [
                    {"text": verse, "url": verse_reference_to_url(verse) or "#"}
                    for verse in guide["verses"]
                ]

        _exclude = {"/study-guides", "/family-tree", "/biblical-timeline", "/biblical-maps"}
        theology_links = [r for r in iter_resources() if r["url"] not in _exclude]

        html = api.template(
            "index.html",
            request=req,
            books=bible.get_books(),
            daily_verse=get_daily_verse(),
            study_guides=study_guides,
            theology_links=theology_links,
        )
        _homepage_cache["date"] = today
        _homepage_cache["html"] = html
        resp.html = html

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
