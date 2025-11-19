# Enterprise Security Incident Response Playbook

**Version**: 1.0  
**Last Updated**: 2025-11-17  
**Framework**: NIST SP 800-61 Rev 2  
**Target Audience**: Security Operations Centers (SOC), Incident Response Teams, IT Operations

---

## Overview

This playbook provides a structured approach to detecting, triaging, investigating, containing, remediating, and learning from security incidents using prompts from the repository. It combines NIST SP 800-61 framework with GDPR/regulatory compliance requirements.

### When to Use This Playbook

```
┌─────────────────────────────────────────────────────────────────┐
│ Activate This Playbook IF:                                      │
├─────────────────────────────────────────────────────────────────┤
│ ✓ Security alert triggered (SIEM, IDS/IPS, EDR)               │
│ ✓ Unusual system behavior reported                             │
│ ✓ Data breach suspected or confirmed                           │
│ ✓ Ransomware or malware detected                               │
│ ✓ Unauthorized access to systems/data                          │
│ ✓ Compliance violation detected (GDPR, SOC2, HIPAA)           │
│                                                                 │
│ ✗ For non-security issues, use:                               │
│   • Performance degradation → DevOps runbook                   │
│   • Application bugs → SDLC workflow                           │
└─────────────────────────────────────────────────────────────────┘
```

### Incident Severity Classification

| Severity | Definition | Response Time | Examples |
|----------|------------|---------------|----------|
| **Critical (P0)** | Data breach, ransomware, C-level compromise | Immediate (< 15 min) | Customer PII exposed, production database encrypted, CEO account compromised |
| **High (P1)** | Service disruption, privilege escalation | < 1 hour | Web server defaced, admin account compromised, DDoS attack |
| **Medium (P2)** | Attempted breach, suspicious activity | < 4 hours | Failed login attempts, malware quarantined, phishing email reported |
| **Low (P3)** | Policy violation, security hygiene | < 24 hours | Weak password detected, unpatched system, misconfigured firewall |

---

## Phase 1: Detection (0-15 Minutes)

### Objective
Identify and confirm potential security incident through monitoring, alerts, or reports

### Duration
**5-15 minutes** from initial alert to incident confirmation

### Prompts to Use

1. **[metrics-and-kpi-designer](../../prompts/analysis/metrics-and-kpi-designer.md)** - Review monitoring dashboards and alert thresholds
2. **[security-code-auditor](../../prompts/governance-compliance/security-code-auditor.md)** - Analyze suspicious code behavior or vulnerabilities
3. **[data-analysis-insights](../../prompts/analysis/data-analysis-insights.md)** - Correlate security events from multiple sources

### Detection Sources

**Automated Alerts** (SIEM, IDS/IPS, EDR):
- Failed authentication attempts (threshold: > 10 in 5 minutes)
- Unusual outbound traffic (data exfiltration indicators)
- Malware signature detected
- Privilege escalation attempts
- File integrity monitoring alerts (critical system files modified)

**Manual Reports**:
- Employee reports suspicious email or activity
- Customer reports unauthorized access to account
- Third-party security researcher reports vulnerability

**Threat Intelligence**:
- CVE published for software in use
- Industry peer reports attack campaign
- Dark web monitoring detects credentials

### Detection Workflow

```
Step 1: Alert Received
  ↓
Step 2: Initial Classification (Severity P0-P3)
  ↓
Step 3: Check for False Positive
  - Review historical data (same alert pattern before?)
  - Validate with context (planned maintenance? authorized activity?)
  ↓
Step 4: If CONFIRMED incident → Escalate to Phase 2 (Triage)
       If FALSE POSITIVE → Document and close
       If UNCERTAIN → Collect more data (1-2 additional checks)
```

### Example: Detecting Ransomware

**Alert**: EDR (Endpoint Detection & Response) detects suspicious file encryption activity on file server (FS-PROD-01)

**Use metrics-and-kpi-designer prompt**:
```
Prompt: "Analyze the following EDR alert for ransomware indicators. Data: Host FS-PROD-01, 
Process: powershell.exe, Activity: Rapid file modifications (500+ files in 2 minutes), 
File extension changes (.docx → .encrypted), Network: Outbound connection to IP 203.0.113.45.

Determine severity (P0-P3) and recommend immediate actions."

AI Response:
"CRITICAL SEVERITY (P0) - High confidence ransomware attack:

Indicators:
1. Mass file encryption (500+ files in 2 min = exfiltration or encryption)
2. Extension change to .encrypted (ransomware signature)
3. PowerShell execution (common ransomware delivery mechanism)
4. Outbound connection to unknown IP (potential C2 communication)

Immediate Actions:
1. ISOLATE FS-PROD-01 from network (disconnect immediately)
2. Preserve forensic evidence (take memory dump before shutdown)
3. Activate P0 incident response (page on-call CISO)
4. Check backups (verify last clean backup timestamp)
5. Hunt for lateral movement (scan other hosts for similar indicators)

Estimated Impact: HIGH (file server compromise affects 200+ users)
Regulatory: GDPR breach notification may be required (assess data affected)"
```

**Decision Point**: Confirmed ransomware (P0) → Escalate to Phase 2 immediately

### Detection Checklists

**For Security Alerts**:
- [ ] Alert source and timestamp recorded
- [ ] Affected system(s) identified (hostname, IP address)
- [ ] Alert severity classified (P0-P3)
- [ ] False positive check completed
- [ ] Initial context gathered (recent changes, maintenance windows)
- [ ] Incident ticket created (include alert details)

**For User Reports**:
- [ ] Reporter contact information captured
- [ ] Incident description documented (what, when, where)
- [ ] Screenshots or evidence collected
- [ ] Affected user accounts or systems identified
- [ ] Reporter notified of next steps

### Deliverables (Phase 1)

- **Incident Ticket**: Created in ticketing system (Jira, ServiceNow, PagerDuty)
  - Ticket ID
  - Severity classification
  - Detection source and timestamp
  - Brief description (1-2 sentences)
  - Assigned to: Incident Commander or on-call engineer
- **Initial Timeline**: Start of incident clock (critical for GDPR 72-hour notification)
- **Stakeholder Notification**: For P0/P1, page on-call CISO and security team

### Decision Point: Proceed to Phase 2?

**YES if**:
- ✓ Confirmed security incident (not false positive)
- ✓ Severity P0-P2 (requires formal response)
- ✓ Incident ticket created and assigned

**NO if** (close incident):
- ✗ Confirmed false positive (e.g., legitimate maintenance activity)
- ✗ Severity P3 with no actual compromise (e.g., weak password warning handled by auto-reset)

---

## Phase 2: Triage (15 Minutes - 1 Hour)

### Objective
Assess incident scope, impact, and urgency; activate appropriate response team and resources

### Duration
**15 minutes to 1 hour** depending on severity and complexity

### Prompts to Use

1. **[security-incident-response](../../prompts/governance-compliance/security-incident-response.md)** - Primary prompt for structured triage
2. **[crisis-management-coordinator](../../prompts/business/crisis-management-coordinator.md)** - Stakeholder communication and escalation
3. **[risk-management-analyst](../../prompts/business/risk-management-analyst.md)** - Assess business impact and regulatory exposure

### Triage Framework (STRIDE Threat Model)

**S** - Spoofing: Is identity compromised? (credentials, certificates, tokens)  
**T** - Tampering: Is data or code modified? (database, files, configurations)  
**R** - Repudiation: Can attacker deny actions? (logging gaps, audit trail)  
**I** - Information Disclosure: Is sensitive data exposed? (PII, PHI, financial data)  
**D** - Denial of Service: Is availability affected? (ransomware, DDoS)  
**E** - Elevation of Privilege: Did attacker gain higher access? (admin, root, system)

### Triage Workflow

```
Step 1: Assemble Incident Response Team
  - Incident Commander (IC): Coordinates response
  - Security Analyst: Technical investigation
  - System Admin: Access to affected systems
  - Legal/Compliance (P0/P1): For breach notification assessment
  - Communications (P0/P1): Stakeholder and customer messaging
  ↓
Step 2: Scope Assessment (5 Questions)
  1. What systems/data are affected? (identify assets)
  2. How many users/customers impacted? (calculate blast radius)
  3. What is the attack vector? (phishing, vulnerability, insider threat)
  4. Is attacker still active? (ongoing vs historical compromise)
  5. What regulations apply? (GDPR, HIPAA, SOC2, PCI-DSS)
  ↓
Step 3: Impact Analysis
  - Confidentiality: What data was exposed? (classify: Public, Internal, Confidential, Restricted)
  - Integrity: What was modified or destroyed? (data corruption, ransomware)
  - Availability: What services are down? (downtime cost, SLA breach)
  ↓
Step 4: Regulatory Assessment
  - Is this a reportable breach? (GDPR: personal data, HIPAA: PHI)
  - What is the notification timeline? (GDPR: 72 hours, state laws vary)
  - Who must be notified? (regulators, customers, media)
  ↓
Step 5: Response Strategy Selection (Choose ONE)
  A. CONTAIN & INVESTIGATE (most common)
     - Isolate affected systems, preserve evidence, deep-dive forensics
  B. IMMEDIATE ERADICATION (active threat)
     - Remove attacker access NOW, investigate after
  C. MONITOR & GATHER INTELLIGENCE (sophisticated APT)
     - Allow continued access under observation to understand tactics
  ↓
Step 6: Activate Response Plan
  - Assign roles and tasks
  - Set up war room (physical or virtual)
  - Establish communication channels (Slack, Teams, conference bridge)
```

### Example: Triaging Ransomware (Continued from Phase 1)

**Incident**: Ransomware detected on file server FS-PROD-01

**Use security-incident-response prompt**:
```
Prompt: "Triage this ransomware incident. Context: File server FS-PROD-01 compromised, 
500+ files encrypted, PowerShell execution detected, outbound connection to suspicious IP 
203.0.113.45. File server hosts:
- Employee documents (HR records, contracts, NDA agreements)
- Customer project files (designs, source code, specifications)
- Financial reports (Q4 2024 earnings, budgets)

Organization: 250 employees, healthcare sector (HIPAA regulated), EU operations (GDPR).

Provide: 1) Scope assessment, 2) Regulatory impact, 3) Response strategy recommendation"

AI Response:
"TRIAGE SUMMARY - Ransomware Incident (P0)

SCOPE ASSESSMENT:
1. Affected Systems: 
   - Primary: FS-PROD-01 (file server, 500+ files encrypted)
   - Potential lateral movement: Scan domain controller DC-01 and backup server BKP-01
2. Impacted Users: 200+ employees accessing file server daily
3. Attack Vector: Likely phishing email with malicious attachment (investigate recent emails)
4. Attacker Status: ACTIVE (outbound C2 connection detected 5 min ago)
5. Affected Data Classifications:
   - RESTRICTED: HR records (SSN, salary data) = HIPAA PHI + GDPR personal data
   - CONFIDENTIAL: Customer source code (IP theft risk)
   - INTERNAL: Financial reports (material non-public information)

IMPACT ANALYSIS:
- Confidentiality: CRITICAL - PHI and personal data exposed (HIPAA + GDPR breach)
- Integrity: HIGH - 500+ files encrypted (data loss, but backups may exist)
- Availability: MEDIUM - File server offline, 200 users affected (workaround: restore from backup)

REGULATORY IMPACT:
- HIPAA Breach: YES (PHI compromised → HHS OCR notification required within 60 days)
- GDPR Breach: YES (personal data compromised → supervisory authority notification within 72 hours)
- Notification Requirements:
  * Regulators: HHS OCR (US), Data Protection Authority (EU) - 72 hours
  * Affected individuals: Employees and customers whose data was compromised - 60 days
  * Media: If > 500 individuals affected (likely YES) - concurrent with individual notification
- Estimated Fine Risk: GDPR up to €20M or 4% annual revenue, HIPAA up to $1.5M

RESPONSE STRATEGY: **IMMEDIATE ERADICATION + CONTAINMENT**

Rationale:
- Active C2 connection = attacker can escalate (spread ransomware, exfiltrate more data)
- PHI/GDPR data exposed = regulatory clock started (need fast containment)
- Backup availability = can restore services quickly after eradication

IMMEDIATE ACTIONS (Next 15 Minutes):
1. ISOLATE: Disconnect FS-PROD-01 from network (already done in Phase 1)
2. KILL C2: Block IP 203.0.113.45 at firewall + DNS sinkhole
3. HUNT: Scan all domain-joined systems for same PowerShell IOCs
4. PRESERVE: Take forensic image of FS-PROD-01 (memory + disk)
5. ACTIVATE: Page CISO, Legal, Compliance, PR team (P0 war room)
6. NOTIFY: Brief CEO/CTO on breach scope and regulatory timeline

NEXT PHASE: Proceed to Phase 3 (Investigation) to:
- Identify ransomware variant (Locky? Ryuk? REvil?)
- Determine initial infection vector (phishing email analysis)
- Assess data exfiltration (was data stolen before encryption?)
- Check backup integrity (verify clean restore point exists)"
```

**Decision Point**: Confirmed P0 breach requiring IMMEDIATE ERADICATION → Proceed to Phase 3 (Investigation)

### Triage Checklists

**Incident Response Team Activation**:
- [ ] Incident Commander assigned and acknowledged
- [ ] Security Analyst(s) assigned (minimum 1, preferably 2-3 for P0)
- [ ] System Admin with access to affected systems on standby
- [ ] Legal/Compliance notified (for P0/P1)
- [ ] Communications/PR team notified (for customer-facing breaches)
- [ ] War room established (physical room or Zoom/Teams bridge)
- [ ] Communication channels set up (dedicated Slack channel or Teams channel)

**Scope Assessment**:
- [ ] Affected systems documented (hostnames, IP addresses, asset tags)
- [ ] Affected users/customers quantified (exact count or estimate)
- [ ] Attack vector hypothesis documented (will be validated in Phase 3)
- [ ] Attacker activity status confirmed (active vs historical)
- [ ] Data classification reviewed (Public, Internal, Confidential, Restricted)

**Regulatory Assessment** (for P0/P1 involving personal data):
- [ ] GDPR applicability checked (EU citizens' data affected?)
- [ ] HIPAA applicability checked (PHI affected?)
- [ ] PCI-DSS applicability checked (payment card data affected?)
- [ ] SOC2/ISO27001 incident reporting requirements reviewed
- [ ] 72-hour GDPR notification clock started (timestamp documented)
- [ ] Breach notification template prepared (draft, not sent yet)

**Response Strategy Selection**:
- [ ] Contain & Investigate (isolate, then analyze)
- [ ] Immediate Eradication (remove threat first, analyze later)
- [ ] Monitor & Gather Intelligence (track attacker under controlled conditions)
- [ ] Strategy rationale documented (why this approach chosen)

### Deliverables (Phase 2)

- **Triage Report** (1-2 pages):
  - Incident summary (what happened, when, where)
  - Scope and impact assessment (STRIDE analysis)
  - Affected data and regulatory implications
  - Response strategy and rationale
  - Immediate actions taken (isolation, blocking, preservation)
- **Incident Response Team Roster**:
  - Roles and contact information (phone, email, Slack handle)
  - Escalation tree (who to contact if IC unavailable)
- **War Room Details**:
  - Physical location or conference bridge URL
  - Slack/Teams channel link
  - Shared document repository (Google Drive, SharePoint)
- **Regulatory Notification Clock**:
  - GDPR 72-hour deadline timestamp
  - HIPAA 60-day deadline timestamp
  - Responsible party assigned (Legal/Compliance)

### Communication Templates

**P0 Incident - Executive Notification** (send within 30 min of triage):
```
Subject: P0 SECURITY INCIDENT - Ransomware on File Server [CONFIDENTIAL]

INCIDENT SUMMARY:
- What: Ransomware encryption detected on file server FS-PROD-01
- When: Detected at 14:35 UTC, attack likely started 14:30 UTC
- Impact: 500+ files encrypted, 200 users affected, PHI/GDPR data potentially exposed
- Status: System isolated, attacker C2 blocked, investigation in progress

IMMEDIATE ACTIONS TAKEN:
- File server disconnected from network (14:37 UTC)
- Attacker command-and-control IP blocked (14:40 UTC)
- Forensic evidence preserved (memory dump captured)
- Incident Response Team activated (IC: Jane Doe, CISO)

NEXT STEPS:
- Phase 3: Deep-dive investigation (ransomware variant ID, infection vector)
- Phase 4: Containment and eradication (remove malware, restore from backup)
- Legal/Compliance: Assess GDPR/HIPAA breach notification requirements (72-hour clock started)

ESTIMATED TIMELINE:
- Investigation: 2-4 hours
- Recovery: 4-6 hours (restore from backup)
- Full resolution: 8-12 hours

LEADERSHIP REQUIRED:
- CEO: Approve external PR statement (if customer notification required)
- CFO: Approve cyber insurance claim (estimated cost: $50k-$200k)
- CTO: Approve temporary service disruption for forensics

WAR ROOM: Conference Bridge +1-555-123-4567, Slack #incident-2025-11-17-ransomware

- Jane Doe, CISO (Incident Commander)
```

**P1/P2 Incident - IT Team Notification**:
```
Subject: P1 Security Incident - Investigating Suspicious Activity on Web Server

Team,

We're investigating a P1 security incident:
- Affected System: WEB-PROD-03 (customer portal)
- Issue: Unusual outbound traffic to unknown IP (possible data exfiltration)
- Impact: 5,000 customers use this portal (no confirmed breach yet)

Current Actions:
- Web server isolated for forensics
- Traffic logs being analyzed
- Backup portal activated (customers redirected to WEB-PROD-04)

No customer notification yet - awaiting investigation results.

Updates every 30 minutes in #incident-response Slack channel.

- Security Team
```

### Escalation Triggers (When to Escalate Severity)

**P2 → P1 Escalation**:
- Confirmed data access (not just attempt)
- More than 100 users affected
- Service disruption > 1 hour

**P1 → P0 Escalation**:
- Personal data (PII, PHI, financial) confirmed exposed
- Ransomware or destructive malware deployed
- C-level executive account compromised
- Customer-facing service down > 2 hours
- Media attention or social media discussion

---

## Phase 3: Investigation (1-4 Hours)

### Objective
Conduct deep forensic analysis to understand attack timeline, tactics, techniques, and procedures (TTPs); determine full scope of compromise

### Duration
**1-4 hours** for initial investigation (P0/P1)  
**Up to 8 hours** for complex Advanced Persistent Threats (APTs)

### Prompts to Use

1. **[security-incident-response](../../prompts/governance-compliance/security-incident-response.md)** - Forensic analysis framework
2. **[security-code-auditor](../../prompts/governance-compliance/security-code-auditor.md)** - Analyze malicious code or exploited vulnerabilities
3. **[data-analysis-insights](../../prompts/analysis/data-analysis-insights.md)** - Correlate logs from multiple sources (SIEM, firewall, EDR)
4. **[technical-documentation-specialist](../../prompts/developers/technical-documentation-specialist.md)** - Document findings and timeline

### Investigation Framework (MITRE ATT&CK)

Use MITRE ATT&CK framework to categorize attacker tactics:

1. **Initial Access**: How did attacker get in? (phishing, exploit, stolen credentials)
2. **Execution**: What did attacker run? (malware, scripts, commands)
3. **Persistence**: Did attacker create backdoors? (scheduled tasks, registry keys, accounts)
4. **Privilege Escalation**: Did attacker gain higher access? (exploit, credential theft)
5. **Defense Evasion**: How did attacker avoid detection? (disable AV, clear logs)
6. **Credential Access**: Were credentials stolen? (keylogging, dumping hashes)
7. **Discovery**: What did attacker enumerate? (network scan, account discovery)
8. **Lateral Movement**: Did attacker spread to other systems? (RDP, PsExec, WMI)
9. **Collection**: What data did attacker gather? (file staging, clipboard capture)
10. **Command and Control (C2)**: How did attacker communicate? (HTTP, DNS, encrypted channel)
11. **Exfiltration**: Was data stolen? (network traffic analysis, file transfer logs)
12. **Impact**: What damage was done? (ransomware, data destruction, defacement)

### Investigation Workflow

```
Step 1: Preserve Evidence (First 15 Minutes)
  - Take forensic images (memory dump, disk image)
  - Collect logs (system, application, security, firewall, SIEM)
  - Photograph screens (if systems being shut down)
  - Document chain of custody (who accessed what, when)
  ↓
Step 2: Timeline Construction (Kill Chain Analysis)
  - Identify Initial Access timestamp (first malicious activity)
  - Map attacker actions chronologically (MITRE ATT&CK tactics)
  - Identify dwell time (how long attacker was in environment before detection)
  ↓
Step 3: Indicator of Compromise (IOC) Extraction
  - File hashes (MD5, SHA256 of malware)
  - IP addresses (C2 servers, attacker infrastructure)
  - Domain names (malicious domains contacted)
  - URLs (phishing links, malware download sites)
  - Email addresses (phishing sender)
  - File paths (malware locations)
  - Registry keys (persistence mechanisms)
  - User accounts (compromised or created by attacker)
  ↓
Step 4: Scope Expansion (Hunt for Lateral Movement)
  - Search all systems for IOCs (file hashes, IPs, domains)
  - Check for same attack patterns on other hosts
  - Review authentication logs (did compromised account access other systems?)
  - Analyze network traffic (lateral movement, data exfiltration)
  ↓
Step 5: Root Cause Analysis
  - What vulnerability was exploited? (CVE, misconfig, weak password)
  - Why did security controls fail? (AV missed malware, SIEM alert ignored)
  - What could have prevented this? (patch management, MFA, network segmentation)
  ↓
Step 6: Data Impact Assessment
  - What files were accessed/exfiltrated/encrypted?
  - Classify data sensitivity (PII, PHI, IP, financial)
  - Determine if encryption keys can recover data (for ransomware)
  - Estimate data loss (if backups unavailable or corrupted)
```

### Example: Investigating Ransomware (Continued from Phase 2)

**Incident**: Ransomware on FS-PROD-01, active C2 blocked, system isolated

**Use security-incident-response + data-analysis-insights prompts**:

```
Prompt: "Conduct forensic investigation of ransomware incident. Evidence collected:

1. Memory Dump: 8GB RAM dump from FS-PROD-01 (captured at 14:50 UTC)
2. Disk Image: 2TB full disk image (captured at 15:30 UTC)
3. Logs Available:
   - Windows Event Logs (System, Security, Application) - 30 days retention
   - EDR Telemetry (Carbon Black) - 90 days retention  
   - Firewall Logs (Palo Alto) - 60 days retention
   - Email Gateway Logs (Proofpoint) - 90 days retention

Analyze and provide:
1. Attack timeline (initial access to detection)
2. MITRE ATT&CK TTPs used
3. IOCs (file hashes, IPs, domains)
4. Scope expansion recommendations
5. Root cause and prevention recommendations"

AI Response (Using data-analysis-insights prompt on logs):

"FORENSIC INVESTIGATION REPORT - Ransomware Incident

ATTACK TIMELINE:
- 2025-11-17 09:23 UTC: INITIAL ACCESS (Phishing Email)
  * Email from "invoices@legitimate-vendor.com" (spoofed) sent to finance@company.com
  * Subject: "Urgent: Payment Overdue - Invoice #8472"
  * Attachment: Invoice_8472.pdf.exe (double extension, 2.3MB)
  * Employee John Smith (jsmith@company.com) opened attachment at 09:23 UTC
  * Email Gateway (Proofpoint) flagged as suspicious but delivered (user override)

- 2025-11-17 09:24 UTC: EXECUTION (Malware Dropper)
  * Invoice_8472.pdf.exe executed by jsmith on workstation WS-FIN-12
  * Dropper SHA256: a3f8d9c2e1b4567890abcdef1234567890abcdef1234567890abcdef12345678
  * Dropper connects to C2: 203.0.113.45:443 (HTTPS, encrypted)
  * Dropper downloads ransomware payload: REvil variant (Sodinokibi)

- 2025-11-17 09:26 UTC: PERSISTENCE (Registry Key)
  * Ransomware creates registry key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svchost
  * Value: C:\Users\jsmith\AppData\Local\Temp\svchost.exe (ransomware payload)

- 2025-11-17 09:28 UTC: CREDENTIAL ACCESS (Mimikatz)
  * Ransomware executes Mimikatz to dump credentials from LSASS process
  * Obtained: Domain admin credentials (dadmin@company.com, password hash)

- 2025-11-17 09:35 UTC: LATERAL MOVEMENT (PsExec)
  * Attacker uses stolen domain admin credentials to connect to file server FS-PROD-01 via PsExec
  * Network connection: WS-FIN-12 → FS-PROD-01:445 (SMB)

- 2025-11-17 09:40 UTC: COLLECTION (File Staging)
  * Ransomware scans file server, identifies 12,000+ files (documents, spreadsheets, source code)
  * Prioritizes file types: .docx, .xlsx, .pdf, .zip, .pst (Outlook archives), .sql (database backups)

- 2025-11-17 10:00-14:20 UTC: EXFILTRATION (Data Theft)
  * Ransomware exfiltrates 85GB data to attacker server 198.51.100.72:8443 (HTTPS, encrypted)
  * Files compressed and uploaded in 500MB chunks (170 uploads total)
  * Firewall detected unusual outbound traffic but alert ignored (assumed backup job)

- 2025-11-17 14:30 UTC: IMPACT (Encryption)
  * Ransomware begins encrypting files on FS-PROD-01
  * Encryption rate: ~250 files/minute (PowerShell script + AES-256 encryption)
  * Ransom note dropped: README_RECOVERY.txt in each encrypted folder
  * Note demands 50 Bitcoin (~$2.1M USD) for decryption key

- 2025-11-17 14:35 UTC: DETECTION (EDR Alert)
  * Carbon Black EDR triggers alert: "Mass file modification detected"
  * Security analyst reviews alert, confirms ransomware (Phase 1 Detection)

- 2025-11-17 14:37 UTC: CONTAINMENT (Initiated)
  * FS-PROD-01 disconnected from network
  * C2 server IP 203.0.113.45 blocked at firewall

TOTAL DWELL TIME: 5 hours 14 minutes (09:23-14:37 UTC)
ENCRYPTION DURATION: 5 minutes (14:30-14:35 UTC)

MITRE ATT&CK TTPs:
- T1566.001: Phishing - Spearphishing Attachment
- T1204.002: User Execution - Malicious File
- T1547.001: Boot or Logon Autostart - Registry Run Keys
- T1003.001: Credential Dumping - LSASS Memory (Mimikatz)
- T1078: Valid Accounts (domain admin)
- T1021.002: Remote Services - SMB/Windows Admin Shares (PsExec)
- T1005: Data from Local System
- T1560.001: Archive Collected Data
- T1041: Exfiltration Over C2 Channel
- T1486: Data Encrypted for Impact (Ransomware)

INDICATORS OF COMPROMISE (IOCs):
File Hashes (SHA256):
- a3f8d9c2e1b4567890abcdef1234567890abcdef1234567890abcdef12345678 (dropper: Invoice_8472.pdf.exe)
- b1c2d3e4f5a6789012345678901234567890abcdef1234567890abcdef123456 (ransomware payload: svchost.exe)

IP Addresses:
- 203.0.113.45 (C2 server, Netherlands)
- 198.51.100.72 (data exfiltration server, Russia)

Domains:
- invoice-payment-update.com (phishing email infrastructure)

Email:
- invoices@legitimate-vendor.com (spoofed sender)

File Paths:
- C:\Users\jsmith\AppData\Local\Temp\svchost.exe
- C:\Users\jsmith\Downloads\Invoice_8472.pdf.exe

Registry Keys:
- HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svchost

Ransom Note:
- README_RECOVERY.txt (contains Bitcoin wallet address: 1BoatSLRHtKNngkdXEeobR76b53LETtpyT)

SCOPE EXPANSION RECOMMENDATIONS:
1. HUNT for IOCs on ALL systems (250 workstations, 50 servers)
   - Search for file hashes a3f8d9c2... and b1c2d3e4...
   - Check network connections to 203.0.113.45 and 198.51.100.72
   - Review registry keys for persistence mechanisms
2. CHECK domain admin account usage (dadmin@company.com)
   - Where else did this account authenticate? (lateral movement)
   - Reset password immediately (compromise confirmed)
3. REVIEW email gateway logs for similar phishing emails
   - Did other employees receive same email?
   - Did anyone else click the attachment?
4. ANALYZE backup integrity
   - Verify file server backups are clean (pre-infection)
   - Check backup retention: last clean backup timestamp (2025-11-16 22:00 UTC)
   - Test restore process (validate before production restore)

ROOT CAUSE ANALYSIS:
Primary: Phishing email with malicious attachment opened by employee
Secondary: Email gateway allowed delivery despite suspicious flag (user override)
Tertiary: Lack of multi-factor authentication (MFA) for domain admin accounts

WHY SECURITY CONTROLS FAILED:
1. Email Gateway: Proofpoint flagged email as suspicious but user overrode warning
   - Recommendation: Disable user override for suspicious attachments
2. Antivirus: Windows Defender failed to detect REvil variant (signature mismatch)
   - Recommendation: Add behavioral analysis (AMSI, ATP) in addition to signature-based detection
3. SIEM: Unusual outbound traffic alert ignored (assumed backup job)
   - Recommendation: Tune SIEM alerts, correlate with approved backup schedules
4. MFA: Domain admin accounts not protected by MFA (Mimikatz stole credentials)
   - Recommendation: Enforce MFA for all privileged accounts (Azure AD Conditional Access)
5. Network Segmentation: File server accessible from user workstations (lateral movement)
   - Recommendation: Segment critical servers, require jump hosts for admin access

PREVENTION RECOMMENDATIONS:
1. IMMEDIATE (Next 7 Days):
   - Enable MFA for all domain admin and privileged accounts
   - Reset all domain admin passwords (assume compromise)
   - Block IOC IPs/domains at firewall (203.0.113.45, 198.51.100.72)
   - Patch workstation WS-FIN-12 and FS-PROD-01 (apply latest security updates)
   - Security awareness training for Finance team (phishing simulation)

2. SHORT-TERM (Next 30 Days):
   - Implement email attachment sandboxing (detonate suspicious files in isolated environment)
   - Deploy EDR to all workstations (current: only servers have Carbon Black)
   - Enable Windows AMSI (Antimalware Scan Interface) for script-based attacks
   - Configure SIEM correlation rules (e.g., 'large data transfer + late night hours = alert')
   - Test incident response playbook (tabletop exercise with Finance and IT teams)

3. LONG-TERM (Next 90 Days):
   - Network micro-segmentation (isolate file servers from user workstations)
   - Implement Zero Trust architecture (authenticate every connection)
   - Deploy DLP (Data Loss Prevention) to detect data exfiltration
   - Conduct penetration test (validate security controls)
   - Establish SOC 24/7 monitoring (current: business hours only)

DATA IMPACT ASSESSMENT:
- Files Accessed: 12,000+ files on FS-PROD-01
- Data Exfiltrated: 85GB (HR records, customer data, source code, financial reports)
- Files Encrypted: 500+ files (before containment stopped encryption)
- Data Classification:
  * RESTRICTED (PHI/PII): 2,500 files (~15GB) - HIPAA + GDPR breach
  * CONFIDENTIAL (IP, source code): 4,000 files (~40GB) - trade secret loss
  * INTERNAL (financial reports): 3,500 files (~20GB) - material non-public info
  * PUBLIC: 2,000 files (~10GB) - no breach impact

RECOVERY OPTIONS:
1. RESTORE FROM BACKUP (Recommended)
   - Last clean backup: 2025-11-16 22:00 UTC (18 hours before infection)
   - Data loss: 18 hours of file changes (acceptable per RPO)
   - Estimated restore time: 4-6 hours
   - Cost: $0 (backups are clean and tested)

2. PAY RANSOM (NOT Recommended)
   - Cost: 50 BTC (~$2.1M USD)
   - No guarantee of decryption key delivery (REvil group has history of scams)
   - Funds terrorist organizations (FBI advises against payment)
   - Does NOT recover exfiltrated data (attacker still has 85GB copy)

3. DECRYPT WITHOUT KEY (Not Feasible)
   - REvil uses AES-256 encryption (computationally infeasible to crack)
   - No known decryption flaws for this variant

RECOMMENDATION: Proceed to Phase 4 (Containment) with backup restore strategy"
```

### Investigation Checklists

**Evidence Preservation**:
- [ ] Forensic images captured (memory dump, disk image)
- [ ] Logs collected from all relevant sources (SIEM, firewall, EDR, email gateway)
- [ ] Screenshots taken (ransom notes, error messages, system states)
- [ ] Chain of custody documented (who accessed evidence, when, for what purpose)
- [ ] Evidence stored securely (encrypted, access-controlled, hash verified)

**Timeline Construction**:
- [ ] Initial access timestamp identified (first malicious activity)
- [ ] Attack progression mapped (each stage of kill chain)
- [ ] Dwell time calculated (time between initial access and detection)
- [ ] Encryption/impact duration measured (for ransomware/destructive attacks)
- [ ] Detection timestamp recorded (when incident was discovered)

**IOC Extraction**:
- [ ] File hashes documented (MD5, SHA256 of malware samples)
- [ ] IP addresses logged (C2 servers, data exfiltration destinations)
- [ ] Domain names recorded (malicious domains contacted)
- [ ] Email addresses captured (phishing senders, attacker communications)
- [ ] User accounts identified (compromised accounts, attacker-created accounts)
- [ ] Registry keys/file paths documented (persistence mechanisms)

**Scope Expansion Hunt**:
- [ ] IOC search completed across all systems (workstations, servers, network devices)
- [ ] Lateral movement analysis completed (which systems did attacker access)
- [ ] Compromised account usage reviewed (authentication logs, access history)
- [ ] Similar attack patterns identified (other phishing emails, same vulnerability exploited)

**Root Cause Analysis**:
- [ ] Initial vulnerability or weakness identified (phishing, unpatched software, weak password)
- [ ] Security control failures analyzed (why AV didn't detect, why SIEM alert ignored)
- [ ] Prevention recommendations documented (immediate, short-term, long-term)

### Deliverables (Phase 3)

- **Forensic Investigation Report** (5-10 pages):
  - Executive summary (1 page: what happened, impact, next steps)
  - Detailed timeline (chronological attack progression with MITRE ATT&CK mapping)
  - IOC list (file hashes, IPs, domains, emails, registry keys)
  - Scope expansion findings (lateral movement, other affected systems)
  - Root cause analysis (why attack succeeded, why controls failed)
  - Recovery recommendations (restore from backup vs pay ransom vs decrypt)
  - Prevention recommendations (immediate, short-term, long-term actions)
- **Evidence Package**:
  - Forensic images (memory dump, disk image) - stored securely
  - Log archives (SIEM, firewall, EDR, email gateway) - timestamped and hashed
  - Chain of custody log - who accessed evidence, when, for what purpose
- **IOC Feed** (for sharing with threat intelligence):
  - STIX/TAXII format IOCs (file hashes, IPs, domains)
  - MITRE ATT&CK TTPs (techniques used)
  - Yara rules (for malware detection)
- **Updated Incident Ticket**:
  - Investigation findings summary
  - Confirmed scope (systems, users, data affected)
  - Regulatory breach confirmation (GDPR, HIPAA status)
  - Recommended response strategy (eradication approach, recovery plan)

### Tool Recommendations

**Forensic Analysis**:
- **Memory Analysis**: Volatility Framework (analyze memory dumps for malware, credentials, network connections)
- **Disk Forensics**: Autopsy, FTK Imager (timeline analysis, file carving, artifact extraction)
- **Log Analysis**: Splunk, ELK Stack, Azure Sentinel (correlate logs from multiple sources)
- **Malware Analysis**: IDA Pro, Ghidra, REMnux (reverse engineer malware samples)

**Threat Intelligence**:
- **VirusTotal**: Check file hashes against global malware database
- **AlienVault OTX**: Research IOCs and attacker infrastructure
- **MISP**: Share IOCs with industry peers (ISACs)
- **Shodan**: Research attacker IP addresses and infrastructure

**Network Forensics**:
- **Wireshark**: Analyze packet captures (PCAP files) for C2 traffic and data exfiltration
- **Zeek (Bro)**: Network traffic analysis and logging
- **NetworkMiner**: Extract files and artifacts from network traffic

---

## Next Steps

**Phases 4-6 will be added in subsequent iterations**:
- **Phase 4: Containment** (Isolate threat, prevent spread)
- **Phase 5: Remediation** (Eradicate malware, restore services)
- **Phase 6: Post-Mortem** (Lessons learned, process improvements)

**[Continue to Iteration 2 →]()**

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-17 | Initial playbook created (Phases 1-3: Detection, Triage, Investigation) |

---

**Maintained by**: [Repository Contributors](../../CONTRIBUTING.md)  
**License**: MIT
