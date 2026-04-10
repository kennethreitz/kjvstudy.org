"""
Custom template filters for KJV Study.

All filters are registered in register_filters() which should be called with
the MiniJinja environment after templates are initialized.

Available Filters:
    slugify         - Create URL-safe slugs from text
    md              - Convert Markdown to HTML (full block elements)
    mdi             - Convert inline Markdown (no paragraph wrapping)
    link_names      - Link person names to family tree pages
    link_verses     - Link verse references like "John 3:16" to verse pages
    inject_word_markers - Add sidenote markers for word studies
    red_letter      - Wrap words of Christ in red letter spans
    format_lists    - Convert (1), (2) patterns to HTML ordered lists
    split_paragraphs - Split text on double newlines into separate <p> tags
    number_format   - Format numbers with commas (31102 -> 31,102)
    linkify_strongs - Convert Strong's refs (G1234, H5678) to links
"""

import re
import mistune
import minijinja

from functools import lru_cache

from .utils.helpers import create_slug


@lru_cache(maxsize=1)
def _get_person_name_pattern(name_to_id_items=None):
    """Build and cache a single combined regex for all person names.

    Uses lru_cache so the regex is compiled once and reused across all calls.
    Accepts a frozenset of items to make it hashable for caching.
    """
    if name_to_id_items is None:
        return None, {}
    name_to_id = dict(name_to_id_items)
    sorted_names = sorted(name_to_id.keys(), key=len, reverse=True)
    # Build lookup: lowercased name -> person_id
    name_lookup = {name: name_to_id[name] for name in sorted_names}
    # Single alternation pattern, longest-first
    alternatives = '|'.join(re.escape(name) for name in sorted_names)
    pattern = re.compile(r'\b(?:' + alternatives + r')\b', re.IGNORECASE)
    return pattern, name_lookup


# Initialize mistune for markdown rendering
_markdown = mistune.create_markdown(escape=False, hard_wrap=False)
_inline_markdown = mistune.create_markdown(
    renderer=mistune.HTMLRenderer(escape=False),
    plugins=['strikethrough']
)


def markdown_to_html(text):
    """Convert markdown to HTML (bold, italic, paragraphs, etc.)."""
    if not text:
        return text
    return _markdown(text).strip()


def markdown_inline(text):
    """Convert inline markdown to HTML (bold, italic, etc. - no paragraph wrapping)."""
    if not text:
        return text
    html = _inline_markdown(text).strip()
    if html.startswith('<p>') and html.endswith('</p>'):
        html = html[3:-4]
    return html


def link_person_names_in_text(text):
    """
    Automatically link verse references and person names in text.

    Links verse references like "Genesis 1:1" and person names like "Abraham"
    to their respective pages.
    """
    if not text:
        return text

    # First, link verse references
    verse_pattern = r'\b((?:1|2|3)\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def verse_replace_callback(match):
        number_prefix = match.group(1) or ''
        book_name = match.group(2)
        chapter = match.group(3)
        verse_start = match.group(4)
        verse_end = match.group(5)
        matched_text = match.group(0)
        full_book = (number_prefix + book_name).strip()
        if verse_end:
            return f'<a href="/book/{full_book}/chapter/{chapter}#verse-{verse_start}-{verse_end}">{matched_text}</a>'
        return f'<a href="/book/{full_book}/chapter/{chapter}#verse-{verse_start}">{matched_text}</a>'

    text = re.sub(verse_pattern, verse_replace_callback, text)

    # Then, link person names to family tree (lazy import to avoid circular dependency)
    from .server import get_person_name_mapping
    name_to_id = get_person_name_mapping()
    if not name_to_id:
        return text

    # Build a single combined regex for all names (sorted longest-first so
    # "Seth or Sheth" matches before "Seth"). This runs one pass over the text
    # instead of 523 separate re.sub() calls.
    combined_pattern, name_lookup = _get_person_name_pattern(frozenset(name_to_id.items()))

    def replace_callback(match):
        matched_text = match.group(0)
        start_pos = match.start()
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')

        if last_lt > last_gt:
            return matched_text

        if last_lt != -1:
            tag_content = text[last_lt:start_pos]
            if 'href=' in tag_content or 'src=' in tag_content:
                return matched_text

        person_id = name_lookup[matched_text.lower()]
        return f'<a href="/family-tree/person/{person_id}">{matched_text}</a>'

    return combined_pattern.sub(replace_callback, text)


def link_verse_references_in_text(text):
    """Automatically link verse references in text (e.g., 'Genesis 1:1', 'Hebrews 9:22')

    Also handles parenthetical format like 'Daniel (8:16, 9:21)' -> linked refs
    """
    if not text:
        return text

    # First, handle parenthetical format: "Book (chapter:verse, chapter:verse)"
    paren_pattern = r'\b((?:1|2|3)\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+\(([^)]+)\)'

    def replace_paren_refs(match):
        number_prefix = match.group(1) or ''
        book_name = match.group(2)
        refs_str = match.group(3)
        full_book = (number_prefix + book_name).strip()

        # Check if inside HTML tag
        start_pos = match.start()
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')
        if last_lt > last_gt:
            return match.group(0)

        # Parse individual refs like "8:16, 9:21" or "1:19, 1:26"
        ref_parts = [r.strip() for r in refs_str.split(',')]
        linked_refs = []
        for ref in ref_parts:
            # Match chapter:verse or chapter:verse-verse
            ref_match = re.match(r'(\d+):(\d+)(?:-(\d+))?', ref)
            if ref_match:
                chapter = ref_match.group(1)
                verse_start = ref_match.group(2)
                verse_end = ref_match.group(3)
                if verse_end:
                    url = f'/book/{full_book}/chapter/{chapter}#verse-{verse_start}-{verse_end}'
                else:
                    url = f'/book/{full_book}/chapter/{chapter}#verse-{verse_start}'
                linked_refs.append(f'<a href="{url}">{ref}</a>')
            else:
                linked_refs.append(ref)

        return f'{full_book} ({", ".join(linked_refs)})'

    text = re.sub(paren_pattern, replace_paren_refs, text)

    # Then handle standard format: "Book chapter:verse"
    pattern = r'\b((?:1|2|3)\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b'

    def replace_reference(match):
        number_prefix = match.group(1) or ''
        book_name = match.group(2)
        chapter = match.group(3)
        verse_start = match.group(4)
        verse_end = match.group(5)
        full_book = (number_prefix + book_name).strip()
        full_reference = match.group(0)

        start_pos = match.start()
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')

        if last_lt > last_gt:
            return full_reference

        if last_lt != -1:
            tag_content = text[last_lt:start_pos]
            if 'href=' in tag_content or 'src=' in tag_content:
                return full_reference

        if verse_end:
            url = f'/book/{full_book}/chapter/{chapter}#verse-{verse_start}-{verse_end}'
        else:
            url = f'/book/{full_book}/chapter/{chapter}#verse-{verse_start}'
        return f'<a href="{url}">{full_reference}</a>'

    text = re.sub(pattern, replace_reference, text)

    # Finally handle chapter-only format: "Book chapter" (e.g., "Isaiah 53")
    chapter_pattern = r'\b((?:1|2|3)\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+)\b(?!:)'

    def replace_chapter_ref(match):
        number_prefix = match.group(1) or ''
        book_name = match.group(2)
        chapter = match.group(3)
        full_book = (number_prefix + book_name).strip()
        full_reference = match.group(0)

        start_pos = match.start()
        text_before = text[:start_pos]
        last_lt = text_before.rfind('<')
        last_gt = text_before.rfind('>')

        if last_lt > last_gt:
            return full_reference

        if last_lt != -1:
            tag_content = text[last_lt:start_pos]
            if 'href=' in tag_content or 'src=' in tag_content:
                return full_reference

        url = f'/book/{full_book}/chapter/{chapter}'
        return f'<a href="{url}">{full_reference}</a>'

    return re.sub(chapter_pattern, replace_chapter_ref, text)


def inject_word_markers(text, word_studies, verse_num, auto_expand=False):
    """Inject sidenote markers into verse text next to annotated words.

    Word studies are collapsed by default, showing only the word and Greek/Hebrew term.
    Clicking expands to show transliteration and full definition.
    If auto_expand is True (global) or study has 'auto_expand': True, show expanded.
    """
    if not word_studies:
        return text

    for idx, study in enumerate(word_studies, 1):
        # Per-study auto_expand takes precedence, then fall back to global
        study_expand = study.get('auto_expand', auto_expand)
        expanded_class = ' expanded' if study_expand else ''
        word = study['word']
        # Link the original term to Strong's page if we have a Strong's number
        strongs = study.get('strongs')
        if strongs:
            term_html = f'<a href="/strongs/{strongs}">{study["term"]}</a>'
        else:
            term_html = study["term"]
        # Wrap details (translit + note) in a span that's hidden by default
        marker = (
            f'<label for="sn-{verse_num}-word-{idx}" class="margin-toggle sidenote-number"></label>'
            f'<input type="checkbox" id="sn-{verse_num}-word-{idx}" class="margin-toggle"/>'
            f'<span class="sidenote word-study{expanded_class}">'
            f'<strong>{word}:</strong> {term_html}'
            f'<span class="word-study-details"> (<em>{study["translit"]}</em>). {study["note"]}</span>'
            f'</span>'
        )
        pattern = re.compile(r'\b(' + re.escape(word) + r')(?!\'[sS])\b', re.IGNORECASE)
        text = pattern.sub(r'\1' + marker, text, count=1)

    return text


def red_letter(text, book, chapter, verse_num):
    """Wrap the words of Christ in red letter span tags"""
    from .red_letter import wrap_red_letter_text
    return wrap_red_letter_text(text, book, chapter, verse_num)


def format_numbered_lists(text):
    """Convert (1), (2), etc. patterns into HTML ordered lists"""
    def _convert(pattern: str, payload: str) -> str:
        markers = list(re.finditer(pattern, payload))
        if len(markers) < 2:
            return payload

        numbers = [int(m.group(1)) for m in markers]
        if numbers[0] != 1:
            return payload

        seq_length = 1
        for i in range(1, len(numbers)):
            if numbers[i] == seq_length + 1:
                seq_length += 1
            else:
                break

        if seq_length < 2:
            return payload

        markers = markers[:seq_length]
        list_items = []
        for i, marker in enumerate(markers):
            start = marker.end()

            if i + 1 < len(markers):
                end = markers[i + 1].start()
            else:
                remaining = payload[start:]
                end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining)
                end = start + end_match.start() + 1 if end_match else len(payload)

            item_text = payload[start:end].strip().rstrip(';,')
            if item_text.endswith(' and'):
                item_text = item_text[:-4]
            list_items.append(f'<li>{item_text}</li>')

        html_list = '<ol>' + ''.join(list_items) + '</ol>'
        list_start = markers[0].start()
        last_marker = markers[-1]
        last_item_start = last_marker.end()
        remaining_after_last = payload[last_item_start:]
        end_match = re.search(r'[.;]\s+(?=[A-Z])|$', remaining_after_last)
        list_end = last_item_start + end_match.start() + 1 if end_match else len(payload)

        after_list = payload[list_end:].strip()
        if after_list:
            return payload[:list_start] + html_list + '</p><p>' + after_list
        return payload[:list_start] + html_list

    primary_pattern = r'\((\d+)\)\s*'
    converted = _convert(primary_pattern, text)
    if converted != text:
        return converted

    fallback_pattern = r'(?<=\s)(\d+)\)\s*'
    return _convert(fallback_pattern, text)


def split_paragraphs(text):
    """Convert double newlines or <br><br> into separate <p> tags for better navigation"""
    if not text:
        return text
    parts = re.split(r'\n\n|<br\s*/?>\s*<br\s*/?>', text)
    paragraphs = [f'<p>{p.strip()}</p>' for p in parts if p.strip()]
    return '\n'.join(paragraphs)


def number_format(value):
    """Format a number with commas (e.g., 31102 -> 31,102)"""
    return f"{value:,}"


def linkify_strongs(text):
    """Convert Strong's references like G1234 or H5678 to links.

    Handles leading zeros in numbers (H04566 -> H4566).
    """
    if not text:
        return text
    pattern = r'\b([GH])(\d+)\b'
    def replace(match):
        prefix = match.group(1)
        num = str(int(match.group(2)))  # Strip leading zeros
        return f'<a href="/strongs/{prefix}{num}" class="strongs-ref">{prefix}{num}</a>'
    return re.sub(pattern, replace, text)


def strip_links(text):
    """Strip HTML anchor tags, keeping only the link text.

    Useful for PDF output where links are not clickable.
    """
    if not text:
        return text
    # Replace <a href="...">text</a> with just text
    return re.sub(r'<a\s+[^>]*>([^<]*)</a>', r'\1', text)


def _safe_html(func):
    """Wrap a filter function so its return value is marked as safe HTML."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return result
        return minijinja.safe(str(result))
    return wrapper


def rsplit(text, sep=' ', maxsplit=-1):
    """Python rsplit as a template filter, since MiniJinja lacks it."""
    if not text:
        return []
    return text.rsplit(sep, maxsplit)


def register_filters(env):
    """Register all custom filters with a MiniJinja environment."""
    env.add_filter('slugify', create_slug)
    env.add_filter('md', _safe_html(markdown_to_html))
    env.add_filter('mdi', _safe_html(markdown_inline))
    env.add_filter('link_names', _safe_html(link_person_names_in_text))
    env.add_filter('link_verses', _safe_html(link_verse_references_in_text))
    env.add_filter('inject_word_markers', _safe_html(inject_word_markers))
    env.add_filter('red_letter', _safe_html(red_letter))
    env.add_filter('format_lists', _safe_html(format_numbered_lists))
    env.add_filter('split_paragraphs', _safe_html(split_paragraphs))
    env.add_filter('number_format', number_format)
    env.add_filter('linkify_strongs', _safe_html(linkify_strongs))
    env.add_filter('strip_links', strip_links)
    env.add_filter('rsplit', rsplit)
