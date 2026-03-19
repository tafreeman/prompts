import { z } from 'zod';

// -- Assertion-Evidence Model --------------------------------------------------
// Every slide must have an "action title" that states a conclusion,
// not a descriptive label.
// Good: "Q3 Revenue Exceeded Target by 15%"
// Bad:  "Quarterly Results"
export const ActionTitleSchema = z.string()
  .min(1, "Action title required — state a conclusion, not a label (Assertion-Evidence Model)")
  .max(100, "Keep action titles concise — max 100 characters");

// -- Anti-pattern: Wall of Text ------------------------------------------------
// Design guide: slides are "glance media" (Reynolds). Max 5-7 lines.
export const BulletListSchema = z.array(z.string())
  .max(7, "Max 7 bullets per list — split into multiple slides if needed");

// -- Anti-pattern: Visual Overload ---------------------------------------------
// Max 6 cards prevents cognitive overload on a single slide.
export const maxCards = (max: number = 6) =>
  z.array(z.any()).max(max, `Max ${max} cards per slide for readability`);

// -- Process Steps (Miller's Law: 7+-2) ----------------------------------------
export const maxSteps = (max: number = 7) =>
  z.array(z.any()).max(max, `Max ${max} steps — cognitive load limit`);

// -- Data Attribution ----------------------------------------------------------
// Design guide "So What?" pattern: data slides should cite sources.
export const SourceSchema = z.string()
  .describe("Data source citation — recommended for evidence slides");

// -- Slide Count ---------------------------------------------------------------
export const SLIDE_COUNT_MAX = 50;
export const SLIDE_COUNT_MIN = 1;
