#!/usr/bin/env python3
"""
Import Treasury of Scripture Knowledge cross-references from OpenBible.info

This script converts the TSK data from OpenBible.info into our internal format.
We filter by vote count to ensure quality cross-references.
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

# Book name mapping from abbreviations to full names
BOOK_MAPPING = {
    "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy",
    "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth", "1Sam": "1 Samuel", "2Sam": "2 Samuel",
    "1Kgs": "1 Kings", "2Kgs": "2 Kings", "1Chr": "1 Chronicles", "2Chr": "2 Chronicles",
    "Ezra": "Ezra", "Neh": "Nehemiah", "Esth": "Esther", "Job": "Job", "Ps": "Psalms",
    "Prov": "Proverbs", "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah",
    "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel",
    "Hos": "Hosea", "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah",
    "Mic": "Micah", "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai",
    "Zech": "Zechariah", "Mal": "Malachi",
    "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
    "Rom": "Romans", "1Cor": "1 Corinthians", "2Cor": "2 Corinthians", "Gal": "Galatians",
    "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians", "1Thess": "1 Thessalonians",
    "2Thess": "2 Thessalonians", "1Tim": "1 Timothy", "2Tim": "2 Timothy", "Titus": "Titus",
    "Phlm": "Philemon", "Heb": "Hebrews", "Jas": "James", "1Pet": "1 Peter", "2Pet": "2 Peter",
    "1John": "1 John", "2John": "2 John", "3John": "3 John", "Jude": "Jude", "Rev": "Revelation"
}

def parse_verse_ref(ref: str) -> tuple:
    """Parse a verse reference like 'Gen.1.1' into (book, chapter, verse)."""
    parts = ref.split('.')
    if len(parts) != 3:
        return None

    book_abbr, chapter, verse = parts
    book = BOOK_MAPPING.get(book_abbr)
    if not book:
        return None

    try:
        return (book, int(chapter), int(verse))
    except ValueError:
        return None

def import_crossrefs(min_votes=3):
    """
    Import cross-references from CSV file.

    Args:
        min_votes: Minimum vote threshold (higher = better quality)
    """
    csv_file = Path("/tmp/cross_references_expanded.csv")
    output_file = Path("kjvstudy_org/data/cross_references.json")

    # Load existing cross-references if any
    existing_refs = {}
    if output_file.exists():
        with open(output_file, 'r') as f:
            existing_refs = json.load(f)

    print(f"Existing cross-references: {len(existing_refs)} verses")
    print(f"Importing with minimum {min_votes} votes...")
    print()

    # Parse CSV and build cross-reference dictionary
    crossrefs = defaultdict(list)
    total_rows = 0
    filtered_rows = 0

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_rows += 1

            # Filter by vote count
            votes = int(row['Votes'])
            if votes < min_votes:
                filtered_rows += 1
                continue

            # Parse source and target verses
            from_ref = parse_verse_ref(row['From Verse'])
            to_ref = parse_verse_ref(row['To Verse'])

            if not from_ref or not to_ref:
                continue

            from_book, from_chapter, from_verse = from_ref
            to_book, to_chapter, to_verse = to_ref

            # Create key in our format
            key = f"{from_book}:{from_chapter}:{from_verse}"
            ref_str = f"{to_book} {to_chapter}:{to_verse}"

            # Add to cross-references
            crossrefs[key].append({
                "ref": ref_str,
                "note": "",  # TSK doesn't include notes in this dataset
                "votes": votes
            })

    print(f"Total rows: {total_rows:,}")
    print(f"Filtered out (< {min_votes} votes): {filtered_rows:,}")
    print(f"Imported verses with cross-refs: {len(crossrefs):,}")

    # Sort cross-references by vote count (highest first) and limit to top N per verse
    max_refs_per_verse = 10
    for key in crossrefs:
        refs = crossrefs[key]
        refs.sort(key=lambda x: x['votes'], reverse=True)
        crossrefs[key] = refs[:max_refs_per_verse]

        # Remove votes from final output (not needed in JSON)
        for ref in crossrefs[key]:
            del ref['votes']

    # Count total cross-reference entries
    total_entries = sum(len(refs) for refs in crossrefs.values())
    print(f"Total cross-reference entries: {total_entries:,}")
    print(f"Average per verse: {total_entries/len(crossrefs):.1f}")
    print()

    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(crossrefs, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")
    print()

    # Show sample
    print("Sample cross-references:")
    print("-" * 80)
    for key in list(crossrefs.keys())[:5]:
        print(f"{key}:")
        for ref in crossrefs[key][:3]:
            print(f"  → {ref['ref']}")
        print()

if __name__ == "__main__":
    import sys

    # Allow specifying minimum votes as command-line argument
    min_votes = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    import_crossrefs(min_votes=min_votes)
