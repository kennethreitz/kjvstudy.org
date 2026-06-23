"""Bible Stories routes for KJV Study.

Routes for browsing Bible stories with adult and kids versions.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from ..kjv import bible
from ..stories import (
    get_categories,
    get_story_by_slug,
    get_story_count,
    get_category_count,
)
from ..utils.pdf import pdf_response, require_pdf_available

router = APIRouter(tags=["Bible Stories"])

from ._templates import templates


def get_books():
    """Get list of Bible books."""
    return bible.get_books()


@router.get("/stories", response_class=HTMLResponse)
async def stories_index(request: Request):
    """Bible stories index page - shows all categories and stories."""
    books = get_books()
    categories = get_categories()
    story_count = get_story_count()
    category_count = get_category_count()

    return templates.TemplateResponse(
        request,
        "stories_index.html",
        {
            "books": books,
            "categories": categories,
            "story_count": story_count,
            "category_count": category_count,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": None}
            ]
        }
    )


@router.get("/stories/kids", response_class=HTMLResponse)
async def stories_kids_index(request: Request):
    """Bible stories index page for kids - shows all categories and kid-friendly stories."""
    books = get_books()
    categories = get_categories()
    story_count = get_story_count()
    category_count = get_category_count()

    return templates.TemplateResponse(
        request,
        "stories_kids_index.html",
        {
            "books": books,
            "categories": categories,
            "story_count": story_count,
            "category_count": category_count,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": "Kids", "url": None}
            ]
        }
    )


@router.get("/stories/{slug}/pdf")
async def story_pdf(request: Request, slug: str):
    """Generate PDF for a story (adult version)."""
    require_pdf_available()

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Render the PDF template
    html_content = templates.get_template("story_pdf.html").render(story=story)

    # Return as downloadable PDF
    filename = f"{slug}.pdf"
    return await pdf_response(html_content, filename)


@router.get("/stories/{slug}/kids/pdf")
async def story_kids_pdf(request: Request, slug: str):
    """Generate PDF for a story (kids version)."""
    require_pdf_available()

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not story.get("kids_narrative"):
        raise HTTPException(status_code=404, detail="Kids version not available for this story")

    # Render the PDF template
    html_content = templates.get_template("story_kids_pdf.html").render(story=story)

    # Return as downloadable PDF
    filename = f"{slug}-kids.pdf"
    return await pdf_response(html_content, filename)


@router.get("/stories/{slug}", response_class=HTMLResponse)
async def story_detail(request: Request, slug: str):
    """Individual story page (adult version)."""
    books = get_books()
    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Find previous and next stories for navigation
    from ..stories import get_all_stories_flat
    all_stories = get_all_stories_flat()
    current_index = None

    for i, s in enumerate(all_stories):
        if s.get("slug") == slug:
            current_index = i
            break

    prev_story = all_stories[current_index - 1] if current_index and current_index > 0 else None
    next_story = all_stories[current_index + 1] if current_index is not None and current_index < len(all_stories) - 1 else None

    return templates.TemplateResponse(
        request,
        "story_detail.html",
        {
            "books": books,
            "story": story,
            "prev_story": prev_story,
            "next_story": next_story,
            "is_kids": False,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": story.get("title", "Story"), "url": None}
            ]
        }
    )


@router.get("/stories/{slug}/kids", response_class=HTMLResponse)
async def story_kids(request: Request, slug: str):
    """Individual story page (kids version)."""
    books = get_books()
    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Check if kids version exists
    if not story.get("kids_narrative"):
        raise HTTPException(status_code=404, detail="Kids version not available for this story")

    # Find previous and next stories for navigation
    from ..stories import get_all_stories_flat
    all_stories = get_all_stories_flat()
    current_index = None

    for i, s in enumerate(all_stories):
        if s.get("slug") == slug:
            current_index = i
            break

    prev_story = all_stories[current_index - 1] if current_index and current_index > 0 else None
    next_story = all_stories[current_index + 1] if current_index is not None and current_index < len(all_stories) - 1 else None

    return templates.TemplateResponse(
        request,
        "story_kids.html",
        {
            "books": books,
            "story": story,
            "prev_story": prev_story,
            "next_story": next_story,
            "is_kids": True,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Bible Stories", "url": "/stories"},
                {"text": story.get("kids_title", story.get("title", "Story")), "url": None}
            ]
        }
    )
