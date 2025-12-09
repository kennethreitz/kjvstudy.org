#!/usr/bin/env python3
"""Add missing Amos commentary."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

filepath = DATA_DIR / "amos.json"
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

commentary = data.get("commentary", {})

# Add new entries - Part 1: Chapters 1-3
new_entries = {
    "1": {
        "14": {
            "analysis": "<strong>I will kindle a fire in the wall of Rabbah</strong> (אַצִּית אֵשׁ בְּחוֹמַת רַבָּה, <em>atsit esh b'chomat rabbah</em>)—God's judgment comes as consuming fire against Ammon's capital. The Hebrew אַצִּית (<em>atsit</em>, 'I will kindle') emphasizes divine agency; this is not merely human warfare but Yahweh's direct intervention. <strong>With shouting in the day of battle, with a tempest in the day of the whirlwind</strong> combines military siege (תְּרוּעָה, <em>teruah</em>, the war cry) with natural disaster imagery—God orchestrates both human armies and cosmic forces for judgment.<br><br>Rabbah (modern Amman, Jordan) represented Ammonite pride and military power. The 'palaces' (אַרְמְנוֹתֶיהָ, <em>armenoteha</em>) symbolize accumulated wealth gained through oppression. This prophecy was fulfilled when Nebuchadnezzar conquered Ammon in 582 BC, though Christ ultimately judges all nations at His return (Matthew 25:31-46).",
            "historical": "Amos prophesied around 760-750 BC during Jeroboam II's reign. Ammon, descended from Lot (Genesis 19:38), had longstanding enmity with Israel. They committed atrocities against Gilead (Amos 1:13), including ripping open pregnant women to expand territory—crimes that demanded divine retribution.",
            "questions": [
                "How does God's sovereignty over nations challenge modern nationalism and the belief that any country is beyond judgment?",
                "What 'palaces' of accumulated wealth in your life might represent injustice or oppression of others?",
                "How should the certainty of divine judgment against evil comfort those who suffer injustice today?"
            ]
        },
        "15": {
            "analysis": "<strong>Their king shall go into captivity, he and his princes together</strong> (וְהָלַךְ מַלְכָּם בַּגּוֹלָה, <em>v'halach malkam bagolah</em>)—The Hebrew מַלְכָּם (<em>malkam</em>) is a wordplay: it means both 'their king' and references Molech/Milcom, the Ammonite deity to whom children were sacrificed (1 Kings 11:5, 33). Both human rulers and false gods prove powerless before Yahweh. <strong>Saith the LORD</strong> (אָמַר יְהוָה, <em>amar YHWH</em>) is the prophetic authentication formula—this is not Amos's opinion but God's irrevocable decree.<br><br>The collapse of both political and religious systems signifies total judgment. No refuge remains—not in military might, political alliances, or false worship. This pattern repeats throughout history when nations trust in anything besides the true God.",
            "historical": "The Babylonian exile fulfilled this prophecy. Archaeological evidence shows Rabbah was destroyed in the 6th century BC. Ironically, Ammonites had long practiced child sacrifice to Molech, and now their god and king both went into captivity—helpless before the covenant God of Israel.",
            "questions": [
                "What false 'kings' or authorities do people trust in today instead of the LORD—government, wealth, ideology, self?",
                "How does the exile of both human rulers and false gods demonstrate that all idolatry ends in captivity?",
                "In what ways might Christians today be trusting in political power rather than the kingdom of God?"
            ]
        }
    },
    "2": {
        "15": {
            "analysis": "In this verse detailing Moab's coming judgment, three classes of warriors prove helpless: <strong>he that handleth the bow</strong> (תֹּפֵשׂ הַקֶּשֶׁת, <em>tofes haqeshet</em>, the archer), <strong>he that is swift of foot</strong> (קַל בְּרַגְלָיו, <em>qal b'raglav</em>, literally 'light in his feet'), and <strong>he that rideth the horse</strong> (רֹכֵב הַסּוּס, <em>rochev hasus</em>, the cavalry). The threefold repetition—'shall not deliver himself' (לֹא יְמַלֵּט, <em>lo yemalet</em>)—hammers home human inability to escape divine judgment.<br><br>Ancient warfare relied on these three military advantages: long-range attack (archers), speed (runners for messages and retreat), and mobile power (cavalry). Yet when God judges, no human strategy suffices. This prefigures Romans 8:33—when God justifies, who can condemn? Conversely, when God condemns, no created thing can deliver (Romans 8:38-39).",
            "historical": "Moab, descended from Lot (Genesis 19:37), occupied territory east of the Dead Sea. They possessed skilled archers and swift-footed messengers. This prophecy found fulfillment in multiple invasions: by Assyria (715 BC), Babylon (582 BC), and finally Arab conquest that erased Moabite identity entirely.",
            "questions": [
                "What modern 'advantages'—technology, wealth, intelligence—do people trust for security instead of God?",
                "How does the futility of military might in escaping judgment challenge nations that trust in weapons?",
                "If no one can flee from God's judgment, what makes the gospel offer of escape through Christ so extraordinary?"
            ]
        },
        "16": {
            "analysis": "<strong>He that is courageous among the mighty shall flee away naked in that day</strong> (וְאַמִּיץ לִבּוֹ בַגִּבּוֹרִים עָרוֹם יָנוּס, <em>v'amitz libo bagiborim arom yanus</em>)—The Hebrew emphasizes irony: אַמִּיץ (<em>amitz</em>) means 'strong, courageous,' yet even the bravest warrior flees עָרוֹם (<em>arom</em>, 'naked, stripped of armor'). The stripping represents complete defeat and humiliation; ancient warriors viewed losing armor as disgrace worse than death. <strong>Saith the LORD</strong> seals this as prophetic certainty, not military speculation.<br><br>This reversal motif appears throughout Scripture: the proud brought low (Isaiah 2:11-17), the mighty made weak (1 Corinthians 1:27-29). Human courage crumbles before divine judgment—no bravado, ideology, or self-confidence can stand when God rises to judge. Only those covered in Christ's righteousness (Isaiah 61:10) have a covering that endures judgment.",
            "historical": "Moabite warriors were renowned for courage (2 Kings 3:26-27 records their desperation in battle). Yet Nebuchadnezzar's armies stripped them of both armor and land. The 'nakedness' fulfills the covenant curses of Deuteronomy 28:48—Israel's judgment falling on nations who opposed God's purposes.",
            "questions": [
                "What does it mean to face judgment 'naked'—without the covering of Christ's righteousness?",
                "How does this verse challenge cultures that glorify human courage and strength as ultimate values?",
                "In what areas of life are you trusting your own 'courage' rather than seeking refuge in God?"
            ]
        }
    }
}

# Merge new entries
for chapter, verses in new_entries.items():
    if chapter not in commentary:
        commentary[chapter] = {}
    for verse, entry in verses.items():
        if verse not in commentary[chapter]:
            commentary[chapter][verse] = entry
            print(f"Added Amos {chapter}:{verse}")

data["commentary"] = commentary

# Save
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to {filepath}")
