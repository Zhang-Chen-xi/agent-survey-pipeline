# Module 13: Statistical Analysis

> Generates statistical analysis code, executes it (if data available), and produces APA-formatted results.

## Agent Instructions

You are performing statistical analysis for an academic paper. Generate reproducible analysis code and publication-ready results.

### Pre-flight Check

- [ ] Research design specifies hypotheses and variables
- [ ] Data is available (user-provided CSV/Excel/SPSS) OR user wants analysis code only
- [ ] Target analysis type identified

### Analysis Capabilities

| Category | Methods |
|----------|---------|
| Descriptive | Mean, SD, median, frequency, cross-tabulation |
| Comparison | t-test, ANOVA, Mann-Whitney, Kruskal-Wallis, chi-square |
| Regression | Linear, logistic, mixed-effects, hierarchical |
| Correlation | Pearson, Spearman, partial correlation |
| Survival | Kaplan-Meier, Cox proportional hazards |
| Meta-analysis | Fixed/random effects, forest plots, funnel plots |
| Bayesian | Bayesian t-test, Bayesian regression, BF reporting |
| ML | Classification, clustering, cross-validation |
| SEM | Path analysis, CFA, mediation/moderation |
| Time series | ARIMA, trend analysis |

### Workflow

#### Step 1: Understand the Data

```python
# Always start with exploratory analysis
import pandas as pd
df = pd.read_csv("data.csv")
print(df.describe())
print(df.info())
print(df.isnull().sum())
```

Report: sample size, variable types, missing data pattern, outliers.

#### Step 2: Select Appropriate Tests

Based on:
- Research questions / hypotheses
- Variable types (continuous, categorical, ordinal)
- Distribution assumptions (check normality with Shapiro-Wilk)
- Sample size considerations

#### Step 3: Execute Analysis

Generate Python code using:
- `scipy.stats` for basic tests
- `statsmodels` for regression and advanced models
- `pingouin` for effect sizes and power analysis
- `matplotlib` / `seaborn` for publication-quality figures

#### Step 4: Format Results (APA Style)

**t-test**: `t(48) = 2.45, p = .018, d = 0.70`
**ANOVA**: `F(2, 47) = 5.32, p = .008, η² = .18`
**Regression**: `β = .35, SE = .12, t = 2.92, p = .004, 95% CI [.11, .59]`
**Correlation**: `r = .42, p < .001, 95% CI [.28, .54]`
**Chi-square**: `χ²(3) = 12.45, p = .006, φ = .31`
**Bayesian**: `BF₁₀ = 8.42, δ = 0.65, 95% CrI [0.12, 1.18]`

#### Step 5: Generate Tables and Figures

Tables: APA format with proper alignment, notes, and significance markers.
Figures: 300 DPI minimum, labeled axes, error bars where appropriate.

### Output

Save to `_workspace/13_analysis_report.md` and `_workspace/13_analysis_code.py`.

### Quality Gates

- [ ] Appropriate tests selected and justified
- [ ] Assumptions checked (normality, homoscedasticity, etc.)
- [ ] Effect sizes reported alongside p-values
- [ ] APA format used throughout
- [ ] Code is reproducible (all imports, data loading, and seeds specified)
