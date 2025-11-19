# Domain Schemas for Prompt Outputs

This document defines standard JSON and Markdown schemas for high-frequency developer and data/database workflows. Use these schemas across prompts to ensure consistent, machine-consumable outputs that integrate cleanly into automation pipelines, dashboards, and enterprise tools.

---

## 1. Code Review Report Schema

For prompts like `code-review-expert-structured.md` and related developer workflows.

### JSON Schema

```json
{
  "review_id": "string (optional, UUID or timestamp)",
  "repository": "string (repo name or URL)",
  "branch": "string",
  "commit_sha": "string (optional)",
  "reviewer": "string (AI or human identifier)",
  "review_date": "ISO 8601 timestamp",
  "summary": {
    "total_files": "integer",
    "total_issues": "integer",
    "critical_issues": "integer",
    "major_issues": "integer",
    "minor_issues": "integer",
    "overall_recommendation": "APPROVE | REQUEST_CHANGES | COMMENT"
  },
  "files": [
    {
      "file_path": "string",
      "language": "string",
      "issues": [
        {
          "issue_id": "string",
          "severity": "CRITICAL | MAJOR | MINOR | INFO",
          "category": "security | performance | maintainability | style | bug | best-practice",
          "line_start": "integer",
          "line_end": "integer (optional, for multi-line issues)",
          "description": "string",
          "rationale": "string (why this is an issue)",
          "suggested_fix": "string (code snippet or description)",
          "references": ["array of strings (links to docs, style guides, CVEs)"]
        }
      ]
    }
  ],
  "positive_highlights": ["array of strings (things done well)"],
  "next_steps": ["array of strings (actions for the author)"]
}
```

### Markdown Template

```markdown
# Code Review Report

**Repository:** [repo_name]  
**Branch:** [branch_name]  
**Commit:** [commit_sha]  
**Reviewer:** [reviewer_name]  
**Date:** [YYYY-MM-DD]

---

## Summary

- **Total Files:** [N]
- **Total Issues:** [N]
  - Critical: [N]
  - Major: [N]
  - Minor: [N]
- **Recommendation:** [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Files Reviewed

### 1. [file_path]

**Language:** [language]

#### Issues

##### Issue 1: [Title] (Severity: [CRITICAL|MAJOR|MINOR|INFO])

- **Category:** [security|performance|maintainability|style|bug|best-practice]
- **Location:** Lines [start]–[end]
- **Description:** [What's wrong]
- **Rationale:** [Why it matters]
- **Suggested Fix:**
  ```language
  [code snippet or description]
  ```text

- **References:** [link1], [link2]

---

## Positive Highlights

- [Something done well]
- [Another strength]

---

## Next Steps

1. [Action item 1]
2. [Action item 2]

```

---

## 2. Test Generation Specification Schema

For prompts like `test-suite-generator-advanced.md` and test-related workflows.

### JSON Schema

```json
{
  "test_suite_id": "string (optional)",
  "target": {
    "type": "function | class | module | API | service",
    "name": "string",
    "language": "string",
    "file_path": "string"
  },
  "generated_date": "ISO 8601 timestamp",
  "test_categories": {
    "unit_tests": [
      {
        "test_name": "string",
        "scenario": "string (what behavior is tested)",
        "inputs": "object or array (test data)",
        "expected_output": "any (expected result)",
        "assertions": ["array of strings (what to assert)"],
        "edge_cases": ["array of strings (boundary conditions tested)"],
        "mocks_required": ["array of strings (dependencies to mock)"]
      }
    ],
    "integration_tests": [
      {
        "test_name": "string",
        "scenario": "string",
        "services_involved": ["array of strings"],
        "inputs": "object",
        "expected_behavior": "string",
        "setup_steps": ["array of strings"],
        "teardown_steps": ["array of strings"]
      }
    ],
    "contract_tests": [
      {
        "test_name": "string",
        "contract_type": "API | event | database",
        "provider": "string",
        "consumer": "string",
        "contract_definition": "object (schema or payload)",
        "validation_rules": ["array of strings"]
      }
    ],
    "load_tests": [
      {
        "test_name": "string",
        "scenario": "string",
        "target_rps": "integer (requests per second)",
        "duration": "string (e.g., '5m')",
        "expected_latency_p99": "string (e.g., '200ms')",
        "expected_error_rate": "string (e.g., '<1%')"
      }
    ]
  },
  "coverage_targets": {
    "statement_coverage": "percentage",
    "branch_coverage": "percentage",
    "critical_paths": ["array of strings (paths that must be covered)"]
  },
  "dependencies": {
    "test_framework": "string (e.g., Jest, pytest, JUnit)",
    "mocking_library": "string",
    "additional_libraries": ["array of strings"]
  }
}
```

### Markdown Template

```markdown
# Test Suite Specification

**Target:** [function/class/module name]  
**Language:** [language]  
**File:** [file_path]  
**Generated:** [YYYY-MM-DD]

---

## Coverage Targets

- Statement Coverage: [N]%
- Branch Coverage: [N]%
- Critical Paths: [list paths]

---

## Unit Tests

### Test 1: [test_name]

- **Scenario:** [what behavior is tested]
- **Inputs:** [test data]
- **Expected Output:** [result]
- **Assertions:**
  - [assertion 1]
  - [assertion 2]
- **Edge Cases:** [boundary conditions]
- **Mocks Required:** [dependencies]

---

## Integration Tests

### Test 1: [test_name]

- **Scenario:** [interaction being tested]
- **Services Involved:** [list services]
- **Inputs:** [test data]
- **Expected Behavior:** [outcome]
- **Setup Steps:**
  1. [step 1]
  2. [step 2]
- **Teardown Steps:**
  1. [step 1]

---

## Contract Tests

### Test 1: [test_name]

- **Contract Type:** [API|event|database]
- **Provider:** [service name]
- **Consumer:** [service name]
- **Contract Definition:**
  ```json
  {schema or payload}
  ```text

- **Validation Rules:** [list rules]

---

## Load Tests

### Test 1: [test_name]

- **Scenario:** [what's being load tested]
- **Target RPS:** [N]
- **Duration:** [time]
- **Expected P99 Latency:** [ms]
- **Expected Error Rate:** [%]

---

## Dependencies

- **Test Framework:** [name]
- **Mocking Library:** [name]
- **Additional Libraries:** [list]

```

---

## 3. Query Optimization Report Schema

For prompts like `sql-query-optimizer-advanced.md` and database performance workflows.

### JSON Schema

```json
{
  "optimization_id": "string (optional)",
  "database_type": "PostgreSQL | MySQL | SQL Server | Oracle | etc.",
  "original_query": "string (SQL)",
  "analysis_date": "ISO 8601 timestamp",
  "performance_baseline": {
    "execution_time_ms": "integer",
    "rows_examined": "integer",
    "rows_returned": "integer",
    "cost_estimate": "number (optional, DB-specific)"
  },
  "issues_identified": [
    {
      "issue_id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "category": "missing_index | N+1_query | full_table_scan | unnecessary_distinct | suboptimal_join | function_on_indexed_column | data_type_mismatch | other",
      "description": "string",
      "impact": "string (performance/cost impact)",
      "location": "string (part of query affected)"
    }
  ],
  "recommended_indexes": [
    {
      "table": "string",
      "columns": ["array of strings"],
      "index_type": "btree | hash | gin | gist | etc.",
      "justification": "string",
      "estimated_improvement": "string (e.g., '40% faster')"
    }
  ],
  "optimized_query": "string (rewritten SQL)",
  "expected_improvements": {
    "execution_time_reduction": "percentage",
    "rows_examined_reduction": "percentage",
    "cost_reduction": "percentage (optional)"
  },
  "validation_steps": ["array of strings (how to test the optimized query)"],
  "rollback_plan": "string (how to revert if needed)"
}
```

### Markdown Template

```markdown
# Query Optimization Report

**Database:** [database_type]  
**Analysis Date:** [YYYY-MM-DD]

---

## Original Query

```sql
[original query]
```text

---

## Performance Baseline

- **Execution Time:** [N] ms
- **Rows Examined:** [N]
- **Rows Returned:** [N]
- **Cost Estimate:** [N] (optional)

---

## Issues Identified

### Issue 1: [Title] (Severity: [CRITICAL|HIGH|MEDIUM|LOW])

- **Category:** [missing_index | N+1_query | full_table_scan | etc.]
- **Description:** [What's wrong]
- **Impact:** [Performance/cost impact]
- **Location:** [Part of query affected]

---

## Recommended Indexes

### Index 1

- **Table:** [table_name]
- **Columns:** [col1, col2, ...]
- **Index Type:** [btree|hash|gin|gist]
- **Justification:** [Why this index helps]
- **Estimated Improvement:** [percentage or description]

**DDL:**

```sql
CREATE INDEX [index_name] ON [table_name] ([columns]) USING [type];
```text

---

## Optimized Query

```sql
[rewritten query]
```text

---

## Expected Improvements

- **Execution Time Reduction:** [N]%
- **Rows Examined Reduction:** [N]%
- **Cost Reduction:** [N]% (optional)

---

## Validation Steps

1. [Step 1: Run EXPLAIN on both queries]
2. [Step 2: Test on staging with production-like data]
3. [Step 3: Compare metrics]

---

## Rollback Plan

[How to revert the change if issues arise]

```

---

## 4. Data Quality Assessment Schema

For prompts like `data-quality-assessment.md` and data analysis workflows.

### JSON Schema

```json
{
  "assessment_id": "string (optional)",
  "dataset": {
    "name": "string",
    "source": "string (database, file, API, etc.)",
    "time_period": "string (e.g., '2025-01-01 to 2025-01-31')",
    "row_count": "integer",
    "column_count": "integer"
  },
  "assessment_date": "ISO 8601 timestamp",
  "dimensions": {
    "completeness": {
      "score": "percentage",
      "missing_values_by_column": {
        "column_name": "percentage"
      },
      "critical_missing_fields": ["array of strings"]
    },
    "accuracy": {
      "score": "percentage",
      "validation_rules_failed": [
        {
          "rule": "string",
          "column": "string",
          "failure_rate": "percentage",
          "examples": ["array of invalid values"]
        }
      ]
    },
    "consistency": {
      "score": "percentage",
      "inconsistencies": [
        {
          "type": "duplicate | conflicting | format_mismatch",
          "description": "string",
          "affected_rows": "integer",
          "severity": "HIGH | MEDIUM | LOW"
        }
      ]
    },
    "timeliness": {
      "score": "percentage",
      "freshness": "string (e.g., 'data is 2 days old')",
      "staleness_issues": ["array of strings"]
    },
    "validity": {
      "score": "percentage",
      "schema_drift_detected": "boolean",
      "type_mismatches": [
        {
          "column": "string",
          "expected_type": "string",
          "actual_type": "string",
          "error_rate": "percentage"
        }
      ]
    },
    "uniqueness": {
      "score": "percentage",
      "duplicate_records": "integer",
      "duplicate_rate": "percentage"
    }
  },
  "overall_score": "percentage",
  "recommended_actions": [
    {
      "priority": "HIGH | MEDIUM | LOW",
      "action": "string",
      "rationale": "string",
      "estimated_effort": "string (e.g., 'low', 'medium', 'high')"
    }
  ],
  "validation_rules": [
    {
      "rule_name": "string",
      "rule_definition": "string (logic or SQL)",
      "applies_to": ["array of column names"]
    }
  ]
}
```

### Markdown Template

```markdown
# Data Quality Assessment

**Dataset:** [name]  
**Source:** [database/file/API]  
**Time Period:** [date range]  
**Rows:** [N] | **Columns:** [N]  
**Assessment Date:** [YYYY-MM-DD]

---

## Overall Score: [N]%

---

## Dimensions

### Completeness: [N]%

**Missing Values by Column:**

| Column | Missing % |
|--------|-----------|
| [col1] | [N]%      |
| [col2] | [N]%      |

**Critical Missing Fields:** [list]

---

### Accuracy: [N]%

**Validation Rules Failed:**

#### Rule 1: [rule name]

- **Column:** [column_name]
- **Failure Rate:** [N]%
- **Examples:** [invalid value 1], [invalid value 2]

---

### Consistency: [N]%

**Inconsistencies:**

#### 1. [Type: duplicate|conflicting|format_mismatch]

- **Description:** [what's inconsistent]
- **Affected Rows:** [N]
- **Severity:** [HIGH|MEDIUM|LOW]

---

### Timeliness: [N]%

- **Freshness:** [description, e.g., "data is 2 days old"]
- **Staleness Issues:** [list any delays or gaps]

---

### Validity: [N]%

- **Schema Drift Detected:** [Yes/No]
- **Type Mismatches:**

| Column | Expected | Actual | Error Rate |
|--------|----------|--------|------------|
| [col1] | [type]   | [type] | [N]%       |

---

### Uniqueness: [N]%

- **Duplicate Records:** [N]
- **Duplicate Rate:** [N]%

---

## Recommended Actions

### 1. [Action Title] (Priority: [HIGH|MEDIUM|LOW])

- **Action:** [what to do]
- **Rationale:** [why it matters]
- **Estimated Effort:** [low|medium|high]

---

## Validation Rules

### Rule 1: [rule_name]

- **Definition:** [logic or SQL]
- **Applies To:** [columns]
```

---

## 5. Experiment Design Specification Schema

For prompts like `experiment-design-analyst.md` and A/B testing workflows.

### JSON Schema

```json
{
  "experiment_id": "string",
  "experiment_name": "string",
  "hypothesis": "string",
  "design_date": "ISO 8601 timestamp",
  "experiment_type": "A/B test | A/B/n test | quasi-experiment | multivariate",
  "primary_metric": {
    "name": "string",
    "definition": "string",
    "measurement_unit": "string",
    "baseline_value": "number (optional)",
    "minimum_detectable_effect": "percentage or absolute"
  },
  "secondary_metrics": [
    {
      "name": "string",
      "definition": "string",
      "measurement_unit": "string"
    }
  ],
  "guardrail_metrics": [
    {
      "name": "string",
      "definition": "string",
      "threshold": "string (value that triggers stop/rollback)"
    }
  ],
  "variants": [
    {
      "variant_id": "string (e.g., 'control', 'variant_A')",
      "description": "string",
      "allocation_percentage": "integer (0-100)"
    }
  ],
  "sample_size": {
    "required_per_variant": "integer",
    "statistical_power": "percentage (typically 80%)",
    "significance_level": "percentage (typically 5%)",
    "estimated_duration": "string (e.g., '2 weeks')"
  },
  "randomization": {
    "unit": "user | session | request | other",
    "method": "random | stratified | cluster",
    "stratification_variables": ["array of strings (optional)"]
  },
  "exclusion_criteria": ["array of strings (who/what is excluded)"],
  "success_criteria": "string (how to decide if experiment succeeded)",
  "risks": [
    {
      "risk": "string",
      "mitigation": "string"
    }
  ],
  "analysis_plan": {
    "statistical_test": "string (e.g., t-test, chi-square, Mann-Whitney)",
    "adjustment_for_multiple_comparisons": "boolean",
    "subgroup_analyses": ["array of strings (optional)"]
  }
}
```

### Markdown Template

```markdown
# Experiment Design Specification

**Experiment ID:** [id]  
**Experiment Name:** [name]  
**Hypothesis:** [hypothesis statement]  
**Design Date:** [YYYY-MM-DD]  
**Type:** [A/B test | A/B/n test | quasi-experiment | multivariate]

---

## Primary Metric

- **Name:** [metric name]
- **Definition:** [how it's measured]
- **Unit:** [unit]
- **Baseline Value:** [current value] (optional)
- **Minimum Detectable Effect (MDE):** [N]%

---

## Secondary Metrics

1. **[Metric Name]:** [definition] | Unit: [unit]
2. **[Metric Name]:** [definition] | Unit: [unit]

---

## Guardrail Metrics

1. **[Metric Name]:** [definition] | Threshold: [value that triggers stop/rollback]

---

## Variants

| Variant ID | Description | Allocation % |
|------------|-------------|--------------|
| control    | [desc]      | [N]%         |
| variant_A  | [desc]      | [N]%         |

---

## Sample Size & Duration

- **Required per Variant:** [N] [units]
- **Statistical Power:** [N]%
- **Significance Level (α):** [N]%
- **Estimated Duration:** [time]

---

## Randomization

- **Unit:** [user|session|request|other]
- **Method:** [random|stratified|cluster]
- **Stratification Variables:** [list] (optional)

---

## Exclusion Criteria

- [Who/what is excluded from the experiment]

---

## Success Criteria

[How to decide if the experiment succeeded]

---

## Risks & Mitigations

### Risk 1: [description]

- **Mitigation:** [how to address]

---

## Analysis Plan

- **Statistical Test:** [t-test|chi-square|Mann-Whitney|etc.]
- **Adjustment for Multiple Comparisons:** [Yes/No]
- **Subgroup Analyses:** [list] (optional)
```

---

## Usage Guidelines

1. **Reference these schemas in prompt YAML frontmatter** or Output Requirements sections to enforce consistency.
2. **Use JSON schemas for automation** (e.g., CI/CD, analytics pipelines, dashboards).
3. **Use Markdown templates for human review** and documentation.
4. **Extend schemas** as needed for your domain, but preserve core fields for cross-prompt compatibility.
5. **Version schemas** when making breaking changes (add a `schema_version` field to JSON outputs).

---

## Related Documents

- `templates/prompt-template.md` – Standard prompt structure
- `docs/prompt-quality-audit.md` – Quality scoring rubric
- `docs/best-practices.md` – General prompt engineering guidance
- `prompts/advanced-techniques/` – CoT, ToT, ReAct, RAG patterns
