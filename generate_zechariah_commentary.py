#!/usr/bin/env python3
"""
Generate scholarly theological commentary for missing Zechariah verses.
This script will create a JSON structure with all 85 missing verses.
"""

import json
import subprocess

# Missing verses by chapter
MISSING_VERSES = {
    2: [9, 10, 11, 12, 13],
    3: [3, 4, 5, 6, 7, 8, 9, 10],
    4: [7, 8, 9, 10, 11, 12, 13, 14],
    5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    6: [8, 9, 10, 11, 12, 13, 14, 15],
    7: [6, 7, 8, 9, 10, 11, 12, 13, 14],
    9: [13, 14, 15, 16, 17],
    10: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    11: [17],
    12: [11, 12, 13, 14],
    13: [8, 9],
    14: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
}

def get_verse_text(chapter, verse):
    """Get verse text using the CLI tool."""
    result = subprocess.run(
        ['uv', 'run', 'python', 'scripts/commentary_cli.py', 'verse', 'Zechariah', str(chapter), str(verse)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data['text']
    return None

# Collect all verse texts
print("Fetching verse texts...")
verse_texts = {}
for chapter, verses in MISSING_VERSES.items():
    verse_texts[chapter] = {}
    for verse in verses:
        text = get_verse_text(chapter, verse)
        if text:
            verse_texts[chapter][verse] = text
            print(f"  {chapter}:{verse} - {text[:50]}...")

# Save to file for manual commentary generation
with open('/Users/kennethreitz/repos/kjvstudy.org/zechariah_missing_verses.json', 'w') as f:
    json.dump(verse_texts, f, indent=2, ensure_ascii=False)

print(f"\nVerse texts saved to zechariah_missing_verses.json")
print(f"Total verses to generate commentary for: {sum(len(v) for v in MISSING_VERSES.values())}")
