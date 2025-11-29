#!/usr/bin/env python3
"""Script to add verse commentary to the JSON file."""

import json
from pathlib import Path

# New commentaries to add
new_commentaries = {
    "Proverbs": {
        "4": {
            "22": {
                "analysis": "<strong>For they are life unto those that find them, and health to all their flesh.</strong> This verse refers to the words of wisdom from the preceding verses. The Hebrew word for \"life\" (<em>chayim</em>, חַיִּים) signifies not merely physical existence but abundant, flourishing vitality—the fullness of life that comes from walking in God's truth. The parallelism with \"health\" (<em>marpe</em>, מַרְפֵּא, meaning healing or remedy) emphasizes both spiritual and physical wholeness.<br><br>\"Those that find them\" uses the Hebrew <em>matsa</em> (מָצָא), suggesting active, diligent seeking rather than passive reception. Wisdom must be pursued and discovered through earnest effort. \"To all their flesh\" (<em>basar</em>, בָּשָׂר) indicates comprehensive benefit—wisdom affects the whole person, body and soul.<br><br>This verse presents wisdom as medicine for the soul and body alike. Just as physical medicine brings healing to diseased flesh, God's wisdom brings restoration to our entire being. The imagery anticipates Christ, who is the wisdom of God personified (1 Corinthians 1:24, 30) and who brings both spiritual life and promises bodily resurrection. Proverbs consistently presents wisdom as the path to life, while folly leads to death—a theme culminating in Jesus' declaration, \"I am the way, the truth, and the life\" (John 14:6).",
                "historical": "Proverbs 4 is part of Solomon's instruction to his son, reflecting the ancient Near Eastern wisdom tradition where fathers passed down life principles to their children. Written around 950 BC, this collection of wisdom would have been crucial for training young Israelites in covenant faithfulness during the United Monarchy period.<br><br>Ancient Israel understood health holistically—physical wellness was inseparable from spiritual obedience. Medical knowledge was limited, so the emphasis on wisdom as \"health to all their flesh\" would have resonated deeply. The Deuteronomic covenant promised physical blessings for obedience (Deuteronomy 28:1-14), and wisdom literature like Proverbs showed the practical path to such blessing.<br><br>In the ancient world, wisdom literature served pedagogical purposes in royal courts and family settings. Young men being prepared for leadership roles would memorize and meditate on these teachings. The promise of life and health through wisdom stood in stark contrast to the futility of idolatry and the death-dealing consequences of sin that surrounded Israel among pagan nations.",
                "questions": [
                    "What specific wisdom from Scripture do you need to 'find' and apply for spiritual and physical health?",
                    "How does viewing God's Word as life-giving medicine change your approach to Bible study?",
                    "In what areas of life have you experienced the life and health that come from walking in wisdom?",
                    "How can you cultivate a more diligent pursuit of wisdom in your daily routine?",
                    "What connection do you see between spiritual health and physical wellness in your own experience?"
                ]
            }
        }
    }
}

def main():
    commentary_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary.json"

    # Read existing commentary
    with open(commentary_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    # Merge new commentaries
    for book, chapters in new_commentaries.items():
        if book not in existing_data:
            existing_data[book] = {}

        for chapter, verses in chapters.items():
            if chapter not in existing_data[book]:
                existing_data[book][chapter] = {}

            for verse, commentary in verses.items():
                existing_data[book][chapter][verse] = commentary

    # Write back to file
    with open(commentary_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print("Successfully added commentary")

if __name__ == "__main__":
    main()
