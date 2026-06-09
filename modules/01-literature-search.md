# Module 01: Multi-Source Literature Search

> Discovers academic papers across multiple databases using bilingual queries and evidence-graded search strategies.

## Agent Instructions

You are performing Phase 1 of the literature discovery pipeline. Your goal is to build a comprehensive, deduplicated corpus of relevant papers for the user's research topic.

### Pre-flight Check

Before starting, verify:
- [ ] Pipeline config loaded from `_workspace/pipeline_config.json`
- [ ] Web search is available
- [ ] User has specified the research topic and scope

If any check fails, return to `modules/00-init.md`.

### Input Required from User

Prompt the user for:
1. **Research topic** (required): The core subject to search
2. **Keywords** (required): 3-8 keywords in both Chinese and English
3. **Time range** (optional, default: last 5 years)
4. **Target databases** (optional, default: all available)
5. **Search depth**: Quick (10-20 papers) / Standard (30-50) / Comprehensive (50-100+)

### Execution Workflow

#### Step 1: Construct Bilingual Search Queries

For EACH research sub-topic, create paired queries:

**English queries** (for international databases):
```
"[topic keyword]" AND ("survey" OR "review" OR "systematic review") [year range]
"[specific method]" [year range]
"[topic]" benchmark comparison [year range]
```

**Chinese queries** (for Chinese databases):
```
"[中文关键词]" AND ("综述" OR "进展" OR "研究现状") [年份范围]
"[具体方法]" [年份范围]
```

#### Step 2: Multi-Source Search Execution

Execute searches across available sources in priority order:

**Tier 1 — High-quality academic sources (always search):**

| Source | Method | Scope |
|--------|--------|-------|
| arXiv | MCP tool or API: `http://export.arxiv.org/api/query?search_query=all:{query}&max_results=25` | CS, Math, Physics preprints |
| Semantic Scholar | API: `https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=20` | Cross-disciplinary, citation counts |
| PubMed | API: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}` | Biomedical |
| Crossref | API: `https://api.crossref.org/works?query={query}&select=DOI,title,author,published&rows=20` | Cross-disciplinary DOI metadata |

**Tier 2 — Enhanced sources (search if available):**

| Source | Method | Scope |
|--------|--------|-------|
| Metaso Academic | MCP: `metaso_web_search(query, scope="paper", size=20, includeSummary=true)` | Chinese journals, theses, strong for Chinese-language papers |
| Metaso Documents | MCP: `metaso_web_search(query, scope="document", size=15)` | Technical reports, white papers |
| Metaso Expert Q&A | MCP: `metaso_chat(query)` | Quick domain orientation (NOT citable directly) |
| Google Scholar | Via web search or SerpAPI | Broad coverage |

**Tier 3 — Specialized sources (search when relevant):**

| Source | When to Use |
|--------|------------|
| IEEE Xplore | Engineering, CS, telecommunications |
| ACM Digital Library | Computer science |
| Web of Science | High-impact journals (if institutional access) |
| Scopus | Broad journal coverage (if institutional access) |
| CNKI (知网) | Chinese academic papers (requires browser automation) |
| DBLP | Computer science bibliography |

#### Step 3: Deduplication

After collecting results from all sources:

1. Normalize titles (lowercase, strip punctuation, remove trailing periods)
2. Match on DOI first (exact match = same paper)
3. Match on title similarity (Levenshtein distance < 5 after normalization = likely same paper)
4. When duplicates found: merge metadata, keep all source URLs, prefer the version with DOI

#### Step 4: Evidence Grading

Classify each discovered paper:

| Grade | Criteria | Action |
|-------|----------|--------|
| **Strong** | Peer-reviewed journal, high citation count (>50), from top venue | Must include |
| **Moderate** | Conference paper, moderate citations (10-50), relevant methodology | Include in review |
| **Emerging** | Recent preprint (<2 years), low citations but high relevance | Include if fills a gap |
| **Peripheral** | Tangentially related, low citations | Include only if corpus is small |

#### Step 5: Generate Search Report

Output a structured report to `_workspace/01_search_report.md`:

```markdown
# Literature Search Report

## Search Parameters
- Topic: [topic]
- Date: [date]
- Databases searched: [list]
- Total results: [N] (before dedup) → [M] (after dedup)

## Corpus Summary

### Strong Evidence (N papers)
1. [Author et al., Year] Title. *Venue*. DOI: xxx. Citations: N. [Source]
   - Relevance: [1-sentence relevance note]

### Moderate Evidence (N papers)
...

### Emerging Evidence (N papers)
...

## Search Gaps
- [Areas where few or no papers were found]
- [Databases that could not be searched and why]

## Next Steps
- Proceed to Module 02 (Paper Retrieve) to download PDFs and extract references
- Proceed to Module 03 (Metadata Enrich) to fill missing metadata
```

### Metaso MCP Integration Notes

When Metaso MCP is available, use this enhanced flow:

```
1. metaso_chat(topic) → Get domain overview, identify key concepts
   ⚠️ This output is AI-generated — NEVER cite directly. Use only for orientation.
2. metaso_web_search(topic_zh, scope="paper", size=20, includeSummary=true) → Chinese papers
3. metaso_web_search(topic_en, scope="paper", size=20, includeSummary=true) → English papers
4. metaso_web_search(topic_zh, scope="document", size=15) → Gray literature
5. For high-value URLs from results: metaso_web_reader(url, format="markdown") → Deep reading
```

**Citation tagging**: Mark sources discovered through Metaso as:
- `[metaso-paper]` — from academic paper search
- `[metaso-doc]` — from document search
- `[metaso-topic]` — from curated knowledge base

### Degradation Strategy

If certain search sources are unavailable:
- **No Metaso**: Use general web search with Chinese keywords + "知网" / "万方" as search terms to find Chinese paper metadata pages
- **No arXiv MCP**: Use `http://export.arxiv.org/api/query` directly via HTTP
- **No Semantic Scholar**: Use web search with site:semanticscholar.org
- **No browser automation**: Skip CNKI; note "CNKI not searched — browser automation unavailable" in report
- **No search at all**: Ask user to provide papers manually; proceed from Module 02 with user-provided input

### Quality Gates

Before proceeding to the next module:
- [ ] At least 15 papers discovered (for Standard depth)
- [ ] Deduplication complete
- [ ] Evidence grading applied
- [ ] Search gaps documented
- [ ] Report saved to `_workspace/01_search_report.md`
