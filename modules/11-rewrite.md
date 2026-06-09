# Module 11: Draft-Based Rewriting

> Rewrites specific sections of an existing draft while preserving the author's voice, reference numbering, and already-finalized content.

## Agent Instructions

You are performing targeted rewriting of an existing draft. **Minimal change, precise replacement** — only modify what the user requests.

### Core Principle

| Draft Region | Treatment |
|-------------|-----------|
| User-finalized sections (no annotation) | **Keep verbatim** — do not change a single character |
| User-specified rewrite sections | Rewrite while matching style and context |
| Placeholders (..., [TODO], [待补充]) | Fill with substantive content |
| Underdeveloped sections | Expand while preserving original intent |

### Pre-flight Check

- [ ] User has provided a draft file (PDF, DOCX, or Markdown)
- [ ] User has specified which sections to rewrite
- [ ] Pipeline config loaded

### Workflow

#### Step 1: Extract Draft Content

**PDF**: `pdftotext -layout draft.pdf draft.txt`
**DOCX**: `pandoc --track-changes=accept draft.docx -o draft.md`
**Markdown**: Read directly

#### Step 2: Identify Rewrite Regions

Priority order for identifying what needs rewriting:
1. **User's explicit instructions** (highest priority): "rewrite section 3", "expand the methodology"
2. **Visual annotations**: Highlights, red text, comments in the draft
3. **Text markers**: "……", "[TODO]", "[待补充]", "[TBD]", empty sections
4. **Structural gaps**: Sections significantly shorter than peers

#### Step 3: Extract Reference System

From the draft's reference list, build a mapping: `{ref_number} → {reference_content}`

**CRITICAL**: When rewriting, you MUST reuse the existing reference numbering. Do NOT renumber or insert new references in the middle. New references go at the end.

#### Step 4: Rewrite

For each section to rewrite:

1. Read the surrounding context (preceding and following sections)
2. Match the author's writing style (formality, terminology, paragraph length)
3. Match citation density (if existing sections cite 2-3 papers per paragraph, do the same)
4. Write the new content
5. Verify all citations reference existing entries in the draft's reference list

**Style matching checklist:**
- [ ] Same level of technical detail
- [ ] Same sentence complexity
- [ ] Same terminology conventions
- [ ] Same citation format

#### Step 5: Generate Updated Document

Produce a new document with:
- Original content preserved for non-rewrite sections (byte-for-byte)
- New content for rewrite sections
- Updated reference list (new entries appended at end)
- Change summary documenting what was modified

### Output

Save to `_workspace/11_rewrite_output.md` (or .docx) with:

```markdown
# Rewrite Summary

## Sections Modified
- Section X: {description of changes}
- Section Y: {description of changes}

## Sections Preserved
- Section A, B, C: unchanged

## New References Added
- [N+1] {reference in GB/T 7714 or original format}
- [N+2] {reference}

## Content
{full document with changes integrated}
```

### Quality Gates

- [ ] Only specified sections were modified
- [ ] Reference numbering preserved
- [ ] Writing style matches original
- [ ] Change summary complete
- [ ] All new citations verified
