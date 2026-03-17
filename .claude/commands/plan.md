---
description: Restate requirements, assess risks, and create step-by-step implementation plan. WAIT for user CONFIRM before touching any code.
---

# Plan Command

This command invokes the **planner** agent to create a comprehensive implementation plan before writing any code.

## What This Command Does

1. **Restate Requirements** - Clarify what needs to be built
2. **Identify Risks** - Surface potential issues and blockers
3. **Create Step Plan** - Break down implementation into phases
4. **Wait for Confirmation** - MUST receive user approval before proceeding

## When to Use

Use `/plan` when:
- Starting a new feature
- Making significant architectural changes
- Working on complex refactoring
- Multiple files/components will be affected
- Requirements are unclear or ambiguous

## How It Works

The planner agent will:

1. **Analyze the request** and restate requirements in clear terms
2. **Break down into phases** with specific, actionable steps
3. **Identify dependencies** between components
4. **Assess risks** and potential blockers
5. **Estimate complexity** (High/Medium/Low)
6. **Present the plan** and WAIT for your explicit confirmation

## Example Usage

```
User: /plan I need to add domain-adaptive recency windows to the deep research scoring pipeline

Agent (planner):
# Implementation Plan: Domain-Adaptive Recency Windows

## Requirements Restatement
- Replace the hard-coded recency window in `agentic_v2/server/multidimensional_scoring.py`
- Load per-profile defaults from `agentic_v2/config/defaults/evaluation.yaml`
- Preserve today's scoring behavior when no override is configured

## Implementation Phases

### Phase 1: Config Contract
- Add recency-window entries to `agentic_v2/config/defaults/evaluation.yaml`
- Define parsing and validation helpers in `agentic_v2/server/scoring_profiles.py`

### Phase 2: Scoring Integration
- Thread the selected window into `agentic_v2/server/multidimensional_scoring.py`
- Keep `183` days as the fallback when a profile does not opt in

### Phase 3: Verification
- Add pytest coverage for default, override, and invalid-window cases
- Re-run the multidimensional scoring tests to confirm no regression

## Dependencies
- No new dependencies
- Existing: `agentic_v2/server/scoring_profiles.py`, `agentic_v2/config/defaults/evaluation.yaml`

## Risks
- MEDIUM: Profile config drift between defaults and runtime loader
- LOW: Behavior change for profiles with partial overrides

## Estimated Complexity: MEDIUM
- Implementation: 2-4 hours
- Testing: 1-2 hours
- Total: 3-6 hours

**WAITING FOR CONFIRMATION**: Proceed with this plan? (yes/no/modify)
```

## Important Notes

**CRITICAL**: The planner agent will **NOT** write any code until you explicitly confirm the plan with "yes" or "proceed" or similar affirmative response.

If you want changes, respond with:
- "modify: [your changes]"
- "different approach: [alternative]"
- "skip phase 2 and do phase 3 first"

## Integration with Other Commands

After planning:
- Use `/tdd` to implement with test-driven development
- Use `/build-fix` if build errors occur
- Use `/code-review` to review completed implementation

## Related Agents

This command invokes the `planner` agent located at:
`.claude/agents/planner.md`
