#!/usr/bin/env python3
"""
Generate static sitemap for all 31,102 Bible verses.

This sitemap is static because verse URLs never change. Generate once,
commit to repo, and reference from sitemap index. Zero runtime cost,
maximum SEO discoverability.

Why static?
-----------
- Verse URLs are completely static (Genesis 1:1 will always be at the same URL)
- Regenerating 31k URLs on every sitemap request wastes CPU time
- Static file can be cached indefinitely by CDN and browsers
- Google prioritizes URLs in sitemaps for crawling
- This approach gives us both speed AND discoverability

When to regenerate:
-------------------
- Never, unless the URL structure for verses changes
- The Bible text hasn't changed in 2000+ years, URLs won't either

Usage:
------
    uv run python scripts/generate_verse_sitemap.py > kjvstudy_org/static/sitemap-verses.xml
    git add kjvstudy_org/static/sitemap-verses.xml
    git commit -m "Update verse sitemap"
"""
import sys
from pathlib import Path

# Add parent directory to path to import kjv module
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import bible


def generate_verse_sitemap():
    """Generate sitemap XML for all verses in the Bible."""
    base_url = "https://kjvstudy.org"

    # Static date - these URLs never change
    lastmod = "2024-01-01"

    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    # Get all books
    books = bible.get_books()
    verse_count = 0

    for book in books:
        # Get all chapters for this book
        chapters = bible.get_chapters_for_book(book)

        for chapter in chapters:
            # Get all verses in this chapter
            verses = bible.get_verses_by_book_chapter(book, chapter)

            for verse_num in range(1, len(verses) + 1):
                sitemap_xml += f"""    <url>
        <loc>{base_url}/book/{book}/chapter/{chapter}/verse/{verse_num}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>never</changefreq>
        <priority>0.4</priority>
    </url>
"""
                verse_count += 1

    sitemap_xml += "</urlset>\n"

    # Print stats to stderr so stdout is clean XML
    print(f"Generated sitemap with {verse_count} verses", file=sys.stderr)
    print(f"Size: {len(sitemap_xml):,} bytes", file=sys.stderr)

    return sitemap_xml


if __name__ == "__main__":
    print(generate_verse_sitemap())
