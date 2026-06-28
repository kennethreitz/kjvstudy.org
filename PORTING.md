# Porting kjvstudy.org from FastAPI to Responder

Status: **scaffold + vertical slice complete and verified.** This document is the
working plan for finishing the migration of the web layer from FastAPI
(`kjvstudy_org/server.py` + `kjvstudy_org/routes/*`) to
[Responder](https://responder.kennethreitz.org) (`kjvstudy_org/responder_app.py`).

All non-web modules (`kjv`, `topics`, `commentary` generation, `red_letter`,
`cross_references`, `reading_plans`, `strongs`, `interlinear_loader`,
`resource_catalog`, `stories`, `study_guides`, `utils/*` except `utils/pdf`) are
framework-agnostic and are reused unchanged.

## How to run each app

```bash
# FastAPI (current production app) — uses the pinned Starlette in pyproject
uv run uvicorn kjvstudy_org.server:app --reload
uv run pytest tests/            # 941 tests, all green

# Responder (the port) — needs Responder + its newer Starlette
uv run --with ~/repos/responder python -m kjvstudy_org.responder_app
uv run --with ~/repos/responder python -c "from kjvstudy_org.responder_app import api; print(api.session().get('/').status_code)"
```

## ⚠️ The hard constraint: Starlette version conflict

**Responder 4.0.0 requires Starlette 1.3.x; FastAPI requires the older
0.4x line.** They cannot be installed in the same synced environment. Practical
consequences:

- The package `__init__.py` no longer force-imports `server` (FastAPI) — importing
  `kjvstudy_org` must not drag in a web framework. Import `kjvstudy_org.server` or
  `kjvstudy_org.responder_app` explicitly.
- Run Responder with `uv run --with ~/repos/responder ...` so it gets its own
  Starlette without touching the project's locked deps. Plain `uv run` keeps the
  FastAPI environment intact.
- **This is a "big-bang" cutover at the dependency layer.** Once `responder` is
  added to `pyproject.toml` as a hard dependency, FastAPI (and the current
  FastAPI-based test suite) stop importing. So the test suite must be ported in
  lockstep with the final cutover (see "Tests" below). Until then we keep both
  runnable side by side via the `--with` trick.

## The handler transformation

FastAPI returns a response; Responder mutates `resp`. Path params are keyword-only
args; query params come from `req.params`.

```python
# BEFORE (FastAPI) — kjvstudy_org/routes/bible.py
@router.get("/book/{book}", response_class=HTMLResponse)
async def read_book(request: Request, book: str):
    books = bible.get_books()
    return templates.TemplateResponse(request, "book.html", {"book": book, "books": books})

# AFTER (Responder) — kjvstudy_org/responder_app.py (or a ported route module)
@api.route("/book/{book}")
async def read_book(req, resp, *, book):
    render(req, resp, "book.html", book=book, books=bible.get_books())
```

Key equivalences:

| FastAPI | Responder |
|---|---|
| `@router.get("/p/{x}")` `async def h(request, x: int)` | `@api.route("/p/{x:int}")` `async def h(req, resp, *, x)` |
| `request.query_params.get("q")` | `req.params.get("q")` |
| `return templates.TemplateResponse(request, "t.html", ctx)` | `render(req, resp, "t.html", **ctx)` |
| `return {"k": v}` (auto-JSON) | `resp.media = {"k": v}` |
| `return HTMLResponse(html)` | `resp.html = html` |
| `return RedirectResponse(url, 301)` | `resp.redirect(url, status_code=301)` |
| `raise HTTPException(404, detail)` | `resp.status_code = 404` + render error |
| `response_model=Model` (Pydantic) | `@api.route(..., response_model=Model)` — **supported** |
| query validation `param: int = Query(...)` | `@api.route(..., params_model=PydanticModel)` → `req.state.validated_params` |

`render(req, resp, name, **ctx)` (defined in `responder_app.py`) is the shared
template helper — Responder doesn't auto-inject the request the way Starlette's
`TemplateResponse` does, and our templates use `request.url.path`, so it passes
`request=req`.

## Cross-cutting concerns

- **Templating**: `register_filters(api.templates._env)` reuses every custom Jinja
  filter; globals (`static_hash`, `disable_analytics`, `resource_pdf_available`,
  `github_repo_url`) are set on the same env. ✅ done in `responder_app.py`.
- **Static files**: `responder.API(static_dir=..., static_route="/static")`. ✅
- **OpenAPI / docs**: `openapi="3.0.2"`, `docs_route="/api/docs"`,
  `openapi_route="/api/openapi.json"`. ✅ (TODO: filter the schema to `/api/*` only,
  as `server.custom_openapi` does.)
- **Cache-Control**: ported to an `@api.after_request()` hook. ✅
- **Other middleware** (TODO): `BotLoggerMiddleware`, `RateLimitMiddleware`,
  `TimeoutMiddleware`, GZip. GZip is a built-in `responder.API(gzip=True)` option;
  the others port to `api.add_middleware(...)` (they are plain Starlette
  `BaseHTTPMiddleware` and should move with minimal change) or `before_request`
  hooks.
- **Custom 404 → error.html** (TODO): Responder's `Router.default_endpoint` expects
  a raw ASGI callable, not a `(req, resp)` view. Wire via `Router(default_response=...)`
  or a catch-all route. See the TODO in `responder_app.py`.

## Business-logic extraction (the real work)

Several `routes/*.py` modules mix framework-agnostic data logic with FastAPI
handlers. Because the route modules construct an `APIRouter` at import time (which
fails under Responder's Starlette), that shared logic must be pulled into
framework-agnostic modules first, then imported by both web layers.

- ✅ **Example done**: study-guide data (`_load_study_guides`,
  `get_featured_study_guides`, catalog/content accessors) moved from
  `routes/study_guides.py` to top-level `kjvstudy_org/study_guides.py`;
  `routes/study_guides.py` re-imports them.
- **TODO**: `routes/commentary.py` exposes `generate_commentary`,
  `generate_chapter_overview`, `generate_book_commentary`,
  `generate_word_study_sidenotes` (injected into `bible.py` via
  `init_bible_commentary`). Extract the generators into a framework-agnostic
  module (e.g. `kjvstudy_org/commentary_gen.py`).
- **TODO**: `utils/pdf.py` imports `fastapi.HTTPException` /
  `fastapi.responses.StreamingResponse`. Re-implement on Responder
  (`resp.file(...)` / Starlette responses) so PDF routes port cleanly.
- **TODO**: the `init_*` dependency-injection shims (`init_bible_commentary`,
  `init_search_family_tree`) exist only to break FastAPI import cycles; with the
  generators extracted they can become plain imports.

## Route-module checklist (266 handlers)

Port each module to Responder routes (web modules) or `response_model` routes (API).
Order is low-risk-first; `resources.py` last because it's large but mostly
helper-driven (the C3/C10 DRY helpers mean its ~155 routes can be registered in a
loop over the resource catalog rather than hand-written).

- [x] `main.py` (3) — homepage, /books, /resources  ✅ in `responder_app.py`
- [x] health  ✅
- [ ] `utility.py` (5) — sitemap.xml, robots.txt, /health, accessibility, about-claude
- [ ] `about.py` (5)
- [ ] `topics.py` (3)
- [ ] `reading_plans.py` (3)
- [ ] `timeline.py` (2)
- [ ] `stories.py` (6)
- [ ] `strongs.py` (5)
- [ ] `study_guides.py` (3) — data layer already extracted
- [ ] `family_tree.py` (9)
- [ ] `commentary.py` (2) — after extracting the generators
- [ ] `bible.py` (10) — book/chapter/verse/interlinear (+ PDF, needs utils/pdf port)
- [ ] `misc.py` (13) — search, OG images, red-letter, verse-of-the-day, random
- [ ] `api.py` (42) — JSON API; use `response_model=` / `params_model=` Pydantic
- [ ] `resources.py` (155) — drive from `resource_catalog`; register in a loop

## Tests

The current suite uses `TestClient(kjvstudy_org.server.app)`. Responder exposes the
same Starlette `TestClient` via `api.session()`, so most assertions port directly —
swap the app fixture and adjust a handful of FastAPI-specific expectations
(validation error shapes, OpenAPI JSON layout). Port the test fixtures alongside the
final dependency cutover.
