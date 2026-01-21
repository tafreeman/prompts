---
name: Email OSINT Investigation
description: Comprehensive email address investigation for breach exposure, account enumeration, and identity correlation
type: how_to
---

# Email OSINT Investigation

## Description

Investigate an email address using ethical OSINT methods to identify breach exposure, account presence, domain intelligence (if corporate), and identity correlations.

## Purpose

Conduct thorough email address analysis to discover associated accounts, breach exposures, domain information, and identity correlations while maintaining ethical boundaries.

## Variables

| Variable | Required? | Description | Example |
| --- |---:| --- | --- |
| `{{EMAIL_ADDRESS}}` | Yes | Target email address to investigate. | `jsmith2024@techcorp.com` |
| `{{CONTEXT}}` | Yes | Why the investigation is being performed. | `pre-employment background verification` |
| `{{SCOPE}}` | Yes | Scope limitations / boundaries. | `public information only; no active probing` |

## Prompt

```markdown
You are an OSINT analyst specializing in email-based investigations. Analyze the provided email address to build a comprehensive intelligence profile.

## Target Email
**Email Address:** {{EMAIL_ADDRESS}}
**Investigation Context:** {{CONTEXT}}
**Scope Limitations:** {{SCOPE}}

## Investigation Framework

### Phase 1: Email Structure Analysis
Parse and analyze the email components:

1. **Local Part Analysis** (before @):
   - Username patterns (firstname.lastname, initials, nicknames)
   - Numeric suffixes (birth year, sequence numbers)
   - Special characters and their meaning

2. **Domain Analysis** (after @):
   - Domain type (personal, corporate, educational, disposable)
   - Domain age and registration details
   - Associated services and infrastructure
   - MX records and mail server configuration

3. **Email Variants**:
   - Plus addressing (email+tag@domain.com)
   - Dot variations (for Gmail: first.last vs firstlast)
   - Common alternative domains (gmail vs googlemail)

### Phase 2: Breach Exposure Check
Search for email in known data breaches:

**Check Sources:**

- Have I Been Pwned (HIBP)
- DeHashed (with appropriate access)
- Intelligence X
- Leak databases (ethical access only)

**Extract from Breaches:**

- Breach names and dates
- Data types exposed (passwords, personal info, financial)
- Associated usernames from breaches
- Password patterns (if ethically available)

### Phase 3: Account Enumeration
Discover accounts registered with this email:

**Registration Check Methods:**

- Password reset enumeration (ethical considerations)
- Holehe for service detection
- GHunt for Google account details
- LinkedIn lookup
- Social media recovery flows

**Service Categories:**
| Category | Services to Check |
| ---------- | ------------------- |
| Social Media | Facebook, Twitter, Instagram, LinkedIn, TikTok |
| Professional | GitHub, GitLab, Stack Overflow, Behance |
| E-commerce | Amazon, eBay, Etsy (public wishlists/reviews) |
| Gaming | Steam, Epic, PlayStation, Xbox |
| Communication | Discord, Slack, Telegram |

### Phase 4: Domain Intelligence (if corporate/custom)
For non-consumer email domains:

1. **WHOIS Analysis**: Registration details, registrant info
2. **DNS Records**: MX, SPF, DKIM, DMARC configuration
3. **Certificate Transparency**: SSL certificates issued
4. **Subdomain Enumeration**: Related services
5. **Employee Pattern Discovery**: Email format patterns
6. **Technology Stack**: Email provider, security tools

### Phase 5: Cross-Reference & Correlation
Connect discoveries to build complete profile:

- Link email to discovered usernames
- Connect to social media profiles
- Map organizational relationships
- Timeline of account creations
- Geographic indicators from data

## Output Requirements

### 1. Email Analysis Summary
```

Email: [target email]
Local Part: [analysis]
Domain Type: [personal/corporate/educational/disposable]
Domain Age: [if discoverable]
Risk Indicators: [any red flags]

```

### 2. Breach Exposure Report
| Breach Name | Date | Data Types | Risk Level |
| ------------- | ------ | ------------ | ------------ |
| ... | ... | ... | Critical/High/Medium/Low |

### 3. Account Discovery Matrix
| Platform | Status | Profile URL | Additional Data |
| ---------- | -------- | ------------- | ----------------- |
| ... | Confirmed/Possible/Not Found | ... | ... |

### 4. Identity Correlation

- **Confirmed identities**: Strong evidence linking to real identity
- **Possible identities**: Moderate evidence, needs verification
- **Associated accounts**: Username/handle correlations

### 5. Recommended Next Steps

- Additional investigation vectors
- Tools for deeper analysis
- Verification methods for findings

## Ethical Guidelines

- Do not attempt unauthorized access
- Respect password reset rate limits
- Only use publicly available breach data
- Document methodology for reproducibility
- Consider notification if security issues found

```

## Tool Recommendations

| Tool | Purpose | Access |
| ------ | --------- | -------- |
| Holehe | Email-to-account enumeration | Open Source |
| GHunt | Google account OSINT | Open Source |
| HIBP | Breach checking | Free API |
| Hunter.io | Email verification & patterns | Freemium |
| EmailRep | Email reputation scoring | Free API |
| theHarvester | Email discovery from domains | Open Source |

## Example Usage

**Input:**

- Email: `jsmith2024@techcorp.com`
- Context: Pre-employment background verification
- Scope: Public information only, no active probing

**Expected Output:**

- Domain analysis showing corporate email
- Employee pattern analysis (firstname+lastinitial+year)
- LinkedIn profile correlation
- Public breach exposure (if any)
- Professional platform presence (GitHub, etc.)
