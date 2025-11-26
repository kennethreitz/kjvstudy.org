"""
Detailed biographical information for notable biblical figures.
Provides richer context than what's available in the GEDCOM data.
"""

import json
from pathlib import Path

# Load biographies from JSON data file
_data_path = Path(__file__).parent / "data" / "biographies.json"
with open(_data_path, "r", encoding="utf-8") as f:
    _data = json.load(f)
    BIOGRAPHIES = _data["biographies"]
    BIOGRAPHY_ALIASES = _data["aliases"]


def get_biography(person_name: str) -> dict:
    """
    Get biographical information for a biblical figure.

    Handles alternate name forms through the BIOGRAPHY_ALIASES mapping.

    Args:
        person_name: Name of the person (e.g., "Abraham", "David", "Noah or Noe")

    Returns:
        Dictionary with biography info, or None if not found
    """
    # Try exact match first
    bio = BIOGRAPHIES.get(person_name)
    if bio:
        return bio

    # Try aliases
    canonical_name = BIOGRAPHY_ALIASES.get(person_name)
    if canonical_name:
        return BIOGRAPHIES.get(canonical_name)

    return None


def has_biography(person_name: str) -> bool:
    """Check if a person has detailed biographical information."""
    # Check exact match
    if person_name in BIOGRAPHIES:
        return True
    # Check aliases
    canonical_name = BIOGRAPHY_ALIASES.get(person_name)
    if canonical_name and canonical_name in BIOGRAPHIES:
        return True
    return False
