#!/usr/bin/env python3
"""Get verse texts for missing commentary."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kjvstudy_org.kjv import Bible

bible = Bible()

# Amos missing verses
amos_refs = [
    "1:14", "1:15", "2:15", "2:16", "3:8", "3:9", "3:10", "3:11", "3:12", "3:13", "3:14", "3:15",
    "4:13", "5:25", "5:26", "5:27", "6:2", "6:3", "6:4", "6:5", "6:6", "6:7", "6:8", "6:9",
    "6:10", "6:11", "6:12", "6:13", "6:14", "7:15", "7:16", "7:17", "8:12", "8:13", "8:14",
    "9:14", "9:15"
]

# John missing verses
john_refs = [
    "8:59", "10:31", "10:32", "10:33", "10:34", "10:35", "10:36", "10:37", "10:38", "10:39",
    "10:40", "10:41", "10:42", "13:38", "14:28", "14:29", "14:30", "14:31", "15:27", "17:22",
    "17:23", "17:24", "17:25", "17:26", "19:31", "19:32", "19:33", "19:34", "19:35", "19:36",
    "19:37", "19:38", "19:39", "19:40", "19:41", "19:42"
]

print("=== AMOS VERSES ===\n")
for ref in amos_refs:
    ch, v = ref.split(":")
    text = bible.get_verse_text("Amos", int(ch), int(v))
    print(f"Amos {ref}: {text}\n")

print("\n\n=== JOHN VERSES ===\n")
for ref in john_refs:
    ch, v = ref.split(":")
    text = bible.get_verse_text("John", int(ch), int(v))
    print(f"John {ref}: {text}\n")
