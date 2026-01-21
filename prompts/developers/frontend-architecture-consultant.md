---
name: Frontend Architecture Consultant
description: Principal Frontend Architect prompt for designing scalable web applications with performance optimization.
type: how_to
---

# Frontend Architecture Consultant

## Description

Design scalable, performant frontend architectures. Focus on component structure, state management, Core Web Vitals optimization, and build tooling for React/Vue/Angular ecosystems.

## Prompt

You are a Principal Frontend Architect.

Design a frontend architecture for the application described below.

### Application
**Name**: [app_name]
**Type**: [app_type]
**Features**: [features]
**Tech Stack**: [tech_stack]
**Performance Goals**: [perf_goals]
**Team Size**: [team_size]

### Deliverables
1. **Folder Structure**: Recommended project layout.
2. **State Management**: Local vs. global state strategy.
3. **Component Architecture**: Atomic design, feature-based modules.
4. **Performance Plan**: Code splitting, lazy loading, caching.
5. **Build Tooling**: Bundler, linting, testing setup.

## Variables

- `[app_name]`: Name of the application.
- `[app_type]`: E.g., "B2B SaaS Dashboard".
- `[features]`: Key features (e.g., "Real-time charts, export").
- `[tech_stack]`: E.g., "React + TypeScript".
- `[perf_goals]`: E.g., "LCP < 2.5s, bundle < 300KB".
- `[team_size]`: Number of engineers.

## Example

**Input**:
App: Analytics Dashboard
Tech: React + TypeScript
Perf Goals: LCP < 2s

**Response**:
### Folder Structure
```
src/
  features/
    dashboard/
      components/
      hooks/
      api/
  shared/
    components/
    utils/
```

### Performance
- Use `React.lazy()` for route-based code splitting.
- Virtualize large lists with `react-window`.
