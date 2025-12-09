#!/usr/bin/env python3
"""Generate scholarly commentary for missing Numbers verses."""

import json
import subprocess
import sys

# Missing verses by chapter
MISSING_VERSES = {
    8: [20, 21, 22, 23, 24, 25, 26],
    10: [36],
    14: [41, 42, 43, 44, 45],
    16: [49, 50],
    17: [11, 12, 13],
    18: [25, 26, 27, 28, 29, 30, 31, 32],
    19: [22],
    22: [39, 40, 41],
    23: [27, 28, 29, 30],
    24: [20, 21, 22, 23, 24, 25],
    28: [27, 28, 29, 30, 31],
    29: [40],
    30: [10, 11, 12, 13, 14, 15, 16],
    31: [51, 52, 53, 54],
    32: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    34: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
}

def get_verse_text(book, chapter, verse):
    """Get verse text using CLI tool."""
    try:
        result = subprocess.run(
            ['uv', 'run', 'python', 'scripts/commentary_cli.py', 'verse', book, str(chapter), str(verse)],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data['text']
    except Exception as e:
        print(f"Error getting {book} {chapter}:{verse}: {e}", file=sys.stderr)
        return None

# Commentary templates organized by theme
COMMENTARY_DATA = {
    # Chapter 8: Levitical consecration (verses 20-26)
    (8, 20): {
        "analysis": "<strong>Moses, and Aaron, and all the congregation... did to the Levites according unto all that the LORD commanded</strong>—This verse emphasizes complete obedience (שָׁמַע <em>shama</em>, to hear and obey) to divine instruction regarding Levitical consecration. The threefold witness (Moses, Aaron, congregation) establishes the corporate nature of Israel's covenant obedience.<br><br>The phrase <strong>according unto all</strong> (כְּכֹל <em>kekol</em>) stresses absolute conformity to God's commands—a recurring theme in wilderness worship (cf. Exodus 39:42-43). The Levites' unique status as substitutes for Israel's firstborn (Numbers 3:12-13) required meticulous adherence to consecration rituals, establishing precedent for New Testament priesthood of all believers (1 Peter 2:9).",
        "historical": "This verse concludes the Levitical consecration ceremony (Numbers 8:5-22), conducted at Sinai during Israel's second year of wilderness wandering (ca. 1445 BC). Moses mediated between God and people while Aaron supervised priestly functions, establishing patterns for Israel's tabernacle service.",
        "questions": [
            "How does the corporate obedience of Israel's leaders and congregation model accountability in Christian community?",
            "What does complete conformity to God's commands ('according unto all') teach about partial obedience?",
            "How does Levitical consecration foreshadow Christ's setting apart of believers for holy service?"
        ]
    },
    (8, 21): {
        "analysis": "<strong>The Levites were purified, and they washed their clothes</strong>—The dual purification (חָטָא <em>chata</em>, ceremonial cleansing) and washing (כָּבַס <em>kabas</em>, laundering garments) symbolizes both inward and outward sanctification. Ancient Near Eastern priestly service universally required ritual purity, but Israel's standards uniquely emphasized moral transformation alongside ceremonial cleanliness.<br><br><strong>Aaron offered them as an offering before the LORD</strong>—The wave offering (תְּנוּפָה <em>tenuphah</em>) of living persons (not animals) dramatically pictures the Levites' total dedication to God's service. Aaron's mediatorial role prefigures Christ's presentation of believers as living sacrifices (Romans 12:1), holy and acceptable to God.",
        "historical": "Wave offerings typically involved priests moving sacrificial portions in prescribed patterns before the altar. Applying this ritual to human beings (Numbers 8:11-15) was unique to Levitical consecration, emphasizing their sacred status as God's possession rather than common Israelites.",
        "questions": [
            "How does the combination of ceremonial cleansing and clothing washing illustrate the comprehensive nature of sanctification?",
            "What does it mean to be 'offered' to God as a living person rather than remaining in self-directed living?",
            "How does Aaron's mediatorial presentation of Levites point forward to Christ's high-priestly ministry?"
        ]
    },
    (8, 22): {
        "analysis": "<strong>After that went the Levites in to do their service</strong>—The sequential phrase <strong>after that</strong> (אַחֲרֵי־כֵן <em>acharei-ken</em>) emphasizes consecration as prerequisite to service. The verb <strong>to do their service</strong> (לַעֲבֹד אֶת־עֲבֹדָתָם <em>la'avod et-avodatam</em>) uses the same root for both worship and work, revealing that Levitical ministry was simultaneously service to God and labor for the community.<br><br>This verse establishes the principle that effective ministry flows from proper consecration—a pattern Jesus affirmed by delaying public ministry until after His baptism and wilderness testing (Luke 3:21-4:14). The phrase <strong>as the LORD had commanded</strong> reiterates covenant fidelity as the foundation for acceptable service.",
        "historical": "The Levites' service (Numbers 3:5-10; 4:1-49) included dismantling, transporting, and reassembling the tabernacle, guarding sacred objects, and assisting priests. This verse marks their official commencement of duties following a month-long consecration process.",
        "questions": [
            "Why must consecration precede service rather than the reverse? What dangers arise from premature ministry?",
            "How does the Hebrew connection between 'worship' and 'work' challenge modern sacred/secular divisions?",
            "What 'wilderness preparation' might God require before releasing you into fuller kingdom service?"
        ]
    },
    (8, 23): {
        "analysis": "<strong>The LORD spake unto Moses</strong>—This divine speech formula (וַיְדַבֵּר יְהוָה <em>vayedaber YHWH</em>) introduces age-related regulations for Levitical service, demonstrating God's concern for both human dignity and physical limitations. Ancient cultures often worked elderly individuals until incapacity; Israel's system provided structured retirement.<br><br>The placement of these verses after the consecration narrative (8:5-22) suggests that even sacred callings have temporal boundaries. God's sovereignty extends over the full lifecycle of ministry—calling, serving, and resting—anticipating the New Testament teaching that different seasons require different contributions to Christ's body (1 Corinthians 12:4-11).",
        "historical": "This passage (8:23-26) addresses administrative details following the broader consecration ritual. Moses received this instruction at Sinai during the second year after the Exodus (Numbers 1:1), as Israel prepared for organized wilderness march and tabernacle service.",
        "questions": [
            "How does God's establishment of retirement ages demonstrate care for His servants' wellbeing?",
            "What does the placement of these regulations after the consecration ceremony teach about lifecycle stages in ministry?",
            "How can churches honor both the energy of younger servants and the wisdom of those transitioning from active service?"
        ]
    },
    (8, 24): {
        "analysis": "<strong>From twenty and five years old and upward they shall go in to wait upon the service</strong>—The minimum age (עֶשְׂרִים וְחָמֵשׁ שָׁנָה <em>esrim vechamesh shanah</em>) for Levitical service balances physical maturity with spiritual readiness. The phrase <strong>wait upon</strong> (לִצְבֹא צָבָא <em>litsvo tzava</em>, literally 'to wage warfare') uses military terminology, revealing that tabernacle service constituted spiritual warfare requiring mature soldiers (cf. Ephesians 6:10-18).<br><br>This age requirement (25) differs from the 30-year threshold for priestly service (Numbers 4:3), suggesting graduated responsibility—Levites began apprenticeship at 25 before assuming full duties at 30. Paul's instruction that elders not be recent converts (1 Timothy 3:6) echoes this principle of seasoned maturity before spiritual leadership.",
        "historical": "The Levitical minimum age of 25 provided five years of apprenticeship before the full service age of 30 (Numbers 4:3). This training period under experienced Levites ensured proper handling of sacred objects and accurate execution of complex tabernacle procedures.",
        "questions": [
            "Why does God use military language ('wage warfare') to describe tabernacle service? What spiritual battles accompany sacred ministry?",
            "How does the apprenticeship model (25-30) inform modern approaches to leadership development in churches?",
            "What character qualities and life experiences make someone 'mature enough' for spiritual leadership?"
        ]
    },
    (8, 25): {
        "analysis": "<strong>From the age of fifty years they shall cease waiting upon the service thereof</strong>—The retirement age (חֲמִשִּׁים שָׁנָה <em>chamishim shanah</em>) acknowledges physical demands of Levitical labor—dismantling, carrying, and reassembling the 13-ton tabernacle structure through wilderness terrain. The verb <strong>cease</strong> (יָשׁוּב <em>yashuv</em>, return/withdraw) is not dismissal but dignified transition from active to advisory roles.<br><br><strong>Shall serve no more</strong>—The phrase (לֹא יַעֲבֹד עוֹד <em>lo ya'avod od</em>) specifically prohibits heavy labor, not all contribution (see verse 26). God's law honored elderly wisdom while protecting aging bodies, contrasting sharply with cultures that discarded unproductive individuals. The principle appears in Paul's instruction to honor widows and elders (1 Timothy 5:3-20).",
        "historical": "Ancient Near Eastern societies often lacked provisions for elderly workers. Israel's structured retirement at 50 (extended from the earlier 45-year proposal in some traditions) demonstrated covenant care for servants of God, ensuring dignity and continued usefulness without physical exploitation.",
        "questions": [
            "How does mandatory retirement from heavy labor demonstrate God's compassion while still valuing ongoing contribution?",
            "What modern ministry practices might 'burn out' faithful servants by ignoring physical limitations?",
            "How can churches honor the wisdom of retired ministers while respecting their need for rest?"
        ]
    },
    (8, 26): {
        "analysis": "<strong>But shall minister with their brethren in the tabernacle... to keep the charge</strong>—Retired Levites continued advisory ministry (שָׁרַת <em>sharat</em>, to serve/attend) and oversight (שָׁמַר מִשְׁמֶרֶת <em>shamar mishmeret</em>, guard responsibility) without performing heavy labor. The phrase <strong>with their brethren</strong> (אֶת־אֶחָיו <em>et-echayv</em>) emphasizes intergenerational partnership—young strength complementing aged wisdom.<br><br><strong>Shall do no service</strong> (עֲבֹדָה לֹא יַעֲבֹד <em>avodah lo ya'avod</em>) specifically refers to physical labor prohibited in verse 25, not all ministry. This balance between rest and continued contribution models healthy transitions from active to emeritus roles. Paul's mentorship of Timothy (2 Timothy 2:2) reflects this multigenerational pattern, where experienced leaders equip successors while gradually reducing direct responsibilities.",
        "historical": "The specific duties retired Levites could perform included mentoring younger Levites, supervising tabernacle security, teaching proper handling of sacred objects, and maintaining institutional memory of worship practices. This preserved continuity across generations while respecting physical limitations.",
        "questions": [
            "What advisory or mentoring roles should churches create for retired ministers and leaders?",
            "How can 'keeping the charge' (oversight without heavy labor) utilize seasoned wisdom while allowing rest?",
            "What intergenerational ministry partnerships in your church could benefit from pairing young energy with experienced wisdom?"
        ]
    },

    # Chapter 10:36 - Cloud movements and ark transportation
    (10, 36): {
        "analysis": "<strong>When it rested, he said, Return, O LORD, unto the many thousands of Israel</strong>—Moses' invocation (שׁוּבָה יְהוָה <em>shuvah YHWH</em>) whenever the cloud halted uses the verb 'return' (שׁוּב), not merely 'remain,' suggesting dynamic divine presence rather than static location. The phrase <strong>many thousands</strong> (רִבְבוֹת אַלְפֵי <em>rivvot alfei</em>, literally 'ten thousands of thousands') emphasizes Israel's vast multitude under God's protection.<br><br>This verse pairs with 10:35 to form liturgical brackets around Israel's march—'Rise up, LORD' (קוּמָה יְהוָה) when departing, 'Return, LORD' when encamping. These invocations became fixed elements of Jewish liturgy and appear in synagogue ark ceremonials. The pattern establishes that all movement (spiritual and physical) requires divine initiative and presence, foreshadowing Christ's promise to be with His church always (Matthew 28:20).",
        "historical": "This verse concludes the section on cloud movements and trumpet signals (Numbers 9:15-10:36), establishing liturgical patterns for Israel's wilderness journeys. Moses spoke these formulas at each camp and departure throughout the 38-year wandering period (ca. 1445-1407 BC).",
        "questions": [
            "How do Moses' invocations ('Rise up... Return') model dependence on God's presence for all life transitions?",
            "What does Israel's need for divine presence in both movement and rest teach about continuous reliance on God?",
            "How can you develop liturgical practices that acknowledge God's presence in your daily comings and goings?"
        ]
    },

    # Chapter 14:41-45 - Presumptuous advance after judgment
    (14, 41): {
        "analysis": "<strong>Moses said, Wherefore now do ye transgress the commandment of the LORD?</strong>—Moses' rhetorical question (לָמָּה זֶּה אַתֶּם עֹבְרִים <em>lamah zeh atem ovrim</em>) uses <strong>transgress</strong> (עָבַר <em>avar</em>, to pass over/violate) to characterize Israel's presumptuous advance as covenant rebellion. After refusing to enter Canaan in faith (14:1-10), they now attempted entry in presumption—replacing God-commanded courage with self-willed bravado.<br><br><strong>But it shall not prosper</strong> (וְהִיא לֹא תִצְלָח <em>vehi lo titslach</em>)—Moses' prophetic warning uses the verb צָלַח (<em>tsalach</em>, to succeed/advance), which requires divine blessing. Human initiative divorced from God's timing and presence inevitably fails. This principle echoes throughout Scripture: Saul's unlawful sacrifice (1 Samuel 13:8-14), Uzzah touching the ark (2 Samuel 6:6-7), disciples' powerless exorcism (Mark 9:14-29).",
        "historical": "This verse introduces Israel's disastrous attempt to invade Canaan after God decreed 40 years wilderness wandering for their unbelief (Numbers 14:26-35). The people's whiplash from cowardly refusal to presumptuous attack (within 24 hours) demonstrates spiritual instability under judgment.",
        "questions": [
            "How does Israel's swing from fearful disobedience to presumptuous action illustrate the dangers of self-directed religion?",
            "What's the difference between God-commanded courage and self-willed presumption in facing challenges?",
            "When have you attempted 'spiritual warfare' in your own strength rather than waiting for God's timing and blessing?"
        ]
    },
    (14, 42): {
        "analysis": "<strong>Go not up, for the LORD is not among you</strong>—Moses' urgent warning (אַל־תַּעֲלוּ כִּי אֵין יְהוָה בְּקִרְבְּכֶם <em>al-ta'alu ki ein YHWH bekirbekem</em>) identifies the fatal flaw in Israel's plan: divine absence. The phrase <strong>is not among you</strong> reverses the covenant promise 'I will dwell among them' (Exodus 25:8), showing that presumptuous disobedience forfeits God's presence.<br><br><strong>That ye be not smitten before your enemies</strong>—The verb <strong>smitten</strong> (נָגַף <em>nagaph</em>, routed/struck down) describes divinely-permitted military defeat. Throughout Israel's history, victories depended on covenant obedience (Joshua 6-8; Judges 7; 1 Samuel 14), while disobedience guaranteed defeat regardless of military strength (Joshua 7; 1 Samuel 4). Paul warns Christians against presuming on grace: 'Let him who thinks he stands take heed lest he fall' (1 Corinthians 10:12).",
        "historical": "Moses spoke this warning after God decreed wilderness wandering (14:26-35). The people's attempt to reverse judgment through self-initiated action demonstrates fundamental misunderstanding of covenant relationship—God determines blessing and judgment, not human religious activity.",
        "questions": [
            "What contemporary 'ministry initiatives' proceed without confirming God's presence and blessing?",
            "How can believers discern the difference between God-directed action and self-willed religious activity?",
            "What spiritual defeats in your life might trace back to proceeding without God's clear presence and approval?"
        ]
    },
    (14, 43): {
        "analysis": "<strong>For the Amalekites and the Canaanites are there before you</strong>—Moses identifies specific enemies (עֲמָלֵקִי וְהַכְּנַעֲנִי <em>Amaleqi vehakena'ani</em>) occupying the terrain, emphasizing concrete military realities Israel would face without divine intervention. Amalek symbolized perpetual opposition to God's people (Exodus 17:8-16; Deuteronomy 25:17-19), while Canaanites represented entrenched wickedness Israel was commissioned to judge.<br><br><strong>Because ye are turned away from the LORD, therefore the LORD will not be with you</strong>—The causal connection (כִּי... עַל־כֵּן <em>ki... al-ken</em>, because... therefore) establishes covenant principle: turning from God (שׁוּב מֵאַחֲרֵי יְהוָה <em>shuv me'acharei YHWH</em>, returning from following the LORD) results in divine withdrawal. God's presence depends on covenant faithfulness, not presumptuous demands. Jesus warned that branches severed from the vine wither and bear no fruit (John 15:4-6).",
        "historical": "Amalekites had attacked Israel at Rephidim (Exodus 17:8-16), earning divine judgment. Canaanites controlled the hill country north of Kadesh-barnea. Both groups would have observed Israel's 40-day spy mission and prepared defenses against invasion, making Israel's unsanctioned attack doubly foolish.",
        "questions": [
            "How does 'turning away from the LORD' manifest in presumptuous religious activity rather than humble obedience?",
            "What 'spiritual enemies' seem insurmountable without God's presence and power in your battles?",
            "How can churches discern when they're 'following the LORD' versus pursuing self-directed agendas?"
        ]
    },
    (14, 44): {
        "analysis": "<strong>But they presumed to go up unto the hill top</strong>—The verb <strong>presumed</strong> (וַיַּעְפִּלוּ <em>vaya'apilu</em>, to act presumptuously/swell up) suggests arrogant self-will despite clear divine prohibition. Their upward march (עָלָה <em>alah</em>) toward the hill country defied both God's judgment and Moses' warnings—epitomizing stiff-necked rebellion masquerading as courageous faith.<br><br><strong>Nevertheless the ark of the covenant of the LORD, and Moses, departed not out of the camp</strong>—The ark's absence underscores divine withdrawal from this unauthorized mission. Throughout Israel's history, ark presence signified God's power (Joshua 6:6-20; 1 Samuel 4-6), while its absence spelled doom. Moses' refusal to accompany them demonstrated prophetic solidarity with God's will over popular sentiment—the true leader serves God's purposes, not crowd demands.",
        "historical": "The ark remained in the Kadesh-barnea camp while Israel attacked northward into the Negev hill country. This was the first military action undertaken without the ark since Jericho's conquest formula was established, making defeat inevitable (cf. Joshua 7 where hidden sin, not ark absence, caused defeat).",
        "questions": [
            "What's the difference between faith-filled courage and presumptuous self-will when facing opposition?",
            "How do spiritual leaders like Moses maintain prophetic integrity when popular opinion demands different action?",
            "What 'arks of God's presence' (corporate worship, Scripture, prayer) do we abandon when pursuing self-directed plans?"
        ]
    },
    (14, 45): {
        "analysis": "<strong>Then the Amalekites came down, and the Canaanites which dwelt in that hill, and smote them</strong>—The coalition attack (וַיֵּרֶד... וַיַּכּוּם <em>vayered... vayakum</em>, came down... struck them) fulfilled Moses' prophecy (14:42-43). The verb <strong>smote</strong> (נָכָה <em>nakah</em>, to strike/defeat) describes comprehensive military disaster—not merely tactical defeat but rout demonstrating divine disfavor.<br><br><strong>Discomfited them, even unto Hormah</strong>—The verb <strong>discomfited</strong> (וַיַּכְּתוּם <em>vayaktum</em>, crushed/pulverized) intensifies the defeat description, while the place name <strong>Hormah</strong> (חָרְמָה <em>Chormah</em>, 'destruction/devotion to destruction') became permanent memorial to presumptuous failure. Later, after 40 years wandering, Israel would legitimately conquer this same region under God's blessing (Numbers 21:1-3), demonstrating that divine timing and presence determine success, not human initiative.",
        "historical": "Hormah (likely modern Tell el-Meshash, 7 miles east of Beersheba) became a landmark for Israel's presumptuous defeat. The site's name commemorated both this disaster and later victory (Numbers 21:3), teaching successive generations the difference between God-blessed and self-willed warfare.",
        "questions": [
            "What 'Hormah moments' (public failures from presumption) has God used to teach you about dependence on His timing?",
            "How does the later conquest of Hormah under divine blessing (Numbers 21:3) illustrate God's redemption of past failures?",
            "What ministry initiatives should be abandoned or postponed until God's clear presence and timing are confirmed?"
        ]
    }
}

# Continue with more verses...
print("Commentary template loaded. Ready to process verses.")
print(f"Total commentary entries prepared: {len(COMMENTARY_DATA)}")
