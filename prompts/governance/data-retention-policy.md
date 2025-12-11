---
title: "Data Retention Policy Generator"
shortTitle: "Retention Policy"
intro: "A ReAct+Reflection prompt for generating comprehensive data retention policies aligned with GDPR data minimization principles, industry requirements, and legal obligations."
type: "how_to"
difficulty: "intermediate"
audience:
  - "solution-architect"
  - "backend-engineer"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "privacy"
  - "compliance"
  - "gdpr"
  - "data-management"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-05"
governance_tags:
  - "requires-human-review"
  - "compliance-critical"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "GDPR"
  - "UK-GDPR"
  - "CCPA"
  - "HIPAA"
  - "SOX"
---
# Data Retention Policy Generator

---

## Description

A comprehensive prompt for generating data retention policies that balance regulatory requirements (GDPR data minimization), legal obligations (litigation holds, tax records), and business needs. Uses ReAct reasoning to systematically analyze data categories, determine retention periods, and create actionable deletion schedules. Essential for DPOs, compliance teams, and data governance professionals.

---

## Research Foundation

**Regulatory Basis:**
- GDPR Article 5(1)(e) - Storage limitation principle ("kept no longer than necessary")
- GDPR Article 17 - Right to erasure implications
- GDPR Recitals 39, 65 - Retention period guidance

**Industry Standards:**
- ISO 15489 - Records Management
- ARMA Generally Accepted Recordkeeping Principles

**Methodology:**
- ReAct reasoning pattern (Yao et al., ICLR 2023) for systematic analysis
- Self-Refine reflection (Madaan et al., NeurIPS 2023) for policy validation

**Key Legal Retention Requirements (Examples):**
- Financial records: 6-7 years (tax, SOX)
- Employment records: 3-7 years post-employment
- Healthcare records: 6-10+ years (HIPAA, local laws)
- Contract documents: 6+ years after expiry
- Litigation holds: Duration of legal proceedings

---

## Use Cases

- GDPR-compliant retention policy development
- Records management schedule creation
- Data minimization initiatives
- Legacy data cleanup planning
- M&A due diligence preparation
- Audit response documentation
- Storage cost optimization
- Privacy by design implementation

---

## Prompt

```text
You are an expert Data Governance Specialist creating a comprehensive data retention policy using a ReAct (Reasoning + Acting) pattern with self-critique reflection.

## Organization Context

**Organization Name:** [ORGANIZATION_NAME]
**Industry:** [INDUSTRY]
**Jurisdictions:** [JURISDICTIONS]
**Primary Regulations:** [REGULATIONS]
**Data Processing Activities:** [PROCESSING_SUMMARY]

**Existing Policies:**
- [LIST_EXISTING_POLICIES]

**Key Systems:**
- [LIST_KEY_SYSTEMS]

---

## Phase 1: Data Inventory Analysis

### Think
First, we must understand what data the organization processes to determine appropriate retention periods.

### Act
Catalog data categories:

| Data Category | Description | Examples | Source Systems | Volume Estimate |
|---------------|-------------|----------|----------------|-----------------|
| Identity Data | Information identifying individuals | Name, DOB, ID numbers | CRM, HR | [Volume] |
| Contact Data | Communication details | Email, phone, address | CRM, Marketing | [Volume] |
| Financial Data | Transaction and payment info | Bank details, invoices | ERP, Payment | [Volume] |
| Employment Data | HR and employee records | Contracts, performance | HRIS, Payroll | [Volume] |
| Customer Data | Product/service usage | Orders, preferences | CRM, Analytics | [Volume] |
| Technical Data | System and device info | IP, logs, device IDs | IT Systems | [Volume] |
| Marketing Data | Consent and campaigns | Opt-ins, responses | Marketing | [Volume] |
| Legal Data | Contractsarkend disputes | Agreements, claims | Legal, DMS | [Volume] |
| Health Data | Medical information | Records, insurance | HR, Benefits | [Volume] |

### Observe
Document any data categories not captured above.

### Reflect
Is the data inventory comprehensive? Are there shadow IT or undocumented data stores?

---

## Phase 2: Legal Requirements Analysis

### Think
Determine all legal and regulatory retention requirements by jurisdiction.

### Act
Map legal requirements:

**Regulatory Requirements:**

| Regulation | Requirement | Data Types | Minimum Period | Maximum Period | Citation |
|------------|-------------|------------|----------------|----------------|----------|
| GDPR | Storage limitation | All personal data | - | "No longer than necessary" | Art. 5(1)(e) |
| GDPR | Security of processing | Breach records | 72 hours to report | Document indefinitely | Art. 33 |
| [JURISDICTION] Tax | Financial records | Tax documents | 6 years | - | [Citation] |
| [JURISDICTION] Employment | Employee records | HR files | 3-7 years | - | [Citation] |
| SOX | Financial records | Audit trails | 7 years | - | Section 802 |
| HIPAA | Medical records | PHI | 6 years | State-dependent | §164.530(j) |
| PCI-DSS | Cardholder data | Payment records | 1 year min audit trail | Minimize storage | Req 3 |
| [INDUSTRY] | [Requirement] | [Data Types] | [Period] | - | [Citation] |

**Contractual Obligations:**

| Contract Type | Retention Clause | Duration | Notes |
|---------------|------------------|----------|-------|
| Customer contracts | Audit provisions | Contract + [X] years | [Notes] |
| Vendor agreements | Record keeping | [Duration] | [Notes] |
| Insurance | Claims history | Policy + [X] years | [Notes] |

### Observe
Note any conflicts between regulatory requirements.

### Reflect
Are all applicable jurisdictions covered? What is the most restrictive requirement per category?

---

## Phase 3: Business Needs Assessment

### Think
Balance legal minimums with legitimate business purposes for retention.

### Act
Document business justifications:

| Data Category | Business Purpose | Legitimate Interest | Proposed Retention | Justification |
|---------------|------------------|---------------------|-------------------|---------------|
| Customer history | Service improvement | Performance of contract | [Period] | [Justification] |
| Analytics data | Product development | Legitimate interest | [Period] | [Justification] |
| Support tickets | Quality assurance | Contract performance | [Period] | [Justification] |
| Marketing preferences | Personalization | Consent | Until withdrawal | Ongoing consent |
| Prospect data | Sales pipeline | Legitimate interest | [Period] | [Justification] |

**Data Minimization Review:**
- [ ] Can purpose be achieved with less data?
- [ ] Can retention period be shortened?
- [ ] Can data be anonymized instead of deleted?
- [ ] Are all categories still necessary?

### Observe
Document any business requests that conflict with minimization principles.

### Reflect
Is each retention period justifiable and proportionate?

---

## Phase 4: Retention Schedule Creation

### Think
Synthesize legal requirements and business needs into a unified retention schedule.

### Act
Create retention schedule:

**Master Retention Schedule:**

| Ref | Data Category | Subcategory | Retention Period | Trigger Event | Legal Basis | Review Cycle |
|-----|---------------|-------------|------------------|---------------|-------------|--------------|
| R001 | Identity Data | Customer identity | 7 years | Account closure | Contract + Tax | Annual |
| R002 | Identity Data | Employee identity | Employment + 7 years | Termination | Employment law | Annual |
| R003 | Contact Data | Customer contact | Account active + 2 years | Last activity | Legitimate interest | Annual |
| R004 | Contact Data | Marketing contacts | Until consent withdrawal | Unsubscribe | Consent | Quarterly |
| R005 | Financial Data | Transaction records | 7 years | Transaction date | Tax/SOX | Annual |
| R006 | Financial Data | Payment card data | Transaction only | Transaction complete | PCI-DSS | Immediate |
| R007 | Employment Data | Payroll records | Employment + 7 years | Termination | Tax/Employment | Annual |
| R008 | Employment Data | Performance reviews | Employment + 3 years | Termination | Legitimate interest | Annual |
| R009 | Customer Data | Service usage | 3 years | Service end | Legitimate interest | Annual |
| R010 | Customer Data | Support tickets | 2 years | Ticket closure | Contract | Annual |
| R011 | Technical Data | Access logs | 2 years | Log creation | Security | Quarterly |
| R012 | Technical Data | Security logs | 3 years | Log creation | Security/Audit | Quarterly |
| R013 | Marketing Data | Campaign records | 3 years | Campaign end | Legitimate interest | Annual |
| R014 | Marketing Data | Consent records | Consent duration + 3 years | Consent withdrawal | Accountability | Annual |
| R015 | Legal Data | Contracts | Contract + 6 years | Contract expiry | Legal claims | Annual |
| R016 | Legal Data | Litigation records | Resolution + 7 years | Case closure | Legal claims | As needed |
| R017 | Health Data | Employee health | Employment + [State law] | Termination | HIPAA/State | Annual |

### Observe
Verify no conflicts between schedule entries.

---

## Phase 5: Deletion Procedures

### Think
Define clear procedures for data deletion when retention periods expire.

### Act
Document deletion procedures:

**Deletion Process:**

```markdown
1. IDENTIFICATION
   - Run retention schedule report monthly
   - Flag records past retention period
   - Verify no litigation holds apply

2. REVIEW
   - Data owner reviews flagged records
   - Confirm no extended retention needed
   - Document approval for deletion

3. EXECUTION
   - Primary system deletion
   - Backup inclusion in next cycle
   - Third-party processor notification
   - Audit trail creation

4. VERIFICATION
   - Confirm deletion complete
   - Update data inventory
   - Generate deletion certificate
```

**Deletion Methods by Data Type:**

| Data Type | Primary Method | Backup Handling | Verification |
|-----------|----------------|-----------------|--------------|
| Structured DB | Hard delete | Include in backup rotation | Audit query |
| Files/Documents | Secure delete | Archive deletion | Storage audit |
| Cloud storage | API deletion + retention policy | Automated | Provider confirmation |
| Physical media | Certified destruction | Same | Destruction certificate |
| Third-party | Processor notification | Contract clause | Written confirmation |

**Litigation Hold Procedures:**
- Hold notice distribution
- Suspension of automated deletion
- Legal review before release
- Documentation requirements

### Observe
Ensure deletion methods meet security requirements.

### Reflect
Are deletion procedures auditable and verifiable?

---

## Phase 6: Implementation Roadmap

### Think
Create a practical implementation plan for the retention policy.

### Act
Develop implementation plan:

**Phase 1: Foundation (Month 1-2)**
| Task | Owner | Deliverable | Timeline |
|------|-------|-------------|----------|
| Policy approval | [Owner] | Signed policy | Week 2 |
| Stakeholder training | [Owner] | Training records | Week 4 |
| System inventory | [Owner] | System register | Week 4 |
| Data mapping | [Owner] | Data flow diagrams | Week 6 |

**Phase 2: Technical Implementation (Month 3-4)**
| Task | Owner | Deliverable | Timeline |
|------|-------|-------------|----------|
| Automated retention rules | [Owner] | Configured systems | Week 10 |
| Deletion workflows | [Owner] | Workflow documentation | Week 12 |
| Audit logging | [Owner] | Log configuration | Week 14 |
| Testing | [Owner] | Test results | Week 16 |

**Phase 3: Operationalization (Month 5-6)**
| Task | Owner | Deliverable | Timeline |
|------|-------|-------------|----------|
| First deletion cycle | [Owner] | Deletion report | Week 18 |
| Exception handling | [Owner] | Exception log | Week 20 |
| Policy refinement | [Owner] | Updated policy | Week 22 |
| Ongoing monitoring | [Owner] | KPI dashboard | Week 24 |

### Observe
Identify resource requirements and dependencies.

---

## Phase 7: Self-Critique Reflection

### Compliance Check

**GDPR Alignment:**
- [ ] Storage limitation principle addressed?
- [ ] Data minimization evidenced?
- [ ] Subject rights considered (erasure)?
- [ ] Accountability documented?

**Legal Coverage:**
- [ ] All jurisdictions covered?
- [ ] Industry requirements included?
- [ ] Contractual obligations mapped?
- [ ] Litigation hold procedures defined?

**Operational Viability:**
- [ ] Retention periods realistic?
- [ ] Deletion procedures feasible?
- [ ] Responsibilities assigned?
- [ ] Review cycles scheduled?

### Gap Analysis

| Gap | Risk | Remediation |
|-----|------|-------------|
| [Gap] | [Risk] | [Action] |

### Policy Quality Score

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Regulatory coverage | [X] | [Notes] |
| Clarity | [X] | [Notes] |
| Implementability | [X] | [Notes] |
| Completeness | [X] | [Notes] |
| **Average** | [X] | |

---

## Output Format

### 1. Executive Summary
- Policy scope and objectives
- Key retention periods summary
- Implementation timeline
- Resource requirements

### 2. Data Retention Policy Document
```markdown
[ORGANIZATION_NAME] DATA RETENTION POLICY

Version: 1.0
Effective Date: [DATE]
Review Date: [DATE]
Owner: [DPO/Legal]

1. Purpose and Scope
2. Definitions
3. Retention Principles
4. Retention Schedule (see Appendix A)
5. Deletion Procedures
6. Exceptions and Holds
7. Roles and Responsibilities
8. Monitoring and Review
9. Related Policies
10. Approval

Appendix A: Master Retention Schedule
Appendix B: Deletion Request Form
Appendix C: Litigation Hold Notice Template
```

### 3. Master Retention Schedule
[Full schedule table]

### 4. Implementation Plan
[Phased roadmap]

### 5. Governance Framework
- Policy owner
- Review frequency
- Exception process
- Audit requirements
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[ORGANIZATION_NAME]` | Organization name | "Acme Corporation" |
| `[INDUSTRY]` | Industry sector | "Financial Services" |
| `[JURISDICTIONS]` | Operating jurisdictions | "EU, UK, USA (CA, NY)" |
| `[REGULATIONS]` | Key regulations | "GDPR, SOX, CCPA" |
| `[PROCESSING_SUMMARY]` | Main processing activities | "Customer management, payroll" |
| `[LIST_EXISTING_POLICIES]` | Current policies | "Privacy Policy v2.1, Security Policy" |
| `[LIST_KEY_SYSTEMS]` | Main systems | "Salesforce, Workday, SAP" |

---

## Example

```text
## Data Retention Policy: Financial Services

### 1. Policy Scope
Applies to all customer financial records, employee data, and operational logs within the EU and UK jurisdictions.

### 2. Data Categories & Retention Periods

| Data Category | Retention Period | Trigger Event | Rationale |
|---------------|------------------|---------------|-----------|
| **Customer KYC Data** | 5 Years | Account Closure | AML Regulations (Money Laundering Regs 2017) |
| **Transaction Logs** | 7 Years | Transaction Date | Tax Audits (HMRC requirement) |
| **Employee Contracts** | 6 Years | Termination | Limitation Act 1980 (Contract claims) |
| **Marketing Consent** | 2 Years | Last Interaction | GDPR Storage Limitation (Recital 39) |
| **Server Access Logs** | 90 Days | Creation Date | Security Incident Response (NIST recommendation) |

### 3. Deletion Procedures
*   **Automated:** Transaction logs in "CoreDB" are purged by daily cron job `purge_logs.sh`.
*   **Manual:** HR Manager reviews "Leavers Folder" quarterly for deletion.

### 4. Litigation Hold Protocol
*   **Trigger:** Receipt of Legal Hold Notice from General Counsel.
*   **Action:** Suspend automated deletion for named custodians/accounts immediately.
```

---

## Tips

- **Start with legal minimums** - Then add only justified business extensions
- **Involve legal early** - Retention requirements vary by jurisdiction
- **Automate where possible** - Manual deletion is error-prone
- **Document everything** - Accountability requires evidence
- **Review annually** - Requirements and business needs change
- **Consider anonymization** - Alternative to deletion for analytics
- **Test deletion** - Verify data is actually removed
- **Include backups** - Often forgotten in retention planning
- **Plan for exceptions** - Litigation holds, regulatory investigations

---

## Related Prompts

- [GDPR Compliance Assessment](gdpr-compliance-assessment.md) - Overall compliance check
- [Privacy Impact Assessment](privacy-impact-assessment.md) - For new processing
- [Data Subject Request Handler](data-subject-request-handler.md) - For deletion requests
