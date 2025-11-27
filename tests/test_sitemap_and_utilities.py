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
        """Sitemap should be valid XML that can be parsed"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Should be parseable XML
        try:
            root = ET.fromstring(content)
            assert root.tag.endswith("urlset")
        except ET.ParseError as e:
            pytest.fail(f"Sitemap is not valid XML: {e}")

    def test_sitemap_performance(self, client):
        """Sitemap should generate quickly (under 1 second)"""
        start_time = time.time()
        response = client.get("/sitemap.xml")
        duration = time.time() - start_time

        assert response.status_code == 200
        assert duration < 1.0, f"Sitemap took {duration:.2f}s to generate (should be <1s)"

    def test_sitemap_url_count(self, client):
        """Sitemap should stay under Google's 50k URL recommendation"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Count <url> tags
        url_count = content.count("<url>")
        assert url_count > 0, "Sitemap should contain URLs"
        assert url_count < 50000, f"Sitemap has {url_count} URLs (should be <50k for Google)"

        # Verify it's a reasonable number (not all 31k verses)
        assert url_count < 5000, f"Sitemap has {url_count} URLs (seems too high - did you include all verses?)"

    def test_sitemap_contains_critical_urls(self, client):
        """Sitemap should include critical pages"""
        response = client.get("/sitemap.xml")
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
            assert url in content, f"Sitemap missing critical URL: {url}"

    def test_sitemap_contains_book_urls(self, client):
        """Sitemap should include book URLs"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Check for some book URLs
        assert "https://kjvstudy.org/book/Genesis" in content
        assert "https://kjvstudy.org/book/John" in content
        assert "https://kjvstudy.org/book/Revelation" in content

    def test_sitemap_contains_chapter_urls(self, client):
        """Sitemap should include chapter URLs"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Check for some chapter URLs
        assert "https://kjvstudy.org/book/Genesis/chapter/1" in content
        assert "https://kjvstudy.org/book/John/chapter/3" in content

    def test_sitemap_excludes_verse_urls(self, client):
        """Sitemap should NOT include individual verse URLs (too many)"""
        response = client.get("/sitemap.xml")
        content = response.content.decode("utf-8")

        # Should NOT contain individual verse URLs
        assert "/verse/1</loc>" not in content, "Sitemap should exclude individual verse URLs"

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
        """Health check should return healthy status"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "kjv-study"
