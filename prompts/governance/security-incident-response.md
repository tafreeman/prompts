---

title: "Security: Incident Response Framework"
category: "governance-compliance"
tags: ["security", "incident-response", "cybersecurity", "SOC", "IR", "threat", "containment"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["restricted-access", "audit-required", "CISO-approval-required", "sensitive"]
data_classification: "Restricted"
risk_level: "Critical"
regulatory_scope: ["SOC2", "ISO27001", "NIST-CSF", "GDPR-breach-notification"]
approval_required: "CISO or Security Director"
retention_period: "7 years (incident records)"
platform: "Claude Sonnet 4.5"
---

# Security: Incident Response Framework

## Description

A structured incident response framework for Security Operations Center (SOC) and Incident Response (IR) teams. Guides rapid assessment, containment, and recovery from security incidents. Follows NIST Cybersecurity Framework and includes breach notification requirements for GDPR/CCPA compliance.

## Use Cases

- Active security incident triage and response
- Data breach assessment and notification
- Ransomware incident handling
- Insider threat investigation
- DDoS attack mitigation
- Compromised credentials response
- Post-incident analysis and documentation

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
```

## Variables

- `[INCIDENT_DESCRIPTION]`: Nature of the security event
- `[SYMPTOMS_OR_ALERTS]`: Initial detection method and indicators
- `[AFFECTED_SYSTEMS]`: Systems, networks, or data involved
- `[CURRENT_STATUS]`: Is incident ongoing, contained, or resolved
- `[TIMESTAMP]`: When incident was discovered

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

**Output:**

```text
**INCIDENT SUMMARY**
- ID: INC-2024-11-17-001
- Type: Data Breach + Unauthorized Access + Data Exfiltration
- Severity: **CRITICAL**
- Status: **ONGOING - REQUIRES IMMEDIATE ACTION**
- GDPR Breach?: **YES** - 72-hour countdown started at 03:15 UTC

---

## Phase 1: DETECTION & ANALYSIS

**1.1 Incident Classification**
- **Type**: Data Breach + Compromised Credentials
- **Severity**: **CRITICAL**
  - Reason: Ongoing data exfiltration, privileged account compromised, 500K PII records at risk
- **Confidence**: **CONFIRMED** (active exfiltration detected)

**1.2 Scope Assessment**
- **Systems Affected**: 
  - Production database server (db-prod-01)
  - Privileged sysadmin account compromised
  - Customer database with PII
- **Data Potentially Compromised**:
  - Customer PII: Names, emails, addresses, phone numbers
  - Estimated records: 500,000
  - Data exported: 15GB to Mega.nz
- **User Accounts**: sysadmin@company.com (privileged)
- **Attack Source**: IP 203.0.113.45 (Russia)
- **Timeline**: 
  - 2:30 UTC: Failed SSH attempts begin
  - 2:35 UTC: Successful login
  - 2:47 UTC: Unusual database queries start
  - 2:50-3:10 UTC: 15GB data exfiltration
  - 3:15 UTC: Detected by SIEM

**1.3 Impact Analysis**
- **Business Impact**: 
  - **Operations**: Customer trust damage, potential service disruption
  - **Revenue**: Possible customer churn, sales impact
  - **Reputation**: Public breach disclosure required, media attention likely
  - **Legal**: GDPR fines (up to €20M or 4% revenue), class action risk
- **Data Impact**: 
  - Type: PII (personally identifiable information)
  - Volume: 500,000 records
  - Sensitivity: Medium-High (no financial/health data, but contact info + addresses)
  - Exfiltrated: 15GB confirmed transferred
- **User Impact**: 500,000 customers
- **Financial Impact** (Estimated):
  - Incident response: $50K-100K
  - Forensics: $75K-150K
  - Legal: $100K-500K
  - GDPR fine: €1M-10M potential
  - Credit monitoring: $15-20/user × 500K = $7.5M-10M
  - **Total estimate**: $8M-$21M+

**1.4 Breach Notification Determination**
- **Is personal data involved?**: **YES** - Names, emails, addresses, phone numbers (PII under GDPR Article 4)
- **Volume**: 500,000 records
- **Likelihood of harm**: **MEDIUM-HIGH**
  - Data can be used for phishing, identity theft, social engineering
  - No financial/health data reduces immediate harm
  - But phone+address combination is high risk
- **72-hour GDPR notification countdown**: **YES - STARTED at 03:15 UTC**
  - Deadline: 2024-11-19 03:15 UTC (71.5 hours remaining)
  - Must notify supervisory authority (Data Protection Authority)
- **Data subject notification**: **LIKELY REQUIRED** under GDPR Article 34 (high risk to rights and freedoms)

---

## Phase 2: CONTAINMENT

**⚠️ IMMEDIATE ACTIONS REQUIRED (NEXT 15 MINUTES)**

**2.1 Immediate Actions (DO NOW)**
- [ ] **URGENT**: Disable account sysadmin@company.com immediately
- [ ] **URGENT**: Block IP 203.0.113.45 at perimeter firewall + cloud WAF
- [ ] **URGENT**: Isolate db-prod-01 from internet (keep internal access for investigation)
- [ ] **URGENT**: Terminate active SSH sessions from 203.0.113.45
- [ ] **URGENT**: Block Mega.nz at proxy/firewall (stop ongoing exfiltration)
- [ ] **URGENT**: Snapshot db-prod-01 for forensics (DO NOT shut down yet)
- [ ] **URGENT**: Enable full packet capture on db-prod-01 network
- [ ] **NOW**: Alert CISO, CTO, Legal, CEO (via emergency contact list)
- [ ] **NOW**: Contact cyber insurance provider
- [ ] **NOW**: Engage incident response firm if no in-house capability

**Expected time to containment**: 5-10 minutes

**2.2 Short-Term Containment (Next 1-4 Hours)**
- [ ] Forensic analysis of sysadmin account compromise (how did attacker get credentials?)
- [ ] Review all privileged account activity in past 30 days
- [ ] Force password reset for ALL privileged accounts
- [ ] Enable MFA on all privileged accounts (if not already)
- [ ] Review firewall logs for other suspicious IPs from same subnet
- [ ] Check for persistence mechanisms (backdoors, additional accounts, SSH keys)
- [ ] Scan db-prod-01 for malware/rootkits
- [ ] Review database audit logs for full extent of data accessed

**2.3 Long-Term Containment (Next 24-72 Hours)**
- [ ] Implement IP whitelist for SSH access (restrict to corporate VPN only)
- [ ] Deploy CASB or DLP to detect future large data transfers
- [ ] Segment database servers into isolated network zone
- [ ] Implement database activity monitoring (DAM) solution
- [ ] Rotate all database credentials
- [ ] Review and harden SSH configuration (disable password auth, key-only)

---

## Phase 3: ERADICATION

**3.1 Root Cause Analysis** (Preliminary - Full forensics required)
- **Attack Vector**: Brute force SSH attack on privileged account
- **Vulnerability Exploited**: 
  - Weak password or password reuse (needs forensic confirmation)
  - No MFA on privileged account
  - No IP whitelist on SSH
  - SSH exposed to internet
- **Initial Access**: Successful SSH login after brute force
- **Persistence**: Unknown - forensic analysis needed (check for SSH keys, cron jobs, user accounts)

**3.2 Threat Removal**
- [x] Disable compromised account (completed in Phase 2)
- [ ] Remove any backdoors found in forensic analysis
- [ ] Delete unauthorized SSH keys
- [ ] Remove any additional accounts created by attacker
- [ ] Reset credentials for all privileged accounts
- [ ] Rebuild db-prod-01 from clean backup if rootkit/malware found

**3.3 Vulnerability Remediation**
- [ ] **Immediate**: Implement MFA for all privileged accounts
- [ ] **Immediate**: IP whitelist on SSH (corporate VPN only)
- [ ] **Week 1**: Deploy PAM (Privileged Access Management) solution
- [ ] **Week 1**: Implement password policy (minimum 16 characters, complexity, rotation)
- [ ] **Week 2**: Deploy database activity monitoring (DAM)
- [ ] **Week 2**: Implement DLP for large data transfers
- [ ] **Month 1**: Security awareness training (phishing, credential protection)

---

## Phase 4: RECOVERY

**4.1 System Restoration**
- **db-prod-01**: 
  - If no malware: Can remain in production with enhanced monitoring
  - If malware found: Must rebuild from clean backup, restore data, validate integrity
- **Recovery Priority**: High (production customer database)
- **Data Restoration**: Not needed unless data corrupted (backup available)
- **Validation Testing**: 
  - Verify no unauthorized accounts
  - Confirm all backdoors removed
  - Test database integrity
  - Validate access controls working

**4.2 Monitoring Plan** (Enhanced for 90 days)
- **Database Activity**:
  - Alert on any query returning >1,000 records
  - Alert on any SSH login from non-whitelisted IP
  - Alert on any outbound transfer >1GB
- **Indicators of Compromise (IoCs) to Watch**:
  - IP: 203.0.113.45 and entire /24 subnet
  - Mega.nz domain and subdomains
  - sysadmin@ account activity (should be disabled)
  - New privileged accounts created
  - SSH key additions
- **Alerting Rules to Add**:
  - Failed SSH login attempts >5 in 10 minutes
  - Privileged account login outside business hours
  - Database query duration >30 seconds (potential exfiltration)

**4.3 Return to Normal Operations**
- **Criteria for "All Clear"**:
  - No suspicious activity for 30 days
  - All vulnerabilities remediated
  - Forensic analysis complete and no additional compromise found
  - Enhanced monitoring showing normal patterns
- **User Communication**: 
  - Internal: Security incident update, new MFA requirements
  - External: Breach notification to affected customers (per GDPR/CCPA)
- **Service Restoration**: Already in production (containment didn't require downtime)

---

## Phase 5: POST-INCIDENT ACTIVITY

**5.1 Lessons Learned** (Preliminary - Full review after incident closed)
- **What Worked**:
  - SIEM detected unusual activity within 30 minutes
  - Incident response framework provided clear action plan
- **What Needs Improvement**:
  - Privileged account had no MFA (critical gap)
  - SSH exposed to internet (should be VPN-only)
  - No database activity monitoring for exfiltration detection
  - No DLP to prevent large data transfers
- **Detection Gaps**:
  - Brute force attack not detected in real-time
  - Large data transfer not blocked by DLP (no DLP deployed)
- **Response Gaps**:
  - 30-minute detection-to-containment time (good, but could be faster with automation)
- **Prevention Opportunities**:
  - Deploy MFA on all accounts (not just privileged)
  - Implement PAM with just-in-time access
  - Deploy DLP and CASB for data exfiltration prevention
  - Regular security awareness training

**5.2 Incident Report** (Draft - Complete within 72 hours)
- **Timeline**: [See timeline above]
- **Actions Taken**: [See containment/eradication phases]
- **Data Impact**: 500,000 customer records (names, emails, addresses, phones)
- **Costs** (Estimated): $8M-$21M
- **Recommendations**:
  1. Immediate MFA deployment
  2. SSH IP whitelisting
  3. PAM solution implementation
  4. DLP deployment
  5. Security training program

**5.3 Regulatory Notifications** ⚠️ **REQUIRED**

**GDPR Breach Notification** (REQUIRED - 72 hours):
- **To**: Relevant Data Protection Authority (DPA)
  - If EU: National DPA (e.g., ICO in UK, CNIL in France, BfDI in Germany)
  - If customers in multiple EU countries: Lead Supervisory Authority
- **Deadline**: 2024-11-19 03:15 UTC (71.5 hours remaining)
- **Content Required** (GDPR Article 33):
  - Nature of breach (unauthorized access, data exfiltration)
  - Categories and approximate number of data subjects (500,000)
  - Categories and approximate number of records (500,000 PII records)
  - Contact point (DPO or privacy officer)
  - Likely consequences (phishing risk, identity theft risk)
  - Measures taken and proposed (containment actions, MFA, monitoring)
- **Method**: Online portal or secure email to DPA

**Data Subject Notification** (LIKELY REQUIRED - Article 34):
- **Trigger**: High risk to rights and freedoms
- **Assessment**: Medium-High risk (PII can enable phishing, identity theft)
- **Decision**: **YES - Notify affected individuals**
- **Deadline**: Without undue delay (typically 30 days, but ASAP is better)
- **Content Required**:
  - Nature of breach
  - Contact point for questions
  - Likely consequences
  - Measures taken
  - Recommendations for data subjects (watch for phishing, fraud alerts)
- **Method**: Email to affected customers + website notice + press release

**U.S. State Breach Laws** (If Applicable):
- **Trigger**: If any affected customers reside in U.S. states with breach laws
- **States**: All 50 states + DC have breach notification laws (requirements vary)
- **California** (if applicable):
  - CCPA: Notify California AG if >500 CA residents affected
  - Cal. Civ. Code § 1798.82: Notify affected CA residents
- **Other States**: Check requirements (typically notification required for state residents)

**Industry-Specific** (If Applicable):
- PCI-DSS: If payment card data involved (not in this case)
- HIPAA: If health data involved (not in this case)

---

## COMMUNICATION PLAN

**Internal Notifications** (SEND NOW - within 1 hour):

✅ **CISO / Security Director**
- Subject: CRITICAL Security Incident - Data Breach - Action Required
- Content: [Incident summary, immediate actions, GDPR notification requirement]
- Method: Phone call + email + Slack emergency channel

✅ **CTO / VP Engineering**
- Subject: CRITICAL Security Incident - Database Compromise
- Content: [Technical details, containment actions, system status]
- Method: Phone call + email

✅ **Legal / General Counsel**
- Subject: URGENT - Data Breach - GDPR Notification Required in 72 Hours
- Content: [Data impact, regulatory obligations, potential fines]
- Method: Phone call + secure email

✅ **CEO / Executive Team**
- Subject: CRITICAL - Security Breach - 500K Customer Records
- Content: [Executive summary, business impact, next steps]
- Method: Phone call + executive briefing doc

✅ **Communications / PR**
- Subject: URGENT - Data Breach - Customer Communication Required
- Content: [Public disclosure requirement, customer notification, press release prep]
- Method: Phone call + email

**External Notifications** (As Required):

⚠️ **Law Enforcement** (FBI Cyber Division):
- **Required?**: Recommended (foreign attribution, significant financial impact)
- **When**: Within 24 hours
- **Method**: Contact local FBI field office or IC3.gov
- **Content**: Incident summary, Russian IP, data exfiltration

⚠️ **Regulatory Authorities**:
- **GDPR DPA**: REQUIRED within 72 hours (deadline: 2024-11-19 03:15 UTC)
- **State AGs**: If applicable (California AG if >500 CA residents)

⚠️ **Cyber Insurance Provider**:
- **Required**: YES (within 24-48 hours per policy terms)
- **Content**: Incident notice, estimated costs, coverage questions

⚠️ **Affected Customers** (500,000):
- **Required**: YES under GDPR Article 34
- **Timeline**: ASAP, typically within 30 days
- **Method**: Email + website notice + press release
- **Sample**: "Important Security Notice: We are writing to inform you of a data security incident that may have affected your personal information..."

⚠️ **Public Disclosure**:
- **Required**: YES (breach affects 500K+ individuals)
- **Timeline**: After customer notification sent
- **Method**: Press release, website notice, SEC filing (if public company)

---

## ESCALATION STATUS: 🚨 **CRITICAL - IMMEDIATE CISO ESCALATION**

**Escalation Triggers Met**:
- ✅ Data breach with PII (500,000 records)
- ✅ Active data exfiltration (15GB confirmed)
- ✅ Privileged account compromise
- ✅ GDPR breach notification required (72-hour deadline)
- ✅ Potential media attention (large breach)

**Recommended Immediate Escalations**:
1. **CISO**: Immediate phone call (do not wait for email)
2. **Legal**: Immediate phone call (GDPR deadline)
3. **CEO**: Immediate briefing (board notification likely needed)
4. **External IR Firm**: Engage if insufficient internal capacity
5. **Law Enforcement**: FBI notification within 24 hours

---

## NEXT STEPS (Priority Order)

**IMMEDIATE (Next 15 minutes)**:
- [ ] Execute containment actions (disable account, block IP, isolate system)
- [ ] Alert CISO, Legal, CEO
- [ ] Contact cyber insurance

**URGENT (Next 1-4 hours)**:
- [ ] Forensic snapshot and analysis begin
- [ ] Implement MFA on all privileged accounts
- [ ] Draft GDPR breach notification to DPA
- [ ] Draft customer notification email

**CRITICAL (Next 24 hours)**:
- [ ] Submit GDPR breach notification to DPA
- [ ] Engage incident response firm for forensics
- [ ] Contact FBI Cyber Division
- [ ] Prepare executive briefing for board

**IMPORTANT (Next 72 hours)**:
- [ ] Complete forensic analysis
- [ ] Send customer breach notification (per GDPR Article 34)
- [ ] Deploy DLP and enhanced monitoring
- [ ] Begin remediation of root cause vulnerabilities

**FOLLOW-UP (Next 30 days)**:
- [ ] Complete incident report
- [ ] Lessons learned review
- [ ] Implement PAM solution
- [ ] Security awareness training rollout

---

**⚠️ DISCLAIMER**: This is an AI-assisted incident response tool. All actions must be validated by qualified security professionals. For active incidents, immediately engage your incident response team, CISO, and legal counsel. Time-sensitive regulatory deadlines (GDPR 72 hours) require immediate legal review.
```

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
```

## Related Prompts

- [Security: Threat Modeling](security-threat-modeling.md) - Proactive threat assessment
- [Security: Vulnerability Assessment](security-vulnerability-assessment.md) - Security review
- [Compliance: Risk Assessment](compliance-risk-assessment.md) - Risk evaluation

## Changelog

### Version 1.0 (2025-11-17)

- Initial release
- NIST SP 800-61 framework implementation
- GDPR breach notification guidance
- Comprehensive containment procedures
- Regulatory compliance checklist
