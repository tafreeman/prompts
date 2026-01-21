---
name: Quality Assurance Planner
description: Develops QA strategies and plans with quality objectives, testing strategies, and continuous improvement.
type: how_to
---

# Quality Assurance Planner

## Description

This prompt develops QA strategies and plans with quality objectives, testing strategies, and continuous improvement frameworks. It helps project managers ensure deliverables meet quality standards throughout the project lifecycle.

## Use Cases

- Quality Assurance for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[project_name]`: Project name (e.g., "Mobile Banking App v3.0 Release")
- `[standards]`: Quality standards (e.g., "ISO 25010, OWASP Mobile Top 10, WCAG 2.1 AA")
- `[deliverables]`: Key deliverables (e.g., "iOS app, Android app, Backend APIs, Admin dashboard")
- `[testing]`: Testing requirements (e.g., "Functional, Performance, Security, Accessibility testing")

## Prompt

### System Prompt

```text
You are a quality assurance expert with experience in software testing, quality management systems, and continuous improvement. You help organizations build quality into their processes rather than inspecting it in at the end.
```

### User Prompt

```text
Develop a QA plan for [project_name].

Quality Context:
- Quality Standards: [standards]
- Key Deliverables: [deliverables]
- Testing Requirements: [testing]

Please provide:
1. Quality objectives and success criteria
2. Testing strategy by type
3. Test environment requirements
4. Defect management process
5. Quality gates and checkpoints
6. Metrics and reporting
7. Continuous improvement approach
```

## Example

### Input

```text
Develop a QA plan for Mobile Banking App v3.0 Release.

Quality Context:
- Quality Standards: ISO 25010, OWASP Mobile Top 10, WCAG 2.1 AA
- Key Deliverables: iOS app, Android app, Backend APIs, Admin dashboard
- Testing Requirements: Functional, Performance, Security, Accessibility testing
```

### Expected Output

```text
## QA Plan: Mobile Banking App v3.0

### Quality Objectives
| Objective | Target | Measurement |
|-----------|--------|-------------|
| Defect density | <0.5 defects/KLOC | Static analysis + testing |
| Test coverage | >80% code coverage | Automated test reports |
| Performance | <2s response time (P95) | Load testing |
| Security | Zero critical vulnerabilities | Penetration testing |
| Accessibility | WCAG 2.1 AA compliant | Automated + manual audit |

### Testing Strategy
| Test Type | Approach | Tools | Coverage |
|-----------|----------|-------|----------|
| Unit | Automated, dev-owned | Jest, XCTest | 80%+ |
| Integration | Automated API testing | Postman, Newman | All endpoints |
| Functional | Manual + automated E2E | Appium, Detox | All user flows |
| Performance | Load and stress testing | k6, Gatling | Critical paths |
| Security | SAST + DAST + Pen test | Snyk, OWASP ZAP | Full app |
| Accessibility | Automated + manual | Axe, VoiceOver | All screens |

### Test Environment Matrix
| Environment | Purpose | Data | Refresh |
|-------------|---------|------|----------|
| Dev | Developer testing | Synthetic | On demand |
| QA | Formal testing | Anonymized prod | Weekly |
| Staging | Pre-prod validation | Prod mirror | Daily |
| Prod | Live | Real | N/A |

### Quality Gates
| Gate | Criteria | Enforced By |
|------|----------|-------------|
| Code Review | 2 approvals, no critical issues | GitHub |
| Build | All unit tests pass, coverage >80% | CI/CD |
| Deploy to QA | Integration tests pass | Pipeline |
| Release | Zero P1/P2 bugs, sign-off complete | Release Manager |

### Defect Severity Matrix
| Severity | Definition | SLA |
|----------|------------|-----|
| P1 Critical | App crash, data loss, security breach | Fix immediately |
| P2 High | Major feature broken, no workaround | Fix within 24 hrs |
| P3 Medium | Feature impacted, workaround exists | Fix within sprint |
| P4 Low | Minor issue, cosmetic | Backlog |

### QA Metrics Dashboard
- Test execution progress (daily)
- Defect discovery rate (daily)
- Defect aging report (weekly)
- Test coverage trend (weekly)
- Quality gate pass rate (per release)
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
