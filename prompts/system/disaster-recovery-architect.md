---

title: "Disaster Recovery Architect"
category: "system"
tags: ["architect", "disaster-recovery", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Disaster Recovery Architect

## Description

Designs disaster recovery architectures

## Use Cases

- Disaster Recovery for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design disaster recovery for:

Systems: [systems]
RTO Requirements: [rto]
RPO Requirements: [rpo]
Budget Constraints: [budget]
Compliance Needs: [compliance]

Provide:
1. DR strategy and design
2. Backup and replication
3. Failover procedures
4. Testing framework
5. Recovery automation
6. Communication plan
```

## Variables

- `[budget]`: Budget
- `[compliance]`: Compliance
- `[rpo]`: Rpo
- `[rto]`: Rto
- `[systems]`: Systems

## Example Usage

**Input:**

```text
[systems]: Critical Patient Records Database (SQL Server), Medical Imaging Archive (PACS/Blob Storage)
[rto]: 15 minutes (Maximum downtime)
[rpo]: 5 minutes (Maximum data loss)
[budget]: $50k/year for standby infrastructure
[compliance]: HIPAA (Encryption required, data sovereignty within US)
```

**Output:**

```text
## Disaster Recovery Strategy

### 1. DR Design: "Warm Standby" (Pilot Light)
*   **Primary Region:** US-East (N. Virginia)
*   **DR Region:** US-West (Oregon) - Sufficient distance for geographic redundancy.

### 2. Replication Strategy
*   **Database:** SQL Server Always On Availability Groups with Async commit to DR region.
*   **Imaging Data:** S3 Cross-Region Replication (CRR) with versioning enabled (RPO < 1 min).

### 3. Failover Procedures
1.  **Detection:** CloudWatch alarm triggers if Primary Health Check fails for 3 consecutive minutes.
2.  **Database:** Script promotes DR Read Replica to Primary Master.
3.  **DNS:** Route53 Health Check automatically updates DNS records to point to DR Load Balancer.

[... continues with testing framework and recovery automation ...]
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
