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
import type { z } from 'zod';
import type { ChartSlide, HubSlide, WorkflowSlide, CycleSlide } from '../schemas/slide.js';
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
// ChartLayout PPTX builder
// ---------------------------------------------------------------------------

type ChartData = z.infer<typeof ChartSlide>;

/** Compute global [min, max] across all bar values (always includes 0). */
function chartDomain(data: ChartData): { min: number; max: number } {
  const all = data.groups.flatMap((g) => g.bars.map((b) => b.value));
  return { min: Math.min(0, ...all), max: Math.max(0, ...all) };
}

const buildChart: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'chart') return;
  const chart = data as unknown as ChartData;

  // Title
  slide.addText(transformText(chart.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.6,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  addAccentBar(slide, PAD.left, PAD.top + 0.65, 1.0, theme, style);

  const { min, max } = chartDomain(chart);
  const range = max - min || 1;
  const hasAnnotations = (chart.annotations?.length ?? 0) > 0;

  // Layout geometry (inches)
  const GROUP_LABEL_W = 1.1;
  const ANNO_W = hasAnnotations ? 1.8 : 0;
  const ANNO_GAP = hasAnnotations ? 0.2 : 0;
  const BAR_AREA_W = CONTENT_W - GROUP_LABEL_W - ANNO_W - ANNO_GAP;
  const CONTENT_TOP = 1.0;
  const AVAILABLE_H = 5.625 - PAD.bottom - CONTENT_TOP - (chart.source ? 0.35 : 0);

  const totalBars = chart.groups.reduce((s, g) => s + g.bars.length, 0);
  const groupGap = pxToInches(16);
  const barH = Math.min(
    0.22,
    (AVAILABLE_H - groupGap * (chart.groups.length - 1)) / (totalBars + chart.groups.length * 0.3),
  );
  const barGap = pxToInches(3);

  // Baseline X position (0 value) within bar area
  const baselineRatio = -min / range;
  const baselineX = PAD.left + GROUP_LABEL_W + baselineRatio * BAR_AREA_W;

  // Baseline tick line (vertical)
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: baselineX,
    y: CONTENT_TOP,
    w: pxToInches(1),
    h: AVAILABLE_H,
    fill: { color: pptxColor(theme.textDim) },
    line: { width: 0 },
  });

  // Render groups
  let curY = CONTENT_TOP;

  chart.groups.forEach((group, gi) => {
    if (gi > 0) curY += groupGap;

    // Group bracket label
    if (group.label) {
      const groupH = group.bars.length * (barH + barGap) - barGap;
      slide.addText(group.label, {
        x: PAD.left,
        y: curY,
        w: GROUP_LABEL_W - 0.1,
        h: groupH,
        fontSize: pxToPoints(10),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.textMuted),
        bold: true,
        align: 'right',
        valign: 'middle',
      });
    }

    group.bars.forEach((bar) => {
      const isNegative = bar.value < 0;
      const magnitudeRatio = Math.abs(bar.value) / range;
      const barLeft = isNegative
        ? PAD.left + GROUP_LABEL_W + (baselineRatio - magnitudeRatio) * BAR_AREA_W
        : baselineX;
      const barW = magnitudeRatio * BAR_AREA_W;

      // Highlight band behind the row
      if (bar.highlight) {
        slide.addShape('rect' as PptxGenJS.ShapeType, {
          x: PAD.left + GROUP_LABEL_W,
          y: curY,
          w: BAR_AREA_W,
          h: barH,
          fill: { color: pptxColor(theme.surface) },
          rectRadius: pxToInches(barH * 48 / 2),  // pill — very large radius
          line: { width: 0 },
        });
      }

      // Bar shape
      if (barW > 0) {
        slide.addShape('rect' as PptxGenJS.ShapeType, {
          x: barLeft,
          y: curY + barH * 0.15,
          w: Math.max(barW, pxToInches(2)),
          h: barH * 0.7,
          fill: { color: pptxColor(theme.accent), transparency: bar.accent ? 10 : 40 },
          line: { width: 0 },
        });
      }

      // Bar row label (left of baseline, italic)
      slide.addText(bar.label, {
        x: PAD.left + GROUP_LABEL_W,
        y: curY,
        w: baselineRatio * BAR_AREA_W - 0.05,
        h: barH,
        fontSize: pxToPoints(9),
        fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted),
        italic: true,
        align: 'right',
        valign: 'middle',
      });

      // Value label (beyond bar end)
      const unit = chart.unit ?? '';
      const valueText = `${bar.value > 0 ? '+' : ''}${bar.value}${unit}`;
      const valueLabelX = isNegative
        ? Math.max(PAD.left + GROUP_LABEL_W, barLeft - 0.4)
        : baselineX + magnitudeRatio * BAR_AREA_W + 0.03;

      slide.addText(valueText, {
        x: valueLabelX,
        y: curY,
        w: 0.5,
        h: barH,
        fontSize: pxToPoints(9),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.text),
        bold: true,
        valign: 'middle',
        align: isNegative ? 'right' : 'left',
      });

      curY += barH + barGap;
    });
  });

  // Annotations panel (right side)
  if (hasAnnotations && chart.annotations) {
    const annoX = PAD.left + GROUP_LABEL_W + BAR_AREA_W + ANNO_GAP;

    // Border line
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x: annoX - ANNO_GAP / 2,
      y: CONTENT_TOP,
      w: pxToInches(1),
      h: AVAILABLE_H,
      fill: { color: pptxColor(theme.textMuted) },
      line: { width: 0 },
    });

    let annoY = CONTENT_TOP;
    const annoItemH = 0.22;
    const annoGroupGap = 0.15;

    chart.annotations.forEach((anno, ai) => {
      if (ai > 0) annoY += annoGroupGap;

      // Annotation group label
      slide.addText(anno.label, {
        x: annoX,
        y: annoY,
        w: ANNO_W - 0.1,
        h: 0.3,
        fontSize: pxToPoints(9),
        fontFace: theme.fontDisplay,
        color: pptxColor(theme.textMuted),
        bold: true,
      });
      annoY += 0.35;

      (anno.items ?? []).forEach((item) => {
        // Item label
        slide.addText(item.label, {
          x: annoX,
          y: annoY,
          w: ANNO_W * 0.55,
          h: annoItemH,
          fontSize: pxToPoints(9),
          fontFace: theme.fontBody,
          color: pptxColor(theme.textMuted),
          italic: true,
          valign: 'middle',
        });
        // Item value
        slide.addText(item.value, {
          x: annoX + ANNO_W * 0.55,
          y: annoY,
          w: ANNO_W * 0.45 - 0.05,
          h: annoItemH,
          fontSize: pxToPoints(10),
          fontFace: theme.fontDisplay,
          color: pptxColor(theme.accent),
          bold: true,
          align: 'right',
          valign: 'middle',
        });
        annoY += annoItemH + pxToInches(2);
      });
    });
  }

  // Source
  if (chart.source) addSource(slide, chart.source, theme);
};

// ---------------------------------------------------------------------------
// HubLayout PPTX builder
// ---------------------------------------------------------------------------

type HubData = z.infer<typeof HubSlide>;

// Hub diagram geometry in inches (10" x 5.625" slide)
const HUB_SLIDE_W = 10;
const HUB_SLIDE_H = 5.625;
const HUB_BOX_INSET_X = 0.75;
const HUB_BOX_INSET_Y = 0.5;
const HUB_BOX_W = HUB_SLIDE_W - HUB_BOX_INSET_X * 2;
const HUB_BOX_H = HUB_SLIDE_H - HUB_BOX_INSET_Y * 2;
const HUB_CX = HUB_SLIDE_W / 2;
const HUB_CY = HUB_SLIDE_H / 2;
const HUB_CR = 0.9;  // circle radius in inches

function hubCircleEdge(corner: { x: number; y: number }): { x: number; y: number } {
  const dx = corner.x - HUB_CX;
  const dy = corner.y - HUB_CY;
  const dist = Math.sqrt(dx * dx + dy * dy);
  return {
    x: HUB_CX + (dx / dist) * HUB_CR,
    y: HUB_CY + (dy / dist) * HUB_CR,
  };
}

const buildHub: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'hub') return;
  const hub = data as unknown as HubData;

  const corners = {
    tl: { x: HUB_BOX_INSET_X, y: HUB_BOX_INSET_Y },
    tr: { x: HUB_BOX_INSET_X + HUB_BOX_W, y: HUB_BOX_INSET_Y },
    bl: { x: HUB_BOX_INSET_X, y: HUB_BOX_INSET_Y + HUB_BOX_H },
    br: { x: HUB_BOX_INSET_X + HUB_BOX_W, y: HUB_BOX_INSET_Y + HUB_BOX_H },
  };

  // Outer border rect
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: HUB_BOX_INSET_X,
    y: HUB_BOX_INSET_Y,
    w: HUB_BOX_W,
    h: HUB_BOX_H,
    fill: { type: 'none' },
    line: { color: pptxColor(theme.text), width: 0.75, transparency: 60 },
  });

  // Diagonal lines from corners to circle edge
  const diagonalCorners = [corners.tl, corners.tr, corners.bl, corners.br];
  diagonalCorners.forEach((corner) => {
    const edge = hubCircleEdge(corner);
    slide.addShape('line' as PptxGenJS.ShapeType, {
      x: corner.x,
      y: corner.y,
      w: edge.x - corner.x,
      h: edge.y - corner.y,
      line: { color: pptxColor(theme.text), width: 0.75, transparency: 65 },
    });
  });

  // Center circle
  slide.addShape('ellipse' as PptxGenJS.ShapeType, {
    x: HUB_CX - HUB_CR,
    y: HUB_CY - HUB_CR,
    w: HUB_CR * 2,
    h: HUB_CR * 2,
    fill: { type: 'none' },
    line: { color: pptxColor(theme.text), width: 0.75 },
  });

  // Center label
  slide.addText(hub.center.label, {
    x: HUB_CX - HUB_CR,
    y: hub.center.sublabel ? HUB_CY - HUB_CR + 0.3 : HUB_CY - 0.2,
    w: HUB_CR * 2,
    h: 0.4,
    fontSize: pxToPoints(18),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: true,
    align: 'center',
    valign: 'middle',
  });

  if (hub.center.sublabel) {
    slide.addText(hub.center.sublabel, {
      x: HUB_CX - HUB_CR,
      y: HUB_CY,
      w: HUB_CR * 2,
      h: 0.35,
      fontSize: pxToPoints(11),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.textMuted),
      align: 'center',
      valign: 'middle',
    });
  }

  // Spoke labels
  const spokeByPos = Object.fromEntries(
    hub.spokes.map((s) => [s.position, s]),
  ) as Partial<Record<'top' | 'bottom' | 'left' | 'right', (typeof hub.spokes)[number]>>;

  const SPOKE_LABEL_W = 2.0;
  const SPOKE_LABEL_H = 0.6;
  const EYEBROW_H = 0.2;
  const EYEBROW_OFFSET = 0.22;

  // Top spoke
  if (spokeByPos.top) {
    const spk = spokeByPos.top;
    const x = HUB_CX - SPOKE_LABEL_W / 2;
    const y = HUB_BOX_INSET_Y - SPOKE_LABEL_H - EYEBROW_H - 0.1;
    if (spk.eyebrow) {
      slide.addText(spk.eyebrow.toUpperCase(), {
        x, y, w: SPOKE_LABEL_W, h: EYEBROW_H,
        fontSize: pxToPoints(8),
        fontFace: theme.fontBody,
        color: pptxColor(theme.accent),
        bold: true,
        align: 'center',
      });
    }
    slide.addText(transformText(spk.label, style), {
      x, y: y + EYEBROW_OFFSET, w: SPOKE_LABEL_W, h: SPOKE_LABEL_H,
      fontSize: pxToPoints(11),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'center',
    });
  }

  // Bottom spoke
  if (spokeByPos.bottom) {
    const spk = spokeByPos.bottom;
    const x = HUB_CX - SPOKE_LABEL_W / 2;
    const y = HUB_BOX_INSET_Y + HUB_BOX_H + 0.1;
    if (spk.eyebrow) {
      slide.addText(spk.eyebrow.toUpperCase(), {
        x, y, w: SPOKE_LABEL_W, h: EYEBROW_H,
        fontSize: pxToPoints(8),
        fontFace: theme.fontBody,
        color: pptxColor(theme.accent),
        bold: true,
        align: 'center',
      });
    }
    slide.addText(transformText(spk.label, style), {
      x, y: y + EYEBROW_OFFSET, w: SPOKE_LABEL_W, h: SPOKE_LABEL_H,
      fontSize: pxToPoints(11),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'center',
    });
  }

  // Left spoke
  if (spokeByPos.left) {
    const spk = spokeByPos.left;
    const x = HUB_BOX_INSET_X - SPOKE_LABEL_W - 0.1;
    const midY = HUB_CY - (EYEBROW_H + SPOKE_LABEL_H) / 2;
    if (spk.eyebrow) {
      slide.addText(spk.eyebrow.toUpperCase(), {
        x, y: midY, w: SPOKE_LABEL_W, h: EYEBROW_H,
        fontSize: pxToPoints(8),
        fontFace: theme.fontBody,
        color: pptxColor(theme.accent),
        bold: true,
        align: 'right',
      });
    }
    slide.addText(transformText(spk.label, style), {
      x, y: midY + EYEBROW_OFFSET, w: SPOKE_LABEL_W, h: SPOKE_LABEL_H,
      fontSize: pxToPoints(11),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'right',
    });
  }

  // Right spoke
  if (spokeByPos.right) {
    const spk = spokeByPos.right;
    const x = HUB_BOX_INSET_X + HUB_BOX_W + 0.1;
    const midY = HUB_CY - (EYEBROW_H + SPOKE_LABEL_H) / 2;
    if (spk.eyebrow) {
      slide.addText(spk.eyebrow.toUpperCase(), {
        x, y: midY, w: SPOKE_LABEL_W, h: EYEBROW_H,
        fontSize: pxToPoints(8),
        fontFace: theme.fontBody,
        color: pptxColor(theme.accent),
        bold: true,
        align: 'left',
      });
    }
    slide.addText(transformText(spk.label, style), {
      x, y: midY + EYEBROW_OFFSET, w: SPOKE_LABEL_W, h: SPOKE_LABEL_H,
      fontSize: pxToPoints(11),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: true,
      align: 'left',
    });
  }

  // Title + body — bottom-right outside box
  const titleX = HUB_SLIDE_W - PAD.right - 3.0;
  const titleY = HUB_SLIDE_H - PAD.bottom - 0.7;
  slide.addText(transformText(hub.title, style), {
    x: titleX,
    y: titleY,
    w: 3.0,
    h: 0.35,
    fontSize: pxToPoints(11),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: true,
    align: 'right',
  });

  if (hub.body) {
    slide.addText(hub.body, {
      x: titleX,
      y: titleY + 0.38,
      w: 3.0,
      h: 0.5,
      fontSize: pxToPoints(9),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
      align: 'right',
      valign: 'top',
      lineSpacingMultiple: 1.3,
    });
  }
};

// ---------------------------------------------------------------------------
// WorkflowLayout PPTX builder
// ---------------------------------------------------------------------------

type WorkflowData = z.infer<typeof WorkflowSlide>;

const buildWorkflow: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'workflow') return;
  const wf = data as unknown as WorkflowData;

  const defaultLabels: [string, string, string] = ['Stage', 'What Happens', 'Time'];
  const [label0, label1, label2] = wf.columnLabels ?? defaultLabels;

  // Title
  slide.addText(transformText(wf.title, style), {
    x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.55,
    fontSize: ptSize('TITLE'),
    fontFace: theme.fontDisplay,
    color: pptxColor(theme.text),
    bold: isBold('TITLE'),
  });

  // Subtitle
  if (wf.subtitle) {
    slide.addText(wf.subtitle, {
      x: PAD.left, y: PAD.top + 0.6, w: CONTENT_W * 0.7, h: 0.4,
      fontSize: ptSize('BODY'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.textMuted),
    });
  }

  // Thin separator rule below header
  const ruleY = wf.subtitle ? PAD.top + 1.1 : PAD.top + 0.65;
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: PAD.left, y: ruleY, w: CONTENT_W, h: pxToInches(1),
    fill: { color: pptxColor(theme.text), transparency: 85 },
    line: { width: 0 },
  });

  // Column proportions: 25% | 55% | 20%
  const colStageW = CONTENT_W * 0.25;
  const colDescW  = CONTENT_W * 0.55;
  const colMetaW  = CONTENT_W * 0.20;

  // Column header row
  const headerRowY = ruleY + 0.1;
  const colHeaderH = 0.25;

  slide.addText(label0.toUpperCase(), {
    x: PAD.left, y: headerRowY, w: colStageW, h: colHeaderH,
    fontSize: ptSize('EYEBROW'), fontFace: theme.fontBody,
    color: pptxColor(theme.textDim), bold: true,
  });
  slide.addText(label1.toUpperCase(), {
    x: PAD.left + colStageW, y: headerRowY, w: colDescW, h: colHeaderH,
    fontSize: ptSize('EYEBROW'), fontFace: theme.fontBody,
    color: pptxColor(theme.textDim), bold: true,
  });
  slide.addText(label2.toUpperCase(), {
    x: PAD.left + colStageW + colDescW, y: headerRowY, w: colMetaW, h: colHeaderH,
    fontSize: ptSize('EYEBROW'), fontFace: theme.fontBody,
    color: pptxColor(theme.textDim), bold: true, align: 'right',
  });

  // Divider below column headers
  const colHeaderDivY = headerRowY + colHeaderH + 0.03;
  slide.addShape('rect' as PptxGenJS.ShapeType, {
    x: PAD.left, y: colHeaderDivY, w: CONTENT_W, h: pxToInches(1),
    fill: { color: pptxColor(theme.text), transparency: 90 },
    line: { width: 0 },
  });

  // Stage rows -- fill remaining height evenly
  const tableTop    = colHeaderDivY + 0.04;
  const tableBottom = 5.625 - PAD.bottom - 0.1;
  const stageCount  = wf.stages.length;
  const rowH        = (tableBottom - tableTop) / stageCount;

  wf.stages.forEach((stage, i) => {
    const rowY = tableTop + i * rowH;
    const isHighlight = stage.highlight === true;
    const textColor   = pptxColor(isHighlight ? theme.text : theme.textMuted);
    const bold        = isHighlight;

    // Stage label (monospace uppercase)
    slide.addText(stage.label, {
      x: PAD.left, y: rowY, w: colStageW - 0.1, h: rowH,
      fontSize: ptSize('EYEBROW'), fontFace: theme.fontDisplay,
      color: textColor, bold: true, valign: 'middle',
    });

    // Description
    if (stage.description) {
      slide.addText(stage.description, {
        x: PAD.left + colStageW, y: rowY, w: colDescW - 0.1, h: rowH,
        fontSize: ptSize('BODY'), fontFace: theme.fontBody,
        color: textColor, bold, valign: 'middle',
      });
    }

    // Meta (right-aligned, CARD size)
    if (stage.meta) {
      slide.addText(stage.meta, {
        x: PAD.left + colStageW + colDescW, y: rowY, w: colMetaW, h: rowH,
        fontSize: ptSize('CARD'), fontFace: theme.fontDisplay,
        color: textColor, bold: true, align: 'right', valign: 'middle',
      });
    }

    // Row divider (except last row)
    if (i < stageCount - 1) {
      slide.addShape('rect' as PptxGenJS.ShapeType, {
        x: PAD.left, y: rowY + rowH - pxToInches(0.5), w: CONTENT_W, h: pxToInches(1),
        fill: { color: pptxColor(theme.text), transparency: 90 },
        line: { width: 0 },
      });
    }
  });
};

// ---------------------------------------------------------------------------
// CycleLayout PPTX builder
// ---------------------------------------------------------------------------

type CycleData = z.infer<typeof CycleSlide>;

const buildCycle: SlideBuilder = (slide, data, theme, style) => {
  if (data.layout !== 'cycle') return;
  const cy = data as unknown as CycleData;

  // Eyebrow
  if (cy.eyebrow) {
    slide.addText(transformText(cy.eyebrow, style), {
      x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.3,
      fontSize: ptSize('EYEBROW'), fontFace: theme.fontBody,
      color: pptxColor(theme.accent), bold: true,
    });
  }

  // Title
  const titleY = cy.eyebrow ? PAD.top + 0.35 : PAD.top;
  slide.addText(transformText(cy.title, style), {
    x: PAD.left, y: titleY, w: CONTENT_W, h: 0.65,
    fontSize: ptSize('TITLE'), fontFace: theme.fontDisplay,
    color: pptxColor(theme.text), bold: isBold('TITLE'),
  });

  // Diagram geometry (inches)
  const diagramTop = titleY + 0.75;
  const diagramH   = 5.625 - PAD.bottom - diagramTop;
  const circleDiam = 2.2;
  const circleR    = circleDiam / 2;
  const CX         = PAD.left + CONTENT_W * 0.52;
  const CY         = diagramTop + diagramH / 2;

  // Circle outline (thin, muted)
  slide.addShape('ellipse' as PptxGenJS.ShapeType, {
    x: CX - circleR, y: CY - circleR, w: circleDiam, h: circleDiam,
    fill: { type: 'none' },
    line: { color: pptxColor(theme.text), width: 1, transparency: 80 },
  });

  // Accent accent ring (slightly larger, dashed — simulates partial arc)
  slide.addShape('ellipse' as PptxGenJS.ShapeType, {
    x: CX - circleR - 0.05, y: CY - circleR - 0.05,
    w: circleDiam + 0.1, h: circleDiam + 0.1,
    fill: { type: 'none' },
    line: { color: pptxColor(theme.accent), width: 4, dashType: 'dash' },
  });

  // Center label
  if (cy.centerLabel) {
    slide.addText(cy.centerLabel, {
      x: CX - circleR + 0.1, y: CY - 0.2, w: circleDiam - 0.2, h: 0.4,
      fontSize: ptSize('CAPTION'), fontFace: theme.fontDisplay,
      color: pptxColor(theme.text), bold: true,
      align: 'center', valign: 'middle',
    });
  }

  // Input block (left of circle)
  if (cy.input) {
    const inputW = CX - circleR - PAD.left - 0.15;
    const inputY = CY - 0.5;

    slide.addText(cy.input.label, {
      x: PAD.left, y: inputY, w: inputW, h: 0.4,
      fontSize: ptSize('CARD'), fontFace: theme.fontDisplay,
      color: pptxColor(theme.text), bold: true, align: 'right',
    });

    if (cy.input.body) {
      slide.addText(cy.input.body, {
        x: PAD.left, y: inputY + 0.45, w: inputW, h: 0.55,
        fontSize: ptSize('CAPTION'), fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted), align: 'right',
        lineSpacingMultiple: 1.3,
      });
    }

    // Dashed horizontal connector: input right edge → circle left edge
    slide.addShape('line' as PptxGenJS.ShapeType, {
      x: PAD.left + inputW, y: CY,
      w: CX - circleR - (PAD.left + inputW), h: 0,
      line: { color: pptxColor(theme.text), width: 1, transparency: 60, dashType: 'sysDot' },
    });
  }

  // Output items (right of circle)
  const outputCount    = cy.outputs.length;
  const outputX        = CX + circleR + 0.2;
  const outputW        = PAD.left + CONTENT_W - outputX;
  const outputAreaH    = diagramH * 0.85;
  const outputSpacing  = outputAreaH / outputCount;
  const outputAreaTop  = diagramTop + diagramH * 0.075;

  cy.outputs.forEach((output, i) => {
    const itemY = outputAreaTop + i * outputSpacing + outputSpacing / 2 - 0.25;

    // Accent dot bullet
    slide.addShape('ellipse' as PptxGenJS.ShapeType, {
      x: outputX, y: itemY + 0.1, w: 0.1, h: 0.1,
      fill: { color: pptxColor(theme.accent) }, line: { width: 0 },
    });

    // Label
    slide.addText(output.label, {
      x: outputX + 0.15, y: itemY, w: outputW - 0.15, h: 0.35,
      fontSize: ptSize('CARD'), fontFace: theme.fontDisplay,
      color: pptxColor(theme.text), bold: true,
    });

    // Body
    if (output.body) {
      slide.addText(output.body, {
        x: outputX + 0.15, y: itemY + 0.38, w: outputW - 0.15, h: 0.4,
        fontSize: ptSize('CAPTION'), fontFace: theme.fontBody,
        color: pptxColor(theme.textMuted), lineSpacingMultiple: 1.3,
      });
    }

    // Tick connector: circle right edge → item
    const connFromY = CY + (i - (outputCount - 1) / 2) * outputSpacing * 0.35;
    slide.addShape('line' as PptxGenJS.ShapeType, {
      x: CX + circleR, y: connFromY,
      w: outputX - (CX + circleR), h: (itemY + 0.13) - connFromY,
      line: { color: pptxColor(theme.text), width: 1, transparency: 65 },
    });
  });

  // Source
  if (cy.source) addSource(slide, cy.source, theme);
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
  chart: buildChart,
  hub: buildHub,
  workflow: buildWorkflow,
  cycle: buildCycle,
  quote: (slide, data, theme, _style) => {
    if (data.layout !== 'quote') return;

    // Eyebrow — slide title as small uppercase category label
    slide.addText(data.title.toUpperCase(), {
      x: PAD.left, y: PAD.top, w: CONTENT_W, h: 0.25,
      fontSize: ptSize('EYEBROW'),
      fontFace: theme.fontBody,
      color: pptxColor(theme.accent),
      bold: true,
      charSpacing: 2.5,
    });

    // Decorative opening quotation mark — large, visually faded via shape transparency
    // (pptxgenjs addText does not support transparency; use a shape overlay instead)
    slide.addShape('rect' as PptxGenJS.ShapeType, {
      x: PAD.left, y: PAD.top + 0.2, w: 2.5, h: 1.4,
      fill: { type: 'none' },
      line: { width: 0 },
    });
    slide.addText('\u201C', {
      x: PAD.left, y: PAD.top + 0.2, w: 2.5, h: 1.4,
      fontSize: 120,
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.accent),
      bold: true,
      valign: 'top',
    });

    // Quote text — HERO size, display font, full text color
    const quoteY = PAD.top + 1.0;
    slide.addText(data.quote, {
      x: PAD.left, y: quoteY, w: CONTENT_W, h: 2.8,
      fontSize: ptSize('HERO'),
      fontFace: theme.fontDisplay,
      color: pptxColor(theme.text),
      bold: isBold('HERO'),
      lineSpacingMultiple: 1.2,
      valign: 'top',
    });

    // Attribution block — only when name or role provided
    if (data.attribution || data.role) {
      const attrY = quoteY + 2.9;

      // Thin horizontal rule (1px-height filled rect at low opacity)
      slide.addShape('rect' as PptxGenJS.ShapeType, {
        x: PAD.left, y: attrY, w: CONTENT_W, h: pxToInches(1),
        fill: { color: pptxColor(theme.textMuted), transparency: 65 },
        line: { width: 0 },
      });

      if (data.attribution) {
        slide.addText(`\u2014\u2002${data.attribution}`, {
          x: PAD.left, y: attrY + 0.1, w: CONTENT_W, h: 0.35,
          fontSize: ptSize('CARD'),
          fontFace: theme.fontDisplay,
          color: pptxColor(theme.text),
          bold: true,
          valign: 'middle',
        });
      }

      if (data.role) {
        const roleY = attrY + (data.attribution ? 0.45 : 0.1);
        slide.addText(data.role, {
          x: PAD.left, y: roleY, w: CONTENT_W, h: 0.3,
          fontSize: ptSize('BODY'),
          fontFace: theme.fontBody,
          color: pptxColor(theme.textMuted),
          valign: 'middle',
        });
      }
    }

    // Optional logo — bottom-right corner (40px height ≈ 0.42")
    if (data.logo) {
      slide.addImage({
        path: data.logo,
        x: 10 - PAD.right - 1.2,
        y: 5.625 - PAD.bottom - 0.55,
        w: 1.2,
        h: 0.42,
        sizing: { type: 'contain', w: 1.2, h: 0.42 },
      });
    }
  },
};
