---

title: "Legacy Modernization Architect"
category: "system"
tags: ["architect", "modernization", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Legacy Modernization Architect

## Description

Architects legacy system modernization

## Use Cases

- Modernization for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Plan modernization for:

Legacy System: [system]
Business Drivers: [drivers]
Modernization Goals: [goals]
Constraints: [constraints]
Timeline: [timeline]

Include:
1. Current state assessment
2. Target architecture
3. Migration strategy
4. Risk mitigation
5. Phased approach
6. Success metrics
```

## Variables

- `[constraints]`: Constraints
- `[drivers]`: Drivers
- `[goals]`: Goals
- `[system]`: System
- `[timeline]`: Timeline

## Example Usage

**Input:**

```text
[system]: Core Banking System (Mainframe COBOL/DB2, 20 years old)
[drivers]: High maintenance costs ($10M/yr), shortage of COBOL developers, inability to launch mobile features
[goals]: Move to cloud-native microservices, enable real-time transaction processing, reduce TCO by 40%
[constraints]: Zero downtime migration required, strict regulatory compliance (OCC/FDIC), 3-year timeline
[timeline]: Phase 1 (Read-only) in 6 months, Phase 2 (write-path) in 18 months, Decom in 36 months
```

**Output:**

```text
## Modernization Strategy

### 1. Current State Assessment
*   **Technical Debt:** High coupling, brittle point-to-point integrations.
*   **Risk:** Knowledge silo concentrated in retiring staff.

### 2. Target Architecture
*   **Pattern:** Strangler Fig Pattern to incrementally replace functionality.
*   **Stack:** Java Spring Boot microservices on Kubernetes (EKS), Aurora PostgreSQL.
*   **Integration:** Kafka for event streaming between Mainframe (CDC) and Cloud.

### 3. Migration Strategy (Phased)
*   **Phase 1 (Hollow Core):** Build read-only APIs on cloud, syncing data via CDC (Change Data Capture) from DB2.
*   **Phase 2 (Vertical Slice):** Migrate "Customer Profile" module completely (read/write).
*   **Phase 3 (Transaction Core):** Migrate ledger logic.

[... continues with risk mitigation and success metrics ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
