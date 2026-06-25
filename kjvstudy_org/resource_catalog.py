"""Single source of truth for the theological resource catalog.

Consumed by the /resources page, the homepage, and universal search so the
three never drift. Each entry: name, url, description, count (+ optional badge).
"""

RESOURCE_CATEGORIES = {
    "People": [
        {
            "name": "Biblical Prophets",
            "url": "/biblical-prophets",
            "description": "Explore the prophetic ministry throughout Scripture, from Isaiah to Malachi",
            "count": "9 prophets"
        },
        {
            "name": "The Twelve Apostles",
            "url": "/the-twelve-apostles",
            "description": "The twelve disciples chosen by Jesus to be witnesses of His ministry",
            "count": "12 apostles"
        },
        {
            "name": "Women of the Bible",
            "url": "/women-of-the-bible",
            "description": "Notable women of Scripture and their significance in redemptive history",
            "count": "12 women"
        }
    ],
    "Theology": [
        {
            "name": "Biblical Angels",
            "url": "/biblical-angels",
            "description": "Angelic beings mentioned in Scripture, including Michael, Gabriel, and the heavenly host",
            "count": "12 entries"
        },
        {
            "name": "The Tetragrammaton",
            "url": "/tetragrammaton",
            "description": "The sacred four-letter name of God (YHWH) and its profound significance",
            "count": "Deep dive"
        },
        {
            "name": "Names of God",
            "url": "/names-of-god",
            "description": "The revelation of God's names throughout Scripture and their meanings",
            "count": "14 names"
        },
        {
            "name": "Parables of Jesus",
            "url": "/parables",
            "description": "The parables spoken by Christ to illustrate spiritual truths",
            "count": "11 parables"
        },
        {
            "name": "Miracles of Jesus",
            "url": "/miracles-of-jesus",
            "description": "Signs and wonders manifesting divine authority over nature, disease, demons, and death",
            "count": "35+ miracles"
        },
        {
            "name": "I Am Statements",
            "url": "/i-am-statements",
            "description": "The seven 'I Am' statements of Jesus in John's Gospel revealing His divine nature",
            "count": "7 statements"
        },
        {
            "name": "The Beatitudes",
            "url": "/beatitudes",
            "description": "The blessings proclaimed by Jesus in the Sermon on the Mount",
            "count": "8 beatitudes"
        },
        {
            "name": "Ten Commandments",
            "url": "/ten-commandments",
            "description": "The moral law given by God to Moses on Mount Sinai",
            "count": "10 commandments"
        },
        {
            "name": "Armor of God",
            "url": "/armor-of-god",
            "description": "The spiritual equipment for warfare described in Ephesians 6",
            "count": "7 pieces"
        },
        {
            "name": "Prayers of the Bible",
            "url": "/prayers-of-the-bible",
            "description": "Sacred prayers from the Psalms, Jesus, Paul, and the early church",
            "count": "20+ prayers"
        },
        {
            "name": "Biblical Covenants",
            "url": "/biblical-covenants",
            "description": "Divine covenants established between God and His people",
            "count": "7 covenants"
        },
        {
            "name": "Fruits of the Spirit",
            "url": "/fruits-of-the-spirit",
            "description": "The nine graces of Galatians 5:22-23 manifested in believers through the Holy Spirit",
            "count": "9 fruits"
        }
    ],
    "Systematic Theology": [
        {
            "name": "The Trinity",
            "url": "/trinity",
            "description": "The mystery of God revealed as Father, Son, and Holy Spirit—three Persons, one God",
            "count": "4 categories"
        },
        {
            "name": "Christology",
            "url": "/christology",
            "description": "The Person and work of Jesus Christ—His deity, humanity, and offices",
            "count": "4 categories"
        },
        {
            "name": "Pneumatology",
            "url": "/pneumatology",
            "description": "The doctrine of the Holy Spirit—His Person, deity, and work in believers",
            "count": "4 categories"
        },
        {
            "name": "Soteriology",
            "url": "/soteriology",
            "description": "The doctrine of salvation—from election to glorification",
            "count": "5 categories"
        },
        {
            "name": "Ecclesiology",
            "url": "/ecclesiology",
            "description": "The doctrine of the Church—its nature, mission, and governance",
            "count": "4 categories"
        },
        {
            "name": "Eschatology",
            "url": "/eschatology",
            "description": "The doctrine of last things—Christ's return, judgment, and eternal state",
            "count": "5 categories"
        },
        {
            "name": "The Kingdom of God",
            "url": "/kingdom-of-god",
            "description": "God's sovereign reign inaugurated in Christ and consummated at His return",
            "count": "5 categories"
        },
        {
            "name": "Types and Shadows",
            "url": "/types-and-shadows",
            "description": "Old Testament persons, events, and institutions that prefigure Christ",
            "count": "5 categories"
        },
        {
            "name": "Messianic Prophecies",
            "url": "/messianic-prophecies",
            "description": "Old Testament prophecies fulfilled in Jesus Christ",
            "count": "5 categories"
        },
        {
            "name": "The Blood in Scripture",
            "url": "/blood-in-scripture",
            "description": "The theology of blood, sacrifice, and redemption throughout Scripture",
            "count": "5 categories"
        },
        {
            "name": "Names and Titles of Christ",
            "url": "/names-of-christ",
            "description": "The names and titles ascribed to Jesus revealing His Person and work",
            "count": "5 categories"
        },
        {
            "name": "Spirits & Demons",
            "url": "/spirits-and-demons",
            "description": "Biblical demonology—Satan, evil spirits, Legion, and spiritual warfare",
            "count": "7 categories"
        },
        {
            "name": "Personifications",
            "url": "/personifications",
            "description": "Abstract concepts given human form—Wisdom, Folly, Death, Sin, and more",
            "count": "6 categories"
        },
        {
            "name": "Bibliology",
            "url": "/bibliology",
            "description": "The Doctrine of Scripture—inspiration, authority, sufficiency, and preservation",
            "count": "4 categories"
        },
        {
            "name": "Theology Proper",
            "url": "/theology-proper",
            "description": "The Attributes of God—His incommunicable and communicable perfections",
            "count": "4 categories"
        },
        {
            "name": "Anthropology",
            "url": "/anthropology",
            "description": "The Doctrine of Man—creation, constitution, and condition of humanity",
            "count": "4 categories"
        },
        {
            "name": "Hamartiology",
            "url": "/hamartiology",
            "description": "The Doctrine of Sin—its origin, nature, transmission, and consequences",
            "count": "4 categories"
        },
        {
            "name": "Providence",
            "url": "/providence",
            "description": "Divine Providence—God's preservation, governance, and concurrence in all things",
            "count": "4 categories"
        },
        {
            "name": "Grace",
            "url": "/grace",
            "description": "The Doctrine of Grace—common grace, effectual grace, election, and perseverance",
            "count": "4 categories"
        },
        {
            "name": "Justification",
            "url": "/justification",
            "description": "The Doctrine of Justification—declared righteous through faith in Christ alone",
            "count": "4 categories"
        },
        {
            "name": "Sanctification",
            "url": "/sanctification",
            "description": "The Doctrine of Sanctification—progressive holiness through the Spirit",
            "count": "4 categories"
        },
        {
            "name": "Law and Gospel",
            "url": "/law-and-gospel",
            "description": "The distinction between Law and Gospel—God's demands and His gracious provision",
            "count": "4 categories"
        },
        {
            "name": "Worship",
            "url": "/worship",
            "description": "The Doctrine of Worship—regulative principle, elements, and the heart of worship",
            "count": "4 categories"
        }
    ],
    "History & Culture": [
        {
            "name": "Biblical Festivals",
            "url": "/biblical-festivals",
            "description": "The appointed feasts and holy days ordained in the Law of Moses",
            "count": "7 festivals"
        },
        {
            "name": "Biblical Geography",
            "url": "/biblical-maps",
            "description": "Locations mentioned in Scripture and their historical significance",
            "count": "Maps & places",
            "badge": "Interactive"
        },
        {
            "name": "Biblical Timeline",
            "url": "/biblical-timeline",
            "description": "Chronological overview of biblical events from Creation to Revelation",
            "count": "Timeline"
        },
        {
            "name": "Genealogies",
            "url": "/family-tree",
            "description": "Interactive family tree from Adam to Jesus Christ with detailed person profiles",
            "count": "160+ people",
            "badge": "Interactive"
        }
    ],
    "Study Tools": [
        {
            "name": "Study Guides",
            "url": "/study-guides",
            "description": "In-depth guides for studying biblical books, themes, and doctrines",
            "count": "Multiple guides"
        }
    ]
}


# Extra search synonyms keyed by resource url, to widen findability beyond the
# display name. Entries without a row are still searchable by their name.
RESOURCE_SEARCH_KEYWORDS = {
    "/trinity": "godhead three persons father son spirit",
    "/christology": "jesus christ lord savior messiah",
    "/soteriology": "salvation saved redemption atonement",
    "/pneumatology": "holy spirit ghost comforter paraclete",
    "/eschatology": "end times last days rapture tribulation millennium",
    "/ecclesiology": "church body believers congregation",
    "/types-and-shadows": "typology foreshadow prefigure",
    "/messianic-prophecies": "prophecy predictions foretold",
    "/blood-in-scripture": "sacrifice atonement covering",
    "/kingdom-of-god": "reign throne rule",
    "/names-of-christ": "jesus titles lord savior",
    "/spirits-and-demons": "devils satan evil unclean",
    "/personifications": "wisdom folly death",
    "/bibliology": "doctrine of scripture inspiration inerrancy authority",
    "/theology-proper": "attributes of god nature character",
    "/anthropology": "doctrine of man humanity image of god",
    "/hamartiology": "doctrine of sin fall depravity",
    "/providence": "preservation governance sovereignty",
    "/grace": "common grace effectual election perseverance",
    "/justification": "declared righteous faith alone imputation",
    "/sanctification": "holiness progressive growth spirit",
    "/law-and-gospel": "law gospel demands provision",
    "/worship": "regulative principle praise reverence",
    "/biblical-angels": "cherubim seraphim michael gabriel angelology",
    "/tetragrammaton": "yhwh yahweh jehovah lord",
    "/names-of-god": "yahweh jehovah el shaddai adonai",
    "/parables": "stories teachings",
    "/miracles-of-jesus": "healing signs wonders",
    "/i-am-statements": "bread light door shepherd resurrection way truth life vine",
    "/beatitudes": "blessed sermon mount",
    "/ten-commandments": "decalogue law sinai",
    "/armor-of-god": "warfare helmet breastplate shield sword",
    "/prayers-of-the-bible": "lord's prayer model",
    "/biblical-covenants": "abrahamic mosaic davidic new",
    "/fruits-of-the-spirit": "love joy peace patience kindness goodness faithfulness gentleness self-control",
    "/biblical-prophets": "elijah elisha isaiah jeremiah ezekiel daniel",
    "/the-twelve-apostles": "disciples twelve peter james john",
    "/women-of-the-bible": "ruth esther mary martha rahab",
    "/biblical-festivals": "passover pentecost tabernacles feast",
    "/biblical-maps": "geography places locations maps",
    "/biblical-timeline": "chronology history dates",
    "/family-tree": "genealogy lineage ancestors descendants",
    "/study-guides": "guides themes doctrines",
}


def iter_resources():
    """Yield every resource entry across all catalog categories."""
    for items in RESOURCE_CATEGORIES.values():
        yield from items
