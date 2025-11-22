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

    # Additional Genesis - Patriarchs and Promises
    "Genesis:12:1": [
        {"ref": "Hebrews 11:8", "note": "Abraham went out by faith"},
        {"ref": "Acts 7:2", "note": "God appeared to Abraham"},
        {"ref": "Genesis 15:7", "note": "Brought thee out of Ur"},
    ],
    "Genesis:12:3": [
        {"ref": "Galatians 3:8", "note": "All nations blessed in thee"},
        {"ref": "Acts 3:25", "note": "Ye are children of the covenant"},
        {"ref": "Genesis 18:18", "note": "All nations shall be blessed"},
    ],
    "Genesis:15:6": [
        {"ref": "Romans 4:3", "note": "Abraham believed God"},
        {"ref": "Galatians 3:6", "note": "Accounted to him for righteousness"},
        {"ref": "James 2:23", "note": "Scripture fulfilled"},
    ],
    "Genesis:22:8": [
        {"ref": "John 1:29", "note": "God will provide the Lamb"},
        {"ref": "Hebrews 11:17", "note": "Offered up Isaac"},
        {"ref": "Genesis 22:13", "note": "Ram provided"},
    ],
    "Genesis:28:12": [
        {"ref": "John 1:51", "note": "Angels ascending and descending"},
        {"ref": "Hebrews 1:14", "note": "Ministering spirits"},
    ],

    # Exodus - Deliverance and Law
    "Exodus:3:14": [
        {"ref": "John 8:58", "note": "Before Abraham was, I AM"},
        {"ref": "Revelation 1:8", "note": "Which is, and was, and is to come"},
        {"ref": "Exodus 6:3", "note": "I appeared unto Abraham"},
    ],
    "Exodus:12:13": [
        {"ref": "1 Corinthians 5:7", "note": "Christ our passover"},
        {"ref": "1 Peter 1:19", "note": "Precious blood of Christ"},
        {"ref": "Hebrews 11:28", "note": "Through faith kept the passover"},
    ],
    "Exodus:20:3": [
        {"ref": "Deuteronomy 5:7", "note": "No other gods before me"},
        {"ref": "Matthew 4:10", "note": "Worship the Lord thy God only"},
        {"ref": "1 Corinthians 8:6", "note": "To us there is but one God"},
    ],
    "Exodus:20:12": [
        {"ref": "Ephesians 6:2", "note": "First commandment with promise"},
        {"ref": "Colossians 3:20", "note": "Obey your parents"},
        {"ref": "Matthew 15:4", "note": "Honour thy father and mother"},
    ],
    "Exodus:33:20": [
        {"ref": "1 Timothy 6:16", "note": "No man hath seen God"},
        {"ref": "John 1:18", "note": "No man hath seen God"},
        {"ref": "Exodus 33:23", "note": "Thou shalt see my back parts"},
    ],

    # Leviticus - Holiness and Sacrifice
    "Leviticus:16:15": [
        {"ref": "Hebrews 9:12", "note": "By his own blood"},
        {"ref": "Hebrews 9:7", "note": "High priest once every year"},
        {"ref": "Leviticus 23:27", "note": "Day of atonement"},
    ],
    "Leviticus:19:18": [
        {"ref": "Matthew 22:39", "note": "Love thy neighbour as thyself"},
        {"ref": "Romans 13:9", "note": "Love is the fulfilling of the law"},
        {"ref": "Galatians 5:14", "note": "All the law is fulfilled in one word"},
    ],

    # Numbers - Wilderness Journey
    "Numbers:21:9": [
        {"ref": "John 3:14", "note": "Son of man must be lifted up"},
        {"ref": "2 Kings 18:4", "note": "Brasen serpent destroyed"},
    ],
    "Numbers:23:19": [
        {"ref": "1 Samuel 15:29", "note": "God is not a man"},
        {"ref": "Titus 1:2", "note": "God cannot lie"},
        {"ref": "Hebrews 6:18", "note": "Impossible for God to lie"},
    ],

    # Deuteronomy - Second Law
    "Deuteronomy:6:4": [
        {"ref": "Mark 12:29", "note": "The Lord our God is one Lord"},
        {"ref": "1 Corinthians 8:4", "note": "There is none other God but one"},
        {"ref": "James 2:19", "note": "There is one God"},
    ],
    "Deuteronomy:6:5": [
        {"ref": "Matthew 22:37", "note": "Love the Lord thy God"},
        {"ref": "Mark 12:30", "note": "With all thy heart"},
        {"ref": "Luke 10:27", "note": "With all thy strength"},
    ],
    "Deuteronomy:8:3": [
        {"ref": "Matthew 4:4", "note": "Man shall not live by bread alone"},
        {"ref": "Luke 4:4", "note": "By every word of God"},
    ],
    "Deuteronomy:18:15": [
        {"ref": "Acts 3:22", "note": "A prophet like unto me"},
        {"ref": "Acts 7:37", "note": "Him shall ye hear"},
        {"ref": "John 1:21", "note": "Art thou that prophet?"},
    ],

    # Joshua - Conquest
    "Joshua:1:5": [
        {"ref": "Hebrews 13:5", "note": "I will never leave thee"},
        {"ref": "Deuteronomy 31:6", "note": "He will not fail thee"},
    ],
    "Joshua:24:15": [
        {"ref": "Ruth 1:16", "note": "Thy people shall be my people"},
        {"ref": "1 Kings 18:21", "note": "How long halt ye?"},
    ],

    # Psalms - Additional Key Passages
    "Psalms:2:7": [
        {"ref": "Acts 13:33", "note": "Thou art my Son"},
        {"ref": "Hebrews 1:5", "note": "This day have I begotten thee"},
        {"ref": "Hebrews 5:5", "note": "Glorified not himself"},
    ],
    "Psalms:16:10": [
        {"ref": "Acts 2:27", "note": "Not leave my soul in hell"},
        {"ref": "Acts 13:35", "note": "Not suffer thine Holy One"},
    ],
    "Psalms:22:18": [
        {"ref": "Matthew 27:35", "note": "Parted my garments"},
        {"ref": "John 19:24", "note": "Cast lots upon my vesture"},
    ],
    "Psalms:34:8": [
        {"ref": "1 Peter 2:3", "note": "Taste that the Lord is gracious"},
        {"ref": "Hebrews 6:4", "note": "Tasted the good word of God"},
    ],
    "Psalms:51:5": [
        {"ref": "Romans 5:12", "note": "Sin entered into the world"},
        {"ref": "Ephesians 2:3", "note": "By nature children of wrath"},
    ],
    "Psalms:110:1": [
        {"ref": "Matthew 22:44", "note": "Sit thou at my right hand"},
        {"ref": "Acts 2:34", "note": "David is not ascended"},
        {"ref": "Hebrews 1:13", "note": "To which of the angels?"},
    ],
    "Psalms:110:4": [
        {"ref": "Hebrews 5:6", "note": "Priest for ever after Melchizedek"},
        {"ref": "Hebrews 7:17", "note": "Thou art a priest for ever"},
    ],
    "Psalms:118:22": [
        {"ref": "Matthew 21:42", "note": "Stone which builders rejected"},
        {"ref": "Acts 4:11", "note": "Become the head of the corner"},
        {"ref": "1 Peter 2:7", "note": "Chief corner stone"},
    ],

    # Proverbs - Wisdom
    "Proverbs:3:5": [
        {"ref": "Jeremiah 17:5", "note": "Cursed is the man that trusteth in man"},
        {"ref": "Psalms 37:5", "note": "Commit thy way unto the LORD"},
    ],
    "Proverbs:3:6": [
        {"ref": "Psalms 25:9", "note": "The meek will he guide"},
        {"ref": "James 4:10", "note": "Humble yourselves"},
    ],
    "Proverbs:22:6": [
        {"ref": "Ephesians 6:4", "note": "Bring them up in nurture"},
        {"ref": "Deuteronomy 6:7", "note": "Teach them diligently"},
    ],

    # Isaiah - Additional Prophecies
    "Isaiah:6:3": [
        {"ref": "Revelation 4:8", "note": "Holy, holy, holy, Lord God Almighty"},
        {"ref": "Ezekiel 3:12", "note": "Blessed be the glory of the LORD"},
    ],
    "Isaiah:40:3": [
        {"ref": "Matthew 3:3", "note": "Voice of one crying in wilderness"},
        {"ref": "John 1:23", "note": "I am the voice"},
    ],
    "Isaiah:40:31": [
        {"ref": "2 Corinthians 4:16", "note": "Inward man is renewed"},
        {"ref": "Psalms 103:5", "note": "Renewed like the eagle"},
    ],
    "Isaiah:55:6": [
        {"ref": "Matthew 7:7", "note": "Seek, and ye shall find"},
        {"ref": "Deuteronomy 4:29", "note": "If thou seek him with all thy heart"},
    ],
    "Isaiah:61:1": [
        {"ref": "Luke 4:18", "note": "Spirit of the Lord upon me"},
        {"ref": "Acts 10:38", "note": "God anointed Jesus"},
    ],

    # Jeremiah - New Covenant
    "Jeremiah:17:9": [
        {"ref": "Matthew 15:19", "note": "Out of the heart proceed evil"},
        {"ref": "Genesis 6:5", "note": "Every imagination evil"},
    ],
    "Jeremiah:31:31": [
        {"ref": "Hebrews 8:8", "note": "I will make a new covenant"},
        {"ref": "Luke 22:20", "note": "New testament in my blood"},
    ],
    "Jeremiah:31:34": [
        {"ref": "Hebrews 8:12", "note": "I will remember their sins no more"},
        {"ref": "Hebrews 10:17", "note": "Iniquities will I remember no more"},
    ],

    # Ezekiel - Visions
    "Ezekiel:36:26": [
        {"ref": "2 Corinthians 5:17", "note": "New creature in Christ"},
        {"ref": "Ezekiel 11:19", "note": "New heart and new spirit"},
    ],
    "Ezekiel:37:5": [
        {"ref": "John 5:25", "note": "Dead shall hear voice of Son"},
        {"ref": "Revelation 11:11", "note": "Spirit of life from God"},
    ],

    # Daniel - Prophecy
    "Daniel:2:44": [
        {"ref": "Revelation 11:15", "note": "Kingdom of our Lord"},
        {"ref": "Luke 1:33", "note": "Of his kingdom no end"},
    ],
    "Daniel:7:13": [
        {"ref": "Matthew 24:30", "note": "Son of man coming in clouds"},
        {"ref": "Revelation 1:7", "note": "Cometh with clouds"},
    ],
    "Daniel:9:24": [
        {"ref": "Galatians 4:4", "note": "Fullness of time"},
        {"ref": "Romans 5:6", "note": "In due time Christ died"},
    ],

    # Hosea - Divine Love
    "Hosea:11:1": [
        {"ref": "Matthew 2:15", "note": "Out of Egypt called my son"},
        {"ref": "Exodus 4:22", "note": "Israel is my son"},
    ],
    "Hosea:13:14": [
        {"ref": "1 Corinthians 15:55", "note": "O death, where is thy sting?"},
        {"ref": "1 Corinthians 15:54", "note": "Death is swallowed up"},
    ],

    # Joel - Pentecost
    "Joel:2:28": [
        {"ref": "Acts 2:17", "note": "Pour out my Spirit"},
        {"ref": "Acts 2:16", "note": "This is that spoken by Joel"},
    ],
    "Joel:2:32": [
        {"ref": "Acts 2:21", "note": "Whosoever shall call on the name"},
        {"ref": "Romans 10:13", "note": "Whosoever shall call shall be saved"},
    ],

    # Micah - Messiah's Birthplace
    "Micah:5:2": [
        {"ref": "Matthew 2:6", "note": "Out of thee shall come a Governor"},
        {"ref": "John 7:42", "note": "Christ cometh of Bethlehem"},
    ],

    # Habakkuk - Righteous by Faith
    "Habakkuk:2:4": [
        {"ref": "Romans 1:17", "note": "Just shall live by faith"},
        {"ref": "Galatians 3:11", "note": "Just shall live by faith"},
        {"ref": "Hebrews 10:38", "note": "Just shall live by faith"},
    ],

    # Zechariah - Prophecy
    "Zechariah:9:9": [
        {"ref": "Matthew 21:5", "note": "Thy King cometh, riding on an ass"},
        {"ref": "John 12:15", "note": "King cometh, sitting on ass's colt"},
    ],
    "Zechariah:12:10": [
        {"ref": "John 19:37", "note": "They shall look on him whom they pierced"},
        {"ref": "Revelation 1:7", "note": "They also which pierced him"},
    ],

    # Malachi - Messenger
    "Malachi:3:1": [
        {"ref": "Matthew 11:10", "note": "Messenger before thy face"},
        {"ref": "Mark 1:2", "note": "Prepare thy way"},
        {"ref": "Luke 1:76", "note": "Prophet of the Highest"},
    ],
    "Malachi:4:5": [
        {"ref": "Matthew 11:14", "note": "This is Elias"},
        {"ref": "Matthew 17:11", "note": "Elias truly shall first come"},
    ],

    # Matthew - Additional Gospel Parallels
    "Matthew:1:21": [
        {"ref": "Acts 4:12", "note": "None other name"},
        {"ref": "Luke 2:11", "note": "Born a Saviour"},
    ],
    "Matthew:4:4": [
        {"ref": "Deuteronomy 8:3", "note": "Man doth not live by bread only"},
        {"ref": "Luke 4:4", "note": "By every word of God"},
    ],
    "Matthew:6:9": [
        {"ref": "Luke 11:2", "note": "When ye pray, say, Our Father"},
        {"ref": "Romans 8:15", "note": "Whereby we cry, Abba, Father"},
    ],
    "Matthew:6:33": [
        {"ref": "1 Kings 3:13", "note": "I have given thee riches"},
        {"ref": "Psalms 37:25", "note": "Not seen righteous forsaken"},
    ],
    "Matthew:7:7": [
        {"ref": "Luke 11:9", "note": "Ask, and it shall be given"},
        {"ref": "John 14:13", "note": "Whatsoever ye shall ask"},
    ],
    "Matthew:11:28": [
        {"ref": "John 6:37", "note": "Him that cometh I will not cast out"},
        {"ref": "Revelation 22:17", "note": "Whosoever will, let him take"},
    ],
    "Matthew:18:20": [
        {"ref": "Matthew 28:20", "note": "I am with you alway"},
        {"ref": "1 Corinthians 5:4", "note": "Gathered together"},
    ],
    "Matthew:24:30": [
        {"ref": "Daniel 7:13", "note": "Son of man coming in clouds"},
        {"ref": "Revelation 1:7", "note": "Every eye shall see him"},
    ],
    "Matthew:28:19": [
        {"ref": "Mark 16:15", "note": "Go ye into all the world"},
        {"ref": "Acts 1:8", "note": "Witnesses unto me"},
    ],
    "Matthew:28:20": [
        {"ref": "Hebrews 13:5", "note": "I will never leave thee"},
        {"ref": "Joshua 1:5", "note": "I will not fail thee"},
    ],

    # Mark - Gospel Parallels
    "Mark:1:15": [
        {"ref": "Matthew 4:17", "note": "Repent: for kingdom of heaven is at hand"},
        {"ref": "Acts 2:38", "note": "Repent, and be baptized"},
    ],
    "Mark:10:45": [
        {"ref": "Matthew 20:28", "note": "Came to minister, give life a ransom"},
        {"ref": "1 Timothy 2:6", "note": "Gave himself a ransom for all"},
    ],
    "Mark:16:16": [
        {"ref": "Acts 16:31", "note": "Believe on the Lord Jesus Christ"},
        {"ref": "John 3:18", "note": "He that believeth not is condemned"},
    ],

    # Luke - Additional Passages
    "Luke:2:14": [
        {"ref": "Ephesians 2:14", "note": "He is our peace"},
        {"ref": "Colossians 1:20", "note": "Peace through blood of his cross"},
    ],
    "Luke:15:7": [
        {"ref": "Matthew 18:13", "note": "Rejoiceth more of that sheep"},
        {"ref": "Ezekiel 33:11", "note": "No pleasure in death of wicked"},
    ],
    "Luke:19:10": [
        {"ref": "Matthew 18:11", "note": "Come to save that which was lost"},
        {"ref": "1 Timothy 1:15", "note": "Christ came to save sinners"},
    ],
    "Luke:23:43": [
        {"ref": "2 Corinthians 12:4", "note": "Caught up into paradise"},
        {"ref": "Philippians 1:23", "note": "To be with Christ"},
    ],
    "Luke:24:46": [
        {"ref": "Acts 17:3", "note": "Christ must needs have suffered"},
        {"ref": "1 Corinthians 15:3", "note": "Christ died for our sins"},
    ],

    # John - Additional I AM statements and key passages
    "John:1:12": [
        {"ref": "Galatians 3:26", "note": "Children of God by faith"},
        {"ref": "1 John 3:1", "note": "That we should be called sons of God"},
    ],
    "John:1:14": [
        {"ref": "1 Timothy 3:16", "note": "God was manifest in the flesh"},
        {"ref": "Philippians 2:7", "note": "Made in likeness of men"},
    ],
    "John:4:24": [
        {"ref": "2 Corinthians 3:17", "note": "The Lord is that Spirit"},
        {"ref": "Philippians 3:3", "note": "Worship God in the spirit"},
    ],
    "John:5:24": [
        {"ref": "John 3:18", "note": "He that believeth is not condemned"},
        {"ref": "Romans 8:1", "note": "No condemnation"},
    ],
    "John:6:37": [
        {"ref": "John 6:44", "note": "No man can come except the Father draw him"},
        {"ref": "Matthew 11:28", "note": "Come unto me, all ye that labour"},
    ],
    "John:10:28": [
        {"ref": "John 10:29", "note": "None shall pluck them out"},
        {"ref": "Romans 8:38", "note": "Nothing shall separate us"},
    ],
    "John:14:1": [
        {"ref": "Philippians 4:6", "note": "Be careful for nothing"},
        {"ref": "1 Peter 5:7", "note": "Casting all your care upon him"},
    ],
    "John:14:2": [
        {"ref": "2 Corinthians 5:1", "note": "House not made with hands"},
        {"ref": "Hebrews 11:16", "note": "He hath prepared for them a city"},
    ],
    "John:14:16": [
        {"ref": "John 14:26", "note": "Comforter, the Holy Ghost"},
        {"ref": "John 15:26", "note": "Spirit of truth"},
    ],
    "John:16:33": [
        {"ref": "Romans 8:37", "note": "More than conquerors"},
        {"ref": "1 John 5:4", "note": "Overcometh the world"},
    ],
    "John:17:3": [
        {"ref": "1 John 5:20", "note": "This is the true God"},
        {"ref": "Jeremiah 9:24", "note": "Knoweth and understandeth me"},
    ],

    # Acts - Early Church
    "Acts:1:8": [
        {"ref": "Luke 24:49", "note": "Promise of my Father"},
        {"ref": "Acts 2:4", "note": "Filled with Holy Ghost"},
    ],
    "Acts:2:38": [
        {"ref": "Mark 1:15", "note": "Repent ye, and believe"},
        {"ref": "Acts 3:19", "note": "Repent ye therefore"},
    ],
    "Acts:4:12": [
        {"ref": "John 14:6", "note": "No man cometh unto the Father"},
        {"ref": "1 Timothy 2:5", "note": "One mediator"},
    ],
    "Acts:16:31": [
        {"ref": "John 3:16", "note": "Whosoever believeth"},
        {"ref": "Romans 10:9", "note": "Believe in thine heart"},
    ],
    "Acts:17:30": [
        {"ref": "Acts 3:19", "note": "Repent ye therefore"},
        {"ref": "2 Peter 3:9", "note": "All should come to repentance"},
    ],

    # Romans - Additional Doctrinal Passages
    "Romans:1:20": [
        {"ref": "Psalms 19:1", "note": "Heavens declare glory of God"},
        {"ref": "Acts 14:17", "note": "He left not himself without witness"},
    ],
    "Romans:2:11": [
        {"ref": "Acts 10:34", "note": "God is no respecter of persons"},
        {"ref": "Colossians 3:25", "note": "No respect of persons"},
    ],
    "Romans:4:5": [
        {"ref": "Romans 3:28", "note": "Justified by faith without deeds"},
        {"ref": "Galatians 2:16", "note": "Not justified by works of law"},
    ],
    "Romans:6:4": [
        {"ref": "Colossians 2:12", "note": "Buried with him in baptism"},
        {"ref": "Galatians 2:20", "note": "Crucified with Christ"},
    ],
    "Romans:7:24": [
        {"ref": "Philippians 3:21", "note": "Vile body"},
        {"ref": "2 Corinthians 5:4", "note": "Mortality swallowed up of life"},
    ],
    "Romans:10:17": [
        {"ref": "Galatians 3:2", "note": "By hearing of faith"},
        {"ref": "1 Peter 1:23", "note": "Born again by the word"},
    ],
    "Romans:12:2": [
        {"ref": "Ephesians 4:23", "note": "Renewed in spirit of your mind"},
        {"ref": "Colossians 3:10", "note": "Renewed in knowledge"},
    ],
    "Romans:13:1": [
        {"ref": "Titus 3:1", "note": "Subject to principalities"},
        {"ref": "1 Peter 2:13", "note": "Submit to every ordinance"},
    ],

    # 1 Corinthians - Additional Church Issues
    "1 Corinthians:1:18": [
        {"ref": "1 Corinthians 2:14", "note": "Natural man receiveth not"},
        {"ref": "Romans 1:16", "note": "Power of God unto salvation"},
    ],
    "1 Corinthians:3:16": [
        {"ref": "1 Corinthians 6:19", "note": "Your body is temple of Holy Ghost"},
        {"ref": "2 Corinthians 6:16", "note": "Ye are temple of living God"},
    ],
    "1 Corinthians:6:20": [
        {"ref": "1 Peter 1:18", "note": "Not redeemed with corruptible things"},
        {"ref": "Romans 12:1", "note": "Present your bodies"},
    ],
    "1 Corinthians:10:31": [
        {"ref": "Colossians 3:17", "note": "Do all in name of the Lord Jesus"},
        {"ref": "1 Peter 4:11", "note": "That God may be glorified"},
    ],
    "1 Corinthians:12:13": [
        {"ref": "Galatians 3:28", "note": "All one in Christ Jesus"},
        {"ref": "Ephesians 4:4", "note": "One body, one Spirit"},
    ],
    "1 Corinthians:15:58": [
        {"ref": "Galatians 6:9", "note": "Not be weary in well doing"},
        {"ref": "Hebrews 6:10", "note": "God is not unrighteous"},
    ],

    # 2 Corinthians - Ministry and Suffering
    "2 Corinthians:3:18": [
        {"ref": "Romans 8:29", "note": "Conformed to image of his Son"},
        {"ref": "Colossians 3:10", "note": "Renewed after image of him"},
    ],
    "2 Corinthians:4:6": [
        {"ref": "Genesis 1:3", "note": "Let there be light"},
        {"ref": "John 1:9", "note": "Lighteth every man"},
    ],
    "2 Corinthians:4:17": [
        {"ref": "Romans 8:18", "note": "Not worthy to be compared"},
        {"ref": "1 Peter 1:6", "note": "Though now for a season"},
    ],
    "2 Corinthians:5:8": [
        {"ref": "Philippians 1:23", "note": "Desire to depart and be with Christ"},
        {"ref": "Revelation 14:13", "note": "Blessed are dead which die in Lord"},
    ],
    "2 Corinthians:5:17": [
        {"ref": "Galatians 6:15", "note": "New creature"},
        {"ref": "Ephesians 4:24", "note": "Put on new man"},
    ],
    "2 Corinthians:5:21": [
        {"ref": "Isaiah 53:6", "note": "LORD hath laid on him iniquity"},
        {"ref": "1 Peter 2:24", "note": "Bare our sins"},
    ],
    "2 Corinthians:6:14": [
        {"ref": "Ephesians 5:11", "note": "No fellowship with works of darkness"},
        {"ref": "2 John 1:10", "note": "Receive him not into your house"},
    ],
    "2 Corinthians:9:7": [
        {"ref": "1 Chronicles 29:9", "note": "Offered willingly"},
        {"ref": "Romans 12:8", "note": "He that giveth, with simplicity"},
    ],
    "2 Corinthians:13:5": [
        {"ref": "2 Peter 1:10", "note": "Make your calling and election sure"},
        {"ref": "1 Corinthians 11:28", "note": "Let a man examine himself"},
    ],

    # Galatians - Freedom in Christ
    "Galatians:1:8": [
        {"ref": "1 John 4:1", "note": "Try the spirits"},
        {"ref": "2 John 1:10", "note": "Receive him not"},
    ],
    "Galatians:2:20": [
        {"ref": "Romans 6:6", "note": "Old man crucified with him"},
        {"ref": "Colossians 3:3", "note": "Ye are dead"},
    ],
    "Galatians:3:13": [
        {"ref": "2 Corinthians 5:21", "note": "Made sin for us"},
        {"ref": "1 Peter 2:24", "note": "Bare our sins"},
    ],
    "Galatians:3:28": [
        {"ref": "Colossians 3:11", "note": "Neither Greek nor Jew"},
        {"ref": "1 Corinthians 12:13", "note": "All baptized into one body"},
    ],
    "Galatians:5:1": [
        {"ref": "John 8:36", "note": "If Son make you free"},
        {"ref": "Romans 8:2", "note": "Free from law of sin and death"},
    ],
    "Galatians:5:22": [
        {"ref": "Ephesians 5:9", "note": "Fruit of the Spirit"},
        {"ref": "Colossians 1:10", "note": "Fruitful in every good work"},
    ],
    "Galatians:6:2": [
        {"ref": "Romans 15:1", "note": "Bear infirmities of the weak"},
        {"ref": "1 Thessalonians 5:14", "note": "Support the weak"},
    ],
    "Galatians:6:7": [
        {"ref": "Job 4:8", "note": "Plow iniquity, reap the same"},
        {"ref": "Proverbs 22:8", "note": "Soweth iniquity shall reap vanity"},
    ],

    # Ephesians - Additional Church Doctrine
    "Ephesians:1:4": [
        {"ref": "2 Thessalonians 2:13", "note": "Chosen from the beginning"},
        {"ref": "1 Peter 1:2", "note": "Elect according to foreknowledge"},
    ],
    "Ephesians:3:20": [
        {"ref": "Romans 16:25", "note": "Able to stablish you"},
        {"ref": "Jude 1:24", "note": "Able to keep you from falling"},
    ],
    "Ephesians:5:18": [
        {"ref": "Acts 2:4", "note": "Filled with the Holy Ghost"},
        {"ref": "Colossians 3:16", "note": "Let word of Christ dwell in you"},
    ],
    "Ephesians:5:25": [
        {"ref": "Colossians 3:19", "note": "Husbands, love your wives"},
        {"ref": "1 Peter 3:7", "note": "Giving honour unto the wife"},
    ],
    "Ephesians:6:1": [
        {"ref": "Colossians 3:20", "note": "Children, obey your parents"},
        {"ref": "Exodus 20:12", "note": "Honour thy father and mother"},
    ],
    "Ephesians:6:12": [
        {"ref": "2 Corinthians 10:4", "note": "Weapons of our warfare not carnal"},
        {"ref": "1 Peter 5:8", "note": "Devil walketh about"},
    ],

    # Philippians - Additional Joy Passages
    "Philippians:1:6": [
        {"ref": "1 Thessalonians 5:24", "note": "Faithful who will do it"},
        {"ref": "Jude 1:24", "note": "Able to keep you from falling"},
    ],
    "Philippians:1:21": [
        {"ref": "Galatians 2:20", "note": "Christ liveth in me"},
        {"ref": "2 Timothy 1:12", "note": "I know whom I have believed"},
    ],
    "Philippians:3:8": [
        {"ref": "Matthew 13:44", "note": "Sold all that he had"},
        {"ref": "Hebrews 11:26", "note": "Esteeming the reproach of Christ"},
    ],
    "Philippians:3:20": [
        {"ref": "Hebrews 11:13", "note": "Strangers and pilgrims"},
        {"ref": "1 Peter 2:11", "note": "Strangers and pilgrims"},
    ],
    "Philippians:4:4": [
        {"ref": "1 Thessalonians 5:16", "note": "Rejoice evermore"},
        {"ref": "1 Peter 1:8", "note": "Rejoice with joy unspeakable"},
    ],
    "Philippians:4:7": [
        {"ref": "John 14:27", "note": "My peace I give unto you"},
        {"ref": "Colossians 3:15", "note": "Let peace of God rule"},
    ],
    "Philippians:4:8": [
        {"ref": "Colossians 3:2", "note": "Set your affection on things above"},
        {"ref": "Romans 12:2", "note": "Be transformed by renewing of mind"},
    ],
    "Philippians:4:19": [
        {"ref": "Matthew 6:33", "note": "All these things shall be added"},
        {"ref": "Psalms 23:1", "note": "I shall not want"},
    ],

    # Colossians - Christ's Supremacy
    "Colossians:1:16": [
        {"ref": "John 1:3", "note": "All things were made by him"},
        {"ref": "Hebrews 1:2", "note": "By whom he made the worlds"},
    ],
    "Colossians:2:9": [
        {"ref": "John 1:14", "note": "Word was made flesh"},
        {"ref": "1 Timothy 3:16", "note": "God manifest in flesh"},
    ],
    "Colossians:2:14": [
        {"ref": "Ephesians 2:15", "note": "Abolished the law"},
        {"ref": "Hebrews 7:18", "note": "Disannulling of commandment"},
    ],
    "Colossians:3:1": [
        {"ref": "Romans 6:4", "note": "Walk in newness of life"},
        {"ref": "Ephesians 2:6", "note": "Raised us up together"},
    ],
    "Colossians:3:23": [
        {"ref": "Ephesians 6:7", "note": "Doing service as to the Lord"},
        {"ref": "1 Corinthians 10:31", "note": "Do all to glory of God"},
    ],

    # 1 Thessalonians - Second Coming
    "1 Thessalonians:4:16": [
        {"ref": "1 Corinthians 15:52", "note": "Trumpet shall sound"},
        {"ref": "Revelation 11:15", "note": "Seventh angel sounded"},
    ],
    "1 Thessalonians:5:2": [
        {"ref": "2 Peter 3:10", "note": "Day of Lord as thief"},
        {"ref": "Revelation 16:15", "note": "I come as a thief"},
    ],
    "1 Thessalonians:5:17": [
        {"ref": "Luke 18:1", "note": "Men ought always to pray"},
        {"ref": "Ephesians 6:18", "note": "Praying always"},
    ],

    # 2 Thessalonians - Steadfastness
    "2 Thessalonians:2:3": [
        {"ref": "1 Timothy 4:1", "note": "Depart from the faith"},
        {"ref": "2 Timothy 3:1", "note": "Perilous times shall come"},
    ],
    "2 Thessalonians:3:3": [
        {"ref": "1 Corinthians 10:13", "note": "God is faithful"},
        {"ref": "2 Timothy 2:13", "note": "He abideth faithful"},
    ],

    # 1 Timothy - Church Order
    "1 Timothy:2:5": [
        {"ref": "John 14:6", "note": "No man cometh unto Father but by me"},
        {"ref": "Acts 4:12", "note": "None other name"},
    ],
    "1 Timothy:3:16": [
        {"ref": "John 1:14", "note": "Word was made flesh"},
        {"ref": "Colossians 2:9", "note": "Fulness of Godhead bodily"},
    ],
    "1 Timothy:4:12": [
        {"ref": "Titus 2:7", "note": "Pattern of good works"},
        {"ref": "1 Peter 5:3", "note": "Ensamples to the flock"},
    ],
    "1 Timothy:6:6": [
        {"ref": "Philippians 4:11", "note": "Learned to be content"},
        {"ref": "Hebrews 13:5", "note": "Be content with such things"},
    ],

    # 2 Timothy - Endurance
    "2 Timothy:1:7": [
        {"ref": "Romans 8:15", "note": "Not received spirit of bondage"},
        {"ref": "1 John 4:18", "note": "Perfect love casteth out fear"},
    ],
    "2 Timothy:2:15": [
        {"ref": "Acts 17:11", "note": "Searched scriptures daily"},
        {"ref": "2 Peter 1:19", "note": "Take heed unto prophecy"},
    ],
    "2 Timothy:3:15": [
        {"ref": "John 5:39", "note": "Search the scriptures"},
        {"ref": "Romans 15:4", "note": "Written for our learning"},
    ],
    "2 Timothy:3:16": [
        {"ref": "2 Peter 1:21", "note": "Holy men spake as moved by Holy Ghost"},
        {"ref": "Hebrews 1:1", "note": "God spake by the prophets"},
    ],
    "2 Timothy:4:7": [
        {"ref": "Philippians 3:14", "note": "Press toward the mark"},
        {"ref": "1 Corinthians 9:24", "note": "So run that ye may obtain"},
    ],

    # Titus - Sound Doctrine
    "Titus:2:13": [
        {"ref": "Philippians 3:20", "note": "Look for the Saviour"},
        {"ref": "1 Thessalonians 1:10", "note": "Wait for his Son from heaven"},
    ],
    "Titus:3:5": [
        {"ref": "Ephesians 2:8", "note": "Not of works"},
        {"ref": "Romans 3:24", "note": "Justified freely by grace"},
    ],

    # Hebrews - Additional Christ's Superiority
    "Hebrews:2:14": [
        {"ref": "1 John 3:8", "note": "Destroy works of devil"},
        {"ref": "Colossians 2:15", "note": "Spoiled principalities"},
    ],
    "Hebrews:7:25": [
        {"ref": "Romans 8:34", "note": "Christ maketh intercession"},
        {"ref": "1 John 2:1", "note": "Advocate with the Father"},
    ],
    "Hebrews:9:27": [
        {"ref": "Genesis 3:19", "note": "Dust thou art, to dust return"},
        {"ref": "Ecclesiastes 12:7", "note": "Dust return to earth"},
    ],
    "Hebrews:10:25": [
        {"ref": "Acts 2:42", "note": "Continued stedfast"},
        {"ref": "1 Corinthians 16:2", "note": "First day of week"},
    ],
    "Hebrews:11:6": [
        {"ref": "Romans 10:17", "note": "Faith cometh by hearing"},
        {"ref": "John 20:29", "note": "Blessed are they that have not seen"},
    ],
    "Hebrews:12:2": [
        {"ref": "Philippians 2:8", "note": "Obedient unto death"},
        {"ref": "1 Peter 2:21", "note": "Christ suffered for us"},
    ],
    "Hebrews:12:6": [
        {"ref": "Proverbs 3:11", "note": "Despise not chastening"},
        {"ref": "Revelation 3:19", "note": "As many as I love, I rebuke"},
    ],
    "Hebrews:12:14": [
        {"ref": "Matthew 5:8", "note": "Pure in heart shall see God"},
        {"ref": "1 Thessalonians 4:7", "note": "Not called unto uncleanness"},
    ],

    # James - Additional Faith and Works
    "James:1:2": [
        {"ref": "1 Peter 1:6", "note": "Rejoice though in heaviness"},
        {"ref": "Romans 5:3", "note": "Glory in tribulations"},
    ],
    "James:1:5": [
        {"ref": "1 Kings 3:9", "note": "Give thy servant understanding heart"},
        {"ref": "Proverbs 2:3", "note": "Criest after knowledge"},
    ],
    "James:1:12": [
        {"ref": "Revelation 2:10", "note": "Crown of life"},
        {"ref": "2 Timothy 4:8", "note": "Crown of righteousness"},
    ],
    "James:4:6": [
        {"ref": "1 Peter 5:5", "note": "God resisteth the proud"},
        {"ref": "Proverbs 3:34", "note": "Giveth grace unto lowly"},
    ],
    "James:5:16": [
        {"ref": "1 John 1:9", "note": "Confess your faults"},
        {"ref": "Proverbs 28:13", "note": "Whoso confesseth shall have mercy"},
    ],

    # 1 Peter - Additional Suffering
    "1 Peter:1:16": [
        {"ref": "Leviticus 11:44", "note": "Be ye holy; for I am holy"},
        {"ref": "Leviticus 19:2", "note": "Holy: for I the LORD am holy"},
    ],
    "1 Peter:2:9": [
        {"ref": "Exodus 19:6", "note": "Kingdom of priests"},
        {"ref": "Revelation 1:6", "note": "Made us kings and priests"},
    ],
    "1 Peter:3:15": [
        {"ref": "Colossians 4:6", "note": "Speech be alway with grace"},
        {"ref": "2 Timothy 2:15", "note": "Rightly dividing the word"},
    ],
    "1 Peter:4:8": [
        {"ref": "Proverbs 10:12", "note": "Love covereth all sins"},
        {"ref": "James 5:20", "note": "Hide a multitude of sins"},
    ],

    # 2 Peter - False Teachers
    "2 Peter:1:4": [
        {"ref": "2 Corinthians 3:18", "note": "Changed into same image"},
        {"ref": "1 John 3:2", "note": "We shall be like him"},
    ],
    "2 Peter:3:9": [
        {"ref": "1 Timothy 2:4", "note": "Will have all to be saved"},
        {"ref": "Ezekiel 33:11", "note": "No pleasure in death of wicked"},
    ],
    "2 Peter:3:18": [
        {"ref": "Colossians 1:10", "note": "Increasing in knowledge"},
        {"ref": "2 Corinthians 3:18", "note": "Changed from glory to glory"},
    ],

    # 1 John - Additional Love and Assurance
    "1 John:1:8": [
        {"ref": "Romans 3:23", "note": "All have sinned"},
        {"ref": "1 Kings 8:46", "note": "No man that sinneth not"},
    ],
    "1 John:2:6": [
        {"ref": "1 Peter 2:21", "note": "Follow his steps"},
        {"ref": "John 13:15", "note": "Ye should do as I have done"},
    ],
    "1 John:3:2": [
        {"ref": "Philippians 3:21", "note": "Fashion our vile body"},
        {"ref": "Colossians 3:4", "note": "Appear with him in glory"},
    ],
    "1 John:4:10": [
        {"ref": "Romans 5:8", "note": "God commendeth his love"},
        {"ref": "John 3:16", "note": "God so loved the world"},
    ],
    "1 John:4:19": [
        {"ref": "Romans 5:5", "note": "Love of God shed abroad"},
        {"ref": "2 Corinthians 5:14", "note": "Love of Christ constraineth"},
    ],
    "1 John:5:13": [
        {"ref": "John 20:31", "note": "That ye might have life"},
        {"ref": "1 John 1:4", "note": "That your joy may be full"},
    ],

    # Jude - Contend for the Faith
    "Jude:1:3": [
        {"ref": "Philippians 1:27", "note": "Striving for the faith"},
        {"ref": "1 Timothy 6:12", "note": "Fight the good fight"},
    ],
    "Jude:1:24": [
        {"ref": "John 10:28", "note": "None shall pluck them out"},
        {"ref": "1 Peter 1:5", "note": "Kept by power of God"},
    ],

    # Revelation - Additional Apocalyptic Passages
    "Revelation:1:7": [
        {"ref": "Matthew 24:30", "note": "Coming in clouds"},
        {"ref": "Zechariah 12:10", "note": "Look on him whom they pierced"},
    ],
    "Revelation:1:18": [
        {"ref": "John 11:25", "note": "I am the resurrection and the life"},
        {"ref": "Romans 6:9", "note": "Death hath no more dominion"},
    ],
    "Revelation:5:9": [
        {"ref": "1 Peter 1:18", "note": "Redeemed with precious blood"},
        {"ref": "Ephesians 1:7", "note": "Redemption through his blood"},
    ],
    "Revelation:19:16": [
        {"ref": "1 Timothy 6:15", "note": "King of kings, Lord of lords"},
        {"ref": "Deuteronomy 10:17", "note": "God of gods, Lord of lords"},
    ],
    "Revelation:20:12": [
        {"ref": "Daniel 7:10", "note": "Books were opened"},
        {"ref": "John 5:28", "note": "All shall hear his voice"},
    ],
    "Revelation:22:20": [
        {"ref": "1 Corinthians 16:22", "note": "Maranatha (Lord cometh)"},
        {"ref": "Philippians 4:5", "note": "The Lord is at hand"},
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
