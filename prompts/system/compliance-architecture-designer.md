---
name: Compliance Architecture Designer
description: Designs compliance-focused architectures
type: how_to
---

# Compliance Architecture Designer

## Description

Designs compliance-focused architectures for GDPR, HIPAA, PCI-DSS, SOX, and ISO 27001. Provides frameworks for data governance, privacy controls, audit logging, and automated compliance verification while maintaining operational efficiency and supporting multi-regulation requirements.

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Governance[Governance Layer]
        Policy[Policy Engine]
        Classify[Data Classification]
        Consent[Consent Management]
    end

    subgraph Controls[Control Layer]
        IAM[Identity & Access]
        Encrypt[Encryption Services]
        DLP[Data Loss Prevention]
    end

    subgraph Monitoring[Monitoring Layer]
        Audit[Audit Logging]
        SIEM[SIEM Platform]
        Alerts[Alert Management]
    end

    subgraph Data[Data Layer]
        PII[(PII Data Store)]
        Tokens[(Tokenization)]
        Archive[(Audit Archive)]
    end

    Policy --> IAM
    Policy --> Encrypt
    Classify --> DLP
    Consent --> PII
    IAM --> PII
    Encrypt --> PII
    DLP --> Audit
    PII --> Tokens
    Audit --> SIEM
    SIEM --> Alerts
    Audit --> Archive
```

## Use Cases

- Designing GDPR-compliant data processing architectures
- Building HIPAA-compliant healthcare information systems
- Implementing PCI-DSS compliant payment processing
- Creating SOX-compliant financial reporting systems
- Establishing multi-regulation compliance frameworks
- Architecting data residency solutions for global operations

## Variables

- `[application]`: Application name and description (e.g., "Multi-tenant HR SaaS platform")
- `[regulations]`: Regulatory requirements (e.g., "GDPR, SOC 2 Type II, ISO 27001")
- `[data_types]`: Data types handled (e.g., "PII (name, email), SPII (SSN, salary), financial records")
- `[deployment]`: Deployment model (e.g., "AWS multi-region with EU data residency requirements")

## Example

### Context
A global HR SaaS platform processing employee data across 30 countries needs to comply with GDPR, CCPA, and prepare for ISO 27001 certification.

### Input

```text
Regulatory Requirements: GDPR (EU), CCPA (California), ISO 27001 certification target
Business Domain: HR SaaS platform with 500+ enterprise customers
Data Sensitivity: Employee PII including SSN, salary, health benefits
Audit Requirements: Annual SOC 2 Type II audit, customer audit rights
```

### Expected Output

- **Framework**: Unified Control Framework mapping ISO 27001 to GDPR articles
- **Data Governance**: Auto-classification at ingestion, tenant-specific encryption keys
- **Privacy Controls**: Consent management service, automated DSAR handling
- **Retention**: Automated lifecycle policies with crypto-shredding for deletion
- **Audit Trail**: Immutable audit logs with 7-year retention

## Related Prompts

- [Security Architecture Specialist](security-architecture-specialist.md) - For security control implementation
- [Data Architecture Designer](data-architecture-designer.md) - For data governance frameworks
- [Disaster Recovery Architect](disaster-recovery-architect.md) - For business continuity compliance
- [Enterprise Integration Architect](enterprise-integration-architect.md) - For compliant data exchange
- [Cloud Architecture Consultant](cloud-architecture-consultant.md) - For cloud compliance certifications
