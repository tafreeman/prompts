---
applyTo: "**/*.cs,**/*.cshtml"
---

# DoD Security and Compliance Standards

## Security-First Development
- Validate all user inputs using ASP.NET Core model validation
- Implement proper authentication and authorization on all endpoints
- Use HTTPS-only with secure cookie settings
- Sanitize all output to prevent XSS attacks

## DoD Compliance Requirements
- Follow NIST Cybersecurity Framework guidelines
- Implement STIG security controls where applicable
- Ensure FIPS 140-2 compliant cryptographic modules
- Maintain comprehensive security documentation

## Data Protection
- Classify data according to DoD information categories
- Implement data loss prevention (DLP) measures
- Use secure coding practices to prevent OWASP Top 10 vulnerabilities
- Regular security testing and penetration testing compliance

## Audit and Logging
- Log all user actions and system events
- Implement structured logging with correlation IDs
- Ensure log integrity and tamper-evident storage
- Maintain logs for minimum retention periods per DoD requirements