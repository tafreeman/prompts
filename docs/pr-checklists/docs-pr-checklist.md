# Docs PR Checklist

A comprehensive checklist to use when opening documentation or subagent-related PRs.
Target audience: new contributors and maintainers. Complete each item before requesting review.

## PR metadata
- [ ] PR title is descriptive and follows repository conventions.
- [ ] PR description includes: short summary, motivation, and a list of changed files.
- [ ] Link to any relevant issue(s) or design docs.

## Content & scope
- [ ] Only documentation or subagent registry changes are included in this PR (or any code changes are clearly separated).
- [ ] All new or changed documentation files are in `docs/` or referenced location.
- [ ] `docs/subagents.yml` updates included if adding/updating subagents.
  - [ ] Added `task_name`, `description`, `output_path`, `acceptance_criteria`, and `sample_prompt`.
  - [ ] Sample prompt is concise (< 5 lines) and reproducible.
- [ ] If adding images/screenshots, they are placed under `docs/assets/` and referenced with relative paths.

## Quality & clarity
- [ ] Content is concise and uses active voice.
- [ ] Headings follow repository style and hierarchy.
- [ ] Code blocks and commands are tested locally where feasible.
- [ ] All examples include expected outputs or notes about variability.

## Accessibility & localization
- [ ] Images include alt text.
- [ ] No hard-to-read color combinations in embedded diagrams.
- [ ] Any user-facing copy is phrased simply to aid future localization.

## Technical verification (minimal)
- [ ] Run local markdown preview and confirm links render.
tested: false
```powershell
# Preview docs locally (example)
npm install -g markserv
markserv docs --port 3000
Start-Sleep -Seconds 1
Start-Process "http://localhost:3000"
```
- [ ] Run repository link-checker (if present) or a simple script to validate internal links.
tested: false
```powershell
# Simple link-check example (requires PowerShell 7+)
Get-Content -Path (Get-ChildItem -Path docs -Recurse -Filter *.md | Select-Object -First 1).FullName
# tested: false — replace with project link-checker when available
```

## Security & privacy
- [ ] No secrets, API keys, or credentials committed.
- [ ] No leaked internal URLs or private data.
- [ ] Run `git secrets --scan` (or equivalent) and resolve findings.
- [ ] Replace any tokens with placeholders (e.g. `[API_KEY]`).

## Review readiness
- [ ] Add reviewers and request specific feedback (technical accuracy, writing, accessibility).
- [ ] Add labels: `docs`, `subagent` (if applicable), `needs-review`.
- [ ] Include a concise "How to test" section in PR description (commands, files to inspect).
- [ ] If the PR changes `subagents.yml`, add a short example run or expected artifact path.

## Post-merge
- [ ] If public docs changed, notify downstream teams or update any published pages.
- [ ] If changes require release notes, add an entry to CHANGELOG or release draft.

## Example "How to test" snippet (PowerShell)
tested: false
```powershell
# From repository root:
# 1) Preview docs
markserv docs --port 3000

# 2) Open preview in browser
Start-Process "http://localhost:3000"

# 3) Manual checks:
#   - Verify new subagent appears in docs/subagents.yml
#   - Click any new doc pages and confirm images load
```

## Reviewer checklist (for maintainers)
- [ ] Confirm acceptance criteria listed in `subagents.yml` are actionable and testable.
- [ ] Verify sample prompt reproduces a reasonable first draft or output.
- [ ] Confirm output_path is appropriate and non-conflicting.
- [ ] Validate documentation tone and target audience appropriateness.

## Merge criteria
- [ ] All required checks pass (CI, linters for docs if configured).
- [ ] At least one approving review from a docs owner or subject-matter expert.
- [ ] No unresolved high-severity comments.
