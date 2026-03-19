/**
 * CLI: Export a deck YAML to PPTX.
 *
 * Usage: npm run export:pptx -- decks/example-pitch.yaml
 */
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { loadDeckOrThrow } from '../src/parse.js';
import { renderPptx } from '../src/export/index.js';

async function main(): Promise<void> {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('Usage: npm run export:pptx -- <deck.yaml>');
    process.exit(1);
  }

  const absPath = resolve(inputPath);
  console.log(`Loading deck: ${absPath}`);

  const manifest = loadDeckOrThrow(absPath);
  console.log(`Validated: "${manifest.title}" (${manifest.slides.length} slides, theme=${manifest.theme}, style=${manifest.style})`);

  console.log('Rendering PPTX...');
  const buffer = await renderPptx(manifest);

  // Create output directory
  const outputDir = resolve('output');
  mkdirSync(outputDir, { recursive: true });

  // Kebab-case filename from title
  const slug = manifest.title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
  const outputPath = resolve(outputDir, `${slug}.pptx`);

  writeFileSync(outputPath, buffer);

  const sizeMB = (buffer.length / 1024 / 1024).toFixed(2);
  console.log(`\nExported: ${outputPath}`);
  console.log(`Size: ${sizeMB} MB (${buffer.length.toLocaleString()} bytes)`);
}

main().catch((err) => {
  console.error('Export failed:', err);
  process.exit(1);
});
