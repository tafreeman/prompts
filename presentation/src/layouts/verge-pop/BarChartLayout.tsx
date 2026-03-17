/**
 * BarChartLayout — Verge-style layout with animated horizontal bar chart groups.
 * Layout ID: "bar-chart"
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

export function BarChartLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 28px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min((topic.barGroups as unknown[] || []).length, 2)}, 1fr)`, gap: 24, marginBottom: 24 }}>
          {(topic.barGroups as Array<{ color?: string; groupLabel: string; bars: Array<{ label: string; value: number }> }> || []).map((group, gi) => (
            <div key={gi} style={{
              background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 24px",
              border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
              opacity: e ? 1 : 0, transform: e ? "translateX(0)" : "translateX(-20px)",
              transition: `all 0.5s ${0.1 + gi * 0.15}s ease`,
            }}>
              <div style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: group.color || topic.color, marginBottom: 16, borderBottom: `${C.accentBarHeight}px solid ${group.color || topic.color}`, paddingBottom: 10 }}>
                {group.groupLabel}
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {(group.bars || []).map((bar, bi) => (
                  <div key={bi}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                      <span style={{ fontFamily: T.fontBody, fontSize: 12, color: T.text }}>{bar.label}</span>
                      <span style={{ fontFamily: T.fontDisplay, fontSize: 12, fontWeight: 700, color: T.text }}>{bar.value}%</span>
                    </div>
                    <div style={{ height: 20, background: "rgba(0,0,0,0.06)", borderRadius: C.innerRadius, overflow: "hidden" }}>
                      <div style={{
                        height: "100%", width: e ? `${bar.value}%` : "0%",
                        background: group.color || topic.color,
                        borderRadius: C.innerRadius,
                        transition: `width 0.8s ${0.3 + bi * 0.06}s ease`,
                      }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default BarChartLayout;
