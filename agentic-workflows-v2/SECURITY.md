# Security Policy

## Supported Versions

This project is under active development. Security fixes are applied to the default branch first.

| Version | Supported |
| --- | --- |
| `main` / latest | Yes |
| Older snapshots | Best effort |

## Reporting a Vulnerability

Please do not open public issues for suspected vulnerabilities.

Use one of these private paths:
- Create a GitHub Security Advisory draft (preferred), or
- Contact maintainers through the private support path in `SUPPORT.md`.

## What to Include

- Affected component and file path
- Reproduction steps or proof of concept
- Impact assessment (confidentiality, integrity, availability)
- Suggested mitigation (if available)

## Response Targets

- Initial acknowledgment: within 3 business days
- Triage decision: within 7 business days
- Fix timeline: based on severity and complexity

## Disclosure Policy

We follow coordinated disclosure:
- Keep details private until a fix is available
- Publish remediation details after patch release
- Credit reporters who want attribution

## Hardening Guidance for Contributors

- Never commit secrets, credentials, or private datasets
- Keep API keys in environment variables
- Add tests for security-sensitive behavior changes
