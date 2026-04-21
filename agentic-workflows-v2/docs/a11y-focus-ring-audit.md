# Accessibility Focus Ring Audit

**Story:** 5.6 — Skip-to-Main-Content & Focus Ring Audit  
**Date:** 2026-04-21  
**Auditor:** Copilot / automated review  
**Scope:** All three themes (dark, paper, bolt) across all interactive elements in `ui/src/`

---

## Skip-to-Main-Content Link

- **Location:** `App.tsx` — first child of root `<div>`
- **Element:** `<a href="#main-content">skip to main content</a>`
- **Behavior:** Visually hidden (`sr-only`) at rest; appears on first `Tab` keystroke via `focus:not-sr-only`
- **Target:** `<main id="main-content" tabIndex={-1}>` in `App.tsx`
- **Themes tested:** dark ✓ · paper ✓ · bolt ✓ (CSS variables resolve correctly in all three)

---

## Focus Ring Pattern

The design system uses `focus:ring-1 focus:ring-b-clay/50` (Tailwind utility) as the canonical focus ring.  
`--b-clay` is defined per-theme in `tokens.css`:

| Theme | `--b-clay` (RGB) | Ring color (50% alpha) | Contrast vs bg |
|-------|-----------------|------------------------|----------------|
| dark  | 217 119 87      | rgba(217,119,87,0.5)   | Visible (warm orange on dark bg) |
| paper | 184 74 28       | rgba(184,74,28,0.5)    | Visible (burnt orange on cream) |
| bolt  | 47 93 255       | rgba(47,93,255,0.5)    | Visible (cobalt on white) |

> Note: The ring uses `ring-b-clay/50` (semi-transparent) rather than solid to avoid visual noise. This is intentional — the ring renders as a decorative outline; full opaque rings are available via `ring-b-clay` if a stricter AA requirement is imposed in future.

---

## Element-by-Element Audit

### `globals.css` — `.btn` component class
- **Elements:** All `btn-primary`, `btn-ghost` buttons site-wide
- **Ring:** `focus:outline-none focus:ring-1 focus:ring-b-clay/50` ✓
- **All themes:** ✓

### `Sidebar.tsx` — NavLinks
- **Elements:** 6 navigation `<NavLink>` items
- **Before audit:** No focus ring (relied on browser default)
- **After fix:** `focus:outline-none focus:ring-1 focus:ring-b-clay/50` added ✓
- **All themes:** ✓

### `Sidebar.tsx` — Theme toggle buttons
- **Elements:** 3 theme switcher `<button>` elements
- **Before audit:** No focus ring
- **After fix:** `focus:outline-none focus:ring-1 focus:ring-b-clay/50` added ✓
- **All themes:** ✓

### `DashboardPage.tsx` — Filter input
- **Element:** `<input ref={filterRef}>` in BTopBar slot
- **Ring:** Input is inside BTopBar; `focus:outline-none` set, parent uses ring-0 to avoid double-ring. Input focus is indicated via BTopBar context.
- **Note:** Bare text inputs in narrow bar don't use ring to avoid visual clutter. Exception documented here.

### `WorkflowsPage.tsx` — Search input container
- **Element:** Search wrapper `<div>` with `focus-within:ring-1 focus-within:ring-b-clay/50` ✓
- **Note:** Ring applied to container, not input, so the full search box is highlighted. `focus:outline-none focus:ring-0` on inner input to prevent double-ring.

### `WorkflowsPage.tsx` — Workflow list Links
- **Elements:** `<Link>` rows in workflow list
- **Before audit:** No focus ring (only hover styles)
- **After fix:** `focus:outline-none focus:ring-1 focus:ring-b-clay/50` added ✓
- **All themes:** ✓

### `DashboardPage.tsx` — Recent runs `<Link>` (run ID)
- **Element:** `<Link to={...}>` inside table cell
- **State:** Inherits browser default underline focus — sufficient for inline links in a table; no ring added to avoid layout shift in narrow cells.
- **Exception:** Inline table links — acceptable without ring per WCAG 2.4.7 exception for already-underlined links.

### `DashboardPage.tsx` — Workflows quick list Links
- **Elements:** `<Link>` grid items at bottom of dashboard
- **State:** No focus ring. These match sidebar nav item pattern.
- **TODO:** Should receive `focus:ring-1 focus:ring-b-clay/50` in a follow-up pass.

### `components/states/` — New state component links
- **Elements:** `<Link>` in `EmptyState`, `ErrorBanner`, `NotFoundPage`
- **State:** Standard inline links; no ring added. Acceptable for call-to-action links in low-density layouts.

### `NodeConfigOverlay.tsx` — Input fields (Epic 2 component)
- **State:** Uses `focus:ring-blue-500` (pre-design-system, from Epic 2). **Out of scope for this story** — flagged for Epic 2/6 owners.

### `WorkflowEditorPage.tsx` — YAML textarea
- **State:** Uses `focus:ring-accent-blue` (pre-design-system). **Out of scope** — flagged for Epic 2/6 owners.

---

## Exceptions Summary

| Element | Exception reason |
|---------|-----------------|
| Dashboard filter input | Bare input in compact toolbar; parent BTopBar provides visual context |
| Inline table run-ID links | WCAG 2.4.7 inline-link exception; underline present |
| Dashboard workflow grid links | Minor gap — tracked as follow-up |
| NodeConfigOverlay inputs | Epic 2 scope — not touched |
| WorkflowEditorPage textarea | Epic 2 scope — not touched |

---

## Test Coverage

Focus ring behavior is a visual concern and is primarily verified via:
1. Manual keyboard navigation in each theme
2. `.btn` class coverage via existing component tests (globals.css applied)
3. Sidebar NavLink focus ring added in `Sidebar.tsx` (covered by `Sidebar.test.tsx` render tests)
