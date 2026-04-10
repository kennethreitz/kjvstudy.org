"""MiniJinja integration for FastAPI.

Drop-in replacement for fastapi.templating.Jinja2Templates using MiniJinja
(a fast Rust-based Jinja2-compatible template engine).
"""

import minijinja
from markupsafe import Markup, escape as markupsafe_escape
from starlette.responses import HTMLResponse


def _jinja2_compatible_finalizer(value):
    """Use markupsafe's escaping (same as Jinja2) instead of MiniJinja's more aggressive escaping."""
    if isinstance(value, Markup):
        return value
    return Markup(markupsafe_escape(str(value)))


class _TemplateWrapper:
    """Wraps a MiniJinja environment + template name to support .render() calls."""

    def __init__(self, env, name):
        self._env = env
        self._name = name

    def render(self, *args, **kwargs):
        if args and isinstance(args[0], dict):
            kwargs.update(args[0])
        return self._env.render_template(self._name, **kwargs)


class MiniJinjaTemplates:
    """FastAPI-compatible template renderer backed by MiniJinja."""

    def __init__(self, directory: str):
        self.directory = directory
        self.env = minijinja.Environment(
            loader=minijinja.load_from_path(directory),
        )
        self.env.auto_escape_callback = lambda name: name.endswith((".html", ".xml"))
        self.env.finalizer = _jinja2_compatible_finalizer
        self.env.reload_before_render = False

    def get_template(self, name: str):
        """Return a template wrapper with a .render() method, matching Jinja2 API."""
        return _TemplateWrapper(self.env, name)

    def TemplateResponse(self, request_or_name, name_or_context=None, context=None, status_code=200, **kwargs):
        """Render a template and return an HTMLResponse.

        Supports both calling conventions:
          TemplateResponse(request, "name.html", {...})        # new Starlette style
          TemplateResponse("name.html", {"request": req, ...}) # old Starlette style
        """
        if isinstance(request_or_name, str):
            # Old style: TemplateResponse("name.html", {"request": req, ...})
            name = request_or_name
            ctx = dict(name_or_context) if name_or_context else {}
        else:
            # New style: TemplateResponse(request, "name.html", {...})
            name = name_or_context
            ctx = dict(context) if context else {}
            ctx["request"] = request_or_name
        html = self.env.render_template(name, **ctx)
        return HTMLResponse(content=html, status_code=status_code, **kwargs)
