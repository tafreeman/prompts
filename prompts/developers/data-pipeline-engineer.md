---
title: "Data Pipeline Engineer"
shortTitle: "Data Pipeline Engineer"
intro: "You are a **Senior Data Pipeline Engineer** with expertise in designing scalable ETL/ELT architectures, real-time streaming systems, and data quality frameworks. You design pipelines that are fault-tolerant, observable, and cost-effective."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "data-engineering"
  - "developer"
  - "enterprise"
  - "developers"
author: "Prompts Library Team"
version: "2.0"
date: "2025-12-02"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---
# Data Pipeline Engineer

## Description

You are a **Senior Data Pipeline Engineer** with expertise in designing scalable ETL/ELT architectures, real-time streaming systems, and data quality frameworks. You follow **DataOps** principles and design pipelines that are fault-tolerant, observable, and cost-effective.

**Your Approach:**
- **Reliability First**: Design for failure with retries, dead-letter queues, and idempotent operations
- **Data Quality**: Implement validation at every stage with clear data contracts
- **Observability**: Metrics, alerting, and lineage tracking from day one
- **Cost Optimization**: Balance latency requirements against compute costs

---

## Use Cases

- Designing batch ETL pipelines for data warehousing
- Building real-time streaming architectures for analytics
- Migrating legacy pipelines to modern cloud-native solutions
- Implementing data quality validation frameworks
- Creating disaster recovery and data backfill strategies

---

## Prompt

```text
Design a data pipeline for:

Data Sources: [data_sources]
Processing Requirements: [processing]
Target Systems: [targets]
Volume and Velocity: [scale]

Include:
1. Pipeline architecture
2. Data transformation logic
3. Error handling and recovery
4. Monitoring and alerting
5. Scalability considerations
6. Data quality validation
```text
## Variables

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `[data_sources]` | Input data systems and formats | `PostgreSQL (CDC), Kafka topics, REST APIs, S3 files (CSV/Parquet)` |
| `[processing]` | Transformation and business logic requirements | `Join customer + orders, calculate rolling 7-day averages, deduplicate by event_id` |
| `[targets]` | Destination systems and formats | `Snowflake (analytics), Redis (cache), Elasticsearch (search), S3 (archive)` |
| `[scale]` | Volume, velocity, and latency requirements | `10M events/day batch`, `50K events/sec streaming`, `<5min latency` |

---

## Example Usage

**Input:**

```text
[data_sources]: IoT Sensors (MQTT Stream), Weather API (REST Polling), ERP System (SQL Batch)
[processing]: Real-time anomaly detection (Temp > 100F), Hourly aggregation of energy usage
[targets]: Snowflake (Data Warehouse), DynamoDB (Real-time Dashboard), S3 (Raw Lake)
[scale]: 1M events/minute peak, <1s latency for alerts
```text
**Output:**

```text
## Data Pipeline Design

### 1. Pipeline Architecture (Lambda Architecture)

```text
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│ IoT Sensors  │───▶│ Kinesis Streams │───▶│    Flink     │───▶ DynamoDB (RT)
│   (MQTT)     │    └─────────────────┘    │  (Anomaly)   │
└──────────────┘            │              └──────────────┘
                            ▼
                    ┌───────────────┐    ┌──────────────┐
                    │   Firehose    │───▶│   S3 Raw     │
                    └───────────────┘    │  (Parquet)   │
                                         └──────────────┘
                                                │
┌──────────────┐    ┌───────────────┐          ▼
│ Weather API  │───▶│   Airflow     │───▶ Snowflake (DW)
│   (REST)     │    │ (Hourly ETL)  │
└──────────────┘    └───────────────┘
                            ▲
┌──────────────┐            │
│ ERP System   │────────────┘
│   (SQL)      │
└──────────────┘
```sql
**Speed Layer:** Kinesis Data Streams → Flink (Windowed Aggregation) → DynamoDB
**Batch Layer:** Kinesis Firehose → S3 (Parquet) → Snowpipe → Snowflake

### 2. Data Transformation Logic

| Stage | Transformation | Output Schema |
|-------|---------------|---------------|
| Ingestion | Validate JSON schema, add `ingestion_ts` | `{device_id, temp_f, humidity, ts, ingestion_ts}` |
| Normalization | Convert Fahrenheit to Celsius | `{device_id, temp_c, humidity, ts}` |
| Enrichment | Join with device metadata (Redis lookup) | `{device_id, temp_c, location, building_id, ts}` |
| Aggregation | 1-hour tumbling window average | `{building_id, avg_temp, hour, event_count}` |

### 3. Error Handling and Recovery

```python
# Dead Letter Queue Pattern
class PipelineErrorHandler:
    def handle_error(self, record, error):
        error_record = {
            "original_record": record,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "retry_count": record.get("_retry_count", 0)
        }
        
        if error_record["retry_count"] < 3:
            # Retry with exponential backoff
            self.retry_queue.send(record, delay=2**error_record["retry_count"])
        else:
            # Send to DLQ for manual inspection
            self.dlq.send(error_record)
            self.alert("dlq_threshold_exceeded", record)
```text
**Recovery Patterns:**
| Failure Type | Detection | Recovery Action |
|--------------|-----------|-----------------|
| Malformed JSON | Schema validation | Send to DLQ, alert if >1% error rate |
| API timeout | HTTP 5xx / timeout | Retry 3x with exponential backoff |
| Destination unavailable | Connection refused | Circuit breaker, buffer to S3, replay |
| Data quality violation | Null checks, range validation | Quarantine record, continue pipeline |

### 4. Monitoring and Alerting

**Key Metrics (RED Method):**
| Metric | Query | Alert Threshold |
|--------|-------|-----------------|
| Rate | `sum(records_processed) by (pipeline)` | N/A (baseline) |
| Errors | `sum(records_failed) / sum(records_total)` | > 1% over 5min |
| Duration | `histogram_quantile(0.95, processing_latency)` | > 2x baseline |

**Alerting Rules:**
```yaml
# Prometheus alerting rules
groups:
  - name: pipeline_alerts
    rules:
      - alert: HighErrorRate
        expr: sum(rate(pipeline_errors_total[5m])) / sum(rate(pipeline_records_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pipeline error rate > 1%"
          
      - alert: ProcessingLagHigh
        expr: pipeline_consumer_lag > 100000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Consumer lag exceeds 100K messages"
```text
### 5. Scalability Considerations

| Dimension | Strategy | Implementation |
|-----------|----------|----------------|
| Horizontal | Partition by device_id | Kinesis: 10 shards (resharding API for peaks) |
| Vertical | Memory tuning | Flink: 4GB heap, 2GB managed memory per slot |
| Cost | Tiered storage | Hot: Kinesis (7 days), Warm: S3 IA (90 days), Cold: Glacier |

### 6. Data Quality Validation

```python
# Great Expectations Integration
@pipeline_stage("validation")
def validate_sensor_data(df):
    expectations = {
        "expect_column_values_to_not_be_null": ["device_id", "temp_c", "ts"],
        "expect_column_values_to_be_between": {
            "temp_c": {"min_value": -50, "max_value": 150}
        },
        "expect_column_values_to_be_unique": ["event_id"],
        "expect_table_row_count_to_be_between": {
            "min_value": 1000,  # Alert if batch is suspiciously small
            "max_value": 10000000
        }
    }
    
    results = validate(df, expectations)
    if not results.success:
        quarantine_failed_records(df, results)
        alert_data_quality_issue(results)
    
    return df[results.passed_rows]
```text
```text
## Tips

- **Start with the end in mind**: Define SLAs (latency, completeness, freshness) before designing architecture
- **Partition wisely**: Choose partition keys that distribute load evenly and match query patterns
- **Idempotency is crucial**: Design every stage to be safely re-runnable without duplicates
- **Schema evolution**: Use Avro/Protobuf with schema registry for forward/backward compatibility
- **Cost awareness**: For batch workloads, consider spot instances; for streaming, right-size based on actual throughput
- **Test data contracts**: Validate schemas at boundaries between teams/systems

---

## Related Prompts

- [Database Schema Designer](./database-schema-designer.md) - Design destination schemas
- [DevOps Pipeline Architect](./devops-pipeline-architect.md) - CI/CD for data pipelines
- [Cloud Migration Specialist](./cloud-migration-specialist.md) - Migrate legacy ETL to cloud
