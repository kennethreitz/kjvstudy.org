#!/usr/bin/env python3
"""
Show which verses have enhanced commentary and which don't.

This script analyzes the verse_commentary.json file and displays statistics
about commentary coverage across the Bible. It helps track progress on adding
enhanced verse-by-verse commentary.

Usage:
    python scripts/show_commentary_coverage.py              # Show summary
    python scripts/show_commentary_coverage.py --book Genesis  # Show specific book
    python scripts/show_commentary_coverage.py --list        # List all commentated verses
    python scripts/show_commentary_coverage.py --missing     # Show verses without commentary
    python scripts/show_commentary_coverage.py --stats       # Detailed statistics
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import argparse


# Path to data directory
DATA_DIR = Path(__file__).parent.parent / "kjvstudy_org" / "data"
VERSE_COMMENTARY_PATH = DATA_DIR / "verse_commentary.json"


def load_commentary() -> Dict[str, dict]:
    """Load verse commentary from JSON file."""
    if not VERSE_COMMENTARY_PATH.exists():
        print(f"Error: {VERSE_COMMENTARY_PATH} not found")
        sys.exit(1)

    with open(VERSE_COMMENTARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_verse_ref(verse_ref: str) -> Tuple[str, int, int]:
    """
    Parse verse reference like 'Genesis 1:1' into (book, chapter, verse).

    Args:
        verse_ref: Verse reference string like "Genesis 1:1" or "1 John 3:16"

    Returns:
        Tuple of (book_name, chapter_num, verse_num)
    """
    parts = verse_ref.rsplit(' ', 1)
    if len(parts) != 2:
        return ("Unknown", 0, 0)

    book = parts[0]
    chapter_verse = parts[1]

    if ':' not in chapter_verse:
        return (book, 0, 0)

    chapter_str, verse_str = chapter_verse.split(':', 1)
    try:
        chapter = int(chapter_str)
        verse = int(verse_str)
    except ValueError:
        return (book, 0, 0)

    return (book, chapter, verse)


def organize_by_book(commentary: Dict[str, dict]) -> Dict[str, Dict[int, List[int]]]:
    """
    Organize commentary by book and chapter.

    Returns:
        Dict of {book: {chapter: [verse1, verse2, ...]}}
    """
    organized = defaultdict(lambda: defaultdict(list))

    for verse_ref in commentary.keys():
        book, chapter, verse = parse_verse_ref(verse_ref)
        if chapter > 0 and verse > 0:
            organized[book][chapter].append(verse)

    # Sort verses within each chapter
    for book in organized:
        for chapter in organized[book]:
            organized[book][chapter].sort()

    return dict(organized)


def show_summary(commentary: Dict[str, dict]):
    """Show high-level summary of commentary coverage."""
    organized = organize_by_book(commentary)

    print("=" * 70)
    print("VERSE COMMENTARY COVERAGE SUMMARY")
    print("=" * 70)
    print()

    total_verses = len(commentary)
    total_books = len(organized)

    print(f"📖 Total verses with enhanced commentary: {total_verses}")
    print(f"📚 Books with commentary: {total_books}")
    print()

    print("Coverage by Book:")
    print("-" * 70)

    for book in sorted(organized.keys()):
        chapters = organized[book]
        total_verses_in_book = sum(len(verses) for verses in chapters.values())
        chapter_list = sorted(chapters.keys())
        chapter_range = f"{min(chapter_list)}-{max(chapter_list)}" if len(chapter_list) > 1 else str(chapter_list[0])

        print(f"  {book:30} {total_verses_in_book:4} verses  (chapters: {chapter_range})")

    print()


def show_book_detail(commentary: Dict[str, dict], book_name: str):
    """Show detailed commentary coverage for a specific book."""
    organized = organize_by_book(commentary)

    if book_name not in organized:
        print(f"❌ No commentary found for book: {book_name}")
        print(f"\nAvailable books:")
        for book in sorted(organized.keys()):
            print(f"  - {book}")
        return

    print("=" * 70)
    print(f"COMMENTARY COVERAGE: {book_name}")
    print("=" * 70)
    print()

    chapters = organized[book_name]
    total_verses = sum(len(verses) for verses in chapters.values())

    print(f"Total verses: {total_verses}")
    print(f"Chapters with commentary: {len(chapters)}")
    print()

    for chapter in sorted(chapters.keys()):
        verses = chapters[chapter]
        verse_list = ", ".join(str(v) for v in verses)
        print(f"  Chapter {chapter:3} ({len(verses):2} verses): {verse_list}")

    print()


def list_all_verses(commentary: Dict[str, dict]):
    """List all verses with commentary."""
    organized = organize_by_book(commentary)

    print("=" * 70)
    print("ALL VERSES WITH ENHANCED COMMENTARY")
    print("=" * 70)
    print()

    for book in sorted(organized.keys()):
        print(f"\n{book}")
        print("-" * 70)

        chapters = organized[book]
        for chapter in sorted(chapters.keys()):
            verses = chapters[chapter]
            verse_list = ", ".join(str(v) for v in verses)
            print(f"  {chapter}:{verse_list}")

    print()


def show_statistics(commentary: Dict[str, dict]):
    """Show detailed statistics about commentary coverage."""
    organized = organize_by_book(commentary)

    print("=" * 70)
    print("DETAILED COMMENTARY STATISTICS")
    print("=" * 70)
    print()

    # Total verses
    total_verses = len(commentary)
    total_books = len(organized)
    total_chapters = sum(len(chapters) for chapters in organized.values())

    print(f"📊 Total Statistics:")
    print(f"  • Enhanced verses: {total_verses}")
    print(f"  • Books covered: {total_books}")
    print(f"  • Chapters covered: {total_chapters}")
    print()

    # Book-level stats
    print("📚 Coverage by Testament:")

    # Common book groupings
    ot_books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
                "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
                "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
                "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
                "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
                "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
                "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]

    nt_books = ["Matthew", "Mark", "Luke", "John", "Acts", "Romans",
                "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
                "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
                "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
                "1 John", "2 John", "3 John", "Jude", "Revelation"]

    ot_verses = sum(sum(len(verses) for verses in organized[book].values())
                    for book in ot_books if book in organized)
    nt_verses = sum(sum(len(verses) for verses in organized[book].values())
                    for book in nt_books if book in organized)

    ot_books_with_commentary = sum(1 for book in ot_books if book in organized)
    nt_books_with_commentary = sum(1 for book in nt_books if book in organized)

    print(f"  • Old Testament: {ot_verses} verses across {ot_books_with_commentary} books")
    print(f"  • New Testament: {nt_verses} verses across {nt_books_with_commentary} books")
    print()

    # Top books by coverage
    print("🏆 Top 10 Books by Commentary Coverage:")
    book_verse_counts = []
    for book in organized:
        count = sum(len(verses) for verses in organized[book].values())
        book_verse_counts.append((book, count))

    book_verse_counts.sort(key=lambda x: x[1], reverse=True)
    for i, (book, count) in enumerate(book_verse_counts[:10], 1):
        print(f"  {i:2}. {book:30} {count:4} verses")

    print()

    # Commentary field completeness
    print("✅ Commentary Field Completeness:")
    has_analysis = sum(1 for v in commentary.values() if v.get('analysis'))
    has_historical = sum(1 for v in commentary.values() if v.get('historical_context'))
    has_questions = sum(1 for v in commentary.values() if v.get('questions'))
    has_application = sum(1 for v in commentary.values() if v.get('application'))

    print(f"  • Analysis: {has_analysis}/{total_verses} ({100*has_analysis/total_verses:.1f}%)")
    print(f"  • Historical Context: {has_historical}/{total_verses} ({100*has_historical/total_verses:.1f}%)")
    print(f"  • Questions: {has_questions}/{total_verses} ({100*has_questions/total_verses:.1f}%)")
    print(f"  • Application: {has_application}/{total_verses} ({100*has_application/total_verses:.1f}%)")

    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Show verse commentary coverage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/show_commentary_coverage.py
  python scripts/show_commentary_coverage.py --book Genesis
  python scripts/show_commentary_coverage.py --list
  python scripts/show_commentary_coverage.py --stats
        """
    )

    parser.add_argument('--book', type=str, help='Show detail for a specific book')
    parser.add_argument('--list', action='store_true', help='List all commentated verses')
    parser.add_argument('--stats', action='store_true', help='Show detailed statistics')

    args = parser.parse_args()

    # Load commentary data
    commentary = load_commentary()

    if args.book:
        show_book_detail(commentary, args.book)
    elif args.list:
        list_all_verses(commentary)
    elif args.stats:
        show_statistics(commentary)
    else:
        show_summary(commentary)


if __name__ == "__main__":
    main()
