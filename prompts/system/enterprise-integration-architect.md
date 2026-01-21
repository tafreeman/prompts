---
name: Enterprise Integration Architect
description: Designs enterprise integration solutions
type: how_to
---

# Enterprise Integration Architect

## Description

Designs enterprise integration solutions including API-led connectivity, event-driven architectures, and B2B integration hubs. Provides strategies for connecting ERP, CRM, SaaS platforms, and partner systems while addressing performance, security, and hybrid cloud integration requirements.

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Sources[Source Systems]
        ERP[ERP System]
        CRM[CRM Platform]
        Legacy[Legacy Apps]
        SaaS[SaaS Apps]
    end

    subgraph Integration[Integration Layer]
        Gateway[API Gateway]
        ESB[Integration Platform]
        Queue[Message Queue]
        Events[Event Bus]
    end

    subgraph Processing[Processing Layer]
        Transform[Transformation]
        Orchestrate[Orchestration]
        Route[Routing Engine]
    end

    subgraph Targets[Target Systems]
        DataLake[(Data Lake)]
        Analytics[Analytics]
        Mobile[Mobile Apps]
        Partners[Partner APIs]
    end

    ERP --> Gateway
    CRM --> ESB
    Legacy --> ESB
    SaaS --> Queue
    Gateway --> Transform
    ESB --> Orchestrate
    Queue --> Events
    Events --> Route
    Transform --> DataLake
    Orchestrate --> Analytics
    Route --> Mobile
    Route --> Partners
```

## Use Cases

- Integrating ERP, CRM, and marketing automation platforms
- Building event-driven architectures with Apache Kafka or cloud event buses
- Creating B2B integration hubs for partner onboarding
- Migrating from ESB to API-led integration
- Implementing master data management (MDM) synchronization
- Designing hybrid integration platforms (on-prem + cloud)

## Variables

- `[systems]`: Systems to integrate (e.g., "Salesforce CRM, SAP ERP, Stripe payments, Logistics WMS")
- `[data_flow]`: Data flow requirements (e.g., "Real-time order sync, batch inventory updates nightly")
- `[performance]`: Performance requirements (e.g., "< 200ms API latency, 10K orders/hour peak")
- `[security]`: Security requirements (e.g., "PCI-DSS for payments, field-level encryption for PII")

## Example

### Context
A manufacturing company needs to integrate SAP ERP, Salesforce CRM, and logistics partners for Order-to-Cash visibility.

### Input
```text

Systems to Integrate: SAP S/4HANA, Salesforce, 15 logistics partners, e-commerce platform
Data Flow Requirements: Order → Fulfillment → Shipping → Delivery updates
Performance Requirements: 500 orders/minute peak, <5s end-to-end latency
Security Requirements: OAuth 2.0 for partners, field-level encryption for PII

```

### Expected Output

- **Pattern**: API-Led connectivity with experience, process, and system APIs
- **Platform**: MuleSoft Anypoint for orchestration, Kafka for events
- **Error Handling**: Dead letter queues, circuit breakers for resilience
- **Monitoring**: Centralized logging, distributed tracing, business KPIs

## Related Prompts

- [API Architecture Designer](api-architecture-designer.md) - For API design patterns
- [Data Architecture Designer](data-architecture-designer.md) - For data transformation
- [Microservices Architecture Expert](microservices-architecture-expert.md) - For service decomposition
- [Security Architecture Specialist](security-architecture-specialist.md) - For integration security
- [Cloud Architecture Consultant](cloud-architecture-consultant.md) - For cloud integration services
