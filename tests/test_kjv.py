# PATH HACK
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kjvstudy_org.kjv import VerseReference

def test_verse_references():
    # Test the parsing of a verse reference string
    assert VerseReference.from_string("Genesis 1:1") == VerseReference(
        book="Genesis", chapter=1, verse=1
    )
    assert VerseReference.from_string("I Corinthians 1:1") == VerseReference(
        book="I Corinthians", chapter=1, verse=1
    )
    assert VerseReference.from_string("John 3:16") == VerseReference(
        book="John", chapter=3, verse=16
    )
    assert VerseReference.from_string("Matthew 5:14") == VerseReference(
        book="Matthew", chapter=5, verse=14
    )
