/**
 * Atelier Sage — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const HERO_IMGS = {
  atelierBoard: "images/atelier-board.jpg",
  editorialWall: "images/editorial-wall.jpg",
};

export const structure = {
  themeId: "atelier-sage",

  introStatColors: ["#557868", "#D7AA58", "#C87052", "#7F9A8C"],

  sprintNodes: [
    { abbr: "BR", label: "Brief", type: "human" },
    { abbr: "IN", label: "Insight", type: "human" },
    { abbr: "FR", label: "Frames", type: "ai" },
    { abbr: "ED", label: "Edit", type: "human" },
    { abbr: "RF", label: "Refine", type: "human" },
    { abbr: "ST", label: "Story", type: "ai" },
    { abbr: "CR", label: "Critique", type: "human" },
    { abbr: "AP", label: "Approve", type: "human" },
  ],

  shellSlides: [
    { id: "intro", order: 1, layout: "cover", label: "Atelier Cover" },
    { id: "landing", order: 2, layout: "nav-hub", label: "Atelier Hub" },
  ],

  contentSlides: [
    {
      id: "overview", order: 3, role: "overview", layout: "two-col",
      label: "What Is a Brand Ecosystem?", num: "01",
      color: "#557868", colorLight: "#7F9A8C", colorGlow: "rgba(85,120,104,0.18)",
    },
    {
      id: "process", order: 4, role: "process", layout: "process-cycle",
      label: "The Process", num: "02",
      color: "#557868", colorLight: "#7F9A8C", colorGlow: "rgba(85,120,104,0.18)",
    },
    {
      id: "works", order: 5, role: "evidence", layout: "stat-cards",
      label: "How This Works", num: "03",
      color: "#D7AA58", colorLight: "#E5C787", colorGlow: "rgba(215,170,88,0.20)",
    },
    {
      id: "language", order: 6, role: "principles", layout: "h-strip",
      label: "Language Bank", num: "04",
      color: "#C87052", colorLight: "#D98C72", colorGlow: "rgba(200,112,82,0.20)",
    },
  ],
};
