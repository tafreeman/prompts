/**
 * ThematicIntro — full-screen cinematic intro sequence.
 *
 * Extracted from the monolith (genai_advocacy_hub_13.jsx lines 665-849).
 */

import React, { useState, useEffect, useRef } from "react";

/* -- entropy helper -- */

let fallbackEntropyCursor = 0;
const FALLBACK_ENTROPY_DIVISOR = 997;

function getRandomUnit(): number {
  const cryptoApi = globalThis.crypto;
  if (cryptoApi && typeof cryptoApi.getRandomValues === "function") {
    return cryptoApi.getRandomValues(new Uint32Array(1))[0] / 0x100000000;
  }
  fallbackEntropyCursor =
    (fallbackEntropyCursor + 619) % FALLBACK_ENTROPY_DIVISOR;
  return fallbackEntropyCursor / FALLBACK_ENTROPY_DIVISOR;
}

/* -- types -- */

interface IntroStat {
  val: string;
  lbl: string;
  color: string;
}

interface DeckIntroProps {
  introBrandLine?: string;
  introTitle?: string;
  introSubtitle?: string;
  introStats?: IntroStat[];
}

interface ThematicIntroProps {
  deck?: DeckIntroProps | null;
  onComplete: () => void;
}

interface StarData {
  x: number;
  y: number;
  s: number;
  d: number;
  hue: number;
  lightness: number;
}

interface StreakData {
  left: number;
  alpha: number;
  duration: number;
}

/* -- fallback intro stats -- */
const DEFAULT_INTRO_STATS: IntroStat[] = [
  { val: "5", lbl: "Modules", color: "#22D3EE" },
  { val: "24", lbl: "Slides", color: "#10B981" },
  { val: "∞", lbl: "Impact", color: "#F59E0B" },
];

function ThematicIntro({ deck, onComplete }: ThematicIntroProps) {
  const [phase, setPhase] = useState(0);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  const introStats = deck?.introStats || DEFAULT_INTRO_STATS;

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
  const starsRef = useRef<StarData[]>(Array.from({ length: 50 }, () => ({
    x: 50 + (getRandomUnit() - 0.5) * 80,
    y: 50 + (getRandomUnit() - 0.5) * 80,
    s: getRandomUnit() * 2 + 1,
    d: getRandomUnit() * 0.8,
    hue: 190 + getRandomUnit() * 40,
    lightness: 70 + getRandomUnit() * 20,
  })));
  const streaksRef = useRef<StreakData[]>(Array.from({ length: 12 }, () => ({
    left: 15 + getRandomUnit() * 70,
    alpha: 0.1 + getRandomUnit() * 0.15,
    duration: 0.8 + getRandomUnit() * 0.6,
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
          background: `hsl(${star.hue}, 80%, ${star.lightness}%)`,
          animation: phase >= 1 ? `warpStar ${1.5 + star.d}s ${star.d * 0.5}s ease-out forwards` : "none",
          opacity: 0,
        }} />
      ))}

      {/* Speed streaks */}
      {phase >= 1 && streaksRef.current.map((streak, i) => (
        <div key={`s${i}`} style={{
          position: "absolute",
          left: `${streak.left}%`,
          top: "0%",
          width: 1,
          height: "100%",
          background: `linear-gradient(180deg, transparent, rgba(34,211,238,${streak.alpha}), transparent)`,
          transformOrigin: "top center",
          animation: `streakLine ${streak.duration}s ${i * 0.08}s ease-out forwards`,
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
          }}>{deck?.introBrandLine || "GenAI Transformation"}</div>
          <h1 style={{
            fontFamily: "'Space Grotesk',sans-serif", fontSize: 48, fontWeight: 700,
            color: "#F0F4F8", textAlign: "center", margin: "0 0 8px", letterSpacing: -1,
            animation: "fadeUp 0.6s 0.2s ease both",
          }}>{deck?.introTitle || "Advocacy Hub"}</h1>
          <p style={{
            fontSize: 16, margin: "0 0 28px", textAlign: "center",
            animation: "fadeUp 0.5s 0.4s ease both",
          }}>
            <span style={{ background: "linear-gradient(90deg, #22D3EE, #10B981)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              {deck?.introSubtitle || "Explore the future of AI"}
            </span>
          </p>
          <div style={{ display: "flex", gap: 32, animation: "fadeUp 0.5s 0.6s ease both" }}>
            {introStats.map((s) => (
              <div key={`${s.lbl}-${s.val}`} style={{ textAlign: "center" }}>
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

export default ThematicIntro;
