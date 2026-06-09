# Module 04: Multi-Source PDF Download

> Downloads paper PDFs using a priority cascade across 10+ sources, with intelligent retry and fallback.

## Agent Instructions

You are downloading PDFs for all references in the enriched reference list. The goal is to maximize download success rate while respecting access restrictions.

### Pre-flight Check

- [ ] `_workspace/02_references.json` exists with enrichment data
- [ ] Output directory `_pdfs/` exists and is writable
- [ ] Pipeline config loaded

### Download Priority Cascade

For EACH reference that needs a PDF, attempt sources in this order. Move to the next source only when the current one fails.

**Tier 1 — Direct open access (no authentication):**

| Priority | Source | URL Pattern | Condition |
|----------|--------|-------------|-----------|
| 1 | arXiv | `https://arxiv.org/pdf/{arxiv_id}.pdf` | Has arXiv ID |
| 2 | PubMed Central | `https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/` | Has PMC ID and is OA |
| 3 | Open Access PDF (from enrichment) | `enrichment.open_access_pdf` URL | Found during enrichment |
| 4 | Publisher OA | `https://doi.org/{doi}` → follow redirect to PDF | DOI resolves to OA paper |
| 5 | Unpaywall | `https://api.unpaywall.org/v2/{doi}?email={CROSSREF_MAILTO}` | Has DOI |

**Tier 2 — Institutional/preprint mirrors:**

| Priority | Source | URL Pattern | Condition |
|----------|--------|-------------|-----------|
| 6 | Semantic Scholar | PDF link from S2 API | S2 has PDF |
| 7 | DBLP | `https://dblp.org/search/publ/api?q={title}` → extract PDF link | CS papers |
| 8 | ResearchGate / Academia | Via web search: `"{title}" filetype:pdf` | General |
| 9 | University repository | Via web search: `"{title}" site:.edu pdf` | General |

**Tier 3 — Browser-based fallback (if browser automation available):**

| Priority | Source | Method | Condition |
|----------|--------|--------|-----------|
| 10 | CNKI | Browser automation on cnki.net | Chinese papers |
| 11 | Google Scholar PDF | Search Scholar, click [PDF] link | General |
| 12 | Publisher page | Navigate to DOI landing page, look for PDF link | Has DOI |

### Download Execution

For each source attempt:

```python
# Pseudocode
def download_pdf(reference, source):
    url = construct_url(reference, source)
    
    # Safety checks
    assert is_safe_url(url)  # No file://, no javascript:, no data:
    assert not is_private_ip(url)  # No 10.x, 172.x, 192.168.x
    
    response = http_get(url, timeout=30, follow_redirects=True)
    
    if response.status == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'pdf' in content_type or response.content[:5] == b'%PDF-':
            filename = sanitize_filename(reference)
            save_to(f'_pdfs/{filename}.pdf', response.content)
            return DownloadResult(success=True, source=source, path=filename)
    
    return DownloadResult(success=False, source=source, error=response.status)
```

### File Naming Convention

```
{first_author_last}_{year}_{first_title_word}.pdf
```

Examples:
- `zhang_2023_example.pdf`
- `smith_2022_attention.pdf`

For Chinese author names, use pinyin: `zhangsan_2023_yanjiu.pdf`

**Sanitization rules:**
- Lowercase
- Replace spaces with underscores
- Remove special characters except hyphens
- Truncate to 80 characters max
- Handle filename collisions by appending `_2`, `_3`, etc.

### Batch Download Strategy

For efficiency, process references in batches:

1. **Batch A — High confidence** (has DOI + OA indicator): Download first, highest success rate
2. **Batch B — Medium confidence** (has DOI, no OA indicator): Download with full cascade
3. **Batch C — Low confidence** (no DOI): Web search only, lower success rate expected

Run batches sequentially. Within each batch, download sequentially to respect rate limits.

### Progress Tracking

Report progress after each batch:

```
PDF Download Progress:
Batch A (High confidence): 25/28 downloaded (89%)
Batch B (Medium confidence): 8/12 downloaded (67%)
Batch C (Low confidence): 2/7 downloaded (29%)

Total: 35/47 downloaded (74%)

Failed downloads:
- [ref_id] Author et al. "Title" — All sources exhausted
- [ref_id] Author et al. "Title" — Paywalled, no OA version found
```

### Missing PDF Document Generation

For references where ALL download sources fail, generate a placeholder Word document:

Save to `_pdfs/MISSING_{ref_id}.docx` containing:

```
MISSING PAPER INFORMATION

Reference: [ref_id]
Title: {title}
Authors: {authors}
Year: {year}
Venue: {venue}
DOI: {doi or "Not available"}

Download Status: FAILED
Sources Attempted: [list all attempted sources and their failure reasons]

Suggested Actions:
1. Access via institutional library subscription
2. Request from authors via ResearchGate
3. Check if the paper is available through inter-library loan
4. Search for the paper on the publisher's website directly

Generated: {timestamp}
```

### Safety Rules

1. **URL safety**: Only download from HTTP/HTTPS URLs. Reject `file://`, `javascript:`, `data:` schemes.
2. **No private IPs**: Reject URLs pointing to `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`, `127.x.x.x`, `localhost`.
3. **Content verification**: Verify the downloaded file starts with `%PDF-` magic bytes.
4. **File size limits**: Reject files > 200MB (likely not a paper) or < 1KB (likely an error page).
5. **No credential stuffing**: Never append user credentials to URLs.
6. **Rate limiting**: Add 500ms delay between downloads from the same domain.
7. **Respect robots.txt**: For Tier 2/3 sources, check robots.txt before downloading.

### Output

Save download manifest to `_workspace/04_download_manifest.json`:

```json
{
  "total_references": 47,
  "downloaded": 35,
  "failed": 12,
  "success_rate": "74%",
  "downloads": [
    {
      "ref_id": 1,
      "filename": "zhang_2023_example.pdf",
      "source": "arxiv",
      "size_bytes": 1234567,
      "verified_pdf": true
    }
  ],
  "failed_references": [
    {
      "ref_id": 5,
      "title": "Paywalled Paper",
      "attempted_sources": ["publisher", "unpaywall", "semantic_scholar", "web_search"],
      "failure_reasons": ["403 Forbidden", "No OA version", "No PDF link", "No results"]
    }
  ]
}
```

### Quality Gates

- [ ] Download manifest saved
- [ ] All downloaded files verified as valid PDFs
- [ ] Missing paper documents generated for failures
- [ ] Success rate reported to user
- [ ] Failed references clearly documented with recovery suggestions
