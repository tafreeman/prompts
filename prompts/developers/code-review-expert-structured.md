---
title: "Code Review Expert: Structured Output"
category: "developers"
subcategory: "code-review"
tags: 
  - code-review
  - automation
  - ci-cd
  - structured-output
  - best-practices
author: "Prompt Engineering Team"
version: "1.1.0"
date: "2025-11-25"
difficulty: "intermediate"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
performance_metrics:
  complexity_rating: "medium"
  token_usage_estimate: "1500-2500"
  quality_score: "90"
testing:
  framework: "manual"
  validation_status: "passed"
  test_cases: ["json-schema-validation", "markdown-rendering"]
governance:
  risk_level: "low"
  data_classification: "internal"
  regulatory_scope: ["general"]
  approval_required: false
  retention_period: "1-year"
platform: "Claude Sonnet 4.5"
---

# Code Review Expert: Structured Output

## Description

An enhanced code review prompt that outputs structured, machine-readable reports conforming to the schema defined in `guides/domain-schemas.md`. Ideal for CI/CD integration, automated reporting, and dashboard analytics.

## Goal

Provide comprehensive code reviews with structured outputs (JSON or Markdown) that can be consumed by automation pipelines, stored in databases, or displayed in dashboards.

## Context

Use this prompt when you need code reviews that integrate with tools (GitHub Actions, GitLab CI, Azure DevOps), feed into dashboards, or require consistent, parseable output across multiple reviews.

## Inputs

- Code changes (diff, pull request, or full files)
- Repository and branch context
- Programming language
- Review focus areas (optional)

## Assumptions

- User wants structured output for automation
- Code is in a supported language
- Basic context (file paths, line numbers) is available

## Constraints

- Output must conform to the Code Review Report Schema (see `guides/domain-schemas.md`)
- Issues must be categorized by severity and category
- Suggested fixes must be actionable

## Process / Reasoning Style

Direct analysis with structured output. No extended reasoning visible unless requested.

## Output Requirements

JSON or Markdown conforming to the Code Review Report Schema in `guides/domain-schemas.md`:

**JSON Fields:**

- `review_id`, `repository`, `branch`, `commit_sha`
- `summary` (total_files, total_issues, severity breakdown, recommendation)
- `files` array with `issues` (severity, category, line range, description, suggested_fix)
- `positive_highlights`, `next_steps`

**Markdown Sections:**

- Summary, Files Reviewed, Issues (categorized), Positive Highlights, Next Steps

## Use Cases

- Automated code review in CI/CD pipelines
- Feeding review data into dashboards or analytics tools
- Storing review results in databases for trend analysis
- Generating consistent, comparable review reports across teams
- Integration with GitHub/GitLab/Azure DevOps via APIs

## Prompt

```text
You are a senior software engineer conducting a structured code review.

## Code Review Request

**Repository:** [REPOSITORY_NAME]  
**Branch:** [BRANCH_NAME]  
**Commit SHA:** [COMMIT_SHA] (optional)  
**Language:** [PROGRAMMING_LANGUAGE]

**Files Changed:**
```diff
[DIFF_OR_FILE_CONTENTS]
```text

**Review Focus (optional):** [FOCUS_AREAS]
(e.g., "security vulnerabilities", "performance", "test coverage")

---

## Task

Conduct a comprehensive code review and output a **structured report** conforming to the Code Review Report Schema (see `docs/domain-schemas.md`).

### Review Guidelines

**Categorize issues** by:

- **Severity:** CRITICAL | MAJOR | MINOR | INFO
- **Category:** security | performance | maintainability | style | bug | best-practice

**For each issue, provide:**

- File path and line range
- Clear description of the problem
- Rationale (why it matters)
- Suggested fix (code snippet or description)
- References (docs, style guides, CVEs) if applicable

**Also identify:**

- Positive highlights (things done well)
- Next steps (actions for the author)

### Output Format: [Choose JSON or Markdown]

**Option 1: JSON Output**

```json
{
  "review_id": "optional-uuid-or-timestamp",
  "repository": "[repo_name]",
  "branch": "[branch]",
  "commit_sha": "[sha]",
  "reviewer": "AI Code Reviewer",
  "review_date": "ISO-8601-timestamp",
  "summary": {
    "total_files": 0,
    "total_issues": 0,
    "critical_issues": 0,
    "major_issues": 0,
    "minor_issues": 0,
    "overall_recommendation": "APPROVE | REQUEST_CHANGES | COMMENT"
  },
  "files": [
    {
      "file_path": "path/to/file.ext",
      "language": "language",
      "issues": [
        {
          "issue_id": "unique-id",
          "severity": "CRITICAL | MAJOR | MINOR | INFO",
          "category": "security | performance | maintainability | style | bug | best-practice",
          "line_start": 0,
          "line_end": 0,
          "description": "What's wrong",
          "rationale": "Why it matters",
          "suggested_fix": "Code snippet or description",
          "references": ["link1", "link2"]
        }
      ]
    }
  ],
  "positive_highlights": ["Thing done well 1", "Thing done well 2"],
  "next_steps": ["Action 1", "Action 2"]
}
```text

**Option 2: Markdown Output**

```markdown
# Code Review Report

**Repository:** [repo_name]  
**Branch:** [branch_name]  
**Commit:** [commit_sha]  
**Reviewer:** AI Code Reviewer  
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

##### Issue 1: [Title] (Severity: CRITICAL|MAJOR|MINOR|INFO)

- **Category:** [security|performance|maintainability|style|bug|best-practice]
- **Location:** Lines [start]–[end]
- **Description:** [What's wrong]
- **Rationale:** [Why it matters]
- **Suggested Fix:**
  ```language
  [code snippet or description]
  ```

- **References:** [link1], [link2]

---

## Positive Highlights

- [Something done well]

---

## Next Steps

1. [Action item 1]
2. [Action item 2]

```text

---

**Now conduct the review** for the provided code changes.
```

## Variables

- `[REPOSITORY_NAME]`: Repository name or URL
- `[BRANCH_NAME]`: Branch being reviewed (e.g., `feature/add-auth`)
- `[COMMIT_SHA]`: Commit hash (optional)
- `[PROGRAMMING_LANGUAGE]`: Language (e.g., Python, JavaScript, Java)
- `[DIFF_OR_FILE_CONTENTS]`: Git diff or full file contents
- `[FOCUS_AREAS]`: Optional focus areas (security, performance, etc.)

## Usage

Use this prompt to generate structured code reviews. Provide the repository context, language, and the diff to be reviewed.

## Examples

**Input:**

```text
You are a senior software engineer conducting a structured code review.

## Code Review Request

**Repository:** ecommerce-api  
**Branch:** feature/add-payment-processing  
**Commit SHA:** a1b2c3d4  
**Language:** Python

**Files Changed:**
```diff
+++ app/payment.py
@@ -10,6 +10,15 @@ import requests
 
+def process_payment(amount, card_number, cvv):
+    # TODO: Add encryption
+    payload = {
+        "amount": amount,
+        "card": card_number,
+        "cvv": cvv
+    }
+    response = requests.post("https://payment-api.example.com/charge", json=payload)
+    return response.json()
+
```text

**Review Focus:** security vulnerabilities, PCI compliance

```

**Output (Markdown):**

```markdown
# Code Review Report

**Repository:** ecommerce-api  
**Branch:** feature/add-payment-processing  
**Commit:** a1b2c3d4  
**Reviewer:** AI Code Reviewer  
**Date:** 2025-11-18

---

## Summary

- **Total Files:** 1
- **Total Issues:** 3
  - Critical: 2
  - Major: 1
  - Minor: 0
- **Recommendation:** REQUEST_CHANGES

---

## Files Reviewed

### 1. app/payment.py

**Language:** Python

#### Issues

##### Issue 1: Unencrypted Payment Data Transmission (Severity: CRITICAL)

- **Category:** security
- **Location:** Lines 11–19
- **Description:** Payment card data (card_number, cvv) is transmitted in plaintext within the application and potentially logged.
- **Rationale:** Violates PCI DSS requirements. Exposing card data in plaintext creates massive security and compliance risk.
- **Suggested Fix:**
  ```python
  # Never handle raw card data in application code
  # Use a PCI-compliant payment processor SDK that tokenizes card data client-side
  
  from payment_processor import PaymentClient
  
  def process_payment(amount, payment_token):
      """
      Process payment using tokenized card data.
      payment_token should be generated client-side by payment processor JS SDK.
      """
      client = PaymentClient(api_key=os.environ['PAYMENT_API_KEY'])
      response = client.charge(amount=amount, token=payment_token)
      return response
  ```text

- **References:**
  - [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
  - [OWASP: Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)

##### Issue 2: API Key Hardcoded or Missing (Severity: CRITICAL)

- **Category:** security
- **Location:** Line 18
- **Description:** No authentication/API key visible in the request to the payment API.
- **Rationale:** Either the API key is hardcoded (security risk) or missing (request will fail). API keys must be stored in environment variables or secrets management.
- **Suggested Fix:**

  ```python
  import os
  
  API_KEY = os.environ.get('PAYMENT_API_KEY')
  if not API_KEY:
      raise ValueError("PAYMENT_API_KEY environment variable not set")
  
  headers = {"Authorization": f"Bearer {API_KEY}"}
  response = requests.post(
      "https://payment-api.example.com/charge", 
      json=payload, 
      headers=headers
  )
  ```text

- **References:** [OWASP: Hardcoded Secrets](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)

##### Issue 3: No Error Handling (Severity: MAJOR)

- **Category:** bug
- **Location:** Lines 11–19
- **Description:** No exception handling for network failures, API errors, or invalid responses.
- **Rationale:** Production code must handle failures gracefully (retries, logging, user-facing errors).
- **Suggested Fix:**

  ```python
  import logging
  
  def process_payment(amount, payment_token):
      try:
          client = PaymentClient(api_key=os.environ['PAYMENT_API_KEY'])
          response = client.charge(amount=amount, token=payment_token)
          return {"success": True, "transaction_id": response.id}
      except PaymentProcessorError as e:
          logging.error(f"Payment processing failed: {e}")
          return {"success": False, "error": "Payment declined"}
      except requests.exceptions.RequestException as e:
          logging.error(f"Network error during payment: {e}")
          return {"success": False, "error": "Service unavailable"}
  ```text

---

## Positive Highlights

- (None observed in this small diff)

---

## Next Steps

1. **CRITICAL**: Remove all handling of raw card data; integrate PCI-compliant payment SDK with client-side tokenization
2. **CRITICAL**: Store API key in environment variable or secrets manager
3. **MAJOR**: Add comprehensive error handling and logging
4. **Recommended**: Add unit tests mocking payment processor responses
5. **Compliance**: Review entire payment flow with security team for PCI DSS compliance

```

## Tips

- **Use JSON for automation:** Parse JSON output in CI/CD scripts, dashboards, or databases
- **Use Markdown for human review:** Easier to read in pull requests and documentation
- **Customize severity thresholds:** Define team-specific rules for CRITICAL vs MAJOR
- **Integrate with existing tools:** Map this schema to GitHub PR comments, JIRA tickets, or Slack alerts
- **Track metrics over time:** Store reviews in a database and analyze trends (issue types, severity distribution)

## Related Prompts

- [Code Review Expert](code-review-expert.md) - Original narrative review format
- [Refactoring Plan Designer](refactoring-plan-designer.md) - For larger code improvements
- [Reflection: Code Review Self-Check](../advanced-techniques/reflection-code-review-self-check.md) - Self-review before submission

## Governance Notes

- **PII Safety:** Ensure code samples don't contain user data, emails, or credentials
- **Security:** Redact API keys, secrets, or internal URLs from review reports
- **Storage:** Code review reports may contain proprietary code; store securely
- **Retention:** Follow company policy for code review retention (typically 2–7 years)

## Changelog

- 2025-11-18: Initial version with structured schema support based on ToT repository evaluation
