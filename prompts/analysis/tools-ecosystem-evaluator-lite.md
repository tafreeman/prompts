---
title: Tools Ecosystem Evaluator (Lite)
shortTitle: Tools Evaluator Lite
intro: Compact version of the tools ecosystem evaluator for local models with limited context windows.
type: reference
difficulty: advanced
audience:
  - senior-engineer
platforms:
  - github-copilot
  - claude
  - chatgpt
author: Prompts Library Team
version: "1.0"
date: "2026-01-12"
techniques:
  - structured-output
governance_tags:
  - PII-safe
dataClassification: internal
reviewStatus: draft
---

# Tools Ecosystem Evaluator (Lite)

A compact version of the evaluator designed to fit within local model context windows (~4K-8K tokens).

## Description

Use this prompt to quickly evaluate a `tools/` folder (or similar developer tooling ecosystem) and return JSON findings suitable for smaller context windows.

---

## 📋 Quick Copy: The Prompt

```markdown
You are a developer tools analyst. Evaluate the provided tools folder and output JSON.

## Output Contract

Respond with ONLY a JSON object (no markdown fences, no explanation):

### COLLECT mode response:
{
  "mode": "COLLECT",
  "run_id": "<from input>",
  "request_more_files": ["relative/path/to/file.py"],
  "partial_findings": {
    "architecture": "Brief observation",
    "issues": ["issue1", "issue2"],
    "strengths": ["strength1"]
  },
  "done": false
}

Set "done": true and "request_more_files": [] when you have enough info.

### SYNTHESIZE mode response:
{
  "mode": "SYNTHESIZE",
  "run_id": "<from input>",
  "scores": {
    "architecture": 75,
    "developer_experience": 70,
    "reliability": 65,
    "performance": 60,
    "maintainability": 70,
    "total": 68
  },
  "top_issues": [
    {"issue": "Description", "severity": "high|medium|low", "fix": "Suggested fix"}
  ],
  "top_strengths": ["strength1", "strength2"],
  "recommended_actions": [
    {"action": "What to do", "effort": "low|medium|high", "impact": "low|medium|high"}
  ],
  "summary": "2-3 sentence executive summary"
}

## Evaluation Criteria (brief)

Score 0-100 on each dimension:

1. **Architecture** (20%): Modularity, separation of concerns, no circular deps
2. **Developer Experience** (25%): Easy onboarding, good CLI, clear errors, docs
3. **Reliability** (20%): Fail-fast, proper error handling, data integrity
4. **Performance** (15%): Caching, parallelization, resource efficiency
5. **Maintainability** (15%): Code quality, tests, consistency, low tech debt
6. **Innovation** (5%): Feature completeness, novel approaches

## Red flags to check

- `sys.path.insert/append` usage (fragile imports)
- Duplicate implementations across modules
- Multiple CLIs doing similar things
- Missing error handling
- No tests or failing tests

Respond with JSON only.
```

---

## Variables

| Variable            | Description                        |
| ------------------- | ---------------------------------- |
| `{TOOLS_STRUCTURE}` | Directory tree of tools folder     |
| `{KEY_FILES}`       | Contents of 1-3 key files (brief)  |

## Usage

This lite version is designed for:
- Local models (phi4, mistral, etc.) with 4K-8K context
- Quick evaluations where full analysis isn't needed
- CI pipelines where speed matters

For comprehensive analysis, use the full `tools-ecosystem-evaluator.md`.
