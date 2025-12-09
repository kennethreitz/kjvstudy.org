#!/usr/bin/env python3
"""
Final merge script for Zechariah commentary.
This will merge all new commentary into the existing file.
"""

import json
import sys

# Load existing commentary
with open('/Users/kennethreitz/repos/kjvstudy.org/kjvstudy_org/data/verse_commentary/zechariah.json', 'r') as f:
    zechariah_data = json.load(f)

# Load the new commentary we've generated
with open('/Users/kennethreitz/repos/kjvstudy.org/zechariah_new_commentary.json', 'r') as f:
    new_commentary = json.load(f)

# Merge new commentary into existing
for chapter_num, verses in new_commentary.items():
    if chapter_num not in zechariah_data['commentary']:
        zechariah_data['commentary'][chapter_num] = {}
   
    for verse_num, content in verses.items():
        if verse_num not in zechariah_data['commentary'][chapter_num]:
            zechariah_data['commentary'][chapter_num][verse_num] = content
            print(f'Added {chapter_num}:{verse_num}')
        else:
            print(f'Skipped {chapter_num}:{verse_num} (already exists)')

#Save back to file
with open('/Users/kennethreitz/repos/kjvstudy.org/kjvstudy_org/data/verse_commentary/zechariah.json', 'w') as f:
    json.dump(zechariah_data, f, indent=2, ensure_ascii=False)

print('\nMerge complete!')
print(f'Total verses now: {sum(len(zechariah_data["commentary"][ch]) for ch in zechariah_data["commentary"])}')
