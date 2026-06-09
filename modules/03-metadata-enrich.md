# Module 03: Metadata Enrichment

> Enriches parsed references with authoritative metadata from Crossref, PubMed, and Semantic Scholar APIs.

## Agent Instructions

You are enriching a parsed reference list with verified metadata. The goal is to fill missing fields, correct errors, and normalize data before citation verification.

### Pre-flight Check

- [ ] `_workspace/02_references.json` exists and is valid
- [ ] `_references/references.bib` exists
- [ ] Pipeline config loaded (check `CROSSREF_MAILTO` for API rate limits)

### Enrichment Pipeline

Process each reference sequentially. For each reference, apply the enrichment cascade:

#### Source 1: Crossref API (Primary)

**For references WITH a DOI:**
```
GET https://api.crossref.org/works/{doi}
Headers: User-Agent: AgentSurveyPipeline/1.0 (mailto:{CROSSREF_MAILTO})
```

Extract:
- Canonical title
- Full author list with ORCID (if available)
- Container title (journal/conference name)
- Volume, issue, page range
- Published date (print and online)
- ISSN, ISBN
- Publisher
- License information
- Reference count (useful for citation network analysis)

**For references WITHOUT a DOI:**
```
GET https://api.crossref.org/works?query.title={title}&query.author={first_author}&select=DOI,title,author,container-title,published-print,volume,issue,page&rows=3
```
Match criteria: title similarity > 0.85 (normalized) AND at least first author surname matches.

**Rate limiting:**
- With `mailto`: 10 requests/second, 3 concurrent
- Without `mailto`: 2 requests/second, 1 concurrent
- Always respect `Retry-After` header on 429 responses
- Add 200ms delay between requests as courtesy

#### Source 2: PubMed/EuropePMC (Biomedical)

For biomedical references (detected by venue keywords: "journal of", "medical", "clinical", "biological", etc.):

**Search by title:**
```
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:{doi}+OR+TITLE:"{title}"&format=json&resultType=core
```

Extract:
- PubMed ID (PMID)
- PMC ID (if open access)
- MeSH terms
- Abstract (first 500 chars for verification)
- Grant information

#### Source 3: Semantic Scholar (Citation Data)

```
GET https://api.semanticscholar.org/graph/v1/paper/{doi_or_s2_id}?fields=title,authors,citationCount,influentialCitationCount,venue,year,externalIds,isOpenAccess,openAccessPdf
```

Extract:
- Citation count (for evidence grading)
- Influential citation count
- Open access PDF URL (if available)
- External IDs (ArXiv, ACL, DBLP, etc.)

#### Source 4: arXiv (Preprints)

For references identified as arXiv preprints:
```
GET http://export.arxiv.org/api/query?id_list={arxiv_id}
```

Extract:
- Full abstract
- Categories
- Updated date (may differ from submitted date)
- PDF URL

### Enrichment Merge Strategy

When multiple sources return data for the same reference:

| Field | Priority |
|-------|----------|
| Title | Crossref > PubMed > Semantic Scholar > arXiv > Original |
| Authors | Crossref > PubMed > Original > Others |
| DOI | Crossref > Semantic Scholar externalIds > Original |
| Year | Crossref published-print > published-online > Original |
| Venue | Crossref container-title > PubMed journal > Original |
| Pages | Crossref > Original |
| Citation count | Semantic Scholar (only source) |
| Abstract | PubMed > arXiv > Semantic Scholar TL;DR |

**Conflict resolution**: When sources disagree (e.g., different page numbers), prefer Crossref as the DOI registration authority. Log the conflict in `_logs/enrichment_conflicts.log`.

### Normalization Rules

After enrichment, normalize all fields:

1. **Author names**: `{Last}, {First}` format. For Chinese names: `{姓}{名}` without comma (e.g., "张三")
2. **Title**: Sentence case for English, original case for Chinese. Strip trailing periods.
3. **Venue**: Full name (not abbreviation). Maintain a mapping of common abbreviations:
   - "NeurIPS" → "Advances in Neural Information Processing Systems"
   - "ICML" → "International Conference on Machine Learning"
   - "J. Am. Chem. Soc." → "Journal of the American Chemical Society"
4. **Year**: 4-digit integer
5. **DOI**: Lowercase, URL-safe format: `10.xxxx/xxxxx`

### Output

Update `_workspace/02_references.json` with enriched metadata:

```json
{
  "ref_id": 1,
  "authors": ["Zhang, San", "Li, Si"],
  "title": "Verified Paper Title",
  "year": 2023,
  "venue": "Nature Communications",
  "volume": "14",
  "issue": "1",
  "pages": "1234-1245",
  "doi": "10.1038/s41467-023-xxxxx",
  "type": "journal",
  "enrichment": {
    "crossref_verified": true,
    "pubmed_id": "12345678",
    "citation_count": 156,
    "influential_citations": 23,
    "open_access": true,
    "open_access_pdf": "https://...",
    "mesh_terms": ["Machine Learning", "Genomics"],
    "enrichment_sources": ["crossref", "pubmed", "semantic_scholar"],
    "enrichment_timestamp": "2025-01-01T12:00:00Z"
  },
  "resolution_status": "ENRICHED",
  "raw_text": "[1] ..."
}
```

Regenerate `_references/references.bib` with enriched data.

### Enrichment Statistics

Report to user after enrichment:

```
Metadata Enrichment Complete:
- Total references: 47
- Crossref verified: 38 (81%)
- PubMed matched: 12 (26%)
- Citation data available: 42 (89%)
- Open access PDFs found: 28 (60%)
- Unresolved after enrichment: 5 (11%)
- Conflicts logged: 3

⚠️ 5 references remain unresolved. These will be flagged for manual verification.
Proceed to Module 04 (PDF Download) or Module 05 (Citation Verify)?
```

### Error Handling

| Error | Recovery |
|-------|----------|
| Crossref 429 Too Many Requests | Respect Retry-After header, reduce concurrency |
| Crossref returns empty for a DOI | DOI may be registered with non-Crossref agency; try DataCite |
| PubMed search timeout | Skip PubMed for this reference, note in log |
| Semantic Scholar rate limit (100 req/5min) | Queue remaining references, process in batches |
| Metadata conflict between sources | Prefer Crossref, log conflict, flag for manual review |
