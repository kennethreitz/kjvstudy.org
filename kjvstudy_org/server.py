from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path

from .kjv import bible


app = FastAPI(
    title="KJV Study - Bible Commentary Platform",
    description="Study the King James Bible with AI-powered commentary and insights",
    version="1.0.0"
)

# Set up Jinja2 templates and static files
current_dir = Path(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom error handler that renders our error template"""
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
            status_code=exc.status_code,
        )
    
    # For other errors, use the default handler
    return await http_exception_handler(request, exc)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    books = list(bible.iter_books())

    return templates.TemplateResponse(
        "index.html", {"request": request, "books": books}
    )


@app.get("/book/{book}", response_class=HTMLResponse)
def read_book(request: Request, book: str):
    books = list(bible.iter_books())
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

    if not chapters:
        raise HTTPException(
            status_code=404, 
            detail=f"The book '{book}' was not found. Please check the spelling or browse all available books."
        )
    return templates.TemplateResponse(
        "book.html",
        {"request": request, "book": book, "chapters": chapters, "books": books},
    )


@app.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
def read_chapter(request: Request, book: str, chapter: int):
    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]
    chapters = [ch for bk, ch in bible.iter_chapters() if bk == book]

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
    
    return templates.TemplateResponse(
        "chapter.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
            "chapters": chapters,
        },
    )


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "kjv-study"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
