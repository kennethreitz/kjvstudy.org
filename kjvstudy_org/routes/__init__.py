"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router, init_templates as init_api_templates
from .resources import router as resources_router, init_templates as init_resources_templates
from .family_tree import router as family_tree_router, init_templates as init_family_tree_templates
from .study_guides import router as study_guides_router, init_templates as init_study_guides_templates
from .commentary import router as commentary_router, init_templates as init_commentary_templates
from .stories import router as stories_router, init_templates as init_stories_templates
from .utility import router as utility_router
from .bible import router as bible_router, init_bible_templates, init_commentary_functions as init_bible_commentary
from .reading_plans import router as reading_plans_router, init_templates as init_reading_plans_templates
from .topics import router as topics_router, init_templates as init_topics_templates
from .strongs import router as strongs_router, init_templates as init_strongs_templates
from .timeline import router as timeline_router, init_templates as init_timeline_templates
from .about import router as about_router, init_templates as init_about_templates
from .main import router as main_router, init_templates as init_main_templates
from .misc import router as misc_router, init_templates as init_misc_templates, init_search_family_tree

__all__ = [
    'api_router', 'init_api_templates',
    'resources_router', 'init_resources_templates',
    'family_tree_router', 'init_family_tree_templates',
    'study_guides_router', 'init_study_guides_templates',
    'commentary_router', 'init_commentary_templates',
    'stories_router', 'init_stories_templates',
    'utility_router',
    'bible_router', 'init_bible_templates', 'init_bible_commentary',
    'reading_plans_router', 'init_reading_plans_templates',
    'topics_router', 'init_topics_templates',
    'strongs_router', 'init_strongs_templates',
    'timeline_router', 'init_timeline_templates',
    'about_router', 'init_about_templates',
    'main_router', 'init_main_templates',
    'misc_router', 'init_misc_templates', 'init_search_family_tree',
]
