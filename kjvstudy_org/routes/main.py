"""Main page routes - homepage, books browser, and resources."""
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..kjv import bible
from ..resource_catalog import RESOURCE_CATEGORIES, iter_resources
from ..utils.books import OT_BOOKS, NT_BOOKS
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

    # Doctrine/people resources for the homepage grid, from the shared catalog.
    # Excludes items already surfaced in the Study Resources / Interactive
    # Resources sections above (study guides, family tree, timeline, maps).
    _homepage_exclude = {"/study-guides", "/family-tree", "/biblical-timeline", "/biblical-maps"}
    theology_links = [r for r in iter_resources() if r["url"] not in _homepage_exclude]

    html = templates.get_template("index.html").render(
        {"request": request, "books": books, "daily_verse": daily_verse,
         "study_guides": study_guides, "theology_links": theology_links}
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
        for book in OT_BOOKS
    ]

    new_testament = [
        {
            'name': book,
            'chapters': get_chapter_count(book),
            'available': book in books,
            'type': book_types.get(book, '')
        }
        for book in NT_BOOKS
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

    # Single source of truth: the shared resource catalog
    resources = RESOURCE_CATEGORIES

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
