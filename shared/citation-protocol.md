# Citation Verification Protocol

> Cross-cutting protocol referenced by Modules 02, 03, 05, and 09. Defines the authoritative specification for citation verification.

## Protocol Version: 1.0

This document is the single source of truth for how citations are verified across the pipeline. All modules that handle citations MUST conform to this protocol.

## Verification Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| `VERIFIED` | Passed all 6 verification steps | Safe to cite |
| `PARTIALLY_VERIFIED` | Passed DOI + Crossref but failed deep verification | Cite with caution, review context |
| `UNVERIFIED` | Could not be verified by any automated source | Flag for manual verification |
| `CORRECTED` | Originally failed, attributes corrected after verification | Safe to cite with corrected data |
| `REMOVED` | Confirmed hallucination (TF or IH) | Do not cite |
| `SUSPICIOUS` | Passed automated checks but flagged for manual review | Cite only after user confirmation |

## Hallucination Taxonomy

### Type TF: Total Fabrication
**Definition**: The entire paper is invented. No trace exists in any academic database, search engine, or library catalog.
**Detection**: Fails Steps 1-4 of verification cascade. No web presence whatsoever.
**Action**: REMOVE immediately. Search for a real replacement.

### Type PAC: Partial Attribute Corruption
**Definition**: A real paper exists, but one or more attributes are wrong — wrong year, wrong venue, misspelled author name, wrong page numbers.
**Detection**: Passes title search but fails metadata match on specific fields.
**Action**: CORRECT the wrong attributes. Keep the reference.

### Type IH: Invented Hallucination
**Definition**: Title and authors are fabricated, but the research topic is real. The AI generated a plausible-sounding paper.
**Detection**: Topic search returns real papers, but this specific title/author combination does not exist.
**Action**: REMOVE and replace with a real paper on the same topic.

### Type PH: Partial Hallucination
**Definition**: A real paper exists but the DOI is wrong, hijacked, or points to a different paper.
**Detection**: DOI resolves to a paper with a different title, or title search finds a paper with a different DOI.
**Action**: Replace with correct DOI or find the correct paper.

### Type SH: Subtle Hallucination
**Definition**: The paper exists and all metadata is correct, but the cited claim is wrong — the paper does not actually support the assertion made in the citing text.
**Detection**: Requires deep reading (Step 5). Abstract or full text contradicts the citation context.
**Action**: Adjust the citation context or replace with a paper that actually supports the claim.

## Crossref API Usage Rules

1. **Always set User-Agent**: `AgentSurveyPipeline/1.0 (mailto:{CROSSREF_MAILTO})`
2. **Rate limits**:
   - With mailto: 10 req/s, 3 concurrent
   - Without mailto: 2 req/s, 1 concurrent
3. **Respect Retry-After headers** on 429 responses
4. **Add 200ms courtesy delay** between requests
5. **Never cache Crossref responses** across sessions (metadata may be updated)

## DOI Validation Rules

A valid DOI matches the pattern: `10.{4+ digits}/{suffix}`

Common publisher DOI patterns:
| Publisher | Pattern |
|-----------|---------|
| Elsevier | `10.1016/j.{journal}.{year}.{article}` |
| Springer | `10.1007/s{journal_id}-{year}-{article}` |
| Nature | `10.1038/s{journal_id}-{year}-{article}` |
| Wiley | `10.1002/{journal}.{year}.{article}` |
| IEEE | `10.1109/{journal}.{year}.{article}` |
| RSC | `10.1039/{journal_code}{year}` |
| ACS | `10.1021/acs.{journal}.{year}` |
| PNAS | `10.1073/pnas.{article}` |

## BibTeX Key Convention

Format: `{first_author_surname}{year}{first_title_word}`

Rules:
- All lowercase
- No spaces, no special characters
- Chinese names: use pinyin without spaces (e.g., `zhangsan2023yanjiu`)
- Collision resolution: append `_2`, `_3`, etc.
- Maximum length: 40 characters
