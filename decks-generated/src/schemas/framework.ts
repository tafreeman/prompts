import { z } from 'zod';

export const FrameworkSlotSchema = z.object({
  /** Which slide position this slot fills. */
  position: z.number().int().min(1),
  /** Required layout for this slot. */
  layout: z.string(),
  /** Suggested title pattern (AI replaces placeholders). */
  titleHint: z.string(),
  /** Content guidance for AI. */
  contentHint: z.string(),
  /** Whether this slot is required or optional. */
  required: z.boolean().default(true),
});

export const FrameworkSchema = z.object({
  id: z.string().min(1),
  name: z.string(),
  description: z.string(),
  /** Target audience for this framework. */
  audience: z.string(),
  /** Recommended slide count range. */
  slideRange: z.object({
    min: z.number().int().min(1),
    max: z.number().int().max(50),
  }),
  /** Default theme for decks using this framework. */
  defaultTheme: z.string(),
  /** Default style mode. */
  defaultStyle: z.string(),
  /** Ordered slot definitions. */
  slots: z.array(FrameworkSlotSchema).min(1),
});

export type Framework = z.infer<typeof FrameworkSchema>;
export type FrameworkSlot = z.infer<typeof FrameworkSlotSchema>;
