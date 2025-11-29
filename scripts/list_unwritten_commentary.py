#!/usr/bin/env python3
"""
List verses without substantive commentary.

Usage:
    python scripts/list_unwritten_commentary.py                    # List all verses without commentary
    python scripts/list_unwritten_commentary.py --book John        # List verses in John without commentary
    python scripts/list_unwritten_commentary.py --book John --chapter 3  # List verses in John 3
    python scripts/list_unwritten_commentary.py --stats            # Show statistics only
    python scripts/list_unwritten_commentary.py --random 10        # Show 10 random verses without commentary
"""

import json
import sys
import argparse
import random
from pathlib import Path

# Add parent directory to path to import kjv module
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import bible


def load_commentary():
    """Load the verse commentary JSON"""
    commentary_path = Path(__file__).parent.parent / 'kjvstudy_org' / 'data' / 'verse_commentary.json'
    with open(commentary_path, 'r') as f:
        return json.load(f)


def get_all_verses():
    """Get all verses in the Bible with their references"""
    all_verses = []
    for verse in bible.iter_verses():
        all_verses.append({
            'book': verse.book,
            'chapter': verse.chapter,
            'verse': verse.verse,
            'text': verse.text
        })
    return all_verses


def has_commentary(commentary_data, book, chapter, verse):
    """Check if a verse has commentary"""
    return (book in commentary_data and
            str(chapter) in commentary_data[book] and
            str(verse) in commentary_data[book][str(chapter)])


def main():
    parser = argparse.ArgumentParser(description='List verses without commentary')
    parser.add_argument('--book', help='Filter by book name')
    parser.add_argument('--chapter', type=int, help='Filter by chapter (requires --book)')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--random', type=int, metavar='N', help='Show N random verses without commentary')
    parser.add_argument('--limit', type=int, help='Limit output to N verses')

    args = parser.parse_args()

    # Load commentary data
    commentary = load_commentary()

    # Get all verses
    all_verses = get_all_verses()

    # Filter verses
    filtered = all_verses
    if args.book:
        filtered = [v for v in filtered if v['book'] == args.book]
        if not filtered:
            print(f"Book '{args.book}' not found or has no verses")
            return

    if args.chapter is not None:
        if not args.book:
            print("Error: --chapter requires --book")
            return
        filtered = [v for v in filtered if v['chapter'] == args.chapter]

    # Find verses without commentary
    without_commentary = [
        v for v in filtered
        if not has_commentary(commentary, v['book'], v['chapter'], v['verse'])
    ]

    total_verses = len(filtered)
    without_count = len(without_commentary)
    with_count = total_verses - without_count

    # Show statistics
    if args.stats or not args.random:
        filter_desc = ""
        if args.book and args.chapter:
            filter_desc = f" in {args.book} {args.chapter}"
        elif args.book:
            filter_desc = f" in {args.book}"

        print(f"Verse Commentary Statistics{filter_desc}:")
        print(f"  Total verses: {total_verses:,}")
        print(f"  With commentary: {with_count:,} ({100*with_count/total_verses:.1f}%)")
        print(f"  Without commentary: {without_count:,} ({100*without_count/total_verses:.1f}%)")
        print()

    if args.stats:
        # Show breakdown by book
        books_without = {}
        for v in without_commentary:
            book = v['book']
            books_without[book] = books_without.get(book, 0) + 1

        if books_without:
            print("Verses without commentary by book:")
            for book, count in sorted(books_without.items(), key=lambda x: x[1], reverse=True)[:20]:
                print(f"  {book}: {count}")
        return

    # Show verses
    verses_to_show = without_commentary

    if args.random:
        verses_to_show = random.sample(without_commentary, min(args.random, len(without_commentary)))
    elif args.limit:
        verses_to_show = without_commentary[:args.limit]

    if verses_to_show:
        print("Verses without commentary:")
        print()
        for v in verses_to_show:
            ref = f"{v['book']} {v['chapter']}:{v['verse']}"
            text_preview = v['text'][:100] + "..." if len(v['text']) > 100 else v['text']
            print(f"{ref}")
            print(f"  {text_preview}")
            print()
    else:
        print("All verses in the specified range have commentary!")


if __name__ == '__main__':
    main()
