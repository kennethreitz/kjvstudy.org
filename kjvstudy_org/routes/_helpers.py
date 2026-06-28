"""Shared helpers for Responder route modules (the port of the FastAPI routes).

Every ported handler has the shape::

    @api.route("/path/{x}")
    async def handler(req, resp, *, x):
        render(req, resp, "template.html", **context)

- Path params are keyword-only args (``*, x``).
- Query params come from ``req.params`` (a multidict; ``.get("q")``).
- HTML responses go through :func:`render`; JSON via ``resp.media = {...}``.
- Redirects via :func:`redirect`; 404s via :func:`abort_404`.
"""


def render(req, resp, template, **context):
    """Render a Jinja template into ``resp.html``.

    Responder doesn't auto-inject the request the way Starlette's
    ``TemplateResponse`` does, and the templates use ``request.url.path``, so we
    pass ``request=req``.
    """
    resp.html = req.api.template(template, request=req, **context)


def redirect(resp, location, status_code=301):
    """Issue an HTTP redirect to ``location``."""
    resp.redirect(location, status_code=status_code)


def abort_404(req, resp, detail="Not Found"):
    """Render the shared error template with a 404 status."""
    from ..kjv import bible
    resp.status_code = 404
    render(req, resp, "error.html", status_code=404, detail=detail, books=bible.get_books())


async def pdf_resp(resp, html, filename):
    """Render ``html`` to a downloadable PDF response (503 if WeasyPrint absent)."""
    from ..utils.pdf import render_html_to_pdf_async, require_pdf_available
    require_pdf_available()
    buf = await render_html_to_pdf_async(html)
    resp.content = buf.getvalue()
    resp.mimetype = "application/pdf"
    resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
