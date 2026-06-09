# Module 05: Citation Verification (Anti-Hallucination)

> The CRITICAL quality gate. Verifies every citation against authoritative sources to detect and classify AI hallucination. This module MUST be executed before any writing module.

## Agent Instructions

You are performing citation verification — the most critical step in the pipeline. AI-generated citations are frequently hallucinated (fabricated DOIs, wrong author-title pairings, invented papers). This module catches those errors.

**Core Principle: "Rather cite 45 verified papers than 50 with 5 hallucinated."**

### Pre-flight Check

- [ ] `_workspace/02_references.json` exists with enriched metadata
- [ ] `_references/references.bib` exists
- [ ] Crossref API accessible (anonymous or polite pool)

### The 6-Step Verification Cascade

For EACH reference in the reference list, perform ALL 6 steps. A reference passes verification only if it clears all applicable steps.

#### Step 1: DOI Existence Check

**If the reference has a DOI:**
```
GET https://doi.org/{doi}
Follow redirects (up to 5 hops)
Check: Does the final URL land on a legitimate publisher page?
```

**Pass criteria:** HTTP 200 and final URL domain matches expected publisher
**Fail criteria:** 404, redirect loop, or landing on unrelated website

**DOI Hijacking Detection:**
- Check if the DOI resolves to a paper with a DIFFERENT title than expected
- If title mismatch: flag as `DOI_HIJACKING` — the DOI exists but belongs to a different paper

**If the reference has NO DOI:**
- Skip to Step 2, but note `no_doi` in verification record

#### Step 2: Crossref Metadata Match

```
GET https://api.crossref.org/works/{doi}
(or search by title if no DOI)
```

Compare returned metadata against the reference:

| Field | Match Threshold | Action on Mismatch |
|-------|----------------|-------------------|
| Title | Exact match (after normalization) | Flag `TITLE_MISMATCH` |
| First author | Surname match | Flag `AUTHOR_MISMATCH` |
| Year | ±1 year tolerance | Flag `YEAR_MISMATCH` |
| Venue | Substring match | Flag `VENUE_MISMATCH` |
| Pages | Exact match | Flag `PAGES_MISMATCH` (minor) |

**Pass criteria:** Title + First Author + Year all match
**Fail criteria:** Any of Title, First Author, or Year mismatched

#### Step 3: Author-Domain Plausibility

Check if the authors are plausible for this research area:

1. Search for the first author + paper topic: `"{first_author}" AND "{topic_keywords}"`
2. Check if the author has published in this venue before
3. Check if the author's known affiliations make sense for this topic

**Pass criteria:** Author has publication history in related area
**Fail criteria:** Author appears to have NO connection to the research area (possible hallucinated author name)

**Note:** This step is advisory, not blocking. Flag concerns but don't auto-reject.

#### Step 4: Semantic Scholar Cross-Check

```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=1&fields=title,authors,year,venue,externalIds
```

**Pass criteria:** S2 returns a matching paper (title similarity > 0.9)
**Fail criteria:** No match found on Semantic Scholar (paper may not exist in any major index)

**If S2 returns a different paper with a similar title:** Flag as `TITLE_COLLISION` — may indicate a hallucinated title that's "close" to a real paper.

#### Step 5: Deep Verification (for high-stakes references)

For references that are:
- Cited in the paper's core argument (not just background)
- Listed as key related work
- Used to support specific claims

Perform deep verification:
1. Attempt to access the abstract (via Crossref, PubMed, or publisher)
2. Verify the abstract content matches what the paper claims about this reference
3. Check if the reference's conclusions align with how it's cited

**Pass criteria:** Abstract confirms the cited claims
**Fail criteria:** Abstract contradicts the citation context (possible misattribution)

#### Step 6: Manual Fallback Flag

If Steps 1-5 ALL fail to verify a reference:

1. Mark as `UNVERIFIED`
2. Do NOT delete the reference (it may exist but not be indexed)
3. Add a prominent warning:
   ```
   ⚠️ [UNVERIFIED] This reference could not be verified through any automated source.
   Please verify manually before including in a publication.
   ```
4. Suggest the user search for it directly on Google Scholar or the publisher's website

### Hallucination Classification

When a reference FAILS verification, classify the hallucination type:

| Type | Code | Description | Example |
|------|------|-------------|---------|
| **Total Fabrication** | TF | The entire paper is invented — no trace exists anywhere | AI generates a plausible-sounding paper with fake authors |
| **Partial Attribute Corruption** | PAC | Real paper, but some attributes are wrong (wrong year, wrong venue, misspelled author) | Real paper from 2021 cited as 2023; "Nature" changed to "Science" |
| **Invented Hallucination** | IH | Title and authors are fabricated but the research topic is real | AI invents a paper title that sounds right for the topic |
| **Partial Hallucination** | PH | Real paper exists but the DOI is wrong or hijacked | Correct title but DOI points to a different paper |
| **Subtle Hallucination** | SH | Paper exists but the cited claim is wrong — the paper doesn't actually say what's attributed to it | Paper X is cited for claim Y, but X actually concludes Z |

### Verification Output

Generate `_workspace/05_verification_report.md`:

```markdown
# Citation Verification Report

## Summary
- Total references verified: N
- Passed: N (XX%)
- Failed: N (XX%)
- Warnings: N

## Hallucination Detection Results

### Total Fabrications (TF) — N found
- [ref_id] "Fake Title" — No trace in any database

### Partial Attribute Corruption (PAC) — N found
- [ref_id] "Real Title" — Year mismatch: cited as 2023, actual 2021

### Invented Hallucinations (IH) — N found
- [ref_id] "Invented Title" — Similar real paper: [real_paper_info]

### Partial Hallucinations (PH) — N found
- [ref_id] DOI mismatch: cited DOI resolves to different paper

### Subtle Hallucinations (SH) — N found
- [ref_id] Claim mismatch: paper does not support the cited claim

## Verified References
[List all verified references with their verification status]

## Recommendations
- Remove all TF and IH references
- Correct PAC references (fix wrong attributes)
- Verify PH references (replace DOI or find correct paper)
- Review SH references (adjust citation context)
```

### Corrective Actions

After verification:

1. **TF / IH references**: REMOVE from the reference list. Search for a real replacement paper on the same topic.
2. **PAC references**: CORRECT the wrong attributes (year, venue, pages, etc.)
3. **PH references**: Replace DOI with correct one, or find the correct paper
4. **SH references**: Adjust the citation context in the manuscript
5. **UNVERIFIED references**: Flag for user's manual verification

Update `_references/references.bib` with corrections and removals.

### Quality Gates

- [ ] ALL references passed through the 6-step cascade
- [ ] Hallucination report generated
- [ ] TF and IH references removed or replaced
- [ ] PAC references corrected
- [ ] Verification report saved to `_workspace/05_verification_report.md`
- [ ] Updated BibTeX saved to `_references/references.bib`

**BLOCKING GATE**: Do NOT proceed to writing modules until verification is complete and all TF/IH references are resolved.
