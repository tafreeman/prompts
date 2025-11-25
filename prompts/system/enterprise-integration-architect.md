---

title: "Enterprise Integration Architect"
category: "system"
tags: ["architect", "integration", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Enterprise Integration Architect

## Description

Designs enterprise integration solutions

## Use Cases

- Integration for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design integration architecture for:

Systems to Integrate: [systems]
Data Flow Requirements: [data_flow]
Performance Requirements: [performance]
Security Requirements: [security]

Include:
1. Integration patterns
2. API design strategy
3. Data transformation
4. Error handling
5. Monitoring and logging
6. Governance framework
```

## Variables

- `[data_flow]`: Data Flow
- `[performance]`: Performance
- `[security]`: Security
- `[systems]`: Systems

## Example Usage

**Input:**

```text
[systems]: Salesforce (CRM), SAP S/4HANA (ERP), Custom Logistics App (PostgreSQL), Stripe (Payments)
[data_flow]: Order-to-Cash process (Order placed -> Payment captured -> Inventory reserved -> Shipping label created -> Invoice generated)
[performance]: Real-time inventory checks (<500ms), eventual consistency for reporting (15 min lag ok)
[security]: OAuth 2.0 for all APIs, PII masking in logs, encrypted message queues
```

**Output:**

```text
## Integration Architecture

### 1. Integration Patterns
*   **Orchestration:** MuleSoft/Camel for complex Order-to-Cash workflow state management.
*   **Event-Driven:** "Order Created" event published to Kafka topic to trigger parallel downstream processes (Billing, Fulfillment).

### 2. Data Flow Design
1.  **Order Entry:** Salesforce triggers webhook to Integration Layer.
2.  **Validation:** Integration Layer calls SAP synchronously to check Inventory (Real-time).
3.  **Payment:** If stock exists, call Stripe to capture funds.
4.  **Fulfillment:** Publish `OrderConfirmed` event. Logistics App consumes event to schedule shipment.

### 3. Error Handling (Reliability)
*   **Dead Letter Queues (DLQ):** For failed messages (e.g., SAP downtime) to allow manual replay.
*   **Circuit Breaker:** Stop calling SAP if error rate > 10% to prevent cascading failure.

[... continues with monitoring and governance ...]
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
