/**
 * HStripLayout — horizontal-strip future screen with centered hero and card grid.
 *
 * Layout ID: "h-strip"
 * Extracted from genai_advocacy_hub_13.jsx FutureScreen (lines 1235-1261).
 */

import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

import { useTheme } from "../../components/hooks/useTheme.js";
import { useChrome } from "../../components/hooks/useChrome.js";
import BackBtn from "../../components/navigation/BackBtn.jsx";
import Particles from "../../components/animations/Particles.jsx";

function HStripLayout({ topic, onBack }) {
  const T = useTheme();
  const C = useChrome();
  const [e,setE]=useState(false); useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  return (
    <div style={{ position:"relative",minHeight:"100vh",background:T.bg,overflow:"hidden" }}>
      <Particles color={topic.color} type="future" active={e}/>
      <div style={{ position:"absolute",top:"42%",left:"50%",width:e?"140%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}30,transparent)`,transform:"translateX(-50%)",transition:"width 1.2s cubic-bezier(0.22,1,0.36,1)" }}/>
      <div style={{ position:"relative",zIndex:2,padding:"36px 48px" }}>
        <BackBtn onClick={onBack}/>
        <div style={{ textAlign:"center",marginBottom:40,opacity:e?1:0,transform:e?"translateY(0) scale(1)":"translateY(40px) scale(0.95)",transition:"all 0.7s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize:36,marginBottom:12,filter:`drop-shadow(0 0 16px ${topic.colorGlow})` }}>{topic.icon}</div>
          <h1 style={{ fontFamily:T.fontDisplay,fontSize:44,fontWeight:C.headingWeight,color:T.text,margin:"0 0 8px",textTransform:C.headingTransform }}>{topic.title}</h1>
          <p style={{ fontSize:16,color:topic.colorLight,fontStyle:"italic",margin:0 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,maxWidth:1000,margin:"0 auto" }}>
          {topic.cards.map((c,i)=>(<div key={i} style={{ background:T.bgCard,borderRadius:C.innerRadius,padding:"28px 28px 22px",borderLeft:`${C.accentBarHeight+1}px solid ${topic.color}`,opacity:e?1:0,transform:e?"scale(1)":"scale(0.8)",transition:`all 0.5s ${0.3+i*0.12}s cubic-bezier(0.22,1,0.36,1)` }}><h3 style={{ fontFamily:T.fontDisplay,fontSize:17,fontWeight:C.headingWeight,color:topic.colorLight,margin:"0 0 10px" }}>{c.title}</h3><p style={{ fontSize:13.5,color:T.textMuted,lineHeight:1.6,margin:0 }}>{c.body}</p></div>))}
        </div>
        <div style={{ textAlign:"center",marginTop:36,maxWidth:700,marginLeft:"auto",marginRight:"auto",opacity:e?1:0,transition:"opacity 0.8s 1s" }}><p style={{ fontSize:15,color:T.textMuted,lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p></div>
      </div>
    </div>
  );
}

HStripLayout.propTypes = {
  topic: PropTypes.object.isRequired,
  onBack: PropTypes.func.isRequired,
};

export default HStripLayout;
export { HStripLayout };
