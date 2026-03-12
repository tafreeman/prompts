import React, { useState, useEffect, useRef, useCallback, createContext, useContext } from "react";
import PropTypes from "prop-types";

const THEMES = [
  { id: "midnight-teal", name: "Midnight Teal", vibe: "Current Default", fontDisplay: "'Space Grotesk',sans-serif", fontBody: "'DM Sans',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap", bg: "#0B1426", bgCard: "#162240", bgDeep: "#111827", text: "#F0F4F8", textMuted: "#CBD5E1", textDim: "#64748B", accent: "#22D3EE", accentGlow: "rgba(8,145,178,0.3)", gradient: ["#22D3EE", "#10B981"] },
  { id: "obsidian-ember", name: "Obsidian & Ember", vibe: "Editorial / Luxury", fontDisplay: "'Playfair Display',serif", fontBody: "'Source Sans 3',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap", bg: "#1A1A1E", bgCard: "#242428", bgDeep: "#2C2C32", text: "#E8E4DF", textMuted: "#9B9590", textDim: "#6B6560", accent: "#D4A853", accentGlow: "rgba(212,168,83,0.25)", gradient: ["#D4A853", "#C75B39"] },
  { id: "arctic-steel", name: "Arctic Steel", vibe: "Industrial Nordic", fontDisplay: "'JetBrains Mono',monospace", fontBody: "'Nunito Sans',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap", bg: "#0F1318", bgCard: "#171D24", bgDeep: "#1E2630", text: "#D6DDE6", textMuted: "#7B8EA3", textDim: "#4E6178", accent: "#4FC3F7", accentGlow: "rgba(79,195,247,0.2)", gradient: ["#4FC3F7", "#B2EBF2"] },
  { id: "midnight-verdant", name: "Midnight Verdant", vibe: "Organic Tech", fontDisplay: "'Outfit',sans-serif", fontBody: "'Karla',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap", bg: "#0A1628", bgCard: "#112240", bgDeep: "#152A4E", text: "#CCD6F6", textMuted: "#8892B0", textDim: "#5A6480", accent: "#64FFDA", accentGlow: "rgba(100,255,218,0.18)", gradient: ["#64FFDA", "#48BB78"] },
  { id: "neon-noir", name: "Neon Noir", vibe: "Cyberpunk / Bold", fontDisplay: "'Chakra Petch',sans-serif", fontBody: "'Barlow',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap", bg: "#050508", bgCard: "#0D0D12", bgDeep: "#14141C", text: "#EAEAF0", textMuted: "#8585A0", textDim: "#55556E", accent: "#00E5FF", accentGlow: "rgba(0,229,255,0.2)", gradient: ["#00E5FF", "#FF2D95"] },
  { id: "paper-ink", name: "Paper & Ink", vibe: "Light Editorial", fontDisplay: "'DM Serif Display',serif", fontBody: "'Atkinson Hyperlegible',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap", bg: "#FAF8F5", bgCard: "#FFFFFF", bgDeep: "#F0EDE8", text: "#1A1A2E", textMuted: "#5C5C6F", textDim: "#8E8E9F", accent: "#1E40AF", accentGlow: "rgba(30,64,175,0.12)", gradient: ["#1E40AF", "#7C3AED"] },
];

const ThemeCtx = createContext(THEMES[0]);

const positionPropType = PropTypes.shape({
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
});

const themePropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  vibe: PropTypes.string.isRequired,
  fontDisplay: PropTypes.string.isRequired,
  fontBody: PropTypes.string.isRequired,
  fontsUrl: PropTypes.string.isRequired,
  bg: PropTypes.string.isRequired,
  bgCard: PropTypes.string.isRequired,
  bgDeep: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  textMuted: PropTypes.string.isRequired,
  textDim: PropTypes.string.isRequired,
  accent: PropTypes.string.isRequired,
  accentGlow: PropTypes.string.isRequired,
  gradient: PropTypes.arrayOf(PropTypes.string).isRequired,
});

const topicCardPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string,
  challenge: PropTypes.string,
  fix: PropTypes.string,
  icon: PropTypes.string,
  stat: PropTypes.string,
  statLabel: PropTypes.string,
});

const topicFocusPanelPropType = PropTypes.shape({
  label: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
});

const topicCapabilityPropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
});

const topicLanePropType = PropTypes.shape({
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  persona: PropTypes.string.isRequired,
  accent: PropTypes.string.isRequired,
  steps: PropTypes.arrayOf(PropTypes.string).isRequired,
});

const topicPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  colorLight: PropTypes.string.isRequired,
  colorGlow: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  optional: PropTypes.bool,
  eyebrow: PropTypes.string,
  summary: PropTypes.string,
  heroPoints: PropTypes.arrayOf(PropTypes.string),
  cards: PropTypes.arrayOf(topicCardPropType),
  talkingPoints: PropTypes.arrayOf(PropTypes.string),
  callout: PropTypes.string.isRequired,
  focusPanels: PropTypes.arrayOf(topicFocusPanelPropType),
  capabilities: PropTypes.arrayOf(topicCapabilityPropType),
  lanes: PropTypes.arrayOf(topicLanePropType),
});

let fallbackEntropyCursor = 0;
const FALLBACK_ENTROPY_DIVISOR = 997;

function getRandomUnit() {
  const cryptoApi = globalThis.crypto;

  if (cryptoApi && typeof cryptoApi.getRandomValues === "function") {
    return cryptoApi.getRandomValues(new Uint32Array(1))[0] / 0x100000000;
  }

  fallbackEntropyCursor = (fallbackEntropyCursor + 619) % FALLBACK_ENTROPY_DIVISOR;
  return fallbackEntropyCursor / FALLBACK_ENTROPY_DIVISOR;
}

const topics = [
  {
    id: "overview", num: "01", title: "Case Study Overview",
    subtitle: "How the AI-accelerated delivery story unfolds across governance, execution, and scale",
    color: "#67E8F9", colorLight: "#A5F3FC", colorGlow: "rgba(103,232,249,0.24)", icon: "◎",
    eyebrow: "Deck Flow",
    summary: "This opening slide condenses the full case study into a single page. Start with the mission need, show the platform operating model, then guide the audience through governance, delivery hurdles, sprint execution, and the scale path ahead.",
    heroPoints: ["Mission need", "Platform model", "Delivery guardrails", "Scale path"],
    cards: [
      { title: "Mission Need", body: "The agency needed one front door to unify fragmented IT catalogs and simplify request intake for users.", icon: "🎯" },
      { title: "Operating Model", body: "The platform connects discovery, request routing, approvals, and downstream procurement in one flow.", icon: "🔗" },
      { title: "Human Governance", body: "Every acceleration claim in the deck is grounded in human review, standards, and approval discipline.", icon: "👥" },
      { title: "What Follows", body: "The remaining pages unpack the detailed story: governance, hurdles, execution mechanics, and what scales next.", icon: "🧭" },
    ],
    talkingPoints: [
      "Lead with the mission problem before showing the technology.",
      "Position the platform as an operating model, not just a catalog UI.",
      "Use the remaining pages as evidence for governance, execution, and scale.",
      "Keep the throughline focused on readiness, speed, and controlled handoff.",
    ],
    callout: "Use this page as the executive case-study opener, then step into the supporting pages for proof.",
  },
  {
    id: "platform", num: "Optional", title: "Service Platform",
    subtitle: "Issue to impact: one front door for IT demand, approvals, and procurement handoff",
    color: "#38BDF8", colorLight: "#7DD3FC", colorGlow: "rgba(56,189,248,0.28)", icon: "⚓",
    optional: true,
    eyebrow: "Issue to Impact",
    summary: "The agency needed a unified platform to consolidate fragmented IT catalogs through an innovative, user-friendly interface that streamlines approvals and requests. The result is a governed path that helps personnel access essential tools faster while improving procurement efficiency and mission readiness.",
    heroPoints: ["Unified IT catalogs", "Role-based approvals", "Procurement handoff", "Mission readiness"],
    focusPanels: [
      { label: "Overview", title: "One governed entry point", body: "The source slide shows the whole operating model: discovery, request intake, approval routing, and procurement continuation anchored in one platform." },
      { label: "Capability Zoom", title: "What users can do", body: "The left-side close-up highlights the platform value: browse orderable goods, research IT solutions, track requests, and integrate with downstream procurement tools." },
      { label: "Process Zoom", title: "How requests move", body: "The right-side close-up clarifies the personas and handoff: any authorized user can request, while authenticated admins continue approved procurement in the relevant tool." },
    ],
    capabilities: [
      { title: "Browse Orderable IT Goods", body: "Explore available hardware and software offered within the platform instead of hunting across disconnected catalogs.", icon: "🧰" },
      { title: "Research IT Solutions", body: "Discover digital services and solution options before submitting a request, improving fit and reducing rework.", icon: "☁️" },
      { title: "Track Requests", body: "Monitor hardware requests and service orders after submission, with admin visibility for group-level management.", icon: "📋" },
      { title: "Integrate Procurement", body: "Approved demand can continue into downstream procurement systems to shorten cycle time and preserve governance.", icon: "🔗" },
    ],
    lanes: [
      {
        title: "Review & Request Tool",
        subtitle: "Service Platform",
        persona: "User: Any authorized personnel with agency credentials",
        accent: "#38BDF8",
        steps: [
          "Browse the catalog of orderable goods and services.",
          "Request items via form. The request is routed to the appropriate approver.",
          "Review the queued request and approve or deny it.",
        ],
      },
      {
        title: "Procurement Tool",
        subtitle: "e.g. Legacy Procurement",
        persona: "User: Admin with procurement permissions",
        accent: "#22D3EE",
        steps: [
          "If approved, the admin continues procurement in the relevant downstream tool.",
        ],
      },
    ],
    talkingPoints: [
      "Quickly changing IT demand needs a single, understandable front door.",
      "The platform simplifies discovery and request submission without weakening governance.",
      "Role-aware routing keeps approvals and procurement aligned to the right persona.",
      "The real impact is faster access to tools and stronger mission readiness.",
    ],
    callout: "This is more than a cleaner catalog experience. It is a governed operating model from need to procurement that can scale across the organization.",
  },
  {
    id: "human", num: "02", title: "Human in the Loop",
    subtitle: "AI Accelerates. Humans Govern.",
    color: "#0891B2", colorLight: "#22D3EE", colorGlow: "rgba(8,145,178,0.3)", icon: "◉",
    cards: [
      { title: "Gated Review Process", body: "Every line of AI-assisted code passed through structured pull request reviews with project-specific checklists before reaching production.", stat: "100%", statLabel: "Human-Reviewed" },
      { title: "Context-Rich Prompts", body: "Standardized prompt templates embedded with architecture documentation, data models, and coding standards kept AI output anchored to the actual system.", stat: "~90%", statLabel: "AI-Assisted Code" },
      { title: "Zero Critical Defects", body: "Disciplined human governance produced zero critical defects at production release — proving speed doesn't sacrifice quality.", stat: "0", statLabel: "Critical Defects" },
    ],
    callout: "AI generated the code. Humans owned every decision. That's not a limitation — it's the model.",
  },
  {
    id: "hurdles", num: "03", title: "Hurdles We Overcame",
    subtitle: "What changed from day one to delivery",
    color: "#F59E0B", colorLight: "#FBBF24", colorGlow: "rgba(245,158,11,0.3)", icon: "⬡",
    cards: [
      { title: "Prompt Standardization", challenge: "Developers used ad-hoc, inconsistent prompts — variable quality and constant refactoring.", fix: "Established versioned prompt templates with embedded architecture context and coding standards." },
      { title: "Process Realignment", challenge: "Traditional review workflows didn't account for AI-generated code patterns and volume.", fix: "Introduced AI-specific gated review checklists — convention adherence, test validation on every PR." },
      { title: "Governance Clearance", challenge: "Federal context required legal and policy approval before any AI-assisted code could reach production.", fix: "Proactively engaged internal risk, internal legal, and client legal to establish approval frameworks." },
      { title: "Team Enablement", challenge: "Team had varying levels of comfort and fluency with AI-assisted development tooling.", fix: "Internal hackathon built hands-on proficiency with tools and guardrails before delivery began." },
    ],
    callout: "Every hurdle became a guardrail. The friction we overcame early is the governance that keeps us fast now.",
  },
  {
    id: "sprint", num: "04", title: "AI Sprint Cycle",
    subtitle: "Human checkpoints at every stage of AI-assisted delivery",
    color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)", icon: "⟳",
    callout: "The AI modified sprint cycle includes numerous human-in-the-loop checkpoints. Development included rapid iterations and adherence to Agile best practices.",
  },
  {
    id: "future", num: "05", title: "Looking Ahead",
    subtitle: "Better steering — not more automation — is the next multiplier",
    color: "#10B981", colorLight: "#34D399", colorGlow: "rgba(16,185,129,0.3)", icon: "△",
    cards: [
      { title: "Model Steering & Planning", body: "System prompts, prefills, and tool configs encode architecture standards and compliance guardrails before developers write a single prompt." },
      { title: "Evolved Prompt Library", body: "Templates evolve from standalone instructions to modular components operating within a steered context — version-controlled, regression-tested." },
      { title: "Human-Governed Pipeline", body: "Automated static analysis and security scanning assist at every commit, but humans make the merge and deploy decisions." },
      { title: "Team Enablement Kit", body: "Onboarding now covers model steering techniques alongside prompt writing — adoption in days, not months." },
    ],
    callout: "The playbook is proven. The automated pipeline turns one project win into a practice-wide competitive advantage.",
  },
];

const sprintNodes = [
  { icon: "📋", label: "Requirements", type: "human" },
  { icon: "🖥️", label: "UI Mockup", type: "human" },
  { icon: "🤖", label: "AI Converts AC", type: "ai" },
  { icon: "✅", label: "AC Refinement", type: "human" },
  { icon: "👥", label: "Human Review", type: "human" },
  { icon: "⚙️", label: "AI Gen Code", type: "ai" },
  { icon: "💻", label: "Code Output", type: "ai" },
  { icon: "👥", label: "Code Review", type: "human" },
  { icon: "🧪", label: "Testing", type: "human" },
  { icon: "🐛", label: "Defect Fix", type: "human" },
  { icon: "🚀", label: "Deploy", type: "human" },
  { icon: "📊", label: "Client Review", type: "human" },
];

// ─── PARTICLES ───
function Particles({ color, type, active }) {
  const canvasRef = useRef(null);
  const pRef = useRef([]);
  const animRef = useRef(null);
  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth * 2; c.height = c.offsetHeight * 2; ctx.scale(2, 2);
    const W = c.offsetWidth, H = c.offsetHeight;
    pRef.current = [];
    let n;
    if (type === "hurdles") {
      n = 60;
    } else if (type === "sprint") {
      n = 40;
    } else {
      n = 30;
    }
    let vx, vy, r;
    for (let i = 0; i < n; i++) {
      if (type === "hurdles") {
        vx = (getRandomUnit() - 0.3) * 3;
        vy = -getRandomUnit() * 4 - 1;
        r = getRandomUnit() * 3 + 1;
      } else {
        vx = (getRandomUnit() - 0.5) * 0.5;
        vy = (getRandomUnit() - 0.5) * 0.5;
        r = getRandomUnit() * 2 + 1;
      }
      pRef.current.push({ x: getRandomUnit() * W, y: getRandomUnit() * H, vx, vy, r, o: getRandomUnit() * 0.5 + 0.15, life: getRandomUnit() * 100 });
    }
    function draw() {
      ctx.clearRect(0,0,W,H);
      pRef.current.forEach(p => {
        p.life++;
        if (type === "hurdles") {
          p.x += p.vx;
          p.y += p.vy;
          p.vy -= 0.02;
          if (p.y < -10 || p.x < -10 || p.x > W + 10) {
            p.x = getRandomUnit() * W;
            p.y = H + 10;
            p.vy = -getRandomUnit() * 4 - 1;
            p.vx = (getRandomUnit() - 0.3) * 3;
          }
        }
        else if(type==="human"){p.x+=Math.sin(p.life*0.015)*0.3;p.y+=Math.cos(p.life*0.012)*0.3;}
        else if (type === "sprint") {
          const cx = W / 2;
          const cy = H / 2;
          const a = Math.atan2(p.y - cy, p.x - cx);
          p.x += Math.cos(a + Math.PI / 2) * 0.35;
          p.y += Math.sin(a + Math.PI / 2) * 0.35;
          const d = Math.hypot(p.x - cx, p.y - cy);
          if (d > Math.max(W, H) * 0.55) {
            p.x = cx + (getRandomUnit() - 0.5) * W * 0.4;
            p.y = cy + (getRandomUnit() - 0.5) * H * 0.4;
          }
        }
        else {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > W) {
            p.vx *= -1;
          }
          if (p.y < 0 || p.y > H) {
            p.vy *= -1;
          }
        }
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=color+Math.round(p.o*255).toString(16).padStart(2,"0");ctx.fill();
      });
      if(type==="human"){const pts=pRef.current;for(let i=0;i<pts.length;i++){for(let j=i+1;j<pts.length;j++){const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);if(d<120){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=color+Math.round((1-d/120)*40).toString(16).padStart(2,"0");ctx.lineWidth=0.5;ctx.stroke();}}}}
      animRef.current=requestAnimationFrame(draw);
    }
    if(active) draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, type, active]);
  return <canvas ref={canvasRef} style={{ position:"absolute",inset:0,width:"100%",height:"100%",pointerEvents:"none",opacity:active?1:0,transition:"opacity 0.8s" }}/>;
}
Particles.propTypes = {
  color: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  active: PropTypes.bool.isRequired,
};

// ─── COMET TRANSITION ───
function CometTransition({ from, color, active, onDone }) {
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;
  const [phase, setPhase] = useState("idle"); // idle → launch → done

  useEffect(() => {
    if (!active || !from) return;
    setPhase("idle");
    // Force reflow then launch
    const t1 = requestAnimationFrame(() => {
      requestAnimationFrame(() => setPhase("launch"));
    });
    const t2 = setTimeout(() => {
      setPhase("done");
      onDoneRef.current();
    }, 700);
    return () => { cancelAnimationFrame(t1); clearTimeout(t2); };
  }, [active, from]);

  if (!active || !from) return null;

  const tx = (typeof globalThis.window !== "undefined" ? globalThis.window.innerWidth / 2 : 500) - from.x;
  const ty = (typeof globalThis.window !== "undefined" ? globalThis.window.innerHeight / 2 : 400) - from.y;

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 100, pointerEvents: "none", overflow: "hidden" }}>
      {/* Comet head */}
      <div style={{
        position: "absolute",
        left: from.x - 10,
        top: from.y - 10,
        width: 20, height: 20,
        borderRadius: "50%",
        background: color,
        boxShadow: `0 0 30px 10px ${color}, 0 0 60px 20px ${color}80, 0 0 4px 2px #FFFFFF`,
        transform: phase === "launch" ? `translate(${tx}px, ${ty}px) scale(0.3)` : "translate(0,0) scale(1)",
        opacity: phase === "launch" ? 0.2 : 1,
        transition: "transform 0.6s cubic-bezier(0.16,1,0.3,1), opacity 0.6s ease",
      }} />
      {/* Trail */}
      {[...new Array(8)].map((_, i) => (
        <div key={i} style={{
          position: "absolute",
          left: from.x - (6 - i * 0.5),
          top: from.y - (6 - i * 0.5),
          width: (12 - i), height: (12 - i),
          borderRadius: "50%",
          background: color,
          opacity: phase === "launch" ? 0 : (0.5 - i * 0.06),
          transform: phase === "launch" ? `translate(${tx * (1 - i * 0.08)}px, ${ty * (1 - i * 0.08)}px)` : "translate(0,0)",
          transition: `transform ${0.6 + i * 0.03}s cubic-bezier(0.16,1,0.3,1) ${i * 0.02}s, opacity ${0.5}s ease ${i * 0.02}s`,
        }} />
      ))}
      {/* Impact ring */}
      <div style={{
        position: "absolute",
        left: "50%", top: "50%",
        width: phase === "launch" ? 200 : 0,
        height: phase === "launch" ? 200 : 0,
        marginLeft: phase === "launch" ? -100 : 0,
        marginTop: phase === "launch" ? -100 : 0,
        borderRadius: "50%",
        border: `2px solid ${color}60`,
        background: `${color}08`,
        transition: "all 0.4s 0.4s ease-out",
        opacity: phase === "launch" ? 0 : 1,
      }} />
    </div>
  );
}
CometTransition.propTypes = {
  from: positionPropType,
  color: PropTypes.string,
  active: PropTypes.bool.isRequired,
  onDone: PropTypes.func.isRequired,
};

// ─── LANDING TILE ───
function LandingTile({ topic, onClick, hovered, onHover }) {
  const T = useContext(ThemeCtx);
  const h = hovered === topic.id;
  return (
    <div onClick={(e) => { const r = e.currentTarget.getBoundingClientRect(); onClick(topic.id, { x: r.left + r.width / 2, y: r.top + r.height / 2 }); }} onMouseEnter={() => onHover(topic.id)} onMouseLeave={() => onHover(null)}
      style={{ flex:1,position:"relative",cursor:"pointer",overflow:"hidden",borderRadius:16,padding:"32px 28px",display:"flex",flexDirection:"column",justifyContent:"space-between",minHeight:300,background:T.bgDeep,
        border:`1px solid ${h?topic.color+"60":"rgba(255,255,255,0.06)"}`,boxShadow:h?`0 0 40px ${topic.colorGlow}, 0 8px 32px rgba(0,0,0,0.4)`:"0 4px 20px rgba(0,0,0,0.3)",
        transform:h?"translateY(-8px) scale(1.02)":"translateY(0) scale(1)",transition:"all 0.4s cubic-bezier(0.34,1.56,0.64,1)" }}>
      <div>
        <div style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:12,fontWeight:500,color:topic.color,letterSpacing:2,textTransform:"uppercase",marginBottom:6,opacity:0.8 }}>{topic.num}</div>
        <div style={{ fontSize:36,marginBottom:10,lineHeight:1,filter:h?`drop-shadow(0 0 12px ${topic.colorGlow})`:"none",transition:"filter 0.4s" }}>{topic.icon}</div>
        <h2 style={{ fontFamily:T.fontDisplay,fontSize:22,fontWeight:700,color:T.text,lineHeight:1.15,margin:"0 0 6px" }}>{topic.title}</h2>
        <p style={{ fontSize:13,color:T.textDim,lineHeight:1.5,margin:0 }}>{topic.subtitle}</p>
      </div>
      <div style={{ display:"flex",alignItems:"center",gap:8,marginTop:20,color:topic.color,fontSize:12,fontWeight:600,fontFamily:"'Space Grotesk',sans-serif",transform:h?"translateX(6px)":"translateX(0)",transition:"transform 0.3s" }}>
        <span>Explore</span><span style={{ fontSize:16,lineHeight:1 }}>→</span>
      </div>
      <div style={{ position:"absolute",bottom:0,left:0,right:0,height:3,background:topic.color,opacity:h?1:0.4,transition:"opacity 0.3s" }}/>
    </div>
  );
}
LandingTile.propTypes = {
  topic: topicPropType.isRequired,
  onClick: PropTypes.func.isRequired,
  hovered: PropTypes.string,
  onHover: PropTypes.func.isRequired,
};

function OptionalDeckLink({ topic, onClick, hovered, onHover }) {
  const T = useContext(ThemeCtx);
  const h = hovered === topic.id;

  return (
    <div
      onClick={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        onClick(topic.id, { x: r.left + r.width / 2, y: r.top + r.height / 2 });
      }}
      onMouseEnter={() => onHover(topic.id)}
      onMouseLeave={() => onHover(null)}
      style={{
        position: "relative",
        cursor: "pointer",
        overflow: "hidden",
        borderRadius: 18,
        padding: "20px 22px",
        background: `linear-gradient(135deg, ${T.bgCard}, ${T.bgDeep})`,
        border: `1px solid ${h ? topic.color + "58" : topic.color + "22"}`,
        boxShadow: h ? `0 0 36px ${topic.colorGlow}, 0 10px 32px rgba(0,0,0,0.28)` : "0 8px 28px rgba(0,0,0,0.24)",
        transform: h ? "translateY(-4px)" : "translateY(0)",
        transition: "all 0.35s cubic-bezier(0.22,1,0.36,1)",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 18, alignItems: "flex-start", flexWrap: "wrap" }}>
        <div style={{ maxWidth: 520 }}>
          <div style={{ fontFamily: T.fontDisplay, fontSize: 10, letterSpacing: 2.8, textTransform: "uppercase", color: topic.colorLight, fontWeight: 700, marginBottom: 8 }}>
            Optional One-Pager
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <div style={{ fontSize: 26, lineHeight: 1 }}>{topic.icon}</div>
            <h3 style={{ fontFamily: T.fontDisplay, fontSize: 24, lineHeight: 1.05, color: T.text, margin: 0 }}>
              {topic.title}
            </h3>
          </div>
          <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6, margin: "0 0 12px" }}>
            {topic.summary}
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {topic.heroPoints.map((point, i) => (
              <span
                key={i}
                style={{
                  padding: "6px 10px",
                  borderRadius: 999,
                  background: topic.color + "12",
                  border: `1px solid ${topic.color}22`,
                  fontSize: 10.5,
                  fontWeight: 700,
                  color: T.text,
                }}
              >
                {point}
              </span>
            ))}
          </div>
        </div>

        <div style={{ minWidth: 210, alignSelf: "stretch", display: "flex", flexDirection: "column", justifyContent: "space-between", gap: 12 }}>
          <div style={{ display: "grid", gap: 8 }}>
            {topic.talkingPoints.slice(0, 2).map((point, i) => (
              <div
                key={i}
                style={{
                  borderRadius: 12,
                  padding: "10px 12px",
                  background: "rgba(255,255,255,0.03)",
                  border: `1px solid ${topic.color}16`,
                  fontSize: 11,
                  color: T.textMuted,
                  lineHeight: 1.45,
                }}
              >
                {point}
              </div>
            ))}
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 8, color: topic.color, fontFamily: T.fontDisplay, fontSize: 12, fontWeight: 700, letterSpacing: 0.4 }}>
            <span>Open the one-pager</span>
            <span style={{ fontSize: 16, lineHeight: 1, transform: h ? "translateX(4px)" : "translateX(0)", transition: "transform 0.25s ease" }}>→</span>
          </div>
        </div>
      </div>

      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 3, background: `linear-gradient(90deg, ${topic.color}, ${topic.colorLight})`, opacity: h ? 1 : 0.72, transition: "opacity 0.2s ease" }} />
    </div>
  );
}
OptionalDeckLink.propTypes = {
  topic: topicPropType.isRequired,
  onClick: PropTypes.func.isRequired,
  hovered: PropTypes.string,
  onHover: PropTypes.func.isRequired,
};

// ─── THEMATIC INTRO (Continuous Galaxy → Solar → Star) ───
// eslint-disable-next-line sonarjs/cognitive-complexity
function ThematicIntro({ onComplete }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const proceedTimeoutRef = useRef(null);
  const [phase, setPhase] = useState(0);
  const [isProceeding, setIsProceeding] = useState(false);
  const [buttonHovered, setButtonHovered] = useState(false);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  const T = useContext(ThemeCtx);

  const stats = [
    { val: "~40%", lbl: "Productivity Uplift", color: T.gradient ? T.gradient[0] : "#22D3EE" },
    { val: "2 mo", lbl: "To Production", color: T.gradient ? T.gradient[1] : "#34D399" },
    { val: "0", lbl: "Critical Defects", color: T.gradient ? T.gradient[1] : "#10B981" },
    { val: "~90%", lbl: "AI-Assisted Code", color: T.accent || "#A78BFA" },
  ];

  const handleProceed = useCallback(() => {
    if (phase < 8 || isProceeding || proceedTimeoutRef.current) return;
    setIsProceeding(true);
    proceedTimeoutRef.current = setTimeout(() => {
      proceedTimeoutRef.current = null;
      onCompleteRef.current();
    }, 850);
  }, [isProceeding, phase]);

  const accentColor = T.accent || "#22D3EE";
  const gradientStart = T.gradient ? T.gradient[0] : "#22D3EE";
  const gradientEnd = T.gradient ? T.gradient[1] : "#10B981";
  const buttonBorderColor = buttonHovered && !isProceeding ? accentColor : `${accentColor}55`;
  const buttonBackground = `linear-gradient(135deg, ${(T.bgCard || "#162240")}EE, ${(T.bgDeep || T.bg || "#0B1426")}E0)`;

  useEffect(() => () => {
    if (proceedTimeoutRef.current) clearTimeout(proceedTimeoutRef.current);
  }, []);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(6), 10850),
      setTimeout(() => setPhase(7), 11550),
      setTimeout(() => setPhase(8), 12250),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  useEffect(() => {
    const onKeyDown = (event) => {
      if (phase < 8 || isProceeding) return;
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        handleProceed();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handleProceed, isProceeding, phase]);

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const TOTAL = 11.4;
    let W = 0, H = 0;

    function resize() {
      W = window.innerWidth;
      H = window.innerHeight;
      c.width = W * dpr;
      c.height = H * dpr;
      c.style.width = W + "px";
      c.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener("resize", resize);

    const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
    const lerp = (a, b, n) => a + (b - a) * n;
    const smoothstep = (a, b, x) => {
      const n = clamp((x - a) / (b - a), 0, 1);
      return n * n * (3 - 2 * n);
    };
    function hexRgb(hex) {
      const raw = hex.replace("#", "");
      const normalized = raw.length === 3 ? raw.split("").map(ch => ch + ch).join("") : raw;
      const v = parseInt(normalized, 16);
      return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
    }
    const accent1 = T.gradient ? T.gradient[0] : "#22D3EE";
    const accent2 = T.gradient ? T.gradient[1] : "#10B981";
    const rgb1 = hexRgb(accent1);
    const rgb2 = hexRgb(accent2);
    const bgRgb = hexRgb(T.bg || "#050B18");
    const warmRgb = [255, 210, 120];
    const coolWhite = [235, 244, 255];
    const rgba = (rgb, a) => `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${a})`;
    const blendRgb = (a, b, n) => [
      Math.round(lerp(a[0], b[0], n)),
      Math.round(lerp(a[1], b[1], n)),
      Math.round(lerp(a[2], b[2], n)),
    ];
    const brightenRgb = (rgb, amount) => [
      Math.min(255, rgb[0] + amount),
      Math.min(255, rgb[1] + amount),
      Math.min(255, rgb[2] + amount),
    ];

    const warpStars = Array.from({ length: 520 }, () => ({
      x: (getRandomUnit() - 0.5) * 2400,
      y: (getRandomUnit() - 0.5) * 1600,
      z: getRandomUnit() * 2200 + 60,
      size: getRandomUnit() * 1.7 + 0.4,
      tint: getRandomUnit(),
    }));

    const galaxyArms = [];
    for (let arm = 0; arm < 4; arm++) {
      const offset = (arm / 4) * Math.PI * 2;
      for (let i = 0; i < 150; i++) {
        const dist = Math.pow(getRandomUnit(), 0.72) * 260 + 18;
        const angle = offset + dist * 0.028 + (getRandomUnit() - 0.5) * 0.36;
        galaxyArms.push({
          dist,
          angle,
          size: getRandomUnit() * 1.8 + 0.4,
          brightness: getRandomUnit() * 0.65 + 0.25,
          tint: getRandomUnit(),
        });
      }
    }
    for (let i = 0; i < 120; i++) {
      galaxyArms.push({
        dist: getRandomUnit() * 55,
        angle: getRandomUnit() * Math.PI * 2,
        size: getRandomUnit() * 2.6 + 0.7,
        brightness: getRandomUnit() * 0.4 + 0.5,
        tint: getRandomUnit() * 0.3,
      });
    }

    const dustBands = Array.from({ length: 18 }, (_, i) => ({
      radius: 120 + i * 18 + getRandomUnit() * 14,
      width: 18 + getRandomUnit() * 26,
      angle: getRandomUnit() * Math.PI * 2,
      tilt: (getRandomUnit() - 0.5) * 0.5,
      alpha: 0.04 + getRandomUnit() * 0.05,
      speed: 0.03 + getRandomUnit() * 0.05,
    }));

    const warpShells = Array.from({ length: 18 }, (_, i) => ({
      depth: i / 18,
      radius: 0.14 + i * 0.055 + getRandomUnit() * 0.02,
      width: 0.6 + getRandomUnit() * 1.4,
      skew: (getRandomUnit() - 0.5) * 0.08,
      offset: getRandomUnit(),
    }));

    const solarBodies = [
      { orbit: 350, size: 7, color: [122, 151, 194], speed: 0.24, angle: 0.9 },
      { orbit: 270, size: 12, color: [193, 145, 86], speed: 0.18, angle: 2.4, rings: true },
      { orbit: 190, size: 6, color: [131, 101, 74], speed: 0.32, angle: 4.15 },
      { orbit: 130, size: 5, color: [89, 154, 208], speed: 0.46, angle: 5.2 },
      { orbit: 90, size: 3.8, color: [225, 183, 132], speed: 0.58, angle: 1.55 },
    ];

    const breachDebris = Array.from({ length: 90 }, () => {
      const a = getRandomUnit() * Math.PI * 2;
      const s = getRandomUnit() * 9 + 3;
      return {
        angle: a,
        speed: s,
        size: getRandomUnit() * 3.2 + 0.8,
        decay: getRandomUnit() * 0.5 + 0.5,
        tint: getRandomUnit(),
      };
    });

    let startTime = performance.now();
    let prevFrame = startTime;

    // eslint-disable-next-line sonarjs/cognitive-complexity
    function draw(now) {
      const dt = Math.min(40, now - prevFrame || 16);
      prevFrame = now;
      const elapsed = (now - startTime) / 1000;
      const t = clamp(elapsed / TOTAL, 0, 1);
      const cx = W / 2;
      const cy = H / 2;

      const galaxyReveal = smoothstep(0.02, 0.24, t);
      const corePull = smoothstep(0.18, 0.56, t);
      const galaxyMorph = smoothstep(0.22, 0.44, t);
      const warpEntry = smoothstep(0.2, 0.4, t);
      const warpTunnel = smoothstep(0.3, 0.62, t) * (1 - smoothstep(0.72, 0.9, t));
      const systemReveal = smoothstep(0.42, 0.76, t);
      const starRush = smoothstep(0.62, 0.92, t);
      const breach = smoothstep(0.84, 1.0, t);
      const supernova = smoothstep(0.84, 0.94, t);
      const remnant = smoothstep(0.92, 1.0, t);
      const aftermath = Math.max(0, elapsed - TOTAL);
      const settle = 1 - Math.exp(-aftermath / 2.8);
      const supernovaPulse = supernova * Math.exp(-aftermath * 2.35);
      const debrisPulse = supernova * Math.exp(-aftermath * 1.05);
      const systemDrift = 1 - settle * 0.94;
      const remnantLight = lerp(1, 0.58, settle);
      const warpPunchIn = smoothstep(0.2, 0.29, t) * (1 - smoothstep(0.31, 0.42, t));
      const warpPunchOut = smoothstep(0.62, 0.73, t) * (1 - smoothstep(0.76, 0.86, t));
      const accelerationPulse = Math.pow(clamp(t, 0, 1), 2.35);
      const bank = Math.sin(t * Math.PI * 1.15) * 0.02 + corePull * 0.028 + warpTunnel * 0.02;

      const coreX = cx + Math.sin(t * Math.PI * 0.55) * W * 0.018 * (1 - systemReveal * 0.75);
      const coreY = cy - H * 0.035 + Math.cos(t * Math.PI * 0.75) * H * 0.008 * (1 - systemReveal * 0.65);
      const starCenterLock = smoothstep(0.74, 0.95, t);
      const starX = lerp(cx + W * 0.16 * (1 - starCenterLock), cx, starCenterLock);
      const starY = lerp(cy - H * 0.06 * (1 - starCenterLock), cy, starCenterLock);
      const focusBlend = smoothstep(0.52, 0.78, t);
      const focusX = lerp(coreX, starX, focusBlend);
      const focusY = lerp(coreY, starY, focusBlend);
      const velocityBase = 0.5 + galaxyReveal * 1 + corePull * 4.8 + warpEntry * 8.5 + warpTunnel * 14.5 + systemReveal * 8.4 + starRush * 22 + breach * 30;
      const velocity = lerp(velocityBase, 0.38, settle);
      const distortionBase = warpEntry * 0.45 + warpTunnel * 0.9 + starRush * 0.35;
      const distortion = distortionBase * (1 - settle * 0.9);
      const cameraCompression = 1 + distortion * 0.035;
      const ambientPresenceBase = smoothstep(0.16, 0.36, t) * (1 - smoothstep(0.72, 0.9, t));
      const ambientPresence = ambientPresenceBase * (1 - settle);
      const shakeBase = ambientPresenceBase * 0.45 + warpTunnel * 1.15 + breach * 0.2;
      const shake = shakeBase * (1 - settle * 0.92);
      const shakeX = Math.sin(elapsed * 38) * shake * 0.8;
      const shakeY = Math.cos(elapsed * 32) * shake * 0.55;
      const cameraZoomBase = 1 + corePull * 0.025 + warpPunchIn * 0.06 + warpTunnel * 0.14 + warpPunchOut * 0.045 + starRush * 0.12;
      const cameraZoom = lerp(cameraZoomBase, 1.018, settle);
      const cameraShiftYBase = 18 - corePull * 20 - warpTunnel * 24 - starRush * 12;
      const cameraShiftY = lerp(cameraShiftYBase, 6, settle);
      const focusParallaxX = (focusX - cx) * 0.04 * (1 - settle * 0.72);

      const bgLift = Math.round(10 * galaxyReveal + 20 * systemReveal * systemDrift + 30 * starRush * (1 - settle * 0.55) + 90 * supernovaPulse + 16 * remnantLight);
      ctx.fillStyle = `rgb(${Math.min(255, bgRgb[0] + bgLift * 0.05)},${Math.min(255, bgRgb[1] + bgLift * 0.08)},${Math.min(255, bgRgb[2] + bgLift * 0.14)})`;
      ctx.fillRect(0, 0, W, H);

      const vignette = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) * 0.72);
      vignette.addColorStop(0, "rgba(0,0,0,0)");
      vignette.addColorStop(1, `rgba(0,0,0,${0.42 - supernovaPulse * 0.2 + settle * 0.08})`);
      ctx.fillStyle = vignette;
      ctx.fillRect(0, 0, W, H);

      if (warpPunchIn > 0.01) {
        const entryFlash = ctx.createRadialGradient(focusX, focusY, 0, focusX, focusY, Math.max(W, H) * (0.08 + warpPunchIn * 0.12));
        entryFlash.addColorStop(0, rgba([255, 255, 255], 0.12 + warpPunchIn * 0.26));
        entryFlash.addColorStop(0.18, rgba(blendRgb(coolWhite, rgb1, 0.28), 0.08 + warpPunchIn * 0.16));
        entryFlash.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = entryFlash;
        ctx.fillRect(0, 0, W, H);

        ctx.beginPath();
        ctx.arc(focusX, focusY, (40 + warpPunchIn * 240) * (1 + warpPunchIn * 0.6), 0, Math.PI * 2);
        ctx.strokeStyle = rgba(blendRgb(rgb1, coolWhite, 0.4), 0.22 * (1 - warpPunchIn * 0.35));
        ctx.lineWidth = 2.2 + warpPunchIn * 4;
        ctx.stroke();
      }

      ctx.save();
      ctx.translate(cx + shakeX * 0.35, cy + shakeY * 0.25 + cameraShiftY * 0.2);
      ctx.scale(cameraZoom, cameraZoom);
      ctx.translate(-cx + focusParallaxX, -cy + cameraShiftY);

      if (warpEntry > 0.01) {
        const preGlow = ctx.createRadialGradient(focusX + shakeX * 0.5, focusY + shakeY * 0.5, 0, focusX + shakeX * 0.5, focusY + shakeY * 0.5, Math.max(W, H) * (0.1 + warpEntry * 0.22));
        preGlow.addColorStop(0, rgba(blendRgb(rgb1, coolWhite, 0.35), 0.06 + warpEntry * 0.08));
        preGlow.addColorStop(0.35, rgba(blendRgb(rgb2, rgb1, 0.45), 0.05 + warpEntry * 0.05));
        preGlow.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = preGlow;
        ctx.fillRect(0, 0, W, H);
      }

      if (warpTunnel > 0.01) {
        warpShells.forEach((shell, i) => {
          const ringProg = (shell.offset + elapsed * (0.18 + accelerationPulse * 0.9) + i * 0.02) % 1;
          const eased = Math.pow(ringProg, 0.8);
          const baseR = Math.max(W, H) * (shell.radius + (1 - eased) * (0.86 + warpTunnel * 0.26 + warpPunchIn * 0.14));
          const alpha = (1 - eased) * (0.02 + warpTunnel * 0.12) * (1 - starRush * 0.38);
          if (alpha <= 0.002) return;
          ctx.save();
          ctx.translate(focusX + shakeX, focusY + shakeY);
          ctx.rotate(bank * 5 + shell.skew * 9);
          ctx.beginPath();
          ctx.ellipse(0, 0, baseR, baseR * (0.45 - shell.skew * 0.2), 0, 0, Math.PI * 2);
          ctx.strokeStyle = rgba(blendRgb(rgb1, rgb2, 0.35 + shell.depth * 0.3), alpha);
          ctx.lineWidth = shell.width + warpTunnel * 1.1 + warpPunchIn * 0.8;
          ctx.stroke();
          ctx.restore();
        });

        for (let i = 0; i < 12; i++) {
          const angle = (i / 12) * Math.PI * 2 + elapsed * 0.15;
          const reach = Math.max(W, H) * (0.3 + warpTunnel * 0.42);
          const sx = focusX + shakeX + Math.cos(angle) * (24 + warpTunnel * 12);
          const sy = focusY + shakeY + Math.sin(angle) * (20 + warpTunnel * 8);
          const ex = focusX + shakeX + Math.cos(angle + bank * 2) * reach;
          const ey = focusY + shakeY + Math.sin(angle + bank * 2) * reach * 0.74;
          const beam = ctx.createLinearGradient(sx, sy, ex, ey);
          beam.addColorStop(0, rgba(coolWhite, 0));
          beam.addColorStop(0.25, rgba(blendRgb(rgb2, coolWhite, 0.22), 0.05 + warpTunnel * 0.05));
          beam.addColorStop(1, rgba(blendRgb(rgb1, rgb2, 0.55), 0));
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(ex, ey);
          ctx.strokeStyle = beam;
          ctx.lineWidth = 1.2 + warpTunnel * 1.3;
          ctx.stroke();
        }

        const tunnelCore = ctx.createRadialGradient(focusX, focusY, 0, focusX, focusY, 140 + warpTunnel * 140);
        tunnelCore.addColorStop(0, rgba(coolWhite, 0.05 + warpTunnel * 0.12 + warpPunchIn * 0.1));
        tunnelCore.addColorStop(0.32, rgba(blendRgb(rgb1, rgb2, 0.4), 0.04 + warpTunnel * 0.07));
        tunnelCore.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = tunnelCore;
        ctx.fillRect(0, 0, W, H);
      }

      if (ambientPresence > 0.01) {
        const hullGrad = ctx.createLinearGradient(cx, H - 110, cx, H);
        hullGrad.addColorStop(0, "rgba(0,0,0,0)");
        hullGrad.addColorStop(0.55, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.16 + ambientPresence * 0.1})`);
        hullGrad.addColorStop(1, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.42 + ambientPresence * 0.16})`);
        ctx.fillStyle = hullGrad;
        ctx.fillRect(0, H - 120, W, 120);

        [cx - W * 0.22, cx + W * 0.22].forEach((engineX, idx) => {
          const engineGrad = ctx.createRadialGradient(engineX + shakeX * 0.5, H + 10, 0, engineX + shakeX * 0.5, H + 10, 90 + warpTunnel * 50);
          engineGrad.addColorStop(0, rgba(blendRgb(rgb1, coolWhite, 0.22 + idx * 0.08), 0.12 + ambientPresence * 0.14 + warpTunnel * 0.08));
          engineGrad.addColorStop(0.4, rgba(blendRgb(rgb2, rgb1, 0.4), 0.06 + ambientPresence * 0.08));
          engineGrad.addColorStop(1, "rgba(0,0,0,0)");
          ctx.beginPath();
          ctx.arc(engineX + shakeX * 0.5, H + 10, 90 + warpTunnel * 50, 0, Math.PI * 2);
          ctx.fillStyle = engineGrad;
          ctx.fill();
        });

        const canopy = ctx.createLinearGradient(cx, H - 34, cx, H);
        canopy.addColorStop(0, `rgba(${rgb1[0]},${rgb1[1]},${rgb1[2]},${0.02 + ambientPresence * 0.03})`);
        canopy.addColorStop(1, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.18 + ambientPresence * 0.1})`);
        ctx.beginPath();
        ctx.moveTo(cx - 110, H);
        ctx.quadraticCurveTo(cx, H - 28 - warpTunnel * 12, cx + 110, H);
        ctx.closePath();
        ctx.fillStyle = canopy;
        ctx.fill();
      }

      // Persistent starfield — one continuous field, accelerating toward the destination star.
      warpStars.forEach(s => {
        s.z -= velocity * (dt * 0.1);
        if (s.z < 1) {
          s.z = 2200;
          s.x = (getRandomUnit() - 0.5) * 2400;
          s.y = (getRandomUnit() - 0.5) * 1600;
          s.tint = getRandomUnit();
        }
        const scale = (980 / s.z) * cameraCompression;
        const sx = cx + shakeX + s.x * scale + Math.sin(bank) * (s.y * scale * 0.24);
        const sy = cy + shakeY + s.y * scale * (1 + distortion * 0.08) + Math.cos(bank) * (s.x * scale * 0.05);
        if (sx < -180 || sx > W + 180 || sy < -180 || sy > H + 180) return;

        const dx = sx - focusX;
        const dy = sy - focusY;
        const dist = Math.hypot(dx, dy) || 1;
        const streakLen = Math.min(380, Math.max(0, (velocity - 1) * (1150 / (s.z + 40)) * (0.72 + warpTunnel * 0.65 + starRush * 0.22)));
        const tx = sx - (dx / dist) * streakLen;
        const ty = sy - (dy / dist) * streakLen;
        const tintMix = clamp(s.tint * 0.7 + systemReveal * 0.35, 0, 1);
        const headColor = blendRgb(blendRgb(rgb1, rgb2, tintMix), coolWhite, 0.38 + breach * 0.25);
        const tailColor = blendRgb(rgb1, rgb2, tintMix);
        const alpha = clamp((0.14 + (1800 - s.z) / 1800 * 0.64 + corePull * 0.08 + warpTunnel * 0.1 + starRush * 0.08) * (1 - settle * 0.8), 0.015, 1);
        if (streakLen > 1.5) {
          const grad = ctx.createLinearGradient(tx, ty, sx, sy);
          grad.addColorStop(0, rgba(tailColor, 0));
          grad.addColorStop(0.55, rgba(tailColor, alpha * 0.45));
          grad.addColorStop(1, rgba(headColor, alpha));
          ctx.beginPath();
          ctx.moveTo(tx, ty);
          ctx.lineTo(sx, sy);
          ctx.strokeStyle = grad;
          ctx.lineWidth = s.size * (1.04 + corePull * 0.5 + warpTunnel * 0.6 + starRush * 0.55 + breach * 0.4);
          ctx.stroke();
        } else {
          ctx.beginPath();
          ctx.arc(sx, sy, s.size * 0.75, 0, Math.PI * 2);
          ctx.fillStyle = rgba(headColor, alpha * 0.85);
          ctx.fill();
        }
      });

      // Galaxy backdrop.
      const galaxyAlpha = (1 - smoothstep(0.34, 0.58, t)) * (0.95 - breach * 0.25);
      if (galaxyAlpha > 0.01) {
        const galaxyScale = 0.6 + galaxyReveal * 1.5 + corePull * 0.35 + galaxyMorph * 0.35;
        const galaxyRot = elapsed * 0.05 + corePull * 0.18;
        const haze = ctx.createRadialGradient(coreX, coreY, 10, coreX, coreY, Math.max(W, H) * 0.36 * galaxyScale);
        haze.addColorStop(0, rgba(blendRgb(rgb2, warmRgb, 0.2), 0.08 * galaxyAlpha));
        haze.addColorStop(0.45, rgba(blendRgb(rgb1, rgb2, 0.4), 0.1 * galaxyAlpha));
        haze.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = haze;
        ctx.fillRect(0, 0, W, H);

        // Keeping the galaxy pass together makes the scene math easier to reason about.
        galaxyArms.forEach(star => {
          const a = star.angle + galaxyRot;
          const gx = coreX + Math.cos(a) * star.dist * galaxyScale;
          const gy = coreY + Math.sin(a) * star.dist * galaxyScale * 0.48;
          if (gx < -20 || gx > W + 20 || gy < -20 || gy > H + 20) return;
          const tint = blendRgb(rgb1, warmRgb, star.tint * 0.55);
          const glow = clamp(star.brightness * galaxyAlpha, 0, 1);
          const morphLen = galaxyMorph * (18 + star.dist * 0.18 + warpTunnel * 50);
          const mdx = gx - focusX;
          const mdy = gy - focusY;
          const md = Math.hypot(mdx, mdy) || 1;
          const tailX = gx + (mdx / md) * morphLen;
          const tailY = gy + (mdy / md) * morphLen;
          if (morphLen > 2) {
            const grad = ctx.createLinearGradient(gx, gy, tailX, tailY);
            grad.addColorStop(0, rgba(blendRgb(tint, coolWhite, 0.18), glow * 0.95));
            grad.addColorStop(1, rgba(tint, 0));
            ctx.beginPath();
            ctx.moveTo(gx, gy);
            ctx.lineTo(tailX, tailY);
            ctx.strokeStyle = grad;
            ctx.lineWidth = star.size * (0.8 + galaxyMorph * 1.4);
            ctx.stroke();
          }
          ctx.beginPath();
          ctx.arc(gx, gy, star.size * (0.65 + galaxyReveal * 0.65) * (1 - galaxyMorph * 0.32), 0, Math.PI * 2);
          ctx.fillStyle = rgba(tint, glow * (0.9 - galaxyMorph * 0.22));
          ctx.fill();
        });
        dustBands.forEach((band, i) => {
          const orbitGrow = 1 + corePull * 0.65 + systemReveal * 0.25;
          const radius = band.radius * orbitGrow;
          const sweep = band.angle + elapsed * band.speed + i * 0.018;
          ctx.save();
          ctx.translate(coreX, coreY);
          ctx.rotate(band.tilt + bank * 3);
          if (galaxyMorph < 0.78) {
            ctx.beginPath();
            ctx.ellipse(0, 0, radius, radius * 0.32, 0, sweep, sweep + Math.PI * (0.78 - galaxyMorph * 0.34));
            ctx.strokeStyle = rgba(blendRgb(rgb1, warmRgb, 0.38), band.alpha * galaxyAlpha * (1 - systemReveal * 0.55) * (1 - galaxyMorph * 0.55));
            ctx.lineWidth = band.width * (0.45 + corePull * 0.18);
            ctx.lineCap = "round";
            ctx.stroke();
          }
          ctx.restore();
        });

        const coreGlow = ctx.createRadialGradient(coreX, coreY, 0, coreX, coreY, 120 + corePull * 130);
        coreGlow.addColorStop(0, rgba([255, 248, 232], 0.16 + corePull * 0.1));
        coreGlow.addColorStop(0.35, rgba(blendRgb(rgb2, warmRgb, 0.32), 0.12 + corePull * 0.06));
        coreGlow.addColorStop(1, "rgba(0,0,0,0)");
        ctx.beginPath();
        ctx.arc(coreX, coreY, 120 + corePull * 130, 0, Math.PI * 2);
        ctx.fillStyle = coreGlow;
        ctx.fill();

        if (galaxyMorph > 0.08) {
          const collapseRingR = (90 + galaxyMorph * 420) * (1 + warpPunchIn * 0.45);
          ctx.beginPath();
          ctx.arc(coreX, coreY, collapseRingR, 0, Math.PI * 2);
          ctx.strokeStyle = rgba(blendRgb(rgb1, rgb2, 0.35), 0.1 * (1 - galaxyMorph * 0.55));
          ctx.lineWidth = 1.5 + galaxyMorph * 2.5;
          ctx.stroke();
        }
      }

      if (warpEntry > 0.02) {
        const spaceLensing = ctx.createRadialGradient(focusX + shakeX * 0.3, focusY + shakeY * 0.3, 0, focusX + shakeX * 0.3, focusY + shakeY * 0.3, Math.max(W, H) * (0.1 + warpEntry * 0.18));
        spaceLensing.addColorStop(0, rgba(coolWhite, 0.02 + warpEntry * 0.05));
        spaceLensing.addColorStop(0.28, rgba(blendRgb(rgb1, rgb2, 0.35), 0.03 + warpEntry * 0.04));
        spaceLensing.addColorStop(0.5, rgba([0, 0, 0], 0));
        spaceLensing.addColorStop(0.7, rgba(blendRgb(rgb1, rgb2, 0.5), 0.015 + warpTunnel * 0.02));
        spaceLensing.addColorStop(1, rgba([0, 0, 0], 0));
        ctx.fillStyle = spaceLensing;
        ctx.fillRect(0, 0, W, H);
      }

      if (warpPunchOut > 0.01) {
        const exitRing = ctx.createRadialGradient(starX, starY, 0, starX, starY, 120 + warpPunchOut * 240);
        exitRing.addColorStop(0, rgba([255, 255, 255], 0));
        exitRing.addColorStop(0.28, rgba(blendRgb(coolWhite, rgb2, 0.3), 0.08 + warpPunchOut * 0.14));
        exitRing.addColorStop(0.48, rgba(blendRgb(rgb1, rgb2, 0.5), 0.05 + warpPunchOut * 0.08));
        exitRing.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = exitRing;
        ctx.fillRect(0, 0, W, H);

        for (let i = 0; i < 14; i++) {
          const a = (i / 14) * Math.PI * 2 + elapsed * 0.08;
          const len = 60 + warpPunchOut * 200;
          const sx = starX + Math.cos(a) * 18;
          const sy = starY + Math.sin(a) * 18;
          const ex = starX + Math.cos(a) * len;
          const ey = starY + Math.sin(a) * len;
          const grad = ctx.createLinearGradient(sx, sy, ex, ey);
          grad.addColorStop(0, rgba(coolWhite, 0.18 + warpPunchOut * 0.16));
          grad.addColorStop(1, rgba(blendRgb(rgb2, warmRgb, 0.35), 0));
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(ex, ey);
          ctx.strokeStyle = grad;
          ctx.lineWidth = 1 + warpPunchOut * 2.2;
          ctx.stroke();
        }
      }

      // Solar system resolves out of the exit vector, with the target star present early and growing continuously.
      const systemAlpha = systemReveal * (1 - breach * 0.15) * systemDrift;
      if (systemAlpha > 0.01) {
        const orbitFade = (1 - smoothstep(0.74, 0.92, t)) * (1 - settle * 0.95);
        solarBodies.forEach((body, i) => {
          const bodyProgress = smoothstep(0.5 + i * 0.02, 0.9, t);
          const orbit = body.orbit * lerp(2.2, 0.24, bodyProgress);
          const angle = body.angle + elapsed * body.speed;
          const px = starX + Math.cos(angle) * orbit;
          const py = starY + Math.sin(angle) * orbit * 0.34;
          const radius = body.size * (1 + starRush * 0.45 + bodyProgress * 0.25);
          const motionBlur = starRush * (18 + i * 3);

          if (orbitFade > 0.02) {
            ctx.beginPath();
            ctx.ellipse(starX, starY, orbit, orbit * 0.34, 0, 0, Math.PI * 2);
            ctx.strokeStyle = rgba(coolWhite, orbitFade * 0.04 * systemAlpha);
            ctx.lineWidth = 1;
            ctx.stroke();
          }

          if (motionBlur > 2) {
            const dx = px - starX;
            const dy = py - starY;
            const d = Math.hypot(dx, dy) || 1;
            const trailGrad = ctx.createLinearGradient(px - (dx / d) * motionBlur, py - (dy / d) * motionBlur, px, py);
            trailGrad.addColorStop(0, rgba(body.color, 0));
            trailGrad.addColorStop(1, rgba(body.color, systemAlpha * 0.28));
            ctx.beginPath();
            ctx.moveTo(px - (dx / d) * motionBlur, py - (dy / d) * motionBlur);
            ctx.lineTo(px, py);
            ctx.strokeStyle = trailGrad;
            ctx.lineWidth = radius * 1.2;
            ctx.stroke();
          }

          const bodyGrad = ctx.createRadialGradient(px - radius * 0.35, py - radius * 0.35, 0, px, py, radius);
          bodyGrad.addColorStop(0, rgba(brightenRgb(body.color, 60), 1));
          bodyGrad.addColorStop(1, rgba(body.color, 0.92));
          ctx.beginPath();
          ctx.arc(px, py, radius, 0, Math.PI * 2);
          ctx.fillStyle = bodyGrad;
          ctx.fill();

          if (body.rings) {
            ctx.beginPath();
            ctx.ellipse(px, py, radius * 2.6, radius * 0.58, -0.28, 0, Math.PI * 2);
            ctx.strokeStyle = rgba(body.color, 0.42 * systemAlpha);
            ctx.lineWidth = 1.7;
            ctx.stroke();
          }
        });

        const starCollapse = smoothstep(0.9, 1.0, t);
        const starRadius = 14 + systemReveal * 40 + starRush * 190 + supernovaPulse * 120 - starCollapse * 260 - settle * 150;
        const starVisibleR = Math.max(0, starRadius);
        if (starVisibleR > 0.5) {
          const starGrad = ctx.createRadialGradient(starX, starY, 0, starX, starY, starVisibleR);
          const starAlpha = (1 - remnant * 0.92) * (1 - settle * 0.88);
          starGrad.addColorStop(0, rgba([255, 255, 245], 0.95 * starAlpha));
          starGrad.addColorStop(0.08, rgba([255, 245, 220], 0.96 * starAlpha));
          starGrad.addColorStop(0.24, rgba([255, 196, 96], 0.88 * starAlpha));
          starGrad.addColorStop(0.55, rgba(blendRgb(rgb2, warmRgb, 0.56), (0.34 + starRush * 0.16) * starAlpha));
          starGrad.addColorStop(1, "rgba(0,0,0,0)");
          ctx.beginPath();
          ctx.arc(starX, starY, starVisibleR, 0, Math.PI * 2);
          ctx.fillStyle = starGrad;
          ctx.fill();

          const coronaCount = 14;
          for (let i = 0; i < coronaCount; i++) {
            const a = (i / coronaCount) * Math.PI * 2 + elapsed * (0.22 + i * 0.01);
            const inner = starVisibleR * (0.48 + Math.sin(elapsed * 3.2 + i) * 0.015);
            const outer = inner + 20 + starRush * 80 * (1 - settle * 0.82) + Math.sin(elapsed * 4 + i * 2.1) * 10;
            ctx.beginPath();
            ctx.moveTo(starX + Math.cos(a) * inner, starY + Math.sin(a) * inner);
            ctx.lineTo(starX + Math.cos(a) * outer, starY + Math.sin(a) * outer);
            ctx.strokeStyle = rgba([255, 205, 120], (0.14 + starRush * 0.18) * starAlpha);
            ctx.lineWidth = 2 + starRush * 2.6 * (1 - settle * 0.8);
            ctx.lineCap = "round";
            ctx.stroke();
          }

          const approachBloom = ctx.createRadialGradient(starX, starY, 0, starX, starY, starVisibleR * (0.9 + starRush * 0.5));
          approachBloom.addColorStop(0, rgba([255, 255, 255], 0));
          approachBloom.addColorStop(0.2, rgba([255, 230, 180], (0.03 + starRush * 0.06) * (1 - settle * 0.9)));
          approachBloom.addColorStop(1, rgba(blendRgb(rgb2, warmRgb, 0.4), 0));
          ctx.fillStyle = approachBloom;
          ctx.fillRect(0, 0, W, H);
        }
      }

      ctx.restore();

      const readabilityMatte = smoothstep(0.67, 0.9, t) * (1 - smoothstep(0.95, 1.0, t));
      if (readabilityMatte > 0.01) {
        const matte = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.min(W, H) * 0.42);
        matte.addColorStop(0, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.72 * readabilityMatte})`);
        matte.addColorStop(0.34, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.42 * readabilityMatte})`);
        matte.addColorStop(0.7, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.12 * readabilityMatte})`);
        matte.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = matte;
        ctx.fillRect(0, 0, W, H);
      }

      if (breach > 0.001) {
        breachDebris.forEach((d, i) => {
          const dist = d.speed * 24 * debrisPulse * (0.6 + d.decay);
          const px = starX + Math.cos(d.angle + i * 0.01) * dist;
          const py = starY + Math.sin(d.angle + i * 0.01) * dist;
          const alpha = ((1 - supernova) * 0.4 + remnant * 0.08) * Math.exp(-aftermath * 1.05);
          const col = blendRgb(warmRgb, coolWhite, d.tint * 0.45 + breach * 0.35);
          ctx.beginPath();
          ctx.arc(px, py, d.size * (1 - supernovaPulse * 0.45), 0, Math.PI * 2);
          ctx.fillStyle = rgba(col, alpha);
          ctx.fill();
        });

        for (let i = 0; i < 3; i++) {
          const ringT = clamp((supernovaPulse - i * 0.08) / (1 - i * 0.08), 0, 1);
          if (ringT <= 0) continue;
          ctx.beginPath();
          ctx.arc(starX, starY, ringT * (190 + i * 140), 0, Math.PI * 2);
          ctx.strokeStyle = rgba(blendRgb(rgb1, warmRgb, 0.55), (1 - ringT) * 0.36);
          ctx.lineWidth = 3.2 - i * 0.45;
          ctx.stroke();
        }

        const whiteOut = ctx.createRadialGradient(starX, starY, 0, starX, starY, Math.max(W, H) * Math.max(supernovaPulse, 0.001) * 1.1);
        whiteOut.addColorStop(0, rgba([255, 255, 255], 0.9 * supernovaPulse));
        whiteOut.addColorStop(0.38, rgba([255, 244, 226], 0.72 * supernovaPulse));
        whiteOut.addColorStop(1, rgba(blendRgb(rgb2, coolWhite, 0.65), 0));
        ctx.fillStyle = whiteOut;
        ctx.fillRect(0, 0, W, H);

        const clearedSpace = ctx.createRadialGradient(starX, starY, 0, starX, starY, Math.max(W, H) * (0.08 + remnant * 0.5));
        clearedSpace.addColorStop(0, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.15 + remnant * 0.55 + settle * 0.18})`);
        clearedSpace.addColorStop(0.62, `rgba(${bgRgb[0]},${bgRgb[1]},${bgRgb[2]},${0.08 + remnant * 0.25 + settle * 0.08})`);
        clearedSpace.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = clearedSpace;
        ctx.fillRect(0, 0, W, H);

        if (remnant > 0.02) {
          const dwarfR = 8 + (1 - remnant) * 10;
          const dwarfAlpha = remnant * remnantLight;
          const dwarf = ctx.createRadialGradient(starX, starY, 0, starX, starY, dwarfR * 4.5);
          dwarf.addColorStop(0, rgba([255, 255, 255], 0.98 * dwarfAlpha));
          dwarf.addColorStop(0.16, rgba([220, 238, 255], 0.92 * dwarfAlpha));
          dwarf.addColorStop(0.38, rgba([170, 210, 255], 0.5 * dwarfAlpha));
          dwarf.addColorStop(1, "rgba(0,0,0,0)");
          ctx.beginPath();
          ctx.arc(starX, starY, dwarfR * 4.5, 0, Math.PI * 2);
          ctx.fillStyle = dwarf;
          ctx.fill();

          ctx.beginPath();
          ctx.arc(starX, starY, dwarfR, 0, Math.PI * 2);
          ctx.fillStyle = rgba([255, 255, 255], 0.95 * dwarfAlpha);
          ctx.fill();
        }
      }

      animRef.current = requestAnimationFrame(draw);
    }

    animRef.current = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener("resize", resize);
    };
  }, [T]);

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 200, background: T.bg || "#050B18",
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      opacity: isProceeding ? 0 : 1, transition: "opacity 0.85s ease",
    }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{
          position: "absolute",
          inset: -40,
          borderRadius: 28,
          background: phase >= 6
            ? `radial-gradient(circle at center, rgba(8,12,20,0.82) 0%, rgba(8,12,20,0.62) 38%, rgba(8,12,20,0.18) 72%, rgba(8,12,20,0) 100%)`
            : "transparent",
          backdropFilter: phase >= 6 ? "blur(12px) saturate(1.08)" : "blur(0px)",
          WebkitBackdropFilter: phase >= 6 ? "blur(12px) saturate(1.08)" : "blur(0px)",
          boxShadow: phase >= 6 ? `0 30px 90px rgba(0,0,0,0.35), inset 0 0 0 1px rgba(255,255,255,0.04)` : "none",
          opacity: phase >= 6 ? 1 : 0,
          transform: phase >= 6 ? "scale(1)" : "scale(0.92)",
          transition: "all 0.8s 0.05s cubic-bezier(0.22,1,0.36,1)",
          pointerEvents: "none",
        }} />

        {/* Horizontal accent line */}
        <div style={{
          width: phase >= 6 ? 120 : 0, height: 2, borderRadius: 1,
          background: `linear-gradient(90deg, transparent, ${accentColor}, transparent)`,
          marginBottom: 28, transition: "width 0.8s 0.2s cubic-bezier(0.22,1,0.36,1)",
        }} />

        {/* Kicker */}
        <div style={{
          fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: T.textDim || "#64748B",
          fontFamily: T.fontDisplay || "'Space Grotesk',sans-serif", fontWeight: 500, marginBottom: 12,
          opacity: phase >= 6 ? 1 : 0, transform: phase >= 6 ? "translateY(0) scale(1)" : "translateY(10px) scale(0.9)",
          transition: "all 0.6s 0.3s cubic-bezier(0.22,1,0.36,1)",
          textShadow: phase >= 6 ? "0 2px 16px rgba(0,0,0,0.55)" : "none",
        }}>AI-Assisted Delivery</div>

        {/* Title */}
        <h1 style={{
          fontFamily: T.fontDisplay || "'Space Grotesk',sans-serif", fontSize: 52, fontWeight: 700,
          color: T.text || "#F0F4F8", textAlign: "center", margin: "0 0 6px", letterSpacing: -1, lineHeight: 1.1,
          opacity: phase >= 6 ? 1 : 0,
          transform: phase >= 6 ? "translateY(0) scale(1)" : "translateY(30px) scale(0.8)",
          transition: "all 0.9s 0.1s cubic-bezier(0.22,1,0.36,1)",
          textShadow: phase >= 6 ? "0 10px 42px rgba(0,0,0,0.7), 0 2px 10px rgba(0,0,0,0.55)" : "none",
        }}>GenAI Transformation</h1>

        {/* Subtitle */}
        <p style={{
          fontSize: 18, fontStyle: "italic", textAlign: "center", margin: "0 0 36px",
          opacity: phase >= 6 ? 1 : 0, transform: phase >= 6 ? "translateY(0)" : "translateY(16px)",
          transition: "all 0.7s 0.4s ease",
          textShadow: phase >= 6 ? "0 2px 16px rgba(0,0,0,0.55)" : "none",
        }}>
          <span style={{
            background: `linear-gradient(90deg, ${gradientStart}, ${gradientEnd})`,
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            From prototype to production in 2 months
          </span>
        </p>

        {/* Stats row */}
        <div style={{
          display: "flex", gap: 40,
          opacity: phase >= 7 ? 1 : 0, transform: phase >= 7 ? "translateY(0)" : "translateY(15px)",
          transition: "all 0.7s ease",
          padding: phase >= 7 ? "14px 18px" : "0px 18px",
          borderRadius: 18,
          background: phase >= 7 ? "rgba(8,12,20,0.24)" : "rgba(8,12,20,0)",
          boxShadow: phase >= 7 ? "inset 0 0 0 1px rgba(255,255,255,0.04)" : "none",
        }}>
          {stats.map((s, i) => (
            <div key={i} style={{
              textAlign: "center",
              opacity: phase >= 7 ? 1 : 0,
              transform: phase >= 7 ? "translateY(0) scale(1)" : "translateY(12px) scale(0.9)",
              transition: `all 0.5s ${i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
            }}>
              <div style={{ fontFamily: T.fontDisplay || "'Space Grotesk',sans-serif", fontSize: 28, fontWeight: 700, color: s.color, textShadow: "0 6px 20px rgba(0,0,0,0.55)" }}>{s.val}</div>
              <div style={{ fontSize: 10, color: T.textMuted || T.textDim || "#CBD5E1", textTransform: "uppercase", letterSpacing: 1, marginTop: 2, textShadow: "0 2px 10px rgba(0,0,0,0.4)" }}>{s.lbl}</div>
            </div>
          ))}
        </div>

        {/* Bottom accent line */}
        <div style={{
          width: phase >= 7 ? 60 : 0, height: 2, borderRadius: 1,
          background: `linear-gradient(90deg, transparent, ${gradientEnd}, transparent)`,
          marginTop: 36, transition: "width 0.6s 0.3s ease",
        }} />

        <div style={{
          marginTop: 24,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
          opacity: phase >= 8 ? 1 : 0,
          transform: phase >= 8 ? "translateY(0) scale(1)" : "translateY(14px) scale(0.96)",
          transition: "all 0.7s 0.15s cubic-bezier(0.22,1,0.36,1)",
        }}>
          <button
            onClick={handleProceed}
            onMouseEnter={() => setButtonHovered(true)}
            onMouseLeave={() => setButtonHovered(false)}
            disabled={isProceeding}
            style={{
              cursor: isProceeding ? "default" : "pointer",
              border: `1px solid ${buttonBorderColor}`,
              borderRadius: 999,
              padding: "12px 22px",
              background: buttonBackground,
              color: T.text || "#F0F4F8",
              fontFamily: T.fontDisplay || "'Space Grotesk',sans-serif",
              fontSize: 13,
              fontWeight: 600,
              letterSpacing: 0.4,
              boxShadow: buttonHovered && !isProceeding
                ? `0 14px 34px rgba(0,0,0,0.4), 0 0 28px ${accentColor}20, 0 0 0 1px rgba(255,255,255,0.05) inset`
                : `0 10px 28px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.04) inset`,
              minWidth: 220,
              opacity: isProceeding ? 0.6 : 1,
              transform: buttonHovered && !isProceeding ? "translateY(-1px) scale(1.02)" : "translateY(0) scale(1)",
              transition: "transform 0.2s ease, opacity 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease",
            }}
          >
            {isProceeding ? "Opening landing page..." : "Proceed to landing page"}
          </button>
          <div style={{
            fontSize: 11,
            letterSpacing: 1.2,
            textTransform: "uppercase",
            color: T.textDim || "#64748B",
            textShadow: "0 2px 10px rgba(0,0,0,0.35)",
          }}>
            Press Enter or click to continue
          </div>
        </div>
      </div>
    </div>
  );
}
ThematicIntro.propTypes = { onComplete: PropTypes.func.isRequired };

// ─── THEME SELECTOR (Start Page) ───
function ThemeSelector({ onSelect }) {
  const [hovered, setHovered] = useState(null);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#08101C", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "40px 48px" }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&family=Playfair+Display:wght@700&family=JetBrains+Mono:wght@700&family=Outfit:wght@700&family=Chakra+Petch:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet" />

      <div style={{ textAlign: "center", marginBottom: 40, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
        <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: "#64748B", fontFamily: "'Space Grotesk',sans-serif", fontWeight: 500, marginBottom: 12 }}>GenAI Transformation</div>
        <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 40, fontWeight: 700, color: "#F0F4F8", margin: "0 0 10px", letterSpacing: -1 }}>Choose Your Theme</h1>
        <p style={{ fontSize: 14, color: "#94A3B8", margin: 0 }}>Select a visual style for the advocacy deck</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, maxWidth: 900, width: "100%" }}>
        {THEMES.map((t, i) => {
          const isH = hovered === t.id;
          return (
            <button key={t.id}
              onClick={() => onSelect(t)}
              onMouseEnter={() => setHovered(t.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                cursor: "pointer", borderRadius: 14, overflow: "hidden",
                border: `1px solid ${isH ? t.accent + "60" : "rgba(255,255,255,0.06)"}`,
                boxShadow: isH ? `0 0 30px ${t.accentGlow}` : "0 2px 12px rgba(0,0,0,0.3)",
                transform: isH ? "translateY(-4px) scale(1.02)" : "translateY(0) scale(1)",
                transition: "all 0.3s cubic-bezier(0.34,1.56,0.64,1)",
                opacity: entered ? 1 : 0,
                transitionDelay: `${0.1 + i * 0.06}s`,
                background: "none", padding: 0, textAlign: "left", width: "100%",
              }}>
              {/* Preview header */}
              <div style={{ background: t.bg, padding: "20px 18px 14px", position: "relative" }}>
                {/* Accent bar */}
                <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: `linear-gradient(90deg, ${t.gradient[0]}, ${t.gradient[1]})` }} />
                <div style={{ fontFamily: t.fontDisplay, fontSize: 18, fontWeight: 700, color: t.text, marginBottom: 4 }}>{t.name}</div>
                <div style={{ fontSize: 10, color: t.textDim, textTransform: "uppercase", letterSpacing: 1 }}>{t.vibe}</div>
              </div>
              {/* Preview body */}
              <div style={{ background: t.bgCard, padding: "14px 18px 16px" }}>
                {/* Mini card previews */}
                <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                  {[t.accent, t.gradient[1], t.textDim].map((c, j) => (
                    <div key={j} style={{ flex: 1, height: 6, borderRadius: 3, background: c, opacity: 0.6 }} />
                  ))}
                </div>
                <div style={{ fontSize: 11, color: t.textMuted, lineHeight: 1.4 }}>
                  <span style={{ color: t.accent, fontWeight: 600 }}>Aa</span> {t.fontDisplay.split(",")[0].replace(/'/g, "")}
                </div>
                {/* Color dots */}
                <div style={{ display: "flex", gap: 5, marginTop: 8 }}>
                  {[t.bg, t.bgCard, t.accent, t.gradient[1]].map((c, j) => (
                    <div key={j} style={{ width: 14, height: 14, borderRadius: "50%", background: c, border: "1px solid rgba(255,255,255,0.1)" }} />
                  ))}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
ThemeSelector.propTypes = { onSelect: PropTypes.func.isRequired };

// ─── BACK BUTTON ───
function BackBtn({ onClick }) {
  const T = useContext(ThemeCtx);
  return <button onClick={onClick} style={{ background:"none",border:"none",color:T.textDim,fontSize:13,cursor:"pointer",fontFamily:T.fontDisplay,marginBottom:20,display:"flex",alignItems:"center",gap:6 }}><span>←</span> Back</button>;
}
BackBtn.propTypes = { onClick: PropTypes.func.isRequired };

// ─── HUMAN SCREEN ───
function HumanScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e,setE]=useState(false); useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="human" active={e}/>
      <div style={{ position:"relative",zIndex:2,maxWidth:900,margin:"0 auto",padding:"48px 32px",opacity:e?1:0,transform:e?"translateY(0)":"translateY(30px)",transition:"all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ textAlign:"center",marginBottom:48 }}>
          <div style={{ width:64,height:64,borderRadius:"50%",background:topic.color+"18",border:`2px solid ${topic.color}40`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:28,margin:"0 auto 20px",boxShadow:`0 0 40px ${topic.colorGlow}` }}>{topic.icon}</div>
          <h1 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:44,fontWeight:700,color:"#F0F4F8",margin:"0 0 8px" }}>{topic.title}</h1>
          <p style={{ fontSize:16,color:topic.colorLight,fontStyle:"italic",margin:0 }}>{topic.subtitle}</p>
          <div style={{ width:80,height:3,background:topic.color,margin:"20px auto 0",borderRadius:2 }}/>
        </div>
        {topic.cards.map((c,i)=>(<div key={i} style={{ background:"#162240",borderRadius:12,padding:"28px 32px",marginBottom:20,display:"flex",alignItems:"flex-start",gap:24,borderLeft:`4px solid ${topic.color}`,opacity:e?1:0,transform:e?"translateY(0)":"translateY(20px)",transition:`all 0.6s ${0.3+i*0.15}s cubic-bezier(0.22,1,0.36,1)` }}>
          <div style={{ flexShrink:0,textAlign:"center",minWidth:72 }}><div style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:32,fontWeight:700,color:topic.colorLight }}>{c.stat}</div><div style={{ fontSize:10,color:"#64748B",textTransform:"uppercase",letterSpacing:1,marginTop:2 }}>{c.statLabel}</div></div>
          <div><h3 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:18,fontWeight:700,color:topic.colorLight,margin:"0 0 8px" }}>{c.title}</h3><p style={{ fontSize:14,color:"#CBD5E1",lineHeight:1.6,margin:0 }}>{c.body}</p></div>
        </div>))}
        <div style={{ textAlign:"center",marginTop:32,padding:"24px",borderTop:`1px solid ${topic.color}20`,borderBottom:`1px solid ${topic.color}20`,opacity:e?1:0,transition:"opacity 1s 0.9s" }}>
          <p style={{ fontSize:16,color:"#CBD5E1",lineHeight:1.6,margin:0,maxWidth:600,marginLeft:"auto",marginRight:"auto" }}><span style={{ color:topic.colorLight,fontWeight:700 }}>&ldquo;{topic.callout}&rdquo;</span></p>
        </div>
      </div>
    </div>
  );
}
HumanScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── HURDLES SCREEN ───
function HurdlesScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e,setE]=useState(false);const [vc,setVc]=useState(0);
  useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  useEffect(() => {
    if (!e) {
      return undefined;
    }

    const iv = topic.cards.map((_, i) => setTimeout(() => setVc(i + 1), 400 + i * 250));
    return () => iv.forEach(clearTimeout);
  }, [e, topic.cards]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="hurdles" active={e}/>
      <div style={{ position:"absolute",inset:0,pointerEvents:"none",overflow:"hidden" }}>{[...Array(8)].map((_,i)=>(<div key={i} style={{ position:"absolute",left:"-10%",top:`${10+i*11}%`,width:e?"120%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}15,transparent)`,transition:`width ${0.6+i*0.1}s ${0.2+i*0.05}s cubic-bezier(0.16,1,0.3,1)` }}/>))}</div>
      <div style={{ position:"relative",zIndex:2,padding:"36px 48px" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ marginBottom:32,transform:e?"translateX(0)":"translateX(-100px)",opacity:e?1:0,transition:"all 0.5s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ display:"flex",alignItems:"center",gap:16,marginBottom:6 }}><div style={{ fontSize:36,transform:e?"rotate(0deg)":"rotate(-90deg)",transition:"transform 0.6s 0.2s cubic-bezier(0.34,1.56,0.64,1)" }}>{topic.icon}</div><h1 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:42,fontWeight:700,color:"#F0F4F8",margin:0,letterSpacing:-1 }}>{topic.title}</h1></div>
          <p style={{ fontSize:15,color:topic.colorLight,fontStyle:"italic",margin:0,paddingLeft:52 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,maxWidth:1100 }}>
          {topic.cards.map((c,i)=>{const v=i<vc,fl=i%2===0,hiddenCardTransform=`translateX(${fl?"-60px":"60px"}) scale(0.92)`;return(
            <div key={i} style={{ background:"#162240",borderRadius:12,padding:"24px 28px",borderTop:`3px solid ${topic.color}`,position:"relative",overflow:"hidden",opacity:v?1:0,transform:v?"translateX(0) scale(1)":hiddenCardTransform,transition:"all 0.45s cubic-bezier(0.34,1.56,0.64,1)" }}>
              <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at ${fl?"left":"right"} center,${topic.color}15,transparent 60%)`,opacity:v?1:0,transition:"opacity 0.3s" }}/>
              <div style={{ position:"relative",zIndex:1 }}>
                <div style={{ display:"flex",alignItems:"center",gap:10,marginBottom:14 }}><div style={{ width:28,height:28,borderRadius:6,background:topic.color+"20",display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"'Space Grotesk',sans-serif",fontWeight:700,fontSize:13,color:topic.color }}>{i+1}</div><h3 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:17,fontWeight:700,color:"#F0F4F8",margin:0 }}>{c.title}</h3></div>
                <div style={{ marginBottom:12 }}><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:"#EF4444",marginBottom:4 }}>Challenge</div><p style={{ fontSize:13,color:"#94A3B8",lineHeight:1.5,margin:0 }}>{c.challenge}</p></div>
                <div><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:"#10B981",marginBottom:4 }}>Solution</div><p style={{ fontSize:13,color:"#CBD5E1",lineHeight:1.5,margin:0 }}>{c.fix}</p></div>
              </div>
            </div>);})}
        </div>
        <div style={{ marginTop:28,background:"#162240",borderRadius:10,padding:"16px 28px",borderLeft:`4px solid ${topic.color}`,display:"flex",alignItems:"center",gap:16,transform:e?"translateX(0)":"translateX(200px)",opacity:e?1:0,transition:"all 0.6s 1.3s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ fontSize:24,color:topic.color }}>⚡</div><p style={{ fontSize:14,color:"#CBD5E1",lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p>
        </div>
      </div>
    </div>
  );
}
HurdlesScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ─── FUTURE SCREEN ───
function FutureScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e,setE]=useState(false); useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="future" active={e}/>
      <div style={{ position:"absolute",top:"42%",left:"50%",width:e?"140%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}30,transparent)`,transform:"translateX(-50%)",transition:"width 1.2s cubic-bezier(0.22,1,0.36,1)" }}/>
      <div style={{ position:"relative",zIndex:2,padding:"36px 48px" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ textAlign:"center",marginBottom:40,opacity:e?1:0,transform:e?"translateY(0) scale(1)":"translateY(40px) scale(0.95)",transition:"all 0.7s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize:36,marginBottom:12,filter:`drop-shadow(0 0 16px ${topic.colorGlow})` }}>{topic.icon}</div>
          <h1 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:44,fontWeight:700,color:"#F0F4F8",margin:"0 0 8px" }}>{topic.title}</h1>
          <p style={{ fontSize:16,color:topic.colorLight,fontStyle:"italic",margin:0 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,maxWidth:1000,margin:"0 auto" }}>
          {topic.cards.map((c,i)=>(<div key={i} style={{ background:"#162240",borderRadius:12,padding:"28px 28px 22px",borderLeft:`4px solid ${topic.color}`,opacity:e?1:0,transform:e?"scale(1)":"scale(0.8)",transition:`all 0.5s ${0.3+i*0.12}s cubic-bezier(0.22,1,0.36,1)` }}><h3 style={{ fontFamily:"'Space Grotesk',sans-serif",fontSize:17,fontWeight:700,color:topic.colorLight,margin:"0 0 10px" }}>{c.title}</h3><p style={{ fontSize:13.5,color:"#CBD5E1",lineHeight:1.6,margin:0 }}>{c.body}</p></div>))}
        </div>
        <div style={{ textAlign:"center",marginTop:36,maxWidth:700,marginLeft:"auto",marginRight:"auto",opacity:e?1:0,transition:"opacity 0.8s 1s" }}><p style={{ fontSize:15,color:"#CBD5E1",lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p></div>
      </div>
    </div>
  );
}
FutureScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

function PlatformMockFrame({ topic, entered, theme }) {
  return (
    <div style={{ position:"relative",minHeight:260,borderRadius:20,overflow:"hidden",background:`linear-gradient(145deg,${theme.bgDeep},${theme.bgCard})`,border:`1px solid ${topic.color}26`,boxShadow:`0 20px 56px ${topic.colorGlow}` }}>
      <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at 15% 15%,${topic.color}20,transparent 28%),radial-gradient(circle at 85% 18%,${topic.color}14,transparent 26%)`,pointerEvents:"none" }}/>
      <div style={{ position:"relative",zIndex:1,padding:"16px 18px 0",display:"flex",alignItems:"center",justifyContent:"space-between" }}>
        <div style={{ display:"flex",gap:6 }}>{["#F97316","#FBBF24","#22C55E"].map((c,i)=><div key={i} style={{ width:9,height:9,borderRadius:"50%",background:c,opacity:0.9 }}/>)}</div>
        <div style={{ display:"flex",gap:8,flexWrap:"wrap",justifyContent:"flex-end" }}>
          {topic.heroPoints.slice(0,2).map((p,i)=><span key={i} style={{ fontSize:10,fontWeight:700,letterSpacing:1,textTransform:"uppercase",padding:"5px 9px",borderRadius:999,background:topic.color+"14",border:`1px solid ${topic.color}28`,color:topic.colorLight,fontFamily:theme.fontDisplay }}>{p}</span>)}
        </div>
      </div>
      <div style={{ position:"relative",zIndex:1,padding:"20px 20px 22px",display:"flex",flexWrap:"wrap",gap:18,alignItems:"stretch" }}>
        <div style={{ flex:"1 1 260px",display:"flex",flexDirection:"column",justifyContent:"space-between" }}>
          <div>
            <div style={{ fontSize:11,textTransform:"uppercase",letterSpacing:2,color:topic.colorLight,fontWeight:700,fontFamily:theme.fontDisplay,marginBottom:10 }}>Unified Service Catalog</div>
            <div style={{ fontFamily:theme.fontDisplay,fontSize:24,fontWeight:700,color:theme.text,lineHeight:1.05,marginBottom:10 }}>Request. Review. Route.</div>
            <p style={{ fontSize:12.5,color:theme.textMuted,lineHeight:1.6,margin:0,maxWidth:360 }}>A cleaner procurement journey starts with a single front door for discovery, request intake, approval routing, and downstream handoff.</p>
          </div>
          <div style={{ display:"flex",gap:10,flexWrap:"wrap",marginTop:14 }}>
            <button style={{ border:"none",borderRadius:12,padding:"9px 13px",background:`linear-gradient(90deg,${topic.color},${topic.colorLight})`,color:"#04111F",fontWeight:800,fontSize:10.5,letterSpacing:0.5,cursor:"default",fontFamily:theme.fontDisplay }}>Browse Catalog</button>
            <div style={{ display:"flex",alignItems:"center",gap:8,padding:"8px 11px",borderRadius:12,background:"rgba(255,255,255,0.04)",border:`1px solid ${topic.color}18`,color:theme.textMuted,fontSize:10.5 }}>
              <span style={{ width:8,height:8,borderRadius:"50%",background:"#22C55E",boxShadow:"0 0 12px rgba(34,197,94,0.45)" }}/>
              CAC-enabled access
            </div>
          </div>
        </div>
        <div style={{ flex:"1 1 240px",display:"grid",gap:10 }}>
          {[
            { label:"Discovery", value:"Catalogs + services" },
            { label:"Governance", value:"Approval queue" },
            { label:"Tracking", value:"User + admin visibility" },
            { label:"Handoff", value:"Procurement continuation" },
          ].map((item,i)=>(
            <div key={i} style={{ background:"rgba(255,255,255,0.04)",border:`1px solid ${topic.color}18`,borderRadius:14,padding:"12px 14px",opacity:entered?1:0,transform:entered?"translateX(0)":"translateX(24px)",transition:`all 0.45s ${0.2 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)` }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.3,color:theme.textDim,fontWeight:700,marginBottom:4 }}>{item.label}</div>
              <div style={{ fontFamily:theme.fontDisplay,fontSize:15,fontWeight:700,color:theme.text }}>{item.value}</div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ position:"relative",zIndex:1,padding:"0 20px 16px",display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(120px,1fr))",gap:8 }}>
        {topic.heroPoints.map((point,i)=>(
          <div key={i} style={{ borderRadius:12,padding:"8px 10px",background:"rgba(4,17,31,0.35)",border:`1px solid ${topic.color}16`,fontSize:10.5,color:theme.textMuted,lineHeight:1.4 }}>
            <span style={{ color:topic.colorLight,fontWeight:700 }}>{String(i + 1).padStart(2,"0")}</span> {point}
          </div>
        ))}
      </div>
    </div>
  );
}
PlatformMockFrame.propTypes = {
  topic: topicPropType.isRequired,
  entered: PropTypes.bool.isRequired,
  theme: themePropType.isRequired,
};

function PlatformLane({ lane, entered, index, theme }) {
  return (
    <div style={{ flex:index===0?"1.3 1 580px":"0.9 1 360px",background:theme.bgCard,borderRadius:20,border:`1px solid ${lane.accent}2a`,overflow:"hidden",opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(24px)",transition:`all 0.55s ${0.25 + index * 0.12}s cubic-bezier(0.22,1,0.36,1)` }}>
      <div style={{ padding:"18px 20px 14px",borderBottom:`1px solid ${lane.accent}1c`,background:`linear-gradient(180deg,${lane.accent}12,transparent)` }}>
        <div style={{ fontSize:11,textTransform:"uppercase",letterSpacing:2,color:lane.accent,fontWeight:800,fontFamily:theme.fontDisplay,marginBottom:6 }}>{lane.title}</div>
        <div style={{ fontFamily:theme.fontDisplay,fontSize:28,fontWeight:700,color:theme.text,lineHeight:1.05,marginBottom:6 }}>{lane.subtitle}</div>
        <div style={{ display:"inline-flex",alignItems:"center",gap:8,padding:"8px 12px",borderRadius:999,background:lane.accent+"12",border:`1px solid ${lane.accent}24`,fontSize:11,color:theme.textMuted }}>
          <span style={{ width:8,height:8,borderRadius:"50%",background:lane.accent }}/>
          {lane.persona}
        </div>
      </div>
      <div style={{ padding:"18px 20px 22px",display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(160px,1fr))",gap:14 }}>
        {lane.steps.map((step,i)=>(
          <div key={i} style={{ position:"relative",padding:"14px 14px 16px",borderRadius:16,background:theme.bgDeep,border:`1px solid ${lane.accent}18` }}>
            <div style={{ width:28,height:28,borderRadius:"50%",display:"flex",alignItems:"center",justifyContent:"center",background:lane.accent+"18",color:lane.accent,fontWeight:800,fontFamily:theme.fontDisplay,fontSize:12,marginBottom:10 }}>{i + 1}</div>
            <p style={{ fontSize:13,color:theme.textMuted,lineHeight:1.6,margin:0 }}>{step}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
PlatformLane.propTypes = {
  lane: topicLanePropType.isRequired,
  entered: PropTypes.bool.isRequired,
  index: PropTypes.number.isRequired,
  theme: themePropType.isRequired,
};

function OverviewScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const platformTopic = topics.find((item) => item.id === "platform") || topic;
  const storyTopics = topics.filter((item) => !item.optional && item.id !== topic.id);

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);

  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="human" active={entered} />
      <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at 10% 0%,${topic.color}18,transparent 26%),radial-gradient(circle at 88% 18%,${platformTopic.color}14,transparent 24%)`,pointerEvents:"none" }} />
      <div style={{ position:"relative",zIndex:2,maxWidth:1320,margin:"0 auto",padding:"24px 28px 28px" }}>
        <BackBtn onClick={onBack} />

        <div style={{ display:"grid",gap:18 }}>
          <div style={{ display:"grid",gridTemplateColumns:"minmax(0,1.05fr) minmax(340px,0.95fr)",gap:18,alignItems:"stretch" }}>
            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:26,padding:"22px 24px",border:`1px solid ${topic.color}22`,boxShadow:"0 14px 48px rgba(0,0,0,0.24)",opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(20px)",transition:"all 0.65s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:3,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:10 }}>{topic.eyebrow}</div>
              <h1 style={{ fontFamily:T.fontDisplay,fontSize:42,fontWeight:800,color:T.text,lineHeight:0.96,letterSpacing:-1.2,margin:"0 0 10px" }}>{topic.title}</h1>
              <p style={{ fontSize:15,color:topic.colorLight,fontStyle:"italic",lineHeight:1.45,margin:"0 0 12px" }}>{topic.subtitle}</p>
              <p style={{ fontSize:13.5,color:T.textMuted,lineHeight:1.65,margin:"0 0 14px",maxWidth:720 }}>{topic.summary}</p>
              <div style={{ display:"flex",flexWrap:"wrap",gap:8,marginBottom:16 }}>
                {topic.heroPoints.map((point,i)=>(
                  <div key={i} style={{ padding:"7px 10px",borderRadius:999,background:topic.color+"12",border:`1px solid ${topic.color}24`,fontSize:10.5,fontWeight:700,color:T.text }}>{point}</div>
                ))}
              </div>
              <div style={{ display:"grid",gridTemplateColumns:"repeat(2,minmax(0,1fr))",gap:10 }}>
                {topic.cards.map((card,i)=>(
                  <div key={i} style={{ background:T.bgDeep,borderRadius:16,padding:"14px 14px 15px",borderTop:`2px solid ${topic.color}`,opacity:entered?1:0,transform:entered?"scale(1)":"scale(0.95)",transition:`all 0.45s ${0.18 + i * 0.08}s cubic-bezier(0.34,1.56,0.64,1)` }}>
                    <div style={{ display:"flex",alignItems:"center",gap:10,marginBottom:8 }}>
                      <div style={{ fontSize:20 }}>{card.icon}</div>
                      <h3 style={{ fontFamily:T.fontDisplay,fontSize:15,fontWeight:700,color:T.text,margin:0,lineHeight:1.2 }}>{card.title}</h3>
                    </div>
                    <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.55,margin:0 }}>{card.body}</p>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ display:"grid",gap:18 }}>
              <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:26,padding:"18px",border:`1px solid ${platformTopic.color}20`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(20px)",transition:"all 0.65s 0.08s cubic-bezier(0.22,1,0.36,1)" }}>
                <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",gap:12,marginBottom:10,flexWrap:"wrap" }}>
                  <div>
                    <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:platformTopic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:5 }}>Operating Model Snapshot</div>
                    <div style={{ fontFamily:T.fontDisplay,fontSize:23,fontWeight:700,color:T.text }}>Where the story starts</div>
                  </div>
                  <div style={{ padding:"7px 10px",borderRadius:999,background:platformTopic.color+"12",border:`1px solid ${platformTopic.color}24`,fontSize:10.5,color:T.textMuted }}>Optional one-pager available</div>
                </div>
                <PlatformMockFrame topic={platformTopic} entered={entered} theme={T} />
              </div>

              <div style={{ background:T.bgCard,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(16px)",transition:"all 0.6s 0.14s cubic-bezier(0.22,1,0.36,1)" }}>
                <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:8 }}>Flow Through The Deck</div>
                <div style={{ display:"grid",gap:10 }}>
                  {storyTopics.map((story) => (
                    <div key={story.id} style={{ display:"grid",gridTemplateColumns:"44px minmax(0,1fr)",gap:12,alignItems:"start",padding:"12px 12px 13px",borderRadius:16,background:T.bgDeep,border:`1px solid ${story.color}18`,boxShadow:`0 10px 26px ${story.colorGlow || "rgba(0,0,0,0.16)"}` }}>
                      <div style={{ width:44,height:44,borderRadius:14,display:"flex",alignItems:"center",justifyContent:"center",background:story.color+"14",color:story.colorLight,fontFamily:T.fontDisplay,fontSize:13,fontWeight:800 }}>{story.num}</div>
                      <div>
                        <div style={{ display:"flex",alignItems:"center",gap:8,marginBottom:4 }}>
                          <div style={{ fontSize:18,lineHeight:1 }}>{story.icon}</div>
                          <h3 style={{ fontFamily:T.fontDisplay,fontSize:16,fontWeight:700,color:T.text,margin:0 }}>{story.title}</h3>
                        </div>
                        <p style={{ fontSize:11.5,color:T.textDim,lineHeight:1.45,margin:"0 0 6px" }}>{story.subtitle}</p>
                        <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.5,margin:0 }}>
                          {story.cards?.[0]?.body || story.cards?.[0]?.fix || story.callout}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div style={{ display:"grid",gridTemplateColumns:"minmax(0,1.15fr) minmax(320px,0.85fr)",gap:18 }}>
            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.2s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",gap:14,marginBottom:10,flexWrap:"wrap" }}>
                <div>
                  <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:5 }}>Executive Takeaways</div>
                  <div style={{ fontFamily:T.fontDisplay,fontSize:23,fontWeight:700,color:T.text }}>How to tell the story cleanly</div>
                </div>
                <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.5,margin:0,maxWidth:320 }}>This page is the compact opener. Use it to orient the audience before going deeper into the detailed pages.</p>
              </div>
              <div style={{ display:"grid",gridTemplateColumns:"repeat(2,minmax(0,1fr))",gap:10 }}>
                {topic.talkingPoints.map((point,i)=>(
                  <div key={i} style={{ padding:"12px 12px 13px",borderRadius:16,background:T.bgDeep,border:`1px solid ${topic.color}16`,fontSize:11.5,color:T.textMuted,lineHeight:1.5 }}>
                    <div style={{ color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,fontSize:10.5,letterSpacing:1.2,textTransform:"uppercase",marginBottom:6 }}>{String(i + 1).padStart(2,"0")}</div>
                    {point}
                  </div>
                ))}
              </div>
            </div>

            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${platformTopic.color}18`,borderLeft:`4px solid ${topic.color}`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.26s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:platformTopic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:8 }}>Optional Supporting Page</div>
              <h3 style={{ fontFamily:T.fontDisplay,fontSize:24,fontWeight:700,color:T.text,lineHeight:1.05,margin:"0 0 8px" }}>{platformTopic.title}</h3>
              <p style={{ fontSize:12.5,color:T.textMuted,lineHeight:1.6,margin:"0 0 12px" }}>{platformTopic.callout}</p>
              <div style={{ display:"grid",gap:8,marginBottom:14 }}>
                {platformTopic.focusPanels.map((panel,i)=>(
                  <div key={i} style={{ padding:"10px 12px",borderRadius:14,background:T.bgDeep,border:`1px solid ${platformTopic.color}16` }}>
                    <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.8,color:platformTopic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:4 }}>{panel.label}</div>
                    <div style={{ fontFamily:T.fontDisplay,fontSize:14,fontWeight:700,color:T.text,marginBottom:5 }}>{panel.title}</div>
                    <p style={{ fontSize:11,color:T.textMuted,lineHeight:1.45,margin:0 }}>{panel.body}</p>
                  </div>
                ))}
              </div>
              <p style={{ fontSize:13,color:"#CBD5E1",lineHeight:1.65,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
OverviewScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

function PlatformScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setEntered(true), 50);
    return () => clearTimeout(t);
  }, []);

  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="human" active={entered} />
      <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at 16% 0%,${topic.color}16,transparent 28%),radial-gradient(circle at 86% 16%,${topic.color}10,transparent 22%)`,pointerEvents:"none" }} />
      <div style={{ position:"relative",zIndex:2,maxWidth:1320,margin:"0 auto",padding:"24px 28px 28px" }}>
        <BackBtn onClick={onBack} />

        <div style={{ display:"grid",gap:18 }}>
          <div style={{ display:"grid",gridTemplateColumns:"minmax(0,1fr) minmax(360px,0.95fr)",gap:18,alignItems:"stretch" }}>
            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:26,padding:"22px 24px",border:`1px solid ${topic.color}22`,boxShadow:`0 14px 48px rgba(0,0,0,0.24)`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(20px)",transition:"all 0.65s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:3,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:10 }}>{topic.eyebrow}</div>
              <h1 style={{ fontFamily:T.fontDisplay,fontSize:42,fontWeight:800,color:T.text,lineHeight:0.96,letterSpacing:-1.2,margin:"0 0 10px" }}>{topic.title}</h1>
              <p style={{ fontSize:15,color:topic.colorLight,fontStyle:"italic",lineHeight:1.45,margin:"0 0 12px" }}>{topic.subtitle}</p>
              <p style={{ fontSize:13.5,color:T.textMuted,lineHeight:1.65,margin:"0 0 14px",maxWidth:720 }}>{topic.summary}</p>
              <div style={{ display:"flex",flexWrap:"wrap",gap:8,marginBottom:16 }}>
                {topic.heroPoints.map((point,i)=>(
                  <div key={i} style={{ padding:"7px 10px",borderRadius:999,background:topic.color+"12",border:`1px solid ${topic.color}24`,fontSize:10.5,fontWeight:700,color:T.text }}>{point}</div>
                ))}
              </div>
              <div style={{ display:"grid",gridTemplateColumns:"repeat(3,minmax(0,1fr))",gap:10 }}>
                {topic.focusPanels.map((panel,i)=>(
                  <div key={i} style={{ background:T.bgDeep,borderRadius:16,padding:"13px 13px 14px",borderTop:`2px solid ${topic.color}`,opacity:entered?1:0,transform:entered?"scale(1)":"scale(0.95)",transition:`all 0.45s ${0.18 + i * 0.08}s cubic-bezier(0.34,1.56,0.64,1)` }}>
                    <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.8,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:6 }}>{panel.label}</div>
                    <div style={{ fontFamily:T.fontDisplay,fontSize:15,fontWeight:700,color:T.text,lineHeight:1.15,marginBottom:6 }}>{panel.title}</div>
                    <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.5,margin:0 }}>{panel.body}</p>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:26,padding:"18px",border:`1px solid ${topic.color}20`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(20px)",transition:"all 0.65s 0.08s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:10 }}>One-Pager Snapshot</div>
              <PlatformMockFrame topic={topic} entered={entered} theme={T} />
            </div>
          </div>

          <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.14s cubic-bezier(0.22,1,0.36,1)" }}>
            <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",gap:14,marginBottom:10,flexWrap:"wrap" }}>
              <div>
                <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:5 }}>Capability View</div>
                <div style={{ fontFamily:T.fontDisplay,fontSize:23,fontWeight:700,color:T.text }}>What the platform enables</div>
              </div>
              <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.5,margin:0,maxWidth:320 }}>The original slide’s left-hand cluster is reconstructed here as a cleaner set of capability cards.</p>
            </div>
            <div style={{ display:"grid",gridTemplateColumns:"repeat(4,minmax(0,1fr))",gap:10 }}>
              {topic.capabilities.map((cap,i)=>(
                <div key={i} style={{ background:T.bgDeep,borderRadius:16,padding:"14px 14px 15px",borderTop:`2px solid ${topic.color}`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(12px)",transition:`all 0.45s ${0.18 + i * 0.07}s cubic-bezier(0.22,1,0.36,1)` }}>
                  <div style={{ display:"flex",alignItems:"center",gap:10,marginBottom:8 }}>
                    <div style={{ fontSize:20 }}>{cap.icon}</div>
                    <h3 style={{ fontFamily:T.fontDisplay,fontSize:15,fontWeight:700,color:T.text,margin:0,lineHeight:1.2 }}>{cap.title}</h3>
                  </div>
                  <p style={{ fontSize:11.5,color:T.textMuted,lineHeight:1.55,margin:0 }}>{cap.body}</p>
                </div>
              ))}
            </div>
          </div>

          <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.2s cubic-bezier(0.22,1,0.36,1)" }}>
            <div style={{ display:"flex",alignItems:"center",justifyContent:"space-between",gap:14,marginBottom:14,flexWrap:"wrap" }}>
              <div>
                <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:5 }}>Process Flow & Personas</div>
                <div style={{ fontFamily:T.fontDisplay,fontSize:23,fontWeight:700,color:T.text }}>How the request moves from user to procurement</div>
              </div>
              <div style={{ padding:"7px 10px",borderRadius:999,background:topic.color+"12",border:`1px solid ${topic.color}24`,fontSize:10.5,color:T.textMuted }}>Governed handoff across personas</div>
            </div>
            <div style={{ display:"flex",gap:14,flexWrap:"wrap" }}>
              {topic.lanes.map((lane, index) => (
                <PlatformLane key={index} lane={lane} entered={entered} index={index} theme={T} />
              ))}
            </div>
          </div>

          <div style={{ display:"grid",gridTemplateColumns:"minmax(0,1.1fr) minmax(320px,0.9fr)",gap:18 }}>
            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.26s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:8 }}>Talking Points</div>
              <div style={{ display:"grid",gridTemplateColumns:"repeat(2,minmax(0,1fr))",gap:10 }}>
                {topic.talkingPoints.map((point,i)=>(
                  <div key={i} style={{ padding:"12px 12px 13px",borderRadius:16,background:T.bgDeep,border:`1px solid ${topic.color}16`,fontSize:11.5,color:T.textMuted,lineHeight:1.5 }}>
                    <div style={{ color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,fontSize:10.5,letterSpacing:1.2,textTransform:"uppercase",marginBottom:6 }}>{String(i + 1).padStart(2,"0")}</div>
                    {point}
                  </div>
                ))}
              </div>
            </div>

            <div style={{ background:`linear-gradient(135deg,${T.bgCard},${T.bgDeep})`,borderRadius:22,padding:"18px 18px 16px",border:`1px solid ${topic.color}18`,borderLeft:`4px solid ${topic.color}`,opacity:entered?1:0,transform:entered?"translateY(0)":"translateY(18px)",transition:"all 0.6s 0.32s cubic-bezier(0.22,1,0.36,1)" }}>
              <div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:2.5,color:topic.colorLight,fontWeight:800,fontFamily:T.fontDisplay,marginBottom:8 }}>Bottom Line</div>
              <p style={{ fontSize:13,color:"#CBD5E1",lineHeight:1.7,margin:0 }}>
                <strong style={{ color:topic.colorLight }}>{topic.callout}</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
PlatformScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ═══════════════════════════════════════════
// SPRINT CYCLE: FIGURE-8 (OPTION B)
// ═══════════════════════════════════════════
function Figure8Cycle({ entered }) {
  const canvasRef = useRef(null);
  const progressRef = useRef(0);

  // Node positions on figure-8 — Requirements (index 0) on far left, emphasized
  const W = 860, H = 420;
  const lcx = 280, rcx = 580, cy = 210, lrx = 210, rrx = 210, ry = 155;

  function fig8Pos(t) {
    // t: 0-1, first half = left loop CW, second half = right loop CW
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = sprintNodes.map((n, i) => {
    const t = i / 12;
    return { ...n, ...fig8Pos(t), t, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = W * 2; c.height = H * 2; ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0008) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, W, H);

      // Draw figure-8 path
      ctx.beginPath();
      for (let i = 0; i <= 300; i++) { const p = fig8Pos(i / 300); i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y); }
      ctx.closePath(); ctx.strokeStyle = "rgba(139,92,246,0.1)"; ctx.lineWidth = 2.5; ctx.stroke();

      // Animated comet
      const trailLen = 0.06;
      for (let i = 0; i < 50; i++) {
        const tt = ((prog - (i / 50) * trailLen) + 1) % 1;
        const p = fig8Pos(tt);
        const alpha = (1 - i / 50) * 0.55;
        ctx.beginPath(); ctx.arc(p.x, p.y, 4 - i * 0.06, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139,92,246,${alpha})`; ctx.fill();
      }
      const lead = fig8Pos(prog);
      ctx.beginPath(); ctx.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#A78BFA"; ctx.shadowColor = "#8B5CF6"; ctx.shadowBlur = 18; ctx.fill(); ctx.shadowBlur = 0;

      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered]);

  return (
    <div style={{ position: "relative", width: W, height: H, margin: "0 auto" }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: W, height: H }} />

      {/* Phase labels */}
      <div style={{ position: "absolute", left: lcx - 50, top: 12, fontSize: 10, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: "#8B5CF6", fontFamily: "'Space Grotesk',sans-serif" }}>Phase 1 — Build</div>
      <div style={{ position: "absolute", left: rcx - 55, top: 12, fontSize: 10, textTransform: "uppercase", letterSpacing: 1.5, fontWeight: 700, color: "#0891B2", fontFamily: "'Space Grotesk',sans-serif" }}>Phase 2 — Validate</div>

      {/* Handoff label */}
      <div style={{ position: "absolute", left: (lcx + rcx) / 2 - 30, top: cy - 12, background: "#111827", border: "1px solid rgba(139,92,246,0.3)", borderRadius: 8, padding: "3px 10px", fontSize: 9, color: "#A78BFA", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, fontFamily: "'Space Grotesk',sans-serif", zIndex: 6 }}>Handoff</div>

      {/* Nodes */}
      {nodePositions.map((n, i) => {
        const isAI = n.type === "ai";
        const size = 30;
        return (
          <div key={i} style={{
            position: "absolute", left: n.x - size, top: n.y - size, width: size * 2, height: size * 2,
            borderRadius: "50%", background: isAI ? AI_BG : "#162240",
            border: `2px solid ${isAI ? "#7C3AED" : "#0891B2"}60`,
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
            fontSize: 22, zIndex: 5,
            boxShadow: `0 0 16px ${isAI ? "rgba(139,92,246,0.18)" : "rgba(8,145,178,0.14)"}`,
            opacity: entered ? 1 : 0,
            transform: entered ? "scale(1)" : "scale(0.7)",
            transition: `all 0.4s ${0.15 + i * 0.06}s cubic-bezier(0.34,1.56,0.64,1)`,
          }}>
            {n.icon}
            {/* Badge */}
            <div style={{ position: "absolute", top: -6, right: -6, fontSize: 8, fontWeight: 700, background: isAI ? "#7C3AED" : "#0891B2", color: "#FFF", borderRadius: 6, padding: "1px 5px", fontFamily: "'Space Grotesk',sans-serif" }}>
              {isAI ? "AI" : "👤"}
            </div>
            {/* Label */}
            <div style={{ position: "absolute", top: size * 2 + 5, fontSize: 11, color: "#E2E8F0", textAlign: "center", whiteSpace: "nowrap", fontWeight: 600, fontFamily: "'Space Grotesk',sans-serif" }}>{n.label}</div>
          </div>
        );
      })}
    </div>
  );
}
Figure8Cycle.propTypes = { entered: PropTypes.bool.isRequired };

// ═══════════════════════════════════════════
// SPRINT CYCLE: CIRCULAR RING (OPTION C)
// ═══════════════════════════════════════════
function CircularRingCycle({ entered }) {
  const canvasRef = useRef(null);
  const progressRef = useRef(0);
  const SIZE = 480;
  const cx = SIZE / 2, cy = SIZE / 2, R = 185;

  // Requirements (index 0) at 9 o'clock (left)
  const nodePositions = sprintNodes.map((n, i) => {
    const angle = Math.PI + (i / 12) * Math.PI * 2; // start at left (π), go CW
    return { ...n, x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle), angle, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    c.width = SIZE * 2; c.height = SIZE * 2; ctx.scale(2, 2);
    let raf;
    function draw() {
      progressRef.current = (progressRef.current + 0.0007) % 1;
      const prog = progressRef.current;
      ctx.clearRect(0, 0, SIZE, SIZE);

      // Ring
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(139,92,246,0.08)"; ctx.lineWidth = 3; ctx.stroke();

      // Direction chevrons
      for (let i = 0; i < 12; i++) {
        const a = Math.PI + ((i + 0.5) / 12) * Math.PI * 2;
        const px = cx + R * Math.cos(a), py = cy + R * Math.sin(a);
        const dir = a + Math.PI / 2;
        ctx.save(); ctx.translate(px, py); ctx.rotate(dir);
        ctx.beginPath(); ctx.moveTo(-4, -3); ctx.lineTo(0, 3); ctx.lineTo(4, -3);
        ctx.strokeStyle = "rgba(148,163,184,0.2)"; ctx.lineWidth = 1; ctx.stroke(); ctx.restore();
      }

      // Radar sweep
      const sweepA = Math.PI + prog * Math.PI * 2;
      ctx.beginPath(); ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R + 15, sweepA - 0.5, sweepA); ctx.closePath();
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R + 15);
      g.addColorStop(0, "rgba(139,92,246,0)"); g.addColorStop(1, "rgba(139,92,246,0.12)");
      ctx.fillStyle = g; ctx.fill();

      // Lead dot
      const da = Math.PI + prog * Math.PI * 2;
      const dx = cx + R * Math.cos(da), dy = cy + R * Math.sin(da);
      ctx.beginPath(); ctx.arc(dx, dy, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#A78BFA"; ctx.shadowColor = "#8B5CF6"; ctx.shadowBlur = 16; ctx.fill(); ctx.shadowBlur = 0;

      // Trail
      for (let i = 1; i < 30; i++) {
        const tp = ((prog - i * 0.003) + 1) % 1;
        const ta = Math.PI + tp * Math.PI * 2;
        ctx.beginPath(); ctx.arc(cx + R * Math.cos(ta), cy + R * Math.sin(ta), 3 - i * 0.08, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139,92,246,${(1 - i / 30) * 0.35})`; ctx.fill();
      }

      raf = requestAnimationFrame(draw);
    }
    if (entered) draw();
    return () => cancelAnimationFrame(raf);
  }, [entered]);

  return (
    <div style={{ position: "relative", width: SIZE, height: SIZE, margin: "0 auto" }}>
      <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: SIZE, height: SIZE }} />

      {/* Center hub */}
      <div style={{ position: "absolute", left: cx - 70, top: cy - 55, width: 140, textAlign: "center", zIndex: 4, opacity: entered ? 1 : 0, transition: "opacity 0.6s 0.5s" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#F0F4F8", fontFamily: "'Space Grotesk',sans-serif", marginBottom: 6 }}>AI Sprint Cycle</div>
        <div style={{ fontSize: 10, color: "#94A3B8", lineHeight: 1.4, marginBottom: 8 }}>1-week cadence</div>
        <div style={{ display: "flex", justifyContent: "center", gap: 14 }}>
          <div><div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 18, fontWeight: 700, color: "#22D3EE" }}>~90%</div><div style={{ fontSize: 7, color: "#64748B", textTransform: "uppercase" }}>AI Code</div></div>
          <div><div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 18, fontWeight: 700, color: "#10B981" }}>0</div><div style={{ fontSize: 7, color: "#64748B", textTransform: "uppercase" }}>Defects</div></div>
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 10, marginTop: 8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 4 }}><div style={{ width: 7, height: 7, borderRadius: "50%", background: "#0891B2" }} /><span style={{ fontSize: 8, color: "#94A3B8" }}>Human</span></div>
          <div style={{ display: "flex", alignItems: "center", gap: 4 }}><div style={{ width: 7, height: 7, borderRadius: "50%", background: "#7C3AED" }} /><span style={{ fontSize: 8, color: "#94A3B8" }}>AI</span></div>
        </div>
      </div>

      {/* Nodes */}
      {nodePositions.map((n, i) => {
        const isAI = n.type === "ai";
        const sz = 26;
        const labelR = R + 46;
        const lx = cx + labelR * Math.cos(n.angle);
        const ly = cy + labelR * Math.sin(n.angle);
        return (
          <React.Fragment key={i}>
            <div style={{
              position: "absolute", left: n.x - sz, top: n.y - sz, width: sz * 2, height: sz * 2,
              borderRadius: "50%", background: isAI ? AI_BG : "#162240",
              border: `2px solid ${isAI ? "#7C3AED" : "#0891B2"}60`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 20, zIndex: 5,
              boxShadow: `0 0 14px ${isAI ? "rgba(139,92,246,0.16)" : "rgba(8,145,178,0.12)"}`,
              opacity: entered ? 1 : 0, transform: entered ? "scale(1)" : "scale(0.6)",
              transition: `all 0.4s ${0.2 + i * 0.06}s cubic-bezier(0.34,1.56,0.64,1)`,
            }}>
              {n.icon}
              <div style={{ position: "absolute", top: -5, right: -5, fontSize: 7, fontWeight: 700, background: isAI ? "#7C3AED" : "#0891B2", color: "#FFF", borderRadius: 5, padding: "1px 4px", fontFamily: "'Space Grotesk',sans-serif" }}>
                {isAI ? "AI" : "👤"}
              </div>
            </div>
            <div style={{ position: "absolute", left: lx - 40, top: ly - 7, width: 80, fontSize: 10, color: "#E2E8F0", textAlign: "center", fontWeight: 600, zIndex: 3, fontFamily: "'Space Grotesk',sans-serif", opacity: entered ? 1 : 0, transition: `opacity 0.4s ${0.3 + i * 0.06}s` }}>{n.label}</div>
          </React.Fragment>
        );
      })}
    </div>
  );
}
CircularRingCycle.propTypes = { entered: PropTypes.bool.isRequired };

// ═══════════════════════════════════════════
// SPRINT SCREEN (with B/C toggle)
// ═══════════════════════════════════════════
function SprintScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [entered, setEntered] = useState(false);
  const [layout, setLayout] = useState("fig8");
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="sprint" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "36px 48px" }}>
        <BackBtn onClick={onBack} />

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 24, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(-20px)", transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize: 38, marginBottom: 6, display: "inline-block" }}>
            <span style={{ display: "inline-block", animation: entered ? "spinI 8s linear infinite" : "none" }}>⟳</span>
          </div>
          <style>{`@keyframes spinI { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
          <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 36, fontWeight: 700, color: "#F0F4F8", margin: "0 0 6px" }}>AI Sprint Cycle</h1>
          <p style={{ fontSize: 14, color: topic.colorLight, fontStyle: "italic", margin: "0 0 16px" }}>{topic.subtitle}</p>

          {/* Layout toggle */}
          <div style={{ display: "flex", justifyContent: "center", gap: 8 }}>
            {[["fig8", "Figure-8 Infinity"], ["ring", "Circular Ring"]].map(([k, l]) => (
              <button key={k} onClick={() => setLayout(k)} style={{
                padding: "6px 16px", borderRadius: 20, cursor: "pointer", fontFamily: "'Space Grotesk',sans-serif", fontSize: 12, fontWeight: 600,
                background: layout === k ? "rgba(139,92,246,0.15)" : "rgba(255,255,255,0.05)",
                border: `1px solid ${layout === k ? "#8B5CF6" : "rgba(255,255,255,0.08)"}`,
                color: layout === k ? "#A78BFA" : "#64748B",
              }}>{l}</button>
            ))}
          </div>
        </div>

        {/* Diagram container */}
        <div style={{ background: "#111827", borderRadius: 16, padding: "28px 20px", border: "1px solid rgba(139,92,246,0.12)", maxWidth: layout === "fig8" ? 920 : 540, margin: "0 auto", boxShadow: "0 4px 40px rgba(0,0,0,0.3)", overflow: "hidden" }}>
          {layout === "fig8" && <Figure8Cycle entered={entered} />}
          {layout === "ring" && <CircularRingCycle entered={entered} />}
        </div>

        {/* Callout */}
        <div style={{ marginTop: 24, background: "#162240", borderRadius: 10, padding: "16px 28px", borderLeft: "4px solid #8B5CF6", display: "flex", alignItems: "center", gap: 16, maxWidth: 920, marginLeft: "auto", marginRight: "auto", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.5s" }}>
          <div style={{ fontSize: 22, color: "#8B5CF6" }}>⟳</div>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: "#A78BFA" }}>{topic.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}
SprintScreen.propTypes = {
  topic: topicPropType.isRequired,
  onBack: PropTypes.func.isRequired,
};

// ═══════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════

const AI_BG = "#1E1B4B";

export default function App() {
  const [theme, setTheme] = useState(null);
  const [introDone, setIntroDone] = useState(false);
  const [active, setActive] = useState(null);
  const [transitioning, setTransitioning] = useState(false);
  const [hovered, setHovered] = useState(null);
  const [comet, setComet] = useState({ active: false, from: null, color: null, targetId: null });

  const handleSelect = (id, pos) => {
    const topic = topics.find(t => t.id === id);
    setTransitioning(true);
    setComet({ active: true, from: pos, color: topic.color, targetId: id });
  };
  const cometRef = useRef(comet);
  cometRef.current = comet;
  const handleCometDone = useCallback(() => {
    setActive(cometRef.current.targetId);
    setComet({ active: false, from: null, color: null, targetId: null });
    setTransitioning(false);
  }, []);
  const handleBack = () => { setTransitioning(true); setTimeout(() => { setActive(null); setTransitioning(false); }, 350); };
  const activeTopic = topics.find(t => t.id === active);
  const primaryTopics = topics.filter((t) => !t.optional);
  const optionalPlatform = topics.find((t) => t.id === "platform");

  // Theme selector gate
  if (!theme) return <ThemeSelector onSelect={(t) => setTheme(t)} />;

  const T = theme;

  return (
    <ThemeCtx.Provider value={T}>
    <div style={{ fontFamily: T.fontBody, minHeight: "100vh", background: T.bg, opacity: (transitioning && !comet.active) ? 0 : 1, transition: "opacity 0.35s ease" }}>
      <link href={T.fontsUrl} rel="stylesheet" />
      <CometTransition from={comet.from} color={comet.color} active={comet.active} onDone={handleCometDone} />
      {!introDone && <ThematicIntro onComplete={() => setIntroDone(true)} />}
      {!active && introDone && (
        <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center", padding: "40px 48px", opacity: comet.active ? 0 : 1, transition: "opacity 0.4s ease" }}>
          <div style={{ marginBottom: 32 }}>
            <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 3, color: T.textDim, fontFamily: T.fontDisplay, fontWeight: 500, marginBottom: 10 }}>AI-Assisted Delivery</div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 44, fontWeight: 700, color: T.text, margin: "0 0 10px", letterSpacing: -1, lineHeight: 1.05 }}>
              GenAI Transformation<br /><span style={{ background: `linear-gradient(90deg,${T.gradient[0]},${T.gradient[1]})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Advocacy Deck</span>
            </h1>
            <p style={{ fontSize: 15, color: T.textDim, margin: 0, maxWidth: 760 }}>Five core pages. One clean storyline. Open the optional Service Platform one-pager from the takeaways section below.</p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 18 }}>
            {primaryTopics.map(t => <LandingTile key={t.id} topic={t} onClick={handleSelect} hovered={hovered} onHover={setHovered} />)}
          </div>

          <div style={{ marginTop: 26, display: "grid", gridTemplateColumns: "minmax(0,0.95fr) minmax(320px,1.05fr)", gap: 18, alignItems: "stretch" }}>
            <div style={{ background: `linear-gradient(135deg, ${T.bgCard}, ${T.bgDeep})`, borderRadius: 18, padding: "18px 20px", border: `1px solid ${T.textDim}20` }}>
              <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 2.5, color: T.accent, fontFamily: T.fontDisplay, fontWeight: 700, marginBottom: 10 }}>Takeaways</div>
              <div style={{ display: "grid", gap: 10 }}>
                {[
                  "Lead with the mission need, then show how the operating model keeps approvals and procurement governed.",
                  "Use Human in the Loop and Hurdles as proof that speed came from stronger review discipline, not weaker controls.",
                  "Close with the sprint mechanics and scale path so the audience sees a repeatable model, not a one-off success.",
                ].map((point, i) => (
                  <div key={i} style={{ borderRadius: 14, padding: "12px 13px", background: T.bgDeep, border: `1px solid ${T.textDim}18`, fontSize: 12, color: T.textMuted, lineHeight: 1.55 }}>
                    <span style={{ color: T.accent, fontWeight: 800, fontFamily: T.fontDisplay, marginRight: 8 }}>{String(i + 1).padStart(2, "0")}</span>
                    {point}
                  </div>
                ))}
              </div>
            </div>

            {optionalPlatform && <OptionalDeckLink topic={optionalPlatform} onClick={handleSelect} hovered={hovered} onHover={setHovered} />}
          </div>

          <div style={{ display: "flex", gap: 36, marginTop: 28, paddingTop: 20, borderTop: `1px solid ${T.border || "rgba(255,255,255,0.06)"}`, flexWrap: "wrap", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", gap: 36, flexWrap: "wrap" }}>
              {[{ val: "~40%", lbl: "Productivity Uplift" }, { val: "2 mo", lbl: "Prototype → Production" }, { val: "0", lbl: "Critical Defects" }, { val: "~90%", lbl: "AI-Assisted Code" }, { val: "~95%", lbl: "Sprint Predictability" }, { val: "1 wk", lbl: "Sprint Cadence" }].map((s, i) => (
                <div key={i}><div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: 700, color: T.accent }}>{s.val}</div><div style={{ fontSize: 10, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{s.lbl}</div></div>
              ))}
            </div>
            <button onClick={() => setTheme(null)} style={{ background: T.bgCard, border: `1px solid ${T.textDim}30`, borderRadius: 8, padding: "6px 14px", fontSize: 11, color: T.textDim, cursor: "pointer", fontFamily: T.fontBody }}>{T.name} ✎</button>
          </div>
        </div>
      )}
      {active === "overview" && <OverviewScreen topic={activeTopic} onBack={handleBack} />}
      {active === "human" && <HumanScreen topic={activeTopic} onBack={handleBack} />}
      {active === "hurdles" && <HurdlesScreen topic={activeTopic} onBack={handleBack} />}
      {active === "future" && <FutureScreen topic={activeTopic} onBack={handleBack} />}
      {active === "platform" && <PlatformScreen topic={activeTopic} onBack={handleBack} />}
      {active === "sprint" && <SprintScreen topic={activeTopic} onBack={handleBack} />}
    </div>
    </ThemeCtx.Provider>
  );
}
