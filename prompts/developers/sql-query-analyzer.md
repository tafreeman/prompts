---
name: SQL Query Analyzer
description: Database expert prompt for analyzing SQL queries for performance, security, and readability.
type: how_to
---
## Description

## Prompt

```sql
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-01';
```

Database expert prompt for analyzing SQL queries for performance, security, and readability.

## Description

## Prompt

```sql
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-01';
```

Database expert prompt for analyzing SQL queries for performance, security, and readability.


# SQL Query Analyzer

## Description

Analyze SQL queries for performance bottlenecks, security risks (SQL injection), and readability. Provide optimization suggestions, index recommendations, and rewritten queries.

## Prompt

You are a Senior Database Engineer.

Analyze the SQL query below for performance, security, and best practices.

### Context
**Database Engine**: [engine]
**Schema**: [schema]
**Query**:
[query]

### Analysis Required
1. **Performance**: Identify slow operations (full table scans, missing indexes).
2. **Security**: Check for SQL injection risks in dynamic SQL.
3. **Readability**: Suggest formatting and naming improvements.
4. **Optimized Query**: Provide a rewritten, optimized version.
5. **Index Recommendations**: Suggest indexes to create.

## Variables

- `[engine]`: E.g., "PostgreSQL", "MySQL", "SQL Server".
- `[schema]`: Table definitions and existing indexes.
- `[query]`: The SQL query to analyze.

## Example

**Input**:
Engine: PostgreSQL
Schema: orders(order_id, order_date, customer_id, total)
Indexes: idx_orders_customer_id
Query:
```sql
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-01';
```

**Response**:
### Performance Issue
- `DATE(order_date)` prevents index usage (function on column).

### Optimized Query
```sql
SELECT * FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2024-01-02';
```

### Index Recommendation
```sql
CREATE INDEX idx_orders_order_date ON orders(order_date);
```## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[engine]` | AUTO-GENERATED: describe `engine` |
| `[query]` | AUTO-GENERATED: describe `query` |
| `[schema]` | AUTO-GENERATED: describe `schema` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

