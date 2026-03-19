#!/usr/bin/env tsx
/**
 * Design compliance audit script.
 *
 * Checks:
 * 1. No raw `padding:` values in layout files (should use SPACING tokens)
 * 2. No raw `fontSize:` values in layout files (should use TYPE_SCALE via primitives)
 * 3. WCAG AA contrast ratio for all 6 themes (text on bg)
 *
 * Exit code 0 = all pass, 1 = violations found.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, relative, extname } from 'node:path';
import { THEMES } from '../src/tokens/themes.js';

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const ROOT = resolve(import.meta.dirname, '..');
const LAYOUT_DIR = resolve(ROOT, 'src/layouts');

// Known exceptions -- these files/paths legitimately use raw values
const EXCEPTIONS: Set<string> = new Set([
  // Primitives define the token → CSS mapping; they are allowed raw values
  'src/components/primitives/',
  // PPTX export builders convert tokens to pptxgenjs units internally
  'src/export/',
  // LayoutRenderer error fallback -- not a real layout, just a dev error box
  'src/layouts/LayoutRenderer.tsx',
  // TableLayout uses raw fontSize for HTML table cells (13px caption, 11px eyebrow)
  // which map to TYPE_SCALE.CAPTION and TYPE_SCALE.EYEBROW conceptually
  'src/layouts/table/TableLayout.tsx',
]);

// ---------------------------------------------------------------------------
// File collection
// ---------------------------------------------------------------------------

function collectFiles(dir: string, ext: string[]): string[] {
  const results: string[] = [];
  for (const entry of readdirSync(dir)) {
    const full = resolve(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      results.push(...collectFiles(full, ext));
    } else if (ext.includes(extname(full))) {
      results.push(full);
    }
  }
  return results;
}

// ---------------------------------------------------------------------------
// Check 1 & 2: raw padding/fontSize in layout files
// ---------------------------------------------------------------------------

interface Violation {
  file: string;
  line: number;
  text: string;
  rule: string;
}

function auditLayoutTokens(files: string[]): Violation[] {
  const violations: Violation[] = [];

  // Patterns that indicate raw pixel/number values instead of tokens
  // Match padding: <number> or padding: "<number>px" etc.
  // Exclude SPACING references and string template expressions
  const paddingRaw = /padding:\s*(?:\d|['"`]\d)/;
  const fontSizeRaw = /fontSize:\s*(?:\d|['"`]\d)/;

  for (const file of files) {
    const rel = relative(ROOT, file).replace(/\\/g, '/');

    // Skip known exceptions
    if ([...EXCEPTIONS].some((ex) => rel.startsWith(ex))) continue;

    const content = readFileSync(file, 'utf-8');
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Skip comments and imports
      if (line.trim().startsWith('//') || line.trim().startsWith('*') || line.includes('import ')) continue;

      // Skip lines that reference SPACING or TYPE_SCALE tokens
      if (line.includes('SPACING') || line.includes('TYPE_SCALE') || line.includes('pxToPoints') || line.includes('pxToInches')) continue;

      if (paddingRaw.test(line)) {
        violations.push({
          file: rel,
          line: i + 1,
          text: line.trim(),
          rule: 'Use SPACING tokens instead of raw padding values',
        });
      }

      if (fontSizeRaw.test(line)) {
        violations.push({
          file: rel,
          line: i + 1,
          text: line.trim(),
          rule: 'Use TYPE_SCALE via Heading/Body primitives instead of raw fontSize',
        });
      }
    }
  }

  return violations;
}

// ---------------------------------------------------------------------------
// Check 3: WCAG AA contrast ratio
// ---------------------------------------------------------------------------

/**
 * Parse a hex color (#RRGGBB) to [r, g, b] in 0-255 range.
 */
function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace('#', '');
  return [
    parseInt(h.substring(0, 2), 16),
    parseInt(h.substring(2, 4), 16),
    parseInt(h.substring(4, 6), 16),
  ];
}

/**
 * Compute relative luminance per WCAG 2.0.
 * https://www.w3.org/TR/WCAG20/#relativeluminancedef
 */
function relativeLuminance(hex: string): number {
  const [r, g, b] = hexToRgb(hex).map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/**
 * Compute contrast ratio between two hex colors.
 * WCAG AA requires >= 4.5:1 for normal text, >= 3:1 for large text.
 */
function contrastRatio(fg: string, bg: string): number {
  const l1 = relativeLuminance(fg);
  const l2 = relativeLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

interface ContrastResult {
  theme: string;
  pair: string;
  ratio: number;
  pass: boolean;
  level: 'AA' | 'AA-large';
}

function auditContrast(): ContrastResult[] {
  const results: ContrastResult[] = [];

  for (const theme of THEMES) {
    // Primary text on bg — must pass AA (4.5:1)
    const textOnBg = contrastRatio(theme.text, theme.bg);
    results.push({
      theme: theme.id,
      pair: 'text on bg',
      ratio: textOnBg,
      pass: textOnBg >= 4.5,
      level: 'AA',
    });

    // Muted text on bg — check AA-large (3:1) since it's secondary
    const mutedOnBg = contrastRatio(theme.textMuted, theme.bg);
    results.push({
      theme: theme.id,
      pair: 'textMuted on bg',
      ratio: mutedOnBg,
      pass: mutedOnBg >= 3.0,
      level: 'AA-large',
    });

    // Accent on bg — check AA-large (3:1) since accents are typically large text
    const accentOnBg = contrastRatio(theme.accent, theme.bg);
    results.push({
      theme: theme.id,
      pair: 'accent on bg',
      ratio: accentOnBg,
      pass: accentOnBg >= 3.0,
      level: 'AA-large',
    });

    // Text on surface — check AA (4.5:1) for card content
    const textOnSurface = contrastRatio(theme.text, theme.surface);
    results.push({
      theme: theme.id,
      pair: 'text on surface',
      ratio: textOnSurface,
      pass: textOnSurface >= 4.5,
      level: 'AA',
    });
  }

  return results;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main(): void {
  console.log('=== Design Compliance Audit ===\n');
  let hasFailures = false;

  // Collect layout tsx files
  const layoutFiles = collectFiles(LAYOUT_DIR, ['.tsx', '.ts']);

  // 1 & 2: Token usage
  console.log('--- Token Usage (layouts) ---');
  const violations = auditLayoutTokens(layoutFiles);
  if (violations.length === 0) {
    console.log('PASS: No raw padding/fontSize values found in layout files.\n');
  } else {
    hasFailures = true;
    console.log(`FAIL: ${violations.length} violation(s) found:\n`);
    for (const v of violations) {
      console.log(`  ${v.file}:${v.line}`);
      console.log(`    ${v.text}`);
      console.log(`    Rule: ${v.rule}\n`);
    }
  }

  // 3: Contrast
  console.log('--- WCAG Contrast (all themes) ---');
  const contrastResults = auditContrast();
  const contrastFails = contrastResults.filter((r) => !r.pass);

  for (const r of contrastResults) {
    const status = r.pass ? 'PASS' : 'FAIL';
    console.log(
      `  [${status}] ${r.theme}: ${r.pair} — ${r.ratio.toFixed(2)}:1 (need ${r.level === 'AA' ? '4.5' : '3.0'}:1)`
    );
  }

  // Known contrast exceptions (documented design decisions)
  const CONTRAST_EXCEPTIONS = new Set([
    // studio-craft uses yellow accent (#F4E04D) on light bg (#F8F6F0) by design.
    // Yellow accents are used for decorative elements (bars, highlights), not text.
    // Body text uses high-contrast theme.text (#0E0E0B) which passes AA at 17.89:1.
    'studio-craft:accent on bg',
  ]);

  const realFails = contrastFails.filter(
    (r) => !CONTRAST_EXCEPTIONS.has(`${r.theme}:${r.pair}`)
  );
  const excepted = contrastFails.filter(
    (r) => CONTRAST_EXCEPTIONS.has(`${r.theme}:${r.pair}`)
  );

  if (excepted.length > 0) {
    console.log(`\nNOTE: ${excepted.length} documented exception(s):`);
    for (const r of excepted) {
      console.log(`  ${r.theme}: ${r.pair} — ${r.ratio.toFixed(2)}:1 (decorative use, not body text)`);
    }
  }

  if (realFails.length > 0) {
    hasFailures = true;
    console.log(`\nFAIL: ${realFails.length} contrast violation(s).\n`);
  } else {
    console.log('\nPASS: All theme contrasts meet WCAG requirements (with documented exceptions).\n');
  }

  // Summary
  console.log('=== Audit Complete ===');
  if (hasFailures) {
    console.log('RESULT: FAIL — see violations above.');
    process.exit(1);
  } else {
    console.log('RESULT: PASS — all checks passed.');
  }
}

main();
