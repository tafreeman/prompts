/**
 * Reference deck sample — Signal Cobalt
 *
 * Image-derived direction from the deck.gallery Swiss / systems reference.
 * Export shape mirrors src/content/genai-advocacy/deck.js so renderers and export
 * scripts can consume the same manifest contract.
 */

export const themeId = "signal-cobalt";

export const HERO_IMGS = {
  dataGrid: "images/data-grid.jpg",
  systemsPhoto: "images/systems-photo.jpg",
};

export const sprintNodes = [
  { abbr: "IN", label: "Input", type: "human" },
  { abbr: "CL", label: "Classify", type: "ai" },
  { abbr: "TG", label: "Tag", type: "ai" },
  { abbr: "RV", label: "Review", type: "human" },
  { abbr: "PL", label: "Plot", type: "ai" },
  { abbr: "PX", label: "Publish", type: "human" },
];

export const slides = [
  { id: "intro", order: 1, layout: "cover", label: "Signal Cover" },
  { id: "landing", order: 2, layout: "nav-hub", label: "Signal Hub" },
  {
    id: "introduction",
    order: 3,
    layout: "two-col",
    label: "Introduction",
    num: "01",
    title: "Introduction",
    subtitle: "A modernist system with stark contrast, electric color blocks, and disciplined grid rules",
    eyebrow: "Reference Story",
    summary: "This sample reflects the second reference image: black/white foundations, cobalt stage panels, orange highlight accents, and clean diagrammatic pacing.",
    heroPoints: ["Swiss framing", "Black/white base", "Cobalt stage slides", "Orange utility accents"],
    color: "#1328FF",
    colorLight: "#5063FF",
    colorGlow: "rgba(19,40,255,0.16)",
    cards: [
      { title: "Hard Contrast", body: "Keep surfaces mostly white or black and reserve cobalt for interruption slides and callout blocks." },
      { title: "Utility Orange", body: "Orange should mark emphasis, data thresholds, and directional hints — never the whole composition." },
      { title: "Grid Discipline", body: "Columns, labels, and captions should align precisely; visual looseness breaks the style immediately." },
      { title: "Systemic Tone", body: "The deck sounds analytical and declarative rather than lyrical or narrative-heavy." },
    ],
    talkingPoints: [
      "Use one strong interruption color per spread.",
      "Treat headings as labels inside a system, not decorative typography.",
      "Favor thin rules and modular blocks over shadows and glow.",
      "Let diagrams and data marks feel engineered.",
    ],
    callout: "The deck works because the system is stricter than the content.",
  },
  {
    id: "color-system",
    order: 4,
    layout: "stat-cards",
    label: "Color",
    num: "02",
    title: "Color",
    subtitle: "Primary palette notes for the Swiss-modern reference",
    color: "#1328FF",
    colorLight: "#5063FF",
    colorGlow: "rgba(19,40,255,0.16)",
    cards: [
      { title: "Cobalt", body: "Use for interruption slides, key labels, and big stage-setting moments.", stat: "#1328FF", statLabel: "Primary" },
      { title: "Orange", body: "Use sparingly for warnings, active data points, and directional emphasis.", stat: "#FF6A13", statLabel: "Utility" },
      { title: "Black", body: "Ground information-dense spreads with black panels when you want maximum authority.", stat: "#121212", statLabel: "Base" },
    ],
    callout: "If every slide is loud, none of them are. Save cobalt for impact.",
  },
  {
    id: "type-rules",
    order: 5,
    layout: "before-after",
    label: "Type Rules",
    num: "03",
    title: "Type Rules",
    subtitle: "Before/after guidance for keeping the visual language crisp",
    color: "#FF6A13",
    colorLight: "#FF9A5C",
    colorGlow: "rgba(255,106,19,0.18)",
    cards: [
      { title: "Headlines", challenge: "Loose editorial copy and soft hierarchy weaken the system feel.", fix: "Use compact, declarative headings with clear rank and strong margins." },
      { title: "Captions", challenge: "Floating annotations become visual clutter when they ignore the grid.", fix: "Align every caption, kicker, and note to the modular column structure." },
      { title: "Data Labels", challenge: "Decorative colors can make charts feel playful instead of precise.", fix: "Use black, gray, cobalt, and one accent orange with disciplined repetition." },
      { title: "Rhythm", challenge: "Equal-weight sections flatten the presentation.", fix: "Alternate quiet white slides with high-contrast interruption spreads." },
    ],
    callout: "This style is less about flair and more about compositional law.",
  },
  {
    id: "system-flow",
    order: 6,
    layout: "process-cycle",
    label: "System Flow",
    num: "04",
    title: "System Flow",
    subtitle: "A compact process sample for charts, maps, and diagram-driven pages",
    color: "#1328FF",
    colorLight: "#5063FF",
    colorGlow: "rgba(19,40,255,0.16)",
    callout: "Charts should feel like parts of the operating system, not pasted-in widgets.",
  },
  {
    id: "data-story",
    order: 7,
    layout: "h-strip",
    label: "Data Story",
    num: "05",
    title: "Data Story",
    subtitle: "Sample narrative blocks for turning metrics into a gallery-style systems deck",
    color: "#121212",
    colorLight: "#404040",
    colorGlow: "rgba(18,18,18,0.10)",
    cards: [
      { title: "Frame", body: "Start with one declarative black slide that names the thesis plainly." },
      { title: "Interrupt", body: "Use a cobalt spread to mark the section break or introduction moment." },
      { title: "Evidence", body: "Follow with white slides carrying tables, charts, or type specimens." },
      { title: "Resolve", body: "Close with an orange-accent sentence or summary line that feels earned." },
    ],
    callout: "Think sequence first: black, cobalt, white, white, accent.",
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
