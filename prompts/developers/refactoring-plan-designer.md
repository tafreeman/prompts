---
title: Refactoring Plan Designer
shortTitle: Refactoring Plan Designer
intro: Creates phased, risk-managed refactoring plans for large-scale code improvements.
  Breaks down complex refactorings into incremental steps with pre-checks, rollback
  strategies, and validation gates.
type: how_to
difficulty: intermediate
audience:

- senior-engineer

platforms:

- claude

topics:

- refactoring
- technical-debt
- developers

author: Prompt Engineering Team
version: '1.0'
date: '2025-11-18'
governance_tags:

- PII-safe
- requires-human-review

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Refactoring Plan Designer

---

## Description

Creates phased, risk-managed refactoring plans for large-scale code improvements. Breaks down complex refactorings into incremental steps with pre-checks, rollback strategies, and validation gates.

## Goal

Enable developers to safely refactor complex codebases by creating detailed, phased plans that minimize risk and maintain system stability throughout the process.

## Context

Use this prompt when planning large refactorings (extracting services, changing data models, migrating frameworks), technical debt paydown initiatives, or any code changes that can't be done in a single pull request.

## Inputs

- Code or system to refactor
- Refactoring goal (what you want to achieve)
- Current pain points or technical debt
- Constraints (team size, timeline, uptime requirements)

## Assumptions

- User can dedicate time to incremental refactoring
- System has some test coverage (or tests will be added)
- Changes need to be production-safe (no big bang rewrites)

## Constraints

- Each phase must be independently deployable
- Risk must be quantified and mitigated
- Rollback plans required for each phase
- Must preserve system functionality throughout

## Process / Reasoning Style

Structured planning with risk analysis. Output is a phased plan with explicit pre-checks, steps, validations, and rollbacks.

---

## Output Requirements

Markdown with the following sections:

1. **Refactoring Overview** (goal, scope, success criteria)
2. **Risk Assessment** (risks and mitigations)
3. **Pre-Refactoring Checklist** (preparation steps)
4. **Phases** (incremental steps, each independently deployable)
5. **Validation & Monitoring** (how to verify success)
6. **Rollback Plans** (per phase)
7. **Timeline Estimate**

---

## Use Cases

- Extracting a microservice from a monolith
- Migrating from one framework/library to another
- Changing database schemas or data models
- Refactoring large modules or classes
- Paying down technical debt systematically

---

## Variables

<details>
<summary><b>Common placeholders</b> (click to expand)</summary>

| Variable | Description | Example |
| --- | --- | --- |
| `[SYSTEM_OR_CODE_DESCRIPTION]` | What is being refactored | `User management module in monolith` |
| `[DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE]` | Current state details | `Tight coupling, shared DB tables, no boundaries` |
| `[PAIN_POINT_*]` | Key pain points (1..n) | `Slow deploys`, `Frequent regressions` |
| `[WHAT_YOU_WANT_TO_ACHIEVE]` | Refactoring goal | `Extract user service behind an API` |
| `[SUCCESS_CRITERION_*]` | Success criteria (1..n) | `No downtime`, `Latency +10ms max` |
| `[N developers]` | Team size constraint | `3 engineers` |
| `[X weeks/months]` | Timeline constraint | `8 weeks` |
| `[current %]` | Current test coverage | `55%` |
| `[ANY_OTHER_INFO]` | Extra constraints/context | `Must be PCI-safe; feature flags required` |

</details>

---

## Usage

**Input:**

```text
System/Code: User management module in a legacy monolith

Current State:

- Shared database tables across 5 domains
- Authentication mixed with user CRUD

Pain Points:

- Deployments take 2 hours
- Frequent regressions in auth flows

Refactoring Goal: Extract user management into an independently deployable service

Success Criteria:

- No production incidents during migration
- <10ms latency overhead for user operations

Constraints:

- Team Size: 3 developers
- Timeline: 8 weeks
- Uptime Requirement: 99.9%
- Test Coverage: 55%
- Deployment Frequency: weekly

Additional Context: Must support feature flags and staged rollout
```

---

## Prompt

```text
You are a senior software architect creating a phased refactoring plan.

## Refactoring Request

**System/Code:** [SYSTEM_OR_CODE_DESCRIPTION]

**Current State:**
[DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE]

**Pain Points:**

- [PAIN_POINT_1]
- [PAIN_POINT_2]
- [PAIN_POINT_3]

**Refactoring Goal:** [WHAT_YOU_WANT_TO_ACHIEVE]

**Success Criteria:**

- [SUCCESS_CRITERION_1]
- [SUCCESS_CRITERION_2]

**Constraints:**

- Team Size: [N developers]
- Timeline: [X weeks/months]
- Uptime Requirement: [e.g., 99.9%]
- Test Coverage: [current %]
- Deployment Frequency: [e.g., daily, weekly]

**Additional Context:** [ANY_OTHER_INFO]

---

## Task

Create a **detailed, phased refactoring plan** that:

1. Breaks the refactoring into small, independently deployable steps
2. Quantifies risk for each phase
3. Includes pre-checks, validation gates, and rollback plans
4. Preserves system functionality throughout

---

## Output Format

### 1. Refactoring Overview

**Goal:** [One-sentence summary]

**Scope:**

- [What's included]
- [What's excluded]

**Success Criteria:**

1. [Measurable criterion 1]
2. [Measurable criterion 2]

**Estimated Effort:** [X person-weeks]

---

### 2. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| ------ | ----------- | --------- | ----------- |
| [Risk 1] | High/Med/Low | High/Med/Low | [How to address] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to address] |

---

### 3. Pre-Refactoring Checklist

Before starting, ensure:

- [ ] [Pre-check 1, e.g., "Test coverage >70%"]
- [ ] [Pre-check 2, e.g., "Feature flag system in place"]
- [ ] [Pre-check 3, e.g., "Monitoring/alerting configured"]
- [ ] [Pre-check 4, e.g., "Stakeholder approval"]

---

### 4. Phases

#### Phase 1: [Phase Name]

**Duration:** [X days/weeks]

**Goal:** [What this phase achieves]

**Steps:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Changes:**

- Files/modules affected: [list]
- Lines of code: [estimate]

**Risk Level:** [High/Medium/Low]

**Validation:**

- [ ] [Validation step 1, e.g., "All tests pass"]
- [ ] [Validation step 2, e.g., "Performance unchanged"]
- [ ] [Validation step 3, e.g., "No error rate increase"]

**Rollback Plan:**
[How to revert this phase if issues arise]

**Deploy Strategy:**
[e.g., "Feature flag off by default, gradual rollout to 10% → 50% → 100%"]

---

#### Phase 2: [Phase Name]

[Same structure as Phase 1]

---

[Additional phases as needed]

---

### 5. Validation & Monitoring

**During Refactoring:**

- Monitor: [Metrics to track, e.g., "error rate, latency, CPU usage"]
- Alerts: [When to stop and rollback]

**After Completion:**

- [ ] [Final validation 1]
- [ ] [Final validation 2]
- [ ] [Documentation updated]
- [ ] [Team trained on new code]

---

### 6. Rollback Plans

**Per-Phase Rollback:** See each phase above

**Full Rollback (All Phases):**
[How to completely revert the refactoring if fundamental issues discovered]

---

### 7. Timeline Estimate

| Phase | Duration | Start | End |
| ------- | ---------- | ------- | ----- |
| Phase 1 | [X weeks] | [Date] | [Date] |
| Phase 2 | [X weeks] | [Date] | [Date] |
| ... | ... | ... | ... |

**Total:** [X weeks/months]

**Buffer:** [+Y weeks for unknowns]
```text

**Output (abbreviated):**

```markdown
### 1. Refactoring Overview

**Goal:** Extract user management into an independently deployable microservice

**Scope:**

- Included: User CRUD, authentication, profile management
- Excluded: User analytics (remains in monolith for now)

**Success Criteria:**

1. User service handles 100% of user operations with <10ms latency overhead
2. Zero production incidents during migration
3. User service independently deployable (CI/CD pipeline)

**Estimated Effort:** 10 person-weeks

---

### 2. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| ------ | ----------- | --------- | ----------- |
| Data migration failure | Medium | High | Dual-write period + rollback script |
| Performance degradation | Medium | High | Load testing before each phase |
| Authentication breaks | Low | Critical | Feature flags + canary rollout |

---

### 4. Phases

#### Phase 1: Preparation & Isolation

**Duration:** 2 weeks

**Goal:** Isolate user management code within monolith

**Steps:**

1. Create user module boundary (namespace, separate folder)
2. Identify all dependencies (inbound/outbound calls)
3. Add integration tests for user service interface
4. Increase test coverage to 80%+ for user code

**Risk Level:** Low

**Validation:**

- [ ] User module passes all tests independently
- [ ] No new cross-module dependencies
- [ ] Performance benchmarks unchanged

**Rollback Plan:** Revert module boundary (code still in monolith)

---

#### Phase 2: Dual-Write Setup

**Duration:** 1 week

**Goal:** Write user data to both monolith DB and new user service DB

**Steps:**

1. Set up user service infrastructure (DB, app, CI/CD)
2. Implement dual-write logic (write to both DBs)
3. Enable dual-write via feature flag (off by default)
4. Monitor data consistency

**Risk Level:** Medium

**Validation:**

- [ ] Data consistency checks pass (monolith DB == user service DB)
- [ ] No latency increase >5ms
- [ ] Error rates unchanged

**Rollback Plan:** Disable feature flag, continue writing to monolith DB only

**Deploy Strategy:** Feature flag on for 10% traffic → monitor 48hrs → 100%

---

#### Phase 3: Read Migration

[Same structure: migrate reads to user service, validate, rollback plan]

---

#### Phase 4: Remove Monolith User Code

[Same structure: delete old user code from monolith, final validation]
```text

- [Code Review Expert: Structured](code-review-expert-structured.md) - For reviewing refactoring PRs

---

## Governance Notes

- **Architecture Review:** Large refactorings should be reviewed by senior engineers
- **Stakeholder Approval:** Get buy-in from product/leadership on timeline and resource allocation
- **Documentation:** Document the plan and share with team
- **Post-Mortem:** After completion, document what worked and what didn't for future refactorings
