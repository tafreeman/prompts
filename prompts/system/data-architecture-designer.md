---
title: "Data Architecture Designer"
shortTitle: "Data Architecture Designer"
intro: "Designs enterprise data architectures"
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
  - "enterprise"
  - "data-architecture"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Data Architecture Designer

---

## Description

Designs enterprise data architectures

---

## Use Cases

- Data Architecture for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

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
