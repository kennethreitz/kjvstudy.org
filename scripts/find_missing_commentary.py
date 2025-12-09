#!/usr/bin/env python3
"""Find missing commentary verses for a book."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

# Standard Bible verse counts
VERSE_COUNTS = {
    "amos": {
        1: 15, 2: 16, 3: 15, 4: 13, 5: 27, 6: 14, 7: 17, 8: 14, 9: 15
    },
    "john": {
        1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59,
        9: 41, 10: 42, 11: 57, 12: 50, 13: 38, 14: 31, 15: 27,
        16: 33, 17: 26, 18: 40, 19: 42, 20: 31, 21: 25
    }
}

def find_missing(book_slug):
    """Find missing verses for a book."""
    filepath = DATA_DIR / f"{book_slug}.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    commentary = data.get("commentary", {})
    verse_counts = VERSE_COUNTS[book_slug]

    missing = []
    total_expected = sum(verse_counts.values())
    total_found = 0

    for chapter, count in verse_counts.items():
        chapter_key = str(chapter)
        chapter_data = commentary.get(chapter_key, {})

        for verse in range(1, count + 1):
            verse_key = str(verse)
            if verse_key in chapter_data:
                total_found += 1
            else:
                missing.append(f"{chapter}:{verse}")

    print(f"\n{book_slug.upper()} COMMENTARY STATUS:")
    print(f"Total verses: {total_expected}")
    print(f"Verses with commentary: {total_found}")
    print(f"Missing verses: {len(missing)}")

    if missing:
        print(f"\nMissing verse references:")
        for ref in missing:
            print(f"  {ref}")

    return missing

if __name__ == "__main__":
    amos_missing = find_missing("amos")
    john_missing = find_missing("john")

    # Print summary for agent
    print(f"\n\nSUMMARY:")
    print(f"Amos: {len(amos_missing)} missing verses")
    print(f"John: {len(john_missing)} missing verses")
