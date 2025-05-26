from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
import random
import html
import json

from .kjv import bible


app = FastAPI(
    title="KJV Study - Bible Commentary Platform",
    description="Study the King James Bible with AI-powered commentary and insights",
    version="1.0.0"
)

# Set up Jinja2 templates and static files
current_dir = Path(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom error handler that renders our error template"""
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
            status_code=exc.status_code,
        )

    # For other errors, use the default handler
    return await http_exception_handler(request, exc)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    books = list(bible.iter_books())

    return templates.TemplateResponse(
        "index.html", {"request": request, "books": books}
    )


@app.get("/book/{book}", response_class=HTMLResponse)
def read_book(request: Request, book: str):
    books = list(bible.iter_books())
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    if not chapters:
        raise HTTPException(
            status_code=404, 
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )
    return templates.TemplateResponse(
        "book.html",
        {"request": request, "book": book, "chapters": chapters, "books": books},
    )


@app.get("/book/{book}/commentary", response_class=HTMLResponse)
def book_commentary(request: Request, book: str):
    """Generate comprehensive commentary for an entire book"""
    books = list(bible.iter_books())
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    if not chapters:
        raise HTTPException(
            status_code=404, 
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )
    
    # Generate comprehensive book commentary
    commentary_data = generate_book_commentary(book, chapters)
    
    return templates.TemplateResponse(
        "book_commentary.html",
        {
            "request": request,
            "book": book,
            "chapters": chapters,
            "books": books,
            **commentary_data
        },
    )


@app.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
def read_chapter(request: Request, book: str, chapter: int):
    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404, 
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )
    
    # Generate AI commentary for the chapter
    commentaries = {}
    for verse in verses:
        commentaries[verse.verse] = generate_commentary(book, chapter, verse)
    
    # Generate chapter overview
    chapter_overview = generate_chapter_overview(book, chapter, verses)
    
    return templates.TemplateResponse(
        "chapter.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview
        },
    )


@app.get("/commentary/{book}/{chapter}", response_class=HTMLResponse)
def commentary(request: Request, book: str, chapter: int):
    """Generate AI-powered commentary for a specific chapter"""
    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Generate AI commentary for each verse
    commentaries = {}
    for verse in verses:
        commentaries[verse.verse] = generate_commentary(book, chapter, verse)

    # Generate chapter overview
    chapter_overview = generate_chapter_overview(book, chapter, verses)

    return templates.TemplateResponse(
        "commentary.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview
        },
    )


def generate_commentary(book, chapter, verse):
    """Generate AI-powered commentary for a specific verse"""
    # Special case for Revelation 1
    if book == "Revelation" and chapter == 1:
        # Dictionary of specialized commentary for Revelation 1
        revelation1_commentary = {
            1: {
                "analysis": """This opening verse establishes the divine origin of the Apocalypse (from Greek ἀποκάλυψις/<em>apokalypsis</em>, meaning "unveiling" or "revelation"). The chain of revelation is significant: from God, to Christ, to angel, to John, to the churches—establishing divine authority and authenticity. The phrase "things which must shortly come to pass" (ἃ δεῖ γενέσθαι ἐν τάχει) indicates both urgency and certainty, though not necessarily immediacy in human time scales. The Greek term ἐν τάχει can indicate rapidity of execution once something begins rather than imminence.<br><br>The phrase "signified it by his angel" uses the Greek ἐσήμανεν (from σημαίνω/<em>sēmainō</em>), literally meaning "to show by signs," hinting at the symbolic nature of the visions to follow. This carefully constructed introduction establishes: divine origin, Christological mediation, angelic communication, apostolic witness, and ecclesiastical destination.""",
                "historical": """During the reign of Emperor Domitian (81-96 CE), imperial cult worship intensified throughout the Roman Empire. Domitian demanded to be addressed as "Lord and God" (<em>dominus et deus noster</em>), and erected statues of himself for veneration. Christians who refused to burn incense to the emperor or participate in imperial festivals faced economic sanctions, social ostracism, and sometimes execution.<br><br>Patmos, where John received this revelation, was a small, rocky island about 37 miles southwest of Miletus in the Aegean Sea. Roman authorities used such islands as places of exile for political prisoners. John identifies himself as there "for the word of God, and for the testimony of Jesus Christ" (v.9), indicating his exile was punishment for his Christian witness.<br><br>The seven churches addressed were located along a Roman postal route in the province of Asia (western Turkey), each facing unique local challenges while sharing the broader imperial context of Roman domination and pressure to compromise.""",
                "questions": [
                    "How does the concept of divine revelation through a chain of transmission (God→Christ→angel→John→churches) shape your understanding of biblical authority?",
                    "In what ways does the description of Jesus 'signifying' the revelation suggest an approach to interpreting the symbolic language throughout the book?",
                    "How should we understand the timeframe indicated by 'shortly come to pass' given that nearly 2,000 years have passed? What different interpretive approaches address this apparent tension?",
                    "How might John's emphasis on the divine origin of this revelation have strengthened the resolve of persecuted believers in Asia Minor?"
                ],
                "cross_references": [
                    {"text": "Daniel 2:28-29", "url": "/book/Daniel/chapter/2#verse-28", "context": "Things revealed about the latter days"},
                    {"text": "John 15:15", "url": "/book/John/chapter/15#verse-15", "context": "Christ revealing the Father's will"},
                    {"text": "Amos 3:7", "url": "/book/Amos/chapter/3#verse-7", "context": "God revealing secrets to prophets"},
                    {"text": "2 Peter 1:20-21", "url": "/book/2 Peter/chapter/1#verse-20", "context": "Divine origin of prophecy"}
                ]
            },
            4: {
                "analysis": """This verse begins the formal epistolary greeting to the seven churches of Asia Minor. The trinitarian formula is striking and unique: the eternal Father ("who is, who was, and who is to come"), the sevenfold Spirit "before his throne," and Jesus Christ (fully described in v.5).<br><br>The description of God as "who is, who was, and who is to come" (ὁ ὢν καὶ ὁ ἦν καὶ ὁ ἐρχόμενος) forms a deliberate adaptation of God's self-revelation in Exodus 3:14. While Greek would normally render the divine name with "who was, who is, and who will be," John alters the final element to emphasize not just God's future existence but His active coming to establish His kingdom.<br><br>The "seven Spirits before his throne" has been interpreted in several ways: (1) the sevenfold manifestation of the Holy Spirit based on Isaiah 11:2-3, (2) the seven archangels of Jewish apocalyptic tradition, or (3) the perfection and completeness of the Holy Spirit. The context strongly suggests this refers to the Holy Spirit in His perfect fullness, as this forms part of the trinitarian greeting. The number seven appears 54 times in Revelation, consistently symbolizing divine completeness and perfection.""",
                "historical": """The seven churches addressed—Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, and Laodicea—were actual congregations in Asia Minor (modern western Turkey). They existed along a natural circular mail route approximately 100 miles in diameter.<br><br>Each city had distinctive characteristics:<br>• <strong>Ephesus</strong>: A major commercial center with the Temple of Artemis (one of the Seven Wonders of the ancient world)<br>• <strong>Smyrna</strong>: A beautiful port city known for emperor worship and fierce loyalty to Rome<br>• <strong>Pergamum</strong>: The provincial capital with an enormous altar to Zeus and a temple to Asclepius (god of healing)<br>• <strong>Thyatira</strong>: Known for trade guilds that posed idolatry challenges for Christians<br>• <strong>Sardis</strong>: Former capital of Lydia, known for wealth and textile industry<br>• <strong>Philadelphia</strong>: The youngest and smallest city, subject to earthquakes<br>• <strong>Laodicea</strong>: A banking center known for eye medicine and black wool<br><br>These churches represented the spectrum of faith communities, facing various challenges: persecution, false teaching, moral compromise, spiritual apathy, and economic pressure to participate in trade guild idolatry. Though historically specific, they also represent the complete church throughout history (seven symbolizing completeness).""",
                "questions": [
                    "What does the description of God as 'who is, who was, and who is to come' reveal about divine nature and how does this differ from Greek philosophical conceptions of deity?",
                    "How does John's adaptation of the divine name from Exodus 3:14 emphasize God's active involvement in human history?",
                    "What theological significance might the order of the Trinity in this greeting have (Father, Spirit, Son) compared to more common formulations?",
                    "How might the believers in these seven diverse churches have found comfort in being addressed collectively under divine blessing?",
                    "What might the image of the 'seven Spirits before his throne' suggest about the Holy Spirit's relationship to both the Father and the churches?"
                ],
                "cross_references": [
                    {"text": "Exodus 3:14", "url": "/book/Exodus/chapter/3#verse-14", "context": "God as the 'I AM'"},
                    {"text": "Isaiah 11:2-3", "url": "/book/Isaiah/chapter/11#verse-2", "context": "Seven aspects of the Spirit"},
                    {"text": "Zechariah 4:2-10", "url": "/book/Zechariah/chapter/4#verse-2", "context": "Seven lamps as the eyes of the LORD"},
                    {"text": "2 Corinthians 13:14", "url": "/book/2 Corinthians/chapter/13#verse-14", "context": "Trinitarian blessing"}
                ]
            },
            7: {
                "analysis": """This powerful verse serves as the central proclamation of Christ's eschatological return, combining two profound Old Testament prophecies in a remarkable synthesis: Daniel 7:13 ("coming with clouds") and Zechariah 12:10 ("they shall look upon me whom they have pierced").<br><br>The declaration begins dramatically with "Behold" (Ἰδού/<em>idou</em>), demanding attention to this climactic event. The "clouds" (νεφελῶν/<em>nephelōn</em>) evoke both the Old Testament theophany tradition where clouds symbolize divine presence (Exodus 13:21, 19:9) and Daniel's vision of the Son of Man coming with clouds to receive dominion and glory.<br><br>The universal witness to Christ's return ("every eye shall see him") emphasizes its public, unmistakable nature, contrasting with His first coming in relative obscurity. The specific mention of "they which pierced him" (ἐξεκέντησαν/<em>exekentēsan</em>, a direct reference to the crucifixion) and the mourning of "all kindreds of the earth" introduces a tension between judgment and potential repentance.<br><br>The verse concludes with divine affirmation—"Even so, Amen"—combining Greek (ναί/<em>nai</em>) and Hebrew (ἀμήν/<em>amēn</em>) expressions of certainty, emphasizing this event's absolute inevitability across all cultures.""",
                "historical": """For Christians facing persecution under Domitian (81-96 CE), this proclamation of Christ's return as cosmic Lord would provide profound hope and perspective. Roman imperial ideology presented the emperor as divine ruler whose reign brought global peace (<em>pax Romana</em>). Imperial propaganda celebrated the emperor's <em>parousia</em> (arrival) to cities with elaborate ceremonies.<br><br>This verse subverts those imperial claims by declaring Jesus—not Caesar—as the true cosmic sovereign whose <em>parousia</em> will bring history to its climax. The language of "tribes of the earth mourning" (πᾶσαι αἱ φυλαὶ τῆς γῆς) echoes Roman triumphal processions where conquered peoples mourned as the victorious emperor processed through Rome.<br><br>For Jewish readers, the combination of Daniel 7:13 and Zechariah 12:10 was especially significant. While first-century Judaism typically separated the Messiah's coming from Yahweh's coming, John merges these, presenting Jesus as fulfilling both messianic hope and divine visitation. This would be both challenging and transformative for Jewish believers.<br><br>Archaeological evidence from the seven cities addressed shows extensive emperor worship installations. In Pergamum stood a massive temple to Augustus; in Ephesus was the Temple of Domitian with a 23-foot statue of the emperor. Against these claims of imperial divinity, the vision of Christ's return asserted true divine sovereignty.""",
                "questions": [
                    "How does the merging of Daniel 7:13 and Zechariah 12:10 transform our understanding of both prophecies, and what does this tell us about Christ's identity?",
                    "What is the significance of the universal nature of Christ's return—that 'every eye shall see him'—in contrast to claims of secret or localized appearances?",
                    "How might the phrase 'all kindreds of the earth shall wail because of him' be understood—is this solely judgment, or might it include elements of repentance and recognition?",
                    "In what ways does the certainty of Christ's return as cosmic Lord challenge contemporary 'empires' and power structures?",
                    "How should the tension between Christ's first coming in humility and His second coming in glory shape our understanding of God's redemptive work?"
                ],
                "cross_references": [
                    {"text": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "context": "Son of Man coming with clouds"},
                    {"text": "Zechariah 12:10-14", "url": "/book/Zechariah/chapter/12#verse-10", "context": "Looking on him whom they pierced"},
                    {"text": "Matthew 24:30-31", "url": "/book/Matthew/chapter/24#verse-30", "context": "Christ's return with clouds and angels"},
                    {"text": "1 Thessalonians 4:16-17", "url": "/book/1 Thessalonians/chapter/4#verse-16", "context": "The Lord's descent from heaven"},
                    {"text": "John 19:34-37", "url": "/book/John/chapter/19#verse-34", "context": "Christ pierced on the cross"}
                ]
            },
            13: {
                "analysis": """This verse begins the extraordinary Christophany—the vision of the glorified Christ among the lampstands. The description combines elements of royal, priestly, prophetic, and divine imagery in a stunning portrait of Christ's transcendent glory.<br><br>The phrase "one like unto the Son of man" (ὅμοιον υἱὸν ἀνθρώπου) deliberately echoes Daniel 7:13-14, where the "Son of Man" comes with clouds and receives everlasting dominion. This title, Jesus' favorite self-designation in the Gospels, here takes on its full apocalyptic significance.<br><br>The clothing described has dual significance: the "garment down to the foot" (ποδήρη/<em>podērē</em>) recalls the high priest's robe (Exodus 28:4, 39:29) while the "golden girdle" or sash around the chest rather than waist suggests royal dignity. In combining these images, Christ is presented as both King and High Priest in the order of Melchizedek (Hebrews 7).<br><br>His position "in the midst of the seven lampstands" is theologically significant, showing Christ's immediate presence with and authority over the churches. The lampstands (later identified as the seven churches) allude to both the tabernacle menorah (Exodus 25:31-40) and Zechariah's vision (Zechariah 4:2-10), suggesting the churches' function as light-bearers in the world under Christ's oversight.""",
                "historical": """In the Greco-Roman world of the late first century, this vision would have provided a stunning contrast to imperial imagery. Roman emperors were typically portrayed in statuary and coinage with idealized, youthful features, wearing the purple toga of authority, and often with radiate crowns suggesting solar divinity.<br><br>Domitian particularly promoted his divine status, having himself addressed as <em>dominus et deus noster</em> ("our lord and god"). In the provincial capital Pergamum (one of the seven churches addressed), a massive temple complex dedicated to emperor worship dominated the acropolis, visible throughout the city.<br><br>The Jewish community would have recognized multiple elements from prophetic tradition. The figure combines features from Ezekiel's vision of God's glory (Ezekiel 1:26-28), Daniel's "Ancient of Days" and "Son of Man" (Daniel 7:9-14, 10:5-6), and various theophany accounts. This deliberate merging of divine imagery with the human "Son of Man" figure creates one of the New Testament's most explicit presentations of Christ's deity.<br><br>Archaeological excavations at Ephesus (another of the seven churches) have uncovered a 23-foot statue of Emperor Domitian that once stood in his temple. John's vision provides the ultimate counter-imperial image: Christ as the true divine sovereign standing among His churches, outshining all imperial pretensions.""",
                "questions": [
                    "How does this vision of the glorified Christ compare with other portraits in Scripture, such as the transfiguration (Matthew 17:1-8) or Isaiah's throne room vision (Isaiah 6:1-5)?",
                    "What theological significance does Christ's position 'in the midst of the seven lampstands' have for our understanding of His relationship to the church?",
                    "How does the combination of royal, priestly, and divine imagery shape our understanding of Christ's multifaceted identity and work?",
                    "In what ways might this vision of Christ have challenged first-century believers' perspectives and provided comfort during persecution?",
                    "How should this majestic portrayal of Christ influence our worship and daily discipleship today?"
                ],
                "cross_references": [
                    {"text": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "context": "Son of Man vision"},
                    {"text": "Ezekiel 1:26-28", "url": "/book/Ezekiel/chapter/1#verse-26", "context": "Throne vision of divine glory"},
                    {"text": "Exodus 28:4, 39:29", "url": "/book/Exodus/chapter/28#verse-4", "context": "High priestly garments"},
                    {"text": "Hebrews 4:14-16", "url": "/book/Hebrews/chapter/4#verse-14", "context": "Christ as High Priest"},
                    {"text": "Zechariah 4:2-10", "url": "/book/Zechariah/chapter/4#verse-2", "context": "Vision of the lampstand"}
                ]
            },
            18: {
                "analysis": """This triumphant declaration by the risen Christ contains some of the most profound Christological statements in Scripture. The opening "I am" (ἐγώ εἰμι/<em>egō eimi</em>) echoes God's self-revelation to Moses (Exodus 3:14) and continues John's high Christology throughout Revelation.<br><br>The phrase "he that liveth, and was dead" encapsulates the central paradox of Christian faith—Christ's death and resurrection. The Greek construction (ὁ ζῶν, καὶ ἐγενόμην νεκρὸς) emphasizes the contrast between His eternal living nature and the historical fact of His death. The perfect tense of "am alive" (ζῶν εἰμι) indicates a past action with continuing results—He lives now because He conquered death.<br><br>The declaration "I am alive forevermore" (ζῶν εἰμι εἰς τοὺς αἰῶνας τῶν αἰώνων) asserts Christ's eternal existence, while "Amen" provides divine self-affirmation.<br><br>The climactic statement about possessing "the keys of hell and of death" (τὰς κλεῖς τοῦ θανάτου καὶ τοῦ ᾅδου) draws on ancient imagery where keys symbolize authority and control. In Jewish apocalyptic literature, these keys belonged exclusively to God. Christ now claims this divine prerogative, declaring His absolute sovereignty over mortality and the afterlife—the ultimate source of human fear.""",
                "historical": """For Christians facing potential martyrdom under Domitian's persecution, this verse would provide extraordinary comfort and courage. The Roman Empire's ultimate weapon against dissidents was death, but Christ's declaration neutralizes this threat by asserting His authority over death itself.<br><br>In Greco-Roman culture, Hades (ᾅδης, translated as "hell" in KJV) was understood as the realm of the dead, ruled by the god of the same name. Various mystery religions promised initiates privileged treatment in the afterlife, while imperial propaganda sometimes suggested the emperor controlled the destiny of subjects even after death.<br><br>Archaeological findings from the period show funerary inscriptions often expressing hopelessness regarding death. A common epitaph read "I was not, I became, I am not, I care not." Against this cultural backdrop of either fear or nihilism toward death, Christ's claim to hold death's keys would be revolutionary.<br><br>In Jewish tradition, Isaiah 22:22 presents God giving the "key of the house of David" to Eliakim, symbolizing transferred authority. The early church would understand Christ's possession of death's keys as fulfillment of His promise to Peter about the "keys of the kingdom" (Matthew 16:19)—but here magnified to cosmic proportions.<br><br>For the seven churches receiving this revelation—some already experiencing martyrdom (like Antipas in Pergamum, 2:13)—this verse transformed their understanding of persecution. Death was no longer defeat but transition into the realm still under Christ's authority.""",
                "questions": [
                    "How does Christ's claim to possess 'the keys of hell and of death' transform our understanding of mortality and the afterlife?",
                    "In what ways does the paradox of Christ who died yet lives forever challenge both ancient and modern conceptions of divine nature?",
                    "How might believers facing persecution or martyrdom throughout history have drawn strength from this verse?",
                    "What practical implications does Christ's victory over death have for disciples facing suffering, bereavement, or their own mortality?",
                    "How does this verse relate to Paul's teaching that 'the last enemy to be destroyed is death' (1 Corinthians 15:26)?"
                ],
                "cross_references": [
                    {"text": "Isaiah 22:22", "url": "/book/Isaiah/chapter/22#verse-22", "context": "The key of David symbolizing authority"},
                    {"text": "Romans 6:9-10", "url": "/book/Romans/chapter/6#verse-9", "context": "Christ dies no more, death has no dominion"},
                    {"text": "1 Corinthians 15:54-57", "url": "/book/1 Corinthians/chapter/15#verse-54", "context": "Death is swallowed up in victory"},
                    {"text": "Hebrews 2:14-15", "url": "/book/Hebrews/chapter/2#verse-14", "context": "Christ destroys death and delivers from its fear"},
                    {"text": "Hosea 13:14", "url": "/book/Hosea/chapter/13#verse-14", "context": "Prophecy of ransom from death and redemption from the grave"}
                ]
            }
        }

        # If we have special commentary for this verse, use it
        if verse.verse in revelation1_commentary:
            return revelation1_commentary[verse.verse]

        # For other verses in Revelation 1, use enhanced but generalized commentary
        analysis = f"This verse is part of John's apocalyptic vision of the glorified Christ. The symbolism connects to Old Testament prophetic tradition, particularly from Daniel and Ezekiel, while revealing Christ's divine nature and authority. The imagery of {get_key_phrase(verse.text.lower())} contributes to the overall majestic portrayal."

        historical = f"Written during a time of imperial persecution under Domitian, this vision would have encouraged believers to remain faithful despite opposition. The apocalyptic imagery draws on Jewish prophetic traditions while speaking to the specific challenges faced by first-century Christians in Asia Minor."

        questions = [
            "How does this verse contribute to the overall portrayal of Christ in Revelation 1?",
            "What symbolic elements in this verse connect to Old Testament prophecy?",
            "How might this imagery have strengthened the faith of persecuted believers?",
            "What does this revelation tell us about Christ's relationship to the Church?"
        ]

        # Generate cross-references specific to Revelation imagery
        cross_refs = [
            {"text": "Daniel 7:9-14", "url": "/book/Daniel/chapter/7#verse-9", "context": "Ancient of Days and Son of Man vision"},
            {"text": "Ezekiel 1:26-28", "url": "/book/Ezekiel/chapter/1#verse-26", "context": "Divine throne vision"},
            {"text": "Isaiah 6:1-5", "url": "/book/Isaiah/chapter/6#verse-1", "context": "Throne room vision"}
        ]

        return {
            "analysis": analysis,
            "historical": historical,
            "questions": random.sample(questions, 3),
            "cross_references": cross_refs[:2]  # Limit to 2 references
        }

    # For all other books/chapters, use the general approach
    verse_text = verse.text.lower()
    verse_number = verse.verse

    # Simulated analysis based on the verse content and patterns
    analysis_templates = [
        f"This verse emphasizes the {get_theme(verse_text)} theme common in {book}. The phrase \"{get_key_phrase(verse_text)}\" is particularly significant as it relates to the broader context of this chapter.",
        f"The {get_language_feature(verse_text)} used here is characteristic of {book}'s literary style. This verse builds upon the previous context while introducing the concept of {get_concept(verse_text)}.",
        f"Here we see a {get_literary_device(verse_text)} that draws attention to {get_theme(verse_text)}. The author uses specific terminology that would have resonated with the original audience.",
        f"This verse contains {get_literary_device(verse_text)} that emphasizes the {get_theme(verse_text)}. The language choice reveals the author's intention to highlight {get_concept(verse_text)}.",
    ]

    historical_templates = [
        f"In the historical context of {get_time_period(book)}, this reference to \"{get_key_phrase(verse_text)}\" would have had significant meaning. {get_historical_context(book)}",
        f"The {get_cultural_element(verse_text)} mentioned here was common in {get_time_period(book)}. {get_historical_context(book)} The original audience would have understood this reference differently than modern readers.",
        f"During {get_time_period(book)}, the concept of {get_concept(verse_text)} had specific cultural connotations. {get_historical_context(book)} This provides important context for understanding the verse.",
        f"The historical setting of {get_time_period(book)} helps explain why the author emphasizes {get_theme(verse_text)}. {get_historical_context(book)}"
    ]

    # Study questions based on verse content
    question_templates = [
        f"How does the concept of {get_concept(verse_text)} apply to contemporary faith?",
        f"What does this verse reveal about the character of God?",
        f"How does this verse connect to other passages in {book} or elsewhere in Scripture?",
        f"What practical applications can be drawn from this verse?",
        f"How might the original audience have understood this passage differently than we do today?",
        f"What aspects of {get_theme(verse_text)} are emphasized in this verse?",
        f"In what ways does this verse challenge or affirm your current understanding?",
        f"How does this verse fit into the broader narrative of Scripture?",
    ]

    # Generate cross-references
    cross_refs = generate_cross_references(book, chapter, verse_number, verse_text)

    # Return a dictionary with all commentary components
    return {
        "analysis": random.choice(analysis_templates),
        "historical": random.choice(historical_templates),
        "questions": random.sample(question_templates, 3),  # Select 3 random questions
        "cross_references": cross_refs
    }


def generate_chapter_overview(book, chapter, verses):
    """Generate an AI-powered overview of the entire chapter"""
    # Special case for Revelation 1
    if book == "Revelation" and chapter == 1:
        return """
    <p><strong>Revelation 1</strong> is the magnificent apocalyptic introduction to the final book of the Bible, often called the <em>Apocalypse</em> (from the Greek ἀποκάλυψις, meaning "unveiling" or "revelation"). Written during the reign of Emperor Domitian (c. 95 CE) when imperial persecution was intensifying, this chapter presents John's vision of the glorified Christ and establishes the divine authority behind the revelations that follow.</p>
        
    <p>The author identifies himself as "John" (verse 1:1, 1:4, 1:9), traditionally understood to be the Apostle John, though some scholars propose it may be another John known as "John the Elder." He was exiled to Patmos, a small rocky island in the Aegean Sea about 37 miles southwest of Miletus, "for the word of God, and for the testimony of Jesus Christ" (verse 9).</p>
        
    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Literary Structure and Context</h4>
        
    <p>Revelation belongs to the apocalyptic genre, characterized by symbolic visions, supernatural beings, cosmic conflict, and the ultimate triumph of good over evil. This literary form was especially meaningful during times of persecution, offering hope through coded imagery that conveyed God's sovereignty over earthly powers.</p>
        
    <p>This chapter establishes several literary patterns that will repeat throughout the book:</p>
    <ul>
        <li>The <strong>number seven</strong> (7 churches, 7 spirits, 7 golden lampstands, 7 stars) symbolizing divine completeness and perfection</li>
        <li><strong>Divine titles</strong> expressing eternal nature ("Alpha and Omega," "First and Last," "Beginning and End")</li>
        <li><strong>Old Testament allusions</strong>, particularly to Daniel, Ezekiel, and Isaiah</li>
        <li><strong>Paradoxical imagery</strong> ("a Lamb as it had been slain" appears later but is foreshadowed by Christ who died yet lives)</li>
    </ul>
        
    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Chapter Structure</h4>
        
    <ol>
        <li><strong>Prologue (Verses 1-3)</strong>: Establishes the divine source and purpose of the revelation, promising blessing to those who read, hear, and keep these prophecies. The phrase "the time is at hand" creates eschatological urgency.</li>
            
        <li><strong>Epistolary Greeting (Verses 4-8)</strong>: John addresses the seven churches of Asia Minor with a trinitarian blessing. This section contains the first of seven beatitudes in Revelation (verse 3) and introduces Christ with titles emphasizing His eternal nature, redemptive work, and future return.</li>
            
        <li><strong>John's Commissioning Vision (Verses 9-16)</strong>: The exiled apostle receives his commission on "the Lord's day" (the first Christian use of this term in literature). Christ appears in transcendent glory among seven golden lampstands, with imagery drawing heavily from Daniel 7:13-14, Daniel 10:5-6, and Ezekiel 1:24-28. Each symbolic element (white hair, flaming eyes, bronze feet, thunderous voice) reveals an aspect of Christ's divine nature and authority.</li>
            
        <li><strong>Christ's Self-Revelation and Command (Verses 17-20)</strong>: After John falls "as dead" before the vision (compare with Isaiah 6:5, Ezekiel 1:28, Daniel 10:8-9), Christ identifies Himself as the eternal living one who conquered death. He commands John to write what he sees, explaining the mystery of the seven stars (angels/messengers of the churches) and seven lampstands (the churches themselves).</li>
    </ol>
        
    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Historical Context</h4>
        
    <p>Emperor Domitian (reigned 81-96 CE) intensified emperor worship throughout the Roman Empire, demanding to be addressed as "Lord and God" (<em>dominus et deus</em>). Christians who refused to participate in imperial cult rituals faced economic marginalization (foreshadowing the "mark of the beast"), social ostracism, and sometimes execution.</p>
        
    <p>The seven churches addressed were located on a Roman postal route in Asia Minor (modern Turkey), each facing unique challenges:</p>
    <ul>
        <li><strong>Ephesus</strong>: A major commercial center with the Temple of Artemis</li>
        <li><strong>Smyrna</strong>: Known for intense emperor worship and Jewish opposition to Christians</li>
        <li><strong>Pergamum</strong>: Center of emperor worship with a large altar to Zeus</li>
        <li><strong>Thyatira</strong>: Known for trade guilds that posed idolatry challenges</li>
        <li><strong>Sardis</strong>: Former capital of Lydia, known for complacency</li>
        <li><strong>Philadelphia</strong>: Smallest city, facing Jewish opposition</li>
        <li><strong>Laodicea</strong>: Wealthy banking center known for lukewarm water supply</li>
    </ul>
        
    <h4 style="color: var(--primary-color); margin-top: 1.5rem;">Theological Significance</h4>
        
    <p>Revelation 1 establishes several profound theological truths:</p>
        
    <ol>
        <li><strong>High Christology</strong>: Christ is portrayed with divine attributes and titles previously reserved for Yahweh in the Old Testament. This establishes one of the earliest and clearest presentations of Christ's deity in Christian literature.</li>
            
        <li><strong>Divine Sovereignty</strong>: Despite the apparent triumph of evil powers (Roman persecution), God remains enthroned and history moves toward His predetermined conclusion.</li>
            
        <li><strong>Trinitarian Framework</strong>: The greeting in verses 4-5 includes all three persons of the Trinity, with the unusual description of the Holy Spirit as "the seven spirits before his throne" (possibly referring to Isaiah 11:2-3 or Zechariah 4:1-10).</li>
            
        <li><strong>Church Identity</strong>: The churches are represented as lampstands with Christ moving among them, suggesting both their mission to bear light and Christ's evaluative presence.</li>
            
        <li><strong>Victory Through Suffering</strong>: John, a "companion in tribulation" (verse 9), writes from exile, establishing that God's revelation comes in the midst of, not despite, suffering. Christ is identified as one who "loved us, and washed us from our sins in his own blood" (verse 5), linking redemption to sacrificial suffering.</li>
    </ol>
        
    <p>When studying Revelation 1, it's essential to approach the text with awareness of its apocalyptic genre, historical context, and symbolic language. The chapter forms the foundation for understanding the entire book, introducing themes, symbols, and theological concepts that will be developed throughout the subsequent visions.</p>
        
    <p>For believers under persecution, whether in the first century or today, this chapter offers the profound assurance that Christ – the Alpha and Omega, the First and Last – remains sovereign over history and present with His church through all tribulations.</p>
    """

    # Simulated chapter overview for other chapters
    themes = [get_theme(v.text.lower()) for v in verses[:5]]  # Sample themes from the first few verses
    unique_themes = list(set(themes))[:3]  # Get up to 3 unique themes

    chapter_type = get_chapter_type(book, chapter)
    time_period = get_time_period(book)
    historical_context = get_historical_context(book)

    overview = f"""
    <p><strong>{book} {chapter}</strong> is a {chapter_type} chapter in the {get_testament_for_book(book)} that explores themes of {', '.join(unique_themes)}.
    Written during {time_period}, this chapter should be understood within its historical context: {historical_context}</p>

    <p>The chapter can be divided into several sections:</p>

    <ol>
        <li><strong>Verses 1-{min(5, len(verses))}</strong>: Introduction and setting the context</li>
        {'<li><strong>Verses 6-' + str(min(12, len(verses))) + '</strong>: Development of key themes</li>' if len(verses) > 5 else ''}
        {'<li><strong>Verses 13-' + str(min(20, len(verses))) + '</strong>: Central message and teachings</li>' if len(verses) > 12 else ''}
        {'<li><strong>Verses ' + str(min(21, len(verses))) + '-' + str(len(verses)) + '</strong>: Conclusion and application</li>' if len(verses) > 20 else ''}
    </ol>

    <p>This chapter is significant because it {get_chapter_significance(book, chapter)}.
    When studying this passage, it's important to consider both its immediate context within {book}
    and its broader place in the scriptural canon.</p>
    """

    return overview


def generate_cross_references(book, chapter, verse, verse_text):
    """Generate simulated cross-references for a verse"""
    # Dictionary of sample cross-references by theme
    theme_references = {
        "salvation": [
            {"book": "John", "chapter": 3, "verse": 16, "context": "God's love and salvation"},
            {"book": "Romans", "chapter": 10, "verse": 9, "context": "Confession and belief for salvation"},
            {"book": "Ephesians", "chapter": 2, "verse": 8, "context": "Salvation by grace through faith"}
        ],
        "faith": [
            {"book": "Hebrews", "chapter": 11, "verse": 1, "context": "Definition of faith"},
            {"book": "James", "chapter": 2, "verse": 17, "context": "Faith and works"},
            {"book": "Romans", "chapter": 1, "verse": 17, "context": "The righteous shall live by faith"}
        ],
        "love": [
            {"book": "1 Corinthians", "chapter": 13, "verse": 4, "context": "Characteristics of love"},
            {"book": "1 John", "chapter": 4, "verse": 8, "context": "God is love"},
            {"book": "John", "chapter": 15, "verse": 13, "context": "Greatest form of love"}
        ],
        "judgment": [
            {"book": "Matthew", "chapter": 25, "verse": 31, "context": "Final judgment"},
            {"book": "Romans", "chapter": 2, "verse": 1, "context": "Judging others"},
            {"book": "Revelation", "chapter": 20, "verse": 12, "context": "Judgment according to deeds"}
        ],
        "creation": [
            {"book": "Genesis", "chapter": 1, "verse": 1, "context": "Creation of heavens and earth"},
            {"book": "Psalm", "chapter": 19, "verse": 1, "context": "Heavens declare God's glory"},
            {"book": "Colossians", "chapter": 1, "verse": 16, "context": "All things created through Christ"}
        ]
    }

    # Identify themes in the verse text
    verse_themes = []
    for theme in theme_references.keys():
        if theme in verse_text or random.random() < 0.2:  # Randomly include some themes
            verse_themes.append(theme)

    # If no themes match, pick a random theme
    if not verse_themes:
        verse_themes = [random.choice(list(theme_references.keys()))]

    # Get references for identified themes
    references = []
    for theme in verse_themes[:2]:  # Limit to two themes
        theme_refs = theme_references[theme]
        for ref in random.sample(theme_refs, min(2, len(theme_refs))):
            # Skip self-references
            if ref["book"] == book and ref["chapter"] == chapter and ref["verse"] == verse:
                continue

            references.append({
                "text": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "url": f"/book/{ref['book']}/chapter/{ref['chapter']}#verse-{ref['verse']}",
                "context": ref["context"]
            })

    # Ensure we have at least one reference
    if not references:
        random_book = random.choice(["Matthew", "John", "Romans", "Psalms", "Proverbs"])
        references.append({
            "text": f"{random_book} 1:1",
            "url": f"/book/{random_book}/chapter/1#verse-1",
            "context": "Related teaching"
        })

    return references


def get_theme(text):
    """Extract a thematic element from text"""
    themes = [
        "redemption", "salvation", "faith", "obedience", "love",
        "judgment", "mercy", "grace", "wisdom", "creation",
        "covenant", "holiness", "righteousness", "truth", "hope",
        "sacrifice", "worship", "prayer", "discipleship", "fellowship"
    ]

    # First check if any themes appear directly in the text
    for theme in themes:
        if theme in text:
            return theme

    # Otherwise return a random theme
    return random.choice(themes)


def get_key_phrase(text):
    """Extract a key phrase from the text"""
    # Split the text into phrases
    phrases = text.replace(".", ". ").replace(";", "; ").replace(":", ": ").split()

    # Select a phrase of 3-5 words if the text is long enough
    if len(phrases) > 5:
        start = random.randint(0, len(phrases) - 5)
        length = random.randint(3, min(5, len(phrases) - start))
        return " ".join(phrases[start:start+length])
    else:
        # If text is short, just return a portion of it
        return text[:min(len(text), 30)]


def get_language_feature(text):
    """Identify a language feature"""
    features = [
        "metaphorical language", "symbolic imagery", "parallelism",
        "rhetorical questioning", "imperative form", "poetic structure",
        "narrative technique", "prophetic language", "didactic teaching",
        "pastoral guidance", "theological explanation", "eschatological reference"
    ]
    return random.choice(features)


def get_literary_device(text):
    """Identify a literary device"""
    devices = [
        "metaphor", "simile", "allusion", "personification", "hyperbole",
        "chiasm", "merism", "synecdoche", "parallelism", "inclusio",
        "rhetorical question", "allegory", "symbolic language", "irony"
    ]

    # Special case for Revelation text which is highly symbolic
    if "throne" in text.lower() or "lamb" in text.lower() or "seal" in text.lower():
        return "apocalyptic symbolism"

    return random.choice(devices)


def get_concept(text):
    """Identify a theological concept"""
    concepts = [
        "divine sovereignty", "human responsibility", "covenant faithfulness",
        "sacrificial atonement", "spiritual renewal", "moral obligation",
        "divine justice", "eschatological hope", "messianic expectation",
        "communal worship", "spiritual discipline", "ethical living",
        "divine revelation", "prophetic fulfillment", "kingdom ethics"
    ]
    return random.choice(concepts)


def get_cultural_element(text):
    """Identify a cultural element"""
    elements = [
        "religious practice", "social custom", "cultural tradition",
        "political structure", "economic system", "family relationship",
        "legal requirement", "worship ritual", "purity regulation",
        "agricultural reference", "military imagery", "architectural feature"
    ]
    return random.choice(elements)


def get_time_period(book):
    """Return the historical time period for a book"""
    time_periods = {
        # Torah
        "Genesis": "the patriarchal period (c. 2000-1700 BCE)",
        "Exodus": "the Egyptian bondage and wilderness wandering (c. 1446-1406 BCE)",
        "Leviticus": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Numbers": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Deuteronomy": "the end of the wilderness wandering (c. 1406 BCE)",

        # Historical books
        "Joshua": "the conquest of Canaan (c. 1406-1375 BCE)",
        "Judges": "the pre-monarchic period (c. 1375-1050 BCE)",
        "Ruth": "the period of the Judges (c. 1100 BCE)",
        "1 Samuel": "the transition to monarchy (c. 1050-1010 BCE)",
        "2 Samuel": "David's reign (c. 1010-970 BCE)",
        "1 Kings": "Solomon's reign and the divided kingdom (c. 970-853 BCE)",
        "2 Kings": "the divided and exilic periods (c. 853-560 BCE)",
        "1 Chronicles": "the post-exilic reflection on David's reign (c. 430-400 BCE)",
        "2 Chronicles": "the post-exilic reflection on the monarchy (c. 430-400 BCE)",
        "Ezra": "the post-exilic return (c. 458-440 BCE)",
        "Nehemiah": "the rebuilding of Jerusalem (c. 445-420 BCE)",
        "Esther": "the Persian period (c. 483-473 BCE)",

        # Wisdom literature
        "Job": "the patriarchal period (literary composition later)",
        "Psalms": "various periods (c. 1000-400 BCE)",
        "Proverbs": "primarily Solomon's reign (c. 970-930 BCE)",
        "Ecclesiastes": "likely Solomon's reign (c. 970-930 BCE)",
        "Song of Solomon": "Solomon's reign (c. 970-930 BCE)",

        # Major Prophets
        "Isaiah": "the Assyrian and pre-exilic periods (c. 740-680 BCE)",
        "Jeremiah": "the final years of Judah and early exile (c. 627-580 BCE)",
        "Lamentations": "just after Jerusalem's fall (c. 586 BCE)",
        "Ezekiel": "the Babylonian exile (c. 593-570 BCE)",
        "Daniel": "the Babylonian and Persian periods (c. 605-530 BCE)",

        # Minor Prophets
        "Hosea": "the final years of the northern kingdom (c. 755-710 BCE)",
        "Joel": "possibly post-exilic period (uncertain date)",
        "Amos": "the prosperous period of Jeroboam II (c. 760-750 BCE)",
        "Obadiah": "possibly after Jerusalem's fall (c. 586 BCE)",
        "Jonah": "the Assyrian period (c. 780-750 BCE)",
        "Micah": "the late 8th century BCE (c. 735-700 BCE)",
        "Nahum": "shortly before Nineveh's fall (c. 630-610 BCE)",
        "Habakkuk": "the neo-Babylonian rise to power (c. 605-597 BCE)",
        "Zephaniah": "during Josiah's reign (c. 640-609 BCE)",
        "Haggai": "the early post-exilic period (c. 520 BCE)",
        "Zechariah": "the early post-exilic period (c. 520-480 BCE)",
        "Malachi": "the mid-5th century BCE (c. 460-430 BCE)",

        # Gospels and Acts
        "Matthew": "the late first century CE (c. 80-90 CE)",
        "Mark": "the mid first century CE (c. 65-70 CE)",
        "Luke": "the late first century CE (c. 80-85 CE)",
        "John": "the late first century CE (c. 90-95 CE)",
        "Acts": "the late first century CE (c. 80-85 CE)",

        # Pauline Epistles
        "Romans": "Paul's third missionary journey (c. 57 CE)",
        "1 Corinthians": "Paul's third missionary journey (c. 55 CE)",
        "2 Corinthians": "Paul's third missionary journey (c. 55-56 CE)",
        "Galatians": "either before or after the Jerusalem Council (c. 48-55 CE)",
        "Ephesians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Philippians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Colossians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "1 Thessalonians": "Paul's second missionary journey (c. 50-51 CE)",
        "2 Thessalonians": "shortly after 1 Thessalonians (c. 50-51 CE)",
        "1 Timothy": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "2 Timothy": "during Paul's second Roman imprisonment (c. 66-67 CE)",
        "Titus": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "Philemon": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Hebrews": "before Jerusalem's destruction (c. 60-70 CE)",

        # General Epistles
        "James": "the early church period (c. 45-50 CE)",
        "1 Peter": "during Nero's persecution (c. 62-64 CE)",
        "2 Peter": "shortly before Peter's death (c. 65-68 CE)",
        "1 John": "the late first century CE (c. 85-95 CE)",
        "2 John": "the late first century CE (c. 85-95 CE)",
        "3 John": "the late first century CE (c. 85-95 CE)",
        "Jude": "the late first century CE (c. 65-80 CE)",

        # Apocalyptic
        "Revelation": "the end of the first century CE (c. 95 CE)"
    }

    return time_periods.get(book, "the biblical period")


def get_historical_context(book):
    """Return historical context for a book"""
    historical_contexts = {
        # Torah
        "Genesis": "The ancient Near Eastern world was filled with competing creation narratives and flood stories.",
        "Exodus": "Egypt was the dominant superpower with a complex polytheistic religion and a god-king pharaoh.",
        "Leviticus": "The ritual systems addressed were designed to distinguish Israel from surrounding Canaanite practices.",
        "Numbers": "The wilderness journey occurred between Egypt's dominance and the Canaanite tribal systems.",
        "Deuteronomy": "Moses delivered these speeches as Israel prepared to enter a land filled with different Canaanite city-states.",

        # Historical books
        "Joshua": "Canaan was fragmented into city-states with various tribal alliances and religious practices.",
        "Judges": "Without central leadership, Israel faced constant threats from surrounding peoples like the Philistines and Midianites.",
        "Ruth": "During the tribal confederacy period, local customs and family laws were paramount for survival.",
        "1 Samuel": "Israel transitioned from tribal confederacy to monarchy while facing Philistine military pressure.",
        "2 Samuel": "David established Jerusalem as the capital during a time of regional power vacuum.",
        "1 Kings": "Solomon's reign represented Israel's golden age, with international trade and diplomatic relations.",
        "2 Kings": "The divided kingdoms faced threats from rising empires: Assyria and later Babylon.",
        "1 Chronicles": "Written after exile to reestablish national identity through connection to David's lineage.",
        "2 Chronicles": "Written to remind returning exiles of their temple-centered worship and Davidic heritage.",
        "Ezra": "The Persian Empire allowed religious freedom while maintaining political control.",
        "Nehemiah": "Persian authorities permitted Jerusalem's rebuilding under local leadership with imperial oversight.",
        "Esther": "Jews in diaspora faced both integration opportunities and threats within the vast Persian Empire.",

        # Wisdom literature
        "Job": "Ancient wisdom traditions often wrestled with the problem of suffering and divine justice.",
        "Psalms": "Temple worship utilized these compositions across various periods of Israel's history.",
        "Proverbs": "Ancient Near Eastern wisdom literature was common in royal courts for training officials.",
        "Ecclesiastes": "Royal wisdom reflections paralleled other ancient Near Eastern philosophical works.",
        "Song of Solomon": "Ancient Near Eastern love poetry often used agricultural and royal imagery.",

        # Major Prophets
        "Isaiah": "Addressed Judah during Assyria's rise, Babylon's threat, and anticipated restoration.",
        "Jeremiah": "Prophesied during Judah's final years as Babylon became the dominant power.",
        "Lamentations": "Written amid the devastating aftermath of Jerusalem's destruction by Babylon.",
        "Ezekiel": "Ministered to exiles in Babylon with visions of God's glory and future restoration.",
        "Daniel": "Demonstrates faithful living under foreign rule during the Babylonian and Persian empires.",

        # Minor Prophets
        "Hosea": "Israel faced imminent threat from Assyria while engaging in Canaanite religious syncretism.",
        "Joel": "Addressed a community devastated by natural disaster as a sign of divine judgment.",
        "Amos": "Economic prosperity masked serious social injustice and religious hypocrisy.",
        "Obadiah": "Edom's betrayal of Judah during Jerusalem's fall heightened ancient tribal hostilities.",
        "Jonah": "Nineveh was the capital of the feared Assyrian Empire, Israel's enemy.",
        "Micah": "Rural communities suffered while urban elites prospered during Assyria's regional dominance.",
        "Nahum": "Nineveh's anticipated fall would end a century of Assyrian oppression.",
        "Habakkuk": "Babylon's rise to power raised questions about God using pagan nations as instruments.",
        "Zephaniah": "Josiah's reforms occurred against the backdrop of Assyria's decline and Babylon's rise.",
        "Haggai": "Economic hardship and political uncertainty complicated the returning exiles' rebuilding efforts.",
        "Zechariah": "Persian support for temple rebuilding came with continued imperial control.",
        "Malachi": "Post-exilic community struggled with religious apathy and intermarriage challenges.",

        # Gospels and Acts
        "Matthew": "Written when Christianity was separating from Judaism following Jerusalem's destruction.",
        "Mark": "Composed during or just after Nero's persecution when eyewitnesses were disappearing.",
        "Luke": "Written when Christians needed to understand their place in the Roman world.",
        "John": "Addressed late first-century challenges from both Judaism and emerging Gnostic thought.",
        "Acts": "Chronicles Christianity's spread across the Roman Empire despite official and unofficial opposition.",

        # Pauline Epistles
        "Romans": "Christians in Rome navigated tensions between Jewish and Gentile believers under imperial watch.",
        "1 Corinthians": "The church existed in a prosperous, cosmopolitan, morally permissive Roman colony.",
        "2 Corinthians": "Paul defended his apostleship against challenges in a culture valuing rhetorical prowess.",
        "Galatians": "Gentile believers faced pressure to adopt Jewish practices for full acceptance.",
        "Ephesians": "Ephesus was a major center of pagan worship, particularly of the goddess Artemis.",
        "Philippians": "The church in this Roman colony maintained partnership with Paul despite his imprisonment.",
        "Colossians": "Syncretistic philosophy threatened to compromise the sufficiency of Christ.",
        "1 Thessalonians": "New believers faced persecution from both Jewish opposition and pagan neighbors.",
        "2 Thessalonians": "Confusion about Christ's return caused some believers to abandon daily responsibilities.",
        "1 Timothy": "False teaching in Ephesus required organizational and doctrinal clarification.",
        "2 Timothy": "Paul's final imprisonment occurred during intensified persecution under Nero.",
        "Titus": "Cretan culture's negative reputation required special attention to Christian character.",
        "Philemon": "Roman slavery was addressed through Christian principles without direct confrontation.",
        "Hebrews": "Jewish Christians faced persecution pressure to return to Judaism's legal protections.",

        # General Epistles
        "James": "Early Jewish believers struggled to live out faith amid economic hardship and discrimination.",
        "1 Peter": "Christians throughout Asia Minor faced growing social hostility and potential persecution.",
        "2 Peter": "False teachers exploited Christian freedom for immoral purposes and denied divine judgment.",
        "1 John": "Early Gnostic ideas threatened the understanding of Christ's incarnation and redemption.",
        "2 John": "Itinerant teachers required careful vetting as false teaching spread through hospitality networks.",
        "3 John": "Power struggles in local churches complicated missionary support and fellowship.",
        "Jude": "Libertine teaching undermined moral standards by distorting grace.",

        # Apocalyptic
        "Revelation": "Emperor worship intensified under Domitian, pressuring Christians to compromise their exclusive loyalty to Christ."
    }

    return historical_contexts.get(book, "This text emerged within the historical context of ancient religious traditions.")


def get_chapter_type(book, chapter):
    """Identify the type of chapter"""
    # Simplified mapping of books to primary genre
    book_genres = {
        # Torah
        "Genesis": "narrative",
        "Exodus": "narrative with legal sections",
        "Leviticus": "legal and ritual",
        "Numbers": "mixed narrative and legal",
        "Deuteronomy": "sermonic and legal",

        # Historical
        "Joshua": "historical narrative",
        "Judges": "cyclical narrative",
        "Ruth": "historical narrative",
        "1 Samuel": "biographical narrative",
        "2 Samuel": "biographical narrative",
        "1 Kings": "historical narrative",
        "2 Kings": "historical narrative",
        "1 Chronicles": "historical and genealogical",
        "2 Chronicles": "historical narrative",
        "Ezra": "historical narrative",
        "Nehemiah": "historical memoir",
        "Esther": "historical narrative",

        # Wisdom
        "Job": "wisdom dialogue",
        "Psalms": "poetic and liturgical",
        "Proverbs": "wisdom sayings",
        "Ecclesiastes": "philosophical reflection",
        "Song of Solomon": "poetic love song",

        # Prophetic
        "Isaiah": "prophetic oracle",
        "Jeremiah": "prophetic oracle",
        "Lamentations": "funeral dirge",
        "Ezekiel": "prophetic vision",
        "Daniel": "apocalyptic and narrative",
        "Hosea": "prophetic oracle",
        "Joel": "prophetic oracle",
        "Amos": "prophetic oracle",
        "Obadiah": "prophetic oracle",
        "Jonah": "prophetic narrative",
        "Micah": "prophetic oracle",
        "Nahum": "prophetic oracle",
        "Habakkuk": "prophetic dialogue",
        "Zephaniah": "prophetic oracle",
        "Haggai": "prophetic oracle",
        "Zechariah": "prophetic vision",
        "Malachi": "prophetic disputation",

        # Gospels
        "Matthew": "biographical gospel",
        "Mark": "action-oriented gospel",
        "Luke": "historical gospel",
        "John": "theological gospel",

        # Acts
        "Acts": "historical narrative",

        # Epistles
        "Romans": "theological epistle",
        "1 Corinthians": "pastoral epistle",
        "2 Corinthians": "apologetic epistle",
        "Galatians": "polemical epistle",
        "Ephesians": "theological epistle",
        "Philippians": "friendship epistle",
        "Colossians": "christological epistle",
        "1 Thessalonians": "eschatological epistle",
        "2 Thessalonians": "eschatological epistle",
        "1 Timothy": "pastoral epistle",
        "2 Timothy": "pastoral epistle",
        "Titus": "pastoral epistle",
        "Philemon": "personal epistle",
        "Hebrews": "homiletical epistle",
        "James": "wisdom epistle",
        "1 Peter": "pastoral epistle",
        "2 Peter": "polemical epistle",
        "1 John": "theological epistle",
        "2 John": "pastoral epistle",
        "3 John": "personal epistle",
        "Jude": "polemical epistle",

        # Apocalyptic
        "Revelation": "apocalyptic vision"
    }

    # Special cases for specific chapters
    special_chapters = {
        ("Genesis", 1): "creation account",
        ("Genesis", 3): "fall narrative",
        ("Exodus", 20): "legal covenant",
        ("Leviticus", 16): "ritual instruction",
        ("Deuteronomy", 28): "covenant blessing and curse",
        ("Joshua", 1): "commissioning narrative",
        ("Judges", 2): "paradigmatic narrative",
        ("1 Samuel", 16): "anointing narrative",
        ("2 Samuel", 7): "covenant narrative",
        ("Psalms", 1): "wisdom psalm",
        ("Psalms", 22): "lament psalm",
        ("Psalms", 23): "shepherd psalm",
        ("Psalms", 24): "royal psalm",
        ("Psalms", 25): "prayer psalm",
        ("Psalms", 26): "trust psalm",
        ("Psalms", 27): "hope psalm",
        ("Psalms", 28): "deliverance psalm",
        ("Psalms", 29): "praise psalm",
        ("Psalms", 30): "joy psalm",
        ("Psalms", 31): "suffering psalm",
        ("Psalms", 32): "wisdom psalm",
        ("Psalms", 33): "praise psalm",
        ("Psalms", 34): "praise psalm",
        ("Psalms", 35): "praise psalm",
        ("Psalms", 36): "praise psalm"
    }

def generate_chapter_overview(book, chapter, verses):
    """Generate an AI-powered overview of the entire chapter"""
    # Simulated chapter overview
    themes = [get_theme(v.text.lower()) for v in verses[:5]]  # Sample themes from the first few verses
    unique_themes = list(set(themes))[:3]  # Get up to 3 unique themes

    chapter_type = get_chapter_type(book, chapter)
    time_period = get_time_period(book)
    historical_context = get_historical_context(book)

    overview = f"""
    <p><strong>{book} {chapter}</strong> is a {chapter_type} chapter in the {get_testament_for_book(book)} that explores themes of {', '.join(unique_themes)}.
    Written during {time_period}, this chapter should be understood within its historical context: {historical_context}</p>

    <p>The chapter can be divided into several sections:</p>

    <ol>
        <li><strong>Verses 1-{min(5, len(verses))}</strong>: Introduction and setting the context</li>
        {'<li><strong>Verses 6-' + str(min(12, len(verses))) + '</strong>: Development of key themes</li>' if len(verses) > 5 else ''}
        {'<li><strong>Verses 13-' + str(min(20, len(verses))) + '</strong>: Central message and teachings</li>' if len(verses) > 12 else ''}
        {'<li><strong>Verses ' + str(min(21, len(verses))) + '-' + str(len(verses)) + '</strong>: Conclusion and application</li>' if len(verses) > 20 else ''}
    </ol>

    <p>This chapter is significant because it {get_chapter_significance(book, chapter)}.
    When studying this passage, it's important to consider both its immediate context within {book}
    and its broader place in the scriptural canon.</p>
    """

    return overview


def generate_cross_references(book, chapter, verse, verse_text):
    """Generate simulated cross-references for a verse"""
    # Dictionary of sample cross-references by theme
    theme_references = {
        "salvation": [
            {"book": "John", "chapter": 3, "verse": 16, "context": "God's love and salvation"},
            {"book": "Romans", "chapter": 10, "verse": 9, "context": "Confession and belief for salvation"},
            {"book": "Ephesians", "chapter": 2, "verse": 8, "context": "Salvation by grace through faith"}
        ],
        "faith": [
            {"book": "Hebrews", "chapter": 11, "verse": 1, "context": "Definition of faith"},
            {"book": "James", "chapter": 2, "verse": 17, "context": "Faith and works"},
            {"book": "Romans", "chapter": 1, "verse": 17, "context": "The righteous shall live by faith"}
        ],
        "love": [
            {"book": "1 Corinthians", "chapter": 13, "verse": 4, "context": "Characteristics of love"},
            {"book": "1 John", "chapter": 4, "verse": 8, "context": "God is love"},
            {"book": "John", "chapter": 15, "verse": 13, "context": "Greatest form of love"}
        ],
        "judgment": [
            {"book": "Matthew", "chapter": 25, "verse": 31, "context": "Final judgment"},
            {"book": "Romans", "chapter": 2, "verse": 1, "context": "Judging others"},
            {"book": "Revelation", "chapter": 20, "verse": 12, "context": "Judgment according to deeds"}
        ],
        "creation": [
            {"book": "Genesis", "chapter": 1, "verse": 1, "context": "Creation of heavens and earth"},
            {"book": "Psalm", "chapter": 19, "verse": 1, "context": "Heavens declare God's glory"},
            {"book": "Colossians", "chapter": 1, "verse": 16, "context": "All things created through Christ"}
        ]
    }

    # Identify themes in the verse text
    verse_themes = []
    for theme in theme_references.keys():
        if theme in verse_text or random.random() < 0.2:  # Randomly include some themes
            verse_themes.append(theme)

    # If no themes match, pick a random theme
    if not verse_themes:
        verse_themes = [random.choice(list(theme_references.keys()))]

    # Get references for identified themes
    references = []
    for theme in verse_themes[:2]:  # Limit to two themes
        theme_refs = theme_references[theme]
        for ref in random.sample(theme_refs, min(2, len(theme_refs))):
            # Skip self-references
            if ref["book"] == book and ref["chapter"] == chapter and ref["verse"] == verse:
                continue

            references.append({
                "text": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "url": f"/book/{ref['book']}/chapter/{ref['chapter']}#verse-{ref['verse']}",
                "context": ref["context"]
            })

    # Ensure we have at least one reference
    if not references:
        random_book = random.choice(["Matthew", "John", "Romans", "Psalms", "Proverbs"])
        references.append({
            "text": f"{random_book} 1:1",
            "url": f"/book/{random_book}/chapter/1#verse-1",
            "context": "Related teaching"
        })

    return references


def get_theme(text):
    """Extract a thematic element from text"""
    themes = [
        "redemption", "salvation", "faith", "obedience", "love",
        "judgment", "mercy", "grace", "wisdom", "creation",
        "covenant", "holiness", "righteousness", "truth", "hope",
        "sacrifice", "worship", "prayer", "discipleship", "fellowship"
    ]

    # First check if any themes appear directly in the text
    for theme in themes:
        if theme in text:
            return theme

    # Otherwise return a random theme
    return random.choice(themes)


def get_key_phrase(text):
    """Extract a key phrase from the text"""
    # Split the text into phrases
    phrases = text.replace(".", ". ").replace(";", "; ").replace(":", ": ").split()

    # Select a phrase of 3-5 words if the text is long enough
    if len(phrases) > 5:
        start = random.randint(0, len(phrases) - 5)
        length = random.randint(3, min(5, len(phrases) - start))
        return " ".join(phrases[start:start+length])
    else:
        # If text is short, just return a portion of it
        return text[:min(len(text), 30)]


def get_language_feature(text):
    """Identify a language feature"""
    features = [
        "metaphorical language", "symbolic imagery", "parallelism",
        "rhetorical questioning", "imperative form", "poetic structure",
        "narrative technique", "prophetic language", "didactic teaching",
        "pastoral guidance", "theological explanation", "eschatological reference"
    ]
    return random.choice(features)


def get_literary_device(text):
    """Identify a literary device"""
    devices = [
        "metaphor", "simile", "allusion", "personification", "hyperbole",
        "chiasm", "merism", "synecdoche", "parallelism", "inclusio",
        "rhetorical question", "allegory", "symbolic language", "irony"
    ]
    return random.choice(devices)


def get_concept(text):
    """Identify a theological concept"""
    concepts = [
        "divine sovereignty", "human responsibility", "covenant faithfulness",
        "sacrificial atonement", "spiritual renewal", "moral obligation",
        "divine justice", "eschatological hope", "messianic expectation",
        "communal worship", "spiritual discipline", "ethical living",
        "divine revelation", "prophetic fulfillment", "kingdom ethics"
    ]
    return random.choice(concepts)


def get_cultural_element(text):
    """Identify a cultural element"""
    elements = [
        "religious practice", "social custom", "cultural tradition",
        "political structure", "economic system", "family relationship",
        "legal requirement", "worship ritual", "purity regulation",
        "agricultural reference", "military imagery", "architectural feature"
    ]
    return random.choice(elements)


def get_time_period(book):
    """Return the historical time period for a book"""
    time_periods = {
        # Torah
        "Genesis": "the patriarchal period (c. 2000-1700 BCE)",
        "Exodus": "the Egyptian bondage and wilderness wandering (c. 1446-1406 BCE)",
        "Leviticus": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Numbers": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Deuteronomy": "the end of the wilderness wandering (c. 1406 BCE)",

        # Historical books
        "Joshua": "the conquest of Canaan (c. 1406-1375 BCE)",
        "Judges": "the pre-monarchic period (c. 1375-1050 BCE)",
        "Ruth": "the period of the Judges (c. 1100 BCE)",
        "1 Samuel": "the transition to monarchy (c. 1050-1010 BCE)",
        "2 Samuel": "David's reign (c. 1010-970 BCE)",
        "1 Kings": "Solomon's reign and the divided kingdom (c. 970-853 BCE)",
        "2 Kings": "the divided and exilic periods (c. 853-560 BCE)",
        "1 Chronicles": "the post-exilic reflection on David's reign (c. 430-400 BCE)",
        "2 Chronicles": "the post-exilic reflection on the monarchy (c. 430-400 BCE)",
        "Ezra": "the post-exilic return (c. 458-440 BCE)",
        "Nehemiah": "the rebuilding of Jerusalem (c. 445-420 BCE)",
        "Esther": "the Persian period (c. 483-473 BCE)",

        # Wisdom literature
        "Job": "the patriarchal period (literary composition later)",
        "Psalms": "various periods (c. 1000-400 BCE)",
        "Proverbs": "primarily Solomon's reign (c. 970-930 BCE)",
        "Ecclesiastes": "likely Solomon's reign (c. 970-930 BCE)",
        "Song of Solomon": "Solomon's reign (c. 970-930 BCE)",

        # Major Prophets
        "Isaiah": "the Assyrian and pre-exilic periods (c. 740-680 BCE)",
        "Jeremiah": "the final years of Judah and early exile (c. 627-580 BCE)",
        "Lamentations": "just after Jerusalem's fall (c. 586 BCE)",
        "Ezekiel": "the Babylonian exile (c. 593-570 BCE)",
        "Daniel": "the Babylonian and Persian periods (c. 605-530 BCE)",

        # Minor Prophets
        "Hosea": "the final years of the northern kingdom (c. 755-710 BCE)",
        "Joel": "possibly post-exilic period (uncertain date)",
        "Amos": "the prosperous period of Jeroboam II (c. 760-750 BCE)",
        "Obadiah": "possibly after Jerusalem's fall (c. 586 BCE)",
        "Jonah": "the Assyrian period (c. 780-750 BCE)",
        "Micah": "the late 8th century BCE (c. 735-700 BCE)",
        "Nahum": "shortly before Nineveh's fall (c. 630-610 BCE)",
        "Habakkuk": "the neo-Babylonian rise to power (c. 605-597 BCE)",
        "Zephaniah": "during Josiah's reign (c. 640-609 BCE)",
        "Haggai": "the early post-exilic period (c. 520 BCE)",
        "Zechariah": "the early post-exilic period (c. 520-480 BCE)",
        "Malachi": "the mid-5th century BCE (c. 460-430 BCE)",

        # Gospels and Acts
        "Matthew": "the late first century CE (c. 80-90 CE)",
        "Mark": "the mid first century CE (c. 65-70 CE)",
        "Luke": "the late first century CE (c. 80-85 CE)",
        "John": "the late first century CE (c. 90-95 CE)",
        "Acts": "the late first century CE (c. 80-85 CE)",

        # Pauline Epistles
        "Romans": "Paul's third missionary journey (c. 57 CE)",
        "1 Corinthians": "Paul's third missionary journey (c. 55 CE)",
        "2 Corinthians": "Paul's third missionary journey (c. 55-56 CE)",
        "Galatians": "either before or after the Jerusalem Council (c. 48-55 CE)",
        "Ephesians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Philippians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Colossians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "1 Thessalonians": "Paul's second missionary journey (c. 50-51 CE)",
        "2 Thessalonians": "shortly after 1 Thessalonians (c. 50-51 CE)",
        "1 Timothy": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "2 Timothy": "during Paul's second Roman imprisonment (c. 66-67 CE)",
        "Titus": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "Philemon": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Hebrews": "before Jerusalem's destruction (c. 60-70 CE)",

        # General Epistles
        "James": "the early church period (c. 45-50 CE)",
        "1 Peter": "during Nero's persecution (c. 62-64 CE)",
        "2 Peter": "shortly before Peter's death (c. 65-68 CE)",
        "1 John": "the late first century CE (c. 85-95 CE)",
        "2 John": "the late first century CE (c. 85-95 CE)",
        "3 John": "the late first century CE (c. 85-95 CE)",
        "Jude": "the late first century CE (c. 65-80 CE)",

        # Apocalyptic
        "Revelation": "the end of the first century CE (c. 95 CE)"
    }

    return time_periods.get(book, "the biblical period")


def get_historical_context(book):
    """Return historical context for a book"""
    historical_contexts = {
        # Torah
        "Genesis": "The ancient Near Eastern world was filled with competing creation narratives and flood stories.",
        "Exodus": "Egypt was the dominant superpower with a complex polytheistic religion and a god-king pharaoh.",
        "Leviticus": "The ritual systems addressed were designed to distinguish Israel from surrounding Canaanite practices.",
        "Numbers": "The wilderness journey occurred between Egypt's dominance and the Canaanite tribal systems.",
        "Deuteronomy": "Moses delivered these speeches as Israel prepared to enter a land filled with different Canaanite city-states.",

        # Historical books
        "Joshua": "Canaan was fragmented into city-states with various tribal alliances and religious practices.",
        "Judges": "Without central leadership, Israel faced constant threats from surrounding peoples like the Philistines and Midianites.",
        "Ruth": "During the tribal confederacy period, local customs and family laws were paramount for survival.",
        "1 Samuel": "Israel transitioned from tribal confederacy to monarchy while facing Philistine military pressure.",
        "2 Samuel": "David established Jerusalem as the capital during a time of regional power vacuum.",
        "1 Kings": "Solomon's reign represented Israel's golden age, with international trade and diplomatic relations.",
        "2 Kings": "The divided kingdoms faced threats from rising empires: Assyria and later Babylon.",
        "1 Chronicles": "Written after exile to reestablish national identity through connection to David's lineage.",
        "2 Chronicles": "Written to remind returning exiles of their temple-centered worship and Davidic heritage.",
        "Ezra": "The Persian Empire allowed religious freedom while maintaining political control.",
        "Nehemiah": "Persian authorities permitted Jerusalem's rebuilding under local leadership with imperial oversight.",
        "Esther": "Jews in diaspora faced both integration opportunities and threats within the vast Persian Empire.",

        # Wisdom literature
        "Job": "Ancient wisdom traditions often wrestled with the problem of suffering and divine justice.",
        "Psalms": "Temple worship utilized these compositions across various periods of Israel's history.",
        "Proverbs": "Ancient Near Eastern wisdom literature was common in royal courts for training officials.",
        "Ecclesiastes": "Royal wisdom reflections paralleled other ancient Near Eastern philosophical works.",
        "Song of Solomon": "Ancient Near Eastern love poetry often used agricultural and royal imagery.",

        # Major Prophets
        "Isaiah": "Addressed Judah during Assyria's rise, Babylon's threat, and anticipated restoration.",
        "Jeremiah": "Prophesied during Judah's final years as Babylon became the dominant power.",
        "Lamentations": "Written amid the devastating aftermath of Jerusalem's destruction by Babylon.",
        "Ezekiel": "Ministered to exiles in Babylon with visions of God's glory and future restoration.",
        "Daniel": "Demonstrates faithful living under foreign rule during the Babylonian and Persian empires.",

        # Minor Prophets
        "Hosea": "Israel faced imminent threat from Assyria while engaging in Canaanite religious syncretism.",
        "Joel": "Addressed a community devastated by natural disaster as a sign of divine judgment.",
        "Amos": "Economic prosperity masked serious social injustice and religious hypocrisy.",
        "Obadiah": "Edom's betrayal of Judah during Jerusalem's fall heightened ancient tribal hostilities.",
        "Jonah": "Nineveh was the capital of the feared Assyrian Empire, Israel's enemy.",
        "Micah": "Rural communities suffered while urban elites prospered during Assyria's regional dominance.",
        "Nahum": "Nineveh's anticipated fall would end a century of Assyrian oppression.",
        "Habakkuk": "Babylon's rise to power raised questions about God using pagan nations as instruments.",
        "Zephaniah": "Josiah's reforms occurred against the backdrop of Assyria's decline and Babylon's rise.",
        "Haggai": "Economic hardship and political uncertainty complicated the returning exiles' rebuilding efforts.",
        "Zechariah": "Persian support for temple rebuilding came with continued imperial control.",
        "Malachi": "Post-exilic community struggled with religious apathy and intermarriage challenges.",

        # Gospels and Acts
        "Matthew": "Written when Christianity was separating from Judaism following Jerusalem's destruction.",
        "Mark": "Composed during or just after Nero's persecution when eyewitnesses were disappearing.",
        "Luke": "Written when Christians needed to understand their place in the Roman world.",
        "John": "Addressed late first-century challenges from both Judaism and emerging Gnostic thought.",
        "Acts": "Chronicles Christianity's spread across the Roman Empire despite official and unofficial opposition.",

        # Pauline Epistles
        "Romans": "Christians in Rome navigated tensions between Jewish and Gentile believers under imperial watch.",
        "1 Corinthians": "The church existed in a prosperous, cosmopolitan, morally permissive Roman colony.",
        "2 Corinthians": "Paul defended his apostleship against challenges in a culture valuing rhetorical prowess.",
        "Galatians": "Gentile believers faced pressure to adopt Jewish practices for full acceptance.",
        "Ephesians": "Ephesus was a major center of pagan worship, particularly of the goddess Artemis.",
        "Philippians": "The church in this Roman colony maintained partnership with Paul despite his imprisonment.",
        "Colossians": "Syncretistic philosophy threatened to compromise the sufficiency of Christ.",
        "1 Thessalonians": "New believers faced persecution from both Jewish opposition and pagan neighbors.",
        "2 Thessalonians": "Confusion about Christ's return caused some believers to abandon daily responsibilities.",
        "1 Timothy": "False teaching in Ephesus required organizational and doctrinal clarification.",
        "2 Timothy": "Paul's final imprisonment occurred during intensified persecution under Nero.",
        "Titus": "Cretan culture's negative reputation required special attention to Christian character.",
        "Philemon": "Roman slavery was addressed through Christian principles without direct confrontation.",
        "Hebrews": "Jewish Christians faced persecution pressure to return to Judaism's legal protections.",

        # General Epistles
        "James": "Early Jewish believers struggled to live out faith amid economic hardship and discrimination.",
        "1 Peter": "Christians throughout Asia Minor faced growing social hostility and potential persecution.",
        "2 Peter": "False teachers exploited Christian freedom for immoral purposes and denied divine judgment.",
        "1 John": "Early Gnostic ideas threatened the understanding of Christ's incarnation and redemption.",
        "2 John": "Itinerant teachers required careful vetting as false teaching spread through hospitality networks.",
        "3 John": "Power struggles in local churches complicated missionary support and fellowship.",
        "Jude": "Libertine teaching undermined moral standards by distorting grace.",

        # Apocalyptic
        "Revelation": "Emperor worship intensified under Domitian, pressuring Christians to compromise their exclusive loyalty to Christ."
    }

    return historical_contexts.get(book, "This text emerged within the historical context of ancient religious traditions.")


def get_chapter_type(book, chapter):
    """Identify the type of chapter"""
    # Simplified mapping of books to primary genre
    book_genres = {
        # Torah
        "Genesis": "narrative",
        "Exodus": "narrative with legal sections",
        "Leviticus": "legal and ritual",
        "Numbers": "mixed narrative and legal",
        "Deuteronomy": "sermonic and legal",

        # Historical
        "Joshua": "historical narrative",
        "Judges": "cyclical narrative",
        "Ruth": "historical narrative",
        "1 Samuel": "biographical narrative",
        "2 Samuel": "biographical narrative",
        "1 Kings": "historical narrative",
        "2 Kings": "historical narrative",
        "1 Chronicles": "historical and genealogical",
        "2 Chronicles": "historical narrative",
        "Ezra": "historical narrative",
        "Nehemiah": "historical memoir",
        "Esther": "historical narrative",

        # Wisdom
        "Job": "wisdom dialogue",
        "Psalms": "poetic and liturgical",
        "Proverbs": "wisdom sayings",
        "Ecclesiastes": "philosophical reflection",
        "Song of Solomon": "poetic love song",

        # Prophetic
        "Isaiah": "prophetic oracle",
        "Jeremiah": "prophetic oracle",
        "Lamentations": "funeral dirge",
        "Ezekiel": "prophetic vision",
        "Daniel": "apocalyptic and narrative",
        "Hosea": "prophetic oracle",
        "Joel": "prophetic oracle",
        "Amos": "prophetic oracle",
        "Obadiah": "prophetic oracle",
        "Jonah": "prophetic narrative",
        "Micah": "prophetic oracle",
        "Nahum": "prophetic oracle",
        "Habakkuk": "prophetic dialogue",
        "Zephaniah": "prophetic oracle",
        "Haggai": "prophetic oracle",
        "Zechariah": "prophetic vision",
        "Malachi": "prophetic disputation",

        # Gospels
        "Matthew": "biographical gospel",
        "Mark": "action-oriented gospel",
        "Luke": "historical gospel",
        "John": "theological gospel",

        # Acts
        "Acts": "historical narrative",

        # Epistles
        "Romans": "theological epistle",
        "1 Corinthians": "pastoral epistle",
        "2 Corinthians": "apologetic epistle",
        "Galatians": "polemical epistle",
        "Ephesians": "theological epistle",
        "Philippians": "friendship epistle",
        "Colossians": "christological epistle",
        "1 Thessalonians": "eschatological epistle",
        "2 Thessalonians": "eschatological epistle",
        "1 Timothy": "pastoral epistle",
        "2 Timothy": "pastoral epistle",
        "Titus": "pastoral epistle",
        "Philemon": "personal epistle",
        "Hebrews": "homiletical epistle",
        "James": "wisdom epistle",
        "1 Peter": "pastoral epistle",
        "2 Peter": "polemical epistle",
        "1 John": "theological epistle",
        "2 John": "pastoral epistle",
        "3 John": "personal epistle",
        "Jude": "polemical epistle",

        # Apocalyptic
        "Revelation": "apocalyptic vision"
    }

    # Special cases for specific chapters
    special_chapters = {
        ("Genesis", 1): "creation account",
        ("Genesis", 3): "fall narrative",
        ("Exodus", 20): "legal covenant",
        ("Leviticus", 16): "ritual instruction",
        ("Deuteronomy", 28): "covenant blessing and curse",
        ("Joshua", 1): "commissioning narrative",
        ("Judges", 2): "paradigmatic narrative",
        ("1 Samuel", 16): "anointing narrative",
        ("2 Samuel", 7): "covenant narrative",
        ("Psalms", 1): "wisdom psalm",
        ("Psalms", 22): "lament psalm",
        ("Psalms", 23): "trust psalm",
        ("Isaiah", 53): "suffering servant oracle",
        ("Matthew", 5): "ethical teaching",
        ("John", 1): "theological prologue",
        ("Romans", 8): "theological exposition",
        ("1 Corinthians", 13): "hymn to love",
        ("Revelation", 1): "apocalyptic vision"
    }

    # Check if this is a special chapter
    if (book, chapter) in special_chapters:
        return special_chapters[(book, chapter)]

    # Otherwise return the general book genre
    return book_genres.get(book, "scriptural")


def get_testament_for_book(book):
    """Determine if a book is in the Old or New Testament"""
    old_testament = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi"
    ]

    return "Old Testament" if book in old_testament else "New Testament"


def get_chapter_significance(book, chapter):
    """Generate significance explanation for a chapter"""
    significance_templates = [
        "provides essential context for understanding God's covenant relationship with His people",
        "reveals key aspects of God's character through divine actions and declarations",
        "establishes important theological principles that resonate throughout Scripture",
        "addresses timeless questions about faith, suffering, and divine purpose",
        "offers practical wisdom for godly living in a fallen world",
        "demonstrates God's faithfulness despite human unfaithfulness",
        "contributes to the biblical metanarrative of redemption",
        "foreshadows Christ's work through typology and prophetic elements",
        "illustrates divine judgment and mercy in response to human actions",
        "provides guidance for worship and spiritual devotion"
    ]

    # Special significance for specific chapters
    special_significance = {
        ("Genesis", 1): "establishes the foundational doctrine of creation and God's sovereignty",
        ("Genesis", 3): "introduces the fall of humanity and the need for redemption",
        ("Exodus", 20): "presents the Decalogue (Ten Commandments) as the cornerstone of biblical law",
        ("Leviticus", 16): "details the Day of Atonement ritual that prefigures Christ's sacrificial work",
        ("Isaiah", 53): "provides the clearest Old Testament prophecy of the Messiah's suffering",
        ("Matthew", 5): "presents Jesus' ethical teaching in the Sermon on the Mount",
        ("John", 3): "contains the essential gospel message of salvation by faith",
        ("Romans", 8): "articulates the doctrines of justification, sanctification, and glorification",
        ("1 Corinthians", 15): "defends the resurrection as central to Christian faith",
        ("Revelation", 1): "introduces apocalyptic visions that reveal Christ's ultimate victory and sovereignty"
    }

    if (book, chapter) in special_significance:
        return special_significance[(book, chapter)]
    else:
        return random.choice(significance_templates)


def generate_book_commentary(book, chapters):
    """Generate comprehensive commentary for an entire book"""
    # Get basic book information
    testament = get_testament_for_book(book)
    time_period = get_time_period(book)
    genre = get_book_genre(book)
    
    # Generate tags based on themes and genre
    tags = generate_book_tags(book, genre)
    
    # Generate introduction based on book
    introduction = generate_book_introduction(book)
    
    # Generate historical context
    historical_context = generate_historical_context(book)
    
    # Generate literary features
    literary_features = generate_literary_features(book, genre)
    
    # Generate key themes
    themes = generate_book_themes(book)
    
    # Generate theological significance
    theological_significance = generate_theological_significance(book)
    
    # Generate contemporary application
    application = generate_book_application(book)
    
    # Generate key highlights from the book
    highlights = generate_book_highlights(book, chapters)
    
    # Generate book outline
    outline = generate_book_outline(book, chapters)
    
    # Generate cross-references to other books
    cross_references = generate_book_cross_references(book)
    
    # Generate chapter summaries with key verses
    chapter_summaries = generate_chapter_summaries(book, chapters)
    
    return {
        "testament": testament,
        "time_period": time_period,
        "genre": genre,
        "tags": tags,
        "introduction": introduction,
        "historical_context": historical_context,
        "literary_features": literary_features,
        "themes": themes,
        "theological_significance": theological_significance,
        "application": application,
        "highlights": highlights,
        "outline": outline,
        "cross_references": cross_references,
        "chapter_summaries": chapter_summaries
    }


def generate_book_tags(book, genre):
    """Generate tags for a book based on its themes and genre"""
    # Base tags on genre
    genre_tags = {
        "narrative": ["Historical", "Narrative", "Story"],
        "law": ["Law", "Torah", "Covenant"],
        "poetry": ["Poetry", "Wisdom", "Lyrical"],
        "prophecy": ["Prophecy", "Prophetic", "Oracle"],
        "apocalyptic": ["Apocalyptic", "Symbolic", "Visionary"],
        "epistle": ["Epistle", "Letter", "Instruction"],
        "gospel": ["Gospel", "Biography", "Testimony"],
        "wisdom": ["Wisdom", "Proverb", "Teaching"]
    }
    
    # Book-specific tags
    book_specific_tags = {
        "Genesis": ["Creation", "Patriarchs", "Covenant", "Origins"],
        "Exodus": ["Deliverance", "Law", "Tabernacle", "Moses"],
        "Leviticus": ["Holiness", "Sacrifice", "Priesthood", "Ritual"],
        "Numbers": ["Wilderness", "Journey", "Census", "Rebellion"],
        "Deuteronomy": ["Covenant", "Law", "Moses", "Instruction"],
        "Joshua": ["Conquest", "Promised Land", "Leadership", "Victory"],
        "Judges": ["Cycle", "Deliverance", "Apostasy", "Tribalism"],
        "Ruth": ["Loyalty", "Redemption", "Kinsman-Redeemer", "Foreigner"],
        "1 Samuel": ["Kingship", "Saul", "David", "Transition"],
        "2 Samuel": ["David", "Kingdom", "Covenant", "Kingship"],
        "1 Kings": ["Solomon", "Temple", "Division", "Kings"],
        "2 Kings": ["Kings", "Prophets", "Exile", "Judgment"],
        "1 Chronicles": ["David", "Genealogy", "Temple", "Worship"],
        "2 Chronicles": ["Temple", "Kings", "Worship", "Reformation"],
        "Ezra": ["Return", "Restoration", "Temple", "Law"],
        "Nehemiah": ["Rebuilding", "Walls", "Reform", "Leadership"],
        "Esther": ["Providence", "Deliverance", "Courage", "Identity"],
        "Job": ["Suffering", "Wisdom", "Righteousness", "Divine Justice"],
        "Psalms": ["Worship", "Praise", "Lament", "Prayer"],
        "Proverbs": ["Wisdom", "Instruction", "Conduct", "Character"],
        "Ecclesiastes": ["Meaning", "Vanity", "Wisdom", "Purpose"],
        "Song of Solomon": ["Love", "Marriage", "Devotion", "Relationship"],
        "Isaiah": ["Holiness", "Messiah", "Judgment", "Restoration"],
        "Jeremiah": ["Judgment", "Covenant", "Restoration", "Prophet"],
        "Lamentations": ["Grief", "Judgment", "Mercy", "Destruction"],
        "Ezekiel": ["Glory", "Vision", "Judgment", "Restoration"],
        "Daniel": ["Kingdom", "Sovereignty", "Faithfulness", "Prophecy"],
        "Hosea": ["Faithfulness", "Covenant", "Redemption", "Apostasy"],
        "Joel": ["Day of the LORD", "Judgment", "Restoration", "Spirit"],
        "Amos": ["Justice", "Judgment", "Righteousness", "Prophecy"],
        "Obadiah": ["Judgment", "Pride", "Edom", "Restoration"],
        "Jonah": ["Mercy", "Mission", "Repentance", "Compassion"],
        "Micah": ["Justice", "Judgment", "Messiah", "Covenant"],
        "Nahum": ["Judgment", "Nineveh", "Justice", "Vengeance"],
        "Habakkuk": ["Faith", "Justice", "Sovereignty", "Questioning"],
        "Zephaniah": ["Day of the LORD", "Judgment", "Remnant", "Restoration"],
        "Haggai": ["Temple", "Priorities", "Restoration", "Blessing"],
        "Zechariah": ["Messiah", "Vision", "Restoration", "Future"],
        "Malachi": ["Covenant", "Faithfulness", "Offering", "Messenger"],
        "Matthew": ["Kingdom", "Messiah", "Fulfillment", "Teaching"],
        "Mark": ["Servant", "Action", "Suffering", "Discipleship"],
        "Luke": ["Savior", "Universal", "Social Justice", "Holy Spirit"],
        "John": ["Belief", "Life", "Word", "Signs"],
        "Acts": ["Church", "Holy Spirit", "Mission", "Growth"],
        "Romans": ["Righteousness", "Faith", "Grace", "Salvation"],
        "1 Corinthians": ["Unity", "Wisdom", "Gifts", "Love"],
        "2 Corinthians": ["Ministry", "Reconciliation", "Generosity", "Weakness"],
        "Galatians": ["Freedom", "Grace", "Faith", "Law"],
        "Ephesians": ["Unity", "Church", "Grace", "Spiritual Warfare"],
        "Philippians": ["Joy", "Humility", "Unity", "Contentment"],
        "Colossians": ["Supremacy", "Completeness", "Wisdom", "Freedom"],
        "1 Thessalonians": ["Encouragement", "Hope", "Faith", "Return"],
        "2 Thessalonians": ["Judgment", "Work", "Hope", "Perseverance"],
        "1 Timothy": ["Leadership", "Church Order", "Sound Doctrine", "Godliness"],
        "2 Timothy": ["Endurance", "Scripture", "Faithfulness", "Legacy"],
        "Titus": ["Good Works", "Leadership", "Sound Doctrine", "Grace"],
        "Philemon": ["Reconciliation", "Forgiveness", "Brotherhood", "Transformation"],
        "Hebrews": ["Superiority", "Faith", "Perseverance", "Covenant"],
        "James": ["Works", "Faith", "Wisdom", "Speech"],
        "1 Peter": ["Suffering", "Holiness", "Hope", "Identity"],
        "2 Peter": ["Knowledge", "False Teaching", "Day of the Lord", "Growth"],
        "1 John": ["Love", "Truth", "Fellowship", "Assurance"],
        "2 John": ["Truth", "Love", "Discernment", "Hospitality"],
        "3 John": ["Hospitality", "Truth", "Example", "Leadership"],
        "Jude": ["Contending", "Faith", "False Teaching", "Judgment"],
        "Revelation": ["Victory", "Judgment", "Worship", "New Creation"]
    }
    
    # Combine tags
    tags = []
    
    # Add genre tags
    for key in genre_tags.keys():
        if key in genre.lower():
            tags.extend(genre_tags[key])
            break
    
    # Add book-specific tags
    if book in book_specific_tags:
        tags.extend(book_specific_tags[book])
    
    # Return unique tags
    return list(set(tags))


def get_book_genre(book):
    """Return the literary genre of a book"""
    genres = {
        # Torah
        "Genesis": "Narrative with genealogy",
        "Exodus": "Narrative with law",
        "Leviticus": "Law and ritual instruction",
        "Numbers": "Narrative with law and census",
        "Deuteronomy": "Sermonic law",
        
        # Historical books
        "Joshua": "Historical narrative",
        "Judges": "Cyclical historical narrative",
        "Ruth": "Historical narrative",
        "1 Samuel": "Historical narrative",
        "2 Samuel": "Historical narrative",
        "1 Kings": "Historical narrative",
        "2 Kings": "Historical narrative",
        "1 Chronicles": "Historical narrative with genealogy",
        "2 Chronicles": "Historical narrative",
        "Ezra": "Historical narrative",
        "Nehemiah": "Historical narrative with memoir",
        "Esther": "Historical narrative",
        
        # Wisdom literature
        "Job": "Wisdom literature with poetic dialogue",
        "Psalms": "Poetry and liturgy",
        "Proverbs": "Wisdom literature",
        "Ecclesiastes": "Wisdom literature with philosophical reflection",
        "Song of Solomon": "Poetry and love song",
        
        # Major Prophets
        "Isaiah": "Prophetic literature with poetry",
        "Jeremiah": "Prophetic literature with biography",
        "Lamentations": "Poetic lament",
        "Ezekiel": "Prophetic literature with apocalyptic elements",
        "Daniel": "Narrative with apocalyptic visions",
        
        # Minor Prophets
        "Hosea": "Prophetic literature",
        "Joel": "Prophetic literature",
        "Amos": "Prophetic literature",
        "Obadiah": "Prophetic literature",
        "Jonah": "Prophetic narrative",
        "Micah": "Prophetic literature",
        "Nahum": "Prophetic literature",
        "Habakkuk": "Prophetic literature with dialogue",
        "Zephaniah": "Prophetic literature",
        "Haggai": "Prophetic literature",
        "Zechariah": "Prophetic literature with apocalyptic visions",
        "Malachi": "Prophetic literature with disputation",
        
        # Gospels
        "Matthew": "Gospel narrative",
        "Mark": "Gospel narrative",
        "Luke": "Gospel narrative with historiography",
        "John": "Gospel narrative with theology",
        
        # Acts
        "Acts": "Historical narrative",
        
        # Pauline Epistles
        "Romans": "Epistle with systematic theology",
        "1 Corinthians": "Epistle",
        "2 Corinthians": "Epistle",
        "Galatians": "Epistle",
        "Ephesians": "Epistle",
        "Philippians": "Epistle",
        "Colossians": "Epistle",
        "1 Thessalonians": "Epistle",
        "2 Thessalonians": "Epistle",
        "1 Timothy": "Pastoral epistle",
        "2 Timothy": "Pastoral epistle",
        "Titus": "Pastoral epistle",
        "Philemon": "Personal epistle",
        "Hebrews": "Epistle with sermonic elements",
        
        # General Epistles
        "James": "Epistle with wisdom elements",
        "1 Peter": "Epistle",
        "2 Peter": "Epistle",
        "1 John": "Epistle with theological discourse",
        "2 John": "Brief epistle",
        "3 John": "Brief epistle",
        "Jude": "Epistle",
        
        # Apocalyptic
        "Revelation": "Apocalyptic literature with epistle elements"
    }
    
    return genres.get(book, "Biblical literature")


def generate_book_introduction(book):
    """Generate introduction for a book"""
    # You would implement detailed logic here based on the book
    # This is a simplified version that would be expanded
    
    introductions = {
        "Genesis": """
        <p>Genesis, the first book of the Bible, serves as the foundation for the entire biblical narrative. Its name comes from the Greek word meaning "origin" or "beginning," and it appropriately records the beginnings of the universe, humanity, sin, salvation, and the nation of Israel. Written by Moses according to traditional attribution, Genesis spans from creation to Israel's migration to Egypt, covering more time than any other book in Scripture.</p>
        
        <p>As the cornerstone of the Pentateuch (the first five books of the Bible), Genesis establishes the theological framework for understanding God's relationship with humanity and His covenant promises. It introduces key themes that resonate throughout Scripture: creation, fall, judgment, grace, covenant, promise, and redemption.</p>
        
        <p>The book divides naturally into two major sections: primeval history (chapters 1-11) and patriarchal narratives (chapters 12-50). The primeval history addresses universal concerns through the stories of creation, the fall, the flood, and the Tower of Babel. The patriarchal narratives focus on God's covenant relationship with Abraham, Isaac, Jacob, and Joseph, establishing the foundation for Israel's national identity.</p>
        
        <p>Throughout Genesis, God is portrayed as the sovereign Creator who brings order out of chaos, makes covenants with His chosen people, and works providentially to fulfill His purposes despite human failings. The book's theological significance extends far beyond its historical narrative, providing the essential backdrop for understanding God's redemptive plan that culminates in Christ.</p>
        """,
        
        "Revelation": """
        <p>Revelation, the final book of the Bible, stands as a triumphant conclusion to God's written word. Also known as the Apocalypse (from the Greek word meaning "unveiling" or "disclosure"), it reveals the culmination of God's redemptive plan through symbolic visions and prophetic declarations. Written by John the Apostle during his exile on the island of Patmos around 95 CE, Revelation addresses seven churches in Asia Minor while providing a cosmic perspective on spiritual realities and future events.</p>
        
        <p>As the Bible's primary apocalyptic book, Revelation employs rich symbolism, vivid imagery, and numerological patterns to communicate its message. It draws heavily from Old Testament prophetic literature, particularly Daniel, Ezekiel, and Zechariah, creating a tapestry of allusions that connect it to the broader biblical narrative.</p>
        
        <p>The book presents itself as a prophecy, an apocalypse, and an epistle simultaneously. It offers both encouragement to persecuted believers and warnings to compromising churches. Throughout its twenty-two chapters, Revelation contrasts the sovereignty of God against human and demonic powers, ultimately depicting the complete victory of Christ over all evil forces.</p>
        
        <p>Central themes include Christ's identity as the slain but victorious Lamb, divine judgment on wickedness, the cosmic conflict between God and Satan, and the glorious hope of a new heaven and new earth. While interpretations of its prophetic timeline vary among scholars, Revelation's core message remains clear: God remains sovereign over history, Christ will return in triumph, and those who remain faithful will participate in His eternal kingdom.</p>
        """
    }
    
    # Get a template introduction based on genre if specific introduction isn't available
    if book not in introductions:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)
        
        # Generate a generic introduction based on testament and genre
        if "narrative" in genre.lower():
            intro = f"""
            <p>{book} is a narrative book in the {testament} that recounts key historical events and developments in Israel's history. The book contains important stories, characters, and events that contribute to the broader biblical narrative and redemptive history.</p>
            
            <p>As with other biblical narratives, {book} combines historical reporting with theological interpretation, showing how God works through historical circumstances and human actions to accomplish His purposes. The narrative demonstrates divine providence, human responsibility, and the consequences of both obedience and disobedience.</p>
            
            <p>Throughout {book}, readers can observe God's faithfulness to His covenant promises despite human failings and opposition. The book's events establish important precedents and patterns that inform biblical theology and provide context for understanding later Scriptural developments.</p>
            """
        elif "epistle" in genre.lower():
            intro = f"""
            <p>{book} is an epistle (letter) in the {testament} written to address specific circumstances, challenges, and questions in the early Christian church. The letter combines theological instruction with practical exhortation, demonstrating the connection between Christian doctrine and everyday living.</p>
            
            <p>Like other New Testament epistles, {book} addresses particular situations while establishing principles with broader application. The letter reflects the apostolic authority of its author and the normative teaching of the early church, contributing to the development of Christian theology and practice.</p>
            
            <p>Throughout {book}, readers can observe the practical outworking of the gospel in community life, personal ethics, and spiritual development. The letter demonstrates how Christ's finished work transforms individual believers and reshapes their relationships and priorities.</p>
            """
        elif "prophetic" in genre.lower() or "prophecy" in genre.lower():
            intro = f"""
            <p>{book} is a prophetic book in the {testament} that communicates divine messages of warning, judgment, and hope to God's people. The prophecies combine historical relevance to their original audience with enduring theological significance and, in some cases, messianic predictions.</p>
            
            <p>Like other biblical prophetic literature, {book} addresses covenant violations, calls for repentance, and proclaims both divine judgment and promised restoration. The prophecies demonstrate God's righteousness, sovereignty over history, and faithful commitment to His covenant purposes.</p>
            
            <p>Throughout {book}, readers encounter powerful imagery, poetic language, and symbolic actions that reinforce the prophetic message. The book reveals God's perspective on historical events and human affairs, often challenging conventional wisdom and cultural assumptions.</p>
            """
        elif "wisdom" in genre.lower():
            intro = f"""
            <p>{book} is a wisdom book in the {testament} that addresses life's fundamental questions and provides guidance for righteous living. The book explores themes of divine order, human experience, and practical ethics, offering insights for navigating the complexities of human existence.</p>
            
            <p>Like other biblical wisdom literature, {book} emphasizes the fear of the Lord as the foundation of true wisdom and contrasts the paths of wisdom and folly. The book demonstrates how reverence for God leads to discernment, virtue, and ultimately flourishing.</p>
            
            <p>Throughout {book}, readers encounter profound reflections on creation's order, human limitations, moral principles, and life's meaning. The book bridges theological truth and practical living, showing how divine wisdom applies to everyday decisions and relationships.</p>
            """
        elif "gospel" in genre.lower():
            intro = f"""
            <p>{book} is a gospel account in the {testament} that presents the life, ministry, death, and resurrection of Jesus Christ. The book combines historical reporting with theological interpretation, portraying Jesus as the fulfillment of Old Testament promises and the inaugurator of God's kingdom.</p>
            
            <p>Like other canonical gospels, {book} selectively records Jesus' words and deeds to communicate His identity and significance. The narrative demonstrates Jesus' divine authority, redemptive mission, and transformative teaching, inviting readers to respond in faith.</p>
            
            <p>Throughout {book}, readers encounter Jesus' interactions with various individuals and groups, His powerful parables and discourses, and the climactic events of His passion and resurrection. The book establishes the historical foundation for Christian faith while interpreting Jesus' significance for all humanity.</p>
            """
        elif "apocalyptic" in genre.lower():
            intro = f"""
            <p>{book} is an apocalyptic book in the {testament} that unveils spiritual realities and future events through symbolic visions and prophetic declarations. The book employs rich imagery and symbolic language to communicate divine perspective on history, cosmic conflict, and ultimate outcomes.</p>
            
            <p>Like other biblical apocalyptic literature, {book} addresses contexts of suffering and persecution, offering hope through the assurance of God's sovereignty and eventual triumph. The visions demonstrate the temporary nature of evil powers and the certainty of divine judgment and redemption.</p>
            
            <p>Throughout {book}, readers encounter dramatic portrayals of spiritual warfare, divine intervention, and eschatological consummation. The book provides a cosmic framework for understanding present trials and maintaining faithful endurance through the assurance of God's ultimate victory.</p>
            """
        else:
            intro = f"""
            <p>{book} is an important book in the {testament} that contributes significantly to the biblical canon. The book addresses themes and concerns relevant to its original audience while establishing principles and patterns with enduring theological significance.</p>
            
            <p>As with other biblical literature, {book} combines historical awareness with divine inspiration, communicating God's truth through human language and cultural forms. The book demonstrates the progressive nature of divine revelation and its adaptation to specific historical contexts.</p>
            
            <p>Throughout {book}, readers can trace important developments in the biblical narrative and theological understanding. The book provides essential insights for comprehending God's character, purposes, and relationship with humanity.</p>
            """
        
        return intro
    
    return introductions[book]


def generate_historical_context(book):
    """Generate historical context for a book"""
    # This would be expanded with more detailed content
    historical_contexts = {
        "Genesis": """
        <p>Genesis was compiled and written by Moses around 1440-1400 BCE, according to traditional attribution. The events it records span from creation to approximately 1800 BCE, covering the primeval period and the age of the patriarchs. The book was composed for the Israelites after their exodus from Egypt as they prepared to enter the Promised Land.</p>
        
        <h3>Ancient Near Eastern Context</h3>
        <p>The world of Genesis was dominated by great civilizations in Mesopotamia and Egypt. Urban centers had developed along the Tigris, Euphrates, and Nile rivers, with advanced writing systems, monumental architecture, and complex religious practices. Polytheism was the norm, with elaborate mythologies explaining creation and natural phenomena.</p>
        
        <p>Several ancient Near Eastern texts share similarities with Genesis narratives, including the Enuma Elish (Babylonian creation myth), the Epic of Gilgamesh (which includes a flood account), and the Atrahasis Epic. However, Genesis presents a distinctly monotheistic worldview that contrasts sharply with these contemporaneous myths.</p>
        
        <h3>Cultural Background</h3>
        <p>The patriarchs (Abraham, Isaac, and Jacob) lived as semi-nomadic herdsmen, moving between established city-states in Canaan. Their lifestyle involved seasonal migration with flocks and herds, establishing temporary settlements, and digging wells. Kinship ties were paramount, with extended family groups (clans) forming the basic social unit.</p>
        
        <p>Marriage customs included bride prices, arranged marriages, and occasionally polygamy, especially when a first wife was barren. Inheritance typically passed to the firstborn son, though Genesis records several instances where this pattern was divinely overturned.</p>
        
        <h3>Archaeological Insights</h3>
        <p>Archaeological discoveries have illuminated many aspects of the Genesis narratives. Excavations at sites like Ur (Abraham's birthplace) reveal a sophisticated urban center. Tablets from Mari and Nuzi document social customs similar to those practiced by the patriarchs, including adoption agreements, surrogacy arrangements, and covenant ceremonies.</p>
        
        <p>Egypt's Middle Kingdom period (2040-1782 BCE) provides the likely background for Joseph's rise to prominence. Historical records show that Semitic people did indeed achieve high positions in Egyptian administration, and periods of famine are documented in Egyptian history.</p>
        """,
        
        "Revelation": """
        <p>Revelation was written during the reign of Emperor Domitian (81-96 CE), according to early church tradition as recorded by Irenaeus. The author, John, was exiled to the island of Patmos "because of the word of God and the testimony of Jesus" (1:9), indicating persecution for his Christian witness. The book addresses seven actual churches in the Roman province of Asia (western Turkey).</p>
        
        <h3>Roman Imperial Context</h3>
        <p>The late first century was marked by increasing imperial persecution of Christians. Domitian intensified emperor worship throughout the Roman Empire, demanding to be addressed as "Lord and God" (<em>dominus et deus noster</em>). He established an imperial cult with temples and statues dedicated to his worship. Christians who refused to participate in emperor worship faced economic sanctions, social ostracism, and sometimes execution.</p>
        
        <p>The province of Asia, where the seven churches were located, was particularly zealous in emperor worship. Ephesus, Smyrna, and Pergamum all had temples dedicated to the imperial cult. Pergamum is specifically mentioned as the place "where Satan's throne is" (2:13), likely referring to its prominence in emperor worship or its massive altar to Zeus.</p>
        
        <h3>Church Situation</h3>
        <p>The seven churches addressed in Revelation faced varying challenges. Some endured direct persecution (Smyrna, Philadelphia), while others struggled with false teaching (Ephesus, Pergamum, Thyatira), spiritual apathy (Sardis), or lukewarm commitment (Laodicea). Economic pressures pushed some believers toward compromise, as participation in trade guilds often required involvement in pagan rituals.</p>
        
        <p>Jewish communities in these cities sometimes opposed Christian groups, as mentioned regarding Smyrna and Philadelphia (2:9, 3:9). This created additional social pressure for Jewish Christians caught between their ethnic heritage and new faith.</p>
        
        <h3>Archaeological Evidence</h3>
        <p>Archaeological excavations have confirmed details about the seven cities addressed in Revelation. Laodicea's lukewarm water came from aqueducts carrying water from hot springs that cooled during transit. The city was indeed wealthy, with a banking industry and medical school known for eye salve. Philadelphia was subject to frequent earthquakes, as alluded to in the promise of a pillar that would never be shaken (3:12).</p>
        
        <p>Ephesus was home to the Temple of Artemis (Diana), one of the Seven Wonders of the ancient world. Excavations have uncovered a massive theater (Acts 19) and evidence of the city's prominence and wealth. Sardis' reputation as a city that appeared alive but was actually in decline is confirmed by archaeological evidence of its diminishing importance in the late first century.</p>
        """
    }
    
    # Generate a generic historical context if specific context isn't available
    if book not in historical_contexts:
        testament = get_testament_for_book(book)
        
        if testament == "Old Testament":
            # Determine approximate time period
            period = "pre-exilic"  # Default
            if book in ["Ezra", "Nehemiah", "Esther", "Haggai", "Zechariah", "Malachi"]:
                period = "post-exilic"
            elif book in ["Jeremiah", "Lamentations", "Ezekiel", "Daniel"]:
                period = "exilic"
            
            context = f"""
            <p>{book} was composed during the {period} period of Israel's history. The book reflects the historical circumstances, cultural influences, and theological concerns of its time.</p>
            
            <h3>Historical Setting</h3>
            <p>The book emerges from a context where Israel's covenant relationship with God shaped its national identity and religious practices. The surrounding nations, with their polytheistic worship and imperial ambitions, provided both cultural pressure and political threats that influenced Israel's historical experience.</p>
            
            <p>The religious life of Israel centered around the covenant, Law, and (depending on the period) the temple, with prophets calling the people back to covenant faithfulness and warning of judgment for persistent disobedience.</p>
            
            <h3>Cultural Background</h3>
            <p>The cultural world of {book} involved agricultural societies organized around tribal and kinship relationships, with increasing urbanization and social stratification over time. Religious practices permeated daily life, and interaction with surrounding cultures created ongoing tension between assimilation and distinctive identity.</p>
            
            <p>Archaeological discoveries have illuminated many aspects of daily life, religious practices, and historical events mentioned in {book}, providing background context for understanding its narratives and teachings.</p>
            """
        else:  # New Testament
            context = f"""
            <p>{book} was written during the first century CE, within the context of the early Christian church developing under Roman imperial rule. The book reflects the historical circumstances, cultural influences, and theological concerns of this formative period.</p>
            
            <h3>Roman Imperial Context</h3>
            <p>The Roman Empire provided the overarching political structure for the New Testament world, with its system of provinces, client kingdoms, and military presence. The Pax Romana (Roman Peace) enabled travel and communication throughout the Mediterranean world, facilitating the spread of Christianity while also presenting challenges through imperial ideology and occasional persecution.</p>
            
            <h3>Religious Environment</h3>
            <p>The religious landscape included Judaism with its various sects (Pharisees, Sadducees, Essenes), Greco-Roman polytheism, mystery religions, and philosophical schools. Early Christianity emerged within this complex environment, defining its identity in relation to Judaism while addressing Gentile converts from pagan backgrounds.</p>
            
            <p>Archaeological discoveries, historical documents, and cultural studies have illuminated many aspects of daily life, religious practices, and social structures in the first-century world, providing valuable context for understanding {book}.</p>
            """

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
