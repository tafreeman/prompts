---
title: "Create OSINT/SOCMINT Prompt Library"
shortTitle: "OSINT Library Creator"
intro: "A comprehensive prompt and script to create a new OSINT-focused prompt library repository."
type: "how_to"
difficulty: "advanced"
audience:
  - "intelligence-analyst"
  - "osint-researcher"
  - "security-professional"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "osint"
  - "socmint"
  - "repository-design"
author: "Prompt Library Team"
version: "1.0"
date: "2025-11-30"
---

# Create OSINT/SOCMINT Prompt Library

## Overview

This document provides:
1. A **design specification** for a new OSINT-focused prompt library
2. A **PowerShell script** to create the repository structure and migrate files
3. A **prompt** to help generate additional content

---

## Part 1: Repository Design Specification

### New Repository Structure

```text
osint-prompts/
├── README.md                           # Main documentation
├── LICENSE                             # MIT License
├── CONTRIBUTING.md                     # Contribution guidelines
│
├── prompts/                            # Core prompt collection
│   ├── index.md                        # Prompt directory index
│   │
│   ├── investigation/                  # Investigation workflows
│   │   ├── username-investigation.md
│   │   ├── email-investigation.md
│   │   ├── phone-investigation.md
│   │   ├── domain-investigation.md
│   │   └── identity-correlation.md
│   │
│   ├── socmint/                        # Social Media Intelligence
│   │   ├── instagram-osint.md
│   │   ├── telegram-osint.md
│   │   ├── linkedin-osint.md
│   │   ├── twitter-osint.md
│   │   └── socmint-investigator.md     # Migrated
│   │
│   ├── techniques/                     # Advanced prompting for OSINT
│   │   ├── react-osint-research.md     # Migrated
│   │   ├── react-knowledge-base.md     # Migrated
│   │   ├── chain-of-thought-analysis.md
│   │   └── tree-of-thoughts-attribution.md
│   │
│   ├── analysis/                       # Analysis & reporting
│   │   ├── threat-intelligence.md
│   │   ├── attribution-analysis.md
│   │   ├── timeline-reconstruction.md
│   │   └── link-analysis.md
│   │
│   └── automation/                     # Tool automation prompts
│       ├── spiderfoot-workflow.md
│       ├── maigret-batch.md
│       └── data-correlation.md
│
├── resources/                          # Reference materials
│   ├── osint_research_resources.md     # Migrated - Tool library
│   ├── osint_tool_evaluation.md        # Migrated - Tool evaluation
│   ├── methodology/
│   │   ├── intelligence-cycle.md
│   │   └── verification-techniques.md
│   └── checklists/
│       ├── username-checklist.md
│       ├── email-checklist.md
│       └── domain-checklist.md
│
├── templates/                          # Reusable templates
│   ├── prompt-template.md              # Base prompt template
│   ├── investigation-report.md         # Report template
│   └── tool-evaluation.md              # Tool assessment template
│
├── tools/                              # Utility scripts
│   ├── validate-prompts.py             # Prompt validation
│   └── generate-index.py               # Index generator
│
└── docs/                               # Documentation
    ├── getting-started.md
    ├── prompt-authoring-guide.md
    └── tool-integration.md
```

### Design Principles

1. **OSINT-Focused**: Only intelligence-related content, no software development prompts
2. **Practical**: Every prompt should map to a real investigation workflow
3. **Tool-Aware**: Reference actual tools (Sherlock, Maigret, SpiderFoot, etc.)
4. **Methodology-Driven**: Follow intelligence cycle (Planning → Collection → Processing → Analysis → Dissemination)
5. **Minimal Dependencies**: No complex build systems or frameworks

### Frontmatter Schema (Simplified)

```yaml
---
title: "Prompt Title"
shortTitle: "Short Name"
intro: "One-sentence description"
type: "investigation|analysis|automation|reference"
category: "username|email|phone|domain|socmint|threat-intel"
tools:                          # Related tools
  - sherlock
  - maigret
platforms:
  - github-copilot
  - claude
author: "Author Name"
version: "1.0"
date: "2025-11-30"
---
```

---

## Part 2: PowerShell Migration Script

Save this as `create-osint-library.ps1` and run it to create the new repository:

```powershell
#Requires -Version 7.0

<#
.SYNOPSIS
    Creates a new OSINT-focused prompt library repository.
.DESCRIPTION
    This script:
    1. Creates the new repository structure
    2. Migrates relevant files from the source library
    3. Generates index files and README
.PARAMETER SourcePath
    Path to the source prompt library (default: current directory)
.PARAMETER DestinationPath
    Path where the new OSINT library will be created
.EXAMPLE
    .\create-osint-library.ps1 -DestinationPath "D:\source\osint-prompts"
#>

param(
    [string]$SourcePath = "D:\source\osi\prompts",
    [string]$DestinationPath = "D:\source\osint-prompts"
)

# Colors for output
$Colors = @{
    Success = "Green"
    Info = "Cyan"
    Warning = "Yellow"
    Error = "Red"
}

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $symbol = switch ($Type) {
        "Success" { "✓" }
        "Info"    { "→" }
        "Warning" { "!" }
        "Error"   { "✗" }
    }
    Write-Host "[$symbol] $Message" -ForegroundColor $Colors[$Type]
}

# === 1. CREATE DIRECTORY STRUCTURE ===
Write-Status "Creating OSINT Library structure..." "Info"

$directories = @(
    "prompts/investigation"
    "prompts/socmint"
    "prompts/techniques"
    "prompts/analysis"
    "prompts/automation"
    "resources/methodology"
    "resources/checklists"
    "templates"
    "tools"
    "docs"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $DestinationPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Status "Created: $dir" "Success"
    }
}

# === 2. MIGRATE FILES ===
Write-Status "Migrating OSINT-related files..." "Info"

$migrations = @(
    # ==========================================
    # ADVANCED FOLDER - ALL FILES (techniques/)
    # ==========================================
    @{
        Source = "prompts/advanced/chain-of-thought-concise.md"
        Dest = "prompts/techniques/chain-of-thought-concise.md"
    }
    @{
        Source = "prompts/advanced/chain-of-thought-debugging.md"
        Dest = "prompts/techniques/chain-of-thought-debugging.md"
    }
    @{
        Source = "prompts/advanced/chain-of-thought-detailed.md"
        Dest = "prompts/techniques/chain-of-thought-detailed.md"
    }
    @{
        Source = "prompts/advanced/chain-of-thought-guide.md"
        Dest = "prompts/techniques/chain-of-thought-guide.md"
    }
    @{
        Source = "prompts/advanced/chain-of-thought-performance-analysis.md"
        Dest = "prompts/techniques/chain-of-thought-performance-analysis.md"
    }
    @{
        Source = "prompts/advanced/library-analysis-react.md"
        Dest = "prompts/techniques/library-analysis-react.md"
    }
    @{
        Source = "prompts/advanced/library.md"
        Dest = "prompts/techniques/library.md"
    }
    @{
        Source = "prompts/advanced/osint-research-react.md"
        Dest = "prompts/techniques/osint-research-react.md"
    }
    @{
        Source = "prompts/advanced/prompt-library-refactor-react.md"
        Dest = "prompts/techniques/prompt-library-refactor-react.md"
    }
    @{
        Source = "prompts/advanced/rag-document-retrieval.md"
        Dest = "prompts/techniques/rag-document-retrieval.md"
    }
    @{
        Source = "prompts/advanced/react-doc-search-synthesis.md"
        Dest = "prompts/techniques/react-doc-search-synthesis.md"
    }
    @{
        Source = "prompts/advanced/react-knowledge-base-research.md"
        Dest = "prompts/techniques/react-knowledge-base-research.md"
    }
    @{
        Source = "prompts/advanced/react-tool-augmented.md"
        Dest = "prompts/techniques/react-tool-augmented.md"
    }
    @{
        Source = "prompts/advanced/README.md"
        Dest = "prompts/techniques/README.md"
    }
    @{
        Source = "prompts/advanced/reflection-self-critique.md"
        Dest = "prompts/techniques/reflection-self-critique.md"
    }
    @{
        Source = "prompts/advanced/tree-of-thoughts-architecture-evaluator.md"
        Dest = "prompts/techniques/tree-of-thoughts-architecture-evaluator.md"
    }
    @{
        Source = "prompts/advanced/tree-of-thoughts-evaluator-reflection.md"
        Dest = "prompts/techniques/tree-of-thoughts-evaluator-reflection.md"
    }
    @{
        Source = "prompts/advanced/tree-of-thoughts-template.md"
        Dest = "prompts/techniques/tree-of-thoughts-template.md"
    }
    
    # ==========================================
    # SOCMINT FOLDER - ALL FILES
    # ==========================================
    @{
        Source = "prompts/socmint/socmint-investigator.md"
        Dest = "prompts/socmint/socmint-investigator.md"
    }
    
    # ==========================================
    # DOCS - OSINT Research & Reports
    # ==========================================
    @{
        Source = "docs/osint_research_resources.md"
        Dest = "resources/osint_research_resources.md"
    }
    @{
        Source = "docs/osint_tool_evaluation_report.md"
        Dest = "resources/osint_tool_evaluation_report.md"
    }
    @{
        Source = "docs/advanced-techniques.md"
        Dest = "docs/advanced-techniques.md"
    }
    
    # ==========================================
    # TEMPLATES
    # ==========================================
    @{
        Source = "templates/prompt-template.md"
        Dest = "templates/prompt-template.md"
    }
)

foreach ($migration in $migrations) {
    $sourcePath = Join-Path $SourcePath $migration.Source
    $destPath = Join-Path $DestinationPath $migration.Dest
    
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Status "Migrated: $($migration.Source) -> $($migration.Dest)" "Success"
    } else {
        Write-Status "Not found: $($migration.Source)" "Warning"
    }
}

# === 3. CREATE README.md ===
Write-Status "Creating README.md..." "Info"

$readme = @'
# OSINT & SOCMINT Prompt Library

A focused, practical prompt library for **Open Source Intelligence (OSINT)** and **Social Media Intelligence (SOCMINT)** investigations.

## 🎯 What This Library Is For

- **Intelligence Analysts**: Prompts for systematic investigation workflows
- **OSINT Researchers**: Tool-specific prompts and automation patterns
- **Security Professionals**: Threat intelligence and attribution analysis
- **Investigators**: Digital footprint analysis and identity correlation

## 🔧 Featured Tools

This library is designed to work with industry-standard OSINT tools:

| Category | Primary Tools | Stars |
|----------|--------------|-------|
| **Username Search** | Maigret, Sherlock, Blackbird | 18k, 70.6k, 5k |
| **Email Intel** | Holehe, GHunt, h8mail | 9.8k, 18.2k, - |
| **Frameworks** | SpiderFoot, theHarvester | 16k, 15.1k |
| **Social Media** | Instaloader, Telepathy | 11.1k, 1.2k |

## 📁 Repository Structure

```text
osint-prompts/
├── prompts/                    # Core prompt collection
│   ├── investigation/          # Investigation workflows
│   ├── socmint/               # Social Media Intelligence
│   ├── techniques/            # Advanced prompting (ReAct, CoT, ToT)
│   ├── analysis/              # Analysis & reporting
│   └── automation/            # Tool automation
├── resources/                  # Reference materials
│   ├── osint_research_resources.md  # Comprehensive tool library
│   └── osint_tool_evaluation.md     # Tool recommendations
├── templates/                  # Reusable templates
└── docs/                       # Documentation
```

## 🚀 Quick Start

### 1. Username Investigation
```text
Use: prompts/investigation/username-investigation.md
Tools: Maigret → Sherlock → Blackbird (AI profiling)
```

### 2. Email-to-Identity
```text
Use: prompts/investigation/email-investigation.md
Tools: Holehe → GHunt → h8mail
```

### 3. Social Media Deep-Dive
```text
Use: prompts/socmint/
Tools: Instaloader (IG), Telepathy (Telegram)
```

## 📖 Key Resources

- **[OSINT Research Resources](resources/osint_research_resources.md)**: Comprehensive tool library with 50+ tools
- **[Tool Evaluation Report](resources/osint_tool_evaluation.md)**: Detailed tool recommendations by use case

## 🧠 Advanced Techniques

This library includes advanced prompting patterns optimized for OSINT:

- **ReAct**: Reasoning + Acting for iterative research
- **Chain-of-Thought**: Step-by-step investigation analysis
- **Tree-of-Thoughts**: Multi-hypothesis attribution

## 📝 Prompt Format

All prompts follow a consistent structure:

```markdown
---
title: "Investigation Prompt"
type: "investigation"
category: "username"
tools: [maigret, sherlock]
---

# Prompt Title

## Description
What this prompt does.

## Prompt
[The actual prompt text]

## Variables
| Variable | Description |
|----------|-------------|
| [TARGET] | The username/email/domain to investigate |

## Example
Concrete example with real workflow.
```

## 🤝 Contributing

1. Follow the template in `templates/prompt-template.md`
2. Focus on practical, tool-aware prompts
3. Include example workflows with real tools

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Built for the OSINT community. 🔍**
'@

$readme | Set-Content (Join-Path $DestinationPath "README.md") -Encoding UTF8
Write-Status "Created README.md" "Success"

# === 4. CREATE LICENSE ===
$license = @'
MIT License

Copyright (c) 2025 OSINT Prompts Library

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'@

$license | Set-Content (Join-Path $DestinationPath "LICENSE") -Encoding UTF8
Write-Status "Created LICENSE" "Success"

# === 5. CREATE PROMPT INDEX ===
$promptIndex = @'
---
title: "OSINT Prompt Index"
---

# OSINT Prompt Library Index

## Investigation Workflows

| Prompt | Description | Tools |
|--------|-------------|-------|
| [Username Investigation](investigation/username-investigation.md) | Full username enumeration workflow | Maigret, Sherlock, Blackbird |
| [Email Investigation](investigation/email-investigation.md) | Email-to-identity workflow | Holehe, GHunt, h8mail |
| [Phone Investigation](investigation/phone-investigation.md) | Phone number OSINT | PhoneInfoga |
| [Domain Investigation](investigation/domain-investigation.md) | Domain/IP reconnaissance | theHarvester, SpiderFoot |

## Social Media Intelligence (SOCMINT)

| Prompt | Description | Tools |
|--------|-------------|-------|
| [SOCMINT Investigator](socmint/socmint-investigator.md) | General social media investigation | Multiple |
| [Instagram OSINT](socmint/instagram-osint.md) | Instagram-specific techniques | Instaloader, Osintgram |
| [Telegram OSINT](socmint/telegram-osint.md) | Telegram channel/user analysis | Telepathy, TeleTracker |

## Advanced Techniques

| Prompt | Pattern | Best For |
|--------|---------|----------|
| [ReAct OSINT Research](techniques/react-osint-research.md) | ReAct | Iterative research |
| [ReAct Knowledge Base](techniques/react-knowledge-base.md) | ReAct | Building tool libraries |
| [Chain-of-Thought Analysis](techniques/chain-of-thought-analysis.md) | CoT | Step-by-step investigation |
| [Tree-of-Thoughts Attribution](techniques/tree-of-thoughts-template.md) | ToT | Multi-hypothesis analysis |

## Analysis & Reporting

| Prompt | Description |
|--------|-------------|
| [Threat Intelligence](analysis/threat-intelligence.md) | CTI analysis framework |
| [Attribution Analysis](analysis/attribution-analysis.md) | Actor attribution |
| [Timeline Reconstruction](analysis/timeline-reconstruction.md) | Event chronology |
'@

$promptIndex | Set-Content (Join-Path $DestinationPath "prompts/index.md") -Encoding UTF8
Write-Status "Created prompts/index.md" "Success"

# === 6. CREATE GETTING STARTED GUIDE ===
$gettingStarted = @'
---
title: "Getting Started with OSINT Prompts"
---

# Getting Started

## Quick Start

### 1. Choose Your Investigation Type

| I have a... | Start with... |
|-------------|---------------|
| Username | `prompts/investigation/username-investigation.md` |
| Email address | `prompts/investigation/email-investigation.md` |
| Phone number | `prompts/investigation/phone-investigation.md` |
| Domain/IP | `prompts/investigation/domain-investigation.md` |
| Social media profile | `prompts/socmint/` |

### 2. Install Required Tools

Most prompts reference specific tools. Install the ones you need:

```bash
# Username Enumeration (pick one or all)
pip install maigret
pip install sherlock-project
git clone https://github.com/p1ngul1n0/blackbird

# Email Intelligence
pip install holehe
pipx install ghunt

# Frameworks
git clone https://github.com/smicallef/spiderfoot
git clone https://github.com/laramies/theHarvester

# Social Media
pip install instaloader
pip install telepathy
```

### 3. Use the Prompts

1. Open the relevant prompt file
2. Copy the prompt text
3. Replace `[VARIABLES]` with your target data
4. Paste into your AI tool (Claude, ChatGPT, Copilot)
5. Follow the workflow

## Best Practices

1. **Start Passive**: Always use passive reconnaissance first
2. **Verify Everything**: Cross-reference findings across tools
3. **Document**: Keep notes on all findings
4. **Legal Compliance**: Ensure your activities are lawful

## Tool Selection Guide

See [resources/osint_tool_evaluation.md](../resources/osint_tool_evaluation.md) for detailed tool recommendations.
'@

$gettingStarted | Set-Content (Join-Path $DestinationPath "docs/getting-started.md") -Encoding UTF8
Write-Status "Created docs/getting-started.md" "Success"

# === 7. CREATE SAMPLE INVESTIGATION PROMPTS ===

$usernameInvestigation = @'
---
title: "Username Investigation Workflow"
shortTitle: "Username OSINT"
intro: "Systematic username enumeration across platforms with AI-powered profiling."
type: "investigation"
category: "username"
tools:
  - maigret
  - sherlock
  - blackbird
platforms:
  - github-copilot
  - claude
author: "OSINT Library"
version: "1.0"
date: "2025-11-30"
---

# Username Investigation Workflow

## Description

A comprehensive workflow for investigating a username across social platforms, extracting linked accounts, and generating behavioral profiles using AI.

## Prompt

```text
You are an OSINT analyst investigating the username: [USERNAME]

## Investigation Workflow

### Phase 1: Username Enumeration
1. Run Maigret for comprehensive coverage (3000+ sites):
   ```bash
   maigret [USERNAME] --html --pdf
   ```
2. Verify with Sherlock (400+ sites, fast):
   ```bash
   sherlock [USERNAME] --csv
   ```
3. Generate AI profile with Blackbird:
   ```bash
   python blackbird.py --username [USERNAME] --ai --pdf
   ```

### Phase 2: Data Extraction
For each confirmed account, extract:
- Profile creation date
- Bio/description text
- Profile picture (reverse image search)
- Linked accounts/emails
- Activity patterns (posting times)
- Geographic indicators

### Phase 3: Email Discovery
If emails are found in profiles:
1. Check account registrations: `holehe [EMAIL]`
2. If Gmail, run GHunt: `ghunt email [EMAIL]`

### Phase 4: Correlation & Analysis
- Cross-reference usernames across platforms
- Identify patterns in:
  - Naming conventions
  - Bio text similarity
  - Profile picture reuse
  - Time zone indicators

## Output Format

Provide a structured report with:
1. **Confirmed Accounts**: Platform, URL, confidence level
2. **Email Addresses**: Discovered emails and their sources
3. **Profile Patterns**: Naming conventions, bio similarities
4. **AI Profile Summary**: Behavioral analysis from Blackbird
5. **Next Steps**: Recommended follow-up actions
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[USERNAME]` | Target username to investigate | `johndoe_123` |

## Example

**Input:**
```text
Investigate username: crypto_trader_2024
```

**Output:**
```text
## Username Investigation Report: crypto_trader_2024

### Confirmed Accounts (High Confidence)
| Platform | URL | Evidence |
|----------|-----|----------|
| Twitter/X | twitter.com/crypto_trader_2024 | Exact match |
| Reddit | reddit.com/u/crypto_trader_2024 | Exact match |
| Telegram | t.me/crypto_trader_2024 | Exact match |

### Discovered Emails
- c.trader2024@proton.me (from Telegram bio)

### Pattern Analysis
- Naming convention: [topic]_[role]_[year]
- Interests: Cryptocurrency, trading
- Active hours: 14:00-22:00 UTC

### AI Profile Summary (Blackbird)
- Likely timezone: UTC-5 to UTC-8 (Americas)
- Account age: Created 2024
- Activity level: High on trading platforms

### Next Steps
1. Run Holehe on discovered email
2. Check crypto addresses mentioned in posts
3. Analyze posting patterns for location indicators
```

## Tips

1. Always run Maigret first - it has the best coverage (3000+ sites)
2. Use Blackbird's AI feature for behavioral analysis
3. Check for username variations: underscores, numbers, etc.
4. Save HTML/PDF reports for documentation
'@

$usernameInvestigation | Set-Content (Join-Path $DestinationPath "prompts/investigation/username-investigation.md") -Encoding UTF8
Write-Status "Created prompts/investigation/username-investigation.md" "Success"

# Email Investigation
$emailInvestigation = @'
---
title: "Email Investigation Workflow"
shortTitle: "Email OSINT"
intro: "Discover accounts linked to an email address without alerting the target."
type: "investigation"
category: "email"
tools:
  - holehe
  - ghunt
  - h8mail
platforms:
  - github-copilot
  - claude
author: "OSINT Library"
version: "1.0"
date: "2025-11-30"
---

# Email Investigation Workflow

## Description

Investigate an email address to discover linked accounts, check for data breaches, and extract identity information - all without alerting the target.

## Prompt

```text
You are an OSINT analyst investigating the email: [EMAIL]

## Investigation Workflow

### Phase 1: Account Discovery (Silent)
Run Holehe to find registered accounts (uses password recovery - silent):
```bash
holehe [EMAIL]
```

### Phase 2: Google Account Investigation
If Gmail, run GHunt for full Google OSINT:
```bash
ghunt email [EMAIL] --json results.json
```

This reveals:
- Google account name
- Profile picture
- Google Maps reviews
- YouTube channel
- Calendar events (if public)
- Google Drive shared files

### Phase 3: Breach Database Search
Check for exposed credentials:
```bash
h8mail -t [EMAIL]
```

Also check:
- haveibeenpwned.com
- IntelligenceX (intelx.io)
- DeHashed

### Phase 4: Username Extraction
For accounts found, extract usernames and run username investigation:
- Holehe output includes usernames for some platforms
- GHunt reveals Google username/Gaia ID

## Output Format

Provide a structured report:
1. **Registered Accounts**: Platform, status, additional info
2. **Google Profile**: Name, picture, associated services
3. **Breach Exposure**: Breaches found, data types exposed
4. **Extracted Usernames**: For follow-up investigation
5. **Risk Assessment**: Exposure level and recommendations
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[EMAIL]` | Target email address | `john.doe@gmail.com` |

## Example

**Input:**
```text
Investigate email: analyst.jane@protonmail.com
```

**Output:**
```text
## Email Investigation Report: analyst.jane@protonmail.com

### Registered Accounts (via Holehe)
| Platform | Status | Additional Info |
|----------|--------|-----------------|
| Twitter | ✓ Exists | Recovery: ana***@protonmail.com |
| Spotify | ✓ Exists | - |
| Adobe | ✓ Exists | - |
| Discord | ✓ Exists | - |

### Breach Exposure
| Breach | Date | Data Types |
|--------|------|------------|
| None found | - | - |

### Extracted Usernames
- Twitter: @analyst_jane (from profile lookup)

### Next Steps
1. Run username investigation on: analyst_jane
2. Check Spotify for public playlists
3. Search Discord servers for username
```

## Tips

1. Holehe is SILENT - it doesn't alert the target
2. GHunt requires authentication - set up before use
3. Always check both email variations (with/without dots for Gmail)
4. ProtonMail/Tutanota emails have limited discoverability
'@

$emailInvestigation | Set-Content (Join-Path $DestinationPath "prompts/investigation/email-investigation.md") -Encoding UTF8
Write-Status "Created prompts/investigation/email-investigation.md" "Success"

# === 8. INITIALIZE GIT REPO ===
Write-Status "Initializing Git repository..." "Info"

Push-Location $DestinationPath
try {
    git init 2>$null
    git add -A 2>$null
    git commit -m "Initial commit: OSINT Prompt Library" 2>$null
    Write-Status "Git repository initialized" "Success"
} catch {
    Write-Status "Git initialization skipped (git not available or error)" "Warning"
}
Pop-Location

# === SUMMARY ===
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Status "OSINT Library created successfully!" "Success"
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $DestinationPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. cd $DestinationPath"
Write-Host "  2. Review and customize prompts"
Write-Host "  3. Add more investigation prompts"
Write-Host "  4. Push to GitHub: git remote add origin <url> && git push -u origin main"
Write-Host ""
```

---

## Part 3: Prompt for Generating Additional Content

Use this prompt with Claude/ChatGPT to generate new investigation prompts:

```text
You are an expert OSINT analyst and prompt engineer. Create a new investigation prompt for the OSINT Prompt Library.

## Requirements

1. **Format**: Follow this exact template:

```markdown
---
title: "[TITLE]"
shortTitle: "[SHORT]"
intro: "[ONE SENTENCE]"
type: "investigation"
category: "[username|email|phone|domain|socmint|threat-intel]"
tools:
  - [tool1]
  - [tool2]
platforms:
  - github-copilot
  - claude
author: "OSINT Library"
version: "1.0"
date: "2025-11-30"
---

# [TITLE]

## Description
[2-3 sentences explaining the workflow]

## Prompt
[The actual prompt with phases, commands, and output format]

## Variables
| Variable | Description | Example |
|----------|-------------|---------|
| [VAR] | Description | example |

## Example
[Realistic input/output example]

## Tips
[3-5 practical tips]
```

2. **Tool Awareness**: Reference real tools:
   - Username: Maigret (3000+ sites), Sherlock (400+), Blackbird (AI)
   - Email: Holehe (120+ sites), GHunt (Google), h8mail (breaches)
   - Domain: theHarvester, SpiderFoot, Shodan, crt.sh
   - Phone: PhoneInfoga
   - Social: Instaloader (IG), Telepathy (Telegram)

3. **Practical Focus**: Include actual shell commands that work
4. **Structured Output**: Define clear report formats
5. **Workflow Phases**: Break into logical investigation phases

## Create a prompt for: [YOUR REQUEST HERE]

Examples:
- "Telegram channel investigation"
- "Cryptocurrency wallet attribution"
- "Domain infrastructure mapping"
- "LinkedIn company enumeration"
```

---

## Usage Instructions

### Option 1: Run the PowerShell Script

```powershell
# Save the script from Part 2 to a file
# Then run:
.\create-osint-library.ps1 -DestinationPath "D:\source\osint-prompts"
```

### Option 2: Manual Creation

1. Create the directory structure manually
2. Copy the files listed in the migration section
3. Create the README and other files from the templates above

### Option 3: Use the Prompt (Part 3)

Use the generation prompt with Claude/ChatGPT to create additional investigation prompts for your library.

---

## Files to Migrate (Complete List)

### Advanced Techniques → `prompts/techniques/`

| Source File | Description |
|-------------|-------------|
| `chain-of-thought-concise.md` | CoT concise pattern |
| `chain-of-thought-debugging.md` | CoT for debugging |
| `chain-of-thought-detailed.md` | CoT detailed analysis |
| `chain-of-thought-guide.md` | CoT usage guide |
| `chain-of-thought-performance-analysis.md` | CoT performance analysis |
| `library-analysis-react.md` | ReAct library analysis |
| `library.md` | Library patterns |
| `osint-research-react.md` | **OSINT ReAct research** |
| `prompt-library-refactor-react.md` | ReAct refactoring |
| `rag-document-retrieval.md` | RAG pattern |
| `react-doc-search-synthesis.md` | **OSINT resource gathering** |
| `react-knowledge-base-research.md` | **OSINT KB research** |
| `react-tool-augmented.md` | Tool-augmented ReAct |
| `README.md` | Techniques README |
| `reflection-self-critique.md` | Reflection pattern |
| `tree-of-thoughts-architecture-evaluator.md` | ToT architecture |
| `tree-of-thoughts-evaluator-reflection.md` | **OSINT resource evaluator** |
| `tree-of-thoughts-template.md` | ToT template |

### SOCMINT → `prompts/socmint/`

| Source File | Description |
|-------------|-------------|
| `socmint-investigator.md` | **SOCMINT investigation workflow** |

### Docs/Resources → `resources/` and `docs/`

| Source File | Destination | Description |
|-------------|-------------|-------------|
| `docs/osint_research_resources.md` | `resources/` | **Comprehensive tool library** |
| `docs/osint_tool_evaluation_report.md` | `resources/` | **Tool evaluation report** |
| `docs/advanced-techniques.md` | `docs/` | Advanced techniques guide |

### Templates → `templates/`

| Source File | Description |
|-------------|-------------|
| `templates/prompt-template.md` | Base prompt template |
