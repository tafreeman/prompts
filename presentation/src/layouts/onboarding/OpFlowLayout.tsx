/**
 * OpFlowLayout — one-pager screen for workflow/catalog topics.
 *
 * Extracted from genai_advocacy_hub_13.jsx (OpFlowScreen, layout id: "op-flow").
 */

import { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
import { UI } from "../../tokens/ui-strings.ts";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  num?: string;
  order?: number;
  callout?: string;
  banner?: string;
  eyebrow?: string;
  summary?: string;
  heroPoints?: string[];
  talkingPoints?: string[];
  cards?: Record<string, unknown>[];
  [key: string]: unknown;
}

interface LayoutProps {
  topic: Topic;
  onBack: () => void;
}

export function OpFlowLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const [entered, setEntered] = useState<boolean>(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const fade = (delay: number) => ({
    opacity: entered ? 1 : 0,
    transform: entered ? "none" : "translateY(10px)",
    transition: `all 0.5s ${delay}s cubic-bezier(0.22,1,0.36,1)`,
  });

  const steps = (topic.steps as Record<string, unknown>[]) || [];
  const isWorkflow = Boolean(steps.length);
  const half = Math.ceil(steps.length / 2);
  const row1 = steps.slice(0, half);
  const row2 = steps.slice(half);
  const categories = (topic.categories as Record<string, unknown>[]) || [];

  // Talking points derived from content
  const talkingPoints = isWorkflow
    ? steps.slice(0, 4).map(s => s.title as string)
    : categories.flatMap(c => (c.items as Record<string, unknown>[]) || []).slice(0, 4).map(i => i.label as string);

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <div style={{ height: 3, background: `linear-gradient(90deg,${topic.color},${topic.color}40,transparent)` }} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}08,transparent 65%)`, pointerEvents: "none" }} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1200, margin: "0 auto", padding: "24px 32px" }}>
        <BackBtn onClick={onBack} />

        {/* ── ROW 1: Header + Snapshot ── */}
        <div style={{ ...fade(0.05), display: "grid", gridTemplateColumns: "1fr 300px", gap: 24, marginBottom: 18 }}>
          <div>
            <div style={{ fontSize: 9, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: topic.color, letterSpacing: 3, textTransform: "uppercase", marginBottom: 6 }}>
              {topic.icon} Module {topic.order || "\u2014"} &nbsp;&middot;&nbsp; One-Pager
            </div>
            <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 7px", letterSpacing: "-0.5px" }}>{topic.title}</h1>
            <p style={{ fontFamily: T.fontDisplay, fontSize: 13.5, fontStyle: "italic", color: topic.color, margin: "0 0 11px" }}>{topic.subtitle}</p>
            <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.65, margin: 0, maxWidth: 540 }}>{(topic.subheadline as string) || (topic.headline as string) || ""}</p>
          </div>
          {/* Snapshot */}
          <div style={{ background: T.bgCard, borderRadius: C.cardRadius, border: `1px solid ${topic.color}22`, borderTop: `3px solid ${topic.color}`, padding: "16px 18px" }}>
            <div style={{ fontSize: 8, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.textDim, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>Snapshot</div>
            {isWorkflow ? (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 9 }}>
                {[
                  { val: String(steps.length), lbl: "Total Steps" },
                  { val: String(steps.filter(s => s.type === "ai").length), lbl: "AI Steps" },
                  { val: String(steps.filter(s => s.type === "human").length), lbl: "Human Gates" },
                  { val: "1 wk", lbl: "Sprint Cycle" },
                ].map((s, i) => (
                  <div key={i} style={{ padding: "9px 11px", background: T.bgDeep, borderRadius: C.innerRadius, borderLeft: `2px solid ${topic.color}40` }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 17, fontWeight: C.headingWeight, color: topic.color, lineHeight: 1, marginBottom: 2 }}>{s.val}</div>
                    <div style={{ fontSize: 8.5, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{s.lbl}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                {categories.map((cat, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, padding: "7px 10px", background: T.bgDeep, borderRadius: C.innerRadius, borderLeft: `2px solid ${cat.color as string}` }}>
                    <div style={{ fontSize: 8, color: cat.color as string, fontWeight: 700 }}>●</div>
                    <div style={{ fontSize: 11, color: T.textMuted, flex: 1 }}>{cat.title as string}</div>
                    <div style={{ fontSize: 9, color: T.textDim }}>{((cat.items as unknown[]) || []).length}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* ── WORKFLOW: 2-row compact step grid ── */}
        {isWorkflow && (
          <>
            <div style={{ ...fade(0.15), fontSize: 8, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.textDim, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 8 }}>{UI.SECTION.processFlow}</div>
            {[row1, row2].filter(row => row.length > 0).map((row, ri) => (
              <div key={ri} style={{ ...fade(0.18 + ri * 0.08), display: "grid", gridTemplateColumns: `repeat(${row.length},1fr)`, gap: 8, marginBottom: 8 }}>
                {row.map((step, i) => {
                  const isAI = step.type === "ai";
                  return (
                    <div key={i} style={{ background: T.bgCard, borderRadius: C.innerRadius, padding: "11px 13px", borderTop: `2px solid ${isAI ? topic.color : topic.color + "38"}` }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 5 }}>
                        <span style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: C.headingWeight, color: isAI ? topic.color : T.textDim }}>{step.num as string}</span>
                        <span style={{ fontSize: 7.5, padding: "1px 6px", borderRadius: 3, background: isAI ? topic.color + "20" : "rgba(255,255,255,0.05)", color: isAI ? topic.color : T.textDim, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, letterSpacing: 0.5 }}>{isAI ? UI.WORKFLOW.ai : UI.WORKFLOW.human}</span>
                      </div>
                      <h4 style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: C.headingWeight, color: T.text, margin: "0 0 4px" }}>{step.title as string}</h4>
                      <p style={{ fontSize: 10, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{(step.body as string).length > 85 ? (step.body as string).slice(0, 85) + "\u2026" : step.body as string}</p>
                    </div>
                  );
                })}
              </div>
            ))}
          </>
        )}

        {/* ── CATALOG: 3-col category cards ── */}
        {!isWorkflow && (
          <>
            <div style={{ ...fade(0.15), fontSize: 8, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.textDim, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 8 }}>Data Classification</div>
            <div style={{ ...fade(0.2), display: "grid", gridTemplateColumns: `repeat(${categories.length},1fr)`, gap: 10, marginBottom: 16 }}>
              {categories.map((cat, ci) => (
                <div key={ci} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "13px 15px", borderTop: `3px solid ${cat.color as string}` }}>
                  <h4 style={{ fontFamily: T.fontDisplay, fontSize: 11.5, fontWeight: C.headingWeight, color: cat.color as string, margin: "0 0 10px" }}>{cat.title as string}</h4>
                  <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                    {((cat.items as Record<string, unknown>[]) || []).map((item, i) => (
                      <div key={i} style={{ padding: "7px 9px", background: T.bgDeep, borderRadius: C.innerRadius, borderLeft: `2px solid ${cat.color as string}45` }}>
                        <div style={{ fontFamily: T.fontDisplay, fontSize: 11, fontWeight: C.headingWeight, color: T.text, marginBottom: 2 }}>{item.label as string}</div>
                        <p style={{ fontSize: 10, color: T.textMuted, lineHeight: 1.45, margin: 0 }}>{item.desc as string}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {/* ── Talking Points + Bottom Line ── */}
        <div style={{ ...fade(0.34), display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "13px 16px" }}>
            <div style={{ fontSize: 8, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.textDim, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 10 }}>{UI.SECTION.talkingPoints}</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
              {talkingPoints.map((pt, i) => (
                <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                  <span style={{ fontFamily: T.fontDisplay, fontSize: 10.5, fontWeight: C.headingWeight, color: topic.color, flexShrink: 0, minWidth: 20 }}>0{i + 1}</span>
                  <span style={{ fontSize: 12, color: T.text, lineHeight: 1.4 }}>{pt}</span>
                </div>
              ))}
            </div>
          </div>
          <div style={{ background: topic.color + "0F", borderRadius: C.cardRadius, padding: "13px 16px", border: `1px solid ${topic.color}22`, borderLeft: `3px solid ${topic.color}` }}>
            <div style={{ fontSize: 8, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: topic.color, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 9 }}>{UI.SECTION.bottomLine}</div>
            <p style={{ fontSize: 13, color: T.text, lineHeight: 1.7, margin: 0, fontWeight: 500 }}>&ldquo;{topic.callout}&rdquo;</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default OpFlowLayout;
