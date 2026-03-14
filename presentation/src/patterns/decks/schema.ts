/**
 * Zod schemas for runtime validation of deck manifests.
 * Mirrors the TypeScript types in ./types.ts but enforces at runtime.
 *
 * Usage:
 *   import { validateDeckManifest } from '../patterns/decks/schema';
 *   const deck = validateDeckManifest(rawData); // throws on invalid
 */

import { z } from 'zod';
import type { DeckManifest } from './types';

/* ── Slide schema ──────────────────────────────────────────── */

const CardSchema = z.object({
  title: z.string().optional(),
  body: z.string().optional(),
  stat: z.union([z.string(), z.number()]).optional(),
  statLabel: z.string().optional(),
  icon: z.string().optional(),
  before: z.string().optional(),
  after: z.string().optional(),
}).passthrough();

const StepSchema = z.object({
  label: z.string(),
  description: z.string().optional(),
  type: z.string().optional(),
});

const LaneSchema = z.object({
  persona: z.string(),
  steps: z.array(StepSchema),
  color: z.string().optional(),
});

const SlideSchema = z.object({
  id: z.string().min(1),
  order: z.number().int().positive(),
  layout: z.string().min(1),

  label: z.string().optional(),
  description: z.string().optional(),
  title: z.string().optional(),
  subtitle: z.string().optional(),
  body: z.string().optional(),
  callout: z.string().optional(),
  eyebrow: z.string().optional(),
  quote: z.string().optional(),
  quoteAuthor: z.string().optional(),

  cards: z.array(CardSchema).optional(),
  talkingPoints: z.array(z.string()).optional(),
  results: z.array(z.object({ label: z.string(), value: z.union([z.string(), z.number()]) })).optional(),
  steps: z.array(StepSchema).optional(),
  details: z.record(z.string(), z.any()).optional(),

  items: z.array(z.record(z.string(), z.any())).optional(),
  badges: z.array(z.object({
    icon: z.string().optional(),
    label: z.string(),
    value: z.union([z.string(), z.number()]),
  })).optional(),
  rows: z.array(z.record(z.string(), z.any())).optional(),

  lanes: z.array(LaneSchema).optional(),

  color: z.string().optional(),
  colorLight: z.string().optional(),
  colorGlow: z.string().optional(),
  bgOverride: z.string().optional(),

  heroImg: z.string().optional(),
}).passthrough(); // Allow deck-specific extra fields

/* ── SprintNode schema ─────────────────────────────────────── */

const SprintNodeSchema = z.object({
  id: z.string().min(1),
  label: z.string().min(1),
  x: z.number(),
  y: z.number(),
  color: z.string().optional(),
});

/* ── DeckManifest schema ───────────────────────────────────── */

const DeckManifestSchema = z.object({
  themeId: z.string().min(1),
  slides: z.array(SlideSchema).min(1),

  title: z.string().optional(),
  description: z.string().optional(),
  author: z.string().optional(),
  created: z.string().optional(),
  updated: z.string().optional(),
  version: z.string().optional(),

  sprintNodes: z.array(SprintNodeSchema).optional(),
  HERO_IMGS: z.record(z.string(), z.string()).optional(),
  layoutFamily: z.string().optional(),
});

/* ── Validation functions ──────────────────────────────────── */

/**
 * Validate a raw object against the DeckManifest schema.
 * Returns typed manifest on success; throws with detailed errors on failure.
 */
export function validateDeckManifest(data: unknown): DeckManifest {
  const result = DeckManifestSchema.safeParse(data);

  if (!result.success) {
    const errors = result.error.flatten();
    console.error('[DeckManifest] Validation failed:', errors);
    throw new Error(
      `Invalid deck manifest:\n${JSON.stringify(errors, null, 2)}`,
    );
  }

  return result.data as DeckManifest;
}

/**
 * Validate that all slides reference registered layouts.
 * Call after validateDeckManifest to catch layout typos.
 */
export function validateLayoutsExist(
  manifest: DeckManifest,
  registry: { has: (id: string) => boolean; list: () => string[] },
): void {
  const missing = manifest.slides.filter((s) => !registry.has(s.layout));

  if (missing.length > 0) {
    const layouts = missing.map((s) => `"${s.layout}" (slide ${s.id})`).join(', ');
    const available = registry.list().join(', ');
    throw new Error(
      `Unknown layouts in deck manifest: ${layouts}. Available: ${available}`,
    );
  }
}

export { DeckManifestSchema, SlideSchema, SprintNodeSchema };
