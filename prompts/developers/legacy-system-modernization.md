---
name: Legacy System Modernization
description: Enterprise Modernization Architect prompt for migrating legacy systems to cloud-native architectures.
type: how_to
---
## Description

## Prompt

```text
---
name: Legacy System Modernization
description: Enterprise Modernization Architect prompt for migrating legacy systems to cloud-native architectures.
type: how_to
---
```

Enterprise Modernization Architect prompt for migrating legacy systems to cloud-native architectures.

## Description

## Prompt

```text
---
name: Legacy System Modernization
description: Enterprise Modernization Architect prompt for migrating legacy systems to cloud-native architectures.
type: how_to
---
```

Enterprise Modernization Architect prompt for migrating legacy systems to cloud-native architectures.


# Legacy System Modernization

## Description

Develop modernization strategies for legacy systems (mainframe, monolith, custom ERP). Balance business continuity, technical debt, and compliance while designing phased migration roadmaps.

## Prompt

You are an Enterprise Modernization Architect.

Develop a modernization strategy for the legacy system described below.

### System Profile
**System Name**: [system_name]
**Current Tech**: [current_tech]
**Target State**: [target_state]
**Business Drivers**: [business_drivers]
**Constraints**: [constraints]

### Deliverables
1. **Assessment Summary**: Technical debt, risk areas, dependencies.
2. **Modernization Approach**: Rehost, replatform, refactor, or rebuild.
3. **Phased Roadmap**: Waves with milestones and durations.
4. **Coexistence Strategy**: How old and new systems run in parallel.
5. **Success Metrics**: KPIs, SLOs, TCO targets.

## Variables

- `[system_name]`: E.g., "Legacy Billing System".
- `[current_tech]`: E.g., "COBOL on z/OS, DB2".
- `[target_state]`: E.g., "Microservices on Kubernetes".
- `[business_drivers]`: E.g., "Reduce maintenance cost 40%".
- `[constraints]`: E.g., "Cannot disrupt month-end processing".

## Example

**Input**:
System: Order Management
Current: Monolith on .NET Framework 4.5, SQL Server
Target: .NET 8 microservices, Azure SQL
Drivers: Improve release velocity

**Response**:
### Approach: Strangler Fig Pattern
1. **Phase 1**: Extract read-only APIs (3 months).
2. **Phase 2**: Migrate Order Creation to new service (6 months).
3. **Phase 3**: Decommission monolith (3 months).

### Coexistence
- API Gateway routes traffic to old or new based on feature flag.## Variables

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
| `[business_drivers]` | AUTO-GENERATED: describe `business_drivers` |
| `[constraints]` | AUTO-GENERATED: describe `constraints` |
| `[current_tech]` | AUTO-GENERATED: describe `current_tech` |
| `[system_name]` | AUTO-GENERATED: describe `system_name` |
| `[target_state]` | AUTO-GENERATED: describe `target_state` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

