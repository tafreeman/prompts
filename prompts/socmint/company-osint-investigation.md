---
title: Company OSINT Investigation
shortTitle: Company OSINT
intro: Comprehensive open-source intelligence gathering on organizations, including
  corporate structure, digital footprint, and threat surface analysis
type: prompt
difficulty: advanced
audience:

- security-professionals
- osint-analysts
- investigators
- competitive-intelligence

platforms:

- github-copilot
- chatgpt
- claude

topics:

- osint
- corporate-intelligence
- threat-surface
- due-diligence

author: OSINT Library
version: '1.0'
date: '2024-11-30'
governance_tags:

- privacy-aware
- ethical-osint

dataClassification: internal
reviewStatus: draft
effectivenessScore: pending
---

# Company OSINT Investigation

## Description

Comprehensive open-source intelligence (OSINT) research on an organization to understand corporate structure, digital footprint, and externally observable security posture for due diligence or security assessment.

## Purpose

Conduct comprehensive open-source intelligence gathering on an organization to understand its structure, digital presence, potential vulnerabilities, and threat surface for security assessment or due diligence purposes.

## Variables

| Variable | Required? | Description | Example |
| --- |---:| --- | --- |
| `{{COMPANY_NAME}}` | Yes | Target organization name. | `TechCorp Industries` |
| `{{PRIMARY_DOMAIN}}` | No | Known primary domain for the organization. | `techcorp.com` |
| `{{INDUSTRY_SECTOR}}` | No | Industry/sector for context and prioritization. | `SaaS / Technology` |
| `{{CONTEXT}}` | Yes | Investigation purpose (why you are researching). | `pre-acquisition security due diligence` |
| `{{BOUNDARIES}}` | Yes | Scope boundaries and constraints. | `public sources only; no active probing` |

## Prompt

```markdown
You are a corporate intelligence analyst conducting comprehensive OSINT research on an organization. Gather and analyze publicly available information to build a complete organizational intelligence picture.

## Target Organization
**Company Name:** {{COMPANY_NAME}}
**Known Domain:** {{PRIMARY_DOMAIN}}
**Industry:** {{INDUSTRY_SECTOR}}
**Investigation Purpose:** {{CONTEXT}} (security assessment/due diligence/competitive intel/threat hunting)
**Scope:** {{BOUNDARIES}}

## Investigation Framework

### Phase 1: Corporate Structure Analysis
Map the organizational structure:

**Business Registration:**

- Legal entity name and type
- Registration number/EIN
- Incorporation state/country
- Registration date
- Registered agent
- Business status (active/inactive)

**Corporate Hierarchy:**

- Parent company
- Subsidiaries and affiliates
- Joint ventures
- Recent M&A activity
- International entities

**Sources:**
| Source | Information Type | Access |
| -------- | ------------------ | -------- |
| SEC EDGAR | Public filings (US) | Free |
| Companies House | UK registrations | Free |
| OpenCorporates | Global database | Freemium |
| LinkedIn | Structure, employees | Free |
| Crunchbase | Funding, investors | Freemium |

### Phase 2: Leadership & Key Personnel
Identify and profile key individuals:

**Executive Team:**

- C-suite executives
- Board members
- Key technical leaders
- Security/IT leadership

**For Each Individual:**

- Professional history
- Educational background
- Public statements/interviews
- Social media presence
- Speaking engagements
- Published works

**Employee Intelligence:**

- Total employee count
- Department breakdown
- Key technical staff (from GitHub, LinkedIn)
- Recent hires/departures
- Employee sentiment (Glassdoor, Blind)

### Phase 3: Digital Footprint Mapping
Comprehensive technical reconnaissance:

**Domain Intelligence:**
```

Primary domain: [domain.com]
Additional domains: [list discovered]
Subdomains: [enumeration results]
Historical domains: [Wayback, DNS history]

```

**DNS Analysis:**
| Record Type | Data | Intelligence Value |
| ------------- | ------ | ------------------- |
| A/AAAA | IP addresses | Infrastructure mapping |
| MX | Mail servers | Email provider |
| TXT | SPF/DKIM/DMARC | Security posture |
| NS | Nameservers | DNS provider |
| CNAME | Aliases | Service mapping |

**Infrastructure Mapping:**

- IP ranges and ASN
- Hosting providers
- CDN usage
- Cloud platforms (AWS, Azure, GCP indicators)
- Geographic distribution

**Web Presence:**

- Main website analysis
- Technology stack (Wappalyzer, BuiltWith)
- CMS identification
- Third-party integrations
- Analytics/tracking codes

### Phase 4: Security Posture Assessment
Evaluate external security indicators:

**Certificate Intelligence:**

- SSL/TLS certificates issued
- Certificate Transparency logs
- Expiration monitoring
- CA usage patterns

**Exposure Analysis:**

- Shodan/Censys results
- Open ports and services
- Version information
- Known vulnerabilities
- Default credentials

**Breach History:**

- Historical data breaches
- Leaked credentials (aggregate data only)
- Dark web mentions
- Paste site appearances

**Security Controls (Observable):**

- Email security (SPF/DKIM/DMARC)
- Web security headers
- WAF indicators
- Bug bounty program
- Security certifications (SOC2, ISO27001)

### Phase 5: Social & Public Presence
Analyze public communications:

**Official Channels:**
| Platform | Handle | Followers | Activity |
| ---------- | -------- | ----------- | ---------- |
| Twitter/X | ... | ... | ... |
| LinkedIn | ... | ... | ... |
| Facebook | ... | ... | ... |
| YouTube | ... | ... | ... |
| Blog | ... | ... | ... |

**Press & Media:**

- Recent news coverage
- Press releases
- Industry publications
- Analyst reports
- Regulatory filings

**Reputation Analysis:**

- Customer reviews
- Employee reviews (Glassdoor)
- BBB rating
- Industry awards/recognition
- Legal proceedings

### Phase 6: Technical Reconnaissance
Deeper technical analysis:

**Code Repositories:**

- GitHub organization
- Public repositories
- Contributor analysis
- Code quality indicators
- Exposed secrets (historical)

**Job Postings Analysis:**

- Technology stack indicators
- Security team size
- Compliance requirements
- Growth areas

**Document Metadata:**

- Public PDFs, documents
- Author information
- Software versions
- Internal paths leaked

**Email Pattern Discovery:**

- Format identification (first.last@, firstl@)
- Key email addresses
- Distribution lists (if discoverable)

## Output Requirements

### 1. Executive Summary
```

Organization: [Full legal name]
Industry: [Sector]
Founded: [Year]
Headquarters: [Location]
Employee Count: [Estimate]
Revenue: [If public/estimated]
Key Finding: [Most significant discovery]
Risk Level: [Assessment if applicable]

```

### 2. Corporate Structure Map
```

[Parent Company]
├── [Target Company]
│   ├── [Subsidiary 1]
│   ├── [Subsidiary 2]
│   └── [Division/Brand]
└── [Affiliate Company]

```

### 3. Digital Asset Inventory
| Asset Type | Details | Risk/Notes |
| ------------ | --------- | ------------ |
| Domains | [count] domains discovered | ... |
| Subdomains | [count] subdomains | ... |
| IP Ranges | [ranges] | ... |
| Cloud Services | [providers] | ... |
| Social Media | [count] accounts | ... |

### 4. Key Personnel
| Name | Title | LinkedIn | Notes |
| ------ | ------- | ---------- | ------- |
| ... | ... | ... | ... |

### 5. Security Findings (if applicable)
| Finding | Severity | Evidence | Recommendation |
| --------- | ---------- | ---------- | ---------------- |
| ... | Critical/High/Medium/Low | ... | ... |

### 6. Threat Surface Summary

- **External Attack Surface**: Summary of exposed assets
- **Information Leakage**: Sensitive data exposure
- **Third-Party Risk**: Vendor and integration risks
- **Human Factor**: Social engineering exposure

### 7. Intelligence Gaps

- Information not discoverable
- Areas requiring further investigation
- Recommended additional tools/methods

## Ethical & Legal Considerations

- Only use publicly available information
- Do not attempt unauthorized access
- Respect robots.txt and rate limits
- No social engineering or deception
- Document all sources for verification
- Consider responsible disclosure for findings

```

## Tool Reference

| Category | Tool | Purpose |
| ---------- | ------ | --------- |
| Domain | Subfinder, Amass | Subdomain enumeration |
| DNS | DNSDumpster, SecurityTrails | DNS intelligence |
| Web | Wappalyzer, BuiltWith | Technology stack |
| Infrastructure | Shodan, Censys | Internet scanning |
| Email | Hunter.io, theHarvester | Email discovery |
| Code | TruffleHog, GitLeaks | Secret scanning |
| Corporate | OpenCorporates, SEC EDGAR | Business records |

## Example Usage

**Input:**

- Company: TechCorp Industries
- Domain: techcorp.com
- Industry: SaaS/Technology
- Purpose: Pre-acquisition security due diligence

**Expected Output:**

- Complete corporate structure with 3 subsidiaries
- Executive team profiles
- 47 subdomains discovered
- Cloud infrastructure on AWS (3 regions)
- 2 medium-severity security findings
- Clean breach history
- Strong security posture indicators
