---

title: "Cloud Migration Specialist"
category: "developers"
tags: ["developer", "cloud-migration", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Cloud Migration Specialist

## Description

Plans cloud migration strategies

## Use Cases

- Cloud Migration for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Create a cloud migration plan for:

Application: [app_name]
Current Infrastructure: [current_infra]
Target Cloud: [target_cloud]
Business Requirements: [requirements]

Provide:
1. Migration assessment
2. Cloud architecture design
3. Migration phases
4. Cost optimization
5. Security considerations
6. Performance validation
```

## Variables

- `[app_name]`: App Name
- `[current_infra]`: Current Infra
- `[requirements]`: Requirements
- `[target_cloud]`: Target Cloud

## Example Usage

**Input:**

```text
[app_name]: Legacy CRM System (Monolith)
[current_infra]: On-premise VMWare, Oracle 11g Database, WebLogic Server
[target_cloud]: Microsoft Azure
[requirements]: Reduce licensing costs by 30%, Improve availability to 99.9%, Enable geo-redundancy
```

**Output:**

```text
## Cloud Migration Plan

### 1. Migration Assessment (6 Rs)
*   **Strategy:** "Re-platform" (Lift, Tinker, and Shift).
*   **Rationale:** Codebase is too large to rewrite immediately, but infrastructure needs modernization.

### 2. Cloud Architecture Design
*   **Compute:** Azure App Service (Linux Containers) to replace WebLogic.
*   **Database:** Azure SQL Managed Instance (compatible with Oracle via SSMA migration tool).
*   **Storage:** Azure Blob Storage for documents.

### 3. Migration Phases
*   **Phase 1 (Proof of Concept):** Migrate non-prod environment and run regression tests.
*   **Phase 2 (Data Sync):** Setup Data Migration Service (DMS) for continuous replication.
*   **Phase 3 (Cutover):** Weekend maintenance window; switch DNS to Azure Traffic Manager.

[... continues with cost optimization and security ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Developer prompts in this category
- Check the developers folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
