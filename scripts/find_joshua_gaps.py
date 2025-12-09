#!/usr/bin/env python3
"""Find missing verses in Joshua commentary."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.kjv import Bible

# Load Joshua commentary
commentary_path = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary" / "joshua.json"
with open(commentary_path, 'r', encoding='utf-8') as f:
    commentary_data = json.load(f)

commentary = commentary_data.get("commentary", {})

# Get all verses in Joshua from the Bible
bible = Bible()

# Joshua has 24 chapters - known from the book structure
JOSHUA_VERSES = {
    1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35,
    9: 27, 10: 43, 11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10,
    17: 18, 18: 28, 19: 51, 20: 9, 21: 45, 22: 34, 23: 16, 24: 33
}

missing = []
existing_count = 0

for chapter in range(1, 25):
    verse_count = JOSHUA_VERSES[chapter]
    chapter_str = str(chapter)

    chapter_data = commentary.get(chapter_str, {})

    for verse in range(1, verse_count + 1):
        verse_str = str(verse)

        if verse_str in chapter_data:
            existing_count += 1
        else:
            missing.append((chapter, verse))

total_verses = sum(JOSHUA_VERSES.values())
print(f"Joshua total verses: {total_verses}")
print(f"Existing commentary: {existing_count}")
print(f"Missing commentary: {len(missing)}")
print()

if missing:
    print("Missing verses:")
    for chapter, verse in missing:
        print(f"  {chapter}:{verse}")
