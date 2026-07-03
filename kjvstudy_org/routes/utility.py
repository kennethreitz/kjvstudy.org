"""Utility routes for KJV Study - sitemap and robots.txt. (Responder port of routes/utility.py)"""
from datetime import datetime
from pathlib import Path
from functools import lru_cache

from ..kjv import bible
from ..topics import get_all_topics
from ..strongs import get_all_strongs
from ..stories import load_all_stories
from ..reading_plans import READING_PLANS
from ..data import get_slugs

# Path to static verse sitemap
_VERSE_SITEMAP_PATH = Path(__file__).parent.parent / "static" / "sitemap-verses.xml"

# Sitemap cache
_sitemap_cache = None
_sitemap_cache_date = None


def register(api):
    # /health is served by Responder's aggregated health checks
    # (health_route= + add_health_check in server.py).

    @api.route("/robots.txt")
    async def robots_txt(req, resp):
        """Generate robots.txt for search engine crawlers"""
        robots_content = """User-agent: *
Allow: /
Disallow: /api/
Disallow: /*/pdf
Disallow: /og/
Disallow: /verse-of-the-day/2
Crawl-delay: 2

# Sitemap location
Sitemap: https://kjvstudy.org/sitemap.xml
"""
        resp.text = robots_content
        resp.mimetype = "text/plain; charset=utf-8"

    @api.route("/sitemap.xml")
    async def sitemap_index(req, resp):
        """Sitemap index - references main sitemap and static verse sitemap"""
        base_url = "https://kjvstudy.org"
        current_date = datetime.now().strftime("%Y-%m-%d")

        sitemap_index_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>{base_url}/sitemap-main.xml</loc>
        <lastmod>{current_date}</lastmod>
    </sitemap>
    <sitemap>
        <loc>{base_url}/sitemap-verses.xml</loc>
        <lastmod>2024-01-01</lastmod>
    </sitemap>
</sitemapindex>
"""
        resp.content = sitemap_index_xml
        resp.mimetype = "application/xml"

    @api.route("/sitemap-verses.xml")
    async def sitemap_verses(req, resp):
        """Serve static verse sitemap (31,102 verses, generated once)"""
        # Check if file exists
        if not _VERSE_SITEMAP_PATH.exists():
            resp.status_code = 404
            resp.text = f"Verse sitemap not found at {_VERSE_SITEMAP_PATH}"
            resp.mimetype = "text/plain"
            return

        resp.content = _VERSE_SITEMAP_PATH.read_bytes()
        resp.mimetype = "application/xml"
        resp.headers["Cache-Control"] = "public, max-age=86400"  # Cache for 1 day
        resp.headers["Content-Encoding"] = "identity"  # Explicitly say it's not compressed

    @api.route("/sitemap-main.xml")
    async def sitemap_main(req, resp):
        """Generate main sitemap with all dynamic URLs (cached daily)"""
        global _sitemap_cache, _sitemap_cache_date

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Return cached sitemap if it's from today
        if _sitemap_cache is not None and _sitemap_cache_date == current_date:
            resp.content = _sitemap_cache
            resp.mimetype = "application/xml"
            return

        # Generate new sitemap
        base_url = "https://kjvstudy.org"

        sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/search</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/study</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/books</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/study-guides</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/reading-plans</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/topics</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/resources</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/verse-of-the-day</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/strongs</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/strongs/hebrew</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/strongs/greek</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/interlinear</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-maps</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/family-tree</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-timeline</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-angels</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-prophets</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/names-of-god</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/tetragrammaton</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/parables</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-covenants</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/the-twelve-apostles</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/women-of-the-bible</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/biblical-festivals</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/fruits-of-the-spirit</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/stories</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/stories/kids</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

        # Add all individual story URLs
        stories_data = load_all_stories()
        for category in stories_data:
            for story in category.get("stories", []):
                slug = story.get("slug", "")
                if slug:
                    sitemap_xml += f"""    <url>
        <loc>{base_url}/stories/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""

        sitemap_xml += f"""    <url>
        <loc>{base_url}/anthropology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/armor-of-god</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/beatitudes</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/bibliology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/blood-in-scripture</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/christology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/ecclesiology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/eschatology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/grace</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/hamartiology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/i-am-statements</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/justification</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/kingdom-of-god</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/law-and-gospel</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/messianic-prophecies</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/miracles-of-jesus</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/names-of-christ</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/personifications</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/pneumatology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/prayers-of-the-bible</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/providence</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/sanctification</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/soteriology</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/spirits-and-demons</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/ten-commandments</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/theology-proper</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/trinity</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/types-and-shadows</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/worship</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

        # Study guide slugs (derived from the actual study-guide content files)
        from ..study_guides import get_study_guides_content as _get_study_guides_content
        for slug in sorted(_get_study_guides_content().keys()):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/study-guides/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Reading plan IDs (derived from the canonical plan registry)
        for plan_id in READING_PLANS:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/reading-plans/{plan_id}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Topic names
        topics = get_all_topics()
        for topic_name in topics.keys():
            sitemap_xml += f"""    <url>
        <loc>{base_url}/topics/{topic_name}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Biblical angels, prophets, names of God, parables, covenants, apostles, women, festivals slugs
        for slug in get_slugs("angels"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-angels/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("prophets"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-prophets/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("names"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/names-of-god/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("parables"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/parables/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("covenants"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-covenants/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("apostles"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/the-twelve-apostles/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("women"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/women-of-the-bible/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("festivals"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-festivals/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        for slug in get_slugs("fruits"):
            sitemap_xml += f"""    <url>
        <loc>{base_url}/fruits-of-the-spirit/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Add all Strong's entries (Hebrew H1-H8674, Greek G1-G5624)
        # Get all Hebrew entries
        hebrew_data = get_all_strongs("hebrew", page=1, per_page=10000)
        for entry in hebrew_data["entries"]:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/strongs/{entry["strongs"]}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""

        # Get all Greek entries
        greek_data = get_all_strongs("greek", page=1, per_page=10000)
        for entry in greek_data["entries"]:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/strongs/{entry["strongs"]}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""

        # Add all book URLs
        books = bible.get_books()
        for book in books:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

            # Add all chapter URLs for each book
            chapters = bible.get_chapters_for_book(book)
            for chapter in chapters:
                sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""
                # Add interlinear URL for each chapter
                sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}/interlinear</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""
                # Note: Individual verse URLs (31,102 total) are in sitemap-verses.xml
                # which is statically generated and referenced in the sitemap index.
                # This keeps the main sitemap fast while maintaining full SEO coverage.

        sitemap_xml += "</urlset>"

        # Cache the generated sitemap
        _sitemap_cache = sitemap_xml
        _sitemap_cache_date = current_date

        resp.content = sitemap_xml
        resp.mimetype = "application/xml"
