#!/usr/bin/env python3
"""Bulk add commentary for Amos and John missing verses."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

def merge_commentary(book_slug, new_entries):
    """Merge new commentary entries into existing file."""
    filepath = DATA_DIR / f"{book_slug}.json"

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    commentary = data.get("commentary", {})
    added_count = 0

    # Merge new entries
    for chapter, verses in new_entries.items():
        if chapter not in commentary:
            commentary[chapter] = {}
        for verse, entry in verses.items():
            if verse not in commentary[chapter]:
                commentary[chapter][verse] = entry
                added_count += 1
                print(f"Added {data['book']} {chapter}:{verse}")

    data["commentary"] = commentary

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nAdded {added_count} verses to {filepath}\n")
    return added_count

# AMOS COMMENTARY
amos_commentary = {
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
            "analysis": "In this verse detailing Moab's coming judgment, three classes of warriors prove helpless: <strong>he that handleth the bow</strong> (תֹּפֵשׂ הַקֶּשֶׁת, <em>tofes haqeshet</em>, the archer), <strong>he that is swift of foot</strong> (קַל בְּרַגְלָיו, <em>qal b'raglav</em>, literally 'light in his feet'), and <strong>he that rideth the horse</strong> (רֹכֵב הַסּוּס, <em>rochev hasus</em>, the cavalry). The threefold repetition—'shall not deliver himself' (לֹא יְמַלֵּט, <em>lo yemalet</em>)—hammers home human inability to escape divine judgment.<br><br>Ancient warfare relied on these three military advantages: long-range attack (archers), speed (runners for messages and retreat), and mobile power (cavalry). Yet when God judges, no human strategy suffices. This prefigures Romans 8:33—when God justifies, who can condemn? Conversely, when God condemns, no created thing can deliver.",
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
    },
    "3": {
        "8": {
            "analysis": "<strong>The lion hath roared, who will not fear?</strong> (אַרְיֵה שָׁאָג מִי לֹא יִירָא, <em>aryeh sha'ag mi lo yira</em>)—Amos uses rhetorical questions to establish cause and effect. The lion's roar (שָׁאָג, <em>sha'ag</em>) triggers instinctive fear; similarly, <strong>the Lord GOD hath spoken, who can but prophesy?</strong> (אֲדֹנָי יְהוִה דִּבֶּר מִי לֹא יִנָּבֵא, <em>Adonai YHWH diber mi lo yinave</em>). When God speaks (דִּבֶּר, <em>diber</em>), the prophet cannot remain silent—prophecy becomes compulsion, not career choice.<br><br>This defends Amos's prophetic authority against critics. He prophesies not from presumption but necessity—God has spoken, therefore he must speak. The same compulsion drove Peter and John: 'We cannot but speak the things which we have seen and heard' (Acts 4:20). True preaching flows from divine encounter, not human agenda.",
            "historical": "Amos spoke this around 760 BC when confronted by Amaziah the priest at Bethel (Amos 7:10-17), who commanded him to stop prophesying. Amos wasn't a professional prophet but a shepherd whom God seized and sent. This verse justifies his divine commission despite lacking formal prophetic credentials.",
            "questions": [
                "How does this verse challenge the modern view of preaching as profession rather than prophetic compulsion?",
                "When was the last time God's Word created such urgency in you that you couldn't remain silent?",
                "What does it mean for the church when preachers speak from personal wisdom rather than 'the Lord GOD hath spoken'?"
            ]
        },
        "9": {
            "analysis": "<strong>Publish in the palaces at Ashdod, and in the palaces in the land of Egypt</strong>—God summons pagan nations as witnesses against Israel's sin. The Hebrew הַשְׁמִיעוּ (<em>hashmi'u</em>, 'proclaim, announce publicly') demands widespread proclamation. Ashdod (Philistine city) and Egypt (Israel's former oppressor) represent notorious wickedness, yet even they will be shocked by <strong>the great tumults</strong> (מְהוּמֹת רַבּוֹת, <em>mehumot rabot</em>, 'great confusion/chaos') and <strong>the oppressed</strong> (עֲשׁוּקִים, <em>ashuqim</em>, 'the oppressed/exploited') within Samaria.<br><br>This is devastating irony: Israel, called to be holy and distinct (Exodus 19:6), has become morally inferior to pagans. When God calls the wicked to witness against His people, judgment is certain. Similarly, Jesus said Sodom and Gomorrah would fare better than cities that rejected Him (Matthew 11:23-24).",
            "historical": "Samaria was Israel's capital, built by Omri (1 Kings 16:24) and famous for wealth and wickedness. By 760 BC, the Northern Kingdom's prosperity under Jeroboam II masked systemic injustice—the rich oppressing the poor while maintaining religious ritual. Archaeological excavations reveal luxury goods and elaborate architecture alongside evidence of extreme economic disparity.",
            "questions": [
                "How should it convict us when secular society recognizes injustice that religious people ignore or perpetuate?",
                "What 'tumults' and 'oppression' might be visible in churches or Christian communities today?",
                "Why does prosperity often blind religious people to their own sin and social injustice?"
            ]
        },
        "10": {
            "analysis": "<strong>They know not to do right</strong> (וְלֹא־יָדְעוּ עֲשׂוֹת־נְכֹחָה, <em>v'lo yad'u asot n'chochah</em>)—The Hebrew יָדְעוּ (<em>yad'u</em>, 'to know') implies not mere intellectual ignorance but moral corruption; they've lost the capacity to recognize righteousness. The word נְכֹחָה (<em>n'chochah</em>, 'right, straight, honest') contrasts with their crooked dealings. <strong>Who store up violence and robbery in their palaces</strong> (הָאוֹצְרִים חָמָס וָשֹׁד בְּאַרְמְנוֹתֵיהֶם, <em>ha'otz'rim chamas v'shod b'armenoteihem</em>)—their wealth is 'stored up' violence (חָמָס, <em>chamas</em>) and plunder (שֹׁד, <em>shod</em>).<br><br>This indicts economic systems built on exploitation. Their palaces—symbols of success—are actually warehouses of injustice. James 5:1-6 echoes this: the wages of defrauded workers cry out to God. When injustice becomes normalized, people lose moral clarity entirely.",
            "historical": "During Jeroboam II's reign (793-753 BC), Israel experienced unprecedented prosperity through military expansion and trade. The wealthy elite accumulated luxury goods through predatory lending, land seizure, and corrupt courts. Amos confronts this 'prosperity gospel'—wealth divorced from justice proves spiritual bankruptcy.",
            "questions": [
                "How might modern Christians 'store up violence and robbery' through economic systems we benefit from but don't examine?",
                "What does it mean to lose the ability to recognize what is right due to cultural or economic complicity in injustice?",
                "How can churches today avoid confusing material prosperity with God's blessing when it's built on exploitation?"
            ]
        },
        "11": {
            "analysis": "<strong>An adversary there shall be even round about the land</strong> (צַר וּסְבִיב הָאָרֶץ, <em>tzar us'viv ha'aretz</em>)—The enemy surrounds them completely; no escape remains. The term צַר (<em>tzar</em>, 'adversary, enemy, distress') appears with geographical emphasis: וּסְבִיב (<em>us'viv</em>, 'all around'). <strong>He shall bring down thy strength from thee</strong> (וְהוֹרִיד מִמֵּךְ עֻזֵּךְ, <em>v'horid mimech uzech</em>)—their military power (עֻזֵּךְ, <em>uzech</em>) will be 'brought down' (הוֹרִיד, <em>horid</em>, literally 'caused to descend'). <strong>Thy palaces shall be spoiled</strong> (וְנָבֹזּוּ אַרְמְנוֹתַיִךְ, <em>v'navozu armenotayich</em>)—plundered completely.<br><br>This reverses Israel's covenant promises. God promised protection from enemies (Leviticus 26:6-8), but covenant-breaking brings covenant curses (Leviticus 26:14-17). The Assyrian invasion of 722 BC fulfilled this literally—Samaria fell after three-year siege, and the nation never recovered.",
            "historical": "In 724 BC, Shalmaneser V of Assyria besieged Samaria; his successor Sargon II completed the conquest in 722 BC. The Assyrians deported 27,290 Israelites according to Assyrian records, replacing them with foreign peoples (2 Kings 17:5-6, 24). The Northern Kingdom ceased to exist—fulfilling Amos's prophecy exactly.",
            "questions": [
                "How does breaking covenant with God remove His protection and guarantee judgment?",
                "What false securities—military might, economic power, political alliances—do nations trust in today?",
                "How should the certainty of God's judgment against covenant-breaking inform Christian faithfulness in our generation?"
            ]
        },
        "12": {
            "analysis": "The shepherd metaphor is devastatingly ironic: <strong>As the shepherd taketh out of the mouth of the lion two legs, or a piece of an ear</strong> (כַּאֲשֶׁר יַצִּיל הָרֹעֶה מִפִּי הָאַרְיֵה, <em>ka'asher yatzil haro'eh mipi ha'aryeh</em>)—these aren't rescued sheep but proof of death for the shepherd's legal defense (Exodus 22:13). Similarly, <strong>so shall the children of Israel be taken out</strong> (כֵּן יִנָּצְלוּ בְנֵי־יִשְׂרָאֵל, <em>ken yinatz'lu b'nei yisrael</em>)—a remnant survives, but barely. <strong>In the corner of a bed, and in Damascus in a couch</strong> describes luxury furniture fragments—all that remains of their opulence.<br><br>The Hebrew יִנָּצְלוּ (<em>yinatz'lu</em>) typically means 'delivered/rescued,' but here it's bitterly ironic: they're 'delivered' only as evidence of destruction. Like torn sheep parts, Israel will be reduced to fragments—a warning that affluence cannot protect from judgment.",
            "historical": "This prophecy was fulfilled multiply: the Assyrian conquest left only remnants, the Babylonian exile scattered survivors, and even today the ten northern tribes remain 'lost.' The reference to Damascus (Syria) and luxury couches emphasizes that those trusting in wealth and political alliances would be first to suffer.",
            "questions": [
                "How does this verse challenge the modern belief that material prosperity indicates God's favor?",
                "What does it mean to be 'saved' yet only as a fragment—bearing permanent marks of judgment?",
                "How should the reality of judgment as a consuming 'lion' shape Christian urgency in evangelism?"
            ]
        },
        "13": {
            "analysis": "<strong>Hear ye, and testify in the house of Jacob</strong> (שִׁמְעוּ וְהָעִידוּ בְּבֵית יַעֲקֹב, <em>shim'u v'ha'idu b'veit ya'akov</em>)—The Hebrew הָעִידוּ (<em>ha'idu</em>, 'testify, bear witness') is legal language; God calls witnesses against His people. The use of 'Jacob' rather than 'Israel' may emphasize their unchanged carnal nature—still deceivers like their ancestor. <strong>Saith the Lord GOD, the God of hosts</strong> (נְאֻם אֲדֹנָי יְהוִה אֱלֹהֵי הַצְּבָאוֹת, <em>ne'um Adonai YHWH Elohei hatzva'ot</em>)—triple divine titles underscore absolute authority.<br><br>This courtroom scene portrays God prosecuting His covenant lawsuit (<em>riv</em>) against Israel. The same God who delivered them now testifies against them—a tragic reversal. Yet even in judgment, God calls witnesses, maintaining judicial righteousness rather than acting as arbitrary tyrant.",
            "historical": "The covenant lawsuit (prophetic riv) was a standard Ancient Near Eastern legal form. God isn't violating His covenant but enforcing it through its curse provisions (Deuteronomy 28-29). This public witness ensures Israel cannot claim ignorance or injustice when judgment falls.",
            "questions": [
                "How does God's use of legal process even in judgment display His righteousness and patience?",
                "What does it mean that God testifies against His own people—those who bear His name?",
                "How should churches today respond when God's Word testifies against their practices?"
            ]
        },
        "14": {
            "analysis": "<strong>In the day that I shall visit the transgressions of Israel upon him</strong> (בְּיוֹם פָּקְדִי פִשְׁעֵי־יִשְׂרָאֵל עָלָיו, <em>b'yom pokdi pish'ei yisrael alav</em>)—The verb פָּקַד (<em>pakad</em>, 'visit, attend to, punish') appears frequently in judgment contexts; God's 'visitation' brings reckoning. <strong>I will also visit the altars of Beth-el</strong> (וּפָקַדְתִּי עַל־מִזְבְּחוֹת בֵּית־אֵל, <em>ufakadti al-mizbechot beit-el</em>)—Bethel's golden calf altar, established by Jeroboam I (1 Kings 12:28-29), epitomized Israel's syncretistic worship. <strong>The horns of the altar shall be cut off</strong> (וְנִגְדְּעוּ קַרְנוֹת הַמִּזְבֵּחַ, <em>v'nigde'u karnot hamizbeach</em>)—altar horns provided sanctuary (1 Kings 1:50), but now even that refuge is destroyed.<br><br>The cutting off of altar horns symbolizes judgment reaching even sacred spaces. No false worship, religious tradition, or holy place can protect covenant-breakers. This prefigures Christ's prophecy that Jerusalem's temple would be destroyed (Matthew 24:1-2)—structures of false confidence collapse under divine judgment.",
            "historical": "Bethel ('House of God') was where Jacob encountered God (Genesis 28:19), making Jeroboam's idolatry there particularly blasphemous. This sanctuary became the center of Israel's apostate worship. In 722 BC, the Assyrians destroyed these altars; Josiah later desecrated the site completely (2 Kings 23:15-16).",
            "questions": [
                "What false refuges—religious traditions, church buildings, rituals—do people trust instead of Christ alone?",
                "How does God's judgment on religious institutions that bear His name warn contemporary churches?",
                "In what ways might modern Christians be like Israel—maintaining religious forms while living in covenant unfaithfulness?"
            ]
        },
        "15": {
            "analysis": "<strong>I will smite the winter house with the summer house</strong> (וְהִכֵּיתִי בֵית־הַחֹרֶף עַל־בֵּית הַקָּיִץ, <em>v'hikeiti beit-hachoref al-beit hakayitz</em>)—The wealthy maintained separate residences for different seasons; winter houses were typically in valleys, summer houses on cool heights. God will strike both simultaneously. <strong>The houses of ivory shall perish</strong> (וְאָבְדוּ בָּתֵּי הַשֵּׁן, <em>v'avdu batei hashen</em>, literally 'houses of tooth/ivory')—ivory inlays represented extreme luxury (1 Kings 22:39 mentions Ahab's ivory house). <strong>The great houses shall have an end</strong> (וְסָפוּ בָּתִּים רַבִּים, <em>v'safu batim rabim</em>)—utter destruction.<br><br>This passage condemns not wealth itself but wealth gained through oppression (Amos 3:10) and maintained through indifference to poverty (Amos 6:4-6). Jesus echoed this in the parable of the rich fool (Luke 12:16-21)—accumulated luxury without God is death. Archaeological excavations at Samaria confirm extensive ivory decorations, fulfilling this prophecy's specificity.",
            "historical": "The Northern Kingdom's aristocracy lived in unprecedented luxury during Jeroboam II's reign. Ivory fragments discovered at Samaria (1931-1935 excavations) confirm palace opulence. When Assyria conquered in 722 BC, these houses were destroyed—the wealthy who trusted in comfort experienced the judgment they'd ignored.",
            "questions": [
                "How does having multiple homes or excessive luxury while others suffer represent covenant unfaithfulness?",
                "What 'houses of ivory'—symbols of accumulated comfort—might blind Christians today to injustice and coming judgment?",
                "How can believers hold wealth and possessions with open hands, recognizing they belong to God and will not endure?"
            ]
        }
    }
}

# This file is getting large - will continue in parts
print("Processing Amos commentary...")
amos_count = merge_commentary("amos", amos_commentary)
print(f"Total Amos verses added: {amos_count}\n")
