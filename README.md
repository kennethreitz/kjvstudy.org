# KJV Study

A comprehensive web application for deep study of the King James Bible, featuring original language tools, extensive theological resources, and classical scholarly presentation.

**Live Site:** [kjvstudy.fly.dev](https://kjvstudy.fly.dev)

## Features

### Bible Reading & Navigation
- **Complete KJV Text** - All 66 books, 1,189 chapters, 31,102 verses
- **Fast Search** - Full-text search with concordance functionality
- **Cross-References** - Comprehensive verse cross-referencing throughout Scripture
- **Verse Linking** - Automatic URL generation for easy sharing and bookmarking
- **Random Verse** - Discover Scripture serendipitously
- **Verse of the Day** - Daily curated verses with reflection questions

### Study Tools

#### Interlinear Bible
- Greek and Hebrew original language texts
- Word-by-word translation analysis
- Strong's concordance numbers
- Etymology and root word exploration
- Morphological tagging

#### Study Guides
Comprehensive 8-section guides with extensive Scripture references:
- **The Gospel Message** - Nature of gospel, Christ's atonement, repentance & faith
- **Salvation by Grace** - Sin, penalty, grace, justification, eternal security
- **New Believer's Guide** - Foundational truths for new Christians
- **Fruits of the Spirit** - Source, cultivation, and evidence of spiritual fruit
- **Prayer & Faith** - Nature of prayer, biblical faith, growing in both
- **Christian Living** - Holiness, separation, stewardship, perseverance
- **God's Love** - Essential nature, covenant faithfulness, responding to love
- **Hope & Comfort** - God as refuge, resurrection hope, blessed hope
- **Wisdom & Guidance** - Fear of the Lord, discerning God's will, godly counsel

#### Biblical Resources

**People & Characters:**
- The Twelve Apostles - Detailed profiles with biblical accounts
- Women of the Bible - Key female figures and their significance
- Biblical Prophets - Major and minor prophets with historical context
- Biblical Angels - Angelic beings and their roles

**Themes & Topics:**
- Parables of Jesus - Complete collection with interpretation
- Names of God - Revealing God's character through His names
- The Tetragrammaton - Deep dive into YHWH
- Biblical Covenants - Adamic, Noahic, Abrahamic, Mosaic, Davidic, New
- Fruits of the Spirit - Greek word studies and theological exposition
- Biblical Festivals - Passover, Pentecost, Tabernacles, and more
- Topical Index - Scripture organized by theme and subtopic

**Historical Context:**
- Biblical Timeline - From Creation through the early Church
- Biblical Maps - Geographic context for biblical narratives
- Family Tree - Genealogies from Adam through biblical history with searchable lineages

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
- **biblepy** - KJV Bible text library
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

### Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kennethreitz/kjvstudy.org.git
   cd kjvstudy.org
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the development server**
   ```bash
   uv run kjvstudy-org
   ```

4. **Open your browser**
   ```
   http://localhost:8000
   ```

### Docker Development

```bash
# Build the image
docker build -t kjvstudy .

# Run the container
docker run -p 8000:8000 kjvstudy

# Or use docker-compose
docker compose up
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
