/**
 * Named type scale -- enforces consistent typography across layouts.
 *
 * Design guide rule: max 2-3 typefaces per deck, hierarchy via size contrast.
 * pptxgenjs mapping: fontSize (pt), bold (fontWeight >= 700).
 *
 * Note: pptxgenjs uses points, not pixels. 1pt = 1.333px.
 * The values below are stored in px for web preview; builders convert to pt.
 */
export interface TypeScaleEntry {
  readonly fontSize: number;       // px (builders convert: px * 0.75 = pt)
  readonly fontWeight: number;
  readonly letterSpacing: number;  // px
  readonly lineHeight: number;     // unitless multiplier
  readonly textTransform?: "uppercase" | "none";
}

export type TypeScaleKey =
  | "STAT"     // 48px -- oversized metric numbers
  | "HERO"     // 44px -- deck title, cover slides
  | "TITLE"    // 32px -- slide action titles
  | "SECTION"  // 24px -- section headers, card titles
  | "CARD"     // 18px -- card headings, emphasized body
  | "BODY"     // 16px -- body text, bullets
  | "CAPTION"  // 13px -- source lines, footnotes
  | "EYEBROW"; // 11px -- uppercase labels, category tags

// ---------------------------------------------------------------------------
// Scale values
// ---------------------------------------------------------------------------

/**
 * Named type scale with 8 entries from STAT (48px) to EYEBROW (11px).
 *
 * pptxgenjs conversion: multiply fontSize by 0.75 to get points.
 *   STAT   48px -> 36pt
 *   HERO   44px -> 33pt
 *   TITLE  32px -> 24pt
 *   SECTION 24px -> 18pt
 *   CARD   18px -> 13.5pt
 *   BODY   16px -> 12pt
 *   CAPTION 13px -> 10pt (approx)
 *   EYEBROW 11px -> 8pt (approx)
 */
export const TYPE_SCALE: Record<TypeScaleKey, TypeScaleEntry> = {
  STAT: {
    fontSize: 48,
    fontWeight: 800,
    letterSpacing: -1.5,
    lineHeight: 1.0,
  },
  HERO: {
    fontSize: 44,
    fontWeight: 800,
    letterSpacing: -1.0,
    lineHeight: 0.96,
  },
  TITLE: {
    fontSize: 32,
    fontWeight: 700,
    letterSpacing: -0.5,
    lineHeight: 1.05,
  },
  SECTION: {
    fontSize: 24,
    fontWeight: 700,
    letterSpacing: 0,
    lineHeight: 1.12,
  },
  CARD: {
    fontSize: 18,
    fontWeight: 600,
    letterSpacing: 0,
    lineHeight: 1.2,
  },
  BODY: {
    fontSize: 16,
    fontWeight: 400,
    letterSpacing: 0,
    lineHeight: 1.6,
  },
  CAPTION: {
    fontSize: 13,
    fontWeight: 500,
    letterSpacing: 0.5,
    lineHeight: 1.4,
  },
  EYEBROW: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: 2.5,
    lineHeight: 1.0,
    textTransform: "uppercase",
  },
} as const;
