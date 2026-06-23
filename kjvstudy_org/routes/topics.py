"""Topics routes - browse and view topical Bible studies."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from ..kjv import bible
from ..topics import get_all_topics, get_topic_with_text
from ..utils.pdf import WEASYPRINT_AVAILABLE, pdf_response, require_pdf_available
from ._templates import templates

router = APIRouter()


# =============================================================================
# Routes
# =============================================================================

@router.get("/topics", response_class=HTMLResponse)
async def topics_page(request: Request):
    """Browse topical index of Bible themes"""
    books = bible.get_books()
    topics = get_all_topics()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "topics.html",
        {
            "topics": topics,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE
        }
    )


@router.get("/topics/{topic_name}", response_class=HTMLResponse)
async def topic_detail(request: Request, topic_name: str):
    """View verses for a specific topic"""
    books = bible.get_books()
    topic = get_topic_with_text(topic_name)

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Topics", "url": "/topics"},
        {"text": topic_name, "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "topic_detail.html",
        {
            "topic": topic,
            "topic_name": topic_name,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/topics/{topic_name}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


@router.get("/topics/{topic_name}/pdf")
async def topic_detail_pdf(topic_name: str):
    """Generate a PDF export for a topic detail page."""
    require_pdf_available()

    topic = get_topic_with_text(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    html_content = templates.get_template("topic_pdf.html").render(
        topic=topic,
        topic_name=topic_name,
    )
    filename = f"{topic_name}.pdf"
    return await pdf_response(html_content, filename)
