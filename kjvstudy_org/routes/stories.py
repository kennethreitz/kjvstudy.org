"""Bible Stories routes for KJV Study. (Responder port of routes/stories.py)

Routes for browsing Bible stories with adult and kids versions.
"""
from ..kjv import bible
from ..stories import (
    get_categories,
    get_story_by_slug,
    get_story_count,
    get_category_count,
    get_adjacent_stories,
)
from ..utils.helpers import get_books
from ._helpers import render, abort_404, pdf_resp


def register(api):
    @api.route("/stories")
    async def stories_index(req, resp):
        """Bible stories index page - shows all categories and stories."""
        books = get_books()
        categories = get_categories()
        story_count = get_story_count()
        category_count = get_category_count()

        render(
            req, resp, "stories_index.html",
            books=books,
            categories=categories,
            story_count=story_count,
            category_count=category_count,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": None}
            ],
        )

    @api.route("/stories/kids")
    async def stories_kids_index(req, resp):
        """Bible stories index page for kids - shows all categories and kid-friendly stories."""
        books = get_books()
        categories = get_categories()
        story_count = get_story_count()
        category_count = get_category_count()

        render(
            req, resp, "stories_kids_index.html",
            books=books,
            categories=categories,
            story_count=story_count,
            category_count=category_count,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": "Kids", "url": None}
            ],
        )

    @api.route("/stories/{slug}/pdf")
    async def story_pdf(req, resp, *, slug):
        """Generate PDF for a story (adult version)."""
        story = get_story_by_slug(slug)

        if not story:
            abort_404(req, resp, "Story not found")
            return

        # Render the PDF template
        html_content = req.api.template("story_pdf.html", story=story)

        # Return as downloadable PDF
        filename = f"{slug}.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/stories/{slug}/kids/pdf")
    async def story_kids_pdf(req, resp, *, slug):
        """Generate PDF for a story (kids version)."""
        story = get_story_by_slug(slug)

        if not story:
            abort_404(req, resp, "Story not found")
            return

        if not story.get("kids_narrative"):
            abort_404(req, resp, "Kids version not available for this story")
            return

        # Render the PDF template
        html_content = req.api.template("story_kids_pdf.html", story=story)

        # Return as downloadable PDF
        filename = f"{slug}-kids.pdf"
        await pdf_resp(resp, html_content, filename)
        return

    @api.route("/stories/{slug}")
    async def story_detail(req, resp, *, slug):
        """Individual story page (adult version)."""
        books = get_books()
        story = get_story_by_slug(slug)

        if not story:
            abort_404(req, resp, "Story not found")
            return

        # Find previous and next stories for navigation
        prev_story, next_story = get_adjacent_stories(slug)

        render(
            req, resp, "story_detail.html",
            books=books,
            story=story,
            prev_story=prev_story,
            next_story=next_story,
            is_kids=False,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": story.get("title", "Story"), "url": None}
            ],
        )

    @api.route("/stories/{slug}/kids")
    async def story_kids(req, resp, *, slug):
        """Individual story page (kids version)."""
        books = get_books()
        story = get_story_by_slug(slug)

        if not story:
            abort_404(req, resp, "Story not found")
            return

        # Check if kids version exists
        if not story.get("kids_narrative"):
            abort_404(req, resp, "Kids version not available for this story")
            return

        # Find previous and next stories for navigation
        prev_story, next_story = get_adjacent_stories(slug)

        render(
            req, resp, "story_kids.html",
            books=books,
            story=story,
            prev_story=prev_story,
            next_story=next_story,
            is_kids=True,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": story.get("kids_title", story.get("title", "Story")), "url": None}
            ],
        )
