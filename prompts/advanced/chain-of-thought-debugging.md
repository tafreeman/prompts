---
name: Chain Of Thought Debugging
description: # Chain-of-Thought: Debugging & Root Cause Analysis
type: how_to
---
## Description

## Prompt

```

## Example Usage

**Input:**

```

# Chain-of-Thought: Debugging & Root Cause Analysis

## Description

## Prompt

```

## Example Usage

**Input:**

```

# Chain-of-Thought: Debugging & Root Cause Analysis


# Chain-of-Thought: Debugging & Root Cause Analysis

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

## Use Cases

- Debugging intermittent production issues with limited reproduction steps
- Root cause analysis for test failures in CI/CD pipelines
- Investigating performance regressions (memory leaks, slowdowns)
- Analyzing security vulnerabilities or unexpected behaviors
- Postmortem analysis for incidents with unclear causes

## Instructions

Use Chain-of-Thought reasoning to debug this issue:

### Step 1: Understanding the Bug
Summarize the symptoms, timeline, and any patterns. Note what works and what doesn't.

### Step 2: Hypothesis Generation
Generate 3-5 testable hypotheses about possible root causes. For each:

- State the hypothesis clearly
- Assess likelihood (HIGH/MEDIUM/LOW)
- List supporting evidence

### Step 3: Hypothesis Prioritization
Rank hypotheses by: (1) likelihood based on evidence, (2) ease of testing

### Step 4: Evidence Analysis
For the top hypothesis:

- Explain why it's most likely
- Design an experiment to confirm/refute it
- If refuted, move to next hypothesis

### Step 5: Root Cause
State the confirmed root cause with evidence chain.

### Step 6: Recommended Fix
Provide:

- Immediate fix (code/config change)
- Long-term fix (prevent recurrence)
- Infrastructure improvements if applicable

### Step 7: Regression Test
Provide test cases that would catch this bug if it recurs.
```

## Example Usage

**Input:**

```markdown
You are an expert software debugger using Chain-of-Thought reasoning to systematically identify and fix bugs.

## Bug Report

**Description:** User authentication fails intermittently in production (~5% of requests)

**Error Message:**
AuthenticationError: JWT token verification failed
    at verifyToken (auth.js:45)
    at authenticate (middleware.js:12)
    at app.use (server.js:30)

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

**Additional Context:**

- Logs show "invalid signature" errors
- Issue started after deploying to multiple servers (load-balanced)
- Single-server staging environment doesn't reproduce the issue

```

**Expected Output:**

```markdown
## Chain-of-Thought Debugging Analysis

### Step 1: Understanding the Bug

**Symptoms:**

- ~5% of authenticated requests fail with "JWT token verification failed"
- Error: "invalid signature"
- Started after deploying to multiple servers (load-balanced)
- Single-server staging works fine

**Key Insight:** The intermittent nature (~5%) combined with the timing (after multi-server deployment) strongly suggests an environment inconsistency across servers.

### Step 3: Evidence Analysis (H1 - JWT_SECRET Mismatch)

**Why H1 is most likely:**

1. **"Invalid signature" error**: This specific error occurs when:
   - Token was signed with a different secret than used for verification
   - Token was corrupted

2. **~5% failure rate**: If 1 of 4 servers has a different JWT_SECRET, we'd expect ~25% failure. But if the secret is loaded from env vars and one server has a stale value, intermittent failures make sense.

3. **Single-server staging works**: Same codebase, different environment = environment variable issue

4. **Started after multi-server deployment**: New servers may have different environment configurations

**Experiment to confirm:**

```bash

# SSH into each production server and check JWT_SECRET
for server in prod-1 prod-2 prod-3 prod-4; do
  echo "=== $server ==="
  ssh $server 'echo $JWT_SECRET | sha256sum'
done

```

If the hashes differ, H1 is confirmed.

### Step 5: Recommended Fix

**Immediate Fix:**
```bash

# Sync JWT_SECRET across all servers from authoritative source
JWT_SECRET=$(aws secretsmanager get-secret-value --secret-id prod/jwt-secret | jq -r .SecretString)
# Deploy to all servers via your config management tool

```

**Code Fix (defense in depth):**
```javascript

// auth.js - Add validation at startup
const JWT_SECRET = process.env.JWT_SECRET;

if (!JWT_SECRET || JWT_SECRET.length < 32) {
  console.error('FATAL: JWT_SECRET is missing or too short');
  process.exit(1);  // Fail fast instead of running with bad config
}

function verifyToken(token) {
  return jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] });
}

```

**Infrastructure Fix (prevent recurrence):**
```yaml

# Use centralized secrets management (e.g., AWS Secrets Manager, Vault)
# kubernetes/deployment.yaml
env:

  - name: JWT_SECRET

    valueFrom:
      secretKeyRef:
        name: jwt-secrets
        key: JWT_SECRET

```

### Summary

| Attribute | Value |
| ----------- | ------- |
| **Root Cause** | JWT_SECRET environment variable mismatch across production servers |
| **Confidence** | HIGH (95%) |
| **Category** | Configuration / Environment |
| **Severity** | HIGH (authentication bypass risk) |
| **Fix Complexity** | LOW (environment sync) |
| **Recommended Action** | 1) Sync secrets immediately, 2) Add startup validation, 3) Use centralized secrets management |
```

## Related Prompts

- [Chain-of-Thought: Performance Analysis](chain-of-thought-performance-analysis.md) - For performance debugging
- [Tree-of-Thoughts: Architecture Evaluator](tree-of-thoughts-architecture-evaluator.md) - For complex system issues

---

## Governance Notes

- **PII Safety:** Ensure bug reports and logs don't contain PII (user IDs, emails, passwords, tokens)
- **Security:** Redact secrets, API keys, and credentials from error messages and code snippets
- **Human Review:** Critical production bugs should be reviewed by senior engineers before deployment
- **Audit Trail:** Save complete CoT reasoning for postmortems and knowledge sharing
- **Cost:** CoT debugging can be token-intensive; use for non-trivial bugs where systematic analysis adds value## Variables

| Variable | Description |
|---|---|
| `[1]` | AUTO-GENERATED: describe `1` |

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
| `['HS256']` | AUTO-GENERATED: describe `'HS256'` |
| `[1]` | AUTO-GENERATED: describe `1` |
| `[Chain-of-Thought: Performance Analysis]` | AUTO-GENERATED: describe `Chain-of-Thought: Performance Analysis` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Tree-of-Thoughts: Architecture Evaluator]` | AUTO-GENERATED: describe `Tree-of-Thoughts: Architecture Evaluator` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

