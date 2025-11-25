---

title: "Frontend Architecture Consultant"
category: "developers"
tags: ["developer", "frontend", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Frontend Architecture Consultant

## Description

Designs frontend architectures

## Use Cases

- Frontend for Developer persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design frontend architecture for:

Application: [app_name]
User Requirements: [user_requirements]
Technology Stack: [tech_stack]
Performance Goals: [performance]

Provide:
1. Component architecture
2. State management strategy
3. Routing and navigation
4. Performance optimization
5. Accessibility compliance
6. Testing approach
```

## Variables

- `[app_name]`: App Name
- `[performance]`: Performance
- `[tech_stack]`: Tech Stack
- `[user_requirements]`: User Requirements

## Example Usage

**Input:**

```text
[app_name]: "MarketPulse" - Marketing Analytics Dashboard
[user_requirements]: Real-time data visualization, Dark/Light mode toggle, Export to PDF, Responsive for tablets
[tech_stack]: React 18, TypeScript, Tailwind CSS, TanStack Query, Recharts
[performance]: Core Web Vitals (LCP < 2.5s, CLS < 0.1), Time to Interactive < 3s on 4G
```

**Output:**

```text
## Frontend Architecture Design

### 1. Component Architecture
*   **Atomic Design:** Atoms (Buttons), Molecules (SearchField), Organisms (DataGrid), Templates (DashboardLayout).
*   **Composition:** Use "Compound Components" pattern for complex UI widgets (e.g., DateRangePicker).

### 2. State Management Strategy
*   **Server State:** TanStack Query (React Query) for caching API responses and optimistic updates.
*   **Client State:** Zustand for global UI state (Sidebar open/close, Theme preference).
*   **Form State:** React Hook Form for validation performance.

### 3. Performance Optimization
*   **Code Splitting:** Lazy load heavy chart libraries (`React.lazy`) and route-based splitting.
*   **Virtualization:** Use `tanstack-virtual` for rendering large data tables (1000+ rows).

[... continues with accessibility and testing ...]
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
