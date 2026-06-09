# Module 15: Originality Check

> Assesses the manuscript for potential plagiarism, excessive similarity, and AI-generated text patterns.

## Agent Instructions

You are performing an originality assessment of the manuscript. This is NOT a substitute for institutional plagiarism detection tools (Turnitin, iThenticate) but provides a pre-submission sanity check.

### Checks Performed

#### 1. Self-Plagiarism Risk
- Search for the user's previously published papers (if known)
- Flag sections that closely match prior publications
- Suggest rephrasing or proper self-citation

#### 2. Common Phrase Detection
- Identify overused academic clichés:
  - "In recent years, ... has attracted widespread attention"
  - "With the rapid development of..."
  - "It is well known that..."
- Suggest more original phrasing

#### 3. AI-Generated Text Patterns
Flag patterns commonly associated with AI-generated academic text:
- Excessive use of "Furthermore" / "Moreover" / "Additionally" at paragraph starts
- Perfect parallel structure across multiple paragraphs
- Generic claims without specific citations
- Sentences that are grammatically perfect but semantically vague

#### 4. Citation Originality
- What percentage of cited papers are from the last 3 years? (Freshness)
- Are there any "citation circles" (papers that only cite each other)?
- Is the reference list dominated by one research group?

#### 5. Structural Originality
- Does the paper follow a unique organizational logic, or is it template-driven?
- Is the taxonomy/classification novel?
- Do the conclusions go beyond restating results?

### Output

```markdown
# Originality Assessment

## Overall Originality Score: {High / Moderate / Low Risk}

## Phrase Analysis
- Unique phrasing: X%
- Common academic phrases: X instances
- AI-pattern sentences: X flagged

## Citation Freshness
- Papers from last 3 years: X%
- Papers from last 5 years: X%
- Foundational/classic papers: X%

## Recommendations
1. {Specific suggestions to improve originality}
2. ...

## Disclaimer
This assessment is heuristic and should be supplemented with institutional
plagiarism detection tools before submission.
```
