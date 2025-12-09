#!/usr/bin/env python3
"""Add remaining Amos commentary - Chapters 4-9."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

filepath = DATA_DIR / "amos.json"
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

commentary = data.get("commentary", {})

# Remaining Amos commentary
new_entries = {
    "4": {
        "13": {
            "analysis": "This doxology proclaims Yahweh's cosmic sovereignty: <strong>He that formeth the mountains</strong> (יֹצֵר הָרִים, <em>yotzer harim</em>)—the participle emphasizes continuous creative power. <strong>And createth the wind</strong> (וּבֹרֵא רוּחַ, <em>uvore ruach</em>)—רוּחַ (<em>ruach</em>) means both 'wind' and 'spirit,' suggesting God's control over both physical and spiritual realms. <strong>And declareth unto man what is his thought</strong> (וּמַגִּיד לְאָדָם מַה־שֵּׂחוֹ, <em>umagid l'adam mah-secho</em>)—God reveals His purposes to humans through prophetic revelation. <strong>That maketh the morning darkness</strong> (עֹשֶׂה שַׁחַר עֵיפָה, <em>oseh shachar eifah</em>)—He controls day and night. <strong>And treadeth upon the high places of the earth</strong> (וְדֹרֵךְ עַל־בָּמֳתֵי אָרֶץ, <em>v'dorech al-bamotei aretz</em>)—walking on earth's high places demonstrates absolute authority. <strong>The LORD, The God of hosts, is his name</strong> (יְהוָה אֱלֹהֵי־צְבָאוֹת שְׁמוֹ, <em>YHWH Elohei-tzva'ot sh'mo</em>).<br><br>This hymnic interruption follows severe judgment oracles, reminding Israel who they're resisting. The God who judges is the Creator-Sustainer of all reality. Similar doxologies appear in Amos 5:8-9 and 9:5-6, structuring the book around God's cosmic majesty—rebellion against such a God guarantees destruction.",
            "historical": "These doxological fragments may derive from ancient Israelite hymns. Their placement after judgment oracles serves theological purpose: reminding hearers that Amos speaks for the sovereign Creator, not merely offering political opinion. The phrases echo creation language from Genesis and anticipate New Testament Christology (Colossians 1:15-17).",
            "questions": [
                "How does recognizing God as Creator of mountains and wind humble human pride and self-sufficiency?",
                "What does it mean that the same God who reveals His thoughts is also the God who judges sin?",
                "How should God's cosmic sovereignty shape our understanding of His authority to judge nations and individuals?"
            ]
        }
    },
    "5": {
        "25": {
            "analysis": "<strong>Have ye offered unto me sacrifices and offerings in the wilderness forty years, O house of Israel?</strong> (הַזְּבָחִים וּמִנְחָה הִגַּשְׁתֶּם־לִי בַמִּדְבָּר, <em>hazevachim uminchah higashtem-li bamidbar</em>)—This rhetorical question expects 'no' as the answer. During the wilderness wandering (Exodus-Deuteronomy), Israel frequently rebelled rather than worshiped. The Hebrew construction emphasizes the pronoun לִי (<em>li</em>, 'to ME')—even when they performed rituals, their hearts weren't directed toward Yahweh but toward idols (Acts 7:42-43 confirms this interpretation).<br><br>God isn't merely criticizing ritual hypocrisy but exposing deep-rooted idolatry spanning generations. The wilderness generation set a pattern: outward religious conformity masking inward rebellion. This challenges any presumption of covenant faithfulness based on ritual performance rather than heart devotion.",
            "historical": "Stephen cited this verse in Acts 7:42-43, interpreting it to mean Israel carried idols even in the wilderness. The golden calf incident (Exodus 32) and subsequent rebellions confirm persistent idolatry. Amos addresses 8th-century Israel by reminding them their ancestors' pattern of faithlessness.",
            "questions": [
                "How might modern Christians maintain religious rituals while their hearts worship other gods—success, comfort, reputation?",
                "What does it mean to offer sacrifices 'unto me' versus performing religious duties without heart engagement?",
                "How does this verse challenge generational assumptions of faithfulness based on religious heritage rather than genuine devotion?"
            ]
        },
        "26": {
            "analysis": "<strong>But ye have borne the tabernacle of your Moloch and Chiun your images</strong> (וּנְשָׂאתֶם אֵת סִכּוּת מַלְכְּכֶם וְאֵת כִּיּוּן צַלְמֵיכֶם, <em>un'satem et sikkut malkechem v'et kiyun tzalmeichem</em>)—Moloch (מֹלֶךְ, <em>molech</em>) was the Ammonite deity requiring child sacrifice; Chiun/Kiyyun (כִּיּוּן, <em>kiyun</em>) likely refers to a star deity, possibly Saturn. <strong>The star of your god, which ye made to yourselves</strong> (כּוֹכַב אֱלֹהֵיכֶם אֲשֶׁר עֲשִׂיתֶם לָכֶם, <em>kochav eloheichem asher asitem lachem</em>)—they created gods with their own hands, inverting the Creator-creature relationship.<br><br>Idolatry always involves exchanging the truth of God for a lie (Romans 1:25), worshiping and serving the creature rather than the Creator. The reference to carrying these idols suggests Israel transported them during wilderness wandering and continued this practice in Canaan—syncretism spanning generations.",
            "historical": "Acts 7:43 translates differently: 'Remphan' instead of 'Chiun,' following the Septuagint. Both refer to astral deities. Canaanite religion featured star worship, and Israel repeatedly fell into this syncretism (Deuteronomy 4:19; 2 Kings 23:5). Amos exposes how Israel's worship mixed Yahwism with paganism.",
            "questions": [
                "What modern 'stars' or celebrities do people worship instead of God—following them, imitating them, trusting their wisdom?",
                "How does making our own gods—through selective theology or cultural accommodation—repeat Israel's error?",
                "Why is syncretism (mixing true worship with false) more dangerous than outright paganism?"
            ]
        },
        "27": {
            "analysis": "<strong>Therefore will I cause you to go into captivity beyond Damascus</strong> (וְהִגְלֵיתִי אֶתְכֶם מֵהָלְאָה לְדַמָּשֶׂק, <em>v'higleiti etchem mehale'ah l'Damaseq</em>)—The judgment fits the crime: they carried idols, so God will cause them to be carried away (הִגְלֵיתִי, <em>higleiti</em>, 'I will exile'). <strong>Beyond Damascus</strong> means further than Syria—fulfilled when Assyria (whose capital Nineveh lay northeast of Damascus) deported Israel in 722 BC. <strong>Saith the LORD, whose name is The God of hosts</strong> (אָמַר יְהוָה אֱלֹהֵי־צְבָאוֹת שְׁמוֹ, <em>amar YHWH Elohei-tzva'ot sh'mo</em>)—the covenant God who commands heavenly armies pronounces this irrevocable decree.<br><br>This is measure-for-measure justice: they wanted other gods, so God removes them from the promised land given specifically for worshiping Him alone. Exile is the covenant curse for idolatry (Deuteronomy 28:36, 64-68). Yet even in judgment, God maintains covenant faithfulness—He warned them repeatedly before acting.",
            "historical": "The Assyrian conquest of 722 BC fulfilled this precisely. Sargon II deported Israelites to Mesopotamia and Media (2 Kings 17:6)—regions 'beyond Damascus.' The ten northern tribes never returned as a nation, becoming the 'lost tribes.' This demonstrates God's faithfulness to His word, even in judgment.",
            "questions": [
                "How does exile function as both punishment and mercy—removing people from covenant blessings they despised?",
                "What modern forms of 'exile' might God use to discipline His people when they pursue idols?",
                "How should the certainty of God's judgment encourage Christians to take warnings seriously rather than presuming on grace?"
            ]
        }
    },
    "6": {
        "2": {
            "analysis": "<strong>Pass ye unto Calneh, and see; and from thence go ye to Hamath the great: then go down to Gath of the Philistines</strong>—God commands Israel to examine three conquered cities as object lessons. Calneh (Assyrian Kullani) fell to Tiglath-Pileser III around 738 BC. Hamath (Syrian city) was defeated by Assyria circa 720 BC. Gath (Philistine city) had been conquered by Uzziah of Judah (2 Chronicles 26:6). <strong>Be they better than these kingdoms? or their border greater than your border?</strong> (הֲטוֹבִים מִן־הַמַּמְלָכוֹת הָאֵלֶּה, <em>hatovim min-hamamlachot ha'eleh</em>)—rhetorical question: if these great cities fell, what makes Israel think they're immune?<br><br>This confronts nationalistic pride and false security. Israel trusted in their covenant status, but covenant unfaithfulness removes covenant protection. If powerful nations fell to judgment, covenantbreakers will fare no better. Peter echoes this: 'judgment must begin at the house of God' (1 Peter 4:17).",
            "historical": "Amos likely prophesied this between 760-750 BC, before some of these cities fell—making it a genuine prophecy. Israel's complacency during prosperous times blinded them to approaching judgment. They thought their election guaranteed safety, but election without obedience brings greater accountability (Amos 3:2).",
            "questions": [
                "What forms of false security—national identity, church membership, religious heritage—do people trust instead of genuine faith?",
                "How does examining other fallen nations or churches warn against presumption on God's patience?",
                "Why do prosperous times often breed spiritual complacency and blindness to approaching judgment?"
            ]
        },
        "3": {
            "analysis": "<strong>Ye that put far away the evil day</strong> (הַמְנַדִּים לְיוֹם רָע, <em>hamenadim l'yom ra</em>)—they mentally distance themselves from coming judgment, assuming it won't arrive. The Hebrew נָדָה (<em>nadah</em>) means 'to remove, put at a distance.' <strong>And cause the seat of violence to come near</strong> (וַתַּגִּישׁוּן שֶׁבֶת חָמָס, <em>vatagishun shevet chamas</em>)—while pushing judgment away, they bring violent oppression near. שֶׁבֶת (<em>shevet</em>, 'seat, throne') suggests enthroned violence—injustice institutionalized in their society.<br><br>This describes psychological denial: people suppress awareness of judgment while embracing the very sins that guarantee it. Romans 2:4-5 warns against despising God's patience, storing up wrath. The more people distance themselves from judgment mentally, the closer they bring it actually through continued sin.",
            "historical": "Israel's prosperity under Jeroboam II created illusion of divine favor despite systemic injustice. The wealthy oppressed the poor while assuming covenant status protected them. This cognitive dissonance—ignoring warnings while multiplying sins—typifies pre-judgment societies throughout Scripture.",
            "questions": [
                "How do modern people 'put far away the evil day' by dismissing biblical warnings about judgment?",
                "What does it mean to have violence 'enthroned' in society—normalized, legalized, institutionalized?",
                "How can churches avoid the trap of assuming God's patience means approval rather than opportunity for repentance?"
            ]
        },
        "4": {
            "analysis": "<strong>That lie upon beds of ivory</strong> (הַשֹּׁכְבִים עַל־מִטּוֹת שֵׁן, <em>hashochevim al-mitot shen</em>)—ivory-inlaid beds represented extreme luxury in the ancient world. <strong>And stretch themselves upon their couches</strong> (וּסְרֻחִים עַל־עַרְשׂוֹתָם, <em>useruchim al-arsotam</em>)—the verb סָרַח (<em>sarach</em>) implies sprawling indolently. <strong>And eat the lambs out of the flock, and the calves out of the midst of the stall</strong>—consuming the choicest meat without concern for cost or scarcity. This isn't merely enjoying God's blessings but self-indulgent luxury while others starve.<br><br>The condemnation isn't wealth per se but indifference: <strong>they are not grieved for the affliction of Joseph</strong> (Amos 6:6). They feast while their brothers suffer, displaying the same cold self-absorption as Dives ignoring Lazarus (Luke 16:19-31). Luxury that breeds apathy toward suffering is sin.",
            "historical": "Archaeological excavations at Samaria uncovered ivory fragments from palace decorations, confirming the biblical account. The Northern Kingdom's aristocracy lived in opulence while exploiting the poor through unjust courts, predatory lending, and land seizure—wealth built on others' suffering.",
            "questions": [
                "How might modern Christians live in ivory-bed comfort while remaining indifferent to brothers and sisters suffering persecution or poverty?",
                "What does it mean to consume 'the choicest' of everything while others lack basics—is this stewardship or self-indulgence?",
                "How can believers cultivate grief over others' affliction rather than insulating ourselves in comfortable isolation?"
            ]
        },
        "5": {
            "analysis": "<strong>That chant to the sound of the viol</strong> (הַפֹּרְטִים עַל־פִּי הַנָּבֶל, <em>haforetim al-pi hanavel</em>)—פָּרַט (<em>parat</em>) means to improvise or play frivolously. <strong>And invent to themselves instruments of musick, like David</strong> (חָשְׁבוּ לָהֶם כְּלֵי־שִׁיר כְּדָוִיד, <em>chashvu lahem klei-shir k'David</em>)—they compare their frivolous entertainment to David's sacred psalmody. This isn't condemning music but mocking their pretension: they think their drunken songs equal David's Spirit-inspired worship.<br><br>The sin is twofold: trivializing worship by equating entertainment with praise, and remaining absorbed in pleasure while the nation faces judgment. Like those on the Titanic playing music as the ship sank, they feast and sing while catastrophe approaches. Revelation 18:22 pronounces similar judgment on Babylon—music ceases when God judges.",
            "historical": "David invented musical instruments for temple worship (2 Chronicles 7:6). Israel's elite perverted this legacy, using music for self-indulgent entertainment rather than God-honoring worship. They maintained religious forms while hearts pursued pleasure—form without power (2 Timothy 3:5).",
            "questions": [
                "How might modern worship music focus more on entertainment and emotional experience than genuine encounter with God?",
                "What does it mean to remain absorbed in entertainment and leisure while the church or world faces crisis?",
                "How can Christians discern between enjoying God's gifts (music, food, comfort) and self-indulgent excess that blinds us to others' needs?"
            ]
        },
        "6": {
            "analysis": "<strong>That drink wine in bowls</strong> (הַשֹּׁתִים בְּמִזְרְקֵי יַיִן, <em>hashotim b'mizrekei yayin</em>)—מִזְרָק (<em>mizrak</em>) typically refers to large ceremonial bowls used in temple service for catching sacrificial blood (Exodus 27:3). Drinking wine from such vessels suggests either mocking sacred objects or consuming alcohol in enormous quantities. <strong>And anoint themselves with the chief ointments</strong> (וְרֵאשִׁית שְׁמָנִים יִמְשָׁחוּ, <em>v'reishit shemanim yimshahu</em>)—using premium oils for personal luxury. <strong>But they are not grieved for the affliction of Joseph</strong> (וְלֹא נֶחְלוּ עַל־שֵׁבֶר יוֹסֵף, <em>v'lo nechlu al-shever Yosef</em>)—the verb חָלָה (<em>chalah</em>) means 'to be sick, grieved, wounded.' They feel no pain over their nation's brokenness (שֵׁבֶר, <em>shever</em>, 'fracture, ruin').<br><br>'Joseph' represents the northern tribes (descendants of Joseph's sons Ephraim and Manasseh). While the nation fractures morally and spiritually, the elite remain absorbed in luxury and entertainment. This lack of grief over sin is itself sin—demonstrating hardened hearts impervious to conviction.",
            "historical": "This describes Israel's aristocracy in the mid-8th century BC. Despite systemic injustice, religious apostasy, and looming Assyrian threat, the wealthy remained self-absorbed. Their callousness toward 'Joseph's affliction' meant indifference to their own people's suffering—the ultimate covenant betrayal.",
            "questions": [
                "How do modern Christians numb themselves to the 'affliction of Joseph'—the suffering church worldwide?",
                "What does it mean to grieve over sin and brokenness rather than merely maintaining comfort and entertainment?",
                "How can believers cultivate spiritual sensitivity rather than the callousness that luxury often breeds?"
            ]
        },
        "7": {
            "analysis": "<strong>Therefore now shall they go captive with the first that go captive</strong> (לָכֵן עַתָּה יִגְלוּ בְּרֹאשׁ גֹּלִים, <em>lachen atah yiglu v'rosh golim</em>)—the phrase בְּרֹאשׁ גֹּלִים (<em>v'rosh golim</em>, 'at the head of exiles') means they'll be first deported. The leaders in luxury become leaders in exile. <strong>And the banquet of them that stretched themselves shall be removed</strong> (וְסָר מִרְזַח סְרוּחִים, <em>v'sar mirzach seruchim</em>)—מִרְזֵחַ (<em>mirzeach</em>) refers to funeral feasts or revelry; their parties end abruptly.<br><br>This is poetic justice: those who lived most comfortably suffer most severely in judgment. Jesus taught similar reversal: 'many that are first shall be last' (Matthew 19:30). Privilege without responsibility, comfort without compassion, leadership without integrity—all bring greater accountability (Luke 12:48).",
            "historical": "When Assyria conquered Samaria in 722 BC, they deported the leadership and aristocracy first—standard ancient Near Eastern practice. The wealthy elite who ignored warnings experienced the judgment they dismissed. Archaeological evidence confirms Samaria's destruction and deportation of its upper classes.",
            "questions": [
                "How does greater privilege bring greater responsibility and potentially greater judgment?",
                "What 'banquets' or comforts might God remove to discipline His people and wake them from spiritual apathy?",
                "How should Christian leaders respond to this warning about being 'first' in judgment if they lead in unfaithfulness?"
            ]
        },
        "8": {
            "analysis": "<strong>The Lord GOD hath sworn by himself</strong> (נִשְׁבַּע אֲדֹנָי יְהוִה בְּנַפְשׁוֹ, <em>nishba Adonai YHWH b'nafsho</em>, literally 'sworn by His soul/life')—when God swears by Himself, the oath is irrevocable (Hebrews 6:13-18). <strong>I abhor the excellency of Jacob, and hate his palaces</strong> (תֹּעֵב אָנֹכִי אֶת־גְּאוֹן יַעֲקֹב וְאַרְמְנֹתָיו שָׂנֵאתִי, <em>toev anochi et-ge'on Ya'akov v'armenotav saneti</em>)—the Hebrew intensifies with both 'abhor' (תָּעַב, <em>ta'av</em>) and 'hate' (שָׂנֵא, <em>sane</em>). גְּאוֹן (<em>ge'on</em>, 'pride, excellency') here means arrogant self-sufficiency, not legitimate glory. <strong>Therefore will I deliver up the city with all that is therein</strong>—total destruction.<br><br>This shocking statement—God abhors and hates His covenant people—demonstrates how sin transforms blessing into curse. Their 'excellency' (covenant status, prosperity) became pride; their palaces (symbols of success) became monuments to oppression. When people pervert God's gifts into idols, He turns against even His own people (Isaiah 1:14).",
            "historical": "Samaria's fall in 722 BC fulfilled this oath. The city God once blessed became the object of His judgment. This demonstrates covenant faithfulness: God keeps His word for blessing or curse, depending on Israel's obedience (Deuteronomy 28).",
            "questions": [
                "How can God's covenant people become objects of His abhorrence through persistent sin and pride?",
                "What 'excellency' or 'palaces'—church buildings, programs, reputations—might God hate if they're built on compromise?",
                "Why is God's oath by Himself both terrifying (guaranteeing judgment) and comforting (guaranteeing salvation through Christ)?"
            ]
        },
        "9": {
            "analysis": "<strong>And it shall come to pass, if there remain ten men in one house, that they shall die</strong>—This describes plague or siege warfare's aftermath. Even survivors in a single household will perish. The number 'ten' may reference a עֲשָׂרָה (<em>asarah</em>, 'ten,' a traditional quorum for Jewish prayer), suggesting even complete families or communities won't escape. This verse continues the relentless depiction of total judgment—no remnant preserved, no survivors exempted.<br><br>The cumulative weight of judgment prophecies in Amos 6 creates an overwhelming sense of inevitability. God isn't threatening; He's announcing settled reality. Like Sodom (Genesis 19), when judgment arrives, escape proves nearly impossible. This should drive people to urgent repentance while opportunity remains.",
            "historical": "The Assyrian siege of Samaria lasted three years (2 Kings 17:5). Siege warfare involved starvation, disease, and finally slaughter when walls were breached. Archaeological evidence from Lachish and other sites confirms the devastating completeness of Assyrian conquest—fulfilling this prophecy's grim details.",
            "questions": [
                "How should the certainty and severity of judgment drive urgent evangelism and discipleship?",
                "What does it mean that even 'ten men' (a community) cannot save each other through collective action apart from God?",
                "How do modern people dismiss warnings of judgment as 'scare tactics' rather than loving warnings?"
            ]
        },
        "10": {
            "analysis": "<strong>And a man's uncle shall take him up, and he that burneth him, to bring out the bones out of the house</strong>—Jewish burial custom involved family members retrieving bodies. דּוֹד (<em>dod</em>, 'uncle') represents extended family obligation. The phrase 'burneth him' (וּמְסָרְפוֹ, <em>um'sarfo</em>) is unusual—Jews typically didn't cremate except in extreme circumstances (plague, war, desecration prevention). <strong>And shall say unto him that is by the sides of the house, Is there yet any with thee? and he shall say, No.</strong>—a survivor check finds none remaining. <strong>Then shall he say, Hold thy tongue: for we may not make mention of the name of the LORD</strong> (הַס כִּי־לֹא לְהַזְכִּיר בְּשֵׁם־יְהוָה, <em>has ki-lo l'hazkir b'shem-YHWH</em>)—either fearing to invoke God's name amidst judgment or recognizing their covenant-breaking forfeited the right to call on Him.<br><br>This chilling scene depicts absolute desolation and spiritual terror. The command to silence suggests recognition that God has turned against them—speaking His name might bring further judgment. When people can no longer pray, judgment has reached its fullest expression.",
            "historical": "This verse reflects the horrors of siege warfare and conquest's aftermath—mass death, emergency cremation, and terrorized survivors afraid to invoke their covenant God. The psychological and spiritual devastation matches physical destruction.",
            "questions": [
                "What does it mean to be unable or afraid to invoke God's name—complete abandonment or self-imposed silence?",
                "How should this terrifying scene motivate urgent faithfulness while we can still freely call on God's name?",
                "What warning does this give about societies or churches where God's name becomes increasingly unwelcome?"
            ]
        },
        "11": {
            "analysis": "<strong>For, behold, the LORD commandeth, and he will smite the great house with breaches, and the little house with clefts</strong> (כִּי־הִנֵּה יְהוָה מְצַוֶּה וְהִכָּה הַבַּיִת הַגָּדוֹל רְסִיסִים וְהַבַּיִת הַקָּטֹן בְּקִעִים, <em>ki-hineh YHWH m'tzaveh v'hikah habayit hagadol resisim v'habayit hakaton b'qi'im</em>)—both great houses (הַבַּיִת הַגָּדוֹל, <em>habayit hagadol</em>, palaces) and small houses (הַבַּיִת הַקָּטֹן, <em>habayit hakaton</em>, peasant dwellings) face destruction. רְסִיסִים (<em>resisim</em>, 'breaches, fragments') and בְּקִעִים (<em>b'qi'im</em>, 'clefts, cracks') suggest structural collapse—both total ruin and partial damage, depending on size.<br><br>This emphasizes judgment's universality: wealth provides no protection. The rich who oppressed and the poor who acquiesced both face consequences. Romans 2:11 confirms this principle: 'there is no respect of persons with God.' Judgment reaches all socioeconomic levels when a nation rejects God.",
            "historical": "Assyrian conquest records and archaeological evidence confirm widespread destruction across all social strata in conquered cities. When Samaria fell, both palaces and peasant homes were destroyed—fulfilling this prophecy's details precisely.",
            "questions": [
                "How does universal judgment—affecting rich and poor alike—demonstrate both God's justice and humanity's collective guilt?",
                "What warning does this give to those who think their humble status exempts them from accountability?",
                "How should the certainty of judgment motivate Christians across all socioeconomic levels to faithful witness?"
            ]
        },
        "12": {
            "analysis": "<strong>Shall horses run upon the rock? will one plow there with oxen?</strong> (הַיְרֻצוּן בַּסֶּלַע סוּסִים אִם־יַחֲרוֹשׁ בַּבְּקָרִים, <em>hayrutzun basela susim im-yacharosh bab'qarim</em>)—two rhetorical questions about absurdities: horses can't gallop on rocky cliffs; oxen can't plow stone. Yet Israel's behavior is equally absurd: <strong>for ye have turned judgment into gall, and the fruit of righteousness into hemlock</strong> (כִּי־הֲפַכְתֶּם לְרֹאשׁ מִשְׁפָּט וּפְרִי צְדָקָה לְלַעֲנָה, <em>ki-hafachtem l'rosh mishpat ufri tz'dakah l'la'anah</em>)—they've inverted justice (מִשְׁפָּט, <em>mishpat</em>) into poison (רֹאשׁ, <em>rosh</em>, literally 'head,' meaning poisonous plant or gall), and righteousness's fruit (צְדָקָה, <em>tz'dakah</em>) into wormwood (לַעֲנָה, <em>la'anah</em>, bitter poison).<br><br>This indicts moral inversion: making justice serve oppression and perverting righteousness into wickedness. When legal systems meant to protect the vulnerable instead exploit them, society commits absurdity worse than horses running on rocks. Isaiah 5:20 pronounces woe on such moral confusion: 'Woe unto them that call evil good, and good evil.'",
            "historical": "Amos repeatedly attacks Israel's corrupt legal system (Amos 5:10-15). Courts that should have defended the poor instead took bribes and ruled for the powerful. This judicial corruption was systemic, not isolated—making judgment inevitable.",
            "questions": [
                "What modern legal or political systems pervert justice into oppression while claiming righteousness?",
                "How do Christians sometimes invert biblical values—calling tolerance 'love,' compromise 'wisdom,' or comfort 'blessing'?",
                "What does it mean to restore justice and righteousness when systems have become thoroughly corrupted?"
            ]
        },
        "13": {
            "analysis": "<strong>Ye which rejoice in a thing of nought</strong> (הַשְּׂמֵחִים לְלֹא דָבָר, <em>hasemechim l'lo davar</em>, literally 'rejoicing in no-thing, vanity')—they celebrate empty achievements. <strong>Which say, Have we not taken to us horns by our own strength?</strong> (הַאֹמְרִים הֲלוֹא בְחָזְקֵנוּ לָקַחְנוּ לָנוּ קַרְנָיִם, <em>ha'om'rim halo v'chozkeinu lakachnu lanu karnayim</em>)—'horns' (קַרְנַיִם, <em>karnayim</em>) symbolize military power (Deuteronomy 33:17). They boast about military victories achieved 'by our own strength' (בְחָזְקֵנוּ, <em>v'chozkeinu</em>), crediting themselves rather than God.<br><br>This reveals the root sin: pride that denies God's sovereignty and credits human achievement. Jeroboam II's military successes (2 Kings 14:25-28) produced nationalistic arrogance—forgetting that God gave the victories. Habakkuk 1:11 describes similar pride: 'his own might is his god.' All human achievement apart from acknowledging God's enablement is 'vanity.'",
            "historical": "Jeroboam II expanded Israel's borders to near-Davidic dimensions, creating prosperity and military confidence. Rather than attributing success to God's covenant faithfulness, Israel credited their own strength—the pattern of all proud civilizations that rise and fall.",
            "questions": [
                "What modern achievements—technological, economic, military—do nations or individuals credit to their own strength rather than God?",
                "How does rejoicing in 'things of nought' describe celebrating temporary, earthly accomplishments while ignoring eternal realities?",
                "What's the difference between legitimate thanksgiving for accomplishments and proud self-credit that forgets God?"
            ]
        },
        "14": {
            "analysis": "<strong>But, behold, I will raise up against you a nation, O house of Israel</strong> (כִּי הִנְנִי מֵקִים עֲלֵיכֶם בֵּית יִשְׂרָאֵל גּוֹי, <em>ki hin'ni meikim aleichem beit Yisrael goy</em>)—God personally raises up (מֵקִים, <em>meikim</em>) the enemy nation (גּוֹי, <em>goy</em>). <strong>Saith the LORD the God of hosts</strong> confirms divine authority. <strong>And they shall afflict you from the entering in of Hemath unto the river of the wilderness</strong> (וְלָחֲצוּ אֶתְכֶם מִלְּבוֹא חֲמָת עַד־נַחַל הָעֲרָבָה, <em>v'lachatzu etchem mil'vo Chamat ad-nachal ha'aravah</em>)—the enemy will oppress (לָחַץ, <em>lachatz</em>) Israel throughout their entire territory, from northern border (Lebo-Hamath) to southern (the Arabah river/wadi).<br><br>This directly counters verse 13's boast about taking 'horns' by their own strength. The same territory they conquered will be reconquered—by a nation God Himself raises against them. Human military might collapses before divine judgment. Assyria fulfilled this prophecy, but ultimately God sovereignly controls all nations for His purposes (Isaiah 10:5-19).",
            "historical": "Tiglath-Pileser III began Assyrian incursions in 734 BC, culminating in Samaria's fall in 722 BC. The Assyrians conquered exactly the territory Jeroboam II had expanded—demonstrating that God giveth and God taketh away. Israel's boasted military victories became meaningless when God withdrew protection.",
            "questions": [
                "How does recognizing God's sovereignty over nations—raising up and bringing down—humble national pride?",
                "What does it mean that God uses pagan nations as instruments of judgment against His own people?",
                "How should Christians respond to national decline or military defeat—as random events or potential divine discipline?"
            ]
        }
    },
    "7": {
        "15": {
            "analysis": "<strong>And the LORD took me as I followed the flock</strong> (וַיִּקָּחֵנִי יְהוָה מֵאַחֲרֵי הַצֹּאן, <em>vayikacheni YHWH me'acharei hatzon</em>)—the verb לָקַח (<em>lakach</em>, 'to take, seize') suggests divine compulsion. Amos didn't volunteer; God took him from shepherding. <strong>And the LORD said unto me, Go, prophesy unto my people Israel</strong> (וַיֹּאמֶר יְהוָה אֵלַי לֵךְ הִנָּבֵא אֶל־עַמִּי יִשְׂרָאֵל, <em>vayomer YHWH elai lech hinave el-ami Yisrael</em>)—God's direct command (לֵךְ, <em>lech</em>, 'go!') and claim ('my people') authenticates Amos's message against Amaziah's opposition (7:10-13).<br><br>This verse defends prophetic authority: Amos prophesies not by professional training but divine commission. The same pattern appears with Moses (Exodus 3:10), Jeremiah (Jeremiah 1:7), and New Testament apostles (Galatians 1:1)—God's call, not human credentials, validates ministry. True preaching flows from divine sending, not self-appointment.",
            "historical": "Amaziah the priest of Bethel commanded Amos to stop prophesying (7:12-13), claiming prophetic ministry required institutional approval. Amos responds by affirming his divine commission—God's authority trumps human religious hierarchies. This conflict between institutional religion and prophetic truth recurs throughout Scripture.",
            "questions": [
                "How does God's calling provide authority independent of institutional approval or professional credentials?",
                "What's the difference between self-appointed ministry and being 'taken' by God for His purposes?",
                "How should churches respond when God sends messengers who lack traditional credentials but speak His word faithfully?"
            ]
        },
        "16": {
            "analysis": "<strong>Now therefore hear thou the word of the LORD: Thou sayest, Prophesy not against Israel, and drop not thy word against the house of Isaac</strong> (וְעַתָּה שְׁמַע דְּבַר־יְהוָה אַתָּה אֹמֵר לֹא תִנָּבֵא עַל־יִשְׂרָאֵל וְלֹא תַטִּיף עַל־בֵּית יִשְׂחָק, <em>v'atah sh'ma d'var-YHWH atah omer lo tinave al-Yisrael v'lo tatif al-beit Yitzchak</em>)—Amos confronts Amaziah directly. The verb טַף (<em>nataf</em>, 'to drop, drip, preach') appears in the causative: 'drop not thy word'—Amaziah wants Amos to stop speaking God's Word. Using 'Isaac' instead of 'Israel' emphasizes covenant sonship, making Amaziah's resistance worse—he's protecting God's covenant people from God's covenant word.<br><br>This confrontation typifies conflict between institutional religion and prophetic truth. Amaziah represents state-sponsored religion serving political ends (Bethel was the king's sanctuary, 7:13), while Amos speaks uncompromising divine truth. When religious leaders prioritize institutional preservation over prophetic faithfulness, they resist God Himself.",
            "historical": "Bethel was the northern kingdom's primary religious center, established by Jeroboam I with golden calf worship (1 Kings 12:28-29). By Amos's time, it functioned as state-controlled religion legitimizing the status quo. Amaziah's opposition to Amos shows how false worship systems silence prophetic voices that threaten their power.",
            "questions": [
                "How do modern religious institutions sometimes resist prophetic voices that threaten comfortable compromise?",
                "What's the difference between legitimate church authority and religious leadership that silences God's Word?",
                "How should Christians respond when religious leaders command them not to speak biblical truth?"
            ]
        },
        "17": {
            "analysis": "<strong>Therefore thus saith the LORD</strong>—Amos pronounces specific judgment on Amaziah personally. <strong>Thy wife shall be an harlot in the city</strong> (אִשְׁתְּךָ בָעִיר תִּזְנֶה, <em>ish't'cha va'ir tizneh</em>)—likely raped by conquering soldiers, a common siege warfare atrocity (Isaiah 13:16; Zechariah 14:2). <strong>And thy sons and thy daughters shall fall by the sword</strong>—his children will be killed. <strong>And thy land shall be divided by line</strong> (וְאַדְמָתְךָ בַחֶבֶל תְּחֻלָּק, <em>v'admat'cha bachevel techulak</em>)—his property will be parceled out to foreign settlers. <strong>And thou shalt die in a polluted land: and Israel shall surely go into captivity forth of his land</strong> (וְאַתָּה עַל־אֲדָמָה טְמֵאָה תָמוּת וְיִשְׂרָאֵל גָּלֹה יִגְלֶה מֵעַל אַדְמָתוֹ, <em>v'atah al-adamah t'me'ah tamut v'Yisrael galoh yigleh me'al admato</em>)—Amaziah will die in exile on unclean (טְמֵאָה, <em>t'me'ah</em>) foreign soil.<br><br>This is the prophet's authority to pronounce judgment (Matthew 18:18; John 20:23). Amaziah resisted God's word, so God's word judges him specifically. The progression—wife, children, land, death in exile—encompasses total loss. Resisting God's prophetic word brings not safety but heightened judgment.",
            "historical": "No record exists of Amaziah's fate, but this prophecy's specificity suggests it was remembered and likely fulfilled during Assyria's conquest. The principle holds: those who silence prophetic truth to preserve institutions face greater judgment than those they sought to protect from conviction.",
            "questions": [
                "How does resisting prophetic truth bring judgment rather than protection from uncomfortable conviction?",
                "What does it mean for religious leaders to die 'in a polluted land'—separated from God's presence and promises?",
                "How should this warning shape how church leaders respond to biblical critique of their practices?"
            ]
        }
    },
    "8": {
        "12": {
            "analysis": "<strong>And they shall wander from sea to sea, and from the north even to the east, they shall run to and fro to seek the word of the LORD, and shall not find it</strong> (וְנָעוּ מִיָּם עַד־יָם וּמִצָּפוֹן וְעַד־מִזְרָח יְשׁוֹטְטוּ לְבַקֵּשׁ אֶת־דְּבַר־יְהוָה וְלֹא יִמְצָאוּ, <em>v'na'u miyam ad-yam umitzafon v'ad-mizrach y'shot'tu l'vakeish et-d'var YHWH v'lo yimtza'u</em>)—The verbs intensify desperate search: נוּעַ (<em>nua</em>, 'to wander'), שׁוֹטֵט (<em>shotet</em>, 'to run to and fro'), בָּקַשׁ (<em>bakash</em>, 'to seek earnestly'). Yet לֹא יִמְצָאוּ (<em>lo yimtza'u</em>, 'they will not find')—God's Word becomes unavailable.<br><br>This describes spiritual famine worse than physical starvation (Amos 8:11). Those who despised God's Word when available will desperately seek it when removed. This prefigures Jesus's warning: 'The night cometh, when no man can work' (John 9:4). Opportunity for repentance doesn't last forever—God's patience has limits. When judgment arrives, it's too late to seek what was previously rejected.",
            "historical": "After Samaria's fall and exile, prophetic voice ceased in the northern kingdom. No more prophets arose; God's Word fell silent. For generations, they'd rejected prophets like Amos—then when judgment came, no prophetic word offered hope or guidance. Hebrews 12:17 describes similar irreversible loss: Esau 'found no place of repentance, though he sought it carefully with tears.'",
            "questions": [
                "How does rejecting God's Word when it's available lead to its removal when desperately needed?",
                "What warning does this give to churches or nations that increasingly silence or ignore Scripture?",
                "How should the possibility of irreversible spiritual famine motivate urgent response to God's Word now?"
            ]
        },
        "13": {
            "analysis": "<strong>In that day shall the fair virgins and young men faint for thirst</strong> (בַּיּוֹם הַהוּא תִּתְעַלַּפְנָה הַבְּתוּלֹת הַיָּפוֹת וְהַבַּחוּרִים בַּצָּמָא, <em>bayom hahu tit'alafnah hab'tulot hayafot v'habachurim batzama</em>)—Young, vigorous people (בְּתוּלוֹת, <em>betulot</em>, 'virgins'; בַּחוּרִים, <em>bachurim</em>, 'young men') typically most resilient will 'faint' (עָלַף, <em>alaf</em>, 'grow faint, languish'). But this is spiritual thirst (צָמָא, <em>tzama</em>), not physical—they faint from lack of God's Word (8:11-12), not water.<br><br>This emphasizes spiritual famine's devastating completeness: even the strong cannot endure. Jesus promised the opposite to those who come to Him: 'whosoever drinketh of the water that I shall give him shall never thirst' (John 4:14). Rejecting Living Water results in unquenchable spiritual thirst.",
            "historical": "This prophecy describes the post-exilic state of the northern tribes. Scattered among pagan nations without temple, priesthood, or prophets, they spiritually withered. Later, Jesus found Israel in similar spiritual famine—shepherdless sheep whom religious leaders had failed to feed (Matthew 9:36).",
            "questions": [
                "How do people today spiritually 'faint for thirst' despite having physical Bibles accessible everywhere?",
                "What's the difference between spiritual thirst that drives people to God versus the judgment-famine where His Word becomes unavailable?",
                "How should this warning motivate believers to drink deeply from God's Word while it remains accessible?"
            ]
        },
        "14": {
            "analysis": "<strong>They that swear by the sin of Samaria</strong> (הַנִּשְׁבָּעִים בְּאַשְׁמַת שֹׁמְרוֹן, <em>hanishba'im b'ashmat Shomron</em>)—'sin' (אַשְׁמַת, <em>ashmat</em>) likely refers to the golden calf at Bethel or possibly Asherah worship. They swear oaths by idols rather than Yahweh. <strong>And say, Thy god, O Dan, liveth</strong> (וְאָמְרוּ חֵי אֱלֹהֶיךָ דָּן, <em>v'am'ru chei Eloheicha Dan</em>)—Dan had the other golden calf shrine (1 Kings 12:29). <strong>And, The manner of Beer-sheba liveth</strong> (וְחֵי דֶּרֶךְ בְּאֵר שָׁבַע, <em>v'chei derech Be'er Sheva</em>)—דֶּרֶךְ (<em>derech</em>) might mean 'way' (pilgrimage route) or refer to another cultic object. <strong>Even they shall fall, and never rise up again</strong> (וְנָפְלוּ וְלֹא־יָקוּמוּ עוֹד, <em>v'naflu v'lo-yakumu od</em>)—permanent spiritual death.<br><br>Swearing by false gods demonstrates complete apostasy—binding oneself to powerless idols rather than the living God. The irony: they say these gods 'live' (חֵי, <em>chei</em>), but worshipers themselves will fall and never rise. Psalm 115:8 warns: 'They that make them are like unto them'—idolaters share their idols' impotence. Only those who swear by the true God's name find life (Jeremiah 4:2).",
            "historical": "The golden calves at Dan and Bethel represented Israel's foundational apostasy (1 Kings 12:28-29). Beer-sheba was in Judah's territory but apparently featured in northern pilgrimage practices. This syncretistic worship—mixing Yahweh forms with pagan content—epitomized covenant unfaithfulness that guaranteed exile.",
            "questions": [
                "What modern equivalents exist to 'swearing by idols'—binding ourselves to false securities and calling them 'alive'?",
                "How does syncretism (mixing true worship with false elements) ultimately prove deadlier than outright paganism?",
                "What does it mean to 'fall and never rise'—experiencing judgment without hope of restoration?"
            ]
        }
    },
    "9": {
        "14": {
            "analysis": "<strong>And I will bring again the captivity of my people of Israel</strong> (וְשַׁבְתִּי אֶת־שְׁבוּת עַמִּי יִשְׂרָאֵל, <em>v'shavti et-sh'vut ami Yisrael</em>)—After chapters of unrelenting judgment, Amos concludes with restoration promise. The verb שׁוּב (<em>shuv</em>, 'to return, restore') signals covenant renewal. <strong>And they shall build the waste cities, and inhabit them</strong> (וּבָנוּ עָרִים נְשַׁמּוֹת וְיָשָׁבוּ, <em>uvanu arim neshamot v'yashavu</em>)—reversing covenant curses (Deuteronomy 28:30, 39). <strong>And they shall plant vineyards, and drink the wine thereof; they shall also make gardens, and eat the fruit of them</strong>—full covenant blessing (Deuteronomy 28:4, 11) restored.<br><br>This demonstrates covenant faithfulness: God judges sin but doesn't abandon His purposes. James's citation in Acts 15:16-17 applies this to Gentile inclusion—God's restoration exceeds ethnic Israel, encompassing all nations through Christ. The ultimate fulfillment awaits Christ's return, when creation itself is restored (Romans 8:19-23).",
            "historical": "While a small remnant returned from Babylonian exile, this prophecy awaits complete fulfillment in the Messianic age. The New Testament interprets it Christologically—Jesus as the tabernacle of David (John 1:14), gathering both Jews and Gentiles into one people (Ephesians 2:11-22).",
            "questions": [
                "How does God's promise of restoration after judgment demonstrate covenant faithfulness despite human unfaithfulness?",
                "In what ways does the New Covenant in Christ fulfill these restoration prophecies beyond merely national Israel?",
                "How should future hope of complete restoration motivate present faithfulness and evangelistic urgency?"
            ]
        },
        "15": {
            "analysis": "<strong>And I will plant them upon their land, and they shall no more be pulled up out of their land which I have given them, saith the LORD thy God</strong> (וּנְטַעְתִּים עַל־אַדְמָתָם וְלֹא יִנָּתְשׁוּ עוֹד מֵעַל אַדְמָתָם אֲשֶׁר נָתַתִּי לָהֶם אָמַר יְהוָה אֱלֹהֶיךָ, <em>un'ta'tim al-admatam v'lo yinat'shu od me'al admatam asher natati lahem amar YHWH Eloheicha</em>)—The metaphor shifts from building/planting to permanent rooting. נָטַע (<em>nata</em>, 'to plant') suggests God Himself plants them; נָתַשׁ (<em>natash</em>, 'to uproot, pluck up') will never again occur. The phrase <strong>no more</strong> (לֹא...עוֹד, <em>lo...od</em>) emphasizes permanence. <strong>Saith the LORD thy God</strong>—Amos ends with intimate covenant language: not merely יְהוָה (<em>YHWH</em>) but יְהוָה אֱלֹהֶיךָ (<em>YHWH Eloheicha</em>, 'the LORD your God')—covenant relationship restored.<br><br>This final verse promises permanent security for God's people. While physical Israel experienced repeated exile, the ultimate fulfillment comes through Christ—believers are 'in Christ' permanently (John 10:28-29; Romans 8:35-39). No power can uproot those God plants in Christ. The book that began with judgment roars ends with grace whispers—God's last word is always restoration.",
            "historical": "The return from Babylonian exile only partially fulfilled this—they rebuilt but remained under foreign domination (Persian, Greek, Roman) and experienced another exile in 70 AD. Full, permanent restoration awaits Christ's return, when God's people inherit the renewed earth (Revelation 21-22).",
            "questions": [
                "How does God's promise of permanent planting provide assurance to believers eternally secure in Christ?",
                "What's the relationship between Old Testament land promises and New Testament spiritual inheritance in Christ?",
                "How should Amos's pattern—judgment leading to restoration—shape how we understand God's discipline and ultimate purposes?"
            ]
        }
    }
}

# Merge entries
added_count = 0
for chapter, verses in new_entries.items():
    if chapter not in commentary:
        commentary[chapter] = {}
    for verse, entry in verses.items():
        if verse not in commentary[chapter]:
            commentary[chapter][verse] = entry
            added_count += 1
            print(f"Added Amos {chapter}:{verse}")

data["commentary"] = commentary

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal Amos verses added: {added_count}")
print(f"Saved to {filepath}")
