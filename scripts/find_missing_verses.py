#!/usr/bin/env python3
"""Find missing verses in commentary files."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.kjv import Bible

def find_missing(book_name: str):
    """Find all verses in a book that don't have commentary."""
    bible = Bible()

    # Determine slug
    slug = book_name.lower().replace(" ", "_").replace("song of solomon", "song_of_solomon")
    filepath = DATA_DIR / f"{slug}.json"

    # Load existing commentary
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"book": book_name, "commentary": {}}

    commentary = data.get("commentary", {})

    # Find missing verses by checking all chapters
    missing = []
    chapters = bible.get_chapters_for_book(book_name)
    if not chapters:
        print(f"Book '{book_name}' not found", file=sys.stderr)
        return []

    for chapter_num in chapters:
        verses = bible.get_verses_by_book_chapter(book_name, chapter_num)
        chapter_verses = commentary.get(str(chapter_num), {})
        for verse_obj in verses:
            verse_num = verse_obj.verse
            if str(verse_num) not in chapter_verses:
                missing.append((chapter_num, verse_num))

    return missing

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_missing_verses.py <book_name>")
        sys.exit(1)

    book = sys.argv[1]
    missing = find_missing(book)

    if missing:
        print(f"Missing {len(missing)} verses in {book}:")
        for ch, v in missing:
            print(f"  {ch}:{v}")
    else:
        print(f"All verses covered in {book}")
