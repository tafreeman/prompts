---
title: 'Chain-of-Thought: Debugging & Root Cause Analysis'
shortTitle: CoT Debugging
intro: A specialized Chain-of-Thought prompt for systematic debugging and root cause
  analysis using explicit step-by-step reasoning.
type: how_to
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- claude
- github-copilot
topics:
- debugging
- development
author: Prompt Engineering Team
version: '1.0'
date: '2025-11-18'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
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

---

### Step 2: Hypothesis Generation

| # | Hypothesis | Likelihood | Evidence |
|---|-----------|-----------|----------|
| H1 | JWT_SECRET differs between servers | HIGH | Started after multi-server deploy; "invalid signature" error; staging works |
| H2 | Clock skew between servers causes token timing issues | MEDIUM | Intermittent failures; multi-server environment |
| H3 | Token parsing issue (header format) | LOW | Would fail consistently, not 5% |
| H4 | Load balancer modifying Authorization header | LOW | Would affect all requests from certain paths |
| H5 | Race condition in token verification | LOW | jwt.verify is synchronous |

**Prioritization:** H1 > H2 > H4 > H3 > H5

---

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

---

### Step 4: Root Cause

**ROOT CAUSE: JWT_SECRET environment variable mismatch across production servers**

When new servers were deployed, the JWT_SECRET was not synchronized. Tokens signed by Server A cannot be verified by Server B if they have different secrets.

**Evidence chain:**
1. "Invalid signature" error → secret mismatch
2. ~5% failure → only some servers affected
3. Started after multi-server deploy → new servers have different config
4. Staging works → single server, no mismatch possible

---

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

---

### Step 6: Regression Test

```javascript
// test/auth.integration.test.js
describe('JWT Authentication (multi-server simulation)', () => {
  const SECRET_A = 'secret-server-a';
  const SECRET_B = 'secret-server-b';  // Different secret
  
  it('should fail verification if secrets mismatch', () => {
    const token = jwt.sign({ userId: '123' }, SECRET_A, { algorithm: 'HS256' });
    
    expect(() => {
      jwt.verify(token, SECRET_B, { algorithms: ['HS256'] });
    }).toThrow('invalid signature');
  });
  
  it('should succeed verification if secrets match', () => {
    const token = jwt.sign({ userId: '123' }, SECRET_A, { algorithm: 'HS256' });
    const decoded = jwt.verify(token, SECRET_A, { algorithms: ['HS256'] });
    
    expect(decoded.userId).toBe('123');
  });
});
```

---

### Summary

| Attribute | Value |
|-----------|-------|
| **Root Cause** | JWT_SECRET environment variable mismatch across production servers |
| **Confidence** | HIGH (95%) |
| **Category** | Configuration / Environment |
| **Severity** | HIGH (authentication bypass risk) |
| **Fix Complexity** | LOW (environment sync) |
| **Recommended Action** | 1) Sync secrets immediately, 2) Add startup validation, 3) Use centralized secrets management |
```

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
