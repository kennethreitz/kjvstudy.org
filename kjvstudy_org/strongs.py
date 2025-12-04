"""
Strong's Concordance lookup system.

Provides Hebrew (H1-H8674) and Greek (G1-G5624) word definitions
from Strong's Exhaustive Concordance.

Data source: https://github.com/openscriptures/strongs (CC-BY-SA)
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

# Cache for loaded dictionaries
_greek_dict: Optional[Dict[str, Any]] = None
_hebrew_dict: Optional[Dict[str, Any]] = None


def _get_data_path() -> Path:
    """Get the path to the strongs data directory."""
    return Path(__file__).parent / "data" / "strongs"


def _load_greek() -> Dict[str, Any]:
    """Load and cache the Greek dictionary."""
    global _greek_dict
    if _greek_dict is None:
        path = _get_data_path() / "greek.json"
        with open(path, "r", encoding="utf-8") as f:
            _greek_dict = json.load(f)
    return _greek_dict


def _load_hebrew() -> Dict[str, Any]:
    """Load and cache the Hebrew dictionary."""
    global _hebrew_dict
    if _hebrew_dict is None:
        path = _get_data_path() / "hebrew.json"
        with open(path, "r", encoding="utf-8") as f:
            _hebrew_dict = json.load(f)
    return _hebrew_dict


def get_strongs_entry(strongs_number: str) -> Optional[Dict[str, Any]]:
    """
    Look up a Strong's number and return the full entry.

    Args:
        strongs_number: A Strong's number like "H1", "G3056", etc.

    Returns:
        Dictionary with word data or None if not found.

    Greek entries have:
        - lemma: Greek word
        - translit: Transliteration
        - strongs_def: Strong's definition
        - kjv_def: KJV translation(s)
        - derivation: Etymology

    Hebrew entries have:
        - lemma: Hebrew word
        - xlit: Transliteration
        - pron: Pronunciation
        - strongs_def: Strong's definition
        - kjv_def: KJV translation(s)
        - derivation: Etymology
    """
    if not strongs_number:
        return None

    # Normalize the number
    strongs_number = strongs_number.upper().strip()

    if strongs_number.startswith("G"):
        dictionary = _load_greek()
    elif strongs_number.startswith("H"):
        dictionary = _load_hebrew()
    else:
        return None

    return dictionary.get(strongs_number)


def get_strongs_definition(strongs_number: str) -> Optional[str]:
    """Get just the Strong's definition for a number."""
    entry = get_strongs_entry(strongs_number)
    if entry:
        return entry.get("strongs_def", "").strip()
    return None


def get_strongs_word(strongs_number: str) -> Optional[str]:
    """Get the original Hebrew/Greek word (lemma)."""
    entry = get_strongs_entry(strongs_number)
    if entry:
        return entry.get("lemma")
    return None


def get_strongs_transliteration(strongs_number: str) -> Optional[str]:
    """Get the transliteration of a Strong's number."""
    entry = get_strongs_entry(strongs_number)
    if entry:
        # Greek uses 'translit', Hebrew uses 'xlit'
        return entry.get("translit") or entry.get("xlit")
    return None


def get_strongs_kjv_usage(strongs_number: str) -> Optional[str]:
    """Get KJV translation usage for a Strong's number."""
    entry = get_strongs_entry(strongs_number)
    if entry:
        return entry.get("kjv_def")
    return None


def format_strongs_entry(strongs_number: str) -> Optional[Dict[str, Any]]:
    """
    Format a Strong's entry for display/API response.

    Returns a normalized dictionary with consistent keys.
    """
    # Normalize: strip leading zeros from number portion (H04566 -> H4566)
    strongs_number = strongs_number.upper().strip()
    if len(strongs_number) > 1 and strongs_number[0] in ('H', 'G'):
        strongs_number = strongs_number[0] + str(int(strongs_number[1:]))

    entry = get_strongs_entry(strongs_number)
    if not entry:
        return None
    is_hebrew = strongs_number.startswith("H")

    return {
        "strongs": strongs_number,
        "language": "Hebrew" if is_hebrew else "Greek",
        "word": entry.get("lemma", ""),
        "transliteration": entry.get("xlit" if is_hebrew else "translit", ""),
        "pronunciation": entry.get("pron", "") if is_hebrew else None,
        "definition": entry.get("strongs_def", "").strip(),
        "kjv_usage": entry.get("kjv_def", ""),
        "derivation": entry.get("derivation", ""),
    }


def get_all_strongs(language: str, page: int = 1, per_page: int = 100) -> dict:
    """
    Get a paginated list of all Strong's entries for a language.

    Args:
        language: "hebrew" or "greek"
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        Dictionary with entries, total count, and pagination info.
    """
    if language == "hebrew":
        dictionary = _load_hebrew()
    elif language == "greek":
        dictionary = _load_greek()
    else:
        return {"entries": [], "total": 0, "page": 1, "per_page": per_page, "total_pages": 0}

    # Sort entries by number
    def sort_key(item):
        num = item[0][1:]  # Remove H or G prefix
        return int(num) if num.isdigit() else 0

    sorted_entries = sorted(dictionary.items(), key=sort_key)
    total = len(sorted_entries)
    total_pages = (total + per_page - 1) // per_page

    # Get the page slice
    start = (page - 1) * per_page
    end = start + per_page
    page_entries = sorted_entries[start:end]

    # Format entries
    entries = []
    for num, entry in page_entries:
        is_hebrew = language == "hebrew"
        entries.append({
            "strongs": num,
            "language": "Hebrew" if is_hebrew else "Greek",
            "word": entry.get("lemma", ""),
            "transliteration": entry.get("xlit" if is_hebrew else "translit", ""),
            "definition": entry.get("strongs_def", "").strip()[:150],  # Truncate for listing
            "kjv_usage": entry.get("kjv_def", ""),
        })

    return {
        "entries": entries,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }


def search_strongs(query: str, language: str = "both", limit: int = 50) -> list:
    """
    Search Strong's dictionaries by definition or KJV usage.

    Args:
        query: Search term
        language: "hebrew", "greek", or "both"
        limit: Maximum results to return

    Returns:
        List of matching entries with Strong's numbers.
    """
    query = query.lower()
    results = []

    if language in ("hebrew", "both"):
        hebrew = _load_hebrew()
        for num, entry in hebrew.items():
            if len(results) >= limit:
                break
            searchable = f"{entry.get('strongs_def', '')} {entry.get('kjv_def', '')}".lower()
            if query in searchable:
                results.append({
                    "strongs": num,
                    "language": "Hebrew",
                    "word": entry.get("lemma", ""),
                    "definition": entry.get("strongs_def", "").strip(),
                    "kjv_usage": entry.get("kjv_def", ""),
                })

    if language in ("greek", "both") and len(results) < limit:
        greek = _load_greek()
        for num, entry in greek.items():
            if len(results) >= limit:
                break
            searchable = f"{entry.get('strongs_def', '')} {entry.get('kjv_def', '')}".lower()
            if query in searchable:
                results.append({
                    "strongs": num,
                    "language": "Greek",
                    "word": entry.get("lemma", ""),
                    "definition": entry.get("strongs_def", "").strip(),
                    "kjv_usage": entry.get("kjv_def", ""),
                })

    return results
