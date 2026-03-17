/**
 * Signal Cobalt — Deck Manifest (content-layer integration)
 *
 * Merges structure (layout skeleton) with swappable text content.
 * Swap the content import to reuse these layouts with different text.
 */

import { mergeDeckContent } from "../merge-deck-content.ts";
import { structure, HERO_IMGS as _HERO_IMGS } from "./structure.js";
import content from "./content.json";

const merged = mergeDeckContent(structure, content);

export const themeId = merged.themeId;
export const HERO_IMGS = _HERO_IMGS;
export const sprintNodes = merged.sprintNodes;
export const slides = merged.slides;
export const contentSlides = merged.contentSlides;
export const deckMeta = merged.deckMeta;

export const SLIDES = merged.slides.map(({ id, label }) => ({ id, label }));

export default slides;
