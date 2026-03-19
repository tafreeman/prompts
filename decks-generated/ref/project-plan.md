# Plan: `decks-generated` — AI-Copiloted Deck Workshop

## Context

The repo has a mature `presentation/` system (34 layouts, 15 themes, 8 deck presets) but it evolved organically and isn't optimized for AI-assisted deck creation. Two HTML reference guides (`presentation-design-guide.html`, `presentation-design-references.html`) codify best practices from 40+ sources (Tufte, Knaflic, Minto, Reynolds, Duarte). The goal is a **new standalone project** at `decks-generated/` purpose-built for human+AI copiloting — where AI writes JSON manifests (never JSX) and design-guide rules are enforced by schema validation. The `/frontend-design` skill will be used during implementation for high-quality, distinctive UI. Parallel sub-agents will accelerate implementation.

---

## High-Level Goals

### 1. AI Ease of Use (Primary)
- AI creates decks by writing a single `manifest.json` — pure data, no JSX
- Zod discriminated-union schemas validate per-layout content with instant, specific error messages
- Framework templates (Executive, Pitch, SCR, etc.) as starter scaffolds the AI populates
- Layout catalog page shows all available layouts with sample data for AI reference
- CLAUDE.md documents every layout schema, theme, and workflow pattern

### 2. Design Quality by Default
- **Assertion-Evidence Model** enforced: `actionTitle` required on every slide (conclusion-first)
- **60-30-10 color rule** computed automatically from theme tokens
- **8px grid** spacing system — no arbitrary pixel values
- **Type scale** enforced (named steps: HERO/TITLE/SECTION/BODY/CAPTION — no raw font sizes)
- **Anti-pattern guards** in Zod: max 7 bullets, max 6 cards, max 100-char titles, source field on data slides
- Design guide principles from the HTML references are structural, not cosmetic

### 3. Curated Simplicity
- **15 layouts** (down from 34) covering the highest-value patterns from the design guide
- **6 themes** (down from 15): 3 dark + 3 light, curated for versatility
- **3 style modes**: clean (default), bold, editorial
- **5 framework templates** with defined slide flows and required slide types

### 4. Production Export
- PPTX export via pptxgenjs (programmatic, not screenshot-based) — the primary output
- HTML single-file, PNG per-slide, PDF as secondary formats
- Each export honors theme tokens and layout structure

### 5. Developer Experience
- React 19 + Vite 6 + TypeScript strict + Storybook 10
- HMR for manifest.json changes — edit JSON, see slides update instantly
- CLI: `npm run new-deck`, `npm run validate`, `npm run export`

---

## Project Structure

```
decks-generated/
├── decks/                        # AI-authored deck manifests
│   └── example-pitch/
│       └── manifest.json         # Single source of truth
├── ref/                          # Reference PPTX files (existing)
├── scripts/
│   ├── new-deck.mts              # Scaffold from framework template
│   ├── validate.mts              # CLI manifest validator
│   ├── export-html.mts
│   ├── export-png.mts
│   ├── export-pdf.mts
│   └── export-pptx.mts          # Programmatic PPTX via pptxgenjs
├── src/
│   ├── App.tsx                   # Root: deck loader + viewer + controls
│   ├── main.tsx
│   ├── schemas/                  # Zod schemas (THE contract AI writes against)
│   │   ├── manifest.ts           # DeckManifest root schema
│   │   ├── slide.ts              # Discriminated union by layout
│   │   ├── guards.ts             # Design-guide guardrails as refinements
│   │   ├── framework.ts          # Framework template definitions
│   │   └── theme.ts              # ThemeId validation
│   ├── tokens/
│   │   ├── themes.ts             # 6 curated themes + Theme interface
│   │   ├── style-modes.ts        # 3 modes + StyleMode interface
│   │   ├── type-scale.ts         # Named scale (HERO → CAPTION)
│   │   ├── spacing.ts            # 8px grid tokens
│   │   └── color-distribution.ts # 60-30-10 CSS variable generator
│   ├── layouts/
│   │   ├── registry.ts           # LayoutRegistry singleton (from presentation/)
│   │   ├── LayoutRenderer.tsx    # Layout string → component resolver
│   │   ├── register-all.ts       # Side-effect registration
│   │   └── {layout-id}/          # 15 layout folders, each with component + register.ts
│   ├── components/
│   │   ├── context/              # ThemeContext, StyleContext, DeckContext
│   │   ├── hooks/                # useTheme, useStyle, useDeck
│   │   ├── primitives/           # Heading, Body, Card, StatValue, CalloutBox, etc.
│   │   ├── deck/                 # DeckViewer, SlideContainer, SlideNavigator
│   │   └── catalog/              # LayoutCatalog (visual reference for AI)
│   ├── frameworks/               # 5 template definitions
│   │   ├── executive-brief.ts
│   │   ├── pitch-deck.ts
│   │   ├── strategy-scr.ts
│   │   ├── tech-architecture.ts
│   │   └── status-report.ts
│   ├── export/                   # PPTX renderer: manifest → pptxgenjs
│   │   ├── pptx-renderer.ts
│   │   ├── pptx-theme-map.ts
│   │   └── pptx-layout-map.ts
│   └── stories/                  # Storybook stories (layouts, primitives, viewer)
├── .storybook/
│   ├── main.ts
│   └── preview.tsx               # Global ThemeContext + StyleContext decorator
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── CLAUDE.md                     # Copilot instructions: schemas, workflows, examples
```

---

## 15 Layouts

| ID | Name | Key Content Fields | Design Guide Pattern |
|----|------|--------------------|---------------------|
| `cover` | Title/Cover | tagline, kpis[] | First impression slide |
| `section-divider` | Section Break | sectionNumber | Pyramid Principle sections |
| `two-column` | Two Column | leftColumn, rightColumn, callout, source | General assertion-evidence |
| `stat-cards` | Stat Cards | cards[]{stat, label, title, body} | KPI evidence |
| `big-number` | Big Number | stat, statLabel, context, source | "So What?" callout |
| `process-steps` | Process Steps | steps[]{label, description} | Sequential flow (max 7) |
| `before-after` | Before/After | before{items[]}, after{items[]} | Transformation stories |
| `quote-block` | Quote Block | quote, attribution, context | Expert testimony |
| `data-table` | Data Table | columns[], rows[], highlight, source | Tabular evidence |
| `kpi-scorecard` | KPI Scorecard | kpis[]{value, label, trend, detail} | Dashboard metrics |
| `timeline` | Timeline | events[]{date, title, description} | Roadmaps, history |
| `card-grid` | Card Grid | cards[]{title, body, icon, stat}, columns | Feature comparisons |
| `image-text` | Image + Text | imageUrl, imageAlt, body, bullets | Photo + narrative |
| `bento-grid` | Bento Grid | cells[]{title, body, size, stat} | 2026 trend layout |
| `closing` | Closing | contactInfo, nextSteps[] | Call to action |

---

## 6 Curated Themes

| Theme ID | Type | Vibe | Source |
|----------|------|------|--------|
| `midnight-teal` | Dark | Professional tech | Existing (most used) |
| `neon-noir` | Dark | Bold keynote | Existing |
| `linear` | Dark | Clean minimal | Existing |
| `paper-ink` | Light | Classic readable | Existing |
| `signal-cobalt` | Light | Corporate blue | Existing |
| `studio-craft` | Light | Warm editorial | Existing |

---

## AI Copilot Workflow

```
1. AI selects framework → creates decks/{id}/manifest.json from template
2. Vite HMR → slides render instantly in browser
3. Human previews, requests edits ("make slide 3 a big-number layout")
4. AI edits manifest.json (never JSX) → instant reload
5. Zod validates on every load → AI gets specific error messages
6. Human approves → AI runs `npm run export:pptx -- --deck {id}`
```

---

## Implementation Phases

### Phase 1: Foundation (Bootstrap + Tokens + Schemas)
- Init project: package.json, vite.config.ts, tsconfig.json, React 19 + Vite 6 + Zod
- Token files: themes.ts (6), style-modes.ts (3), type-scale.ts, spacing.ts, color-distribution.ts
- Zod schemas: manifest.ts, slide.ts (discriminated union), guards.ts, framework.ts
- Context/hooks: ThemeContext, StyleContext, DeckContext
- **Parallel agents**: tokens + schemas can be built simultaneously

### Phase 2: Layout System (Registry + 5 Core Layouts)
- Port registry.ts from `presentation/src/layouts/registry.ts` (simplified)
- Build primitives: Heading, Body, Card, StatValue, CalloutBox, AccentBar, Eyebrow, IconBadge
- Build SlideContainer (16:9 viewport wrapper)
- 5 core layouts: cover, two-column, stat-cards, big-number, section-divider
- **Use /frontend-design skill** for distinctive, high-quality layout components
- **Parallel agents**: primitives + layouts can be built simultaneously

### Phase 3: Deck Viewer + Navigation
- DeckViewer: manifest loader + Zod validator + slide renderer
- SlideNavigator: keyboard (arrows), click, slide counter
- App.tsx: deck selector + viewer + theme/style controls
- Example deck: `decks/example-pitch/manifest.json`
- HMR wiring for manifest file changes

### Phase 4: Remaining 10 Layouts
- process-steps, before-after, quote-block, data-table
- kpi-scorecard, timeline, card-grid, image-text
- bento-grid (2026 trend), closing
- **Parallel agents**: layouts are independent — build 3-4 at a time

### Phase 5: Framework Templates + AI Workflow
- 5 framework template files with sample manifests
- `scripts/new-deck.mts`: scaffold from framework
- `scripts/validate.mts`: CLI validator with detailed errors
- LayoutCatalog.tsx: visual reference page for all layouts
- CLAUDE.md: complete copilot instructions

### Phase 6: Storybook
- Config + global decorator (theme/style toolbar selectors)
- Stories for all primitives and all 15 layouts
- DeckViewer + LayoutCatalog stories

### Phase 7: Export Pipeline
- export-pptx.mts: programmatic PPTX via pptxgenjs (primary)
- export-html.mts: single-file Vite build
- export-png.mts: Playwright per-slide capture
- export-pdf.mts: pdf-lib assembly

### Phase 8: Polish + Verification
- E2E: create deck → preview → export all formats
- AI copilot dry run: simulate Claude creating a deck from scratch
- Design guide compliance audit

---

## Key Files to Reuse from `presentation/`

| Source File | What to Reuse |
|-------------|---------------|
| `presentation/src/layouts/registry.ts` | LayoutRegistry singleton pattern (simplify: add metadata, remove LayoutFeatures) |
| `presentation/src/tokens/themes.ts` | 6 of 15 Theme definitions + Theme interface |
| `presentation/src/tokens/style-modes.ts` | StyleMode interface pattern (reduce to 3 modes) |
| `presentation/src/patterns/decks/schema.ts` | Zod validation pattern (extend to discriminated union) |
| `presentation/gen-playbook-lite.cjs` | pptxgenjs slide-building patterns (refactor to per-layout builders) |
| `presentation/scripts/export-presentation.mjs` | Playwright + pdf-lib export pipeline |
| `presentation/.storybook/preview.jsx` | Global decorator pattern for theme/style context |

---

## Verification Plan

1. **Schema validation**: Create valid + invalid manifests, verify Zod produces actionable errors
2. **Layout rendering**: Every layout renders with sample data across all 6 themes in Storybook
3. **Deck viewer**: Load example-pitch manifest, navigate all slides, switch themes/styles
4. **HMR**: Edit manifest.json → browser updates without full reload
5. **PPTX export**: Generate PPTX from example deck, open in PowerPoint, verify fidelity
6. **AI dry run**: Use Claude to create a deck from the pitch-deck framework by editing only manifest.json
7. **Guardrails**: Verify >7 bullets, missing actionTitle, >6 cards all produce clear Zod errors
