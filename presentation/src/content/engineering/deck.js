/**
 * Engineering Deck — Manifest (content-layer integration)
 *
 * Merges structure (layout skeleton) with swappable text content.
 * Swap the content import to reuse these layouts with different text.
 */

import { mergeDeckContent } from "../merge-deck-content.ts";
import { structure } from "./structure.js";
import content from "./content.json";

const merged = mergeDeckContent(structure, content);

export const themeId = merged.themeId;
export const sprintNodes = merged.sprintNodes;
export const contentSlides = merged.contentSlides;
export const deckMeta = merged.deckMeta;

export default merged.slides;
