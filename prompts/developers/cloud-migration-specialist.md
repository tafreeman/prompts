---
title: "Cloud Migration Specialist"
category: "developers"
tags: ["developer", "cloud-migration", "enterprise", "azure", "aws", "modernization"]
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-26"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Cloud Migration Specialist

## Description

Enterprise cloud migration architect specializing in lift-and-shift, re-platform, and modernization strategies. Uses AWS Cloud Adoption Framework (CAF) and Azure Well-Architected Framework to plan migrations with cost optimization, security hardening, and performance validation.

## Use Cases

- On-premise to cloud migrations (Azure, AWS, GCP)
- Datacenter exit strategies
- Legacy application modernization (monolith → microservices)
- Disaster recovery and business continuity planning
- Multi-cloud and hybrid cloud architectures

## Prompt

```text
You are a Cloud Migration Architect with expertise in Azure, AWS, and GCP.

Create a cloud migration plan for:

**Application**: [app_name]
**Current Infrastructure**: [current_infra]
**Target Cloud**: [target_cloud]
**Business Requirements**: [requirements]

Provide:
1. **Migration Assessment** (6 Rs: Rehost, Replatform, Repurchase, Refactor, Retire, Retain)
2. **Cloud Architecture Design** (Compute, storage, networking, database with Well-Architected principles)
3. **Migration Phases** (Proof-of-concept, pilot, production cutover with rollback plans)4. **Cost Optimization** (TCO analysis, Reserved Instances, rightsizing recommendations)
5. **Security Considerations** (Identity, network segmentation, encryption, compliance mapping)
6. **Performance Validation** (Load testing, disaster recovery, SLA targets)

Use tables for architecture comparisons and include Azure Calculator or AWS Pricing estimates.
```

## Variables

- `[app_name]`: Application name and architecture (e.g., "Legacy CRM System - Java/Oracle monolith, 5000 concurrent users")
- `[current_infra]`: Current hosting environment (e.g., "On-premise VMware ESXi 7.0, Oracle 11g RAC (2-node cluster), F5 load balancer")
- `[target_cloud]`: Target cloud provider and services (e.g., "Microsoft Azure - App Services, Azure SQL Managed Instance, Application Gateway")
- `[requirements]`: Business drivers and constraints (e.g., "Reduce licensing costs by 30%, achieve 99.9% SLA, enable geo-redundancy for DR, complete migration in 9 months")

## Example Usage

**Input:**

```text
Application: Legacy CRM System - Java 8 Monolith (Spring Framework 4.x)
- Architecture: 3-tier (Web → App → DB)
- Users: 5,000 concurrent (peak), 20K total
- Current Performance: Avg response time 800ms, 95th percentile 2.5s
- Database: Oracle 11g RAC (2-node cluster, 2TB data)
- Integrations: Salesforce (REST API), SAP (SOAP), internal LDAP

Current Infrastructure:
- Hosting: On-premise VMware ESXi 7.0 (3 hosts, 192GB RAM each)
- App Servers: 6x WebLogic 12c (Oracle JDK 8)
- Database: Oracle 11g RAC (2-node cluster)
- Load Balancer: F5 BIG-IP (hardware appliance)
- Storage: NetApp SAN (10TB provisioned)
- Network: Cisco ASA firewall, DMZ architecture

Target Cloud: Microsoft Azure
- Preference: PaaS over IaaS where possible
- Regions: Primary (East US 2), DR (West US 2)

Business Requirements:
- Reduce Oracle licensing costs by 30% ($500K/year savings target)
- Improve availability from 99.5% → 99.9% (4.4 hours → 8.76 hours downtime/year)
- Enable geo-redundancy for disaster recovery (RPO: 1 hour, RTO: 4 hours)
- Complete migration in 9 months (Go-Live: Sept 2026)
- Zero data loss during cutover window
- Maintain or improve current performance (800ms avg response → \u003c 600ms)
```

**Output:**

```markdown
# Cloud Migration Plan: Legacy CRM to Azure

**Migration Strategy**: Re-platform (Lift, Tinker, and Shift)  
**Target Go-Live**: September 2026 (9-month timeline)  
**Estimated Cost**: $420K/year (vs. $650K current on-prem = 35% savings)

---

## 1. Migration Assessment (6 Rs Framework)

### Application Component Analysis

| Component | Current | Migration Strategy | Rationale |
|-----------|---------|-------------------|-----------|
| **Web/App Tier** | WebLogic 12c (Java 8) | **Re-platform** → Azure App Service (Linux containers) | Eliminate WebLogic licensing; modernize to containerized deployment |
| **Database** | Oracle 11g RAC | **Re-platform** → Azure SQL Managed Instance | Reduce Oracle licensing 80% via SQL Server migration; SSMA tool available |
| **Load Balancer** | F5 BIG-IP | **Rehost** → Azure Application Gateway | Native Azure service; no hardware maintenance |
| **File Storage** | NetApp SAN | **Rehost** → Azure Files Premium | Lift-and-shift with SMB protocol compatibility |
| **LDAP** | On-prem Active Directory | **Repurchase** → Azure AD (Entra ID) | Cloud-native identity; SSO + MFA |
| **Monitoring** | Nagios | **Refactor** → Azure Monitor + App Insights | Modernize observability stack |

### Decision Matrix: Rehost vs. Replatform vs. Refactor

**Selected Strategy: Re-platform (85% of workload)**

**Rejected Alternatives**:
- ❌ **Rehost (Lift-and-Shift IaaS)**: Keeps Oracle 11g licensing costs; no cost savings achieved
- ❌ **Refactor (Microservices Rewrite)**: 18-month timeline exceeds 9-month constraint; high risk

---

## 2. Cloud Architecture Design (Azure Well-Architected)

### Conceptual Architecture

```

┌─────────────────────────────────────────────────────────────┐
│                   Azure Front Door (Global)                  │
│              CDN + WAF + DDoS Protection                      │
└──────────────┬──────────────────────────────┬────────────────┘
               │                              │
      ┌────────▼────────┐          ┌─────────▼─────────┐
      │  East US 2      │          │  West US 2 (DR)   │
      │  (Primary)      │          │  (Standby)        │
      └────────┬────────┘          └─────────┬─────────┘
               │                              │
      ┌────────▼─────────────────────────────▼───────────┐
      │     Azure App Service Plan (Premium v3)          │
      │  - 6x Linux containers (Java 17 + Tomcat 10)     │
      │  - Auto-scale: 6-12 instances                     │
      └────────┬──────────────────────────────────────────┘
               │
      ┌────────▼─────────────────────────────────────────┐
      │  Azure SQL Managed Instance (Business Critical)  │
      │  - 8 vCores, 32GB RAM                            │
      │  - Geo-replication: East US 2 ↔ West US 2        │
      │  - Automated backups (PITR: 35 days)             │
      └──────────────────────────────────────────────────┘

```

### Detailed Component Specifications

| Layer | Azure Service | SKU/Configuration | Monthly Cost | Notes |
|-------|---------------|-------------------|--------------|-------|
| **CDN/WAF** | Azure Front Door Premium | Standard tier | $280 | DDoS Protection Standard included |
| **Compute** | App Service Plan (Premium v3) | P2v3 (2 cores, 8GB) × 6 instances | $1,200 | Linux containers; auto-scale to 12 |
| **Database** | SQL Managed Instance - Business Critical | 8 vCores, 32GB RAM | $2,400 | 99.99% SLA; zone-redundant |
| **Storage** | Azure Files Premium | 2TB provisioned | $410 | SMB 3.0; 100K IOPS |
| **Networking** | VNet, App Gateway, VPN | Standard tier | $180 | Site-to-site VPN to on-prem (cutover) |
| **Monitoring** | Azure Monitor + App Insights | Standard tier | $150 | Custom metrics + APM |
| **Backup/DR** | Geo-replication + Azure Backup | West US 2 standby | $400 | RPO: 1 hour, RTO: 4 hours |
| **Total** | | | **$5,020/month** | **$60K/year** (vs. $650K on-prem) |

**Cost Savings**: $590K/year (91% reduction) — exceeds 30% target

---

## 3. Migration Phases (9-Month Timeline)

### Phase 1: Proof of Concept (Months 1-2)

**Goal**: Validate Oracle → Azure SQL migration feasibility

**Tasks**:
1. **Database Migration Assessment**:
   - Run SQL Server Migration Assistant (SSMA) on Oracle 11g schema
   - Generate compatibility report (expected: 85% auto-convertible, 15% manual remediation)
   - Identify PL/SQL stored procedures requiring T-SQL rewrite
2. **Non-Prod Environment Build** (Azure DevTest subscription):
   - Deploy App Service + SQL Managed Instance in East US 2
   - Migrate 10% sample dataset (200GB) via Azure Data Migration Service (DMS)
   - Run regression test suite (500 automated Selenium tests)
3. **Performance Baseline**:
   - Load test with JMeter (1,000 concurrent users)
   - Target: Avg response time \u003c 600ms (vs. 800ms current)

**Success Criteria**:
- ✅ 95% of regression tests pass
- ✅ Performance within 20% of current baseline
- ✅ Zero P0/P1 showstoppers identified

**Go/No-Go Decision**: Feb 28, 2026

---

### Phase 2: Pilot Migration (Months 3-5)

**Goal**: Migrate non-production environments + 10% of user base

**Tasks**:
1. **Full Data Migration** (Month 3):
   - Use Azure DMS for continuous replication (on-prem Oracle → Azure SQL MI)
   - Initial full load: 2TB (estimated 48 hours over 1Gbps link)
   - Incremental sync: Real-time CDC (Change Data Capture)
2. **Application Code Modernization** (Month 4):
   - Upgrade Java 8 → Java 17 (LTS)
   - Replace WebLogic-specific APIs with Spring Boot 3.x
   - Containerize app (Docker image → Azure Container Registry)
3. **Pilot Rollout** (Month 5):
   - Select 500 users (10% of total) from Sales Dept
   - Route pilot traffic via Azure Traffic Manager (weighted routing)
   - Run in parallel with on-prem for 4 weeks (shadowing mode)

**Rollback Plan**:
- DNS TTL = 5 minutes (fast failback to on-prem)
- Keep Oracle 11g in sync via bidirectional replication during pilot

---

### Phase 3: Production Cutover (Months 6-7)

**Goal**: Migrate 100% of users with \u003c4-hour downtime

**Cutover Weekend (July 4-6, 2026)**:

| Time | Activity | Owner | Rollback Trigger |
|------|----------|-------|------------------|
| **Fri 6pm** | Freeze Oracle writes; enable read-only mode | DBA | N/A |
| **Fri 7pm** | Final DMS sync (incremental changes since pilot) | Migration Team | Sync duration \u003e 4 hours |
| **Fri 11pm** | Validate data integrity (row counts, checksums) | QA Team | \u003e 1% data discrepancy |
| **Sat 2am** | DNS cutover: Point `crm.company.com` to Azure Front Door | Network Team | Health check failures |
| **Sat 3am** | Smoke tests (100 critical user scenarios) | QA Team | \u003e 5 failures |
| **Sat 6am** | Go-Live announcement (email blast to 20K users) | Comms Team | \u003e 10% error rate |
| **Sat 10am** | Monitor dashboards (Azure Monitor alerts) | On-call SRE | SLA breach (response time \u003e 1s) |

**Rollback Decision Point**: Saturday 10am (if \u003e 5% of users report issues)

---

### Phase 4: Stabilization & Optimization (Months 8-9)

**Goal**: Decommission on-prem; optimize Azure costs

**Tasks**:
1. **Decommission On-Prem** (Month 8):
   - Shut down Oracle 11g RAC (August 15, 2026)
   - Reclaim VMware licenses ($200K/year savings)
   - Archive final Oracle backup to Azure Blob (compliance: 7-year retention)
2. **Cost Optimization** (Month 9):
   - Purchase Azure Reserved Instances (3-year term = 40% discount)
   - Rightsizing: Reduce App Service from P2v3 → P1v3 if CPU \u003c 50%
   - Enable auto-shutdown for dev/test environments (weekends)

**Final Cost**:
- Current estimate: $60K/year
- Post-optimization: $420K/year with 3-year RI commitment

---

## 4. Cost Optimization (TCO Analysis)

### On-Premise vs. Azure - 3-Year Comparison

| Cost Category | Current (On-Prem) | Azure (Year 1) | Azure (Year 2-3 with RI) |
|---------------|-------------------|----------------|-------------------------|
| **Oracle Licensing** | $300K/year | $0 | $0 |
| **VMware Licensing** | $120K/year | $0 | $0 |
| **Hardware Refresh** | $150K/year (amortized) | $0 | $0 |
| **Data Center** | $50K/year (power, cooling, space) | $0 | $0 |
| **IT Labor** | $80K/year (2 DBAs + 1 SysAdmin) | $30K (reduced to 1 Cloud Ops) | $30K |
| **Azure Services** | — | $60K/year (on-demand) | $36K/year (40% RI discount) |
| **Migration Costs** | — | $150K (one-time) | $0 |
| **Total (3 Years)** | **$2.1M** | **$240K** | **$102K** |

**3-Year Savings**: $1.76M (84%)  
**Payback Period**: 3 months (migration cost recovered by Oracle license savings)

### Azure Cost Optimization Tactics

1. **Reserved Instances (RI)**: Commit to 3-year SQL MI + App Service RIs = 40% discount
2. **Auto-Scaling**: Scale down App Service to 3 instances during off-peak hours (10pm-6am) = 25% compute savings
3. **Azure Hybrid Benefit**: If you have existing Windows Server licenses, apply them to Azure VMs (not applicable here, using Linux)
4. **Dev/Test Pricing**: Use separate Azure subscription for non-prod (15% discount)

---

## 5. Security Considerations

### Identity & Access Management

| Security Control | On-Prem | Azure Implementation | Benefit |
|------------------|---------|----------------------|---------|
| **Authentication** | LDAP (cleartext passwords) | Azure AD (Entra ID) with MFA | Phishing-resistant; conditional access policies |
| **Authorization** | Hard-coded roles in app | Azure RBAC + App Registrations | Least-privilege; audit logs in Azure AD |
| **Secrets Management** | Hardcoded in `web.xml` | Azure Key Vault | Rotate secrets without app redeployment |

### Network Segmentation

```

Internet → Azure Front Door (WAF) → App Gateway (TLS offload) → App Service (Private Endpoint)
                                                                      ↓
                                                          Azure SQL MI (Private Endpoint)
                                                                      ↓
                                                          VNet Service Endpoints → Azure Storage

```

**Security Hardening**:
- ✅ No public IPs on App Service or SQL MI (private endpoints only)
- ✅ NSG (Network Security Group) rules: Deny all inbound except from App Gateway
- ✅ TLS 1.3 enforced; HTTP → HTTPS redirect
- ✅ Azure DDoS Protection Standard (automatic mitigation)

### Encryption

| Data State | On-Prem | Azure |
|------------|---------|-------|
| **At Rest** | Oracle TDE (Basic) | SQL MI TDE with customer-managed keys (Azure Key Vault) |
| **In Transit** | TLS 1.2 (app ↔ Oracle) | TLS 1.3 (end-to-end: client ↔ Azure) |
| **In Use** (SQL queries) | None | Always Encrypted (column-level encryption for PII) |

### Compliance Mapping

| Requirement | Current Compliance | Azure Service | Attestation |
|-------------|-------------------|---------------|-------------|
| **SOC 2 Type II** | Self-attested | Azure inherits Microsoft SOC 2 | Azure Trust Center |
| **ISO 27001** | Not certified | Azure SQL MI is ISO 27001 certified | Shared responsibility model |
| **GDPR** (EU users) | Manual DPO processes | Azure Policy + Data Residency (EU regions) | GDPR compliance toolkit |

---

## 6. Performance Validation

### Load Testing Plan (Month 6 - Pre-Cutover)

**Tool**: Apache JMeter  
**Scenario**: Simulate Black Friday peak load (10,000 concurrent users)

| Metric | Target (SLA) | Current (On-Prem) | Azure (Pilot Results) | Status |
|--------|--------------|-------------------|----------------------|--------|
| **Avg Response Time** | \u003c 600ms | 800ms | **520ms** | 🟢 35% improvement |
| **95th Percentile** | \u003c 1.5s | 2.5s | **1.2s** | 🟢 52% improvement |
| **Throughput** | \u003e 500 req/sec | 400 req/sec | **650 req/sec** | 🟢 63% improvement |
| **Error Rate** | \u003c 0.1% | 0.3% | **0.05%** | 🟢 Exceeds target |

**Performance Improvement Drivers**:
- Azure SQL MI has faster SSD storage (100K IOPS vs. 20K IOPS on NetApp SAN)
- App Service Premium v3 uses newer Intel CPUs (20% faster than on-prem VMware)
- Azure Front Door CDN reduces latency for static assets (images, CSS, JS)

### Disaster Recovery Testing

**Scenario**: Primary region (East US 2) failure  
**Procedure**:
1. Trigger manual failover to West US 2 (via Azure Portal)
2. Verify SQL MI geo-replica promotion (automated)
3. DNS failover to West US 2 App Service (manual via Azure Traffic Manager)

**DR Test Results** (July 2026):
- **RPO** (Recovery Point Objective): 5 minutes (exceeds 1-hour target)
- **RTO** (Recovery Time Objective): 45 minutes (exceeds 4-hour target)
- **Data Loss**: 0 rows (continuous geo-replication)

---

## Success Metrics

### Migration KPIs (Track Monthly)

| Metric | Baseline | Target | Actual (Post-Migration) |
|--------|----------|--------|------------------------|
| **Cost Savings** | $650K/year | -30% ($455K/year) | **-84% ($102K/year)** 🟢 |
| **Availability SLA** | 99.5% (43.8 hrs down/year) | 99.9% (8.76 hrs/year) | **99.95% (4.4 hrs/year)** 🟢 |
| **Avg Response Time** | 800ms | \u003c 600ms | **520ms** 🟢 |
| **Migration Timeline** | N/A | 9 months | **8.5 months** 🟢 |
| **Data Loss (Cutover)** | N/A | 0 rows | **0 rows** 🟢 |

---

## Rollback & Contingency Plans

### Scenario 1: SQL Migration Fails (\u003e 5% Data Loss)

**Trigger**: SSMA conversion \u003c 80% success rate  
**Fallback**: Keep Oracle 11g; migrate app tier only to Azure VMs (IaaS) → Defer database migration to Phase 2

### Scenario 2: Performance Regression (\u003e 1s Avg Response Time)

**Trigger**: Load test results fail SLA target  
**Mitigation**:
1. Scale up SQL MI: 8 vCores → 16 vCores (+$2.4K/month)
2. Enable SQL MI read replicas for reporting queries
3. Add Azure Redis Cache for session state ($200/month)

### Scenario 3: Cutover Weekend Overrun (\u003e 4-Hour Downtime)

**Rollback Plan**:
- Revert DNS to on-prem F5 load balancer (5-minute TTL)
- Re-enable Oracle 11g writes (remove read-only mode)
- Notify users: "Migration postponed to next maintenance window (August 1)"

```

## Tips

- **Start with Database Assessment First**: 80% of migration failures are database-related (schema incompatibility, performance regression). Run SSMA early (Month 1).
- **Use Native Cloud DB When Possible**: Migrating Oracle → Azure SQL MI saves 80% on licensing vs. running Oracle on Azure VMs (IaaS).
- **Pilot with Real Users, Not Just QA**: Synthetic load tests miss edge cases. Run pilot with 10% of production traffic for 30 days.
- **Negotiate Reserved Instances Early**: 3-year Azure RIs offer 40% discount but require upfront budget approval. Factor into TCO before migration kickoff.
- **Automate Rollback**: DNS-based rollback is fastest (5-min TTL). Never rely on manual steps during 2am cutover windows.
- **Monitor Cloud Costs Weekly**: Azure spending can spike unexpectedly (e.g., forgotten dev VMs). Set up budget alerts in Azure Cost Management.

## Related Prompts

- **[devops-architecture-planner](../system/devops-architecture-planner.md)** - For CI/CD pipeline setup post-migration
- **[data-pipeline-engineer](./data-pipeline-engineer.md)** - For ongoing data integration with cloud services
- **[security-code-auditor](./security-code-auditor.md)** - For pre-migration security assessment
