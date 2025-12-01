# JSON Schema Validation Files

This directory contains [JSON Schema](https://json-schema.org/) validation files for the data directory. These schemas formally define the structure, types, and constraints for each JSON data file.

## What is JSON Schema?

JSON Schema is a vocabulary that allows you to annotate and validate JSON documents. It provides:

- **Structure validation**: Ensure JSON follows expected format
- **Type safety**: Validate data types (string, number, array, etc.)
- **Constraints**: Enforce min/max values, patterns, required fields
- **Documentation**: Self-documenting schemas describe data structure
- **IDE support**: Enable autocomplete and inline validation in editors

## Available Schemas

| Schema File | Data File | Description |
|-------------|-----------|-------------|
| `bible_metadata.schema.json` | `bible_metadata.json` | Bible books, testaments, abbreviations |
| `word_studies.schema.json` | `word_studies.json` | Hebrew/Greek word definitions |
| `study_guides.schema.json` | `study_guides.json` | Study guide catalog and content |
| `verse_commentary.schema.json` | `verse_commentary/*.json` | Verse analysis and commentary (per book) |
| `featured_verses.schema.json` | `featured_verses.json` | Verse-of-the-day rotation |
| `resource_slugs.schema.json` | `resource_slugs.json` | Resource URL slugs for sitemap |
| `book_introduction.schema.json` | `data/books/*.json` | Individual book introductions (66 files) |

## Schema Features

### Validation Rules

Each schema enforces:
- **Required fields**: Ensures critical data is present
- **Data types**: Validates strings, numbers, arrays, objects
- **Format patterns**: Validates verse references, slugs, etc.
- **Value constraints**: Min/max lengths, numeric ranges
- **Unique values**: Prevents duplicates in arrays
- **Additional properties**: Blocks unexpected fields

### Example: Bible Metadata Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["old_testament_books", "new_testament_books", "book_abbreviations"],
  "properties": {
    "old_testament_books": {
      "type": "array",
      "minItems": 39,
      "maxItems": 39,
      "items": {"type": "string"},
      "uniqueItems": true
    },
    ...
  }
}
```

This ensures:
- ✅ Exactly 39 OT books (no more, no less)
- ✅ All book names are strings
- ✅ No duplicate book names
- ✅ Required fields present

## Using the Schemas

### 1. Command Line Validation

Use the provided validation script:

```bash
# Validate all main data files
python scripts/validate_data.py

# Validate all 66 book introduction files
python scripts/validate_data.py --books

# Validate specific file
python scripts/validate_data.py --file bible_metadata.json

# Show detailed output
python scripts/validate_data.py --verbose

# Regenerate all JSON schemas from Pydantic models
python scripts/validate_data.py --generate-schemas
```

### 2. Python Validation

```python
import json
from jsonschema import validate

# Load data and schema
with open('kjvstudy_org/data/bible_metadata.json') as f:
    data = json.load(f)

with open('kjvstudy_org/data/schemas/bible_metadata.schema.json') as f:
    schema = json.load(f)

# Validate
validate(instance=data, schema=schema)  # Raises ValidationError if invalid
```

### 3. IDE Integration

#### VS Code
Install the [JSON Schema extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml):

Add to `.vscode/settings.json`:
```json
{
  "json.schemas": [
    {
      "fileMatch": ["kjvstudy_org/data/bible_metadata.json"],
      "url": "./kjvstudy_org/data/schemas/bible_metadata.schema.json"
    },
    {
      "fileMatch": ["kjvstudy_org/data/word_studies.json"],
      "url": "./kjvstudy_org/data/schemas/word_studies.schema.json"
    }
  ]
}
```

#### PyCharm/IntelliJ
1. Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings
2. Add mapping for each data file to its schema

### 4. Pre-commit Hook

Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-json-data
        name: Validate JSON data files
        entry: python scripts/validate_data.py
        language: system
        pass_filenames: false
```

### 5. CI/CD Integration

Add to `.github/workflows/test.yml`:
```yaml
- name: Validate JSON schemas
  run: |
    pip install jsonschema
    python scripts/validate_data.py
```

## Common Validation Patterns

### Verse References

Pattern for verse references like "John 3:16" or "Genesis 1:1-3":
```json
{
  "pattern": "^[A-Za-z0-9 ]+ \\d+:\\d+(-\\d+)?$"
}
```

### URL Slugs

Pattern for lowercase-with-hyphens slugs:
```json
{
  "pattern": "^[a-z-]+$"
}
```

### Hebrew/Greek Text

UTF-8 strings with minimum length:
```json
{
  "type": "string",
  "minLength": 1
}
```

## Error Messages

### Common Validation Errors

**Missing Required Field**
```
ValidationError: 'old_testament_books' is a required property
```
→ Add the missing field to your JSON

**Wrong Type**
```
ValidationError: 42 is not of type 'string'
```
→ Fix the data type (e.g., change number to string)

**Invalid Pattern**
```
ValidationError: 'john-316' does not match '^[A-Za-z0-9 ]+ \\d+:\\d+(-\\d+)?$'
```
→ Fix the format (should be "John 3:16")

**Array Length**
```
ValidationError: [38 items] is too short (minimum: 39)
```
→ Add missing items to the array

**Duplicate Values**
```
ValidationError: ['Genesis', 'Exodus', 'Genesis'] has non-unique elements
```
→ Remove duplicate entries

## Creating New Schemas

### Template

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://kjvstudy.org/schemas/your_file.schema.json",
  "title": "Your Data File",
  "description": "Description of what this schema validates",
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "Description of field1",
      "minLength": 1
    },
    "field2": {
      "type": "array",
      "description": "Description of field2",
      "items": {
        "type": "string"
      }
    }
  },
  "additionalProperties": false
}
```

### Steps to Add New Schema

1. **Create schema file**: `schemas/your_file.schema.json`
2. **Add to mapping**: Update `SCHEMA_MAPPING` in `scripts/validate_data.py`
3. **Test validation**: Run `python scripts/validate_data.py --file your_file.json`
4. **Add to CI**: Include in automated testing

## Best Practices

### 1. Use Strict Validation
- Set `"additionalProperties": false` to block unexpected fields
- Use `"uniqueItems": true` for arrays that shouldn't have duplicates
- Specify `minItems`/`maxItems` for arrays with known sizes

### 2. Provide Clear Descriptions
```json
{
  "description": "Hebrew word in original script (e.g., אֱלֹהִים)"
}
```

### 3. Use Definitions for Reusable Types
```json
{
  "definitions": {
    "verseReference": {
      "type": "string",
      "pattern": "^[A-Za-z0-9 ]+ \\d+:\\d+(-\\d+)?$"
    }
  },
  "properties": {
    "verses": {
      "type": "array",
      "items": {"$ref": "#/definitions/verseReference"}
    }
  }
}
```

### 4. Version Your Schemas
Include `$id` with URL for schema versioning:
```json
{
  "$id": "https://kjvstudy.org/schemas/v1/bible_metadata.schema.json"
}
```

## Testing

### Manual Testing
```bash
# Test all schemas
python scripts/validate_data.py --verbose

# Test specific schema
python scripts/validate_data.py --file bible_metadata.json
```

### Automated Testing
```python
# In tests/test_schemas.py
import pytest
from scripts.validate_data import validate_file

def test_bible_metadata_valid():
    assert validate_file("bible_metadata.json")

def test_word_studies_valid():
    assert validate_file("word_studies.json")
```

## Resources

- **JSON Schema Documentation**: https://json-schema.org/
- **JSON Schema Validator**: https://www.jsonschemavalidator.net/
- **Understanding JSON Schema**: https://json-schema.org/understanding-json-schema/
- **Schema Store**: https://www.schemastore.org/json/ (examples)

## Future Enhancements

- [ ] Add schemas for all remaining data files
- [ ] Generate TypeScript types from schemas
- [ ] Create schema documentation website
- [ ] Add more complex validation rules
- [ ] Implement custom validators for biblical references
- [ ] Create schema migration tools

---

*Last Updated: 2025-11-27*
*Schemas: 7 active schemas covering core data files and 66 book introductions*
