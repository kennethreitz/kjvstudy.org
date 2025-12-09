#!/usr/bin/env python3
"""Merge new commentary into Joshua file."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Load existing Joshua commentary
joshua_path = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary" / "joshua.json"
with open(joshua_path, 'r', encoding='utf-8') as f:
    joshua_data = json.load(f)

# Load new commentary
new_commentary_path = Path("/tmp/joshua_new_commentary.json")
with open(new_commentary_path, 'r', encoding='utf-8') as f:
    new_data = json.load(f)

# Merge the commentary
for chapter, verses in new_data.items():
    if chapter not in joshua_data["commentary"]:
        joshua_data["commentary"][chapter] = {}

    for verse, content in verses.items():
        # Only add if not already present
        if verse not in joshua_data["commentary"][chapter]:
            joshua_data["commentary"][chapter][verse] = content
            print(f"Added commentary for Joshua {chapter}:{verse}")
        else:
            print(f"Skipped Joshua {chapter}:{verse} (already exists)")

# Save the updated file
with open(joshua_path, 'w', encoding='utf-8') as f:
    json.dump(joshua_data, f, ensure_ascii=False, indent=2)

print(f"\nSaved updated commentary to {joshua_path}")

# Count totals
total_verses = sum(len(verses) for verses in joshua_data["commentary"].values() if isinstance(verses, dict))
print(f"Total verses with commentary: {total_verses}")
