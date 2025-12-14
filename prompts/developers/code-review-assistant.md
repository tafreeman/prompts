---
title: Code Review Assistant
shortTitle: Code Review
intro: An AI assistant that performs thorough code reviews, identifying potential
  issues, suggesting improvements, and ensuring code quality. This prompt helps developers
  get constructive feedback on their code before committing or submitting pull requests.
type: how_to
difficulty: beginner
audience:
- senior-engineer
- junior-engineer
platforms:
- claude
- chatgpt
- github-copilot
topics:
- code-review
- quality
- developers
- best-practices
author: Prompts Library Team
version: '2.0.0'
date: '2025-12-11'
governance_tags:
- PII-safe
- requires-human-review
dataClassification: internal
reviewStatus: approved
effectivenessScore: 0.0
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
  complexity_rating: "low"
  token_usage_estimate: "1000-2000"
  quality_score: "90"
testing:
  framework: "manual"
  validation_status: "passed"
  test_cases: ["beginner-review", "educational-feedback"]
governance:
  risk_level: "low"
  data_classification: "internal"
  regulatory_scope: ["SOC2", "ISO27001"]
  approval_required: false
  retention_period: "1-year"
---

# Code Review Assistant

---

## Description

An AI assistant that performs thorough code reviews, identifying potential issues, suggesting improvements, and ensuring code quality. This prompt helps developers get constructive feedback on their code before committing or submitting pull requests.

---

## Use Cases

- Review code before submitting a pull request
- Get feedback on refactoring decisions
- Learn best practices for a specific programming language
- Identify potential bugs or security vulnerabilities
- Improve code readability and maintainability

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `[LANGUAGE]` | Programming language (and optionally framework) | `Python`, `TypeScript + React`, `Java + Spring Boot` |
| `[BRIEF DESCRIPTION OF WHAT THE CODE DOES]` | What the code is intended to do | `Parses invoices and writes to DB` |
| `[PASTE YOUR CODE HERE]` | Code to review (ideally 50–300 lines) | *(paste code)* |

---

## Usage

**Input:**

```text
Programming Language: Python
Context: Calculates average order value from a list of payments

Code:
<paste code here>
```

---

## Prompt

```text
You are an experienced software engineer conducting a code review. Please review the following code and provide detailed feedback.

Programming Language: [LANGUAGE]
Context: [BRIEF DESCRIPTION OF WHAT THE CODE DOES]

Code:
```[LANGUAGE]
[PASTE YOUR CODE HERE]
```text

Please analyze the code and provide:

1. **Overall Assessment**: Brief summary of code quality
2. **Strengths**: What the code does well
3. **Issues**: Bugs, security vulnerabilities, or logic errors
4. **Improvements**: Suggestions for better practices, performance, or readability
5. **Refactoring**: Specific code snippets showing recommended changes

Focus on:

- Code correctness and logic
- Best practices for [LANGUAGE]
- Performance considerations
- Security implications
- Readability and maintainability
- Potential edge cases

```text

**Output:**

```text

**Overall Assessment:**
The function is functionally correct for basic use cases but lacks error handling and could be more Pythonic.

**Strengths:**

- Clear function name that describes its purpose
- Simple, readable logic
- Correct mathematical implementation for valid inputs

**Issues:**

- No error handling for empty lists (ZeroDivisionError)
- No validation for non-numeric inputs (TypeError)
- Manual loop could be more efficient

**Improvements:**

1. Add input validation and error handling
2. Use Python's built-in functions for better performance
3. Add type hints for clarity
4. Include docstring documentation

**Refactoring:**

```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: A list of numeric values
        
    Returns:
        The arithmetic mean of the numbers
        
    Raises:
        ValueError: If the list is empty or contains non-numeric values
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements must be numeric")
    
    return sum(numbers) / len(numbers)
```text

This refactored version:

- Uses built-in `sum()` for better performance
- Includes comprehensive error handling
- Has type hints and docstring
- Follows Python best practices (PEP 8)

```python

---

## Tips

- Be specific about the context and purpose of your code for more relevant feedback
- Include any particular concerns you have (e.g., "I'm worried about performance")
- For large codebases, review smaller sections at a time for more focused feedback
- Mention your experience level if you want feedback adjusted to your skill level
- Include any specific standards or style guides your team follows

## Language-Specific Considerations

### Python
- Check for type hints and proper use of `Optional`
- Look for `with` statements for resource management
- Verify PEP 8 compliance
- Check for mutable default arguments

### JavaScript/TypeScript
- Verify proper async/await usage (no floating promises)
- Check for proper null/undefined handling
- Look for TypeScript type safety (`any` overuse)
- Verify proper event listener cleanup

### Java
- Check for proper exception handling (no empty catches)
- Verify resource management (try-with-resources)
- Look for null safety (Optional usage)
- Check for thread safety in concurrent code

### Go
- Verify error handling (no ignored errors)
- Check for proper defer usage
- Look for goroutine leaks
- Verify context propagation

---

## Example Feedback Snippets

### Critical: Security Issue
```text
🔴 **CRITICAL - Security Vulnerability**
**Line 15**: SQL injection vulnerability

The query uses string concatenation with user input:
`query = "SELECT * FROM users WHERE id = " + user_id`

**Fix**: Use parameterized queries:
`cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`

**Why**: Attackers can inject malicious SQL to access/delete data.
```sql

### Major: Missing Error Handling
```text
🟡 **MAJOR - Missing Error Handling**
**Lines 23-25**: API call has no error handling

The `requests.get()` call will crash if the network fails.

**Fix**:
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error(f"API call failed: {e}")
    return None
```json

**Why**: Unhandled exceptions cause poor user experience and make debugging harder.
```

### Minor: Naming Improvement
```text
🟢 **MINOR - Naming Suggestion**
**Line 8**: Variable name `x` is not descriptive

**Suggestion**: Rename to `user_count` or `total_records` based on its purpose.

**Why**: Descriptive names make code self-documenting.
```text

---

## Related Prompts

- [Bug Finder and Fixer](bug-finder.md) - Specialized bug detection
- [Code Documentation Generator](code-documentation-generator.md) - Generate docs
- [Code Review Expert: Structured Output](code-review-expert-structured.md) - JSON/machine-readable output
- [Security Code Auditor](security-code-auditor.md) - Security-focused review
