/**
 * Studio Handbook — AI-assisted creative studio onboarding deck
 *
 * Editorial yellow + black + cream aesthetic inspired by agency onboarding handbooks.
 * Five layout types: hb-chapter, hb-practices, hb-process, hb-manifesto, hb-index.
 */
export const themeId = "studio-craft";

export const sprintNodes = [
  { abbr: "BR", label: "Brief",     type: "human" },
  { abbr: "RS", label: "Research",  type: "human" },
  { abbr: "CO", label: "Concept",   type: "ai"    },
  { abbr: "DE", label: "Design",    type: "ai"    },
  { abbr: "EX", label: "Execute",   type: "ai"    },
  { abbr: "RV", label: "Review",    type: "human" },
  { abbr: "RF", label: "Refine",    type: "human" },
  { abbr: "DL", label: "Deliver",   type: "human" },
];

export const contentSlides = [
  // ── 01 · WHO WE ARE ──────────────────────────────────
  {
    id: "who-we-are",
    order: 1,
    layout: "hb-chapter",
    num: "01",
    title: "Who We Are",
    subtitle: "Big ideas, human taste, AI velocity.",
    color: "#F4E04D",
    colorLight: "#FBF09E",
    colorGlow: "rgba(244,224,77,0.35)",
    icon: "◆",
    eyebrow: "The Studio",
    summary: "We are a creative studio that builds with intelligence. Not a software shop with a design layer, not a design shop that dabbles in code — we are a team that uses AI to expand what is possible at every stage of the process.",
    heroPoints: [
      "AI-native from day one",
      "Creative direction stays human",
      "Output quality is non-negotiable",
      "Craft and speed are not opposites",
    ],
    chapters: [
      { num: "01", title: "Who We Are",    sub: "Big ideas, AI-powered"  },
      { num: "02", title: "What We Build", sub: "Practice areas"         },
      { num: "03", title: "Our Process",   sub: "Brief to delivery"      },
      { num: "04", title: "We Believe",    sub: "Studio manifesto"       },
      { num: "05", title: "Our Clients",   sub: "Who we work with"       },
      { num: "06", title: "Your First Day",sub: "What to expect"         },
    ],
    callout: "We don't use AI to go faster. We use AI to go further.",
  },

  // ── 02 · WHAT WE BUILD ───────────────────────────────
  {
    id: "what-we-build",
    order: 2,
    layout: "hb-practices",
    num: "02",
    title: "What We Build",
    subtitle: "Five practice areas. One integrated team.",
    color: "#0E0E0B",
    colorLight: "#4B4843",
    colorGlow: "rgba(14,14,11,0.2)",
    icon: "▲",
    eyebrow: "Practice Areas",
    summary: "Every engagement touches more than one practice. The best work lives at the intersection of rigorous research, strategic clarity, and craft execution.",
    practices: [
      {
        title: "Research Practice",
        body: "Primary and secondary research, user studies, market analysis, and behavioral synthesis. We find the insight others miss.",
        dark: false,
      },
      {
        title: "Strategy Practice",
        body: "Brand positioning, audience architecture, messaging frameworks, and go-to-market planning. Direction before execution.",
        dark: true,
      },
      {
        title: "Innovation Practice",
        body: "AI-assisted ideation, rapid prototyping, concept sprints, and emerging technology integration. What's next, now.",
        dark: false,
      },
      {
        title: "Branding Practice",
        body: "Visual identity, design systems, typographic standards, and brand governance. The look and feel of an idea.",
        dark: true,
      },
      {
        title: "Creative AI Practice",
        body: "Model-assisted creative direction, prompt engineering for production, AI output curation, and human-AI workflow design.",
        dark: false,
        highlight: true,
      },
    ],
    callout: "Practices are lenses, not silos. Most briefs require three or more to answer properly.",
  },

  // ── 03 · OUR PROCESS ─────────────────────────────────
  {
    id: "our-process",
    order: 3,
    layout: "hb-process",
    num: "03",
    title: "Our Process",
    subtitle: "Eight steps from brief to delivery.",
    color: "#F4E04D",
    colorLight: "#FBF09E",
    colorGlow: "rgba(244,224,77,0.35)",
    icon: "◇",
    eyebrow: "How This Works",
    steps: [
      { num: "01", title: "Intake",     body: "Define the brief, set success criteria, align on timeline and budget." },
      { num: "02", title: "Research",   body: "Understand the context, audience, competitors, and constraints." },
      { num: "03", title: "Strategy",   body: "Frame the problem, define the solution space, establish direction." },
      { num: "04", title: "Concepting", body: "AI-assisted ideation phase — generate, filter, select, elevate." },
      { num: "05", title: "Design",     body: "Translate selected concepts into refined, presentable artifacts." },
      { num: "06", title: "Execution",  body: "Build at production quality with AI tooling and human oversight." },
      { num: "07", title: "Review",     body: "Cross-functional review, client presentation, and feedback integration." },
      { num: "08", title: "Delivery",   body: "Final handoff, documentation, and retrospective." },
    ],
    callout: "The first step of the process is to trust the process.",
  },

  // ── 04 · WE BELIEVE ──────────────────────────────────
  {
    id: "we-believe",
    order: 4,
    layout: "hb-manifesto",
    num: "04",
    title: "We Believe",
    subtitle: "The ideas we hold regardless of brief.",
    color: "#0E0E0B",
    colorLight: "#4B4843",
    colorGlow: "rgba(14,14,11,0.2)",
    icon: "★",
    eyebrow: "Studio Manifesto",
    statement: "Fulfill a Need.\nCreate a Feeling.",
    beliefs: [
      "Good work starts with a good question.",
      "Speed without taste is noise.",
      "Humans set the direction. AI closes the distance.",
      "Constraints are the brief inside the brief.",
      "The best idea should win — regardless of where it came from.",
    ],
    callout: "We measure by the quality of our output, not the hours we logged.",
  },

  // ── 05 · OUR CLIENTS ─────────────────────────────────
  {
    id: "our-clients",
    order: 5,
    layout: "hb-index",
    num: "05",
    title: "Who We Work With",
    subtitle: "The types of clients we do our best work for.",
    color: "#C53B2F",
    colorLight: "#D97065",
    colorGlow: "rgba(197,59,47,0.25)",
    icon: "○",
    eyebrow: "Client Index",
    categories: [
      { label: "Challenger Brands",   body: "Brands that are right but not yet noticed — we help them become unavoidable." },
      { label: "Enterprise at Pivot", body: "Large organizations navigating transformation — we give them clarity and velocity." },
      { label: "Category Creators",   body: "Clients who are defining something new — we help them name, frame, and own the space." },
      { label: "Mission-Driven Orgs", body: "Government, non-profit, and civic entities — we amplify impact without diluting rigor." },
      { label: "AI-Native Ventures",  body: "Teams building with AI at the core — we bring creative craft to technical ambition." },
      { label: "Platform Companies",  body: "Networks and platforms scaling their community — we design for belonging, not just use." },
    ],
    callout: "The best client relationships begin with mutual respect for the brief — and for each other.",
  },

  // ── 06 · YOUR FIRST DAY ──────────────────────────────
  {
    id: "first-day",
    order: 6,
    layout: "hb-chapter",
    num: "06",
    title: "Your First Day",
    subtitle: "What you need to know before week one is over.",
    color: "#F2A614",
    colorLight: "#F7C86E",
    colorGlow: "rgba(242,166,20,0.3)",
    icon: "◉",
    eyebrow: "Getting Started",
    summary: "First week at the studio sets the tone for everything. We move fast, but not carelessly. We have high expectations, but we also have context, support, and a genuine interest in your success here.",
    heroPoints: [
      "Read the handbook before asking — it's written for you",
      "Brief is law — if it's unclear, ask before you assume",
      "AI output is your output — own what you produce",
      "Show work early and often — we critique, not dismiss",
      "Lunch is sacred — we eat together on Tuesdays",
    ],
    chapters: [
      { num: "9:00",  title: "Studio Tour",       sub: "Tools, spaces, rituals"     },
      { num: "10:00", title: "Team Intros",        sub: "Who does what"              },
      { num: "11:00", title: "Active Projects",    sub: "What we're working on"      },
      { num: "13:00", title: "First Brief",        sub: "Jump in immediately"        },
      { num: "15:00", title: "AI Tooling",         sub: "Setup and standards"        },
      { num: "17:00", title: "Day One Retro",      sub: "What worked today"          },
    ],
    callout: "Nobody expects you to know everything on day one. We do expect you to ask.",
  },
];
