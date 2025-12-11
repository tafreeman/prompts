---
title: "Ad Copy Generator"
shortTitle: "Ad Copy"
intro: "Create persuasive advertising copy for various channels including Google Ads, Facebook, LinkedIn, display ads, and more."
type: "how_to"
difficulty: "beginner"
audience:
  - "functional-team"
  - "business-analyst"
  - "project-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "advertising"
  - "copywriting"
  - "creative"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
  - "general-use"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.2
---
# Ad Copy Generator

---

## Description

Create high-converting advertising copy tailored to specific platforms, audiences, and campaign goals. This prompt helps marketers, advertisers, and business owners develop compelling ad copy that captures attention, communicates value, and drives desired actions.

---

## Use Cases

- Google Search Ads (responsive search ads, headlines, descriptions)
- Facebook and Instagram Ads (primary text, headlines, descriptions)
- LinkedIn Ads (sponsored content, message ads, text ads)
- Display and banner ads
- YouTube ad scripts (bumper ads, skippable ads)
- Retargeting ad campaigns

---

## Prompt

```text
You are an expert advertising copywriter who creates high-converting ad copy. Write compelling ad copy based on the following campaign brief:

**Campaign Overview:**
- Platform: [GOOGLE SEARCH/FACEBOOK/INSTAGRAM/LINKEDIN/DISPLAY/YOUTUBE/OTHER]
- Ad Format: [SEARCH AD/IMAGE AD/VIDEO AD/CAROUSEL/STORY/SPONSORED CONTENT]
- Campaign Goal: [AWARENESS/TRAFFIC/LEADS/CONVERSIONS/APP INSTALLS/ENGAGEMENT]
- Budget Level: [TESTING/SCALING/AGGRESSIVE]

**Product/Service:**
- Name: [YOUR PRODUCT/SERVICE]
- Category: [INDUSTRY/TYPE]
- Price Point: [FREE/BUDGET/MID-RANGE/PREMIUM]
- Primary Value Prop: [MAIN BENEFIT]

**Target Audience:**
- Who: [AUDIENCE DESCRIPTION]
- Awareness Level: [COLD/WARM/HOT - DO THEY KNOW YOU?]
- Pain Points: [WHAT PROBLEMS DO THEY HAVE?]
- Desires: [WHAT DO THEY WANT?]

**Campaign Context:**
- Offer: [DISCOUNT/FREE TRIAL/DEMO/DOWNLOAD/NONE]
- Urgency Elements: [LIMITED TIME/SCARCITY/NONE]
- Competitors: [WHO ARE YOU UP AGAINST?]

**Brand Voice:** [PROFESSIONAL/FRIENDLY/BOLD/LUXURY/PLAYFUL/URGENT]

**Constraints:**
- Character limits: [PLATFORM-SPECIFIC LIMITS]
- Must include: [REQUIRED ELEMENTS - BRAND NAME, KEYWORDS, ETC.]
- Avoid: [ANYTHING TO STAY AWAY FROM]
- Compliance: [ANY INDUSTRY REGULATIONS]

Please provide:
1. Multiple ad variations (3-5 complete ads)
2. A/B testing recommendations
3. Audience-specific messaging angles
4. Platform-specific optimization tips
5. Suggested ad extensions or additional elements
```text

---

## Variables

| Variable | Description |
|----------|-------------|
| `[GOOGLE SEARCH/FACEBOOK/INSTAGRAM/LINKEDIN/DISPLAY/YOUTUBE/OTHER]` | Where the ad will run |
| `[SEARCH AD/IMAGE AD/VIDEO AD/CAROUSEL/STORY/SPONSORED CONTENT]` | The format of the ad |
| `[AWARENESS/TRAFFIC/LEADS/CONVERSIONS/APP INSTALLS/ENGAGEMENT]` | What you want to achieve |
| `[YOUR PRODUCT/SERVICE]` | What you're advertising |
| `[AUDIENCE DESCRIPTION]` | Who you're targeting |
| `[COLD/WARM/HOT - DO THEY KNOW YOU?]` | How familiar the audience is with your brand |
| `[DISCOUNT/FREE TRIAL/DEMO/DOWNLOAD/NONE]` | Any special offer |
| `[PROFESSIONAL/FRIENDLY/BOLD/LUXURY/PLAYFUL/URGENT]` | The tone of your ads |
| `[PLATFORM-SPECIFIC LIMITS]` | Character or format restrictions |

---

## Example Usage

**Input:**

```text
You are an expert advertising copywriter who creates high-converting ad copy. Write compelling ad copy based on the following campaign brief:

**Campaign Overview:**
- Platform: Google Search
- Ad Format: Responsive Search Ad
- Campaign Goal: Lead generation (demo requests)
- Budget Level: Scaling (proven product, ready to grow)

**Product/Service:**
- Name: DataSync Pro
- Category: B2B SaaS / Data Integration
- Price Point: Premium ($500+/month)
- Primary Value Prop: Connect all your data sources in minutes, not months—no engineering team required

**Target Audience:**
- Who: Operations managers, data analysts, and business intelligence leads at mid-market companies (100-1000 employees)
- Awareness Level: Warm - actively searching for data integration solutions
- Pain Points: Data silos, manual data exports, waiting on engineering resources, inaccurate reports from outdated data
- Desires: Single source of truth, self-service data access, faster decision-making

**Campaign Context:**
- Offer: Free 14-day trial + personalized demo
- Urgency Elements: None (evergreen campaign)
- Competitors: Fivetran, Stitch, Airbyte, custom solutions

**Brand Voice:** Professional but not corporate, confident, technically credible

**Constraints:**
- Character limits: Headlines max 30 chars each (need 15), Descriptions max 90 chars each (need 4)
- Must include: "DataSync Pro" in at least 3 headlines, "demo" or "trial" in CTAs
- Avoid: "Cheap," "basic," anything that sounds entry-level
- Compliance: Standard B2B, no special requirements

Please provide:
1. Multiple ad variations (3-5 complete ads)
2. A/B testing recommendations
3. Audience-specific messaging angles
4. Platform-specific optimization tips
5. Suggested ad extensions or additional elements
```text

**Output:**

```text
# DataSync Pro - Google Search Ads Campaign

## Headlines Bank (15 Headlines, max 30 characters each)

### Brand + Core Value
1. "DataSync Pro® - Unify Data" (27)
2. "DataSync Pro Data Platform" (27)
3. "DataSync Pro® - Try Free" (25)

### Benefit-Focused
4. "Connect Data in Minutes" (24)
5. "End Data Silos Forever" (23)
6. "No Engineering Required" (24)
7. "One Source of Truth" (19)
8. "Real-Time Data Sync" (19)

### Pain Point
9. "Stop Manual Data Exports" (25)
10. "Tired of Data Silos?" (21)
11. "Skip the Engineering Queue" (27)

### Action/Offer
12. "Get Your Free Demo" (18)
13. "Start 14-Day Free Trial" (24)
14. "Book a Demo - See It Live" (25)
15. "Request Personalized Demo" (26)

---

## Descriptions Bank (4 Descriptions, max 90 characters each)

1. "Connect 200+ data sources in minutes. No code, no engineers. Start your free trial today." (89)

2. "DataSync Pro integrates your data stack without IT bottlenecks. Book a personalized demo now." (90)

3. "Unify your data in one platform. Self-service setup, enterprise security. Free 14-day trial." (90)

4. "Stop waiting on engineering. DataSync Pro gives you data access in minutes. See a live demo." (90)

---

## Responsive Search Ad Combinations (5 Variations)

### Ad Variation 1: Pain Point Focus
**Headlines:** Tired of Data Silos? | DataSync Pro® - Unify Data | Start 14-Day Free Trial
**Description:** Connect 200+ data sources in minutes. No code, no engineers. Start your free trial today.

### Ad Variation 2: Speed Focus
**Headlines:** Connect Data in Minutes | No Engineering Required | DataSync Pro® - Try Free
**Description:** Stop waiting on engineering. DataSync Pro gives you data access in minutes. See a live demo.

### Ad Variation 3: Outcome Focus
**Headlines:** One Source of Truth | DataSync Pro Data Platform | Get Your Free Demo
**Description:** Unify your data in one platform. Self-service setup, enterprise security. Free 14-day trial.

### Ad Variation 4: Competitive Differentiation
**Headlines:** Skip the Engineering Queue | DataSync Pro® - Unify Data | Book a Demo - See It Live
**Description:** DataSync Pro integrates your data stack without IT bottlenecks. Book a personalized demo now.

### Ad Variation 5: Direct Response
**Headlines:** DataSync Pro® - Try Free | Real-Time Data Sync | Request Personalized Demo
**Description:** Connect 200+ data sources in minutes. No code, no engineers. Start your free trial today.

---

## A/B Testing Recommendations

### Test 1: Pain vs. Gain Framing
- **A:** "Stop Manual Data Exports" / "Tired of Data Silos?"
- **B:** "Connect Data in Minutes" / "One Source of Truth"
- **Hypothesis:** Pain points may drive higher CTR from problem-aware audiences, but gain-framing may convert better.

### Test 2: Offer Prominence
- **A:** Lead with "Free Trial" in Headline 1
- **B:** Lead with benefit, trial in Headline 3
- **Hypothesis:** Testing whether the offer or the value prop is more compelling for this audience.

### Test 3: Technical vs. Business Language
- **A:** "200+ Data Sources" / "Real-Time Sync"
- **B:** "One Source of Truth" / "Faster Decisions"
- **Hypothesis:** Analysts may prefer technical; managers may prefer business outcomes.

### Test 4: Demo vs. Trial CTA
- **A:** "Book a Demo"
- **B:** "Start Free Trial"
- **Hypothesis:** Some users want hands-on evaluation; others prefer guided experience.

---

## Audience-Specific Messaging Angles

### For Data Analysts
**Angle:** Technical capability + self-service
**Headlines:** "200+ Connectors, Zero Code" / "Skip the SQL Queue"
**Message:** Emphasize they can do it themselves without waiting on engineering

### For Operations Managers
**Angle:** Time savings + reliability
**Headlines:** "Automate Data Pipelines" / "End Manual Exports"
**Message:** Focus on eliminating tedious manual work and errors

### For BI Leads
**Angle:** Single source of truth + trust
**Headlines:** "Trusted Data for BI" / "One Source of Truth"
**Message:** Emphasize data quality and decision-making confidence

### For CTOs/Tech Decision-Makers
**Angle:** Enterprise-ready + ROI
**Headlines:** "Enterprise Data Integration" / "No More Engineering Backlog"
**Message:** Focus on freeing up engineering resources for strategic work

---

## Platform-Specific Optimization Tips

### Google RSA Best Practices

1. **Pin strategically:** Pin brand name headline to Position 1 for brand consistency, but leave other positions dynamic for Google to optimize.

2. **Use keyword insertion:** Consider `{KeyWord:Data Integration}` in one headline to improve relevance scores.

3. **Match search intent:** These keywords suggest high commercial intent—emphasize demo/trial CTAs prominently.

4. **Quality Score focus:** Ensure landing page closely matches ad messaging (mention "minutes, not months" and "no engineering" prominently).

5. **Mobile optimization:** Test shorter headlines for mobile devices where truncation is more common.

---

## Suggested Ad Extensions

### Sitelinks (4)
1. **"See Pricing"** → Pricing page
2. **"200+ Integrations"** → Integrations directory
3. **"Customer Stories"** → Case studies page
4. **"How It Works"** → Product tour or demo video

### Callouts (4-6)
- "Free 14-Day Trial"
- "No Credit Card Required"
- "Setup in Minutes"
- "SOC 2 Certified"
- "200+ Data Sources"
- "24/7 Support"

### Structured Snippets
- **Types:** CRM, ERP, Cloud Storage, Marketing Tools, Databases, APIs
- **Features:** Real-Time Sync, No-Code Setup, Enterprise Security, Automated Scheduling

### Call Extension
- Add phone number for enterprise prospects who prefer to talk to sales

### Lead Form Extension
- Test direct lead form for "Request Demo" with fields: Name, Email, Company Size, Current Data Stack

---

## Performance Benchmarks to Target

Based on B2B SaaS search campaigns in this category:

| Metric | Target Range |
|--------|-------------|
| CTR | 3-5% |
| Conversion Rate | 2-4% |
| Cost Per Lead | $50-150 |
| Quality Score | 7+ |

---

## Quick Win Recommendations

1. **Create ad group segmentation** by keyword intent (brand, competitor, feature, pain point) with tailored messaging for each

2. **Build a dedicated landing page** that mirrors ad messaging—don't send to homepage

3. **Set up conversion tracking** for demo requests AND trial starts to optimize for both

4. **Start with Target CPA bidding** once you have 15+ conversions, then test Maximize Conversions

5. **Review search terms weekly** to add negatives and find new opportunities
```text

---

## Tips

- **Match message to intent:** Cold audiences need education; warm audiences need differentiation; hot audiences need a clear CTA
- **Front-load value:** Put your strongest benefit at the beginning—many platforms truncate copy
- **Respect platform culture:** LinkedIn ads feel different from Instagram ads—match the environment
- **Include social proof when possible:** Numbers, awards, and testimonials boost credibility (if space allows)
- **Test systematically:** Change one element at a time to understand what's actually driving performance
- **Write for the click, but optimize for conversion:** CTR matters, but conversion rate and cost-per-acquisition matter more

---

## Related Prompts

- [Headline and Tagline Creator](headline-tagline-creator.md)
- [Social Media Content Generator](social-media-content-generator.md)
- [Product Description Generator](product-description-generator.md)
- [Email Newsletter Writer](email-newsletter-writer.md)
