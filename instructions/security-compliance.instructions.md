---
applyTo: "**/*.cs,**/*.cshtml"
name: "dod-security-compliance-standards"
description: "Enforce DoD security controls, NIST, STIG, and FIPS compliance for all code and configurations"
---

# DoD Security and Compliance Standards

> Purpose: Ensure all code, configurations, and deployments meet Department of Defense security requirements, including NIST, STIG, and FIPS 140-2 compliance.

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

### Example: Secure Controller with Validation and Audit Logging

✅ **Correct implementation:**

```csharp
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    [HttpPost]
    public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest request)
    {
        if (!ModelState.IsValid)
        {
            _logger.LogWarning("Invalid user creation request from {User}", User.Identity?.Name);
            return BadRequest(ModelState);
        }

        var user = await _userService.CreateAsync(request);
        _logger.LogInformation("User {UserId} created by {Actor}", user.Id, User.Identity?.Name);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

## Constraints and Fallbacks

- Do NOT disable security features (HTTPS, CSRF, input validation) without written authorization from the Information System Security Officer (ISSO).
- When STIG controls conflict with functional requirements, document the risk, propose compensating controls, and escalate for Authority to Operate (ATO) review.
- If FIPS-compliant cryptography is unavailable in a library, use only approved alternatives from the DoD Approved Products List (APL) or escalate to security architecture.

## Response Format Expectations

When applying these standards, use this structure:

1. **Summary paragraph** – ≤3 sentences describing the security posture and compliance alignment.
2. **Bullet list of controls** – map each implementation detail to a specific DoD/NIST/STIG requirement (e.g., "STIG V-123456 – input validation enforced").
3. **Code example** – a short snippet (≤2 blocks) demonstrating secure implementation.
4. **Compliance deviations** – list any controls not met, the risk level, and proposed compensating controls or waiver process.
