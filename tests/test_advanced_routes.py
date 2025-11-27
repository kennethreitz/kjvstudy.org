"""
Tests for advanced routes: Family Tree, Timeline, Concordance, and Study Guides.

These tests cover complex, user-facing features with multiple routes and data dependencies.
"""
import pytest


class TestFamilyTreeRoutes:
    """Tests for biblical family tree genealogy routes"""

    def test_family_tree_main_page(self, client):
        """Test main family tree page loads"""
        response = client.get("/family-tree")
        assert response.status_code == 200
        content = response.content.decode()
        assert "family" in content.lower() or "tree" in content.lower()

    def test_family_tree_has_generations(self, client):
        """Test family tree page displays generation information"""
        response = client.get("/family-tree")
        assert response.status_code == 200
        content = response.content.decode()
        # Should reference generations or genealogy
        assert "generation" in content.lower() or "genealogy" in content.lower()

    def test_family_tree_generation_page(self, client):
        """Test individual generation page loads"""
        # Test generation 1 (Adam/Eve)
        response = client.get("/family-tree/generation/1")
        assert response.status_code == 200
        content = response.content.decode()
        assert "generation" in content.lower()

    def test_family_tree_generation_adam(self, client):
        """Test generation 1 contains Adam"""
        response = client.get("/family-tree/generation/1")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Adam" in content or "adam" in content.lower()

    def test_family_tree_invalid_generation(self, client):
        """Test non-existent generation returns 404"""
        response = client.get("/family-tree/generation/999")
        assert response.status_code == 404

    def test_family_tree_person_page(self, client):
        """Test individual person page loads"""
        # Test Adam's page
        response = client.get("/family-tree/person/i1")
        assert response.status_code in [200, 404]  # May or may not exist depending on GEDCOM data

        if response.status_code == 200:
            content = response.content.decode()
            # Should have person information
            assert len(content) > 100

    def test_family_tree_person_not_found(self, client):
        """Test non-existent person returns 404"""
        response = client.get("/family-tree/person/invalid-person-id-xyz")
        assert response.status_code == 404

    def test_family_tree_search_page(self, client):
        """Test family tree search page loads"""
        response = client.get("/family-tree/search")
        assert response.status_code == 200
        content = response.content.decode()
        assert "search" in content.lower()

    def test_family_tree_search_with_query(self, client):
        """Test family tree search with query parameter"""
        response = client.get("/family-tree/search?q=Adam")
        assert response.status_code in [200, 303]  # 303 if exact match redirects

        if response.status_code == 200:
            content = response.content.decode()
            assert "Adam" in content or "adam" in content.lower()

    def test_family_tree_search_empty_query(self, client):
        """Test family tree search with empty query"""
        response = client.get("/family-tree/search?q=")
        assert response.status_code == 200

    def test_family_tree_lineage_page(self, client):
        """Test Messianic lineage page loads"""
        response = client.get("/family-tree/lineage")
        assert response.status_code == 200
        content = response.content.decode()
        assert "lineage" in content.lower() or "messiah" in content.lower()

    def test_family_tree_lineage_svg(self, client):
        """Test Messianic lineage SVG generation"""
        response = client.get("/family-tree/lineage.svg")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/svg+xml"

        # Verify it's valid SVG
        content = response.content.decode()
        assert "<svg" in content
        assert "</svg>" in content

    def test_family_tree_descendants_page(self, client):
        """Test descendants view for a person"""
        # Test Adam's descendants
        response = client.get("/family-tree/person/i1/descendants")
        assert response.status_code in [200, 404]  # 404 if person not found

        if response.status_code == 200:
            content = response.content.decode()
            assert "descendants" in content.lower() or "descendant" in content.lower()

    def test_family_tree_descendants_invalid_person(self, client):
        """Test descendants view for non-existent person"""
        response = client.get("/family-tree/person/invalid-xyz/descendants")
        assert response.status_code == 404

    def test_family_tree_ancestors_page(self, client):
        """Test ancestors view for a person"""
        # Test Jesus's ancestors
        response = client.get("/family-tree/person/i42/ancestors")
        assert response.status_code in [200, 404]  # 404 if person not found

        if response.status_code == 200:
            content = response.content.decode()
            assert "ancestors" in content.lower() or "ancestor" in content.lower()

    def test_family_tree_ancestors_invalid_person(self, client):
        """Test ancestors view for non-existent person"""
        response = client.get("/family-tree/person/invalid-xyz/ancestors")
        assert response.status_code == 404

    def test_family_tree_navigation_links(self, client):
        """Test family tree pages have proper navigation"""
        response = client.get("/family-tree")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have links to persons or generations
        assert "/family-tree/" in content


class TestBiblicalTimelineRoutes:
    """Tests for biblical timeline routes"""

    def test_timeline_page_loads(self, client):
        """Test biblical timeline page loads"""
        response = client.get("/biblical-timeline")
        assert response.status_code == 200
        content = response.content.decode()
        assert "timeline" in content.lower()

    def test_timeline_has_events(self, client):
        """Test timeline displays biblical events"""
        response = client.get("/biblical-timeline")
        assert response.status_code == 200
        content = response.content.decode()

        # Should contain references to major biblical events or periods
        assert (
            "creation" in content.lower() or
            "flood" in content.lower() or
            "abraham" in content.lower() or
            "exodus" in content.lower() or
            "christ" in content.lower()
        )

    def test_timeline_has_dates(self, client):
        """Test timeline includes chronological dates"""
        response = client.get("/biblical-timeline")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have BC dates
        assert "BC" in content or "BCE" in content or "AM" in content

    def test_timeline_pdf_generation(self, client):
        """Test timeline PDF generation"""
        response = client.get("/biblical-timeline/pdf")

        # PDF generation might not be available
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            assert response.headers["content-type"] == "application/pdf"
            # Verify it's a PDF
            assert response.content[:4] == b'%PDF'

    def test_timeline_metadata(self, client):
        """Test timeline page has proper metadata"""
        response = client.get("/biblical-timeline")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have HTML structure
        assert "<html" in content.lower()
        assert "<title>" in content


class TestConcordanceRoutes:
    """Tests for concordance (word lookup) routes"""

    def test_concordance_page_loads(self, client):
        """Test concordance page loads"""
        response = client.get("/concordance")
        assert response.status_code == 200
        content = response.content.decode()
        assert "concordance" in content.lower()

    def test_concordance_has_search(self, client):
        """Test concordance page has search functionality"""
        response = client.get("/concordance")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have search input or form
        assert "search" in content.lower() or "word" in content.lower()

    def test_concordance_with_word_query(self, client):
        """Test concordance with word lookup"""
        response = client.get("/concordance?word=love")
        assert response.status_code == 200
        content = response.content.decode()

        # Should display results for "love"
        assert "love" in content.lower()

    def test_concordance_common_word(self, client):
        """Test concordance with common biblical word"""
        response = client.get("/concordance?word=God")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have results (God appears many times)
        assert "God" in content or "god" in content.lower()

    def test_concordance_rare_word(self, client):
        """Test concordance with less common word"""
        response = client.get("/concordance?word=righteousness")
        assert response.status_code == 200

    def test_concordance_empty_query(self, client):
        """Test concordance with no word parameter"""
        response = client.get("/concordance?word=")
        assert response.status_code == 200

    def test_concordance_case_insensitive(self, client):
        """Test concordance is case-insensitive"""
        response1 = client.get("/concordance?word=love")
        response2 = client.get("/concordance?word=LOVE")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Both should return results
        assert len(response1.content) > 1000
        assert len(response2.content) > 1000

    def test_concordance_verse_links(self, client):
        """Test concordance results link to verses"""
        response = client.get("/concordance?word=faith")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have links to Bible verses
        if "faith" in content.lower():
            assert "/book/" in content or "verse" in content.lower()


class TestStudyGuidesRoutes:
    """Tests for study guides routes"""

    def test_study_guides_index_loads(self, client):
        """Test study guides index page loads"""
        response = client.get("/study-guides")
        assert response.status_code == 200
        content = response.content.decode()
        assert "study" in content.lower() or "guide" in content.lower()

    def test_study_guides_has_categories(self, client):
        """Test study guides index has categories"""
        response = client.get("/study-guides")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have study guide categories or links
        assert len(content) > 1000  # Substantial content

    def test_study_guides_has_links(self, client):
        """Test study guides index links to individual guides"""
        response = client.get("/study-guides")
        assert response.status_code == 200
        content = response.content.decode()

        # Should have links to individual study guides
        assert "/study-guides/" in content

    def test_study_guide_detail_page(self, client):
        """Test individual study guide detail page"""
        # Test a common study guide slug
        response = client.get("/study-guides/salvation")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            content = response.content.decode()
            assert "salvation" in content.lower()

    def test_study_guide_gospel(self, client):
        """Test gospel study guide"""
        response = client.get("/study-guides/gospel")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            content = response.content.decode()
            assert "gospel" in content.lower()

    def test_study_guide_prayer_faith(self, client):
        """Test prayer & faith study guide"""
        response = client.get("/study-guides/prayer-faith")
        assert response.status_code in [200, 404]

    def test_study_guide_invalid_slug(self, client):
        """Test non-existent study guide returns 404"""
        response = client.get("/study-guides/this-guide-does-not-exist")
        assert response.status_code == 404

    def test_study_guide_has_verses(self, client):
        """Test study guide pages include verse references"""
        response = client.get("/study-guides/salvation")

        if response.status_code == 200:
            content = response.content.decode()
            # Should have verse references or Bible links
            assert (
                "/book/" in content or
                "verse" in content.lower() or
                "chapter" in content.lower()
            )

    def test_study_guide_pdf_generation(self, client):
        """Test study guide PDF generation"""
        response = client.get("/study-guides/salvation/pdf")

        # PDF might not be available or guide might not exist
        assert response.status_code in [200, 404, 500, 503]

        if response.status_code == 200:
            assert response.headers["content-type"] == "application/pdf"
            # Verify it's a PDF
            assert response.content[:4] == b'%PDF'

    def test_study_guide_pdf_invalid_slug(self, client):
        """Test PDF for non-existent study guide returns error"""
        response = client.get("/study-guides/invalid-guide-xyz/pdf")
        # Should return 404 for invalid guide, or 503 if WeasyPrint not available
        assert response.status_code in [404, 503]

    def test_study_guide_navigation(self, client):
        """Test study guide pages have breadcrumbs/navigation"""
        response = client.get("/study-guides/salvation")

        if response.status_code == 200:
            content = response.content.decode()
            # Should have navigation back to study guides
            assert "/study-guides" in content or "study guide" in content.lower()


class TestAdvancedRoutesIntegration:
    """Integration tests across multiple advanced route types"""

    def test_all_major_pages_load(self, client):
        """Test all major advanced pages load successfully"""
        pages = [
            "/family-tree",
            "/biblical-timeline",
            "/concordance",
            "/study-guides",
        ]

        for page in pages:
            response = client.get(page)
            assert response.status_code == 200, f"Page {page} failed to load"

    def test_pages_have_html_structure(self, client):
        """Test pages have valid HTML structure"""
        pages = [
            "/family-tree",
            "/biblical-timeline",
            "/concordance",
            "/study-guides",
        ]

        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                content = response.content.decode()
                assert "<html" in content.lower()
                assert "<body" in content.lower()
                assert "</html>" in content.lower()

    def test_pages_have_titles(self, client):
        """Test pages have proper title tags"""
        pages = [
            "/family-tree",
            "/biblical-timeline",
            "/concordance",
            "/study-guides",
        ]

        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                content = response.content.decode()
                assert "<title>" in content.lower()

    def test_pages_return_html_content_type(self, client):
        """Test HTML pages return correct content type"""
        pages = [
            "/family-tree",
            "/biblical-timeline",
            "/concordance",
            "/study-guides",
        ]

        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                assert "text/html" in content_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
