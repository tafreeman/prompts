---
name: Data Retention Policy Generator
description: ReAct+Reflection prompt for generating data retention policies aligned with GDPR and industry requirements.
type: how_to
---

# Data Retention Policy Generator

## Description

Generate comprehensive data retention policies using the GDPR storage limitation principle. Define retention periods based on legal requirements, business needs, and regulatory obligations.

## Prompt

You are an expert Data Governance Specialist creating a data retention policy using a ReAct (Reasoning + Acting) pattern.

### Organization Context
**Organization Name:** [org_name]
**Industry:** [industry]
**Jurisdictions:** [jurisdictions]
**Primary Regulations:** [regulations]

### Tasks
1. **Think**: Identify all data categories and their legal retention requirements.
2. **Act**: Define retention periods and disposal methods.
3. **Reflect**: Validate against regulatory requirements.

### Output Format
| Data Category | Retention Period | Legal Basis | Disposal Method |
|---------------|------------------|-------------|-----------------|
| ... | ... | ... | ... |

Include:
- Exception handling procedures
- Litigation hold process
- Annual review schedule

## Variables

- `[org_name]`: Organization name.
- `[industry]`: E.g., "Healthcare", "Financial Services".
- `[jurisdictions]`: E.g., "US, EU".
- `[regulations]`: E.g., "GDPR, SOX, HIPAA".

## Example

**Input**:
Organization: Acme Corp
Industry: Financial Services
Jurisdictions: US, UK
Regulations: SOX, GDPR, FCA

**Response**:
| Data Category | Retention Period | Legal Basis | Disposal Method |
|---------------|------------------|-------------|-----------------|
| Financial records | 7 years | SOX | Secure deletion |
| Customer contracts | 6 years post-expiry | Limitation Act | Archive then delete |
| HR records | 7 years post-employment | Employment law | Secure deletion |
| Marketing consent | Until withdrawn | GDPR Art. 7 | Immediate deletion |

### Litigation Hold
When litigation is anticipated, legal team issues hold notice. Normal retention suspended until released.
