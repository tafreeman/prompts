/**
 * Verge Pop — Structure (layout skeleton).
 * Text content lives in the companion `content.json`.
 */

export const HERO_IMGS = {};

export const structure = {
  themeId: "verge-orange",

  introStatColors: ["#00CC99", "#3399FF", "#FF3366", "#FFD600"],

  sprintNodes: [
    { abbr: "RQ", label: "Research",  type: "human" },
    { abbr: "IN", label: "Insight",   type: "human" },
    { abbr: "AD", label: "AI Draft",  type: "ai"    },
    { abbr: "ED", label: "Editorial", type: "human" },
    { abbr: "CR", label: "Review",    type: "human" },
    { abbr: "PL", label: "Publish",   type: "human" },
  ],

  shellSlides: [
    { id: "intro",   order: 1, layout: "cover",   label: "Cover"  },
    { id: "landing", order: 2, layout: "nav-hub", label: "Hub"    },
  ],

  contentSlides: [
    {
      id: "connection", order: 3, role: "overview",
      layout: "stat-hero",
      label: "Community Connection", num: "01",
      color: "#00CC99",
    },
    {
      id: "niche", order: 4, role: "people",
      layout: "quote-collage",
      label: "Niche Over Scale", num: "02",
      color: "#FF3366",
    },
    {
      id: "platforms", order: 5, role: "data",
      layout: "badge-grid",
      label: "Digital Homes", num: "03",
      color: "#FF6633",
    },
    {
      id: "search", order: 6, role: "evidence",
      layout: "stat-hero",
      label: "AI vs Search", num: "04",
      color: "#FFD600",
    },
    {
      id: "creativity", order: 7, role: "principles",
      layout: "color-blocks",
      label: "AI & Creativity", num: "05",
      color: "#FF3366",
    },
    {
      id: "brands", order: 8, role: "challenges",
      layout: "data-table",
      label: "Brands & Communities", num: "06",
      color: "#00CC99",
    },
    {
      id: "media", order: 9, role: "tools",
      layout: "bar-chart",
      label: "Media Communities", num: "07",
      color: "#3399FF",
    },
    {
      id: "belonging", order: 10, role: "vision",
      layout: "stat-hero",
      label: "Content & Belonging", num: "08",
      color: "#00CC66",
    },
  ],
};
