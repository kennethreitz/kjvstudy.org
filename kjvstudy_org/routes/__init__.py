"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router
from .resources import router as resources_router, init_templates as init_resources_templates

__all__ = ['api_router', 'resources_router', 'init_resources_templates']
