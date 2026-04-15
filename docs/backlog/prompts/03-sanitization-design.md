# Prompt 03 — Prompt sanitization and security design

## Use this for

Designing the pre-flight sanitization and policy enforcement layer for outbound model prompts.

## Prompt

```markdown
# Role
You are a security-focused AI platform architect specializing in secret redaction, prompt pipeline hardening, and safe LLM request middleware.

# Objective
Design a prompt sanitization and security layer for `C:\Users\tandf\source\prompts` that runs before outbound provider calls.

The system should detect and handle:
- API keys
- bearer tokens
- passwords and secrets
- `.env`-style key/value material
- private tokens embedded in free text
- other sensitive payloads that should be redacted, blocked, or flagged

# Reference source
Base the design on safety and context-management patterns studied in:

- `C:\Users\tandf\source\claude-code-main`

Review and adapt ideas from:

- `src/tools/`
- `src/utils/`
- `src/utils/tokenBudget.ts`
- `src/bridge/`
- any related secret-safe or context-safe handling patterns found during repo review

# Tasks
1. Propose where sanitization middleware should live in the repo.
2. Recommend whether it should run before every provider call or only selected ones.
3. Define the classification outcomes:
   - clean
   - redacted
   - blocked
   - requires-approval
4. Design the redaction categories and false-positive strategy.
5. Propose core models/contracts for sanitization results.
6. Recommend tests and fixtures needed to validate the policy.
7. Explain how this should integrate with existing hooks or secret-detection mechanisms.

# Constraints
- Prefer fail-safe behavior for high-risk findings.
- Do not store raw secrets in logs.
- Return redacted copies rather than mutating original inputs where possible.
- Be specific to this repo’s Python orchestration shape.

# Deliverable format
Return:
1. Recommended middleware architecture
2. Classification policy
3. File/folder plan
4. Core contracts/models
5. Test plan
6. Risks and mitigations
```
