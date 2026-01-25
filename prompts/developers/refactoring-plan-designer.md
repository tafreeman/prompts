---
name: Refactoring Plan Designer
description: Creates phased, risk-managed refactoring plans for large-scale code improvements. Breaks down complex refactorings into incremental steps with pre-checks, rollback strategies, and validation gates.
type: how_to
---
## Description

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

### 3. Pre-Refactoring Checklist

Before starting, ensure:

- [ ] [Pre-check 1, e.g., "Test coverage >70%"]
- [ ] [Pre-check 2, e.g., "Feature flag system in place"]
- [ ] [Pre-check 3, e.g., "Monitoring/alerting configured"]
- [ ] [Pre-check 4, e.g., "Stakeholder approval"]

#### Phase 2: [Phase Name]

[Same structure as Phase 1]

### 5. Validation & Monitoring

**During Refactoring:**

- Monitor: [Metrics to track, e.g., "error rate, latency, CPU usage"]
- Alerts: [When to stop and rollback]

**After Completion:**

- [ ] [Final validation 1]
- [ ] [Final validation 2]
- [ ] [Documentation updated]
- [ ] [Team trained on new code]

### 7. Timeline Estimate

| Phase | Duration | Start | End |
| ------- | ---------- | ------- | ----- |
| Phase 1 | [X weeks] | [Date] | [Date] |
| Phase 2 | [X weeks] | [Date] | [Date] |
| ... | ... | ... | ... |

**Total:** [X weeks/months]

**Buffer:** [+Y weeks for unknowns]
```

Creates phased, risk-managed refactoring plans for large-scale code improvements. Breaks down complex refactorings into incremental steps with pre-checks, rollback strategies, and validation gates.

## Description

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

### 3. Pre-Refactoring Checklist

Before starting, ensure:

- [ ] [Pre-check 1, e.g., "Test coverage >70%"]
- [ ] [Pre-check 2, e.g., "Feature flag system in place"]
- [ ] [Pre-check 3, e.g., "Monitoring/alerting configured"]
- [ ] [Pre-check 4, e.g., "Stakeholder approval"]

#### Phase 2: [Phase Name]

[Same structure as Phase 1]

### 5. Validation & Monitoring

**During Refactoring:**

- Monitor: [Metrics to track, e.g., "error rate, latency, CPU usage"]
- Alerts: [When to stop and rollback]

**After Completion:**

- [ ] [Final validation 1]
- [ ] [Final validation 2]
- [ ] [Documentation updated]
- [ ] [Team trained on new code]

### 7. Timeline Estimate

| Phase | Duration | Start | End |
| ------- | ---------- | ------- | ----- |
| Phase 1 | [X weeks] | [Date] | [Date] |
| Phase 2 | [X weeks] | [Date] | [Date] |
| ... | ... | ... | ... |

**Total:** [X weeks/months]

**Buffer:** [+Y weeks for unknowns]
```

Creates phased, risk-managed refactoring plans for large-scale code improvements. Breaks down complex refactorings into incremental steps with pre-checks, rollback strategies, and validation gates.


# Refactoring Plan Designer

## Output Requirements

Markdown with the following sections:

1. **Refactoring Overview** (goal, scope, success criteria)
2. **Risk Assessment** (risks and mitigations)
3. **Pre-Refactoring Checklist** (preparation steps)
4. **Phases** (incremental steps, each independently deployable)
5. **Validation & Monitoring** (how to verify success)
6. **Rollback Plans** (per phase)
7. **Timeline Estimate**

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

### 3. Pre-Refactoring Checklist

Before starting, ensure:

- [ ] [Pre-check 1, e.g., "Test coverage >70%"]
- [ ] [Pre-check 2, e.g., "Feature flag system in place"]
- [ ] [Pre-check 3, e.g., "Monitoring/alerting configured"]
- [ ] [Pre-check 4, e.g., "Stakeholder approval"]

#### Phase 2: [Phase Name]

[Same structure as Phase 1]

### 5. Validation & Monitoring

**During Refactoring:**

- Monitor: [Metrics to track, e.g., "error rate, latency, CPU usage"]
- Alerts: [When to stop and rollback]

**After Completion:**

- [ ] [Final validation 1]
- [ ] [Final validation 2]
- [ ] [Documentation updated]
- [ ] [Team trained on new code]

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

#### Phase 3: Read Migration

[Same structure: migrate reads to user service, validate, rollback plan]

## Governance Notes

- **Architecture Review:** Large refactorings should be reviewed by senior engineers
- **Stakeholder Approval:** Get buy-in from product/leadership on timeline and resource allocation
- **Documentation:** Document the plan and share with team
- **Post-Mortem:** After completion, document what worked and what didn't for future refactorings## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[ANY_OTHER_INFO]` | AUTO-GENERATED: describe `ANY_OTHER_INFO` |
| `[DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE]` | AUTO-GENERATED: describe `DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE` |
| `[PAIN_POINT_1]` | AUTO-GENERATED: describe `PAIN_POINT_1` |
| `[PAIN_POINT_2]` | AUTO-GENERATED: describe `PAIN_POINT_2` |
| `[PAIN_POINT_3]` | AUTO-GENERATED: describe `PAIN_POINT_3` |
| `[SUCCESS_CRITERION_1]` | AUTO-GENERATED: describe `SUCCESS_CRITERION_1` |
| `[SUCCESS_CRITERION_2]` | AUTO-GENERATED: describe `SUCCESS_CRITERION_2` |
| `[SYSTEM_OR_CODE_DESCRIPTION]` | AUTO-GENERATED: describe `SYSTEM_OR_CODE_DESCRIPTION` |
| `[WHAT_YOU_WANT_TO_ACHIEVE]` | AUTO-GENERATED: describe `WHAT_YOU_WANT_TO_ACHIEVE` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[+Y weeks for unknowns]` | AUTO-GENERATED: describe `+Y weeks for unknowns` |
| `[ANY_OTHER_INFO]` | AUTO-GENERATED: describe `ANY_OTHER_INFO` |
| `[DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE]` | AUTO-GENERATED: describe `DESCRIBE_CURRENT_CODE_OR_ARCHITECTURE` |
| `[Date]` | AUTO-GENERATED: describe `Date` |
| `[Documentation updated]` | AUTO-GENERATED: describe `Documentation updated` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Final validation 1]` | AUTO-GENERATED: describe `Final validation 1` |
| `[Final validation 2]` | AUTO-GENERATED: describe `Final validation 2` |
| `[Measurable criterion 1]` | AUTO-GENERATED: describe `Measurable criterion 1` |
| `[Measurable criterion 2]` | AUTO-GENERATED: describe `Measurable criterion 2` |
| `[Metrics to track, e.g., "error rate, latency, CPU usage"]` | AUTO-GENERATED: describe `Metrics to track, e.g., "error rate, latency, CPU usage"` |
| `[N developers]` | AUTO-GENERATED: describe `N developers` |
| `[One-sentence summary]` | AUTO-GENERATED: describe `One-sentence summary` |
| `[PAIN_POINT_*]` | AUTO-GENERATED: describe `PAIN_POINT_*` |
| `[PAIN_POINT_1]` | AUTO-GENERATED: describe `PAIN_POINT_1` |
| `[PAIN_POINT_2]` | AUTO-GENERATED: describe `PAIN_POINT_2` |
| `[PAIN_POINT_3]` | AUTO-GENERATED: describe `PAIN_POINT_3` |
| `[Phase Name]` | AUTO-GENERATED: describe `Phase Name` |
| `[Pre-check 1, e.g., "Test coverage >70%"]` | AUTO-GENERATED: describe `Pre-check 1, e.g., "Test coverage >70%"` |
| `[Pre-check 2, e.g., "Feature flag system in place"]` | AUTO-GENERATED: describe `Pre-check 2, e.g., "Feature flag system in place"` |
| `[Pre-check 3, e.g., "Monitoring/alerting configured"]` | AUTO-GENERATED: describe `Pre-check 3, e.g., "Monitoring/alerting configured"` |
| `[Pre-check 4, e.g., "Stakeholder approval"]` | AUTO-GENERATED: describe `Pre-check 4, e.g., "Stakeholder approval"` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[SUCCESS_CRITERION_*]` | AUTO-GENERATED: describe `SUCCESS_CRITERION_*` |
| `[SUCCESS_CRITERION_1]` | AUTO-GENERATED: describe `SUCCESS_CRITERION_1` |
| `[SUCCESS_CRITERION_2]` | AUTO-GENERATED: describe `SUCCESS_CRITERION_2` |
| `[SYSTEM_OR_CODE_DESCRIPTION]` | AUTO-GENERATED: describe `SYSTEM_OR_CODE_DESCRIPTION` |
| `[Same structure as Phase 1]` | AUTO-GENERATED: describe `Same structure as Phase 1` |
| `[Same structure: migrate reads to user service, validate, rollback plan]` | AUTO-GENERATED: describe `Same structure: migrate reads to user service, validate, rollback plan` |
| `[Team trained on new code]` | AUTO-GENERATED: describe `Team trained on new code` |
| `[WHAT_YOU_WANT_TO_ACHIEVE]` | AUTO-GENERATED: describe `WHAT_YOU_WANT_TO_ACHIEVE` |
| `[What's excluded]` | AUTO-GENERATED: describe `What's excluded` |
| `[What's included]` | AUTO-GENERATED: describe `What's included` |
| `[When to stop and rollback]` | AUTO-GENERATED: describe `When to stop and rollback` |
| `[X person-weeks]` | AUTO-GENERATED: describe `X person-weeks` |
| `[X weeks]` | AUTO-GENERATED: describe `X weeks` |
| `[X weeks/months]` | AUTO-GENERATED: describe `X weeks/months` |
| `[current %]` | AUTO-GENERATED: describe `current %` |
| `[e.g., 99.9%]` | AUTO-GENERATED: describe `e.g., 99.9%` |
| `[e.g., daily, weekly]` | AUTO-GENERATED: describe `e.g., daily, weekly` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

