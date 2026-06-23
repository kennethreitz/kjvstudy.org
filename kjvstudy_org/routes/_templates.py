"""Shared Jinja2Templates instance used by every route module.

Created here so all route modules import the same object; server.py registers
the custom filters and global variables on it at startup.
"""
from pathlib import Path

from fastapi.templating import Jinja2Templates

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
