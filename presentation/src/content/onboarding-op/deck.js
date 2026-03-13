// ─── Onboarding One-Pager Deck ───
// Reuses all onboarding content remapped to dense op-* one-pager layouts.
import { contentSlides as src, sprintNodes } from "../onboarding/deck.js";
export { sprintNodes };
export const themeId = "linear";

const LAYOUT_MAP = {
  "info-cards": "op-brief",
  "checklist":  "op-brief",
  "workflow":   "op-flow",
  "pillars":    "op-brief",
  "catalog":    "op-flow",
};

export const contentSlides = src.map(slide => ({
  ...slide,
  layout: LAYOUT_MAP[slide.layout] || "op-brief",
}));
