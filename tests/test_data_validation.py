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

from scripts.validate_data import validate_file, validate_book_file, MODEL_MAPPING, DATA_DIR


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

    def test_red_letter_verses_structure(self):
        """Test that red_letter_verses.json has correct structure."""
        assert validate_file("red_letter_verses.json")


class TestBookValidation:
    """Test validation of 66 book introduction files."""

    def test_books_directory_exists(self):
        """Test that the books directory exists."""
        books_dir = DATA_DIR / "books"
        assert books_dir.exists(), f"Books directory not found: {books_dir}"

    def test_all_66_books_exist(self):
        """Test that all 66 book files exist."""
        books_dir = DATA_DIR / "books"
        book_files = list(books_dir.glob("*.json"))
        assert len(book_files) == 66, f"Expected 66 book files, found {len(book_files)}"

    def test_validate_all_book_files(self):
        """Test that all 66 book files validate against BookIntroduction schema."""
        books_dir = DATA_DIR / "books"
        book_files = sorted(books_dir.glob("*.json"))

        failed_books = []
        for book_file in book_files:
            if not validate_book_file(book_file):
                failed_books.append(book_file.name)

        assert len(failed_books) == 0, f"The following books failed validation: {', '.join(failed_books)}"

    def test_sample_books(self):
        """Test specific book files to ensure proper validation."""
        books_to_test = ["genesis.json", "john.json", "revelation.json"]
        books_dir = DATA_DIR / "books"

        for book_name in books_to_test:
            book_file = books_dir / book_name
            assert book_file.exists(), f"{book_name} not found"
            assert validate_book_file(book_file), f"{book_name} failed validation"
