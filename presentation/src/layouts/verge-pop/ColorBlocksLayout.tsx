/**
 * ColorBlocksLayout — Verge-style layout with asymmetric color block grid.
 * Layout ID: "color-blocks"
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

export function ColorBlocksLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  const blocks = topic.blocks as Array<{ area: string; bgColor?: string; stat?: { val: string; label: string }; text?: string; chartBars?: Array<{ label: string; peopleOnly: number; mixed: number; aiOnly: number }> }> || [];
  const left = blocks.find((b) => b.area === "left");
  const topRight = blocks.find((b) => b.area === "top-right");
  const bottomRight = blocks.find((b) => b.area === "bottom-right");

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1180, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 24px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1.2fr", gridTemplateRows: "auto 1fr",
          gap: 0, marginBottom: 24, borderRadius: C.cardRadius, overflow: "hidden",
          border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`, minHeight: 420,
        }}>
          {left && (
            <div style={{
              gridRow: "1 / -1", background: left.bgColor || topic.color,
              padding: "40px 32px", display: "flex", flexDirection: "column",
              justifyContent: "center", alignItems: "center",
              opacity: e ? 1 : 0, transition: "opacity 0.6s 0.1s ease",
            }}>
              {left.stat && (
                <>
                  <div style={{ fontFamily: T.fontDisplay, fontSize: 80, fontWeight: 900, color: "#000", lineHeight: 1, marginBottom: 16 }}>{left.stat.val}</div>
                  <p style={{ fontFamily: T.fontBody, fontSize: 14, color: "#000", textAlign: "center", lineHeight: 1.5, maxWidth: 220 }}>{left.stat.label}</p>
                </>
              )}
            </div>
          )}
          {topRight && (
            <div style={{
              background: topRight.bgColor || T.bgCard, padding: "28px 24px",
              display: "flex", alignItems: "center",
              borderBottom: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`,
              opacity: e ? 1 : 0, transition: "opacity 0.6s 0.2s ease",
            }}>
              <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: "#000", lineHeight: 1.5, margin: 0 }}>{topRight.text}</p>
            </div>
          )}
          {bottomRight && (
            <div style={{
              background: bottomRight.bgColor || T.bgCard, padding: "20px 20px",
              overflow: "auto", opacity: e ? 1 : 0, transition: "opacity 0.6s 0.3s ease",
            }}>
              {bottomRight.chartBars && (
                <div style={{ display: "grid", gap: 5 }}>
                  <div style={{ display: "flex", justifyContent: "flex-end", gap: 16, marginBottom: 4, fontSize: 9, fontFamily: T.fontDisplay, fontWeight: 700, color: "#000" }}>
                    <span>PEOPLE ONLY</span><span>AI + PEOPLE</span><span>AI ONLY</span>
                  </div>
                  {bottomRight.chartBars.map((bar, idx) => (
                    <div key={idx} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <span style={{ fontFamily: T.fontDisplay, fontSize: 10, fontWeight: 700, color: "#000", minWidth: 100, textTransform: "uppercase", textAlign: "right" }}>{bar.label}</span>
                      <div style={{ flex: 1, display: "flex", height: 14, borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ width: `${bar.peopleOnly}%`, background: "#3399FF", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                        <div style={{ width: `${bar.mixed}%`, background: "#FFD600", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                        <div style={{ width: `${bar.aiOnly}%`, background: "#00CC66", transition: `width 0.8s ${0.3 + idx * 0.04}s ease` }} />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}` }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default ColorBlocksLayout;
