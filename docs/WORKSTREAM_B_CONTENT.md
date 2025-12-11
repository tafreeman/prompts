# 🔧 Workstream B: Content & Technical Improvements

**Created:** December 4, 2025  
**Focus:** Missing content, documentation, tooling, templates  
**Estimated Effort:** ~10 hours  
**Parallel Safe:** ✅ Yes - No overlap with Workstream A

---

## 🎯 Scope

This workstream covers all **content and technical** improvements:
- Missing sections in prompts (Variables, Tips, Examples)
- README and documentation fixes
- Template creation
- Directory structure
- Evaluation tooling

**Does NOT include:** Formatting, visual styling, navigation fixes (those are in Workstream A)

---

## 🔴 CRITICAL (Do First)

### B1. Fix README Architecture Mismatch
**Effort:** 30 minutes  
**Impact:** Misleads users about available features

**Problem:** README.md describes components that don't exist:
- `src/app.py` (Flask application) - ❌ Doesn't exist
- `src/templates/` - ❌ Doesn't exist  
- `deployment/` directory - ❌ Doesn't exist

**Action:** Update README.md to either:
1. Remove references to non-existent webapp components
2. Mark webapp section as "🔮 Planned" with link to `docs/PROMPT_WEB_APP_ARCHITECTURE.md`

**Files to check:**
- `README.md` (root)
- `docs/README.md`

---

### B2. Add Missing Standard Sections (10 files)
**Effort:** 2 hours  
**Impact:** Incomplete prompts confuse users

| File | Missing Sections | Priority |
|:-----|:-----------------|:--------:|
| `prompts/advanced/library.md` | Description, Variables, Example, Tips | 🔴 High |
| `prompts/advanced/prompt-library-refactor-react.md` | Variables, Example | 🔴 High |
| `prompts/advanced/chain-of-thought-guide.md` | Variables, Tips | 🟠 Medium |
| `prompts/analysis/library-capability-radar.md` | Variables, Tips | 🟠 Medium |
| `prompts/analysis/library-network-graph.md` | Variables, Tips | 🟠 Medium |
| `prompts/analysis/library-structure-treemap.md` | Variables, Tips | 🟠 Medium |
| `prompts/system/example-research-output.md` | Description, Prompt, Variables, Tips | 🔴 High |
| `prompts/system/frontier-agent-deep-research.md` | Tips | 🟢 Low |
| `prompts/system/m365-copilot-research-agent.md` | Tips | 🟢 Low |
| `prompts/system/office-agent-technical-specs.md` | Tips | 🟢 Low |

**Template for Variables section:**
```markdown
## Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `[variable_name]` | What this variable represents | Example value |
```text
**Template for Tips section:**
```markdown
## Tips

- **Be specific**: Provide detailed context for better results
- **Iterate**: Refine the output by asking follow-up questions
- **Customize**: Adjust the tone and format to match your needs
```text
---

### B3. Create Simplified Quick Start Template
**Effort:** 1 hour  
**Impact:** Current 17-section template intimidates new contributors

**Create:** `templates/prompt-template-minimal.md`

**Content:**
```markdown
---
title: "[Prompt Title]"
description: "[One-line description]"
category: "[business|developers|creative|analysis|governance|m365|advanced]"
---

# [Prompt Title]

## Description

[2-3 sentences explaining what this prompt does and when to use it]

## Prompt

```text
[The actual prompt text with [variables] in brackets]
```text
## Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `[variable]` | Description | Example value |

## Example Usage

### Input
```text
[Prompt with variables filled in]
```text
### Output
```text
[Expected AI response]
```text
```sql
---

## 🟠 HIGH PRIORITY

### B4. Create Missing Referenced Prompts (Optional)
**Effort:** 3-4 hours  
**Impact:** Depends on whether these prompts should exist

**Prompts referenced but don't exist:**

| Referenced File | Referenced From | Action |
|:----------------|:----------------|:------:|
| `reflection-code-review-self-check.md` | chain-of-thought-debugging.md | Create or Remove link |
| `react-codebase-navigator.md` | chain-of-thought-debugging.md | Create or Remove link |
| `tree-of-thoughts-decision-guide.md` | chain-of-thought-guide.md | Create or Remove link |
| `rag-code-ingestion.md` | rag-document-retrieval.md | Create or Remove link |
| `rag-citation-framework.md` | rag-document-retrieval.md | Create or Remove link |
| `project-charter-creator.md` | agile-sprint-planner.md | Create or Remove link |
| `swot-analysis.md` | competitive-intelligence-researcher.md | Create or Remove link |

**Decision:** For each, determine if the prompt SHOULD exist:
- If yes → Create it using the minimal template
- If no → Remove the link (handled in Workstream A)

---

### B5. Update Category Index Files
**Effort:** 1 hour  
**Impact:** Category landing pages may be outdated

**Files to review and update:**
- `prompts/advanced/index.md`
- `prompts/analysis/index.md`
- `prompts/business/index.md`
- `prompts/creative/index.md`
- `prompts/developers/index.md`
- `prompts/governance/index.md`
- `prompts/m365/index.md`
- `prompts/system/index.md`

**For each:**
1. Verify all listed prompts actually exist
2. Add any prompts that exist but aren't listed
3. Update descriptions if needed
4. Ensure consistent formatting

---

## 🟡 MEDIUM PRIORITY

### B6. Flatten Deep Directory Structure
**Effort:** 2 hours  
**Impact:** 76 directories make navigation confusing

**Directories to consolidate:**

| Current Location | Move To |
|:-----------------|:--------|
| `techniques/reflexion/*.md` | `prompts/advanced/` |
| `techniques/context-optimization/*.md` | `prompts/advanced/` |
| `techniques/meta-prompting/*.md` | `prompts/advanced/` |

**After moving:**
1. Update any internal links
2. Delete empty directories
3. Update index files

---

### B7. Run Full Library Evaluation
**Effort:** 1-2 hours (API time)  
**Impact:** Get current quality scores

**Command:**
```bash
python testing/evals/dual_eval.py prompts/ \
  --format json \
  --output docs/EVALUATION_RESULTS.json \
  --runs 1 \
  --models openai/gpt-4o-mini
```sql
**After running:**
1. Review results for lowest-scoring prompts
2. Prioritize improvements based on scores
3. Update quality tracking in consolidated plan

---

### B8. Create Validation Scripts
**Effort:** 1 hour  
**Impact:** Automate quality checks

**Create:** `tools/validate_prompts.py`

```python
#!/usr/bin/env python3
"""Validate prompt files for required sections and frontmatter."""

import re
import sys
from pathlib import Path
import yaml

REQUIRED_SECTIONS = ['Description', 'Prompt', 'Variables', 'Example']
REQUIRED_FRONTMATTER = ['title', 'description']

def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}

def extract_sections(content: str) -> list:
    """Extract H2 section headers from markdown content."""
    return re.findall(r'^## (.+)$', content, re.MULTILINE)

def validate_file(path: Path) -> list:
    """Validate a single prompt file. Returns list of issues."""
    issues = []
    content = path.read_text(encoding='utf-8')
    
    # Check frontmatter
    fm = extract_frontmatter(content)
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            issues.append(f"Missing frontmatter: {field}")
    
    # Check sections
    sections = extract_sections(content)
    for section in REQUIRED_SECTIONS:
        if section not in sections and section.lower() not in [s.lower() for s in sections]:
            issues.append(f"Missing section: {section}")
    
    return issues

def main():
    errors = 0
    for path in Path("prompts").rglob("*.md"):
        if path.name in ['index.md', 'README.md']:
            continue
        
        issues = validate_file(path)
        if issues:
            print(f"\n{path}:")
            for issue in issues:
                print(f"  - {issue}")
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"Files with issues: {errors}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
```text
---

### B9. Create Link Checker Script
**Effort:** 30 minutes  

**Create:** `tools/check_links.py`

```python
#!/usr/bin/env python3
"""Check for broken internal links in markdown files."""

import re
import sys
from pathlib import Path

def check_links(path: Path) -> list:
    """Check internal links in a markdown file. Returns broken links."""
    broken = []
    content = path.read_text(encoding='utf-8')
    
    # Find markdown links
    links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
    
    for text, link in links:
        if link.startswith('http'):
            continue
        
        # Resolve relative path
        target = (path.parent / link).resolve()
        if not target.exists():
            broken.append((text, link))
    
    return broken

def main():
    errors = 0
    for path in Path("prompts").rglob("*.md"):
        broken = check_links(path)
        if broken:
            print(f"\n{path}:")
            for text, link in broken:
                print(f"  - [{text}]({link})")
            errors += len(broken)
    
    print(f"\n{'='*50}")
    print(f"Total broken links: {errors}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
```text
---

## 🟢 LOW PRIORITY

### B10. Add GitHub Action for PR Validation
**Effort:** 30 minutes  

**Create:** `.github/workflows/validate-prompts.yml`

```yaml
name: Validate Prompts

on:
  pull_request:
    paths:
      - 'prompts/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Validate prompt structure
        run: python tools/validate_prompts.py
      
      - name: Check internal links
        run: python tools/check_links.py
```text
---

### B11. Document Contribution Guidelines
**Effort:** 1 hour  

**Update:** `CONTRIBUTING.md`

Add sections for:
1. How to create a new prompt (link to minimal template)
2. Required sections checklist
3. Frontmatter requirements
4. How to test locally
5. PR checklist

---

## ✅ Completion Checklist

| Task | Status | Files | Notes |
|:-----|:------:|------:|:------|
| B1. Fix README mismatch | ⬜ | 2 | Remove or mark planned |
| B2. Add missing sections | ⬜ | 10 | Use templates provided |
| B3. Create minimal template | ⬜ | 1 | New file |
| B4. Create missing prompts | ⬜ | 7 | Optional - decide first |
| B5. Update index files | ⬜ | 8 | Review each category |
| B6. Flatten directories | ⬜ | ~10 | Move then delete |
| B7. Run evaluation | ⬜ | All | Needs API access |
| B8. Create validate script | ⬜ | 1 | New tool |
| B9. Create link checker | ⬜ | 1 | New tool |
| B10. Add GitHub Action | ⬜ | 1 | New workflow |
| B11. Update CONTRIBUTING | ⬜ | 1 | Add prompt guidelines |

---

## 📊 Success Metrics

| Metric | Before | Target |
|:-------|:------:|:------:|
| Files missing required sections | 10 | 0 |
| README accuracy | ~60% | 100% |
| Validation scripts | 0 | 2 |
| GitHub Actions for prompts | 0 | 1 |
| Template options | 1 | 2 |

---

## 🔄 Coordination Notes

**No conflicts with Workstream A because:**
- Workstream A: Changes formatting/structure WITHIN files
- Workstream B: Creates new files, adds content sections

**If creating new prompts (B4):**
- Create with proper structure so Workstream A doesn't need to fix them
- Use the minimal template from B3

**Communication points:**
- If B6 (flatten directories) moves files, notify A team to skip those files
- If B4 creates prompts referenced by broken links, notify A team

---

*Workstream B — Content & Technical Focus — December 4, 2025*
