"""Study guide data loader (framework-agnostic).

Loads study guide JSON files and exposes the catalog, full content, and the
curated homepage selection. The web layer imports from here; no web framework
is referenced.
"""
import json
from pathlib import Path
from functools import lru_cache

_STUDY_GUIDES_DIR = Path(__file__).parent / "data" / "study_guides"


@lru_cache(maxsize=1)
def _load_study_guides():
    """Load study guides from per-guide JSON files. Cached since data never changes."""
    guides_dir = _STUDY_GUIDES_DIR
    catalog = {}
    content = {}

    for path in sorted(guides_dir.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        guide_content = payload.get("content")
        if not guide_content or "slug" not in guide_content:
            continue

        slug = guide_content["slug"]
        content[slug] = guide_content

        catalog_entry = payload.get("catalog_entry")
        category = payload.get("category", "Uncategorized")
        if catalog_entry:
            catalog.setdefault(category, []).append(catalog_entry)

    return {"catalog": catalog, "content": content}


def get_study_guides_catalog():
    """Return the study guide catalog grouped by category."""
    return _load_study_guides()["catalog"]


def get_study_guides_content():
    """Return full study guide detail content keyed by slug."""
    return _load_study_guides()["content"]


# Curated subset shown on the homepage: which guides appear, grouped and ordered.
# The card content (title/description/verses) comes from the catalog, so only the
# curation lives here.
_FEATURED_HOMEPAGE_GUIDES = {
    "Foundational Studies": ["new-believer", "salvation", "gospel"],
    "Character & Living": ["fruits-spirit", "prayer-faith", "christian-living"],
    "Biblical Themes": ["gods-love", "hope-comfort", "wisdom-guidance"],
    "Doctrinal Studies": ["trinity", "resurrection", "heaven-eternity"],
    "Family & Relationships": ["biblical-marriage", "raising-children", "money-stewardship"],
}


def get_featured_study_guides() -> dict:
    """Homepage's curated study-guide cards, with content pulled from the catalog.

    Returns {category: [catalog_entry copy, ...]} preserving the curated order.
    Entries are copies so callers can annotate them (e.g. verse_refs) without
    mutating the cached catalog.
    """
    by_slug = {}
    for items in get_study_guides_catalog().values():
        for entry in items:
            by_slug[entry["slug"]] = entry

    featured = {}
    for category, slugs in _FEATURED_HOMEPAGE_GUIDES.items():
        entries = [dict(by_slug[s]) for s in slugs if s in by_slug]
        if entries:
            featured[category] = entries
    return featured
