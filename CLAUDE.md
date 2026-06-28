# Claude Code Development Notes

This file contains information for Claude Code (AI assistant) about the kjvstudy.org project.

## Project Overview

KJV Study is a modern web application for studying the King James Bible with AI-powered commentary and insights. Built with FastAPI, it provides both a web interface and a comprehensive RESTful API.

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Package Manager**: uv
- **Bible Data**: Custom implementation with local JSON (31,102 verses from 1769 Cambridge KJV)
- **Templates**: Jinja2
- **Styling**: Tufte CSS (Edward Tufte-inspired typography)
- **Deployment**: Docker via Dokploy
- **CI/CD**: GitHub Actions

## Testing

### Test Suite

The project has **941 comprehensive tests** across 16 test files:

- **87 API endpoint tests** (`test_api.py`) - Health checks, verse/book/Bible endpoints, search, interlinear, cross-references, topics, reading plans
- **87 utility tests** (`test_utils.py`) - Helper functions and utilities
- **85 coverage tests part 5** (`test_coverage_part5.py`)
- **84 coverage tests part 6** (`test_coverage_part6.py`)
- **77 coverage tests part 2** (`test_coverage_part2.py`)
- **77 coverage improvement tests** (`test_coverage_improvements.py`)
- **76 resource route tests** (`test_resource_routes.py`) - Biblical resources, parables, names of God, etc.
- **64 web route tests** (`test_web_routes.py`) - Homepage, book/chapter/verse pages, search, topics, accessibility
- **62 Strong's concordance tests** (`test_strongs.py`) - Hebrew/Greek lexicon functionality
- **61 coverage tests part 4** (`test_coverage_part4.py`)
- **59 coverage tests part 3** (`test_coverage_part3.py`)
- **46 advanced route tests** (`test_advanced_routes.py`) - Commentary, stories, family trees, etc.
- **39 edge case tests** (`test_edge_cases.py`) - Error handling, boundary conditions, validation
- **22 data validation tests** (`test_data_validation.py`) - JSON data integrity
- **14 sitemap/utility tests** (`test_sitemap_and_utilities.py`)
- **1 KJV core test** (`test_kjv.py`)

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_api.py -v

# Run with coverage
uv run pytest tests/ --cov=kjvstudy_org --cov-report=html

# Run in Docker (recommended)
docker compose exec web uv run pytest tests/ -v
```

### Test Fixtures

Shared fixtures are defined in `tests/conftest.py`:

- `client` - FastAPI TestClient
- `sample_verses` - Common verse references
- `sample_books` - Sample book names
- `book_abbreviations` - Abbreviation mappings
- `bible_facts` - Bible validation data

### CI/CD

Tests run automatically via GitHub Actions:

- **On every push** to main
- **On every pull request**
- **Before deployment** (Dokploy deploys on push to main after tests pass)

See `.github/workflows/test.yml` and `.github/workflows/deploy.yml`

## API Documentation

The API is fully documented with OpenAPI/Swagger:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Key API Endpoints

```
GET /api/health                              - Health check
GET /api/verse/{book}/{chapter}/{verse}      - Get single verse
GET /api/verse-range/{book}/{chapter}/{start}/{end} - Get verse range
GET /api/verse-of-the-day                    - Get daily verse
GET /api/books                               - List all books
GET /api/books/{book}                        - Get book details
GET /api/books/{book}/chapters/{chapter}     - Get chapter
GET /api/books/{book}/text                   - Get entire book
GET /api/bible                               - Get entire Bible (31,102 verses)
GET /api/search?q={query}                    - Search verses
GET /api/interlinear/{book}/{chapter}/{verse} - Get word-by-word analysis
GET /api/cross-references/{book}/{chapter}/{verse} - Get cross-references
GET /api/topics                              - List topics
GET /api/topics/{topic_name}                 - Get topic details
GET /api/reading-plans                       - List reading plans
GET /api/reading-plans/{plan_id}             - Get reading plan
```

All endpoints support book name abbreviations (Gen, Ex, Mt, etc.)

## Development Workflow

### Local Development

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn kjvstudy_org.server:app --reload

# Or use Docker
docker compose up
```

### Project Structure

```
kjvstudy_org/
├── server.py           # FastAPI application
├── kjv.py             # Bible data access
├── cross_references.py # Cross-reference data
├── reading_plans.py    # Reading plan data
├── topics.py          # Topical index
├── interlinear_loader.py # Hebrew/Greek word analysis
├── templates/         # Jinja2 HTML templates
└── static/            # CSS, images, etc.

tests/
├── conftest.py        # Shared fixtures
├── test_api.py        # API tests
├── test_edge_cases.py # Edge case tests
├── test_web_routes.py # Web route tests
└── README.md          # Test documentation
```

### Key Features

1. **Comprehensive Bible Text**
   - All 66 books, 31,102 verses
   - Book abbreviation support
   - Chapter and verse navigation

2. **Study Resources**
   - Cross-references
   - Topical index
   - Reading plans
   - Study guides
   - Biblical timeline
   - Family trees/genealogies
   - Maps

3. **Advanced Features**
   - Interlinear data (Hebrew/Greek)
   - Word-by-word analysis
   - Strong's numbers
   - Full-text search
   - Verse of the day

4. **API**
   - RESTful JSON API
   - OpenAPI documentation
   - Example parameters
   - Comprehensive endpoints

## Code Quality

### Warnings (Known Issues)

The test suite shows several deprecation warnings:

1. **`example` deprecated in favor of `examples`**
   - FastAPI parameter examples should use `examples=` instead of `example=`
   - Non-breaking, cosmetic issue

2. **`on_event` deprecated in favor of lifespan**
   - FastAPI startup events should use lifespan context manager
   - Non-breaking, will be fixed in future update

3. **TemplateResponse parameter order**
   - Starlette expects `Request` as first parameter
   - Non-breaking, cosmetic issue

None of these warnings affect functionality.

## Data Validation

Always validate data before committing changes to JSON files:

```bash
# Validate all data files with Pydantic models
uv run python scripts/validate_data.py
```

This validates:
- `bible_metadata.json`
- `featured_verses.json`
- `reading_plans/` (12 files)
- `red_letter_verses.json`
- `resource_slugs.json`
- `study_guides/` (36 files)
- `topics/` (36 files)
- `verse_commentary/` (66 files - one per book)
- `word_studies.json`

## Contributing

When making changes:

1. **Write tests** for new features
2. **Run tests** before committing: `uv run pytest tests/ -v`
3. **Validate data** before committing: `uv run python scripts/validate_data.py`
4. **Check CI** - GitHub Actions will run tests automatically
5. **Update docs** if adding API endpoints
6. **Follow existing patterns** in the codebase

## Useful Commands

```bash
# Sync dependencies
uv sync

# Run server
uv run uvicorn kjvstudy_org.server:app --reload

# Run tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_api.py::TestAPIHealth -v

# Check test coverage
uv run pytest tests/ --cov=kjvstudy_org --cov-report=term-missing

# Validate data files
uv run python scripts/validate_data.py

# Format code (if ruff is configured)
uv run ruff check .

# Docker commands
docker compose up            # Start server
docker compose exec web bash # Shell into container
docker compose exec web uv run pytest tests/ -v # Run tests in container
```

## Notes for Claude

- All tests pass (100/100)
- Use `uv` for all Python package management
- API responses use `name` field for books, not `book`
- API responses use `start`/`end` for verse ranges, not `start_verse`/`end_verse`
- Error handling returns proper 404 for invalid inputs (not found resources)
- Book abbreviations are comprehensive but some edge cases may not work
- The project uses Tufte CSS for clean, readable typography
- Interlinear data is available for most verses but not all
- Cross-references data is extensive but not complete for all verses
