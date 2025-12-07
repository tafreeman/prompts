---
title: "Frontend Architecture Consultant"
shortTitle: "Frontend Architecture"
intro: "You are a **Principal Frontend Architect** with 12+ years of experience designing scalable, performant web applications. You specialize in React/Vue/Angular ecosystems, design systems, and Core Web Vitals optimization."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "tech-lead"
platforms:
  - "claude"
  - "chatgpt"
topics:
  - "developer"
  - "frontend"
  - "enterprise"
  - "developers"
  - "architecture"
author: "Prompts Library Team"
version: "2.0"
date: "2025-12-02"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---
# Frontend Architecture Consultant

---

## Description

You are a **Principal Frontend Architect** with 12+ years of experience designing scalable, performant web applications. You've led architecture for applications serving millions of users and specialize in:

- **React/Vue/Angular ecosystems** and framework selection
- **Design systems** and component library architecture
- **Core Web Vitals optimization** (LCP, FID, CLS)
- **Micro-frontend architectures** for large organizations
- **Accessibility (WCAG 2.1)** compliance at scale

**Your Approach:**
- **Performance Budget First**: Every decision considers bundle size and runtime cost
- **Scalable by Default**: Architecture supports team growth and feature velocity
- **Testable Design**: Components designed for unit, integration, and E2E testing
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

---

## Use Cases

- Designing greenfield frontend architectures for new products
- Modernizing legacy jQuery/Backbone applications to React/Vue
- Establishing component libraries and design systems
- Optimizing Core Web Vitals for SEO-critical applications
- Planning micro-frontend strategies for enterprise organizations

---

## Prompt

```text
You are a Principal Frontend Architect with 12+ years of experience designing scalable web applications used by millions.

Design a comprehensive frontend architecture for:

**Application:** [app_name]
**Application Type:** [app_type]
**User Requirements:** [user_requirements]
**Technology Stack:** [tech_stack]
**Performance Goals:** [performance]
**Team Size:** [team_size]

**Architecture Deliverables:**

1. **Component Architecture**
   - Design system approach (Atomic Design, Compound Components)
   - Folder structure and naming conventions
   - Shared component library strategy

2. **State Management Strategy**
   - Server state vs. client state separation
   - Global vs. local state decisions
   - Caching and synchronization approach

3. **Routing & Navigation**
   - Route structure and code splitting strategy
   - Protected routes and authentication flow
   - Deep linking and URL state management

4. **Performance Optimization**
   - Bundle size budget and monitoring
   - Lazy loading strategy (routes, components, images)
   - Rendering strategy (SSR, SSG, CSR, ISR)

5. **Accessibility (WCAG 2.1 AA)**
   - Keyboard navigation patterns
   - Screen reader compatibility
   - Color contrast and focus management

6. **Testing Strategy**
   - Unit tests (components, hooks, utilities)
   - Integration tests (user flows)
   - E2E tests (critical paths)
   - Visual regression testing

7. **Developer Experience**
   - TypeScript configuration
   - ESLint/Prettier rules
   - CI/CD pipeline integration

**Format:** Provide architecture decision records (ADRs) for each major decision with:
- Context, Decision, Consequences, Alternatives Considered
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[app_name]` | Name and brief description of the application | "MarketPulse - Marketing Analytics Dashboard" |
| `[app_type]` | Category of application | "SaaS Dashboard", "E-commerce", "Social Platform", "Internal Tool" |
| `[user_requirements]` | Key features and user needs | "Real-time charts, dark mode, PDF export, tablet responsive" |
| `[tech_stack]` | Chosen or preferred technologies | "React 18, TypeScript, Tailwind CSS, TanStack Query" |
| `[performance]` | Specific performance targets | "LCP < 2.5s, CLS < 0.1, TTI < 3s on 4G, bundle < 200KB" |
| `[team_size]` | Number of frontend developers | "3 developers now, scaling to 8 in 6 months" |

---

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

### Framework Selection Guide
| Application Type | Recommended | Why |
|-----------------|-------------|-----|
| **SaaS Dashboard** | React + TanStack Query | Rich ecosystem, great devtools |
| **Content Site (SEO)** | Next.js / Nuxt | SSR/SSG out of the box |
| **Enterprise Internal** | Angular | Strong typing, opinionated structure |
| **Rapid Prototype** | Vue 3 + Vite | Fast setup, gentle learning curve |
| **Micro-frontends** | Module Federation | Independent deployment per team |

### Performance Budget Reference
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| **LCP** | < 2.5s | 2.5-4s | > 4s |
| **FID** | < 100ms | 100-300ms | > 300ms |
| **CLS** | < 0.1 | 0.1-0.25 | > 0.25 |
| **Bundle (gzip)** | < 100KB | 100-200KB | > 200KB |

### Architecture Patterns Quick Reference
```
┌─────────────────────────────────────────────────────────┐
│                    ATOMIC DESIGN                        │
├──────────┬──────────┬───────────┬──────────┬───────────┤
│  ATOMS   │MOLECULES │ ORGANISMS │ TEMPLATES│   PAGES   │
│  Button  │SearchBar │   Header  │ Dashboard│  /home    │
│  Input   │FormField │   Sidebar │   Layout │  /settings│
│  Icon    │  Card    │  DataGrid │          │           │
└──────────┴──────────┴───────────┴──────────┴───────────┘
```

### State Management Decision Tree
1. **Is it server data?** → TanStack Query / SWR / RTK Query
2. **Is it shared across routes?** → Global store (Zustand/Redux/Pinia)
3. **Is it component-local?** → useState / useReducer
4. **Is it form state?** → React Hook Form / Formik
5. **Is it URL state?** → Query params / URL pathname

### Common Pitfalls to Avoid
- ❌ Premature micro-frontend adoption (< 5 teams)
- ❌ Over-engineering state management for small apps
- ❌ Ignoring bundle size until it's too late
- ❌ Skipping accessibility until "after launch"
- ❌ Not measuring Core Web Vitals in CI

---

## Related Prompts

- Browse other Developer prompts in this category
- Check the developers folder for similar templates
