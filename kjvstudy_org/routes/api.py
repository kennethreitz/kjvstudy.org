"""API routes for KJV Study - JSON endpoints for programmatic access."""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import JSONResponse

from ..kjv import bible
from ..cross_references import get_cross_references
from ..reading_plans import get_plan, get_plan_summary
from ..topics import get_all_topics, get_topic
from ..interlinear_loader import get_interlinear_data, has_interlinear_data
from ..utils.books import normalize_book_name, OT_BOOKS
from ..utils.search import perform_full_text_search
from ..utils.helpers import get_daily_verse

router = APIRouter(prefix="/api", tags=["API"])


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
            "reading_plan": "/api/reading-plans/{plan_id}"
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
    q: str = Query(..., description="Search query", example="faith"),
    limit: Optional[int] = Query(None, description="Max results", example=10)
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


@router.get("/verse-of-the-day")
def verse_of_the_day_api():
    """API endpoint for verse of the day."""
    return get_daily_verse()


@router.get("/verse/{book}/{chapter}/{verse}")
def api_get_verse(
    book: str = Path(..., description="Book name", example="John"),
    chapter: int = Path(..., description="Chapter number", example=3),
    verse: int = Path(..., description="Verse number", example=16)
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
    book: str = Path(..., description="Book name", example="Psalms"),
    chapter: int = Path(..., description="Chapter number", example=23),
    start: int = Path(..., description="Starting verse number", example=1),
    end: int = Path(..., description="Ending verse number", example=6)
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
    book: str = Path(..., description="Book name", example="John"),
    chapter: int = Path(..., description="Chapter number", example=1),
    verse: int = Path(..., description="Verse number", example=1)
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
def api_get_book(book: str = Path(..., description="Book name", example="Genesis")):
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
        "chapters": chapter_details
    }


@router.get("/books/{book}/chapters/{chapter}")
def api_get_chapter(
    book: str = Path(..., description="Book name", example="Romans"),
    chapter: int = Path(..., description="Chapter number", example=8)
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
        "verses": verse_list
    }


@router.get("/books/{book}/text")
def api_get_book_text(book: str = Path(..., description="Book name", example="Philemon")):
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
    book: str = Path(..., description="Book name", example="John"),
    chapter: int = Path(..., description="Chapter number", example=3),
    verse: int = Path(..., description="Verse number", example=16)
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
def api_get_topic(topic_name: str = Path(..., description="Topic name", example="faith")):
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
def api_get_reading_plan(plan_id: str = Path(..., description="Reading plan ID", example="chronological")):
    """Get details about a specific reading plan."""
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Reading plan not found")

    return plan
