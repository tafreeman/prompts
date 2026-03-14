/**
 * Enhanced palette utilities — computed glow, WCAG contrast, font fallbacks.
 * Additive enhancement to palette.js — does NOT replace existing exports.
 *
 * Usage:
 *   import { computeThemeTokens, checkContrast } from '../tokens/palette-enhanced';
 */

/* ── Hex ↔ RGB conversion ──────────────────────────────────── */

export interface RGB {
  r: number;
  g: number;
  b: number;
}

export function hexToRgb(hex: string): RGB {
  const clean = hex.replace('#', '');
  return {
    r: parseInt(clean.slice(0, 2), 16),
    g: parseInt(clean.slice(2, 4), 16),
    b: parseInt(clean.slice(4, 6), 16),
  };
}

/* ── Computed glow ──────────────────────────────────────────── */

/**
 * Derive glow color from accent hex at a given opacity.
 * Replaces manually-defined accentGlow values in themes.
 */
export function computeAccentGlow(accentHex: string, opacity: number = 0.25): string {
  const { r, g, b } = hexToRgb(accentHex);
  return `rgba(${r},${g},${b},${opacity})`;
}

/* ── WCAG 2.1 contrast checking ────────────────────────────── */

/**
 * Calculate relative luminance per WCAG 2.1.
 * @see https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
 */
export function getRelativeLuminance(hex: string): number {
  const { r, g, b } = hexToRgb(hex);
  const [rs, gs, bs] = [r, g, b].map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

export interface ContrastResult {
  ratio: number;
  passes: boolean;
  level: 'AAA' | 'AA' | 'fail';
}

/**
 * Check WCAG 2.1 contrast ratio between foreground and background.
 * AA requires 4.5:1 for normal text, AAA requires 7:1.
 */
export function checkContrast(foreground: string, background: string): ContrastResult {
  const fgLum = getRelativeLuminance(foreground);
  const bgLum = getRelativeLuminance(background);
  const ratio = parseFloat(
    ((Math.max(fgLum, bgLum) + 0.05) / (Math.min(fgLum, bgLum) + 0.05)).toFixed(2),
  );
  return {
    ratio,
    passes: ratio >= 4.5,
    level: ratio >= 7 ? 'AAA' : ratio >= 4.5 ? 'AA' : 'fail',
  };
}

/* ── Font fallback chains ──────────────────────────────────── */

/**
 * Build a robust CSS font-family string with system fallbacks.
 * Ensures graceful degradation if Google Fonts fail to load.
 */
export function buildFontChain(primaryFont: string): string {
  // Strip existing quotes if present
  const clean = primaryFont.replace(/^['"]|['"]$/g, '');
  const isMonospace = clean.toLowerCase().includes('mono');

  const fallbacks = isMonospace
    ? ["'Courier New'", 'Courier', 'monospace']
    : [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
      ];

  return [`'${clean}'`, ...fallbacks].join(', ');
}

/* ── Computed theme tokens ─────────────────────────────────── */

export interface ContrastResults {
  text_bg: ContrastResult;
  textMuted_bg: ContrastResult;
  accent_bg: ContrastResult;
  accent_bgCard: ContrastResult;
}

export interface ComputedThemeExtras {
  accentGlowComputed: string;
  accentGlowStrong: string;
  fontDisplayChain: string;
  fontBodyChain: string;
  contrastResults: ContrastResults;
}

/**
 * Precompute all derived token values for a theme.
 * Called once at theme initialisation; results are cached.
 */
export function computeThemeTokens<T extends {
  accent: string;
  text: string;
  textMuted: string;
  bg: string;
  bgCard: string;
  fontDisplay: string;
  fontBody: string;
}>(theme: T): T & ComputedThemeExtras {
  return {
    ...theme,
    accentGlowComputed: computeAccentGlow(theme.accent, 0.25),
    accentGlowStrong: computeAccentGlow(theme.accent, 0.45),
    fontDisplayChain: buildFontChain(theme.fontDisplay),
    fontBodyChain: buildFontChain(theme.fontBody),
    contrastResults: {
      text_bg: checkContrast(theme.text, theme.bg),
      textMuted_bg: checkContrast(theme.textMuted, theme.bg),
      accent_bg: checkContrast(theme.accent, theme.bg),
      accent_bgCard: checkContrast(theme.accent, theme.bgCard),
    },
  };
}

/* ── Accessibility validation ──────────────────────────────── */

export interface ValidationResult {
  valid: boolean;
  warnings: string[];
  errors: string[];
}

/**
 * Validate that a theme meets accessibility standards.
 * Warns on AA failures, errors on critical contrast issues.
 */
export function validateThemeAccessibility(
  theme: { name: string } & { contrastResults: ContrastResults },
): ValidationResult {
  const warnings: string[] = [];
  const errors: string[] = [];

  if (!theme.contrastResults.text_bg.passes) {
    warnings.push(`Theme "${theme.name}": text/bg contrast fails AA (${theme.contrastResults.text_bg.ratio}:1)`);
  }
  if (!theme.contrastResults.textMuted_bg.passes) {
    warnings.push(`Theme "${theme.name}": textMuted/bg contrast fails AA (${theme.contrastResults.textMuted_bg.ratio}:1)`);
  }
  if (theme.contrastResults.text_bg.level === 'fail' && theme.contrastResults.text_bg.ratio < 3) {
    errors.push(`Theme "${theme.name}": text/bg contrast critically low (${theme.contrastResults.text_bg.ratio}:1)`);
  }

  return { valid: errors.length === 0, warnings, errors };
}
