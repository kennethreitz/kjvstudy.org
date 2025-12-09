#!/usr/bin/env python3
"""Add John commentary - Part 2: Chapters 13-19."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

filepath = DATA_DIR / "john.json"
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

commentary = data.get("commentary", {})

# John commentary - Part 2
new_entries = {
    "13": {
        "38": {
            "analysis": "<strong>Jesus answered him, Wilt thou lay down thy life for my sake?</strong> (ἀποκρίνεται Ἰησοῦς· Τὴν ψυχήν σου ὑπὲρ ἐμοῦ θήσεις, <em>apokrinetai Iēsous· Tēn psychēn sou hyper emou thēseis</em>)—Jesus questions Peter's confident self-assessment (13:37). The verb θήσεις (<em>thēseis</em>, 'will you lay down') echoes Jesus's own statement about laying down His life (John 10:11, 15). <strong>Verily, verily, I say unto thee, The cock shall not crow, till thou hast denied me thrice</strong> (ἀμὴν ἀμὴν λέγω σοι, οὐ μὴ ἀλέκτωρ φωνήσῃ ἕως οὗ ἀρνήσῃ με τρίς, <em>amēn amēn legō soi, ou mē alektōr phōnēsē heōs hou arnēsē me tris</em>)—The double ἀμὴν (<em>amēn</em>, 'verily') emphasizes certainty. Peter will deny (ἀρνήσῃ, <em>arnēsē</em>, 'deny, disown') Jesus τρίς (<em>tris</em>, 'three times') before dawn.<br><br>This prophecy reveals Jesus's omniscience and Peter's overconfidence. Peter genuinely intended loyalty but didn't know his own weakness. Jesus's prediction isn't cruel but preparatory—knowing Peter will fail yet be restored teaches that discipleship depends on Christ's keeping power, not human strength. Peter's restoration (John 21:15-19) would prove grace triumphs over failure.",
            "historical": "This occurred in the Upper Room during the Last Supper, hours before Peter's actual denials (John 18:15-27). Peter's self-confidence was characteristic—he repeatedly spoke impulsively (Matthew 14:28; 16:22; 17:4). Yet Jesus chose him to lead the church, demonstrating God uses broken, restored sinners, not perfect saints.",
            "questions": [
                "How does Peter's overconfidence warn against trusting our own strength rather than depending on Christ's sustaining grace?",
                "What does Jesus's foreknowledge of Peter's failure yet continued investment in him teach about God's patient discipleship?",
                "How should Christians respond when we fail Christ—with despair like Judas or repentance like Peter?"
            ]
        }
    },
    "14": {
        "28": {
            "analysis": "<strong>Ye have heard how I said unto you, I go away, and come again unto you</strong>—Jesus reminds them of His previous teaching (14:3). <strong>If ye loved me, ye would rejoice, because I said, I go unto the Father: for my Father is greater than I</strong> (εἰ ἠγαπᾶτέ με ἐχάρητε ἄν, ὅτι πορεύομαι πρὸς τὸν πατέρα, ὅτι ὁ πατὴρ μείζων μού ἐστιν, <em>ei ēgapate me echarēte an, hoti poreuomai pros ton patera, hoti ho patēr meizōn mou estin</em>)—This verse requires careful exegesis. <strong>My Father is greater than I</strong> (ὁ πατὴρ μείζων μού ἐστιν, <em>ho patēr meizōn mou estin</em>) doesn't deny Jesus's deity but acknowledges His voluntary subordination during incarnation (Philippians 2:6-8). The Father is 'greater' (μείζων, <em>meizōn</em>) positionally, not ontologically—Jesus temporarily submitted to human limitations during His earthly ministry.<br><br>Jesus says if they loved Him properly, they'd rejoice at His return to glory rather than grieve His departure. His going to the Father means: completed atonement, resumed glory, and sent Spirit (John 16:7). Arians and Jehovah's Witnesses misuse this verse to deny Christ's deity, but context shows Jesus speaks of His mediatorial office during incarnation, not His essential nature (Colossians 2:9).",
            "historical": "This statement came during the Upper Room Discourse before crucifixion. Jesus was preparing disciples for His departure while affirming His unity with the Father (John 14:9-11). Early church councils (Nicaea 325, Constantinople 381) clarified that 'greater' refers to Jesus's voluntary human state, not inequality within the Trinity.",
            "questions": [
                "How does understanding Jesus's voluntary submission during incarnation reconcile this verse with His full deity?",
                "What does it mean to love Christ rightly—rejoicing in His glorification rather than selfishly wanting His physical presence?",
                "How should Christians use this verse apologetically when confronted by those who deny Christ's deity?"
            ]
        },
        "29": {
            "analysis": "<strong>And now I have told you before it come to pass, that, when it is come to pass, ye might believe</strong> (καὶ νῦν εἴρηκα ὑμῖν πρὶν γενέσθαι, ἵνα ὅταν γένηται πιστεύσητε, <em>kai nyn eirēka hymin prin genesthai, hina hotan genētai pisteusēte</em>)—Jesus predicts His death, resurrection, and return to the Father before it happens, so that when fulfilled, it will strengthen faith. The purpose clause ἵνα...πιστεύσητε (<em>hina...pisteusēte</em>, 'in order that you might believe') indicates that prophecy's fulfillment validates Jesus's divine knowledge and mission.<br><br>This principle—prophecy preceding fulfillment to confirm faith—operates throughout Scripture. Jesus repeatedly predicted His passion (Matthew 16:21; 17:22-23; 20:18-19) so disciples wouldn't stumble when it occurred. Fulfilled prophecy removes the excuse of doubt—God provides evidence before events to demonstrate sovereign control over history.",
            "historical": "When these predictions came true—crucifixion, resurrection, ascension—the disciples' faith solidified. Acts records their bold proclamation, rooted in fulfilled prophecy. Thomas's doubt (John 20:24-29) vanished when Jesus appeared; the disciples' fear transformed to courage when they witnessed what Jesus had foretold.",
            "questions": [
                "How does Jesus's predictive prophecy demonstrate His divine foreknowledge and strengthen faith when fulfilled?",
                "What role should fulfilled biblical prophecy play in apologetics and personal assurance of faith?",
                "How can Christians prepare others through teaching so unexpected trials don't destroy their faith?"
            ]
        },
        "30": {
            "analysis": "<strong>Hereafter I will not talk much with you: for the prince of this world cometh, and hath nothing in me</strong> (οὐκέτι πολλὰ λαλήσω μεθ' ὑμῶν, ἔρχεται γὰρ ὁ τοῦ κόσμου ἄρχων καὶ ἐν ἐμοὶ οὐκ ἔχει οὐδέν, <em>ouketi polla lalēsō meth' hymōn, erchetai gar ho tou kosmou archōn kai en emoi ouk echei ouden</em>)—Jesus announces His teaching time is ending because <strong>the prince of this world</strong> (ὁ τοῦ κόσμου ἄρχων, <em>ho tou kosmou archōn</em>, Satan) approaches—Judas's betrayal and the crucifixion plot. Yet critically, Satan <strong>hath nothing in me</strong> (ἐν ἐμοὶ οὐκ ἔχει οὐδέν, <em>en emoi ouk echei ouden</em>)—no sin, no claim, no foothold. Jesus is perfectly sinless (2 Corinthians 5:21; Hebrews 4:15; 1 Peter 2:22).<br><br>This affirms Christ's qualification as spotless sacrifice. Satan has claims on all humanity through sin (Romans 3:23), but Jesus is immune—no inherited sin nature, no personal sin, no vulnerability to temptation that resulted in sin. His voluntary death is therefore substitutionary, not deserved punishment.",
            "historical": "This statement came shortly before Jesus and the disciples left the Upper Room for Gethsemane (John 14:31). Within hours, Satan's attack through Judas, the Jewish leaders, and Roman authorities would commence. Yet Jesus confidently asserted Satan's powerlessness over Him—death would come by choice, not conquest.",
            "questions": [
                "How does Jesus's sinlessness—Satan having 'nothing in Him'—qualify Him as the perfect sacrifice for sin?",
                "What does it mean that Satan is 'prince of this world'—what power does he have, and what are its limits?",
                "How should Christians respond to satanic attack knowing that Satan had no claim on sinless Jesus yet has claims on us through remaining sin?"
            ]
        },
        "31": {
            "analysis": "<strong>But that the world may know that I love the Father; and as the Father gave me commandment, even so I do. Arise, let us go hence</strong> (ἀλλ' ἵνα γνῷ ὁ κόσμος ὅτι ἀγαπῶ τὸν πατέρα, καὶ καθὼς ἐνετείλατο μοί ὁ πατήρ, οὕτως ποιῶ. ἐγείρεσθε, ἄγωμεν ἐντεῦθεν, <em>all' hina gnō ho kosmos hoti agapō ton patera, kai kathōs eneteilato moi ho patēr, houtōs poiō. egeiresthe, agōmen enteuthen</em>)—Jesus explains His voluntary death: not Satan's victory but demonstration of His love for the Father. <strong>I love the Father</strong> (ἀγαπῶ τὸν πατέρα, <em>agapō ton patera</em>) using ἀγαπάω (<em>agapaō</em>, covenant love) shows the cross reveals Trinitarian love—the Son's obedience to the Father's redemptive plan. <strong>As the Father gave me commandment, even so I do</strong> (καθὼς ἐνετείλατο μοί ὁ πατήρ, οὕτως ποιῶ, <em>kathōs eneteilato moi ho patēr, houtōs poiō</em>)—perfect obedience to the Father's will. <strong>Arise, let us go hence</strong>—they leave the Upper Room for Gethsemane.<br><br>The cross is the supreme demonstration of the Son's love for the Father—willing obedience unto death (Philippians 2:8). This reframes the atonement: not merely God satisfying His wrath, but the Son joyfully honoring the Father by accomplishing redemption. The world sees God's love (John 3:16) and intra-Trinitarian love displayed at Calvary.",
            "historical": "This marks the transition from Upper Room discourse to Gethsemane. Chapters 15-17 may have been spoken en route or in the garden. Jesus went willingly, demonstrating the cross was voluntary submission to the Father's plan, not forced by circumstances or enemies.",
            "questions": [
                "How does viewing the cross as Jesus's love-demonstration to the Father enrich our understanding of atonement?",
                "What does Jesus's perfect obedience teach about true love—that it submits to God's will even when costly?",
                "How should Christians imitate Jesus's obedience to the Father's commands as demonstration of our love for God?"
            ]
        }
    },
    "15": {
        "27": {
            "analysis": "<strong>And ye also shall bear witness, because ye have been with me from the beginning</strong> (καὶ ὑμεῖς δὲ μαρτυρεῖτε, ὅτι ἀπ' ἀρχῆς μετ' ἐμοῦ ἐστε, <em>kai hymeis de martyreite, hoti ap' archēs met' emou este</em>)—After promising the Holy Spirit's witness (15:26), Jesus commissions the disciples as witnesses. μαρτυρεῖτε (<em>martyreite</em>, 'you bear witness') is imperative—not optional but commanded. Their qualification is ἀπ' ἀρχῆς μετ' ἐμοῦ ἐστε (<em>ap' archēs met' emou este</em>, 'from the beginning with me')—eyewitness testimony from those who companied with Jesus throughout His ministry (Acts 1:21-22).<br><br>Christian witness rests on historical events witnessed and testified by credible eyewitnesses, empowered by the Holy Spirit. The apostles' unique qualification was physical presence during Jesus's ministry; later believers witness based on the apostolic testimony preserved in Scripture and the Spirit's internal testimony (1 John 5:9-11).",
            "historical": "This commission was fulfilled starting at Pentecost (Acts 2). The apostles testified to Jesus's life, death, and resurrection with Spirit-empowered boldness (Acts 4:20, 33). Their eyewitness accounts, recorded in the Gospels and epistles, form the foundation of Christian faith (Ephesians 2:20).",
            "questions": [
                "How does the eyewitness nature of apostolic testimony validate the historical reliability of the Gospel accounts?",
                "What's the difference between the apostles' unique witness role and the ongoing witness of all believers?",
                "How do the Holy Spirit's witness and human witness work together in evangelism?"
            ]
        }
    },
    "17": {
        "22": {
            "analysis": "<strong>And the glory which thou gavest me I have given them; that they may be one, even as we are one</strong> (κἀγὼ τὴν δόξαν ἣν δέδωκάς μοι δέδωκα αὐτοῖς, ἵνα ὦσιν ἓν καθὼς ἡμεῖς ἕν, <em>kagō tēn doxan hēn dedōkas moi dedōka autois, hina ōsin hen kathōs hēmeis hen</em>)—Jesus prays that believers share in <strong>the glory</strong> (τὴν δόξαν, <em>tēn doxan</em>) the Father gave the Son. This isn't merely future glory but present participation in Christ's divine life. The purpose: <strong>that they may be one</strong> (ἵνα ὦσιν ἓν, <em>hina ōsin hen</em>), modeled on Trinitarian unity: <strong>even as we are one</strong> (καθὼς ἡμεῖς ἕν, <em>kathōs hēmeis hen</em>). Christian unity isn't organizational but ontological—participation in the divine nature (2 Peter 1:4) through union with Christ.<br><br>This profound prayer reveals that believers' unity flows from sharing Christ's glory—His presence, character, and mission. Division among Christians contradicts our nature as people indwelt by the same Spirit and united to the same Head. True unity requires supernatural transformation, not merely ecumenical agreement.",
            "historical": "This is part of Jesus's High Priestly Prayer (John 17) before His arrest. He prayed not only for the eleven disciples but 'for them also which shall believe on me through their word' (17:20)—all future Christians. Church history shows the struggle to maintain unity; divisions reveal how Christians often live below their calling.",
            "questions": [
                "How does sharing in Christ's glory create the basis for Christian unity rather than mere institutional organization?",
                "What does it mean that Christian unity is modeled on Trinitarian unity—distinct persons in perfect communion?",
                "How should churches pursue unity while maintaining doctrinal faithfulness—balancing truth and love?"
            ]
        },
        "23": {
            "analysis": "<strong>I in them, and thou in me, that they may be made perfect in one</strong> (ἐγὼ ἐν αὐτοῖς καὶ σὺ ἐν ἐμοί, ἵνα ὦσιν τετελειωμένοι εἰς ἕν, <em>egō en autois kai sy en emoi, hina ōsin teteleiōmenoi eis hen</em>)—The chain of union: Father in Son, Son in believers, creating perfect unity. τετελειωμένοι (<em>teteleiōmenoi</em>, 'perfected, made complete') indicates process toward completeness εἰς ἕν (<em>eis hen</em>, 'into one'). <strong>And that the world may know that thou hast sent me, and hast loved them, as thou hast loved me</strong> (καὶ ἵνα γινώσκῃ ὁ κόσμος ὅτι σύ με ἀπέστειλας καὶ ἠγάπησας αὐτοὺς καθὼς ἐμὲ ἠγάπησας, <em>kai hina ginōskē ho kosmos hoti sy me apesteilas kai ēgapēsas autous kathōs eme ēgapēsas</em>)—Christian unity authenticates Jesus's mission and reveals God's love to the world.<br><br>This staggering claim: the world recognizes Christ's divine mission through believers' supernatural unity. When the church displays loving unity amidst diversity, it witnesses to the reality of Jesus's incarnation and the Father's love. Conversely, church divisions undermine evangelistic credibility. The Father loves believers <strong>as</strong> He loves the Son—adopting us into His family.",
            "historical": "The early church's unity attracted converts: 'Behold, how they love one another!' (Tertullian reports). When Christians transcended ethnic, social, and economic divisions (Galatians 3:28), it demonstrated supernatural transformation. Modern church divisions—denominational, racial, class-based—hinder evangelistic impact by contradicting Jesus's prayer.",
            "questions": [
                "How does Christian unity (or disunity) serve as evidence for or against the gospel's truth claims?",
                "What does it mean that God loves believers 'as' He loves Christ—how should this transform our self-understanding?",
                "How can local churches pursue the unity Jesus prayed for while avoiding compromise of biblical truth?"
            ]
        },
        "24": {
            "analysis": "<strong>Father, I will that they also, whom thou hast given me, be with me where I am</strong> (Πάτερ, ὃ δέδωκάς μοι, θέλω ἵνα ὅπου εἰμὶ ἐγὼ κἀκεῖνοι ὦσιν μετ' ἐμοῦ, <em>Pater, ho dedōkas moi, thelō hina hopou eimi egō kakeinoi ōsin met' emou</em>)—Jesus uses θέλω (<em>thelō</em>, 'I will, desire') expressing authority as well as affection. He wills believers' eternal presence with Him. <strong>That they may behold my glory, which thou hast given me: for thou lovedst me before the foundation of the world</strong> (ἵνα θεωρῶσιν τὴν δόξαν τὴν ἐμὴν ἣν δέδωκάς μοι, ὅτι ἠγάπησάς με πρὸ καταβολῆς κόσμου, <em>hina theōrōsin tēn doxan tēn emēn hēn dedōkas moi, hoti ēgapēsas me pro katabolēs kosmou</em>)—Heaven's essence is beholding (θεωρῶσιν, <em>theōrōsin</em>, 'behold, gaze upon') Christ's glory (δόξαν, <em>doxan</em>) which He possessed πρὸ καταβολῆς κόσμου (<em>pro katabolēs kosmou</em>, 'before the foundation of the world')—His pre-incarnate, eternal glory.<br><br>This defines eternal life: not merely duration but quality—experiencing the love between Father and Son that existed before creation. The beatific vision (1 John 3:2) is seeing Christ as He truly is, sharing in the glory He had with the Father eternally. This surpasses all earthly joys.",
            "historical": "This prayer anticipates Christ's ascension and believers' future glorification. Paul echoes this: 'that I may know him, and the power of his resurrection' (Philippians 3:10); 'we shall be like him; for we shall see him as he is' (1 John 3:2). Heaven is Christocentric—the Lamb is its light (Revelation 21:23).",
            "questions": [
                "How does defining heaven as 'beholding Christ's glory' differ from popular notions of heaven as eternal pleasure park?",
                "What does it mean that Christ possessed glory 'before the foundation of the world'—how does this affirm His deity?",
                "How should the hope of eternally beholding Christ's glory shape present priorities and values?"
            ]
        },
        "25": {
            "analysis": "<strong>O righteous Father, the world hath not known thee: but I have known thee, and these have known that thou hast sent me</strong> (Πάτερ δίκαιε, καὶ ὁ κόσμος σε οὐκ ἔγνω, ἐγὼ δέ σε ἔγνων, καὶ οὗτοι ἔγνωσαν ὅτι σύ με ἀπέστειλας, <em>Pater dikaie, kai ho kosmos se ouk egnō, egō de se egnōn, kai houtoi egnōsan hoti sy me aposteilas</em>)—Jesus addresses the Father as <strong>righteous</strong> (δίκαιε, <em>dikaie</em>, 'just, righteous'), acknowledging divine justice. <strong>The world hath not known thee</strong> (ὁ κόσμος σε οὐκ ἔγνω, <em>ho kosmos se ouk egnō</em>)—willful ignorance, not mere lack of information. Yet Jesus knows the Father perfectly (ἐγὼ δέ σε ἔγνων, <em>egō de se egnōn</em>), and believers have come to know (ἔγνωσαν, <em>egnōsan</em>) that Jesus was sent by the Father—recognizing His divine mission.<br><br>This creates three categories: the world (willfully ignorant of God), Jesus (who knows the Father perfectly), and believers (who know Jesus was sent by the Father). Salvation is knowledge—not mere information but covenant relationship. The world's refusal to know God is culpable ignorance (Romans 1:20-21), making judgment righteous.",
            "historical": "This prayer concluded Jesus's public ministry. The contrast between 'the world' that rejects and 'these' who believe would intensify—the world would crucify Jesus, but believers would form the church. Paul later described the gospel as revealing what was hidden from the world (Colossians 1:26).",
            "questions": [
                "How does the world's refusal to 'know' God differ from intellectual ignorance—what makes it culpable?",
                "What does it mean to 'know' God through Christ—how is this knowledge different from knowing facts about God?",
                "How should believers live as those who 'know' in a world that refuses knowledge of God?"
            ]
        },
        "26": {
            "analysis": "<strong>And I have declared unto them thy name, and will declare it</strong> (καὶ ἐγνώρισα αὐτοῖς τὸ ὄνομά σου καὶ γνωρίσω, <em>kai egnōrisa autois to onoma sou kai gnōrisō</em>)—Jesus revealed God's character (ὄνομα, <em>onoma</em>, 'name' meaning nature, character, reputation) during His earthly ministry and will continue through the Spirit (John 16:13-15). γνωρίσω (<em>gnōrisō</em>, 'I will make known') is future tense—ongoing revelation. <strong>That the love wherewith thou hast loved me may be in them, and I in them</strong> (ἵνα ἡ ἀγάπη ἣν ἠγάπησάς με ἐν αὐτοῖς ᾖ κἀγὼ ἐν αὐτοῖς, <em>hina hē agapē hēn ēgapēsas me en autois ē kagō en autois</em>)—The goal: believers experience the same love (ἡ ἀγάπη, <em>hē agapē</em>) the Father has for the Son, with Christ dwelling in them (κἀγὼ ἐν αὐτοῖς, <em>kagō en autois</em>).<br><br>This concludes the High Priestly Prayer with stunning revelation: God's love for believers equals His love for Christ; Christ dwells in believers. This is mystical union—not absorption into deity but intimate communion. Christianity isn't merely forgiveness of sins but adoption into Trinitarian love. Knowing God's name means experiencing His love.",
            "historical": "After this prayer, Jesus went to Gethsemane (John 18:1). His final words before arrest concerned believers' participation in divine love—demonstrating that His mission's goal was not merely legal justification but relational transformation. The Spirit would continue Christ's revelatory work (John 14:26; 16:13).",
            "questions": [
                "How does Jesus's ongoing revelation of the Father's name through the Spirit shape Christian discipleship and growth?",
                "What does it mean that believers experience the same love the Father has for the Son—how should this transform our identity?",
                "How is Christ 'in' believers practically—what does His indwelling presence mean for daily life?"
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
            print(f"Added John {chapter}:{verse}")

data["commentary"] = commentary

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal John verses added (Part 2): {added_count}")
print(f"Saved to {filepath}")
