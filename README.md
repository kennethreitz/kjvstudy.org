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
- **31,102 verses** from the 1769 Cambridge KJV edition
- Full-text search with concordance functionality
- Cross-references throughout Scripture
- Verse of the Day and Random Verse discovery
- Red Letter edition tracking words of Christ

### Original Language Tools

**Interlinear Bible**
- Complete Greek (NT) and Hebrew (OT) word-by-word analysis
- Morphological tagging and grammatical parsing
- Root word exploration and etymology
- Word occurrence tracking across the entire Bible

**Strong's Concordance**
- 8,674 Hebrew entries (H1-H8674)
- 5,624 Greek entries (G1-G5624)
- Definitions, transliterations, pronunciation guides
- Searchable by word, definition, or Strong's number
- Related word derivations and cross-references

### AI-Powered Commentary
- Verse-by-verse theological analysis
- Chapter overviews and book summaries
- Historical and cultural context
- Reflection questions for personal study
- Word studies for key biblical terms

### Study Resources

**39+ Resource Categories:**

| Category | Examples |
|----------|----------|
| Biblical People | Twelve Apostles, Women of the Bible, Prophets, Angels |
| Systematic Theology | Christology, Soteriology, Eschatology, Pneumatology |
| Biblical Themes | Parables, Covenants, Names of God, Fruits of the Spirit |
| Historical Context | Timeline, Maps, Festivals, Family Trees |

**Study Guides:**
- The Gospel Message
- Salvation by Grace
- New Believer's Guide
- Prayer and Faith
- Christian Living
- Hope and Comfort
- Wisdom and Guidance

**Reading Plans:**
- One-Year Bible
- 90-Day New Testament
- Chronological Reading
- Gospels and Acts (30 days)
- Psalms and Proverbs
- And more

### Family Tree Explorer
- 429+ biblical figures with genealogical data
- 77+ generations from Adam through the New Testament
- Interactive ancestor/descendant navigation
- Biographical data and related Scripture references
- GEDCOM-based data with Kekule numbering

### PDF Export
Generate downloadable PDFs for:
- Individual verses, chapters, or entire books
- Study guides and topical collections
- Bible stories (including children's versions)
- Reading plans and resources

### Accessibility
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

Full RESTful API with OpenAPI documentation at `/api/docs`.

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
