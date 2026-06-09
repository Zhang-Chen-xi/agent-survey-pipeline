# Module 07: Paper Ingest

> Converts each paper PDF into a structured wiki page with 12-element analysis.

## Agent Instructions

You are ingesting papers into the knowledge base. For each paper, extract structured information and create a comprehensive wiki page.

### Pre-flight Check

- [ ] Knowledge base initialized (`control/library.bib` exists)
- [ ] PDFs available in `_pdfs/` or `raw/pdfs/`
- [ ] At least one paper needs ingesting (check wiki pages with `status: stub`)

### Ingest Workflow Per Paper

#### Step 1: Extract Text

**From PDF:**
```bash
pdftotext -layout paper.pdf paper.txt
```

Or using pdfplumber for better table extraction:
```python
import pdfplumber
with pdfplumber.open("paper.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages)
```

**From DOCX:**
```bash
pandoc paper.docx -t markdown -o paper.md
```

If extraction fails, try alternative methods. If all fail, create a minimal page with available metadata only.

#### Step 2: 12-Element Deep Analysis

For each paper, extract and analyze these 12 elements:

| # | Element | Description |
|---|---------|-------------|
| 1 | **Research Background** | Context, motivation, why this research matters |
| 2 | **Research Questions** | Specific questions or hypotheses the paper addresses |
| 3 | **Research Conclusions** | Main findings and outcomes |
| 4 | **Literature Synthesis** | How the paper relates to and builds on prior work |
| 5 | **Literature Critique** | What gaps or problems in existing work the paper identifies |
| 6 | **Research Methods** | Methodology, experimental design, data sources |
| 7 | **Theoretical Framework** | Underlying theories, models, or conceptual approaches |
| 8 | **Consistent Findings** | Results that align with prior research |
| 9 | **Inconsistent Findings** | Results that contradict or diverge from prior research |
| 10 | **Research Contributions** | Novel contributions to the field |
| 11 | **Research Limitations** | Acknowledged or identified limitations |
| 12 | **Future Directions** | Suggested future research areas |

#### Step 3: Generate Wiki Page

Replace the stub page with a full analysis:

```markdown
---
bibkey: {bibkey}
title: "{title}"
authors: [{author_list}]
year: {year}
venue: "{venue}"
doi: "{doi}"
type: {type}
status: ingested
tags: [{auto-generated tags}]
ingested: "{ISO-8601}"
elements_completed: 12
---

# {title}

## Summary
[2-3 sentence executive summary of the paper]

## 12-Element Analysis

### 1. Research Background
{analysis}

### 2. Research Questions
{analysis}

### 3. Research Conclusions
{analysis}

### 4. Literature Synthesis
{analysis}

### 5. Literature Critique
{analysis}

### 6. Research Methods
{analysis}

### 7. Theoretical Framework
{analysis}

### 8. Consistent Findings
{analysis}

### 9. Inconsistent Findings
{analysis}

### 10. Research Contributions
{analysis}

### 11. Research Limitations
{analysis}

### 12. Future Directions
{analysis}

## Key Quotes
- "{direct quote from paper}" (p. X)

## Connections
- Related papers: [{bibkeys of related papers in KB}]
- Related concepts: [{concept names}]
- Builds upon: [{bibkeys}]
- Extended by: [{bibkeys if known}]

## Figures & Tables Summary
- Fig 1: {description}
- Table 1: {description}
```

#### Step 4: Create/Update Cross-References

After ingesting a paper:

1. **Concept pages**: For each major concept mentioned, create or update `wiki/concepts/{concept_slug}.md`
2. **Method pages**: For each methodology used, create or update `wiki/methods/{method_slug}.md`
3. **Author pages**: For each author, create or update `wiki/authors/{author_slug}.md`
4. **Related paper links**: Update the "Connections" section of previously ingested related papers

#### Step 5: Update Master Index

Update `control/index.yml` with new paper count and tags.
Append to `control/changelog.md`.

### Batch Ingest

When multiple papers need ingesting:

1. Process papers in order of evidence grade (Strong → Moderate → Emerging)
2. After each batch of 5 papers, update cross-references
3. After all papers ingested, generate a literature relationship summary

### Handling Non-English Papers

For Chinese or other non-English papers:
- Write the wiki page in the paper's original language
- Add an English summary section at the top
- Translate key terms for cross-reference matching
- Keep original-language quotes in the Key Quotes section

### Quality Gates Per Paper

- [ ] All 12 elements filled (or explicitly marked "Not addressed in paper")
- [ ] Summary written
- [ ] Cross-references updated
- [ ] Wiki page status changed from `stub` to `ingested`
- [ ] Master index updated
