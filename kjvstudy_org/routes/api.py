"""API routes for KJV Study - JSON endpoints for programmatic access."""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Path
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import JSONResponse, StreamingResponse

from ..utils.pdf import render_html_to_pdf, WEASYPRINT_AVAILABLE

from ..kjv import bible
from ..cross_references import get_cross_references
from ..reading_plans import get_plan, get_plan_summary
from ..topics import get_all_topics, get_topic
from ..interlinear_loader import get_interlinear_data, has_interlinear_data
from ..utils.books import normalize_book_name, OT_BOOKS
from ..utils.search import perform_full_text_search
from ..utils.helpers import get_daily_verse, create_slug
from ..stories import (
    get_categories,
    get_story_by_slug,
    get_story_count,
    get_category_count,
    get_all_stories_flat,
)

router = APIRouter(prefix="/api", tags=["API"])

# Templates will be set by the main app
templates = None


def init_templates(app_templates):
    """Initialize templates from the main app."""
    global templates
    templates = app_templates


@router.get("/")
def api_index():
    """API index with links to documentation and available endpoints."""
    return {
        "name": "KJV Study API",
        "version": "1.0.0",
        "description": "RESTful API for accessing King James Bible verses and study resources",
        "documentation": {
            "swagger_ui": "/api/docs",
            "redoc": "/api/redoc",
            "openapi_json": "/api/openapi.json"
        },
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search?q={query}",
            "verse_of_the_day": "/api/verse-of-the-day",
            "verse": "/api/verse/{book}/{chapter}/{verse}",
            "verse_range": "/api/verse-range/{book}/{chapter}/{start}/{end}",
            "interlinear": "/api/interlinear/{book}/{chapter}/{verse}",
            "books": "/api/books",
            "book": "/api/books/{book}",
            "chapter": "/api/books/{book}/chapters/{chapter}",
            "book_text": "/api/books/{book}/text",
            "bible": "/api/bible",
            "cross_references": "/api/cross-references/{book}/{chapter}/{verse}",
            "topics": "/api/topics",
            "topic": "/api/topics/{topic_name}",
            "reading_plans": "/api/reading-plans",
            "reading_plan": "/api/reading-plans/{plan_id}",
            "stories": "/api/stories",
            "story": "/api/stories/{slug}"
        }
    }


@router.get("/health")
def api_health_check():
    """API health check endpoint for monitoring and status verification."""
    return {
        "status": "healthy",
        "service": "KJV Study API",
        "version": "1.0.0"
    }


@router.get("/search")
def search_api(
    q: str = Query(..., description="Search query", examples=["faith"]),
    limit: Optional[int] = Query(None, description="Max results", examples=[10])
):
    """JSON API endpoint for search."""
    if not q or len(q.strip()) < 2:
        return {"query": q, "results": [], "total": 0}

    results = perform_full_text_search(q.strip(), limit)
    is_direct_verse = False

    # Check if this was a direct verse reference match
    if results and len(results) == 1 and results[0].get("score") == 100.0:
        is_direct_verse = True

    return {
        "query": q,
        "results": results,
        "total": len(results),
        "is_direct_verse": is_direct_verse
    }


@router.get("/universal-search")
def universal_search_api(
    q: str = Query(..., description="Search query", examples=["love"]),
    limit: int = Query(5, description="Max results per category", examples=[5])
):
    """Universal search across all content types."""
    if not q or len(q.strip()) < 2:
        return {"query": q, "results": {}}

    query = q.strip().lower()
    results = {}

    # Search Bible books
    all_books = bible.get_books()
    matching_books = [
        {"name": book, "url": f"/book/{book}"}
        for book in all_books
        if query in book.lower()
    ][:limit]
    if matching_books:
        results["books"] = matching_books

    # Search Bible verses (limit to top results for speed)
    verse_results = perform_full_text_search(q.strip(), limit)
    if verse_results:
        results["verses"] = [
            {
                "reference": r["reference"],
                "text": r["text"][:100] + "..." if len(r.get("text", "")) > 100 else r.get("text", ""),
                "url": f"/book/{r['book']}/chapter/{r['chapter']}/verse/{r['verse']}"
            }
            for r in verse_results
        ]

    # Search topics
    all_topics = get_all_topics()
    matching_topics = [
        {"name": name.replace("_", " ").title(), "url": f"/topics/{name}"}
        for name, data in all_topics.items()
        if query in name.lower() or query in data.get("description", "").lower()
    ][:limit]
    if matching_topics:
        results["topics"] = matching_topics

    # Search stories
    all_stories = get_all_stories_flat()
    matching_stories = [
        {
            "title": s["title"],
            "url": f"/stories/{s['slug']}",
            "category": s.get("category_name", "")
        }
        for s in all_stories
        if query in s.get("title", "").lower() or query in s.get("description", "").lower()
    ][:limit]
    if matching_stories:
        results["stories"] = matching_stories

    # Search reading plans
    from ..reading_plans import READING_PLANS
    matching_plans = [
        {"name": plan["name"], "url": f"/reading-plans/{plan_id}"}
        for plan_id, plan in READING_PLANS.items()
        if query in plan["name"].lower() or query in plan.get("description", "").lower()
    ][:limit]
    if matching_plans:
        results["plans"] = matching_plans

    return {"query": q, "results": results}


@router.get("/verse-of-the-day")
def verse_of_the_day_api():
    """API endpoint for verse of the day."""
    return get_daily_verse()


@router.get("/verse/{book}/{chapter}/{verse}")
def api_get_verse(
    book: str = Path(..., description="Book name", examples=["John"]),
    chapter: int = Path(..., description="Chapter number", examples=[3]),
    verse: int = Path(..., description="Verse number", examples=[16])
):
    """Get a single verse text."""
    try:
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            raise HTTPException(status_code=404, detail="Verse not found")

        return JSONResponse({
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verse-range/{book}/{chapter}/{start}/{end}")
def api_get_verse_range(
    book: str = Path(..., description="Book name", examples=["Psalms"]),
    chapter: int = Path(..., description="Chapter number", examples=[23]),
    start: int = Path(..., description="Starting verse number", examples=[1]),
    end: int = Path(..., description="Ending verse number", examples=[6])
):
    """Get a range of verses."""
    try:
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verses = []
        verse_texts = []

        for verse_num in range(start, end + 1):
            verse_text = bible.get_verse_text(book, chapter, verse_num)
            if verse_text:
                verses.append({
                    "verse": verse_num,
                    "text": verse_text
                })
                verse_texts.append(verse_text)

        if not verses:
            raise HTTPException(status_code=404, detail="Verse range not found")

        return JSONResponse({
            "book": book,
            "chapter": chapter,
            "start": start,
            "end": end,
            "reference": f"{book} {chapter}:{start}-{end}",
            "verses": verses,
            "text": " ".join(verse_texts)
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interlinear/{book}/{chapter}/{verse}")
def api_get_interlinear(
    book: str = Path(..., description="Book name", examples=["John"]),
    chapter: int = Path(..., description="Chapter number", examples=[1]),
    verse: int = Path(..., description="Verse number", examples=[1])
):
    """Get interlinear (word-by-word) data for a verse."""
    try:
        canonical_name = normalize_book_name(book)
        if canonical_name:
            book = canonical_name

        verse_text = bible.get_verse_text(book, chapter, verse)
        if not verse_text:
            raise HTTPException(status_code=404, detail="Verse not found")

        if not has_interlinear_data(book, chapter, verse):
            return JSONResponse({
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "reference": f"{book} {chapter}:{verse}",
                "text": verse_text,
                "interlinear_available": False,
                "words": []
            })

        interlinear_words = get_interlinear_data(book, chapter, verse)

        return JSONResponse({
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "reference": f"{book} {chapter}:{verse}",
            "text": verse_text,
            "interlinear_available": True,
            "words": interlinear_words
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/books")
def api_get_books():
    """Get list of all Bible books."""
    books = list(bible.iter_books())

    old_testament = []
    new_testament = []

    for book in books:
        chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
        book_info = {
            "name": book,
            "chapters": len(chapters),
            "testament": "Old Testament" if book in OT_BOOKS else "New Testament"
        }

        if book in OT_BOOKS:
            old_testament.append(book_info)
        else:
            new_testament.append(book_info)

    return {
        "total_books": len(books),
        "old_testament": old_testament,
        "new_testament": new_testament
    }


@router.get("/books/{book}")
def api_get_book(book: str = Path(..., description="Book name", examples=["Genesis"])):
    """Get details about a specific book."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
    if not chapters:
        raise HTTPException(status_code=404, detail="Book not found")

    chapter_details = []
    for chapter in chapters:
        verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
        chapter_details.append({
            "chapter": chapter,
            "verses": len(verses)
        })

    return {
        "name": book,
        "total_chapters": len(chapters),
        "chapters": chapter_details,
        "links": {
            "pdf": f"/api/books/{book}/pdf"
        }
    }


@router.get("/books/{book}/pdf")
def api_book_pdf(book: str = Path(..., description="Book name", examples=["Genesis"])):
    """Generate PDF for an entire Bible book."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]
    if not chapters:
        raise HTTPException(status_code=404, detail="Book not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Prepare data for template
    chapters_data = []
    total_verses = 0
    for chapter in chapters:
        verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
        if verses:
            chapter_verses = []
            for v in verses:
                chapter_verses.append({
                    "verse": v.verse,
                    "text": v.text
                })
            chapters_data.append({
                "chapter": chapter,
                "verses": chapter_verses
            })
            total_verses += len(verses)

    if not chapters_data:
        raise HTTPException(status_code=404, detail="No verses found for this book")

    # Render the PDF template
    html_content = templates.get_template("book_pdf.html").render(
        book=book,
        chapters=chapters_data,
        chapter_count=len(chapters_data),
        verse_count=total_verses,
    )

    # Generate PDF
    pdf_buffer = render_html_to_pdf(html_content)

    # Return as downloadable PDF
    filename = f"{create_slug(book)}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/books/{book}/chapters/{chapter}")
def api_get_chapter(
    book: str = Path(..., description="Book name", examples=["Romans"]),
    chapter: int = Path(..., description="Chapter number", examples=[8])
):
    """Get all verses in a chapter."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")

    verse_list = []
    for v in verses:
        verse_list.append({
            "verse": v.verse,
            "text": v.text
        })

    return {
        "book": book,
        "chapter": chapter,
        "total_verses": len(verses),
        "verses": verse_list,
        "links": {
            "pdf": f"/api/books/{book}/chapters/{chapter}/pdf"
        }
    }


@router.get("/books/{book}/chapters/{chapter}/pdf")
def api_chapter_pdf(
    book: str = Path(..., description="Book name", examples=["Romans"]),
    chapter: int = Path(..., description="Chapter number", examples=[8])
):
    """Generate PDF for a specific Bible chapter."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Prepare data for template
    verse_list = []
    for v in verses:
        verse_list.append({
            "verse": v.verse,
            "text": v.text
        })

    # Render the PDF template
    html_content = templates.get_template("chapter_pdf.html").render(
        book=book,
        chapter=chapter,
        verses=verse_list,
        verse_count=len(verses),
    )

    # Generate PDF
    pdf_buffer = render_html_to_pdf(html_content)

    # Return as downloadable PDF
    filename = f"{create_slug(book)}-chapter-{chapter}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/books/{book}/text")
def api_get_book_text(book: str = Path(..., description="Book name", examples=["Philemon"])):
    """Get all text content of a book."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verses = [v for v in bible.iter_verses() if v.book == book]
    if not verses:
        raise HTTPException(status_code=404, detail="Book not found")

    chapters = {}
    for v in verses:
        if v.chapter not in chapters:
            chapters[v.chapter] = []
        chapters[v.chapter].append({
            "verse": v.verse,
            "text": v.text
        })

    chapter_list = []
    for chapter_num in sorted(chapters.keys()):
        chapter_list.append({
            "chapter": chapter_num,
            "verses": chapters[chapter_num]
        })

    return {
        "book": book,
        "total_chapters": len(chapters),
        "total_verses": len(verses),
        "chapters": chapter_list
    }


@router.get("/bible")
def api_get_bible():
    """Get the entire Bible text."""
    books_data = {}
    for v in bible.iter_verses():
        if v.book not in books_data:
            books_data[v.book] = {}
        if v.chapter not in books_data[v.book]:
            books_data[v.book][v.chapter] = []
        books_data[v.book][v.chapter].append({
            "verse": v.verse,
            "text": v.text
        })

    books_list = []
    for book_name in books_data:
        chapter_list = []
        for chapter_num in sorted(books_data[book_name].keys()):
            chapter_list.append({
                "chapter": chapter_num,
                "verses": books_data[book_name][chapter_num]
            })

        books_list.append({
            "book": book_name,
            "chapters": chapter_list
        })

    total_verses = sum(len(books_data[book][ch]) for book in books_data for ch in books_data[book])

    return {
        "total_books": len(books_data),
        "total_verses": total_verses,
        "books": books_list
    }


@router.get("/cross-references/{book}/{chapter}/{verse}")
def api_get_cross_references(
    book: str = Path(..., description="Book name", examples=["John"]),
    chapter: int = Path(..., description="Chapter number", examples=[3]),
    verse: int = Path(..., description="Verse number", examples=[16])
):
    """Get cross-references for a verse."""
    canonical_name = normalize_book_name(book)
    if canonical_name:
        book = canonical_name

    verse_text = bible.get_verse_text(book, chapter, verse)
    if not verse_text:
        raise HTTPException(status_code=404, detail="Verse not found")

    cross_refs = get_cross_references(book, chapter, verse)

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "reference": f"{book} {chapter}:{verse}",
        "cross_references": cross_refs
    }


@router.get("/topics")
def api_get_topics():
    """Get list of all topics."""
    topics = get_all_topics()

    topic_list = []
    for topic_name, topic_data in topics.items():
        topic_list.append({
            "name": topic_name,
            "slug": topic_name,
            "description": topic_data.get("description", ""),
            "subtopics": list(topic_data.get("subtopics", {}).keys())
        })

    return {
        "total_topics": len(topics),
        "topics": topic_list
    }


@router.get("/topics/{topic_name}")
def api_get_topic(topic_name: str = Path(..., description="Topic name", examples=["faith"])):
    """Get details about a specific topic."""
    topic = get_topic(topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    return {
        "name": topic_name,
        "description": topic.get("description", ""),
        "overview": topic.get("overview", ""),
        "subtopics": topic.get("subtopics", {})
    }


@router.get("/reading-plans")
def api_get_reading_plans():
    """Get list of all reading plans."""
    plans = get_plan_summary()

    return {
        "total_plans": len(plans),
        "plans": plans
    }


@router.get("/reading-plans/{plan_id}")
def api_get_reading_plan(plan_id: str = Path(..., description="Reading plan ID", examples=["chronological"])):
    """Get details about a specific reading plan."""
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    return plan


@router.get("/stories")
def api_get_stories():
    """Get list of all Bible stories organized by category."""
    categories = get_categories()
    story_count = get_story_count()
    category_count = get_category_count()

    # Format categories for API response
    categories_list = []
    for category in categories:
        stories_list = []
        for story in category.get("stories", []):
            stories_list.append({
                "title": story.get("title"),
                "slug": story.get("slug"),
                "description": story.get("description"),
                "verses": story.get("verses", []),
                "characters": story.get("characters", []),
                "themes": story.get("themes", []),
                "kids_title": story.get("kids_title"),
                "kids_description": story.get("kids_description"),
                "has_kids_version": bool(story.get("kids_narrative"))
            })
        categories_list.append({
            "category": category.get("category"),
            "slug": category.get("slug"),
            "description": category.get("description"),
            "story_count": len(stories_list),
            "stories": stories_list
        })

    return {
        "total_stories": story_count,
        "total_categories": category_count,
        "categories": categories_list
    }


@router.get("/stories/{slug}")
def api_get_story(slug: str = Path(..., description="Story slug", examples=["creation-of-the-world"])):
    """Get a specific Bible story by slug."""
    story = get_story_by_slug(slug)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return {
        "title": story.get("title"),
        "slug": story.get("slug"),
        "description": story.get("description"),
        "category": story.get("category_name"),
        "category_slug": story.get("category_slug"),
        "verses": story.get("verses", []),
        "characters": story.get("characters", []),
        "themes": story.get("themes", []),
        "narrative": story.get("narrative"),
        "kids_title": story.get("kids_title"),
        "kids_description": story.get("kids_description"),
        "kids_narrative": story.get("kids_narrative"),
        "has_kids_version": bool(story.get("kids_narrative")),
        "links": {
            "web": f"/stories/{slug}",
            "kids_web": f"/stories/{slug}/kids" if story.get("kids_narrative") else None,
            "pdf": f"/api/stories/{slug}/pdf",
            "kids_pdf": f"/api/stories/{slug}/kids/pdf" if story.get("kids_narrative") else None
        }
    }


@router.get("/stories/{slug}/pdf")
def api_story_pdf(slug: str = Path(..., description="Story slug")):
    """Generate PDF for a story (adult version)."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Render the PDF template
    html_content = templates.get_template("story_pdf.html").render(story=story)

    # Generate PDF
    pdf_buffer = render_html_to_pdf(html_content)

    # Return as downloadable PDF
    filename = f"{slug}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/stories/{slug}/kids/pdf")
def api_story_kids_pdf(slug: str = Path(..., description="Story slug")):
    """Generate PDF for a story (kids version)."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    story = get_story_by_slug(slug)

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if not story.get("kids_narrative"):
        raise HTTPException(status_code=404, detail="Kids version not available for this story")

    if not templates:
        raise HTTPException(status_code=500, detail="Templates not initialized")

    # Render the PDF template
    html_content = templates.get_template("story_kids_pdf.html").render(story=story)

    # Generate PDF
    pdf_buffer = render_html_to_pdf(html_content)

    # Return as downloadable PDF
    filename = f"{slug}-kids.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
