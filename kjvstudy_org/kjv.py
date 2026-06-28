from pydantic import BaseModel
from pathlib import Path
from functools import lru_cache

import json
import re


class Verse(BaseModel):
    book: str
    chapter: int
    verse: int
    text: str


class VerseReference(BaseModel):
    book: str
    chapter: int
    verse: int

    @classmethod
    @lru_cache(maxsize=2048)
    def from_string(cls, s: str):
        """
        Parses a string in the format "Book Chapter:Verse" or "Book Chapter Verse"
        and returns a VerseReference object.

        Supports both colon format (John 3:16) and space format (John 3 16).
        """

        # Split the string into parts.
        split_s = s.split(" ")

        # Handle book names with multiple words (e.g., "I Corinthians", "Song of Solomon").
        # The chapter:verse will always be the last part (contains ":").
        # Everything before that is the book name.
        # Example: "Song of Solomon 1:1" -> book="Song of Solomon", chapter_verse="1:1"

        chapter_verse = split_s[-1]  # Last part is always chapter:verse or just verse

        # Check if using colon format (e.g., "3:16") or space format (e.g., "Rev 22 20")
        if ":" in chapter_verse:
            # Standard format: Book Chapter:Verse
            book = " ".join(split_s[:-1])
            chapter, verse = chapter_verse.split(":")
        else:
            # Space format: Book Chapter Verse (last two parts are chapter and verse)
            if len(split_s) >= 3 and split_s[-1].isdigit() and split_s[-2].isdigit():
                verse = split_s[-1]
                chapter = split_s[-2]
                book = " ".join(split_s[:-2])
            else:
                # Fallback to original behavior (will likely fail, but maintains compatibility)
                book = " ".join(split_s[:-1])
                chapter, verse = chapter_verse.split(":")

        return cls(book=book, chapter=int(chapter), verse=int(verse))


_REFERENCE_RE = re.compile(r'^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$')


def parse_reference_parts(reference: str):
    """Parse "Book Chapter:Verse[-VerseEnd]" into (book, chapter, verse, verse_end).

    Returns a tuple ``(book: str, chapter: int, verse: int, verse_end: int|None)``
    or ``None`` if the reference cannot be parsed. Handles multi-word and numbered
    book names (e.g. "Song of Solomon", "1 Corinthians") and optional verse ranges.
    This is the single canonical reference parser shared across the codebase.
    """
    if not reference or not isinstance(reference, str):
        return None
    match = _REFERENCE_RE.match(reference.strip())
    if not match:
        return None
    book = match.group(1).strip()
    chapter = int(match.group(2))
    verse = int(match.group(3))
    verse_end = int(match.group(4)) if match.group(4) else None
    return book, chapter, verse, verse_end


class Bible:
    """Represents a Bible."""

    def __init__(self, fname=None):
        if fname is None:
            # Get the directory where this script is located
            current_dir = Path(__file__).parent
            # Look for verses file in the package static directory
            self.fname = current_dir / "static" / "verses-1769.json"
        else:
            self.fname = Path(fname)

        # Load the JSON data from the file.
        with open(self.fname, "r", encoding="utf-8") as f:
            self.verses = json.load(f)

        # Pre-process verse text for performance (clean once instead of on every access)
        # Remove the leading "# " and brackets from the text stored in JSON
        # Example: "# [In the beginning...]" -> "In the beginning..."
        self._cleaned_verses = {
            key: text.replace("# ", "").replace("[", "").replace("]", "")
            for key, text in self.verses.items()
        }

        # Build indexes for O(1) lookups instead of O(n) iteration
        self._book_index = {}       # book -> [verse_keys]
        self._chapter_index = {}    # (book, chapter) -> [verse_keys]
        self._book_chapters = {}    # book -> sorted list of chapter numbers
        self._total_words = 0

        for key in self.verses:
            ref = VerseReference.from_string(key)
            # Book index
            if ref.book not in self._book_index:
                self._book_index[ref.book] = []
            self._book_index[ref.book].append(key)
            # Chapter index
            ch_key = (ref.book, ref.chapter)
            if ch_key not in self._chapter_index:
                self._chapter_index[ch_key] = []
            self._chapter_index[ch_key].append(key)
            # Book chapters
            if ref.book not in self._book_chapters:
                self._book_chapters[ref.book] = set()
            self._book_chapters[ref.book].add(ref.chapter)
            # Word count
            self._total_words += len(self._cleaned_verses[key].split())

        # Sort chapter sets into lists
        for book in self._book_chapters:
            self._book_chapters[book] = sorted(self._book_chapters[book])

    @lru_cache(maxsize=1024)
    def __getitem__(self, verse):
        """Returns the text of the verse."""

        # Check if the verse exists in the dictionary.
        if verse not in self.verses:
            raise KeyError(f"Verse {verse} not found in the Bible.")

        return self.verses[verse]

    def iter_verses(self):
        """Iterates over the verses in the Bible."""

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)

            # Use pre-cleaned text for performance (5-10x faster than cleaning on every iteration)
            text = self._cleaned_verses[verse]

            yield Verse(
                book=verse_ref.book,
                chapter=verse_ref.chapter,
                verse=verse_ref.verse,
                text=text,
            )

    @lru_cache(maxsize=1)
    def get_books(self):
        """Returns a list of all books in the Bible."""
        yielded = set()
        books = []

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if verse_ref.book in yielded:
                continue
            yielded.add(verse_ref.book)
            books.append(verse_ref.book)
        
        return books

    def iter_books(self):
        """Iterates over the books in the Bible."""
        for book in self.get_books():
            yield book

    @lru_cache(maxsize=1)
    def get_chapters(self):
        """Returns a list of all chapters in the Bible."""
        yielded = set()
        chapters = []

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if (verse_ref.book, verse_ref.chapter) in yielded:
                continue
            yielded.add((verse_ref.book, verse_ref.chapter))
            chapters.append((verse_ref.book, verse_ref.chapter))
        
        return chapters

    def iter_chapters(self):
        """Iterates over the chapters in the Bible."""
        for book, chapter in self.get_chapters():
            yield book, chapter

    def iter_chapters_by_book(self):
        """Iterates over the chapters in the Bible, grouped by book."""

        yielded = set()

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if (verse_ref.book, verse_ref.chapter) in yielded:
                continue
            yielded.add((verse_ref.book, verse_ref.chapter))
            yield verse_ref.book, verse_ref.chapter

    def iter_verse_references(self):
        """Iterates over the verse references in the Bible."""

        for verse in self.verses:
            yield VerseReference.from_string(verse)

    @lru_cache(maxsize=256)
    def get_verses_by_book_chapter(self, book, chapter):
        """Returns a list of verses for a specific book and chapter."""
        keys = self._chapter_index.get((book, chapter), [])
        verses = []
        for key in keys:
            ref = VerseReference.from_string(key)
            verses.append(Verse(
                book=ref.book,
                chapter=ref.chapter,
                verse=ref.verse,
                text=self._cleaned_verses[key],
            ))
        return sorted(verses, key=lambda v: v.verse)

    @lru_cache(maxsize=128)
    def get_chapters_for_book(self, book):
        """Returns a list of chapter numbers for a specific book."""
        return self._book_chapters.get(book, [])

    @lru_cache(maxsize=2048)
    def get_verse_text(self, book, chapter, verse_num):
        """Returns the text for a specific verse."""
        verse_key = f"{book} {chapter}:{verse_num}"
        if verse_key in self.verses:
            # Use pre-cleaned text for performance
            return self._cleaned_verses[verse_key]
        return None

    @lru_cache(maxsize=1)
    def get_verse_count(self):
        """Returns the total number of verses in the Bible."""
        return len(self.verses)

    def get_total_words(self):
        """Returns the total word count across all verses (pre-computed at init)."""
        return self._total_words

    def get_verses_by_book(self, book):
        """Returns all verses for a specific book, grouped by chapter."""
        chapters = self._book_chapters.get(book, [])
        return {ch: self.get_verses_by_book_chapter(book, ch) for ch in chapters}


# Create an instance of the Bible class.
bible = Bible()


if __name__ == "__main__":

    print(VerseReference.from_string("Genesis 1:1"))
    print(VerseReference.from_string("I Corinthians 1:1"))
    print(VerseReference.from_string("John 3:16"))

    print(bible["Genesis 1:1"])