"""Helper utilities for KJV Study."""
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from functools import lru_cache

from ..kjv import bible, VerseReference
from ..topics import get_all_topics
from ..red_letter import get_christ_words

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
    """Load featured verses from JSON file. Cached since data never changes."""
    with open(_FEATURED_VERSES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convert dict format to tuple format for compatibility
    return [
        (verse["book"], verse["chapter"], verse["verse"])
        for verse in data["verses"]
    ]


@lru_cache(maxsize=512)
def create_slug(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    Cached since same inputs generate same outputs and called frequently.
    """
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def get_verse_text(book: str, chapter: int, verse: int) -> str:
    """Get the actual text of a specific verse."""
    try:
        text = bible.get_verse_text(book, chapter, verse)
        if text:
            return text
        return f"{book} {chapter}:{verse} text not found"
    except:
        return f"{book} {chapter}:{verse}"


def is_verse_reference(query: str) -> bool:
    """Check if query looks like a verse reference."""
    # Pattern for verse references like "John 3:16", "1 John 4:8", "Genesis 1:1", etc.
    verse_pattern = r'^(I{1,3}|1|2|3)?\s*[A-Za-z]+(\s+[A-Za-z]+)?\s+\d+:\d+$'
    return bool(re.match(verse_pattern, query.strip()))


def parse_verse_reference(query: str) -> Optional[Dict]:
    """Parse a verse reference string and return verse info if found."""
    try:
        cleaned_query = query.strip()
        verse_ref = VerseReference.from_string(cleaned_query)
        verse_text = bible.get_verse_text(verse_ref.book, verse_ref.chapter, verse_ref.verse)

        if verse_text:
            return {
                "book": verse_ref.book,
                "chapter": verse_ref.chapter,
                "verse": verse_ref.verse,
                "text": verse_text,
                "reference": f"{verse_ref.book} {verse_ref.chapter}:{verse_ref.verse}",
                "url": f"/book/{verse_ref.book}/chapter/{verse_ref.chapter}#verse-{verse_ref.verse}",
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
            verse_text = bible.get_verse_text(verse_ref.book, verse_ref.chapter, verse_ref.verse)

            if verse_text:
                return {
                    "book": verse_ref.book,
                    "chapter": verse_ref.chapter,
                    "verse": verse_ref.verse,
                    "text": verse_text,
                    "reference": f"{verse_ref.book} {verse_ref.chapter}:{verse_ref.verse}",
                    "url": f"/book/{verse_ref.book}/chapter/{verse_ref.chapter}#verse-{verse_ref.verse}",
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
        "resources": []
    }

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

    if book in ["Matthew", "Mark", "Luke", "John"]:
        related["resources"].append({"name": "Parables of Jesus", "url": "/parables"})

    # Add topic links based on common themes
    topic_keywords = {
        "Salvation": ["John", "Romans", "Ephesians", "Titus"],
        "Prayer": ["Matthew", "Luke", "1 Thessalonians", "James"],
        "Love": ["John", "1 Corinthians", "1 John"],
        "Faith": ["Hebrews", "James", "Romans"],
        "Hope": ["Romans", "1 Peter", "Hebrews"],
        "Peace": ["Philippians", "John", "Romans"],
        "Wisdom": ["Proverbs", "Ecclesiastes", "James"],
    }

    topics_data = get_all_topics()
    for topic_name in topics_data.keys():
        if topic_name in topic_keywords and book in topic_keywords[topic_name]:
            related["topics"].append({"name": topic_name, "url": f"/topics/{topic_name}"})

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

    if book in ["Matthew", "Mark", "Luke", "John"]:
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


def get_daily_verse() -> Dict:
    """Get the verse of the day based on the current date."""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    verse_index = day_of_year % len(FEATURED_VERSES)

    book, chapter, verse = FEATURED_VERSES[verse_index]
    verse_text = bible.get_verse_text(book, chapter, verse)
    christ_words = get_christ_words(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": verse_text,
        "reference": f"{book} {chapter}:{verse}",
        "url": f"/book/{book}/chapter/{chapter}#verse-{verse}",
        "red_letter": christ_words
    }
