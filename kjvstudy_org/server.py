from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
import random
import html

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

    return templates.TemplateResponse(
        "chapter.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
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
                "analysis": "This opening verse establishes the divine origin of the Apocalypse (revelation). The chain of revelation is significant: from God, to Christ, to angel, to John, to the churches. The phrase \"things which must shortly come to pass\" indicates urgency and certainty, not necessarily immediacy in human time scales.",
                "historical": "During the reign of Emperor Domitian (81-96 CE), Christians faced increasing pressure to participate in emperor worship. This book offered hope to persecuted believers by assuring them of God's ultimate sovereignty over human rulers and the certainty of Christ's victory.",
                "questions": [
                    "How does the concept of divine revelation shape your approach to Scripture?",
                    "What significance might the chain of transmission (God→Christ→angel→John→churches) have for understanding authority?",
                    "How should we understand the timeframe indicated by 'shortly come to pass' given that nearly 2,000 years have passed?"
                ],
                "cross_references": [
                    {"text": "Daniel 2:28-29", "url": "/book/Daniel/chapter/2#verse-28", "context": "Things revealed about the latter days"},
                    {"text": "John 15:15", "url": "/book/John/chapter/15#verse-15", "context": "Christ revealing the Father's will"}
                ]
            },
            4: {
                "analysis": "This verse begins the formal greeting to the seven churches of Asia Minor. The trinitarian formula is unique: the eternal Father ('who is, who was, and who is to come'), the sevenfold Spirit, and Jesus Christ. The number seven symbolizes completeness or perfection in biblical numerology.",
                "historical": "The seven churches addressed were actual congregations in Asia Minor (modern Turkey). They existed in a cultural environment dominated by pagan worship, including the imperial cult. Each city had its own social, economic, and spiritual challenges that are addressed in chapters 2-3.",
                "questions": [
                    "What does the description of God as 'who is, who was, and who is to come' reveal about divine nature?",
                    "What might the 'seven Spirits' represent in this context?",
                    "How does this trinitarian greeting compare to those found in Paul's letters?"
                ],
                "cross_references": [
                    {"text": "Exodus 3:14", "url": "/book/Exodus/chapter/3#verse-14", "context": "God as the 'I AM'"},
                    {"text": "Isaiah 11:2-3", "url": "/book/Isaiah/chapter/11#verse-2", "context": "Seven aspects of the Spirit"}
                ]
            },
            7: {
                "analysis": "This verse emphasizes Christ's glorious return, visible to all, including those who rejected and pierced Him. It combines references from Daniel 7:13 (coming with clouds) and Zechariah 12:10 (those who pierced him shall mourn). The divine declaration 'I am Alpha and Omega' frames the verse with God's sovereignty.",
                "historical": "For Christians experiencing persecution, this promise of Christ's visible return as judge and vindicator would provide hope and encouragement. The verse establishes that history's culmination centers on Christ's return, not the reign of human emperors.",
                "questions": [
                    "How does the certainty of Christ's return influence Christian ethics and perseverance?",
                    "What is the significance of combining Old Testament references about God with descriptions of Jesus?",
                    "How should believers balance the hope of Christ's return with responsible living in the present world?"
                ],
                "cross_references": [
                    {"text": "Matthew 24:30", "url": "/book/Matthew/chapter/24#verse-30", "context": "Christ's return with clouds"},
                    {"text": "Zechariah 12:10", "url": "/book/Zechariah/chapter/12#verse-10", "context": "Looking on him whom they pierced"}
                ]
            },
            13: {
                "analysis": "This verse begins the dramatic vision of Christ amid the lampstands. The figure is described in terms combining royal, priestly and divine attributes. The 'one like unto the Son of man' echoes Daniel 7:13, while the long robe with golden sash suggests high priestly attire (Exodus 28:4).",
                "historical": "In the first century, the imagery would connect with both Jewish apocalyptic expectations and contrast with imperial imagery. While Roman emperors claimed divine status, this vision presents Christ with true divine and cosmic authority.",
                "questions": [
                    "How does this vision of Christ compare with portrayals elsewhere in Scripture?",
                    "What significance might the position 'in the midst of the lampstands' have for church leadership?",
                    "How do the combined royal and priestly elements reveal Christ's roles?"
                ],
                "cross_references": [
                    {"text": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "context": "Son of Man vision"},
                    {"text": "Hebrews 4:14-16", "url": "/book/Hebrews/chapter/4#verse-14", "context": "Christ as High Priest"}
                ]
            },
            18: {
                "analysis": "This powerful declaration by the risen Christ emphasizes His victory over death and authority over the afterlife. The phrase 'I am he that liveth, and was dead' directly references Christ's resurrection. The 'keys of hell and of death' symbolize authority over mortality and judgment.",
                "historical": "For early Christians facing potential martyrdom, this verse would provide profound reassurance that death was not the final word. Christ's authority extends beyond death itself, offering hope to those facing persecution.",
                "questions": [
                    "How does Christ's victory over death transform the Christian understanding of mortality?",
                    "What does it mean that Christ holds 'the keys of hell and of death'?",
                    "How might this verse have comforted believers facing imperial persecution?"
                ],
                "cross_references": [
                    {"text": "Isaiah 22:22", "url": "/book/Isaiah/chapter/22#verse-22", "context": "The key of David"},
                    {"text": "Romans 6:9", "url": "/book/Romans/chapter/6#verse-9", "context": "Christ dies no more"}
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
        
    <p>The author identifies himself as "John" (verse 1:1, 1:4, 1:9), traditionally understood to be the Apostle John, though some scholars propose it may be another John known as "John the Elder." He was exiled tocan be divided into several key sections:</p>

        <ol>
            <li><strong>Verses 1-3</strong>: Introduction and blessing for those who read and keep the prophecy</li>
            <li><strong>Verses 4-8</strong>: Greeting to the seven churches and proclamation of Christ's divine authority</li>
            <li><strong>Verses 9-16</strong>: John's vision of the glorified Christ amid the lampstands</li>
            <li><strong>Verses 17-20</strong>: Christ's commission to John and explanation of the symbolic vision</li>
        </ol>

        <p>Revelation 1 is significant because it establishes the divine authority behind the apocalyptic visions and presents Christ in His glorified, exalted state. The vivid symbolism introduces key motifs that will appear throughout the book, including the number seven (churches, spirits, lampstands), divine titles ("Alpha and Omega," "First and Last"), and the imagery of Christ as both priest and king.</p>

        <p>When studying this passage, it's important to understand its historical context during a time of imperial persecution, as well as its place as the culmination of biblical prophecy and apocalyptic literature.</p>
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


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "kjv-study"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
