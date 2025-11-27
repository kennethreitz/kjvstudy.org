"""
Tests for JSON data file validation using Pydantic models.

This test suite ensures all JSON data files conform to their schemas,
catching data integrity issues early in development.
"""

import pytest
from pathlib import Path

# Import validation script
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate_data import validate_file, MODEL_MAPPING


class TestDataValidation:
    """Test data file validation using Pydantic models."""

    @pytest.mark.parametrize("data_file", MODEL_MAPPING.keys())
    def test_validate_data_file(self, data_file):
        """Test that each data file validates against its Pydantic model."""
        assert validate_file(data_file), f"{data_file} failed validation"

    def test_bible_metadata_structure(self):
        """Test that bible_metadata.json has correct structure."""
        assert validate_file("bible_metadata.json")

    def test_word_studies_structure(self):
        """Test that word_studies.json has correct structure."""
        assert validate_file("word_studies.json")

    def test_study_guides_structure(self):
        """Test that study_guides.json has correct structure."""
        assert validate_file("study_guides.json")

    def test_verse_commentary_structure(self):
        """Test that verse_commentary.json has correct structure."""
        assert validate_file("verse_commentary.json")

    def test_featured_verses_structure(self):
        """Test that featured_verses.json has correct structure."""
        assert validate_file("featured_verses.json")

    def test_resource_slugs_structure(self):
        """Test that resource_slugs.json has correct structure."""
        assert validate_file("resource_slugs.json")
