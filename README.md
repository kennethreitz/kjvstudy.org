# KJV Study

A comprehensive web application for deep study of the King James Bible, featuring original language tools, extensive theological resources, and classical scholarly presentation.

**Live Site:** [kjvstudy.org](https://kjvstudy.org)

## Quick Start - Run It Yourself

The easiest way to run KJV Study locally is with Docker:

```bash
# Clone the repository
git clone https://github.com/kennethreitz/kjvstudy.org.git
cd kjvstudy.org

# Start with Docker Compose
docker compose up
```

Then open your browser to **http://localhost:8000**

That's it! The application will run with all features enabled.

---

## Features

### Bible Reading & Navigation
- **[Complete KJV Text](https://kjvstudy.org/books)** - All 66 books, 1,189 chapters, 31,102 verses
- **[Fast Search](https://kjvstudy.org/search)** - Full-text search with concordance functionality
- **[Cross-References](https://kjvstudy.org/book/John/chapter/3/verse/16)** - Comprehensive verse cross-referencing throughout Scripture
- **Verse Linking** - Automatic URL generation for easy sharing and bookmarking
- **[Random Verse](https://kjvstudy.org/random-verse)** - Discover Scripture serendipitously
- **[Verse of the Day](https://kjvstudy.org/verse-of-the-day)** - Daily curated verses with reflection questions

### Study Tools

#### [Interlinear Bible](https://kjvstudy.org/interlinear)
- Greek and Hebrew original language texts
- Word-by-word translation analysis
- Strong's concordance numbers
- Etymology and root word exploration
- Morphological tagging

#### [Study Guides](https://kjvstudy.org/study-guides)
Comprehensive 8-section guides with extensive Scripture references:
- **[The Gospel Message](https://kjvstudy.org/study-guides/gospel)** - Nature of gospel, Christ's atonement, repentance & faith
- **[Salvation by Grace](https://kjvstudy.org/study-guides/salvation)** - Sin, penalty, grace, justification, eternal security
- **[New Believer's Guide](https://kjvstudy.org/study-guides/new-believer)** - Foundational truths for new Christians
- **[Fruits of the Spirit](https://kjvstudy.org/study-guides/fruits-spirit)** - Source, cultivation, and evidence of spiritual fruit
- **[Prayer & Faith](https://kjvstudy.org/study-guides/prayer-faith)** - Nature of prayer, biblical faith, growing in both
- **[Christian Living](https://kjvstudy.org/study-guides/christian-living)** - Holiness, separation, stewardship, perseverance
- **[God's Love](https://kjvstudy.org/study-guides/gods-love)** - Essential nature, covenant faithfulness, responding to love
- **[Hope & Comfort](https://kjvstudy.org/study-guides/hope-comfort)** - God as refuge, resurrection hope, blessed hope
- **[Wisdom & Guidance](https://kjvstudy.org/study-guides/wisdom-guidance)** - Fear of the Lord, discerning God's will, godly counsel

#### Biblical Resources

**People & Characters:**
- **[The Twelve Apostles](https://kjvstudy.org/the-twelve-apostles)** - Detailed profiles with biblical accounts
- **[Women of the Bible](https://kjvstudy.org/women-of-the-bible)** - Key female figures and their significance
- **[Biblical Prophets](https://kjvstudy.org/biblical-prophets)** - Major and minor prophets with historical context
- **[Biblical Angels](https://kjvstudy.org/biblical-angels)** - Angelic beings and their roles

**Themes & Topics:**
- **[Parables of Jesus](https://kjvstudy.org/parables)** - Complete collection with interpretation
- **[Names of God](https://kjvstudy.org/names-of-god)** - Revealing God's character through His names
- **[The Tetragrammaton](https://kjvstudy.org/tetragrammaton)** - Deep dive into YHWH
- **[Biblical Covenants](https://kjvstudy.org/biblical-covenants)** - Adamic, Noahic, Abrahamic, Mosaic, Davidic, New
- **[Fruits of the Spirit](https://kjvstudy.org/fruits-of-the-spirit)** - Greek word studies and theological exposition
- **[Biblical Festivals](https://kjvstudy.org/biblical-festivals)** - Passover, Pentecost, Tabernacles, and more
- **[Topical Index](https://kjvstudy.org/topics)** - Scripture organized by theme and subtopic

**Historical Context:**
- **[Biblical Timeline](https://kjvstudy.org/biblical-timeline)** - From Creation through the early Church
- **[Biblical Maps](https://kjvstudy.org/biblical-maps)** - Geographic context for biblical narratives
- **[Family Tree](https://kjvstudy.org/family-tree)** - Genealogies from Adam through biblical history with searchable lineages

### Design & User Experience

**Tufte CSS Styling:**
- Classical typography with serif fonts for optimal readability
- Sidenotes and margin notes for supplementary information
- High contrast and generous white space
- Responsive design that adapts to all screen sizes

**Performance:**
- Aggressive caching for instant page loads
- Optimized for Fly.io deployment
- Always-on configuration eliminates cold starts
- Lazy loading of interlinear data

**Accessibility:**
- Semantic HTML structure
- Clear heading hierarchy
- Keyboard navigation support
- High contrast text

## Tech Stack

**Backend:**
- **FastAPI** - Modern, high-performance Python web framework
- **Python 3.13** - Latest Python with performance improvements
- **Custom Bible Class** - Optimized KJV text access with 31,102 verses from 1769 Cambridge edition
- **Jinja2** - Server-side templating with custom filters

**Frontend:**
- **Tufte CSS** - Edward Tufte-inspired classical design
- **Vanilla JavaScript** - Minimal client-side code for enhanced functionality
- **Semantic HTML** - Accessible, well-structured markup

**Infrastructure:**
- **Docker** - Containerized deployment
- **Fly.io** - Production hosting with global CDN
- **uv** - Fast Python package management

## Installation

### Docker (Recommended)

See the [Quick Start](#quick-start---run-it-yourself) section above for the easiest way to run locally.

**Alternative Docker commands:**
```bash
# Build and run manually
docker build -t kjvstudy .
docker run -p 8000:8000 kjvstudy
```

### Python Development

For development without Docker:

**Prerequisites:**
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

**Steps:**
```bash
# Install dependencies
uv sync

# Run the development server
uv run kjvstudy-org

# Open http://localhost:8000
```

## Deployment

### Fly.io Deployment

The application is optimized for Fly.io with:
- 2GB RAM, shared CPU (2 cores)
- Always-on configuration (min 1 machine)
- Preloaded interlinear data for fast responses
- Health checks and automatic recovery

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login to Fly
fly auth login

# Deploy
fly deploy

# View logs
fly logs

# SSH into machine
fly ssh console
```

### Environment Variables

```bash
PYTHONUNBUFFERED=1              # Immediate log output
PYTHONDONTWRITEBYTECODE=1       # Skip .pyc files
PRELOAD_INTERLINEAR=true        # Load interlinear data on startup
```

## Project Structure

```
kjvstudy.org/
├── kjvstudy_org/
│   ├── server.py              # Main FastAPI application
│   ├── kjv.py                 # Bible text access
│   ├── cross_references.py    # Cross-reference data
│   ├── topics.py              # Topical index
│   ├── interlinear_loader.py  # Greek/Hebrew data
│   ├── reading_plans.py       # Bible reading plans
│   ├── templates/             # Jinja2 templates
│   │   ├── base.html         # Base template with Tufte CSS
│   │   ├── verse.html        # Individual verse pages
│   │   ├── study_guides.html # Study guide templates
│   │   └── ...
│   └── static/               # Static assets
├── Dockerfile                # Container configuration
├── fly.toml                  # Fly.io deployment config
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## Contributing

We welcome contributions! Areas where you can help:

**Development:**
- Backend optimization and new features
- Frontend improvements and accessibility
- Mobile app development
- API development for external integrations

**Content:**
- Theological review for accuracy
- Additional study guides and resources
- Original language expertise (Greek/Hebrew)
- Historical and cultural context

**Design:**
- UI/UX improvements
- Accessibility enhancements
- Mobile experience optimization
- Print stylesheet development

**Documentation:**
- Tutorials and how-to guides
- API documentation
- User guides
- Translation to other languages

## Roadmap

**Planned Features:**
- Multiple Bible translations (ESV, NASB, NIV)
- User accounts with note-taking and highlighting
- Bible reading plans with progress tracking
- AI-powered commentary generation
- Mobile applications (iOS/Android)
- Prayer journal integration
- Scripture memorization tools
- Community discussion forums
- Live streaming integration for Bible studies

## License

This project is open source and available under the [ISC License](LICENSE).

## Acknowledgments

- **King James Bible (1769)** - The foundational text
- **FastAPI Community** - Excellent web framework
- **Edward Tufte** - Design philosophy and CSS inspiration
- **Open Source Community** - Tools and libraries that make this possible

---

*"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth."*
— 2 Timothy 2:15 (KJV)
