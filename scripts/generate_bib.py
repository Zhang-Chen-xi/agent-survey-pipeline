#!/usr/bin/env python3
"""
BibTeX generator for the Agent Survey Pipeline.

Converts a structured references JSON file into a properly formatted BibTeX file.

Usage:
    python generate_bib.py --input references.json --output references.bib
"""

import argparse
import json
import re
from pathlib import Path
from typing import Optional


def make_bibkey(entry: dict, existing_keys: set) -> str:
    """Generate a unique BibTeX key."""
    authors = entry.get("authors", [])
    first_author = authors[0] if authors else "unknown"
    
    # Extract last name
    if "," in first_author:
        last_name = first_author.split(",")[0].strip()
    elif " " in first_author:
        last_name = first_author.split()[-1]
    else:
        last_name = first_author
    
    year = str(entry.get("year", "0000"))
    title = entry.get("title", "")
    first_word = title.split()[0].lower() if title else "untitled"
    
    # Clean for BibTeX key
    last_name = re.sub(r'[^\w]', '', last_name.lower())
    first_word = re.sub(r'[^\w]', '', first_word)
    
    key = f"{last_name}{year}{first_word}"[:40]
    
    # Handle collisions
    base_key = key
    counter = 2
    while key in existing_keys:
        key = f"{base_key}_{counter}"
        counter += 1
    
    return key


def get_entry_type(entry: dict) -> str:
    """Determine BibTeX entry type."""
    type_map = {
        "journal": "article",
        "article": "article",
        "conference": "inproceedings",
        "inproceedings": "inproceedings",
        "book": "book",
        "thesis": "phdthesis",
        "phdthesis": "phdthesis",
        "mastersthesis": "mastersthesis",
        "preprint": "misc",
        "report": "techreport",
        "misc": "misc",
    }
    entry_type = entry.get("type", "misc").lower()
    return type_map.get(entry_type, "misc")


def format_authors_bibtex(authors: list) -> str:
    """Format author list for BibTeX."""
    if not authors:
        return "Unknown"
    return " and ".join(authors)


def escape_bibtex(text: str) -> str:
    """Escape special BibTeX characters."""
    if not text:
        return ""
    # Protect capital letters in titles (wrap in braces)
    # But don't double-escape
    return text


def generate_entry(entry: dict, bibkey: str) -> str:
    """Generate a single BibTeX entry."""
    entry_type = get_entry_type(entry)
    
    lines = [f"@{entry_type}{{{bibkey},"]
    
    # Authors
    authors = entry.get("authors", [])
    if authors:
        lines.append(f"  author    = {{{format_authors_bibtex(authors)}}},")
    
    # Title
    title = entry.get("title", "")
    if title:
        lines.append(f"  title     = {{{title}}},")
    
    # Venue-specific fields
    if entry_type == "article":
        venue = entry.get("venue", "") or entry.get("journal", "")
        if venue:
            lines.append(f"  journal   = {{{venue}}},")
    elif entry_type == "inproceedings":
        venue = entry.get("venue", "") or entry.get("booktitle", "")
        if venue:
            lines.append(f"  booktitle = {{{venue}}},")
    elif entry_type in ("book",):
        venue = entry.get("publisher", "")
        if venue:
            lines.append(f"  publisher = {{{venue}}},")
    elif entry_type in ("phdthesis", "mastersthesis"):
        venue = entry.get("school", "") or entry.get("institution", "")
        if venue:
            lines.append(f"  school    = {{{venue}}},")
    elif entry_type == "techreport":
        venue = entry.get("institution", "")
        if venue:
            lines.append(f"  institution = {{{venue}}},")
    
    # Year
    year = entry.get("year", "")
    if year:
        lines.append(f"  year      = {{{year}}},")
    
    # Optional fields
    volume = entry.get("volume", "")
    if volume:
        lines.append(f"  volume    = {{{volume}}},")
    
    issue = entry.get("issue", "") or entry.get("number", "")
    if issue:
        lines.append(f"  number    = {{{issue}}},")
    
    pages = entry.get("pages", "")
    if pages:
        lines.append(f"  pages     = {{{pages.replace('-', '--')}}},")
    
    doi = entry.get("doi", "")
    if doi:
        lines.append(f"  doi       = {{{doi}}},")
    
    url = entry.get("url", "")
    if url:
        lines.append(f"  url       = {{{url}}},")
    
    # Language
    language = entry.get("language", "")
    if language:
        lines.append(f"  language  = {{{language}}},")
    
    lines.append("}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate BibTeX from references JSON")
    parser.add_argument("--input", "-i", required=True, help="Path to references JSON")
    parser.add_argument("--output", "-o", default="references.bib", help="Output .bib file")
    args = parser.parse_args()
    
    # Load references
    with open(args.input, "r") as f:
        data = json.load(f)
    
    references = data if isinstance(data, list) else data.get("references", [])
    print(f"Loaded {len(references)} references")
    
    # Generate BibTeX
    existing_keys = set()
    entries = []
    
    for ref in references:
        bibkey = make_bibkey(ref, existing_keys)
        existing_keys.add(bibkey)
        ref["_bibkey"] = bibkey
        entry_text = generate_entry(ref, bibkey)
        entries.append(entry_text)
    
    # Write output
    header = [
        "% BibTeX file generated by Agent Survey Pipeline",
        "% https://github.com/RainVallo/agent-survey-pipeline",
        f"% Total entries: {len(entries)}",
        "",
    ]
    
    output = "\n\n".join(header + entries) + "\n"
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"BibTeX file saved to {args.output} ({len(entries)} entries)")
    
    # Print key mapping
    print("\nBibTeX key mapping:")
    for ref in references:
        print(f"  {ref['_bibkey']:40s} ← {ref.get('title', '')[:50]}")


if __name__ == "__main__":
    main()
