---
title: "Regulatory Change Analyzer"
shortTitle: "Reg Change Analyzer"
intro: "A prompt to analyze new regulations or updates and assess their impact on organization policies and systems."
type: "how_to"
difficulty: "advanced"
audience:
  - "legal-counsel"
  - "compliance-officer"
  - "policy-analyst"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "legal"
  - "compliance"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-11"
governance_tags:
  - "requires-human-review"
  - "legal-advice-disclaimer"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "Global"
---
# Regulatory Change Analyzer

---

## Description

Helps compliance and legal teams digest complex regulatory texts (e.g., EU AI Act, new GDPR guidance) and determine the operational impact. It extracts key requirements, deadlines, and applicability criteria to aid in gap analysis.

---

## Use Cases

- Analyzing a new privacy law in a specific US state
- Reviewing updates to PCI-DSS standards
- Assessing the impact of the EU AI Act on product roadmap
- Summarizing regulatory enforcement actions for executive briefing
- Updating internal policies to match new legal requirements

---

## Prompt

```text
You are a Legal Compliance Analyst. Analyze the provided regulatory text or summary and assess its impact.

## Regulation / Update
[REGULATION_TEXT]

## Organization Context
[ORG_CONTEXT] (e.g., "Global SaaS company with customers in EU and US, processing HR data")

## Instructions
1.  Summarize the key requirements of the regulation.
2.  Identify the specific impacts on the organization based on the context.
3.  Highlight critical deadlines and penalties.
4.  Suggest immediate next steps for compliance.

## Output Format
- **Executive Summary**
- **Key Requirements Checklist**
- **Impact Assessment**
- **Action Plan**
```

---

## Variables

- `[REGULATION_TEXT]`: The text of the law or a detailed summary (e.g., "EU AI Act - High Risk Systems requirements").
- `[ORG_CONTEXT]`: Details about the company to tailor the impact analysis.

---

## Example

```text
## Impact Analysis: EU AI Act (High-Risk Systems)

### Executive Summary
The EU AI Act introduces strict obligations for "High-Risk" AI systems. Given your company provides "AI-based recruitment software," your product likely falls under the High-Risk classification (Annex III), requiring immediate attention to conformity assessments.

### Key Requirements Checklist
*   [ ] Risk Management System (Art. 9)
*   [ ] Data Governance & Training Data Quality (Art. 10)
*   [ ] Technical Documentation (Art. 11)
*   [ ] Human Oversight measures (Art. 14)
*   [ ] Registration in EU Database (Art. 51)

### Impact Assessment
*   **Product:** Need to implement logging and transparency features to explain ranking decisions to candidates.
*   **Data:** Must audit training data for gender/racial bias to meet Art. 10.
*   **Legal:** Need to appoint an Authorized Representative in the EU.

### Action Plan
1.  **Q1:** Conduct a gap analysis against Annex III requirements.
2.  **Q2:** Update technical documentation to include detailed model cards.
3.  **Q3:** Establish a "Human Oversight" workflow for the recruitment tool.
```

---

## Tips

- **Disclaimer:** This prompt provides analysis, not legal advice. Always consult with qualified counsel.
- **Applicability:** The first step is always determining "Does this apply to us?" Focus on jurisdiction and scope.
- **Deadlines:** Look for "entry into force" vs "date of application" – they are often different.

---

## Related Prompts

- [GDPR Compliance Assessment](/prompts/governance/gdpr-compliance-assessment) — Assess GDPR compliance for regulatory changes in privacy
- [AI/ML Privacy Risk Assessment](/prompts/governance/ai-ml-privacy-risk-assessment) — Analyze EU AI Act and AI regulation impacts
- [Compliance Policy Generator](/prompts/governance/compliance-policy-generator) — Draft updated policies based on new regulations
- [Legal Contract Review](/prompts/governance/legal-contract-review) — Review contracts for regulatory compliance clauses
