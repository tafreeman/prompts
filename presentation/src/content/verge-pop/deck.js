/**
 * Verge Pop — Community & Digital Trends Deck
 *
 * Pop-art editorial data stories about digital communities, platform
 * fragmentation, AI and creativity. Uses the new Verge-family layouts:
 *   stat-hero, quote-collage, badge-grid, data-table, bar-chart, color-blocks
 */

export const themeId = "verge-orange";

export const HERO_IMGS = {};

export const sprintNodes = [
  { abbr: "RQ", label: "Research",  type: "human" },
  { abbr: "IN", label: "Insight",   type: "human" },
  { abbr: "AD", label: "AI Draft",  type: "ai"    },
  { abbr: "ED", label: "Editorial", type: "human" },
  { abbr: "CR", label: "Review",    type: "human" },
  { abbr: "PL", label: "Publish",   type: "human" },
];

export const slides = [
  { id: "intro",   order: 1, layout: "cover",   label: "Cover"  },
  { id: "landing", order: 2, layout: "nav-hub", label: "Hub"    },

  // ── 01 — stat-hero ────────────────────────────────────────────────────
  {
    id: "connection",
    order: 3,
    layout: "stat-hero",
    label: "Community Connection",
    num: "01",
    title: "Small, interactive, and content unlocks community",
    subtitle: "People juggle seven different groups: two online, two IRL, three that mix both.",
    question: "If you had to choose, which makes you feel more connected to others around you?",
    color: "#00CC99",
    statItems: [
      {
        val: "91%", label: "SMALL", bgColor: "#00CC99",
        bullets: [
          "Connecting with a small group of friends / family in-person",
          "Direct messaging or chatting",
          "Participating in a small online group / club / community",
        ],
      },
      {
        val: "91%", label: "GROUP", bgColor: "#FFD600",
        bullets: [
          "Casual interactions in public spaces",
          "Online gaming with others",
          "Attending a meetup with 100 + people",
        ],
      },
      {
        val: "78%", label: "CONTENT", bgColor: "#3399FF",
        bullets: [
          "Creating and sharing content",
          "Scrolling through social media feeds",
          "Listening to podcasts or audiobooks",
        ],
      },
    ],
    callout: "Small, interactive, and content-driven groups are the dominant community pattern.",
  },

  // ── 02 — quote-collage ────────────────────────────────────────────────
  {
    id: "niche",
    order: 4,
    layout: "quote-collage",
    label: "Niche Over Scale",
    num: "02",
    title: "NICHE over scale = meaning",
    subtitle: "We asked people about their most important online group. Some led with the platform, while others focused on what unites them.",
    centerLabel: "COMMUNITIES AROUND SHARED INTERESTS",
    color: "#FF3366",
    quotes: [
      { text: "I follow an Outlander group on Reddit that I really enjoy.", bgColor: "#FFD600" },
      { text: "Addicting vibes on Discord — I've found people who understand what I'm going through.", bgColor: "#FF3366" },
      { text: "A K-pop group on Discord that discusses the topic in depth.", bgColor: "#FF3366" },
      { text: "My Swiftie FB groups.", bgColor: "#00CC99" },
      { text: "Reddit — it shows me that other people have it worse or the same, and I find support.", bgColor: "#FFD600" },
      { text: "Goth crochet for the spookies.", bgColor: "#FF6633" },
      { text: "Faith Family Church because it helps me grow spiritually.", bgColor: "#00CC99" },
      { text: "South Florida saltwater fishing.", bgColor: "#FFD600" },
      { text: "I'm part of an online knitting club. It's really fun and interactive.", bgColor: "#3399FF" },
    ],
    callout: "The platform matters less than the shared interest that binds the community.",
  },

  // ── 03 — badge-grid ───────────────────────────────────────────────────
  {
    id: "platforms",
    order: 5,
    layout: "badge-grid",
    label: "Digital Homes",
    num: "03",
    title: "As we splinter, small platforms become \"digital homes\"",
    subtitle: "",
    question: "Which of the following online spaces do you feel connected..?",
    color: "#FF6633",
    badges: [
      { icon: "🌐", name: "FEDIVERSE",   value: "43%", bgColor: "#FF3366" },
      { icon: "🐘", name: "MASTODON",    value: "32%", bgColor: "#FF6633" },
      { icon: "👻", name: "SNAPCHAT",    value: "29%", bgColor: "#FFD600" },
      { icon: "💼", name: "LINKEDIN",    value: "22%", bgColor: "#3399FF" },
      { icon: "📱", name: "WHATSAPP",    value: "37%", bgColor: "#00CC66" },
      { icon: "📷", name: "INSTAGRAM",   value: "32%", bgColor: "#FF3366" },
      { icon: "🎨", name: "PATREON",     value: "29%", bgColor: "#FF6633" },
      { icon: "📰", name: "NEWS APPS",   value: "21%", bgColor: "#3399FF" },
      { icon: "📝", name: "SUBSTACK",    value: "37%", bgColor: "#00CC66" },
      { icon: "✖️",  name: "X (TWITTER)", value: "31%", bgColor: "#000000" },
      { icon: "🧵", name: "THREADS",     value: "26%", bgColor: "#FFD600" },
      { icon: "👽", name: "REDDIT",      value: "20%", bgColor: "#FF6633" },
      { icon: "▶️",  name: "YOUTUBE",     value: "34%", bgColor: "#FF3366" },
      { icon: "🎵", name: "TIKTOK",      value: "30%", bgColor: "#000000" },
      { icon: "💬", name: "SLACK",       value: "25%", bgColor: "#3399FF" },
      { icon: "🌍", name: "MEDIA SITES", value: "18%", bgColor: "#00CC66" },
      { icon: "📘", name: "FACEBOOK",    value: "33%", bgColor: "#3399FF" },
      { icon: "🎮", name: "DISCORD",     value: "29%", bgColor: "#7C3AED" },
      { icon: "❓", name: "QUORA",       value: "23%", bgColor: "#FF3366" },
    ],
    callout: "Platform fragmentation is accelerating — people are spreading across more spaces than ever.",
  },

  // ── 04 — stat-hero ────────────────────────────────────────────────────
  {
    id: "search",
    order: 6,
    layout: "stat-hero",
    label: "AI vs Search",
    num: "04",
    title: "A real challenger to Google",
    subtitle: "",
    color: "#FFD600",
    statItems: [
      {
        val: "76%", label: "SPONSORED", bgColor: "#FFD600",
        bullets: [
          "stated that more than 1/4 of their Google Search results when shopping appear to be sponsored or promoted",
          "only 14% describe these sponsored or promoted results as \"very helpful\"",
        ],
      },
      {
        val: "61%", label: "AI SEARCH", bgColor: "#FF6633",
        bullets: [
          "of Gen Z and 53% of Millennials reported that they are using AI tools in place of search engines to find information about a topic",
        ],
      },
    ],
    callout: "AI tools are becoming the new front door for information discovery.",
  },

  // ── 05 — color-blocks ─────────────────────────────────────────────────
  {
    id: "creativity",
    order: 7,
    layout: "color-blocks",
    label: "AI & Creativity",
    num: "05",
    title: "Creating vs. Being Creative",
    subtitle: "",
    color: "#FF3366",
    blocks: [
      {
        area: "left", bgColor: "#FF3366",
        stat: { val: "55%", label: "think that AI will never impede human creativity" },
      },
      {
        area: "top-right", bgColor: "#FFF5E6",
        text: "The more \"artistic\" the endeavor, the less we want AI in the creative process.",
      },
      {
        area: "bottom-right", bgColor: "#FFD600",
        chartBars: [
          { label: "Poetry",         peopleOnly: 95, mixed: 3,  aiOnly: 2  },
          { label: "Literature",     peopleOnly: 90, mixed: 7,  aiOnly: 3  },
          { label: "Music",          peopleOnly: 85, mixed: 10, aiOnly: 5  },
          { label: "Art",            peopleOnly: 80, mixed: 12, aiOnly: 8  },
          { label: "Recipes",        peopleOnly: 70, mixed: 20, aiOnly: 10 },
          { label: "Fashion",        peopleOnly: 60, mixed: 25, aiOnly: 15 },
          { label: "Photography",    peopleOnly: 55, mixed: 28, aiOnly: 17 },
          { label: "Architecture",   peopleOnly: 50, mixed: 30, aiOnly: 20 },
          { label: "Digital Design", peopleOnly: 30, mixed: 35, aiOnly: 35 },
          { label: "Animation",      peopleOnly: 25, mixed: 35, aiOnly: 40 },
        ],
      },
    ],
    callout: "People draw a clear line between artistic expression and functional creation.",
  },

  // ── 06 — data-table ───────────────────────────────────────────────────
  {
    id: "brands",
    order: 8,
    layout: "data-table",
    label: "Brands & Communities",
    num: "06",
    title: "Ultimately, brands are expected to join communities",
    subtitle: "",
    color: "#00CC99",
    tableTitle: "Brand Engagements",
    tableHeaders: ["", "Total", "Gen Z", "Mill", "Gen X", "Boom"],
    headerColors: ["transparent", "#FF3366", "#FFD600", "#FF6633", "#3399FF", "#00CC66"],
    tableRows: [
      ["Engaging and collaborating in the community", "79%", "79%", "81%", "75%", "75%"],
      ["Providing products or services",              "72%", "70%", "69%", "76%", "76%"],
      ["Contributing content",                        "70%", "68%", "70%", "68%", "73%"],
      ["Offering exclusive benefits or events",        "67%", "66%", "68%", "68%", "65%"],
      ["Sponsoring the community with funds",          "64%", "69%", "67%", "63%", "54%"],
    ],
    callout: "Brands are expected to participate, not just advertise.",
  },

  // ── 07 — bar-chart ────────────────────────────────────────────────────
  {
    id: "media",
    order: 9,
    layout: "bar-chart",
    label: "Media Communities",
    num: "07",
    title: "Major media brands are places of community",
    subtitle: "",
    color: "#3399FF",
    barGroups: [
      {
        groupLabel: "PLATFORMS",
        color: "#FF6633",
        bars: [
          { label: "Facebook Groups",  value: 75 },
          { label: "Reddit",           value: 65 },
          { label: "YouTube channels", value: 60 },
          { label: "Discord",          value: 57 },
          { label: "TikTok",           value: 55 },
          { label: "Instagram",        value: 50 },
        ],
      },
      {
        groupLabel: "MEDIA",
        color: "#00CC66",
        bars: [
          { label: "Online Learning",     value: 85 },
          { label: "Blogger Groups",      value: 70 },
          { label: "MasterClasses",       value: 65 },
          { label: "Specialized Forums",  value: 60 },
          { label: "Major Media Brands",  value: 55 },
        ],
      },
    ],
    callout: "Media brands compete with social platforms as community hubs.",
  },

  // ── 08 — stat-hero ────────────────────────────────────────────────────
  {
    id: "belonging",
    order: 10,
    layout: "stat-hero",
    label: "Content & Belonging",
    num: "08",
    title: "While community needs belonging, content is critical",
    subtitle: "",
    question: "What are the top criteria for what makes a great community?",
    color: "#00CC66",
    statItems: [
      {
        val: "78%", label: "HIGH QUALITY CONTENT", bgColor: "#00CC66",
        bullets: [
          "Quality content relevant to my interests",
          "Effective moderation and leadership",
          "Active member participation in the group",
          "Diverse perspectives and contributions",
        ],
      },
      {
        val: "90%", label: "BELONGING & ENGAGEMENT", bgColor: "#3399FF",
        bullets: [
          "Supportive and empathetic community atmosphere",
          "Have shared values",
          "People engage one-on-one with each other",
          "Strong sense of belonging",
        ],
      },
    ],
    callout: "Quality content and genuine belonging are the twin pillars of community.",
  },
];

export const contentSlides = slides
  .filter((s) => s.layout !== "cover" && s.layout !== "nav-hub")
  .sort((a, b) => a.order - b.order);

export const SLIDES = slides
  .slice()
  .sort((a, b) => a.order - b.order)
  .map(({ id, label }) => ({ id, label }));

export default slides;
