#!/usr/bin/env python3
"""Merge famous verses into correct psalms.json file."""

import json
from pathlib import Path

# Read the verse_commentary.json with new verses
with open('verse_commentary.json') as f:
    new_data = json.load(f)

# Read the actual psalms.json file
psalms_file = Path('kjvstudy_org/data/verse_commentary/psalms.json')
with open(psalms_file) as f:
    psalms_data = json.load(f)

# Verses to merge
verses_to_add = [
    ('1', '1'),
    ('22', '1'),
    ('23', '6'),
    ('46', '10'),
    ('91', '11'),
    ('103', '1'),
    ('139', '23')
]

added = []
for chapter, verse in verses_to_add:
    if chapter in new_data['commentary'] and verse in new_data['commentary'][chapter]:
        if chapter not in psalms_data['commentary']:
            psalms_data['commentary'][chapter] = {}
        psalms_data['commentary'][chapter][verse] = new_data['commentary'][chapter][verse]
        added.append(f'{chapter}:{verse}')
        print(f'✓ Added Psalm {chapter}:{verse}')

# Write back to the correct file
with open(psalms_file, 'w', encoding='utf-8') as f:
    json.dump(psalms_data, f, ensure_ascii=False, indent=2)

print(f'\nMerged {len(added)} verses: {", ".join(added)}')
