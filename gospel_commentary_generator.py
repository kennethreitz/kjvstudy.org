#!/usr/bin/env python
"""
Generate comprehensive verse-by-verse commentary for key Gospel passages.

This script creates detailed theological analysis focusing on:
1. Major theological passages
2. Key teachings of Jesus
3. Miracle narratives
4. Passion and resurrection accounts
5. Unique material in each Gospel

Due to the extensive scope (3,779 verses), this focuses on generating high-quality
commentary for significant passages that can serve as templates for future expansion.
"""

import json
from pathlib import Path
from typing import Dict, List

# Key passages that deserve detailed commentary
KEY_GOSPEL_PASSAGES = {
    "John": {
        1: [1, 14, 29],  # Prologue, Word became flesh, Behold the Lamb
        3: [3, 5, 16],   # Born again, Spirit, For God so loved
        4: [24],         # God is Spirit
        6: [35, 48, 51], # I am the bread of life
        8: [12, 32, 58], # Light of the world, Draw all men, Before Abraham was
        10: [11, 14],    # Good shepherd
        11: [25, 35],    # I am the resurrection, Jesus wept
        13: [34],        # New commandment
        14: [6, 15, 16, 26, 27],  # The way, if you love me, Helper, teach you, peace
        15: [5, 13],     # Vine and branches, greater love
        16: [33],        # I have overcome
        17: [3, 17],     # This is eternal life, sanctify
        19: [30],        # It is finished
        20: [28, 31],    # My Lord and my God, that you may believe
    },
    "Matthew": {
        1: [21, 23],     # Jesus saves, Emmanuel
        3: [17],         # This is my beloved Son
        4: [4, 19],      # Man shall not live by bread alone, fishers of men
        5: [3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 16, 17, 44, 48],  # Beatitudes and key teachings
        6: [9, 10, 11, 12, 13, 19, 21, 24, 33],  # Lord's Prayer and teachings
        7: [7, 12, 21],  # Ask seek knock, golden rule, not everyone
        11: [28, 29],    # Come unto me
        16: [16, 18, 24, 26],  # Peter's confession, build my church, deny himself
        18: [3, 20],     # Become like children, where two or three
        22: [37, 38, 39],  # Great commandment
        24: [14, 35, 44],  # Gospel preached, heaven and earth pass, be ready
        26: [26, 28, 39, 41],  # This is my body, blood, not my will, watch and pray
        27: [46],        # My God why have you forsaken me
        28: [18, 19, 20],  # All authority, Great Commission, I am with you
    },
    "Mark": {
        1: [15, 17],     # Repent and believe, fishers of men
        2: [17],         # Not the righteous but sinners
        8: [34, 35, 36, 38],  # Deny himself, lose life to save it
        9: [23, 24],     # All things possible, help my unbelief
        10: [27, 45],    # With God all things possible, ransom for many
        12: [30, 31],    # Great commandment
        16: [15, 16],    # Go into all the world
    },
    "Luke": {
        1: [35, 37, 38, 46, 47],  # Holy Spirit, nothing impossible, Mary's response, Magnificat
        2: [10, 11, 14],  # Good tidings, Savior born, Glory to God
        4: [18, 19],     # Anointed to preach, acceptable year
        6: [27, 28, 31, 36, 37, 38],  # Love enemies, golden rule, merciful, judge not, give
        9: [23, 24],     # Take up cross, lose life to save it
        10: [27],        # Love God and neighbor
        11: [2, 3, 4, 9, 13],  # Our Father, daily bread, forgive, ask seek knock, Holy Spirit
        12: [15, 34, 48],  # Beware covetousness, where treasure is, much given
        15: [7, 10, 18, 20, 24],  # Joy in heaven, prodigal son story
        17: [33],        # Lose life to preserve it
        18: [13, 27],    # God be merciful, impossible with men possible with God
        19: [10],        # Seek and save the lost
        22: [19, 20, 42],  # This is my body, new covenant, not my will
        23: [34, 43, 46],  # Father forgive, paradise, into your hands
        24: [46, 47],    # Suffer and rise, repentance and forgiveness
    }
}

def create_comprehensive_commentary(book: str, chapter: int, verse: int, text: str) -> Dict:
    """
    Create comprehensive commentary structure for a verse.

    This function would ideally call an AI model or theological database
    to generate detailed, scholarly commentary. For now, it provides
    a template structure.
    """
    reference = f"{book} {chapter}:{verse}"

    # This is where you would integrate with Claude API or other
    # theological resources to generate actual commentary
    commentary = {
        "analysis": f"<strong>{text}</strong><br><br>[Comprehensive theological analysis would be generated here, including Greek/Hebrew word studies, theological significance, and doctrinal implications.]",
        "historical_context": "[Detailed historical and cultural background would be provided here, including first-century context, Gospel-specific perspective, and relevant archaeological/historical information.]",
        "application": "",  # Left empty per existing format
        "questions": [
            f"How does {reference} reveal the nature and character of Jesus Christ?",
            f"What does this verse teach about the Gospel message and salvation?",
            f"How should this truth transform the way believers think and live?"
        ]
    }

    return commentary

def generate_gospel_commentary() -> Dict:
    """
    Generate commentary for key Gospel passages.

    Returns a dictionary ready to be merged into verse_commentary.json.
    """
    from kjvstudy_org.kjv import bible

    commentary_dict = {}

    for gospel, chapters in KEY_GOSPEL_PASSAGES.items():
        print(f"\nProcessing {gospel}...")

        for chapter_num, verses in chapters.items():
            print(f"  Chapter {chapter_num}...")

            for verse_num in verses:
                # Get the verse text
                verse_text = bible.get_verse_text(gospel, chapter_num, verse_num)

                if verse_text is None:
                    print(f"    Warning: Could not find {gospel} {chapter_num}:{verse_num}")
                    continue

                reference = f"{gospel} {chapter_num}:{verse_num}"

                # Generate commentary
                commentary = create_comprehensive_commentary(
                    gospel,
                    chapter_num,
                    verse_num,
                    verse_text
                )

                commentary_dict[reference] = commentary
                print(f"    Generated commentary for {reference}")

    return commentary_dict

def save_commentary(commentary: Dict, output_file: str = None):
    """Save commentary to JSON file."""
    if output_file is None:
        output_file = Path(__file__).parent / "gospel_commentary_output.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(commentary, f, indent=2, ensure_ascii=False)

    print(f"\nCommentary saved to {output_file}")
    print(f"Total entries: {len(commentary)}")

def main():
    """Main function to generate and save Gospel commentary."""
    print("=" * 70)
    print("Gospel Commentary Generator")
    print("=" * 70)
    print("\nGenerating commentary for key Gospel passages...")
    print("This focuses on theologically significant verses that can serve")
    print("as templates for comprehensive commentary expansion.\n")

    commentary = generate_gospel_commentary()
    save_commentary(commentary)

    print("\n" + "=" * 70)
    print("Generation complete!")
    print("=" * 70)
    print("\nTo generate full commentary for all 3,779 Gospel verses,")
    print("consider using an AI model with theological training or")
    print("consulting biblical commentaries and theological resources.")

if __name__ == "__main__":
    main()
