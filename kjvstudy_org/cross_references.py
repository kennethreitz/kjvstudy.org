"""
Cross-reference system for linking related Bible verses.
Organized by major theological themes and narrative connections.
"""

from functools import lru_cache
from pathlib import Path

from .kjv import bible, parse_reference_parts
from .utils.data_access import load_merged_json_dir


@lru_cache(maxsize=1)
def _load_cross_references():
    """Load cross-references from per-book JSON files (fallback to legacy file)."""
    base_dir = Path(__file__).parent / "data"
    return load_merged_json_dir(base_dir / "cross_references", base_dir / "cross_references.json")


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
    key = f"{book}:{chapter}:{verse}"
    refs = CROSS_REFERENCES.get(key, [])

    # Enhance each reference with the actual verse text
    enhanced_refs = []
    for ref in refs:
        enhanced_ref = ref.copy()

        # Parse the reference and look up the verse text for tooltips
        parsed = parse_reference_parts(ref['ref'])
        if parsed:
            ref_book, ref_chapter, ref_verse, _ = parsed
            try:
                verse_text = bible.get_verse_text(ref_book, ref_chapter, ref_verse)
                enhanced_ref['text'] = verse_text or ""
            except Exception:
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
        Dictionary with 'book', 'chapter', 'verse' keys, or None if unparseable.
    """
    parsed = parse_reference_parts(ref)
    if not parsed:
        return None

    book, chapter, verse, _ = parsed
    return {'book': book, 'chapter': chapter, 'verse': verse}
