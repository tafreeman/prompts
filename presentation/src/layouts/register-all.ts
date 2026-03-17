/**
 * register-all.ts — import this once at app startup to register all layout families.
 *
 * Each sub-module calls layoutRegistry.register(...) as a side effect.
 * Import order does not matter — registry uses a Map internally.
 *
 * Registered layout IDs after import:
 *   Base:       two-col, stat-cards, stat-cards-manifest, before-after, h-strip, process-lanes
 *   Verge Pop:  stat-hero, quote-collage, badge-grid, data-table, bar-chart, color-blocks
 *   Sprint:     process-cycle
 *   Onboarding: info-cards, checklist, workflow, pillars, catalog, op-brief, op-flow
 *   Handbook:   hb-chapter, hb-practices, hb-process, hb-manifesto, hb-index
 *   Engineering: eng-architecture, eng-code-flow, eng-tech-stack, eng-roadmap
 *
 * Usage in main.jsx or App entry:
 *   import "../layouts/register-all.ts";
 */

import "./base/register.ts";
import "./verge-pop/register.ts";
import "./sprint/register.ts";
import "./onboarding/register.ts";
import "./handbook/register.ts";
import "./engineering/register.ts";
import "./advocacy/register.ts";
import "./advocacy-dense/register.ts";
