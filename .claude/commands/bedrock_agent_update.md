# /bedrock_agent_update - Update Existing Sites & Articles

Update content on **existing** domains and articles while maintaining 100% fidelity to the site's writing style, CSS, layout, and quality standards.

**Arguments:** $ARGUMENTS

---

## Phase 0.5: Log Session Start (MANDATORY)

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action execute --summary "Started /bedrock_agent_update session" --username $(whoami) --command bedrock_agent_update
```

---

## Purpose

This command is for **updating existing sites** — NOT creating new ones. When updating, the source site IS the style guide. Every aspect of generated content must match the original exactly:

- Writing voice, tone, and personality
- British/American English spelling conventions
- Article structure (headings, paragraphs, image placement)
- CSS classes, colours, fonts, and spacing
- URL patterns and navigation structure
- Review scoring systems (if applicable)
- Byline and date formatting
- Category and tag taxonomy

> **Rule:** The site's existing content is the ONLY authority. Do NOT apply `/bedrock_agent` scaffold rules, Astro templates, or Docsify defaults. Match what exists.

---

## Phase 0: RAG Context Loading (MANDATORY)

Load relevant context from past sessions:

```bash
# Read recent learnings
ls ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/ | tail -5
ls ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/ | tail -5

# Read feedback corrections
cat ~/pitaya/knowledge/feedback_corrections.md | head -100
```

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│              BEDROCK AGENT UPDATE PROTOCOL                           │
│              (EXISTING SITE FIDELITY MODE)                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STEP 1: SITE SCAN & STYLE EXTRACTION                                │
│  ────────────────────────────────────                                │
│  • Fetch the live site homepage + 3-5 sample articles                │
│  • Extract: writing voice, CSS patterns, HTML structure              │
│  • Document the site's "style bible" (auto-generated)                │
│  • Identify article types (review, news, feature, guide, etc.)       │
│                                                                      │
│  STEP 2: CONTENT PLANNING                                            │
│  ────────────────────────                                            │
│  • Propose articles/updates with titles matching site conventions     │
│  • Map each to the correct article type template                     │
│  • Assign to appropriate categories & tags                           │
│  • Present plan to user for approval                                 │
│                                                                      │
│  STEP 3: CONTENT GENERATION (STYLE-LOCKED)                           │
│  ──────────────────────────────────────────                          │
│  • Write content matching the extracted style bible exactly           │
│  • Generate HTML using the site's actual CSS classes                  │
│  • Maintain the site's image patterns and alt text conventions        │
│  • Apply the site's scoring system (if reviews)                      │
│                                                                      │
│  STEP 4: STYLE FIDELITY QA (3 GATES)                                │
│  ─────────────────────────────────────                               │
│  • Gate 1: Writing Style Match (voice, tone, spelling, structure)    │
│  • Gate 2: Visual/CSS Match (classes, layout, responsiveness)        │
│  • Gate 3: Editorial Standards (accuracy, sourcing, SEO)             │
│                                                                      │
│  STEP 5: LOCAL REVIEW                                                │
│  ────────────────────                                                │
│  • Generate local HTML files for browser preview                     │
│  • Present to user for approval                                      │
│  • Iterate if needed                                                 │
│                                                                      │
│  STEP 6: REFLECT                                                     │
│  ───────────────                                                     │
│  • Capture learnings about the site's style                          │
│  • Store style bible for future updates to the same site             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Interactive Menu

When invoked, present this menu:

```
BEDROCK AGENT — UPDATE MODE
════════════════════════════════════════════════════════

What would you like to update?

  3. Update an existing domain
     → Refresh multiple pages, add new articles to a site
     → Full site scan, batch content generation

  4. Update an existing article
     → Rewrite or refresh a single article
     → Precision style matching for one page

════════════════════════════════════════════════════════
```

Use `AskUserQuestion` with these two options. Then ask for the target URL.

---

## Step 0.5: API Leak Compliance Context (MANDATORY — R-SEO-04)

**CRITICAL:** The SEO Strategy Knowledge Base at `https://seo-strategy-hphbw.sevalla.app/api-leak` is the CORE guide for all content updates. Before modifying ANY content, assess the impact on Google's API leak parameters.

**Load API Leak Context:**

```bash
# 1. Load the API leak standard
cat ~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md

# 2. Check if domain has an existing API leak diagnosis
curl -s "https://seo-strategy-hphbw.sevalla.app/api/audits/{domain}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data: print(f'Prior audit: {data[\"date\"]} — Risk: {data[\"risk_level\"]}')
else: print('No prior audit — run /A_Virtual_Team with API leak analysis first')
"

# 3. Get current site metrics from PostHog (if available)
# Check gambling ratio, pogo rate, dwell time, scroll depth
```

**Pre-Update Impact Assessment:**

Before generating or modifying content, evaluate these parameters:

| Parameter | What to Check | Impact of Update |
|-----------|--------------|-----------------|
| `siteFocusScore` | Does the new content stay within the site's declared vertical? | Off-topic content lowers focus score |
| `numOfGamblingPages` | Will update change the gambling-to-editorial ratio? | Adding money pages without editorial = ratio spike |
| `contentEffort` | Is the updated content higher effort than what it replaces? | Never reduce content quality in an update |
| `rhubarb` | Will the update create quality gaps between page types? | Money page updates must match site avg quality |
| `racterScores` | Is the content AI-generated? If so, add unique human data | Pure AI content flags automated production |
| `freshboxArticleScores` | Are timestamps and dates being updated honestly? | No false freshness (R-CONTENT-05a) |
| `affiliateLinkDensity` | Will the update increase affiliate link density? | Max 1 sponsored link per 300 words |
| `anchorMismatchDemotion` | Are internal links topically relevant? | R-ANCHOR-01 keyword-rich anchors required |

**HARD RULE:** If an update would push gambling ratio above 5% or create a rhubarb quality delta > 35%, the update is BLOCKED until counterbalancing editorial content is added.

---

## Step 1: Site Scan & Style Extraction

### For Option 3 (Update Existing Domain)

Scan the full site to build a comprehensive style bible:

1. **Fetch homepage** — Navigation, layout, hero patterns, sidebar widgets
2. **Fetch 3-5 articles** across different categories (reviews, news, features)
3. **Extract CSS patterns** — Colour scheme, font stack, spacing, card layouts
4. **Analyse writing style** per article type:

```markdown
## Auto-Generated Style Bible: [SITE NAME]

### Voice & Tone
- Perspective: [First person / Third person / Mixed]
- Register: [Casual / Professional / Academic]
- Humour: [Frequent / Occasional / Rare / None]
- Regional English: [British / American / Australian]

### Article Types Found
| Type | Title Convention | Structure | Avg Length |
|------|-----------------|-----------|------------|
| Review | [Pattern] | [Headings?] | [Words] |
| News | [Pattern] | [Headings?] | [Words] |
| Feature | [Pattern] | [Headings?] | [Words] |

### HTML Patterns
- Article container: [CSS class]
- Title element: [h1/h2 + class]
- Author byline: [format]
- Date format: [pattern]
- Image handling: [sizes, alt text, captions]
- Score display: [format, if applicable]

### CSS Variables / Theme
- Primary colour: [hex]
- Secondary colour: [hex]
- Font family: [stack]
- Link colour: [hex]
- Heading weight: [bold/normal]

### URL Patterns
- Reviews: [pattern]
- News: [pattern]
- Features: [pattern]

### Category & Tag Taxonomy
- Categories: [list]
- Tag patterns: [convention]
```

### For Option 4 (Update Existing Article)

Focused scan on the single article + 2 articles of the same type:

1. **Fetch the target article** — Full HTML + content analysis
2. **Fetch 2 similar articles** (same category/type) for style calibration
3. **Build focused style profile** for that article type only

---

## Step 2: Content Planning

### For Option 3 (Domain Update)

Present a content plan:

```markdown
## Content Plan: [SITE NAME]

**Proposed Articles:**

| # | Title | Type | Category | Target Topic |
|---|-------|------|----------|-------------|
| 1 | [Matching site convention] | Review | [Existing cat] | [Topic] |
| 2 | [Matching site convention] | News | [Existing cat] | [Topic] |

**Style Lock:**
- Voice: [Extracted from scan]
- Format: [Extracted from scan]
- Scoring: [Extracted from scan]

Approve this plan? (Yes / Edit / Cancel)
```

### For Option 4 (Article Update)

Present a focused update plan:

```markdown
## Article Update Plan

**Original:** [Title + URL]
**Update Type:** [Rewrite / Refresh / Expand]
**Changes Proposed:**
- [Specific change 1]
- [Specific change 2]

**Style Lock:** [Same as original article]

Approve? (Yes / Edit / Cancel)
```

---

## Step 3: Content Generation (Style-Locked)

### Writing Rules (CRITICAL)

These rules override ALL other content generation defaults:

1. **Voice match** — If the site uses first person, write in first person. If third person, use third person. No exceptions.
2. **Spelling match** — If the site uses British English ("colour", "favourite"), use British English throughout. Check the site, not your defaults.
3. **Structure match** — If reviews have NO section headings, do NOT add section headings. If news articles use H2s, use H2s. Mirror exactly.
4. **Length match** — Count the average paragraph count and word count of existing articles of the same type. Match within 10%.
5. **Tone match** — If the site is irreverent and casual, be irreverent and casual. If formal, be formal. Read 3+ examples to calibrate.
6. **Title match** — Follow the site's exact title convention (lowercase "review", pipe separators for lists, etc.).
7. **No invented patterns** — Never add structures (pros/cons boxes, star ratings, callout blocks) that don't exist on the site.
8. **Image conventions** — Match alt text style, image sizes, placement between paragraphs.
9. **Scoring system** — Use the site's exact scoring format. Do NOT change the scale or display method.
10. **Categories/tags** — Only use categories and tags that already exist on the site.

### HTML Output

Generate HTML that uses the site's actual CSS classes:

```html
<!-- Match the site's exact article wrapper -->
<article class="[site-specific-class]">
  <header>
    <h1 class="[site-specific-class]">[Title in site convention]</h1>
    <span class="[byline-class]">[Author format matching site]</span>
    <time datetime="[ISO-8601]">[Date in site format]</time>
  </header>

  <div class="[content-class]">
    <!-- Content paragraphs matching site structure exactly -->
    <p>[Opening paragraph matching site voice]</p>

    <!-- Images placed where the site typically places them -->
    <img src="[placeholder]" alt="[alt text in site convention]"
         width="[site-standard]" height="[site-standard]">

    <p>[Body content in site voice]</p>
  </div>
</article>
```

### Local File Output

Save generated content to:

```
/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/updates/[site-slug]/
├── style_bible.md          # Auto-generated style reference
├── articles/
│   ├── article-1.html      # Individual article files
│   ├── article-2.html
│   └── ...
├── preview/
│   └── index.html          # Local preview page (links to all articles)
└── CONTENT_PLAN.md         # Approved content plan
```

---

## Step 4: Style Fidelity QA (3 Gates)

### Gate 1: Writing Style Match (B-NINA + W-VERA)

| Check | Pass Criteria |
|-------|--------------|
| Voice perspective | Matches site (1st/3rd person) |
| Regional English | Correct spelling variant throughout |
| Tone calibration | Reads like existing site content |
| Paragraph structure | Length and count within 10% of site average |
| Title convention | Follows site's exact pattern |
| No invented elements | Zero structures not found on original site |

**Threshold:** ALL checks must pass. This is binary, not scored.

### Gate 2: Visual/CSS Match (B-MAX + W-MAYA)

| Check | Pass Criteria |
|-------|--------------|
| CSS classes | All classes exist on original site |
| HTML structure | Matches site's article template |
| Image dimensions | Consistent with site standards |
| Responsive patterns | Same breakpoints as original |

**Threshold:** ALL checks must pass.

### Gate 3: Editorial Standards (B-RANK + W-LARS)

| Check | Pass Criteria |
|-------|--------------|
| Factual accuracy | All claims verified via web search |
| SEO consistency | Meta patterns match existing pages |
| Internal linking | Category/tag taxonomy respected |
| URL slug format | Matches site's URL convention |

**Threshold:** ALL checks must pass.

### Gate 4: API Leak Compliance (B-RANK + W-LUNA) — R-SEO-04

| Check | Pass Criteria |
|-------|--------------|
| Topical coherence | New content stays within site's declared vertical (`siteFocusScore`) |
| Gambling ratio | After update, gambling pages remain < 5% of indexed total (`numOfGamblingPages`) |
| Quality delta | Money page quality within 20% of site avg (`rhubarb`) |
| Content effort | Updated content is higher effort than what it replaces (`contentEffort`) |
| Affiliate density | Max 1 sponsored link per 300 words (`affiliateLinkDensity`) |
| Freshness honesty | No false update timestamps, real content changes only (`lastSignificantUpdate`) |
| Anchor text | Internal links use keyword-rich anchors per R-ANCHOR-01 |

**Threshold:** ALL checks must pass. Gambling ratio > 5% = BLOCKED.

### R-DATA-07 Compliance (MANDATORY)

All numerical comparisons in content must pass the 4-step check:
1. **Extract** the numbers being compared
2. **Compare** them mathematically
3. **Verify** the language matches the direction (above/below/higher/lower)
4. **Confirm** no inversions exist

---

## Step 5: Local Review

Generate a self-contained preview page:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Content Preview: [Site Name]</title>
  <style>
    /* Inline the site's core CSS for local preview */
    body { font-family: [site-font]; }
    /* ... key styles extracted from site ... */
  </style>
</head>
<body>
  <h1>Content Preview</h1>
  <p>Generated: [date] | Articles: [count]</p>

  <nav>
    <ul>
      <li><a href="articles/article-1.html">Article 1 title</a></li>
      <!-- ... -->
    </ul>
  </nav>

  <hr>
  <p><em>Open individual article files in browser to preview.</em></p>
</body>
</html>
```

Present the file path to the user:
```
Local preview ready at:
  /home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/updates/[site-slug]/preview/index.html

Open in browser to review. No deployment — local only.
```

---

## Step 6: Reflect

Capture learnings about the site's style for future updates:

```bash
# Save style bible for future reference
cp style_bible.md ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/[site-slug]_style_bible.md

# Capture session learnings
# Invoke /reflect
```

---

## Team Assignments

| Phase | BlackTeam | WhiteTeam |
|-------|-----------|-----------|
| Site Scan | B-NINA (Content), B-MAX (UX) | — |
| Content Plan | B-NINA, B-CONT, B-RANK | W-NINA (Editorial) |
| Content Gen | B-CONT (Production), B-NINA (Voice) | — |
| QA Gate 1 | B-NINA | W-VERA (Content QA) |
| QA Gate 2 | B-MAX | W-MAYA (Accessibility) |
| QA Gate 3 | B-RANK | W-LARS (SEO) |
| Local Review | B-POST | W-QUIN (QA Lead) |

---

## Key Differences from `/bedrock_agent`

| Aspect | `/bedrock_agent` (New) | `/bedrock_agent_update` (Existing) |
|--------|----------------------|----------------------------------|
| Source of truth | Bedrock Agent rules & templates | The existing site itself |
| HTML framework | Docsify or Astro scaffold | Site's actual HTML/CSS |
| Writing style | Defined by content style setting | Extracted from live site |
| QA focus | 5 Ralph Loops (content + technical) | 3 Style Fidelity Gates |
| Deployment | Git + Vercel | Local preview only (user decides) |
| Content structure | Generated from scratch | Must match existing patterns |
| CSS/design | Theme variables from config | Site's actual stylesheet |

---

## R-SEC-01 Compliance

- NO hardcoded API keys in generated files
- Load any API keys from `~/.keys/.env`
- Scan all output for: `phx_`, `phc_`, `pk_`, `sk-`, `ntn_`, `AIzaSy`, `xoxb-`

### Red Team Challenge (R-WORKFLOW-02 — MANDATORY, NEVER SKIP)

**DELIVERY BLOCKED until Red Team passes. This phase is NON-NEGOTIABLE.**

Before deploying updates or marking session complete:

1. **R-REX reviews** all updated content and style fidelity
2. **Execute applicable Red Gates:**
   - RG-1: Validation Integrity — did Fidelity Gates actually validate style match? (100%)
   - RG-2: Adversarial Edge Cases — broken layouts, missing assets, encoding (95%)
   - RG-3: Regression & Drift — do updates break existing pages? (100%)
   - RG-4: Systemic Bias — gambling ratio check, brand balance (95%)
   - RG-5: Security — no leaked keys, CSP intact (100%)
   - RG-7: Root Cause & Pattern — no known anti-pattern repetition (100%)

3. **Challenge Report:** `CERTIFIED` to proceed, `FLAGGED` to fix (max 2 cycles)

**If RedTeam is skipped:** The session is NON-COMPLIANT with R-WORKFLOW-02.

### Final: Log Session Completion

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action complete --summary "Completed /bedrock_agent_update session" --username $(whoami) --command bedrock_agent_update
```

---

## R-DEBUG-01 Compliance

Before any action on live content:
1. Verify the URL is accessible
2. Test fetches return expected content
3. Validate HTML parsing succeeds
4. Only proceed after local verification passes
