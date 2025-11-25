---

title: "Data Pipeline Engineer"
category: "developers"
tags: ["developer", "data-engineering", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Data Pipeline Engineer

## Description

Designs data processing pipelines

## Use Cases

- Data Engineering for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[data_sources]`: Data Sources
- `[processing]`: Processing
- `[scale]`: Scale
- `[targets]`: Targets

## Example Usage

**Input:**

```text
[data_sources]: IoT Sensors (MQTT Stream), Weather API (REST Polling), ERP System (SQL Batch)
[processing]: Real-time anomaly detection (Temp > 100F), Hourly aggregation of energy usage
[targets]: Snowflake (Data Warehouse), DynamoDB (Real-time Dashboard), S3 (Raw Lake)
[scale]: 1M events/minute peak, <1s latency for alerts
```

**Output:**

```text
## Data Pipeline Design

### 1. Pipeline Architecture (Lambda Architecture)
*   **Speed Layer:** Kinesis Data Streams -> Flink (Windowed Aggregation) -> DynamoDB.
*   **Batch Layer:** Kinesis Firehose -> S3 (Parquet) -> Snowpipe -> Snowflake.

### 2. Data Transformation Logic
*   **Normalization:** Convert all sensor units to metric (Celsius, Joules).
*   **Enrichment:** Join sensor stream with static "Device Metadata" (Location, Model) cached in Redis.

### 3. Error Handling and Recovery
*   **Bad Data:** Send malformed JSON to S3 "Dead Letter Bucket" for manual inspection.
*   **Backpressure:** Kinesis automatically buffers spikes; Flink handles checkpointing for exactly-once processing.

[... continues with monitoring and scalability ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Developer prompts in this category
- Check the developers folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
