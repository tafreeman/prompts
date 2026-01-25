---
name: react-knowledge-base-research
description: 'AUTO-GENERATED: ReAct OSINT/SOCMINT knowledge-base research prompt. Please refine.'
type: how_to
difficulty: advanced
author: Prompt Library Team
date: '2025-11-30'
---
## Description

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
| -------- | ----- | ------- | ------- |
| **Awesome OSINT** | `github.com/jivoi/awesome-osint` | Comprehensive OSINT taxonomy (200+ contributors) | 23.7k |
| **Social-Media-OSINT-Tools-Collection** | `github.com/osintambition/Social-Media-OSINT-Tools-Collection` | SOCMINT for 17+ platforms | 1.5k |
| **OSINT Framework** | `osintframework.com` | Visual tool taxonomy | - |

### Tier 2: Username & Account Enumeration
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **Sherlock** | `github.com/sherlock-project/sherlock` | 400+ sites, industry standard | 70.6k |
| **Maigret** | `github.com/soxoj/maigret` | 3000+ sites, recursive search, reporting | 18k |
| **Blackbird** | `github.com/p1ngul1n0/blackbird` | AI profiling, 600+ platforms | 5k |
| **Holehe** | `github.com/megadose/holehe` | Email-to-accounts (120+ sites) | 9.8k |
| **WhatsMyName** | `github.com/WebBreacher/WhatsMyName` | Username enumeration data | - |

### Tier 3: OSINT Automation Frameworks
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **SpiderFoot** | `github.com/smicallef/spiderfoot` | 200+ modules, web UI, TOR, correlation | 16k |
| **theHarvester** | `github.com/laramies/theHarvester` | Email/subdomain harvesting, 30+ sources | 15.1k |
| **Recon-ng** | `github.com/lanmaster53/recon-ng` | Metasploit-style recon framework | - |
| **Maltego** | `maltego.com` | Graphical link analysis (commercial) | - |

### Tier 4: Social Media Specific Tools
#### Instagram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Instaloader** | `github.com/instaloader/instaloader` | **Active** - Media/metadata download |
| **Osintgram** | `github.com/Datalux/Osintgram` | ⚠️ May break - Interactive IG shell |
| **Toutatis** | `github.com/megadose/toutatis` | **Active** - Phone/email extraction |

#### Telegram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Telepathy** | `github.com/proseltd/Telepathy-Community` | **Active** - Chat archival |
| **TeleTracker** | `github.com/tsale/TeleTracker` | **Active** - Channel tracking |
| **CCTV** | `github.com/IvanGlinkin/CCTV` | **Active** - Location tracking |

#### LinkedIn
| Tool | URL | Status |
| ------ | ----- | -------- |
| **LinkedInDumper** | `github.com/l4rm4nd/LinkedInDumper` | **Active** - Employee extraction |
| **CrossLinked** | `github.com/m8sec/CrossLinked` | **Active** - Search engine scraping |

### Tier 5: Email & Phone Intelligence
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **GHunt** | `github.com/mxrch/GHunt` | Google account investigation |
| **h8mail** | `github.com/khast3x/h8mail` | Email breach hunting |
| **PhoneInfoga** | `github.com/sundowndev/PhoneInfoga` | Phone number OSINT |
| **Hunter.io** | `hunter.io` | Professional email discovery |

### Tier 6: Domain, IP & Infrastructure
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Shodan** | `shodan.io` | Internet-connected device search |
| **Censys** | `censys.io` | Internet-wide scanning data |
| **SecurityTrails** | `securitytrails.com` | Historical DNS/WHOIS |
| **crt.sh** | `crt.sh` | Certificate Transparency logs |
| **DNSDumpster** | `dnsdumpster.com` | DNS reconnaissance |

### Tier 7: Threat Intelligence & Dark Web
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Have I Been Pwned** | `haveibeenpwned.com` | Data breach search |
| **IntelligenceX** | `intelx.io` | Dark web, paste sites, breaches |
| **DeHashed** | `dehashed.com` | Breach database search |
| **Ahmia** | `ahmia.fi` | Tor hidden service search |

### Tier 8: AI-Powered OSINT
| Tool | URL | Capability |
| ------ | ----- | ------------ |
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
| ------ | -------------- | ------------- | ------------- | ---------------- |
| ... | High/Med/Low | Active/Risky | CLI/API/Web | Primary/Backup/Skip |

### 2. Recommended Tool Stack

```

AUTO-GENERATED: Short description of this prompt. Please refine.

## Description

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
| -------- | ----- | ------- | ------- |
| **Awesome OSINT** | `github.com/jivoi/awesome-osint` | Comprehensive OSINT taxonomy (200+ contributors) | 23.7k |
| **Social-Media-OSINT-Tools-Collection** | `github.com/osintambition/Social-Media-OSINT-Tools-Collection` | SOCMINT for 17+ platforms | 1.5k |
| **OSINT Framework** | `osintframework.com` | Visual tool taxonomy | - |

### Tier 2: Username & Account Enumeration
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **Sherlock** | `github.com/sherlock-project/sherlock` | 400+ sites, industry standard | 70.6k |
| **Maigret** | `github.com/soxoj/maigret` | 3000+ sites, recursive search, reporting | 18k |
| **Blackbird** | `github.com/p1ngul1n0/blackbird` | AI profiling, 600+ platforms | 5k |
| **Holehe** | `github.com/megadose/holehe` | Email-to-accounts (120+ sites) | 9.8k |
| **WhatsMyName** | `github.com/WebBreacher/WhatsMyName` | Username enumeration data | - |

### Tier 3: OSINT Automation Frameworks
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **SpiderFoot** | `github.com/smicallef/spiderfoot` | 200+ modules, web UI, TOR, correlation | 16k |
| **theHarvester** | `github.com/laramies/theHarvester` | Email/subdomain harvesting, 30+ sources | 15.1k |
| **Recon-ng** | `github.com/lanmaster53/recon-ng` | Metasploit-style recon framework | - |
| **Maltego** | `maltego.com` | Graphical link analysis (commercial) | - |

### Tier 4: Social Media Specific Tools
#### Instagram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Instaloader** | `github.com/instaloader/instaloader` | **Active** - Media/metadata download |
| **Osintgram** | `github.com/Datalux/Osintgram` | ⚠️ May break - Interactive IG shell |
| **Toutatis** | `github.com/megadose/toutatis` | **Active** - Phone/email extraction |

#### Telegram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Telepathy** | `github.com/proseltd/Telepathy-Community` | **Active** - Chat archival |
| **TeleTracker** | `github.com/tsale/TeleTracker` | **Active** - Channel tracking |
| **CCTV** | `github.com/IvanGlinkin/CCTV` | **Active** - Location tracking |

#### LinkedIn
| Tool | URL | Status |
| ------ | ----- | -------- |
| **LinkedInDumper** | `github.com/l4rm4nd/LinkedInDumper` | **Active** - Employee extraction |
| **CrossLinked** | `github.com/m8sec/CrossLinked` | **Active** - Search engine scraping |

### Tier 5: Email & Phone Intelligence
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **GHunt** | `github.com/mxrch/GHunt` | Google account investigation |
| **h8mail** | `github.com/khast3x/h8mail` | Email breach hunting |
| **PhoneInfoga** | `github.com/sundowndev/PhoneInfoga` | Phone number OSINT |
| **Hunter.io** | `hunter.io` | Professional email discovery |

### Tier 6: Domain, IP & Infrastructure
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Shodan** | `shodan.io` | Internet-connected device search |
| **Censys** | `censys.io` | Internet-wide scanning data |
| **SecurityTrails** | `securitytrails.com` | Historical DNS/WHOIS |
| **crt.sh** | `crt.sh` | Certificate Transparency logs |
| **DNSDumpster** | `dnsdumpster.com` | DNS reconnaissance |

### Tier 7: Threat Intelligence & Dark Web
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Have I Been Pwned** | `haveibeenpwned.com` | Data breach search |
| **IntelligenceX** | `intelx.io` | Dark web, paste sites, breaches |
| **DeHashed** | `dehashed.com` | Breach database search |
| **Ahmia** | `ahmia.fi` | Tor hidden service search |

### Tier 8: AI-Powered OSINT
| Tool | URL | Capability |
| ------ | ----- | ------------ |
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
| ------ | -------------- | ------------- | ------------- | ---------------- |
| ... | High/Med/Low | Active/Risky | CLI/API/Web | Primary/Backup/Skip |

### 2. Recommended Tool Stack

```

AUTO-GENERATED: Short description of this prompt. Please refine.


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
| -------- | ----- | ------- | ------- |
| **Awesome OSINT** | `github.com/jivoi/awesome-osint` | Comprehensive OSINT taxonomy (200+ contributors) | 23.7k |
| **Social-Media-OSINT-Tools-Collection** | `github.com/osintambition/Social-Media-OSINT-Tools-Collection` | SOCMINT for 17+ platforms | 1.5k |
| **OSINT Framework** | `osintframework.com` | Visual tool taxonomy | - |

### Tier 2: Username & Account Enumeration
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **Sherlock** | `github.com/sherlock-project/sherlock` | 400+ sites, industry standard | 70.6k |
| **Maigret** | `github.com/soxoj/maigret` | 3000+ sites, recursive search, reporting | 18k |
| **Blackbird** | `github.com/p1ngul1n0/blackbird` | AI profiling, 600+ platforms | 5k |
| **Holehe** | `github.com/megadose/holehe` | Email-to-accounts (120+ sites) | 9.8k |
| **WhatsMyName** | `github.com/WebBreacher/WhatsMyName` | Username enumeration data | - |

### Tier 3: OSINT Automation Frameworks
| Tool | URL | Capability | Stars |
| ------ | ----- | ------------ | ------- |
| **SpiderFoot** | `github.com/smicallef/spiderfoot` | 200+ modules, web UI, TOR, correlation | 16k |
| **theHarvester** | `github.com/laramies/theHarvester` | Email/subdomain harvesting, 30+ sources | 15.1k |
| **Recon-ng** | `github.com/lanmaster53/recon-ng` | Metasploit-style recon framework | - |
| **Maltego** | `maltego.com` | Graphical link analysis (commercial) | - |

### Tier 4: Social Media Specific Tools
#### Instagram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Instaloader** | `github.com/instaloader/instaloader` | **Active** - Media/metadata download |
| **Osintgram** | `github.com/Datalux/Osintgram` | ⚠️ May break - Interactive IG shell |
| **Toutatis** | `github.com/megadose/toutatis` | **Active** - Phone/email extraction |

#### Telegram
| Tool | URL | Status |
| ------ | ----- | -------- |
| **Telepathy** | `github.com/proseltd/Telepathy-Community` | **Active** - Chat archival |
| **TeleTracker** | `github.com/tsale/TeleTracker` | **Active** - Channel tracking |
| **CCTV** | `github.com/IvanGlinkin/CCTV` | **Active** - Location tracking |

#### LinkedIn
| Tool | URL | Status |
| ------ | ----- | -------- |
| **LinkedInDumper** | `github.com/l4rm4nd/LinkedInDumper` | **Active** - Employee extraction |
| **CrossLinked** | `github.com/m8sec/CrossLinked` | **Active** - Search engine scraping |

### Tier 5: Email & Phone Intelligence
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **GHunt** | `github.com/mxrch/GHunt` | Google account investigation |
| **h8mail** | `github.com/khast3x/h8mail` | Email breach hunting |
| **PhoneInfoga** | `github.com/sundowndev/PhoneInfoga` | Phone number OSINT |
| **Hunter.io** | `hunter.io` | Professional email discovery |

### Tier 6: Domain, IP & Infrastructure
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Shodan** | `shodan.io` | Internet-connected device search |
| **Censys** | `censys.io` | Internet-wide scanning data |
| **SecurityTrails** | `securitytrails.com` | Historical DNS/WHOIS |
| **crt.sh** | `crt.sh` | Certificate Transparency logs |
| **DNSDumpster** | `dnsdumpster.com` | DNS reconnaissance |

### Tier 7: Threat Intelligence & Dark Web
| Tool | URL | Capability |
| ------ | ----- | ------------ |
| **Have I Been Pwned** | `haveibeenpwned.com` | Data breach search |
| **IntelligenceX** | `intelx.io` | Dark web, paste sites, breaches |
| **DeHashed** | `dehashed.com` | Breach database search |
| **Ahmia** | `ahmia.fi` | Tor hidden service search |

### Tier 8: AI-Powered OSINT
| Tool | URL | Capability |
| ------ | ----- | ------------ |
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
| ------ | -------------- | ------------- | ------------- | ---------------- |
| ... | High/Med/Low | Active/Risky | CLI/API/Web | Primary/Backup/Skip |

### 2. Recommended Tool Stack

```text

[USE_CASE] Workflow:


1. [Tool A] → Initial discovery
2. [Tool B] → Deep dive
3. [Tool C] → Reporting/Export

```

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
| ---------- | ------------------- |
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
| ------ | -------------- | ------------- | ------------- | ---------------- |
| Maigret | High | Active | CLI, Reports | **Primary** |
| Sherlock | High | Active | CLI, Docker | Backup |
| Blackbird | High | Active | CLI, AI | **Primary (AI)** |
| Holehe | High | Active | CLI, Maltego | **Primary** |
| h8mail | High | Active | CLI | **Primary** |

### 2. Recommended Tool Stack

```text

Username Investigation Workflow:


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
- [ ] Update breach databases in h8mail## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[N]` | AUTO-GENERATED: describe `N` |
| `[USE_CASE]` | AUTO-GENERATED: describe `USE_CASE` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[N]` | AUTO-GENERATED: describe `N` |
| `[Platform API changes]` | AUTO-GENERATED: describe `Platform API changes` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Tool A]` | AUTO-GENERATED: describe `Tool A` |
| `[Tool B]` | AUTO-GENERATED: describe `Tool B` |
| `[Tool C]` | AUTO-GENERATED: describe `Tool C` |
| `[USE_CASE]` | AUTO-GENERATED: describe `USE_CASE` |
| `[Use browser automation fallback]` | AUTO-GENERATED: describe `Use browser automation fallback` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

