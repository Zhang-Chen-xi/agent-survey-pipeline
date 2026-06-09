# Environment Initialization

> This module MUST be executed first before any other pipeline module. It ensures all required tools, API keys, and configurations are in place.

## Agent Instructions

When starting a new pipeline session, you MUST perform the following initialization sequence. **Do NOT hardcode any API keys, email addresses, or personal information.** All values must be obtained from the user at runtime.

### Step 1: Check Runtime Capabilities

Verify the following capabilities are available. For each missing capability, inform the user and suggest how to enable it.

**Required Capabilities:**

| Capability | How to Check | Fallback |
|-----------|-------------|----------|
| Web Search | Test with a simple query | Ask user to enable web search or provide API key |
| File I/O | Test writing a temp file | Use in-memory storage (limited) |
| Code Execution | Test `python3 --version` or `node --version` | Ask user to install Python 3.8+ or Node.js 18+ |

**Optional Capabilities (check and report availability):**

| Capability | How to Check | Benefit |
|-----------|-------------|--------|
| Metaso MCP | Check if `metaso_web_search` tool exists | Chinese academic search, document search |
| arXiv MCP | Check if `arxiv` MCP tools exist | Preprint search and metadata |
| Semantic Scholar | Test API (no key needed, rate limited) | Citation counts, paper metadata |
| Crossref API | Test DOI lookup | Reference verification, metadata enrichment |
| Browser Automation | Check if Playwright/browser tools exist | CNKI search, paywalled content |
| LibreOffice | Test `soffice --version` | PDF conversion from DOCX |
| pandoc | Test `pandoc --version` | Document format conversion |
| poppler-utils | Test `pdftotext -v` | PDF text extraction |

### Step 2: Collect User Configuration

**You MUST prompt the user for the following values. NEVER assume, hardcode, or reuse values from previous sessions.**

#### 2a. Crossref Polite Pool Email (Recommended)

If user provides an email, store it as `CROSSREF_MAILTO`. If skipped, use anonymous access at 2 req/s.

#### 2b. Search Engine Configuration

Check if the user's environment has specific search APIs configured.

#### 2c. Citation Style Default

Options: GB/T 7714-2015, APA 7th Edition, IEEE, Chicago 17th Edition, Other.

#### 2d. Working Language

Options: Chinese, English, Bilingual.

#### 2e. Output Directory

Default: ./output/

### Step 3: Create Working Directory Structure

```
{output_dir}/
├── _workspace/
├── _references/
├── _pdfs/
├── _wiki/
├── _delivery/
└── _logs/
```

### Step 4: Save Configuration

Save as `{output_dir}/_workspace/pipeline_config.json`.

### Step 5: Dependency Installation (If Needed)

Python: pdfplumber, pypdf, reportlab, bibtexparser, requests
Node.js: docx, bibtex-js

### Step 6: Smoke Test

Verify pipeline is functional.

## Error Recovery

- Search unavailable: Inform user
- No code execution: Text-only workflow
- Write access denied: Ask user for writable directory
- Crossref API timeout: Use anonymous access

## Security Notes

- NEVER log, echo, or store API keys in output files
- NEVER include email addresses in generated documents
- NEVER hardcode credentials in scripts
