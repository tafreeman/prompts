---
title: "API Design Consultant"
category: "developers"
tags: ["developer", "api-design", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
---

# API Design Consultant

## Description
Creates RESTful API specifications

## Use Cases
- API Design for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```
Design a RESTful API for [service_name] with the following requirements:

Core Functionality: [core_features]
Data Models: [data_models]
Authentication: [auth_method]
Rate Limiting: [rate_limits]

Provide:
1. Endpoint specifications
2. Request/Response schemas
3. Error handling
4. Security considerations
5. Documentation structure
```

## Variables
- `[auth_method]`: Auth Method
- `[core_features]`: Core Features
- `[data_models]`: Data Models
- `[rate_limits]`: Rate Limits
- `[service_name]`: Service Name

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
