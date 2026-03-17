/**
 * StatHeroLayout — Verge-style layout with large stat cards and bold hero title.
 * Layout ID: "stat-hero"
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

export function StatHeroLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        {topic.question && (
          <div style={{ float: "right", maxWidth: 320, background: T.text, borderRadius: C.cardRadius, padding: "14px 18px", marginLeft: 24, marginBottom: 16 }}>
            <span style={{ fontFamily: T.fontDisplay, fontSize: 20, fontWeight: 700, color: T.bg }}>Q: </span>
            <span style={{ fontFamily: T.fontBody, fontSize: 13, color: T.bg, lineHeight: 1.5 }}>{topic.question as string}</span>
          </div>
        )}
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 48, fontWeight: C.headingWeight, color: T.text, margin: "0 0 16px", lineHeight: 1.1, maxWidth: 680, opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(20px)", transition: "all 0.6s ease" }}>
          {topic.title}
        </h1>
        {topic.subtitle && <p style={{ fontSize: 15, color: T.textMuted, margin: "0 0 32px", maxWidth: 600, lineHeight: 1.6 }}>{topic.subtitle}</p>}
        <div style={{ display: "flex", gap: 20, flexWrap: "wrap", marginBottom: 32, clear: "both" }}>
          {(topic.statItems as Array<{ bgColor?: string; label: string; val: string; bullets?: string[] }> || []).map((item, idx) => (
            <div key={idx} style={{
              background: item.bgColor || topic.color,
              borderRadius: C.cardRadius, padding: "24px 28px",
              flex: 1, minWidth: 200, maxWidth: 340,
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.15)`,
              opacity: e ? 1 : 0, transform: e ? "translateY(0)" : "translateY(24px)",
              transition: `all 0.5s ${0.15 + idx * 0.1}s ease`,
            }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: "#000", marginBottom: 6 }}>{item.label}</div>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 56, fontWeight: 700, color: "#000", lineHeight: 1, marginBottom: 12 }}>{item.val}</div>
              {item.bullets && (
                <ul style={{ margin: 0, padding: "0 0 0 16px", fontSize: 12, color: "#000", lineHeight: 1.7 }}>
                  {item.bullets.map((b, bi) => <li key={bi} style={{ marginBottom: 2 }}>{b}</li>)}
                </ul>
              )}
            </div>
          ))}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 24px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default StatHeroLayout;
