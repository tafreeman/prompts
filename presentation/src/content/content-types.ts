/**
 * Content layer type definitions.
 *
 * Each layout expects a specific text-content shape. These interfaces define
 * the **text-only** contract — no colors, no layout IDs, no ordering.
 * Structure (layout, order, colors) lives in the companion structure file.
 *
 * Usage:
 *   import type { SlideContentMap } from "./content-types";
 *   const content: SlideContentMap = { "overview": { title: "...", ... } };
 */

// ── Shared card shapes ──────────────────────────────────────────────────

export interface BasicCard {
  readonly title: string;
  readonly body: string;
}

export interface StatCard {
  readonly title: string;
  readonly body: string;
  readonly stat: string;
  readonly statLabel: string;
}

export interface DetailCard {
  readonly title: string;
  readonly step?: string;
  readonly marker?: string;
  readonly eyebrow?: string;
  readonly highlight: string;
  readonly details: readonly string[];
}

export interface BeforeAfterCard {
  readonly title: string;
  readonly challenge: string;
  readonly fix: string;
}

export interface ChecklistItem {
  readonly icon: string;
  readonly title: string;
  readonly desc: string;
}

export interface WorkflowStep {
  readonly num: string;
  readonly title: string;
  readonly type?: string;
  readonly body: string;
  readonly tip?: string;
}

export interface PillarItem {
  readonly icon: string;
  readonly title: string;
  readonly items: readonly string[];
}

export interface CatalogCategory {
  readonly title: string;
  readonly items: readonly string[];
}

export interface FocusPanel {
  readonly label: string;
  readonly title: string;
  readonly body: string;
}

export interface Capability {
  readonly title: string;
  readonly body: string;
  readonly marker: string;
}

export interface Lane {
  readonly title: string;
  readonly subtitle: string;
  readonly persona: string;
  readonly steps: readonly string[];
}

export interface ResultItem {
  readonly label: string;
  readonly value: string;
  readonly detail?: string;
}

export interface RoadmapCard extends BasicCard {
  readonly status?: string;
}

// ── Per-layout content interfaces ───────────────────────────────────────

export interface TwoColContent {
  readonly title: string;
  readonly subtitle: string;
  readonly eyebrow?: string;
  readonly summary?: string;
  readonly heroPoints?: readonly string[];
  readonly cards: readonly BasicCard[];
  readonly talkingPoints?: readonly string[];
  readonly callout?: string;
}

export interface StatCardsContent {
  readonly title: string;
  readonly subtitle: string;
  readonly thesis?: string;
  readonly heroTitle?: string;
  readonly kicker?: string;
  readonly subkicker?: string;
  readonly cards: readonly (BasicCard | StatCard | DetailCard)[];
  readonly leadershipPoints?: readonly string[];
  readonly results?: readonly ResultItem[];
  readonly enablementTitle?: string;
  readonly enablement?: string;
  readonly callout?: string;
}

export interface BeforeAfterContent {
  readonly title: string;
  readonly subtitle: string;
  readonly cards: readonly BeforeAfterCard[];
  readonly callout?: string;
}

export interface ProcessCycleContent {
  readonly title: string;
  readonly subtitle: string;
  readonly callout?: string;
}

export interface HStripContent {
  readonly title: string;
  readonly subtitle: string;
  readonly cards: readonly BasicCard[];
  readonly callout?: string;
}

export interface ProcessLanesContent {
  readonly title: string;
  readonly subtitle: string;
  readonly eyebrow?: string;
  readonly summary?: string;
  readonly heroPoints?: readonly string[];
  readonly focusPanels?: readonly FocusPanel[];
  readonly capabilities?: readonly Capability[];
  readonly lanes: readonly Lane[];
  readonly talkingPoints?: readonly string[];
  readonly callout?: string;
}

export interface InfoCardsContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline?: string;
  readonly subheadline?: string;
  readonly banner?: string;
  readonly cards: readonly StatCard[];
  readonly callout?: string;
}

export interface ChecklistContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline?: string;
  readonly approved: readonly ChecklistItem[];
  readonly forbidden: readonly ChecklistItem[];
}

export interface WorkflowContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline?: string;
  readonly subheadline?: string;
  readonly steps: readonly WorkflowStep[];
  readonly callout?: string;
}

export interface PillarsContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline?: string;
  readonly subheadline?: string;
  readonly pillars: readonly PillarItem[];
  readonly results?: readonly ResultItem[];
  readonly callout?: string;
}

export interface CatalogContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline?: string;
  readonly subheadline?: string;
  readonly categories: readonly CatalogCategory[];
  readonly callout?: string;
}

export interface EngArchitectureContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline: string;
  readonly subheadline?: string;
  readonly cards: readonly BasicCard[];
}

export interface EngCodeFlowContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline: string;
  readonly subheadline?: string;
  readonly cards: readonly BasicCard[];
}

export interface EngTechStackContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline: string;
  readonly cards: readonly BasicCard[];
  readonly results?: readonly ResultItem[];
}

export interface EngRoadmapContent {
  readonly title: string;
  readonly subtitle: string;
  readonly headline: string;
  readonly cards: readonly RoadmapCard[];
  readonly talkingPoints?: readonly string[];
}

// ── Layout-to-content discriminated map ─────────────────────────────────

export interface LayoutContentMap {
  "two-col": TwoColContent;
  "stat-cards": StatCardsContent;
  "before-after": BeforeAfterContent;
  "process-cycle": ProcessCycleContent;
  "h-strip": HStripContent;
  "process-lanes": ProcessLanesContent;
  "info-cards": InfoCardsContent;
  "checklist": ChecklistContent;
  "workflow": WorkflowContent;
  "pillars": PillarsContent;
  "catalog": CatalogContent;
  "eng-architecture": EngArchitectureContent;
  "eng-code-flow": EngCodeFlowContent;
  "eng-tech-stack": EngTechStackContent;
  "eng-roadmap": EngRoadmapContent;
}

export type LayoutId = keyof LayoutContentMap;

// ── Slide content map (keyed by slide ID) ───────────────────────────────

/** Text content for all slides in a deck, keyed by slide `id`. */
export type SlideContentMap = {
  readonly [slideId: string]: LayoutContentMap[LayoutId];
};

// ── Deck-level text content ─────────────────────────────────────────────

export interface DeckContent {
  /** Deck-level text (intro splash, tagline, brand) */
  readonly deck: {
    readonly brandLine: string;
    readonly title: string;
    readonly titleAccent: string;
    readonly tagline: string;
    readonly introBrandLine?: string;
    readonly introTitle: string;
    readonly introSubtitle: string;
    readonly introStats: readonly { readonly val: string; readonly lbl: string }[];
    readonly stats: readonly { readonly val: string; readonly lbl: string }[];
  };
  /** Per-slide text, keyed by slide `id` */
  readonly slides: SlideContentMap;
}
