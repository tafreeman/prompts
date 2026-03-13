/**
 * GenAI Advocacy Hub — Deck Manifest
 *
 * Content source of truth for the presentation. Each slide entry carries:
 *   - `id`     — stable slug (matches DOM data-slide-id and URL hash)
 *   - `order`  — explicit numeric position (1-based); drives nav ordering
 *   - `layout` — discriminator that selects the layout renderer component
 *                (matches the Slidev convention: one string → one renderer)
 *
 * Layout registry (see src/components/layouts/LayoutRegistry.js):
 *   "cover"         → intro/title splash
 *   "nav-hub"       → landing tile grid
 *   "two-col"       → heading + 2-column card grid (overview)
 *   "stat-cards"    → expandable cards + KPI results row (human)
 *   "before-after"  → challenge/fix card pairs (hurdles)
 *   "process-cycle" → Figure8 or ring sprint diagram (sprint)
 *   "h-strip"       → 1×N horizontal card strip (future)
 *   "process-lanes" → swimlane with capabilities + focusPanels (platform)
 */

// ─── HERO IMAGE REFS ───
export const HERO_IMGS = {
  carrierFleet:     "images/carrier-fleet.jpg",
  helicopterRappel: "images/helicopter-rappel.jpg",
  droneDeck:        "images/drone-deck.jpg",
  carrierOps:       "images/carrier-ops.jpg",
  uavSunset:        "images/uav-sunset.jpg",
};

// ─── SPRINT NODES ───
// SVG icon key (abbr) maps to SPRINT_ICONS in the rendering layer.
// type: "human" | "ai" — drives colour coding on the sprint diagram.
export const sprintNodes = [
  { abbr: "RQ", label: "Requirements",  type: "human" },
  { abbr: "UI", label: "UI Mockup",     type: "human" },
  { abbr: "AD", label: "AI AC Draft",   type: "ai"    },
  { abbr: "RF", label: "AC Refine",     type: "human" },
  { abbr: "RV", label: "Human Review",  type: "human" },
  { abbr: "AC", label: "AI Code",       type: "ai"    },
  { abbr: "CO", label: "Code Output",   type: "ai"    },
  { abbr: "PR", label: "PR Review",     type: "human" },
  { abbr: "QA", label: "Testing",       type: "human" },
  { abbr: "FX", label: "Fixes",         type: "human" },
  { abbr: "DP", label: "Deploy",        type: "human" },
  { abbr: "RO", label: "Client Readout",type: "human" },
];

// ─── SLIDES ───
export const slides = [
  // ── Shell slides (no content body) ────────────────────────────────────
  {
    id: "intro",
    order: 1,
    layout: "cover",
    label: "Intro Splash",
  },
  {
    id: "landing",
    order: 2,
    layout: "nav-hub",
    label: "Navigation Hub",
  },

  // ── Content slides ─────────────────────────────────────────────────────
  {
    id: "overview",
    order: 3,
    layout: "two-col",
    label: "Case Study Overview",
    num: "01",
    title: "Case Study Overview",
    subtitle: "How the AI-accelerated delivery story unfolds across governance, execution, and scale",
    color: "#67E8F9", colorLight: "#A5F3FC", colorGlow: "rgba(103,232,249,0.24)",
    eyebrow: "Deck Flow",
    summary: "This opener gives the audience the full story in one pass: the mission need, the platform model, the governance proof points, and the path to scale.",
    heroPoints: ["Mission need", "Platform model", "Delivery guardrails", "Scale path"],
    cards: [
      { title: "Mission Need",      body: "The agency needed one front door for fragmented IT demand." },
      { title: "Operating Model",   body: "The platform links discovery, approval, and procurement handoff." },
      { title: "Human Governance",  body: "Speed stayed credible because humans still owned review and release." },
      { title: "What Follows",      body: "The next pages prove governance, execution, and scale in detail." },
    ],
    talkingPoints: [
      "Lead with the mission problem before the technology.",
      "Frame the platform as an operating model, not a catalog screen.",
      "Use the rest of the deck as proof of governance and execution.",
      "Keep the throughline on readiness, speed, and controlled handoff.",
    ],
    callout: "Use this slide as the executive opener, then move into the proof pages.",
  },
  {
    id: "human",
    order: 4,
    layout: "stat-cards",
    label: "Human in the Loop",
    num: "02",
    title: "Human in the Loop",
    heroTitle: "Human-in-the-Loop Focused AI Development",
    kicker: "AI-Accelerated Delivery",
    subkicker: "Governance-First Delivery",
    subtitle: "AI accelerates delivery. Human judgment governs quality.",
    thesis: "Accelerated by AI. Governed by human expertise.",
    color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)",
    cards: [
      {
        title: "Governance First", step: "01", marker: "GF",
        eyebrow: "Approvals before acceleration",
        highlight: "Approvals and legal clearance came before acceleration.",
        details: [
          "Risk, legal, and compliance teams approved AI use before production release.",
          "Contract updates included explicit AI language and operating guardrails.",
        ],
      },
      {
        title: "Quality Gates", step: "02", marker: "QG",
        eyebrow: "Human review at every gate",
        highlight: "Every AI-assisted line was reviewed before merge.",
        details: [
          "More time was invested in review discipline, not less.",
          "Unit and integration testing validated output before release.",
          "No merge moved forward until all gates passed.",
        ],
      },
      {
        title: "Context Engineering", step: "03", marker: "PC",
        eyebrow: "Manage context, lower variance",
        highlight: "Standardized prompts, process learning sessions, and developer expertise provided the system the full context.",
        details: [
          "Architecture docs, data models, and coding standards were embedded in prompts.",
          "Variance dropped because outputs stayed anchored to the real system.",
        ],
      },
    ],
    leadershipPoints: [
      "Governance sat inside the workflow, not after the fact.",
      "Humans kept release authority even when AI authored most of the implementation.",
      "Review rigor made speed credible to leadership.",
    ],
    results: [
      { value: "50%", label: "Reduction in development time", detail: "through incorporation of AI tools in development processes" },
      { value: "90%", label: "Of production code developed via AI" },
      { value: "2",   label: "Months from idea to production" },
      { value: "0",   label: "Critical defects discovered post deployment" },
    ],
    enablementTitle: "Enablement + Outcome",
    enablement: "An internal hackathon built team fluency and confidence, turning experimentation into a repeatable delivery habit.",
    callout: "AI generated code. Humans owned the decisions.",
  },
  {
    id: "hurdles",
    order: 5,
    layout: "before-after",
    label: "Hurdles We Overcame",
    num: "03",
    title: "Hurdles We Overcame",
    subtitle: "What changed from day one to delivery",
    color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)",
    cards: [
      { title: "Prompt Standardization", challenge: "Ad-hoc prompts created uneven quality and rework.",            fix: "Versioned prompt templates added consistent architecture context." },
      { title: "Process Realignment",    challenge: "Traditional reviews were not built for AI-assisted output.",    fix: "AI-specific review checklists made quality gates explicit." },
      { title: "Governance Clearance",   challenge: "Policy approval was required before production use.",           fix: "Risk and legal teams were engaged early to set guardrails." },
      { title: "Team Enablement",        challenge: "Skill levels with AI tools were uneven across the team.",       fix: "A hands-on hackathon built shared confidence before delivery." },
    ],
    callout: "The early friction became the guardrails that let the team move fast later.",
  },
  {
    id: "sprint",
    order: 6,
    layout: "process-cycle",
    label: "AI Sprint Cycle",
    num: "04",
    title: "AI Sprint Cycle",
    subtitle: "Human checkpoints at every stage of AI-assisted delivery",
    color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)",
    // sprintNodes live at the top of this file — passed in by the renderer
    callout: "The sprint changed, but human checkpoints stayed embedded throughout delivery.",
  },
  {
    id: "future",
    order: 7,
    layout: "h-strip",
    label: "Looking Ahead",
    num: "05",
    title: "Looking Ahead",
    subtitle: "Better steering — not more automation — is the next multiplier",
    color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)",
    cards: [
      { title: "Model Steering & Planning",  body: "Guardrails move upstream into prompts, tools, and workflow defaults." },
      { title: "Evolved Prompt Library",     body: "Prompt assets become reusable, modular, and versioned." },
      { title: "Human-Governed Pipeline",    body: "Automation helps at every step, but humans still decide to merge and deploy." },
      { title: "Team Enablement Kit",        body: "New team members can learn the playbook in days, not months." },
    ],
    callout: "The playbook is proven. The next gain comes from better steering, not less governance.",
  },
  {
    id: "platform",
    order: 8,
    layout: "process-lanes",
    label: "Service Platform",
    optional: true,
    num: "Optional",
    title: "Service Platform",
    subtitle: "One front door for IT demand, approvals, and procurement handoff",
    color: "#38BDF8", colorLight: "#7DD3FC", colorGlow: "rgba(56,189,248,0.28)",
    eyebrow: "Issue to Impact",
    summary: "The platform creates one governed front door for IT demand, approvals, and procurement continuation, helping users get the right tools faster.",
    heroPoints: ["Unified IT catalogs", "Role-based approvals", "Procurement handoff", "Mission readiness"],
    focusPanels: [
      { label: "Overview",        title: "One governed entry point",  body: "Discovery, request intake, approvals, and procurement continuation all sit in one flow." },
      { label: "Capability Zoom", title: "What users can do",         body: "Users can browse, research, track, and route requests without jumping tools." },
      { label: "Process Zoom",    title: "How requests move",         body: "Users request. Approvers review. Admins complete procurement in the right tool." },
    ],
    capabilities: [
      { title: "Browse IT Goods",       body: "See hardware and software options in one place.",            marker: "BG" },
      { title: "Research Solutions",    body: "Explore available IT services before submitting demand.",    marker: "RS" },
      { title: "Track Requests",        body: "Users and admins can see request status clearly.",           marker: "TR" },
      { title: "Continue Procurement",  body: "Approved demand flows into the right downstream tool.",     marker: "CP" },
    ],
    lanes: [
      {
        title: "Review & Request Tool",
        subtitle: "Service Platform",
        persona: "User: Any authorized personnel with agency credentials",
        accent: "#38BDF8",
        steps: [
          "Browse orderable goods and services.",
          "Submit a request form routed to the right approver.",
          "Approve or deny the queued request.",
        ],
      },
      {
        title: "Procurement Tool",
        subtitle: "e.g. Legacy Procurement",
        persona: "User: Admin with procurement permissions",
        accent: "#22D3EE",
        steps: [
          "Approved requests continue in the relevant procurement tool.",
        ],
      },
    ],
    talkingPoints: [
      "Fast-changing IT demand needs one clear front door.",
      "The platform simplifies discovery without weakening control.",
      "Role-based routing keeps the right people in the loop.",
      "The real payoff is faster access and stronger readiness.",
    ],
    callout: "This is not just a catalog. It is a governed path from need to procurement.",
  },
];

// Convenience: ordered list excluding shell slides (intro/landing)
export const contentSlides = slides
  .filter((s) => s.layout !== "cover" && s.layout !== "nav-hub")
  .sort((a, b) => a.order - b.order);

// Convenience: SLIDES registry for export scripts (replaces the hardcoded array)
export const SLIDES = slides
  .sort((a, b) => a.order - b.order)
  .map(({ id, label }) => ({ id, label }));

export default slides;
