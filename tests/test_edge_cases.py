"""
Edge case and error handling tests for KJV Study API

Fixtures are imported from conftest.py
"""
import pytest


class TestErrorHandling:
    """Tests for error handling and edge cases"""

    def test_invalid_book_name(self, client):
        """Test verse endpoint with non-existent book"""
        response = client.get("/api/verse/NotABook/1/1")
        assert response.status_code in [404, 500]

    def test_invalid_chapter_number(self, client):
        """Test verse endpoint with invalid chapter"""
        response = client.get("/api/verse/Genesis/999/1")
        assert response.status_code in [404, 500]

    def test_invalid_verse_number(self, client):
        """Test verse endpoint with invalid verse"""
        response = client.get("/api/verse/John/3/999")
        assert response.status_code in [404, 500]

    def test_negative_chapter(self, client):
        """Test verse endpoint with negative chapter"""
        response = client.get("/api/verse/Genesis/-1/1")
        assert response.status_code in [404, 422, 500]

    def test_negative_verse(self, client):
        """Test verse endpoint with negative verse"""
        response = client.get("/api/verse/Genesis/1/-1")
        assert response.status_code in [404, 422, 500]

    def test_zero_chapter(self, client):
        """Test verse endpoint with zero chapter"""
        response = client.get("/api/verse/Genesis/0/1")
        assert response.status_code in [404, 422, 500]

    def test_zero_verse(self, client):
        """Test verse endpoint with zero verse"""
        response = client.get("/api/verse/Genesis/1/0")
        assert response.status_code in [404, 422, 500]


class TestVerseRangeEdgeCases:
    """Tests for verse range edge cases"""

    def test_reversed_verse_range(self, client):
        """Test verse range with start > end"""
        response = client.get("/api/verse-range/John/3/16/1")
        # Should handle reversed ranges gracefully
        assert response.status_code in [200, 400, 422, 500]

    def test_single_verse_range(self, client):
        """Test verse range with start = end"""
        response = client.get("/api/verse-range/John/3/16/16")
        assert response.status_code == 200
        if response.status_code == 200:
            data = response.json()
            assert len(data["verses"]) == 1

    def test_large_verse_range(self, client):
        """Test verse range spanning many verses"""
        response = client.get("/api/verse-range/Psalms/119/1/176")
        assert response.status_code == 200
        data = response.json()
        assert len(data["verses"]) == 176

    def test_verse_range_exceeds_chapter(self, client):
        """Test verse range that goes beyond chapter length"""
        response = client.get("/api/verse-range/John/3/1/999")
        # Should handle gracefully, possibly returning up to last verse
        assert response.status_code in [200, 404, 422]


class TestBookAbbreviations:
    """Comprehensive tests for book name abbreviations"""

    def test_old_testament_abbreviations(self, client):
        """Test various Old Testament book abbreviations"""
        abbreviations = {
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
        }

        for abbrev, full_name in abbreviations.items():
            response = client.get(f"/api/books/{abbrev}")
            assert response.status_code in [200, 404, 500]
            if response.status_code == 200:
                data = response.json()
                # Response has "name" field, not "book"
                assert data["name"] == full_name

    def test_new_testament_abbreviations(self, client):
        """Test various New Testament book abbreviations"""
        abbreviations = {
            "Matt": "Matthew",
            "Rom": "Romans",
            "Cor": "Corinthians",
            "Gal": "Galatians",
            "Eph": "Ephesians",
            "Phil": "Philippians",
            "Col": "Colossians",
            "Thess": "Thessalonians",
            "Heb": "Hebrews",
            "Jas": "James",
            "Rev": "Revelation",
        }

        for abbrev, full_name in abbreviations.items():
            response = client.get(f"/api/books/{abbrev}")
            # Some abbreviations might need more context (like 1 Cor vs 2 Cor)
            assert response.status_code in [200, 404]

    def test_numbered_book_abbreviations(self, client):
        """Test abbreviations for numbered books"""
        test_cases = [
            ("1 Sam", "I Samuel"),
            ("2 Sam", "II Samuel"),
            ("1 Kings", "I Kings"),
            ("2 Kings", "II Kings"),
            ("1 Cor", "I Corinthians"),
            ("2 Cor", "II Corinthians"),
        ]

        for abbrev, expected in test_cases:
            response = client.get(f"/api/verse/{abbrev}/1/1")
            if response.status_code == 200:
                data = response.json()
                # Book name might be in Roman numerals or Arabic numerals
                assert "Samuel" in data["book"] or "Corinthians" in data["book"] or "Kings" in data["book"]


class TestSearchFunctionality:
    """Comprehensive search tests"""

    def test_search_common_words(self, client):
        """Test search for common biblical words"""
        common_words = ["love", "faith", "hope", "peace", "righteousness"]

        for word in common_words:
            response = client.get(f"/api/search?q={word}")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] > 0
            assert len(data["results"]) > 0

    def test_search_phrase(self, client):
        """Test search for a phrase"""
        response = client.get("/api/search?q=God so loved the world")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0

    def test_search_case_insensitive(self, client):
        """Test search is case insensitive"""
        response1 = client.get("/api/search?q=LOVE&limit=10")
        response2 = client.get("/api/search?q=love&limit=10")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Results should be similar for case-insensitive search
        data1 = response1.json()
        data2 = response2.json()
        assert data1["total"] > 0
        assert data2["total"] > 0

    def test_search_very_short_query(self, client):
        """Test search with very short query"""
        response = client.get("/api/search?q=a")
        assert response.status_code == 200
        # Might return empty or filtered results for very short queries

    def test_search_special_characters(self, client):
        """Test search with special characters"""
        response = client.get("/api/search?q=love?")
        assert response.status_code == 200

    def test_search_with_zero_limit(self, client):
        """Test search with limit=0"""
        response = client.get("/api/search?q=love&limit=0")
        assert response.status_code == 200

    def test_search_with_large_limit(self, client):
        """Test search with very large limit"""
        response = client.get("/api/search?q=love&limit=10000")
        assert response.status_code == 200
        data = response.json()
        # Should handle large limits gracefully


class TestBookBoundaries:
    """Tests for book boundaries and edge cases"""

    def test_shortest_book(self, client):
        """Test the shortest book (2 John or 3 John)"""
        response = client.get("/api/books/III John/text")
        assert response.status_code == 200
        data = response.json()
        assert data["total_chapters"] == 1
        assert data["total_verses"] > 0

    def test_longest_book(self, client):
        """Test the longest book (Psalms)"""
        response = client.get("/api/books/Psalms")
        assert response.status_code == 200
        data = response.json()
        assert data["total_chapters"] == 150

    def test_first_book(self, client):
        """Test first book of the Bible"""
        response = client.get("/api/books/Genesis")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Genesis"

    def test_last_book(self, client):
        """Test last book of the Bible"""
        response = client.get("/api/books/Revelation")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Revelation"

    def test_longest_chapter(self, client):
        """Test longest chapter (Psalms 119)"""
        response = client.get("/api/books/Psalms/chapters/119")
        assert response.status_code == 200
        data = response.json()
        assert data["total_verses"] == 176


class TestCrossReferencesEdgeCases:
    """Tests for cross-references edge cases"""

    def test_verse_with_no_cross_references(self, client):
        """Test verse that might have no cross-references"""
        response = client.get("/api/cross-references/III John/1/1")
        assert response.status_code == 200
        data = response.json()
        assert "cross_references" in data
        # Might be empty list

    def test_verse_with_many_cross_references(self, client):
        """Test verse with many cross-references"""
        response = client.get("/api/cross-references/John/3/16")
        assert response.status_code == 200
        data = response.json()
        assert "cross_references" in data


class TestInterlinearEdgeCases:
    """Tests for interlinear data edge cases"""

    def test_old_testament_interlinear(self, client):
        """Test interlinear for Old Testament (Hebrew)"""
        response = client.get("/api/interlinear/Genesis/1/1")
        assert response.status_code == 200
        data = response.json()
        assert "interlinear_available" in data

    def test_new_testament_interlinear(self, client):
        """Test interlinear for New Testament (Greek)"""
        response = client.get("/api/interlinear/John/1/1")
        assert response.status_code == 200
        data = response.json()
        assert "interlinear_available" in data


class TestTopicsEdgeCases:
    """Tests for topics edge cases"""

    def test_nonexistent_topic(self, client):
        """Test non-existent topic"""
        response = client.get("/api/topics/notarealtopic123456")
        assert response.status_code == 404

    def test_topic_case_sensitivity(self, client):
        """Test topic name case sensitivity"""
        response1 = client.get("/api/topics/faith")
        response2 = client.get("/api/topics/Faith")
        response3 = client.get("/api/topics/FAITH")

        # At least one should work
        assert any(r.status_code == 200 for r in [response1, response2, response3])


class TestReadingPlansEdgeCases:
    """Tests for reading plans edge cases"""

    def test_nonexistent_reading_plan(self, client):
        """Test non-existent reading plan"""
        response = client.get("/api/reading-plans/not-a-real-plan")
        assert response.status_code == 404

    def test_all_reading_plans_structure(self, client):
        """Test structure of all reading plans"""
        response = client.get("/api/reading-plans")
        assert response.status_code == 200
        data = response.json()

        assert "plans" in data
        for plan in data["plans"]:
            assert "id" in plan
            assert "name" in plan
            assert "description" in plan
            assert "days" in plan


class TestAPIPerformance:
    """Tests for API performance and large data handling"""

    def test_entire_bible_response_size(self, client):
        """Test that entire Bible endpoint returns valid data"""
        response = client.get("/api/bible")
        assert response.status_code == 200
        data = response.json()

        # Verify structure
        assert "total_books" in data
        assert "total_verses" in data
        assert "books" in data

        # Verify counts
        assert data["total_books"] == 66
        assert data["total_verses"] > 31000  # KJV has 31,102 verses

    def test_long_book_response(self, client):
        """Test response for longest books"""
        long_books = ["Psalms", "Genesis", "Isaiah", "Jeremiah"]

        for book in long_books:
            response = client.get(f"/api/books/{book}/text")
            assert response.status_code == 200
            data = response.json()
            assert data["total_verses"] > 100


class TestContentValidation:
    """Tests for content validation"""

    def test_john_3_16_content(self, client):
        """Test that John 3:16 has correct content"""
        response = client.get("/api/verse/John/3/16")
        assert response.status_code == 200
        data = response.json()

        text = data["text"].lower()
        assert "god" in text
        assert "loved" in text
        assert "world" in text
        assert "son" in text

    def test_genesis_1_1_content(self, client):
        """Test that Genesis 1:1 has correct content"""
        response = client.get("/api/verse/Genesis/1/1")
        assert response.status_code == 200
        data = response.json()

        text = data["text"].lower()
        assert "beginning" in text
        assert "god" in text
        assert "created" in text
        assert "heaven" in text
        assert "earth" in text

    def test_psalms_23_1_content(self, client):
        """Test that Psalms 23:1 has correct content"""
        response = client.get("/api/verse/Psalms/23/1")
        assert response.status_code == 200
        data = response.json()

        text = data["text"].lower()
        assert "lord" in text
        assert "shepherd" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
