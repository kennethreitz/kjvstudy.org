from pydantic import BaseModel


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
