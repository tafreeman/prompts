import { useState, useEffect, useRef, useCallback, createContext, useContext } from "react";

const THEMES = [
  { id: "midnight-teal", name: "Midnight Teal", vibe: "Current Default", fontDisplay: "'Space Grotesk',sans-serif", fontBody: "'DM Sans',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap", bg: "#0B1426", bgCard: "#162240", bgDeep: "#111827", text: "#F0F4F8", textMuted: "#CBD5E1", textDim: "#64748B", accent: "#22D3EE", accentGlow: "rgba(8,145,178,0.3)", gradient: ["#22D3EE", "#10B981"] },
  { id: "obsidian-ember", name: "Obsidian & Ember", vibe: "Editorial / Luxury", fontDisplay: "'Playfair Display',serif", fontBody: "'Source Sans 3',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap", bg: "#1A1A1E", bgCard: "#242428", bgDeep: "#2C2C32", text: "#E8E4DF", textMuted: "#9B9590", textDim: "#6B6560", accent: "#D4A853", accentGlow: "rgba(212,168,83,0.25)", gradient: ["#D4A853", "#C75B39"] },
  { id: "arctic-steel", name: "Arctic Steel", vibe: "Industrial Nordic", fontDisplay: "'JetBrains Mono',monospace", fontBody: "'Nunito Sans',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap", bg: "#0F1318", bgCard: "#171D24", bgDeep: "#1E2630", text: "#D6DDE6", textMuted: "#7B8EA3", textDim: "#4E6178", accent: "#4FC3F7", accentGlow: "rgba(79,195,247,0.2)", gradient: ["#4FC3F7", "#B2EBF2"] },
  { id: "midnight-verdant", name: "Midnight Verdant", vibe: "Organic Tech", fontDisplay: "'Outfit',sans-serif", fontBody: "'Karla',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap", bg: "#0A1628", bgCard: "#112240", bgDeep: "#152A4E", text: "#CCD6F6", textMuted: "#8892B0", textDim: "#5A6480", accent: "#64FFDA", accentGlow: "rgba(100,255,218,0.18)", gradient: ["#64FFDA", "#48BB78"] },
  { id: "neon-noir", name: "Neon Noir", vibe: "Cyberpunk / Bold", fontDisplay: "'Chakra Petch',sans-serif", fontBody: "'Barlow',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap", bg: "#050508", bgCard: "#0D0D12", bgDeep: "#14141C", text: "#EAEAF0", textMuted: "#8585A0", textDim: "#55556E", accent: "#00E5FF", accentGlow: "rgba(0,229,255,0.2)", gradient: ["#00E5FF", "#FF2D95"] },
  { id: "paper-ink", name: "Paper & Ink", vibe: "Light Editorial", fontDisplay: "'DM Serif Display',serif", fontBody: "'Atkinson Hyperlegible',sans-serif", fontsUrl: "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap", bg: "#FAF8F5", bgCard: "#FFFFFF", bgDeep: "#F0EDE8", text: "#1A1A2E", textMuted: "#5C5C6F", textDim: "#8E8E9F", accent: "#1E40AF", accentGlow: "rgba(30,64,175,0.12)", gradient: ["#1E40AF", "#7C3AED"] },
];

const ThemeCtx = createContext(THEMES[0]);

const topics = [
  {
    id: "hurdles", num: "02", title: "Hurdles We Overcame",
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
    id: "human", num: "01", title: "Human in the Loop",
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
    id: "sprint", num: "04", title: "AI Sprint Cycle",
    subtitle: "Human checkpoints at every stage of AI-assisted delivery",
    color: "#8B5CF6", colorLight: "#A78BFA", colorGlow: "rgba(139,92,246,0.3)", icon: "⟳",
    callout: "The AI modified sprint cycle includes numerous human-in-the-loop checkpoints. Development included rapid iterations and adherence to Agile best practices.",
  },
  {
    id: "future", num: "03", title: "Looking Ahead",
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
    const n = type === "hurdles" ? 60 : type === "sprint" ? 40 : 30;
    for (let i = 0; i < n; i++) pRef.current.push({ x: Math.random()*W, y: Math.random()*H, vx: type==="hurdles"?(Math.random()-0.3)*3:(Math.random()-0.5)*0.5, vy: type==="hurdles"?-Math.random()*4-1:(Math.random()-0.5)*0.5, r: type==="hurdles"?Math.random()*3+1:Math.random()*2+1, o: Math.random()*0.5+0.15, life: Math.random()*100 });
    function draw() {
      ctx.clearRect(0,0,W,H);
      pRef.current.forEach(p => {
        p.life++;
        if(type==="hurdles"){p.x+=p.vx;p.y+=p.vy;p.vy-=0.02;if(p.y<-10||p.x<-10||p.x>W+10){p.x=Math.random()*W;p.y=H+10;p.vy=-Math.random()*4-1;p.vx=(Math.random()-0.3)*3;}}
        else if(type==="human"){p.x+=Math.sin(p.life*0.015)*0.3;p.y+=Math.cos(p.life*0.012)*0.3;}
        else if(type==="sprint"){const cx=W/2,cy=H/2,a=Math.atan2(p.y-cy,p.x-cx);p.x+=Math.cos(a+Math.PI/2)*0.35;p.y+=Math.sin(a+Math.PI/2)*0.35;const d=Math.sqrt((p.x-cx)**2+(p.y-cy)**2);if(d>Math.max(W,H)*0.55){p.x=cx+(Math.random()-0.5)*W*0.4;p.y=cy+(Math.random()-0.5)*H*0.4;}}
        else{p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;}
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=color+Math.round(p.o*255).toString(16).padStart(2,"0");ctx.fill();
      });
      if(type==="human"){const pts=pRef.current;for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);if(d<120){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=color+Math.round((1-d/120)*40).toString(16).padStart(2,"0");ctx.lineWidth=0.5;ctx.stroke();}}}
      animRef.current=requestAnimationFrame(draw);
    }
    if(active) draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, type, active]);
  return <canvas ref={canvasRef} style={{ position:"absolute",inset:0,width:"100%",height:"100%",pointerEvents:"none",opacity:active?1:0,transition:"opacity 0.8s" }}/>;
}

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

  const tx = (typeof window !== "undefined" ? window.innerWidth / 2 : 500) - from.x;
  const ty = (typeof window !== "undefined" ? window.innerHeight / 2 : 400) - from.y;

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
      {[...Array(8)].map((_, i) => (
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

// ─── THEMATIC INTRO ───
function ThematicIntro({ onComplete }) {
  const [phase, setPhase] = useState(0);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 100),   // stars appear + warp
      setTimeout(() => setPhase(2), 1200),  // comet launches
      setTimeout(() => setPhase(3), 2200),  // title appears
      setTimeout(() => setPhase(4), 3400),  // impact burst
      setTimeout(() => { setPhase(5); onCompleteRef.current(); }, 4200),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  // Generate static star positions once
  const starsRef = useRef(Array.from({ length: 50 }, () => ({
    x: 50 + (Math.random() - 0.5) * 80,
    y: 50 + (Math.random() - 0.5) * 80,
    s: Math.random() * 2 + 1,
    d: Math.random() * 0.8,
    angle: Math.random() * 360,
    dist: Math.random() * 40 + 10,
  })));

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 200, background: "#020810",
      overflow: "hidden",
      opacity: phase >= 5 ? 0 : 1, transition: "opacity 0.6s ease",
    }}>
      <style>{`
        @keyframes warpStar {
          0% { transform: translate(-50%,-50%) scale(1); opacity: 0.6; }
          100% { transform: translate(-50%,-50%) scale(3) translateZ(0); opacity: 0; }
        }
        @keyframes cometFly {
          0% { transform: translate(0, -120vh) scale(0.3); opacity: 0; }
          15% { opacity: 1; }
          70% { transform: translate(0, 0) scale(1); opacity: 1; }
          100% { transform: translate(0, 0) scale(0); opacity: 0; }
        }
        @keyframes impactRing {
          0% { transform: translate(-50%,-50%) scale(0); opacity: 0.8; }
          60% { opacity: 0.4; }
          100% { transform: translate(-50%,-50%) scale(4); opacity: 0; }
        }
        @keyframes fadeUp {
          0% { opacity: 0; transform: translateY(20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes streakLine {
          0% { transform: scaleY(0); opacity: 0; }
          20% { opacity: 0.4; }
          100% { transform: scaleY(1); opacity: 0; }
        }
      `}</style>

      {/* Warp stars */}
      {starsRef.current.map((star, i) => (
        <div key={i} style={{
          position: "absolute",
          left: `${star.x}%`, top: `${star.y}%`,
          width: star.s, height: star.s,
          borderRadius: "50%",
          background: `hsl(${190 + Math.random() * 40}, 80%, ${70 + Math.random() * 20}%)`,
          animation: phase >= 1 ? `warpStar ${1.5 + star.d}s ${star.d * 0.5}s ease-out forwards` : "none",
          opacity: 0,
        }} />
      ))}

      {/* Speed streaks */}
      {phase >= 1 && [...Array(12)].map((_, i) => (
        <div key={`s${i}`} style={{
          position: "absolute",
          left: `${15 + Math.random() * 70}%`,
          top: "0%",
          width: 1,
          height: "100%",
          background: `linear-gradient(180deg, transparent, rgba(34,211,238,${0.1 + Math.random() * 0.15}), transparent)`,
          transformOrigin: "top center",
          animation: `streakLine ${0.8 + Math.random() * 0.6}s ${i * 0.08}s ease-out forwards`,
        }} />
      ))}

      {/* Comet */}
      {phase >= 2 && (
        <div style={{
          position: "absolute", left: "50%", top: "50%",
          marginLeft: -10, marginTop: -10,
          width: 20, height: 20,
          borderRadius: "50%",
          background: "radial-gradient(circle, #FFFFFF 20%, #22D3EE 60%, transparent 100%)",
          boxShadow: "0 0 40px 15px rgba(34,211,238,0.5), 0 0 80px 30px rgba(34,211,238,0.2)",
          animation: "cometFly 1.2s cubic-bezier(0.16,1,0.3,1) forwards",
        }}>
          {/* Comet tail */}
          <div style={{
            position: "absolute", left: "50%", bottom: "100%",
            marginLeft: -3, width: 6, height: 120,
            background: "linear-gradient(180deg, transparent, rgba(34,211,238,0.4), rgba(255,255,255,0.6))",
            borderRadius: 3, filter: "blur(2px)",
          }} />
        </div>
      )}

      {/* Impact burst */}
      {phase >= 4 && (
        <>
          <div style={{
            position: "absolute", left: "50%", top: "50%",
            width: 200, height: 200,
            borderRadius: "50%",
            border: "2px solid rgba(34,211,238,0.5)",
            animation: "impactRing 0.8s ease-out forwards",
          }} />
          <div style={{
            position: "absolute", left: "50%", top: "50%",
            width: 100, height: 100,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(255,255,255,0.3), transparent 70%)",
            animation: "impactRing 0.6s 0.1s ease-out forwards",
          }} />
        </>
      )}

      {/* Title text — appears after comet lands */}
      {phase >= 3 && (
        <div style={{
          position: "absolute", inset: 0,
          display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
          zIndex: 10,
        }}>
          <div style={{
            fontSize: 11, textTransform: "uppercase", letterSpacing: 4, color: "#64748B",
            fontFamily: "'Space Grotesk',sans-serif", marginBottom: 12,
            animation: "fadeUp 0.6s 0.1s ease both",
          }}>AI-Assisted Delivery</div>
          <h1 style={{
            fontFamily: "'Space Grotesk',sans-serif", fontSize: 48, fontWeight: 700,
            color: "#F0F4F8", textAlign: "center", margin: "0 0 8px", letterSpacing: -1,
            animation: "fadeUp 0.6s 0.2s ease both",
          }}>GenAI Transformation</h1>
          <p style={{
            fontSize: 16, margin: "0 0 28px", textAlign: "center",
            animation: "fadeUp 0.5s 0.4s ease both",
          }}>
            <span style={{ background: "linear-gradient(90deg, #22D3EE, #10B981)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              From prototype to production in 2 months
            </span>
          </p>
          <div style={{ display: "flex", gap: 32, animation: "fadeUp 0.5s 0.6s ease both" }}>
            {[
              { val: "~40%", lbl: "Uplift", color: "#22D3EE" },
              { val: "2 mo", lbl: "Delivery", color: "#34D399" },
              { val: "0", lbl: "Defects", color: "#10B981" },
              { val: "~90%", lbl: "AI Code", color: "#A78BFA" },
            ].map((s, i) => (
              <div key={i} style={{ textAlign: "center" }}>
                <div style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: 24, fontWeight: 700, color: s.color }}>{s.val}</div>
                <div style={{ fontSize: 9, color: "#64748B", textTransform: "uppercase", letterSpacing: 1 }}>{s.lbl}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

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
            <div key={t.id}
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
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── BACK BUTTON ───
function BackBtn({ onClick }) {
  const T = useContext(ThemeCtx);
  return <button onClick={onClick} style={{ background:"none",border:"none",color:T.textDim,fontSize:13,cursor:"pointer",fontFamily:T.fontDisplay,marginBottom:20,display:"flex",alignItems:"center",gap:6 }}><span>←</span> Back</button>;
}

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
          <p style={{ fontSize:16,color:"#CBD5E1",lineHeight:1.6,margin:0,maxWidth:600,marginLeft:"auto",marginRight:"auto" }}><span style={{ color:topic.colorLight,fontWeight:700 }}>"{topic.callout}"</span></p>
        </div>
      </div>
    </div>
  );
}

// ─── HURDLES SCREEN ───
function HurdlesScreen({ topic, onBack }) {
  const T = useContext(ThemeCtx);
  const [e,setE]=useState(false);const [vc,setVc]=useState(0);
  useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  useEffect(()=>{if(!e)return;const iv=topic.cards.map((_,i)=>setTimeout(()=>setVc(i+1),400+i*250));return()=>iv.forEach(clearTimeout)},[e,topic.cards.length]);
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
          {topic.cards.map((c,i)=>{const v=i<vc,fl=i%2===0;return(
            <div key={i} style={{ background:"#162240",borderRadius:12,padding:"24px 28px",borderTop:`3px solid ${topic.color}`,position:"relative",overflow:"hidden",opacity:v?1:0,transform:v?"translateX(0) scale(1)":`translateX(${fl?"-60px":"60px"}) scale(0.92)`,transition:"all 0.45s cubic-bezier(0.34,1.56,0.64,1)" }}>
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
            <p style={{ fontSize: 15, color: T.textDim, margin: 0, maxWidth: 600 }}>Four narratives. One story. Select a topic to explore.</p>
          </div>
          <div style={{ display: "flex", gap: 18 }}>
            {topics.map(t => <LandingTile key={t.id} topic={t} onClick={handleSelect} hovered={hovered} onHover={setHovered} />)}
          </div>
          <div style={{ display: "flex", gap: 36, marginTop: 32, paddingTop: 20, borderTop: `1px solid ${T.border || "rgba(255,255,255,0.06)"}`, flexWrap: "wrap", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", gap: 36, flexWrap: "wrap" }}>
              {[{ val: "~40%", lbl: "Productivity Uplift" }, { val: "2 mo", lbl: "Prototype → Production" }, { val: "0", lbl: "Critical Defects" }, { val: "~90%", lbl: "AI-Assisted Code" }, { val: "~95%", lbl: "Sprint Predictability" }, { val: "1 wk", lbl: "Sprint Cadence" }].map((s, i) => (
                <div key={i}><div style={{ fontFamily: T.fontDisplay, fontSize: 22, fontWeight: 700, color: T.accent }}>{s.val}</div><div style={{ fontSize: 10, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{s.lbl}</div></div>
              ))}
            </div>
            <button onClick={() => setTheme(null)} style={{ background: T.bgCard, border: `1px solid ${T.textDim}30`, borderRadius: 8, padding: "6px 14px", fontSize: 11, color: T.textDim, cursor: "pointer", fontFamily: T.fontBody }}>{T.name} ✎</button>
          </div>
        </div>
      )}
      {active === "human" && <HumanScreen topic={activeTopic} onBack={handleBack} />}
      {active === "hurdles" && <HurdlesScreen topic={activeTopic} onBack={handleBack} />}
      {active === "future" && <FutureScreen topic={activeTopic} onBack={handleBack} />}
      {active === "sprint" && <SprintScreen topic={activeTopic} onBack={handleBack} />}
    </div>
    </ThemeCtx.Provider>
  );
}
