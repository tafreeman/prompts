---
title: "Governance & Risk Prompts"
shortTitle: "Governance"
intro: "Enterprise governance, privacy, and compliance prompts using ReAct reasoning and self-critique reflection patterns."
type: "reference"
difficulty: "intermediate"
audience:

  - "functional-team"
  - "solution-architect"
  - "project-manager"
  - "security-engineer"

platforms:

  - "github-copilot"
  - "chatgpt"
  - "claude"

author: "Prompt Library Team"
version: "1.1"
date: "2025-12-05"
governance_tags:

  - "requires-human-review"
  - "compliance-critical"

dataClassification: "internal"
reviewStatus: "draft"
layout: "category-landing"
children:

  - /prompts/governance/access-control-reviewer
  - /prompts/governance/ai-ml-privacy-risk-assessment
  - /prompts/governance/compliance-policy-generator
  - /prompts/governance/data-classification-helper
  - /prompts/governance/data-retention-policy
  - /prompts/governance/data-subject-request-handler
  - /prompts/governance/gdpr-compliance-assessment
  - /prompts/governance/hipaa-compliance-checker
  - /prompts/governance/legal-contract-review
  - /prompts/governance/privacy-impact-assessment
  - /prompts/governance/regulatory-change-analyzer
  - /prompts/governance/security-incident-response
  - /prompts/governance/soc2-audit-preparation
  - /prompts/governance/sox-audit-preparer
  - /prompts/governance/vendor-security-review

featuredLinks:
  gettingStarted:

    - /docs/prompt-authorship-guide

  popular:

    - /prompts/governance/gdpr-compliance-assessment
    - /prompts/governance/soc2-audit-preparation
    - /prompts/governance/privacy-impact-assessment

---

# Governance & Risk Prompts

Enterprise governance, privacy, and compliance prompts designed for regulatory assessments, audit preparation, and privacy operations. All prompts use the **ReAct (Reasoning + Acting) pattern** with **self-critique reflection** for systematic, auditable analysis.

---

## Overview

These prompts address critical governance needs for organizations operating under GDPR, CCPA, SOC 2, and emerging AI regulations. Each prompt follows a structured methodology:

1. **ReAct Pattern**: Think → Act → Observe → Reflect cycles ensure thorough analysis
2. **Self-Critique Reflection**: Built-in quality checks and gap analysis
3. **Regulatory Alignment**: Based on official guidance (ICO, AICPA, EU sources)
4. **Actionable Outputs**: Remediation roadmaps, evidence checklists, and compliance documentation

---

## In This Section

| Category | Pattern | Representative Prompt |
| :--- | :--- | :--- |
| **Privacy Compliance** | GDPR Article-by-Article assessment | [GDPR Compliance Assessment](/prompts/governance/gdpr-compliance-assessment) |
| **Impact Assessment** | ICO 7-step DPIA methodology | [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment) |
| **Subject Rights** | DSR workflow with verification | [Data Subject Request Handler](/prompts/governance/data-subject-request-handler) |
| **Data Lifecycle** | Retention schedule generation | [Data Retention Policy](/prompts/governance/data-retention-policy) |
| **Data Classification** | Sensitivity-level mapping | [Data Classification Helper](/prompts/governance/data-classification-helper) |
| **Security Audit** | SOC 2 Trust Services Criteria | [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) |
| **Financial Controls** | SOX ITGC compliance | [SOX Audit Preparer](/prompts/governance/sox-audit-preparer) |
| **Healthcare** | HIPAA Security/Privacy Rules | [HIPAA Compliance Checker](/prompts/governance/hipaa-compliance-checker) |
| **Identity & Access** | RBAC and SoD analysis | [Access Control Reviewer](/prompts/governance/access-control-reviewer) |
| **Third-Party Risk** | Vendor security assessment | [Vendor Security Review](/prompts/governance/vendor-security-review) |
| **Regulatory Intel** | Regulation impact analysis | [Regulatory Change Analyzer](/prompts/governance/regulatory-change-analyzer) |
| **Policy Drafting** | Framework-aligned policies | [Compliance Policy Generator](/prompts/governance/compliance-policy-generator) |
| **AI Governance** | ML privacy and EU AI Act | [AI/ML Privacy Risk Assessment](/prompts/governance/ai-ml-privacy-risk-assessment) |
| **Legal Review** | Contract risk analysis | [Legal Contract Review](/prompts/governance/legal-contract-review) |
| **Security Operations** | Incident response | [Security Incident Response](/prompts/governance/security-incident-response) |

---

## Quick Starts

### Privacy & Data Protection

- **Preparing for GDPR audit?** Use [GDPR Compliance Assessment](/prompts/governance/gdpr-compliance-assessment) for systematic Article 5-49 coverage.
- **Launching a new data processing activity?** Start with [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment) using ICO's 7-step DPIA.
- **Received a deletion request?** Follow [Data Subject Request Handler](/prompts/governance/data-subject-request-handler) for compliant processing.
- **Need a retention schedule?** Generate with [Data Retention Policy](/prompts/governance/data-retention-policy) mapping legal requirements.
- **Classifying data assets?** Use [Data Classification Helper](/prompts/governance/data-classification-helper) for sensitivity mapping.

### Security & Audit

- **Preparing for SOC 2 certification?** Use [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) to assess all Trust Services Criteria.
- **Preparing for SOX audit?** Use [SOX Audit Preparer](/prompts/governance/sox-audit-preparer) for ITGC compliance.
- **Reviewing user access?** Use [Access Control Reviewer](/prompts/governance/access-control-reviewer) for RBAC and SoD analysis.
- **Handling a security breach?** Follow [Security Incident Response](/prompts/governance/security-incident-response) for documented containment.

### Vendor & Third-Party

- **Evaluating a vendor?** Use [Vendor Security Review](/prompts/governance/vendor-security-review) for third-party risk assessment.

### AI Governance

- **Deploying an AI system?** Start with [AI/ML Privacy Risk Assessment](/prompts/governance/ai-ml-privacy-risk-assessment) for GDPR Art. 22 and EU AI Act compliance.

### Policy & Regulatory

- **New regulation to analyze?** Use [Regulatory Change Analyzer](/prompts/governance/regulatory-change-analyzer) for impact assessment.
- **Need a policy document?** Use [Compliance Policy Generator](/prompts/governance/compliance-policy-generator) for framework-aligned policies.

---

## Browse by Regulation

### GDPR / UK GDPR

- [GDPR Compliance Assessment](/prompts/governance/gdpr-compliance-assessment)
- [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment)
- [Data Subject Request Handler](/prompts/governance/data-subject-request-handler)
- [Data Retention Policy](/prompts/governance/data-retention-policy)
- [Data Classification Helper](/prompts/governance/data-classification-helper)

### HIPAA / Healthcare

- [HIPAA Compliance Checker](/prompts/governance/hipaa-compliance-checker)
- [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment)

### SOC 2 / AICPA

- [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation)
- [Access Control Reviewer](/prompts/governance/access-control-reviewer)
- [Vendor Security Review](/prompts/governance/vendor-security-review)

### SOX / Financial Controls

- [SOX Audit Preparer](/prompts/governance/sox-audit-preparer)
- [Access Control Reviewer](/prompts/governance/access-control-reviewer)

### EU AI Act / AI Governance

- [AI/ML Privacy Risk Assessment](/prompts/governance/ai-ml-privacy-risk-assessment)
- [Regulatory Change Analyzer](/prompts/governance/regulatory-change-analyzer)

### Legal & Contracts

- [Legal Contract Review](/prompts/governance/legal-contract-review)

### Security Operations

- [Security Incident Response](/prompts/governance/security-incident-response)

---

## Research Foundation

All governance prompts are grounded in:

**Prompting Methodologies:**

- **ReAct**: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023 ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629))
- **Self-Refine**: Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback", NeurIPS 2023 ([arXiv:2303.17651](https://arxiv.org/abs/2303.17651))

**Regulatory Sources:**

- European Data Protection Board (EDPB) guidelines
- UK Information Commissioner's Office (ICO) guidance
- AICPA Trust Services Criteria
- NIST Frameworks (CSF, Privacy Framework, AI RMF)

---

## Governance Tags

| Tag | Meaning |
| ----- | --------- |
| `requires-human-review` | Output must be reviewed by qualified personnel |
| `compliance-critical` | Errors may result in regulatory violations |
| `audit-required` | Actions should create audit trail |
| `pii-handling` | May process or output personal data |
| `ai-ethics` | Involves AI/ML ethical considerations |

---

**Note:** These prompts are designed to assist professionals but do not replace qualified legal, privacy, or security advice. Always verify outputs with subject matter experts and maintain human oversight for compliance decisions.
