---

title: "Microservices Architecture Expert"
category: "system"
tags: ["architect", "microservices", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Microservices Architecture Expert

## Description

Designs microservices ecosystems

## Use Cases

- Microservices for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design microservices architecture for:

Domain: [domain]
Business Capabilities: [capabilities]
Scale Requirements: [scale]
Team Structure: [teams]

Include:
1. Service decomposition
2. Communication patterns
3. Data management
4. Service mesh design
5. Observability strategy
6. Deployment architecture
```

## Variables

- `[capabilities]`: Capabilities
- `[domain]`: Domain
- `[scale]`: Scale
- `[teams]`: Teams

## Example Usage

**Input:**

```text
[domain]: Global Logistics and Supply Chain Management
[capabilities]: Order tracking, Fleet management, Route optimization, Inventory forecasting, Driver payroll
[scale]: 50k trucks, 10M packages/day, global distribution
[teams]: 12 squads (approx 8-10 devs each), distributed across 3 time zones
```

**Output:**

```text
## Microservices Architecture Design

### 1. Service Decomposition (Domain-Driven Design)

**Bounded Contexts:**
*   **Logistics Core:**
    *   `Shipment Service` (Lifecycle of a package)
    *   `Routing Service` (Graph algorithms for pathfinding)
*   **Fleet Operations:**
    *   `Vehicle Telemetry Service` (IoT stream ingestion)
    *   `Driver Service` (Shifts, compliance)
*   **Commerce:**
    *   `Billing Service` (Invoicing)
    *   `Payroll Service` (Driver compensation)

### 2. Communication Patterns
*   **Synchronous (Internal):** gRPC for high-performance inter-service communication (e.g., Routing -> Telemetry).
*   **Asynchronous (Event-Driven):** Kafka for domain events (e.g., `PackageDelivered` event triggers `Billing` and `Notification`).
*   **External:** GraphQL Gateway for mobile apps and web dashboard.

[... continues with data management and service mesh ...]
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
