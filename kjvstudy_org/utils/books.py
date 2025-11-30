"""Book name normalization and categorization utilities."""
import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

# Path to bible metadata JSON file
_METADATA_PATH = Path(__file__).parent.parent / "data" / "bible_metadata.json"


@lru_cache(maxsize=1)
def _load_bible_metadata() -> dict:
    """
    Load bible metadata from JSON file.
    Cached since this data never changes and is accessed frequently.
    """
    with open(_METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Load data from JSON
_metadata = _load_bible_metadata()
OT_BOOKS = _metadata["old_testament_books"]
NT_BOOKS = _metadata["new_testament_books"]
BOOK_ABBREVIATIONS = _metadata["book_abbreviations"]


@lru_cache(maxsize=1)
def _get_lowercase_abbreviations() -> dict:
    """Create a lowercase mapping of abbreviations for case-insensitive lookup."""
    return {k.lower(): v for k, v in BOOK_ABBREVIATIONS.items()}


@lru_cache(maxsize=1)
def _get_lowercase_canonical_names() -> dict:
    """Create a lowercase mapping of canonical book names."""
    all_books = OT_BOOKS + NT_BOOKS
    return {b.lower(): b for b in all_books}


def normalize_book_name(book: str) -> Optional[str]:
    """
    Normalize book name variations to canonical form.
    Returns the canonical book name if a variation is detected, None otherwise.
    Case-insensitive lookup.
    """
    # First try exact match in abbreviations
    if book in BOOK_ABBREVIATIONS:
        return BOOK_ABBREVIATIONS[book]
    # Then try case-insensitive match in abbreviations
    lowercase_abbrevs = _get_lowercase_abbreviations()
    result = lowercase_abbrevs.get(book.lower())
    if result:
        return result
    # Finally, check if it's a case variation of a canonical name
    lowercase_canonical = _get_lowercase_canonical_names()
    canonical = lowercase_canonical.get(book.lower())
    if canonical and canonical != book:
        return canonical
    return None


def is_old_testament(book: str) -> bool:
    """Check if a book is in the Old Testament."""
    return book in OT_BOOKS


def is_new_testament(book: str) -> bool:
    """Check if a book is in the New Testament."""
    return book in NT_BOOKS


def get_testament(book: str) -> str:
    """Return the testament name for a book."""
    if is_old_testament(book):
        return "Old Testament"
    elif is_new_testament(book):
        return "New Testament"
    return "Unknown"
