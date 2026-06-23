"""Reading plans routes - browse and view Bible reading plans."""
import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse

from ..kjv import bible
from ..reading_plans import get_plan, get_plan_summary
from ..utils.books import normalize_book_name, OT_BOOKS, NT_BOOKS
from ..utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf_async
from ._templates import templates

router = APIRouter()


# =============================================================================
# Helper Functions
# =============================================================================

def parse_reading_reference(ref: str) -> list:
    """Parse a reading reference like 'Genesis 1-3' or 'Matthew 1' into chapter list.

    Returns list of tuples: [(book, chapter), ...]
    """
    # Handle patterns like "Genesis 1-3", "Matthew 1", "1 John 2-3"
    # Pattern: optional number prefix + book name + chapter range
    pattern = r'^((?:\d\s+)?[A-Za-z]+(?:\s+[A-Za-z]+)?)\s+(\d+)(?:-(\d+))?$'
    match = re.match(pattern, ref.strip())
    if not match:
        return []

    book = match.group(1)
    start_ch = int(match.group(2))
    end_ch = int(match.group(3)) if match.group(3) else start_ch

    # Normalize book name - if it's already canonical, use it as-is
    normalized = normalize_book_name(book)
    if not normalized:
        # Check if it's already a valid canonical name
        all_books = OT_BOOKS + NT_BOOKS
        if book in all_books:
            normalized = book
        else:
            return []

    return [(normalized, ch) for ch in range(start_ch, end_ch + 1)]


def get_reading_text(readings: list) -> list:
    """Get the Bible text for a list of reading references.

    Returns list of dicts with book, chapter, and verses.
    """
    result = []
    for ref in readings:
        chapters = parse_reading_reference(ref)
        for book, chapter in chapters:
            verses = bible.get_verses_by_book_chapter(book, chapter)
            if verses:
                result.append({
                    'book': book,
                    'chapter': chapter,
                    'verses': verses,
                    'reference': f"{book} {chapter}"
                })
    return result


# =============================================================================
# Routes
# =============================================================================

@router.get("/reading-plans", response_class=HTMLResponse)
async def reading_plans_page(request: Request):
    """Browse Bible reading plans"""
    books = bible.get_books()
    plans = get_plan_summary()

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "reading_plans.html",
        {
            "plans": plans,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/reading-plans/{plan_id}", response_class=HTMLResponse)
async def reading_plan_detail(request: Request, plan_id: str):
    """View a specific reading plan"""
    books = bible.get_books()
    plan = get_plan(plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    # Pass day info without text - text will be lazy loaded via API
    all_days = plan.get('days') or plan.get('sample_days', [])
    days_data = []
    for day in all_days:
        day_data = {
            'day': day['day'],
            'theme': day.get('theme', ''),
            'readings': day['readings']
        }
        days_data.append(day_data)

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Reading Plans", "url": "/reading-plans"},
        {"text": plan["name"], "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "reading_plan_detail.html",
        {
            "plan": plan,
            "plan_id": plan_id,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/reading-plans/{plan_id}/pdf" if WEASYPRINT_AVAILABLE else None,
            "days_data": days_data,
            "total_days": plan.get('duration_days', len(days_data))
        }
    )


@router.get("/reading-plans/{plan_id}/pdf")
async def reading_plan_pdf(plan_id: str):
    """Generate a PDF export for a reading plan."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    # Include full Bible text for all plans (including 365-day plans)
    include_text = True

    days_with_text = None
    if include_text:
        all_days = plan.get('days') or plan.get('sample_days', [])
        days_with_text = []
        for day in all_days:
            day_data = {
                'day': day['day'],
                'theme': day.get('theme', ''),
                'readings': day['readings'],
                'text': get_reading_text(day['readings'])
            }
            days_with_text.append(day_data)

    html_content = templates.get_template("reading_plan_pdf.html").render(
        plan=plan,
        include_text=include_text,
        days_with_text=days_with_text
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    if pdf_buffer is None:
        raise HTTPException(status_code=503, detail="PDF generation failed")

    filename = f"reading-plan-{plan_id}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
