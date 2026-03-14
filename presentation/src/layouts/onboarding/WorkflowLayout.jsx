/**
 * WorkflowLayout — vertical timeline workflow screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (WorkflowScreen, layout id: "workflow").
 */

import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useTheme } from "../../components/hooks/useTheme.js";
import { useChrome } from "../../components/hooks/useChrome.js";
import BackBtn from "../../components/navigation/BackBtn.jsx";
import SectionHeader from "../../components/compound/SectionHeader.jsx";
import Particles from "../../components/animations/Particles.jsx";

export function WorkflowLayout({ topic, onBack }) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  const [expanded, setExpanded] = useState(null);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 960, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
          {(topic.steps || []).map((step, i) => {
            const isAI = step.type === "ai";
            const isExp = expanded === i;
            return (
              <div key={i} onClick={() => setExpanded(isExp ? null : i)} style={{ cursor: "pointer" }}>
                <div style={{ display: "flex", gap: 16, alignItems: "stretch", opacity: entered ? 1 : 0, transform: entered ? "none" : "translateX(-20px)", transition: `all 0.45s ${0.15 + i * 0.08}s ease` }}>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 44 }}>
                    <div style={{ width: 36, height: 36, borderRadius: "50%", background: isAI ? T.accent + "20" : T.bgCard, border: `2px solid ${isAI ? T.accent : T.textDim}60`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: T.fontDisplay, fontSize: 12, fontWeight: C.headingWeight, color: isAI ? T.accent : T.textMuted, flexShrink: 0 }}>{step.num}</div>
                    {i < topic.steps.length - 1 && <div style={{ width: 2, flex: 1, minHeight: 16, background: isAI ? T.accent + "30" : (T.border || "rgba(255,255,255,0.06)"), margin: "4px 0" }} />}
                  </div>
                  <div style={{ flex: 1, paddingBottom: 16 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                      <h3 style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: C.headingWeight, color: T.text, margin: 0 }}>{step.title}</h3>
                      <span style={{ fontSize: 9, fontWeight: C.headingWeight, padding: "2px 8px", borderRadius: C.pillRadius, background: isAI ? T.accent + "20" : "rgba(255,255,255,0.06)", color: isAI ? T.accent : T.textDim, fontFamily: T.fontDisplay, letterSpacing: 1, textTransform: "uppercase" }}>{isAI ? "AI" : "Human"}</span>
                    </div>
                    <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{step.body}</p>
                    {isExp && step.tip && (
                      <div style={{ marginTop: 10, padding: "10px 14px", borderRadius: C.innerRadius, background: T.accent + "0A", borderLeft: `${C.accentBarHeight}px solid ${T.accent}40`, fontSize: 12, color: T.accent, lineHeight: 1.5 }}>💡 {step.tip}</div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}
WorkflowLayout.propTypes = { topic: PropTypes.object.isRequired, onBack: PropTypes.func.isRequired };

export default WorkflowLayout;
