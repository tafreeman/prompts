/**
 * CLI: Create a new deck from a framework template.
 *
 * Usage: npm run new-deck -- --framework pitch-deck --name my-deck
 */
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import yaml from 'js-yaml';
import { FRAMEWORKS_BY_ID, FRAMEWORKS } from '../src/frameworks/index.js';

// -- Parse args ---------------------------------------------------------------

function parseArgs(argv: string[]): { framework: string; name: string } {
  let framework = '';
  let name = '';

  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--framework' && argv[i + 1]) {
      framework = argv[++i];
    } else if (argv[i] === '--name' && argv[i + 1]) {
      name = argv[++i];
    }
  }

  return { framework, name };
}

const { framework: frameworkId, name: deckName } = parseArgs(process.argv);

// -- Validate -----------------------------------------------------------------

if (!frameworkId || !deckName) {
  console.error('Usage: npm run new-deck -- --framework <id> --name <kebab-case-name>');
  console.error('');
  console.error('Available frameworks:');
  FRAMEWORKS.forEach((f) => {
    console.error(`  ${f.id.padEnd(22)} ${f.name} (${f.audience})`);
  });
  process.exit(1);
}

const fw = FRAMEWORKS_BY_ID[frameworkId];

if (!fw) {
  console.error(`Unknown framework: "${frameworkId}"`);
  console.error('');
  console.error('Available frameworks:');
  FRAMEWORKS.forEach((f) => {
    console.error(`  ${f.id.padEnd(22)} ${f.name}`);
  });
  process.exit(1);
}

// -- Load the sampleManifest dynamically by ID --------------------------------

const frameworkModule = await import(`../src/frameworks/${frameworkId}.js`);
const manifest = frameworkModule.sampleManifest;

if (!manifest) {
  console.error(`Framework "${frameworkId}" does not export a sampleManifest.`);
  process.exit(1);
}

// -- Write YAML ---------------------------------------------------------------

const deckDir = resolve('decks', deckName);
const manifestPath = join(deckDir, 'manifest.yaml');

if (existsSync(manifestPath)) {
  console.error(`Deck already exists: ${manifestPath}`);
  console.error('Choose a different name or delete the existing deck first.');
  process.exit(1);
}

mkdirSync(deckDir, { recursive: true });

const yamlContent = yaml.dump(manifest, {
  lineWidth: 120,
  noRefs: true,
  quotingType: '"',
  forceQuotes: false,
});

writeFileSync(manifestPath, yamlContent, 'utf-8');

console.log(`Created new deck from "${fw.name}" framework:`);
console.log(`  ${manifestPath}`);
console.log('');
console.log('Next steps:');
console.log(`  1. Edit ${manifestPath} — replace [placeholder] values with real content`);
console.log(`  2. Run: npm run validate ${manifestPath}`);
console.log('  3. Preview in browser: npm run dev');
console.log('');
