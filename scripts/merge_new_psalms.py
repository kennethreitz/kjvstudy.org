#!/usr/bin/env python3
"""Merge newly generated Psalms commentary into the correct file."""

import json
from pathlib import Path

# Read the incorrectly placed commentary
with open('verse_commentary.json') as f:
    new_data = json.load(f)

# Read the actual psalms.json file
psalms_file = Path('kjvstudy_org/data/verse_commentary/psalms.json')
with open(psalms_file) as f:
    psalms_data = json.load(f)

# Merge the new chapters (95, 96, 98, 110, 145-150)
new_chapters = ['95', '96', '98', '110', '145', '146', '147', '148', '149', '150']
added = []

for chapter in new_chapters:
    if chapter in new_data['commentary']:
        psalms_data['commentary'][chapter] = new_data['commentary'][chapter]
        added.append(chapter)
        print(f'✓ Added Psalm {chapter}')

# Write back to the correct file
with open(psalms_file, 'w', encoding='utf-8') as f:
    json.dump(psalms_data, f, ensure_ascii=False, indent=2)

print(f'\nMerged {len(added)} chapters: {", ".join(added)}')
