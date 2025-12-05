---
title: "Code Review Assistant"
shortTitle: "Code Review"
intro: "An AI assistant that performs thorough code reviews, identifying potential issues, suggesting improvements, and ensuring code quality. This prompt helps developers get constructive feedback on their code before committing or submitting pull requests."
type: "how_to"
difficulty: "beginner"
audience:
  - "senior-engineer"
  - "junior-engineer"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "code-review"
  - "quality"
  - "developers"
  - "best-practices"
author: "Prompts Library Team"
version: "2.0"
date: "2025-12-02"
governance_tags:
  - "PII-safe"
  - "requires-human-review"
dataClassification: "internal"
reviewStatus: "approved"
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

---

## Variables

| Variable | Description | Example Values |
| :--- |-------------| :--- |
| `[LANGUAGE]` | Programming language | `Python`, `JavaScript`, `TypeScript`, `Java`, `Go`, `C#`, `Rust` |
| `[BRIEF DESCRIPTION OF WHAT THE CODE DOES]` | One-line explanation of the code's purpose | `User authentication middleware`, `Shopping cart calculation`, `File upload handler` |
| `[PASTE YOUR CODE HERE]` | The actual code to review | 50-300 lines recommended per review |

## Review Criteria Checklist

Use this checklist to ensure comprehensive reviews:

### Critical Issues (Must Address)
- [ ] **Security vulnerabilities** - SQL injection, XSS, hardcoded secrets, auth bypass
- [ ] **Data loss risks** - Unvalidated deletes, missing transactions, race conditions
- [ ] **Breaking changes** - API contract violations, removed public methods

### Major Issues (Should Address)
- [ ] **Logic errors** - Off-by-one, null handling, boundary conditions
- [ ] **Error handling** - Uncaught exceptions, silent failures, poor error messages
- [ ] **Performance** - N+1 queries, memory leaks, inefficient algorithms

### Minor Issues (Consider Addressing)
- [ ] **Code style** - Naming conventions, formatting, organization
- [ ] **Documentation** - Missing comments, outdated docs, unclear intent
- [ ] **Test coverage** - Missing tests, edge cases not covered

### Severity Classification Guide

| Severity | Criteria | Examples |
| :--- |----------| :--- |
| **Critical** | Could cause security breach, data loss, or system failure | SQL injection, plaintext passwords, null pointer in hot path |
| **Major** | Causes incorrect behavior or significant technical debt | Unhandled exceptions, race conditions, missing validation |
| **Minor** | Affects readability or maintainability | Poor naming, missing docs, style inconsistencies |
| **Suggestion** | Nice-to-have improvements | Refactoring opportunities, alternative approaches |


---

## Example Usage

**Input:**

```text

You are an experienced software engineer conducting a code review. Please review the following code and provide detailed feedback.

Programming Language: Python
Context: Function to calculate the average of a list of numbers

Code:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)
```text

Please analyze the code and provide:

1. **Overall Assessment**: Brief summary of code quality
2. **Strengths**: What the code does well
3. **Issues**: Bugs, security vulnerabilities, or logic errors
4. **Improvements**: Suggestions for better practices, performance, or readability
5. **Refactoring**: Specific code snippets showing recommended changes

Focus on:

- Code correctness and logic
- Best practices for Python
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

```text

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
```text
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
```text
**Why**: Unhandled exceptions cause poor user experience and make debugging harder.
```text
### Minor: Naming Improvement
```text
🟢 **MINOR - Naming Suggestion**
**Line 8**: Variable name `x` is not descriptive

**Suggestion**: Rename to `user_count` or `total_records` based on its purpose.

**Why**: Descriptive names make code self-documenting.
```text
## Related Prompts - Specialized bug detection - Generate docs
- [Code Review Expert: Structured Output](code-review-expert-structured.md) - JSON/machine-readable output - Detailed refactoring guidance
- [Security Code Auditor](security-code-auditor.md) - Security-focused review
