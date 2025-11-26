"""Bible Stories data loader.

Loads all story JSON files and provides access to stories by category and slug.
"""
import json
from pathlib import Path
from typing import Optional


# Path to stories directory
STORIES_DIR = Path(__file__).parent / "data" / "stories"


def load_all_stories() -> list[dict]:
    """Load all story categories from JSON files."""
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


def get_story_count() -> int:
    """Get total number of stories."""
    return len(get_all_stories_flat())


def get_category_count() -> int:
    """Get total number of categories."""
    return len(load_all_stories())


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
    global STORY_CATEGORIES
    STORY_CATEGORIES = load_all_stories()
