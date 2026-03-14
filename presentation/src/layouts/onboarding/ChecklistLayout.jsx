/**
 * ChecklistLayout — approved / prohibited checklist screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (ChecklistScreen, layout id: "checklist").
 */

import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useTheme } from "../../components/hooks/useTheme.js";
import { useChrome } from "../../components/hooks/useChrome.js";
import BackBtn from "../../components/navigation/BackBtn.jsx";
import SectionHeader from "../../components/compound/SectionHeader.jsx";
import Particles from "../../components/animations/Particles.jsx";

export function ChecklistLayout({ topic, onBack }) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  const Item = ({ item, delay }) => (
    <div style={{ display: "flex", gap: 10, padding: "10px 14px", borderRadius: C.innerRadius, background: T.bgDeep, marginBottom: 8, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateX(-12px)", transition: `all 0.4s ${delay}s ease` }}>
      <div style={{ fontSize: 16, flexShrink: 0, marginTop: 1 }}>{item.icon}</div>
      <div>
        <div style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: C.headingWeight, color: T.text, marginBottom: 3 }}>{item.title}</div>
        <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{item.desc}</p>
      </div>
    </div>
  );
  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1100, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.success, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>Approved</div>
            {(topic.approved || []).map((item, i) => <Item key={i} item={item} delay={0.15 + i * 0.06} />)}
            {topic.awareness && (
              <>
                <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.warning, letterSpacing: 2.5, textTransform: "uppercase", marginTop: 16, marginBottom: 12 }}>Awareness Only</div>
                {topic.awareness.map((item, i) => <Item key={`a${i}`} item={item} delay={0.5 + i * 0.06} />)}
              </>
            )}
          </div>
          <div>
            <div style={{ fontSize: 10, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.danger, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>Prohibited</div>
            {(topic.forbidden || []).map((item, i) => <Item key={i} item={item} delay={0.2 + i * 0.06} />)}
          </div>
        </div>
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}
ChecklistLayout.propTypes = { topic: PropTypes.object.isRequired, onBack: PropTypes.func.isRequired };

export default ChecklistLayout;
