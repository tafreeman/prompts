---

title: "Digital Transformation Advisor"
category: "business"
tags: ["consultant", "digital-transformation", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Digital Transformation Advisor

## Description

Guides digital transformation initiatives

## Use Cases

- Digital Transformation for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Plan digital transformation for:

Organization: [organization]
Current State: [current_state]
Transformation Goals: [goals]
Budget: [budget]
Timeline: [timeline]

Include:
1. Digital maturity assessment
2. Transformation strategy
3. Technology roadmap
4. Change management
5. Implementation phases
6. Success measurement
```

## Variables

- `[budget]`: Budget
- `[current_state]`: Current State
- `[goals]`: Goals
- `[organization]`: Organization
- `[timeline]`: Timeline

## Example Usage

**Input:**

```text
[organization]: National Insurance Provider ("SafeGuard")
[current_state]: Paper-based claims processing (fax/mail), legacy mainframe core, siloed customer data
[goals]: Achieve 100% digital claims submission, implement AI-driven underwriting, 360-degree customer view
[budget]: $50M Capital Investment
[timeline]: 3 Years (2025-2027)
```

**Output:**

```text
## Digital Transformation Plan

### 1. Digital Maturity Assessment
*   **Current Score:** 1.5/5 (Ad-hoc Digital).
*   **Gap:** Heavy reliance on manual data entry (OCR) creates 3-day lag in claims visibility.

### 2. Transformation Strategy
*   **Core Modernization:** Wrap legacy mainframe in API layer (MuleSoft) rather than full rewrite.
*   **Customer Experience:** Mobile-first "Claims Bot" for instant photo upload and status tracking.

### 3. Technology Roadmap
*   **Year 1:** API Gateway & Cloud Data Lake setup.
*   **Year 2:** Mobile App launch & AI Pilot for simple claims.
*   **Year 3:** Full AI Underwriting rollout.

[... continues with change management and success measurement ...]
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
