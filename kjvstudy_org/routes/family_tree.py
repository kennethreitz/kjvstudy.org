"""Family tree routes for biblical genealogy.

This module handles all family tree related routes including:
- Main family tree page
- Generation pages
- Individual person pages
- Search functionality
- Ancestors/descendants views
- SVG lineage visualization
"""
from pathlib import Path
from typing import List, Dict, Optional

from turboapi import APIRouter, Request, HTTPException, Query
from turboapi import HTMLResponse, RedirectResponse, Response

from ..utils.helpers import get_verse_text

try:
    from ged4py import GedcomReader
except ImportError:
    GedcomReader = None

router = APIRouter(tags=["Family Tree"])

# Templates will be set by the main app
templates = None

# Module-level cache
_family_tree_cache = None
_family_tree_generations_cache = None
_name_to_person_id_cache = None


def init_templates(app_templates):
    """Initialize templates from the main app."""
    global templates
    templates = app_templates


def get_books():
    """Get list of Bible books."""
    from ..kjv import bible
    return bible.get_books()


def get_static_dir():
    """Get the static directory path."""
    return Path(__file__).parent.parent / "static"


def expand_book_abbreviation(abbrev):
    """Expand common Bible book abbreviations to full names."""
    abbreviations = {
        "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy",
        "Josh": "Joshua", "Judg": "Judges", "1 Sam": "1 Samuel", "2 Sam": "2 Samuel",
        "1 Kgs": "1 Kings", "2 Kgs": "2 Kings", "1 Chr": "1 Chronicles", "2 Chr": "2 Chronicles",
        "Neh": "Nehemiah", "Esth": "Esther", "Ps": "Psalms", "Prov": "Proverbs",
        "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah", "Jer": "Jeremiah",
        "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
        "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah", "Mic": "Micah",
        "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai",
        "Zech": "Zechariah", "Mal": "Malachi",
        "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
        "Rom": "Romans", "1 Cor": "1 Corinthians", "2 Cor": "2 Corinthians",
        "Gal": "Galatians", "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians",
        "1 Thess": "1 Thessalonians", "2 Thess": "2 Thessalonians",
        "1 Tim": "1 Timothy", "2 Tim": "2 Timothy", "Titus": "Titus", "Phlm": "Philemon",
        "Heb": "Hebrews", "Jas": "James", "1 Pet": "1 Peter", "2 Pet": "2 Peter",
        "1 John": "1 John", "2 John": "2 John", "3 John": "3 John", "Jude": "Jude",
        "Rev": "Revelation"
    }
    return abbreviations.get(abbrev, abbrev)


def get_biblical_verses(name: str) -> list:
    """Get biblical verses related to a person by name."""
    return []


def parse_verses_from_notes(note_text: str) -> list:
    """Parse verse references from GEDCOM note text."""
    import re
    verses = []

    # Pattern to match verse references like "Gen 3:15", "1 Sam 2:1-10", etc.
    verse_pattern = r'(?:(\d)\s+)?([A-Z][a-z]+)\s+(\d+):(\d+)(?:-(\d+))?'

    for match in re.finditer(verse_pattern, note_text):
        number = match.group(1) or ""
        book = match.group(2)
        chapter = int(match.group(3))
        start_verse = int(match.group(4))
        end_verse = int(match.group(5)) if match.group(5) else start_verse

        # Expand abbreviation to full book name
        full_book = expand_book_abbreviation(book)
        if number:
            full_book = f"{number} {full_book}"

        # Create reference string
        if start_verse == end_verse:
            reference = f"{full_book} {chapter}:{start_verse}"
        else:
            reference = f"{full_book} {chapter}:{start_verse}-{end_verse}"

        verse_text = get_verse_text(full_book, chapter, start_verse) or ""

        verses.append({
            "reference": reference,
            "text": verse_text
        })

    return verses


def parse_gedcom_to_tree_data(gedcom_path):
    """Parse GEDCOM file into family tree format."""
    tree_data = {}

    gedcom = GedcomReader(str(gedcom_path))

    # First pass: collect all individuals
    for record in gedcom.records0():
        if record.tag == 'INDI':
            person_id = str(record.xref_id).replace('@', '').replace('#', '').lower()

            name = "Unknown"
            title = "Biblical Figure"
            for sub in record.sub_records:
                if sub.tag == 'NAME':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    name_value = str(value).replace('/', '').strip()
                    name = ' '.join(name_value.split())
                    break

            for sub in record.sub_records:
                if sub.tag == 'OCCU':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    title = str(value)
                    break

            description = f"Biblical figure from {name}'s genealogy"
            note_verses = []
            for sub in record.sub_records:
                if sub.tag == 'NOTE':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    note_text = str(value)
                    description = note_text
                    note_verses = parse_verses_from_notes(note_text)
                    break

            birth_year = "Unknown"
            death_year = "Unknown"
            age_at_death = "Unknown"

            for sub in record.sub_records:
                if sub.tag == 'BIRT':
                    for date_sub in sub.sub_records:
                        if date_sub.tag == 'DATE':
                            value = date_sub.value[0] if isinstance(date_sub.value, tuple) else date_sub.value
                            birth_year = str(value)
                elif sub.tag == 'DEAT':
                    for date_sub in sub.sub_records:
                        if date_sub.tag == 'DATE':
                            value = date_sub.value[0] if isinstance(date_sub.value, tuple) else date_sub.value
                            death_year = str(value)

            if birth_year != "Unknown" and death_year != "Unknown":
                try:
                    birth_num = int(birth_year.split()[0]) if birth_year.split() else 0
                    death_num = int(death_year.split()[0]) if death_year.split() else 0
                    if death_num > birth_num:
                        age_at_death = f"{death_num - birth_num} years"
                except (ValueError, IndexError):
                    pass

            manual_verses = get_biblical_verses(name)
            all_verses = note_verses if note_verses else manual_verses

            person_data = {
                "name": name,
                "title": title,
                "description": description,
                "children": [],
                "parents": [],
                "siblings": [],
                "spouse": None,
                "verses": all_verses,
                "birth_year": birth_year,
                "death_year": death_year,
                "age_at_death": age_at_death
            }

            tree_data[person_id] = person_data

    # Second pass: collect family relationships
    for record in gedcom.records0():
        if record.tag == 'FAM':
            husband_id = None
            wife_id = None
            children = []

            for sub in record.sub_records:
                if sub.tag == 'HUSB':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    husband_id = str(value).replace('@', '').replace('#', '').lower()
                elif sub.tag == 'WIFE':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    wife_id = str(value).replace('@', '').replace('#', '').lower()
                elif sub.tag == 'CHIL':
                    value = sub.value[0] if isinstance(sub.value, tuple) else sub.value
                    child_id = str(value).replace('@', '').replace('#', '').lower()
                    children.append(child_id)

            if husband_id and husband_id in tree_data and wife_id and wife_id in tree_data:
                tree_data[husband_id]["spouse"] = tree_data[wife_id]["name"]
                tree_data[wife_id]["spouse"] = tree_data[husband_id]["name"]

            for child_id in children:
                if child_id in tree_data:
                    if husband_id and husband_id in tree_data:
                        tree_data[husband_id]["children"].append(child_id)
                        if husband_id not in tree_data[child_id]["parents"]:
                            tree_data[child_id]["parents"].append(husband_id)
                    if wife_id and wife_id in tree_data:
                        tree_data[wife_id]["children"].append(child_id)
                        if wife_id not in tree_data[child_id]["parents"]:
                            tree_data[child_id]["parents"].append(wife_id)

    # Third pass: calculate siblings
    for person_id, person in tree_data.items():
        siblings_set = set()
        for parent_id in person["parents"]:
            if parent_id in tree_data:
                for sibling_id in tree_data[parent_id]["children"]:
                    if sibling_id != person_id:
                        siblings_set.add(sibling_id)
        person["siblings"] = list(siblings_set)

    # Calculate generations using BFS
    generations = {}
    for person_id, person in tree_data.items():
        person["generation"] = None

    roots = [pid for pid, person in tree_data.items() if len(person["parents"]) == 0]
    queue = [(pid, 1) for pid in roots]
    visited = set()

    while queue:
        person_id, gen_num = queue.pop(0)
        if person_id in visited:
            continue
        visited.add(person_id)

        if person_id in tree_data:
            tree_data[person_id]["generation"] = gen_num
            if gen_num not in generations:
                generations[gen_num] = []
            generations[gen_num].append(person_id)

            for child_id in tree_data[person_id]["children"]:
                if child_id not in visited:
                    queue.append((child_id, gen_num + 1))

    # Calculate Kekulé numbers from Christ
    jesus_id = None
    for person_id, person in tree_data.items():
        if person["name"].lower() in ["jesus", "jesus christ", "christ"]:
            jesus_id = person_id
            break

    for person_id, person in tree_data.items():
        person["kekule_number"] = None

    if jesus_id:
        queue = [(jesus_id, 1)]
        visited_reverse = set()

        while queue:
            person_id, kekule_num = queue.pop(0)
            if person_id in visited_reverse:
                continue
            visited_reverse.add(person_id)

            if person_id in tree_data:
                tree_data[person_id]["kekule_number"] = kekule_num
                parents = tree_data[person_id]["parents"]

                for i, parent_id in enumerate(parents):
                    if parent_id not in visited_reverse:
                        if i == 0:  # Father
                            queue.append((parent_id, kekule_num * 2))
                        else:  # Mother
                            queue.append((parent_id, kekule_num * 2 + 1))

    return tree_data, generations


def get_family_tree_data():
    """Load and cache family tree data."""
    global _family_tree_cache, _family_tree_generations_cache, _name_to_person_id_cache

    if _family_tree_cache is None:
        gedcom_path = get_static_dir() / "adameve.ged"

        if gedcom_path.exists() and GedcomReader:
            try:
                tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
                _family_tree_cache = tree_data
                _family_tree_generations_cache = generations

                _name_to_person_id_cache = {}
                for person_id, person in tree_data.items():
                    _name_to_person_id_cache[person["name"].lower()] = person_id

            except Exception:
                _family_tree_cache = {}
                _family_tree_generations_cache = {}
                _name_to_person_id_cache = {}
        else:
            _family_tree_cache = {}
            _family_tree_generations_cache = {}
            _name_to_person_id_cache = {}

    return _family_tree_cache, _family_tree_generations_cache


def search_family_tree(query: str, limit: Optional[int] = None) -> List[Dict]:
    """Search family tree for people matching the query."""
    results = []
    if not query or len(query.strip()) < 2:
        return results

    try:
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            return results

        query_lower = query.lower().strip()
        for person_id, person in family_tree_data.items():
            if query_lower in person["name"].lower():
                results.append({
                    "type": "person",
                    "id": person_id,
                    "name": person["name"],
                    "generation": person.get("generation"),
                    "birth_year": person.get("birth_year", "Unknown"),
                    "death_year": person.get("death_year", "Unknown"),
                    "url": f"/family-tree/person/{person_id}",
                    "description": f"Generation {person.get('generation', '?')} from Adam"
                })

        results.sort(key=lambda x: (
            0 if x["name"].lower() == query_lower else 1,
            x["name"]
        ))

        if limit is not None:
            return results[:limit]
        return results

    except Exception:
        return results


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/family-tree", response_class=HTMLResponse)
async def family_tree_page(request: Request):
    """Biblical family tree page using GEDCOM file."""
    family_tree_data, generations = get_family_tree_data()

    if not family_tree_data:
        raise HTTPException(
            status_code=500,
            detail="Family tree data not available"
        )

    return templates.TemplateResponse(
            request,
            "family_tree.html",
            {
            "books": get_books(),
            "family_tree_data": family_tree_data,
            "generations": generations,
            "person_names": sorted(
                {
                    person["name"].strip()
                    for person in family_tree_data.values()
                    if person.get("name")
                },
                key=lambda name: name.lower()
            ),
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": None}
            ]
        }
    )


@router.get("/family-tree/generation/{gen_num}", response_class=HTMLResponse)
async def family_tree_generation_page(request: Request, gen_num: int):
    """Individual generation page."""
    gedcom_path = get_static_dir() / "adameve.ged"

    if not gedcom_path.exists():
        raise HTTPException(
            status_code=404,
            detail="GEDCOM file not found."
        )

    if not GedcomReader:
        raise HTTPException(
            status_code=500,
            detail="GEDCOM parser not available."
        )

    try:
        family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse GEDCOM file: {str(e)}"
        )

    generation_people = generations.get(gen_num, [])

    if not generation_people:
        raise HTTPException(
            status_code=404,
            detail=f"Generation {gen_num} not found"
        )

    return templates.TemplateResponse(
            request,
            "family_tree_generation.html",
            {
            "books": get_books(),
            "family_tree_data": family_tree_data,
            "generation_num": gen_num,
            "generation_people": generation_people,
            "generations": generations,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": f"Generation {gen_num}", "url": None}
            ]
        }
    )


@router.get("/family-tree/person/{person_id}", response_class=HTMLResponse)
async def family_tree_person_page(request: Request, person_id: str):
    """Individual person page."""
    from ..biblical_biographies import get_biography

    gedcom_path = get_static_dir() / "adameve.ged"

    if not gedcom_path.exists():
        raise HTTPException(
            status_code=404,
            detail="GEDCOM file not found."
        )

    if not GedcomReader:
        raise HTTPException(
            status_code=500,
            detail="GEDCOM parser not available."
        )

    try:
        family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse GEDCOM file: {str(e)}"
        )

    person_id_lower = person_id.lower()
    if person_id_lower not in family_tree_data:
        raise HTTPException(
            status_code=404,
            detail=f"Person '{person_id}' not found"
        )

    person = family_tree_data[person_id_lower]
    biography = get_biography(person["name"])

    return templates.TemplateResponse(
            request,
            "family_tree_person.html",
            {
            "books": get_books(),
            "person": person,
            "person_id": person_id_lower,
            "family_tree_data": family_tree_data,
            "generations": generations,
            "biography": biography,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": None}
            ]
        }
    )


@router.get("/family-tree/search", response_class=HTMLResponse)
async def family_tree_search_page(request: Request, q: str = ""):
    """Search the family tree."""
    gedcom_path = get_static_dir() / "adameve.ged"

    if not gedcom_path.exists():
        raise HTTPException(
            status_code=404,
            detail="GEDCOM file not found."
        )

    if not GedcomReader:
        raise HTTPException(
            status_code=500,
            detail="GEDCOM parser not available."
        )

    try:
        family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse GEDCOM file: {str(e)}"
        )

    all_names = sorted([person["name"] for person in family_tree_data.values()])

    results = []
    exact_match_id = None
    if q:
        query_lower = q.lower()
        for person_id, person in family_tree_data.items():
            if query_lower in person["name"].lower():
                results.append({
                    "id": person_id,
                    "name": person["name"],
                    "generation": person.get("generation"),
                    "birth_year": person.get("birth_year", "Unknown"),
                    "death_year": person.get("death_year", "Unknown")
                })
                if person["name"].lower() == query_lower:
                    exact_match_id = person_id

    if exact_match_id:
        return RedirectResponse(url=f"/family-tree/person/{exact_match_id}", status_code=303)

    return templates.TemplateResponse(
            request,
            "family_tree_search.html",
            {
            "books": get_books(),
            "query": q,
            "results": results,
            "all_names": all_names,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Search", "url": None}
            ]
        }
    )


@router.get("/family-tree/interactive", response_class=HTMLResponse)
async def family_tree_interactive_page(request: Request):
    """Interactive D3.js-based family tree visualization."""
    family_tree_data, generations = get_family_tree_data()

    if not family_tree_data:
        raise HTTPException(
            status_code=500,
            detail="Family tree data not available"
        )

    return templates.TemplateResponse(
            request,
            "family_tree_interactive.html",
            {
            "books": get_books(),
            "family_tree_data": family_tree_data,
            "generations": generations,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Interactive Tree", "url": None}
            ]
        }
    )


@router.get("/family-tree/lineage", response_class=HTMLResponse)
async def family_tree_lineage_page(request: Request):
    """Dedicated page for the Messianic lineage visualization."""
    return templates.TemplateResponse(
            request,
            "family_tree_lineage.html",
            {
            "books": get_books(),
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Messianic Lineage", "url": None}
            ]
        }
    )


@router.get("/family-tree/person/{person_id}/descendants", response_class=HTMLResponse)
async def family_tree_descendants_page(request: Request, person_id: str):
    """View all descendants of a person."""
    family_tree_data, generations = get_family_tree_data()

    if not family_tree_data:
        raise HTTPException(status_code=500, detail="Family tree data not available")

    person_id_lower = person_id.lower()
    if person_id_lower not in family_tree_data:
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")

    person = family_tree_data[person_id_lower]

    def get_descendants_tree(pid, max_depth=10):
        if max_depth <= 0:
            return None

        person_data = family_tree_data.get(pid)
        if not person_data:
            return None

        children = []
        for child_id in person_data.get("children", []):
            child_tree = get_descendants_tree(child_id, max_depth - 1)
            if child_tree:
                children.append(child_tree)

        return {
            "id": pid,
            "name": person_data["name"],
            "generation": person_data.get("generation"),
            "kekule_number": person_data.get("kekule_number"),
            "children": children,
            "child_count": len(person_data.get("children", []))
        }

    descendants_tree = get_descendants_tree(person_id_lower)

    return templates.TemplateResponse(
            request,
            "family_tree_descendants.html",
            {
            "books": get_books(),
            "person": person,
            "person_id": person_id_lower,
            "descendants_tree": descendants_tree,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": f"/family-tree/person/{person_id_lower}"},
                {"text": "Descendants", "url": None}
            ]
        }
    )


@router.get("/family-tree/person/{person_id}/ancestors", response_class=HTMLResponse)
async def family_tree_ancestors_page(request: Request, person_id: str):
    """View all ancestors of a person."""
    family_tree_data, generations = get_family_tree_data()

    if not family_tree_data:
        raise HTTPException(status_code=500, detail="Family tree data not available")

    person_id_lower = person_id.lower()
    if person_id_lower not in family_tree_data:
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")

    person = family_tree_data[person_id_lower]

    def get_ancestors_tree(pid, max_depth=20):
        if max_depth <= 0:
            return None

        person_data = family_tree_data.get(pid)
        if not person_data:
            return None

        parents = []
        for parent_id in person_data.get("parents", []):
            parent_tree = get_ancestors_tree(parent_id, max_depth - 1)
            if parent_tree:
                parents.append(parent_tree)

        return {
            "id": pid,
            "name": person_data["name"],
            "generation": person_data.get("generation"),
            "kekule_number": person_data.get("kekule_number"),
            "parents": parents,
            "parent_count": len(person_data.get("parents", []))
        }

    ancestors_tree = get_ancestors_tree(person_id_lower)

    return templates.TemplateResponse(
            request,
            "family_tree_ancestors.html",
            {
            "books": get_books(),
            "person": person,
            "person_id": person_id_lower,
            "ancestors_tree": ancestors_tree,
            "breadcrumbs": [
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": f"/family-tree/person/{person_id_lower}"},
                {"text": "Ancestors", "url": None}
            ]
        }
    )


@router.get("/family-tree/lineage.svg")
async def family_tree_lineage_svg(request: Request):
    """Generate SVG visualization of the Messianic lineage (Adam to Jesus)."""
    gedcom_path = get_static_dir() / "adameve.ged"

    if not gedcom_path.exists() or not GedcomReader:
        raise HTTPException(status_code=404, detail="Family tree data not available")

    try:
        family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse family tree: {str(e)}")

    # Find all people in direct paternal line (Kekulé powers of 2)
    lineage = []

    for person_id, person in family_tree_data.items():
        kekule = person.get("kekule_number")
        if kekule and kekule > 0:
            # Check if kekule is a power of 2
            if kekule & (kekule - 1) == 0:
                lineage.append({
                    "id": person_id,
                    "name": person["name"],
                    "kekule": kekule,
                    "generation": person.get("generation", 0),
                    "birth_year": person.get("birth_year", "Unknown"),
                    "death_year": person.get("death_year", "Unknown")
                })

    lineage.sort(key=lambda x: -x["kekule"])

    # Generate SVG
    width = 800
    node_height = 80
    node_width = 700
    margin_top = 40
    margin_bottom = 40
    vertical_spacing = 20

    height = margin_top + (len(lineage) * (node_height + vertical_spacing)) + margin_bottom

    svg_parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<style>',
        '.person-box { fill: #f9f9f9; stroke: #333; stroke-width: 1.5; }',
        '.person-box:hover { fill: #f0f8ff; stroke: #0066cc; }',
        '.person-name { font-family: "ETBembo", Palatino, "Book Antiqua", serif; font-size: 18px; font-weight: 600; fill: #111; }',
        '.person-dates { font-family: "ETBembo", Palatino, "Book Antiqua", serif; font-size: 14px; fill: #666; }',
        '.person-meta { font-family: "ETBembo", Palatino, "Book Antiqua", serif; font-size: 12px; fill: #999; }',
        '.connector-line { stroke: #999; stroke-width: 2; fill: none; }',
        '</style>',
        '</defs>',
    ]

    x = (width - node_width) / 2

    # Draw connector lines
    for i in range(len(lineage) - 1):
        y1 = margin_top + (i * (node_height + vertical_spacing)) + node_height
        y2 = margin_top + ((i + 1) * (node_height + vertical_spacing))
        mid_x = x + (node_width / 2)
        svg_parts.append(f'<line class="connector-line" x1="{mid_x}" y1="{y1}" x2="{mid_x}" y2="{y2}" />')

    # Draw person boxes
    for i, person in enumerate(lineage):
        y = margin_top + (i * (node_height + vertical_spacing))

        svg_parts.append(f'<a href="/family-tree/person/{person["id"]}">')
        svg_parts.append(f'<rect class="person-box" x="{x}" y="{y}" width="{node_width}" height="{node_height}" rx="4" />')

        name_y = y + 28
        svg_parts.append(f'<text class="person-name" x="{x + node_width/2}" y="{name_y}" text-anchor="middle">{person["name"]}</text>')

        dates_text = ""
        if person["birth_year"] != "Unknown" and person["death_year"] != "Unknown":
            dates_text = f'{person["birth_year"]} – {person["death_year"]}'
        elif person["birth_year"] != "Unknown":
            dates_text = f'Born {person["birth_year"]}'
        elif person["death_year"] != "Unknown":
            dates_text = f'Died {person["death_year"]}'

        if dates_text:
            dates_y = y + 48
            svg_parts.append(f'<text class="person-dates" x="{x + node_width/2}" y="{dates_y}" text-anchor="middle">{dates_text}</text>')

        meta_text = f'Generation {person["generation"]}'
        if person["kekule"] > 1:
            meta_text += f' • Kekulé #{person["kekule"]}'
        meta_y = y + 66
        svg_parts.append(f'<text class="person-meta" x="{x + node_width/2}" y="{meta_y}" text-anchor="middle">{meta_text}</text>')

        svg_parts.append('</a>')

    svg_parts.append('</svg>')

    svg_content = '\n'.join(svg_parts)
    return Response(content=svg_content, media_type="image/svg+xml")
