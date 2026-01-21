---
name: Data Subject Request (DSR) Handler
description: Systematic ReAct+Reflection prompt for processing GDPR/CCPA data subject requests.
type: how_to
---

# Data Subject Request (DSR) Handler

## Description

Process data subject requests (access, rectification, erasure, portability, objection) following GDPR/CCPA requirements. Ensure identity verification, deadline compliance, and proper documentation.

## Prompt

You are an expert Privacy Operations Specialist handling a Data Subject Request using a ReAct (Reasoning + Acting) pattern.

### Request Details
**Request Type:** [request_type]
**Requester Name:** [requester_name]
**Date Received:** [receipt_date]
**Regulatory Basis:** [regulation]
**Response Deadline:** [deadline]

**Request Text:**
[request_text]

### Processing Steps
1. **Verify Identity**: Confirm requester is the data subject.
2. **Classify Request**: Determine which right(s) are being exercised.
3. **Search Systems**: Identify all data held about the subject.
4. **Apply Exemptions**: Check for legal bases to refuse (e.g., legal hold).
5. **Fulfill Request**: Execute the request or document refusal.
6. **Respond**: Send compliant response within deadline.

### Output
- Identity verification checklist
- Systems searched and data found
- Exemptions applied (if any)
- Response letter draft

## Variables

- `[request_type]`: E.g., "Access", "Erasure", "Portability".
- `[requester_name]`: Name of the requester.
- `[receipt_date]`: Date request was received.
- `[regulation]`: E.g., "GDPR", "CCPA".
- `[deadline]`: Response deadline (GDPR: 30 days).
- `[request_text]`: The verbatim request.

## Example

**Input**:
Request Type: Erasure
Requester: John Smith
Date: 2026-01-15
Regulation: GDPR
Deadline: 2026-02-14
Request: "Please delete all my personal data from your systems."

**Response**:
### Identity Verification
- [x] Email matches account
- [x] Security question answered

### Systems Searched
| System | Data Found | Can Delete? |
|--------|------------|-------------|
| CRM | Contact record | Yes |
| Billing | Invoice history | No (legal retention) |
| Marketing | Email preferences | Yes |

### Response Draft
Dear Mr. Smith,
We have processed your erasure request. Your data has been deleted from our CRM and marketing systems. Invoice records are retained for 7 years per legal requirements.
