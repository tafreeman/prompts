/**
 * Unified TypeScript types for all deck manifests.
 * Single source of truth — every deck conforms to this shape.
 *
 * Based on the union of all fields across genai-advocacy, verge-pop,
 * studio, onboarding, onboarding-op, and reference decks.
 */

/** A single slide within a deck. */
export interface Slide {
  // ── Required ──
  id: string;
  order: number;
  layout: string;

  // ── Metadata ──
  label?: string;
  description?: string;

  // ── Text content ──
  title?: string;
  subtitle?: string;
  body?: string;
  callout?: string;
  eyebrow?: string;
  quote?: string;
  quoteAuthor?: string;

  // ── Structured content ──
  cards?: Array<{
    title?: string;
    body?: string;
    stat?: string | number;
    statLabel?: string;
    icon?: string;
    before?: string;
    after?: string;
    [key: string]: any;
  }>;

  talkingPoints?: string[];
  results?: Array<{ label: string; value: string | number }>;
  steps?: Array<{ label: string; description?: string; type?: string }>;
  details?: Record<string, any>;

  // ── Lists / grids ──
  items?: Array<Record<string, any>>;
  badges?: Array<{ icon?: string; label: string; value: string | number }>;
  rows?: Array<Record<string, any>>;

  // ── Persona / process ──
  lanes?: Array<{
    persona: string;
    steps: Array<{ label: string; description?: string; type?: string }>;
    color?: string;
  }>;

  // ── Styling overrides ──
  color?: string;
  colorLight?: string;
  colorGlow?: string;
  bgOverride?: string;

  // ── Hero images ──
  heroImg?: string;
}

/** A node in the sprint cycle SVG diagram. */
export interface SprintNode {
  id: string;
  label: string;
  x: number;
  y: number;
  color?: string;
}

/** Top-level deck manifest — validated at runtime by Zod. */
export interface DeckManifest {
  // ── Required ──
  themeId: string;
  slides: Slide[];

  // ── Optional metadata ──
  title?: string;
  description?: string;
  author?: string;
  created?: string;
  updated?: string;
  version?: string;

  // ── Optional deck-level data ──
  sprintNodes?: SprintNode[];
  HERO_IMGS?: Record<string, string>;

  // ── Layout family hint ──
  layoutFamily?: string;
}

/** Known deck identifiers. */
export type DeckId =
  | 'genai-advocacy'
  | 'onboarding'
  | 'studio'
  | 'verge-pop'
  | 'onboarding-op'
  | 'engineering';
