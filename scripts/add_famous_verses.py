#!/usr/bin/env python3
"""
Add commentary for famous Psalm verses to verse_commentary.json
Covers Psalms 1:1, 22:1, 23:6, 46:10, 91:11, 103:1, 139:23
"""

import json
from pathlib import Path


def merge_commentary_entries():
    """Merge famous verse commentaries into verse_commentary.json"""

    # Define paths
    script_dir = Path(__file__).parent
    commentary_file = script_dir.parent / "kjvstudy_org" / "data" / "verse_commentary" / "psalms.json"

    # New commentary data for famous Psalm verses
    new_commentary = {
        "1": {
            "1": {
                "analysis": "The psalm opens with a declaration of blessing upon the one who practices discernment in association: 'Blessed is the man that walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor sitteth in the seat of the scornful.' The Hebrew word for 'blessed' ('asher') means happy, fortunate, or favored by God. The verse employs a descending structure of three levels of involvement - walking, standing, sitting - suggesting progressive spiritual corruption. 'Counsel of the ungodly' (Hebrew 'etzah') refers to the advice and wisdom of those who reject God's law. The three parallel phrases (counsel/way/seat and ungodly/sinners/scornful) create a literary pattern emphasizing that following ungodly perspectives leads inevitably to ungodly behavior. The verse assumes that blessedness flows from careful choices about whom and what we follow. This is not isolation from the world but discriminating alignment - choosing to follow God's wisdom rather than human opposition to it. The progression from walking to sitting suggests that influences we entertain become increasingly difficult to abandon.",
                "historical": "Psalm 1 serves as a preface or introduction to the entire Psalter, likely added by editors. Its themes of contrasting the righteous with the wicked appear throughout wisdom literature (Proverbs, Job). The 'counsel of the ungodly' may reflect specific historical contexts - either resistance to idolatry during monarchy, or maintaining Jewish faith during exile. In the Second Temple period, this verse would have resonated with maintaining separation from Hellenistic and pagan influences that threatened Jewish identity. The emphasis on 'walking' rather than standing or sitting suggests an ancient Near Eastern understanding of life as a journey or way. The proverb 'the way of the righteous versus the way of the wicked' structures Proverbs and deuteronomic theology. Jesus echoes this teaching when warning about 'the broad way' versus 'the narrow way' (Matthew 7:13-14). The verse's placement at the Psalter's beginning indicates that following God's law through careful choice is foundational to all worship and prayer that follows. Its universalizing language ('the man') suggests applicability across generations and circumstances.",
                "questions": [
                    "What is the difference between withdrawal from the world and wisdom in choosing influences?",
                    "Why does the verse emphasize walking, standing, and sitting - the various degrees of involvement?",
                    "How does the Hebrew concept of blessing ('asher') relate to happiness and favor in our understanding?",
                    "What are modern examples of 'counsel of the ungodly' that might shape our values and decisions?",
                    "Why would this psalm be placed first in the Psalter, and what does that position tell us about its importance?"
                ]
            }
        },
        "22": {
            "1": {
                "analysis": "This verse contains the most poignant prayer of lament in Scripture: 'My God, my God, why hast thou forsaken me? why art thou so far from helping me, and from the words of my roaring?' The repetition 'My God, my God' emphasizes intimate covenant relationship despite the cry of abandonment. 'Forsaken' (Hebrew 'azab') means abandoned or left destitute. The psalmist expresses not doubting faith but anguished questioning - God remains 'my God' even while feeling abandoned. 'Why art thou so far' expresses the experience of divine hiddenness or silence, a profound spiritual trial. 'Roaring' (Hebrew 'shaagah') depicts the anguish of a wounded animal or person in extremity. The verse captures the paradox of faith - maintaining covenant relationship with God while experiencing complete abandonment. This is not cynical atheism but betrayal of intimate trust, which makes the abandonment cut more deeply. The verse validates human suffering and doubt within the framework of faith, teaching that wrestling with God is itself a form of prayer.",
                "historical": "Jesus quoted this verse on the cross (Matthew 27:46, Mark 15:34), identifying His crucifixion with this Davidic lament. The historical or literary context of Psalm 22 remains debated - it may reflect David's experience of persecution, or an author facing oppression during other historical periods. However, its prophetic fulfillment in Christ's passion is central to New Testament interpretation. The psalm may have been composed during a period of exile, persecution, or military defeat when God's presence seemed withdrawn. In the ancient world, to be forsaken by one's god meant complete devastation - loss of protection, honor, and identity. Yet the psalm's trajectory moves from lament to trust to future proclamation (verses 22-31), reflecting the Easter movement from crucifixion to resurrection. The rabbis considered this psalm a prototype of righteous suffering that would ultimately vindicate God's purposes. The verse's honesty about suffering without platitudes makes it profoundly pastoral - validating the experience of dark faith rather than demanding false certainty.",
                "questions": [
                    "How does calling God 'My God' while feeling forsaken demonstrate mature faith?",
                    "What does this verse teach us about the difference between doubt in God's existence and suffering in God's silence?",
                    "Why was it significant that Jesus quoted this psalm during His crucifixion?",
                    "How does this verse legitimize lament and questioning as forms of prayer?",
                    "What hope can we find in a psalm that begins with such anguish yet ends in confidence?"
                ]
            }
        },
        "23": {
            "6": {
                "analysis": "The psalm concludes with confident assurance: 'Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever.' 'Surely' (Hebrew 'ak') introduces a strong affirmation based on the preceding covenant faithfulness of the Shepherd. 'Goodness' (Hebrew 'tov') encompasses all divine benefits, blessing, and favor. 'Mercy' (Hebrew 'hesed') denotes covenant loyalty, kindness, and unbreakable commitment. 'Follow me' (Hebrew 'radaph') means pursue relentlessly - goodness and mercy actively pursue the sheep. The image transforms from protection during danger to blessing in response to faithfulness. 'All the days of my life' covers the entire lifespan, moving from present experience to future assurance. 'Dwell in the house of the LORD for ever' transcends earthly life, referring to eternal communion with God in His dwelling place. This is not merely surviving threats but dwelling in intimate presence. The verse climaxes the psalm's movement from vulnerable sheep to confident heir, from provision in the wilderness to permanent residence in God's house. It answers the deepest human longing - to be pursued by goodness rather than pursued by enemies, and to find permanent home.",
                "historical": "This verse represents eschatological hope in the Old Testament - the promise of eternal communion with God. In the Second Temple period, this psalm would have been sung in liturgical worship, with 'the house of the LORD' referring to the Jerusalem temple. However, the phrase 'for ever' suggests longing beyond earthly temple worship toward the eternal temple described in Revelation 21:3. The psalm may reflect both David's experience as a shepherd-king finding confidence in God's protection, and the broader faith of Israel facing exile or oppression. Eusebius and early Church Fathers identified this psalm with Christ as the Good Shepherd. The vision of goodness and mercy 'following' (pursuing) the righteous anticipates Psalm 145:19 ('He will fulfil the desire of them that fear him') and ultimately Romans 8:28-39, where nothing can separate us from God's love. The shift from 'beside me' (verse 4 - shepherd's rod and staff) to 'before me' (table in verse 5) to 'follow me' creates a complete envelopment of God's care. The eternal dwelling in God's house becomes the eschatological fulfillment of the covenant relationship symbolized in temple worship.",
                "questions": [
                    "How does the image of goodness and mercy pursuing us differ from merely receiving mercy when we ask?",
                    "What is the significance of moving from survival provisions to dwelling in God's house for ever?",
                    "How does 'the house of the LORD' in ancient context connect to New Testament promises of eternal home?",
                    "Why does the psalm conclude with eternity rather than ending with present protection?",
                    "What comfort does this promise provide in facing the reality and awareness of our mortality?"
                ]
            }
        },
        "46": {
            "10": {
                "analysis": "The verse captures the essence of surrender and trust: 'Be still, and know that I am God: I will be exalted among the heathen, I will be exalted in the earth.' 'Be still' (Hebrew 'rapah') means to cease, to let go, to stop striving. This is not passivity but active relinquishment of human control and anxiety. 'Know' (Hebrew 'yada') involves not mere intellectual assent but relational recognition and acceptance of God's sovereignty. The command to know comes at a moment of complete helplessness - it presupposes the cessation of self-effort. The phrase 'I am God' (Hebrew 'Ani Elohim') is a divine self-declaration of absolute power and authority. The parallelism 'I will be exalted among the heathen, I will be exalted in the earth' uses repetition to emphasize universal recognition of God's supremacy. The verse does not promise absence of struggle but promises perspective - in trusting silence, we recognize God's ultimate control regardless of immediate circumstances. The movement from command ('Be still') to confidence ('I will be exalted') suggests that true peace flows from abandoning self-reliance and recognizing divine sovereignty. This is contemplative theology - knowing God through cessation rather than doing.",
                "historical": "Psalm 46 is titled 'A Song for the sons of Korah' and may commemorate God's protection of Jerusalem during the Assyrian crisis (701 BCE), when Sennacherib's army surrounded the city. The psalm's repeated refrain 'The LORD of hosts is with us' (verses 7, 11) reflects the miraculous deliverance recorded in 2 Kings 19:35, where an angel destroyed the Assyrian army in one night. In this context, verse 10's command to 'be still' addresses the panic and military preparations of the city - a call to trust in God rather than in military might. The verse also resonates with wisdom literature's understanding of inner peace as a fruit of faith (Proverbs 3:5-6). In Christian devotional tradition, this verse has become foundational to contemplative prayer and meditation, emphasizing that knowing God (not merely knowing about God) requires quieting the human will. Reformers and modern theologians have cited this verse in critiquing activism and works-righteousness, arguing that salvation and peace flow from faith rather than achievement. The verse's invitation to 'stillness' offers counter-cultural wisdom in ages of activism, anxiety, and constant striving.",
                "questions": [
                    "What does it mean to 'be still' and how does this differ from mere inactivity or passivity?",
                    "How can stopping our striving actually increase our ability to recognize God's action?",
                    "What did 'be still' mean in the historical context of Jerusalem facing military siege?",
                    "Why is 'knowing' that God is God described as the outcome of being still rather than as a prerequisite?",
                    "How does this verse challenge modern approaches to faith that emphasize action, achievement, and taking control?"
                ]
            }
        },
        "91": {
            "11": {
                "analysis": "This verse promises divine protection through angelic ministry: 'For he shall give his angels charge over thee, to keep thee in all thy ways.' 'Angels' (Hebrew 'malakeem') are God's messengers and servants, depicted throughout Scripture as instruments of divine will. 'Charge' (Hebrew 'tzavah') means to command, indicating that angelic protection is not accident but divine assignment. 'Keep thee' (Hebrew 'shamar') suggests guarding, watching, and preserving. 'In all thy ways' indicates protection throughout all circumstances and decisions of life. The verse emphasizes that God's protection is comprehensive and personal, not generic. The assignment of angels specifically 'over' the protected person suggests constant vigilance. This verse embodies the theology that God's care extends beyond abstract providence to personal, concrete protection through spiritual agencies. The promise does not guarantee absence of hardship but affirms that God's protective purpose works through angelic ministry. The verse affirms both God's ultimate protection and the reality of spiritual conflict, suggesting that invisible forces work on behalf of the righteous.",
                "historical": "Satan quoted this very verse to Jesus during the temptation in the wilderness (Matthew 4:6, Luke 4:10-11), claiming it as justification for Jesus to throw Himself from the temple pinnacle. Jesus' response - 'It is written again, Thou shalt not tempt the Lord thy God' (Matthew 4:7) - demonstrates that the promise assumes alignment with God's will, not presumptuous testing of God's protection. The verse belongs to Psalm 91, titled the 'Psalm of Protection' or dwelling 'in the secret place of the most High.' In ancient Near Eastern thought, divine protection through angelic beings was common across cultures. Hebrew tradition depicts angels as active agents - Abraham's three visitors (Genesis 18), Jacob's wrestling angel (Genesis 32), Hagar's angel (Genesis 16), and the angel of the LORD throughout Scripture. The promise gained particular significance in Jewish tradition during persecution - the assurance that even when human power seemed overwhelming, God's angelic forces were deployed on behalf of the faithful. Christian tradition has developed rich angelology based partly on verses like this, though Protestant Reformation caution against angel worship has tempered medieval excesses. The verse remains foundational to intercessory prayer practices emphasizing belief in angelic intercession.",
                "questions": [
                    "How does angelic protection relate to God's sovereignty - are angels active agents or does God work directly?",
                    "Why did Satan's misquotation of this verse distort the promise into presumption?",
                    "What is the difference between God's promise of protection and protection from all danger or suffering?",
                    "How should belief in angelic protection shape our understanding of prayer and spiritual warfare?",
                    "Why does God work through angelic agencies rather than directly intervening in all situations?"
                ]
            }
        },
        "103": {
            "1": {
                "analysis": "The psalm opens with an exhortation to comprehensive praise: 'Bless the LORD, O my soul: and all that is within me, bless his holy name.' 'Bless the LORD' (Hebrew 'barak et YHWH') means to praise, to acknowledge worth and dignity. The address 'O my soul' ('nephesh') appeals to the deepest center of the person - the seat of will, desire, and being. 'All that is within me' emphasizes that every dimension of the person participates in worship - not just lips or intellect but the totality of being. 'His holy name' indicates that the focus is God's character as revealed in His self-designation and reputation. The structure moves from internal orientation ('my soul,' 'all within me') to external action (praising God's name). The repetition of 'bless' creates an emphatic exhortation - not a quiet meditation but a vigorous rousing of the whole self toward worship. The verse establishes that genuine praise involves the mobilization of the entire person toward recognition of God's holiness. This is not dutiful obligation but willing overflow of gratitude. The verse's repetition suggests that without intentional exhortation to ourselves, we may neglect or forget to praise.",
                "historical": "Psalm 103 is traditionally attributed to David and emphasizes God's compassion despite human sin and mortality. The psalm's themes of redemption, healing, forgiveness, and divine compassion suggest possible contexts of David's life - recovery from illness (2 Samuel 12:10-23), forgiveness after sin (2 Samuel 11-12), or confidence despite enemies. However, the psalm's universal scope ('all that is within me,' the breadth of verses 2-18) suggests it may have been used communally in temple worship. The Hebrew phrase 'nephesh' (soul) undergoes development in biblical theology - while sometimes referring to life force or breath, here it denotes the conscious, willing center of personhood. The exhortation to bless God with 'all that is within me' echoes the Shema ('Love the LORD your God with all your heart, all your soul, all your mind' - Deuteronomy 6:5), suggesting that wholehearted devotion is central to covenant response. The psalm appears regularly in Jewish and Christian liturgical prayer, often used as a call to worship. The personal ('my soul') combined with universal scope ('all within me') reflects both individual and communal dimensions of worship.",
                "questions": [
                    "Why does the psalmist need to exhort himself to bless God - doesn't genuine emotion overflow naturally?",
                    "What is the significance of addressing the 'soul' as something to be commanded or persuaded?",
                    "How does engaging the whole person in worship differ from intellectual agreement with theological truths?",
                    "What does it mean that this psalm is addressed both individually and for communal worship?",
                    "Why begin a psalm cataloging God's compassion with a call to personal motivation rather than with the facts themselves?"
                ]
            }
        },
        "139": {
            "23": {
                "analysis": "The psalm reaches its climactic prayer: 'Search me, O God, and know my heart: try me, and know my thoughts.' 'Search' (Hebrew 'chaqar') means to examine thoroughly, to investigate from all angles. The parallel 'know my heart' and 'know my thoughts' emphasize that this examination is not superficial but penetrates to the deepest levels of motivation and intention. 'Try me' (Hebrew 'bachan') means to test, to prove, or to attempt - suggesting that the examination is transformative, not merely informational. 'Thoughts' (Hebrew 'siaach') includes both intellectual concepts and the patterns of consciousness. The dramatic move from verses 1-22 (celebrating God's omniscience) to verse 23 is from doctrine to prayer - from understanding God's all-knowing nature to inviting His examination of oneself. The psalmist doesn't merely acknowledge but invites divine scrutiny. This represents the height of trust and surrender - opening the deepest self to God's penetrating gaze. The verse assumes that God's knowledge, while comprehensive, can become personally transformative when we submit to it consciously. Self-deception and spiritual blindness are recognized as genuine dangers requiring divine examination.",
                "historical": "Psalm 139 is often attributed to David and explores God's omniscience - that God knows us completely, is always present, and understands us better than we understand ourselves (verse 6). The psalm appears to have emerged from reflective meditation on divine attributes rather than addressing a specific historical crisis. However, the movement from assertion of God's knowledge (verses 1-18) to prayer for examination (verses 23-24) suggests spiritual maturity - recognizing that intellectual knowledge of God's omniscience becomes salvific only through personal submission to that scrutiny. The verse's invitation to examination reflects the Hebrew prophetic tradition of examining the nation's unfaithfulness (Jeremiah's confessions, Hosea's call to repentance). In Christian tradition, this verse has become central to confession and spiritual direction - the understanding that genuine transformation requires acknowledging not just external behavior but hidden motivations and thoughts. The psalm's emphasis on God knowing us 'before a word is on my tongue' (verse 4) and forming us in the womb (verses 13-16) reflects a theology of radical dependence - we are known and formed by God. The psalmist's invitation to examination becomes an act of faith, trusting that divine knowledge serves redemptive rather than condemning purposes.",
                "questions": [
                    "What is the difference between acknowledging God's omniscience intellectually and inviting His examination personally?",
                    "Why is self-deception about our own hearts and motives described as such a serious spiritual problem?",
                    "How does God's 'trying' or testing us lead to transformation rather than condemnation?",
                    "What courage does it require to pray 'Search me, O God' given the exposure such examination brings?",
                    "How does this prayer reflect mature faith - the willingness to be known completely and transformed by that knowledge?"
                ]
            }
        }
    }

    print("Loading verse_commentary.json...")
    with open(commentary_file, 'r', encoding='utf-8') as f:
        commentary = json.load(f)

    # Merge new commentary
    merged_count = 0
    for book, chapters in new_commentary.items():
        if book not in commentary:
            commentary[book] = {}
            print(f"  + Added new book: Psalm {book}")

        for chapter, verses in chapters.items():
            if chapter not in commentary[book]:
                commentary[book][chapter] = {}

            for verse, content in verses.items():
                commentary[book][chapter][verse] = content
                merged_count += 1
                print(f"  ✓ Merged Psalm {book}:{verse}")

    # Write back to file
    print(f"\nWriting merged commentary to {commentary_file}...")
    with open(commentary_file, 'w', encoding='utf-8') as f:
        json.dump(commentary, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully merged {merged_count} commentaries")

    # Verify merge
    print("\nVerifying merge...")
    with open(commentary_file, 'r', encoding='utf-8') as f:
        verify_data = json.load(f)

    all_verified = True
    for book, chapters in new_commentary.items():
        for chapter, verses in chapters.items():
            for verse in verses.keys():
                if verse in verify_data.get(book, {}).get(chapter, {}):
                    print(f"  ✓ Verified Psalm {book}:{verse}")
                else:
                    print(f"  ✗ FAILED: Psalm {book}:{verse}")
                    all_verified = False

    if all_verified:
        print("\n" + "="*60)
        print("SUCCESS! All famous verse commentaries merged and verified.")
        print("="*60)
        return True
    else:
        print("\n" + "="*60)
        print("WARNING: Some verses failed verification!")
        print("="*60)
        return False


if __name__ == "__main__":
    merge_commentary_entries()
