"""Main page routes - homepage, books browser, and resources."""
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..kjv import bible
from ..utils.helpers import get_daily_verse, verse_reference_to_url
from ._templates import templates

router = APIRouter()

# Server-side cache for homepage (rebuilds once per day)
_homepage_cache = {"date": None, "html": None}


# =============================================================================
# Routes
# =============================================================================

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    today = date.today()
    if _homepage_cache["date"] == today and _homepage_cache["html"] is not None:
        return HTMLResponse(content=_homepage_cache["html"], headers={"Cache-Control": "public, max-age=3600"})

    books = bible.get_books()
    daily_verse = get_daily_verse()

    # Define study guide categories
    study_guides = {
        "Foundational Studies": [
            {
                "title": "New Believer's Guide",
                "description": "Essential truths for new Christians",
                "slug": "new-believer",
                "verses": ["John 3:16", "Romans 10:9", "1 John 1:9", "2 Corinthians 5:17"]
            },
            {
                "title": "Salvation by Grace",
                "description": "Understanding God's gift of salvation",
                "slug": "salvation",
                "verses": ["Ephesians 2:8-9", "Romans 3:23", "Romans 6:23", "Titus 3:5"]
            },
            {
                "title": "The Gospel Message",
                "description": "The good news of Jesus Christ",
                "slug": "gospel",
                "verses": ["1 Corinthians 15:3-4", "Romans 1:16", "Mark 16:15", "Acts 4:12"]
            }
        ],
        "Character & Living": [
            {
                "title": "Fruits of the Spirit",
                "description": "Developing Christian character",
                "slug": "fruits-spirit",
                "verses": ["Galatians 5:22-23", "1 Corinthians 13:4-7", "Philippians 4:8", "Colossians 3:12-14"]
            },
            {
                "title": "Prayer & Faith",
                "description": "Growing in prayer and trust",
                "slug": "prayer-faith",
                "verses": ["Matthew 6:9-13", "1 Thessalonians 5:17", "Hebrews 11:1", "James 1:6"]
            },
            {
                "title": "Christian Living",
                "description": "Walking as followers of Christ",
                "slug": "christian-living",
                "verses": ["Romans 12:1-2", "1 Peter 2:9", "Matthew 5:14-16", "Philippians 2:14-16"]
            }
        ],
        "Biblical Themes": [
            {
                "title": "God's Love",
                "description": "Understanding the depth of God's love",
                "slug": "gods-love",
                "verses": ["1 John 4:8", "John 3:16", "Romans 8:38-39", "1 John 3:1"]
            },
            {
                "title": "Hope & Comfort",
                "description": "Finding hope in difficult times",
                "slug": "hope-comfort",
                "verses": ["Romans 15:13", "2 Corinthians 1:3-4", "Psalm 23:4", "Isaiah 41:10"]
            },
            {
                "title": "Wisdom & Guidance",
                "description": "Seeking God's wisdom for life",
                "slug": "wisdom-guidance",
                "verses": ["Proverbs 3:5-6", "James 1:5", "Psalm 119:105", "Proverbs 27:17"]
            }
        ],
        "Doctrinal Studies": [
            {
                "title": "The Trinity",
                "description": "Understanding God as Father, Son, and Holy Spirit",
                "slug": "trinity",
                "verses": ["Matthew 28:19", "2 Corinthians 13:14", "1 Peter 1:2", "John 14:16-17"]
            },
            {
                "title": "The Resurrection",
                "description": "Christ's victory over death and our hope",
                "slug": "resurrection",
                "verses": ["1 Corinthians 15:20-22", "Romans 6:4-5", "John 11:25-26", "1 Thessalonians 4:16-17"]
            },
            {
                "title": "Heaven & Eternity",
                "description": "Our eternal home with God",
                "slug": "heaven-eternity",
                "verses": ["Revelation 21:1-4", "John 14:2-3", "Philippians 3:20-21", "1 Corinthians 2:9"]
            }
        ],
        "Family & Relationships": [
            {
                "title": "Biblical Marriage",
                "description": "God's design for marriage",
                "slug": "biblical-marriage",
                "verses": ["Ephesians 5:22-33", "Genesis 2:24", "1 Corinthians 7:3-5", "Hebrews 13:4"]
            },
            {
                "title": "Raising Children",
                "description": "Biblical principles for parenting",
                "slug": "raising-children",
                "verses": ["Proverbs 22:6", "Ephesians 6:4", "Deuteronomy 6:6-7", "Colossians 3:21"]
            },
            {
                "title": "Money & Stewardship",
                "description": "Biblical wisdom on finances",
                "slug": "money-stewardship",
                "verses": ["Malachi 3:10", "Luke 16:10-11", "1 Timothy 6:10", "Proverbs 3:9-10"]
            }
        ]
    }

    # Process verse references to add URLs
    for category in study_guides.values():
        for guide in category:
            guide['verse_refs'] = [
                {
                    'text': verse,
                    'url': verse_reference_to_url(verse) or '#'
                }
                for verse in guide['verses']
            ]

    html = templates.get_template("index.html").render(
        {"request": request, "books": books, "daily_verse": daily_verse, "study_guides": study_guides}
    )
    _homepage_cache["date"] = today
    _homepage_cache["html"] = html
    return HTMLResponse(content=html, headers={"Cache-Control": "public, max-age=3600"}
    )


@router.get("/books", response_class=HTMLResponse)
async def books_page(request: Request):
    """Browse all books of the Bible"""
    books = bible.get_books()

    # Define book categories with types
    book_types = {
        # Old Testament
        'Genesis': 'law', 'Exodus': 'law', 'Leviticus': 'law', 'Numbers': 'law', 'Deuteronomy': 'law',
        'Joshua': 'historical', 'Judges': 'historical', 'Ruth': 'historical',
        '1 Samuel': 'historical', '2 Samuel': 'historical', '1 Kings': 'historical', '2 Kings': 'historical',
        '1 Chronicles': 'historical', '2 Chronicles': 'historical', 'Ezra': 'historical',
        'Nehemiah': 'historical', 'Esther': 'historical',
        'Job': 'wisdom', 'Psalms': 'wisdom', 'Proverbs': 'wisdom', 'Ecclesiastes': 'wisdom', 'Song of Solomon': 'wisdom',
        'Isaiah': 'major-prophets', 'Jeremiah': 'major-prophets', 'Lamentations': 'major-prophets',
        'Ezekiel': 'major-prophets', 'Daniel': 'major-prophets',
        'Hosea': 'minor-prophets', 'Joel': 'minor-prophets', 'Amos': 'minor-prophets',
        'Obadiah': 'minor-prophets', 'Jonah': 'minor-prophets', 'Micah': 'minor-prophets',
        'Nahum': 'minor-prophets', 'Habakkuk': 'minor-prophets', 'Zephaniah': 'minor-prophets',
        'Haggai': 'minor-prophets', 'Zechariah': 'minor-prophets', 'Malachi': 'minor-prophets',
        # New Testament
        'Matthew': 'gospels', 'Mark': 'gospels', 'Luke': 'gospels', 'John': 'gospels',
        'Acts': 'acts',
        'Romans': 'pauline', '1 Corinthians': 'pauline', '2 Corinthians': 'pauline',
        'Galatians': 'pauline', 'Ephesians': 'pauline', 'Philippians': 'pauline', 'Colossians': 'pauline',
        '1 Thessalonians': 'pauline', '2 Thessalonians': 'pauline',
        '1 Timothy': 'pauline', '2 Timothy': 'pauline', 'Titus': 'pauline', 'Philemon': 'pauline',
        'Hebrews': 'general', 'James': 'general', '1 Peter': 'general', '2 Peter': 'general',
        '1 John': 'general', '2 John': 'general', '3 John': 'general', 'Jude': 'general',
        'Revelation': 'apocalyptic'
    }

    # Organize books by testament
    old_testament_books = [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
        '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
        'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
        'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
        'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'
    ]

    new_testament_books = [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
        '1 John', '2 John', '3 John', 'Jude', 'Revelation'
    ]

    # Get chapter counts for each book
    def get_chapter_count(book_name):
        chapters = bible.get_chapters_for_book(book_name)
        return len(chapters)

    old_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in old_testament_books
    ]

    new_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in new_testament_books
    ]

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "books.html",
            {
            "old_testament": old_testament,
            "new_testament": new_testament,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    """Browse all theological resources"""
    books = bible.get_books()

    # Organize resources into categories
    resources = {
        "People": [
            {
                "name": "Biblical Prophets",
                "url": "/biblical-prophets",
                "description": "Explore the prophetic ministry throughout Scripture, from Isaiah to Malachi",
                "count": "9 prophets"
            },
            {
                "name": "The Twelve Apostles",
                "url": "/the-twelve-apostles",
                "description": "The twelve disciples chosen by Jesus to be witnesses of His ministry",
                "count": "12 apostles"
            },
            {
                "name": "Women of the Bible",
                "url": "/women-of-the-bible",
                "description": "Notable women of Scripture and their significance in redemptive history",
                "count": "12 women"
            }
        ],
        "Theology": [
            {
                "name": "Biblical Angels",
                "url": "/biblical-angels",
                "description": "Angelic beings mentioned in Scripture, including Michael, Gabriel, and the heavenly host",
                "count": "12 entries"
            },
            {
                "name": "The Tetragrammaton",
                "url": "/tetragrammaton",
                "description": "The sacred four-letter name of God (YHWH) and its profound significance",
                "count": "Deep dive"
            },
            {
                "name": "Names of God",
                "url": "/names-of-god",
                "description": "The revelation of God's names throughout Scripture and their meanings",
                "count": "14 names"
            },
            {
                "name": "Parables of Jesus",
                "url": "/parables",
                "description": "The parables spoken by Christ to illustrate spiritual truths",
                "count": "11 parables"
            },
            {
                "name": "Miracles of Jesus",
                "url": "/miracles-of-jesus",
                "description": "Signs and wonders manifesting divine authority over nature, disease, demons, and death",
                "count": "35+ miracles"
            },
            {
                "name": "I Am Statements",
                "url": "/i-am-statements",
                "description": "The seven 'I Am' statements of Jesus in John's Gospel revealing His divine nature",
                "count": "7 statements"
            },
            {
                "name": "The Beatitudes",
                "url": "/beatitudes",
                "description": "The blessings proclaimed by Jesus in the Sermon on the Mount",
                "count": "8 beatitudes"
            },
            {
                "name": "Ten Commandments",
                "url": "/ten-commandments",
                "description": "The moral law given by God to Moses on Mount Sinai",
                "count": "10 commandments"
            },
            {
                "name": "Armor of God",
                "url": "/armor-of-god",
                "description": "The spiritual equipment for warfare described in Ephesians 6",
                "count": "7 pieces"
            },
            {
                "name": "Prayers of the Bible",
                "url": "/prayers-of-the-bible",
                "description": "Sacred prayers from the Psalms, Jesus, Paul, and the early church",
                "count": "20+ prayers"
            },
            {
                "name": "Biblical Covenants",
                "url": "/biblical-covenants",
                "description": "Divine covenants established between God and His people",
                "count": "7 covenants"
            },
            {
                "name": "Fruits of the Spirit",
                "url": "/fruits-of-the-spirit",
                "description": "The nine graces of Galatians 5:22-23 manifested in believers through the Holy Spirit",
                "count": "9 fruits"
            }
        ],
        "Systematic Theology": [
            {
                "name": "The Trinity",
                "url": "/trinity",
                "description": "The mystery of God revealed as Father, Son, and Holy Spirit—three Persons, one God",
                "count": "4 categories"
            },
            {
                "name": "Christology",
                "url": "/christology",
                "description": "The Person and work of Jesus Christ—His deity, humanity, and offices",
                "count": "4 categories"
            },
            {
                "name": "Pneumatology",
                "url": "/pneumatology",
                "description": "The doctrine of the Holy Spirit—His Person, deity, and work in believers",
                "count": "4 categories"
            },
            {
                "name": "Soteriology",
                "url": "/soteriology",
                "description": "The doctrine of salvation—from election to glorification",
                "count": "5 categories"
            },
            {
                "name": "Ecclesiology",
                "url": "/ecclesiology",
                "description": "The doctrine of the Church—its nature, mission, and governance",
                "count": "4 categories"
            },
            {
                "name": "Eschatology",
                "url": "/eschatology",
                "description": "The doctrine of last things—Christ's return, judgment, and eternal state",
                "count": "5 categories"
            },
            {
                "name": "The Kingdom of God",
                "url": "/kingdom-of-god",
                "description": "God's sovereign reign inaugurated in Christ and consummated at His return",
                "count": "5 categories"
            },
            {
                "name": "Types and Shadows",
                "url": "/types-and-shadows",
                "description": "Old Testament persons, events, and institutions that prefigure Christ",
                "count": "5 categories"
            },
            {
                "name": "Messianic Prophecies",
                "url": "/messianic-prophecies",
                "description": "Old Testament prophecies fulfilled in Jesus Christ",
                "count": "5 categories"
            },
            {
                "name": "The Blood in Scripture",
                "url": "/blood-in-scripture",
                "description": "The theology of blood, sacrifice, and redemption throughout Scripture",
                "count": "5 categories"
            },
            {
                "name": "Names and Titles of Christ",
                "url": "/names-of-christ",
                "description": "The names and titles ascribed to Jesus revealing His Person and work",
                "count": "5 categories"
            },
            {
                "name": "Spirits & Demons",
                "url": "/spirits-and-demons",
                "description": "Biblical demonology—Satan, evil spirits, Legion, and spiritual warfare",
                "count": "7 categories"
            },
            {
                "name": "Personifications",
                "url": "/personifications",
                "description": "Abstract concepts given human form—Wisdom, Folly, Death, Sin, and more",
                "count": "6 categories"
            },
            {
                "name": "Bibliology",
                "url": "/bibliology",
                "description": "The Doctrine of Scripture—inspiration, authority, sufficiency, and preservation",
                "count": "4 categories"
            },
            {
                "name": "Theology Proper",
                "url": "/theology-proper",
                "description": "The Attributes of God—His incommunicable and communicable perfections",
                "count": "4 categories"
            },
            {
                "name": "Anthropology",
                "url": "/anthropology",
                "description": "The Doctrine of Man—creation, constitution, and condition of humanity",
                "count": "4 categories"
            },
            {
                "name": "Hamartiology",
                "url": "/hamartiology",
                "description": "The Doctrine of Sin—its origin, nature, transmission, and consequences",
                "count": "4 categories"
            },
            {
                "name": "Providence",
                "url": "/providence",
                "description": "Divine Providence—God's preservation, governance, and concurrence in all things",
                "count": "4 categories"
            },
            {
                "name": "Grace",
                "url": "/grace",
                "description": "The Doctrine of Grace—common grace, effectual grace, election, and perseverance",
                "count": "4 categories"
            },
            {
                "name": "Justification",
                "url": "/justification",
                "description": "The Doctrine of Justification—declared righteous through faith in Christ alone",
                "count": "4 categories"
            },
            {
                "name": "Sanctification",
                "url": "/sanctification",
                "description": "The Doctrine of Sanctification—progressive holiness through the Spirit",
                "count": "4 categories"
            },
            {
                "name": "Law and Gospel",
                "url": "/law-and-gospel",
                "description": "The distinction between Law and Gospel—God's demands and His gracious provision",
                "count": "4 categories"
            },
            {
                "name": "Worship",
                "url": "/worship",
                "description": "The Doctrine of Worship—regulative principle, elements, and the heart of worship",
                "count": "4 categories"
            }
        ],
        "History & Culture": [
            {
                "name": "Biblical Festivals",
                "url": "/biblical-festivals",
                "description": "The appointed feasts and holy days ordained in the Law of Moses",
                "count": "7 festivals"
            },
            {
                "name": "Biblical Geography",
                "url": "/biblical-maps",
                "description": "Locations mentioned in Scripture and their historical significance",
                "count": "Maps & places",
                "badge": "Interactive"
            },
            {
                "name": "Biblical Timeline",
                "url": "/biblical-timeline",
                "description": "Chronological overview of biblical events from Creation to Revelation",
                "count": "Timeline"
            },
            {
                "name": "Genealogies",
                "url": "/family-tree",
                "description": "Interactive family tree from Adam to Jesus Christ with detailed person profiles",
                "count": "160+ people",
                "badge": "Interactive"
            }
        ],
        "Study Tools": [
            {
                "name": "Study Guides",
                "url": "/study-guides",
                "description": "In-depth guides for studying biblical books, themes, and doctrines",
                "count": "Multiple guides"
            }
        ]
    }

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Resources", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "resources.html",
            {
            "resources": resources,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )
