#!/usr/bin/env python3
"""
Fix red letter verses that incorrectly include narrative text.

This script finds verses marked as "full" that contain narrative introductions
(like "Jesus answered them,") and extracts only the actual spoken words.
"""

import json
import re
from pathlib import Path
from kjvstudy_org.kjv import Bible

# Common narrative patterns that should NOT be in red
NARRATIVE_PATTERNS = [
    # "Jesus answered and said unto them," -> extract after the comma
    r'^(.*?Jesus answered and said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Jesus answered\s+(?:them|him|her|it)[,:])\s*(.+)$',
    r'^(.*?Jesus answered(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?And Jesus said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Jesus said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Jesus saith(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Then said Jesus(?:\s+(?:to|unto)\s+(?:them|him|her))?[,:])\s*(.+)$',
    r'^(.*?And he said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?he answered and said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?he answered(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?But he answered and said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?But Jesus answered and said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?But Jesus called(?:\s+(?:them|him|her))?(?:\s+unto\s+him)? and said[,:])\s*(.+)$',
    r'^(.*?When Jesus (?:perceived|understood) it, he said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?And when he had called (?:all )?(?:the )?people(?:\s+unto him)?(?:\s+with his disciples also)?, he said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Jesus answereth again, and saith(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?And while they abode in Galilee, Jesus said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?Jesus called them(?:\s+unto him)? and said[,:])\s*(.+)$',

    # Handle cases with preceding dialogue
    r'^(.*?\. (?:And )?Jesus said(?:\s+unto\s+(?:them|him|her|it))?[,:])\s*(.+)$',
    r'^(.*?\. And he answered and said[,:])\s*(.+)$',
]


def extract_spoken_words(verse_text: str) -> str | None:
    """
    Extract only the spoken words from a verse, removing narrative introduction.

    Returns the spoken words, or None if no clear pattern is found.
    """
    # Try each pattern
    for pattern in NARRATIVE_PATTERNS:
        match = re.match(pattern, verse_text, re.IGNORECASE)
        if match:
            narrative = match.group(1)
            spoken = match.group(2)
            return spoken.strip()

    return None


def main():
    # Load the Bible and red letter data
    bible = Bible()
    data_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "red_letter_verses.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    verses = data.get("verses", {})

    # Find problematic verses
    fixes = []
    no_match = []

    for verse_key, value in verses.items():
        if value == 'full':
            # Parse the verse key
            parts = verse_key.rsplit(':', 1)
            if len(parts) == 2:
                book_chapter, verse_num = parts
                book_parts = book_chapter.rsplit(' ', 1)
                if len(book_parts) == 2:
                    book, chapter = book_parts
                    try:
                        text = bible.get_verse_text(book, int(chapter), int(verse_num))

                        # Check if it has narrative introduction
                        if any(phrase in text for phrase in ['Jesus answered', 'Jesus said', 'he answered', 'he said', 'Jesus saith']):
                            spoken = extract_spoken_words(text)
                            if spoken:
                                fixes.append((verse_key, text, spoken))
                            else:
                                no_match.append((verse_key, text))
                    except Exception as e:
                        print(f"Error processing {verse_key}: {e}")

    # Display findings
    print(f"\n{'='*80}")
    print(f"Found {len(fixes)} verses that can be automatically fixed")
    print(f"Found {len(no_match)} verses that need manual review")
    print(f"{'='*80}\n")

    if fixes:
        print(f"\nVERSES TO FIX ({len(fixes)}):")
        print("="*80)
        for verse_key, original, spoken in fixes[:10]:
            print(f"\n{verse_key}")
            print(f"  Original: {original}")
            print(f"  Spoken:   {spoken}")
        if len(fixes) > 10:
            print(f"\n... and {len(fixes) - 10} more")

    if no_match:
        print(f"\n\nVERSES NEEDING MANUAL REVIEW ({len(no_match)}):")
        print("="*80)
        for verse_key, text in no_match[:5]:
            print(f"\n{verse_key}")
            print(f"  {text}")
        if len(no_match) > 5:
            print(f"\n... and {len(no_match) - 5} more")

    # Apply fixes automatically
    print(f"\n{'='*80}")
    print(f"Applying fixes to {len(fixes)} verses...")

    # Apply fixes
    for verse_key, _, spoken in fixes:
        verses[verse_key] = spoken

    # Save updated data
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Updated {len(fixes)} verses in {data_path}")

    if no_match:
        print(f"\n⚠ {len(no_match)} verses still need manual review")
        print("These verses may have complex narrative structures that couldn't be")
        print("automatically parsed. Please review them manually.")

        # Save list of verses needing manual review
        manual_path = Path(__file__).parent.parent / "scripts" / "red_letter_manual_review.txt"
        with open(manual_path, 'w', encoding='utf-8') as f:
            for verse_key, text in no_match:
                f.write(f"{verse_key}\n")
                f.write(f"  {text}\n\n")
        print(f"\nSaved list to: {manual_path}")


if __name__ == '__main__':
    main()
