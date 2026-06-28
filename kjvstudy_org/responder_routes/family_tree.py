"""Family tree routes for biblical genealogy. (Responder port of routes/family_tree.py)

This module handles all family tree related routes including:
- Main family tree page
- Generation pages
- Individual person pages
- Search functionality
- Ancestors/descendants views
- SVG lineage visualization
"""
from ..utils.family_tree import (
    get_static_dir,
    parse_gedcom_to_tree_data,
    get_family_tree_data,
)

try:
    from ged4py import GedcomReader
except ImportError:
    GedcomReader = None

from ..utils.helpers import get_books
from ._helpers import render, redirect, abort_404


# ============================================================================
# ROUTES
# ============================================================================

def register(api):
    @api.route("/family-tree")
    async def family_tree_page(req, resp):
        """Biblical family tree page using GEDCOM file."""
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            resp.status_code = 500
            resp.media = {"detail": "Family tree data not available"}
            return

        render(
            req, resp, "family_tree.html",
            books=get_books(),
            family_tree_data=family_tree_data,
            generations=generations,
            person_names=sorted(
                {
                    person["name"].strip()
                    for person in family_tree_data.values()
                    if person.get("name")
                },
                key=lambda name: name.lower()
            ),
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": None}
            ],
        )

    @api.route("/family-tree/generation/{gen_num:int}")
    async def family_tree_generation_page(req, resp, *, gen_num):
        """Individual generation page."""
        gedcom_path = get_static_dir() / "adameve.ged"

        if not gedcom_path.exists():
            abort_404(req, resp, "GEDCOM file not found.")
            return

        if not GedcomReader:
            resp.status_code = 500
            resp.media = {"detail": "GEDCOM parser not available."}
            return

        try:
            family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
        except Exception as e:
            resp.status_code = 500
            resp.media = {"detail": f"Failed to parse GEDCOM file: {str(e)}"}
            return

        generation_people = generations.get(gen_num, [])

        if not generation_people:
            abort_404(req, resp, f"Generation {gen_num} not found")
            return

        render(
            req, resp, "family_tree_generation.html",
            books=get_books(),
            family_tree_data=family_tree_data,
            generation_num=gen_num,
            generation_people=generation_people,
            generations=generations,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": f"Generation {gen_num}", "url": None}
            ],
        )

    @api.route("/family-tree/person/{person_id}")
    async def family_tree_person_page(req, resp, *, person_id):
        """Individual person page."""
        from ..biblical_biographies import get_biography

        gedcom_path = get_static_dir() / "adameve.ged"

        if not gedcom_path.exists():
            abort_404(req, resp, "GEDCOM file not found.")
            return

        if not GedcomReader:
            resp.status_code = 500
            resp.media = {"detail": "GEDCOM parser not available."}
            return

        try:
            family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
        except Exception as e:
            resp.status_code = 500
            resp.media = {"detail": f"Failed to parse GEDCOM file: {str(e)}"}
            return

        person_id_lower = person_id.lower()
        if person_id_lower not in family_tree_data:
            abort_404(req, resp, f"Person '{person_id}' not found")
            return

        person = family_tree_data[person_id_lower]
        biography = get_biography(person["name"])

        render(
            req, resp, "family_tree_person.html",
            books=get_books(),
            person=person,
            person_id=person_id_lower,
            family_tree_data=family_tree_data,
            generations=generations,
            biography=biography,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": None}
            ],
        )

    @api.route("/family-tree/search")
    async def family_tree_search_page(req, resp):
        """Search the family tree."""
        q = req.params.get("q", "")

        gedcom_path = get_static_dir() / "adameve.ged"

        if not gedcom_path.exists():
            abort_404(req, resp, "GEDCOM file not found.")
            return

        if not GedcomReader:
            resp.status_code = 500
            resp.media = {"detail": "GEDCOM parser not available."}
            return

        try:
            family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
        except Exception as e:
            resp.status_code = 500
            resp.media = {"detail": f"Failed to parse GEDCOM file: {str(e)}"}
            return

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
            redirect(resp, f"/family-tree/person/{exact_match_id}", 303)
            return

        render(
            req, resp, "family_tree_search.html",
            books=get_books(),
            query=q,
            results=results,
            all_names=all_names,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Search", "url": None}
            ],
        )

    @api.route("/family-tree/interactive")
    async def family_tree_interactive_page(req, resp):
        """Interactive D3.js-based family tree visualization."""
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            resp.status_code = 500
            resp.media = {"detail": "Family tree data not available"}
            return

        render(
            req, resp, "family_tree_interactive.html",
            books=get_books(),
            family_tree_data=family_tree_data,
            generations=generations,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Interactive Tree", "url": None}
            ],
        )

    @api.route("/family-tree/lineage")
    async def family_tree_lineage_page(req, resp):
        """Dedicated page for the Messianic lineage visualization."""
        render(
            req, resp, "family_tree_lineage.html",
            books=get_books(),
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": "Messianic Lineage", "url": None}
            ],
        )

    @api.route("/family-tree/person/{person_id}/descendants")
    async def family_tree_descendants_page(req, resp, *, person_id):
        """View all descendants of a person."""
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            resp.status_code = 500
            resp.media = {"detail": "Family tree data not available"}
            return

        person_id_lower = person_id.lower()
        if person_id_lower not in family_tree_data:
            abort_404(req, resp, f"Person '{person_id}' not found")
            return

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

        render(
            req, resp, "family_tree_descendants.html",
            books=get_books(),
            person=person,
            person_id=person_id_lower,
            descendants_tree=descendants_tree,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": f"/family-tree/person/{person_id_lower}"},
                {"text": "Descendants", "url": None}
            ],
        )

    @api.route("/family-tree/person/{person_id}/ancestors")
    async def family_tree_ancestors_page(req, resp, *, person_id):
        """View all ancestors of a person."""
        family_tree_data, generations = get_family_tree_data()

        if not family_tree_data:
            resp.status_code = 500
            resp.media = {"detail": "Family tree data not available"}
            return

        person_id_lower = person_id.lower()
        if person_id_lower not in family_tree_data:
            abort_404(req, resp, f"Person '{person_id}' not found")
            return

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

        render(
            req, resp, "family_tree_ancestors.html",
            books=get_books(),
            person=person,
            person_id=person_id_lower,
            ancestors_tree=ancestors_tree,
            breadcrumbs=[
                {"text": "Home", "url": "/"},
                {"text": "Family Tree", "url": "/family-tree"},
                {"text": person["name"], "url": f"/family-tree/person/{person_id_lower}"},
                {"text": "Ancestors", "url": None}
            ],
        )

    @api.route("/family-tree/lineage.svg")
    async def family_tree_lineage_svg(req, resp):
        """Generate SVG visualization of the Messianic lineage (Adam to Jesus)."""
        gedcom_path = get_static_dir() / "adameve.ged"

        if not gedcom_path.exists() or not GedcomReader:
            abort_404(req, resp, "Family tree data not available")
            return

        try:
            family_tree_data, generations = parse_gedcom_to_tree_data(gedcom_path)
        except Exception as e:
            resp.status_code = 500
            resp.media = {"detail": f"Failed to parse family tree: {str(e)}"}
            return

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
        resp.content = svg_content
        resp.mimetype = "image/svg+xml"
