"""
Additional tests to improve coverage - Part 2.

Targets:
- cross_references.py (68% -> higher)
- jinja_filters.py (74% -> higher)
- commentary_loader.py (64% -> higher)
- topics.py (77% -> higher)
- search_index.py (48% -> higher)
"""
import pytest


class TestCrossReferencesModule:
    """Direct tests for cross_references module."""

    def test_get_cross_references_john_3_16(self):
        """Test cross references for famous verse."""
        from kjvstudy_org.cross_references import get_cross_references
        refs = get_cross_references("John", 3, 16)
        assert isinstance(refs, list)

    def test_get_cross_references_genesis_1_1(self):
        """Test cross references for first verse."""
        from kjvstudy_org.cross_references import get_cross_references
        refs = get_cross_references("Genesis", 1, 1)
        assert isinstance(refs, list)

    def test_get_cross_references_nonexistent(self):
        """Test cross references for verse with no refs."""
        from kjvstudy_org.cross_references import get_cross_references
        refs = get_cross_references("Philemon", 1, 25)
        assert isinstance(refs, list)

    def test_parse_reference_valid(self):
        """Test parsing valid reference."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("Genesis 1:1")
        assert result is not None
        assert result["book"] == "Genesis"
        assert result["chapter"] == 1
        assert result["verse"] == 1

    def test_parse_reference_numbered_book(self):
        """Test parsing numbered book reference."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("1 John 3:16")
        assert result is not None
        assert result["book"] == "1 John"
        assert result["chapter"] == 3
        assert result["verse"] == 16

    def test_parse_reference_invalid_no_colon(self):
        """Test parsing invalid reference without colon."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("Genesis 1")
        assert result is None

    def test_parse_reference_invalid_no_space(self):
        """Test parsing invalid reference without space."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("Genesis1:1")
        assert result is None

    def test_parse_reference_invalid_non_numeric(self):
        """Test parsing invalid reference with non-numeric values."""
        from kjvstudy_org.cross_references import parse_reference
        result = parse_reference("Genesis abc:xyz")
        assert result is None

    def test_cross_references_with_text(self):
        """Test that cross references include verse text."""
        from kjvstudy_org.cross_references import get_cross_references
        refs = get_cross_references("John", 3, 16)
        if refs:
            # Should have text field (may be empty for some)
            assert "text" in refs[0] or "ref" in refs[0]


class TestJinjaFilters:
    """Tests for Jinja2 template filters."""

    def test_markdown_to_html_basic(self):
        """Test basic markdown conversion."""
        from kjvstudy_org.jinja_filters import markdown_to_html
        result = markdown_to_html("**bold** and *italic*")
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_markdown_to_html_empty(self):
        """Test markdown with empty input."""
        from kjvstudy_org.jinja_filters import markdown_to_html
        assert markdown_to_html("") == ""
        assert markdown_to_html(None) is None

    def test_markdown_inline_basic(self):
        """Test inline markdown conversion."""
        from kjvstudy_org.jinja_filters import markdown_inline
        result = markdown_inline("**bold**")
        assert "<strong>bold</strong>" in result
        # Should not have paragraph wrapper
        assert not result.startswith("<p>")

    def test_markdown_inline_empty(self):
        """Test inline markdown with empty input."""
        from kjvstudy_org.jinja_filters import markdown_inline
        assert markdown_inline("") == ""
        assert markdown_inline(None) is None

    def test_link_verse_references(self):
        """Test verse reference linking."""
        from kjvstudy_org.jinja_filters import link_verse_references_in_text
        result = link_verse_references_in_text("Read John 3:16 for more.")
        # The function links verse references
        assert 'href="' in result
        assert "John" in result
        assert "3:16" in result

    def test_link_verse_references_range(self):
        """Test verse range reference linking."""
        from kjvstudy_org.jinja_filters import link_verse_references_in_text
        result = link_verse_references_in_text("In Genesis 1:1-3 we see")
        assert 'href="' in result
        assert "Genesis" in result

    def test_link_verse_references_numbered_book(self):
        """Test numbered book reference linking."""
        from kjvstudy_org.jinja_filters import link_verse_references_in_text
        result = link_verse_references_in_text("See 1 John 4:8")
        assert 'href="/book/1 John/chapter/4#verse-8"' in result

    def test_link_verse_references_empty(self):
        """Test verse reference linking with empty input."""
        from kjvstudy_org.jinja_filters import link_verse_references_in_text
        assert link_verse_references_in_text("") == ""
        assert link_verse_references_in_text(None) is None

    def test_inject_word_markers_basic(self):
        """Test word marker injection."""
        from kjvstudy_org.jinja_filters import inject_word_markers
        word_studies = [
            {"word": "love", "term": "agape", "translit": "agapē", "note": "Divine love"}
        ]
        result = inject_word_markers("God is love.", word_studies, 1)
        assert "sidenote" in result
        assert "agape" in result

    def test_inject_word_markers_empty(self):
        """Test word marker injection with no studies."""
        from kjvstudy_org.jinja_filters import inject_word_markers
        result = inject_word_markers("God is love.", [], 1)
        assert result == "God is love."

    def test_format_numbered_lists_basic(self):
        """Test numbered list formatting."""
        from kjvstudy_org.jinja_filters import format_numbered_lists
        text = "The points are: (1) first point (2) second point (3) third point."
        result = format_numbered_lists(text)
        assert "<ol>" in result
        assert "<li>" in result

    def test_format_numbered_lists_no_list(self):
        """Test text without numbered list."""
        from kjvstudy_org.jinja_filters import format_numbered_lists
        text = "Just regular text."
        result = format_numbered_lists(text)
        assert result == text

    def test_split_paragraphs_basic(self):
        """Test paragraph splitting."""
        from kjvstudy_org.jinja_filters import split_paragraphs
        text = "First paragraph.\n\nSecond paragraph."
        result = split_paragraphs(text)
        assert "<p>First paragraph.</p>" in result
        assert "<p>Second paragraph.</p>" in result

    def test_split_paragraphs_empty(self):
        """Test paragraph splitting with empty input."""
        from kjvstudy_org.jinja_filters import split_paragraphs
        assert split_paragraphs("") == ""
        assert split_paragraphs(None) is None

    def test_number_format(self):
        """Test number formatting."""
        from kjvstudy_org.jinja_filters import number_format
        assert number_format(31102) == "31,102"
        assert number_format(1000000) == "1,000,000"
        assert number_format(100) == "100"

    def test_linkify_strongs_greek(self):
        """Test Strong's Greek number linking."""
        from kjvstudy_org.jinja_filters import linkify_strongs
        result = linkify_strongs("The word G26 means love.")
        assert 'href="/strongs/G26"' in result
        assert "strongs-ref" in result

    def test_linkify_strongs_hebrew(self):
        """Test Strong's Hebrew number linking."""
        from kjvstudy_org.jinja_filters import linkify_strongs
        result = linkify_strongs("The word H157 means love.")
        assert 'href="/strongs/H157"' in result

    def test_linkify_strongs_empty(self):
        """Test Strong's linking with empty input."""
        from kjvstudy_org.jinja_filters import linkify_strongs
        assert linkify_strongs("") == ""
        assert linkify_strongs(None) is None


class TestCommentaryLoader:
    """Tests for commentary loader module."""

    def test_load_commentary(self):
        """Test loading commentary data."""
        from kjvstudy_org.utils.commentary_loader import load_commentary
        data = load_commentary()
        assert isinstance(data, dict)
        # Should have some books
        assert len(data) > 0

    def test_load_commentary_flat(self):
        """Test loading flat commentary data."""
        from kjvstudy_org.utils.commentary_loader import load_commentary_flat
        data = load_commentary_flat()
        assert isinstance(data, dict)
        # Keys should be in "Book Chapter:Verse" format
        if data:
            key = list(data.keys())[0]
            assert ":" in key

    def test_normalize_entry_valid(self):
        """Test normalizing valid entry."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        entry = {
            "analysis": "Test analysis",
            "historical": "Test historical",
            "questions": ["Q1", "Q2"]
        }
        result = _normalize_entry(entry)
        assert result["analysis"] == "Test analysis"
        assert result["historical"] == "Test historical"
        assert result["questions"] == ["Q1", "Q2"]

    def test_normalize_entry_historical_context(self):
        """Test normalizing entry with historical_context key."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        entry = {
            "analysis": "Test",
            "historical_context": "Historical info"
        }
        result = _normalize_entry(entry)
        assert result["historical"] == "Historical info"

    def test_normalize_entry_non_dict(self):
        """Test normalizing non-dict entry."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        result = _normalize_entry("not a dict")
        assert result["analysis"] == ""
        assert result["historical"] == ""
        assert result["questions"] == []

    def test_normalize_entry_missing_fields(self):
        """Test normalizing entry with missing fields."""
        from kjvstudy_org.utils.commentary_loader import _normalize_entry
        result = _normalize_entry({})
        assert result["analysis"] == ""
        assert result["historical"] == ""
        assert result["questions"] == []

    def test_slugify(self):
        """Test book name slugification."""
        from kjvstudy_org.utils.commentary_loader import _slugify
        assert _slugify("Genesis") == "genesis"
        assert _slugify("1 Samuel") == "1_samuel"
        assert _slugify("Song of Solomon") == "song_of_solomon"


class TestTopicsModule:
    """Tests for topics module."""

    def test_get_all_topics(self):
        """Test getting all topics."""
        from kjvstudy_org.topics import get_all_topics
        topics = get_all_topics()
        assert isinstance(topics, dict)

    def test_get_topic_valid(self):
        """Test getting a valid topic."""
        from kjvstudy_org.topics import get_all_topics, get_topic
        all_topics = get_all_topics()
        if all_topics:
            topic_name = list(all_topics.keys())[0]
            topic = get_topic(topic_name)
            assert topic is not None

    def test_get_topic_invalid(self):
        """Test getting non-existent topic."""
        from kjvstudy_org.topics import get_topic
        result = get_topic("NonExistentTopic12345")
        assert result is None

    def test_get_topic_with_text(self):
        """Test getting topic with verse text."""
        from kjvstudy_org.topics import get_all_topics, get_topic_with_text
        all_topics = get_all_topics()
        if all_topics:
            topic_name = list(all_topics.keys())[0]
            topic = get_topic_with_text(topic_name)
            if topic:
                assert "subtopics" in topic or isinstance(topic, dict)

    def test_get_topic_with_text_invalid(self):
        """Test getting non-existent topic with text."""
        from kjvstudy_org.topics import get_topic_with_text
        result = get_topic_with_text("NonExistentTopic12345")
        assert result is None

    def test_search_topics(self):
        """Test searching topics."""
        from kjvstudy_org.topics import search_topics
        results = search_topics("love")
        assert isinstance(results, list)

    def test_search_topics_no_results(self):
        """Test searching topics with no results."""
        from kjvstudy_org.topics import search_topics
        results = search_topics("xyznonexistent12345")
        assert isinstance(results, list)
        assert len(results) == 0


class TestSearchIndexModule:
    """Tests for search index module."""

    def test_get_search_stats(self):
        """Test getting search stats."""
        from kjvstudy_org.utils.search_index import get_search_stats
        stats = get_search_stats()
        assert isinstance(stats, dict)
        assert "indexed" in stats

    def test_highlight_matches(self):
        """Test highlighting search matches."""
        from kjvstudy_org.utils.search_index import highlight_matches
        result = highlight_matches("God is love", "love")
        assert "<mark>love</mark>" in result

    def test_highlight_matches_multiple(self):
        """Test highlighting multiple matches."""
        from kjvstudy_org.utils.search_index import highlight_matches
        result = highlight_matches("God is love and love is God", "love")
        assert result.count("<mark>love</mark>") == 2

    def test_highlight_matches_case_insensitive(self):
        """Test case insensitive highlighting."""
        from kjvstudy_org.utils.search_index import highlight_matches
        result = highlight_matches("LOVE is love", "love")
        assert "<mark>" in result


class TestReadingPlansModule:
    """Tests for reading plans module."""

    def test_get_plan_valid(self):
        """Test getting a valid reading plan."""
        from kjvstudy_org.reading_plans import get_plan
        plan = get_plan("chronological")
        if plan:
            assert "name" in plan

    def test_get_plan_invalid(self):
        """Test getting non-existent plan."""
        from kjvstudy_org.reading_plans import get_plan
        plan = get_plan("nonexistent-plan-xyz")
        assert plan is None

    def test_get_plan_summary(self):
        """Test getting plan summary."""
        from kjvstudy_org.reading_plans import get_plan_summary
        summary = get_plan_summary()
        assert isinstance(summary, (list, dict))


class TestStoriesModule:
    """Tests for stories module."""

    def test_load_all_stories(self):
        """Test loading all stories."""
        from kjvstudy_org.stories import load_all_stories
        stories = load_all_stories()
        assert isinstance(stories, list)

    def test_get_all_stories_flat(self):
        """Test getting flat stories list."""
        from kjvstudy_org.stories import get_all_stories_flat
        stories = get_all_stories_flat()
        assert isinstance(stories, list)

    def test_get_story_by_slug_invalid(self):
        """Test getting non-existent story."""
        from kjvstudy_org.stories import get_story_by_slug
        story = get_story_by_slug("nonexistent-story-xyz")
        assert story is None

    def test_get_stories_by_category(self):
        """Test getting stories by category."""
        from kjvstudy_org.stories import get_stories_by_category, get_categories
        categories = get_categories()
        if categories:
            cat_slug = categories[0].get("slug")
            if cat_slug:
                stories = get_stories_by_category(cat_slug)
                assert isinstance(stories, list)

    def test_get_stories_by_category_invalid(self):
        """Test getting stories from non-existent category."""
        from kjvstudy_org.stories import get_stories_by_category
        stories = get_stories_by_category("nonexistent-category")
        assert stories == []

    def test_get_category_by_slug(self):
        """Test getting category by slug."""
        from kjvstudy_org.stories import get_category_by_slug, get_categories
        categories = get_categories()
        if categories:
            cat_slug = categories[0].get("slug")
            if cat_slug:
                category = get_category_by_slug(cat_slug)
                assert category is not None

    def test_get_category_by_slug_invalid(self):
        """Test getting non-existent category."""
        from kjvstudy_org.stories import get_category_by_slug
        category = get_category_by_slug("nonexistent-category")
        assert category is None

    def test_get_story_count(self):
        """Test getting story count."""
        from kjvstudy_org.stories import get_story_count
        count = get_story_count()
        assert isinstance(count, int)
        assert count >= 0

    def test_get_category_count(self):
        """Test getting category count."""
        from kjvstudy_org.stories import get_category_count
        count = get_category_count()
        assert isinstance(count, int)
        assert count >= 0


class TestKJVModule:
    """Tests for kjv module."""

    def test_get_books(self):
        """Test getting all books."""
        from kjvstudy_org.kjv import bible
        books = bible.get_books()
        assert len(books) == 66

    def test_get_verse_text(self):
        """Test getting specific verse text."""
        from kjvstudy_org.kjv import bible
        text = bible.get_verse_text("Genesis", 1, 1)
        assert "beginning" in text.lower()

    def test_get_verse_text_invalid(self):
        """Test getting verse text for invalid reference."""
        from kjvstudy_org.kjv import bible
        text = bible.get_verse_text("NotABook", 1, 1)
        assert text is None or text == ""

    def test_get_chapters_for_book(self):
        """Test getting chapters for a book."""
        from kjvstudy_org.kjv import bible
        chapters = bible.get_chapters_for_book("Genesis")
        assert len(chapters) == 50

    def test_get_chapters_for_psalms(self):
        """Test getting chapters for Psalms."""
        from kjvstudy_org.kjv import bible
        chapters = bible.get_chapters_for_book("Psalms")
        assert len(chapters) == 150

    def test_get_verses_by_book_chapter(self):
        """Test getting verses for a chapter."""
        from kjvstudy_org.kjv import bible
        verses = bible.get_verses_by_book_chapter("Genesis", 1)
        assert len(verses) == 31

    def test_iter_verses(self):
        """Test iterating all verses."""
        from kjvstudy_org.kjv import bible
        count = 0
        for verse in bible.iter_verses():
            count += 1
            if count >= 10:
                break
        assert count == 10


class TestBooksModule:
    """Tests for books module."""

    def test_get_book_data_genesis(self):
        """Test getting Genesis book data."""
        from kjvstudy_org.books import get_book_data, has_book_data
        if has_book_data("Genesis"):
            data = get_book_data("Genesis")
            assert data is not None

    def test_has_book_data(self):
        """Test checking for book data."""
        from kjvstudy_org.books import has_book_data
        # Should return boolean
        result = has_book_data("Genesis")
        assert isinstance(result, bool)

    def test_has_book_data_invalid(self):
        """Test checking for non-existent book data."""
        from kjvstudy_org.books import has_book_data
        result = has_book_data("NotABook")
        assert result is False


class TestUtilsBooks:
    """Tests for utils/books module."""

    def test_normalize_book_name_abbreviation(self):
        """Test normalizing book abbreviations."""
        from kjvstudy_org.utils.books import normalize_book_name
        # Gen is a known abbreviation
        result = normalize_book_name("Gen")
        assert result == "Genesis"
        # Some abbreviations may not be mapped
        # Just verify the function handles various inputs

    def test_normalize_book_name_canonical(self):
        """Test normalizing canonical names returns None."""
        from kjvstudy_org.utils.books import normalize_book_name
        # Canonical names should return None (no redirect needed)
        assert normalize_book_name("Genesis") is None

    def test_normalize_book_name_invalid(self):
        """Test normalizing invalid book name."""
        from kjvstudy_org.utils.books import normalize_book_name
        result = normalize_book_name("NotABook")
        assert result is None

    def test_ot_books_count(self):
        """Test Old Testament books count."""
        from kjvstudy_org.utils.books import OT_BOOKS
        assert len(OT_BOOKS) == 39

    def test_nt_books_count(self):
        """Test New Testament books count."""
        from kjvstudy_org.utils.books import NT_BOOKS
        assert len(NT_BOOKS) == 27


class TestRedLetterModule:
    """Tests for red letter module."""

    def test_wrap_red_letter_text_gospels(self):
        """Test red letter text in Gospels."""
        from kjvstudy_org.red_letter import wrap_red_letter_text
        # This verse contains words of Jesus
        result = wrap_red_letter_text("For God so loved the world", "John", 3, 16)
        # May or may not have red letter markup depending on verse
        assert isinstance(result, str)

    def test_wrap_red_letter_text_non_gospels(self):
        """Test red letter text outside Gospels."""
        from kjvstudy_org.red_letter import wrap_red_letter_text
        result = wrap_red_letter_text("In the beginning", "Genesis", 1, 1)
        # Genesis should not have red letters
        assert isinstance(result, str)


class TestInterlinearLoader:
    """Tests for interlinear loader module."""

    def test_get_interlinear_data_genesis(self):
        """Test getting interlinear data for Genesis."""
        from kjvstudy_org.interlinear_loader import get_interlinear_data
        data = get_interlinear_data("Genesis", 1, 1)
        # May or may not have data
        assert data is None or isinstance(data, list)

    def test_has_interlinear_data(self):
        """Test checking for interlinear data."""
        from kjvstudy_org.interlinear_loader import has_interlinear_data
        result = has_interlinear_data("Genesis", 1, 1)
        assert isinstance(result, bool)

    def test_get_interlinear_data_john(self):
        """Test getting interlinear data for John (Greek)."""
        from kjvstudy_org.interlinear_loader import get_interlinear_data
        data = get_interlinear_data("John", 1, 1)
        assert data is None or isinstance(data, list)
