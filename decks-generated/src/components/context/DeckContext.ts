import { createContext } from 'react';
import type { DeckManifest } from '../../schemas/manifest.js';

/**
 * Currently loaded deck manifest. null = no deck loaded.
 * Provides deck-level metadata (title, theme, style) to any component.
 */
export const DeckContext = createContext<DeckManifest | null>(null);
