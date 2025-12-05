---
title: "Cloud Architecture Consultant"
shortTitle: "Cloud Architecture Consu..."
intro: "Designs cloud-native architectures"
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "architect"
  - "system"
  - "cloud-architecture"
  - "enterprise"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 3.0
---
# Cloud Architecture Consultant


---

## Description

Designs cloud-native architectures


---

## Use Cases

- Cloud Architecture for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows


---

## Prompt

```text
Design cloud architecture for:

Application: [application]
Cloud Provider: [provider]
Scalability Needs: [scalability]
Compliance Requirements: [compliance]
Budget Constraints: [budget]

Provide:
1. Cloud service selection
2. Architecture patterns
3. Cost optimization
4. Security design
5. Disaster recovery
6. Migration strategy
```text

---

## Variables

- `[application]`: Application
- `[budget]`: Budget
- `[compliance]`: Compliance
- `[provider]`: Provider
- `[scalability]`: Scalability


---

## Example Usage

**Input:**

```text
[application]: Global Media Streaming Platform (Netflix-like)
[provider]: AWS (Primary) with Multi-region active-active
[scalability]: 10M concurrent users, auto-scaling for viral content
[compliance]: MPAA (Motion Picture Association) Content Security Best Practices
[budget]: Cost-aware (Spot instances for transcoding), Savings Plans for compute
```text
**Output:**

```text
## Cloud Architecture Design

### 1. Cloud Service Selection
*   **Compute:** EKS (Kubernetes) for microservices, Lambda for event triggers.
*   **Content Delivery:** CloudFront with Lambda@Edge for personalization.
*   **Media Processing:** AWS Elemental MediaConvert for transcoding.

### 2. Architecture Patterns
*   **Cell-Based Architecture:** Isolate failure domains by sharding users into "cells" (self-contained stacks).
*   **CQRS:** Separate read paths (Catalog browsing) from write paths (Watch history).

### 3. Cost Optimization
*   **Spot Fleet:** Use Spot instances for stateless transcoding workers (60-90% savings).
*   **Intelligent Tiering:** S3 Intelligent-Tiering for video library storage.

[... continues with security and disaster recovery ...]
```text

---

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints


---

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates
