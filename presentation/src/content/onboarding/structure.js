/**
 * Onboarding Deck — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const structure = {
  themeId: "gamma-dark",

  introStatColors: ["#F97316", "#FBBF24", "#22C55E", "#A855F7"],

  sprintNodes: [
    { abbr: "RQ", label: "Requirements", t: 0 },
    { abbr: "PL", label: "Planning", t: 0.17 },
    { abbr: "EX", label: "Execution", t: 0.33 },
    { abbr: "UT", label: "Unit Tests", t: 0.5 },
    { abbr: "E2E", label: "Integration", t: 0.67 },
    { abbr: "RV", label: "Review", t: 0.83 },
  ],

  shellSlides: [],

  contentSlides: [
    {
      id: "expectations", order: 1, role: "overview", layout: "info-cards",
      color: "#F97316", colorLight: "#FB923C", colorGlow: "rgba(249,115,22,0.3)",
      icon: "\uD83D\uDCCB",
    },
    {
      id: "tools", order: 2, role: "tools", layout: "checklist",
      color: "#FBBF24", colorLight: "#FDE68A", colorGlow: "rgba(251,191,36,0.3)",
      icon: "\uD83D\uDEE1\uFE0F",
    },
    {
      id: "devworkflow", order: 3, role: "process", layout: "workflow",
      color: "#A855F7", colorLight: "#C084FC", colorGlow: "rgba(168,85,247,0.3)",
      icon: "\u2699\uFE0F",
    },
    {
      id: "disciplines", order: 4, role: "principles", layout: "pillars",
      color: "#14B8A6", colorLight: "#5EEAD4", colorGlow: "rgba(20,184,166,0.3)",
      icon: "\uD83D\uDD2C",
    },
    {
      id: "qa", order: 5, role: "evidence", layout: "info-cards",
      color: "#EC4899", colorLight: "#F472B6", colorGlow: "rgba(236,72,153,0.3)",
      icon: "\uD83E\uDDEA",
    },
    {
      id: "functional", order: 6, role: "people", layout: "checklist",
      color: "#06B6D4", colorLight: "#22D3EE", colorGlow: "rgba(6,182,212,0.3)",
      icon: "\uD83D\uDCCA",
    },
    {
      id: "compliance", order: 7, role: "compliance", layout: "catalog",
      color: "#EF4444", colorLight: "#F87171", colorGlow: "rgba(239,68,68,0.3)",
      icon: "\uD83D\uDD10",
    },
  ],
};
