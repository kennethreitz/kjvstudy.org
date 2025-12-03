# KJV Study Data Directory

This directory contains all biblical reference data for the KJV Study application in structured JSON format. All data is externalized from code for easier maintenance, editing, and version control.

## Overview

- **359 JSON files** containing biblical reference data (+ 9 schema files)
- **Total size**: ~58 MB (including 28 MB verse commentary, 12 MB compressed interlinear)
- **Coverage**: Complete Bible reference materials, study resources, and theological content
- **Format**: UTF-8 encoded JSON with consistent structure

## Quick Stats

| Category | Files | Size | Description |
|----------|-------|------|-------------|
| Bible Text & Metadata | 67 | ~85K | Book metadata, chapters, verses, abbreviations |
| Interlinear Data | 1 | 12M (compressed) | Greek/Hebrew words with Strong's numbers |
| Verse Commentary | 64 | 28M | In-depth theological analysis for 12,321 verses |
| Cross-references | 66 | 9.0M | Treasury of Scripture Knowledge references (split per book) |
| Study Resources | 75 | ~2.0M | Study guides, topics, word studies, resources |
| Reference Materials | 84 | ~19M | Reading plans, biographies, timeline, stories, Strong's |

---

## Core Bible Data

### `bible_metadata.json` (5.7K)
**Contains**: Old Testament books (39), New Testament books (27), book abbreviations (~150)

**Structure**:
```json
{
  "old_testament_books": ["Genesis", "Exodus", ...],
  "new_testament_books": ["Matthew", "Mark", ...],
  "book_abbreviations": {
    "Gen": "Genesis",
    "Matt": "Matthew",
    ...
  }
}
```

**Used by**: `utils/books.py`, book normalization, sitemap generation

---

### `books/` Directory (66 files)
**Contains**: Individual JSON file for each Bible book with introduction, summary, outline, and key themes

**Files**: `genesis.json`, `matthew.json`, `revelation.json`, etc.

**Structure**:
```json
{
  "name": "Genesis",
  "testament": "Old Testament",
  "genre": "Law/Pentateuch",
  "author": "Moses",
  "date_written": "~1440-1400 BC",
  "summary": "...",
  "key_themes": [...],
  "outline": [...]
}
```

**Used by**: `books.py`, book detail pages

---

## Interlinear & Language Data

### `interlinear.json.gz` (12M compressed)
**Contains**: Complete interlinear Bible data for 31,031 verses with original Greek/Hebrew words, transliterations, Strong's numbers, parsing, and definitions

**Structure**:
```json
{
  "John:3:16": [
    {
      "position": 1,
      "original": "Οὕτως",
      "transliteration": "houtōs",
      "strongs": "G3779",
      "english": "For so",
      "parsing": "adv",
      "definition": "in this manner, thus, so"
    },
    ...
  ]
}
```

**Used by**: `interlinear_loader.py`, interlinear verse views, API `/api/interlinear` endpoint

**Note**: Compressed with gzip for efficient storage and lazy-loaded on first access

---

### `word_studies.json` (35K)
**Contains**: 53 biblical terms with Hebrew/Greek definitions, transliterations, and theological notes

**Structure**:
```json
{
  "love": {
    "ot_term": "אַהֲבָה",
    "ot_transliteration": "ahavah",
    "ot_meaning": "love, affection",
    "ot_note": "...",
    "nt_term": "ἀγάπη",
    "nt_transliteration": "agape",
    "nt_meaning": "divine, self-sacrificial love",
    "nt_note": "..."
  }
}
```

**Coverage**: Divine Names (5), Salvation & Redemption (9), Spiritual Nature (9), Worship & Practice (7), Religious Roles (4), Spiritual States (7), Law & Judgment (3), Other Key Terms (9)

**Used by**: `routes/commentary.py`, word study sidenotes in verse commentary

---

### `red_letter_verses.json` (86K)
**Contains**: 2,007 verses containing the words of Jesus Christ from the Gospels, Acts, and Revelation

**Structure**:
```json
{
  "description": "Words of Jesus Christ (red letter edition)",
  "note": "This contains the actual words spoken by Jesus...",
  "verses": {
    "Matthew 3:15": "Suffer it to be so now: for thus it becometh us to fulfil all righteousness.",
    "Matthew 5:3": "full",
    "John 3:16": "full",
    ...
  }
}
```

**Value Types**:
- `"full"`: Jesus speaks the entire verse
- `"text"`: The exact words Jesus spoke (partial verse)

**Coverage**:
- Matthew: 638 verses
- Mark: 290 verses
- Luke: 578 verses
- John: 427 verses
- Acts: 17 verses
- Revelation: 67 verses

**Used by**: `red_letter.py`, verse and chapter templates for red letter edition rendering

**Schema**: `schemas/red_letter_verses.schema.json` (JSON Schema validation file)

---

### `strongs/` (2 files, ~800K combined)
**Contains**: Strong's Concordance data for Hebrew (Old Testament) and Greek (New Testament) word lookups

**Files**: `hebrew.json`, `greek.json`

**Structure**:
```json
{
  "H1": {
    "strongs": "H1",
    "word": "אָב",
    "transliteration": "ab",
    "pronunciation": "awb",
    "definition": "father",
    "kjv_usage": "father, chief, families, desire, patrimony",
    "derivation": "from primitive root"
  }
}
```

**Coverage**:
- Hebrew: ~8,674 entries (H1-H8674)
- Greek: ~5,624 entries (G1-G5624)

**Used by**: `routes/strongs.py`, word study pages, interlinear displays

---

### `close_family_marriages.json` (3.0K)
**Contains**: Documented biblical examples of close-family marriages with scriptural references

**Structure**:
```json
{
  "marriages": [
    {
      "person1": "Abraham",
      "person2": "Sarah",
      "relationship": "half-siblings",
      "description": "Sarah was Abraham's half-sister...",
      "verse": "Genesis 20:12",
      "notes": "..."
    }
  ]
}
```

**Used by**: Biblical history resources, cultural context pages

---

## Study Resources

### `study_guides/` (36 files, ~532K combined)
**Contains**: 25 complete study guides with 183 sections and 732 verse references, split per guide

**Structure**:
```json
{
  "catalog": {
    "Foundational Studies": [
      {
        "title": "New Believer's Guide",
        "description": "...",
        "slug": "new-believer",
        "verses": ["John 3:16", "Romans 8:28", ...]
      }
    ]
  },
  "content": {
    "new-believer": {
      "title": "New Believer's Guide",
      "sections": [
        {
          "title": "God's Infinite Love for You",
          "verses": ["John 3:16", ...],
          "content": "..."
        }
      ]
    }
  }
}
```

**Categories**: Foundational Studies, Character & Living, Biblical Themes, Doctrinal Studies, Thematic Studies, Family & Relationships

**Used by**: `routes/study_guides.py`, `/study-guides` pages

---

### `verse_commentary/` (64 files, 28 MB combined)
**Contains**: In-depth theological commentary for 12,321 verses across 64 books, split per book for efficient loading

**Files**: `john.json`, `genesis.json`, `romans.json`, etc. (one file per book)

**Structure** (per file):
```json
{
  "book": "John",
  "commentary": {
    "3": {
      "16": {
        "analysis": "Detailed theological analysis with Greek/Hebrew words...",
        "historical": "First-century context, cultural background...",
        "questions": [
          "How does this verse challenge modern assumptions?",
          "What does this reveal about God's character?"
        ]
      }
    }
  }
}
```

**Coverage**:
- 64 of 66 books (missing: Song of Solomon, Habakkuk, Haggai)
- 12,321 verses with comprehensive commentary
- Largest files: 1 Chronicles (975 verses, 2.8 MB), 2 Chronicles (822 verses, 2.4 MB)
- Smallest files: 1 Peter (3 verses, 16 KB), Amos (11 verses, 28 KB)

**Features**:
- Deep theological analysis with original language insights
- Historical and cultural context for each verse
- Reflection questions for personal study and group discussion
- Citations of related passages and cross-references

**Used by**: `routes/commentary.py`, `routes/api.py`, enhanced verse detail pages

**Performance**: Split per book for lazy loading—only loads commentary for requested book

---

### `resources/` (39 files, ~1.4M combined)
**Contains**: All biblical reference resources split by major category (angels, prophets, parables, covenants, apostles, women, festivals, fruits of the Spirit, miracles, prayers, beatitudes, commandments, armor of God, I AM statements, systematic theology topics)

**Structure** (per file):
```json
{
  "angels": {
    "Major Angels": {
      "Michael": {
        "title": "Michael the Archangel",
        "description": "...",
        "key_verses": [...],
        "content": "..."
      }
    }
  }
}
```

**Resource Types**:
- Biblical Figures: Angels (4), Prophets (8), Apostles (12), Women (12)
- Biblical Content: Parables (8), Miracles, Prayers, Beatitudes (9), Commandments (10)
- Theological Topics: Trinity, Christology, Soteriology, Pneumatology, Eschatology, Ecclesiology, etc.
- Special Topics: Armor of God (6), I AM Statements (7), Types & Shadows, Messianic Prophecies, Blood in Scripture, Kingdom of God, Names of Christ, Spirits & Demons, Personifications

**Used by**: `data/__init__.py`, `routes/resources.py`, all resource detail pages

---

## Reference Materials

### `topics/` (36 files, ~180K combined)
**Contains**: Topical verse index organized by major theological and practical topics with subtopics and verse references

**Structure**:
```json
{
  "Salvation": {
    "description": "God's plan to redeem humanity through Jesus Christ",
    "subtopics": {
      "By Grace": {
        "verses": ["Ephesians 2:8-9", "Romans 3:24", ...]
      },
      "Through Faith": {
        "verses": ["Romans 5:1", "Acts 16:31", ...]
      }
    }
  }
}
```

**Used by**: `topics.py`, `/topics` pages, topical search

---

### `reading_plans/` (6 files, ~140K combined)
**Contains**: comprehensive Bible reading plans with daily readings and themes

**Plans**:
- Chronological (365 days) - Read in historical order
- One Year (365 days) - Systematic OT/NT/Psalms/Proverbs
- New Testament (90 days)
- Gospels & Acts (30 days)
- Psalms & Proverbs (60 days)
- Pentateuch (50 days)
- Prophets (90 days)
- Paul's Epistles (30 days)

**Structure**:
```json
{
  "chronological_plan": {
    "1": ["Genesis 1-3"],
    "2": ["Genesis 4-7"],
    ...
  }
}
```

**Used by**: `reading_plans.py`, `/reading-plans` pages

---

### `cross_references/` (66 files, 9.0 MB combined)
**Contains**: Comprehensive cross-reference system linking related Bible verses based on Treasury of Scripture Knowledge, split per book for efficient loading

**Files**: `genesis.json`, `john.json`, `revelation.json`, etc. (one file per book)

**Structure** (per file):
```json
{
  "Genesis:1:1": [
    {
      "ref": "Hebrews 11:3",
      "note": "Creation"
    },
    {
      "ref": "Isaiah 45:18",
      "note": "Creation"
    }
  ],
  "Genesis:1:9": [
    {
      "ref": "2 Peter 3:5",
      "note": "References God"
    }
  ]
}
```

**Coverage**:
- 24,900+ verses with cross-references (80% of Bible)
- 120,858 total cross-reference entries
- Average 4.9 references per verse
- Quality filtered (minimum 3 community votes)
- Limited to top 10 references per verse

**Source**: [OpenBible.info Cross-References](https://www.openbible.info/labs/cross-references/) (CC-BY)

**Used by**: `cross_references.py`, verse detail pages with cross-reference links

**Performance**: Split per book allows lazy loading—only loads cross-references for the requested book

---

### `biblical_timeline.json` (65K)
**Contains**: Major biblical events with dates, descriptions, and verse references

**Structure**:
```json
{
  "events": [
    {
      "date": "~4004 BC",
      "title": "Creation",
      "description": "...",
      "verses": ["Genesis 1:1", ...],
      "category": "Beginning"
    }
  ]
}
```

**Used by**: `routes/biblical_timeline.py`, `/biblical-timeline` page

---

### `biographies.json` (143K)
**Contains**: Biographical information for 127 biblical figures with life events, key verses, and significance

**Structure**:
```json
{
  "biographies": {
    "Abraham": {
      "summary": "...",
      "significance": "...",
      "key_events": [
        {
          "age": 75,
          "event": "Called by God to leave Ur",
          "verse": "Genesis 12:1-4"
        }
      ]
    }
  }
}
```

**Coverage**: 127 biblical figures including Adam, Noah, Abraham, Moses, David, Jesus, all apostles, prophets, and notable women

**Used by**: Biography pages, family tree integration, study resources

---

## Metadata & Configuration

### `chapter_explanations.json` (1.9K)
**Contains**: Explanatory text for popular/significant Bible chapters

**Structure**:
```json
{
  "John": {
    "3": "Contains John 3:16 - 'For God so loved the world'...",
    "1": "The Word became flesh - Jesus as the eternal Logos..."
  }
}
```

**Used by**: `utils/helpers.py`, chapter popularity explanations

---

### `popular_chapters.json` (1.9K)
**Contains**: Popularity scores (1-10) for chapters and high readership books

**Structure**:
```json
{
  "popular_chapters": {
    "John": {"3": 10, "1": 9},
    "Psalms": {"23": 10, "91": 9}
  },
  "high_readership_books": ["Matthew", "Mark", "Luke", "John", ...]
}
```

**Used by**: `utils/helpers.py`, chapter popularity scoring

---

### `featured_verses.json` (1.6K)
**Contains**: 31 featured verses for verse-of-the-day rotation

**Structure**:
```json
{
  "verses": [
    {"book": "John", "chapter": 3, "verse": 16},
    {"book": "Psalms", "chapter": 23, "verse": 1},
    ...
  ]
}
```

**Used by**: `utils/helpers.py`, verse-of-the-day feature (rotates by day of year)

---

### `resource_slugs.json` (1.8K)
**Contains**: URL slugs for all resource types used in sitemap generation

**Structure**:
```json
{
  "study_guides": ["sermon-on-the-mount", "lords-prayer", ...],
  "angels": ["michael", "gabriel", "lucifer", "abaddon"],
  "prophets": ["moses", "elijah", "isaiah", ...],
  ...
}
```

**Resource Types**: study_guides, angels, prophets, names_of_god, parables, covenants, apostles, women, festivals, fruits_of_spirit, and more

**Used by**: `routes/utility.py`, sitemap.xml generation

---

### `schemas/` (9 files)
**Contains**: JSON Schema validation files and Pydantic models for data structure validation

**Files**: `red_letter_verses.schema.json`, book introduction schemas, and other validation files

**Used by**: Data validation during development and CI/CD

---

## Story Resources

### `stories/` Directory (24 files)
**Contains**: Biblical stories organized by category for narrative study

**Files**: `01_creation.json`, `02_patriarchs.json`, `03_job_suffering.json`, etc.

**Structure**:
```json
{
  "category": "Creation and Early Earth",
  "slug": "creation",
  "description": "...",
  "stories": [
    {
      "title": "The Seven Days of Creation",
      "slug": "seven-days-creation",
      "summary": "...",
      "key_verses": [...],
      "content": "...",
      "age_appropriate": ["kids", "teens", "adults"]
    }
  ]
}
```

**Categories**: Creation, Patriarchs, Job, Exodus, Conquest, Judges, Kings, Prophets, Exile, Jesus' Birth, Jesus' Ministry, Miracles, Parables, Crucifixion/Resurrection, Early Church, Paul's Journeys

**Used by**: `stories.py`, `routes/stories.py`, `/stories` pages

---

## Editing Guidelines

### JSON Format
- **Encoding**: UTF-8
- **Indentation**: 2 spaces (no tabs)
- **Line Endings**: LF (Unix-style)
- **Trailing Commas**: Not allowed in JSON
- **Quotes**: Use double quotes for strings

### Validation
After editing any JSON file, validate with:
```bash
# Test JSON syntax
python -m json.tool kjvstudy_org/data/your_file.json > /dev/null

# Run application tests
uv run pytest tests/ -v
```

### Best Practices

1. **Verse References**: Use consistent format: `"Book Chapter:Verse"` (e.g., `"John 3:16"`)
2. **Book Names**: Use full canonical names matching `bible_metadata.json`
3. **HTML in Content**: Use `<strong>`, `<em>`, `<br>` for formatting (will be rendered in templates)
4. **Slugs**: Use lowercase with hyphens (e.g., `"sermon-on-the-mount"`)
5. **Hebrew/Greek**: Ensure UTF-8 encoding preserved for special characters
6. **Descriptions**: Keep concise, clear, and theologically accurate

### Adding New Content

**New Study Guide**:
1. Add to appropriate category in `study_guides/` (catalog entry + content)
2. Add full content with sections to `content` object
3. Add slug to `resource_slugs.json` under `study_guides`
4. Test with: `curl http://localhost:8000/study-guides/your-slug`

**New Resource**:
1. Add to appropriate category file in `resources/`
2. Add slug to `resource_slugs.json`
3. Update sitemap in `routes/utility.py` if needed
4. Test resource page rendering

**New Topic**:
1. Add to the appropriate file in `topics/` with description and subtopics
2. Include verse references in standard format
3. Test with: `/topics/Your-Topic`

---

## Data Sources & Credits

### Original Sources
- **Bible Text**: King James Version 1769 Cambridge Edition (public domain)
- **Interlinear Data**: [tahmmee/interlinear_bibledata](https://github.com/tahmmee/interlinear_bibledata) repository (public domain)
- **Strong's Numbers**: Strong's Exhaustive Concordance (public domain)
- **Cross References**: [OpenBible.info](https://www.openbible.info/labs/cross-references/) based on Treasury of Scripture Knowledge (CC-BY)
- **Book Introductions**: Compiled from public domain Bible study resources

### Content Creation
- **Study Guides**: Original content created for KJV Study
- **Commentary**: Original theological analysis
- **Word Studies**: Compiled from multiple lexical sources
- **Stories**: Retold from biblical narrative text

### Theological Review
All theological content has been reviewed for:
- Biblical accuracy
- Doctrinal soundness
- Historical context
- Practical application

---

## File Sizes & Performance

### Optimization Strategies

1. **Compression**: `interlinear.json.gz` compressed with gzip (141 MB → 12 MB, 91% reduction)
2. **Lazy Loading**: Interlinear data loaded on first access via `interlinear_loader.py`
3. **Caching**: All JSON loaders use `@lru_cache` for single-load-per-process
4. **Separation**: Large resources split into individual files (books, stories)

### Loading Performance

| File | Size | Load Time* | Cache |
|------|------|-----------|-------|
| bible_metadata.json | 5.7K | <1ms | Yes |
| study_guides/ | 265K (combined) | ~10ms | Yes (per-file merge) |
| resources/ | 1.3M (combined) | ~50ms | Yes (per-file load & merge) |
| interlinear.json.gz | 12M | ~500ms | Yes (lazy) |

*Approximate times on modern hardware

### Memory Usage
- **Total Data**: ~58 MB uncompressed (including verse commentary)
- **Peak Memory**: ~60 MB with all data cached (excluding interlinear)
- **Interlinear**: ~140 MB when decompressed and cached (lazy loaded)
- **Verse Commentary**: ~28 MB (lazy loaded per book)
- **Cross-references**: ~9 MB (lazy loaded per book)

---

## Version Control

### Git LFS
Not currently using Git LFS, but `interlinear.json.gz` (12M) could benefit if repository size becomes an issue.

### .gitignore
The following files are ignored:
- `__pycache__/`
- `*.pyc`
- `interlinear_data.py` (deprecated, replaced by `interlinear.json.gz`)

### Backup Strategy
All JSON files are version controlled in Git. For production deployments:
1. Verify JSON integrity before commit
2. Test application after data changes
3. Use feature branches for major content updates
4. Tag releases for stable data versions

---

## Troubleshooting

### Common Issues

**JSON Syntax Error**
```bash
# Validate JSON syntax
python -m json.tool data/your_file.json
```

**Missing Data**
- Check file exists: `ls -lh kjvstudy_org/data/`
- Check file permissions: `chmod 644 kjvstudy_org/data/*.json`
- Check encoding: `file kjvstudy_org/data/your_file.json` (should show UTF-8)

**Interlinear Data Not Loading**
```bash
# Check compressed file exists
ls -lh kjvstudy_org/data/interlinear.json.gz

# Test decompression
gunzip -c kjvstudy_org/data/interlinear.json.gz | head -100
```

**Cache Issues**
- Restart application to clear `@lru_cache`
- Check for stale imports in Python
- Verify no hardcoded data remains in `.py` files

---

## Development Workflow

### Typical Data Update Flow

1. **Edit JSON file** in your editor with proper syntax highlighting
2. **Validate syntax**: `python -m json.tool data/file.json > /dev/null`
3. **Test locally**: `uv run uvicorn kjvstudy_org.server:app --reload`
4. **Run tests**: `uv run pytest tests/ -v`
5. **Commit changes**: `git add data/file.json && git commit -m "Update: ..."`
6. **Deploy**: Changes automatically deployed via CI/CD

### Testing Changes

```bash
# Test specific functionality
uv run pytest tests/test_advanced_routes.py::TestStudyGuidesRoutes -v

# Test all routes
uv run pytest tests/test_web_routes.py -v

# Test API endpoints
uv run pytest tests/test_api.py -v
```

---

## Future Enhancements

### Potential Additions
- [ ] **Concordance Data**: Complete Strong's concordance in JSON
- [ ] **Lexicon Data**: Full Hebrew/Greek lexicons
- [ ] **Maps Data**: GeoJSON for biblical locations
- [ ] **Chronology Data**: Detailed timeline with BCE/CE dates
- [ ] **Manuscript Data**: Textual variants and manuscript information
- [ ] **Archaeological Data**: Historical/archaeological context

### Format Improvements
- [x] **JSON Schema**: Add JSON schema validation files (added `schemas/red_letter_verses.schema.json`)
- [ ] **TypeScript Types**: Generate TypeScript interfaces from JSON
- [ ] **API Versioning**: Version data files for backward compatibility
- [ ] **Multilingual**: Support for multiple Bible translations

---

## Questions & Support

For questions about data structure or content:
- **GitHub Issues**: https://github.com/kennethreitz/kjvstudy.org/issues
- **Documentation**: See `CLAUDE.md` for development notes
- **API Docs**: http://localhost:8000/api/docs

---

*Last Updated: 2025-12-01*
*Total Files: 359 JSON files + 9 schema files*
*Total Size: ~58 MB (including 28 MB verse commentary, 12 MB compressed interlinear, 9 MB cross-references)*

**File Breakdown:**
- Root-level: 11 files
- Books: 66 files
- Verse Commentary: 64 files (missing: Song of Solomon, Habakkuk, Haggai)
- Cross-references: 66 files
- Study Guides: 36 files
- Topics: 36 files
- Resources: 39 files
- Stories: 24 files
- Reading Plans: 6 files
- Strong's: 2 files
- Schemas: 9 files
