# OSINT & SOCMINT Research Resource Library

Generated on: 2025-11-30  
Updated: 2025-11-30

---

## 1. Primary Knowledge Bases (The "Meta" Lists)

These repositories are the "gold standard" starting points. They contain thousands of tools, categorized by function.

| Name | Focus | URL | Description | Stars | Last Verified |
|------|-------|-----|-------------|-------|---------------|
| **Awesome OSINT** | General | `github.com/jivoi/awesome-osint` | The most comprehensive list of OSINT tools, categorized by source (Social Media, Domain, Email, Threat Intel, etc.). 200+ contributors. | 23.7k | 2025-11-30 |
| **Social-Media-OSINT-Tools-Collection** | SOCMINT | `github.com/osintambition/Social-Media-OSINT-Tools-Collection` | Focused specifically on Social Media Intelligence tools covering 17+ platforms (Facebook, Twitter, Instagram, Telegram, Discord, TikTok, etc.). | 1.5k | 2025-11-30 |
| **Awesome Intelligence** | Threat Intel | `github.com/ARPSyndicate/awesome-intelligence` | Broader intelligence resources including GEOINT, HUMINT, and CTI. | - | 2025-11-30 |
| **OSINT Framework** | Taxonomy | `osintframework.com` | Visual taxonomy of tools. Excellent for understanding the *workflow* of an investigation. | - | 2025-11-30 |

## 2. Username Enumeration & Account Search Tools

Tools for hunting usernames across multiple platforms.

| Name | Type | URL | Description | Stars | Status |
|------|------|-----|-------------|-------|--------|
| **Sherlock** | Python CLI | `github.com/sherlock-project/sherlock` | The industry standard for username enumeration. Searches 400+ sites. Docker, pip, and Apify actor support. | 70.6k | **Active** |
| **Maigret** | Python CLI | `github.com/soxoj/maigret` | Advanced fork of Sherlock with 3000+ sites, recursive search, profile parsing, HTML/PDF/XMind reports. Has Telegram bot. | 18k | **Active** |
| **Blackbird** | Python CLI | `github.com/p1ngul1n0/blackbird` | Username/email search with **free AI-powered profiling**. 600+ platforms via WhatsMyName integration. PDF export. | 5k | **Active** |
| **WhatsMyName** | Data/Web | `github.com/WebBreacher/WhatsMyName` | Username enumeration data project. Powers Blackbird, provides web interface. | - | **Active** |
| **Holehe** | Python CLI | `github.com/megadose/holehe` | Email-to-registered-accounts checker. Uses password recovery to find 120+ sites without alerting target. Maltego transform available. | 9.8k | **Active** |
| **Snoop** | Python CLI | `github.com/snooppr/snoop` | Russian-focused OSINT tool for username search. | - | **Active** |
| **Social Analyzer** | Python/API | `github.com/qeeqbox/social-analyzer` | API, CLI, and Web App for finding profiles across 1000+ social media sites. | - | **Active** |
| **NexFil** | Python CLI | `github.com/thewhiteh4t/nexfil` | Fast username checker across most social network sites. | - | **Active** |

## 3. AI & Prompt Engineering Resources

Resources specifically for developing **LLM-based OSINT agents** and prompts.

| Name | Type | URL | Key Value |
|------|------|-----|-----------|
| **Awesome ChatGPT Prompts** | Prompts | `github.com/f/awesome-chatgpt-prompts` | Contains a "Act as..." section. Search for "Cyber Security Specialist" or "Researcher" for prompt templates. |
| **OSINT-Analyser** | Tool/Agent | `github.com/joestanding/OSINT-Analyser` | **Study this code.** It uses LLMs (GPT) to analyze Telegram data. Good example of an "OSINT Agent". |
| **Robin** | Tool/Agent | `github.com/apurvsinghgautam/robin` | An AI-powered Dark Web OSINT tool. Demonstrates how to wrap LLMs around search queries. |
| **LLM_OSINT** | Proof of Concept | `github.com/sshh12/LLM_OSINT` | A "web agent" concept that uses LLMs to scrape and summarize. Good for understanding the logic flow. |
| **Blackbird AI** | Built-in | `github.com/p1ngul1n0/blackbird` | Free AI engine that analyzes found accounts and returns behavioral/technical profiles. |

## 4. Comprehensive OSINT Automation Frameworks

Full-featured platforms for automated reconnaissance.

| Name | Type | URL | Description | Stars | Status |
|------|------|-----|-------------|-------|--------|
| **SpiderFoot** | Python/Web | `github.com/smicallef/spiderfoot` | 200+ modules, web UI & CLI, TOR integration, correlation engine, dark web search. Targets IPs, domains, emails, usernames, BTC addresses. | 16k | **Active** |
| **theHarvester** | Python CLI | `github.com/laramies/theHarvester` | Gathers emails, subdomains, hosts, employee names from 30+ public sources (Shodan, Censys, Hunter, SecurityTrails). | 15.1k | **Active** |
| **Maltego** | Commercial | `maltego.com` | Industry-standard graphical link analysis tool. Transforms for many data sources. |  | **Active** |
| **Recon-ng** | Python CLI | `github.com/lanmaster53/recon-ng` | Full-featured reconnaissance framework with modules similar to Metasploit. | - | **Active** |
| **OSINT.SH** | Web | `osint.sh` | Information Gathering Toolset - web-based aggregator. | - | **Active** |

## 5. Social Media Specific Tools

### Instagram

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Instaloader** | Python | `github.com/instaloader/instaloader` | Robust media/metadata downloader. Good session management. | **Active** |
| **Osintgram** | Python | `github.com/Datalux/Osintgram` | Interactive shell for IG analysis (followers, emails, phones, locations). | ⚠️ **May Break** |
| **Toutatis** | Python | `github.com/megadose/toutatis` | Extract info from phone numbers/emails on Instagram. | **Active** |
| **Picuki** | Web | `picuki.com` | Browse IG content without login (passive recon). | **Active** |

### Telegram

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Telepathy** | Python | `github.com/proseltd/Telepathy-Community` | Archives Telegram chats, analyzes communication patterns. | **Active** |
| **TeleTracker** | Python | `github.com/tsale/TeleTracker` | Track and gather Telegram channel info. | **Active** |
| **CCTV** | Python | `github.com/IvanGlinkin/CCTV` | Telegram location tracking via API. 50-100m precision. | **Active** |
| **Telegram-osint-lib** | Python | `github.com/Postuf/telegram-osint-lib` | Python library for Telegram OSINT. | **Active** |
| **TOsint** | Python | `github.com/drego85/tosint` | Extract info from Telegram bots and channels. | **Active** |

### Twitter/X

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Twint** | Python | (Archived) | Previously powerful Twitter scraper. | ⚠️ **Archived** |
| **Tinfoleak** | Web | `tinfoleak.com` | Twitter user leaks search. | **Active** |
| **ExportData** | Commercial | `exportdata.io` | Historical tweets, followers export. | **Active** |

### Discord

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **DiscordOSINT** | Resources | `github.com/husseinmuhaisen/DiscordOSINT` | OSINT techniques and search syntax for Discord. | **Active** |
| **Discord History Tracker** | Extension | `dht.chylex.com` | Save and view Discord chat history offline. | **Active** |

### LinkedIn

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **LinkedInDumper** | Python | `github.com/l4rm4nd/LinkedInDumper` | Extract company employee info via LinkedIn API. | **Active** |
| **CrossLinked** | Python | `github.com/m8sec/CrossLinked` | LinkedIn enumeration via search engine scraping. | **Active** |
| **InSpy** | Python | `github.com/jobroche/InSpy` | Python-based LinkedIn enumeration. | **Active** |

## 6. Email Intelligence Tools

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Holehe** | Python | `github.com/megadose/holehe` | Check if email is used on 120+ sites via password recovery. | **Active** |
| **GHunt** | Python | `github.com/mxrch/GHunt` | Investigate Google accounts (emails, documents). | **Active** |
| **h8mail** | Python | `github.com/khast3x/h8mail` | Email OSINT & password breach hunting. | **Active** |
| **Hunter.io** | Web/API | `hunter.io` | Find professional email addresses. | **Active** |
| **Epieos** | Web | `epieos.com` | Email-to-social accounts finder. | **Active** |

## 7. Phone Number Research

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **PhoneInfoga** | Python | `github.com/sundowndev/PhoneInfoga` | Advanced phone number OSINT framework. | **Active** |
| **Truecaller** | Web/App | `truecaller.com` | Global reverse phone lookup. | **Active** |

## 8. Domain & IP Research Tools

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Shodan** | Web/API | `shodan.io` | Search engine for Internet-connected devices. | **Active** |
| **Censys** | Web/API | `censys.io` | Internet-wide scanning data. | **Active** |
| **FOFA** | Web/API | `en.fofa.info` | Chinese alternative to Shodan. | **Active** |
| **ZoomEye** | Web/API | `zoomeye.ai` | Cyberspace search engine. | **Active** |
| **GreyNoise** | Web/API | `viz.greynoise.io` | Internet scanner identification. | **Active** |
| **DNSDumpster** | Web | `dnsdumpster.com` | DNS recon & research. | **Active** |
| **SecurityTrails** | Web/API | `securitytrails.com` | Historical DNS and WHOIS data. | **Active** |
| **crt.sh** | Web | `crt.sh` | Certificate Transparency log search. | **Active** |

## 9. Threat Intelligence & Dark Web

| Name | Type | URL | Description | Status |
|------|------|-----|-------------|--------|
| **Have I Been Pwned** | Web/API | `haveibeenpwned.com` | Data breach search. | **Active** |
| **IntelligenceX** | Web/API | `intelx.io` | Dark web, paste sites, data breach search. | **Active** |
| **DeHashed** | Web/API | `dehashed.com` | Breach database search. | **Active** |
| **Ahmia** | Web | `ahmia.fi` | Tor hidden service search. | **Active** |
| **OnionScan** | Python | `github.com/s-rah/onionscan` | Dark Web investigation tool. | **Active** |
| **DarkSearch** | Web/API | `darksearch.io` | Free dark web search engine. | **Active** |
| **Torch** | Web | `xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion` | .onion search engine. | **Active** |

## 10. Core Automation Scripts (For Workflow Study)

Study these repositories to understand how to build **robust OSINT workflows** in Python.

| Name | Target | URL | Status | Notes |
|------|--------|-----|--------|-------|
| **Sherlock** | Usernames | `github.com/sherlock-project/sherlock` | **Active** | The standard for username enumeration. Study its `sites.json` to see how it maps 400+ sites. |
| **Instaloader** | Instagram | `github.com/instaloader/instaloader` | **Active** | Robust Python library for IG. Good example of handling session management and rate limits. |
| **Maigret** | Usernames | `github.com/soxoj/maigret` | **Active** | Fork of Sherlock with better reporting (PDF/HTML). Good for learning report generation. |
| **socid_extractor** | Multiple | `github.com/soxoj/socid_extractor` | **Active** | Extract user IDs from profile pages. Powers Maigret's recursive search. |
| **Osintgram** | Instagram | `github.com/Datalux/Osintgram` | **CAUTION** | ⚠️ May break due to API changes. Use only for code study (historical). |
| **theHarvester** | Domains/Emails | `github.com/laramies/theHarvester` | **Active** | Excellent example of multi-source data gathering with 30+ modules. |
| **SpiderFoot** | Multi-target | `github.com/smicallef/spiderfoot` | **Active** | Study its module architecture for building extensible OSINT tools. |

## 11. Methodology & Best Practices

Guides on *how* to structure your investigations and prompts.

- **The Intelligence Cycle**:
    1. **Planning**: Define the question (e.g., "Who owns this domain?").
    2. **Collection**: Gather raw data (Passive Recon).
    3. **Processing**: Filter noise (Normalization).
    4. **Analysis**: Connect dots (Correlation).
    5. **Dissemination**: Report findings.
  - *Tip: Structure your LLM prompts to follow these exact 5 steps for better results.*

- **Bellingcat Guides**: (`bellingcat.com/resources`)
  - The industry standard for verification and geolocation methodology. Use their case studies to build "Few-Shot" examples for your prompts.

- **Trace Labs OSINT VM**: (`tracelabs.org`)
  - Pre-configured VM with OSINT tools for ethical missing persons investigations. Good for learning workflows.

- **OSINT Techniques**: (`osinttechniques.com`)
  - Michael Bazzell's comprehensive OSINT guide. Covers Privacy, Sock Puppets, and more.

## 12. Gaps & Limitations

- **Social Media APIs**: Tools like `Osintgram` break constantly because platforms (Instagram/Twitter/LinkedIn) aggressively fight scrapers.
  - *Dev Tip*: When building new tools, rely on **browser automation** (Selenium/Playwright) rather than private APIs if possible, or use official paid APIs.
- **LLM Hallucinations**: AI agents often "invent" tools or findings.
  - *Prompt Tip*: Always include a "Verification Step" in your prompt instructions (e.g., "Check if the URL returns 200 OK before listing it").
- **Rate Limiting**: Most platforms implement aggressive rate limiting.
  - *Dev Tip*: Implement exponential backoff, use proxy rotation, and respect `robots.txt` for ethical OSINT.
- **Data Freshness**: OSINT data changes rapidly. Verify timestamps and cross-reference multiple sources.

---

## Quick Reference: Tool Selection by Use Case

| Use Case | Recommended Tools |
|----------|-------------------|
| **Username across all platforms** | Sherlock → Maigret → Blackbird |
| **Email to accounts** | Holehe → Epieos → GHunt |
| **Phone number lookup** | PhoneInfoga → Truecaller |
| **Domain/IP recon** | theHarvester → SpiderFoot → Shodan |
| **Instagram deep-dive** | Instaloader → Osintgram → Picuki |
| **Telegram monitoring** | Telepathy → TeleTracker |
| **Data breach check** | HIBP → IntelligenceX → DeHashed |
| **Full automation** | SpiderFoot (web UI) → Maltego |
