"""Passage study workspace routes."""
import re
from urllib.parse import quote

from ..kjv import bible
from ..cross_references import get_cross_references
from ..interlinear_loader import get_interlinear_data
from ..commentary_gen import (
    generate_chapter_overview,
    generate_commentary,
    generate_word_study_sidenotes,
)
from ..utils.books import normalize_book_name
from ..utils.helpers import get_related_content
from ._helpers import abort_404, redirect, render
from .bible import group_cross_references, _CROSS_REF_NOTE_PRIORITY


_REFERENCE_PATTERNS = (
    re.compile(r"^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$"),
    re.compile(r"^(.+?)\s+(\d+)\s+(\d+)(?:-(\d+))?$"),
    re.compile(r"^(.+?)\s+(\d+)$"),
)


def _canonical_book(book: str):
    candidate = normalize_book_name(book) or book
    return candidate if candidate in bible.get_books() else None


def parse_study_reference(reference: str):
    """Parse a chapter or passage reference for the study workspace."""
    cleaned = " ".join((reference or "").strip().split())
    if not cleaned:
        return None

    for pattern in _REFERENCE_PATTERNS:
        match = pattern.match(cleaned)
        if not match:
            continue

        book = _canonical_book(match.group(1))
        if not book:
            return None

        chapter = int(match.group(2))
        verse_start = (
            int(match.group(3))
            if match.lastindex and match.lastindex >= 3 and match.group(3)
            else None
        )
        verse_end = (
            int(match.group(4))
            if match.lastindex and match.lastindex >= 4 and match.group(4)
            else None
        )

        if verse_start is not None and verse_end is not None and verse_start > verse_end:
            return None

        return book, chapter, verse_start, verse_end

    return None


def _study_url(book: str, chapter: int, verse_start=None, verse_end=None):
    book_part = quote(book)
    if verse_start is None:
        return f"/study/{book_part}/{chapter}"
    if verse_end is None or verse_end == verse_start:
        return f"/study/{book_part}/{chapter}/{verse_start}"
    return f"/study/{book_part}/{chapter}/{verse_start}/{verse_end}"


def _passage_label(book: str, chapter: int, verse_start=None, verse_end=None):
    if verse_start is None:
        return f"{book} {chapter}"
    if verse_end is None or verse_end == verse_start:
        return f"{book} {chapter}:{verse_start}"
    return f"{book} {chapter}:{verse_start}-{verse_end}"


def _build_study_rows(book: str, chapter: int, verses):
    rows = []
    recent_words = {}
    seen_words = set()
    cooldown_verses = 5

    for verse in verses:
        commentary = generate_commentary(book, chapter, verse)

        excluded_words = {
            word
            for word, previous_verse in recent_words.items()
            if verse.verse - previous_verse < cooldown_verses
        }
        word_studies = generate_word_study_sidenotes(
            verse.text, book, chapter, verse.verse, excluded_words
        )
        for study in word_studies:
            word_lower = study["word"].lower()
            study["auto_expand"] = word_lower not in seen_words
            seen_words.add(word_lower)
            recent_words[word_lower] = verse.verse

        cross_refs = get_cross_references(book, chapter, verse.verse)
        grouped_refs = group_cross_references(cross_refs, book, chapter, build_urls=True)
        sorted_groups = sorted(
            grouped_refs.items(),
            key=lambda item: _CROSS_REF_NOTE_PRIORITY.get(item[0], 4),
        )

        interlinear_words = get_interlinear_data(book, chapter, verse.verse) or []
        has_commentary = bool(
            commentary
            and (
                commentary.get("analysis")
                or commentary.get("historical")
                or commentary.get("theological")
                or commentary.get("questions")
            )
        )

        rows.append({
            "verse": verse,
            "reference": f"{book} {chapter}:{verse.verse}",
            "commentary": commentary,
            "has_commentary": has_commentary,
            "word_studies": word_studies,
            "cross_reference_groups": [
                {"description": desc, "refs": refs}
                for desc, refs in sorted_groups
            ],
            "interlinear_preview": interlinear_words[:12],
            "interlinear_count": len(interlinear_words),
        })

    return rows


def _render_landing(req, resp, *, query="", error=None):
    render(
        req, resp, "study_workspace.html",
        books=bible.get_books(),
        breadcrumbs=[{"text": "Home", "url": "/"}, {"text": "Study", "url": None}],
        query=query,
        error=error,
        workspace=None,
    )


def _render_workspace(req, resp, *, book, chapter, verse_start=None, verse_end=None):
    canonical = _canonical_book(book)
    if canonical and canonical != book:
        redirect(resp, _study_url(canonical, chapter, verse_start, verse_end), 301)
        return

    chapters = bible.get_chapters_for_book(book)
    if not chapters:
        abort_404(req, resp, f"The book '{book}' was not found.")
        return

    chapter_verses = bible.get_verses_by_book_chapter(book, chapter)
    if not chapter_verses:
        abort_404(req, resp, f"Chapter {chapter} of {book} was not found.")
        return

    if verse_start is None:
        selected_verses = chapter_verses
        verse_end = None
    else:
        if verse_end is None:
            verse_end = verse_start
        if verse_start > verse_end:
            abort_404(req, resp, "The requested passage range was not found.")
            return
        selected_verses = [
            verse for verse in chapter_verses
            if verse_start <= verse.verse <= verse_end
        ]

    if not selected_verses:
        abort_404(req, resp, "The requested passage range was not found.")
        return

    label = _passage_label(book, chapter, verse_start, verse_end)
    rows = _build_study_rows(book, chapter, selected_verses)

    workspace = {
        "book": book,
        "chapter": chapter,
        "verse_start": verse_start,
        "verse_end": verse_end,
        "label": label,
        "url": _study_url(book, chapter, verse_start, verse_end),
        "chapter_url": f"/book/{quote(book)}/chapter/{chapter}",
        "interlinear_url": f"/book/{quote(book)}/chapter/{chapter}/interlinear",
        "rows": rows,
        "verse_count": len(selected_verses),
        "chapter_overview": generate_chapter_overview(book, chapter, chapter_verses),
        "related_content": get_related_content(book, chapter),
    }

    render(
        req, resp, "study_workspace.html",
        books=bible.get_books(),
        breadcrumbs=[
            {"text": "Home", "url": "/"},
            {"text": "Study", "url": "/study"},
            {"text": label, "url": None},
        ],
        query=label,
        error=None,
        workspace=workspace,
    )


def register(api):
    @api.route("/study")
    async def study_landing(req, resp):
        query = (req.params.get("q") or "").strip()
        if query:
            parsed = parse_study_reference(query)
            if parsed:
                book, chapter, verse_start, verse_end = parsed
                redirect(resp, _study_url(book, chapter, verse_start, verse_end), 302)
                return
            _render_landing(req, resp, query=query, error="Reference not found")
            return

        _render_landing(req, resp)

    @api.route("/study/{book}/{chapter:int}")
    async def study_chapter(req, resp, *, book, chapter):
        _render_workspace(req, resp, book=book, chapter=chapter)

    @api.route("/study/{book}/{chapter:int}/{verse_start:int}")
    async def study_single_verse(req, resp, *, book, chapter, verse_start):
        _render_workspace(
            req, resp,
            book=book, chapter=chapter, verse_start=verse_start
        )

    @api.route("/study/{book}/{chapter:int}/{verse_start:int}/{verse_end:int}")
    async def study_passage(req, resp, *, book, chapter, verse_start, verse_end):
        _render_workspace(
            req, resp,
            book=book, chapter=chapter,
            verse_start=verse_start, verse_end=verse_end
        )
