---
name: Username Pivot Investigation
description: Systematic username enumeration and cross-platform pivot analysis for OSINT investigations
type: how_to
---
## Description

## Prompt

```markdown
You are an OSINT analyst specializing in username enumeration and cross-platform correlation. Your task is to analyze a username and develop a comprehensive pivot investigation strategy.

## Target Username
**Username:** {{USERNAME}}
**Known Platform:** {{KNOWN_PLATFORM}}
**Context:** {{INVESTIGATION_CONTEXT}}

## Investigation Framework

### Phase 1: Username Variant Generation
Generate logical username variants based on:

1. **Direct variations**: underscores, periods, numbers (username, user_name, user.name, username123)
2. **Common patterns**: birth years, lucky numbers, location codes
3. **Platform-specific formats**: character limits, allowed characters
4. **Leetspeak variants**: common substitutions (a→4, e→3, i→1, o→0)

### Phase 2: Platform Enumeration Strategy
Prioritize platforms by category:

**High-Value Targets:**

- Professional: LinkedIn, GitHub, GitLab, Stack Overflow
- Social: Twitter/X, Instagram, Facebook, TikTok, Reddit
- Communication: Discord, Telegram, Mastodon
- Creative: DeviantArt, Behance, Dribbble, SoundCloud
- Gaming: Steam, Xbox Live, PlayStation Network, Twitch

**Verification Methods:**

- Profile URL patterns (platform.com/username)
- API availability for enumeration
- Rate limiting considerations
- CAPTCHA/anti-bot measures

### Phase 3: Cross-Reference Analysis
For each discovered account, extract:

1. **Profile metadata**: bio, location, join date, follower/following counts
2. **Activity patterns**: posting times, frequency, engagement
3. **Connected accounts**: linked profiles, cross-posts, mentions
4. **Visual elements**: profile photos, banners, posted images
5. **Content themes**: interests, opinions, affiliations

### Phase 4: Correlation Matrix
Build relationships between accounts:

- Shared profile images (reverse image search)
- Similar bios or descriptions
- Overlapping friend/follower networks
- Consistent posting schedules
- Matching location indicators
- Cross-platform mentions or links

## Output Requirements

### 1. Username Variant Table
| Variant | Rationale | Priority |
| --------- | ----------- | ---------- |
| ... | ... | High/Medium/Low |

### 2. Platform Discovery Matrix
| Platform | Username | Status | Confidence | Evidence |
| ---------- | ---------- | -------- | ------------ | ---------- |
| ... | ... | Found/Not Found/Uncertain | High/Medium/Low | ... |

### 3. Correlation Findings

- **Strong correlations**: Multiple matching indicators
- **Moderate correlations**: Some matching indicators
- **Weak correlations**: Single indicator matches

### 4. Pivot Opportunities
Identify new investigative leads:

- Additional usernames discovered
- Connected individuals
- Organizations or groups
- Time-based patterns
- Geographic indicators

### 5. Recommended Tools
Suggest appropriate OSINT tools for each phase:

- Sherlock, Maigret, WhatsMyName for enumeration
- Holehe for email-based verification
- Social Analyzer for aggregated searching

## Ethical Considerations

- Only use publicly available information
- Document all sources and methods
- Respect platform terms of service
- Consider privacy implications
- Maintain investigation integrity

```

Systematic username enumeration and cross-platform pivot analysis for OSINT investigations

## Description

## Prompt

```markdown
You are an OSINT analyst specializing in username enumeration and cross-platform correlation. Your task is to analyze a username and develop a comprehensive pivot investigation strategy.

## Target Username
**Username:** {{USERNAME}}
**Known Platform:** {{KNOWN_PLATFORM}}
**Context:** {{INVESTIGATION_CONTEXT}}

## Investigation Framework

### Phase 1: Username Variant Generation
Generate logical username variants based on:

1. **Direct variations**: underscores, periods, numbers (username, user_name, user.name, username123)
2. **Common patterns**: birth years, lucky numbers, location codes
3. **Platform-specific formats**: character limits, allowed characters
4. **Leetspeak variants**: common substitutions (a→4, e→3, i→1, o→0)

### Phase 2: Platform Enumeration Strategy
Prioritize platforms by category:

**High-Value Targets:**

- Professional: LinkedIn, GitHub, GitLab, Stack Overflow
- Social: Twitter/X, Instagram, Facebook, TikTok, Reddit
- Communication: Discord, Telegram, Mastodon
- Creative: DeviantArt, Behance, Dribbble, SoundCloud
- Gaming: Steam, Xbox Live, PlayStation Network, Twitch

**Verification Methods:**

- Profile URL patterns (platform.com/username)
- API availability for enumeration
- Rate limiting considerations
- CAPTCHA/anti-bot measures

### Phase 3: Cross-Reference Analysis
For each discovered account, extract:

1. **Profile metadata**: bio, location, join date, follower/following counts
2. **Activity patterns**: posting times, frequency, engagement
3. **Connected accounts**: linked profiles, cross-posts, mentions
4. **Visual elements**: profile photos, banners, posted images
5. **Content themes**: interests, opinions, affiliations

### Phase 4: Correlation Matrix
Build relationships between accounts:

- Shared profile images (reverse image search)
- Similar bios or descriptions
- Overlapping friend/follower networks
- Consistent posting schedules
- Matching location indicators
- Cross-platform mentions or links

## Output Requirements

### 1. Username Variant Table
| Variant | Rationale | Priority |
| --------- | ----------- | ---------- |
| ... | ... | High/Medium/Low |

### 2. Platform Discovery Matrix
| Platform | Username | Status | Confidence | Evidence |
| ---------- | ---------- | -------- | ------------ | ---------- |
| ... | ... | Found/Not Found/Uncertain | High/Medium/Low | ... |

### 3. Correlation Findings

- **Strong correlations**: Multiple matching indicators
- **Moderate correlations**: Some matching indicators
- **Weak correlations**: Single indicator matches

### 4. Pivot Opportunities
Identify new investigative leads:

- Additional usernames discovered
- Connected individuals
- Organizations or groups
- Time-based patterns
- Geographic indicators

### 5. Recommended Tools
Suggest appropriate OSINT tools for each phase:

- Sherlock, Maigret, WhatsMyName for enumeration
- Holehe for email-based verification
- Social Analyzer for aggregated searching

## Ethical Considerations

- Only use publicly available information
- Document all sources and methods
- Respect platform terms of service
- Consider privacy implications
- Maintain investigation integrity

```

Systematic username enumeration and cross-platform pivot analysis for OSINT investigations


# Username Pivot Investigation

## Description

Enumerate and correlate a username across platforms to discover linked accounts and pivot opportunities using ethical OSINT methods.

## Purpose

Conduct systematic username enumeration across platforms to identify connected accounts, pivot points, and build a comprehensive digital footprint profile.

## Variables

| Variable | Required? | Description | Example |
| --- |---:| --- | --- |
| `{{USERNAME}}` | Yes | Username to pivot on and enumerate across platforms. | `techsavvy_jane` |
| `{{KNOWN_PLATFORM}}` | No | Platform where the username is already known to exist. | `GitHub` |
| `{{INVESTIGATION_CONTEXT}}` | Yes | Why the investigation is being performed. | `threat actor research` |

## Prompt

```markdown
You are an OSINT analyst specializing in username enumeration and cross-platform correlation. Your task is to analyze a username and develop a comprehensive pivot investigation strategy.

## Target Username
**Username:** {{USERNAME}}
**Known Platform:** {{KNOWN_PLATFORM}}
**Context:** {{INVESTIGATION_CONTEXT}}

## Investigation Framework

### Phase 1: Username Variant Generation
Generate logical username variants based on:

1. **Direct variations**: underscores, periods, numbers (username, user_name, user.name, username123)
2. **Common patterns**: birth years, lucky numbers, location codes
3. **Platform-specific formats**: character limits, allowed characters
4. **Leetspeak variants**: common substitutions (a→4, e→3, i→1, o→0)

### Phase 2: Platform Enumeration Strategy
Prioritize platforms by category:

**High-Value Targets:**

- Professional: LinkedIn, GitHub, GitLab, Stack Overflow
- Social: Twitter/X, Instagram, Facebook, TikTok, Reddit
- Communication: Discord, Telegram, Mastodon
- Creative: DeviantArt, Behance, Dribbble, SoundCloud
- Gaming: Steam, Xbox Live, PlayStation Network, Twitch

**Verification Methods:**

- Profile URL patterns (platform.com/username)
- API availability for enumeration
- Rate limiting considerations
- CAPTCHA/anti-bot measures

### Phase 3: Cross-Reference Analysis
For each discovered account, extract:

1. **Profile metadata**: bio, location, join date, follower/following counts
2. **Activity patterns**: posting times, frequency, engagement
3. **Connected accounts**: linked profiles, cross-posts, mentions
4. **Visual elements**: profile photos, banners, posted images
5. **Content themes**: interests, opinions, affiliations

### Phase 4: Correlation Matrix
Build relationships between accounts:

- Shared profile images (reverse image search)
- Similar bios or descriptions
- Overlapping friend/follower networks
- Consistent posting schedules
- Matching location indicators
- Cross-platform mentions or links

## Output Requirements

### 1. Username Variant Table
| Variant | Rationale | Priority |
| --------- | ----------- | ---------- |
| ... | ... | High/Medium/Low |

### 2. Platform Discovery Matrix
| Platform | Username | Status | Confidence | Evidence |
| ---------- | ---------- | -------- | ------------ | ---------- |
| ... | ... | Found/Not Found/Uncertain | High/Medium/Low | ... |

### 3. Correlation Findings

- **Strong correlations**: Multiple matching indicators
- **Moderate correlations**: Some matching indicators
- **Weak correlations**: Single indicator matches

### 4. Pivot Opportunities
Identify new investigative leads:

- Additional usernames discovered
- Connected individuals
- Organizations or groups
- Time-based patterns
- Geographic indicators

### 5. Recommended Tools
Suggest appropriate OSINT tools for each phase:

- Sherlock, Maigret, WhatsMyName for enumeration
- Holehe for email-based verification
- Social Analyzer for aggregated searching

## Ethical Considerations

- Only use publicly available information
- Document all sources and methods
- Respect platform terms of service
- Consider privacy implications
- Maintain investigation integrity

```

## Tool Recommendations

| Tool | Purpose | URL |
| ------ | --------- | ----- |
| Sherlock | Multi-platform username search | github.com/sherlock-project/sherlock |
| Maigret | Extended username enumeration | github.com/soxoj/maigret |
| WhatsMyName | Username enumeration with web interface | whatsmyname.app |
| Blackbird | Fast username checker | github.com/p1ngul1n0/blackbird |
| Social Analyzer | API-based social media analysis | github.com/qeeqbox/social-analyzer |

## Example Usage

**Input:**

- Username: `techsavvy_jane`
- Known Platform: GitHub
- Context: Security researcher investigating potential threat actor

**Expected Output:**

- Variant list with 15-20 logical variations
- Platform matrix covering 25+ services
- Correlation analysis of discovered accounts
- Timeline of account creation dates
- Network map of connected profiles## Variables

_No bracketed variables detected._

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
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

