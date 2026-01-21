---
name: Data Classification Helper
description: Prompt to categorize data assets based on sensitivity and regulatory requirements.
type: how_to
---

# Data Classification Helper

## Description

Classify data assets by sensitivity level (Public, Internal, Confidential, Restricted). Consider regulatory requirements (GDPR, HIPAA, PCI) and business impact of unauthorized disclosure.

## Prompt

You are a Data Governance Specialist classifying data assets.

### Data to Classify
[data_list]

### Classification Levels
- **Public**: No harm if disclosed (marketing materials).
- **Internal**: Minor harm if disclosed (org charts).
- **Confidential**: Significant harm (customer data, financials).
- **Restricted**: Severe harm (PII, PHI, credentials).

### Output Format
| Data Field | Classification | Rationale | Regulations |
|------------|----------------|-----------|-------------|
| ... | ... | ... | ... |

### Additional Analysis
- Encryption requirements
- Access control recommendations
- Retention considerations

## Variables

- `[data_list]`: List of fields or data types to classify.

## Example

**Input**:
Data List: User ID, Email, Password Hash, Date of Birth, Credit Card Last 4, Public Profile URL

**Response**:
| Data Field | Classification | Rationale | Regulations |
|------------|----------------|-----------|-------------|
| User ID | Internal | System identifier, no PII | None |
| Email | Confidential | Personal identifier | GDPR, CCPA |
| Password Hash | Restricted | Authentication credential | SOC 2 |
| Date of Birth | Confidential | PII, age discrimination risk | GDPR |
| Credit Card Last 4 | Confidential | Partial payment data | PCI-DSS |
| Public Profile URL | Public | Intentionally shared | None |

### Recommendations
- Encrypt at rest: Password Hash, Email, DOB
- Access control: Restrict Credit Card data to finance team
