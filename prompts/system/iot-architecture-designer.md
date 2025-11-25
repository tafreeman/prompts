---

title: "IoT Architecture Designer"
category: "system"
tags: ["architect", "iot", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# IoT Architecture Designer

## Description

Designs IoT system architectures

## Use Cases

- IoT for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design IoT architecture for:

Use Case: [use_case]
Device Types: [devices]
Data Volume: [data_volume]
Connectivity: [connectivity]
Security Requirements: [security]

Provide:
1. Device architecture
2. Communication protocols
3. Data processing pipeline
4. Cloud integration
5. Security framework
6. Management platform
```

## Variables

- `[connectivity]`: Connectivity
- `[data_volume]`: Data Volume
- `[devices]`: Devices
- `[security]`: Security
- `[use_case]`: Use Case

## Example Usage

**Input:**

```text
[use_case]: Smart Factory Predictive Maintenance
[devices]: Vibration sensors (10k units), Temperature gauges (5k units), PLC controllers
[data_volume]: 1TB/day streaming telemetry
[connectivity]: LoRaWAN for sensors (low power), MQTT over Wi-Fi for controllers
[security]: Mutual TLS (mTLS) for device auth, end-to-end encryption, air-gapped OT network
```

**Output:**

```text
## IoT Architecture Design

### 1. Device Architecture
*   **Edge Gateway:** Aggregates sensor data via LoRaWAN, performs local anomaly detection (Edge ML), and batches uploads to cloud.
*   **Protocol:** MQTT over TLS for efficient, lightweight messaging.

### 2. Data Processing Pipeline
*   **Ingestion:** AWS IoT Core (MQTT Broker).
*   **Hot Path (Real-time):** IoT Rules -> Kinesis Data Streams -> Lambda (Alerting if temp > threshold).
*   **Cold Path (Analytics):** Kinesis Firehose -> S3 Data Lake -> Athena/Quicksight for historical trend analysis.

### 3. Security Framework
*   **Device Identity:** X.509 Certificates provisioned at manufacturing.
*   **Network:** Network segmentation separating OT (Operational Tech) from IT networks.

[... continues with management platform and cloud integration ...]
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
