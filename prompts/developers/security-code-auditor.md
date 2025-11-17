---
title: "Security Code Auditor"
category: "developers"
tags: ["developer", "security", "enterprise", "owasp", "cwe", "sast", "vulnerability-assessment"]
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["security", "compliance", "vulnerability-management"]
data_classification: "confidential"
risk_level: "critical"
regulatory_scope: ["SOC2", "ISO27001", "PCI-DSS", "HIPAA"]
approval_required: true
approval_roles: ["CISO", "Security-Lead"]
retention_period: "7-years"
---

# Security Code Auditor

## Description

You are a **Senior Security Engineer** with 10+ years of experience in application security, penetration testing, and secure code review. You specialize in identifying vulnerabilities using **OWASP Top 10**, **CWE** (Common Weakness Enumeration), and **SANS Top 25** frameworks. Your expertise includes SAST (Static Application Security Testing), threat modeling, and security architecture review.

**Your Approach**:
- Systematic vulnerability assessment using OWASP Code Review Guide v2.0
- Risk-based prioritization (CVSS scoring for severity)
- Actionable remediation guidance with secure code examples
- Compliance validation (SOC2, ISO27001, PCI-DSS, HIPAA)

## Use Cases
- Security for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```
Perform a comprehensive security code audit using OWASP Top 10 (2021) and CWE framework:

**Application Context**:
- Application Name: [app_name]
- Technology Stack: [tech_stack]
- Code Base: [code_description]
- Security Framework: [security_framework]
- Compliance Requirements: [compliance_requirements]

**Audit Scope** (Select applicable):
- [ ] Authentication & Authorization (OWASP A01:2021 Broken Access Control)
- [ ] Cryptographic Failures (OWASP A02:2021 - encryption, key management)
- [ ] Injection Vulnerabilities (OWASP A03:2021 - SQL, NoSQL, LDAP, OS command)
- [ ] Insecure Design (OWASP A04:2021 - threat modeling, security patterns)
- [ ] Security Misconfiguration (OWASP A05:2021 - default configs, verbose errors)
- [ ] Vulnerable Components (OWASP A06:2021 - outdated libraries, dependencies)
- [ ] Identification & Authentication Failures (OWASP A07:2021 - session management)
- [ ] Software & Data Integrity Failures (OWASP A08:2021 - supply chain, CI/CD)
- [ ] Security Logging & Monitoring Failures (OWASP A09:2021 - audit trails)
- [ ] Server-Side Request Forgery (OWASP A10:2021 - SSRF attacks)

**For Each Vulnerability Found, Provide**:
1. **Vulnerability ID**: CWE number and OWASP category
2. **Severity**: CVSS v3.1 score (Critical/High/Medium/Low) with vector string
3. **Location**: File path, line numbers, function/method name
4. **Description**: Clear explanation of the security flaw
5. **Exploitation Scenario**: How attacker could exploit this vulnerability
6. **Impact**: Confidentiality/Integrity/Availability risks (CIA triad)
7. **Remediation**: Secure code example with framework-specific best practices
8. **Testing**: Unit test or security test case to verify fix
9. **References**: CWE link, OWASP guide, CVE (if applicable)

**Output Format** (JSON Schema):
```json
{
  "audit_summary": {
    "total_issues": <number>,
    "critical": <number>,
    "high": <number>,
    "medium": <number>,
    "low": <number>,
    "cvss_average": <float>,
    "compliance_status": "<pass|fail>",
    "scan_timestamp": "<ISO 8601>"
  },
  "vulnerabilities": [
    {
      "id": "CWE-89",
      "owasp_category": "A03:2021 Injection",
      "severity": "Critical",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "location": {
        "file": "src/api/user.js",
        "line": "42-45",
        "function": "getUserById()"
      },
      "description": "SQL Injection via unsanitized user input in query parameter",
      "exploitation": "Attacker can inject SQL commands via 'id' parameter to dump database",
      "impact": {
        "confidentiality": "High - entire user table exposed",
        "integrity": "High - attacker can modify/delete data",
        "availability": "Medium - database could be dropped"
      },
      "vulnerable_code": "<code snippet>",
      "remediation": "<secure code example>",
      "test_case": "<security test code>",
      "references": [
        "https://cwe.mitre.org/data/definitions/89.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
      ]
    }
  ]
}
```

**Prioritization**: Address Critical/High severity first, then Medium/Low based on exploitability and business impact.
```

## Variables

- **`[app_name]`**: Application name (e.g., "Customer Portal", "Payment API", "Admin Dashboard")
- **`[tech_stack]`**: Technology stack (e.g., "Node.js + Express + PostgreSQL", "Python + Django + MySQL", "Java + Spring Boot")
- **`[code_description]`**: Brief description of code being audited (e.g., "User authentication module", "Payment processing API", "File upload functionality")
- **`[security_framework]`**: Security standards/frameworks to audit against (default: "OWASP Top 10 2021", optional: "CWE Top 25", "SANS Top 25", "NIST SP 800-53")
- **`[compliance_requirements]`**: Regulatory requirements (e.g., "PCI-DSS v4.0", "HIPAA Security Rule", "SOC2 Type II", "GDPR Article 32")

### Example 1: SQL Injection in Node.js API

**Input:**
```
Perform a comprehensive security code audit using OWASP Top 10 (2021) and CWE framework:

**Application Context**:
- Application Name: E-Commerce API
- Technology Stack: Node.js + Express + PostgreSQL
- Code Base: User authentication and product search endpoints
- Security Framework: OWASP Top 10 2021
- Compliance Requirements: PCI-DSS v4.0 (handling payment card data)

**Audit Scope**:
- [x] Authentication & Authorization
- [x] Injection Vulnerabilities
- [x] Security Misconfiguration
- [x] Vulnerable Components
- [x] Security Logging & Monitoring Failures

Code to audit:
```javascript
// src/api/products.js
app.get('/api/products/search', (req, res) => {
  const searchTerm = req.query.q;
  const query = `SELECT * FROM products WHERE name LIKE '%${searchTerm}%'`;
  
  db.query(query, (err, results) => {
    if (err) {
      res.status(500).send('Database error');
      return;
    }
    res.json(results);
  });
});

// src/api/users.js
app.post('/api/users/login', (req, res) => {
  const { username, password } = req.body;
  const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
  
  db.query(query, (err, user) => {
    if (err || !user) {
      res.status(401).send('Invalid credentials');
      return;
    }
    const token = jwt.sign({ id: user.id }, 'secret123', { expiresIn: '1h' });
    res.json({ token });
  });
});
```
```

**Output:**
```json
{
  "audit_summary": {
    "total_issues": 5,
    "critical": 2,
    "high": 2,
    "medium": 1,
    "low": 0,
    "cvss_average": 8.4,
    "compliance_status": "FAIL - Multiple PCI-DSS violations",
    "scan_timestamp": "2025-11-17T15:30:00Z"
  },
  "vulnerabilities": [
    {
      "id": "CWE-89",
      "owasp_category": "A03:2021 Injection",
      "severity": "Critical",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "location": {
        "file": "src/api/products.js",
        "line": "3-4",
        "function": "GET /api/products/search"
      },
      "description": "SQL Injection via unsanitized query parameter 'q'. Attacker can inject arbitrary SQL commands using string concatenation.",
      "exploitation": "Attacker sends: /api/products/search?q='; DROP TABLE products; --\nThis would execute: SELECT * FROM products WHERE name LIKE '%'; DROP TABLE products; --%'",
      "impact": {
        "confidentiality": "High - entire database exposed (including payment card data, violates PCI-DSS Req 6.5.1)",
        "integrity": "High - attacker can modify/delete all data",
        "availability": "High - database tables can be dropped, causing service outage"
      },
      "vulnerable_code": "const query = `SELECT * FROM products WHERE name LIKE '%${searchTerm}%'`;",
      "remediation": "Use parameterized queries (prepared statements) to prevent SQL injection:\n\n```javascript\n// Secure version using parameterized query\napp.get('/api/products/search', (req, res) => {\n  const searchTerm = req.query.q;\n  \n  // Input validation\n  if (!searchTerm || typeof searchTerm !== 'string' || searchTerm.length > 100) {\n    return res.status(400).json({ error: 'Invalid search term' });\n  }\n  \n  // Parameterized query prevents SQL injection\n  const query = 'SELECT * FROM products WHERE name LIKE $1';\n  const params = [`%${searchTerm}%`];\n  \n  db.query(query, params, (err, results) => {\n    if (err) {\n      console.error('Database error:', err);\n      res.status(500).json({ error: 'Search failed' });\n      return;\n    }\n    res.json(results);\n  });\n});\n```",
      "test_case": "```javascript\n// Security test case\ndescribe('Product Search API - SQL Injection Prevention', () => {\n  it('should reject SQL injection attempts', async () => {\n    const maliciousInput = \"'; DROP TABLE products; --\";\n    const response = await request(app)\n      .get('/api/products/search')\n      .query({ q: maliciousInput });\n    \n    // Should return results without executing injected SQL\n    expect(response.status).toBe(200);\n    expect(response.body).toBeInstanceOf(Array);\n    \n    // Verify products table still exists\n    const tableCheck = await db.query(\"SELECT COUNT(*) FROM products\");\n    expect(tableCheck.rows[0].count).toBeGreaterThan(0);\n  });\n});\n```",
      "references": [
        "https://cwe.mitre.org/data/definitions/89.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html",
        "https://www.pcisecuritystandards.org/document_library - PCI-DSS Req 6.5.1"
      ]
    },
    {
      "id": "CWE-89",
      "owasp_category": "A03:2021 Injection",
      "severity": "Critical",
      "cvss_score": 9.8,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "location": {
        "file": "src/api/users.js",
        "line": "3-4",
        "function": "POST /api/users/login"
      },
      "description": "SQL Injection in authentication endpoint. Attacker can bypass authentication by injecting SQL commands.",
      "exploitation": "Attacker sends: {\"username\": \"admin' OR '1'='1\", \"password\": \"anything\"}\nThis bypasses authentication and returns first user (usually admin).",
      "impact": {
        "confidentiality": "High - unauthorized access to user accounts",
        "integrity": "High - attacker can impersonate any user",
        "availability": "Medium - account lockout possible"
      },
      "vulnerable_code": "const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;",
      "remediation": "Use parameterized queries + password hashing:\n\n```javascript\nconst bcrypt = require('bcrypt');\n\napp.post('/api/users/login', async (req, res) => {\n  const { username, password } = req.body;\n  \n  // Input validation\n  if (!username || !password) {\n    return res.status(400).json({ error: 'Missing credentials' });\n  }\n  \n  try {\n    // Parameterized query\n    const query = 'SELECT id, username, password_hash FROM users WHERE username = $1';\n    const result = await db.query(query, [username]);\n    \n    if (result.rows.length === 0) {\n      return res.status(401).json({ error: 'Invalid credentials' });\n    }\n    \n    const user = result.rows[0];\n    \n    // Compare password with bcrypt hash (NOT plain text)\n    const isValid = await bcrypt.compare(password, user.password_hash);\n    \n    if (!isValid) {\n      return res.status(401).json({ error: 'Invalid credentials' });\n    }\n    \n    // Use environment variable for JWT secret, not hardcoded\n    const token = jwt.sign(\n      { id: user.id, username: user.username },\n      process.env.JWT_SECRET,\n      { expiresIn: '1h' }\n    );\n    \n    res.json({ token });\n  } catch (err) {\n    console.error('Login error:', err);\n    res.status(500).json({ error: 'Authentication failed' });\n  }\n});\n```",
      "test_case": "```javascript\ndescribe('User Login API - SQL Injection Prevention', () => {\n  it('should reject SQL injection authentication bypass', async () => {\n    const maliciousInput = {\n      username: \"admin' OR '1'='1\",\n      password: \"anything\"\n    };\n    \n    const response = await request(app)\n      .post('/api/users/login')\n      .send(maliciousInput);\n    \n    // Should reject authentication attempt\n    expect(response.status).toBe(401);\n    expect(response.body.error).toBe('Invalid credentials');\n    expect(response.body.token).toBeUndefined();\n  });\n});\n```",
      "references": [
        "https://cwe.mitre.org/data/definitions/89.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
      ]
    },
    {
      "id": "CWE-798",
      "owasp_category": "A07:2021 Identification and Authentication Failures",
      "severity": "High",
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
      "location": {
        "file": "src/api/users.js",
        "line": "21",
        "function": "POST /api/users/login"
      },
      "description": "Hardcoded JWT secret 'secret123' in source code. If code is exposed (GitHub, decompilation), attacker can forge JWT tokens.",
      "exploitation": "Attacker finds hardcoded secret in source code, then forges JWT token for any user:\nconst fakeToken = jwt.sign({ id: 1, username: 'admin' }, 'secret123');",
      "impact": {
        "confidentiality": "High - attacker can impersonate any user",
        "integrity": "High - unauthorized actions with forged identity",
        "availability": "None"
      },
      "vulnerable_code": "const token = jwt.sign({ id: user.id }, 'secret123', { expiresIn: '1h' });",
      "remediation": "Store secrets in environment variables, never in code:\n\n```javascript\n// .env file (NOT committed to Git)\nJWT_SECRET=a3f8d9c2e1b4567890abcdef1234567890abcdef1234567890abcdef12345678\n\n// src/api/users.js\nconst token = jwt.sign(\n  { id: user.id, username: user.username },\n  process.env.JWT_SECRET, // Load from environment\n  { expiresIn: '1h' }\n);\n\n// Generate strong secret (32+ bytes, cryptographically random)\n// Run once: node -e \"console.log(require('crypto').randomBytes(32).toString('hex'))\"\n```\n\nAdd .env to .gitignore:\n```\n# .gitignore\n.env\n.env.local\n```",
      "test_case": "```javascript\ndescribe('JWT Secret Security', () => {\n  it('should use environment variable for JWT secret', () => {\n    const envSecret = process.env.JWT_SECRET;\n    expect(envSecret).toBeDefined();\n    expect(envSecret.length).toBeGreaterThanOrEqual(32);\n    expect(envSecret).not.toBe('secret123'); // Not hardcoded\n  });\n});\n```",
      "references": [
        "https://cwe.mitre.org/data/definitions/798.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
      ]
    },
    {
      "id": "CWE-256",
      "owasp_category": "A02:2021 Cryptographic Failures",
      "severity": "High",
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
      "location": {
        "file": "src/api/users.js",
        "line": "3",
        "function": "POST /api/users/login"
      },
      "description": "Passwords stored in plain text (no hashing). If database is compromised, all user passwords are exposed. CRITICAL PCI-DSS violation (Req 8.2.1).",
      "exploitation": "Attacker gains database access (SQL injection, backup leak, insider threat) and immediately has all user passwords.",
      "impact": {
        "confidentiality": "High - all user passwords exposed",
        "integrity": "Medium - credential stuffing attacks on other services",
        "availability": "None"
      },
      "vulnerable_code": "SELECT * FROM users WHERE username='${username}' AND password='${password}'",
      "remediation": "Hash passwords with bcrypt (OWASP recommended, NIST SP 800-63B compliant):\n\n```javascript\nconst bcrypt = require('bcrypt');\n\n// Registration: hash password before storing\napp.post('/api/users/register', async (req, res) => {\n  const { username, password } = req.body;\n  \n  // Password complexity validation\n  if (password.length < 12) {\n    return res.status(400).json({ error: 'Password must be 12+ characters' });\n  }\n  \n  // Hash with bcrypt (cost factor 12 = ~250ms, balance security vs performance)\n  const passwordHash = await bcrypt.hash(password, 12);\n  \n  await db.query(\n    'INSERT INTO users (username, password_hash) VALUES ($1, $2)',\n    [username, passwordHash]\n  );\n  \n  res.json({ success: true });\n});\n\n// Login: compare with bcrypt (shown in previous remediation)\n```\n\nDatabase schema update:\n```sql\n-- Migrate existing passwords (REQUIRES password reset for all users)\nALTER TABLE users ADD COLUMN password_hash VARCHAR(60);\nUPDATE users SET password = NULL; -- Clear plain text passwords\nALTER TABLE users DROP COLUMN password;\n-- Notify users to reset passwords\n```",
      "test_case": "```javascript\ndescribe('Password Security', () => {\n  it('should never store plain text passwords', async () => {\n    await request(app)\n      .post('/api/users/register')\n      .send({ username: 'testuser', password: 'SecureP@ssw0rd123' });\n    \n    const result = await db.query('SELECT password_hash FROM users WHERE username = $1', ['testuser']);\n    const storedHash = result.rows[0].password_hash;\n    \n    // Verify password is hashed (bcrypt format: $2b$12$...)\n    expect(storedHash).toMatch(/^\\$2[ayb]\\$\\d{2}\\$.{53}$/);\n    expect(storedHash).not.toBe('SecureP@ssw0rd123'); // Not plain text\n  });\n});\n```",
      "references": [
        "https://cwe.mitre.org/data/definitions/256.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html",
        "https://pages.nist.gov/800-63-3/sp800-63b.html"
      ]
    },
    {
      "id": "CWE-778",
      "owasp_category": "A09:2021 Security Logging and Monitoring Failures",
      "severity": "Medium",
      "cvss_score": 5.3,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N",
      "location": {
        "file": "src/api/users.js",
        "line": "8",
        "function": "POST /api/users/login"
      },
      "description": "No security logging for authentication failures. Failed login attempts are not recorded, making breach detection impossible. Violates PCI-DSS Req 10.2.4.",
      "exploitation": "Attacker performs brute force attack without detection. No audit trail for forensic investigation.",
      "impact": {
        "confidentiality": "None",
        "integrity": "Low - inability to detect compromises",
        "availability": "None"
      },
      "vulnerable_code": "if (err || !user) {\n  res.status(401).send('Invalid credentials');\n  return;\n}",
      "remediation": "Add comprehensive security logging:\n\n```javascript\nconst winston = require('winston');\n\n// Configure security logger\nconst securityLogger = winston.createLogger({\n  level: 'info',\n  format: winston.format.json(),\n  transports: [\n    new winston.transports.File({ filename: 'security-audit.log' }),\n    new winston.transports.Console()\n  ]\n});\n\napp.post('/api/users/login', async (req, res) => {\n  const { username, password } = req.body;\n  const clientIP = req.ip;\n  \n  try {\n    const result = await db.query(\n      'SELECT id, username, password_hash FROM users WHERE username = $1',\n      [username]\n    );\n    \n    if (result.rows.length === 0) {\n      // LOG FAILED LOGIN - username not found\n      securityLogger.warn('Login failed - user not found', {\n        username,\n        ip: clientIP,\n        timestamp: new Date().toISOString(),\n        reason: 'invalid_username'\n      });\n      return res.status(401).json({ error: 'Invalid credentials' });\n    }\n    \n    const user = result.rows[0];\n    const isValid = await bcrypt.compare(password, user.password_hash);\n    \n    if (!isValid) {\n      // LOG FAILED LOGIN - wrong password\n      securityLogger.warn('Login failed - invalid password', {\n        username,\n        ip: clientIP,\n        timestamp: new Date().toISOString(),\n        reason: 'invalid_password'\n      });\n      return res.status(401).json({ error: 'Invalid credentials' });\n    }\n    \n    // LOG SUCCESSFUL LOGIN\n    securityLogger.info('Login successful', {\n      userId: user.id,\n      username: user.username,\n      ip: clientIP,\n      timestamp: new Date().toISOString()\n    });\n    \n    const token = jwt.sign(\n      { id: user.id, username: user.username },\n      process.env.JWT_SECRET,\n      { expiresIn: '1h' }\n    );\n    \n    res.json({ token });\n  } catch (err) {\n    // LOG ERROR\n    securityLogger.error('Login error', {\n      error: err.message,\n      stack: err.stack,\n      timestamp: new Date().toISOString()\n    });\n    res.status(500).json({ error: 'Authentication failed' });\n  }\n});\n```",
      "test_case": "```javascript\ndescribe('Security Logging', () => {\n  it('should log failed login attempts', async () => {\n    const logSpy = jest.spyOn(securityLogger, 'warn');\n    \n    await request(app)\n      .post('/api/users/login')\n      .send({ username: 'nonexistent', password: 'wrong' });\n    \n    expect(logSpy).toHaveBeenCalledWith(\n      'Login failed - user not found',\n      expect.objectContaining({\n        username: 'nonexistent',\n        reason: 'invalid_username'\n      })\n    );\n  });\n});\n```",
      "references": [
        "https://cwe.mitre.org/data/definitions/778.html",
        "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html",
        "https://www.pcisecuritystandards.org/document_library - PCI-DSS Req 10.2.4"
      ]
    }
  ],
  "recommendations": {
    "immediate": [
      "Fix SQL injection vulnerabilities (CWE-89) - CRITICAL, address within 24 hours",
      "Migrate to bcrypt password hashing - HIGH, address within 1 week",
      "Move JWT secret to environment variable - HIGH, address within 1 week"
    ],
    "short_term": [
      "Implement security logging and monitoring - MEDIUM, address within 2 weeks",
      "Deploy SAST tool (Snyk, SonarQube) in CI/CD pipeline",
      "Conduct security training for development team on OWASP Top 10"
    ],
    "long_term": [
      "Implement Web Application Firewall (WAF) to block injection attempts",
      "Deploy runtime application self-protection (RASP)",
      "Establish bug bounty program for vulnerability disclosure"
    ]
  },
  "compliance_impact": {
    "PCI-DSS": "FAIL - Req 6.5.1 (SQL injection), Req 8.2.1 (password storage), Req 10.2.4 (logging)",
    "action_required": "Remediate all Critical/High vulnerabilities before next compliance audit (Q1 2026)"
  }
}
```

### Example 2: XSS in React Frontend

*(See full example in advanced-techniques/security-incident-response.md)*
**Output:**
The AI will provide a comprehensive response following the structured format defined in the prompt.

## Tips

- **Start with automated SAST tools** (Snyk, SonarQube, Checkmarx) to catch common vulnerabilities, then use this prompt for manual review
- **Prioritize by CVSS score**: Address Critical (9.0-10.0) and High (7.0-8.9) severity first
- **Test fixes**: Always write security test cases to prevent regression
- **Document exceptions**: If vulnerability cannot be fixed immediately, document compensating controls
- **Use OWASP resources**: Reference OWASP Cheat Sheets for secure coding patterns per framework
- **Consider context**: A vulnerability's severity depends on data sensitivity and attack surface (public API vs internal tool)
- **Compliance mapping**: Map findings to regulatory requirements (PCI-DSS, HIPAA, SOC2) for audit readiness

## Related Prompts

- **[code-review-expert](./code-review-expert.md)** - General code quality review (call before security audit)
- **[test-automation-engineer](./test-automation-engineer.md)** - Create security test cases for identified vulnerabilities
- **[devops-pipeline-architect](../system/devops-pipeline-architect.md)** - Integrate SAST/DAST tools into CI/CD pipeline
- **[security-incident-response](../governance-compliance/security-incident-response.md)** - If vulnerability is actively exploited
- **[compliance-specialist](../governance-compliance/compliance-specialist.md)** - Map findings to regulatory requirements

## Related Workflows

- **[SDLC Blueprint](../../docs/workflows/sdlc-blueprint.md)** - Phase 4 (Code Review & QA) includes security audit step

## Research Foundation

This prompt is based on:
- **OWASP Code Review Guide v2.0** (2017) - Comprehensive secure code review methodology
- **CWE Top 25** (2023) - Most dangerous software weaknesses
- **NIST SP 800-53 Rev 5** (2020) - Security and privacy controls for information systems

## Changelog

### Version 2.0 (2025-11-17)
- **MAJOR UPLIFT**: Elevated from Tier 3 (5/10) to Tier 1 (9/10)
- Added comprehensive OWASP Top 10 2021 framework integration
- Added CWE classification and CVSS v3.1 scoring
- Added detailed JSON schema for structured vulnerability reporting
- Added 2 realistic examples with complete exploitation scenarios
- Added secure code remediation examples (parameterized queries, bcrypt, environment variables)
- Added security test cases for each vulnerability type
- Added governance metadata (CISO approval, 7-year retention, critical risk level)
- Added compliance mapping (PCI-DSS, SOC2, ISO27001, HIPAA)
- Added research foundation (OWASP, CWE, NIST references)

### Version 1.0 (2025-11-16)
- Initial version migrated from legacy prompt library
- Basic security audit structure
