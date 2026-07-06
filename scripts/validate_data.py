#!/usr/bin/env python3
"""
Validate JSON data files using Pydantic models.

This script validates all data files in kjvstudy_org/data/ using Pydantic models
for type safety and validation. Pydantic provides clear error messages and
keeps data checks independent of the web layer.

Usage:
    python scripts/validate_data.py              # Validate all files
    python scripts/validate_data.py --file bible_metadata.json  # Validate specific file
    python scripts/validate_data.py --verbose    # Show detailed output
    python scripts/validate_data.py --generate-schemas  # Generate JSON schemas

Requirements:
    pip install pydantic
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


class StudyGuideFile(BaseModel):
    """Schema for a single study guide file"""
    content: GuideContent
    catalog_entry: Optional[CatalogEntry] = None
    category: Optional[str] = None


class TopicsFile(BaseModel):
    """Schema for a single topics file"""
    root: Dict[str, dict]


class ReadingPlanFile(BaseModel):
    """Schema for a single reading plan file"""
    plan: Dict[str, List[Dict[str, object]]]


class VerseCommentaryEntry(BaseModel):
    """Schema for verse commentary entry"""
    analysis: str = Field(..., min_length=1)
    historical: str = Field(..., min_length=1)
    questions: List[str] = Field(..., min_length=1)


class VerseCommentaryBook(BaseModel):
    """Schema for a single verse commentary book file"""
    book: str = Field(..., min_length=1)
    commentary: Dict[str, Dict[str, VerseCommentaryEntry]] = Field(..., min_length=1)

    @field_validator('commentary')
    @classmethod
    def check_numeric_keys(cls, v):
        for chapter_key, verses in v.items():
            if not str(chapter_key).isdigit():
                raise ValueError(f"Invalid chapter key: {chapter_key}")
            if not isinstance(verses, dict) or len(verses) == 0:
                raise ValueError(f"Chapter {chapter_key} must contain verse entries")
            for verse_key, entry in verses.items():
                if not str(verse_key).isdigit():
                    raise ValueError(f"Invalid verse key: {verse_key}")
                if not isinstance(entry, (dict, BaseModel)):
                    raise ValueError(f"Verse {chapter_key}:{verse_key} must be an object")
        return v


class Devotional(BaseModel):
    """Schema for verse devotional content"""
    title: str = Field(..., min_length=1, max_length=100)
    theme: str = Field(..., min_length=1, max_length=50)
    opening: str = Field(..., min_length=10)
    meditation: str = Field(..., min_length=20)
    application: str = Field(..., min_length=10)
    prayer: str = Field(..., min_length=10)

    @field_validator('prayer')
    @classmethod
    def prayer_ends_with_amen(cls, v):
        if not v.strip().endswith('Amen.'):
            raise ValueError("Prayer must end with 'Amen.'")
        return v


class FeaturedVerse(BaseModel):
    """Schema for individual featured verse with optional devotional"""
    book: str = Field(..., min_length=1)
    chapter: int = Field(..., ge=1)
    verse: int = Field(..., ge=1)
    devotional: Optional[Devotional] = None


class FeaturedVerses(BaseModel):
    """Schema for featured_verses.json - 365 verses with devotionals"""
    verses: List[FeaturedVerse] = Field(..., min_length=1)

    @field_validator('verses')
    @classmethod
    def check_devotional_coverage(cls, v):
        # Warn if not all verses have devotionals
        with_devotional = sum(1 for verse in v if verse.devotional is not None)
        if with_devotional < len(v):
            # This is just informational, not an error
            pass
        return v


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



class PoetryBookData(BaseModel):
    """Schema for individual book poetry data"""
    is_poetry: bool = Field(..., description="Whether the entire book is poetry")
    poetry_chapters: List[int] | str = Field(..., description="List of chapter numbers that are poetry, or 'all'")
    stanza_breaks: Dict[str, List[int]] = Field(..., description="Map of chapter number to list of verse numbers with stanza breaks")

    @field_validator('poetry_chapters')
    @classmethod
    def check_chapters_sorted(cls, v):
        # Allow "all" as a special value for entirely poetry books
        if v == "all":
            return v
        if v != sorted(v):
            raise ValueError("poetry_chapters must be sorted")
        if len(v) != len(set(v)):
            raise ValueError("Duplicate chapter numbers found")
        return v

    @field_validator('stanza_breaks')
    @classmethod
    def check_stanza_breaks(cls, v):
        for chapter_key, verses in v.items():
            if not chapter_key.isdigit():
                raise ValueError(f"Invalid chapter key: {chapter_key}")
            if verses != sorted(verses):
                raise ValueError(f"Stanza breaks for chapter {chapter_key} must be sorted")
            if len(verses) != len(set(verses)):
                raise ValueError(f"Duplicate verse numbers in chapter {chapter_key}")
        return v


class PoetryFormatting(BaseModel):
    """Schema for poetry_formatting.json"""
    books: Dict[str, PoetryBookData] = Field(..., min_length=1)

    @field_validator('books')
    @classmethod
    def check_valid_books(cls, v):
        # Many books have poetic sections (Psalms, Prophets, NT hymns, etc.)
        # Just validate that book names are valid Bible books
        valid_books = {
            'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
            'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
            '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther',
            'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
            'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel',
            'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
            'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
            'Matthew', 'Mark', 'Luke', 'John', 'Acts',
            'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
            'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
            '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
            'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation'
        }
        for book_name in v.keys():
            if book_name not in valid_books:
                raise ValueError(f"Invalid book name: {book_name}")
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
    "study_guides": StudyGuideFile,
    "verse_commentary": VerseCommentaryBook,
    "topics": TopicsFile,
    "reading_plans": ReadingPlanFile,
    "featured_verses.json": FeaturedVerses,
    "red_letter_verses.json": RedLetterVerses,
    "poetry_formatting.json": PoetryFormatting,
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
    if data_file == "verse_commentary":
        return validate_verse_commentary_directory(verbose)
    if data_file == "study_guides":
        return validate_study_guides_directory(verbose)
    if data_file == "topics":
        return validate_topics_directory(verbose)
    if data_file == "reading_plans":
        return validate_reading_plans_directory(verbose)

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


def validate_verse_commentary_directory(verbose: bool = False) -> bool:
    """Validate all per-book verse commentary files."""
    dir_path = DATA_DIR / "verse_commentary"
    if not dir_path.exists():
        print(f"❌ verse_commentary: Directory not found at {dir_path}")
        return False

    passed = 0
    failed = 0

    for file_path in sorted(dir_path.glob("*.json")):
        data, error = load_json(file_path)
        if error:
            print(f"❌ {file_path.name}: {error}")
            failed += 1
            continue

        try:
            VerseCommentaryBook(**data)
            if verbose:
                print(f"✅ {file_path.name}: Valid")
            passed += 1
        except ValidationError as e:
            print(f"❌ {file_path.name}: Validation failed")
            for error_detail in e.errors():
                location = " -> ".join(str(loc) for loc in error_detail['loc'])
                print(f"   {location}: {error_detail['msg']}")
            failed += 1
        except Exception as e:
            print(f"❌ {file_path.name}: Unexpected error")
            print(f"   Error: {str(e)}")
            failed += 1

    if failed == 0:
        print(f"✅ verse_commentary: Valid ({passed} files)")
        return True

    print(f"❌ verse_commentary: {failed} files failed validation")
    return False


def validate_study_guides_directory(verbose: bool = False) -> bool:
    """Validate per-guide study guide files."""
    dir_path = DATA_DIR / "study_guides"
    if not dir_path.exists():
        print(f"❌ study_guides: Directory not found at {dir_path}")
        return False

    passed = 0
    failed = 0

    for file_path in sorted(dir_path.glob("*.json")):
        data, error = load_json(file_path)
        if error:
            print(f"❌ {file_path.name}: {error}")
            failed += 1
            continue

        try:
            StudyGuideFile(**data)
            if verbose:
                print(f"✅ {file_path.name}: Valid")
            passed += 1
        except ValidationError as e:
            print(f"❌ {file_path.name}: Validation failed")
            for error_detail in e.errors():
                location = " -> ".join(str(loc) for loc in error_detail['loc'])
                print(f"   {location}: {error_detail['msg']}")
            failed += 1
        except Exception as e:
            print(f"❌ {file_path.name}: Unexpected error")
            print(f"   Error: {str(e)}")
            failed += 1

    if failed == 0:
        print(f"✅ study_guides: Valid ({passed} files)")
        return True

    print(f"❌ study_guides: {failed} files failed validation")
    return False


def validate_topics_directory(verbose: bool = False) -> bool:
    """Validate per-topic files."""
    dir_path = DATA_DIR / "topics"
    if not dir_path.exists():
        print(f"❌ topics: Directory not found at {dir_path}")
        return False

    passed = 0
    failed = 0

    for file_path in sorted(dir_path.glob("*.json")):
        data, error = load_json(file_path)
        if error:
            print(f"❌ {file_path.name}: {error}")
            failed += 1
            continue

        try:
            TopicsFile(root=data)
            if verbose:
                print(f"✅ {file_path.name}: Valid")
            passed += 1
        except ValidationError as e:
            print(f"❌ {file_path.name}: Validation failed")
            for error_detail in e.errors():
                location = " -> ".join(str(loc) for loc in error_detail['loc'])
                print(f"   {location}: {error_detail['msg']}")
            failed += 1
        except Exception as e:
            print(f"❌ {file_path.name}: Unexpected error")
            print(f"   Error: {str(e)}")
            failed += 1

    if failed == 0:
        print(f"✅ topics: Valid ({passed} files)")
        return True

    print(f"❌ topics: {failed} files failed validation")
    return False


def validate_reading_plans_directory(verbose: bool = False) -> bool:
    """Validate per-plan reading plan files."""
    dir_path = DATA_DIR / "reading_plans"
    if not dir_path.exists():
        print(f"❌ reading_plans: Directory not found at {dir_path}")
        return False

    passed = 0
    failed = 0

    for file_path in sorted(dir_path.glob("*.json")):
        data, error = load_json(file_path)
        if error:
            print(f"❌ {file_path.name}: {error}")
            failed += 1
            continue

        try:
            # Each file has one key with the plan id mapping to the plan object
            if len(data) != 1:
                raise ValueError("Reading plan file must contain exactly one plan")
            ReadingPlanFile(plan=data)
            if verbose:
                print(f"✅ {file_path.name}: Valid")
            passed += 1
        except ValidationError as e:
            print(f"❌ {file_path.name}: Validation failed")
            for error_detail in e.errors():
                location = " -> ".join(str(loc) for loc in error_detail['loc'])
                print(f"   {location}: {error_detail['msg']}")
            failed += 1
        except Exception as e:
            print(f"❌ {file_path.name}: Unexpected error")
            print(f"   Error: {str(e)}")
            failed += 1

    if failed == 0:
        print(f"✅ reading_plans: Valid ({passed} files)")
        return True

    print(f"❌ reading_plans: {failed} files failed validation")
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
        schema_file = data_file.replace('.json', '.schema.json') if data_file.endswith('.json') else f"{data_file}.schema.json"
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
