#!/usr/bin/env python3
"""
Generate and add commentary for 20 verses from 1 Chronicles.
"""

import json
from pathlib import Path

# Commentary data - scholarly, specific to each verse
COMMENTARY_DATA = {
    "1": {
        "1": {
            "analysis": "<strong>Adam, Sheth, Enosh</strong>—The genealogy begins at humanity's origin, establishing that Chronicles is not merely tribal history but cosmic-redemptive narrative. The Hebrew אָדָם (<em>adam</em>) means both 'man' and 'red earth,' linking humanity to creation itself (Gen 2:7). By starting with Adam rather than Abraham, the Chronicler affirms Israel's role within universal history—God's covenant people emerge from the same human family that fell in Eden, requiring the redemption Chronicles ultimately points toward in David's line.<br><br>The terse, rhythmic naming (no verbs, just nouns in sequence) creates what scholars call a 'skeletal genealogy'—compressing millennia into three Hebrew words. This literary device emphasizes continuity: from Adam through Seth (appointed after Abel's murder) to Enosh (when men 'began to call upon the name of the LORD,' Gen 4:26), the godly line persists despite the Fall.",
            "historical": "Written after the Babylonian exile (ca. 450-400 BC), Chronicles addresses returned exiles who needed to understand their identity as the continuing people of God despite national catastrophe. The opening genealogies (1 Chr 1-9) trace covenant continuity from creation through exile, assuring post-exilic Judah that they remain Abraham's seed.",
            "questions": [
                "How does beginning with Adam (rather than Abraham) shape your understanding of God's redemptive plan as universal rather than merely ethnic?",
                "In what ways does your spiritual lineage (through faith) connect you to the 'godly line' that began calling on God's name in Enosh's generation?"
            ]
        },
        "11": {
            "analysis": "<strong>Mizraim begat Ludim, and Anamim</strong>—Mizraim (מִצְרַיִם, <em>mitsrayim</em>) is the Hebrew name for Egypt, here personified as Ham's son whose descendants populate North Africa. The verb יָלַד (<em>yalad</em>, 'begat/fathered') appears repeatedly in genealogies, emphasizing biological descent but also—in Scripture's theological framework—the transmission of covenant blessing or curse (Ham's line bore Canaan's curse, Gen 9:25).<br><br>The Ludim are identified with Libya/Lydia, the Anamim with an Egyptian tribe. Chronicles' inclusion of Gentile nations serves a polemical purpose for post-exilic readers: Israel's God is sovereign over all peoples. The nations that oppressed Israel (Egypt, Babylon) are themselves part of God's ordered creation, subject to His providential plan.",
            "historical": "This section (1 Chr 1:8-16) parallels Genesis 10's 'Table of Nations,' but the Chronicler selectively edits for his audience. Egypt (Mizraim) looms large in Israel's memory as both oppressor (Exodus) and failed refuge (Jeremiah 43). Post-exilic Jews needed reminding that even Egypt's origins fall under Yahweh's design.",
            "questions": [
                "How does recognizing God's sovereignty over the nations that oppressed Israel inform your response to hostile political powers today?",
                "What does the careful preservation of Gentile genealogies reveal about God's concern for all peoples, not just Israel?"
            ]
        },
        "21": {
            "analysis": "<strong>Hadoram also, and Uzal, and Diklah</strong>—These are descendants of Joktan (Shem's line, v. 20), representing Arabian tribes. Uzal is associated with Sana'a in Yemen (Ezek 27:19), and the list traces Semitic peoples who settled the Arabian Peninsula. The Hebrew particle גַּם (<em>gam</em>, 'also') suggests this continues an enumeration, embedding these names within the broader Shemitic family from which Abraham (v. 27) would come.<br><br>The genealogy narrows progressively: from all humanity (Adam) to Shem's line, then to Abraham's, then to Israel's tribes. This funnel structure demonstrates God's elective purpose—choosing one man (Abraham) to bless all nations. Yet by preserving Arabian and Edomite names, Chronicles affirms that election doesn't negate God's providential care for non-Israelites.",
            "historical": "Joktan's descendants represent the southern Arabs, distinct from Abraham's later line through Ishmael. Ancient readers would recognize these tribal names from trade routes (spice trade through Yemen) and diplomatic relations. The Chronicler includes them to show Israel's kinship with surrounding peoples.",
            "questions": [
                "How does God's progressive narrowing of focus (from all nations to one man, Abraham) illustrate the principle that God often works through the particular to reach the universal?",
                "In what ways should recognizing our common descent from Noah shape inter-ethnic relations among believers today?"
            ]
        },
        "31": {
            "analysis": "<strong>These are the sons of Ishmael</strong>—The Hebrew phrase אֵלֶּה בְנֵי יִשְׁמָעֵאל (<em>elleh bene yishmael</em>) concludes Ishmael's genealogy before the text pivots to Isaac (v. 34). Ishmael, though not the covenant heir, receives God's promise: 'twelve princes shall he beget' (Gen 17:20). This verse lists Jetur (father of the Itureans, Luke 3:1) and Kedemah, fulfilling that promise.<br><br>The Chronicler's inclusion demonstrates that God's non-covenant promises are also certain. Though Ishmael was 'cast out' (Gal 4:30), God faithfully blessed him as pledged. This affirms God's character: He keeps every word—covenant promises to Isaac's line AND general promises to Ishmael's. For post-exilic readers tempted to doubt God's faithfulness amid broken conditions, this is crucial reassurance.",
            "historical": "Ishmael's twelve tribal princes parallel Israel's twelve tribes, suggesting God's blessing pattern (though not covenant status). Arab peoples traced ancestry through Ishmael (and later, Keturah's sons, v. 32-33), making this genealogy historically and politically significant for Jewish-Arab relations in the post-exilic period.",
            "questions": [
                "How does God's faithfulness to Ishmael (despite his non-elect status) demonstrate that God's character is trustworthy even when we're not recipients of covenant blessing?",
                "In what ways does this genealogy challenge us to see divine providence operating even in the lives of those 'outside' our faith community?"
            ]
        },
        "41": {
            "analysis": "<strong>The sons of Anah; Dishon</strong>—This verse appears within Edom's genealogy (descendants of Esau). The Hebrew toledot (תּוֹלְדוֹת, 'generations/descendants') structure carefully tracks Esau's line, paralleling the attention given to Jacob/Israel. Dishon (דִּישׁוֹן) appears among Seir the Horite's descendants (Gen 36:21), representing the indigenous Horites whom Esau's clan absorbed.<br><br>The names Amram, Eshban, Ithran, and Cheran are otherwise obscure Edomite clans. Yet their preservation in Scripture demonstrates the Bible's historiographical precision—these weren't invented legends but careful records. For the post-exilic community, this meticulous record-keeping validated their own genealogical concerns about tribal purity (Ezra 2:59-63) and showed continuity with pre-exilic records thought lost.",
            "historical": "Edom occupied the mountainous region south of the Dead Sea. Though 'brother' to Israel through Esau (Jacob's twin), Edom became Israel's bitter enemy (Obadiah). The Chronicler's inclusion of extensive Edomite genealogy (vv. 35-54) affirms God's sovereignty over Israel's enemies—even hostile Edom exists within Yahweh's ordered plan.",
            "questions": [
                "How does Scripture's careful recording of even enemy genealogies demonstrate God's concern for truth and historical accuracy?",
                "What does the parallel treatment of Esau's line (despite his rejection) teach about God's respect for all human dignity, even those outside covenant promises?"
            ]
        },
        "51": {
            "analysis": "<strong>Hadad died also. And the dukes of Edom were</strong>—The phrase וַיָּמָת הֲדַד (<em>vayamot hadad</em>, 'and Hadad died') marks the end of Edom's kings before Israel had kings (v. 43). The term אַלּוּפִים (<em>allufim</em>, 'dukes/chiefs') denotes tribal leaders, distinct from מֶלֶךְ (<em>melek</em>, 'king'). After dynastic kingship ended, Edom reverted to tribal confederation.<br><br>This detail carries theological weight: Edom had kings before Israel (v. 43), yet their monarchy proved unstable. Meanwhile, Israel's later Davidic monarchy would be eternal (17:11-14). The contrast teaches that human institutions apart from divine covenant lack permanence. Edom's succession of kings—each replacing the previous without dynasty—foreshadows the instability of all earthly powers not grounded in God's promises.",
            "historical": "The 'dukes of Edom' list (vv. 51-54) records the tribal structure after monarchical collapse, likely from the period when Edom fell under Assyrian and Babylonian domination. For the Chronicler's audience, this demonstrated that nations rise and fall at God's direction, encouraging faith amid Persian imperial rule.",
            "questions": [
                "How does the instability of Edom's monarchy (vs. the promised permanence of David's line) illustrate the difference between human ambition and divine promise?",
                "What contemporary 'kingdoms' appear more successful than God's people, yet lack the eternal covenant promises that guarantee our future?"
            ]
        }
    },
    "2": {
        "7": {
            "analysis": "<strong>Achar, the troubler of Israel, who transgressed in the thing accursed</strong>—The name עָכָר (<em>Akhar</em>) is a wordplay on עָכַר (<em>akhar</em>, 'to trouble'), referencing Achan's sin (Josh 7). The 'thing accursed' is הַחֵרֶם (<em>ha-herem</em>), items devoted to destruction/God alone. Achan's theft of Jericho's devoted plunder brought corporate judgment—36 men died at Ai because one man violated covenant.<br><br>The Chronicler changes Achan's name to Achar ('Troubler'), emphasizing his infamous legacy. This genealogical note serves as warning: sin within the covenant community brings communal consequences. For post-exilic readers tempted toward syncretism and disobedience (Malachi's accusations), Achar's inclusion reminds that individual unfaithfulness jeopardizes the whole people.",
            "historical": "Achan's sin occurred during the Conquest (ca. 1400 BC), yet the Chronicler (writing 900+ years later) preserves the memory. The transgression violated herem warfare rules—devoted items belonged solely to Yahweh. Corporate responsibility was fundamental to covenant theology: one man's sin infected the camp (Josh 7:1, 'Israel hath sinned').",
            "questions": [
                "In what ways does our individualistic culture obscure the biblical reality that personal sin affects the broader faith community?",
                "How does Achan's story challenge the notion that 'private' disobedience is inconsequential if others don't know about it?"
            ]
        },
        "17": {
            "analysis": "<strong>Abigail bare Amasa: and the father of Amasa was Jether the Ishmeelite</strong>—Abigail was David's sister (or half-sister), making Amasa David's nephew. Amasa became Absalom's general during his rebellion (2 Sam 17:25), later pardoned by David and appointed commander (2 Sam 19:13), but murdered by Joab (2 Sam 20:10). The designation 'Ishmeelite' (יִשְׁמְעֵאלִי, <em>yishmeeli</em>) indicates Jether's ethnic identity—Abigail married outside Israel proper, though Ishmaelites were Abrahamic cousins.<br><br>This mixed genealogy demonstrates that David's family included Gentile connections, foreshadowing the Messiah's mission to all nations. The note also explains Amasa's tragic role: his mixed heritage may have made him politically useful to Absalom's coalition but suspect to ethnic purists. Chronicles includes difficult family history honestly, showing covenant blessing doesn't erase human complexity.",
            "historical": "Amasa's appointment as commander (replacing Joab) was David's attempt at reconciliation after Absalom's revolt. His murder by Joab (jealous for his position) illustrates the violence plaguing David's house after the Bathsheba incident (2 Sam 12:10, 'the sword shall never depart from thine house').",
            "questions": [
                "How does Abigail's marriage to an Ishmeelite challenge ethnocentric readings of Israel's history and point toward the gospel's inclusion of all peoples?",
                "What does Amasa's tragic story reveal about the long-term consequences of family dysfunction and political intrigue, even in godly lineages?"
            ]
        },
        "27": {
            "analysis": "<strong>The sons of Ram the firstborn of Jerahmeel were, Maaz, and Jamin, and Eker</strong>—This verse details the Jerahmeelite clan within Judah. The name רָם (<em>Ram</em>) means 'exalted,' and he held firstborn status (הַבְּכוֹר, <em>habbekhor</em>) within Jerahmeel's line. The Jerahmeelites were southern Judean clans, possibly semi-nomadic, distinct from the Calebites and mainline Judah.<br><br>The Chronicler's extensive treatment of Jerahmeelite genealogy (vv. 25-33) serves an important post-exilic function: validating the Judahite identity of southern clans whose ethnic purity might be questioned after centuries of intermingling with Edomites and others. By documenting their authentic descent from Judah through Jerahmeel (v. 9), Chronicles affirms their covenant standing despite geographic marginalization.",
            "historical": "The Jerahmeelites inhabited the Negev region, south of Hebron. David maintained friendly relations with them during his outlaw period (1 Sam 27:10, 30:29). Their inclusion in Judah's genealogy, despite cultural distinctiveness, shows the tribal flexibility of ancient Israel's social structure.",
            "questions": [
                "How does Scripture's careful preservation of marginal clan genealogies demonstrate God's concern for those on the geographic and social periphery?",
                "In what ways should the validation of 'questionable' Judahites inform the church's approach to believers whose cultural expressions differ from the mainstream?"
            ]
        },
        "37": {
            "analysis": "<strong>Zabad begat Ephlal, and Ephlal begat Obed</strong>—This continues the genealogy of Sheshan's line (vv. 34-41), which came through his daughter who married Jarha, an Egyptian servant. The names זָבָד (<em>Zabad</em>, 'gift/endowment'), עָפְלָל (<em>Ephlal</em>, possibly 'judge/arbiter'), and עוֹבֵד (<em>Obed</em>, 'servant/worshiper') are otherwise obscure, yet their preservation demonstrates the Bible's concern for covenant continuity even through unconventional lines.<br><br>This genealogy is remarkable for flowing through a daughter (no sons, v. 34) who married a foreigner—an Egyptian. Yet her descendants are counted fully within Judah, foreshadowing Ruth (a Moabite woman whose son Obed became David's grandfather, Ruth 4:17). The parallel names (both lines include an 'Obed') suggest God's pattern: covenant blessing transcends ethnic and gender barriers, flowing through faith rather than bloodline alone.",
            "historical": "Sheshan's decision to give his daughter to his Egyptian servant (v. 35) reflects the patriarchal practice of preserving the family name through daughters when no sons existed. That an Egyptian could be incorporated into Judah's genealogy demonstrates Israel's occasional ethnic permeability, despite later strict separationism.",
            "questions": [
                "How does Sheshan's Egyptian-descended line within Judah challenge ethnocentric understandings of covenant identity?",
                "In what ways does this genealogy preview the New Testament's radical teaching that in Christ 'there is neither Jew nor Greek' (Gal 3:28)?"
            ]
        },
        "47": {
            "analysis": "<strong>The sons of Jahdai; Regem, and Jotham, and Gesham, and Pelet, and Ephah, and Shaaph</strong>—Jahdai's identity is uncertain; he appears only here. The six sons listed are otherwise unknown, yet their preservation in Scripture testifies to God's exhaustive knowledge: every generation matters, even those that leave no other historical trace. The name רֶגֶם (<em>Regem</em>) means 'friend/stone pile,' and שַׁעַף (<em>Shaaph</em>) means 'bald/divided.'<br><br>This genealogical obscurity teaches humility: most lives leave no monument but a name in God's record. For post-exilic Judeans feeling forgotten by history—their nation destroyed, temple burned, dynasty ended—these obscure names whisper encouragement. God remembers. The genealogies aren't mere lists but theological statements: Yahweh keeps covenant with every generation, famous or forgotten.",
            "historical": "The placement of Jahdai within Caleb's broader genealogy (vv. 42-49) suggests a Calebite sub-clan. Caleb himself was a Kenizzite (Num 32:12), ethnically Edomite, yet fully incorporated into Judah—another example of covenant transcending ethnicity. These obscure names likely represent families significant in local regions, though forgotten by national history.",
            "questions": [
                "How does God's preservation of genealogically 'obscure' names encourage believers whose service seems unnoticed by the world?",
                "What does the inclusion of forgotten clans teach about God's valuation of faithfulness over fame?"
            ]
        }
    },
    "3": {
        "2": {
            "analysis": "<strong>Absalom the son of Maachah the daughter of Talmai king of Geshur</strong>—This verse lists David's sons born in Hebron, emphasizing their mothers' identities. Maachah (מַעֲכָה) was a Geshurite princess, making Absalom half-Aramean royalty. The diplomatic marriage allied David with Geshur (a small Aramean kingdom northeast of Galilee), but produced Israel's most infamous rebel. Absalom's foreign royal blood may have fueled his ambitions—he had legitimate claim to Geshur's throne and thought himself worthy of Israel's.<br><br>The juxtaposition of <strong>Adonijah the son of Haggith</strong> is telling: Adonijah also later rebelled, attempting to seize the throne (1 Kgs 1). Both sons, products of David's polygamous marriages, brought disaster. The genealogy thus quietly critiques the dynastic politics—multiple wives for political alliances—that plagued David's house with rivalry, murder (Absalom killed Amnon), and rebellion.",
            "historical": "David reigned in Hebron seven years (2 Sam 5:5) before capturing Jerusalem. His Hebron wives represented political alliances: Maachah connected him to Geshur (where Absalom later fled after murdering Amnon, 2 Sam 13:37-38). These marriages, typical for ancient Near Eastern kings, introduced foreign influences that Scripture implicitly criticizes.",
            "questions": [
                "How did David's pragmatic political marriages (violating Deut 17:17's prohibition on multiplying wives) sow seeds of familial chaos and national crisis?",
                "In what ways do we compromise God's relational standards for pragmatic 'success,' not realizing the long-term consequences?"
            ]
        },
        "12": {
            "analysis": "<strong>Amaziah his son, Azariah his son, Jotham his son</strong>—This rapid genealogical succession traces the Davidic line through three kings of Judah. Amaziah (אֲמַצְיָהוּ, <em>Amatsyahu</em>, 'Yahweh is mighty') defeated Edom but foolishly challenged Israel and was defeated (2 Kgs 14). Azariah (עֲזַרְיָהוּ, <em>Azaryahu</em>, 'Yahweh has helped'), also called Uzziah, reigned prosperously but was struck with leprosy for usurping priestly prerogatives (2 Chr 26:16-21). Jotham (יוֹתָם, <em>Yotam</em>, 'Yahweh is perfect') reigned righteously but couldn't stop the people's corruption (2 Kgs 15:35).<br><br>The genealogy's bare-bones style hides complex histories: Amaziah's assassination (2 Kgs 14:19), Azariah's 52-year reign ending in shameful isolation, Jotham's regent-ship during his father's leprosy. Yet the Chronicler emphasizes continuity—the Davidic line persists despite individual failures, because God's covenant with David (17:11-14) is irrevocable.",
            "historical": "This period (ca. 800-735 BC) saw Judah's prosperity under Azariah/Uzziah, contemporaneous with Amos and Hosea's northern ministry. Yet beneath material success, spiritual decay grew. Isaiah's vision (Isa 6) occurred 'in the year that king Uzziah died,' marking the shift from prosperity to crisis as Assyria rose.",
            "questions": [
                "How does the Davidic line's persistence despite kings' personal failures demonstrate that God's purposes advance through His faithfulness, not human merit?",
                "What warning does Azariah's leprosy (judgment for pride, 2 Chr 26:16) offer to those experiencing success and prosperity?"
            ]
        },
        "22": {
            "analysis": "<strong>The sons of Shemaiah; Hattush, and Igeal, and Bariah, and Neariah, and Shaphat, six</strong>—This verse presents a textual problem: five names are listed, but the text says 'six' (שִׁשָּׁה, <em>shishah</em>). Either a name dropped from transmission, or Shemaiah himself is counted as the sixth. The names represent post-exilic Davidic descendants—Hattush (חַטּוּשׁ) returned from Babylon with Ezra (Ezra 8:2)—showing the royal line's continuation after the monarchy's end.<br><br>This genealogical survival proves crucial for the Chronicler's theology: though Judah has no king, the Davidic house endures, awaiting the ultimate Son of David. The listing of descendants into the Persian period (these names reach ca. 400 BC) demonstrates that God's promise 'your throne shall be established for ever' (2 Sam 7:16) outlasts political destruction. The Messiah will come from this preserved line.",
            "historical": "After 586 BC, the Davidic family lost political power but maintained genealogical identity. Zerubbabel (v. 19), a grandson of King Jehoiachin, served as Persian-appointed governor but not king. Post-exilic Davidic descendants lived as private citizens, their significance theological (messianic hope) rather than political.",
            "questions": [
                "How does the preservation of David's line through the exile (despite loss of throne and kingdom) illustrate God's faithfulness to His promises even when circumstances seem to contradict them?",
                "In what areas of life are you tempted to doubt God's promises because visible 'kingdoms' have fallen, though His purposes remain certain?"
            ]
        }
    },
    "4": {
        "8": {
            "analysis": "<strong>And Coz begat Anub, and Zobebah, and the families of Aharhel the son of Harum</strong>—This verse appears within Judah's genealogy, listing otherwise unknown individuals. The name קוֹץ (<em>Qots</em>, 'Coz') may mean 'thorn,' while צוֹבֵבָה (<em>Tsobebah</em>) means 'canopy/umbrella.' These obscure names highlight the Chronicler's exhaustive genealogical method—preserving even minor clans for whom no narrative survives.<br><br>The phrase 'families of Aharhel' (מִשְׁפְּחוֹת אַחַרְחֵל, <em>mishpechot Acharchel</em>) indicates clan divisions within Judah. For post-exilic readers concerned with establishing legitimate tribal identity after exile's disruptions, these detailed clan records validated claims to land inheritance (Neh 11:25-36 shows returnees settling ancestral towns). Genealogical precision wasn't antiquarian interest but practical necessity for covenant community reconstitution.",
            "historical": "After the exile, land redistribution required proof of ancestral ownership (Ezra 2:59-62 describes those unable to prove lineage). The Chronicler's genealogies, drawing on pre-exilic temple archives, provided the documentation necessary for reestablishing tribal territories. Though Coz's descendants left no historical record, their inclusion ensured their land rights.",
            "questions": [
                "How does God's preservation of 'insignificant' genealogical data demonstrate His concern for justice and property rights among His people?",
                "What does the careful documentation of obscure families teach about the value of each individual and clan within the covenant community?"
            ]
        },
        "18": {
            "analysis": "<strong>These are the sons of Bithiah the daughter of Pharaoh, which Mered took</strong>—This verse preserves an astonishing detail: Mered (a Judahite) married an Egyptian princess, Pharaoh's daughter. The name בִּתְיָה (<em>Bithyah</em>) means 'daughter of Yahweh'—a Hebrew name, suggesting she converted to Israel's faith. Rabbinic tradition (not biblical) identifies her as the princess who rescued Moses, though the chronology doesn't support this.<br><br>The note demonstrates that Gentiles could be incorporated into Judah through faith. Bithiah abandoned Egyptian royalty to join the covenant people, her sons (Jered, Heber, Jekuthiel, v. 18) counting as full Judahites. This foreshadows Ruth, Rahab, and ultimately the gospel's inclusion of Gentiles. The Chronicler's audience, tempted toward ethnic exclusivism (Ezra-Nehemiah's divorce crisis, Ezra 9-10), needed reminding that covenant identity depends on faith, not ethnicity alone.",
            "historical": "Intermarriage with Egyptians was generally prohibited (Deut 7:3), but conversion changed the equation—Bithiah's Hebrew name signals covenantal commitment. Her inclusion in Judah's genealogy parallels Ruth the Moabitess's inclusion in David's line (Ruth 4:17). Both demonstrate that Gentiles who embrace Yahweh become full covenant members.",
            "questions": [
                "How does Bithiah's conversion and incorporation into Judah illustrate the gospel principle that faith, not ethnicity, determines covenant membership?",
                "What does her willingness to abandon Egyptian royalty for Israel's God teach about the cost and value of following Yahweh?"
            ]
        },
        "28": {
            "analysis": "<strong>And they dwelt at Beer-sheba, and Moladah, and Hazar-shual</strong>—This verse lists settlements of Simeon's tribe in the southern Negev. Beer-sheba (בְּאֵר שֶׁבַע, <em>beer sheva</em>, 'well of seven/oath') was Israel's southern boundary ('from Dan to Beer-sheba'). Moladah and Hazar-shual were towns within Judah's territory assigned to Simeon (Josh 19:2-3), reflecting Simeon's absorption into Judah—Jacob's prophecy that Simeon would be 'scattered in Israel' (Gen 49:7) was fulfilled as Simeon lost independent tribal identity.<br><br>The preservation of Simeonite towns demonstrates the Chronicler's concern for completeness—though Simeon essentially disappeared (no Simeonite territory in post-exilic period), their heritage is documented. For post-exilic readers, this taught that even 'failed' tribes remained part of covenant history. God's purposes include the marginalized and absorbed, not just the prominent.",
            "historical": "Simeon's territory was enclaved within Judah's southern region (Josh 19:1, 'their inheritance was within the inheritance of Judah'). Over time, Simeonites assimilated into Judah or dispersed, fulfilling Gen 49:7's judgment. By the monarchy, Simeon functioned as Judahite sub-clans rather than a separate tribe, though their genealogy persisted.",
            "questions": [
                "How does Simeon's gradual disappearance as a distinct tribe (yet preservation in genealogy) illustrate that God's judgment and discipline don't erase covenant belonging?",
                "What encouragement does Simeon's inclusion offer to those who feel their spiritual heritage has been 'absorbed' or marginalized?"
            ]
        },
        "38": {
            "analysis": "<strong>These mentioned by their names were princes in their families</strong>—The phrase אֵלֶּה הַבָּאִים בְּשֵׁמוֹת נְשִׂיאִים (<em>eleh habaim beshemot nesi'im</em>) identifies the previously listed Simeonites (vv. 34-37) as נְשִׂיאִים (<em>nesi'im</em>, 'princes/leaders/chiefs'). Despite Simeon's tribal decline, they produced notable leaders. The concluding phrase <strong>and the house of their fathers increased greatly</strong> (וּבֵית אֲבוֹתֵיהֶם פָּרְצוּ לָרוֹב, <em>uvet avoteihem partsu larov</em>) uses פָּרַץ (<em>parats</em>, 'to break out/increase abundantly'), the same verb describing Jacob's blessing (Gen 30:30).<br><br>This teaches that God's blessing (numeric increase, prominent leaders) can coexist with tribal marginalization. Simeon, though 'scattered' (Gen 49:7), still experienced covenant blessing. For post-exilic Jews—politically powerless under Persian rule yet experiencing population growth—this was reassuring: God's purposes don't require political dominance.",
            "historical": "The Simeonite expansion described (v. 39-43) occurred during Hezekiah's reign (v. 41), when some Simeonites migrated southeast, displacing Hamites and Meunites. This aggression demonstrates vitality despite the tribe's marginalization within Judah, showing that blessing can manifest unexpectedly.",
            "questions": [
                "How does Simeon's simultaneous decline (tribal absorption) and blessing (population increase, leaders) illustrate that God's favor doesn't always mean worldly prominence?",
                "In what ways might God be blessing you or your community even while 'increasing' you in ways that don't resemble conventional success?"
            ]
        }
    },
    "5": {
        "5": {
            "analysis": "<strong>Micah his son, Reaia his son, Baal his son</strong>—This genealogy traces the Reubenite line. The name בַּעַל (<em>Baal</em>) is startling in a godly genealogy—it's the name of Canaan's chief deity. Before Baal worship became synonymous with apostasy (Elijah's era, 1 Kgs 18), 'Baal' (meaning 'lord/master') was used in Hebrew compound names: Ishbaal/Eshbaal (1 Chr 8:33), Merib-baal (8:34). Later scribes often changed 'Baal' to 'Bosheth' ('shame') in names, but Chronicles preserves the original.<br><br>The name's inclusion demonstrates the Bible's honest historiography—covenant people weren't always scrupulously distinct from surrounding cultures. Syncretism was an ongoing temptation, names reflecting cultural compromise. Yet God's purposes advanced despite imperfect bearers. For post-exilic readers, this was cautionary: don't assume covenant status immunizes against cultural assimilation.",
            "historical": "Reuben, Jacob's firstborn, lost preeminence due to defiling his father's bed (Gen 35:22; 1 Chr 5:1). The tribe settled east of Jordan (Num 32) and was first exiled when Assyria conquered Transjordan (v. 6, 26). By the Chronicler's time, Reuben existed only genealogically—ten lost tribes absorbed into exile. This genealogy preserves a vanished tribe's memory.",
            "questions": [
                "How does the use of 'Baal' in Israelite names illustrate the subtle ways cultural compromise infiltrates God's people through 'acceptable' syncretism?",
                "What 'culturally normal' practices might believers today adopt without recognizing their incompatibility with wholehearted covenant faithfulness?"
            ]
        },
        "15": {
            "analysis": "<strong>Ahi the son of Abdiel, the son of Guni, chief of the house of their fathers</strong>—This verse concludes the genealogy of Gad's tribe. The name אֲחִי (<em>Achi</em>) means 'my brother,' עַבְדִּיאֵל (<em>Abdiel</em>) means 'servant of God,' and גּוּנִי (<em>Guni</em>) means 'protected/painted.' The designation רֹאשׁ לְבֵית אֲבוֹתָם (<em>rosh levet avotam</em>, 'chief of the house of their fathers') identifies Ahi as clan head, responsible for representing his extended family in tribal affairs.<br><br>The Gadites, like Reuben, settled east of Jordan and were exiled early (v. 26). Yet the Chronicler preserves their leadership structure, teaching that God's covenant includes those who 'disappeared' from history. For post-exilic readers wondering about the ten lost tribes, this genealogy affirms: God remembers. The lost tribes aren't erased from His purposes—they await eschatological restoration (Ezek 37:15-23, Rev 7:4-8).",
            "historical": "Gad's territory (Gilead region) was vulnerable to Aramean and later Assyrian aggression. The tribe's military prowess is noted (vv. 18-22), but geography doomed them—Transjordan fell to Tiglath-Pileser III in 733 BC (v. 26), decades before Judah's exile. The Chronicler's attention to exiled tribes shows his concern for all Israel, not just Judah.",
            "questions": [
                "How does the preservation of Gad's genealogy (despite the tribe's early exile and disappearance) demonstrate that God's covenant transcends historical catastrophe?",
                "What hope does this offer regarding God's faithfulness to believers who seem 'lost' to the church through persecution, apostasy, or historical disruption?"
            ]
        }
    }
}

def load_existing_commentary():
    """Load the existing 1 Chronicles commentary file."""
    filepath = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

    if not filepath.exists():
        return {"book": "1 Chronicles", "commentary": {}}

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_commentary(data):
    """Save the updated commentary file."""
    filepath = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / "1_chronicles.json"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def merge_commentary(existing, new_data):
    """Merge new commentary with existing data."""
    for chapter, verses in new_data.items():
        if chapter not in existing["commentary"]:
            existing["commentary"][chapter] = {}

        for verse, content in verses.items():
            if verse not in existing["commentary"][chapter]:
                existing["commentary"][chapter][verse] = content
                print(f"Added commentary for 1 Chronicles {chapter}:{verse}")
            else:
                print(f"Skipped 1 Chronicles {chapter}:{verse} (already exists)")

    return existing

def main():
    print("Loading existing 1 Chronicles commentary...")
    existing = load_existing_commentary()

    print("\nMerging new commentary...")
    updated = merge_commentary(existing, COMMENTARY_DATA)

    print("\nSaving updated commentary...")
    save_commentary(updated)

    print("\n✓ Successfully added commentary for 20 verses from 1 Chronicles")
    print("\nSummary of verses added:")
    for chapter in sorted(COMMENTARY_DATA.keys(), key=int):
        verses = sorted(COMMENTARY_DATA[chapter].keys(), key=int)
        print(f"  Chapter {chapter}: verses {', '.join(verses)}")

if __name__ == "__main__":
    main()
