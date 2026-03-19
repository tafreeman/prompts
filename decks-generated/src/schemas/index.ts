export { SlideSchema, LAYOUT_IDS } from './slide.js';
export type { Slide, LayoutId } from './slide.js';
export {
  CoverSlide, SectionSlide, TextSlide, CardsSlide,
  NumberSlide, CompareSlide, StepsSlide, TableSlide,
  ScorecardSlide, TimelineSlide, GridSlide, ClosingSlide,
} from './slide.js';

export {
  DeckManifestSchema, ThemeIdSchema, StyleModeIdSchema,
  validateManifest, validateManifestOrThrow,
} from './manifest.js';
export type { DeckManifest, ValidationResult } from './manifest.js';

export {
  ActionTitleSchema, BulletListSchema, SourceSchema,
  SLIDE_COUNT_MIN, SLIDE_COUNT_MAX,
} from './guards.js';

export { FrameworkSchema, FrameworkSlotSchema } from './framework.js';
export type { Framework, FrameworkSlot } from './framework.js';
