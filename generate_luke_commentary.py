#!/usr/bin/env python3
"""Generate commentary for missing Luke verses."""

import json

# Read existing luke.json
with open('kjvstudy_org/data/verse_commentary/luke.json', 'r') as f:
    data = json.load(f)

commentary = data.get('commentary', {})

# Ensure all chapter keys exist
for ch in range(1, 25):
    ch_str = str(ch)
    if ch_str not in commentary:
        commentary[ch_str] = {}

# Luke 6:47-49 - Parable of the Two Builders
commentary['6']['47'] = {
    "analysis": "<strong>Whosoever cometh to me, and heareth my sayings, and doeth them</strong> (ὁ ἐρχόμενος πρός με καὶ ἀκούων μου τῶν λόγων καὶ ποιῶν αὐτούς)—Jesus establishes three progressive conditions for true discipleship: coming (<em>erchomai</em>, approaching in relationship), hearing (<em>akouō</em>, attentive listening), and doing (<em>poieō</em>, active obedience). Luke's account emphasizes that genuine faith must manifest in obedience, not mere intellectual assent or emotional experience.<br><br>The phrase <strong>I will shew you to whom he is like</strong> introduces a parable about foundations—a common rabbinic teaching method. Jesus positions himself as the authoritative interpreter of what constitutes wise living, claiming divine prerogative to judge the validity of one's spiritual foundation. This echoes the Shema's call to not only hear but to obey (Deuteronomy 6:4-9).",
    "historical": "Luke places this teaching at the conclusion of the Sermon on the Plain (6:17-49), Jesus's programmatic discourse delivered to both disciples and crowds in Galilee. First-century Palestinian construction required deep foundations due to seasonal flooding from winter rains—builders who cut corners faced catastrophic losses. The imagery would resonate powerfully with Jesus's agrarian audience.",
    "questions": [
        "Which of the three conditions (coming, hearing, doing) represents your weakest area of discipleship currently?",
        "How does Jesus's emphasis on obedience challenge contemporary 'grace alone' perspectives that minimize behavioral transformation?",
        "What 'floods' (trials, temptations, cultural pressures) are currently testing whether your faith is built on rock or sand?"
    ]
}

commentary['6']['48'] = {
    "analysis": "<strong>He is like a man which built an house, and digged deep, and laid the foundation on a rock</strong> (ὅμοιός ἐστιν ἀνθρώπῳ οἰκοδομοῦντι οἰκίαν ὃς ἔσκαψεν καὶ ἐβάθυνεν καὶ ἔθηκεν θεμέλιον ἐπὶ τὴν πέτραν)—Luke's version emphasizes the <em>labor</em> involved: he 'digged' (<em>skaptō</em>) and 'went deep' (<em>bathunō</em>), terms suggesting strenuous excavation. Obedience to Christ's teachings requires deliberate effort and cost—there are no shortcuts to spiritual stability.<br><br>The rock foundation (<em>petra</em>) that withstands the flood's 'vehement beating' (<em>prosrēxen</em>, to break against) represents Christ himself and his authoritative word. <strong>Could not shake it: for it was founded upon a rock</strong>—the emphatic repetition underscores that the house's resilience derives entirely from its foundation, not the builder's skill or the structure's beauty. Paul later echoes this imagery: 'For other foundation can no man lay than that is laid, which is Jesus Christ' (1 Corinthians 3:11).",
    "historical": "Roman construction techniques in first-century Palestine included both sophisticated stone foundations (used in public buildings and wealthy homes) and cheaper earth-based construction. Flash floods from sudden rainstorms were common and devastating. Jesus's audience would have witnessed firsthand the difference between structures built on bedrock versus those on soil or sand.",
    "questions": [
        "What does 'digging deep' look like practically in your spiritual life—what comfort or convenience might you need to excavate to reach the Rock?",
        "How do you measure spiritual maturity: by external appearances (the house) or by tested stability (the foundation)?",
        "In what ways might you be trusting your own religious effort rather than resting wholly on Christ as your foundation?"
    ]
}

commentary['6']['49'] = {
    "analysis": "<strong>But he that heareth, and doeth not</strong> (ὁ δὲ ἀκούσας καὶ μὴ ποιήσας)—The aorist participles emphasize decisive hearing followed by decisive non-doing. This isn't ignorance but willful disobedience—hearing Jesus's words without implementing them. James later warns against being 'hearers only, deceiving your own selves' (James 1:22).<br><br><strong>Without a foundation built an house upon the earth</strong> (ᾠκοδόμησεν οἰκίαν ἐπὶ τὴν γῆν χωρὶς θεμελίου)—the preposition <em>epi</em> (upon) contrasts with the previous verse's foundation <em>epi petra</em> (upon rock). Building 'upon the earth' suggests surface-level construction, expedient but catastrophically inadequate. <strong>Immediately it fell; and the ruin of that house was great</strong> (εὐθέως ἔπεσεν, καὶ ἐγένετο τὸ ῥῆγμα τῆς οἰκίας ἐκείνης μέγα)—the dramatic collapse (<em>rhēgma</em>, breach, ruin) illustrates eschatological judgment. Profession without practice ends in 'great' ruin, echoing Jesus's warning about those who prophesied and cast out demons in his name yet are condemned as workers of iniquity (Matthew 7:21-23).",
    "historical": "Luke wrote to a largely Gentile audience facing pressure to compromise Christian ethics for social acceptance. This parable warned against cultural accommodation—maintaining Christian profession while abandoning Christian practice. The 'great ruin' anticipates final judgment when false professors face eternal consequences for superficial faith.",
    "questions": [
        "What teachings of Jesus do you 'hear' regularly but consistently fail to implement—what's your area of willful disobedience?",
        "How might cultural Christianity (religious identity without transformed behavior) represent building without a foundation in modern contexts?",
        "Does the warning of 'great ruin' affect how urgently you pursue obedience, or have you grown desensitized to biblical warnings of judgment?"
    ]
}

# Luke 8:51-56 - Raising Jairus's Daughter
commentary['8']['51'] = {
    "analysis": "<strong>And when he came into the house, he suffered no man to go in, save Peter, and James, and John</strong> (ἐλθὼν δὲ εἰς τὴν οἰκίαν οὐκ ἀφῆκεν εἰσελθεῖν τινα σὺν αὐτῷ εἰ μὴ Πέτρον καὶ Ἰωάννην καὶ Ἰάκωβον)—Jesus deliberately limits the witnesses to his 'inner circle,' the same three who will witness the Transfiguration (9:28) and Gethsemane agony (Mark 14:33). The verb <em>aphiēmi</em> (suffered, permitted) indicates Jesus's sovereign control over who observes this miracle.<br><br>This selective disclosure reveals Jesus's pedagogical wisdom—some revelations of divine power require spiritual maturity to properly interpret. <strong>And the father and the mother of the maiden</strong>—Luke's medical precision (he includes details about Jairus and his wife) reflects his attention to human dimensions of the narrative. The parents' inclusion ensures credible testimony to their daughter's actual death and subsequent resurrection.",
    "historical": "In first-century Jewish mourning customs, the entire community would gather at a death, with professional mourners (often women) hired to wail and play flutes. Jesus's restriction of the crowd to just five witnesses (the three disciples plus two parents) was highly unusual and would have been considered socially inappropriate, demonstrating his authority over social conventions when divine purposes required privacy.",
    "questions": [
        "Why might Jesus limit witnesses to his most powerful miracles—what spiritual principle about revelation and readiness does this illustrate?",
        "How do you respond when God works in 'private' ways that cannot be publicly validated or vindicated to skeptics?",
        "What might it mean for your spiritual formation that Jesus reveals different aspects of himself to different people at different times?"
    ]
}

commentary['8']['52'] = {
    "analysis": "<strong>And all wept, and bewailed her</strong> (ἔκλαιον δὲ πάντες καὶ ἐκόπτοντο αὐτήν)—the imperfect tense indicates ongoing weeping and loud lamentation. The verb <em>koptō</em> (bewailed) literally means 'to beat' (the breast in mourning), describing the demonstrative grief displays common in ancient Near Eastern death rituals. <strong>But he said, Weep not; she is not dead, but sleepeth</strong> (μὴ κλαίετε· οὐ γὰρ ἀπέθανεν ἀλλὰ καθεύδει)—Jesus's present imperative <em>klaiete</em> commands them to stop their weeping immediately.<br><br>The statement <strong>she is not dead, but sleepeth</strong> doesn't deny biological death (Luke explicitly states in v.55 that 'her spirit came again') but reframes death from the perspective of Jesus's resurrection power. For Christ, death is temporary sleep because he possesses authority to awaken the dead. This anticipates his declaration at Lazarus's tomb: 'Our friend Lazarus sleepeth; but I go, that I may awake him out of sleep' (John 11:11). Paul later uses this same sleep metaphor for believers who have died (1 Thessalonians 4:13-14).",
    "historical": "First-century mourning practices were immediate and intense—bodies were buried within 24 hours due to climate, and mourning began instantly upon death. The presence of mourners confirmed the finality of death in the community's eyes, making their ridicule of Jesus (v.53) a public attestation that the girl was genuinely deceased, not merely unconscious or in a coma.",
    "questions": [
        "How does Jesus's reframing of death as 'sleep' transform Christian perspectives on mortality and grief?",
        "In what current 'dead' situations (relationships, ministries, hopes) might you need to hear Jesus say, 'She is not dead, but sleepeth'?",
        "What does this passage teach about the difference between human perspective ('dead') and divine perspective ('sleeping')?"
    ]
}

commentary['8']['53'] = {
    "analysis": "<strong>And they laughed him to scorn, knowing that she was dead</strong> (καὶ κατεγέλων αὐτοῦ, εἰδότες ὅτι ἀπέθανεν)—the compound verb <em>katagelao</em> indicates contemptuous ridicule, not polite disagreement. The participle <em>eidotes</em> (knowing) emphasizes their certainty—these mourners had verified the death and now mocked Jesus's statement as delusional or blasphemous. This scorn parallels the ridicule Jesus will face at the cross ('He saved others; himself he cannot save,' Matthew 27:42).<br><br>The mourners' certainty about death's finality represents human wisdom confronting divine power. Their laughter reveals the natural mind's inability to comprehend resurrection—'the natural man receiveth not the things of the Spirit of God: for they are foolishness unto him' (1 Corinthians 2:14). Yet their mockery inadvertently confirms the miracle's authenticity: skeptical witnesses testify that death was genuine, making the subsequent resurrection irrefutable.",
    "historical": "Luke, writing as a physician, would have understood death verification practices in the ancient world. The presence of professional mourners served as a form of death certification—they were hired precisely because death had been confirmed. Their ridicule of Jesus demonstrates that the girl's death was publicly acknowledged and medically certain, eliminating later claims that she was merely comatose.",
    "questions": [
        "How do you respond when your faith declarations about God's power to resurrect dead situations are met with scorn or ridicule?",
        "Why might God allow skeptics and mockers to witness his miraculous works—what purpose does their testimony serve?",
        "In what ways does the world's 'certainty' about impossibility (death's finality) blind it to God's resurrection power?"
    ]
}

commentary['8']['54'] = {
    "analysis": "<strong>And he put them all out</strong> (αὐτὸς δὲ ἐκβαλὼν ἔξω πάντας)—the forceful verb <em>ekballō</em> (cast out, expel) indicates Jesus physically removed the scoffers. Unbelief disqualifies people from witnessing divine power; mockery forfeits the privilege of observing miracles. This expulsion anticipates Jesus's teaching that 'the kingdom of God shall be taken from you, and given to a nation bringing forth the fruits thereof' (Matthew 21:43).<br><br><strong>And took her by the hand, and called, saying, Maid, arise</strong> (κρατήσας τῆς χειρὸς αὐτῆς ἐφώνησεν λέγων· Ἡ παῖς, ἔγειρε)—Jesus's physical touch (the verb <em>krateō</em> means 'to grasp firmly') would render him ceremonially unclean under Levitical law (Numbers 19:11-22), yet divine authority transcends ritual purity regulations. The word <em>pais</em> (maid, child) is tender, and <em>egeirō</em> (arise) is the same verb used of Jesus's own resurrection—he commands death to release its victim as one having authority over the grave itself.",
    "historical": "Touching a corpse incurred seven days of uncleanness in Jewish law, requiring purification rituals. Jesus's willingness to touch the dead girl demonstrated that his purity was not passive (defiled by contact with impurity) but active (transmitting life and cleansing). This foreshadows the gospel principle that Christ's righteousness is not corrupted by contact with sinners but rather transforms them.",
    "questions": [
        "Why does unbelief disqualify people from witnessing miracles—what does this teach about the relationship between faith and revelation?",
        "How does Jesus's touch of the dead girl challenge religious systems that emphasize separation from 'unclean' people or situations?",
        "What 'dead' areas of your life need Jesus's personal touch and the command 'Arise'?"
    ]
}

commentary['8']['55'] = {
    "analysis": "<strong>And her spirit came again</strong> (καὶ ἐπέστρεψεν τὸ πνεῦμα αὐτῆς)—Luke's medical vocabulary is precise: the verb <em>epistrephō</em> (returned, came back) confirms that her <em>pneuma</em> (spirit) had departed, validating her actual death. This verse refutes natural explanations (coma, catalepsy) and affirms bodily resurrection—spirit reunited with body. Luke's anthropology distinguishes spirit from body, anticipating Christian teaching about intermediate state and bodily resurrection.<br><br><strong>And she arose straightway</strong> (καὶ ἀνέστη παραχρῆμα)—the adverb <em>parachrēma</em> emphasizes the instantaneous nature of the miracle. No gradual recovery, no convalescence—immediate restoration of life and vitality. <strong>And he commanded to give her meat</strong> (καὶ διέταξεν αὐτῇ δοθῆναι φαγεῖν)—Jesus's practical concern that she be fed demonstrates the <em>physicality</em> of resurrection (not a ghost or vision) and his pastoral care for human needs. This detail anticipates the post-resurrection Jesus eating fish with his disciples to prove his bodily resurrection (Luke 24:41-43).",
    "historical": "In Jewish anthropology, the spirit departing confirmed death, and its return meant resurrection—not resuscitation. Luke's emphasis on the spirit's return and the girl's immediate eating served apologetic purposes for his Gentile audience, many of whom were influenced by Greek dualism that denied bodily resurrection. This miracle validates Jewish-Christian resurrection hope against Hellenistic skepticism.",
    "questions": [
        "How does the detail about 'her spirit came again' affirm both the reality of death and the truth of bodily resurrection?",
        "What does Jesus's command to feed the girl teach about the integration of spiritual and physical needs in Christian ministry?",
        "In what ways does this resurrection miracle point forward to Jesus's own resurrection and the believer's future resurrection?"
    ]
}

commentary['8']['56'] = {
    "analysis": "<strong>And her parents were astonished</strong> (καὶ ἐξέστησαν οἱ γονεῖς αὐτῆς)—the verb <em>existēmi</em> (astonished, amazed) literally means 'to stand outside oneself,' indicating overwhelming shock. Even Jairus, who demonstrated faith by seeking Jesus (v.41), is stunned by the actualization of resurrection. Faith believes for the miracle, but witnessing it exceeds comprehension.<br><br><strong>But he charged them that they should tell no man what was done</strong> (ὁ δὲ παρήγγειλεν αὐτοῖς μηδενὶ εἰπεῖν τὸ γεγονός)—Jesus's command to silence (<em>parangellō</em>, to command strictly) seems paradoxical given the publicity of the miracle. This 'messianic secret' motif in Luke reflects Jesus's strategic management of his reputation—premature political messianism could derail his mission. He came to die as the suffering servant before being revealed as conquering king. The resurrection miracle must not trigger popular revolt or forced coronation before Jerusalem and the cross. Yet the command proves impossible to fully obey—the girl's resurrection would be evident to all who knew of her death.",
    "historical": "In first-century Galilee, messianic expectations were politically charged—many anticipated a military deliverer to overthrow Rome. Powerful miracles like raising the dead could catalyze insurrection. Jesus's silencing commands throughout Luke's Gospel reflect his deliberate avoidance of political messianism until the proper time. He would enter Jerusalem as king (19:38), but only after teaching his disciples the necessity of the cross.",
    "questions": [
        "Why might authentic miracles sometimes need to be held in confidence rather than immediately publicized—what does this teach about wisdom in testimony?",
        "How do you process the tension between amazing answers to prayer (astonishment) and continued trust in God's character?",
        "In what ways might premature publicity of God's work derail his larger purposes in your life or ministry?"
    ]
}

# Save progress
data['commentary'] = commentary

with open('kjvstudy_org/data/verse_commentary/luke.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Generated Luke 6:47-49 and 8:51-56 (9 verses)")
