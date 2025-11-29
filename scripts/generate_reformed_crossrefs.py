#!/usr/bin/env python3
"""
Generate Reformed-focused cross-references for KJV Study.

This script helps identify and organize cross-references based on
Reformed theological themes and doctrines.
"""

import json
from pathlib import Path

# Key Reformed Theological Themes
REFORMED_THEMES = {
    "total_depravity": {
        "description": "Human inability and the effects of sin",
        "key_verses": [
            "Romans 3:10-12",
            "Romans 3:23",
            "Ephesians 2:1-3",
            "Genesis 6:5",
            "Jeremiah 17:9",
            "John 6:44",
            "1 Corinthians 2:14",
            "Romans 8:7-8",
        ]
    },
    "unconditional_election": {
        "description": "God's sovereign choice in salvation",
        "key_verses": [
            "Ephesians 1:4-5",
            "Romans 9:11-16",
            "2 Thessalonians 2:13",
            "Acts 13:48",
            "John 15:16",
            "Romans 8:29-30",
            "2 Timothy 1:9",
        ]
    },
    "particular_redemption": {
        "description": "Christ died for His elect/sheep",
        "key_verses": [
            "John 10:11",
            "John 10:15",
            "Matthew 1:21",
            "Ephesians 5:25",
            "Acts 20:28",
            "John 17:9",
        ]
    },
    "irresistible_grace": {
        "description": "Effectual calling and regeneration",
        "key_verses": [
            "John 6:37",
            "John 6:44-45",
            "Acts 16:14",
            "Ezekiel 36:26-27",
            "1 Peter 1:3",
            "2 Corinthians 4:6",
            "Philippians 2:13",
        ]
    },
    "perseverance_saints": {
        "description": "Eternal security and preservation",
        "key_verses": [
            "John 10:27-29",
            "Romans 8:38-39",
            "Philippians 1:6",
            "1 Peter 1:5",
            "Jude 1:24",
            "Romans 8:29-30",
        ]
    },
    "sovereignty_god": {
        "description": "God's absolute sovereignty over all things",
        "key_verses": [
            "Daniel 4:35",
            "Ephesians 1:11",
            "Proverbs 16:9",
            "Proverbs 21:1",
            "Isaiah 46:10",
            "Romans 9:18-21",
            "Acts 4:27-28",
        ]
    },
    "covenant_grace": {
        "description": "Covenant theology and promises",
        "key_verses": [
            "Genesis 17:7",
            "Jeremiah 31:31-33",
            "Hebrews 8:6-13",
            "2 Corinthians 3:6",
            "Galatians 3:15-18",
            "Luke 22:20",
        ]
    },
    "justification_faith": {
        "description": "Justification by faith alone",
        "key_verses": [
            "Romans 3:28",
            "Romans 4:5",
            "Romans 5:1",
            "Galatians 2:16",
            "Ephesians 2:8-9",
            "Philippians 3:9",
            "Genesis 15:6",
        ]
    },
    "union_christ": {
        "description": "Union with Christ",
        "key_verses": [
            "Romans 6:3-5",
            "Galatians 2:20",
            "Ephesians 1:3-4",
            "Colossians 3:3",
            "1 Corinthians 1:30",
            "John 15:1-5",
        ]
    },
}

def parse_verse_range(ref: str) -> list:
    """Parse verse reference like 'Romans 3:10-12' into individual verses."""
    if '-' in ref:
        # Handle verse ranges
        parts = ref.split()
        book = ' '.join(parts[:-1])
        chapter_verses = parts[-1]

        if ':' in chapter_verses:
            chapter, verse_range = chapter_verses.split(':')
            if '-' in verse_range:
                start, end = verse_range.split('-')
                return [f"{book} {chapter}:{v}" for v in range(int(start), int(end) + 1)]
    return [ref]

def generate_theme_crossrefs():
    """Generate cross-references organized by Reformed themes."""

    print("=" * 80)
    print("REFORMED CROSS-REFERENCE GENERATOR")
    print("=" * 80)
    print()

    for theme_key, theme_data in REFORMED_THEMES.items():
        print(f"\n{theme_key.upper().replace('_', ' ')}")
        print(f"  {theme_data['description']}")
        print(f"  Key verses: {len(theme_data['key_verses'])}")
        print()

        # Expand verse ranges
        all_verses = []
        for ref in theme_data['key_verses']:
            all_verses.extend(parse_verse_range(ref))

        for verse in all_verses[:3]:  # Show first 3 as examples
            print(f"    - {verse}")
        if len(all_verses) > 3:
            print(f"    ... and {len(all_verses) - 3} more")

    print()
    print("=" * 80)
    print(f"Total themes: {len(REFORMED_THEMES)}")
    print("=" * 80)

if __name__ == "__main__":
    generate_theme_crossrefs()
