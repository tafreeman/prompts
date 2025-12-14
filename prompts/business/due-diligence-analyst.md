---
title: Due Diligence Analyst
shortTitle: Due Diligence
intro: Conducts comprehensive due diligence with analysis frameworks, risk assessment,
  findings summary, and recommendations.
type: how_to
difficulty: advanced
audience:
- solution-architect
- business-analyst
platforms:
- claude
- chatgpt
- github-copilot
topics:
- analysis
- business
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Due Diligence Analyst

---

## Description

Conducts comprehensive due diligence

---

## Use Cases

- Due Diligence for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

---

## Variables

- `[transaction]`: Transaction type (e.g., "Acquisition of FinAI for $50M")
- `[target]`: Target company (e.g., "FinAI Inc. – AI-powered fraud detection startup")
- `[focus]`: Focus areas (e.g., "Technical architecture, IP ownership, team retention")
- `[timeline]`: Due diligence timeline (e.g., "14 days before LOI expiration")
- `[stakeholders]`: Key stakeholders (e.g., "CEO, CFO, CTO, Legal Counsel")

---

## Example

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
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates
