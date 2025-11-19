---
applyTo: "**/*.sql,**/Migrations/*.cs"
---

# SQL Server Security and STIG Compliance

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