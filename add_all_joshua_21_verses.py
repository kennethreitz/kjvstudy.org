#!/usr/bin/env python3
"""Add complete commentary for Joshua 21:25-42"""

import json

# Define all the commentary data
COMMENTARY_DATA = """
{
  "25": {
    "analysis": "<strong>And out of the half tribe of Manasseh, Tanach with her suburbs, and Gath-rimmon with her suburbs; two cities.</strong><br><br>These final two cities complete the Kohathite allocation from the non-priestly Levites. The Hebrew <em>migrash</em> (מִגְרָשׁ, \\"suburbs\\") refers to the pasture lands extending outward from each city, essential for Levitical livestock. Tanach (also spelled Taanach) was strategically positioned near Megiddo in the Jezreel Valley, controlling vital trade routes. Archaeological excavations at Tell Ta'annek have uncovered Late Bronze Age destruction layers and Iron Age I resettlement, consistent with Israelite conquest and Levitical occupation.<br><br>Gath-rimmon appears twice in Joshua 21—here in Manasseh's territory and in verse 24 from Dan. This has led to textual questions, with some scholars suggesting scribal duplication or identifying two different cities with the same name. The parallel passage in 1 Chronicles 6:70 lists Bileam instead of Gath-rimmon for Manasseh's allocation, likely referring to the same location (Bileam being another name for Ibleam). Such textual variations remind us that ancient place names could change and cities could be known by multiple designations.<br><br>The precision \\"two cities\\" maintains the careful accounting throughout this chapter. God's promises are specific and measurable—not vague spiritual sentiments but concrete geographical realities. The Kohathites' total allocation (verse 26) was ten cities, demonstrating God's equitable provision for each Levitical family according to their size and needs.",
    "historical": "Tanach (modern Tell Ta'annek) guarded the southern approach to the Jezreel Valley, one of ancient Israel's most strategic military corridors. Judges 5:19 mentions Tanach as the site where Deborah and Barak defeated Sisera's coalition. The city's assignment to Levites placed covenant-faithful teachers at this critical junction where Israel faced constant pressure from Canaanite and foreign powers. Levitical presence in such strategic locations wasn't coincidental—it positioned God's law-keepers where cultural and military tensions were highest.<br><br>The Jezreel Valley served as ancient Israel's breadbasket, providing rich agricultural land. Levites stationed here would have access to abundant tithes from prosperous farming communities. Yet this fertility also attracted pagan worship—Baal cults focused on agricultural fertility, making Levitical teaching about Yahweh as provider of rain and harvest particularly crucial in this region.",
    "questions": [
      "How does God's placement of faithful teachers at strategic cultural crossroads challenge you to engage rather than withdraw from contested spaces?",
      "What does the specificity of Levitical city assignments teach about God's attention to practical details in kingdom work?",
      "How should the Levites' economic dependence on God's provision through tithes inform modern church funding and ministerial support?"
    ]
  }
}
"""

# Read the existing file
print("Reading Joshua commentary file...")
with open('kjvstudy_org/data/verse_commentary/joshua.json', 'r') as f:
    data = json.load(f)

# Parse the commentary data (just verse 25 for now to test)
test_data = json.loads(COMMENTARY_DATA)

# Add to the main data
print(f"Adding {len(test_data)} verses to chapter 21...")
for verse_num, commentary in test_data.items():
    data['commentary']['21'][verse_num] = commentary
    print(f"  Added verse {verse_num}")

# Save the file
print("Saving updated file...")
with open('kjvstudy_org/data/verse_commentary/joshua.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nSuccess! Added verses to Joshua chapter 21")
