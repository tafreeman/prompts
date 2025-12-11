# OSINT/SOCMINT Tool Evaluation Report

**Generated**: November 30, 2025  
**Methodology**: ReAct (Reasoning + Acting) Pattern  
**Source**: Curated industry resources from `osint_research_resources.md`

---

## Executive Summary

This report evaluates the best OSINT, SOCMINT, and Cyber Intelligence tools available based on systematic research of verified industry resources. All tools were verified for active maintenance status, feature completeness, and reliability.

---

## 1. Tool Evaluation Matrix

| Tool | Category | Stars | Latest Release | Reliability | Best For | Recommendation |
|------|----------|-------|----------------|-------------|----------|----------------|
| **Sherlock** | Username | 70.6k | v0.16.0 (Sep 2024) | ✅ Active | Fast username search, 400+ sites | **Primary** |
| **Maigret** | Username | 18k | Dec 2024 | ✅ Active | Comprehensive search (3000+ sites), PDF reports | **Primary** |
| **Blackbird** | Username/Email | 5k | Active | ✅ Active | AI-powered profiling (FREE), 600+ sites | **Primary (AI)** |
| **Holehe** | Email | 9.8k | Active | ✅ Active | Silent email-to-accounts (120+ sites) | **Primary** |
| **SpiderFoot** | Framework | 16k | v4.0 (Apr 2022) | ✅ Active | Full automation, 200+ modules, web UI | **Primary** |
| **theHarvester** | Domain/Email | 15.1k | v4.8.2 (Jul 2024) | ✅ Active | Email/subdomain harvesting, 30+ sources | **Primary** |
| **Instaloader** | Instagram | 11.1k | v4.15 (Nov 2024) | ✅ Active | Instagram media/metadata download | **Primary** |
| **GHunt** | Google | 18.2k | v2.2.0 (Jun 2024) | ✅ Active | Google account OSINT | **Primary** |
| **Telepathy** | Telegram | 1.2k | v2.3.4 (2024) | ✅ Active | Telegram chat archival, analysis | **Primary** |
| **PhoneInfoga** | Phone | - | Active | ✅ Active | Phone number OSINT | **Primary** |

---

## 2. Recommended Tool Stacks by Use Case

### Username Investigation Workflow

```text
1. Maigret → Comprehensive search (3000+ sites, PDF report)
2. Sherlock → Verify with industry standard (400+ sites)
3. Blackbird → FREE AI profiling on confirmed accounts
4. Holehe → Email discovery from found profiles
5. GHunt → Google account investigation (if Gmail found)
```

### Email-to-Identity Investigation

```text
1. Holehe → Find accounts linked to email (120+ sites, silent)
2. h8mail → Breach database search
3. HIBP → Data breach verification
4. GHunt → If Gmail, full Google OSINT
```

### Domain/IP Reconnaissance

```text
1. theHarvester → Emails, subdomains from 30+ sources
2. SpiderFoot → Full automation with 200+ modules
3. Shodan → Device/service enumeration
4. crt.sh → Certificate transparency search
```

### Social Media Deep-Dive

```text
Instagram: Instaloader → Osintgram (caution) → Picuki
Telegram:  Telepathy → TeleTracker → CCTV (location)
LinkedIn:  LinkedInDumper → CrossLinked
```

### Full Automation (Enterprise)

```text
1. SpiderFoot (web UI) → Complete target analysis
2. Maltego → Graphical link analysis
3. All findings → JSON export for correlation
```

---

## 3. Detailed Tool Profiles

### Tier 1: Username Enumeration

#### Sherlock (70.6k ⭐)
- **URL**: `github.com/sherlock-project/sherlock`
- **Capability**: 400+ sites, industry standard
- **Install**: `pip install sherlock-project` or Docker
- **Features**: Apify actor support, CSV/XLSX export, TOR support
- **Status**: ✅ Active (279 contributors)

#### Maigret (18k ⭐)
- **URL**: `github.com/soxoj/maigret`
- **Capability**: 3000+ sites, recursive search
- **Install**: `pip install maigret` or Docker
- **Features**: Profile parsing, PDF/HTML/XMind reports, web UI, Telegram bot
- **Status**: ✅ Active (42 contributors)

#### Blackbird (5k ⭐)
- **URL**: `github.com/p1ngul1n0/blackbird`
- **Capability**: 600+ platforms via WhatsMyName
- **Install**: `pip install -r requirements.txt`
- **Features**: **FREE AI profiling**, email search, PDF export
- **Status**: ✅ Active (18 contributors)

### Tier 2: Email Intelligence

#### Holehe (9.8k ⭐)
- **URL**: `github.com/megadose/holehe`
- **Capability**: 120+ sites via password recovery
- **Install**: `pip install holehe`
- **Features**: Silent (doesn't alert target), Maltego transform, async
- **Status**: ✅ Active (25 contributors)

#### GHunt (18.2k ⭐)
- **URL**: `github.com/mxrch/GHunt`
- **Capability**: Google account OSINT
- **Install**: `pipx install ghunt`
- **Features**: Email/Gaia/Drive/Geolocate modules, JSON export, browser extension
- **Status**: ✅ Active (v2.2.0, Jun 2024)

### Tier 3: OSINT Automation Frameworks

#### SpiderFoot (16k ⭐)
- **URL**: `github.com/smicallef/spiderfoot`
- **Capability**: 200+ modules, comprehensive automation
- **Install**: `pip install -r requirements.txt`
- **Features**: 
  - Web UI & CLI
  - TOR integration
  - 37 correlation rules
  - Targets: IPs, domains, emails, usernames, BTC addresses
  - Integrates with: Shodan, HIBP, GreyNoise, SecurityTrails, etc.
- **Status**: ✅ Active (developed since 2012)

#### theHarvester (15.1k ⭐)
- **URL**: `github.com/laramies/theHarvester`
- **Capability**: Email/subdomain harvesting
- **Install**: `uv sync` (Python 3.12+)
- **Features**: 30+ passive modules including Shodan, Censys, Hunter, SecurityTrails
- **Status**: ✅ Active (v4.8.2, Jul 2024)

### Tier 4: Social Media Tools

#### Instaloader (11.1k ⭐)
- **URL**: `github.com/instaloader/instaloader`
- **Capability**: Instagram media/metadata
- **Install**: `pip install instaloader`
- **Features**: Public/private profiles, comments, geotags, auto-rename, resume
- **Status**: ✅ Active (v4.15, Nov 2024, 143 releases)

#### Telepathy (1.2k ⭐)
- **URL**: `github.com/proseltd/Telepathy-Community`
- **Capability**: Telegram OSINT
- **Install**: `pip install telepathy`
- **Features**: Chat archival, memberlists, location lookup, forwards mapping, translation
- **Status**: ✅ Active (v2.3.4)

---

## 4. Limitations & Mitigations

| Risk | Tools Affected | Mitigation |
|------|---------------|------------|
| **API Rate Limiting** | All username tools | Use built-in delays, proxy rotation, TOR |
| **Social Media API Changes** | Osintgram, Toutatis | Use Instaloader (more robust) or Picuki (passive) |
| **False Positives** | Username enumeration | Cross-verify with multiple tools, check profile content |
| **Account Blocking** | Instagram, Telegram tools | Use dedicated research accounts, respect platform ToS |
| **Stale Data** | Cached results | Always verify timestamps, cross-reference sources |

---

## 5. Maintenance Checklist

- [ ] **Weekly**: Check Maigret/Sherlock GitHub for sites.json updates
- [ ] **Before Operations**: Verify Holehe against test email
- [ ] **Monthly**: Update all tools to latest versions
- [ ] **Quarterly**: Test tool functionality against known targets
- [ ] **Review**: Check tool GitHub issues for known breakages

---

## 6. Quick Reference Card

| If You Need... | Use This Tool |
|----------------|---------------|
| Username → All platforms | **Maigret** (3000+ sites) |
| Username → Fast check | **Sherlock** (400+ sites) |
| Username → AI analysis | **Blackbird** (free AI) |
| Email → Accounts | **Holehe** (silent, 120+ sites) |
| Email → Breaches | **h8mail** + **HIBP** |
| Email → Google OSINT | **GHunt** |
| Domain → Full recon | **theHarvester** |
| Any target → Full auto | **SpiderFoot** |
| Instagram → Media | **Instaloader** |
| Telegram → Archive | **Telepathy** |
| Phone → OSINT | **PhoneInfoga** |

---

## 7. Installation Quick Start

```bash
# Username Enumeration
pip install sherlock-project
pip install maigret
git clone https://github.com/p1ngul1n0/blackbird && pip install -r requirements.txt

# Email Intelligence
pip install holehe
pipx install ghunt

# Frameworks
git clone https://github.com/smicallef/spiderfoot && pip install -r requirements.txt
git clone https://github.com/laramies/theHarvester && uv sync

# Social Media
pip install instaloader
pip install telepathy
```

---

## 8. Tool Selection Flowchart

```
START: What do you have?
│
├─► Username
│   ├─► Need comprehensive coverage? → Maigret (3000+ sites)
│   ├─► Need speed? → Sherlock (400+ sites)
│   └─► Need AI analysis? → Blackbird (free AI profiling)
│
├─► Email Address
│   ├─► Find linked accounts? → Holehe (silent, 120+ sites)
│   ├─► Check breaches? → h8mail + HIBP
│   └─► Gmail specifically? → GHunt
│
├─► Domain/IP
│   ├─► Quick recon? → theHarvester (30+ sources)
│   └─► Full automation? → SpiderFoot (200+ modules)
│
├─► Social Media
│   ├─► Instagram? → Instaloader
│   ├─► Telegram? → Telepathy
│   └─► LinkedIn? → LinkedInDumper / CrossLinked
│
└─► Phone Number → PhoneInfoga
```

---

## References

- [Awesome OSINT](https://github.com/jivoi/awesome-osint) - 23.7k ⭐
- [Social-Media-OSINT-Tools-Collection](https://github.com/osintambition/Social-Media-OSINT-Tools-Collection) - 1.5k ⭐
- [OSINT Framework](https://osintframework.com) - Visual taxonomy

---

*Report generated using ReAct methodology from `react-knowledge-base-research.md`*
