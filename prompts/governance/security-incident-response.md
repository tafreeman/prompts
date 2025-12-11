---
title: "Security: Incident Response Framework"
shortTitle: "Security: Incident Respo..."
intro: "A structured incident response framework for Security Operations Center (SOC) and Incident Response (IR) teams. Guides rapid assessment, containment, and recovery from security incidents. Follows N..."
type: "tutorial"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "governance-compliance"
  - "incident-response"
  - "cybersecurity"
  - "security"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
governance_tags:
  - "restricted-access"
  - "audit-required"
  - "CISO-approval-required"
  - "sensitive"
dataClassification: "internal"
reviewStatus: "draft"
data_classification: "Restricted"
risk_level: "Critical"
regulatory_scope:
  - "SOC2"
  - "ISO27001"
  - "NIST-CSF"
  - "GDPR-breach-notification"
approval_required: "CISO or Security Director"
retention_period: "7 years (incident records)"
effectivenessScore: 4.4
---
# Security: Incident Response Framework

---

## Description

A structured incident response framework for Security Operations Center (SOC) and Incident Response (IR) teams. Guides rapid assessment, containment, and recovery from security incidents. Follows NIST Cybersecurity Framework and includes breach notification requirements for GDPR/CCPA compliance.

---

## Use Cases

- Active security incident triage and response
- Data breach assessment and notification
- Ransomware incident handling
- Insider threat investigation
- DDoS attack mitigation
- Compromised credentials response
- Post-incident analysis and documentation

---

## Prompt

```text
You are a security incident response assistant following NIST IR framework (NIST SP 800-61).

**Incident Alert**: [INCIDENT_DESCRIPTION]

**Initial Indicators**: [SYMPTOMS_OR_ALERTS]

**Systems Affected**: [AFFECTED_SYSTEMS]

**Current Status**: [ONGOING_OR_CONTAINED]

**Time Discovered**: [TIMESTAMP]

**Instructions**:

Follow the NIST Incident Response lifecycle:

## Phase 1: DETECTION & ANALYSIS

**1.1 Incident Classification**
- **Type**: [Malware, Phishing, Data Breach, DDoS, Insider Threat, Compromised Credentials, Ransomware, Other]
- **Severity**: Critical / High / Medium / Low (use criteria below)
- **Confidence**: Confirmed / Likely / Suspected

**Severity Criteria**:
- **Critical**: Data breach with PII/PHI, ransomware encryption, total system compromise, ongoing active attack
- **High**: Successful intrusion, malware infection, privilege escalation, significant data at risk
- **Medium**: Attempted intrusion, suspicious activity, potential malware, limited scope
- **Low**: Policy violation, failed attack attempt, no data impact

**1.2 Scope Assessment**
- Systems/networks affected
- Data potentially compromised
- User accounts involved
- Geographic scope
- Timeline of compromise

**1.3 Impact Analysis**
- **Business Impact**: Revenue, Operations, Reputation, Legal
- **Data Impact**: Type and volume of data at risk (PII, Financial, PHI, IP, etc.)
- **User Impact**: Number of users/customers affected
- **Financial Impact**: Estimated costs (response, recovery, fines, lawsuits)

**1.4 Breach Notification Determination**
- Is personal data involved? (triggers GDPR Art. 33, CCPA, etc.)
- Volume of records affected
- Likelihood of harm to data subjects
- 72-hour GDPR notification countdown started? [YES/NO]

## Phase 2: CONTAINMENT

**2.1 Immediate Actions (First 15 Minutes)**
List actions to stop incident spread:
- [ ] Isolate affected systems from network
- [ ] Disable compromised accounts
- [ ] Block malicious IPs/domains at firewall/proxy
- [ ] Snapshot systems for forensics
- [ ] Alert key stakeholders (CISO, Legal, Executive)

**2.2 Short-Term Containment**
- Network segmentation actions
- System isolation decisions
- Access control changes
- Backup verification

**2.3 Long-Term Containment**
- Persistent threat removal
- System rebuild requirements
- Monitoring enhancements

## Phase 3: ERADICATION

**3.1 Root Cause Analysis**
- Attack vector identified
- Vulnerability exploited
- Initial access method
- Persistence mechanisms

**3.2 Threat Removal**
- Malware removal steps
- Backdoor elimination
- Credential reset requirements
- Patch deployment

**3.3 Vulnerability Remediation**
- Immediate patches/fixes
- Configuration changes
- Security control improvements

## Phase 4: RECOVERY

**4.1 System Restoration**
- Systems safe to restore to production
- Recovery priority order
- Data restoration from clean backups
- Validation testing required

**4.2 Monitoring Plan**
- Enhanced monitoring for 30-90 days
- Indicators of Compromise (IoCs) to watch
- Alerting rules to add

**4.3 Return to Normal Operations**
- Criteria for "all clear"
- User communication plan
- Service restoration timeline

## Phase 5: POST-INCIDENT ACTIVITY

**5.1 Lessons Learned**
- What worked well
- What needs improvement
- Detection gaps
- Response gaps
- Prevention opportunities

**5.2 Incident Report** (Required within 72 hours)
- Timeline of events
- Actions taken
- Data impact assessment
- Costs incurred
- Recommendations

**5.3 Regulatory Notifications** (If Applicable)
- GDPR breach notification (72 hours to DPA, 30 days to data subjects if high risk)
- CCPA breach notification (California AG + affected residents)
- State breach laws (varies by state)
- Industry-specific (PCI-DSS, HIPAA, etc.)

## Communication Plan

**Internal Notifications** (within 1 hour):
- CISO / Security Director
- CTO / VP Engineering
- Legal / General Counsel
- CEO / Executive Team
- Communications / PR
- HR (if insider threat)

**External Notifications** (as required):
- Law enforcement (FBI, local police for >$100K or national security)
- Regulatory authorities (DPA, FTC, etc.)
- Cyber insurance provider
- Affected customers/partners
- Public disclosure (if required)

**Communication Templates**:
- Internal: "Security Incident - [Severity] - Action Required"
- Customer: "Important Security Notice Regarding Your Account"
- Regulator: "Data Breach Notification - [Company] - [Date]"

## Escalation Triggers

**Immediate CISO Escalation**:
- Data breach with PII/PHI
- Ransomware with encryption
- Executive/VIP account compromise
- Active data exfiltration detected
- Media attention or public disclosure
- Suspected nation-state actor

**Law Enforcement Notification**:
- Financial loss >$100K
- Nation-state attribution
- Child safety issues
- Terrorism-related
- Ongoing criminal activity

## Output Format

Provide structured incident report:

**INCIDENT SUMMARY**
- ID: [INC-YYYY-MM-DD-XXX]
- Type: [Incident Type]
- Severity: [Critical/High/Medium/Low]
- Status: [New/In Progress/Contained/Resolved]
- GDPR Breach?: [Yes/No]

**TIMELINE**
- T+0: [Discovery time and method]
- T+15min: [Initial containment actions]
- T+1hr: [Stakeholder notifications]
- T+24hr: [Status update]
- T+72hr: [Resolution or ongoing]

**IMPACT**
- Systems affected: [List]
- Data compromised: [Type, volume, sensitivity]
- Users affected: [Count, type]
- Est. cost: $[Amount]

**ACTIONS TAKEN**
- Containment: [Summary]
- Eradication: [Summary]
- Recovery: [Summary]

**NEXT STEPS**
- [ ] Action item 1
- [ ] Action item 2

**REGULATORY OBLIGATIONS**
- GDPR notification due: [Timestamp if applicable]
- Other notifications: [List]
```text

---

## Variables

- `[INCIDENT_DESCRIPTION]`: Nature of the security event
- `[SYMPTOMS_OR_ALERTS]`: Initial detection method and indicators
- `[AFFECTED_SYSTEMS]`: Systems, networks, or data involved
- `[CURRENT_STATUS]`: Is incident ongoing, contained, or resolved
- `[TIMESTAMP]`: When incident was discovered

---

## Example Usage

**Input:**

```text
You are a security incident response assistant following NIST IR framework.

**Incident Alert**: Suspicious login activity and potential data exfiltration detected

**Initial Indicators**:
- SIEM alert: Multiple failed SSH login attempts followed by successful login from IP 203.0.113.45 (Russia)
- Unusual database query activity at 2:47 AM UTC
- Outbound transfer of 15GB to external cloud storage (Mega.nz)
- Compromised account: sysadmin@company.com (privileged account)

**Systems Affected**:
- Production database server (db-prod-01.company.com)
- Customer data database (contains PII: names, emails, addresses, phone numbers)
- Estimate: 500,000 customer records potentially accessed

**Current Status**: Ongoing - Account still active, need immediate containment

**Time Discovered**: 2024-11-17 03:15 UTC (28 minutes ago)

**Instructions**: [Follow framework above]
```

**Expected Output:**

```markdown
# INCIDENT REPORT

## INCIDENT SUMMARY
- **ID**: INC-2024-11-17-001
- **Type**: Data Breach / Unauthorized Access
- **Severity**: CRITICAL (P1)
- **Status**: In Progress - Active Containment
- **GDPR Breach**: ✅ YES - Personal data (PII) of EU residents potentially compromised

## TIMELINE
| Time | Event | Action Taken |
|------|-------|--------------|
| T+0 (03:15 UTC) | Discovery via SIEM alert | SOC analyst escalated to IR team |
| T+5min | Account sysadmin@company.com confirmed compromised | - |
| T+10min | External IP 203.0.113.45 traced to Russian ASN | - |
| T+15min | **CONTAINMENT INITIATED** | See actions below |
| T+28min | Current status | Active response, containment in progress |

## IMMEDIATE CONTAINMENT ACTIONS (T+0 to T+1hr)

### 1. Account Containment
- [ ] **IMMEDIATE**: Disable sysadmin@company.com in Active Directory
- [ ] Force password reset for all privileged accounts with db-prod-01 access
- [ ] Revoke all active sessions for compromised account
- [ ] Enable MFA enforcement for all admin accounts (if not already)

### 2. Network Containment
- [ ] **IMMEDIATE**: Block IP 203.0.113.45 at firewall (inbound and outbound)
- [ ] Block outbound connections to Mega.nz (*.mega.nz, *.mega.co.nz)
- [ ] Isolate db-prod-01.company.com from network (keep powered on for forensics)
- [ ] Enable enhanced logging on all database servers

### 3. Evidence Preservation
- [ ] Snapshot db-prod-01 VM/disk immediately (before further changes)
- [ ] Export SIEM logs for past 72 hours (SSH, DB queries, network flows)
- [ ] Preserve Mega.nz transfer logs if accessible
- [ ] Image memory dump of db-prod-01 (live forensics)

## IMPACT ASSESSMENT

| Category | Assessment |
|----------|------------|
| **Systems Affected** | db-prod-01.company.com (production database server) |
| **Data Type** | PII: names, emails, addresses, phone numbers |
| **Records Potentially Accessed** | ~500,000 customer records |
| **Data Classification** | Confidential / Restricted (PII) |
| **Est. Financial Impact** | $5M–$15M (regulatory fines, remediation, legal, reputation) |
| **Exfiltration Confirmed** | 15GB transferred to Mega.nz — likely database dump |

## REGULATORY OBLIGATIONS

### GDPR (EU General Data Protection Regulation)
- **Notification Required**: ✅ YES — Personal data breach affecting EU residents
- **Deadline**: 72 hours from awareness = **2024-11-19 03:15 UTC**
- **Notify**: Lead Supervisory Authority (Data Protection Authority)
- **Data Subject Notification**: Required if high risk to individuals (likely yes)

### Additional Notifications
| Authority/Stakeholder | Deadline | Status |
|-----------------------|----------|--------|
| GDPR DPA | 2024-11-19 03:15 UTC | ⏳ Pending |
| Cyber Insurance Provider | ASAP | ⏳ Pending |
| Legal Counsel | Immediate | ⏳ Pending |
| Executive Team (CISO → CEO) | T+1hr | ⏳ Pending |
| Affected Customers | TBD (after impact confirmed) | ⏳ Pending |

## ESCALATION TRIGGERS MET
- ✅ Data breach with PII — CISO escalation required
- ✅ Active data exfiltration detected — Immediate containment
- ✅ Privileged account compromise — Full access review
- ⚠️ Potential nation-state actor (Russian IP) — Consider law enforcement

## NEXT STEPS (Next 24 Hours)
- [ ] Complete containment actions above
- [ ] Engage external forensics firm (if needed)
- [ ] Prepare GDPR breach notification draft
- [ ] Conduct full access review for all privileged accounts
- [ ] Begin eradication: determine root cause (phishing? credential stuffing? vulnerability?)
- [ ] Prepare customer communication (pending legal review)
- [ ] Schedule post-incident review (within 30 days)

## INCIDENT COMMANDER
- **Assigned To**: [IR Lead Name]
- **Backup**: [Backup Name]
- **War Room**: [Slack channel / Zoom link]
- **Next Update**: T+2hr (05:15 UTC)
```

---

## Tips

- **Act fast**: Minutes matter in containment - automate where possible
- **Document everything**: Timeline, actions, decisions for legal/regulatory needs
- **Assume breach until proven otherwise**: Treat all suspicious activity as confirmed compromise
- **Preserve evidence**: Snapshot systems before containment actions destroy forensic evidence
- **Know your notification obligations**: GDPR (72 hours), state laws (varies), industry regulations
- **Communicate clearly**: Use severity levels consistently, provide actionable next steps
- **Don't panic**: Follow the framework systematically

## Governance & Compliance

### Access Control

- **SOC/IR Teams Only**: Restricted to trained security personnel
- **CISO Approval Required**: For access grant
- **Background Check Required**: For IR team members
- **NDA Required**: All IR activities confidential

### Audit Requirements

- **Log all incidents**: Every alert, even false positives
- **Incident ID**: Unique identifier (INC-YYYY-MM-DD-XXX)
- **Retain for 7 years**: Legal/regulatory requirement
- **Chain of custody**: For forensic evidence
- **Post-incident review**: Mandatory within 30 days

### Regulatory Compliance

- **GDPR**: 72-hour breach notification to DPA, data subject notification if high risk
- **CCPA**: California AG + affected residents notification
- **SOC 2**: Incident response procedures documented and tested
- **ISO 27001**: Incident management process (Annex A.16)
- **NIST CSF**: Incident response lifecycle followed
- **PCI-DSS**: Incident response plan if payment data involved

---

## Output Schema (JSON)

```json
{
  "incident_id": "INC-2024-11-17-001",
  "severity": "critical|high|medium|low",
  "type": "data-breach|malware|ddos|...",
  "status": "new|in-progress|contained|resolved",
  "gdpr_breach": true,
  "timeline": [
    {"time": "T+0", "event": "Discovery"},
    {"time": "T+15min", "event": "Containment"}
  ],
  "impact": {
    "systems": ["..."],
    "data_type": "PII|Financial|PHI|IP",
    "records_affected": 500000,
    "estimated_cost": 10000000
  },
  "containment_actions": ["...", "..."],
  "eradication_actions": ["...", "..."],
  "recovery_plan": "...",
  "regulatory_notifications": [
    {
      "authority": "GDPR DPA",
      "deadline": "2024-11-19T03:15:00Z",
      "status": "pending"
    }
  ],
  "next_steps": ["...", "..."]
}
```text

---

## Related Prompts

<!-- Links removed - files don't exist yet -->
