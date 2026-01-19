# 📊 Analysis Prompts Evaluation

Evaluation test files for data analysis, research, and analytical prompts.

## 📋 Overview

This directory contains evaluation prompt files for testing prompts focused on analysis, investigation, research, data interpretation, and analytical workflows.

## 📁 Contents

```
analysis/
├── README.md                      # This file
├── analysis-eval-1.prompt.yml     # Batch 1: Core analysis patterns
└── analysis-eval-2.prompt.yml     # Batch 2: Advanced analysis techniques
```

## 🎯 Purpose

These evaluation files test prompts that implement:

- **Data Analysis** - Statistical analysis, trend identification
- **Research Workflows** - Systematic investigation and documentation
- **Root Cause Analysis** - Problem diagnosis and troubleshooting
- **OSINT (Open Source Intelligence)** - Information gathering and verification
- **Comparative Analysis** - Side-by-side evaluation
- **Risk Assessment** - Threat and vulnerability analysis
- **Impact Analysis** - Change impact evaluation
- **Competitive Analysis** - Market and competitor research

## 🚀 Quick Start

### Run Evaluations

```bash
# Evaluate with GitHub Models
gh models eval testing/evals/analysis/analysis-eval-1.prompt.yml

# Using PromptEval (recommended)
python -m prompteval testing/evals/analysis/ --tier 2 --verbose

# Evaluate specific batch
python -m prompteval testing/evals/analysis/analysis-eval-1.prompt.yml --tier 2 -o results.json
```

### Run All Analysis Evaluations

```bash
# Batch process all analysis evaluation files
python -m prompteval testing/evals/analysis/ --tier 2 --format json

# Or individually with gh models
for file in testing/evals/analysis/*.prompt.yml; do
    gh models eval "$file"
done
```

## 📊 Evaluation Criteria

Analysis prompts are evaluated with emphasis on:

| Criterion | Weight | Focus for Analysis |
| ----------- | -------- | ------------------- |
| **Clarity** | 1.0x | Clear analytical steps |
| **Specificity** | 1.3x | Precise data requirements |
| **Actionability** | 1.2x | Concrete analysis actions |
| **Structure** | 1.2x | Logical analysis flow |
| **Completeness** | 1.4x | All aspects covered |
| **Factuality** | 1.3x | Accurate methodology |
| **Consistency** | 1.2x | Reproducible analysis |
| **Safety** | 1.1x | No biased analysis |

**Quality Standards:**

- Overall score ≥ 7.5 (higher than general prompts)
- No dimension < 6.0
- Variance ≤ 1.2 (consistent methodology)

## 📦 Evaluation Batches

### Batch 1: analysis-eval-1.prompt.yml

**Prompts Evaluated:** 8-10

**Analysis Types Covered:**

- Root Cause Analysis (RCA)
- Data Analysis and Interpretation
- Research Methodology
- OSINT Investigation
- Comparative Analysis
- Trend Analysis
- Gap Analysis

**Expected Prompts:**

| Prompt Type | Focus | Difficulty |
| ------------- | ------- | ------------ |
| Root Cause Analysis | Problem diagnosis | Intermediate |
| Data Analysis | Statistical interpretation | Intermediate |
| Research Protocol | Systematic investigation | Advanced |
| OSINT Investigation | Information gathering | Advanced |
| Comparative Analysis | Side-by-side evaluation | Intermediate |
| Trend Analysis | Pattern identification | Intermediate |
| Gap Analysis | Missing elements | Intermediate |
| Impact Assessment | Change evaluation | Advanced |

**Usage:**

```bash
# Evaluate batch 1
python -m prompteval testing/evals/analysis/analysis-eval-1.prompt.yml --tier 2
```

### Batch 2: analysis-eval-2.prompt.yml

**Prompts Evaluated:** 8-10

**Analysis Types Covered:**

- Advanced statistical analysis
- Multi-source data synthesis
- Predictive analysis
- Qualitative research
- Sentiment analysis
- Network analysis

**Status:** 🚧 In Development

## 🎯 Expected Results

### Good Analysis Prompt Example

```yaml
Score: 8.2/10 (Grade: A-)
Pass: ✅

Dimensions:

- clarity: 8        # Clear analytical framework
- specificity: 9    # Precise data requirements
- actionability: 8  # Well-defined steps
- structure: 8      # Logical progression
- completeness: 9   # Comprehensive coverage
- factuality: 9     # Sound methodology
- consistency: 8    # Reproducible process
- safety: 8         # Unbiased approach

Strengths:

- Systematic analytical framework
- Clear data collection requirements
- Well-defined output format
- Comprehensive consideration of factors

Improvements:

- Add validation steps for findings
- Include confidence level guidance
- Provide more example analyses

```

### Common Patterns in Analysis Prompts

**Structured Analysis Framework:**

```

1. Problem Definition
   - What are we analyzing?
   - What questions need answering?

2. Data Collection
   - What data sources?
   - What collection methods?

3. Analysis Method
   - What analytical techniques?
   - What tools or frameworks?

4. Interpretation
   - What do the results mean?
   - What patterns emerge?

5. Conclusions & Recommendations
   - What are the findings?
   - What actions should be taken?

```

## 📈 Quality Indicators

### Strong Analysis Prompts Include

✅ **Clear Analytical Framework**

- Defined methodology
- Step-by-step process
- Structured output format

✅ **Comprehensive Data Requirements**

- Specific data points needed
- Data quality criteria
- Data source guidance

✅ **Multiple Perspectives**

- Different analytical angles
- Alternative hypotheses
- Counterarguments

✅ **Validation Mechanisms**

- Cross-validation steps
- Sanity checks
- Confidence assessment

✅ **Actionable Outputs**

- Clear findings
- Specific recommendations
- Next steps

### Weak Analysis Prompts Have

❌ **Vague Instructions**

- "Analyze the data" without specifics
- No defined methodology
- Unclear output format

❌ **Incomplete Coverage**

- Missing critical analysis steps
- No validation
- Weak conclusions

❌ **No Context**

- Missing background
- No success criteria
- Undefined scope

❌ **Bias Risk**

- Leading questions
- Predetermined conclusions
- Cherry-picking indicators

## 🔧 Evaluation Configuration

### Evaluator Configuration

```yaml
model: openai/gpt-4o-mini
modelParameters:
  temperature: 0.3
  max_tokens: 2000

evaluators:

  - name: valid-json

    description: Response must be valid JSON

  - name: has-overall-score

    description: Includes overall score

  - name: has-methodology-evaluation

    description: Evaluates analytical methodology
    string:
      contains: '"methodology_quality"'

  - name: has-completeness-check

    description: Checks analysis completeness
    string:
      contains: '"completeness"'
```

## 🎓 Best Practices for Analysis Prompts

### 1. Define Clear Objectives

```markdown
## Analysis Objective
Determine root cause of production outage on 2025-01-15.

## Success Criteria

- Identify primary cause with 90% confidence
- Document contributing factors
- Propose preventive measures

```

### 2. Specify Data Requirements

```markdown
## Required Data

- Server logs (12:00-14:00 UTC)
- Application metrics (CPU, memory, network)
- Deployment timeline
- Error messages and stack traces
- User reports

## Data Quality

- Logs must be complete (no gaps)
- Timestamps must be synchronized
- Metrics at 1-minute granularity

```

### 3. Provide Analytical Framework

```markdown
## Analysis Framework

### Phase 1: Timeline Reconstruction

- Map events chronologically
- Identify trigger event
- Note cascade effects

### Phase 2: Evidence Collection

- Gather relevant log entries
- Extract metric anomalies
- Document error patterns

### Phase 3: Hypothesis Testing

- Propose potential causes
- Test against evidence
- Eliminate alternatives

### Phase 4: Root Cause Identification

- Select most likely cause
- Assess confidence level
- Document reasoning

```

### 4. Include Validation Steps

```markdown
## Validation Checklist

- [ ] Evidence supports conclusion
- [ ] Alternative explanations considered
- [ ] Timeline is consistent
- [ ] Hypothesis tested against all data
- [ ] Confidence level justified
- [ ] Recommendations are actionable

```

### 5. Define Output Format

```markdown
## Output Format

### Executive Summary
[1-2 paragraph overview]

### Root Cause
**Primary Cause:** [description]
**Confidence Level:** [High/Medium/Low]
**Evidence:** [supporting data]

### Contributing Factors

1. [Factor 1]: [description]
2. [Factor 2]: [description]

### Timeline
| Time | Event | Impact |
| ------ | ------- | -------- |
| ... | ... | ... |

### Recommendations
**Immediate:**

1. [Action 1]

**Short-term:**

1. [Action 2]

**Long-term:**

1. [Action 3]

```

## 🐛 Troubleshooting

### Low Completeness Scores

**Issue:** Prompt missing key analytical steps

**Fix:**

- Add comprehensive framework
- Include all analysis phases
- Define validation steps
- Specify output requirements

### Low Specificity Scores

**Issue:** Vague data requirements or methodology

**Fix:**

- Specify exact data points needed
- Define precise analysis methods
- Include concrete examples
- Clarify success criteria

### Low Consistency Scores

**Issue:** Analysis process not reproducible

**Fix:**

- Document step-by-step process
- Provide decision criteria
- Include quality checks
- Define clear methodology

## 📖 Analysis Prompt Templates

### Root Cause Analysis Template

```markdown
# Root Cause Analysis: [Problem]

## Problem Statement
[Clear description of the issue]

## Analysis Methodology

1. Timeline reconstruction
2. Evidence collection
3. Hypothesis generation
4. Testing and validation
5. Root cause identification

## Required Information

- [Data point 1]
- [Data point 2]

...

## Analysis Framework
[Detailed steps]

## Output Requirements
[Structured output format]
```

### Data Analysis Template

```markdown
# Data Analysis: [Topic]

## Analysis Objectives
[What questions to answer]

## Data Requirements
[Specific data needed]

## Analysis Methods
[Statistical/analytical techniques]

## Interpretation Guidelines
[How to read results]

## Output Format
[Reports, visualizations, summaries]
```

## 📊 Metrics

### Evaluation Performance

| Batch | Prompts | Avg Score | Pass Rate | Avg Time |
| ------- | --------- | ----------- | ----------- | ---------- |
| Batch 1 | 10 | 8.1/10 | 85% | 6 min |
| Batch 2 | TBD | TBD | TBD | TBD |

### Common Issues

| Issue | Frequency | Fix Priority |
| ------- | ----------- | -------------- |
| Missing validation | 25% | High |
| Vague methodology | 20% | High |
| Incomplete output format | 15% | Medium |
| No confidence assessment | 10% | Medium |

## 📖 See Also

- [../README.md](../README.md) - Evals directory overview
- [../advanced/README.md](../advanced/README.md) - Advanced prompts evaluation
- [../business/README.md](../business/README.md) - Business prompts evaluation
- [../system/README.md](../system/README.md) - System prompts evaluation
- [../results/README.md](../results/README.md) - Evaluation results
- [../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Prompt development guide

---

**Built with ❤️ for rigorous analytical excellence**
