"""
Book introductions and metadata loader.
Loads individual JSON files for each book of the Bible.
"""

import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

from .utils.books import OT_BOOKS, NT_BOOKS

# Path to books data directory
_books_dir = Path(__file__).parent / "data" / "books"

# Book name -> JSON filename, derived from the canonical book list so it stays
# in sync (and uses the same Arabic-numeral names as the rest of the app).
_BOOK_FILENAME_MAP = {
    book: book.lower().replace(" ", "_") + ".json"
    for book in OT_BOOKS + NT_BOOKS
}


@lru_cache(maxsize=66)
def get_book_data(book_name: str) -> Optional[dict]:
    """
    Get the full data for a specific book.

    Args:
        book_name: The canonical name of the book (e.g., "Genesis", "I Corinthians")

    Returns:
        Dictionary with book data or None if not found
    """
    filename = _BOOK_FILENAME_MAP.get(book_name)
    if not filename:
        return None

    filepath = _books_dir / filename
    if not filepath.exists():
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_book_introduction(book_name: str) -> Optional[str]:
    """Get just the introduction text for a book."""
    data = get_book_data(book_name)
    return data.get("introduction") if data else None


def get_book_themes(book_name: str) -> Optional[list]:
    """Get the key themes for a book."""
    data = get_book_data(book_name)
    return data.get("key_themes") if data else None


def get_book_key_verses(book_name: str) -> Optional[list]:
    """Get the key verses for a book."""
    data = get_book_data(book_name)
    return data.get("key_verses") if data else None


def get_book_outline(book_name: str) -> Optional[list]:
    """Get the outline for a book."""
    data = get_book_data(book_name)
    return data.get("outline") if data else None


def get_book_christ_in_book(book_name: str) -> Optional[str]:
    """Get the Christ in this book section."""
    data = get_book_data(book_name)
    return data.get("christ_in_book") if data else None


def get_book_metadata(book_name: str) -> Optional[dict]:
    """
    Get metadata for a book (author, date, category, etc.)
    without the full content.
    """
    data = get_book_data(book_name)
    if not data:
        return None

    return {
        "name": data.get("name"),
        "abbreviation": data.get("abbreviation"),
        "testament": data.get("testament"),
        "position": data.get("position"),
        "chapters": data.get("chapters"),
        "category": data.get("category"),
        "author": data.get("author"),
        "date_written": data.get("date_written"),
    }


@lru_cache(maxsize=1)
def get_all_books_metadata() -> list:
    """
    Get metadata for all books in canonical order.
    Cached since this is called frequently and data never changes.
    """
    books = []
    for book_name in _BOOK_FILENAME_MAP.keys():
        metadata = get_book_metadata(book_name)
        if metadata:
            books.append(metadata)

    # Sort by position
    books.sort(key=lambda x: x.get("position", 999))
    return books


def has_book_data(book_name: str) -> bool:
    """Check if we have introduction data for a book."""
    return book_name in _BOOK_FILENAME_MAP


@lru_cache(maxsize=1)
def get_books_by_category() -> dict:
    """
    Get all books organized by category.
    Cached since this is expensive (loads all 66 books) and data never changes.
    """
    categories = {}
    for book_name in _BOOK_FILENAME_MAP.keys():
        data = get_book_data(book_name)
        if data:
            category = data.get("category", "Unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append({
                "name": data.get("name"),
                "abbreviation": data.get("abbreviation"),
                "chapters": data.get("chapters"),
                "position": data.get("position"),
            })

    # Sort books within each category by position
    for category in categories:
        categories[category].sort(key=lambda x: x.get("position", 999))

    return categories
