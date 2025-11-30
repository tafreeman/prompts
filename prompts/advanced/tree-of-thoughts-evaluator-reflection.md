---
title: "ToT Evaluator: OSINT Resource Assessment"
shortTitle: "OSINT Resource Evaluator"
intro: "A rigorous Tree-of-Thoughts evaluation pattern for assessing the safety, quality, and operational utility of OSINT and Cyber resources."
type: "how_to"
difficulty: "advanced"
audience:
  - "security-engineer"
  - "soc-manager"
  - "compliance-officer"
platforms:
  - "chatgpt"
  - "claude"
topics:
  - "evaluation"
  - "osint"
  - "supply-chain-security"
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-30"
governance_tags:
  - "risk-assessment"
  - "supply-chain"
dataClassification: "internal"
reviewStatus: "draft"
---
## Description

This prompt applies the **Tree-of-Thoughts (ToT)** reasoning framework to evaluate OSINT tools, repositories, and datasets. It is designed to prevent the inclusion of malicious, abandoned, or legally risky tools in your intelligence library. Phase 1 performs a deep technical and functional assessment, while Phase 2 reflects on safety, ethics, and long-term viability.

## Goal

To produce a **Decision-Grade Verdict** on whether a specific OSINT resource should be adopted by an enterprise or investigation team.

## Context

- **Target**: A GitHub repo, software tool, or data service identified for potential use.
- **Risks**: Malware in scripts, abandoned code, violation of Terms of Service (ToS), poor OPSEC.

## Process / Reasoning Style

1. **Phase 1 – Tree-of-Thoughts Evaluation**
   - **Branch A (Functionality)**: Does it work? Is it unique?
   - **Branch B (Security/Safety)**: Is the code safe? Who maintains it? Any obfuscated code?
   - **Branch C (Viability)**: Is it actively maintained? Is the community healthy?

2. **Phase 2 – Reflection & Self-Critique**
   - **Safety Check**: Did we miss any red flags? (e.g., "install.sh" piping to bash)
   - **Legal/Ethical Check**: Does this tool violate platform ToS (e.g., scraping)?
   - **Verdict Refinement**: Adjust the final score based on these risks.

## Prompt

```text
You are a Senior Security Engineer evaluating a new OSINT resource for inclusion in our secure library. Use a **Two-Phase Tree-of-Thoughts + Reflection** pattern.

**Resource to Evaluate**: [RESOURCE_NAME] ([URL])
**Context/Use Case**: [USE_CASE]

### Phase 1 – Tree-of-Thoughts Evaluation

Explore three reasoning branches to assess the resource:

**Branch A: Functionality & Utility**
- Thoughts: Does this solve a unique problem? Is it better than existing standard tools?
- Evidence: Features, documentation quality, ease of use.

**Branch B: Security & Integrity**
- Thoughts: Is the code visible? Are there binary blobs? Does it require excessive permissions?
- Evidence: Code review (simulated), dependency analysis, author reputation.

**Branch C: Maintenance & Viability**
- Thoughts: When was the last commit? How many open issues? Is the author responsive?
- Evidence: Commit history, issue tracker health.

**Synthesis & Initial Score (0-100)**:
Combine findings into an initial assessment.

### Phase 2 – Reflection & Self-Critique

Critically review your Phase 1 assessment with a "Paranoid Security Mindset":

1. **Malware/Supply Chain Risk**:
   - Did I check for "curled-to-bash" scripts?
   - Are there suspicious dependencies?

2. **Legal & OPSEC Risk**:
   - Does this tool aggressively scrape in a way that triggers IP bans?
   - Does it leak analyst data (e.g., "phone home" telemetry)?

3. **Final Verdict**:
   - **Approved**: Safe and useful.
   - **Provisional**: Useful but requires sandboxing/code audit.
   - **Rejected**: Too risky or broken.

**Output Format**:

#### Executive Summary
- **Verdict**: [Approved/Provisional/Rejected]
- **Risk Level**: [High/Medium/Low]
- **Score**: [0-100]

#### Detailed Analysis
- **Strengths**: ...
- **Risks**: ...
- **OPSEC Warnings**: ...

#### Reflection Notes
- "I initially rated this high on utility, but the Reflection phase highlighted that it hasn't been updated in 2 years, which is a critical risk for OSINT tools relying on APIs. Downgraded score by 20 points."
```

## Variables

- `[RESOURCE_NAME]`: Name of the tool/repo.
- `[URL]`: Link to the resource.
- `[USE_CASE]`: How you intend to use it (e.g., "Automated daily scraping of Twitter").

## Example Usage

### Input

- **Resource**: `Twint` (Twitter Intelligence Tool)
- **Use Case**: Historical tweet retrieval for sentiment analysis.

### Output Excerpt

```text
...
**Branch C (Maintenance)**: Twint is legendary but has been largely broken since Twitter's 2023 API changes.
...
**Phase 2 Reflection**:
- **Critique**: Phase 1 correctly identified it as "broken", but I need to be stronger on the *rejection*. Using this tool now is a waste of time.
- **Legal Check**: It bypasses API limits, which is a ToS violation. Enterprise risk is high.

**Executive Summary**:
- **Verdict**: Rejected
- **Risk Level**: High (Functional & Legal)
- **Score**: 15/100
- **Reason**: Tool is unmaintained and non-functional against current Twitter defenses.
```
