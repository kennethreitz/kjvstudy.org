"""Biblical resources routes - maps, angels, prophets, names of God, etc.

These routes handle the biblical reference and study resources pages.
Data is imported from the centralized data module to avoid duplication.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

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
    MIRACLES_DATA,
    PRAYERS_DATA,
    BEATITUDES_DATA,
    TEN_COMMANDMENTS_DATA,
    ARMOR_OF_GOD_DATA,
    I_AM_STATEMENTS_DATA,
    TRINITY_DATA,
    CHRISTOLOGY_DATA,
    SOTERIOLOGY_DATA,
    PNEUMATOLOGY_DATA,
    ESCHATOLOGY_DATA,
    ECCLESIOLOGY_DATA,
    TYPES_AND_SHADOWS_DATA,
    MESSIANIC_PROPHECIES_DATA,
    BLOOD_IN_SCRIPTURE_DATA,
    KINGDOM_OF_GOD_DATA,
    NAMES_OF_CHRIST_DATA,
    SPIRITS_AND_DEMONS_DATA,
    PERSONIFICATIONS_DATA,
    # Additional Systematic Theology
    BIBLIOLOGY_DATA,
    THEOLOGY_PROPER_DATA,
    ANTHROPOLOGY_DATA,
    HAMARTIOLOGY_DATA,
    PROVIDENCE_DATA,
    GRACE_DATA,
    JUSTIFICATION_DATA,
    SANCTIFICATION_DATA,
    LAW_AND_GOSPEL_DATA,
    WORSHIP_DATA,
)
from ..utils.helpers import create_slug
from ..utils.pdf import WEASYPRINT_AVAILABLE, render_html_to_pdf, render_html_to_pdf_async

router = APIRouter(tags=["Biblical Resources"])

# Templates will be set by the main app
templates = None


def init_templates(app_templates):
    """Initialize templates from the main app."""
    global templates
    templates = app_templates
    templates.env.globals['resource_pdf_available'] = WEASYPRINT_AVAILABLE


def get_books():
    """Get list of Bible books."""
    from ..kjv import bible
    return bible.get_books()


def find_item_by_slug(data: dict, slug: str):
    """Find an item in a nested data structure by its slug."""
    for category_name, category in data.items():
        for item_name, item_data in category.items():
            if create_slug(item_name) == slug:
                return item_data, item_name, category_name
    return None, None, None


def _get_resource_item_or_404(data: dict, slug: str, not_found_message: str):
    """Fetch a resource item by slug or raise a 404 error."""
    item, item_name, category_name = find_item_by_slug(data, slug)
    if not item:
        raise HTTPException(status_code=404, detail=not_found_message)
    return item, item_name, category_name


def _resource_detail_response(
    request: Request,
    data: dict,
    slug: str,
    *,
    resource_title: str,
    back_url: str,
    back_text: str,
    not_found_message: str,
):
    """Render the shared resource detail template with optional PDF controls."""
    item, item_name, category_name = _get_resource_item_or_404(data, slug, not_found_message)

    pdf_url = f"{request.url.path.rstrip('/')}/pdf" if WEASYPRINT_AVAILABLE else None

    return templates.TemplateResponse(
        request,
        "resource_detail.html",
        {
            "books": get_books(),
            "item": item,
            "item_name": item_name,
            "category_name": category_name,
            "resource_title": resource_title,
            "back_url": back_url,
            "back_text": back_text,
            "pdf_available": WEASYPRINT_AVAILABLE,
            "pdf_url": pdf_url,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": resource_title, "url": back_url},
                {"text": item_name, "url": None},
            ],
        }
    )


async def _resource_detail_pdf_response(
    data: dict,
    slug: str,
    *,
    resource_title: str,
    not_found_message: str,
):
    """Generate a PDF export for a resource detail entry."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    item, item_name, category_name = _get_resource_item_or_404(data, slug, not_found_message)

    html_content = templates.get_template("resource_detail_pdf.html").render(
        item=item,
        item_name=item_name,
        category_name=category_name,
        resource_title=resource_title,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(item_name)}-{create_slug(resource_title)}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


async def _resource_index_pdf_response(resource_data: dict, page_title: str, page_subtitle: str, page_description: str):
    """Generate PDF for resource index-style pages."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    html_content = templates.get_template("resource_index_pdf.html").render(
        resource_data=resource_data,
        page_title=page_title,
        page_subtitle=page_subtitle,
        page_description=page_description,
    )

    pdf_buffer = await render_html_to_pdf_async(html_content)
    filename = f"{create_slug(page_title)}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


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
                {"text": "Resources", "url": "/resources"},
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Biblical Angels", "url": None}
            ]
        }
    )


@router.get("/biblical-angels/pdf")
async def biblical_angels_page_pdf():
    return await _resource_index_pdf_response(
        ANGELS_DATA,
        page_title="Biblical Angels",
        page_subtitle="Heavenly messengers throughout Scripture",
        page_description="Explore angels and angelic beings mentioned in the King James Bible, including Michael, Gabriel, and the heavenly host."
    )


@router.get("/biblical-angels/{angel_slug}", response_class=HTMLResponse)
def angel_detail(request: Request, angel_slug: str):
    """Individual biblical angels detail page."""
    return _resource_detail_response(
        request,
        ANGELS_DATA,
        angel_slug,
        resource_title="Biblical Angels",
        back_url="/biblical-angels",
        back_text="Biblical Angels",
        not_found_message="Biblical Angels item not found",
    )


@router.get("/biblical-angels/{angel_slug}/pdf")
async def angel_detail_pdf(angel_slug: str):
    """PDF export for a biblical angel detail page."""
    return await _resource_detail_pdf_response(
        ANGELS_DATA,
        angel_slug,
        resource_title="Biblical Angels",
        not_found_message="Biblical Angels item not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Biblical Prophets", "url": None}
            ]
        }
    )


@router.get("/biblical-prophets/pdf")
async def biblical_prophets_pdf():
    """PDF export for the prophets index."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    html_content = templates.get_template("biblical_prophets_pdf.html").render(prophets_data=PROPHETS_DATA)
    pdf_buffer = await render_html_to_pdf_async(html_content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=biblical-prophets.pdf"}
    )


@router.get("/biblical-prophets/{prophet_slug}", response_class=HTMLResponse)
def prophet_detail(request: Request, prophet_slug: str):
    """Individual biblical prophets detail page."""
    return _resource_detail_response(
        request,
        PROPHETS_DATA,
        prophet_slug,
        resource_title="Biblical Prophets",
        back_url="/biblical-prophets",
        back_text="Biblical Prophets",
        not_found_message="Biblical Prophets item not found",
    )


@router.get("/biblical-prophets/{prophet_slug}/pdf")
async def prophet_detail_pdf(prophet_slug: str):
    """PDF export for a biblical prophet entry."""
    return await _resource_detail_pdf_response(
        PROPHETS_DATA,
        prophet_slug,
        resource_title="Biblical Prophets",
        not_found_message="Biblical Prophets item not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Names of God", "url": None}
            ]
        }
    )


@router.get("/names-of-god/pdf")
async def names_of_god_page_pdf():
    return await _resource_index_pdf_response(
        NAMES_DATA,
        page_title="Names of God",
        page_subtitle="Divine titles revealed in Scripture",
        page_description="Explore the revelation of God's names throughout Scripture and their meanings."
    )


@router.get("/names-of-god/{name_slug}", response_class=HTMLResponse)
def name_of_god_detail(request: Request, name_slug: str):
    """Individual name of God detail page."""
    return _resource_detail_response(
        request,
        NAMES_DATA,
        name_slug,
        resource_title="Names of God",
        back_url="/names-of-god",
        back_text="Names of God",
        not_found_message="Name of God not found",
    )


@router.get("/names-of-god/{name_slug}/pdf")
async def name_of_god_detail_pdf(name_slug: str):
    """PDF export for a Name of God entry."""
    return await _resource_detail_pdf_response(
        NAMES_DATA,
        name_slug,
        resource_title="Names of God",
        not_found_message="Name of God not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Parables of Jesus", "url": None}
            ]
        }
    )


@router.get("/parables/pdf")
async def parables_pdf():
    """PDF export for the parables index."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    html_content = templates.get_template("parables_pdf.html").render(parables_data=PARABLES_DATA)
    pdf_buffer = await render_html_to_pdf_async(html_content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=parables.pdf"}
    )


@router.get("/parables/{parable_slug}", response_class=HTMLResponse)
def parable_detail(request: Request, parable_slug: str):
    """Individual parable detail page."""
    return _resource_detail_response(
        request,
        PARABLES_DATA,
        parable_slug,
        resource_title="Parables of Jesus",
        back_url="/parables",
        back_text="Parables of Jesus",
        not_found_message="Parable not found",
    )


@router.get("/parables/{parable_slug}/pdf")
async def parable_detail_pdf(parable_slug: str):
    """PDF export for a parable entry."""
    return await _resource_detail_pdf_response(
        PARABLES_DATA,
        parable_slug,
        resource_title="Parables of Jesus",
        not_found_message="Parable not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Biblical Covenants", "url": None}
            ]
        }
    )


@router.get("/biblical-covenants/pdf")
async def biblical_covenants_page_pdf():
    return await _resource_index_pdf_response(
        COVENANTS_DATA,
        page_title="Biblical Covenants",
        page_subtitle="Divine promises across redemptive history",
        page_description="Survey the major covenants established between God and His people throughout Scripture."
    )


@router.get("/biblical-covenants/{covenant_slug}", response_class=HTMLResponse)
def covenant_detail(request: Request, covenant_slug: str):
    """Individual covenant detail page."""
    return _resource_detail_response(
        request,
        COVENANTS_DATA,
        covenant_slug,
        resource_title="Biblical Covenants",
        back_url="/biblical-covenants",
        back_text="Biblical Covenants",
        not_found_message="Biblical Covenant not found",
    )


@router.get("/biblical-covenants/{covenant_slug}/pdf")
async def covenant_detail_pdf(covenant_slug: str):
    """PDF export for covenant entries."""
    return await _resource_detail_pdf_response(
        COVENANTS_DATA,
        covenant_slug,
        resource_title="Biblical Covenants",
        not_found_message="Biblical Covenant not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Twelve Apostles", "url": None}
            ]
        }
    )


@router.get("/the-twelve-apostles/pdf")
async def apostles_page_pdf():
    """PDF export for the apostles index."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    html_content = templates.get_template("twelve_apostles_pdf.html").render(apostles_data=APOSTLES_DATA)
    pdf_buffer = await render_html_to_pdf_async(html_content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=twelve-apostles.pdf"}
    )


@router.get("/the-twelve-apostles/{apostle_slug}", response_class=HTMLResponse)
def apostle_detail(request: Request, apostle_slug: str):
    """Individual apostle detail page."""
    return _resource_detail_response(
        request,
        APOSTLES_DATA,
        apostle_slug,
        resource_title="The Twelve Apostles",
        back_url="/the-twelve-apostles",
        back_text="The Twelve Apostles",
        not_found_message="Apostle not found",
    )


@router.get("/the-twelve-apostles/{apostle_slug}/pdf")
async def apostle_detail_pdf(apostle_slug: str):
    """PDF export for apostle entries."""
    return await _resource_detail_pdf_response(
        APOSTLES_DATA,
        apostle_slug,
        resource_title="The Twelve Apostles",
        not_found_message="Apostle not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Women of the Bible", "url": None}
            ]
        }
    )


@router.get("/women-of-the-bible/pdf")
async def women_of_the_bible_page_pdf():
    return await _resource_index_pdf_response(
        WOMEN_DATA,
        page_title="Women of the Bible",
        page_subtitle="Faithful witnesses throughout redemptive history",
        page_description="Explore the lives, faith, and legacies of notable women throughout Scripture."
    )


@router.get("/women-of-the-bible/{woman_slug}", response_class=HTMLResponse)
def woman_detail(request: Request, woman_slug: str):
    """Individual woman of the Bible detail page."""
    return _resource_detail_response(
        request,
        WOMEN_DATA,
        woman_slug,
        resource_title="Women of the Bible",
        back_url="/women-of-the-bible",
        back_text="Women of the Bible",
        not_found_message="Woman of the Bible not found",
    )


@router.get("/women-of-the-bible/{woman_slug}/pdf")
async def woman_detail_pdf(woman_slug: str):
    """PDF export for Women of the Bible entries."""
    return await _resource_detail_pdf_response(
        WOMEN_DATA,
        woman_slug,
        resource_title="Women of the Bible",
        not_found_message="Woman of the Bible not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Biblical Festivals", "url": None}
            ]
        }
    )


@router.get("/biblical-festivals/pdf")
async def biblical_festivals_page_pdf():
    return await _resource_index_pdf_response(
        FESTIVALS_DATA,
        page_title="Biblical Festivals",
        page_subtitle="Appointed feasts of the Lord",
        page_description="Learn about the appointed feasts and holy days ordained in the Law of Moses."
    )


@router.get("/biblical-festivals/{festival_slug}", response_class=HTMLResponse)
def festival_detail(request: Request, festival_slug: str):
    """Individual biblical festival detail page."""
    return _resource_detail_response(
        request,
        FESTIVALS_DATA,
        festival_slug,
        resource_title="Biblical Festivals",
        back_url="/biblical-festivals",
        back_text="Biblical Festivals",
        not_found_message="Biblical Festival not found",
    )


@router.get("/biblical-festivals/{festival_slug}/pdf")
async def festival_detail_pdf(festival_slug: str):
    """PDF export for biblical festival entries."""
    return await _resource_detail_pdf_response(
        FESTIVALS_DATA,
        festival_slug,
        resource_title="Biblical Festivals",
        not_found_message="Biblical Festival not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Fruits of the Spirit", "url": None}
            ]
        }
    )


@router.get("/fruits-of-the-spirit/pdf")
async def fruits_of_the_spirit_page_pdf():
    return await _resource_index_pdf_response(
        FRUITS_DATA,
        page_title="Fruits of the Spirit",
        page_subtitle="Developing Christian character",
        page_description="Meditate on the Spirit-produced virtues described in Galatians 5."
    )


@router.get("/fruits-of-the-spirit/{fruit_slug}", response_class=HTMLResponse)
def fruit_detail(request: Request, fruit_slug: str):
    """Individual fruit of the Spirit detail page."""
    return _resource_detail_response(
        request,
        FRUITS_DATA,
        fruit_slug,
        resource_title="Fruits of the Spirit",
        back_url="/fruits-of-the-spirit",
        back_text="Fruits of the Spirit",
        not_found_message="Fruit of the Spirit not found",
    )


@router.get("/fruits-of-the-spirit/{fruit_slug}/pdf")
async def fruit_detail_pdf(fruit_slug: str):
    """PDF export for Fruits of the Spirit entries."""
    return await _resource_detail_pdf_response(
        FRUITS_DATA,
        fruit_slug,
        resource_title="Fruits of the Spirit",
        not_found_message="Fruit of the Spirit not found",
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
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Tetragrammaton", "url": None}
            ]
        }
    )


@router.get("/tetragrammaton/pdf")
async def tetragrammaton_pdf():
    """PDF export for the Tetragrammaton page."""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="PDF generation is not available. WeasyPrint system libraries are not installed."
        )

    html_content = templates.get_template("tetragrammaton_pdf.html").render(content=TETRAGRAMMATON_CONTENT)
    pdf_buffer = await render_html_to_pdf_async(html_content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tetragrammaton.pdf"}
    )


# ============================================================================
# MIRACLES OF JESUS
# ============================================================================
@router.get("/miracles-of-jesus", response_class=HTMLResponse)
def miracles_page(request: Request):
    """Miracles of Jesus page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": MIRACLES_DATA,
            "page_title": "Miracles of Jesus",
            "page_subtitle": "Signs and Wonders Manifesting Divine Authority",
            "page_description": "Explore the miracles of Jesus Christ recorded in the Gospels - healings, nature miracles, exorcisms, and raisings from the dead.",
            "base_url": "/miracles-of-jesus",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Miracles of Jesus", "url": None}
            ]
        }
    )


@router.get("/miracles-of-jesus/pdf")
async def miracles_page_pdf():
    return await _resource_index_pdf_response(
        MIRACLES_DATA,
        page_title="Miracles of Jesus",
        page_subtitle="Signs and Wonders Manifesting Divine Authority",
        page_description="Explore the miracles of Jesus Christ recorded in the Gospels - healings, nature miracles, exorcisms, and raisings from the dead."
    )


@router.get("/miracles-of-jesus/{miracle_slug}", response_class=HTMLResponse)
def miracle_detail(request: Request, miracle_slug: str):
    """Individual miracle detail page."""
    return _resource_detail_response(
        request,
        MIRACLES_DATA,
        miracle_slug,
        resource_title="Miracles of Jesus",
        back_url="/miracles-of-jesus",
        back_text="Miracles of Jesus",
        not_found_message="Miracle not found",
    )


@router.get("/miracles-of-jesus/{miracle_slug}/pdf")
async def miracle_detail_pdf(miracle_slug: str):
    """PDF export for miracle entries."""
    return await _resource_detail_pdf_response(
        MIRACLES_DATA,
        miracle_slug,
        resource_title="Miracles of Jesus",
        not_found_message="Miracle not found",
    )


# ============================================================================
# PRAYERS OF THE BIBLE
# ============================================================================
@router.get("/prayers-of-the-bible", response_class=HTMLResponse)
def prayers_page(request: Request):
    """Prayers of the Bible page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": PRAYERS_DATA,
            "page_title": "Prayers of the Bible",
            "page_subtitle": "Sacred Conversations with the Almighty",
            "page_description": "Explore the prayers recorded in Scripture - from the Psalms to the prayers of Jesus, Paul, and the early church.",
            "base_url": "/prayers-of-the-bible",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Prayers of the Bible", "url": None}
            ]
        }
    )


@router.get("/prayers-of-the-bible/pdf")
async def prayers_page_pdf():
    return await _resource_index_pdf_response(
        PRAYERS_DATA,
        page_title="Prayers of the Bible",
        page_subtitle="Sacred Conversations with the Almighty",
        page_description="Explore the prayers recorded in Scripture - from the Psalms to the prayers of Jesus, Paul, and the early church."
    )


@router.get("/prayers-of-the-bible/{prayer_slug}", response_class=HTMLResponse)
def prayer_detail(request: Request, prayer_slug: str):
    """Individual prayer detail page."""
    return _resource_detail_response(
        request,
        PRAYERS_DATA,
        prayer_slug,
        resource_title="Prayers of the Bible",
        back_url="/prayers-of-the-bible",
        back_text="Prayers of the Bible",
        not_found_message="Prayer not found",
    )


@router.get("/prayers-of-the-bible/{prayer_slug}/pdf")
async def prayer_detail_pdf(prayer_slug: str):
    """PDF export for prayer entries."""
    return await _resource_detail_pdf_response(
        PRAYERS_DATA,
        prayer_slug,
        resource_title="Prayers of the Bible",
        not_found_message="Prayer not found",
    )


# ============================================================================
# THE BEATITUDES
# ============================================================================
@router.get("/beatitudes", response_class=HTMLResponse)
def beatitudes_page(request: Request):
    """The Beatitudes page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": BEATITUDES_DATA,
            "page_title": "The Beatitudes",
            "page_subtitle": "The Blessings of the Kingdom",
            "page_description": "Explore the Beatitudes from Jesus's Sermon on the Mount - the foundational blessings that describe the character of kingdom citizens.",
            "base_url": "/beatitudes",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Beatitudes", "url": None}
            ]
        }
    )


@router.get("/beatitudes/pdf")
async def beatitudes_page_pdf():
    return await _resource_index_pdf_response(
        BEATITUDES_DATA,
        page_title="The Beatitudes",
        page_subtitle="The Blessings of the Kingdom",
        page_description="Explore the Beatitudes from Jesus's Sermon on the Mount - the foundational blessings that describe the character of kingdom citizens."
    )


@router.get("/beatitudes/{beatitude_slug}", response_class=HTMLResponse)
def beatitude_detail(request: Request, beatitude_slug: str):
    """Individual beatitude detail page."""
    return _resource_detail_response(
        request,
        BEATITUDES_DATA,
        beatitude_slug,
        resource_title="The Beatitudes",
        back_url="/beatitudes",
        back_text="The Beatitudes",
        not_found_message="Beatitude not found",
    )


@router.get("/beatitudes/{beatitude_slug}/pdf")
async def beatitude_detail_pdf(beatitude_slug: str):
    """PDF export for Beatitudes entries."""
    return await _resource_detail_pdf_response(
        BEATITUDES_DATA,
        beatitude_slug,
        resource_title="The Beatitudes",
        not_found_message="Beatitude not found",
    )


# ============================================================================
# THE TEN COMMANDMENTS
# ============================================================================
@router.get("/ten-commandments", response_class=HTMLResponse)
def ten_commandments_page(request: Request):
    """The Ten Commandments page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": TEN_COMMANDMENTS_DATA,
            "page_title": "The Ten Commandments",
            "page_subtitle": "The Moral Law of God",
            "page_description": "Study the Ten Commandments given by God to Moses on Mount Sinai - the foundation of biblical morality and divine law.",
            "base_url": "/ten-commandments",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Ten Commandments", "url": None}
            ]
        }
    )


@router.get("/ten-commandments/pdf")
async def ten_commandments_page_pdf():
    return await _resource_index_pdf_response(
        TEN_COMMANDMENTS_DATA,
        page_title="The Ten Commandments",
        page_subtitle="The Moral Law of God",
        page_description="Study the Ten Commandments given by God to Moses on Mount Sinai - the foundation of biblical morality and divine law."
    )


@router.get("/ten-commandments/{commandment_slug}", response_class=HTMLResponse)
def commandment_detail(request: Request, commandment_slug: str):
    """Individual commandment detail page."""
    return _resource_detail_response(
        request,
        TEN_COMMANDMENTS_DATA,
        commandment_slug,
        resource_title="The Ten Commandments",
        back_url="/ten-commandments",
        back_text="The Ten Commandments",
        not_found_message="Commandment not found",
    )


@router.get("/ten-commandments/{commandment_slug}/pdf")
async def commandment_detail_pdf(commandment_slug: str):
    """PDF export for Ten Commandments entries."""
    return await _resource_detail_pdf_response(
        TEN_COMMANDMENTS_DATA,
        commandment_slug,
        resource_title="The Ten Commandments",
        not_found_message="Commandment not found",
    )


# ============================================================================
# THE ARMOR OF GOD
# ============================================================================
@router.get("/armor-of-god", response_class=HTMLResponse)
def armor_of_god_page(request: Request):
    """The Armor of God page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": ARMOR_OF_GOD_DATA,
            "page_title": "The Armor of God",
            "page_subtitle": "Divine Equipment for Spiritual Warfare",
            "page_description": "Study the Armor of God from Ephesians 6 - the spiritual equipment believers need to stand against the wiles of the devil.",
            "base_url": "/armor-of-god",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Armor of God", "url": None}
            ]
        }
    )


@router.get("/armor-of-god/pdf")
async def armor_of_god_page_pdf():
    return await _resource_index_pdf_response(
        ARMOR_OF_GOD_DATA,
        page_title="The Armor of God",
        page_subtitle="Divine Equipment for Spiritual Warfare",
        page_description="Study the Armor of God from Ephesians 6 - the spiritual equipment believers need to stand against the wiles of the devil."
    )


@router.get("/armor-of-god/{armor_slug}", response_class=HTMLResponse)
def armor_detail(request: Request, armor_slug: str):
    """Individual armor piece detail page."""
    return _resource_detail_response(
        request,
        ARMOR_OF_GOD_DATA,
        armor_slug,
        resource_title="The Armor of God",
        back_url="/armor-of-god",
        back_text="The Armor of God",
        not_found_message="Armor piece not found",
    )


@router.get("/armor-of-god/{armor_slug}/pdf")
async def armor_detail_pdf(armor_slug: str):
    """PDF export for Armor of God entries."""
    return await _resource_detail_pdf_response(
        ARMOR_OF_GOD_DATA,
        armor_slug,
        resource_title="The Armor of God",
        not_found_message="Armor piece not found",
    )


# ============================================================================
# I AM STATEMENTS OF JESUS
# ============================================================================
@router.get("/i-am-statements", response_class=HTMLResponse)
def i_am_statements_page(request: Request):
    """I Am Statements of Jesus page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": I_AM_STATEMENTS_DATA,
            "page_title": "I Am Statements of Jesus",
            "page_subtitle": "Divine Self-Revelations in the Gospel of John",
            "page_description": "Explore the seven 'I Am' statements of Jesus in John's Gospel - profound declarations of His divine nature and mission.",
            "base_url": "/i-am-statements",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "I Am Statements", "url": None}
            ]
        }
    )


@router.get("/i-am-statements/pdf")
async def i_am_statements_page_pdf():
    return await _resource_index_pdf_response(
        I_AM_STATEMENTS_DATA,
        page_title="I Am Statements of Jesus",
        page_subtitle="Divine Self-Revelations in the Gospel of John",
        page_description="Explore the seven 'I Am' statements of Jesus in John's Gospel - profound declarations of His divine nature and mission."
    )


@router.get("/i-am-statements/{statement_slug}", response_class=HTMLResponse)
def i_am_statement_detail(request: Request, statement_slug: str):
    """Individual I Am statement detail page."""
    return _resource_detail_response(
        request,
        I_AM_STATEMENTS_DATA,
        statement_slug,
        resource_title="I Am Statements",
        back_url="/i-am-statements",
        back_text="I Am Statements",
        not_found_message="Statement not found",
    )


@router.get("/i-am-statements/{statement_slug}/pdf")
async def i_am_statement_detail_pdf(statement_slug: str):
    """PDF export for I Am statement entries."""
    return await _resource_detail_pdf_response(
        I_AM_STATEMENTS_DATA,
        statement_slug,
        resource_title="I Am Statements",
        not_found_message="Statement not found",
    )


# ============================================================================
# THE TRINITY
# ============================================================================
@router.get("/trinity", response_class=HTMLResponse)
def trinity_page(request: Request):
    """The Trinity - doctrine of God page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": TRINITY_DATA,
            "page_title": "The Trinity",
            "page_subtitle": "The Doctrine of One God in Three Persons",
            "page_description": "An expansive theological study of the Trinity - the doctrine that God eternally exists as Father, Son, and Holy Spirit, three distinct Persons sharing one divine essence.",
            "base_url": "/trinity",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Trinity", "url": None}
            ]
        }
    )


@router.get("/trinity/pdf")
async def trinity_page_pdf():
    return await _resource_index_pdf_response(
        TRINITY_DATA,
        page_title="The Trinity",
        page_subtitle="The Doctrine of One God in Three Persons",
        page_description="An expansive theological study of the Trinity - the doctrine that God eternally exists as Father, Son, and Holy Spirit, three distinct Persons sharing one divine essence."
    )


@router.get("/trinity/{item_slug}", response_class=HTMLResponse)
def trinity_detail(request: Request, item_slug: str):
    """Individual Trinity topic detail page."""
    return _resource_detail_response(
        request,
        TRINITY_DATA,
        item_slug,
        resource_title="The Trinity",
        back_url="/trinity",
        back_text="The Trinity",
        not_found_message="Topic not found",
    )


@router.get("/trinity/{item_slug}/pdf")
async def trinity_detail_pdf(item_slug: str):
    """PDF export for Trinity topics."""
    return await _resource_detail_pdf_response(
        TRINITY_DATA,
        item_slug,
        resource_title="The Trinity",
        not_found_message="Topic not found",
    )


# ============================================================================
# CHRISTOLOGY
# ============================================================================
@router.get("/christology", response_class=HTMLResponse)
def christology_page(request: Request):
    """Christology - the doctrine of Christ page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": CHRISTOLOGY_DATA,
            "page_title": "Christology",
            "page_subtitle": "The Doctrine of the Person and Work of Christ",
            "page_description": "An expansive theological study of Christology - the doctrine concerning Jesus Christ, His divine-human nature, His offices, and His saving work.",
            "base_url": "/christology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Christology", "url": None}
            ]
        }
    )


@router.get("/christology/pdf")
async def christology_page_pdf():
    return await _resource_index_pdf_response(
        CHRISTOLOGY_DATA,
        page_title="Christology",
        page_subtitle="The Doctrine of the Person and Work of Christ",
        page_description="An expansive theological study of Christology - the doctrine concerning Jesus Christ, His divine-human nature, His offices, and His saving work."
    )


@router.get("/christology/{item_slug}", response_class=HTMLResponse)
def christology_detail(request: Request, item_slug: str):
    """Individual Christology topic detail page."""
    return _resource_detail_response(
        request,
        CHRISTOLOGY_DATA,
        item_slug,
        resource_title="Christology",
        back_url="/christology",
        back_text="Christology",
        not_found_message="Topic not found",
    )


@router.get("/christology/{item_slug}/pdf")
async def christology_detail_pdf(item_slug: str):
    """PDF export for Christology topics."""
    return await _resource_detail_pdf_response(
        CHRISTOLOGY_DATA,
        item_slug,
        resource_title="Christology",
        not_found_message="Topic not found",
    )


# ============================================================================
# SOTERIOLOGY
# ============================================================================
@router.get("/soteriology", response_class=HTMLResponse)
def soteriology_page(request: Request):
    """Soteriology - the doctrine of salvation page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": SOTERIOLOGY_DATA,
            "page_title": "Soteriology",
            "page_subtitle": "The Doctrine of Salvation",
            "page_description": "An expansive theological study of Soteriology - the doctrine of salvation, covering election, atonement, regeneration, justification, sanctification, and glorification.",
            "base_url": "/soteriology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Soteriology", "url": None}
            ]
        }
    )


@router.get("/soteriology/pdf")
async def soteriology_page_pdf():
    return await _resource_index_pdf_response(
        SOTERIOLOGY_DATA,
        page_title="Soteriology",
        page_subtitle="The Doctrine of Salvation",
        page_description="An expansive theological study of Soteriology - the doctrine of salvation, covering election, atonement, regeneration, justification, sanctification, and glorification."
    )


@router.get("/soteriology/{item_slug}", response_class=HTMLResponse)
def soteriology_detail(request: Request, item_slug: str):
    """Individual Soteriology topic detail page."""
    return _resource_detail_response(
        request,
        SOTERIOLOGY_DATA,
        item_slug,
        resource_title="Soteriology",
        back_url="/soteriology",
        back_text="Soteriology",
        not_found_message="Topic not found",
    )


@router.get("/soteriology/{item_slug}/pdf")
async def soteriology_detail_pdf(item_slug: str):
    """PDF export for Soteriology topics."""
    return await _resource_detail_pdf_response(
        SOTERIOLOGY_DATA,
        item_slug,
        resource_title="Soteriology",
        not_found_message="Topic not found",
    )


# ============================================================================
# PNEUMATOLOGY
# ============================================================================
@router.get("/pneumatology", response_class=HTMLResponse)
def pneumatology_page(request: Request):
    """Pneumatology - the doctrine of the Holy Spirit page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": PNEUMATOLOGY_DATA,
            "page_title": "Pneumatology",
            "page_subtitle": "The Doctrine of the Holy Spirit",
            "page_description": "An expansive theological study of Pneumatology - the doctrine of the Holy Spirit, His person, deity, work in salvation, and ministry to believers.",
            "base_url": "/pneumatology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Pneumatology", "url": None}
            ]
        }
    )


@router.get("/pneumatology/pdf")
async def pneumatology_page_pdf():
    return await _resource_index_pdf_response(
        PNEUMATOLOGY_DATA,
        page_title="Pneumatology",
        page_subtitle="The Doctrine of the Holy Spirit",
        page_description="An expansive theological study of Pneumatology - the doctrine of the Holy Spirit, His person, deity, work in salvation, and ministry to believers."
    )


@router.get("/pneumatology/{item_slug}", response_class=HTMLResponse)
def pneumatology_detail(request: Request, item_slug: str):
    """Individual Pneumatology topic detail page."""
    return _resource_detail_response(
        request,
        PNEUMATOLOGY_DATA,
        item_slug,
        resource_title="Pneumatology",
        back_url="/pneumatology",
        back_text="Pneumatology",
        not_found_message="Topic not found",
    )


@router.get("/pneumatology/{item_slug}/pdf")
async def pneumatology_detail_pdf(item_slug: str):
    """PDF export for Pneumatology topics."""
    return await _resource_detail_pdf_response(
        PNEUMATOLOGY_DATA,
        item_slug,
        resource_title="Pneumatology",
        not_found_message="Topic not found",
    )


# ============================================================================
# ESCHATOLOGY
# ============================================================================
@router.get("/eschatology", response_class=HTMLResponse)
def eschatology_page(request: Request):
    """Eschatology - the doctrine of last things page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": ESCHATOLOGY_DATA,
            "page_title": "Eschatology",
            "page_subtitle": "The Doctrine of Last Things",
            "page_description": "An expansive theological study of Eschatology - the doctrine of death, resurrection, the second coming of Christ, final judgment, and eternal destinies.",
            "base_url": "/eschatology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Eschatology", "url": None}
            ]
        }
    )


@router.get("/eschatology/pdf")
async def eschatology_page_pdf():
    return await _resource_index_pdf_response(
        ESCHATOLOGY_DATA,
        page_title="Eschatology",
        page_subtitle="The Doctrine of Last Things",
        page_description="An expansive theological study of Eschatology - the doctrine of death, resurrection, the second coming of Christ, final judgment, and eternal destinies."
    )


@router.get("/eschatology/{item_slug}", response_class=HTMLResponse)
def eschatology_detail(request: Request, item_slug: str):
    """Individual Eschatology topic detail page."""
    return _resource_detail_response(
        request,
        ESCHATOLOGY_DATA,
        item_slug,
        resource_title="Eschatology",
        back_url="/eschatology",
        back_text="Eschatology",
        not_found_message="Topic not found",
    )


@router.get("/eschatology/{item_slug}/pdf")
async def eschatology_detail_pdf(item_slug: str):
    """PDF export for Eschatology topics."""
    return await _resource_detail_pdf_response(
        ESCHATOLOGY_DATA,
        item_slug,
        resource_title="Eschatology",
        not_found_message="Topic not found",
    )


# ============================================================================
# ECCLESIOLOGY
# ============================================================================
@router.get("/ecclesiology", response_class=HTMLResponse)
def ecclesiology_page(request: Request):
    """Ecclesiology - the doctrine of the church page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": ECCLESIOLOGY_DATA,
            "page_title": "Ecclesiology",
            "page_subtitle": "The Doctrine of the Church",
            "page_description": "An expansive theological study of Ecclesiology - the doctrine of the church, its nature, marks, government, mission, and ordinances.",
            "base_url": "/ecclesiology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Ecclesiology", "url": None}
            ]
        }
    )


@router.get("/ecclesiology/pdf")
async def ecclesiology_page_pdf():
    return await _resource_index_pdf_response(
        ECCLESIOLOGY_DATA,
        page_title="Ecclesiology",
        page_subtitle="The Doctrine of the Church",
        page_description="An expansive theological study of Ecclesiology - the doctrine of the church, its nature, marks, government, mission, and ordinances."
    )


@router.get("/ecclesiology/{item_slug}", response_class=HTMLResponse)
def ecclesiology_detail(request: Request, item_slug: str):
    """Individual Ecclesiology topic detail page."""
    return _resource_detail_response(
        request,
        ECCLESIOLOGY_DATA,
        item_slug,
        resource_title="Ecclesiology",
        back_url="/ecclesiology",
        back_text="Ecclesiology",
        not_found_message="Topic not found",
    )


@router.get("/ecclesiology/{item_slug}/pdf")
async def ecclesiology_detail_pdf(item_slug: str):
    """PDF export for Ecclesiology topics."""
    return await _resource_detail_pdf_response(
        ECCLESIOLOGY_DATA,
        item_slug,
        resource_title="Ecclesiology",
        not_found_message="Topic not found",
    )


# ============================================================================
# TYPES AND SHADOWS OF CHRIST
# ============================================================================
@router.get("/types-and-shadows", response_class=HTMLResponse)
def types_and_shadows_page(request: Request):
    """Types and Shadows of Christ page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": TYPES_AND_SHADOWS_DATA,
            "page_title": "Types and Shadows of Christ",
            "page_subtitle": "Old Testament Figures Fulfilled in Christ",
            "page_description": "An expansive study of Old Testament types and shadows pointing to Christ - persons, events, and institutions that prefigure and find their fulfillment in Jesus.",
            "base_url": "/types-and-shadows",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Types and Shadows", "url": None}
            ]
        }
    )


@router.get("/types-and-shadows/pdf")
async def types_and_shadows_page_pdf():
    return await _resource_index_pdf_response(
        TYPES_AND_SHADOWS_DATA,
        page_title="Types and Shadows of Christ",
        page_subtitle="Old Testament Figures Fulfilled in Christ",
        page_description="An expansive study of Old Testament types and shadows pointing to Christ - persons, events, and institutions that prefigure and find their fulfillment in Jesus."
    )


@router.get("/types-and-shadows/{item_slug}", response_class=HTMLResponse)
def types_and_shadows_detail(request: Request, item_slug: str):
    """Individual Types and Shadows topic detail page."""
    return _resource_detail_response(
        request,
        TYPES_AND_SHADOWS_DATA,
        item_slug,
        resource_title="Types and Shadows",
        back_url="/types-and-shadows",
        back_text="Types and Shadows",
        not_found_message="Topic not found",
    )


@router.get("/types-and-shadows/{item_slug}/pdf")
async def types_and_shadows_detail_pdf(item_slug: str):
    """PDF export for Types and Shadows topics."""
    return await _resource_detail_pdf_response(
        TYPES_AND_SHADOWS_DATA,
        item_slug,
        resource_title="Types and Shadows",
        not_found_message="Topic not found",
    )


# ============================================================================
# MESSIANIC PROPHECIES
# ============================================================================
@router.get("/messianic-prophecies", response_class=HTMLResponse)
def messianic_prophecies_page(request: Request):
    """Messianic Prophecies page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": MESSIANIC_PROPHECIES_DATA,
            "page_title": "Messianic Prophecies",
            "page_subtitle": "Old Testament Predictions Fulfilled in Christ",
            "page_description": "An expansive study of Messianic prophecies - Old Testament predictions concerning the Messiah's coming, ministry, suffering, and triumph, all fulfilled in Jesus Christ.",
            "base_url": "/messianic-prophecies",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Messianic Prophecies", "url": None}
            ]
        }
    )


@router.get("/messianic-prophecies/pdf")
async def messianic_prophecies_page_pdf():
    return await _resource_index_pdf_response(
        MESSIANIC_PROPHECIES_DATA,
        page_title="Messianic Prophecies",
        page_subtitle="Old Testament Predictions Fulfilled in Christ",
        page_description="An expansive study of Messianic prophecies - Old Testament predictions concerning the Messiah's coming, ministry, suffering, and triumph, all fulfilled in Jesus Christ."
    )


@router.get("/messianic-prophecies/{item_slug}", response_class=HTMLResponse)
def messianic_prophecies_detail(request: Request, item_slug: str):
    """Individual Messianic Prophecy topic detail page."""
    return _resource_detail_response(
        request,
        MESSIANIC_PROPHECIES_DATA,
        item_slug,
        resource_title="Messianic Prophecies",
        back_url="/messianic-prophecies",
        back_text="Messianic Prophecies",
        not_found_message="Topic not found",
    )


@router.get("/messianic-prophecies/{item_slug}/pdf")
async def messianic_prophecies_detail_pdf(item_slug: str):
    """PDF export for Messianic Prophecies topics."""
    return await _resource_detail_pdf_response(
        MESSIANIC_PROPHECIES_DATA,
        item_slug,
        resource_title="Messianic Prophecies",
        not_found_message="Topic not found",
    )


# ============================================================================
# THE BLOOD IN SCRIPTURE
# ============================================================================
@router.get("/blood-in-scripture", response_class=HTMLResponse)
def blood_in_scripture_page(request: Request):
    """The Blood in Scripture page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": BLOOD_IN_SCRIPTURE_DATA,
            "page_title": "The Blood in Scripture",
            "page_subtitle": "The Theology of Redemption Through Blood",
            "page_description": "An expansive study of the blood in Scripture - its significance, Old Testament foundations, and ultimate fulfillment in the blood of Christ for redemption, justification, and cleansing.",
            "base_url": "/blood-in-scripture",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Blood in Scripture", "url": None}
            ]
        }
    )


@router.get("/blood-in-scripture/pdf")
async def blood_in_scripture_page_pdf():
    return await _resource_index_pdf_response(
        BLOOD_IN_SCRIPTURE_DATA,
        page_title="The Blood in Scripture",
        page_subtitle="The Theology of Redemption Through Blood",
        page_description="An expansive study of the blood in Scripture - its significance, Old Testament foundations, and ultimate fulfillment in the blood of Christ for redemption, justification, and cleansing."
    )


@router.get("/blood-in-scripture/{item_slug}", response_class=HTMLResponse)
def blood_in_scripture_detail(request: Request, item_slug: str):
    """Individual Blood in Scripture topic detail page."""
    return _resource_detail_response(
        request,
        BLOOD_IN_SCRIPTURE_DATA,
        item_slug,
        resource_title="The Blood in Scripture",
        back_url="/blood-in-scripture",
        back_text="The Blood in Scripture",
        not_found_message="Topic not found",
    )


@router.get("/blood-in-scripture/{item_slug}/pdf")
async def blood_in_scripture_detail_pdf(item_slug: str):
    """PDF export for Blood in Scripture topics."""
    return await _resource_detail_pdf_response(
        BLOOD_IN_SCRIPTURE_DATA,
        item_slug,
        resource_title="The Blood in Scripture",
        not_found_message="Topic not found",
    )


# ============================================================================
# THE KINGDOM OF GOD
# ============================================================================
@router.get("/kingdom-of-god", response_class=HTMLResponse)
def kingdom_of_god_page(request: Request):
    """The Kingdom of God page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": KINGDOM_OF_GOD_DATA,
            "page_title": "The Kingdom of God",
            "page_subtitle": "The Reign of God Through Christ",
            "page_description": "An expansive study of the Kingdom of God - its nature, King, entrance requirements, growth, and ultimate consummation at Christ's return.",
            "base_url": "/kingdom-of-god",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Kingdom of God", "url": None}
            ]
        }
    )


@router.get("/kingdom-of-god/pdf")
async def kingdom_of_god_page_pdf():
    return await _resource_index_pdf_response(
        KINGDOM_OF_GOD_DATA,
        page_title="The Kingdom of God",
        page_subtitle="The Reign of God Through Christ",
        page_description="An expansive study of the Kingdom of God - its nature, King, entrance requirements, growth, and ultimate consummation at Christ's return."
    )


@router.get("/kingdom-of-god/{item_slug}", response_class=HTMLResponse)
def kingdom_of_god_detail(request: Request, item_slug: str):
    """Individual Kingdom of God topic detail page."""
    return _resource_detail_response(
        request,
        KINGDOM_OF_GOD_DATA,
        item_slug,
        resource_title="The Kingdom of God",
        back_url="/kingdom-of-god",
        back_text="The Kingdom of God",
        not_found_message="Topic not found",
    )


@router.get("/kingdom-of-god/{item_slug}/pdf")
async def kingdom_of_god_detail_pdf(item_slug: str):
    """PDF export for Kingdom of God topics."""
    return await _resource_detail_pdf_response(
        KINGDOM_OF_GOD_DATA,
        item_slug,
        resource_title="The Kingdom of God",
        not_found_message="Topic not found",
    )


# ============================================================================
# NAMES AND TITLES OF CHRIST
# ============================================================================
@router.get("/names-of-christ", response_class=HTMLResponse)
def names_of_christ_page(request: Request):
    """Names and Titles of Christ page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": NAMES_OF_CHRIST_DATA,
            "page_title": "Names and Titles of Christ",
            "page_subtitle": "The Glorious Designations of Our Lord",
            "page_description": "An expansive study of the names and titles of Jesus Christ - divine names, messianic titles, redemptive designations, and relational names revealing His person and work.",
            "base_url": "/names-of-christ",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Names of Christ", "url": None}
            ]
        }
    )


@router.get("/names-of-christ/pdf")
async def names_of_christ_page_pdf():
    return await _resource_index_pdf_response(
        NAMES_OF_CHRIST_DATA,
        page_title="Names and Titles of Christ",
        page_subtitle="The Glorious Designations of Our Lord",
        page_description="An expansive study of the names and titles of Jesus Christ - divine names, messianic titles, redemptive designations, and relational names revealing His person and work."
    )


@router.get("/names-of-christ/{item_slug}", response_class=HTMLResponse)
def names_of_christ_detail(request: Request, item_slug: str):
    """Individual Names of Christ topic detail page."""
    return _resource_detail_response(
        request,
        NAMES_OF_CHRIST_DATA,
        item_slug,
        resource_title="Names of Christ",
        back_url="/names-of-christ",
        back_text="Names of Christ",
        not_found_message="Topic not found",
    )


@router.get("/names-of-christ/{item_slug}/pdf")
async def names_of_christ_detail_pdf(item_slug: str):
    """PDF export for Names of Christ topics."""
    return await _resource_detail_pdf_response(
        NAMES_OF_CHRIST_DATA,
        item_slug,
        resource_title="Names of Christ",
        not_found_message="Topic not found",
    )


# ============================================================================
# SPIRITS AND DEMONS
# ============================================================================
@router.get("/spirits-and-demons", response_class=HTMLResponse)
def spirits_and_demons_page(request: Request):
    """Spirits and Demons - biblical demonology page."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": SPIRITS_AND_DEMONS_DATA,
            "page_title": "Spirits & Demons",
            "page_subtitle": "Biblical Demonology and Spiritual Warfare",
            "page_description": "A comprehensive study of demons, Satan, evil spirits, and spiritual warfare in Scripture—from Legion to the Lake of Fire.",
            "base_url": "/spirits-and-demons",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Spirits & Demons", "url": None}
            ]
        }
    )


@router.get("/spirits-and-demons/pdf")
async def spirits_and_demons_page_pdf():
    return await _resource_index_pdf_response(
        SPIRITS_AND_DEMONS_DATA,
        page_title="Spirits & Demons",
        page_subtitle="Biblical Demonology and Spiritual Warfare",
        page_description="A comprehensive study of demons, Satan, evil spirits, and spiritual warfare in Scripture—from Legion to the Lake of Fire."
    )


@router.get("/spirits-and-demons/{item_slug}", response_class=HTMLResponse)
def spirits_and_demons_detail(request: Request, item_slug: str):
    """Individual Spirits and Demons topic detail page."""
    return _resource_detail_response(
        request,
        SPIRITS_AND_DEMONS_DATA,
        item_slug,
        resource_title="Spirits & Demons",
        back_url="/spirits-and-demons",
        back_text="Spirits & Demons",
        not_found_message="Topic not found",
    )


@router.get("/spirits-and-demons/{item_slug}/pdf")
async def spirits_and_demons_detail_pdf(item_slug: str):
    """PDF export for Spirits & Demons topics."""
    return await _resource_detail_pdf_response(
        SPIRITS_AND_DEMONS_DATA,
        item_slug,
        resource_title="Spirits & Demons",
        not_found_message="Topic not found",
    )


# ============================================================================
# PERSONIFICATIONS IN SCRIPTURE
# ============================================================================
@router.get("/personifications", response_class=HTMLResponse)
def personifications_page(request: Request):
    """Personifications in Scripture - abstract concepts given human form."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": PERSONIFICATIONS_DATA,
            "page_title": "Personifications in Scripture",
            "page_subtitle": "Abstract Concepts Given Human Form",
            "page_description": "A study of biblical personifications—Wisdom, Folly, Death, Sin, and other abstract concepts portrayed as persons throughout Scripture.",
            "base_url": "/personifications",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Personifications", "url": None}
            ]
        }
    )


@router.get("/personifications/pdf")
async def personifications_page_pdf():
    return await _resource_index_pdf_response(
        PERSONIFICATIONS_DATA,
        page_title="Personifications in Scripture",
        page_subtitle="Abstract Concepts Given Human Form",
        page_description="A study of biblical personifications—Wisdom, Folly, Death, Sin, and other abstract concepts portrayed as persons throughout Scripture."
    )


@router.get("/personifications/{item_slug}", response_class=HTMLResponse)
def personifications_detail(request: Request, item_slug: str):
    """Individual Personification topic detail page."""
    return _resource_detail_response(
        request,
        PERSONIFICATIONS_DATA,
        item_slug,
        resource_title="Personifications",
        back_url="/personifications",
        back_text="Personifications",
        not_found_message="Topic not found",
    )


@router.get("/personifications/{item_slug}/pdf")
async def personifications_detail_pdf(item_slug: str):
    """PDF export for Personifications topics."""
    return await _resource_detail_pdf_response(
        PERSONIFICATIONS_DATA,
        item_slug,
        resource_title="Personifications",
        not_found_message="Topic not found",
    )


# ============================================================================
# BIBLIOLOGY - THE DOCTRINE OF SCRIPTURE
# ============================================================================
@router.get("/bibliology", response_class=HTMLResponse)
def bibliology_page(request: Request):
    """Bibliology - The Doctrine of Scripture."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": BIBLIOLOGY_DATA["categories"],
            "page_title": BIBLIOLOGY_DATA["title"],
            "page_subtitle": BIBLIOLOGY_DATA["subtitle"],
            "page_description": BIBLIOLOGY_DATA["introduction"],
            "base_url": "/bibliology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Bibliology", "url": None}
            ]
        }
    )


@router.get("/bibliology/pdf")
async def bibliology_page_pdf():
    return await _resource_index_pdf_response(
        BIBLIOLOGY_DATA["categories"],
        page_title=BIBLIOLOGY_DATA["title"],
        page_subtitle=BIBLIOLOGY_DATA["subtitle"],
        page_description=BIBLIOLOGY_DATA["introduction"]
    )


@router.get("/bibliology/{item_slug}", response_class=HTMLResponse)
def bibliology_detail(request: Request, item_slug: str):
    """Individual Bibliology topic detail page."""
    return _resource_detail_response(
        request,
        BIBLIOLOGY_DATA["categories"],
        item_slug,
        resource_title="Bibliology",
        back_url="/bibliology",
        back_text="Bibliology",
        not_found_message="Topic not found",
    )


@router.get("/bibliology/{item_slug}/pdf")
async def bibliology_detail_pdf(item_slug: str):
    """PDF export for Bibliology topics."""
    return await _resource_detail_pdf_response(
        BIBLIOLOGY_DATA["categories"],
        item_slug,
        resource_title="Bibliology",
        not_found_message="Topic not found",
    )


# ============================================================================
# THEOLOGY PROPER - THE ATTRIBUTES OF GOD
# ============================================================================
@router.get("/theology-proper", response_class=HTMLResponse)
def theology_proper_page(request: Request):
    """Theology Proper - The Attributes of God."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": THEOLOGY_PROPER_DATA["categories"],
            "page_title": THEOLOGY_PROPER_DATA["title"],
            "page_subtitle": THEOLOGY_PROPER_DATA["subtitle"],
            "page_description": THEOLOGY_PROPER_DATA["introduction"],
            "base_url": "/theology-proper",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Theology Proper", "url": None}
            ]
        }
    )


@router.get("/theology-proper/pdf")
async def theology_proper_page_pdf():
    return await _resource_index_pdf_response(
        THEOLOGY_PROPER_DATA["categories"],
        page_title=THEOLOGY_PROPER_DATA["title"],
        page_subtitle=THEOLOGY_PROPER_DATA["subtitle"],
        page_description=THEOLOGY_PROPER_DATA["introduction"]
    )


@router.get("/theology-proper/{item_slug}", response_class=HTMLResponse)
def theology_proper_detail(request: Request, item_slug: str):
    """Individual Theology Proper topic detail page."""
    return _resource_detail_response(
        request,
        THEOLOGY_PROPER_DATA["categories"],
        item_slug,
        resource_title="Theology Proper",
        back_url="/theology-proper",
        back_text="Theology Proper",
        not_found_message="Topic not found",
    )


@router.get("/theology-proper/{item_slug}/pdf")
async def theology_proper_detail_pdf(item_slug: str):
    """PDF export for Theology Proper topics."""
    return await _resource_detail_pdf_response(
        THEOLOGY_PROPER_DATA["categories"],
        item_slug,
        resource_title="Theology Proper",
        not_found_message="Topic not found",
    )


# ============================================================================
# ANTHROPOLOGY - THE DOCTRINE OF MAN
# ============================================================================
@router.get("/anthropology", response_class=HTMLResponse)
def anthropology_page(request: Request):
    """Anthropology - The Doctrine of Man."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": ANTHROPOLOGY_DATA["categories"],
            "page_title": ANTHROPOLOGY_DATA["title"],
            "page_subtitle": ANTHROPOLOGY_DATA["subtitle"],
            "page_description": ANTHROPOLOGY_DATA["introduction"],
            "base_url": "/anthropology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Anthropology", "url": None}
            ]
        }
    )


@router.get("/anthropology/pdf")
async def anthropology_page_pdf():
    return await _resource_index_pdf_response(
        ANTHROPOLOGY_DATA["categories"],
        page_title=ANTHROPOLOGY_DATA["title"],
        page_subtitle=ANTHROPOLOGY_DATA["subtitle"],
        page_description=ANTHROPOLOGY_DATA["introduction"]
    )


@router.get("/anthropology/{item_slug}", response_class=HTMLResponse)
def anthropology_detail(request: Request, item_slug: str):
    """Individual Anthropology topic detail page."""
    return _resource_detail_response(
        request,
        ANTHROPOLOGY_DATA["categories"],
        item_slug,
        resource_title="Anthropology",
        back_url="/anthropology",
        back_text="Anthropology",
        not_found_message="Topic not found",
    )


@router.get("/anthropology/{item_slug}/pdf")
async def anthropology_detail_pdf(item_slug: str):
    """PDF export for Anthropology topics."""
    return await _resource_detail_pdf_response(
        ANTHROPOLOGY_DATA["categories"],
        item_slug,
        resource_title="Anthropology",
        not_found_message="Topic not found",
    )


# ============================================================================
# HAMARTIOLOGY - THE DOCTRINE OF SIN
# ============================================================================
@router.get("/hamartiology", response_class=HTMLResponse)
def hamartiology_page(request: Request):
    """Hamartiology - The Doctrine of Sin."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": HAMARTIOLOGY_DATA["categories"],
            "page_title": HAMARTIOLOGY_DATA["title"],
            "page_subtitle": HAMARTIOLOGY_DATA["subtitle"],
            "page_description": HAMARTIOLOGY_DATA["introduction"],
            "base_url": "/hamartiology",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Hamartiology", "url": None}
            ]
        }
    )


@router.get("/hamartiology/pdf")
async def hamartiology_page_pdf():
    return await _resource_index_pdf_response(
        HAMARTIOLOGY_DATA["categories"],
        page_title=HAMARTIOLOGY_DATA["title"],
        page_subtitle=HAMARTIOLOGY_DATA["subtitle"],
        page_description=HAMARTIOLOGY_DATA["introduction"]
    )


@router.get("/hamartiology/{item_slug}", response_class=HTMLResponse)
def hamartiology_detail(request: Request, item_slug: str):
    """Individual Hamartiology topic detail page."""
    return _resource_detail_response(
        request,
        HAMARTIOLOGY_DATA["categories"],
        item_slug,
        resource_title="Hamartiology",
        back_url="/hamartiology",
        back_text="Hamartiology",
        not_found_message="Topic not found",
    )


@router.get("/hamartiology/{item_slug}/pdf")
async def hamartiology_detail_pdf(item_slug: str):
    """PDF export for Hamartiology topics."""
    return await _resource_detail_pdf_response(
        HAMARTIOLOGY_DATA["categories"],
        item_slug,
        resource_title="Hamartiology",
        not_found_message="Topic not found",
    )


# ============================================================================
# PROVIDENCE - DIVINE PROVIDENCE
# ============================================================================
@router.get("/providence", response_class=HTMLResponse)
def providence_page(request: Request):
    """Providence - Divine Providence."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": PROVIDENCE_DATA["categories"],
            "page_title": PROVIDENCE_DATA["title"],
            "page_subtitle": PROVIDENCE_DATA["subtitle"],
            "page_description": PROVIDENCE_DATA["introduction"],
            "base_url": "/providence",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Providence", "url": None}
            ]
        }
    )


@router.get("/providence/pdf")
async def providence_page_pdf():
    return await _resource_index_pdf_response(
        PROVIDENCE_DATA["categories"],
        page_title=PROVIDENCE_DATA["title"],
        page_subtitle=PROVIDENCE_DATA["subtitle"],
        page_description=PROVIDENCE_DATA["introduction"]
    )


@router.get("/providence/{item_slug}", response_class=HTMLResponse)
def providence_detail(request: Request, item_slug: str):
    """Individual Providence topic detail page."""
    return _resource_detail_response(
        request,
        PROVIDENCE_DATA["categories"],
        item_slug,
        resource_title="Providence",
        back_url="/providence",
        back_text="Providence",
        not_found_message="Topic not found",
    )


@router.get("/providence/{item_slug}/pdf")
async def providence_detail_pdf(item_slug: str):
    """PDF export for Providence topics."""
    return await _resource_detail_pdf_response(
        PROVIDENCE_DATA["categories"],
        item_slug,
        resource_title="Providence",
        not_found_message="Topic not found",
    )


# ============================================================================
# GRACE - THE DOCTRINE OF GRACE
# ============================================================================
@router.get("/grace", response_class=HTMLResponse)
def grace_page(request: Request):
    """Grace - The Doctrine of Grace."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": GRACE_DATA["categories"],
            "page_title": GRACE_DATA["title"],
            "page_subtitle": GRACE_DATA["subtitle"],
            "page_description": GRACE_DATA["introduction"],
            "base_url": "/grace",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Grace", "url": None}
            ]
        }
    )


@router.get("/grace/pdf")
async def grace_page_pdf():
    return await _resource_index_pdf_response(
        GRACE_DATA["categories"],
        page_title=GRACE_DATA["title"],
        page_subtitle=GRACE_DATA["subtitle"],
        page_description=GRACE_DATA["introduction"]
    )


@router.get("/grace/{item_slug}", response_class=HTMLResponse)
def grace_detail(request: Request, item_slug: str):
    """Individual Grace topic detail page."""
    return _resource_detail_response(
        request,
        GRACE_DATA["categories"],
        item_slug,
        resource_title="Grace",
        back_url="/grace",
        back_text="Grace",
        not_found_message="Topic not found",
    )


@router.get("/grace/{item_slug}/pdf")
async def grace_detail_pdf(item_slug: str):
    """PDF export for Grace topics."""
    return await _resource_detail_pdf_response(
        GRACE_DATA["categories"],
        item_slug,
        resource_title="Grace",
        not_found_message="Topic not found",
    )


# ============================================================================
# JUSTIFICATION - THE DOCTRINE OF JUSTIFICATION
# ============================================================================
@router.get("/justification", response_class=HTMLResponse)
def justification_page(request: Request):
    """Justification - The Doctrine of Justification."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": JUSTIFICATION_DATA["categories"],
            "page_title": JUSTIFICATION_DATA["title"],
            "page_subtitle": JUSTIFICATION_DATA["subtitle"],
            "page_description": JUSTIFICATION_DATA["introduction"],
            "base_url": "/justification",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Justification", "url": None}
            ]
        }
    )


@router.get("/justification/pdf")
async def justification_page_pdf():
    return await _resource_index_pdf_response(
        JUSTIFICATION_DATA["categories"],
        page_title=JUSTIFICATION_DATA["title"],
        page_subtitle=JUSTIFICATION_DATA["subtitle"],
        page_description=JUSTIFICATION_DATA["introduction"]
    )


@router.get("/justification/{item_slug}", response_class=HTMLResponse)
def justification_detail(request: Request, item_slug: str):
    """Individual Justification topic detail page."""
    return _resource_detail_response(
        request,
        JUSTIFICATION_DATA["categories"],
        item_slug,
        resource_title="Justification",
        back_url="/justification",
        back_text="Justification",
        not_found_message="Topic not found",
    )


@router.get("/justification/{item_slug}/pdf")
async def justification_detail_pdf(item_slug: str):
    """PDF export for Justification topics."""
    return await _resource_detail_pdf_response(
        JUSTIFICATION_DATA["categories"],
        item_slug,
        resource_title="Justification",
        not_found_message="Topic not found",
    )


# ============================================================================
# SANCTIFICATION - THE DOCTRINE OF SANCTIFICATION
# ============================================================================
@router.get("/sanctification", response_class=HTMLResponse)
def sanctification_page(request: Request):
    """Sanctification - The Doctrine of Sanctification."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": SANCTIFICATION_DATA["categories"],
            "page_title": SANCTIFICATION_DATA["title"],
            "page_subtitle": SANCTIFICATION_DATA["subtitle"],
            "page_description": SANCTIFICATION_DATA["introduction"],
            "base_url": "/sanctification",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Sanctification", "url": None}
            ]
        }
    )


@router.get("/sanctification/pdf")
async def sanctification_page_pdf():
    return await _resource_index_pdf_response(
        SANCTIFICATION_DATA["categories"],
        page_title=SANCTIFICATION_DATA["title"],
        page_subtitle=SANCTIFICATION_DATA["subtitle"],
        page_description=SANCTIFICATION_DATA["introduction"]
    )


@router.get("/sanctification/{item_slug}", response_class=HTMLResponse)
def sanctification_detail(request: Request, item_slug: str):
    """Individual Sanctification topic detail page."""
    return _resource_detail_response(
        request,
        SANCTIFICATION_DATA["categories"],
        item_slug,
        resource_title="Sanctification",
        back_url="/sanctification",
        back_text="Sanctification",
        not_found_message="Topic not found",
    )


@router.get("/sanctification/{item_slug}/pdf")
async def sanctification_detail_pdf(item_slug: str):
    """PDF export for Sanctification topics."""
    return await _resource_detail_pdf_response(
        SANCTIFICATION_DATA["categories"],
        item_slug,
        resource_title="Sanctification",
        not_found_message="Topic not found",
    )


# ============================================================================
# LAW AND GOSPEL
# ============================================================================
@router.get("/law-and-gospel", response_class=HTMLResponse)
def law_and_gospel_page(request: Request):
    """Law and Gospel - The Doctrine of Law and Gospel."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": LAW_AND_GOSPEL_DATA["categories"],
            "page_title": LAW_AND_GOSPEL_DATA["title"],
            "page_subtitle": LAW_AND_GOSPEL_DATA["subtitle"],
            "page_description": LAW_AND_GOSPEL_DATA["introduction"],
            "base_url": "/law-and-gospel",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Law and Gospel", "url": None}
            ]
        }
    )


@router.get("/law-and-gospel/pdf")
async def law_and_gospel_page_pdf():
    return await _resource_index_pdf_response(
        LAW_AND_GOSPEL_DATA["categories"],
        page_title=LAW_AND_GOSPEL_DATA["title"],
        page_subtitle=LAW_AND_GOSPEL_DATA["subtitle"],
        page_description=LAW_AND_GOSPEL_DATA["introduction"]
    )


@router.get("/law-and-gospel/{item_slug}", response_class=HTMLResponse)
def law_and_gospel_detail(request: Request, item_slug: str):
    """Individual Law and Gospel topic detail page."""
    return _resource_detail_response(
        request,
        LAW_AND_GOSPEL_DATA["categories"],
        item_slug,
        resource_title="Law and Gospel",
        back_url="/law-and-gospel",
        back_text="Law and Gospel",
        not_found_message="Topic not found",
    )


@router.get("/law-and-gospel/{item_slug}/pdf")
async def law_and_gospel_detail_pdf(item_slug: str):
    """PDF export for Law and Gospel topics."""
    return await _resource_detail_pdf_response(
        LAW_AND_GOSPEL_DATA["categories"],
        item_slug,
        resource_title="Law and Gospel",
        not_found_message="Topic not found",
    )


# ============================================================================
# WORSHIP - THE DOCTRINE OF WORSHIP
# ============================================================================
@router.get("/worship", response_class=HTMLResponse)
def worship_page(request: Request):
    """Worship - The Doctrine of Worship."""
    return templates.TemplateResponse(
            request,
            "resource_index.html",
            {
            "books": get_books(),
            "resource_data": WORSHIP_DATA["categories"],
            "page_title": WORSHIP_DATA["title"],
            "page_subtitle": WORSHIP_DATA["subtitle"],
            "page_description": WORSHIP_DATA["introduction"],
            "base_url": "/worship",
            "pdf_available": WEASYPRINT_AVAILABLE,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "Worship", "url": None}
            ]
        }
    )


@router.get("/worship/pdf")
async def worship_page_pdf():
    return await _resource_index_pdf_response(
        WORSHIP_DATA["categories"],
        page_title=WORSHIP_DATA["title"],
        page_subtitle=WORSHIP_DATA["subtitle"],
        page_description=WORSHIP_DATA["introduction"]
    )


@router.get("/worship/{item_slug}", response_class=HTMLResponse)
def worship_detail(request: Request, item_slug: str):
    """Individual Worship topic detail page."""
    return _resource_detail_response(
        request,
        WORSHIP_DATA["categories"],
        item_slug,
        resource_title="Worship",
        back_url="/worship",
        back_text="Worship",
        not_found_message="Topic not found",
    )


@router.get("/worship/{item_slug}/pdf")
async def worship_detail_pdf(item_slug: str):
    """PDF export for Worship topics."""
    return await _resource_detail_pdf_response(
        WORSHIP_DATA["categories"],
        item_slug,
        resource_title="Worship",
        not_found_message="Topic not found",
    )
