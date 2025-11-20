"""
Cross-reference system for linking related Bible verses.
Organized by major theological themes and narrative connections.
"""

# Cross-references database: book:chapter:verse -> list of related verses
CROSS_REFERENCES = {
    # Genesis - Creation and Fall
    "Genesis:1:1": [
        {"ref": "John 1:1", "note": "The Word in creation"},
        {"ref": "Hebrews 11:3", "note": "By faith we understand creation"},
        {"ref": "Colossians 1:16", "note": "All things created by Christ"},
    ],
    "Genesis:1:26": [
        {"ref": "Genesis 5:1", "note": "Made in God's likeness"},
        {"ref": "Ephesians 4:24", "note": "New man in God's image"},
        {"ref": "Colossians 3:10", "note": "Renewed in knowledge"},
    ],
    "Genesis:3:15": [
        {"ref": "Romans 16:20", "note": "Satan crushed under feet"},
        {"ref": "Galatians 4:4", "note": "Born of a woman"},
        {"ref": "Revelation 12:9", "note": "The serpent cast down"},
    ],

    # Psalms - Messianic Prophecies
    "Psalms:22:1": [
        {"ref": "Matthew 27:46", "note": "Christ's cry from the cross"},
        {"ref": "Mark 15:34", "note": "Why hast thou forsaken me?"},
    ],
    "Psalms:22:16": [
        {"ref": "John 19:37", "note": "They pierced my hands and feet"},
        {"ref": "John 20:25", "note": "Print of the nails"},
    ],
    "Psalms:23:1": [
        {"ref": "John 10:11", "note": "I am the good shepherd"},
        {"ref": "Hebrews 13:20", "note": "Great shepherd of the sheep"},
        {"ref": "1 Peter 5:4", "note": "Chief Shepherd"},
    ],

    # Isaiah - Messianic Prophecies
    "Isaiah:7:14": [
        {"ref": "Matthew 1:23", "note": "Virgin shall conceive"},
        {"ref": "Luke 1:27", "note": "Virgin espoused to Joseph"},
    ],
    "Isaiah:9:6": [
        {"ref": "Luke 2:11", "note": "Unto you is born a Saviour"},
        {"ref": "John 1:1", "note": "The Word was God"},
    ],
    "Isaiah:53:5": [
        {"ref": "1 Peter 2:24", "note": "By whose stripes ye were healed"},
        {"ref": "Matthew 8:17", "note": "Himself took our infirmities"},
    ],
    "Isaiah:53:7": [
        {"ref": "Acts 8:32", "note": "As a sheep to the slaughter"},
        {"ref": "John 1:29", "note": "Behold the Lamb of God"},
    ],

    # Gospels - Christ's Ministry
    "Matthew:1:23": [
        {"ref": "Isaiah 7:14", "note": "Virgin shall conceive (prophecy)"},
        {"ref": "Matthew 28:20", "note": "I am with you alway"},
    ],
    "Matthew:3:17": [
        {"ref": "Matthew 17:5", "note": "This is my beloved Son"},
        {"ref": "2 Peter 1:17", "note": "Voice from heaven"},
    ],
    "Matthew:5:17": [
        {"ref": "Romans 10:4", "note": "Christ is the end of the law"},
        {"ref": "Galatians 3:24", "note": "Law our schoolmaster"},
    ],
    "Matthew:16:16": [
        {"ref": "John 6:69", "note": "Thou art that Christ"},
        {"ref": "Matthew 16:18", "note": "Upon this rock"},
    ],
    "Matthew:26:26": [
        {"ref": "1 Corinthians 11:24", "note": "This is my body"},
        {"ref": "Luke 22:19", "note": "In remembrance of me"},
    ],

    # John - I AM Statements
    "John:1:1": [
        {"ref": "Genesis 1:1", "note": "In the beginning"},
        {"ref": "1 John 1:1", "note": "Word of life"},
        {"ref": "Revelation 19:13", "note": "Name called The Word of God"},
    ],
    "John:1:29": [
        {"ref": "Isaiah 53:7", "note": "As a lamb (prophecy)"},
        {"ref": "1 Corinthians 5:7", "note": "Christ our passover"},
        {"ref": "1 Peter 1:19", "note": "Precious blood of Christ"},
    ],
    "John:3:16": [
        {"ref": "Romans 5:8", "note": "God commendeth his love"},
        {"ref": "1 John 4:9", "note": "God sent his only begotten Son"},
    ],
    "John:6:35": [
        {"ref": "John 6:48", "note": "I am that bread of life"},
        {"ref": "John 6:51", "note": "Living bread from heaven"},
    ],
    "John:8:12": [
        {"ref": "John 9:5", "note": "I am the light of the world"},
        {"ref": "John 1:4", "note": "Life was the light of men"},
    ],
    "John:10:11": [
        {"ref": "Psalms 23:1", "note": "The LORD is my shepherd"},
        {"ref": "Hebrews 13:20", "note": "Great shepherd of the sheep"},
    ],
    "John:11:25": [
        {"ref": "John 14:6", "note": "I am the way, truth, and life"},
        {"ref": "Revelation 1:18", "note": "I am he that liveth"},
    ],
    "John:14:6": [
        {"ref": "Acts 4:12", "note": "None other name under heaven"},
        {"ref": "1 Timothy 2:5", "note": "One mediator"},
    ],
    "John:15:1": [
        {"ref": "Psalms 80:8", "note": "Brought a vine out of Egypt"},
        {"ref": "Isaiah 5:1", "note": "Beloved had a vineyard"},
    ],

    # Romans - Justification by Faith
    "Romans:1:16": [
        {"ref": "1 Corinthians 1:18", "note": "Power of God unto salvation"},
        {"ref": "2 Timothy 1:8", "note": "Not ashamed of the gospel"},
    ],
    "Romans:3:23": [
        {"ref": "Romans 5:12", "note": "Sin entered into the world"},
        {"ref": "1 John 1:8", "note": "If we say we have no sin"},
    ],
    "Romans:3:24": [
        {"ref": "Ephesians 2:8", "note": "By grace through faith"},
        {"ref": "Titus 3:5", "note": "Not by works of righteousness"},
    ],
    "Romans:5:1": [
        {"ref": "Romans 3:28", "note": "Justified by faith"},
        {"ref": "Galatians 2:16", "note": "Not justified by works of law"},
    ],
    "Romans:5:8": [
        {"ref": "John 3:16", "note": "God so loved the world"},
        {"ref": "1 John 4:10", "note": "Herein is love"},
    ],
    "Romans:6:23": [
        {"ref": "Ezekiel 18:4", "note": "Soul that sinneth shall die"},
        {"ref": "1 Corinthians 15:56", "note": "Sting of death is sin"},
    ],
    "Romans:8:1": [
        {"ref": "John 3:18", "note": "Not condemned"},
        {"ref": "John 5:24", "note": "Shall not come into condemnation"},
    ],
    "Romans:8:28": [
        {"ref": "Jeremiah 29:11", "note": "Thoughts of peace"},
        {"ref": "Ephesians 1:11", "note": "According to his purpose"},
    ],
    "Romans:10:9": [
        {"ref": "Acts 16:31", "note": "Believe on the Lord Jesus Christ"},
        {"ref": "1 John 4:15", "note": "Confess that Jesus is the Son of God"},
    ],
    "Romans:12:1": [
        {"ref": "1 Corinthians 6:20", "note": "Glorify God in your body"},
        {"ref": "2 Corinthians 5:15", "note": "Live unto him"},
    ],

    # 1 Corinthians - Church Life
    "1 Corinthians:10:13": [
        {"ref": "Hebrews 2:18", "note": "Able to succour them that are tempted"},
        {"ref": "James 1:13", "note": "God cannot be tempted"},
    ],
    "1 Corinthians:11:24": [
        {"ref": "Matthew 26:26", "note": "This is my body"},
        {"ref": "Luke 22:19", "note": "In remembrance of me"},
    ],
    "1 Corinthians:13:4": [
        {"ref": "1 John 4:8", "note": "God is love"},
        {"ref": "Colossians 3:14", "note": "Put on charity"},
    ],
    "1 Corinthians:15:3": [
        {"ref": "Isaiah 53:5", "note": "Wounded for our transgressions"},
        {"ref": "1 Peter 2:24", "note": "Who his own self bare our sins"},
    ],
    "1 Corinthians:15:20": [
        {"ref": "Colossians 1:18", "note": "Firstborn from the dead"},
        {"ref": "Revelation 1:5", "note": "First begotten of the dead"},
    ],

    # Ephesians - The Church
    "Ephesians:1:7": [
        {"ref": "Colossians 1:14", "note": "Redemption through his blood"},
        {"ref": "1 Peter 1:19", "note": "Precious blood of Christ"},
    ],
    "Ephesians:2:8": [
        {"ref": "Romans 3:24", "note": "Justified freely by grace"},
        {"ref": "Titus 3:5", "note": "Not by works"},
    ],
    "Ephesians:2:10": [
        {"ref": "James 2:17", "note": "Faith without works is dead"},
        {"ref": "Titus 2:14", "note": "Zealous of good works"},
    ],
    "Ephesians:4:32": [
        {"ref": "Colossians 3:13", "note": "Forgiving one another"},
        {"ref": "Matthew 6:14", "note": "Forgive men their trespasses"},
    ],
    "Ephesians:6:11": [
        {"ref": "Romans 13:12", "note": "Put on the armour of light"},
        {"ref": "1 Thessalonians 5:8", "note": "Breastplate of faith and love"},
    ],

    # Philippians - Joy in Christ
    "Philippians:2:5": [
        {"ref": "1 Peter 2:21", "note": "Christ suffered for us"},
        {"ref": "Matthew 11:29", "note": "Learn of me"},
    ],
    "Philippians:2:10": [
        {"ref": "Isaiah 45:23", "note": "Every knee shall bow"},
        {"ref": "Romans 14:11", "note": "Every tongue confess"},
    ],
    "Philippians:4:6": [
        {"ref": "1 Peter 5:7", "note": "Casting all your care upon him"},
        {"ref": "Matthew 6:25", "note": "Take no thought for your life"},
    ],
    "Philippians:4:13": [
        {"ref": "2 Corinthians 12:9", "note": "My grace is sufficient"},
        {"ref": "1 Timothy 1:12", "note": "Christ strengthened me"},
    ],

    # Hebrews - Christ's Superiority
    "Hebrews:1:3": [
        {"ref": "Colossians 1:15", "note": "Image of the invisible God"},
        {"ref": "2 Corinthians 4:4", "note": "Image of God"},
    ],
    "Hebrews:4:12": [
        {"ref": "Ephesians 6:17", "note": "Sword of the Spirit"},
        {"ref": "Revelation 1:16", "note": "Sharp twoedged sword"},
    ],
    "Hebrews:4:15": [
        {"ref": "2 Corinthians 5:21", "note": "Knew no sin"},
        {"ref": "1 Peter 2:22", "note": "Who did no sin"},
    ],
    "Hebrews:9:12": [
        {"ref": "1 Peter 1:18", "note": "Not redeemed with silver and gold"},
        {"ref": "Acts 20:28", "note": "Purchased with his own blood"},
    ],
    "Hebrews:11:1": [
        {"ref": "2 Corinthians 5:7", "note": "Walk by faith, not by sight"},
        {"ref": "Romans 8:24", "note": "Hope that is seen is not hope"},
    ],
    "Hebrews:13:8": [
        {"ref": "Malachi 3:6", "note": "I change not"},
        {"ref": "James 1:17", "note": "No variableness, neither shadow of turning"},
    ],

    # James - Faith and Works
    "James:1:22": [
        {"ref": "Matthew 7:21", "note": "Not every one that saith Lord, Lord"},
        {"ref": "Luke 6:46", "note": "Why call ye me Lord, and do not?"},
    ],
    "James:2:17": [
        {"ref": "Ephesians 2:10", "note": "Created unto good works"},
        {"ref": "Titus 2:14", "note": "Zealous of good works"},
    ],
    "James:4:7": [
        {"ref": "1 Peter 5:8", "note": "Resist the devil"},
        {"ref": "Ephesians 6:11", "note": "Stand against the wiles of the devil"},
    ],

    # 1 Peter - Suffering and Glory
    "1 Peter:1:18": [
        {"ref": "Hebrews 9:12", "note": "Not with blood of goats"},
        {"ref": "Acts 20:28", "note": "Purchased with his own blood"},
    ],
    "1 Peter:2:24": [
        {"ref": "Isaiah 53:5", "note": "Wounded for our transgressions"},
        {"ref": "1 Corinthians 15:3", "note": "Christ died for our sins"},
    ],
    "1 Peter:5:7": [
        {"ref": "Philippians 4:6", "note": "Be careful for nothing"},
        {"ref": "Psalms 55:22", "note": "Cast thy burden upon the LORD"},
    ],

    # 1 John - Love and Assurance
    "1 John:1:7": [
        {"ref": "Revelation 1:5", "note": "Washed us from our sins"},
        {"ref": "Hebrews 9:14", "note": "Blood of Christ"},
    ],
    "1 John:1:9": [
        {"ref": "Proverbs 28:13", "note": "Whoso confesseth shall have mercy"},
        {"ref": "Psalms 32:5", "note": "I acknowledged my sin"},
    ],
    "1 John:2:1": [
        {"ref": "Romans 8:34", "note": "Christ maketh intercession"},
        {"ref": "Hebrews 7:25", "note": "Ever liveth to make intercession"},
    ],
    "1 John:3:16": [
        {"ref": "John 15:13", "note": "Greater love hath no man"},
        {"ref": "Romans 5:8", "note": "Christ died for us"},
    ],
    "1 John:4:8": [
        {"ref": "1 Corinthians 13:4", "note": "Charity suffereth long"},
        {"ref": "1 John 4:16", "note": "God is love"},
    ],
    "1 John:5:11": [
        {"ref": "John 3:36", "note": "He that believeth hath life"},
        {"ref": "John 10:28", "note": "I give unto them eternal life"},
    ],

    # Revelation - End Times
    "Revelation:1:8": [
        {"ref": "Revelation 21:6", "note": "Alpha and Omega"},
        {"ref": "Isaiah 44:6", "note": "I am the first and the last"},
    ],
    "Revelation:3:20": [
        {"ref": "John 10:9", "note": "I am the door"},
        {"ref": "Song of Solomon 5:2", "note": "Open to me"},
    ],
    "Revelation:21:4": [
        {"ref": "Isaiah 25:8", "note": "Wipe away tears"},
        {"ref": "Revelation 7:17", "note": "God shall wipe away all tears"},
    ],
}


def get_cross_references(book: str, chapter: int, verse: int) -> list:
    """
    Get cross-references for a specific verse.

    Args:
        book: Book name (e.g., "Genesis", "John")
        chapter: Chapter number
        verse: Verse number

    Returns:
        List of cross-reference dictionaries with 'ref' and 'note' keys
    """
    key = f"{book}:{chapter}:{verse}"
    return CROSS_REFERENCES.get(key, [])


def parse_reference(ref: str) -> dict:
    """
    Parse a reference string like "Genesis 1:1" into components.

    Args:
        ref: Reference string

    Returns:
        Dictionary with 'book', 'chapter', 'verse' keys
    """
    parts = ref.rsplit(' ', 1)
    if len(parts) != 2:
        return None

    book = parts[0]
    chapter_verse = parts[1].split(':')
    if len(chapter_verse) != 2:
        return None

    try:
        return {
            'book': book,
            'chapter': int(chapter_verse[0]),
            'verse': int(chapter_verse[1])
        }
    except ValueError:
        return None
