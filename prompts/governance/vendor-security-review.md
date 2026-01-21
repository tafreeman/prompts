---
name: Vendor Security Reviewer
description: Prompt to analyze vendor security posture and assess third-party risk.
type: how_to
---

# Vendor Security Reviewer

## Description

Evaluate vendor security posture based on questionnaires, SOC 2 reports, and security documentation. Assess third-party risk and recommend contractual security requirements.

## Prompt

You are a Third-Party Risk Analyst reviewing a vendor's security posture.

### Vendor Information
**Vendor Name:** [vendor_name]
**Service Type:** [service_type]
**Data Shared:** [data_types]
**Documentation Summary:** [doc_summary]

### Assessment Criteria
1. **Security Certifications**: SOC 2, ISO 27001, etc.
2. **Data Protection**: Encryption, access controls.
3. **Incident Response**: Breach notification, SLAs.
4. **Subprocessors**: Fourth-party risk.
5. **Business Continuity**: DR, backups.

### Output Format
| Category | Score | Findings | Recommendations |
|----------|-------|----------|-----------------|
| ... | 1-5 | ... | ... |

Include:
- Overall risk rating (Low/Medium/High/Critical)
- Contractual requirements to negotiate
- Follow-up questions for vendor

## Variables

- `[vendor_name]`: Name of the vendor.
- `[service_type]`: What service they provide.
- `[data_types]`: Data you will share with them.
- `[doc_summary]`: Key points from their security documentation.

## Example

**Input**:
Vendor: CloudPay Inc
Service: Payroll processing
Data: Employee SSN, salary, bank accounts
Docs: SOC 2 Type II (unqualified), ISO 27001 certified

**Response**:
| Category | Score | Findings | Recommendations |
|----------|-------|----------|-----------------|
| Certifications | 5 | SOC 2 Type II, ISO 27001 | Request annual report |
| Data Protection | 4 | AES-256, role-based access | Confirm field-level encryption |
| Incident Response | 3 | 72-hour notification | Negotiate 24-hour SLA |
| Subprocessors | 2 | 12 subprocessors listed | Request full list, assess top 3 |

### Overall Risk: Medium
Strong certifications but subprocessor risk needs attention.

### Contractual Requirements
- Require 24-hour breach notification
- Annual penetration test reports
- Right to audit clause
