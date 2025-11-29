"""API routes for KJV Study - JSON endpoints for programmatic access."""
from typing import Optional, List
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse, StreamingResponse

from ..utils.pdf import render_html_to_pdf, render_html_to_pdf_async, WEASYPRINT_AVAILABLE

from ..kjv import bible
from ..cross_references import get_cross_references
from ..reading_plans import get_plan, get_plan_summary
from ..topics import get_all_topics, get_topic
from ..interlinear_loader import get_interlinear_data, has_interlinear_data
from ..utils.books import normalize_book_name, OT_BOOKS
from ..utils.search import perform_full_text_search
from ..utils.helpers import get_daily_verse, create_slug
from ..books import get_book_data, get_all_books_metadata, has_book_data
from ..red_letter import get_christ_words, load_red_letter_verses
from ..stories import (
    get_categories,
    get_story_by_slug,
    get_story_count,
    get_category_count,
    get_all_stories_flat,
)
from ..data import (
    _data as RESOURCES_DATA,
    find_resource_by_slug,
    _create_slug,
    # Import all specific resource dicts
    BIBLICAL_LOCATIONS, ANGELS_DATA, PROPHETS_DATA, NAMES_DATA,
    PARABLES_DATA, COVENANTS_DATA, APOSTLES_DATA, WOMEN_DATA,
    FESTIVALS_DATA, FRUITS_DATA, MIRACLES_DATA, PRAYERS_DATA,
    BEATITUDES_DATA, TEN_COMMANDMENTS_DATA, ARMOR_OF_GOD_DATA,
    I_AM_STATEMENTS_DATA, TRINITY_DATA, CHRISTOLOGY_DATA,
    SOTERIOLOGY_DATA, PNEUMATOLOGY_DATA, ESCHATOLOGY_DATA,
    ECCLESIOLOGY_DATA, TYPES_AND_SHADOWS_DATA, MESSIANIC_PROPHECIES_DATA,
    BLOOD_IN_SCRIPTURE_DATA, KINGDOM_OF_GOD_DATA, NAMES_OF_CHRIST_DATA,
    SPIRITS_AND_DEMONS_DATA, PERSONIFICATIONS_DATA, BIBLIOLOGY_DATA,
    THEOLOGY_PROPER_DATA, ANTHROPOLOGY_DATA, HAMARTIOLOGY_DATA,
    PROVIDENCE_DATA, GRACE_DATA, JUSTIFICATION_DATA, SANCTIFICATION_DATA,
    LAW_AND_GOSPEL_DATA, WORSHIP_DATA
)

router = APIRouter(prefix="/api", tags=["API"])

# Templates will be set by the main app
templates = None


# Pydantic models for API responses
class VerseResponse(BaseModel):
    """Response model for a single verse"""
    book: str = Field(..., json_schema_extra={"example": "John"})
    chapter: int = Field(..., json_schema_extra={"example": 3})
    verse: int = Field(..., json_schema_extra={"example": 16})
    reference: str = Field(..., json_schema_extra={"example": "John 3:16"})
    text: str = Field(..., json_schema_extra={"example": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."})
    red_letter: Optional[str] = Field(
        None,
        description="Words of Christ: null if Jesus doesn't speak, 'full' if entire verse, or the quoted words if partial",
        json_schema_extra={"example": "full"}
    )


class VerseInRange(BaseModel):
    """Single verse within a range"""
    verse: int = Field(..., json_schema_extra={"example": 1})
    text: str = Field(..., json_schema_extra={"example": "The LORD is my shepherd; I shall not want."})
    red_letter: Optional[str] = Field(
        None,
        description="Words of Christ: null if Jesus doesn't speak, 'full' if entire verse, or the quoted words if partial"
    )


class VerseRangeResponse(BaseModel):
    """Response model for a range of verses"""
    book: str = Field(..., json_schema_extra={"example": "Psalms"})
    chapter: int = Field(..., json_schema_extra={"example": 23})
    start: int = Field(..., json_schema_extra={"example": 1})
    end: int = Field(..., json_schema_extra={"example": 6})
    reference: str = Field(..., json_schema_extra={"example": "Psalms 23:1-6"})
    verses: List[VerseInRange]
    text: str = Field(..., json_schema_extra={"example": "The LORD is my shepherd; I shall not want..."})


class DailyVerseResponse(BaseModel):
    """Response model for verse of the day"""
    book: str = Field(..., json_schema_extra={"example": "John"})
    chapter: int = Field(..., json_schema_extra={"example": 3})
    verse: int = Field(..., json_schema_extra={"example": 16})
    text: str = Field(..., json_schema_extra={"example": "For God so loved the world..."})
    reference: str = Field(..., json_schema_extra={"example": "John 3:16"})
    url: str = Field(..., json_schema_extra={"example": "/book/John/chapter/3#verse-16"})
    red_letter: Optional[str] = Field(
        None,
        description="Words of Christ: null if Jesus doesn't speak, 'full' if entire verse, or the quoted words if partial",
        json_schema_extra={"example": "full"}
    )


class ResourceVerse(BaseModel):
    """Verse reference in a resource"""
    reference: str = Field(..., json_schema_extra={"example": "Genesis 2:8"})
    text: str = Field(..., json_schema_extra={"example": "And the LORD God planted a garden..."})


class ResourceCategoryInfo(BaseModel):
    """Information about a resource category"""
    name: str = Field(..., json_schema_extra={"example": "biblical_locations"})
    title: str = Field(..., json_schema_extra={"example": "Biblical Locations"})
    item_count: int = Field(..., json_schema_extra={"example": 15})
    url: str = Field(..., json_schema_extra={"example": "/api/resources/biblical_locations"})
    html_url: str = Field(..., json_schema_extra={"example": "/biblical-locations"})


class ResourcesListResponse(BaseModel):
    """Response listing all resource categories"""
    total_categories: int = Field(..., json_schema_extra={"example": 39})
    categories: List[ResourceCategoryInfo]


class ResourceItemSummary(BaseModel):
    """Summary of a resource item"""
    name: str = Field(..., json_schema_extra={"example": "Garden of Eden"})
    slug: str = Field(..., json_schema_extra={"example": "garden-of-eden"})
    description: str = Field(..., json_schema_extra={"example": "The original home of mankind"})
    verse_count: int = Field(..., json_schema_extra={"example": 2})
    url: str = Field(..., json_schema_extra={"example": "/api/resources/biblical_locations/garden-of-eden"})


class ResourceCategoryResponse(BaseModel):
    """Response for a specific resource category"""
    category: str = Field(..., json_schema_extra={"example": "biblical_locations"})
    title: str = Field(..., json_schema_extra={"example": "Biblical Locations"})
    total_items: int = Field(..., json_schema_extra={"example": 15})
    items: List[ResourceItemSummary]


class ResourceItemDetail(BaseModel):
    """Detailed information about a specific resource item"""
    name: str = Field(..., json_schema_extra={"example": "Garden of Eden"})
    slug: str = Field(..., json_schema_extra={"example": "garden-of-eden"})
    category: str = Field(..., json_schema_extra={"example": "biblical_locations"})
    description: str = Field(..., json_schema_extra={"example": "The original home of mankind"})
    verses: List[ResourceVerse]


class RedLetterVerse(BaseModel):
    """A verse containing words of Christ"""
    reference: str = Field(..., json_schema_extra={"example": "John 3:16"})
    book: str = Field(..., json_schema_extra={"example": "John"})
    chapter: int = Field(..., json_schema_extra={"example": 3})
    verse: int = Field(..., json_schema_extra={"example": 16})
    text: str = Field(..., json_schema_extra={"example": "For God so loved the world..."})
    christ_words: str = Field(..., json_schema_extra={"example": "full"})
    is_full_verse: bool = Field(..., json_schema_extra={"example": True})


class RedLetterListResponse(BaseModel):
    """Response listing red letter verses"""
    total: int = Field(..., json_schema_extra={"example": 1842})
    verses: List[RedLetterVerse]
    limit: int = Field(..., json_schema_extra={"example": 50})
    offset: int = Field(..., json_schema_extra={"example": 0})


class RedLetterStatsResponse(BaseModel):
    """Statistics about red letter verses"""
    total_verses: int = Field(..., json_schema_extra={"example": 1842})
    full_verses: int = Field(..., json_schema_extra={"example": 1456})
    partial_verses: int = Field(..., json_schema_extra={"example": 386})
    books_with_red_letter: List[str] = Field(..., json_schema_extra={"example": ["Matthew", "Mark", "Luke", "John"]})
    by_book: dict = Field(..., json_schema_extra={"example": {"Matthew": 644, "Mark": 285}})


# Mapping of category names to their data dictionaries
CATEGORY_TO_DATA = {
    'biblical_locations': BIBLICAL_LOCATIONS,
    'angels': ANGELS_DATA,
    'prophets': PROPHETS_DATA,
    'names': NAMES_DATA,
    'parables': PARABLES_DATA,
    'covenants': COVENANTS_DATA,
    'apostles': APOSTLES_DATA,
    'women': WOMEN_DATA,
    'festivals': FESTIVALS_DATA,
    'fruits': FRUITS_DATA,
    'miracles': MIRACLES_DATA,
    'prayers': PRAYERS_DATA,
    'beatitudes': BEATITUDES_DATA,
    'ten_commandments': TEN_COMMANDMENTS_DATA,
    'armor_of_god': ARMOR_OF_GOD_DATA,
    'i_am_statements': I_AM_STATEMENTS_DATA,
    'trinity': TRINITY_DATA,
    'christology': CHRISTOLOGY_DATA,
    'soteriology': SOTERIOLOGY_DATA,
    'pneumatology': PNEUMATOLOGY_DATA,
    'eschatology': ESCHATOLOGY_DATA,
    'ecclesiology': ECCLESIOLOGY_DATA,
    'types_and_shadows': TYPES_AND_SHADOWS_DATA,
    'messianic_prophecies': MESSIANIC_PROPHECIES_DATA,
    'blood_in_scripture': BLOOD_IN_SCRIPTURE_DATA,
    'kingdom_of_god': KINGDOM_OF_GOD_DATA,
    'names_of_christ': NAMES_OF_CHRIST_DATA,
    'spirits_and_demons': SPIRITS_AND_DEMONS_DATA,
    'personifications': PERSONIFICATIONS_DATA,
    'bibliology': BIBLIOLOGY_DATA,
    'theology_proper': THEOLOGY_PROPER_DATA,
    'anthropology': ANTHROPOLOGY_DATA,
    'hamartiology': HAMARTIOLOGY_DATA,
    'providence': PROVIDENCE_DATA,
    'grace': GRACE_DATA,
    'justification': JUSTIFICATION_DATA,
    'sanctification': SANCTIFICATION_DATA,
    'law_and_gospel': LAW_AND_GOSPEL_DATA,
    'worship': WORSHIP_DATA
}


def init_templates(app_templates):
    """Initialize templates from the main app."""
    global templates
    templates = app_templates


@router.get("/")
def api_index():
    """API index with links to documentation and available endpoints."""
    return {
        "name": "KJV Study API",
        "version": "1.0.0",
        "description": "RESTful API for accessing King James Bible verses and study resources",
        "documentation": {
            "swagger_ui": "/api/docs",
            "redoc": "/api/redoc",
            "openapi_json": "/api/openapi.json"
        },
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search?q={query}",
            "verse_of_the_day": "/api/verse-of-the-day",
            "verse": "/api/verse/{book}/{chapter}/{verse}",
            "verse_range": "/api/verse-range/{book}/{chapter}/{start}/{end}",
            "interlinear": "/api/interlinear/{book}/{chapter}/{verse}",
            "books": "/api/books",
            "book": "/api/books/{book}",
            "chapter": "/api/books/{book}/chapters/{chapter}",
            "book_text": "/api/books/{book}/text",
            "bible": "/api/bible",
            "cross_references": "/api/cross-references/{book}/{chapter}/{verse}",
            "topics": "/api/topics",
            "topic": "/api/topics/{topic_name}",
            "reading_plans": "/api/reading-plans",
            "reading_plan": "/api/reading-plans/{plan_id}",
            "stories": "/api/stories",
            "story": "/api/stories/{slug}",
            "red_letter": "/api/red-letter?book={book}&limit={limit}&offset={offset}",
            "red_letter_stats": "/api/red-letter/stats"
        }
    }


@router.get("/health")
def api_health_check():
    """API health check endpoint for monitoring and status verification."""
    return {
        "status": "healthy",
        "service": "KJV Study API",
        "version": "1.0.0"
    }


@router.get("/search")
def search_api(
    q: str = Query(..., description="Search query", example="faith"),
    limit: Optional[int] = Query(None, description="Max results", example=10)
):
    """JSON API endpoint for search."""
    if not q or len(q.strip()) < 2:
        return {"query": q, "results": [], "total": 0}

    results = perform_full_text_search(q.strip(), limit)
    is_direct_verse = False

    # Check if this was a direct verse reference match
    if results and len(results) == 1 and results[0].get("score") == 100.0:
        is_direct_verse = True

    return {
        "query": q,
        "results": results,
        "total": len(results),
        "is_direct_verse": is_direct_verse
    }


@router.get("/universal-search")
def universal_search_api(
    q: str = Query(..., description="Search query", example="love"),
    limit: int = Query(5, description="Max results per category", example=5)
):
    """Universal search across all content types."""
    if not q or len(q.strip()) < 2:
        return {"query": q, "results": {}}

    query = q.strip().lower()
    results = {}

    # Search Bible books (with common synonyms/misspellings)
    book_synonyms = {
        "song of songs": "Song of Solomon",
        "canticles": "Song of Solomon",
        "revelations": "Revelation",
        "apocalypse": "Revelation",
        "psalters": "Psalms",
        "proverb": "Proverbs",
        "ecclesiast": "Ecclesiastes",
        "lament": "Lamentations",
        "phil": "Philippians",
        "1 sam": "1 Samuel",
        "2 sam": "2 Samuel",
        "1 kin": "1 Kings",
        "2 kin": "2 Kings",
        "1 chron": "1 Chronicles",
        "2 chron": "2 Chronicles",
        "1 cor": "1 Corinthians",
        "2 cor": "2 Corinthians",
        "1 thess": "1 Thessalonians",
        "2 thess": "2 Thessalonians",
        "1 tim": "1 Timothy",
        "2 tim": "2 Timothy",
        "1 pet": "1 Peter",
        "2 pet": "2 Peter",
        "1 joh": "1 John",
        "2 joh": "2 John",
        "3 joh": "3 John",
    }
    all_books = bible.get_books()
    matching_books = []

    # Check for synonym matches first
    for synonym, book_name in book_synonyms.items():
        if query in synonym and book_name not in [b["name"] for b in matching_books]:
            matching_books.append({"name": book_name, "url": f"/book/{book_name}"})

    # Then check direct book name matches
    for book in all_books:
        if query in book.lower() and book not in [b["name"] for b in matching_books]:
            matching_books.append({"name": book, "url": f"/book/{book}"})

    matching_books = matching_books[:limit]
    if matching_books:
        results["books"] = matching_books

    # Search Bible verses (limit to top results for speed)
    verse_results = perform_full_text_search(q.strip(), limit)
    if verse_results:
        results["verses"] = [
            {
                "reference": r["reference"],
                "text": r["text"][:100] + "..." if len(r.get("text", "")) > 100 else r.get("text", ""),
                "url": f"/book/{r['book']}/chapter/{r['chapter']}/verse/{r['verse']}"
            }
            for r in verse_results
        ]

    # Search topics
    all_topics = get_all_topics()
    matching_topics = [
        {"name": name.replace("_", " ").title(), "url": f"/topics/{name}"}
        for name, data in all_topics.items()
        if query in name.lower() or query in data.get("description", "").lower()
    ][:limit]
    if matching_topics:
        results["topics"] = matching_topics

    # Search stories
    all_stories = get_all_stories_flat()
    matching_stories = [
        {
            "title": s["title"],
            "url": f"/stories/{s['slug']}",
            "category": s.get("category_name", "")
        }
        for s in all_stories
        if query in s.get("title", "").lower() or query in s.get("description", "").lower()
    ][:limit]
    if matching_stories:
        results["stories"] = matching_stories

    # Search reading plans
    from ..reading_plans import READING_PLANS
    matching_plans = [
        {"name": plan["name"], "url": f"/reading-plans/{plan_id}"}
        for plan_id, plan in READING_PLANS.items()
        if query in plan["name"].lower() or query in plan.get("description", "").lower()
    ][:limit]
    if matching_plans:
        results["plans"] = matching_plans

    # Search resources (theological studies, biblical figures, etc.)
    resources_to_search = [
        # Theological studies with synonyms
        ("trinity godhead three persons father son spirit", "/trinity", "The Trinity"),
        ("christology jesus christ lord savior messiah", "/christology", "Christology"),
        ("soteriology salvation saved redemption atonement", "/soteriology", "Soteriology"),
        ("pneumatology holy spirit ghost comforter paraclete", "/pneumatology", "Pneumatology"),
        ("eschatology end times last days rapture tribulation millennium", "/eschatology", "Eschatology"),
        ("ecclesiology church body believers congregation", "/ecclesiology", "Ecclesiology"),
        ("types_and_shadows typology foreshadow prefigure", "/types-and-shadows", "Types and Shadows"),
        ("messianic_prophecies prophecy predictions foretold", "/messianic-prophecies", "Messianic Prophecies"),
        ("blood_in_scripture sacrifice atonement covering", "/blood-in-scripture", "The Blood in Scripture"),
        ("kingdom_of_god reign throne rule", "/kingdom-of-god", "The Kingdom of God"),
        ("names_of_christ jesus titles lord savior", "/names-of-christ", "Names of Christ"),
        ("spirits_and_demons devils satan evil unclean", "/spirits-and-demons", "Spirits and Demons"),
        ("personifications wisdom folly death", "/personifications", "Personifications"),
        ("angels cherubim seraphim michael gabriel", "/biblical-angels", "Biblical Angels"),
        ("prophets elijah elisha isaiah jeremiah ezekiel daniel", "/biblical-prophets", "Biblical Prophets"),
        ("names_of_god yahweh jehovah el shaddai adonai", "/names-of-god", "Names of God"),
        ("parables stories teachings", "/parables", "Parables of Jesus"),
        ("covenants abrahamic mosaic davidic new", "/biblical-covenants", "Biblical Covenants"),
        ("apostles disciples twelve peter james john", "/the-twelve-apostles", "The Twelve Apostles"),
        ("women ruth esther mary martha rahab", "/women-of-the-bible", "Women of the Bible"),
        ("festivals passover pentecost tabernacles feast", "/biblical-festivals", "Biblical Festivals"),
        ("fruits love joy peace patience kindness goodness faithfulness gentleness self-control", "/fruits-of-the-spirit", "Fruits of the Spirit"),
        ("miracles healing signs wonders", "/miracles-of-jesus", "Miracles of Jesus"),
        ("prayers lord's prayer model", "/prayers-of-the-bible", "Prayers of the Bible"),
        ("beatitudes blessed sermon mount", "/beatitudes", "The Beatitudes"),
        ("ten_commandments decalogue law sinai", "/ten-commandments", "Ten Commandments"),
        ("armor_of_god warfare helmet breastplate shield sword", "/armor-of-god", "Armor of God"),
        ("i_am_statements bread light door shepherd resurrection way truth life vine", "/i-am-statements", "I Am Statements"),
        ("tetragrammaton yhwh yahweh jehovah lord", "/tetragrammaton", "The Tetragrammaton"),
        ("timeline chronology history dates", "/biblical-timeline", "Biblical Timeline"),
        ("family_tree genealogy lineage ancestors descendants", "/family-tree", "Biblical Genealogies"),
        ("interlinear hebrew greek original language", "/interlinear", "Interlinear Bible"),
        ("concordance word search find", "/concordance", "Concordance"),
        ("study_guides", "/study-guides", "Study Guides"),
        ("maps geography places locations", "/maps", "Bible Maps"),
        # Individual study guides
        ("new believer faith basics beginner", "/study-guides/new-believer", "New Believer's Guide"),
        ("salvation saved born again", "/study-guides/salvation", "Understanding Salvation"),
        ("gospel good news", "/study-guides/gospel", "The Gospel Message"),
        ("fruits spirit love joy peace", "/study-guides/fruits-spirit", "Fruits of the Spirit Guide"),
        ("prayer faith praying", "/study-guides/prayer-faith", "Prayer & Faith"),
        ("christian living walk daily", "/study-guides/christian-living", "Christian Living"),
        ("god's love agape", "/study-guides/gods-love", "God's Love"),
        ("hope comfort suffering trials", "/study-guides/hope-comfort", "Hope & Comfort"),
        ("wisdom guidance direction decisions", "/study-guides/wisdom-guidance", "Wisdom & Guidance"),
        ("trinity father son spirit", "/study-guides/trinity", "Trinity Study Guide"),
        ("resurrection risen easter", "/study-guides/resurrection", "The Resurrection"),
        ("heaven eternity afterlife", "/study-guides/heaven-eternity", "Heaven & Eternity"),
        ("sovereignty of god control providence", "/study-guides/sovereignty-of-god", "Sovereignty of God"),
        ("attributes of god character nature", "/study-guides/attributes-of-god", "Attributes of God"),
        ("doctrine of scripture bible inspiration inerrancy", "/study-guides/doctrine-of-scripture", "Doctrine of Scripture"),
        ("problem of evil theodicy suffering why", "/study-guides/problem-of-evil", "Problem of Evil"),
        ("covenant theology dispensation", "/study-guides/covenant-theology", "Covenant Theology"),
        ("spirits demons spiritual warfare", "/study-guides/spirits-demons", "Spirits & Demons Guide"),
        ("gospel in old testament types shadows", "/study-guides/gospel-in-ot", "Gospel in the Old Testament"),
        ("law and christian grace mosaic", "/study-guides/law-and-christian", "The Law and the Christian"),
        ("faith and works james paul", "/study-guides/faith-and-works", "Faith and Works"),
        ("scarlet thread redemption blood", "/study-guides/scarlet-thread", "Scarlet Thread of Redemption"),
        ("biblical marriage husband wife", "/study-guides/biblical-marriage", "Biblical Marriage"),
        ("raising children parenting family", "/study-guides/raising-children", "Raising Children"),
        ("money stewardship finances tithe giving", "/study-guides/money-stewardship", "Money & Stewardship"),
        # Biblical figures (link to family tree)
        ("adam eve first man woman creation", "/family-tree/adam", "Adam"),
        ("noah ark flood", "/family-tree/noah", "Noah"),
        ("abraham abram father faith", "/family-tree/abraham", "Abraham"),
        ("isaac son promise", "/family-tree/isaac", "Isaac"),
        ("jacob israel twelve tribes", "/family-tree/jacob", "Jacob"),
        ("joseph dreamer coat egypt", "/family-tree/joseph", "Joseph"),
        ("moses exodus law lawgiver", "/family-tree/moses", "Moses"),
        ("david king shepherd psalmist", "/family-tree/david", "David"),
        ("solomon wisdom temple", "/family-tree/solomon", "Solomon"),
        ("paul apostle gentiles saul tarsus", "/family-tree/paul", "Paul the Apostle"),
    ]
    matching_resources = [
        {"name": name, "url": url}
        for key, url, name in resources_to_search
        if query in key.lower() or query in name.lower()
    ][:limit]
    if matching_resources:
        results["resources"] = matching_resources

    return {"query": q, "results": results}


@router.get(
    "/verse-of-the-day",
    response_model=DailyVerseResponse,
    summary="Get verse of the day",
    description="Returns a featured verse that changes daily"
)
def verse_of_the_day_api():
    """API endpoint for verse of the day."""
    return get_daily_verse()


@router.get(
    "/verse/{book}/{chapter}/{verse}",
    response_model=VerseResponse,
    summary="Get a single verse",
    description="Retrieve a specific Bible verse by book, chapter, and verse number. Includes red letter (words of Christ) information.",
    responses={
        200: {
            "description": "Successfully retrieved verse",
            "content": {
                "application/json": {
                    "examples": {
                        "jesus_speaks": {
                            "summary": "Verse where Jesus speaks (full)",
                            "value": {
                                "book": "John",
                                "chapter": 3,
                                "verse": 16,
                                "reference": "John 3:16",
                                "text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
                                "red_letter": "full"
                            }
                        },
                        "no_jesus": {
                            "summary": "Verse without Jesus speaking",
                            "value": {
                                "book": "Genesis",
                                "chapter": 1,
                                "verse": 1,
                                "reference": "Genesis 1:1",
                                "text": "In the beginning God created the heaven and the earth.",
                                "red_letter": None
                            }
                        },
                        "partial_jesus": {
                            "summary": "Verse where Jesus speaks part of it",
                            "value": {
                                "book": "Matthew",
                                "chapter": 4,
                                "verse": 4,
                                "reference": "Matthew 4:4",
                                "text": "But he answered and said, It is written, Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God.",
                                "red_letter": "It is written, Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God."
                            }
                        }
                    }
                }
            }
        }
    }
)
def api_get_verse(
    book: str = Path(..., description="Book name (supports abbreviations)", example="John"),
    chapter: int = Path(..., description="Chapter number", example=3, ge=1),
    verse: int = Path(..., description="Verse number", example=16, ge=1)
):
    """Get a single verse with red letter information."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    # Check if book exists
    all_books = bible.get_books()
    if book not in all_books:
        raise HTTPException(status_code=404, detail=f"Book '{book}' not found")

    # Check valid chapter/verse numbers
    if chapter < 1 or verse < 1:
        raise HTTPException(status_code=404, detail="Invalid chapter or verse number")

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        raise HTTPException(status_code=404, detail="Verse not found")

    # Get red letter information (words of Christ)
    christ_words = get_christ_words(book, chapter, verse)

    return JSONResponse({
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "reference": f"{book} {chapter}:{verse}",
        "text": verse_text,
        "red_letter": christ_words
    })


@router.get(
    "/verse-range/{book}/{chapter}/{start}/{end}",
    response_model=VerseRangeResponse,
    summary="Get a range of verses",
    description="Retrieve multiple consecutive verses from a chapter. Each verse includes red letter information.",
    responses={
        200: {
            "description": "Successfully retrieved verse range",
            "content": {
                "application/json": {
                    "examples": {
                        "sermon_on_mount": {
                            "summary": "Beatitudes (Jesus speaking)",
                            "value": {
                                "book": "Matthew",
                                "chapter": 5,
                                "start": 3,
                                "end": 5,
                                "reference": "Matthew 5:3-5",
                                "verses": [
                                    {
                                        "verse": 3,
                                        "text": "Blessed are the poor in spirit: for their's is the kingdom of heaven.",
                                        "red_letter": "full"
                                    },
                                    {
                                        "verse": 4,
                                        "text": "Blessed are they that mourn: for they shall be comforted.",
                                        "red_letter": "full"
                                    },
                                    {
                                        "verse": 5,
                                        "text": "Blessed are the meek: for they shall inherit the earth.",
                                        "red_letter": "full"
                                    }
                                ],
                                "text": "Blessed are the poor in spirit: for their's is the kingdom of heaven. Blessed are they that mourn: for they shall be comforted. Blessed are the meek: for they shall inherit the earth."
                            }
                        },
                        "psalm": {
                            "summary": "Psalm 23 excerpt (no Jesus)",
                            "value": {
                                "book": "Psalms",
                                "chapter": 23,
                                "start": 1,
                                "end": 3,
                                "reference": "Psalms 23:1-3",
                                "verses": [
                                    {
                                        "verse": 1,
                                        "text": "The LORD is my shepherd; I shall not want.",
                                        "red_letter": None
                                    },
                                    {
                                        "verse": 2,
                                        "text": "He maketh me to lie down in green pastures: he leadeth me beside the still waters.",
                                        "red_letter": None
                                    },
                                    {
                                        "verse": 3,
                                        "text": "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.",
                                        "red_letter": None
                                    }
                                ],
                                "text": "The LORD is my shepherd; I shall not want. He maketh me to lie down in green pastures: he leadeth me beside the still waters. He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."
                            }
                        }
                    }
                }
            }
        }
    }
)
def api_get_verse_range(
    book: str = Path(..., description="Book name (supports abbreviations)", example="Psalms"),
    chapter: int = Path(..., description="Chapter number", example=23, ge=1),
    start: int = Path(..., description="Starting verse number", example=1, ge=1),
    end: int = Path(..., description="Ending verse number", example=6, ge=1)
):
    """Get a range of verses with red letter information."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    # Check if book exists
    all_books = bible.get_books()
    if book not in all_books:
        raise HTTPException(status_code=404, detail=f"Book '{book}' not found")

    # Check valid verse numbers
    if chapter < 1 or start < 1 or end < 1:
        raise HTTPException(status_code=404, detail="Invalid chapter or verse number")

    verses = []
    verse_texts = []

    for verse_num in range(start, end + 1):
        verse_text = bible.get_verse_text(book, chapter, verse_num)
        if verse_text:
            christ_words = get_christ_words(book, chapter, verse_num)
            verses.append({
                "verse": verse_num,
                "text": verse_text,
                "red_letter": christ_words
            })
            verse_texts.append(verse_text)

    if not verses:
        raise HTTPException(status_code=404, detail="Verse range not found")

    return JSONResponse({
        "book": book,
        "chapter": chapter,
        "start": start,
        "end": end,
        "reference": f"{book} {chapter}:{start}-{end}",
        "verses": verses,
        "text": " ".join(verse_texts)
    })


@router.get("/interlinear/{book}/{chapter}/{verse}")
def api_get_interlinear(
    book: str = Path(..., description="Book name", example="John"),
    chapter: int = Path(..., description="Chapter number", example=1),
    verse: int = Path(..., description="Verse number", example=1)
):
    """Get interlinear (word-by-word) data for a verse."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    # Check if book exists
    all_books = bible.get_books()
    if book not in all_books:
        raise HTTPException(status_code=404, detail=f"Book '{book}' not found")

    # Check valid chapter/verse numbers
    if chapter < 1 or verse < 1:
        raise HTTPException(status_code=404, detail="Invalid chapter or verse number")

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        raise HTTPException(status_code=404, detail="Verse not found")

    if not has_interlinear_data(book, chapter, verse):
        return JSONResponse({
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text,
            "interlinear_available": False,
            "words": []
        })

    interlinear_words = get_interlinear_data(book, chapter, verse)

    return JSONResponse({
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "reference": f"{book} {chapter}:{verse}",
        "text": verse_text,
        "interlinear_available": True,
        "words": interlinear_words
    })


@router.get("/books")
def api_get_books():
    """Get list of all Bible books with metadata."""
    books = bible.get_books()

    old_testament = []
    new_testament = []

    for book in books:
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
        book_data = get_book_data(book) if has_book_data(book) else None

        book_info = {
            "name": book,
            "chapters": len(chapters),
            "testament": "Old Testament" if book in OT_BOOKS else "New Testament"
        }

        # Add metadata from book introductions if available
        if book_data:
            book_info["abbreviation"] = book_data.get("abbreviation")
            book_info["category"] = book_data.get("category")
            book_info["author"] = book_data.get("author")
            book_info["position"] = book_data.get("position")

        if book in OT_BOOKS:
            old_testament.append(book_info)
        else:
            new_testament.append(book_info)

    return {
        "total_books": len(books),
        "old_testament": old_testament,
        "new_testament": new_testament
    }


@router.get("/books/{book}")
def api_get_book(book: str = Path(..., description="Book name", example="Genesis")):
    """Get details about a specific book including introduction and study material."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
    if not chapters:
        raise HTTPException(status_code=404, detail="Book not found")

    chapter_details = []
    for chapter in chapters:
        verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
        chapter_details.append({
            "chapter": chapter,
            "verses": len(verses)
        })

    result = {
        "name": book,
        "total_chapters": len(chapters),
        "chapters": chapter_details,
        "links": {
            "pdf": f"/api/books/{book}/pdf"
        }
    }

    # Add book introduction data if available
    book_data = get_book_data(book) if has_book_data(book) else None
    if book_data:
        result["abbreviation"] = book_data.get("abbreviation")
        result["testament"] = book_data.get("testament")
        result["position"] = book_data.get("position")
        result["category"] = book_data.get("category")
        result["author"] = book_data.get("author")
        result["date_written"] = book_data.get("date_written")
        result["introduction"] = book_data.get("introduction")
        result["key_themes"] = book_data.get("key_themes")
        result["key_verses"] = book_data.get("key_verses")
        result["outline"] = book_data.get("outline")
        result["historical_context"] = book_data.get("historical_context")
        result["literary_style"] = book_data.get("literary_style")
        result["christ_in_book"] = book_data.get("christ_in_book")
        result["practical_application"] = book_data.get("practical_application")

    return result


@router.get("/books/{book}/pdf")
async def api_book_pdf(book: str = Path(..., description="Book name", example="Genesis")):
    """Generate PDF for an entire Bible book."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
    if not chapters:
        raise HTTPException(status_code=404, detail="Book not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Prepare data for template
    chapters_data = []
    total_verses = 0
    for chapter in chapters:
        verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
        if verses:
            chapter_verses = []
            for v in verses:
                chapter_verses.append({
                    "verse": v.verse,
                    "text": v.text
                })
            chapters_data.append({
                "chapter": chapter,
                "verses": chapter_verses
            })
            total_verses += len(verses)

    if not chapters_data:
        raise HTTPException(status_code=404, detail="No verses found for this book")

    # Render the PDF template
    html_content = templates.get_template("book_pdf.html").render(
        book=book,
        chapters=chapters_data,
        chapter_count=len(chapters_data),
        verse_count=total_verses,
    )

    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Return as downloadable PDF
    filename = f"{create_slug(book)}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/books/{book}/chapters/{chapter}")
def api_get_chapter(
    book: str = Path(..., description="Book name", example="Romans"),
    chapter: int = Path(..., description="Chapter number", example=8)
):
    """Get all verses in a chapter."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")

    verse_list = []
    for v in verses:
        verse_list.append({
            "verse": v.verse,
            "text": v.text
        })

    return {
        "book": book,
        "chapter": chapter,
        "total_verses": len(verses),
        "verses": verse_list,
        "links": {
            "pdf": f"/api/books/{book}/chapters/{chapter}/pdf"
        }
    }


@router.get("/books/{book}/chapters/{chapter}/pdf")
async def api_chapter_pdf(
    book: str = Path(..., description="Book name", example="Romans"),
    chapter: int = Path(..., description="Chapter number", example=8)
):
    """Generate PDF for a specific Bible chapter."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Prepare data for template
    verse_list = []
    for v in verses:
        verse_list.append({
            "verse": v.verse,
            "text": v.text
        })

    # Render the PDF template
    html_content = templates.get_template("chapter_pdf.html").render(
        book=book,
        chapter=chapter,
        verses=verse_list,
        verse_count=len(verses),
    )

    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Return as downloadable PDF
    filename = f"{create_slug(book)}-chapter-{chapter}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/books/{book}/text")
def api_get_book_text(book: str = Path(..., description="Book name", example="Philemon")):
    """Get all text content of a book."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book]
    if not verses:
        raise HTTPException(status_code=404, detail="Book not found")

    chapters = {}
    for v in verses:
        if v.chapter not in chapters:
            chapters[v.chapter] = []
        chapters[v.chapter].append({
            "verse": v.verse,
            "text": v.text
        })

    chapter_list = []
    for chapter_num in sorted(chapters.keys()):
        chapter_list.append({
            "chapter": chapter_num,
            "verses": chapters[chapter_num]
        })

    return {
        "book": book,
        "total_chapters": len(chapters),
        "total_verses": len(verses),
        "chapters": chapter_list
    }


@router.get("/bible")
def api_get_bible():
    """Get the entire Bible text."""
    books_data = {}
    for v in bible.iter_verses():
        if v.book not in books_data:
            books_data[v.book] = {}
        if v.chapter not in books_data[v.book]:
            books_data[v.book][v.chapter] = []
        books_data[v.book][v.chapter].append({
            "verse": v.verse,
            "text": v.text
        })

    books_list = []
    for book_name in books_data:
        chapter_list = []
        for chapter_num in sorted(books_data[book_name].keys()):
            chapter_list.append({
                "chapter": chapter_num,
                "verses": books_data[book_name][chapter_num]
            })

        books_list.append({
            "book": book_name,
            "chapters": chapter_list
        })

    total_verses = sum(len(books_data[book][ch]) for book in books_data for ch in books_data[book])

    return {
        "total_books": len(books_data),
        "total_verses": total_verses,
        "books": books_list
    }


@router.get("/cross-references/{book}/{chapter}/{verse}")
def api_get_cross_references(
    book: str = Path(..., description="Book name", example="John"),
    chapter: int = Path(..., description="Chapter number", example=3),
    verse: int = Path(..., description="Verse number", example=16)
):
    """Get cross-references for a verse."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        raise HTTPException(status_code=404, detail="Verse not found")

    cross_refs = get_cross_references(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "reference": f"{book} {chapter}:{verse}",
        "cross_references": cross_refs
    }


@router.get("/topics")
def api_get_topics():
    """Get list of all topics."""
    topics = get_all_topics()

    topic_list = []
    for topic_name, topic_data in topics.items():
        topic_list.append({
            "name": topic_name,
            "slug": topic_name,
            "description": topic_data.get("description", ""),
            "subtopics": list(topic_data.get("subtopics", {}).keys())
        })

    return {
        "total_topics": len(topics),
        "topics": topic_list
    }


@router.get("/topics/{topic_name}")
def api_get_topic(topic_name: str = Path(..., description="Topic name", example="faith")):
    """Get details about a specific topic."""
    topic = get_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    return {
        "name": topic_name,
        "description": topic.get("description", ""),
        "overview": topic.get("overview", ""),
        "subtopics": topic.get("subtopics", {})
    }


@router.get("/reading-plans")
def api_get_reading_plans():
    """Get list of all reading plans."""
    plans = get_plan_summary()

    return {
        "total_plans": len(plans),
        "plans": plans
    }


@router.get("/reading-plans/{plan_id}")
def api_get_reading_plan(plan_id: str = Path(..., description="Reading plan ID", example="chronological")):
    """Get details about a specific reading plan."""
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    return plan


@router.get("/stories")
def api_get_stories():
    """Get list of all Bible stories organized by category."""
    categories = get_categories()
    story_count = get_story_count()
    category_count = get_category_count()

    # Format categories for API response
    categories_list = []
    for category in categories:
        stories_list = []
        for story in category.get("stories", []):
            stories_list.append({
                "title": story.get("title"),
                "slug": story.get("slug"),
                "description": story.get("description"),
                "verses": story.get("verses", []),
                "characters": story.get("characters", []),
                "themes": story.get("themes", []),
                "kids_title": story.get("kids_title"),
                "kids_description": story.get("kids_description"),
                "has_kids_version": bool(story.get("kids_narrative"))
            })
        categories_list.append({
            "category": category.get("category"),
            "slug": category.get("slug"),
            "description": category.get("description"),
            "story_count": len(stories_list),
            "stories": stories_list
        })

    return {
        "total_stories": story_count,
        "total_categories": category_count,
        "categories": categories_list
    }


@router.get("/stories/{slug}")
def api_get_story(slug: str = Path(..., description="Story slug", example="creation-of-the-world")):
    """Get a specific Bible story by slug."""
    story = get_story_by_slug(slug)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return {
        "title": story.get("title"),
        "slug": story.get("slug"),
        "description": story.get("description"),
        "category": story.get("category_name"),
        "category_slug": story.get("category_slug"),
        "verses": story.get("verses", []),
        "characters": story.get("characters", []),
        "themes": story.get("themes", []),
        "narrative": story.get("narrative"),
        "kids_title": story.get("kids_title"),
        "kids_description": story.get("kids_description"),
        "kids_narrative": story.get("kids_narrative"),
        "has_kids_version": bool(story.get("kids_narrative")),
        "links": {
            "web": f"/stories/{slug}",
            "kids_web": f"/stories/{slug}/kids" if story.get("kids_narrative") else None,
            "pdf": f"/api/stories/{slug}/pdf",
            "kids_pdf": f"/api/stories/{slug}/kids/pdf" if story.get("kids_narrative") else None
        }
    }


@router.get("/stories/{slug}/pdf")
async def api_story_pdf(slug: str = Path(..., description="Story slug")):
    """Generate PDF for a story (adult version)."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Render the PDF template
    html_content = templates.get_template("story_pdf.html").render(story=story)

    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Return as downloadable PDF
    filename = f"{slug}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/stories/{slug}/kids/pdf")
async def api_story_kids_pdf(slug: str = Path(..., description="Story slug")):
    """Generate PDF for a story (kids version)."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not story.get("kids_narrative"):
        raise HTTPException(status_code=404, detail="Kids version not available for this story")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Render the PDF template
    html_content = templates.get_template("story_kids_pdf.html").render(story=story)

    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Return as downloadable PDF
    filename = f"{slug}-kids.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ============================================================================
# RESOURCES ENDPOINTS
# ============================================================================

@router.get(
    "/resources",
    response_model=ResourcesListResponse,
    summary="List all resource categories",
    description="Get a list of all biblical resource categories (locations, angels, prophets, etc.)"
)
def api_list_resource_categories():
    """List all available resource categories."""
    def format_title(key: str) -> str:
        """Convert snake_case to Title Case."""
        return key.replace('_', ' ').title()
    
    def count_items(category_data: dict) -> int:
        """Count total items in a category (including nested subcategories)."""
        count = 0
        for value in category_data.values():
            if isinstance(value, dict):
                # Check if this is an item or a subcategory
                if 'description' in value or 'verses' in value:
                    count += 1
                else:
                    # It's a subcategory, recurse
                    count += count_items(value)
        return count
    
    categories = []
    for cat_name, cat_data in RESOURCES_DATA.items():
        # Create HTML URL by converting snake_case to kebab-case
        html_url = f"/{cat_name.replace('_', '-')}"
        categories.append({
            "name": cat_name,
            "title": format_title(cat_name),
            "item_count": count_items(cat_data),
            "url": f"/api/resources/{cat_name}",
            "html_url": html_url
        })
    
    return {
        "total_categories": len(categories),
        "categories": categories
    }


@router.get(
    "/resources/{category}",
    response_model=ResourceCategoryResponse,
    summary="Get all items in a resource category",
    description="Retrieve all items within a specific resource category",
    responses={
        200: {
            "description": "Successfully retrieved category",
            "content": {
                "application/json": {
                    "example": {
                        "category": "biblical_locations",
                        "title": "Biblical Locations",
                        "total_items": 15,
                        "items": [
                            {
                                "name": "Garden of Eden",
                                "slug": "garden-of-eden",
                                "description": "The original home of mankind",
                                "verse_count": 2,
                                "url": "/api/resources/biblical_locations/garden-of-eden"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def api_get_resource_category(
    category: str = Path(..., description="Resource category name", example="biblical_locations")
):
    """Get all items in a specific resource category."""
    if category not in RESOURCES_DATA:
        raise HTTPException(status_code=404, detail=f"Resource category '{category}' not found")
    
    cat_data = RESOURCES_DATA[category]
    
    def format_title(key: str) -> str:
        return key.replace('_', ' ').title()
    
    def flatten_items(data: dict, parent_key: str = "") -> list:
        """Flatten nested resource structure into a list of items."""
        items = []
        for key, value in data.items():
            if isinstance(value, dict):
                if 'description' in value or 'verses' in value:
                    # This is an item
                    slug = _create_slug(key)
                    verse_count = len(value.get('verses', []))
                    items.append({
                        "name": key,
                        "slug": slug,
                        "description": value.get('description', ''),
                        "verse_count": verse_count,
                        "url": f"/api/resources/{category}/{slug}"
                    })
                else:
                    # This is a subcategory, recurse
                    items.extend(flatten_items(value, key))
        return items
    
    items = flatten_items(cat_data)
    
    return {
        "category": category,
        "title": format_title(category),
        "total_items": len(items),
        "items": items
    }


@router.get(
    "/resources/{category}/{slug}",
    response_model=ResourceItemDetail,
    summary="Get a specific resource item",
    description="Retrieve detailed information about a specific resource item including all verses",
    responses={
        200: {
            "description": "Successfully retrieved resource item",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Garden of Eden",
                        "slug": "garden-of-eden",
                        "category": "biblical_locations",
                        "description": "The original home of mankind",
                        "verses": [
                            {
                                "reference": "Genesis 2:8",
                                "text": "And the LORD God planted a garden eastward in Eden; and there he put the man whom he had formed."
                            },
                            {
                                "reference": "Genesis 3:23",
                                "text": "Therefore the LORD God sent him forth from the garden of Eden, to till the ground from whence he was taken."
                            }
                        ]
                    }
                }
            }
        }
    }
)
def api_get_resource_item(
    category: str = Path(..., description="Resource category name", example="biblical_locations"),
    slug: str = Path(..., description="Resource item slug", example="garden-of-eden")
):
    """Get detailed information about a specific resource item."""
    if category not in CATEGORY_TO_DATA:
        raise HTTPException(status_code=404, detail=f"Resource category '{category}' not found")

    cat_data = CATEGORY_TO_DATA[category]

    # Search for the item by slug in potentially nested structure
    def find_by_slug(data: dict, target_slug: str):
        """Recursively search for an item by slug."""
        for key, value in data.items():
            if isinstance(value, dict):
                # Check if this is an item (has description or verses)
                if 'description' in value or 'verses' in value:
                    if _create_slug(key) == target_slug:
                        return value, key
                else:
                    # It's a subcategory, recurse
                    result = find_by_slug(value, target_slug)
                    if result:
                        return result
        return None

    result = find_by_slug(cat_data, slug)

    if not result:
        raise HTTPException(status_code=404, detail=f"Resource item '{slug}' not found in category '{category}'")

    item_data, item_name = result

    return {
        "name": item_name,
        "slug": slug,
        "category": category,
        "description": item_data.get('description', ''),
        "verses": item_data.get('verses', [])
    }

@router.get("/resources/{category}/pdf")
async def api_get_resource_category_pdf(
    category: str = Path(..., description="Resource category name", example="biblical_locations")
):
    """Generate PDF for an entire resource category."""
    # Check if category exists first (before checking WeasyPrint)
    if category not in CATEGORY_TO_DATA:
        raise HTTPException(status_code=404, detail=f"Resource category '{category}' not found")

    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )
    
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")
    
    cat_data = CATEGORY_TO_DATA[category]
    
    def format_title(key: str) -> str:
        return key.replace('_', ' ').title()
    
    title = format_title(category)
    
    # Render the PDF template
    html_content = templates.get_template("resource_index_pdf.html").render(
        resource_data=cat_data,
        page_title=title,
        page_subtitle=f"Biblical study resource",
        page_description=f"Explore {title.lower()} from the King James Bible"
    )
    
    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)
    
    # Return as downloadable PDF
    filename = f"{category}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/resources/{category}/{slug}/pdf")
async def api_get_resource_item_pdf(
    category: str = Path(..., description="Resource category name", example="biblical_locations"),
    slug: str = Path(..., description="Resource item slug", example="garden-of-eden")
):
    """Generate PDF for a specific resource item."""
    # Check if category exists first (before checking WeasyPrint)
    if category not in CATEGORY_TO_DATA:
        raise HTTPException(status_code=404, detail=f"Resource category '{category}' not found")
    
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")
    
    cat_data = CATEGORY_TO_DATA[category]
    
    # Find the item
    def find_by_slug(data: dict, target_slug: str):
        for key, value in data.items():
            if isinstance(value, dict):
                if 'description' in value or 'verses' in value:
                    if _create_slug(key) == target_slug:
                        return value, key
                else:
                    result = find_by_slug(value, target_slug)
                    if result:
                        return result
        return None
    
    result = find_by_slug(cat_data, slug)

    if not result:
        raise HTTPException(status_code=404, detail=f"Resource item '{slug}' not found")

    # Now check WeasyPrint availability
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    item_data, item_name = result

    def format_title(key: str) -> str:
        return key.replace('_', ' ').title()

    # Render the PDF template
    html_content = templates.get_template("resource_detail_pdf.html").render(
        item=item_data,
        item_name=item_name,
        category_name="",  # Not used in simple template
        resource_title=format_title(category)
    )
    
    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Return as downloadable PDF
    filename = f"{slug}-{category}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get(
    "/red-letter",
    response_model=RedLetterListResponse,
    summary="List all red letter verses",
    description="Get a list of all verses containing the words of Jesus Christ (red letter edition). Supports filtering by book and pagination."
)
def api_list_red_letter_verses(
    book: Optional[str] = Query(None, description="Filter by book name", example="John"),
    limit: int = Query(50, description="Maximum number of verses to return", example=50, ge=1, le=500),
    offset: int = Query(0, description="Number of verses to skip", example=0, ge=0)
):
    """List all red letter verses with optional filtering and pagination."""
    red_letter_data = load_red_letter_verses()

    # Parse all verses and build result list
    all_verses = []
    for verse_ref, christ_words in red_letter_data.items():
        # Parse the reference (format: "Book Chapter:Verse")
        parts = verse_ref.rsplit(' ', 1)
        if len(parts) != 2:
            continue

        book_name = parts[0]
        chapter_verse = parts[1].split(':')
        if len(chapter_verse) != 2:
            continue

        try:
            chapter_num = int(chapter_verse[0])
            verse_num = int(chapter_verse[1])
        except ValueError:
            continue

        # Apply book filter if specified
        if book and book_name != book:
            # Try normalizing the book name in case it's an abbreviation
            canonical = normalize_book_name(book)
            if not canonical or book_name != canonical:
                continue

        # Get the verse text
        verse_text = bible.get_verse_text(book_name, chapter_num, verse_num)
        if not verse_text:
            continue

        all_verses.append({
            "reference": verse_ref,
            "book": book_name,
            "chapter": chapter_num,
            "verse": verse_num,
            "text": verse_text,
            "christ_words": christ_words,
            "is_full_verse": christ_words == "full"
        })

    # Apply pagination
    total = len(all_verses)
    paginated_verses = all_verses[offset:offset + limit]

    return {
        "total": total,
        "verses": paginated_verses,
        "limit": limit,
        "offset": offset
    }


@router.get(
    "/red-letter/stats",
    response_model=RedLetterStatsResponse,
    summary="Get red letter statistics",
    description="Get statistics about verses containing the words of Jesus Christ, including counts by book and full vs. partial verses."
)
def api_red_letter_stats():
    """Get statistics about red letter verses in the Bible."""
    red_letter_data = load_red_letter_verses()

    total_verses = len(red_letter_data)
    full_verses = sum(1 for v in red_letter_data.values() if v == "full")
    partial_verses = total_verses - full_verses

    # Count by book
    by_book = {}
    books_set = set()

    for verse_ref in red_letter_data.keys():
        # Parse the reference (format: "Book Chapter:Verse")
        parts = verse_ref.rsplit(' ', 1)
        if len(parts) != 2:
            continue

        book_name = parts[0]
        books_set.add(book_name)
        by_book[book_name] = by_book.get(book_name, 0) + 1

    # Sort books by count (descending)
    by_book = dict(sorted(by_book.items(), key=lambda x: x[1], reverse=True))

    return {
        "total_verses": total_verses,
        "full_verses": full_verses,
        "partial_verses": partial_verses,
        "books_with_red_letter": sorted(list(books_set)),
        "by_book": by_book
    }
