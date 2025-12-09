#!/usr/bin/env python3
"""Generate commentary for missing verses."""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from kjvstudy_org.kjv import Bible

def get_verse_text(bible, book, chapter, verse):
    """Get verse text from Bible."""
    verse_key = f"{book} {chapter}:{verse}"
    try:
        return bible.get_verse_text(book, chapter, verse)
    except:
        return None

def main():
    bible = Bible()

    # Missing verses for Amos
    amos_verses = [
        (1, 14), (1, 15), (2, 15), (2, 16), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12),
        (3, 13), (3, 14), (3, 15), (4, 13), (5, 25), (5, 26), (5, 27), (6, 2), (6, 3),
        (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
        (6, 13), (6, 14), (7, 15), (7, 16), (7, 17), (8, 12), (8, 13), (8, 14),
        (9, 14), (9, 15)
    ]

    # Missing verses for John
    john_verses = [
        (8, 59), (10, 31), (10, 32), (10, 33), (10, 34), (10, 35), (10, 36), (10, 37),
        (10, 38), (10, 39), (10, 40), (10, 41), (10, 42), (13, 38), (14, 28), (14, 29),
        (14, 30), (14, 31), (15, 27), (17, 22), (17, 23), (17, 24), (17, 25), (17, 26),
        (19, 31), (19, 32), (19, 33), (19, 34), (19, 35), (19, 36), (19, 37), (19, 38),
        (19, 39), (19, 40), (19, 41), (19, 42)
    ]

    print("=== AMOS VERSES ===\n")
    for chapter, verse in amos_verses:
        text = get_verse_text(bible, "Amos", chapter, verse)
        print(f"Amos {chapter}:{verse}")
        print(f"{text}\n")

    print("\n=== JOHN VERSES ===\n")
    for chapter, verse in john_verses:
        text = get_verse_text(bible, "John", chapter, verse)
        print(f"John {chapter}:{verse}")
        print(f"{text}\n")

if __name__ == "__main__":
    main()
