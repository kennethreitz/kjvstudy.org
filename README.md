# KJV Study - AI-Powered Biblical Commentary Platform

A modern, responsive web application for studying the King James Version of the Bible with AI-generated commentary and insights.

## 🎯 Vision

This project aims to create an intelligent Bible study platform that combines the timeless text of the KJV with modern AI technology to provide:

- **Deep Scriptural Analysis**: AI-generated commentary that explores historical context, theological themes, and cross-references
- **Personalized Study Paths**: Adaptive learning that adjusts to individual study patterns and interests
- **Interactive Exploration**: Dynamic connections between passages, themes, and concepts
- **Scholarly Insights**: Commentary that draws from centuries of biblical scholarship and interpretation
- **Accessible Learning**: Making deep biblical study available to everyone, regardless of theological background

## ✨ Features

### Current Features
- **Clean, Responsive Design**: Modern interface optimized for reading and study
- **Complete KJV Text**: Full biblical text with chapter and verse navigation
- **Intuitive Navigation**: Easy browsing through books, chapters, and verses
- **Mobile-First Design**: Optimized for smartphones, tablets, and desktop
- **Fast Performance**: Built with FastAPI for quick loading and responsive interactions

### Planned AI Commentary Features
- **Verse-by-Verse Commentary**: AI-generated insights for every verse
- **Historical Context**: Background information on cultural, historical, and geographical context
- **Theological Themes**: Identification and explanation of key theological concepts
- **Cross-References**: Intelligent linking to related passages throughout Scripture
- **Study Questions**: Thought-provoking questions to deepen understanding
- **Sermon Outlines**: AI-generated preaching and teaching materials
- **Devotional Insights**: Daily application and spiritual reflection prompts
- **Academic Analysis**: Scholarly examination of original languages, manuscripts, and interpretations

### Advanced AI Capabilities (Future)
- **Personalized Commentary**: Tailored insights based on reading history and interests
- **Comparative Analysis**: Side-by-side comparison with other translations and versions
- **Topical Studies**: AI-curated studies on specific themes (e.g., prophecy, parables, covenant)
- **Interactive Q&A**: Natural language interface for asking questions about passages
- **Study Group Features**: Collaborative tools for group study and discussion
- **Audio Commentary**: AI-generated spoken commentary and explanations

## 🛠 Technology Stack

- **Backend**: FastAPI (Python) - High-performance web framework
- **Frontend**: Modern HTML5, CSS3, and vanilla JavaScript
- **Templates**: Jinja2 templating for dynamic content
- **Data**: JSON-based Bible text storage for fast access
- **AI Integration**: Planned integration with GPT-4, Claude, or other LLMs
- **Deployment**: Docker-ready for easy deployment

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- UV (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kjvstudy.org
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the development server**
   ```bash
   uv run python -m kjvstudy
   ```

4. **Open your browser**
   Navigate to `http://localhost:8000`

### Project Structure
```
kjvstudy.org/
├── kjvstudy/           # Main application package
│   ├── __init__.py
│   ├── __main__.py     # Application entry point
│   ├── kjv.py          # Bible text data handling
│   └── server.py       # FastAPI web server
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Home page - book selection
│   ├── book.html       # Chapter listing for a book
│   └── chapter.html    # Verse display for a chapter
├── static/             # CSS, JavaScript, and assets
│   └── style.css       # Main stylesheet
├── verses-1769.json    # Complete KJV text data
└── pyproject.toml      # Project dependencies and config
```

## 🤖 AI Commentary Implementation Plan

### Phase 1: Basic Commentary Generation
- Integrate with OpenAI GPT-4 or Anthropic Claude
- Generate verse-by-verse commentary for popular passages
- Store generated commentary in database for performance
- Add commentary display in the chapter view

### Phase 2: Enhanced Analysis
- Historical and cultural context generation
- Cross-reference identification and linking
- Theological theme extraction and explanation
- Integration with Bible dictionaries and concordances

### Phase 3: Interactive Features
- Natural language Q&A about passages
- Personalized study recommendations
- Custom study plan generation
- Advanced search with semantic understanding

### Phase 4: Community and Collaboration
- User-generated notes and insights
- Community discussion features
- Study group creation and management
- Sharing and bookmarking capabilities

## 🎨 Design Philosophy

### Typography and Reading Experience
- **Serif fonts** for Scripture text to enhance readability
- **Optimal line spacing** and margins for extended reading
- **Responsive text sizing** that adapts to screen size and user preferences
- **High contrast** for accessibility and eye comfort

### User Interface
- **Minimalist design** that keeps focus on the text
- **Intuitive navigation** that doesn't distract from study
- **Progressive disclosure** of features to avoid overwhelming new users
- **Consistent visual hierarchy** throughout the application

### Performance
- **Fast loading times** for immediate access to Scripture
- **Efficient caching** of frequently accessed content
- **Progressive enhancement** for users with slower connections
- **Offline capability** for core reading features (planned)

## 🔮 Future Enhancements

### Content Expansion
- Multiple Bible translations and versions
- Original language tools (Hebrew, Greek)
- Historical Bible versions and manuscripts
- Integration with Bible atlases and timelines

### Study Tools
- Note-taking and highlighting system
- Bible reading plans and tracking
- Prayer journal integration
- Scripture memorization tools

### AI-Powered Features
- Automatic sermon generation from passages
- Bible study curriculum creation
- Personalized devotional content
- Intelligent study group matching

### Community Features
- User profiles and study progress tracking
- Discussion forums for passage exploration
- Expert commentary from biblical scholars
- Live streaming of Bible studies and sermons

## 🤝 Contributing

We welcome contributions from developers, theologians, and Bible enthusiasts! Here's how you can help:

### For Developers
- Frontend improvements and responsive design
- Backend optimization and new features
- AI integration and commentary generation
- Testing and quality assurance

### For Biblical Scholars
- Content review and theological accuracy
- Historical and cultural context insights
- Cross-reference suggestions and verification
- Study question and outline creation

### For Users
- Bug reports and feature requests
- User experience feedback
- Beta testing of new features
- Community building and engagement

## 📄 License

This project is open source and available under the [ISC License](LICENSE).

## 🙏 Acknowledgments

- **King James Bible (1769)**: The foundational text that makes this project possible
- **FastAPI Community**: For the excellent web framework
- **Open Source Community**: For the tools and libraries that power this application
- **Biblical Scholars**: Whose centuries of study inform our AI commentary approach

## 📞 Contact

For questions, suggestions, or collaboration opportunities:
- Create an issue on GitHub
- Join our community discussions
- Follow development updates

---

*"Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth."* - 2 Timothy 2:15 (KJV)
