import React, { useRef, useEffect } from "react";

const AI_BG = "#1E1B4B";

interface CycleNode {
  icon: string;
  label: string;
  type: string;
}

interface CircularRingCycleProps {
  entered: boolean;
  nodes: CycleNode[];
}

export function CircularRingCycle({ entered, nodes }: CircularRingCycleProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const progressRef = useRef<number>(0);
  const SIZE = 480;
  const cx = SIZE / 2, cy = SIZE / 2, R = 185;

  // Requirements (index 0) at 9 o'clock (left)
  const nodePositions = nodes.map((n, i) => {
    const angle = Math.PI + (i / Math.max(nodes.length, 1)) * Math.PI * 2; // start at left (π), go CW
    return { ...n, x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle), angle, i };
  });

  useEffect(() => {
    const c = canvasRef.current; if (!c) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    c.width = SIZE * 2; c.height = SIZE * 2; ctx.scale(2, 2);
    let raf: number;
    function draw() {
      progressRef.current = (progressRef.current + 0.0007) % 1;
      const prog = progressRef.current;
      ctx!.clearRect(0, 0, SIZE, SIZE);

      // Ring
      ctx!.beginPath(); ctx!.arc(cx, cy, R, 0, Math.PI * 2);
      ctx!.strokeStyle = "rgba(139,92,246,0.08)"; ctx!.lineWidth = 3; ctx!.stroke();

      // Direction chevrons
      for (let i = 0; i < 12; i++) {
        const a = Math.PI + ((i + 0.5) / 12) * Math.PI * 2;
        const px = cx + R * Math.cos(a), py = cy + R * Math.sin(a);
        const dir = a + Math.PI / 2;
        ctx!.save(); ctx!.translate(px, py); ctx!.rotate(dir);
        ctx!.beginPath(); ctx!.moveTo(-4, -3); ctx!.lineTo(0, 3); ctx!.lineTo(4, -3);
        ctx!.strokeStyle = "rgba(148,163,184,0.2)"; ctx!.lineWidth = 1; ctx!.stroke(); ctx!.restore();
      }

      // Radar sweep
      const sweepA = Math.PI + prog * Math.PI * 2;
      ctx!.beginPath(); ctx!.moveTo(cx, cy);
      ctx!.arc(cx, cy, R + 15, sweepA - 0.5, sweepA); ctx!.closePath();
      const g = ctx!.createRadialGradient(cx, cy, 0, cx, cy, R + 15);
      g.addColorStop(0, "rgba(139,92,246,0)"); g.addColorStop(1, "rgba(139,92,246,0.12)");
      ctx!.fillStyle = g; ctx!.fill();

      // Lead dot
      const da = Math.PI + prog * Math.PI * 2;
      const dx = cx + R * Math.cos(da), dy = cy + R * Math.sin(da);
      ctx!.beginPath(); ctx!.arc(dx, dy, 5, 0, Math.PI * 2);
      ctx!.fillStyle = "#A78BFA"; ctx!.shadowColor = "#8B5CF6"; ctx!.shadowBlur = 16; ctx!.fill(); ctx!.shadowBlur = 0;

      // Trail
      for (let i = 1; i < 30; i++) {
        const tp = ((prog - i * 0.003) + 1) % 1;
        const ta = Math.PI + tp * Math.PI * 2;
        ctx!.beginPath(); ctx!.arc(cx + R * Math.cos(ta), cy + R * Math.sin(ta), 3 - i * 0.08, 0, Math.PI * 2);
        ctx!.fillStyle = `rgba(139,92,246,${(1 - i / 30) * 0.35})`; ctx!.fill();
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

export default CircularRingCycle;
