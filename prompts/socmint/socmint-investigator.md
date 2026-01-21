---
name: SOCMINT Investigator
description: A comprehensive guide and toolset for Social Media Intelligence (SOCMINT) investigations, focusing on cross-platform correlation and digital footprint analysis.
type: how_to
---

# SOCMINT Investigator

## Description

This prompt guides you through a professional Social Media Intelligence (SOCMINT) investigation. It uses a "Cross-Platform Correlation" methodology to map a target's digital footprint across LinkedIn, X (Twitter), and other platforms, leveraging best-in-class open source tools.

## Prerequisites

- **Python Environment**: Required for tools like Sherlock, Maigret, and Twint.
- **Sock Puppet Accounts**: Do NOT use personal accounts for investigation. Use dedicated research accounts.
- **VPN/Tor**: Ensure network anonymity (OpSec).

## Methodology: Cross-Platform Correlation

1. **Discovery**: Identify unique identifiers (usernames, handles, emails).
2. **Enumeration**: Map these identifiers across 400+ platforms.
3. **Correlation**: Link disparate profiles using behavioral cues (bio, location, avatar).
4. **Deep Dive**: Extract specific data (posts, connections) from confirmed profiles.

**OpSec Reminder**:

- Never interact with the target (no likes, follows, or connection requests).
- Use a clean browser session or VM.
- Document every step with timestamps.

```

## Variables

| Variable | Description | Example |
| ---------- | ------------- | --------- |
| `[TARGET_IDENTIFIER]` | The starting point for the investigation | "jdoe1990" or "john.doe@example.com" |
| `[INVESTIGATION_GOAL]` | What you are trying to find | "Verify employment history and identify public leaks" |

## Example Usage

### Input

```text
**Target**: "cryptoking_99"
**Goal**: Identify the real identity behind this crypto influencer handle.
```

### Expected Output

```text
**Phase 1 Analysis**:

- Sherlock found "cryptoking_99" on: Twitter, Reddit, GitHub, and Steam.
- GitHub profile links to a personal website: `cryptoking.io`.

**Phase 2 Deep Dive**:

- **Twitter**: Twint scrape shows frequent posts about "Miami" and "Python".
- **GitHub**: Code commits show email `alex.smith@gmail.com`.
- **Whois**: `cryptoking.io` is registered to "Alex Smith" in Miami, FL.

**Phase 3 Correlation**:

- **Avatar**: Twitter pfp matches LinkedIn profile for "Alex Smith (Blockchain Dev)".
- **Location**: Both are in Miami.
- **Conclusion**: High confidence that "cryptoking_99" is Alex Smith.

```
