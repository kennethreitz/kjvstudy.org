"""Topics routes - browse and view topical Bible studies."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from ..kjv import bible
from ..topics import get_all_topics, get_topic_with_text
from ..utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf_async

router = APIRouter()
templates = None


def init_templates(t: Jinja2Templates):
    """Initialize templates for topics routes."""
    global templates
    templates = t


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
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    topic = get_topic_with_text(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    html_content = templates.get_template("topic_pdf.html").render(
        topic=topic,
        topic_name=topic_name,
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{topic_name}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
