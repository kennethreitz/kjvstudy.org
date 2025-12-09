#!/usr/bin/env python3
"""Find missing verses in Joshua commentary."""

import json
import subprocess
from collections import defaultdict

# Get all Joshua verses from the CLI
result = subprocess.run(
    ['uv', 'run', 'python', 'scripts/commentary_cli.py', 'verse', 'Joshua', '1', '1'],
    capture_output=True,
    text=True
)

# Load existing commentary
with open('kjvstudy_org/data/verse_commentary/joshua.json', 'r') as f:
    commentary = json.load(f)

# Joshua has 24 chapters with these verse counts
chapter_verse_counts = {
    1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35,
    9: 27, 10: 43, 11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10,
    17: 18, 18: 28, 19: 51, 20: 9, 21: 45, 22: 34, 23: 16, 24: 33
}

# Find missing verses
missing = []
for chapter, verse_count in chapter_verse_counts.items():
    ch_key = str(chapter)
    for verse in range(1, verse_count + 1):
        v_key = str(verse)
        if ch_key not in commentary['commentary'] or v_key not in commentary['commentary'][ch_key]:
            missing.append((chapter, verse))

print(f"Total verses in Joshua: {sum(chapter_verse_counts.values())}")
print(f"Missing verses: {len(missing)}\n")

# Group by chapter
by_chapter = defaultdict(list)
for ch, v in missing:
    by_chapter[ch].append(v)

for ch in sorted(by_chapter.keys()):
    verses = sorted(by_chapter[ch])
    print(f"Chapter {ch}: {len(verses)} verses - {verses}")
