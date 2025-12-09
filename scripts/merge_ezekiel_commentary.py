#!/usr/bin/env python3
"""
Merge all generated Ezekiel commentary into the existing file
"""

import json
from pathlib import Path

# Load existing Ezekiel commentary
ezekiel_path = Path('kjvstudy_org/data/verse_commentary/ezekiel.json')
with open(ezekiel_path, 'r') as f:
    ezekiel_data = json.load(f)

# Import all commentary batches
from generate_ezekiel_commentary import COMMENTARY as batch1
from generate_ezekiel_commentary_batch2 import COMMENTARY_BATCH2 as batch2
from generate_ezekiel_commentary_batch3 import COMMENTARY_BATCH3 as batch3
from generate_ezekiel_commentary_final import COMMENTARY_FINAL as batch4

# Merge all batches
all_new_commentary = {}
for batch in [batch1, batch2, batch3, batch4]:
    for chapter, verses in batch.items():
        if chapter not in all_new_commentary:
            all_new_commentary[chapter] = {}
        all_new_commentary[chapter].update(verses)

# Merge into existing commentary
commentary = ezekiel_data.get('commentary', {})
for chapter, verses in all_new_commentary.items():
    if chapter not in commentary:
        commentary[chapter] = {}
    for verse, content in verses.items():
        if verse not in commentary[chapter]:
            commentary[chapter][verse] = content
            print(f"Added: Ezekiel {chapter}:{verse}")
        else:
            print(f"Skipped (already exists): Ezekiel {chapter}:{verse}")

# Update the data
ezekiel_data['commentary'] = commentary

# Save back to file
with open(ezekiel_path, 'w') as f:
    json.dump(ezekiel_data, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully merged commentary into {ezekiel_path}")
print(f"Total chapters in commentary: {len(commentary)}")

# Count total verses
total_verses = sum(len(verses) for verses in commentary.values())
print(f"Total verses with commentary: {total_verses}")
