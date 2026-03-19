/**
 * StyleMode -- visual chrome variant for slide elements.
 *
 * Controls shape treatment (radius, borders, shadows) and heading style.
 * Independent of color theme: any theme x any style mode.
 *
 * pptxgenjs mapping:
 *   cardRadius      -> rectRadius on RECTANGLE shapes
 *   cardBorderWidth -> border.pt on shapes
 *   accentBarHeight -> height of decorative RECTANGLE accent bars
 *   headingWeight   -> bold: true/false (700+ = bold)
 *   headingTransform -> not directly supported; apply in text string
 */
export interface StyleMode {
  readonly id: StyleModeId;
  readonly name: string;
  readonly vibe: string;
  readonly cardRadius: number;       // px (pptxgenjs: convert to inches)
  readonly innerRadius: number;      // inner element radius
  readonly cardBorderWidth: number;  // px (pptxgenjs: convert to pt)
  readonly accentBarHeight: number;  // px
  readonly sectionGap: number;       // px between major sections
  readonly useGlow: boolean;         // web preview only (ignored in PPTX)
  readonly useSoftShadow: boolean;   // pptxgenjs: shadow property on shapes
  readonly headingWeight: number;    // 600/700/900
  readonly headingTransform: "none" | "uppercase";
  readonly labelTracking: number;    // letter-spacing for labels (px)
}

export type StyleModeId = "clean" | "bold" | "editorial";

// ---------------------------------------------------------------------------
// Style mode definitions
// ---------------------------------------------------------------------------

/** Modern Tech -- rounded corners, soft shadows, subtle glow. */
const clean: StyleMode = {
  id: "clean",
  name: "Clean",
  vibe: "Modern Tech",
  cardRadius: 16,
  innerRadius: 12,
  cardBorderWidth: 1,
  accentBarHeight: 3,
  sectionGap: 28,
  useGlow: true,
  useSoftShadow: true,
  headingWeight: 700,
  headingTransform: "none",
  labelTracking: 3,
} as const;

/** Swiss Systems -- sharp corners, thick borders, heavy type. */
const bold: StyleMode = {
  id: "bold",
  name: "Bold",
  vibe: "Swiss Systems",
  cardRadius: 0,
  innerRadius: 0,
  cardBorderWidth: 3,
  accentBarHeight: 6,
  sectionGap: 20,
  useGlow: false,
  useSoftShadow: false,
  headingWeight: 900,
  headingTransform: "uppercase",
  labelTracking: 4,
} as const;

/** Magazine Pacing -- tight radius, generous whitespace, refined type. */
const editorial: StyleMode = {
  id: "editorial",
  name: "Editorial",
  vibe: "Magazine Pacing",
  cardRadius: 4,
  innerRadius: 4,
  cardBorderWidth: 1,
  accentBarHeight: 1,
  sectionGap: 36,
  useGlow: false,
  useSoftShadow: true,
  headingWeight: 600,
  headingTransform: "none",
  labelTracking: 5,
} as const;

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

/** All 3 style modes. */
export const STYLE_MODES: readonly StyleMode[] = [
  clean,
  bold,
  editorial,
] as const;

/** Lookup a style mode by its ID. */
export const STYLE_MODES_BY_ID: Record<StyleModeId, StyleMode> = {
  clean,
  bold,
  editorial,
} as const;
