# Project Documentation

This directory contains architecture documentation, coding standards, decision records, and the subagent registry for the `prompts` monorepo.

## Contents

| Path | Description |
| --- | --- |
| `ARCHITECTURE.md` | System architecture overview and component diagrams |
| `CODING_STANDARDS.md` | Coding standards and style guidelines |
| `subagents.yml` | Canonical registry of subagent definitions |
| `adr/` | Architecture Decision Records (ADRs) |
| `pr-checklists/` | PR review checklists for documentation and code changes |

## Table of Contents
- [Purpose](#purpose)
- [Quick start](#quick-start)
- [Subagent registry (`subagents.yml`)](#subagent-registry-subagentsyml)
- [How to add or update a subagent](#how-to-add-or-update-a-subagent)
- [Docs PR checklist (summary)](#docs-pr-checklist-summary)
- [Previewing docs (Windows / PowerShell)](#previewing-docs-windows--powershell)
- [Contacts & references](#contacts--references)

## Purpose
This directory holds architecture documentation, decision records, the canonical registry of subagents, and contributor-facing guidance for documentation PRs. Aim for clarity, reproducibility, and reviewer-friendly diffs.

## Quick start
- Edit `docs/subagents.yml` to add or update an agent definition.
- Add any new doc pages under `docs/` (follow file naming conventions).
- Open a pull request and include the checklist in `docs/pr-checklists/docs-pr-checklist.md`.

### Contributor todo (minimal)
- [ ] Add/modify mapping in `docs/subagents.yml`
- [ ] Add supporting docs under `docs/` (if applicable)
- [ ] Run local docs preview (PowerShell)
- [ ] Attach screenshots / sample outputs to PR
- [ ] Request reviewer(s) and assign labels

## Subagent registry (`subagents.yml`)
Primary source of truth for built-in and maintained subagents. Each entry should include:
- task_name
- description
- output_path (where generated artifacts or results should be saved)
- acceptance_criteria (list)
- sample_prompt (single example to exercise the agent)

See `docs/subagents.yml` for examples and canonical fields.

## How to add or update a subagent
1. Create or update an entry in `docs/subagents.yml` (follow existing examples).
2. Add supporting docs in `docs/` if the subagent needs detailed usage or examples.
3. Update any tests or fixtures that reference the subagent name.
4. Submit a docs PR using the docs PR checklist below.

## Docs PR checklist (summary)
Use the full checklist at `docs/pr-checklists/docs-pr-checklist.md` before requesting review.

## Previewing docs (Windows / PowerShell)
tested: false
```powershell
# Install a light markdown server (one-time)
npm install -g markserv

# Run preview from repo root (serves README.md at http://localhost:3000)
markserv docs --port 3000
```
tested: false
```powershell
# Alternatively, open a single file in the default Windows markdown previewer:
Start-Process docs\README.md
```

## Contacts & references
- Maintainers: see repository CODEOWNERS and PR templates.
- Canonical subagent list: `docs/subagents.yml`
- Docs PR checklist: `docs/pr-checklists/docs-pr-checklist.md`
- Runtime package docs: `agentic-workflows-v2/docs/README.md`
