#!/usr/bin/env python3
"""Get verse text for a list of references."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.kjv import Bible

# Missing Acts verses
refs = [
    (14, 28), (17, 33), (17, 34), (19, 36), (19, 37), (19, 38), (19, 39), (19, 40), (19, 41),
    (22, 25), (22, 26), (22, 27), (22, 28), (22, 29), (22, 30),
    (25, 17), (25, 18), (25, 19), (25, 20), (25, 21), (25, 22), (25, 23), (25, 24), (25, 25), (25, 26), (25, 27),
    (26, 30), (26, 31), (26, 32),
    (27, 43), (27, 44),
    (28, 29), (28, 30), (28, 31)
]

bible = Bible()

for ch, v in refs:
    text = bible.get_verse_text("Acts", ch, v)
    print(f"Acts {ch}:{v}")
    print(f"  {text}")
    print()
