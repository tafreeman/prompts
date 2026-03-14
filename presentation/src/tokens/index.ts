/**
 * Token barrel export — single import point for all design tokens.
 *
 * Usage:
 *   import { SPACING, TIMING, EASING, SHADOWS, RADIUS } from '../tokens';
 */

// New TypeScript token modules
export { SPACING, SIZE_TO_SPACING, scale } from './spacing';
export type { SpacingKey } from './spacing';

export { TIMING, EASING, getPhaseDurations } from './timing';
export type { EasingKey } from './timing';

export { SHADOWS } from './shadows';
export type { ShadowKey } from './shadows';

export { RADIUS, BORDER_WIDTH } from './borders';
export type { RadiusKey, BorderWidthKey } from './borders';

export {
  computeAccentGlow,
  hexToRgb,
  getRelativeLuminance,
  checkContrast,
  buildFontChain,
  computeThemeTokens,
  validateThemeAccessibility,
} from './palette-enhanced';
export type { RGB, ContrastResult, ComputedThemeExtras, ValidationResult } from './palette-enhanced';

// Re-export existing JS token modules
export { TYPE_SCALE } from './type-scale';
export { STYLE_MODES, STYLE_MODES_BY_ID } from './style-modes';
export { THEMES, THEMES_BY_ID, THEME_FONT_URLS } from './themes';
export { lightenHex, hexToGlow, buildPalette, resolveSlideColor, resolveTopicColors, resolveIntroStatColors } from './palette';
export { UI } from './ui-strings';
