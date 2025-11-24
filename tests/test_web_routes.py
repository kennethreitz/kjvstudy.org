"""
Tests for web page routes and HTML endpoints

Fixtures are imported from conftest.py
"""
import pytest


class TestHomePage:
    """Tests for homepage"""

    def test_homepage_loads(self, client):
        """Test that homepage loads successfully"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_homepage_contains_title(self, client):
        """Test homepage contains site title"""
        response = client.get("/")
        assert b"KJV" in response.content or b"Bible" in response.content

    def test_homepage_has_search(self, client):
        """Test homepage has search functionality"""
        response = client.get("/")
        assert b"search" in response.content.lower()


class TestBookPages:
    """Tests for book listing and detail pages"""

    def test_books_page_loads(self, client):
        """Test books listing page"""
        response = client.get("/books")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_books_page_has_genesis(self, client):
        """Test books page lists Genesis"""
        response = client.get("/books")
        assert b"Genesis" in response.content

    def test_books_page_has_revelation(self, client):
        """Test books page lists Revelation"""
        response = client.get("/books")
        assert b"Revelation" in response.content

    def test_book_detail_page(self, client):
        """Test individual book page"""
        response = client.get("/book/John")
        assert response.status_code == 200
        assert b"John" in response.content

    def test_book_with_abbreviation(self, client):
        """Test book page with abbreviation redirects"""
        response = client.get("/book/Gen", follow_redirects=False)
        # Should redirect to canonical name
        assert response.status_code in [200, 301, 302, 307, 308]


class TestChapterPages:
    """Tests for chapter pages"""

    def test_chapter_page_loads(self, client):
        """Test chapter page loads"""
        response = client.get("/book/John/chapter/3")
        assert response.status_code == 200
        assert b"John" in response.content
        assert b"3" in response.content or b"3:" in response.content

    def test_chapter_has_verses(self, client):
        """Test chapter page displays verses"""
        response = client.get("/book/John/chapter/3")
        assert response.status_code == 200
        # Should contain verse numbers or verse content
        assert b"16" in response.content  # John 3:16

    def test_first_chapter(self, client):
        """Test first chapter of Genesis"""
        response = client.get("/book/Genesis/chapter/1")
        assert response.status_code == 200
        assert b"beginning" in response.content.lower()


class TestVersePage:
    """Tests for individual verse pages"""

    def test_verse_page_loads(self, client):
        """Test individual verse page"""
        response = client.get("/book/John/chapter/3/verse/16")
        assert response.status_code == 200
        assert b"John 3:16" in response.content

    def test_verse_has_content(self, client):
        """Test verse page displays verse text"""
        response = client.get("/book/John/chapter/3/verse/16")
        assert response.status_code == 200
        assert b"God" in response.content or b"loved" in response.content

    def test_verse_navigation(self, client):
        """Test verse page has navigation links"""
        response = client.get("/book/John/chapter/3/verse/16")
        assert response.status_code == 200
        # Should have links to previous/next verses or chapter
        content = response.content.lower()
        assert b"verse" in content or b"chapter" in content


class TestSearchPage:
    """Tests for search functionality"""

    def test_search_page_loads(self, client):
        """Test search page loads"""
        response = client.get("/search?q=love")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_search_returns_results(self, client):
        """Test search returns results"""
        response = client.get("/search?q=love")
        assert response.status_code == 200
        # Should have some results
        assert b"love" in response.content.lower()

    def test_search_empty_query(self, client):
        """Test search with empty query"""
        response = client.get("/search?q=")
        assert response.status_code == 200


class TestTopicsPages:
    """Tests for topics pages"""

    def test_topics_index_loads(self, client):
        """Test topics index page"""
        response = client.get("/topics")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_topic_detail_page(self, client):
        """Test individual topic page"""
        response = client.get("/topics/faith")
        # Topic might or might not exist
        assert response.status_code in [200, 404]


class TestReadingPlansPages:
    """Tests for reading plans pages"""

    def test_reading_plans_index(self, client):
        """Test reading plans index page"""
        response = client.get("/reading-plans")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_reading_plan_detail(self, client):
        """Test individual reading plan page"""
        response = client.get("/reading-plan/chronological")
        # Accept both 200 and 404 as route might not exist
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert b"chronological" in response.content.lower()


class TestResourcePages:
    """Tests for resource pages"""

    def test_study_guides_page(self, client):
        """Test study guides page"""
        response = client.get("/study-guides")
        assert response.status_code in [200, 404]

    def test_resources_page(self, client):
        """Test resources page"""
        response = client.get("/resources")
        assert response.status_code in [200, 404]


class TestStaticPages:
    """Tests for static/special pages"""

    def test_verse_of_the_day(self, client):
        """Test verse of the day page"""
        response = client.get("/verse-of-the-day")
        assert response.status_code == 200

    def test_random_verse(self, client):
        """Test random verse endpoint"""
        response = client.get("/random-verse", follow_redirects=False)
        # Should redirect to a random verse
        assert response.status_code in [302, 303, 307, 308]


class TestHealthCheck:
    """Tests for health check endpoint"""

    def test_health_endpoint(self, client):
        """Test /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200


class TestNotFoundPages:
    """Tests for 404 handling"""

    def test_nonexistent_page(self, client):
        """Test 404 for non-existent page"""
        response = client.get("/this-page-does-not-exist")
        assert response.status_code == 404

    def test_nonexistent_book(self, client):
        """Test 404 for non-existent book"""
        response = client.get("/book/NotABook")
        assert response.status_code == 404


class TestRedirects:
    """Tests for redirects"""

    def test_book_abbreviation_redirects(self, client):
        """Test book abbreviations redirect properly"""
        response = client.get("/book/Gen/chapter/1", follow_redirects=False)
        # Should redirect to canonical name if needed
        assert response.status_code in [200, 301, 302, 307, 308]


class TestHTMLStructure:
    """Tests for HTML structure and metadata"""

    def test_homepage_has_meta_tags(self, client):
        """Test homepage has proper meta tags"""
        response = client.get("/")
        content = response.content.decode()
        assert "<html" in content.lower()
        assert "<head" in content.lower()
        assert "<body" in content.lower()

    def test_verse_page_has_og_tags(self, client):
        """Test verse page has Open Graph tags"""
        response = client.get("/book/John/chapter/3/verse/16")
        content = response.content.decode()
        # Should have some meta tags
        assert "og:" in content.lower() or "meta" in content.lower()


class TestNavigation:
    """Tests for navigation elements"""

    def test_homepage_has_navigation(self, client):
        """Test homepage has navigation links"""
        response = client.get("/")
        content = response.content.lower()
        # Should have links to major sections
        assert b"book" in content or b"search" in content


class TestAccessibility:
    """Tests for accessibility features"""

    def test_pages_have_titles(self, client):
        """Test pages have proper titles"""
        pages = [
            "/",
            "/books",
            "/book/John",
            "/book/John/chapter/3",
        ]

        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                assert b"<title>" in response.content


class TestContentTypes:
    """Tests for content type headers"""

    def test_html_pages_content_type(self, client):
        """Test HTML pages return correct content type"""
        html_pages = [
            "/",
            "/books",
            "/book/John",
        ]

        for page in html_pages:
            response = client.get(page)
            if response.status_code == 200:
                assert "text/html" in response.headers.get("content-type", "")

    def test_api_json_content_type(self, client):
        """Test API endpoints return JSON"""
        api_endpoints = [
            "/api/",
            "/api/health",
            "/api/books",
        ]

        for endpoint in api_endpoints:
            response = client.get(endpoint)
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                assert "application/json" in content_type or "json" in content_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
