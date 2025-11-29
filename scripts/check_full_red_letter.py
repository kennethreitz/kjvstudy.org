#!/usr/bin/env python3
"""Check for verses marked as 'full' that contain narrative introductions."""

import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import get_verse

# Load red letter data
data_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "red_letter_verses.json"
with open(data_path) as f:
    data = json.load(f)

# Common narrative patterns that indicate the verse has narrative before Jesus speaks
narrative_patterns = [
    "And he answered and said",
    "And Jesus answered and said",
    "And he said unto them",
    "And Jesus said unto them",
    "Then said he",
    "Then Jesus said",
    "And he saith unto them",
    "And Jesus saith unto them",
    "Then saith he",
    "Then Jesus saith",
    "And he spake",
    "And Jesus spake",
]

# Check verses marked as "full"
issues = []
for ref, value in data['verses'].items():
    if value == 'full':
        # Parse reference
        parts = ref.rsplit(' ', 1)
        if len(parts) == 2:
            book = parts[0]
            chapter_verse = parts[1].split(':')
            if len(chapter_verse) == 2:
                chapter = int(chapter_verse[0])
                verse = int(chapter_verse[1])
                
                # Get the actual verse text
                verse_data = get_verse(book, chapter, verse)
                if verse_data:
                    text = verse_data['text']
                    
                    # Check if it starts with narrative
                    for pattern in narrative_patterns:
                        if text.startswith(pattern):
                            issues.append({
                                'ref': ref,
                                'text': text,
                                'pattern': pattern
                            })
                            break

print(f"Found {len(issues)} verses marked as 'full' that start with narrative:")
print()

for issue in issues[:30]:  # Show first 30
    print(f"{issue['ref']}:")
    print(f"  Pattern: {issue['pattern']}")
    print(f"  Text: {issue['text'][:120]}...")
    print()
