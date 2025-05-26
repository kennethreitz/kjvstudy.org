from pydantic import BaseModel
from pathlib import Path

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

    def iter_books(self):
        """Iterates over the books in the Bible."""

        yielded = set()

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if verse_ref.book in yielded:
                continue
            yielded.add(verse_ref.book)
            yield verse_ref.book

    def iter_chapters(self):
        """Iterates over the chapters in the Bible."""

        yielded = set()

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)
            if (verse_ref.book, verse_ref.chapter) in yielded:
                continue
            yielded.add((verse_ref.book, verse_ref.chapter))
            yield verse_ref.book, verse_ref.chapter

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
