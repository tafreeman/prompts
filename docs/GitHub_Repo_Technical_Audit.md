# GitHub Repository Technical Audit: `tafreeman/prompts`

**Audit Date:** February 25, 2026  
**Scope:** Full local filesystem review (`D:\source\prompts`) — includes committed code, gitignored files, and local-only artifacts  
**Purpose:** Identify issues that would raise red flags for technical hiring managers at Anthropic, OpenAI, or hyperscaler federal divisions

---

## Executive Summary

The repository demonstrates **real architectural depth** — a DAG-based workflow engine with Kahn's algorithm scheduling, rubric-based evaluation scoring, LangGraph integration, and a full FastAPI+React UI. This is substantially above typical portfolio work. However, **14 issues** ranging from critical security exposure to cosmetic cleanup would significantly undermine a technical reviewer's first impression. Most fixes require < 30 minutes each.

**Verdict:** Strong foundation. Needs a focused cleanup sprint before sharing with hiring managers.

---

## 🔴 CRITICAL (Fix Immediately)

### 1. Live API Keys in `.env` — Credential Exposure Risk

**What I found:** Your `.env` file contains **live, plaintext API keys**:
- `GITHUB_TOKEN=github_pat_11ARMNHYA0yfNc2gP2VFaG_...`
- `HF_TOKEN=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`
- `OPENAI_API_KEY=sk-svcacct-pCGENBdD9FgHVkZJD1oEGIb...`
- `AZURE_OPENAI_API_KEY_0=5hcedZbCJBzXlYq7dGWBuL1l...`
- `AZURE_AI_SERVICES_ENDPOINT=5hcedZbCJBzXlYq7dGWBuL1l...`

**Mitigating factor:** `.env` is in `.gitignore` and `.env.example` is clean. So these are NOT pushed to GitHub.

**Remaining risk:** If `.env` was **ever** committed historically (even briefly), secrets are in git reflog. Also, any fork/clone of your local machine captures them.

**Action required:**
1. Run `git log --all --full-history -- .env` to verify it was never committed
2. **Rotate all keys immediately** regardless — treat as compromised since they've been read by this session
3. Consider using a secrets manager (Azure Key Vault, 1Password CLI) instead of `.env` for production keys

---

### 2. Scratch/Debug Files Committed to Repo Root

**Files that should NOT be in the repo:**

| File | What It Is | Signal to Reviewer |
|------|-----------|-------------------|
| `output.txt` | Model discovery JSON dump (2026-02-17) | Debug artifact left in repo |
| `output44.json` | Another discovery dump (2026-02-21) | Worse — numbered iteration |
| `output44.jsonooojko.json` | Typo'd filename | Looks like keyboard mash |
| `output44.jsonoooo.json` | Another typo'd filename | Severe code hygiene issue |
| `follow.txt` | Agent factory docstring fragment | Random snippet committed |
| `folder_report.txt` | Directory analysis log | Dev tooling output |
| `directory_analysis.log` | Same | Same |
| `prompts.sln` | Visual Studio Solution file | Confusing in 91% Python repo |
| `ANALYSIS.md`, `REVIEW.md`, `REFACTORING_PLAN.md` | Internal planning docs | Fine locally, messy in public repo |
| `system.md` | Unknown system doc | Clutters root |
| `chatlg.md` (in agentic-v2-eval) | Chat log | Debug artifact |

**Impact:** A hiring manager spends ~30 seconds on the repo landing page. Seeing `output44.jsonooojko.json` in the root immediately signals "this person doesn't clean up after themselves." This is the single highest-impact cosmetic fix.

**Action:**
```bash
# Remove from git tracking (keeps local copies)
git rm --cached output.txt output44.json "output44.jsonooojko.json" "output44.jsonoooo.json" follow.txt folder_report.txt directory_analysis.log prompts.sln ANALYSIS.md REVIEW.md REFACTORING_PLAN.md system.md
# Add to .gitignore
echo -e "output*.txt\noutput*.json\nfollow.txt\nfolder_report.txt\ndirectory_analysis.log\n*.sln\nANALYSIS.md\nREVIEW.md\nREFACTORING_PLAN.md\nsystem.md" >> .gitignore
git add .gitignore && git commit -m "chore: remove scratch/debug artifacts from tracking"
git push
```

---

### 3. `.aider.conf.yml` Committed — AI-Generated Code Signal

**What it is:** Configuration file for the Aider AI coding assistant.

**Why this matters for AI company applications:** This is a neon sign saying "AI tool wrote portions of this codebase." When applying to Anthropic or OpenAI, they want evidence **you** built this. Aider config in the repo makes every line of code ambiguous — did you design the DAG executor, or did Aider scaffold it?

**Action:**
```bash
git rm --cached .aider.conf.yml
echo ".aider.conf.yml" >> .gitignore
git commit -m "chore: remove aider config from tracking"
```

**Interview prep:** Be ready to explain: "I used Aider for rapid prototyping of boilerplate, but I designed the architecture — the DAG executor with Kahn's algorithm, the rubric-based scoring system, the tier-routing model, and the workflow YAML schema. Here's how the scoring handles edge cases..." Then walk through `scorer.py` or `dag_executor.py` line by line.

---

## 🟡 HIGH PRIORITY (Fix Before Sharing)

### 4. 8 Contributors on a "Personal Portfolio" Project

**Problem:** GitHub shows 8 contributors. If this is your proof-of-work for AI engineering skills, a reviewer will ask: "Who built what?" 

**Scenarios:**
- If contributors are bot accounts (Aider, Dependabot, GitHub Actions bots) → Explainable but still misleading
- If they're real collaborators → Must be precise about which components you own
- If they're variations of your own account → Clean up

**Action:** Either add a `CONTRIBUTORS.md` explaining roles, or add a section to README: "Architecture, core runtime, and evaluation framework designed and primarily implemented by Andy Freeman. CI/CD and dependency management assisted by automated tooling."

---

### 5. README (Root) Too Sparse for Portfolio Use

**Current state:** Basic directory listing with component descriptions. Functional but not impressive.

**What's missing that your code actually demonstrates:**
- No architecture diagram (even ASCII)
- No description of the design problems you solved
- No example of running the eval framework
- No mention of 10 workflow definitions or what they do
- No performance data or eval results
- No screenshots of the React UI

**The code is genuinely good — the README doesn't sell it.** A technical reviewer spends 30 seconds on README before deciding whether to look deeper. Right now, your README says "here are some directories" when it should say "here's a production-grade multi-agent workflow engine with DAG-based execution, model-tier routing, YAML-defined workflows, rubric-based evaluation scoring, and a live React dashboard."

**Recommended README structure:**
1. One-paragraph overview: what it is, why it exists, what problems it solves
2. Architecture diagram (Mermaid or ASCII showing Runtime → DAG Engine → Model Tiers → Eval)
3. Key design decisions (why DAG over pipeline, why YAML workflow definitions, why rubric-based scoring)
4. Quick demo: `agentic run code_review --dry-run` with output
5. Eval framework: how scoring works, sample rubric, sample result
6. Links to deeper docs in subdirectories

---

### 6. No GitHub Repo Description, Topics, or Website

**Current state:** "No description, website, or topics provided"

**Impact:** Repo is invisible in GitHub search. Not indexed for discovery. Free SEO completely unused.

**Action (60 seconds in GitHub Settings):**
- **Description:** "Multi-agent AI workflow engine with DAG execution, model-tier routing, YAML workflow definitions, and rubric-based LLM evaluation"
- **Website:** Your LinkedIn URL
- **Topics:** `agentic-ai`, `multi-agent-systems`, `llm-evaluation`, `workflow-orchestration`, `python`, `langchain`, `langgraph`, `prompt-engineering`

---

### 7. No Releases or Tags

**Current:** 0 releases, 0 packages, 229 commits.

**Signal:** "Experiment in progress" vs. "shippable software." Even a `v0.1.0` tag elevates perception from hobby to project.

**Action:**
```bash
git tag -a v0.1.0 -m "Initial release: DAG workflow engine, eval framework, 10 workflow definitions"
git push origin v0.1.0
```
Then create a GitHub Release from the tag with a brief changelog.

---

### 8. `.gitignore` is Bloated with Specific File Paths

Your `.gitignore` is **~250 lines** and contains dozens of individual file paths like:
```
multiagent-workflows/dashboard_data/run_architecture_evolution_20260127_013620.json
multiagent-workflows/dashboard_data/run_bug_fixing_20260127_013645.json
...
```

This suggests files were committed, then individually gitignored after the fact. It's a pattern reviewers recognize as reactive cleanup rather than proactive hygiene.

**Action:** Replace specific file paths with glob patterns:
```
multiagent-workflows/dashboard_data/*.json
```

---

## 🟢 POSITIVE SIGNALS (What's Working)

These are the things a technical reviewer would be impressed by:

### Architecture Quality
- **DAG Executor (`dag_executor.py`):** Clean implementation of Kahn's algorithm with `asyncio.wait(FIRST_COMPLETED)` for true parallel scheduling, cascade skip on failure, deadlock detection, max concurrency limits, and SSE/WebSocket event streaming. This is production-grade concurrent systems design.
- **Orchestrator Agent (`orchestrator.py`):** Capability-based agent matching with scored selection, dependency-aware subtask scheduling, both DAG and legacy pipeline execution paths. Shows software architecture maturity.
- **Smart Model Router (`smart_router.py`):** Health-weighted selection, adaptive cooldowns with exponential backoff, circuit breaker pattern, cost-aware routing, stats persistence. Enterprise-level resilience patterns.
- **Scorer (`scorer.py`):** Clean, well-documented rubric-based scoring with YAML-driven criteria, weighted normalization, clamping, and missing-criteria tracking. Good separation of concerns.

### Code Quality
- **Type annotations throughout** — `dict[str, float]`, `Optional[str]`, `list[dict[str, Any]]` — consistent modern Python 3.11+ style
- **Dataclasses used correctly** — frozen where appropriate, field factories, clean defaults
- **Custom exception hierarchy** — `MissingDependencyError`, `CycleDetectedError` with structured attributes
- **Docstrings** — Google-style with Args/Returns/Raises sections, examples in key classes
- **Pre-commit hooks** — black, isort, ruff, mypy, docformatter, pydocstyle — full professional toolchain

### Testing
- **35+ test files** across both packages covering:
  - Unit tests: DAG, scoring, normalization, expressions, contracts, model routing
  - Integration tests: agents, LangChain engine, server routes, workflows
  - Eval-specific: rubrics, adapters, benchmarks, quality evaluators, sandbox
- **pytest + pytest-asyncio + pytest-cov** — proper async test infrastructure
- **Fixtures directory** with test data — not mocking everything, testing real behavior

### Project Structure
- **Monorepo with independent packages** — `agentic-workflows-v2` and `agentic-v2-eval` each have their own `pyproject.toml`, README, tests, docs
- **10 YAML workflow definitions** — deep_research, code_review, bug_resolution, tdd_codegen, fullstack_generation, multi_agent_codegen_e2e — shows breadth
- **`.env.example`** with rate limit documentation — thoughtful developer experience
- **CLAUDE.md** with code quality standards — shows you think about engineering process, not just code
- **Community health files** — CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md, SUPPORT.md, LICENSE (MIT)

### Scale
- **229 commits** — sustained effort, not a weekend hack
- **pyproject.toml with hatchling** — modern Python packaging
- **Optional dependency groups** — `[dev]`, `[server]`, `[langchain]`, `[tracing]`, `[claude]` — professional extras management
- **CLI entry point** — `agentic` command registered in pyproject.toml scripts

---

## 📋 COMPLETE FIX CHECKLIST (Priority Order)

| # | Fix | Time | Impact |
|---|-----|------|--------|
| 1 | Rotate all API keys (`.env` was read) | 15 min | Security |
| 2 | `git rm --cached` all scratch files from root | 10 min | First impression |
| 3 | Remove `.aider.conf.yml` from tracking | 2 min | AI company optics |
| 4 | Add repo description + topics in GitHub Settings | 2 min | Discoverability |
| 5 | Rewrite root README with architecture, design decisions, demo | 60 min | Highest leverage |
| 6 | Add `CONTRIBUTORS.md` or explain 8 contributors | 10 min | Credibility |
| 7 | Create v0.1.0 release tag | 5 min | Polish |
| 8 | Clean up `.gitignore` — replace file paths with globs | 15 min | Hygiene |
| 9 | Verify `.env` was never in git history | 5 min | Security |
| 10 | Consider `git filter-branch` or BFG to scrub scratch files from history | 30 min | Thoroughness |
| 11 | Add CI badge to README (if GitHub Actions configured) | 5 min | Credibility |
| 12 | Remove `chatlg.md` from `agentic-v2-eval` | 2 min | Cleanup |
| 13 | Prepare Aider usage talking points for interviews | 20 min | Interview prep |
| 14 | Add screenshot of React UI to README | 10 min | Visual proof |

**Estimated total cleanup time: ~3 hours**

---

## Code Quality Deep Dive

### Strengths by Component

**DAG Engine** — The `dag_executor.py` is the crown jewel. Kahn's algorithm with `asyncio.FIRST_COMPLETED`, cascade failure propagation, deadlock detection, and observable event streaming is exactly what Anthropic's infrastructure teams build. If you can walk through this code line-by-line in an interview, it demonstrates concurrent systems thinking that's hard to fake.

**Evaluation Scorer** — `scorer.py` is clean and well-tested. The weighted normalization with clamping and missing-criteria handling shows you've thought about real-world eval edge cases (what happens when a criterion is absent? what about out-of-range scores?). This directly maps to Anthropic's eval infrastructure.

**Workflow YAML Schema** — 10 workflow definitions with `capabilities`, `inputs`, typed fields, `depends_on`, `when` conditions, and `loop_until` expressions. This is a real DSL, not toy config. The `deep_research.yaml` with ToT planning, ReAct retrieval, CoVe verification, and RAG packaging shows you understand the research agent pattern space.

**LangGraph Integration** — `graph.py` compiles YAML configs into LangGraph StateGraphs with conditional edges, loop edges, and tier-0 deterministic steps. This bridges your runtime abstraction to the LangChain ecosystem, which is the right architectural choice for extensibility.

### Areas for Improvement

**`_call_model` in Orchestrator** — Currently returns hardcoded JSON. Even a `raise NotImplementedError("Subclass must implement")` would be better than a silent stub that masks integration state.

**Some "Aggressive design improvements" comments** — Several modules have docstrings like "Aggressive design improvements: ..." which reads like Claude/Aider-generated commentary rather than your architectural voice. Consider rewriting these to be more specific and personal.

**`_discovery` directory in root** — Unclear purpose, adds clutter.

**`prompts_tools.egg-info/` in root** — Build artifact that should be gitignored (it's in .gitignore but still tracked).

---

## Interview Readiness Assessment

**If asked "Walk me through the architecture":**
You can point to: YAML workflow definitions → LangGraph compiler (`graph.py`) → DAG executor with Kahn's scheduling (`dag_executor.py`) → Smart model router with circuit breakers (`smart_router.py`) → Rubric-based eval scoring (`scorer.py`). This is a coherent, multi-layered system.

**If asked "What's the hardest technical problem you solved?":**
The DAG executor's handling of failure propagation with cascade skip, combined with the async concurrency model using `asyncio.wait(FIRST_COMPLETED)`, is a strong answer. It's a real distributed systems pattern applied to AI workflow orchestration.

**If asked "Did you use AI tools to build this?":**
Be honest. "I used Aider for scaffolding and boilerplate. I designed the architecture — the DAG execution model, the tier-routing scheme, the evaluation rubric system, and the YAML workflow DSL. I can walk you through any module." Then demonstrate by explaining `dag_executor.py` or `scorer.py` internals.

**If asked "Why isn't this a pip-installable package on PyPI?":**
"It's structured for it — `pyproject.toml` with hatchling, CLI entry point registered, optional dependency groups. Publishing to PyPI is on the roadmap." (Consider actually publishing — takes 10 minutes and dramatically elevates perception.)
