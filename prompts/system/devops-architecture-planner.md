---

title: "DevOps Architecture Planner"
category: "system"
tags: ["architect", "devops", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# DevOps Architecture Planner

## Description

Designs DevOps and CI/CD architectures

## Use Cases

- DevOps for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design DevOps architecture for:

Development Team: [team]
Technology Stack: [stack]
Deployment Environments: [environments]
Quality Requirements: [quality]

Provide:
1. CI/CD pipeline design
2. Infrastructure as code
3. Monitoring and observability
4. Security integration
5. Deployment strategies
6. Automation framework
```

## Variables

- `[environments]`: Environments
- `[quality]`: Quality
- `[stack]`: Stack
- `[team]`: Team

## Example Usage

**Input:**

```text
[team]: 50 developers, 5 squads (Checkout, Search, Profile, Inventory, Payments)
[stack]: Java/Spring Boot microservices, Angular frontend, Kubernetes (EKS), PostgreSQL
[environments]: Dev, QA, Staging, Prod (Blue/Green)
[quality]: 80% code coverage gate, automated security scanning (SAST/DAST), zero critical vulns
```

**Output:**

```text
## DevOps Architecture

### 1. CI/CD Pipeline Design (GitLab CI / GitHub Actions)
*   **Commit Stage:** Unit Tests, Checkstyle, SAST (SonarQube).
*   **Build Stage:** Build Docker container, tag with commit SHA, push to ECR.
*   **Deploy Dev:** Helm upgrade to Dev namespace.
*   **Integration Test:** Run API integration tests against Dev.
*   **Promote:** Manual approval gate for Staging/Prod.

### 2. Infrastructure as Code (IaC)
*   **Tool:** Terraform with remote state locking (S3 + DynamoDB).
*   **Structure:** Modular approach (VPC module, EKS module, RDS module) to enforce standards across squads.

### 3. Deployment Strategy
*   **Production:** Blue/Green deployment using ArgoCD Rollouts.
    *   Traffic shifted 1% -> 10% -> 50% -> 100% based on health metrics (Error rate < 1%).
    *   Instant rollback if metrics degrade.

[... continues with observability and security integration ...]
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
