---
name: Security Architecture Specialist
description: Designs secure system architectures
type: how_to
---
## Description

## Prompt

```mermaid
flowchart TB
    subgraph Perimeter[Perimeter Security]
        WAF[WAF]
        DDoS[DDoS Protection]
        Firewall[Firewall]
    end

    subgraph Identity[Identity Layer]
        IdP[Identity Provider]
        MFA[MFA]
        RBAC[RBAC/ABAC]
    end

    subgraph Network[Network Security]
        Segment[Network Segmentation]
        mTLS[mTLS/Zero Trust]
        VPN[VPN/Private Link]
    end

    subgraph Data[Data Protection]
        Encrypt[Encryption]
        KMS[Key Management]
        DLP[Data Loss Prevention]
    end

    subgraph Monitor[Security Monitoring]
        SIEM[SIEM]
        SOC[SOC/SOAR]
        Threat[Threat Intel]
    end

    WAF --> Firewall
    DDoS --> WAF
    Firewall --> IdP
    IdP --> MFA
    MFA --> RBAC
    RBAC --> Segment
    Segment --> mTLS
    mTLS --> Encrypt
    Encrypt --> KMS
    KMS --> DLP
    DLP --> SIEM
    SIEM --> SOC
    SOC --> Threat
```

Designs secure system architectures

## Description

## Prompt

```mermaid
flowchart TB
    subgraph Perimeter[Perimeter Security]
        WAF[WAF]
        DDoS[DDoS Protection]
        Firewall[Firewall]
    end

    subgraph Identity[Identity Layer]
        IdP[Identity Provider]
        MFA[MFA]
        RBAC[RBAC/ABAC]
    end

    subgraph Network[Network Security]
        Segment[Network Segmentation]
        mTLS[mTLS/Zero Trust]
        VPN[VPN/Private Link]
    end

    subgraph Data[Data Protection]
        Encrypt[Encryption]
        KMS[Key Management]
        DLP[Data Loss Prevention]
    end

    subgraph Monitor[Security Monitoring]
        SIEM[SIEM]
        SOC[SOC/SOAR]
        Threat[Threat Intel]
    end

    WAF --> Firewall
    DDoS --> WAF
    Firewall --> IdP
    IdP --> MFA
    MFA --> RBAC
    RBAC --> Segment
    Segment --> mTLS
    mTLS --> Encrypt
    Encrypt --> KMS
    KMS --> DLP
    DLP --> SIEM
    SIEM --> SOC
    SOC --> Threat
```

Designs secure system architectures


# Security Architecture Specialist

## Description

Designs comprehensive security architectures including zero-trust networks, identity management, data protection, and security monitoring. Provides strategies for threat mitigation, compliance, DevSecOps integration, and security operations while balancing security with usability and performance.

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Perimeter[Perimeter Security]
        WAF[WAF]
        DDoS[DDoS Protection]
        Firewall[Firewall]
    end

    subgraph Identity[Identity Layer]
        IdP[Identity Provider]
        MFA[MFA]
        RBAC[RBAC/ABAC]
    end

    subgraph Network[Network Security]
        Segment[Network Segmentation]
        mTLS[mTLS/Zero Trust]
        VPN[VPN/Private Link]
    end

    subgraph Data[Data Protection]
        Encrypt[Encryption]
        KMS[Key Management]
        DLP[Data Loss Prevention]
    end

    subgraph Monitor[Security Monitoring]
        SIEM[SIEM]
        SOC[SOC/SOAR]
        Threat[Threat Intel]
    end

    WAF --> Firewall
    DDoS --> WAF
    Firewall --> IdP
    IdP --> MFA
    MFA --> RBAC
    RBAC --> Segment
    Segment --> mTLS
    mTLS --> Encrypt
    Encrypt --> KMS
    KMS --> DLP
    DLP --> SIEM
    SIEM --> SOC
    SOC --> Threat
```

## Use Cases

- Designing zero-trust network architectures for enterprises
- Implementing identity and access management (IAM) solutions
- Building security monitoring and SIEM architectures
- Creating data protection strategies with encryption and DLP
- Architecting secure cloud landing zones
- Designing DevSecOps security gates and automation

## Variables

- `[application]`: Application name (e.g., "PCI-DSS Level 1 payment processing platform")
- `[threat_model]`: Threat model (e.g., "External attackers, insider threats, supply chain risks")
- `[compliance]`: Compliance requirements (e.g., "PCI-DSS, SOC 2, GDPR, HIPAA")
- `[data_classification]`: Data classification (e.g., "PAN data (Restricted), Customer PII (Confidential)")
- `[cloud_provider]`: Cloud provider (e.g., "AWS multi-region with GovCloud for regulated workloads")

## Example

### Context
A fintech company handling payment card data needs PCI-DSS compliant infrastructure.

### Input

```text
System: Payment processing platform with card-present and card-not-present transactions
Security Requirements: PCI-DSS Level 1, SOC 2 Type II, zero-trust architecture
Compliance Standards: PCI-DSS 4.0, SOC 2, GDPR for EU customers
Threat Landscape: Sophisticated attackers, state-sponsored threats, insider risk
```

### Expected Output

- **Identity**: Azure AD with PIM, MFA everywhere, just-in-time access
- **Network**: Micro-segmentation, mTLS between services
- **Data Protection**: HSM-backed encryption, tokenization for PAN
- **Monitoring**: Microsoft Sentinel with 24/7 SOC
- **DevSecOps**: SAST/DAST/SCA in pipeline, container scanning

## Related Prompts

- [Compliance Architecture Designer](compliance-architecture-designer.md) - For regulatory compliance
- [Cloud Architecture Consultant](cloud-architecture-consultant.md) - For secure cloud design
- [API Architecture Designer](api-architecture-designer.md) - For API security
- [DevOps Architecture Planner](devops-architecture-planner.md) - For DevSecOps integration
- [Disaster Recovery Architect](disaster-recovery-architect.md) - For security incident recovery## Variables

| Variable | Description |
|---|---|
| `[MFA]` | AUTO-GENERATED: describe `MFA` |
| `[SIEM]` | AUTO-GENERATED: describe `SIEM` |
| `[WAF]` | AUTO-GENERATED: describe `WAF` |

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
| `[API Architecture Designer]` | AUTO-GENERATED: describe `API Architecture Designer` |
| `[Cloud Architecture Consultant]` | AUTO-GENERATED: describe `Cloud Architecture Consultant` |
| `[Compliance Architecture Designer]` | AUTO-GENERATED: describe `Compliance Architecture Designer` |
| `[DDoS Protection]` | AUTO-GENERATED: describe `DDoS Protection` |
| `[Data Loss Prevention]` | AUTO-GENERATED: describe `Data Loss Prevention` |
| `[Data Protection]` | AUTO-GENERATED: describe `Data Protection` |
| `[DevOps Architecture Planner]` | AUTO-GENERATED: describe `DevOps Architecture Planner` |
| `[Disaster Recovery Architect]` | AUTO-GENERATED: describe `Disaster Recovery Architect` |
| `[Encryption]` | AUTO-GENERATED: describe `Encryption` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Firewall]` | AUTO-GENERATED: describe `Firewall` |
| `[Identity Layer]` | AUTO-GENERATED: describe `Identity Layer` |
| `[Identity Provider]` | AUTO-GENERATED: describe `Identity Provider` |
| `[Key Management]` | AUTO-GENERATED: describe `Key Management` |
| `[MFA]` | AUTO-GENERATED: describe `MFA` |
| `[Network Security]` | AUTO-GENERATED: describe `Network Security` |
| `[Network Segmentation]` | AUTO-GENERATED: describe `Network Segmentation` |
| `[Perimeter Security]` | AUTO-GENERATED: describe `Perimeter Security` |
| `[RBAC/ABAC]` | AUTO-GENERATED: describe `RBAC/ABAC` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[SIEM]` | AUTO-GENERATED: describe `SIEM` |
| `[SOC/SOAR]` | AUTO-GENERATED: describe `SOC/SOAR` |
| `[Security Monitoring]` | AUTO-GENERATED: describe `Security Monitoring` |
| `[Threat Intel]` | AUTO-GENERATED: describe `Threat Intel` |
| `[VPN/Private Link]` | AUTO-GENERATED: describe `VPN/Private Link` |
| `[WAF]` | AUTO-GENERATED: describe `WAF` |
| `[application]` | AUTO-GENERATED: describe `application` |
| `[cloud_provider]` | AUTO-GENERATED: describe `cloud_provider` |
| `[compliance]` | AUTO-GENERATED: describe `compliance` |
| `[data_classification]` | AUTO-GENERATED: describe `data_classification` |
| `[mTLS/Zero Trust]` | AUTO-GENERATED: describe `mTLS/Zero Trust` |
| `[threat_model]` | AUTO-GENERATED: describe `threat_model` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

