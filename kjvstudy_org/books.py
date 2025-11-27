"""
Book introductions and metadata loader.
Loads individual JSON files for each book of the Bible.
"""

import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

# Path to books data directory
_books_dir = Path(__file__).parent / "data" / "books"

# Mapping of book names to their JSON filenames
_BOOK_FILENAME_MAP = {
    # Old Testament
    "Genesis": "genesis.json",
    "Exodus": "exodus.json",
    "Leviticus": "leviticus.json",
    "Numbers": "numbers.json",
    "Deuteronomy": "deuteronomy.json",
    "Joshua": "joshua.json",
    "Judges": "judges.json",
    "Ruth": "ruth.json",
    "I Samuel": "1_samuel.json",
    "II Samuel": "2_samuel.json",
    "I Kings": "1_kings.json",
    "II Kings": "2_kings.json",
    "I Chronicles": "1_chronicles.json",
    "II Chronicles": "2_chronicles.json",
    "Ezra": "ezra.json",
    "Nehemiah": "nehemiah.json",
    "Esther": "esther.json",
    "Job": "job.json",
    "Psalms": "psalms.json",
    "Proverbs": "proverbs.json",
    "Ecclesiastes": "ecclesiastes.json",
    "Solomon's Song": "solomons_song.json",
    "Isaiah": "isaiah.json",
    "Jeremiah": "jeremiah.json",
    "Lamentations": "lamentations.json",
    "Ezekiel": "ezekiel.json",
    "Daniel": "daniel.json",
    "Hosea": "hosea.json",
    "Joel": "joel.json",
    "Amos": "amos.json",
    "Obadiah": "obadiah.json",
    "Jonah": "jonah.json",
    "Micah": "micah.json",
    "Nahum": "nahum.json",
    "Habakkuk": "habakkuk.json",
    "Zephaniah": "zephaniah.json",
    "Haggai": "haggai.json",
    "Zechariah": "zechariah.json",
    "Malachi": "malachi.json",
    # New Testament
    "Matthew": "matthew.json",
    "Mark": "mark.json",
    "Luke": "luke.json",
    "John": "john.json",
    "Acts": "acts.json",
    "Romans": "romans.json",
    "I Corinthians": "1_corinthians.json",
    "II Corinthians": "2_corinthians.json",
    "Galatians": "galatians.json",
    "Ephesians": "ephesians.json",
    "Philippians": "philippians.json",
    "Colossians": "colossians.json",
    "I Thessalonians": "1_thessalonians.json",
    "II Thessalonians": "2_thessalonians.json",
    "I Timothy": "1_timothy.json",
    "II Timothy": "2_timothy.json",
    "Titus": "titus.json",
    "Philemon": "philemon.json",
    "Hebrews": "hebrews.json",
    "James": "james.json",
    "I Peter": "1_peter.json",
    "II Peter": "2_peter.json",
    "I John": "1_john.json",
    "II John": "2_john.json",
    "III John": "3_john.json",
    "Jude": "jude.json",
    "Revelation": "revelation.json",
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
