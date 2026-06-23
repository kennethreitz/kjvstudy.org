"""Bible routes - book, chapter, verse, and interlinear views."""
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse

from ..kjv import bible
from ..cross_references import get_cross_references
from ..interlinear_loader import get_interlinear_data, has_interlinear_data
from ..books import get_book_data, has_book_data
from ..utils.books import normalize_book_name, OT_BOOKS, get_canonical_book_order
from ..utils.helpers import create_slug, get_related_content, get_chapter_popularity_score, get_chapter_popularity_explanation
from ..utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf_async
from ..utils.poetry_loader import is_poetry_chapter, get_stanza_breaks


@lru_cache(maxsize=1)
def _load_section_headings():
    """Load section headings data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "section_headings.json"
    if data_path.exists():
        with open(data_path) as f:
            return json.load(f)
    return {}


def get_section_headings(book: str, chapter: int) -> dict:
    """Get section headings for a specific chapter.

    Returns dict mapping verse number (int) to heading text.
    """
    headings_data = _load_section_headings()
    chapter_headings = headings_data.get(book, {}).get(str(chapter), {})
    # Convert string keys to int for easier template use
    return {int(k): v for k, v in chapter_headings.items()}

router = APIRouter()

from ._templates import templates


# Import these from commentary route to avoid circular imports
generate_commentary = None
generate_chapter_overview = None
generate_book_commentary = None
generate_word_study_sidenotes = None


def init_commentary_functions(commentary_func, chapter_overview_func, book_commentary_func, word_study_func):
    """Initialize commentary functions."""
    global generate_commentary, generate_chapter_overview, generate_book_commentary, generate_word_study_sidenotes
    generate_commentary = commentary_func
    generate_chapter_overview = chapter_overview_func
    generate_book_commentary = book_commentary_func
    generate_word_study_sidenotes = word_study_func


# =============================================================================
# Book Routes
# =============================================================================

@router.get("/book/{book}", response_class=HTMLResponse)
async def read_book(request: Request, book: str):
    """Display a Bible book overview with chapter listing."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}", status_code=301)

    books = bible.get_books()
    chapters = bible.get_chapters_for_book(book)

    if not chapters:
        raise HTTPException(
            status_code=404,
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )

    # Generate commentary data for the book page
    commentary_data = generate_book_commentary(book, chapters)

    # Calculate popularity scores for each chapter
    chapter_popularity = {}
    chapter_explanations = {}
    for chapter in chapters:
        chapter_popularity[chapter] = get_chapter_popularity_score(book, chapter)
        chapter_explanations[chapter] = get_chapter_popularity_explanation(book, chapter)

    # Get book introduction data if available
    book_intro = get_book_data(book) if has_book_data(book) else None

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "book.html",
        {
            "book": book,
            "chapters": chapters,
            "books": books,
            "chapter_popularity": chapter_popularity,
            "chapter_explanations": chapter_explanations,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "book_intro": book_intro,
            **commentary_data
        },
    )


@router.get("/book/{book}/pdf")
async def book_pdf(request: Request, book: str):
    """Generate a PDF export for an entire Bible book."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/pdf", status_code=301)

    chapters = bible.get_chapters_for_book(book)
    if not chapters:
        raise HTTPException(
            status_code=404,
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )

    chapters_data = []
    total_verses = 0
    for chapter_num in chapters:
        verses = bible.get_verses_by_book_chapter(book, chapter_num)
        if not verses:
            continue
        total_verses += len(verses)
        chapter_is_poetry = is_poetry_chapter(book, chapter_num)
        chapters_data.append({
            "chapter": chapter_num,
            "verses": verses,
            "section_headings": get_section_headings(book, chapter_num),
            "stanza_breaks": get_stanza_breaks(book, chapter_num) if chapter_is_poetry else set(),
            "is_poetry": chapter_is_poetry
        })

    if not chapters_data:
        raise HTTPException(
            status_code=404,
            detail=f"No verses found for the book '{book}'."
        )

    # Get book introduction data if available
    book_intro = get_book_data(book) if has_book_data(book) else None

    html_content = templates.get_template("book_pdf.html").render(
        book=book,
        chapters=chapters_data,
        chapter_count=len(chapters_data),
        verse_count=total_verses,
        book_intro=book_intro,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(book)}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/book/{book}/commentary")
def book_commentary_redirect(book: str):
    """Redirect old book commentary URLs to book page"""
    return RedirectResponse(url=f"/book/{book}", status_code=301)


@router.get("/book/{book}/{chapter}")
def redirect_chapter_legacy(book: str, chapter: int):
    """Redirect legacy chapter URLs to correct format"""
    return RedirectResponse(url=f"/book/{book}/chapter/{chapter}", status_code=301)


# =============================================================================
# Chapter Routes
# =============================================================================

@router.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
async def read_chapter(request: Request, book: str, chapter: int):
    """Display a Bible chapter with commentary."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Generate AI commentary for the chapter (two-pass for lookahead)
    commentaries = {}
    recent_words = {}  # Track {word: verse_num} for cooldown
    seen_words = set()  # Track words shown for first-occurrence expansion
    cooldown_verses = 5  # Don't repeat same word within 5 verses

    # First pass: collect all data
    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)
        # Filter out words shown recently (within cooldown period)
        excluded_words = {w for w, v in recent_words.items() if verse.verse - v < cooldown_verses}
        # Add word study sidenotes
        word_studies = generate_word_study_sidenotes(verse.text, book, chapter, verse.verse, excluded_words)
        # Mark first occurrence of each word as auto-expanded
        for study in word_studies:
            word_lower = study['word'].lower()
            if word_lower not in seen_words:
                study['auto_expand'] = True
                seen_words.add(word_lower)
            else:
                study['auto_expand'] = False
            recent_words[word_lower] = verse.verse
        commentary['word_studies'] = word_studies

        # Add cross-references
        cross_refs = get_cross_references(book, chapter, verse.verse)
        if cross_refs:
            # Group cross-references by their description/note
            grouped_refs = defaultdict(list)
            for ref in cross_refs:
                description = ref['note'] if ref['note'] else 'Related'
                # Parse the reference to build URL
                if ' ' in ref['ref'] and ':' in ref['ref']:
                    ref_book = ref['ref'].rsplit(' ', 1)[0]
                    ref_chapter_verse = ref['ref'].rsplit(' ', 1)[1]
                    ref_chapter = ref_chapter_verse.split(':')[0]
                    ref_verse = ref_chapter_verse.split(':')[1]
                    # Same chapter: use anchor link; different chapter/book: link to chapter view with anchor
                    if ref_book == book and ref_chapter == str(chapter):
                        url = f"#verse-{ref_verse}"
                    else:
                        url = f"/book/{ref_book}/chapter/{ref_chapter}#verse-{ref_verse}"
                else:
                    ref_book = None
                    ref_chapter_verse = ref['ref']
                    url = '#'
                grouped_refs[description].append({
                    'text': ref['ref'],
                    'url': url,
                    'book': ref_book,
                    'chapter_verse': ref_chapter_verse
                })
            # Priority ordering for note types (lower = higher priority)
            note_priority = {
                'Prophecy': 1,
                'Covenant': 1,
                'Fulfillment': 1,
                'References Jesus': 2,
                'References Christ': 2,
                'Resurrection': 2,
                'Salvation': 2,
                'References Lord': 3,
                'References God': 3,
                'Kingdom': 3,
                'Faith': 3,
                'Grace': 3,
                'Judgment': 3,
                'Parallel theme': 5,  # Generic - lower priority
            }
            # Sort refs: same book first, then by note priority, then canonical order, then chapter:verse numerically
            book_order = get_canonical_book_order()
            def parse_cv(cv):
                """Parse '3:14' into (3, 14) for numeric sorting."""
                try:
                    parts = cv.split(':')
                    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
                except (ValueError, IndexError):
                    return (999, 999)
            for desc, refs in grouped_refs.items():
                priority = note_priority.get(desc, 4)  # Default priority for unlisted notes
                refs.sort(key=lambda r: (0 if r['book'] == book else 1, book_order.get(r['book'], 999), parse_cv(r['chapter_verse'])))
            # Condense refs: show book only when it changes
            for desc, refs in grouped_refs.items():
                last_book = None
                for r in refs:
                    if r['book'] == last_book:
                        r['display'] = r['chapter_verse']  # Just "1:20"
                    else:
                        r['display'] = r['text']  # Full "Revelation 1:20"
                        last_book = r['book']
            # Sort groups by note priority
            sorted_groups = sorted(grouped_refs.items(), key=lambda x: note_priority.get(x[0], 4))
            commentary['cross_reference_groups'] = [
                {'description': desc, 'refs': refs}
                for desc, refs in sorted_groups
            ]
        else:
            commentary['cross_reference_groups'] = []

        commentaries[verse.verse] = commentary

    # Cross-refs: expand if next verse is long (more margin space), collapse if short
    verse_list = [v for v in verses]
    for i, verse in enumerate(verse_list):
        commentary = commentaries.get(verse.verse)
        if not commentary:
            continue
        if commentary.get('cross_reference_groups'):
            # Check next verse length - long verse = more margin room
            next_verse = verse_list[i + 1] if i + 1 < len(verse_list) else None
            next_verse_len = len(next_verse.text) if next_verse else 0
            # Expand if next verse is 120+ chars (provides margin space)
            commentary['xref_auto_expand'] = next_verse_len >= 120

    # Generate chapter overview
    chapter_overview = generate_chapter_overview(book, chapter, verses)

    # Get related content for internal linking
    related_content = get_related_content(book, chapter)

    # Get section headings for this chapter
    section_headings = get_section_headings(book, chapter)

    # Get poetry formatting info
    is_poetry = is_poetry_chapter(book, chapter)
    stanza_breaks = get_stanza_breaks(book, chapter) if is_poetry else set()

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "chapter.html",
        {
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
            "commentaries": commentaries,
            "chapter_overview": chapter_overview,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "related_content": related_content,
            "section_headings": section_headings,
            "is_poetry": is_poetry,
            "stanza_breaks": stanza_breaks
        }
    )


@router.get("/book/{book}/chapter/{chapter}/pdf")
async def chapter_pdf(request: Request, book: str, chapter: int):
    """Generate a PDF export for a specific Bible chapter."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/pdf", status_code=301)

    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        raise HTTPException(
            status_code=404,
            detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
        )

    # Generate commentaries with cross-references and word studies for PDF
    commentaries = {}
    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)
        # Add word study sidenotes
        word_studies = generate_word_study_sidenotes(verse.text, book, chapter, verse.verse, for_pdf=True)
        commentary['word_studies'] = word_studies

        # Add cross-references grouped by description
        cross_refs = get_cross_references(book, chapter, verse.verse)
        grouped_refs = defaultdict(list)
        for ref in cross_refs:
            description = ref['note'] if ref['note'] else 'Related'
            # Parse the reference to extract book and chapter:verse
            if ' ' in ref['ref'] and ':' in ref['ref']:
                ref_book = ref['ref'].rsplit(' ', 1)[0]
                ref_chapter_verse = ref['ref'].rsplit(' ', 1)[1]
            else:
                ref_book = None
                ref_chapter_verse = ref['ref']
            grouped_refs[description].append({
                'text': ref['ref'],
                'book': ref_book,
                'chapter_verse': ref_chapter_verse
            })

        # Sort and condense refs: same book first, then canonical order, then chapter:verse numerically
        book_order = get_canonical_book_order()
        def parse_chapter_verse(cv):
            """Parse '3:14' into (3, 14) for numeric sorting."""
            try:
                parts = cv.split(':')
                return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
            except (ValueError, IndexError):
                return (999, 999)
        for desc, refs in grouped_refs.items():
            refs.sort(key=lambda r: (0 if r['book'] == book else 1, book_order.get(r['book'], 999), parse_chapter_verse(r['chapter_verse'])))
            # Condense: show book only when it changes
            last_book = None
            for r in refs:
                if r['book'] == last_book:
                    r['display'] = r['chapter_verse']
                else:
                    r['display'] = r['text']
                    last_book = r['book']

        # Pass all cross-refs (PDF has more space)
        commentary['cross_reference_groups'] = [
            {'description': desc, 'refs': [r['display'] for r in refs]}
            for desc, refs in grouped_refs.items()
        ]
        commentaries[verse.verse] = commentary

    # Get book metadata for richer PDF
    book_data = get_book_data(book)
    total_chapters = len(chapters)

    # Collect all unique word studies shown for glossary
    glossary = []
    seen_words = set()
    for verse_num, commentary in commentaries.items():
        for study in commentary.get('word_studies', []):
            word_lower = study['word'].lower()
            if word_lower not in seen_words:
                seen_words.add(word_lower)
                glossary.append(study)
    glossary.sort(key=lambda x: x['word'])

    # Get section headings for this chapter
    section_headings = get_section_headings(book, chapter)

    # Get poetry formatting info
    is_poetry = is_poetry_chapter(book, chapter)
    stanza_breaks = get_stanza_breaks(book, chapter) if is_poetry else set()

    html_content = templates.get_template("chapter_pdf.html").render(
        book=book,
        chapter=chapter,
        verses=verses,
        verse_count=len(verses),
        commentaries=commentaries,
        book_data=book_data,
        total_chapters=total_chapters,
        glossary=glossary,
        section_headings=section_headings,
        is_poetry=is_poetry,
        stanza_breaks=stanza_breaks,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(book)}-chapter-{chapter}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# =============================================================================
# Interlinear Routes
# =============================================================================

@router.get("/book/{book}/chapter/{chapter}/interlinear/pdf")
async def chapter_interlinear_pdf(book: str, chapter: int):
    """Generate PDF export for interlinear chapter view."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/interlinear/pdf", status_code=301)

    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(status_code=404, detail=f"The book '{book}' was not found.")
        else:
            raise HTTPException(status_code=404, detail=f"Chapter {chapter} of {book} was not found.")

    # Get interlinear data for each verse
    verses_with_interlinear = []
    for verse in verses:
        interlinear_words = get_interlinear_data(book, chapter, verse.verse)
        verses_with_interlinear.append({
            'verse': verse,
            'interlinear_words': interlinear_words or []
        })

    # Determine if OT or NT for language badge
    is_old_testament = book in OT_BOOKS

    html_content = templates.get_template("chapter_interlinear_pdf.html").render(
        book=book,
        chapter=chapter,
        verses_with_interlinear=verses_with_interlinear,
        is_old_testament=is_old_testament
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{book.lower().replace(' ', '-')}-{chapter}-interlinear.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/book/{book}/chapter/{chapter}/interlinear", response_class=HTMLResponse)
async def read_chapter_interlinear(request: Request, book: str, chapter: int):
    """Display a chapter with interlinear Hebrew/Greek for every verse"""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/interlinear", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Get interlinear data for each verse
    verses_with_interlinear = []
    for verse in verses:
        interlinear_words = get_interlinear_data(book, chapter, verse.verse)
        verses_with_interlinear.append({
            'verse': verse,
            'interlinear_words': interlinear_words or []
        })

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": f"/book/{book}/chapter/{chapter}"},
        {"text": "Interlinear", "url": None}
    ]

    # Determine if OT or NT for language badge
    is_old_testament = book in OT_BOOKS

    return templates.TemplateResponse(
        request,
        "chapter_interlinear.html",
        {
            "book": book,
            "chapter": chapter,
            "verses_with_interlinear": verses_with_interlinear,
            "books": books,
            "chapters": chapters,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "is_old_testament": is_old_testament,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/book/{book}/chapter/{chapter}/interlinear/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


# =============================================================================
# Verse Routes
# =============================================================================

@router.get("/book/{book}/chapter/{chapter}/verse/{verse_num}/pdf")
async def verse_pdf(book: str, chapter: int, verse_num: int):
    """Generate PDF export for a single verse with commentary."""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/verse/{verse_num}/pdf", status_code=301)

    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    verses = bible.get_verses_by_book_chapter(book, chapter)
    if not verses:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter} of {book} was not found.")

    # Find the specific verse
    verse = None
    for v in verses:
        if v.verse == verse_num:
            verse = v
            break

    if not verse:
        raise HTTPException(status_code=404, detail=f"Verse {verse_num} not found in {book} {chapter}.")

    # Generate commentary
    try:
        commentary = generate_commentary(book, chapter, verse)
    except Exception:
        commentary = None

    # Get cross-references
    cross_refs = get_cross_references(book, chapter, verse_num)

    # Get interlinear data
    interlinear_words = get_interlinear_data(book, chapter, verse_num)

    # Determine if OT
    is_ot = book in OT_BOOKS

    html_content = templates.get_template("verse_pdf.html").render(
        book=book,
        chapter=chapter,
        verse_num=verse_num,
        verse_text=verse.text,
        commentary=commentary,
        cross_references=cross_refs,
        interlinear_words=interlinear_words,
        is_old_testament=is_ot
    )
    pdf_buffer = await render_html_to_pdf_async(html_content)

    filename = f"{book.lower().replace(' ', '-')}-{chapter}-{verse_num}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/book/{book}/chapter/{chapter}/verse/{verse_num}", response_class=HTMLResponse)
async def read_verse(request: Request, book: str, chapter: int, verse_num: int):
    """Display a single verse with detailed commentary"""
    # Redirect book name variations to canonical form
    canonical_name = normalize_book_name(book)
    if canonical_name:
        return RedirectResponse(url=f"/book/{canonical_name}/chapter/{chapter}/verse/{verse_num}", status_code=301)

    books = bible.get_books()
    verses = bible.get_verses_by_book_chapter(book, chapter)
    chapters = bible.get_chapters_for_book(book)

    if not verses:
        # Check if the book exists first
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Chapter {chapter} of {book} was not found. This book has {len(chapters)} chapters."
            )

    # Find the specific verse
    verse = None
    for v in verses:
        if v.verse == verse_num:
            verse = v
            break

    if not verse:
        raise HTTPException(
            status_code=404,
            detail=f"Verse {verse_num} not found in {book} {chapter}. This chapter has {len(verses)} verses."
        )

    # Generate commentary for this verse
    try:
        commentary = generate_commentary(book, chapter, verse)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error generating commentary for {book} {chapter}:{verse_num}: {e}")
        commentary = None

    # Get cross-references for this verse
    cross_refs = get_cross_references(book, chapter, verse_num)

    # Check if interlinear data is available and load it
    has_interlinear = has_interlinear_data(book, chapter, verse_num)
    interlinear_words = get_interlinear_data(book, chapter, verse_num) if has_interlinear else None

    # Get related content for internal linking
    related_content = get_related_content(book, chapter, verse_num)

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Books", "url": "/books"},
        {"text": book, "url": f"/book/{book}"},
        {"text": f"Chapter {chapter}", "url": f"/book/{book}/chapter/{chapter}"},
        {"text": f"Verse {verse_num}", "url": None}
    ]

    # Determine if Old Testament for interlinear styling
    is_ot = book in OT_BOOKS

    return templates.TemplateResponse(
        request,
        "verse.html",
        {
            "book": book,
            "chapter": chapter,
            "verse_num": verse_num,
            "verse_text": verse.text,
            "commentary": commentary,
            "cross_references": cross_refs,
            "total_verses": len(verses),
            "books": books,
            "chapters": chapters,
            "breadcrumbs": breadcrumbs,
            "current_book": book,
            "current_chapter": chapter,
            "current_verse": verse_num,
            "has_interlinear": has_interlinear,
            "interlinear_words": interlinear_words,
            "related_content": related_content,
            "is_old_testament": is_ot,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/book/{book}/chapter/{chapter}/verse/{verse_num}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )
