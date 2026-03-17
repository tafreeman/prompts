/**
 * Current (Advocacy) Deck — Deck Manifest (content-layer integration)
 *
 * This is the original advocacy deck, previously inline in App.v14.jsx.
 * Merges structure (layout skeleton) with swappable text content.
 */

import { mergeDeckContent } from "../merge-deck-content.ts";
import { structure } from "./structure.js";
import content from "./content.json";

const merged = mergeDeckContent(structure, content);

export const themeId = merged.themeId;
export const sprintNodes = merged.sprintNodes;
export const slides = merged.slides;
export const contentSlides = merged.contentSlides;
export const deckMeta = merged.deckMeta;

export default slides;
