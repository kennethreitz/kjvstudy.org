"""Biblical resources routes - maps, angels, prophets, names of God, etc.
(Responder port of routes/resources.py)

These routes handle the biblical reference and study resources pages.
Data is imported from the centralized data module to avoid duplication.
"""
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
    # Functions
    find_resource_by_slug,
)
from ..utils.helpers import create_slug, get_books
from ..utils.pdf import WEASYPRINT_AVAILABLE, pdf_context
from ._helpers import render, abort_404, pdf_resp


def find_item_by_slug(data: dict, slug: str):
    """Find an item in a nested data structure by its slug.

    Now uses O(1) slug index lookup instead of O(n) iteration.
    """
    return find_resource_by_slug(data, slug)


def _get_resource_item_or_404(req, resp, data: dict, slug: str, not_found_message: str):
    """Fetch a resource item by slug or render a 404 error.

    On a miss the shared error template is rendered into ``resp`` and a
    ``(None, None, None)`` tuple is returned so callers can bail out.
    """
    item, item_name, category_name = find_item_by_slug(data, slug)
    if not item:
        abort_404(req, resp, not_found_message)
        return None, None, None
    return item, item_name, category_name


def _resource_detail_response(
    req,
    resp,
    data: dict,
    slug: str,
    *,
    resource_title: str,
    back_url: str,
    back_text: str,
    not_found_message: str,
):
    """Render the shared resource detail template with optional PDF controls."""
    item, item_name, category_name = _get_resource_item_or_404(req, resp, data, slug, not_found_message)
    if item is None:
        return

    render(
        req,
        resp,
        "resource_detail.html",
        books=get_books(),
        item=item,
        item_name=item_name,
        category_name=category_name,
        resource_title=resource_title,
        back_url=back_url,
        back_text=back_text,
        **pdf_context(f"{req.url.path.rstrip('/')}/pdf"),
        breadcrumbs=[
            {"text": "Home", "url": "/"},
            {"text": "Resources", "url": "/resources"},
            {"text": resource_title, "url": back_url},
            {"text": item_name, "url": None},
        ],
    )


async def _resource_detail_pdf_response(
    req,
    resp,
    data: dict,
    slug: str,
    *,
    resource_title: str,
    not_found_message: str,
):
    """Generate a PDF export for a resource detail entry."""
    item, item_name, category_name = _get_resource_item_or_404(req, resp, data, slug, not_found_message)
    if item is None:
        return

    html_content = req.api.template(
        "resource_detail_pdf.html",
        item=item,
        item_name=item_name,
        category_name=category_name,
        resource_title=resource_title,
    )

    filename = f"{create_slug(item_name)}-{create_slug(resource_title)}.pdf"
    await pdf_resp(resp, html_content, filename)


async def _resource_index_pdf_response(req, resp, resource_data: dict, page_title: str, page_subtitle: str, page_description: str):
    """Generate PDF for resource index-style pages."""
    html_content = req.api.template(
        "resource_index_pdf.html",
        resource_data=resource_data,
        page_title=page_title,
        page_subtitle=page_subtitle,
        page_description=page_description,
    )

    filename = f"{create_slug(page_title)}.pdf"
    await pdf_resp(resp, html_content, filename)


def _resource_index_response(
    req,
    resp,
    *,
    resource_data: dict,
    page_title: str,
    page_subtitle: str,
    page_description: str,
    base_url: str,
    breadcrumb_label: str = None,
):
    """Render a standard ``resource_index.html`` listing page (shared scaffolding).

    Mirrors :func:`_resource_index_pdf_response`. The trailing breadcrumb defaults
    to ``page_title``; pass ``breadcrumb_label`` only when it should differ.
    """
    render(
        req,
        resp,
        "resource_index.html",
        books=get_books(),
        resource_data=resource_data,
        page_title=page_title,
        page_subtitle=page_subtitle,
        page_description=page_description,
        base_url=base_url,
        pdf_available=WEASYPRINT_AVAILABLE,
        breadcrumbs=[
            {"text": "Home", "url": "/"},
            {"text": "Resources", "url": "/resources"},
            {"text": breadcrumb_label or page_title, "url": None},
        ],
    )


def _custom_resource_index(req, resp, template: str, *, breadcrumb_text: str, **context):
    """Render a themed resource index page (one with its own bespoke template).

    Supplies the shared scaffolding every such page needs: the book list, the
    PDF-availability flag, and the Home / Resources / <page> breadcrumb trail.
    Page-specific data (e.g. ``angels_data=ANGELS_DATA``) is passed as kwargs.
    """
    render(
        req,
        resp,
        template,
        books=get_books(),
        pdf_available=WEASYPRINT_AVAILABLE,
        breadcrumbs=[
            {"text": "Home", "url": "/"},
            {"text": "Resources", "url": "/resources"},
            {"text": breadcrumb_text, "url": None},
        ],
        **context,
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


def register(api):
    # ========================================================================
    # BIBLICAL MAPS
    # ========================================================================
    @api.route("/biblical-maps")
    async def biblical_maps_page(req, resp):
        """Biblical maps page showing important biblical locations."""
        _custom_resource_index(
            req, resp, "biblical_maps.html",
            breadcrumb_text="Biblical Geography",
            biblical_locations=BIBLICAL_LOCATIONS,
        )

    # ========================================================================
    # BIBLICAL ANGELS
    # ========================================================================
    @api.route("/biblical-angels")
    async def biblical_angels_page(req, resp):
        """Biblical angels page exploring angels throughout Scripture."""
        _custom_resource_index(
            req, resp, "biblical_angels.html",
            breadcrumb_text="Biblical Angels",
            angels_data=ANGELS_DATA,
        )

    @api.route("/biblical-angels/pdf")
    async def biblical_angels_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            ANGELS_DATA,
            page_title="Biblical Angels",
            page_subtitle="Heavenly messengers throughout Scripture",
            page_description="Explore angels and angelic beings mentioned in the King James Bible, including Michael, Gabriel, and the heavenly host."
        )

    @api.route("/biblical-angels/{angel_slug}")
    async def angel_detail(req, resp, *, angel_slug):
        """Individual biblical angels detail page."""
        _resource_detail_response(
            req, resp,
            ANGELS_DATA,
            angel_slug,
            resource_title="Biblical Angels",
            back_url="/biblical-angels",
            back_text="Biblical Angels",
            not_found_message="Biblical Angels item not found",
        )

    @api.route("/biblical-angels/{angel_slug}/pdf")
    async def angel_detail_pdf(req, resp, *, angel_slug):
        """PDF export for a biblical angel detail page."""
        await _resource_detail_pdf_response(
            req, resp,
            ANGELS_DATA,
            angel_slug,
            resource_title="Biblical Angels",
            not_found_message="Biblical Angels item not found",
        )

    # ========================================================================
    # BIBLICAL PROPHETS
    # ========================================================================
    @api.route("/biblical-prophets")
    async def biblical_prophets_page(req, resp):
        """Biblical prophets page exploring the prophetic ministry throughout Scripture."""
        _custom_resource_index(
            req, resp, "biblical_prophets.html",
            breadcrumb_text="Biblical Prophets",
            prophets_data=PROPHETS_DATA,
        )

    @api.route("/biblical-prophets/pdf")
    async def biblical_prophets_pdf(req, resp):
        """PDF export for the prophets index."""
        html_content = req.api.template("biblical_prophets_pdf.html", prophets_data=PROPHETS_DATA)
        await pdf_resp(resp, html_content, "biblical-prophets.pdf")

    @api.route("/biblical-prophets/{prophet_slug}")
    async def prophet_detail(req, resp, *, prophet_slug):
        """Individual biblical prophets detail page."""
        _resource_detail_response(
            req, resp,
            PROPHETS_DATA,
            prophet_slug,
            resource_title="Biblical Prophets",
            back_url="/biblical-prophets",
            back_text="Biblical Prophets",
            not_found_message="Biblical Prophets item not found",
        )

    @api.route("/biblical-prophets/{prophet_slug}/pdf")
    async def prophet_detail_pdf(req, resp, *, prophet_slug):
        """PDF export for a biblical prophet entry."""
        await _resource_detail_pdf_response(
            req, resp,
            PROPHETS_DATA,
            prophet_slug,
            resource_title="Biblical Prophets",
            not_found_message="Biblical Prophets item not found",
        )

    # ========================================================================
    # NAMES OF GOD
    # ========================================================================
    @api.route("/names-of-god")
    async def names_of_god_page(req, resp):
        """Names of God page exploring divine names throughout Scripture."""
        _custom_resource_index(
            req, resp, "names_of_god.html",
            breadcrumb_text="Names of God",
            names_data=NAMES_DATA,
        )

    @api.route("/names-of-god/pdf")
    async def names_of_god_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            NAMES_DATA,
            page_title="Names of God",
            page_subtitle="Divine titles revealed in Scripture",
            page_description="Explore the revelation of God's names throughout Scripture and their meanings."
        )

    @api.route("/names-of-god/{name_slug}")
    async def name_of_god_detail(req, resp, *, name_slug):
        """Individual name of God detail page."""
        _resource_detail_response(
            req, resp,
            NAMES_DATA,
            name_slug,
            resource_title="Names of God",
            back_url="/names-of-god",
            back_text="Names of God",
            not_found_message="Name of God not found",
        )

    @api.route("/names-of-god/{name_slug}/pdf")
    async def name_of_god_detail_pdf(req, resp, *, name_slug):
        """PDF export for a Name of God entry."""
        await _resource_detail_pdf_response(
            req, resp,
            NAMES_DATA,
            name_slug,
            resource_title="Names of God",
            not_found_message="Name of God not found",
        )

    # ========================================================================
    # PARABLES
    # ========================================================================
    @api.route("/parables")
    async def parables_page(req, resp):
        """Parables of Jesus page."""
        _custom_resource_index(
            req, resp, "parables.html",
            breadcrumb_text="Parables of Jesus",
            parables_data=PARABLES_DATA,
        )

    @api.route("/parables/pdf")
    async def parables_pdf(req, resp):
        """PDF export for the parables index."""
        html_content = req.api.template("parables_pdf.html", parables_data=PARABLES_DATA)
        await pdf_resp(resp, html_content, "parables.pdf")

    @api.route("/parables/{parable_slug}")
    async def parable_detail(req, resp, *, parable_slug):
        """Individual parable detail page."""
        _resource_detail_response(
            req, resp,
            PARABLES_DATA,
            parable_slug,
            resource_title="Parables of Jesus",
            back_url="/parables",
            back_text="Parables of Jesus",
            not_found_message="Parable not found",
        )

    @api.route("/parables/{parable_slug}/pdf")
    async def parable_detail_pdf(req, resp, *, parable_slug):
        """PDF export for a parable entry."""
        await _resource_detail_pdf_response(
            req, resp,
            PARABLES_DATA,
            parable_slug,
            resource_title="Parables of Jesus",
            not_found_message="Parable not found",
        )

    # ========================================================================
    # BIBLICAL COVENANTS
    # ========================================================================
    @api.route("/biblical-covenants")
    async def biblical_covenants_page(req, resp):
        """Biblical covenants page."""
        _custom_resource_index(
            req, resp, "biblical_covenants.html",
            breadcrumb_text="Biblical Covenants",
            covenants_data=COVENANTS_DATA,
        )

    @api.route("/biblical-covenants/pdf")
    async def biblical_covenants_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            COVENANTS_DATA,
            page_title="Biblical Covenants",
            page_subtitle="Divine promises across redemptive history",
            page_description="Survey the major covenants established between God and His people throughout Scripture."
        )

    @api.route("/biblical-covenants/{covenant_slug}")
    async def covenant_detail(req, resp, *, covenant_slug):
        """Individual covenant detail page."""
        _resource_detail_response(
            req, resp,
            COVENANTS_DATA,
            covenant_slug,
            resource_title="Biblical Covenants",
            back_url="/biblical-covenants",
            back_text="Biblical Covenants",
            not_found_message="Biblical Covenant not found",
        )

    @api.route("/biblical-covenants/{covenant_slug}/pdf")
    async def covenant_detail_pdf(req, resp, *, covenant_slug):
        """PDF export for covenant entries."""
        await _resource_detail_pdf_response(
            req, resp,
            COVENANTS_DATA,
            covenant_slug,
            resource_title="Biblical Covenants",
            not_found_message="Biblical Covenant not found",
        )

    # ========================================================================
    # THE TWELVE APOSTLES
    # ========================================================================
    @api.route("/the-twelve-apostles")
    async def apostles_page(req, resp):
        """The Twelve Apostles page."""
        _custom_resource_index(
            req, resp, "twelve_apostles.html",
            breadcrumb_text="The Twelve Apostles",
            apostles_data=APOSTLES_DATA,
        )

    @api.route("/the-twelve-apostles/pdf")
    async def apostles_page_pdf(req, resp):
        """PDF export for the apostles index."""
        html_content = req.api.template("twelve_apostles_pdf.html", apostles_data=APOSTLES_DATA)
        await pdf_resp(resp, html_content, "twelve-apostles.pdf")

    @api.route("/the-twelve-apostles/{apostle_slug}")
    async def apostle_detail(req, resp, *, apostle_slug):
        """Individual apostle detail page."""
        _resource_detail_response(
            req, resp,
            APOSTLES_DATA,
            apostle_slug,
            resource_title="The Twelve Apostles",
            back_url="/the-twelve-apostles",
            back_text="The Twelve Apostles",
            not_found_message="Apostle not found",
        )

    @api.route("/the-twelve-apostles/{apostle_slug}/pdf")
    async def apostle_detail_pdf(req, resp, *, apostle_slug):
        """PDF export for apostle entries."""
        await _resource_detail_pdf_response(
            req, resp,
            APOSTLES_DATA,
            apostle_slug,
            resource_title="The Twelve Apostles",
            not_found_message="Apostle not found",
        )

    # ========================================================================
    # WOMEN OF THE BIBLE
    # ========================================================================
    @api.route("/women-of-the-bible")
    async def women_of_the_bible_page(req, resp):
        """Women of the Bible page."""
        _custom_resource_index(
            req, resp, "women_of_the_bible.html",
            breadcrumb_text="Women of the Bible",
            women_data=WOMEN_DATA,
        )

    @api.route("/women-of-the-bible/pdf")
    async def women_of_the_bible_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            WOMEN_DATA,
            page_title="Women of the Bible",
            page_subtitle="Faithful witnesses throughout redemptive history",
            page_description="Explore the lives, faith, and legacies of notable women throughout Scripture."
        )

    @api.route("/women-of-the-bible/{woman_slug}")
    async def woman_detail(req, resp, *, woman_slug):
        """Individual woman of the Bible detail page."""
        _resource_detail_response(
            req, resp,
            WOMEN_DATA,
            woman_slug,
            resource_title="Women of the Bible",
            back_url="/women-of-the-bible",
            back_text="Women of the Bible",
            not_found_message="Woman of the Bible not found",
        )

    @api.route("/women-of-the-bible/{woman_slug}/pdf")
    async def woman_detail_pdf(req, resp, *, woman_slug):
        """PDF export for Women of the Bible entries."""
        await _resource_detail_pdf_response(
            req, resp,
            WOMEN_DATA,
            woman_slug,
            resource_title="Women of the Bible",
            not_found_message="Woman of the Bible not found",
        )

    # ========================================================================
    # BIBLICAL FESTIVALS
    # ========================================================================
    @api.route("/biblical-festivals")
    async def biblical_festivals_page(req, resp):
        """Biblical festivals page."""
        _custom_resource_index(
            req, resp, "biblical_festivals.html",
            breadcrumb_text="Biblical Festivals",
            festivals_data=FESTIVALS_DATA,
        )

    @api.route("/biblical-festivals/pdf")
    async def biblical_festivals_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            FESTIVALS_DATA,
            page_title="Biblical Festivals",
            page_subtitle="Appointed feasts of the Lord",
            page_description="Learn about the appointed feasts and holy days ordained in the Law of Moses."
        )

    @api.route("/biblical-festivals/{festival_slug}")
    async def festival_detail(req, resp, *, festival_slug):
        """Individual biblical festival detail page."""
        _resource_detail_response(
            req, resp,
            FESTIVALS_DATA,
            festival_slug,
            resource_title="Biblical Festivals",
            back_url="/biblical-festivals",
            back_text="Biblical Festivals",
            not_found_message="Biblical Festival not found",
        )

    @api.route("/biblical-festivals/{festival_slug}/pdf")
    async def festival_detail_pdf(req, resp, *, festival_slug):
        """PDF export for biblical festival entries."""
        await _resource_detail_pdf_response(
            req, resp,
            FESTIVALS_DATA,
            festival_slug,
            resource_title="Biblical Festivals",
            not_found_message="Biblical Festival not found",
        )

    # ========================================================================
    # FRUITS OF THE SPIRIT
    # ========================================================================
    @api.route("/fruits-of-the-spirit")
    async def fruits_of_the_spirit_page(req, resp):
        """Fruits of the Spirit page."""
        _custom_resource_index(
            req, resp, "fruits_of_spirit.html",
            breadcrumb_text="Fruits of the Spirit",
            fruits_data=FRUITS_DATA,
        )

    @api.route("/fruits-of-the-spirit/pdf")
    async def fruits_of_the_spirit_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            FRUITS_DATA,
            page_title="Fruits of the Spirit",
            page_subtitle="Developing Christian character",
            page_description="Meditate on the Spirit-produced virtues described in Galatians 5."
        )

    @api.route("/fruits-of-the-spirit/{fruit_slug}")
    async def fruit_detail(req, resp, *, fruit_slug):
        """Individual fruit of the Spirit detail page."""
        _resource_detail_response(
            req, resp,
            FRUITS_DATA,
            fruit_slug,
            resource_title="Fruits of the Spirit",
            back_url="/fruits-of-the-spirit",
            back_text="Fruits of the Spirit",
            not_found_message="Fruit of the Spirit not found",
        )

    @api.route("/fruits-of-the-spirit/{fruit_slug}/pdf")
    async def fruit_detail_pdf(req, resp, *, fruit_slug):
        """PDF export for Fruits of the Spirit entries."""
        await _resource_detail_pdf_response(
            req, resp,
            FRUITS_DATA,
            fruit_slug,
            resource_title="Fruits of the Spirit",
            not_found_message="Fruit of the Spirit not found",
        )

    # ========================================================================
    # TETRAGRAMMATON (Special page with inline content)
    # ========================================================================
    @api.route("/tetragrammaton")
    async def tetragrammaton_page(req, resp):
        """The sacred Tetragrammaton - YHWH."""
        render(
            req,
            resp,
            "tetragrammaton.html",
            books=get_books(),
            content=TETRAGRAMMATON_CONTENT,
            pdf_available=WEASYPRINT_AVAILABLE,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Resources", "url": "/resources"},
                {"text": "The Tetragrammaton", "url": None}
            ],
        )

    @api.route("/tetragrammaton/pdf")
    async def tetragrammaton_pdf(req, resp):
        """PDF export for the Tetragrammaton page."""
        html_content = req.api.template("tetragrammaton_pdf.html", content=TETRAGRAMMATON_CONTENT)
        await pdf_resp(resp, html_content, "tetragrammaton.pdf")

    # ========================================================================
    # MIRACLES OF JESUS
    # ========================================================================
    @api.route("/miracles-of-jesus")
    async def miracles_page(req, resp):
        """Miracles of Jesus page."""
        _resource_index_response(
            req, resp,
            resource_data=MIRACLES_DATA,
            page_title="Miracles of Jesus",
            page_subtitle="Signs and Wonders Manifesting Divine Authority",
            page_description="Explore the miracles of Jesus Christ recorded in the Gospels - healings, nature miracles, exorcisms, and raisings from the dead.",
            base_url="/miracles-of-jesus",
        )

    @api.route("/miracles-of-jesus/pdf")
    async def miracles_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            MIRACLES_DATA,
            page_title="Miracles of Jesus",
            page_subtitle="Signs and Wonders Manifesting Divine Authority",
            page_description="Explore the miracles of Jesus Christ recorded in the Gospels - healings, nature miracles, exorcisms, and raisings from the dead."
        )

    @api.route("/miracles-of-jesus/{miracle_slug}")
    async def miracle_detail(req, resp, *, miracle_slug):
        """Individual miracle detail page."""
        _resource_detail_response(
            req, resp,
            MIRACLES_DATA,
            miracle_slug,
            resource_title="Miracles of Jesus",
            back_url="/miracles-of-jesus",
            back_text="Miracles of Jesus",
            not_found_message="Miracle not found",
        )

    @api.route("/miracles-of-jesus/{miracle_slug}/pdf")
    async def miracle_detail_pdf(req, resp, *, miracle_slug):
        """PDF export for miracle entries."""
        await _resource_detail_pdf_response(
            req, resp,
            MIRACLES_DATA,
            miracle_slug,
            resource_title="Miracles of Jesus",
            not_found_message="Miracle not found",
        )

    # ========================================================================
    # PRAYERS OF THE BIBLE
    # ========================================================================
    @api.route("/prayers-of-the-bible")
    async def prayers_page(req, resp):
        """Prayers of the Bible page."""
        _resource_index_response(
            req, resp,
            resource_data=PRAYERS_DATA,
            page_title="Prayers of the Bible",
            page_subtitle="Sacred Conversations with the Almighty",
            page_description="Explore the prayers recorded in Scripture - from the Psalms to the prayers of Jesus, Paul, and the early church.",
            base_url="/prayers-of-the-bible",
        )

    @api.route("/prayers-of-the-bible/pdf")
    async def prayers_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            PRAYERS_DATA,
            page_title="Prayers of the Bible",
            page_subtitle="Sacred Conversations with the Almighty",
            page_description="Explore the prayers recorded in Scripture - from the Psalms to the prayers of Jesus, Paul, and the early church."
        )

    @api.route("/prayers-of-the-bible/{prayer_slug}")
    async def prayer_detail(req, resp, *, prayer_slug):
        """Individual prayer detail page."""
        _resource_detail_response(
            req, resp,
            PRAYERS_DATA,
            prayer_slug,
            resource_title="Prayers of the Bible",
            back_url="/prayers-of-the-bible",
            back_text="Prayers of the Bible",
            not_found_message="Prayer not found",
        )

    @api.route("/prayers-of-the-bible/{prayer_slug}/pdf")
    async def prayer_detail_pdf(req, resp, *, prayer_slug):
        """PDF export for prayer entries."""
        await _resource_detail_pdf_response(
            req, resp,
            PRAYERS_DATA,
            prayer_slug,
            resource_title="Prayers of the Bible",
            not_found_message="Prayer not found",
        )

    # ========================================================================
    # THE BEATITUDES
    # ========================================================================
    @api.route("/beatitudes")
    async def beatitudes_page(req, resp):
        """The Beatitudes page."""
        _resource_index_response(
            req, resp,
            resource_data=BEATITUDES_DATA,
            page_title="The Beatitudes",
            page_subtitle="The Blessings of the Kingdom",
            page_description="Explore the Beatitudes from Jesus's Sermon on the Mount - the foundational blessings that describe the character of kingdom citizens.",
            base_url="/beatitudes",
        )

    @api.route("/beatitudes/pdf")
    async def beatitudes_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            BEATITUDES_DATA,
            page_title="The Beatitudes",
            page_subtitle="The Blessings of the Kingdom",
            page_description="Explore the Beatitudes from Jesus's Sermon on the Mount - the foundational blessings that describe the character of kingdom citizens."
        )

    @api.route("/beatitudes/{beatitude_slug}")
    async def beatitude_detail(req, resp, *, beatitude_slug):
        """Individual beatitude detail page."""
        _resource_detail_response(
            req, resp,
            BEATITUDES_DATA,
            beatitude_slug,
            resource_title="The Beatitudes",
            back_url="/beatitudes",
            back_text="The Beatitudes",
            not_found_message="Beatitude not found",
        )

    @api.route("/beatitudes/{beatitude_slug}/pdf")
    async def beatitude_detail_pdf(req, resp, *, beatitude_slug):
        """PDF export for Beatitudes entries."""
        await _resource_detail_pdf_response(
            req, resp,
            BEATITUDES_DATA,
            beatitude_slug,
            resource_title="The Beatitudes",
            not_found_message="Beatitude not found",
        )

    # ========================================================================
    # THE TEN COMMANDMENTS
    # ========================================================================
    @api.route("/ten-commandments")
    async def ten_commandments_page(req, resp):
        """The Ten Commandments page."""
        _resource_index_response(
            req, resp,
            resource_data=TEN_COMMANDMENTS_DATA,
            page_title="The Ten Commandments",
            page_subtitle="The Moral Law of God",
            page_description="Study the Ten Commandments given by God to Moses on Mount Sinai - the foundation of biblical morality and divine law.",
            base_url="/ten-commandments",
        )

    @api.route("/ten-commandments/pdf")
    async def ten_commandments_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            TEN_COMMANDMENTS_DATA,
            page_title="The Ten Commandments",
            page_subtitle="The Moral Law of God",
            page_description="Study the Ten Commandments given by God to Moses on Mount Sinai - the foundation of biblical morality and divine law."
        )

    @api.route("/ten-commandments/{commandment_slug}")
    async def commandment_detail(req, resp, *, commandment_slug):
        """Individual commandment detail page."""
        _resource_detail_response(
            req, resp,
            TEN_COMMANDMENTS_DATA,
            commandment_slug,
            resource_title="The Ten Commandments",
            back_url="/ten-commandments",
            back_text="The Ten Commandments",
            not_found_message="Commandment not found",
        )

    @api.route("/ten-commandments/{commandment_slug}/pdf")
    async def commandment_detail_pdf(req, resp, *, commandment_slug):
        """PDF export for Ten Commandments entries."""
        await _resource_detail_pdf_response(
            req, resp,
            TEN_COMMANDMENTS_DATA,
            commandment_slug,
            resource_title="The Ten Commandments",
            not_found_message="Commandment not found",
        )

    # ========================================================================
    # THE ARMOR OF GOD
    # ========================================================================
    @api.route("/armor-of-god")
    async def armor_of_god_page(req, resp):
        """The Armor of God page."""
        _resource_index_response(
            req, resp,
            resource_data=ARMOR_OF_GOD_DATA,
            page_title="The Armor of God",
            page_subtitle="Divine Equipment for Spiritual Warfare",
            page_description="Study the Armor of God from Ephesians 6 - the spiritual equipment believers need to stand against the wiles of the devil.",
            base_url="/armor-of-god",
        )

    @api.route("/armor-of-god/pdf")
    async def armor_of_god_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            ARMOR_OF_GOD_DATA,
            page_title="The Armor of God",
            page_subtitle="Divine Equipment for Spiritual Warfare",
            page_description="Study the Armor of God from Ephesians 6 - the spiritual equipment believers need to stand against the wiles of the devil."
        )

    @api.route("/armor-of-god/{armor_slug}")
    async def armor_detail(req, resp, *, armor_slug):
        """Individual armor piece detail page."""
        _resource_detail_response(
            req, resp,
            ARMOR_OF_GOD_DATA,
            armor_slug,
            resource_title="The Armor of God",
            back_url="/armor-of-god",
            back_text="The Armor of God",
            not_found_message="Armor piece not found",
        )

    @api.route("/armor-of-god/{armor_slug}/pdf")
    async def armor_detail_pdf(req, resp, *, armor_slug):
        """PDF export for Armor of God entries."""
        await _resource_detail_pdf_response(
            req, resp,
            ARMOR_OF_GOD_DATA,
            armor_slug,
            resource_title="The Armor of God",
            not_found_message="Armor piece not found",
        )

    # ========================================================================
    # I AM STATEMENTS OF JESUS
    # ========================================================================
    @api.route("/i-am-statements")
    async def i_am_statements_page(req, resp):
        """I Am Statements of Jesus page."""
        _resource_index_response(
            req, resp,
            resource_data=I_AM_STATEMENTS_DATA,
            page_title="I Am Statements of Jesus",
            page_subtitle="Divine Self-Revelations in the Gospel of John",
            page_description="Explore the seven 'I Am' statements of Jesus in John's Gospel - profound declarations of His divine nature and mission.",
            base_url="/i-am-statements",
            breadcrumb_label="I Am Statements",
        )

    @api.route("/i-am-statements/pdf")
    async def i_am_statements_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            I_AM_STATEMENTS_DATA,
            page_title="I Am Statements of Jesus",
            page_subtitle="Divine Self-Revelations in the Gospel of John",
            page_description="Explore the seven 'I Am' statements of Jesus in John's Gospel - profound declarations of His divine nature and mission."
        )

    @api.route("/i-am-statements/{statement_slug}")
    async def i_am_statement_detail(req, resp, *, statement_slug):
        """Individual I Am statement detail page."""
        _resource_detail_response(
            req, resp,
            I_AM_STATEMENTS_DATA,
            statement_slug,
            resource_title="I Am Statements",
            back_url="/i-am-statements",
            back_text="I Am Statements",
            not_found_message="Statement not found",
        )

    @api.route("/i-am-statements/{statement_slug}/pdf")
    async def i_am_statement_detail_pdf(req, resp, *, statement_slug):
        """PDF export for I Am statement entries."""
        await _resource_detail_pdf_response(
            req, resp,
            I_AM_STATEMENTS_DATA,
            statement_slug,
            resource_title="I Am Statements",
            not_found_message="Statement not found",
        )

    # ========================================================================
    # THE TRINITY
    # ========================================================================
    @api.route("/trinity")
    async def trinity_page(req, resp):
        """The Trinity - doctrine of God page."""
        _resource_index_response(
            req, resp,
            resource_data=TRINITY_DATA,
            page_title="The Trinity",
            page_subtitle="The Doctrine of One God in Three Persons",
            page_description="An expansive theological study of the Trinity - the doctrine that God eternally exists as Father, Son, and Holy Spirit, three distinct Persons sharing one divine essence.",
            base_url="/trinity",
        )

    @api.route("/trinity/pdf")
    async def trinity_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            TRINITY_DATA,
            page_title="The Trinity",
            page_subtitle="The Doctrine of One God in Three Persons",
            page_description="An expansive theological study of the Trinity - the doctrine that God eternally exists as Father, Son, and Holy Spirit, three distinct Persons sharing one divine essence."
        )

    @api.route("/trinity/{item_slug}")
    async def trinity_detail(req, resp, *, item_slug):
        """Individual Trinity topic detail page."""
        _resource_detail_response(
            req, resp,
            TRINITY_DATA,
            item_slug,
            resource_title="The Trinity",
            back_url="/trinity",
            back_text="The Trinity",
            not_found_message="Topic not found",
        )

    @api.route("/trinity/{item_slug}/pdf")
    async def trinity_detail_pdf(req, resp, *, item_slug):
        """PDF export for Trinity topics."""
        await _resource_detail_pdf_response(
            req, resp,
            TRINITY_DATA,
            item_slug,
            resource_title="The Trinity",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # CHRISTOLOGY
    # ========================================================================
    @api.route("/christology")
    async def christology_page(req, resp):
        """Christology - the doctrine of Christ page."""
        _resource_index_response(
            req, resp,
            resource_data=CHRISTOLOGY_DATA,
            page_title="Christology",
            page_subtitle="The Doctrine of the Person and Work of Christ",
            page_description="An expansive theological study of Christology - the doctrine concerning Jesus Christ, His divine-human nature, His offices, and His saving work.",
            base_url="/christology",
        )

    @api.route("/christology/pdf")
    async def christology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            CHRISTOLOGY_DATA,
            page_title="Christology",
            page_subtitle="The Doctrine of the Person and Work of Christ",
            page_description="An expansive theological study of Christology - the doctrine concerning Jesus Christ, His divine-human nature, His offices, and His saving work."
        )

    @api.route("/christology/{item_slug}")
    async def christology_detail(req, resp, *, item_slug):
        """Individual Christology topic detail page."""
        _resource_detail_response(
            req, resp,
            CHRISTOLOGY_DATA,
            item_slug,
            resource_title="Christology",
            back_url="/christology",
            back_text="Christology",
            not_found_message="Topic not found",
        )

    @api.route("/christology/{item_slug}/pdf")
    async def christology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Christology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            CHRISTOLOGY_DATA,
            item_slug,
            resource_title="Christology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # SOTERIOLOGY
    # ========================================================================
    @api.route("/soteriology")
    async def soteriology_page(req, resp):
        """Soteriology - the doctrine of salvation page."""
        _resource_index_response(
            req, resp,
            resource_data=SOTERIOLOGY_DATA,
            page_title="Soteriology",
            page_subtitle="The Doctrine of Salvation",
            page_description="An expansive theological study of Soteriology - the doctrine of salvation, covering election, atonement, regeneration, justification, sanctification, and glorification.",
            base_url="/soteriology",
        )

    @api.route("/soteriology/pdf")
    async def soteriology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            SOTERIOLOGY_DATA,
            page_title="Soteriology",
            page_subtitle="The Doctrine of Salvation",
            page_description="An expansive theological study of Soteriology - the doctrine of salvation, covering election, atonement, regeneration, justification, sanctification, and glorification."
        )

    @api.route("/soteriology/{item_slug}")
    async def soteriology_detail(req, resp, *, item_slug):
        """Individual Soteriology topic detail page."""
        _resource_detail_response(
            req, resp,
            SOTERIOLOGY_DATA,
            item_slug,
            resource_title="Soteriology",
            back_url="/soteriology",
            back_text="Soteriology",
            not_found_message="Topic not found",
        )

    @api.route("/soteriology/{item_slug}/pdf")
    async def soteriology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Soteriology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            SOTERIOLOGY_DATA,
            item_slug,
            resource_title="Soteriology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # PNEUMATOLOGY
    # ========================================================================
    @api.route("/pneumatology")
    async def pneumatology_page(req, resp):
        """Pneumatology - the doctrine of the Holy Spirit page."""
        _resource_index_response(
            req, resp,
            resource_data=PNEUMATOLOGY_DATA,
            page_title="Pneumatology",
            page_subtitle="The Doctrine of the Holy Spirit",
            page_description="An expansive theological study of Pneumatology - the doctrine of the Holy Spirit, His person, deity, work in salvation, and ministry to believers.",
            base_url="/pneumatology",
        )

    @api.route("/pneumatology/pdf")
    async def pneumatology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            PNEUMATOLOGY_DATA,
            page_title="Pneumatology",
            page_subtitle="The Doctrine of the Holy Spirit",
            page_description="An expansive theological study of Pneumatology - the doctrine of the Holy Spirit, His person, deity, work in salvation, and ministry to believers."
        )

    @api.route("/pneumatology/{item_slug}")
    async def pneumatology_detail(req, resp, *, item_slug):
        """Individual Pneumatology topic detail page."""
        _resource_detail_response(
            req, resp,
            PNEUMATOLOGY_DATA,
            item_slug,
            resource_title="Pneumatology",
            back_url="/pneumatology",
            back_text="Pneumatology",
            not_found_message="Topic not found",
        )

    @api.route("/pneumatology/{item_slug}/pdf")
    async def pneumatology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Pneumatology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            PNEUMATOLOGY_DATA,
            item_slug,
            resource_title="Pneumatology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # ESCHATOLOGY
    # ========================================================================
    @api.route("/eschatology")
    async def eschatology_page(req, resp):
        """Eschatology - the doctrine of last things page."""
        _resource_index_response(
            req, resp,
            resource_data=ESCHATOLOGY_DATA,
            page_title="Eschatology",
            page_subtitle="The Doctrine of Last Things",
            page_description="An expansive theological study of Eschatology - the doctrine of death, resurrection, the second coming of Christ, final judgment, and eternal destinies.",
            base_url="/eschatology",
        )

    @api.route("/eschatology/pdf")
    async def eschatology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            ESCHATOLOGY_DATA,
            page_title="Eschatology",
            page_subtitle="The Doctrine of Last Things",
            page_description="An expansive theological study of Eschatology - the doctrine of death, resurrection, the second coming of Christ, final judgment, and eternal destinies."
        )

    @api.route("/eschatology/{item_slug}")
    async def eschatology_detail(req, resp, *, item_slug):
        """Individual Eschatology topic detail page."""
        _resource_detail_response(
            req, resp,
            ESCHATOLOGY_DATA,
            item_slug,
            resource_title="Eschatology",
            back_url="/eschatology",
            back_text="Eschatology",
            not_found_message="Topic not found",
        )

    @api.route("/eschatology/{item_slug}/pdf")
    async def eschatology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Eschatology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            ESCHATOLOGY_DATA,
            item_slug,
            resource_title="Eschatology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # ECCLESIOLOGY
    # ========================================================================
    @api.route("/ecclesiology")
    async def ecclesiology_page(req, resp):
        """Ecclesiology - the doctrine of the church page."""
        _resource_index_response(
            req, resp,
            resource_data=ECCLESIOLOGY_DATA,
            page_title="Ecclesiology",
            page_subtitle="The Doctrine of the Church",
            page_description="An expansive theological study of Ecclesiology - the doctrine of the church, its nature, marks, government, mission, and ordinances.",
            base_url="/ecclesiology",
        )

    @api.route("/ecclesiology/pdf")
    async def ecclesiology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            ECCLESIOLOGY_DATA,
            page_title="Ecclesiology",
            page_subtitle="The Doctrine of the Church",
            page_description="An expansive theological study of Ecclesiology - the doctrine of the church, its nature, marks, government, mission, and ordinances."
        )

    @api.route("/ecclesiology/{item_slug}")
    async def ecclesiology_detail(req, resp, *, item_slug):
        """Individual Ecclesiology topic detail page."""
        _resource_detail_response(
            req, resp,
            ECCLESIOLOGY_DATA,
            item_slug,
            resource_title="Ecclesiology",
            back_url="/ecclesiology",
            back_text="Ecclesiology",
            not_found_message="Topic not found",
        )

    @api.route("/ecclesiology/{item_slug}/pdf")
    async def ecclesiology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Ecclesiology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            ECCLESIOLOGY_DATA,
            item_slug,
            resource_title="Ecclesiology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # TYPES AND SHADOWS OF CHRIST
    # ========================================================================
    @api.route("/types-and-shadows")
    async def types_and_shadows_page(req, resp):
        """Types and Shadows of Christ page."""
        _resource_index_response(
            req, resp,
            resource_data=TYPES_AND_SHADOWS_DATA,
            page_title="Types and Shadows of Christ",
            page_subtitle="Old Testament Figures Fulfilled in Christ",
            page_description="An expansive study of Old Testament types and shadows pointing to Christ - persons, events, and institutions that prefigure and find their fulfillment in Jesus.",
            base_url="/types-and-shadows",
            breadcrumb_label="Types and Shadows",
        )

    @api.route("/types-and-shadows/pdf")
    async def types_and_shadows_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            TYPES_AND_SHADOWS_DATA,
            page_title="Types and Shadows of Christ",
            page_subtitle="Old Testament Figures Fulfilled in Christ",
            page_description="An expansive study of Old Testament types and shadows pointing to Christ - persons, events, and institutions that prefigure and find their fulfillment in Jesus."
        )

    @api.route("/types-and-shadows/{item_slug}")
    async def types_and_shadows_detail(req, resp, *, item_slug):
        """Individual Types and Shadows topic detail page."""
        _resource_detail_response(
            req, resp,
            TYPES_AND_SHADOWS_DATA,
            item_slug,
            resource_title="Types and Shadows",
            back_url="/types-and-shadows",
            back_text="Types and Shadows",
            not_found_message="Topic not found",
        )

    @api.route("/types-and-shadows/{item_slug}/pdf")
    async def types_and_shadows_detail_pdf(req, resp, *, item_slug):
        """PDF export for Types and Shadows topics."""
        await _resource_detail_pdf_response(
            req, resp,
            TYPES_AND_SHADOWS_DATA,
            item_slug,
            resource_title="Types and Shadows",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # MESSIANIC PROPHECIES
    # ========================================================================
    @api.route("/messianic-prophecies")
    async def messianic_prophecies_page(req, resp):
        """Messianic Prophecies page."""
        _resource_index_response(
            req, resp,
            resource_data=MESSIANIC_PROPHECIES_DATA,
            page_title="Messianic Prophecies",
            page_subtitle="Old Testament Predictions Fulfilled in Christ",
            page_description="An expansive study of Messianic prophecies - Old Testament predictions concerning the Messiah's coming, ministry, suffering, and triumph, all fulfilled in Jesus Christ.",
            base_url="/messianic-prophecies",
        )

    @api.route("/messianic-prophecies/pdf")
    async def messianic_prophecies_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            MESSIANIC_PROPHECIES_DATA,
            page_title="Messianic Prophecies",
            page_subtitle="Old Testament Predictions Fulfilled in Christ",
            page_description="An expansive study of Messianic prophecies - Old Testament predictions concerning the Messiah's coming, ministry, suffering, and triumph, all fulfilled in Jesus Christ."
        )

    @api.route("/messianic-prophecies/{item_slug}")
    async def messianic_prophecies_detail(req, resp, *, item_slug):
        """Individual Messianic Prophecy topic detail page."""
        _resource_detail_response(
            req, resp,
            MESSIANIC_PROPHECIES_DATA,
            item_slug,
            resource_title="Messianic Prophecies",
            back_url="/messianic-prophecies",
            back_text="Messianic Prophecies",
            not_found_message="Topic not found",
        )

    @api.route("/messianic-prophecies/{item_slug}/pdf")
    async def messianic_prophecies_detail_pdf(req, resp, *, item_slug):
        """PDF export for Messianic Prophecies topics."""
        await _resource_detail_pdf_response(
            req, resp,
            MESSIANIC_PROPHECIES_DATA,
            item_slug,
            resource_title="Messianic Prophecies",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # THE BLOOD IN SCRIPTURE
    # ========================================================================
    @api.route("/blood-in-scripture")
    async def blood_in_scripture_page(req, resp):
        """The Blood in Scripture page."""
        _resource_index_response(
            req, resp,
            resource_data=BLOOD_IN_SCRIPTURE_DATA,
            page_title="The Blood in Scripture",
            page_subtitle="The Theology of Redemption Through Blood",
            page_description="An expansive study of the blood in Scripture - its significance, Old Testament foundations, and ultimate fulfillment in the blood of Christ for redemption, justification, and cleansing.",
            base_url="/blood-in-scripture",
        )

    @api.route("/blood-in-scripture/pdf")
    async def blood_in_scripture_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            BLOOD_IN_SCRIPTURE_DATA,
            page_title="The Blood in Scripture",
            page_subtitle="The Theology of Redemption Through Blood",
            page_description="An expansive study of the blood in Scripture - its significance, Old Testament foundations, and ultimate fulfillment in the blood of Christ for redemption, justification, and cleansing."
        )

    @api.route("/blood-in-scripture/{item_slug}")
    async def blood_in_scripture_detail(req, resp, *, item_slug):
        """Individual Blood in Scripture topic detail page."""
        _resource_detail_response(
            req, resp,
            BLOOD_IN_SCRIPTURE_DATA,
            item_slug,
            resource_title="The Blood in Scripture",
            back_url="/blood-in-scripture",
            back_text="The Blood in Scripture",
            not_found_message="Topic not found",
        )

    @api.route("/blood-in-scripture/{item_slug}/pdf")
    async def blood_in_scripture_detail_pdf(req, resp, *, item_slug):
        """PDF export for Blood in Scripture topics."""
        await _resource_detail_pdf_response(
            req, resp,
            BLOOD_IN_SCRIPTURE_DATA,
            item_slug,
            resource_title="The Blood in Scripture",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # THE KINGDOM OF GOD
    # ========================================================================
    @api.route("/kingdom-of-god")
    async def kingdom_of_god_page(req, resp):
        """The Kingdom of God page."""
        _resource_index_response(
            req, resp,
            resource_data=KINGDOM_OF_GOD_DATA,
            page_title="The Kingdom of God",
            page_subtitle="The Reign of God Through Christ",
            page_description="An expansive study of the Kingdom of God - its nature, King, entrance requirements, growth, and ultimate consummation at Christ's return.",
            base_url="/kingdom-of-god",
        )

    @api.route("/kingdom-of-god/pdf")
    async def kingdom_of_god_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            KINGDOM_OF_GOD_DATA,
            page_title="The Kingdom of God",
            page_subtitle="The Reign of God Through Christ",
            page_description="An expansive study of the Kingdom of God - its nature, King, entrance requirements, growth, and ultimate consummation at Christ's return."
        )

    @api.route("/kingdom-of-god/{item_slug}")
    async def kingdom_of_god_detail(req, resp, *, item_slug):
        """Individual Kingdom of God topic detail page."""
        _resource_detail_response(
            req, resp,
            KINGDOM_OF_GOD_DATA,
            item_slug,
            resource_title="The Kingdom of God",
            back_url="/kingdom-of-god",
            back_text="The Kingdom of God",
            not_found_message="Topic not found",
        )

    @api.route("/kingdom-of-god/{item_slug}/pdf")
    async def kingdom_of_god_detail_pdf(req, resp, *, item_slug):
        """PDF export for Kingdom of God topics."""
        await _resource_detail_pdf_response(
            req, resp,
            KINGDOM_OF_GOD_DATA,
            item_slug,
            resource_title="The Kingdom of God",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # NAMES AND TITLES OF CHRIST
    # ========================================================================
    @api.route("/names-of-christ")
    async def names_of_christ_page(req, resp):
        """Names and Titles of Christ page."""
        _resource_index_response(
            req, resp,
            resource_data=NAMES_OF_CHRIST_DATA,
            page_title="Names and Titles of Christ",
            page_subtitle="The Glorious Designations of Our Lord",
            page_description="An expansive study of the names and titles of Jesus Christ - divine names, messianic titles, redemptive designations, and relational names revealing His person and work.",
            base_url="/names-of-christ",
            breadcrumb_label="Names of Christ",
        )

    @api.route("/names-of-christ/pdf")
    async def names_of_christ_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            NAMES_OF_CHRIST_DATA,
            page_title="Names and Titles of Christ",
            page_subtitle="The Glorious Designations of Our Lord",
            page_description="An expansive study of the names and titles of Jesus Christ - divine names, messianic titles, redemptive designations, and relational names revealing His person and work."
        )

    @api.route("/names-of-christ/{item_slug}")
    async def names_of_christ_detail(req, resp, *, item_slug):
        """Individual Names of Christ topic detail page."""
        _resource_detail_response(
            req, resp,
            NAMES_OF_CHRIST_DATA,
            item_slug,
            resource_title="Names of Christ",
            back_url="/names-of-christ",
            back_text="Names of Christ",
            not_found_message="Topic not found",
        )

    @api.route("/names-of-christ/{item_slug}/pdf")
    async def names_of_christ_detail_pdf(req, resp, *, item_slug):
        """PDF export for Names of Christ topics."""
        await _resource_detail_pdf_response(
            req, resp,
            NAMES_OF_CHRIST_DATA,
            item_slug,
            resource_title="Names of Christ",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # SPIRITS AND DEMONS
    # ========================================================================
    @api.route("/spirits-and-demons")
    async def spirits_and_demons_page(req, resp):
        """Spirits and Demons - biblical demonology page."""
        _resource_index_response(
            req, resp,
            resource_data=SPIRITS_AND_DEMONS_DATA,
            page_title="Spirits & Demons",
            page_subtitle="Biblical Demonology and Spiritual Warfare",
            page_description="A comprehensive study of demons, Satan, evil spirits, and spiritual warfare in Scripture—from Legion to the Lake of Fire.",
            base_url="/spirits-and-demons",
        )

    @api.route("/spirits-and-demons/pdf")
    async def spirits_and_demons_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            SPIRITS_AND_DEMONS_DATA,
            page_title="Spirits & Demons",
            page_subtitle="Biblical Demonology and Spiritual Warfare",
            page_description="A comprehensive study of demons, Satan, evil spirits, and spiritual warfare in Scripture—from Legion to the Lake of Fire."
        )

    @api.route("/spirits-and-demons/{item_slug}")
    async def spirits_and_demons_detail(req, resp, *, item_slug):
        """Individual Spirits and Demons topic detail page."""
        _resource_detail_response(
            req, resp,
            SPIRITS_AND_DEMONS_DATA,
            item_slug,
            resource_title="Spirits & Demons",
            back_url="/spirits-and-demons",
            back_text="Spirits & Demons",
            not_found_message="Topic not found",
        )

    @api.route("/spirits-and-demons/{item_slug}/pdf")
    async def spirits_and_demons_detail_pdf(req, resp, *, item_slug):
        """PDF export for Spirits & Demons topics."""
        await _resource_detail_pdf_response(
            req, resp,
            SPIRITS_AND_DEMONS_DATA,
            item_slug,
            resource_title="Spirits & Demons",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # PERSONIFICATIONS IN SCRIPTURE
    # ========================================================================
    @api.route("/personifications")
    async def personifications_page(req, resp):
        """Personifications in Scripture - abstract concepts given human form."""
        _resource_index_response(
            req, resp,
            resource_data=PERSONIFICATIONS_DATA,
            page_title="Personifications in Scripture",
            page_subtitle="Abstract Concepts Given Human Form",
            page_description="A study of biblical personifications—Wisdom, Folly, Death, Sin, and other abstract concepts portrayed as persons throughout Scripture.",
            base_url="/personifications",
            breadcrumb_label="Personifications",
        )

    @api.route("/personifications/pdf")
    async def personifications_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            PERSONIFICATIONS_DATA,
            page_title="Personifications in Scripture",
            page_subtitle="Abstract Concepts Given Human Form",
            page_description="A study of biblical personifications—Wisdom, Folly, Death, Sin, and other abstract concepts portrayed as persons throughout Scripture."
        )

    @api.route("/personifications/{item_slug}")
    async def personifications_detail(req, resp, *, item_slug):
        """Individual Personification topic detail page."""
        _resource_detail_response(
            req, resp,
            PERSONIFICATIONS_DATA,
            item_slug,
            resource_title="Personifications",
            back_url="/personifications",
            back_text="Personifications",
            not_found_message="Topic not found",
        )

    @api.route("/personifications/{item_slug}/pdf")
    async def personifications_detail_pdf(req, resp, *, item_slug):
        """PDF export for Personifications topics."""
        await _resource_detail_pdf_response(
            req, resp,
            PERSONIFICATIONS_DATA,
            item_slug,
            resource_title="Personifications",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # BIBLIOLOGY - THE DOCTRINE OF SCRIPTURE
    # ========================================================================
    @api.route("/bibliology")
    async def bibliology_page(req, resp):
        """Bibliology - The Doctrine of Scripture."""
        _resource_index_response(
            req, resp,
            resource_data=BIBLIOLOGY_DATA["categories"],
            page_title=BIBLIOLOGY_DATA["title"],
            page_subtitle=BIBLIOLOGY_DATA["subtitle"],
            page_description=BIBLIOLOGY_DATA["introduction"],
            base_url="/bibliology",
            breadcrumb_label="Bibliology",
        )

    @api.route("/bibliology/pdf")
    async def bibliology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            BIBLIOLOGY_DATA["categories"],
            page_title=BIBLIOLOGY_DATA["title"],
            page_subtitle=BIBLIOLOGY_DATA["subtitle"],
            page_description=BIBLIOLOGY_DATA["introduction"]
        )

    @api.route("/bibliology/{item_slug}")
    async def bibliology_detail(req, resp, *, item_slug):
        """Individual Bibliology topic detail page."""
        _resource_detail_response(
            req, resp,
            BIBLIOLOGY_DATA["categories"],
            item_slug,
            resource_title="Bibliology",
            back_url="/bibliology",
            back_text="Bibliology",
            not_found_message="Topic not found",
        )

    @api.route("/bibliology/{item_slug}/pdf")
    async def bibliology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Bibliology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            BIBLIOLOGY_DATA["categories"],
            item_slug,
            resource_title="Bibliology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # THEOLOGY PROPER - THE ATTRIBUTES OF GOD
    # ========================================================================
    @api.route("/theology-proper")
    async def theology_proper_page(req, resp):
        """Theology Proper - The Attributes of God."""
        _resource_index_response(
            req, resp,
            resource_data=THEOLOGY_PROPER_DATA["categories"],
            page_title=THEOLOGY_PROPER_DATA["title"],
            page_subtitle=THEOLOGY_PROPER_DATA["subtitle"],
            page_description=THEOLOGY_PROPER_DATA["introduction"],
            base_url="/theology-proper",
            breadcrumb_label="Theology Proper",
        )

    @api.route("/theology-proper/pdf")
    async def theology_proper_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            THEOLOGY_PROPER_DATA["categories"],
            page_title=THEOLOGY_PROPER_DATA["title"],
            page_subtitle=THEOLOGY_PROPER_DATA["subtitle"],
            page_description=THEOLOGY_PROPER_DATA["introduction"]
        )

    @api.route("/theology-proper/{item_slug}")
    async def theology_proper_detail(req, resp, *, item_slug):
        """Individual Theology Proper topic detail page."""
        _resource_detail_response(
            req, resp,
            THEOLOGY_PROPER_DATA["categories"],
            item_slug,
            resource_title="Theology Proper",
            back_url="/theology-proper",
            back_text="Theology Proper",
            not_found_message="Topic not found",
        )

    @api.route("/theology-proper/{item_slug}/pdf")
    async def theology_proper_detail_pdf(req, resp, *, item_slug):
        """PDF export for Theology Proper topics."""
        await _resource_detail_pdf_response(
            req, resp,
            THEOLOGY_PROPER_DATA["categories"],
            item_slug,
            resource_title="Theology Proper",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # ANTHROPOLOGY - THE DOCTRINE OF MAN
    # ========================================================================
    @api.route("/anthropology")
    async def anthropology_page(req, resp):
        """Anthropology - The Doctrine of Man."""
        _resource_index_response(
            req, resp,
            resource_data=ANTHROPOLOGY_DATA["categories"],
            page_title=ANTHROPOLOGY_DATA["title"],
            page_subtitle=ANTHROPOLOGY_DATA["subtitle"],
            page_description=ANTHROPOLOGY_DATA["introduction"],
            base_url="/anthropology",
            breadcrumb_label="Anthropology",
        )

    @api.route("/anthropology/pdf")
    async def anthropology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            ANTHROPOLOGY_DATA["categories"],
            page_title=ANTHROPOLOGY_DATA["title"],
            page_subtitle=ANTHROPOLOGY_DATA["subtitle"],
            page_description=ANTHROPOLOGY_DATA["introduction"]
        )

    @api.route("/anthropology/{item_slug}")
    async def anthropology_detail(req, resp, *, item_slug):
        """Individual Anthropology topic detail page."""
        _resource_detail_response(
            req, resp,
            ANTHROPOLOGY_DATA["categories"],
            item_slug,
            resource_title="Anthropology",
            back_url="/anthropology",
            back_text="Anthropology",
            not_found_message="Topic not found",
        )

    @api.route("/anthropology/{item_slug}/pdf")
    async def anthropology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Anthropology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            ANTHROPOLOGY_DATA["categories"],
            item_slug,
            resource_title="Anthropology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # HAMARTIOLOGY - THE DOCTRINE OF SIN
    # ========================================================================
    @api.route("/hamartiology")
    async def hamartiology_page(req, resp):
        """Hamartiology - The Doctrine of Sin."""
        _resource_index_response(
            req, resp,
            resource_data=HAMARTIOLOGY_DATA["categories"],
            page_title=HAMARTIOLOGY_DATA["title"],
            page_subtitle=HAMARTIOLOGY_DATA["subtitle"],
            page_description=HAMARTIOLOGY_DATA["introduction"],
            base_url="/hamartiology",
            breadcrumb_label="Hamartiology",
        )

    @api.route("/hamartiology/pdf")
    async def hamartiology_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            HAMARTIOLOGY_DATA["categories"],
            page_title=HAMARTIOLOGY_DATA["title"],
            page_subtitle=HAMARTIOLOGY_DATA["subtitle"],
            page_description=HAMARTIOLOGY_DATA["introduction"]
        )

    @api.route("/hamartiology/{item_slug}")
    async def hamartiology_detail(req, resp, *, item_slug):
        """Individual Hamartiology topic detail page."""
        _resource_detail_response(
            req, resp,
            HAMARTIOLOGY_DATA["categories"],
            item_slug,
            resource_title="Hamartiology",
            back_url="/hamartiology",
            back_text="Hamartiology",
            not_found_message="Topic not found",
        )

    @api.route("/hamartiology/{item_slug}/pdf")
    async def hamartiology_detail_pdf(req, resp, *, item_slug):
        """PDF export for Hamartiology topics."""
        await _resource_detail_pdf_response(
            req, resp,
            HAMARTIOLOGY_DATA["categories"],
            item_slug,
            resource_title="Hamartiology",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # PROVIDENCE - DIVINE PROVIDENCE
    # ========================================================================
    @api.route("/providence")
    async def providence_page(req, resp):
        """Providence - Divine Providence."""
        _resource_index_response(
            req, resp,
            resource_data=PROVIDENCE_DATA["categories"],
            page_title=PROVIDENCE_DATA["title"],
            page_subtitle=PROVIDENCE_DATA["subtitle"],
            page_description=PROVIDENCE_DATA["introduction"],
            base_url="/providence",
            breadcrumb_label="Providence",
        )

    @api.route("/providence/pdf")
    async def providence_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            PROVIDENCE_DATA["categories"],
            page_title=PROVIDENCE_DATA["title"],
            page_subtitle=PROVIDENCE_DATA["subtitle"],
            page_description=PROVIDENCE_DATA["introduction"]
        )

    @api.route("/providence/{item_slug}")
    async def providence_detail(req, resp, *, item_slug):
        """Individual Providence topic detail page."""
        _resource_detail_response(
            req, resp,
            PROVIDENCE_DATA["categories"],
            item_slug,
            resource_title="Providence",
            back_url="/providence",
            back_text="Providence",
            not_found_message="Topic not found",
        )

    @api.route("/providence/{item_slug}/pdf")
    async def providence_detail_pdf(req, resp, *, item_slug):
        """PDF export for Providence topics."""
        await _resource_detail_pdf_response(
            req, resp,
            PROVIDENCE_DATA["categories"],
            item_slug,
            resource_title="Providence",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # GRACE - THE DOCTRINE OF GRACE
    # ========================================================================
    @api.route("/grace")
    async def grace_page(req, resp):
        """Grace - The Doctrine of Grace."""
        _resource_index_response(
            req, resp,
            resource_data=GRACE_DATA["categories"],
            page_title=GRACE_DATA["title"],
            page_subtitle=GRACE_DATA["subtitle"],
            page_description=GRACE_DATA["introduction"],
            base_url="/grace",
            breadcrumb_label="Grace",
        )

    @api.route("/grace/pdf")
    async def grace_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            GRACE_DATA["categories"],
            page_title=GRACE_DATA["title"],
            page_subtitle=GRACE_DATA["subtitle"],
            page_description=GRACE_DATA["introduction"]
        )

    @api.route("/grace/{item_slug}")
    async def grace_detail(req, resp, *, item_slug):
        """Individual Grace topic detail page."""
        _resource_detail_response(
            req, resp,
            GRACE_DATA["categories"],
            item_slug,
            resource_title="Grace",
            back_url="/grace",
            back_text="Grace",
            not_found_message="Topic not found",
        )

    @api.route("/grace/{item_slug}/pdf")
    async def grace_detail_pdf(req, resp, *, item_slug):
        """PDF export for Grace topics."""
        await _resource_detail_pdf_response(
            req, resp,
            GRACE_DATA["categories"],
            item_slug,
            resource_title="Grace",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # JUSTIFICATION - THE DOCTRINE OF JUSTIFICATION
    # ========================================================================
    @api.route("/justification")
    async def justification_page(req, resp):
        """Justification - The Doctrine of Justification."""
        _resource_index_response(
            req, resp,
            resource_data=JUSTIFICATION_DATA["categories"],
            page_title=JUSTIFICATION_DATA["title"],
            page_subtitle=JUSTIFICATION_DATA["subtitle"],
            page_description=JUSTIFICATION_DATA["introduction"],
            base_url="/justification",
            breadcrumb_label="Justification",
        )

    @api.route("/justification/pdf")
    async def justification_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            JUSTIFICATION_DATA["categories"],
            page_title=JUSTIFICATION_DATA["title"],
            page_subtitle=JUSTIFICATION_DATA["subtitle"],
            page_description=JUSTIFICATION_DATA["introduction"]
        )

    @api.route("/justification/{item_slug}")
    async def justification_detail(req, resp, *, item_slug):
        """Individual Justification topic detail page."""
        _resource_detail_response(
            req, resp,
            JUSTIFICATION_DATA["categories"],
            item_slug,
            resource_title="Justification",
            back_url="/justification",
            back_text="Justification",
            not_found_message="Topic not found",
        )

    @api.route("/justification/{item_slug}/pdf")
    async def justification_detail_pdf(req, resp, *, item_slug):
        """PDF export for Justification topics."""
        await _resource_detail_pdf_response(
            req, resp,
            JUSTIFICATION_DATA["categories"],
            item_slug,
            resource_title="Justification",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # SANCTIFICATION - THE DOCTRINE OF SANCTIFICATION
    # ========================================================================
    @api.route("/sanctification")
    async def sanctification_page(req, resp):
        """Sanctification - The Doctrine of Sanctification."""
        _resource_index_response(
            req, resp,
            resource_data=SANCTIFICATION_DATA["categories"],
            page_title=SANCTIFICATION_DATA["title"],
            page_subtitle=SANCTIFICATION_DATA["subtitle"],
            page_description=SANCTIFICATION_DATA["introduction"],
            base_url="/sanctification",
            breadcrumb_label="Sanctification",
        )

    @api.route("/sanctification/pdf")
    async def sanctification_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            SANCTIFICATION_DATA["categories"],
            page_title=SANCTIFICATION_DATA["title"],
            page_subtitle=SANCTIFICATION_DATA["subtitle"],
            page_description=SANCTIFICATION_DATA["introduction"]
        )

    @api.route("/sanctification/{item_slug}")
    async def sanctification_detail(req, resp, *, item_slug):
        """Individual Sanctification topic detail page."""
        _resource_detail_response(
            req, resp,
            SANCTIFICATION_DATA["categories"],
            item_slug,
            resource_title="Sanctification",
            back_url="/sanctification",
            back_text="Sanctification",
            not_found_message="Topic not found",
        )

    @api.route("/sanctification/{item_slug}/pdf")
    async def sanctification_detail_pdf(req, resp, *, item_slug):
        """PDF export for Sanctification topics."""
        await _resource_detail_pdf_response(
            req, resp,
            SANCTIFICATION_DATA["categories"],
            item_slug,
            resource_title="Sanctification",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # LAW AND GOSPEL
    # ========================================================================
    @api.route("/law-and-gospel")
    async def law_and_gospel_page(req, resp):
        """Law and Gospel - The Doctrine of Law and Gospel."""
        _resource_index_response(
            req, resp,
            resource_data=LAW_AND_GOSPEL_DATA["categories"],
            page_title=LAW_AND_GOSPEL_DATA["title"],
            page_subtitle=LAW_AND_GOSPEL_DATA["subtitle"],
            page_description=LAW_AND_GOSPEL_DATA["introduction"],
            base_url="/law-and-gospel",
            breadcrumb_label="Law and Gospel",
        )

    @api.route("/law-and-gospel/pdf")
    async def law_and_gospel_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            LAW_AND_GOSPEL_DATA["categories"],
            page_title=LAW_AND_GOSPEL_DATA["title"],
            page_subtitle=LAW_AND_GOSPEL_DATA["subtitle"],
            page_description=LAW_AND_GOSPEL_DATA["introduction"]
        )

    @api.route("/law-and-gospel/{item_slug}")
    async def law_and_gospel_detail(req, resp, *, item_slug):
        """Individual Law and Gospel topic detail page."""
        _resource_detail_response(
            req, resp,
            LAW_AND_GOSPEL_DATA["categories"],
            item_slug,
            resource_title="Law and Gospel",
            back_url="/law-and-gospel",
            back_text="Law and Gospel",
            not_found_message="Topic not found",
        )

    @api.route("/law-and-gospel/{item_slug}/pdf")
    async def law_and_gospel_detail_pdf(req, resp, *, item_slug):
        """PDF export for Law and Gospel topics."""
        await _resource_detail_pdf_response(
            req, resp,
            LAW_AND_GOSPEL_DATA["categories"],
            item_slug,
            resource_title="Law and Gospel",
            not_found_message="Topic not found",
        )

    # ========================================================================
    # WORSHIP - THE DOCTRINE OF WORSHIP
    # ========================================================================
    @api.route("/worship")
    async def worship_page(req, resp):
        """Worship - The Doctrine of Worship."""
        _resource_index_response(
            req, resp,
            resource_data=WORSHIP_DATA["categories"],
            page_title=WORSHIP_DATA["title"],
            page_subtitle=WORSHIP_DATA["subtitle"],
            page_description=WORSHIP_DATA["introduction"],
            base_url="/worship",
            breadcrumb_label="Worship",
        )

    @api.route("/worship/pdf")
    async def worship_page_pdf(req, resp):
        await _resource_index_pdf_response(
            req, resp,
            WORSHIP_DATA["categories"],
            page_title=WORSHIP_DATA["title"],
            page_subtitle=WORSHIP_DATA["subtitle"],
            page_description=WORSHIP_DATA["introduction"]
        )

    @api.route("/worship/{item_slug}")
    async def worship_detail(req, resp, *, item_slug):
        """Individual Worship topic detail page."""
        _resource_detail_response(
            req, resp,
            WORSHIP_DATA["categories"],
            item_slug,
            resource_title="Worship",
            back_url="/worship",
            back_text="Worship",
            not_found_message="Topic not found",
        )

    @api.route("/worship/{item_slug}/pdf")
    async def worship_detail_pdf(req, resp, *, item_slug):
        """PDF export for Worship topics."""
        await _resource_detail_pdf_response(
            req, resp,
            WORSHIP_DATA["categories"],
            item_slug,
            resource_title="Worship",
            not_found_message="Topic not found",
        )
