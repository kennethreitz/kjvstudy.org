"""Utility helpers for HTML-to-PDF generation with disk caching."""
import hashlib
import io
import sys
import os
from pathlib import Path
from typing import BinaryIO
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Starlette (not FastAPI) so this module imports under both the FastAPI app and
# the Responder port, which require different Starlette versions.
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

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
_pdf_executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="pdf_worker")

# Disk cache directory for generated PDFs
PDF_CACHE_DIR = Path(os.getenv("PDF_CACHE_DIR", "/tmp/pdf-cache"))
PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_key(html_content: str) -> str:
    """Generate a stable cache key from HTML content."""
    return hashlib.sha256(html_content.encode()).hexdigest()


def _render_pdf_sync(html_content: str) -> BinaryIO:
    """Internal synchronous PDF rendering function with disk cache."""
    if not WEASYPRINT_AVAILABLE or HTML is None:
        raise RuntimeError("WeasyPrint is not available for PDF generation")

    key = _cache_key(html_content)
    cache_path = PDF_CACHE_DIR / f"{key}.pdf"

    # Serve from disk cache if available
    if cache_path.exists():
        pdf_buffer = io.BytesIO(cache_path.read_bytes())
        return pdf_buffer

    # Render and cache to disk
    pdf_buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)

    # Write atomically to avoid serving partial files
    tmp_path = cache_path.with_suffix(".tmp")
    tmp_path.write_bytes(pdf_buffer.getvalue())
    tmp_path.rename(cache_path)

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
    Cached PDFs are served from disk without re-rendering.

    Returns a BytesIO instance positioned at the beginning of the generated PDF.
    Raises RuntimeError if WeasyPrint isn't available at runtime.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_pdf_executor, _render_pdf_sync, html_content)


def require_pdf_available():
    """Raise 503 if PDF generation isn't available (WeasyPrint missing)."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed.",
        )


def pdf_context(pdf_url: str) -> dict:
    """Template-context fragment for a page that offers a PDF download.

    Returns ``pdf_available`` plus ``pdf_url`` (None when PDF rendering is
    unavailable, so templates hide the download button). Shared by the paired
    detail handlers (resource, study guide, topic, interlinear, reading plan).
    """
    return {
        "pdf_available": WEASYPRINT_AVAILABLE,
        "pdf_url": pdf_url if WEASYPRINT_AVAILABLE else None,
    }


async def pdf_response(html: str, filename: str) -> StreamingResponse:
    """Render HTML to a PDF download response (attachment)."""
    pdf_buffer = await render_html_to_pdf_async(html)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
