---

title: "Due Diligence Analyst"
category: "business"
tags: ["consultant", "due-diligence", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Due Diligence Analyst

## Description

Conducts comprehensive due diligence

## Use Cases

- Due Diligence for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Conduct due diligence for:

Transaction: [transaction]
Target Company: [target]
Focus Areas: [focus]
Timeline: [timeline]
Stakeholders: [stakeholders]

Provide:
1. Due diligence plan
2. Information requests
3. Analysis framework
4. Risk assessment
5. Findings summary
6. Recommendations
```

## Variables

- `[focus]`: Focus
- `[stakeholders]`: Stakeholders
- `[target]`: Target
- `[timeline]`: Timeline
- `[transaction]`: Transaction

## Example Usage

**Input:**

```text
[transaction]: Series B Venture Investment ($20M)
[target]: "FinAI" (AI-driven Credit Scoring Startup)
[focus]: Technical Due Diligence (IP ownership, Code Quality, Security Compliance)
[timeline]: 2 Weeks (Expedited)
[stakeholders]: Investment Committee, CTO (Acquirer)
```

**Output:**

```text
## Technical Due Diligence Report

### 1. Due Diligence Plan
*   **Day 1-3:** Codebase scan (Black Duck) for Open Source license violations.
*   **Day 4-7:** Architecture review and key personnel interviews.

### 2. Findings Summary
*   **IP Risk:** 🔴 HIGH. Core AI algorithm contains GPL v3 licensed code (Copyleft), contaminating proprietary IP.
*   **Security:** 🟢 LOW. SOC2 Type II certified; Pen test remediation complete.
*   **Scalability:** 🟡 MEDIUM. Monolithic Python backend may struggle with 10x user growth.

### 3. Recommendations
*   **Deal Breaker:** Require "FinAI" to rewrite the GPL-contaminated module *before* closing.
*   **Post-Close:** Budget $500k for microservices refactoring in Year 1.

[... continues with information requests and risk assessment ...]
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
