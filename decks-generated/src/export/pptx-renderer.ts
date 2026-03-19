/**
 * PPTX renderer -- converts a DeckManifest into a PowerPoint buffer.
 *
 * Pipeline: manifest -> theme/style lookup -> slide iteration -> pptxgenjs -> Buffer
 */
import PptxGenJSDefault from 'pptxgenjs';
import type PptxGenJS from 'pptxgenjs';
import type { DeckManifest } from '../schemas/manifest.js';
import type { LayoutId } from '../schemas/slide.js';
import { THEMES_BY_ID } from '../tokens/themes.js';
import { STYLE_MODES_BY_ID } from '../tokens/style-modes.js';
import { applyTheme, pptxColor } from './pptx-theme-map.js';
import { PPTX_BUILDERS } from './pptx-layout-map.js';

// Handle ESM/CJS interop: tsx may double-wrap the default export
const PptxGenJSCtor = (
  typeof PptxGenJSDefault === 'function'
    ? PptxGenJSDefault
    : (PptxGenJSDefault as unknown as { default: typeof PptxGenJSDefault }).default
) as typeof PptxGenJSDefault;

/**
 * Render a validated DeckManifest to a PPTX buffer.
 *
 * @param manifest - A validated DeckManifest (call validateManifestOrThrow first).
 * @returns A Buffer containing the .pptx file contents.
 */
export async function renderPptx(manifest: DeckManifest): Promise<Buffer> {
  const pptx: PptxGenJS = new PptxGenJSCtor();
  const theme = THEMES_BY_ID[manifest.theme];
  const style = STYLE_MODES_BY_ID[manifest.style];

  applyTheme(pptx, theme);

  for (const slideData of manifest.slides) {
    const pptxSlide = pptx.addSlide();

    // Set slide background from theme (or per-slide override)
    const bgColor = slideData.bgOverride ?? theme.bg;
    pptxSlide.background = { color: pptxColor(bgColor) };

    // Look up and run the layout builder
    const builder = PPTX_BUILDERS[slideData.layout as LayoutId];
    if (builder) {
      builder(pptxSlide, slideData, theme, style);
    }

    // Speaker notes
    if (slideData.notes) {
      pptxSlide.addNotes(slideData.notes);
    }
  }

  return pptx.write({ outputType: 'nodebuffer' }) as Promise<Buffer>;
}
