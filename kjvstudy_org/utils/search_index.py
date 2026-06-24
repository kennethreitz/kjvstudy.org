"""
SQLite FTS5 search index for fast Bible verse search.

This module provides a full-text search index using SQLite's FTS5 extension,
enabling efficient searches across all 31,102 Bible verses.
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from contextlib import contextmanager

from ..kjv import bible
from .books import OT_BOOKS

# Database location - store in static directory alongside other data
DB_PATH = Path(__file__).parent.parent / "static" / "search_index.db"


@contextmanager
def get_connection():
    """
    Get a database connection with proper cleanup and thread safety.

    Creates a new connection for each request instead of using a global connection.
    This is thread-safe and works well with FastAPI's concurrent request handling.
    SQLite connection creation is very fast (~microseconds), so this is efficient.
    """
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_search_index(force_rebuild: bool = False) -> bool:
    """
    Initialize the FTS5 search index.

    Creates the database and populates it with all Bible verses if it doesn't exist.
    Returns True if the index was created/rebuilt, False if it already existed.
    """
    if DB_PATH.exists() and not force_rebuild:
        return False

    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Remove old database if rebuilding
    if DB_PATH.exists():
        DB_PATH.unlink()

    with get_connection() as conn:
        cursor = conn.cursor()

        # Create FTS5 virtual table for full-text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS verses_fts USING fts5(
                book,
                chapter,
                verse,
                text,
                reference,
                tokenize='porter unicode61'
            )
        """)

        # Create regular table for metadata and fast lookups
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verses (
                id INTEGER PRIMARY KEY,
                book TEXT NOT NULL,
                chapter INTEGER NOT NULL,
                verse INTEGER NOT NULL,
                text TEXT NOT NULL,
                reference TEXT NOT NULL,
                UNIQUE(book, chapter, verse)
            )
        """)

        # Create indexes for common queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_book ON verses(book)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_book_chapter ON verses(book, chapter)")

        # Populate with all verses
        print("Building search index...")
        batch = []
        batch_size = 1000
        total = 0

        for verse in bible.iter_verses():
            reference = f"{verse.book} {verse.chapter}:{verse.verse}"
            row = (verse.book, verse.chapter, verse.verse, verse.text, reference)
            batch.append(row)
            total += 1

            if len(batch) >= batch_size:
                cursor.executemany(
                    "INSERT INTO verses (book, chapter, verse, text, reference) VALUES (?, ?, ?, ?, ?)",
                    batch
                )
                cursor.executemany(
                    "INSERT INTO verses_fts (book, chapter, verse, text, reference) VALUES (?, ?, ?, ?, ?)",
                    batch
                )
                batch = []

        # Insert remaining
        if batch:
            cursor.executemany(
                "INSERT INTO verses (book, chapter, verse, text, reference) VALUES (?, ?, ?, ?, ?)",
                batch
            )
            cursor.executemany(
                "INSERT INTO verses_fts (book, chapter, verse, text, reference) VALUES (?, ?, ?, ?, ?)",
                batch
            )

        conn.commit()
        print(f"Search index built with {total} verses")

    return True


def search_verses(
    query: str,
    limit: Optional[int] = None,
    book_filter: Optional[str] = None,
    testament_filter: Optional[str] = None
) -> List[Dict]:
    """
    Search for verses matching the query using FTS5.

    Args:
        query: Search terms (supports FTS5 query syntax)
        limit: Maximum number of results
        book_filter: Filter to specific book
        testament_filter: Filter to "old" or "new" testament

    Returns:
        List of matching verses with relevance scores
    """
    # Ensure index exists
    if not DB_PATH.exists():
        init_search_index()

    with get_connection() as conn:
        cursor = conn.cursor()

        # Build the FTS5 query
        # Escape special FTS5 characters and prepare search terms
        search_terms = query.strip()
        if not search_terms:
            return []

        # For simple queries, search for all terms
        # FTS5 will handle ranking by relevance
        fts_query = ' '.join(f'"{term}"' for term in search_terms.split())

        # Build SQL with optional filters
        sql = """
            SELECT
                book,
                chapter,
                verse,
                text,
                reference,
                bm25(verses_fts) as score
            FROM verses_fts
            WHERE verses_fts MATCH ?
        """
        params = [fts_query]

        if book_filter:
            sql += " AND book = ?"
            params.append(book_filter)

        if testament_filter:
            ot_books = OT_BOOKS
            if testament_filter.lower() == 'old':
                placeholders = ','.join('?' * len(ot_books))
                sql += f" AND book IN ({placeholders})"
                params.extend(ot_books)
            elif testament_filter.lower() == 'new':
                placeholders = ','.join('?' * len(ot_books))
                sql += f" AND book NOT IN ({placeholders})"
                params.extend(ot_books)

        # Order by relevance (bm25 score - lower is better in SQLite)
        sql += " ORDER BY score"

        if limit:
            sql += " LIMIT ?"
            params.append(limit)

        cursor.execute(sql, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                "book": row["book"],
                "chapter": row["chapter"],
                "verse": row["verse"],
                "text": row["text"],
                "reference": row["reference"],
                "url": f"/book/{row['book']}/chapter/{row['chapter']}#verse-{row['verse']}",
                "score": abs(row["score"]),  # BM25 returns negative, we want positive
                "highlighted_text": highlight_matches(row["text"], query)
            })

        return results


def highlight_matches(text: str, query: str) -> str:
    """Highlight matching terms in text."""
    highlighted = text
    for term in query.lower().split():
        # Case-insensitive replacement with highlighting
        import re
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        highlighted = pattern.sub(f'<mark>{term}</mark>', highlighted)
    return highlighted


def get_search_stats() -> Dict:
    """Get statistics about the search index."""
    if not DB_PATH.exists():
        return {"indexed": False, "verses": 0}

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM verses")
        count = cursor.fetchone()[0]

        return {
            "indexed": True,
            "verses": count,
            "db_size_mb": round(DB_PATH.stat().st_size / (1024 * 1024), 2)
        }


# Initialize on import if database doesn't exist
if not DB_PATH.exists():
    # Don't auto-init during import - call init_search_index() explicitly
    pass
