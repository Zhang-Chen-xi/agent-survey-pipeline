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
|-----------|-------------|---------|
| Metaso MCP | Check if `metaso_web_search` tool exists | Chinese academic search, document search |
| arXiv MCP | Check if `arxiv` MCP tools exist | Preprint search and metadata |
| Semantic Scholar | Test API (no key needed, rate limited) | Citation counts, paper metadata |
| Crossref API | Test DOI lookup | Reference verification, metadata enrichment |
| Browser Automation | Check if Playwright/browser tools exist | CNKI search, paywalled content |
| LibreOffice | Test `soffice --version` | PDF conversion from DOCX |
| pandoc | Test `pandoc --version` | Document format conversion |
| poppler-utils | Test `pdftotext -v` | PDF text extraction |

**Report to User:**
```
Pipeline Environment Check:
✅ Web Search — available
✅ File I/O — available
✅ Python 3.x — available
✅ Crossref API — available (polite pool)
⚠️ Metaso MCP — not available (Chinese academic search limited)
⚠️ arXiv MCP — not available (using web fallback)
⚠️ LibreOffice — not installed (DOCX→PDF conversion unavailable)
❌ Browser Automation — not available (CNKI search disabled)
```

### Step 2: Collect User Configuration

**You MUST prompt the user for the following values. NEVER assume, hardcode, or reuse values from previous sessions.**

#### 2a. Crossref Polite Pool Email (Recommended)

```
To use the Crossref API at higher rate limits (10 req/s instead of 2 req/s),
please provide an email address for the Crossref Polite Pool.
This email is sent ONLY to Crossref's API as an identifier — it is not
stored, shared, or used for any other purpose.

Email (or press Enter to skip and use anonymous rate limits):
```

If user provides an email, store it as `CROSSREF_MAILTO`. If skipped, use anonymous access at 2 req/s.

#### 2b. Search Engine Configuration

Check if the user's environment has specific search APIs configured:

```
The pipeline uses web search for literature discovery. Current setup:
- [Auto-detected search tools]

Do you have any of the following? (select all that apply)
1. Semantic Scholar API key (for higher rate limits)
2. Google Scholar access via SerpAPI or similar
3. Institutional access to Web of Science / Scopus
4. None — use default web search
```

#### 2c. Citation Style Default

```
What citation style should the pipeline use by default?
1. GB/T 7714-2015 (Chinese national standard)
2. APA 7th Edition
3. IEEE
4. Chicago 17th Edition
5. Other (specify)
```

#### 2d. Working Language

```
What is the primary language for the output document?
1. Chinese (简体中文)
2. English
3. Bilingual (Chinese primary, English abstract)
```

#### 2e. Output Directory

```
Where should pipeline outputs be saved?
Default: ./output/
Custom path:
```

### Step 3: Create Working Directory Structure

```
{output_dir}/
├── _workspace/          # Working files
├── _references/         # BibTeX and reference files
├── _pdfs/               # Downloaded PDFs
├── _wiki/               # Knowledge base wiki pages
├── _delivery/           # Final output documents
└── _logs/               # Pipeline execution logs
```

Create this structure and verify write access.

### Step 4: Save Configuration

Save the collected configuration as `{output_dir}/_workspace/pipeline_config.json`:

```json
{
  "crossref_mailto": "<user-provided or empty>",
  "citation_style": "gbt7714|apa7|ieee|chicago17",
  "language": "zh|en|bilingual",
  "output_dir": "<path>",
  "capabilities": {
    "web_search": true,
    "metaso_mcp": false,
    "arxiv_mcp": false,
    "browser": false,
    "libreoffice": false,
    "pandoc": false,
    "poppler": false
  },
  "session_started": "<ISO-8601 timestamp>"
}
```

**IMPORTANT**: This config file contains ONLY the user's explicit choices. No API keys are stored in plain text. If API keys are needed at runtime, obtain them from environment variables or prompt the user again.

### Step 5: Dependency Installation (If Needed)

If optional scripts are used, ensure dependencies are available:

**Python packages:**
```bash
pip install pdfplumber pypdf reportlab bibtexparser requests
```

**Node.js packages:**
```bash
npm install docx bibtex-js
```

**System packages (if available):**
```bash
# Debian/Ubuntu
sudo apt-get install poppler-utils pandoc libreoffice
```

Only install what's actually needed for the current pipeline run. Ask the user before installing system packages.

### Step 6: Smoke Test

Run a minimal test to verify the pipeline is functional:

1. Search for a known paper (e.g., "Attention Is All You Need" on arXiv)
2. Verify the Crossref API responds (if configured)
3. Write and read back a test file
4. Report success/failure to user

```
Pipeline initialization complete.
✅ Search: working
✅ Crossref API: working (polite pool)
✅ File I/O: working
✅ Configuration saved

Ready to proceed. What would you like to work on?
```

## Error Recovery

If initialization fails at any step:
- **Search unavailable**: Inform user that literature discovery will be limited. Suggest they provide papers manually.
- **No code execution**: Inform user that BibTeX generation and PDF processing will be limited. Offer to do text-only workflow.
- **Write access denied**: Ask user for a writable directory.
- **Crossref API timeout**: Proceed with anonymous access (slower but functional).

## Security Notes

- NEVER log, echo, or store API keys in output files
- NEVER include email addresses in generated documents (Crossref mailto is sent only in API headers)
- NEVER hardcode credentials in scripts — always pass via environment variables or runtime config
- If a script requires an API key, prompt the user at the moment of need, not during init
