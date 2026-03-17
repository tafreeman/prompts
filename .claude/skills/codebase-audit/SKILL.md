---
name: codebase-audit
description: Parallel agent codebase audit. Spawns 5 specialized sub-agents to analyze dependencies, code quality, test coverage, API surface, best practice adherence, security, documentation, librarian practices, and performance — each writes findings to docs/audit/. Synthesizes a prioritized top-10 action plan.
---

# Codebase Audit

Comprehensive parallel architecture audit using specialized sub-agents. Each agent writes results to disk incrementally so partial results survive session limits.

## Trigger

Use when:
- User asks for "audit", "architecture review", "codebase analysis", "health check"
- Before major refactors or new feature planning
- Periodic maintenance reviews

## Setup

1. Create output directory: `mkdir -p docs/audit`
2. Record start time and current git SHA in `docs/audit/README.md`

## Parallel Agents (launch ALL 7 simultaneously)

### Agent 1: Dependency Analysis → `docs/audit/dependencies.md`
- Map all Python dependencies (pyproject.toml) and JS dependencies (package.json)
- Flag outdated packages (check latest versions)
- Flag known vulnerabilities if detectable
- Identify unused dependencies
- Check for version conflicts across packages

### Agent 2: Code Quality → `docs/audit/code-quality.md`
- Identify files over 800 lines (per coding standards)
- Find functions over 50 lines
- Detect duplicated logic across modules
- Flag deep nesting (>4 levels)
- Check for bare `except:` or `except Exception`
- Run ruff with full rule set and summarize top issues

### Agent 3: Test Coverage → `docs/audit/test-coverage.md`
- Run pytest with `--cov` for each Python package
- Identify modules with <80% coverage (the project gate)
- List untested public functions/classes
- Flag test files with no assertions
- Check for flaky test patterns (sleep, network calls without mocks)

### Agent 4: API Surface → `docs/audit/api-surface.md`
- Document all FastAPI endpoints (routes, methods, auth)
- Document all CLI commands and their options
- List all public protocol interfaces
- Check for inconsistencies (e.g., mixed response formats)
- Identify undocumented public APIs

### Agent 5: Performance → `docs/audit/performance.md`
- Flag synchronous I/O in async code paths
- Identify N+1 query patterns
- Check for unbounded list operations (no pagination)
- Flag heavy imports at module level
- Identify missing caching opportunities
- Check for blocking calls in event loops
- Flag any use of `time.sleep()` in async code
- Identify any use of `print()` for logging instead of proper logging framework
- Check for inefficient algorithms in critical code paths (e.g., O(n^2) where O(n log n) is possible)
 
### Agent 6: Security → `docs/audit/security.md`
- Check for hardcoded secrets (regex scan)
- Flag use of `eval`, `exec`, `pickle` with untrusted input
- Identify outdated dependencies with known vulnerabilities (cross-ref with Agent 1)
- Check for missing auth on API endpoints (cross-ref with Agent 4)
- Flag use of weak cryptography (e.g., MD5, SHA1)
- Check for CORS misconfigurations in FastAPI
- Identify any use of `os.system`, `subprocess` without proper sanitization
- Flag any use of `open()` on user-provided paths without validation
- Check for proper use of `Content-Security-Policy` headers in API responses
- Identify any use of `pickle` or `yaml` for deserialization of untrusted input
- Flag any use of `eval()` or `exec()` with untrusted input
- Check for hardcoded secrets in code (e.g., API keys, database passwords) using regex patterns
- Identify any use of `os.system()` or `subprocess` without proper sanitization of

### Agent 7: Documentation & Librarian Practices → `docs/audit/documentation.md`
- Check for missing or outdated docstrings on public functions/classes
- Verify README and other top-level documentation is up-to-date
- Identify orphaned modules with no documentation
- Check for consistent docstring style (e.g., Google, NumPy)
- Verify that code examples in docs are correct and runnable

## Synthesis

After all 7 agents complete:
1. Read all 7 agent reports
2. Cross-reference findings (e.g., untested code that also has quality issues = higher priority)
3. Write `docs/audit/summary.md` with:
   - Top 10 prioritized action items (CRITICAL → LOW)
   - Quick wins (fixable in <30 min)
   - Strategic items (require planning)
   - Metrics snapshot (coverage %, file count, dep count, endpoint count)

## Output Format

Each agent report uses this structure:
```markdown
# [Area] Audit — [date]
**Git SHA:** [sha]
**Status:** ✅ Healthy | ⚠️ Issues Found | 🔴 Critical

## Findings
### Critical
- ...
### High
- ...
### Medium
- ...

## Metrics
| Metric | Value | Gate | Status |
|--------|-------|------|--------|

## Recommendations
1. ...
```
