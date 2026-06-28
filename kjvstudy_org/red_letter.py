"""
Red Letter Edition - Words of Christ

This module handles loading and checking verses that contain
the words of Jesus Christ (traditionally printed in red in Bibles).
"""

import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

from .kjv import bible, parse_reference_parts
from .utils.books import normalize_book_name


@lru_cache(maxsize=1)
def load_red_letter_verses():
    """Load the red letter verses data from JSON file."""
    data_path = Path(__file__).parent / "data" / "red_letter_verses.json"

    if not data_path.exists():
        return {}

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get("verses", {})


def iter_red_letter_verses(book_filter: Optional[str] = None):
    """Yield parsed red-letter verses, optionally filtered by book.

    Each item is a dict: reference, book, chapter, verse, text, christ_words,
    is_full_verse. Entries that don't parse or have no verse text are skipped.
    The book filter accepts canonical names and abbreviations (e.g. "Mt" ->
    "Matthew"), so the web and API surfaces filter identically.
    """
    canonical_filter = None
    if book_filter:
        canonical_filter = normalize_book_name(book_filter) or book_filter

    for verse_ref, christ_words in load_red_letter_verses().items():
        parsed = parse_reference_parts(verse_ref)
        if not parsed:
            continue
        book_name, chapter_num, verse_num, _ = parsed

        if canonical_filter and book_name != canonical_filter:
            continue

        verse_text = bible.get_verse_text(book_name, chapter_num, verse_num)
        if not verse_text:
            continue

        yield {
            "reference": verse_ref,
            "book": book_name,
            "chapter": chapter_num,
            "verse": verse_num,
            "text": verse_text,
            "christ_words": christ_words,
            "is_full_verse": christ_words == "full",
        }


def red_letter_stats() -> dict:
    """Aggregate red-letter statistics.

    ``total``/``full``/``partial`` are over the raw verse map; ``by_book`` counts
    every parseable reference (ignoring any filter), ordered by count descending.
    """
    red_letter_data = load_red_letter_verses()
    total = len(red_letter_data)
    full = sum(1 for v in red_letter_data.values() if v == "full")

    by_book = {}
    for verse_ref in red_letter_data:
        parsed = parse_reference_parts(verse_ref)
        if not parsed:
            continue
        by_book[parsed[0]] = by_book.get(parsed[0], 0) + 1

    by_book = dict(sorted(by_book.items(), key=lambda x: x[1], reverse=True))
    return {"total": total, "full": full, "partial": total - full, "by_book": by_book}


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
