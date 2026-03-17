/**
 * GenAI Advocacy — Deck Structure (layout skeleton).
 *
 * Contains layout IDs, ordering, colors, and visual metadata.
 * Text content lives in the companion `content.json`.
 * Combine with `mergeDeckContent(structure, content)` to produce a full deck.
 */

// ─── HERO IMAGE REFS ───
export const HERO_IMGS = {
  carrierFleet:     "images/carrier-fleet.jpg",
  helicopterRappel: "images/helicopter-rappel.jpg",
  droneDeck:        "images/drone-deck.jpg",
  carrierOps:       "images/carrier-ops.jpg",
  uavSunset:        "images/uav-sunset.jpg",
};

// ─── DECK STRUCTURE ───
export const structure = {
  themeId: "midnight-teal",

  /** Intro stat colors (text comes from content.json) */
  introStatColors: ["#67E8F9", "#38BDF8", "#10B981", "#A78BFA"],

  sprintNodes: [
    { abbr: "RQ", label: "Requirements",   type: "human" },
    { abbr: "UI", label: "UI Mockup",      type: "human" },
    { abbr: "AD", label: "AI AC Draft",    type: "ai"    },
    { abbr: "RF", label: "AC Refine",      type: "human" },
    { abbr: "RV", label: "Human Review",   type: "human" },
    { abbr: "AC", label: "AI Code",        type: "ai"    },
    { abbr: "CO", label: "Code Output",    type: "ai"    },
    { abbr: "PR", label: "PR Review",      type: "human" },
    { abbr: "QA", label: "Testing",        type: "human" },
    { abbr: "FX", label: "Fixes",          type: "human" },
    { abbr: "DP", label: "Deploy",         type: "human" },
    { abbr: "RO", label: "Client Readout", type: "human" },
  ],

  /** Shell slides (no text content) */
  shellSlides: [
    { id: "intro",   order: 1, layout: "cover",   label: "Intro Splash" },
    { id: "landing", order: 2, layout: "nav-hub", label: "Navigation Hub" },
  ],

  /** Content slide skeletons — text merged from content.json by `id` key */
  contentSlides: [
    {
      id: "overview", order: 3, role: "overview", layout: "two-col",
      label: "Case Study Overview", num: "01",
      color: "#67E8F9", colorLight: "#A5F3FC", colorGlow: "rgba(103,232,249,0.24)",
    },
    {
      id: "human", order: 4, role: "evidence", layout: "stat-cards",
      label: "Human in the Loop", num: "02",
      color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)",
    },
    {
      id: "hurdles", order: 5, role: "challenges", layout: "before-after",
      label: "Hurdles We Overcame", num: "03",
      color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)",
    },
    {
      id: "sprint", order: 6, role: "process", layout: "process-cycle",
      label: "AI Sprint Cycle", num: "04",
      color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)",
    },
    {
      id: "future", order: 7, role: "vision", layout: "h-strip",
      label: "Looking Ahead", num: "05",
      color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)",
    },
    {
      id: "platform", order: 8, role: "tools", layout: "process-lanes",
      label: "Service Platform", num: "Optional", optional: true,
      color: "#38BDF8", colorLight: "#7DD3FC", colorGlow: "rgba(56,189,248,0.28)",
    },
  ],
};
