#!/usr/bin/env python3
"""
Detect shallow/generic commentary entries that need improvement.

Flags entries that have:
- Generic templated questions ("How does X:Y deepen my understanding...")
- Boilerplate historical sections
- Missing Greek/Hebrew terms
- Very short analysis sections
- Templated analysis patterns
"""

import json
import os
import re
from pathlib import Path

# Patterns that indicate generic/shallow commentary
GENERIC_QUESTION_PATTERNS = [
    r"How does .+ deepen my understanding of the gospel",
    r"What specific action or attitude change does this verse call me to make",
    r"How can I more sacrificially love the people",
    r"How does this passage point to Christ and His redemptive work\?$",
]

GENERIC_HISTORICAL_PATTERNS = [
    r"<strong>Historical Setting:</strong> .+ was written around \d+ CE from",
    r"<strong>Occasion:</strong> Preparing for visit to Rome",
    r"The Greco-Roman world valued rhetoric, philosophy, and social status",
    r"First-century believers lived in a pluralistic, pagan society",
    r"Paul's instructions addressed both timeless theological truths and specific cultural situations",
]

GENERIC_ANALYSIS_PATTERNS = [
    r"This verse contributes to .+'s overall purpose in",
    r"The key themes of justification by faith, law and grace, Israel and the church are evident",
    r"Paul carefully explains the law's role: revealing sin and pointing to Christ",
    r"The Holy Spirit empowers believers for holiness and service",
    r"Christ is the center of Paul's theology and message",
    r"Paul's discussion of Israel's role in God's redemptive plan\.$",
    r"Paul's teaching on sanctification and life in the Spirit\.$",
]

# Good indicators (if missing, flag the entry)
GOOD_INDICATORS = {
    'greek': [r'<em>[^<]+</em>', r'[Gg]reek', r'[α-ωΑ-Ω]'],
    'hebrew': [r'<em>[^<]+</em>', r'[Hh]ebrew', r'[\u0590-\u05FF]'],
}


def check_entry(book: str, chapter: str, verse: str, entry: dict) -> list[str]:
    """Check a single commentary entry for quality issues."""
    issues = []

    analysis = entry.get('analysis', '')
    historical = entry.get('historical', '')
    questions = entry.get('questions', [])

    ref = f"{book} {chapter}:{verse}"

    # Check for generic questions
    for q in questions:
        for pattern in GENERIC_QUESTION_PATTERNS:
            if re.search(pattern, q):
                issues.append(f"{ref}: Generic question pattern detected")
                break

    # Check for generic historical content
    for pattern in GENERIC_HISTORICAL_PATTERNS:
        if re.search(pattern, historical):
            issues.append(f"{ref}: Generic historical boilerplate detected")
            break

    # Check for generic analysis patterns
    for pattern in GENERIC_ANALYSIS_PATTERNS:
        if re.search(pattern, analysis):
            issues.append(f"{ref}: Generic analysis pattern detected")
            break

    # Check analysis length (too short is suspicious)
    # Good commentary should be at least 500 chars
    if len(analysis) < 400:
        issues.append(f"{ref}: Analysis too short ({len(analysis)} chars)")

    # Check for presence of original language terms in NT books
    nt_books = ['matthew', 'mark', 'luke', 'john', 'acts', 'romans',
                '1_corinthians', '2_corinthians', 'galatians', 'ephesians',
                'philippians', 'colossians', '1_thessalonians', '2_thessalonians',
                '1_timothy', '2_timothy', 'titus', 'philemon', 'hebrews',
                'james', '1_peter', '2_peter', '1_john', '2_john', '3_john',
                'jude', 'revelation']

    book_lower = book.lower().replace(' ', '_')

    # Check for Greek in NT
    if book_lower in nt_books:
        has_greek = any(re.search(p, analysis) for p in GOOD_INDICATORS['greek'])
        if not has_greek:
            issues.append(f"{ref}: Missing Greek terms (NT book)")

    # Check for Hebrew in OT
    if book_lower not in nt_books:
        has_hebrew = any(re.search(p, analysis) for p in GOOD_INDICATORS['hebrew'])
        if not has_hebrew:
            issues.append(f"{ref}: Missing Hebrew terms (OT book)")

    return issues


def scan_book(filepath: Path) -> list[str]:
    """Scan a single book's commentary file."""
    all_issues = []

    with open(filepath) as f:
        data = json.load(f)

    book = data.get('book', filepath.stem.replace('_', ' ').title())
    commentary = data.get('commentary', {})

    for chapter, verses in commentary.items():
        if not isinstance(verses, dict):
            continue
        for verse, entry in verses.items():
            if not isinstance(entry, dict) or 'analysis' not in entry:
                continue
            issues = check_entry(book, chapter, verse, entry)
            all_issues.extend(issues)

    return all_issues


def main():
    """Scan all commentary files and report issues."""
    import argparse
    parser = argparse.ArgumentParser(description='Detect shallow commentary')
    parser.add_argument('--worst', action='store_true', help='Show only worst offenders (3+ issues)')
    parser.add_argument('--book', type=str, help='Check specific book only')
    parser.add_argument('--export', type=str, help='Export problem verses to file')
    args = parser.parse_args()

    commentary_dir = Path('kjvstudy_org/data/verse_commentary')

    # Track issues per verse
    verse_issues = {}  # ref -> list of issues

    for filepath in sorted(commentary_dir.glob('*.json')):
        if args.book and args.book.lower() not in filepath.stem.lower():
            continue

        with open(filepath) as f:
            data = json.load(f)

        book = data.get('book', filepath.stem.replace('_', ' ').title())
        commentary = data.get('commentary', {})

        for chapter, verses in commentary.items():
            if not isinstance(verses, dict):
                continue
            for verse, entry in verses.items():
                if not isinstance(entry, dict) or 'analysis' not in entry:
                    continue
                issues = check_entry(book, chapter, verse, entry)
                if issues:
                    ref = f"{book} {chapter}:{verse}"
                    verse_issues[ref] = [i.split(': ', 1)[1] for i in issues]

    # Summary
    print(f"\n{'='*60}")
    print(f"SHALLOW COMMENTARY DETECTION REPORT")
    print(f"{'='*60}\n")

    if not verse_issues:
        print("✅ No issues detected! All commentary appears to be high quality.")
        return

    # Filter to worst offenders if requested
    if args.worst:
        verse_issues = {k: v for k, v in verse_issues.items() if len(v) >= 3}
        print(f"Showing only verses with 3+ issues:\n")

    # Sort by number of issues (worst first)
    sorted_verses = sorted(verse_issues.items(), key=lambda x: -len(x[1]))

    # Count by severity
    severe = sum(1 for v in verse_issues.values() if len(v) >= 3)
    moderate = sum(1 for v in verse_issues.values() if len(v) == 2)
    minor = sum(1 for v in verse_issues.values() if len(v) == 1)

    print(f"📊 Issue Summary:")
    print(f"   🔴 Severe (3+ issues): {severe} verses")
    print(f"   🟡 Moderate (2 issues): {moderate} verses")
    print(f"   🟢 Minor (1 issue): {minor} verses")
    print(f"   Total: {len(verse_issues)} verses with issues\n")

    # Show worst offenders
    print(f"\n🔴 WORST OFFENDERS (need immediate attention):")
    print("-" * 60)

    shown = 0
    for ref, issues in sorted_verses:
        if len(issues) >= 3:
            print(f"\n{ref} ({len(issues)} issues):")
            for issue in issues:
                print(f"   • {issue}")
            shown += 1
            if shown >= 50:
                remaining = sum(1 for _, v in sorted_verses if len(v) >= 3) - 50
                if remaining > 0:
                    print(f"\n   ... and {remaining} more severe cases")
                break

    # Export if requested
    if args.export:
        with open(args.export, 'w') as f:
            for ref, issues in sorted_verses:
                if len(issues) >= 3:
                    f.write(f"{ref}\n")
        print(f"\n📁 Exported {severe} severe cases to {args.export}")

    print(f"\n{'='*60}")


if __name__ == '__main__':
    main()
