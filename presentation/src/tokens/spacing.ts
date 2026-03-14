/**
 * Spacing tokens — consistent spacing scale using 4px base unit.
 * All spacing values are multiples of 4 for crisp alignment on retina displays.
 *
 * Usage:
 *   import { SPACING, SIZE_TO_SPACING } from '../tokens/spacing';
 *   style={{ padding: SPACING.lg, gap: SPACING.md }}
 */

export const SPACING = {
  xs:   4,   // 1 unit  — tight icon gaps
  sm:   8,   // 2 units — compact inner padding
  md:  12,   // 3 units — default padding
  lg:  16,   // 4 units — card padding, section gaps
  xl:  24,   // 6 units — generous spacing
  '2xl': 32, // 8 units — section separators
  '3xl': 40, // 10 units — large breakpoints
  '4xl': 56, // 14 units — hero spacing
} as const;

export type SpacingKey = keyof typeof SPACING;

/**
 * Map component size props to spacing values.
 * Used by components that accept size="sm" | "md" | "lg".
 */
export const SIZE_TO_SPACING: Record<'sm' | 'md' | 'lg', number> = {
  sm: SPACING.md,   // 12px
  md: SPACING.lg,   // 16px
  lg: SPACING.xl,   // 24px
};

/**
 * Scale a spacing value by a multiplier.
 * @example scale('lg', 2) → 32
 */
export function scale(baseKey: SpacingKey, multiplier: number): number {
  return SPACING[baseKey] * multiplier;
}
