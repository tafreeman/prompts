/**
 * Spacing tokens -- 8px base grid.
 *
 * Industry standard (Google, Microsoft, Apple). Divisible by 2 and 4
 * for half/quarter adjustments. Aligns with device pixel ratios.
 *
 * pptxgenjs mapping: convert px to inches (px / 96).
 */
export const SPACING = {
  xs:    8,    // 1 unit  -- tight icon gaps, inner padding
  sm:   16,    // 2 units -- compact card padding
  md:   24,    // 3 units -- default padding, gaps between elements
  lg:   32,    // 4 units -- card padding, inter-card gaps
  xl:   48,    // 6 units -- section margins
  '2xl': 64,  // 8 units -- major section separators
  '3xl': 80,  // 10 units -- hero-level spacing
} as const;

export type SpacingKey = keyof typeof SPACING;

/**
 * Standard slide padding (16:9 at 10" x 5.625").
 * Leaves ~8.5" x 4.625" content area.
 */
export const SLIDE_PADDING = {
  top:    0.5,    // inches
  right:  0.75,   // inches
  bottom: 0.5,    // inches
  left:   0.75,   // inches
} as const;

/**
 * Standard slide dimensions (16:9 widescreen).
 */
export const SLIDE_DIMENSIONS = {
  width:  10,      // inches
  height: 5.625,   // inches
} as const;

/** Convert px to inches for pptxgenjs positioning. */
export function pxToInches(px: number): number {
  return px / 96;
}

/** Convert px to points for pptxgenjs font sizes. */
export function pxToPoints(px: number): number {
  return px * 0.75;
}
