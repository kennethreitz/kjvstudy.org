from pydantic import BaseModel
from pathlib import Path
from functools import lru_cache

import json


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
        with open(self.fname, "r") as f:
            self.verses = json.load(f)

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

            # Remove the leading "# " and brackets from the text.
            # This is a workaround for the JSON format.
            # The text is stored as a string with leading "# " and brackets.
            # Example: "# [In the beginning God created the heaven and the earth.]"
            text = self.verses[verse]
            text.replace("# ", "")
            text.replace("[", "")
            text.replace("]", "")

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
        Parses a string in the format "Book Chapter:Verse" and returns a VerseReference object.
        """

        # Split the string into parts.
        split_s = s.split(" ")

        # Handle the case where the book name has multiple words (e.g., "I Corinthians").
        # If the book name has more than one word, we need to join them.
        # The chapter and verse will always be the last part.
        # Example: "I Corinthians 1:1" -> ["I", "Corinthians", "1:1"]

        if len(split_s) > 2:
            book = split_s[0] + " " + split_s[1]
            chapter_verse = split_s[2]
        else:
            book = split_s[0]
            chapter_verse = split_s[1]

        chapter, verse = chapter_verse.split(":")
        return cls(book=book, chapter=int(chapter), verse=int(verse))


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
        with open(self.fname, "r") as f:
            self.verses = json.load(f)

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

            # Remove the leading "# " and brackets from the text.
            # This is a workaround for the JSON format.
            # The text is stored as a string with leading "# " and brackets.
            # Example: "# [In the beginning God created the heaven and the earth.]"
            text = self.verses[verse]
            text.replace("# ", "")
            text.replace("[", "")
            text.replace("]", "")

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
        verses = []
        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if verse_ref.book == book and verse_ref.chapter == chapter:
                # Clean up the text
                text = self.verses[verse]
                text = text.replace("# ", "").replace("[", "").replace("]", "")
                verses.append(Verse(
                    book=verse_ref.book,
                    chapter=verse_ref.chapter,
                    verse=verse_ref.verse,
                    text=text,
                ))
        return sorted(verses, key=lambda v: v.verse)

    @lru_cache(maxsize=128)
    def get_chapters_for_book(self, book):
        """Returns a list of chapter numbers for a specific book."""
        chapters = set()
        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if verse_ref.book == book:
                chapters.add(verse_ref.chapter)
        return sorted(list(chapters))

    @lru_cache(maxsize=2048)
    def get_verse_text(self, book, chapter, verse_num):
        """Returns the text for a specific verse."""
        verse_key = f"{book} {chapter}:{verse_num}"
        if verse_key in self.verses:
            text = self.verses[verse_key]
            return text.replace("# ", "").replace("[", "").replace("]", "")
        return None

    @lru_cache(maxsize=1)
    def get_verse_count(self):
        """Returns the total number of verses in the Bible."""
        return len(self.verses)


# Create an instance of the Bible class.
bible = Bible()


if __name__ == "__main__":

    print(VerseReference.from_string("Genesis 1:1"))
    print(VerseReference.from_string("I Corinthians 1:1"))
    print(VerseReference.from_string("John 3:16"))

    print(bible["Genesis 1:1"])
# print()
# print(verse)
# break  # Just print the first verse for demonstration
