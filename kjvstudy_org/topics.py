"""
Topical index for finding Bible verses by theme.
Organized by major theological and practical topics.
"""

import json
from pathlib import Path

# Load topics from JSON data file
_data_path = Path(__file__).parent / "data" / "topics.json"
with open(_data_path, "r", encoding="utf-8") as f:
    TOPICS = json.load(f)


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
