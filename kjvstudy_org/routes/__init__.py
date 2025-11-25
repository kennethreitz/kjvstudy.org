"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router
from .resources import router as resources_router, init_templates as init_resources_templates
from .family_tree import router as family_tree_router, init_templates as init_family_tree_templates

__all__ = [
    'api_router',
    'resources_router', 'init_resources_templates',
    'family_tree_router', 'init_family_tree_templates'
]
