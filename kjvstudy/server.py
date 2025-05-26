from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .kjv import bible


app = FastAPI()

# Set up Jinja2 templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse(
        "book.html",
        {"request": request, "book": book, "chapters": chapters, "books": books},
    )


@app.get("/book/{book}/chapter/{chapter}", response_class=HTMLResponse)
def read_chapter(request: Request, book: str, chapter: int):
    books = list(bible.iter_books())
    verses = [v for v in bible.iter_verses() if v.book == book and v.chapter == chapter]

    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return templates.TemplateResponse(
        "chapter.html",
        {
            "request": request,
            "book": book,
            "chapter": chapter,
            "verses": verses,
            "books": books,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
