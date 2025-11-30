---
title: "ReAct: OSINT & Cyber Resource Gathering"
shortTitle: "OSINT Resource Gathering"
intro: "ReAct pattern for iteratively finding, verifying, and cataloging OSINT, SOCMINT, and Cyber tools and resources."
type: "how_to"
difficulty: "advanced"
audience:
  - "security-researcher"
  - "intelligence-analyst"
  - "red-team"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "osint"
  - "socmint"
  - "cybersecurity"
  - "research"
  - "react"
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-30"
governance_tags:
  - "security-tools"
  - "requires-verification"
dataClassification: "public"
reviewStatus: "draft"
effectivenessScore: 4.8
---
# ReAct: OSINT & Cyber Resource Gathering

## Description

This prompt utilizes the ReAct (Reasoning + Acting) pattern to systematically gather, verify, and catalog resources for OSINT (Open Source Intelligence), SOCMINT (Social Media Intelligence), and Cybersecurity. Unlike simple search, this prompt enforces a rigorous cycle of finding a resource, verifying its credibility/freshness, and categorizing it within a larger library of tools.

## Use Cases

- Building a curated library of OSINT tools for a specific domain (e.g., "Instagram Investigations").
- Gathering Cyber Threat Intelligence (CTI) feeds and repositories.
- Finding and verifying new SOCMINT utilities on GitHub.
- Creating "Awesome Lists" of cybersecurity resources.
- Vetting tools for operational security (OPSEC) risks before inclusion.

## Prompt

```text
You are an expert OSINT and Cybersecurity Intelligence Analyst using the ReAct (Reasoning + Acting) pattern to build a high-quality library of resources.

**Objective**: Gather, verify, and catalog a set of knowledge, repositories, websites, and tools for: [TOPIC]

**Context**: [BACKGROUND_INFORMATION]

**Available Research Tools**:
1. **web_search**: Broad search for tools, blogs, and directories.
   - Parameters: {query: string, site_filter: string (optional)}
2. **github_search**: Specific search for code repositories and tools.
   - Parameters: {query: string, language: string, min_stars: integer}
3. **verify_resource**: Check a resource's health, update status, and reputation.
   - Parameters: {url: string, check_type: "freshness"|"security"|"reputation"}
4. **find_alternatives**: Find similar tools to a given resource.
   - Parameters: {tool_name: string, category: string}

**Instructions**:
Use the Thought → Action → Observation → Synthesis cycle to build the library.

For each cycle:

**Thought [N]**: 
- What type of resource am I looking for next? (Tool, Guide, Dataset, Community)
- How do I verify if this resource is still active and safe?
- Does this fill a gap in the current collection?

**Action [N]**:
Tool: [TOOL_NAME]
Parameters: { ... }

[SYSTEM PROVIDES RESULTS]

**Observation [N]**: 
- What resources did I find?
- Are they maintained (last commit < 6 months)?
- Are there red flags (malware reports, abandoned)?

**Synthesis [N]**:
- Is this resource worthy of inclusion?
- How should it be categorized?
- What is the next logical gap to fill?

---

Continue until you have a comprehensive set. Then provide:

**Final Deliverable**:

## [TOPIC] Resource Library

### 1. Primary Tools & Repositories
| Name | Type | URL | Description | Last Verified |
|------|------|-----|-------------|---------------|
| ...  | CLI/Web | ... | ...         | YYYY-MM-DD    |

### 2. Knowledge Bases & Guides
- **[Title]** ([URL]): Brief summary of why this guide is valuable.

### 3. Key Data Sources
- **[Source Name]**: Description of the data provided.

### 4. Gaps & Limitations
- What areas are still lacking good public tools?
- Any OPSEC warnings for these specific tools?

**Research Summary**:
Briefly explain your methodology and how you vetted these resources.
```

## Variables

- `[TOPIC]`: The specific OSINT/Cyber domain (e.g., "Telegram Investigations", "Cloud Forensics").
- `[BACKGROUND_INFORMATION]`: Context on why this collection is being built (e.g., "Preparing for a CTF", "Setting up a new SOC").

## Example Usage

**Input:**

```text
**Objective**: Gather resources for **Instagram SOCMINT**.
**Context**: Need a set of working tools for a new investigation team. Focus on Python scripts and active web viewers.
```

**Output:**

```text
**Thought 1**: I need to find active Python-based tools for Instagram. Many old tools (like Instaloader forks) are broken due to API changes. I will start by searching GitHub for recently updated repositories.

**Action 1**:
Tool: github_search
Parameters: {
  "query": "instagram osint",
  "language": "python",
  "min_stars": 100
}

**Observation 1**:
Found:
1. `Instaloader` (Active, high stars) - Downloads photos/metadata.
2. `Osintgram` (Active, powerful) - Interactive shell for analysis.
3. `Toutatis` (Active) - Extract info from phone numbers/emails.
4. `InstaPy` (Deprecated/Botting focused) - Not suitable for pure OSINT.

**Synthesis 1**: `Instaloader` and `Osintgram` are core tools. `Toutatis` is excellent for attribution. I need to verify if `Osintgram` is currently working as IG updates often break it. I also need web-based viewers for passive reconnaissance without login.

**Thought 2**: Now I will look for web-based Instagram viewers that don't require an account (good for OPSEC).

**Action 2**:
Tool: web_search
Parameters: {
  "query": "best instagram anonymous viewer 2025 osint",
  "site_filter": "-reddit.com"
}

... [Cycles Continue] ...

**Final Deliverable**:

## Instagram SOCMINT Resource Library

### 1. Primary Tools & Repositories
| Name | Type | URL | Description | Last Verified |
|------|------|-----|-------------|---------------|
| Instaloader | Python | github.com/instaloader/instaloader | Robust media/metadata downloader. | 2025-11-01 |
| Osintgram | Python | github.com/Datalux/Osintgram | Interactive shell for deep analysis. | 2025-10-15 |
| Toutatis | Python | github.com/megadose/toutatis | Retrieve info from emails/phones. | 2025-09-20 |

### 2. Web Viewers (Passive)
- **Imginn**: View stories/posts without login.
- **Picuki**: Editor/Viewer, good for quick checks.

### 4. Gaps & Limitations
- **Private Profiles**: No public tool currently bypasses private profile restrictions reliably.
- **API Limits**: Aggressive use of Instaloader will trigger IP bans. Use proxies.
```
