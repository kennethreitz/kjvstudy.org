"""Utility helpers for HTML-to-PDF generation."""
import io
from typing import BinaryIO

try:  # pragma: no cover - optional dependency
    from weasyprint import HTML  # type: ignore
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):  # pragma: no cover - handled gracefully elsewhere
    HTML = None
    WEASYPRINT_AVAILABLE = False


def render_html_to_pdf(html_content: str) -> BinaryIO:
    """Render HTML content to a PDF byte stream.

    Returns a BytesIO instance positioned at the beginning of the generated PDF.
    Raises RuntimeError if WeasyPrint isn't available at runtime.
    """
    if not WEASYPRINT_AVAILABLE or HTML is None:
        raise RuntimeError("WeasyPrint is not available for PDF generation")

    pdf_buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer
