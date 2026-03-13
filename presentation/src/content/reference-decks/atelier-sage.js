/**
 * Reference deck sample — Atelier Sage
 *
 * Image-derived direction from the deck.gallery editorial/process reference.
 * Export shape mirrors src/content/genai-advocacy/deck.js so renderers and export
 * scripts can consume the same manifest contract.
 */

export const themeId = "atelier-sage";

export const HERO_IMGS = {
  atelierBoard: "images/atelier-board.jpg",
  editorialWall: "images/editorial-wall.jpg",
};

export const sprintNodes = [
  { abbr: "BR", label: "Brief", type: "human" },
  { abbr: "IN", label: "Insight", type: "human" },
  { abbr: "FR", label: "Frames", type: "ai" },
  { abbr: "ED", label: "Edit", type: "human" },
  { abbr: "RF", label: "Refine", type: "human" },
  { abbr: "ST", label: "Story", type: "ai" },
  { abbr: "CR", label: "Critique", type: "human" },
  { abbr: "AP", label: "Approve", type: "human" },
];

export const slides = [
  { id: "intro", order: 1, layout: "cover", label: "Atelier Cover" },
  { id: "landing", order: 2, layout: "nav-hub", label: "Atelier Hub" },
  {
    id: "overview",
    order: 3,
    layout: "two-col",
    label: "What Is a Brand Ecosystem?",
    num: "01",
    title: "What Is a Brand Ecosystem?",
    subtitle: "An airy editorial framing of process, voice, and visual cues",
    eyebrow: "Reference Story",
    summary: "This sample mirrors the spacious editorial deck style: restrained palette, poetic headings, compact body copy, and one image-led focal block per slide.",
    heroPoints: ["Whitespaced composition", "Soft sage primary", "Ochre/terracotta support", "Editorial sequencing"],
    color: "#557868",
    colorLight: "#7F9A8C",
    colorGlow: "rgba(85,120,104,0.18)",
    cards: [
      { title: "Quiet Surface", body: "Warm paper backgrounds and thin rules let typography do most of the work." },
      { title: "Measured Accent", body: "Sage carries primary emphasis while ochre and terracotta act as small punctuation marks." },
      { title: "Image Anchor", body: "Each spread needs one visual block that stabilizes the page and stops the layout from floating away." },
      { title: "Process Language", body: "Headings sound like chapters, not dashboards: How This Works, Step 8, The Process." },
    ],
    talkingPoints: [
      "Lead with atmosphere before detail.",
      "Keep dense copy inside one bounded column.",
      "Use accent color in short bars, labels, and numerals rather than large fills.",
      "Let the serif headline carry the personality.",
    ],
    callout: "The deck feels curated because color is quiet and hierarchy does the talking.",
  },
  {
    id: "process",
    order: 4,
    layout: "process-cycle",
    label: "The Process",
    num: "02",
    title: "The Process",
    subtitle: "A gentle, chapter-like flow from brief to approval",
    color: "#557868",
    colorLight: "#7F9A8C",
    colorGlow: "rgba(85,120,104,0.18)",
    callout: "This cycle should read like an editorial spread first and an operating model second.",
  },
  {
    id: "works",
    order: 5,
    layout: "stat-cards",
    label: "How This Works",
    num: "03",
    title: "How This Works",
    subtitle: "A sample content slide with one large image block and three compact proof cards",
    color: "#D7AA58",
    colorLight: "#E5C787",
    colorGlow: "rgba(215,170,88,0.20)",
    cards: [
      { title: "Step 1", body: "Set the premise with a short editorial intro rather than a technical explainer.", stat: "01", statLabel: "Premise" },
      { title: "Step 2", body: "Use an anchored photo or collage to carry texture and credibility.", stat: "02", statLabel: "Anchor" },
      { title: "Step 3", body: "Resolve with a confident sentence in the accent color family.", stat: "03", statLabel: "Resolve" },
    ],
    callout: "The image should feel placed, not decorated — it is the counterweight to the typography.",
  },
  {
    id: "language",
    order: 6,
    layout: "h-strip",
    label: "Language Bank",
    num: "04",
    title: "Language Bank",
    subtitle: "Suggested phrases to keep the deck in the same editorial register",
    color: "#C87052",
    colorLight: "#D98C72",
    colorGlow: "rgba(200,112,82,0.20)",
    cards: [
      { title: "Section Titles", body: "The Process, How This Works, Step 8, Presentation." },
      { title: "Support Phrases", body: "Guided sequence, editorial pacing, restrained accent, image-led spread." },
      { title: "Callout Style", body: "Short, quotable, and warm — more magazine than product sheet." },
      { title: "Numeral System", body: "Use numbered chapters as visual anchors: 01, 02, 03…" },
    ],
    callout: "Use language with rhythm. The tone is composed, not hyped.",
  },
];

export const contentSlides = slides
  .filter((slide) => slide.layout !== "cover" && slide.layout !== "nav-hub")
  .sort((a, b) => a.order - b.order);

export const SLIDES = slides
  .slice()
  .sort((a, b) => a.order - b.order)
  .map(({ id, label }) => ({ id, label }));

export default slides;
