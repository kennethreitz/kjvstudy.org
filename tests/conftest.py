"""
Shared pytest configuration and fixtures
"""
import pytest
from kjvstudy_org.server import api


@pytest.fixture(scope="session")
def client():
    """
    Create test client fixture with session scope for reuse across tests.
    api.requests is a Starlette TestClient against the Responder app.
    """
    return api.requests


@pytest.fixture(scope="session")
def sample_verses():
    """Sample verse references for testing"""
    return {
        "john_3_16": {"book": "John", "chapter": 3, "verse": 16},
        "genesis_1_1": {"book": "Genesis", "chapter": 1, "verse": 1},
        "psalms_23": {"book": "Psalms", "chapter": 23, "start": 1, "end": 6},
        "matthew_5_14": {"book": "Matthew", "chapter": 5, "verse": 14},
        "romans_8_28": {"book": "Romans", "chapter": 8, "verse": 28},
    }


@pytest.fixture(scope="session")
def sample_books():
    """Sample book names for testing"""
    return {
        "short_book": "Philemon",
        "long_book": "Genesis",
        "new_testament": "John",
        "old_testament": "Psalms",
        "first_book": "Genesis",
        "last_book": "Revelation",
    }


@pytest.fixture(scope="session")
def book_abbreviations():
    """Common book abbreviations mapping"""
    return {
        # Old Testament
        "Gen": "Genesis",
        "Exo": "Exodus",
        "Lev": "Leviticus",
        "Num": "Numbers",
        "Deut": "Deuteronomy",
        "Josh": "Joshua",
        "Ps": "Psalms",
        "Prov": "Proverbs",
        "Isa": "Isaiah",
        "Jer": "Jeremiah",
        "Ezek": "Ezekiel",
        "Dan": "Daniel",
        # New Testament
        "Matt": "Matthew",
        "Rom": "Romans",
        "Gal": "Galatians",
        "Eph": "Ephesians",
        "Phil": "Philippians",
        "Col": "Colossians",
        "Heb": "Hebrews",
        "Jas": "James",
        "Rev": "Revelation",
    }


@pytest.fixture(scope="session")
def bible_facts():
    """Known facts about the KJV Bible for validation"""
    return {
        "total_books": 66,
        "total_verses": 31102,
        "old_testament_books": 39,
        "new_testament_books": 27,
        "longest_chapter": {"book": "Psalms", "chapter": 119, "verses": 176},
        "longest_book": {"name": "Psalms", "chapters": 150},
    }
