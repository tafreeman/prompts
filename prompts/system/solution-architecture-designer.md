---

title: "Solution Architecture Designer"
category: "system"
tags: ["architect", "solution-design", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Solution Architecture Designer

## Description

Designs comprehensive solution architectures

## Use Cases

- Solution Design for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design solution architecture for:

Business Problem: [problem]
Functional Requirements: [functional_req]
Non-functional Requirements: [nonfunctional_req]
Constraints: [constraints]
Integration Needs: [integrations]

Provide:
1. High-level architecture diagram
2. Component specifications
3. Technology stack recommendations
4. Integration patterns
5. Scalability considerations
6. Security architecture
```

## Variables

- `[constraints]`: Constraints
- `[functional_req]`: Functional Req
- `[integrations]`: Integrations
- `[nonfunctional_req]`: Nonfunctional Req
- `[problem]`: Problem

## Example Usage

**Input:**

```text
[problem]: Legacy monolithic e-commerce platform crashing during peak traffic events (Black Friday)
[functional_req]: Support 50k concurrent users, real-time inventory sync, personalized recommendations, omnichannel cart
[nonfunctional_req]: 99.99% uptime, <200ms page load, auto-scaling, disaster recovery RTO < 1 hour
[constraints]: AWS cloud, Java/Spring Boot backend, React frontend, budget cap $50k/month run rate
[integrations]: Salesforce CRM, SAP ERP, Stripe Payments, SendGrid Email
```

**Output:**

```text
## High-Level Architecture

**Pattern:** Event-Driven Microservices on AWS

1.  **Frontend Layer:**
    *   CloudFront CDN for static assets
    *   React SPA hosted on S3
    *   BFF (Backend for Frontend) pattern using GraphQL (AppSync)

2.  **API Gateway Layer:**
    *   AWS API Gateway for request routing, throttling, and auth
    *   Cognito for customer identity management

3.  **Service Layer (Microservices):**
    *   **Product Service:** ECS Fargate (read-heavy, cached)
    *   **Order Service:** Lambda (burst scaling)
    *   **Inventory Service:** ECS Fargate (high consistency)
    *   **Recommendation Service:** SageMaker endpoint

4.  **Data Layer:**
    *   **Operational DB:** Aurora PostgreSQL (Orders, Customers)
    *   **Cache:** ElastiCache Redis (Sessions, Product Catalog)
    *   **Search:** OpenSearch (Product search)
    *   **Event Bus:** EventBridge for async decoupling (OrderPlaced -> InventoryUpdate)

[... continues with component specs and integration patterns ...]
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
