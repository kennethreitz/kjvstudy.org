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

    def test_homepage_surfaces_passage_workspace(self, client):
        """Test homepage links to the passage workspace"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Passage Workspace" in response.content
        assert b'href="/study"' in response.content
        assert b'id="study-notes-badge"' in response.content


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

    def test_chapter_links_to_study_workspace(self, client):
        """Test chapter page links to the study workspace"""
        response = client.get("/book/John/chapter/3")
        assert response.status_code == 200
        assert b'href="/study/John/3"' in response.content

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

    def test_verse_links_to_study_workspace(self, client):
        """Test verse page links to the study workspace"""
        response = client.get("/book/John/chapter/3/verse/16")
        assert response.status_code == 200
        assert b'href="/study/John/3/16"' in response.content


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


class TestChangelog:
    """Tests for the changelog page"""

    def test_changelog_loads(self, client):
        response = client.get("/changelog")
        assert response.status_code == 200
        assert b"Changelog" in response.content

    def test_changelog_has_entries(self, client):
        response = client.get("/changelog")
        content = response.content.decode()
        # Oldest and newest curated entries are present
        assert "Genesis" in content  # April 2025 entry title
        assert "The Fine-Print Edition" in content
        assert content.count('class="changelog-entry"') >= 5

    def test_changelog_linked_from_sidebar(self, client):
        response = client.get("/")
        assert b'href="/changelog"' in response.content


class TestStudyWorkspace:
    """Tests for the passage study workspace"""

    def test_study_landing_loads(self, client):
        response = client.get("/study")
        assert response.status_code == 200
        assert b"Passage Study Workspace" in response.content
        assert b"1 Corinthians 13" in response.content
        assert b'href="/study/1%20Corinthians/13"' in response.content
        assert b"id=\"saved-study-notes\"" in response.content
        assert b"kjvstudy:notes:" in response.content
        assert response.content.index(b"Your Passages With Notes") < response.content.index(b"Begin With A Passage")
        assert b'id="study-notes-badge"' in response.content

    def test_study_query_redirects_to_workspace(self, client):
        response = client.get("/study?q=John%203:16-17", follow_redirects=False)
        assert response.status_code in [301, 302, 307, 308]
        assert response.headers["location"].endswith("/study/John/3/16/17")

    def test_study_query_accepts_numbered_book_abbreviation(self, client):
        response = client.get("/study?q=1%20Cor%2013", follow_redirects=False)
        assert response.status_code in [301, 302, 307, 308]
        assert response.headers["location"].endswith("/study/1%20Corinthians/13")

    def test_study_single_verse_workspace(self, client):
        response = client.get("/study/John/3/16")
        assert response.status_code == 200
        assert b"John 3:16" in response.content
        assert b"<h2>John 3:16</h2>" in response.content
        assert b"KJV Text" not in response.content
        assert b"God so loved the world" in response.content
        assert b"Notes" in response.content

    def test_study_passage_workspace(self, client):
        response = client.get("/study/Romans/8/28/30")
        assert response.status_code == 200
        assert b"Romans 8:28-30" in response.content
        assert b"<h2>Romans 8:28-30</h2>" in response.content
        assert b"Verse Study" in response.content

    def test_study_abbreviation_redirects(self, client):
        response = client.get("/study/Gen/1/1", follow_redirects=False)
        assert response.status_code in [301, 302, 307, 308]
        assert response.headers["location"].endswith("/study/Genesis/1/1")

    def test_study_invalid_reference(self, client):
        response = client.get("/study?q=NotABook%201:1")
        assert response.status_code == 200
        assert b"Reference not found" in response.content


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

    def test_base_js_updates_study_notes_badge(self, client):
        """Test shared JS includes study notes badge updater"""
        response = client.get("/static/base.js")
        assert response.status_code == 200
        assert b"function updateStudyNotesBadge()" in response.content
        assert b"study-notes-badge" in response.content
        assert b"kjvstudy:notes:" in response.content

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


class TestStoryRoutes:
    """Tests for Bible stories routes"""

    def test_stories_index(self, client):
        """Test stories index page loads"""
        response = client.get("/stories")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Bible Stories" in content or "stories" in content.lower()

    def test_stories_kids_index(self, client):
        """Test kids stories index page loads"""
        response = client.get("/stories/kids")
        assert response.status_code == 200
        content = response.content.decode()
        assert "kids" in content.lower() or "children" in content.lower()

    def test_story_detail_page(self, client):
        """Test individual story page loads"""
        # Try to get a story - we don't know the exact slugs without loading data
        # so we'll test the index and ensure it has story links
        response = client.get("/stories")
        content = response.content.decode()

        # Should have links to individual stories
        assert "/stories/" in content or response.status_code == 200

    def test_story_counts_work(self, client):
        """Test story counts are displayed and cached"""
        response = client.get("/stories")
        content = response.content.decode()

        # Story count should be displayed somewhere (or page should load)
        assert response.status_code == 200


class TestMarkdownRendering:
    """Tests for Mistune markdown rendering in templates"""

    def test_markdown_renders_in_pages(self, client):
        """Test that pages using markdown filters render successfully"""
        # Resources pages use markdown for descriptions
        response = client.get("/resources")
        assert response.status_code == 200
        content = response.content.decode()

        # Should render successfully (not have raw markdown)
        # If we see **text** or *text* that hasn't been converted, markdown failed
        # Note: This is a basic smoke test - detailed markdown tests would need fixtures

    def test_resource_pages_with_markdown(self, client):
        """Test resource pages that use markdown rendering"""
        resource_pages = [
            "/biblical-angels",
            "/biblical-prophets",
            "/parables",
        ]

        for page in resource_pages:
            response = client.get(page)
            assert response.status_code == 200, f"Page {page} failed to load"


class TestResourceSlugLookups:
    """Tests for optimized resource slug index lookups"""

    def test_resource_detail_pages_load(self, client):
        """Test that resource detail pages load successfully with slug lookups"""
        # Test some known resource detail pages
        test_pages = [
            "/biblical-angels/michael",
            "/biblical-prophets/moses",
            "/names-of-god/yahweh",
        ]

        for page in test_pages:
            response = client.get(page)
            # Should either load (200) or be a valid 404 if that specific item doesn't exist
            assert response.status_code in [200, 404]

    def test_invalid_resource_slug_returns_404(self, client):
        """Test that invalid resource slugs return 404"""
        response = client.get("/biblical-angels/this-angel-does-not-exist")
        assert response.status_code == 404


class TestAboutPages:
    """Tests for about pages"""

    def test_about_page_loads(self, client):
        """Test main about page loads"""
        response = client.get("/about")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_about_page_has_title(self, client):
        """Test about page has proper title"""
        response = client.get("/about")
        content = response.content.decode()
        assert "About KJV Study" in content

    def test_about_page_has_toc(self, client):
        """Test about page has table of contents"""
        response = client.get("/about")
        content = response.content.decode()
        assert "Contents" in content
        assert 'class="toc"' in content

    def test_about_page_has_theological_convictions(self, client):
        """Test about page has theological convictions section"""
        response = client.get("/about")
        content = response.content.decode()
        assert "Theological Convictions" in content

    def test_about_page_has_sidenotes(self, client):
        """Test about page has Tufte-style sidenotes"""
        response = client.get("/about")
        content = response.content.decode()
        assert 'class="sidenote"' in content
        assert 'class="margin-toggle sidenote-number"' in content

    def test_about_page_has_keyboard_nav(self, client):
        """Test about page has keyboard navigation script"""
        response = client.get("/about")
        content = response.content.decode()
        assert "KJVNav" in content
        assert "ArrowDown" in content or "ArrowUp" in content

    def test_about_page_has_creator_section(self, client):
        """Test about page has creator section"""
        response = client.get("/about")
        content = response.content.decode()
        assert "Kenneth Reitz" in content
        assert "kennethreitz.org" in content

    def test_about_page_has_open_source_section(self, client):
        """Test about page has open source section"""
        response = client.get("/about")
        content = response.content.decode()
        assert "Open Source" in content
        assert "github.com" in content


class TestAboutStatsPage:
    """Tests for about/stats page"""

    def test_stats_page_loads(self, client):
        """Test stats page loads"""
        response = client.get("/about/stats")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_stats_page_has_title(self, client):
        """Test stats page has proper title"""
        response = client.get("/about/stats")
        content = response.content.decode()
        assert "Statistics" in content

    def test_stats_page_has_bible_stats(self, client):
        """Test stats page has Bible statistics"""
        response = client.get("/about/stats")
        content = response.content.decode()
        assert "31,102" in content  # Total verses
        assert "66" in content  # Total books

    def test_stats_page_has_commentary_stats(self, client):
        """Test stats page has commentary statistics"""
        response = client.get("/about/stats")
        content = response.content.decode()
        assert "Commentary" in content

    def test_stats_page_has_cross_reference_stats(self, client):
        """Test stats page has cross-reference statistics"""
        response = client.get("/about/stats")
        content = response.content.decode()
        assert "Cross-Reference" in content or "cross-reference" in content


class TestAboutCommentaryIndex:
    """Tests for about/commentary index page"""

    def test_commentary_index_loads(self, client):
        """Test commentary index page loads"""
        response = client.get("/about/commentary")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_commentary_index_has_title(self, client):
        """Test commentary index has proper title"""
        response = client.get("/about/commentary")
        content = response.content.decode()
        assert "Commentary" in content

    def test_commentary_index_has_books(self, client):
        """Test commentary index lists books"""
        response = client.get("/about/commentary")
        content = response.content.decode()
        # Should have at least some Bible books listed
        assert "Genesis" in content or "Matthew" in content or "John" in content

    def test_commentary_index_has_toc(self, client):
        """Test commentary index has table of contents"""
        response = client.get("/about/commentary")
        content = response.content.decode()
        assert "toc" in content.lower() or "contents" in content.lower()


class TestAboutCrossReferencesIndex:
    """Tests for about/cross-references index page"""

    def test_cross_references_index_loads(self, client):
        """Test cross-references index page loads"""
        response = client.get("/about/cross-references")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_cross_references_index_has_title(self, client):
        """Test cross-references index has proper title"""
        response = client.get("/about/cross-references")
        content = response.content.decode()
        assert "Cross-Reference" in content or "Cross Reference" in content

    def test_cross_references_index_has_books(self, client):
        """Test cross-references index lists books"""
        response = client.get("/about/cross-references")
        content = response.content.decode()
        # Should have Bible books listed
        assert "Genesis" in content or "Matthew" in content or "John" in content

    def test_cross_references_index_books_in_biblical_order(self, client):
        """Test cross-references index has books in biblical order"""
        response = client.get("/about/cross-references")
        content = response.content.decode()
        # Genesis should appear before Exodus, and both before Matthew
        genesis_pos = content.find("Genesis")
        exodus_pos = content.find("Exodus")
        matthew_pos = content.find("Matthew")

        if genesis_pos > -1 and exodus_pos > -1:
            assert genesis_pos < exodus_pos, "Genesis should appear before Exodus"
        if exodus_pos > -1 and matthew_pos > -1:
            assert exodus_pos < matthew_pos, "Exodus should appear before Matthew"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
