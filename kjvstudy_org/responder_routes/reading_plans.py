"""Reading plans routes - browse and view Bible reading plans. (Responder port of routes/reading_plans.py)"""
import re

from ..kjv import bible
from ..reading_plans import get_plan, get_plan_summary
from ..utils.books import normalize_book_name, OT_BOOKS, NT_BOOKS
from ..utils.pdf import pdf_context, require_pdf_available
from ._helpers import render, abort_404, pdf_resp


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

def register(api):
    @api.route("/reading-plans")
    async def reading_plans_page(req, resp):
        """Browse Bible reading plans"""
        books = bible.get_books()
        plans = get_plan_summary()

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Reading Plans", "url": None}
        ]

        render(
            req, resp, "reading_plans.html",
            plans=plans,
            books=books,
            breadcrumbs=breadcrumbs,
        )

    @api.route("/reading-plans/{plan_id}")
    async def reading_plan_detail(req, resp, *, plan_id):
        """View a specific reading plan"""
        books = bible.get_books()
        plan = get_plan(plan_id)

        if not plan:
            abort_404(req, resp, "Reading plan not found")
            return

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

        render(
            req, resp, "reading_plan_detail.html",
            plan=plan,
            plan_id=plan_id,
            books=books,
            breadcrumbs=breadcrumbs,
            **pdf_context(f"/reading-plans/{plan_id}/pdf"),
            days_data=days_data,
            total_days=plan.get('duration_days', len(days_data)),
        )

    @api.route("/reading-plans/{plan_id}/pdf")
    async def reading_plan_pdf(req, resp, *, plan_id):
        """Generate a PDF export for a reading plan."""
        require_pdf_available()

        plan = get_plan(plan_id)
        if not plan:
            abort_404(req, resp, "Reading plan not found")
            return

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

        html_content = api.template(
            "reading_plan_pdf.html",
            plan=plan,
            include_text=include_text,
            days_with_text=days_with_text,
        )
        await pdf_resp(resp, html_content, f"reading-plan-{plan_id}.pdf")
        return
