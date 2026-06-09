# Module 08: Paper Outline Generation

> Generates a structured paper outline based on the research topic, literature corpus, and user requirements.

## Agent Instructions

You are creating the structural blueprint for a paper. This outline will guide all subsequent writing modules.

### Pre-flight Check

- [ ] Literature search complete (`_workspace/01_search_report.md`)
- [ ] Citation verification complete (`_workspace/05_verification_report.md`)
- [ ] Knowledge base has ingested papers (recommended but not required)
- [ ] User has specified paper type and scope

### Input Required from User

```
To generate the paper outline, I need:
1. Paper type: Survey/Review / Research Paper / Thesis Chapter / Conference Paper
2. Target venue: [Journal/Conference name, or "General"]
3. Target length: [word count or page count]
4. Key arguments or themes you want to emphasize: [optional]
5. Any specific sections required by the venue: [optional]
```

### Outline Generation Workflow

#### Step 1: Analyze Literature Corpus

From the verified references and wiki pages:
1. Identify major themes and clusters
2. Map chronological development
3. Find consensus areas and debate areas
4. Identify research gaps

#### Step 2: Determine Structure Template

**Survey/Review Paper:**
```
1. Introduction (10%)
   - Motivation and significance
   - Scope and contribution
   - Paper organization
2. Background / Preliminaries (10%)
   - Key definitions
   - Foundational concepts
3. Taxonomy / Classification (10%)
   - Proposed categorization of approaches
4. Main Theme 1 (15%)
   - Sub-approach A
   - Sub-approach B
   - Comparison and discussion
5. Main Theme 2 (15%)
   ...
6. Main Theme N (15%)
   ...
7. Cross-cutting Analysis (10%)
   - Benchmark comparison
   - Common challenges
8. Open Problems and Future Directions (10%)
9. Conclusion (5%)
```

**Research Paper (IMRaD):**
```
1. Introduction (15%)
   - Problem statement
   - Motivation
   - Contributions (3-4 bullet points)
2. Related Work (15%)
   - Grouped by approach category
3. Methodology (25%)
   - Overview
   - Component 1
   - Component 2
   - Algorithm/Procedure
4. Experiments (25%)
   - Setup (datasets, baselines, metrics)
   - Main results
   - Ablation studies
   - Case studies
5. Discussion (10%)
   - Limitations
   - Broader impact
6. Conclusion (10%)
```

#### Step 3: Populate Outline with Literature

For each section, assign:
- Which references will be cited
- Key arguments to make
- Figures/tables to include
- Estimated word count

Save to `_workspace/08_outline.md`:

```markdown
# Paper Outline: {Working Title}

## Metadata
- Type: {survey|research|thesis}
- Target: {venue}
- Length: {target words}
- Citation style: {style}

## Section 1: Introduction (~{N} words)
### 1.1 Motivation
- {key point} [cite: bibkey1, bibkey2]
- {key point} [cite: bibkey3]
### 1.2 Scope and Contribution
- Contribution 1: ...
- Contribution 2: ...
### 1.3 Organization
- "Section 2 reviews..."

## Section 2: {Title} (~{N} words)
### 2.1 {Subsection}
- {argument} [cite: bibkey4]
- Table 1: {description}
...

## Figures and Tables Plan
- Figure 1: Taxonomy diagram (Section 3)
- Table 1: Comparison of approaches (Section 4)
- Figure 2: Timeline of developments (Section 2)

## Literature Allocation
- Section 1 cites: [bibkeys] (N papers)
- Section 2 cites: [bibkeys] (N papers)
...
```

#### Step 4: User Review Checkpoint

Present the outline to the user for approval:

```
Here is the proposed paper outline. Please review:

[Display outline]

Do you want to:
1. Proceed with this outline
2. Modify specific sections
3. Restructure entirely
4. Add/remove sections

Please confirm before I proceed to writing.
```

**IMPORTANT**: Do NOT proceed to writing modules until the user approves the outline.

### Quality Gates

- [ ] Outline covers all required sections
- [ ] Literature allocation is balanced (no section with 0 citations)
- [ ] Estimated word counts sum to target length
- [ ] User has approved the outline
- [ ] Outline saved to `_workspace/08_outline.md`
