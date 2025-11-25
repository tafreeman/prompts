---

title: "Project Documentation Manager"
category: "business"
tags: ["project-manager", "documentation", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Project Documentation Manager

## Description

Manages project documentation

## Use Cases

- Documentation for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Organize documentation for:

Project: [project_name]
Document Types: [doc_types]
Audience: [audience]
Compliance Requirements: [compliance]

Provide:
1. Documentation strategy
2. Template library
3. Version control
4. Access management
5. Review processes
6. Archive procedures
```

## Variables

- `[audience]`: Audience
- `[compliance]`: Compliance
- `[doc_types]`: Doc Types
- `[project_name]`: Project Name

## Example Usage

**Input:**

```text
[project_name]: ISO 9001:2015 Certification
[doc_types]: Process Maps (Visio), Standard Operating Procedures (SOPs), Training Manuals, Audit Checklists
[audience]: Internal Employees (Users), External Auditors (Approvers)
[compliance]: ISO 9001:2015 Clause 7.5 (Documented Information)
```

**Output:**

```text
## Documentation Strategy

### 1. Strategy & Hierarchy
*   **Level 1:** Quality Manual (Policy).
*   **Level 2:** Procedures (Who, What, When).
*   **Level 3:** Work Instructions (How-to steps).
*   **Level 4:** Records (Evidence).

### 2. Template Library
*   **SOP Header:** Must include Doc ID, Version, Owner, Approver, Effective Date.
*   **Format:** Standardized MS Word styles for auto-generated Table of Contents.

### 3. Version Control
*   **Naming Convention:** `ISO-PROC-[Dept]-[ID]-v[Major].[Minor]` (e.g., `ISO-PROC-HR-001-v2.0`).
*   **Change Log:** Mandatory table at start of every document tracking "Reason for Change".

[... continues with access management and archive procedures ...]
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
