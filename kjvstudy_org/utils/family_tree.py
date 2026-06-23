"""Biblical genealogy (GEDCOM) parsing and lookup.

Single source of truth for the family-tree data used by the family-tree pages,
the API, site search, and the name-linking Jinja filter. Parses the bundled
``static/adameve.ged`` once and caches the result.
"""
import re
from pathlib import Path
from typing import List, Dict, Optional

from .helpers import get_verse_text

try:
    from ged4py import GedcomReader
except ImportError:
    GedcomReader = None


def get_static_dir() -> Path:
    """Return the package static directory (where adameve.ged lives)."""
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
    """Hook for name-keyed verses; verses come from GEDCOM notes, so this is empty."""
    return []


def parse_verses_from_notes(note_text: str) -> list:
    """Parse verse references from GEDCOM note text, resolving each to KJV text."""
    verses = []

    # Pattern to match verse references like "Gen 3:15", "1 Sam 2:1-10", etc.
    verse_pattern = r'(?:(\d)\s+)?([A-Z][a-z]+)\s+(\d+):(\d+)(?:-(\d+))?'

    for match in re.finditer(verse_pattern, note_text):
        number = match.group(1) or ""
        book = match.group(2)
        chapter = int(match.group(3))
        start_verse = int(match.group(4))
        end_verse = int(match.group(5)) if match.group(5) else start_verse

        full_book = expand_book_abbreviation(book)
        if number:
            full_book = f"{number} {full_book}"

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
    """Parse a GEDCOM file into our family-tree format (people + generations)."""
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

    # Third pass: calculate siblings (people who share at least one parent)
    for person_id, person in tree_data.items():
        siblings_set = set()
        for parent_id in person["parents"]:
            if parent_id in tree_data:
                for sibling_id in tree_data[parent_id]["children"]:
                    if sibling_id != person_id:
                        siblings_set.add(sibling_id)
        person["siblings"] = list(siblings_set)

    # Calculate generations using BFS from root people (those with no parents)
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

    # Calculate Kekulé (Ahnentafel) numbers working back from Christ
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
                        if i == 0:  # Father = 2n
                            queue.append((parent_id, kekule_num * 2))
                        else:  # Mother = 2n + 1
                            queue.append((parent_id, kekule_num * 2 + 1))

    return tree_data, generations


# Cache for family tree data to avoid reloading on every request
_family_tree_cache = None
_family_tree_generations_cache = None
_name_to_person_id_cache = None


def get_family_tree_data():
    """Load and cache family tree data (returns tree_data and generations)."""
    global _family_tree_cache, _family_tree_generations_cache, _name_to_person_id_cache

    if _family_tree_cache is None:
        gedcom_path = get_static_dir() / "adameve.ged"

        if gedcom_path.exists() and GedcomReader:
            try:
                tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
                _family_tree_cache = tree_data
                _family_tree_generations_cache = generations

                # Build name -> person_id mapping (case-insensitive)
                _name_to_person_id_cache = {}
                for person_id, person in tree_data.items():
                    name = person["name"]
                    _name_to_person_id_cache[name.lower()] = person_id

                    # Handle compound names like "Sarai or Sarah" - store each variant
                    if " or " in name.lower():
                        for variant in (n.strip() for n in name.split(" or ")):
                            if variant:
                                _name_to_person_id_cache[variant.lower()] = person_id

            except Exception:
                _family_tree_cache = {}
                _family_tree_generations_cache = {}
                _name_to_person_id_cache = {}
        else:
            _family_tree_cache = {}
            _family_tree_generations_cache = {}
            _name_to_person_id_cache = {}

    return _family_tree_cache, _family_tree_generations_cache


def get_person_name_mapping():
    """Get the name -> person ID mapping (ensures data is loaded first)."""
    get_family_tree_data()
    return _name_to_person_id_cache


def search_family_tree(query: str, limit: Optional[int] = None) -> List[Dict]:
    """Search the family tree for people whose name matches the query."""
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

        # Exact matches first, then alphabetical
        results.sort(key=lambda x: (
            0 if x["name"].lower() == query_lower else 1,
            x["name"]
        ))

        if limit is not None:
            return results[:limit]
        return results

    except Exception:
        return results
