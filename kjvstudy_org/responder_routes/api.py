"""API routes for KJV Study - JSON endpoints for programmatic access.

Responder port of routes/api.py. Every handler mutates ``resp`` (JSON via
``resp.media``, PDFs via ``pdf_resp``) instead of returning a response.
"""
from typing import Optional, List
from pydantic import BaseModel, Field
import json
import random
import re
from pathlib import Path as FilePath
from functools import lru_cache

from ..kjv import bible
from ..cross_references import get_cross_references
from ..reading_plans import get_plan, get_plan_summary
from ..topics import get_all_topics, get_topic_with_text
from ..interlinear_loader import get_interlinear_data, has_interlinear_data
from ..utils.books import normalize_book_name, OT_BOOKS, NT_BOOKS
from ..utils.search import perform_full_text_search
from ..utils.helpers import get_daily_verse, create_slug, CHAPTER_EXPLANATIONS
from ..utils.stats import compute_site_stats
from ..resource_catalog import iter_resources, RESOURCE_SEARCH_KEYWORDS
from ..utils.commentary_loader import load_commentary
from ..books import get_book_data, get_all_books_metadata, has_book_data
from ..red_letter import get_christ_words, iter_red_letter_verses, red_letter_stats
from ..strongs import (
    get_strongs_entry, format_strongs_entry, search_strongs,
    get_strongs_definition, get_strongs_word
)
from ..stories import (
    get_categories,
    get_story_by_slug,
    get_story_count,
    get_category_count,
    get_all_stories_flat,
)
from ..data import (
    _data as RESOURCES_DATA,
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

from ._helpers import pdf_resp


@lru_cache(maxsize=1)
def _load_verse_commentary():
    """Load verse commentary from split per-book files. Cached since data never changes."""
    return load_commentary()


@lru_cache(maxsize=1)
def _load_biographies():
    """Load biographies from JSON file. Cached since data never changes."""
    biographies_path = FilePath(__file__).parent.parent / "data" / "biographies.json"
    if not biographies_path.exists():
        return {"biographies": {}, "aliases": {}}

    with open(biographies_path, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_close_family_marriages():
    """Load known close family marriages from JSON file. Cached since data never changes."""
    marriages_path = FilePath(__file__).parent.parent / "data" / "close_family_marriages.json"
    if not marriages_path.exists():
        return {"marriages": []}

    with open(marriages_path, "r", encoding="utf-8") as f:
        return json.load(f)


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


class CommentaryResponse(BaseModel):
    """Verse commentary response"""
    book: str = Field(..., json_schema_extra={"example": "John"})
    chapter: int = Field(..., json_schema_extra={"example": 3})
    verse: int = Field(..., json_schema_extra={"example": 16})
    reference: str = Field(..., json_schema_extra={"example": "John 3:16"})
    text: str = Field(..., json_schema_extra={"example": "For God so loved the world..."})
    analysis: str = Field(..., json_schema_extra={"example": "<strong>For I am the LORD...</strong>"})
    historical: str = Field(..., json_schema_extra={"example": "Historical context..."})
    questions: List[str] = Field(..., json_schema_extra={"example": ["How does this verse...", "What does..."]})


class ChapterCommentaryResponse(BaseModel):
    """Chapter commentary response"""
    book: str = Field(..., json_schema_extra={"example": "Genesis"})
    chapter: int = Field(..., json_schema_extra={"example": 1})
    explanation: str = Field(..., json_schema_extra={"example": "The creation account..."})


class BulkVerseRequest(BaseModel):
    """Request body for bulk verse lookup"""
    references: List[str] = Field(..., json_schema_extra={"example": ["John 3:16", "Romans 8:28", "Psalm 23:1"]})


class BulkVerseResponse(BaseModel):
    """Response for bulk verse lookup"""
    total: int = Field(..., json_schema_extra={"example": 3})
    verses: List[VerseResponse]


class KeyEvent(BaseModel):
    """A key event in a person's life"""
    age: int = Field(..., json_schema_extra={"example": 100})
    event: str = Field(..., json_schema_extra={"example": "Birth of Isaac"})
    verse: str = Field(..., json_schema_extra={"example": "Genesis 21:5"})


class BiographyResponse(BaseModel):
    """Biography of a biblical figure"""
    name: str = Field(..., json_schema_extra={"example": "Abraham"})
    summary: str = Field(..., json_schema_extra={"example": "Originally named Abram..."})
    significance: str = Field(..., json_schema_extra={"example": "Abraham is the father of the Hebrew nation..."})
    key_events: List[KeyEvent]


class FamilyTreeListResponse(BaseModel):
    """List of all people in family tree"""
    total: int = Field(..., json_schema_extra={"example": 42})
    people: List[str] = Field(..., json_schema_extra={"example": ["Adam", "Noah", "Abraham"]})


class PersonStat(BaseModel):
    """Statistical information about a person"""
    name: str = Field(..., json_schema_extra={"example": "Methuselah"})
    person_id: str = Field(..., json_schema_extra={"example": "i12"})
    value: int = Field(..., json_schema_extra={"example": 969})
    additional_info: Optional[str] = Field(None, json_schema_extra={"example": "Lived 969 years"})


class FamilyTreeStatsResponse(BaseModel):
    """Statistics about the biblical family tree from GEDCOM data"""
    total_people: int = Field(..., json_schema_extra={"example": 429})
    total_generations: int = Field(..., json_schema_extra={"example": 77})
    longest_lived: PersonStat
    most_children: PersonStat
    most_siblings: PersonStat
    average_lifespan: Optional[float] = Field(None, json_schema_extra={"example": 256.5})
    total_with_known_ages: int = Field(..., json_schema_extra={"example": 156})
    close_family_marriages: int = Field(..., json_schema_extra={"example": 3}, description="Marriages between close relatives (common in early biblical times)")


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


def register(api):
    @api.route("/api/")
    async def api_index(req, resp):
        """API index with links to documentation and available endpoints."""
        resp.media = {
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
                "red_letter_stats": "/api/red-letter/stats",
                "random_verse": "/api/verse/random?testament={testament}&book={book}",
                "commentary": "/api/commentary/{book}/{chapter}/{verse}",
                "chapter_commentary": "/api/chapter-commentary/{book}/{chapter}",
                "bulk_verses": "/api/verses/bulk",
                "family_tree": "/api/family-tree",
                "family_tree_stats": "/api/family-tree/stats",
                "biography": "/api/family-tree/{name}"
            }
        }

    @api.route("/api/health")
    async def api_health_check(req, resp):
        """API health check endpoint for monitoring and status verification."""
        resp.media = {
            "status": "healthy",
            "service": "KJV Study API",
            "version": "1.0.0"
        }

    @api.route("/api/search")
    async def search_api(req, resp):
        """JSON API endpoint for search."""
        q = req.params.get("q")
        limit_raw = req.params.get("limit")
        limit = int(limit_raw) if limit_raw is not None else None

        if not q or len(q.strip()) < 2:
            resp.media = {"query": q, "results": [], "total": 0}
            return

        results = perform_full_text_search(q.strip(), limit)
        is_direct_verse = False

        # Check if this was a direct verse reference match
        if results and len(results) == 1 and results[0].get("score") == 100.0:
            is_direct_verse = True

        resp.media = {
            "query": q,
            "results": results,
            "total": len(results),
            "is_direct_verse": is_direct_verse
        }

    @api.route("/api/universal-search")
    async def universal_search_api(req, resp):
        """Universal search across all content types."""
        q = req.params.get("q")
        limit = int(req.params.get("limit", 5))

        if not q or len(q.strip()) < 2:
            resp.media = {"query": q, "results": {}}
            return

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
        # Theological resources -- derived from the shared catalog so search always
        # covers every resource (incl. systematic-theology pages) with no drift.
        resources_to_search = [
            (f"{RESOURCE_SEARCH_KEYWORDS.get(r['url'], '')} {r['name']}", r["url"], r["name"])
            for r in iter_resources()
        ]
        resources_to_search += [
            # Search-only study tools (not part of the resource catalog)
            ("interlinear hebrew greek original language", "/interlinear", "Interlinear Bible"),
            ("concordance word search find", "/concordance", "Concordance"),
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
            # Biblical figures (link to family tree search, which resolves the person)
            ("adam eve first man woman creation", "/family-tree/search?q=Adam", "Adam"),
            ("noah ark flood", "/family-tree/search?q=Noah", "Noah"),
            ("abraham abram father faith", "/family-tree/search?q=Abraham", "Abraham"),
            ("isaac son promise", "/family-tree/search?q=Isaac", "Isaac"),
            ("jacob israel twelve tribes", "/family-tree/search?q=Jacob", "Jacob"),
            ("joseph dreamer coat egypt", "/family-tree/search?q=Joseph", "Joseph"),
            ("moses exodus law lawgiver", "/family-tree/search?q=Moses", "Moses"),
            ("david king shepherd psalmist", "/family-tree/search?q=David", "David"),
            ("solomon wisdom temple", "/family-tree/search?q=Solomon", "Solomon"),
            ("paul apostle gentiles saul tarsus", "/family-tree/search?q=Paul", "Paul the Apostle"),
        ]
        matching_resources = [
            {"name": name, "url": url}
            for key, url, name in resources_to_search
            if query in key.lower() or query in name.lower()
        ][:limit]
        if matching_resources:
            results["resources"] = matching_resources

        resp.media = {"query": q, "results": results}

    @api.route("/api/verse-of-the-day")
    async def verse_of_the_day_api(req, resp):
        """API endpoint for verse of the day."""
        resp.media = get_daily_verse()

    @api.route("/api/verse/{book}/{chapter:int}/{verse:int}")
    async def api_get_verse(req, resp, *, book, chapter, verse):
        """Get a single verse with red letter information and optional interlinear data."""
        interlinear = str(req.params.get("interlinear", "")).lower() in ("1", "true", "yes", "on")

        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        # Check if book exists
        all_books = bible.get_books()
        if book not in all_books:
            resp.status_code = 404
            resp.media = {"detail": f"Book '{book}' not found"}
            return

        # Check valid chapter/verse numbers
        if chapter < 1 or verse < 1:
            resp.status_code = 404
            resp.media = {"detail": "Invalid chapter or verse number"}
            return

        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            resp.status_code = 404
            resp.media = {"detail": "Verse not found"}
            return

        # Get red letter information (words of Christ)
        christ_words = get_christ_words(book, chapter, verse)

        result = {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text,
            "red_letter": christ_words
        }

        # Optionally include interlinear data
        if interlinear:
            interlinear_words = get_interlinear_data(book, chapter, verse)
            result["interlinear"] = {
                "available": bool(interlinear_words),
                "words": interlinear_words or []
            }

        resp.media = result

    @api.route("/api/verse-range/{book}/{chapter:int}/{start:int}/{end:int}")
    async def api_get_verse_range(req, resp, *, book, chapter, start, end):
        """Get a range of verses with red letter information."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        # Check if book exists
        all_books = bible.get_books()
        if book not in all_books:
            resp.status_code = 404
            resp.media = {"detail": f"Book '{book}' not found"}
            return

        # Check valid verse numbers
        if chapter < 1 or start < 1 or end < 1:
            resp.status_code = 404
            resp.media = {"detail": "Invalid chapter or verse number"}
            return

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
            resp.status_code = 404
            resp.media = {"detail": "Verse range not found"}
            return

        resp.media = {
            "book": book,
            "chapter": chapter,
            "start": start,
            "end": end,
            "reference": f"{book} {chapter}:{start}-{end}",
            "verses": verses,
            "text": " ".join(verse_texts)
        }

    @api.route("/api/interlinear/{book}/{chapter:int}/{verse:int}")
    async def api_get_interlinear(req, resp, *, book, chapter, verse):
        """Get interlinear (word-by-word) data for a verse."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        # Check if book exists
        all_books = bible.get_books()
        if book not in all_books:
            resp.status_code = 404
            resp.media = {"detail": f"Book '{book}' not found"}
            return

        # Check valid chapter/verse numbers
        if chapter < 1 or verse < 1:
            resp.status_code = 404
            resp.media = {"detail": "Invalid chapter or verse number"}
            return

        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            resp.status_code = 404
            resp.media = {"detail": "Verse not found"}
            return

        if not has_interlinear_data(book, chapter, verse):
            resp.media = {
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "reference": f"{book} {chapter}:{verse}",
                "text": verse_text,
                "interlinear_available": False,
                "words": []
            }
            return

        interlinear_words = get_interlinear_data(book, chapter, verse)

        resp.media = {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text,
            "interlinear_available": True,
            "words": interlinear_words
        }

    @api.route("/api/books")
    async def api_get_books(req, resp):
        """Get list of all Bible books with metadata."""
        books = bible.get_books()

        old_testament = []
        new_testament = []

        for book in books:
            chapters = bible.get_chapters_for_book(book)
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

        resp.media = {
            "total_books": len(books),
            "old_testament": old_testament,
            "new_testament": new_testament
        }

    @api.route("/api/books/{book}")
    async def api_get_book(req, resp, *, book):
        """Get details about a specific book including introduction and study material."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        chapters = bible.get_chapters_for_book(book)
        if not chapters:
            resp.status_code = 404
            resp.media = {"detail": "Book not found"}
            return

        chapter_details = []
        for chapter in chapters:
            verses = bible.get_verses_by_book_chapter(book, chapter)
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

        resp.media = result

    @api.route("/api/books/{book}/pdf")
    async def api_book_pdf(req, resp, *, book):
        """Generate PDF for an entire Bible book."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        chapters = bible.get_chapters_for_book(book)
        if not chapters:
            resp.status_code = 404
            resp.media = {"detail": "Book not found"}
            return

        # Prepare data for template
        chapters_data = []
        total_verses = 0
        for chapter in chapters:
            verses = bible.get_verses_by_book_chapter(book, chapter)
            if verses:
                chapter_verses = [{"verse": v.verse, "text": v.text} for v in verses]
                chapters_data.append({
                    "chapter": chapter,
                    "verses": chapter_verses
                })
                total_verses += len(verses)

        if not chapters_data:
            resp.status_code = 404
            resp.media = {"detail": "No verses found for this book"}
            return

        # Render the PDF template
        html_content = api.template(
            "book_pdf.html",
            book=book,
            chapters=chapters_data,
            chapter_count=len(chapters_data),
            verse_count=total_verses,
        )

        # Return as downloadable PDF
        filename = f"{create_slug(book)}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/api/books/{book}/chapters/{chapter:int}")
    async def api_get_chapter(req, resp, *, book, chapter):
        """Get all verses in a chapter."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verses = bible.get_verses_by_book_chapter(book, chapter)
        if not verses:
            resp.status_code = 404
            resp.media = {"detail": "Chapter not found"}
            return

        verse_list = [{"verse": v.verse, "text": v.text} for v in verses]

        resp.media = {
            "book": book,
            "chapter": chapter,
            "total_verses": len(verses),
            "verses": verse_list,
            "links": {
                "pdf": f"/api/books/{book}/chapters/{chapter}/pdf"
            }
        }

    @api.route("/api/books/{book}/chapters/{chapter:int}/pdf")
    async def api_chapter_pdf(req, resp, *, book, chapter):
        """Generate PDF for a specific Bible chapter."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verses = bible.get_verses_by_book_chapter(book, chapter)
        if not verses:
            resp.status_code = 404
            resp.media = {"detail": "Chapter not found"}
            return

        # Prepare data for template
        verse_list = [{"verse": v.verse, "text": v.text} for v in verses]

        # Render the PDF template
        html_content = api.template(
            "chapter_pdf.html",
            book=book,
            chapter=chapter,
            verses=verse_list,
            verse_count=len(verses),
        )

        # Return as downloadable PDF
        filename = f"{create_slug(book)}-chapter-{chapter}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/api/books/{book}/text")
    async def api_get_book_text(req, resp, *, book):
        """Get all text content of a book."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        book_chapters = bible.get_chapters_for_book(book)
        if not book_chapters:
            resp.status_code = 404
            resp.media = {"detail": "Book not found"}
            return

        chapter_list = []
        total_verses = 0
        for ch in book_chapters:
            verses = bible.get_verses_by_book_chapter(book, ch)
            chapter_list.append({
                "chapter": ch,
                "verses": [{"verse": v.verse, "text": v.text} for v in verses]
            })
            total_verses += len(verses)

        resp.media = {
            "book": book,
            "total_chapters": len(book_chapters),
            "total_verses": total_verses,
            "chapters": chapter_list
        }

    @api.route("/api/bible")
    async def api_get_bible(req, resp):
        """Get the entire Bible text."""
        books_list = []
        total_verses = 0
        for book_name in bible.get_books():
            chapter_list = []
            for ch in bible.get_chapters_for_book(book_name):
                verses = bible.get_verses_by_book_chapter(book_name, ch)
                chapter_list.append({
                    "chapter": ch,
                    "verses": [{"verse": v.verse, "text": v.text} for v in verses]
                })
                total_verses += len(verses)
            books_list.append({
                "book": book_name,
                "chapters": chapter_list
            })

        resp.media = {
            "total_books": len(books_list),
            "total_verses": total_verses,
            "books": books_list
        }

    @api.route("/api/cross-references/{book}/{chapter:int}/{verse:int}")
    async def api_get_cross_references(req, resp, *, book, chapter, verse):
        """Get cross-references for a verse."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            resp.status_code = 404
            resp.media = {"detail": "Verse not found"}
            return

        cross_refs = get_cross_references(book, chapter, verse)

        resp.media = {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "cross_references": cross_refs
        }

    @api.route("/api/topics")
    async def api_get_topics(req, resp):
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

        resp.media = {
            "total_topics": len(topics),
            "topics": topic_list
        }

    @api.route("/api/topics/{topic_name}")
    async def api_get_topic(req, resp, *, topic_name):
        """Get details about a specific topic."""
        topic = get_topic_with_text(topic_name)
        if not topic:
            resp.status_code = 404
            resp.media = {"detail": "Topic not found"}
            return

        resp.media = {
            "name": topic_name,
            "description": topic.get("description", ""),
            "overview": topic.get("overview", ""),
            "subtopics": topic.get("subtopics", {})
        }

    @api.route("/api/reading-plans")
    async def api_get_reading_plans(req, resp):
        """Get list of all reading plans."""
        plans = get_plan_summary()

        resp.media = {
            "total_plans": len(plans),
            "plans": plans
        }

    @api.route("/api/reading-plans/{plan_id}")
    async def api_get_reading_plan(req, resp, *, plan_id):
        """Get details about a specific reading plan."""
        plan = get_plan(plan_id)
        if not plan:
            resp.status_code = 404
            resp.media = {"detail": "Reading plan not found"}
            return

        resp.media = plan

    @api.route("/api/reading-plans/{plan_id}/day/{day_num:int}")
    async def api_get_reading_plan_day_text(req, resp, *, plan_id, day_num):
        """Get the Scripture text for a specific day in a reading plan."""
        plan = get_plan(plan_id)
        if not plan:
            resp.status_code = 404
            resp.media = {"detail": "Reading plan not found"}
            return

        all_days = plan.get('days') or plan.get('sample_days', [])

        # Find the specific day
        day_data = None
        for day in all_days:
            if day['day'] == day_num:
                day_data = day
                break

        if not day_data:
            resp.status_code = 404
            resp.media = {"detail": f"Day {day_num} not found in plan"}
            return

        # Import the get_reading_text function from reading_plans routes
        from .reading_plans import get_reading_text

        # Get the text for this day's readings
        text_sections = get_reading_text(day_data['readings'])

        # Convert Verse objects to dicts for JSON serialization
        result = []
        for section in text_sections:
            result.append({
                'book': section['book'],
                'chapter': section['chapter'],
                'reference': section['reference'],
                'verses': [{'verse': v.verse, 'text': v.text} for v in section['verses']]
            })

        resp.media = {
            'day': day_num,
            'theme': day_data.get('theme', ''),
            'readings': day_data['readings'],
            'text': result
        }

    @api.route("/api/stories")
    async def api_get_stories(req, resp):
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

        resp.media = {
            "total_stories": story_count,
            "total_categories": category_count,
            "categories": categories_list
        }

    @api.route("/api/stories/{slug}")
    async def api_get_story(req, resp, *, slug):
        """Get a specific Bible story by slug."""
        story = get_story_by_slug(slug)
        if not story:
            resp.status_code = 404
            resp.media = {"detail": "Story not found"}
            return

        resp.media = {
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

    @api.route("/api/stories/{slug}/pdf")
    async def api_story_pdf(req, resp, *, slug):
        """Generate PDF for a story (adult version)."""
        story = get_story_by_slug(slug)

        if not story:
            resp.status_code = 404
            resp.media = {"detail": "Story not found"}
            return

        # Render the PDF template
        html_content = api.template("story_pdf.html", story=story)

        # Return as downloadable PDF
        filename = f"{slug}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/api/stories/{slug}/kids/pdf")
    async def api_story_kids_pdf(req, resp, *, slug):
        """Generate PDF for a story (kids version)."""
        story = get_story_by_slug(slug)

        if not story:
            resp.status_code = 404
            resp.media = {"detail": "Story not found"}
            return

        if not story.get("kids_narrative"):
            resp.status_code = 404
            resp.media = {"detail": "Kids version not available for this story"}
            return

        # Render the PDF template
        html_content = api.template("story_kids_pdf.html", story=story)

        # Return as downloadable PDF
        filename = f"{slug}-kids.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    # ========================================================================
    # RESOURCES ENDPOINTS
    # ========================================================================

    @api.route("/api/resources")
    async def api_list_resource_categories(req, resp):
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

        resp.media = {
            "total_categories": len(categories),
            "categories": categories
        }

    @api.route("/api/resources/{category}")
    async def api_get_resource_category(req, resp, *, category):
        """Get all items in a specific resource category."""
        if category not in RESOURCES_DATA:
            resp.status_code = 404
            resp.media = {"detail": f"Resource category '{category}' not found"}
            return

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
                        slug = create_slug(key)
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

        resp.media = {
            "category": category,
            "title": format_title(category),
            "total_items": len(items),
            "items": items
        }

    @api.route("/api/resources/{category}/{slug}")
    async def api_get_resource_item(req, resp, *, category, slug):
        """Get detailed information about a specific resource item."""
        if category not in CATEGORY_TO_DATA:
            resp.status_code = 404
            resp.media = {"detail": f"Resource category '{category}' not found"}
            return

        cat_data = CATEGORY_TO_DATA[category]

        # Search for the item by slug in potentially nested structure
        def find_by_slug(data: dict, target_slug: str):
            """Recursively search for an item by slug."""
            for key, value in data.items():
                if isinstance(value, dict):
                    # Check if this is an item (has description or verses)
                    if 'description' in value or 'verses' in value:
                        if create_slug(key) == target_slug:
                            return value, key
                    else:
                        # It's a subcategory, recurse
                        result = find_by_slug(value, target_slug)
                        if result:
                            return result
            return None

        result = find_by_slug(cat_data, slug)

        if not result:
            resp.status_code = 404
            resp.media = {"detail": f"Resource item '{slug}' not found in category '{category}'"}
            return

        item_data, item_name = result

        resp.media = {
            "name": item_name,
            "slug": slug,
            "category": category,
            "description": item_data.get('description', ''),
            "verses": item_data.get('verses', [])
        }

    @api.route("/api/resources/{category}/pdf")
    async def api_get_resource_category_pdf(req, resp, *, category):
        """Generate PDF for an entire resource category."""
        # Check if category exists first (before checking WeasyPrint)
        if category not in CATEGORY_TO_DATA:
            resp.status_code = 404
            resp.media = {"detail": f"Resource category '{category}' not found"}
            return

        cat_data = CATEGORY_TO_DATA[category]

        def format_title(key: str) -> str:
            return key.replace('_', ' ').title()

        title = format_title(category)

        # Render the PDF template
        html_content = api.template(
            "resource_index_pdf.html",
            resource_data=cat_data,
            page_title=title,
            page_subtitle=f"Biblical study resource",
            page_description=f"Explore {title.lower()} from the King James Bible"
        )

        # Return as downloadable PDF
        filename = f"{category}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/api/resources/{category}/{slug}/pdf")
    async def api_get_resource_item_pdf(req, resp, *, category, slug):
        """Generate PDF for a specific resource item."""
        # Check if category exists first (before checking WeasyPrint)
        if category not in CATEGORY_TO_DATA:
            resp.status_code = 404
            resp.media = {"detail": f"Resource category '{category}' not found"}
            return

        cat_data = CATEGORY_TO_DATA[category]

        # Find the item
        def find_by_slug(data: dict, target_slug: str):
            for key, value in data.items():
                if isinstance(value, dict):
                    if 'description' in value or 'verses' in value:
                        if create_slug(key) == target_slug:
                            return value, key
                    else:
                        result = find_by_slug(value, target_slug)
                        if result:
                            return result
            return None

        result = find_by_slug(cat_data, slug)

        if not result:
            resp.status_code = 404
            resp.media = {"detail": f"Resource item '{slug}' not found"}
            return

        item_data, item_name = result

        def format_title(key: str) -> str:
            return key.replace('_', ' ').title()

        # Render the PDF template
        html_content = api.template(
            "resource_detail_pdf.html",
            item=item_data,
            item_name=item_name,
            category_name="",  # Not used in simple template
            resource_title=format_title(category)
        )

        # Return as downloadable PDF
        filename = f"{slug}-{category}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/api/red-letter")
    async def api_list_red_letter_verses(req, resp):
        """List all red letter verses with optional filtering and pagination."""
        book = req.params.get("book")
        limit = int(req.params.get("limit", 50))
        offset = int(req.params.get("offset", 0))

        all_verses = list(iter_red_letter_verses(book))

        total = len(all_verses)
        paginated_verses = all_verses[offset:offset + limit]

        resp.media = {
            "total": total,
            "verses": paginated_verses,
            "limit": limit,
            "offset": offset
        }

    @api.route("/api/red-letter/stats")
    async def api_red_letter_stats(req, resp):
        """Get statistics about red letter verses in the Bible."""
        stats = red_letter_stats()

        resp.media = {
            "total_verses": stats["total"],
            "full_verses": stats["full"],
            "partial_verses": stats["partial"],
            "books_with_red_letter": sorted(stats["by_book"].keys()),
            "by_book": stats["by_book"]
        }

    @api.route("/api/verse/random")
    async def api_random_verse(req, resp):
        """Get a random Bible verse with optional filtering."""
        testament = req.params.get("testament")
        book = req.params.get("book")

        all_books = bible.get_books()

        # Apply testament filter
        if testament:
            testament = testament.lower()
            if testament == "ot":
                filtered_books = [b for b in all_books if b in OT_BOOKS]
            elif testament == "nt":
                filtered_books = [b for b in all_books if b not in OT_BOOKS]
            else:
                resp.status_code = 400
                resp.media = {"detail": "Testament must be 'ot' or 'nt'"}
                return
        else:
            filtered_books = all_books

        # Apply book filter
        if book:
            canonical_name = normalize_book_name(book)
            if canonical_name:
                book = canonical_name
            if book not in filtered_books:
                resp.status_code = 404
                resp.media = {"detail": f"Book '{book}' not found"}
                return
            filtered_books = [book]

        # Select random book
        selected_book = random.choice(filtered_books)

        # Get random chapter
        chapters = bible.get_chapters_for_book(selected_book)
        if not chapters:
            resp.status_code = 404
            resp.media = {"detail": "No chapters found"}
            return

        selected_chapter = random.choice(chapters)

        # Get random verse
        verses = bible.get_verses_by_book_chapter(selected_book, selected_chapter)
        if not verses:
            resp.status_code = 404
            resp.media = {"detail": "No verses found"}
            return

        selected_verse_num = random.choice([v.verse for v in verses])

        # Get the verse text
        verse_text = bible.get_verse_text(selected_book, selected_chapter, selected_verse_num)
        if not verse_text:
            resp.status_code = 404
            resp.media = {"detail": "Verse text not found"}
            return

        # Get red letter information
        christ_words = get_christ_words(selected_book, selected_chapter, selected_verse_num)

        resp.media = {
            "book": selected_book,
            "chapter": selected_chapter,
            "verse": selected_verse_num,
            "reference": f"{selected_book} {selected_chapter}:{selected_verse_num}",
            "text": verse_text,
            "red_letter": christ_words
        }

    @api.route("/api/commentary/{book}/{chapter:int}/{verse:int}")
    async def api_get_verse_commentary(req, resp, *, book, chapter, verse):
        """Get commentary for a specific verse."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        # Check if book exists
        all_books = bible.get_books()
        if book not in all_books:
            resp.status_code = 404
            resp.media = {"detail": f"Book '{book}' not found"}
            return

        # Get verse text
        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            resp.status_code = 404
            resp.media = {"detail": "Verse not found"}
            return

        # Load commentary data
        commentary_data = _load_verse_commentary()

        # Navigate to the commentary
        if book not in commentary_data:
            resp.status_code = 404
            resp.media = {"detail": "Commentary not available for this book"}
            return

        if chapter not in commentary_data[book]:
            resp.status_code = 404
            resp.media = {"detail": "Commentary not available for this chapter"}
            return

        if verse not in commentary_data[book][chapter]:
            resp.status_code = 404
            resp.media = {"detail": "Commentary not available for this verse"}
            return

        verse_commentary = commentary_data[book][chapter][verse]

        resp.media = {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text,
            "analysis": verse_commentary.get("analysis", ""),
            "historical": verse_commentary.get("historical", ""),
            "questions": verse_commentary.get("questions", [])
        }

    @api.route("/api/chapter-commentary/{book}/{chapter:int}")
    async def api_get_chapter_commentary(req, resp, *, book, chapter):
        """Get commentary/explanation for a specific chapter."""
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        # Check if book exists
        all_books = bible.get_books()
        if book not in all_books:
            resp.status_code = 404
            resp.media = {"detail": f"Book '{book}' not found"}
            return

        # Check if chapter exists
        chapters = bible.get_chapters_for_book(book)
        if chapter not in chapters:
            resp.status_code = 404
            resp.media = {"detail": f"Chapter {chapter} not found in {book}"}
            return

        # Get chapter explanation
        if book in CHAPTER_EXPLANATIONS and chapter in CHAPTER_EXPLANATIONS[book]:
            explanation = CHAPTER_EXPLANATIONS[book][chapter]
        else:
            # Provide generic explanation if specific one doesn't exist
            explanation = f"Chapter {chapter} of {book}"

        resp.media = {
            "book": book,
            "chapter": chapter,
            "explanation": explanation
        }

    @api.route("/api/verses/bulk", methods=["POST"])
    async def api_bulk_verse_lookup(req, resp):
        """Look up multiple verses in a single request."""
        from ..kjv import VerseReference

        try:
            body = await req.media()
        except Exception:
            body = {}
        references = body.get("references", []) if isinstance(body, dict) else []

        verses = []
        for ref_string in references:
            try:
                # Parse the reference
                verse_ref = VerseReference.from_string(ref_string.strip())

                # Normalize book name
                book = verse_ref.book
                canonical_name = normalize_book_name(book)
                if canonical_name:
                    book = canonical_name

                # Get verse text
                verse_text = bible.get_verse_text(book, verse_ref.chapter, verse_ref.verse)

                if verse_text:
                    # Get red letter information
                    christ_words = get_christ_words(book, verse_ref.chapter, verse_ref.verse)

                    verses.append({
                        "book": book,
                        "chapter": verse_ref.chapter,
                        "verse": verse_ref.verse,
                        "reference": f"{book} {verse_ref.chapter}:{verse_ref.verse}",
                        "text": verse_text,
                        "red_letter": christ_words
                    })
            except Exception:
                # Skip invalid references
                continue

        resp.media = {
            "total": len(verses),
            "verses": verses
        }

    @api.route("/api/family-tree/stats")
    async def api_family_tree_stats(req, resp):
        """Get statistics about the biblical family tree from GEDCOM data."""
        from ..utils.family_tree import get_family_tree_data
        import re

        try:
            family_tree_data, generations = get_family_tree_data()

            if not family_tree_data:
                raise RuntimeError("Family tree data not available")

            # Load biographies for supplemental age data
            biographies_data = _load_biographies()
            biographies = biographies_data.get("biographies", {})
            aliases = biographies_data.get("aliases", {})

            # Load known close family marriages
            known_marriages_data = _load_close_family_marriages()
            known_marriages = known_marriages_data.get("marriages", [])

            # Calculate statistics
            total_people = len(family_tree_data)
            total_generations = len(generations) if generations else 0

            # Find longest lived person
            longest_lived_person = None
            longest_lived_person_id = None
            longest_lifespan = 0

            # Find person with most children
            most_children_person = None
            most_children_person_id = None
            most_children_count = 0

            # Find person with most siblings
            most_siblings_person = None
            most_siblings_person_id = None
            most_siblings_count = 0

            # Track close family marriages
            close_family_marriages_count = 0

            # Calculate average lifespan
            total_age = 0
            people_with_ages = 0

            for person_id, person in family_tree_data.items():
                # Check lifespan - try multiple formats
                age = None

                # Try age_at_death field first
                if person.get("age_at_death") and person["age_at_death"] != "Unknown":
                    try:
                        # Parse age (format: "123 years")
                        age_str = person["age_at_death"].replace(" years", "").strip()
                        age = int(age_str)
                    except (ValueError, AttributeError):
                        pass

                # Also try death_year field which might contain "Lived XXX years"
                if age is None and person.get("death_year") and person["death_year"] != "Unknown":
                    try:
                        death_text = person["death_year"]
                        if "Lived" in death_text and "years" in death_text:
                            # Format: "Lived 930 years"
                            match = re.search(r'Lived (\d+) years', death_text)
                            if match:
                                age = int(match.group(1))
                    except (ValueError, AttributeError):
                        pass

                # Finally, check biographies.json for age data
                if age is None:
                    person_name = person.get("name")
                    # Check if name is an alias
                    lookup_name = aliases.get(person_name, person_name)

                    if lookup_name in biographies:
                        try:
                            biography = biographies[lookup_name]
                            key_events = biography.get("key_events", [])
                            # Find death event (usually the last event with highest age)
                            death_age = 0
                            for event in key_events:
                                event_age = event.get("age")
                                if event_age is not None and event_age > death_age:
                                    death_age = event_age
                            if death_age > 0:
                                age = death_age
                        except (ValueError, AttributeError, KeyError):
                            pass

                # Record age statistics if we found an age
                if age is not None:
                    total_age += age
                    people_with_ages += 1

                    if age > longest_lifespan:
                        longest_lifespan = age
                        longest_lived_person = person
                        longest_lived_person_id = person_id

                # Check children count
                children_count = len(person.get("children", []))
                if children_count > most_children_count:
                    most_children_count = children_count
                    most_children_person = person
                    most_children_person_id = person_id

                # Check siblings count
                siblings_count = len(person.get("siblings", []))
                if siblings_count > most_siblings_count:
                    most_siblings_count = siblings_count
                    most_siblings_person = person
                    most_siblings_person_id = person_id

                # Check for close family marriages (if person has spouse)
                if person.get("spouse"):
                    spouse_name = person.get("spouse")
                    # Check if spouse is in the family tree
                    for potential_spouse_id, potential_spouse in family_tree_data.items():
                        if potential_spouse.get("name") == spouse_name:
                            # Check if they share parents (siblings)
                            person_parents = set(person.get("parents", []))
                            spouse_parents = set(potential_spouse.get("parents", []))

                            if person_parents and spouse_parents and person_parents & spouse_parents:
                                # They share at least one parent - siblings or half-siblings
                                close_family_marriages_count += 0.5  # Count each marriage once (will be seen from both sides)

                            # Check if spouse is parent's sibling (aunt/uncle-niece/nephew)
                            for parent_id in person.get("parents", []):
                                if parent_id in family_tree_data:
                                    parent_siblings = family_tree_data[parent_id].get("siblings", [])
                                    if potential_spouse_id in parent_siblings:
                                        close_family_marriages_count += 0.5

                            break

            # Calculate average lifespan
            average_lifespan = round(total_age / people_with_ages, 1) if people_with_ages > 0 else None

            # Add known biblical close family marriages to the count
            close_family_marriages_count += len(known_marriages)

            # Build response
            resp.media = {
                "total_people": total_people,
                "total_generations": total_generations,
                "longest_lived": {
                    "name": longest_lived_person["name"] if longest_lived_person else "Unknown",
                    "person_id": longest_lived_person_id if longest_lived_person_id else "unknown",
                    "value": longest_lifespan,
                    "additional_info": f"Lived {longest_lifespan} years" if longest_lived_person else None
                },
                "most_children": {
                    "name": most_children_person["name"] if most_children_person else "Unknown",
                    "person_id": most_children_person_id if most_children_person_id else "unknown",
                    "value": most_children_count,
                    "additional_info": f"Had {most_children_count} children" if most_children_person else None
                },
                "most_siblings": {
                    "name": most_siblings_person["name"] if most_siblings_person else "Unknown",
                    "person_id": most_siblings_person_id if most_siblings_person_id else "unknown",
                    "value": most_siblings_count,
                    "additional_info": f"Had {most_siblings_count} siblings" if most_siblings_person else None
                },
                "average_lifespan": average_lifespan,
                "total_with_known_ages": people_with_ages,
                "close_family_marriages": int(close_family_marriages_count)
            }
        except Exception as e:
            resp.status_code = 500
            resp.media = {"detail": f"Failed to load family tree statistics: {str(e)}"}
            return

    @api.route("/api/family-tree")
    async def api_list_family_tree(req, resp):
        """List all people with biographies."""
        data = _load_biographies()
        biographies = data.get("biographies", {})

        people = sorted(list(biographies.keys()))

        resp.media = {
            "total": len(people),
            "people": people
        }

    @api.route("/api/family-tree/{name}")
    async def api_get_biography(req, resp, *, name):
        """Get biography of a specific person."""
        data = _load_biographies()
        biographies = data.get("biographies", {})
        aliases = data.get("aliases", {})

        # Check if name is an alias
        if name in aliases:
            name = aliases[name]

        # Get biography
        if name not in biographies:
            resp.status_code = 404
            resp.media = {"detail": f"Biography for '{name}' not found"}
            return

        biography = biographies[name]

        resp.media = {
            "name": name,
            "summary": biography.get("summary", ""),
            "significance": biography.get("significance", ""),
            "key_events": biography.get("key_events", [])
        }

    # =========================================================================
    # Strong's Concordance Endpoints
    # =========================================================================

    @api.route("/api/strongs/{strongs_number}")
    async def api_get_strongs(req, resp, *, strongs_number):
        """Look up a Strong's concordance entry."""
        entry = format_strongs_entry(strongs_number)
        if not entry:
            resp.status_code = 404
            resp.media = {
                "detail": f"Strong's number '{strongs_number}' not found. Use H1-H8674 for Hebrew or G1-G5624 for Greek."
            }
            return
        resp.media = entry

    @api.route("/api/strongs")
    async def api_search_strongs(req, resp):
        """Search Strong's concordance by definition or KJV usage."""
        q = req.params.get("q")
        language = req.params.get("language", "both")
        limit = int(req.params.get("limit", 50))

        results = search_strongs(q, language=language.lower(), limit=limit)
        resp.media = {
            "query": q,
            "language": language,
            "total": len(results),
            "results": results
        }

    @api.route("/api/stats")
    async def api_stats(req, resp):
        """Get comprehensive site statistics."""
        resp.media = compute_site_stats()
