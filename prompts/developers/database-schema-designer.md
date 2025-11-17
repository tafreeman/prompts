---
title: "Database Schema Designer"
category: "developers"
tags: ["developer", "database-design", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
---

# Database Schema Designer

## Description
Designs optimized database schemas

## Use Cases
- Database Design for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```
Design a database schema for [application_name]:

Business Requirements: [requirements]
Expected Scale: [scale]
Performance Needs: [performance]
Compliance: [compliance]

Include:
1. Entity-Relationship diagram
2. Table structures with constraints
3. Indexing strategy
4. Normalization analysis
5. Migration scripts
```

## Variables
- `[application_name]`: Application Name
- `[compliance]`: Compliance
- `[performance]`: Performance
- `[requirements]`: Requirements
- `[scale]`: Scale

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
