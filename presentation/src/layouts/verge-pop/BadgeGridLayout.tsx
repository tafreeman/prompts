/**
 * BadgeGridLayout — Verge-style layout with colored badge pills in a grid.
 * Layout ID: "badge-grid"
 */

import React, { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  callout?: string;
  [key: string]: unknown;
}

interface LayoutProps {
  topic: Topic;
  onBack: () => void;
}

export function BadgeGridLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 16px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        {topic.question && (
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: T.text, borderRadius: C.cardRadius, padding: "10px 16px", marginBottom: 24 }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: 700, color: T.bg }}>Q:</span>
            <span style={{ fontFamily: T.fontBody, fontSize: 13, color: T.bg }}>{topic.question as string}</span>
          </div>
        )}
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min((topic.badges as unknown[] || []).length, 5)}, 1fr)`, gap: 10, marginBottom: 24 }}>
          {(topic.badges as Array<{ bgColor?: string; icon: string; name: string; value: string }> || []).map((badge, idx) => {
            const dark = badge.bgColor === "#000000";
            return (
              <div key={idx} style={{
                display: "flex", alignItems: "center", gap: 8,
                background: badge.bgColor || topic.color,
                borderRadius: C.pillRadius > 20 ? 12 : C.pillRadius, padding: "10px 14px",
                border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
                opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(12px)",
                transition: `all 0.35s ${0.02 + idx * 0.025}s ease`,
              }}>
                <span style={{ fontSize: 18 }}>{badge.icon}</span>
                <span style={{ fontFamily: T.fontDisplay, fontSize: 10, fontWeight: 700, color: dark ? "#FFF" : "#000", letterSpacing: 1, textTransform: "uppercase", flex: 1 }}>{badge.name}</span>
                <span style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: dark ? "#FFF" : "#000" }}>{badge.value}</span>
              </div>
            );
          })}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default BadgeGridLayout;
