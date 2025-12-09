#!/usr/bin/env python3
"""Generate commentary for missing verses in Proverbs and Acts."""

import json
import subprocess
import sys

def get_verse_text(book, chapter, verse):
    """Get verse text using the CLI tool."""
    result = subprocess.run(
        ["uv", "run", "python", "scripts/commentary_cli.py", "verse", book, str(chapter), str(verse)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data['text']
    return None

def load_json_file(filepath):
    """Load a JSON file."""
    with open(filepath) as f:
        return json.load(f)

def save_json_file(filepath, data):
    """Save a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Proverbs missing verses
proverbs_missing = [
    (27, 18), (27, 19), (27, 20), (27, 21), (27, 22), (27, 23), (27, 24), (27, 25), (27, 26), (27, 27),
    (28, 14), (28, 15), (28, 16), (28, 17), (28, 18), (28, 19), (28, 20), (28, 21), (28, 22), (28, 23),
    (28, 24), (28, 25), (28, 26), (28, 27), (28, 28), (29, 26), (29, 27), (30, 26), (30, 27), (30, 28),
    (30, 29), (30, 30), (30, 31), (30, 32), (30, 33), (31, 31)
]

# Acts missing verses
acts_missing = [
    (14, 28), (17, 33), (17, 34), (19, 36), (19, 37), (19, 38), (19, 39), (19, 40), (19, 41),
    (22, 25), (22, 26), (22, 27), (22, 28), (22, 29), (22, 30), (25, 17), (25, 18), (25, 19),
    (25, 20), (25, 21), (25, 22), (25, 23), (25, 24), (25, 25), (25, 26), (25, 27), (26, 30),
    (26, 31), (26, 32), (27, 43), (27, 44), (28, 29), (28, 30), (28, 31)
]

# Get all verse texts
print("Fetching verse texts for Proverbs...")
proverbs_verses = {}
for ch, v in proverbs_missing:
    text = get_verse_text("Proverbs", ch, v)
    if text:
        proverbs_verses[f"{ch}:{v}"] = text
        print(f"  {ch}:{v}")

print(f"\nFetching verse texts for Acts...")
acts_verses = {}
for ch, v in acts_missing:
    text = get_verse_text("Acts", ch, v)
    if text:
        acts_verses[f"{ch}:{v}"] = text
        print(f"  {ch}:{v}")

# Save verse texts to a file for reference
with open('missing_verses.json', 'w') as f:
    json.dump({
        'proverbs': proverbs_verses,
        'acts': acts_verses
    }, f, indent=2)

print(f"\nFetched {len(proverbs_verses)} Proverbs verses and {len(acts_verses)} Acts verses")
print("Saved to missing_verses.json")
