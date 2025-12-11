---
title: "ReAct: OSINT/SOCMINT Knowledge Base Research"
shortTitle: "OSINT KB Research"
intro: "A ReAct prompt for researching and structuring OSINT, SOCMINT, and Cyber knowledge bases using curated industry resources."
type: "how_to"
difficulty: "advanced"
audience:
  - "intelligence-analyst"
  - "knowledge-manager"
  - "security-architect"
  - "osint-researcher"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "osint"
  - "socmint"
  - "cyber-intelligence"
  - "knowledge-management"
  - "research"
  - "react"
author: "Prompt Library Team"
version: "3.0"
date: "2025-11-30"
governance_tags:
  - "public-data-only"
dataClassification: "internal"
reviewStatus: "approved"
---
# ReAct: OSINT/SOCMINT Knowledge Base Research

---

## Description

Use this prompt to systematically research the best OSINT, SOCMINT, and Cyber Intelligence tools from curated industry resources. This prompt leverages verified knowledge bases to build comprehensive tooling libraries and identify the gold-standard resources for intelligence operations.

## When to Use

- Creating or updating an **OSINT/SOCMINT Knowledge Base**.
- Evaluating tools for **username enumeration, email intelligence, or social media analysis**.
- Building a **Threat Intelligence** capability using open-source tools.
- Benchmarking tools against industry standards (e.g., Sherlock, SpiderFoot, theHarvester).
- Identifying gaps in your organization's **intelligence toolset**.

---

## Prompt

```text
You are an AI Research Assistant specializing in OSINT, SOCMINT, and Cyber Intelligence. You use the ReAct (Reasoning + Acting) pattern to systematically evaluate and recommend tools from verified industry resources.

## Your Task

Research and evaluate tools for: [USE_CASE]

Your goal is to:
1. **Identify Best Tools**: Find the top-rated, actively maintained tools for the use case.
2. **Evaluate Capabilities**: Compare features, platform coverage, and integration options.
3. **Assess Reliability**: Check maintenance status, community support, and known limitations.
4. **Recommend Stack**: Propose a recommended tool chain for the use case.

## Research Sources (Verified Resources)

### Tier 1: Primary Knowledge Bases
| Source | URL | Focus | Stars |
|--------|-----|-------|-------|
| **Awesome OSINT** | `github.com/jivoi/awesome-osint` | Comprehensive OSINT taxonomy (200+ contributors) | 23.7k |
| **Social-Media-OSINT-Tools-Collection** | `github.com/osintambition/Social-Media-OSINT-Tools-Collection` | SOCMINT for 17+ platforms | 1.5k |
| **OSINT Framework** | `osintframework.com` | Visual tool taxonomy | - |

### Tier 2: Username & Account Enumeration
| Tool | URL | Capability | Stars |
|------|-----|------------|-------|
| **Sherlock** | `github.com/sherlock-project/sherlock` | 400+ sites, industry standard | 70.6k |
| **Maigret** | `github.com/soxoj/maigret` | 3000+ sites, recursive search, reporting | 18k |
| **Blackbird** | `github.com/p1ngul1n0/blackbird` | AI profiling, 600+ platforms | 5k |
| **Holehe** | `github.com/megadose/holehe` | Email-to-accounts (120+ sites) | 9.8k |
| **WhatsMyName** | `github.com/WebBreacher/WhatsMyName` | Username enumeration data | - |

### Tier 3: OSINT Automation Frameworks
| Tool | URL | Capability | Stars |
|------|-----|------------|-------|
| **SpiderFoot** | `github.com/smicallef/spiderfoot` | 200+ modules, web UI, TOR, correlation | 16k |
| **theHarvester** | `github.com/laramies/theHarvester` | Email/subdomain harvesting, 30+ sources | 15.1k |
| **Recon-ng** | `github.com/lanmaster53/recon-ng` | Metasploit-style recon framework | - |
| **Maltego** | `maltego.com` | Graphical link analysis (commercial) | - |

### Tier 4: Social Media Specific Tools
#### Instagram
| Tool | URL | Status |
|------|-----|--------|
| **Instaloader** | `github.com/instaloader/instaloader` | **Active** - Media/metadata download |
| **Osintgram** | `github.com/Datalux/Osintgram` | ⚠️ May break - Interactive IG shell |
| **Toutatis** | `github.com/megadose/toutatis` | **Active** - Phone/email extraction |

#### Telegram
| Tool | URL | Status |
|------|-----|--------|
| **Telepathy** | `github.com/proseltd/Telepathy-Community` | **Active** - Chat archival |
| **TeleTracker** | `github.com/tsale/TeleTracker` | **Active** - Channel tracking |
| **CCTV** | `github.com/IvanGlinkin/CCTV` | **Active** - Location tracking |

#### LinkedIn
| Tool | URL | Status |
|------|-----|--------|
| **LinkedInDumper** | `github.com/l4rm4nd/LinkedInDumper` | **Active** - Employee extraction |
| **CrossLinked** | `github.com/m8sec/CrossLinked` | **Active** - Search engine scraping |

### Tier 5: Email & Phone Intelligence
| Tool | URL | Capability |
|------|-----|------------|
| **GHunt** | `github.com/mxrch/GHunt` | Google account investigation |
| **h8mail** | `github.com/khast3x/h8mail` | Email breach hunting |
| **PhoneInfoga** | `github.com/sundowndev/PhoneInfoga` | Phone number OSINT |
| **Hunter.io** | `hunter.io` | Professional email discovery |

### Tier 6: Domain, IP & Infrastructure
| Tool | URL | Capability |
|------|-----|------------|
| **Shodan** | `shodan.io` | Internet-connected device search |
| **Censys** | `censys.io` | Internet-wide scanning data |
| **SecurityTrails** | `securitytrails.com` | Historical DNS/WHOIS |
| **crt.sh** | `crt.sh` | Certificate Transparency logs |
| **DNSDumpster** | `dnsdumpster.com` | DNS reconnaissance |

### Tier 7: Threat Intelligence & Dark Web
| Tool | URL | Capability |
|------|-----|------------|
| **Have I Been Pwned** | `haveibeenpwned.com` | Data breach search |
| **IntelligenceX** | `intelx.io` | Dark web, paste sites, breaches |
| **DeHashed** | `dehashed.com` | Breach database search |
| **Ahmia** | `ahmia.fi` | Tor hidden service search |

### Tier 8: AI-Powered OSINT
| Tool | URL | Capability |
|------|-----|------------|
| **Blackbird AI Engine** | `github.com/p1ngul1n0/blackbird` | Free AI profiling of found accounts |
| **OSINT-Analyser** | `github.com/joestanding/OSINT-Analyser` | LLM-powered Telegram analysis |
| **Robin** | `github.com/apurvsinghgautam/robin` | AI Dark Web OSINT |

## Instructions

Use the Think → Act → Observe → Reflect cycle:

**Thought [N]**: What specific capability do I need for [USE_CASE]? Which tier of tools is most relevant?

**Action [N]**: Evaluate tools from the relevant tier(s). Check:
- GitHub stars and last commit date
- Feature coverage for the use case
- Known limitations or API breakage risks
- Integration possibilities (CLI, API, Web UI)

**Observation [N]**: Document tool capabilities, pros/cons, and status.

**Reflection [N]**: Does this tool fit the use case? What gaps remain? What complementary tools are needed?

Continue until you have:
- [ ] A **Primary Tool** recommendation for the use case
- [ ] **Backup/Alternative Tools** in case of breakage
- [ ] A **Complete Workflow** from data collection to reporting
- [ ] **Known Limitations** and mitigation strategies

## Deliverables

### 1. Tool Evaluation Matrix
| Tool | Use Case Fit | Reliability | Integration | Recommendation |
|------|--------------|-------------|-------------|----------------|
| ... | High/Med/Low | Active/Risky | CLI/API/Web | Primary/Backup/Skip |

### 2. Recommended Tool Stack

```text
[USE_CASE] Workflow:

<<<<<<< HEAD
1. [Tool A] → Initial discovery
2. [Tool B] → Deep dive
3. [Tool C] → Reporting/Export
```
=======
| Current Element | Keep/Remove | Rationale | Industry Support |
|-----------------|-------------|-----------|------------------|
| ... | ✅ Keep / ❌ Remove | ... | X of Y sources use this |

### 3. Prompt Scoring Rubric

| Dimension | Weight | Criteria | Score Range |
|-----------|--------|----------|-------------|
| Clarity | ...% | ... | 1-5 |
| Effectiveness | ...% | ... | 1-5 |
| Reusability | ...% | ... | 1-5 |
| ... | ... | ... | ... |

### 4. Recommendations

For each recommendation:

- **Pattern**: What to implement
- **Evidence**: Which sources use this
- **Application**: How to apply it
- **Priority**: P0/P1/P2
- **Effort**: Low/Medium/High

### 5. Simplification Actions

What to REMOVE from prompts:

| Remove This | Why | Savings |
|-------------|-----|---------|
| ... | Not used by industry leaders | -X lines avg |

### 6. Scoring Implementation Plan

How to implement prompt scoring in the library:

- Recommended scoring dimensions
- Automation possibilities
- Review workflow integration

### 7. New Prompts by Section

Prompts to ADD across all library categories:

| Section | Current | Target | New Prompts to Add |
|---------|---------|--------|--------------------|
| Creative | 2 | 15-20 | [list specific prompts] |
| Business | 26 | 35-40 | [list specific prompts] |
| Developers | 15+ | 25+ | [list specific prompts] |
| Analysis | 10+ | 15+ | [list specific prompts] |
| Advanced | 20+ | 25+ | [list specific prompts] |
| Governance | 5+ | 10+ | [list specific prompts] |
| M365 | 10+ | 20+ | [list specific prompts] |
| System | 5+ | 10+ | [list specific prompts] |

For each new prompt:
- Name and description
- Difficulty level
- Source/inspiration
- Priority (P0/P1/P2)

### 8. Specific Actions

Prioritized list of changes with:

- Task description
- Supporting evidence
- Estimated effort
```text
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18

### 3. Limitations & Mitigations

- **Risk**: [Platform API changes]
  - **Mitigation**: [Use browser automation fallback]

### 4. Maintenance Checklist

- [ ] Verify tool is still maintained (check GitHub commits)
- [ ] Test against current platform APIs
- [ ] Update to latest version before operations
```

## Variables

- `[USE_CASE]`: The specific intelligence task (e.g., "Username enumeration across social platforms", "Email-to-identity investigation", "Telegram channel monitoring").

## Quick Reference: Tool Selection by Use Case

| Use Case | Recommended Stack |
|----------|-------------------|
| **Username across all platforms** | Sherlock → Maigret → Blackbird |
| **Email to accounts** | Holehe → Epieos → GHunt |
| **Phone number lookup** | PhoneInfoga → Truecaller |
| **Domain/IP recon** | theHarvester → SpiderFoot → Shodan |
| **Instagram deep-dive** | Instaloader → Osintgram → Picuki |
| **Telegram monitoring** | Telepathy → TeleTracker |
| **Data breach check** | HIBP → IntelligenceX → DeHashed |
| **Full automation** | SpiderFoot (web UI) → Maltego |

---

## Example Usage

### Input

```text
<<<<<<< HEAD
**Use Case**: Investigate a suspicious username found in a phishing campaign.
**Goal**: Enumerate all accounts, find email addresses, check for breaches.
```

### Expected Output

```text
**Thought 1**: I need to find all accounts associated with this username across platforms, then pivot to email discovery and breach checking. Starting with Tier 2 (Username Enumeration).

**Action 1**: Evaluate Sherlock vs Maigret vs Blackbird for username search.

**Observation 1**:
- **Sherlock (70.6k ⭐)**: Industry standard, 400+ sites, fast, Docker support. No AI features.
- **Maigret (18k ⭐)**: 3000+ sites, recursive search, profile parsing, HTML/PDF reports. More comprehensive.
- **Blackbird (5k ⭐)**: 600+ sites, FREE AI profiling that generates behavioral analysis. Best for attribution.

**Reflection 1**: For investigation, I want comprehensive coverage AND AI profiling. Maigret for breadth, then Blackbird for AI analysis on confirmed accounts.

**Thought 2**: Once I have accounts, I need to extract email addresses and check breaches. Moving to Tier 5.

**Action 2**: Evaluate Holehe for email-to-accounts and h8mail for breach hunting.

**Observation 2**:
- **Holehe**: Uses password recovery to silently check 120+ sites. Won't alert target.
- **h8mail**: Searches breach databases for exposed credentials.
- **HIBP API**: Standard for breach notification.

**Reflection 2**: Chain: Username → Maigret → Extract emails → Holehe → h8mail/HIBP.

---

**Final Deliverable**:

### 1. Tool Evaluation Matrix
| Tool | Use Case Fit | Reliability | Integration | Recommendation |
|------|--------------|-------------|-------------|----------------|
| Maigret | High | Active | CLI, Reports | **Primary** |
| Sherlock | High | Active | CLI, Docker | Backup |
| Blackbird | High | Active | CLI, AI | **Primary (AI)** |
| Holehe | High | Active | CLI, Maltego | **Primary** |
| h8mail | High | Active | CLI | **Primary** |

### 2. Recommended Tool Stack
=======
## Research Question

What is the minimal effective structure for prompt documents, and what scoring systems are used to rate prompt quality?

## Context

Project: tafreeman/prompts - A prompt library with 145+ prompts
Problem: Current prompts may have unnecessary sections/fields
Goal: 1) Simplify to essential content only, 2) Implement prompt scoring
```text

---

## Example Usage: Content Expansion

### Input
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18

```text
Username Investigation Workflow:

<<<<<<< HEAD
1. Maigret → Comprehensive username search (3000+ sites, PDF report)
2. Blackbird → AI profiling on confirmed accounts
3. Holehe → Email discovery from found profiles
4. h8mail + HIBP → Breach check on discovered emails
5. SpiderFoot → Automated correlation of all findings
```

### 3. Limitations & Mitigations

- **Risk**: Social media API changes break Osintgram/Toutatis
  - **Mitigation**: Use Instaloader (more robust) or Picuki (passive web)
- **Risk**: Rate limiting on username searches
  - **Mitigation**: Use Maigret's built-in delays, run via TOR

### 4. Maintenance Checklist

- [ ] Check Maigret GitHub for sites.json updates
- [ ] Verify Holehe against test email before operation
- [ ] Update breach databases in h8mail
=======
What are best practices for structuring creative writing and content generation prompts that serve multiple skill levels?

## Context

Project: tafreeman/prompts - A prompt library for AI-assisted work
Current State: 145 prompts total, only 2 in creative category
Goal: Expand creative prompts to 15-20, covering writing, marketing, editing, storytelling
Target Users: Business professionals, marketing teams, content creators
```text

---

## Tips

- **Start with the most specialized source** for your topic (Copy.ai for creative, Stripe for API docs)
- **Look for contributing guides** - they often explain the content model
- **Note the differences** - where sources disagree may indicate context-dependent choices
- **Focus on actionable patterns** - skip things that don't apply to your project
- **Cite everything** - recommendations are stronger with multiple sources
- **Favor simplicity** - if top sources don't use a feature, question whether you need it
- **Research scoring early** - understand how to measure prompt quality before creating more

---

## Current Repository Context

For reference when researching, our library currently has:

| Category | Count | Target | Status | Expansion Ideas |
|----------|-------|--------|--------|------------------|
| Creative | 2 | 15-20 | 🔴 Critical | Writing, marketing, editing, storytelling |
| Business | 26 | 35-40 | 🟡 Expand | Sales, HR, exec comms, operations |
| Developers | 15+ | 25+ | 🟡 Expand | Testing, DevOps, architecture, debugging |
| Analysis | 10+ | 15+ | 🟡 Expand | Data viz, reporting, competitive analysis |
| Advanced | 20+ | 25+ | 🟢 Good | Multi-agent, RAG patterns, fine-tuning |
| Governance | 5+ | 10+ | 🟡 Expand | Compliance, risk, audit, policy |
| M365 | 10+ | 20+ | 🟡 Expand | Teams, SharePoint, Power Platform |
| System | 5+ | 10+ | 🟡 Expand | Agent configs, personas, guardrails |

**Expansion Priorities (All Sections):**

| Priority | Section | Current → Target | Focus Areas |
|----------|---------|------------------|-------------|
| P0 | Creative | 2 → 15-20 | Writing, marketing, editing, storytelling |
| P0 | Business | 26 → 35-40 | Sales, HR, executive comms, operations |
| P1 | M365 | 10+ → 20+ | Teams, SharePoint, Power Platform, Outlook |
| P1 | Developers | 15+ → 25+ | Testing, DevOps, architecture, code review |
| P1 | Governance | 5+ → 10+ | Compliance, risk assessment, audit, policy |
| P2 | Analysis | 10+ → 15+ | Data viz, reporting, competitive intel |
| P2 | Advanced | 20+ → 25+ | Multi-agent, RAG, fine-tuning guides |
| P2 | System | 5+ → 10+ | Agent personas, guardrails, configurations |

**Simplification Targets:**

- Reduce average prompt length by 30-40%
- Remove redundant sections across all prompts
- Standardize to minimal effective structure

**Scoring Implementation:**

- Add `effectivenessScore` field to frontmatter
- Create automated scoring via `tools/validators/`
- Implement review workflow with scoring criteria

---

## Related Prompts

- [ReAct: Repository Analysis](prompt-library-refactor-react.md) - Analyze repository structure
- [ReAct: Tool-Augmented](react-tool-augmented.md) - General ReAct pattern with tools
- [Chain-of-Thought Debugging](chain-of-thought-debugging.md) - Step-by-step reasoning
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18
