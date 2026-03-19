import { z } from 'zod';
import { SlideSchema } from './slide.js';
import { SLIDE_COUNT_MIN, SLIDE_COUNT_MAX } from './guards.js';

// -- Theme + Style IDs validated against known values --------------------------

export const ThemeIdSchema = z.enum([
  "midnight-teal", "neon-noir", "linear",
  "paper-ink", "signal-cobalt", "studio-craft",
]);

export const StyleModeIdSchema = z.enum(["clean", "bold", "editorial"]);

// -- Root Manifest -------------------------------------------------------------

export const DeckManifestSchema = z.object({
  // Metadata
  title: z.string().min(1).max(120),
  subtitle: z.string().max(200).optional(),
  author: z.string().optional(),
  date: z.string().optional(),
  version: z.string().default("1.0.0"),

  // Design
  theme: ThemeIdSchema.default("midnight-teal"),
  style: StyleModeIdSchema.default("clean"),

  // Framework template this deck was started from (informational)
  framework: z.string().optional(),

  // Slides
  slides: z.array(SlideSchema)
    .min(SLIDE_COUNT_MIN, "Deck must have at least 1 slide")
    .max(SLIDE_COUNT_MAX, `Max ${SLIDE_COUNT_MAX} slides per deck`),
})
.superRefine((data, ctx) => {
  // -- Custom guardrail: check for duplicate slide IDs --
  const ids = data.slides.map((s) => s.id);
  const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dupes.length > 0) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: `Duplicate slide IDs: ${[...new Set(dupes)].join(", ")}`,
      path: ["slides"],
    });
  }
});

export type DeckManifest = z.infer<typeof DeckManifestSchema>;

// -- Validation Functions ------------------------------------------------------

export interface ValidationResult {
  success: boolean;
  data?: DeckManifest;
  errors?: string[];
}

/**
 * Validate a parsed YAML object against the DeckManifest schema.
 * Returns a result object with either typed data or human-readable errors.
 */
export function validateManifest(raw: unknown): ValidationResult {
  const result = DeckManifestSchema.safeParse(raw);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map((issue) => {
    const path = issue.path.length > 0 ? issue.path.join(".") : "(root)";
    return `  ${path}: ${issue.message}`;
  });

  return { success: false, errors };
}

/**
 * Validate and throw on failure — for use in build pipelines.
 */
export function validateManifestOrThrow(raw: unknown): DeckManifest {
  const result = validateManifest(raw);
  if (!result.success) {
    throw new Error(
      `Invalid deck manifest:\n${result.errors!.join("\n")}`
    );
  }
  return result.data!;
}
