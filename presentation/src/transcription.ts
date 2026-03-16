/**
 * transcription.ts — Cross-family layout normalisation.
 *
 * Extracted from App.v14.jsx. Pure extraction — no logic changes.
 * Public API: transcribeTopic + layout set constants.
 */

export type Topic = Record<string, unknown> & { layout: string };

// ── Layout set constants ───────────────────────────────────────────────────

export const BASE_LAYOUTS = new Set(["two-col","stat-cards","before-after","process-cycle","h-strip","process-lanes"]);
export const VERGE_LAYOUTS = new Set(["stat-hero","quote-collage","badge-grid","data-table","bar-chart","color-blocks"]);
export const HANDBOOK_LAYOUTS = new Set(["hb-chapter","hb-practices","hb-process","hb-manifesto","hb-index"]);
export const ADV_LAYOUTS = new Set(["adv-overview","adv-stats","adv-hurdles","adv-future","adv-platform"]);
export const ADVD_LAYOUTS = new Set(["advd-overview","advd-stats","advd-hurdles","advd-future","advd-platform"]);

// ── Transcription functions ────────────────────────────────────────────────

function transcribeToBase(topic: Topic): Topic {
  switch (topic.layout) {
    case "info-cards": return {
      ...topic, layout: "stat-cards",
      kicker: `Module ${topic.order || ""}`,
      thesis: topic.banner || undefined,
      leadershipPoints: (topic.cards as any[]).map((c: any) => `${c.stat}${c.statLabel ? " "+c.statLabel : ""}: ${c.title}`),
      cards: (topic.cards as any[]).map((c: any) => ({ title: c.title, step: c.stat, eyebrow: c.statLabel, body: c.body })),
    };
    case "checklist": return {
      ...topic, layout: "two-col",
      summary: `${((topic.approved as any[])||[]).length} approved tools · ${((topic.forbidden as any[])||[]).length} prohibited practices`,
      heroPoints: ((topic.approved as any[])||[]).map((i: any) => i.title),
      cards: ((topic.approved as any[])||[]).map((i: any) => ({ title: i.title, body: i.desc })),
      talkingPoints: ((topic.forbidden as any[])||[]).map((i: any) => `${i.icon} ${i.title}: ${i.desc}`),
    };
    case "workflow": return {
      ...topic, layout: "two-col",
      summary: `${((topic.steps as any[])||[]).filter((s: any)=>s.type==="human").length} human checkpoints · ${((topic.steps as any[])||[]).filter((s: any)=>s.type==="ai").length} AI-assisted phases`,
      heroPoints: ((topic.steps as any[])||[]).map((s: any) => `${s.num}. ${s.title}`),
      cards: ((topic.steps as any[])||[]).map((s: any) => ({ title: `${s.num}. ${s.title}`, body: s.body })),
      talkingPoints: ((topic.steps as any[])||[]).filter((s: any) => s.tip).map((s: any) => `${s.title}: ${s.tip}`),
    };
    case "pillars": return {
      ...topic, layout: "stat-cards",
      kicker: `Module ${topic.order || ""}`,
      thesis: topic.subtitle,
      leadershipPoints: ((topic.pillars as any[])||[]).flatMap((p: any) => ((p.items as any[])||[]).slice(0,2)),
      cards: ((topic.pillars as any[])||[]).map((p: any) => ({ title: p.title, step: p.icon||"", body: ((p.items as any[])||[]).join(" · ") })),
      results: ((topic.results as any[])||[]).map((r: any) => ({ value: r.val, label: r.label })),
    };
    case "catalog": return {
      ...topic, layout: "two-col",
      summary: topic.subtitle,
      heroPoints: ((topic.categories as any[])||[]).map((c: any) => c.title),
      cards: ((topic.categories as any[])||[]).map((c: any) => ({ title: c.title, body: ((c.items as any[])||[]).map((i: any)=>i.label||i).join(" · ") })),
      talkingPoints: ((topic.categories as any[])||[]).flatMap((c: any) => ((c.items as any[])||[]).map((i: any) => `${i.label||i}: ${i.desc||""}`.trim())),
    };
    case "hb-chapter": return {
      ...topic, layout: "two-col",
      summary: topic.summary,
      heroPoints: ((topic.chapters as any[])||[]).map((c: any) => `${c.num}. ${c.title} — ${c.sub}`),
      cards: ((topic.chapters as any[])||[]).map((c: any) => ({ title: c.title, body: c.sub })),
      talkingPoints: topic.heroPoints || [],
    };
    case "hb-practices": return {
      ...topic, layout: "stat-cards",
      kicker: topic.eyebrow,
      thesis: topic.summary,
      cards: ((topic.practices as any[])||[]).map((p: any, i: number) => ({ title: p.title, step: `0${i+1}`, body: p.body })),
    };
    case "hb-process": return {
      ...topic, layout: "process-cycle",
    };
    case "hb-manifesto": return {
      ...topic, layout: "h-strip",
      heroPoints: topic.beliefs || [],
      cards: ((topic.beliefs as any[])||[]).map((b: any) => ({ title: b, body: "" })),
    };
    case "hb-index": return {
      ...topic, layout: "two-col",
      summary: topic.subtitle,
      heroPoints: ((topic.categories as any[])||[]).map((c: any) => c.label),
      cards: ((topic.categories as any[])||[]).map((c: any) => ({ title: c.label, body: c.body })),
      talkingPoints: [],
    };
    // ── Verge → Base ────────────────────────────────────────────────────────
    case "stat-hero": return {
      ...topic, layout: "stat-cards",
      cards: ((topic.statCards as any[])||[]).map((c: any) => ({ title: c.body?.slice(0,40)||"", stat: c.value, statLabel: c.label, body: c.body||"" })),
    };
    case "quote-collage": return {
      ...topic, layout: "h-strip",
      cards: ((topic.quotes as any[])||[]).map((q: any) => ({ title: q.text, body: q.attr||"" })),
    };
    case "badge-grid": return {
      ...topic, layout: "two-col",
      heroPoints: ((topic.badges as any[])||[]).map((b: any) => b.label),
      cards: ((topic.badges as any[])||[]).map((b: any) => ({ title: b.label, body: b.meta||"" })),
    };
    case "data-table": return {
      ...topic, layout: "stat-cards",
      cards: ((topic.tableRows as any[])||[]).map((r: any) => ({ title: r[0]||"", body: ((r as any[]).slice?.(1)||[]).join(" · "), stat: "", statLabel: "" })),
    };
    case "bar-chart": return {
      ...topic, layout: "stat-cards",
      cards: ((topic.barGroups as any[])||[]).map((g: any) => ({ title: g.label||"", body: ((g.bars as any[])||[]).map((b: any) => `${b.label}: ${b.value}`).join(", "), stat: "" })),
    };
    case "color-blocks": return {
      ...topic, layout: "two-col",
      cards: ((topic.blocks as any[])||[]).map((b: any) => ({ title: b.label||"", body: b.body||"" })),
    };
    // ── Engineering → Base ──────────────────────────────────────────────────
    case "eng-architecture": return {
      ...topic, layout: "stat-cards",
      cards: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body||"", stat: c.stat||"", statLabel: c.statLabel||"" })),
    };
    case "eng-code-flow": return {
      ...topic, layout: "two-col",
      cards: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body||"" })),
    };
    case "eng-tech-stack": return {
      ...topic, layout: "stat-cards",
      cards: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body||"", stat: c.stat||"", statLabel: "" })),
    };
    case "eng-roadmap": return {
      ...topic, layout: "h-strip",
      cards: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body||"" })),
    };
    // ── Ops → Base ──────────────────────────────────────────────────────────
    case "op-brief": return {
      ...topic, layout: "stat-cards",
      kicker: topic.headline,
      cards: topic.cards,
    };
    case "op-flow": return {
      ...topic, layout: "two-col",
      cards: ((topic.steps as any[] || topic.cards as any[])||[]).map((s: any) => ({ title: s.title||s.num||"", body: s.body||"" })),
    };
    // ── Advocacy → Base ─────────────────────────────────────────────────────
    case "adv-overview":
    case "advd-overview": return {
      ...topic, layout: "two-col",
      heroPoints: topic.heroPoints,
      cards: topic.cards,
      talkingPoints: topic.talkingPoints,
    };
    case "adv-stats":
    case "advd-stats": return {
      ...topic, layout: "stat-cards",
      thesis: topic.thesis,
      cards: ((topic.cards as any[])||[]).map((c: any) => ({ ...c, stat: c.step||c.stat||"", statLabel: c.eyebrow||c.statLabel||"" })),
    };
    case "adv-hurdles":
    case "advd-hurdles": return {
      ...topic, layout: "before-after",
      cards: topic.cards,
    };
    case "adv-future":
    case "advd-future": return {
      ...topic, layout: "h-strip",
      cards: topic.cards,
      callout: topic.callout,
    };
    case "adv-platform":
    case "advd-platform": return {
      ...topic, layout: "process-lanes",
      focusPanels: topic.focusPanels,
      capabilities: topic.capabilities,
      lanes: topic.lanes,
    };
    default: return topic;
  }
}

function transcribeToVerge(topic: Topic): Topic {
  switch (topic.layout) {
    case "info-cards": return {
      ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: (topic.cards as any[]).map((c: any) => ({ value: c.stat, label: c.statLabel, body: c.body })),
    };
    case "checklist": return {
      ...topic, layout: "badge-grid",
      badges: [
        ...((topic.approved as any[])||[]).map((i: any) => ({ icon: i.icon, label: i.title, meta: "Approved" })),
        ...((topic.forbidden as any[])||[]).map((i: any) => ({ icon: i.icon, label: i.title, meta: "Prohibited" })),
      ],
    };
    case "workflow": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.steps as any[])||[]).map((s: any) => ({ label: `${s.num}. ${s.title}`, value: s.type.toUpperCase(), body: s.body })),
    };
    case "pillars": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.pillars as any[])||[]).map((p: any) => ({ label: p.title, value: p.icon||"", body: ((p.items as any[])||[]).slice(0,2).join(" · ") })),
    };
    case "catalog": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.categories as any[])||[]).map((c: any) => ({ label: c.title, value: c.items?.length||0, body: ((c.items as any[])||[]).slice(0,3).map((i: any)=>i.label||i).join(" · ") })),
    };
    case "hb-chapter": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.chapters as any[])||[]).map((c: any) => ({ label: c.title, value: c.num, body: c.sub })),
    };
    case "hb-practices": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.practices as any[])||[]).map((p: any, i: number) => ({ label: p.title, value: `0${i+1}`, body: p.body.slice(0, 80) })),
    };
    case "hb-process": return {
      ...topic, layout: "color-blocks",
      blocks: ((topic.steps as any[])||[]).map((s: any) => ({ label: s.title, value: s.num, body: s.body })),
    };
    case "hb-manifesto": return {
      ...topic, layout: "quote-collage",
      quotes: ((topic.beliefs as any[])||[]).map((b: any) => ({ text: b, attr: topic.eyebrow || "Studio" })),
    };
    case "hb-index": return {
      ...topic, layout: "badge-grid",
      badges: ((topic.categories as any[])||[]).map((c: any, i: number) => ({ icon: `0${i+1}`, label: c.label, meta: c.body.split(" ").slice(0,5).join(" ") })),
    };
    // -- Base -> Verge
    case "two-col": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, body: c.body||"", value: "" })),
    };
    case "stat-cards": return { ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: ((topic.cards as any[])||[]).map((c: any) => ({ value: c.stat||"", label: c.statLabel||"", body: c.body||"" })),
    };
    case "before-after": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, body: (c.challenge||"")+" -> "+(c.fix||""), value: "" })),
    };
    case "process-cycle": return { ...topic, layout: "color-blocks", blocks: [] };
    case "h-strip": return { ...topic, layout: "quote-collage",
      quotes: ((topic.cards as any[])||[]).map((c: any) => ({ text: c.title, attr: c.body||"" })),
    };
    case "process-lanes": return { ...topic, layout: "color-blocks",
      blocks: ((topic.lanes as any[])||[]).map((l: any) => ({ label: l.title, value: l.persona||"", body: l.subtitle||"" })),
    };
    // -- Engineering -> Verge
    case "eng-architecture": return { ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: ((topic.cards as any[])||[]).map((c: any) => ({ value: c.stat||"", label: c.title, body: c.body||"" })),
    };
    case "eng-code-flow": return { ...topic, layout: "badge-grid",
      badges: ((topic.cards as any[])||[]).map((c: any) => ({ icon: c.icon||"->", label: c.title, meta: (c.body as string)?.slice(0,40)||"" })),
    };
    case "eng-tech-stack": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, value: c.stat||"", body: c.body||"" })),
    };
    case "eng-roadmap": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, value: c.stat||"", body: c.body||"" })),
    };
    // -- Ops -> Verge
    case "op-brief": return { ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: ((topic.cards as any[])||[]).map((c: any) => ({ value: c.stat||"", label: c.statLabel||"", body: c.body||"" })),
    };
    case "op-flow": return { ...topic, layout: "color-blocks",
      blocks: ((topic.steps as any[]||topic.cards as any[])||[]).map((s: any) => ({ label: s.title||"", value: s.type||"", body: s.body||"" })),
    };
    // -- Advocacy -> Verge
    case "adv-overview": return { ...topic, layout: "badge-grid",
      badges: [...((topic.heroPoints as any[])||[]).map((p: any) => ({ icon: "O", label: p, meta: "" })), ...((topic.cards as any[])||[]).map((c: any) => ({ icon: ".", label: c.title, meta: (c.body as string)?.slice(0,30)||"" }))],
    };
    case "adv-stats": return { ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: ((topic.cards as any[])||[]).map((c: any) => ({ value: (c.step||c.stat)||"", label: (c.eyebrow||c.statLabel)||"", body: c.body||"" })),
    };
    case "adv-hurdles": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, body: c.challenge||"", value: "" })),
    };
    case "adv-future": return { ...topic, layout: "quote-collage",
      quotes: [{ text: (topic.callout as string)||"", attr: topic.title }, ...((topic.cards as any[])||[]).map((c: any) => ({ text: c.title, attr: c.body||"" }))],
    };
    case "adv-platform": return { ...topic, layout: "color-blocks",
      blocks: ((topic.capabilities as any[])||[]).map((c: any) => ({ label: c.title, value: c.icon||"", body: c.body||"" })),
    };
    // -- Advocacy Dense -> Verge
    case "advd-overview": return { ...topic, layout: "badge-grid",
      badges: [...((topic.heroPoints as any[])||[]).map((p: any) => ({ icon: "O", label: p, meta: "" })), ...((topic.cards as any[])||[]).map((c: any) => ({ icon: ".", label: c.title, meta: (c.body as string)?.slice(0,30)||"" }))],
    };
    case "advd-stats": return { ...topic, layout: "stat-hero",
      heroTitle: topic.title,
      statCards: ((topic.cards as any[])||[]).map((c: any) => ({ value: (c.step||c.stat)||"", label: (c.eyebrow||c.statLabel)||"", body: c.body||"" })),
    };
    case "advd-hurdles": return { ...topic, layout: "color-blocks",
      blocks: ((topic.cards as any[])||[]).map((c: any) => ({ label: c.title, body: c.challenge||"", value: "" })),
    };
    case "advd-future": return { ...topic, layout: "quote-collage",
      quotes: [{ text: (topic.callout as string)||"", attr: topic.title }, ...((topic.cards as any[])||[]).map((c: any) => ({ text: c.title, attr: c.body||"" }))],
    };
    case "advd-platform": return { ...topic, layout: "color-blocks",
      blocks: ((topic.capabilities as any[])||[]).map((c: any) => ({ label: c.title, value: c.icon||"", body: c.body||"" })),
    };
    default: return topic;
  }
}

function transcribeToHandbook(topic: Topic): Topic {
  switch (topic.layout) {
    case "two-col": return {
      ...topic, layout: "hb-chapter",
      eyebrow: topic.eyebrow || "Chapter",
      summary: topic.summary || topic.subtitle,
      heroPoints: topic.heroPoints || [],
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.body?.slice(0,60)||"" })),
    };
    case "stat-cards": return {
      ...topic, layout: "hb-practices",
      eyebrow: topic.kicker || "Practices",
      summary: topic.thesis || topic.subtitle,
      practices: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body || "", dark: false })),
    };
    case "process-cycle": return { ...topic, layout: "hb-process" };
    case "h-strip": return {
      ...topic, layout: "hb-manifesto",
      eyebrow: "Manifesto",
      statement: topic.title,
      beliefs: topic.heroPoints || ((topic.cards as any[])||[]).map((c: any) => c.title),
    };
    case "before-after": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Before \u2192 After",
      summary: topic.subtitle,
      heroPoints: ((topic.cards as any[])||[]).map((c: any) => `${c.title}: ${c.fix||""}`).slice(0,5),
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.fix?.slice(0,50)||"" })),
    };
    case "process-lanes": return {
      ...topic, layout: "hb-index",
      eyebrow: "Platforms",
      categories: ((topic.lanes as any[])||[]).map((l: any) => ({ label: l.title, body: l.subtitle || l.persona })),
    };
    // ── Info-rich source layouts → Handbook ─────────────────────────────────
    case "info-cards": return {
      ...topic, layout: "hb-practices",
      eyebrow: "Module",
      summary: topic.banner,
      practices: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body || "", dark: false })),
    };
    case "checklist": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Governance",
      summary: topic.subtitle,
      heroPoints: ((topic.forbidden as any[])||[]).map((i: any) => `${i.icon} ${i.title}`),
      chapters: ((topic.approved as any[])||[]).map((i: any, idx: number) => ({ num: `0${idx+1}`, title: i.title, sub: i.desc || "" })),
    };
    case "workflow": return {
      ...topic, layout: "hb-process",
      steps: ((topic.steps as any[])||[]).map((s: any) => ({ num: s.num || "", title: s.title, body: s.body || "" })),
    };
    case "pillars": return {
      ...topic, layout: "hb-index",
      categories: ((topic.pillars as any[])||[]).map((p: any) => ({ label: p.title, body: ((p.items as any[])||[]).join(" · ") })),
    };
    case "catalog": return {
      ...topic, layout: "hb-index",
      categories: ((topic.categories as any[])||[]).map((c: any) => ({ label: c.title, body: ((c.items as any[])||[]).map((i: any) => i.label || i).join(" · ") })),
    };
    // ── Verge → Handbook ────────────────────────────────────────────────────
    case "stat-hero": return {
      ...topic, layout: "hb-practices",
      eyebrow: "Stats",
      summary: topic.subtitle,
      practices: ((topic.statCards as any[])||[]).map((c: any) => ({ title: `${c.value} ${c.label}`, body: c.body || "", dark: false })),
    };
    case "quote-collage": return {
      ...topic, layout: "hb-manifesto",
      eyebrow: "Manifesto",
      statement: ((topic.quotes as any[])||[])[0]?.text || topic.title,
      beliefs: ((topic.quotes as any[])||[]).map((q: any) => q.text),
    };
    case "badge-grid": return {
      ...topic, layout: "hb-index",
      categories: ((topic.badges as any[])||[]).map((b: any) => ({ label: b.label || b.name || "", body: b.meta || "" })),
    };
    case "data-table": return {
      ...topic, layout: "hb-chapter",
      eyebrow: (topic.tableTitle as string) || "Data",
      summary: topic.subtitle,
      chapters: ((topic.tableRows as any[])||[]).map((r: any, i: number) => ({ num: `0${i+1}`, title: r[0] || "", sub: ((r as any[]).slice?.(1) || []).join(" · ") })),
    };
    case "bar-chart": return {
      ...topic, layout: "hb-practices",
      eyebrow: "Metrics",
      summary: topic.subtitle,
      practices: ((topic.barGroups as any[])||[]).map((g: any) => ({ title: g.label || "", body: ((g.bars as any[])||[]).map((b: any) => `${b.label}: ${b.value}`).join(", "), dark: false })),
    };
    case "color-blocks": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Overview",
      summary: topic.subtitle,
      chapters: ((topic.blocks as any[])||[]).map((b: any, i: number) => ({ num: `0${i+1}`, title: b.label || "", sub: b.body?.slice(0, 60) || "" })),
    };
    // ── Engineering → Handbook ──────────────────────────────────────────────
    case "eng-architecture": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Architecture",
      summary: topic.subtitle || topic.subheadline,
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.body?.slice(0, 60) || "" })),
    };
    case "eng-code-flow": return {
      ...topic, layout: "hb-process",
      steps: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, body: c.body || "" })),
    };
    case "eng-tech-stack": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Architecture",
      summary: topic.subtitle || topic.subheadline,
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.body?.slice(0, 60) || "" })),
    };
    case "eng-roadmap": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Architecture",
      summary: topic.subtitle || topic.subheadline,
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.body?.slice(0, 60) || "" })),
    };
    // ── Ops → Handbook ──────────────────────────────────────────────────────
    case "op-brief": return {
      ...topic, layout: "hb-practices",
      eyebrow: "One-Pager",
      summary: topic.headline,
      practices: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body || "", dark: false })),
    };
    case "op-flow": return {
      ...topic, layout: "hb-process",
      steps: ((topic.steps as any[] || topic.cards as any[])||[]).map((s: any, i: number) => ({ num: s.num || `0${i+1}`, title: s.title || "", body: s.body || "" })),
    };
    // ── Advocacy → Handbook ─────────────────────────────────────────────────
    case "adv-overview":
    case "advd-overview": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Overview",
      summary: topic.summary || topic.subtitle,
      heroPoints: (topic.heroPoints as any[]) || [],
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.body?.slice(0, 60) || "" })),
    };
    case "adv-stats":
    case "advd-stats": return {
      ...topic, layout: "hb-practices",
      eyebrow: "Stats",
      summary: topic.thesis,
      practices: ((topic.cards as any[])||[]).map((c: any) => ({ title: c.title, body: c.body || "", dark: false })),
    };
    case "adv-hurdles":
    case "advd-hurdles": return {
      ...topic, layout: "hb-chapter",
      eyebrow: "Challenges",
      summary: topic.subtitle,
      chapters: ((topic.cards as any[])||[]).map((c: any, i: number) => ({ num: `0${i+1}`, title: c.title, sub: c.challenge?.slice(0, 50) || "" })),
    };
    case "adv-future":
    case "advd-future": return {
      ...topic, layout: "hb-manifesto",
      eyebrow: "Vision",
      statement: topic.callout || topic.title,
      beliefs: ((topic.cards as any[])||[]).map((c: any) => c.title),
    };
    case "adv-platform":
    case "advd-platform": return {
      ...topic, layout: "hb-index",
      categories: ((topic.capabilities as any[])||[]).map((c: any) => ({ label: c.title, body: c.body || "" })),
    };
    default: return topic;
  }
}

function transcribeToAdvocacy(topic: Topic): Topic {
  switch (topic.layout) {
    case "info-cards": return {
      ...topic, layout: "adv-stats",
      thesis: topic.banner,
      cards: (topic.cards as any[]).map((c: any) => ({
        title: c.title, body: c.body,
        step: c.stat, eyebrow: c.statLabel,
        marker: c.icon || "○",
      })),
    };
    case "checklist": return {
      ...topic, layout: "adv-overview",
      heroPoints: ((topic.approved as any[]) || []).map((i: any) => i.title),
      cards: ((topic.approved as any[]) || []).map((i: any) => ({ title: i.title, body: i.desc })),
      talkingPoints: ((topic.forbidden as any[]) || []).map((i: any) => `${i.icon} ${i.title}`),
    };
    case "workflow": return {
      ...topic, layout: "adv-hurdles",
      cards: ((topic.steps as any[]) || []).map((s: any) => ({
        title: s.title,
        challenge: s.body,
        fix: s.tip || (s.type === "ai" ? "AI-assisted" : "Human review"),
      })),
    };
    case "pillars": return {
      ...topic, layout: "adv-platform",
      capabilities: ((topic.pillars as any[]) || []).flatMap((p: any) => ((p.items as any[]) || []).map((i: any) => ({
        icon: p.icon || "●", title: i, body: "",
      }))),
      focusPanels: ((topic.results as any[]) || []).map((r: any) => ({ label: r.val, title: r.label, body: "" })),
    };
    case "catalog": return {
      ...topic, layout: "adv-future",
      cards: ((topic.categories as any[]) || []).slice(0, 4).map((c: any) => ({
        title: c.title,
        body: ((c.items as any[]) || []).slice(0, 3).map((i: any) => i.label || i).join(" · "),
      })),
    };
    // ── Base → Advocacy ─────────────────────────────────────────────────────
    case "two-col": return {
      ...topic, layout: "adv-overview",
      heroPoints: topic.heroPoints,
      cards: topic.cards,
      talkingPoints: topic.talkingPoints,
      summary: topic.summary,
    };
    case "stat-cards": return {
      ...topic, layout: "adv-stats",
      thesis: (topic.thesis as any) || (topic.kicker as any),
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, body: c.body || "",
        step: c.stat || c.step || "", eyebrow: c.statLabel || c.eyebrow || "",
        marker: c.icon || "○",
      })),
    };
    case "before-after": return {
      ...topic, layout: "adv-hurdles",
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, challenge: c.challenge || "", fix: c.fix || "",
      })),
    };
    case "h-strip": return {
      ...topic, layout: "adv-future",
      cards: topic.cards,
      callout: topic.callout,
    };
    case "process-lanes": return {
      ...topic, layout: "adv-platform",
      focusPanels: topic.focusPanels,
      capabilities: topic.capabilities,
      lanes: topic.lanes,
      eyebrow: topic.eyebrow,
    };
    // ── Handbook → Advocacy ─────────────────────────────────────────────────
    case "hb-chapter": return {
      ...topic, layout: "adv-overview",
      heroPoints: (topic.heroPoints as any) || [],
      cards: ((topic.chapters as any[]) || []).map((c: any) => ({ title: c.title, body: c.sub || "" })),
      summary: topic.summary,
    };
    case "hb-practices": return {
      ...topic, layout: "adv-stats",
      thesis: topic.summary,
      cards: ((topic.practices as any[]) || []).map((c: any) => ({
        title: c.title, body: c.body || "",
        step: "", eyebrow: "", marker: "○",
      })),
    };
    case "hb-manifesto": return {
      ...topic, layout: "adv-future",
      callout: (topic.statement as any) || "",
      cards: ((topic.beliefs as any[]) || []).map((b: any) => ({ title: b, body: "" })),
    };
    case "hb-index": return {
      ...topic, layout: "adv-platform",
      capabilities: ((topic.categories as any[]) || []).map((c: any) => ({
        icon: "●", title: c.label || "", body: c.body || "",
      })),
      focusPanels: [],
      lanes: [],
    };
    // ── Verge → Advocacy ────────────────────────────────────────────────────
    case "stat-hero": return {
      ...topic, layout: "adv-stats",
      thesis: topic.subtitle,
      cards: ((topic.statCards as any[]) || []).map((c: any) => ({
        title: c.label || "", body: c.body || "",
        step: c.value || "", eyebrow: "", marker: "○",
      })),
    };
    case "quote-collage": return {
      ...topic, layout: "adv-future",
      callout: ((topic.quotes as any[]) || [])[0]?.text || "",
      cards: ((topic.quotes as any[]) || []).slice(1).map((q: any) => ({ title: q.text, body: q.attr || "" })),
    };
    case "badge-grid": return {
      ...topic, layout: "adv-overview",
      heroPoints: ((topic.badges as any[]) || []).map((b: any) => b.label || b.name || ""),
      cards: ((topic.badges as any[]) || []).map((b: any) => ({ title: b.label || b.name || "", body: b.meta || "" })),
    };
    case "data-table": return {
      ...topic, layout: "adv-stats",
      thesis: (topic.tableTitle as any) || "",
      cards: ((topic.tableRows as any[]) || []).map((r: any) => ({
        title: r[0] || "", body: ((r as any[]).slice?.(1) || []).join(" · "),
        step: "", eyebrow: "", marker: "○",
      })),
    };
    case "bar-chart": return {
      ...topic, layout: "adv-stats",
      thesis: topic.subtitle,
      cards: ((topic.barGroups as any[]) || []).map((g: any) => ({
        title: g.label || "",
        body: ((g.bars as any[]) || []).map((b: any) => `${b.label}: ${b.value}`).join(", "),
        step: "", eyebrow: "", marker: "○",
      })),
    };
    case "color-blocks": return {
      ...topic, layout: "adv-overview",
      heroPoints: [],
      cards: ((topic.blocks as any[]) || []).map((b: any) => ({ title: b.label || "", body: b.body || "" })),
    };
    // ── Engineering → Advocacy ──────────────────────────────────────────────
    case "eng-architecture": return {
      ...topic, layout: "adv-stats",
      thesis: (topic.subheadline as any) || topic.subtitle,
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, body: c.body || "",
        step: c.stat || "", eyebrow: c.statLabel || "", marker: "○",
      })),
    };
    case "eng-code-flow": return {
      ...topic, layout: "adv-hurdles",
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, challenge: c.body || "", fix: "",
      })),
    };
    case "eng-tech-stack": return {
      ...topic, layout: "adv-stats",
      thesis: (topic.subheadline as any) || topic.subtitle,
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, body: c.body || "",
        step: c.stat || "", eyebrow: c.statLabel || "", marker: "○",
      })),
    };
    case "eng-roadmap": return {
      ...topic, layout: "adv-future",
      callout: (topic.callout as any) || "",
      cards: ((topic.cards as any[]) || []).map((c: any) => ({ title: c.title, body: c.body || "" })),
    };
    // ── Ops → Advocacy ──────────────────────────────────────────────────────
    case "op-brief": return {
      ...topic, layout: "adv-stats",
      thesis: topic.headline,
      cards: ((topic.cards as any[]) || []).map((c: any) => ({
        title: c.title, body: c.body || "",
        step: c.stat || "", eyebrow: c.statLabel || "", marker: "○",
      })),
    };
    case "op-flow": return {
      ...topic, layout: "adv-hurdles",
      cards: ((topic.steps as any[] || topic.cards as any[]) || []).map((s: any) => ({
        title: s.title || "", challenge: s.body || "", fix: s.tip || "",
      })),
    };
    default: return topic;
  }
}

function transcribeToAdvocacyDense(topic: Topic): Topic {
  const base = transcribeToAdvocacy(topic);
  return { ...base, layout: base.layout.replace("adv-", "advd-") };
}

export function transcribeTopic(topic: Topic, targetFamily: string): Topic {
  if (targetFamily === "base" && !BASE_LAYOUTS.has(topic.layout)) return transcribeToBase(topic);
  if (targetFamily === "verge" && !VERGE_LAYOUTS.has(topic.layout)) return transcribeToVerge(topic);
  if (targetFamily === "handbook" && !HANDBOOK_LAYOUTS.has(topic.layout)) return transcribeToHandbook(topic);
  if (targetFamily === "advocacy" && !ADV_LAYOUTS.has(topic.layout)) return transcribeToAdvocacy(topic);
  if (targetFamily === "advocacy-dense" && !ADVD_LAYOUTS.has(topic.layout)) return transcribeToAdvocacyDense(topic);
  return topic;
}
