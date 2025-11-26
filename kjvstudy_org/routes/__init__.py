"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router
from .resources import router as resources_router, init_templates as init_resources_templates
from .family_tree import router as family_tree_router, init_templates as init_family_tree_templates
from .study_guides import router as study_guides_router, init_templates as init_study_guides_templates
from .commentary import router as commentary_router, init_templates as init_commentary_templates
from .stories import router as stories_router, init_templates as init_stories_templates
from .utility import router as utility_router

__all__ = [
    'api_router',
    'resources_router', 'init_resources_templates',
    'family_tree_router', 'init_family_tree_templates',
    'study_guides_router', 'init_study_guides_templates',
    'commentary_router', 'init_commentary_templates',
    'stories_router', 'init_stories_templates',
    'utility_router',
]
