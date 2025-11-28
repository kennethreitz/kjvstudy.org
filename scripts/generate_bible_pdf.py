#!/usr/bin/env python3
"""
Generate a complete Bible PDF with cross-references and word studies.

This is a one-time generation script that creates a comprehensive PDF of the
entire King James Bible. The resulting PDF will be ~1000 pages and include
all cross-references and word studies as footnotes.

Usage:
    uv run python scripts/generate_bible_pdf.py

Output:
    kjv-complete-bible.pdf (in the current directory)
"""

import asyncio
import sys
from pathlib import Path
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.kjv import bible
from kjvstudy_org.routes.commentary import generate_commentary, generate_word_study_sidenotes
from kjvstudy_org.cross_references import get_cross_references
from kjvstudy_org.utils.books import OT_BOOKS, NT_BOOKS
from kjvstudy_org.utils.pdf import render_html_to_pdf_async
from jinja2 import Environment, FileSystemLoader


async def generate_bible_pdf():
    """Generate the complete Bible PDF."""
    print("=" * 80)
    print("GENERATING COMPLETE BIBLE PDF")
    print("=" * 80)
    print()
    print("This will generate a comprehensive PDF of the entire KJV Bible")
    print("with cross-references and word studies as footnotes.")
    print()
    print("⚠️  This may take several minutes to complete...")
    print()

    # Load Jinja2 templates
    template_dir = Path(__file__).parent.parent / "kjvstudy_org" / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    # Add number_format filter
    def number_format(value):
        return f"{value:,}"
    env.filters['number_format'] = number_format

    books = bible.get_books()
    old_testament = OT_BOOKS
    new_testament = NT_BOOKS

    # Prepare data for all books
    books_data = []
    total_verses = 0
    total_books = len(books)

    print(f"Processing {total_books} books...")
    print()

    for book_idx, book_name in enumerate(books, 1):
        print(f"[{book_idx}/{total_books}] Processing {book_name}...")

        chapters_dict = {}
        commentaries_dict = {}
        shown_words = set()  # Track word studies per book

        # Get all chapters for this book
        chapters = bible.get_chapters_for_book(book_name)

        for chapter_num in chapters:
            verses = bible.get_verses_by_book_chapter(book_name, chapter_num)
            chapters_dict[chapter_num] = verses
            total_verses += len(verses)

            # Generate commentaries for this chapter
            chapter_commentaries = {}
            for verse in verses:
                commentary = generate_commentary(book_name, chapter_num, verse)

                # Add word study sidenotes (avoiding repetition within book)
                word_studies = generate_word_study_sidenotes(
                    verse.text, book_name, chapter_num, verse.verse, shown_words
                )
                commentary['word_studies'] = word_studies
                for study in word_studies:
                    shown_words.add(study['word'].lower())

                # Add cross-references grouped by description
                cross_refs = get_cross_references(book_name, chapter_num, verse.verse)
                grouped_refs = defaultdict(list)
                for ref in cross_refs:
                    description = ref['note'] if ref['note'] else 'Related'
                    grouped_refs[description].append(ref['ref'])

                commentary['cross_reference_groups'] = [
                    {'description': desc, 'refs': refs}
                    for desc, refs in grouped_refs.items()
                ]

                chapter_commentaries[verse.verse] = commentary

            commentaries_dict[chapter_num] = chapter_commentaries

        books_data.append({
            'name': book_name,
            'chapter_count': len(chapters),
            'chapters': chapters_dict,
            'commentaries': commentaries_dict
        })

        print(f"  ✓ {book_name}: {len(chapters)} chapters")

    print()
    print(f"✅ Processed all {total_books} books ({total_verses:,} verses)")
    print()
    print("Rendering HTML template...")

    # Render HTML
    template = env.get_template("bible_pdf.html")
    html_content = template.render(
        books=books_data,
        old_testament=old_testament,
        new_testament=new_testament,
        total_verses=total_verses,
    )

    print("✓ HTML rendered")
    print()
    print("Generating PDF (this will take a while)...")

    # Generate PDF
    pdf_buffer = await render_html_to_pdf_async(html_content)

    # Save to file
    output_file = Path("kjv-complete-bible.pdf")
    with open(output_file, 'wb') as f:
        f.write(pdf_buffer.getvalue())

    file_size_mb = output_file.stat().st_size / (1024 * 1024)

    print()
    print("=" * 80)
    print("✅ COMPLETE BIBLE PDF GENERATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Output file: {output_file.absolute()}")
    print(f"File size: {file_size_mb:.1f} MB")
    print(f"Total verses: {total_verses:,}")
    print(f"Books: {total_books}")
    print()
    print("The PDF includes:")
    print("  • Title page and table of contents")
    print("  • All 66 books of the King James Bible")
    print("  • Cross-references as footnotes (grouped by theme)")
    print("  • Word studies with Greek/Hebrew terms")
    print("  • Professional typography and formatting")
    print()


if __name__ == "__main__":
    asyncio.run(generate_bible_pdf())
