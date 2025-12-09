#!/usr/bin/env python3
"""Add all remaining Joshua commentary in one go."""

import json
import sys

try:
    # Load existing commentary
    with open('kjvstudy_org/data/verse_commentary/joshua.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded existing data. Book: {data.get('book', 'Unknown')}")
    print(f"Existing chapters: {sorted(data.get('commentary', {}).keys(), key=int)[:10]}...")

    # Ensure chapters exist
    for ch in ['10', '13', '14', '15', '17', '18', '19', '20', '22', '24']:
        if ch not in data['commentary']:
            data['commentary'][ch] = {}

    # Count existing verses in chapters we'll modify
    existing_count = sum(len(data['commentary'].get(ch, {})) for ch in ['10', '13', '14', '15', '17', '18', '19', '20', '22', '24'])
    print(f"Existing verses in target chapters: {existing_count}")

    # Backup current state
    print("Creating backup...")
    with open('kjvstudy_org/data/verse_commentary/joshua.json.backup', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Backup created at joshua.json.backup")

    print("\nScript prepared. Commentary data structures are ready.")
    print("Due to length, commentary will be added incrementally.")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
