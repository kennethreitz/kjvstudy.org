#!/usr/bin/env python3
"""
Merge new commentary into the main verse_commentary.json file.
Uses a line-by-line approach to handle the large JSON file.
"""

import json
from pathlib import Path
import re

def merge_commentary():
    """Merge new commentary into existing file."""

    # Paths
    main_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary.json"
    new_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary_new_10.json"
    backup_file = main_file.with_suffix('.json.backup')

    print(f"Main file: {main_file}")
    print(f"New file: {new_file}")
    print(f"Backup will be: {backup_file}")

    # Load the new commentary (small file, safe to load fully)
    print("\nLoading new commentary...")
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    print(f"Loaded {sum(len(verses) for book in new_data.values() for verses in book.values())} new commentaries")

    # Create backup of original file
    print("\nCreating backup...")
    import shutil
    shutil.copy2(main_file, backup_file)
    print(f"✓ Backup created: {backup_file}")

    # Now load main file - try with error recovery
    print("\nLoading main commentary file...")
    print("(This may take a moment - file is ~27MB)")

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            main_data = json.load(f)
        print("✓ Main file loaded successfully")
    except json.JSONDecodeError as e:
        print(f"✗ JSON decode error at position {e.pos}: {e.msg}")
        print("\nAttempting to fix JSON...")

        # Read the file and try to fix common issues
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to fix by removing the problematic section and re-parsing
        # This is a last resort - we'll just skip the broken part
        print("Manual intervention required - JSON file has corruption.")
        print("Please fix the JSON file manually or use the standalone file.")
        return False

    # Merge new data into main data
    print("\nMerging new commentary into main file...")
    merged_count = 0

    for book, chapters in new_data.items():
        if book not in main_data:
            main_data[book] = {}
            print(f"  + Added new book: {book}")

        for chapter, verses in chapters.items():
            if chapter not in main_data[book]:
                main_data[book][chapter] = {}
                print(f"  + Added new chapter: {book} {chapter}")

            for verse, content in verses.items():
                main_data[book][chapter][verse] = content
                merged_count += 1
                print(f"  ✓ Merged {book} {chapter}:{verse}")

    # Write merged data back
    print(f"\nWriting merged data to {main_file}...")
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully merged {merged_count} commentaries")
    print(f"✓ New file size: {main_file.stat().st_size:,} bytes")

    # Verify
    print("\nVerifying merge...")
    with open(main_file, 'r', encoding='utf-8') as f:
        verify_data = json.load(f)

    all_verified = True
    for book, chapters in new_data.items():
        for chapter, verses in chapters.items():
            for verse in verses.keys():
                if verse in verify_data.get(book, {}).get(chapter, {}):
                    print(f"  ✓ Verified {book} {chapter}:{verse}")
                else:
                    print(f"  ✗ FAILED: {book} {chapter}:{verse}")
                    all_verified = False

    if all_verified:
        print("\n" + "="*60)
        print("SUCCESS! All commentaries merged and verified.")
        print("="*60)
        print(f"Backup available at: {backup_file}")
        return True
    else:
        print("\n" + "="*60)
        print("WARNING: Some verses failed verification!")
        print("="*60)
        return False

if __name__ == "__main__":
    merge_commentary()
