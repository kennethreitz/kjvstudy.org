"""About routes - stats, cross-references index, and about page."""
import asyncio
import json
from collections import defaultdict
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..kjv import bible
from ..utils.books import OT_BOOKS, NT_BOOKS
from ..utils.stats import compute_site_stats
from ._templates import templates

router = APIRouter()


# =============================================================================
# Helper Functions (run in thread pool)
# =============================================================================

def _compute_crossref_index() -> tuple:
    """Compute cross-reference index - runs in thread pool."""
    data_dir = Path(__file__).parent.parent / "data" / "cross_references"

    # Build index of all verses with cross-references, grouped by book
    crossref_index = defaultdict(lambda: defaultdict(list))

    for file in sorted(data_dir.glob('*.json')):
        with open(file, 'r') as f:
            data = json.load(f)

            for verse_key, refs in data.items():
                # Parse verse key: "Book:Chapter:Verse"
                parts = verse_key.split(':')
                if len(parts) == 3:
                    book, chapter, verse = parts
                    crossref_index[book][int(chapter)].append({
                        'verse': int(verse),
                        'ref_count': len(refs)
                    })

    # Sort books in biblical order (OT then NT)
    biblical_order = OT_BOOKS + NT_BOOKS
    book_order = {book: i for i, book in enumerate(biblical_order)}

    # Convert to regular dict and sort
    crossref_index = {
        book: {
            chapter: sorted(verses, key=lambda x: x['verse'])
            for chapter, verses in sorted(chapters.items())
        }
        for book, chapters in sorted(crossref_index.items(), key=lambda x: book_order.get(x[0], 999))
    }

    # Calculate statistics
    total_books = len(crossref_index)
    total_verses = sum(
        len(verses)
        for chapters in crossref_index.values()
        for verses in chapters.values()
    )
    total_refs = sum(
        sum(v['ref_count'] for v in verses)
        for chapters in crossref_index.values()
        for verses in chapters.values()
    )

    return crossref_index, total_books, total_verses, total_refs


# =============================================================================
# Routes
# =============================================================================

@router.get("/about/stats", response_class=HTMLResponse)
async def stats(request: Request):
    """Hidden statistics page - comprehensive site metrics"""
    # Run heavy computation in thread pool (cached after the first call)
    stats_data = await asyncio.to_thread(compute_site_stats, True)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Statistics", "url": None}
    ]

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "books": books,
            "stats": stats_data,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about/cross-references", response_class=HTMLResponse)
async def cross_references_index(request: Request):
    """Cross-references index - list all verses with cross-references"""
    # Run heavy I/O in thread pool
    crossref_index, total_books, total_verses, total_refs = await asyncio.to_thread(_compute_crossref_index)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Cross-References Index", "url": None}
    ]

    return templates.TemplateResponse(
        "cross_references_index.html",
        {
            "request": request,
            "books": books,
            "crossref_index": crossref_index,
            "total_books": total_books,
            "total_verses": total_verses,
            "total_refs": total_refs,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page - site information, creator, data sources, theological approach"""
    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": None}
    ]
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "books": books,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about/claude", response_class=HTMLResponse)
async def claude_page(request: Request):
    """A note from Claude - reflections from the AI assistant behind KJV Study"""
    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "A Note from Claude", "url": None}
    ]
    return templates.TemplateResponse(
        request,
        "about_claude.html",
        {
            "books": books,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about/accessibility", response_class=HTMLResponse)
async def accessibility(request: Request):
    """Accessibility page - keyboard navigation, screen readers, text-to-speech"""
    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Accessibility", "url": None}
    ]
    return templates.TemplateResponse(
        "accessibility.html",
        {
            "request": request,
            "books": books,
            "breadcrumbs": breadcrumbs,
        }
    )
