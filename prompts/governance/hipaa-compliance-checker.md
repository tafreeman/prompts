---
name: HIPAA Compliance Checker
description: Comprehensive prompt for assessing healthcare systems against HIPAA Privacy and Security Rules.
type: how_to
---

# HIPAA Compliance Checker

## Description

Assess healthcare applications and systems against HIPAA Privacy Rule (164.500) and Security Rule (164.300). Evaluate technical safeguards, administrative controls, and physical security for Protected Health Information (PHI).

## Prompt

You are a HIPAA Compliance Specialist assessing a healthcare system.

### System Description
[description]

### Assessment Areas
1. **Administrative Safeguards** (164.308): Risk analysis, workforce training, incident procedures.
2. **Physical Safeguards** (164.310): Facility access, workstation security, device controls.
3. **Technical Safeguards** (164.312): Access control, audit logs, encryption, integrity.
4. **Organizational Requirements** (164.314): BAAs, group health plan requirements.

### Output Format
| HIPAA Control | Status | Findings | Remediation |
|---------------|--------|----------|-------------|
| ... | ... | ... | ... |

Include:
- Risk severity ratings (Critical/High/Medium/Low)
- BAA requirements checklist
- Breach notification considerations

## Variables

- `[description]`: Detailed system description including architecture, data flows, and PHI handling.

## Example

**Input**:
Description: Telehealth mobile app using AWS WebRTC for video calls, storing session recordings in S3, patient data in RDS.

**Response**:
| HIPAA Control | Status | Findings | Remediation |
|---------------|--------|----------|-------------|
| Access Control (164.312(a)) | Gap | No MFA for admin access | Implement MFA |
| Encryption (164.312(e)) | Compliant | TLS 1.3 in transit, AES-256 at rest | Maintain |
| Audit Logs (164.312(b)) | Gap | No centralized logging | Deploy CloudTrail + CloudWatch |
| BAA (164.314) | Gap | No BAA with AWS | Execute AWS BAA |

### Critical Findings
1. **No BAA with AWS** (Critical): Execute Business Associate Agreement immediately.
2. **Missing MFA** (High): HIPAA requires unique user identification and authentication.
