#!/usr/bin/env python3
"""Get verse texts for missing Joshua verses."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.kjv import Bible

bible = Bible()

MISSING = [
    (17, 16), (17, 17), (17, 18),
    (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10),
    (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17),
    (18, 18), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (18, 24),
    (18, 25), (18, 26), (18, 27), (18, 28),
    (19, 37), (19, 38), (19, 39), (19, 40), (19, 41), (19, 42), (19, 43),
    (19, 44), (19, 45), (19, 46), (19, 47), (19, 48), (19, 49), (19, 50),
    (19, 51),
    (20, 4), (20, 5), (20, 6), (20, 7), (20, 8), (20, 9),
    (22, 31), (22, 32), (22, 33), (22, 34),
    (24, 25), (24, 26), (24, 27), (24, 28), (24, 29), (24, 30), (24, 31),
    (24, 32), (24, 33)
]

verses = {}
for chapter, verse in MISSING:
    text = bible.get_verse_text("Joshua", chapter, verse)
    key = f"{chapter}:{verse}"
    verses[key] = text

print(json.dumps(verses, indent=2))
