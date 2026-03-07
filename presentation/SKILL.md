---
name: design-framework
description: Evaluate and improve the visual design quality of React-based presentation JSX files using built-in design principles. Use this skill when the user asks to review, audit, critique, or improve the design of an existing React presentation, advocacy deck, or proposal UI. Also trigger when the user mentions making a presentation "look less AI-generated", improving visual quality, applying design principles, wants a design audit before sharing a deck, or asks to apply/switch a theme. Works alongside the frontend-design skill — frontend-design creates from scratch, this skill improves existing work.
---

This skill evaluates existing React-based presentation JSX files against modern, widely-regarded design principles and produces a structured design audit with prioritized improvements. Changes are only made after the user approves the audit findings.

The user provides a React JSX file (typically a config-driven advocacy deck or internal presentation) and wants its visual design elevated from "functional" to "professionally designed" — grounded in real principles, not aesthetic opinion.

## Workflow

Follow this sequence exactly. Do not skip the audit or jump straight to code changes.

### Step 1 — Read and Understand

Read the full JSX file. Identify:
- The theme/token system (color palette, typography, spacing values)
- Layout types present (cards, grids, timelines, etc.)
- Animation patterns (entry reveals, hover states, canvas effects)
- Config structure (where content lives vs. where design decisions live)
- The intended audience and tone (enterprise, creative, technical, etc.)
- Whether theme values are centralized in a theme object or scattered as hardcoded values
- Whether the file follows the standardized config schema (see Config & Theme Architecture below)

### Step 2 — Audit Against Principles

Evaluate the file against every principle category in the Built-In Design Principles section below. Score each category as Strong / Adequate / Needs Work / Critical.

### Step 3 — Produce the Design Audit Report

Present findings to the user in this format:

```
## Design Audit: [filename]

### Overall Assessment
[2-3 sentences: current quality level, strongest aspects, biggest opportunities]

### Critical Issues (fix these first)
1. [Issue]: [What's wrong] -> [What the principle says] -> [Specific fix]
2. ...

### Improvements (meaningful quality uplift)
1. [Issue]: [What's wrong] -> [Principle] -> [Fix]
2. ...

### Polish (nice-to-have refinements)
1. ...

### What's Working Well
- [Highlight things that should be preserved]

### Recommended Changes Summary
[Numbered list of specific code changes, in priority order, with estimated impact: High/Medium/Low]
```

Ground every finding in a named principle from this document. Do not make subjective aesthetic calls without citing a principle. If something is a matter of taste rather than principle, label it as such.

### Step 4 — Wait for Approval

Present the audit and explicitly ask:
> "Here's the design audit. Which changes would you like me to implement? You can approve all, pick specific items by number, or ask me to adjust the recommendations."

Do NOT proceed to code changes until the user responds. This is a hard gate.

### Step 5 — Implement Approved Changes

Apply only the approved changes. For each change:
- Explain which principle it addresses (one line, in a code comment is fine for non-obvious changes)
- Preserve all existing functionality — animations, interactivity, config-driven behavior
- Keep changes surgical — don't refactor surrounding code that wasn't flagged
- Maintain the file's existing architecture (if it's a single-file artifact, keep it single-file)
- If touching theme values, consolidate them into the theme/config object — never scatter tokens

After implementation, briefly summarize what changed and suggest the user preview the result.

## Quick Mode

If the user says something like "just fix it", "quick pass", or "apply the obvious fixes," skip the full audit report:

1. Read the file and identify the top 3-5 most impactful issues (prioritize Anti-AI-Slop and Visual Hierarchy)
2. List them briefly (one line each with the fix)
3. Ask for a quick confirmation: "I'll fix these 5 items — good to go?"
4. Implement on approval

Quick mode is for iteration speed. Use it when the user has already seen a full audit and is doing follow-up passes, or when they explicitly ask for speed over thoroughness.

---

# Built-In Design Principles

These are the principles every audit evaluates against. Each category includes what to look for, common violations, and fix patterns.

---

## 1. Visual Hierarchy & Attention

**Principle**: Every screen should have exactly one focal point. The viewer's eye should follow a deliberate path: primary element > supporting context > detail.

**What to audit**:
- Is there a clear single focal point per screen?
- Do size, weight, color, and position all agree on what's most important?
- Are stats/metrics visually dominant when they're the key message?
- Does the callout/closing statement have appropriate emphasis without competing with the header?

**Common violations**:
- Everything the same size (flat hierarchy)
- Multiple competing accent colors with equal weight
- Stats buried in card body instead of visually elevated

**Fix patterns**:
- Use a 3:1 minimum size ratio between primary and secondary text
- Limit accent colors to one per screen; use opacity/lightness variants for secondary emphasis
- Stat values should be 2-3x the size of their labels
- Use whitespace isolation to create emphasis (more space around important elements)

---

## 2. Typography

**Principle**: Type choices carry tone. A presentation's credibility lives in its typography more than any other element. Pair a distinctive display face with a neutral-to-warm body face.

**What to audit**:
- Are font pairings intentional? (contrast in style, harmony in tone)
- Is the type scale consistent? (defined scale, not random sizes)
- Letter-spacing: wide for uppercase labels, tight for large headings?
- Line-height: body 1.5-1.7, headings 1.0-1.2?
- Uppercase reserved for small navigational/categorical text only?
- Does the display font match the deck's tone? (serif = authority, mono = technical, geometric sans = modern, rounded = approachable)

**Type scale recommendation** (base 4px):
```
Label:    10px  (uppercase, wide tracking, 600 weight)
Caption:  11px  (muted, regular weight)
Small:    12px  (minimum readable size)
Body:     13-14px (primary reading text)
Subhead:  16-18px (card titles, section labels)
Title:    22-26px (screen titles)
Display:  30-40px (hero stats, landing title)
```

**Verified Google Fonts pairings** (grouped by tone):

*Executive / Consulting:*
- Playfair Display + Source Sans 3
- DM Serif Display + Atkinson Hyperlegible
- Lora + Source Sans 3

*Technical / Engineering:*
- JetBrains Mono + Nunito Sans
- Fira Code + Barlow
- IBM Plex Mono + IBM Plex Sans

*Modern Professional:*
- Sora + Libre Franklin
- Outfit + Karla
- Plus Jakarta Sans + Newsreader
- Instrument Sans + Lora

*Bold / Distinctive:*
- Chakra Petch + Barlow
- Bricolage Grotesque + Literata
- Archivo Black + Work Sans
- Bebas Neue + Lato

**IMPORTANT**: Do NOT suggest Cabinet Grotesk, Satoshi, Clash Display, or General Sans — these are Fontshare/paid fonts NOT available via Google Fonts CDN. Artifact rendering will fail silently.

---

## 3. Color Theory & Palette

**Principle**: Color is communication, not decoration. Every color should have a job. Dominant/accent relationships should be clear and consistent across all screens.

**What to audit**:
- Background-to-foreground contrast ratio sufficient? (4.5:1 body, 3:1 large text)
- Does each page have a distinct hue, visually separable from others?
- Are glow/shadow colors derived from the accent (not generic box-shadows)?
- Is opacity used for depth hierarchy? (full accent primary, 40-60% secondary, 10-20% background tints)
- Does the palette avoid the "rainbow problem"? (too many equally-saturated hues)
- Are all color values in the theme object, not hardcoded in components?

**Fix patterns**:
- Derive secondary colors from primary via HSL manipulation (adjust lightness/saturation, keep hue)
- Colored shadows: `box-shadow: 0 8px 32px ${accentColor}20`
- Accent-tinted borders: `${accentColor}15` to `${accentColor}25`
- Limit each screen to 1 accent hue + neutral palette
- Glow values computed from accent at 20-30% opacity
- Background depth: 3 shades (bg > bgCard > bgDeep) with 2-4% lightness steps

**Dark mode surface hierarchy** (3-tier minimum):
```
bg:      #0A-#12 range  (deepest — page background)
bgCard:  #11-#1A range  (elevated — card containers)
bgDeep:  #16-#22 range  (inset — card content areas, code blocks)
```

---

## 4. Spacing & Rhythm

**Principle**: Consistent spacing creates visual rhythm. Use a base unit (4px or 8px) and derive all spacing from multiples. Irregular spacing signals amateur design.

**What to audit**:
- Discernible spacing scale? (e.g., 4/8/12/16/24/32/48/64)
- Margins and paddings consistent across similar elements?
- Uniform card gaps?
- Adequate page padding at edges?
- Vertical rhythm maintained between sections?

**Common violations**:
- Padding 26px one card, 30px the next, 22px on another (pick 24 or 32)
- Border-radius varies between elements on the same screen
- Cards jammed to screen edges

**Fix patterns**:
- Spacing scale: `[4, 8, 12, 16, 24, 32, 48, 64, 96]`
- Card padding: uniform (recommended 24px)
- Section gaps: 1.5-2x card gaps
- Page padding: minimum 32px sides, 48px top/bottom
- Border-radius scale: cards 10-12px, badges/chips 16-20px, buttons 6-8px, icons 50% or match card

---

## 5. Layout & Composition

**Principle**: Layouts should guide the eye naturally. Symmetry communicates stability; asymmetry communicates energy. Choose deliberately.

**What to audit**:
- Does the layout match content purpose? (metrics = grid, narrative = vertical, comparison = table)
- Is maxWidth set appropriately? (900-960px content, 1100px wide layouts)
- Consistent grid alignment?
- Intentional density variation across screens?

**Presentation-specific layout guidance**:
- Landing tiles: equal-width flex children, consistent minHeight
- Stat cards: left-aligned stat block (~50-60px) + right content
- Before/After: 2-column grid with labeled sections
- Pillars: equal-width columns, top-aligned, optional results column
- Timeline: horizontal flow with phase markers, vertical cards below
- Results: 4-column metric grid top, 2-column narrative below
- Personas: 2x2 or 1x4 grid with pain/gain sections
- Comparison: table grid with sticky header, color-coded score chips

**Common violations**:
- Everything centered (monotony across screens)
- Same layout type for every screen
- Lines exceeding 75 characters (optimal: 45-75)

---

## 6. Motion & Animation

**Principle**: Animation should communicate, not decorate. Entry animations establish spatial origin. Hover states confirm interactivity. Transitions maintain continuity.

**What to audit**:
- Staggered entry timing? (sequential reveal, not all at once)
- Intentional easing? (`cubic-bezier(0.22,1,0.36,1)` for reveals; avoid `linear` or default `ease`)
- Appropriate durations? (200-400ms micro, 500-800ms page transitions)
- Particle/canvas cleanup? (cancelAnimationFrame in useEffect return)
- Clear animation hierarchy? (container first, then children stagger)
- Particle colors derived from page accent, not hardcoded?

**Fix patterns**:
- Stagger delay: 0.1-0.15s between cards, 0.25s between sections
- Consistent easing: `cubic-bezier(0.22, 1, 0.36, 1)` (smooth deceleration)
- Particles: 20-40 per screen, accent-colored, reduced connection distance
- Page transitions: 300-400ms opacity crossfade
- Particle styles by theme:
  - `"network"` — connected dots (collaborative/systems)
  - `"orbit"` — circular motion (process/cycle)
  - `"grid"` — subtle drift (technical/structured)
  - `"float"` — gentle random (warm/organic)
  - `"none"` — no particles (light themes, print aesthetic)

---

## 7. Anti-AI-Slop Checklist

These patterns immediately signal "AI generated this." Flag and fix all of them.

### Typography tells
- Using Inter, Roboto, or system fonts (generic, no personality)
- Using Space Grotesk + DM Sans on every generation (Claude's default pairing)
- No type scale (arbitrary font sizes)
- Overuse of uppercase (labels only, never body)
- Same font weight throughout (no bold/regular contrast)
- Letter-spacing on body text
- Display and body font from same family with no contrast

### Color tells
- Purple-to-blue/teal gradient as default accent
- Cyan (#22D3EE) + green (#10B981) gradient — Claude's specific default
- White cards on light gray (the "SaaS landing page" look)
- Rainbow of equally-weighted accents
- Generic gray borders unrelated to theme
- `box-shadow: 0 2px 8px rgba(0,0,0,0.1)` (the default shadow)
- Pure black (#000000) background — use dark gray (#0A-#1A)
- Pure white (#FFFFFF) text on dark — use off-white (#D6-#F0)
- Glow/shadow using generic black instead of accent-tinted

### Layout tells
- Everything perfectly centered and symmetrical
- Identical card heights forced via fixed height
- No whitespace variation
- Every screen same layout type
- maxWidth not set (content stretches to fill)

### Animation tells
- Fade-in only (no transform, no stagger)
- Hover limited to `opacity: 0.8` or `scale(1.02)`
- Default `ease` everywhere
- Everything animates simultaneously
- `transition: all` instead of specific properties
- Bounce/overshoot on every element

### Content-design tells
- Icons used as decoration rather than communication
- Every card has an emoji regardless of whether it helps
- Decorative elements unrelated to content
- Stats all look equally important (no visual weighting)

### Architecture tells
- Colors hardcoded in components instead of theme object
- Font names scattered instead of referenced from theme
- No consistent card schema
- Theme values duplicated in multiple places

---

## 8. Presentation-Specific Patterns

**Landing page**:
- Tiles create anticipation — each visually distinct but part of a family
- Stats bar feels like a confident data strip, not an afterthought
- Title/accent split creates clear two-line hierarchy
- Brand line (small, uppercase, tracked) anchors the top
- Each tile's bottom border color hints at its detail screen's accent

**Detail screens**:
- Every screen belongs to the same deck (consistent chrome: back button, header, callout pattern)
- Each screen feels distinct via accent color and layout type
- Callout/closing statement is the "so what" — second-most prominent after main content
- Section header pattern: icon badge > brand line > title > subtitle > gradient divider

**Data presentation**:
- Stat values dominate their containers (large, bold, accent-colored)
- Labels: small, muted, uppercase — supporting cast
- Avoid chartjunk: if a stat is "0", don't make zero look impressive
- Stat shape is always `{ value: string, label: string }`

**Narrative flow**:
- Deck tells a story across screens (landing > detail > ... > results)
- Each screen has one clear takeaway
- Callouts should be quotable (short, punchy, opinionated)
- Vary layout types across screens to maintain visual interest

---

## 9. Gestalt Principles Applied

**Proximity**: Related items closer together than unrelated items. Card group gaps smaller than section gaps.

**Similarity**: Same-type elements look the same. All stat values same font/size. All labels match. Inconsistency here is the #1 sign of careless design.

**Continuity**: Eye follows lines and curves. Use borders, dividers, alignment to create visual paths.

**Closure**: Mind completes incomplete shapes. Use partial borders, open layouts, implied containers (background tints instead of hard borders) for sophistication.

**Figure-Ground**: Important elements clearly separate from background via elevation (shadow), color contrast, or spatial isolation.

---

## 10. Accessibility Baseline

Even for internal presentations, maintain these minimums:

- **Contrast**: 4.5:1 body text, 3:1 large text (>18px bold or >24px)
- **Color alone**: Don't rely on color as only differentiator (add icon/label differences too)
- **Motion**: Respect `prefers-reduced-motion` — wrap animations in media query or provide static fallback
- **Font size**: Minimum 12px for visible text. 10px only for uppercase tracking labels. 9px and below never acceptable.
- **Dark mode contrast trap**: Dark gray text (#64748B) on dark backgrounds (#0B1426) often fails. Audit muted text colors specifically.

---

## 11. Config & Theme Architecture

**Principle**: Content, design tokens, and rendering logic should be cleanly separated. A non-developer should be able to edit the config and produce a different deck without touching React code.

### Standardized Config Schema

```
deck                          — Deck-level metadata and global theme
  +-- brand                   — Organization/project line (string)
  +-- title                   — Main deck title (string)
  +-- titleAccent             — Gradient-styled accent title (string)
  +-- tagline                 — Landing page subtitle (string)
  +-- accentGradient          — [color1, color2] for title gradient
  +-- stats[]                 — Landing page bottom stats bar
  |   +-- { val, label }
  +-- theme                   — Global design tokens
      +-- bg, bgCard, bgDeep  — 3-tier surface hierarchy
      +-- text, textMuted, textDim — 3-tier text hierarchy
      +-- border               — Default border color (accent-tinted)
      +-- fontDisplay          — CSS font-family for headings/stats
      +-- fontBody             — CSS font-family for body text
      +-- googleFontsUrl       — Full Google Fonts import URL

pages[]                        — Each page = one landing tile + one detail screen
  +-- id                       — Unique slug (kebab-case)
  +-- num                      — Display number ("01", "02", etc.)
  +-- title                    — Screen title
  +-- subtitle                 — Italicized subtitle
  +-- icon                     — Tile icon (emoji or unicode)
  +-- theme                    — Page-level accent colors
  |   +-- color                — Primary accent (hex)
  |   +-- light                — Light variant (hex)
  +-- layout                   — Layout type string (see Layout Registry)
  +-- banner                   — Optional intro paragraph
  +-- callout                  — Closing quote/statement
  +-- cards[]                  — Content cards
      +-- title                — Always present
      +-- body                 — Optional
      +-- icon                 — Optional
      +-- stat                 — Optional, always { value, label }
```

**Card base shape** (every card follows this regardless of layout):
```json
{
  "title": "Required",
  "body": "Optional",
  "icon": "Optional",
  "stat": { "value": "~40%", "label": "Metric Name" }
}
```

Layout-specific extensions add fields but never replace the base:
- `before-after` adds: `before`, `after`
- `personas` adds: `pain`, `gain`
- `timeline` uses: `phases[].cards[]`
- `sprint` uses: `sprint.nodes[]` with `{ icon, label, type }`
- `pillars` uses: `pillars[].items[]`
- `comparison` uses: `comparison.columns[]` and `comparison.rows[]`

### Config audit checklist
- All design tokens in `deck.theme` or `page.theme`? (no hardcoded hex in components)
- `stat` always `{ value, label }` — never `{ stat, statLabel }` or variants?
- Every page has all required fields?
- Glow computed from `theme.color` at 30% opacity, not stored separately?
- Google Fonts loaded via `<link>` using `theme.googleFontsUrl`?
- Surface hierarchy maintained (bg < bgCard < bgDeep in lightness)?

---

## 12. Verified Theme Catalog

These themes are researched, tested, and verified. Each uses intentional font pairings, color relationships, and interaction patterns.

### Obsidian & Ember
**Vibe**: Editorial / Luxury Dark | **Audience**: Executive, consulting, client-facing
**Fonts**: Playfair Display + Source Sans 3
**Palette**: Matte charcoal (#1A1A1E), warm amber (#D4A853), terracotta (#C75B39)
**Surfaces**: #1A1A1E > #242428 > #2C2C32 | **Text**: #E8E4DF / #9B9590 / #6B6560
**Page accents**: Amber, Terracotta, Sage (#5B8A72), Lavender (#8B7EC8)
**Particles**: network | **Card borders**: left

### Arctic Steel
**Vibe**: Industrial / Minimalist Nordic | **Audience**: Engineering, DevOps, platform
**Fonts**: JetBrains Mono + Nunito Sans
**Palette**: Blue-steel (#0F1318), electric ice-blue (#4FC3F7)
**Surfaces**: #0F1318 > #171D24 > #1E2630 | **Text**: #D6DDE6 / #7B8EA3 / #4E6178
**Page accents**: Ice-blue, Coral (#FF6B6B), Green (#69F0AE), Amber (#FFD54F)
**Particles**: grid | **Card borders**: top

### Midnight Verdant
**Vibe**: Deep Navy / Organic Tech | **Audience**: Developer enablement, internal teams
**Fonts**: Outfit + Karla
**Palette**: Midnight navy (#0A1628), teal-green (#64FFDA)
**Surfaces**: #0A1628 > #112240 > #152A4E | **Text**: #CCD6F6 / #8892B0 / #5A6480
**Page accents**: Teal, Coral (#F78166), Violet (#BD93F9), Yellow (#F1FA8C)
**Particles**: network | **Card borders**: left

### Warm Slate
**Vibe**: Warm Professional | **Audience**: Client stakeholders, trust-building, conservative
**Fonts**: Sora + Libre Franklin
**Palette**: Warm charcoal (#1C1B1F), terracotta (#C17C5A), sage (#7EA87E)
**Surfaces**: #1C1B1F > #272529 > #302E33 | **Text**: #EDE8E3 / #A39E98 / #6E6A65
**Page accents**: Terracotta, Sage, Steel blue (#6B8EC2), Gold (#C4A265)
**Particles**: float | **Card borders**: left

### Neon Noir
**Vibe**: Cyberpunk / High Contrast | **Audience**: Innovation showcases, bold pitches
**Fonts**: Chakra Petch + Barlow
**Palette**: True black (#050508), vivid cyan (#00E5FF), magenta (#FF2D95)
**Surfaces**: #050508 > #0D0D12 > #14141C | **Text**: #EAEAF0 / #8585A0 / #55556E
**Page accents**: Cyan, Magenta, Lime (#AAFF00), Lavender (#B388FF)
**Particles**: orbit | **Card borders**: top

### Paper & Ink
**Vibe**: Light Editorial / Printcraft | **Audience**: White papers, report-style, print-ready
**Fonts**: DM Serif Display + Atkinson Hyperlegible
**Palette**: Warm off-white (#FAF8F5), ink-blue (#1E40AF), amber (#B45309)
**Surfaces**: #FAF8F5 > #FFFFFF > #F0EDE8 | **Text**: #1A1A2E / #5C5C6F / #8E8E9F
**Page accents**: Ink-blue, Amber, Forest (#047857), Violet (#7C3AED)
**Particles**: none | **Card borders**: left

### Style-to-Theme Quick Map

| Requested Style | Theme | Key Moves |
|---|---|---|
| "More editorial" / "premium" | Obsidian & Ember | Serif display, warm amber, matte surfaces |
| "More technical" / "engineering" | Arctic Steel | Monospace display, ice-blue, grid particles |
| "Developer-focused" / "terminal" | Midnight Verdant | Navy + teal-green, network particles |
| "Warmer" / "approachable" / "trust" | Warm Slate | Terracotta + sage, rounded body font |
| "Bold" / "innovative" / "disruptive" | Neon Noir | High-contrast neon, angular display font |
| "Print-ready" / "white paper" | Paper & Ink | Light mode, serif display, ink-blue accents |

---

## 13. Layout Type Registry

Each layout type determines which renderer is used. The config's `page.layout` must match one of these.

| Layout | Purpose | Card Shape | Visual Pattern |
|---|---|---|---|
| `stat-cards` | Metric-driven narrative | `{ title, body, icon, stat }` | Vertical stack, stat left, content right |
| `before-after` | Transformation story | `{ title, icon, before, after }` | 2-column grid, red/green labeled sections |
| `pillars` | Framework breakdown | `pillars[].items[]` | Horizontal columns, optional results sidebar |
| `timeline` | Phased roadmap | `phases[].cards[]` | Horizontal track, vertical milestone cards |
| `sprint` | Process cycle | `sprint.nodes[]` | Figure-8 path, animated comet trail |
| `results` | KPI dashboard | `metrics[] + cards[]` | 4-col metrics top, 2-col narrative below |
| `personas` | Stakeholder value props | `{ title, icon, pain, gain, stat }` | 2x2 grid, pain/gain sections |
| `comparison` | Evaluation matrix | `columns[] + rows[]` | Table grid, color-coded score chips |

---

## Theme Application Workflow

When the user asks to apply or switch themes:
1. Identify the target theme (by name, vibe description, or audience context)
2. Show the theme's key properties and confirm before applying
3. Update the theme/config object — do not scatter colors throughout components
4. Update the Google Fonts `<link>` tag
5. Reassign page-level accent colors from the theme's palette
6. Adjust particle style and card border treatment to match

If the user describes a vibe without naming a theme (e.g., "make it warmer"), map to the closest verified theme and suggest it.

---

## Important Constraints

- **Principles over preferences**: Every recommendation must trace to a principle in this document. "I think it would look better" is not valid rationale.
- **Preserve functionality**: Never break animations, navigation, config-driven rendering, or component structure. Design improvements are visual-layer only.
- **Respect the aesthetic direction**: If the deck is dark-themed, don't suggest light. If minimal, don't add decoration. Improve within the established direction.
- **Font suggestions must be Google Fonts**: Only suggest fonts from the verified pairings above. Artifact rendering fails silently with unavailable fonts.
- **Inline styles only**: These files use inline React styles (no CSS modules, no Tailwind). All changes must work within that constraint.
- **Config-driven awareness**: Design tokens belong in the theme/config object, not hardcoded in components. Theme object is the single source of truth.
- **No localStorage/sessionStorage**: These run in Claude.ai artifacts where browser storage APIs are unavailable.
- **Card schema consistency**: Every card follows the base shape. Layout-specific fields are optional extensions, never replacements.

## Working With the Frontend-Design Skill

- **frontend-design** = Bold creation from scratch. Creative maximalism. Distinctive first impressions.
- **design-framework** = Principled improvement of existing work. Evidence-based refinement. Polish and coherence.

If a file needs to be rebuilt from scratch rather than improved, suggest the user invoke frontend-design instead.
