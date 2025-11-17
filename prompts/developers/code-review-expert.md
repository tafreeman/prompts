---
title: "Code Review Expert"
category: "developers"
tags: ["developer", "code-quality", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
---

# Code Review Expert

## Description
Provides comprehensive code reviews

## Use Cases
- Code Quality for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```
Review the following [language] code for:

Code: [code_snippet]
Context: [context]
Critical Areas: [focus_areas]

Analyze:
1. Code quality and best practices
2. Security vulnerabilities
3. Performance bottlenecks
4. Maintainability issues
5. Testing coverage
6. Documentation quality

Provide specific recommendations with examples.
```

## Variables
- `[code_snippet]`: Code Snippet
- `[context]`: Context
- `[focus_areas]`: Focus Areas
- `[language]`: Language

## Example Usage

**Input:**
Replace the bracketed placeholders with your specific values, then use with Claude Sonnet 4.5 or Code 5.

**Output:**
The AI will provide a comprehensive response following the structured format defined in the prompt.

## Tips
- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts
- Browse other Developer prompts in this category
- Check the developers folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)
- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
