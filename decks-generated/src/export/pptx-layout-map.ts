/**
 * PPTX layout builders -- one function per layout ID.
 *
 * Each builder receives a pptxgenjs Slide, typed slide data, theme, and style mode.
 * Coordinates are in INCHES. Font sizes are in POINTS (from TYPE_SCALE via pxToPoints).
 *
 * pptxgenjs API reference:
 *   slide.addText(text | TextProps[], options)
 *   slide.addShape(shapeName, options)
 *   slide.addTable(rows, options)
 */
import PptxGenJS from 'pptxgenjs';
import type { Slide } from '../schemas/slide.js';
import type { LayoutId } from '../schemas/slide.js';
import type { Theme } from '../tokens/themes.js';
import type { StyleMode } from '../tokens/style-modes.js';
import { TYPE_SCALE } from '../tokens/type-scale.js';
import { SLIDE_PADDING } from '../tokens/spacing.js';
import { pxToPoints, pxToInches } from '../tokens/spacing.js';
import { pptxColor } from './pptx-theme-map.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type SlideBuilder = (
  pptxSlide: PptxGenJS.Slide,
  data: Slide,
  theme: Theme,
  style: StyleMode,
) => void;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const PAD = SLIDE_PADDING;
const CONTENT_W = 10 - PAD.left - PAD.right;       // ~8.5"
const CONTENT_H = 5.625 - PAD.top - PAD.bottom;    // ~4.625"

function ptSize(key: keyof typeof TYPE_SCALE): number {
  return pxToPoints(TYPE_SCALE[key].fontSize);
}

function isBold(key: keyof typeof TYPE_SCALE): boolean {
  return TYPE_SCALE[key].fontWeight >= 700;
}

/** Apply heading transform from style mode. */
function transformText(text: string, style: StyleMode): string {
  return style.headingTransform === 'uppercase' ? text.toUpperCase() : text;
}

/** Add an accent bar shape. */
function addAccentBar(
  slide: PptxGenJS.Slide,
  x: number,
  y: number,
  w: number,
  theme: Theme,
  style: StyleMode,
): void {
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x,
    y,
    w,
    h: pxToInches(style.accentBarHeight),
    fill: { color: pptxColor(theme.accent) },
    line: { width: 0 },
  });
}

/** Add a source/citation line at the bottom. */
function addSource(
  slide: PptxGenJS.Slide,
  source: string,
  theme: Theme,
): void {
  slide.addText(source, {
    x: PAD.left,
    y: 5.625 - PAD.bottom - 0.3,
    w: CONTENT_W,
    h: 0.3,
    fontSize: ptSize('CAPTION'),
    fontFace: theme.fontBody,
    color: pptxColor(theme.textDim),
    italic: true,
  });
}

/** Add a callout bar at the bottom of content area. */
function addCallout(
  slide: PptxGenJS.Slide,
  text: string,
  y: number,
  theme: Theme,
  style: StyleMode,
): void {
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: PAD.left,
    y,
    w: CONTENT_W,
    h: 0.45,
    fill: { color: pptxColor(theme.surface) },
    rectRadius: pxToInches(style.cardRadius),
    line: { width: 0 },
  });
  slide.addText(text, {
    x: PAD.left + 0.15,
    y,
    w: CONTENT_W - 0.3,
    h: 0.45,
    fontSize: ptSize('CAPTION'),
    fontFace: theme.fontBody,
    color: pptxColor(theme.accent),
    bold: true,
    valign: 'middle',
  });
}

// ---------------------------------------------------------------------------
// Builders
// ---------------------------------------------------------------------------

const buildCover: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'cover') return;

  // Eyebrow
  if (data.eyebrow) {
    slide.addText(transformText(data.eyebrow, style), {
      x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.35,
      fontSize: ptSize('EYEBROW'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
    });
  }

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: 1.0, w: CONTENT_W, h: 1.2,
    fontSize: ptSize('HERO'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('HERO'),
    valign: 'middle',
  });

  // Subtitle
  if (data.subtitle) {
    slide.addText(data.subtitle, {
      x: PAD.left, y: 2.3, w: CONTENT_W, h: 0.5,
      fontSize: ptSize('SECTION'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
    });
  }

  // Tagline
  if (data.tagline) {
    slide.addText(data.tagline, {
      x: PAD.left, y: 2.9, w: CONTENT_W, h: 0.4,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
      italic: true,
    });
  }

  // KPIs row
  if (data.kpis && data.kpis.length > 0) {
    const kpiY = 3.8;
    const kpiW = CONTENT_W / data.kpis.length;
    data.kpis.forEach((kpi, i) => {
      const x = PAD.left + i * kpiW;
      slide.addText(String(kpi.value), {
        x, y: kpiY, w: kpiW, h: 0.6,
        fontSize: ptSize('STAT'),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.accent),
        bold: true,
        align: 'center',
      });
      slide.addText(kpi.label, {
        x, y: kpiY + 0.6, w: kpiW, h: 0.3,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        align: 'center',
      });
    });
  }
};

const buildSection: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'section') return;

  // Section number
  if (data.sectionNumber !== undefined) {
    slide.addText(String(data.sectionNumber).padStart(2, '0'), {
      x: PAD.left, y: 1.0, w: 1.5, h: 1.0,
      fontSize: ptSize('STAT'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.accent),
      bold: true,
    });
  }

  // Accent bar
  addAccentBar(slide, PAD.left, 2.2, 1.5, theme, style);

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: 2.4, w: CONTENT_W, h: 1.2,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
    valign: 'middle',
  });

  // Subtitle
  if (data.subtitle) {
    slide.addText(data.subtitle, {
      x: PAD.left, y: 3.7, w: CONTENT_W, h: 0.5,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
    });
  }
};

const buildText: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'text') return;

  // Eyebrow
  if (data.eyebrow) {
    slide.addText(transformText(data.eyebrow, style), {
      x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.3,
      fontSize: ptSize('EYEBROW'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
    });
  }

  // Title
  const titleY = data.eyebrow ? PAD.top + 0.35 : PAD.top;
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: titleY, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, titleY + 0.65, 1.0, theme, style);

  let bodyY = titleY + 0.8;

  // Body text
  if (data.body) {
    slide.addText(data.body, {
      x: PAD.left, y: bodyY, w: CONTENT_W, h: 1.0,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
      valign: 'top',
      lineSpacingMultiple: 1.5,
    });
    bodyY += 1.1;
  }

  // Bullets
  if (data.bullets && data.bullets.length > 0) {
    const bulletItems: PptxGenJS.TextProps[] = data.bullets.map((b) => ({
      text: b,
      options: {
        bullet: true,
        fontSize: ptSize('BODY'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
      },
    }));
    slide.addText(bulletItems, {
      x: PAD.left, y: bodyY, w: CONTENT_W, h: CONTENT_H - (bodyY - PAD.top) - 0.5,
      valign: 'top',
      lineSpacingMultiple: 1.6,
    });
  }

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildCards: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'cards') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const cardCount = data.cards.length;
  const gap = 0.2;
  const cardW = (CONTENT_W - gap * (cardCount - 1)) / cardCount;
  const cardY = 1.4;
  const cardH = 2.8;

  data.cards.forEach((card, i) => {
    const x = PAD.left + i * (cardW + gap);

    // Card background
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x, y: cardY, w: cardW, h: cardH,
      fill: { color: pptxColor(theme.surface) },
      rectRadius: pxToInches(style.cardRadius),
      line: style.cardBorderWidth > 0
        ? { color: pptxColor(theme.surfaceDeep), width: style.cardBorderWidth * 0.75 }
        : { width: 0 },
    });

    let innerY = cardY + 0.2;

    // Stat
    if (card.stat !== undefined) {
      slide.addText(String(card.stat), {
        x: x + 0.15, y: innerY, w: cardW - 0.3, h: 0.6,
        fontSize: ptSize('STAT'),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.accent),
        bold: true,
      });
      innerY += 0.6;
    }

    // Label
    if (card.label) {
      slide.addText(card.label, {
        x: x + 0.15, y: innerY, w: cardW - 0.3, h: 0.3,
        fontSize: ptSize('EYEBROW'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
      });
      innerY += 0.35;
    }

    // Card title
    slide.addText(card.title, {
      x: x + 0.15, y: innerY, w: cardW - 0.3, h: 0.35,
      fontSize: ptSize('CARD'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
    });
    innerY += 0.4;

    // Card body
    if (card.body) {
      slide.addText(card.body, {
        x: x + 0.15, y: innerY, w: cardW - 0.3, h: cardH - (innerY - cardY) - 0.15,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        valign: 'top',
        lineSpacingMultiple: 1.4,
      });
    }
  });

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.5, theme, style);

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildNumber: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'number') return;

  // Eyebrow
  if (data.eyebrow) {
    slide.addText(transformText(data.eyebrow, style), {
      x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.3,
      fontSize: ptSize('EYEBROW'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
    });
  }

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top + 0.35, w: CONTENT_W, h: 0.55,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.95, 1.0, theme, style);

  // Big stat
  slide.addText(String(data.stat), {
    x: PAD.left, y: 1.8, w: CONTENT_W, h: 1.4,
    fontSize: ptSize('STAT') * 1.5,
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.accent),
    bold: true,
    align: 'center',
    valign: 'middle',
  });

  // Stat label
  slide.addText(data.statLabel, {
    x: PAD.left, y: 3.2, w: CONTENT_W, h: 0.4,
    fontSize: ptSize('SECTION'),
    fontFace: theme.fontBody,
    color: pptxColor(theme.textMuted),
    align: 'center',
  });

  // Context
  if (data.context) {
    slide.addText(data.context, {
      x: PAD.left + 1.0, y: 3.8, w: CONTENT_W - 2.0, h: 0.8,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
      align: 'center',
      lineSpacingMultiple: 1.4,
    });
  }

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildCompare: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'compare') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const colW = (CONTENT_W - 0.3) / 2;
  const colY = 1.3;
  const colH = 3.0;

  // Build a column
  const buildCol = (col: typeof data.left, x: number) => {
    // Column background
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x, y: colY, w: colW, h: colH,
      fill: { color: pptxColor(theme.surface) },
      rectRadius: pxToInches(style.cardRadius),
      line: { width: 0 },
    });

    let innerY = colY + 0.15;

    // Column title
    if (col.title) {
      slide.addText(col.title, {
        x: x + 0.2, y: innerY, w: colW - 0.4, h: 0.4,
        fontSize: ptSize('CARD'),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.text),
        bold: true,
      });
      innerY += 0.45;
    }

    // Column body
    if (col.body) {
      slide.addText(col.body, {
        x: x + 0.2, y: innerY, w: colW - 0.4, h: 0.8,
        fontSize: ptSize('BODY'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        valign: 'top',
      });
      innerY += 0.85;
    }

    // Column bullets
    if (col.bullets && col.bullets.length > 0) {
      const items: PptxGenJS.TextProps[] = col.bullets.map((b) => ({
        text: b,
        options: {
          bullet: true,
          fontSize: ptSize('BODY'),
          fontFace: theme.fontBody,
          color: pptxColor(theme.textMuted),
        },
      }));
      slide.addText(items, {
        x: x + 0.2, y: innerY, w: colW - 0.4, h: colH - (innerY - colY) - 0.15,
        valign: 'top',
        lineSpacingMultiple: 1.5,
      });
    }
  };

  buildCol(data.left, PAD.left);
  buildCol(data.right, PAD.left + colW + 0.3);

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.5, theme, style);

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildSteps: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'steps') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const stepCount = data.steps.length;
  const stepW = (CONTENT_W - 0.15 * (stepCount - 1)) / stepCount;
  const stepY = 1.5;

  data.steps.forEach((step, i) => {
    const x = PAD.left + i * (stepW + 0.15);

    // Step number circle
    slide.addShape('ellipse' as PptxGenJS.ShapeType, {
      x: x + stepW / 2 - 0.2, y: stepY, w: 0.4, h: 0.4,
      fill: { color: pptxColor(theme.accent) },
      line: { width: 0 },
    });
    slide.addText(String(i + 1), {
      x: x + stepW / 2 - 0.2, y: stepY, w: 0.4, h: 0.4,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.bg),
      bold: true,
      align: 'center',
      valign: 'middle',
    });

    // Connector line between circles
    if (i < stepCount - 1) {
      const lineX = x + stepW / 2 + 0.2;
      const lineW = stepW + 0.15 - 0.4;
      slide.addShape('rect' as PptxGenJS.ShapeType, {
        x: lineX, y: stepY + 0.18, w: lineW, h: 0.04,
        fill: { color: pptxColor(theme.surfaceDeep) },
        line: { width: 0 },
      });
    }

    // Step label
    slide.addText(step.label, {
      x, y: stepY + 0.55, w: stepW, h: 0.35,
      fontSize: ptSize('CARD'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'center',
    });

    // Step description
    if (step.description) {
      slide.addText(step.description, {
        x, y: stepY + 0.95, w: stepW, h: 1.2,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        align: 'center',
        valign: 'top',
        lineSpacingMultiple: 1.3,
      });
    }
  });

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.5, theme, style);
};

const buildTable: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'table') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  // Build table data
  const colCount = data.columns.length;
  const colW = CONTENT_W / colCount;

  // Header row
  const headerRow: PptxGenJS.TableCell[] = data.columns.map((col) => ({
    text: col,
    options: {
      fontSize: ptSize('CAPTION'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      fill: { color: pptxColor(theme.surfaceDeep) },
      border: [
        { pt: 0, color: pptxColor(theme.surfaceDeep) },
        { pt: 0, color: pptxColor(theme.surfaceDeep) },
        { pt: 1, color: pptxColor(theme.accent) },
        { pt: 0, color: pptxColor(theme.surfaceDeep) },
      ],
      valign: 'middle' as const,
      align: 'left' as const,
    },
  }));

  // Data rows
  const dataRows: PptxGenJS.TableCell[][] = data.rows.map((row) =>
    data.columns.map((col) => {
      const val = row[col];
      const isHighlight = data.highlight && col === data.highlight;
      return {
        text: val !== undefined ? String(val) : '',
        options: {
          fontSize: ptSize('BODY'),
          fontFace: theme.fontBody,
          color: isHighlight ? pptxColor(theme.accent) : pptxColor(theme.textMuted),
          bold: isHighlight ? true : false,
          fill: { color: pptxColor(theme.bg) },
          border: [
            { pt: 0, color: pptxColor(theme.surfaceDeep) },
            { pt: 0, color: pptxColor(theme.surfaceDeep) },
            { pt: 0.5, color: pptxColor(theme.surfaceDeep) },
            { pt: 0, color: pptxColor(theme.surfaceDeep) },
          ],
          valign: 'middle' as const,
          align: 'left' as const,
        },
      };
    }),
  );

  const tableRows = [headerRow, ...dataRows];

  slide.addTable(tableRows, {
    x: PAD.left,
    y: 1.2,
    w: CONTENT_W,
    colW: Array(colCount).fill(colW) as number[],
    rowH: 0.45,
    margin: [0.05, 0.1, 0.05, 0.1],
  });

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildScorecard: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'scorecard') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const kpiCount = data.kpis.length;
  const cols = kpiCount <= 4 ? kpiCount : Math.ceil(kpiCount / 2);
  const rows = kpiCount <= 4 ? 1 : 2;
  const gap = 0.2;
  const kpiW = (CONTENT_W - gap * (cols - 1)) / cols;
  const kpiH = rows === 1 ? 2.8 : 1.3;

  data.kpis.forEach((kpi, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = PAD.left + col * (kpiW + gap);
    const y = 1.3 + row * (kpiH + gap);

    // Card background
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x, y, w: kpiW, h: kpiH,
      fill: { color: pptxColor(theme.surface) },
      rectRadius: pxToInches(style.cardRadius),
      line: { width: 0 },
    });

    // Value
    slide.addText(String(kpi.value), {
      x: x + 0.15, y: y + 0.1, w: kpiW - 0.3, h: 0.5,
      fontSize: ptSize('STAT'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.accent),
      bold: true,
    });

    // Trend arrow
    const trendChar = kpi.trend === 'up' ? '\u2191' : kpi.trend === 'down' ? '\u2193' : '';
    const trendColor = kpi.trend === 'up' ? theme.success : kpi.trend === 'down' ? theme.danger : theme.textMuted;

    // Label + trend
    slide.addText(`${kpi.label} ${trendChar}`, {
      x: x + 0.15, y: y + 0.6, w: kpiW - 0.3, h: 0.3,
      fontSize: ptSize('CAPTION'),
      fontFace: theme.fontBody,
      color: pptxColor(trendColor),
      bold: true,
    });

    // Detail
    if (kpi.detail) {
      slide.addText(kpi.detail, {
        x: x + 0.15, y: y + 0.9, w: kpiW - 0.3, h: 0.3,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textDim),
      });
    }
  });

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.5, theme, style);

  // Source
  if (data.source) addSource(slide, data.source, theme);
};

const buildTimeline: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'timeline') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const eventCount = data.events.length;
  const eventW = CONTENT_W / eventCount;
  const lineY = 2.0;

  // Horizontal timeline line
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: PAD.left, y: lineY, w: CONTENT_W, h: 0.04,
    fill: { color: pptxColor(theme.surfaceDeep) },
    line: { width: 0 },
  });

  data.events.forEach((event, i) => {
    const x = PAD.left + i * eventW;
    const dotX = x + eventW / 2;

    // Timeline dot
    slide.addShape('ellipse' as PptxGenJS.ShapeType, {
      x: dotX - 0.12, y: lineY - 0.1, w: 0.24, h: 0.24,
      fill: { color: pptxColor(theme.accent) },
      line: { width: 0 },
    });

    // Date
    slide.addText(event.date, {
      x, y: lineY - 0.55, w: eventW, h: 0.35,
      fontSize: ptSize('EYEBROW'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
      align: 'center',
    });

    // Event title
    slide.addText(event.title, {
      x, y: lineY + 0.35, w: eventW, h: 0.35,
      fontSize: ptSize('CARD'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'center',
    });

    // Event description
    if (event.description) {
      slide.addText(event.description, {
        x, y: lineY + 0.75, w: eventW, h: 0.8,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        align: 'center',
        valign: 'top',
        lineSpacingMultiple: 1.3,
      });
    }
  });

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.5, theme, style);
};

const buildGrid: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'grid') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const cols = data.columns as number;
  const cellCount = data.cells.length;
  const rowCount = Math.ceil(cellCount / cols);
  const gap = 0.2;
  const cellW = (CONTENT_W - gap * (cols - 1)) / cols;
  const cellH = rowCount === 1 ? 3.0 : (3.5 - gap * (rowCount - 1)) / rowCount;

  data.cells.forEach((cell, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = PAD.left + col * (cellW + gap);
    const y = 1.3 + row * (cellH + gap);

    // Cell background
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x, y, w: cellW, h: cellH,
      fill: { color: pptxColor(theme.surface) },
      rectRadius: pxToInches(style.cardRadius),
      line: { width: 0 },
    });

    let innerY = y + 0.15;

    // Cell stat
    if (cell.stat !== undefined) {
      slide.addText(String(cell.stat), {
        x: x + 0.15, y: innerY, w: cellW - 0.3, h: 0.45,
        fontSize: ptSize('SECTION'),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.accent),
        bold: true,
      });
      innerY += 0.45;
    }

    // Cell title
    slide.addText(cell.title, {
      x: x + 0.15, y: innerY, w: cellW - 0.3, h: 0.3,
      fontSize: ptSize('CARD'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
    });
    innerY += 0.35;

    // Cell body
    if (cell.body) {
      slide.addText(cell.body, {
        x: x + 0.15, y: innerY, w: cellW - 0.3, h: cellH - (innerY - y) - 0.15,
        fontSize: ptSize('CAPTION'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        valign: 'top',
        lineSpacingMultiple: 1.3,
      });
    }
  });

  // Callout
  if (data.callout) addCallout(slide, data.callout, 4.8, theme, style);
};

const buildClosing: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'closing') return;

  // Title
  slide.addText(transformText(data.title, style), {
    x: PAD.left, y: 0.8, w: CONTENT_W, h: 1.0,
    fontSize: ptSize('HERO'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('HERO'),
    valign: 'middle',
  });

  // Subtitle
  if (data.subtitle) {
    slide.addText(data.subtitle, {
      x: PAD.left, y: 1.9, w: CONTENT_W, h: 0.5,
      fontSize: ptSize('SECTION'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
    });
  }

  addAccentBar(slide, PAD.left, 2.5, 1.5, theme, style);

  // Next steps
  if (data.nextSteps && data.nextSteps.length > 0) {
    const items: PptxGenJS.TextProps[] = data.nextSteps.map((step) => ({
      text: step,
      options: {
        bullet: true,
        fontSize: ptSize('BODY'),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
      },
    }));
    slide.addText(items, {
      x: PAD.left, y: 2.7, w: CONTENT_W, h: 2.0,
      valign: 'top',
      lineSpacingMultiple: 1.6,
    });
  }

  // Contact
  if (data.contact) {
    slide.addText(data.contact, {
      x: PAD.left, y: 5.0, w: CONTENT_W, h: 0.35,
      fontSize: ptSize('CAPTION'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
    });
  }
};

// ---------------------------------------------------------------------------
// Registry
// ---------------------------------------------------------------------------

export const PPTX_BUILDERS: Record<LayoutId, SlideBuilder> = {
  cover: buildCover,
  section: buildSection,
  text: buildText,
  cards: buildCards,
  number: buildNumber,
  compare: buildCompare,
  steps: buildSteps,
  table: buildTable,
  scorecard: buildScorecard,
  timeline: buildTimeline,
  grid: buildGrid,
  closing: buildClosing,
};
