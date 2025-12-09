#!/usr/bin/env python3
"""Find missing verses in commentary files."""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from kjvstudy_org.kjv import Bible

def find_missing_verses(book_name: str, commentary_file: Path):
    """Find missing verses in a commentary file."""
    # Load commentary
    with open(commentary_file) as f:
        data = json.load(f)

    commentary = data.get("commentary", {})

    # Get expected structure from Bible
    bible = Bible()

    # Build expected verses from Bible data
    expected_verses = {}
    for verse_ref in bible.iter_verse_references():
        if verse_ref.book == book_name:
            chapter_str = str(verse_ref.chapter)
            if chapter_str not in expected_verses:
                expected_verses[chapter_str] = []
            expected_verses[chapter_str].append(verse_ref.verse)

    # Find missing verses
    missing = []
    for chapter_str, verses in sorted(expected_verses.items(), key=lambda x: int(x[0])):
        chapter_data = commentary.get(chapter_str, {})
        for verse_num in sorted(verses):
            verse_str = str(verse_num)
            if verse_str not in chapter_data:
                missing.append((int(chapter_str), verse_num))

    return missing

def main():
    books = [
        ("Amos", "amos.json"),
        ("John", "john.json")
    ]

    commentary_dir = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary"

    for book_name, filename in books:
        filepath = commentary_dir / filename
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue

        missing = find_missing_verses(book_name, filepath)
        print(f"\n{book_name}: {len(missing)} missing verses")
        for chapter, verse in missing:
            print(f"  {book_name} {chapter}:{verse}")

if __name__ == "__main__":
    main()
