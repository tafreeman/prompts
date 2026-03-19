import type { Framework } from '../schemas/framework.js';
import type { DeckManifest } from '../schemas/manifest.js';

/** Pitch Deck — investor-ready fundraising narrative. */
export const pitchDeck: Framework = {
  id: 'pitch-deck',
  name: 'Pitch Deck',
  description: 'Investor-ready fundraising narrative following the classic VC pitch structure. Covers problem, solution, traction, market, team, and ask.',
  audience: 'Investors, VCs',
  slideRange: { min: 8, max: 12 },
  defaultTheme: 'midnight-teal',
  defaultStyle: 'bold',
  slots: [
    {
      position: 1,
      layout: 'cover',
      titleHint: '[Company Name] — [One-Line Value Prop]',
      contentHint: 'Company name, tagline, and 2-3 headline KPIs (ARR, growth rate, customers).',
      required: true,
    },
    {
      position: 2,
      layout: 'text',
      titleHint: '[Problem Statement — Quantified Pain]',
      contentHint: 'Define the problem with data. Cost of the status quo. Why now?',
      required: true,
    },
    {
      position: 3,
      layout: 'cards',
      titleHint: '[Solution Delivers Measurable Advantage]',
      contentHint: '3-4 cards showing product pillars with key metrics per pillar.',
      required: true,
    },
    {
      position: 4,
      layout: 'scorecard',
      titleHint: '[Traction Proves Product-Market Fit]',
      contentHint: '4-6 KPIs: ARR, customers, retention, growth rate, churn.',
      required: true,
    },
    {
      position: 5,
      layout: 'number',
      titleHint: '[TAM/SAM Opportunity Size]',
      contentHint: 'Big TAM number with CAGR and SAM breakdown in context.',
      required: true,
    },
    {
      position: 6,
      layout: 'grid',
      titleHint: '[Platform/Product Capabilities]',
      contentHint: '4-6 cells showing product pillars, each with a stat and description.',
      required: false,
    },
    {
      position: 7,
      layout: 'timeline',
      titleHint: '[Clear Path to Revenue Target]',
      contentHint: '4-6 milestones from current state to target ARR/exit.',
      required: true,
    },
    {
      position: 8,
      layout: 'closing',
      titleHint: '[Raising $X to Capture Market Opportunity]',
      contentHint: 'Ask amount, valuation, use of funds (3-4 bullets), contact.',
      required: true,
    },
  ],
};

/** Sample manifest for Pitch Deck framework — AI replaces placeholders. */
export const sampleManifest: DeckManifest = {
  title: '[Your Company] — Series [A/B] Pitch',
  subtitle: 'Investor Pitch Deck',
  author: '[Founding Team]',
  date: '2025-Q4',
  version: '1.0.0',
  theme: 'midnight-teal',
  style: 'bold',
  framework: 'pitch-deck',
  slides: [
    {
      id: 'cover',
      layout: 'cover',
      title: '[Your Company] — [The Future of Your Category]',
      subtitle: '[Round] — [$X raise at $Y pre-money]',
      tagline: '[Memorable one-liner about your value prop]',
      kpis: [
        { value: '[$X]', label: 'ARR' },
        { value: '[X%]', label: 'YoY Growth' },
        { value: '[N]', label: 'Customers' },
      ],
    },
    {
      id: 'problem',
      layout: 'text',
      title: '[Current Approach Costs Industry $X Annually]',
      columns: '1',
      body: '[Explain the core problem in 2-3 sentences. Why is the status quo broken? Why now?]',
      bullets: [
        '[Key pain point with quantified impact]',
        '[Customer tolerance threshold being exceeded]',
        '[Revenue or efficiency loss for target segment]',
      ],
      source: '[Industry report, year]',
    },
    {
      id: 'solution',
      layout: 'cards',
      title: '[Product Delivers X Improvement Over Status Quo]',
      cards: [
        { title: '[Feature 1]', stat: '[Metric]', label: '[Label]', body: '[One-sentence value prop]' },
        { title: '[Feature 2]', stat: '[Metric]', label: '[Label]', body: '[One-sentence value prop]' },
        { title: '[Feature 3]', stat: '[Metric]', label: '[Label]', body: '[One-sentence value prop]' },
      ],
      callout: '[Competitive advantage summary]',
    },
    {
      id: 'traction',
      layout: 'scorecard',
      title: '[Traction Proves Product-Market Fit]',
      kpis: [
        { value: '[$X]', label: 'ARR', trend: 'up', detail: '[Growth narrative]' },
        { value: '[N]', label: 'Customers', trend: 'up', detail: '[Customer profile]' },
        { value: '[X%]', label: 'Net Revenue Retention', trend: 'up', detail: '[Expansion detail]' },
        { value: '[X%]', label: 'Monthly Churn', trend: 'down', detail: '[Improvement narrative]' },
      ],
      source: '[Internal metrics, date]',
    },
    {
      id: 'market',
      layout: 'number',
      title: '[Category] Is a $[X]B Market by [Year]',
      stat: '$[X]B',
      statLabel: 'Total Addressable Market',
      context: '[CAGR and SAM breakdown. Which segment you target and why.]',
      source: '[Market research firm, year]',
    },
    {
      id: 'platform',
      layout: 'grid',
      title: '[A Complete Platform for Your Category]',
      columns: 3,
      cells: [
        { title: '[Capability 1]', stat: '[Metric]', body: '[Brief description]', size: 'md' },
        { title: '[Capability 2]', stat: '[Metric]', body: '[Brief description]', size: 'md' },
        { title: '[Capability 3]', stat: '[Metric]', body: '[Brief description]', size: 'md' },
        { title: '[Capability 4]', body: '[Brief description]', size: 'lg' },
        { title: '[Capability 5]', body: '[Brief description]', size: 'md' },
      ],
    },
    {
      id: 'roadmap',
      layout: 'timeline',
      title: '[Clear Path to $[X]M ARR by [Date]]',
      events: [
        { date: '[Q1 Year]', title: '[Milestone 1]', description: '[Key deliverable]' },
        { date: '[Q2 Year]', title: '[Milestone 2]', description: '[Key deliverable]' },
        { date: '[Q3 Year]', title: '[Milestone 3]', description: '[Key deliverable]' },
        { date: '[Q4 Year]', title: '[Milestone 4]', description: '[Key deliverable]' },
      ],
    },
    {
      id: 'ask',
      layout: 'closing',
      title: '[Raising $X to Capture the Market Opportunity]',
      subtitle: '[Round] at [$X pre-money valuation]',
      nextSteps: [
        '[Use of funds item 1 — e.g., Expand engineering team]',
        '[Use of funds item 2 — e.g., Launch new regions]',
        '[Use of funds item 3 — e.g., Build sales team]',
        '[Use of funds item 4 — e.g., Achieve certification]',
      ],
      contact: '[founders@company.com]',
    },
  ],
};
