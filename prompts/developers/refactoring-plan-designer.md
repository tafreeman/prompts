---

title: "Refactoring Plan Designer"
category: "developers"
tags: ["refactoring", "technical-debt", "developers", "planning", "risk-management"]
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-18"
difficulty: "intermediate"
governance_tags: ["architectural-change", "requires-review"]
platform: "Claude Sonnet 4.5"
---

# Refactoring Plan Designer

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

## Output Requirements

Markdown with the following sections:

1. **Refactoring Overview** (goal, scope, success criteria)
2. **Risk Assessment** (risks and mitigations)
3. **Pre-Refactoring Checklist** (preparation steps)
4. **Phases** (incremental steps, each independently deployable)
5. **Validation & Monitoring** (how to verify success)
6. **Rollback Plans** (per phase)
7. **Timeline Estimate**

## Use Cases

- Extracting a microservice from a monolith
- Migrating from one framework/library to another
- Changing database schemas or data models
- Refactoring large modules or classes
- Paying down technical debt systematically

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
|------|-----------|---------|-----------|
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
|-------|----------|-------|-----|
| Phase 1 | [X weeks] | [Date] | [Date] |
| Phase 2 | [X weeks] | [Date] | [Date] |
| ... | ... | ... | ... |

**Total:** [X weeks/months]

**Buffer:** [+Y weeks for unknowns]
```

## Variables

- `[SYSTEM_OR_CODE_DESCRIPTION]`: High-level description of what's being refactored
- `[DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE]`: Current state
- `[PAIN_POINT_X]`: Problems with current code
- `[WHAT_YOU_WANT_TO_ACHIEVE]`: Refactoring goal
- `[SUCCESS_CRITERION_X]`: Measurable success indicators
- `[N developers]`: Team size
- `[X weeks/months]`: Timeline
- `[e.g., 99.9%]`: Uptime requirement
- `[current %]`: Test coverage
- `[ANY_OTHER_INFO]`: Additional context

## Example Usage

**Input:**

```text
**System/Code:** E-commerce monolith (Rails app, 200K LOC)

**Current State:**
Single Rails app with tightly coupled user management, product catalog, and order processing.

**Pain Points:**
- User service changes require full app redeploy (risky)
- User service team blocked by order processing team
- Database contention (users and orders share same DB)

**Refactoring Goal:** Extract user management into a separate microservice

**Success Criteria:**
- User service independently deployable
- <10ms latency increase for user operations
- Zero downtime during extraction

**Constraints:**
- Team Size: 5 developers
- Timeline: 3 months
- Uptime Requirement: 99.95%
- Test Coverage: 60%
- Deployment Frequency: Daily
```

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
|------|-----------|---------|-----------|
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
```

## Tips

- **Start small:** First phase should be low-risk preparation (tests, boundaries)
- **Use feature flags:** Enable gradual rollout and instant rollback
- **Monitor everything:** Track latency, error rates, data consistency
- **Plan for failure:** Every phase needs a rollback plan
- **Communicate:** Share the plan with team and stakeholders
- **Iterate:** Adjust phases based on learnings from early phases

## Related Prompts

- [Tree-of-Thoughts: Architecture Evaluator](../advanced-techniques/tree-of-thoughts-architecture-evaluator.md) - For evaluating refactoring options
- [Chain-of-Thought: Debugging](../advanced-techniques/chain-of-thought-debugging.md) - For fixing issues during refactoring
- [Code Review Expert: Structured](code-review-expert-structured.md) - For reviewing refactoring PRs

## Governance Notes

- **Architecture Review:** Large refactorings should be reviewed by senior engineers
- **Stakeholder Approval:** Get buy-in from product/leadership on timeline and resource allocation
- **Documentation:** Document the plan and share with team
- **Post-Mortem:** After completion, document what worked and what didn't for future refactorings

## Changelog

- 2025-11-18: Initial version based on ToT repository evaluation recommendations
