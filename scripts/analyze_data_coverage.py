#!/usr/bin/env python3
"""
Analyze data coverage to identify gaps and areas for improvement.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import bible
from kjvstudy_org.utils.commentary_loader import load_commentary_flat


def analyze_commentary_coverage():
    """Analyze verse commentary coverage."""
    print("=" * 80)
    print("VERSE COMMENTARY COVERAGE ANALYSIS")
    print("=" * 80)
    print()

    commentary = load_commentary_flat()

    total_verses = 31102
    verses_with_commentary = len(commentary)
    coverage_pct = (verses_with_commentary / total_verses) * 100

    print(f"Total verses in Bible: {total_verses:,}")
    print(f"Verses with commentary: {verses_with_commentary:,}")
    print(f"Coverage: {coverage_pct:.1f}%")
    print()

    # Analyze by book
    by_book = defaultdict(int)
    for verse_ref in commentary.keys():
        book = verse_ref.split(':')[0] if ':' in verse_ref else verse_ref.split(' ')[0]
        by_book[book] += 1

    print(f"Books with commentary ({len(by_book)} books):")
    for book, count in sorted(by_book.items(), key=lambda x: x[1], reverse=True):
        print(f"  {book}: {count} verses")
    print()

    return verses_with_commentary


def analyze_cross_reference_coverage():
    """Analyze cross-reference coverage."""
    print("=" * 80)
    print("CROSS-REFERENCE COVERAGE ANALYSIS")
    print("=" * 80)
    print()

    xref_file = Path("kjvstudy_org/data/cross_references.json")
    with open(xref_file, 'r') as f:
        cross_refs = json.load(f)

    total_verses = 31102
    verses_with_xrefs = len(cross_refs)
    total_xrefs = sum(len(refs) for refs in cross_refs.values())
    avg_xrefs_per_verse = total_xrefs / verses_with_xrefs if verses_with_xrefs > 0 else 0

    # Count how many have descriptions
    xrefs_with_descriptions = 0
    xrefs_without_descriptions = 0

    for refs in cross_refs.values():
        for ref in refs:
            if ref.get('note') and ref['note'].strip():
                xrefs_with_descriptions += 1
            else:
                xrefs_without_descriptions += 1

    coverage_pct = (verses_with_xrefs / total_verses) * 100
    description_pct = (xrefs_with_descriptions / total_xrefs) * 100 if total_xrefs > 0 else 0

    print(f"Total verses in Bible: {total_verses:,}")
    print(f"Verses with cross-references: {verses_with_xrefs:,}")
    print(f"Coverage: {coverage_pct:.1f}%")
    print()
    print(f"Total cross-reference entries: {total_xrefs:,}")
    print(f"Average per verse: {avg_xrefs_per_verse:.1f}")
    print()
    print(f"Cross-refs with descriptions: {xrefs_with_descriptions:,} ({description_pct:.1f}%)")
    print(f"Cross-refs without descriptions: {xrefs_without_descriptions:,}")
    print()


def analyze_word_studies():
    """Analyze word studies coverage."""
    print("=" * 80)
    print("WORD STUDIES ANALYSIS")
    print("=" * 80)
    print()

    word_studies_file = Path("kjvstudy_org/data/word_studies.json")
    with open(word_studies_file, 'r') as f:
        word_studies = json.load(f)

    total_studies = len(word_studies)

    # Categorize by OT/NT coverage
    has_ot = 0
    has_nt = 0
    has_both = 0

    for word, data in word_studies.items():
        ot = bool(data.get('ot_term'))
        nt = bool(data.get('nt_term'))

        if ot and nt:
            has_both += 1
        elif ot:
            has_ot += 1
        elif nt:
            has_nt += 1

    print(f"Total word studies: {total_studies}")
    print(f"  Both OT and NT: {has_both}")
    print(f"  OT only: {has_ot}")
    print(f"  NT only: {has_nt}")
    print()

    # Show sample words
    print("Sample words studied:")
    for word in list(word_studies.keys())[:10]:
        print(f"  - {word}")
    print()


def analyze_books_without_data():
    """Identify books with minimal study material."""
    print("=" * 80)
    print("BOOKS WITH MINIMAL STUDY MATERIAL")
    print("=" * 80)
    print()

    books = bible.get_books()

    # Load commentary
    commentary = load_commentary_flat()

    # Count verses per book
    book_stats = {}

    for book in books:
        chapters = bible.get_chapters_for_book(book)
        total_verses = sum(len(bible.get_verses_by_book_chapter(book, ch)) for ch in chapters)

        # Count commentary for this book
        commentary_count = sum(1 for ref in commentary.keys() if ref.startswith(book + ':') or ref.startswith(book + ' '))

        book_stats[book] = {
            'total_verses': total_verses,
            'commentary': commentary_count,
            'commentary_pct': (commentary_count / total_verses * 100) if total_verses > 0 else 0
        }

    # Sort by lowest commentary percentage
    sorted_books = sorted(book_stats.items(), key=lambda x: x[1]['commentary_pct'])

    print("Books with lowest commentary coverage:")
    print()
    for book, stats in sorted_books[:15]:
        print(f"{book:20} {stats['total_verses']:4} verses, {stats['commentary']:4} commentary ({stats['commentary_pct']:.1f}%)")
    print()


def main():
    """Run all analyses."""
    analyze_commentary_coverage()
    analyze_cross_reference_coverage()
    analyze_word_studies()
    analyze_books_without_data()

    print("=" * 80)
    print("RECOMMENDATIONS FOR IMPROVEMENT")
    print("=" * 80)
    print()
    print("1. Expand verse commentary to more books (currently 6-7% coverage)")
    print("2. Add more word studies (currently 53 terms)")
    print("3. Focus commentary on underserved books")
    print("4. Consider adding thematic commentary (not just verse-by-verse)")
    print()


if __name__ == "__main__":
    main()
