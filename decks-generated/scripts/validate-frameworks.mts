/**
 * Validates all framework sampleManifests against the DeckManifest schema.
 * Run: npx tsx scripts/validate-frameworks.mts
 */
import { validateManifest } from '../src/schemas/manifest.js';
import { sampleManifest as eb } from '../src/frameworks/executive-brief.js';
import { sampleManifest as pd } from '../src/frameworks/pitch-deck.js';
import { sampleManifest as scr } from '../src/frameworks/strategy-scr.js';
import { sampleManifest as ta } from '../src/frameworks/tech-architecture.js';
import { sampleManifest as sr } from '../src/frameworks/status-report.js';

const manifests: [string, unknown][] = [
  ['executive-brief', eb],
  ['pitch-deck', pd],
  ['strategy-scr', scr],
  ['tech-architecture', ta],
  ['status-report', sr],
];

let allPass = true;

for (const [name, manifest] of manifests) {
  const result = validateManifest(manifest);
  if (result.success) {
    console.log(`PASS: ${name} (${result.data!.slides.length} slides)`);
  } else {
    allPass = false;
    console.log(`FAIL: ${name}`);
    result.errors!.forEach((e) => console.log(`  ${e}`));
  }
}

if (!allPass) {
  process.exit(1);
}

console.log('\nAll framework sampleManifests are valid.');
