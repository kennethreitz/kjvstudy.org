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


def get_christ_words(book: str, chapter: int, verse: int) -> str:
    """
    Get the actual words spoken by Christ in a verse.

    Args:
        book: Name of the book (e.g., "Matthew", "John")
        chapter: Chapter number
        verse: Verse number

    Returns:
        The words Christ spoke, or None if no words in this verse.
        Returns 'full' if Christ speaks the entire verse.
    """
    red_letter_verses = load_red_letter_verses()
    verse_key = f"{book} {chapter}:{verse}"
    return red_letter_verses.get(verse_key)


def wrap_red_letter_text(text: str, book: str, chapter: int, verse: int) -> str:
    """
    Wrap the words of Christ in red letter span tags.

    Args:
        text: The verse text
        book: Name of the book
        chapter: Chapter number
        verse: Verse number

    Returns:
        The text with Christ's words wrapped in red span tags.
    """
    christ_words = get_christ_words(book, chapter, verse)

    if not christ_words:
        return text

    # If the entire verse is Christ speaking
    if christ_words == 'full':
        return f'<span class="words-of-christ">{text}</span>'

    # Find and wrap only the words Christ spoke
    if christ_words in text:
        return text.replace(christ_words, f'<span class="words-of-christ">{christ_words}</span>')

    return text
