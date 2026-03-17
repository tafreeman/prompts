/**
 * Studio Handbook — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const structure = {
  themeId: "studio-craft",

  introStatColors: ["#F4E04D", "#F2A614", "#C53B2F", "#0E0E0B"],

  sprintNodes: [
    { abbr: "BR", label: "Brief",     type: "human" },
    { abbr: "RS", label: "Research",  type: "human" },
    { abbr: "CO", label: "Concept",   type: "ai"    },
    { abbr: "DE", label: "Design",    type: "ai"    },
    { abbr: "EX", label: "Execute",   type: "ai"    },
    { abbr: "RV", label: "Review",    type: "human" },
    { abbr: "RF", label: "Refine",    type: "human" },
    { abbr: "DL", label: "Deliver",   type: "human" },
  ],

  shellSlides: [],

  contentSlides: [
    {
      id: "who-we-are", order: 1, role: "overview",
      layout: "hb-chapter",
      num: "01", icon: "\u25C6",
      color: "#F4E04D", colorLight: "#FBF09E", colorGlow: "rgba(244,224,77,0.35)",
    },
    {
      id: "what-we-build", order: 2, role: "principles",
      layout: "hb-practices",
      num: "02", icon: "\u25B2",
      color: "#0E0E0B", colorLight: "#4B4843", colorGlow: "rgba(14,14,11,0.2)",
    },
    {
      id: "our-process", order: 3, role: "process",
      layout: "hb-process",
      num: "03", icon: "\u25C7",
      color: "#F4E04D", colorLight: "#FBF09E", colorGlow: "rgba(244,224,77,0.35)",
    },
    {
      id: "we-believe", order: 4, role: "vision",
      layout: "hb-manifesto",
      num: "04", icon: "\u2605",
      color: "#0E0E0B", colorLight: "#4B4843", colorGlow: "rgba(14,14,11,0.2)",
    },
    {
      id: "our-clients", order: 5, role: "people",
      layout: "hb-index",
      num: "05", icon: "\u25CB",
      color: "#C53B2F", colorLight: "#D97065", colorGlow: "rgba(197,59,47,0.25)",
    },
    {
      id: "first-day", order: 6, role: "tools",
      layout: "hb-chapter",
      num: "06", icon: "\u25C9",
      color: "#F2A614", colorLight: "#F7C86E", colorGlow: "rgba(242,166,20,0.3)",
    },
  ],
};
