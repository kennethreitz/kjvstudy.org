"""
Tests for Strong's Concordance functionality.

Tests cover:
- Strong's data loading and lookup
- Hebrew and Greek entry retrieval
- Search functionality
- Pagination
- Web routes
- API endpoints
"""

import pytest
from fastapi.testclient import TestClient

from kjvstudy_org.server import app
from kjvstudy_org.strongs import (
    get_strongs_entry,
    get_strongs_definition,
    get_strongs_word,
    get_strongs_transliteration,
    get_strongs_kjv_usage,
    format_strongs_entry,
    search_strongs,
    get_all_strongs,
)


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestStrongsDataLoading:
    """Tests for Strong's data loading and basic lookup"""

    def test_get_hebrew_entry(self):
        """Test retrieving a Hebrew Strong's entry"""
        entry = get_strongs_entry("H1")
        assert entry is not None
        assert "lemma" in entry

    def test_get_greek_entry(self):
        """Test retrieving a Greek Strong's entry"""
        entry = get_strongs_entry("G1")
        assert entry is not None
        assert "lemma" in entry

    def test_get_entry_case_insensitive(self):
        """Test Strong's lookup is case-insensitive"""
        entry1 = get_strongs_entry("H430")
        entry2 = get_strongs_entry("h430")
        assert entry1 == entry2

    def test_get_entry_with_whitespace(self):
        """Test Strong's lookup handles whitespace"""
        entry = get_strongs_entry("  H1  ")
        assert entry is not None

    def test_get_invalid_entry(self):
        """Test invalid Strong's number returns None"""
        entry = get_strongs_entry("X9999")
        assert entry is None

    def test_get_nonexistent_entry(self):
        """Test nonexistent Strong's number returns None"""
        entry = get_strongs_entry("H99999")
        assert entry is None

    def test_get_empty_entry(self):
        """Test empty string returns None"""
        entry = get_strongs_entry("")
        assert entry is None

    def test_get_none_entry(self):
        """Test None input returns None"""
        entry = get_strongs_entry(None)
        assert entry is None


class TestStrongsHelperFunctions:
    """Tests for Strong's helper functions"""

    def test_get_definition(self):
        """Test getting Strong's definition"""
        definition = get_strongs_definition("G26")
        assert definition is not None
        assert len(definition) > 0

    def test_get_word(self):
        """Test getting original word (lemma)"""
        word = get_strongs_word("G26")
        assert word is not None
        # Greek agape
        assert "γάπ" in word or "agap" in word.lower()

    def test_get_transliteration(self):
        """Test getting transliteration"""
        translit = get_strongs_transliteration("G26")
        assert translit is not None
        # Transliteration is "agápē" - check for base characters
        assert "ag" in translit.lower() and "p" in translit.lower()

    def test_get_kjv_usage(self):
        """Test getting KJV usage"""
        usage = get_strongs_kjv_usage("G26")
        assert usage is not None
        assert "love" in usage.lower()

    def test_get_hebrew_transliteration(self):
        """Test Hebrew transliteration uses xlit field"""
        translit = get_strongs_transliteration("H1")
        assert translit is not None

    def test_helper_functions_invalid_number(self):
        """Test helper functions handle invalid numbers"""
        assert get_strongs_definition("X9999") is None
        assert get_strongs_word("X9999") is None
        assert get_strongs_transliteration("X9999") is None
        assert get_strongs_kjv_usage("X9999") is None


class TestFormatStrongsEntry:
    """Tests for format_strongs_entry function"""

    def test_format_greek_entry(self):
        """Test formatting Greek entry"""
        entry = format_strongs_entry("G26")
        assert entry is not None
        assert entry["strongs"] == "G26"
        assert entry["language"] == "Greek"
        assert "word" in entry
        assert "definition" in entry

    def test_format_hebrew_entry(self):
        """Test formatting Hebrew entry"""
        entry = format_strongs_entry("H430")
        assert entry is not None
        assert entry["strongs"] == "H430"
        assert entry["language"] == "Hebrew"
        assert "word" in entry
        assert "definition" in entry

    def test_format_entry_has_all_fields(self):
        """Test formatted entry has all expected fields"""
        entry = format_strongs_entry("G26")
        expected_fields = [
            "strongs", "language", "word", "transliteration",
            "definition", "kjv_usage", "derivation"
        ]
        for field in expected_fields:
            assert field in entry

    def test_format_hebrew_has_pronunciation(self):
        """Test Hebrew entries include pronunciation"""
        entry = format_strongs_entry("H1")
        assert "pronunciation" in entry

    def test_format_invalid_entry(self):
        """Test formatting invalid entry returns None"""
        entry = format_strongs_entry("X9999")
        assert entry is None


class TestSearchStrongs:
    """Tests for Strong's search functionality"""

    def test_search_finds_results(self):
        """Test search returns results"""
        results = search_strongs("love")
        assert len(results) > 0

    def test_search_result_structure(self):
        """Test search results have correct structure"""
        results = search_strongs("love", limit=1)
        assert len(results) > 0
        result = results[0]
        assert "strongs" in result
        assert "language" in result
        assert "word" in result
        assert "definition" in result

    def test_search_hebrew_only(self):
        """Test search Hebrew only"""
        results = search_strongs("God", language="hebrew")
        for result in results:
            assert result["language"] == "Hebrew"

    def test_search_greek_only(self):
        """Test search Greek only"""
        results = search_strongs("love", language="greek")
        for result in results:
            assert result["language"] == "Greek"

    def test_search_both_languages(self):
        """Test search both languages"""
        results = search_strongs("peace", language="both")
        languages = set(r["language"] for r in results)
        # Should have at least one result
        assert len(results) > 0

    def test_search_respects_limit(self):
        """Test search respects limit parameter"""
        results = search_strongs("the", limit=5)
        assert len(results) <= 5

    def test_search_case_insensitive(self):
        """Test search is case-insensitive"""
        results1 = search_strongs("love")
        results2 = search_strongs("LOVE")
        assert len(results1) == len(results2)

    def test_search_no_results(self):
        """Test search with no results"""
        results = search_strongs("xyznonexistent123")
        assert len(results) == 0


class TestGetAllStrongs:
    """Tests for paginated Strong's listing"""

    def test_get_all_hebrew(self):
        """Test getting all Hebrew entries"""
        data = get_all_strongs("hebrew", page=1, per_page=100)
        assert "entries" in data
        assert "total" in data
        assert "page" in data
        assert "total_pages" in data
        assert len(data["entries"]) == 100
        assert data["total"] > 8000  # Should have ~8674 Hebrew entries

    def test_get_all_greek(self):
        """Test getting all Greek entries"""
        data = get_all_strongs("greek", page=1, per_page=100)
        assert len(data["entries"]) == 100
        assert data["total"] > 5000  # Should have ~5523 Greek entries

    def test_pagination_page_2(self):
        """Test pagination returns different entries"""
        page1 = get_all_strongs("hebrew", page=1, per_page=10)
        page2 = get_all_strongs("hebrew", page=2, per_page=10)

        # Entries should be different
        page1_ids = [e["strongs"] for e in page1["entries"]]
        page2_ids = [e["strongs"] for e in page2["entries"]]
        assert page1_ids != page2_ids

    def test_pagination_total_pages(self):
        """Test total pages calculation"""
        data = get_all_strongs("hebrew", page=1, per_page=100)
        expected_pages = (data["total"] + 99) // 100
        assert data["total_pages"] == expected_pages

    def test_entries_sorted_by_number(self):
        """Test entries are sorted by Strong's number"""
        data = get_all_strongs("hebrew", page=1, per_page=10)
        numbers = [int(e["strongs"][1:]) for e in data["entries"]]
        assert numbers == sorted(numbers)

    def test_invalid_language(self):
        """Test invalid language returns empty"""
        data = get_all_strongs("invalid", page=1)
        assert data["entries"] == []
        assert data["total"] == 0

    def test_entry_has_required_fields(self):
        """Test paginated entries have required fields"""
        data = get_all_strongs("greek", page=1, per_page=1)
        entry = data["entries"][0]
        assert "strongs" in entry
        assert "language" in entry
        assert "word" in entry
        assert "transliteration" in entry
        assert "definition" in entry


class TestStrongsWebRoutes:
    """Tests for Strong's web routes"""

    def test_strongs_index_page(self, client):
        """Test Strong's index page loads"""
        response = client.get("/strongs")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Strong" in content

    def test_strongs_search_page(self, client):
        """Test Strong's search with query"""
        response = client.get("/strongs?q=love")
        assert response.status_code == 200
        content = response.content.decode()
        assert "love" in content.lower()

    def test_strongs_entry_page_greek(self, client):
        """Test Greek Strong's entry page"""
        response = client.get("/strongs/G26")
        assert response.status_code == 200
        content = response.content.decode()
        assert "G26" in content
        assert "Greek" in content

    def test_strongs_entry_page_hebrew(self, client):
        """Test Hebrew Strong's entry page"""
        response = client.get("/strongs/H430")
        assert response.status_code == 200
        content = response.content.decode()
        assert "H430" in content
        assert "Hebrew" in content

    def test_strongs_entry_case_insensitive(self, client):
        """Test entry page handles lowercase"""
        response = client.get("/strongs/g26")
        assert response.status_code == 200

    def test_strongs_invalid_entry(self, client):
        """Test invalid entry returns 404"""
        response = client.get("/strongs/X9999")
        assert response.status_code == 404

    def test_strongs_hebrew_index(self, client):
        """Test Hebrew index page"""
        response = client.get("/strongs/hebrew")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Hebrew" in content
        assert "H1" in content

    def test_strongs_greek_index(self, client):
        """Test Greek index page"""
        response = client.get("/strongs/greek")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Greek" in content
        assert "G1" in content

    def test_strongs_hebrew_pagination(self, client):
        """Test Hebrew index pagination"""
        response = client.get("/strongs/hebrew?page=2")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Page 2" in content

    def test_strongs_greek_pagination(self, client):
        """Test Greek index pagination"""
        response = client.get("/strongs/greek?page=2")
        assert response.status_code == 200

    def test_strongs_entry_has_verse_occurrences(self, client):
        """Test entry page shows verse occurrences"""
        # Use a common word that should have occurrences
        response = client.get("/strongs/G2316")  # theos (God)
        assert response.status_code == 200
        content = response.content.decode()
        # Should have occurrences section if interlinear data exists
        assert "Occurrence" in content or "verse" in content.lower()


class TestStrongsAPIRoutes:
    """Tests for Strong's API endpoints"""

    def test_api_strongs_entry(self, client):
        """Test API Strong's entry endpoint"""
        response = client.get("/api/strongs/G26")
        assert response.status_code == 200
        data = response.json()
        assert data["strongs"] == "G26"
        assert data["language"] == "Greek"

    def test_api_strongs_hebrew_entry(self, client):
        """Test API Hebrew Strong's entry"""
        response = client.get("/api/strongs/H430")
        assert response.status_code == 200
        data = response.json()
        assert data["strongs"] == "H430"
        assert data["language"] == "Hebrew"

    def test_api_strongs_invalid(self, client):
        """Test API invalid Strong's number"""
        response = client.get("/api/strongs/X9999")
        assert response.status_code == 404

    def test_api_strongs_search(self, client):
        """Test API Strong's search endpoint"""
        response = client.get("/api/strongs?q=love")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0


class TestStrongsEdgeCases:
    """Edge case tests for Strong's functionality"""

    def test_first_hebrew_entry(self, client):
        """Test first Hebrew entry (H1)"""
        response = client.get("/strongs/H1")
        assert response.status_code == 200

    def test_last_hebrew_entry(self, client):
        """Test last Hebrew entry (H8674)"""
        response = client.get("/strongs/H8674")
        assert response.status_code == 200

    def test_first_greek_entry(self, client):
        """Test first Greek entry (G1)"""
        response = client.get("/strongs/G1")
        assert response.status_code == 200

    def test_last_greek_entry(self, client):
        """Test last Greek entry (G5624)"""
        response = client.get("/strongs/G5624")
        assert response.status_code == 200

    def test_hebrew_boundary_plus_one(self, client):
        """Test beyond Hebrew range returns 404"""
        response = client.get("/strongs/H9999")
        assert response.status_code == 404

    def test_greek_boundary_plus_one(self, client):
        """Test beyond Greek range returns 404"""
        response = client.get("/strongs/G9999")
        assert response.status_code == 404

    def test_common_hebrew_words(self, client):
        """Test common Hebrew Strong's numbers"""
        common = ["H430", "H3068", "H1", "H7965", "H2617"]
        for num in common:
            response = client.get(f"/strongs/{num}")
            assert response.status_code == 200, f"Failed for {num}"

    def test_common_greek_words(self, client):
        """Test common Greek Strong's numbers"""
        common = ["G26", "G2316", "G3056", "G4102", "G5485"]
        for num in common:
            response = client.get(f"/strongs/{num}")
            assert response.status_code == 200, f"Failed for {num}"

    def test_strongs_with_derivation_links(self, client):
        """Test entry with derivation containing Strong's references"""
        # H1580 has derivation with references to other Strong's numbers
        response = client.get("/strongs/H1580")
        assert response.status_code == 200
        content = response.content.decode()
        # Should have linked Strong's references in derivation
        assert "/strongs/H" in content or "derivation" in content.lower()


class TestStrongsIntegration:
    """Integration tests for Strong's functionality"""

    def test_search_then_view_entry(self, client):
        """Test searching and then viewing an entry"""
        # Search for love
        search_response = client.get("/strongs?q=love")
        assert search_response.status_code == 200

        # View G26 (agape)
        entry_response = client.get("/strongs/G26")
        assert entry_response.status_code == 200
        content = entry_response.content.decode()
        assert "love" in content.lower()

    def test_browse_hebrew_then_entry(self, client):
        """Test browsing Hebrew index then viewing entry"""
        # Browse Hebrew
        index_response = client.get("/strongs/hebrew")
        assert index_response.status_code == 200

        # View first entry
        entry_response = client.get("/strongs/H1")
        assert entry_response.status_code == 200

    def test_navigate_between_entries(self, client):
        """Test navigation between Strong's entries"""
        response = client.get("/strongs/H100")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have navigation to adjacent entries
        assert "H99" in content or "H101" in content

    def test_strongs_page_has_breadcrumbs(self, client):
        """Test Strong's pages have breadcrumb navigation"""
        response = client.get("/strongs/G26")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have link back to Strong's index
        assert "/strongs" in content
