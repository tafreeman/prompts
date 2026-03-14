/**
 * Border tokens — radius and width constants.
 * Mirrors values from style-modes.js but as standalone constants
 * for components that need border values without the full style mode context.
 */

export const RADIUS = {
  none:  0,
  xs:    2,
  sm:    4,
  md:    8,
  lg:   12,
  xl:   16,
  pill: 999,
} as const;

export type RadiusKey = keyof typeof RADIUS;

export const BORDER_WIDTH = {
  none:   0,
  thin:   1,
  medium: 2,
  thick:  3,
} as const;

export type BorderWidthKey = keyof typeof BORDER_WIDTH;
