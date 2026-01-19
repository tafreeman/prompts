---
title: Quality Assurance Planner
shortTitle: QA Planner
intro: Develops QA strategies and plans with quality objectives, testing strategies,
  and continuous improvement.
type: how_to
difficulty: intermediate
audience:

- project-manager
- qa-engineer

platforms:

- claude
- chatgpt
- github-copilot

topics:

- quality
- project-management

author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Quality Assurance Planner

---

## Description

Develops QA strategies and plans

---

## Use Cases

- Quality Assurance for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Create QA plan for:

Project: [project_name]
Quality Standards: [standards]
Deliverables: [deliverables]
Testing Requirements: [testing]

Include:

1. Quality objectives
2. QA processes and procedures
3. Testing strategy
4. Quality metrics
5. Review and approval workflows
6. Continuous improvement

```text

---

## Variables

- `[project_name]`: Project name (e.g., "Mobile Banking App v3.0 Release")
- `[standards]`: Quality standards (e.g., "ISO 25010, OWASP Mobile Top 10, WCAG 2.1 AA")
- `[deliverables]`: Key deliverables (e.g., "iOS app, Android app, Backend APIs, Admin dashboard")
- `[testing]`: Testing requirements (e.g., "Functional, Performance, Security, Accessibility testing")

---

## Example

```text
## Quality Assurance Plan

### 1. Quality Objectives

*   **Functional:** Zero Critical/High severity bugs at launch.
*   **Performance:** App load time < 2s on 4G.
*   **Security:** Pass external Pen Test with no high-risk findings.

### 2. Testing Strategy

*   **Shift Left:** Static code analysis (SonarQube) in CI/CD pipeline.
*   **Manual Testing:** Exploratory testing for "Check Deposit" flow (high risk).
*   **Automation:** Appium for regression suite (Target: 80% coverage).

### 3. Review Workflows

*   **Defect Triage:** Daily meeting (PM, Dev Lead, QA Lead) to prioritize bugs.
*   **Exit Criteria:** 100% of Test Cases executed, 95% Pass rate.

[... continues with metrics and continuous improvement ...]
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
