# Data Pipeline Blueprint

A comprehensive workflow guide for designing, building, and operating data pipelines (ETL/ELT) from initial data discovery through production monitoring. This blueprint chains together prompts from the library to create an end-to-end data pipeline development process.

---

## Overview

This blueprint covers the full data pipeline lifecycle:

1. **Data Discovery** – Understanding source data
2. **Schema Design** – Modeling target data structures
3. **Pipeline Design** – Architecting ETL/ELT flows
4. **Validation Rules** – Ensuring data quality
5. **Monitoring & Alerting** – Observing production pipelines
6. **Incident Handling** – Responding to pipeline failures

---

## Workflow Stages

### Stage 1: Data Discovery & Quality Assessment

**Goal:** Understand source data and identify quality issues before building the pipeline.

**Prompts to Use:**

- **[Data Quality Assessment](../prompts/analysis/data-quality-assessment.md)**
  - Assess source data across six quality dimensions
  - Identify completeness, accuracy, consistency, timeliness, validity, and uniqueness issues
  - Generate quantified quality scores and recommended fixes

**Inputs:**

- Source dataset (sample or full)
- Schema/column definitions
- Context (how data will be used)

**Outputs:**

- Data Quality Assessment Report (see `docs/domain-schemas.md`)
- List of data issues to address
- Validation rules to implement

**Key Questions:**

- What percentage of critical fields are missing?
- Are there schema drift or type mismatch issues?
- What validation rules are currently violated?

---

### Stage 2: Schema Design

**Goal:** Design target schemas (warehouse/lakehouse) that support analytics and ML use cases.

**Prompts to Use:**

- **[Database Schema Designer](../prompts/developers/database-schema-designer.md)**
  - Design normalized or denormalized schemas
  - Plan indexing, partitioning, and constraints
  - Consider scalability and query performance

- **[Tree-of-Thoughts: Architecture Evaluator](../prompts/advanced-techniques/tree-of-thoughts-architecture-evaluator.md)**
  - Evaluate architecture options (star schema, snowflake, data vault, lakehouse)
  - Compare trade-offs (query performance, storage, complexity)

**Inputs:**

- Source data assessment from Stage 1
- Analytics requirements (reports, dashboards, ML models)
- Performance targets (query latency, data freshness)

**Outputs:**

- Target schema (tables, columns, types, keys, indexes)
- Partitioning strategy
- Data retention policy

**Key Decisions:**

- Normalize vs denormalize?
- What grain for fact tables?
- How to handle slowly changing dimensions (SCD Type 1/2/3)?

---

### Stage 3: Pipeline Design

**Goal:** Architect the ETL/ELT pipeline to transform source data into target schema.

**Prompts to Use:**

- **[Data Pipeline Engineer](../prompts/developers/data-pipeline-engineer.md)**
  - Design extraction, transformation, and loading steps
  - Plan scheduling, dependencies, and orchestration
  - Consider failure handling and retries

- **[Chain-of-Thought: Performance Analysis](../prompts/advanced-techniques/chain-of-thought-performance-analysis.md)**
  - Optimize pipeline performance (parallelization, batch sizing)
  - Identify bottlenecks (network, CPU, I/O)

**Inputs:**

- Source data assessment (Stage 1)
- Target schema (Stage 2)
- Data volume and freshness requirements

**Outputs:**

- Pipeline architecture diagram
- DAG (directed acyclic graph) for orchestration
- Transformation logic (SQL, Python, Spark, etc.)
- Incremental vs full refresh strategy

**Key Decisions:**

- ETL (transform before load) vs ELT (transform after load)?
- Batch vs streaming?
- How to handle late-arriving data?
- Idempotency: can we re-run safely?

---

### Stage 4: Validation Rules & Data Quality Checks

**Goal:** Implement automated data quality checks within the pipeline.

**Prompts to Use:**

- **[Data Quality Assessment](../prompts/analysis/data-quality-assessment.md)** (revisit)
  - Generate validation rules based on Stage 1 assessment
  - Define acceptance criteria for each stage of the pipeline

**Inputs:**

- Data quality issues from Stage 1
- Target schema constraints (NOT NULL, foreign keys, ranges)

**Outputs:**

- Validation rules (SQL checks, great_expectations tests, dbt tests)
- Failure actions (block, alert, log)
- Data quality SLOs (e.g., "completeness >95%")

**Example Validation Rules:**

```sql
-- Completeness check
SELECT COUNT(*) AS missing_count
FROM orders
WHERE customer_id IS NULL;
-- Fail if missing_count > 1000

-- Accuracy check
SELECT COUNT(*) AS negative_amounts
FROM orders
WHERE total_amount < 0;
-- Fail if negative_amounts > 0

-- Uniqueness check
SELECT order_id, COUNT(*) AS dup_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
-- Fail if dup_count > 0
```

---

### Stage 5: Monitoring & Alerting

**Goal:** Observe pipeline health and data quality in production.

**Prompts to Use:**

- **[Metrics and KPI Designer](../prompts/analysis/metrics-and-kpi-designer.md)**
  - Define pipeline SLIs (Service Level Indicators)
  - Set SLOs (latency, throughput, data quality scores)

**Inputs:**

- Pipeline design from Stage 3
- Validation rules from Stage 4
- Business requirements (data freshness, uptime)

**Outputs:**

- Monitoring dashboard (Datadog, Grafana, CloudWatch)
- Alerts (email, Slack, PagerDuty) for:
  - Pipeline failures
  - Data quality violations
  - Latency SLO breaches
  - Resource utilization spikes

**Key Metrics:**

- **Pipeline Execution Time** (p50, p95, p99)
- **Data Freshness** (time since last successful run)
- **Data Quality Scores** (completeness, accuracy, consistency %)
- **Error Rate** (% of failed records or jobs)
- **Resource Utilization** (CPU, memory, cost per run)

---

### Stage 6: Incident Handling & Root Cause Analysis

**Goal:** Quickly diagnose and fix pipeline failures.

**Prompts to Use:**

- **[Chain-of-Thought: Debugging](../prompts/advanced-techniques/chain-of-thought-debugging.md)**
  - Systematic root cause analysis for pipeline failures
  - Generate hypotheses, test them, propose fixes

- **[Reflection: Data Pipeline Risk Review](../prompts/advanced-techniques/reflection-data-pipeline-risk-review.md)** (if available)
  - Postmortem analysis after incidents
  - Identify preventive measures

**Inputs:**

- Error logs, stack traces, or alerts
- Pipeline code and configuration
- Recent changes (code deploys, schema changes, data source updates)

**Outputs:**

- Root cause analysis report
- Fix (code change, schema update, config tweak)
- Regression tests to prevent recurrence
- Postmortem document

**Common Failure Modes:**

- **Schema drift**: Source system added/removed columns
- **Data volume spike**: Unexpected traffic or batch size
- **Upstream system failure**: Source API or database down
- **Resource limits**: Out of memory, disk space, connection pool
- **Logic bugs**: Incorrect transformation, edge case not handled

---

## End-to-End Example

### Scenario: Building a Customer Analytics Pipeline

**Stage 1: Data Discovery**

Use **Data Quality Assessment** on source `customer_orders` table:

- Result: 8% missing `customer_id`, 2% negative `total_amount`, inconsistent `status` casing
- Action: Document issues, plan fixes

**Stage 2: Schema Design**

Use **Database Schema Designer** to create star schema:

- Fact table: `fact_orders` (order_id, customer_id, date_id, amount, quantity)
- Dimension tables: `dim_customers`, `dim_dates`, `dim_products`
- Partitioning: by `order_date` (monthly partitions)
- Indexes: on foreign keys and date columns

**Stage 3: Pipeline Design**

Use **Data Pipeline Engineer**:

- **Extract**: Incremental load from source DB (WHERE order_date > last_run_date)
- **Transform**: Join orders with customers/products, handle missing customer_id, convert status to lowercase
- **Load**: Upsert into fact/dim tables
- **Orchestration**: Airflow DAG, runs daily at 2 AM

**Stage 4: Validation Rules**

Implement checks:

- Completeness: `customer_id` missing rate <5%
- Accuracy: No negative `total_amount`
- Consistency: `status` matches enum ('pending', 'shipped', 'delivered', 'cancelled')
- Uniqueness: No duplicate `order_id`

**Stage 5: Monitoring**

Set up dashboard:

- Pipeline execution time (target: <15 minutes p95)
- Data freshness (target: <2 hours)
- Quality scores per dimension
- Alerts if any validation rule fails or execution time >30 minutes

**Stage 6: Incident Handling**

Pipeline fails with "Out of Memory" error:

- Use **Chain-of-Thought: Debugging** to analyze
- Hypothesis: Data volume spike (Black Friday sales)
- Root cause: Batch size too large for memory
- Fix: Reduce batch size, add pagination
- Regression test: Load test with 10x normal data volume

---

## Prompt Chaining Summary

| Stage | Primary Prompts | Outputs |
|-------|----------------|---------|
| 1. Data Discovery | Data Quality Assessment | Quality report, issues list, validation rules |
| 2. Schema Design | Database Schema Designer, Tree-of-Thoughts: Architecture Evaluator | Target schema, indexing strategy, partitioning plan |
| 3. Pipeline Design | Data Pipeline Engineer, Chain-of-Thought: Performance Analysis | Pipeline architecture, DAG, transformation logic |
| 4. Validation Rules | Data Quality Assessment (revisit) | Validation rules, acceptance criteria, SLOs |
| 5. Monitoring | Metrics and KPI Designer | Monitoring dashboard, alerts, SLIs/SLOs |
| 6. Incident Handling | Chain-of-Thought: Debugging, Reflection: Data Pipeline Risk Review | Root cause analysis, fixes, postmortems |

---

## Best Practices

### General

- **Start with data quality assessment** – Don't build pipelines on bad data
- **Design for idempotency** – Pipelines should be re-runnable without side effects
- **Validate early and often** – Catch issues in dev, not prod
- **Monitor everything** – Pipeline health, data quality, resource usage
- **Document assumptions** – What does "good data" look like?

### Performance

- **Incremental loads** – Only process new/changed data
- **Partitioning** – Enables parallel processing and faster queries
- **Batch sizing** – Balance memory usage and throughput
- **Parallelization** – Process independent partitions in parallel

### Reliability

- **Retries with backoff** – Handle transient failures
- **Alerting** – Detect failures fast
- **Rollback plans** – How to recover from bad data loads
- **Testing** – Unit tests for transforms, integration tests for full pipeline

### Governance

- **Data lineage** – Track where data comes from and where it goes
- **Access control** – Who can read/write data?
- **Retention policies** – How long to keep raw vs aggregated data
- **Audit logs** – Track all data changes

---

## Related Documents

- `docs/domain-schemas.md` – Structured output schemas for prompts
- `docs/sdlc-blueprint.md` – Software development lifecycle for code-heavy pipelines
- `docs/best-practices.md` – General prompt engineering guidance

## Related Prompts

### Discovery & Analysis

- [Data Quality Assessment](../prompts/analysis/data-quality-assessment.md)
- [Data Analysis Specialist](../prompts/analysis/data-analysis-specialist.md)
- [Trend Analysis Specialist](../prompts/analysis/trend-analysis-specialist.md)

### Design

- [Database Schema Designer](../prompts/developers/database-schema-designer.md)
- [Tree-of-Thoughts: Architecture Evaluator](../prompts/advanced-techniques/tree-of-thoughts-architecture-evaluator.md)

### Implementation

- [Data Pipeline Engineer](../prompts/developers/data-pipeline-engineer.md)
- [SQL Query Optimizer (Advanced)](../prompts/developers/sql-query-optimizer-advanced.md)

### Operations

- [Metrics and KPI Designer](../prompts/analysis/metrics-and-kpi-designer.md)
- [Chain-of-Thought: Debugging](../prompts/advanced-techniques/chain-of-thought-debugging.md)
- [Chain-of-Thought: Performance Analysis](../prompts/advanced-techniques/chain-of-thought-performance-analysis.md)

---

## Changelog

- 2025-11-18: Initial version based on ToT repository evaluation recommendations
