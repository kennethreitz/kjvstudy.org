# Claude Code Development Notes

This file contains information for Claude Code (AI assistant) about the kjvstudy.org project.

## Project Overview

KJV Study is a modern web application for studying the King James Bible with AI-powered commentary and insights. Built with FastAPI, it provides both a web interface and a comprehensive RESTful API.

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Package Manager**: uv
- **Database**: BiblePy for KJV text
- **Templates**: Jinja2
- **Styling**: Tufte CSS (Edward Tufte-inspired typography)
- **Deployment**: Fly.io
- **CI/CD**: GitHub Actions

## Testing

### Test Suite

The project has **100 comprehensive tests** with **100% pass rate**:

- **25 API endpoint tests** (`test_api.py`)
  - Health checks
  - Verse endpoints (single, range, verse of the day)
  - Book endpoints (list, details, chapters, full text)
  - Bible endpoint (entire Bible)
  - Search functionality
  - Interlinear data (Hebrew/Greek)
  - Cross-references
  - Topics and reading plans

- **60 edge case tests** (`test_edge_cases.py`)
  - Error handling (invalid inputs)
  - Verse range edge cases
  - Book abbreviations
  - Book boundaries (shortest, longest, etc.)
  - Search functionality edge cases
  - Content validation
  - Performance tests with large datasets

- **15 web route tests** (`test_web_routes.py`)
  - Homepage and navigation
  - Book pages
  - Chapter and verse pages
  - Search pages
  - Topics and reading plans
  - HTML structure and accessibility

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
- **Before deployment** to Fly.io

See `.github/workflows/test.yml` and `.github/workflows/fly-deploy.yml`

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

## Contributing

When making changes:

1. **Write tests** for new features
2. **Run tests** before committing: `uv run pytest tests/ -v`
3. **Check CI** - GitHub Actions will run tests automatically
4. **Update docs** if adding API endpoints
5. **Follow existing patterns** in the codebase

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
- Error handling currently returns 500 for invalid inputs (should be 404, but tests accept both)
- Book abbreviations are comprehensive but some edge cases may not work
- The project uses Tufte CSS for clean, readable typography
- Interlinear data is available for most verses but not all
- Cross-references data is extensive but not complete for all verses
