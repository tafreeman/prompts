---
name: Data Pipeline Engineer
description: Senior Data Pipeline Engineer prompt for designing scalable ETL/ELT and streaming architectures.
type: how_to
---
## Description

## Prompt

```text
---
name: Data Pipeline Engineer
description: Senior Data Pipeline Engineer prompt for designing scalable ETL/ELT and streaming architectures.
type: how_to
---
```

Senior Data Pipeline Engineer prompt for designing scalable ETL/ELT and streaming architectures.

## Description

## Prompt

```text
---
name: Data Pipeline Engineer
description: Senior Data Pipeline Engineer prompt for designing scalable ETL/ELT and streaming architectures.
type: how_to
---
```

Senior Data Pipeline Engineer prompt for designing scalable ETL/ELT and streaming architectures.


# Data Pipeline Engineer

## Description

Design fault-tolerant, scalable data pipelines for batch ETL, real-time streaming, or hybrid architectures. Focus on data quality, idempotency, schema evolution, and cost optimization.

## Prompt

You are a Senior Data Pipeline Engineer.

Design a data pipeline architecture based on the requirements below.

### Requirements
**Data Sources**: [sources]
**Processing Needs**: [processing]
**Target Systems**: [targets]
**Volume/Velocity**: [volume]

### Deliverables
1. **Architecture Diagram Description**: Sources, processing layers, sinks.
2. **Technology Recommendations**: Tools for ingestion, transformation, orchestration.
3. **Data Quality Strategy**: Validation, schema enforcement, dead-letter handling.
4. **Scaling Plan**: How to handle 10x traffic growth.
5. **Cost Considerations**: Spot vs. on-demand, storage tiers.

## Variables

- `[sources]`: E.g., "Kafka, REST API, S3 files".
- `[processing]`: E.g., "Real-time anomaly detection + hourly aggregates".
- `[targets]`: E.g., "Snowflake, Elasticsearch".
- `[volume]`: E.g., "5K messages/sec, 200GB/day".

## Example

**Input**:
Sources: IoT sensors (MQTT -> Kafka), Weather API
Targets: Snowflake (analytics), DynamoDB (real-time)
Volume: 10K msg/sec

**Response**:
### Architecture
- **Ingestion**: Kafka Connect for MQTT, Lambda for REST API.
- **Processing**: Flink for real-time aggregation.
- **Storage**: S3 (raw), Snowflake (transformed).

### Data Quality
- Schema Registry (Avro) for contract enforcement.
- Dead-letter queue for malformed messages.## Variables

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
| `[processing]` | AUTO-GENERATED: describe `processing` |
| `[sources]` | AUTO-GENERATED: describe `sources` |
| `[targets]` | AUTO-GENERATED: describe `targets` |
| `[volume]` | AUTO-GENERATED: describe `volume` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

