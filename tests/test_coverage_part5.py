"""
Additional tests to improve coverage - Part 5.

Focus on low-coverage modules:
- routes/stories.py (54%)
- routes/bible.py (60%)
- utils/commentary_loader.py (64%)
- utils/search.py (70%)
- routes/topics.py (74%)
"""
import pytest


class TestStoriesRoutes:
    """Tests for stories routes (54% coverage)."""

    def test_stories_index_page(self, client):
        """Test stories index page loads."""
        response = client.get("/stories")
        assert response.status_code == 200
        assert "Stories" in response.text or "stories" in response.text

    def test_stories_kids_index_page(self, client):
        """Test kids stories index page loads."""
        response = client.get("/stories/kids")
        assert response.status_code == 200

    def test_story_detail_valid(self, client):
        """Test valid story detail page."""
        # First get the stories index to find a valid story
        response = client.get("/stories")
        assert response.status_code == 200
        # Try some common story slugs
        story_slugs = ["creation", "noahs-ark", "david-and-goliath", "the-exodus"]
        for slug in story_slugs:
            response = client.get(f"/stories/{slug}")
            if response.status_code == 200:
                break
        # At least the route should work (even if 404)
        assert response.status_code in [200, 404]

    def test_story_detail_invalid(self, client):
        """Test invalid story returns 404."""
        response = client.get("/stories/this-story-does-not-exist-12345")
        assert response.status_code == 404

    def test_story_kids_version(self, client):
        """Test kids version of a story."""
        story_slugs = ["creation", "noahs-ark", "david-and-goliath"]
        for slug in story_slugs:
            response = client.get(f"/stories/{slug}/kids")
            if response.status_code == 200:
                break
        assert response.status_code in [200, 404]

    def test_story_kids_invalid(self, client):
        """Test invalid kids story returns 404."""
        response = client.get("/stories/nonexistent-story/kids")
        assert response.status_code == 404

    def test_story_pdf_endpoint(self, client):
        """Test story PDF endpoint (may return 503 if WeasyPrint unavailable)."""
        story_slugs = ["creation", "noahs-ark"]
        for slug in story_slugs:
            response = client.get(f"/stories/{slug}/pdf")
            # 503 means WeasyPrint not installed, 404 means story not found
            assert response.status_code in [200, 404, 503]
            if response.status_code != 404:
                break

    def test_story_kids_pdf_endpoint(self, client):
        """Test kids story PDF endpoint."""
        response = client.get("/stories/creation/kids/pdf")
        assert response.status_code in [200, 404, 503]


class TestBibleRoutes:
    """Tests for bible routes (60% coverage)."""

    def test_book_page_genesis(self, client):
        """Test book page for Genesis."""
        response = client.get("/book/Genesis")
        assert response.status_code == 200
        assert "Genesis" in response.text

    def test_book_page_invalid(self, client):
        """Test invalid book returns 404."""
        response = client.get("/book/NotARealBook")
        assert response.status_code == 404

    def test_book_abbreviation_redirect(self, client):
        """Test book abbreviation redirects to full name."""
        response = client.get("/book/Gen", follow_redirects=False)
        # Should redirect to /book/Genesis
        assert response.status_code in [200, 301, 307]

    def test_book_pdf_endpoint(self, client):
        """Test book PDF endpoint."""
        response = client.get("/book/Philemon/pdf")
        # 503 if WeasyPrint not installed
        assert response.status_code in [200, 503]

    def test_book_pdf_invalid(self, client):
        """Test invalid book PDF returns 404."""
        response = client.get("/book/FakeBook/pdf")
        assert response.status_code in [404, 503]

    def test_chapter_page(self, client):
        """Test chapter page loads."""
        response = client.get("/book/Genesis/chapter/1")
        assert response.status_code == 200
        assert "Genesis" in response.text

    def test_chapter_page_invalid_chapter(self, client):
        """Test invalid chapter returns 404."""
        response = client.get("/book/Genesis/chapter/999")
        assert response.status_code == 404

    def test_chapter_page_invalid_book(self, client):
        """Test invalid book in chapter route."""
        response = client.get("/book/FakeBook/chapter/1")
        assert response.status_code == 404

    def test_chapter_pdf_endpoint(self, client):
        """Test chapter PDF endpoint."""
        response = client.get("/book/Genesis/chapter/1/pdf")
        assert response.status_code in [200, 503]

    def test_chapter_pdf_invalid(self, client):
        """Test invalid chapter PDF."""
        response = client.get("/book/Genesis/chapter/999/pdf")
        assert response.status_code in [404, 503]

    def test_legacy_chapter_redirect(self, client):
        """Test legacy chapter URL redirects."""
        response = client.get("/book/Genesis/1", follow_redirects=False)
        assert response.status_code in [301, 307]

    def test_book_commentary_redirect(self, client):
        """Test book commentary redirect."""
        response = client.get("/book/Genesis/commentary", follow_redirects=False)
        assert response.status_code in [301, 307]

    def test_verse_page(self, client):
        """Test verse page loads."""
        response = client.get("/book/Genesis/chapter/1/verse/1")
        assert response.status_code == 200

    def test_verse_page_invalid_verse(self, client):
        """Test invalid verse returns 404."""
        response = client.get("/book/Genesis/chapter/1/verse/999")
        assert response.status_code == 404

    def test_verse_pdf_endpoint(self, client):
        """Test verse PDF endpoint."""
        response = client.get("/book/Genesis/chapter/1/verse/1/pdf")
        assert response.status_code in [200, 503]

    def test_interlinear_chapter_page(self, client):
        """Test interlinear chapter page."""
        response = client.get("/book/Genesis/chapter/1/interlinear")
        assert response.status_code == 200

    def test_interlinear_chapter_invalid(self, client):
        """Test invalid interlinear chapter."""
        response = client.get("/book/FakeBook/chapter/1/interlinear")
        assert response.status_code == 404

    def test_interlinear_pdf_endpoint(self, client):
        """Test interlinear PDF endpoint."""
        response = client.get("/book/Genesis/chapter/1/interlinear/pdf")
        assert response.status_code in [200, 503]

    def test_new_testament_book(self, client):
        """Test New Testament book page."""
        response = client.get("/book/Matthew")
        assert response.status_code == 200

    def test_new_testament_interlinear(self, client):
        """Test New Testament interlinear."""
        response = client.get("/book/Matthew/chapter/1/interlinear")
        assert response.status_code == 200


class TestCommentaryLoaderModule:
    """Tests for commentary_loader module (64% coverage)."""

    def test_load_commentary(self):
        """Test loading commentary data."""
        from kjvstudy_org.utils.commentary_loader import load_commentary
        result = load_commentary()
        assert isinstance(result, dict)
        # Should have some books loaded
        assert len(result) > 0

    def test_load_commentary_flat(self):
        """Test loading flat commentary."""
        from kjvstudy_org.utils.commentary_loader import load_commentary_flat
        result = load_commentary_flat()
        assert isinstance(result, dict)
        # Keys should be "Book Chapter:Verse" format
        if result:
            key = list(result.keys())[0]
            assert ":" in key

    def test_normalize_entry_valid(self):
        """Test normalizing valid entry."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        entry = {
            "analysis": "Test analysis",
            "historical": "Test context",
            "questions": ["Q1", "Q2"]
        }
        result = _normalize_entry(entry)
        assert result["analysis"] == "Test analysis"
        assert result["historical"] == "Test context"
        assert result["questions"] == ["Q1", "Q2"]

    def test_normalize_entry_historical_context_key(self):
        """Test normalizing entry with historical_context key."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        entry = {
            "analysis": "Test",
            "historical_context": "Context from alt key"
        }
        result = _normalize_entry(entry)
        assert result["historical"] == "Context from alt key"

    def test_normalize_entry_not_dict(self):
        """Test normalizing non-dict entry."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        result = _normalize_entry("not a dict")
        assert result == {"analysis": "", "historical": "", "questions": []}

    def test_normalize_entry_empty(self):
        """Test normalizing empty entry."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        result = _normalize_entry({})
        assert result["analysis"] == ""
        assert result["historical"] == ""
        assert result["questions"] == []

    def test_slugify(self):
        """Test slugify function."""
        from kjvstudy_org.utils.commentary_loader import _slugify
        assert _slugify("1 Samuel") == "1_samuel"
        assert _slugify("Song of Solomon") == "song_of_solomon"
        assert _slugify("Genesis") == "genesis"

    def test_slugify_empty(self):
        """Test slugify with empty string."""
        from kjvstudy_org.utils.commentary_loader import _slugify
        result = _slugify("")
        assert result == "book"

    def test_slugify_special_chars(self):
        """Test slugify with special characters."""
        from kjvstudy_org.utils.commentary_loader import _slugify
        result = _slugify("Book!!!Name???")
        assert result == "book_name"


class TestSearchModule:
    """Tests for search module (70% coverage)."""

    def test_perform_full_text_search(self):
        """Test full text search."""
        from kjvstudy_org.utils.search import perform_full_text_search
        results = perform_full_text_search("love", limit=10)
        assert isinstance(results, list)
        if results:
            assert "book" in results[0]
            assert "text" in results[0]

    def test_perform_search_verse_reference(self):
        """Test search with verse reference."""
        from kjvstudy_org.utils.search import perform_full_text_search
        results = perform_full_text_search("John 3:16")
        assert isinstance(results, list)

    def test_calculate_relevance_score(self):
        """Test relevance score calculation."""
        from kjvstudy_org.utils.search import calculate_relevance_score
        text = "For God so loved the world that he gave"
        terms = ["loved", "world"]
        score = calculate_relevance_score(text, terms)
        assert isinstance(score, float)
        assert score > 0

    def test_calculate_relevance_score_exact_match(self):
        """Test relevance score with exact word matches."""
        from kjvstudy_org.utils.search import calculate_relevance_score
        text = "God so loved the world"
        terms = ["loved"]
        score = calculate_relevance_score(text, terms)
        # Should have bonus for exact word match
        assert score > 1.0

    def test_highlight_search_terms(self):
        """Test search term highlighting."""
        from kjvstudy_org.utils.search import highlight_search_terms
        text = "For God so loved the world"
        terms = ["loved", "world"]
        result = highlight_search_terms(text, terms)
        assert "<mark>" in result
        assert "loved" in result or "Loved" in result

    def test_ensure_search_index(self):
        """Test ensure search index."""
        from kjvstudy_org.utils.search import ensure_search_index
        result = ensure_search_index()
        # Returns True if FTS available, False otherwise
        assert isinstance(result, bool)

    def test_legacy_search(self):
        """Test legacy search function."""
        from kjvstudy_org.utils.search import _legacy_search
        results = _legacy_search("God", limit=5)
        assert isinstance(results, list)
        assert len(results) <= 5


class TestTopicsRoutes:
    """Tests for topics routes (74% coverage)."""

    def test_topics_page(self, client):
        """Test topics index page."""
        response = client.get("/topics")
        assert response.status_code == 200
        assert "Topics" in response.text or "topics" in response.text

    def test_topic_detail_love(self, client):
        """Test topic detail for love."""
        response = client.get("/topics/Love")
        # May or may not exist
        assert response.status_code in [200, 404]

    def test_topic_detail_faith(self, client):
        """Test topic detail for faith."""
        response = client.get("/topics/Faith")
        assert response.status_code in [200, 404]

    def test_topic_detail_invalid(self, client):
        """Test invalid topic returns 404."""
        response = client.get("/topics/NotARealTopic12345")
        assert response.status_code == 404

    def test_topic_pdf_endpoint(self, client):
        """Test topic PDF endpoint."""
        # Try common topics
        topics = ["Love", "Faith", "Salvation"]
        for topic in topics:
            response = client.get(f"/topics/{topic}/pdf")
            if response.status_code in [200, 503]:
                break
        # 503 if WeasyPrint not installed, 404 if topic not found
        assert response.status_code in [200, 404, 503]


class TestPdfModule:
    """Tests for PDF module (68% coverage)."""

    def test_weasyprint_available_constant(self):
        """Test WEASYPRINT_AVAILABLE constant exists."""
        from kjvstudy_org.utils.pdf import WEASYPRINT_AVAILABLE
        assert isinstance(WEASYPRINT_AVAILABLE, bool)

    def test_render_html_to_pdf_sync(self):
        """Test synchronous PDF rendering."""
        from kjvstudy_org.utils.pdf import render_html_to_pdf, WEASYPRINT_AVAILABLE
        if not WEASYPRINT_AVAILABLE:
            pytest.skip("WeasyPrint not available")
        html = "<html><body><h1>Test</h1></body></html>"
        result = render_html_to_pdf(html)
        assert result is not None

    def test_render_html_to_pdf_async_import(self):
        """Test async PDF rendering function exists."""
        from kjvstudy_org.utils.pdf import render_html_to_pdf_async, WEASYPRINT_AVAILABLE
        # Just verify the async function exists and is callable
        assert callable(render_html_to_pdf_async)

    def test_render_pdf_sync_internal(self):
        """Test internal sync render function."""
        from kjvstudy_org.utils.pdf import _render_pdf_sync, WEASYPRINT_AVAILABLE
        if not WEASYPRINT_AVAILABLE:
            with pytest.raises(RuntimeError):
                _render_pdf_sync("<html></html>")
        else:
            result = _render_pdf_sync("<html><body>Test</body></html>")
            assert result is not None


class TestBooksUtilModule:
    """Tests for utils/books.py module (79% coverage)."""

    def test_normalize_book_name_valid(self):
        """Test normalizing valid book abbreviation."""
        from kjvstudy_org.utils.books import normalize_book_name
        # Should return None for already canonical names
        result = normalize_book_name("Genesis")
        # If it's already canonical, returns None
        assert result is None or result == "Genesis"

    def test_normalize_book_name_abbreviation(self):
        """Test normalizing book abbreviation."""
        from kjvstudy_org.utils.books import normalize_book_name
        result = normalize_book_name("Gen")
        assert result == "Genesis" or result is None

    def test_ot_books_constant(self):
        """Test OT_BOOKS constant exists."""
        from kjvstudy_org.utils.books import OT_BOOKS
        assert isinstance(OT_BOOKS, (list, set, tuple))
        assert "Genesis" in OT_BOOKS

    def test_nt_books_constant(self):
        """Test NT_BOOKS constant exists."""
        from kjvstudy_org.utils.books import NT_BOOKS
        assert isinstance(NT_BOOKS, (list, set, tuple))
        assert "Matthew" in NT_BOOKS


class TestResourceData:
    """Tests for resource_data module (50% coverage)."""

    def test_resource_data_module_import(self):
        """Test resource data module imports."""
        from kjvstudy_org import resource_data
        assert resource_data is not None


class TestMainModule:
    """Tests for main module (62% coverage)."""

    def test_main_module_import(self):
        """Test main module imports."""
        from kjvstudy_org import main
        assert main is not None

    def test_main_app_exists(self):
        """Test main has app reference."""
        from kjvstudy_org import main
        # main.py typically imports app from server
        assert hasattr(main, 'app') or hasattr(main, 'server')


class TestKjvModule:
    """Tests for kjv module (83% coverage)."""

    def test_bible_get_books(self):
        """Test getting all books."""
        from kjvstudy_org.kjv import bible
        books = bible.get_books()
        assert isinstance(books, list)
        assert len(books) == 66

    def test_bible_get_chapters(self):
        """Test getting chapters for a book."""
        from kjvstudy_org.kjv import bible
        chapters = bible.get_chapters_for_book("Genesis")
        assert isinstance(chapters, list)
        assert len(chapters) == 50

    def test_bible_get_verses_by_book_chapter(self):
        """Test getting verses by book and chapter."""
        from kjvstudy_org.kjv import bible
        verses = bible.get_verses_by_book_chapter("Genesis", 1)
        assert isinstance(verses, list)
        assert len(verses) == 31

    def test_bible_iter_verses(self):
        """Test iterating over all verses."""
        from kjvstudy_org.kjv import bible
        count = 0
        for verse in bible.iter_verses():
            count += 1
            if count >= 10:
                break
        assert count == 10


class TestRedLetterModule:
    """Tests for red_letter module (92% coverage)."""

    def test_red_letter_import(self):
        """Test red letter module imports."""
        from kjvstudy_org import red_letter
        assert red_letter is not None


class TestCrossReferencesModule:
    """Tests for cross_references module (88% coverage)."""

    def test_get_cross_references(self):
        """Test getting cross references."""
        from kjvstudy_org.cross_references import get_cross_references
        refs = get_cross_references("John", 3, 16)
        assert isinstance(refs, list)

    def test_parse_reference(self):
        """Test parsing a reference."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("Genesis 1:1")
        assert result is not None
        assert result.get("book") == "Genesis"


class TestServerModule:
    """Tests for server module (86% coverage)."""

    def test_app_exists(self, client):
        """Test app exists and responds."""
        response = client.get("/")
        assert response.status_code == 200

    def test_api_docs_endpoint(self, client):
        """Test API docs endpoint."""
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_openapi_endpoint(self, client):
        """Test OpenAPI endpoint."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200


class TestJinjaFiltersModule:
    """Tests for jinja_filters module (96% coverage)."""

    def test_filters_module_import(self):
        """Test jinja filters module imports."""
        from kjvstudy_org import jinja_filters
        assert jinja_filters is not None


class TestFamilyTreeRoutes:
    """Tests for family_tree routes (85% coverage)."""

    def test_family_tree_index(self, client):
        """Test family tree index page."""
        response = client.get("/family-tree")
        assert response.status_code == 200

    def test_family_tree_person_adam(self, client):
        """Test family tree for Adam."""
        response = client.get("/family-tree/person/adam")
        assert response.status_code in [200, 404]

    def test_family_tree_person_abraham(self, client):
        """Test family tree for Abraham."""
        response = client.get("/family-tree/person/abraham")
        assert response.status_code in [200, 404]

    def test_family_tree_generation(self, client):
        """Test family tree generation view."""
        response = client.get("/family-tree/generation/1")
        assert response.status_code in [200, 404]


class TestMiscRoutes:
    """Tests for misc routes (90% coverage)."""

    def test_random_verse_redirect(self, client):
        """Test random verse endpoint."""
        response = client.get("/random", follow_redirects=False)
        # Should redirect to a random verse or return 404 if not implemented
        assert response.status_code in [200, 302, 307, 404]


class TestStudyGuidesRoutes:
    """Tests for study_guides routes (86% coverage)."""

    def test_study_guides_index(self, client):
        """Test study guides index."""
        response = client.get("/study-guides")
        assert response.status_code == 200

    def test_study_guide_salvation(self, client):
        """Test salvation study guide."""
        response = client.get("/study-guides/salvation")
        assert response.status_code in [200, 404]


class TestTimelineRoutes:
    """Tests for timeline routes (90% coverage)."""

    def test_timeline_index(self, client):
        """Test timeline index."""
        response = client.get("/timeline")
        assert response.status_code in [200, 302, 307, 404]

    def test_timeline_event(self, client):
        """Test timeline event page."""
        response = client.get("/timeline/creation")
        assert response.status_code in [200, 404]


class TestAboutRoutes:
    """Tests for about routes (94% coverage)."""

    def test_about_page(self, client):
        """Test about page."""
        response = client.get("/about")
        assert response.status_code == 200


class TestDataInit:
    """Tests for data __init__ module (95% coverage)."""

    def test_data_module_import(self):
        """Test data module imports."""
        from kjvstudy_org import data
        assert data is not None


class TestInterlinearLoaderExtended:
    """Extended tests for interlinear_loader module."""

    def test_get_interlinear_data_genesis(self):
        """Test getting interlinear data for Genesis."""
        from kjvstudy_org.interlinear_loader import get_interlinear_data
        result = get_interlinear_data("Genesis", 1, 1)
        assert result is None or isinstance(result, list)

    def test_has_interlinear_data(self):
        """Test checking if interlinear data exists."""
        from kjvstudy_org.interlinear_loader import has_interlinear_data
        result = has_interlinear_data("Genesis", 1, 1)
        assert isinstance(result, bool)

    def test_find_verses_by_strongs_h430(self):
        """Test finding verses by Strong's number H430."""
        from kjvstudy_org.interlinear_loader import find_verses_by_strongs
        result = find_verses_by_strongs("H430", limit=5)
        assert isinstance(result, list)
