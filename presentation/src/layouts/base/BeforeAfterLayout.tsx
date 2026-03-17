/**
 * BeforeAfterLayout — challenge/solution cards with staggered reveal animation.
 *
 * Layout ID: "before-after"
 * Extracted from genai_advocacy_hub_13.jsx HurdlesScreen (lines 1188-1232).
 */

import React, { useState, useEffect } from "react";

import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import { usePresentationViewport } from "../../components/hooks/usePresentationViewport.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
import Particles from "../../components/animations/Particles.tsx";
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

function BeforeAfterLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme() as Theme;
  const C = useChrome() as StyleMode;
  const viewport = usePresentationViewport();
  const [e,setE]=useState<boolean>(false);const [vc,setVc]=useState<number>(0);
  useEffect(()=>{const t=setTimeout(()=>setE(true),50);return()=>clearTimeout(t)},[]);
  useEffect(() => {
    if (!e) {
      return undefined;
    }

    const iv = (topic.cards ?? []).map((_, i) => setTimeout(() => setVc(i + 1), 400 + i * 250));
    return () => iv.forEach(clearTimeout);
  }, [e, topic.cards]);
  return (
    <div style={{ position:"relative",minHeight:"100dvh",background:T.bg,overflowX:"hidden",overflowY:viewport.overlayScroll }}>
      <Particles color={topic.color} type="hurdles" active={e}/>
      <div style={{ position:"absolute",inset:0,pointerEvents:"none",overflow:"hidden" }}>{[...Array(8)].map((_,i)=>(<div key={i} style={{ position:"absolute",left:"-10%",top:`${10+i*11}%`,width:e?"120%":"0%",height:1,background:`linear-gradient(90deg,transparent,${topic.color}15,transparent)`,transition:`width ${0.6+i*0.1}s ${0.2+i*0.05}s cubic-bezier(0.16,1,0.3,1)` }}/>))}</div>
      <div style={{ position:"relative",zIndex:2,padding:`${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack}/>
        <div style={{ marginBottom:32,transform:e?"translateX(0)":"translateX(-100px)",opacity:e?1:0,transition:"all 0.5s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ display:"flex",alignItems:viewport.isPhone?"flex-start":"center",gap:16,marginBottom:6 }}><div style={{ fontSize:viewport.isPhone?30:36,transform:e?"rotate(0deg)":"rotate(-90deg)",transition:"transform 0.6s 0.2s cubic-bezier(0.34,1.56,0.64,1)" }}>{topic.icon}</div><h1 style={{ fontFamily:T.fontDisplay,fontSize:viewport.titleSize,fontWeight:C.headingWeight,color:T.text,margin:0,letterSpacing:-1,textTransform:C.headingTransform }}>{topic.title}</h1></div>
          <p style={{ fontSize:viewport.bodySize,color:topic.colorLight,fontStyle:"italic",margin:0,paddingLeft:viewport.isPhone?0:52 }}>{topic.subtitle}</p>
        </div>
        <div style={{ display:"grid",gridTemplateColumns:viewport.isCompact?"1fr":"1fr 1fr",gap:viewport.cardGap,maxWidth:1100 }}>
          {(topic.cards ?? []).map((c,i)=>{const v=i<vc,fl=i%2===0;const hiddenTransform=`translateX(${fl ? "-60px" : "60px"}) scale(0.92)`;return(
            <div key={i} style={{ background:T.bgCard,borderRadius:C.innerRadius,padding:viewport.isPhone?"18px 18px":"24px 28px",borderTop:`${C.accentBarHeight}px solid ${topic.color}`,position:"relative",overflow:"hidden",opacity:v?1:0,transform:v?"translateX(0) scale(1)":hiddenTransform,transition:"all 0.45s cubic-bezier(0.34,1.56,0.64,1)" }}>
              <div style={{ position:"absolute",inset:0,background:`radial-gradient(circle at ${fl?"left":"right"} center,${topic.color}15,transparent 60%)`,opacity:v?1:0,transition:"opacity 0.3s" }}/>
              <div style={{ position:"relative",zIndex:1 }}>
                <div style={{ display:"flex",alignItems:"center",gap:10,marginBottom:14 }}><div style={{ width:28,height:28,borderRadius:C.tagRadius,background:topic.color+"20",display:"flex",alignItems:"center",justifyContent:"center",fontFamily:T.fontDisplay,fontWeight:700,fontSize:13,color:topic.color }}>{i+1}</div><h3 style={{ fontFamily:T.fontDisplay,fontSize:17,fontWeight:C.headingWeight,color:T.text,margin:0 }}>{c.title as string}</h3></div>
                <div style={{ marginBottom:12 }}><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:T.danger,marginBottom:4 }}>Challenge</div><p style={{ fontSize:viewport.isPhone?12.5:13,color:T.textDim,lineHeight:1.5,margin:0 }}>{c.challenge as string}</p></div>
                <div><div style={{ fontSize:10,textTransform:"uppercase",letterSpacing:1.2,fontWeight:700,color:T.success,marginBottom:4 }}>Solution</div><p style={{ fontSize:viewport.isPhone?12.5:13,color:T.textMuted,lineHeight:1.5,margin:0 }}>{c.fix as string}</p></div>
              </div>
            </div>);})}
        </div>
        <div style={{ marginTop:28,background:T.bgCard,borderRadius:C.innerRadius,padding:viewport.isPhone?"16px 18px":"16px 28px",borderLeft:`${C.accentBarHeight+1}px solid ${topic.color}`,display:"flex",alignItems:"center",gap:16,transform:e?"translateX(0)":"translateX(200px)",opacity:e?1:0,transition:"all 0.6s 1.3s cubic-bezier(0.16,1,0.3,1)" }}>
          <div style={{ fontSize:24,color:topic.color }}>⚡</div><p style={{ fontSize:14,color:T.textMuted,lineHeight:1.6,margin:0 }}><strong style={{ color:topic.colorLight }}>{topic.callout}</strong></p>
        </div>
      </div>
    </div>
  );
}

export default BeforeAfterLayout;
export { BeforeAfterLayout };
