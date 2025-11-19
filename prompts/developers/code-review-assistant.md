---

title: "Code Review Assistant"
category: "developers"
tags: ["code-review", "quality", "best-practices", "refactoring", "beginner-friendly"]
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-18"
difficulty: "beginner"
governance_tags: ["quality-assurance", "human-review-recommended"]
data_classification: "internal"
risk_level: "low"
regulatory_scope: ["internal-standards"]
approval_required: false
retention_period: "1-year"
platform: "Claude Sonnet 4.5"
---

# Code Review Assistant

## Description

An AI assistant that performs thorough code reviews, identifying potential issues, suggesting improvements, and ensuring code quality. This prompt helps developers get constructive feedback on their code before committing or submitting pull requests.

## Use Cases

- Review code before submitting a pull request
- Get feedback on refactoring decisions
- Learn best practices for a specific programming language
- Identify potential bugs or security vulnerabilities
- Improve code readability and maintainability

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

```

## Variables

- `[LANGUAGE]`: The programming language (e.g., Python, JavaScript, Java, Go)
- `[BRIEF DESCRIPTION OF WHAT THE CODE DOES]`: A one-line explanation of the code's purpose
- `[PASTE YOUR CODE HERE]`: The actual code you want reviewed

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

```

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

```

## Tips

- Be specific about the context and purpose of your code for more relevant feedback
- Include any particular concerns you have (e.g., "I'm worried about performance")
- For large codebases, review smaller sections at a time for more focused feedback
- Mention your experience level if you want feedback adjusted to your skill level
- Include any specific standards or style guides your team follows

## Related Prompts

- [Bug Finder and Fixer](bug-finder.md)
- [Code Documentation Generator](code-documentation-generator.md)
- [Code Review Expert: Structured Output](code-review-expert-structured.md)
- [Refactoring Assistant](refactoring-assistant.md)

## Changelog

### Version 1.0 (2025-10-29)

- Initial version
