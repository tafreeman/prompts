---
name: GDPR Compliance Assessment
description: Comprehensive ReAct+Reflection prompt for assessing GDPR compliance of data processing activities.
type: how_to
---

# GDPR Compliance Assessment

## Description

Conduct a systematic GDPR compliance assessment for data processing activities. Generate gap analysis and remediation plans based on the six GDPR principles and data subject rights.

## Prompt

You are an expert Data Protection Officer conducting a GDPR compliance assessment using a ReAct (Reasoning + Acting) pattern with self-critique reflection.

### Assessment Context
**Organization/System:** [org_or_system]
**Processing Activity:** [processing_description]
**Data Categories:** [data_categories]
**Data Subjects:** [data_subjects]
**Processing Purposes:** [purposes]

### Assessment Areas
1. **Lawfulness, Fairness, Transparency** (Art. 5(1)(a))
2. **Purpose Limitation** (Art. 5(1)(b))
3. **Data Minimization** (Art. 5(1)(c))
4. **Accuracy** (Art. 5(1)(d))
5. **Storage Limitation** (Art. 5(1)(e))
6. **Security** (Art. 5(1)(f))

### Output Format
| Principle | Compliance Status | Findings | Recommendations |
|-----------|-------------------|----------|-----------------|
| ... | Compliant/Gap | ... | ... |

## Variables

- `[org_or_system]`: Organization or system being assessed.
- `[processing_description]`: What data processing occurs.
- `[data_categories]`: Types of personal data processed.
- `[data_subjects]`: Whose data is processed.
- `[purposes]`: Why data is processed.

## Example

**Input**:
System: Customer Newsletter
Processing: Collect email, send weekly marketing emails
Data Categories: Email address, name, preferences
Data Subjects: Customers who opt-in
Purposes: Marketing communications

**Response**:
| Principle | Status | Findings | Recommendations |
|-----------|--------|----------|-----------------|
| Lawfulness | Compliant | Consent-based (Art. 6(1)(a)) | Maintain consent records |
| Purpose Limitation | Compliant | Single stated purpose | Document purpose clearly |
| Data Minimization | Gap | Collecting phone number but not using | Remove phone field |
| Storage Limitation | Gap | No retention policy defined | Add 2-year inactive deletion |
| Security | Compliant | TLS encryption, access controls | Continue monitoring |
