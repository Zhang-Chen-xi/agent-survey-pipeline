# Agent Survey Pipeline — Cross-Platform Prompt Set for Academic Survey & Paper Writing

> A collection of agent-readable prompts that guide any AI agent (Claude, GPT, Gemini, Qwen, etc.) to reproduce a battle-tested academic literature survey and paper writing pipeline. Originally built and iterated across 30+ skills on QoderWork, now generalized for cross-platform use.

## What Is This?

This repository contains **no code you run directly** — it contains **instructions your AI agent reads and follows**. Each file in `modules/` is a self-contained prompt that instructs an agent how to execute one stage of the academic research pipeline, from literature discovery through final PDF/DOCX delivery.

The pipeline was refined through real-world use: writing survey papers, managing hundreds of references, verifying citations against Crossref/PubMed, and generating publication-ready documents. It embeds hard-won lessons about AI hallucination in references, PDF extraction edge cases, and academic writing conventions.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT SURVEY PIPELINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 0: Environment Setup                                         │
│  └── modules/00-init.md          → API keys, tools, email config    │
│                                                                      │
│  Phase 1: Literature Discovery                                      │
│  ├── modules/01-literature-search.md  → Multi-source search        │
│  ├── modules/02-paper-retrieve.md     → Reference parsing + PDF    │
│  ├── modules/03-metadata-enrich.md    → Crossref/PubMed enrichment │
│  └── modules/04-pdf-download.md       → Multi-source PDF cascade    │
│                                                                      │
│  Phase 2: Citation Verification                                     │
│  └── modules/05-citation-verify.md    → 6-step anti-hallucination  │
│                                                                      │
│  Phase 3: Knowledge Management                                      │
│  ├── modules/06-knowledge-base.md     → Wiki + BibTeX KB setup     │
│  └── modules/07-paper-ingest.md       → Paper → wiki page          │
│                                                                      │
│  Phase 4: Paper Writing                                             │
│  ├── modules/08-outline.md            → Paper outline generation   │
│  ├── modules/09-literature-review.md  → Survey/review writing      │
│  ├── modules/10-manuscript.md         → Full IMRaD manuscript      │
│  ├── modules/11-rewrite.md            → Draft-based rewriting      │
│  ├── modules/12-polish.md             → Academic language polish   │
│  └── modules/13-stats-analysis.md     → Statistical analysis       │
│                                                                      │
│  Phase 5: Quality & Delivery                                        │
│  ├── modules/14-review.md             → Multi-dim paper review     │
│  ├── modules/15-originality.md        → Originality check          │
│  ├── modules/16-pdf-delivery.md       → PDF generation             │
│  └── modules/17-docx-delivery.md      → DOCX generation            │
│                                                                      │
│  Shared Protocols & Utilities                                       │
│  ├── shared/citation-protocol.md      → Citation verification spec  │
│  ├── shared/anti-hallucination.md     → Anti-fabrication rules      │
│  ├── shared/writing-standards.md      → Academic writing standards  │
│  └── shared/reference-formats.md      → BibTeX/GB-T/APA/IEEE       │
│                                                                      │
│  Agent Entry Points                                                  │
│  ├── survey-agent.md    → Full survey paper end-to-end             │
│  └── paper-agent.md     → General paper writing end-to-end         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### For Human Users

1. **Copy this repository** (or download the `modules/` and `shared/` directories).
2. **Feed the files to your AI agent** — paste the relevant module into your conversation, or point your agent to the directory.
3. **Start with `modules/00-init.md`** — it will prompt you to configure API keys and tools.
4. **Use `survey-agent.md` or `paper-agent.md`** as the top-level orchestrator for end-to-end workflows.

### For Agent Developers

Integrate the prompt modules into your agent system:

- Each `modules/*.md` is a self-contained system prompt for one pipeline stage.
- `shared/*.md` contains cross-cutting protocols referenced by multiple modules.
- `scripts/` contains helper scripts (Python/JS) for BibTeX generation, PDF download, etc.
- The `scripts/` are optional — agents can implement the logic natively or call the scripts.

### Example: Running a Full Survey

```
User: "Write a literature survey on [your topic]"
Agent reads: survey-agent.md → orchestrates all modules in order
Agent prompts user for: API keys, target scope, citation style
Agent executes: search → retrieve → verify → write → deliver
```

## Key Design Principles

**Anti-Hallucination First**: Every citation must pass through a 6-step verification cascade (Crossref API → DOI resolution → metadata matching → author-domain check → deep verification → manual fallback). The pipeline classifies 5 types of AI hallucination and handles each explicitly.

**Prefer Incomplete Over Fake**: When a reference cannot be verified, the pipeline marks it as `[UNVERIFIED]` rather than fabricating plausible-looking metadata. "Rather cite 45 verified papers than 50 with 5 hallucinated."

**Cross-Platform**: No dependency on a specific AI platform. Modules work with Claude (Anthropic), GPT (OpenAI), Gemini (Google), Qwen (Alibaba), DeepSeek, or any agent with web search, file I/O, and code execution capabilities.

**Progressive Enhancement**: Each module checks for optional tools (Metaso MCP, arXiv API, Semantic Scholar, etc.) and degrades gracefully. A basic agent with only web search can still run the pipeline — an agent with full MCP tooling gets better results.

## Repository Structure

| Directory | Purpose | Audience |
|-----------|---------|----------|
| `modules/` | Agent prompt files (one per pipeline stage) | AI Agents |
| `shared/` | Cross-cutting protocols and standards | AI Agents |
| `scripts/` | Helper scripts (Python/JS) | AI Agents |
| `utils/` | Utility templates | AI Agents |
| `survey-agent.md` | Full survey orchestrator prompt | AI Agents |
| `paper-agent.md` | General paper orchestrator prompt | AI Agents |
| `README.md` | This file | Humans |

## Requirements

The agent executing this pipeline needs:

- **Web search** capability (any search API or browser)
- **File I/O** (read/write markdown, JSON, BibTeX, DOCX, PDF)
- **Code execution** (Python 3.8+ and/or Node.js 18+ for helper scripts)
- **Optional**: Metaso MCP, arXiv API access, Semantic Scholar API, Crossref polite pool, browser automation

API keys and configuration are set up interactively via `modules/00-init.md`.

## Citation

If this prompt set contributes to your research workflow, please cite:

```bibtex
@misc{agent-survey-pipeline,
  title  = {Agent Survey Pipeline: Cross-Platform Prompts for Academic Literature Survey and Paper Writing},
  year   = {2025},
  note   = {https://github.com/RainVallo/agent-survey-pipeline}
}
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
