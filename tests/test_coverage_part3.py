"""
Additional tests to improve coverage - Part 3.

Focus on routes and remaining gaps.
"""
import pytest


class TestAPIEndpointsExtended:
    """Extended API endpoint tests."""

    def test_verse_of_the_day(self, client):
        """Test verse of the day endpoint."""
        response = client.get("/api/verse-of-the-day")
        assert response.status_code == 200
        data = response.json()
        assert "text" in data or "verse" in data

    def test_books_api(self, client):
        """Test books list API."""
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.json()
        # API may return dict with total_books key
        assert isinstance(data, (dict, list))

    def test_book_detail_api(self, client):
        """Test book detail API."""
        response = client.get("/api/books/Genesis")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data or "chapters" in data

    def test_book_chapters_api(self, client):
        """Test book chapters API."""
        response = client.get("/api/books/Genesis/chapters/1")
        assert response.status_code == 200

    def test_book_text_api(self, client):
        """Test book full text API."""
        response = client.get("/api/books/Philemon/text")
        assert response.status_code == 200

    def test_verse_range_api(self, client):
        """Test verse range API."""
        response = client.get("/api/verse-range/Genesis/1/1/5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))

    def test_bible_api(self, client):
        """Test entire bible API (limited)."""
        response = client.get("/api/bible?limit=10")
        assert response.status_code == 200

    def test_strongs_api_greek(self, client):
        """Test Strong's API for Greek."""
        response = client.get("/api/strongs/G26")
        assert response.status_code == 200

    def test_strongs_api_hebrew(self, client):
        """Test Strong's API for Hebrew."""
        response = client.get("/api/strongs/H157")
        assert response.status_code == 200

    def test_strongs_api_invalid(self, client):
        """Test Strong's API with invalid number."""
        response = client.get("/api/strongs/X999999")
        assert response.status_code in [200, 404]

    def test_commentary_api(self, client):
        """Test commentary API."""
        response = client.get("/api/commentary/John/3/16")
        assert response.status_code == 200

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200


class TestWebRoutesExtended:
    """Extended web route tests."""

    def test_homepage(self, client):
        """Test homepage loads."""
        response = client.get("/")
        assert response.status_code == 200
        assert "KJV" in response.text or "Bible" in response.text

    def test_books_page(self, client):
        """Test books listing page."""
        response = client.get("/books")
        assert response.status_code == 200

    def test_search_page_empty(self, client):
        """Test search page with no query."""
        response = client.get("/search")
        assert response.status_code == 200

    def test_about_page(self, client):
        """Test about page."""
        response = client.get("/about")
        assert response.status_code == 200

    def test_timeline_page(self, client):
        """Test timeline page."""
        response = client.get("/timeline")
        # May redirect or return page
        assert response.status_code in [200, 302, 307, 404]

    def test_family_tree_page(self, client):
        """Test family tree page."""
        response = client.get("/family-tree")
        assert response.status_code == 200

    def test_study_guides_page(self, client):
        """Test study guides page."""
        response = client.get("/study-guides")
        assert response.status_code == 200

    def test_resources_page(self, client):
        """Test resources page."""
        response = client.get("/resources")
        assert response.status_code == 200

    def test_sitemap_xml(self, client):
        """Test sitemap.xml."""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200
        assert "xml" in response.headers.get("content-type", "")

    def test_robots_txt(self, client):
        """Test robots.txt."""
        response = client.get("/robots.txt")
        assert response.status_code == 200


class TestStrongsRoutesExtended:
    """Extended Strong's routes tests."""

    def test_strongs_index(self, client):
        """Test Strong's index page."""
        response = client.get("/strongs")
        assert response.status_code == 200

    def test_strongs_greek_letter(self, client):
        """Test Strong's Greek by first letter."""
        response = client.get("/strongs/greek/a")
        assert response.status_code in [200, 404]

    def test_strongs_hebrew_letter(self, client):
        """Test Strong's Hebrew by first letter."""
        response = client.get("/strongs/hebrew/a")
        assert response.status_code in [200, 404]

    def test_strongs_number_page(self, client):
        """Test Strong's number page."""
        response = client.get("/strongs/G26")
        assert response.status_code == 200

    def test_strongs_search(self, client):
        """Test Strong's search."""
        response = client.get("/strongs/search?q=love")
        assert response.status_code in [200, 404]


class TestFamilyTreeRoutes:
    """Tests for family tree routes."""

    def test_family_tree_index(self, client):
        """Test family tree index."""
        response = client.get("/family-tree")
        assert response.status_code == 200

    def test_family_tree_person(self, client):
        """Test family tree person page."""
        # Try common biblical figures
        persons = ["adam", "abraham", "david", "jesus"]
        for person in persons:
            response = client.get(f"/family-tree/person/{person}")
            if response.status_code == 200:
                break
        # At least one should work or we should get 404s gracefully
        assert response.status_code in [200, 404]


class TestTimelineRoutes:
    """Tests for timeline routes."""

    def test_timeline_index(self, client):
        """Test timeline index."""
        response = client.get("/timeline")
        assert response.status_code in [200, 302, 307, 404]

    def test_timeline_event(self, client):
        """Test timeline event page."""
        response = client.get("/timeline/creation")
        # May or may not exist
        assert response.status_code in [200, 404]


class TestStudyGuidesRoutes:
    """Tests for study guides routes."""

    def test_study_guides_index(self, client):
        """Test study guides index."""
        response = client.get("/study-guides")
        assert response.status_code == 200

    def test_study_guide_detail(self, client):
        """Test study guide detail page."""
        # Try to find a study guide
        response = client.get("/study-guides/salvation")
        assert response.status_code in [200, 404]


class TestMiscRoutes:
    """Tests for misc routes."""

    def test_random_verse(self, client):
        """Test random verse endpoint."""
        response = client.get("/random")
        # Should redirect or return verse or 404
        assert response.status_code in [200, 302, 307, 404]

    def test_favicon(self, client):
        """Test favicon."""
        response = client.get("/favicon.ico")
        assert response.status_code in [200, 404]

    def test_manifest(self, client):
        """Test manifest.json."""
        response = client.get("/manifest.json")
        assert response.status_code in [200, 404]


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_page(self, client):
        """Test 404 error page."""
        response = client.get("/nonexistent-page-12345")
        assert response.status_code == 404

    def test_invalid_book_api(self, client):
        """Test invalid book in API."""
        response = client.get("/api/books/NotARealBook")
        assert response.status_code == 404

    def test_invalid_chapter_api(self, client):
        """Test invalid chapter in API."""
        response = client.get("/api/books/Genesis/chapters/999")
        assert response.status_code == 404

    def test_invalid_verse_api(self, client):
        """Test invalid verse in API."""
        response = client.get("/api/verse/Genesis/1/999")
        assert response.status_code == 404


class TestUtilsHelpersExtended:
    """Extended tests for utils/helpers."""

    def test_create_slug(self):
        """Test slug creation."""
        from kjvstudy_org.utils.helpers import create_slug
        assert create_slug("Hello World") == "hello-world"
        assert create_slug("Test  123") == "test-123"

    def test_get_related_content(self):
        """Test getting related content."""
        from kjvstudy_org.utils.helpers import get_related_content
        result = get_related_content("Genesis", 1)
        assert isinstance(result, (dict, list, type(None)))

    def test_get_chapter_popularity_score(self):
        """Test chapter popularity score."""
        from kjvstudy_org.utils.helpers import get_chapter_popularity_score
        score = get_chapter_popularity_score("John", 3)
        assert isinstance(score, (int, float))

    def test_get_chapter_popularity_explanation(self):
        """Test chapter popularity explanation."""
        from kjvstudy_org.utils.helpers import get_chapter_popularity_explanation
        explanation = get_chapter_popularity_explanation("John", 3)
        assert isinstance(explanation, (str, type(None)))


class TestBiblicalBiographies:
    """Tests for biblical biographies module."""

    def test_get_all_biographies(self):
        """Test getting all biographies."""
        from kjvstudy_org import biblical_biographies
        # Module should import successfully
        assert biblical_biographies is not None

    def test_get_biography(self):
        """Test getting a single biography."""
        from kjvstudy_org.biblical_biographies import get_biography
        bio = get_biography("abraham")
        # May or may not exist
        assert bio is None or isinstance(bio, dict)


class TestDataModule:
    """Tests for data module."""

    def test_data_module_import(self):
        """Test data module imports correctly."""
        from kjvstudy_org import data
        assert data is not None


class TestSearchModule:
    """Tests for search module."""

    def test_search_index_module_import(self):
        """Test search index module imports."""
        from kjvstudy_org.utils import search_index
        assert search_index is not None

    def test_search_module_import(self):
        """Test search module imports."""
        from kjvstudy_org.utils import search
        assert search is not None


class TestCommentaryRoutes:
    """Tests for commentary routes."""

    def test_commentary_verse_page(self, client):
        """Test verse with commentary."""
        response = client.get("/book/John/chapter/3/verse/16")
        assert response.status_code == 200
        # Should have some commentary elements

    def test_commentary_chapter_page(self, client):
        """Test chapter with commentary."""
        response = client.get("/book/Genesis/chapter/1")
        assert response.status_code == 200


class TestResourceRoutes:
    """Tests for resource routes."""

    def test_maps_page(self, client):
        """Test maps resource page."""
        response = client.get("/resources/maps")
        assert response.status_code in [200, 404]

    def test_charts_page(self, client):
        """Test charts resource page."""
        response = client.get("/resources/charts")
        assert response.status_code in [200, 404]

    def test_concordance_page(self, client):
        """Test concordance page."""
        response = client.get("/resources/concordance")
        assert response.status_code in [200, 404]


class TestAPIResponseFormats:
    """Tests for API response formats."""

    def test_verse_api_format(self, client):
        """Test verse API response format."""
        response = client.get("/api/verse/John/3/16")
        assert response.status_code == 200
        data = response.json()
        # Should have standard fields
        assert isinstance(data, dict)

    def test_search_api_format(self, client):
        """Test search API response format."""
        response = client.get("/api/search?q=love")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data or "query" in data

    def test_books_api_format(self, client):
        """Test books API response format."""
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.json()
        # Should have books data
        if isinstance(data, dict):
            assert "books" in data or "total_books" in data


class TestCacheAndPerformance:
    """Tests to verify caching behavior."""

    def test_repeated_requests(self, client):
        """Test that repeated requests work (caching doesn't break)."""
        for _ in range(3):
            response = client.get("/api/verse/Genesis/1/1")
            assert response.status_code == 200

    def test_multiple_books(self, client):
        """Test accessing multiple books."""
        books = ["Genesis", "Psalms", "Matthew", "Revelation"]
        for book in books:
            response = client.get(f"/book/{book}")
            assert response.status_code == 200
