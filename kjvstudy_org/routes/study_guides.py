"""Study guides routes for KJV Study.

This module contains the study guides routes and content.
"""
import json
from pathlib import Path
from functools import lru_cache
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from ..kjv import bible
from ..utils.helpers import verse_reference_to_url
from ..utils.pdf import WEASYPRINT_AVAILABLE, pdf_response, require_pdf_available

router = APIRouter(tags=["Study Guides"])

from ._templates import templates

# Path to study guides directory
_STUDY_GUIDES_DIR = Path(__file__).parent.parent / "data" / "study_guides"


@lru_cache(maxsize=1)
def _load_study_guides():
    """Load study guides from per-guide JSON files. Cached since data never changes."""
    guides_dir = _STUDY_GUIDES_DIR
    catalog = {}
    content = {}

    for path in sorted(guides_dir.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        guide_content = payload.get("content")
        if not guide_content or "slug" not in guide_content:
            continue

        slug = guide_content["slug"]
        content[slug] = guide_content

        catalog_entry = payload.get("catalog_entry")
        category = payload.get("category", "Uncategorized")
        if catalog_entry:
            catalog.setdefault(category, []).append(catalog_entry)

    return {"catalog": catalog, "content": content}


def get_books():
    """Get list of Bible books."""
    return bible.get_books()


def _get_study_guides_catalog():
    """Return the study guide catalog grouped by category."""
    data = _load_study_guides()
    return data["catalog"]


def _get_study_guides_content():
    """Return full study guide detail content."""
    data = _load_study_guides()
    return data["content"]


def _attach_verse_texts(guide: dict):
    """Populate verse text data for each section in a guide."""
    for section in guide.get("sections", []):
        verse_texts = []
        for verse_ref in section.get("verses", []):
            try:
                verse_text = None
                parts = verse_ref.split(" ")
                if len(parts) >= 2:
                    book = " ".join(parts[:-1])
                    chapter_verse = parts[-1]
                    if ":" in chapter_verse:
                        if "-" in chapter_verse:
                            chapter, verse_range = chapter_verse.split(":")
                            start_verse, end_verse = verse_range.split("-")
                            verse_text = ""
                            for v in range(int(start_verse), int(end_verse) + 1):
                                text = bible.get_verse_text(book, int(chapter), v)
                                if text:
                                    verse_text += f"[{v}] {text} "
                        else:
                            chapter, verse = chapter_verse.split(":")
                            verse_text = bible.get_verse_text(book, int(chapter), int(verse))
                    else:
                        chapter = int(chapter_verse)
                        verse_text = f"(See {book} {chapter})"

                if verse_text:
                    verse_texts.append({
                        "reference": verse_ref,
                        "text": verse_text,
                        "url": verse_reference_to_url(verse_ref) or "#"
                    })
                else:
                    verse_texts.append({
                        "reference": verse_ref,
                        "text": f"(See {verse_ref})",
                        "url": verse_reference_to_url(verse_ref) or "#"
                    })
            except Exception as exc:
                print(f"Error parsing verse {verse_ref}: {exc}")
                verse_texts.append({
                    "reference": verse_ref,
                    "text": f"(See {verse_ref})",
                    "url": "#"
                })

        section["verse_texts"] = verse_texts



@router.get("/study-guides", response_class=HTMLResponse)
async def study_guides_page(request: Request):
    """Study guides main page"""
    books = get_books()

    # Define study guide categories
    study_guides = _get_study_guides_catalog()

    # Process verse references to add URLs
    for category in study_guides.values():
        for guide in category:
            guide['verse_refs'] = [
                {
                    'text': verse,
                    'url': verse_reference_to_url(verse) or '#'
                }
                for verse in guide['verses']
            ]

    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Study Guides", "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "study_guides.html",
            {
            "books": books,
            "study_guides": study_guides,
            "breadcrumbs": breadcrumbs
        }
    )

@router.get("/study-guides/{slug}", response_class=HTMLResponse)
async def study_guide_detail(request: Request, slug: str):
    """Individual study guide page"""
    books = get_books()

    # Study guide content
    guides_content = _get_study_guides_content()

    if slug not in guides_content:
        raise HTTPException(status_code=404, detail="Study guide not found")

    guide = guides_content[slug]

    _attach_verse_texts(guide)

    # Build breadcrumbs
    breadcrumbs = [
        {"text": "Home", "url": "/"},
        {"text": "Study Guides", "url": "/study-guides"},
        {"text": guide["title"], "url": None}
    ]

    return templates.TemplateResponse(
            request,
            "study_guide_detail.html",
            {
            "books": books,
            "guide": guide,
            "breadcrumbs": breadcrumbs,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": f"/study-guides/{slug}/pdf" if WEASYPRINT_AVAILABLE else None
        }
    )


@router.get("/study-guides/{slug}/pdf")
async def study_guide_pdf(slug: str):
    """Generate a PDF export for a study guide."""
    require_pdf_available()

    guides_content = _get_study_guides_content()
    guide = guides_content.get(slug)
    if not guide:
        raise HTTPException(status_code=404, detail="Study guide not found")

    _attach_verse_texts(guide)

    html_content = templates.get_template("study_guide_pdf.html").render(guide=guide)
    filename = f"{slug}.pdf"
    return await pdf_response(html_content, filename)
