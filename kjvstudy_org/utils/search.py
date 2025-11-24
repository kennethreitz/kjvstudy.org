"""Search functionality for Bible verses."""
from typing import List, Dict, Optional

from ..kjv import bible
from .helpers import is_verse_reference, parse_verse_reference


def perform_full_text_search(query: str, limit: Optional[int] = None) -> List[Dict]:
    """Perform full text search across all Bible verses or find specific verse references."""
    results = []

    # First, check if this looks like a verse reference
    if is_verse_reference(query):
        verse_result = parse_verse_reference(query)
        if verse_result:
            return [verse_result]

    # If not a verse reference or verse not found, perform regular text search
    search_terms = query.lower().split()

    # Search through all verses using the iter_verses method
    for verse in bible.iter_verses():
        verse_text = verse.text.lower()

        # Check if all search terms are in the verse
        if all(term in verse_text for term in search_terms):
            # Calculate relevance score
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

    # Limit results if specified
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
    """Highlight search terms in text."""
    highlighted = text
    for term in search_terms:
        # Simple highlighting (could be improved)
        highlighted = highlighted.replace(term, f"<mark>{term}</mark>")
    return highlighted
