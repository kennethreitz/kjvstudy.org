"""About routes - stats, cross-references index, and about page."""
import asyncio
import json
import re
from collections import defaultdict
from pathlib import Path

from turboapi import APIRouter, Request
from turboapi import HTMLResponse
from starlette.templating import Jinja2Templates

from ..kjv import bible
from ..utils.books import OT_BOOKS, NT_BOOKS

router = APIRouter()
templates = None


def init_templates(t: Jinja2Templates):
    """Initialize templates for about routes."""
    global templates
    templates = t


# =============================================================================
# Helper Functions (run in thread pool)
# =============================================================================

def _compute_stats() -> dict:
    """Compute all statistics - runs in thread pool to avoid blocking."""
    data_dir = Path(__file__).parent.parent / "data"

    # Bible statistics
    total_verses = bible.get_verse_count()
    total_books = len(bible.get_books())
    total_chapters = len(bible.get_chapters())

    # Calculate words in Bible
    total_words = sum(len(verse.text.split()) for verse in bible.iter_verses())

    # Count unique book types
    ot_books = len(OT_BOOKS)
    nt_books = len(NT_BOOKS)

    # Data file statistics
    total_json_files = len(list(data_dir.glob('**/*.json')))

    # Verse commentary statistics
    verse_commentary_files = len(list((data_dir / 'verse_commentary').glob('*.json')))
    total_commentary_verses = 0
    total_commentary_words = 0
    for file in (data_dir / 'verse_commentary').glob('*.json'):
        with open(file) as f:
            data = json.load(f)
        commentary = data.get('commentary', {})
        for chapter in commentary.values():
            for verse_data in chapter.values():
                total_commentary_verses += 1
                # Count words in analysis + historical
                analysis = verse_data.get('analysis', '')
                historical = verse_data.get('historical', '')
                # Strip HTML tags for accurate word count
                clean_analysis = re.sub(r'<[^>]+>', '', analysis)
                clean_historical = re.sub(r'<[^>]+>', '', historical)
                total_commentary_words += len(clean_analysis.split()) + len(clean_historical.split())

    # Cross-reference statistics
    cross_reference_files = len(list((data_dir / 'cross_references').glob('*.json')))
    total_cross_refs = 0
    verses_with_cross_refs = 0
    for file in (data_dir / 'cross_references').glob('*.json'):
        with open(file) as f:
            data = json.load(f)
        verses_with_cross_refs += len(data)
        for verse_refs in data.values():
            total_cross_refs += len(verse_refs)

    # Red letter statistics
    with open(data_dir / 'red_letter_verses.json') as f:
        red_letter_data = json.load(f)
    total_red_letter_verses = len(red_letter_data['verses'])

    # Study resources
    study_guide_files = len(list((data_dir / 'study_guides').glob('*.json')))
    topic_files = len(list((data_dir / 'topics').glob('*.json')))
    resource_files = len(list((data_dir / 'resources').glob('*.json')))
    story_files = len(list((data_dir / 'stories').glob('*.json')))

    # Bible Stories statistics
    total_stories = 0
    stories_with_kids = 0
    total_story_characters = set()
    total_story_themes = set()
    total_story_words = 0
    total_kids_story_words = 0
    for file in (data_dir / 'stories').glob('*.json'):
        try:
            with open(file) as f:
                story_data = json.load(f)
            stories = story_data.get('stories', [])
            total_stories += len(stories)
            for story in stories:
                # Count words in narrative
                narrative = story.get('narrative', '')
                total_story_words += len(narrative.split())
                if story.get('kids_narrative'):
                    stories_with_kids += 1
                    total_kids_story_words += len(story.get('kids_narrative', '').split())
                for char in story.get('characters', []):
                    total_story_characters.add(char)
                for theme in story.get('themes', []):
                    total_story_themes.add(theme)
        except (json.JSONDecodeError, IOError):
            continue

    # Interlinear data size
    interlinear_file = data_dir / 'interlinear.json.gz'
    interlinear_size_mb = interlinear_file.stat().st_size / 1024 / 1024 if interlinear_file.exists() else 0

    # Calculate total data directory size
    total_data_size = sum(f.stat().st_size for f in data_dir.glob('**/*') if f.is_file())
    total_data_size_mb = total_data_size / 1024 / 1024

    # Book abbreviations
    bible_metadata_file = data_dir / 'bible_metadata.json'
    with open(bible_metadata_file) as f:
        bible_metadata = json.load(f)
    total_abbreviations = len(bible_metadata.get('book_abbreviations', {}))

    # Biographies
    with open(data_dir / 'biographies.json') as f:
        bio_data = json.load(f)
    total_biographies = len(bio_data.get('biographies', {}))

    # Reading plans
    reading_plan_files = len(list((data_dir / 'reading_plans').glob('*.json')))

    # Strong's concordance
    strongs_dir = data_dir / 'strongs'
    if strongs_dir.exists():
        with open(strongs_dir / 'hebrew.json') as f:
            hebrew_data = json.load(f)
        with open(strongs_dir / 'greek.json') as f:
            greek_data = json.load(f)
        total_hebrew_entries = len(hebrew_data)
        total_greek_entries = len(greek_data)
    else:
        total_hebrew_entries = 0
        total_greek_entries = 0

    return {
        'bible': {
            'total_verses': total_verses,
            'total_books': total_books,
            'ot_books': ot_books,
            'nt_books': nt_books,
            'total_chapters': total_chapters,
            'total_words': total_words,
            'avg_words_per_verse': round(total_words / total_verses, 1),
            'avg_verses_per_chapter': round(total_verses / total_chapters, 1),
        },
        'commentary': {
            'files': verse_commentary_files,
            'verses_covered': total_commentary_verses,
            'total_words': total_commentary_words,
            'avg_words_per_verse': round(total_commentary_words / total_commentary_verses, 1) if total_commentary_verses > 0 else 0,
            'coverage_percent': round((total_commentary_verses / total_verses) * 100, 1),
        },
        'cross_references': {
            'files': cross_reference_files,
            'verses_with_refs': verses_with_cross_refs,
            'total_references': total_cross_refs,
            'avg_refs_per_verse': round(total_cross_refs / verses_with_cross_refs, 1) if verses_with_cross_refs > 0 else 0,
            'coverage_percent': round((verses_with_cross_refs / total_verses) * 100, 1),
        },
        'red_letter': {
            'total_verses': total_red_letter_verses,
            'percent_of_bible': round((total_red_letter_verses / total_verses) * 100, 1),
        },
        'study_resources': {
            'study_guides': study_guide_files,
            'topics': topic_files,
            'resources': resource_files,
            'stories': story_files,
            'biographies': total_biographies,
            'reading_plans': reading_plan_files,
        },
        'bible_stories': {
            'categories': story_files,
            'total_stories': total_stories,
            'stories_with_kids': stories_with_kids,
            'unique_characters': len(total_story_characters),
            'unique_themes': len(total_story_themes),
            'total_words': total_story_words,
            'kids_words': total_kids_story_words,
        },
        'language_tools': {
            'hebrew_entries': total_hebrew_entries,
            'greek_entries': total_greek_entries,
            'total_strongs': total_hebrew_entries + total_greek_entries,
            'interlinear_size_mb': round(interlinear_size_mb, 1),
        },
        'data': {
            'total_json_files': total_json_files,
            'total_size_mb': round(total_data_size_mb, 1),
            'book_abbreviations': total_abbreviations,
        }
    }


def _compute_crossref_index() -> tuple:
    """Compute cross-reference index - runs in thread pool."""
    data_dir = Path(__file__).parent.parent / "data" / "cross_references"

    # Build index of all verses with cross-references, grouped by book
    crossref_index = defaultdict(lambda: defaultdict(list))

    for file in sorted(data_dir.glob('*.json')):
        with open(file, 'r') as f:
            data = json.load(f)

            for verse_key, refs in data.items():
                # Parse verse key: "Book:Chapter:Verse"
                parts = verse_key.split(':')
                if len(parts) == 3:
                    book, chapter, verse = parts
                    crossref_index[book][int(chapter)].append({
                        'verse': int(verse),
                        'ref_count': len(refs)
                    })

    # Sort books in biblical order (OT then NT)
    biblical_order = OT_BOOKS + NT_BOOKS
    book_order = {book: i for i, book in enumerate(biblical_order)}

    # Convert to regular dict and sort
    crossref_index = {
        book: {
            chapter: sorted(verses, key=lambda x: x['verse'])
            for chapter, verses in sorted(chapters.items())
        }
        for book, chapters in sorted(crossref_index.items(), key=lambda x: book_order.get(x[0], 999))
    }

    # Calculate statistics
    total_books = len(crossref_index)
    total_verses = sum(
        len(verses)
        for chapters in crossref_index.values()
        for verses in chapters.values()
    )
    total_refs = sum(
        sum(v['ref_count'] for v in verses)
        for chapters in crossref_index.values()
        for verses in chapters.values()
    )

    return crossref_index, total_books, total_verses, total_refs


# =============================================================================
# Routes
# =============================================================================

@router.get("/about/stats", response_class=HTMLResponse)
async def stats(request: Request):
    """Hidden statistics page - comprehensive site metrics"""
    # Run heavy computation in thread pool
    stats_data = await asyncio.to_thread(_compute_stats)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Statistics", "url": None}
    ]

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "books": books,
            "stats": stats_data,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about/cross-references", response_class=HTMLResponse)
async def cross_references_index(request: Request):
    """Cross-references index - list all verses with cross-references"""
    # Run heavy I/O in thread pool
    crossref_index, total_books, total_verses, total_refs = await asyncio.to_thread(_compute_crossref_index)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Cross-References Index", "url": None}
    ]

    return templates.TemplateResponse(
        "cross_references_index.html",
        {
            "request": request,
            "books": books,
            "crossref_index": crossref_index,
            "total_books": total_books,
            "total_verses": total_verses,
            "total_refs": total_refs,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page - site information, creator, data sources, theological approach"""
    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": None}
    ]
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "books": books,
            "breadcrumbs": breadcrumbs,
        }
    )


@router.get("/about/accessibility", response_class=HTMLResponse)
async def accessibility(request: Request):
    """Accessibility page - keyboard navigation, screen readers, text-to-speech"""
    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Accessibility", "url": None}
    ]
    return templates.TemplateResponse(
        "accessibility.html",
        {
            "request": request,
            "books": books,
            "breadcrumbs": breadcrumbs,
        }
    )
