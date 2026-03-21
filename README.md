# KJV Study

A scholarly web application for deep study of the King James Bible — pairing the 1769 Cambridge text with original language tools, AI-powered commentary, and classical typography inspired by Edward Tufte.

**[kjvstudy.org](https://kjvstudy.org)**

---

## Overview

KJV Study provides the complete King James Bible (31,102 verses) alongside an extensive suite of research tools: interlinear Hebrew and Greek analysis, Strong's Concordance, cross-references, topical indexes, genealogies, reading plans, and verse-by-verse AI commentary. The entire application is served as a fast, accessible web experience with a full REST API.

```bash
git clone https://github.com/kennethreitz/kjvstudy.org.git
cd kjvstudy.org
docker compose up
# → http://localhost:8000
```

---

## Features

### Scripture

- **31,102 verses** from the 1769 Cambridge KJV edition — [browse all 66 books](https://kjvstudy.org/books)
- [Full-text search](https://kjvstudy.org/search) with SQLite-backed concordance
- [Cross-references](https://kjvstudy.org/book/John/chapter/3/verse/16) throughout Scripture
- [Red Letter edition](https://kjvstudy.org/red-letter) highlighting the words of Christ
- [Verse of the Day](https://kjvstudy.org/verse-of-the-day) and [Random Verse](https://kjvstudy.org/random-verse)

### Original Languages

- **[Interlinear Bible](https://kjvstudy.org/interlinear)** — word-by-word Greek (NT) and Hebrew (OT) with morphological tagging, grammatical parsing, root word exploration, and occurrence tracking
- **[Strong's Concordance](https://kjvstudy.org/strongs)** — [8,674 Hebrew](https://kjvstudy.org/strongs/hebrew) and [5,624 Greek](https://kjvstudy.org/strongs/greek) entries with definitions, transliterations, pronunciation, and derivations

### Commentary

AI-powered [verse-by-verse theological analysis](https://kjvstudy.org/book/John/chapter/3/verse/16) with chapter overviews, book summaries, historical context, word studies, and reflection questions — generated for all 66 books.

### Study Resources

| | |
|---|---|
| **Theology** | [Christology](https://kjvstudy.org/christology), [Soteriology](https://kjvstudy.org/soteriology), [Eschatology](https://kjvstudy.org/eschatology), [Pneumatology](https://kjvstudy.org/pneumatology) |
| **People** | [Twelve Apostles](https://kjvstudy.org/the-twelve-apostles), [Women of the Bible](https://kjvstudy.org/women-of-the-bible), [Prophets](https://kjvstudy.org/biblical-prophets), [Angels](https://kjvstudy.org/biblical-angels) |
| **Themes** | [Parables](https://kjvstudy.org/parables), [Covenants](https://kjvstudy.org/biblical-covenants), [Names of God](https://kjvstudy.org/names-of-god), [Fruits of the Spirit](https://kjvstudy.org/fruits-of-the-spirit) |
| **History** | [Timeline](https://kjvstudy.org/biblical-timeline), [Maps](https://kjvstudy.org/biblical-maps), [Festivals](https://kjvstudy.org/biblical-festivals) |
| **Guides** | [Gospel](https://kjvstudy.org/study-guides/gospel), [Salvation](https://kjvstudy.org/study-guides/salvation), [New Believer](https://kjvstudy.org/study-guides/new-believer), [Prayer & Faith](https://kjvstudy.org/study-guides/prayer-faith), &c. |
| **Plans** | [One-Year Bible](https://kjvstudy.org/reading-plans/one-year), [90-Day NT](https://kjvstudy.org/reading-plans/90-day-nt), [Chronological](https://kjvstudy.org/reading-plans/chronological), &c. |

39 resource categories, 36 study guides, 36 topical indexes, 12 reading plans, 25+ biblical stories (with children's versions).

### Family Trees

[429+ biblical figures](https://kjvstudy.org/family-tree) across 77+ generations from Adam through the New Testament — with interactive ancestor/descendant navigation, biographical data, and GEDCOM-based genealogy.

### PDF Export

Downloadable PDFs for verses, chapters, books, study guides, stories, and reading plans.

### Accessibility

Keyboard navigation (Vim-style and arrow keys), screen reader support, text-to-speech, dark mode with system preference detection, and adjustable font sizes. See [/accessibility](https://kjvstudy.org/accessibility).

---

## Architecture

```
kjvstudy_org/
├── server.py                # FastAPI application
├── kjv.py                   # Bible text access
├── routes/                  # 16 route modules
├── utils/                   # Search, PDF, commentary helpers
├── templates/               # 77 Jinja2 templates
├── static/                  # Tufte CSS, ET Book fonts, JS
└── data/                    # Bible text, commentary, interlinear,
                             # Strong's, cross-references, topics,
                             # study guides, reading plans, stories,
                             # genealogy, timeline, and more
```

| | |
|---|---|
| **Backend** | FastAPI, Python 3.13, Gunicorn |
| **Frontend** | Tufte CSS, ET Book, vanilla JS |
| **Data** | JSON, SQLite (search), gzip (interlinear) |
| **PDF** | WeasyPrint |
| **Packaging** | uv |
| **Infrastructure** | Docker, nginx, Fly.io |
| **CI/CD** | GitHub Actions |

---

## API

Full REST API with [interactive documentation](https://kjvstudy.org/api/docs).

```
GET /api/verse/{book}/{chapter}/{verse}
GET /api/verse-range/{book}/{chapter}/{start}/{end}
GET /api/books/{book}/chapters/{chapter}
GET /api/search?q={query}
GET /api/interlinear/{book}/{chapter}/{verse}
GET /api/strongs/{number}
GET /api/cross-references/{book}/{chapter}/{verse}
GET /api/topics/{topic}
GET /api/reading-plans/{plan}
GET /api/verse-of-the-day
GET /api/bible
```

All endpoints support book name abbreviations (Gen, Ex, Mt, Rev, &c.).

---

## Development

```bash
# With Docker (recommended)
docker compose up

# Without Docker (requires Python 3.13+ and uv)
uv sync
uv run kjvstudy-org

# Tests (941 tests across 16 files)
uv run pytest tests/ -v

# Data validation
uv run python scripts/validate_data.py
```

## Deployment

Deployed to [Fly.io](https://fly.io) with `fly deploy`. Production runs behind nginx for static asset caching, with Gunicorn/Uvicorn serving the FastAPI application. Health checks, auto-recovery, and HTTPS are configured out of the box.

---

## License

ISC License. See [LICENSE](LICENSE).

---

*"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth."*
— 2 Timothy 2:15
