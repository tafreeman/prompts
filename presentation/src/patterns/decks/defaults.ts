/**
 * Sensible defaults for optional DeckManifest fields.
 * Use when constructing manifests programmatically.
 */

import type { DeckManifest, Slide } from './types';

export const DEFAULT_SLIDE: Partial<Slide> = {
  layout: 'two-col',
  talkingPoints: [],
  cards: [],
};

export const DEFAULT_MANIFEST: Partial<DeckManifest> = {
  version: '1.0.0',
  layoutFamily: 'native',
};

/**
 * Apply defaults to a partial slide, auto-generating id and order if missing.
 */
export function withSlideDefaults(partial: Partial<Slide>, index: number): Slide {
  return {
    id: partial.id ?? `slide-${index + 1}`,
    order: partial.order ?? index + 1,
    layout: partial.layout ?? 'two-col',
    ...partial,
  } as Slide;
}
