#!/usr/bin/env python3
"""Fix Psalm 115:13 - add missing historical field."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

psalms_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "psalms.json"

with open(psalms_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add historical field to Psalm 115:13
data["commentary"]["115"]["13"]["historical"] = (
    "Psalm 115 was likely written during or after the Babylonian exile, when Israel faced "
    "mockery from surrounding nations who questioned the power of their invisible God compared "
    "to pagan idols. The psalm's emphasis on God's sovereignty and the futility of idolatry "
    "would have provided crucial encouragement to a displaced people.<br><br>"
    "The phrase \"both small and great\" reflects ancient Near Eastern social stratification. "
    "Israel was a highly stratified society: kings, priests, nobles, landowners, farmers, servants, "
    "and slaves occupied distinct social tiers. Yet God's blessing transcends these human distinctions. "
    "This radical equality before God challenged prevailing social norms where blessings and favor "
    "typically correlated with status and power.<br><br>"
    "The \"fear of the LORD\" was central to Old Testament piety. It appears over 300 times in Scripture. "
    "For ancient Israelites, this fear shaped ethical behavior, worship practices, and daily decisions. "
    "The book of Deuteronomy repeatedly commands Israel to fear God (Deuteronomy 6:13, 10:12), connecting "
    "this fear with covenant obedience. Job is described as one who \"feared God and eschewed evil\" (Job 1:1). "
    "The wisdom tradition declares: \"The fear of the LORD is the beginning of knowledge\" (Proverbs 1:7)."
)

with open(psalms_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Fixed Psalm 115:13 - added historical field")
