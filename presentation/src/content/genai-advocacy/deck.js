/**
 * GenAI Advocacy Hub — Deck Manifest (content-layer integration)
 *
 * This module merges structure (layout skeleton) with swappable text content.
 * To use different text on the same slide layouts, swap the content import:
 *
 *   import content from "./alternative-content.json";
 *
 * All original exports are preserved for backward compatibility with
 * App.v14.jsx, Storybook stories, and export scripts.
 */

import { mergeDeckContent } from "../merge-deck-content.ts";
import { structure, HERO_IMGS as _HERO_IMGS } from "./structure.js";
import content from "./content.json" with { type: "json" };

// ── Merge structure + content ───────────────────────────────────────────
const merged = mergeDeckContent(structure, content);

// ── Backward-compatible exports ─────────────────────────────────────────

export const themeId = merged.themeId;
export const HERO_IMGS = _HERO_IMGS;
export const sprintNodes = merged.sprintNodes;

/** All slides (shell + content), sorted by order */
export const slides = merged.slides;

/** Content slides only (shell slides excluded), sorted by order */
export const contentSlides = merged.contentSlides;

/** Slide ID/label pairs for export scripts */
export const SLIDES = merged.slides.map(({ id, label }) => ({ id, label }));

/** Deck-level text metadata for App.v14 createDeckPreset */
export const deckMeta = merged.deckMeta;

export default slides;
