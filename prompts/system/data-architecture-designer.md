---

title: "Data Architecture Designer"
category: "system"
tags: ["architect", "data-architecture", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Data Architecture Designer

## Description

Designs enterprise data architectures

## Use Cases

- Data Architecture for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design data architecture for:

Business Requirements: [requirements]
Data Sources: [sources]
Data Volume: [volume]
Analytics Needs: [analytics]
Governance Requirements: [governance]

Provide:
1. Data model design
2. Storage strategy
3. Data pipeline architecture
4. Governance framework
5. Quality management
6. Analytics platform
```

## Variables

- `[analytics]`: Analytics
- `[governance]`: Governance
- `[requirements]`: Requirements
- `[sources]`: Sources
- `[volume]`: Volume

## Example Usage

**Input:**

```text
[requirements]: Unified Customer 360 View, Real-time Personalization, Churn Prediction
[sources]: Salesforce CRM (Structured), SAP ERP (Structured), Website Clickstream (JSON), Zendesk Tickets (Unstructured)
[volume]: 500GB/day ingestion, 2PB total retention
[analytics]: Real-time dashboards (Tableau), Ad-hoc SQL queries, ML model training
[governance]: GDPR "Right to be Forgotten", Data Quality score > 95%
```

**Output:**

```text
## Data Architecture Design

### 1. Data Model Design (Lakehouse)
*   **Bronze Layer (Raw):** Immutable landing zone for all source data (Parquet format).
*   **Silver Layer (Cleansed):** Conformed dimensions, PII tokenized, data quality checks applied.
*   **Gold Layer (Curated):** Aggregated "Customer 360" tables optimized for BI.

### 2. Storage Strategy
*   **Data Lake:** S3 (Standard for hot, Glacier Deep Archive for >3 years).
*   **Warehouse:** Snowflake (Separation of storage and compute).

### 3. Data Pipeline Architecture
*   **Ingestion:** Kafka Connect for real-time streams (Clickstream), Airbyte for batch (CRM/ERP).
*   **Transformation:** dbt (Data Build Tool) for SQL-based transformations in Snowflake.
*   **Orchestration:** Airflow for dependency management.

[... continues with governance and quality management ...]
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
