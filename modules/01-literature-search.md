# Module 01: Multi-Source Literature Search

> Discovers academic papers across multiple databases using bilingual queries and evidence-graded search strategies.

## Agent Instructions

You are performing Phase 1 of the literature discovery pipeline. Your goal is to build a comprehensive, deduplicated corpus of relevant papers for the user's research topic.

### Pre-flight Check

- [ ] Pipeline config loaded from `_workspace/pipeline_config.json`
- [ ] Web search is available
- [ ] User has specified the research topic and scope

### Input Required from User

1. **Research topic** (required)
2. **Keywords** (required): 3-8 keywords in both Chinese and English
3. **Time range** (optional, default: last 5 years)
4. **Target databases** (optional, default: all available)
5. **Search depth**: Quick (10-20 papers) / Standard (30-50) / Comprehensive (50-100+)

### Execution Workflow

#### Step 1: Construct Bilingual Search Queries

Create paired English and Chinese queries for each sub-topic.

#### Step 2: Multi-Source Search Execution

**Tier 1**: arXiv, Semantic Scholar, PubMed, Crossref
**Tier 2**: Metaso Academic/Documents, Google Scholar
**Tier 3**: IEEE Xplore, ACM DL, Web of Science, Scopus, CNKI, DBLP

#### Step 3: Deduplication

Normalize titles, match on DOI and title similarity.

#### Step 4: Evidence Grading

Strong / Moderate / Emerging / Peripheral

#### Step 5: Generate Search Report

Output to `_workspace/01_search_report.md`

### Degradation Strategy

Graceful fallbacks for unavailable sources.

### Quality Gates

- [ ] At least 15 papers discovered
- [ ] Deduplication complete
- [ ] Evidence grading applied
- [ ] Search gaps documented
