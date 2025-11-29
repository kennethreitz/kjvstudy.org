"""Utility helpers for HTML-to-PDF generation."""
import io
import sys
import os
from typing import BinaryIO
from concurrent.futures import ThreadPoolExecutor
import asyncio

try:  # pragma: no cover - optional dependency
    # Suppress WeasyPrint's stdout/stderr noise during import
    _stdout = sys.stdout
    _stderr = sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        from weasyprint import HTML  # type: ignore
        WEASYPRINT_AVAILABLE = True
    finally:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = _stdout
        sys.stderr = _stderr
except (ImportError, OSError):  # pragma: no cover - handled gracefully elsewhere
    HTML = None
    WEASYPRINT_AVAILABLE = False

# Thread pool for CPU-intensive PDF generation
_pdf_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="pdf_worker")


def _render_pdf_sync(html_content: str) -> BinaryIO:
    """Internal synchronous PDF rendering function."""
    if not WEASYPRINT_AVAILABLE or HTML is None:
        raise RuntimeError("WeasyPrint is not available for PDF generation")

    pdf_buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer


def render_html_to_pdf(html_content: str) -> BinaryIO:
    """Synchronous wrapper for backward compatibility.

    NOTE: Use render_html_to_pdf_async() in async contexts to avoid blocking.

    Returns a BytesIO instance positioned at the beginning of the generated PDF.
    Raises RuntimeError if WeasyPrint isn't available at runtime.
    """
    return _render_pdf_sync(html_content)


async def render_html_to_pdf_async(html_content: str) -> BinaryIO:
    """Async-compatible PDF rendering that won't block the event loop.

    Runs PDF generation in a thread pool to prevent blocking FastAPI.

    Returns a BytesIO instance positioned at the beginning of the generated PDF.
    Raises RuntimeError if WeasyPrint isn't available at runtime.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_pdf_executor, _render_pdf_sync, html_content)
