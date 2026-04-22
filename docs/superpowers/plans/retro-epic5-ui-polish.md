# Retro — Epic 5: Console UI Polish

> **Status:** COMPLETED 2026-04-22. Retrospective plan — Epic 5 shipped without a prospective plan. Written after the fact to preserve decision history.
> **Audience:** UI contributors, accessibility reviewers, future console redesign authors.
> **Last verified:** 2026-04-22

---

## Goal

Bring the React dashboard from "functional but unfinished" to "production-quality console experience." Focus on three qualities: consistent visual language (ASCII terminal-style, across three themes), keyboard-first interaction, and defensible accessibility (WCAG AA focus rings, contrast, skip links). Ship all changes behind the design system so individual components stop re-implementing visual primitives.

---

## Stories (shipped)

### 5.1 — ASCII `StatusBadge` migration
- **Commit:** `b2c218b feat(ui): ASCII StatusBadge migration (Story 5.1)`
- **Change:** All status indicators now render as bracket-text (`[OK ]`, `[RUN]`, `[ERR]`, `[WARN]`) using `--b-*` CSS tokens.
- **Outcome:** Consistent across dark / paper / bolt themes. A reader skimming the dashboard can scan status in monospace instantly.

### 5.2 — Empty / error / 404 state pages
- **Commit:** `4d9b986 feat(ui): empty/error/404 state pages (Story 5.2)`
- **Change:** `EmptyState` (`$ no <entity> yet`), `ErrorBanner` (`[!] {msg}`), `NotFoundPage` (terminal-style 404), `AppErrorBoundary` (React error boundary).
- **Outcome:** Every list view handles zero-items gracefully. Errors surface with actionable context rather than a blank pane.

### 5.3 — `BDagMini` static SVG DAG thumbnail
- **Commit:** `46ab268 feat(ui): BDagMini static SVG DAG thumbnail (Story 5.3)`
- **Change:** Pure SVG DAG thumbnail component, reuses `layoutDAG` (Kahn topological sort). Linear chains render vertically; parallel branches center-align per rank. Themed via CSS vars.
- **Outcome:** Run list rows show at-a-glance workflow shape without a heavy React Flow render.

### 5.4 — Global `useHotkeys` hook
- **Commit:** `d172a19 feat(ui): global useHotkeys hook (Story 5.4)`
- **Change:** Shared hook for `n` / `f` / `/` / `j` / `k` / `Esc` with input-focus guard and unmount cleanup.
- **Outcome:** Consistent keyboard behavior across the app. No more conflicting `keydown` listeners across components.

### 5.5 — Dashboard filter keyboard listener
- **Commit:** `37bfa54 feat(ui): dashboard filter keyboard listener (Story 5.5)`
- **Change:** `/` and `f` focus the filter input; `Esc` clears and blurs. Filter narrows runs by workflow name or run ID.
- **Outcome:** Users with many runs can find the one they want without touching the mouse.

### 5.6 — Skip-to-main link + focus ring audit
- **Commit:** `8983061 feat(ui): skip-to-main link and focus ring audit (Story 5.6)`
- **Change:** Visually hidden "skip to main" link appears on first Tab; `<main id="main-content">` as target. `focus:ring-1 focus:ring-b-clay/50` added to every interactive element.
- **Outcome:** Screen-reader and keyboard-only users can bypass navigation. Audit notes preserved at `docs/a11y-focus-ring-audit.md` (legacy location — candidate for relocation).

### 5.7 — Paper theme contrast QA
- **Commit:** `c7768b7 style(ui): paper theme sidebar contrast QA (Story 5.7)`
- **Change:** `--b-text-dim` on `--b-bg1` measured at 7.45:1 (paper passes AA). Bolt 5.92:1. Dark 3.80:1 — intentionally in the dim tier.
- **Outcome:** Contrast decisions documented per theme. Subsequent WCAG regression (commit `c70a652 fix(ui): raise dark-theme --b-text-dim to pass WCAG AA (4.5:1)`) landed as a direct consequence of this audit.

---

## Lessons

### What worked

- **Design system first, component second.** Every story touched `--b-*` tokens before shipping. The paper-theme contrast QA (5.7) would have been impossible if individual components had hardcoded grays.
- **Stories sized for one commit each.** All seven stories landed as single commits. Reviewers could keep the whole change in their head; no multi-commit PRs demanding a linear read.
- **Accessibility as a first-class gate.** Story 5.6 was not a polish task — it was table stakes for the "production-quality console" goal. Treating it that way from the start avoided the common outcome where a11y becomes a post-ship cleanup.
- **Monospace ASCII is a signature, not a gimmick.** The `[OK ]` / `[ERR]` pattern makes the product feel distinctive against every generic React dashboard. Contributors gravitate to it.

### What would have been better with a plan

- **Focus-ring audit was scope-bounded by discovery.** Story 5.6 shipped the audit, then story `c70a652` shipped the follow-up fix two days later. A prospective plan would have treated contrast QA (5.7) and the dark-theme fix as one story.
- **`a11y-focus-ring-audit.md` lives in `agentic-workflows-v2/docs/`, not in this package's docs.** The file is useful but hard to find. A convention for where audit artifacts go (proposed in the stale-docs audit as `docs/audit/`) would help.
- **Test coverage on the new hooks lagged.** `useHotkeys` shipped with implicit "tested by using it" coverage. Commit `87eddd3 test(ui): fix stale tests after design-system redesign` caught several regressions that a test-first approach would have prevented.

### Process notes for future UI polish epics

1. Write the accessibility contract first. List the WCAG criteria the epic must satisfy; stories derive from there.
2. A focus ring / contrast audit is a deliverable, not a discovery — pair it with the design system changes in the same PR.
3. Vitest coverage before merge, not after the redesign. The stale-tests commit pattern is avoidable.
4. Document the token contract. `--b-*` variables now have a load-bearing semantic meaning; that should be documented somewhere a new UI contributor will find it (candidate: `architecture-ui.md` §design-system).

---

## Links

- CHANGELOG: [`../../../CHANGELOG.md`](../../../CHANGELOG.md) — Epic 5 entries under `[0.3.0]`.
- UI architecture deep-dive: [`../../architecture-ui.md`](../../architecture-ui.md)
- Focus-ring audit: [`../../../agentic-workflows-v2/docs/a11y-focus-ring-audit.md`](../../../agentic-workflows-v2/docs/a11y-focus-ring-audit.md)
- Post-epic WCAG fix: commit `c70a652 fix(ui): raise dark-theme --b-text-dim to pass WCAG AA (4.5:1)`
