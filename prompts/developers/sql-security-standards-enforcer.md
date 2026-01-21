---
name: SQL Security Standards Enforcer
description: You are a **Senior Database Security Engineer** and **SQL Server Expert**. Your mission is to enforce strict security standards on T-SQL code, ensuring every query, stored procedure, and view is harde
type: how_to
---

# SQL Security Standards Enforcer


## Prompt

```text
You are a Senior Database Security Engineer and SQL Server expert.

Refactor or review the SQL below to comply with strict SQL security and data-access standards.

Inputs:

- SQL Code: [sql_code]
- Context (optional): [context]
- Constraints (optional): [constraints]

Requirements:
1) Eliminate SQL injection risks (parameterize; avoid unsafe dynamic SQL)
2) Enforce least privilege and secure ownership chaining assumptions
3) Validate/whitelist identifiers that cannot be parameterized (e.g., ORDER BY columns)
4) Avoid SELECT *; minimize sensitive column exposure
5) Add safe error handling patterns where appropriate
6) Provide a short checklist for reviewers and test/verification steps

Return the improved SQL plus a brief explanation of each change.
```

## Variables

- `[sql_code]`: The SQL code to generate, refactor, or review.
- `[context]`: Optional database/schema context (tables, views, security model).
- `[constraints]`: Optional constraints such as legacy schema, existing roles, or performance limits.

## Usage

### Example 1: Refactoring Legacy Dynamic SQL

**Input:**

```text
You are a senior SQL Server engineer and security reviewer. Refactor the following SQL to fully comply with our SQL Security and Data Access Standards.

**Context**: User search feature for an internal employee directory.
**Code**:

```sql

CREATE PROCEDURE SearchEmployees (@Name VARCHAR(100), @SortColumn VARCHAR(50))
AS
BEGIN
    DECLARE @SQL VARCHAR(MAX)
    SET @SQL = 'SELECT * FROM Employees WHERE Name LIKE ''%' + @Name + '%'' ORDER BY ' + @SortColumn
    EXEC(@SQL)
END

```text

```text

**Output:**

```markdown
### Summary
Refactored the insecure dynamic SQL procedure to use `sp_executesql` with parameters and whitelisted sorting columns. This eliminates SQL injection risks and enforces least privilege.

### Standards-Linked Actions

- **Injection Prevention**: Replaced string concatenation with parameterized `sp_executesql` for the `@Name` filter.
- **Injection Prevention**: Implemented strict whitelisting for `@SortColumn` to prevent injection via `ORDER BY`.
- **Data Protection**: Replaced `SELECT *` with explicit column list to minimize data exposure.
- **Secure Coding**: Added schema prefix `dbo.` and input validation.

### SQL Code

```sql

CREATE OR ALTER PROCEDURE dbo.SearchEmployees 
    @Name NVARCHAR(100), 
    @SortColumn NVARCHAR(50) = 'LastName'
AS
BEGIN
    SET NOCOUNT ON;

    -- 1. Input Validation & Normalization
    SET @Name = NULLIF(TRIM(@Name), '');

    -- 2. Whitelist Sorting Columns (Prevention of Injection in ORDER BY)
    DECLARE @SafeSortColumn NVARCHAR(50);

    SELECT @SafeSortColumn = CASE @SortColumn
        WHEN 'FirstName' THEN 'FirstName'
        WHEN 'LastName' THEN 'LastName'
        WHEN 'Department' THEN 'Department'
        ELSE 'LastName' -- Default fallback
    END;

    -- 3. Parameterized Query Execution
    DECLARE @SQL NVARCHAR(MAX);
    SET @SQL = N'
        SELECT EmployeeId, FirstName, LastName, Department, Email 
        FROM dbo.Employees 
        WHERE (@Name IS NULL OR LastName LIKE @NameParam OR FirstName LIKE @NameParam)
        ORDER BY ' + QUOTENAME(@SafeSortColumn);

    -- Execute with parameters
    EXEC sp_executesql 
        @SQL, 
        N'@NameParam NVARCHAR(100)', 
        @NameParam = @Name; -- Pass parameter safely
END
GO

```text

### Deviations and Assumptions

- **Assumption**: The `Employees` table is in the `dbo` schema.
- **Assumption**: `EmployeeId`, `FirstName`, `LastName`, `Department`, `Email` are the only non-sensitive columns needed for search. Excluded `Salary` and `SSN` if they exist.

```text

## Related Prompts

- **[security-code-auditor](./security-code-auditor.md)** - General security audit prompt.
- **[api-design-consultant](./api-design-consultant.md)** - Secure API design often connects to secure databases.

---

## Research Foundation

- **OWASP Top 10 (A03:2021 Injection)** - Primary risk addressed.
- **CIS SQL Server Benchmark** - Industry standard for hardening SQL Server.
- **Microsoft SQL Server Security Best Practices** - Vendor guidance.
