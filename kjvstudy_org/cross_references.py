"""
Cross-reference system for linking related Bible verses.
Organized by major theological themes and narrative connections.
"""

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _load_cross_references():
    """Load cross-references from per-book JSON files (fallback to legacy file)."""
    base_dir = Path(__file__).parent / "data"
    crossref_dir = base_dir / "cross_references"
    legacy_path = base_dir / "cross_references.json"

    aggregated = {}
    if crossref_dir.exists():
        for path in sorted(crossref_dir.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    aggregated.update(content)
    elif legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            aggregated = json.load(f)

    return aggregated


CROSS_REFERENCES = _load_cross_references()


def get_cross_references(book: str, chapter: int, verse: int) -> list:
    """
    Get cross-references for a specific verse with verse text for tooltips.

    Args:
        book: Book name (e.g., "Genesis", "John")
        chapter: Chapter number
        verse: Verse number

    Returns:
        List of cross-reference dictionaries with 'ref', 'note', and 'text' keys
    """
    from .kjv import bible

    key = f"{book}:{chapter}:{verse}"
    refs = CROSS_REFERENCES.get(key, [])

    # Enhance each reference with the actual verse text
    enhanced_refs = []
    for ref in refs:
        enhanced_ref = ref.copy()

        # Parse the reference to get the verse text
        ref_str = ref['ref']
        parts = ref_str.rsplit(' ', 1)
        if len(parts) == 2:
            ref_book = parts[0]
            chapter_verse = parts[1]

            if ':' in chapter_verse:
                ref_chapter, ref_verse = chapter_verse.split(':')
                ref_chapter = int(ref_chapter)
                ref_verse = int(ref_verse)

                # Get the verse text using the bible object
                try:
                    verse_text = bible.get_verse_text(ref_book, ref_chapter, ref_verse)
                    enhanced_ref['text'] = verse_text if verse_text else ""
                except Exception:
                    enhanced_ref['text'] = ""
            else:
                enhanced_ref['text'] = ""
        else:
            enhanced_ref['text'] = ""

        enhanced_refs.append(enhanced_ref)

    return enhanced_refs


def parse_reference(ref: str) -> dict:
    """
    Parse a reference string like "Genesis 1:1" into components.

    Args:
        ref: Reference string

    Returns:
        Dictionary with 'book', 'chapter', 'verse' keys
    """
    parts = ref.rsplit(' ', 1)
    if len(parts) != 2:
        return None

    book = parts[0]
    chapter_verse = parts[1].split(':')
    if len(chapter_verse) != 2:
        return None

    try:
        return {
            'book': book,
            'chapter': int(chapter_verse[0]),
            'verse': int(chapter_verse[1])
        }
    except ValueError:
        return None
