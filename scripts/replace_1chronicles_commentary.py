#!/usr/bin/env python3
"""
Replace generic filler commentary with proper scholarly commentary for 20 1 Chronicles verses.
"""

import json
from pathlib import Path

# Commentary data with scholarly theological insights
COMMENTARY_DATA = {
    "1": {
        "2": {
            "analysis": "<strong>Kenan, Mahalaleel, Jered</strong>—these patriarchs bridge Adam to Noah in the godly line (Genesis 5). The Hebrew name קֵינָן (<em>Qenan</em>) means 'possession' or 'acquisition,' while מַהֲלַלְאֵל (<em>Mahalalel</em>) means 'praise of God,' and יֶרֶד (<em>Yered</em>) means 'descent.' The Chronicler omits Cain's line entirely, focusing only on the lineage through which Messiah would come.<br><br>This selective genealogy reflects Hebrew historiography's theological purpose—not exhaustive records but <em>heilsgeschichte</em> (salvation history). Every name preserved points toward God's covenant faithfulness across generations, culminating in David and ultimately Christ (Matthew 1:1-17).",
            "historical": "Written post-exilic (c. 450-400 BC), Chronicles reestablished Israel's identity after Babylonian captivity by tracing their lineage back to Adam. The Chronicler drew from Genesis 5 but adapted it for returnees needing to reclaim their theological heritage and land rights through documented ancestry.",
            "questions": [
                "How does God's preservation of a faithful line through history assure you of His commitment to fulfill His promises?",
                "What does it mean that your spiritual lineage traces back through Christ to Adam—both as fallen humanity and redeemed creation?"
            ]
        },
        "12": {
            "analysis": "<strong>Of whom came the Philistines</strong> (מִמֶּנּוּ יָצְאוּ פְלִשְׁתִּים)—this parenthetical note identifies the Casluhim as progenitors of Israel's perpetual enemies. The Philistines, Sea Peoples who invaded Canaan c. 1200 BC, descended from Ham through Mizraim (Egypt), establishing five city-states: Gaza, Ashkelon, Ashdod, Ekron, Gath.<br><br>The Chronicler's inclusion serves theological purposes: Israel's struggles weren't random but part of the outworking of Noah's prophecy regarding Canaan (Genesis 9:25-27). The Philistines' uncircumcised status marked them as outside covenant blessings, yet God used them to discipline Israel (Judges, 1 Samuel) and refine David's kingship.",
            "historical": "The Philistines dominated coastal Palestine during the Iron Age I (1200-1000 BC) with superior iron technology. Their conflict with Israel climaxed under Saul and David, who finally subdued them. Archaeological evidence from Philistine cities reveals Aegean cultural connections, confirming their 'Sea Peoples' origin.",
            "questions": [
                "How does understanding the genealogy of Israel's enemies help you see God's sovereignty over historical conflicts?",
                "What persistent 'Philistines' (spiritual enemies) does God allow in your life for refinement rather than immediate removal?"
            ]
        },
        "22": {
            "analysis": "<strong>Ebal, and Abimael, and Sheba</strong>—these sons of Joktan represent Arabian tribal founders descended from Shem. The Hebrew עוֹבָל (<em>Obal</em>/Ebal) possibly means 'bare' or 'stripped,' while אֲבִימָאֵל (<em>Abimael</em>) means 'my father is God,' and שְׁבָא (<em>Sheba</em>) denotes 'seven' or 'oath.'<br><br>Sheba particularly matters: this Arabian kingdom (modern Yemen) produced the Queen who visited Solomon (1 Kings 10), testing his wisdom with hard questions. These Semitic peoples, though outside Israel's covenant line, shared linguistic and cultural connections, and some like Sheba acknowledged Yahweh's supremacy through Solomon.",
            "historical": "The Joktanite tribes settled southern Arabia, establishing trade networks dealing in spices, gold, and incense. Sheba became wealthy through controlling trade routes, evident in archaeological remains at sites like Marib. The Queen of Sheba's visit (c. 950 BC) represents these kingdoms' recognition of Israel's God during Solomon's zenith.",
            "questions": [
                "How does the Queen of Sheba's seeking wisdom from Solomon challenge you to pursue spiritual wisdom with equal diligence?",
                "What does it mean that even peoples outside the covenant line could recognize and honor Yahweh?"
            ]
        },
        "32": {
            "analysis": "<strong>The sons of Keturah, Abraham's concubine</strong> (בְּנֵי קְטוּרָה פִּילֶגֶשׁ אַבְרָהָם)—after Sarah's death, Abraham married קְטוּרָה (<em>Qeturah</em>, 'incense' or 'fragrance'), producing six sons including Midian. Though legitimate sons, Genesis 25:6 specifies Abraham gave them gifts and sent them eastward, reserving Isaac's inheritance. Midian's descendants became the Midianites, both trading partners (Genesis 37:28) and enemies (Numbers 25, Judges 6-8) of Israel.<br><br>This demonstrates God's blessing extended beyond Isaac while maintaining covenant exclusivity. Abraham's fruitfulness fulfilled God's promise to make him 'father of many nations' (Genesis 17:5), yet the covenant line ran singularly through Isaac and Jacob—foreshadowing salvation's particularity through Christ while God's common grace extends universally.",
            "historical": "Abraham remarried after Sarah's death at age 127 (Genesis 23:1), when he was 137. He lived another 38 years (died at 175), making Keturah's sons contemporaries of Jacob's youth. The Midianites settled east of Jordan and northwest Arabia, trading in spices and controlling caravan routes.",
            "questions": [
                "How does God's blessing of Keturah's sons alongside covenant promises to Isaac reflect His common grace while maintaining particular election?",
                "What does Abraham's provision for all his children while preserving Isaac's unique inheritance teach about God's justice and mercy?"
            ]
        },
        "42": {
            "analysis": "<strong>The sons of Ezer; Bilhan, and Zavan, and Jakan</strong>—these Horite/Hurrian clans descended from Seir the Edomite (Genesis 36:27). The בִּלְהָן (<em>Bilhan</em>) and זַעֲוָן (<em>Zaavan</em>) families inhabited Edom before Esau's descendants displaced them. The Horites were indigenous cave-dwellers (חֹרִי from חוֹר, 'hole' or 'cave') in Mount Seir's rugged terrain.<br><br>The Chronicler's inclusion of Edomite genealogies serves to establish completeness and acknowledge kinship: Edom descended from Esau, Jacob's twin brother. Though Edom became Israel's bitter enemy (Obadiah), they remained 'brothers,' and Deuteronomy 23:7 forbade abhorring Edomites. This demonstrates God's concern for all peoples while working His purposes through Israel.",
            "historical": "The Horites inhabited Seir before Esau's arrival (Deuteronomy 2:12, 22). Archaeological evidence from Edomite sites shows sophisticated iron-working and copper mining operations in the Arabah valley. Edom's eventual destruction by Babylon (c. 553 BC) and Nabatean occupation fulfilled prophetic warnings.",
            "questions": [
                "How does God's command not to abhor Edomites despite their hostility challenge your attitude toward those who oppose you?",
                "What does the preservation of Horite genealogies teach about God valuing every people group's historical significance?"
            ]
        },
        "52": {
            "analysis": "<strong>Duke Aholibamah, duke Elah, duke Pinon</strong> (אַלּוּף אָהֳלִיבָמָה אַלּוּף אֵילָה אַלּוּף פִּינֹן)—אַלּוּף (<em>alluph</em>) means 'chieftain' or 'clan leader,' rendered 'duke' in KJV. These Edomite tribal chiefs ruled regions rather than centralized kingdoms. Aholibamah (אָהֳלִיבָמָה, 'tent of the high place') suggests religious significance, while Elah (אֵילָה) means 'terebinth tree' or possibly refers to the port city Elath, and Pinon (פִּינֹן) remains obscure.<br><br>Edom's tribal confederacy contrasted with Israel's covenant kingship. Before Israel had kings, Edom had chieftains (Genesis 36:31), yet this political precocity didn't translate to covenant blessing. God's delays often precede greater purposes—Israel's later monarchy would produce David and ultimately Messiah.",
            "historical": "Edomite chiefs ruled from fortified highlands south of the Dead Sea, controlling trade routes between Arabia and the Mediterranean. Their copper mining and caravan trade created wealth reflected in archaeological sites like Bozrah and Teman. Edom's fall came through Babylonian campaigns (6th century BC) and later Nabatean displacement.",
            "questions": [
                "How does Edom's early political development without covenant blessing warn against equating worldly success with divine favor?",
                "What does God's patient work through Israel's slower development teach about His timing versus immediate results?"
            ]
        }
    },
    "2": {
        "8": {
            "analysis": "<strong>And the sons of Ethan; Azariah</strong>—this brief notice identifies Azariah (עֲזַרְיָה, 'Yahweh has helped') as descended from Zerah's son Ethan. This is likely Ethan the Ezrahite, the wise man Solomon surpassed (1 Kings 4:31), credited with Psalm 89. Ethan's wisdom represented pre-Davidic Israel's intellectual heritage, yet Solomon's God-given wisdom exceeded all predecessors.<br><br>The genealogy's inclusion within Judah's tribal records establishes that wisdom, worship, and covenant faithfulness were Judah's inheritance before kingship. Even Israel's wisest sages needed Solomon's greater revelation, which itself foreshadowed Christ, 'in whom are hidden all the treasures of wisdom and knowledge' (Colossians 2:3).",
            "historical": "Ethan lived during the judges period or early monarchy, representing Israel's wisdom tradition. His psalm (Psalm 89) wrestles with God's covenant promises to David amid national crisis, possibly written during exile. The Ezrahites formed a guild of temple musicians and wisdom teachers.",
            "questions": [
                "How does recognizing that even Ethan's wisdom paled before Solomon's—and Solomon's before Christ's—humble you in pursuing knowledge?",
                "What does it mean that true wisdom is a person (Christ) rather than merely intellectual achievement?"
            ]
        },
        "18": {
            "analysis": "<strong>Caleb the son of Hezron begat children of Azubah his wife, and of Jerioth</strong>—this Caleb differs from the faithful spy (Numbers 13-14); this is Caleb ben Hezron of Judah's early generations. The Hebrew עֲזוּבָה (<em>Azubah</em>) means 'forsaken,' a poignant name perhaps reflecting circumstances of her birth. יְרִיעוֹת (<em>Jerioth</em>) means 'tent curtains,' possibly indicating Bedouin connections.<br><br>The text's grammar creates interpretive challenges—whether Azubah and Jerioth were co-wives or whether Jerioth identifies Azubah's children. Either way, the complexity reflects real family dynamics. These genealogical details weren't mere antiquarianism but established land claims and inheritance rights for post-exilic returnees reclaiming Judah's territory.",
            "historical": "The Chronicler compiled these genealogies from ancient family records, court archives, and Genesis-Samuel materials. For post-exilic Jews, proving Judahite descent meant legitimate claims to ancestral lands. Names like 'forsaken' remind us these records preserved real people's stories, not just data.",
            "questions": [
                "How does the name 'Azubah' (forsaken) remind you that God includes and redeems those whom society marginalizes?",
                "What does the preservation of complex family details teach about God's concern for the particulars of our lives?"
            ]
        },
        "28": {
            "analysis": "<strong>And the sons of Onam were, Shammai, and Jada</strong>—these Jerahmeelite clans descended from Judah's firstborn line. שַׁמַּי (<em>Shammai</em>) means 'desolate' or possibly 'renowned,' while יָדָע (<em>Yada</em>) derives from 'to know.' The Jerahmeelites occupied southern Judah's wilderness regions, maintaining tribal identity distinct from main Judahite settlements.<br><br>Nadab, Shammai's son, bears the same name as Aaron's son who died offering strange fire (Leviticus 10:1-2). Names recurred across Israelite families, sometimes honoring ancestors, sometimes carrying prophetic or memorial significance. The preservation of these marginal clans demonstrates God's covenant includes not just prominent lines but obscure families whose faithfulness mattered equally.",
            "historical": "The Jerahmeelites dwelt in the Negev wilderness south of Hebron, mentioned when David shared spoils with them (1 Samuel 30:29). They represented semi-nomadic pastoral clans who maintained Judahite identity while living frontier existence. Their territory bordered Edom and the Kenites.",
            "questions": [
                "How does God's careful record of 'marginal' clans like the Jerahmeelites encourage you if you feel spiritually insignificant?",
                "What does the recurrence of names like Nadab across generations teach about how families process tragedy and hope?"
            ]
        },
        "38": {
            "analysis": "<strong>And Obed begat Jehu, and Jehu begat Azariah</strong>—this genealogical fragment traces Judahite lineage through names rich with theological meaning. עוֹבֵד (<em>Obed</em>) means 'servant' or 'worshiper,' יֵהוּא (<em>Yehu</em>) means 'Yahweh is He,' and עֲזַרְיָה (<em>Azaryah</em>) means 'Yahweh has helped.' These theophoric names (containing God's name) demonstrate covenant consciousness persisting through generations.<br><br>While seemingly mundane, such genealogies established legal identity and theological continuity. Every 'begat' represented God's faithfulness across decades, even centuries. The chain from Judah to David to Christ depended on each link holding—one broken generation would have severed Messiah's lineage. God preserves His purposes through ordinary faithfulness.",
            "historical": "Genealogies served multiple purposes: establishing tribal membership, determining inheritance rights, priestly qualification, and maintaining covenant identity. Post-exilic returnees needed documented lineage to reclaim properties under Ezra-Nehemiah's reforms. Names were chosen carefully to express faith, commemorate events, or honor ancestors.",
            "questions": [
                "How does seeing your life as one link in God's larger chain of faithfulness across generations affect your sense of purpose?",
                "What spiritual legacy are you leaving for those who will come after you, even if you never know their names?"
            ]
        },
        "48": {
            "analysis": "<strong>Maachah, Caleb's concubine, bare Sheber, and Tirhanah</strong>—מַעֲכָה (<em>Maacah</em>) was a common name meaning 'oppression' or 'pressure,' shared by multiple biblical women including David's wife. As פִּילֶגֶשׁ (<em>pilegesh</em>, 'concubine'), Maachah held secondary wife status—legitimate but without full wife privileges. Sheber (שֶׁבֶר, 'fracture' or 'breach') and Tirhanah (תִּרְחֲנָה, meaning uncertain) extended Caleb's considerable family network.<br><br>Concubinage in ancient Israel, while culturally accepted, fell short of God's Genesis 2:24 design for monogamous marriage. The practice created household tensions (Genesis 16, 21) and succession conflicts (2 Samuel 3:2-5). The Chronicler records these realities without moral commentary, letting Scripture's narrative arc—from polygamy's problems to Christ's elevation of marriage (Matthew 19:4-6)—provide interpretation.",
            "historical": "Concubines were secondary wives, often from lower social status, captured in war, or given as gifts. Their children could inherit, though primary wives' sons received preference. The practice persisted throughout Old Testament period but decreased post-exilic, with later Judaism emphasizing monogamy more strongly.",
            "questions": [
                "How does Scripture's honest recording of concubinage without approving it teach us to distinguish between what God permits and what He prefers?",
                "What does Christ's upholding of Genesis 2:24 (one man, one woman) teach about God's ideal versus cultural accommodations?"
            ]
        }
    },
    "3": {
        "3": {
            "analysis": "<strong>The fifth, Shephatiah of Abital: the sixth, Ithream by Eglah his wife</strong>—these were David's sons born in Hebron during his seven-year reign over Judah (2 Samuel 3:2-5). שְׁפַטְיָה (<em>Shephatyah</em>) means 'Yahweh has judged,' while יִתְרְעָם (<em>Ithream</em>) means 'remainder of the people' or 'excellence of the people.' Abital (אֲבִיטָל, 'my father is dew') and Eglah (עֶגְלָה, 'heifer' or 'young cow') remain obscure, mentioned only in genealogies.<br><br>Significantly, none of David's Hebron-born sons succeeded him; Solomon, born later in Jerusalem to Bathsheba, inherited the throne. This demonstrates God's sovereign election transcends birth order and human expectations—the eighth son of Jesse's eighth son became king, and the scandal-born son (Solomon) inherited instead of firstborns. Grace operates independently of human merit or natural advantage.",
            "historical": "David reigned in Hebron 1010-1003 BC before capturing Jerusalem and establishing it as capital. His multiple marriages during this period followed ancient Near Eastern royal practice of cementing political alliances, though they created household tensions that plagued his reign (2 Samuel 13-18, 1 Kings 1-2).",
            "questions": [
                "How does God's choice of Solomon over David's earlier sons encourage you if you feel like a 'late arrival' in faith?",
                "What does the obscurity of most of David's sons teach about finding significance in God's particular calling rather than prominence?"
            ]
        },
        "13": {
            "analysis": "<strong>Ahaz his son, Hezekiah his son, Manasseh his son</strong>—this sequence presents Judah's most dramatic spiritual oscillation: wicked Ahaz (אָחָז, 'he has grasped'), righteous Hezekiah (חִזְקִיָּהוּ, 'Yahweh strengthens'), and wicked Manasseh (מְנַשֶּׁה, 'causing to forget'). Ahaz promoted Baal worship and sacrificed his sons (2 Kings 16:3); Hezekiah reformed Judah and trusted God through Assyrian crisis (2 Kings 18-20); Manasseh reintroduced abominations and shed innocent blood (2 Kings 21:16).<br><br>This genealogical segment proves godliness neither guarantees godly offspring nor results from godly parents—each generation must choose covenant faithfulness. Hezekiah's reforms didn't prevent Manasseh's apostasy, yet Manasseh's evil didn't doom Josiah (his grandson) to wickedness. God's grace remains accessible to every generation, regardless of ancestral patterns.",
            "historical": "Ahaz ruled 735-715 BC during Assyria's expansion; Hezekiah 715-686 BC, surviving Sennacherib's siege (701 BC); Manasseh 696-642 BC, Judah's longest reign. Manasseh's 55-year rule allowed deep syncretism that Josiah's later reforms couldn't fully eradicate, contributing to eventual exile (2 Kings 23:26-27).",
            "questions": [
                "How does the Ahaz-Hezekiah-Manasseh sequence challenge assumptions that godly parenting guarantees godly children?",
                "What hope does Hezekiah's faithfulness despite Ahaz's wickedness offer if you came from a difficult spiritual background?"
            ]
        },
        "23": {
            "analysis": "<strong>And the sons of Neariah; Elioenai, and Hezekiah, and Azrikam, three</strong>—these descendants of David's royal line lived post-exilic, after the Babylonian captivity ended monarchy. אֶלְיוֹעֵינַי (<em>Elyoenai</em>) means 'my eyes are toward Yahweh,' חִזְקִיָּה (<em>Hizkiyah</em>) means 'Yahweh strengthens,' and עַזְרִיקָם (<em>Azrikam</em>) means 'my help has risen.' The careful specification 'three' emphasizes completeness and accuracy in record-keeping.<br><br>Though kingship ended with Zedekiah (586 BC), God preserved David's line through exile, fulfilling His covenant promise that David's house wouldn't fail (2 Samuel 7:16). These obscure descendants maintained Davidic identity across exile's dark centuries, unknowingly preserving Messiah's genealogical pathway until Christ's birth seven generations later (Matthew 1:1-17). Faithfulness in obscurity prepares for God's purposes.",
            "historical": "After Babylonian exile (539 BC return), Davidic descendants like Zerubbabel led returnees but didn't regain kingship. The family maintained identity through careful genealogical records, anticipating messianic fulfillment. These names appear in Chronicles' unique post-exilic extension (1 Chronicles 3:17-24), possibly updated during Ezra-Nehemiah's era.",
            "questions": [
                "How does God's preservation of David's line through obscure descendants encourage you when your faithfulness seems insignificant?",
                "What does it mean that Messiah's genealogy depended on unknown believers maintaining covenant identity through exile?"
            ]
        }
    },
    "4": {
        "9": {
            "analysis": "<strong>And Jabez was more honourable than his brethren</strong> (וַיְהִי יַעְבֵּץ נִכְבָּד מֵאֶחָיו)—יַעְבֵּץ (<em>Yabetz</em>) means 'he causes pain,' reflecting his mother's difficult labor. Yet despite an ominous name, Jabez achieved נִכְבָּד (<em>nikhbad</em>, 'honored,' 'weighty,' 'glorious'). His mother's naming him 'pain' could have defined his identity, but his prayer (v. 10) reveals faith that transcended circumstances. The statement 'more honourable' suggests righteous reputation, not mere prominence.<br><br>Jabez models refusing to accept limiting labels others impose. Rather than accepting 'pain' as identity, he sought God's blessing, enlarged borders, divine presence, and protection from evil. His prayer became Israel's model for seeking God's favor—not passively accepting fate but actively pursuing God's purposes through petition. Christ teaches similar boldness: 'Ask, and it shall be given you' (Matthew 7:7).",
            "historical": "Jabez appears abruptly in Judahite genealogies without lineage context, suggesting his fame derived from character rather than ancestry. The Chronicler highlights exceptional individuals (like Jabez) amid genealogical lists, demonstrating personal faithfulness matters more than pedigree. The town Jabez (1 Chronicles 2:55) may have been named after him.",
            "questions": [
                "What negative labels or painful circumstances has your past imposed that God wants to transcend through faith like Jabez?",
                "How does Jabez's prayer challenge you to pursue God's blessing and enlarged influence rather than accepting limited expectations?"
            ]
        },
        "19": {
            "analysis": "<strong>And the sons of his wife Hodiah the sister of Naham, the father of Keilah the Garmite</strong>—this complex verse navigates familial relationships within Judah. הוֹדִיָּה (<em>Hodiyah</em>) means 'majesty of Yahweh' or 'praise Yahweh,' while נַחַם (<em>Naham</em>) means 'comfort.' Keilah, a fortified town David later rescued (1 Samuel 23), demonstrates how genealogies preserved both family and territorial connections.<br><br>The phrase 'father of Keilah' likely means 'founder' or 'chief,' showing patriarchs established settlements bearing their names or governance. This intertwining of genealogy and geography helped post-exilic returnees reclaim ancestral lands. Every name in these lists represented not just individuals but families, clans, and territorial claims rooted in God's covenant land promises.",
            "historical": "Keilah, located in Judah's Shephelah (lowlands), served as a fortified border town against Philistine incursions. David's rescue of Keilah from Philistines (1 Samuel 23:1-13) demonstrated his leadership before becoming king. The town's inhabitants, however, would have betrayed David to Saul, showing political complexity in border regions.",
            "questions": [
                "How does the connection between genealogy and geography show that God's promises include both people and place?",
                "What does it mean that your spiritual inheritance includes both relationship with God's people and place in His kingdom?"
            ]
        },
        "29": {
            "analysis": "<strong>And at Bilhah, and at Ezem, and at Tolad</strong>—these Simeonite towns in southern Judah's Negev reflect tribal settlement patterns. בִּלְהָה (<em>Bilhah</em>) shares the name of Rachel's handmaid (Genesis 29:29), עֶצֶם (<em>Etzem</em>) means 'bone' or 'strength,' and תּוֹלָד (<em>Tolad</em>) means 'generations' or 'birth.' The list continues from verse 28, enumerating Simeon's allotted cities within Judah's territory (Joshua 19:2-8).<br><br>Simeon's absorption into Judah fulfilled Jacob's prophecy: 'I will divide them in Jacob, and scatter them in Israel' (Genesis 49:7). Though receiving inheritance, Simeon lacked distinct tribal territory, eventually merging with Judah. This demonstrates God's prophetic words accomplish their purpose across centuries. What seemed like curse (scattering) ensured Simeon's preservation through Judah, the tribe producing Messiah.",
            "historical": "Simeon's territory, theoretically within Judah's borders, never achieved full independence. By David's census (2 Samuel 24), Simeon had largely merged with Judah. The Chronicler's listing preserves Simeon's identity even as tribal distinctiveness faded, showing God remembers every tribe despite historical absorption.",
            "questions": [
                "How does Simeon's absorption into Judah demonstrate that God's discipline can become the means of preservation and blessing?",
                "What does it mean that even 'scattered' tribes remained in God's covenant memory and received inheritance?"
            ]
        },
        "39": {
            "analysis": "<strong>And they went to the entrance of Gedor, even unto the east side of the valley, to seek pasture for their flocks</strong>—this describes Simeonite expansion seeking גְּדוֹר (<em>Gedor</em>, location debated), illustrating tribal movements pursuing resources. The phrase 'seek pasture' (לְבַקֵּשׁ מִרְעֶה, <em>levakesh mireh</em>) describes nomadic-pastoral economy's demands—tribes needed extensive grazing lands for livestock survival.<br><br>The passage (vv. 38-43) records Simeonite conquest of Hamite populations during Hezekiah's reign, demonstrating continued tribal identity and expansion even after 722 BC northern kingdom's fall. While Israel proper collapsed, Judah's southern tribes maintained covenant consciousness and territorial claims. This faithfulness through turbulent times preserved them for return from Babylonian exile generations later. Persistent seeking—whether pasture or God's purposes—characterizes covenant faithfulness.",
            "historical": "This expansion occurred during Hezekiah's reforms (c. 715-686 BC), when Assyria had destroyed northern Israel. Some northern tribes like Simeonite clans found refuge in Judah, maintaining identity. Their aggressive expansion southward suggests population pressure and economic necessity. The Chronicler preserves this as example of tribal vitality during monarchy's twilight.",
            "questions": [
                "How does the Simeonites' diligent seeking of pasture illustrate the persistent pursuit required in spiritual life?",
                "What does this minor tribe's maintained identity through Israel's collapse teach about faithfulness when larger structures fail?"
            ]
        }
    },
    "5": {
        "6": {
            "analysis": "<strong>Beerah his son, whom Tilgath-pilneser king of Assyria carried away captive: he was prince of the Reubenites</strong>—בְּאֵרָה (<em>Beerah</em>) means 'well' or 'spring,' while תִּלְגַּת פִּלְנֶאסֶר (<em>Tilgath-pilneser</em>) renders Tiglath-Pileser III, the Neo-Assyrian king who deported northern tribes (734-732 BC, 2 Kings 15:29). Beerah's designation as נָשִׂיא (<em>nasi</em>, 'prince' or 'tribal chief') indicates leadership status, making his exile particularly significant for Reuben's tribe.<br><br>Reuben, Israel's firstborn, lost birthright blessings through sin (Genesis 35:22, 49:3-4, 1 Chronicles 5:1), and now lost land through exile—fulfilled judgment for covenant unfaithfulness. Yet even recording exiled leaders preserves hope: God remembers His people even in judgment. The exile wasn't annihilation but discipline, positioning eventual restoration (Ezra-Nehemiah). Judgment doesn't negate identity in God's covenant memory.",
            "historical": "Tiglath-Pileser III (745-727 BC) transformed Assyria into empire, implementing mass deportation policies to prevent rebellion. The 734-732 BC campaigns decimated northern Israel, deporting Transjordanian tribes (Reuben, Gad, Manasseh) before Samaria's final fall in 722 BC. Archaeological evidence from Assyrian records confirms these deportations.",
            "questions": [
                "How does Reuben's loss of birthright followed by exile warn against presuming covenant privilege excuses unfaithfulness?",
                "What hope does God's preservation of exiled leaders' names offer when you face consequences of past failures?"
            ]
        },
        "16": {
            "analysis": "<strong>And they dwelt in Gilead in Bashan, and in her towns, and in all the suburbs of Sharon, upon their borders</strong>—this verse maps Gadite territory east of Jordan: גִּלְעָד (<em>Gilead</em>, 'heap of testimony') signified the covenant boundary between Jacob and Laban (Genesis 31:47-48), while בָּשָׁן (<em>Bashan</em>) denoted fertile highlands famous for cattle and oaks. שָׁרוֹן (<em>Sharon</em>) here differs from coastal Sharon, referring to Transjordan pasturelands.<br><br>The territorial description emphasizes borders and suburbs (מִגְרְשֵׁיהֶן, <em>migrasheihen</em>, 'pasture lands'), showing tribal inheritance included both settlements and grazing lands. God's land promises weren't abstract but concrete—specific territories for specific tribes. The Transjordanian tribes' choice to settle east of Jordan (Numbers 32) required Moses' conditional approval: they must fight alongside their brothers before enjoying inheritance. Privilege always accompanies responsibility in covenant relationship.",
            "historical": "Gilead and Bashan, conquered under Moses (Numbers 21:21-35) and distributed to Reuben, Gad, and half-tribe Manasseh, provided rich pasturelands ideal for livestock. Their exposed position made them vulnerable to foreign invasion, suffering first in Assyrian deportations (734-732 BC). The territories' fertility made them contested throughout Old Testament period.",
            "questions": [
                "How does Gad's inheritance east of Jordan, requiring them to fight before settling, illustrate that spiritual blessing requires faithful service?",
                "What does the precision of tribal boundaries teach about God's detailed planning and provision for His people?"
            ]
        }
    }
}

def main():
    # Load existing commentary file
    commentary_file = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

    with open(commentary_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure the structure exists
    if "commentary" not in data:
        data["commentary"] = {}

    # Replace the commentary entries (overwrite existing)
    verses_replaced = 0
    for chapter, verses in COMMENTARY_DATA.items():
        if chapter not in data["commentary"]:
            data["commentary"][chapter] = {}

        for verse, commentary in verses.items():
            data["commentary"][chapter][verse] = commentary
            verses_replaced += 1
            print(f"Replaced commentary for 1 Chronicles {chapter}:{verse}")

    # Save the updated file
    with open(commentary_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Successfully replaced {verses_replaced} commentary entries in 1_chronicles.json")
    print(f"📖 File location: {commentary_file}")
    print("\n📝 Summary:")
    print("Replaced generic 'Genealogical Significance' filler with:")
    print("- Specific Hebrew words with transliterations")
    print("- Direct verse quotes")
    print("- Historical context and dates")
    print("- Theological significance")
    print("- Practical reflection questions")

if __name__ == "__main__":
    main()
