---

title: "Performance Architecture Optimizer"
category: "system"
tags: ["architect", "performance", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Performance Architecture Optimizer

## Description

Optimizes system performance architecture

## Use Cases

- Performance for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[budget]`: Budget
- `[issues]`: Issues
- `[load]`: Load
- `[system_name]`: System Name
- `[targets]`: Targets

## Example Usage

**Input:**

```text
[system_name]: Global Video Streaming Platform (10M concurrent viewers)
[issues]: High latency during live events (p99 > 5s), database CPU spikes to 100%, "thundering herd" on cache miss
[targets]: p99 latency < 500ms, 99.99% availability, reduce infrastructure cost by 20%
[load]: 500k requests/sec peak, 10PB data transfer/month
[budget]: $200k/month cloud spend limit
```

**Output:**

```text
## Performance Optimization Strategy

### 1. Bottleneck Analysis
*   **Root Cause:** Synchronous calls to user profile DB on every video segment request.
*   **Impact:** DB CPU saturation causes cascading latency.
*   **Inefficiency:** Cache stampede when popular live streams start.

### 2. Architecture Optimization
*   **Edge Compute:** Move auth verification to CloudFront Functions (Edge) to offload origin.
*   **Async Processing:** Decouple analytics writing using Kinesis Firehose (fire-and-forget).

### 3. Caching Strategy (Multi-Layer)
*   **L1 (Browser):** Aggressive Cache-Control headers for video segments (immutable).
*   **L2 (CDN):** Origin Shield architecture to collapse concurrent requests.
*   **L3 (App):** Request coalescing (singleflight pattern) to prevent thundering herd on cache misses.

[... continues with database optimization and monitoring ...]
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
