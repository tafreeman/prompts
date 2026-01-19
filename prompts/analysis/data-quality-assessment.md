---
title: "Data Quality Assessment"
shortTitle: "Data Quality"
intro: "Systematically evaluates dataset quality across six dimensions and generates structured reports with recommended actions."
type: "how_to"
difficulty: "intermediate"
audience:

  - "senior-engineer"
  - "business-analyst"

platforms:

  - "claude"
  - "chatgpt"
  - "github-copilot"

topics:

  - "data-quality"
  - "analysis"

author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-18"
governance_tags:

  - "PII-safe"
  - "general-use"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.6
---
# Data Quality Assessment

---

## Description

Systematically evaluates dataset quality across six dimensions (completeness, accuracy, consistency, timeliness, validity, uniqueness) and generates structured reports with recommended actions conforming to the schema in `docs/domain-schemas.md`.

## Goal

Identify data quality issues before they impact analytics, ML models, or business decisions, and provide actionable recommendations to improve data quality.

## Context

Use this prompt when onboarding new datasets, auditing existing data pipelines, preparing data for ML training, or investigating data-related issues (unexpected model behavior, incorrect reports).

## Inputs

- Dataset description (name, source, schema)
- Sample data or summary statistics
- Context (how the data will be used)
- Known issues or concerns (optional)

## Assumptions

- User has access to the dataset or representative sample
- Basic data profiling has been done (row/column counts, types)
- User can implement validation rules or fixes

## Constraints

- Assessment must be quantitative (scores, percentages)
- Recommendations must be actionable and prioritized
- Output must conform to Data Quality Assessment Schema (see `docs/domain-schemas.md`)

## Process / Reasoning Style

Systematic evaluation across six data quality dimensions with quantified scores and evidence-based recommendations.

---

## Output Requirements

Structured Markdown or JSON conforming to the Data Quality Assessment Schema in `docs/domain-schemas.md`:

**Sections:**

1. Overall Score (0–100%)
2. Dimension Scores (Completeness, Accuracy, Consistency, Timeliness, Validity, Uniqueness)
3. Issue Details (per dimension)
4. Recommended Actions (prioritized by impact)
5. Validation Rules (proposed checks)

---

## Use Cases

- Onboarding new data sources into a data warehouse
- Auditing data pipelines for quality issues
- Preparing datasets for ML model training
- Investigating anomalies in reports or dashboards
- Compliance checks for data governance initiatives

---

## Prompt

```text
You are a data quality expert assessing a dataset across six quality dimensions.

## Dataset Information

**Dataset Name:** [DATASET_NAME]

**Source:** [SOURCE_SYSTEM_OR_FILE]

**Time Period:** [TIME_RANGE]

**Schema:**
```text

[SAMPLE_DATA_OR_SUMMARY_STATS]

```text

**Usage Context:** [HOW_DATA_WILL_BE_USED]

**Known Issues (optional):** [ANY_KNOWN_PROBLEMS]

---

## Task

Conduct a comprehensive data quality assessment across six dimensions:

1. **Completeness**: Missing values, nulls, gaps
2. **Accuracy**: Validation rules violated, incorrect values
3. **Consistency**: Duplicates, conflicting data, format mismatches
4. **Timeliness**: Data freshness, staleness issues
5. **Validity**: Schema drift, type mismatches, invalid ranges
6. **Uniqueness**: Duplicate records

For each dimension, provide:

- **Score (0–100%)**
- **Issues Identified** (with examples and impact)
- **Severity** (High/Medium/Low)

Then provide:

- **Overall Score** (weighted average across dimensions)
- **Recommended Actions** (prioritized by impact and effort)
- **Validation Rules** (to prevent future issues)

---

## Output Format

Follow the Data Quality Assessment Schema from `docs/domain-schemas.md`:

# Data Quality Assessment

**Dataset:** [name]  
**Source:** [source]  
**Time Period:** [date range]  
**Rows:** [N] | **Columns:** [M]  
**Assessment Date:** [YYYY-MM-DD]

---

## Overall Score: [N]%

---

## Dimensions

### Completeness: [N]%

**Missing Values by Column:**

| Column | Missing % |
| -------- | ----------- |
| [col1] | [N]%      |
| [col2] | [N]%      |

**Critical Missing Fields:** [list columns with >20% missing data]

**Impact:** [How missing data affects downstream use]

---

### Accuracy: [N]%

**Validation Rules Failed:**

#### Rule 1: [rule name]

- **Column:** [column_name]
- **Failure Rate:** [N]%
- **Examples:** [invalid value 1], [invalid value 2]
- **Impact:** [How this affects data consumers]

---

### Consistency: [N]%

**Inconsistencies:**

#### 1. [Type: duplicate|conflicting|format_mismatch]

- **Description:** [what's inconsistent]
- **Affected Rows:** [N] ([N]% of dataset)
- **Severity:** [HIGH|MEDIUM|LOW]
- **Example:** [specific inconsistency]

---

### Timeliness: [N]%

- **Freshness:** [description, e.g., "data is 2 days old"]
- **Expected Refresh Frequency:** [e.g., "daily"]
- **Actual Refresh:** [e.g., "every 3 days"]
- **Staleness Issues:** [list any delays or gaps]

---

### Validity: [N]%

- **Schema Drift Detected:** [Yes/No]
- **Type Mismatches:**

| Column | Expected | Actual | Error Rate |
| -------- | ---------- | -------- | ------------ |
| [col1] | [type]   | [type] | [N]%       |

- **Out-of-Range Values:**
  - [Column X]: [N] values outside expected range [min, max]

---

### Uniqueness: [N]%

- **Duplicate Records:** [N] ([N]% of dataset)
- **Duplicate Rate by Key:** [if composite key, show breakdown]
- **Example Duplicates:** [show a few duplicate row IDs]

---

## Recommended Actions

### 1. [Action Title] (Priority: [HIGH|MEDIUM|LOW])

- **Action:** [what to do]
- **Rationale:** [why it matters]
- **Estimated Effort:** [low|medium|high]
- **Expected Improvement:** [e.g., "+15% accuracy score"]

### 2. [Action Title] (Priority: [HIGH|MEDIUM|LOW])

[Same structure]

---

## Validation Rules

### Rule 1: [rule_name]

- **Definition:** [logic or SQL]
- **Applies To:** [columns]
- **Failure Action:** [alert|block|log]

### Rule 2: [rule_name]

[Same structure]

---

## Next Steps

1. [Step 1: e.g., "Implement validation rules in ETL pipeline"]
2. [Step 2: e.g., "Fix high-priority data issues"]
3. [Step 3: e.g., "Set up automated quality monitoring"]

```text

---

## Variables

- `[DATASET_NAME]`: Name of the dataset
- `[SOURCE_SYSTEM_OR_FILE]`: Where the data comes from
- `[TIME_RANGE]`: Date range of the data
- `[TABLE_SCHEMA_OR_COLUMN_DEFINITIONS]`: Column names and types
- `[N]`, `[M]`: Row and column counts
- `[SAMPLE_DATA_OR_SUMMARY_STATS]`: Sample rows or profiling output
- `[HOW_DATA_WILL_BE_USED]`: Context (analytics, ML, reporting)
- `[ANY_KNOWN_PROBLEMS]`: Pre-existing issues or concerns

---

## Example Usage

**Input:**

```text
**Dataset Name:** customer_orders

**Source:** PostgreSQL production database

**Time Period:** 2025-01-01 to 2025-11-18

**Schema:**

- order_id (int, primary key)
- customer_id (int, foreign key)
- order_date (timestamp)
- total_amount (decimal)
- status (varchar)
- shipping_address (text)

**Row Count:** 1,500,000  
**Column Count:** 6

**Sample Data:**
| order_id | customer_id | order_date | total_amount | status | shipping_address |
| ---------- | ------------- | ------------ | -------------- | -------- | ------------------ |
| 1 | 101 | 2025-01-05 10:30 | 49.99 | shipped | 123 Main St |
| 2 | NULL | 2025-01-05 11:00 | 199.99 | pending | NULL |
| 3 | 103 | 2025-01-05 11:15 | -10.00 | SHIPPED | 456 Oak Ave |

**Usage Context:** Customer analytics and ML churn prediction model

**Known Issues:** Some orders missing customer_id, status field has inconsistent casing
```text

---

## Tips

- **Quantify everything:** Use percentages and counts, not vague terms like "some" or "many"
- **Prioritize by impact:** Focus on issues that affect critical use cases first
- **Provide examples:** Show actual invalid values, not just descriptions
- **Propose automation:** Validation rules should be implementable in ETL/database
- **Track over time:** Re-run assessment periodically to measure improvement

---

## Related Prompts

- [Data Pipeline Engineer](../developers/data-pipeline-engineer.md) - For building quality checks into pipelines


---

## Governance Notes

- **Data Classification:** Ensure sample data doesn't contain PII
- **Compliance:** Data quality issues may violate regulatory requirements (GDPR, CCPA)
- **Stakeholder Communication:** Share assessment with data governance team and data consumers
- **Remediation Tracking:** Create tickets/tasks for recommended actions and track completion
