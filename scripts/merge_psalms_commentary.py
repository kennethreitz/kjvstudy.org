#!/usr/bin/env python3
"""
Generate and merge all 78 missing Psalms commentaries.
This script creates scholarly Reformed commentary with Hebrew transliterations.
"""

import json
from pathlib import Path

# Define ALL new commentary entries
new_commentary_data = {
    "86": {
        "12": {
            "analysis": "<strong>I will praise thee, O Lord my God, with all my heart</strong> (אוֹדְךָ אֲדֹנָי אֱלֹהַי בְּכָל־לְבָבִי, <em>odekha Adonai elohai b'khol-l'vavi</em>)—The verb <em>yadah</em> (praise, give thanks) in the first person: I will personally, continuously give thanks. <em>B'khol-l'vavi</em> (with all my heart) echoes the Shema's command to love God with all your heart (Deuteronomy 6:5). Wholehearted praise is undivided devotion—not perfunctory ritual but total engagement of will, emotion, and affection.<br><br><strong>I will glorify thy name for evermore</strong> (וַאֲכַבְּדָה שִׁמְךָ לְעוֹלָם, <em>va'akhabdah shimkha l'olam</em>)—<em>Kabad</em> means to make heavy, to honor, glorify. God's <em>shem</em> (name) represents his character and reputation. <em>L'olam</em> (forever, perpetually) extends praise beyond this life into eternity. This is the Westminster Shorter Catechism's answer to man's chief end: 'to glorify God and enjoy him forever.'",
            "historical": "Psalm 86 is labeled 'A Prayer of David,' the only psalm in Book III so attributed. Its language echoes Moses' revelation of God's character in Exodus 34:6-7. Ancient worship emphasized God's name as the locus of his presence—to glorify his name was to magnify his revealed character. Jewish liturgy incorporated this verse in daily prayers.",
            "questions": [
                "What does wholehearted praise look like practically in your daily life?",
                "How can you glorify God's name (his character) in the ordinary moments of today?",
                "What would change if you truly lived for God's glory rather than personal comfort or reputation?"
            ]
        },
        "13": {
            "analysis": "<strong>For great is thy mercy toward me</strong> (כִּי־גָדוֹל חַסְדְּךָ עָלָי, <em>ki-gadol chasdekha alai</em>)—<em>Gadol</em> (great, vast, immense) modifies <em>chesed</em>, that untranslatable Hebrew gem meaning steadfast love, loyal kindness, covenant faithfulness. God's <em>chesed</em> toward David personally (<em>alai</em>, upon me, toward me) is the ground of all praise. This isn't generic divine benevolence but specific, experienced mercy in David's life.<br><br><strong>And thou hast delivered my soul from the lowest hell</strong> (וְהִצַּלְתָּ נַפְשִׁי מִשְּׁאוֹל תַּחְתִּיָּה, <em>v'hitzalta nafshi mish'ol tachtiyah</em>)—<em>Natsal</em> (deliver, snatch away, rescue) in the perfect tense: accomplished deliverance. <em>Sh'ol tachtiyah</em> (Sheol below, the lowest hell) describes the grave, death's realm, the pit. David testifies to being rescued from the brink of death—whether physical danger or spiritual despair. Christians read this as foreshadowing Christ's resurrection: he descended to the dead and rose victorious (1 Peter 3:19, Ephesians 4:9).",
            "historical": "Sheol in Hebrew thought was the underworld, the realm of the dead—not necessarily eternal punishment but the state of mortality and separation from the land of the living. Deliverance from Sheol meant being saved from premature death. The 'lowest Sheol' intensifies the danger: not just near death but at death's deepest point.",
            "questions": [
                "How has God's mercy (chesed) been specifically great toward you in your life story?",
                "From what 'lowest hell' (desperate circumstance or sin) has God delivered you?",
                "How does Christ's descent and resurrection amplify the hope of this verse?"
            ]
        },
        "14": {
            "analysis": "<strong>O God, the proud are risen against me</strong> (אֱלֹהִים זֵדִים קָמוּ־עָלַי, <em>Elohim zedim kamu-alai</em>)—<em>Zedim</em> (proud ones, presumptuous, arrogant) describes those who act with insolent pride. <em>Qamu</em> (they have risen) suggests insurrection, uprising—like Absalom's rebellion against David, or Saul's pursuit. The proud don't merely oppose; they actively rise up in organized hostility.<br><br><strong>And the assemblies of violent men have sought after my soul</strong> (וַעֲדַת עָרִיצִים בִּקְשׁוּ נַפְשִׁי, <em>va'adat aritsim bikshu nafshi</em>)—<em>Adat</em> (assembly, congregation) ironically applies to the wicked what should describe God's people. <em>Aritsim</em> (violent, ruthless, terrorizing men) gathered in organized conspiracy. <em>Bikshu nafshi</em> (have sought my life) indicates murderous intent. <strong>And have not set thee before them</strong> (וְלֹא שָׂמוּךָ לְנֶגְדָּם, <em>v'lo samukha l'negdam</em>)—The root problem: they don't set God before their eyes. Practical atheism: living as if God doesn't exist or doesn't see. Contrast Psalm 16:8: 'I have set the LORD always before me.'",
            "historical": "David faced numerous conspiracies: Saul's court, Absalom's rebellion, enemies throughout his reign. The language of assembly and seeking his life describes organized opposition, not random violence. In ancient kingdoms, court intrigues and assassination attempts were constant threats. This verse could describe any of David's major crises.",
            "questions": [
                "How does pride lead people to oppose God's purposes and God's people?",
                "What does it mean practically to 'set God before you' in daily decisions?",
                "When facing opposition, how can you avoid responding with the same godless pride as your opponents?"
            ]
        },
        "15": {
            "analysis": "<strong>But thou, O Lord, art a God full of compassion, and gracious</strong> (וְאַתָּה אֲדֹנָי אֵל־רַחוּם וְחַנּוּן, <em>v'atah Adonai el-rachum v'chanun</em>)—The emphatic contrast: <em>But thou!</em> This quotes Exodus 34:6, where God revealed his character to Moses. <em>Rachum</em> (compassionate, full of womb-love) comes from <em>rechem</em> (womb), suggesting maternal tenderness. <em>Chanun</em> (gracious) means giving undeserved favor. These aren't mere attributes but God's self-revelation of his essential nature.<br><br><strong>Longsuffering, and plenteous in mercy and truth</strong> (אֶרֶךְ אַפַּיִם וְרַב־חֶסֶד וֶאֱמֶת, <em>erekh apayim v'rav-chesed ve'emet</em>)—<em>Erekh apayim</em> (long of nostrils, slow to anger) is a Hebrew idiom: God's anger has a long fuse. <em>Rav-chesed</em> (abundant in steadfast love) and <em>emet</em> (truth, faithfulness) complete the Exodus 34 formula. This is the gospel: God's character is fundamentally gracious. His wrath is real but restrained; his mercy is abundant and eager. Contrast the violent men of verse 14 with God's compassionate nature—which would you rather face?",
            "historical": "This Exodus 34:6-7 formula became Israel's foundational creed, quoted repeatedly (Numbers 14:18, Nehemiah 9:17, Psalm 103:8, 145:8, Joel 2:13, Jonah 4:2). Moses had asked to see God's glory; God proclaimed his name, revealing that his glory is supremely his gracious, merciful character. David appeals to this revelation when facing enemies.",
            "questions": [
                "How does knowing God is 'slow to anger' affect how you approach him in your sin and failure?",
                "What's the difference between God's longsuffering and modern notions of tolerance or leniency?",
                "How can you reflect God's character (compassion, grace, patience, mercy, truth) in your relationships?"
            ]
        },
        "16": {
            "analysis": "<strong>O turn unto me, and have mercy upon me</strong> (פְּנֵה־אֵלַי וְחָנֵּנִי, <em>p'neh-elai v'choneni</em>)—<em>Panah</em> means to turn, face toward. David asks God to turn his face toward him—the opposite of hiding his face (Psalm 13:1, 27:9). <em>Chanan</em> (have mercy, be gracious) is the verb form of <em>chen</em> (grace). The plea: Look at me with favor, not judgment; with grace, not wrath. Fallen humans instinctively hide from God's gaze (Genesis 3:8); redeemed believers seek his face (Psalm 27:8).<br><br><strong>Give thy strength unto thy servant</strong> (תְּנָה־עֻזְּךָ לְעַבְדֶּךָ, <em>t'nah-uz'kha l'avdekha</em>)—<em>Oz</em> (strength, might) is what David needs against the violent men (v.14). But notice: not self-generated strength or military power, but <em>thy strength</em>—divine empowerment. <strong>And save the son of thine handmaid</strong> (וְהוֹשִׁיעָה לְבֶן־אֲמָתֶךָ, <em>v'hoshi'ah l'ven-amatekha</em>)—<em>Ben-amatekha</em> (son of your handmaid) was a way to claim God's household protection. In ancient culture, children born in a master's house to his servants had special status and security. David says: I'm born into your household; defend me as your own!",
            "historical": "The phrase 'son of your handmaid' appears also in Psalm 116:16. It may refer literally to David's mother being devoted to God's service, or figuratively to David being a servant from birth. In ancient Near Eastern culture, being born in the master's household gave one rights and protection that outsiders lacked. David claims covenant family status.",
            "questions": [
                "What does it mean to seek God's face rather than merely his hand (his blessings)?",
                "Where in your life do you need to stop relying on your own strength and ask for God's?",
                "How does your identity as God's child (born into his household through faith) give you confidence in prayer?"
            ]
        },
        "17": {
            "analysis": "<strong>Shew me a token for good</strong> (עֲשֵׂה־עִמִּי אוֹת לְטוֹבָה, <em>aseh-imi ot l'tovah</em>)—<em>Ot</em> (sign, token, mark) is what David requests—visible evidence of God's favor. Not secret, mystical reassurance but public vindication. Like Gideon's fleece (Judges 6:36-40) or Hezekiah's sundial (2 Kings 20:8-11), a sign confirms God's word and demonstrates his presence. <em>L'tovah</em> (for good, for blessing) specifies the sign's nature: evidence of divine favor.<br><br><strong>That they which hate me may see it, and be ashamed</strong> (וְיִרְאוּ שֹׂנְאַי וְיֵבֹשׁוּ, <em>v'yir'u son'ai v'yevoshu</em>)—The purpose: public vindication. <em>Son'ai</em> (those who hate me) will <em>see</em> (<em>ra'ah</em>) and be <em>ashamed</em> (<em>bosh</em>, disappointed, humiliated). Not personal vengeance but theodicy: when God visibly defends his servant, it proves that the wicked's confidence was misplaced. <strong>Because thou, LORD, hast holpen me, and comforted me</strong> (כִּי־אַתָּה יְהוָה עֲזַרְתַּנִי וְנִחַמְתָּנִי, <em>ki-atah YHWH azartani v'nichamtani</em>)—Past tenses expressing confidence: You have helped (<em>azar</em>) and comforted (<em>nacham</em>) me. Faith speaks of future deliverance as already accomplished (Romans 8:30).",
            "historical": "God's visible interventions—the plagues in Egypt, Jericho's walls falling, Gideon's victories—served not just to deliver Israel but to demonstrate Yahweh's supremacy to watching nations. The sign David requests would similarly vindicate both David and David's God before his enemies. This anticipates Christ's resurrection as the ultimate vindicating sign (Matthew 12:39-40, Romans 1:4).",
            "questions": [
                "Is it appropriate to ask God for visible signs of his favor, or is that lack of faith?",
                "How does God's public vindication of his people serve his larger purposes in the world?",
                "What signs or tokens of God's goodness in your past give you confidence for present challenges?"
            ]
        }
    },
    "94": {
        "21": {
            "analysis": "<strong>They gather themselves together against the soul of the righteous</strong> (יָגוֹדּוּ עַל־נֶפֶשׁ צַדִּיק, <em>yagodu al-nefesh tsadiq</em>)—<em>Gadad</em> means to gather in troops, to band together in hostile formation. Not random opposition but organized conspiracy. The <em>nefesh</em> (soul, life) of the <em>tsadiq</em> (righteous) is the target. Throughout history, the wicked have formed alliances against God's people: Pharisees and Herodians against Jesus (Mark 3:6), Sanhedrin against the apostles (Acts 4:27), Roman persecutors against Christians.<br><br><strong>And condemn the innocent blood</strong> (וְדָם נָקִי יַרְשִׁיעוּ, <em>v'dam naqi yarshi'u</em>)—<em>Dam naqi</em> (innocent blood) represents the righteous person. <em>Rasha</em> (to condemn, declare guilty) inverts justice: the innocent are convicted, the guilty go free. This is judicial murder—using legal machinery to execute the blameless. Naboth condemned for Ahab's greed (1 Kings 21), Jesus crucified by legal proceeding (Matthew 27:24), Stephen stoned by council vote (Acts 7:58-60). Unjust courts are Satan's mockery of God's justice.",
            "historical": "Psalm 94 is a lament against oppressive rulers who pervert justice (verses 3-7, 20-21). Likely written during a period when Israel's own leaders or foreign occupiers abused the judicial system. The prophet Micah condemned similar corruption: 'They build Zion with blood and Jerusalem with iniquity' (Micah 3:10). Amos and Isaiah likewise denounced legal oppression of the righteous poor.",
            "questions": [
                "How should Christians respond when legal systems are used to persecute the righteous?",
                "What modern examples exist of organized conspiracy against the innocent, and how should the church respond?",
                "How does Jesus's unjust trial and condemnation both exemplify this psalm and provide hope for the persecuted?"
            ]
        },
        "22": {
            "analysis": "<strong>But the LORD is my defence</strong> (וַיְהִי יְהוָה לִי לְמִשְׂגָּב, <em>vay'hi YHWH li l'misgav</em>)—The emphatic contrast: <em>But</em>! Against the gathered wicked (v.21), David has Yahweh. <em>Misgav</em> means high fortress, secure stronghold, place of refuge. Like Masada or En-gedi's cliffs, a <em>misgav</em> provides protection beyond human assault. God himself is David's impregnable fortress—no conspiracy can breach divine defense.<br><br><strong>And my God is the rock of my refuge</strong> (וֵאלֹהַי לְצוּר מַחְסִי, <em>vElohay l'tsur machsi</em>)—Double imagery: <em>tsur</em> (rock, cliff) suggests stability and strength; <em>machseh</em> (refuge, shelter) suggests protection and safety. The rock is not merely a defensive position but a place of <em>refuge</em>—where one runs and hides. Moses hid in the rock's cleft to glimpse God's glory (Exodus 33:22); believers hide in the Rock who is Christ (1 Corinthians 10:4). Paul quotes this psalm in Romans 11:9, applying the wicked's judgment to those who reject Christ.",
            "historical": "David knew literal rock refuges—caves and mountain strongholds where he hid from Saul (1 Samuel 23:25-29, 24:1-3). These physical refuges illustrated spiritual reality: God's protection is more secure than any geographical fortress. The metaphor pervades the Psalms: Psalm 18:2, 31:3, 62:2, 71:3. Ancient Israel's rocky terrain made the imagery vivid and concrete.",
            "questions": [
                "What makes God a better refuge than any earthly defense or security system?",
                "In what threatening situation do you need to flee to God as your rock and fortress today?",
                "How does Christ fulfill this imagery as our Rock and our hiding place?"
            ]
        },
        "23": {
            "analysis": "<strong>And he shall bring upon them their own iniquity</strong> (וַיָּשֶׁב עֲלֵיהֶם אֶת־אוֹנָם, <em>vayashev alehem et-onam</em>)—<em>Shub</em> (return, bring back, repay) means God will cause their <em>aven</em> (iniquity, wickedness, trouble) to boomerang upon them. The principle of poetic justice: Haman hanged on his own gallows (Esther 7:10), Pharaoh drowned in the sea he used to murder Hebrew babies (Exodus 14:28), conspirators thrown to lions that were meant for Daniel (Daniel 6:24). God's judgment often uses the wicked's own schemes as instruments of their downfall.<br><br><strong>And shall cut them off in their own wickedness</strong> (וּבְרָעָתָם יַצְמִיתֵם, <em>uv'ra'atam yatsmitem</em>)—<em>Ra'ah</em> (evil, wickedness) becomes the means of their <em>cutting off</em> (<em>tsamat</em>, destroy, exterminate, silence). <strong>Yea, the LORD our God shall cut them off</strong> (יַצְמִיתֵם יְהוָה אֱלֹהֵינוּ, <em>yatsmitem YHWH Eloheinu</em>)—Emphatic repetition and divine title: Yahweh our God personally executes this judgment. The psalm began asking 'How long shall the wicked triumph?' (v.3); it ends affirming their certain destruction. Delayed judgment is not cancelled judgment.",
            "historical": "The principle appears throughout Scripture: Babel's confusion (Genesis 11), Sodom's fire (Genesis 19), Korah's earth-swallowing (Numbers 16), Sennacherib's army (2 Kings 19). Revelation promises final implementation: the beast and false prophet thrown into the lake of fire (Revelation 19:20), Satan bound and judged (Revelation 20:10). Justice may tarry but will not fail.",
            "questions": [
                "How does believing in certain future judgment affect your response to current injustice?",
                "What does 'bringing their own iniquity upon them' teach about the self-destructive nature of sin?",
                "How should Christians balance longing for justice with praying for enemies' repentance (while there's time)?"
            ]
        }
    },
    "95": {
        "8": {
            "analysis": "<strong>Harden not your heart</strong> (אַל־תַּקְשׁוּ לְבַבְכֶם, <em>al-takshu l'vavkhem</em>)—The prohibition uses <em>qashah</em> (to be hard, stiff, stubborn). The heart can be hardened like Pharaoh's (Exodus 7-14) or softened like Josiah's (2 Kings 22:19). Hardening is willful resistance to God's voice—the opposite of the tender responsiveness called for in verses 6-7. Hebrews 3-4 extensively applies this warning to Christians: 'Today, if you hear his voice, do not harden your hearts' (Hebrews 3:7-8, 15; 4:7).<br><br><strong>As in the provocation, and as in the day of temptation in the wilderness</strong> (כִּמְרִיבָה כְּיוֹם מַסָּה בַּמִּדְבָּר, <em>kim'rivah k'yom Massah bamidbar</em>)—<em>Merivah</em> (provocation, strife, contention) and <em>Massah</em> (testing) reference Exodus 17:7, where Israel tested God at Rephidim, demanding water: 'Is the LORD among us or not?' They provoked God by doubting his presence and provision despite repeated miracles. This became the paradigmatic example of unbelief.",
            "historical": "The Meribah-Massah incident (Exodus 17:1-7) occurred early in the wilderness wanderings. Despite seeing the plagues in Egypt, the Red Sea parting, manna from heaven, Israel doubted at the first difficulty. This pattern repeated throughout forty years, culminating in unbelief at Kadesh-barnea (Numbers 13-14), which resulted in that generation dying in the wilderness. Psalm 95 warns subsequent generations not to repeat the pattern.",
            "questions": [
                "In what areas of your life might you be hardening your heart against what God is saying?",
                "How does today's comfort and provision not guarantee tomorrow's faith under pressure?",
                "What practices help maintain a tender, responsive heart toward God's voice?"
            ]
        },
        "9": {
            "analysis": "<strong>When your fathers tempted me, proved me</strong> (אֲשֶׁר נִסּוּנִי אֲבוֹתֵיכֶם בְּחָנוּנִי, <em>asher nisuni avoteikhem b'chanuni</em>)—<em>Nasah</em> (test, tempt, put to the proof) and <em>bachan</em> (examine, try, prove) are synonymous intensification. The irony: God tests humans to prove their faithfulness, but Israel reversed the relationship, testing God's faithfulness. They put God on trial: 'Prove yourself to us! Show us you care!' This inverted the proper creature-Creator relationship. We don't test God; he tests us (Deuteronomy 8:2).<br><br><strong>And saw my work</strong> (גַּם־רָאוּ פָעֳלִי, <em>gam-ra'u fo'oli</em>)—<em>Gam</em> (also, even) emphasizes: they tested me <em>even though</em> they had <em>seen</em> (<em>ra'ah</em>) my <em>works</em> (<em>po'al</em>, deeds, acts). They were eyewitnesses to God's miracles yet still doubted. Seeing isn't believing when the heart is hard. Jesus faced the same: people saw his miracles yet demanded more signs (John 6:30). Thomas needed to see to believe, but Jesus said, 'Blessed are those who have not seen and yet have believed' (John 20:29).",
            "historical": "The wilderness generation saw more miracles than any generation before or since: ten plagues, Red Sea crossing, pillar of cloud and fire, manna daily, water from rocks, victories in battle, God's presence at Sinai. Yet Hebrews 3:10 quotes this verse, noting they 'always go astray in their heart.' Knowledge of God's works doesn't automatically produce faith when the will resists.",
            "questions": [
                "What 'works of God' have you personally witnessed, and how do you guard against forgetting them?",
                "How can someone see God's provision repeatedly yet still doubt when new challenges arise?",
                "What's the difference between legitimate questioning and the sinful 'testing' of God condemned here?"
            ]
        },
        "10": {
            "analysis": "<strong>Forty years long was I grieved with this generation</strong> (אַרְבָּעִים שָׁנָה אָקוּט בְּדוֹר, <em>arba'im shanah akut b'dor</em>)—<em>Akut</em> means to feel loathing, disgust, grief. For <em>forty years</em>—an entire generation—God experienced grief over his people's unbelief. This anthropopathism (attributing human emotions to God) reveals God's heart: he doesn't coldly destroy rebels but grieves like a parent over wayward children. Genesis 6:6 similarly says God was 'grieved in his heart' before the flood. Ephesians 4:30 warns: 'Do not grieve the Holy Spirit.'<br><br><strong>And said, It is a people that do err in their heart</strong> (וָאֹמַר עַם תֹּעֵי לֵבָב הֵם, <em>va'omar am to'ei levav hem</em>)—God's diagnosis: <em>to'ei levav</em> (erring in heart, going astray in heart). The problem wasn't intellectual confusion but heart rebellion. <strong>And they have not known my ways</strong> (וְהֵם לֹא־יָדְעוּ דְרָכָי, <em>v'hem lo-yad'u d'rakhai</em>)—<em>Yada</em> (know) means experiential, intimate knowledge. They didn't <em>know</em> God's <em>ways</em> (character, patterns, methods) because they refused to trust and obey. Knowledge requires relationship; relationship requires trust.",
            "historical": "The forty years began at the golden calf incident (Exodus 32) and continued through rebellion at Kadesh-barnea (Numbers 13-14) until the last of that generation died (Numbers 26:65, Deuteronomy 2:14-16). Joshua and Caleb were exceptions because they wholly followed the LORD (Numbers 32:11-12). The number forty often signifies a complete period of testing in Scripture (Moses on Sinai, Elijah's journey, Jesus's temptation).",
            "questions": [
                "How does knowing that sin grieves God (not just angers him) affect how you view your disobedience?",
                "What does 'erring in heart' reveal about the root cause of spiritual wandering and doctrinal error?",
                "How do you grow in knowing God's ways rather than merely knowing about God?"
            ]
        },
        "11": {
            "analysis": "<strong>Unto whom I sware in my wrath</strong> (אֲשֶׁר־נִשְׁבַּעְתִּי בְאַפִּי, <em>asher-nishba'ti v'api</em>)—<em>Shaba</em> (to swear, take an oath) combined with <em>af</em> (anger, wrath) indicates a solemn divine oath pronounced in judgment. God bound himself by oath that the wilderness generation would not enter his rest. Numbers 14:21-23 records this oath: 'As I live... none of the men who have seen my glory and my signs... shall see the land.' God's oaths are irrevocable (Hebrews 6:17-18).<br><br><strong>That they should not enter into my rest</strong> (אִם־יְבֹאוּן אֶל־מְנוּחָתִי, <em>im-yevo'un el-m'nuchati</em>)—<em>Im</em> here is a negative oath formula: 'surely not!' <em>M'nuchah</em> (rest, resting place) primarily meant the Promised Land (Deuteronomy 12:9, Psalm 132:14), a place of security, peace, and provision after wilderness wandering. But Hebrews 3:7-4:11 applies this to eternal rest—the ultimate Sabbath rest for God's people. The wilderness generation's exclusion typifies all who reject God's provision: they cannot enter his rest. Only faith grants entrance (Hebrews 4:3).",
            "historical": "The generation that left Egypt never entered Canaan. They died in the wilderness over forty years (Numbers 26:64-65). Only their children, led by Joshua and Caleb, crossed the Jordan. Yet Hebrews argues that even Joshua didn't give them ultimate rest (Hebrews 4:8)—there remains a Sabbath rest for God's people, fulfilled in Christ. Unbelief excludes from rest in every generation.",
            "questions": [
                "What is the 'rest' that God offers, and how do people still miss it through unbelief today?",
                "How does Hebrews' application of this warning to Christians challenge presumptuous or nominal faith?",
                "What practices help you 'strive to enter that rest' (Hebrews 4:11) rather than hardening your heart?"
            ]
        }
    }
}

# Continue with remaining sections...
# Due to length, I'll add the remaining 51 verses in the next section

print("Partial commentary data structure created.")
print("This includes Psalm 86:12-17, 94:21-23, 95:8-11")
print("Remaining: 109:27-31, 112:10, 116:18-19, 118:25-29, 127:2-5, 133:2-3, 136:9-26, 137:9, 141:7-10, 144:12-15, 149:7-9")
