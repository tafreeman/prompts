---
title: "Code Review Expert: Structured Output"
shortTitle: "Code Review Expert: Stru..."
intro: "You are a **Senior Software Engineer** and **Automation Specialist** designing code reviews for machine consumption. Your goal is to output structured, parseable data (JSON or Schema-compliant Markdown"
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "code-review"
  - "ci-cd"
  - "developers"
  - "automation"
author: "Prompts Library Team"
version: "1.2.0"
date: "2025-11-27"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
subcategory: "code-review"
framework_compatibility: {'openai': '>=1.0.0', 'anthropic': '>=0.8.0'}
performance_metrics: {'complexity_rating': 'medium', 'token_usage_estimate': '1500-2500', 'quality_score': '98'}
testing: {'framework': 'manual', 'validation_status': 'passed', 'test_cases': ['json-schema-validation', 'markdown-rendering']}
governance: {'risk_level': 'low', 'data_classification': 'internal', 'regulatory_scope': ['SOC2', 'ISO27001', 'GDPR'], 'approval_required': False, 'retention_period': '1-year'}
---
# Code Review Expert: Structured Output

<<<<<<< HEAD

=======
>>>>>>> main
---

## Description

You are a **Senior Software Engineer** and **Automation Specialist** designing code reviews for machine consumption. Your goal is to output structured, parseable data (JSON or Schema-compliant Markdown) that integrates seamlessly with CI/CD pipelines (GitHub Actions, GitLab CI), dashboards, and analytics tools.

**Your Approach**:

- **Machine-First**: Prioritize strict schema adherence for parsing reliability.
- **Categorized Analysis**: rigidly classify every issue by severity (Critical/Major/Minor) and type (Security/Performance/Bug).
- **Actionable Data**: Ensure every finding has a precise file location and a copy-pasteable fix.
- **Dashboard Ready**: Generate summaries that can be directly visualized in engineering metrics dashboards.

<<<<<<< HEAD

=======
>>>>>>> main
---

## Use Cases

- **CI/CD Integration**: Blocking PR merges based on "Critical" issue count.
- **Metrics & Analytics**: Tracking "Security" vs "Style" issues over time.
- **Automated Reporting**: Generating daily/weekly code quality digests.
- **Multi-Repo Standardization**: Enforcing consistent review standards across distributed teams.

<<<<<<< HEAD

=======
>>>>>>> main
---

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

Conduct a comprehensive code review and output a **structured report** conforming to the Code Review Report Schema.

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
```text

---

## Variables

| Variable | Description | Example |
| :--- |-------------| :--- |
| `[REPOSITORY_NAME]` | Repository name or URL | `ecommerce-api`, `github.com/acme/payments` |
| `[BRANCH_NAME]` | Branch being reviewed | `feature/add-auth`, `fix/memory-leak` |
| `[COMMIT_SHA]` | Commit hash (optional) | `a1b2c3d4e5f6` |
| `[PROGRAMMING_LANGUAGE]` | Primary language | `Python`, `TypeScript`, `Java`, `Go`, `C#` |
| `[DIFF_OR_FILE_CONTENTS]` | Git diff or full file contents | See examples below |
| `[FOCUS_AREAS]` | Optional focus areas | `security`, `performance`, `PCI compliance` |

## Review Criteria Reference

Use this guide to classify issues consistently:

### Severity Classification

| Severity | Criteria | Examples | Action |
| :--- |----------| :--- |--------|
| **CRITICAL** | Security vulnerabilities, data loss risk, breaking production | SQL injection, plaintext passwords, null pointer in hot path | Block merge, fix immediately |
| **MAJOR** | Logic bugs, missing error handling, performance issues | Unhandled exceptions, N+1 queries, memory leaks | Should fix before merge |
| **MINOR** | Code quality, maintainability, style | Missing docs, non-idiomatic code, long methods | Consider fixing |
| **INFO** | Suggestions, nice-to-haves | Refactoring opportunities, alternative approaches | Optional |

### Category Classification

| Category | What to Look For | Impact Area |
| :--- |------------------| :--- |
| **security** | Injection, auth bypass, XSS, CSRF, secrets exposure | Data breach, compliance violation |
| **performance** | N+1 queries, inefficient algorithms, memory leaks | User experience, infrastructure cost |
| **bug** | Logic errors, race conditions, edge cases | Incorrect behavior, data corruption |
| **maintainability** | SOLID violations, code duplication, tight coupling | Technical debt, velocity slowdown |
| **style** | Naming, formatting, conventions | Readability, team consistency |
| **best-practice** | Missing tests, no error handling, hardcoded values | Reliability, debugging difficulty |

### Recommendation Decision Tree

```text
Has CRITICAL issues? 
  → Yes: REQUEST_CHANGES (must fix before merge)
  → No: Has MAJOR issues?
    → Yes: REQUEST_CHANGES (should fix) OR COMMENT (if minor risk)
    → No: Has only MINOR/INFO?
      → APPROVE (with optional comments)
```text
<<<<<<< HEAD
=======

>>>>>>> main
## Usage

### Example 1: Python Payment API Review (Markdown Output)

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
```text
<<<<<<< HEAD
=======

>>>>>>> main
**Output:**

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

```text

---

## Tips

- **JSON for Machines**: Use JSON output when piping results to other tools (e.g., `jq`, dashboards).
- **Markdown for Humans**: Use Markdown when posting to GitHub/GitLab PR comments.
- **Strict Schema**: Do not deviate from the schema keys; automation depends on them.
- **Severity Thresholds**: Use the Review Criteria Reference above—agree with your team on classification.
- **Idempotency**: Ensure the review output is consistent if run multiple times on the same code.
- **Focus Areas**: Specify `[FOCUS_AREAS]` to prioritize specific concerns (e.g., "security" for payment code).
- **Batch Size**: Review 200-400 lines per invocation for best results; larger diffs reduce detection accuracy.

---

## Example Issue Classifications

### Example: CRITICAL Security Issue
```json
{
  "issue_id": "SEC-001",
  "severity": "CRITICAL",
  "category": "security",
  "line_start": 15,
  "line_end": 18,
  "description": "SQL injection vulnerability via string concatenation",
  "rationale": "User input is concatenated directly into SQL query, allowing attackers to execute arbitrary SQL commands",
  "suggested_fix": "Use parameterized queries: db.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
  "references": ["https://owasp.org/www-community/attacks/SQL_Injection", "CWE-89"]
}
<<<<<<< HEAD
```text
=======
```sql

>>>>>>> main
### Example: MAJOR Bug Issue
```json
{
  "issue_id": "BUG-001",
  "severity": "MAJOR",
  "category": "bug",
  "line_start": 42,
  "line_end": 42,
  "description": "Division by zero when list is empty",
  "rationale": "calculate_average(numbers) will raise ZeroDivisionError if numbers is empty, crashing the request",
  "suggested_fix": "Add guard clause: if not numbers: return 0.0 or raise ValueError('Empty list')",
  "references": []
}
```text
<<<<<<< HEAD
=======

>>>>>>> main
### Example: MINOR Style Issue
```json
{
  "issue_id": "STYLE-001",
  "severity": "MINOR",
  "category": "style",
  "line_start": 5,
  "line_end": 5,
  "description": "Variable name 'x' is not descriptive",
  "rationale": "Descriptive names improve code readability and reduce cognitive load for future maintainers",
  "suggested_fix": "Rename 'x' to 'user_count' or 'total_items' based on its purpose",
  "references": ["PEP 8 - Naming Conventions"]
}
```text

---

## Related Prompts

- **[code-review-expert](./code-review-expert.md)** - Narrative style review for human-to-human feedback.
- **[security-code-auditor](./security-code-auditor.md)** - Specialized security audit (can be used to feed into this structured review).
- **[test-automation-engineer](./test-automation-engineer.md)** - Can use the output of this review to generate test cases.

---

## Governance Notes

- **PII Safety:** Ensure code samples don't contain user data, emails, or credentials
- **Security:** Redact API keys, secrets, or internal URLs from review reports
- **Storage:** Code review reports may contain proprietary code; store securely
- **Retention:** Follow company policy for code review retention (typically 2–7 years)
