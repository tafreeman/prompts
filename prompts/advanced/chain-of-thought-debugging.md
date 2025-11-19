---

title: "Chain-of-Thought: Debugging & Root Cause Analysis"
category: "advanced-techniques"
tags: ["chain-of-thought", "debugging", "root-cause-analysis", "developers", "reasoning"]
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-18"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Chain-of-Thought: Debugging & Root Cause Analysis

## Description

A specialized Chain-of-Thought prompt for systematic debugging and root cause analysis. Guides developers through reproducing bugs, generating hypotheses, designing experiments, and proposing validated fixes with regression tests.

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

## Use Cases

- Debugging intermittent production issues with limited reproduction steps
- Root cause analysis for test failures in CI/CD pipelines
- Investigating performance regressions (memory leaks, slowdowns)
- Analyzing security vulnerabilities or unexpected behaviors
- Postmortem analysis for incidents with unclear causes

## Prompt

```text
You are an expert software debugger using Chain-of-Thought reasoning to systematically identify and fix bugs.

## Bug Report

**Description:** [BUG_DESCRIPTION]

**Error Message:**
```

[ERROR_MESSAGE_OR_STACK_TRACE]

```text

**Reproduction Steps:**
[REPRODUCTION_STEPS]

**Expected Behavior:** [EXPECTED_BEHAVIOR]

**Actual Behavior:** [ACTUAL_BEHAVIOR]

**Environment:**
- OS: [OPERATING_SYSTEM]
- Runtime: [RUNTIME_VERSION]
- Dependencies: [KEY_DEPENDENCIES]

**Relevant Code:**
```[LANGUAGE]
[CODE_SNIPPET]
```text

**Additional Context:** [LOGS_TELEMETRY_OR_OTHER_INFO]

---

## Task

Using Chain-of-Thought reasoning, debug this issue systematically:

### Step 1: Symptom Analysis

Analyze the symptoms. What is the observable problem? What does the error message tell us? What are the key clues in the stack trace, logs, or telemetry?

### Step 2: Hypothesis Generation

Generate 3–5 hypotheses about what might be causing this issue. For each hypothesis:

- State the hypothesis clearly
- Explain the reasoning (why this might be the cause)
- Identify what evidence would support or refute it

### Step 3: Hypothesis Prioritization

Rank the hypotheses by:

- Likelihood (based on symptoms and code)
- Ease of testing (can we validate this quickly?)

### Step 4: Experiment Design

For the top 2–3 hypotheses, design experiments to test them:

- What code changes or tests would validate/falsify the hypothesis?
- What specific values, inputs, or conditions should we check?
- What output or behavior would confirm or deny the hypothesis?

### Step 5: Root Cause Identification

Based on the analysis and experiments, identify the root cause:

- State the root cause clearly
- Provide evidence (from code, logs, or reasoning)
- Explain why other hypotheses were ruled out

### Step 6: Proposed Fix

Propose a minimal, testable fix:

- Provide a code snippet (if applicable)
- Explain why this fix addresses the root cause
- Note any trade-offs or risks
- Suggest where the fix should be applied

### Step 7: Regression Tests

Propose test cases to prevent this bug from recurring:

- Unit tests for the specific failure mode
- Integration tests if multiple components are involved
- Edge cases that should now be covered

### Step 8: Verification Steps

List steps to verify the fix works:

1. Run the reproduction steps with the fix applied
2. Run the regression tests
3. Check for unintended side effects

---

## Output Format

**Symptom Summary:**
[concise description of the observed problem]

**Initial Hypotheses:**

1. [Hypothesis 1] - Likelihood: [High/Medium/Low], Evidence: [what would support it]
2. [Hypothesis 2] - ...
3. [Hypothesis 3] - ...

**Experiment Design:**

- Hypothesis 1: [test approach]
- Hypothesis 2: [test approach]

**Root Cause:**
[evidence-based conclusion about what's causing the bug]

**Proposed Fix:**

```[LANGUAGE]
[code snippet or description]
```text

*Rationale:* [why this fixes the root cause]

**Regression Tests:**

- Test 1: [scenario]
- Test 2: [scenario]

**Verification Steps:**

1. [step 1]
2. [step 2]
3. [step 3]

```

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

## Example Usage

**Input:**

```text

You are an expert software debugger using Chain-of-Thought reasoning to systematically identify and fix bugs.

## Bug Report

**Description:** User authentication fails intermittently in production (~5% of requests)

**Error Message:**

```

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

**Output:**

```markdown
**Symptom Summary:**
JWT token verification fails intermittently (~5%) in production with "invalid signature" error. Issue is environment-specific (multi-server, load-balanced) and timing-dependent (within token validity period).

**Initial Hypotheses:**
1. **JWT_SECRET mismatch across servers** - Likelihood: High
   - Evidence: Issue only occurs in multi-server setup, not single-server staging
   - Support: Different secrets would cause signature verification to fail on different servers
   
2. **Clock skew between servers** - Likelihood: Medium
   - Evidence: Timing-dependent failure (~5% suggests occasional, not systematic)
   - Support: JWT exp/iat claims could fail validation if server clocks are out of sync
   
3. **Race condition in token issuance** - Likelihood: Low
   - Evidence: Failures are on verification, not issuance
   - Support: Would require token to be used before it's fully written, unlikely with this code

**Experiment Design:**
- Hypothesis 1: Check `process.env.JWT_SECRET` on all production servers. If different, verification would fail when request hits server with different secret.
- Hypothesis 2: Compare server clocks (use `date` command or NTP status). If >30s skew, could cause exp/iat validation issues.

**Root Cause:**
JWT_SECRET environment variable is not synchronized across all servers in the load-balanced pool. When a token is issued by Server A (with SECRET_A) and verified by Server B (with SECRET_B), signature verification fails.

**Evidence:**
- Issue only occurs in multi-server production (not single-server staging)
- ~5% failure rate likely corresponds to proportion of requests hitting mismatched server
- "invalid signature" error is consistent with secret mismatch

**Proposed Fix:**
```javascript
// Option 1: Use centralized secret management (recommended)
// Deploy this change to ensure all servers use the same secret:

// config.js
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager();

async function getJwtSecret() {
  const data = await secretsManager.getSecretValue({ 
    SecretId: 'prod/jwt-secret' 
  }).promise();
  return JSON.parse(data.SecretString).JWT_SECRET;
}

module.exports = { getJwtSecret };

// auth.js
const { getJwtSecret } = require('./config');

let cachedSecret = null;

async function verifyToken(token) {
  if (!cachedSecret) {
    cachedSecret = await getJwtSecret();
  }
  return jwt.verify(token, cachedSecret, { algorithms: ['HS256'] });
}

// Option 2: Short-term fix (if centralized secret management unavailable)
// Manually sync JWT_SECRET environment variable across all servers
// Use deployment scripts to ensure consistency
```text

*Rationale:* The root cause is environment variable inconsistency. Centralized secret management (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) ensures all servers use the same secret without manual sync. Option 2 is a temporary workaround.

**Regression Tests:**

- **Test 1:** Multi-server integration test
  - Start 3 instances of the app with load balancer
  - Issue token from instance 1
  - Verify token succeeds on instances 1, 2, 3
  
- **Test 2:** Secret rotation test
  - Rotate JWT_SECRET
  - Verify all servers pick up new secret
  - Verify tokens issued before rotation fail gracefully

- **Test 3:** Clock skew test (rule out hypothesis 2)
  - Artificially skew server clock by ±60s
  - Verify tokens still validate correctly

**Verification Steps:**

1. Deploy centralized secret management to staging (multi-server setup)
2. Run load test with 10,000 requests across all servers
3. Verify 0% authentication failures
4. Deploy to production and monitor error rates for 24 hours
5. Verify authentication error rate drops to <0.01%

```

## Tips

- **Start broad, narrow down:** Generate multiple hypotheses, then prioritize and test systematically
- **Use evidence, not intuition:** Every hypothesis and conclusion should be backed by observable evidence
- **Test one variable at a time:** Design experiments that isolate specific causes
- **Consider the environment:** Many bugs are environment-specific (multi-server, race conditions, resource limits)
- **Propose minimal fixes:** Avoid over-engineering; fix the root cause with minimal code changes
- **Always include regression tests:** Prevent the bug from recurring
- **Document reasoning:** Visible CoT reasoning helps others learn and validates your logic

## Related Prompts

- [Chain-of-Thought: Performance Analysis](chain-of-thought-performance-analysis.md) - For performance debugging
- [Reflection: Code Review Self-Check](../developers/reflection-code-review-self-check.md) - For validating fixes
- [Tree-of-Thoughts: Architecture Evaluator](tree-of-thoughts-architecture-evaluator.md) - For complex system issues
- [ReAct: Codebase Navigator](react-codebase-navigator.md) - For exploring unfamiliar code

## Governance Notes

- **PII Safety:** Ensure bug reports and logs don't contain PII (user IDs, emails, passwords, tokens)
- **Security:** Redact secrets, API keys, and credentials from error messages and code snippets
- **Human Review:** Critical production bugs should be reviewed by senior engineers before deployment
- **Audit Trail:** Save complete CoT reasoning for postmortems and knowledge sharing
- **Cost:** CoT debugging can be token-intensive; use for non-trivial bugs where systematic analysis adds value

## Changelog

- 2025-11-18: Initial version based on ToT repository evaluation recommendations
