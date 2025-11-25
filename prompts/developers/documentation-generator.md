---

title: "Documentation Generator"
category: "developers"
tags: ["developer", "documentation", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Documentation Generator

## Description

Creates technical documentation

## Use Cases

- Documentation for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Generate comprehensive documentation for:

Project: [project_name]
Audience: [audience]
Documentation Type: [doc_type]
Technical Details: [tech_details]

Include:
1. Architecture overview
2. API documentation
3. Setup instructions
4. Usage examples
5. Troubleshooting guide
6. Contributing guidelines
```

## Variables

- `[audience]`: Audience
- `[doc_type]`: Doc Type
- `[project_name]`: Project Name
- `[tech_details]`: Tech Details

## Example Usage

**Input:**

```text
[project_name]: "PayFast" Payment Gateway SDK
[audience]: External Developers (Integrators)
[doc_type]: API Reference & Integration Guide
[tech_details]: REST API, OAuth 2.0, Webhooks, Idempotency keys, Rate limits
```

**Output:**

```text
## Documentation Plan

### 1. Architecture Overview
*   **Diagram:** Sequence diagram showing the "Checkout Flow" (Client -> Merchant -> PayFast).
*   **Concepts:** Explanation of "Payment Intents" and "Captures".

### 2. API Documentation (OpenAPI/Swagger)
*   **Authentication:** "How to generate API Keys".
*   **Endpoints:** `POST /v1/charges`, `GET /v1/transactions/{id}`.
*   **Parameters:** Clear typing (e.g., `amount`: integer (cents)).

### 3. Usage Examples (Code Snippets)
*   **Languages:** cURL, Python (Requests), Node.js (Axios), Java.
*   **Scenario:** "Creating a one-time charge" vs "Saving a card for later".

### 4. Troubleshooting Guide
*   **Common Errors:** `402 Payment Required` (Card declined), `401 Unauthorized` (Bad API key).
*   **Idempotency:** How to safely retry requests using `Idempotency-Key` header.

[... continues with setup instructions and contributing ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Developer prompts in this category
- Check the developers folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
