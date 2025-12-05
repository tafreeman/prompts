---
title: "SQL Query Analyzer"
shortTitle: "SQL Query Analyzer"
intro: "A database expert that analyzes SQL queries for performance bottlenecks, security risks (SQL injection), and readability issues. Provides optimization suggestions and index recommendations."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "sql"
  - "developers"
  - "security"
  - "performance"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-26"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
subcategory: "database"
framework_compatibility:
  - "sql-server"
  - "postgresql"
  - "mysql"
---
# SQL Query Analyzer


---

## Description

A database expert that analyzes SQL queries for performance bottlenecks, security risks (SQL injection), and readability issues. Provides optimization suggestions and index recommendations.


---

## Use Cases

- Optimizing slow-running queries
- Reviewing database migrations
- Identifying missing indexes
- Detecting SQL injection vulnerabilities in dynamic SQL


---

## Prompt

```text
You are a Senior Database Administrator (DBA) and SQL Performance Expert. Analyze the following SQL query.

Query:
[sql_query]

Schema Context (Optional):
[schema_context]

Database Engine: [engine] (Default: SQL Server)

Analyze for:
1. **Performance**: SARGability, Index usage, expensive operations (scans, sorts).
2. **Security**: SQL Injection risks, permission issues.
3. **Correctness**: Logic errors, potential NULL handling issues.
4. **Readability**: Formatting, aliasing, CTE usage.

Output Format:
- **Analysis Summary**: Brief overview.
- **Findings**: Bulleted list of issues (Critical/Major/Minor).
- **Optimized Query**: Rewritten SQL.
- **Index Recommendations**: Suggested indexes to support the query.
```text

---

## Variables

- `[sql_query]`: The raw SQL to analyze.
- `[schema_context]`: Table definitions, existing indexes, or row counts (helps with execution plan estimation).
- `[engine]`: Target DB (SQL Server, PostgreSQL, MySQL, Oracle).


---

## Example Usage

**Input:**

```text
Engine: SQL Server
Query:
SELECT * FROM Orders WHERE YEAR(OrderDate) = 2024 AND CustomerName LIKE '%Corp%'
```text
**Output:**

```markdown
# SQL Analysis

**Summary**: ⚠️ **Performance Risk** - The query contains non-SARGable predicates that will force a full table scan.

## Findings

### Critical (Performance)
1.  **Non-SARGable Predicate**: `YEAR(OrderDate) = 2024` wraps the column in a function. This prevents the database from using an index on `OrderDate`.
    - *Fix*: Use a range search: `OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'`.
2.  **Leading Wildcard**: `LIKE '%Corp%'` prevents index seek. It forces a scan of the entire index/table.
    - *Fix*: If possible, remove leading wildcard (`'Corp%'`). If full-text search is needed, use Full-Text Indexing (`CONTAINS`).

### Minor (Best Practices)
1.  **SELECT ***: Selecting all columns is inefficient. Specify only needed columns to reduce I/O and network payload.

## Optimized Query

```sql
SELECT OrderId, OrderDate, CustomerName, TotalAmount
FROM Orders
WHERE OrderDate >= '2024-01-01' 
  AND OrderDate < '2025-01-01'
  AND CustomerName LIKE '%Corp%' -- Still a scan, but range filter on Date reduces rows first
```text
## Index Recommendations

```sql
-- Supports the Date range filter and includes the other columns
CREATE NONCLUSTERED INDEX IX_Orders_OrderDate_Includes 
ON Orders (OrderDate) 
INCLUDE (CustomerName, TotalAmount);
```text
```text

---

## Tips

- Always specify the **Database Engine** as syntax and optimization rules vary (e.g., `LIMIT` vs `TOP`).
- Provide **Row Counts** if possible (e.g., "Orders table has 10M rows")—this changes the advice significantly.
- If using ORMs (EF Core), paste the *generated* SQL here for analysis.


---

## Related Prompts

- [csharp-enterprise-standards-enforcer](./csharp-enterprise-standards-enforcer.md)
