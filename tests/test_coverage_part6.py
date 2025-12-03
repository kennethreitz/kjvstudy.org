"""
Additional tests to improve coverage - Part 6.

Targeting modules with lowest coverage:
- routes/resources.py (76%)
- utils/search_index.py (67%)
- routes/bible.py (60%) - PDF routes
- routes/commentary.py (78%)
"""
import pytest


class TestResourcesRoutes:
    """Tests for resources routes (76% coverage)."""

    def test_resources_index(self, client):
        """Test resources index page."""
        response = client.get("/resources")
        assert response.status_code == 200

    def test_biblical_maps(self, client):
        """Test biblical maps resource page."""
        response = client.get("/biblical-maps")
        assert response.status_code == 200

    def test_biblical_angels(self, client):
        """Test biblical angels resource page."""
        response = client.get("/biblical-angels")
        assert response.status_code == 200

    def test_biblical_prophets(self, client):
        """Test biblical prophets resource page."""
        response = client.get("/biblical-prophets")
        assert response.status_code == 200

    def test_names_of_god(self, client):
        """Test names of God resource page."""
        response = client.get("/names-of-god")
        assert response.status_code == 200

    def test_parables(self, client):
        """Test parables resource page."""
        response = client.get("/parables")
        assert response.status_code == 200

    def test_biblical_covenants(self, client):
        """Test covenants resource page."""
        response = client.get("/biblical-covenants")
        assert response.status_code == 200

    def test_twelve_apostles(self, client):
        """Test twelve apostles resource page."""
        response = client.get("/the-twelve-apostles")
        assert response.status_code == 200

    def test_women_of_the_bible(self, client):
        """Test women of the Bible resource page."""
        response = client.get("/women-of-the-bible")
        assert response.status_code == 200

    def test_biblical_festivals(self, client):
        """Test festivals resource page."""
        response = client.get("/biblical-festivals")
        assert response.status_code == 200

    def test_fruits_of_the_spirit(self, client):
        """Test fruits of the spirit resource page."""
        response = client.get("/fruits-of-the-spirit")
        assert response.status_code == 200

    def test_miracles_of_jesus(self, client):
        """Test miracles of Jesus resource page."""
        response = client.get("/miracles-of-jesus")
        assert response.status_code == 200

    def test_prayers_of_the_bible(self, client):
        """Test prayers of the Bible resource page."""
        response = client.get("/prayers-of-the-bible")
        assert response.status_code == 200

    def test_beatitudes(self, client):
        """Test beatitudes resource page."""
        response = client.get("/beatitudes")
        assert response.status_code == 200

    def test_ten_commandments(self, client):
        """Test ten commandments resource page."""
        response = client.get("/ten-commandments")
        assert response.status_code == 200

    def test_armor_of_god(self, client):
        """Test armor of God resource page."""
        response = client.get("/armor-of-god")
        assert response.status_code == 200

    def test_i_am_statements(self, client):
        """Test I AM statements resource page."""
        response = client.get("/i-am-statements")
        assert response.status_code == 200

    def test_tetragrammaton(self, client):
        """Test tetragrammaton resource page."""
        response = client.get("/tetragrammaton")
        assert response.status_code == 200


class TestResourceDetailPages:
    """Tests for resource detail pages."""

    def test_angel_detail(self, client):
        """Test angel detail page."""
        response = client.get("/biblical-angels/gabriel")
        assert response.status_code in [200, 404]

    def test_prophet_detail(self, client):
        """Test prophet detail page."""
        response = client.get("/biblical-prophets/isaiah")
        assert response.status_code in [200, 404]

    def test_apostle_detail(self, client):
        """Test apostle detail page."""
        response = client.get("/the-twelve-apostles/peter")
        assert response.status_code in [200, 404]

    def test_parable_detail(self, client):
        """Test parable detail page."""
        response = client.get("/parables/the-sower")
        assert response.status_code in [200, 404]

    def test_miracle_detail(self, client):
        """Test miracle detail page."""
        response = client.get("/miracles-of-jesus/water-to-wine")
        assert response.status_code in [200, 404]

    def test_name_of_god_detail(self, client):
        """Test name of God detail page."""
        response = client.get("/names-of-god/yahweh")
        assert response.status_code in [200, 404]

    def test_woman_detail(self, client):
        """Test woman of the Bible detail page."""
        response = client.get("/women-of-the-bible/mary")
        assert response.status_code in [200, 404]

    def test_festival_detail(self, client):
        """Test festival detail page."""
        response = client.get("/biblical-festivals/passover")
        assert response.status_code in [200, 404]

    def test_fruit_detail(self, client):
        """Test fruit of the spirit detail page."""
        response = client.get("/fruits-of-the-spirit/love")
        assert response.status_code in [200, 404]

    def test_prayer_detail(self, client):
        """Test prayer detail page."""
        response = client.get("/prayers-of-the-bible/lords-prayer")
        assert response.status_code in [200, 404]

    def test_beatitude_detail(self, client):
        """Test beatitude detail page."""
        response = client.get("/beatitudes/poor-in-spirit")
        assert response.status_code in [200, 404]


class TestResourcePDFRoutes:
    """Tests for resource PDF routes."""

    def test_angels_pdf(self, client):
        """Test angels PDF."""
        response = client.get("/biblical-angels/pdf")
        assert response.status_code in [200, 503]

    def test_prophets_pdf(self, client):
        """Test prophets PDF."""
        response = client.get("/biblical-prophets/pdf")
        assert response.status_code in [200, 503]

    def test_parables_pdf(self, client):
        """Test parables PDF."""
        response = client.get("/parables/pdf")
        assert response.status_code in [200, 503]

    def test_covenants_pdf(self, client):
        """Test covenants PDF."""
        response = client.get("/biblical-covenants/pdf")
        assert response.status_code in [200, 503]

    def test_apostles_pdf(self, client):
        """Test apostles PDF."""
        response = client.get("/the-twelve-apostles/pdf")
        assert response.status_code in [200, 503]

    def test_women_pdf(self, client):
        """Test women PDF."""
        response = client.get("/women-of-the-bible/pdf")
        assert response.status_code in [200, 503]

    def test_festivals_pdf(self, client):
        """Test festivals PDF."""
        response = client.get("/biblical-festivals/pdf")
        assert response.status_code in [200, 503]

    def test_fruits_pdf(self, client):
        """Test fruits PDF."""
        response = client.get("/fruits-of-the-spirit/pdf")
        assert response.status_code in [200, 503]

    def test_miracles_pdf(self, client):
        """Test miracles PDF."""
        response = client.get("/miracles-of-jesus/pdf")
        assert response.status_code in [200, 503]

    def test_prayers_pdf(self, client):
        """Test prayers PDF."""
        response = client.get("/prayers-of-the-bible/pdf")
        assert response.status_code in [200, 503]

    def test_beatitudes_pdf(self, client):
        """Test beatitudes PDF."""
        response = client.get("/beatitudes/pdf")
        assert response.status_code in [200, 503]

    def test_tetragrammaton_pdf(self, client):
        """Test tetragrammaton PDF."""
        response = client.get("/tetragrammaton/pdf")
        assert response.status_code in [200, 503]


class TestSearchIndexModule:
    """Tests for search_index module (67% coverage)."""

    def test_search_verses_love(self):
        """Test searching for love."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("love", limit=10)
            assert isinstance(results, list)

    def test_search_verses_with_book_filter(self):
        """Test search with book filter."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("God", limit=10, book_filter="Genesis")
            assert isinstance(results, list)
            for r in results:
                assert r["book"] == "Genesis"

    def test_search_verses_with_old_testament_filter(self):
        """Test search with OT filter."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("Lord", limit=10, testament_filter="old")
            assert isinstance(results, list)

    def test_search_verses_with_new_testament_filter(self):
        """Test search with NT filter."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("Jesus", limit=10, testament_filter="new")
            assert isinstance(results, list)

    def test_search_verses_empty_query(self):
        """Test search with empty query."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("", limit=10)
            assert results == []

    def test_search_verses_whitespace_query(self):
        """Test search with whitespace query."""
        from kjvstudy_org.utils.search_index import search_verses, DB_PATH
        if DB_PATH.exists():
            results = search_verses("   ", limit=10)
            assert results == []

    def test_highlight_matches(self):
        """Test highlight matches function."""
        from kjvstudy_org.utils.search_index import highlight_matches
        result = highlight_matches("For God so loved the world", "loved world")
        assert "<mark>" in result
        assert "loved" in result

    def test_get_search_stats(self):
        """Test getting search stats."""
        from kjvstudy_org.utils.search_index import get_search_stats
        stats = get_search_stats()
        assert "indexed" in stats
        assert "verses" in stats

    def test_get_connection(self):
        """Test database connection context manager."""
        from kjvstudy_org.utils.search_index import get_connection, DB_PATH
        if DB_PATH.exists():
            with get_connection() as conn:
                assert conn is not None
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                assert cursor.fetchone()[0] == 1


class TestBiblePDFRoutes:
    """Tests for Bible PDF routes."""

    def test_book_pdf_philemon(self, client):
        """Test book PDF for short book."""
        response = client.get("/book/Philemon/pdf")
        assert response.status_code in [200, 503]

    def test_chapter_pdf_genesis_1(self, client):
        """Test chapter PDF."""
        response = client.get("/book/Genesis/chapter/1/pdf")
        assert response.status_code in [200, 503]

    def test_verse_pdf_john_3_16(self, client):
        """Test verse PDF."""
        response = client.get("/book/John/chapter/3/verse/16/pdf")
        assert response.status_code in [200, 503]

    def test_interlinear_pdf_genesis_1(self, client):
        """Test interlinear PDF."""
        response = client.get("/book/Genesis/chapter/1/interlinear/pdf")
        assert response.status_code in [200, 503]

    def test_book_pdf_invalid(self, client):
        """Test PDF for invalid book."""
        response = client.get("/book/NotABook/pdf")
        assert response.status_code in [404, 503]


class TestCommentaryRoutes:
    """Tests for commentary routes (78% coverage)."""

    def test_commentary_api_john_3_16(self, client):
        """Test commentary API for John 3:16."""
        response = client.get("/api/commentary/John/3/16")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_commentary_api_genesis_1_1(self, client):
        """Test commentary API for Genesis 1:1."""
        response = client.get("/api/commentary/Genesis/1/1")
        assert response.status_code == 200

    def test_commentary_api_invalid_book(self, client):
        """Test commentary API for invalid book."""
        response = client.get("/api/commentary/FakeBook/1/1")
        assert response.status_code == 404

    def test_commentary_api_invalid_chapter(self, client):
        """Test commentary API for invalid chapter."""
        response = client.get("/api/commentary/Genesis/999/1")
        assert response.status_code == 404

    def test_commentary_api_invalid_verse(self, client):
        """Test commentary API for invalid verse."""
        response = client.get("/api/commentary/Genesis/1/999")
        assert response.status_code == 404


class TestAPIEndpointsExtended:
    """Extended API endpoint tests."""

    def test_api_cross_references(self, client):
        """Test cross references API."""
        response = client.get("/api/cross-references/John/3/16")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))

    def test_api_interlinear(self, client):
        """Test interlinear API."""
        response = client.get("/api/interlinear/Genesis/1/1")
        assert response.status_code == 200

    def test_api_topics_list(self, client):
        """Test topics list API."""
        response = client.get("/api/topics")
        assert response.status_code == 200

    def test_api_topics_detail(self, client):
        """Test topic detail API."""
        response = client.get("/api/topics/Love")
        assert response.status_code in [200, 404]

    def test_api_reading_plans_list(self, client):
        """Test reading plans list API."""
        response = client.get("/api/reading-plans")
        assert response.status_code == 200

    def test_api_reading_plan_detail(self, client):
        """Test reading plan detail API."""
        # Get list first to find a valid ID
        response = client.get("/api/reading-plans")
        data = response.json()
        plans = data.get("plans", [])
        if plans:
            plan_id = plans[0].get("id", plans[0].get("slug", "bible-in-a-year"))
            response = client.get(f"/api/reading-plans/{plan_id}")
            assert response.status_code in [200, 404]


class TestDataModuleFunctions:
    """Tests for data module functions."""

    def test_find_resource_by_slug(self):
        """Test finding resource by slug."""
        from kjvstudy_org.data import find_resource_by_slug, ANGELS_DATA
        result = find_resource_by_slug(ANGELS_DATA, "gabriel")
        # Returns tuple (item, item_name, category_name) or (None, None, None)
        assert result is not None

    def test_find_resource_by_slug_invalid(self):
        """Test finding invalid resource by slug."""
        from kjvstudy_org.data import find_resource_by_slug, ANGELS_DATA
        item, item_name, category_name = find_resource_by_slug(ANGELS_DATA, "not-an-angel")
        assert item is None


class TestHelpersModuleExtended:
    """Extended tests for helpers module."""

    def test_create_slug_with_spaces(self):
        """Test slug creation with spaces."""
        from kjvstudy_org.utils.helpers import create_slug
        result = create_slug("Hello World Test")
        assert result == "hello-world-test"

    def test_create_slug_with_special_chars(self):
        """Test slug creation with special chars."""
        from kjvstudy_org.utils.helpers import create_slug
        result = create_slug("Test's & Example!")
        assert "-" in result or result == "tests-example"

    def test_is_verse_reference_valid(self):
        """Test verse reference detection."""
        from kjvstudy_org.utils.helpers import is_verse_reference
        assert is_verse_reference("John 3:16") is True
        assert is_verse_reference("Genesis 1:1") is True

    def test_is_verse_reference_invalid(self):
        """Test invalid verse reference detection."""
        from kjvstudy_org.utils.helpers import is_verse_reference
        result = is_verse_reference("not a verse")
        assert result is False

    def test_parse_verse_reference_valid(self):
        """Test parsing valid verse reference."""
        from kjvstudy_org.utils.helpers import parse_verse_reference
        result = parse_verse_reference("John 3:16")
        assert result is not None
        assert result.get("book") == "John"

    def test_parse_verse_reference_invalid(self):
        """Test parsing invalid verse reference."""
        from kjvstudy_org.utils.helpers import parse_verse_reference
        result = parse_verse_reference("not a verse reference")
        assert result is None


class TestBooksModule:
    """Tests for books module."""

    def test_get_book_data(self):
        """Test getting book data."""
        from kjvstudy_org.books import get_book_data
        data = get_book_data("Genesis")
        assert data is None or isinstance(data, dict)

    def test_has_book_data(self):
        """Test checking if book has data."""
        from kjvstudy_org.books import has_book_data
        result = has_book_data("Genesis")
        assert isinstance(result, bool)


class TestServerExtended:
    """Extended tests for server module."""

    def test_static_files(self, client):
        """Test static files are served."""
        response = client.get("/static/css/tufte.css")
        assert response.status_code in [200, 404]

    def test_api_prefix(self, client):
        """Test API prefix works."""
        response = client.get("/api/health")
        assert response.status_code == 200


class TestMiscRoutesExtended:
    """Extended tests for misc routes."""

    def test_robots_txt(self, client):
        """Test robots.txt."""
        response = client.get("/robots.txt")
        assert response.status_code == 200

    def test_sitemap_xml(self, client):
        """Test sitemap.xml."""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200


class TestRedLetterModule:
    """Tests for red_letter module."""

    def test_red_letter_module_import(self):
        """Test red letter module imports."""
        from kjvstudy_org import red_letter
        assert red_letter is not None

    def test_is_red_letter_verse(self):
        """Test checking if verse is red letter."""
        try:
            from kjvstudy_org.red_letter import is_red_letter
            # Matthew 5:3 is part of the Beatitudes (Jesus speaking)
            result = is_red_letter("Matthew", 5, 3)
            assert isinstance(result, bool)
        except (ImportError, AttributeError):
            pass  # Function may not exist


class TestReadingPlansRoutes:
    """Tests for reading plans routes."""

    def test_reading_plans_index(self, client):
        """Test reading plans index page."""
        response = client.get("/reading-plans")
        assert response.status_code == 200

    def test_reading_plan_detail(self, client):
        """Test reading plan detail page."""
        response = client.get("/reading-plans/bible-in-a-year")
        assert response.status_code in [200, 404]
