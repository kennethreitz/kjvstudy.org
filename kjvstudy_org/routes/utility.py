"""Utility routes for KJV Study - sitemap, robots.txt, health checks."""
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import Response

from ..kjv import bible
from ..topics import get_all_topics

router = APIRouter(tags=["Utility"])

# Sitemap cache
_sitemap_cache = None
_sitemap_cache_date = None

# Study guide slugs for sitemap (extracted from study_guides module)
STUDY_GUIDE_SLUGS = [
    "sermon-on-the-mount", "lords-prayer", "beatitudes", "fruit-of-spirit",
    "armor-of-god", "ten-commandments", "parables-of-jesus", "miracles-of-jesus",
    "names-of-god", "attributes-of-god", "trinity", "holy-spirit",
    "salvation", "justification", "sanctification", "redemption",
]


@router.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "kjv-study"}


@router.get("/robots.txt", response_class=Response)
def robots_txt():
    """Generate robots.txt for search engine crawlers"""
    robots_content = """User-agent: *
Allow: /
Disallow: /api/

# Sitemap location
Sitemap: https://kjvstudy.org/sitemap.xml

# Crawl delay (be nice to our servers)
Crawl-delay: 1
"""
    return Response(content=robots_content, media_type="text/plain")


@router.get("/sitemap.xml", response_class=Response)
def sitemap():
    """Generate comprehensive sitemap.xml with all URLs (cached daily)"""
    global _sitemap_cache, _sitemap_cache_date

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Return cached sitemap if it's from today
    if _sitemap_cache is not None and _sitemap_cache_date == current_date:
        return Response(content=_sitemap_cache, media_type="application/xml")

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
        <loc>{base_url}/concordance</loc>
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
"""

    # Study guide slugs
    for slug in STUDY_GUIDE_SLUGS:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/study-guides/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    # Reading plan IDs
    reading_plan_ids = [
        "chronological", "one-year", "new-testament", "gospels-acts",
        "psalms-proverbs", "pentateuch", "prophets", "paul-epistles"
    ]
    for plan_id in reading_plan_ids:
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
    angel_slugs = ["michael", "gabriel", "lucifer", "abaddon"]
    for slug in angel_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-angels/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    prophet_slugs = ["moses", "elijah", "isaiah", "jeremiah", "ezekiel", "daniel", "jonah", "john-the-baptist"]
    for slug in prophet_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-prophets/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    god_name_slugs = ["elohim", "yahweh", "adonai", "el-shaddai", "yahweh-jireh", "yahweh-rapha", "yahweh-nissi", "yahweh-shalom", "yahweh-tsidkenu", "yahweh-shammah"]
    for slug in god_name_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/names-of-god/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    parable_slugs = ["sower", "wheat-tares", "mustard-seed", "good-samaritan", "prodigal-son", "lost-sheep", "talents", "wise-foolish-builders"]
    for slug in parable_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/parables/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    covenant_slugs = ["noahic", "abrahamic", "mosaic", "davidic", "new-covenant"]
    for slug in covenant_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-covenants/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    apostle_slugs = ["peter", "andrew", "james-son-of-zebedee", "john", "philip", "bartholomew", "thomas", "matthew", "james-son-of-alphaeus", "thaddaeus", "simon-zealot", "judas-iscariot"]
    for slug in apostle_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/the-twelve-apostles/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    women_slugs = ["eve", "sarah", "rebekah", "rachel", "miriam", "deborah", "ruth", "hannah", "esther", "mary-mother-of-jesus", "mary-magdalene", "martha"]
    for slug in women_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/women-of-the-bible/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    festival_slugs = ["passover", "unleavened-bread", "firstfruits", "pentecost", "trumpets", "atonement", "tabernacles"]
    for slug in festival_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/biblical-festivals/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    fruit_slugs = ["love", "joy", "peace", "longsuffering", "gentleness", "goodness", "faith", "meekness", "temperance"]
    for slug in fruit_slugs:
        sitemap_xml += f"""    <url>
        <loc>{base_url}/fruits-of-the-spirit/{slug}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
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

        # Add book commentary URLs
        sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/commentary</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

        # Add all chapter URLs and verse URLs for each book
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
        for chapter in chapters:
            sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
"""
            # Add chapter commentary
            sitemap_xml += f"""    <url>
        <loc>{base_url}/commentary/{book}/{chapter}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
"""

            # Add all verse URLs for this chapter
            verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
            for verse_num in range(1, len(verses) + 1):
                sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}/verse/{verse_num}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.5</priority>
    </url>
"""

    sitemap_xml += "</urlset>"

    # Cache the generated sitemap
    _sitemap_cache = sitemap_xml
    _sitemap_cache_date = current_date

    return Response(content=sitemap_xml, media_type="application/xml")
