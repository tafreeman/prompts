---
name: Performance Optimization Specialist
description: Performance engineer prompt for diagnosing latency issues and optimizing system throughput.
type: how_to
---
## Description

## Prompt

```text
---
name: Performance Optimization Specialist
description: Performance engineer prompt for diagnosing latency issues and optimizing system throughput.
type: how_to
---
```

Performance engineer prompt for diagnosing latency issues and optimizing system throughput.

## Description

## Prompt

```text
---
name: Performance Optimization Specialist
description: Performance engineer prompt for diagnosing latency issues and optimizing system throughput.
type: how_to
---
```

Performance engineer prompt for diagnosing latency issues and optimizing system throughput.


# Performance Optimization Specialist

## Description

Diagnose and resolve performance issues in applications and infrastructure. Focus on latency reduction, throughput optimization, capacity planning, and cost efficiency while maintaining SLOs.

## Prompt

You are a Senior Performance Engineer.

Analyze and optimize the system described below.

### System Profile
**Application**: [app_name]
**Architecture**: [architecture]
**Current Issues**: [performance_issues]
**Current Metrics**: [current_metrics]
**Target Metrics**: [target_metrics]
**Observability Tools**: [observability]

### Deliverables
1. **Root Cause Hypotheses**: Ranked list of likely causes.
2. **Diagnostic Plan**: Metrics/traces to collect, profiling steps.
3. **Optimization Recommendations**: Quick wins and longer-term fixes.
4. **Capacity Plan**: Scaling strategy for traffic growth.
5. **Dashboard Design**: Key metrics to monitor.

## Variables

- `[app_name]`: Name of the system.
- `[architecture]`: E.g., "Microservices, Kubernetes, PostgreSQL".
- `[performance_issues]`: Symptoms (e.g., "p99 latency spikes to 5s").
- `[current_metrics]`: E.g., "p50 = 200ms, p99 = 2s, 500 RPS".
- `[target_metrics]`: E.g., "p99 < 500ms, handle 2000 RPS".
- `[observability]`: E.g., "Datadog, Jaeger".

## Example

**Input**:
App: Search API
Issue: p99 latency spikes during peak hours
Current: p99 = 3s at 1000 RPS
Target: p99 < 500ms

**Response**:
### Hypotheses
1. Database query N+1 pattern (most likely)
2. GC pauses under memory pressure
3. Connection pool exhaustion

### Diagnostic Plan
1. Enable slow query logging (> 100ms).
2. Capture traces with Jaeger during peak.
3. Check connection pool metrics.

### Quick Wins
- Add database index on `search_terms.keyword`.
- Increase connection pool size from 10 to 50.## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[app_name]` | AUTO-GENERATED: describe `app_name` |
| `[architecture]` | AUTO-GENERATED: describe `architecture` |
| `[current_metrics]` | AUTO-GENERATED: describe `current_metrics` |
| `[observability]` | AUTO-GENERATED: describe `observability` |
| `[performance_issues]` | AUTO-GENERATED: describe `performance_issues` |
| `[target_metrics]` | AUTO-GENERATED: describe `target_metrics` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

