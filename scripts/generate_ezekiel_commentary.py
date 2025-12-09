#!/usr/bin/env python3
"""
Generate missing commentary for Ezekiel
"""

import json
from pathlib import Path

# All missing verses with their text
COMMENTARY = {
    "21": {
        "28": {
            "analysis": "<strong>The sword, the sword is drawn: for the slaughter it is furbished</strong>—This oracle shifts from Babylon (21:1-27) to Ammon, who gloated over Judah's fall. The Hebrew חֶרֶב (ḥerev, 'sword') is repeated for emphasis, with מְרֻטָּה (mĕruṭṭāh, 'drawn/unsheathed') and מְרוּטָה (mĕrûṭāh, 'polished/furbished') showing the weapon's readiness.<br><br><strong>Concerning the Ammonites, and concerning their reproach</strong> (חֶרְפָּתָם, ḥerpātām)—Ammon mocked Jerusalem's destruction (25:3, 6), but God's sword would not return to its sheath until Ammon too was judged. The 'glittering' (בָּרָק, bārāq, 'lightning/flash') describes the polished blade's terrifying appearance. Five years after Jerusalem fell (587 BC), Nebuchadnezzar conquered Ammon (582 BC), fulfilling this prophecy exactly.",
            "historical": "The Ammonites (descendants of Lot through incest, Genesis 19:38) occupied territory east of the Jordan River. They perpetually opposed Israel and rejoiced at Jerusalem's fall in 586 BC. Ezekiel prophesied their destruction circa 587 BC, shortly after his visions of Jerusalem's judgment.",
            "questions": [
                "How does rejoicing over others' judgment invite judgment upon ourselves?",
                "What does God's extended 'sword' metaphor teach about His impartial justice?",
                "How should believers respond when witnessing divine judgment on the wicked?"
            ]
        },
        "29": {
            "analysis": "<strong>Whiles they see vanity unto thee, whiles they divine a lie unto thee</strong>—Ammon relied on false prophets and diviners (שָׁוְא, shāwĕ, 'emptiness/falsehood'; קָסַם, qāsam, 'to divine'). Their occult practices gave lying oracles, promising security when destruction loomed.<br><br><strong>To bring thee upon the necks of them that are slain, of the wicked</strong>—The imagery depicts corpses piled with Ammon's slain 'upon the necks' of Judah's wicked who were already judged. Their fate was linked: both nations would fall under Babylon's sword. <strong>Whose day is come, when their iniquity shall have an end</strong> (עֲוֹנָם קֵץ, ăwōnām qēṣ)—The appointed time (יוֹם, yôm) of final reckoning. God's patience has limits; accumulated iniquity reaches fullness and demands judgment (Genesis 15:16).",
            "historical": "Ammonite religion centered on Molech/Milcom worship, involving child sacrifice and divination practices explicitly condemned in Mosaic law (Leviticus 18:21, Deuteronomy 18:10-12). Their false prophets promised peace, but Nebuchadnezzar destroyed them five years after Jerusalem.",
            "questions": [
                "What modern 'divinations' or false assurances do people trust instead of God's Word?",
                "How does God's patience with accumulating sin differ from His ultimate justice?",
                "Why does God judge nations who mock His people's discipline?"
            ]
        },
        "30": {
            "analysis": "<strong>Shall I cause it to return into his sheath?</strong>—A rhetorical question expecting 'No.' Once God's sword of judgment is drawn (v. 28), it will not be sheathed until the sentence is fully executed. This contrasts with potential repentance scenarios elsewhere (Jeremiah 18:7-8).<br><br><strong>I will judge thee in the place where thou wast created, in the land of thy nativity</strong>—Ammon would not escape by fleeing; judgment would find them in their homeland east of Jordan. The Hebrew מְכוֹרוֹתַיִךְ (mĕkôrôtayik, 'origins/nativity') and מוֹלַדְתֵּךְ (môladetēk, 'birthplace') emphasize that their ancestral land would become their graveyard. God judges nations where they sinned, removing any illusion of sanctuary. This principle appears throughout Scripture: judgment comes to the sinner's own territory (Obadiah 15-16).",
            "historical": "Ammon's territory was roughly modern-day Amman, Jordan. After Nebuchadnezzar's 582 BC conquest, Ammonite identity largely disappeared from history. Archaeological evidence shows massive destruction of Ammonite cities in the early 6th century BC, confirming Ezekiel's prophecy.",
            "questions": [
                "What does God's refusal to 'sheath the sword' teach about the certainty of judgment?",
                "How does judging nations 'in their own land' demonstrate God's omnipresence?",
                "Are there sins or situations you're trying to escape rather than face before God?"
            ]
        },
        "31": {
            "analysis": "<strong>I will pour out mine indignation upon thee</strong>—The Hebrew זַעְמִי (zaʿmî, 'indignation/wrath') describes God's burning anger at persistent covenant violation. The 'pouring out' (שָׁפַךְ, shāphak) metaphor suggests overwhelming, inescapable judgment like a flood.<br><br><strong>I will blow against thee in the fire of my wrath</strong>—God Himself becomes the bellows (פּוּחַ, pûaḥ, 'to blow/breathe'), intensifying judgment like a blacksmith fans flames. <strong>And deliver thee into the hand of brutish men, and skilful to destroy</strong>—The Babylonians are described as בֹּעֲרִים (bōʿărîm, 'brutish/burning'), and חָרָשֵׁי מַשְׁחִית (ḥārāshê mashḥît, 'artisans of destruction'). This chilling phrase depicts professional destroyers—soldiers whose craft was devastation. God uses ungodly nations as instruments of His righteous judgment (Isaiah 10:5-6).",
            "historical": "Nebuchadnezzar's Babylonian army was infamous for systematic, professional destruction. Archaeological excavations show Babylonian siege techniques were brutally efficient, including starvation tactics, systematic burning, and complete demolition of city walls and gates.",
            "questions": [
                "How can God righteously use 'brutish men' as instruments of His judgment?",
                "What does God's 'blowing on' judgment fires teach about His active involvement?",
                "When have you seen God use difficult circumstances as refining fire in your life?"
            ]
        },
        "32": {
            "analysis": "<strong>Thou shalt be for fuel to the fire</strong>—Ammon itself would become אָכְלָה לָאֵשׁ (oklāh lāēsh, 'food for fire'), not merely destroyed by fire but consumed as its fuel. This intensifies the judgment: complete obliteration.<br><br><strong>Thy blood shall be in the midst of the land; thou shalt be no more remembered</strong>—The Hebrew זָכַר (zākar, 'to remember/mention') indicates total erasure from collective memory. Unlike Israel, who would be preserved and restored (chapter 37), Ammon would vanish from history. <strong>For I the LORD have spoken it</strong>—The divine signature כִּי אֲנִי יְהוָה דִּבַּרְתִּי (kî ănî YHWH dibbartî) seals the prophecy with absolute certainty. What God speaks must occur (Isaiah 55:11). Archaeological and historical records confirm: after the Babylonian conquest, Ammonite culture disappeared, absorbed into Arab populations.",
            "historical": "By the 3rd century BC, 'Ammon' existed only as a geographical reference (Amman). The Ammonites as a distinct people were gone. In contrast, Jewish identity survived Babylonian exile. This dramatic difference fulfilled Ezekiel's distinction between Israel's discipline and Ammon's destruction.",
            "questions": [
                "What does Ammon's complete erasure teach about God's sovereignty over nations?",
                "How does God's preservation of Israel contrast with Ammon's disappearance?",
                "What promises has God 'spoken' to believers that are equally certain?"
            ]
        }
    },
    "22": {
        "31": {
            "analysis": "<strong>Therefore have I poured out mine indignation upon them; I have consumed them with the fire of my wrath</strong>—This concluding verse of chapter 22 summarizes Jerusalem's fate. The Hebrew זַעַם (zaʿam, 'indignation') and חֵמָה (ḥēmāh, 'wrath/burning anger') depict God's intense anger at systemic corruption detailed in verses 1-30.<br><br><strong>Their own way have I recompensed upon their heads</strong>—The principle of poetic justice: דַּרְכָּם בְּרֹאשָׁם נָתַתִּי (darkām bĕrōshām nātattî, 'their way on their head I have placed'). They are punished according to their own evil path (Proverbs 1:31, Galatians 6:7). God's judgment is perfectly calibrated to the sin: prophets who saw false visions received true judgment; princes who shed blood had blood poured out; priests who profaned holy things saw the temple destroyed. This verse follows God's futile search for an intercessor (v. 30): finding none, judgment became inevitable.",
            "historical": "Chapter 22 catalogs Jerusalem's comprehensive corruption circa 590 BC: bloodshed, idolatry, oppression, sexual immorality, dishonest gain, Sabbath violation, and prophetic lies. No social class was exempt—princes, priests, prophets, and people all participated. Jerusalem fell in 586 BC, four years after this prophecy.",
            "questions": [
                "How does God's search for 'one intercessor' (v. 30) highlight the importance of faithful remnants?",
                "What does 'their own way recompensed on their heads' teach about the nature of sin's consequences?",
                "Are there systemic sins in our culture where God might be searching for intercessors?"
            ]
        }
    },
    "24": {
        "22": {
            "analysis": "<strong>And ye shall do as I have done: ye shall not cover your lips, nor eat the bread of men</strong>—Ezekiel's strange behavior (not mourning his wife's death, vv. 15-18) becomes a prophetic sign for the exiles. לֹא תַעְטוּ (lōʾ taʿṭû, 'you shall not cover') refers to the customary mourning practice of covering the lower face. לֶחֶם אֲנָשִׁים (leḥem ănāshîm, 'bread of men') was food brought by mourners to comfort the bereaved.<br><br>When Jerusalem falls, the exiles' grief will be so overwhelming, so unnatural (losing the temple, God's dwelling), that normal mourning rituals will seem inadequate. Their shock will paralyze traditional expressions of grief. This prophecy came true: when news reached Babylon in 585 BC (33:21), the people were stunned into silence, realizing God's Word through Ezekiel was devastatingly accurate.",
            "historical": "Ezekiel's wife died suddenly on the very day God announced Jerusalem's siege would begin (24:1-2, 15-18). This was 588 BC. God commanded Ezekiel not to mourn publicly, making him a living object lesson. Ancient Near Eastern mourning was elaborate: wailing, tearing clothes, covering the head, removing shoes, sitting in ashes.",
            "questions": [
                "How did God use Ezekiel's personal tragedy to communicate His message?",
                "When have you experienced grief so profound that normal expressions seemed inadequate?",
                "What does this passage teach about God's sovereignty even over our deepest losses?"
            ]
        },
        "23": {
            "analysis": "<strong>And your tires shall be upon your heads, and your shoes upon your feet</strong>—They would not remove their headwear (פְּאֵרֵיכֶם, pĕʾērêkem, 'turbans/head-dresses') or shoes, customary mourning gestures. <strong>Ye shall not mourn nor weep; but ye shall pine away for your iniquities, and mourn one toward another</strong>—Instead of outward mourning, they would נָמַקּוּ (nāmaqqû, 'waste away/rot') inwardly, consumed by guilt. The verb suggests gradual decay, spiritual and emotional disintegration.<br><br>This describes a worse state than open grief: the paralysis of knowing judgment was deserved, that their own sins destroyed Jerusalem. וּנְהַמְתֶּם (ûnĕhamtem, 'and groan') אִישׁ אֶל־אָחִיו (ʾîsh ʾel-ʾāḥîw, 'each to his brother')—private groaning between individuals, not corporate mourning. Their guilt would isolate them even from communal grief, each man alone with his deserved punishment.",
            "historical": "This prophecy materialized in 586 BC when Jerusalem fell. The book of Lamentations records this stunned, guilty grief: 'The LORD hath done that which he devised...he hath thrown down in his wrath' (Lamentations 2:17). Unlike normal tragedies blamed on fate, this was recognized as deserved covenant judgment.",
            "questions": [
                "What is the difference between mourning a tragedy and mourning deserved consequences?",
                "How can recognition of our own sin in judgment lead to repentance rather than despair?",
                "When has conviction of sin 'wasted away' your spirit before restoration came?"
            ]
        },
        "24": {
            "analysis": "<strong>Thus Ezekiel is unto you a sign</strong>—אוֹת (ʾôt, 'sign/wonder') makes Ezekiel a prophetic omen, his actions prefiguring their experience. <strong>According to all that he hath done shall ye do</strong>—כְּכֹל אֲשֶׁר־עָשָׂה תַּעֲשׂוּ (kĕkōl ăsher-ʿāsāh taʿăśû, 'like all that he has done, you will do'). His restrained grief would mirror theirs exactly.<br><br><strong>And when this cometh, ye shall know that I am the Lord GOD</strong>—The signature recognition formula וִידַעְתֶּם כִּי־אֲנִי אֲדֹנָי יְהוִה (wîdaʿtem kî-ănî ʾădōnāy YHWH) appears over 60 times in Ezekiel. Fulfilled prophecy forces acknowledgment of God's sovereignty. The exiles had doubted Ezekiel (12:21-28); some believed false prophets promising quick return. Jerusalem's fall would vindicate God's true prophet and prove His word unfailing. This 'knowing' would come through bitter experience, not comfortable teaching.",
            "historical": "Ezekiel prophesied in Babylon from 593-571 BC. For seven years (593-586 BC), exiles debated whether Jerusalem would really fall. False prophets like Hananiah promised return within two years (Jeremiah 28). When Jerusalem actually fell in 586 BC, Ezekiel's credibility was established forever.",
            "questions": [
                "How do fulfilled prophecies demonstrate God's sovereignty and trustworthiness?",
                "Why does God often use dramatic 'signs' to communicate His message?",
                "What happens when we ignore God's true prophets and believe comforting lies?"
            ]
        },
        "25": {
            "analysis": "<strong>Also, thou son of man, shall it not be in the day when I take from them their strength</strong>—God addresses Ezekiel directly (בֶּן־אָדָם, ben-ʾādām, 'son of man'). <strong>The joy of their glory</strong> (מָעוֹז, māʿôz, 'stronghold/fortress'; מְשׂוֹשׂ תִּפְאַרְתָּם, mĕśôś tifʾartām, 'joy of their beauty')—metaphors for the Jerusalem temple, Israel's pride and God's earthly dwelling.<br><br><strong>The desire of their eyes, and that whereupon they set their minds</strong>—מַשָּׂא נַפְשָׁם (maśśāʾ naphshām, 'lifting of their soul') indicates deep emotional attachment. The temple was their supreme treasure, like Ezekiel's wife was to him (v. 16). <strong>Their sons and their daughters</strong>—Many died in the siege; others were taken captive. The prophet describes total loss: religious center, family members, homeland—everything that gave life meaning.",
            "historical": "Solomon's temple stood from 966-586 BC (380 years). It represented God's presence, covenant faithfulness, and national identity. Its destruction was psychologically, spiritually, and nationally catastrophic. The temple would not be rebuilt until 516 BC—70 years later, fulfilling Jeremiah's prophecy.",
            "questions": [
                "What 'temples'—things we consider essential to faith—might God remove to teach us deeper dependence?",
                "How can losing what we treasure most become a pathway to knowing God better?",
                "What does God's willingness to destroy His own temple teach about His priorities?"
            ]
        },
        "26": {
            "analysis": "<strong>In that day shall thy mouth be opened to him which is escaped</strong>—A fugitive (פָּלִיט, pālîṭ, 'survivor/refugee') would bring news of Jerusalem's fall to Babylon. God had struck Ezekiel mute except for prophetic utterances (3:26-27); <strong>and thou shalt speak, and be no more dumb</strong>—his speech would be fully restored when the prophecy was fulfilled.<br><br><strong>And thou shalt be a sign unto them; and they shall know that I am the LORD</strong>—Ezekiel's restored speech would itself be a prophetic sign (אוֹת, ʾôt) proving God's word reliable. This occurred exactly as predicted (33:21-22): 'one that had escaped out of Jerusalem came unto me...and my mouth was opened...and I was no more dumb.' The fulfillment of this specific detail—his speech restored at the exact moment news arrived—authenticated his entire prophetic ministry.",
            "historical": "Ezekiel was struck mute in 593 BC (3:26). He could speak only God's prophetic messages for seven years. In January 585 BC, a survivor reached Babylon with news of Jerusalem's fall (33:21), and Ezekiel's full speech was restored. This 18-month gap (fall in July 586, news in January 585) reflects the dangerous 900-mile journey.",
            "questions": [
                "How did God use Ezekiel's muteness to focus attention on His prophetic word?",
                "What does the precise fulfillment of this sign teach about biblical prophecy's reliability?",
                "How has God used limitations in your life to amplify His message?"
            ]
        },
        "27": {
            "analysis": "<strong>And they shall know that I am the LORD, when I have laid the land most desolate</strong>—The recognition formula concludes this sequence. וְיָדְעוּ כִּי־אֲנִי יְהוָה (wĕyādĕʿû kî-ănî YHWH, 'and they shall know that I am the LORD') comes through experiencing God's described judgment: Jerusalem destroyed, temple burned, people scattered.<br><br><strong>Because of all their abominations which they have committed</strong>—The causal clause traces judgment to its source: תּוֹעֲבוֹתֵיהֶם (tôʿăbôtêhem, 'abominations/detestable acts'). Chapter 8 detailed these abominations: idolatry in the temple itself, sun worship, women weeping for Tammuz, secret idols. The exile was not divine capriciousness but covenant justice. God repeatedly warned (2 Kings 17:13-14); they persistently refused. When prophetic threat became historical reality, the survivors would 'know YHWH'—not by comfortable experience, but through devastating discipline that proved His word true.",
            "historical": "This verse concludes the symbolic action section (24:15-27). Jerusalem fell in 586 BC after an 18-month siege. Archaeology confirms massive destruction: burn layers, scattered skeletal remains, demolished walls. Lamentations and Psalms 74, 79 capture the survivors' horror—and their acknowledgment that God did exactly what He promised.",
            "questions": [
                "How does deserved judgment lead to 'knowing the LORD' in ways blessing cannot?",
                "What 'abominations' had become so normalized in Judah that only destruction could wake them?",
                "How do you respond when God's warnings come true in your life?"
            ]
        }
    },
    "26": {
        "20": {
            "analysis": "<strong>When I shall bring thee down with them that descend into the pit</strong>—Tyre's judgment continues. בּוֹר (bôr, 'pit') often means Sheol, the realm of the dead (Psalm 28:1, Isaiah 14:15). <strong>With the people of old time</strong> (עַם־עוֹלָם, ʿam-ʿôlām)—ancient civilizations already destroyed and forgotten.<br><br><strong>And shall set glory in the land of the living</strong>—While Tyre descends to death, God promises צְבִי (ṣĕbî, 'beauty/glory') in אֶרֶץ חַיִּים (ʾereṣ ḥayyîm, 'the land of the living')—referring to restored Israel (20:6, 15). Tyre's wealth and splendor would vanish, but Israel's glory would be restored. This contrast appears throughout prophetic literature: prideful nations are humbled, while humble Israel is exalted (Isaiah 2:11-17). Tyre's ruins would testify to God's judgment; Israel's restoration would testify to His faithfulness.",
            "historical": "Nebuchadnezzar besieged Tyre 585-573 BC (29:18). Though island Tyre survived initially, Alexander the Great completely destroyed it in 332 BC, using mainland ruins to build a causeway, exactly as prophecy depicted (26:12). Today, Tyre is a modest Lebanese town—its ancient glory utterly gone.",
            "questions": [
                "What does Tyre's descent 'to the pit' teach about the destiny of prideful wealth?",
                "How does Israel's promised restoration contrast with Tyre's permanent desolation?",
                "What modern 'Tyres'—centers of wealth and power—might face similar judgment?"
            ]
        },
        "21": {
            "analysis": "<strong>I will make thee a terror, and thou shalt be no more</strong>—בַּלָּהוֹת (ballāhôt, 'terrors/horrifying thing') describes Tyre as an object lesson of judgment. <strong>Though thou be sought for, yet shalt thou never be found again, saith the Lord GOD</strong>—The Hebrew תְבֻקְשִׁי וְלֹא־תִמָּצְאִי (tĕbuqshî wĕlōʾ-timmāṣĕʾî, 'you will be sought but not found') promises permanent erasure.<br><br>This is the divine signature: נְאֻם אֲדֹנָי יְהוִה (nĕʾum ʾădōnāy YHWH, 'utterance of the Lord GOD') sealing the prophecy. Ancient Tyre's magnificent civilization—described in chapter 27 as the perfection of beauty—would become a byword for judgment. Isaiah 23, Amos 1:9-10, Zechariah 9:3-4, and Jesus' own references (Matthew 11:21-22, Luke 10:13-14) all assume Tyre's destruction as historical fact. Archaeological excavations confirm: Phoenician Tyre's glory was systematically obliterated, first by Babylon, then completely by Alexander. The city exists but its ancient identity is irretrievable—precisely as prophesied.",
            "historical": "Phoenician Tyre was founded circa 2750 BC, making it one of antiquity's oldest cities. It pioneered maritime trade, invented purple dye, and spread the alphabet. At its peak, Tyre controlled Mediterranean commerce. Yet its pride brought judgment: 'sought for, yet never found again.' This prophecy, written 586 BC, came true by 332 BC.",
            "questions": [
                "How does Tyre becoming 'a terror' (cautionary tale) serve God's purposes?",
                "What does permanent loss of identity teach about valuing worldly achievement over God?",
                "How does Jesus' reference to Tyre's judgment (Matthew 11:21-22) apply to our accountability?"
            ]
        }
    },
    "27": {
        "29": {
            "analysis": "<strong>And all that handle the oar, the mariners, and all the pilots of the sea, shall come down from their ships</strong>—The lament for Tyre continues from verse 1. Those who תֹּפְשֵׂי מָשׁוֹט (tōphĕśê māshôṭ, 'handle the oar'), the חֹבְלִים (ḥōbĕlîm, 'sailors'), and כֹּל חֹבְלֵי הַיָּם (kōl ḥōbĕlê hayyām, 'all pilots of the sea') abandon ship.<br><br>This vivid imagery depicts maritime professionals—whose livelihood depends on sailing—leaving their vessels to stand on shore. It's an unnatural act, signaling the end of seafaring itself. When Tyre, the ancient world's commercial hub, falls, international trade collapses. Those who profited from Tyre's wealth watch helplessly as their economic system crumbles. Revelation 18:17-19 echoes this passage in describing Babylon's fall, showing the pattern of commercial empire collapse continues throughout history.",
            "historical": "Tyre's maritime dominance lasted over 1,000 years. Phoenician ships reached Britain for tin, circumnavigated Africa, and established Carthage. Tyrian purple dye and cedar wood were legendary. The city's commercial network spanned the known world (27:12-24). When Babylon besieged Tyre (585-573 BC), this economic empire began its collapse.",
            "questions": [
                "How do economic empires built on pride eventually face God's judgment?",
                "What does the image of sailors abandoning ships teach about the instability of worldly wealth?",
                "How does Revelation 18's echo of this passage apply to modern commercial powers?"
            ]
        },
        "30": {
            "analysis": "<strong>They shall stand upon the land; and shall cause their voice to be heard against thee, and shall cry bitterly</strong>—The maritime workers stand on אֶל־הָאָרֶץ (ʾel-hāʾāreṣ, 'on the land'), displaced from their natural element. They וְהִשְׁמִיעוּ עָלַיִךְ בְּקוֹלָם (wĕhishmîʿû ʿālayik bĕqôlām, 'cause to be heard upon you with their voice').<br><br>וְיִזְעֲקוּ מָרָה (wĕyizʿăqû mārāh, 'and they shall cry bitterly')—the verb זָעַק (zāʿaq) indicates anguished outcry, while מָרָה (mārāh, 'bitter') suggests grief mixed with despair. Their lament is both for Tyre and for their own livelihoods destroyed with her. Economic interdependence means Tyre's judgment cascades to all who benefited from her trade. This collective mourning demonstrates how one nation's pride and judgment affects entire regions—a principle seen when any economic superpower collapses.",
            "historical": "Ancient economies were less diversified than modern ones; Tyre's fall devastated Mediterranean commerce. Ezekiel 27:12-24 lists Tyre's trade partners: Tarshish (Spain), Greece, Tubal, Meshech, Togarmah, Dedan, Arabia, Sheba—a vast network. When the hub collapsed, the entire system suffered. Historical records show economic depression followed Babylon's campaigns.",
            "questions": [
                "How does economic interconnection mean one nation's sin affects many?",
                "What is the spiritual danger of building identity and security on commercial success?",
                "How should believers respond when economic systems they depend on face judgment?"
            ]
        },
        "31": {
            "analysis": "<strong>And they shall cast up dust upon their heads, they shall wallow themselves in the ashes</strong>—Ancient Near Eastern mourning rituals: וְהֶעֱלוּ עָפָר עַל־רָאשֵׁיהֶם (wĕheʿĕlû ʿāphār ʿal-rāshêhem, 'cast up dust upon their heads') and בָּאֵפֶר יִתְפַּלָּשׁוּ (bāʾēpher yitpallāshû, 'in ashes they shall wallow'). The verb פָּלַשׁ (pālash, 'to roll/wallow') suggests desperate, unrestrained grief.<br><br><strong>And they shall weep for thee with bitterness of heart and bitter wailing</strong>—The repetition of מָר (mār, 'bitter') intensifies the description: מַר־נֶפֶשׁ (mar-nephesh, 'bitter of soul') and מִסְפֵּד מָר (mispēd mār, 'bitter lamentation'). This is not polite mourning but visceral anguish. Yet their grief is selfish—they mourn lost profits, not lost souls; commercial opportunity, not covenant relationship. This contrasts sharply with godly grief over sin (2 Corinthians 7:10). Their 'bitter wailing' reveals the emptiness of lamenting judgment while remaining unchanged by it.",
            "historical": "Archaeological excavations at ancient sites show mourning customs: burial jars containing ashes, figurines depicting mourners with raised hands, texts describing professional mourners and elaborate funeral rites. In Phoenician culture, mourning rituals for national catastrophes were intense, public, and extended. Ezekiel's description matches historical records of ancient Mediterranean mourning practices.",
            "questions": [
                "What is the difference between mourning consequences and mourning sin itself?",
                "How does worldly grief differ from godly grief that leads to repentance?",
                "When have you mourned lost opportunities without addressing underlying spiritual issues?"
            ]
        },
        "32": {
            "analysis": "<strong>And in their wailing they shall take up a lamentation for thee, and lament over thee</strong>—The Hebrew נָשָׂא קִינָה (nāsāʾ qînāh, 'lift up a lament/dirge') refers to formal funeral songs. וְקוֹנְנוּ עָלַיִךְ (wĕqônĕnû ʿālayik, 'and they shall lament over you') uses the verb קוּן (qûn), meaning ritualized mourning.<br><br>This introduces the actual funeral dirge for Tyre (verses 32b-36), one of several in Ezekiel (19:1-14, 26:17-18, 27:32-36, 28:12-19, 32:2-16). The form mimics actual ancient funeral laments, with rhetorical questions, past glory recalled, and present devastation mourned. Biblical lament literature (Lamentations, select Psalms) serves theological purposes: acknowledging God's justice, confessing sin, and ultimately hoping in restoration. But Tyre's lament ends without hope—only permanent desolation.",
            "historical": "Ancient funeral dirges followed set patterns: invoking the deceased, recalling past glory, describing present ruin, and sometimes ending with hope. Professional mourners were hired for important deaths (Jeremiah 9:17-18). Ezekiel, as a priest, would have been familiar with liturgical lament forms and adapts them for prophetic purposes, showing God's judgment on nations follows similar patterns to human death.",
            "questions": [
                "How do biblical laments help believers process grief while maintaining faith in God?",
                "What is significant about Tyre's lament ending without hope of restoration?",
                "How should we 'lament' when God's judgment falls on proud systems or nations?"
            ]
        },
        "33": {
            "analysis": "<strong>Saying, What city is like Tyrus, like the destroyed in the midst of the sea?</strong>—The rhetorical question מִי כְצוֹר כַּדּוּמָה בְּתוֹךְ הַיָּם (mî khĕṣôr kaddûmāh bĕthôkh hayyām, 'who is like Tyre, like the silenced in the midst of the sea?') uses דּוּמָה (dûmāh, 'silence/desolation'), suggesting Tyre's voice is stilled forever.<br><br>This echoes laments over Babylon ('who is like Babylon?'—Revelation 18:18) and represents humanity's astonishment when seemingly invincible powers fall. Tyre appeared impregnable: island fortress, commercial dominance, wealth beyond measure. Yet God silenced her. The question highlights not just Tyre's uniqueness but the shock of her destruction—if mighty Tyre can fall, no human achievement is secure. Only God's kingdom is unshakable (Hebrews 12:27-28).",
            "historical": "Tyre's island location made it nearly impregnable to ancient siege warfare. It resisted Assyrian king Shalmaneser V for five years (724-720 BC) and Nebuchadnezzar for thirteen years (585-573 BC). Many doubted Tyre could fall. Yet Alexander the Great destroyed it in 332 BC by building a causeway from mainland to island—a feat considered impossible. The rhetorical question proved ironic: Tyre's uniqueness made her fall more stunning.",
            "questions": [
                "What modern powers seem 'like Tyre'—too established to fall?",
                "How does human shock at judgment reveal our false confidence in worldly security?",
                "What does Tyre's uniqueness-turned-vulnerability teach about pride?"
            ]
        },
        "34": {
            "analysis": "<strong>When thy wares went forth out of the seas, thou filledst many people</strong>—Tyre's commercial reach: עִזְבוֹנַיִךְ (ʿizbônayik, 'your merchandise') מִיַּמִּים (miyyammîm, 'from the seas') הִשְׂבַּעַתְּ עַמִּים רַבִּים (hisbaʿat ʿammîm rabbîm, 'satisfied many peoples'). The verb שָׂבַע (sābaʿ, 'to be satisfied/filled') suggests Tyre provided abundance.<br><br><strong>Thou didst enrich the kings of the earth with the multitude of thy riches and of thy merchandise</strong>—Tyre's wealth enriched monarchs: הֶעֱשַׁרְתְּ מַלְכֵי־אָרֶץ (heʿeshartĕ malkhê-ʾāreṣ, 'you made rich the kings of earth'). But wealth without worship, commerce without covenant, produces judgment. Tyre's error was self-sufficiency (28:2—'thou hast said, I am a God'). Prosperity became pride, trade became trust, wealth replaced worship. Her riches couldn't save her—highlighting that material abundance, while potentially good, becomes idolatrous when divorced from acknowledging God as ultimate provider (Deuteronomy 8:17-18).",
            "historical": "Tyre's commercial catalog (27:12-24) shows trade in silver, iron, tin, lead, slaves, horses, ivory, ebony, wine, wool, spices, gold, precious stones—virtually everything valuable in the ancient world. Kings relied on Tyrian goods and expertise. Solomon used Tyrian craftsmen for the temple (1 Kings 5:1-12). But this economic power bred spiritual pride that demanded judgment.",
            "questions": [
                "How can economic prosperity become spiritual poison if it leads to self-sufficiency?",
                "What is the difference between stewarding wealth for God's glory and trusting wealth as security?",
                "How should believers relate to commerce and wealth in light of Tyre's example?"
            ]
        },
        "35": {
            "analysis": "<strong>In the time when thou shalt be broken by the seas in the depths of the waters</strong>—The metaphor shifts: Tyre the magnificent ship is נִשְׁבַּרְתְּ מִיַּמִּים (nishbartĕ miyyammîm, 'broken by the seas') בְּמַעֲמַקֵּי־מָיִם (bĕmaʿămaqê-māyim, 'in the depths of waters'). The very element that enabled Tyre's prosperity—the sea—becomes her destroyer.<br><br><strong>Thy merchandise and all thy company in the midst of thee shall fall</strong>—מַעֲרָבֵךְ וְכָל־קְהָלֵךְ (maʿărābēkh wĕkhol-qĕhālēkh, 'your merchandise and all your assembly') נָפָלוּ (nāphālû, 'have fallen'). Total collapse: goods, sailors, merchants—all sink together. This imagery of a wrecked ship represents total systemic failure. Tyre's integrated economy, which seemed so sophisticated and resilient, proves vulnerable to God's judgment. The lesson: systems built on human pride rather than divine foundation are destined for catastrophic failure (Matthew 7:24-27).",
            "historical": "Maritime disasters were common in antiquity but rarely catastrophic to empires because trade networks were diversified. Tyre's uniqueness was that the city itself was the network's center. When the city fell, the entire system collapsed—like a modern financial crisis when the central bank fails. Ezekiel's ship metaphor captures this systemic interdependence and vulnerability.",
            "questions": [
                "How does the metaphor of Tyre as a wrecked ship illustrate total systemic collapse?",
                "What modern 'ships'—complex systems we trust—might be vulnerable to similar judgment?",
                "How do we avoid building our lives on systems destined for failure?"
            ]
        },
        "36": {
            "analysis": "<strong>The merchants among the people shall hiss at thee; thou shalt be a terror, and never shalt be any more</strong>—The final verse: סֹחֲרִים בָּעַמִּים (sōḥărîm bāʿammîm, 'traders among the peoples') שָׁרְקוּ עָלָיִךְ (shārĕqû ʿālayik, 'hiss at you'). The verb שָׁרַק (shāraq) indicates shocked derision, a hissing sound expressing horror and contempt (1 Kings 9:8, Jeremiah 19:8).<br><br><strong>Thou shalt be a terror</strong>—בַּלָּהוֹת הָיִית (ballāhôt hāyît, 'terrors you have become'), an object lesson of judgment. <strong>And never shalt be any more</strong>—וְאֵינֵךְ עַד־עוֹלָם (wĕʾênēkh ʿad-ʿôlām, 'and you are not until eternity'). This concludes the extended lament (chapters 26-28) with finality: Tyre's commercial glory is permanently ended. Those who profited from her trade now mock her—fair-weather friends revealed when prosperity ends. The chapter warns against building identity on economic achievement, participating in systems built on pride, or trusting wealth for security. Only God's kingdom endures; all else is vapor (James 4:14).",
            "historical": "Ezekiel 26-28 was written circa 586 BC. Babylon besieged Tyre 585-573 BC. Alexander destroyed it completely 332 BC. By Roman times, Tyre was a minor port. Today, it's a small Lebanese city with ancient ruins—literally 'a terror and never shall be any more' as a commercial empire. The prophecy's fulfillment over centuries demonstrates God's sovereignty over history.",
            "questions": [
                "Why do those who profited from a system mock it when it falls?",
                "What does Tyre becoming 'a terror'—a cautionary example—teach subsequent generations?",
                "How should believers invest their lives to avoid Tyre's fate of building on temporal foundations?"
            ]
        }
    }
}

# Save the first batch
print("Commentary batch 1 ready: Chapters 21-22, 24, 26-27")
print(json.dumps(COMMENTARY, indent=2))
