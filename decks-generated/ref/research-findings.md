# Research Findings: Deck Generation Best Practices

## What Works

### Schema-Driven Systems
- **Zod discriminated unions** are ~3-5x faster than regular unions (skips non-matching branches)
- **Discriminator field must be `z.literal()`** — duck-typing with optional discriminators causes silent failures
- Add `.superRefine()` for human-readable error messages — default union errors list all rejected branches

### Design Tokens
- **3-tier hierarchy**: reference (raw values) → semantic (named) → component (contextual)
- **60-30-10 color rule** as CSS custom properties works well for theming
- **Flat TypeScript objects** sufficient for small projects; Figma Tokens Studio + Style Dictionary for enterprise
- Keep token count minimal — "token fatigue" kills productivity when abstraction becomes the goal

### Hot Reloading JSON in Vite
- Use `import.meta.glob('/decks/*.json', { eager: true })` for batch loading
- Add `configureServer` hook to watch the decks directory for HMR
- Keep individual manifest files < 100KB for fast HMR
- `import.meta.globEager` is deprecated — use `{ eager: true }` option

### PPTX Generation (pptxgenjs)
- No CSS support — every element needs absolute positioning (`x`, `y`, `w`, `h`)
- Font names must match installed system fonts (no auto-substitution)
- Colors must be RGB hex, not CSS color values
- Use Slide Masters for brand consistency post-export
- Accept 80% fidelity — budget 20% for manual cleanup
- Prioritize web export (HTML/PNG) as primary; PPTX as secondary

### Presentation System Patterns
- **Registry pattern** (self-registering components) eliminates switch statements, O(1) lookup
- **Content/structure separation** works for data-driven decks; tight coupling is fine for narrative decks
- **Transcription functions** for cross-family layout mapping are unique and valuable

---

## What Doesn't Work (Anti-Patterns to Avoid)

### AI-Generated Content Failures
- Generic, formulaic bullet points that sound "written by someone learning business English"
- AI overfills slides with text instead of concise points
- AI lacks audience context — produces one-size-fits-all content
- Tome shut down its slides product (March 2025) — market signal about pure-AI approaches
- **Mitigation**: Design-guide guardrails in schema (max bullets, action titles, concise limits)

### PPTX Export Disasters
- Blurred backgrounds and transparent fills don't render in PPTX
- Gradients downconverted to solid colors
- Font substitution breaks layouts when fonts aren't installed
- Gamma's "broken exports" are frequently cited as blocking issues
- **Mitigation**: Design for PPTX constraints from day one; test export early

### Template Rigidity
- Too-strict templates block creative iteration and reduce adoption
- Too-loose templates produce visual chaos
- Master slide neglect causes inconsistency within decks
- **Mitigation**: "Guardrails with escape hatches" — strict defaults, override with warnings

### Token Sprawl
- Teams create recursive abstraction layers, debating "semantic" vs "functional" naming
- `color-background-surface-secondary-inverse-hover` replaces simple names
- Thousands of derived tokens mapping to other tokens — maintenance nightmare
- **Mitigation**: Cap at ~20 tokens per theme; use flat objects, not nested hierarchies

### Schema Validation UX
- Generic errors ("Field required") don't help users understand WHY
- Strict validation that blocks saving prevents rapid drafting
- Zod discriminated union errors print ALL rejected branches — unreadable for complex schemas
- **Mitigation**: Custom `.superRefine()` with contextual messages; validate on render, not on save

### Content Separation Pitfalls
- WYSIWYG tools blur content and design — makes separation artificial
- Content can't be reused across formats without rework when tightly coupled to layout
- **Mitigation**: Our approach (JSON manifest with layout field) is the right middle ground

---

## Actionable Decisions for decks-generated

| Decision | Rationale |
|----------|-----------|
| Use discriminated union by `layout` field | 3-5x faster validation, precise per-layout errors |
| Add `.superRefine()` to all schemas | Default Zod union errors are unreadable |
| Cap at 6 themes, ~20 tokens each | Avoid token fatigue; flat objects not nested hierarchies |
| 8px spacing grid (not 4px) | Industry standard, aligns with device pixel ratios |
| PPTX export as secondary format | Accept 80% fidelity, prioritize web preview |
| Design for PPTX constraints in layouts | Avoid gradients/transparency/custom fonts that won't export |
| Guardrails with escape hatches | Max bullets, required action titles, but allow `.passthrough()` for custom fields |
| Single manifest.json per deck | No structure/content split — reduces indirection |
| Vite glob + configureServer for HMR | Proven pattern for watching JSON during development |

---

## AI API Integration (Stretch Goal)

Architecture if pursued later:
- **BFF proxy** (Express alongside Vite dev server) — never expose API keys client-side
- **Streaming SSE** for content generation (better UX than waiting for complete response)
- **Sidebar copilot panel** (right drawer) for slide content suggestions
- **Inline "improve" buttons** on text elements
- Claude API with system prompt containing deck metadata, audience, tone
- **Not core scope** — Claude Code already serves as the AI copilot for editing manifest.json

---

## Sources

- Slidev, Spectacle, MDX Deck — React/Vite presentation frameworks
- PptxGenJS docs and GitHub issues — PPTX generation limitations
- Gamma, Beautiful.ai, Tome — AI presentation tool reviews and postmortems
- Zod discriminated unions API docs and GitHub issues (#792, #1095, #2106)
- Figma forum — PPTX export quality threads
- Token Fatigue article (Web Designer Depot) — design token anti-patterns
- Microsoft Copilot UX guidance — AI assistant UI patterns
