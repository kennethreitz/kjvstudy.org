"""Biblical resources routes - maps, angels, prophets, names of God, etc.

These routes handle the biblical reference and study resources pages.
Data is imported from the centralized data module to avoid duplication.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from ..data import (
    BIBLICAL_LOCATIONS,
    ANGELS_DATA,
    PROPHETS_DATA,
    NAMES_DATA,
    PARABLES_DATA,
    COVENANTS_DATA,
    APOSTLES_DATA,
    WOMEN_DATA,
    FESTIVALS_DATA,
    FRUITS_DATA,
)
from ..utils.helpers import create_slug

router = APIRouter(tags=["Biblical Resources"])

# Templates will be set by the main app
templates = None


def init_templates(app_templates):
    """Initialize templates from the main app."""
    global templates
    templates = app_templates


def get_books():
    """Get list of Bible books."""
    from ..kjv import bible
    return list(bible.iter_books())


def find_item_by_slug(data: dict, slug: str):
    """Find an item in a nested data structure by its slug."""
    for category_name, category in data.items():
        for item_name, item_data in category.items():
            if create_slug(item_name) == slug:
                return item_data, item_name, category_name
    return None, None, None


# ============================================================================
# BIBLICAL MAPS
# ============================================================================
@router.get("/biblical-maps", response_class=HTMLResponse)
def biblical_maps_page(request: Request):
    """Biblical maps page showing important biblical locations."""
    return templates.TemplateResponse(
            request,
            "biblical_maps.html",
            {
            "books": get_books(),
            "biblical_locations": BIBLICAL_LOCATIONS,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Geography", "url": None}
            ]
        }
    )


# ============================================================================
# BIBLICAL ANGELS
# ============================================================================
@router.get("/biblical-angels", response_class=HTMLResponse)
def biblical_angels_page(request: Request):
    """Biblical angels page exploring angels throughout Scripture."""
    return templates.TemplateResponse(
            request,
            "biblical_angels.html",
            {
            "books": get_books(),
            "angels_data": ANGELS_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Angels", "url": None}
            ]
        }
    )


@router.get("/biblical-angels/{angel_slug}", response_class=HTMLResponse)
def angel_detail(request: Request, angel_slug: str):
    """Individual biblical angels detail page."""
    item, item_name, category_name = find_item_by_slug(ANGELS_DATA, angel_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Biblical Angels item not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Biblical Angels",
            "back_url": "/biblical-angels",
            "back_text": "Biblical Angels",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Angels", "url": "/biblical-angels"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# BIBLICAL PROPHETS
# ============================================================================
@router.get("/biblical-prophets", response_class=HTMLResponse)
def biblical_prophets_page(request: Request):
    """Biblical prophets page exploring the prophetic ministry throughout Scripture."""
    return templates.TemplateResponse(
            request,
            "biblical_prophets.html",
            {
            "books": get_books(),
            "prophets_data": PROPHETS_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Prophets", "url": None}
            ]
        }
    )


@router.get("/biblical-prophets/{prophet_slug}", response_class=HTMLResponse)
def prophet_detail(request: Request, prophet_slug: str):
    """Individual biblical prophets detail page."""
    item, item_name, category_name = find_item_by_slug(PROPHETS_DATA, prophet_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Biblical Prophets item not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Biblical Prophets",
            "back_url": "/biblical-prophets",
            "back_text": "Biblical Prophets",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Prophets", "url": "/biblical-prophets"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# NAMES OF GOD
# ============================================================================
@router.get("/names-of-god", response_class=HTMLResponse)
def names_of_god_page(request: Request):
    """Names of God page exploring divine names throughout Scripture."""
    return templates.TemplateResponse(
            request,
            "names_of_god.html",
            {
            "books": get_books(),
            "names_data": NAMES_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Names of God", "url": None}
            ]
        }
    )


@router.get("/names-of-god/{name_slug}", response_class=HTMLResponse)
def name_of_god_detail(request: Request, name_slug: str):
    """Individual name of God detail page."""
    item, item_name, category_name = find_item_by_slug(NAMES_DATA, name_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Name of God not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Names of God",
            "back_url": "/names-of-god",
            "back_text": "Names of God",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Names of God", "url": "/names-of-god"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# PARABLES
# ============================================================================
@router.get("/parables", response_class=HTMLResponse)
def parables_page(request: Request):
    """Parables of Jesus page."""
    return templates.TemplateResponse(
            request,
            "parables.html",
            {
            "books": get_books(),
            "parables_data": PARABLES_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Parables of Jesus", "url": None}
            ]
        }
    )


@router.get("/parables/{parable_slug}", response_class=HTMLResponse)
def parable_detail(request: Request, parable_slug: str):
    """Individual parable detail page."""
    item, item_name, category_name = find_item_by_slug(PARABLES_DATA, parable_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Parable not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Parables of Jesus",
            "back_url": "/parables",
            "back_text": "Parables of Jesus",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Parables of Jesus", "url": "/parables"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# BIBLICAL COVENANTS
# ============================================================================
@router.get("/biblical-covenants", response_class=HTMLResponse)
def biblical_covenants_page(request: Request):
    """Biblical covenants page."""
    return templates.TemplateResponse(
            request,
            "biblical_covenants.html",
            {
            "books": get_books(),
            "covenants_data": COVENANTS_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Covenants", "url": None}
            ]
        }
    )


@router.get("/biblical-covenants/{covenant_slug}", response_class=HTMLResponse)
def covenant_detail(request: Request, covenant_slug: str):
    """Individual covenant detail page."""
    item, item_name, category_name = find_item_by_slug(COVENANTS_DATA, covenant_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Biblical Covenant not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Biblical Covenants",
            "back_url": "/biblical-covenants",
            "back_text": "Biblical Covenants",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Covenants", "url": "/biblical-covenants"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# THE TWELVE APOSTLES
# ============================================================================
@router.get("/the-twelve-apostles", response_class=HTMLResponse)
def apostles_page(request: Request):
    """The Twelve Apostles page."""
    return templates.TemplateResponse(
            request,
            "twelve_apostles.html",
            {
            "books": get_books(),
            "apostles_data": APOSTLES_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "The Twelve Apostles", "url": None}
            ]
        }
    )


@router.get("/the-twelve-apostles/{apostle_slug}", response_class=HTMLResponse)
def apostle_detail(request: Request, apostle_slug: str):
    """Individual apostle detail page."""
    item, item_name, category_name = find_item_by_slug(APOSTLES_DATA, apostle_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Apostle not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "The Twelve Apostles",
            "back_url": "/the-twelve-apostles",
            "back_text": "The Twelve Apostles",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "The Twelve Apostles", "url": "/the-twelve-apostles"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# WOMEN OF THE BIBLE
# ============================================================================
@router.get("/women-of-the-bible", response_class=HTMLResponse)
def women_of_the_bible_page(request: Request):
    """Women of the Bible page."""
    return templates.TemplateResponse(
            request,
            "women_of_the_bible.html",
            {
            "books": get_books(),
            "women_data": WOMEN_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Women of the Bible", "url": None}
            ]
        }
    )


@router.get("/women-of-the-bible/{woman_slug}", response_class=HTMLResponse)
def woman_detail(request: Request, woman_slug: str):
    """Individual woman of the Bible detail page."""
    item, item_name, category_name = find_item_by_slug(WOMEN_DATA, woman_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Woman of the Bible not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Women of the Bible",
            "back_url": "/women-of-the-bible",
            "back_text": "Women of the Bible",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Women of the Bible", "url": "/women-of-the-bible"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# BIBLICAL FESTIVALS
# ============================================================================
@router.get("/biblical-festivals", response_class=HTMLResponse)
def biblical_festivals_page(request: Request):
    """Biblical festivals page."""
    return templates.TemplateResponse(
            request,
            "biblical_festivals.html",
            {
            "books": get_books(),
            "festivals_data": FESTIVALS_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Festivals", "url": None}
            ]
        }
    )


@router.get("/biblical-festivals/{festival_slug}", response_class=HTMLResponse)
def festival_detail(request: Request, festival_slug: str):
    """Individual biblical festival detail page."""
    item, item_name, category_name = find_item_by_slug(FESTIVALS_DATA, festival_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Biblical Festival not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Biblical Festivals",
            "back_url": "/biblical-festivals",
            "back_text": "Biblical Festivals",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Biblical Festivals", "url": "/biblical-festivals"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# FRUITS OF THE SPIRIT
# ============================================================================
@router.get("/fruits-of-the-spirit", response_class=HTMLResponse)
def fruits_of_the_spirit_page(request: Request):
    """Fruits of the Spirit page."""
    return templates.TemplateResponse(
            request,
            "fruits_of_spirit.html",
            {
            "books": get_books(),
            "fruits_data": FRUITS_DATA,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Fruits of the Spirit", "url": None}
            ]
        }
    )


@router.get("/fruits-of-the-spirit/{fruit_slug}", response_class=HTMLResponse)
def fruit_detail(request: Request, fruit_slug: str):
    """Individual fruit of the Spirit detail page."""
    item, item_name, category_name = find_item_by_slug(FRUITS_DATA, fruit_slug)

    if not item:
        raise HTTPException(status_code=404, detail="Fruit of the Spirit not found")

    return templates.TemplateResponse(
            request,
            "resource_detail.html",
            {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": "Fruits of the Spirit",
            "back_url": "/fruits-of-the-spirit",
            "back_text": "Fruits of the Spirit",
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Fruits of the Spirit", "url": "/fruits-of-the-spirit"},
                {"text": item_name, "url": None}
            ]
        }
    )


# ============================================================================
# TETRAGRAMMATON (Special page with inline content)
# ============================================================================
TETRAGRAMMATON_CONTENT = {
    "title": "The Tetragrammaton: יהוה",
    "subtitle": "The Sacred Four-Letter Name of God",
    "introduction": "The Tetragrammaton—from Greek <em>tetra</em> ('four') and <em>gramma</em> ('letter')—refers to the four Hebrew consonants יהוה (yod-he-vav-he) that constitute God's most sacred, intimate, and frequently used name in Scripture. This name appears approximately 6,828 times in the Hebrew Bible, far exceeding all other divine designations combined. Yet its precise pronunciation was lost centuries ago when Jewish reverence for God's holiness led to the practice of substituting <em>Adonai</em> ('Lord') whenever the name appeared in public reading.",
    "sections": [
        {
            "heading": "The Hebrew Letters and Original Pronunciation",
            "content": "The four consonants comprising the Tetragrammaton are יהוה, transliterated as YHWH or JHVH. From right to left in Hebrew: yod (י), he (ה), vav (ו), he (ה). Ancient Hebrew was written without vowels; readers supplied vowel sounds from context and oral tradition.",
            "verses": [
                {"reference": "Exodus 3:13-15", "text": "And Moses said unto God, Behold, when I come unto the children of Israel, and shall say unto them, The God of your fathers hath sent me unto you; and they shall say to me, What is his name? what shall I say unto them? And God said unto Moses, I AM THAT I AM: and he said, Thus shalt thou say unto the children of Israel, I AM hath sent me unto you."}
            ]
        },
        {
            "heading": "Etymology and Theological Meaning",
            "content": "The Tetragrammaton derives from the Hebrew verb הָיָה (hayah), meaning 'to be,' 'to exist,' 'to become.' God's self-revelation at the burning bush—'I AM THAT I AM'—employs the first-person imperfect form of this verb.",
            "verses": [
                {"reference": "Exodus 6:2-8", "text": "And God spake unto Moses, and said unto him, I am the LORD: and I appeared unto Abraham, unto Isaac, and unto Jacob, by the name of God Almighty, but by my name JEHOVAH was I not known to them."},
                {"reference": "Psalm 90:2", "text": "Before the mountains were brought forth, or ever thou hadst formed the earth and the world, even from everlasting to everlasting, thou art God."}
            ]
        },
        {
            "heading": "Jewish Reverence and the Practice of Substitution",
            "content": "The Tetragrammaton's sacredness in Jewish tradition stems from the third commandment. By the intertestamental period, YHWH was pronounced only by priests during temple service.",
            "verses": [
                {"reference": "Exodus 20:7", "text": "Thou shalt not take the name of the LORD thy God in vain; for the LORD will not hold him guiltless that taketh his name in vain."},
                {"reference": "Psalm 111:9", "text": "He sent redemption unto his people: he hath commanded his covenant for ever: holy and reverend is his name."}
            ]
        },
        {
            "heading": "Christ and the Tetragrammaton",
            "content": "The New Testament reveals a stunning identification: Jesus Christ claims the prerogatives, honors, and identity associated with YHWH.",
            "verses": [
                {"reference": "John 8:56-59", "text": "Your father Abraham rejoiced to see my day: and he saw it, and was glad. Then said the Jews unto him, Thou art not yet fifty years old, and hast thou seen Abraham? Jesus said unto them, Verily, verily, I say unto you, Before Abraham was, I am."},
                {"reference": "Philippians 2:9-11", "text": "Wherefore God also hath highly exalted him, and given him a name which is above every name: that at the name of Jesus every knee should bow."},
                {"reference": "Revelation 1:8", "text": "I am Alpha and Omega, the beginning and the ending, saith the Lord, which is, and which was, and which is to come, the Almighty."}
            ]
        }
    ],
    "conclusion": "The Tetragrammaton stands at the center of biblical revelation—the name by which the eternal, self-existent, unchangeable God revealed Himself to Israel, redeemed His people from bondage, established covenant relationship, and ultimately became incarnate in Jesus Christ."
}


@router.get("/tetragrammaton", response_class=HTMLResponse)
def tetragrammaton_page(request: Request):
    """The sacred Tetragrammaton - YHWH."""
    return templates.TemplateResponse(
            request,
            "tetragrammaton.html",
            {
            "books": get_books(),
            "content": TETRAGRAMMATON_CONTENT,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Tetragrammaton", "url": None}
            ]
        }
    )
