"""Commentary system for AI-powered verse and chapter commentary.

This module contains the commentary generation system including:
- Commentary route handler
- Helper functions for generating theological commentary
- Book summaries, chapter overviews, and verse analysis
"""
import asyncio
import json
import random
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..utils.commentary_loader import load_commentary, load_commentary_flat
from ..utils.books import OT_BOOKS, NT_BOOKS, is_old_testament
from ..utils.helpers import get_books
from ..interlinear_loader import get_interlinear_data

router = APIRouter(tags=["Commentary"])

from ._templates import templates


def _compute_commentary_index() -> tuple:
    """Compute commentary index - runs in thread pool."""
    data_dir = Path(__file__).parent.parent / "data" / "verse_commentary"

    # Build index of all verses with commentary, grouped by book
    commentary_index = defaultdict(lambda: defaultdict(list))

    for file in sorted(data_dir.glob('*.json')):
        with open(file, 'r') as f:
            data = json.load(f)
            book = data.get('book')
            commentary = data.get('commentary', {})

            for chapter_num, chapter_data in commentary.items():
                for verse_num in sorted(chapter_data.keys(), key=int):
                    commentary_index[book][int(chapter_num)].append(int(verse_num))

    # Sort books in biblical order (OT then NT)
    biblical_order = OT_BOOKS + NT_BOOKS
    book_order = {book: i for i, book in enumerate(biblical_order)}

    commentary_index = {
        book: dict(sorted(chapters.items()))
        for book, chapters in sorted(commentary_index.items(), key=lambda x: book_order.get(x[0], 999))
    }

    # Calculate statistics
    total_books = len(commentary_index)
    total_verses = sum(
        len(verses)
        for chapters in commentary_index.values()
        for verses in chapters.values()
    )

    return commentary_index, total_books, total_verses


@router.get("/about/commentary", response_class=HTMLResponse)
async def commentary_index(request: Request):
    """Commentary index - list all verses with commentary"""
    # Run heavy I/O in thread pool
    commentary_idx, total_books, total_verses = await asyncio.to_thread(_compute_commentary_index)

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"},
        {"text": "Commentary Index", "url": None}
    ]

    # Get books list for navigation
    from ..kjv import bible
    books = bible.get_books()

    return templates.TemplateResponse(
        "commentary_index.html",
        {
            "request": request,
            "books": books,
            "commentary_index": commentary_idx,
            "total_books": total_books,
            "total_verses": total_verses,
            "breadcrumbs": breadcrumbs,
        }
    )

# Data directory paths
_DATA_DIR = Path(__file__).parent.parent / "data"
_WORD_STUDIES_PATH = _DATA_DIR / "word_studies.json"


@lru_cache(maxsize=1)
def _load_word_studies() -> dict:
    """Load word studies from JSON file. Cached since data never changes."""
    with open(_WORD_STUDIES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert flat JSON structure to nested structure expected by code
    converted = {}
    for word, info in data.items():
        entry = {}

        # Some words are OT-only, NT-only, or both
        if "ot_term" in info:
            entry["ot"] = {
                "term": info["ot_term"],
                "translit": info["ot_transliteration"],
                "meaning": info["ot_meaning"],
                "note": info["ot_note"],
                "strongs": info.get("ot_strongs", [])
            }

        if "nt_term" in info:
            entry["nt"] = {
                "term": info["nt_term"],
                "translit": info["nt_transliteration"],
                "meaning": info["nt_meaning"],
                "note": info["nt_note"],
                "strongs": info.get("nt_strongs", [])
            }

        converted[word] = entry
    return converted


@lru_cache(maxsize=1)
def _load_verse_commentary() -> dict:
    """Load verse commentary from per-book JSON files."""
    return load_commentary()


def _get_enhanced_commentary(book: str, chapter: int, verse_num: int):
    """Fetch enhanced commentary entry with tolerant key handling."""
    data = _load_verse_commentary()

    # Try direct lookup
    book_data = data.get(book) or data.get(book.strip())
    if book_data:
        chapter_data = book_data.get(chapter) or book_data.get(str(chapter))
        if chapter_data:
            entry = chapter_data.get(verse_num) or chapter_data.get(str(verse_num))
            if entry:
                return entry

    # Fallback to flat lookup (handles any residual key formatting)
    flat = load_commentary_flat()
    return flat.get(f"{book} {chapter}:{verse_num}")


def _format_numbered_lists(text: str) -> str:
    """Convert (1), (2) style lists into HTML ordered lists."""
    import re

    if not text:
        return text

    def _convert(pattern: str, payload: str) -> str:
        markers = list(re.finditer(pattern, payload))
        if len(markers) < 2:
            return payload

        numbers = [int(m.group(1)) for m in markers]
        if numbers[0] != 1:
            return payload

        seq_length = 1
        for i in range(1, len(numbers)):
            if numbers[i] == seq_length + 1:
                seq_length += 1
            else:
                break

        if seq_length < 2:
            return payload

        markers_seq = markers[:seq_length]
        list_items = []
        for i, marker in enumerate(markers_seq):
            start = marker.end()
            if i + 1 < len(markers_seq):
                end = markers_seq[i + 1].start()
            else:
                remaining = payload[start:]
                end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining)
                end = start + end_match.start() + 1 if end_match else len(payload)

            item_text = payload[start:end].strip().rstrip(';,')
            if item_text.endswith(' and'):
                item_text = item_text[:-4]
            list_items.append(f'<li>{item_text}</li>')

        html_list = '<ol>' + ''.join(list_items) + '</ol>'
        list_start = markers_seq[0].start()
        last_marker = markers_seq[-1]
        last_item_start = last_marker.end()
        remaining_after_last = payload[last_item_start:]
        end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining_after_last)
        list_end = last_item_start + end_match.start() + 1 if end_match else len(payload)

        after_list = payload[list_end:].strip()
        if after_list:
            return payload[:list_start] + html_list + '</p><p>' + after_list
        return payload[:list_start] + html_list

    # Try classic (1) pattern first
    primary_pattern = r'\((\d+)\)\s*'
    converted = _convert(primary_pattern, text)
    if converted != text:
        return converted

    # Fallback: bare "1)" patterns preceded by whitespace
    fallback_pattern = r'(?<=\s)(\d+)\)\s*'
    return _convert(fallback_pattern, text)


def get_verse_text(book, chapter, verse):
    """Get the text of a specific verse."""
    from ..kjv import bible
    return bible.get_verse_text(book, chapter, verse) or ""


@router.get("/commentary/{book}/{chapter}")
async def commentary_redirect(book: str, chapter: int):
    """Redirect old chapter commentary URLs to chapter page"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}", status_code=301)


def link_bible_references(text):
    """Convert Bible references in text to clickable links

    Handles formats like:
    - Genesis 6:8
    - 1 John 4:8
    - Romans 5:1
    - Ephesians 2:8-10
    - Matthew 5:3-12
    """
    import re

    # Pattern matches book names (including numbered books) + chapter + verse (with optional range)
    # Examples: "Genesis 6:8", "1 John 4:8", "Romans 5:1", "Ephesians 2:8-10"
    pattern = r'\b((?:[123]\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def replace_reference(match):
        book_name = match.group(1)  # e.g., "Genesis", "1 John", "Song of Solomon"
        chapter = match.group(2)    # e.g., "6"
        verse_start = match.group(3)  # e.g., "8"
        verse_end = match.group(4)  # e.g., "10" (optional)

        # Full matched text (e.g., "Genesis 6:8" or "Romans 5:1-5")
        full_ref = match.group(0)

        # Create the link URL using chapter anchor
        if verse_end:
            url = f'/book/{book_name}/chapter/{chapter}#verse-{verse_start}-{verse_end}'
        else:
            url = f'/book/{book_name}/chapter/{chapter}#verse-{verse_start}'

        # Return the linked reference
        return f'<a href="{url}">{full_ref}</a>'

    # Replace all matches
    linked_text = re.sub(pattern, replace_reference, text)
    return linked_text


def generate_word_study_sidenotes(verse_text, book, chapter, verse_num, shown_words=None, for_pdf=False):
    """Generate Hebrew/Greek/Aramaic word study sidenotes for key terms in the verse

    Uses intelligent selection to show only 1-2 word studies per verse, creating variety
    across chapters rather than showing every theological term. Avoids repeating words
    that have already been shown in the same chapter.

    Cross-references with interlinear data to ensure the word study matches the actual
    Greek/Hebrew word used in this specific verse (via Strong's numbers).

    Args:
        verse_text: The text of the verse
        book: The book name
        chapter: The chapter number
        verse_num: The verse number
        shown_words: Set of words already shown in this chapter (lowercase)
        for_pdf: If True, show word studies more liberally for PDF output
    """
    if shown_words is None:
        shown_words = set()

    verse_lower = verse_text.lower()

    # Determine if Old Testament (Hebrew/Aramaic) or New Testament (Greek)
    is_ot = is_old_testament(book)

    # Load word studies from JSON file
    word_studies = _load_word_studies()

    # Only show important theological terms (not common words like 'walk', 'call')
    priority_words = {
        'god', 'lord', 'spirit', 'holy', 'christ', 'messiah',
        'salvation', 'save', 'redeem', 'atonement', 'propitiation', 'reconcile',
        'grace', 'mercy', 'faith', 'hope', 'love', 'truth',
        'sin', 'iniquity', 'transgression', 'wrath', 'judgment', 'forgive',
        'covenant', 'law', 'gospel', 'word',
        'heaven', 'kingdom', 'eternal', 'resurrection', 'glory',
        'blood', 'sacrifice', 'lamb', 'altar', 'priest',
        'righteous', 'justify', 'sanctify', 'holy',
        'angel', 'prophet', 'apostle',
        'baptize', 'repent', 'believe', 'confess',
        'born again', 'adoption', 'elect', 'predestine',
    }
    word_studies = {k: v for k, v in word_studies.items() if k in priority_words}

    # Get interlinear data for this verse to cross-reference Strong's numbers
    interlinear = get_interlinear_data(book, chapter, verse_num)
    verse_strongs = set()
    strongs_to_interlinear = {}  # Map Strong's number to interlinear word data
    if interlinear:
        for word_data in interlinear:
            strongs = word_data.get('strongs', '')
            if strongs:
                verse_strongs.add(strongs)
                strongs_to_interlinear[strongs] = word_data

    # Build reverse lookup: Strong's number -> word study entries
    # This allows us to find word studies that match the verse's actual Greek/Hebrew
    strongs_to_study = {}
    testament_key = 'ot' if is_ot else 'nt'
    for word, studies in word_studies.items():
        study = studies.get(testament_key)
        if study:
            for s in study.get('strongs', []):
                if s not in strongs_to_study:
                    strongs_to_study[s] = []
                strongs_to_study[s].append((word, study))

    # First, collect all potential word studies in this verse
    # EXCLUDE words that have already been shown in this chapter
    potential_sidenotes = []
    added_words = set()  # Track which word studies we've added

    for word, studies in word_studies.items():
        # Skip if this word was recently shown (within cooldown period)
        if word in shown_words:
            continue
        if word in verse_lower:
            # Use appropriate testament
            study = studies.get(testament_key, studies.get('ot') or studies.get('nt'))
            if study:
                # Cross-reference with interlinear data if available
                study_strongs = study.get('strongs', [])
                if verse_strongs and study_strongs:
                    # Check if any of the word study's Strong's numbers match the verse
                    matching_strongs = [s for s in study_strongs if s in verse_strongs]
                    if not matching_strongs:
                        # The word appears in English but doesn't match the expected Hebrew/Greek
                        # Try to find another word study that DOES match the verse's Strong's
                        found_alternative = False
                        for strongs_num in verse_strongs:
                            if strongs_num in strongs_to_study:
                                for alt_word, alt_study in strongs_to_study[strongs_num]:
                                    if alt_word not in shown_words and alt_word not in added_words:
                                        # Get the first matching Strong's number for this study
                                        alt_strongs = alt_study.get('strongs', [])
                                        matched_strongs = next((s for s in alt_strongs if s in verse_strongs), alt_strongs[0] if alt_strongs else None)
                                        potential_sidenotes.append({
                                            "word": alt_word.title(),
                                            "term": alt_study['term'],
                                            "translit": alt_study['translit'],
                                            "meaning": alt_study['meaning'],
                                            "note": link_bible_references(alt_study['note']),
                                            "strongs": matched_strongs
                                        })
                                        added_words.add(alt_word)
                                        found_alternative = True
                                        break
                            if found_alternative:
                                break
                        continue

                if word not in added_words:
                    # Get the first matching Strong's number for this study
                    matched_strongs = next((s for s in study_strongs if s in verse_strongs), study_strongs[0] if study_strongs else None)
                    potential_sidenotes.append({
                        "word": word.title(),
                        "term": study['term'],
                        "translit": study['translit'],
                        "meaning": study['meaning'],
                        "note": link_bible_references(study['note']),
                        "strongs": matched_strongs
                    })
                    added_words.add(word)

    if not potential_sidenotes:
        return []

    # Deterministic selection based on verse for consistency
    import random
    random.seed(f"{book}{chapter}{verse_num}")

    # Show 1 sidenote per verse (2 for PDF) to prevent horizontal collision in margin
    max_sidenotes = 2 if for_pdf else 1

    # Randomly select which word study to show from those available
    selected = random.sample(potential_sidenotes, min(max_sidenotes, len(potential_sidenotes)))
    return selected


def generate_commentary(book, chapter, verse):
    """Generate AI-powered commentary for a specific verse"""
    # Load enhanced commentary from JSON file
    enhanced_commentary = _load_verse_commentary()

    # Check for enhanced commentary first
    commentary_data = _get_enhanced_commentary(book, chapter, verse.verse)
    if commentary_data:
        commentary_data = {
            "analysis": _format_numbered_lists(commentary_data.get("analysis", "")),
            "historical": _format_numbered_lists(commentary_data.get("historical", "")),
            "questions": commentary_data.get("questions", []),
            "theological": _format_numbered_lists(commentary_data.get("theological", "")) if commentary_data.get("theological") else None,
        }
        return {
            "analysis": commentary_data["analysis"],
            "historical": commentary_data["historical"],
            "questions": commentary_data["questions"],
            "theological": commentary_data.get("theological"),
            "cross_references": generate_cross_references(book, chapter, verse.verse, verse.text),
            "is_enhanced": True
        }

    # For all other books/chapters, use enhanced theological analysis
    verse_text = verse.text.lower()
    verse_number = verse.verse

    # Generate sophisticated analysis based on biblical themes and context
    theme = get_enhanced_theological_theme(verse_text, book)
    key_concept = extract_theological_concept(verse_text, book)
    literary_context = analyze_literary_context(book, chapter)

    # Create rich, scholarly analysis
    analysis_templates = [
        f"This verse develops the {theme} theme central to {book}. The concept of <strong>{key_concept}</strong> reflects {get_theological_significance(book, theme)}. {get_literary_analysis(verse_text, book, literary_context)} The original language emphasizes {get_linguistic_insight(verse_text, book)}, providing deeper understanding of the author's theological intention.",

        f"Within the broader context of {book}, this passage highlights {theme} through {get_rhetorical_device(verse_text)}. The theological weight of <strong>{key_concept}</strong> {get_doctrinal_significance(key_concept, book)}. This verse contributes to the book's overall argument by {get_structural_purpose(book, chapter, verse_number)}.",

        f"The {theme} theme here intersects with {get_biblical_theology_connection(theme, book)}. Biblical theology recognizes this as part of {get_canonical_development(theme)}. The phrase emphasizing <strong>{key_concept}</strong> {get_systematic_theology_insight(key_concept)} and connects to the broader scriptural witness about {get_cross_biblical_theme(theme)}."
    ]

    historical_templates = [
        f"The historical context of {get_detailed_time_period(book)} provides crucial background for understanding this verse. {get_comprehensive_historical_context(book)} The {get_cultural_background(book, verse_text)} would have shaped how the original audience understood {key_concept}. Archaeological and historical evidence reveals {get_archaeological_insight(book, theme)}.",

        f"This passage must be understood within {get_socio_political_context(book)}. The author writes to address {get_historical_audience_situation(book, chapter)}, making the emphasis on {theme} particularly relevant. Historical documents from this period show {get_historical_parallel(book, key_concept)}, illuminating the verse's original impact.",

        f"The literary and historical milieu of {get_literary_historical_context(book)} shapes this text's meaning. {get_historical_theological_development(book, theme)} Understanding {get_ancient_worldview_context(book)} helps modern readers appreciate why the author emphasizes {key_concept} in this particular way."
    ]

    question_templates = [
        f"How does the {theme} theme in this verse connect to the overarching narrative of Scripture, and what does this reveal about God's character and purposes?",
        f"In what ways does understanding {key_concept} in its original context challenge or deepen contemporary Christian thinking about {theme}?",
        f"How might the original audience's understanding of {key_concept} differ from modern interpretations, and what bridges can be built between ancient meaning and contemporary application?",
        f"What systematic theological implications arise from this verse's treatment of {theme}, and how does it contribute to a biblical theology of {get_related_doctrine(theme)}?",
        f"How does this verse's literary context within {book} chapter {chapter} illuminate its theological significance, and what does this teach us about biblical interpretation?",
        f"What practical applications emerge from understanding {theme} as presented in this verse, particularly in light of {get_contemporary_relevance(theme, key_concept)}?",
        f"How does this passage contribute to our understanding of {get_biblical_theological_trajectory(theme)}, and what implications does this have for Christian discipleship?",
        f"In what ways does this verse's emphasis on {key_concept} address {get_contemporary_theological_challenge(theme)}, and how should the church respond?"
    ]

    # Generate cross-references with variety per verse
    cross_refs = get_enhanced_cross_references(book, chapter, verse_number, verse_text, theme, key_concept)

    # Only return cross-references for verses without specific commentary
    # Generic commentary adds no value and should not be displayed
    return {
        "analysis": None,
        "historical": None,
        "questions": None,
        "cross_references": cross_refs,
        "is_enhanced": False
    }


def get_enhanced_theological_theme(verse_text, book):
    """Extract primary theological theme from verse text considering book context"""
    themes = {
        # Core theological themes
        "salvation": ["save", "redeem", "deliver", "rescue", "forgive", "justify", "sanctify"],
        "covenant": ["covenant", "promise", "faithful", "oath", "testament", "pledge"],
        "kingdom of God": ["kingdom", "reign", "rule", "throne", "dominion", "authority"],
        "divine love": ["love", "mercy", "compassion", "grace", "kindness", "tender"],
        "faith and obedience": ["faith", "believe", "trust", "obey", "follow", "serve"],
        "judgment and justice": ["judge", "justice", "righteous", "condemn", "punish", "wrath"],
        "worship and praise": ["worship", "praise", "glory", "honor", "magnify", "exalt"],
        "suffering and persecution": ["suffer", "afflict", "persecute", "trial", "tribulation"],
        "hope and restoration": ["hope", "restore", "renew", "heal", "comfort", "peace"],
        "wisdom and understanding": ["wise", "wisdom", "understand", "knowledge", "discern"],
        "creation and providence": ["create", "made", "form", "establish", "sustain", "provide"],
        "sin and rebellion": ["sin", "transgress", "rebel", "iniquity", "evil", "wicked"]
    }

    # Book-specific theme adjustments
    book_themes = {
        "Genesis": ["creation and providence", "covenant", "divine love"],
        "Psalms": ["worship and praise", "divine love", "suffering and persecution"],
        "Romans": ["salvation", "faith and obedience", "judgment and justice"],
        "John": ["divine love", "salvation", "faith and obedience"],
        "Revelation": ["kingdom of God", "judgment and justice", "hope and restoration"]
    }

    primary_themes = book_themes.get(book, list(themes.keys())[:3])

    for theme in primary_themes:
        if any(word in verse_text for word in themes[theme]):
            return theme

    # Fallback to most common theme for the book
    return primary_themes[0] if primary_themes else "divine love"

def extract_theological_concept(verse_text, book):
    """Extract key theological concept from verse"""
    concepts = ["grace", "faith", "love", "righteousness", "salvation", "redemption",
               "covenant", "kingdom", "glory", "peace", "wisdom", "truth", "life",
               "hope", "mercy", "justice", "holiness", "forgiveness", "eternal life"]

    for concept in concepts:
        if concept in verse_text:
            return concept

    # Extract meaningful phrases if no single concept found
    if "lord" in verse_text or "god" in verse_text:
        return "divine sovereignty"
    elif "people" in verse_text or "nation" in verse_text:
        return "covenant community"
    else:
        return "divine revelation"

def analyze_literary_context(book, chapter):
    """Provide literary context for the book and chapter"""
    contexts = {
        "Genesis": f"foundational narrative establishing God's relationship with creation and humanity",
        "Psalms": f"worship literature expressing the full range of human experience before God",
        "Romans": f"systematic theological exposition of the gospel",
        "John": f"theological biography emphasizing Jesus' divine identity",
        "Revelation": f"apocalyptic literature revealing God's ultimate victory",
        "1 Corinthians": f"pastoral letter addressing practical Christian living issues",
        "Matthew": f"gospel presenting Jesus as the fulfillment of Jewish Messianic hope"
    }
    return contexts.get(book, f"biblical literature contributing to the canon's theological witness")

def get_theological_significance(book, theme):
    """Get theological significance of theme within book context"""
    significance_map = {
        ("Genesis", "creation and providence"): "God's absolute sovereignty over all existence",
        ("Psalms", "worship and praise"): "the proper human response to God's character and works",
        ("Romans", "salvation"): "justification by faith as the foundation of Christian hope",
        ("John", "divine love"): "the essential nature of God revealed through Christ",
        ("Revelation", "kingdom of God"): "the ultimate establishment of divine rule over creation"
    }
    key = (book, theme)
    return significance_map.get(key, f"the development of {theme} within biblical theology")

def get_doctrinal_significance(concept, book):
    """Provide doctrinal significance of theological concept"""
    return f"connects to fundamental Christian doctrine about {concept}, contributing to our understanding of God's nature and relationship with humanity"

def get_enhanced_cross_references(book, chapter, verse_number, verse_text, theme, concept):
    """Generate enhanced cross-references based on theme and concept with variety"""
    # Expanded pool of cross-references for each theme
    theme_refs = {
        "salvation": [
            {"text": "Romans 10:9", "url": "/book/Romans/chapter/10#verse-9", "context": "Confession and faith"},
            {"text": "Ephesians 2:8-9", "url": "/book/Ephesians/chapter/2#verse-8", "context": "Salvation by grace"},
            {"text": "Acts 4:12", "url": "/book/Acts/chapter/4#verse-12", "context": "No other name"},
            {"text": "Titus 3:5", "url": "/book/Titus/chapter/3#verse-5", "context": "Not by works"},
            {"text": "John 3:16", "url": "/book/John/chapter/3#verse-16", "context": "God's love and salvation"}
        ],
        "divine love": [
            {"text": "1 John 4:8", "url": "/book/1 John/chapter/4#verse-8", "context": "God is love"},
            {"text": "Romans 5:8", "url": "/book/Romans/chapter/5#verse-8", "context": "Love in Christ's death"},
            {"text": "Jeremiah 31:3", "url": "/book/Jeremiah/chapter/31#verse-3", "context": "Everlasting love"},
            {"text": "John 15:13", "url": "/book/John/chapter/15#verse-13", "context": "Greater love"}
        ],
        "faith and obedience": [
            {"text": "Hebrews 11:1", "url": "/book/Hebrews/chapter/11#verse-1", "context": "Definition of faith"},
            {"text": "James 2:17", "url": "/book/James/chapter/2#verse-17", "context": "Faith and works"},
            {"text": "Proverbs 3:5-6", "url": "/book/Proverbs/chapter/3#verse-5", "context": "Trust in the Lord"},
            {"text": "John 14:15", "url": "/book/John/chapter/14#verse-15", "context": "Love and obedience"}
        ],
        "covenant": [
            {"text": "Genesis 17:7", "url": "/book/Genesis/chapter/17#verse-7", "context": "Everlasting covenant"},
            {"text": "Jeremiah 31:31", "url": "/book/Jeremiah/chapter/31#verse-31", "context": "New covenant"},
            {"text": "Hebrews 8:6", "url": "/book/Hebrews/chapter/8#verse-6", "context": "Better covenant"}
        ],
        "kingdom of God": [
            {"text": "Matthew 6:33", "url": "/book/Matthew/chapter/6#verse-33", "context": "Seek first the kingdom"},
            {"text": "Luke 17:21", "url": "/book/Luke/chapter/17#verse-21", "context": "Kingdom within you"},
            {"text": "Colossians 1:13", "url": "/book/Colossians/chapter/1#verse-13", "context": "Transferred to kingdom"}
        ]
    }

    # Get available references for the theme
    available_refs = theme_refs.get(theme, [
        {"text": "Psalm 119:105", "url": "/book/Psalms/chapter/119#verse-105", "context": "Word is a lamp"},
        {"text": "2 Timothy 3:16", "url": "/book/2 Timothy/chapter/3#verse-16", "context": "All Scripture inspired"},
        {"text": "Isaiah 40:8", "url": "/book/Isaiah/chapter/40#verse-8", "context": "Word stands forever"},
        {"text": "Matthew 24:35", "url": "/book/Matthew/chapter/24#verse-35", "context": "Words not pass away"}
    ])

    # Use verse number to create variety - different verses get different refs
    import random
    random.seed(f"{book}{chapter}{verse_number}")  # Deterministic but varied per verse
    selected = random.sample(available_refs, min(2, len(available_refs)))

    return selected


def get_literary_analysis(verse_text, book, literary_context):
    """Provide literary analysis of the verse within its context"""
    if "lord" in verse_text or "god" in verse_text:
        return f"The divine name or title here functions within {literary_context} to establish theological authority and covenantal relationship."
    elif any(word in verse_text for word in ["love", "mercy", "grace"]):
        return f"The emotional and relational language employed here is characteristic of {literary_context}, emphasizing the personal nature of divine-human relationship."
    else:
        return f"The literary structure and word choice here contribute to {literary_context}, advancing the author's theological argument."

def get_linguistic_insight(verse_text, book):
    """Provide insight into original language significance"""
    insights = {
        "lord": "the covenant name Yahweh, emphasizing God's faithfulness to His promises",
        "love": "agape in Greek contexts or hesed in Hebrew, indicating covenantal loyalty",
        "faith": "pistis in Greek, encompassing both belief and faithfulness",
        "salvation": "soteria in Greek or yeshua in Hebrew, indicating deliverance and wholeness",
        "grace": "charis in Greek or hen in Hebrew, emphasizing unmerited divine favor"
    }

    for word, insight in insights.items():
        if word in verse_text:
            return insight
    return "careful word choice that would have carried specific theological weight for the original audience"

def get_rhetorical_device(verse_text):
    """Identify rhetorical or literary devices in the verse"""
    if "like" in verse_text or "as" in verse_text:
        return "simile or metaphorical language"
    elif any(word in verse_text for word in ["all", "every", "none", "nothing"]):
        return "universal language and absolute statements"
    elif "?" in verse_text:
        return "rhetorical questioning that engages the reader"
    else:
        return "declarative statements that establish theological truth"

def get_structural_purpose(book, chapter, verse_number):
    """Explain how the verse functions structurally within the book"""
    if verse_number == 1:
        return f"introducing key themes that will be developed throughout {book}"
    elif chapter == 1:
        return f"establishing foundational concepts crucial to {book}'s theological argument"
    else:
        return f"building upon previous themes while advancing the overall message of {book}"

def get_biblical_theology_connection(theme, book):
    """Connect the theme to broader biblical theology"""
    connections = {
        "salvation": "the metanarrative of redemption running from Genesis to Revelation",
        "divine love": "God's covenantal faithfulness demonstrated throughout salvation history",
        "kingdom of God": "the progressive revelation of God's rule from creation to consummation",
        "covenant": "God's relationship with His people from Abraham through the new covenant",
        "faith and obedience": "the proper human response to divine revelation across Scripture"
    }
    return connections.get(theme, "the broader canonical witness to God's character and purposes")

def get_canonical_development(theme):
    """Describe how the theme develops across the biblical canon"""
    developments = {
        "salvation": "a unified storyline from the promise in Genesis 3:15 to its fulfillment in Christ",
        "divine love": "progressive revelation from covenant love in the Old Testament to agape love in the New",
        "kingdom of God": "development from creation mandate through Davidic kingdom to eschatological fulfillment",
        "covenant": "evolution from creation covenant through Abrahamic, Mosaic, Davidic, to new covenant"
    }
    return developments.get(theme, "progressive revelation that finds its culmination in Christ")

def get_systematic_theology_insight(concept):
    """Provide systematic theological perspective on the concept"""
    insights = {
        "grace": "relates to the doctrine of soteriology and God's unmerited favor in salvation",
        "faith": "central to epistemology and the means by which humans receive divine revelation",
        "love": "fundamental to theology proper, revealing God's essential nature and character",
        "salvation": "encompasses justification, sanctification, and glorification in the ordo salutis",
        "kingdom": "relates to eschatology and the ultimate purpose of God's redemptive plan"
    }
    return insights.get(concept, "contributes to our systematic understanding of Christian doctrine")

def get_cross_biblical_theme(theme):
    """Identify how the theme appears across Scripture"""
    cross_biblical = {
        "salvation": "God's saving work from the Exodus to the cross",
        "divine love": "hesed in the Old Testament and agape in the New Testament",
        "kingdom of God": "God's reign from creation through the millennial kingdom",
        "covenant": "God's relational commitment from Noah to the new covenant"
    }
    return cross_biblical.get(theme, "God's consistent character and purposes")

def get_detailed_time_period(book):
    """Provide detailed historical time period for the book"""
    periods = {
        "Genesis": "the patriarchal period (c. 2000-1500 BCE) and primeval history",
        "Exodus": "the period of Egyptian bondage and wilderness wandering (c. 1440-1400 BCE)",
        "Psalms": "the monarchic period, particularly David's reign (c. 1000-970 BCE)",
        "Romans": "the early imperial period under Nero (c. 57 CE)",
        "John": "the late first century during increasing tension between synagogue and church",
        "Revelation": "the Domitian persecution period (c. 95 CE)"
    }
    return periods.get(book, "the biblical period relevant to this book's composition")

def get_comprehensive_historical_context(book):
    """Provide comprehensive historical background"""
    contexts = {
        "Genesis": "The ancient Near Eastern world with its creation myths, flood narratives, and patriarchal social structures provided the cultural backdrop against which God's revelation stands in stark contrast.",
        "Romans": "The Roman Empire at its height, with sophisticated legal systems, diverse religious practices, and increasing Christian presence in major urban centers shaped Paul's theological arguments.",
        "Psalms": "The Israelite monarchy with its temple worship, court life, and constant military threats created the liturgical and emotional context for these prayers and praises."
    }
    return contexts.get(book, "The historical and cultural milieu of the biblical world informed the author's theological expression and the audience's understanding.")

def get_archaeological_insight(book, theme):
    """Provide relevant archaeological insight"""
    insights = {
        ("Genesis", "creation and providence"): "Ancient Near Eastern creation texts like Enuma Elish provide comparative context for understanding Genesis's unique theological perspective",
        ("Romans", "salvation"): "Inscriptions from Corinth and Rome reveal the social dynamics and religious pluralism that shaped early Christian communities",
        ("Psalms", "worship and praise"): "Temple archaeology and ancient musical instruments illuminate the liturgical context of Israelite worship"
    }
    key = (book, theme)
    return insights.get(key, "Archaeological discoveries continue to illuminate the historical context of biblical texts")

def get_related_doctrine(theme):
    """Identify related systematic theology doctrines"""
    doctrines = {
        "salvation": "soteriology and the doctrine of salvation",
        "divine love": "theology proper and the doctrine of God",
        "kingdom of God": "eschatology and the doctrine of last things",
        "covenant": "theology of covenant and God's relational commitment"
    }
    return doctrines.get(theme, "fundamental Christian doctrine")

def get_contemporary_relevance(theme, concept):
    """Identify contemporary relevance and application"""
    relevance = {
        "salvation": "addressing questions of religious pluralism and the exclusivity of Christ",
        "divine love": "responding to cultural confusion about the nature of love and relationships",
        "kingdom of God": "providing hope in times of political and social upheaval",
        "faith and obedience": "challenging cultural relativism with objective truth claims"
    }
    return relevance.get(theme, "contemporary challenges facing the church and individual believers")

def get_cultural_background(book, verse_text):
    """Provide cultural background relevant to the verse"""
    backgrounds = {
        "Genesis": "ancient Near Eastern cosmology and patriarchal society",
        "Matthew": "first-century Palestinian Jewish culture under Roman occupation",
        "Romans": "Greco-Roman urban culture with diverse religious and philosophical influences",
        "Psalms": "ancient Israelite worship practices and court culture",
        "John": "late first-century Jewish-Christian tensions and Hellenistic thought"
    }
    return backgrounds.get(book, "the cultural context of the biblical world")

def get_socio_political_context(book):
    """Provide socio-political context for the book"""
    contexts = {
        "Genesis": "the tribal and clan-based society of the ancient Near East",
        "Matthew": "Roman imperial rule over Jewish Palestine with messianic expectations",
        "Romans": "the cosmopolitan capital of the Roman Empire with diverse populations",
        "Psalms": "the Israelite monarchy with its court politics and military conflicts",
        "Revelation": "imperial persecution under Domitian's demand for emperor worship"
    }
    return contexts.get(book, "the political and social structures of the biblical period")

def get_historical_audience_situation(book, chapter):
    """Describe the specific situation of the original audience"""
    situations = {
        "Genesis": "the foundational narrative for Israel's identity and relationship with God",
        "Matthew": "Jewish Christians seeking to understand Jesus as Messiah",
        "Romans": "a mixed congregation of Jewish and Gentile believers in the imperial capital",
        "Psalms": "worshipers in the temple and those seeking God in times of distress",
        "Revelation": "persecuted Christians in Asia Minor facing pressure to compromise"
    }
    return situations.get(book, "believers seeking to understand God's will and purposes")

def get_historical_parallel(book, concept):
    """Provide historical parallels that illuminate the concept"""
    parallels = {
        "salvation": "rescue narratives from ancient literature that would resonate with the audience",
        "kingdom": "imperial and royal imagery familiar to subjects of ancient monarchies",
        "covenant": "treaty language and adoption practices from the ancient world",
        "love": "patron-client relationships and family loyalty concepts"
    }
    return parallels.get(concept, "cultural practices and social structures that would have been familiar to the original readers")

def get_literary_historical_context(book):
    """Provide literary and historical context combined"""
    contexts = {
        "Genesis": "ancient Near Eastern narrative literature addressing origins and identity",
        "Matthew": "Jewish biographical literature presenting Jesus as the fulfillment of Scripture",
        "Romans": "Hellenistic epistolary literature with sophisticated theological argumentation",
        "Psalms": "ancient Near Eastern poetry and hymnic literature for worship",
        "Revelation": "Jewish apocalyptic literature using symbolic imagery to convey hope"
    }
    return contexts.get(book, "the literary conventions and historical circumstances of biblical literature")

def get_historical_theological_development(book, theme):
    """Describe how the theme developed historically within the book's context"""
    developments = {
        ("Genesis", "creation and providence"): "The development from creation to divine election established God's sovereign care over history",
        ("Romans", "salvation"): "Paul's systematic presentation built upon centuries of Jewish understanding about righteousness and divine justice",
        ("Psalms", "worship and praise"): "Israel's liturgical traditions developed through centuries of temple worship and personal devotion"
    }
    key = (book, theme)
    return developments.get(key, f"The historical development of {theme} within the theological tradition of {book}")

def get_ancient_worldview_context(book):
    """Provide ancient worldview context"""
    worldviews = {
        "Genesis": "a worldview where divine beings actively governed natural and historical processes",
        "Matthew": "a worldview expecting divine intervention through a promised Messiah",
        "Romans": "a worldview shaped by both Jewish monotheism and Greco-Roman philosophical thought",
        "Psalms": "a worldview centered on covenant relationship between God and His people"
    }
    return worldviews.get(book, "the ancient worldview that shaped the author's theological expression")

def get_biblical_theological_trajectory(theme):
    """Describe the biblical theological trajectory of the theme"""
    trajectories = {
        "salvation": "from physical deliverance in the Old Testament to spiritual redemption in the New",
        "kingdom of God": "from earthly theocracy through Davidic kingdom to eschatological fulfillment",
        "divine love": "from covenant faithfulness to sacrificial love demonstrated in Christ",
        "faith and obedience": "from law observance to faith in Christ as the means of righteousness"
    }
    return trajectories.get(theme, "the progressive revelation of God's purposes throughout Scripture")

def get_contemporary_theological_challenge(theme):
    """Identify contemporary theological challenges addressed by the theme"""
    challenges = {
        "salvation": "religious pluralism and questions about the necessity of Christ",
        "divine love": "the problem of evil and suffering in light of God's goodness",
        "kingdom of God": "the apparent delay of Christ's return and God's justice",
        "faith and obedience": "the relationship between faith and works in salvation"
    }
    return challenges.get(theme, "questions about God's character and purposes in the modern world")

def generate_chapter_overview(book, chapter, verses):
    """Generate an AI-powered overview of the entire chapter"""
    # Simulated chapter overview
    themes = [get_theme(v.text.lower()) for v in verses[:5]]  # Sample themes from the first few verses
    unique_themes = list(set(themes))[:3]  # Get up to 3 unique themes

    chapter_type = get_chapter_type(book, chapter)
    time_period = get_time_period(book)
    historical_context = get_historical_context(book)

    overview = f"""
    <p><strong>{book} {chapter}</strong> is a {chapter_type} chapter in the {get_testament_for_book(book)} that explores themes of {', '.join(unique_themes)}.
    Written during {time_period}, this chapter should be understood within its historical context: {historical_context}</p>

    <p>The chapter can be divided into several sections:</p>

    <ol>
        <li><strong>Verses 1-{min(5, len(verses))}</strong>: Introduction and setting the context</li>
        {'<li><strong>Verses 6-' + str(min(12, len(verses))) + '</strong>: Development of key themes</li>' if len(verses) > 5 else ''}
        {'<li><strong>Verses 13-' + str(min(20, len(verses))) + '</strong>: Central message and teachings</li>' if len(verses) > 12 else ''}
        {'<li><strong>Verses ' + str(min(21, len(verses))) + '-' + str(len(verses)) + '</strong>: Conclusion and application</li>' if len(verses) > 20 else ''}
    </ol>

    <p>This chapter is significant because it {get_chapter_significance(book, chapter)}.
    When studying this passage, it's important to consider both its immediate context within {book}
    and its broader place in the scriptural canon.</p>
    """

    return overview


def generate_cross_references(book, chapter, verse, verse_text):
    """Generate simulated cross-references for a verse"""
    # Dictionary of sample cross-references by theme
    theme_references = {
        "salvation": [
            {"book": "John", "chapter": 3, "verse": 16, "context": "God's love and salvation"},
            {"book": "Romans", "chapter": 10, "verse": 9, "context": "Confession and belief for salvation"},
            {"book": "Ephesians", "chapter": 2, "verse": 8, "context": "Salvation by grace through faith"}
        ],
        "faith": [
            {"book": "Hebrews", "chapter": 11, "verse": 1, "context": "Definition of faith"},
            {"book": "James", "chapter": 2, "verse": 17, "context": "Faith and works"},
            {"book": "Romans", "chapter": 1, "verse": 17, "context": "The righteous shall live by faith"}
        ],
        "love": [
            {"book": "1 Corinthians", "chapter": 13, "verse": 4, "context": "Characteristics of love"},
            {"book": "1 John", "chapter": 4, "verse": 8, "context": "God is love"},
            {"book": "John", "chapter": 15, "verse": 13, "context": "Greatest form of love"}
        ],
        "judgment": [
            {"book": "Matthew", "chapter": 25, "verse": 31, "context": "Final judgment"},
            {"book": "Romans", "chapter": 2, "verse": 1, "context": "Judging others"},
            {"book": "Revelation", "chapter": 20, "verse": 12, "context": "Judgment according to deeds"}
        ],
        "creation": [
            {"book": "Genesis", "chapter": 1, "verse": 1, "context": "Creation of heavens and earth"},
            {"book": "Psalm", "chapter": 19, "verse": 1, "context": "Heavens declare God's glory"},
            {"book": "Colossians", "chapter": 1, "verse": 16, "context": "All things created through Christ"}
        ]
    }

    # Identify themes in the verse text
    verse_themes = []
    for theme in theme_references.keys():
        if theme in verse_text or random.random() < 0.2:  # Randomly include some themes
            verse_themes.append(theme)

    # If no themes match, pick a random theme
    if not verse_themes:
        verse_themes = [random.choice(list(theme_references.keys()))]

    # Get references for identified themes
    references = []
    for theme in verse_themes[:2]:  # Limit to two themes
        theme_refs = theme_references[theme]
        for ref in random.sample(theme_refs, min(2, len(theme_refs))):
            # Skip self-references
            if ref["book"] == book and ref["chapter"] == chapter and ref["verse"] == verse:
                continue

            references.append({
                "text": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "url": f"/book/{ref['book']}/chapter/{ref['chapter']}#verse-{ref['verse']}",
                "context": ref["context"]
            })

    # Ensure we have at least one reference
    if not references:
        random_book = random.choice(["Matthew", "John", "Romans", "Psalms", "Proverbs"])
        references.append({
            "text": f"{random_book} 1:1",
            "url": f"/book/{random_book}/chapter/1#verse-1",
            "context": "Related teaching"
        })

    return references


def get_theme(text):
    """Extract a thematic element from text"""
    themes = [
        "redemption", "salvation", "faith", "obedience", "love",
        "judgment", "mercy", "grace", "wisdom", "creation",
        "covenant", "holiness", "righteousness", "truth", "hope",
        "sacrifice", "worship", "prayer", "discipleship", "fellowship"
    ]

    # First check if any themes appear directly in the text
    for theme in themes:
        if theme in text:
            return theme

    # Otherwise return a random theme
    return random.choice(themes)


def get_time_period(book):
    """Return the historical time period for a book"""
    time_periods = {
        # Torah
        "Genesis": "the patriarchal period (c. 2000-1700 BCE)",
        "Exodus": "the Egyptian bondage and wilderness wandering (c. 1446-1406 BCE)",
        "Leviticus": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Numbers": "Israel's wilderness period (c. 1446-1406 BCE)",
        "Deuteronomy": "the end of the wilderness wandering (c. 1406 BCE)",

        # Historical books
        "Joshua": "the conquest of Canaan (c. 1406-1375 BCE)",
        "Judges": "the pre-monarchic period (c. 1375-1050 BCE)",
        "Ruth": "the period of the Judges (c. 1100 BCE)",
        "1 Samuel": "the transition to monarchy (c. 1050-1010 BCE)",
        "2 Samuel": "David's reign (c. 1010-970 BCE)",
        "1 Kings": "Solomon's reign and the divided kingdom (c. 970-853 BCE)",
        "2 Kings": "the divided and exilic periods (c. 853-560 BCE)",
        "1 Chronicles": "the post-exilic reflection on David's reign (c. 430-400 BCE)",
        "2 Chronicles": "the post-exilic reflection on the monarchy (c. 430-400 BCE)",
        "Ezra": "the post-exilic return (c. 458-440 BCE)",
        "Nehemiah": "the rebuilding of Jerusalem (c. 445-420 BCE)",
        "Esther": "the Persian period (c. 483-473 BCE)",

        # Wisdom literature
        "Job": "the patriarchal period (literary composition later)",
        "Psalms": "various periods (c. 1000-400 BCE)",
        "Proverbs": "primarily Solomon's reign (c. 970-930 BCE)",
        "Ecclesiastes": "likely Solomon's reign (c. 970-930 BCE)",
        "Song of Solomon": "Solomon's reign (c. 970-930 BCE)",

        # Major Prophets
        "Isaiah": "the Assyrian and pre-exilic periods (c. 740-680 BCE)",
        "Jeremiah": "the final years of Judah and early exile (c. 627-580 BCE)",
        "Lamentations": "just after Jerusalem's fall (c. 586 BCE)",
        "Ezekiel": "the Babylonian exile (c. 593-570 BCE)",
        "Daniel": "the Babylonian and Persian periods (c. 605-530 BCE)",

        # Minor Prophets
        "Hosea": "the final years of the northern kingdom (c. 755-710 BCE)",
        "Joel": "possibly post-exilic period (uncertain date)",
        "Amos": "the prosperous period of Jeroboam II (c. 760-750 BCE)",
        "Obadiah": "possibly after Jerusalem's fall (c. 586 BCE)",
        "Jonah": "the Assyrian period (c. 780-750 BCE)",
        "Micah": "the late 8th century BCE (c. 735-700 BCE)",
        "Nahum": "shortly before Nineveh's fall (c. 630-610 BCE)",
        "Habakkuk": "the neo-Babylonian rise to power (c. 605-597 BCE)",
        "Zephaniah": "during Josiah's reign (c. 640-609 BCE)",
        "Haggai": "the early post-exilic period (c. 520 BCE)",
        "Zechariah": "the early post-exilic period (c. 520-480 BCE)",
        "Malachi": "the mid-5th century BCE (c. 460-430 BCE)",

        # Gospels and Acts
        "Matthew": "the late first century CE (c. 80-90 CE)",
        "Mark": "the mid first century CE (c. 65-70 CE)",
        "Luke": "the late first century CE (c. 80-85 CE)",
        "John": "the late first century CE (c. 90-95 CE)",
        "Acts": "the late first century CE (c. 80-85 CE)",

        # Pauline Epistles
        "Romans": "Paul's third missionary journey (c. 57 CE)",
        "1 Corinthians": "Paul's third missionary journey (c. 55 CE)",
        "2 Corinthians": "Paul's third missionary journey (c. 55-56 CE)",
        "Galatians": "either before or after the Jerusalem Council (c. 48-55 CE)",
        "Ephesians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Philippians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Colossians": "Paul's Roman imprisonment (c. 60-62 CE)",
        "1 Thessalonians": "Paul's second missionary journey (c. 50-51 CE)",
        "2 Thessalonians": "shortly after 1 Thessalonians (c. 50-51 CE)",
        "1 Timothy": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "2 Timothy": "during Paul's second Roman imprisonment (c. 66-67 CE)",
        "Titus": "after Paul's first Roman imprisonment (c. 62-64 CE)",
        "Philemon": "Paul's Roman imprisonment (c. 60-62 CE)",
        "Hebrews": "before Jerusalem's destruction (c. 60-70 CE)",

        # General Epistles
        "James": "the early church period (c. 45-50 CE)",
        "1 Peter": "during Nero's persecution (c. 62-64 CE)",
        "2 Peter": "shortly before Peter's death (c. 65-68 CE)",
        "1 John": "the late first century CE (c. 85-95 CE)",
        "2 John": "the late first century CE (c. 85-95 CE)",
        "3 John": "the late first century CE (c. 85-95 CE)",
        "Jude": "the late first century CE (c. 65-80 CE)",

        # Apocalyptic
        "Revelation": "the end of the first century CE (c. 95 CE)"
    }

    return time_periods.get(book, "the biblical period")


def get_historical_context(book):
    """Return historical context for a book"""
    historical_contexts = {
        # Torah
        "Genesis": "The ancient Near Eastern world was filled with competing creation narratives and flood stories.",
        "Exodus": "Egypt was the dominant superpower with a complex polytheistic religion and a god-king pharaoh.",
        "Leviticus": "The ritual systems addressed were designed to distinguish Israel from surrounding Canaanite practices.",
        "Numbers": "The wilderness journey occurred between Egypt's dominance and the Canaanite tribal systems.",
        "Deuteronomy": "Moses delivered these speeches as Israel prepared to enter a land filled with different Canaanite city-states.",

        # Historical books
        "Joshua": "Canaan was fragmented into city-states with various tribal alliances and religious practices.",
        "Judges": "Without central leadership, Israel faced constant threats from surrounding peoples like the Philistines and Midianites.",
        "Ruth": "During the tribal confederacy period, local customs and family laws were paramount for survival.",
        "1 Samuel": "Israel transitioned from tribal confederacy to monarchy while facing Philistine military pressure.",
        "2 Samuel": "David established Jerusalem as the capital during a time of regional power vacuum.",
        "1 Kings": "Solomon's reign represented Israel's golden age, with international trade and diplomatic relations.",
        "2 Kings": "The divided kingdoms faced threats from rising empires: Assyria and later Babylon.",
        "1 Chronicles": "Written after exile to reestablish national identity through connection to David's lineage.",
        "2 Chronicles": "Written to remind returning exiles of their temple-centered worship and Davidic heritage.",
        "Ezra": "The Persian Empire allowed religious freedom while maintaining political control.",
        "Nehemiah": "Persian authorities permitted Jerusalem's rebuilding under local leadership with imperial oversight.",
        "Esther": "Jews in diaspora faced both integration opportunities and threats within the vast Persian Empire.",

        # Wisdom literature
        "Job": "Ancient wisdom traditions often wrestled with the problem of suffering and divine justice.",
        "Psalms": "Temple worship utilized these compositions across various periods of Israel's history.",
        "Proverbs": "Ancient Near Eastern wisdom literature was common in royal courts for training officials.",
        "Ecclesiastes": "Royal wisdom reflections paralleled other ancient Near Eastern philosophical works.",
        "Song of Solomon": "Ancient Near Eastern love poetry often used agricultural and royal imagery.",

        # Major Prophets
        "Isaiah": "Addressed Judah during Assyria's rise, Babylon's threat, and anticipated restoration.",
        "Jeremiah": "Prophesied during Judah's final years as Babylon became the dominant power.",
        "Lamentations": "Written amid the devastating aftermath of Jerusalem's destruction by Babylon.",
        "Ezekiel": "Ministered to exiles in Babylon with visions of God's glory and future restoration.",
        "Daniel": "Demonstrates faithful living under foreign rule during the Babylonian and Persian empires.",

        # Minor Prophets
        "Hosea": "Israel faced imminent threat from Assyria while engaging in Canaanite religious syncretism.",
        "Joel": "Addressed a community devastated by natural disaster as a sign of divine judgment.",
        "Amos": "Economic prosperity masked serious social injustice and religious hypocrisy.",
        "Obadiah": "Edom's betrayal of Judah during Jerusalem's fall heightened ancient tribal hostilities.",
        "Jonah": "Nineveh was the capital of the feared Assyrian Empire, Israel's enemy.",
        "Micah": "Rural communities suffered while urban elites prospered during Assyria's regional dominance.",
        "Nahum": "Nineveh's anticipated fall would end a century of Assyrian oppression.",
        "Habakkuk": "Babylon's rise to power raised questions about God using pagan nations as instruments.",
        "Zephaniah": "Josiah's reforms occurred against the backdrop of Assyria's decline and Babylon's rise.",
        "Haggai": "Economic hardship and political uncertainty complicated the returning exiles' rebuilding efforts.",
        "Zechariah": "Persian support for temple rebuilding came with continued imperial control.",
        "Malachi": "Post-exilic community struggled with religious apathy and intermarriage challenges.",

        # Gospels and Acts
        "Matthew": "Written when Christianity was separating from Judaism following Jerusalem's destruction.",
        "Mark": "Composed during or just after Nero's persecution when eyewitnesses were disappearing.",
        "Luke": "Written when Christians needed to understand their place in the Roman world.",
        "John": "Addressed late first-century challenges from both Judaism and emerging Gnostic thought.",
        "Acts": "Chronicles Christianity's spread across the Roman Empire despite official and unofficial opposition.",

        # Pauline Epistles
        "Romans": "Christians in Rome navigated tensions between Jewish and Gentile believers under imperial watch.",
        "1 Corinthians": "The church existed in a prosperous, cosmopolitan, morally permissive Roman colony.",
        "2 Corinthians": "Paul defended his apostleship against challenges in a culture valuing rhetorical prowess.",
        "Galatians": "Gentile believers faced pressure to adopt Jewish practices for full acceptance.",
        "Ephesians": "Ephesus was a major center of pagan worship, particularly of the goddess Artemis.",
        "Philippians": "The church in this Roman colony maintained partnership with Paul despite his imprisonment.",
        "Colossians": "Syncretistic philosophy threatened to compromise the sufficiency of Christ.",
        "1 Thessalonians": "New believers faced persecution from both Jewish opposition and pagan neighbors.",
        "2 Thessalonians": "Confusion about Christ's return caused some believers to abandon daily responsibilities.",
        "1 Timothy": "False teaching in Ephesus required organizational and doctrinal clarification.",
        "2 Timothy": "Paul's final imprisonment occurred during intensified persecution under Nero.",
        "Titus": "Cretan culture's negative reputation required special attention to Christian character.",
        "Philemon": "Roman slavery was addressed through Christian principles without direct confrontation.",
        "Hebrews": "Jewish Christians faced persecution pressure to return to Judaism's legal protections.",

        # General Epistles
        "James": "Early Jewish believers struggled to live out faith amid economic hardship and discrimination.",
        "1 Peter": "Christians throughout Asia Minor faced growing social hostility and potential persecution.",
        "2 Peter": "False teachers exploited Christian freedom for immoral purposes and denied divine judgment.",
        "1 John": "Early Gnostic ideas threatened the understanding of Christ's incarnation and redemption.",
        "2 John": "Itinerant teachers required careful vetting as false teaching spread through hospitality networks.",
        "3 John": "Power struggles in local churches complicated missionary support and fellowship.",
        "Jude": "Libertine teaching undermined moral standards by distorting grace.",

        # Apocalyptic
        "Revelation": "Emperor worship intensified under Domitian, pressuring Christians to compromise their exclusive loyalty to Christ."
    }

    return historical_contexts.get(book, "This text emerged within the historical context of ancient religious traditions.")


# Literary genre per book, used by get_book_genre() (label form).
BOOK_GENRE = {
    # Torah
    "Genesis": "Narrative with genealogy",
    "Exodus": "Narrative with law",
    "Leviticus": "Law and ritual instruction",
    "Numbers": "Narrative with law and census",
    "Deuteronomy": "Sermonic law",

    # Historical books
    "Joshua": "Historical narrative",
    "Judges": "Cyclical historical narrative",
    "Ruth": "Historical narrative",
    "1 Samuel": "Historical narrative",
    "2 Samuel": "Historical narrative",
    "1 Kings": "Historical narrative",
    "2 Kings": "Historical narrative",
    "1 Chronicles": "Historical narrative with genealogy",
    "2 Chronicles": "Historical narrative",
    "Ezra": "Historical narrative",
    "Nehemiah": "Historical narrative with memoir",
    "Esther": "Historical narrative",

    # Wisdom literature
    "Job": "Wisdom literature with poetic dialogue",
    "Psalms": "Poetry and liturgy",
    "Proverbs": "Wisdom literature",
    "Ecclesiastes": "Wisdom literature with philosophical reflection",
    "Song of Solomon": "Poetry and love song",

    # Major Prophets
    "Isaiah": "Prophetic literature with poetry",
    "Jeremiah": "Prophetic literature with biography",
    "Lamentations": "Poetic lament",
    "Ezekiel": "Prophetic literature with apocalyptic elements",
    "Daniel": "Narrative with apocalyptic visions",

    # Minor Prophets
    "Hosea": "Prophetic literature",
    "Joel": "Prophetic literature",
    "Amos": "Prophetic literature",
    "Obadiah": "Prophetic literature",
    "Jonah": "Prophetic narrative",
    "Micah": "Prophetic literature",
    "Nahum": "Prophetic literature",
    "Habakkuk": "Prophetic literature with dialogue",
    "Zephaniah": "Prophetic literature",
    "Haggai": "Prophetic literature",
    "Zechariah": "Prophetic literature with apocalyptic visions",
    "Malachi": "Prophetic literature with disputation",

    # Gospels
    "Matthew": "Gospel narrative",
    "Mark": "Gospel narrative",
    "Luke": "Gospel narrative with historiography",
    "John": "Gospel narrative with theology",

    # Acts
    "Acts": "Historical narrative",

    # Pauline Epistles
    "Romans": "Epistle with systematic theology",
    "1 Corinthians": "Epistle",
    "2 Corinthians": "Epistle",
    "Galatians": "Epistle",
    "Ephesians": "Epistle",
    "Philippians": "Epistle",
    "Colossians": "Epistle",
    "1 Thessalonians": "Epistle",
    "2 Thessalonians": "Epistle",
    "1 Timothy": "Pastoral epistle",
    "2 Timothy": "Pastoral epistle",
    "Titus": "Pastoral epistle",
    "Philemon": "Personal epistle",
    "Hebrews": "Epistle with sermonic elements",

    # General Epistles
    "James": "Epistle with wisdom elements",
    "1 Peter": "Epistle",
    "2 Peter": "Epistle",
    "1 John": "Epistle with theological discourse",
    "2 John": "Brief epistle",
    "3 John": "Brief epistle",
    "Jude": "Epistle",

    # Apocalyptic
    "Revelation": "Apocalyptic literature with epistle elements"
}


def get_chapter_type(book, chapter):
    """Identify the type of chapter"""

    # Simplified mapping of books to primary genre
    book_genres = {
        # Torah
        "Genesis": "narrative",
        "Exodus": "narrative with legal sections",
        "Leviticus": "legal and ritual",
        "Numbers": "mixed narrative and legal",
        "Deuteronomy": "sermonic and legal",

        # Historical
        "Joshua": "historical narrative",
        "Judges": "cyclical narrative",
        "Ruth": "historical narrative",
        "1 Samuel": "biographical narrative",
        "2 Samuel": "biographical narrative",
        "1 Kings": "historical narrative",
        "2 Kings": "historical narrative",
        "1 Chronicles": "historical and genealogical",
        "2 Chronicles": "historical narrative",
        "Ezra": "historical narrative",
        "Nehemiah": "historical memoir",
        "Esther": "historical narrative",

        # Wisdom
        "Job": "wisdom dialogue",
        "Psalms": "poetic and liturgical",
        "Proverbs": "wisdom sayings",
        "Ecclesiastes": "philosophical reflection",
        "Song of Solomon": "poetic love song",

        # Prophetic
        "Isaiah": "prophetic oracle",
        "Jeremiah": "prophetic oracle",
        "Lamentations": "funeral dirge",
        "Ezekiel": "prophetic vision",
        "Daniel": "apocalyptic and narrative",
        "Hosea": "prophetic oracle",
        "Joel": "prophetic oracle",
        "Amos": "prophetic oracle",
        "Obadiah": "prophetic oracle",
        "Jonah": "prophetic narrative",
        "Micah": "prophetic oracle",
        "Nahum": "prophetic oracle",
        "Habakkuk": "prophetic dialogue",
        "Zephaniah": "prophetic oracle",
        "Haggai": "prophetic oracle",
        "Zechariah": "prophetic vision",
        "Malachi": "prophetic disputation",

        # Gospels
        "Matthew": "biographical gospel",
        "Mark": "action-oriented gospel",
        "Luke": "historical gospel",
        "John": "theological gospel",

        # Acts
        "Acts": "historical narrative",

        # Epistles
        "Romans": "theological epistle",
        "1 Corinthians": "pastoral epistle",
        "2 Corinthians": "apologetic epistle",
        "Galatians": "polemical epistle",
        "Ephesians": "theological epistle",
        "Philippians": "friendship epistle",
        "Colossians": "christological epistle",
        "1 Thessalonians": "eschatological epistle",
        "2 Thessalonians": "eschatological epistle",
        "1 Timothy": "pastoral epistle",
        "2 Timothy": "pastoral epistle",
        "Titus": "pastoral epistle",
        "Philemon": "personal epistle",
        "Hebrews": "homiletical epistle",
        "James": "wisdom epistle",
        "1 Peter": "pastoral epistle",
        "2 Peter": "polemical epistle",
        "1 John": "theological epistle",
        "2 John": "pastoral epistle",
        "3 John": "personal epistle",
        "Jude": "polemical epistle",

        # Apocalyptic
        "Revelation": "apocalyptic vision"
    }

    # Special cases for specific chapters
    special_chapters = {
        ("Genesis", 1): "creation account",
        ("Genesis", 3): "fall narrative",
        ("Exodus", 20): "legal covenant",
        ("Leviticus", 16): "ritual instruction",
        ("Deuteronomy", 28): "covenant blessing and curse",
        ("Joshua", 1): "commissioning narrative",
        ("Judges", 2): "paradigmatic narrative",
        ("1 Samuel", 16): "anointing narrative",
        ("2 Samuel", 7): "covenant narrative",
        ("Psalms", 1): "wisdom psalm",
        ("Psalms", 22): "lament psalm",
        ("Psalms", 23): "trust psalm",
        ("Isaiah", 53): "suffering servant oracle",
        ("Matthew", 5): "ethical teaching",
        ("John", 1): "theological prologue",
        ("Romans", 8): "theological exposition",
        ("1 Corinthians", 13): "hymn to love",
        ("Revelation", 1): "apocalyptic vision"
    }

    # Check if this is a special chapter
    if (book, chapter) in special_chapters:
        return special_chapters[(book, chapter)]

    # Otherwise return the general book genre
    return book_genres.get(book, "scriptural")


def get_testament_for_book(book):
    """Determine if a book is in the Old or New Testament"""
    return "Old Testament" if is_old_testament(book) else "New Testament"


def generate_literary_features(book, genre):
    """Generate commentary on literary features of a book"""

    # Default features based on genre
    if "narrative" in genre.lower():
        return f"""
        <p>{book} employs narrative techniques characteristic of biblical historiography. The book uses plot development, characterization, dialogue, and setting to convey both historical events and theological meaning. Narratives in {book} are carefully structured to highlight divine providence and human response.</p>

        <h3>Structure</h3>
        <p>The narrative structure of {book} involves a clear progression with rising and falling action, climactic moments, and resolution. The author selectively includes details that advance the theological purpose while maintaining historical accuracy.</p>

        <h3>Literary Devices</h3>
        <p>Common literary devices in {book} include:</p>
        <ul>
            <li><strong>Repetition</strong> - Key phrases and motifs recur to emphasize important themes</li>
            <li><strong>Type-scenes</strong> - Conventional scenarios (e.g., encounters at wells, divine calls) that evoke specific expectations</li>
            <li><strong>Inclusio</strong> - Framing sections with similar language to create literary units</li>
            <li><strong>Chiasm</strong> - Mirror-image structures that highlight central elements</li>
        </ul>

        <p>These narrative techniques guide the reader's interpretation and highlight theological significance within historical events.</p>
        """
    elif "epistle" in genre.lower():
        return f"""
        <p>{book} follows the conventions of ancient letter-writing while adapting them for theological instruction. The epistle combines formal elements of Greco-Roman correspondence with Jewish expository methods to communicate Christian teaching.</p>

        <h3>Structure</h3>
        <p>The epistle follows a typical pattern including:</p>
        <ul>
            <li><strong>Opening</strong> - Sender, recipients, and greeting (often theologically expanded)</li>
            <li><strong>Thanksgiving/Prayer</strong> - Expressing gratitude and/or intercession for recipients</li>
            <li><strong>Body</strong> - Doctrinal exposition followed by practical application</li>
            <li><strong>Closing</strong> - Final exhortations, greetings, and benediction</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>The epistle employs various rhetorical techniques including:</p>
        <ul>
            <li><strong>Diatribe</strong> - Dialogue with imaginary opponent through questions and answers</li>
            <li><strong>Paraenesis</strong> - Moral exhortation often through contrasting vices and virtues</li>
            <li><strong>Examples</strong> - Drawing on biblical figures or contemporary situations as models</li>
            <li><strong>Metaphors</strong> - Extended comparisons that illustrate theological concepts</li>
        </ul>

        <p>These epistolary features reflect both Greco-Roman rhetorical education and Jewish interpretive traditions adapted for Christian purposes.</p>
        """
    elif "wisdom" in genre.lower() or "poetry" in genre.lower():
        return f"""
        <p>{book} exemplifies biblical wisdom literature and poetic expression. The book uses carefully crafted language, figurative speech, and structural patterns to convey insights about divine order and human experience.</p>

        <h3>Poetic Structure</h3>
        <p>The poetry in {book} primarily employs parallelism, where successive lines relate to each other in various ways:</p>
        <ul>
            <li><strong>Synonymous parallelism</strong> - Second line restates the first with similar meaning</li>
            <li><strong>Antithetic parallelism</strong> - Second line contrasts with the first</li>
            <li><strong>Synthetic parallelism</strong> - Second line develops or completes the first</li>
            <li><strong>Emblematic parallelism</strong> - One line uses a metaphor to illustrate the other</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>{book} employs numerous literary techniques including:</p>
        <ul>
            <li><strong>Imagery</strong> - Vivid sensory language drawing on nature, daily life, and cultural practices</li>
            <li><strong>Metaphor and simile</strong> - Comparisons that illuminate abstract concepts</li>
            <li><strong>Acrostic patterns</strong> - Alphabetical arrangements that structure content</li>
            <li><strong>Personification</strong> - Abstract qualities given human attributes (particularly wisdom)</li>
        </ul>

        <p>These poetic features create aesthetic beauty while making the wisdom more memorable and impactful.</p>
        """
    elif "prophetic" in genre.lower():
        return f"""
        <p>{book} employs the distinctive literary forms of biblical prophecy. The book combines poetic expression, symbolic actions, and visionary experiences to communicate divine messages with both immediate and future significance.</p>

        <h3>Prophetic Forms</h3>
        <p>{book} includes various prophetic forms:</p>
        <ul>
            <li><strong>Oracle</strong> - Divine speech introduced by "Thus says the LORD" or similar formula</li>
            <li><strong>Woe oracle</strong> - Judgment pronouncement beginning with "Woe to..."</li>
            <li><strong>Lawsuit</strong> - Covenant litigation using legal metaphors with witnesses, evidence, and verdict</li>
            <li><strong>Vision report</strong> - Account of prophetic visions with interpretation</li>
            <li><strong>Symbolic action</strong> - Prophetic performance conveying message visually</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>Prophetic literature in {book} employs various techniques:</p>
        <ul>
            <li><strong>Metaphor and simile</strong> - Comparing Israel to unfaithful spouse, vineyard, etc.</li>
            <li><strong>Hyperbole</strong> - Deliberate exaggeration for rhetorical effect</li>
            <li><strong>Merism</strong> - Expressing totality through contrasting pairs</li>
            <li><strong>Wordplay</strong> - Puns and sound associations (particularly in Hebrew)</li>
        </ul>

        <p>These prophetic literary features combine aesthetic power with rhetorical force to call for response to divine revelation.</p>
        """
    elif "apocalyptic" in genre.lower():
        return f"""
        <p>{book} exemplifies apocalyptic literature with its distinctive symbolic imagery and visionary framework. The book uses heavily symbolic language, cosmic dualism, and revelatory encounters to unveil spiritual realities and future events.</p>

        <h3>Apocalyptic Features</h3>
        <p>Key characteristics of {book} as apocalyptic literature include:</p>
        <ul>
            <li><strong>Symbolic visions</strong> - Elaborate imagery requiring interpretation</li>
            <li><strong>Heavenly mediators</strong> - Angels explaining visions to the recipient</li>
            <li><strong>Cosmic dualism</strong> - Sharp contrast between good/evil, present age/age to come</li>
            <li><strong>Deterministic view</strong> - History moving toward predetermined divine conclusion</li>
            <li><strong>Pseudonymity</strong> - Attribution to ancient figure (in non-canonical apocalypses)</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>Apocalyptic literature in {book} employs various techniques:</p>
        <ul>
            <li><strong>Symbolism</strong> - Numbers, colors, and animals representing spiritual realities</li>
            <li><strong>Mythic imagery</strong> - Drawing on cosmic battle motifs and ancient Near Eastern symbols</li>
            <li><strong>Recapitulation</strong> - Same events described from different perspectives</li>
            <li><strong>Intercalation</strong> - Interrupting one sequence with another for theological purposes</li>
        </ul>

        <p>These apocalyptic features enable the communication of transcendent realities that defy literal description and provide hope in times of crisis.</p>
        """
    elif "gospel" in genre.lower():
        return f"""
        <p>{book} represents the distinctive gospel genre—a theological biography focusing on Jesus' life, teaching, death, and resurrection. The book combines narrative elements, discourse material, and passion account to proclaim Jesus' identity and significance.</p>

        <h3>Structure</h3>
        <p>{book} organizes its material with theological purpose, including:</p>
        <ul>
            <li><strong>Prologue</strong> - Introducing theological themes and Jesus' identity</li>
            <li><strong>Ministry narrative</strong> - Accounts of teachings, miracles, and encounters</li>
            <li><strong>Discourse sections</strong> - Extended teaching blocks on various themes</li>
            <li><strong>Passion narrative</strong> - Detailed account of Jesus' final days, death, and resurrection</li>
        </ul>

        <h3>Literary Devices</h3>
        <p>The gospel employs various techniques including:</p>
        <ul>
            <li><strong>Inclusio</strong> - Framing devices marking literary units</li>
            <li><strong>Chiasm</strong> - Mirror structures highlighting central elements</li>
            <li><strong>Typology</strong> - Presenting Jesus as fulfilling Old Testament patterns</li>
            <li><strong>Irony</strong> - Contrasts between appearance and reality, human and divine perspectives</li>
            <li><strong>Parables</strong> - Figurative stories conveying kingdom truths</li>
        </ul>

        <p>These gospel features combine to present Jesus Christ as the fulfillment of God's promises and the decisive revelation of God's salvation.</p>
        """
    else:
        return f"""
        <p>{book} employs various literary techniques and structural elements to communicate its message effectively. The book's form serves its function, using appropriate conventions to convey its theological content.</p>

        <h3>Structure</h3>
        <p>The book demonstrates intentional organization, with distinct sections addressing different aspects of its theme. Transitions between sections are marked by shifts in topic, audience, or literary form.</p>

        <h3>Literary Devices</h3>
        <p>The book employs various literary techniques including:</p>
        <ul>
            <li><strong>Imagery</strong> - Concrete pictures that convey abstract concepts</li>
            <li><strong>Repetition</strong> - Key terms and phrases that emphasize important themes</li>
            <li><strong>Contrast</strong> - Opposing concepts to highlight distinctions</li>
            <li><strong>Figurative language</strong> - Metaphors and similes that illuminate meaning</li>
        </ul>

        <p>These literary features enhance the book's communicative power and contribute to its enduring significance in the biblical canon.</p>
        """


def generate_book_themes(book):
    """Generate themes for a book"""

    # Book-specific themes - abbreviated versions, expand as needed
    themes = {
        "Genesis": """
        <p>Genesis establishes the foundational theological themes that undergird the entire biblical narrative:</p>

        <h3>Divine Sovereignty and Creative Order</h3>
        <p>Genesis opens with the most profound theological statement in Scripture: "In the beginning God created the heavens and the earth" (1:1). This declaration establishes God's absolute sovereignty over all reality. The creation account reveals God's transcendence, immanence, and wisdom in creating with purpose and design.</p>

        <h3>The Imago Dei and Human Dignity</h3>
        <p>The creation of humanity "in the image of God" (1:26-27) represents one of Scripture's most profound anthropological statements. This divine image distinguishes humans from all other creatures, conferring unique dignity and capacity for relationship with the divine.</p>

        <h3>The Fall and Total Depravity</h3>
        <p>Genesis 3 records the catastrophic entrance of sin into God's perfect creation. The progression of sin from Genesis 3 through 11 demonstrates sin's exponential expansion. Yet even in judgment, divine grace appears through promised redemption (3:15).</p>

        <h3>Covenant Theology and Redemptive Promise</h3>
        <p>Genesis introduces the fundamental covenant structure governing God's relationship with humanity. The Abrahamic covenant (Genesis 12, 15, 17, 22) forms the foundational charter for God's redemptive work.</p>
        """,

        "Exodus": """
        <p>Exodus develops several major theological themes that shape the biblical narrative:</p>

        <h3>Divine Deliverance</h3>
        <p>The exodus event establishes God as the deliverer who sees affliction, hears cries, and acts powerfully to save. This deliverance comes through both supernatural intervention and human agency, establishing a pattern where God works through human instruments while maintaining divine sovereignty.</p>

        <h3>Covenant Relationship</h3>
        <p>Exodus transforms God's covenant with the patriarchs into a formalized national covenant at Sinai. This covenant establishes Israel's special status as God's "treasured possession," "kingdom of priests," and "holy nation" (Exodus 19:5-6).</p>

        <h3>Divine Revelation</h3>
        <p>Throughout Exodus, God progressively reveals Himself through words and actions. The revelation culminates in the giving of the law and the tabernacle instructions.</p>

        <h3>Divine Presence</h3>
        <p>The tabernacle establishment addresses how a holy God can dwell among an unholy people. The book concludes with God's glory filling the tabernacle, confirming His presence among Israel.</p>
        """,

        "Revelation": """
        <p>Revelation develops several major themes that bring the biblical narrative to its climactic conclusion:</p>

        <h3>Divine Sovereignty</h3>
        <p>God's absolute sovereignty over history and creation stands as the book's foundation. Despite apparent chaos and the temporary triumph of evil, the heavenly throne room scenes establish that God remains in control.</p>

        <h3>Christ's Identity and Victory</h3>
        <p>Revelation presents Christ as the glorified Lord, the slaughtered but victorious Lamb, and the conquering King. The paradoxical image of the slain Lamb who conquers is particularly significant.</p>

        <h3>Faithful Witness Amid Persecution</h3>
        <p>The call to faithful endurance despite suffering runs throughout the book. Martyrdom is presented not as defeat but as victory following Christ's pattern.</p>

        <h3>New Creation</h3>
        <p>The climactic vision of new heavens and earth completes the biblical narrative begun in Genesis, emphasizing the comprehensive scope of redemption.</p>
        """
    }

    # Default themes based on testament and genre
    if book not in themes:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        if testament == "Old Testament":
            if "narrative" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Providence</h3>
                <p>God sovereignly works through historical circumstances and human decisions to accomplish His purposes.</p>

                <h3>Covenant Fidelity</h3>
                <p>The book traces God's faithfulness to His covenant promises despite human failings.</p>

                <h3>Leadership and Authority</h3>
                <p>Various leaders demonstrate both positive and negative examples of exercising authority.</p>

                <h3>Obedience and Blessing</h3>
                <p>The narrative demonstrates connections between faithfulness to God's commands and experiencing His blessing.</p>
                """
            elif "prophetic" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Judgment</h3>
                <p>God's righteous response to persistent sin demonstrates His holiness and justice.</p>

                <h3>Repentance and Restoration</h3>
                <p>God's judgment aims at restoration, with calls to return to covenant faithfulness.</p>

                <h3>The Day of the LORD</h3>
                <p>The prophetic anticipation of divine intervention brings both judgment and vindication.</p>

                <h3>Messianic Hope</h3>
                <p>Promises of a coming deliverer point toward God's ultimate solution to human sin.</p>
                """
            else:
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Divine Revelation</h3>
                <p>God communicates His character, will, and purposes through various means.</p>

                <h3>Covenant Relationship</h3>
                <p>The formal relationship between God and His people establishes mutual commitments.</p>

                <h3>Human Responsibility</h3>
                <p>People are accountable for their response to divine revelation.</p>

                <h3>Divine Faithfulness</h3>
                <p>Despite human failures, God remains faithful to His promises and purposes.</p>
                """
        else:  # New Testament
            if "gospel" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus is presented as Son of God, Son of Man, Messiah, Savior, and Lord.</p>

                <h3>Kingdom of God</h3>
                <p>Jesus' proclamation and demonstration of God's reign reveals both its present reality and future consummation.</p>

                <h3>Discipleship</h3>
                <p>Following Jesus requires transformed values, priorities, and relationships.</p>

                <h3>Fulfillment</h3>
                <p>Jesus fulfills Old Testament prophecies, patterns, and promises.</p>
                """
            elif "epistle" in genre.lower():
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus Christ's person and work form the foundation for Christian faith and practice.</p>

                <h3>Soteriology</h3>
                <p>Salvation through Christ involves justification, reconciliation, redemption, and sanctification.</p>

                <h3>Ecclesiology</h3>
                <p>The church as Christ's body has both unity and diversity.</p>

                <h3>Ethics</h3>
                <p>Christian behavior flows from gospel transformation rather than mere rule-keeping.</p>
                """
            else:
                return """
                <p>The book develops several significant theological themes:</p>

                <h3>Christology</h3>
                <p>Jesus Christ's identity and work form the center of Christian faith.</p>

                <h3>Soteriology</h3>
                <p>Salvation through Christ transforms believers' standing before God.</p>

                <h3>Ecclesiology</h3>
                <p>The church has a distinct identity and mission in the world.</p>

                <h3>Eschatology</h3>
                <p>God's future promises provide hope and shape present priorities.</p>
                """

    return themes.get(book, """
        <p>The book develops several significant theological themes:</p>

        <h3>Divine Revelation</h3>
        <p>God communicates His character, will, and purposes through various means.</p>

        <h3>Covenant Relationship</h3>
        <p>The formal relationship between God and His people establishes mutual commitments.</p>

        <h3>Human Responsibility</h3>
        <p>People are accountable for their response to divine revelation.</p>

        <h3>Divine Faithfulness</h3>
        <p>Despite human failures, God remains faithful to His promises and purposes.</p>
        """)


def generate_theological_significance(book):
    """Generate theological significance for a book"""

    # Book-specific theological significance - abbreviated versions
    theological = {
        "Genesis": """
        <p>Genesis establishes the foundational theological architecture for understanding God's character and redemptive purposes:</p>

        <h3>Doctrine of God</h3>
        <p>Genesis reveals the one true God as utterly distinct from polytheistic deities. God appears as self-existent, transcendent yet immanent, omnipotent, omniscient, omnipresent, and immutable.</p>

        <h3>Doctrine of Humanity</h3>
        <p>The creation of humanity in God's image establishes fundamental theological anthropology. The divine image encompasses rational, moral, spiritual, creative, and relational dimensions.</p>

        <h3>Doctrine of Sin</h3>
        <p>Genesis 3 provides the biblical account of sin's entry into creation, establishing the framework for understanding human moral corruption.</p>

        <h3>Doctrine of Salvation</h3>
        <p>Genesis 3:15 introduces the protoevangelium ("first gospel"), promising that the woman's offspring will defeat the serpent. This establishes the pattern of redemption through suffering.</p>
        """,

        "Exodus": """
        <p>Exodus develops several foundational theological concepts:</p>

        <h3>Doctrine of God</h3>
        <p>Exodus significantly advances biblical revelation about God's nature. Through His self-disclosure as "I AM WHO I AM" (Exodus 3:14), God reveals His self-existence and covenant faithfulness.</p>

        <h3>Doctrine of Salvation</h3>
        <p>The exodus event establishes the paradigm for understanding salvation throughout Scripture. The Passover introduces substitutionary atonement concepts later fulfilled in Christ.</p>

        <h3>Doctrine of Covenant</h3>
        <p>Exodus develops the covenant concept, now expanded to include an entire nation. This establishes Israel's unique relationship with God as a "kingdom of priests."</p>

        <h3>Doctrine of Worship</h3>
        <p>The tabernacle instructions establish principles for appropriate worship, including divine prescription, centrality of sacrifice, and priestly mediation.</p>
        """
    }

    # Generate generic theological significance if specific content isn't available
    if book not in theological:
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            return f"""
            <p>{book} contributes significantly to biblical theology in several areas:</p>

            <h3>Understanding of God</h3>
            <p>The book reveals aspects of God's character and ways of working in history.</p>

            <h3>Covenant Relationship</h3>
            <p>The book develops aspects of God's covenant relationship with Israel.</p>

            <h3>Ethical Framework</h3>
            <p>Through commands and examples, {book} contributes to biblical understanding of righteous living.</p>

            <h3>Messianic Anticipation</h3>
            <p>Various passages contribute to the developing messianic hope in Scripture.</p>
            """
        else:  # New Testament
            return f"""
            <p>{book} contributes significantly to biblical theology in several areas:</p>

            <h3>Christology</h3>
            <p>The book develops understanding of Jesus Christ's person and work.</p>

            <h3>Soteriology</h3>
            <p>The book articulates aspects of salvation accomplished through Christ.</p>

            <h3>Ecclesiology</h3>
            <p>Through instruction and example, {book} shapes understanding of the church's nature and purpose.</p>

            <h3>Eschatology</h3>
            <p>The book contributes to biblical teaching about last things.</p>
            """

    return theological.get(book, """
        <p>The book develops several significant theological concepts:</p>

        <h3>Divine Revelation</h3>
        <p>God communicates His character, will, and purposes through various means.</p>

        <h3>Covenant Relationship</h3>
        <p>The formal relationship between God and His people establishes mutual commitments.</p>

        <h3>Human Responsibility</h3>
        <p>People are accountable for their response to divine revelation.</p>

        <h3>Divine Faithfulness</h3>
        <p>Despite human failures, God remains faithful to His promises and purposes.</p>
        """)


def generate_book_tags(book, genre):
    """Generate tags for a book based on its themes and genre"""
    # Base tags on genre
    genre_tags = {
        "narrative": ["Historical", "Narrative", "Story"],
        "law": ["Law", "Torah", "Covenant"],
        "poetry": ["Poetry", "Wisdom", "Lyrical"],
        "prophecy": ["Prophecy", "Prophetic", "Oracle"],
        "apocalyptic": ["Apocalyptic", "Symbolic", "Visionary"],
        "epistle": ["Epistle", "Letter", "Instruction"],
        "gospel": ["Gospel", "Biography", "Testimony"],
        "wisdom": ["Wisdom", "Proverb", "Teaching"]
    }

    # Book-specific tags
    book_specific_tags = {
        "Genesis": ["Creation", "Patriarchs", "Covenant", "Origins"],
        "Exodus": ["Deliverance", "Law", "Tabernacle", "Moses"],
        "Leviticus": ["Holiness", "Sacrifice", "Priesthood", "Ritual"],
        "Numbers": ["Wilderness", "Journey", "Census", "Rebellion"],
        "Deuteronomy": ["Covenant", "Law", "Moses", "Instruction"],
        "Joshua": ["Conquest", "Promised Land", "Leadership", "Victory"],
        "Judges": ["Cycle", "Deliverance", "Apostasy", "Tribalism"],
        "Ruth": ["Loyalty", "Redemption", "Kinsman-Redeemer", "Foreigner"],
        "1 Samuel": ["Kingship", "Saul", "David", "Transition"],
        "2 Samuel": ["David", "Kingdom", "Covenant", "Kingship"],
        "1 Kings": ["Solomon", "Temple", "Division", "Kings"],
        "2 Kings": ["Kings", "Prophets", "Exile", "Judgment"],
        "1 Chronicles": ["David", "Genealogy", "Temple", "Worship"],
        "2 Chronicles": ["Temple", "Kings", "Worship", "Reformation"],
        "Ezra": ["Return", "Restoration", "Temple", "Law"],
        "Nehemiah": ["Rebuilding", "Walls", "Reform", "Leadership"],
        "Esther": ["Providence", "Deliverance", "Courage", "Identity"],
        "Job": ["Suffering", "Wisdom", "Righteousness", "Divine Justice"],
        "Psalms": ["Worship", "Praise", "Lament", "Prayer"],
        "Proverbs": ["Wisdom", "Instruction", "Conduct", "Character"],
        "Ecclesiastes": ["Meaning", "Vanity", "Wisdom", "Purpose"],
        "Song of Solomon": ["Love", "Marriage", "Devotion", "Relationship"],
        "Isaiah": ["Holiness", "Messiah", "Judgment", "Restoration"],
        "Jeremiah": ["Judgment", "Covenant", "Restoration", "Prophet"],
        "Lamentations": ["Grief", "Judgment", "Mercy", "Destruction"],
        "Ezekiel": ["Glory", "Vision", "Judgment", "Restoration"],
        "Daniel": ["Kingdom", "Sovereignty", "Faithfulness", "Prophecy"],
        "Hosea": ["Faithfulness", "Covenant", "Redemption", "Apostasy"],
        "Joel": ["Day of the LORD", "Judgment", "Restoration", "Spirit"],
        "Amos": ["Justice", "Judgment", "Righteousness", "Prophecy"],
        "Obadiah": ["Judgment", "Pride", "Edom", "Restoration"],
        "Jonah": ["Mercy", "Mission", "Repentance", "Compassion"],
        "Micah": ["Justice", "Judgment", "Messiah", "Covenant"],
        "Nahum": ["Judgment", "Nineveh", "Justice", "Vengeance"],
        "Habakkuk": ["Faith", "Justice", "Sovereignty", "Questioning"],
        "Zephaniah": ["Day of the LORD", "Judgment", "Remnant", "Restoration"],
        "Haggai": ["Temple", "Priorities", "Restoration", "Blessing"],
        "Zechariah": ["Messiah", "Vision", "Restoration", "Future"],
        "Malachi": ["Covenant", "Faithfulness", "Offering", "Messenger"],
        "Matthew": ["Kingdom", "Messiah", "Fulfillment", "Teaching"],
        "Mark": ["Servant", "Action", "Suffering", "Discipleship"],
        "Luke": ["Savior", "Universal", "Social Justice", "Holy Spirit"],
        "John": ["Belief", "Life", "Word", "Signs"],
        "Acts": ["Church", "Holy Spirit", "Mission", "Growth"],
        "Romans": ["Righteousness", "Faith", "Grace", "Salvation"],
        "1 Corinthians": ["Unity", "Wisdom", "Gifts", "Love"],
        "2 Corinthians": ["Ministry", "Reconciliation", "Generosity", "Weakness"],
        "Galatians": ["Freedom", "Grace", "Faith", "Law"],
        "Ephesians": ["Unity", "Church", "Grace", "Spiritual Warfare"],
        "Philippians": ["Joy", "Humility", "Unity", "Contentment"],
        "Colossians": ["Supremacy", "Completeness", "Wisdom", "Freedom"],
        "1 Thessalonians": ["Encouragement", "Hope", "Faith", "Return"],
        "2 Thessalonians": ["Judgment", "Work", "Hope", "Perseverance"],
        "1 Timothy": ["Leadership", "Church Order", "Sound Doctrine", "Godliness"],
        "2 Timothy": ["Endurance", "Scripture", "Faithfulness", "Legacy"],
        "Titus": ["Good Works", "Leadership", "Sound Doctrine", "Grace"],
        "Philemon": ["Reconciliation", "Forgiveness", "Brotherhood", "Transformation"],
        "Hebrews": ["Superiority", "Faith", "Perseverance", "Covenant"],
        "James": ["Works", "Faith", "Wisdom", "Speech"],
        "1 Peter": ["Suffering", "Holiness", "Hope", "Identity"],
        "2 Peter": ["Knowledge", "False Teaching", "Day of the Lord", "Growth"],
        "1 John": ["Love", "Truth", "Fellowship", "Assurance"],
        "2 John": ["Truth", "Love", "Discernment", "Hospitality"],
        "3 John": ["Hospitality", "Truth", "Example", "Leadership"],
        "Jude": ["Contending", "Faith", "False Teaching", "Judgment"],
        "Revelation": ["Victory", "Judgment", "Worship", "New Creation"]
    }

    # Combine tags
    tags = []

    # Add genre tags
    for key in genre_tags.keys():
        if key in genre.lower():
            tags.extend(genre_tags[key])
            break

    # Add book-specific tags
    if book in book_specific_tags:
        tags.extend(book_specific_tags[book])

    # Return unique tags
    return list(set(tags))


def get_book_genre(book):
    """Return the literary genre of a book"""
    return BOOK_GENRE.get(book, "Biblical literature")


def generate_book_introduction(book):
    """Generate introduction for a book"""
    # You would implement detailed logic here based on the book
    # This is a simplified version that would be expanded

    introductions = {
        "Genesis": """
        <p>Genesis stands as the magnificent opening movement of God's eternal symphony, establishing the foundational truths upon which all subsequent Scripture builds. The Hebrew title <em>Bereshith</em> ("In the beginning") and the Greek <em>Genesis</em> ("origin" or "generation") both capture the book's essential character as the account of beginnings—the universe, life, humanity, sin, redemption, and the covenant people of God. Traditionally attributed to Moses, who received both direct revelation and ancient records under divine inspiration, Genesis spans an extraordinary chronological range from creation (circa 4000 BCE) to Israel's settlement in Egypt (circa 1700 BCE), encompassing more historical time than any other biblical book.</p>

        <p>As the foundational document of the Pentateuch (Torah), Genesis establishes the theological architecture for understanding God's character, His relationship with creation, and His redemptive purposes. The book introduces and develops the great themes that echo throughout Scripture: divine sovereignty and human responsibility, creation and fall, judgment and grace, covenant faithfulness and human unfaithfulness, promise and fulfillment, election and mission. Every major theological concept in Scripture finds its seedbed in Genesis, making it indispensable for biblical theology.</p>

        <p>The literary structure of Genesis reveals careful theological artistry. The primeval history (chapters 1-11) addresses universal human concerns through a series of escalating crises: creation and fall (1-3), fratricide and civilization's corruption (4-6), judgment and new beginning through the flood (7-9), and the scattering at Babel (10-11). These narratives establish fundamental truths about God's nature, human nature, sin's consequences, and divine grace. The patriarchal narratives (chapters 12-50) then focus the universal scope onto God's particular covenant relationship with Abraham and his descendants, tracing the development of promise through four generations: Abraham (12-25), Isaac (25-26), Jacob (27-36), and Joseph (37-50).</p>

        <p>Genesis presents God as the sovereign Creator who speaks the universe into existence, the holy Judge who responds to sin with righteous judgment, the gracious Redeemer who provides covering for human shame and promises ultimate victory over evil, and the faithful Covenant-maker who binds Himself by promise to bless all nations through Abraham's offspring. The book's doctrine of humanity reveals both the dignity of image-bearing and the devastation of the fall, establishing the theological tension that drives the entire biblical narrative toward its resolution in Christ.</p>

        <p>Archaeological discoveries have illuminated many aspects of Genesis's ancient Near Eastern background while highlighting its distinctive theological perspectives. Unlike contemporaneous creation myths that depict chaotic divine conflicts, Genesis presents ordered creation by divine fiat. Where ancient flood stories feature capricious gods, Genesis reveals moral judgment and gracious preservation. The patriarchal narratives reflect accurate knowledge of second-millennium customs, geography, and social structures, supporting their historical reliability while emphasizing their theological significance.</p>

        <p>The book's theological significance extends far beyond historical narrative. Genesis provides the foundation for understanding the Trinity (with hints of divine plurality in creation), the nature of marriage and family, the origin and consequence of sin, the principle of substitutionary sacrifice, the covenant of grace, election and calling, divine providence, and eschatological hope. New Testament authors repeatedly return to Genesis for theological foundation, citing it more than any other Old Testament book except Psalms and Isaiah.</p>
        """,

        "Exodus": """
        <p>Exodus stands as one of the most theologically significant and historically foundational books in Scripture, chronicling the birth of Israel as a nation and establishing paradigms of redemption that resonate throughout biblical revelation. The Hebrew title <em>Shemoth</em> ("Names") reflects the book's opening genealogical connection to Genesis, while the Greek <em>Exodus</em> ("going out") captures the central redemptive event that defines Israel's identity and God's character as Redeemer. Traditionally attributed to Moses, who was uniquely qualified as both participant and recipient of divine revelation, Exodus spans approximately 80-90 years from Israel's oppression in Egypt through their formative period at Mount Sinai.</p>

        <p>As the pivotal second movement of the Pentateuch, Exodus transforms the family narrative of Genesis into the national epic of Israel, establishing the theological foundations for understanding covenant relationship, redemptive deliverance, divine law, and theocratic worship. The book's tri-partite structure reveals divine purpose: redemption from bondage (chapters 1-15), preparation for covenant (chapters 16-18), and establishment of covenant relationship with its attendant law and worship system (chapters 19-40). This structure establishes the biblical pattern of salvation (deliverance), sanctification (preparation), and service (covenant worship).</p>

        <p>The theological significance of Exodus cannot be overstated. It introduces the divine name YHWH with unprecedented fullness, revealing God's self-existence, covenant faithfulness, and redemptive character. The book establishes fundamental doctrines: the nature of divine calling and commissioning (Moses' burning bush encounter), the reality of spiritual warfare (the plagues as assault on Egyptian deities), the principle of substitutionary redemption (Passover), the nature of divine judgment and mercy (Red Sea deliverance), the character of divine law as expression of divine holiness, and the necessity of mediated approach to the holy God (priesthood and sacrificial system).</p>

        <p>Exodus profoundly shapes biblical understanding of redemption through its typological richness. The Passover lamb prefigures Christ as the Lamb of God, the Red Sea crossing anticipates baptism and deliverance from sin's dominion, the wilderness journey represents the believer's pilgrimage, manna symbolizes dependence on divine provision (fulfilled in Christ as bread of life), and the tabernacle system establishes the theology of divine presence, substitutionary sacrifice, and priestly mediation that finds ultimate fulfillment in Christ's work.</p>

        <p>Archaeological discoveries have confirmed many details of Exodus while illuminating its ancient Near Eastern context. The oppression narrative reflects accurate knowledge of Egyptian building projects, administrative practices, and social conditions during the New Kingdom period. The wilderness itinerary contains authentic geographical and topographical details. The tabernacle construction accounts demonstrate intimate familiarity with ancient craftsmanship and religious practices. Yet Exodus consistently presents Israel's experience as unique, emphasizing YHWH's supremacy over all competing claims to deity.</p>

        <p>The book's literary artistry enhances its theological message through careful structuring, vivid imagery, and dramatic tension. The plague narrative builds inexorably toward the climactic Passover, each plague demonstrating YHWH's sovereignty over a particular aspect of Egyptian religion. The Sinai theophany combines awesome transcendence with gracious covenant-making. The golden calf apostasy and subsequent restoration reveal both human sinfulness and divine mercy, establishing the pattern of covenant violation and renewal that characterizes Israel's subsequent history.</p>

        <p>Exodus establishes Israel's constitutional framework through the Mosaic Law, which encompasses moral principles (Ten Commandments), civil legislation (Book of the Covenant), and ceremonial regulations (tabernacle laws). This comprehensive legal system distinguishes Israel from surrounding nations while reflecting universal moral principles rooted in divine character. The law serves multiple purposes: revealing God's holiness, exposing human sinfulness, providing social order, and pointing toward ultimate redemption through the sacrificial system.</p>

        <p>The tabernacle, described in extraordinary detail, serves as the book's climax and theological center. Its elaborate construction demonstrates several crucial truths: God's desire to dwell among His people, the necessity of approaching the holy God according to divine prescription, the centrality of substitutionary sacrifice, the importance of priestly mediation, and the symbolic nature of worship that points beyond itself to eternal realities. The tabernacle's completion and the descent of divine glory (40:34-38) fulfills God's promise to dwell among His people and provides the theological foundation for understanding divine presence throughout Scripture.</p>
        """,

        "Revelation": """
        <p>Revelation stands as the magnificent crescendo of biblical revelation, the ultimate unveiling of God's eternal purposes and the triumphant conclusion of redemptive history. The Greek title <em>Apokalypsis</em> ("apocalypse" or "unveiling") captures the book's essential character as divine disclosure of hidden realities, while its alternative designation as "The Revelation of Jesus Christ" emphasizes both its christocentric focus and its origin in the risen Lord Himself. Written by John the Apostle during his exile on Patmos around 95 CE under Emperor Domitian's persecution, this prophetic masterpiece addresses seven churches in Asia Minor while providing a cosmic perspective on the spiritual warfare underlying human history and the certain victory of God's kingdom.</p>

        <p>As the Bible's primary apocalyptic work, Revelation employs the sophisticated literary conventions of Jewish apocalyptic literature while transcending them through its uncompromising Christian theology. The book operates on multiple levels simultaneously: it functions as an epistle to first-century churches, a prophecy concerning future events, and an apocalyptic vision of eternal realities. Its complex symbolic system draws from an extraordinary range of Old Testament sources—particularly Daniel, Ezekiel, Isaiah, and Zechariah—creating an intricate tapestry of intertextual allusions that requires deep biblical literacy to fully appreciate. The book contains over 400 Old Testament allusions while never directly quoting any passage, demonstrating the author's profound scriptural knowledge and sophisticated literary technique.</p>

        <p>The theological architecture of Revelation reveals careful structural design built around the number seven (appearing 54 times), symbolizing divine perfection and completeness. The book unfolds through a series of interconnected septets: seven churches (2-3), seven seals (6-8), seven trumpets (8-11), seven bowls (16), and seven beatitudes scattered throughout. This numerical symbolism extends to other significant numbers: twelve (representing the people of God), three and a half or 42 months or 1,260 days (representing the period of tribulation), and 144,000 (the symbolic number of the redeemed). These numerical patterns create a liturgical rhythm that enhances the book's use in worship while reinforcing its theological themes.</p>

        <p>Revelation's christology reaches the pinnacle of New Testament development, presenting Christ in multiple roles: the risen Lord walking among the lampstands (1), the slain Lamb who is worthy to open the sealed scroll (5), the conquering Lion of Judah (5), the faithful and true witness (19), the Word of God clothed in a robe dipped in blood (19), and the Alpha and Omega who makes all things new (21-22). This multifaceted portrait integrates Christ's first advent in humility with His second advent in glory, His sacrificial death with His royal victory, His identification with human suffering with His cosmic sovereignty. The famous image of the Lamb standing as though slain (5:6) paradoxically combines vulnerability and power, revealing that ultimate victory comes through redemptive suffering.</p>

        <p>The book's treatment of eschatology addresses both individual and cosmic destiny while maintaining productive tension between already/not yet fulfillment. The heavenly throne room scenes (4-5) establish God's eternal sovereignty and the Lamb's worthiness to execute divine purposes. The judgment sequences (seals, trumpets, bowls) reveal God's progressive response to persistent evil while maintaining space for repentance. The fall of Babylon (17-18) symbolizes the collapse of all systems opposed to God's rule. The millennium (20) represents the establishment of divine righteousness, however interpreted. The new heaven and earth (21-22) envision the ultimate transformation of creation into God's eternal dwelling place with His people.</p>

        <p>Archaeological and historical research has illuminated Revelation's first-century context while confirming its accurate knowledge of imperial ideology and local conditions. The seven cities addressed were major centers along the Roman postal route in Asia Minor, each facing specific challenges from emperor worship, trade guild requirements, and social pressure to compromise Christian distinctives. Emperor Domitian's demand for divine honors created particular tension for Christians whose exclusive loyalty to Christ as Lord conflicted with imperial claims to divinity. The book's political symbolism, while encoded for protection, clearly presents Christ as the true Caesar and God's kingdom as the ultimate imperium.</p>

        <p>The literary artistry of Revelation employs sophisticated techniques including chiastic structure, recapitulation, progressive parallelism, and telescoping visions. The trumpet and bowl judgments follow similar patterns while intensifying in severity. The woman clothed with the sun (12) and the harlot Babylon (17) present contrasting images of faithful and unfaithful community. The marriage supper of the Lamb (19) and the holy city descending from heaven (21) provide climactic images of consummated union between God and His people. These literary patterns reinforce the book's theological message while creating memorable imagery for liturgical and devotional use.</p>

        <p>Revelation's influence on Christian thought, worship, and culture has been immeasurable, inspiring countless artistic works, musical compositions, architectural designs, and theological reflections. Its hymnic passages have enriched Christian liturgy from ancient times, while its vivid imagery has provided hope for persecuted believers throughout church history. The book's emphasis on divine sovereignty provides comfort in times of chaos, its call to faithful witness challenges complacency, and its vision of ultimate renewal sustains hope for cosmic restoration.</p>

        <p>The theological synthesis of Revelation brings the entire biblical narrative to its intended conclusion, resolving the tensions introduced in Genesis and developed throughout Scripture. The tree of life, lost in Eden, reappears in the new Jerusalem. The curse pronounced after the fall is finally removed. The scattered nations of Babel are gathered in harmonious worship. The promise to Abraham that all nations would be blessed through his offspring finds ultimate fulfillment as the nations walk by the light of the Lamb. Death, the last enemy, is finally destroyed. The dwelling of God is with humanity, and they shall be His people, and God Himself will be with them and be their God—the ultimate fulfillment of the covenant promise that echoes throughout Scripture.</p>
        """
    }

    # Get a template introduction based on genre if specific introduction isn't available
    if book not in introductions:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        # Generate a generic introduction based on testament and genre
        if "narrative" in genre.lower():
            intro = f"""
            <p>{book} is a narrative book in the {testament} that recounts key historical events and developments in Israel's history. The book contains important stories, characters, and events that contribute to the broader biblical narrative and redemptive history.</p>

            <p>As with other biblical narratives, {book} combines historical reporting with theological interpretation, showing how God works through historical circumstances and human actions to accomplish His purposes. The narrative demonstrates divine providence, human responsibility, and the consequences of both obedience and disobedience.</p>

            <p>Throughout {book}, readers can observe God's faithfulness to His covenant promises despite human failings and opposition. The book's events establish important precedents and patterns that inform biblical theology and provide context for understanding later Scriptural developments.</p>
            """
        elif "epistle" in genre.lower():
            intro = f"""
            <p>{book} is an epistle (letter) in the {testament} written to address specific circumstances, challenges, and questions in the early Christian church. The letter combines theological instruction with practical exhortation, demonstrating the connection between Christian doctrine and everyday living.</p>

            <p>Like other New Testament epistles, {book} addresses particular situations while establishing principles with broader application. The letter reflects the apostolic authority of its author and the normative teaching of the early church, contributing to the development of Christian theology and practice.</p>

            <p>Throughout {book}, readers can observe the practical outworking of the gospel in community life, personal ethics, and spiritual development. The letter demonstrates how Christ's finished work transforms individual believers and reshapes their relationships and priorities.</p>
            """
        elif "prophetic" in genre.lower() or "prophecy" in genre.lower():
            intro = f"""
            <p>{book} is a prophetic book in the {testament} that communicates divine messages of warning, judgment, and hope to God's people. The prophecies combine historical relevance to their original audience with enduring theological significance and, in some cases, messianic predictions.</p>

            <p>Like other biblical prophetic literature, {book} addresses covenant violations, calls for repentance, and proclaims both divine judgment and promised restoration. The prophecies demonstrate God's righteousness, sovereignty over history, and faithful commitment to His covenant purposes.</p>

            <p>Throughout {book}, readers encounter powerful imagery, poetic language, and symbolic actions that reinforce the prophetic message. The book reveals God's perspective on historical events and human affairs, often challenging conventional wisdom and cultural assumptions.</p>
            """
        elif "wisdom" in genre.lower():
            intro = f"""
            <p>{book} is a wisdom book in the {testament} that addresses life's fundamental questions and provides guidance for righteous living. The book explores themes of divine order, human experience, and practical ethics, offering insights for navigating the complexities of human existence.</p>

            <p>Like other biblical wisdom literature, {book} emphasizes the fear of the Lord as the foundation of true wisdom and contrasts the paths of wisdom and folly. The book demonstrates how reverence for God leads to discernment, virtue, and ultimately flourishing.</p>

            <p>Throughout {book}, readers encounter profound reflections on creation's order, human limitations, moral principles, and life's meaning. The book bridges theological truth and practical living, showing how divine wisdom applies to everyday decisions and relationships.</p>
            """
        elif "gospel" in genre.lower():
            intro = f"""
            <p>{book} is a gospel account in the {testament} that presents the life, ministry, death, and resurrection of Jesus Christ. The book combines historical reporting with theological interpretation, portraying Jesus as the fulfillment of Old Testament promises and the inaugurator of God's kingdom.</p>

            <p>Like other canonical gospels, {book} selectively records Jesus' words and deeds to communicate His identity and significance. The narrative demonstrates Jesus' divine authority, redemptive mission, and transformative teaching, inviting readers to respond in faith.</p>

            <p>Throughout {book}, readers encounter Jesus' interactions with various individuals and groups, His powerful parables and discourses, and the climactic events of His passion and resurrection. The book establishes the historical foundation for Christian faith while interpreting Jesus' significance for all humanity.</p>
            """
        elif "apocalyptic" in genre.lower():
            intro = f"""
            <p>{book} is an apocalyptic book in the {testament} that unveils spiritual realities and future events through symbolic visions and prophetic declarations. The book employs rich imagery and symbolic language to communicate divine perspective on history, cosmic conflict, and ultimate outcomes.</p>

            <p>Like other biblical apocalyptic literature, {book} addresses contexts of suffering and persecution, offering hope through the assurance of God's sovereignty and eventual triumph. The visions demonstrate the temporary nature of evil powers and the certainty of divine judgment and redemption.</p>

            <p>Throughout {book}, readers encounter dramatic portrayals of spiritual warfare, divine intervention, and eschatological consummation. The book provides a cosmic framework for understanding present trials and maintaining faithful endurance through the assurance of God's ultimate victory.</p>
            """
        else:
            intro = f"""
            <p>{book} is an important book in the {testament} that contributes significantly to the biblical canon. The book addresses themes and concerns relevant to its original audience while establishing principles and patterns with enduring theological significance.</p>

            <p>As with other biblical literature, {book} combines historical awareness with divine inspiration, communicating God's truth through human language and cultural forms. The book demonstrates the progressive nature of divine revelation and its adaptation to specific historical contexts.</p>

            <p>Throughout {book}, readers can trace important developments in the biblical narrative and theological understanding. The book provides essential insights for comprehending God's character, purposes, and relationship with humanity.</p>
            """

        return intro

    return introductions[book]


def generate_historical_context(book):
    """Generate historical context for a book"""
    historical_contexts = {
        "Genesis": """
        <p>Genesis was compiled and written by Moses around 1440-1400 BCE according to traditional attribution, though the events it records span an extraordinary chronological range from creation to approximately 1700 BCE when Israel settled in Egypt. The book was composed for the Israelites after their exodus from Egypt as they prepared to enter the Promised Land, providing them with their theological and historical foundation as the people of God. Archaeological evidence and textual analysis support Mosaic authorship while allowing for minor editorial updates during later periods.</p>

        <h3>Ancient Near Eastern Cultural Milieu</h3>
        <p>The world of Genesis was dominated by sophisticated civilizations in Mesopotamia, Egypt, and Canaan, each contributing to the complex cultural matrix within which the patriarchs lived and moved. The Sumerian civilization (c. 3500-2000 BCE) had established urban centers, developed cuneiform writing, created elaborate temple complexes (ziggurats), and produced extensive literature including creation myths, flood narratives, and wisdom literature. The Akkadian Empire (c. 2334-2154 BCE) unified Mesopotamia under Sargon and his successors, creating the first multi-ethnic empire and spreading Semitic languages throughout the region.</p>

        <p>Egypt during the patriarchal period experienced the grandeur of the Old Kingdom (c. 2686-2181 BCE) with its pyramid construction, followed by the Middle Kingdom (c. 2055-1650 BCE) when the patriarchs likely entered Egypt. Egyptian religion was sophisticated and pervasive, with elaborate funeral practices, temple rituals, and a complex pantheon headed by Ra, Ptah, and Amun. The pharaoh was considered divine, creating a theological environment radically different from the monotheism of the patriarchs.</p>

        <h3>Comparative Literature and Distinctive Theology</h3>
        <p>Genesis shares certain structural and thematic similarities with ancient Near Eastern literature while maintaining fundamental theological distinctions. The Enuma Elish (Babylonian creation epic) describes creation through divine conflict and the establishment of Marduk's supremacy, contrasting sharply with Genesis's peaceful creation through divine fiat. The Epic of Gilgamesh contains a flood narrative (Utnapishtim) with remarkable parallels to Noah's account, yet the biblical version emphasizes moral judgment and divine covenant rather than capricious divine annoyance.</p>

        <p>The Atrahasis Epic provides another flood account emphasizing overpopulation and divine irritation, while Genesis focuses on moral corruption and divine justice. Sumerian King Lists mention extraordinarily long lifespans for antediluvian rulers, paralleling Genesis's pre-flood longevity accounts. The Mesopotamian creation account in Genesis 2 uses geographical references (Tigris, Euphrates, Pishon, Gihon) that reflect intimate knowledge of ancient river systems and geography.</p>

        <h3>Archaeological Illumination</h3>
        <p>Archaeological discoveries have dramatically illuminated the Genesis narratives while confirming their historical reliability. The Nuzi tablets (15th-14th centuries BCE) reveal social customs that precisely match patriarchal practices: adoption procedures, inheritance laws, marriage customs, and property transactions described in Genesis. The Mari archives (18th century BCE) document the semi-nomadic lifestyle, tribal movements, and personal names that characterize the patriarchal period.</p>

        <p>Excavations at sites like Ur, Haran, Shechem, Hebron, and Beersheba have revealed extensive Middle Bronze Age occupation during the patriarchal period. The discovery of the Ebla tablets (c. 2400-2250 BCE) has provided numerous parallels to early Genesis, including place names, personal names, and cultural practices. Egyptian records from the Middle Kingdom period document Asiatic immigration into Egypt, providing the historical context for Jacob's family settlement in Goshen.</p>

        <h3>Religious and Social Context</h3>
        <p>The religious environment of the ancient Near East was thoroughly polytheistic, with elaborate temple systems, professional priesthoods, and complex mythologies explaining natural phenomena and human existence. Each city-state typically had a patron deity with associated temples, festivals, and ritual requirements. The concept of covenant relationships between deities and peoples was common, though these typically involved mutual obligations and were often temporary or conditional.</p>

        <p>Social structures were hierarchical and patriarchal, with extended family units (bet ab - "father's house") forming the basic social unit. Marriage customs included bride-price, polygamy among the wealthy, and complex inheritance laws favoring male primogeniture. The practice of adoption was common for childless couples, and the rights of the firstborn carried significant legal and social weight. Genesis accurately reflects these cultural patterns while subverting them through divine election and covenant promise.</p>

        <h3>Linguistic and Literary Features</h3>
        <p>Genesis exhibits archaic Hebrew linguistic features consistent with early composition, including ancient poetic structures (like Jacob's blessing in chapter 49), primitive narrative techniques, and vocabulary that reflects contact with both Mesopotamian and Egyptian cultures. The use of different divine names (Elohim, YHWH, El Shaddai) reflects sophisticated theological understanding rather than documentary fragmentation, as each name emphasizes different aspects of divine character appropriate to specific contexts.</p>

        <p>The toledot ("generations") structure that organizes Genesis reflects ancient genealogical and historiographical practices found throughout the ancient Near East. The narrative's concern with genealogy, chronology, and geographical precision demonstrates the author's intent to provide historical rather than merely mythological material. The literary artistry evident in the patriarchal narratives—including wordplay, symmetry, and thematic development—reveals sophisticated compositional technique consistent with ancient scribal education.</p>

        <h3>Cultural Background</h3>
        <p>The patriarchs (Abraham, Isaac, and Jacob) lived as semi-nomadic herdsmen, moving between established city-states in Canaan. Their lifestyle involved seasonal migration with flocks and herds, establishing temporary settlements, and digging wells. Kinship ties were paramount, with extended family groups (clans) forming the basic social unit.</p>

        <p>Marriage customs included bride prices, arranged marriages, and occasionally polygamy, especially when a first wife was barren. Inheritance typically passed to the firstborn son, though Genesis records several instances where this pattern was divinely overturned.</p>

        <h3>Archaeological Insights</h3>
        <p>Archaeological discoveries have illuminated many aspects of the Genesis narratives. Excavations at sites like Ur (Abraham's birthplace) reveal a sophisticated urban center. Tablets from Mari and Nuzi document social customs similar to those practiced by the patriarchs, including adoption agreements, surrogacy arrangements, and covenant ceremonies.</p>

        <p>Egypt's Middle Kingdom period (2040-1782 BCE) provides the likely background for Joseph's rise to prominence. Historical records show that Semitic people did indeed achieve high positions in Egyptian administration, and periods of famine are documented in Egyptian history.</p>
        """,

        "Exodus": """
        <p>Exodus emerges from the historical setting of Egyptian dominance and Israelite oppression during the second millennium BCE. Traditional dating places the exodus event around 1446 BCE (based on 1 Kings 6:1), though some scholars prefer a later date around 1270-1260 BCE during Rameses II's reign.</p>

        <h3>Egyptian Background</h3>
        <p>The Egypt of Exodus was a sophisticated civilization with monumental architecture, complex religious systems, and highly centralized government. The unnamed pharaoh likely ruled during Egypt's New Kingdom period (1550-1070 BCE), a time of imperial expansion and extensive building projects requiring massive labor forces. Egyptian records confirm the use of Semitic slaves for construction, and archaeological evidence from sites like Pi-Rameses aligns with biblical descriptions of brick-making with straw.</p>

        <p>Egyptian religion centered on a vast pantheon of deities associated with natural forces. The pharaoh claimed divine status as the incarnation of Horus and son of Ra, providing context for the cosmic theological conflict underlying the plagues, each targeting specific Egyptian gods. This religious background illuminates why Pharaoh repeatedly hardened his heart despite mounting evidence of YHWH's superior power.</p>

        <h3>Israelite Situation</h3>
        <p>The Israelites had grown from Jacob's family of 70 persons to a multitude large enough to threaten Egyptian security (Exodus 1:7-10). Archaeological evidence from the eastern Nile Delta (biblical Goshen) confirms Semitic settlements during this period. Their transition from honored guests (due to Joseph's position) to enslaved laborers likely occurred with a dynastic change—"a new king...who did not know about Joseph" (Exodus 1:8).</p>

        <p>The forced labor conditions described in Exodus are consistent with Egyptian practices for foreign populations. Israelite identity during this period was primarily tribal and familial rather than national. The exodus event would become foundational for their emerging national identity and self-understanding as a people set apart by divine election and deliverance.</p>

        <h3>Wilderness Context</h3>
        <p>The Sinai Peninsula, where Israel journeyed after leaving Egypt, was sparsely populated and largely controlled by Egypt through mining operations and military outposts. The harsh desert environment required divine provision for survival, emphasizing Israel's dependence on God. Egyptian records confirm the presence of Semitic peoples in this region during the second millennium BCE.</p>

        <p>Mount Sinai (possibly Jebel Musa in traditional identification) provided an appropriately awesome setting for divine revelation. The theophanic manifestations described in Exodus—thunder, lightning, earthquake, fire, and cloud—align with the dramatic landscape of the Sinai mountains. This wilderness experience would become paradigmatic for Israel's understanding of pilgrimage, testing, and dependence on divine grace.</p>
        """,

        "Revelation": """
        <p>Revelation was written during the reign of Emperor Domitian (81-96 CE), according to early church tradition as recorded by Irenaeus. The author, John, was exiled to the island of Patmos "because of the word of God and the testimony of Jesus" (1:9), indicating persecution for his Christian witness. The book addresses seven actual churches in the Roman province of Asia (western Turkey).</p>

        <h3>Roman Imperial Context</h3>
        <p>The late first century was marked by increasing imperial persecution of Christians. Domitian intensified emperor worship throughout the Roman Empire, demanding to be addressed as "Lord and God" (<em>dominus et deus noster</em>). He established an imperial cult with temples and statues dedicated to his worship. Christians who refused to participate in emperor worship faced economic sanctions, social ostracism, and sometimes execution.</p>

        <p>The province of Asia, where the seven churches were located, was particularly zealous in emperor worship. Ephesus, Smyrna, and Pergamum all had temples dedicated to the imperial cult. Pergamum is specifically mentioned as the place "where Satan's throne is" (2:13), likely referring to its prominence in emperor worship or its massive altar to Zeus.</p>

        <h3>Church Situation</h3>
        <p>The seven churches addressed in Revelation faced varying challenges. Some endured direct persecution (Smyrna, Philadelphia), while others struggled with false teaching (Ephesus, Pergamum, Thyatira), spiritual apathy (Sardis), or lukewarm commitment (Laodicea). Economic pressures pushed some believers toward compromise, as participation in trade guilds often required involvement in pagan rituals.</p>

        <p>Jewish communities in these cities sometimes opposed Christian groups, as mentioned regarding Smyrna and Philadelphia (2:9, 3:9). This created additional social pressure for Jewish Christians caught between their ethnic heritage and new faith.</p>

        <h3>Archaeological Evidence</h3>
        <p>Archaeological excavations have confirmed details about the seven cities addressed in Revelation. Laodicea's lukewarm water came from aqueducts carrying water from hot springs that cooled during transit. The city was indeed wealthy, with a banking industry and medical school known for eye salve. Philadelphia was subject to frequent earthquakes, as alluded to in the promise of a pillar that would never be shaken (3:12).</p>

        <p>Ephesus was home to the Temple of Artemis (Diana), one of the Seven Wonders of the ancient world. Excavations have uncovered a massive theater (Acts 19) and evidence of the city's prominence and wealth. Sardis' reputation as a city that appeared alive but was actually in decline is confirmed by archaeological evidence of its diminishing importance in the late first century.</p>
        """
    }

    # Generate a generic historical context if specific context isn't available
    if book not in historical_contexts:
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            # Determine approximate time period
            period = "pre-exilic"  # Default
            if book in ["Ezra", "Nehemiah", "Esther", "Haggai", "Zechariah", "Malachi"]:
                period = "post-exilic"
            elif book in ["Jeremiah", "Lamentations", "Ezekiel", "Daniel"]:
                period = "exilic"

            context = f"""
            <p>{book} was composed during the {period} period of Israel's history. The book reflects the historical circumstances, cultural influences, and theological concerns of its time.</p>

            <h3>Historical Setting</h3>
            <p>The book emerges from a context where Israel's covenant relationship with God shaped its national identity and religious practices. The surrounding nations, with their polytheistic worship and imperial ambitions, provided both cultural pressure and political threats that influenced Israel's historical experience.</p>

            <p>The religious life of Israel centered around the covenant, Law, and (depending on the period) the temple, with prophets calling the people back to covenant faithfulness and warning of judgment for persistent disobedience.</p>

            <h3>Cultural Background</h3>
            <p>The cultural world of {book} involved agricultural societies organized around tribal and kinship relationships, with increasing urbanization and social stratification over time. Religious practices permeated daily life, and interaction with surrounding cultures created ongoing tension between assimilation and distinctive identity.</p>

            <p>Archaeological discoveries have illuminated many aspects of daily life, religious practices, and historical events mentioned in {book}, providing background context for understanding its narratives and teachings.</p>
            """
        else:  # New Testament
            context = f"""
            <p>{book} was written during the first century CE, within the context of the early Christian church developing under Roman imperial rule. The book reflects the historical circumstances, cultural influences, and theological concerns of this formative period.</p>

            <h3>Roman Imperial Context</h3>
            <p>The Roman Empire provided the overarching political structure for the New Testament world, with its system of provinces, client kingdoms, and military presence. The Pax Romana (Roman Peace) enabled travel and communication throughout the Mediterranean world, facilitating the spread of Christianity while also presenting challenges through imperial ideology and occasional persecution.</p>

            <h3>Religious Environment</h3>
            <p>The religious landscape included Judaism with its various sects (Pharisees, Sadducees, Essenes), Greco-Roman polytheism, mystery religions, and philosophical schools. Early Christianity emerged within this complex environment, defining its identity in relation to Judaism while addressing Gentile converts from pagan backgrounds.</p>

            <p>Archaeological discoveries, historical documents, and cultural studies have illuminated many aspects of daily life, religious practices, and social structures in the first-century world, providing valuable context for understanding {book}.</p>
            """

        return context

    return historical_contexts.get(book, """
        <p>This book was written within the historical context of ancient religious traditions and cultural developments. The book reflects the circumstances, influences, and concerns of its time period while establishing principles with enduring significance.</p>

        <h3>Historical Setting</h3>
        <p>The book emerges from a context where covenant relationship with God shaped religious identity and practices. The surrounding nations and cultures provided both challenges and opportunities that influenced the historical experience of God's people.</p>

        <h3>Cultural Background</h3>
        <p>The cultural world involved societies organized around religious, social, and political structures that shaped daily life and community relationships. Archaeological discoveries have illuminated many aspects of this historical context.</p>
        """)


def get_chapter_significance(book, chapter):
    """Generate significance explanation for a chapter"""
    significance_templates = [
        "provides essential context for understanding God's covenant relationship with His people",
        "reveals key aspects of God's character through divine actions and declarations",
        "establishes important theological principles that resonate throughout Scripture",
        "addresses timeless questions about faith, suffering, and divine purpose",
        "offers practical wisdom for godly living in a fallen world",
        "demonstrates God's faithfulness despite human unfaithfulness",
        "contributes to the biblical metanarrative of redemption",
        "foreshadows Christ's work through typology and prophetic elements",
        "illustrates divine judgment and mercy in response to human actions",
        "provides guidance for worship and spiritual devotion"
    ]

    # Special significance for specific chapters
    special_significance = {
        ("Genesis", 1): "establishes the foundational doctrine of creation and God's sovereignty",
        ("Genesis", 3): "introduces the fall of humanity and the need for redemption",
        ("Exodus", 20): "presents the Decalogue (Ten Commandments) as the cornerstone of biblical law",
        ("Leviticus", 16): "details the Day of Atonement ritual that prefigures Christ's sacrificial work",
        ("Isaiah", 53): "provides the clearest Old Testament prophecy of the Messiah's suffering",
        ("Matthew", 5): "presents Jesus' ethical teaching in the Sermon on the Mount",
        ("John", 3): "contains the essential gospel message of salvation by faith",
        ("Romans", 8): "articulates the doctrines of justification, sanctification, and glorification",
        ("1 Corinthians", 15): "defends the resurrection as central to Christian faith",
        ("Revelation", 1): "introduces apocalyptic visions that reveal Christ's ultimate victory and sovereignty"
    }

    if (book, chapter) in special_significance:
        return special_significance[(book, chapter)]
    else:
        return random.choice(significance_templates)


def generate_book_commentary(book, chapters):
    """Generate comprehensive commentary for an entire book"""
    # Get basic book information
    testament = get_testament_for_book(book)
    time_period = get_time_period(book)
    genre = get_book_genre(book)

    # Generate tags based on themes and genre
    tags = generate_book_tags(book, genre)

    # Generate introduction based on book
    introduction = generate_book_introduction(book)

    # Generate historical context
    historical_context = generate_historical_context(book)

    # Generate literary features
    literary_features = generate_literary_features(book, genre)

    # Generate key themes
    themes = generate_book_themes(book)

    # Generate theological significance
    theological_significance = generate_theological_significance(book)

    # Generate contemporary application
    application = generate_book_application(book)

    # Generate key highlights from the book
    highlights = generate_book_highlights(book, chapters)

    # Generate book outline
    outline = generate_book_outline(book, chapters)

    # Generate cross-references to other books
    cross_references = generate_book_cross_references(book)

    # Generate chapter summaries with key verses
    chapter_summaries = generate_chapter_summaries(book, chapters)

    return {
        "testament": testament,
        "time_period": time_period,
        "genre": genre,
        "tags": tags,
        "introduction": introduction,
        "historical_context": historical_context,
        "literary_features": literary_features,
        "themes": themes,
        "theological_significance": theological_significance,
        "application": application,
        "highlights": highlights,
        "outline": outline,
        "cross_references": cross_references,
        "chapter_summaries": chapter_summaries
    }


def generate_book_application(book):
    """Generate contemporary application for a book"""
    # Simple implementation for now
    applications = {
        "Exodus": """
        <p>Exodus provides enduring insights that apply to contemporary life:</p>

        <h3>Divine Deliverance</h3>
        <p>The exodus story reminds us that God sees and responds to the suffering of His people. In a world where many experience various forms of bondage—whether addiction, oppression, or spiritual darkness—Exodus testifies that God is a deliverer. The pattern of redemption from Egypt foreshadows Christ's greater deliverance from sin, offering hope to those in seemingly impossible situations and affirming that liberation comes through divine intervention, not merely human effort.</p>

        <h3>Identity Formation</h3>
        <p>Israel's transformation from slaves to "a kingdom of priests and a holy nation" (Exodus 19:6) parallels the Christian's new identity in Christ. This theme addresses contemporary questions of personal identity, reminding believers that they are defined not by past bondage or present circumstances but by covenant relationship with God. The corporate identity of Israel also speaks to the church's collective identity as God's people set apart for divine purposes in a secular world.</p>

        <h3>Law and Grace</h3>
        <p>The law given at Sinai provides ethical guidance while demonstrating humanity's need for grace. This balanced perspective challenges both legalism (reducing faith to rule-keeping) and antinomianism (disregarding moral standards). The law in Exodus shows that freedom is not lawlessness but rather the liberty to live according to God's design. For Christians, the moral principles underlying the law continue to provide wisdom for ethical decision-making, even as we recognize Christ as the law's fulfillment.</p>

        <h3>Divine Presence</h3>
        <p>The tabernacle established the profound truth that God desires to dwell among His people. In an age of spiritual disconnection and isolation, this theme reminds us that God is not distant but seeks communion with humanity. The elaborate preparations for God's presence in Exodus highlight both divine holiness and divine nearness. For Christians, this anticipates the incarnation ("the Word became flesh and tabernacled among us") and the indwelling of the Holy Spirit, assuring believers of God's abiding presence through all circumstances.</p>
        """,

        "Genesis": """
        <p>Genesis provides enduring insights that apply to contemporary life:</p>

        <h3>Human Identity and Purpose</h3>
        <p>In a culture often confused about human identity and value, Genesis reminds us that all people bear God's image (Genesis 1:26-27). This foundational truth addresses issues of racism, sexism, abortion, euthanasia, and other ethical concerns by establishing the inherent dignity of every human life. It also counters contemporary nihilism by affirming that human life has divinely-given purpose and meaning.</p>

        <h3>Environmental Stewardship</h3>
        <p>Genesis establishes humans as God's representatives who are to "rule over" creation while simultaneously being charged to "work and take care of" the garden (Genesis 1:28, 2:15). This balanced perspective avoids both exploitative domination and nature worship, providing a theological foundation for responsible environmental stewardship that honors the Creator by caring for His creation.</p>

        <h3>Marriage and Family</h3>
        <p>The creation account establishes marriage as a divine institution uniting male and female in a complementary relationship (Genesis 2:18-25). This foundational teaching informs Christian understanding of gender, sexuality, marriage, and family life. Genesis also honestly portrays family dysfunction, showing the consequences of polygamy, favoritism, deception, and rivalry, providing negative examples that warn against similar patterns.</p>

        <h3>Faith Amid Trials</h3>
        <p>The patriarchs' journeys demonstrate faith amid uncertainty, disappointment, and waiting. Abraham's willingness to leave homeland security for an unknown destination (Genesis 12:1-4) and to trust God's promise despite apparent impossibility (Genesis 15:6) exemplifies the faith journey. Joseph's declaration that "God meant it for good" despite his brothers' evil intentions (Genesis 50:20) provides a profound theology of suffering that acknowledges pain while trusting divine purpose.</p>
        """
    }

    # Default application based on testament and genre
    if book not in applications:
        testament = get_testament_for_book(book)
        genre = get_book_genre(book)

        if testament == "Old Testament":
            return """
            <p>This book provides valuable insights for contemporary application:</p>

            <h3>Understanding God's Character</h3>
            <p>The book reveals aspects of God's nature that remain relevant for today's believers. These divine attributes provide the foundation for theology, worship, and spiritual formation. Understanding God's character shapes our expectations, prayers, and relationship with Him.</p>

            <h3>Covenant Faithfulness</h3>
            <p>God's commitment to His covenant promises demonstrates His trustworthiness and faithfulness. This encourages believers to trust God's promises today and to model similar faithfulness in relationships and commitments. The covenant pattern also informs our understanding of baptism and communion as signs of the new covenant.</p>

            <h3>Ethical Guidance</h3>
            <p>While specific applications may require contextual adaptation, the book's ethical principles provide timeless guidance for moral decision-making. These principles address relationships, justice, integrity, and other aspects of personal and community life. They challenge contemporary cultural values that contradict biblical standards.</p>

            <h3>Spiritual Formation</h3>
            <p>The examples of both faithfulness and failure provide learning opportunities for spiritual development. These biblical accounts invite self-examination and encourage growth in godly character. They remind believers that spiritual formation involves both divine grace and human responsibility.</p>
            """
        else:  # New Testament
            return """
            <p>This book provides valuable insights for contemporary application:</p>

            <h3>Christlike Character</h3>
            <p>The book's portrayal of Jesus and teaching about Him provides the pattern for Christian character and conduct. This Christlikeness manifests in relationships, attitudes, speech, and actions. The transformative power of the gospel enables believers to grow in resembling Christ.</p>

            <h3>Church Life and Mission</h3>
            <p>Principles for healthy church community address worship, leadership, conflict resolution, and mutual edification. These guidelines help contemporary churches maintain biblical faithfulness while addressing current challenges. They also inform the church's missional engagement with surrounding culture.</p>

            <h3>Spiritual Warfare</h3>
            <p>The book acknowledges the reality of spiritual conflict and provides resources for overcoming evil. This perspective balances awareness of spiritual opposition with confidence in Christ's victory. It helps believers recognize and resist temptation while avoiding both naive dismissal and unhealthy obsession with demonic activity.</p>

            <h3>Eschatological Hope</h3>
            <p>The anticipation of Christ's return and the fulfillment of God's promises provides perspective for current circumstances. This hope sustains believers through suffering and shapes priorities and decisions. It balances engagement with present responsibilities and anticipation of future glory.</p>
            """

    return applications.get(book, """
                <p>The book provides enduring insights that profoundly apply to contemporary life, offering divine wisdom for navigating the complexities of modern existence:</p>

                <h3>Spiritual Formation and Discipleship</h3>
                <p>The book offers comprehensive guidance for spiritual growth, character development, and deepening relationship with God. These insights help believers develop authentic faith that withstands cultural pressures, intellectual challenges, and personal trials. The principles for prayer, worship, Scripture study, and spiritual disciplines provide practical pathways for communion with God. The book demonstrates how divine truth transforms the heart, renews the mind, and shapes behavior according to God's righteous standards. Contemporary disciples can apply these insights to develop spiritual maturity, overcome sinful patterns, and cultivate the fruit of the Spirit in daily life.</p>

                <h3>Community Living and Relational Wisdom</h3>
                <p>The book provides profound principles for building healthy relationships, resolving conflicts, and fostering mutual edification within Christian community. These insights address contemporary challenges in marriage and family life, church relationships, workplace dynamics, and social interactions. The book demonstrates how the gospel transforms relationships by promoting forgiveness, humility, service, and sacrificial love. Modern believers can apply these principles to strengthen marriages, raise children according to biblical values, build authentic friendships, and create communities characterized by grace, truth, and mutual support.</p>

                <h3>Ethical Decision-Making and Moral Clarity</h3>
                <p>The book establishes timeless moral principles and decision-making frameworks that help believers navigate complex ethical dilemmas in contemporary society. These guidelines address issues like business ethics, medical decisions, political engagement, environmental stewardship, and social justice concerns. The book demonstrates how divine law reflects God's character and promotes human flourishing, providing objective moral standards that transcend cultural relativism. Contemporary Christians can apply these insights to make decisions that honor God, benefit others, and maintain personal integrity in morally ambiguous situations.</p>

                <h3>Hope, Perseverance, and Eternal Perspective</h3>
                <p>The book provides profound encouragement for facing suffering, maintaining faith during trials, and trusting in God's sovereign purposes even when circumstances seem hopeless. These insights address contemporary struggles with anxiety, depression, injustice, persecution, and existential questions about life's meaning. The book demonstrates how divine promises sustain believers through difficult seasons and how eternal perspective transforms present priorities. Modern disciples can apply these truths to develop resilience, find purpose in suffering, maintain joy amid difficulties, and live with confident hope in God's ultimate victory over evil.</p>

                <h3>Cultural Engagement and Missional Living</h3>
                <p>The book offers wisdom for engaging contemporary culture with gospel truth while maintaining distinct Christian identity and values. These insights help believers navigate secularization, pluralism, technological advancement, and social change without compromising biblical fidelity. The book demonstrates how Christians can serve as salt and light in their communities, workplaces, and spheres of influence. Contemporary believers can apply these principles to engage in meaningful dialogue with unbelievers, advocate for justice and righteousness, and demonstrate the transforming power of the gospel through word and deed.</p>

                <h3>Stewardship and Resource Management</h3>
                <p>The book establishes comprehensive principles for managing time, talents, and treasures as faithful stewards of God's gifts. These insights address contemporary challenges related to materialism, financial planning, career choices, and resource allocation. The book demonstrates how biblical stewardship involves using all resources to glorify God and serve others rather than merely accumulating wealth or pursuing personal advancement. Modern Christians can apply these principles to develop healthy attitudes toward money, make wise investment decisions, practice generous giving, and use their skills and opportunities to advance God's kingdom.</p>

                <h3>Leadership and Influence</h3>
                <p>The book provides timeless principles for exercising godly leadership and positive influence in family, church, workplace, and community contexts. These insights address contemporary leadership challenges including authority and submission, servant leadership, decision-making processes, and accountability structures. The book demonstrates how biblical leadership involves sacrificial service, moral integrity, visionary thinking, and empowering others for ministry and service. Contemporary leaders can apply these principles to lead with humility and wisdom, develop others' potential, create healthy organizational cultures, and use their influence to promote justice and righteousness.</p>
                """)


def generate_book_highlights(book, chapters):
    """Generate key highlights from a book"""
    # Simple highlights based on book
    # In a real implementation, this would be much more detailed and accurate
    highlights = []

    if book == "Genesis":
        highlights = [
            {"reference": "Genesis 1:1", "description": "The foundational statement of God's creative activity", "url": "/book/Genesis/chapter/1#verse-1", "text": get_verse_text("Genesis", 1, 1)},
            {"reference": "Genesis 1:26-27", "description": "Creation of humanity in God's image", "url": "/book/Genesis/chapter/1#verse-26", "text": get_verse_text("Genesis", 1, 26)},
            {"reference": "Genesis 3:15", "description": "First messianic prophecy (the protoevangelium)", "url": "/book/Genesis/chapter/3#verse-15", "text": get_verse_text("Genesis", 3, 15)},
            {"reference": "Genesis 12:1-3", "description": "God's covenant call and promise to Abraham", "url": "/book/Genesis/chapter/12#verse-1", "text": get_verse_text("Genesis", 12, 1)},
            {"reference": "Genesis 22:1-18", "description": "Abraham's faith demonstrated in offering Isaac", "url": "/book/Genesis/chapter/22#verse-1", "text": get_verse_text("Genesis", 22, 1)},
        ]
    elif book == "Exodus":
        highlights = [
            {"reference": "Exodus 3:14", "description": "God's self-revelation as 'I AM WHO I AM'", "url": "/book/Exodus/chapter/3#verse-14", "text": get_verse_text("Exodus", 3, 14)},
            {"reference": "Exodus 12:1-30", "description": "Institution of the Passover", "url": "/book/Exodus/chapter/12#verse-1", "text": get_verse_text("Exodus", 12, 1)},
            {"reference": "Exodus 14:13-31", "description": "Crossing of the Red Sea", "url": "/book/Exodus/chapter/14#verse-13", "text": get_verse_text("Exodus", 14, 13)},
            {"reference": "Exodus 20:1-17", "description": "The Ten Commandments", "url": "/book/Exodus/chapter/20#verse-1", "text": get_verse_text("Exodus", 20, 1)},
            {"reference": "Exodus 25:8", "description": "Command to build the tabernacle", "url": "/book/Exodus/chapter/25#verse-8", "text": get_verse_text("Exodus", 25, 8)},
            {"reference": "Exodus 34:6-7", "description": "Revelation of God's character and attributes", "url": "/book/Exodus/chapter/34#verse-6", "text": get_verse_text("Exodus", 34, 6)}
        ]
    elif book == "Revelation":
        highlights = [
            {"reference": "Revelation 1:8", "description": "God as Alpha and Omega, encompassing all history", "url": "/book/Revelation/chapter/1#verse-8", "text": get_verse_text("Revelation", 1, 8)},
            {"reference": "Revelation 4-5", "description": "Throne room vision with the Lamb who was slain", "url": "/book/Revelation/chapter/4#verse-1", "text": get_verse_text("Revelation", 4, 1)},
            {"reference": "Revelation 12", "description": "Cosmic conflict between the woman and the dragon", "url": "/book/Revelation/chapter/12#verse-1", "text": get_verse_text("Revelation", 12, 1)},
            {"reference": "Revelation 19:11-16", "description": "Christ's return as conquering King", "url": "/book/Revelation/chapter/19#verse-11", "text": get_verse_text("Revelation", 19, 11)},
            {"reference": "Revelation 20:11-15", "description": "Final judgment at the great white throne", "url": "/book/Revelation/chapter/20#verse-11", "text": get_verse_text("Revelation", 20, 11)},
            {"reference": "Revelation 21:1-5", "description": "New heaven and new earth with God dwelling with His people", "url": "/book/Revelation/chapter/21#verse-1", "text": get_verse_text("Revelation", 21, 1)}
        ]
    else:
        # Generate some general highlights based on chapter count
        chapter_count = len(chapters)
        if chapter_count > 0:
            highlights.append({"reference": f"{book} 1:1", "description": "Opening statement establishing key themes", "url": f"/book/{book}/chapter/1#verse-1", "text": get_verse_text(book, 1, 1)})

        if chapter_count > 5:
            highlights.append({"reference": f"{book} {chapter_count//4}:1", "description": "Important development in the book's message", "url": f"/book/{book}/chapter/{chapter_count//4}#verse-1", "text": get_verse_text(book, chapter_count//4, 1)})

        if chapter_count > 10:
            highlights.append({"reference": f"{book} {chapter_count//2}:1", "description": "Central teaching or turning point", "url": f"/book/{book}/chapter/{chapter_count//2}#verse-1", "text": get_verse_text(book, chapter_count//2, 1)})

        if chapter_count > 15:
            highlights.append({"reference": f"{book} {3*chapter_count//4}:1", "description": "Application of key principles", "url": f"/book/{book}/chapter/{3*chapter_count//4}#verse-1", "text": get_verse_text(book, 3*chapter_count//4, 1)})

        if chapter_count > 0:
            highlights.append({"reference": f"{book} {chapter_count}:1", "description": "Concluding summary or final exhortation", "url": f"/book/{book}/chapter/{chapter_count}#verse-1", "text": get_verse_text(book, chapter_count, 1)})

    return highlights


def generate_book_outline(book, chapters):
    """Generate an outline for a book"""
    # Simple outline based on book
    # In a real implementation, this would be much more detailed and accurate

    if book == "Genesis":
        return [
            {
                "title": "Primeval History (1-11)",
                "items": [
                    {"text": "Creation of the universe and humanity", "reference": "Genesis 1-2", "url": "/book/Genesis/chapter/1"},
                    {"text": "Fall and its immediate consequences", "reference": "Genesis 3-5", "url": "/book/Genesis/chapter/3"},
                    {"text": "Judgment of the flood and new beginning", "reference": "Genesis 6-9", "url": "/book/Genesis/chapter/6"},
                    {"text": "Table of nations and tower of Babel", "reference": "Genesis 10-11", "url": "/book/Genesis/chapter/10"}
                ]
            },
            {
                "title": "Abraham Cycle (12-25)",
                "items": [
                    {"text": "Call and covenant promises", "reference": "Genesis 12-15", "url": "/book/Genesis/chapter/12"},
                    {"text": "Covenant confirmation and Sodom's destruction", "reference": "Genesis 16-19", "url": "/book/Genesis/chapter/16"},
                    {"text": "Isaac's birth and testing of Abraham", "reference": "Genesis 20-22", "url": "/book/Genesis/chapter/20"},
                    {"text": "Death of Sarah and marriage of Isaac", "reference": "Genesis 23-25", "url": "/book/Genesis/chapter/23"}
                ]
            },
            {
                "title": "Jacob Cycle (25-36)",
                "items": [
                    {"text": "Jacob and Esau: birth and birthright", "reference": "Genesis 25-27", "url": "/book/Genesis/chapter/25"},
                    {"text": "Jacob's exile and marriages", "reference": "Genesis 28-30", "url": "/book/Genesis/chapter/28"},
                    {"text": "Return to Canaan and reconciliation", "reference": "Genesis 31-33", "url": "/book/Genesis/chapter/31"},
                    {"text": "Dinah incident and covenant renewal", "reference": "Genesis 34-36", "url": "/book/Genesis/chapter/34"}
                ]
            },
            {
                "title": "Joseph Story (37-50)",
                "items": [
                    {"text": "Joseph sold into slavery", "reference": "Genesis 37-38", "url": "/book/Genesis/chapter/37"},
                    {"text": "Joseph's imprisonment and rise to power", "reference": "Genesis 39-41", "url": "/book/Genesis/chapter/39"},
                    {"text": "Brothers' journeys to Egypt and testing", "reference": "Genesis 42-44", "url": "/book/Genesis/chapter/42"},
                    {"text": "Reconciliation and settlement in Egypt", "reference": "Genesis 45-47", "url": "/book/Genesis/chapter/45"},
                    {"text": "Jacob's blessings and death", "reference": "Genesis 48-50", "url": "/book/Genesis/chapter/48"}
                ]
            }
        ]
    elif book == "Exodus":
        return [
            {
                "title": "Israel in Egypt (1-12)",
                "items": [
                    {"text": "Oppression and Moses' birth", "reference": "Exodus 1-2", "url": "/book/Exodus/chapter/1"},
                    {"text": "Moses' call and confrontation with Pharaoh", "reference": "Exodus 3-6", "url": "/book/Exodus/chapter/3"},
                    {"text": "Plagues on Egypt", "reference": "Exodus 7-10", "url": "/book/Exodus/chapter/7"},
                    {"text": "Passover and Exodus", "reference": "Exodus 11-12", "url": "/book/Exodus/chapter/11"}
                ]
            },
            {
                "title": "Journey to Sinai (13-19)",
                "items": [
                    {"text": "Crossing the Red Sea", "reference": "Exodus 13-15", "url": "/book/Exodus/chapter/13"},
                    {"text": "Wilderness provisions and challenges", "reference": "Exodus 16-17", "url": "/book/Exodus/chapter/16"},
                    {"text": "Jethro's advice and arrival at Sinai", "reference": "Exodus 18-19", "url": "/book/Exodus/chapter/18"}
                ]
            },
            {
                "title": "Covenant at Sinai (20-24)",
                "items": [
                    {"text": "Ten Commandments", "reference": "Exodus 20", "url": "/book/Exodus/chapter/20"},
                    {"text": "Book of the Covenant", "reference": "Exodus 21-23", "url": "/book/Exodus/chapter/21"},
                    {"text": "Covenant confirmation", "reference": "Exodus 24", "url": "/book/Exodus/chapter/24"}
                ]
            },
            {
                "title": "Tabernacle Instructions (25-31)",
                "items": [
                    {"text": "Tabernacle furnishings", "reference": "Exodus 25-27", "url": "/book/Exodus/chapter/25"},
                    {"text": "Priesthood and offerings", "reference": "Exodus 28-30", "url": "/book/Exodus/chapter/28"},
                    {"text": "Craftsmen and Sabbath regulations", "reference": "Exodus 31", "url": "/book/Exodus/chapter/31"}
                ]
            },
            {
                "title": "Covenant Violation and Renewal (32-34)",
                "items": [
                    {"text": "Golden calf incident", "reference": "Exodus 32", "url": "/book/Exodus/chapter/32"},
                    {"text": "Moses' intercession", "reference": "Exodus 33", "url": "/book/Exodus/chapter/33"},
                    {"text": "Covenant renewal", "reference": "Exodus 34", "url": "/book/Exodus/chapter/34"}
                ]
            },
            {
                "title": "Tabernacle Construction (35-40)",
                "items": [
                    {"text": "Gathering materials", "reference": "Exodus 35-36", "url": "/book/Exodus/chapter/35"},
                    {"text": "Making furnishings and priestly garments", "reference": "Exodus 37-39", "url": "/book/Exodus/chapter/37"},
                    {"text": "Tabernacle completion and divine glory", "reference": "Exodus 40", "url": "/book/Exodus/chapter/40"}
                ]
            }
        ]
    else:
        # Generate a simple outline based on chapter count
        chapter_count = len(chapters)
        section_count = min(4, max(2, chapter_count // 5))  # Between 2 and 4 sections

        chapters_per_section = chapter_count // section_count
        outline = []

        for i in range(section_count):
            start_chapter = i * chapters_per_section + 1
            end_chapter = min(chapter_count, (i + 1) * chapters_per_section)

            if i == 0:
                title = "Introduction and Background"
            elif i == section_count - 1:
                title = "Conclusion and Final Exhortations"
            else:
                title = f"Main Section {i}"

            items = []
            for j in range(min(4, end_chapter - start_chapter + 1)):
                chapter_num = start_chapter + j
                items.append({
                    "text": f"Chapter {chapter_num}",
                    "reference": f"{book} {chapter_num}",
                    "url": f"/book/{book}/chapter/{chapter_num}"
                })

            outline.append({
                "title": f"{title} ({start_chapter}-{end_chapter})",
                "items": items
            })

        return outline


def generate_book_cross_references(book):
    """Generate cross-references to other books"""
    # Simple cross-references based on book
    # In a real implementation, this would be much more detailed and accurate

    cross_refs = []

    if book == "Genesis":
        cross_refs = [
            {"reference": "John 1:1-3", "url": "/book/John/chapter/1#verse-1", "description": "Echoes Genesis 1:1, revealing Christ's role in creation"},
            {"reference": "Romans 4:1-25", "url": "/book/Romans/chapter/4#verse-1", "description": "Develops Abraham's faith as pattern for justification"},
            {"reference": "Galatians 3:6-29", "url": "/book/Galatians/chapter/3#verse-6", "description": "Connects Abrahamic covenant to salvation in Christ"},
            {"reference": "Hebrews 11:8-22", "url": "/book/Hebrews/chapter/11#verse-8", "description": "Celebrates faith of Abraham, Isaac, Jacob, and Joseph"},
            {"reference": "1 Peter 3:20", "url": "/book/1 Peter/chapter/3#verse-20", "description": "References Noah's flood as type of baptism"}
        ]
    elif book == "Exodus":
        cross_refs = [
            {"reference": "John 1:14-18", "url": "/book/John/chapter/1#verse-14", "description": "The Word 'tabernacled' among us, echoing Exodus 40"},
            {"reference": "1 Corinthians 5:7", "url": "/book/1 Corinthians/chapter/5#verse-7", "description": "Christ as our Passover lamb"},
            {"reference": "Hebrews 9:1-28", "url": "/book/Hebrews/chapter/9#verse-1", "description": "Tabernacle symbolism fulfilled in Christ"},
            {"reference": "1 Peter 2:9-10", "url": "/book/1 Peter/chapter/2#verse-9", "description": "Church as royal priesthood, echoing Exodus 19:5-6"},
            {"reference": "Revelation 15:3", "url": "/book/Revelation/chapter/15#verse-3", "description": "The song of Moses sung in heaven"}
        ]
    elif book == "Revelation":
        cross_refs = [
            {"reference": "Daniel 7:1-28", "url": "/book/Daniel/chapter/7#verse-1", "description": "Provides imagery for beasts and Son of Man"},
            {"reference": "Ezekiel 1:4-28", "url": "/book/Ezekiel/chapter/1#verse-4", "description": "Influences throne room vision"},
            {"reference": "Isaiah 6:1-7", "url": "/book/Isaiah/chapter/6#verse-1", "description": "Parallels heavenly worship scenes"},
            {"reference": "Zechariah 4:1-14", "url": "/book/Zechariah/chapter/4#verse-1", "description": "Background for lampstands imagery"},
            {"reference": "Matthew 24:29-31", "url": "/book/Matthew/chapter/24#verse-29", "description": "Jesus' teaching on His return"}
        ]
    else:
        # Generate basic cross-references based on testament
        testament = get_testament_for_book(book)

        if testament == "Old Testament":
            cross_refs = [
                {"reference": "Matthew 5:17-20", "url": "/book/Matthew/chapter/5#verse-17", "description": "Jesus fulfills the Law and Prophets"},
                {"reference": "Romans 15:4", "url": "/book/Romans/chapter/15#verse-4", "description": "Old Testament written for our instruction"},
                {"reference": "1 Corinthians 10:1-11", "url": "/book/1 Corinthians/chapter/10#verse-1", "description": "Old Testament examples as warnings"},
                {"reference": "2 Timothy 3:16-17", "url": "/book/2 Timothy/chapter/3#verse-16", "description": "Scripture's inspiration and usefulness"},
                {"reference": "Hebrews 1:1-2", "url": "/book/Hebrews/chapter/1#verse-1", "description": "God's revelation in the prophets and in His Son"}
            ]
        else:  # New Testament
            cross_refs = [
                {"reference": "Psalm 110:1-7", "url": "/book/Psalms/chapter/110#verse-1", "description": "Messianic psalm frequently quoted in NT"},
                {"reference": "Isaiah 53:1-12", "url": "/book/Isaiah/chapter/53#verse-1", "description": "Suffering servant prophecy fulfilled in Christ"},
                {"reference": "Daniel 7:13-14", "url": "/book/Daniel/chapter/7#verse-13", "description": "Son of Man receiving everlasting dominion"},
                {"reference": "Joel 2:28-32", "url": "/book/Joel/chapter/2#verse-28", "description": "Prophecy of Spirit's outpouring"},
                {"reference": "Malachi 3:1", "url": "/book/Malachi/chapter/3#verse-1", "description": "Prophecy of messenger preparing the way"}
            ]

    return cross_refs


def generate_chapter_summaries(book, chapters):
    """Generate chapter summaries with key verses"""
    # Simple chapter summaries based on book and chapter count
    # In a real implementation, this would be much more detailed and accurate

    summaries = {}

    # Special case for Genesis 1
    if book == "Genesis" and 1 in chapters:
        summaries[1] = {
            "summary": "God creates the universe, earth, and all living things in six days, culminating with the creation of humanity in His image. Each creative act is pronounced 'good,' with the completed creation declared 'very good.'",
            "key_verses": [
                {
                    "verse_num": 1,
                    "brief": "The foundational declaration of God's creative act",
                    "text": "In the beginning God created the heaven and the earth.",
                    "url": "/book/Genesis/chapter/1#verse-1",
                    "comment": "This opening verse establishes monotheism and God's role as Creator, contrasting with ancient Near Eastern creation myths involving multiple deities and preexisting matter."
                },
                {
                    "verse_num": 26,
                    "brief": "Creation of humans in God's image",
                    "text": "And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth, and over every creeping thing that creepeth upon the earth.",
                    "url": "/book/Genesis/chapter/1#verse-26",
                    "comment": "This verse establishes the unique status of humans as God's image-bearers, with both dignity and responsibility. The plural 'us' has been interpreted variously as divine deliberation, royal plural, or early hint of trinitarian reality."
                },
                {
                    "verse_num": 31,
                    "brief": "God's evaluation of creation as very good",
                    "text": "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day.",
                    "url": "/book/Genesis/chapter/1#verse-31",
                    "comment": "The divine evaluation affirms creation's inherent goodness, establishing that evil comes not from God's creative act but from subsequent corruption. This verse provides the foundation for a positive Christian view of the material world."
                }
            ]
        }

    # Generate simple summaries for all chapters
    for ch in chapters:
        if ch not in summaries:
            # Create a generic summary
            summary = f"Chapter {ch} of {book} continues the narrative with important developments and teachings."

            # Create some generic key verses
            key_verses = []
            if ch > 0:
                key_verses.append({
                    "verse_num": 1,
                    "brief": "Opening verse of the chapter",
                    "text": get_verse_text(book, ch, 1),
                    "url": f"/book/{book}/chapter/{ch}#verse-1",
                    "comment": f"This verse begins chapter {ch} and establishes its context and direction."
                })

                if ch % 2 == 0:  # Add another key verse for even-numbered chapters
                    verse_num = min(ch, 10)
                    key_verses.append({
                        "verse_num": verse_num,
                        "brief": f"Key teaching in verse {verse_num}",
                        "text": f"[Text of {book} {ch}:{verse_num}]",
                        "url": f"/book/{book}/chapter/{ch}#verse-{verse_num}",
                        "comment": f"This verse contains significant content related to the chapter's main themes."
                    })

            summaries[ch] = {
                "summary": summary,
                "key_verses": key_verses
            }

    return summaries
