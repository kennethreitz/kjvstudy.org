"""Biblical timeline routes. (Responder port of routes/timeline.py)"""
import json
from pathlib import Path

from ..kjv import bible
from ..utils.pdf import WEASYPRINT_AVAILABLE
from ._helpers import render, pdf_resp


# =============================================================================
# Helper Functions
# =============================================================================

# Cache timeline data at module level
_TIMELINE_CACHE: dict | None = None


def _load_timeline_data() -> dict:
    """Load timeline data from JSON file (internal, uncached)."""
    data_dir = Path(__file__).parent.parent / "data"
    timeline_path = data_dir / "biblical_timeline.json"

    with open(timeline_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_biblical_timeline_context():
    """
    Load comprehensive biblical timeline data from JSON file (cached).

    Returns tuple of (timeline_events, introduction, chronology_note, chronology_comparison, conclusion)
    """
    global _TIMELINE_CACHE
    if _TIMELINE_CACHE is None:
        _TIMELINE_CACHE = _load_timeline_data()

    timeline_events = _TIMELINE_CACHE.get("timeline_events", {})
    introduction = _TIMELINE_CACHE.get("introduction", "")
    chronology_note = _TIMELINE_CACHE.get("chronology_note", "")
    chronology_comparison = _TIMELINE_CACHE.get("chronology_comparison", [])
    conclusion = _TIMELINE_CACHE.get("conclusion", "")

    return timeline_events, introduction, chronology_note, chronology_comparison, conclusion


# =============================================================================
# Routes
# =============================================================================

def register(api):
    @api.route("/biblical-timeline")
    async def biblical_timeline_page(req, resp):
        """Biblical timeline page showing major biblical events chronologically"""
        books = bible.get_books()

        timeline_events, introduction, chronology_note, chronology_comparison, conclusion = get_biblical_timeline_context()

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Resources", "url": "/resources"},
            {"text": "Biblical Timeline", "url": None}
        ]

        render(
            req, resp,
            "biblical_timeline.html",
            books=books,
            timeline_events=timeline_events,
            introduction=introduction,
            chronology_note=chronology_note,
            chronology_comparison=chronology_comparison,
            conclusion=conclusion,
            breadcrumbs=breadcrumbs,
            pdf_available=WEASYPRINT_AVAILABLE,
        )

    @api.route("/biblical-timeline/pdf")
    async def biblical_timeline_pdf(req, resp):
        """Generate PDF export for the biblical timeline."""
        timeline_events, introduction, chronology_note, chronology_comparison, conclusion = get_biblical_timeline_context()

        html_content = api.template(
            "biblical_timeline_pdf.html",
            timeline_events=timeline_events,
            introduction=introduction,
            chronology_note=chronology_note,
            chronology_comparison=chronology_comparison,
            conclusion=conclusion,
        )
        await pdf_resp(resp, html_content, "biblical-timeline.pdf")
        return
