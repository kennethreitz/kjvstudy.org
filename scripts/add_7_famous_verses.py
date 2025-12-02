#!/usr/bin/env python3
"""Add 7 missing famous verses to psalms.json"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries

# Just the 7 verses we need to add
new_commentaries = {
    "Psalms": {
        # Get the content from the other script
    }
}

# Read the content from add_famous_verses.py
with open(Path(__file__).parent / "add_famous_verses.py") as f:
    script = f.read()

# Extract just the new_commentary dict content
import re
match = re.search(r'new_commentary = ({.*?})\s+# Load existing', script, re.DOTALL)
if match:
    new_comm_str = match.group(1)
    new_comm = eval(new_comm_str)
    new_commentaries["Psalms"] = new_comm

# Use the proper merge function
merge_commentary_entries(new_commentaries)
print("✓ Added 7 famous verses")
