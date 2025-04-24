import json
from pydantic import BaseModel


class Bible:
    def __init__(self, fname=None):
        self.fname = fname or "verses-1769.json"

        # Load the JSON data from the file.
        with open(self.fname, "r") as f:
            self.verses = json.load(f)

    def iter_verses(self):
        """
        Iterates over the verses in the Bible.
        """

        for verse in self.verses:
            verse_ref = VerseReference.from_string(verse)

            yield Verse(
                book=verse_ref.book,
                chapter=verse_ref.chapter,
                verse=verse_ref.verse,
                text=self.verses[verse],
            )

    def iter_verse_references(self):
        """
        Iterates over the verse references in the Bible.
        """

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


print(VerseReference.from_string("Genesis 1:1"))
print(VerseReference.from_string("I Corinthians 1:1"))
print(VerseReference.from_string("John 3:16"))


bible = Bible()
for verse in bible.iter_verses():
    print(verse)
    # break  # Just print the first verse for demonstration
