---
title: Code Review Expert
shortTitle: Code Review Expert
intro: You are a **Senior Software Engineer** with 10+ years of experience conducting
  code reviews across multiple languages and frameworks. You follow **Google's Engineering
  Practices** and emphasize **SOLID
type: how_to
difficulty: advanced
title: "Code Review Expert"
shortTitle: "Code Review Expert"
intro: "A senior software engineer with 10+ years of experience conducting code reviews across multiple languages and frameworks, following Google's Engineering Practices and emphasizing SOLID principles."
type: "how_to"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "code-review"
  - "enterprise"
  - "developers"
  - "code-quality"
  - "security"
author: "Prompts Library Team"
version: "2.3.0"
date: "2025-12-11"
governance_tags:
  - "general-use"
  - "PII-safe"
  - "requires-human-review"
dataClassification: "internal"
reviewStatus: "approved"
subcategory: "code-review"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
  github-copilot: ">=1.0.0"
performance_metrics:
  complexity_rating: "high"
  token_usage_estimate: "2000-3000"
  quality_score: "98"
testing:
  framework: "manual"
  validation_status: "passed"
  test_cases: ["security-audit", "performance-check", "solid-principles"]
governance:
  risk_level: "medium"
  data_classification: "internal"
  regulatory_scope: ["SOC2", "ISO27001", "GDPR"]
  approval_required: false
  retention_period: "2-years"
---

# Code Review Expert

---

## Description

Senior-level code review prompt focused on actionable feedback and engineering excellence. Produces clear merge guidance (blockers vs. important vs. suggestions) grounded in SOLID, readability, reliability, security, and maintainability.

---

## Prompt

```text
You are a Senior Software Engineer performing a structured code review.

Review the following change with the stated goal and context:

- Language/Framework: [language]
- PR Goal: [pr_goal]
- Component/Context: [context]
- Focus Areas: [focus_areas]
- Code/Diff:
  [code_snippet]

Requirements:
1) Call out issues as 🔴 BLOCKERS, 🟡 IMPORTANT, 🟢 SUGGESTIONS
2) Provide concrete recommendations and small patch-style snippets where useful
3) Highlight strengths and what’s done well
4) Note risks, edge cases, and missing tests
5) End with an overall assessment: APPROVE / REQUEST CHANGES / COMMENT
```

---

## Variables

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `[language]` | Programming language/framework | `Python + Django`, `TypeScript + React`, `Java + Spring Boot`, `Go`, `C# + .NET` |
| `[code_snippet]` | Code to review (50-300 lines optimal) | Paste actual code from PR |
| `[context]` | Component description | `User authentication service`, `Payment processing API`, `React dashboard component` |
| `[pr_goal]` | What the PR aims to accomplish | `Add password reset`, `Fix memory leak`, `Refactor database layer` |
| `[focus_areas]` | Specific concerns to prioritize | `Performance`, `Thread safety`, `Error handling`, `Test coverage` |

## Usage

**Input:**

```text
[language]: TypeScript + React
[context]: React dashboard component
[pr_goal]: Fix a memory leak in a subscription hook
[focus_areas]: Performance, Error handling, Test coverage

[code_snippet]:
<paste the relevant diff or 50–300 lines of code here>
```

## Output Format Specification

Structure your review using this format for consistency:

```markdown
## Code Review Summary

### 🔴 BLOCKERS (Must Fix)
[List critical issues that block merge]

### 🟡 IMPORTANT (Should Fix)
[List major issues that should be addressed]

### 🟢 SUGGESTIONS (Nice to Have)
[List minor improvements and optional changes]

---

### Detailed Findings

#### Finding 1: [Title]
- **Category**: 🔴 Blocker / 🟡 Important / 🟢 Suggestion
- **Location**: `file.py`, lines 10-15, function `process_data()`
- **Issue**: What's wrong
- **Impact**: Why it matters
- **Recommendation**:
  ```python
  # Fixed code here
  ```
- **Rationale**: Principle or best practice being applied

---

## Strengths
- [Positive observation 1]
- [Positive observation 2]

## Overall Assessment
**APPROVE** / **REQUEST CHANGES** / **COMMENT**
```text
```json

**Output** (condensed):

```text

CODE REVIEW SUMMARY

🔴 **BLOCKERS** (Must Fix Before Merge):

1. **Category**: 🔴 Blocker - Security Vulnerability  
   **Location**: src/api/register.py, lines 6-7, 11  
   **Issue**: SQL Injection vulnerabilities  
   **Impact**: Attacker can inject SQL commands, steal database, delete data (CVSS 9.8 Critical)  
   **Recommendation**:

   ```python
   # Use parameterized queries
   existing_user = db.execute(
       "SELECT * FROM users WHERE email = ?", (email,)
   ).fetchone()
   
   db.execute(
       "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
       (username, email, password_hash)  # Also fix password storage (see #2)
   )
   ```text

   **Rationale**: OWASP A03:2021 Injection - Never concatenate user input into SQL queries

2. **Category**: 🔴 Blocker - Security  
   **Location**: line 11  
   **Issue**: Plain text password storage  
   **Impact**: If database is breached, all user passwords are exposed  
   **Recommendation**:

   ```python
   from werkzeug.security import generate_password_hash
   password_hash = generate_password_hash(password)
   # Store password_hash, not password
   ```text

   **Rationale**: OWASP Password Storage Cheat Sheet - Use bcrypt/Argon2/PBKDF2

3. **Category**: 🔴 Blocker - Data Loss Risk  
   **Location**: Missing throughout  
   **Issue**: No transaction rollback on email failure  
   **Impact**: User created in DB but no verification email sent → orphan records  
   **Recommendation**:

   ```python
   try:
       db.execute(...)
       send_email(...)
       db.commit()  # Commit only if both succeed
   except Exception as e:
       db.rollback()  # Rollback on failure
       return jsonify({'error': 'Registration failed'}), 500
   ```text

🟡 **IMPORTANT** (Should Fix):

1. **Category**: 🟡 Important - Error Handling  
   **Location**: line 4-6  
   **Issue**: KeyError if 'username'/'email'/'password' missing from request  
   **Recommendation**:

   ```python
   username = data.get('username')
   email = data.get('email')
   password = data.get('password')
   
   if not all([username, email, password]):
       return jsonify({'error': 'Missing required fields'}), 400
   ```text

2. **Category**: 🟡 Important - Code Quality (Single Responsibility Principle)  
   **Issue**: register() does too much (validation, DB logic, email sending)  
   **Recommendation**: Extract to separate functions:

   ```python
   def validate_registration_data(data):
       # Return (is_valid, error_message)
   
   def create_user(username, email, password_hash):
       # Return user_id or raise exception
   
   def send_verification_email(email, user_id):
       # Handle email logic
   
   @app.route('/api/register', methods=['POST'])
   def register():
       is_valid, error = validate_registration_data(request.json)
       if not is_valid:
       return jsonify({'error': error}), 400
       # ... orchestrate calls to other functions
   ```text

🟢 **SUGGESTIONS** (Nice to Have):

1. **Category**: 🟢 Suggestion - Testing  
   **Issue**: No unit tests provided  
   **Recommendation**: Add tests for happy path + error cases (existing user, missing fields, SQL injection attempts)

---

**STRENGTHS**:

- Clear API endpoint structure
- Returns appropriate HTTP status codes (400, 201)
- Includes email verification step (good security practice)

**PRIORITY FIXES**:

- Fix SQL injection (CRITICAL - #1)
- Hash passwords (CRITICAL - #2)
- Add transaction handling (CRITICAL - #3)
- Improve error handling (#4)
- Refactor for SRP (#5)

**OVERALL ASSESSMENT**: ❌ **REQUEST CHANGES** - 3 critical blockers must be addressed before merge

```text
- **[test-automation-engineer](./test-automation-engineer.md)** - Review test coverage and quality
- **[performance-optimization-specialist](./performance-optimization-specialist.md)** - Performance-focused code review

---

## Related Workflows

<!-- SDLC Blueprint link removed - file doesn't exist yet -->

---

## Research Foundation

- **Google Engineering Practices** - Code Review Developer Guide (2019)
- **Martin Fowler - Clean Code** (2008) - Refactoring and code quality principles
- **Robert C. Martin - SOLID Principles** (2000) - Object-oriented design fundamentals
