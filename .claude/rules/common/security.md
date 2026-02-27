# Security Guidelines

## Mandatory Security Checks

Before ANY commit:
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized HTML)
- [ ] CSRF protection enabled
- [ ] Authentication/authorization verified
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak sensitive data
- [ ] No PII or model weights in logs

## Secret Management

- NEVER hardcode secrets in source code
- ALWAYS use environment variables or a secret manager
- Validate that required secrets are present at startup
- Rotate any secrets that may have been exposed

## Logging Safety

- Never log API keys, user data, or raw model parameters
- Be cautious with training samples containing PII
- Audit log output regularly
- Compliance requirement: GDPR, CCPA

## AI-Generated Code

- Treat Copilot/Claude output as **untrusted input**
- Always review for correctness, security, and standards adherence
- Run full lint + type check + tests before accepting
- AI does not know your architecture — never blindly accept

## Security Response Protocol

If security issue found:
1. STOP immediately
2. Use **security-reviewer** agent
3. Fix CRITICAL issues before continuing
4. Rotate any exposed secrets
5. Review entire codebase for similar issues
