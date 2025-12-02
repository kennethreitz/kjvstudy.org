#!/usr/bin/env python3
"""
Commentary CLI - Command-line tool for managing verse commentary.

Usage:
    # Check coverage against top verses
    uv run python scripts/commentary_cli.py coverage

    # List missing verses for a book
    uv run python scripts/commentary_cli.py missing Isaiah

    # Get verse text (for agent use)
    uv run python scripts/commentary_cli.py verse Isaiah 7 14

    # Add commentary for a verse
    uv run python scripts/commentary_cli.py add Isaiah 7 14 --analysis "..." --historical "..." --questions "Q1" "Q2"

    # Validate commentary file
    uv run python scripts/commentary_cli.py validate Isaiah

    # Show stats for all books
    uv run python scripts/commentary_cli.py stats
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"


def slugify(book: str) -> str:
    """Create filesystem-friendly file name for a book."""
    slug = re.sub(r"[^a-z0-9]+", book.lower(), "")
    slug = re.sub(r"[^a-z0-9]+", "_", book.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "book"


def load_book_commentary(book: str) -> dict:
    """Load commentary file for a book."""
    slug = slugify(book)
    filepath = DATA_DIR / f"{slug}.json"

    if not filepath.exists():
        return {"book": book, "commentary": {}}

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_book_commentary(book: str, data: dict) -> Path:
    """Save commentary file for a book."""
    slug = slugify(book)
    filepath = DATA_DIR / f"{slug}.json"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath


def get_verse_text(book: str, chapter: int, verse: int) -> dict | None:
    """Get verse text from the KJV module."""
    try:
        from kjvstudy_org.kjv import Bible
        bible = Bible()
        text = bible.get_verse_text(book, chapter, verse)
        if text:
            return {"book": book, "chapter": chapter, "verse": verse, "text": text}
        return None
    except Exception as e:
        print(f"Error loading verse: {e}", file=sys.stderr)
        return None


def cmd_verse(args):
    """Get verse text."""
    verse = get_verse_text(args.book, args.chapter, args.verse)
    if verse:
        print(json.dumps(verse, indent=2))
    else:
        print(f"Verse not found: {args.book} {args.chapter}:{args.verse}", file=sys.stderr)
        sys.exit(1)


def cmd_coverage(args):
    """Check coverage against top verses list."""
    # Import check_top_verses functionality
    from check_top_verses import TOP_VERSES, check_coverage

    covered, missing = check_coverage()
    total = len(TOP_VERSES)

    print(f"Coverage: {len(covered)}/{total} ({100*len(covered)/total:.1f}%)")
    print(f"Missing: {len(missing)} verses")

    if args.verbose and missing:
        print("\nMissing verses:")
        for book, verses in sorted(missing.items()):
            print(f"  {book}: {', '.join(map(str, verses))}")


def cmd_missing(args):
    """List missing verses for a book."""
    from check_top_verses import TOP_VERSES

    book = args.book
    if book not in TOP_VERSES:
        print(f"Book '{book}' not in top verses list", file=sys.stderr)
        print(f"Available books: {', '.join(sorted(TOP_VERSES.keys()))}", file=sys.stderr)
        sys.exit(1)

    data = load_book_commentary(book)
    commentary = data.get("commentary", {})

    missing = []
    for chapter, verses in TOP_VERSES[book].items():
        chapter_data = commentary.get(str(chapter), {})
        for verse in verses:
            if str(verse) not in chapter_data:
                missing.append(f"{chapter}:{verse}")

    if missing:
        print(f"Missing verses in {book}:")
        for ref in missing:
            print(f"  {ref}")
    else:
        print(f"All top verses covered in {book}")


def cmd_add(args):
    """Add commentary for a verse."""
    book = args.book
    chapter = str(args.chapter)
    verse = str(args.verse)

    # Load existing data
    data = load_book_commentary(book)
    commentary = data.get("commentary", {})

    # Check if verse already exists
    if chapter in commentary and verse in commentary[chapter]:
        if not args.force:
            print(f"Commentary already exists for {book} {chapter}:{verse}", file=sys.stderr)
            print("Use --force to overwrite", file=sys.stderr)
            sys.exit(1)

    # Build commentary entry
    entry = {
        "analysis": args.analysis,
        "historical": args.historical,
        "questions": args.questions or []
    }

    # Add to structure
    if chapter not in commentary:
        commentary[chapter] = {}
    commentary[chapter][verse] = entry
    data["commentary"] = commentary

    # Save
    filepath = save_book_commentary(book, data)
    print(f"Added commentary for {book} {chapter}:{verse}")
    print(f"Saved to: {filepath}")


def cmd_validate(args):
    """Validate commentary file structure."""
    book = args.book
    data = load_book_commentary(book)

    errors = []
    warnings = []

    if "book" not in data:
        errors.append("Missing 'book' field")

    if "commentary" not in data:
        errors.append("Missing 'commentary' field")
    else:
        for chapter, verses in data["commentary"].items():
            if not isinstance(verses, dict):
                errors.append(f"Chapter {chapter} is not a dict")
                continue

            for verse, entry in verses.items():
                ref = f"{chapter}:{verse}"

                if not isinstance(entry, dict):
                    errors.append(f"{ref}: Entry is not a dict")
                    continue

                if "analysis" not in entry:
                    warnings.append(f"{ref}: Missing 'analysis'")
                if "historical" not in entry:
                    warnings.append(f"{ref}: Missing 'historical'")
                if "questions" not in entry:
                    warnings.append(f"{ref}: Missing 'questions'")
                elif not isinstance(entry.get("questions"), list):
                    errors.append(f"{ref}: 'questions' is not a list")

    if errors:
        print(f"ERRORS in {book}:")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print(f"WARNINGS in {book}:")
        for w in warnings:
            print(f"  - {w}")

    if not errors and not warnings:
        print(f"{book}: Valid")

    sys.exit(1 if errors else 0)


def cmd_stats(args):
    """Show stats for all commentary files."""
    files = list(DATA_DIR.glob("*.json"))

    print(f"{'Book':<20} {'Chapters':<10} {'Verses':<10}")
    print("-" * 42)

    total_chapters = 0
    total_verses = 0

    for filepath in sorted(files):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        book = data.get("book", filepath.stem)
        commentary = data.get("commentary", {})

        chapters = len(commentary)
        verses = sum(len(v) for v in commentary.values() if isinstance(v, dict))

        print(f"{book:<20} {chapters:<10} {verses:<10}")
        total_chapters += chapters
        total_verses += verses

    print("-" * 42)
    print(f"{'TOTAL':<20} {total_chapters:<10} {total_verses:<10}")


def cmd_export_verse(args):
    """Export verse with commentary as JSON (for agents)."""
    book = args.book
    chapter = args.chapter
    verse = args.verse

    # Get verse text
    verse_data = get_verse_text(book, chapter, verse)

    # Get commentary
    data = load_book_commentary(book)
    commentary = data.get("commentary", {}).get(str(chapter), {}).get(str(verse))

    output = {
        "reference": f"{book} {chapter}:{verse}",
        "text": verse_data.get("text") if verse_data else None,
        "has_commentary": commentary is not None,
        "commentary": commentary
    }

    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for managing verse commentary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # verse command
    p_verse = subparsers.add_parser("verse", help="Get verse text")
    p_verse.add_argument("book", help="Book name")
    p_verse.add_argument("chapter", type=int, help="Chapter number")
    p_verse.add_argument("verse", type=int, help="Verse number")
    p_verse.set_defaults(func=cmd_verse)

    # coverage command
    p_coverage = subparsers.add_parser("coverage", help="Check top verses coverage")
    p_coverage.add_argument("-v", "--verbose", action="store_true", help="Show missing verses")
    p_coverage.set_defaults(func=cmd_coverage)

    # missing command
    p_missing = subparsers.add_parser("missing", help="List missing verses for a book")
    p_missing.add_argument("book", help="Book name")
    p_missing.set_defaults(func=cmd_missing)

    # add command
    p_add = subparsers.add_parser("add", help="Add commentary for a verse")
    p_add.add_argument("book", help="Book name")
    p_add.add_argument("chapter", type=int, help="Chapter number")
    p_add.add_argument("verse", type=int, help="Verse number")
    p_add.add_argument("--analysis", required=True, help="Theological analysis")
    p_add.add_argument("--historical", required=True, help="Historical context")
    p_add.add_argument("--questions", nargs="+", help="Reflection questions")
    p_add.add_argument("--force", action="store_true", help="Overwrite existing")
    p_add.set_defaults(func=cmd_add)

    # validate command
    p_validate = subparsers.add_parser("validate", help="Validate commentary file")
    p_validate.add_argument("book", help="Book name")
    p_validate.set_defaults(func=cmd_validate)

    # stats command
    p_stats = subparsers.add_parser("stats", help="Show stats for all books")
    p_stats.set_defaults(func=cmd_stats)

    # export command
    p_export = subparsers.add_parser("export", help="Export verse with commentary")
    p_export.add_argument("book", help="Book name")
    p_export.add_argument("chapter", type=int, help="Chapter number")
    p_export.add_argument("verse", type=int, help="Verse number")
    p_export.set_defaults(func=cmd_export_verse)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
