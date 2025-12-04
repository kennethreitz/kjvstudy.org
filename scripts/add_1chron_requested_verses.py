#!/usr/bin/env python3
"""Generate commentary for 20 specific verses from 1 Chronicles."""

import json
from pathlib import Path

# Generate commentary for each verse
COMMENTARY = {
    "16": {
        "33": {
            "analysis": "<strong>Then shall the trees of the wood sing out at the presence of the LORD</strong>—This poetic personification climaxes David's psalm celebrating the ark's arrival in Jerusalem (Ps 96:12-13). The Hebrew <em>ranan</em> (רָנַן) means to cry out in jubilation, the same word used for Israel's shout at the Red Sea.<br><br><strong>Because he cometh to judge the earth</strong> (כִּי־בָא לִשְׁפּוֹט). The verb <em>shaphat</em> means both 'to judge' and 'to rule/govern.' Creation itself responds to Yahweh's universal kingship—a theme Peter applies to the final judgment (2 Pet 3:10-13) when all creation will be renewed under Christ's righteous reign.",
            "historical": "Written during the post-exilic period (likely 450-400 BC), the Chronicler reinterprets David's psalm for returnees rebuilding temple worship. The original context was Israel's golden age under David, but the application looks forward to God's ultimate restoration and judgment.",
            "questions": [
                "How does creation's response to God's presence challenge your own worship—is your praise as spontaneous and wholehearted as nature's?",
                "What does it mean that judgment is presented as good news that makes creation rejoice rather than a threat to fear?"
            ]
        },
        "43": {
            "analysis": "<strong>And David returned to bless his house</strong> (וַיָּשָׁב דָּוִיד לְבָרֵךְ אֶת־בֵּיתוֹ). After orchestrating national worship, David fulfilled his priestly role as household head. The verb <em>barak</em> (בָּרַךְ, 'to bless') means to invoke God's favor and instruct in covenant faithfulness.<br><br>This verse provides crucial balance—public worship doesn't substitute for family discipleship. The contrast with Michal's contempt (2 Sam 6:20) is omitted by Chronicles, emphasizing instead the proper order: God's house first, then our own households under His blessing. As family priest, David models Deuteronomy 6:6-7's command to teach children diligently.",
            "historical": "Chronicles presents an idealized David, omitting his moral failures to focus on his role establishing proper worship. Written for post-exilic families rebuilding community life, this verse emphasizes that worship in God's house must flow into family devotion.",
            "questions": [
                "Do you prioritize corporate worship while neglecting spiritual leadership in your own household, or vice versa?",
                "How can you practically 'bless your house' by leading family members in worship and biblical instruction?"
            ]
        }
    },
    "17": {
        "10": {
            "analysis": "<strong>Furthermore I tell thee that the LORD will build thee an house</strong>—The Hebrew wordplay is stunning: David wanted to build Yahweh a <em>bayit</em> (בַּיִת, temple/house), but God reverses it: <em>bayit</em> for David means dynasty/lineage. This is the Davidic Covenant, foundational to all messianic expectation.<br><br><strong>I will subdue all thine enemies</strong> (וְהִכְנַעְתִּי אֶת־כָּל־אֹיְבֶיךָ). The verb <em>hakhna</em> means to humble or subjugate completely. God alone establishes His kingdom—human effort can't build what only divine grace constructs. Paul echoes this in 1 Cor 15:25, where Christ 'must reign till he hath put all enemies under his feet.'",
            "historical": "This covenant (parallel to 2 Sam 7) was given c. 1000 BC after David captured Jerusalem and brought the ark. It became Israel's constitutional doctrine of kingship, promising an eternal throne—fulfilled ultimately in Christ's resurrection and eternal reign (Luke 1:32-33).",
            "questions": [
                "When have you tried to 'build God a house' through your own efforts, only to discover He wanted to build something in you instead?",
                "How does God's promise to 'subdue all enemies' for David foreshadow Christ's victory over sin, death, and Satan for you?"
            ]
        },
        "20": {
            "analysis": "<strong>O LORD, there is none like thee, neither is there any God beside thee</strong>—David's doxological response to the covenant proclaims radical monotheism. The Hebrew <em>ein kamokha</em> (אֵין כָּמוֹךָ, 'there is none like you') and <em>ein elohim zulatekha</em> (אֵין אֱלֹהִים זוּלָתֶךָ, 'no God besides you') echo Deuteronomy 4:35's foundational creed.<br><br><strong>According to all that we have heard with our ears</strong>—True theology rests on revelation, not speculation. David's worship flows from salvation history: exodus, conquest, covenant. This is covenantal epistemology—we know God through His saving acts and self-disclosure in Scripture.",
            "historical": "Written during an era of rampant polytheism (Canaanite Baalism, later Assyrian and Babylonian pantheons), this confession anchors Israel's identity in Yahweh's incomparability. For post-exilic readers tempted by Persian religious syncretism, it reaffirms exclusive worship.",
            "questions": [
                "How does your practical life (calendar, budget, anxieties) demonstrate whether you truly believe 'there is no God beside' the Lord?",
                "What specific acts of God in history ('heard with our ears') form the foundation of your worship and theology?"
            ]
        }
    },
    "18": {
        "3": {
            "analysis": "<strong>David smote Hadarezer king of Zobah unto Hamath, as he went to stablish his dominion by the river Euphrates</strong>—This military campaign fulfilled God's land promises to Abraham (Gen 15:18: 'from the river of Egypt to...Euphrates'). The Hebrew <em>natsav yad</em> (נַצֵּב יָד, 'to establish dominion') literally means 'to set up a monument/hand,' indicating territorial sovereignty markers.<br><br>Hadarezer's defeat subdued Aram (Syria), Israel's northern threat. Chronicles emphasizes that Davidic empire reached its God-ordained borders, making Solomon's reign the realization of rest promised in Deut 12:9-10. This prefigures Christ's kingdom extending to earth's ends (Ps 72:8).",
            "historical": "David's wars (c. 995-985 BC) secured Israel's greatest territorial extent. Zobah was an Aramean kingdom north of Damascus; Hamath lay further north on the Orontes River. These victories made Israel the dominant Levantine power, fulfilling covenant promises and creating conditions for temple construction.",
            "questions": [
                "How do David's military victories as God's anointed king foreshadow Christ's spiritual conquest over sin's dominion and Satan's kingdom?",
                "What 'Euphrates moments' in your life show God fulfilling promises beyond your own ability to accomplish them?"
            ]
        },
        "13": {
            "analysis": "<strong>Thus the LORD preserved David whithersoever he went</strong> (וַיּוֹשַׁע יְהוָה אֶת־דָּוִיד בְּכֹל אֲשֶׁר הָלָךְ). The verb <em>yasha</em> (יָשַׁע) means 'to save/deliver/preserve'—the same root as 'Jesus' (<em>Yeshua</em>, 'Yahweh saves'). Chronicles attributes all David's success solely to divine preservation.<br><br><strong>All the Edomites became David's servants</strong>—Edom, descended from Esau (Jacob's brother), represents hostile opposition to God's elect. Their subjugation fulfills Isaac's blessing-curse (Gen 27:29, 40) and anticipates Obadiah's prophecy of Edom's judgment. Yet Romans 9:13 shows God's sovereign choice transcends ethnic boundaries.",
            "historical": "Edom controlled the Arabah copper mines and trade routes from Aqaba to Damascus. David's conquest (c. 990 BC) gave Israel critical economic resources and removed a persistent enemy. The placement of garrisons (<em>netsivim</em>) ensured long-term control, enabling Solomon's commercial ventures.",
            "questions": [
                "Where do you need to trust that 'the LORD will preserve you whithersoever you go' rather than relying on your own strength?",
                "How does God's sovereignty in subduing enemies apply to your spiritual battles against besetting sins and Satanic opposition?"
            ]
        }
    },
    "19": {
        "6": {
            "analysis": "<strong>They had made themselves odious to David</strong> (הִבְאִישׁוּ עִם־דָּוִד). The verb <em>ba'ash</em> (בָּאַשׁ) means 'to stink/become repugnant,' used of moral corruption (Gen 34:30). Hanun's humiliation of David's ambassadors (v.4) was covenant treachery demanding response.<br><br><strong>A thousand talents of silver</strong>—approximately 37.5 tons of silver, an astronomical sum demonstrating desperation. Hiring Mesopotamian chariots and Syrian mercenaries shows Ammon mobilizing the entire northern Levant against Israel. Yet money can't purchase security apart from God—a lesson Israel's kings repeatedly ignored (cf. Isa 31:1).",
            "historical": "The Ammonite war (c. 990 BC) followed David's diplomatic overture after Nahash's death. Mesopotamia (Aram-Naharaim) lay between the Tigris and Euphrates; Syria-Maachah was a small Aramean kingdom near Mt. Hermon. This international coalition represented Israel's most serious military threat since the Philistines.",
            "questions": [
                "When have you 'made yourself odious' through pride or foolish decisions, then tried to buy your way out of the consequences?",
                "How does Ammon's mercenary alliance illustrate the futility of trusting in worldly alliances rather than God's protection?"
            ]
        },
        "16": {
            "analysis": "<strong>They were put to the worse before Israel</strong> (נִגְּפוּ לִפְנֵי יִשְׂרָאֵל). The verb <em>nagaph</em> (נָגַף) means 'to be struck down/defeated,' often used of God's judgment. Despite superior numbers and mercenary reinforcements, the Arameans suffered decisive defeat.<br><br><strong>Drew forth the Syrians that were beyond the river</strong>—The 'river' (הַנָּהָר) always means the Euphrates in Chronicles. This escalation brought forces from the Aramean heartland, yet even this couldn't overcome God's purpose to establish David's kingdom to its promised borders. Human schemes fail when they oppose divine covenant.",
            "historical": "Hadarezer's mobilization of trans-Euphrates forces (with Shophach as commander) represented the maximum Aramean military effort. David's victory (v.18: 7,000 charioteers killed) permanently ended Aramean independence, making them vassals. This battle was decisive for establishing Solomon's empire.",
            "questions": [
                "What 'reinforcements beyond the river' do you summon when God's purposes contradict your plans, and how does that work out?",
                "How should the sovereignty of God in Israel's battles inform your response when opposition to God's will seems overwhelming?"
            ]
        }
    },
    "20": {
        "7": {
            "analysis": "<strong>But when he defied Israel, Jonathan the son of Shimea David's brother slew him</strong>—This verse concludes the account of giant-slaying (vv.4-7), echoing David's youth. The verb <em>charaph</em> (חָרַף, 'to defy/reproach') is the same used of Goliath's blasphemous challenge (1 Sam 17:10).<br><br>Jonathan's victory over another giant shows that David's faith was transmissible—family members imitate covenant courage. The giants' defeat symbolizes removing the final remnants of pre-conquest Canaanite strength, fulfilling Joshua's incomplete conquest (Josh 11:22: giants remained in Gaza, Gath, and Ashdod). Christ's victory over death is the ultimate giant-slaying.",
            "historical": "These battles occurred c. 985 BC, late in David's wars. The giants were Rephaim descendants, possibly related to the Anakim who terrorized Israel's spies (Num 13:33). Their final elimination removed a psychological as well as military threat, demonstrating God's faithfulness to complete what He begins.",
            "questions": [
                "What 'giants' defy God's purposes in your life, and who in your family or church might God use to help defeat them?",
                "How does the defeat of literal giants in David's era foreshadow Christ's defeat of spiritual giants (principalities and powers)?"
            ]
        }
    },
    "21": {
        "9": {
            "analysis": "<strong>And the LORD spake unto Gad, David's seer, saying</strong>—After David's prideful census (v.1-8), God sends Gad (גָּד, 'fortune'), a prophet attached to David's court since his outlaw days (1 Sam 22:5). The term <em>chozeh</em> (חֹזֶה, 'seer') emphasizes visionary revelation.<br><br>This verse introduces God's three-fold judgment offer (v.11-12: three years famine, three months defeat, or three days pestilence). God's speaking through prophets maintained covenant communication even in judgment. Gad appears only here and after the plague, showing prophets as covenant mediators who both announce and interpret divine discipline.",
            "historical": "The census (c. 980 BC) was sinful because it reflected trust in military strength rather than God's power. Numbering Israel evoked the wilderness census sin (Num 1-4 vs. Exod 30:11-16's atonement requirement). Gad's prophetic ministry demonstrates that even at the monarchy's height, prophets checked royal power.",
            "questions": [
                "When God sends messengers to confront your sin, do you respond with David's eventual repentance (v.17) or hardened resistance?",
                "How does the necessity of prophetic mediation in the Old Testament highlight your privilege of direct access to God through Christ?"
            ]
        },
        "19": {
            "analysis": "<strong>And David went up at the saying of Gad, which he spake in the name of the LORD</strong>—True repentance produces immediate obedience. The Hebrew construction emphasizes agency: the word was Gad's, but the authority was Yahweh's (<em>b'shem YHWH</em>, בְּשֵׁם יְהוָה).<br><br>David's 'going up' (עָלָה) to Ornan's threshing floor reverses his descending into pride. This location becomes the temple site (22:1; 2 Chr 3:1), where Solomon's temple will stand. From judgment comes sanctuary; from plague-stopping sacrifice comes the place of perpetual atonement. This prefigures Golgotha, where God's judgment and mercy meet.",
            "historical": "The threshing floor of Ornan (Araunah in 2 Sam 24) was on Mt. Moriah, where Abraham offered Isaac (Gen 22). David's purchase of the site (v.24-25) and sacrifice transformed a place of threatened judgment into the location of God's dwelling—a prophetic pattern of substitutionary atonement.",
            "questions": [
                "How quickly do you obey when God's word (through Scripture, conscience, or godly counsel) directs you to specific action?",
                "What 'threshing floors' in your life—places of crushing and judgment—has God transformed into places of worship and grace?"
            ]
        },
        "29": {
            "analysis": "<strong>For the tabernacle of the LORD, which Moses made in the wilderness, and the altar of the burnt offering, were at that season in the high place at Gibeon</strong>—This verse explains why David couldn't inquire of the Lord at the Mosaic tabernacle: his fear of the destroying angel (v.30) prevented the seven-mile journey to Gibeon.<br><br>The split between ark (in Jerusalem) and tabernacle (at Gibeon, 1 Chr 16:39) created temporary liturgical dualism, resolved only when Solomon completed the temple. Chronicles presents this tension to show why the unified temple was theologically necessary—one God demands one sanctuary (Deut 12:5-14).",
            "historical": "The tabernacle remained at Gibeon (6 miles northwest of Jerusalem) from Saul's massacre of Nob's priests (1 Sam 22:17-19) until Solomon's temple. Gibeon was a major 'high place' where Solomon later sacrificed (2 Chr 1:3). David's inability to reach it demonstrates how sin disrupts normal worship patterns.",
            "questions": [
                "When fear or failure disrupts your normal spiritual disciplines, where do you turn for access to God?",
                "How does the divided worship (ark in Jerusalem, tabernacle at Gibeon) illustrate the incomplete nature of all Old Covenant worship, resolved in Christ?"
            ]
        }
    },
    "22": {
        "9": {
            "analysis": "<strong>For his name shall be Solomon, and I will give peace and quietness unto Israel in his days</strong>—The name <em>Shlomo</em> (שְׁלֹמֹה) derives from <em>shalom</em> (שָׁלוֹם, 'peace/wholeness/completion'). God ordains both the son and his name, signaling his role as temple-builder.<br><br><strong>A man of rest</strong> (אִישׁ מְנוּחָה, <em>ish menuchah</em>)—While David was a warrior (<em>ish milchamah</em>), Solomon embodies the <em>menuchah</em> promised in Deuteronomy 12:9-10. This typological rest prefigures Christ, the greater Solomon who gives eternal rest (Matt 11:28; Heb 4:8-11). Only in Messianic peace can true worship be established.",
            "historical": "This prophecy, given before Solomon's birth to Bathsheba (c. 985 BC), secured succession despite Adonijah's later claims. Solomon's reign (970-930 BC) was indeed characterized by peace and prosperity, enabling massive building projects. Yet his later apostasy showed that even typological Solomonic peace wasn't ultimate.",
            "questions": [
                "How does Solomon as 'man of rest' who builds God's house foreshadow Jesus, who gives rest and makes you God's temple?",
                "What 'warfare' in your life prevents rest, and how does Christ's finished work provide the peace Solomon only typified?"
            ]
        },
        "19": {
            "analysis": "<strong>Now set your heart and your soul to seek the LORD your God</strong> (וְעַתָּה תְּנוּ לְבַבְכֶם וְנַפְשְׁכֶם לִדְרוֹשׁ לַיהוָה אֱלֹהֵיכֶם)—David's charge uses the Shema's language (Deut 6:5): whole-person devotion (<em>levav</em>, heart; <em>nephesh</em>, soul). The verb <em>darash</em> (דָּרַשׁ, 'to seek') means diligent inquiry, not casual interest.<br><br><strong>Arise therefore, and build</strong>—Seeking precedes building; worship precedes work. The sanctuary must be built 'to the name of the LORD' (לְשֵׁם יְהוָה), not for human glory. This priority of devotion before action echoes Mary's 'better part' (Luke 10:42) and Paul's 'seek first' (Matt 6:33).",
            "historical": "David's final charge to Israel's leaders (c. 970 BC) emphasized that temple construction required spiritual preparation, not just material resources. The Chronicler, writing for post-exilic temple rebuilders (Ezra-Nehemiah era), applies this principle: external building without internal seeking produces empty formalism.",
            "questions": [
                "How much of your Christian activity involves 'building' without first 'seeking' God with whole-hearted devotion?",
                "What does it mean practically to 'set your heart and soul' to seek God before undertaking ministry projects?"
            ]
        }
    },
    "23": {
        "10": {
            "analysis": "<strong>And the sons of Shimei were, Jahath, Zina, and Jeush, and Beriah. These four were the sons of Shimei</strong>—This genealogical detail within the Levitical organization (ch. 23-26) demonstrates Chronicles' commitment to exhaustive priestly records. The name Shimei (שִׁמְעִי) means 'heard/famous,' from <em>shama</em> (to hear).<br><br>While seemingly mundane, such lists established post-exilic temple legitimacy—only documented Levites could serve. Every name matters in God's covenant administration. Paul's metaphor of the body (1 Cor 12:12-27) echoes this: obscure members are necessary, and genealogical precision ensures proper function.",
            "historical": "David's Levitical reorganization (c. 970 BC) prepared for temple service under Solomon. These genealogies proved invaluable after the exile when returnees needed to verify priestly and Levitical lineage (Ezra 2:62; Neh 7:64). Chronicles preserves what appears mundane because covenant community requires documented continuity.",
            "questions": [
                "How does Scripture's careful recording of 'obscure' servants challenge your evaluation of who is truly important in God's kingdom?",
                "What does the necessity of documented lineage for service teach about God's orderliness and the importance of legitimate calling?"
            ]
        },
        "20": {
            "analysis": "<strong>Of the sons of Uzziel; Michah the first, and Jesiah the second</strong>—Uzziel (עֻזִּיאֵל, 'God is my strength') was Kohath's grandson (Exod 6:18). The designation 'first' and 'second' indicates birth order, important for establishing service priority.<br><br>This brief notice, within extensive Levitical genealogies, shows God's attention to detail in worship organization. No servant is anonymous before Him; each has a place and calling. The principle extends to the New Covenant: God knows His own by name (John 10:3), and believers are 'living stones' with specific placement in the spiritual house (1 Pet 2:5).",
            "historical": "These genealogies served practical purposes in David's administrative reorganization and later in post-exilic restoration. Knowing one's Levitical subdivision determined specific temple duties—gate keeping, music, teaching, or sacrificial assistance. Order in worship honors the God of order (1 Cor 14:40).",
            "questions": [
                "Do you view your place in the body of Christ as significant as these 'first' and 'second' sons in their Levitical duties?",
                "How does God's careful recording of individual names and birth orders encourage you about His personal knowledge of you?"
            ]
        },
        "30": {
            "analysis": "<strong>And to stand every morning to thank and praise the LORD, and likewise at even</strong>—The Hebrew construction emphasizes regularity: <em>la'amod baboker baboker</em> (לַעֲמֹד בַּבֹּקֶר בַּבֹּקֶר, 'to stand morning by morning'). The Levites' primary duty was liturgical: <em>l'hodot ul'hallel</em> (לְהֹדוֹת וּלְהַלֵּל, 'to give thanks and to praise').<br><br>This twice-daily pattern paralleled the <em>tamid</em> offerings (Exod 29:38-42), creating rhythmic worship anchoring Israel's life. Jesus maintained morning prayer (Mark 1:35) and evening devotion, modeling what the Levites symbolized—constant priestly intercession (Heb 7:25). Believers now fulfill this Levitical calling as a 'royal priesthood' (1 Pet 2:9).",
            "historical": "David's organization of 24-hour temple worship (1 Chr 9:33: 'day and night') created what later Judaism called the 'perpetual offering.' This pattern continued until AD 70. The Chronicler presents this ideal worship to motivate post-exilic returnees toward comprehensive devotion, not minimal ritualism.",
            "questions": [
                "How does the Levitical pattern of morning and evening worship challenge your own devotional consistency?",
                "In what ways can you fulfill your calling as a New Covenant priest who offers continual 'sacrifice of praise' (Heb 13:15)?"
            ]
        }
    },
    "24": {
        "8": {
            "analysis": "<strong>The third to Harim, the fourth to Seorim</strong>—This verse appears within the priestly division list (24:7-18), establishing the rotation of Aaron's descendants for temple service. Harim (חָרִם, 'dedicated/consecrated') and Seorim (שְׂעֹרִים, 'barley') represent the third and fourth courses of David's 24-fold division.<br><br>Harim's descendants returned from exile (Ezra 2:39; Neh 7:42), showing these divisions maintained continuity. Zechariah, John the Baptist's father, belonged to Abijah's course (Luke 1:5, the eighth division). These seemingly dry lists demonstrate God's orderly provision for perpetual worship—a pattern Paul applies to New Testament ministry support (1 Cor 9:13-14).",
            "historical": "David's division of priests into 24 courses (c. 970 BC) ensured that each served one week every six months, making temple service manageable while maintaining constant worship. This system functioned until AD 70. The Chronicler records it to validate post-exilic priestly service and encourage proper organization.",
            "questions": [
                "How does God's detailed organization of worship service challenge modern attitudes of 'spontaneity over structure' in ministry?",
                "What principles from the priestly course system apply to modern church leadership rotation and ministry responsibility?"
            ]
        },
        "18": {
            "analysis": "<strong>The three and twentieth to Delaiah, the four and twentieth to Maaziah</strong>—These final two priestly courses complete the 24-fold division. Delaiah (דְּלָיָה, 'Yahweh has drawn/delivered') and Maaziah (מַעַזְיָה, 'Yahweh is a refuge') bear theophoric names declaring God's character.<br><br>The 24 courses created year-round temple coverage, fulfilling the Levitical law's requirement for perpetual service (Num 18:5-7). Revelation's 24 elders (Rev 4:4, 10) may allude to this priestly order, symbolizing the complete worship of redeemed humanity. Each division's lot-casting (24:5) showed that God sovereignly determines ministry assignments.",
            "historical": "These divisions served faithfully through Solomon's reign, survived (partially) through the divided kingdom, endured the exile, and were re-established under Ezra-Nehemiah. The system's longevity (nearly 1,000 years) demonstrates the wisdom of David's Spirit-led organization and God's faithfulness to ordained structures.",
            "questions": [
                "How do the theophoric names (declaring 'Yahweh has drawn,' 'Yahweh is refuge') in priestly divisions remind you that ministry flows from God's character?",
                "What does the casting of lots for priestly service teach about trusting God's sovereignty in your own calling and ministry placement?"
            ]
        },
        "28": {
            "analysis": "<strong>Of Mahli came Eleazar, who had no sons</strong>—This brief notice records a genealogical dead end. Mahli was a Levite of the Merarite clan (23:21), and Eleazar's childlessness meant his line ended. The Hebrew simply states וְלֹא־הָיוּ לוֹ בָנִים (<em>v'lo hayu lo banim</em>, 'and he had no sons').<br><br>Yet Chronicles records even failed lineages, showing covenant faithfulness isn't measured by progeny. Some serve God without earthly legacy. Isaiah 56:3-5 promises eunuchs 'a name better than sons and daughters'—spiritual fruitfulness exceeds physical. Eleazar's service mattered despite his childlessness, foreshadowing Paul's teaching that singleness can enable undistracted devotion (1 Cor 7:32-35).",
            "historical": "In ancient Israel, childlessness was considered divine judgment (Gen 30:1-2), yet the Chronicler matter-of-factly records Eleazar's situation without negative comment. Post-exilic readers, many of whom likely struggled with broken families and uncertain lineages, would find comfort that faithful service, not merely biological succession, honors God.",
            "questions": [
                "How does God's honoring of Eleazar's service despite childlessness encourage those whose lives don't follow conventional 'success' metrics?",
                "In what ways might God be calling you to spiritual fruitfulness that transcends physical legacy or earthly recognition?"
            ]
        }
    }
}

def main():
    """Add commentary to 1 Chronicles JSON file."""

    # Load existing commentary
    file_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add new commentary
    verses_added = 0
    for chapter, verses in COMMENTARY.items():
        if chapter not in data['commentary']:
            data['commentary'][chapter] = {}

        for verse, content in verses.items():
            if verse not in data['commentary'][chapter]:
                data['commentary'][chapter][verse] = content
                verses_added += 1
                print(f"✓ Added commentary for 1 Chronicles {chapter}:{verse}")
            else:
                print(f"⊘ Skipped 1 Chronicles {chapter}:{verse} (already exists)")

    # Save updated commentary
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"✅ Successfully added {verses_added} new commentary entries to 1 Chronicles")
    print(f"{'='*70}\n")

    # Print detailed summary
    print("VERSES ADDED:")
    for chapter, verses in sorted(COMMENTARY.items(), key=lambda x: int(x[0])):
        for verse in sorted(verses.keys(), key=lambda x: int(x)):
            print(f"  • 1 Chronicles {chapter}:{verse}")
    print(f"\n{'='*70}")

if __name__ == '__main__':
    main()
