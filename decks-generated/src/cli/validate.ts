import { loadDeck } from '../parse.js';
import { LAYOUT_IDS } from '../schemas/index.js';

const filePath = process.argv[2];

if (!filePath) {
  console.error('Usage: npm run validate <path-to-deck.yaml>');
  console.error('');
  console.error('Available layouts:', LAYOUT_IDS.join(', '));
  process.exit(1);
}

console.log(`Validating: ${filePath}`);
console.log('');

const result = loadDeck(filePath);

if (result.success) {
  const { data } = result;
  console.log('\u2713 Valid deck manifest');
  console.log(`  Title:  ${data!.title}`);
  console.log(`  Theme:  ${data!.theme}`);
  console.log(`  Style:  ${data!.style}`);
  console.log(`  Slides: ${data!.slides.length}`);
  console.log('');
  data!.slides.forEach((slide, i) => {
    console.log(`  ${i + 1}. [${slide.layout}] ${slide.title}`);
  });
  process.exit(0);
} else {
  console.error('\u2717 Validation failed:');
  console.error('');
  result.errors!.forEach((err) => console.error(err));
  console.error('');
  console.error('Available layouts:', LAYOUT_IDS.join(', '));
  process.exit(1);
}
