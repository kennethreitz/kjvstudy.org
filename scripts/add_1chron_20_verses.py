#!/usr/bin/env python3
"""Add commentary for 20 verses in 1 Chronicles."""

import json
from pathlib import Path

# Load existing commentary
commentary_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

with open(commentary_file, 'r') as f:
    data = json.load(f)

# New commentary entries
new_entries = {
    "9": {
        "38": {
            "analysis": "<strong>Mikloth begat Shimeam</strong> (מִקְלוֹת הוֹלִיד אֶת־שִׁמְאָם)—this genealogical record documents the Benjamite families who returned to Jerusalem after the exile. The phrase <strong>over against their brethren</strong> (נֶגֶד אֲחֵיהֶם) indicates these families settled in close proximity to their relatives, demonstrating covenant faithfulness to family bonds and the promised land.<br><br>The Chronicler's emphasis on post-exilic settlement patterns shows God's faithfulness in restoration. These genealogies aren't mere records—they're theological declarations that YHWH preserves His people through judgment and return, fulfilling promises made to Abraham (Genesis 12:7) and renewed through the prophets (Jeremiah 29:10-14).",
            "historical": "Written c. 450-400 BC, 1 Chronicles was composed for post-exilic Jews rebuilding their identity. The genealogies spanning Adam to the returned exiles demonstrated continuity with pre-exilic Israel and God's covenant faithfulness despite Babylonian captivity.",
            "questions": [
                "How does genealogical continuity demonstrate God's covenant faithfulness across generations and national calamity?",
                "What does the return to ancestral lands teach about the permanence of God's promises to His people?"
            ]
        }
    },
    "10": {
        "4": {
            "analysis": "<strong>These uncircumcised</strong> (הָעֲרֵלִים הָאֵלֶּה)—Saul's contempt for Philistines highlights his concern for honor rather than repentance. The term 'uncircumcised' emphasizes covenant identity, yet Saul violated that covenant through disobedience (1 Samuel 13:13-14, 15:22-23). His suicide contradicts Torah's sanctity of life and demonstrates the ultimate futility of self-reliance.<br><br><strong>Fell upon it</strong> (וַיִּפֹּל עָלֶיהָ)—suicide was exceptionally rare in Scripture, appearing only with Saul, his armor-bearer, Ahithophel (2 Samuel 17:23), Zimri (1 Kings 16:18), and Judas (Matthew 27:5). Each case involves covenant rebellion. Saul's death fulfills Samuel's prophecy (1 Samuel 28:19) and demonstrates that those who reject God's word ultimately destroy themselves.",
            "historical": "The Battle of Mount Gilboa (c. 1010 BC) ended Saul's 40-year reign and the Philistines' domination of Israel. Chronicles' account is more concise than 1 Samuel 31, focusing on divine judgment rather than tragic heroism.",
            "questions": [
                "How does Saul's concern for honor over repentance reveal the danger of valuing reputation above relationship with God?",
                "What does Saul's tragic end teach about the consequences of persistent disobedience to God's clear commands?"
            ]
        },
        "14": {
            "analysis": "<strong>Enquired not of the LORD</strong> (לֹא־דָרַשׁ בַּיהוָה)—the verb <em>darash</em> means to seek diligently, consult, or inquire earnestly. Saul's fundamental failure wasn't military incompetence but spiritual independence. He consulted a medium at Endor (1 Samuel 28:7) but not YHWH—the defining indictment of his reign.<br><br><strong>Therefore he slew him</strong> (וַיְמִיתֵהוּ)—divine causation in Scripture encompasses both direct action and judicial abandonment. God 'killed' Saul by withdrawing protection and allowing consequences of rebellion. This parallels Romans 1:24-28 where God 'gives over' rebels to their chosen path. The kingdom's transfer to David fulfills prophetic word (1 Samuel 13:14) and demonstrates that God's purposes cannot be thwarted by human rebellion.",
            "historical": "Chronicles was written for post-exilic Jews facing their own temptation toward self-reliance. Saul's failure to inquire of YHWH warned the restored community that ritual without relationship, and temple without trust, would end in judgment.",
            "questions": [
                "In what areas of life might you be making decisions without genuinely seeking God's direction?",
                "How does the transfer of the kingdom to David demonstrate God's commitment to His promises despite human failure?"
            ]
        }
    },
    "11": {
        "10": {
            "analysis": "<strong>The mighty men</strong> (הַגִּבֹּרִים)—David's elite warriors, called <em>gibborim</em>, parallel the ancient 'mighty men' (<em>nephilim</em>) of Genesis 6:4, but unlike those rebels, David's champions fought for God's anointed king. The phrase <strong>strengthened themselves with him</strong> (הִתְחַזְּקִים עִמּוֹ) uses the reflexive form—they made themselves strong together with David, not for him but alongside him.<br><br><strong>According to the word of the LORD</strong> (כִּדְבַר־יְהוָה)—their valor wasn't mere military prowess but covenant participation in divine purposes. Their loyalty to David was ultimately loyalty to YHWH's prophetic word through Samuel (1 Samuel 16:12-13). This points forward to the apostles who strengthened themselves with Christ (Luke 22:28) and the church built on apostolic foundation (Ephesians 2:20).",
            "historical": "David's mighty men came from diverse backgrounds—some joined him at Adullam during Saul's pursuit (1 Samuel 22:1-2), others at Ziklag (1 Chronicles 12:1-22), still others at Hebron (12:23-40). Their unity around David prefigures the church's unity in Christ.",
            "questions": [
                "How does loyal support of God's anointed leaders reflect participation in divine purposes rather than mere human allegiance?",
                "What does the diversity of David's mighty men teach about God uniting unlikely people around His chosen servant?"
            ]
        },
        "20": {
            "analysis": "<strong>Abishai</strong> (אֲבִישַׁי, 'my father is Jesse')—Zeruiah's son and David's nephew, Abishai appears frequently as David's fierce defender. <strong>Chief of the three</strong> represents the elite inner circle, though verse 21 clarifies he wasn't among 'the three' most honored. The Hebrew <strong>lifting up his spear</strong> (עוֹרֵר אֶת־חֲנִיתוֹ) uses <em>'orer</em>, meaning 'to rouse' or 'brandish'—suggesting aggressive, fearless warfare.<br><br>Killing 300 men in single combat demonstrates extraordinary martial skill, but also raises ethical questions. These exploits occurred during David's rise to power and defensive wars—contexts where YHWH sanctioned military action against covenant enemies. Later prophets and Christ would reveal that God's ultimate kingdom advances not through spears but through suffering servanthood (Isaiah 53; Philippians 2:5-8).",
            "historical": "Abishai's exploits likely occurred during David's outlaw years or early reign (c. 1010-1000 BC). His loyalty remained constant even when David showed mercy to enemies, notably when Abishai wanted to kill Saul (1 Samuel 26:6-9) and Shimei (2 Samuel 16:9).",
            "questions": [
                "How do Old Testament warriors prefigure spiritual warfare in the New Covenant (Ephesians 6:10-18)?",
                "What does Abishai's position—honored but not among 'the three'—teach about God's distribution of roles and recognition?"
            ]
        },
        "30": {
            "analysis": "<strong>Netophathite</strong> (נְטוֹפָתִי)—residents of Netophah, a village near Bethlehem (Ezra 2:22, Nehemiah 7:26). This geographical reference connects David's mighty men to Judah's heartland, the region of his origins and future messianic promises. The repetition of 'Netophathite' emphasizes covenant connection to promised territory.<br><br>These seemingly mundane genealogical details carry theological weight—they demonstrate that God's kingdom purposes involve real people from real places. The incarnation similarly roots salvation history in verifiable geography: 'Bethlehem Ephratah' (Micah 5:2), 'Nazareth' (Matthew 2:23), 'Golgotha' (Mark 15:22). God doesn't work through abstractions but through embodied, located human beings.",
            "historical": "Netophah lay approximately 3 miles southeast of Bethlehem. The village produced other notable figures including Seraiah the son of Tanhumeth (2 Kings 25:23) and singers who returned from Babylonian exile (Nehemiah 12:28).",
            "questions": [
                "How does Scripture's attention to specific places and people combat the notion that faith is merely abstract or spiritual?",
                "What does the geographic concentration of David's allies around Bethlehem foreshadow about the Messiah's origins?"
            ]
        },
        "40": {
            "analysis": "<strong>Ithrite</strong> (יִתְרִי)—descendants of Jether/Ithrah, from Kiriath-jearim in Judah (1 Chronicles 2:53). Both Ira and Gareb bore this designation, indicating they were kinsmen serving together in David's elite corps. Shared geographic and familial origins often strengthened military cohesion in ancient warfare.<br><br>The inclusion of these 'ordinary' names in Scripture's inspired record demonstrates that God notices and honors faithful service even when historical details are sparse. We know nothing of Ira and Gareb beyond their tribal affiliation and elite status, yet their names endure eternally. This anticipates Christ's promise that even a cup of cold water given in His name won't lose its reward (Matthew 10:42).",
            "historical": "The 'Thirty' (actually 37 names in 2 Samuel 23 and Chronicles 11) represents David's expanding elite corps. New champions joined as David's kingdom grew, demonstrating that God continually raises up servants for His purposes.",
            "questions": [
                "How does the eternal record of obscure faithful servants encourage you in seemingly unnoticed service?",
                "What does the geographic diversity of David's mighty men teach about God's kingdom transcending tribal boundaries?"
            ]
        }
    },
    "12": {
        "3": {
            "analysis": "<strong>Ahiezer</strong> (אֲחִיעֶזֶר, 'my brother is help')—notably, these Benjamites from Gibeah, Saul's hometown (1 Samuel 10:26), defected to David. <strong>Berachah</strong> (בְּרָכָה) means 'blessing,' and <strong>Jehu the Antothite</strong> came from Anathoth, later home to Jeremiah (Jeremiah 1:1). These warriors from Saul's own tribe recognizing David as God's anointed demonstrates the Spirit's work transcending natural loyalties.<br><br>Their tribal treason was actually covenant faithfulness—choosing God's choice over tribal allegiance. This prefigures Jesus's teaching that following Him may divide natural families (Matthew 10:34-37) and Paul's declaration that in Christ there is neither Jew nor Greek, slave nor free (Galatians 3:28). True brotherhood isn't biological but spiritual.",
            "historical": "These Benjamites joined David at Ziklag during his exile among the Philistines (c. 1012-1010 BC). Their defection risked Saul's vengeance against their families, demonstrating the costliness of following God's anointed before his public vindication.",
            "questions": [
                "When has following God's clear direction required you to transcend natural loyalties or tribal allegiances?",
                "How do these Benjamite defectors prefigure the church's composition from every tribe, tongue, and nation?"
            ]
        },
        "13": {
            "analysis": "<strong>Jeremiah the tenth, Machbanai the eleventh</strong> (יִרְמְיָהוּ הָעֲשִׂירִי מַכְבַּנַּי עַשְׁתֵּי־עָשָׂר)—this verse concludes a roster of Gadite warriors ranked by prowess. The ordinal numbers indicate hierarchical organization within David's forces, demonstrating administrative order even during his fugitive years. These Gadites crossed the flooding Jordan (v. 15), showing extraordinary courage and commitment.<br><br>The preservation of these names in Scripture's eternal record honors faithful warriors whom God remembers even when historical details are lost. Hebrews 11:32-38 similarly commemorates obscure faithful servants who 'through faith subdued kingdoms.' Our names may be forgotten by history, but they're written in the Lamb's book of life (Revelation 21:27).",
            "historical": "Gadites dwelt east of the Jordan in Gilead and Bashan (Numbers 32:34-36). Their journey to David required crossing the Jordan during its seasonal flood (v. 15), a feat requiring both military skill and divine favor, echoing Israel's miraculous crossing under Joshua (Joshua 3:14-17).",
            "questions": [
                "How does God's eternal record of obscure servants encourage faithfulness even when your service seems unrecognized?",
                "What does the organized ranking of David's forces during his wilderness years teach about maintaining godly order in difficult seasons?"
            ]
        },
        "23": {
            "analysis": "<strong>Ready armed to the war</strong> (חָלוּץ לַצָּבָא)—literally 'equipped for the army,' indicating full battle readiness. These troops came <strong>to Hebron</strong> (חֶבְרוֹן), David's capital during his 7-year reign over Judah (2 Samuel 5:5), to crown him king over all Israel. The phrase <strong>to turn the kingdom</strong> (לְהָסֵב מַלְכוּת־שָׁאוּל אֵלָיו) uses <em>haseb</em>, meaning 'to turn around' or 'transfer'—not violent overthrow but divinely orchestrated succession.<br><br><strong>According to the word of the LORD</strong> (כִּפִי יְהוָה)—this phrase appears repeatedly in Chronicles, emphasizing that Israel's history isn't mere political maneuvering but the outworking of prophetic word. Samuel's anointing (1 Samuel 16:12-13) and Nathan's covenant (2 Samuel 7:12-16) find fulfillment in David's unified kingdom, ultimately pointing to Messiah's eternal throne (Luke 1:32-33).",
            "historical": "David reigned in Hebron over Judah for 7½ years before the northern tribes crowned him at age 37 (2 Samuel 5:4-5). This gathering at Hebron (c. 1003 BC) represented national reunification after civil war between David and Saul's house under Ish-bosheth.",
            "questions": [
                "How does David's gradual ascension to full kingship demonstrate God's timing in fulfilling His promises?",
                "What does the unity of Israel's tribes around God's chosen king foreshadow about the church's unity in Christ?"
            ]
        },
        "33": {
            "analysis": "<strong>Expert in war</strong> (עֹרְכֵי מִלְחָמָה)—literally 'arrangers of battle,' indicating not just individual prowess but tactical skill in military formations. Zebulun's contingent numbered 50,000, the largest tribal force, demonstrating extraordinary commitment to David's kingship. <strong>Keep rank</strong> (לַעֲרֹךְ) uses the same root as 'expert'—they could form and maintain battle lines, essential for ancient warfare.<br><br><strong>Not of double heart</strong> (לֹא־בְּלֵב וָלֵב)—literally 'not with heart and heart,' meaning unified loyalty without divided allegiance. This Hebrew idiom appears in Psalm 12:2 describing flattering lips that speak 'with a double heart.' Zebulun's single-hearted devotion contrasts with wavering Israel under Elijah: 'How long halt ye between two opinions?' (1 Kings 18:21). Jesus echoed this: 'No man can serve two masters' (Matthew 6:24).",
            "historical": "Zebulun's territory in lower Galilee faced frequent foreign invasions, producing a tribe battle-hardened and militarily sophisticated. Their wholehearted support of David (c. 1003 BC) demonstrated that northern tribes recognized God's anointing despite having no blood connection to David's Judean base.",
            "questions": [
                "In what areas of life might you be 'double-hearted,' trying to serve both God and competing loyalties?",
                "How does Zebulun's combination of military skill and undivided loyalty model effective service to God's kingdom?"
            ]
        }
    },
    "13": {
        "3": {
            "analysis": "<strong>Let us bring again the ark</strong> (וְנָסֵבָה אֶת־אֲרוֹן אֱלֹהֵינוּ אֵלֵינוּ)—David's desire to restore the ark demonstrates his heart for God's presence, contrasting sharply with Saul. The ark represented YHWH's throne (1 Samuel 4:4), residing at Kiriath-jearim for 70+ years after its capture by Philistines and return (1 Samuel 6:21-7:2). <strong>We enquired not at it</strong> (לֹא־דְרַשְׁנוּהוּ) uses <em>darash</em>—the same verb describing what Saul failed to do (1 Chronicles 10:14).<br><br>Yet good intentions don't sanctify disobedience—David's first attempt violated Torah by transporting the ark on a cart rather than Levites' shoulders (Numbers 4:15, 7:9). Uzzah's death (v. 10) taught that passion for God's presence must align with God's prescribed methods. The means matter as much as the ends. New Covenant worship 'in spirit and truth' (John 4:24) still requires obedience, not presumption.",
            "historical": "David's first attempt to bring the ark to Jerusalem (c. 1003 BC) occurred soon after his coronation over all Israel. The ark's neglect during Saul's 40-year reign symbolized Israel's spiritual apostasy, making its restoration symbolically crucial for David's reform.",
            "questions": [
                "How can genuine zeal for God's glory become corrupted when it ignores God's prescribed methods?",
                "What does the ark's 70-year neglect teach about the danger of maintaining religious forms while ignoring God's presence?"
            ]
        },
        "13": {
            "analysis": "<strong>David brought not the ark home</strong> (וְלֹא־הֵסִיר דָּוִיד אֶת־הָאָרוֹן)—after Uzzah's death, David feared YHWH and halted the procession. <strong>Carried it aside</strong> (וַיַּטֵּהוּ) means he diverted it, placing it in <strong>Obed-edom the Gittite</strong>'s house. 'Gittite' indicates Obed-edom was from Gath-rimmon, a Levitical city (Joshua 21:24), though some suggest Philistine Gath, making his faithfulness more remarkable.<br><br>The ark's three-month stay blessed Obed-edom's household (v. 14), demonstrating that God's presence brings blessing when approached rightly. This parallels Jesus's words: 'Today salvation has come to this house' (Luke 19:9). God desires to dwell with His people (Revelation 21:3), but His holiness demands reverence. The delay taught David that enthusiasm must submit to instruction—the second successful attempt (chapter 15) carefully followed Torah regulations.",
            "historical": "The three-month delay (c. 1003 BC) allowed David to study Torah requirements for ark transportation (15:2, 13). This pause transformed a failure into wisdom, demonstrating that setbacks in serving God can become preparation for faithful service.",
            "questions": [
                "When have delays or apparent failures in your spiritual life actually been God's preparation for more faithful service?",
                "How does Obed-edom's willingness to house the ark after Uzzah's death demonstrate faith that honors God's holiness?"
            ]
        }
    },
    "14": {
        "9": {
            "analysis": "<strong>The Philistines came</strong> (וּפְלִשְׁתִּים בָּאוּ)—David's coronation threatened Philistine hegemony over Israel. <strong>Spread themselves</strong> (וַיִּפָּשְׁטוּ) means they 'raided' or 'made a foray,' using the same verb describing locusts swarming (Judges 9:33). The <strong>valley of Rephaim</strong> (עֵמֶק רְפָאִים) lies southwest of Jerusalem, named after the ancient <em>Rephaim</em> (giant clans). Its strategic location threatened David's capital.<br><br>Unlike Saul who failed to inquire of YHWH, David immediately sought divine direction (v. 10). God granted specific tactical instructions—attacking from behind balsam trees when hearing 'the sound of marching' in the treetops (v. 15), likely representing angelic armies (2 Kings 6:17). This pattern of inquiry before battle characterizes David's reign and prefigures Jesus who did nothing except what He saw the Father doing (John 5:19).",
            "historical": "This Philistine invasion occurred shortly after David's coronation at Hebron (c. 1003 BC). The Philistines had tolerated David's presence in Ziklag under their vassal control, but his unified kingship over Israel threatened their regional dominance.",
            "questions": [
                "How does David's immediate inquiry of God in crisis contrast with Saul's pattern of self-reliance?",
                "What does God's specific tactical guidance teach about seeking divine direction for practical challenges, not just 'spiritual' matters?"
            ]
        }
    },
    "15": {
        "2": {
            "analysis": "<strong>Then David said</strong> (אָז אָמַר דָּוִיד)—the temporal marker indicates David learned from Uzzah's death. <strong>None ought to carry the ark... but the Levites</strong> (לֹא לָשֵׂאת אֶת־אֲרוֹן הָאֱלֹהִים כִּי אִם־הַלְוִיִּם) directly quotes Numbers 4:15 and 7:9. The first attempt used a Philistine method—an ox cart (6:7)—treating God's throne like captured war booty. Now David aligns practice with Torah.<br><br><strong>The LORD chosen</strong> (בָּחַר יְהוָה)—God's election of Levites for tabernacle service (Numbers 3:12-13, 8:14-18) wasn't arbitrary but covenantal. Their selection in place of Israel's firstborn after the golden calf incident (Exodus 32:26-29) established that approaching God requires both divine appointment and consecration. New Covenant access to God's presence comes through Christ our High Priest (Hebrews 4:14-16), who is both divinely appointed and eternally consecrated.",
            "historical": "This second attempt (c. 1003 BC) succeeded because David submitted zeal to Scripture. The three-month delay allowed study of Mosaic law, demonstrating that effective spiritual leadership requires biblical knowledge, not just passion or political authority.",
            "questions": [
                "How does David's submission to Torah after failure demonstrate that godly leadership learns from mistakes rather than defending them?",
                "What does Levitical consecration for ark transportation teach about God's requirement of both calling and preparation for ministry?"
            ]
        },
        "12": {
            "analysis": "<strong>Ye are the chief of the fathers of the Levites</strong> (אַתֶּם רָאשֵׁי הָאָבוֹת לַלְוִיִּם)—David addresses Levitical clan heads, emphasizing their covenantal responsibility. <strong>Sanctify yourselves</strong> (הִתְקַדְּשׁוּ) uses the reflexive Hithpael stem—they must actively consecrate themselves through ritual purification (Numbers 8:6-22), not passively receive holiness. This included washing garments, ceremonial bathing, and abstaining from ritual defilement.<br><br><strong>That ye may bring up the ark</strong> (לְהַעֲלוֹת אֶת־אֲרוֹן)—the verb <em>ha'alot</em> ('bring up') carries liturgical freight, used for sacrificial offerings ascending to God. Transporting the ark wasn't mere logistics but worship. David's insistence on proper consecration after Uzzah's death demonstrates learned reverence. Hebrews 12:28-29 echoes this: 'Let us have grace, whereby we may serve God acceptably with reverence and godly fear: For our God is a consuming fire.'",
            "historical": "The second ark procession (c. 1003 BC) contrasts dramatically with the first—now Levites carry it on poles as prescribed (v. 15), sacrifices accompany every six steps (2 Samuel 6:13), and David dances before the Lord with abandoned joy (v. 29). Proper method enabled proper worship.",
            "questions": [
                "How does the call to 'sanctify yourselves' challenge modern assumptions that casualness with God demonstrates intimacy?",
                "What does David's insistence on Levitical consecration teach about preparation for ministry beyond mere willingness or talent?"
            ]
        },
        "22": {
            "analysis": "<strong>Chenaniah, chief of the Levites</strong> (וּכְנַנְיָהוּ שַׂר־הַלְוִיִּם)—his name means 'YHWH establishes.' <strong>Was for song</strong> (בְּמַשָּׂא) literally means 'in the lifting up,' referring to lifting up voices in song, not burden-bearing. <strong>He instructed about the song</strong> (יָסַר בַּמַּשָּׂא)—the verb <em>yasar</em> means to discipline, instruct, or train, indicating formal musical education and liturgical oversight.<br><br><strong>Because he was skilful</strong> (כִּי־מֵבִין הוּא)—the verb <em>mebin</em> means understanding, discerning, or having insight. True worship leadership requires both Spirit-given understanding and developed skill. Excellence in worship doesn't compete with Spirit-dependence but expresses it. Paul's instruction that worship should be done 'decently and in order' (1 Corinthians 14:40) and David's organization of Levitical musicians (1 Chronicles 25:1-7) demonstrate that preparing excellent worship honors God.",
            "historical": "David revolutionized Israelite worship by organizing professional Levitical musicians (1 Chronicles 25). This unprecedented liturgical sophistication prepared Israel for temple worship and established patterns influencing synagogue liturgy and ultimately Christian worship.",
            "questions": [
                "How does Chenaniah's combination of skill and understanding challenge false dichotomies between 'skilled' and 'Spirit-led' worship?",
                "What does the appointment of a worship leader with training responsibility teach about the importance of musical excellence in corporate worship?"
            ]
        }
    },
    "16": {
        "3": {
            "analysis": "<strong>He dealt to every one of Israel</strong> (וַיְחַלֵּק לְכָל־אִישׁ יִשְׂרָאֵל)—David's distribution of food to all participants, <strong>both man and woman</strong> (מֵאִישׁ וְעַד־אִשָּׁה), demonstrates covenant inclusion and royal generosity. A <strong>loaf of bread</strong> (חַלַּת־לֶחֶם), <strong>a good piece of flesh</strong> (אֶשְׁפָּר), and <strong>a flagon of wine</strong> (אֲשִׁישָׁה, likely raisin cakes) provided festive celebration, not mere subsistence.<br><br>This royal feast prefigures messianic banquet imagery throughout Scripture. Isaiah prophesies a feast 'of fat things, of wines on the lees well refined' (Isaiah 25:6). Jesus's multiplication of loaves (Matthew 14:13-21) and institution of the Lord's Supper (Luke 22:19-20) fulfill this pattern. The King provides abundant provision for all who gather in His presence. Revelation's marriage supper of the Lamb (19:9) consummates this theme.",
            "historical": "This celebration followed the ark's successful installation in Jerusalem (c. 1003 BC). David's distribution to all participants—not just Levites or tribal leaders—democratized covenant blessing and foreshadowed the priesthood of all believers (1 Peter 2:9).",
            "questions": [
                "How does David's inclusive distribution of celebratory food reflect God's desire that all His people feast in His presence?",
                "What connections do you see between this feast, the Lord's Supper, and the future marriage supper of the Lamb?"
            ]
        },
        "13": {
            "analysis": "<strong>O ye seed of Israel his servant</strong> (זֶרַע יִשְׂרָאֵל עַבְדּוֹ)—David's psalm (vv. 8-36) addresses God's covenant people through Abraham's grandson. <strong>Seed</strong> (זֶרַע) appears throughout Genesis in promises to Abraham (12:7, 15:5, 17:7), carrying messianic freight ultimately fulfilled in Christ who is 'the seed' (Galatians 3:16). <strong>His servant</strong> recalls Jacob's title, but also anticipates the Suffering Servant of Isaiah 42-53.<br><br><strong>Children of Jacob, his chosen ones</strong> (בְּנֵי יַעֲקֹב בְּחִירָיו)—the term <em>bechirav</em> (chosen ones) emphasizes divine election, not human merit. Israel's identity rests on God's sovereign choice, a theme Paul expounds in Romans 9-11. Yet New Covenant believers—Jew and Gentile—are also 'a chosen generation' (1 Peter 2:9), elect according to God's foreknowledge (Ephesians 1:4-5). Election produces worship, not pride.",
            "historical": "This psalm (Psalm 105:1-15 with adaptations) recounts salvation history from Abraham through Egyptian bondage. David's liturgical use of salvation history taught Israel their identity and purpose, establishing a pattern for Christian worship rooted in gospel proclamation.",
            "questions": [
                "How does remembering your identity as 'chosen' in Christ shape your worship and daily obedience?",
                "What does David's emphasis on covenant history teach about the importance of remembering God's past faithfulness?"
            ]
        },
        "23": {
            "analysis": "<strong>Sing unto the LORD, all the earth</strong> (שִׁירוּ לַיהוָה כָּל־הָאָרֶץ)—David's call extends beyond Israel to universal worship, anticipating the Great Commission (Matthew 28:19) and Revelation's vision of every tribe, tongue, and nation before God's throne (7:9). The verb <strong>shew forth</strong> (בַּשְּׂרוּ) means 'proclaim good news,' the same root as <em>besorah</em> (gospel). Worship inherently includes evangelistic proclamation.<br><br><strong>From day to day his salvation</strong> (מִיּוֹם־אֶל־יוֹם יְשׁוּעָתוֹ)—continuous, daily declaration of YHWH's saving acts. The noun <em>yeshu'ato</em> (salvation) shares its root with 'Jesus' (Yeshua), who embodies God's ultimate saving act. Authentic worship doesn't merely celebrate past deliverance but proclaims ongoing salvation, pointing others to the Savior. As Paul declares, 'How shall they hear without a preacher?' (Romans 10:14).",
            "historical": "David's psalm combines personal thanksgiving with missionary vision. Written c. 1003 BC during Israel's limited international influence, it prophetically envisions worldwide worship—fulfilled as the gospel spreads to earth's ends (Acts 1:8).",
            "questions": [
                "How does your personal worship include proclamation of God's salvation to those who don't yet know Him?",
                "What does 'from day to day' teach about making gospel proclamation a daily practice rather than occasional activity?"
            ]
        }
    }
}

# Merge new entries with existing data
for chapter, verses in new_entries.items():
    if chapter not in data["commentary"]:
        data["commentary"][chapter] = {}
    for verse, content in verses.items():
        if verse not in data["commentary"][chapter]:
            data["commentary"][chapter][verse] = content
            print(f"Added commentary for 1 Chronicles {chapter}:{verse}")
        else:
            print(f"Commentary already exists for 1 Chronicles {chapter}:{verse}, skipping")

# Save updated data
with open(commentary_file, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nCompleted! Commentary entries processed.")
