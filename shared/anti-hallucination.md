# Anti-Hallucination Rules

> Cross-cutting protocol for preventing, detecting, and handling AI hallucination in academic writing.

## Core Principle

**"Rather cite 45 verified papers than 50 with 5 hallucinated."**

## Rules for Writing Modules

### Rule 1: No Citation Without Verification
Before writing ANY citation `\cite{bibkey}` or `[N]`:
1. Confirm `bibkey` exists in `_references/references.bib`
2. Confirm the entry has `resolution_status: VERIFIED` or `CORRECTED`
3. If not found or not verified, write `[CITATION NEEDED]` instead

### Rule 2: No Invented Statistics
Before writing ANY numerical claim:
1. Confirm the number comes from a verified source (paper, database, official statistic)
2. If the exact number is unavailable, use qualitative language:
   - ✅ "Studies have shown significant improvement"
   - ❌ "Studies show a 73.2% improvement" (unless verified)

### Rule 3: No Invented Methodology Details
Before describing ANY method:
1. Confirm details come from the paper's wiki page or verified abstract
2. If details are uncertain, cite the paper but describe only what is confirmed

### Rule 4: No Invented Quotes
NEVER create fake quotes attributed to papers. Only quote text you have actually read from the source.

### Rule 5: Transparent Uncertainty
When uncertain about a claim:
- Use hedging: "appears to", "has been reported to", "according to [author]"
- Add verification note: `[VERIFICATION NEEDED: claim about X]`
- Never present uncertain information as established fact

## Detection Checklist

After writing any section, self-check:

- [ ] Every `\cite{}` / `[N]` maps to a verified BibTeX entry
- [ ] No statistics without source attribution
- [ ] No methodology claims not found in cited papers
- [ ] No quotes that I cannot trace to a source
- [ ] No "perfect" papers that conveniently support every claim (possible confirmation bias)
- [ ] Contradictory evidence acknowledged where it exists

## Handling [CITATION NEEDED] Placeholders

At the end of each writing session:
1. Collect all `[CITATION NEEDED]` markers
2. For each, search for a real verified paper that could fill the gap
3. If found: add to references, verify, and replace the placeholder
4. If not found: flag for user attention in the Writing Notes section
5. Never silently remove a placeholder — either replace it or keep the flag

## Post-Writing Audit

After completing the full manuscript:
1. Extract all citations
2. Cross-check against `_workspace/05_verification_report.md`
3. Flag any citation that was added after verification (needs re-verification)
4. Run Module 05 verification cascade on any new references
5. Report final citation statistics:
   ```
   Citation Audit:
   - Total citations: N
   - Pre-verified: N (X%)
   - Newly added and verified: N
   - Unverified: N (flagged for review)
   - Removed hallucinations: N
   ```
