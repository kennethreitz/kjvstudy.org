"""Helper utilities for KJV Study."""
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from functools import lru_cache

from ..kjv import bible, VerseReference, parse_reference_parts
from ..topics import get_all_topics
from ..red_letter import get_christ_words
from ..stories import get_all_stories_flat
from .books import normalize_book_name, GOSPELS

# Paths to data files
_DATA_DIR = Path(__file__).parent.parent / "data"
_CHAPTER_EXPLANATIONS_PATH = _DATA_DIR / "chapter_explanations.json"
_POPULAR_CHAPTERS_PATH = _DATA_DIR / "popular_chapters.json"
_FEATURED_VERSES_PATH = _DATA_DIR / "featured_verses.json"


@lru_cache(maxsize=1)
def _load_chapter_explanations() -> dict:
    """Load chapter explanations from JSON file. Cached since data never changes."""
    with open(_CHAPTER_EXPLANATIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert string keys to integers for chapter numbers
    return {
        book: {int(chapter): explanation for chapter, explanation in chapters.items()}
        for book, chapters in data.items()
    }


@lru_cache(maxsize=1)
def _load_popular_chapters() -> dict:
    """Load popular chapters from JSON file. Cached since data never changes."""
    with open(_POPULAR_CHAPTERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert string keys to integers for chapter numbers
    popular = {
        book: {int(chapter): score for chapter, score in chapters.items()}
        for book, chapters in data["popular_chapters"].items()
    }
    return {
        "popular_chapters": popular,
        "high_readership_books": data["high_readership_books"]
    }


@lru_cache(maxsize=1)
def _load_featured_verses() -> list:
    """Load featured verses (with their devotionals) from JSON. Data never changes."""
    with open(_FEATURED_VERSES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["verses"]


@lru_cache(maxsize=512)
def create_slug(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    Cached since same inputs generate same outputs and called frequently.
    """
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def get_books():
    """Return the list of Bible book names (shared route helper)."""
    return bible.get_books()


def highlight_terms(text: str, terms) -> str:
    """Wrap each search term in <mark> tags (case-insensitive match, case preserved).

    The single shared highlighter, used by both the web search page and the FTS
    index results.
    """
    highlighted = text
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        highlighted = pattern.sub(f'<mark>{term}</mark>', highlighted)
    return highlighted


def get_verse_text(book: str, chapter: int, verse: int) -> str:
    """Get the actual text of a specific verse."""
    try:
        text = bible.get_verse_text(book, chapter, verse)
        if text:
            return text
        return f"{book} {chapter}:{verse} text not found"
    except (KeyError, ValueError, TypeError, AttributeError):
        return f"{book} {chapter}:{verse}"


def is_verse_reference(query: str) -> bool:
    """Check if query looks like a verse reference."""
    # Pattern for verse references like "John 3:16", "1 John 4:8", "Genesis 1:1", etc.
    # Also supports space format like "Rev 22 20" (without colon)
    colon_pattern = r'^(I{1,3}|1|2|3)?\s*[A-Za-z]+(\s+[A-Za-z]+)?\s+\d+:\d+$'
    space_pattern = r'^(I{1,3}|1|2|3)?\s*[A-Za-z]+(\s+[A-Za-z]+)?\s+\d+\s+\d+$'
    query = query.strip()
    return bool(re.match(colon_pattern, query) or re.match(space_pattern, query))


def parse_verse_reference(query: str) -> Optional[Dict]:
    """Parse a verse reference string and return verse info if found."""
    try:
        cleaned_query = query.strip()
        verse_ref = VerseReference.from_string(cleaned_query)

        # Try to normalize the book name (handles abbreviations like "Rev" -> "Revelation")
        book = verse_ref.book
        normalized = normalize_book_name(book)
        if normalized:
            book = normalized

        verse_text = bible.get_verse_text(book, verse_ref.chapter, verse_ref.verse)

        if verse_text:
            return {
                "book": book,
                "chapter": verse_ref.chapter,
                "verse": verse_ref.verse,
                "text": verse_text,
                "reference": f"{book} {verse_ref.chapter}:{verse_ref.verse}",
                "url": f"/book/{book}/chapter/{verse_ref.chapter}#verse-{verse_ref.verse}",
                "score": 100.0,
                "highlighted_text": verse_text
            }
    except Exception as e:
        print(f"Error parsing verse reference '{query}': {e}")

    # Try alternative book name formats (Roman numerals to numbers)
    try:
        alternative_query = query.strip()
        alternative_query = re.sub(r'^I\s+', '1 ', alternative_query)
        alternative_query = re.sub(r'^II\s+', '2 ', alternative_query)
        alternative_query = re.sub(r'^III\s+', '3 ', alternative_query)

        if alternative_query != query.strip():
            verse_ref = VerseReference.from_string(alternative_query)

            # Try to normalize the book name
            book = verse_ref.book
            normalized = normalize_book_name(book)
            if normalized:
                book = normalized

            verse_text = bible.get_verse_text(book, verse_ref.chapter, verse_ref.verse)

            if verse_text:
                return {
                    "book": book,
                    "chapter": verse_ref.chapter,
                    "verse": verse_ref.verse,
                    "text": verse_text,
                    "reference": f"{book} {verse_ref.chapter}:{verse_ref.verse}",
                    "url": f"/book/{book}/chapter/{verse_ref.chapter}#verse-{verse_ref.verse}",
                    "score": 100.0,
                    "highlighted_text": verse_text
                }
    except Exception as e2:
        print(f"Alternative parsing also failed for '{query}': {e2}")

    return None


@lru_cache(maxsize=256)
def get_related_content(book: str, chapter: int = None, verse: int = None) -> Dict:
    """
    Get related study guides, topics, and resources for a given passage.
    Cached since this does expensive dictionary lookups and topic searches.
    """
    related = {
        "study_guides": [],
        "topics": [],
        "people": [],
        "resources": [],
        "stories": []
    }

    # Find related Bible stories based on verse references
    all_stories = get_all_stories_flat()
    for story in all_stories:
        story_verses = story.get("verses", [])
        for verse_ref in story_verses:
            # Parse verse references like "Genesis 1:1-31" or "Genesis 2:1-3"
            if verse_ref.startswith(book + " "):
                # Extract chapter from reference
                ref_part = verse_ref[len(book) + 1:]  # e.g., "1:1-31" or "2:1-3"
                if ":" in ref_part:
                    ref_chapter = ref_part.split(":")[0]
                    try:
                        ref_chapter_num = int(ref_chapter)
                        # If chapter matches (or no chapter specified), include this story
                        if chapter is None or ref_chapter_num == chapter:
                            story_entry = {
                                "name": story.get("title", ""),
                                "url": f"/stories/{story.get('slug', '')}",
                                "description": story.get("description", "")[:100] + "..." if len(story.get("description", "")) > 100 else story.get("description", "")
                            }
                            # Avoid duplicates
                            if story_entry not in related["stories"]:
                                related["stories"].append(story_entry)
                                break  # Only add each story once per book/chapter match
                    except ValueError:
                        pass

    # Map books to related people
    book_people_map = {
        "Genesis": [{"name": "Abraham", "url": "/family-tree/person/i60"}, {"name": "Jacob", "url": "/family-tree/person/i58"}],
        "Exodus": [{"name": "Moses", "url": "/biblical-prophets/moses"}],
        "1 Samuel": [{"name": "Samuel", "url": "/biblical-prophets"}],
        "2 Samuel": [{"name": "David", "url": "/family-tree/person/i113"}],
        "1 Kings": [{"name": "Elijah", "url": "/biblical-prophets/elijah"}],
        "2 Kings": [{"name": "Elijah", "url": "/biblical-prophets/elijah"}, {"name": "Elisha", "url": "/biblical-prophets"}],
        "Isaiah": [{"name": "Isaiah", "url": "/biblical-prophets/isaiah"}],
        "Jeremiah": [{"name": "Jeremiah", "url": "/biblical-prophets/jeremiah"}],
        "Ezekiel": [{"name": "Ezekiel", "url": "/biblical-prophets/ezekiel"}],
        "Daniel": [{"name": "Daniel", "url": "/biblical-prophets/daniel"}],
        "Jonah": [{"name": "Jonah", "url": "/biblical-prophets/jonah"}],
        "Matthew": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}],
        "Mark": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}],
        "Luke": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}, {"name": "John the Baptist", "url": "/biblical-prophets"}],
        "John": [{"name": "John", "url": "/the-twelve-apostles/john"}],
        "Acts": [{"name": "Peter", "url": "/the-twelve-apostles/simon-peter"}, {"name": "Paul", "url": "/the-twelve-apostles"}],
        "Ruth": [{"name": "Ruth", "url": "/women-of-the-bible/ruth"}],
        "Esther": [{"name": "Esther", "url": "/women-of-the-bible/esther"}],
    }

    if book in book_people_map:
        related["people"] = book_people_map[book]

    # Map books/passages to special resources
    if book in ["Exodus", "Leviticus", "Numbers", "Deuteronomy"]:
        related["resources"].append({"name": "Biblical Festivals", "url": "/biblical-festivals"})
        related["resources"].append({"name": "Biblical Covenants", "url": "/biblical-covenants"})

    if book in ["Genesis", "Exodus", "Numbers"]:
        related["resources"].append({"name": "Biblical Timeline", "url": "/biblical-timeline"})

    if book in ["Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings"]:
        related["resources"].append({"name": "Biblical Maps", "url": "/biblical-maps"})

    if book in GOSPELS:
        related["resources"].append({"name": "Parables of Jesus", "url": "/parables"})

    # Add topic links based on verse references in topic data
    topics_data = get_all_topics()
    for topic_name, topic_data in topics_data.items():
        topic_matched = False
        # Check subtopics for verse references
        subtopics = topic_data.get("subtopics", {})
        for subtopic_name, subtopic_data in subtopics.items():
            if topic_matched:
                break
            verses = subtopic_data.get("verses", [])
            for verse_entry in verses:
                ref = verse_entry.get("ref", "")
                # Check if this reference matches our book/chapter
                if ref.startswith(book + " "):
                    ref_part = ref[len(book) + 1:]
                    if ":" in ref_part:
                        ref_chapter = ref_part.split(":")[0]
                        try:
                            ref_chapter_num = int(ref_chapter)
                            if chapter is None or ref_chapter_num == chapter:
                                related["topics"].append({
                                    "name": topic_name,
                                    "url": f"/topics/{topic_name}"
                                })
                                topic_matched = True
                                break
                        except ValueError:
                            pass

    # Add specific resource pages based on book/chapter
    specific_resources = {
        # Sermon on the Mount / Beatitudes
        ("Matthew", 5): [{"name": "The Beatitudes", "url": "/beatitudes"}],
        ("Matthew", 6): [{"name": "Prayers of the Bible", "url": "/prayers-of-the-bible"}],
        ("Matthew", 7): [{"name": "The Beatitudes", "url": "/beatitudes"}],
        # Ten Commandments
        ("Exodus", 20): [{"name": "Ten Commandments", "url": "/ten-commandments"}],
        ("Deuteronomy", 5): [{"name": "Ten Commandments", "url": "/ten-commandments"}],
        # Armor of God & Spiritual Warfare
        ("Ephesians", 6): [{"name": "Armor of God", "url": "/armor-of-god"}, {"name": "Spirits and Demons", "url": "/spirits-and-demons"}],
        # Fruits of the Spirit
        ("Galatians", 5): [{"name": "Fruits of the Spirit", "url": "/fruits-of-the-spirit"}],
        # I Am Statements (John's Gospel)
        ("John", 6): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}],
        ("John", 8): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}],
        ("John", 10): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}],
        ("John", 11): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}],
        ("John", 14): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}, {"name": "The Trinity", "url": "/trinity"}],
        ("John", 15): [{"name": "I Am Statements of Jesus", "url": "/i-am-statements"}],
        # John 1 - Christology, Names of Christ
        ("John", 1): [{"name": "Names of Christ", "url": "/names-of-christ"}, {"name": "Christology", "url": "/christology"}],
        # Love chapter
        ("1 Corinthians", 13): [{"name": "Biblical Love", "url": "/topics/Love"}],
        # Faith chapter
        ("Hebrews", 11): [{"name": "Heroes of Faith", "url": "/topics/Faith"}],
        # Messianic prophecies in key OT chapters
        ("Isaiah", 7): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Isaiah", 9): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Isaiah", 11): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Isaiah", 53): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Micah", 5): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Zechariah", 9): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Zechariah", 12): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Psalm", 22): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Psalms", 22): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Psalms", 110): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Daniel", 7): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        ("Daniel", 9): [{"name": "Messianic Prophecies", "url": "/messianic-prophecies"}],
        # Names of God
        ("Exodus", 3): [{"name": "Names of God", "url": "/names-of-god"}, {"name": "Tetragrammaton", "url": "/tetragrammaton"}],
        ("Exodus", 6): [{"name": "Names of God", "url": "/names-of-god"}],
        ("Genesis", 14): [{"name": "Names of God", "url": "/names-of-god"}],
        ("Genesis", 22): [{"name": "Names of God", "url": "/names-of-god"}],
        # Biblical covenants
        ("Genesis", 9): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("Genesis", 15): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("Genesis", 17): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("2 Samuel", 7): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("Jeremiah", 31): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("Hebrews", 8): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}],
        ("Hebrews", 9): [{"name": "Biblical Covenants", "url": "/biblical-covenants"}, {"name": "Blood in Scripture", "url": "/blood-in-scripture"}],
        # Angels
        ("Genesis", 18): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Genesis", 19): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Daniel", 10): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Luke", 1): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Luke", 2): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Revelation", 4): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        ("Revelation", 5): [{"name": "Biblical Angels", "url": "/biblical-angels"}],
        # Trinity
        ("Matthew", 3): [{"name": "The Trinity", "url": "/trinity"}],
        ("Matthew", 28): [{"name": "The Trinity", "url": "/trinity"}],
        ("2 Corinthians", 13): [{"name": "The Trinity", "url": "/trinity"}],
        # Holy Spirit / Pneumatology
        ("Acts", 2): [{"name": "Pneumatology", "url": "/pneumatology"}],
        ("John", 16): [{"name": "Pneumatology", "url": "/pneumatology"}],
        ("Romans", 8): [{"name": "Pneumatology", "url": "/pneumatology"}, {"name": "Providence", "url": "/providence"}],
        # Eschatology
        ("Matthew", 24): [{"name": "Eschatology", "url": "/eschatology"}],
        ("Matthew", 25): [{"name": "Eschatology", "url": "/eschatology"}],
        ("1 Thessalonians", 4): [{"name": "Eschatology", "url": "/eschatology"}],
        ("2 Thessalonians", 2): [{"name": "Eschatology", "url": "/eschatology"}],
        ("Revelation", 20): [{"name": "Eschatology", "url": "/eschatology"}],
        ("Revelation", 21): [{"name": "Eschatology", "url": "/eschatology"}],
        ("Revelation", 22): [{"name": "Eschatology", "url": "/eschatology"}],
        # Ecclesiology (Church)
        ("Matthew", 16): [{"name": "Ecclesiology", "url": "/ecclesiology"}],
        ("Matthew", 18): [{"name": "Ecclesiology", "url": "/ecclesiology"}],
        ("1 Corinthians", 12): [{"name": "Ecclesiology", "url": "/ecclesiology"}],
        ("Ephesians", 4): [{"name": "Ecclesiology", "url": "/ecclesiology"}],
        # Soteriology (Salvation)
        ("Romans", 3): [{"name": "Soteriology", "url": "/soteriology"}],
        ("Romans", 5): [{"name": "Soteriology", "url": "/soteriology"}, {"name": "Justification", "url": "/justification"}],
        ("Romans", 6): [{"name": "Soteriology", "url": "/soteriology"}, {"name": "Sanctification", "url": "/sanctification"}],
        ("Ephesians", 2): [{"name": "Soteriology", "url": "/soteriology"}, {"name": "Grace", "url": "/grace"}],
        ("Titus", 3): [{"name": "Soteriology", "url": "/soteriology"}],
        # Types and Shadows
        ("Hebrews", 10): [{"name": "Types and Shadows", "url": "/types-and-shadows"}],
        # Blood in Scripture
        ("Leviticus", 17): [{"name": "Blood in Scripture", "url": "/blood-in-scripture"}],
        # Kingdom of God
        ("Matthew", 13): [{"name": "Kingdom of God", "url": "/kingdom-of-god"}],
        ("Mark", 4): [{"name": "Kingdom of God", "url": "/kingdom-of-god"}],
        ("Luke", 17): [{"name": "Kingdom of God", "url": "/kingdom-of-god"}],
        # Miracles of Jesus
        ("Matthew", 8): [{"name": "Miracles of Jesus", "url": "/miracles-of-jesus"}],
        ("Matthew", 9): [{"name": "Miracles of Jesus", "url": "/miracles-of-jesus"}],
        ("Mark", 5): [{"name": "Miracles of Jesus", "url": "/miracles-of-jesus"}],
        ("John", 2): [{"name": "Miracles of Jesus", "url": "/miracles-of-jesus"}],
        ("John", 9): [{"name": "Miracles of Jesus", "url": "/miracles-of-jesus"}],
        # Christology
        ("Colossians", 1): [{"name": "Christology", "url": "/christology"}],
        ("Philippians", 2): [{"name": "Christology", "url": "/christology"}],
        ("Hebrews", 1): [{"name": "Christology", "url": "/christology"}],
        # Law and Gospel
        ("Romans", 7): [{"name": "Law and Gospel", "url": "/law-and-gospel"}],
        ("Galatians", 3): [{"name": "Law and Gospel", "url": "/law-and-gospel"}],
        # Hamartiology (Sin)
        ("Genesis", 3): [{"name": "Hamartiology", "url": "/hamartiology"}],
        ("Romans", 1): [{"name": "Hamartiology", "url": "/hamartiology"}],
        # Providence
        ("Genesis", 50): [{"name": "Providence", "url": "/providence"}],
        # Worship
        ("Psalms", 100): [{"name": "Worship", "url": "/worship"}],
        ("Psalms", 150): [{"name": "Worship", "url": "/worship"}],
        ("John", 4): [{"name": "Worship", "url": "/worship"}],
        # Spirits and Demons
        ("1 Peter", 5): [{"name": "Spirits and Demons", "url": "/spirits-and-demons"}],
    }

    if chapter is not None:
        key = (book, chapter)
        if key in specific_resources:
            for resource in specific_resources[key]:
                if resource not in related["resources"]:
                    related["resources"].append(resource)

    return related


# Load popular chapters data from JSON
_popular_data = _load_popular_chapters()
POPULAR_CHAPTERS = _popular_data["popular_chapters"]
HIGH_READERSHIP_BOOKS = _popular_data["high_readership_books"]


@lru_cache(maxsize=512)
def get_chapter_popularity_score(book: str, chapter: int) -> int:
    """
    Calculate popularity score for a chapter (1-10 scale) based on well-known verses.
    Cached since calculation is deterministic and called frequently.
    """
    if book in POPULAR_CHAPTERS and chapter in POPULAR_CHAPTERS[book]:
        return POPULAR_CHAPTERS[book][chapter]

    default_score = 4

    if chapter == 1:
        default_score += 1

    if book in HIGH_READERSHIP_BOOKS:
        default_score += 1

    total_chapters = len(bible.get_chapters_for_book(book))
    if total_chapters <= 5:
        default_score += 1

    return min(default_score, 6)


# Load chapter explanations from JSON
CHAPTER_EXPLANATIONS = _load_chapter_explanations()


def get_chapter_popularity_explanation(book: str, chapter: int) -> str:
    """Get explanation for why a chapter is popular or what it contains."""
    if book in CHAPTER_EXPLANATIONS and chapter in CHAPTER_EXPLANATIONS[book]:
        return CHAPTER_EXPLANATIONS[book][chapter]

    if chapter == 1:
        return f"Opening chapter of {book} - introduces key themes and characters"

    if book in GOSPELS:
        return "Gospel account of Jesus' life and ministry"
    elif book in ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]:
        return "Torah/Pentateuch - foundational law and history of Israel"
    elif book in ["Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon"]:
        return "Wisdom literature - poetry and practical life guidance"
    elif book in ["Isaiah", "Jeremiah", "Ezekiel", "Daniel"]:
        return "Major prophet - messages of judgment and hope"
    elif book in ["Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
                  "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
                  "1 Timothy", "2 Timothy", "Titus", "Philemon"]:
        return "Pauline epistle - apostolic teaching for the early church"
    elif book == "Acts":
        return "History of the early church and spread of the gospel"
    elif book == "Revelation":
        return "Apocalyptic vision of the end times and Christ's victory"
    else:
        return f"Part of {book} - explore this chapter to discover its significance"


# Load featured verses from JSON
FEATURED_VERSES = _load_featured_verses()


def get_daily_verse(date_str: Optional[str] = None) -> Dict:
    """Get the verse of the day for a given date (current date if omitted).

    Calendar-aligned (Jan 1 -> the first featured verse). This is the single
    source of truth shared by the web pages and /api/verse-of-the-day so they
    always show the same verse for a given day.
    """
    if date_str is None:
        date_obj = datetime.now()
        date_str = date_obj.strftime("%Y-%m-%d")
    else:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    if FEATURED_VERSES:
        day_of_year = date_obj.timetuple().tm_yday  # 1-366
        verse_data = FEATURED_VERSES[(day_of_year - 1) % len(FEATURED_VERSES)]
    else:
        verse_data = {"book": "John", "chapter": 3, "verse": 16}

    book = verse_data["book"]
    chapter = verse_data["chapter"]
    verse = verse_data["verse"]
    devotional = verse_data.get("devotional")

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        # Fallback to John 3:16 if the configured verse is missing
        book, chapter, verse, devotional = "John", 3, 16, None
        verse_text = bible.get_verse_text(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": verse_text,
        "reference": f"{book} {chapter}:{verse}",
        "url": f"/book/{book}/chapter/{chapter}#verse-{verse}",
        "date": date_str,
        "devotional": devotional,
        "red_letter": get_christ_words(book, chapter, verse),
    }


def verse_reference_to_url(reference: str) -> Optional[str]:
    """Convert a verse reference to its chapter-anchor URL (the site-wide form).

    Examples:
        "John 3:16"      -> "/book/John/chapter/3#verse-16"
        "Romans 8:38-39" -> "/book/Romans/chapter/8#verse-38-39"
    Returns None if the reference cannot be parsed. Handles multi-word and
    numbered book names (e.g. "Song of Solomon", "1 Corinthians").
    """
    parts = parse_reference_parts(reference)
    if not parts:
        return None

    book, chapter, verse, verse_end = parts
    if verse_end:
        return f"/book/{book}/chapter/{chapter}#verse-{verse}-{verse_end}"
    return f"/book/{book}/chapter/{chapter}#verse-{verse}"
