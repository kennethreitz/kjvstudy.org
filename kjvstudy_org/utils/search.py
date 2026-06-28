"""Search functionality for Bible verses."""
from typing import List, Dict, Optional

from ..kjv import bible
from .helpers import is_verse_reference, parse_verse_reference, highlight_terms

# Try to use FTS5 search if available
_use_fts = False
try:
    from .search_index import search_verses as fts_search, init_search_index, DB_PATH
    _use_fts = True
except ImportError:
    pass


def perform_full_text_search(query: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Perform full text search across all Bible verses.

    Uses SQLite FTS5 for efficient searching when available,
    falls back to O(n) iteration otherwise.
    """
    # First, check if this looks like a verse reference
    if is_verse_reference(query):
        verse_result = parse_verse_reference(query)
        if verse_result:
            return [verse_result]

    # Use FTS5 if available and index exists
    if _use_fts and DB_PATH.exists():
        return fts_search(query, limit)

    # Fallback to original O(n) search
    return _legacy_search(query, limit)


def _legacy_search(query: str, limit: Optional[int] = None) -> List[Dict]:
    """Original O(n) search through all verses - used as fallback."""
    results = []
    search_terms = query.lower().split()

    for verse in bible.iter_verses():
        verse_text = verse.text.lower()

        # Check if all search terms are in the verse
        if all(term in verse_text for term in search_terms):
            score = calculate_relevance_score(verse.text, search_terms)

            results.append({
                "book": verse.book,
                "chapter": verse.chapter,
                "verse": verse.verse,
                "text": verse.text,
                "reference": f"{verse.book} {verse.chapter}:{verse.verse}",
                "url": f"/book/{verse.book}/chapter/{verse.chapter}#verse-{verse.verse}",
                "score": score,
                "highlighted_text": highlight_search_terms(verse.text, search_terms)
            })

    # Sort by relevance score (higher is better)
    results.sort(key=lambda x: x["score"], reverse=True)

    if limit is not None:
        return results[:limit]
    return results


def calculate_relevance_score(text: str, search_terms: List[str]) -> float:
    """Calculate relevance score for search results."""
    text_lower = text.lower()
    score = 0.0

    for term in search_terms:
        # Count occurrences of each term
        count = text_lower.count(term.lower())
        score += count

        # Bonus for exact word matches
        if f" {term.lower()} " in f" {text_lower} ":
            score += 0.5

    return score


def highlight_search_terms(text: str, search_terms: List[str]) -> str:
    """Highlight a list of search terms in text."""
    return highlight_terms(text, search_terms)


def ensure_search_index():
    """Ensure the FTS5 search index is built."""
    if _use_fts:
        init_search_index()
        return True
    return False
