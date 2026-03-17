/**
 * Signal Cobalt — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const HERO_IMGS = {
  dataGrid: "images/data-grid.jpg",
  systemsPhoto: "images/systems-photo.jpg",
};

export const structure = {
  themeId: "signal-cobalt",

  introStatColors: ["#1328FF", "#FF6A13", "#121212", "#5063FF"],

  sprintNodes: [
    { abbr: "IN", label: "Input", type: "human" },
    { abbr: "CL", label: "Classify", type: "ai" },
    { abbr: "TG", label: "Tag", type: "ai" },
    { abbr: "RV", label: "Review", type: "human" },
    { abbr: "PL", label: "Plot", type: "ai" },
    { abbr: "PX", label: "Publish", type: "human" },
  ],

  shellSlides: [
    { id: "intro", order: 1, layout: "cover", label: "Signal Cover" },
    { id: "landing", order: 2, layout: "nav-hub", label: "Signal Hub" },
  ],

  contentSlides: [
    {
      id: "introduction", order: 3, role: "overview", layout: "two-col",
      label: "Introduction", num: "01",
      color: "#1328FF", colorLight: "#5063FF", colorGlow: "rgba(19,40,255,0.16)",
    },
    {
      id: "color-system", order: 4, role: "evidence", layout: "stat-cards",
      label: "Color", num: "02",
      color: "#1328FF", colorLight: "#5063FF", colorGlow: "rgba(19,40,255,0.16)",
    },
    {
      id: "type-rules", order: 5, role: "challenges", layout: "before-after",
      label: "Type Rules", num: "03",
      color: "#FF6A13", colorLight: "#FF9A5C", colorGlow: "rgba(255,106,19,0.18)",
    },
    {
      id: "system-flow", order: 6, role: "process", layout: "process-cycle",
      label: "System Flow", num: "04",
      color: "#1328FF", colorLight: "#5063FF", colorGlow: "rgba(19,40,255,0.16)",
    },
    {
      id: "data-story", order: 7, role: "vision", layout: "h-strip",
      label: "Data Story", num: "05",
      color: "#121212", colorLight: "#404040", colorGlow: "rgba(18,18,18,0.10)",
    },
  ],
};
