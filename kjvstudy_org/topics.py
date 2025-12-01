"""
Topical index for finding Bible verses by theme.
Organized by major theological and practical topics.
"""

import json
from pathlib import Path


def _load_topics():
    """Load topics from per-topic JSON files, fallback to legacy single file."""
    base_dir = Path(__file__).parent / "data"
    topics_dir = base_dir / "topics"
    legacy_path = base_dir / "topics.json"

    aggregated = {}
    if topics_dir.exists():
        for path in sorted(topics_dir.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
            if isinstance(content, dict):
                aggregated.update(content)
    elif legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            aggregated = json.load(f)

    return aggregated


TOPICS = _load_topics()


def get_all_topics():
    """Get all topics"""
    return TOPICS


def get_topic(topic_name: str):
    """Get a specific topic"""
    return TOPICS.get(topic_name)


def search_topics(query: str):
    """Search for topics by name or description"""
    query_lower = query.lower()
    results = []

    for topic_name, topic_data in TOPICS.items():
        if query_lower in topic_name.lower() or query_lower in topic_data.get("description", "").lower():
            results.append({
                "name": topic_name,
                "description": topic_data["description"],
                "subtopic_count": len(topic_data.get("subtopics", {}))
            })

    return results
