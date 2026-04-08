# Documentation Drift Report

Generated 2026-04-08 during documentation audit.

## Critical Drift (factual errors in high-visibility docs)

### 1. Root README.md — Workflow count inflated
- **Claims**: "10 production workflow definitions" (line 119), "10 YAML workflow definitions" (line 219)
- **Actual**: 6 YAML files in `agentic-workflows-v2/agentic_v2/workflows/definitions/`:
  `bug_resolution`, `code_review`, `conditional_branching`, `fullstack_generation`, `iterative_review`, `test_deterministic`
- **Action**: Update to 6; remove 4 phantom workflows from table (`deep_research`, `tdd_codegen_e2e`, `multi_agent_codegen_e2e`, `plan_implementation`)

### 2. Root README.md — Test file count stale
- **Claims**: "36 test files" (lines 235, 349)
- **Actual**: 78 `test_*.py` files in `agentic-workflows-v2/tests/`
- **Action**: Update count

### 3. Root README.md — Agent persona count
- **Claims**: "12 agent persona definitions (.md)" in CLAUDE.md
- **Actual**: 7 persona files (`architect`, `coder`, `orchestrator`, `planner`, `reviewer`, `tester`, `validator`)
- **Action**: Update CLAUDE.md persona count

### 4. .claude/README.md — Skills table incomplete
- **Claims**: "Skills (11)" with 11 entries in table
- **Actual**: 14 SKILL.md files. Missing from table: `codebase-audit`, `session-plan`, `test-fix`
- **Action**: Add 3 missing skills to table, update count to 14

### 5. .github/copilot-instructions.md — Tier model mismatch
- **Claims**: References tiers `tier0` to `tier3` only
- **Actual**: Root README documents tiers 0–5 (including Tier 4 Premium, Tier 5 Frontier)
- **Status**: Low priority — copilot-instructions may intentionally simplify

### 6. .github/copilot-instructions.md — Dead reference
- **Claims**: References `.github/instructions/prompts-repo.instructions.md`
- **Actual**: File does not exist at that path
- **Action**: Remove or fix reference

## Moderate Drift (inconsistencies between sibling docs)

### 7. Root README.md vs agentic-workflows-v2/README.md — Workflow lists disagree
- Root lists 8 workflows in table; subproject lists 6
- Both are wrong; actual count is 6 YAML files

### 8. .claude/rules/ vs .github/copilot-instructions.md — Duplication
- Coding style, immutability, formatting, testing rules are duplicated between the two surfaces
- **Canonical home**: `.claude/rules/` (machine-loaded); copilot-instructions summarizes for Copilot surface
- **Status**: Intentional duplication for dual-surface support; no action needed but noted

### 9. docs/README.md — `tested: false` markers in PowerShell examples
- Lines 59, 67 contain raw `tested: false` strings above code blocks
- These are metadata leaking into rendered content
- **Action**: Remove or convert to HTML comments

### 10. CLAUDE.md — Agent persona count
- **Claims**: "12 agent persona definitions (.md)" under agentic_v2/prompts/
- **Actual**: 7 persona .md files
- **Action**: Update to 7

### 11. CLAUDE.md — Test file count
- **Claims**: "74 files, ~1456 tests"
- **Actual**: 78 test_*.py files (count may have grown)
- **Action**: Update to 78+

## Contradictions Between .claude/rules/ and Docs

### 12. Security: AI-generated code review (unique to .claude/rules/)
- `common/security.md` treats Claude/Copilot output as "untrusted input" requiring full review
- This guidance does NOT appear in `.github/copilot-instructions.md` (understandable — Copilot wouldn't instruct distrust of itself)
- **Status**: Noted, no contradiction — different audience

### 13. Windows environment guidance (unique to root CLAUDE.md)
- Root CLAUDE.md specifies Windows PowerShell as primary environment
- `.claude/rules/` does not reference Windows-specific guidance
- **Status**: Correct separation — CLAUDE.md is environment config, rules are coding standards
