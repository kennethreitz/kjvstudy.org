"""Helper utilities for KJV Study."""
import re
import hashlib
from datetime import datetime
from typing import Optional, Dict, List
from functools import lru_cache

from ..kjv import bible, VerseReference
from ..topics import get_all_topics


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
        "Genesis": [{"name": "Abraham", "url": "/family-tree"}, {"name": "Jacob", "url": "/family-tree"}],
        "Exodus": [{"name": "Moses", "url": "/biblical-prophets/moses"}],
        "1 Samuel": [{"name": "Samuel", "url": "/biblical-prophets"}],
        "2 Samuel": [{"name": "David", "url": "/family-tree"}],
        "1 Kings": [{"name": "Elijah", "url": "/biblical-prophets/elijah"}],
        "2 Kings": [{"name": "Elijah", "url": "/biblical-prophets/elijah"}, {"name": "Elisha", "url": "/biblical-prophets"}],
        "Isaiah": [{"name": "Isaiah", "url": "/biblical-prophets/isaiah"}],
        "Jeremiah": [{"name": "Jeremiah", "url": "/biblical-prophets/jeremiah"}],
        "Ezekiel": [{"name": "Ezekiel", "url": "/biblical-prophets/ezekiel"}],
        "Daniel": [{"name": "Daniel", "url": "/biblical-prophets/daniel"}],
        "Jonah": [{"name": "Jonah", "url": "/biblical-prophets/jonah"}],
        "Matthew": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}],
        "Mark": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}],
        "Luke": [{"name": "The Twelve Apostles", "url": "/the-twelve-apostles"}, {"name": "John the Baptist", "url": "/biblical-prophets/john-the-baptist"}],
        "John": [{"name": "John", "url": "/the-twelve-apostles/john"}],
        "Acts": [{"name": "Peter", "url": "/the-twelve-apostles/peter"}, {"name": "Paul", "url": "/the-twelve-apostles"}],
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


# Popular/well-known chapters with their scores (1-10 scale)
POPULAR_CHAPTERS = {
    "John": {3: 10},
    "1 Corinthians": {13: 10},
    "Psalms": {23: 10, 91: 9, 1: 8, 139: 8},
    "Romans": {8: 9, 3: 8, 12: 8},
    "Matthew": {5: 9, 6: 8, 7: 8},
    "Ephesians": {2: 8, 6: 8},
    "Philippians": {4: 8},
    "Genesis": {1: 9, 3: 8, 22: 7},
    "Exodus": {20: 8, 14: 7},
    "Isaiah": {53: 9, 40: 8},
    "Jeremiah": {29: 7},
    "Proverbs": {31: 7, 3: 7},
    "Ecclesiastes": {3: 8},
    "1 Peter": {5: 7},
    "James": {1: 7},
    "Hebrews": {11: 8, 12: 7},
    "Revelation": {21: 8, 22: 7},
    "Luke": {2: 9, 15: 8},
    "2 Timothy": {3: 7},
    "Joshua": {1: 7},
    "Daniel": {3: 7, 6: 7},
    "1 John": {4: 8},
    "Galatians": {5: 7},
    "Colossians": {3: 7},
    "1 Thessalonians": {4: 7},
    "Mark": {16: 7},
    "Acts": {2: 8},
    "1 Samuel": {17: 7},
    "Job": {19: 7},
    "2 Corinthians": {5: 7},
    "1 Kings": {3: 6, 18: 6},
    "Malachi": {3: 6},
    "Joel": {2: 6},
    "Micah": {6: 6},
    "Habakkuk": {2: 6},
}

HIGH_READERSHIP_BOOKS = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "Genesis", "Exodus", "Psalms", "Proverbs"
]


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


# Chapter explanations for popular chapters
CHAPTER_EXPLANATIONS = {
    "John": {
        3: "Contains John 3:16 - 'For God so loved the world' - the most quoted verse in Christianity",
        1: "The Word became flesh - Jesus as the eternal Logos and the calling of the first disciples",
    },
    "1 Corinthians": {
        13: "The famous 'Love Chapter' - 'Love is patient, love is kind' - essential reading for weddings and Christian living",
    },
    "Psalms": {
        23: "The beloved Shepherd Psalm - 'The Lord is my shepherd, I shall not want' - comfort in times of trouble",
        91: "Psalm of protection - 'He who dwells in the shelter of the Most High' - promises of God's care",
        1: "The blessed man - contrasts the righteous and wicked, foundation of wisdom literature",
        139: "God's omniscience and omnipresence - 'You have searched me and known me' - intimate knowledge of God",
    },
    "Romans": {
        8: "No condemnation in Christ - 'All things work together for good' - assurance of salvation",
        3: "All have sinned - universal need for salvation and justification by faith",
        12: "Living sacrifice - practical Christian living and spiritual gifts",
    },
    "Matthew": {
        5: "The Beatitudes - 'Blessed are the poor in spirit' - foundation of Christian ethics",
        6: "The Lord's Prayer and teachings on worry - 'Give us this day our daily bread'",
        7: "Golden Rule and narrow gate - 'Do unto others as you would have them do unto you'",
    },
    "Genesis": {
        1: "Creation account - 'In the beginning God created the heavens and the earth'",
        3: "The Fall - Adam and Eve's disobedience and the first promise of redemption",
        22: "Abraham's ultimate test - the near-sacrifice of Isaac, foreshadowing Christ",
    },
    "Isaiah": {
        53: "The Suffering Servant - 'He was wounded for our transgressions' - prophecy of Christ's crucifixion",
        40: "Comfort my people - 'Every valley shall be exalted' - hope and restoration",
    },
}


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


# Featured verses for verse of the day
FEATURED_VERSES = [
    ("John", 3, 16),
    ("Psalms", 23, 1),
    ("Proverbs", 3, 5),
    ("Philippians", 4, 13),
    ("Romans", 8, 28),
    ("Isaiah", 40, 31),
    ("Jeremiah", 29, 11),
    ("Joshua", 1, 9),
    ("Matthew", 11, 28),
    ("Psalms", 46, 10),
    ("Romans", 12, 2),
    ("2 Timothy", 1, 7),
    ("Proverbs", 22, 6),
    ("1 Corinthians", 13, 4),
    ("Galatians", 5, 22),
    ("Hebrews", 11, 1),
    ("James", 1, 2),
    ("1 Peter", 5, 7),
    ("Psalms", 119, 105),
    ("Matthew", 6, 33),
    ("John", 14, 6),
    ("Romans", 5, 8),
    ("Ephesians", 2, 8),
    ("Psalms", 27, 1),
    ("Isaiah", 41, 10),
    ("Matthew", 28, 19),
    ("John", 1, 1),
    ("Psalms", 51, 10),
    ("Proverbs", 18, 10),
    ("2 Corinthians", 5, 17),
    ("Colossians", 3, 23),
]


def get_daily_verse() -> Dict:
    """Get the verse of the day based on the current date."""
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    verse_index = day_of_year % len(FEATURED_VERSES)

    book, chapter, verse = FEATURED_VERSES[verse_index]
    verse_text = bible.get_verse_text(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": verse_text,
        "reference": f"{book} {chapter}:{verse}",
        "url": f"/book/{book}/chapter/{chapter}#verse-{verse}"
    }
