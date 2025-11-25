---

title: "Market Entry Strategist"
category: "business"
tags: ["consultant", "market-entry", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Market Entry Strategist

## Description

Develops market entry strategies

## Use Cases

- Market Entry for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Develop market entry strategy for:

Company: [company]
Target Market: [market]
Product/Service: [offering]
Competitive Landscape: [competition]
Resources: [resources]

Provide:
1. Market analysis
2. Entry strategy options
3. Go-to-market plan
4. Resource requirements
5. Risk assessment
6. Success metrics
```

## Variables

- `[company]`: Company
- `[competition]`: Competition
- `[market]`: Market
- `[offering]`: Offering
- `[resources]`: Resources

## Example Usage

**Input:**

```text
[company]: US-based SaaS HR Platform ("HR-Flow")
[market]: Germany (DACH Region)
[offering]: Employee Engagement & Performance Software
[competition]: Personio (Local incumbent), SAP SuccessFactors (Enterprise), Workday
[resources]: $2M Budget, 1 Local Sales Rep, No local office yet
```

**Output:**

```text
## Market Entry Strategy: Germany

### 1. Market Analysis
*   **Regulatory:** GDPR compliance is non-negotiable; Local data residency (Frankfurt region) required.
*   **Culture:** Preference for "Trust" and "Certifications" over "Innovation" marketing.

### 2. Entry Strategy Options
*   **Option A:** Direct Sales (Hire local team). High control, slow scale.
*   **Option B:** Channel Partners (Resellers). Lower margin, faster reach. (Recommended)

### 3. Go-to-Market Plan
*   **Positioning:** " The GDPR-compliant alternative for modern SMEs."
*   **Channel:** Partner with local HR consultancies who implement software.

[... continues with resource requirements and risk assessment ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
