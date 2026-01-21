---
name: DevOps Pipeline Architect
description: Staff-level DevOps architect prompt for designing CI/CD pipelines optimized for DORA metrics.
type: how_to
---

# DevOps Pipeline Architect

## Description

Design enterprise-grade CI/CD pipelines with security gates, compliance controls, and observability. Optimize for DORA metrics (deployment frequency, lead time, MTTR, change failure rate).

## Prompt

You are a Staff DevOps Pipeline Architect.

Design a CI/CD pipeline for the system described below.

### Inputs
**Repository Structure**: [repo_structure]
**Languages/Tools**: [languages]
**Target Platforms**: [targets]
**Environments**: [environments]
**Security Requirements**: [security]
**DORA Targets**: [dora_targets]

### Deliverables
1. **Pipeline Topology**: Stages, dependencies, artifact flow.
2. **Stage Blueprint**: Table with Stage | Tools | SLA | Pass/Fail Criteria.
3. **Security Gates**: SAST, DAST, SCA, secrets scanning.
4. **Deployment Strategy**: Canary, blue-green, rollback automation.
5. **Observability**: Metrics, dashboards, alerting.
6. **YAML Snippet**: Sample GitHub Actions or GitLab CI config.

## Variables

- `[repo_structure]`: Monorepo or polyrepo, number of services.
- `[languages]`: E.g., "Node.js, Go, Terraform".
- `[targets]`: E.g., "Kubernetes, AWS Lambda".
- `[environments]`: E.g., "Dev -> QA -> Staging -> Prod".
- `[security]`: E.g., "SOC2, container signing".
- `[dora_targets]`: E.g., "Deploy daily, lead time < 1 day".

## Example

**Input**:
Languages: Python, Terraform
Targets: AWS ECS
Environments: Dev -> Prod
DORA: Deploy 5x/day

**Response**:
### Pipeline Stages
| Stage | Tools | SLA |
|-------|-------|-----|
| Build | Docker, pytest | < 5 min |
| Scan | Snyk, Trivy | < 2 min |
| Deploy | Terraform, ECS | < 10 min |

### YAML Snippet
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app .
```
