#!/usr/bin/env python3
"""Find verses in 1 Chronicles that don't have commentary."""

import json
from pathlib import Path

# 1 Chronicles chapter verse counts
CHAPTER_VERSES = {
    1: 54, 2: 55, 3: 24, 4: 43, 5: 26, 6: 81, 7: 40, 8: 40, 9: 44,
    10: 14, 11: 47, 12: 40, 13: 14, 14: 17, 15: 29, 16: 43, 17: 27,
    18: 17, 19: 19, 20: 8, 21: 30, 22: 19, 23: 32, 24: 31, 25: 31,
    26: 32, 27: 34, 28: 21, 29: 30
}

def main():
    filepath = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing = data.get("commentary", {})

    missing = []
    for chapter, verse_count in CHAPTER_VERSES.items():
        chapter_str = str(chapter)
        for verse in range(1, verse_count + 1):
            verse_str = str(verse)
            if chapter_str not in existing or verse_str not in existing[chapter_str]:
                missing.append((chapter, verse))

    print(f"Total verses in 1 Chronicles: {sum(CHAPTER_VERSES.values())}")
    print(f"Verses with commentary: {sum(len(v) for v in existing.values())}")
    print(f"Verses missing commentary: {len(missing)}")
    print("\nFirst 20 missing verses:")
    for i, (ch, v) in enumerate(missing[:20], 1):
        print(f"{i}. 1 Chronicles {ch}:{v}")

if __name__ == "__main__":
    main()
