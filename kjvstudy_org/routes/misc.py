"""Miscellaneous routes - search, interlinear, random verse, verse of the day, red letter, OG images.

Responder port of routes/misc.py.
"""
import asyncio
import hashlib
import random
import re
from datetime import datetime, timedelta
from pathlib import Path as PathLib
from typing import Optional
from urllib.parse import unquote

from ..kjv import bible
from ..red_letter import iter_red_letter_verses, red_letter_stats
from ..utils.search import perform_full_text_search
from ..utils.helpers import get_daily_verse
from ..utils.family_tree import search_family_tree
from ..og_image import get_cached_or_generate
from ..stories import get_story_by_slug
from ..strongs import normalize_strongs
from ._helpers import render, redirect, pdf_resp


# =============================================================================
# Routes
# =============================================================================

def parse_strongs_number(query: str) -> str | None:
    """Parse a Strong's number query and return the redirect URL, or None.

    Normalizes leading zeros (H0001 -> /strongs/H1) so the redirect target
    matches the canonical Strong's URL.
    """
    normalized = normalize_strongs(query)
    return f'/strongs/{normalized}' if normalized else None


# =============================================================================
# Dynamic OG Image Generation
# =============================================================================

async def _og_png(resp, cache_key, title, subtitle, page_type, verse_text=None):
    """Render (or serve from cache) an OG PNG response with long-lived caching.

    CPU-bound image generation runs in a thread pool so it never blocks the
    event loop. Shared by every /og/*.png handler.
    """
    image_bytes = await asyncio.to_thread(
        get_cached_or_generate,
        cache_key=cache_key,
        title=title,
        subtitle=subtitle,
        verse_text=verse_text,
        page_type=page_type,
    )
    resp.content = image_bytes
    resp.mimetype = "image/png"
    resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"


def register(api):
    @api.route("/search")
    async def search_page(req, resp):
        """Search page with results (includes Bible verses and family tree)"""
        q = req.params.get("q")

        # Check if query is a Strong's number - redirect if so
        if q:
            strongs_url = parse_strongs_number(q)
            if strongs_url:
                redirect(resp, strongs_url, 302)
                return

        books = bible.get_books()
        search_results = []
        family_tree_results = []
        is_direct_verse = False

        if q and len(q.strip()) >= 2:
            # Search Bible verses (cap at 50 to keep template rendering fast)
            search_results = perform_full_text_search(q.strip(), limit=50)
            # Check if this was a direct verse reference match
            if search_results and len(search_results) == 1 and search_results[0].get("score") == 100.0:
                is_direct_verse = True

            # Also search family tree (limit to 5 results)
            family_tree_results = search_family_tree(q.strip(), limit=5)

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Search", "url": None}
        ]

        render(
            req, resp, "search.html",
            query=q or "",
            results=search_results,
            family_tree_results=family_tree_results,
            books=books,
            total_results=len(search_results) + len(family_tree_results),
            is_direct_verse=is_direct_verse,
            breadcrumbs=breadcrumbs,
        )

    @api.route("/interlinear")
    async def interlinear_landing_page(req, resp):
        """Landing page explaining interlinear Bible study"""
        books = bible.get_books()

        # Featured verses with interlinear data
        featured_verses = [
            {"reference": "John 3:16", "url": "/book/John/chapter/3/verse/16#interlinear", "note": "God's love for the world"},
            {"reference": "Genesis 1:1", "url": "/book/Genesis/chapter/1/verse/1#interlinear", "note": "In the beginning"},
            {"reference": "Psalm 23:1", "url": "/book/Psalms/chapter/23/verse/1#interlinear", "note": "The Lord is my shepherd"},
            {"reference": "Romans 8:28", "url": "/book/Romans/chapter/8/verse/28#interlinear", "note": "All things work together for good"},
            {"reference": "Matthew 28:19", "url": "/book/Matthew/chapter/28/verse/19#interlinear", "note": "The Great Commission"},
            {"reference": "1 Corinthians 13:4", "url": "/book/1 Corinthians/chapter/13/verse/4#interlinear", "note": "Love is patient"},
        ]

        # Build breadcrumbs
        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Interlinear", "url": None}
        ]

        render(
            req, resp, "interlinear_landing.html",
            books=books,
            featured_verses=featured_verses,
            breadcrumbs=breadcrumbs,
        )

    @api.route("/random-verse")
    async def random_verse(req, resp):
        """Redirect to a random Bible verse"""
        # Get all books
        all_books = bible.get_books()

        # Pick a random book
        book = random.choice(all_books)

        # Get all chapters for this book
        chapters = bible.get_chapters_for_book(book)

        # Pick a random chapter
        chapter = random.choice(chapters)

        # Get all verses for this chapter
        verses = bible.get_verses_by_book_chapter(book, chapter)

        # Pick a random verse
        verse = random.choice(verses)

        # Redirect to the verse page with cache control headers to ensure fresh random verse each time
        redirect(resp, f"/book/{book}/chapter/{chapter}/verse/{verse.verse}", 302)
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"

    @api.route("/verse-of-the-day")
    async def verse_of_the_day_redirect(req, resp):
        """Redirect to today's verse of the day (prevents caching, allows bookmarking)."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        redirect(resp, f"/verse-of-the-day/{today_str}", 302)

    @api.route("/verse-of-the-day/{date}")
    async def verse_of_the_day_page(req, resp, *, date):
        """Verse of the day page for a specific date."""
        books = bible.get_books()

        # Parse the date
        try:
            current_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            # Invalid date format, redirect to today
            redirect(resp, "/verse-of-the-day", 302)
            return

        date_str = current_date.strftime("%Y-%m-%d")
        daily_verse = get_daily_verse(date_str)

        # Calculate prev/next dates for navigation
        prev_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
        next_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        today_str = datetime.now().strftime("%Y-%m-%d")

        # Generate past 30 days of verses (from the viewed date)
        past_verses = []
        for i in range(1, 31):  # Past 30 days (not including current)
            past_date = current_date - timedelta(days=i)
            past_date_str = past_date.strftime("%Y-%m-%d")
            verse = get_daily_verse(past_date_str)
            past_verses.append(verse)

        # Build breadcrumbs
        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Verse of the Day", "url": "/verse-of-the-day"}
        ]

        render(
            req, resp, "verse_of_the_day.html",
            books=books,
            daily_verse=daily_verse,
            past_verses=past_verses,
            breadcrumbs=breadcrumbs,
            prev_date=prev_date,
            next_date=next_date,
            is_today=date_str == today_str,
        )

    @api.route("/stars")
    async def stars_page(req, resp):
        """Stars page - displays user's saved starred pages from localStorage"""
        books = bible.get_books()

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Stars", "url": None}
        ]

        render(
            req, resp, "stars.html",
            books=books,
            breadcrumbs=breadcrumbs,
        )

    @api.route("/stars/pdf", methods=["POST"])
    async def stars_pdf(req, resp):
        """Render the user's starred pages (POSTed from localStorage) as a PDF anthology."""
        try:
            data = await req.media()
        except Exception:
            data = None
        raw = data.get("stars") if isinstance(data, dict) else None
        if not isinstance(raw, list):
            resp.status_code = 400
            resp.media = {"detail": "Expected a JSON body of the form {\"stars\": [...]}"}
            return

        # Sanitize + bound the client-supplied data before rendering.
        stars = []
        for item in raw[:500]:
            if not isinstance(item, dict):
                continue
            clean_crumbs = []
            crumbs = item.get("breadcrumbs")
            if isinstance(crumbs, list):
                for c in crumbs:
                    if isinstance(c, dict) and c.get("text"):
                        clean_crumbs.append({"text": str(c["text"])[:80]})
            stars.append({
                "title": str(item.get("title") or "")[:200],
                "url": str(item.get("url") or "")[:300],
                "description": str(item.get("description") or "")[:500],
                "excerpt": str(item.get("excerpt") or "")[:600],
                "note": str(item.get("note") or "")[:2000],
                "breadcrumbs": clean_crumbs,
            })

        if not stars:
            resp.status_code = 400
            resp.media = {"detail": "No stars to render"}
            return

        html = req.api.template(
            "stars_pdf.html",
            stars=stars,
            generated=datetime.now().strftime("%B %-d, %Y"),
        )
        await pdf_resp(resp, html, "my-starred-pages.pdf")

    @api.route("/red-letter")
    async def red_letter_page(req, resp):
        """Red Letter Edition - Words of Christ page"""
        book = req.params.get("book")
        page = int(req.params.get("page", 1))

        books = bible.get_books()

        # Filtered, parsed verses for the table (book filter accepts abbreviations)
        all_verses = list(iter_red_letter_verses(book))

        # Sort by book order, then chapter, then verse
        book_order = {b: i for i, b in enumerate(books)}
        all_verses.sort(key=lambda v: (book_order.get(v["book"], 999), v["chapter"], v["verse"]))

        # Pagination
        per_page = 50
        total = len(all_verses)
        total_pages = (total + per_page - 1) // per_page
        page = min(page, total_pages) if total_pages > 0 else 1
        offset = (page - 1) * per_page
        verses = all_verses[offset:offset + per_page]

        # Stats and sidebar counts (unfiltered, by_book already sorted by count)
        stats = red_letter_stats()
        total_all = stats["total"]
        full_verses = stats["full"]
        partial_verses = stats["partial"]
        books_with_counts = list(stats["by_book"].items())

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Red Letter", "url": "/red-letter"}
        ]
        if book:
            breadcrumbs.append({"text": book, "url": None})

        render(
            req, resp, "red_letter.html",
            books=books,
            verses=verses,
            total=total,
            total_all=total_all,
            full_verses=full_verses,
            partial_verses=partial_verses,
            books_with_counts=books_with_counts,
            selected_book=book,
            page=page,
            total_pages=total_pages,
            per_page=per_page,
            breadcrumbs=breadcrumbs,
        )

    # =========================================================================
    # Dynamic OG Image Generation
    # =========================================================================

    @api.route("/og/verse/{book}/{chapter:int}/{verse:int}.png")
    async def og_image_verse(req, resp, *, book, chapter, verse):
        """Generate OG image for a specific verse."""
        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            # Return default image if verse not found
            default_path = PathLib(__file__).parent.parent / "static" / "og-image.png"
            content = await asyncio.to_thread(default_path.read_bytes)
            resp.content = content
            resp.mimetype = "image/png"
            return

        await _og_png(
            resp,
            cache_key=f"verse:{book}:{chapter}:{verse}",
            title=f"{book} {chapter}:{verse}",
            subtitle="King James Version",
            verse_text=verse_text,
            page_type="verse",
        )

    @api.route("/og/chapter/{book}/{chapter:int}.png")
    async def og_image_chapter(req, resp, *, book, chapter):
        """Generate OG image for a chapter."""
        # Get first verse as preview
        verse_text = bible.get_verse_text(book, chapter, 1)

        await _og_png(
            resp,
            cache_key=f"chapter:{book}:{chapter}",
            title=f"{book} {chapter}",
            subtitle="King James Version",
            verse_text=verse_text[:150] + "..." if verse_text and len(verse_text) > 150 else verse_text,
            page_type="chapter",
        )

    @api.route("/og/book/{book}.png")
    async def og_image_book(req, resp, *, book):
        """Generate OG image for a book."""
        await _og_png(
            resp,
            cache_key=f"book:{book}",
            title=book,
            subtitle="King James Version Bible",
            page_type="book",
        )

    @api.route("/og/topic/{topic}.png")
    async def og_image_topic(req, resp, *, topic):
        """Generate OG image for a topic."""
        topic_name = unquote(topic)

        await _og_png(
            resp,
            cache_key=f"topic:{topic_name}",
            title=topic_name,
            subtitle="Topical Bible Study",
            page_type="topic",
        )

    @api.route("/og/story/{slug}.png")
    async def og_image_story(req, resp, *, slug):
        """Generate OG image for a Bible story."""
        # Look up the story title, falling back to a humanized slug
        title = slug.replace("-", " ").title()
        story = get_story_by_slug(slug)
        if story:
            title = story.get("title", title)

        await _og_png(
            resp,
            cache_key=f"story:{slug}",
            title=title,
            subtitle="Bible Stories",
            page_type="story",
        )

    @api.route("/og/guide/{slug}.png")
    async def og_image_guide(req, resp, *, slug):
        """Generate OG image for a study guide."""
        await _og_png(
            resp,
            cache_key=f"guide:{slug}",
            title=slug.replace("-", " ").title(),  # Fallback title
            subtitle="Bible Study Guide",
            page_type="guide",
        )
