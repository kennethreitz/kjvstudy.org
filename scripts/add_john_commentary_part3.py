#!/usr/bin/env python3
"""Add John commentary - Part 3: Chapter 19 (final 12 verses)."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "kjvstudy_org" / "data" / "verse_commentary"

filepath = DATA_DIR / "john.json"
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

commentary = data.get("commentary", {})

# John commentary - Part 3: Chapter 19
new_entries = {
    "19": {
        "31": {
            "analysis": "<strong>The Jews therefore, because it was the preparation, that the bodies should not remain upon the cross on the sabbath day, (for that sabbath day was an high day,)</strong> (Οἱ οὖν Ἰουδαῖοι, ἐπεὶ παρασκευὴ ἦν, ἵνα μὴ μείνῃ ἐπὶ τοῦ σταυροῦ τὰ σώματα ἐν τῷ σαββάτῳ, ἦν γὰρ μεγάλη ἡ ἡμέρα ἐκείνου τοῦ σαββάτου, <em>Hoi oun Ioudaioi, epei paraskeuē ēn, hina mē meinē epi tou staurou ta sōmata en tō sabbatō, ēn gar megalē hē hēmera ekeinou tou sabbatou</em>)—Jewish law forbade leaving bodies on crosses overnight (Deuteronomy 21:23), especially before a Sabbath. This was ἡ παρασκευή (<em>hē paraskeuē</em>, 'the Preparation'), Friday before Sabbath. Moreover, ἦν γὰρ μεγάλη ἡ ἡμέρα (<em>ēn gar megalē hē hēmera</em>, 'it was a high day')—Passover Sabbath coinciding with weekly Sabbath. <strong>Besought Pilate that their legs might be broken, and that they might be taken away</strong>—<em>crurifragium</em> (breaking legs) hastened death by preventing victims from pushing up to breathe, causing rapid asphyxiation.<br><br>The irony is brutal: religious leaders who orchestrated Jesus's execution now concern themselves with ritual purity, wanting bodies removed before Sabbath. They strain at gnats while swallowing camels (Matthew 23:24)—meticulous about ceremonial law while murdering the Messiah. This exposes how religion without heart can coexist with horrific evil.",
            "historical": "Roman crucifixion normally left bodies to rot as deterrent, but Romans accommodated Jewish sensibilities in Judea. Archaeological evidence from first-century Jerusalem (Yehohanan ben Hagkol, discovered 1968) confirms crucifixion practices and leg-breaking. Passover Sabbath (15 Nisan) was especially sacred, making this a 'high' Sabbath.",
            "questions": [
                "How does concern for ritual purity while orchestrating murder demonstrate the danger of external religion without heart transformation?",
                "What modern forms of 'straining at gnats while swallowing camels' do religious people practice today?",
                "How should Christians guard against prioritizing religious observance over justice, mercy, and faithfulness?"
            ]
        },
        "32": {
            "analysis": "<strong>Then came the soldiers, and brake the legs of the first, and of the other which was crucified with him</strong> (ἦλθον οὖν οἱ στρατιῶται καὶ τοῦ μὲν πρώτου κατέαξαν τὰ σκέλη καὶ τοῦ ἄλλου τοῦ συσταυρωθέντος αὐτῷ, <em>ēlthon oun hoi stratiōtai kai tou men prōtou kateaxan ta skelē kai tou allou tou systaurōthentos autō</em>)—The Roman soldiers systematically broke the legs (κατέαξαν τὰ σκέλη, <em>kateaxan ta skelē</em>) of both thieves crucified with Jesus. The verb κατάγνυμι (<em>katagnymi</em>) means to 'break in pieces, shatter.' This brutal act fulfilled its purpose: hastening death through respiratory failure when victims could no longer lift themselves to exhale.<br><br>These two criminals—one who repented (Luke 23:40-43), one who blasphemed (Luke 23:39)—represent humanity's response to Christ. Both witnessed His innocence, heard His prayer for His executioners, experienced His presence in suffering. One found paradise; one died in his sins. Proximity to Jesus doesn't save; faith does.",
            "historical": "Luke records the 'penitent thief' dialogue (Luke 23:39-43), showing one thief's deathbed conversion. Crucifixion victims typically survived 24-72 hours; breaking legs reduced this to minutes. The soldiers' efficiency in breaking both thieves' legs highlights the exception made for Jesus (verse 33).",
            "questions": [
                "How do the two thieves illustrate the two possible responses to Christ—rejection or repentance?",
                "What does the penitent thief's immediate salvation teach about grace, faith, and the sufficiency of Christ's sacrifice?",
                "Why is proximity to Christ or Christian environments insufficient for salvation without personal faith?"
            ]
        },
        "33": {
            "analysis": "<strong>But when they came to Jesus, and saw that he was dead already, they brake not his legs</strong> (ἐπὶ δὲ τὸν Ἰησοῦν ἐλθόντες, ὡς εἶδον ἤδη αὐτὸν τεθνηκότα, οὐ κατέαξαν αὐτοῦ τὰ σκέλη, <em>epi de ton Iēsoun elthontes, hōs eidon ēdē auton tethnēkota, ou kateaxan autou ta skelē</em>)—The soldiers' observation (εἶδον, <em>eidon</em>, 'they saw') that Jesus was τεθνηκότα (<em>tethnēkota</em>, 'already dead') prevented them from breaking His legs. This was unexpected; crucifixion victims rarely died within six hours (Jesus was crucified at 9am and died at 3pm, Mark 15:25, 34). His rapid death may have resulted from the physical trauma of scourging, emotional agony in Gethsemane (Luke 22:44), and voluntarily yielding His spirit (John 19:30).<br><br>Providence guided this seemingly random military decision. The soldiers had no theological knowledge, yet their pragmatic choice fulfilled prophecy (Exodus 12:46; Numbers 9:12; Psalm 34:20)—the Paschal Lamb's bones remained unbroken. God sovereignly orchestrates even minute details to accomplish His redemptive purposes.",
            "historical": "Roman soldiers were experienced executioners who could determine death reliably. Jesus's unusually rapid death surprised even Pilate (Mark 15:44). Medical theories suggest cardiac rupture, hemopericardium, or hypovolemic shock from scourging and crucifixion. Regardless of physiological mechanism, Jesus voluntarily dismissed His spirit (John 10:18).",
            "questions": [
                "How does Jesus's rapid, voluntary death demonstrate His sovereign control even during crucifixion?",
                "What does the fulfillment of detailed prophecy about unbroken bones teach about Scripture's inspiration and God's sovereign control?",
                "How should believers trust God's providence when circumstances seem random or meaningless?"
            ]
        },
        "34": {
            "analysis": "<strong>But one of the soldiers with a spear pierced his side, and forthwith came there out blood and water</strong> (ἀλλ' εἷς τῶν στρατιωτῶν λόγχῃ αὐτοῦ τὴν πλευρὰν ἔνυξεν, καὶ ἐξῆλθεν εὐθὺς αἷμα καὶ ὕδωρ, <em>all' heis tōn stratiōtōn lonchē autou tēn pleuran enyxen, kai exēlthen euthys haima kai hydōr</em>)—To confirm death, a soldier thrust a λόγχη (<em>lonchē</em>, 'lance, spear') into Jesus's πλευράν (<em>pleuran</em>, 'side'), producing αἷμα καὶ ὕδωρ (<em>haima kai hydōr</em>, 'blood and water'). Medical explanations include: pericardial effusion, pleural effusion, or separated blood clot and serum. John emphasizes εὐθὺς (<em>euthys</em>, 'immediately'), stressing the eyewitness detail.<br><br>Theologically, blood and water symbolize atonement and cleansing. 1 John 5:6 references this: 'This is he that came by water and blood, even Jesus Christ.' The water may symbolize the Spirit (John 7:38-39), baptism, or sanctification. The blood represents the new covenant (Matthew 26:28). Together they encompass full salvation: justification (blood) and sanctification (water).",
            "historical": "Roman spears typically penetrated 5-6 inches. Striking the right side would pierce the right atrium or ventricle, releasing blood; the pericardial sac would release serous fluid. John's precise medical observation has led many physicians throughout history to faith, recognizing authentic eyewitness detail rather than legendary embellishment.",
            "questions": [
                "How does the medical detail of 'blood and water' validate the Gospel's historical reliability as eyewitness testimony?",
                "What theological significance do blood and water carry—how do they represent full salvation?",
                "How should the physical reality of Christ's death and suffering shape our understanding of atonement?"
            ]
        },
        "35": {
            "analysis": "<strong>And he that saw it bare record, and his record is true: and he knoweth that he saith true, that ye might believe</strong> (καὶ ὁ ἑωρακὼς μεμαρτύρηκεν, καὶ ἀληθινὴ αὐτοῦ ἐστιν ἡ μαρτυρία, καὶ ἐκεῖνος οἶδεν ὅτι ἀληθῆ λέγει, ἵνα καὶ ὑμεῖς πιστεύσητε, <em>kai ho heōrakōs memartyrēken, kai alēthinē autou estin hē martyria, kai ekeinos oiden hoti alēthē legei, hina kai hymeis pisteusēte</em>)—John solemnly testifies to eyewitness observation. ὁ ἑωρακώς (<em>ho heōrakōs</em>, 'the one who saw') is emphatic. μεμαρτύρηκεν (<em>memartyrēken</em>, 'has testified') is perfect tense—past action with continuing results. His testimony is ἀληθινὴ (<em>alēthinē</em>, 'true, genuine, reliable'). The purpose clause ἵνα...πιστεύσητε (<em>hina...pisteusēte</em>, 'in order that you might believe') reveals John's evangelical intent—recording historical facts to produce faith.<br><br>This verse establishes the evidential basis of Christian faith. John doesn't ask readers to believe myths or legends but documented historical events witnessed by credible observers. Faith rests on facts, not blind credulity. The Apostle's integrity—willingness to die for testimony he knew to be either true or false—validates his credibility.",
            "historical": "John likely wrote his Gospel around 85-95 AD, as the last surviving apostle. His emphatic eyewitness claim counters emerging gnostic denials of Christ's physical incarnation and death. Church tradition records John's martyrdom under Domitian, demonstrating his willingness to die for testimony he could have recanted if false.",
            "questions": [
                "How does John's emphatic eyewitness testimony provide a foundation for faith distinct from blind belief or subjective experience?",
                "What makes the apostles' willingness to die for their testimony particularly significant for Christian apologetics?",
                "How should believers today communicate that Christian faith rests on historical events, not mythology or wishful thinking?"
            ]
        },
        "36": {
            "analysis": "<strong>For these things were done, that the scripture should be fulfilled, A bone of him shall not be broken</strong> (ἐγένετο γὰρ ταῦτα ἵνα ἡ γραφὴ πληρωθῇ· Ὀστοῦν οὐ συντριβήσεται αὐτοῦ, <em>egeneto gar tauta hina hē graphē plērōthē· Ostoun ou syntribēsetai autou</em>)—John identifies prophecy fulfillment. The phrase ἵνα ἡ γραφὴ πληρωθῇ (<em>hina hē graphē plērōthē</em>, 'that the Scripture might be fulfilled') indicates divine design, not coincidence. <strong>A bone of him shall not be broken</strong> (Ὀστοῦν οὐ συντριβήσεται, <em>Ostoun ou syntribēsetai</em>) quotes Exodus 12:46 and Psalm 34:20. The Passover lamb regulations required bones remain intact; David's psalm about God's protection found ultimate fulfillment in Christ.<br><br>This typological fulfillment demonstrates Scripture's unity and divine inspiration. The Passover lamb pointed forward to Christ (1 Corinthians 5:7); what seemed mere ritual detail revealed Messianic prophecy. Jesus is the true Passover Lamb whose sacrifice delivers from death's angel, whose blood marks God's people for salvation.",
            "historical": "Passover lambs were slaughtered on 14 Nisan (Exodus 12:6), eaten without broken bones. Jesus died as the Passover lambs were being sacrificed in the temple—the ultimate Lamb replacing all others. The coincidence of timing, prophecy, and fulfillment demonstrates divine orchestration spanning 1500 years from Moses to Christ.",
            "questions": [
                "How does typological fulfillment—Passover lamb to Christ—demonstrate the Bible's divine inspiration and unity?",
                "What does it mean that Jesus is our Passover Lamb—how does His sacrifice parallel and fulfill Exodus 12?",
                "How should Christians read Old Testament Law and ritual in light of Christ's fulfillment?"
            ]
        },
        "37": {
            "analysis": "<strong>And again another scripture saith, They shall look on him whom they pierced</strong> (καὶ πάλιν ἑτέρα γραφὴ λέγει· Ὄψονται εἰς ὃν ἐξεκέντησαν, <em>kai palin hetera graphē legei· Opsontai eis hon exekentēsan</em>)—John cites Zechariah 12:10. The verb ὄψονται (<em>opsontai</em>, 'they shall look, gaze upon') combined with ἐξεκέντησαν (<em>exekentēsan</em>, 'they pierced') describes the spear thrust (19:34) but points beyond to eschatological fulfillment. Zechariah's prophecy has dual fulfillment: historical (the crucifixion) and future (Christ's second coming when all will see the One they pierced, Revelation 1:7).<br><br>This prophecy carries both judgment and grace. Those who 'pierced' Him—representing all sinners whose sins nailed Him there—will 'look upon' Him either in saving faith or condemning judgment. The same wounded Christ is both Savior and Judge. Zechariah 12:10 continues: 'they shall mourn for him'—mourning in repentance (Second Coming) or mourning in terror (final judgment).",
            "historical": "Zechariah prophesied around 520-518 BC, 550 years before crucifixion was even invented by Phoenicians and adopted by Romans. The specific detail of 'piercing' (דָּקַר, <em>daqar</em> in Hebrew; ἐκκεντέω, <em>ekkenteo</em> in Greek) rather than generic 'killing' demonstrates prophetic precision only explicable by divine inspiration.",
            "questions": [
                "How does Zechariah's 'piercing' prophecy demonstrate supernatural foreknowledge of crucifixion method 550 years before its invention?",
                "What does it mean that all will 'look upon' the One they pierced—how does this apply both at conversion and final judgment?",
                "How should recognition that our sins 'pierced' Christ shape our understanding of personal accountability for His death?"
            ]
        },
        "38": {
            "analysis": "<strong>And after this Joseph of Arimathaea, being a disciple of Jesus, but secretly for fear of the Jews, besought Pilate that he might take away the body of Jesus: and Pilate gave him leave</strong> (Μετὰ δὲ ταῦτα ἠρώτησεν τὸν Πιλᾶτον Ἰωσὴφ ὁ ἀπὸ Ἁριμαθαίας, ὢν μαθητὴς τοῦ Ἰησοῦ κεκρυμμένος δὲ διὰ τὸν φόβον τῶν Ἰουδαίων, ἵνα ἄρῃ τὸ σῶμα τοῦ Ἰησοῦ· καὶ ἐπέτρεψεν ὁ Πιλᾶτος, <em>Meta de tauta ērōtēsen ton Pilaton Iōsēph ho apo Harimathaias, ōn mathētēs tou Iēsou kekrymmenos de dia ton phobon tōn Ioudaiōn, hina arē to sōma tou Iēsou· kai epetrepsen ho Pilatos</em>)—Joseph was μαθητὴς...κεκρυμμένος (<em>mathētēs...kekrymmenos</em>, 'a disciple...hidden') διὰ τὸν φόβον τῶν Ἰουδαίων (<em>dia ton phobon tōn Ioudaiōn</em>, 'because of the fear of the Jews'). Yet crisis prompted courage: he openly requested Jesus's body. <strong>He came therefore, and took the body of Jesus</strong>—Joseph's public action 'outed' him as Jesus's follower, risking his Sanhedrin position (Mark 15:43 identifies him as 'an honourable counsellor').<br><br>Fear had kept Joseph secret, but Jesus's death catalyzed courageous faith. Sometimes God allows crisis to move secret disciples to public confession. Joseph's costly obedience—risking reputation, position, ritual defilement—demonstrates transformative faith. His unused tomb (Matthew 27:60) fulfilled Isaiah 53:9: 'with the rich in his death.'",
            "historical": "Arimathea was likely Ramathaim-zophim, Samuel's birthplace (1 Samuel 1:1), about 20 miles northwest of Jerusalem. As a wealthy Sanhedrin member (Luke 23:50), Joseph had resources and influence to request the body and provide burial. Roman law typically allowed families to claim crucifixion victims' bodies; Pilate's permission shows respect for Joseph's status.",
            "questions": [
                "How does Joseph's transformation from 'secret disciple' to public confessor demonstrate that crisis can strengthen rather than destroy faith?",
                "What modern forms of 'secret discipleship' do Christians practice to avoid social or professional cost?",
                "How did providing an honorable burial for Jesus demonstrate both love for Christ and courage to associate with a condemned criminal?"
            ]
        },
        "39": {
            "analysis": "<strong>And there came also Nicodemus, which at the first came to Jesus by night, and brought a mixture of myrrh and aloes, about an hundred pound weight</strong> (ἦλθεν δὲ καὶ Νικόδημος, ὁ ἐλθὼν πρὸς αὐτὸν νυκτὸς τὸ πρῶτον, φέρων μίγμα σμύρνης καὶ ἀλόης ὡς λίτρας ἑκατόν, <em>ēlthen de kai Nikodēmos, ho elthōn pros auton nyktos to prōton, pherōn migma smyrnēs kai aloēs hōs litras hekaton</em>)—Nicodemus, introduced in John 3 as the nighttime visitor, now comes publicly with extravagant burial spices: σμύρνης καὶ ἀλόης (<em>smyrnēs kai aloēs</em>, 'myrrh and aloes') weighing ὡς λίτρας ἑκατόν (<em>hōs litras hekaton</em>, 'about 100 pounds/75 lbs modern weight'). This enormous quantity—appropriate for kings (2 Chronicles 16:14)—demonstrates both wealth and devotion.<br><br>Nicodemus's progression tracks spiritual growth: first, fearful nighttime inquiry (John 3:1-21); second, tepid defense of Jesus (John 7:50-51); finally, public identification with the crucified Christ. The 'hundred pounds' of spices is lavish—far exceeding normal burial practices. This act of worship echoes Mary's anointing (John 12:3): when you love Jesus, no gift is excessive. Both Joseph and Nicodemus gave treasures to honor the One religious leaders dishonored.",
            "historical": "Roman custom was cremation; Jewish custom required quick burial with spices to offset decomposition in warm climate. Nicodemus's quantity suggested expectation of extended burial. Myrrh and aloes were aromatic resins mixed and applied between linen wrappings. The expense indicated royal burial—ironically for the 'King of the Jews' mocked hours earlier.",
            "questions": [
                "How does Nicodemus's spiritual journey from secret seeker to public confessor encourage gradual growth in faith?",
                "What does the extravagant quantity of burial spices teach about appropriate worship—is anything 'too much' for Jesus?",
                "How do Joseph and Nicodemus's actions demonstrate that true faith eventually requires public identification with Christ regardless of cost?"
            ]
        },
        "40": {
            "analysis": "<strong>Then took they the body of Jesus, and wound it in linen clothes with the spices, as the manner of the Jews is to bury</strong> (ἔλαβον οὖν τὸ σῶμα τοῦ Ἰησοῦ καὶ ἔδησαν αὐτὸ ὀθονίοις μετὰ τῶν ἀρωμάτων, καθὼς ἔθος ἐστὶν τοῖς Ἰουδαίοις ἐνταφιάζειν, <em>elabon oun to sōma tou Iēsou kai edēsan auto othoniois meta tōn arōmatōn, kathōs ethos estin tois Ioudaiois entaphiazein</em>)—They wrapped Jesus's body in ὀθόνια (<em>othonia</em>, 'linen strips/cloths') μετὰ τῶν ἀρωμάτων (<em>meta tōn arōmatōn</em>, 'with the spices'), following Jewish burial customs. The verb ἔδησαν (<em>edēsan</em>, 'bound, wrapped') indicates tight binding. This detail becomes significant in resurrection accounts: the grave clothes remained intact yet empty (John 20:6-7), indicating Jesus passed through them rather than unwrapping.<br><br>This proper burial fulfilled prophecy (Isaiah 53:9) and validated Jesus's true death against later claims He merely swooned. The care taken by Joseph and Nicodemus—wealthy men risking defilement before Passover—demonstrates costly love. Their 'burial rites' prepared the tomb Jesus would vacate three days later, making the resurrection undeniable: sealed tomb, wrapped body, Roman guard, yet empty grave.",
            "historical": "Jewish burial required washing the body, anointing with spices, and wrapping in linen strips—process taking several hours. They had to complete this before 6pm when Sabbath began. The haste partly explains the women's intention to return Sunday with additional spices (Mark 16:1), though they found the tomb empty.",
            "questions": [
                "How does the detailed burial account validate Jesus's real death against swoon theories?",
                "What does the care and expense of Jesus's burial by Joseph and Nicodemus teach about properly honoring Christ?",
                "How do the burial details—wrapped body in sealed tomb—make the resurrection evidence more compelling?"
            ]
        },
        "41": {
            "analysis": "<strong>Now in the place where he was crucified there was a garden; and in the garden a new sepulchre, wherein was never man yet laid</strong> (ἦν δὲ ἐν τῷ τόπῳ ὅπου ἐσταυρώθη κῆπος, καὶ ἐν τῷ κήπῳ μνημεῖον καινὸν ἐν ᾧ οὐδέπω οὐδεὶς ἦν τεθειμένος, <em>ēn de en tō topō hopou estaurōthē kēpos, kai en tō kēpō mnēmeion kainon en hō oudepō oudeis ēn tetheimenos</em>)—Crucifixion occurred at Golgotha (John 19:17); nearby was a κῆπος (<em>kēpos</em>, 'garden') containing Joseph's μνημεῖον καινόν (<em>mnēmeion kainon</em>, 'new tomb'). The phrase οὐδέπω οὐδεὶς ἦν τεθειμένος (<em>oudepō oudeis ēn tetheimenos</em>, 'no one yet had been laid') emphasizes the tomb's unused state—prepared by Joseph but virgin until Jesus's burial.<br><br>The 'garden' evokes Eden where sin entered (Genesis 3); now in a garden, redemption is accomplished. The unused tomb fulfills typology: like the unblemished sacrifice, Jesus rested in a 'new' tomb undefiled by prior death. This also eliminates claims others' bones were later confused with Jesus's—no one else was ever buried there.",
            "historical": "Garden tombs near Jerusalem were owned by wealthy families—carved from rock, sealed with rolling stones. Joseph owned this tomb (Matthew 27:60), intending it for his own burial. Providing it for Jesus was costly—he'd need another tomb. Archaeological site Church of the Holy Sepulchre preserves ancient tradition locating both Golgotha and garden tomb.",
            "questions": [
                "How does the 'garden' setting connect Jesus's death and resurrection to both Creation (Eden) and new creation themes?",
                "What's the theological significance of Jesus being buried in a new, unused tomb?",
                "How does Joseph's sacrifice of his personal tomb illustrate costly discipleship—giving Jesus what was most precious?"
            ]
        },
        "42": {
            "analysis": "<strong>There laid they Jesus therefore because of the Jews' preparation day; for the sepulchre was nigh at hand</strong> (ἐκεῖ οὖν διὰ τὴν παρασκευὴν τῶν Ἰουδαίων, ὅτι ἐγγὺς ἦν τὸ μνημεῖον, ἔθηκαν τὸν Ἰησοῦν, <em>ekei oun dia tēn paraskeuēn tōn Ioudaiōn, hoti engys ēn to mnēmeion, ethēkan ton Iēsoun</em>)—Time pressure (παρασκευή, <em>paraskeuē</em>, 'Preparation day'—Friday before Sabbath) and proximity (ἐγγὺς ἦν, <em>engys ēn</em>, 'was near') determined the burial location. They had perhaps two hours before 6pm Sabbath. The verb ἔθηκαν (<em>ethēkan</em>, 'they placed, laid') suggests reverent positioning of Jesus's body in the tomb.<br><br>Divine providence arranged every detail: Joseph's unused tomb happened to be near Golgotha; the timing forced hasty but complete burial; witnesses observed the location (Luke 23:55). These 'coincidences' ensured irrefutable resurrection evidence—known tomb, verified death, sealed entrance, yet empty three days later. Nothing was left to chance; God orchestrated circumstances to maximize evidential clarity for the most important event in history.",
            "historical": "Jewish law required burial same day as death (Deuteronomy 21:23). Sabbath began at sundown Friday. This time constraint meant Joseph and Nicodemus worked quickly but thoroughly. The women observed burial location to return Sunday (Mark 16:1), providing multiple witnesses who could testify the same tomb later found empty was where Jesus was buried.",
            "questions": [
                "How does God's providence in small details—tomb location, timing, witnesses—strengthen resurrection evidence?",
                "What does the haste required by Sabbath law teach about how God uses even legal restrictions to accomplish His purposes?",
                "How should believers trust that God orchestrates even seemingly minor details to accomplish His sovereign will?"
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

print(f"\nTotal John verses added (Part 3): {added_count}")
print(f"Saved to {filepath}")
print(f"\n=== ALL JOHN COMMENTARY COMPLETE ===")
print(f"Total: 13 + 11 + {added_count} = 36 verses")
