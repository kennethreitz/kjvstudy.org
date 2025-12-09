#!/usr/bin/env python3
"""Add scholarly theological commentary to missing verses."""

import json

# Load missing verses
with open('missing_verses.json') as f:
    verses_data = json.load(f)

# ============================================================================
# PROVERBS COMMENTARY
# ============================================================================

proverbs_commentary = {
    "27": {
        "18": {
            "analysis": "<strong>Whoso keepeth the fig tree shall eat the fruit thereof</strong> (שֹׁמֵר תְּאֵנָה יֹאכַל פִּרְיָהּ, <em>shomer te'enah yokhal piryah</em>)—the Hebrew verb שָׁמַר (<em>shamar</em>, 'to keep, guard, watch') emphasizes faithful, attentive care rather than mere ownership. Ancient fig trees required patient cultivation: pruning, protection from pests, watering during dry seasons.<br><br><strong>So he that waiteth on his master shall be honoured</strong> (שֹׁמֵר אֲדֹנָיו יְכֻבָּד, <em>shomer adonav yekhubbad</em>)—the parallel reveals vocational faithfulness as spiritual discipline. The term כָּבוֹד (<em>kavod</em>, 'honor, weight, glory') suggests not empty praise but substantial reward. Jesus extends this principle in the parable of the faithful servant (Luke 12:42-44), where stewardship leads to greater responsibility.",
            "historical": "In ancient Israelite agriculture, fig trees were among the most valuable assets, providing food, shade, and trade goods. Unlike grain harvests requiring seasonal labor, fig cultivation demanded year-round attention. Solomon's proverb reflects an agrarian economy where long-term faithfulness, not quick gains, produced wealth.",
            "questions": [
                "What 'fig tree' has God entrusted to your care that requires patient, long-term faithfulness?",
                "How does our culture's demand for instant results conflict with the biblical principle of faithful stewardship?",
                "In what ways might you be 'waiting on your Master' with the expectation of eternal honor rather than immediate recognition?"
            ]
        },
        "19": {
            "analysis": "<strong>As in water face answereth to face</strong> (כַּמַּיִם הַפָּנִים לַפָּנִים, <em>kamayim hapanim lapanim</em>)—the simile of water as mirror employs the ancient practice of seeing one's reflection in still water before polished metal mirrors became common. The Hebrew פָּנִים (<em>panim</em>, 'face') also carries connotations of presence, countenance, and inner disposition.<br><br><strong>So the heart of man to man</strong> (כֵּן לֵב־הָאָדָם לָאָדָם, <em>ken lev-ha'adam la'adam</em>)—the לֵב (<em>lev</em>, 'heart') in Hebrew encompasses mind, will, emotions, and moral character. This proverb reveals the profound truth of human interconnectedness: we know ourselves through relationships. Iron sharpens iron (Proverbs 27:17); water reflects water; hearts reveal hearts.",
            "historical": "Before glass mirrors (invented around 1st century AD), people saw their reflections in polished bronze, copper, or still pools of water. The clarity of self-knowledge paralleled the quality of reflection. This proverb dates from Solomon's era (10th century BC) when such reflections were common experiences.",
            "questions": [
                "Who in your life serves as a 'mirror' reflecting your true character back to you?",
                "What does your response to others reveal about the condition of your own heart?",
                "How does community and fellowship help you see yourself more clearly before God?"
            ]
        },
        "20": {
            "analysis": "<strong>Hell and destruction are never full</strong> (שְׁאוֹל וַאֲבַדּוֹ לֹא תִשְׂבַּעְנָה, <em>sheol va'abaddo lo tisba'enah</em>)—שְׁאוֹל (<em>Sheol</em>) denotes the realm of the dead, the grave that swallows all humanity; אֲבַדּוֹן (<em>Abaddon</em>, 'destruction, place of perishing') appears six times in Scripture, personified in Revelation 9:11 as the angel of the abyss. The verb שָׂבַע (<em>sava</em>, 'to be satisfied, filled') is negated absolutely.<br><br><strong>So the eyes of man are never satisfied</strong> (וְעֵינֵי הָאָדָם לֹא תִשְׂבַּעְנָה, <em>ve'einei ha'adam lo tisba'enah</em>)—human desire mirrors death's insatiability. John warns against 'the lust of the eyes' (1 John 2:16); Ecclesiastes declares all earthly pursuits vanity. Only in God do our souls find rest (Psalm 63:5).",
            "historical": "Ancient Israelites viewed Sheol as an ever-hungry mouth (Isaiah 5:14, Habakkuk 2:5), swallowing the dead without distinction between righteous and wicked. This proverb reflects the wisdom tradition's meditation on human mortality and desire, themes fully developed in Ecclesiastes.",
            "questions": [
                "What desires in your life function like Sheol—never satisfied no matter how much you feed them?",
                "How does consumerism exploit the principle that 'the eyes of man are never satisfied'?",
                "Where have you found genuine satisfaction that transcends the endless cycle of desire?"
            ]
        },
        "21": {
            "analysis": "<strong>As the fining pot for silver, and the furnace for gold</strong> (מַצְרֵף לַכֶּסֶף וְכוּר לַזָּהָב, <em>matzeref lakkesef ve'khur lazahav</em>)—the מַצְרֵף (<em>matzeref</em>, 'crucible, refining pot') and כּוּר (<em>kur</em>, 'furnace') test metal purity by extreme heat, burning away dross. Malachi 3:2-3 uses this imagery for God's refining work.<br><br><strong>So is a man to his praise</strong> (וְאִיש לְפִי מְהַלְלוֹ, <em>ve'ish lefi mehallelo</em>)—how a man handles תְּהִלָּה (<em>tehillah</em>, 'praise, commendation') reveals his character. Does praise produce humility or arrogance? Gratitude or entitlement? The test of success often proves harder than the test of adversity. Herod accepted worship and was struck down (Acts 12:21-23); David deflected glory to God (2 Samuel 7:18-29).",
            "historical": "Ancient metalworking required intense heat (over 1000°C for gold) to separate precious metal from impurities. Refiners watched the molten metal until they could see their reflection in its surface—a picture of God's refining work continuing until He sees His image in us (2 Corinthians 3:18).",
            "questions": [
                "How do you respond when praised—with pride, deflection to God, or awkward dismissal?",
                "What does your reaction to recognition reveal about your identity and security?",
                "Can you identify ways God has used both adversity and success to refine your character?"
            ]
        },
        "22": {
            "analysis": "<strong>Though thou shouldest bray a fool in a mortar among wheat with a pestle</strong> (אִם־תִּכְתּוֹשׁ אֶת־הָאֱוִיל בַּמַּכְתֵּשׁ בְּתוֹךְ הָרִיפוֹת בַּעֱלִי, <em>im-tikhtosh et-ha'evil bamakhitesh betokh harifot ba'eli</em>)—the graphic imagery employs כָּתַשׁ (<em>katash</em>, 'to pound, beat') and מַכְתֵּשׁ (<em>makhtesh</em>, 'mortar'), tools for grinding grain with an עֱלִי (<em>eli</em>, 'pestle'). The violent action suggests extreme measures applied to the אֱוִיל (<em>evil</em>, 'fool').<br><br><strong>Yet will not his foolishness depart from him</strong> (לֹא־תָסוּר מֵעָלָיו אִוַּלְתּוֹ, <em>lo-tasur me'alav ivvalto</em>)—the אִוֶּלֶת (<em>ivvelet</em>, 'folly, foolishness') remains immovable. Proverbs distinguishes the פֶּתִי (<em>peti</em>, 'simple one' who can learn) from the אֱוִיל ('fool' who rejects correction) and the לֵץ (<em>lets</em>, 'scoffer' who mocks wisdom). This fool has hardened beyond discipline's reach—a sobering warning about the calcification of character.",
            "historical": "Mortars and pestles were ubiquitous in ancient Near Eastern households for grinding grain, spices, and herbs. The proverb's hyperbole—grinding a person like grain—would have immediately communicated the futility of trying to reform someone who refuses correction. Even the most forceful discipline cannot change a hardened fool.",
            "questions": [
                "Are there areas of your life where you're resisting correction, risking the hardening of folly?",
                "How can you cultivate a teachable spirit that remains soft to God's discipline?",
                "Who in your life might need your prayers more than your correction, having hardened against instruction?"
            ]
        },
        "23": {
            "analysis": "<strong>Be thou diligent to know the state of thy flocks</strong> (יָדֹעַ תֵּדַע פְּנֵי צֹאנֶךָ, <em>yado'a teda penei tzonekha</em>)—the emphatic doubling of יָדַע (<em>yada</em>, 'to know') creates an intensive imperative: 'knowing, know!' This is intimate, experiential knowledge, not mere information. The פָּנִים (<em>panim</em>, 'face') of the flock suggests personal attention to each animal's condition.<br><br><strong>And look well to thy herds</strong> (שִׁית לִבְּךָ לַעֲדָרִים, <em>shit libekha la'adarim</em>)—literally 'set your heart to the herds.' The לֵב (<em>lev</em>, 'heart') again emphasizes not casual observation but devoted attention. This begins a five-verse unit (23-27) on stewardship and providence, teaching that faithful management of God's gifts secures lasting provision. Jesus's parable of the talents (Matthew 25:14-30) extends this principle to all divine entrustments.",
            "historical": "In ancient Israel's pastoral economy, wealth consisted primarily in livestock. Unlike modern absentee ownership, biblical shepherding required personal, daily involvement. David's faithfulness as a shepherd prepared him for kingship (1 Samuel 17:34-37). The imagery would resonate deeply in an agrarian society where negligent stewardship meant ruin.",
            "questions": [
                "What 'flocks' has God entrusted to your stewardship—family, ministry, work, resources?",
                "Are you giving personal, attentive care to what God has given you, or merely managing from a distance?",
                "How does faithful stewardship of earthly resources prepare you for eternal responsibilities?"
            ]
        },
        "24": {
            "analysis": "<strong>For riches are not for ever</strong> (כִּי לֹא לְעוֹלָם חֹסֶן, <em>ki lo le'olam chosen</em>)—חֹסֶן (<em>chosen</em>, 'wealth, riches, treasure') lacks permanence; לְעוֹלָם (<em>le'olam</em>, 'forever, perpetually') is negated. What seems solid proves transient. James 5:2-3 warns the wealthy: 'Your riches are corrupted... your gold and silver is cankered.'<br><br><strong>And doth the crown endure to every generation?</strong> (וְאִם־נֵזֶר לְדוֹר וָדוֹר, <em>ve'im-nezer ledor vador</em>)—the rhetorical question expects a negative answer. Even the נֵזֶר (<em>nezer</em>, 'crown, diadem')—symbol of ultimate earthly power—passes from דּוֹר (<em>dor</em>, 'generation') to generation. Solomon, possessing unparalleled wealth and power, understood their impermanence. Only God's kingdom endures forever (Daniel 4:34); storing treasure in heaven proves the wise investment (Matthew 6:19-20).",
            "historical": "Solomon wrote from experience—his vast wealth (1 Kings 10:14-29) and the succession of Israelite dynasties demonstrated that neither riches nor royal power guaranteed permanence. Within a generation of Solomon's death, the kingdom split; later, both Israel and Judah fell. The proverb's wisdom proved prophetically accurate.",
            "questions": [
                "What are you building your security upon—temporary riches or eternal treasure?",
                "How does the impermanence of wealth and power challenge your priorities and investments?",
                "What can you invest in today that will endure 'from generation to generation'?"
            ]
        },
        "25": {
            "analysis": "<strong>The hay appeareth, and the tender grass sheweth itself</strong> (גָּלָה חָצִיר וְנִרְאָה־דֶשֶׁא, <em>galah chatzir ve'nir'ah-deshe</em>)—the agricultural cycle continues: חָצִיר (<em>chatzir</em>, 'grass, hay') is revealed (גָּלָה, <em>galah</em>, 'to uncover, disclose') as mature growth, while דֶּשֶׁא (<em>deshe</em>, 'tender grass, vegetation') appears as new growth.<br><br><strong>And herbs of the mountains are gathered</strong> (וְנֶאֶסְפוּ עִשְּׂבוֹת הָרִים, <em>ve'ne'esfu issvot harim</em>)—the verb אָסַף (<em>asaf</em>, 'to gather, collect') suggests intentional harvesting. This verse continues the stewardship theme (verses 23-27): nature's reliable cycles reward the diligent manager. God's creation operates by faithful rhythms (Genesis 8:22); human responsibility is to work in harmony with divine providence, neither presuming on tomorrow nor despising today's provision.",
            "historical": "Ancient Israel's agricultural calendar structured life around planting (October-November), winter rains (December-February), spring harvest (March-May), and summer drought (June-September). Mountain herbs provided supplemental fodder during dry seasons. The proverb assumes intimate knowledge of these cycles—wisdom lost in modern urbanization.",
            "questions": [
                "How aware are you of the 'seasons' and rhythms God has established in your life and work?",
                "Are you harvesting opportunities when they appear, or letting them pass unharvested?",
                "What does patient attention to natural cycles teach about trusting God's provision?"
            ]
        },
        "26": {
            "analysis": "<strong>The lambs are for thy clothing</strong> (כְּבָשִׂים לִלְבוּשֶׁךָ, <em>kevasim livushekha</em>)—כֶּבֶשׂ (<em>keves</em>, 'lamb, sheep') provides לְבוּשׁ (<em>levush</em>, 'clothing, garment') through wool. The plural suggests sustainable yield: proper management allows shearing without slaughtering the flock.<br><br><strong>And the goats are the price of the field</strong> (וּמְחִיר שָׂדֶה עַתּוּדִים, <em>umechir sadeh attudim</em>)—עַתּוּד (<em>attud</em>, 'male goat, he-goat') serves as מְחִיר (<em>mechir</em>, 'price, payment') for acquiring or maintaining the שָׂדֶה (<em>sadeh</em>, 'field, cultivated land'). The economic principle: faithful stewardship creates a self-sustaining cycle where assets generate resources for acquiring more productive capacity. This is biblical prosperity—not getting rich quick, but patient multiplication of God's entrustments (compare the parable of the minas, Luke 19:11-27).",
            "historical": "In ancient agrarian economies, livestock served multiple functions: food (milk, meat), clothing (wool, leather), capital (breeding stock), and currency (trade, dowry, tribute). A well-managed flock provided sustainable income without depleting the principal—precisely the economic wisdom this passage teaches. Biblical stewardship emphasizes multiplication through faithful management.",
            "questions": [
                "How are you managing God's resources to create sustainable provision rather than short-term consumption?",
                "What 'assets' has God given you that, properly tended, could multiply provision for others?",
                "Where might you be consuming 'seed corn' that should be invested for future harvest?"
            ]
        },
        "27": {
            "analysis": "<strong>And thou shalt have goats' milk enough for thy food</strong> (וְדֵי חֲלֵב עִזִּים לְלַחְמֶךָ, <em>vedei chalev izzim lelahmekha</em>)—דַּי (<em>dai</em>, 'sufficiency, enough') modifies חָלָב (<em>chalav</em>, 'milk'); עֵז (<em>ez</em>, 'goat') produces abundant, nourishing milk. לֶחֶם (<em>lechem</em>, 'bread, food') represents complete sustenance.<br><br><strong>For the food of thy household, and for the maintenance for thy maidens</strong> (לְלֶחֶם בֵּיתֶךָ וְחַיִּים לְנַעֲרוֹתֶיךָ, <em>lelechem beitekha vechayim lena'arotekha</em>)—the provision extends to בַּיִת (<em>bayit</em>, 'household, family') and נַעֲרָה (<em>na'arah</em>, 'young woman, maidservant'). The word חַיִּים (<em>chayyim</em>, 'life, living, sustenance') emphasizes not mere survival but flourishing life. This concluding verse of the stewardship unit (23-27) reveals the goal: faithful management provides abundantly for one's entire household. Paul echoes this: 'If anyone does not provide for his own... he has denied the faith' (1 Timothy 5:8).",
            "historical": "Goat's milk was a staple in ancient Near Eastern diets—more digestible than cow's milk, rich in nutrients, and goats thrived in Israel's rocky terrain where cattle struggled. A household's ability to provide for servants demonstrated both prosperity and proper management. Biblical household codes consistently emphasize masters' responsibility to provide for those under their care (Ephesians 6:9, Colossians 4:1).",
            "questions": [
                "Are you managing your resources to provide not only for yourself but for your entire household?",
                "How does this vision of sustainable provision challenge modern consumerism and debt culture?",
                "What does 'enough' look like in your life—and are you content with God's sufficient provision?"
            ]
        }
    },
    "28": {
        "14": {
            "analysis": "<strong>Happy is the man that feareth alway</strong> (אַשְׁרֵי אָדָם מְפַחֵד תָּמִיד, <em>ashrei adam mefached tamid</em>)—אַשְׁרֵי (<em>ashrei</em>, 'blessed, happy') opens the Psalter (Psalm 1:1) and marks the truly flourishing life. מְפַחֵד (<em>mefached</em>, 'fearing, being in awe') modifies פַּחַד (<em>pachad</em>, 'fear, dread, reverence'); תָּמִיד (<em>tamid</em>, 'continually, always') makes this not occasional but habitual. This is not paranoia but perpetual God-consciousness—the fear of the LORD that is the beginning of wisdom (Proverbs 9:10).<br><br><strong>But he that hardeneth his heart shall fall into mischief</strong> (וּמַקְשֶׁה לִבּוֹ יִפּוֹל בְּרָעָה, <em>umaqsheh libbo yippol bera'ah</em>)—קָשָׁה (<em>qashah</em>, 'to be hard, stiff, stubborn') describes the calcified לֵב (<em>lev</em>, 'heart'). Pharaoh's hardened heart (Exodus 7-14) exemplifies this warning. The result: נָפַל (<em>nafal</em>, 'to fall, collapse') into רָעָה (<em>ra'ah</em>, 'evil, calamity, disaster'). Proverbs constantly contrasts the soft, teachable heart with the hard, rebellious one.",
            "historical": "The 'fear of the LORD' permeates Israel's wisdom tradition—not terror but awe-filled reverence before the Almighty. Conversely, hardened hearts marked Israel's rebellions (Psalm 95:8, Hebrews 3:7-8). This proverb, from Solomon's era, would echo through centuries of prophetic warnings against stubborn hearts (Jeremiah 7:24, Ezekiel 3:7).",
            "questions": [
                "What does it mean for you to 'fear always'—to maintain continual awareness of God's presence?",
                "Where might your heart be hardening against God's correction or leading?",
                "How can you cultivate a tender, responsive heart that remains soft to the Holy Spirit's conviction?"
            ]
        },
        "15": {
            "analysis": "<strong>As a roaring lion, and a ranging bear</strong> (אֲרִי־נֹהֵם וְדֹב שׁוֹקֵק, <em>ari-nohem vedov shoqeq</em>)—אֲרִי (<em>ari</em>, 'lion') that נָהַם (<em>naham</em>, 'roars, growls') and דֹּב (<em>dov</em>, 'bear') that שָׁקַק (<em>shaqaq</em>, 'ranges, rushes, seeks prey') are apex predators, feared throughout Scripture. The roaring lion signals the kill (Psalm 22:13); the charging bear, proverbial ferocity (2 Samuel 17:8; Hosea 13:8).<br><br><strong>So is a wicked ruler over the poor people</strong> (מֹשֵׁל רָשָׁע עַל עַם־דָּל, <em>moshel rasha al am-dal</em>)—the רָשָׁע (<em>rasha</em>, 'wicked, guilty, criminal') מֹשֵׁל (<em>moshel</em>, 'ruler, governor') preys upon עַם־דָּל (<em>am-dal</em>, 'poor people, weak folk'). This isn't governance but predation. Scripture consistently champions justice for the poor (Psalm 82:3-4); tyrants who exploit the vulnerable face divine judgment (Ezekiel 34:1-10). Rome's tyranny exemplified this in Jesus's era; Revelation depicts imperial power as a beast (Revelation 13).",
            "historical": "Ancient Near Eastern kings frequently portrayed themselves as lions—symbols of power. But Proverbs subverts this: the wicked ruler is not majestic but predatory, terrorizing the vulnerable. Israel experienced such rulers (1 Kings 12:1-19, Rehoboam's oppression), and the prophets thundered against those who devoured God's people (Ezekiel 22:25-29).",
            "questions": [
                "How should Christians respond to governing authorities who act as 'roaring lions' toward the vulnerable?",
                "Where do you see exploitation of the weak—and what is your responsibility to intervene?",
                "If you hold authority over others, how can you ensure you're shepherding rather than predating?"
            ]
        },
        "16": {
            "analysis": "<strong>The prince that wanteth understanding is also a great oppressor</strong> (נָגִיד חֲסַר תְּבוּנוֹת וְרַב מַעֲשַׁקּוֹת, <em>nagid chasar tevunot verav ma'ashaqqot</em>)—נָגִיד (<em>nagid</em>, 'prince, ruler, leader') who is חָסֵר (<em>chaser</em>, 'lacking, devoid of') תְּבוּנָה (<em>tevunah</em>, 'understanding, insight, intelligence') becomes רַב (<em>rav</em>, 'great, abundant in') מַעֲשָׁקָּה (<em>ma'ashaqqah</em>, 'oppression, extortion'). Ignorant leadership multiplies injustice—not from malice but from incompetence.<br><br><strong>But he that hateth covetousness shall prolong his days</strong> (שֹׂנֵא בֶצַע יַאֲרִיךְ יָמִים, <em>sone vetza ya'arikh yamim</em>)—שָׂנֵא (<em>sane</em>, 'to hate, detest') toward בֶּצַע (<em>betza</em>, 'unjust gain, dishonest profit, greed') leads to אָרַךְ (<em>arakh</em>, 'to lengthen, prolong') of יָמִים (<em>yamim</em>, 'days, life'). Rejecting corrupt gain secures lasting life. Jethro counseled Moses to appoint leaders who 'hate covetousness' (Exodus 18:21); greed shortened Achan's days (Joshua 7) and Judas's (Matthew 27:3-5).",
            "historical": "Ancient kingship concentrated vast power; without wisdom, rulers became tyrants. Solomon's prayer for wisdom rather than wealth (1 Kings 3:9-12) stands as the ideal; Rehoboam's foolishness split the kingdom (1 Kings 12). The Dead Sea Scrolls emphasize that Israel's future messianic king must be wise, not merely powerful.",
            "questions": [
                "How does this proverb challenge the idea that 'good intentions' excuse incompetent leadership?",
                "What areas of influence in your life require greater understanding to avoid unwitting oppression?",
                "Where might covetousness be subtly shortening your effectiveness and legacy?"
            ]
        },
        "17": {
            "analysis": "<strong>A man that doeth violence to the blood of any person shall flee to the pit</strong> (אָדָם עָשֻׁק בְּדַם־נֶפֶשׁ עַד־בּוֹר יָנוּס, <em>adam ashuq bedam-nefesh ad-bor yanus</em>)—עָשַׁק (<em>ashaq</em>, 'oppressed, burdened') by דָּם (<em>dam</em>, 'blood') of נֶפֶשׁ (<em>nefesh</em>, 'soul, life, person') indicates guilt for murder. This one יָנוּס (<em>yanus</em>, 'flees, runs away') to the בּוֹר (<em>bor</em>, 'pit, cistern, grave')—whether execution or death fleeing justice.<br><br><strong>Let no man stay him</strong> (אַל־יִתְמְכוּ־בוֹ, <em>al-yitmeku-vo</em>)—the prohibition: none should תָּמַךְ (<em>tamakh</em>, 'support, uphold, sustain') the murderer. This is not vigilante violence but rejection of harboring the guilty. Cities of refuge (Numbers 35) protected the accidental killer but not the intentional murderer. Genesis 9:6 establishes the sanctity of human life: 'Whoso sheddeth man's blood, by man shall his blood be shed.'",
            "historical": "Ancient Israel's law distinguished intentional murder from accidental homicide (Exodus 21:12-14, Deuteronomy 19:1-13). Cities of refuge protected the latter; the former faced execution. The avenger of blood pursued murderers who forfeited the right to protection. This proverb reinforces capital punishment for murder, established from Noah onward (Genesis 9:6).",
            "questions": [
                "How does this proverb uphold the sanctity and value of human life?",
                "What does it mean to 'stay' (support) someone who is guilty of bloodshed—and why is this forbidden?",
                "How should justice and mercy interact when dealing with violent offenders?"
            ]
        },
        "18": {
            "analysis": "<strong>Whoso walketh uprightly shall be saved</strong> (הוֹלֵךְ תָּמִים יִוָּשֵׁעַ, <em>holekh tamim yivvashea</em>)—הָלַךְ (<em>halakh</em>, 'to walk, go, behave') describes the תָּמִים (<em>tamim</em>, 'blameless, complete, having integrity') life. This one will be יָשַׁע (<em>yasha</em>, 'saved, delivered, rescued'). Note: תָּמִים does not mean sinless perfection but wholehearted devotion, walking in covenant faithfulness (Genesis 17:1, 'Walk before me and be blameless').<br><br><strong>But he that is perverse in his ways shall fall at once</strong> (וְנֶעְקַשׁ דְּרָכַיִם יִפּוֹל בְּאֶחָת, <em>vene'qash derakhayim yippol be'echat</em>)—עָקַשׁ (<em>aqash</em>, 'twisted, crooked, perverse') in דֶּרֶךְ (<em>derekh</em>, 'way, path, manner of life') results in נָפַל (<em>nafal</em>, 'to fall, collapse') בְּאֶחָת (<em>be'echat</em>, 'at once, suddenly, in one moment'). Integrity brings gradual deliverance; duplicity brings sudden destruction. Ananias and Sapphira exemplify this principle (Acts 5:1-11).",
            "historical": "The metaphor of 'walking' pervades biblical ethics—not static belief but dynamic obedience. Israel's covenant called for walking in God's ways (Deuteronomy 5:33, 8:6). The wisdom tradition consistently contrasts the straight path of the righteous with the crooked path of the wicked (Proverbs 2:15, 4:18-19).",
            "questions": [
                "In what areas of life might you be walking 'perversely' (with a divided heart) rather than 'uprightly' (with integrity)?",
                "How does the promise of being 'saved' through upright living relate to salvation by grace through faith?",
                "What crooked paths are you tempted to take that promise shortcuts but threaten sudden collapse?"
            ]
        },
        "19": {
            "analysis": "<strong>He that tilleth his land shall have plenty of bread</strong> (עֹבֵד אַדְמָתוֹ יִשְׂבַּע־לָחֶם, <em>oved admato yisba-lachem</em>)—עָבַד (<em>avad</em>, 'to work, serve, till') the אֲדָמָה (<em>adamah</em>, 'ground, land, soil') produces שָׂבַע (<em>sava</em>, 'abundance, satisfaction') of לֶחֶם (<em>lechem</em>, 'bread, food'). This repeats Proverbs 12:11, emphasizing that honest labor yields provision. From Eden, humanity's mandate included work (Genesis 2:15); the curse made it toilsome (Genesis 3:17-19), but diligence still brings reward.<br><br><strong>But he that followeth after vain persons shall have poverty enough</strong> (וּמְרַדֵּף רֵיקִים יִשְׂבַּע־רִישׁ, <em>umraddaf reiqim yisba-rish</em>)—רָדַף (<em>radaf</em>, 'to pursue, chase after') רֵיק (<em>req</em>, 'empty, vain, worthless') people leads to שָׂבַע (<em>sava</em>, 'abundance') of רֵישׁ (<em>resh</em>, 'poverty, want'). Ironic parallelism: diligence brings plenty; chasing fantasies brings plenty—of poverty. Proverbs 13:20 warns: 'He that walketh with wise men shall be wise: but a companion of fools shall be destroyed.'",
            "historical": "Ancient Israel's agricultural economy made the contrast vivid: the farmer who worked his field prospered; the fool who chased schemes or loafed with idlers faced destitution. Paul's missionary work included tentmaking (Acts 18:3); he commanded, 'If any would not work, neither should he eat' (2 Thessalonians 3:10).",
            "questions": [
                "What 'fields' has God given you to till—and are you working them diligently?",
                "Who are the 'vain persons' (empty people, get-rich-quick schemers) that might be distracting you from faithful labor?",
                "How does contentment with honest work combat the allure of shortcuts and schemes?"
            ]
        },
        "20": {
            "analysis": "<strong>A faithful man shall abound with blessings</strong> (אִישׁ אֱמוּנוֹת רַב־בְּרָכוֹת, <em>ish emunot rav-berakhot</em>)—אִישׁ אֱמוּנָה (<em>ish emunah</em>, 'man of faithfulness, trustworthiness, steadfastness') will have רַב (<em>rav</em>, 'many, abundant') בְּרָכָה (<em>berakhah</em>, 'blessings'). אֱמוּנָה shares roots with אָמֵן (<em>amen</em>)—firmness, reliability, faithfulness. Jesus's parable: 'Well done, good and faithful servant... enter thou into the joy of thy lord' (Matthew 25:21).<br><br><strong>But he that maketh haste to be rich shall not be innocent</strong> (וְאָץ לְהַעֲשִׁיר לֹא יִנָּקֶה, <em>ve'atz leha'ashir lo yinnaqqeh</em>)—אוּץ (<em>uts</em>, 'to hasten, hurry, press') toward עָשַׁר (<em>ashar</em>, 'to be rich, wealthy') will not be נָקָה (<em>naqqah</em>, 'innocent, clean, unpunished'). Getting rich quick requires compromises, corner-cutting, exploitation. Proverbs 13:11: 'Wealth gotten by vanity shall be diminished: but he that gathereth by labour shall increase.'",
            "historical": "Ancient commerce offered many temptations to dishonest gain—false weights, deceptive contracts, exploitative lending. Israel's law prohibited such practices (Leviticus 19:35-36, Deuteronomy 25:13-16). The contrast: faithful, patient work brings blessing; greedy haste brings guilt and eventual loss.",
            "questions": [
                "In what areas of life are you being faithful rather than seeking quick results?",
                "What shortcuts to wealth or success tempt you to compromise integrity?",
                "How does this proverb challenge prosperity gospel teaching that equates faith with rapid financial gain?"
            ]
        },
        "21": {
            "analysis": "<strong>To have respect of persons is not good</strong> (הַכֵּר־פָּנִים לֹא־טוֹב, <em>hakker-panim lo-tov</em>)—נָכַר פָּנִים (<em>nakar panim</em>, 'to recognize faces, show partiality') is לֹא־טוֹב (<em>lo-tov</em>, 'not good'). This Hebrew idiom for favoritism appears throughout Scripture (Leviticus 19:15, Deuteronomy 16:19). James 2:1-9 condemns partiality in the church; God Himself 'regardeth not persons' (Deuteronomy 10:17).<br><br><strong>For for a piece of bread that man will transgress</strong> (וְעַל־פַּת־לֶחֶם יִפְשַׁע־גָבֶר, <em>ve'al-pat-lechem yifsha-gaver</em>)—the second line reveals the danger: for a mere פַּת לֶחֶם (<em>pat lechem</em>, 'piece of bread, morsel'), a man will פָּשַׁע (<em>pasha</em>, 'transgress, rebel, sin'). Once favoritism becomes habitual, judges and leaders can be bought for nothing. Corruption begins with small compromises; soon, justice is sold for trifles. Micah 7:3 laments: 'The prince asketh, and the judge asketh for a reward.'",
            "historical": "Ancient Near Eastern legal systems struggled with judicial corruption—the powerful bribing judges to oppress the poor. Israel's law prohibited taking bribes (Exodus 23:8), yet the prophets constantly condemned corrupt judges (Isaiah 1:23, 5:23, Amos 5:12). This proverb exposes how small compromises lead to total corruption.",
            "questions": [
                "Where might you be showing partiality—favoring the wealthy, attractive, or influential over others?",
                "What 'small' compromises might be conditioning you to larger injustices?",
                "How can you cultivate the practice of treating all people with equal dignity, reflecting God's impartiality?"
            ]
        },
        "22": {
            "analysis": "<strong>He that hasteth to be rich hath an evil eye</strong> (נִבְהָל לְהוֹן אִישׁ עַיִן רָע, <em>nivhal lehon ish ayin ra</em>)—נִבְהָל (<em>nivhal</em>, 'hastening, hurrying') toward הוֹן (<em>hon</em>, 'wealth, riches') reveals עַיִן רָע (<em>ayin ra</em>, 'evil eye'), a Hebrew idiom for stinginess, envy, and greed. Jesus warns against this 'evil eye' (Matthew 6:22-23, 20:15). The greedy person's vision is distorted—seeing others as competition, God's gifts as insufficient.<br><br><strong>And considereth not that poverty shall come upon him</strong> (וְלֹא־יֵדַע כִּי־חֶסֶר יְבֹאֶנּוּ, <em>velo-yeda ki-cheser yevo'ennu</em>)—יָדַע (<em>yada</em>, 'to know, understand') is negated: he does not know that חֶסֶר (<em>cheser</em>, 'want, lack, poverty') approaches. Proverbs repeatedly warns that greed leads to poverty (Proverbs 11:24, 13:11). 'He that loveth silver shall not be satisfied with silver' (Ecclesiastes 5:10); the insatiable appetite for more guarantees eventual loss.",
            "historical": "First-century Palestine saw dramatic wealth disparities, with wealthy landowners exploiting peasant farmers. Jesus's parables frequently address greed (Luke 12:13-21, the rich fool; Luke 16:19-31, the rich man and Lazarus). Paul commands contentment: 'Having food and raiment let us be therewith content' (1 Timothy 6:8).",
            "questions": [
                "How can you recognize whether you have an 'evil eye'—a greedy, envious disposition?",
                "What warning signs indicate you're 'hastening to be rich' rather than trusting God's provision?",
                "Where has greed paradoxically led to poverty in your life—relational, spiritual, or even material?"
            ]
        },
        "23": {
            "analysis": "<strong>He that rebuketh a man afterwards shall find more favour</strong> (מוֹכִיחַ אָדָם אַחֲרַי חֵן יִמְצָא, <em>mokhiach adam acharai chen yimtsa</em>)—מוֹכִיחַ (<em>mokhiach</em>, 'one who rebukes, reproves, corrects') brings אַחֲרַי (<em>acharai</em>, 'afterward, later') the discovery (מָצָא, <em>matsa</em>) of חֵן (<em>chen</em>, 'favor, grace'). Initially painful, faithful correction produces later gratitude. Proverbs 27:6: 'Faithful are the wounds of a friend; but the kisses of an enemy are deceitful.'<br><br><strong>Than he that flattereth with the tongue</strong> (מִמַּחֲלִיק לָשׁוֹן, <em>mimachaliq lashon</em>)—חָלַק (<em>chalaq</em>, 'to be smooth, slippery, flattering') with the לָשׁוֹן (<em>lashon</em>, 'tongue') produces immediate pleasure but eventual harm. Flattery deceives, rebounds, and destroys relationships. Paul refused such tactics: 'For neither at any time used we flattering words' (1 Thessalonians 2:5). True love speaks truth (Ephesians 4:15).",
            "historical": "Ancient royal courts were notorious for flattering courtiers who told kings what they wanted to hear. True prophets brought rebuke (Nathan to David, 2 Samuel 12; Micaiah to Ahab, 1 Kings 22) and faced hostility—but history vindicated them. Proverbs advocates the prophetic courage to speak uncomfortable truth.",
            "questions": [
                "Who in your life loves you enough to rebuke you—and are you receiving their correction with gratitude?",
                "Where might you be flattering rather than speaking truth, seeking immediate approval over long-term benefit?",
                "How can you cultivate both the courage to rebuke when necessary and the humility to receive rebuke?"
            ]
        },
        "24": {
            "analysis": "<strong>Whoso robbeth his father or his mother, and saith, It is no transgression</strong> (גּוֹזֵל אָבִיו וְאִמּוֹ וְאֹמֵר אֵין־פָּשַׁע, <em>gozel aviv ve'immo ve'omer ein-pasha</em>)—גָּזַל (<em>gazal</em>, 'to rob, plunder, tear away violently') from אָב (<em>av</em>, 'father') and אֵם (<em>em</em>, 'mother') while claiming אֵין פֶּשַׁע (<em>ein pesha</em>, 'no transgression, no sin') reveals radical moral blindness. Jesus condemned the Corban tradition that evaded parental support (Mark 7:9-13): 'Ye say, If a man shall say to his father or mother, It is Corban... he shall be free.'<br><br><strong>The same is the companion of a destroyer</strong> (חָבֵר הוּא לְאִישׁ מַשְׁחִית, <em>chaver hu le'ish mashchit</em>)—חָבֵר (<em>chaver</em>, 'companion, associate, partner') with אִישׁ מַשְׁחִית (<em>ish mashchit</em>, 'man of destruction, one who ruins/destroys'). Such behavior aligns one with those who tear down rather than build. The fifth commandment (Exodus 20:12) promises long life for honoring parents; this proverb shows the inverse—robbing parents associates one with death-dealers.",
            "historical": "Ancient Near Eastern societies considered parental care a sacred duty. Adult children supported aging parents who had no social security system. Jesus's anger at Corban abuse (first-century Pharisaic loophole allowing vows to temple to override parental support) shows how seriously He took this command. Paul echoes it: 'If any provide not for his own... he hath denied the faith' (1 Timothy 5:8).",
            "questions": [
                "Are you caring for your aging parents according to biblical commands, or finding loopholes?",
                "What rationalizations might you use to justify withholding support or honor from parents?",
                "How does proper honor of parents reflect honoring God, who commands it?"
            ]
        },
        "25": {
            "analysis": "<strong>He that is of a proud heart stirreth up strife</strong> (רְחַב־לֵב יְגָרֶה מָדוֹן, <em>rechav-lev yegareh madon</em>)—רָחָב (<em>rachav</em>, 'wide, broad') לֵב (<em>lev</em>, 'heart') suggests arrogance, the inflated ego. This גָּרָה (<em>garah</em>, 'stirs up, provokes') מָדוֹן (<em>madon</em>, 'strife, contention, quarreling'). Pride demands its way, refuses correction, resents challenges. Proverbs 13:10: 'Only by pride cometh contention.' James 4:1-2 traces wars to selfish desires.<br><br><strong>But he that putteth his trust in the LORD shall be made fat</strong> (וּבוֹטֵחַ עַל־יְהוָה יְדֻשָּׁן, <em>uvoteach al-YHWH yedusshan</em>)—בָּטַח (<em>batach</em>, 'to trust, be confident, secure') in יהוה (YHWH, the covenant name of God) results in דָּשֵׁן (<em>dashen</em>, 'to be fat, prosperous, flourishing'). Biblical 'fatness' symbolizes abundant blessing (Genesis 27:28, Psalm 36:8). Security rooted in God produces peace; pride produces conflict. Humility trusts God's vindication; pride demands self-vindication.",
            "historical": "Israel's history repeatedly demonstrated this principle: humble trust brought prosperity (Jehoshaphat, 2 Chronicles 20); proud self-reliance brought disaster (Uzziah, 2 Chronicles 26:16-21). Jesus embodied ultimate humility (Philippians 2:5-11), entrusting Himself to the Father; God exalted Him to the highest place.",
            "questions": [
                "Where does pride create strife in your relationships—and how might humility bring peace?",
                "What insecurities drive your need to be right, to win arguments, to defend yourself?",
                "How would deeper trust in God's vindication free you from proud self-assertion?"
            ]
        },
        "26": {
            "analysis": "<strong>He that trusteth in his own heart is a fool</strong> (בּוֹטֵחַ בְּלִבּוֹ הוּא כְסִיל, <em>boteach belibbo hu khesil</em>)—בָּטַח (<em>batach</em>, 'to trust, be confident') in one's own לֵב (<em>lev</em>, 'heart, mind, inner self') makes one a כְּסִיל (<em>kesil</em>, 'fool, dullard'). Jeremiah 17:9 explains why: 'The heart is deceitful above all things, and desperately wicked: who can know it?' Self-trust is folly because the self deceives. Modern 'follow your heart' advice is anti-biblical—our hearts need transformation, not trust.<br><br><strong>But whoso walketh wisely, he shall be delivered</strong> (וְהוֹלֵךְ בְּחָכְמָה הוּא יִמָּלֵט, <em>veholekh vechokhmah hu yimmalet</em>)—הָלַךְ (<em>halakh</em>, 'to walk, go') in חָכְמָה (<em>chokhmah</em>, 'wisdom') leads to מָלַט (<em>malat</em>, 'to escape, be delivered, slip away'). Wisdom means submitting to God's revelation rather than inner feelings. Proverbs 3:5-6: 'Trust in the LORD with all thine heart; and lean not unto thine own understanding.'",
            "historical": "Ancient Near Eastern wisdom literature consistently warned against trusting human wisdom apart from divine guidance. Egypt's wisdom literature similarly emphasized the limits of human understanding. Israel's distinctive contribution was identifying true wisdom with the fear of YHWH (Proverbs 9:10)—wisdom is not human achievement but divine gift received through revelation and obedience.",
            "questions": [
                "In what areas are you trusting your own judgment rather than seeking God's wisdom in Scripture?",
                "How does modern culture's 'trust yourself' mantra conflict with biblical wisdom?",
                "What practices help you 'walk wisely' by submitting your heart to God's Word?"
            ]
        },
        "27": {
            "analysis": "<strong>He that giveth unto the poor shall not lack</strong> (נוֹתֵן לָרָשׁ אֵין מַחְסוֹר, <em>noten larash ein machsor</em>)—נָתַן (<em>natan</em>, 'to give') to the רָשׁ (<em>rash</em>, 'poor, destitute') results in אֵין מַחְסוֹר (<em>ein machsor</em>, 'no lack, no want'). This paradox pervades Scripture: giving produces abundance (Proverbs 11:24-25, 19:17, 22:9). Jesus taught: 'Give, and it shall be given unto you' (Luke 6:38). Paul: 'He which soweth bountifully shall reap also bountifully' (2 Corinthians 9:6).<br><br><strong>But he that hideth his eyes shall have many a curse</strong> (וּמַעְלִים עֵינָיו רַב־מְאֵרוֹת, <em>uma'lim einav rav-me'erot</em>)—עָלַם (<em>alam</em>, 'to hide, conceal') the עַיִן (<em>ayin</em>, 'eyes') from the poor's plight brings רַב (<em>rav</em>, 'many, abundant') מְאֵרָה (<em>me'erah</em>, 'curses, oaths'). Refusing to see need doesn't eliminate it—it brings judgment. The rich man ignored Lazarus at his gate and suffered eternally (Luke 16:19-31). James 2:15-16 condemns empty words without material help.",
            "historical": "Ancient Israel's law commanded care for the poor: leaving gleanings (Leviticus 19:9-10), canceling debts (Deuteronomy 15:1-11), protecting widows and orphans (Deuteronomy 24:17-22). The prophets thundered against those who exploited or ignored the poor (Amos 5:11-12, Isaiah 58:6-7). Early Christians practiced radical generosity (Acts 2:44-45, 4:32-37).",
            "questions": [
                "Who are the 'poor' in your sphere—and are you giving generously or 'hiding your eyes'?",
                "How has God proven this principle true in your life when you've given sacrificially?",
                "What would 'not hiding your eyes' look like practically in your context this week?"
            ]
        },
        "28": {
            "analysis": "<strong>When the wicked rise, men hide themselves</strong> (בְּקוּם רְשָׁעִים יִסָּתֵר אָדָם, <em>bequm resha'im yissater adam</em>)—when רָשָׁע (<em>rasha</em>, 'wicked, guilty') קוּם (<em>qum</em>, 'rises, stands, comes to power'), humanity סָתַר (<em>satar</em>, 'hides, conceals itself'). Tyranny breeds fear; people disappear, speak in whispers, distrust neighbors. Totalitarian regimes demonstrate this—oppression drives righteousness underground.<br><br><strong>But when they perish, the righteous increase</strong> (וּבְאָבְדָם יִרְבּוּ צַדִּיקִים, <em>uve'ovdam yirbu tzaddiqim</em>)—when the wicked אָבַד (<em>avad</em>, 'perish, are destroyed'), the צַדִּיק (<em>tzaddiq</em>, 'righteous') רָבָה (<em>ravah</em>, 'multiply, increase, become numerous'). Freedom from oppression allows righteousness to flourish. Proverbs 28:12, 29:2 express similar truths. History confirms this: persecuted churches survive underground; when persecution lifts, they multiply openly.",
            "historical": "Israel experienced this cycle: oppression under Pharaoh, Egyptian judges, Philistines, and Assyrian/Babylonian conquest drove faithful Israelites into hiding. When oppressors fell, the righteous remnant emerged and multiplied. The early church endured Roman persecution (Acts 8:1-4), but 'they that were scattered abroad went every where preaching the word.'",
            "questions": [
                "How should Christians respond when the wicked 'rise' to power—hide, resist, or persist faithfully?",
                "What does the 'increase' of the righteous require beyond mere numbers—and how can you contribute to this flourishing?",
                "How does this proverb encourage perseverance during seasons when wickedness seems triumphant?"
            ]
        }
    },
    "29": {
        "26": {
            "analysis": "<strong>Many seek the ruler's favour</strong> (רַבִּים מְבַקְשִׁים פְּנֵי־מוֹשֵׁל, <em>rabbim mevaqshim penei-moshel</em>)—רַב (<em>rab</em>, 'many') בָּקַשׁ (<em>baqash</em>, 'seek, desire earnestly') the פָּנִים (<em>panim</em>, 'face, favor, presence') of מֹשֵׁל (<em>moshel</em>, 'ruler, governor'). Seeking a ruler's favor was standard ancient Near Eastern practice—patronage systems distributed resources and protection. Courtiers vied for royal attention; citizens sought audience to petition justice.<br><br><strong>But every man's judgment cometh from the LORD</strong> (וּמֵיְהוָה מִשְׁפַּט־אִישׁ, <em>umei'YHWH mishpat-ish</em>)—yet מִשְׁפָּט (<em>mishpat</em>, 'judgment, justice, decision') comes מִן (<em>min</em>, 'from') יהוה (YHWH). Ultimate justice lies not in human courts but divine sovereignty. Joseph told his brothers, 'Ye thought evil... but God meant it unto good' (Genesis 50:20). Paul: 'Vengeance is mine; I will repay, saith the Lord' (Romans 12:19).",
            "historical": "Ancient royal courts concentrated immense power; a king's favor meant prosperity, his disfavor meant ruin. Daniel and his friends navigated Babylonian and Persian courts, trusting God's sovereignty over human rulers (Daniel 2, 3, 6). Esther's story demonstrates both seeking the king's favor and trusting God's providence (Esther 4:14).",
            "questions": [
                "Where are you seeking human approval or favor instead of trusting God's judgment and timing?",
                "How does confidence in God's sovereignty free you from anxiety about human decisions affecting you?",
                "What injustices in your life require you to trust that 'every man's judgment cometh from the LORD'?"
            ]
        },
        "27": {
            "analysis": "<strong>An unjust man is an abomination to the just</strong> (תּוֹעֲבַת צַדִּיקִים אִישׁ עָוֶל, <em>to'avat tzaddiqim ish avel</em>)—תּוֹעֵבָה (<em>to'evah</em>, 'abomination, detestable thing, object of loathing') describes how צַדִּיק (<em>tzaddiq</em>, 'righteous') regard אִישׁ עָוֶל (<em>ish avel</em>, 'man of injustice, perverse man'). Righteousness hates evil (Psalm 97:10, Romans 12:9). The righteous cannot be indifferent to injustice—it provokes moral revulsion.<br><br><strong>And he that is upright in the way is abomination to the wicked</strong> (וְתוֹעֲבַת רָשָׁע יְשַׁר־דָּרֶךְ, <em>veto'avat rasha yeshar-derekh</em>)—reciprocally, the יָשָׁר דֶּרֶךְ (<em>yashar derekh</em>, 'upright in way, straight of path') is תּוֹעֵבָה to the רָשָׁע (<em>rasha</em>, 'wicked'). Moral opposites produce mutual abhorrence. Jesus: 'If the world hate you, ye know that it hated me before it hated you' (John 15:18). Light and darkness cannot have fellowship (2 Corinthians 6:14).",
            "historical": "This proverb concludes Solomon's collection (Proverbs 10-29), summarizing the ethical dualism pervading the book: two ways, two destinies, two communities with irreconcilable values. Israel's history demonstrated this tension: prophets versus false prophets, faithful remnant versus idolatrous majority. The church inherits this conflict: 'All that will live godly in Christ Jesus shall suffer persecution' (2 Timothy 3:12).",
            "questions": [
                "Does injustice provoke 'abomination' in you—or have you become desensitized to evil?",
                "How should Christians maintain moral clarity while loving enemies and praying for persecutors?",
                "Where do you experience the wicked's 'abomination' toward your uprightness—and how do you respond?"
            ]
        }
    },
    "30": {
        "26": {
            "analysis": "<strong>The conies are but a feeble folk</strong> (שְׁפַנִּים עַם לֹא־עָצוּם, <em>shefannim am lo-atzum</em>)—שָׁפָן (<em>shafan</em>, 'rock badger, hyrax') are described as עַם (<em>am</em>, 'people, folk') who are לֹא עָצוּם (<em>lo atzum</em>, 'not mighty, not strong'). These small creatures, similar to large rodents, weigh only 4-5 kg yet thrive in harsh terrain.<br><br><strong>Yet make they their houses in the rocks</strong> (וַיָּשִׂימוּ בַסֶּלַע בֵּיתָם, <em>vayyasimu vasela betam</em>)—they שִׂים (<em>sim</em>, 'set, establish, make') their בַּיִת (<em>bayit</em>, 'house, dwelling') in סֶלַע (<em>sela</em>, 'rock, cliff'). Wisdom compensates for weakness. This section (30:24-28) presents four small creatures who exemplify wisdom: compensating for limitations through clever strategy. The coney's wisdom: seeking secure refuge. Spiritually, believers find refuge in the Rock: 'The name of the LORD is a strong tower' (Proverbs 18:10); 'The LORD is my rock' (Psalm 18:2).",
            "historical": "Rock badgers (hyraxes) inhabit Israel's rocky terrain, particularly around the Dead Sea and wilderness areas. Despite vulnerability to predators (eagles, foxes), they survive by inhabiting inaccessible cliffs. Agur's observations (Proverbs 30) draw on Palestinian natural history to teach spiritual wisdom.",
            "questions": [
                "What vulnerabilities and weaknesses in your life require you to seek secure refuge in God?",
                "How can you emulate the coney's wisdom by making your dwelling in the Rock of Christ?",
                "Where has God's strength been perfected in your weakness (2 Corinthians 12:9-10)?"
            ]
        },
        "27": {
            "analysis": "<strong>The locusts have no king</strong> (מֶלֶךְ אֵין לָאַרְבֶּה, <em>melekh ein la'arbeh</em>)—אַרְבֶּה (<em>arbeh</em>, 'locust') has no מֶלֶךְ (<em>melekh</em>, 'king'). Unlike bees with queens or ants with organized hierarchy, locusts lack centralized leadership.<br><br><strong>Yet go they forth all of them by bands</strong> (וַיֵּצֵא חֹצֵץ כֻּלּוֹ, <em>vayyetze chotzetz kullo</em>)—yet they יָצָא (<em>yatza</em>, 'go forth') חֹצֵץ (<em>chotzetz</em>, 'in ranks, in military formation') כֹּל (<em>kol</em>, 'all'). Without a king, they achieve remarkable coordination. Joel 2:7-8 describes their disciplined advance: 'They shall march every one on his ways, and they shall not break their ranks.' The lesson: discipline and order don't require hierarchical control. The church, though lacking earthly king, moves forward under Christ's headship through shared commitment to divine purpose.",
            "historical": "Locust swarms devastated ancient Near Eastern agriculture, sometimes covering hundreds of square miles. Joel 1-2 describes a locust plague as type of the Day of the LORD. Despite their small size and lack of leadership structure, locusts' coordinated movements could darken the sky (Exodus 10:15) and strip entire regions bare.",
            "questions": [
                "How can Christians achieve unity and coordinated mission without heavy-handed hierarchical control?",
                "What does locust-like discipline require—and how is it cultivated without a 'king'?",
                "Where has your lack of external structure revealed whether you have internal discipline and commitment?"
            ]
        },
        "28": {
            "analysis": "<strong>The spider taketh hold with her hands</strong> (שְׂמָמִית בְּיָדַיִם תְּתַפֵּשׂ, <em>semamit beyadayim tetappes</em>)—שְׂמָמִית (<em>semamit</em>, 'spider' or possibly 'lizard') תָּפַשׂ (<em>tafas</em>, 'grasps, seizes, takes hold') with יָדַיִם (<em>yadayim</em>, 'hands'). The creature uses its 'hands' (legs) skillfully to weave or climb.<br><br><strong>And is in kings' palaces</strong> (וְהִיא בְּהֵיכְלֵי מֶלֶךְ, <em>vehi beheikhlei melekh</em>)—yet she is found in הֵיכָל (<em>hekhal</em>, 'palace, temple') of מֶלֶךְ (<em>melekh</em>, 'king'). Despite being catchable by hand, small and vulnerable, the spider (or lizard) inhabits the highest places. The lesson: persistence and skill, not size or strength, open doors. Spiritually, diligent use of what God has given, however small, grants access to His presence. 'His lord said unto him, Well done, good and faithful servant: thou hast been faithful over a few things, I will make thee ruler over many things' (Matthew 25:23).",
            "historical": "Ancient Near Eastern palaces, despite their grandeur, could not exclude small creatures. The proverb's irony: the lowliest creature inhabits the loftiest residence. This democratization of wisdom—that small, weak creatures teach profound lessons—characterizes biblical wisdom literature and contrasts with ancient Near Eastern texts that celebrated only the mighty.",
            "questions": [
                "What small gifts or limited resources has God given you that, used faithfully, could grant access to greater influence?",
                "How does the spider's presence in palaces encourage you about God's ability to bring you into places beyond your natural reach?",
                "Where are you despising 'the day of small things' (Zechariah 4:10) rather than using what's in your hand?"
            ]
        },
        "29": {
            "analysis": "<strong>There be three things which go well</strong> (שְׁלֹשָׁה הֵמָּה מֵיטִיבֵי צָעַד, <em>sheloshah hemmah metivei tza'ad</em>)—שָׁלוֹשׁ (<em>shalosh</em>, 'three') מֵיטִיב (<em>metiv</em>, 'do well, make good') in צַעַד (<em>tza'ad</em>, 'step, march, gait'). This introduces a numerical proverb (three... four) examining dignified, impressive movement.<br><br><strong>Yea, four are comely in going</strong> (וְאַרְבָּעָה מֵיטִבֵי לָכֶת, <em>ve'arba'ah metivei lakhet</em>)—אַרְבַּע (<em>arba</em>, 'four') expand the list. הָלַךְ (<em>halakh</em>, 'to walk, go') done מֵיטִיב ('well, excellently'). The structure creates expectation: what four things move with dignity? Verses 30-31 answer: lion, greyhound, he-goat, and king. The lesson: certain creatures and persons possess natural majesty in motion. Spiritually, believers should 'walk worthy of the vocation wherewith ye are called' (Ephesians 4:1), exhibiting dignity befitting God's children.",
            "historical": "Numerical proverbs (x... x+1) appear throughout Proverbs (6:16-19, 30:15-16, 18-19, 21-23, 24-28, 29-31) and other wisdom literature (Job 5:19, Amos 1-2). This literary device creates anticipation and emphasizes the final item. The form was common in ancient Near Eastern wisdom traditions.",
            "questions": [
                "How does your 'walk' (lifestyle, conduct) reflect the dignity of being God's child?",
                "What would it mean to move through life with the composure and confidence the proverb describes?",
                "Who models for you a 'comely' way of living that exhibits grace under pressure?"
            ]
        },
        "30": {
            "analysis": "<strong>A lion which is strongest among beasts</strong> (לַיִשׁ גִּבּוֹר בַּבְּהֵמָה, <em>layish gibbor babbehemah</em>)—לַיִשׁ (<em>layish</em>, 'lion') characterized as גִּבּוֹר (<em>gibbor</em>, 'mighty, strong, warrior') among בְּהֵמָה (<em>behemah</em>, 'beast, animal, cattle'). The lion symbolizes regal power throughout Scripture (Genesis 49:9, Revelation 5:5).<br><br><strong>And turneth not away for any</strong> (וְלֹא־יָשׁוּב מִפְּנֵי־כֹל, <em>velo-yashuv mippnei-khol</em>)—יָשַׁב (<em>yashuv</em>, 'turn back, return, retreat') is negated: the lion does not retreat מִפְּנֵי (<em>mippnei</em>, 'from before, from the face of') כֹּל (<em>kol</em>, 'any, all'). Fearless, the lion advances regardless of opposition. Proverbs 28:1 says, 'The righteous are bold as a lion.' Believers should exhibit similar courage: 'God hath not given us the spirit of fear; but of power, and of love, and of a sound mind' (2 Timothy 1:7).",
            "historical": "Lions inhabited Israel and surrounding regions until the 13th century AD. Biblical characters encountered lions (Samson, David, Daniel). The lion's fearless advance made it the ultimate symbol of courage and kingship. Jesus is called 'the Lion of the tribe of Judah' (Revelation 5:5), emphasizing His royal authority and conquering power.",
            "questions": [
                "What opposition causes you to 'turn away' rather than advancing with lion-like courage?",
                "How does Christ's identity as the Lion of Judah embolden you to face challenges without retreating?",
                "Where is God calling you to 'be bold as a lion' in standing for truth or righteousness?"
            ]
        },
        "31": {
            "analysis": "<strong>A greyhound</strong> (זַרְזִיר מׇתְנַיִם, <em>zarzir motnayim</em>)—this phrase is difficult; זַרְזִיר (<em>zarzir</em>) appears only here. Translations vary: 'greyhound' (KJV), 'rooster' (ESV), 'strutting rooster' (NIV). מָתְנַיִם (<em>motnayim</em>, 'loins, hips') suggests girded loins, denoting readiness. Whatever the animal, the emphasis is dignified, purposeful movement.<br><br><strong>An he goat also; and a king, against whom there is no rising up</strong> (וְתָיִשׁ וּמֶלֶךְ אַלְקוּם עִמּוֹ, <em>vetayish umelekh alqum immo</em>)—תַּיִשׁ (<em>tayish</em>, 'he-goat, male goat') leads the flock confidently; מֶלֶךְ (<em>melekh</em>, 'king') אַלְקוּם עִמּוֹ (<em>alqum immo</em>, 'his army/people with him') presents a monarch with loyal subjects. The unifying theme: authority exercised with dignity. Believers are a 'royal priesthood' (1 Peter 2:9), called to exhibit godly dignity and confident authority as God's representatives.",
            "historical": "Kings in the ancient Near East cultivated images of majesty and invincibility. Israel's ideal king combined might with justice (Psalm 72). The comparison of righteous leadership to dignified animals echoes prophetic imagery (Ezekiel 34, Jesus as the Good Shepherd). Agur's observations teach that true authority exhibits calm, confident strength.",
            "questions": [
                "How can you lead with calm confidence rather than anxious control or domineering force?",
                "What does 'walking worthy' of your royal identity as God's child look like practically?",
                "Who exemplifies for you leadership that combines strength with grace, authority with humility?"
            ]
        },
        "32": {
            "analysis": "<strong>If thou hast done foolishly in lifting up thyself</strong> (אִם־נָבַלְתָּ בְהִתְנַשֵּׂא, <em>im-navalta vehitnasse</em>)—אִם (<em>im</em>, 'if') introduces a conditional. נָבַל (<em>naval</em>, 'to be foolish, to act as a fool') combined with הִתְנַשֵּׂא (<em>hitnasse</em>, 'to lift oneself up, exalt oneself') describes self-exaltation—the root of so much folly. Pride precedes destruction (Proverbs 16:18).<br><br><strong>Or if thou hast thought evil, lay thine hand upon thy mouth</strong> (וְאִם־זַמּוֹתָ יָד לְפֶה, <em>ve'im-zammota yad lefeh</em>)—or if זָמַם (<em>zamam</em>, 'to plan, devise, scheme') evil, place יָד (<em>yad</em>, 'hand') upon פֶּה (<em>peh</em>, 'mouth'). The remedy for prideful words or evil schemes: silence. Stop talking. Job learned this: 'I will lay mine hand upon my mouth' (Job 40:4). James 1:19: 'Let every man be swift to hear, slow to speak, slow to wrath.' Silence prevents compound folly—when you've erred, don't make it worse by justifying yourself.",
            "historical": "Ancient Near Eastern wisdom emphasized control of speech. Egyptian wisdom literature warned against hasty words. The gesture of hand over mouth symbolized humility and restraint (Job 21:5, 29:9). Agur's counsel: recognize folly immediately and cease multiplying it through defensive speech. This requires rare humility.",
            "questions": [
                "When you've 'lifted yourself up' foolishly, do you compound the error by justifying yourself—or do you 'lay your hand upon your mouth'?",
                "What would it look like to practice immediate silence when you recognize you've erred?",
                "How does pride make you defend yourself rather than quickly confessing folly?"
            ]
        },
        "33": {
            "analysis": "<strong>Surely the churning of milk bringeth forth butter</strong> (כִּי מִיץ חָלָב יוֹצִיא חֶמְאָה, <em>ki mitz chalav yotzi chem'ah</em>)—מִיץ (<em>mitz</em>, 'pressing, churning, squeezing') of חָלָב (<em>chalav</em>, 'milk') produces (יָצָא, <em>yatza</em>) חֶמְאָה (<em>chem'ah</em>, 'butter, curds'). Natural process: consistent pressure produces desired result.<br><br><strong>And the wringing of the nose bringeth forth blood</strong> (וּמִיץ־אַף יוֹצִיא דָם, <em>umitz-af yotzi dam</em>)—מִיץ (<em>mitz</em>, 'pressing, squeezing') of אַף (<em>af</em>, 'nose, nostril') brings דָּם (<em>dam</em>, 'blood'). Violent pressure produces violent result.<br><br><strong>So the forcing of wrath bringeth forth strife</strong> (וּמִיץ אַפַּיִם יוֹצִיא רִיב, <em>umitz appayim yotzi riv</em>)—similarly, מִיץ אַפַּיִם (<em>mitz appayim</em>, 'pressing/forcing of anger') produces רִיב (<em>riv</em>, 'strife, contention, lawsuit'). Note: אַף means both 'nose' and 'anger' (anger 'flares the nostrils'). Nurturing anger, dwelling on grievances, pressing resentment inevitably produces conflict. The lesson: what you press/cultivate determines what emerges. Press milk, get butter; press anger, get strife. Ephesians 4:26-27: 'Let not the sun go down upon your wrath: Neither give place to the devil.'",
            "historical": "Ancient dairy production involved churning milk in skins or pottery to separate butter. The physical analogy would be immediately clear to agrarian audiences. The wordplay on אַף ('nose' and 'anger') is lost in English but powerful in Hebrew. Agur's agricultural wisdom applies to emotional and spiritual life: cultivation determines harvest.",
            "questions": [
                "What are you 'churning' in your heart—and what will it inevitably produce?",
                "Where are you 'forcing wrath' by nurturing grievances rather than releasing them to God?",
                "How can you cultivate peace and grace with the same intentionality that produces butter from milk?"
            ]
        }
    },
    "31": {
        "31": {
            "analysis": "<strong>Give her of the fruit of her hands</strong> (תְּנוּ־לָהּ מִפְּרִי יָדֶיהָ, <em>tenu-lah mippri yadeha</em>)—נָתַן (<em>natan</em>, 'give, bestow') to the Proverbs 31 woman מִן (<em>min</em>, 'from') פְּרִי (<em>peri</em>, 'fruit, produce') of her יָדַיִם (<em>yadayim</em>, 'hands'). She deserves recognition and reward for her work. This is not charity but justice—her labor has earned honor.<br><br><strong>And let her own works praise her in the gates</strong> (וִיהַלְלוּהָ בַשְּׁעָרִים מַעֲשֶׂיהָ, <em>vihallluha vasha'arim ma'aseha</em>)—הָלַל (<em>halal</em>, 'to praise, commend, celebrate') happens in the שַׁעַר (<em>sha'ar</em>, 'gates')—the public square where elders sat, business was conducted, justice rendered. Her מַעֲשֶׂה (<em>ma'aseh</em>, 'works, deeds') speak for themselves. The conclusion to Proverbs: true wisdom produces fruit visible to all. Proverbs opened with 'The fear of the LORD is the beginning of knowledge' (1:7) and closes with a woman whose works praise her publicly—wisdom incarnate. Jesus: 'By their fruits ye shall know them' (Matthew 7:20).",
            "historical": "The city gates in ancient Israel served as the civic center—the place of judgment, commerce, and community gathering. To be praised in the gates meant public recognition from the community's leaders and elders. The Proverbs 31 woman (31:10-31) concludes the book by presenting wisdom in feminine form—the worthy woman embodies all the book's teachings. Her public honor vindicates wisdom's value.",
            "questions": [
                "Are you giving recognition to those whose faithful work deserves honor?",
                "What 'fruit of your hands' are you producing that will speak for you in the public square?",
                "How does the Proverbs 31 woman's blend of private faithfulness and public impact challenge gender stereotypes in both ancient and modern contexts?"
            ]
        }
    }
}

# Load existing Proverbs file
with open('kjvstudy_org/data/verse_commentary/proverbs.json') as f:
    proverbs_data = json.load(f)

# Merge commentary
for chapter, verses in proverbs_commentary.items():
    if chapter not in proverbs_data['commentary']:
        proverbs_data['commentary'][chapter] = {}
    for verse, commentary in verses.items():
        proverbs_data['commentary'][chapter][verse] = commentary

# Save updated Proverbs file
with open('kjvstudy_org/data/verse_commentary/proverbs.json', 'w') as f:
    json.dump(proverbs_data, f, indent=2, ensure_ascii=False)

print("✓ Added 36 verses to Proverbs")
print("  - Proverbs 27:18-27 (10 verses)")
print("  - Proverbs 28:14-28 (15 verses)")
print("  - Proverbs 29:26-27 (2 verses)")
print("  - Proverbs 30:26-33 (8 verses)")
print("  - Proverbs 31:31 (1 verse)")
