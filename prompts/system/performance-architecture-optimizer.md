---
title: "Performance Architecture Optimizer"
shortTitle: "Performance Architecture..."
intro: "Optimizes system performance architecture"
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
  - "performance"
  - "enterprise"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Performance Architecture Optimizer

---

## Description

Optimizes system performance architecture

---

## Use Cases

- Performance for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Optimize performance architecture for:

System: [system_name]
Performance Issues: [issues]
Target Metrics: [targets]
User Load: [load]
Budget Constraints: [budget]

Provide:
1. Performance bottleneck analysis
2. Architecture optimization
3. Caching strategy
4. Load balancing design
5. Database optimization
6. Monitoring framework
```text

---

## Variables

- `[budget]`: Budget
- `[issues]`: Issues
- `[load]`: Load
- `[system_name]`: System Name
- `[targets]`: Targets

---

## Example Usage

**Input:**

```text
[system_name]: Global Video Streaming Platform (10M concurrent viewers)
[issues]: High latency during live events (p99 > 5s), database CPU spikes to 100%, "thundering herd" on cache miss
[targets]: p99 latency < 500ms, 99.99% availability, reduce infrastructure cost by 20%
[load]: 500k requests/sec peak, 10PB data transfer/month
[budget]: $200k/month cloud spend limit
```text
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
