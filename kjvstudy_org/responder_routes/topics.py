"""Topics routes - browse and view topical Bible studies. (Responder port of routes/topics.py)"""
from ..kjv import bible
from ..topics import get_all_topics, get_topic_with_text
from ..utils.pdf import WEASYPRINT_AVAILABLE, pdf_context
from ._helpers import render, abort_404, pdf_resp


def register(api):
    @api.route("/topics")
    async def topics_page(req, resp):
        """Browse topical index of Bible themes"""
        books = bible.get_books()
        topics = get_all_topics()

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Topics", "url": None}
        ]

        render(
            req, resp, "topics.html",
            topics=topics,
            books=books,
            breadcrumbs=breadcrumbs,
            pdf_available=WEASYPRINT_AVAILABLE,
        )

    @api.route("/topics/{topic_name}")
    async def topic_detail(req, resp, *, topic_name):
        """View verses for a specific topic"""
        books = bible.get_books()
        topic = get_topic_with_text(topic_name)

        if not topic:
            abort_404(req, resp, "Topic not found")
            return

        breadcrumbs = [
            {"text": "Home", "url": "/"},
            {"text": "Topics", "url": "/topics"},
            {"text": topic_name, "url": None}
        ]

        render(
            req, resp, "topic_detail.html",
            topic=topic,
            topic_name=topic_name,
            books=books,
            breadcrumbs=breadcrumbs,
            **pdf_context(f"/topics/{topic_name}/pdf"),
        )

    @api.route("/topics/{topic_name}/pdf")
    async def topic_detail_pdf(req, resp, *, topic_name):
        """Generate a PDF export for a topic detail page."""
        topic = get_topic_with_text(topic_name)
        if not topic:
            abort_404(req, resp, "Topic not found")
            return

        html_content = req.api.template(
            "topic_pdf.html",
            topic=topic,
            topic_name=topic_name,
        )
        filename = f"{topic_name}.pdf"
        await pdf_resp(resp, html_content, filename)
        return
