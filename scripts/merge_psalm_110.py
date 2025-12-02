#!/usr/bin/env python3
"""
Merge Psalm 110 commentary into verse_commentary.json
"""

import json
from pathlib import Path


def merge_psalm_110():
    """Load Psalm 110 commentary and merge into main commentary file."""

    # Define paths
    script_dir = Path(__file__).parent
    psalm_110_file = script_dir / "psalm_110.json"
    commentary_file = script_dir.parent / "verse_commentary.json"

    # Load Psalm 110 commentary
    with open(psalm_110_file, 'r', encoding='utf-8') as f:
        psalm_110_data = json.load(f)

    # Load existing commentary
    with open(commentary_file, 'r', encoding='utf-8') as f:
        commentary = json.load(f)

    # Merge Psalm 110 into Psalms section
    if 'commentary' not in commentary:
        commentary['commentary'] = {}

    # Add or update Psalm 110
    psalm_110_verses = psalm_110_data.get('110', {})
    if psalm_110_verses:
        commentary['commentary']['110'] = psalm_110_verses
        print(f"✓ Added Psalm 110 with {len(psalm_110_verses)} verses")

    # Write back to file
    with open(commentary_file, 'w', encoding='utf-8') as f:
        json.dump(commentary, f, indent=2, ensure_ascii=False)

    print(f"✓ Merged into {commentary_file}")
    print(f"✓ Psalm 110 commentary successfully added to verse_commentary.json")


if __name__ == "__main__":
    merge_psalm_110()
