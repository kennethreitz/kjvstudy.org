#!/usr/bin/env python3
"""
Validate JSON data files using Pydantic models.

This script validates all data files in kjvstudy_org/data/ using Pydantic models
for type safety and validation. Pydantic provides better error messages and
integrates naturally with FastAPI.

Usage:
    python scripts/validate_data.py              # Validate all files
    python scripts/validate_data.py --file bible_metadata.json  # Validate specific file
    python scripts/validate_data.py --verbose    # Show detailed output
    python scripts/validate_data.py --generate-schemas  # Generate JSON schemas

Requirements:
    pip install pydantic (already installed with FastAPI)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from pydantic import BaseModel, RootModel, Field, field_validator, ValidationError
except ImportError:
    print("Error: pydantic package not found")
    print("Install with: pip install pydantic")
    sys.exit(1)

# Path to data directory
DATA_DIR = Path(__file__).parent.parent / "kjvstudy_org" / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"


# ============================================================================
# Pydantic Models for Data Validation
# ============================================================================

class BibleMetadata(BaseModel):
    """Schema for bible_metadata.json"""
    old_testament_books: List[str] = Field(..., min_length=39, max_length=39)
    new_testament_books: List[str] = Field(..., min_length=27, max_length=27)
    book_abbreviations: Dict[str, str] = Field(..., min_length=1)

    @field_validator('old_testament_books', 'new_testament_books')
    @classmethod
    def check_unique_books(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("Duplicate book names found")
        return v


class WordStudy(BaseModel):
    """Schema for individual word study entry"""
    ot_term: Optional[str] = Field(None, min_length=1)
    ot_transliteration: Optional[str] = Field(None, min_length=1)
    ot_meaning: Optional[str] = Field(None, min_length=1)
    ot_note: Optional[str] = Field(None, min_length=1)
    nt_term: Optional[str] = Field(None, min_length=1)
    nt_transliteration: Optional[str] = Field(None, min_length=1)
    nt_meaning: Optional[str] = Field(None, min_length=1)
    nt_note: Optional[str] = Field(None, min_length=1)


class WordStudies(RootModel[Dict[str, WordStudy]]):
    """Schema for word_studies.json"""
    root: Dict[str, WordStudy]


class CatalogEntry(BaseModel):
    """Schema for study guide catalog entry"""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    slug: str = Field(..., pattern=r'^[a-z-]+$')
    verses: List[str]

    @field_validator('verses')
    @classmethod
    def check_verse_format(cls, v):
        import re
        pattern = r'^[A-Za-z0-9 ]+ \d+:\d+(-\d+)?$'
        for verse in v:
            if not re.match(pattern, verse):
                raise ValueError(f"Invalid verse reference format: {verse}")
        return v


class StudySection(BaseModel):
    """Schema for study guide section"""
    title: str = Field(..., min_length=1)
    verses: List[str]
    content: str = Field(..., min_length=1)

    @field_validator('verses')
    @classmethod
    def check_verse_format(cls, v):
        import re
        pattern = r'^[A-Za-z0-9 ]+ \d+:\d+(-\d+)?$'
        for verse in v:
            if not re.match(pattern, verse):
                raise ValueError(f"Invalid verse reference format: {verse}")
        return v


class GuideContent(BaseModel):
    """Schema for study guide content"""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    sections: List[StudySection] = Field(..., min_length=1)


class StudyGuides(BaseModel):
    """Schema for study_guides.json"""
    catalog: Dict[str, List[CatalogEntry]]
    content: Dict[str, GuideContent]


class VerseCommentaryEntry(BaseModel):
    """Schema for verse commentary entry"""
    analysis: str = Field(..., min_length=1)
    historical: str = Field(..., min_length=1)
    questions: List[str] = Field(..., min_length=1)


class VersesDict(RootModel[Dict[str, VerseCommentaryEntry]]):
    """Dictionary of verse numbers to commentary entries"""
    root: Dict[str, VerseCommentaryEntry]


class ChaptersDict(RootModel[Dict[str, VersesDict]]):
    """Dictionary of chapter numbers to verses"""
    root: Dict[str, VersesDict]


class VerseCommentary(RootModel[Dict[str, ChaptersDict]]):
    """Schema for verse_commentary.json - nested structure: Book -> Chapter -> Verse -> Commentary"""
    root: Dict[str, ChaptersDict]


class FeaturedVerse(BaseModel):
    """Schema for individual featured verse"""
    book: str = Field(..., min_length=1)
    chapter: int = Field(..., ge=1)
    verse: int = Field(..., ge=1)


class FeaturedVerses(BaseModel):
    """Schema for featured_verses.json"""
    verses: List[FeaturedVerse] = Field(..., min_length=1)


class RedLetterVerses(BaseModel):
    """Schema for red_letter_verses.json"""
    description: str = Field(..., min_length=1)
    note: str = Field(..., min_length=1)
    verses: Dict[str, str] = Field(..., min_length=1)

    @field_validator('verses')
    @classmethod
    def check_verses(cls, v):
        import re
        # Validate verse reference format
        pattern = r"^[A-Za-z0-9 ']+ \d+:\d+$"
        for key, value in v.items():
            if not re.match(pattern, key):
                raise ValueError(f"Invalid verse reference key: {key}")
            # Value must be either "full" or a non-empty string
            if value != "full" and (not isinstance(value, str) or len(value) == 0):
                raise ValueError(f"Invalid value for {key}: must be 'full' or a non-empty string")
        return v


class ResourceSlugs(BaseModel):
    """Schema for resource_slugs.json"""
    study_guides: List[str]
    angels: List[str]
    prophets: List[str]
    names_of_god: List[str]
    parables: List[str]
    covenants: List[str]
    apostles: List[str]
    women: List[str]
    festivals: List[str]
    fruits_of_spirit: List[str]

    @field_validator('*')
    @classmethod
    def check_slugs(cls, v):
        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError("Duplicate slugs found")
        # Check slug format
        import re
        pattern = r'^[a-z-]+$'
        for slug in v:
            if not re.match(pattern, slug):
                raise ValueError(f"Invalid slug format: {slug}")
        return v


class OutlineSection(BaseModel):
    """Schema for book outline section"""
    section: str = Field(..., min_length=1)
    chapters: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class KeyTheme(BaseModel):
    """Schema for book key theme"""
    theme: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class KeyVerse(BaseModel):
    """Schema for book key verse"""
    reference: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class BookIntroduction(BaseModel):
    """Schema for individual book introduction file"""
    name: str = Field(..., min_length=1)
    abbreviation: str = Field(..., min_length=1)
    testament: str = Field(..., pattern=r'^(Old Testament|New Testament)$')
    position: int = Field(..., ge=1, le=66)
    chapters: int = Field(..., ge=1)
    category: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    date_written: str = Field(..., min_length=1)
    introduction: str = Field(..., min_length=1)
    outline: List[OutlineSection] = Field(..., min_length=1)
    key_themes: List[KeyTheme] = Field(..., min_length=1)
    key_verses: List[KeyVerse] = Field(..., min_length=1)
    christ_in_book: Optional[str] = None


# ============================================================================
# Validation Logic
# ============================================================================

# Mapping of data files to their Pydantic models
MODEL_MAPPING = {
    "bible_metadata.json": BibleMetadata,
    "word_studies.json": WordStudies,
    "study_guides.json": StudyGuides,
    "verse_commentary.json": VerseCommentary,
    "featured_verses.json": FeaturedVerses,
    "red_letter_verses.json": RedLetterVerses,
    "resource_slugs.json": ResourceSlugs,
}


def load_json(file_path: Path) -> Tuple[dict, Optional[str]]:
    """Load JSON file and return data and error message if any."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"JSON syntax error: {e}"
    except Exception as e:
        return None, f"Error loading file: {e}"


def validate_file(data_file: str, verbose: bool = False) -> bool:
    """Validate a single data file using its Pydantic model."""
    if data_file not in MODEL_MAPPING:
        if verbose:
            print(f"⚠️  {data_file}: No validation model defined (skipped)")
        return True

    model_class = MODEL_MAPPING[data_file]
    data_path = DATA_DIR / data_file

    # Check if file exists
    if not data_path.exists():
        print(f"❌ {data_file}: File not found at {data_path}")
        return False

    # Load data file
    data, error = load_json(data_path)
    if error:
        print(f"❌ {data_file}: {error}")
        return False

    # Validate using Pydantic model
    try:
        # For RootModel subclasses, pass data directly to constructor
        # For regular BaseModel subclasses, unpack as kwargs
        if issubclass(model_class, RootModel):
            model_class(data)
        else:
            model_class(**data)

        print(f"✅ {data_file}: Valid")
        if verbose:
            print(f"   Model: {model_class.__name__}")
            print(f"   Size: {data_path.stat().st_size:,} bytes")
        return True

    except ValidationError as e:
        print(f"❌ {data_file}: Validation failed")
        for error_detail in e.errors():
            location = " -> ".join(str(loc) for loc in error_detail['loc'])
            print(f"   {location}: {error_detail['msg']}")
            if verbose and 'ctx' in error_detail:
                print(f"   Context: {error_detail['ctx']}")
        return False

    except Exception as e:
        print(f"❌ {data_file}: Unexpected error")
        print(f"   Error: {str(e)}")
        return False


def validate_all(verbose: bool = False) -> Tuple[int, int]:
    """Validate all data files with models. Returns (passed, failed) counts."""
    passed = 0
    failed = 0

    print("=" * 60)
    print("Validating JSON data files with Pydantic models")
    print("=" * 60)
    print()

    for data_file in sorted(MODEL_MAPPING.keys()):
        if validate_file(data_file, verbose):
            passed += 1
        else:
            failed += 1
        if verbose:
            print()

    return passed, failed


def validate_book_file(book_file: Path, verbose: bool = False) -> bool:
    """Validate a single book JSON file using BookIntroduction model."""
    # Load data file
    data, error = load_json(book_file)
    if error:
        print(f"❌ {book_file.name}: {error}")
        return False

    # Validate using Pydantic model
    try:
        BookIntroduction(**data)
        print(f"✅ {book_file.name}: Valid")
        if verbose:
            print(f"   Size: {book_file.stat().st_size:,} bytes")
        return True

    except ValidationError as e:
        print(f"❌ {book_file.name}: Validation failed")
        for error_detail in e.errors():
            location = " -> ".join(str(loc) for loc in error_detail['loc'])
            print(f"   {location}: {error_detail['msg']}")
        return False

    except Exception as e:
        print(f"❌ {book_file.name}: Unexpected error")
        print(f"   Error: {str(e)}")
        return False


def validate_all_books(verbose: bool = False) -> Tuple[int, int]:
    """Validate all 66 book introduction files. Returns (passed, failed) counts."""
    passed = 0
    failed = 0

    books_dir = DATA_DIR / "books"
    if not books_dir.exists():
        print(f"❌ Books directory not found: {books_dir}")
        return 0, 0

    print("=" * 60)
    print("Validating 66 book introduction files")
    print("=" * 60)
    print()

    book_files = sorted(books_dir.glob("*.json"))
    for book_file in book_files:
        if validate_book_file(book_file, verbose):
            passed += 1
        else:
            failed += 1
        if verbose:
            print()

    return passed, failed


def generate_json_schemas():
    """Generate JSON Schema files from Pydantic models."""
    print("=" * 60)
    print("Generating JSON Schema files from Pydantic models")
    print("=" * 60)
    print()

    SCHEMAS_DIR.mkdir(exist_ok=True)

    # Generate schemas for main data files
    for data_file, model_class in MODEL_MAPPING.items():
        schema_file = data_file.replace('.json', '.schema.json')
        schema_path = SCHEMAS_DIR / schema_file

        try:
            # Generate JSON Schema from Pydantic model
            schema = model_class.model_json_schema()

            # Add metadata
            schema['$id'] = f"https://kjvstudy.org/schemas/{schema_file}"
            schema['title'] = model_class.__doc__ or model_class.__name__

            # Write schema file
            with open(schema_path, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)

            print(f"✅ Generated {schema_file}")

        except Exception as e:
            print(f"❌ Failed to generate {schema_file}: {e}")

    # Generate schema for book introduction files
    try:
        schema_file = "book_introduction.schema.json"
        schema_path = SCHEMAS_DIR / schema_file

        schema = BookIntroduction.model_json_schema()
        schema['$id'] = f"https://kjvstudy.org/schemas/{schema_file}"
        schema['title'] = "Schema for individual book introduction files"

        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)

        print(f"✅ Generated {schema_file}")

    except Exception as e:
        print(f"❌ Failed to generate {schema_file}: {e}")

    print()
    print(f"Schemas written to: {SCHEMAS_DIR}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate JSON data files with Pydantic models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_data.py                    # Validate all files
  python scripts/validate_data.py -f bible_metadata.json  # Validate one file
  python scripts/validate_data.py --verbose          # Show details
  python scripts/validate_data.py --generate-schemas # Generate JSON schemas
        """
    )
    parser.add_argument(
        '-f', '--file',
        help='Validate specific file only',
        metavar='FILE'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--generate-schemas',
        action='store_true',
        help='Generate JSON Schema files from Pydantic models'
    )
    parser.add_argument(
        '--books',
        action='store_true',
        help='Validate all 66 book introduction files'
    )

    args = parser.parse_args()

    # Generate schemas if requested
    if args.generate_schemas:
        generate_json_schemas()
        sys.exit(0)

    # Validate books if requested
    if args.books:
        passed, failed = validate_all_books(args.verbose)

        print()
        print("=" * 60)
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 60)

        sys.exit(0 if failed == 0 else 1)

    # Validate specific file or all files
    if args.file:
        success = validate_file(args.file, args.verbose)
        sys.exit(0 if success else 1)
    else:
        passed, failed = validate_all(args.verbose)

        print()
        print("=" * 60)
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 60)

        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
