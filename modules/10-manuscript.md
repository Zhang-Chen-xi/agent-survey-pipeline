# Module 10: Full Manuscript Writing (IMRaD)

> Writes a complete academic manuscript following IMRaD structure with cross-validated hypothesis-analysis-results-discussion chain.

## Agent Instructions

You are writing a complete academic research manuscript. This module produces a publication-ready paper with consistent logical chains from research questions to conclusions.

### Pre-flight Check

- [ ] Outline approved (`_workspace/08_outline.md`)
- [ ] Literature review drafted (Module 09) or user-provided
- [ ] All references verified (Module 05)
- [ ] Statistical analysis complete (Module 13) if applicable

### Agent Team Simulation

In a full deployment, this module orchestrates 5 specialist roles. As a single agent, simulate this by performing each role sequentially:

| Role | Responsibility | Output |
|------|---------------|--------|
| Research Designer | Research questions, hypotheses, methodology | `01_research_design.md` |
| Experiment Manager | Experiment protocols, data collection | `02_experiment_protocol.md` |
| Statistical Analyst | Analysis code, results, visualizations | `03_analysis_report.md` |
| Paper Writer | IMRaD writing, citation management | `04_manuscript.md` |
| Submission Preparer | Journal selection, formatting, cover letter | `05_submission_package.md` |

### Manuscript Structure

#### Title and Abstract

**Title**: Informative, specific, 10-15 words. Avoid jargon abbreviations.

**Abstract** (structured, 200-300 words):
- Background/Objective: 1-2 sentences
- Methods: 2-3 sentences
- Results: 2-3 sentences (with key numbers)
- Conclusion: 1-2 sentences

#### Introduction (4-paragraph structure)

1. **Background & Motivation**: Broad context, why this research matters
2. **Problem Statement & Gap**: What's known, what's missing, why it matters
3. **Proposed Solution**: Your approach, key innovations
4. **Contributions**: Explicit list of 3-4 contributions

Each contribution must be verifiable and traceable through the paper:
```
Contribution 1 → addressed in Method Section X → validated in Experiment Y → discussed in Discussion Z
```

#### Methods

- Sufficient detail for reproduction
- Formal notation where appropriate
- Algorithm pseudocode for novel procedures
- Data description with access information

#### Results

- Follow the same order as Methods
- Use APA format for statistics: `F(2, 47) = 5.32, p = .008, η² = .18`
- Tables for numerical comparisons, figures for trends
- Report effect sizes, not just p-values

#### Discussion

- Interpret results in context of research questions
- Compare with prior work (cite specifically)
- Acknowledge limitations honestly
- Suggest concrete future directions

#### Conclusion

- Restate main finding (1 sentence)
- Broader implications (1-2 sentences)
- Forward-looking statement (1 sentence)

### Cross-Validation Chain

After drafting, verify the logical consistency:

```
Hypotheses (Introduction)
    ↓ Each hypothesis must have a corresponding...
Analysis Method (Methods)
    ↓ Each analysis must produce...
Results (Results)
    ↓ Each result must be interpreted in...
Discussion (Discussion)
    ↓ Discussion must address all original...
Conclusions (Conclusion)
```

Flag any broken links in the chain.

### Output

Save to `_workspace/10_manuscript.md` with all sections.

### Quality Gates

- [ ] Complete IMRaD structure
- [ ] Hypothesis-analysis-results-discussion chain validated
- [ ] All citations verified
- [ ] Statistical reporting follows APA format
- [ ] Abstract reflects actual content
- [ ] Title is informative and specific
