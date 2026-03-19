import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import yaml from 'js-yaml';
import { validateManifest, validateManifestOrThrow } from './schemas/index.js';
import type { DeckManifest, ValidationResult } from './schemas/index.js';

/**
 * Load and validate a deck YAML file.
 *
 * Pipeline: read file -> YAML parse -> Zod validate -> typed DeckManifest
 */
export function loadDeck(filePath: string): ValidationResult {
  const absPath = resolve(filePath);
  let raw: string;

  try {
    raw = readFileSync(absPath, 'utf-8');
  } catch {
    return {
      success: false,
      errors: [`File not found: ${absPath}`],
    };
  }

  let parsed: unknown;
  try {
    parsed = yaml.load(raw);
  } catch (err) {
    return {
      success: false,
      errors: [`YAML parse error: ${(err as Error).message}`],
    };
  }

  return validateManifest(parsed);
}

/**
 * Load and validate -- throws on any failure.
 */
export function loadDeckOrThrow(filePath: string): DeckManifest {
  const absPath = resolve(filePath);
  const raw = readFileSync(absPath, 'utf-8');
  const parsed = yaml.load(raw);
  return validateManifestOrThrow(parsed);
}
