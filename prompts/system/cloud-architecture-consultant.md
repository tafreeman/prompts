---
name: Cloud Architecture Consultant
description: Designs cloud-native architectures
type: how_to
---
## Description

## Prompt

```mermaid
flowchart TB
    subgraph Users
        Web[Web Users]
        Mobile[Mobile Users]
        API[API Consumers]
    end

    subgraph Edge[Edge Layer]
        CDN[CDN / WAF]
        DNS[Global DNS]
    end

    subgraph Compute[Compute Layer]
        K8s[Kubernetes Cluster]
        Serverless[Serverless Functions]
        Containers[Container Services]
    end

    subgraph Data[Data Layer]
        SQL[(SQL Database)]
        NoSQL[(NoSQL Store)]
        Cache[(Redis Cache)]
        Lake[(Data Lake)]
    end

    subgraph Platform[Platform Services]
        Queue[Message Queue]
        Events[Event Bus]
        Storage[Object Storage]
    end

    Users --> DNS
    DNS --> CDN
    CDN --> K8s
    CDN --> Serverless
    K8s --> SQL
    K8s --> Cache
    Serverless --> NoSQL
    K8s --> Queue
    Queue --> Events
    Events --> Lake
    Containers --> Storage
```

Designs cloud-native architectures

## Description

## Prompt

```mermaid
flowchart TB
    subgraph Users
        Web[Web Users]
        Mobile[Mobile Users]
        API[API Consumers]
    end

    subgraph Edge[Edge Layer]
        CDN[CDN / WAF]
        DNS[Global DNS]
    end

    subgraph Compute[Compute Layer]
        K8s[Kubernetes Cluster]
        Serverless[Serverless Functions]
        Containers[Container Services]
    end

    subgraph Data[Data Layer]
        SQL[(SQL Database)]
        NoSQL[(NoSQL Store)]
        Cache[(Redis Cache)]
        Lake[(Data Lake)]
    end

    subgraph Platform[Platform Services]
        Queue[Message Queue]
        Events[Event Bus]
        Storage[Object Storage]
    end

    Users --> DNS
    DNS --> CDN
    CDN --> K8s
    CDN --> Serverless
    K8s --> SQL
    K8s --> Cache
    Serverless --> NoSQL
    K8s --> Queue
    Queue --> Events
    Events --> Lake
    Containers --> Storage
```

Designs cloud-native architectures


# Cloud Architecture Consultant

## Description

Designs cloud-native architectures for scalable, resilient applications across AWS, Azure, and GCP. Provides recommendations for compute, storage, networking, and cost optimization strategies while addressing compliance, security, and disaster recovery requirements.

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Users
        Web[Web Users]
        Mobile[Mobile Users]
        API[API Consumers]
    end

    subgraph Edge[Edge Layer]
        CDN[CDN / WAF]
        DNS[Global DNS]
    end

    subgraph Compute[Compute Layer]
        K8s[Kubernetes Cluster]
        Serverless[Serverless Functions]
        Containers[Container Services]
    end

    subgraph Data[Data Layer]
        SQL[(SQL Database)]
        NoSQL[(NoSQL Store)]
        Cache[(Redis Cache)]
        Lake[(Data Lake)]
    end

    subgraph Platform[Platform Services]
        Queue[Message Queue]
        Events[Event Bus]
        Storage[Object Storage]
    end

    Users --> DNS
    DNS --> CDN
    CDN --> K8s
    CDN --> Serverless
    K8s --> SQL
    K8s --> Cache
    Serverless --> NoSQL
    K8s --> Queue
    Queue --> Events
    Events --> Lake
    Containers --> Storage
```

## Use Cases

- Migrating on-premises applications to cloud-native architectures
- Designing multi-region deployments for global user bases
- Implementing serverless architectures for event-driven workloads
- Building hybrid cloud solutions connecting on-premises and cloud
- Cost optimization through right-sizing and reserved capacity planning
- Disaster recovery and business continuity architecture

## Variables

- `[application]`: Application name and description (e.g., "Global video streaming platform with 50M subscribers")
- `[provider]`: Cloud provider (e.g., "AWS (primary), multi-region deployment")
- `[scalability]`: Scalability requirements (e.g., "Handle 10x traffic spikes during live events")
- `[compliance]`: Compliance requirements (e.g., "GDPR, CCPA, SOC 2 Type II")
- `[budget]`: Budget constraints (e.g., "$2M annual cloud spend, optimize for cost efficiency")

## Example

### Context
A streaming video platform needs to support 10 million concurrent viewers during live events, with content delivery to 50+ countries, while maintaining costs under $200K/month.

### Input

```text
Application: Global Video Streaming Platform
Cloud Provider: AWS (primary), with multi-CDN strategy
Scalability Needs: 10M concurrent viewers, 500k requests/sec, auto-scale 0 to peak in <5 min
Compliance Requirements: GDPR (EU), CCPA (California), content licensing geo-restrictions
Budget Constraints: $200k/month target, optimize for variable workloads
```

### Expected Output

- **Architecture Pattern**: Cell-based architecture with regional isolation
- **Compute**: EKS with Karpenter for rapid scaling, Lambda@Edge for personalization
- **Storage**: S3 Intelligent Tiering for video library, CloudFront for delivery
- **Cost Strategy**: Spot instances for transcoding (60-90% savings), reserved capacity for baseline
- **DR**: Active-active across 3 regions with Route53 health checks

## Related Prompts

- [Disaster Recovery Architect](disaster-recovery-architect.md) - For DR/BC planning
- [Performance Architecture Optimizer](performance-architecture-optimizer.md) - For cloud performance tuning
- [Security Architecture Specialist](security-architecture-specialist.md) - For cloud security controls
- [DevOps Architecture Planner](devops-architecture-planner.md) - For CI/CD in cloud
- [Microservices Architecture Expert](microservices-architecture-expert.md) - For container orchestration
- Check the system folder for similar templates## Variables

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
| `[(Data Lake)]` | AUTO-GENERATED: describe `(Data Lake)` |
| `[(NoSQL Store)]` | AUTO-GENERATED: describe `(NoSQL Store)` |
| `[(Redis Cache)]` | AUTO-GENERATED: describe `(Redis Cache)` |
| `[(SQL Database)]` | AUTO-GENERATED: describe `(SQL Database)` |
| `[API Consumers]` | AUTO-GENERATED: describe `API Consumers` |
| `[CDN / WAF]` | AUTO-GENERATED: describe `CDN / WAF` |
| `[Compute Layer]` | AUTO-GENERATED: describe `Compute Layer` |
| `[Container Services]` | AUTO-GENERATED: describe `Container Services` |
| `[Data Layer]` | AUTO-GENERATED: describe `Data Layer` |
| `[DevOps Architecture Planner]` | AUTO-GENERATED: describe `DevOps Architecture Planner` |
| `[Disaster Recovery Architect]` | AUTO-GENERATED: describe `Disaster Recovery Architect` |
| `[Edge Layer]` | AUTO-GENERATED: describe `Edge Layer` |
| `[Event Bus]` | AUTO-GENERATED: describe `Event Bus` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Global DNS]` | AUTO-GENERATED: describe `Global DNS` |
| `[Kubernetes Cluster]` | AUTO-GENERATED: describe `Kubernetes Cluster` |
| `[Message Queue]` | AUTO-GENERATED: describe `Message Queue` |
| `[Microservices Architecture Expert]` | AUTO-GENERATED: describe `Microservices Architecture Expert` |
| `[Mobile Users]` | AUTO-GENERATED: describe `Mobile Users` |
| `[Object Storage]` | AUTO-GENERATED: describe `Object Storage` |
| `[Performance Architecture Optimizer]` | AUTO-GENERATED: describe `Performance Architecture Optimizer` |
| `[Platform Services]` | AUTO-GENERATED: describe `Platform Services` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Security Architecture Specialist]` | AUTO-GENERATED: describe `Security Architecture Specialist` |
| `[Serverless Functions]` | AUTO-GENERATED: describe `Serverless Functions` |
| `[Web Users]` | AUTO-GENERATED: describe `Web Users` |
| `[application]` | AUTO-GENERATED: describe `application` |
| `[budget]` | AUTO-GENERATED: describe `budget` |
| `[compliance]` | AUTO-GENERATED: describe `compliance` |
| `[provider]` | AUTO-GENERATED: describe `provider` |
| `[scalability]` | AUTO-GENERATED: describe `scalability` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

