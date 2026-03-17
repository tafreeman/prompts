/**
 * DataTableLayout — Verge-style layout with a color-headed data table.
 * Layout ID: "data-table"
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

export function DataTableLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [e, setE] = useState(false);
  useEffect(() => { const t = setTimeout(() => setE(true), 50); return () => clearTimeout(t); }, []);

  const headers = topic.tableHeaders as string[] || [];
  const colors = topic.headerColors as string[] || [];
  const rows = topic.tableRows as string[][] || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1080, margin: "0 auto", padding: "48px" }}>
        <BackBtn onClick={onBack} />
        <h1 style={{ fontFamily: T.fontDisplay, fontSize: 42, fontWeight: C.headingWeight, color: T.text, margin: "0 0 28px", lineHeight: 1.1 }}>
          {topic.title}
        </h1>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, overflow: "hidden", border: `${C.cardBorderWidth}px solid rgba(0,0,0,0.1)`, marginBottom: 24, opacity: e ? 1 : 0, transition: "opacity 0.6s 0.1s ease" }}>
          {topic.tableTitle && (
            <div style={{ background: T.success || "#00CC66", padding: "12px 20px" }}>
              <span style={{ fontFamily: T.fontDisplay, fontSize: 15, fontWeight: 700, color: "#000", textTransform: "uppercase", letterSpacing: 2 }}>{topic.tableTitle as string}</span>
            </div>
          )}
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {headers.map((h, i) => (
                  <th key={i} style={{
                    fontFamily: T.fontDisplay, fontSize: 12, fontWeight: 700,
                    padding: "12px 14px", textAlign: i === 0 ? "left" : "center",
                    color: colors[i] === "transparent" || !colors[i] ? "#000" : "#000",
                    background: colors[i] || "transparent",
                    letterSpacing: 1, textTransform: "uppercase",
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr key={ri} style={{ borderTop: "1px solid rgba(0,0,0,0.08)" }}>
                  {row.map((cell, ci) => (
                    <td key={ci} style={{
                      fontFamily: ci === 0 ? T.fontBody : T.fontDisplay,
                      fontSize: ci === 0 ? 13 : 15, padding: "12px 14px",
                      textAlign: ci === 0 ? "left" : "center",
                      color: "#000", fontWeight: ci === 0 ? 400 : 700,
                    }}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${topic.color}`, maxWidth: 700 }}>
          <p style={{ fontFamily: T.fontDisplay, fontSize: 18, color: T.text, margin: 0, fontWeight: 600 }}>{topic.callout}</p>
        </div>
      </div>
    </div>
  );
}

export default DataTableLayout;
