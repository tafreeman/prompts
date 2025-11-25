---

title: "Project Closure Specialist"
category: "business"
tags: ["project-manager", "project-closure", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Project Closure Specialist

## Description

Manages project closure activities

## Use Cases

- Project Closure for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Plan project closure for:

Project: [project_name]
Deliverables Status: [deliverables]
Stakeholder Satisfaction: [satisfaction]
Lessons Learned: [lessons]

Provide:
1. Closure checklist
2. Final deliverable review
3. Stakeholder sign-off
4. Documentation handover
5. Team transition plan
6. Post-project evaluation
```

## Variables

- `[deliverables]`: Deliverables
- `[lessons]`: Lessons
- `[project_name]`: Project Name
- `[satisfaction]`: Satisfaction

## Example Usage

**Input:**

```text
[project_name]: Corporate Website Redesign v3.0
[deliverables]: New Site Live (Done), CMS Training (Done), SEO Audit (Done), Analytics Setup (Done)
[satisfaction]: Client NPS 9/10 ("Love the design"), but complained about SEO report being 2 days late
[lessons]: Content migration took 2x longer than estimated due to unstructured legacy data
```

**Output:**

```text
## Project Closure Plan

### 1. Closure Checklist
*   [x] **Financial:** Final invoice sent and paid.
*   [x] **Technical:** Admin credentials transferred to client IT.
*   [ ] **Marketing:** Case study draft approved by client.

### 2. Final Deliverable Review
*   **Scope Verification:** All SOW items delivered.
*   **Quality:** SEO Audit delay noted; root cause was tool API outage (force majeure).

### 3. Stakeholder Sign-off
*   **Action:** Schedule "Final Walkthrough & Sign-off" meeting for Friday.
*   **Document:** "Project Acceptance Form" ready for digital signature.

### 4. Lessons Learned (Retrospective)
*   **Issue:** Content Migration delay.
*   **Action:** Update estimation template to include "Content Audit" phase *before* quoting migration hours.

[... continues with handover and team transition ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
