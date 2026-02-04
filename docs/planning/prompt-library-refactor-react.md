---
title: "ReAct: Architecture Plan Validator"
shortTitle: "Plan Validator ReAct"
intro: "ReAct-based prompt for reading implementation plans, validating architecture decisions, and recommending optimizations for multi-model agentic workflows."
type: "how_to"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "architecture"
  - "validation"
  - "agentic-workflows"
  - "model-routing"
author: "Prompt Library Team"
version: "5.0"
date: "2026-02-02"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# ReAct: Architecture Plan Validator

---

## Description

This is an executable ReAct (Reasoning + Acting) prompt for **validating architecture plans** before implementation. Use this prompt to:

1. Read and understand proposed implementation plans
2. Validate architecture decisions against best practices
3. Identify gaps, risks, and over-engineering
4. Recommend optimizations for your specific use case
5. Validate model tier assignments for cost/performance balance

## Goal

Perform systematic validation of an architecture plan to ensure it:

1. **Fits the use case** - Right-sized for actual requirements (not over-engineered)
2. **Optimizes model usage** - Smaller models where possible, large models only when needed
3. **Minimizes complexity** - Fewest moving parts that still meet requirements
4. **Enables incremental delivery** - Phased approach with early value
5. **Avoids common pitfalls** - Anti-patterns, premature abstractions, etc.

---

## Plan Context: Agentic Workflows v2

> **Current Plans Under Review:**
> - `docs/planning/agentic-workflows-v2-architecture.md` - Full architecture
> - `docs/planning/agentic-workflows-v2-implementation-patterns.md` - Code patterns
> - `docs/planning/agentic-workflows-v2-phased-implementation.md` - Phased plan with model tiers

### Proposed Architecture Summary

```
agentic-workflows/
├── contracts/          # Pydantic schemas for inter-agent messages
├── tools/              # Tool system with auto-discovery
│   └── builtin/        # File ops, code tools, search
├── agents/             # Agent implementations
│   └── implementations/  # Architect, Coder, Reviewer, etc.
├── engine/             # Orchestration
│   └── patterns/       # Sequential, Parallel, Iterative, Self-Refine
├── workflows/          # YAML workflow definitions
├── models/             # LLM integration + routing
├── evaluation/         # Quality scoring
└── cli/                # Command-line interface
```

### Proposed Model Tiering

| Tier | Model Size | Cost | Tasks |
|------|------------|------|-------|
| **0** | None | Free | File copy, template render, JSON transform |
| **1** | 1-3B | Cheap | Code formatting, docstrings, validation |
| **2** | 7-14B | Moderate | Code generation, review, testing |
| **3** | 32B+/Cloud | Expensive | Architecture, complex reasoning, evaluation |

---

## Validation Framework

### Decision Criteria Matrix

For each architecture decision, evaluate:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Necessity** | Is this component actually needed for MVP? | High |
| **Complexity** | Does added complexity justify the benefit? | High |
| **Model Fit** | Is the right model tier assigned? | High |
| **Alternatives** | Are there simpler approaches? | Medium |
| **Dependencies** | Does this create tight coupling? | Medium |
| **Testability** | Can this be tested in isolation? | Medium |
| **Incremental** | Can this be delivered incrementally? | Low |

### Common Anti-Patterns to Check

| Anti-Pattern | Description | Red Flag |
|--------------|-------------|----------|
| **Premature Abstraction** | Building flexibility before knowing needs | "Registry", "Factory", "Plugin system" for < 3 items |
| **Over-Tiering** | Too many model tiers with unclear boundaries | More than 3-4 tiers |
| **Kitchen Sink** | Including everything "just in case" | Features with no clear user story |
| **Enterprise Creep** | Adding enterprise features before product-market fit | "RBAC", "Audit logs", "Multi-tenancy" too early |
| **Parallel Paths** | Multiple ways to do the same thing | Both YAML and Python workflow definitions |
| **Abstraction Inversion** | Abstracting low-level, hardcoding high-level | Generic tool system but hardcoded workflow steps |

---

## Architecture Validation Checklist

### Phase 0: Foundation (No LLM)

- [ ] **Q1**: Are Tier 0 tools truly LLM-free? (file ops, templates, JSON)
- [ ] **Q2**: Is the tool registry over-engineered for the number of tools?
- [ ] **Q3**: Do we need auto-discovery or would explicit registration suffice?

### Phase 1: Contracts & Small Models

- [ ] **Q4**: Are Pydantic contracts necessary, or would simple dicts work?
- [ ] **Q5**: Is Tier 1 (small models) actually useful, or should we jump to Tier 2?
- [ ] **Q6**: What's the cost difference between Tier 1 and Tier 2 for simple tasks?

### Phase 2: Core Engine

- [ ] **Q7**: Do we need a full "executor" abstraction or direct agent calls?
- [ ] **Q8**: Is state management/checkpointing needed for MVP?
- [ ] **Q9**: How many agents do we actually need vs. plan to build?

### Phase 3: Orchestration

- [ ] **Q10**: Do we need all 4 patterns (sequential, parallel, iterative, self-refine)?
- [ ] **Q11**: Which pattern addresses the primary use case?
- [ ] **Q12**: Can we start with 1 pattern and add others later?

### Phase 4: Large Models

- [ ] **Q13**: What specifically requires Tier 3 (large models)?
- [ ] **Q14**: Can evaluation be done with Tier 2 models instead?
- [ ] **Q15**: Is the "Architect" agent needed, or can humans provide architecture?

### Cross-Cutting

- [ ] **Q16**: What's the actual MVP - what's the smallest thing that delivers value?
- [ ] **Q17**: What existing code can be reused vs. rewritten?
- [ ] **Q18**: What's the testing strategy for each tier?

---

## ReAct Validation Loop

Execute validation using iterative Thought → Action → Observation cycles:

### Phase 1: Read and Understand Plans

**Thought**: I need to read all related planning documents to understand the full proposal.

**Action**: Load all architecture documents
```text
read_file("docs/planning/agentic-workflows-v2-architecture.md")
read_file("docs/planning/agentic-workflows-v2-implementation-patterns.md")
read_file("docs/planning/agentic-workflows-v2-phased-implementation.md")
```

**Observation**: Document key decisions, component count, and complexity indicators.

---

### Phase 2: Map Current State

**Thought**: I need to understand what already exists before validating new additions.

**Action**: Analyze existing codebase
```text
list_dir("multiagent-workflows/src/")
list_dir("tools/")
grep_search("class.*Agent", includePattern="**/*.py")
grep_search("def execute", includePattern="**/*.py")
```

**Observation**: Create inventory of existing components that could be reused.

---

### Phase 3: Identify Primary Use Case

**Thought**: Architecture should be driven by use cases, not abstractions.

**Action**: Find user stories and requirements
```text
grep_search("use case|user story|requirement", includePattern="**/*.md")
read_file("README.md")  # Often contains primary use case
```

**Observation**: Document the PRIMARY use case this architecture serves.

---

### Phase 4: Validate Model Tier Assignments

**Thought**: Model tiers should be based on actual task complexity, not assumptions.

**Action**: Analyze task-to-tier mapping
```text
# For each proposed Tier 1 task, ask:
# - Has this been tested with a 1-3B model?
# - What's the quality difference vs Tier 2?
# - What's the cost difference?

# For each proposed Tier 3 task, ask:
# - Can this be done with Tier 2?
# - What specific capability requires 32B+?
```

**Observation**: Create validated tier mapping with justifications.

---

### Phase 5: Simplification Analysis

**Thought**: What can be removed or simplified without losing core value?

**Action**: Apply YAGNI (You Aren't Gonna Need It) analysis
```text
# For each component, ask:
# 1. Does MVP need this?
# 2. Can it be added later without major refactoring?
# 3. What's the cost of including it now vs. later?
```

**Observation**: Create "defer list" of components to build later.

---

### Phase 6: Alternative Architecture

**Thought**: Is there a simpler architecture that meets the same goals?

**Action**: Sketch minimal viable architecture
```text
# Minimal architecture might be:
# 1. Single orchestrator (no patterns abstraction)
# 2. Direct LLM calls (no model router for < 3 models)
# 3. Dict-based messages (no Pydantic until validation fails)
# 4. File-based state (no checkpoint system)
```

**Observation**: Compare complexity of proposed vs. minimal architecture.

---

## Deliverables

### 1. Architecture Validation Report

```markdown
## Architecture Validation Report

**Plan Reviewed**: [Plan name and version]
**Reviewer**: [AI Assistant]
**Date**: [Date]

### Executive Summary
[1-2 paragraph summary of findings]

### Validation Results

| Component | Verdict | Rationale |
|-----------|---------|-----------|
| Tool Registry | ✅ Keep | Auto-discovery useful for 10+ tools |
| Model Router | ⚠️ Simplify | Only 3 models - use dict mapping |
| Pydantic Contracts | ⚠️ Defer | Start with dicts, add validation when bugs occur |
| State Checkpointing | ❌ Remove | Not needed for < 5 min workflows |
| ... | ... | ... |

### Recommended Changes
1. [Change 1]
2. [Change 2]
...

### Deferred Components (Build Later)
1. [Component] - Add when [trigger condition]
2. [Component] - Add when [trigger condition]
...
```

### 2. Simplified Architecture Proposal

```markdown
## Minimal Viable Architecture

### Core Components (MVP)
- [ ] Component 1: [Purpose]
- [ ] Component 2: [Purpose]
...

### Deferred Components (v2)
- [ ] Component X: [Trigger to add]
...

### Model Usage
| Task | Model | Justification |
|------|-------|---------------|
| ... | ... | ... |
```

### 3. Implementation Priority Matrix

```markdown
## Priority Matrix

| Component | Value | Effort | Priority | Phase |
|-----------|-------|--------|----------|-------|
| ... | H/M/L | H/M/L | P0/P1/P2 | 0-5 |
```

---

## Validation Questions by Architecture Type

### For Agentic Workflows

1. **Agent Count**: How many agents are actually needed?
   - Rule of thumb: Start with 3 or fewer
   - Each agent adds: prompts, contracts, tests, routing logic

2. **Pattern Complexity**: Which patterns are essential?
   - Sequential: Almost always needed
   - Iterative: Needed for quality-sensitive tasks
   - Parallel: Only if tasks are truly independent
   - Self-Refine: Only if quality varies significantly

3. **Model Routing**: Is routing logic justified?
   - < 3 models: Use simple if/else
   - 3-5 models: Use config dict
   - > 5 models: Consider router abstraction

### For Tool Systems

1. **Tool Count**: How many tools?
   - < 5 tools: Direct registration
   - 5-15 tools: Simple registry
   - > 15 tools: Auto-discovery may help

2. **Tool Complexity**: Are tools doing too much?
   - Good: Single responsibility (read_file, write_file)
   - Bad: Multi-purpose (file_operations with 10 modes)

### For Multi-Model Systems

1. **Tier Boundaries**: Are tiers clearly differentiated?
   - Good: Clear capability gaps (1B can't do X, 7B can)
   - Bad: Arbitrary splits (tasks could go either way)

2. **Cost Optimization**: Is the optimization real?
   - Calculate: (Tier 1 cost × Tier 1 calls) vs (Tier 2 cost × all calls)
   - Sometimes simpler to use one model for everything

---

## Existing Infrastructure (Reuse Candidates)

### Already Built ✅

| Component | Location | Reusable? |
|-----------|----------|-----------|
| LLM Client | `tools/llm/llm_client.py` | ✅ Yes |
| Model Manager | `multiagent-workflows/src/.../model_manager.py` | ✅ Yes |
| Agent Base | `multiagent-workflows/src/.../agents/` | ⚠️ Partial |
| Workflow Engine | `multiagent-workflows/src/.../core/engine.py` | ⚠️ Review |
| Tool Definitions | `multiagent-workflows/scripts/run_repo_maintenance.py` | ⚠️ Extract |

### Key Question
> **Before building new, ask**: Can existing code be adapted with < 50% effort of rewrite?

---

## Execution Instructions

To run this validation:

1. **Load Context**: Read all planning documents
   ```
   read_file("docs/planning/agentic-workflows-v2-architecture.md")
   read_file("docs/planning/agentic-workflows-v2-implementation-patterns.md")
   read_file("docs/planning/agentic-workflows-v2-phased-implementation.md")
   ```

2. **Understand Current State**: Map existing code
   ```
   list_dir("multiagent-workflows/src/multiagent_workflows/")
   list_dir("tools/")
   ```

3. **Execute ReAct Loop**: Follow phases 1-6

4. **Generate Deliverables**:
   - Architecture Validation Report
   - Simplified Architecture Proposal
   - Implementation Priority Matrix

5. **Discuss Findings**: Present alternatives to stakeholders

---

---

## Quick Start: Run Validation Now

To immediately validate the current agentic-workflows-v2 plan:

```powershell
# 1. Read all three planning documents
# In Copilot Chat or Claude, paste this prompt:

@workspace Read and analyze these architecture documents:
- docs/planning/agentic-workflows-v2-architecture.md
- docs/planning/agentic-workflows-v2-implementation-patterns.md  
- docs/planning/agentic-workflows-v2-phased-implementation.md

Then answer:
1. What is the PRIMARY use case this serves?
2. Which components can be deferred to v2?
3. Is the model tiering strategy validated?
4. What existing code can be reused?
5. What's the simplest architecture that delivers MVP?
```

### Architecture Documents to Review

| Document | Purpose | Key Decisions |
|----------|---------|---------------|
| `agentic-workflows-v2-architecture.md` | Full architecture | Folder structure, components |
| `agentic-workflows-v2-implementation-patterns.md` | Code patterns | Contracts, tools, patterns |
| `agentic-workflows-v2-phased-implementation.md` | Phased plan | Model tiers, task mapping |

---

## Related Resources

- [Phased Implementation Plan](agentic-workflows-v2-phased-implementation.md) - Model tier assignments
- [Architecture Document](agentic-workflows-v2-architecture.md) - Full system design
- [Implementation Patterns](agentic-workflows-v2-implementation-patterns.md) - Code examples

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 5.0 | 2026-02-02 | Transformed to Architecture Plan Validator; added validation framework, anti-patterns, simplification analysis |
| 4.0 | 2025-12-02 | Previous: Prompt Library Analysis |
| 3.0 | 2025-11-30 | Added governance context |
| 2.0 | 2025-11-29 | Initial ReAct structure |
