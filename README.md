# KJV Study

A web application for studying the King James Bible with AI-powered commentary and insights.

## Features

- Browse and search King James Bible verses
- **Study Guides** - Comprehensive Bible study guides covering foundational Christian truths, character development, and biblical themes
- **Verse of the Day** - Daily Scripture verses with reflection questions and sharing capabilities
- AI-powered biblical commentary and insights
- Clean, responsive web interface
- Fast verse lookup and navigation

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

Run the development server:
```bash
uv run kjvstudy-org
```

The application will be available at http://localhost:8000

## New Features

### Study Guides
Access comprehensive Bible study guides at `/study-guides` covering:
- **Foundational Studies**: New Believer's Guide, Salvation by Grace, The Gospel Message
- **Character & Living**: Fruits of the Spirit, Prayer & Faith, Christian Living
- **Biblical Themes**: God's Love, Hope & Comfort, Wisdom & Guidance

Each study guide includes:
- Scripture references with full text
- Study notes and practical applications
- Reflection questions for deeper understanding

### Verse of the Day
Visit `/verse-of-the-day` for:
- Daily Scripture verses from a curated collection
- Reflection questions for meditation
- Easy sharing capabilities
- Links to read the full chapter or book
- Integrated with the homepage for daily inspiration

## Docker

Build and run with Docker:
```bash
docker build -t kjvstudy .
docker run -p 8000:8000 kjvstudy
```

## Requirements

- Python 3.13+
- FastAPI
- biblepy

## License

<<<<<<< HEAD
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
=======
See LICENSE file for details.
>>>>>>> bb2748c (Simplify README documentation)
