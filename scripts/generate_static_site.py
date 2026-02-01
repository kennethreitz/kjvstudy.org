#!/usr/bin/env python3
"""Static site generator for kjvstudy.org.

Pre-renders high-traffic HTML pages (~1,300) using FastAPI's TestClient.
Everything else is served by the FastAPI sidecar at runtime.
"""

import argparse
import json
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def create_app():
    from kjvstudy_org.server import app
    return app


def get_test_client(app):
    from fastapi.testclient import TestClient
    return TestClient(app, raise_server_exceptions=False)


def enumerate_urls():
    """Enumerate high-traffic HTML pages only (~1,300 URLs).

    Covers: homepage, book listing, 66 book pages, ~1,189 chapter pages,
    and a handful of top-level resource/about pages.
    """
    from kjvstudy_org.kjv import bible

    urls = [
        "/",
        "/books",
        "/resources",
        "/about",
        "/about/stats",
        "/about/cross-references",
        "/about/accessibility",
        "/about/commentary",
        "/topics",
        "/reading-plans",
        "/study-guides",
        "/stories",
        "/stories/kids",
        "/strongs",
        "/strongs/hebrew",
        "/strongs/greek",
        "/interlinear",
        "/family-tree",
        "/biblical-timeline",
        "/biblical-maps",
        "/red-letter",
        "/stars",
    ]

    # 66 book pages + ~1,189 chapter pages
    for book in bible.get_books():
        urls.append(f"/book/{book}")
        for chapter in bible.get_chapters_for_book(book):
            urls.append(f"/book/{book}/chapter/{chapter}")

    return urls


def url_to_filepath(output_dir: Path, url: str) -> Path:
    path = url.strip("/")
    if path == "":
        return output_dir / "index.html"
    return output_dir / path / "index.html"


def render_url(client, output_dir: Path, url: str) -> tuple[str, bool, str]:
    try:
        filepath = url_to_filepath(output_dir, url)
        response = client.get(url)

        if response.status_code >= 400:
            return (url, False, f"HTTP {response.status_code}")

        if response.status_code in (301, 302, 307, 308):
            location = response.headers.get("location", "/")
            redirect_html = (
                f'<!DOCTYPE html><html><head>'
                f'<meta http-equiv="refresh" content="0;url={location}">'
                f'<link rel="canonical" href="{location}">'
                f'</head><body><a href="{location}">Redirecting...</a></body></html>'
            )
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(redirect_html, encoding="utf-8")
            return (url, True, "redirect")

        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)
        return (url, True, "ok")

    except Exception as e:
        return (url, False, str(e)[:200])


def generate_random_verse_page(output_dir: Path):
    """Generate /random-verse as a client-side JS page + verse-list JSON."""
    from kjvstudy_org.kjv import bible

    verse_urls = []
    for book in bible.get_books():
        for chapter in bible.get_chapters_for_book(book):
            for v in bible.get_verses_by_book_chapter(book, chapter):
                verse_urls.append(f"/book/{book}/chapter/{chapter}/verse/{v.verse}")

    json_path = output_dir / "random-verse-list.json"
    json_path.write_text(json.dumps(verse_urls), encoding="utf-8")

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>Random Verse - KJV Study</title>
    <link rel="stylesheet" href="/static/tufte.css"/>
    <link rel="stylesheet" href="/static/style.css"/>
</head>
<body>
    <article>
        <h1>Random Verse</h1>
        <p style="font-style:italic;color:#666">Picking a random verse&hellip;</p>
    </article>
    <script>
    fetch('/random-verse-list.json')
        .then(function(r){return r.json()})
        .then(function(vs){window.location.replace(vs[Math.floor(Math.random()*vs.length)])})
        .catch(function(){window.location.replace('/book/John/chapter/3/verse/16')});
    </script>
</body>
</html>"""

    html_path = output_dir / "random-verse" / "index.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    print(f"  Random verse page + {len(verse_urls)} verse list written")


def generate_utility_files(client, output_dir: Path):
    for url, filename in [
        ("/robots.txt", "robots.txt"),
        ("/sitemap.xml", "sitemap.xml"),
        ("/sitemap-main.xml", "sitemap-main.xml"),
        ("/sitemap-verses.xml", "sitemap-verses.xml"),
    ]:
        resp = client.get(url)
        if resp.status_code == 200:
            (output_dir / filename).write_bytes(resp.content)
            print(f"  {filename}")


def copy_static_assets(output_dir: Path):
    src = PROJECT_ROOT / "kjvstudy_org" / "static"
    dst = output_dir / "static"
    if dst.exists():
        shutil.rmtree(dst)
    skip = {"search_index.db", "scofield_commentary.json"}
    shutil.copytree(src, dst, ignore=lambda d, files: [f for f in files if f in skip])
    print(f"  Static assets copied to {dst}")


def main():
    parser = argparse.ArgumentParser(description="Generate static HTML site for kjvstudy.org")
    parser.add_argument("--output", "-o", default="dist", help="Output directory")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Parallel workers")
    parser.add_argument("--dry-run", action="store_true", help="Enumerate URLs without rendering")
    args = parser.parse_args()

    output_dir = Path(args.output).resolve()

    print("Static site generator for kjvstudy.org")
    print(f"Output: {output_dir}")
    print(f"Workers: {args.workers}")
    print()

    print("Initializing FastAPI app...")
    app = create_app()
    client = get_test_client(app)
    client.__enter__()

    try:
        print("Enumerating URLs...")
        all_urls = enumerate_urls()
        print(f"  Total: {len(all_urls)} HTML pages")

        if args.dry_run:
            print("\nDry run — not rendering.")
            return

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

        print("\nCopying static assets...")
        copy_static_assets(output_dir)

        print("\nGenerating utility files...")
        generate_utility_files(client, output_dir)

        print("\nGenerating random verse page...")
        generate_random_verse_page(output_dir)

        print(f"\nRendering {len(all_urls)} HTML pages...")
        start = time.time()
        ok = 0
        fail = 0
        errors = []

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(render_url, client, output_dir, u): u for u in all_urls}
            done = 0
            for future in as_completed(futures):
                done += 1
                url, success, msg = future.result()
                if success:
                    ok += 1
                else:
                    fail += 1
                    errors.append((url, msg))

                if done % 200 == 0 or done == len(all_urls):
                    elapsed = time.time() - start
                    rate = done / elapsed if elapsed > 0 else 0
                    print(f"  [{done}/{len(all_urls)}] {rate:.0f}/sec  errors={fail}")

        elapsed = time.time() - start
        print(f"\nDone in {elapsed:.1f}s")
        print(f"  Success: {ok}")
        print(f"  Errors:  {fail}")

        if errors:
            print(f"\nErrors:")
            for url, msg in errors[:20]:
                print(f"  {url}: {msg}")

    finally:
        client.__exit__(None, None, None)


if __name__ == "__main__":
    main()
