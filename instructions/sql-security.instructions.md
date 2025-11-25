---
applyTo: "**/*.sql,**/Migrations/*.cs"
name: "sql-security-stig-compliance"
description: "Enforce SQL Server security best practices, STIG compliance, and DoD data protection standards"
---

# SQL Server Security and STIG Compliance

> Prompt reference: use `dotnet-prompts/developers/sql-security-standards-enforcer.md` when you need an AI prompt that enforces these requirements in generated SQL.
> Purpose: Ensure all SQL code, migrations, and database configurations meet DoD security and STIG compliance standards.

## Database Security Requirements

- Always use parameterized queries to prevent SQL injection
- Implement least privilege access with role-based security
- Enable Transparent Data Encryption (TDE) for data at rest
- Configure Always Encrypted for sensitive columns (PII, SSN, etc.)

## STIG Compliance Standards

- Audit all database access and modifications
- Implement strong password policies for database accounts
- Use Windows Authentication when possible
- Regular security assessments and vulnerability scans

## Query Standards

- Use stored procedures for complex operations
- Implement proper error handling without exposing system details
- Log all database operations for audit trails
- Optimize queries for performance and resource usage

### Example: Parameterized Query vs SQL Injection Risk

✅ **Correct (parameterized):**

```csharp
using var command = new SqlCommand(
    "SELECT * FROM Users WHERE Email = @email AND IsActive = @isActive", connection);
command.Parameters.AddWithValue("@email", userEmail);
command.Parameters.AddWithValue("@isActive", true);
```

❌ **Avoid (string concatenation – SQL injection risk):**

```csharp
var sql = $"SELECT * FROM Users WHERE Email = '{userEmail}' AND IsActive = 1";
```

### Example: Stored Procedure with Error Handling

✅ **Correct stored procedure:**

```sql
CREATE PROCEDURE [dbo].[uspGetUserById]
    @UserId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT UserId, Email, CreatedAt
        FROM dbo.Users
        WHERE UserId = @UserId AND IsDeleted = 0;
    END TRY
    BEGIN CATCH
        -- Log error without exposing system details
        EXEC uspLogError;
        THROW;
    END CATCH
END
```

## Constraints and Fallbacks

- Do NOT use dynamic SQL or string concatenation for user input; always use parameterized queries or stored procedures.
- When TDE or Always Encrypted cannot be enabled due to legacy constraints, document the risk, implement application-level encryption, and escalate for ATO review.
- If Windows Authentication is unavailable (e.g., cross-platform scenarios), use SQL authentication with strong password policies, rotate credentials quarterly, and log all access.

## Response Format Expectations

When generating or reviewing SQL code, use this structure:

1. **Summary paragraph** – ≤3 sentences describing the SQL operation and which security/STIG controls it satisfies.
2. **Bullet list of security measures** – map to specific sections above (e.g., "Database Security – parameterized query used", "STIG Compliance – audit logging enabled").
3. **SQL code example** – a short snippet (≤2 blocks) showing the correct pattern.
4. **Deviations note** – if any STIG control cannot be met, explain the risk, proposed compensating control, and escalation path.

Always pair these instructions with the referenced prompt whenever generating or reviewing SQL via AI so the standard response structure (summary, standards-linked actions, SQL, deviations) is followed consistently.
