"""Tests for sitemap, robots.txt, and utility endpoints."""
import time
import xml.etree.ElementTree as ET
import pytest


class TestSitemap:
    """Tests for sitemap.xml generation"""

    def test_sitemap_exists(self, client):
        """Sitemap should return 200 and valid XML"""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/xml"

    def test_sitemap_valid_xml(self, client):
        """Sitemap index should be valid XML that can be parsed"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Should be parseable XML
        try:
            root = ET.fromstring(content)
            assert root.tag.endswith("sitemapindex"), "Root element should be sitemapindex"
        except ET.ParseError as e:
            pytest.fail(f"Sitemap is not valid XML: {e}")

    @pytest.mark.skip(reason="Performance test - flaky depending on system load")
    def test_sitemap_performance(self, client):
        """Sitemap should generate quickly (under 1 second)"""
        start_time = time.time()
        response = client.get("/sitemap.xml")
        duration = time.time() - start_time

        assert response.status_code == 200
        assert duration < 1.0, f"Sitemap took {duration:.2f}s to generate (should be <1s)"

    def test_sitemap_index_references(self, client):
        """Sitemap index should reference both main and verse sitemaps"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Should reference both sitemaps
        assert "sitemap-main.xml" in content, "Should reference main sitemap"
        assert "sitemap-verses.xml" in content, "Should reference verse sitemap"

        # Count <sitemap> tags
        sitemap_count = content.count("<sitemap>")
        assert sitemap_count == 2, f"Should have exactly 2 sitemap references, found {sitemap_count}"

    def test_sitemap_main_contains_critical_urls(self, client):
        """Main sitemap should include critical pages"""
        response = client.get("/sitemap-main.xml")
        content = response.content.decode("utf-8")

        critical_urls = [
            "https://kjvstudy.org/",
            "https://kjvstudy.org/books",
            "https://kjvstudy.org/search",
            "https://kjvstudy.org/topics",
            "https://kjvstudy.org/reading-plans",
            "https://kjvstudy.org/resources",
        ]

        for url in critical_urls:
            assert url in content, f"Main sitemap missing critical URL: {url}"

    def test_sitemap_main_contains_book_urls(self, client):
        """Main sitemap should include book URLs"""
        response = client.get("/sitemap-main.xml")
        content = response.content.decode("utf-8")

        # Check for some book URLs
        assert "https://kjvstudy.org/book/Genesis" in content
        assert "https://kjvstudy.org/book/John" in content
        assert "https://kjvstudy.org/book/Revelation" in content

    def test_sitemap_main_contains_chapter_urls(self, client):
        """Main sitemap should include chapter URLs"""
        response = client.get("/sitemap-main.xml")
        content = response.content.decode("utf-8")

        # Check for some chapter URLs
        assert "https://kjvstudy.org/book/Genesis/chapter/1" in content
        assert "https://kjvstudy.org/book/John/chapter/3" in content

    def test_sitemap_main_excludes_verse_urls(self, client):
        """Main sitemap should NOT include individual verse URLs"""
        response = client.get("/sitemap-main.xml")
        content = response.content.decode("utf-8")

        # Should NOT contain individual verse URLs
        assert "/verse/1</loc>" not in content, "Main sitemap should exclude verse URLs"

    def test_sitemap_verses_contains_verse_urls(self, client):
        """Verse sitemap should include individual verse URLs"""
        response = client.get("/sitemap-verses.xml")
        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Should contain verse URLs
        assert "https://kjvstudy.org/book/Genesis/chapter/1/verse/1" in content
        assert "https://kjvstudy.org/book/John/chapter/3/verse/16" in content

        # Count verse URLs (should be 31,102)
        verse_count = content.count("/verse/")
        assert verse_count > 30000, f"Verse sitemap should have ~31k verses, found {verse_count}"

    def test_sitemap_caching(self, client):
        """Sitemap should return the same content on repeated requests (cache working)"""
        response1 = client.get("/sitemap.xml")
        response2 = client.get("/sitemap.xml")

        assert response1.content == response2.content
        assert response1.status_code == 200
        assert response2.status_code == 200


class TestRobotsTxt:
    """Tests for robots.txt"""

    def test_robots_txt_exists(self, client):
        """Robots.txt should exist and return 200"""
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

    def test_robots_txt_content(self, client):
        """Robots.txt should have proper directives"""
        response = client.get("/robots.txt")
        content = response.content.decode("utf-8")

        assert "User-agent: *" in content
        assert "Allow: /" in content
        assert "Sitemap: https://kjvstudy.org/sitemap.xml" in content

    def test_robots_txt_disallows_api(self, client):
        """Robots.txt should disallow /api/ endpoints"""
        response = client.get("/robots.txt")
        content = response.content.decode("utf-8")

        assert "Disallow: /api/" in content


class TestHealthCheck:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Health check should aggregate readiness checks and pass"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"
        assert data["checks"]["bible"]["status"] == "ok"
        assert data["checks"]["books"]["status"] == "ok"
