"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router
from .resources import router as resources_router
from .family_tree import router as family_tree_router
from .study_guides import router as study_guides_router
from .commentary import router as commentary_router
from .stories import router as stories_router
from .utility import router as utility_router
from .bible import router as bible_router, init_commentary_functions as init_bible_commentary
from .reading_plans import router as reading_plans_router
from .topics import router as topics_router
from .strongs import router as strongs_router
from .timeline import router as timeline_router
from .about import router as about_router
from .main import router as main_router
from .misc import router as misc_router, init_search_family_tree

__all__ = [
    'api_router',
    'resources_router',
    'family_tree_router',
    'study_guides_router',
    'commentary_router',
    'stories_router',
    'utility_router',
    'bible_router', 'init_bible_commentary',
    'reading_plans_router',
    'topics_router',
    'strongs_router',
    'timeline_router',
    'about_router',
    'main_router',
    'misc_router', 'init_search_family_tree',
]
