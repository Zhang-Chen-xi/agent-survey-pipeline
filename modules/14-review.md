# Module 14: Paper Review (Multi-Dimensional)

> Performs structured peer-review-quality analysis of the manuscript before delivery.

## Agent Instructions

You are reviewing the manuscript as a rigorous peer reviewer would. Provide constructive, specific, actionable feedback.

### Review Framework

#### Dimension 1: Argument Clarity (30%)

Evaluate:
- Is the central thesis clearly stated?
- Does every section contribute to the thesis?
- Are transitions logical and well-signposted?
- Can a reader summarize the paper's argument after one reading?

#### Dimension 2: Literature Engagement (25%)

Evaluate:
- Are key works in the field cited?
- Is the literature organized thematically (not just listed)?
- Are comparisons between approaches fair and specific?
- Is the paper's positioning relative to prior work clear?

#### Dimension 3: Evidence-Argument Fit (20%)

Evaluate:
- Do the data/results actually support the claims?
- Are there claims without supporting evidence?
- Is the methodology appropriate for the research questions?
- Are limitations honestly acknowledged?

#### Dimension 4: Knowledge Advancement (15%)

Evaluate:
- What is genuinely new vs. incremental?
- Does the paper advance understanding beyond existing work?
- Are the contributions specific and verifiable?

#### Dimension 5: Intellectual Honesty (10%)

Evaluate:
- Are alternative explanations considered?
- Are limitations presented as genuine constraints, not humble-brags?
- Are negative results reported?
- Are related concurrent works acknowledged?

### Output Template

```markdown
# Paper Review: {Title}

## Overall Assessment: {Accept / Minor Revision / Major Revision / Reject}
## Confidence: {High / Medium / Low}

## Summary
[2-3 paragraph summary of the paper and your assessment]

## Strengths
### S1: {Title}
{Detailed explanation with section/figure references}

### S2: {Title}
...

## Weaknesses
### W1: {Title}
{What is wrong, where specifically, why it matters, how to fix it}

### W2: {Title}
...

## Minor Issues
- [Specific, actionable items]

## Questions for the Authors
1. {Question that would clarify a concern}

## Actionable Revision Plan
1. {Priority-ordered revision tasks}
```

### Quality Gates

- [ ] At least 3 strengths and 3 weaknesses identified
- [ ] All weaknesses have specific section/line references
- [ ] All weaknesses include actionable fix suggestions
- [ ] Overall assessment consistent with identified issues
- [ ] Tone is professional and constructive
