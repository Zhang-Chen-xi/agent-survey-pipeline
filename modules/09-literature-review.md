# Module 09: Literature Review / Survey Writing

> Writes a comprehensive literature review with anti-hallucination enforcement, multi-level literature tracing, and smart error handling for inaccessible papers.

## Agent Instructions

You are writing a literature review or survey paper. This is the core writing module. Every citation you write MUST come from the verified reference list. **Absolutely no fabrication of references, data, or claims.**

### Iron Rules (Non-Negotiable)

1. **NEVER fabricate a citation.** If you cannot find a verified reference for a claim, write `[CITATION NEEDED]` instead.
2. **NEVER invent data or statistics.** If the exact number is not in your verified sources, say "studies suggest" rather than inventing a percentage.
3. **NEVER attribute a claim to a paper that doesn't make it.** Verify the paper actually says what you're citing it for.
4. **"Rather incomplete than fake."** A survey with 45 verified papers is infinitely better than one with 50 papers where 5 are hallucinated.
5. **Every citation must trace back to `_references/references.bib`** via BibTeX key. No ad-hoc references.

### Pre-flight Check

- [ ] Outline approved (`_workspace/08_outline.md`)
- [ ] Citation verification complete (`_workspace/05_verification_report.md`)
- [ ] All TF/IH hallucinations removed from reference list
- [ ] Wiki pages ingested (recommended for deep analysis)

### Writing Workflow

#### Phase 1: Pre-Writing Organization

1. **Group references by theme** according to the outline sections
2. **Build citation matrix**: For each pair of key papers, note how they relate (builds on, contradicts, extends, applies)
3. **Identify narrative arc**: What story does the literature tell? Chronological? Problem-solution? Debate-resolution?

#### Phase 2: Section-by-Section Writing

For each section in the outline:

**Step 2a: Literature Tracing (Level 0/1/2)**

- **Level 0 — Direct references**: Papers directly cited in this section
- **Level 1 — Context references**: Papers that provide background for Level 0 papers
- **Level 2 — Peripheral references**: Survey papers, foundational works that frame the section

Ensure each section has appropriate depth. A survey section should typically have 5-15 Level 0 references.

**Step 2b: Draft the Section**

Write in academic prose following these principles:

1. **Thematic organization, not chronological**: Group by approach/idea, not by year
2. **Critical analysis, not summary**: Don't just list what each paper does — compare, contrast, evaluate
3. **Clear topic sentences**: Each paragraph should start with a clear claim, then support with evidence
4. **Smooth transitions**: Connect paragraphs and sections with logical transitions
5. **Proper citation density**: At least 1-2 citations per substantive claim

**Writing patterns for survey papers:**

```markdown
## {Section Title}

{Opening paragraph: scope and organization of this section}

### {Subsection: Approach Category A}

{Topic sentence introducing this category}.
Early work by {author} \cite{bibkey1} established...
This was extended by \cite{bibkey2} who...
A fundamentally different approach was proposed by \cite{bibkey3},
which {key innovation}.

**Comparison.** The key distinction between these approaches lies in...
While \cite{bibkey1} achieves {result}, \cite{bibkey3} demonstrates
{contrasting result}, suggesting that {analysis}.

### {Subsection: Approach Category B}
...

### {Summary and Discussion}
{Synthesis paragraph connecting this section to the broader narrative}
```

**Step 2c: Citation Verification During Writing**

As you write each citation:
1. Look up the BibTeX key in `_references/references.bib`
2. Confirm the paper exists and is verified
3. Confirm the claim you're making is consistent with the paper's actual content (check wiki page if available)
4. Use the correct citation command for the target format (LaTeX `\cite{}`, Word `[1]`, etc.)

If you cannot verify a citation mid-writing:
- Write `[CITATION NEEDED: topic description]` as a placeholder
- Continue writing
- Flag all placeholders in the section summary for user attention

#### Phase 3: Cross-Section Integration

After all sections are drafted:

1. **Check citation consistency**: Same paper cited the same way throughout
2. **Check narrative flow**: Does the story progress logically?
3. **Check coverage**: Are there sections with too few citations? Too many without analysis?
4. **Check balance**: Is each major approach given appropriate coverage?
5. **Write connecting paragraphs** between sections if needed

#### Phase 4: Introduction and Conclusion

Write these LAST (after all body sections):

**Introduction must include:**
- The research problem and why it matters (with citations)
- What makes this survey timely and needed
- Scope: what IS and IS NOT covered
- Explicit contribution statement (3-4 contributions)
- Paper organization paragraph

**Conclusion must include:**
- Summary of key findings from the survey
- The most important open problems
- A forward-looking perspective on the field

### Handling Inaccessible Key Papers

When a paper is important but unavailable (no PDF, paywalled):

```
User Decision Required:
Paper "{title}" ({bibkey}) is identified as important for Section {N}
but no full text is available.

Options:
1. [Cite by metadata only] — Use title/abstract from Crossref/S2, cite with ⚠️ marker
2. [Find replacement] — Search for a similar accessible paper
3. [Skip this paper] — Remove from this section
4. [User provides PDF] — Wait for user to upload
```

### Output

Save the literature review to `_workspace/09_literature_review.md`:

```markdown
# {Paper Title}

## Abstract
{150-250 word abstract}

## 1. Introduction
{full text with \cite{bibkey} citations}

## 2. {Section Title}
{full text}
...

## N. Conclusion
{full text}

## References
{auto-generated from cited BibTeX entries}

---
## Writing Notes
- Citations used: N
- [CITATION NEEDED] placeholders: N
- Sections requiring user review: [list]
- Inaccessible papers cited: [list with decisions]
```

### Quality Gates

- [ ] All sections written per outline
- [ ] Zero fabricated citations (every `\cite{}` maps to a verified BibTeX entry)
- [ ] Citation density appropriate throughout
- [ ] Critical analysis present (not just summaries)
- [ ] [CITATION NEEDED] placeholders clearly flagged
- [ ] Writing notes section complete
