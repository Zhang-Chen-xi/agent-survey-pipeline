# Module 06: Knowledge Base Setup

> Sets up a BibTeX + Markdown wiki knowledge base for managing the literature corpus across the research lifecycle.

## Agent Instructions

You are setting up a structured knowledge base for the user's research literature. This KB persists across sessions and supports paper ingest, wiki browsing, and retrieval.

### Architecture

The knowledge base uses a four-layer architecture:

```
{kb_root}/
├── raw/                    # Layer 1: Raw materials (PDFs, extracted text)
│   ├── pdfs/               # Original PDFs
│   └── text/               # Extracted text files
├── wiki/                   # Layer 2: Global wiki (one page per paper)
│   ├── papers/             # Paper wiki pages
│   ├── concepts/           # Concept pages (cross-paper themes)
│   ├── methods/            # Method pages
│   └── authors/            # Author pages
├── projects/               # Layer 3: Project trees (per research project)
│   └── {project_name}/
│       ├── manifest.yml    # Project metadata
│       ├── outline.md      # Paper outline
│       ├── literature-map.md  # Literature relationship map
│       └── notes/          # Project-specific notes
└── control/                # Layer 4: Control files
    ├── library.bib          # Master BibTeX file
    ├── index.yml            # Master index
    └── changelog.md         # Change log
```

### Setup Sequence

#### Step 1: Determine KB Location

Ask the user:
```
Where should the knowledge base be created?
1. Current working directory: ./literature-kb/
2. Custom path: [specify]
3. Use existing KB: [specify path to existing kb_root]
```

If option 3 and an existing KB is found, skip to Step 3 (verification).

#### Step 2: Initialize Directory Structure

Create all directories and seed control files.

**`control/library.bib`:**
```bibtex
% Master BibTeX file for literature knowledge base
% Created: {timestamp}
% This file is auto-maintained by the pipeline.
% Manual edits are preserved (new entries are appended, never overwritten).
```

**`control/index.yml`:**
```yaml
# Knowledge Base Index
kb_name: "{user's project name}"
created: "{ISO-8601}"
version: "1.0"
stats:
  total_papers: 0
  total_concepts: 0
  total_methods: 0
  total_authors: 0
projects: []
```

**`control/changelog.md`:**
```markdown
# Knowledge Base Changelog

## {date} — Initialized
- Created knowledge base structure
- Project: {project name}
```

#### Step 3: Import Existing References

If `_workspace/02_references.json` and `_references/references.bib` exist:

1. Copy verified references into `control/library.bib`
2. For each verified reference, create a stub wiki page in `wiki/papers/`

**Wiki page template** (`wiki/papers/{bibkey}.md`):
```markdown
---
bibkey: {bibkey}
title: "{title}"
authors: [{author_list}]
year: {year}
venue: "{venue}"
doi: "{doi}"
type: {article|inproceedings|book|...}
status: stub
tags: []
ingested: "{ISO-8601}"
---

# {title}

## Summary
[To be filled during paper ingest]

## Key Contributions
[To be filled]

## Methodology
[To be filled]

## Relevance to Project
[To be filled]

## Connections
- Related papers: []
- Related concepts: []
```

#### Step 4: Report KB Status

```
Knowledge Base Initialized:
📁 Location: {kb_root}
📄 Papers: {N} stub pages created
📚 Master BibTeX: {N} entries
🏗️ Projects: 0 (create one with paper writing modules)

Next: Run Module 07 (Paper Ingest) to fill in wiki pages,
or proceed directly to writing modules.
```

### Global Hard Rules

These rules govern ALL knowledge base operations:

1. **Never delete a wiki page** — only mark as deprecated
2. **Never overwrite user edits** — append or merge, never replace
3. **BibTeX is the source of truth** — wiki pages derive from BibTeX entries
4. **Every paper gets exactly one wiki page** — identified by BibTeX key
5. **Frontmatter is machine-managed** — do not edit YAML frontmatter manually
6. **Raw PDFs are never modified** — read-only after ingest
7. **Project trees are isolated** — changes in one project don't affect others
8. **Changelog is append-only** — never edit past entries
9. **Index is rebuilt from disk** — if index.yml is corrupted, rebuild from wiki pages
10. **Cross-references use BibTeX keys** — never use titles or DOIs as internal links
11. **All timestamps are ISO-8601 UTC** — consistent dating
12. **Stub pages are valid** — a page with only frontmatter is acceptable
