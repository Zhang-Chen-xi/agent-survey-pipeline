# Module 02: Paper Retrieval & Reference Parsing

> Extracts structured references from paper text/PDFs, resolves them to DOIs, and prepares for metadata enrichment.

## Agent Instructions

You are performing reference extraction — converting raw paper text into a structured, machine-readable reference list.

### Pre-flight Check

- [ ] Search report available at `_workspace/01_search_report.md`
- [ ] At least one paper PDF or full text available
- [ ] Pipeline config loaded

### Input Sources

Accept references from:
1. **PDF files** — Extract text first using `pdftotext -layout paper.pdf paper.txt` or pdfplumber
2. **Plain text / Markdown** — Direct parsing
3. **User-pasted reference lists** — Direct parsing
4. **DOCX files** — Convert to text first via pandoc: `pandoc paper.docx -t plain -o paper.txt`

### Reference Parsing Pipeline

#### Step 1: Locate the References Section

Identify the reference section using these heuristics:
- Section titled "References", "Bibliography", "Works Cited", or Chinese equivalents ("参考文献", "引用文献")
- Usually the last major section before appendices
- Contains numbered entries `[1]`, `[2]`... or author-year entries `Smith et al. (2020)`

#### Step 2: Parse Individual References

Support TWO reference formats:

**Format A — Numbered references** (common in IEEE, GB/T 7714):
```
[1] Author A, Author B, Author C. Title of the paper[J]. Journal Name, 2020, 15(3): 123-145.
[2] Author D, Author E. Conference Paper Title[C]//Proceedings of XYZ. 2021: 456-467.
```

**Format B — Author-year references** (common in APA, Chicago):
```
Smith, J. A., & Doe, B. C. (2020). Title of the paper. Journal Name, 15(3), 123-145.
```

For EACH reference, extract:

| Field | Required | Notes |
|-------|----------|-------|
| `ref_id` | Yes | Sequential number or author-year key |
| `authors` | Yes | List of author names |
| `title` | Yes | Full paper title |
| `year` | Yes | Publication year |
| `venue` | Yes | Journal name, conference name, or "arXiv preprint" |
| `volume` | No | Journal volume |
| `issue` | No | Journal issue |
| `pages` | No | Page range |
| `doi` | No | If present in text |
| `url` | No | If present in text |
| `type` | Yes | journal / conference / book / thesis / preprint / report |
| `raw_text` | Yes | Original reference text verbatim |

#### Step 3: DOI Resolution Attempts

For references WITHOUT a DOI in the original text, attempt resolution:

1. **Crossref API** (primary):
   ```
   GET https://api.crossref.org/works?query.title={url_encoded_title}&query.author={first_author}&select=DOI,title,author&rows=1
   ```
   - Match if: returned title similarity > 0.85 AND first author matches
   - Add `mailto={CROSSREF_MAILTO}` header if configured (for polite pool rate limits)

2. **Semantic Scholar API** (secondary):
   ```
   GET https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=1&fields=title,externalIds,authors
   ```
   - Extract DOI from `externalIds.DOI`

3. **arXiv search** (for preprints):
   ```
   GET http://export.arxiv.org/api/query?search_query=ti:"{title}"&max_results=1
   ```
   - Extract arXiv ID, construct URL: `https://arxiv.org/abs/{arxiv_id}`

4. **Mark as unresolved** if all attempts fail:
   ```json
   { "doi": null, "resolution_status": "UNRESOLVED", "resolution_note": "Could not resolve via Crossref/S2/arXiv" }
   ```

#### Step 4: Output Structured Reference List

Save to `_workspace/02_references.json`:

```json
{
  "source_paper": "paper_title",
  "extraction_date": "2025-01-01",
  "total_references": 47,
  "resolved_doi": 38,
  "unresolved": 9,
  "references": [
    {
      "ref_id": 1,
      "authors": ["Zhang, S.", "Li, X."],
      "title": "Example Paper Title",
      "year": 2023,
      "venue": "Nature Communications",
      "volume": "14",
      "pages": "1234-1245",
      "doi": "10.1038/s41467-023-xxxxx",
      "type": "journal",
      "resolution_status": "RESOLVED",
      "raw_text": "[1] Zhang S, Li X. Example Paper Title..."
    }
  ]
}
```

#### Step 5: Generate BibTeX (Preliminary)

Convert the JSON references to BibTeX format and save to `_references/references.bib`.

Use these entry types:
- `@article` for journal papers
- `@inproceedings` for conference papers
- `@book` for books
- `@phdthesis` / `@mastersthesis` for theses
- `@misc` for preprints, reports, web resources

**BibTeX key format**: `{first_author_last}{year}{first_word_of_title}`
Example: `zhang2023example`

### Handling Chinese References

Chinese references (GB/T 7714 format) require special handling:

```
[1] 张三, 李四. 中文论文标题[J]. 期刊名称, 2023, 45(2): 100-110.
```

- Preserve original Chinese characters in title, authors, venue
- Add pinyin transliteration for BibTeX keys: `zhangsan2023zhongwen`
- Search CNKI (if browser available) or Metaso for DOI resolution
- Mark as `language = {zh}` in BibTeX

### Error Handling

| Error | Recovery |
|-------|----------|
| PDF extraction garbled | Try alternative extraction (pdfplumber vs pdftotext) |
| Reference format unrecognized | Save raw text, mark as `PARSE_FAILED`, ask user for help |
| Crossref API timeout | Retry once, then fall back to Semantic Scholar |
| DOI resolution conflict | Prefer Crossref result, note alternative in log |
| >30% references unresolved | Warn user: "High unresolved rate may indicate non-standard citation format" |

### Quality Gates

- [ ] All references parsed into structured format
- [ ] DOI resolution attempted for all entries
- [ ] BibTeX file generated
- [ ] Parse success rate > 80% (flag if lower)
- [ ] Output saved to `_workspace/02_references.json` and `_references/references.bib`
