"""Loader for poetry formatting data (stanza breaks, poetry books)."""

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POETRY_FILE = DATA_DIR / "poetry_formatting.json"

# Books that are entirely poetry (render each verse as a line)
POETRY_BOOKS = {"Psalms"}


@lru_cache(maxsize=1)
def _load_poetry_data() -> dict:
    """Load poetry formatting data from JSON file."""
    if not POETRY_FILE.exists():
        return {"stanza_breaks": {}}
    with open(POETRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_poetry_book(book: str) -> bool:
    """Check if a book should be rendered as poetry."""
    return book in POETRY_BOOKS


def get_stanza_breaks(book: str, chapter: int) -> set:
    """Get verse numbers that have stanza breaks before them.

    Returns a set of verse numbers where a stanza break should appear
    before the verse (extra vertical spacing).
    """
    if book != "Psalms":
        return set()

    data = _load_poetry_data()
    breaks = data.get("stanza_breaks", {}).get(str(chapter), [])
    return set(breaks)
