"""Loader for poetry formatting data (stanza breaks, poetry books)."""

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POETRY_FILE = DATA_DIR / "poetry_formatting.json"


@lru_cache(maxsize=1)
def _load_poetry_data() -> dict:
    """Load poetry formatting data from JSON file."""
    if not POETRY_FILE.exists():
        return {"books": {}}
    with open(POETRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_poetry_book(book: str) -> bool:
    """Check if a book is entirely poetry (all chapters are poetry)."""
    data = _load_poetry_data()
    book_data = data.get("books", {}).get(book, {})
    return book_data.get("is_poetry", False)


def is_poetry_chapter(book: str, chapter: int) -> bool:
    """Check if a specific chapter should be rendered as poetry.

    Some books (like Job) have both prose and poetry chapters.
    """
    data = _load_poetry_data()
    book_data = data.get("books", {}).get(book, {})
    poetry_chapters = book_data.get("poetry_chapters", [])
    # Handle "all" for books that are entirely poetry
    if poetry_chapters == "all":
        return True
    return chapter in poetry_chapters


def get_stanza_breaks(book: str, chapter: int) -> set:
    """Get verse numbers that have stanza breaks before them.

    Returns a set of verse numbers where a stanza break should appear
    before the verse (extra vertical spacing).
    """
    data = _load_poetry_data()
    book_data = data.get("books", {}).get(book, {})
    breaks = book_data.get("stanza_breaks", {}).get(str(chapter), [])
    return set(breaks)


def get_poetry_books() -> list:
    """Get list of books that have any poetry chapters."""
    data = _load_poetry_data()
    return list(data.get("books", {}).keys())
