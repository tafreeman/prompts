/**
 * E2E lifecycle tests -- validates the full YAML-to-PPTX pipeline.
 *
 * These tests run against the Node.js modules directly (no dev server needed).
 */
import { describe, it, expect, afterAll } from 'vitest';
import { resolve } from 'node:path';
import { writeFileSync, mkdirSync, rmSync } from 'node:fs';

import { loadDeck, loadDeckOrThrow } from '../src/parse.js';
import { validateManifest } from '../src/schemas/manifest.js';
import { LAYOUT_IDS } from '../src/schemas/slide.js';
import { THEMES } from '../src/tokens/themes.js';
import { STYLE_MODES } from '../src/tokens/style-modes.js';
import { FRAMEWORKS } from '../src/frameworks/index.js';
import {
  executiveBriefManifest,
  pitchDeckManifest,
  strategySCRManifest,
  techArchitectureManifest,
  statusReportManifest,
} from '../src/frameworks/index.js';
import { renderPptx } from '../src/export/pptx-renderer.js';

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const EXAMPLE_DECK = resolve(__dirname, '..', 'decks', 'example-pitch.yaml');
const TMP_DIR = resolve(__dirname, '..', '.tmp-test');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function tmpYaml(name: string, content: string): string {
  mkdirSync(TMP_DIR, { recursive: true });
  const p = resolve(TMP_DIR, name);
  writeFileSync(p, content, 'utf-8');
  return p;
}

function cleanup() {
  try {
    rmSync(TMP_DIR, { recursive: true, force: true });
  } catch {
    // ignore
  }
}

// ---------------------------------------------------------------------------
// 1. Validate example deck
// ---------------------------------------------------------------------------

describe('Example deck validation', () => {
  it('loadDeckOrThrow succeeds on example-pitch.yaml', () => {
    const manifest = loadDeckOrThrow(EXAMPLE_DECK);
    expect(manifest).toBeDefined();
    expect(manifest.title).toBeTruthy();
    expect(manifest.slides.length).toBeGreaterThanOrEqual(1);
  });
});

// ---------------------------------------------------------------------------
// 2-6. Validate bad decks
// ---------------------------------------------------------------------------

describe('Bad deck validation', () => {
  afterAll(cleanup);

  it('rejects missing title with actionable error', () => {
    const yaml = `
title: Test
theme: midnight-teal
style: clean
slides:
  - id: s1
    layout: cover
    title: ""
`;
    const result = loadDeck(tmpYaml('missing-title.yaml', yaml));
    expect(result.success).toBe(false);
    expect(result.errors!.join('\n')).toMatch(/Action title required/i);
  });

  it('rejects more than 7 bullets', () => {
    const bullets = Array.from({ length: 8 }, (_, i) => `      - "Bullet ${i + 1}"`).join('\n');
    const yaml = `
title: Test
theme: midnight-teal
style: clean
slides:
  - id: s1
    layout: text
    title: "Valid Title Here"
    bullets:
${bullets}
`;
    const result = loadDeck(tmpYaml('too-many-bullets.yaml', yaml));
    expect(result.success).toBe(false);
    expect(result.errors!.join('\n')).toMatch(/max 7/i);
  });

  it('rejects more than 6 cards', () => {
    const cards = Array.from({ length: 7 }, (_, i) =>
      `      - title: "Card ${i + 1}"`
    ).join('\n');
    const yaml = `
title: Test
theme: midnight-teal
style: clean
slides:
  - id: s1
    layout: cards
    title: "Valid Title Here"
    cards:
${cards}
`;
    const result = loadDeck(tmpYaml('too-many-cards.yaml', yaml));
    expect(result.success).toBe(false);
    const errText = result.errors!.join('\n').toLowerCase();
    expect(errText).toMatch(/at most 6|max 6/i);
  });

  it('rejects duplicate slide IDs', () => {
    const yaml = `
title: Test
theme: midnight-teal
style: clean
slides:
  - id: dupe
    layout: cover
    title: "First slide"
  - id: dupe
    layout: section
    title: "Second slide"
`;
    const result = loadDeck(tmpYaml('dupe-ids.yaml', yaml));
    expect(result.success).toBe(false);
    expect(result.errors!.join('\n').toLowerCase()).toMatch(/duplicate/i);
  });

  it('rejects invalid layout name', () => {
    const yaml = `
title: Test
theme: midnight-teal
style: clean
slides:
  - id: s1
    layout: nonexistent-layout
    title: "Valid Title Here"
`;
    const result = loadDeck(tmpYaml('bad-layout.yaml', yaml));
    expect(result.success).toBe(false);
    expect(result.errors).toBeDefined();
    expect(result.errors!.length).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// 7. All 12 layout IDs exist
// ---------------------------------------------------------------------------

describe('Layout registry', () => {
  it('has exactly 12 layout IDs', () => {
    expect(LAYOUT_IDS.length).toBe(12);
  });

  it('contains the expected IDs', () => {
    const expected = [
      'cover', 'section', 'text', 'cards', 'number', 'compare',
      'steps', 'table', 'scorecard', 'timeline', 'grid', 'closing',
    ];
    for (const id of expected) {
      expect(LAYOUT_IDS).toContain(id);
    }
  });
});

// ---------------------------------------------------------------------------
// 8. All 6 themes exist
// ---------------------------------------------------------------------------

describe('Themes', () => {
  it('has exactly 6 themes', () => {
    expect(THEMES.length).toBe(6);
  });

  it('each theme has required fields', () => {
    for (const theme of THEMES) {
      expect(theme.id).toBeTruthy();
      expect(theme.name).toBeTruthy();
      expect(theme.bg).toBeTruthy();
      expect(theme.text).toBeTruthy();
      expect(theme.accent).toBeTruthy();
      expect(theme.surface).toBeTruthy();
      expect(theme.fontDisplay).toBeTruthy();
      expect(theme.fontBody).toBeTruthy();
    }
  });
});

// ---------------------------------------------------------------------------
// 9. All 3 style modes exist
// ---------------------------------------------------------------------------

describe('Style modes', () => {
  it('has exactly 3 style modes', () => {
    expect(STYLE_MODES.length).toBe(3);
  });
});

// ---------------------------------------------------------------------------
// 10. All 5 frameworks exist and their sampleManifests validate
// ---------------------------------------------------------------------------

describe('Frameworks', () => {
  it('has exactly 5 frameworks', () => {
    expect(FRAMEWORKS.length).toBe(5);
  });

  const sampleManifests = [
    { name: 'executive-brief', manifest: executiveBriefManifest },
    { name: 'pitch-deck', manifest: pitchDeckManifest },
    { name: 'strategy-scr', manifest: strategySCRManifest },
    { name: 'tech-architecture', manifest: techArchitectureManifest },
    { name: 'status-report', manifest: statusReportManifest },
  ];

  for (const { name, manifest } of sampleManifests) {
    it(`${name} sampleManifest validates`, () => {
      const result = validateManifest(manifest);
      expect(result.success).toBe(true);
      if (!result.success) {
        // Show errors for debugging if it fails
        console.error(`${name} errors:`, result.errors);
      }
    });
  }
});

// ---------------------------------------------------------------------------
// 11. Export PPTX
// ---------------------------------------------------------------------------

describe('PPTX export', () => {
  it('renderPptx returns a non-empty Buffer', async () => {
    const manifest = loadDeckOrThrow(EXAMPLE_DECK);
    const buffer = await renderPptx(manifest);
    expect(buffer).toBeInstanceOf(Buffer);
    expect(buffer.length).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// 12. Parse invalid YAML
// ---------------------------------------------------------------------------

describe('Invalid YAML handling', () => {
  afterAll(cleanup);

  it('loadDeck returns error for malformed YAML', () => {
    const badYaml = `
title: Test
slides:
  - id: broken
    layout: cover
    title: "Valid"
  invalid yaml here: [[[
`;
    const result = loadDeck(tmpYaml('malformed.yaml', badYaml));
    expect(result.success).toBe(false);
    expect(result.errors).toBeDefined();
    expect(result.errors!.some((e) => e.toLowerCase().includes('yaml') || e.toLowerCase().includes('parse'))).toBe(true);
  });

  it('loadDeck returns error for nonexistent file', () => {
    const result = loadDeck('/nonexistent/path/to/deck.yaml');
    expect(result.success).toBe(false);
    expect(result.errors!.join('\n')).toMatch(/not found/i);
  });
});
