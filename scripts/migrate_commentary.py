#!/usr/bin/env python3
"""
Migrate commentary from verse_commentary.json (root) to per-book files.

Only migrates verses that DON'T already exist in the per-book files.
Leaves duplicates in the source file for review.
"""

import json
import sys
from pathlib import Path

# Paths
ROOT_FILE = Path(__file__).parent.parent / "verse_commentary.json"
DATA_DIR = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary"


def slugify(book: str) -> str:
    """Create filesystem-friendly file name for a book."""
    import re
    slug = re.sub(r"[^a-z0-9]+", "_", book.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "book"


def load_root_commentary():
    """Load the root verse_commentary.json file."""
    if not ROOT_FILE.exists():
        print(f"Source file not found: {ROOT_FILE}")
        return []

    with open(ROOT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both array format and object format
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        # If it's a dict with book as key, convert to list format
        return [{"book": book, "commentary": chapters} for book, chapters in data.items()]
    return []


def load_book_file(book_name: str) -> dict:
    """Load existing per-book commentary file."""
    slug = slugify(book_name)
    book_file = DATA_DIR / f"{slug}.json"

    if not book_file.exists():
        return {"book": book_name, "commentary": {}}

    with open(book_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_book_file(book_name: str, data: dict):
    """Save per-book commentary file."""
    slug = slugify(book_name)
    book_file = DATA_DIR / f"{slug}.json"

    with open(book_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Saved: {book_file.name}")


def main():
    print("=" * 70)
    print("COMMENTARY MIGRATION")
    print("=" * 70)
    print()
    print(f"Source: {ROOT_FILE}")
    print(f"Target: {DATA_DIR}")
    print()

    # Load source data
    source_data = load_root_commentary()
    if not source_data:
        print("No source data to migrate.")
        return

    print(f"Found {len(source_data)} book entries in source file")
    print()

    # Track statistics
    total_migrated = 0
    total_duplicates = 0
    duplicates_by_book = {}

    # Process each book
    for book_entry in source_data:
        book_name = book_entry.get("book")
        new_commentary = book_entry.get("commentary", {})

        if not book_name or not new_commentary:
            continue

        print(f"Processing: {book_name}")

        # Load existing book file
        existing_data = load_book_file(book_name)
        existing_commentary = existing_data.get("commentary", {})

        migrated_count = 0
        duplicate_count = 0
        duplicate_verses = []

        # Check each chapter/verse
        for chapter_str, verses in new_commentary.items():
            if not isinstance(verses, dict):
                continue

            for verse_str, entry in verses.items():
                # Check if verse already exists
                existing_chapter = existing_commentary.get(chapter_str, {})

                if verse_str in existing_chapter:
                    # Duplicate - don't overwrite
                    duplicate_count += 1
                    duplicate_verses.append(f"{chapter_str}:{verse_str}")
                else:
                    # New verse - migrate it
                    if chapter_str not in existing_commentary:
                        existing_commentary[chapter_str] = {}
                    existing_commentary[chapter_str][verse_str] = entry
                    migrated_count += 1

        # Save updated book file if we migrated anything
        if migrated_count > 0:
            existing_data["commentary"] = existing_commentary
            save_book_file(book_name, existing_data)

        print(f"  Migrated: {migrated_count} verses")
        print(f"  Duplicates (skipped): {duplicate_count} verses")

        if duplicate_verses:
            duplicates_by_book[book_name] = duplicate_verses

        total_migrated += migrated_count
        total_duplicates += duplicate_count
        print()

    # Summary
    print("=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"Total verses migrated: {total_migrated}")
    print(f"Total duplicates skipped: {total_duplicates}")
    print()

    if duplicates_by_book:
        print("DUPLICATES BY BOOK (for review):")
        print("-" * 70)
        for book, verses in duplicates_by_book.items():
            print(f"\n{book}:")
            for v in verses[:10]:  # Show first 10
                print(f"  {v}")
            if len(verses) > 10:
                print(f"  ... and {len(verses) - 10} more")

    # Create a new file with only duplicates for review
    if total_duplicates > 0:
        print()
        print("Creating duplicates file for review...")
        duplicates_data = []

        for book_entry in source_data:
            book_name = book_entry.get("book")
            if book_name not in duplicates_by_book:
                continue

            dup_verses = set(duplicates_by_book[book_name])
            dup_commentary = {}

            for chapter_str, verses in book_entry.get("commentary", {}).items():
                if not isinstance(verses, dict):
                    continue
                for verse_str, entry in verses.items():
                    if f"{chapter_str}:{verse_str}" in dup_verses:
                        if chapter_str not in dup_commentary:
                            dup_commentary[chapter_str] = {}
                        dup_commentary[chapter_str][verse_str] = entry

            if dup_commentary:
                duplicates_data.append({
                    "book": book_name,
                    "commentary": dup_commentary
                })

        if duplicates_data:
            dup_file = Path(__file__).parent.parent / "verse_commentary_duplicates.json"
            with open(dup_file, 'w', encoding='utf-8') as f:
                json.dump(duplicates_data, f, ensure_ascii=False, indent=2)
            print(f"Saved duplicates to: {dup_file}")

    print()
    print("Done! Review duplicates if any, then delete source file.")


if __name__ == "__main__":
    main()
