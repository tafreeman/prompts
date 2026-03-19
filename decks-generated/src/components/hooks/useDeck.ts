import { useContext } from 'react';
import type { DeckManifest } from '../../schemas/manifest.js';
import { DeckContext } from '../context/DeckContext.js';

/** Read the currently loaded deck manifest from context. null = no deck loaded. */
export function useDeck(): DeckManifest | null {
  return useContext(DeckContext);
}
