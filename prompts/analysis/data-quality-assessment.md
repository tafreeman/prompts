---
name: Data Quality Assessment
description: Systematically evaluates dataset quality across six dimensions and generates structured reports with recommended actions.
type: how_to
---

# Data Quality Assessment

## Output Requirements

Structured Markdown or JSON conforming to the Data Quality Assessment Schema in `docs/domain-schemas.md`:

**Sections:**

1. Overall Score (0–100%)
2. Dimension Scores (Completeness, Accuracy, Consistency, Timeliness, Validity, Uniqueness)
3. Issue Details (per dimension)
4. Recommended Actions (prioritized by impact)
5. Validation Rules (proposed checks)

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

## Output Format

Follow the Data Quality Assessment Schema from `docs/domain-schemas.md`:

# Data Quality Assessment

**Dataset:** [name]  
**Source:** [source]  
**Time Period:** [date range]  
**Rows:** [N] | **Columns:** [M]  
**Assessment Date:** [YYYY-MM-DD]

## Dimensions

### Completeness: [N]%

**Missing Values by Column:**

| Column | Missing % |
| -------- | ----------- |
| [col1] | [N]%      |
| [col2] | [N]%      |

**Critical Missing Fields:** [list columns with >20% missing data]

**Impact:** [How missing data affects downstream use]

### Consistency: [N]%

**Inconsistencies:**

#### 1. [Type: duplicate|conflicting|format_mismatch]

- **Description:** [what's inconsistent]
- **Affected Rows:** [N] ([N]% of dataset)
- **Severity:** [HIGH|MEDIUM|LOW]
- **Example:** [specific inconsistency]

### Validity: [N]%

- **Schema Drift Detected:** [Yes/No]
- **Type Mismatches:**

| Column | Expected | Actual | Error Rate |
| -------- | ---------- | -------- | ------------ |
| [col1] | [type]   | [type] | [N]%       |

- **Out-of-Range Values:**
  - [Column X]: [N] values outside expected range [min, max]

## Recommended Actions

### 1. [Action Title] (Priority: [HIGH|MEDIUM|LOW])

- **Action:** [what to do]
- **Rationale:** [why it matters]
- **Estimated Effort:** [low|medium|high]
- **Expected Improvement:** [e.g., "+15% accuracy score"]

### 2. [Action Title] (Priority: [HIGH|MEDIUM|LOW])

[Same structure]

## Next Steps

1. [Step 1: e.g., "Implement validation rules in ETL pipeline"]
2. [Step 2: e.g., "Fix high-priority data issues"]
3. [Step 3: e.g., "Set up automated quality monitoring"]

```text

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

## Related Prompts

- [Data Pipeline Engineer](../developers/data-pipeline-engineer.md) - For building quality checks into pipelines


---

## Governance Notes

- **Data Classification:** Ensure sample data doesn't contain PII
- **Compliance:** Data quality issues may violate regulatory requirements (GDPR, CCPA)
- **Stakeholder Communication:** Share assessment with data governance team and data consumers
- **Remediation Tracking:** Create tickets/tasks for recommended actions and track completion
