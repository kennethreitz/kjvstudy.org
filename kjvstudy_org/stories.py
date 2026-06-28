"""Bible Stories data loader.

Loads all story JSON files and provides access to stories by category and slug.
"""
import json
from functools import lru_cache
from pathlib import Path
from typing import Optional


# Path to stories directory
STORIES_DIR = Path(__file__).parent / "data" / "stories"


def _load_all_stories_uncached() -> list[dict]:
    """Load all story categories from JSON files (internal, uncached)."""
    categories = []

    if not STORIES_DIR.exists():
        return categories

    # Load JSON files in order (they're numbered)
    json_files = sorted(STORIES_DIR.glob("*.json"))

    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                category_data = json.load(f)
                categories.append(category_data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {json_file}: {e}")
            continue

    return categories


# Load stories once at module import time
_STORIES_CACHE: list[dict] | None = None


def load_all_stories() -> list[dict]:
    """Load all story categories from JSON files (cached)."""
    global _STORIES_CACHE
    if _STORIES_CACHE is None:
        _STORIES_CACHE = _load_all_stories_uncached()
    return _STORIES_CACHE


def get_all_stories_flat() -> list[dict]:
    """Get all stories as a flat list with category info attached."""
    categories = load_all_stories()
    all_stories = []

    for category in categories:
        category_name = category.get("category", "Unknown")
        category_slug = category.get("slug", "unknown")

        for story in category.get("stories", []):
            story_with_category = story.copy()
            story_with_category["category_name"] = category_name
            story_with_category["category_slug"] = category_slug
            all_stories.append(story_with_category)

    return all_stories


def get_story_by_slug(slug: str) -> Optional[dict]:
    """Find a story by its slug."""
    for story in get_all_stories_flat():
        if story.get("slug") == slug:
            return story
    return None


def get_adjacent_stories(slug: str) -> tuple[Optional[dict], Optional[dict]]:
    """Return (prev_story, next_story) around the story with the given slug.

    Either side is None at the ends of the list; returns (None, None) when the
    slug is not found.
    """
    stories = get_all_stories_flat()
    for i, story in enumerate(stories):
        if story.get("slug") == slug:
            prev_story = stories[i - 1] if i > 0 else None
            next_story = stories[i + 1] if i < len(stories) - 1 else None
            return prev_story, next_story
    return None, None


def get_stories_by_category(category_slug: str) -> list[dict]:
    """Get all stories in a specific category."""
    categories = load_all_stories()

    for category in categories:
        if category.get("slug") == category_slug:
            stories = []
            for story in category.get("stories", []):
                story_with_category = story.copy()
                story_with_category["category_name"] = category.get("category", "Unknown")
                story_with_category["category_slug"] = category_slug
                stories.append(story_with_category)
            return stories

    return []


def get_category_by_slug(category_slug: str) -> Optional[dict]:
    """Get a category by its slug."""
    categories = load_all_stories()

    for category in categories:
        if category.get("slug") == category_slug:
            return category
    return None


# Cache story counts
_CACHED_STORY_COUNT = None
_CACHED_CATEGORY_COUNT = None


def get_story_count() -> int:
    """Get total number of stories (cached)."""
    global _CACHED_STORY_COUNT
    if _CACHED_STORY_COUNT is None:
        _CACHED_STORY_COUNT = len(get_all_stories_flat())
    return _CACHED_STORY_COUNT


def get_category_count() -> int:
    """Get total number of categories (cached)."""
    global _CACHED_CATEGORY_COUNT
    if _CACHED_CATEGORY_COUNT is None:
        _CACHED_CATEGORY_COUNT = len(load_all_stories())
    return _CACHED_CATEGORY_COUNT


# Pre-load categories on module import for faster access
STORY_CATEGORIES = None


def get_categories() -> list[dict]:
    """Get all categories (cached)."""
    global STORY_CATEGORIES
    if STORY_CATEGORIES is None:
        STORY_CATEGORIES = load_all_stories()
    return STORY_CATEGORIES


def refresh_stories():
    """Refresh the cached stories (useful after adding new files)."""
    global _STORIES_CACHE, STORY_CATEGORIES, _CACHED_STORY_COUNT, _CACHED_CATEGORY_COUNT
    # Clear the primary cache first; otherwise load_all_stories() just returns
    # the stale data and nothing actually reloads.
    _STORIES_CACHE = None
    _CACHED_STORY_COUNT = None
    _CACHED_CATEGORY_COUNT = None
    STORY_CATEGORIES = load_all_stories()
