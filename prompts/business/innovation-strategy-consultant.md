---
title: "Innovation Strategy Consultant"
shortTitle: "Innovation Strategy"
intro: "Develops innovation strategies with opportunity identification, innovation frameworks, and implementation roadmaps."
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "business-analyst"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "innovation"
  - "strategy"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Innovation Strategy Consultant

---

## Description

Develops innovation strategies

---

## Use Cases

- Innovation for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Develop innovation strategy for:

Organization: [organization]
Innovation Goals: [goals]
Current Capabilities: [capabilities]
Market Opportunities: [opportunities]

Include:
1. Innovation assessment
2. Opportunity identification
3. Innovation framework
4. Implementation roadmap
5. Governance model
6. Success metrics
```text

---

## Variables

- `[capabilities]`: Capabilities
- `[goals]`: Goals
- `[opportunities]`: Opportunities
- `[organization]`: Organization

---

## Example Usage

**Input:**

```text
[organization]: Automotive Tier 1 Supplier (Traditional Powertrain)
[goals]: Transition revenue mix from 90% ICE (Internal Combustion) to 50% EV (Electric Vehicle) by 2030
[capabilities]: Strong mechanical engineering, world-class manufacturing; Weak software/electronics
[opportunities]: Battery Management Systems (BMS), Thermal Management for EVs
```text

**Output:**

```text
## Innovation Strategy

### 1. Innovation Assessment
*   **Gap:** "Software Defined Vehicle" trend requires capabilities we lack (Embedded C++, AI).
*   **Asset:** Deep relationships with OEMs (Ford, GM, VW) and manufacturing scale.

### 2. Innovation Framework (Three Horizons)
*   **Horizon 1 (Core):** Light-weighting existing mechanical parts for EVs.
*   **Horizon 2 (Adjacent):** Thermal management systems (leveraging existing HVAC expertise).
*   **Horizon 3 (Transformational):** AI-driven predictive maintenance software.

### 3. Implementation Roadmap
*   **Buy vs Build:** Acquire a small BMS software startup to jumpstart Horizon 2.
*   **Partnership:** Joint Venture with battery cell manufacturer.

[... continues with governance and success metrics ...]
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
