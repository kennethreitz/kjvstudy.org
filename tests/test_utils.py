"""
Tests for utility modules - search, books, stories, biographies, etc.
Targeting modules with lower test coverage.
"""
import pytest
from fastapi.testclient import TestClient


class TestSearchModule:
    """Tests for kjvstudy_org.utils.search module"""

    def test_calculate_relevance_score_single_term(self):
        """Test relevance score calculation with single term"""
        from kjvstudy_org.utils.search import calculate_relevance_score

        text = "In the beginning God created the heaven and the earth."
        score = calculate_relevance_score(text, ["beginning"])
        assert score > 0

    def test_calculate_relevance_score_multiple_terms(self):
        """Test relevance score with multiple search terms"""
        from kjvstudy_org.utils.search import calculate_relevance_score

        text = "For God so loved the world"
        score = calculate_relevance_score(text, ["god", "loved"])
        # Should get points for both terms
        assert score >= 2.0

    def test_calculate_relevance_score_word_boundaries(self):
        """Test that exact word matches get bonus"""
        from kjvstudy_org.utils.search import calculate_relevance_score

        text = "God is love"
        score_exact = calculate_relevance_score(text, ["love"])
        # Exact word match should have bonus
        assert score_exact > 1.0

    def test_calculate_relevance_score_multiple_occurrences(self):
        """Test that multiple occurrences increase score"""
        from kjvstudy_org.utils.search import calculate_relevance_score

        text = "The LORD is my shepherd. The LORD is good."
        score = calculate_relevance_score(text, ["lord"])
        # Should count both occurrences
        assert score >= 2.0

    def test_highlight_search_terms_basic(self):
        """Test basic search term highlighting"""
        from kjvstudy_org.utils.search import highlight_search_terms

        text = "For God so loved the world"
        highlighted = highlight_search_terms(text, ["god"])
        assert "<mark>" in highlighted
        assert "</mark>" in highlighted

    def test_highlight_search_terms_case_insensitive(self):
        """Test case insensitive highlighting"""
        from kjvstudy_org.utils.search import highlight_search_terms

        text = "The LORD is my shepherd"
        highlighted = highlight_search_terms(text, ["lord"])
        assert "<mark>" in highlighted

    def test_highlight_search_terms_multiple(self):
        """Test highlighting multiple terms"""
        from kjvstudy_org.utils.search import highlight_search_terms

        text = "God is love"
        highlighted = highlight_search_terms(text, ["god", "love"])
        # Should have two mark tags
        assert highlighted.count("<mark>") == 2

    def test_ensure_search_index(self):
        """Test search index initialization"""
        from kjvstudy_org.utils.search import ensure_search_index

        # Should return True if FTS available, False otherwise
        result = ensure_search_index()
        assert isinstance(result, bool)

    def test_perform_full_text_search_verse_reference(self):
        """Test search with verse reference"""
        from kjvstudy_org.utils.search import perform_full_text_search

        # Test with verse reference format
        results = perform_full_text_search("John 3:16")
        assert len(results) >= 1
        assert results[0]["book"] == "John"
        assert results[0]["chapter"] == 3
        assert results[0]["verse"] == 16

    def test_perform_full_text_search_regular_query(self):
        """Test regular keyword search"""
        from kjvstudy_org.utils.search import perform_full_text_search

        results = perform_full_text_search("love", limit=10)
        assert len(results) > 0
        # All results should have the search term (or stem)
        for result in results:
            text_lower = result["text"].lower()
            # FTS may use stemming, so check for love/loved/loves
            assert "love" in text_lower or "loved" in text_lower or "loves" in text_lower


class TestBooksModule:
    """Tests for kjvstudy_org.books module"""

    def test_get_book_data_genesis(self):
        """Test getting data for Genesis"""
        from kjvstudy_org.books import get_book_data

        data = get_book_data("Genesis")
        assert data is not None
        assert "introduction" in data or "name" in data

    def test_get_book_data_psalms(self):
        """Test getting data for Psalms"""
        from kjvstudy_org.books import get_book_data

        data = get_book_data("Psalms")
        assert data is not None

    def test_get_book_data_invalid(self):
        """Test getting data for non-existent book"""
        from kjvstudy_org.books import get_book_data

        data = get_book_data("NotABook")
        assert data is None

    def test_get_book_introduction(self):
        """Test getting book introduction"""
        from kjvstudy_org.books import get_book_introduction

        intro = get_book_introduction("Genesis")
        # Should return string or None
        assert intro is None or isinstance(intro, str)

    def test_get_book_themes(self):
        """Test getting book themes"""
        from kjvstudy_org.books import get_book_themes

        themes = get_book_themes("Genesis")
        # Should return list or None
        assert themes is None or isinstance(themes, list)

    def test_get_book_key_verses(self):
        """Test getting key verses"""
        from kjvstudy_org.books import get_book_key_verses

        verses = get_book_key_verses("John")
        assert verses is None or isinstance(verses, list)

    def test_get_book_outline(self):
        """Test getting book outline"""
        from kjvstudy_org.books import get_book_outline

        outline = get_book_outline("Romans")
        assert outline is None or isinstance(outline, list)

    def test_get_book_christ_in_book(self):
        """Test getting Christ in book section"""
        from kjvstudy_org.books import get_book_christ_in_book

        result = get_book_christ_in_book("Isaiah")
        assert result is None or isinstance(result, str)

    def test_get_book_metadata(self):
        """Test getting book metadata"""
        from kjvstudy_org.books import get_book_metadata

        metadata = get_book_metadata("Matthew")
        if metadata:
            assert "testament" in metadata or "name" in metadata

    def test_get_book_metadata_invalid(self):
        """Test getting metadata for invalid book"""
        from kjvstudy_org.books import get_book_metadata

        metadata = get_book_metadata("FakeBook")
        assert metadata is None

    def test_get_all_books_metadata(self):
        """Test getting all books metadata"""
        from kjvstudy_org.books import get_all_books_metadata

        all_books = get_all_books_metadata()
        assert isinstance(all_books, list)
        # Should have 66 books
        assert len(all_books) == 66

    def test_has_book_data(self):
        """Test checking if book has data"""
        from kjvstudy_org.books import has_book_data

        assert has_book_data("Genesis") is True
        assert has_book_data("NotABook") is False

    def test_get_books_by_category(self):
        """Test getting books by category"""
        from kjvstudy_org.books import get_books_by_category

        categories = get_books_by_category()
        assert isinstance(categories, dict)
        # Should have multiple categories
        assert len(categories) > 0


class TestStoriesModule:
    """Tests for kjvstudy_org.stories module"""

    def test_load_all_stories(self):
        """Test loading all stories"""
        from kjvstudy_org.stories import load_all_stories

        stories = load_all_stories()
        assert isinstance(stories, list)

    def test_get_all_stories_flat(self):
        """Test getting flat list of stories"""
        from kjvstudy_org.stories import get_all_stories_flat

        stories = get_all_stories_flat()
        assert isinstance(stories, list)
        if len(stories) > 0:
            # Each story should have category info attached
            story = stories[0]
            assert "category_name" in story or "slug" in story

    def test_get_story_by_slug_exists(self):
        """Test getting existing story by slug"""
        from kjvstudy_org.stories import get_all_stories_flat, get_story_by_slug

        all_stories = get_all_stories_flat()
        if len(all_stories) > 0:
            first_slug = all_stories[0].get("slug")
            if first_slug:
                story = get_story_by_slug(first_slug)
                assert story is not None

    def test_get_story_by_slug_not_exists(self):
        """Test getting non-existent story"""
        from kjvstudy_org.stories import get_story_by_slug

        story = get_story_by_slug("not-a-real-story-slug-12345")
        assert story is None

    def test_get_stories_by_category(self):
        """Test getting stories by category"""
        from kjvstudy_org.stories import load_all_stories, get_stories_by_category

        categories = load_all_stories()
        if len(categories) > 0:
            cat_slug = categories[0].get("slug")
            if cat_slug:
                stories = get_stories_by_category(cat_slug)
                assert isinstance(stories, list)

    def test_get_stories_by_invalid_category(self):
        """Test getting stories from non-existent category"""
        from kjvstudy_org.stories import get_stories_by_category

        stories = get_stories_by_category("not-a-real-category")
        assert stories == []

    def test_get_category_by_slug_exists(self):
        """Test getting existing category"""
        from kjvstudy_org.stories import load_all_stories, get_category_by_slug

        categories = load_all_stories()
        if len(categories) > 0:
            slug = categories[0].get("slug")
            if slug:
                category = get_category_by_slug(slug)
                assert category is not None

    def test_get_category_by_slug_not_exists(self):
        """Test getting non-existent category"""
        from kjvstudy_org.stories import get_category_by_slug

        category = get_category_by_slug("fake-category-slug-xyz")
        assert category is None

    def test_get_story_count(self):
        """Test getting story count"""
        from kjvstudy_org.stories import get_story_count

        count = get_story_count()
        assert isinstance(count, int)
        assert count >= 0

    def test_get_category_count(self):
        """Test getting category count"""
        from kjvstudy_org.stories import get_category_count

        count = get_category_count()
        assert isinstance(count, int)
        assert count >= 0

    def test_get_categories(self):
        """Test getting categories"""
        from kjvstudy_org.stories import get_categories

        categories = get_categories()
        assert isinstance(categories, list)

    def test_refresh_stories(self):
        """Test refreshing story cache"""
        from kjvstudy_org.stories import refresh_stories, get_categories

        # Should not raise
        refresh_stories()
        categories = get_categories()
        assert isinstance(categories, list)


class TestBiblicalBiographies:
    """Tests for kjvstudy_org.biblical_biographies module"""

    def test_get_biography_abraham(self):
        """Test getting Abraham's biography"""
        from kjvstudy_org.biblical_biographies import get_biography

        bio = get_biography("Abraham")
        assert bio is not None
        assert isinstance(bio, dict)

    def test_get_biography_david(self):
        """Test getting David's biography"""
        from kjvstudy_org.biblical_biographies import get_biography

        bio = get_biography("David")
        assert bio is not None

    def test_get_biography_not_exists(self):
        """Test getting non-existent biography"""
        from kjvstudy_org.biblical_biographies import get_biography

        bio = get_biography("Not A Real Person At All")
        assert bio is None

    def test_get_biography_via_alias(self):
        """Test getting biography via alias name"""
        from kjvstudy_org.biblical_biographies import get_biography, BIOGRAPHY_ALIASES

        # If there are aliases, test one
        if BIOGRAPHY_ALIASES:
            alias = next(iter(BIOGRAPHY_ALIASES.keys()))
            bio = get_biography(alias)
            # Should either find via alias or return None if canonical not found
            # Just verify no crash
            assert bio is None or isinstance(bio, dict)

    def test_has_biography_exists(self):
        """Test checking existing biography"""
        from kjvstudy_org.biblical_biographies import has_biography

        assert has_biography("Abraham") is True

    def test_has_biography_not_exists(self):
        """Test checking non-existent biography"""
        from kjvstudy_org.biblical_biographies import has_biography

        assert has_biography("Totally Made Up Person") is False

    def test_has_biography_via_alias(self):
        """Test checking biography via alias"""
        from kjvstudy_org.biblical_biographies import has_biography, BIOGRAPHY_ALIASES

        if BIOGRAPHY_ALIASES:
            alias = next(iter(BIOGRAPHY_ALIASES.keys()))
            # Should return boolean
            result = has_biography(alias)
            assert isinstance(result, bool)


class TestRedLetterModule:
    """Tests for kjvstudy_org.red_letter module"""

    def test_load_red_letter_verses(self):
        """Test loading red letter verses"""
        from kjvstudy_org.red_letter import load_red_letter_verses

        verses = load_red_letter_verses()
        assert isinstance(verses, dict)

    def test_get_christ_words_known_verse(self):
        """Test getting Christ's words from known red letter verse"""
        from kjvstudy_org.red_letter import get_christ_words

        # John 3:16 - Jesus speaking
        words = get_christ_words("John", 3, 16)
        # May or may not be marked as red letter depending on data
        # Just verify no crash
        assert words is None or isinstance(words, str)

    def test_get_christ_words_not_red_letter(self):
        """Test verse without Christ's words"""
        from kjvstudy_org.red_letter import get_christ_words

        # Genesis 1:1 - Not Jesus speaking
        words = get_christ_words("Genesis", 1, 1)
        assert words is None

    def test_wrap_red_letter_text_no_words(self):
        """Test wrapping text when no Christ words"""
        from kjvstudy_org.red_letter import wrap_red_letter_text

        text = "In the beginning God created the heaven and the earth."
        result = wrap_red_letter_text(text, "Genesis", 1, 1)
        # Should return unchanged if no red letter
        assert result == text

    def test_wrap_red_letter_text_full_verse(self):
        """Test wrapping full verse red letter"""
        from kjvstudy_org.red_letter import wrap_red_letter_text, load_red_letter_verses

        verses = load_red_letter_verses()
        # Find a verse marked as 'full'
        full_verse = None
        for ref, words in verses.items():
            if words == 'full':
                full_verse = ref
                break

        if full_verse:
            # Parse reference
            parts = full_verse.rsplit(' ', 1)
            if len(parts) == 2:
                book = parts[0]
                chap_verse = parts[1].split(':')
                if len(chap_verse) == 2:
                    chapter, verse = int(chap_verse[0]), int(chap_verse[1])
                    text = "Some verse text"
                    result = wrap_red_letter_text(text, book, chapter, verse)
                    assert 'class="words-of-christ"' in result


class TestHelpersModule:
    """Tests for kjvstudy_org.utils.helpers module"""

    def test_create_slug_basic(self):
        """Test basic slug creation"""
        from kjvstudy_org.utils.helpers import create_slug

        slug = create_slug("Hello World")
        assert slug == "hello-world"

    def test_create_slug_special_chars(self):
        """Test slug with special characters"""
        from kjvstudy_org.utils.helpers import create_slug

        slug = create_slug("God's Love!")
        assert "'" not in slug
        assert "!" not in slug

    def test_create_slug_numbers(self):
        """Test slug with numbers"""
        from kjvstudy_org.utils.helpers import create_slug

        slug = create_slug("John 3:16")
        assert isinstance(slug, str)
        assert len(slug) > 0

    def test_is_verse_reference_valid(self):
        """Test valid verse reference detection"""
        from kjvstudy_org.utils.helpers import is_verse_reference

        assert is_verse_reference("John 3:16") is True
        assert is_verse_reference("Genesis 1:1") is True
        assert is_verse_reference("1 John 4:8") is True

    def test_is_verse_reference_invalid(self):
        """Test invalid verse reference detection"""
        from kjvstudy_org.utils.helpers import is_verse_reference

        assert is_verse_reference("hello world") is False
        assert is_verse_reference("God is love") is False

    def test_parse_verse_reference_valid(self):
        """Test parsing valid verse reference"""
        from kjvstudy_org.utils.helpers import parse_verse_reference

        result = parse_verse_reference("John 3:16")
        assert result is not None
        assert result["book"] == "John"
        assert result["chapter"] == 3
        assert result["verse"] == 16

    def test_parse_verse_reference_invalid(self):
        """Test parsing invalid verse reference"""
        from kjvstudy_org.utils.helpers import parse_verse_reference

        result = parse_verse_reference("not a verse")
        assert result is None

    def test_get_verse_text(self):
        """Test getting verse text"""
        from kjvstudy_org.utils.helpers import get_verse_text

        text = get_verse_text("John", 3, 16)
        assert isinstance(text, str)
        assert len(text) > 0

    def test_get_verse_text_invalid(self):
        """Test getting text for invalid verse"""
        from kjvstudy_org.utils.helpers import get_verse_text

        text = get_verse_text("FakeBook", 999, 999)
        # Should return some fallback string
        assert isinstance(text, str)

    def test_get_daily_verse(self):
        """Test getting daily verse"""
        from kjvstudy_org.utils.helpers import get_daily_verse

        verse = get_daily_verse()
        assert isinstance(verse, dict)
        assert "book" in verse
        assert "chapter" in verse
        assert "verse" in verse
        assert "text" in verse

    def test_get_chapter_popularity_score(self):
        """Test getting chapter popularity score"""
        from kjvstudy_org.utils.helpers import get_chapter_popularity_score

        # Psalms 23 should be popular
        score = get_chapter_popularity_score("Psalms", 23)
        assert isinstance(score, int)
        assert 1 <= score <= 10

    def test_get_chapter_popularity_explanation(self):
        """Test getting chapter popularity explanation"""
        from kjvstudy_org.utils.helpers import get_chapter_popularity_explanation

        explanation = get_chapter_popularity_explanation("Psalms", 23)
        assert isinstance(explanation, str)
        assert len(explanation) > 0

    def test_get_related_content(self):
        """Test getting related content"""
        from kjvstudy_org.utils.helpers import get_related_content

        related = get_related_content("John", 3, 16)
        assert isinstance(related, dict)
        assert "study_guides" in related
        assert "topics" in related


class TestCommentaryLoaderModule:
    """Tests for kjvstudy_org.utils.commentary_loader module"""

    def test_load_commentary(self):
        """Test loading commentary data"""
        from kjvstudy_org.utils.commentary_loader import load_commentary

        commentary = load_commentary()
        assert isinstance(commentary, dict)

    def test_load_commentary_flat(self):
        """Test loading flat commentary"""
        from kjvstudy_org.utils.commentary_loader import load_commentary_flat

        flat = load_commentary_flat()
        assert isinstance(flat, dict)
        # Keys should be like "Book Chapter:Verse"
        if flat:
            key = next(iter(flat.keys()))
            assert ":" in key

    def test_normalize_entry_valid(self):
        """Test normalizing valid entry"""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry

        entry = {
            "analysis": "Some analysis",
            "historical": "Historical context",
            "questions": ["Q1", "Q2"]
        }
        normalized = _normalize_entry(entry)
        assert normalized["analysis"] == "Some analysis"
        assert normalized["historical"] == "Historical context"
        assert len(normalized["questions"]) == 2

    def test_normalize_entry_with_historical_context(self):
        """Test normalizing entry with historical_context key"""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry

        entry = {
            "analysis": "Analysis",
            "historical_context": "Context via alternative key"
        }
        normalized = _normalize_entry(entry)
        assert normalized["historical"] == "Context via alternative key"

    def test_normalize_entry_invalid(self):
        """Test normalizing non-dict entry"""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry

        result = _normalize_entry("not a dict")
        assert result["analysis"] == ""
        assert result["historical"] == ""
        assert result["questions"] == []

    def test_slugify(self):
        """Test slugify function"""
        from kjvstudy_org.utils.commentary_loader import _slugify

        assert _slugify("Genesis") == "genesis"
        assert _slugify("1 John") == "1_john"
        assert _slugify("Song of Solomon") == "song_of_solomon"


class TestInterlinearLoader:
    """Tests for kjvstudy_org.interlinear_loader module"""

    def test_get_interlinear_data_genesis(self):
        """Test getting interlinear data for Genesis 1:1"""
        from kjvstudy_org.interlinear_loader import get_interlinear_data

        data = get_interlinear_data("Genesis", 1, 1)
        # Returns list of word data or None
        assert data is None or isinstance(data, (dict, list))
        if isinstance(data, list) and len(data) > 0:
            # Each item should have word info
            assert "original" in data[0] or "english" in data[0]

    def test_get_interlinear_data_john(self):
        """Test getting interlinear data for John 1:1"""
        from kjvstudy_org.interlinear_loader import get_interlinear_data

        data = get_interlinear_data("John", 1, 1)
        assert data is None or isinstance(data, (dict, list))

    def test_get_interlinear_data_invalid(self):
        """Test getting interlinear data for invalid verse"""
        from kjvstudy_org.interlinear_loader import get_interlinear_data

        data = get_interlinear_data("FakeBook", 999, 999)
        assert data is None


class TestCrossReferencesModule:
    """Tests for kjvstudy_org.cross_references module"""

    def test_get_cross_references_john_3_16(self):
        """Test getting cross references for John 3:16"""
        from kjvstudy_org.cross_references import get_cross_references

        refs = get_cross_references("John", 3, 16)
        assert isinstance(refs, list)

    def test_get_cross_references_genesis(self):
        """Test getting cross references for Genesis 1:1"""
        from kjvstudy_org.cross_references import get_cross_references

        refs = get_cross_references("Genesis", 1, 1)
        assert isinstance(refs, list)

    def test_get_cross_references_invalid(self):
        """Test getting cross references for invalid verse"""
        from kjvstudy_org.cross_references import get_cross_references

        refs = get_cross_references("NotABook", 999, 999)
        assert isinstance(refs, list)
        assert len(refs) == 0


class TestPdfModule:
    """Tests for kjvstudy_org.utils.pdf module"""

    def test_weasyprint_available_flag(self):
        """Test that WEASYPRINT_AVAILABLE flag is set"""
        from kjvstudy_org.utils.pdf import WEASYPRINT_AVAILABLE

        assert isinstance(WEASYPRINT_AVAILABLE, bool)

    def test_render_html_to_pdf_when_available(self):
        """Test PDF rendering when weasyprint available"""
        from kjvstudy_org.utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf

        if WEASYPRINT_AVAILABLE:
            html = "<html><body><h1>Test</h1></body></html>"
            pdf_buffer = render_html_to_pdf(html)
            assert pdf_buffer is not None
            # Should be at position 0
            assert pdf_buffer.tell() == 0
            # Should have PDF content
            content = pdf_buffer.read()
            assert content.startswith(b'%PDF')
        else:
            # Should raise RuntimeError when not available
            with pytest.raises(RuntimeError):
                render_html_to_pdf("<html></html>")

    def test_render_html_to_pdf_async(self):
        """Test async PDF rendering function exists"""
        from kjvstudy_org.utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf_async
        import asyncio

        # Just verify the async function exists and is callable
        assert callable(render_html_to_pdf_async)

        # If weasyprint available, test via sync wrapper
        if WEASYPRINT_AVAILABLE:
            html = "<html><body><p>Async Test</p></body></html>"
            # Run async function synchronously for testing
            loop = asyncio.new_event_loop()
            try:
                pdf_buffer = loop.run_until_complete(render_html_to_pdf_async(html))
                assert pdf_buffer is not None
                content = pdf_buffer.read()
                assert content.startswith(b'%PDF')
            finally:
                loop.close()


class TestTopicsModule:
    """Tests for kjvstudy_org.topics module"""

    def test_get_all_topics(self):
        """Test getting all topics"""
        from kjvstudy_org.topics import get_all_topics

        topics = get_all_topics()
        assert isinstance(topics, dict)
        assert len(topics) > 0

    def test_get_topic_valid(self):
        """Test getting valid topic"""
        from kjvstudy_org.topics import get_all_topics, get_topic

        all_topics = get_all_topics()
        if all_topics:
            topic_name = next(iter(all_topics.keys()))
            topic = get_topic(topic_name)
            assert topic is not None

    def test_get_topic_invalid(self):
        """Test getting invalid topic"""
        from kjvstudy_org.topics import get_topic

        topic = get_topic("not_a_real_topic_xyz123")
        assert topic is None


class TestStoriesRoutes:
    """Tests for kjvstudy_org.routes.stories module"""

    def test_stories_index_page(self, client):
        """Test stories index page loads"""
        response = client.get("/stories")
        assert response.status_code == 200
        assert "Stories" in response.text or "stories" in response.text.lower()

    def test_stories_category_page(self, client):
        """Test stories category page"""
        from kjvstudy_org.stories import load_all_stories

        categories = load_all_stories()
        if categories:
            slug = categories[0].get("slug")
            if slug:
                response = client.get(f"/stories/category/{slug}")
                # Should return 200 or redirect
                assert response.status_code in [200, 301, 302, 307, 404]

    def test_stories_invalid_category(self, client):
        """Test invalid category returns 404"""
        response = client.get("/stories/category/not-a-real-category-xyz")
        assert response.status_code == 404

    def test_story_detail_page(self, client):
        """Test individual story page"""
        from kjvstudy_org.stories import get_all_stories_flat

        stories = get_all_stories_flat()
        if stories:
            slug = stories[0].get("slug")
            if slug:
                response = client.get(f"/story/{slug}")
                # Should return 200 or 404
                assert response.status_code in [200, 404]

    def test_story_invalid_slug(self, client):
        """Test invalid story slug returns 404"""
        response = client.get("/story/not-a-real-story-slug-xyz")
        assert response.status_code == 404


class TestReadingPlansModule:
    """Tests for kjvstudy_org.reading_plans module"""

    def test_get_all_plans(self):
        """Test getting all reading plans"""
        from kjvstudy_org.reading_plans import get_all_plans

        plans = get_all_plans()
        assert isinstance(plans, dict)
        assert len(plans) > 0

    def test_get_plan_by_id(self):
        """Test getting reading plan by ID"""
        from kjvstudy_org.reading_plans import get_all_plans, get_plan

        plans = get_all_plans()
        if plans:
            plan_id = next(iter(plans.keys()))
            plan = get_plan(plan_id)
            assert plan is not None

    def test_get_plan_invalid_id(self):
        """Test getting reading plan with invalid ID"""
        from kjvstudy_org.reading_plans import get_plan

        plan = get_plan("not-a-real-plan-id-xyz")
        assert plan is None

    def test_get_plan_summary(self):
        """Test getting plan summary"""
        from kjvstudy_org.reading_plans import get_plan_summary

        summary = get_plan_summary()
        assert isinstance(summary, list)
        assert len(summary) > 0
        # Each item should have name and id
        if summary:
            assert "name" in summary[0] or "id" in summary[0]
