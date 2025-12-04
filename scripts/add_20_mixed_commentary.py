#!/usr/bin/env python3
"""
Generate scholarly theological commentary for 20 verses from 1 Chronicles and 1 Corinthians.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def load_commentary_file(book_slug):
    """Load existing commentary file."""
    file_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / f"{book_slug}.json"

    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Create new structure
        book_name = book_slug.replace('_', ' ').title()
        return {"book": book_name, "commentary": {}}

def save_commentary_file(book_slug, data):
    """Save commentary file."""
    file_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "verse_commentary" / f"{book_slug}.json"

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {file_path}")

def add_commentary(book_slug, chapter, verse, commentary_data):
    """Add commentary for a single verse."""
    data = load_commentary_file(book_slug)

    # Ensure chapter exists
    ch_str = str(chapter)
    v_str = str(verse)

    if ch_str not in data['commentary']:
        data['commentary'][ch_str] = {}

    # Add verse commentary
    data['commentary'][ch_str][v_str] = commentary_data

    return data

# Commentary data for all 20 verses
commentaries = {
    "1_chronicles": {
        "25": {
            "8": {
                "analysis": "<strong>They cast lots, ward against ward</strong> (גּוֹרָל, <em>goral</em>)—the division of temple musicians was determined by sacred lot, not human preference or talent assessment. The phrase <strong>as well the small as the great, the teacher as the scholar</strong> establishes radical equality before God's sovereignty. This democratic distribution echoes Proverbs 16:33: \"The lot is cast into the lap; but the whole disposing thereof is of the LORD.\"<br><br>David's organization of 288 musicians into 24 courses (v.7) paralleled the priestly divisions, elevating worship to the same sacred status as sacrifice. The Hebrew <em>mishmar</em> (ward/watch) indicates military precision—worship was spiritual warfare requiring disciplined rotation and accountability.",
                "historical": "Written circa 450-400 BC by the Chronicler (likely Ezra), this passage records David's temple preparations circa 1000 BC. The 24 musical divisions served weekly rotations, ensuring continuous temple worship. This organizational structure persisted through the Second Temple period and informed synagogue liturgy.",
                "questions": [
                    "How does casting lots challenge our modern emphasis on meritocracy and talent-based selection in ministry?",
                    "What does the equal treatment of 'teacher and scholar' reveal about God's view of service versus our human hierarchies?"
                ]
            },
            "18": {
                "analysis": "<strong>The eleventh to Azareel</strong>—this verse continues the systematic listing of temple musicians appointed by lot. Azareel (עֲזַרְאֵל, 'God has helped') served with his extended family unit of twelve, demonstrating that worship leadership was both individual calling and family heritage.<br><br>The repetitive formula throughout 1 Chronicles 25 (\"he, his sons, and his brethren, were twelve\") emphasizes the communal nature of Israelite worship. Unlike modern individualism, biblical ministry was embedded in kinship networks. Each course of twelve musicians served one week per rotation (24 weeks yearly), meaning Azareel's family dedicated roughly a month annually to full-time temple service while maintaining other vocations the rest of the year.",
                "historical": "The Levitical musicians descended from Asaph, Heman, and Jeduthun (25:1). These family guilds preserved musical traditions through oral transmission and apprenticeship. Archaeological evidence from Qumran and Masada confirms the continuation of these musical divisions into the Second Temple period.",
                "questions": [
                    "How might incorporating extended family into ministry callings enrich or complicate modern church leadership?",
                    "What advantages exist in rotating ministry responsibilities rather than permanent specialized roles?"
                ]
            },
            "28": {
                "analysis": "<strong>The one and twentieth to Hothir</strong> (הוֹתִיר, possibly 'He has left a remnant')—the 21st of 24 musical courses, Hothir was likely a son of Heman the seer (25:4). His name's possible meaning reflects the theological theme that God always preserves a faithful remnant, even as the nation's spiritual condition fluctuates.<br><br>The number symbolism is significant: 24 courses × 12 members = 288 total musicians (25:7), a multiple of 12 (tribes) and 24 (priestly divisions). This mathematical precision reflects the Chronicler's theology that worship must be orderly, not chaotic (cf. 1 Cor 14:33, 40). The seemingly mundane genealogical lists establish that every worshiper has a divinely appointed place in God's cosmic temple service.",
                "historical": "The Chronicler's emphasis on temple organization addressed the post-exilic community's need to rebuild not just structures but sacred institutions. These detailed lists legitimized Second Temple worship practices by rooting them in David's authoritative arrangements.",
                "questions": [
                    "How does the concept of a 'remnant' in Hothir's name encourage believers during seasons of spiritual decline?",
                    "What does the mathematical precision in worship organization suggest about God's character?"
                ]
            }
        },
        "26": {
            "7": {
                "analysis": "<strong>Whose brethren were strong men</strong> (חַיִל אֲנָשִׁים, <em>chayil anashim</em>)—literally 'men of valor/ability.' The gatekeepers required physical strength because they guarded temple treasuries and controlled access to sacred spaces. Obed-Edom's family (v.4-8) was blessed with 62 descendants, fulfilling God's promise when David brought the ark to his house (2 Sam 6:11-12).<br><br>The names carry significance: Othni (עָתְנִי, 'forceful'), Rephael (רְפָאֵל, 'God has healed'), Obed (עֹבֵד, 'servant'), Elzabad (אֶלְזָבָד, 'God has given'), Elihu (אֱלִיהוּא, 'He is my God'), and Semachiah (סְמַכְיָהוּ, 'Yahweh has sustained'). These theophoric names declared that temple service required both divine calling and human capability—grace and strength working together.",
                "historical": "The gatekeepers (שֹׁעֲרִים, <em>sho'arim</em>) were Levites responsible for temple security, preventing unauthorized entry (Num 18:1-7). Their role combined sacred duty with practical protection, guarding not just physical entrances but the holiness of God's dwelling. The 93 gatekeepers from Obed-Edom's line (26:8) demonstrated how one act of faithful hospitality to the ark multiplied into generational blessing.",
                "questions": [
                    "How do physical strength and spiritual calling intersect in your understanding of ministry qualifications?",
                    "What does the blessing on Obed-Edom's descendants teach about the generational impact of faithful service?"
                ]
            },
            "17": {
                "analysis": "<strong>Eastward were six Levites, northward four a day</strong>—this verse details the strategic deployment of gatekeepers at different temple entrances. The eastern gate received six guards (not four) because it was the main entrance where the glory of the Lord entered (Ezek 43:1-4) and where the high priest performed key rituals.<br><br><strong>Toward Asuppim two and two</strong>—Asuppim (אֲסֻפִּים, 'storehouses') required only four guards total (two pairs) because these treasuries were less trafficked. This proportional distribution reflects wise stewardship: greater protection where greater risk exists. The total deployment (6+4+4+4=18, plus additional gatekeepers) ensured 24/7 coverage, with guards working in shifts, much like the priests and musicians.",
                "historical": "The temple's four cardinal directions had spiritual significance. East faced the Holy of Holies (most sacred), north was for sacrificial preparation, south for public access, and west backed against the royal palace. This spatial theology taught that approaching God requires proper order and authorized entry points—a truth fulfilled in Christ as 'the door' (John 10:9).",
                "questions": [
                    "How does proportional allocation of resources (more guards where more needed) inform wise church administration?",
                    "What does the restricted access to God's presence in the Old Covenant reveal about the significance of Christ's open invitation?"
                ]
            },
            "27": {
                "analysis": "<strong>Out of the spoils won in battles did they dedicate to maintain the house of the LORD</strong>—this verse establishes the principle that war plunder was consecrated (קָדַשׁ, <em>qadash</em>) for temple upkeep. The Hebrew <em>milchamot</em> (battles) refers to Israel's defensive and conquest wars under divine mandate. Rather than hoarding wealth, victorious commanders like David, Joab, and others (vv.25-28) devoted captured treasure to God's house.<br><br>This practice fulfills the law in Numbers 31:25-30 requiring a portion of war spoils for the sanctuary. The theology: all victory comes from God, therefore the fruits of victory belong first to God. This prefigures Romans 12:1—presenting our bodies as living sacrifices—where spiritual battles result in offerings of worship. The maintenance (<em>chazaq</em>, 'to strengthen/repair') of God's house took priority over personal enrichment.",
                "historical": "David's wars expanded Israel's borders and brought immense wealth (captured gold, silver, bronze from Arameans, Moabites, Ammonites, etc.). Rather than building a personal treasury, David stockpiled these resources for Solomon's temple construction. This reverses ancient Near Eastern patterns where conquered wealth funded royal palaces and personal monuments.",
                "questions": [
                    "How should Christians today 'dedicate spoils' from their vocational and financial victories to God's work?",
                    "What does prioritizing temple maintenance over personal wealth reveal about David's understanding of stewardship?"
                ]
            }
        },
        "27": {
            "5": {
                "analysis": "<strong>Benaiah the son of Jehoiada, a chief priest</strong> (כֹּהֵן רֹאשׁ, <em>kohen rosh</em>)—Benaiah was both a mighty warrior (2 Sam 23:20-23) and descended from the priestly line. The phrase 'chief priest' likely means 'a priest of first rank' or possibly 'a leading priest' rather than high priest. He commanded 24,000 troops during the third month (Sivan, roughly May-June).<br><br>Benaiah's dual role as priest and military captain embodied Israel's theocratic ideal: no separation between sacred and secular. His legendary exploits—killing a lion in a pit on a snowy day, defeating two Moabite champions, killing an Egyptian giant with the giant's own spear—demonstrated that priestly piety and warrior courage are not contradictory but complementary. His appointment as Solomon's commander-in-chief (1 Kings 2:35) rewarded his loyalty during Adonijah's rebellion.",
                "historical": "The 12-month military rotation (24,000 soldiers × 12 months = 288,000 total) provided a standing army without permanent militarization. Each able-bodied man served one month annually, maintaining civilian life while ensuring national defense. This system balanced agricultural productivity with military readiness during David's empire period (circa 1000-970 BC).",
                "questions": [
                    "How does Benaiah's combination of priestly heritage and warrior prowess challenge false dichotomies between contemplation and action?",
                    "What advantages exist in a citizen-soldier model versus a professional military for maintaining both strength and humility?"
                ]
            },
            "15": {
                "analysis": "<strong>Heldai the Netophathite, of Othniel</strong>—the twelfth and final captain in David's rotational army, Heldai served during the twelfth month (Adar, roughly February-March). His designation 'the Netophathite' links him to Netophah, a Levitical city near Bethlehem (Neh 7:26), while 'of Othniel' connects him to the clan descended from Caleb's younger brother, Israel's first judge (Judg 3:9-11).<br><br>The completion of the yearly cycle with Heldai's command emphasizes the order and reliability of David's administration. Each captain commanded <strong>twenty and four thousand</strong>, the phrase repeated throughout chapter 27 like a liturgical refrain, underscoring both military might (288,000 troops total) and administrative precision. This structure ensured that no region bore disproportionate military burden and that the army remained accountable to tribal leadership rather than becoming a personal royal force.",
                "historical": "Netophah lay in Judah's hill country, breeding warriors familiar with defensive terrain. The connection to Othniel's clan recalled God's pattern of raising deliverers from unexpected sources (Othniel was nephew to Caleb, himself a non-Israelite Kenizzite who became Judah's champion). This genealogical note affirmed that faithfulness, not ethnic purity, qualified one for leadership in Israel.",
                "questions": [
                    "How does the rotational military system prevent the concentration of power that often corrupts permanent professional armies?",
                    "What does Heldai's connection to Othniel teach about God's willingness to use unexpected backgrounds for His purposes?"
                ]
            },
            "25": {
                "analysis": "<strong>Over the king's treasures was Azmaveth... over the storehouses in the fields... was Jehonathan</strong>—this verse distinguishes between central royal treasuries (אוֹצָר, <em>otsar</em>) managed by Azmaveth and distributed agricultural storehouses (אֹצָרוֹת, <em>otsarot</em>) managed by Jehonathan son of Uzziah. The dual administration prevented financial corruption through checks and balances: no single official controlled both liquid assets and agricultural commodities.<br><br>The phrase <strong>in the fields, in the cities, and in the villages, and in the castles</strong> indicates a comprehensive storage network throughout David's kingdom. These storehouses held grain reserves for famine years (cf. Joseph's administration in Egypt), military provisions, and taxation revenues. The names are significant: Azmaveth (עַזְמָוֶת, 'strong unto death'—unwavering loyalty) and Jehonathan (יְהוֹנָתָן, 'Yahweh has given'—acknowledgment that all wealth comes from God).",
                "historical": "Ancient Near Eastern kingdoms depended on efficient taxation and storage systems. David's administrative structure (27:25-31 lists various economic officials) transformed Israel from a tribal confederacy into a centralized monarchy capable of sustaining a standing army, royal court, and temple construction projects. This bureaucracy enabled Solomon's golden age but also sowed seeds for the eventual division between north and south over taxation disputes.",
                "questions": [
                    "How does separating financial management responsibilities create accountability in modern church or organizational leadership?",
                    "What does the extensive storage network reveal about the relationship between faith in God's provision and practical stewardship?"
                ]
            }
        },
        "28": {
            "1": {
                "analysis": "<strong>David assembled all the princes of Israel</strong>—this grand assembly (קָהַל, <em>qahal</em>) gathered every level of leadership: tribal princes, military captains (thousands and hundreds), royal stewards, and mighty warriors. The comprehensiveness establishes that Solomon's accession and temple-building project had national consensus, not merely royal decree.<br><br>The phrase <strong>all the substance and possession of the king, and of his sons</strong> indicates stewards managed not just state property but the royal family's personal holdings—no distinction existed between public and private royal wealth. David's transparent leadership convened this assembly <strong>unto Jerusalem</strong> to witness his charge to Solomon (vv.9-10) and the presentation of temple plans (vv.11-19). This public accountability prevented the secrecy that breeds tyranny. The Hebrew <em>gibbor chayil</em> ('mighty men of valor') recalls David's elite warriors (2 Sam 23) now integrated into official state administration.",
                "historical": "This assembly occurred near the end of David's 40-year reign (circa 970 BC), after suppressing Adonijah's coup attempt (1 Kings 1). By gathering all leadership, David ensured the transition to Solomon would be peaceful and that the temple project would be a national priority, not Solomon's personal ambition. The Chronicler emphasizes this assembly to legitimize Second Temple worship by connecting it to David's authoritative commission.",
                "questions": [
                    "How does David's inclusive assembly model challenge modern tendencies toward top-down, exclusive leadership decisions?",
                    "What safeguards does public accountability provide against the corruption that often accompanies leadership transitions?"
                ]
            },
            "11": {
                "analysis": "<strong>David gave to Solomon his son the pattern</strong> (תַּבְנִית, <em>tabnit</em>)—the same Hebrew word used when God gave Moses the tabernacle pattern (Ex 25:9, 40). This linguistic parallel establishes that Solomon's temple, like the tabernacle, was divinely revealed, not humanly designed. David received this <em>tabnit</em> 'by the Spirit' (v.12), making temple architecture a matter of revelation, not merely aesthetic preference.<br><br>The detailed list—<strong>porch, houses, treasuries, upper chambers, inner parlours, place of the mercy seat</strong>—demonstrates that God cares about spatial theology. Each architectural element taught doctrine: the progression from outer courts to Holy of Holies illustrated the difficulty of approaching God; the mercy seat (כַּפֹּרֶת, <em>kapporet</em>) where blood was sprinkled pictured atonement. This verse refutes the notion that worship style is purely pragmatic; form and function are integrated in biblical worship.",
                "historical": "David was prohibited from building the temple due to bloodshed (1 Chr 22:8; 28:3), but he prepared everything: materials, finances, and divinely revealed architectural plans. This prepared-but-not-executed role parallels Moses, who received tabernacle plans but Joshua led conquest. The temple's completion under Solomon (circa 960 BC) fulfilled Nathan's prophecy (2 Sam 7:12-13) that David's son would build God's house.",
                "questions": [
                    "How should the divinely revealed nature of temple architecture inform our theology of worship space and liturgy today?",
                    "What does David's acceptance of limitation (preparing but not building) teach about finding purpose in roles that don't bring personal glory?"
                ]
            },
            "21": {
                "analysis": "<strong>The courses of the priests and the Levites</strong> recalls the organized divisions established in chapters 23-26. David assures Solomon that the infrastructure is already in place—he won't build alone. The phrase <strong>every willing skilful man</strong> (כָּל־נָדִיב בַּחָכְמָה, <em>kol-nadiv bachochmah</em>) combines two essential qualities: <em>nadiv</em> (willing/generous heart) and <em>chochmah</em> (skill/wisdom).<br><br>This echoes Exodus 35:10, where Bezalel and craftsmen were both Spirit-filled and skilled. Biblical ministry requires both: willingness without skill produces zeal without knowledge; skill without willingness produces professionalism without passion. The concluding promise—<strong>all the people will be wholly at thy commandment</strong>—assures Solomon of national support. The Hebrew <em>mitzvah</em> (commandment) suggests not mere obedience but covenant loyalty; the people would follow Solomon because they followed God's revealed plan through David.",
                "historical": "Solomon's temple construction (960-953 BC) required 153,600 workers (2 Chr 2:17-18): 70,000 burden-bearers, 80,000 stone-cutters, 3,600 overseers. The project's success depended on willing skilled labor across generations. Tyrian craftsmen supplemented Israelite workers (1 Kings 5:6), demonstrating that even in sacred projects, God uses gifted unbelievers for His purposes.",
                "questions": [
                    "How can churches cultivate both willing hearts and skilled hands rather than settling for one or the other?",
                    "What does David's assurance of support teach about the importance of preparing successors rather than making them dependent?"
                ]
            }
        },
        "29": {
            "10": {
                "analysis": "<strong>David blessed the LORD before all the congregation</strong>—this public doxology (בָּרַךְ, <em>barach</em>) models responsive worship. Having received the people's freewill offerings (vv.6-9), David immediately redirects praise upward, preventing the assembly from honoring him instead of God. The address <strong>LORD God of Israel our father</strong> invokes covenant history: Israel's identity is rooted in Abraham, Isaac, and Jacob, not in royal achievements.<br><br>The phrase <strong>for ever and ever</strong> (לְעוֹלָם וָעֶד, <em>le'olam va'ed</em>) ascribes eternal majesty to God, contrasting human transience (v.15). This benediction launches one of Scripture's greatest prayers (vv.10-19), which Jesus echoed in the Lord's Prayer ('Thine is the kingdom and the power and the glory forever'—though absent from earliest manuscripts, reflecting liturgical tradition rooted in David's blessing). David's public worship taught Israel that all success originates with God, all resources belong to God, and all glory returns to God.",
                "historical": "This prayer occurred at the climax of David's final assembly (circa 970 BC), after the people donated lavishly for temple construction—about 185 tons of gold and 375 tons of silver (vv.3-7). Rather than leveraging this generosity for political capital, David used it as a teaching moment about God's ownership of all things. The Chronicler preserved this prayer as a model for post-exilic temple fundraising.",
                "questions": [
                    "How can leaders redirect praise away from themselves without false humility or awkwardness?",
                    "What does David's immediate blessing of God (rather than thanking donors) reveal about the proper direction of gratitude in Christian stewardship?"
                ]
            },
            "20": {
                "analysis": "<strong>Now bless the LORD your God</strong>—David calls the congregation to corporate worship (בָּרַךְ, <em>barach</em>). The shift from David's solo blessing (v.10) to congregational participation models biblical worship as dialogue, not monologue. The response is immediate and total: <strong>all the congregation blessed the LORD God of their fathers</strong>, affirming covenant continuity across generations.<br><br>The physical actions—<strong>bowed down their heads, and worshipped the LORD, and the king</strong>—combine posture with proclamation. The Hebrew <em>shachah</em> (worship/prostrate) is used twice: first toward Yahweh, then toward the king as His representative. This is not king-worship (forbidden in Scripture) but recognition of theocratic authority. They honored the king as God's anointed (<em>mashiach</em>), prefiguring ultimate submission to Christ, the Davidic Messiah. The grammatical structure makes clear: worship ascends to God first, honor to human authority second.",
                "historical": "This assembly worship event (circa 970 BC) was the culmination of David's reign and the inauguration of Solomon's. The dual focus—worshipping God and honoring the king—reflected Israel's theocracy where royal authority was derivative, not absolute. The Second Temple community reading Chronicles would recognize this as the ideal relationship between sacred and civil authority, which they lacked under Persian rule.",
                "questions": [
                    "How does the pattern of blessing God first, then honoring human authority, guard against both anarchy and totalitarianism?",
                    "What is the difference between honoring God-ordained authority and the idolatry of state-worship?"
                ]
            },
            "30": {
                "analysis": "<strong>With all his reign and his might</strong>—the final verse of 1 Chronicles summarizes David's 40-year kingship. The Hebrew <em>malkut</em> (reign/kingdom) and <em>gevurah</em> (might/power) encompass both political administration and military conquest. The phrase <strong>the times that went over him</strong> uses the verb <em>avar</em> (pass over/through), suggesting David experienced historical forces beyond his control—he was both actor and acted-upon.<br><br>The comprehensive scope—<strong>over him, and over Israel, and over all the kingdoms of the countries</strong>—moves from personal to national to international. David's life was not isolated but intersected with Egypt, Philistia, Aram, Moab, Ammon, and Edom. This global perspective suits Chronicles' purpose: to show Israel that their history is never merely local but part of God's redemptive plan for all nations. The verse's inconclusiveness (no final 'Amen' or benediction) propels readers forward to 2 Chronicles, where Solomon's temple represents the next chapter in God's dwelling with His people.",
                "historical": "Chronicles was written for post-exilic Jews (circa 450-400 BC) who had no king and lived under Persian authority. By ending with David's international influence, the Chronicler encouraged them that God's purposes transcend political circumstances. The messianic hope—a future son of David—would restore not just Israel but God's reign 'over all the kingdoms.'",
                "questions": [
                    "How does understanding that 'times go over us' (circumstances beyond our control) balance human agency with divine sovereignty?",
                    "What does the triple focus (individual, national, international) teach about the scope of our responsibilities as believers?"
                ]
            }
        }
    },
    "1_corinthians": {
        "1": {
            "10": {
                "analysis": "<strong>I beseech you, brethren, by the name of our Lord Jesus Christ</strong>—Paul's appeal (παρακαλῶ, <em>parakalo</em>) invokes Christ's authority, not apostolic rank. The basis for unity is the shared <em>name</em> (ὄνομα, <em>onoma</em>) into which they were baptized (v.13), representing total identification with Christ's person and work. <strong>That ye all speak the same thing</strong> (τὸ αὐτὸ λέγητε, <em>to auto legete</em>) doesn't mandate uniformity in all opinions but agreement on gospel essentials.<br><br>The diagnosis—<strong>divisions</strong> (σχίσματα, <em>schismata</em>, literally 'tears/rips')—indicates the church fabric was being torn. The solution: <strong>perfectly joined together</strong> (κατηρτισμένοι, <em>katertismenoi</em>), a term used for mending fishing nets (Mark 1:19) and setting broken bones. Unity requires active restoration work, not passive tolerance. <strong>Same mind and judgment</strong> (νοῦς, <em>nous</em>; γνώμη, <em>gnome</em>) distinguishes between intellectual conviction and practical application—both are necessary for genuine unity.",
                "historical": "Corinth was a cosmopolitan port city (population ~100,000) with extreme wealth disparity and philosophical pluralism. The church, planted by Paul circa AD 50-51 (Acts 18), was fracturing around personality cults (vv.11-12): Paul, Apollos, Cephas, Christ. Paul wrote 1 Corinthians circa AD 54-55 from Ephesus to address these divisions before they became irreparable schisms.",
                "questions": [
                    "Where does Paul's call for 'speaking the same thing' intersect with modern debates about theological diversity versus doctrinal precision?",
                    "How do 'mending' and 'setting bones' metaphors inform our approach to church conflict—active intervention versus hands-off tolerance?"
                ]
            },
            "20": {
                "analysis": "<strong>Where is the wise? where is the scribe? where is the disputer of this world?</strong>—Paul's rhetorical questions mock three types of human wisdom: Greek philosophers (σοφός, <em>sophos</em>), Jewish Torah scholars (γραμματεύς, <em>grammateus</em>), and Hellenistic debaters (συζητητής, <em>syzetetes</em>). The triple 'where?' (ποῦ, <em>pou</em>) implies these authorities are nowhere—absent when it matters most.<br><br><strong>Hath not God made foolish the wisdom of this world?</strong>—the verb <em>emorainen</em> (made foolish) is divine judgment. God didn't merely ignore human wisdom; He actively exposed its bankruptcy by accomplishing redemption through the cross, which human wisdom deemed absurd (v.18). The phrase <strong>wisdom of this world</strong> (σοφία τοῦ κόσμου, <em>sophia tou kosmou</em>) indicates not neutral learning but a worldview system opposed to God. This echoes Isaiah 29:14 (quoted in v.19): God destroys human wisdom that denies revelation.",
                "historical": "Corinth housed multiple philosophical schools (Stoicism, Epicureanism, Cynicism) and Jewish synagogues where Torah debate was prized. The Greeks sought wisdom (v.22), but the gospel message—crucified Messiah—was intellectual scandal (μωρία, <em>moria</em>, 'foolishness,' v.23). Paul's argument destabilized both Jewish expectations (Messiah should conquer) and Greek philosophy (gods don't suffer).",
                "questions": [
                    "How do we distinguish between God-given intellectual tools and 'wisdom of this world' that opposes revelation?",
                    "What does God's 'making foolish' of worldly wisdom imply about the relationship between academic credentials and spiritual authority?"
                ]
            },
            "30": {
                "analysis": "<strong>But of him are ye in Christ Jesus</strong>—the phrase <em>ex autou</em> (of/from Him) attributes salvation's origin solely to God, refuting any boasting (v.29). Our position <strong>in Christ</strong> (ἐν Χριστῷ, <em>en Christo</em>) is Paul's signature phrase (used 165 times), indicating vital union with Christ as our federal head. This is positional truth: we exist 'in Christ' by God's sovereign initiative.<br><br>Christ becomes four things <strong>unto us</strong> (ἡμῖν, <em>hemin</em>, dative of advantage): (1) <strong>wisdom</strong> (σοφία, <em>sophia</em>)—answering the Greeks' search (v.22); (2) <strong>righteousness</strong> (δικαιοσύνη, <em>dikaiosyne</em>)—legal standing before God; (3) <strong>sanctification</strong> (ἁγιασμός, <em>hagiasmos</em>)—progressive holiness; (4) <strong>redemption</strong> (ἀπολύτρωσις, <em>apolutrosis</em>)—liberation from sin's slavery. These cover justification (righteousness), sanctification (holiness), and consummation (final redemption). Christ is not a means to these benefits; He <em>is</em> these benefits.",
                "historical": "Corinthian believers were mostly low-status (vv.26-28)—not many wise, mighty, or noble. Their temptation was to supplement Christ with human wisdom/status to gain credibility. Paul insists Christ is comprehensively sufficient. This passage became foundational for Reformation theology: <em>solus Christus</em> (Christ alone) provides everything necessary for salvation.",
                "questions": [
                    "How do we practically live in the 'of Him' reality that salvation originates entirely with God and not our response?",
                    "Which of the four aspects (wisdom, righteousness, sanctification, redemption) are you most tempted to seek apart from Christ?"
                ]
            }
        },
        "2": {
            "9": {
                "analysis": "<strong>But as it is written</strong>—Paul loosely cites Isaiah 64:4 (also echoing 52:15; 65:17), but his version doesn't exactly match the Septuagint or Hebrew Masoretic Text. He likely combines multiple OT passages or quotes an intertestamental source (some church fathers suggested the Apocalypse of Elijah). The triad—<strong>eye hath not seen, ear heard, neither entered into the heart of man</strong>—encompasses all human sensory and cognitive faculties. God's prepared realities exceed all empirical observation and rational imagination.<br><br><strong>The things which God hath prepared</strong> (ἃ ἡτοίμασεν ὁ θεός, <em>ha hetoimasen ho theos</em>) uses the perfect tense, indicating completed preparation awaiting revelation. Critically, Paul is <em>not</em> discussing heaven's future glories (the verse is often misapplied in funeral contexts) but present gospel realities revealed by the Spirit (v.10). The phrase <strong>for them that love him</strong> echoes Deuteronomy 6:5 and identifies the recipients: those in covenant relationship, not generic humanity.",
                "historical": "Paul contrasts the 'wisdom of this age' (2:6) with revealed gospel wisdom. Corinthian converts came from mystery religions promising secret knowledge (gnosis). Paul counters: Christian truth isn't secret elitism but Spirit-revealed understanding given to all believers (vv.10-16). The gospel's riches surpass pagan mysteries and Jewish traditions alike.",
                "questions": [
                    "How does misapplying this verse to heaven (rather than present gospel realities) diminish our appreciation for what God has already revealed?",
                    "What practical difference does it make that God's prepared things are known by love (v.9) and revealed by the Spirit (v.10) rather than discovered by intellect?"
                ]
            }
        },
        "3": {
            "3": {
                "analysis": "<strong>For ye are yet carnal</strong> (σαρκικοί, <em>sarkikoi</em>)—Paul returns to the rebuke begun in 1:10-13. The Corinthians are genuine believers (3:1, 'babes in Christ') but behaving like unbelievers. <em>Sarkikoi</em> (fleshly/carnal) indicates those dominated by sin nature rather than Spirit. Evidence of carnality: <strong>envying, and strife, and divisions</strong> (ζῆλος, ἔρις, διχοστασίαι)—jealousy over gifts/status, quarreling over leaders, and factional splits.<br><br>The climactic accusation—<strong>are ye not carnal, and walk as men?</strong>—uses <em>anthropoi</em> (mere humans). To 'walk as men' means living according to fallen human nature, not the new creation identity believers possess. The rhetorical question expects the answer 'yes'—their behavior proves their carnality. This is devastating: they claimed spiritual superiority (4:8, 'ye are full, ye are rich') while living like pagans. The grammar emphasizes ongoing action (present tense): they <em>keep on</em> being carnal and <em>keep on</em> walking as mere humans.",
                "historical": "Corinth's church-splits revolved around personality cults (1:12: 'I am of Paul... Apollos... Cephas'). Ironically, while claiming spiritual sophistication, they demonstrated spiritual infancy. Paul's diagnosis—carnality manifested in division—remains the primary test of spiritual maturity. This passage became central to later holiness movements distinguishing positional sanctification (in Christ) from practical sanctification (Christ-likeness).",
                "questions": [
                    "What is the relationship between doctrinal knowledge and spiritual maturity if Corinthian believers could be orthodox yet carnal?",
                    "How do envy and division reveal carnality even when disguised in theological or worship-style debates?"
                ]
            }
        }
    }
}

def main():
    """Generate and add commentary for all 20 verses."""
    added_count = 0

    print("Adding commentary for 20 verses from 1 Chronicles and 1 Corinthians...\n")

    # Process 1 Chronicles verses
    for chapter, verses in commentaries["1_chronicles"].items():
        data = load_commentary_file("1_chronicles")
        for verse, commentary in verses.items():
            if chapter not in data['commentary']:
                data['commentary'][chapter] = {}
            if verse not in data['commentary'][chapter]:
                data['commentary'][chapter][verse] = commentary
                print(f"✓ Added 1 Chronicles {chapter}:{verse}")
                added_count += 1
            else:
                print(f"○ 1 Chronicles {chapter}:{verse} already exists, skipping")
        save_commentary_file("1_chronicles", data)

    # Process 1 Corinthians verses
    for chapter, verses in commentaries["1_corinthians"].items():
        data = load_commentary_file("1_corinthians")
        for verse, commentary in verses.items():
            if chapter not in data['commentary']:
                data['commentary'][chapter] = {}
            if verse not in data['commentary'][chapter]:
                data['commentary'][chapter][verse] = commentary
                print(f"✓ Added 1 Corinthians {chapter}:{verse}")
                added_count += 1
            else:
                print(f"○ 1 Corinthians {chapter}:{verse} already exists, skipping")
        save_commentary_file("1_corinthians", data)

    print(f"\n{'='*60}")
    print(f"SUMMARY: Added commentary for {added_count} verses")
    print(f"{'='*60}")
    print("\nBooks updated:")
    print("- /Users/kennethreitz/repos/kjvstudy.org/kjvstudy_org/data/verse_commentary/1_chronicles.json")
    print("- /Users/kennethreitz/repos/kjvstudy.org/kjvstudy_org/data/verse_commentary/1_corinthians.json")

if __name__ == "__main__":
    main()
