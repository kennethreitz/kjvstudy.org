#!/usr/bin/env python3
"""
Script to add famous Proverbs commentary to the verse_commentary.json database.
Loads commentary from proverbs_famous.json and merges it using the standard merge function.
"""

import json
from pathlib import Path
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries


def main():
    # Load the proverbs famous commentary
    script_dir = Path(__file__).parent
    proverbs_file = script_dir / "proverbs_famous.json"

    if not proverbs_file.exists():
        print(f"Error: {proverbs_file} not found")
        return False

    with open(proverbs_file, 'r') as f:
        proverbs_data = json.load(f)

    # Prepare the new commentaries in the expected format
    new_commentaries = {
        "Proverbs": proverbs_data
    }

    # Merge with existing commentaries
    print(f"Merging commentary data from {proverbs_file}")
    print(f"Adding commentary for {len(proverbs_data)} chapters in Proverbs")

    # Count verses being added
    total_verses = 0
    for chapter, verses in proverbs_data.items():
        total_verses += len(verses)
    print(f"Total verses being added: {total_verses}")

    # Perform the merge
    result = merge_commentary_entries(new_commentaries)

    if result:
        print("Successfully merged Proverbs commentary!")
        print(f"Result: {result}")
    else:
        print("Merge completed (no explicit return value)")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
