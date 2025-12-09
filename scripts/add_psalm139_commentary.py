#!/usr/bin/env python3
"""
Add commentary for Psalm 139 verses on divine omniscience and omnipresence.
Safely merges with existing psalms.json file.
"""

import json
from pathlib import Path

# New commentary to add
NEW_COMMENTARY = {
    "1": {
        "analysis": "<strong>O LORD, thou hast searched me, and known me</strong>—The verb <em>chaqar</em> (חָקַר, 'searched') means to probe deeply, to examine thoroughly, like a miner excavating precious ore. This is no surface-level glance but divine investigation to the core of being. The parallel verb <em>yada</em> (יָדַע, 'known') signifies intimate, experiential knowledge—the same word used of marital union (Genesis 4:1). God doesn't merely know <em>about</em> us; He knows us with perfect, exhaustive intimacy.<br><br>David opens this psalm acknowledging that divine omniscience precedes human self-knowledge. Before we examine ourselves, we have already been examined by the One who formed us. This foundational truth grounds all authentic spirituality: we worship a God who knows us completely and loves us anyway.",
        "historical": "Composed by David, likely during his reign (c. 1010-970 BC). As Israel's shepherd-king, David understood both the comfort and weight of being known by God. This psalm reflects mature theological reflection on God's attributes, possibly written during a time of introspection or after experiencing God's protective providence.",
        "questions": [
            "What aspects of your life do you try to hide from God's searching gaze, even though He already knows them completely?",
            "How does knowing that God's knowledge of you is intimate (<em>yada</em>) rather than merely intellectual change your relationship with Him?",
            "In what ways does God's exhaustive knowledge of you bring comfort rather than fear?"
        ]
    },
    "2": {
        "analysis": "<strong>Thou knowest my downsitting and mine uprising, thou understandest my thought afar off</strong>—God's omniscience extends to the mundane rhythm of daily life: sitting down and standing up, the bookends of every human activity. The Hebrew <em>binah</em> (בִּינָה, 'understandest') suggests discernment of what lies beneath the surface. God perceives our thoughts while they're still 'afar off'—before they fully form, while still inchoate desires and half-formed intentions.<br><br>No moment is too trivial for divine attention, no thought too fleeting to escape God's notice. This verse demolishes the false dichotomy between 'sacred' and 'secular'—all of life unfolds under the watchful eye of Him who numbers our hairs (Matthew 10:30). The God who governs galaxies attends to whether you sit or stand.",
        "historical": "Ancient Near Eastern religions often portrayed gods as distant, capricious beings requiring elaborate rituals to gain their attention. David's portrayal of YHWH as intimately aware of mundane human actions was radically counter-cultural, emphasizing the covenant God's personal involvement with His people.",
        "questions": [
            "How would your daily routine change if you lived consciously aware that God knows your every sitting and rising?",
            "What 'afar off' thoughts—barely-formed desires or intentions—might God be discerning in you right now?",
            "Do you compartmentalize your life into 'spiritual' and 'ordinary' moments, forgetting that all moments are known to God?"
        ]
    },
    "3": {
        "analysis": "<strong>Thou compassest my path and my lying down, and art acquainted with all my ways</strong>—The verb <em>zarah</em> (זָרָה, 'compassest') means to winnow or sift grain, examining every kernel. God sifts our path (journey, course of life) and our lying down (rest, private life). The phrase <em>art acquainted</em> comes from <em>sakan</em> (סָכַן), meaning to be familiar through careful observation, like a neighbor who knows your habits.<br><br>God's knowledge isn't abstract but detailed and specific. He knows not just that we travel but every step of the journey; not just that we rest but the quality of our sleep and the thoughts that keep us awake. Every way (<em>derek</em>, דֶּרֶךְ)—our habits, choices, patterns of behavior—stands open before Him. This is total transparency before absolute holiness.",
        "historical": "In David's era, paths were dangerous—bandits, wild animals, harsh terrain. The imagery of God 'compassing' or encircling one's path evoked both protection and examination. Similarly, lying down in ancient tents offered little privacy. David uses these realities to illustrate that nothing in human life escapes divine awareness.",
        "questions": [
            "If God is 'winnowing' your path, what chaff (worthless pursuits or sins) might He be separating from the wheat?",
            "What do you do in private ('lying down') that you wouldn't do if you were fully conscious of God's presence?",
            "How familiar (<em>sakan</em>) is God with your habitual 'ways'—and what do those patterns reveal about your heart?"
        ]
    },
    "4": {
        "analysis": "<strong>For there is not a word in my tongue, but, lo, O LORD, thou knowest it altogether</strong>—God's omniscience anticipates even our speech. Before a word exists <em>in</em> (בְּ) the tongue—before articulation, while still mere intention—the LORD knows it <em>altogether</em> (<em>kulloh</em>, כֻּלֹּה, 'completely, entirely'). Jesus echoed this truth: we will give account for every idle word (Matthew 12:36).<br><br>This verse exposes the futility of verbal pretense. We craft our words to manage others' perceptions, but we cannot edit our speech before God, who hears both what we say and what we meant to say, both our words and the heart-motives beneath them. Every prayer, promise, boast, and lie stands naked before Him who <em>knows it altogether</em>.",
        "historical": "In ancient Israel, words carried tremendous weight—blessings and curses were considered effectual, oaths binding, vows sacred. David's acknowledgment that God knows words before they're spoken underscores divine foreknowledge and the moral accountability of speech, central to Hebrew wisdom literature (Proverbs 18:21).",
        "questions": [
            "What words do you shape carefully for others' ears but cannot hide from God who knows them 'altogether'?",
            "How would your speech change if you remembered that God hears your words before your tongue forms them?",
            "Are there prayers you've prayed with your lips while your heart said something different—and what does God know 'altogether' about that disconnect?"
        ]
    },
    "5": {
        "analysis": "<strong>Thou hast beset me behind and before, and laid thine hand upon me</strong>—The verb <em>tzur</em> (צוּר, 'beset') means to bind, confine, or enclose—like a city under siege. God surrounds David from all temporal directions: behind (past) and before (future). This is not hostile encirclement but protective encompassing. The laying on of God's hand (<em>kaph</em>, כַּף) suggests both authority and blessing, like a hand placed on one's head in commissioning.<br><br>David cannot escape into past regrets or future anxieties; God occupies every temporal space. This divine 'besetting' means we cannot outrun our history or our destiny—both are held in God's hand. The very hand that constrains us also guides, protects, and blesses.",
        "historical": "The imagery of being 'beset' would resonate deeply with David, who experienced literal siege warfare and also God's protective encirclement during his fugitive years fleeing Saul. This military metaphor transforms into a theological truth: God's sovereignty surrounds us completely.",
        "questions": [
            "What 'behind' (past failures or sins) or 'before' (future fears) are you trying to escape from, forgetting that God has already 'beset' those times with His presence?",
            "How does it feel to be 'confined' by God—is it oppressive restriction or liberating security?",
            "Where in your life do you need to feel God's hand laid upon you—for guidance, for healing, for commissioning?"
        ]
    },
    "6": {
        "analysis": "<strong>Such knowledge is too wonderful for me; it is high, I cannot attain unto it</strong>—The adjective <em>pele</em> (פֶּלֶא, 'wonderful') denotes what is extraordinary, surpassing, miraculous—used of God's mighty works (Exodus 15:11). Divine omniscience isn't just comprehensive but <em>qualitatively different</em> from human knowledge. It is <em>high</em> (<em>sagab</em>, שָׂגַב)—exalted, inaccessible, beyond reach. David doesn't mean he cannot comprehend God's knowledge intellectually (though that's true); he means he cannot <em>attain</em> it experientially or possess it.<br><br>This is the proper posture before mystery: wonder rather than mastery. The finite cannot contain the infinite. God's knowledge humbles us not to despair but to worship. We don't need to know everything God knows; we need to trust the One who does.",
        "historical": "Ancient wisdom literature frequently acknowledged the limits of human understanding compared to divine wisdom (Job 28:12-28; Proverbs 25:2). David, despite being a king with considerable power and knowledge, here models intellectual humility before the incomprehensible God—a corrective to human pride.",
        "questions": [
            "What aspects of God's knowledge do you struggle to accept because you cannot 'attain' them or understand them fully?",
            "How does acknowledging that God's knowledge is 'too wonderful' for you change your posture from trying to figure everything out to trusting Him?",
            "Are there mysteries in your life that God knows completely while you only see in part—and can you rest in His higher knowledge?"
        ]
    },
    "8": {
        "analysis": "<strong>If I ascend up into heaven, thou art there: if I make my bed in hell, behold, thou art there</strong>—David explores God's omnipresence through cosmic extremes. <em>Heaven</em> (<em>shamayim</em>, שָׁמַיִם) represents the highest heights, God's dwelling place. <em>Hell</em> (<em>sheol</em>, שְׁאוֹל) is the grave, the realm of the dead, the lowest depths. The emphatic <em>thou art there</em> (<em>sham attah</em>, שָׁם אַתָּה) brackets both locations—God's presence is not limited by spatial or spiritual boundaries.<br><br>Sheol was understood as shadowy separation from God's active presence (Psalm 88:5), yet even there, God <em>is</em>. This anticipates the Christian truth that Christ descended to the dead (1 Peter 3:19). There is literally nowhere—no height of blessing, no depth of despair—outside God's presence.",
        "historical": "Ancient cosmology conceived heaven above and sheol below, with earth between. David uses this three-tiered worldview to express God's universal presence. Notably, sheol wasn't hell in the later Christian sense but the shadowy underworld where all the dead went—making God's presence there even more remarkable.",
        "questions": [
            "What 'heavenly' highs or 'sheol' lows have you experienced where you felt God's presence was absent—and how does this verse challenge that perception?",
            "How does knowing that God is present even in sheol (death, darkness, separation) change how you face your deepest fears?",
            "Are you trying to ascend to some spiritual height to meet God, forgetting that He is already wherever you are?"
        ]
    },
    "9": {
        "analysis": "<strong>If I take the wings of the morning, and dwell in the uttermost parts of the sea</strong>—<em>Wings of the morning</em> (<em>kanfei-shachar</em>, כַּנְפֵי־שָׁחַר) evokes the swift, eastward-spreading dawn light—the fastest natural phenomenon known to the ancient world. To ride dawn's light from east to the furthest west (<em>uttermost parts of the sea</em> = westernmost Mediterranean) represents maximum speed and distance. David imagines impossible escape velocity.<br><br>Even if we could travel at the speed of light itself, racing the dawn across the planet, we couldn't outrun God. This isn't threatening pursuit but reassuring presence. Jonah tried fleeing west by sea (Jonah 1:3); he discovered the truth of this verse. Geography cannot distance us from God.",
        "historical": "For ancient Israelites landlocked in Judea, the sea (especially the westward Mediterranean) represented the edge of the known world—mysterious, dangerous, and distant. Dawn's eastward light racing to the western sea encompasses the entire known world, from boundary to boundary.",
        "questions": [
            "What are you running from—and how fast—believing you can outpace God's presence in your life?",
            "Like Jonah fleeing to the 'uttermost parts of the sea,' have you tried geographical escape from God's calling or conviction?",
            "How does the speed of 'morning's wings' illustrate that no matter how fast you run toward or away from something, God is already there?"
        ]
    },
    "10": {
        "analysis": "<strong>Even there shall thy hand lead me, and thy right hand shall hold me</strong>—The conditional clauses of verses 8-9 ('if I...') resolve in this assurance: <em>even there</em> (גַּם־שָׁם, <em>gam-sham</em>). Wherever 'there' is—heights, depths, east, west—God's hand performs a dual function: <em>lead</em> (<em>nachah</em>, נָחָה, to guide) and <em>hold</em> (<em>achaz</em>, אָחַז, to grasp firmly). The right hand signifies power and favor.<br><br>God's omnipresence isn't neutral surveillance but active guidance and protective grasp. We cannot flee beyond His reach, but why would we want to? His hand leads through unfamiliar territory and holds us secure in dangerous places. The same hand that created galaxies holds you steady.",
        "historical": "The right hand in Hebrew culture symbolized strength, authority, and covenant faithfulness. God's right hand delivered Israel from Egypt (Exodus 15:6), sustained them in wilderness, and seated the Messiah in power (Psalm 110:1). David draws on this rich tradition.",
        "questions": [
            "Where has God's hand led you that you didn't want to go—and in hindsight, how did that guidance prove faithful?",
            "What situation requires you to trust that God's right hand is holding you, even though you cannot see or feel it?",
            "How does knowing God will 'lead' and 'hold' you anywhere change your willingness to go where He sends?"
        ]
    },
    "11": {
        "analysis": "<strong>If I say, Surely the darkness shall cover me; even the night shall be light about me</strong>—David explores a third hypothetical escape: concealment in darkness (<em>choshek</em>, חֹשֶׁךְ). <em>Cover me</em> (<em>shuf</em>, שׁוּף) means to overwhelm or crush—darkness as refuge from exposure. But the conditional sentence breaks mid-verse (completed in v. 12): what we expect to be dark becomes light.<br><br>This anticipates both moral and literal truths. Morally: secret sins performed 'under cover of darkness' stand revealed to God (Ephesians 5:11-13). Literally: night doesn't diminish God's vision. We hide in darkness hoping for invisibility, but God dwells in unapproachable light (1 Timothy 6:16) and sees perfectly in absolute darkness.",
        "historical": "In pre-electric ancient world, darkness was total—no streetlights, no ambient glow. Night brought genuine concealment, making it prime time for crime and immorality. David's assertion that even night becomes light to God would have sounded radical, challenging assumptions about darkness as hiding place.",
        "questions": [
            "What do you do under 'cover of darkness'—literal night or metaphorical secrecy—that you wouldn't do in broad daylight before witnesses?",
            "How does knowing that darkness and light are alike to God affect your willingness to confess hidden sins?",
            "What darkness in your life—depression, ignorance, sin—needs to become 'light about you' through God's illuminating presence?"
        ]
    },
    "12": {
        "analysis": "<strong>Yea, the darkness hideth not from thee; but the night shineth as the day: the darkness and the light are both alike to thee</strong>—The emphatic <em>yea</em> (גַּם, <em>gam</em>) concludes the thought from v. 11. <em>Hideth not</em> (<em>lo-yachshik</em>, לֹא־יַחְשִׁיךְ)—darkness cannot darken things from God. Night <em>shines</em> (<em>ya'ir</em>, יָאִיר) as day—to divine perception, no difference exists. The final phrase <em>darkness and light are both alike</em> (<em>ka-choshekah ka-orah</em>, כַּחֲשֵׁיכָה כָאוֹרָה) uses <em>ka</em> (כַּ, 'as, like') twice—equal, equivalent, identical to God.<br><br>This obliterates our categories of concealment. God doesn't have night vision; He has perfect vision unaffected by ambient light levels. To Him who is light (1 John 1:5), all things are equally visible. This truth simultaneously comforts (God sees our affliction even in deepest darkness) and convicts (God sees our sin even in deepest secrecy).",
        "historical": "Light and darkness were primal categories in Hebrew thought—creation began with God separating light from darkness (Genesis 1:4). Yet the Creator transcends His creation; the distinction that organizes our reality doesn't limit His perception. This verse presents God as utterly beyond creaturely limitations.",
        "questions": [
            "Since darkness and light are alike to God, what does this reveal about the futility of trying to hide anything from Him?",
            "How does this truth comfort you when walking through your 'darkest valley' (Psalm 23:4)—that God sees perfectly even there?",
            "What would change if you lived every moment—public daylight and private nighttime—with equal consciousness that all is equally visible to God?"
        ]
    }
}

def main():
    json_path = Path("kjvstudy_org/data/verse_commentary/psalms.json")

    # Read existing file
    print("Reading existing psalms.json...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure structure exists
    if 'commentary' not in data:
        data['commentary'] = {}
    if '139' not in data['commentary']:
        data['commentary']['139'] = {}

    # Check what we're adding
    existing_verses = set(data['commentary']['139'].keys())
    new_verses = set(NEW_COMMENTARY.keys())
    overlap = existing_verses & new_verses

    if overlap:
        print(f"WARNING: These verses already exist: {sorted(overlap, key=int)}")
        print("They will be OVERWRITTEN.")

    # Merge new commentary
    print(f"\nAdding commentary for Psalm 139 verses: {sorted(NEW_COMMENTARY.keys(), key=int)}")
    for verse, commentary in NEW_COMMENTARY.items():
        data['commentary']['139'][verse] = commentary

    # Write back to file
    print("\nWriting updated file...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Summary
    all_verses = sorted(data['commentary']['139'].keys(), key=int)
    print(f"\n✓ Success! Psalm 139 now has commentary for {len(all_verses)} verses:")
    print(f"  Verses: {', '.join(all_verses)}")
    print(f"\n  Added: {', '.join(sorted(NEW_COMMENTARY.keys(), key=int))}")

if __name__ == "__main__":
    main()
