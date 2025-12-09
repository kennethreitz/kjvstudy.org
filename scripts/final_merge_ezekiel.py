#!/usr/bin/env python3
"""
Final merge of all Ezekiel commentary
"""

import json
import sys
from pathlib import Path

# Import all batches
sys.path.insert(0, str(Path(__file__).parent))

from generate_ezekiel_commentary import COMMENTARY as batch1
from generate_ezekiel_commentary_batch2 import COMMENTARY_BATCH2 as batch2
from generate_ezekiel_commentary_batch3 import COMMENTARY_BATCH3 as batch3
from generate_ezekiel_commentary_final import COMMENTARY_FINAL as batch4

# Load existing Ezekiel file
ezekiel_path = Path('kjvstudy_org/data/verse_commentary/ezekiel.json')
print(f'Loading {ezekiel_path}...')
with open(ezekiel_path, 'r') as f:
    ezekiel_data = json.load(f)

# Get existing commentary
commentary = ezekiel_data.get('commentary', {})
print(f'Existing chapters: {len(commentary)}')

# Track additions
added_count = 0
skipped_count = 0

# Merge all batches
for batch_name, batch in [('Batch 1', batch1), ('Batch 2', batch2), ('Batch 3', batch3), ('Batch 4', batch4)]:
    print(f'\nProcessing {batch_name}...')
    for chapter, verses in batch.items():
        if chapter not in commentary:
            commentary[chapter] = {}
        for verse, content in verses.items():
            if verse not in commentary[chapter]:
                commentary[chapter][verse] = content
                added_count += 1
                print(f'  Added: Ezekiel {chapter}:{verse}')
            else:
                skipped_count += 1

# Update the data
ezekiel_data['commentary'] = commentary

# Save back
print(f'\nSaving to {ezekiel_path}...')
with open(ezekiel_path, 'w') as f:
    json.dump(ezekiel_data, f, indent=2, ensure_ascii=False)

# Summary
total_verses = sum(len(verses) for verses in commentary.values())
print(f'\n✓ Successfully merged commentary')
print(f'  Added: {added_count} verses')
print(f'  Skipped (already exist): {skipped_count} verses')
print(f'  Total chapters: {len(commentary)}')
print(f'  Total verses: {total_verses}')
