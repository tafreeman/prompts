---
name: session-plan
description: Plan a focused session with 1-2 goals, explicit success criteria, and a TODO checklist. Prevents mega-sessions that hit rate limits by scoping work upfront and tracking progress.
---

# Session Plan

Break ambitious work into focused, achievable sessions. Prevents the #1 pattern of failed sessions: stacking 4-5 tasks that hit rate limits before finishing.

## Trigger

Use when:
- User describes multiple things they want to accomplish
- Task sounds like it could take a full session or more
- User says "I want to...", "Let's work on...", "Can you..."
- Beginning of any non-trivial session

## Process

### 1. Scope Check

Ask: "How many distinct tasks is this?" If > 2, propose splitting:

```
I see 4 tasks here. To avoid hitting limits mid-work, I'd suggest:

**This session:**
1. [Most important/blocking task]
2. [Second priority if related]

**Next session:**
3. [Task 3]
4. [Task 4]

Want to proceed with this split, or reprioritize?
```

### 2. Create Session Plan

For the scoped tasks, create a TODO list with:
- [ ] **Goal 1:** [Clear description]
  - [ ] Success criteria: [What "done" looks like]
  - [ ] Verification: [Command to prove it works]
- [ ] **Goal 2:** [Clear description]
  - [ ] Success criteria: [What "done" looks like]
  - [ ] Verification: [Command to prove it works]
- [ ] **Commit:** Stage and commit completed work

### 3. Execute with Checkpoints

After completing each goal:
1. Run the verification command
2. Update the TODO (mark complete)
3. Ask: "Goal 1 is done and verified. Move to Goal 2?"

### 4. Session Wrap-Up

Before ending:
1. Summarize what was completed
2. List anything deferred
3. Suggest what to tackle next session
4. Commit all work if not already committed

## Rules

- **Max 2 goals per session** — quality over quantity
- **Verify before claiming done** — run the actual commands
- **Commit after each goal** — don't accumulate uncommitted work
- **If hitting rate limits** — commit what's done, document remaining in TODO
- **Never silently skip a goal** — explicitly defer with reason

## Anti-Patterns to Avoid

- "Let me also quickly..." — scope creep mid-session
- Fixing unrelated issues discovered during work (note them, don't fix)
- Starting Goal 2 before Goal 1 is verified and committed
