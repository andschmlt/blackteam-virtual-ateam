# /launch_site - End-to-End Site Launch Pipeline

Build a complete content site from zero to production in one guided workflow. Orchestrates `/bedrock_agent`, `/content_palm`, TechOps TopList, `/news_update_agent`, GCP automation, and SEO audits into a strict 8-phase pipeline.

**Reference:** `memory/content_pipeline_flow.md` (architecture overview)

---

## Arguments

```
/launch_site [domain-name-or-project-description]
```

Arguments: $ARGUMENTS

---

## How It Works

```
/launch_site
    │
    ▼
Phase 1: INTAKE WIZARD (collect all inputs)
    │
    ▼
Phase 2: STRUCTURE (/bedrock_agent)
    │
    ▼
Phase 3: MONEY PAGES (/content_palm + TechOps TopList)
    │  ↳ Select writer pool via CW-R9 (GEO) + CW-R10 (content type)
    │    25 writers available — see CONTENT_WRITER_RULES.md
    ▼
Phase 4: FIRST DEPLOY (Vercel + DNS)
    │
    ▼
Phase 4.5: POSTHOG + NAVBOOST (18 KPI metrics)
    │
    ▼
Phase 5: SEO AUDIT — STATIC (seo-toolkit audit-static)
    │
    ▼
Phase 6: SEO FIXES (fix all issues from Phase 5)
    │
    ▼
Phase 7: NEWS AUTOMATION (GCP Cloud Run + Scheduler)
    │  ↳ Assign writer rotation per site — CW-R9 GEO pool
    │    Track in data/writer_rotation.json (no 3x consecutive)
    ▼
Phase 8: SEO AUDIT — LIVE (seo-toolkit audit + GSC)
    │
    ▼
LAUNCH COMPLETE — Triple Sign-Off
```

---

## Phase 0: Context Loading (DEFERRED — Load Per Phase)

**IMPORTANT:** Do NOT load all learnings and standards upfront. Load them as each phase begins. This preserves context for actual work.

### 0A: Always Load (before Phase 1)
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07

### 0B: Log Session Start
```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action execute --summary "Started /launch_site session" --username $(whoami) --command launch_site
```

### Deferred Loading Schedule

**When entering Phase 2 (Structure),** load:
- `~/.claude/standards/ASTRO_TECHNICAL_SEO_RULES.md` — R-SEO-03
- `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` — R-IMG-01
- BlackTeam learnings matching bedrock/astro/structure:
  ```bash
  ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*bedrock* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*astro* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*seo_standards* 2>/dev/null | head -5
  ```

**When entering Phase 3 (Money Pages),** load:
- `~/.claude/standards/PALM_CONTENT_RULES.md`
- `~/.claude/standards/ANCHOR_TEXT_RULES.md` — R-ANCHOR-01
- `~/.claude/standards/ANCHOR_DISTRIBUTION_RULES.md` — R-ANCHOR-02
- BlackTeam learnings matching palm/toplist/money:
  ```bash
  ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*palm* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*toplist* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*money* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*betting* 2>/dev/null | head -5
  ```

**When entering Phase 4.5 (PostHog),** load:
- `~/.claude/standards/POSTHOG_RULES.md`

**When entering Phase 5-6 (SEO Audit),** load:
- BlackTeam/WhiteTeam SEO learnings:
  ```bash
  ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*seo_audit* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*screaming_frog* ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/*seo* 2>/dev/null | head -5
  ```

**When entering Phase 7 (News Automation),** load:
- BlackTeam learnings matching news/editorial/cloud_run:
  ```bash
  ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*news* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*editorial* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*content_writer* 2>/dev/null | head -5
  ```
- Security standards (Cloud Run deploy):
  - `~/.claude/standards/SECRETS_ROTATION_SCHEDULE.md` — R-SEC-06
  - `~/.claude/standards/INPUT_VALIDATION_RULES.md` — R-SEC-02
  - `~/.claude/standards/CORS_SECURITY_RULES.md` — R-SEC-03
  - `~/.claude/standards/CRYPTOGRAPHY_RULES.md` — R-SEC-04

**When entering Phase 8B (API Leak Diagnosis),** load:
- `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md` — R-SEO-04
- SEO Strategy KB API (`https://seo-strategy-hphbw.sevalla.app/api-leak`) — 206 parameters
  - `/api/api-leak/categories` — parameter categories
  - `/api/api-leak/params?q={param}` — individual parameter lookup
  - `/api/audits/{domain}` — check for prior audit
  - Fallback if API unreachable: use the local GOOGLE_API_LEAK_DIAGNOSIS.md standard

**Do NOT preload all standards at Phase 0. Read each file only when its phase starts.**

---

## Phase 1: INTAKE WIZARD

**MANDATORY — Collect ALL inputs before any execution.**

Present the wizard as a numbered questionnaire. Wait for user answers before proceeding. Do NOT assume defaults without confirmation.

### 1A: Project Identity

Ask the user:

```
┌──────────────────────────────────────────────────────────┐
│  LAUNCH SITE — INTAKE WIZARD                             │
│                                                          │
│  1. Domain name?                                         │
│     (e.g., australiafootball.com, europeangaming.eu)     │
│                                                          │
│  2. Project title?                                       │
│     (e.g., "Australia Football Hub", "European Gaming")  │
│                                                          │
│  3. Vertical category?                                   │
│     [ ] Sports    [ ] Gaming    [ ] Entertainment        │
│     [ ] Business  [ ] Travel    [ ] Custom: ________     │
│                                                          │
│  4. Sub-category?                                        │
│     (e.g., Football, Esports, F1, Cricket, iGaming)     │
│                                                          │
│  5. Geographic scope?                                    │
│     [ ] Local     [ ] National  [ ] National Hub         │
│     [ ] International                                    │
│                                                          │
│  6. Country? (if local/national)                         │
│     (e.g., Australia, Germany, Malta)                    │
│                                                          │
│  7. Content style?                                       │
│     [ ] Journalism  [ ] Statistical  [ ] Travel & Venue  │
│     [ ] Encyclopedia  [ ] Mixed                          │
│                                                          │
│  8. Content scope?                                       │
│     [ ] Starter (20 players / 10 teams)                  │
│     [ ] Standard (80 / 24)                               │
│     [ ] Enterprise (150+ / 48+)                          │
│     [ ] Hub (200+ / 60+ / multi-sport)                   │
│                                                          │
│  9. Theme & design approach?                             │
│     [ ] KEEP EXISTING — Preserve the current live site's │
│         theme, menu, layouts, sections, and styles.       │
│         (Site must already be live at the domain.)        │
│         → Phase 2 will SCRAPE the existing site to       │
│           extract CSS, navigation, layout structure,     │
│           component patterns, and rebuild in Astro       │
│           with pixel-perfect fidelity.                   │
│     [ ] BUILD NEW — Create a fresh theme from scratch    │
│         using /bedrock_agent defaults for the vertical.  │
│         (For brand-new domains or full redesigns.)       │
│     [ ] HYBRID — Keep navigation + brand colors but      │
│         modernize layout and components.                 │
│         → Scrape nav + color palette, build new layout.  │
│                                                          │
│     If KEEP EXISTING:                                    │
│     9a. Live site URL to scrape: ______________________  │
│         (default: https://www.{domain from Q1}/)         │
│     9b. Pages to scrape for reference (comma-sep):       │
│         [ ] Auto-detect (homepage + 5 key pages)         │
│         [ ] Custom: ______________________________       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**NOTE on Q9:** This is a **critical fork point**. When "KEEP EXISTING" is selected:
- Phase 2 runs a site scrape BEFORE `/bedrock_agent`, extracting the live site's HTML/CSS structure
- The scraped assets become the design reference for the Astro build
- All CSS tokens, color variables, font stacks, spacing, and component patterns are preserved
- Navigation structure (menu items, dropdowns, order) is replicated exactly
- This is the approach used for australiafootball.com — the WordPress theme was scraped and rebuilt pixel-perfect in Astro

When "BUILD NEW" is selected:
- Phase 2 runs `/bedrock_agent` with default Astro theme generation
- Fresh design tokens, navigation, and layout from bedrock's vertical templates

### 1B: Money Pages

```
┌──────────────────────────────────────────────────────────┐
│  MONEY PAGES                                             │
│                                                          │
│  10. Money page types needed?                            │
│      [ ] Betting roundup     [ ] Casino roundup          │
│      [ ] Both                [ ] None (skip Phase 3)     │
│                                                          │
│  11. ClickUp content task ID(s)?                         │
│      (Single source of truth: contains TopList ID,       │
│       brand lineup, Dragon cloaked links, SEO keywords)  │
│      Betting task ID: _____________                      │
│      Casino task ID:  _____________                      │
│      (e.g., 863gbtb0p, 86afp6hge)                       │
│                                                          │
│  12. Confirm from ClickUp task (auto-extracted):         │
│      a) TechOps TopList ID:  _______ (per money page)   │
│      b) Brand lineup:        [extracted from task]       │
│      c) SEO target keywords: [extracted from task]       │
│      d) Target geo:          [extracted from task]       │
│                                                          │
│  13. Dragon cloaked affiliate links?                     │
│      [ ] Yes — links use linkaly.net SP domain           │
│          (PREFERRED — all affiliate URLs go through      │
│           Dragon link cloaking before Palm generation)   │
│      [ ] Not yet — FLAG as blocker, must be set up       │
│          before Phase 3 execution                        │
│      [ ] Raw tracking links (fallback only, document     │
│          reason: ________________________________)       │
│                                                          │
│  14. Palm content type?                                  │
│      [ ] roundup-review (standard)                       │
│      [ ] roundup-review-sp (single product)              │
│      [ ] single-review                                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**NOTE on Q11:** The ClickUp task is the SINGLE SOURCE OF TRUTH for money pages. Use the ClickUp API to extract TopList ID, brand lineup, Dragon links, target geo, and SEO keywords. NEVER ask for these separately if a task ID is provided.

**NOTE on Q13:** Dragon cloaking is REQUIRED for production money pages. If links aren't cloaked yet, this is a **hard blocker** — Phase 3 cannot proceed until Dragon links are configured in ClickUp. Raw tracking links are a temporary fallback only (e.g., Dragon /go/ routes not configured for the domain yet).

### 1C: News Automation

```
┌──────────────────────────────────────────────────────────┐
│  NEWS AUTOMATION                                         │
│                                                          │
│  15. Enable automated news pipeline?                     │
│      [ ] Yes  [ ] No (skip Phase 7)                      │
│                                                          │
│  16. RSS feeds (comma-separated URLs or "auto-detect"):  │
│      _________________________________________________   │
│                                                          │
│  17. Daily article targets?                              │
│      RSS news per day:       [5]  (default)              │
│      AI editorial per day:   [3]  (default)              │
│                                                          │
│  18. Editorial writer personas?                          │
│      [ ] Use defaults:                                   │
│          B-LUCA (Breaking, 97.5% grammar)                │
│          B-EMMT (Features, 99.8% grammar)                │
│          B-VICS (Opinion, 99% grammar)                   │
│          B-ALIS (Analysis, 100% grammar)                 │
│          B-NATE (Roundups, 98% grammar)                  │
│      [ ] Custom (provide later)                          │
│                                                          │
│  19. Scheduler timezone?                                 │
│      (e.g., Australia/Sydney, Europe/London)             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 1D: Analytics

```
┌──────────────────────────────────────────────────────────┐
│  POSTHOG ANALYTICS                                       │
│                                                          │
│  20. Enable PostHog + NavBoost tracking?                 │
│      [ ] Yes (create project + full NavBoost KPIs)       │
│      [ ] No (skip Phase 4.5)                             │
│                                                          │
│  21. PostHog project?                                    │
│      [ ] Create new project (auto via API)               │
│      [ ] Use existing — Project ID: _____________        │
│                                                          │
│  22. NavBoost CTA selectors? (for money page tracking)   │
│      [ ] Use defaults:                                   │
│          [data-toplist] a, a[rel="sponsored"],            │
│          .cta-button, a[href*="/go/"]                     │
│      [ ] Custom: ________________________________        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 1E: Infrastructure

```
┌──────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE                                          │
│                                                          │
│  23. Hosting?                                            │
│      [ ] Vercel (default)  [ ] Other: ____________       │
│                                                          │
│  24. GitHub repo name?                                   │
│      Org: ParadiseMediaOrg (always)                      │
│      Repo name: _____________ (default: domain name)     │
│      e.g., "australiafootball.com" → ParadiseMediaOrg/   │
│            australiafootball.com                          │
│      Visibility: [ ] Private (default)  [ ] Public       │
│                                                          │
│  25. Custom domain? (if yes, provide)                    │
│      [ ] Yes: ____________  [ ] No (use vercel.app)      │
│                                                          │
│  26. GCP project for Cloud Run?                          │
│      (e.g., paradisemedia-bi)                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**NOTE on Q24:** A NEW repo is ALWAYS created in `ParadiseMediaOrg` for every `/launch_site` run. The default repo name is the domain name from Q1. This is non-negotiable — every site gets its own repo.

### 1F: Confirmation

After collecting all answers, present a summary table:

```markdown
## Launch Site — Confirmed Configuration

| Setting | Value |
|---------|-------|
| Domain | [Q1] |
| Title | [Q2] |
| Vertical | [Q3] → [Q4] |
| Geo | [Q5] / [Q6] |
| Style | [Q7] |
| Scope | [Q8] |
| **Theme approach** | **[Q9: KEEP EXISTING / BUILD NEW / HYBRID]** |
| Scrape URL | [Q9a — if KEEP/HYBRID] |
| **Money pages** | [Q10] |
| ClickUp task(s) | Betting: [Q11a] / Casino: [Q11b] |
| TopList IDs | [extracted from ClickUp task] |
| Brand lineup | [extracted from ClickUp task] |
| SEO keywords | [extracted from ClickUp task] |
| Dragon links | [Q13: Yes/Not yet/Raw fallback] |
| Palm content type | [Q14] |
| **News pipeline** | [Q15] — [Q17] articles/day |
| Writers | [Q18: defaults or custom] |
| Timezone | [Q19] |
| **PostHog** | [Q20: Yes/No] |
| PostHog project | [Q21: new/existing ID] |
| CTA selectors | [Q22: defaults/custom] |
| **Hosting** | [Q23] |
| GitHub repo | ParadiseMediaOrg/[Q24] (NEW) |
| Visibility | [private/public] |
| Custom domain | [Q25] |
| GCP project | [Q26] |

### Blockers (resolve before proceeding)
- [ ] Dragon links configured? (Q13 = "Not yet" → BLOCKER)
- [ ] ClickUp task IDs valid? (Q11 provided → verify via API)
- [ ] If KEEP EXISTING: live site accessible? (Q9a URL returns 200)

Proceed? (yes/no)
```

**HARD GATE:** Do NOT proceed until user confirms AND all blockers are resolved.

---

## Phase 2: STRUCTURE — /bedrock_agent

**Purpose:** Create the Astro project with all content collections, pages, and components.

**CRITICAL FORK — Based on Q9 (Theme Decision):**

### Path A: KEEP EXISTING (Q9 = "Keep Existing" or "Hybrid")

When the user wants to preserve the current live site's design, we MUST scrape and replicate it before generating content.

**Phase 2-KEEP: Site Scrape & Astro Rebuild**

#### 2-KEEP-A: Scrape the Existing Site

```bash
# 1. Fetch homepage + key pages (from Q9b or auto-detect)
SITE_URL="[Q9a]"  # e.g., https://www.australiafootball.com

# 2. Extract full page HTML for each reference page
for PAGE in "/" "/news/" "/{sport}/" "/{sport}/teams/" "/{sport}/players/"; do
  curl -s "${SITE_URL}${PAGE}" > /tmp/scrape_$(echo $PAGE | tr '/' '_').html
done

# 3. Extract CSS — all linked stylesheets
curl -s "$SITE_URL" | grep -oP 'href="([^"]*\.css[^"]*)"' | \
  while read -r css; do curl -s "${SITE_URL}${css}" >> /tmp/scraped_styles.css; done

# 4. Extract inline styles from <style> tags
curl -s "$SITE_URL" | python3 -c "
import sys, re
html = sys.stdin.read()
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
for s in styles:
    print(s)
" > /tmp/scraped_inline_styles.css
```

#### 2-KEEP-B: Extract Design Tokens

From the scraped CSS, extract and document:

| Token | What to Extract | Where It Goes |
|-------|----------------|---------------|
| Colors | Primary, secondary, accent, background, text | `globals.css` CSS custom properties |
| Fonts | Font families, sizes, weights, line heights | `globals.css` typography tokens |
| Spacing | Margins, paddings, gaps (convert to token scale) | `globals.css` spacing tokens |
| Breakpoints | Media query breakpoints | `globals.css` responsive tokens |
| Component patterns | Card styles, nav patterns, table styles | Component `.astro` files |

```bash
# Extract CSS custom properties (variables)
grep -oP '--[a-zA-Z0-9-]+:\s*[^;]+' /tmp/scraped_styles.css | sort -u

# Extract font declarations
grep -oP 'font-family:[^;]+' /tmp/scraped_styles.css | sort -u

# Extract color values
grep -oP '(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsl\([^)]+\))' /tmp/scraped_styles.css | sort -u
```

#### 2-KEEP-C: Extract Navigation Structure

```bash
# Extract nav HTML structure
curl -s "$SITE_URL" | python3 -c "
import sys, re
html = sys.stdin.read()
# Find main nav element
nav = re.search(r'<nav[^>]*>(.*?)</nav>', html, re.DOTALL)
if nav:
    # Extract all links and their text
    links = re.findall(r'<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]+)</a>', nav.group(1))
    for href, text in links:
        print(f'{text.strip()} → {href}')
"
```

#### 2-KEEP-D: Build Astro Project Using Scraped Reference

1. Invoke `/bedrock_agent` with wizard answers from Phase 1A
2. **OVERRIDE default theme** with scraped design tokens:
   - Replace generated `globals.css` with scraped CSS variables
   - Replace generated nav items with scraped navigation structure
   - Match scraped layout patterns (grid/flex structure, sidebar placement)
   - Preserve exact color scheme, font stack, and spacing
3. Run 5 Ralph Loops QA (92+ threshold each)
4. **Extra validation loop:** Visual comparison between scraped pages and built pages
5. Generate Release Notes

**Phase 2-KEEP Checklist:**
- [ ] Live site scraped (homepage + [N] key pages from Q9b)
- [ ] CSS custom properties extracted and mapped to `globals.css`
- [ ] Navigation structure replicated exactly (same items, same order, same dropdowns)
- [ ] Layout grid/flex patterns match original (columns, sidebar position, header/footer)
- [ ] Font families, sizes, and weights preserved
- [ ] Color palette preserved (±5% tolerance on hex values)
- [ ] Component patterns replicated (cards, tables, lists match original)
- [ ] Astro project created with content collections + Zod schemas
- [ ] All 5 Ralph Loops passed at 92+
- [ ] `npm run build` succeeds with 0 errors
- [ ] **Visual fidelity check:** Side-by-side comparison of 3+ pages shows near-identical output

**If HYBRID (Q9 = "Hybrid"):**
- Only scrape navigation structure + brand colors
- Use `/bedrock_agent` defaults for layout and components
- Apply scraped nav and colors as overrides

---

### Path B: BUILD NEW (Q9 = "Build New")

Fresh theme using `/bedrock_agent` vertical templates.

**Execute:**
1. Invoke `/bedrock_agent` with wizard answers from Phase 1A
2. Pass through the 8-question bedrock wizard (pre-filled from Phase 1)
3. Run 5 Ralph Loops QA (92+ threshold each)
4. Generate Release Notes

**Phase 2-NEW Checklist:**
- [ ] Astro project created with content collections + Zod schemas
- [ ] Dynamic `[slug].astro` pages for all entity types
- [ ] Navigation component with all sections
- [ ] CSS tokens + `globals.css` (no `:global()` in .css files — R-CSS-01)
- [ ] Layout.astro with `astro-seo` package (R-SEO-02)
- [ ] `trailingSlash: 'always'` in astro.config.mjs (R-SEO-03a)
- [ ] JSON-LD schemas (BreadcrumbList, WebSite on homepage only)
- [ ] All 5 Ralph Loops passed at 92+
- [ ] `npm run build` succeeds with 0 errors

---

**Shared Phase 2 Requirements (both paths):**
- [ ] Layout.astro with `astro-seo` package (R-SEO-02)
- [ ] `trailingSlash: 'always'` in astro.config.mjs (R-SEO-03a)
- [ ] JSON-LD schemas (BreadcrumbList, WebSite on homepage only)
- [ ] Dynamic `[slug].astro` pages for all entity types

**API Leak Quality Gates — Phase 2 (MANDATORY):**

These gates ensure the site structure is optimized for Google's classification algorithms from day one. Reference: SEO Strategy KB (Phase 0G preload).

| Gate | API Leak Parameter | Requirement | Check |
|------|--------------------|-------------|-------|
| Topical Focus | `siteFocusScore` / `siteRadius` | ALL content must be within the declared vertical (Q3/Q4). No off-topic pages. | Review content collections — every page serves the site's core topic |
| Commercial Ratio | `pandaDemotion` | Commercial pages (betting, casino, affiliate) must be < 5% of total indexed pages | Count: money pages / total indexed pages. If > 5%, add more editorial content BEFORE indexing money pages |
| Content Depth | `contentEffort` | Every indexed page must have > 200 words of meaningful content | `grep -rn "noindex" src/pages/` to verify thin pages are excluded |
| Site Classification | `topPetacatTaxId` / `siteType` | Homepage + About page must clearly declare the site's topic for Google's classifier | Verify homepage has H1 + meta description matching vertical |
| Navigation UX | `navDemotion` | Clean navigation, no interstitials, mobile-friendly. Max 8-12 top-level nav items (R-SEO-03f) | Test mobile viewport, verify no popups on first visit |
| Ad Density | `clutterScore` | No display ads on initial launch. Zero above-the-fold commercial content on non-money pages | Visual audit of every page template |
| Schema Signals | `entityAnnotations` / `pqData` | WebSite + BreadcrumbList JSON-LD must be valid. Author markup if YMYL vertical | Run Google Rich Results Test on homepage |

**HARD GATE:** Commercial ratio >= 5% at launch = BLOCKED. Add more editorial content to dilute ratio before proceeding.

**Output:** Working Astro project in `~/{domain}/`

---

## Phase 3: MONEY PAGES — /content_palm + TechOps TopList

**Skip if:** User answered "None" in question 10.

### 3A: Extract ClickUp Task Data (MANDATORY before Palm generation)

If ClickUp task IDs were provided in Q11, extract all money page configuration:

```bash
# Extract task data via ClickUp API
curl -s "https://api.clickup.com/api/v2/task/{TASK_ID}" \
  -H "Authorization: $CLICKUP_API_KEY" | python3 -c "
import json, sys
task = json.load(sys.stdin)
print(f'Name: {task[\"name\"]}')
print(f'Description: {task[\"description\"][:500]}')
# Extract custom fields for: TopList ID, brand lineup, Dragon links, SEO keywords, geo
for cf in task.get('custom_fields', []):
    print(f'  {cf[\"name\"]}: {cf.get(\"value\", \"N/A\")}')
"
```

**From the ClickUp task, extract and store:**

| Field | Where It Goes | Used By |
|-------|-------------|---------|
| TopList ID | Phase 3 post-processing (R-TOPLIST-01) | TopList embed `data-toplist` attribute |
| Brand lineup | Palm API `offer_lineup` parameter | Palm content generation |
| Dragon cloaked URLs | Palm API `offer_lineup` URLs | Affiliate links in content |
| SEO target keywords | Palm API `keyword` parameter | Content topic + SEO focus |
| Target geo | Palm API `geo` parameter | Geographic targeting |

### 3B: Prepare Palm API Request

Build the Palm request with data from ClickUp + wizard answers:

```json
{
  "content_type": "[Q14]",
  "keyword": "[from ClickUp task SEO keywords]",
  "geo": "[from ClickUp task target geo]",
  "language": "[derived from geo]",
  "offer_lineup": ["[Dragon-cloaked brand URLs from ClickUp]"],
  "seo_keywords": "[from ClickUp task — NOW SENT, not metadata-only]",
  "clickup_url": "[Q11 task URL — Palm can cross-reference]"
}
```

**CRITICAL:** The `offer_lineup` MUST use Dragon-cloaked URLs (linkaly.net), NOT raw affiliate tracking links. If Q13 = "Raw fallback", document the reason and flag for follow-up cloaking.

### 3C: Generate Content via Palm

1. Invoke `/content_palm` in Mode B (from bedrock session)
2. Pass all extracted variables (keyword, geo, lineup with Dragon links, SEO keywords)
3. Generate each money page article via Palm v3 API

### 3D: Post-Processing (R-PALM-FMT-01)

Phase 10a post-processing:
1. Replace static "First Look" table with TechOps TopList embed (R-TOPLIST-01)
2. Verify Dragon-cloaked URLs survived Palm generation (Palm may rewrite URLs)
3. Apply R-PALM-FMT-01 formatting transforms
4. Save to project content collection
5. Add TopList CDN to CSP in `vercel.json`

**Phase 3 Checklist:**
- [ ] ClickUp task data extracted (TopList ID, lineup, Dragon links, keywords, geo)
- [ ] Palm API receives keyword + geo + SEO keywords from ClickUp (not manual entry)
- [ ] Brand lineup uses Dragon-cloaked URLs (R-CONTENT-01 — exact user lineup)
- [ ] Palm articles generated for each money page type
- [ ] TechOps TopList embed replaces ALL static comparison tables
- [ ] TopList ID matches the one from ClickUp task (R-TOPLIST-01)
- [ ] CSP in `vercel.json` allows TopList CDN (script-src, style-src, connect-src)
- [ ] No grammar edits applied to Palm output (R-CONTENT-02)
- [ ] Money pages NOT added to main navigation (R-CONTENT-03)
- [ ] Affiliate links have `rel="nofollow sponsored noopener noreferrer"`
- [ ] Dragon-cloaked URLs verified in final output (not rewritten by Palm)

**API Leak Quality Gates — Phase 3 (MANDATORY):**

Money pages face the HIGHEST scrutiny from Google's classification systems. These gates are derived from the Firefly/Copia system and Atom #3076 (Safe Publishing Pattern).

| Gate | API Leak Parameter | Requirement | Check |
|------|--------------------|-------------|-------|
| Gambling Ratio | `numOfGamblingPages` (Firefly ID 30) | Money pages must be < 5% of total indexed pages. Track: gambling_pages / total_pages | Calculate ratio AFTER adding money pages. If > 5%, do NOT index money pages until more editorial content exists |
| Quality Delta | `rhubarb` (ID 56) | Money page engagement (scroll, dwell) must be within 20% of site average | After Phase 4.5 data: compare money page scroll % vs site avg. Flag if delta > 20% |
| Content Effort | `contentEffort` (ID 45) | Money pages must demonstrate first-hand expertise, not thin affiliate copy | Verify: original comparisons, specific data points, unique insights — NOT just scraped operator descriptions |
| AI Content | `racterScores` (ID 52) | If Palm-generated, content must be human-reviewed and enriched with unique data | Add at least 3 unique data points per money page that Palm wouldn't generate (user testing, local regulations, payment methods) |
| Review Quality | `productReviewPUhqPage` (ID 178) | Review pages need UHQ (Ultra High Quality) signals: testing evidence, original photos, comparison data | Include at least: screenshots, personal testing notes, date-stamped comparison tables |
| Affiliate Density | `affiliateLinkDensity` | Max 1 affiliate link per 300 words. TopList embed counts as 1 link cluster | Count: total affiliate links / word count. Flag if density too high |
| YMYL Classification | `YMYL Health Score` | Gambling = highest YMYL tier. Require: About page, author credentials, responsible gambling notice | Verify: `/about/` page exists, author markup in JSON-LD, responsible gambling disclaimer on every money page |

**Atom #3076 Scorecard — Evaluate BEFORE deploying money pages:**

| # | Rule | Status | Grade |
|---|------|--------|-------|
| 1 | Publish news FIRST, casino SECOND | [News count] : [gambling count] ratio | — |
| 2 | Drip casino pages slowly | Only add money pages [X] at a time | — |
| 3 | Casino pages must get engagement | Post-deploy monitoring required | — |
| 4 | Keep casino in one subfolder | /betting/ and /casino/ only | — |
| 5 | Casino content must be high-effort | TopList embed + original reviews | — |
| 6 | Publish news DAILY | Cloud Run pipeline (Phase 7) | — |
| 7 | Monitor gambling page ratio | Track in Phase 8B | — |
| 8 | Avoid AI-generated casino content | Human review mandatory | — |
| 9 | Real content updates only | No false freshness | — |
| 10 | Build direct readership | Newsletter/social (post-launch) | — |

**HARD GATE:** Gambling ratio >= 5% at money page deployment = BLOCKED. Add more editorial content first.

**TopList Embed Format:**
```html
<div data-toplist="{ID}"></div>
<script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
```

**Output:** Money page markdown files in content collection + updated `vercel.json`

---

## Phase 4: REPO CREATION + FIRST DEPLOY

### 4A: Create GitHub Repository (MANDATORY)

Every `/launch_site` run creates a NEW repo in `ParadiseMediaOrg`.

```bash
# 1. Navigate to project directory
cd ~/{domain}

# 2. Initialize git
git init
git branch -M main

# 3. Create .gitignore (Astro standard)
cat > .gitignore << 'EOF'
# build output
dist/
.output/

# dependencies
node_modules/

# astro
.astro/

# environment
.env
.env.*

# editor
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# keys — NEVER commit (R-SEC-01)
*.pem
*.key
EOF

# 4. Create repo in ParadiseMediaOrg
gh repo create ParadiseMediaOrg/{repo-name} \
  --private \
  --source=. \
  --remote=origin \
  --description "{project-title} — Astro content site"

# 5. First commit + push
git add -A
git commit -m "Initial commit: {project-title} Astro project

Created via /launch_site pipeline.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push -u origin main
```

**Verify repo:**
```bash
gh repo view ParadiseMediaOrg/{repo-name} --json name,url,visibility --jq '.'
```

### 4B: Build & Deploy to Vercel

```bash
# 1. Build — must succeed with 0 errors
cd ~/{domain} && npm run build

# 2. Link to Vercel (interactive — select org/team)
vercel link

# 3. Deploy to production
vercel deploy --prod

# 4. Configure custom domain (if Q25 = yes)
vercel domains add {custom-domain}
```

### 4C: Configure Vercel GitHub Integration

```bash
# Connect Vercel project to GitHub repo for auto-deploy on push
vercel git connect
```

After this, every `git push origin main` will trigger a Vercel production deployment automatically.

### 4D: Post-Deploy Verification

```bash
# Check production URL
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/

# Spot-check 5 pages
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/{sport}/
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/news/
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/betting/{slug}/ # if money pages
curl -s -o /dev/null -w "%{http_code}" https://{production-url}/sitemap.xml
```

**Phase 4 Checklist:**
- [ ] GitHub repo created: `ParadiseMediaOrg/{repo-name}`
- [ ] Repo visibility: private (default)
- [ ] `.gitignore` includes node_modules, dist, .env, keys (R-SEC-01)
- [ ] First commit pushed to main
- [ ] `npm run build` succeeds with 0 errors
- [ ] Vercel project linked and deployed
- [ ] Vercel GitHub integration connected (auto-deploy on push)
- [ ] Production URL returns 200
- [ ] Custom domain configured + HTTPS working (if applicable)
- [ ] Spot-check: 5 random pages return 200
- [ ] `sitemap.xml` accessible

**Output:** Live site at `https://{domain}/` or `https://{slug}.vercel.app/`, GitHub repo at `ParadiseMediaOrg/{repo-name}`

---

## Phase 4.5: POSTHOG + NAVBOOST SETUP

**Skip if:** User answered "No" in question 20.

**Purpose:** Add PostHog analytics with full NavBoost KPI tracking to the Astro site. Done after first deploy (Phase 4) to verify events on live site, before SEO audit (Phase 5) since PostHog scripts affect performance metrics.

### 4.5A: Create or Connect PostHog Project

```python
import requests, os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.keys/.env"))

POSTHOG_API_KEY = os.environ["POSTHOG_PERSONAL_API_KEY"]
POSTHOG_ORG_ID = "019b2233-57a2-0000-3260-cfa42e906fc4"

headers = {"Authorization": f"Bearer {POSTHOG_API_KEY}"}
response = requests.get(
    f"https://us.i.posthog.com/api/organizations/{POSTHOG_ORG_ID}/projects/",
    headers=headers
)
existing = {p["name"].lower(): p for p in response.json().get("results", [])}

if "{domain}" in existing:
    project = existing["{domain}"]
else:
    response = requests.post(
        f"https://us.i.posthog.com/api/organizations/{POSTHOG_ORG_ID}/projects/",
        headers={**headers, "Content-Type": "application/json"},
        json={"name": "{domain}"}
    )
    project = response.json()
```

### 4.5B: Add PostHog to Layout.astro

Add the PostHog snippet to the Astro site's `<head>`:

```astro
<!-- In Layout.astro <head>, BEFORE closing </head> -->
<script is:inline>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init('{API_TOKEN}', {
    api_host: 'https://us.i.posthog.com',
    person_profiles: 'identified_only',
    capture_pageview: true,
    capture_pageleave: true,
    autocapture: true,
    autocapture_web_vitals_opt_in: true,
    capture_performance_opt_in: true,
    session_recording: { maskAllInputs: true, maskTextContent: false },
    enable_heatmaps: true,
    property_denylist: ['$ip']
  });
</script>
```

**NOTE:** PostHog project API tokens are public client-side tokens by design — this is an R-SEC-01 exception. Do NOT put them in `~/.keys/.env`.

### 4.5C: Add NavBoost Tracker

Copy `navboost-tracker.js` to `public/js/` and configure:

```bash
cp ~/virtual-ateam/BlackTeam/projects/posthog-integration/setup/{template}/navboost-tracker.js \
   ~/{domain}/public/js/navboost-tracker.js
# Update CONFIG.SITE_DOMAIN and CTA_SELECTORS per Q22
```

Add script tag to Layout.astro (after PostHog init):
```astro
<script src="/js/navboost-tracker.js" is:inline></script>
```

**CTA selectors** (from Q22):
- Default: `[data-toplist] a`, `a[rel="sponsored"]`, `.cta-button`, `a[href*="/go/"]`
- Custom: per user answer

### 4.5D: Update CSP for PostHog

Add PostHog domains to `vercel.json` CSP:
- `script-src`: `us.i.posthog.com us-assets.i.posthog.com`
- `connect-src`: `us.i.posthog.com`

### 4.5E: Deploy + Verify Events

```bash
cd ~/{domain}
git add src/layouts/Layout.astro public/js/navboost-tracker.js vercel.json
git commit -m "Add PostHog + NavBoost tracking (18 KPI metrics)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

Verify events after Vercel redeploy:
```bash
curl -s "https://us.i.posthog.com/api/projects/{PROJECT_ID}/events/?limit=5" \
  -H "Authorization: Bearer $POSTHOG_PERSONAL_API_KEY" | python3 -c "
import json, sys
events = json.load(sys.stdin).get('results', [])
print(f'Events received: {len(events)}')
for e in events[:5]:
    print(f'  {e[\"event\"]} — {e.get(\"properties\", {}).get(\"\$current_url\", \"N/A\")}')
"
```

**Phase 4.5 Checklist:**
- [ ] PostHog project created/connected (ID + token stored)
- [ ] PostHog snippet in Layout.astro `<head>`
- [ ] NavBoost tracker at `public/js/navboost-tracker.js`
- [ ] CTA selectors configured (Q22)
- [ ] CSP allows `us.i.posthog.com` + `us-assets.i.posthog.com`
- [ ] Committed, pushed, Vercel redeployed
- [ ] PostHog receiving events (`$pageview`, `navboost:session_start`)
- [ ] Session recording active
- [ ] Heatmaps enabled

**18 NavBoost Metrics → Google API Leak Parameter Mapping:**

Every PostHog metric directly proxies a Google API leak parameter. This mapping is the bridge between observable data and Google's ranking signals.

| # | PostHog Metric | Target | API Leak Parameter | Google Signal |
|---|---------------|--------|-------------------|---------------|
| 1 | Dwell time | >90s | `goodClicks` (ID 91) | Long dwell = "good click" in NavBoost. 13-month rolling window. |
| 2 | Pogo rate | <18% | `badClicks` (ID 92) | Quick return to SERP = "bad click". Directly degrades rankings. |
| 3-6 | Scroll depth (25/50/75/100%) | >50% avg | `lastLongestClicks` (ID 93) | Deepest scroll in session feeds NavBoost quality signal. |
| 7-9 | CTA visible/clicks/CTR | >5% | `userInteractionData` | Active engagement proves page utility. |
| 10 | Good abandonment | >15% | `goodClicks` (variant) | User satisfied without return to SERP = positive signal. |
| 11-12 | Session start/end | — | `voterTokenCount` (ID 106) | Chrome session count — low volume = less signal for NavBoost. |
| 13 | SERP return rate | <25% | `serpDemotion` (ID 127) | High SERP return rate triggers demotion at SERP level. |
| 14 | Engagement score | >70 | Composite of `goodClicks` + `badClicks` + `lastLongestClicks` | Weighted NavBoost quality proxy. |
| 15 | Outbound clicks | — | `affiliateLinkDensity` + `goodClicks` | Outbound click patterns indicate commercial vs informational. |
| 16 | Heartbeat events | — | `chromeInTotal` | Active tab confirmation prevents idle-tab inflation. |
| 17 | TopList row visibility | — | `rhubarb` quality delta proxy | TopList engagement vs page engagement gap detection. |
| 18 | Session time | >60s | `goodClicks` threshold | Sessions >60s clear the "good click" minimum threshold. |

**NavBoost 13-Month Window Warning:** Click data persists for 13 months. Poor early metrics on a new site can suppress rankings for over a year. Getting NavBoost right from launch is CRITICAL — you cannot easily undo bad click signals.

**Per-Template Monitoring (add to Phase 8B baseline):**

After 7 days of live data, evaluate each page template:

| Template | Required Metrics | Minimum Grade |
|----------|-----------------|---------------|
| Homepage | Scroll >40%, Dwell >30s, Pogo <20% | C |
| Article/News | Scroll >50%, Dwell >60s, Pogo <18% | B- |
| Sport Hub | Scroll >40%, Dwell >25s | C |
| Money Page | Scroll >40%, Dwell >45s, CTA CTR >3% | C+ |
| Fixtures/Data | Scroll >50% (idle-tab skew expected) | B- |

**HARD GATE:** If homepage pogo rate > 25% after 7 days = P1 emergency fix before any further content investment.

**Output:** PostHog project live, NavBoost tracking 18 metrics mapped to API leak parameters, session recording + heatmaps active

---

## Phase 5: SEO AUDIT — STATIC BUILD

**Purpose:** Catch all SEO issues before the site is indexed.

**Execute:**
```bash
# Install SEO toolkit if not present
pip install -e /tmp/seo-toolkit 2>/dev/null

# Build the site
cd ~/{domain} && npm run build

# Run static audit on dist/
seo-toolkit audit-static ./dist --json --output /tmp/{domain}-seo-static.json
```

**The static audit checks 29+ items across these categories:**

| Category | Key Checks |
|----------|-----------|
| Content Structure | Title length (50-60 chars), meta description (120-160), OG tags, headings |
| Architecture | Trailing slashes, URL structure, crawl depth |
| Images | Alt text present, no hotlinking, sizing attributes |
| Internal Links | Broken links, orphan pages |
| Structured Data | JSON-LD valid, Schema.org types correct |
| Indexability | noindex on thin pages, canonical URLs set |
| Crawlability | sitemap.xml present, robots.txt valid |
| Launch Readiness | Breadcrumbs, preconnect hints, HTML sitemap |

**Phase 5 Checklist:**
- [ ] `seo-toolkit audit-static ./dist` executed
- [ ] Overall score recorded: ___/100 (target: 80+)
- [ ] All CRITICAL issues listed
- [ ] All QUICK WINS listed
- [ ] Report saved to `/tmp/{domain}-seo-static.json`

**Mandatory R-SEO-03 Checks (from Astro Technical SEO Rules):**
- [ ] (a) `trailingSlash: 'always'` in astro.config.mjs
- [ ] (b) No external image hotlinking (all images in `public/images/`)
- [ ] (c) `<title>` under 60 chars including suffix
- [ ] (d) Meta descriptions 120-160 chars, no truncation
- [ ] (e) OG type: `article` for content, `website` for index pages
- [ ] (f) Nav links budget: max 8-12 top-level items
- [ ] (g) JSON-LD: WebSite on homepage only, BreadcrumbList on all pages
- [ ] (h) sitemap.xml matches actual indexable pages (no ghost URLs)
- [ ] (i) No thin content pages indexed (< 200 words → noindex per R-SEO-03i)

**Mandatory R-SEO-04 Checks (from Google API Leak Diagnosis — SEO Strategy KB):**

| Check | API Leak Parameter | How to Verify in Static Build |
|-------|--------------------|------------------------------|
| Firefly Gambling Ratio | `numOfGamblingPages` (ID 30) | Count: pages with `/betting/` or `/casino/` in URL ÷ total pages in sitemap. Must be < 5% |
| Thin Content Detection | `pandaDemotion` / `babyPandaDemotion` | Count words per page in `dist/`. Pages < 200 words must have `noindex` |
| Content Effort Assessment | `contentEffort` (ID 45) | Sample 5 articles — each must have > 500 words, images, subheadings, original analysis |
| Commercial Page Quality | `rhubarb` (ID 56) | Money pages must have same structural depth as editorial (word count, images, sections) |
| AI Content Signals | `racterScores` (ID 52) | Flag any pages with zero unique data points or pure template content |
| Spam Indicators | `spamBrainTotalDocSpamScore` (ID 136) | No doorway pages, no keyword-stuffed titles, no hidden text |
| Ad Density | `clutterScore` (ID 192) | Count above-the-fold commercial elements. Target: 0 on non-money pages |
| Affiliate Link Density | `affiliateLinkDensity` | Count `rel="sponsored"` links per page. Max 1 per 300 words |
| Topical Coherence | `siteFocusScore` | Every page in sitemap must serve the declared vertical. No off-topic content indexed |
| Freshness Signals | `lastSignificantUpdate` / `bylineDate` | All articles have ISO datetime stamps. No backdated content |

**HARD GATE:** Firefly gambling ratio >= 5% = BLOCKED. Fix before proceeding.

**Output:** SEO audit report with score and issue list + API Leak parameter assessment

---

## Phase 6: SEO FIXES

**Purpose:** Fix all issues found in Phase 5 before search engines index the site.

**Execute:**
1. Sort issues by severity: Critical → High → Medium
2. Fix each issue (refer to R-SEO-03 sub-rules)
3. Rebuild after each batch of fixes
4. Re-run `seo-toolkit audit-static ./dist` to verify
5. Repeat until score >= 85

**Common Fix Patterns (from australiafootball.com learnings):**

| Issue | Fix |
|-------|-----|
| Thin content pages indexed | Add `<meta name="robots" content="noindex">` to [slug].astro |
| Missing BreadcrumbList JSON-LD | Add to Breadcrumb.astro component |
| Sitemap ghost URLs | Fix sitemap filter to exclude noindexed pages |
| Title too long | Shorten suffix (e.g., ` \| AFL` instead of ` \| Australia Football`) |
| WebSite schema on all pages | Move to homepage-only conditional |
| Hotlinked images | Download to `public/images/`, update references |
| Missing OG image | Add default OG image to config |
| No news sitemap | Create `sitemap-news.xml.ts` (Google News protocol) |
| Trailing slash inconsistency | Set `trailingSlash: 'always'` + fix all internal links |

**Phase 6 Checklist:**
- [ ] All CRITICAL issues from Phase 5 resolved
- [ ] All HIGH issues from Phase 5 resolved
- [ ] Re-audit score: ___/100 (must be >= 90)
- [ ] No `:global()` in standalone .css files (R-CSS-01)
- [ ] `.prose` ul/ol/li rules working in built CSS
- [ ] Changes committed and pushed
- [ ] Vercel redeploy verified

**HARD GATE:** Score must be >= 90 AND all R-SEO-04 API Leak checks GREEN before proceeding to Phase 7.

**API Leak Fixes Priority (in addition to standard SEO fixes):**

| Priority | API Leak Issue | Fix Pattern |
|----------|---------------|-------------|
| P0 | Gambling ratio > 5% | Add more editorial content OR noindex money pages temporarily |
| P0 | Thin content pages indexed | Add `noindex` to pages < 200 words |
| P1 | Money page quality delta (rhubarb) | Enrich money pages: add sections, images, unique data, increase word count |
| P1 | No About page / author markup | Create `/about/` page with team credentials, add author JSON-LD |
| P2 | Weak topical coherence | Remove or noindex off-topic content |
| P2 | High affiliate link density | Reduce sponsored links, spread across more content |
| P3 | AI content signals | Add unique data points, human-written analysis, personal experience markers |

---

## Phase 7: NEWS AUTOMATION — GCP Setup

**Skip if:** User answered "No" in question 15.

**Purpose:** Set up automated daily publishing via Cloud Run Jobs + Cloud Scheduler.

### 7A: Prepare Scripts

Copy and configure from the australiafootball.com template:

```
{domain}/scripts/
├── news_updater.py              ← RSS + Google News + Reddit + FoxSports aggregation (v2.0)
├── editorial_generator.py       ← AI editorial (Claude API) with matching feed sources
├── scraper_foxsports.py         ← FoxSports AU web scraper module (conditional import)
├── requirements-news-updater.txt← pip deps: requests, beautifulsoup4, lxml
├── Dockerfile.news-updater      ← Includes pip install + scraper module
├── Dockerfile.editorial-generator
├── cloudbuild-news-updater.yaml
├── cloudbuild-editorial-generator.yaml
├── deploy-news-updater.sh
└── deploy-editorial-generator.sh
```

**Security features built into scripts (v2.0):**
- `_sanitize_output()` — strips GIT_TOKEN and ANTHROPIC_API_KEY from all log output
- Credential validation — `ValueError` raised at startup if tokens missing when push enabled
- Source quality weighting — 5-tier system (Official→Community) for article selection
- Reddit filtering — `REDDIT_EXCLUDE_PATTERNS` auto-filters match threads, memes, mod posts
- FoxSports domain whitelist — only `foxsports.com.au` URLs accepted, redirect detection
- Safe defaults — `GIT_EMAIL=bot@paradisemedia.com` (no personal email in source)

**Configure per user answers:**
- RSS feeds (question 16)
- Daily caps (question 17)
- Writer personas (question 18)
- Timezone (question 19)

### 7B: Add R-CONTENT-03 Links

If money pages exist, configure the editorial generator to include subtle internal links:
- ONE link per article to the relevant money page
- Natural anchor text woven into an existing sentence
- Rotate between betting and casino links based on context

### 7C: Deploy to GCP

#### 7C-1: Pre-Flight Security Validation (R-DEBUG-01 — MANDATORY)

```bash
# 1. Local dry-run test — MUST pass before any deploy
cd ~/{domain}
LOCAL_REPO=~/{domain} NEWS_DRY_RUN=true python3 scripts/news_updater.py
# VERIFY: Exits cleanly, no import errors, "Total new candidates" > 0

LOCAL_REPO=~/{domain} EDITORIAL_DRY_RUN=true python3 scripts/editorial_generator.py
# VERIFY: Exits cleanly, RSS feeds fetched

# 2. R-SEC-01 scan — no hardcoded keys in source
grep -rn 'phx_\|phc_\|pk_\|sk-\|ntn_\|AIzaSy\|xoxb-\|ghp_\|ghs_' scripts/*.py
# VERIFY: Returns ZERO matches

# 3. Token validation check — scripts raise ValueError if GITHUB_TOKEN missing
python3 -c "
import os; os.environ['NEWS_GIT_PUSH']='true'; os.environ['NEWS_DRY_RUN']='false'
try:
    exec(open('scripts/news_updater.py').read().split('# ─── RSS')[0])
    print('ERROR: Should have raised ValueError for missing GITHUB_TOKEN')
except ValueError as e:
    print(f'PASS: {e}')
"
```

**BLOCKED:** Deploy is blocked until all 3 pre-flight checks pass.

#### 7C-2: Create Secrets & Deploy

```bash
# 1. Validate secrets exist (or create)
for secret in "github-token-{domain}" "anthropic-api-key"; do
  if ! gcloud secrets versions list "$secret" --project=paradisemedia-bi > /dev/null 2>&1; then
    echo "Creating secret: $secret"
    gcloud secrets create "$secret" --data-file=-
  else
    echo "Secret exists: $secret"
  fi
done

# 2. Build and push Docker images
gcloud builds submit --config scripts/cloudbuild-news-updater.yaml --project=paradisemedia-bi .
gcloud builds submit --config scripts/cloudbuild-editorial-generator.yaml --project=paradisemedia-bi .

# 3. Create Cloud Schedulers with OIDC authentication
# News: hourly
gcloud scheduler jobs create http news-updater-{domain}-hourly \
  --schedule="0 * * * *" \
  --time-zone="{timezone}" \
  --http-method=POST \
  --oidc-service-account-email=paradisemedia-bi@appspot.gserviceaccount.com \
  --uri="https://{region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/paradisemedia-bi/jobs/news-updater-{domain}:run"

# Editorial: 3x daily with timezone from question 19
gcloud scheduler jobs create http editorial-generator-{domain}-3daily \
  --schedule="0 0,8,16 * * *" \
  --time-zone="{timezone}" \
  --http-method=POST \
  --oidc-service-account-email=paradisemedia-bi@appspot.gserviceaccount.com \
  --uri="https://{region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/paradisemedia-bi/jobs/editorial-generator-{domain}:run"
```

### 7D: Deploy Standings Updater (R-CONTENT-05 — for sports sites)

If the site has standings/ladder/fixture pages with hardcoded data:
- [ ] Create `scripts/update_standings.py` (Wikipedia scraper + Monte Carlo probabilities)
- [ ] Schedule weekly Cloud Run Job or document manual update cadence
- [ ] Add "Last Updated" dates to all data-driven pages (R-CONTENT-05d)
- [ ] Label off-season pages correctly: "Final [YEAR] Standings" (R-CONTENT-05e)
- [ ] No false freshness claims on pages without active pipelines (R-CONTENT-05a)

### 7E: Verify Automation

- [ ] Trigger news-updater manually — verify article appears on site
- [ ] Trigger editorial-generator manually — verify article appears on site
- [ ] Check timestamps use `YYYY-MM-DDTHH:MM` format (R-CONTENT-04)
- [ ] Check 2-hour minimum gap between articles (R-CONTENT-04)
- [ ] Check R-CONTENT-03 money page links present in editorial articles
- [ ] Check all standings pages show current data (R-CONTENT-05)

### 7F: Post-Deployment Security Audit (R-DEPLOY-01 — MANDATORY)

**MANDATORY after EVERY Cloud Run deploy. All 6 checks must pass.**

```bash
# 1. IAM Policy — no allUsers, only approved principals
gcloud run jobs get-iam-policy news-updater-{domain} --region={region} --project=paradisemedia-bi
gcloud run jobs get-iam-policy editorial-generator-{domain} --region={region} --project=paradisemedia-bi
# VERIFY: Only domain:paradisemedia.com + service accounts. NO allUsers/allAuthenticatedUsers.

# 2. Secrets — tokens via Secret Manager (not env vars)
gcloud run jobs describe news-updater-{domain} --region={region} --format="yaml" | grep -A2 secretKeyRef
# VERIFY: GITHUB_TOKEN uses secretKeyRef, NOT plain value

# 3. R-SEC-01 Scan — no keys in source (should already pass from 7C-1)
grep -rn 'ghp_\|ghs_\|sk-\|phx_\|phc_' scripts/*.py
# VERIFY: 0 matches

# 4. Log Leakage Check — no tokens in Cloud Run logs
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=news-updater-{domain}" \
  --limit=20 --project=paradisemedia-bi --format="value(textPayload)" | grep -i 'ghp_\|token\|password'
# VERIFY: 0 matches (sanitize_output should prevent this)

# 5. Network — Cloud Run job only needs outbound HTTPS
# (No inbound listeners, no persistent containers)
gcloud run jobs describe news-updater-{domain} --region={region} --format="value(spec.template.spec.containers[0].resources)"
# VERIFY: memory ≤ 512Mi, CPU ≤ 1

# 6. Cloud Scheduler Auth — OIDC token enforced
gcloud scheduler jobs describe news-updater-{domain}-hourly --location={region} --format="yaml" | grep oidc
# VERIFY: oidcToken.serviceAccountEmail is set
```

**DEPLOY STATUS:** Only mark `PRODUCTION READY` after all 6 checks pass.

```
R-DEPLOY-01 Checklist: Phase 7F
- [ ] 1. IAM Policy: Approved principals only
- [ ] 2. Secrets: Via Secret Manager secretKeyRef
- [ ] 3. R-SEC-01: No hardcoded keys in source
- [ ] 4. Log Leakage: No tokens in Cloud Run logs
- [ ] 5. Network: Resource limits enforced
- [ ] 6. Scheduler Auth: OIDC token configured
```

**Phase 7 Config Summary:**

| Pipeline | Schedule | Per Run | Daily Cap | Jitter |
|----------|----------|---------|-----------|--------|
| news_updater | Hourly | 1 | [Q17a] | 0-25 min |
| editorial_generator | 3x/day | 1 | [Q17b] | 0-2 hours |

**News Sources (v2.0):** 30 feeds — 19 RSS (direct), 6 Google News (underserved verticals), 7 Reddit Atom (community), 1 FoxSports web scrape. Source quality weighting (Tier 1-5) applied to article selection.

**Output:** Running Cloud Run Jobs + Cloud Schedulers producing ~8 articles/day

---

## Phase 8: SEO AUDIT — LIVE SITE

**Purpose:** Full production audit with API-powered checks (Firecrawl, PageSpeed, Ahrefs).

**Execute:**
```bash
# Full live audit
seo-toolkit audit {domain} --json --output /tmp/{domain}-seo-live.json

# Quick mode if Screaming Frog not available
seo-toolkit audit {domain} --quick --json --output /tmp/{domain}-seo-live.json

# Compare against static audit
seo-toolkit compare /tmp/{domain}-seo-static.json /tmp/{domain}-seo-live.json
```

**Live audit adds these checks (beyond static):**

| Category | What It Tests |
|----------|--------------|
| Performance | LCP, CLS, INP via PageSpeed API |
| Core Web Vitals | TTFB, FCP, real user data |
| HTTP Headers | Cache-Control, compression, HSTS |
| Security | HTTPS redirect, mixed content |
| Mobile | Viewport, font sizes, touch targets |
| Hreflang | Language tags (if multi-language) |

**Phase 8 Checklist:**

**Overall (HARD GATE):**
- [ ] Live audit overall score: ___/100 (must be >= 90)
- [ ] 0 CRITICAL issues remaining
- [ ] Compare report: static vs live delta (no regressions)

**Performance & Core Web Vitals:**
- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] INP < 200ms
- [ ] TTFB < 800ms
- [ ] PageSpeed score >= 90 (mobile)

**Security & Headers:**
- [ ] HTTPS redirect working (HTTP → HTTPS)
- [ ] No mixed content warnings
- [ ] HSTS header present
- [ ] Cache-Control headers set on static assets
- [ ] CSP header configured (especially if TopList embed — R-TOPLIST-01)

**Crawlability & Indexability:**
- [ ] robots.txt accessible and correct
- [ ] sitemap.xml matches live indexable pages
- [ ] No orphan pages (all pages reachable from nav/links)
- [ ] Canonical URLs resolve correctly
- [ ] No duplicate content flagged

**Mobile & Accessibility:**
- [ ] Viewport meta tag present
- [ ] Font sizes readable (>= 16px body)
- [ ] Touch targets >= 48px
- [ ] No horizontal scroll on mobile

**Structured Data:**
- [ ] JSON-LD validates (Google Rich Results Test)
- [ ] BreadcrumbList on all content pages
- [ ] WebSite schema on homepage only

**HARD GATE:** Overall live score must be >= 90 AND 0 critical issues. If either fails, fix issues and re-audit before proceeding.

### 8B: Google API Leak Full Diagnosis (R-SEO-04) — CORE GUIDE

**Purpose:** Comprehensive site health diagnosis using the SEO Strategy Knowledge Base as the CORE, CRITICAL, MUST-HAVE guide. This is NOT a simple baseline — it's a full Tier 1 + Tier 2 parameter evaluation with hard gates.

**Data Sources:**
- SEO Strategy KB: `https://seo-strategy-hphbw.sevalla.app/api-leak` (206 parameters, 4,123+ atoms)
- R-SEO-04 standard: `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md`
- PostHog NavBoost metrics (Project ID from Phase 4.5)
- Core Web Vitals from Phase 8A

**Step 1: Collect All Available Data**

```bash
# 1. Fetch site content inventory
SITEMAP_PAGES=$(curl -s "https://{domain}/sitemap.xml" | grep -c "<loc>")
GAMBLING_PAGES=$(curl -s "https://{domain}/sitemap.xml" | grep -cE "(betting|casino|gambling|pokies)")
echo "Total indexed: $SITEMAP_PAGES | Gambling: $GAMBLING_PAGES | Ratio: $(echo "scale=2; $GAMBLING_PAGES * 100 / $SITEMAP_PAGES" | bc)%"

# 2. Pull PostHog NavBoost metrics (7-day window)
python3 -c "
import sys; sys.path.insert(0, '/home/andre/virtual-ateam/BlackTeam/projects/posthog-integration/lib')
from posthog_metrics_lib import PostHogMetrics
m = PostHogMetrics()
data = m.get_complete_metrics(project_id={PROJECT_ID}, days=7)
print(f'Users: {data[\"users\"]} | Sessions: {data[\"sessions\"]}')
print(f'Pogo: {data.get(\"pogo_rate\", \"N/A\")}% | Dwell: {data.get(\"median_dwell\", \"N/A\")}s')
print(f'Scroll: {data.get(\"avg_scroll\", \"N/A\")}% | Engagement: {data.get(\"engagement_score\", \"N/A\")}')
"

# 3. Check for existing audit in SEO Strategy KB
curl -s "https://seo-strategy-hphbw.sevalla.app/api/audits/{domain}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data: print(f'Prior audit: {json.dumps(data, indent=2)}')
else: print('No prior audit — creating first baseline')
"

# 4. Fetch CWV data from Phase 8A results
# (Already collected in Phase 8 — reference those values)
```

**Step 2: Full Tier 1 + Tier 2 Parameter Evaluation**

Run the complete diagnosis using the SEO Strategy KB API to fetch parameter details and relevant knowledge atoms:

```bash
# Fetch critical parameter details from the KB
for param_id in siteFocusScore numOfGamblingPages contentEffort rhubarb navBoost siteAuthority; do
  curl -s "https://seo-strategy-hphbw.sevalla.app/api/api-leak/params?q=$param_id"
done

# Fetch the most relevant knowledge atoms for the site's vertical
curl -s "https://seo-strategy-hphbw.sevalla.app/api/search?q={vertical}+gambling+content+quality"
```

**TIER 1: Critical Parameter Assessment**

```markdown
## R-SEO-04 Full Diagnosis — {domain}

### 1. Topical Identity (IDs 1-8)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `siteFocusScore` | [HIGH/MODERATE/LOW] — [explain] | [GREEN/YELLOW/RED] |
| `siteRadius` | [NARROW/MODERATE/WIDE] — [explain] | [GREEN/YELLOW/RED] |
| `topPetacatTaxId` | [Classification label] | [GREEN/YELLOW/RED] |
| `commercialScore` | [Commercial pages] / [Total pages] = [X%] | [GREEN if <5%, YELLOW if 5-15%, RED if >15%] |

### 2. Firefly Casino Content Detector (IDs 30-44)

| Parameter | Value | Threshold | Status |
|-----------|-------|-----------|--------|
| `numOfGamblingPages` | [count] | <5% ratio | [GREEN/YELLOW/RED] |
| `numOfUrls` (indexed) | [count] | — | — |
| `numOfArticles8` | [count] | — | — |
| `dailyGoodClicks` | [from PostHog] | >50% of total | [GREEN/YELLOW/RED] |

### 3. NavBoost Click Signals (IDs 91-107)

| Parameter | PostHog Metric | Value | Target | Status |
|-----------|---------------|-------|--------|--------|
| `badClicks` (92) | Pogo rate | [X%] | <18% | [GREEN/YELLOW/RED] |
| `goodClicks` (91) | Median dwell | [Xs] | >90s | [GREEN/YELLOW/RED] |
| `lastLongestClicks` (93) | Avg scroll | [X%] | >50% | [GREEN/YELLOW/RED] |
| `voterTokenCount` (106) | Google sessions | [X] | — | [HIGH/LOW VOLUME] |
| `serpDemotion` (127) | SERP return rate | [X%] | <25% | [GREEN/YELLOW/RED] |

**Per-Template NavBoost Profile:**

| Template | Sessions | Scroll | Dwell | NavBoost Grade |
|----------|----------|--------|-------|---------------|
| homepage | — | — | — | — |
| article | — | — | — | — |
| sport_hub | — | — | — | — |
| money_page | — | — | — | — |

### 4. Content Quality & Effort (IDs 45-51)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `contentEffort` (45) | [Original / Mixed / Commodity] | [GREEN/YELLOW/RED] |
| `OriginalContentScore` (46) | [X% original, X% aggregated] | [GREEN/YELLOW/RED] |
| `siteQualityStddev` (51) | [Quality variance level] | [GREEN/YELLOW/RED] |
| `racterScores` (52) | [AI content status] | [GREEN/YELLOW/RED] |

### 5. Freshness Signals (IDs 76-88)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `lastSignificantUpdate` (76) | [Publishing cadence] | [GREEN/YELLOW/RED] |
| `freshboxArticleScores` (84) | [News sitemap active?] | [GREEN/YELLOW/RED] |
| `bylineDate` (78) | [ISO timestamps with R-CONTENT-04 stagger?] | [GREEN/YELLOW/RED] |

### 6. Parasite SEO / Site Reputation Abuse (IDs 56-61)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `rhubarb` (56) | Money page scroll [X%] vs site avg [Y%] — delta [Z%] | [GREEN if <20%, YELLOW if 20-35%, RED if >35%] |
| `siteAutopilotScore` (60) | [Automated / Manual editorial] | [GREEN/YELLOW/RED] |
```

**TIER 2: Important Parameter Assessment**

```markdown
### 7. Authority & Trust (IDs 113-122)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `siteAuthority` (113) | [DR / domain age / brand recognition] | [GREEN/YELLOW/RED] |
| `directFrac` (112) | [% direct traffic] | [GREEN/YELLOW/RED] |
| `nsr` (119) | [Historical quality reputation] | [GREEN/YELLOW/RED] |

### 8. Demotion Stack (IDs 123-130)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `pandaDemotion` (123) | [Thin pages mitigated?] | [GREEN/YELLOW/RED] |
| `anchorMismatchDemotion` (129) | [Anchor text topical relevance] | [GREEN/YELLOW/RED] |
| `navDemotion` (126) | [Mobile UX, no interstitials] | [GREEN/YELLOW/RED] |
| `serpDemotion` (127) | [Pogo rate within threshold?] | [GREEN/YELLOW/RED] |

### 9. Core Web Vitals (from Phase 8A)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| LCP | [Xms] | ≤1,200ms | [GOOD/NEEDS IMPROVEMENT/POOR] |
| CLS | [X] | ≤0.1 | [GOOD/NEEDS IMPROVEMENT/POOR] |
| INP | [Xms] | ≤200ms | [GOOD/NEEDS IMPROVEMENT/POOR] |

### 10. Spam & Scam Detection (IDs 131-145)

| Parameter | Assessment | Risk |
|-----------|-----------|------|
| `scamness` (131) | [Language review] | [GREEN/YELLOW/RED] |
| `spambrainTotalDocSpamScore` (136) | [Spam patterns?] | [GREEN/YELLOW/RED] |
| `clutterScore` (192) | [Ad density assessment] | [GREEN/YELLOW/RED] |
```

**Step 3: Atom #3076 Safe Publishing Pattern Scorecard**

If the site has money pages (betting/casino), evaluate against the 10-rule playbook:

```markdown
### Safe Publishing Pattern (Atom #3076)

| # | Rule | Status | Grade |
|---|------|--------|-------|
| 1 | Publish news FIRST, casino SECOND | [news count] : [gambling count] | [A-F] |
| 2 | Drip casino pages slowly | [velocity check] | [A-F] |
| 3 | Casino pages must get engagement | [PostHog data] | [A-F] |
| 4 | Keep casino in one subfolder | [URL structure] | [A-F] |
| 5 | Casino content must be high-effort | [Content review] | [A-F] |
| 6 | Publish news DAILY | [Automation status] | [A-F] |
| 7 | Monitor gambling page ratio | [X%] | [A-F] |
| 8 | Avoid AI-generated casino content | [Content origin] | [A-F] |
| 9 | Real content updates only | [Freshness signals] | [A-F] |
| 10 | Build direct readership | [directFrac data] | [A-F] |

**Overall Score:** [A-F] ([description])
```

**Step 4: Compound Effects Analysis**

Document parameter interaction chains:

```markdown
### Compound Effects Chain

[Parameter A] (risk level)
    ↓ amplifies
[Parameter B] (risk level)
    ↓ degrades
[Signal C]
    ↓ could trigger
[Demotion D]
    ↓ resulting in
[Ranking impact]

**Saving graces:** [List parameters that counterbalance risks]
```

**Step 5: Risk Matrix & Recovery Plan**

```markdown
### Top 5 Risk Factors

| # | Parameter | Risk | Confidence | Impact |
|---|-----------|------|-----------|--------|
| 1 | [param] | [RED/YELLOW/GREEN] | [X%] | [Critical/High/Medium/Low] |
| 2-5 | ... | ... | ... | ... |

### Final Risk Matrix

| Parameter | Risk | Action Priority | Owner |
|-----------|------|----------------|-------|
| ... | ... | ... | [B-RANK/B-MAX/B-NINA/etc.] |

### Prioritized Recovery Actions

| Priority | Action | API Leak Rationale | Timeline |
|----------|--------|-------------------|----------|
| P1 | [action] | [parameter + explanation] | [timeline] |
| P2-P4 | ... | ... | ... |
```

**Step 6: Save Diagnosis to SEO Strategy KB (optional)**

```bash
# If API supports creating audits, submit the diagnosis
curl -X POST "https://seo-strategy-hphbw.sevalla.app/api/audits" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "{domain}",
    "date": "'$(date +%Y-%m-%d)'",
    "risk_level": "[OVERALL RISK]",
    "tier1_summary": "[summary]",
    "tier2_summary": "[summary]"
  }'
```

**Step 7: Generate Report**

Save the full diagnosis as:
- Markdown: `~/reports/{domain}/api_leak_diagnosis_{date}.md`
- PDF (if requested): Use ReportLab generator with Paradise Media branding

**HARD GATES for Phase 8B:**
- [ ] **RED on ANY Tier 1 parameter** = MUST have documented recovery plan before launch sign-off
- [ ] **Gambling ratio >= 5%** = LAUNCH BLOCKED until ratio reduced (consistent with Phase 2, 3, 5 gates)
- [ ] **Pogo rate > 25%** = LAUNCH BLOCKED until homepage/key pages fixed
- [ ] **Zero fresh content (no articles < 7 days)** = LAUNCH BLOCKED until news pipeline active
- [ ] **No About page on YMYL site** = LAUNCH BLOCKED until About + author markup added

**Ongoing Monitoring (post-launch):**

This diagnosis is NOT one-time. Schedule re-evaluation:

| Trigger | Action |
|---------|--------|
| Weekly (automated) | Tier 1 quick-check via PostHog NavBoost metrics |
| Monthly | Full Tier 1 + Tier 2 re-evaluation |
| Traffic drop > 10% | Immediate full Tier 1-3 diagnosis |
| Core update within 2 weeks | Focus on `pandaDemotion`, `siteAuthority`, `navBoost` |
| New money pages added | Re-check gambling ratio + rhubarb quality delta |
| Content velocity change | Re-check `contentEffort`, `racterScores`, `freshboxArticleScores` |

### 8C: Google Search Console Setup

Manual actions for the user:

```
GSC Checklist:
- [ ] Add property in GSC (URL prefix method)
- [ ] Verify ownership (DNS TXT or HTML file)
- [ ] Submit sitemap.xml
- [ ] Submit sitemap-news.xml (if news pipeline enabled)
- [ ] Request indexing for money pages (priority)
- [ ] Request indexing for homepage + hub pages
- [ ] Validate breadcrumbs in Rich Results Test
- [ ] Check Mobile Usability report
```

**Output:** Live SEO score + API leak baseline + GSC setup instructions + 0 critical issues confirmed

---

## LAUNCH COMPLETE — Triple Sign-Off

Present final status:

```markdown
## /launch_site Complete

### Project: {domain}
**Date:** {today}

### Phase Status
| Phase | Description | Status | Score |
|-------|-------------|--------|-------|
| 1 | Intake Wizard | COMPLETE | — |
| 2 | Structure (/bedrock_agent) | COMPLETE | Ralph Loops: 92+ |
| 3 | Money Pages (/content_palm) | COMPLETE / SKIPPED | — |
| 4 | First Deploy | COMPLETE | 200 OK |
| 4.5 | PostHog + NavBoost | COMPLETE / SKIPPED | 18 metrics |
| 5 | SEO Audit — Static | COMPLETE | __/100 |
| 6 | SEO Fixes | COMPLETE | __/100 (>= 90) |
| 7 | News Automation | COMPLETE / SKIPPED | Verified |
| 8 | SEO Audit — Live | COMPLETE | __/100 |

### Deliverables
- [ ] Astro project: `~/{domain}/`
- [ ] GitHub repo: `https://github.com/ParadiseMediaOrg/{repo-name}`
- [ ] Production URL: `https://{domain}/` or `https://{slug}.vercel.app/`
- [ ] Money pages: `/betting/...`, `/casino/...`
- [ ] PostHog project: ID {id}, 18 NavBoost metrics + session recording + heatmaps
- [ ] Cloud Run Jobs: `news-updater-{domain}`, `editorial-generator-{domain}`
- [ ] Cloud Schedulers: hourly + 3x daily
- [ ] SEO reports: `/tmp/{domain}-seo-static.json`, `/tmp/{domain}-seo-live.json`
- [ ] GSC: property added, sitemaps submitted

### Configuration Reference
| Component | Value |
|-----------|-------|
| GitHub repo | `ParadiseMediaOrg/{repo-name}` |
| Repo visibility | private |
| Vercel project | {slug} |
| Auto-deploy | Yes (Vercel GitHub integration) |
| GCP project | {gcp-project} |
| ClickUp task (betting) | {task_id} |
| ClickUp task (casino) | {task_id} |
| TopList ID (betting) | {id} (from ClickUp) |
| TopList ID (casino) | {id} (from ClickUp) |
| Dragon links | {yes/raw fallback} |
| PostHog project ID | {id} |
| PostHog API token | {token} (public) |
| NavBoost CTA selectors | {defaults/custom} |
| News daily cap | {N} RSS + {N} editorial |
| Writers | B-LUCA, B-EMMT, B-VICS, B-ALIS, B-NATE |
| Scheduler timezone | {tz} |

---
**B-BOB:** APPROVED
**W-WOL:** APPROVED
**R-REX:** CERTIFIED

*Site launched via /launch_site pipeline*
```

---

## Rules Enforced Across All Phases

| Rule | Phase | Enforcement |
|------|-------|-------------|
| R-CONTENT-01 | 3 | Never override user brand lineups |
| R-CONTENT-02 | 3 | No grammar fixes on Palm output |
| R-CONTENT-03 | 3, 7 | Subtle money page links in articles (Dragon-cloaked) |
| R-CONTENT-04 | 7 | Timestamp stagger, 2h gap, `YYYY-MM-DDTHH:MM` |
| R-TOPLIST-01 | 3 | TechOps TopList embed on all money pages |
| R-CSS-01 | 2, 6 | No `:global()` in standalone .css files |
| R-SEO-02 | 2 | astro-seo package, OG tags, Twitter Cards |
| R-SEO-03 | 2, 5, 6 | 9 Astro technical SEO sub-rules |
| R-IMG-01 | 2, 3 | Image diversity, 3-tier selection |
| R-SEC-01 | 2, 7 | No hardcoded API keys |
| R-DEBUG-01 | 4, 7 | Test locally before deploying |
| R-DEPLOY-01 | 4, 7 | Post-deployment security audit |
| R-POSTHOG | 4.5 | PostHog + NavBoost 18 KPIs, CSP for posthog domains |
| R-DATA-07 | All | Numerical comparison validation |
| R-AUDIT-01 | 5, 6, 8 | Deep audits only, never surface checks |
| R-ANCHOR-01 | 3, 7 | Keyword-rich anchor text on all money page links, no generic anchors, 2x max distribution |
| R-ANCHOR-02 | 3, 7 | Menu-priority anchor distribution: top-level nav sports get anchors before "More" dropdown sports; no sport >3x density of top-level; zero-anchor sports blocked if 3+ articles; update `docs/ANCHOR_TEXT_INVENTORY.md` after changes |
| **R-SEO-04** | **0G, 2, 3, 5, 6, 8B** | **Google API Leak Diagnosis — CORE GUIDE.** SEO Strategy KB (`seo-strategy-hphbw.sevalla.app/api-leak`) is the must-have reference for all site builds and content updates. 206 parameters + 4,123 atoms. Loaded in Phase 0G, enforced as quality gates in Phases 2 (topical focus, commercial ratio), 3 (gambling ratio, rhubarb, content effort), 5-6 (Firefly check, thin content, spam signals), 8B (full Tier 1+2 diagnosis with hard gates). Ongoing: weekly NavBoost quick-check, monthly full re-evaluation. |
| R-CONTENT-05 | 7 | Content freshness: no false freshness claims, weekly stale audit, "Last Updated" on data pages |

**MANDATORY:** After any anchor text additions or changes to australiafootball.com, update `docs/ANCHOR_TEXT_INVENTORY.md` with the new anchors.

**MANDATORY:** The SEO Strategy Knowledge Base at `https://seo-strategy-hphbw.sevalla.app/api-leak` is the CORE reference for ALL phases. Every site build and content update MUST consult the API leak parameters. Phase 8B diagnosis is NOT optional — it's a hard gate for launch sign-off.

---

## Quick Reference

```bash
# Run full pipeline
/launch_site europeangaming.eu

# Skip to specific phase (if resuming)
# Just invoke the relevant sub-command:
/bedrock_agent           # Phase 2
/content_palm            # Phase 3
seo-toolkit audit-static # Phase 5
seo-toolkit audit        # Phase 8
```

---

## Session End (MANDATORY)

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action complete --summary "Completed /launch_site for {domain}" --username $(whoami) --command launch_site
```

Invoke `/reflect` and `/capture_learnings` to update RAG with any new patterns.

---

*launch_site v1.0 | Content Pipeline System | Paradise Media Group*
*Reference: memory/content_pipeline_flow.md*
