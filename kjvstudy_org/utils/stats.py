"""Site-wide statistics, computed once and cached.

Shared by the /about page and the /api/stats endpoint so they report identical
numbers and only walk the data directory once per process.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

from ..kjv import bible
from .books import OT_BOOKS, NT_BOOKS

_DATA_DIR = Path(__file__).parent.parent / "data"


@lru_cache(maxsize=2)
def compute_site_stats(include_stories: bool = False) -> dict:
    """Compute comprehensive site statistics. Cached since the data never changes.

    When ``include_stories`` is True the result also carries a ``bible_stories``
    section (used by the /about page); the API omits it.
    """
    data_dir = _DATA_DIR

    # Bible statistics
    total_verses = bible.get_verse_count()
    total_books = len(bible.get_books())
    total_chapters = len(bible.get_chapters())
    total_words = bible.get_total_words()
    ot_books = len(OT_BOOKS)
    nt_books = len(NT_BOOKS)

    # Data file statistics
    total_json_files = len(list(data_dir.glob('**/*.json')))

    # Verse commentary statistics
    verse_commentary_files = len(list((data_dir / 'verse_commentary').glob('*.json')))
    total_commentary_verses = 0
    total_commentary_words = 0
    for file in (data_dir / 'verse_commentary').glob('*.json'):
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
        commentary = data.get('commentary', {})
        for chapter in commentary.values():
            for verse_data in chapter.values():
                total_commentary_verses += 1
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
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
        verses_with_cross_refs += len(data)
        for verse_refs in data.values():
            total_cross_refs += len(verse_refs)

    # Red letter statistics
    with open(data_dir / 'red_letter_verses.json', encoding="utf-8") as f:
        red_letter_data = json.load(f)
    total_red_letter_verses = len(red_letter_data['verses'])

    # Study resources
    study_guide_files = len(list((data_dir / 'study_guides').glob('*.json')))
    topic_files = len(list((data_dir / 'topics').glob('*.json')))
    resource_files = len(list((data_dir / 'resources').glob('*.json')))
    story_files = len(list((data_dir / 'stories').glob('*.json')))

    # Interlinear data size
    interlinear_file = data_dir / 'interlinear.json.gz'
    interlinear_size_mb = interlinear_file.stat().st_size / 1024 / 1024 if interlinear_file.exists() else 0

    # Calculate total data directory size
    total_data_size = sum(f.stat().st_size for f in data_dir.glob('**/*') if f.is_file())
    total_data_size_mb = total_data_size / 1024 / 1024

    # Book abbreviations
    with open(data_dir / 'bible_metadata.json', encoding="utf-8") as f:
        bible_metadata = json.load(f)
    total_abbreviations = len(bible_metadata.get('book_abbreviations', {}))

    # Biographies
    with open(data_dir / 'biographies.json', encoding="utf-8") as f:
        bio_data = json.load(f)
    total_biographies = len(bio_data.get('biographies', {}))

    # Reading plans
    reading_plan_files = len(list((data_dir / 'reading_plans').glob('*.json')))

    # Strong's concordance
    strongs_dir = data_dir / 'strongs'
    if strongs_dir.exists():
        with open(strongs_dir / 'hebrew.json', encoding="utf-8") as f:
            hebrew_data = json.load(f)
        with open(strongs_dir / 'greek.json', encoding="utf-8") as f:
            greek_data = json.load(f)
        total_hebrew_entries = len(hebrew_data)
        total_greek_entries = len(greek_data)
    else:
        total_hebrew_entries = 0
        total_greek_entries = 0

    stats = {
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

    if include_stories:
        stats['bible_stories'] = _compute_story_stats(data_dir, story_files)

    return stats


def _compute_story_stats(data_dir: Path, story_files: int) -> dict:
    """Aggregate Bible-story statistics (only needed by the /about page)."""
    total_stories = 0
    stories_with_kids = 0
    total_story_characters = set()
    total_story_themes = set()
    total_story_words = 0
    total_kids_story_words = 0
    for file in (data_dir / 'stories').glob('*.json'):
        try:
            with open(file, encoding="utf-8") as f:
                story_data = json.load(f)
            stories = story_data.get('stories', [])
            total_stories += len(stories)
            for story in stories:
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

    return {
        'categories': story_files,
        'total_stories': total_stories,
        'stories_with_kids': stories_with_kids,
        'unique_characters': len(total_story_characters),
        'unique_themes': len(total_story_themes),
        'total_words': total_story_words,
        'kids_words': total_kids_story_words,
    }
