/**
 * Maps Theme tokens to pptxgenjs configuration.
 *
 * Applies slide layout (16:9), default fonts, and theme colors.
 * pptxgenjs requires hex colors WITHOUT the '#' prefix.
 */
import PptxGenJS from 'pptxgenjs';
import type { Theme } from '../tokens/themes.js';

/**
 * Configure the pptxgenjs instance with theme-derived defaults.
 * - Sets 16:9 widescreen layout (10" x 5.625")
 * - Applies heading and body font families
 */
export function applyTheme(pptx: PptxGenJS, theme: Theme): void {
  pptx.defineLayout({ name: 'WIDE_16x9', width: 10, height: 5.625 });
  pptx.layout = 'WIDE_16x9';
  pptx.theme = {
    headFontFace: theme.fontDisplay,
    bodyFontFace: theme.fontBody,
  };
}

/** Strip '#' prefix from hex color for pptxgenjs. */
export function pptxColor(hex: string): string {
  return hex.replace('#', '');
}
