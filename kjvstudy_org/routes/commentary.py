"""Commentary routes (FastAPI layer).

Thin FastAPI wrapper around the framework-agnostic commentary generation
logic in :mod:`kjvstudy_org.commentary_gen`. Only the route handlers live
here; every generation/helper function and data dict lives in commentary_gen
so it can be imported without pulling in FastAPI.
"""
import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ._templates import templates
from ..commentary_gen import (
    # Needed by the route handlers below
    _compute_commentary_index,
    # Re-exported for server.py (and any other importer) so the existing
    # ``from .routes.commentary import ...`` keeps working unchanged.
    generate_commentary,
    generate_chapter_overview,
    generate_book_commentary,
    generate_word_study_sidenotes,
)

router = APIRouter(tags=["Commentary"])


@router.get("/about/commentary", response_class=HTMLResponse)
async def commentary_index(request: Request):
    """Commentary index - list all verses with commentary"""
    # Run heavy I/O in thread pool
    commentary_idx, total_books, total_verses = await asyncio.to_thread(_compute_commentary_index)

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Commentary Index", "url": None}
    ]

    # Get books list for navigation
    from ..kjv import bible
    books = bible.get_books()

    return templates.TemplateResponse(
        "commentary_index.html",
        {
            "request": request,
            "books": books,
            "commentary_index": commentary_idx,
            "total_books": total_books,
            "total_verses": total_verses,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/commentary/{book}/{chapter}")
async def commentary_redirect(book: str, chapter: int):
    """Redirect old chapter commentary URLs to chapter page"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}", status_code=301)
