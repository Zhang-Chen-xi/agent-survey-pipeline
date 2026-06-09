# Pipeline Utilities

This directory contains utility templates and configuration examples for the Agent Survey Pipeline.

## Configuration Templates

### runtime.conf.example

```ini
# Agent Survey Pipeline Runtime Configuration
# Copy this file to runtime.conf and fill in your values

[crossref]
# Email for Crossref Polite Pool (higher rate limits)
# Leave empty for anonymous access (2 req/s)
mailto = 

[search]
# Semantic Scholar API key (optional, for higher rate limits)
# Get one at: https://www.semanticscholar.org/product/api#api-key-form
s2_api_key = 

[output]
# Default output directory
output_dir = ./output
# Default citation style: gbt7714 | apa7 | ieee | chicago17
citation_style = gbt7714
# Default language: zh | en | bilingual
language = zh

[tools]
# Paths to optional tools (auto-detected if in PATH)
pandoc = pandoc
soffice = soffice
pdftotext = pdftotext
```

## Agent Integration Notes

### For Claude (Anthropic)
- Load module files as system prompts or initial messages
- Use Artifacts for document output
- Leverage web search for literature discovery

### For GPT (OpenAI)
- Use system messages for module instructions
- Use code interpreter for script execution
- Use browsing for Metaso/web search fallback

### For Gemini (Google)
- Use system instructions for module prompts
- Leverage Google Scholar integration naturally
- Use code execution for scripts

### For Qwen (Alibaba)
- Strong Chinese academic search capabilities
- Leverage built-in search for CNKI content
- Use Metaso MCP if available

### For Any Agent
- Each module in `modules/` is self-contained
- `shared/` protocols should be loaded alongside any module that handles citations
- Scripts in `scripts/` are optional — agents can implement the logic natively
