"""Commentary routes. (Responder port of routes/commentary.py)

Thin wrapper around the framework-agnostic commentary generation logic in
:mod:`kjvstudy_org.commentary_gen`. Only the route handlers live here; every
generation/helper function and data dict lives in commentary_gen so it can be
imported without pulling in a web framework.
"""
import asyncio

from ..commentary_gen import (
    # Needed by the route handlers below
    _compute_commentary_index,
    # Re-exported so the existing ``from ...commentary import ...`` imports
    # (e.g. in server.py) keep working unchanged.
    generate_commentary,
    generate_chapter_overview,
    generate_book_commentary,
    generate_word_study_sidenotes,
)
from ._helpers import render, redirect, abort_404


def register(api):
    @api.route("/about/commentary")
    async def commentary_index(req, resp):
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

        render(
            req, resp, "commentary_index.html",
            books=books,
            commentary_index=commentary_idx,
            total_books=total_books,
            total_verses=total_verses,
            breadcrumbs=breadcrumbs,
        )

    @api.route("/commentary/{book}/{chapter:int}")
    async def commentary_redirect(req, resp, *, book, chapter):
        """Redirect old chapter commentary URLs to chapter page"""
        redirect(resp, f"/book/{book}/chapter/{chapter}", 301)
        return
