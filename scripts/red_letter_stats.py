#!/usr/bin/env python3
"""
Red Letter Edition Statistics

This script analyzes and displays statistics about the red letter verses
(words of Jesus Christ) in the KJV Study Bible.

Usage:
    python scripts/red_letter_stats.py
    uv run python scripts/red_letter_stats.py
"""

import json
from pathlib import Path
from collections import Counter, defaultdict


def load_red_letter_data():
    """Load the red letter verses JSON file."""
    data_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "red_letter_verses.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_verse_reference(ref):
    """Parse a verse reference like 'Matthew 3:15' into components."""
    parts = ref.rsplit(' ', 1)
    book = parts[0]
    chapter_verse = parts[1].split(':')
    chapter = int(chapter_verse[0])
    verse = int(chapter_verse[1])
    return book, chapter, verse


def analyze_red_letter_data(data):
    """Analyze the red letter verses and return statistics."""
    verses = data['verses']

    # Basic counts
    total_verses = len(verses)
    full_verses = sum(1 for v in verses.values() if v == 'full')
    partial_verses = total_verses - full_verses

    # Count by book
    books = Counter()
    full_by_book = Counter()
    partial_by_book = Counter()

    # Track consecutive verses (discourses)
    discourses = []
    current_discourse = []
    last_book = None
    last_chapter = None
    last_verse = None

    for ref, text in sorted(verses.items()):
        book, chapter, verse = parse_verse_reference(ref)

        books[book] += 1

        if text == 'full':
            full_by_book[book] += 1
        else:
            partial_by_book[book] += 1

        # Track discourses (consecutive verses)
        if (book == last_book and
            chapter == last_chapter and
            verse == last_verse + 1):
            current_discourse.append((book, chapter, verse))
        else:
            if len(current_discourse) > 1:
                discourses.append(current_discourse)
            current_discourse = [(book, chapter, verse)]

        last_book = book
        last_chapter = chapter
        last_verse = verse

    # Don't forget the last discourse
    if len(current_discourse) > 1:
        discourses.append(current_discourse)

    # Sort discourses by length
    discourses.sort(key=len, reverse=True)

    return {
        'total_verses': total_verses,
        'full_verses': full_verses,
        'partial_verses': partial_verses,
        'books': books,
        'full_by_book': full_by_book,
        'partial_by_book': partial_by_book,
        'discourses': discourses,
    }


def format_discourse(discourse):
    """Format a discourse for display."""
    book, start_chapter, start_verse = discourse[0]
    _, end_chapter, end_verse = discourse[-1]

    if start_chapter == end_chapter:
        return f"{book} {start_chapter}:{start_verse}-{end_verse}"
    else:
        return f"{book} {start_chapter}:{start_verse} - {end_chapter}:{end_verse}"


def print_stats(stats):
    """Print statistics in a formatted way."""
    print("=" * 70)
    print("RED LETTER EDITION STATISTICS")
    print("Words of Jesus Christ in the KJV Bible")
    print("=" * 70)
    print()

    # Overall stats
    print("📊 OVERALL STATISTICS")
    print("-" * 70)
    print(f"Total verses with Christ's words: {stats['total_verses']:,}")
    print(f"  • Full verses (entire verse):   {stats['full_verses']:,} ({stats['full_verses']/stats['total_verses']*100:.1f}%)")
    print(f"  • Partial verses (quoted only): {stats['partial_verses']:,} ({stats['partial_verses']/stats['total_verses']*100:.1f}%)")
    print()

    # By book
    print("📖 VERSES BY BOOK")
    print("-" * 70)
    print(f"{'Book':<15} {'Total':>8} {'Full':>8} {'Partial':>8} {'% Full':>8}")
    print("-" * 70)

    for book in sorted(stats['books'].keys()):
        total = stats['books'][book]
        full = stats['full_by_book'][book]
        partial = stats['partial_by_book'][book]
        pct_full = (full / total * 100) if total > 0 else 0

        print(f"{book:<15} {total:>8,} {full:>8,} {partial:>8,} {pct_full:>7.1f}%")

    print("-" * 70)
    print(f"{'TOTAL':<15} {stats['total_verses']:>8,} {stats['full_verses']:>8,} {stats['partial_verses']:>8,}")
    print()

    # Testament breakdown
    gospels = ['Matthew', 'Mark', 'Luke', 'John']
    gospel_count = sum(stats['books'][book] for book in gospels if book in stats['books'])
    other_count = stats['total_verses'] - gospel_count

    print("📚 BY TESTAMENT")
    print("-" * 70)
    print(f"Gospels (Matthew, Mark, Luke, John): {gospel_count:,} verses ({gospel_count/stats['total_verses']*100:.1f}%)")
    print(f"Acts & Revelation:                   {other_count:,} verses ({other_count/stats['total_verses']*100:.1f}%)")
    print()

    # Longest discourses
    print("💬 LONGEST CONTINUOUS DISCOURSES")
    print("-" * 70)
    print("(Consecutive verses where Jesus speaks)")
    print()

    for i, discourse in enumerate(stats['discourses'][:15], 1):
        length = len(discourse)
        formatted = format_discourse(discourse)
        print(f"{i:2}. {formatted:<40} ({length:3} verses)")

    print()

    # Notable discourses
    print("⭐ NOTABLE DISCOURSES")
    print("-" * 70)

    notable = {
        "Sermon on the Mount": ("Matthew", 5, 1, 7, 27),
        "Olivet Discourse": ("Matthew", 24, 4, 25, 46),
        "Upper Room Discourse": ("John", 14, 1, 16, 33),
        "High Priestly Prayer": ("John", 17, 1, 17, 26),
        "Good Shepherd": ("John", 10, 1, 10, 18),
        "Bread of Life": ("John", 6, 26, 6, 65),
    }

    for name, (book, sc, sv, ec, ev) in notable.items():
        if sc == ec:
            reference = f"{book} {sc}:{sv}-{ev}"
        else:
            reference = f"{book} {sc}:{sv} - {ec}:{ev}"

        print(f"  {name:<25} {reference}")

    print()
    print("=" * 70)


def main():
    """Main function to run the statistics."""
    data = load_red_letter_data()
    stats = analyze_red_letter_data(data)
    print_stats(stats)


if __name__ == '__main__':
    main()
