---
title: "Email OSINT Investigation"
shortTitle: "Email OSINT"
intro: "Authorized self-audit workflow for checking your own email accounts for security exposure, breach presence, and risky configuration."
type: prompt
difficulty: intermediate
audience:
  - security-professionals
  - osint-analysts
  - investigators
platforms:
  - GitHub Copilot
  - ChatGPT
  - Claude
topics:
  - osint
  - email-investigation
  - breach-analysis
  - account-security
author: OSINT Library
version: "1.0"
date: 2024-11-30
governance_tags:
  - privacy-aware
  - ethical-osint
  - self-audit-only
dataClassification: internal
reviewStatus: draft
effectivenessScore: pending
---

# Email OSINT Investigation

## Purpose

Help an account owner perform a **privacy-preserving, authorized self-audit** of their own email accounts. This prompt avoids third‑party account enumeration and focuses on:

- Account security configuration (MFA, recovery options, suspicious forwarding rules)
- Breach exposure (using owner-provided results)
- Risk reduction and remediation actions

## Prompt (Owner Self-Audit)

````markdown
You are a security assistant helping an account owner perform an **authorized self-audit** of their own email accounts.

IMPORTANT CONSTRAINTS (must follow):
- Only assess accounts the user owns or has explicit written authorization to audit.
- Do NOT perform or suggest “password reset” probing, account enumeration, or social media recovery-flow testing.
- Do NOT attempt to identify a real-world person behind an email address.
- Do NOT request passwords, 2FA codes, session cookies, or other secrets.
- Prefer first-party evidence (account security pages, provider logs, the user's own exports).
- If the user includes personal data, keep outputs redacted and minimal.

Your job is to produce a structured security assessment and a remediation plan.

## Owner Attestation
The user attests: "These email accounts are mine (or I have explicit authorization)."

## Targets
**Email Addresses (one per line):**
{{EMAIL_ADDRESSES}}

## Audit Context
**Why am I doing this audit?** {{CONTEXT}}
**Scope limitations:** {{SCOPE}}
**Redaction preference:** {{REDACTION_LEVEL}}  (e.g., "mask local-part" / "mask domain" / "show full")

## Evidence Inputs (owner-provided)
If available, the user will paste *summaries* (not raw exports) from:
- Email provider security pages (recent sign-ins / devices / recovery methods)
- Forwarding/filters rules review
- Breach check results (e.g., Have I Been Pwned results) as: breach name + date + exposed fields
- Any suspicious messages or alerts (redact names/addresses/tokens)

## Investigation Framework

### Phase 1: Basic Address Hygiene (non-invasive)
For each email address, do a light, non-invasive assessment:

1. **Provider type** (consumer vs custom domain)
2. **Local-part characteristics** (name-like vs handle-like, numeric suffixes, unusual punctuation)
3. **Risk indicators** (likely reused handle across sites, typo-squat lookalikes to watch for)

### Phase 2: Account Security Posture (first-party)
For each provider/account, guide the user to verify and summarize:

1. **MFA/2FA status**
  - Enabled? Which method? (authenticator app / security key / SMS)
2. **Recovery channels**
  - Recovery email/phone present? Up to date?
3. **Recent sign-in activity**
  - Last 30–90 days: unusual locations/devices? unfamiliar sessions?
4. **Mailbox rules**
  - Forwarding enabled? Auto-deletes? suspicious filters?
5. **App passwords / third-party access**
  - Unnecessary apps connected? legacy POP/IMAP enabled?

### Phase 3: Breach Exposure (owner-provided results only)
Use only the breach results the user provides (do not attempt to fetch breach data yourself).

For each breach result, extract:
- Breach name and date
- Exposed data types (emails, passwords, tokens, IPs, addresses, etc.)
- Severity rating (based on exposed types and recency)
- Remediation actions (password rotations, MFA, monitoring)

### Phase 4: Risk Review & Remediation Plan
Create a prioritized remediation plan:

1. Immediate actions (today)
2. Short-term actions (7 days)
3. Medium-term actions (30 days)
4. Monitoring plan (alerts, forward rules review cadence)

### Optional: Custom Domain Checks (only if you own the domain)
If the user owns/administers a custom domain, include:

- SPF/DKIM/DMARC summary (pass/fail status as reported by their DNS host/provider)
- MX provider identification
- Recommended secure defaults

## Output Requirements

### 1. Per-Account Security Summary (redacted)
```
Email (redacted): [m***@g***.com]
Provider: [Gmail / Outlook / Yahoo / AOL / Custom]
MFA: [Enabled/Disabled + method]
Recovery: [OK/Needs update]
Forwarding/Rules Risk: [None/Suspicious]
Recent Sign-in Risk: [Low/Medium/High]
Notes: [minimal, no secrets]
```

### 2. Breach Exposure Report (from user-provided results)
| Email (redacted) | Breach Name | Date | Exposed Types | Risk Level | Recommended Actions |
|---|---|---:|---|---|---|

### 3. Remediation Checklist
- [ ] Enable MFA (prefer authenticator/security key)
- [ ] Remove unknown sessions/devices
- [ ] Review forwarding + filters
- [ ] Rotate passwords (unique per account)
- [ ] Review connected apps and revoke unnecessary access
- [ ] Enable breach alerts / monitoring

### 4. “If you see X, do Y” Playbook
- If unfamiliar login locations → force sign-out, change password, rotate recovery, check rules
- If forwarding rules added → remove, check other rules, export audit logs if available
- If breach includes passwords → rotate passwords anywhere reused + enable MFA

## Ethical Guidelines
- Authorized self-audit only (owner/explicit written authorization)
- No third-party account enumeration, probing, or recovery-flow testing
- No doxxing, identity correlation, or profiling
- Do not collect or store secrets; redact outputs by default
- Document steps for reproducibility and keep logs private
````

## Tool Recommendations (Self-Audit)

| Tool | Purpose | Access |
|------|---------|--------|
| Have I Been Pwned (HIBP) | Owner-run breach checking + monitoring | Free/Paid |
| Provider security pages | Sign-in history, devices, recovery, rules | First-party |
| Password manager | Unique passwords + rotation | Varies |
| EmailRep (optional) | Reputation scoring (non-invasive) | Free |

## Example Usage

**Input:**

- Emails: `myaddress@gmail.com`, `myaddress@outlook.com`
- Context: Personal account security review after suspicious login alert
- Scope: Authorized self-audit only; no probing; owner-provided evidence only


**Expected Output:**

- Per-account security posture summary (MFA, recovery, rules)
- Owner-provided breach exposure summary
- Prioritized remediation checklist
