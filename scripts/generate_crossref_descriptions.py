#!/usr/bin/env python3
"""
Generate concise descriptions for cross-references.

For each cross-reference pair, generates a 2-5 word description explaining
the thematic or narrative connection between the verses.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import kjv module
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import bible


def generate_description(from_verse_text, to_verse_text, from_ref, to_ref):
    """
    Generate a 2-5 word description of why two verses are cross-referenced.

    This looks for common themes, keywords, or narrative connections.
    """
    from_lower = from_verse_text.lower()
    to_lower = to_verse_text.lower()

    # Common theological themes and keywords
    theme_keywords = {
        'salvation': ['save', 'salvation', 'saved', 'saviour', 'savior'],
        'faith': ['faith', 'believe', 'believed', 'believing', 'trust'],
        'grace': ['grace', 'gracious', 'mercy', 'merciful'],
        'love': ['love', 'loved', 'loveth', 'charity'],
        'righteousness': ['righteous', 'righteousness', 'just', 'justice'],
        'redemption': ['redeem', 'redeemed', 'redemption', 'ransom'],
        'covenant': ['covenant', 'testament', 'promise', 'promised'],
        'judgment': ['judgment', 'judge', 'judged', 'wrath'],
        'kingdom': ['kingdom', 'king', 'reign'],
        'glory': ['glory', 'glorified', 'glorious'],
        'holy': ['holy', 'holiness', 'sanctified', 'saint'],
        'spirit': ['spirit', 'ghost'],
        'prayer': ['pray', 'prayer', 'prayed'],
        'word': ['word', 'scripture', 'law', 'commandment'],
        'creation': ['create', 'created', 'creation', 'made'],
        'resurrection': ['resurrection', 'risen', 'rise', 'raise'],
        'prophecy': ['prophecy', 'prophesy', 'foretold', 'prophet'],
        'worship': ['worship', 'praise', 'worship'],
        'sin': ['sin', 'sinned', 'transgression', 'iniquity'],
        'repentance': ['repent', 'repented', 'repentance'],
        'eternal life': ['eternal', 'everlasting', 'forever', 'immortal'],
        'cross': ['cross', 'crucified', 'crucify'],
        'blood': ['blood'],
        'sacrifice': ['sacrifice', 'offering', 'altar'],
        'temple': ['temple', 'tabernacle', 'sanctuary'],
        'baptism': ['baptize', 'baptized', 'baptism'],
        'peace': ['peace', 'peaceful'],
        'hope': ['hope'],
        'witness': ['witness', 'testify', 'testimony'],
        'truth': ['truth', 'true'],
        'light': ['light'],
        'darkness': ['darkness', 'dark'],
        'evil': ['evil', 'wicked'],
        'good': ['good', 'goodness'],
        'blessing': ['bless', 'blessed', 'blessing'],
        'curse': ['curse', 'cursed'],
    }

    # Find common themes
    common_themes = []
    for theme, keywords in theme_keywords.items():
        from_has = any(kw in from_lower for kw in keywords)
        to_has = any(kw in to_lower for kw in keywords)
        if from_has and to_has:
            common_themes.append(theme)

    if common_themes:
        # Use the first common theme
        return common_themes[0].title()

    # Check for narrative connections (same person/place)
    names = ['jesus', 'christ', 'god', 'lord', 'moses', 'david', 'abraham',
             'paul', 'peter', 'john', 'israel', 'jerusalem', 'egypt', 'babylon']
    for name in names:
        if name in from_lower and name in to_lower:
            return f"References {name.title()}"

    # Default: parallel teaching
    return "Parallel theme"


def add_descriptions_to_crossrefs(sample_size=None):
    """Add descriptions to cross-references"""

    crossref_file = Path("kjvstudy_org/data/cross_references.json")

    print("Loading cross-references...")
    with open(crossref_file, 'r') as f:
        crossrefs = json.load(f)

    total_refs = sum(len(refs) for refs in crossrefs.values())
    print(f"Total cross-reference entries: {total_refs:,}")

    if sample_size:
        print(f"\nProcessing sample of {sample_size} verses...")
    else:
        print(f"\nProcessing all {len(crossrefs):,} verses...")

    processed = 0
    updated = 0

    for verse_key, refs in list(crossrefs.items())[:sample_size] if sample_size else crossrefs.items():
        # Parse verse key: "Book:Chapter:Verse"
        parts = verse_key.split(':')
        if len(parts) != 3:
            continue

        from_book, from_chapter, from_verse = parts[0], int(parts[1]), int(parts[2])

        # Get the source verse text
        from_text = bible.get_verse_text(from_book, from_chapter, from_verse)
        if not from_text:
            continue

        # Process each cross-reference
        for ref in refs:
            # Skip if already has a description
            if ref.get('note') and ref['note'].strip():
                continue

            # Parse reference: "Book Chapter:Verse"
            ref_str = ref['ref']
            try:
                ref_parts = ref_str.rsplit(' ', 1)
                if len(ref_parts) != 2:
                    continue

                to_book = ref_parts[0]
                chapter_verse = ref_parts[1].split(':')
                if len(chapter_verse) != 2:
                    continue

                to_chapter, to_verse = int(chapter_verse[0]), int(chapter_verse[1])

                # Get the target verse text
                to_text = bible.get_verse_text(to_book, to_chapter, to_verse)
                if not to_text:
                    continue

                # Generate description
                description = generate_description(from_text, to_text, verse_key, ref_str)
                ref['note'] = description
                updated += 1

            except (ValueError, IndexError) as e:
                continue

        processed += 1
        if processed % 100 == 0:
            print(f"Processed {processed:,} verses, updated {updated:,} cross-references...")

    print(f"\n✅ Updated {updated:,} cross-reference descriptions")

    # Save updated cross-references
    print(f"Saving to {crossref_file}...")
    with open(crossref_file, 'w') as f:
        json.dump(crossrefs, f, indent=2, ensure_ascii=False)

    print("✅ Done!")

    # Show sample
    print("\nSample cross-references with descriptions:")
    print("-" * 80)
    for verse_key in list(crossrefs.keys())[:3]:
        print(f"\n{verse_key}:")
        for ref in crossrefs[verse_key][:3]:
            print(f"  → {ref['ref']}: {ref['note']}")


if __name__ == "__main__":
    # Process a sample first to test
    # add_descriptions_to_crossrefs(sample_size=10)

    # Or process everything (will take a while!)
    add_descriptions_to_crossrefs()
