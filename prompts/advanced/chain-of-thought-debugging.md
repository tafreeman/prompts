---
title: "Chain-of-Thought: Debugging & Root Cause Analysis"
shortTitle: "CoT Debugging"
intro: "A specialized Chain-of-Thought prompt for systematic debugging and root cause analysis using explicit step-by-step reasoning."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "junior-engineer"
platforms:
  - "claude"
  - "github-copilot"
topics:
  - "debugging"
  - "development"
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-18"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Chain-of-Thought: Debugging & Root Cause Analysis

---

## Description

A specialized Chain-of-Thought prompt for systematic debugging and root cause analysis. Guides developers through reproducing bugs, generating hypotheses, designing experiments, and proposing validated fixes with regression tests.

---

## Research Foundation

Based on Chain-of-Thought prompting (Wei et al., NeurIPS 2022) and adapted for software debugging workflows. Incorporates systematic debugging methodologies from "Why Programs Fail" (Zeller, 2009) and hypothesis-driven experimentation.

## Goal

Enable developers to debug issues systematically using explicit step-by-step reasoning, reducing guesswork and improving fix quality through structured root cause analysis.

## Context

Use this prompt when debugging production issues, investigating test failures, analyzing error logs, or performing root cause analysis. Best suited for complex, non-obvious bugs where the cause isn't immediately apparent.

## Inputs

- Bug description or error message
- Reproduction steps (if known)
- Relevant code snippets
- Error logs, stack traces, or telemetry
- Environment details (OS, runtime, dependencies)
- Expected vs. actual behavior

## Assumptions

- User has access to the codebase and can test hypotheses
- Bug is reproducible (or can be approximated)
- User has basic debugging tools (debugger, profiler, logs)

## Constraints

- Focus on root cause, not just symptoms
- Propose fixes that are minimal, testable, and don't introduce regressions
- Reasoning must be explicit and step-by-step
- Each hypothesis must be testable

## Process / Reasoning Style

**Chain-of-Thought (explicit reasoning)**

1. **Symptom Analysis:** Understand the observed behavior
2. **Hypothesis Generation:** Create 3–5 testable hypotheses about root causes
3. **Hypothesis Prioritization:** Rank by likelihood and test difficulty
4. **Experiment Design:** Define tests to validate/falsify each hypothesis
5. **Root Cause Identification:** Determine the actual cause based on evidence
6. **Fix Proposal:** Design a minimal, testable fix
7. **Regression Prevention:** Propose tests to prevent future occurrences

All reasoning steps must be visible in the output.

---

## Output Requirements

Structured Markdown with the following sections:

1. **Symptom Summary**
2. **Initial Hypotheses** (ranked)
3. **Experiment Design** (for top hypotheses)
4. **Root Cause** (evidence-based conclusion)
5. **Proposed Fix** (code snippet + rationale)
6. **Regression Tests** (test cases to prevent recurrence)
7. **Verification Steps** (how to confirm the fix works)

See `docs/domain-schemas.md` for additional schema options.

---

## Use Cases

- Debugging intermittent production issues with limited reproduction steps
- Root cause analysis for test failures in CI/CD pipelines
- Investigating performance regressions (memory leaks, slowdowns)
- Analyzing security vulnerabilities or unexpected behaviors
- Postmortem analysis for incidents with unclear causes

---

## Prompt

```text
You are an expert software debugger using Chain-of-Thought reasoning to systematically identify and fix bugs.

## Bug Report

**Description:** [BUG_DESCRIPTION]

**Error Message:**
```text

---

## Variables

- `[BUG_DESCRIPTION]`: High-level description of the bug (e.g., "User login fails intermittently")
- `[ERROR_MESSAGE_OR_STACK_TRACE]`: Full error message or stack trace
- `[REPRODUCTION_STEPS]`: Steps to reproduce the bug (or "unknown" if not reproducible)
- `[EXPECTED_BEHAVIOR]`: What should happen
- `[ACTUAL_BEHAVIOR]`: What actually happens
- `[OPERATING_SYSTEM]`: OS and version (e.g., "Ubuntu 22.04", "Windows 11")
- `[RUNTIME_VERSION]`: Runtime environment (e.g., "Node.js 20.10", "Python 3.11")
- `[KEY_DEPENDENCIES]`: Relevant libraries and versions
- `[LANGUAGE]`: Programming language
- `[CODE_SNIPPET]`: Relevant code (function, class, or module)
- `[LOGS_TELEMETRY_OR_OTHER_INFO]`: Additional diagnostic information

---

## Example Usage

**Input:**

```text

You are an expert software debugger using Chain-of-Thought reasoning to systematically identify and fix bugs.

## Bug Report

**Description:** User authentication fails intermittently in production (~5% of requests)

**Error Message:**

```text

AuthenticationError: JWT token verification failed
    at verifyToken (auth.js:45)
    at authenticate (middleware.js:12)
    at app.use (server.js:30)

```text

**Reproduction Steps:**

1. User logs in successfully
2. User makes an authenticated API request within 5 minutes
3. ~5% of the time, the request fails with JWT verification error

**Expected Behavior:** All authenticated requests within token expiry (1 hour) should succeed

**Actual Behavior:** Some requests fail with JWT verification error, even with valid tokens

**Environment:**

- OS: Ubuntu 22.04 (production)
- Runtime: Node.js 20.10
- Dependencies: jsonwebtoken 9.0.2, express 4.18.2

**Relevant Code:**

```javascript
// auth.js
function verifyToken(token) {
  return jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
}

// middleware.js
async function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  
  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```text

**Additional Context:**

- Logs show "invalid signature" errors
- Issue started after deploying to multiple servers (load-balanced)
- Single-server staging environment doesn't reproduce the issue

```text

---

## Tips

- **Start broad, narrow down:** Generate multiple hypotheses, then prioritize and test systematically
- **Use evidence, not intuition:** Every hypothesis and conclusion should be backed by observable evidence
- **Test one variable at a time:** Design experiments that isolate specific causes
- **Consider the environment:** Many bugs are environment-specific (multi-server, race conditions, resource limits)
- **Propose minimal fixes:** Avoid over-engineering; fix the root cause with minimal code changes
- **Always include regression tests:** Prevent the bug from recurring
- **Document reasoning:** Visible CoT reasoning helps others learn and validates your logic

---

## Related Prompts

- [Chain-of-Thought: Performance Analysis](chain-of-thought-performance-analysis.md) - For performance debugging
- [Tree-of-Thoughts: Architecture Evaluator](tree-of-thoughts-architecture-evaluator.md) - For complex system issues

---

## Governance Notes

- **PII Safety:** Ensure bug reports and logs don't contain PII (user IDs, emails, passwords, tokens)
- **Security:** Redact secrets, API keys, and credentials from error messages and code snippets
- **Human Review:** Critical production bugs should be reviewed by senior engineers before deployment
- **Audit Trail:** Save complete CoT reasoning for postmortems and knowledge sharing
- **Cost:** CoT debugging can be token-intensive; use for non-trivial bugs where systematic analysis adds value
