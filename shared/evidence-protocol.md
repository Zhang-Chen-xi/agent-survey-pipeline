# Evidence & Permission Protocol

> Cross-cutting protocol (v2.0) referenced by `citation-protocol.md`, Modules 05, 09, and both orchestrator entry points (`survey-agent.md`, `paper-agent.md`). Defines how full-text evidence is graded, how identifiers are bound to papers, how external actions are gated, and how failures must be reported.

## Protocol Version: 2.0

This document is the single source of truth for the **evidence layer** of the pipeline. Citation *identity* verification is governed by `citation-protocol.md`; this protocol governs what may be asserted *about* a paper and what the agent is allowed to *do*.

## 1. Three-State Separation

Three independent states must never be conflated:

| State | Question it answers | Established by |
|-------|--------------------|--------------------|
| Identity verification | Is this a real paper with correct metadata? | 6-step cascade (`citation-protocol.md`) |
| Full-text availability | Do we actually possess the full text locally? | Download manifest + file existence + non-empty extraction |
| Claim support | Does the source actually support this specific statement? | Evidence grading below (A/B/C) |

A `VERIFIED` paper whose full text was never retrieved does **not** support an A-grade claim. A PDF file that exists on disk but yields no extractable text is **not** available full text.

## 2. Evidence Grades for Claims

Every load-bearing claim in a draft must be traceable to one of:

| Grade | Requirement | Strength |
|-------|-------------|----------|
| **A** | Quoted verbatim from retrieved full text, with a locator (page / section / paragraph) | Strong — may state the claim as supported |
| **B** | Taken from the official publisher/indexer abstract only | Medium — claim must be weakened to what the abstract literally says |
| **C** | Cross-citation: a verified paper mentions the target, but we have not read either the full text or the official abstract | Weak — label as reported-by-source; never present as confirmed fact |

Hard rules:

1. **Critical claims require grade A.** A claim flagged `critical: true` (central result, quantitative conclusion, priority/novelty assertion) may not rest on B or C evidence — retrieve the full text or omit/rephrase the claim.
2. **B-grade evidence must carry an `Abstract` locator**, so the reader can see the claim never left the abstract.
3. Quotes must be verbatim and must actually appear in the retrieved text file (grep-checkable). A paraphrase is not a quote.
4. Evidence files must live inside the designated evidence directory; never reference paths outside it.

## 3. Identifier Binding Verification

API metadata is not trustworthy on its own. Before accepting DOI / PMID / PMCID / arXiv-ID from any search or enrichment endpoint, confirm the identifier belongs to **the paper being described**, not to a paper it references.

Known trap (observed in the wild): a PubMed parsing path that walks all `ArticleId` elements of a record can overwrite the correct title's DOI/PMC with identifiers of articles listed in its reference list. Rule: every identifier that will be written into the unified record must be independently confirmed (resolve the DOI and compare titles, or cross-check PMID against the publisher page). Unconfirmed identifiers are kept as `pending` clues, never as verified fields.

## 4. Permission Gates

Six named permissions control all external or destructive side effects. They live in `review_config.json` as booleans and default to **false**:

```json
{
  "external_submission": false,
  "background_monitor": false,
  "connector_changes": false,
  "browser_control": false,
  "dependency_install": false,
  "library_write": false
}
```

Rules:

1. **Silence is not consent.** A user not objecting does not grant a permission; only an explicit affirmative does.
2. **No idle-timeout auto-proceed.** Waiting for an answer never turns into "assume yes and act".
3. Granting one action is not a standing grant. Publication/submission to any external service additionally requires a **public-disclosure warning**: once pushed, content may be cached or indexed and cannot be fully retracted.
4. Before any gated action, re-state which permission is being used and for what exact operation.

## 5. Conservative Failure Policy

Failures must degrade toward "unknown", never toward a fabricated success or a false accusation:

- Network error, timeout, or no-match in verification → status `error` or `unverified`, **never** evidence that the paper is fabricated.
- HTTP 200 on a landing page is not identity verification; metadata must still match.
- Never delete or drop a candidate reference because of a low citation count; citation count is popularity, not validity.
- Partial results are preserved on failure — do not delete or overwrite existing outputs when a run fails; write to a new versioned path instead.
- Length-limited API responses (e.g., truncated full text) must be recorded in `degradation_log`, not silently treated as complete.

## 6. Unified Literature Record (v2 schema)

All modules exchange literature through one envelope:

```json
{
  "schema_version": "2.0",
  "papers": [
    {
      "paper_id": "p_0001",
      "title": "...", "authors": [], "year": 2024, "venue": "...",
      "doi": null, "pmid": null, "arxiv_id": null,
      "abstract": "...",
      "url": "...", "source": "...",
      "verification_status": "pending",
      "sources": [],
      "fulltext_status": "none",
      "fulltext_path": null,
      "tags": [], "notes": ""
    }
  ],
  "search_queries_used": [],
  "degradation_log": []
}
```

`paper_id` is the stable internal key: assigned once, never recycled, and referenced by citations, evidence records, and wiki pages.

## 7. Citation Placeholders

Drafts cite with `{REF:paper_id}` placeholders, not hand-written numbers. Final numbering is compiled at the source-markdown level immediately before DOCX/PDF rendering; any placeholder whose `paper_id` is unknown to the pool **must fail the build**, not be dropped silently.

## 8. Scope Honesty

This protocol grounds PRISMA-S-style reporting discipline (documented searches, provenance, degradation logs) but does **not** claim to be a full systematic-review engine. If the user asks for a systematic review, meta-analysis, or protocol registration, say what this pipeline does and does not cover before starting.
