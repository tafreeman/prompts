/**
 * Engineering Deck — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const structure = {
  themeId: "arctic-steel",

  introStatColors: ["#60A5FA", "#34D399", "#A78BFA", "#F59E0B"],

  sprintNodes: [
    { abbr: "AD", label: "Architecture", t: 0 },
    { abbr: "CO", label: "Code", t: 0.2 },
    { abbr: "QA", label: "Test", t: 0.4 },
    { abbr: "RV", label: "Review", t: 0.6 },
    { abbr: "DP", label: "Deploy", t: 0.8 },
  ],

  shellSlides: [],

  contentSlides: [
    {
      id: "system-architecture", order: 1, role: "overview", layout: "eng-architecture",
      color: "#60A5FA", colorLight: "#93C5FD", colorGlow: "rgba(96,165,250,0.3)",
      icon: "\u{1F3D7}\uFE0F",
    },
    {
      id: "data-pipeline", order: 2, role: "process", layout: "eng-code-flow",
      color: "#34D399", colorLight: "#6EE7B7", colorGlow: "rgba(52,211,153,0.3)",
      icon: "\u{1F517}",
    },
    {
      id: "tech-evolution", order: 3, role: "evidence", layout: "eng-tech-stack",
      color: "#A78BFA", colorLight: "#C4B5FD", colorGlow: "rgba(167,139,250,0.3)",
      icon: "\u2699\uFE0F",
    },
    {
      id: "implementation-roadmap", order: 4, role: "vision", layout: "eng-roadmap",
      color: "#F59E0B", colorLight: "#FCD34D", colorGlow: "rgba(245,158,11,0.3)",
      icon: "\u{1F5FA}\uFE0F",
    },
  ],
};
