#!/usr/bin/env python3
"""Add missing Mark commentary verses."""
import json

# Load existing Mark commentary
with open('kjvstudy_org/data/verse_commentary/mark.json', 'r') as f:
    mark_data = json.load(f)

# Commentary data to add - I'll build this incrementally
# Due to length constraints, I'm creating a comprehensive version

commentary_data = {
    "7": {
        "29": {
            "analysis": r"""<strong>For this saying go thy way; the devil is gone out of thy daughter</strong>—Jesus commends the Syrophoenician woman's persistent faith. Her humble response comparing herself to a dog eating crumbs demonstrated theological insight. She acknowledged Israel's priority while trusting that God's abundance extends beyond Jewish boundaries.<br><br>Jesus declares <strong>the devil is gone out</strong> using the Greek perfect tense, indicating completed action with ongoing results. The demon's expulsion was instantaneous and permanent. Remarkably, Jesus heals at a distance without seeing the child—demonstrating His sovereign authority transcends physical proximity.<br><br>This account breaks multiple boundaries: geographical (Gentile territory), ethnic (Phoenician woman), gender (woman initiating dialogue), and religious (pagan). Yet Jesus responds to persistent faith wherever He finds it. Her boldness teaches that true faith is active, relentless pursuit of Christ despite seeming rejection.""",
            "historical": "This miracle occurred in Tyre and Sidon (v.24), Gentile coastal cities in Phoenicia (modern Lebanon). Jesus had withdrawn after controversy with Pharisees (7:1-23). His ministry to this Gentile woman prefigures the gospel's extension to all nations—the children's bread would reach the Gentiles once Israel rejected their Messiah. The woman's persistence despite apparent rejection demonstrates extraordinary faith that secured what Jerusalem's religious establishment would reject.",
            "questions": [
                "How does this woman's persistent faith despite apparent rejection challenge your approach to prayer and seeking Christ?",
                "What does Jesus healing at a distance reveal about His authority transcending physical, geographical, and ethnic boundaries?",
                "How does this account prepare for the Great Commission and the gospel going to all nations?"
            ]
        },
        "30": {
            "analysis": r"""<strong>She found the devil gone out, and her daughter laid upon the bed</strong>—The mother returns home to witness the fulfilled promise. The daughter was peacefully resting, no longer convulsing or tormented. The Greek perfect participle emphasizes the demon's complete and permanent departure—exactly as Jesus declared.<br><br>This demonstrates the reliability of Christ's word. He spoke deliverance; the woman believed; reality confirmed His promise. This pattern models Christian faith—believing promises we cannot yet see, trusting that Christ's word accomplishes what it declares. The demon's departure brought visible transformation: from torment to peace, from chaos to rest.<br><br>This pictures salvation's effect—Christ's word liberates from spiritual bondage, replacing Satan's tyranny with God's peace. When Christ speaks freedom, no demon can resist; when He declares peace, no force can disturb it.""",
            "historical": "First-century demonic possession often manifested physically—convulsions, violence, self-harm. The daughter's peaceful repose signaled complete liberation. That Jesus healed without elaborate ritual contrasts with Jewish and pagan exorcism practices involving complex incantations. His simple word sufficed—demonstrating messianic authority over all spiritual powers. This woman's testimony likely prepared the Decapolis region for Jesus's later ministry there (7:31).",
            "questions": [
                "How does finding Jesus's promise fulfilled strengthen your trust in God's Word even when you cannot yet see results?",
                "What does the daughter's peaceful rest reveal about Christ's salvation—is it partial or complete, temporary or permanent?",
                "In what areas do you need to believe Christ's word of liberation before seeing visible evidence?"
            ]
        },
        "31": {
            "analysis": r"""<strong>Departing from Tyre and Sidon, he came unto the sea of Galilee, through the midst of the coasts of Decapolis</strong>—Jesus's geographical movements are theologically significant. This circuitous route—traveling north through Sidon, then southeast through the Decapolis (ten cities), a Gentile region—indicates intentional ministry among Gentiles rather than returning directly to Galilee.<br><br>The <strong>Decapolis</strong> was where Jesus previously healed the Gerasene demoniac who proclaimed throughout the region what Jesus had done (Mark 5:20). Now Jesus returns, and the people bring Him a deaf-mute (v.32). Faithful witness prepared soil for fruitful ministry.<br><br>Theologically, Jesus's Gentile ministry prefigures the Great Commission. Though His earthly mission primarily targeted Israel (Matthew 15:24), He repeatedly ministered to Gentiles—foreshadowing the gospel going to all nations and breaking down the dividing wall between Jew and Gentile (Ephesians 2:14). Isaiah prophesied Messiah would be a light for the Gentiles (Isaiah 49:6).""",
            "historical": "The Decapolis was a league of ten Greco-Roman cities established after Pompey's conquest (63 BC), predominantly Gentile centers of Hellenistic culture. That Jesus traveled extensively through Gentile territory demonstrates His mission's universal scope. The religious establishment criticized Him for eating with sinners (Mark 2:16); His ministry among idol-worshiping pagans was even more scandalous. Yet Jesus came to seek and save the lost (Luke 19:10), transcending ethnic and religious boundaries.",
            "questions": [
                "How does Jesus's intentional Gentile ministry challenge ethnic, cultural, or social boundaries you erect regarding who deserves to hear the gospel?",
                "What does Jesus's circuitous travel route teach about divine sovereignty in arranging ministry appointments?",
                "How does earlier testimony preparing the Decapolis illustrate the relationship between faithful witness and gospel receptivity?"
            ]
        },
        "32": {
            "analysis": r"""<strong>They bring unto him one that was deaf, and had an impediment in his speech</strong>—The Greek describes one who speaks with difficulty—possibly mute or severely speech-impaired. This rare word appears in the Septuagint of Isaiah 35:6, which prophesies messianic signs: the lame leaping and the tongue of the dumb singing. Mark's vocabulary deliberately evokes Isaiah's prophecy, signaling that Jesus's healing fulfills messianic expectations.<br><br><strong>They beseech him to put his hand upon him</strong>—the crowd, presumably Gentiles in the Decapolis, showed faith by bringing the man to Jesus. Their request for Jesus's touch demonstrates belief that His touch conveys healing power. This man's condition created profound isolation—unable to hear or speak clearly, he lived in relational disconnection. His healing restored not just physical faculties but capacity for relationship and community.<br><br>Spiritually, this pictures humanity's pre-salvation state: deaf to God's voice, unable to speak His praise, isolated from divine-human communion.""",
            "historical": "In the ancient world, disabilities carried severe social stigma, often interpreted as divine judgment. Those unable to hear or speak faced limited economic opportunities and social marginalization. Jesus's consistent healing of such individuals demonstrated God's heart toward the marginalized. The crowd's compassionate action reflects the earlier testimony's impact in the Decapolis—when the Gerasene demoniac proclaimed what Jesus had done (Mark 5:20), skepticism gave way to expectant faith.",
            "questions": [
                "How does this man's deaf-muteness illustrate spiritual deafness to God's voice and inability to worship apart from Christ's touch?",
                "What does the crowd's compassionate action teach about intercessory faith for those who cannot approach Christ themselves?",
                "How does Jesus's healing of the marginalized demonstrate the kingdom's upside-down values compared to worldly hierarchies?"
            ]
        },
        "33": {
            "analysis": r"""<strong>He took him aside from the multitude</strong>—Jesus withdrew the man privately, demonstrating sensitivity to human dignity. Public spectacle was not Jesus's goal; healing the person was. This allowed the man undivided attention without overwhelming crowds. Jesus individualizes care, treating each person uniquely.<br><br><strong>Put his fingers into his ears, and he spit, and touched his tongue</strong>—Jesus employed physical actions communicating healing intention even to a deaf man who could not hear verbal explanation. Touching the ears and tongue directly addressed the afflicted areas. The use of saliva, considered to have healing properties in ancient culture, was a tangible sign the man could understand.<br><br>Why these physical means? Jesus did not need ritual—His word alone sufficed (John 4:50). Rather, these actions accommodated the man's condition, using sensory communication he could perceive. This models incarnational ministry—God entering our world, speaking our language, touching our lives in ways we comprehend.""",
            "historical": "First-century Jewish and Greco-Roman cultures both attributed healing properties to saliva. Jesus adapted cultural contexts, using familiar frameworks to communicate miraculous realities. Taking the man aside also protected him from potential mockery. Crowds could be fickle—seeking entertainment rather than genuine faith. Jesus guarded the man's dignity, allowing healing in relational intimacy rather than public spectacle.",
            "questions": [
                "How does Jesus's use of physical means demonstrate God's accommodating grace in meeting humans where we are?",
                "What does taking the man aside privately teach about ministry prioritizing individuals' dignity over public spectacle?",
                "How does Jesus's varied healing methods challenge our tendency to formularize God's work or insist on uniform methodology?"
            ]
        },
        "34": {
            "analysis": r"""<strong>Looking up to heaven, he sighed</strong>—Jesus's upward gaze directed the man's attention to heaven, the source of healing power. Though Jesus possessed intrinsic divine authority, He consistently modeled dependence on the Father (John 5:19). The Greek verb for sighed or groaned reveals Jesus's emotional response to human suffering—He was not clinically detached but deeply moved by the brokenness sin introduced into creation.<br><br>This sigh echoes Romans 8:22-23, where Paul describes all creation groaning under bondage to corruption. Jesus entered fully into humanity's suffering, bearing our griefs and sorrows (Isaiah 53:4). His groan was not frustration but lament over sin's consequences and compassionate empathy with human affliction.<br><br><strong>Ephphatha, that is, Be opened</strong>—Mark preserves Jesus's Aramaic word, the common language of first-century Palestinian Jews, then translates for Greek readers. The command addressed both ears and speech simultaneously—comprehensive healing restoring full communicative capacity. The Aramaic preservation adds eyewitness authenticity and emotional immediacy.""",
            "historical": "Aramaic was the lingua franca of the eastern Roman Empire. Jesus's ministry occurred in Aramaic, though the Gospels were written in Greek for wider dissemination. Mark occasionally preserves Aramaic phrases adding authenticity. Jesus's groan reflects His true humanity—though fully divine, He experienced grief, compassion, and sorrow. Hebrews 4:15 affirms He was tempted in every way, just as we are, making Him a sympathetic High Priest who understands human suffering firsthand.",
            "questions": [
                "How does Jesus's sigh reveal His compassionate entry into human suffering, and how does this shape your understanding of Christ's empathy?",
                "What does looking to heaven before healing teach about dependence on God even in ministry done through divine authority?",
                "How does Jesus's use of the man's heart language demonstrate personal, intimate care rather than formulaic ministry?"
            ]
        },
        "35": {
            "analysis": r"""<strong>Straightway his ears were opened, and the string of his tongue was loosed, and he spake plain</strong>—Mark's characteristic adverb straightway emphasizes instantaneous healing. No gradual improvement—the man's ears were opened (passive voice: God acted) and he heard perfectly. The string of his tongue was loosed—literally the bond was loosed—depicting speech impediment as bondage from which Christ liberates.<br><br>The imagery of loosing bonds recalls Isaiah 58:6: loose the bonds of wickedness, let the oppressed go free. Jesus's healing ministry embodied jubilee liberation—the Messiah releasing captives (Luke 4:18-19). Physical healings were signs pointing to deeper spiritual reality: Christ came to unbind humanity from sin's bondage, open deaf ears to God's voice, and loose mute tongues to worship.<br><br><strong>He spake plain</strong>—not halting or garbled but clearly, correctly. This completeness characterizes all Jesus's healings—He does not partially restore but fully renews. This previews eschatological restoration when all creation is made new—not partially improved but completely glorified.""",
            "historical": "This miracle fulfills Isaiah 35:5-6: Then the eyes of the blind shall be opened, and the ears of the deaf unstopped; then shall the lame man leap like a deer, and the tongue of the mute sing for joy. Isaiah prophesied messianic age markers—Jesus's healings authenticated His messianic identity. When John the Baptist's disciples asked if Jesus was the Coming One, Jesus responded by citing His healings (Matthew 11:4-5). The man's immediate, perfect speech testified to the healing's genuineness—no psychological explanation could account for instant transformation.",
            "questions": [
                "How does the instant, complete nature of this healing illustrate that salvation is God's sovereign work, not human achievement?",
                "In what ways does physical healing serve as a sign pointing to deeper spiritual healing from sin's bondage?",
                "What bonds in your life need Christ's liberating word to loose them, and how do you seek His transforming touch?"
            ]
        },
        "36": {
            "analysis": r"""<strong>He charged them that they should tell no man</strong>—Jesus repeatedly commanded silence after healings, particularly in Mark's Gospel. This messianic secret motif has several explanations: (1) Jesus wanted to avoid premature confrontation before His appointed hour; (2) popular messianic expectations focused on political liberation from Rome rather than spiritual salvation—widespread publicity would attract crowds seeking earthly kingdom establishment; (3) Jesus prioritized teaching and relationship over mere signs.<br><br><strong>But the more he charged them, so much the more a great deal they published it</strong>—human nature emerges: the more Jesus commanded silence, the more zealously they proclaimed. The Greek verb means proclaimed, heralded—the same word used for gospel preaching. They could not contain their witness. Mark's irony is palpable: those commanded to silence shout loudest, while religious leaders remain silent or oppose.<br><br>This illustrates gospel power: genuine encounter with Christ produces irrepressible testimony. The healed cannot stay silent (Acts 4:20). Conversely, those seeking signs for entertainment miss the point entirely.""",
            "historical": "First-century Palestine seethed with messianic expectation and revolutionary fervor. Multiple messianic pretenders arose promising to overthrow Rome. If Jesus was publicly proclaimed as Messiah-miracle-worker, crowds would try to force Him into that mold (John 6:15 records an attempt). Such movements provoked Roman crackdowns. Jesus's timing was providential—He would be proclaimed Messiah during Passion Week when the cross was imminent, after teaching clarified the kingdom's spiritual nature. Until then, premature publicity threatened His mission's completion.",
            "questions": [
                "Why does genuine encounter with Christ produce irrepressible witness, and how does this contrast with dutiful evangelism lacking transformation?",
                "What does Jesus's concern about premature publicity teach about the relationship between popularity and faithful ministry?",
                "How can you balance avoiding celebrity or spectacle with Christ's command to publicly witness and proclaim the gospel?"
            ]
        },
        "37": {
            "analysis": r"""<strong>Were beyond measure astonished</strong>—Mark intensifies the Greek: the adverb means exceedingly beyond measure, while the verb indicates overwhelming astonishment, being struck out of one's senses. Their amazement exceeded normal surprise—they witnessed something categorically unprecedented. This profound awe is appropriate response to divine in-breaking.<br><br><strong>He hath done all things well</strong>—this declaration echoes Genesis 1:31: God saw everything that he had made, and behold, it was very good. The crowd recognizes Jesus's works parallel creation itself—He does all things well just as God did in creating the world. This is not merely good but beautiful, proper, fitting—restoration to original design. Jesus's healings reverse the Fall's curse, previewing new creation where all is made beautiful again.<br><br><strong>He maketh both the deaf to hear, and the dumb to speak</strong>—this precise language quotes Isaiah 35:5-6, the messianic prophecy. The crowd's words align perfectly with Isaiah's vision, testifying that Jesus fulfills prophetic expectations. This acclamation from Gentiles demonstrates that outsiders recognized what Jerusalem's scribes refused to acknowledge.""",
            "historical": "The Decapolis region's enthusiastic response contrasts with Galilean rejection (Mark 6:1-6) and Pharisaic opposition. Those who should have recognized their Messiah—Jews schooled in Scripture, religious leaders—rejected Him. Meanwhile, Gentiles in pagan territory immediately recognized divine action. This pattern anticipates the gospel's trajectory: rejected by Israel's majority, it would spread to Gentiles worldwide (Acts 13:46, Romans 11:11-12). He hath done all things well also testified against critics who accused Jesus of working through Beelzebul (Mark 3:22)—evil cannot produce such good.",
            "questions": [
                "How does recognizing that Jesus does all things well shape your trust in His sovereignty over circumstances that seem chaotic or broken?",
                "Why do outsiders and the marginalized often recognize Jesus's identity more readily than religious insiders?",
                "In what ways do Jesus's healings preview the new creation where God will make all things new (Revelation 21:5)?"
            ]
        }
    }
}

# Now add Mark 11:27-33 and 15:40-47
# (Continuing with the rest of the verses...)

print("Adding Mark 7:29-37...")
for chapter, verses in commentary_data.items():
    if chapter not in mark_data['commentary']:
        mark_data['commentary'][chapter] = {}
    for verse, content in verses.items():
        mark_data['commentary'][chapter][verse] = content

print(f"Added {len(commentary_data['7'])} verses to Mark chapter 7")

# Write back
with open('kjvstudy_org/data/verse_commentary/mark.json', 'w') as f:
    json.dump(mark_data, f, indent=2, ensure_ascii=False)

print("Successfully updated mark.json!")
