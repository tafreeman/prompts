---
name: Cloud Migration Specialist
description: You are an **Enterprise Cloud Migration Architect** specializing in lift-and-shift, re-platform, and modernization strategies. You use AWS Cloud Adoption Framework (CAF) and Azure Well-Architected Fra
type: how_to
---

# Cloud Migration Specialist

## Use Cases

- On-premise to cloud migrations (Azure, AWS, GCP)
- Datacenter exit strategies
- Legacy application modernization (monolith → microservices)
- Disaster recovery and business continuity planning
- Multi-cloud and hybrid cloud architectures

## Usage

**Input:**

```text
Application: Legacy CRM
Current Infrastructure: VMware + Oracle 11g + F5
Target Cloud: Azure
Business Requirements: 99.9% uptime, EU data residency, reduce cost by 30%
```

## 1. Migration Assessment (6 Rs Framework)

### Application Component Analysis

| Component | Current | Migration Strategy | Rationale |
| ----------- | --------- | ------------------- | ----------- |
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

### Phase 3: Production Cutover (Months 6-7)

**Goal**: Migrate 100% of users with \u003c4-hour downtime

**Cutover Weekend (July 4-6, 2026)**:

| Time | Activity | Owner | Rollback Trigger |
| ------ | ---------- | ------- | ------------------ |
| **Fri 6pm** | Freeze Oracle writes; enable read-only mode | DBA | N/A |
| **Fri 7pm** | Final DMS sync (incremental changes since pilot) | Migration Team | Sync duration \u003e 4 hours |
| **Fri 11pm** | Validate data integrity (row counts, checksums) | QA Team | \u003e 1% data discrepancy |
| **Sat 2am** | DNS cutover: Point `crm.company.com` to Azure Front Door | Network Team | Health check failures |
| **Sat 3am** | Smoke tests (100 critical user scenarios) | QA Team | \u003e 5 failures |
| **Sat 6am** | Go-Live announcement (email blast to 20K users) | Comms Team | \u003e 10% error rate |
| **Sat 10am** | Monitor dashboards (Azure Monitor alerts) | On-call SRE | SLA breach (response time \u003e 1s) |

**Rollback Decision Point**: Saturday 10am (if \u003e 5% of users report issues)

## 4. Cost Optimization (TCO Analysis)

### On-Premise vs. Azure - 3-Year Comparison

| Cost Category | Current (On-Prem) | Azure (Year 1) | Azure (Year 2-3 with RI) |
| --------------- | ------------------- | ---------------- | ------------------------- |
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

## 6. Performance Validation

### Load Testing Plan (Month 6 - Pre-Cutover)

**Tool**: Apache JMeter  
**Scenario**: Simulate Black Friday peak load (10,000 concurrent users)

| Metric | Target (SLA) | Current (On-Prem) | Azure (Pilot Results) | Status |
| -------- | -------------- | ------------------- | ---------------------- | -------- |
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

```text

## Related Prompts

- **[devops-architecture-planner](../system/devops-architecture-planner.md)** - For CI/CD pipeline setup post-migration
- **[data-pipeline-engineer](./data-pipeline-engineer.md)** - For ongoing data integration with cloud services
- **[security-code-auditor](./security-code-auditor.md)** - For pre-migration security assessment
