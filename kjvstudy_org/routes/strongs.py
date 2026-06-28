"""Strong's Concordance routes - Hebrew and Greek word study."""
import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..kjv import bible
from ..strongs import format_strongs_entry, search_strongs, get_all_strongs, normalize_strongs
from ..interlinear_loader import find_verses_by_strongs
from ._templates import templates

router = APIRouter()


# =============================================================================
# Routes
# =============================================================================

@router.get("/concordance")
async def concordance_redirect():
    """Redirect /concordance to /strongs."""
    return RedirectResponse(url="/strongs", status_code=301)


@router.get("/strongs", response_class=HTMLResponse)
async def strongs_index(request: Request, q: str = None):
    """Strong's Concordance search and lookup page."""
    from fastapi.responses import RedirectResponse

    results = []
    if q:
        # Redirect Strong's-number queries (e.g. "H0001" -> /strongs/H1) when found
        normalized = normalize_strongs(q)
        if normalized:
            entry = format_strongs_entry(normalized)
            if entry:
                return RedirectResponse(url=f"/strongs/{normalized}", status_code=302)

        results = search_strongs(q, language="both", limit=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_index.html",
        {
            "query": q or "",
            "results": results,
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/strongs/hebrew", response_class=HTMLResponse)
async def strongs_hebrew_index(request: Request, page: int = 1):
    """Paginated index of all Hebrew Strong's entries."""
    data = get_all_strongs("hebrew", page=page, per_page=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": "Hebrew", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_language_index.html",
        {
            "language": "Hebrew",
            "language_code": "hebrew",
            "entries": data["entries"],
            "page": data["page"],
            "total_pages": data["total_pages"],
            "total": data["total"],
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/strongs/greek", response_class=HTMLResponse)
async def strongs_greek_index(request: Request, page: int = 1):
    """Paginated index of all Greek Strong's entries."""
    data = get_all_strongs("greek", page=page, per_page=100)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": "Greek", "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_language_index.html",
        {
            "language": "Greek",
            "language_code": "greek",
            "entries": data["entries"],
            "page": data["page"],
            "total_pages": data["total_pages"],
            "total": data["total"],
            "books": books,
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/strongs/{strongs_number}", response_class=HTMLResponse)
async def strongs_entry(request: Request, strongs_number: str):
    """View a single Strong's concordance entry."""
    entry = format_strongs_entry(strongs_number)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Strong's number '{strongs_number}' not found"
        )

    # Find all verses containing this Strong's number
    verse_occurrences = find_verses_by_strongs(strongs_number, limit=10000)
    total_occurrences = len(verse_occurrences)

    # Fetch full verse text for each occurrence and highlight the word
    for occ in verse_occurrences:
        verse_text = bible.get_verse_text(occ["book"], occ["chapter"], occ["verse"])
        if verse_text:
            # Highlight the English word in the verse text
            english_word = occ.get("english", "")
            if english_word and english_word in verse_text:
                occ["verse_text"] = verse_text.replace(
                    english_word,
                    f'<mark>{english_word}</mark>',
                    1  # Only highlight first occurrence
                )
            else:
                occ["verse_text"] = verse_text
        else:
            occ["verse_text"] = ""

    # Extract and fetch related Strong's entries from derivation
    related_entries = []
    if entry.get("derivation"):
        # Find all Strong's references like H1234 or G5678
        strongs_refs = re.findall(r'([HG])(\d+)', entry["derivation"])
        seen = set()
        for prefix, num in strongs_refs:
            ref = f"{prefix}{num}"
            if ref.upper() != strongs_number.upper() and ref not in seen:
                seen.add(ref)
                related = format_strongs_entry(ref)
                if related:
                    related_entries.append(related)

    books = bible.get_books()
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Strong's Concordance", "url": "/strongs"},
        {"text": strongs_number.upper(), "url": None}
    ]

    return templates.TemplateResponse(
        request,
        "strongs_entry.html",
        {
            "entry": entry,
            "books": books,
            "breadcrumbs": breadcrumbs,
            "verse_occurrences": verse_occurrences,
            "total_occurrences": total_occurrences,
            "related_entries": related_entries
        }
    )
