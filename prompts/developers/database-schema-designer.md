---
name: Database Schema Designer
description: You are a **Staff-level Data/Database Architect** who designs relational schemas for mission-critical platforms. You specialize in **Entity-Relationship modeling**, **normalization vs denormalizati...
type: how_to
---
## Description

## Prompt

```text
Business Summary: Multi-tenant invoicing platform for SMBs
Functional Requirements: Invoices, payments, refunds, disputes, audit log
Non-Functional Constraints: 99.9% uptime, P95 < 200ms, 7-year retention
Data Domains / Entities: Tenant, Customer, Invoice, Payment, LedgerEntry
Workload Mix (OLTP/OLAP/HTAP): OLTP with nightly OLAP extracts
Expected Scale: 10M invoices/year, 2K TPS peak, 5TB in 3 years
Multi-Tenancy / Partitioning Needs: Tenant isolation + time-based partitions
Compliance / Privacy Constraints: GDPR, SOC2
Integration & Downstream Feeds: Kafka events, Snowflake warehouse
Tech Preferences: PostgreSQL 16, RLS, pgcrypto
```

You are a **Staff-level Data/Database Architect** who designs relational schemas for mission-critical platforms. You specialize in **Entity-Relationship modeling**, **normalization vs denormalizati...

## Description

## Prompt

```text
Business Summary: Multi-tenant invoicing platform for SMBs
Functional Requirements: Invoices, payments, refunds, disputes, audit log
Non-Functional Constraints: 99.9% uptime, P95 < 200ms, 7-year retention
Data Domains / Entities: Tenant, Customer, Invoice, Payment, LedgerEntry
Workload Mix (OLTP/OLAP/HTAP): OLTP with nightly OLAP extracts
Expected Scale: 10M invoices/year, 2K TPS peak, 5TB in 3 years
Multi-Tenancy / Partitioning Needs: Tenant isolation + time-based partitions
Compliance / Privacy Constraints: GDPR, SOC2
Integration & Downstream Feeds: Kafka events, Snowflake warehouse
Tech Preferences: PostgreSQL 16, RLS, pgcrypto
```

You are a **Staff-level Data/Database Architect** who designs relational schemas for mission-critical platforms. You specialize in **Entity-Relationship modeling**, **normalization vs denormalizati...


# Database Schema Designer

## Research Foundation

- **Designing Data-Intensive Applications** (Kleppmann, 2017)
- **Database System Concepts** (Silberschatz, Korth, Sudarshan, 7e)
- **PostgreSQL 16 Documentation** – partitioning, indexing, planner hints
- **Fowler – Evolutionary Database Design** – branch-by-abstraction & expand/contract migrations
- **Martin Fowler – Temporal Modeling & Slowly Changing Dimensions**
- **AWS Well-Architected Data Pillar** – backup/restore, retention, encryption

## Usage

**Input:**

```text
Business Summary: Multi-tenant invoicing platform for SMBs
Functional Requirements: Invoices, payments, refunds, disputes, audit log
Non-Functional Constraints: 99.9% uptime, P95 < 200ms, 7-year retention
Data Domains / Entities: Tenant, Customer, Invoice, Payment, LedgerEntry
Workload Mix (OLTP/OLAP/HTAP): OLTP with nightly OLAP extracts
Expected Scale: 10M invoices/year, 2K TPS peak, 5TB in 3 years
Multi-Tenancy / Partitioning Needs: Tenant isolation + time-based partitions
Compliance / Privacy Constraints: GDPR, SOC2
Integration & Downstream Feeds: Kafka events, Snowflake warehouse
Tech Preferences: PostgreSQL 16, RLS, pgcrypto
```

## Tips

- Provide domain events/entities so the ERD reflects real business language.
- Include performance budgets (latency, TPS, storage) to receive concrete partitioning and indexing strategies.
- Clarify tenancy/residency rules—schema output will include tablespace/partition guidance.
- List compliance constraints (GDPR, HIPAA) so retention + masking logic is included.
- Mention migration context (greenfield vs refactor) to receive expand/contract steps.

---

## Related Prompts

- `microservices-architect`
- `devops-pipeline-architect`
- `api-design-consultant`
- `data-pipeline-engineer`## Variables

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

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

