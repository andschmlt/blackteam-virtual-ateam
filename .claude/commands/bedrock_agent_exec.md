# /bedrock_agent — Execution Spec (Options 1-2)

**This file is loaded by bedrock_agent.md when the user selects Option 1 (New domain) or Option 2 (New article).**
**Do NOT read this file for Options 3-4 — those route to /bedrock_agent_update.**

---

## MANDATORY WORKFLOW ENFORCEMENT

**STOP. READ THIS FIRST. NO EXCEPTIONS.**

Before executing ANY bedrock_agent command, you MUST follow this workflow:

**STEP 1: BLACKTEAM BRIEF (MANDATORY)**
- Generate Project Tracking ID: BT-YYYY-NNN
- Create Project Brief with scope, assignments, quality gates
- Assign ALL team personas to work streams
- Present brief to user for approval

**STEP 1b: WRITER SELECTION (MANDATORY for content verticals)**
- Identify target GEO from project domain/brief
- Apply CW-R9 (GEO routing) + CW-R10 (content type routing)
- Check writer_rotation.json — no 3x consecutive same writer
- GEO→Writers: AU→FINN/JACK/ROSA | DACH→HANA/YUKI/NINW | FR→CLEO/OLGA/HUGL | IT→MARC/ZARA/DAVI | ES→RAJA/LEON/ABEL | UK→HANA/CLEO/MILA | US→SURI/JACK/MILA | World→YUKI/KAIA

**STEP 2: TEAM EXECUTION (MANDATORY)**
- Content Writer → Writes per persona voice/variables (CW-R9/R10)
- Head of Content → Editorial standards, voice, accuracy
- SEO Commander → H1/H2 structure, keywords, meta tags
- PixelPerfect → Visual QA, accessibility, design system
- DataForge → Data pipelines, JSON files, scraping
- Post Production → Links, images, functional testing
- Elias Thorne → ML models, ratings, algorithms
- Insight → Data quality, coverage gaps

**STEP 3: 5 RALPH LOOPS QA (MANDATORY)** — Each loop 92+ to pass
1. Loop 1: Content Quality (Head of Content)
2. Loop 2: SEO Optimization (SEO Commander)
3. Loop 3: Technical QA (Post Production)
4. Loop 4: UX/UI Review (PixelPerfect)
5. Loop 5: Data Validation (Elias + Insight)

**STEP 4: RELEASE APPROVAL** — Release Notes → Post Production Manager → Director approval → ClickUp comment

**STEP 5: GIT + DEPLOY** — Git commit → Push to GitHub → Astro build → Deploy to Vercel → Update hub/index.html

**STEP 6: REFLECT** — Invoke /reflect to capture learnings, update skills files

### Pre-Execution Checklist (MUST complete ALL)

- [ ] BlackTeam Brief created with Project ID
- [ ] All team personas assigned to work streams
- [ ] User approved the brief before execution
- [ ] Content generated following team standards
- [ ] Loop 1-5 all passed (92+ each)
- [ ] Release Notes generated and approved
- [ ] Director final approval obtained
- [ ] Git committed, pushed, Astro built, deployed to Vercel
- [ ] /reflect invoked to capture learnings
- [ ] R-SEO-03a-i: All 9 Astro technical SEO sub-rules checked
- [ ] R-ANCHOR-01: Money page links use keyword-rich anchor text, 2x max distribution

**IF ANY CHECKBOX IS UNCHECKED, DO NOT PROCEED. QUALITY OVER SPEED — ALWAYS.**
**ALL AUDITS MUST BE DEEP — NEVER SURFACE-LEVEL (R-AUDIT-01)**

---

## Project Reference

- **Command ID:** BT-2026-004
- **Base Path:** `/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/`
- **Framework:** `bedrock_agent/The_Agent/`
- **Docs:** `bedrock_agent/The_Agent/docs/`
- **GitHub:** [ParadiseMediaOrg/AS-Virtual_Team_System_v2](https://github.com/ParadiseMediaOrg/AS-Virtual_Team_System_v2/tree/main/projects/bedrock_agent)

### Reference Projects (Use as Templates)

| Project | ID | Type | Files | Astro | Vercel URL |
|---------|-----|------|-------|-------|------------|
| **Australian Sports Hub** | BT-2026-005 | Multi-sport (5 sports) | 287 content, 324 pages | `Australian_Sports_Hub_Astro/` | `australian-sports-hub.vercel.app` |
| WC 2026 | BT-2026-001 | Single tournament | 3,523 files | `WC_2026_Astro_V2/` | `wc-2026.vercel.app` |
| Italian Serie A | BT-2026-002 | Single league | 348 files | `Italian_Serie_A_Astro/` | `italian-serie-a.vercel.app` |
| Bundesliga | BT-2026-003 | Single league | ~300 files | `Bundesliga_2025-26_Astro_V2/` | — |
| Premier League | — | Single league | ~300 files | `Premier_League_2025-26_Astro/` | — |
| F1 2026 | — | Single championship | ~200 files | `F1_2026_Astro/` | `f1-2026.vercel.app` |
| Six Nations | — | Single tournament | ~100 files | `Six_Nations_2026_Astro/` | — |
| Tennis Grand Slams | — | Multi-tournament | ~100 files | `Tennis_Grand_Slams_Astro/` | — |
| Ligue 1 | — | Single league | ~200 files | `Ligue_1_2025-26_Astro/` | — |

### Australian Sports Hub Reference (RECOMMENDED for multi-sport projects)

**Full reference doc:** `bedrock_agent/Australian_Sports_Hub_Astro/PROJECT_REFERENCE.md`

Most comprehensive project: 5 sports, 11 content collections, 3 Zod schemas, 287 content files, 324 pages, sport-specific CSS theming, custom sitemap.xml.ts, Pagefind search, ~78 factual errors caught via web search verification.

**Key patterns:** (1) Multi-collection schema — single schema works across multiple sports (2) Sport-specific page dirs with identical template structure (3) Fact-checking workflow — parallel agents per sport (4) `@astrojs/sitemap` conflicts with custom `sitemap.xml.ts` — use custom only

---

## What is a Vertical?

A **Vertical** is a content category — the broad topic area your project covers.

**Hierarchy:** Vertical (Sports, Politics, Gaming) → Sub-category (Football, Tennis) → Scope (Local, National, International) → Title (Serie A, World Cup 2026)

| Vertical | Sub-category | Scope | Title |
|----------|--------------|-------|-------|
| Sports | Football | International | FIFA World Cup 2026 |
| Sports | Football | Local | Serie A (Italy) |
| Sports | Tennis | International | Grand Slams |
| Gaming | Esports | International | LoL Worlds |

---

## Commands

```
/bedrock_agent                          # Show main menu (4 options)
/bedrock_agent new                      # Option 1: Create new project (interactive wizard)
/bedrock_agent configure [project]      # Edit existing project config
/bedrock_agent generate [project]       # Option 2: Generate content & HTML website
/bedrock_agent status [project]         # Check progress & file counts
/bedrock_agent qa [project]             # Run quality checks
/bedrock_agent version [project]        # Create archived version
/bedrock_agent list                     # List all projects
/bedrock_agent_update                   # Options 3-4: Update existing site/article (style-locked)
```

**Arguments:** $ARGUMENTS

---

## Interactive Wizard

When running `/bedrock_agent new`, guide the user through these questions using `AskUserQuestion`.

### Q1: Vertical Category

| Vertical | Examples |
|----------|----------|
| Sports | Football leagues, Tennis, Golf, MMA |
| Politics | Elections, Parliament, Local councils |
| Gaming | Esports, Casino, Video games |
| Entertainment | Film, Music, Celebrity news |
| Business | Finance, Markets, Industry news |
| Travel | Destinations, Hotels, Reviews |
| Other | Custom category |

### Q2: Sub-category (Based on Vertical)

**If Sports:**

| Sport | Popular competitions |
|-------|---------------------|
| Football | World Cup, Serie A, Premier League |
| Rugby | Six Nations, World Cup, Super Rugby |
| Tennis | Grand Slams, ATP/WTA Tours |
| Golf | PGA Tour, Majors, Ryder Cup |
| Darts | PDC World Championship |
| Basketball | NBA, EuroLeague, FIBA |
| Formula 1 | F1 World Championship |
| MMA | UFC, Bellator, ONE Championship |
| Cricket | World Cup, IPL, The Ashes |

**If Gaming:** Esports, Casino, Video Games, Other
**If Politics:** Local, National, International, Other

### Q3: Geographic Scope

| Scope | Examples |
|-------|----------|
| Local | Serie A (Italy), Bundesliga (Germany), single country/region |
| National | US Open (Tennis), FA Cup — country-wide but not single league |
| National Hub | Australian Sports Hub (multiple sports, single country) — uses multi-collection Astro template |
| International | FIFA World Cup, Olympics, Champions League, Grand Slams |

### Q4: Tournament/League Title
Official title, e.g. "FIFA World Cup 2026", "Serie A 2025-26", "Bundesliga 2025-26"

### Q5: Country (If Local/National Scope)
Italy, Germany, England, Spain, France, USA, or specify.

### Q6: Content Style

| Style | Description |
|-------|-------------|
| Sports Journalism | Match reports, player interviews, transfer news, expert analysis |
| Statistical | Data-driven, stats tables, rankings, comparison tools |
| Travel & Venue | Stadium guides, city info, fan travel tips |
| Encyclopedia | Wikipedia-style factual pages, historical records, profiles |
| Mixed | Combination of above (like WC 2026 project) |

### Q7: News Section

| Option | What happens |
|--------|-------------|
| Yes | News scraping pipeline, cron job for daily updates, Google News + RSS + APIs |
| No | Static content only, manual updates, lower maintenance |

### Q8: Content Scope

| Size | Players | Teams | Best for |
|------|---------|-------|----------|
| Starter | 20 | 10 | Quick MVP, testing |
| Standard | 50 | 20 | Single tournament/league |
| Complete | 100 | 32 | Full coverage |
| Enterprise | 150+ | 48+ | WC 2026 scale |
| Hub | 200+ | 60+ | Multi-sport hub (Australian Sports Hub scale) |
| Custom | ? | ? | You specify |

### Wizard Summary

After all questions, display a PROJECT CONFIGURATION SUMMARY with all selections and the project folder path. Ask: "Proceed with this configuration? (Yes / Edit / Cancel)"

---

## Generated Output

```
{Project_Name}/
├── main/
│   ├── config/vertical.json    # Master config
│   ├── data/
│   ├── output/
│   │   ├── index.html          # Docsify website
│   │   ├── _sidebar.md         # Navigation
│   │   ├── README.md           # Homepage
│   │   ├── latest_news.md      # News feed (if enabled)
│   │   ├── players/current/ + legends/
│   │   ├── teams/
│   │   ├── tournaments/
│   │   ├── venues/
│   │   ├── news/               # (if enabled)
│   │   └── comparison/dynamic/
│   ├── scripts/news_scraper.py # (if enabled)
│   └── qa/
├── Version_1.0/RELEASE_NOTES.md
├── docs/
└── VERSION.md
```

### vertical.json Configuration

```json
{
  "project": { "name": "Serie A 2025-26", "slug": "Serie_A_2025-26", "created": "2026-01-20", "version": "1.0" },
  "vertical": { "category": "Sports", "subcategory": "Football", "scope": "Local", "country": "Italy" },
  "content": { "style": ["sports_journalism", "statistical"], "players_target": 50, "teams_target": 20, "include_legends": true, "include_venues": true },
  "news": { "enabled": true, "sources": ["google_news", "rss_feeds"], "cron_schedule": "0 12 * * *", "keywords": ["Serie A", "Italian football", "Calcio"] },
  "entities": { "primary": "players", "group": "teams", "event": "matches", "venue": "stadiums" },
  "theme": { "primary_color": "#1a472a", "secondary_color": "#ffffff" }
}
```

---

## Command Details

### `/bedrock_agent new`
Starts interactive wizard with all questions above.

### `/bedrock_agent configure [project]`
Load and edit existing vertical.json. Display current settings, ask what to change, save updates.

### `/bedrock_agent generate [project]`
Options: `html` (Docsify website), `comparison` (comparison tool data), `templates` (content templates), `news` (run news scraper), `all` (everything, default).

### `/bedrock_agent status [project]`
Count files per category, calculate progress %, check news pipeline status, check HTML existence.

### `/bedrock_agent qa [project]`
Run quality gates (placeholders, section presence, minimum files, sources, R-CONTENT-04/05, R-ANCHOR-01, images). Run Ralph Loops if requested.

### `/bedrock_agent version [project]`
Show current version, ask for new (1.1 minor / 2.0 major / custom), copy main/ to Version_X.Y/, generate RELEASE_NOTES.md.

### `/bedrock_agent list`
Scan bedrock_agent directory, load each project's config, count files, display formatted table.

---

## News Pipeline (When Enabled)

1. **Configure sources** based on vertical/subcategory (Google News API, sport-specific RSS, official feeds)
2. **Create cron job** for daily updates: `0 12 * * * /path/to/scripts/news_scraper.py`
3. **Generate keywords** from project config (Title + Country + Key terms)

---

## BLACKTEAM INTEGRATION (AUTOMATIC)

After project creation via `/bedrock_agent new`, BlackTeam is AUTOMATICALLY invoked with full team assignments and 5 Ralph Loops.

### Team Roster & Assignments

| Role | Persona | Responsibilities |
|------|---------|-----------------|
| Content Quality | Head of Content | Editorial standards, voice, accuracy, storytelling |
| SEO Strategy | SEO Commander | H1/H2 structure, keywords, meta tags, competitor research |
| Data Engineering | DataForge | Data pipelines, JSON files, news scraping |
| ML/Data Science | Elias Thorne | Player rating models, comparison algorithms, stats |
| UX/UI Design | PixelPerfect | Visual design, fonts, colors, responsive |
| BI Development | DataViz | Stats dashboards, charts, visualizations |
| QA Testing | Post Production Mgr | Link testing, content QA, broken images, final checks |
| Code Quality | CodeGuard | Code standards, security, performance |
| Data Analysis | Insight | Content insights, gaps, recommendations |

---

## 5 RALPH LOOPS (MANDATORY)

Every task goes through 5 Ralph Loops. Each MUST pass (92+) before release.

**Use the Agent tool for each Ralph Loop** — each loop runs as a subagent with its own context window. This ensures the full checklist is in context for each reviewer.

### Loop Execution Order

1. **Loop 1 (Content Quality)** — runs FIRST, must pass before others start
2. **Loops 2, 3, 4 (SEO, Technical, UX/UI)** — run IN PARALLEL after Loop 1 passes
3. **Loop 5 (Data Validation)** — runs LAST after Loops 2-4 all pass

### Re-run Efficiency
- If Loop 2 fails but 3 and 4 pass → fix Loop 2 issues → re-run ONLY Loop 2
- Passed loops retain their scores — do NOT re-run

### Loop 1: Content Quality (Head of Content)

**Section A: Historical Content Verification**
- [ ] A1. Team History — founded year, championship/trophy counts, milestones, past managers, name changes, ownership history verified against official sources
- [ ] A2. Tournament/League History — first edition year, all past champions, record holders, format changes, historical venues, rule changes with years
- [ ] A3. Player History — career statistics, championship wins (years, teams), career start date, previous teams, awards, records
- [ ] A4. Venue/Circuit History — opening year, previous names, capacity, notable events, renovations, layout changes

**Section B: Editorial Quality Standards**
- [ ] B1. No Placeholder Content — no TBD, TODO, PLACEHOLDER, [INSERT X], Lorem ipsum, Coming soon, empty sections
- [ ] B2. Factual Accuracy — all statistics from official data, dates consistent, names spelled correctly (verify special characters), rankings current
- [ ] B3. Voice & Tone — professional journalism, consistent tense, no informal language, active voice, engaging but not sensationalist
- [ ] B4. Content Completeness — all entities have full profiles (not stubs), bio sections 150+ words, stats include all relevant metrics, career highlights 5+ bullets, news 300+ words
- [ ] B5. Cross-References — team pages link to all players, player pages link to teams, venues link to events, news links to entities

**Section C: Source Verification**
- [ ] C1. Primary sources used (official league/federation/team websites, verified outlets, press releases)
- [ ] C2. Statistics attributed, quotes attributed, historical facts verifiable, no unsourced claims

**Score: ___/100 | PASS: 92+ required**

### Loop 2: SEO Optimization (SEO Commander)

**Section A: On-Page SEO Structure**
- [ ] A1. Heading Hierarchy — one H1 per page with primary keyword, H2s follow logically, H3s nest under H2s, no level skipping
- [ ] A2. Meta Tags — title 50-60 chars keyword at start, description 150-160 chars with CTA, OG:title/description/image set, Twitter card tags
- [ ] A3. URL Structure — clean slugs (hyphens not underscores), keywords in path, lowercase, logical hierarchy

**Section B: Keyword Optimization**
- [ ] B1. Research Completed — primary keyword per page, 3-5 secondary keywords, long-tail variations, competitor analysis, search volume data
- [ ] B2. Placement — primary in H1 + first 100 words, secondary in H2s, keywords in alt text + meta description, natural density 1-2%
- [ ] B3. Entity-Specific — player names include team/position, team names include sport/league, venues include country

**Section C: Technical SEO**
- [ ] C1. Internal Linking — 3-5 per page, descriptive anchor text, breadcrumbs, sidebar nav
- [ ] C2. Image SEO — all have alt text with keywords, descriptive filenames, compressed, lazy loaded
- [ ] C3. Schema Markup — SportsOrganization for teams, Person for players, SportsEvent for matches, Article for news, BreadcrumbList
- [ ] C4. Indexability — no noindex on public pages, sitemap.xml generated, robots.txt configured, canonical URLs, no duplicates

**Score: ___/100 | PASS: 92+ required**

### Loop 3: Technical QA (Post Production Manager)

**Section A: Link Validation (ZERO TOLERANCE FOR 404s)**
- [ ] A1. Internal — nav links, content links, card links, sidebar links, anchor links, no circular redirects
- [ ] A2. External — all work, rel="noopener noreferrer", target="_blank", no defunct sites
- [ ] A3. Assets — image src paths, CSS files, JS files, favicon, fonts all load

**Section B: Build & Deployment**
- [ ] B1. Astro Build — npm run build succeeds, no TypeScript errors, no missing imports, collections valid, pages generated
- [ ] B2. Asset Generation — dist/ contains all pages, CSS bundled/minified, images copied
- [ ] B3. Vercel Deployment — successful, no build errors, preview + production URLs work

**Section C: Content Integrity**
- [ ] C1. Data Rendering — all frontmatter renders, no "undefined"/"null", numbers/dates format correctly
- [ ] C2. Content Display — no truncated content, no HTML as text, special characters render, code blocks formatted
- [ ] C3. Dynamic Content — filters, sort, search, pagination all work

**Section D: Performance**
- [ ] D1. Homepage loads under 3s, no render-blocking resources, images lazy loaded, fonts preloaded
- [ ] D2. Images compressed, CSS/JS minified, no unused CSS

**Section E: Browser Testing**
- [ ] Desktop: Chrome, Firefox, Safari, Edge (latest)
- [ ] Mobile: iOS Safari, Chrome Mobile, Samsung Internet

**Section F: Final Checks**
- [ ] F1. No JS errors in console, no 404s in network tab, no CORS errors
- [ ] F2. sitemap.xml valid, robots.txt exists, no accidental blocks

**Score: ___/100 | PASS: 92+ required**

### Loop 4: UX/UI Review (PixelPerfect)

**Section A: Text Visibility & Readability**
- [ ] A1. Contrast — body text 4.5:1 minimum, large text (18px+) 3:1 minimum, NO white on light backgrounds, NO light gray on white
- [ ] A2. Never Use — white on yellow, light gray (#CCC) on white, red (#E10600) on black (#15151E) for body, anything below 4.5:1
- [ ] A3. Typography — body 16px min, H1 2rem, H2 1.5rem, H3 1.25rem, line-height 1.5-1.7, weight 400 body / 600-700 headings
- [ ] A4. Font Consistency — primary font site-wide, fallback fonts specified, no incompatible mixing

**Section B: Color System & Theme**
- [ ] B1. Brand colors applied correctly (primary for headers/CTAs, secondary for accents, cards have contrast, links distinct)
- [ ] B2. Hover & Focus states visible and distinct, no color-only changes
- [ ] B3. Dark Mode (if applicable) — text readable, images don't clash, cards have borders

**Section C: Astro Template Compliance**
- [ ] C1. Components consistent (cards, headers, footers, nav match patterns)
- [ ] C2. Layout grid (container max-width, columns, spacing via CSS variables, responsive breakpoints)
- [ ] C3. Design tokens (CSS variables for colors, spacing, fonts — no magic numbers)

**Section D: Responsive Design**
- [ ] D1. Mobile (320-767px) — single column, 44px touch targets, font scaling, no overflow, tables scroll, nav collapses
- [ ] D2. Tablet (768-1023px) — two columns where appropriate, cards reflow, images scale
- [ ] D3. Desktop (1024px+) — full layout, sidebar visible, max content width enforced, no horizontal scroll

**Section E: Accessibility (WCAG 2.1)**
- [ ] E1. Keyboard — all elements focusable, logical tab order, no traps, skip links
- [ ] E2. Screen Reader — semantic HTML (nav, main, article, aside), ARIA labels, alt text, form labels
- [ ] E3. Motion — respects prefers-reduced-motion, no flashing (3 Hz limit), animations pausable

**Section F: Visual Polish**
- [ ] F1. Alignment & spacing consistent, no overlapping, grid maintained
- [ ] F2. Images load, correct aspect ratios, no stretching, alt text present
- [ ] F3. Cards same height in rows, no overflow, hover states work
- [ ] F4. Logo displays, active nav state shows current page, mobile menu works

**Score: ___/100 | PASS: 92+ required**

### Loop 5: Data & ML Validation (Elias Thorne + Insight)

**Section A: Data Accuracy (Elias Thorne)**
- [ ] A1. Numeric Ranges — ratings 0-100, ages 16-50, speeds possible, percentages sum correctly, no impossible negatives
- [ ] A2. Statistical Consistency — W+L+D=Total, points calculations correct, goal difference matches, times formatted (mm:ss.xxx)
- [ ] A3. Ranking Algorithm — top-ranked have best stats, no outliers, historical weighting correct, algorithm documented

**Section B: Data Completeness (Insight)**
- [ ] B1. Entity Coverage — all teams, players, venues have content, full schedule present, no orphan pages
- [ ] B2. Field Completeness — no empty required fields, image paths specified, all stats populated, bios filled
- [ ] B3. Relationship Integrity — team references valid, player-team relationships correct, venue-event links accurate

**Section C: Historical Data Verification**
- [ ] C1. Championship records accurate (counts, years, no false claims)
- [ ] C2. Career statistics verified (start dates, totals, wins, podiums, records)
- [ ] C3. Timeline consistency (chronological order, no future as past, dates consistent)

**Section D: JSON/Data File Validation**
- [ ] D1. Valid JSON syntax, required fields present, correct data types, no trailing commas, UTF-8
- [ ] D2. Frontmatter matches Zod schema, all fields populated, optional fields handled, enum values valid

**Section E: News Pipeline (If Enabled)**
- [ ] E1. Sources configured, keywords relevant, no spam, deduplication working
- [ ] E2. Articles formatted, attribution included, dates accurate, categories correct

**Section F: Content Freshness (R-CONTENT-05)**
- [ ] Standings/ladders/fixtures match current round from official sources
- [ ] "Last Updated" timestamp visible on all data-driven pages
- [ ] No false freshness claims without active pipeline
- [ ] Off-season pages labelled: "Final [YEAR] Standings"

**Score: ___/100 | PASS: 92+ required**

---

## BLACKTEAM EXECUTION FLOW

After `/bedrock_agent generate` completes:

1. **INVOKE BLACKTEAM** — `/blackteam "QA review for {Project_Name}"`
2. **ASSIGN ALL ROLES** — Each specialist receives their work stream
3. **PARALLEL EXECUTION** — Head of Content, SEO Commander, PixelPerfect, Elias Thorne, Post Production, Insight all work simultaneously
4. **RUN RALPH LOOPS** — Loop 1 sequential → Loops 2-4 parallel → Loop 5 sequential
5. **COLLECT FEEDBACK** — Each specialist comments with findings
6. **FIX ISSUES** — Address feedback from failed loops ONLY
7. **RE-RUN FAILED LOOPS** — Only re-run loops that failed
8. **DIRECTOR APPROVAL** — Final sign-off
9. **VERSION RELEASE** — Create Version_X.0 with release notes

### Team Feedback Format

Each persona MUST provide: Persona Name, Role, Loop #, Score, Status (PASS/NEEDS WORK), Observations (what was done well + what needs improvement), Issues Found (issue, file/location, severity), Recommendations (specific actionable advice), Files Reviewed with status.

---

## R-TOPLIST-01: TechOps TopList Embed (MANDATORY for Money Pages)

ALL money pages MUST use TechOps TopList embed widget:
```html
<div data-toplist="{TOPLIST_ID}"></div>
<script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
```

**Rules:** ASK user for TopList ID if not supplied. Replace Palm "First Look" table during post-processing. Each page gets own unique ID. CDN must be in CSP (script-src, style-src, connect-src).

| Page | TopList ID |
|------|-----------|
| `/betting/best-betting-sites-australia/` | `10-best-betting-sites-in-australia-for-2-7ur6rr` |
| `/casino/best-online-casinos-australia/` | `best-online-casino-australia-review-yc7ynm` |

---

## R-ANCHOR-01: Keyword-Rich Anchor Text (MANDATORY)

ALL internal links to money pages MUST use keyword-rich anchor text. **NEVER** generic action-verb anchors.

| Vertical | Approved Keywords |
|----------|------------------|
| Betting | "best betting sites in Australia" (5.4K), "AFL betting" (3.6K), "NRL betting tips" (1.3K), "Melbourne Cup odds" (8.1K), "sports betting sites" (1.6K) |
| Casino | "online pokies in Australia" (110K), "best online casinos in Australia" (14.8K), "top Australian online casinos" (40.5K), "best pokies online" (33.1K), "real money casino sites" (6.6K) |

**Rules:** No single anchor >2x across site. Sport-specific anchors preferred. Verify against keyword list before publishing. Update `docs/ANCHOR_TEXT_INVENTORY.md` after changes.

---

## R-ANCHOR-02: Menu-Priority Anchor Distribution

Top-level nav sports (A-League, Matildas, W-League, Socceroos, World Cup) get anchor priority over "More" dropdown sports. No sport >3x anchor density of any top-level sport. Every sport with 3+ articles MUST have 1 betting + 1 casino anchor. Check distribution before adding links.

---

## ASTRO DEPLOYMENT (MANDATORY)

After QA passes and content is committed, create Astro version:

### Required File Structure

```
{Project_Name}_Astro/
├── package.json               # astro, @astrojs/mdx
├── astro.config.mjs           # mdx integration
├── tsconfig.json              # extends @astro/tsconfig/strict
├── vercel.json                # buildCommand, outputDirectory
└── src/
    ├── content/config.ts      # Zod schemas for ALL entities
    ├── components/            # Header.astro, Footer.astro, *Card.astro
    ├── layouts/Layout.astro   # SEO meta tags, nav, footer, global styles
    ├── pages/                 # index.astro + {entity}/index.astro + [...slug].astro
    └── styles/globals.css     # CSS variables
```

### CSS Variable Requirements

```css
:root {
  --{sport}-primary: #XXXXXX;
  --{sport}-secondary: #XXXXXX;
  --{sport}-black: #XXXXXX;
  --{sport}-white: #XXXXXX;
  --{sport}-gray: #XXXXXX;
  --font-primary: 'Font Name', sans-serif;
  --font-heading: 'Font Name', sans-serif;
}
```

### Page Requirements

**Listing Page (index.astro):** getCollection() call, sort by relevant field, filter UI, grid/list with card components, client-side filter JS.

**Detail Page ([slug].astro):** getStaticPaths() with all slugs, getCollection() filtered by slug, full entity details, related content section, back to listing link.

**Card Components:** Accept entity props, link to detail page, image with fallback, key info, hover state, responsive.

**Layout.astro:** DOCTYPE, html lang="en", head (charset, viewport, description, OG tags, twitter card, favicon, title with suffix), body (Header, slot, Footer), global styles imported.

### Build & Deploy

```bash
cd {Project_Name}_Astro && npm install
npm run build
npx pagefind --site dist
npm run preview
vercel deploy --prod
```

Deploy URL: `{project-slug}.vercel.app`

---

## Persona Standards (From Past Projects)

1. **Research Before Execution** — Verify all player/team data against official sources BEFORE writing
2. **Accessibility First** — WCAG 2.1 AA mandatory, check contrast ratios before approving colors
3. **Test All Links** — Every link tested, zero 404s in production
4. **Historical Data Verification** — Championship counts, stats verified against official federation/league sites
5. **Mobile-First** — Test for 320px first, no horizontal scrolling, 44px touch targets
6. **Completeness Over Speed** — 20 complete profiles > 100 stubs. Never ship placeholder content
7. **SEO Not Optional** — Every page must have proper metadata. Missing meta = release blocked
8. **Documented Feedback** — QA feedback includes specific file references and actionable recommendations

---

## MASTER EXECUTION CHECKLIST

**PRE-EXECUTION**
- [ ] BlackTeam Brief created with BT-YYYY-NNN
- [ ] All team personas assigned
- [ ] User approved brief
- [ ] Reference templates identified

**CONTENT GENERATION**
- [ ] All entities created
- [ ] Historical data verified by Head of Content
- [ ] Statistics verified by Elias Thorne + Insight
- [ ] No placeholder text

**5 RALPH LOOPS QA**
- [ ] Loop 1: Content Quality 92+ PASS (historical verification completed)
- [ ] Loop 2: SEO Optimization 92+ PASS (all meta tags, keywords)
- [ ] Loop 3: Technical QA 92+ PASS (zero 404s, all assets load)
- [ ] Loop 4: UX/UI Review 92+ PASS (WCAG 2.1 AA, text visible)
- [ ] Loop 5: Data Validation 92+ PASS (all data in valid ranges)

**ASTRO TEMPLATE COMPLIANCE**
- [ ] File structure matches standard
- [ ] CSS variables defined
- [ ] Content collection schemas valid
- [ ] Pages have filters and detail pages
- [ ] Card components consistent

**RELEASE & DEPLOY**
- [ ] RELEASE_NOTES.md generated
- [ ] Director final approval
- [ ] Git commit + push to GitHub
- [ ] Deployed to Vercel, production URL tested
- [ ] hub/index.html updated

**POST-RELEASE**
- [ ] /reflect invoked
- [ ] ClickUp task updated
- [ ] Team notified

---

### Log Session Completion

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action complete --summary "Completed /bedrock_agent session" --username $(whoami) --command bedrock_agent
```
