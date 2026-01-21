---
name: Code Review Assistant
description: An AI assistant that performs thorough code reviews, identifying potential issues, suggesting improvements, and ensuring code quality. This prompt helps developers get constructive feedback on their c
type: how_to
---

# Code Review Assistant

## Use Cases

- Review code before submitting a pull request
- Get feedback on refactoring decisions
- Learn best practices for a specific programming language
- Identify potential bugs or security vulnerabilities
- Improve code readability and maintainability

## Usage

**Input:**

```text
Programming Language: Python
Context: Calculates average order value from a list of payments

Code:
<paste code here>
```

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

## Related Prompts

- [Bug Finder and Fixer](bug-finder.md) - Specialized bug detection
- [Code Documentation Generator](code-documentation-generator.md) - Generate docs
- [Code Review Expert: Structured Output](code-review-expert-structured.md) - JSON/machine-readable output
- [Security Code Auditor](security-code-auditor.md) - Security-focused review
