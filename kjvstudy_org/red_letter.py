"""
Red Letter Edition - Words of Christ

This module handles loading and checking verses that contain
the words of Jesus Christ (traditionally printed in red in Bibles).
"""

import json
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def load_red_letter_verses():
    """Load the red letter verses data from JSON file."""
    data_path = Path(__file__).parent / "data" / "red_letter_verses.json"

    if not data_path.exists():
        return {}

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get("verses", {})


def is_red_letter_verse(book: str, chapter: int, verse: int) -> bool:
    """
    Check if a verse contains words of Christ.

    Args:
        book: Name of the book (e.g., "Matthew", "John")
        chapter: Chapter number
        verse: Verse number

    Returns:
        True if this verse contains Christ's words
    """
    red_letter_verses = load_red_letter_verses()
    verse_key = f"{book} {chapter}:{verse}"
    return red_letter_verses.get(verse_key, False)


def wrap_red_letter_text(text: str, book: str, chapter: int, verse: int) -> str:
    """
    Wrap verse text in red letter span if it contains Christ's words.

    Args:
        text: The verse text
        book: Name of the book
        chapter: Chapter number
        verse: Verse number

    Returns:
        The text wrapped in a span tag if it's a red letter verse,
        otherwise returns the original text.
    """
    if is_red_letter_verse(book, chapter, verse):
        return f'<span class="words-of-christ">{text}</span>'
    return text
