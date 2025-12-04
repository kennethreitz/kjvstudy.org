# KJV Study

A comprehensive web application for deep study of the King James Bible, featuring original language tools, AI-powered commentary, extensive theological resources, and classical scholarly presentation.

**Live Site:** [kjvstudy.org](https://kjvstudy.org)

## Quick Start

```bash
git clone https://github.com/kennethreitz/kjvstudy.org.git
cd kjvstudy.org
docker compose up
```

Open **http://localhost:8000** and start studying.

---

## Features

### Complete Bible Text
- [**31,102 verses**](https://kjvstudy.org/books) from the 1769 Cambridge KJV edition
- [Full-text search](https://kjvstudy.org/search) with concordance functionality
- [Cross-references](https://kjvstudy.org/book/John/chapter/3/verse/16) throughout Scripture
- [Verse of the Day](https://kjvstudy.org/verse-of-the-day) and [Random Verse](https://kjvstudy.org/random-verse) discovery
- Red Letter edition tracking words of Christ

### Original Language Tools

**[Interlinear Bible](https://kjvstudy.org/interlinear)**
- Complete Greek (NT) and Hebrew (OT) word-by-word analysis
- Morphological tagging and grammatical parsing
- Root word exploration and etymology
- Word occurrence tracking across the entire Bible

**[Strong's Concordance](https://kjvstudy.org/strongs)**
- [8,674 Hebrew entries](https://kjvstudy.org/strongs/hebrew) (H1-H8674)
- [5,624 Greek entries](https://kjvstudy.org/strongs/greek) (G1-G5624)
- Definitions, transliterations, pronunciation guides
- Searchable by word, definition, or Strong's number
- Related word derivations and cross-references

### AI-Powered Commentary
- [Verse-by-verse theological analysis](https://kjvstudy.org/book/John/chapter/3/verse/16)
- Chapter overviews and book summaries
- Historical and cultural context
- Reflection questions for personal study
- Word studies for key biblical terms

### Study Resources

**39+ Resource Categories:**

| Category | Examples |
|----------|----------|
| Biblical People | [Twelve Apostles](https://kjvstudy.org/the-twelve-apostles), [Women of the Bible](https://kjvstudy.org/women-of-the-bible), [Prophets](https://kjvstudy.org/biblical-prophets), [Angels](https://kjvstudy.org/biblical-angels) |
| Systematic Theology | [Christology](https://kjvstudy.org/christology), [Soteriology](https://kjvstudy.org/soteriology), [Eschatology](https://kjvstudy.org/eschatology), [Pneumatology](https://kjvstudy.org/pneumatology) |
| Biblical Themes | [Parables](https://kjvstudy.org/parables), [Covenants](https://kjvstudy.org/biblical-covenants), [Names of God](https://kjvstudy.org/names-of-god), [Fruits of the Spirit](https://kjvstudy.org/fruits-of-the-spirit) |
| Historical Context | [Timeline](https://kjvstudy.org/biblical-timeline), [Maps](https://kjvstudy.org/biblical-maps), [Festivals](https://kjvstudy.org/biblical-festivals), [Family Trees](https://kjvstudy.org/family-tree) |

**Study Guides:**
- [The Gospel Message](https://kjvstudy.org/study-guides/gospel)
- [Salvation by Grace](https://kjvstudy.org/study-guides/salvation)
- [New Believer's Guide](https://kjvstudy.org/study-guides/new-believer)
- [Prayer and Faith](https://kjvstudy.org/study-guides/prayer-faith)
- [Christian Living](https://kjvstudy.org/study-guides/christian-living)
- &c.

**Reading Plans:**
- [One-Year Bible](https://kjvstudy.org/reading-plans/one-year)
- [90-Day New Testament](https://kjvstudy.org/reading-plans/90-day-nt)
- [Chronological Reading](https://kjvstudy.org/reading-plans/chronological)
- [Gospels and Acts](https://kjvstudy.org/reading-plans/gospels-acts)
- &c.

### [Family Tree Explorer](https://kjvstudy.org/family-tree)
- 429+ biblical figures with genealogical data
- 77+ generations from Adam through the New Testament
- Interactive ancestor/descendant navigation
- Biographical data and related Scripture references
- GEDCOM-based data with Kekule numbering

### PDF Export
Generate downloadable PDFs for:
- Individual verses, chapters, or entire books
- Study guides and topical collections
- [Bible stories](https://kjvstudy.org/stories) (including children's versions)
- Reading plans and resources

### [Accessibility](https://kjvstudy.org/accessibility)
- Full keyboard navigation (Vim-style and arrow keys)
- Screen reader support with semantic HTML
- Text-to-speech for Scripture reading
- Dark mode with system preference detection
- Adjustable font sizes

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.13 |
| Frontend | Tufte CSS, Vanilla JavaScript |
| Data | JSON (Bible text), SQLite (search index), Gzip (interlinear) |
| Infrastructure | Docker, Fly.io |
| Package Management | uv |

---

## API

Full RESTful API with [OpenAPI documentation](https://kjvstudy.org/api/docs).

**Key Endpoints:**
```
GET /api/verse/{book}/{chapter}/{verse}
GET /api/books/{book}/chapters/{chapter}
GET /api/search?q={query}
GET /api/interlinear/{book}/{chapter}/{verse}
GET /api/strongs/{number}
GET /api/cross-references/{book}/{chapter}/{verse}
GET /api/topics/{topic}
GET /api/reading-plans/{plan}
```

---

## Development

### With Docker (Recommended)
```bash
docker compose up
```

### Without Docker
```bash
# Requires Python 3.13+ and uv
uv sync
uv run kjvstudy-org
```

### Running Tests
```bash
uv run pytest tests/ -v
```

100 tests covering API endpoints, edge cases, and web routes.

---

## Deployment

Optimized for Fly.io:

```bash
fly deploy
```

Configuration includes:
- 2GB RAM with shared CPU
- Always-on (no cold starts)
- Preloaded interlinear data
- Health checks and auto-recovery

---

## Project Structure

```
kjvstudy.org/
├── kjvstudy_org/
│   ├── server.py           # FastAPI application
│   ├── kjv.py              # Bible text access (31,102 verses)
│   ├── interlinear_loader.py
│   ├── strongs_loader.py
│   ├── cross_references.py
│   ├── topics.py
│   ├── reading_plans.py
│   ├── routes/             # API and web routes
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS, images
│   └── data/               # JSON data files
├── tests/                  # Test suite
├── Dockerfile
├── fly.toml
└── pyproject.toml
```

---

## Contributing

Contributions welcome in:

- **Development**: Backend features, frontend improvements, API extensions
- **Content**: Theological review, study guides, original language expertise
- **Design**: Accessibility, mobile experience, print stylesheets
- **Documentation**: Tutorials, API docs, translations

---

## License

ISC License. See [LICENSE](LICENSE).

---

*"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth."* — 2 Timothy 2:15
