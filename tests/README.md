# KJV Study API Tests

Comprehensive test suite for the KJV Study API and web application.

## Test Files

### `test_api.py`
Core API endpoint tests covering:
- Health checks
- Verse endpoints (single, range, verse of the day)
- Book endpoints (list, details, chapters, full text)
- Bible endpoint (entire Bible)
- Search functionality
- Interlinear data
- Cross-references
- Topics and reading plans
- Book name normalization

### `test_edge_cases.py`
Edge case and error handling tests:
- Invalid inputs and error responses
- Verse range edge cases
- Book abbreviations (comprehensive)
- Search functionality edge cases
- Book boundaries (shortest, longest, etc.)
- Cross-references edge cases
- Interlinear data edge cases
- Topics and reading plans edge cases
- Performance tests with large data
- Content validation

### `test_web_routes.py`
Web page and HTML endpoint tests:
- Homepage
- Book listing and detail pages
- Chapter and verse pages
- Search pages
- Topics and reading plans pages
- Resource pages
- 404 handling
- Redirects
- HTML structure and metadata
- Navigation elements
- Accessibility features
- Content types

### `conftest.py`
Shared pytest configuration and fixtures:
- `client` - TestClient for API requests
- `sample_verses` - Common verse references
- `sample_books` - Sample book names
- `book_abbreviations` - Abbreviation mappings
- `bible_facts` - Known Bible facts for validation

## Running Tests

### Run all tests
```bash
uv run pytest tests/ -v
```

### Run specific test file
```bash
uv run pytest tests/test_api.py -v
```

### Run specific test class
```bash
uv run pytest tests/test_api.py::TestVerseEndpoints -v
```

### Run specific test
```bash
uv run pytest tests/test_api.py::TestVerseEndpoints::test_get_single_verse -v
```

### Run with coverage
```bash
uv run pytest tests/ --cov=kjvstudy_org --cov-report=html
```

### Run tests in parallel (faster)
```bash
uv run pytest tests/ -n auto
```

## Test Categories

### Functional Tests
- API endpoints return correct data
- Web pages load correctly
- Search functionality works
- Data integrity

### Edge Cases
- Invalid inputs
- Boundary conditions
- Error handling
- Performance with large datasets

### Integration Tests
- Book name normalization
- Cross-references linking
- Interlinear data availability
- Content validation

## Fixtures

Fixtures are defined in `conftest.py` and automatically available to all test files:

- **client**: FastAPI TestClient for making requests
- **sample_verses**: Dictionary of common verse references
- **sample_books**: Dictionary of sample book names
- **book_abbreviations**: Mapping of abbreviations to full names
- **bible_facts**: Known facts about the KJV Bible

## Best Practices

1. **Use fixtures** - Leverage shared fixtures from conftest.py
2. **Descriptive names** - Test names should describe what they test
3. **Arrange-Act-Assert** - Follow AAA pattern in tests
4. **One assertion per concept** - Keep tests focused
5. **Test edge cases** - Don't just test happy paths
6. **Use parametrize** - For testing multiple similar cases

## Adding New Tests

When adding new functionality:

1. Add API tests to `test_api.py`
2. Add edge case tests to `test_edge_cases.py`
3. Add web route tests to `test_web_routes.py`
4. Update fixtures in `conftest.py` if needed
5. Run tests to ensure they pass
6. Add documentation if needed

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: uv run pytest tests/ -v --cov
```
