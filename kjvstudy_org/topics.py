"""
Topical index for finding Bible verses by theme.
Organized by major theological and practical topics.
"""

from functools import lru_cache
from pathlib import Path

from typing import Dict, Any

from .kjv import bible, parse_reference_parts
from .utils.data_access import load_merged_json_dir

@lru_cache(maxsize=1)
def _load_topics():
    """Load topics from per-topic JSON files, fallback to legacy single file."""
    base_dir = Path(__file__).parent / "data"
    return load_merged_json_dir(base_dir / "topics", base_dir / "topics.json")


def _get_verse_text_for_reference(reference: str) -> str:
    """Look up a single verse text from a reference like 'John 3:16'.

    Uses the first verse of a range (e.g. 3:16-17 -> 3:16).
    """
    parsed = parse_reference_parts(reference)
    if not parsed:
        return ""

    book, chapter, verse, _ = parsed
    try:
        return bible.get_verse_text(book, chapter, verse) or ""
    except Exception:
        return ""


def _enrich_topic_with_text(topic: Dict[str, Any]) -> Dict[str, Any]:
    """Attach verse text (and normalized reference fields) to a topic's verses."""
    subtopics = topic.get("subtopics", {})
    enriched_subtopics = {}

    for subtopic_name, subtopic_data in subtopics.items():
        verses_with_text = []
        for entry in subtopic_data.get("verses", []):
            if isinstance(entry, dict):
                reference = entry.get("reference") or entry.get("ref") or ""
                note = entry.get("note", "")
            else:
                reference = str(entry)
                note = ""

            verse_text = _get_verse_text_for_reference(reference)
            verses_with_text.append({
                "reference": reference,
                "ref": reference,
                "text": verse_text,
                "note": note
            })

        enriched_subtopics[subtopic_name] = {
            **subtopic_data,
            "verses": verses_with_text
        }

    return {
        **topic,
        "subtopics": enriched_subtopics
    }


def get_all_topics():
    """Get all topics"""
    return _load_topics()


def get_topic(topic_name: str):
    """Get a specific topic"""
    return _load_topics().get(topic_name)


@lru_cache(maxsize=None)
def get_topic_with_text(topic_name: str):
    """Get a topic with verse text attached to each reference."""
    topic = _load_topics().get(topic_name)
    if not topic:
        return None
    return _enrich_topic_with_text(topic)


def search_topics(query: str):
    """Search for topics by name or description"""
    query_lower = query.lower()
    results = []

    for topic_name, topic_data in _load_topics().items():
        if query_lower in topic_name.lower() or query_lower in topic_data.get("description", "").lower():
            results.append({
                "name": topic_name,
                "description": topic_data["description"],
                "subtopic_count": len(topic_data.get("subtopics", {}))
            })

    return results
