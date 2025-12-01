"""Shared loader for verse commentary data split into per-book JSON files."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Dict

DATA_DIR = Path(__file__).parent.parent / "data"
COMMENTARY_DIR = DATA_DIR / "verse_commentary"


def _normalize_entry(entry: Dict) -> Dict[str, object]:
    """Normalize commentary entry keys and defaults."""
    if not isinstance(entry, dict):
        return {"analysis": "", "historical": "", "questions": []}

    return {
        "analysis": entry.get("analysis", ""),
        "historical": entry.get("historical") or entry.get("historical_context", ""),
        "questions": entry.get("questions", []),
    }


@lru_cache(maxsize=1)
def load_commentary() -> Dict[str, Dict[int, Dict[int, Dict[str, object]]]]:
    """
    Load verse commentary from the per-book directory.

    Returns:
        Nested mapping of Book -> Chapter -> Verse -> commentary entry.
    """
    aggregated: Dict[str, Dict[int, Dict[int, Dict[str, object]]]] = {}
    if not COMMENTARY_DIR.exists():
        return aggregated

    for path in sorted(COMMENTARY_DIR.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        # Handle both wrapped ({book, commentary}) and direct chapter dictionaries
        book_name = payload.get("book") if isinstance(payload, dict) else None
        chapters = payload.get("commentary") if isinstance(payload, dict) else payload

        if not isinstance(chapters, dict):
            continue

        if not book_name:
            book_name = path.stem.replace("_", " ").title()

        book_data = aggregated.setdefault(book_name, {})

        for chapter_key, verses in chapters.items():
            try:
                chapter = int(chapter_key)
            except (TypeError, ValueError):
                continue

            if not isinstance(verses, dict):
                continue

            chapter_data = book_data.setdefault(chapter, {})
            for verse_key, entry in verses.items():
                try:
                    verse = int(verse_key)
                except (TypeError, ValueError):
                    continue

                chapter_data[verse] = _normalize_entry(entry)

    return aggregated


def load_commentary_flat() -> Dict[str, Dict[str, object]]:
    """
    Load commentary as a flat dictionary keyed by "Book Chapter:Verse".

    Returns:
        Dictionary of verse reference strings to commentary entries.
    """
    flat: Dict[str, Dict[str, object]] = {}
    for book, chapters in load_commentary().items():
        for chapter, verses in chapters.items():
            for verse, entry in verses.items():
                flat[f"{book} {chapter}:{verse}"] = entry
    return flat


def _slugify(book: str) -> str:
    """Create filesystem-friendly file name for a book."""
    slug = re.sub(r"[^a-z0-9]+", "_", book.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "book"


def merge_commentary_entries(new_entries: Dict[str, Dict[str, Dict[str, dict]]]) -> None:
    """Merge new commentary entries into per-book JSON files."""
    COMMENTARY_DIR.mkdir(exist_ok=True)

    for book, chapters in new_entries.items():
        book_file = COMMENTARY_DIR / f"{_slugify(book)}.json"

        if book_file.exists():
            with open(book_file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        else:
            payload = {"book": book, "commentary": {}}

        commentary = payload.get("commentary", {})

        for chapter, verses in chapters.items():
            chapter_key = str(chapter)
            chapter_block = commentary.setdefault(chapter_key, {})
            for verse, entry in verses.items():
                chapter_block[str(verse)] = entry

        payload["book"] = payload.get("book") or book
        payload["commentary"] = commentary

        with open(book_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # Clear cached data so future loads pick up updates
    load_commentary.cache_clear()
