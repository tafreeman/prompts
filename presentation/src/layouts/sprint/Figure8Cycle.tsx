import React, { useRef, useEffect } from "react";

const AI_BG = "#1E1B4B";

interface CycleNode {
  icon: string;
  label: string;
  type: string;
}

interface Figure8CycleProps {
  entered: boolean;
  nodes: CycleNode[];
}

export function Figure8Cycle({ entered, nodes }: Figure8CycleProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const progressRef = useRef<number>(0);

  // Node positions on figure-8 — Requirements (index 0) on far left, emphasized
  const W = 860, H = 420;
  const lcx = 280, rcx = 580, cy = 210, lrx = 210, rrx = 210, ry = 155;

  function fig8Pos(t: number) {
    // t: 0-1, first half = left loop CW, second half = right loop CW
    if (t < 0.5) {
      const a = -Math.PI + t * 2 * Math.PI * 2;
      return { x: lcx + lrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    } else {
      const a = Math.PI - (t - 0.5) * 2 * Math.PI * 2;
      return { x: rcx + rrx * Math.cos(a), y: cy + ry * Math.sin(a) };
    }
  }

  const nodePositions = nodes.map((n, i) => {
    const t = i / Math.max(nodes.length, 1);
    return { ...n, ...fig8Pos(t), t, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    c.width = W * 2; c.height = H * 2; ctx.scale(2, 2);
    let raf: number;
    function draw() {
      progressRef.current = (progressRef.current + 0.0008) % 1;
      const prog = progressRef.current;
      ctx!.clearRect(0, 0, W, H);

      // Draw figure-8 path
      ctx!.beginPath();
      for (let i = 0; i <= 300; i++) { const p = fig8Pos(i / 300); i === 0 ? ctx!.moveTo(p.x, p.y) : ctx!.lineTo(p.x, p.y); }
      ctx!.closePath(); ctx!.strokeStyle = "rgba(139,92,246,0.1)"; ctx!.lineWidth = 2.5; ctx!.stroke();

      // Animated comet
      const trailLen = 0.06;
      for (let i = 0; i < 50; i++) {
        const tt = ((prog - (i / 50) * trailLen) + 1) % 1;
        const p = fig8Pos(tt);
        const alpha = (1 - i / 50) * 0.55;
        ctx!.beginPath(); ctx!.arc(p.x, p.y, 4 - i * 0.06, 0, Math.PI * 2);
        ctx!.fillStyle = `rgba(139,92,246,${alpha})`; ctx!.fill();
      }
      const lead = fig8Pos(prog);
      ctx!.beginPath(); ctx!.arc(lead.x, lead.y, 6, 0, Math.PI * 2);
      ctx!.fillStyle = "#A78BFA"; ctx!.shadowColor = "#8B5CF6"; ctx!.shadowBlur = 18; ctx!.fill(); ctx!.shadowBlur = 0;

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

export default Figure8Cycle;
