# australiafootball.com — Team Handover Document

**Author:** Andre Schmidt
**Date:** 2026-02-24
**For:** Glen, Martin, Abdiel
**Status:** Active

---

## Table of Contents

1. [How I Work — Quick Overview](#1-how-i-work)
2. [The Virtual ATeam System](#2-the-virtual-ateam-system)
3. [Using /bedrock_agent — Step by Step](#3-using-bedrock_agent)
4. [Cloud Run News Automation](#4-cloud-run-news-automation)
5. [Project Architecture](#5-project-architecture)
6. [What I Fixed in the Last 48 Hours](#6-recent-fixes)
7. [Git Workflow — Branch Rules](#7-git-workflow)
8. [Your Task List](#8-your-task-list)
9. [Key File Paths](#9-key-file-paths)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. How I Work

I use Claude Code (CLI) with a custom orchestration system called the **Virtual ATeam**. Think of it as having 70+ AI "team members" organized into 3 teams that build, review, and challenge each other's work.

### My Typical Session Flow

```
1. Open terminal, cd ~/australiafootball.com
2. Run Claude Code
3. Use slash commands to trigger workflows:
   - /bedrock_agent     → Generate new content verticals (full sites)
   - /A_Virtual_Team    → Full build + review + challenge pipeline
   - /blackteam         → Execute tasks (build, fix, deploy)
   - /whiteteam         → Review/audit existing work
   - /posthog_analysis  → Analytics reports
   - /news_update_agent → Manual news article generation
```

### How I Interact

- I give natural language instructions: *"Add 15 news articles across all sport sections"*
- The system assigns the right "personas" (specialists) to handle it
- I review the output, approve or request changes
- Everything gets committed to git with descriptive messages

### Key Principle

The system has built-in quality gates. Every piece of work goes through:
1. **BlackTeam builds it** (16 specialists)
2. **WhiteTeam validates it** (25 validators)
3. **RedTeam challenges it** (29 adversarial testers)
4. Only after **triple sign-off** does it ship

---

## 2. The Virtual ATeam System

### Commands You Should Know

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `/A_Virtual_Team` | Full pipeline: build + validate + challenge | Major features, new sections, refactors |
| `/bedrock_agent` | Generate complete content verticals | New sports sections, betting content |
| `/blackteam` | Execute tasks without validation overhead | Quick fixes, small updates |
| `/whiteteam` | Validate/audit existing work only | Code reviews, SEO audits |
| `/news_update_agent` | Generate news articles from RSS feeds | Manual news when Cloud Run is down |
| `/posthog_analysis` | Analytics reports from PostHog | Performance reviews |
| `/content_palm` | Generate content via Palm v3 API | Betting articles, reviews |

### The 3 Teams

**BlackTeam (Builders)** — 16 personas
- B-BOB (Director) coordinates everything
- B-RANK (SEO), B-MAX (UI), B-CODY (Code Quality), B-NINA (Content), etc.

**WhiteTeam (Validators)** — 25 personas
- W-WOL (Director) assigns reviewers
- Each BT member has a WT counterpart who reviews their work

**RedTeam (Challengers)** — 29 personas
- R-REX (Director) runs 7 adversarial "Red Gates"
- Tries to break what BT built and WT approved
- Must pass all 7 gates to be CERTIFIED

### Example: How I Created the Betting Section

```
Me: /bedrock_agent → Selected "Australian Sports Hub" project
     → Generated betting vertical with 10 AU-licensed bookmakers
     → Palm v3 API produced the article (6,662 words)
     → Ralph Loops QA (5 cycles) scored it
     → WhiteTeam validated SEO, security, accessibility
     → RedTeam challenged with adversarial tests
     → I reviewed, approved, committed, deployed to Vercel
```

---

## 3. Using /bedrock_agent — Step by Step

### What It Does

`/bedrock_agent` generates **complete content verticals** — a set of articles organized by sections for a specific topic/site. It handles everything from research to deployment.

### Step-by-Step Usage

#### Step 1: Launch It

```
/bedrock_agent
```

You'll see a menu:
```
1. Create a NEW content vertical
2. Update an EXISTING site
3. Check project registry
4. Generate news updates
```

Choose option 1 for a new vertical, option 2 to add articles to existing sites.

#### Step 2: Define Your Vertical

The system asks you for:
- **Project name** (e.g., "Australian Sports Hub")
- **Domain** (e.g., australiafootball.com)
- **Sections** (e.g., AFL, NRL, Cricket, Tennis...)
- **Articles per section** (e.g., 2-5)
- **Content type** (news, evergreen, analysis, betting reviews)

#### Step 3: Content Research

The system researches via:
- DataForSEO API (keyword volumes, CPC, competition)
- RSS feeds (current news angles)
- Existing site content (avoid duplicates)

#### Step 4: Content Generation

5 parallel writing agents generate articles simultaneously. Each article gets:
- SEO-optimized title and meta description
- Proper frontmatter (Astro Content Collection format)
- Internal links to related articles
- Image placeholders with alt text

#### Step 5: Ralph Loops QA (5 Cycles)

Every article passes through 5 quality gates:

| Loop | Reviewer | Checks |
|------|----------|--------|
| 1 | Director (B-BOB) | Strategy alignment, factual accuracy |
| 2 | SEO (B-RANK) | Keywords, meta tags, slugs, internal links |
| 3 | Post-Production (B-POST) | Formatting, images, layout |
| 4 | PixelPerfect (B-MAX) | Visual QA, responsive design |
| 5 | CodeGuard (B-CODY) | Code quality, no security issues |

Articles scoring below 85/100 get sent back for revision.

#### Step 6: Build & Deploy

```bash
# Build the Astro site
npm run build

# Deploy to Vercel
npx vercel --prod --archive=tgz
```

#### Step 7: Post-Deploy Audit

Mandatory checks after every deployment:
- Security headers present (CSP, HSTS, X-Frame-Options)
- All URLs in sitemap return 200
- No hardcoded API keys (R-SEC-01)
- OG tags and Twitter cards working

### Critical Rules to Follow

| Rule | What It Means |
|------|--------------|
| R-CONTENT-01 | NEVER change brand lineups — use what the user provides |
| R-CONTENT-03 | Betting links must be subtle, woven into content — NOT in nav menu |
| R-SEC-01 | No API keys in source code — load from `~/.keys/.env` |
| R-DEBUG-01 | Always test locally before deploying |
| R-SEO-02 | Always use `astro-seo` package for meta/OG tags |
| R-AUDIT-01 | Audits must be deep — verify actual content, not just "does it load?" |
| R-IMG-01 | Use diverse images — never same Unsplash query for multiple articles |
| R-TOPLIST-01 | ALL money pages use TechOps TopList embed — never static markdown tables |

---

## 4. Cloud Run News Automation

### Architecture Overview

```
Cloud Scheduler (hourly)
        |
        v
Cloud Run Job: news-updater-australiafootball
        |
        v
1. Random 0-25 min jitter (avoid predictable timing)
2. Fetch RSS from 11 sources
3. Pick 1 article (weighted by underrepresented sports)
4. Generate Markdown with frontmatter
5. Git commit + push to GitHub
        |
        v
GitHub webhook → Vercel auto-redeploys
        |
        v
Live on australiafootball.com in ~60 seconds
```

### RSS Feed Sources (11 Active)

| Sport | Source |
|-------|--------|
| AFL | afl.com.au |
| NRL | leaguefreak.com |
| A-League | aleagues.com.au |
| Cricket | cricket.com.au |
| Formula 1 | formula1.com, speedcafe.com |
| Tennis | atptour.com |
| General | ABC Sport, The Guardian, ESPN Australia, SMH |

### Cloud Run Configuration

| Setting | Value |
|---------|-------|
| Service | `news-updater-australiafootball` |
| Region | us-central1 |
| GCP Project | paradisemedia-bi |
| Schedule | Every hour (`0 * * * *`), Sydney timezone |
| Articles per run | 1 |
| Daily cap | 5 articles (reduced from 20 on 2026-02-24) |
| Jitter | 0-25 minutes random delay |

### Editorial Generator (Claude AI) — Added 2026-02-25

Generates 3 original editorial articles per day using Claude API, spread randomly over 24 hours.

| Setting | Value |
|---------|-------|
| Service | `editorial-generator-australiafootball` |
| Schedule | 3x/day (`0 0,8,16 * * *`), Sydney timezone |
| Articles per run | 1 |
| Daily cap | 3 articles |
| Jitter | 0-2 hours random delay per run |
| Model | claude-sonnet-4-20250514 |
| Personas | 5 writers (LF breaking, EC features, VC opinion, AK analysis, NR roundups) |
| R-CONTENT-03 | Auto-injects subtle betting/casino links |

**Key files:**
| File | Purpose |
|------|---------|
| `scripts/editorial_generator.py` | Main Python script (1100 lines, Claude API) |
| `scripts/Dockerfile.editorial-generator` | Docker image definition |
| `scripts/cloudbuild-editorial-generator.yaml` | Cloud Build pipeline |
| `scripts/deploy-editorial-generator.sh` | Deployment helper |
| `scripts/requirements-editorial.txt` | Python deps (anthropic SDK) |

### RSS Updater — Key Files

| File | Purpose |
|------|---------|
| `scripts/news_updater.py` | Main Python script (600 lines) |
| `scripts/Dockerfile.news-updater` | Docker image definition |
| `scripts/cloudbuild-news-updater.yaml` | Cloud Build pipeline |
| `scripts/deploy-news-updater.sh` | Deployment helper |
| `scripts/monitor_news_updater.sh` | Health monitoring (checks every 2 hours) |

### Environment Variables (Cloud Run)

```
NEWS_PER_RUN=1
NEWS_MAX_DAILY=5
NEWS_JITTER_MAX=1500        # seconds (25 min max)
NEWS_GIT_PUSH=true
NEWS_DRY_RUN=false
GITHUB_TOKEN=<from Secret Manager>
GIT_USER=ParadiseMediaOrg
GIT_EMAIL=andre@paradisemedia.com
```

### Monitoring

The monitor script runs continuously and checks:
- Cloud Run job executions (are they happening?)
- Error rate in logs
- Scheduler job status (enabled/disabled)
- Alerts via email to andre@paradisemedia.com

```bash
# Check monitor status
cat ~/australiafootball.com/scripts/news_monitor.log

# Check recent Cloud Run executions
gcloud run jobs executions list --job=news-updater-australiafootball --region=us-central1 --limit=5

# View logs
gcloud logging read 'resource.labels.job_name="news-updater-australiafootball"' --limit=20 --format="table(timestamp,textPayload)"
```

### Auto-Detected Sports Categories (18)

a-league, w-league, socceroos, matildas, afl, nrl, cricket, nbl, npl, world-cup, epl, f1, tennis, ufc, horse-racing, v8-supercars, rugby-union, nba

---

## 5. Project Architecture

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Astro 4.16.0 (static site generator) |
| Hosting | Vercel (free tier) |
| CDN | Cloudflare |
| Domain | australiafootball.com → australiafootballcom.vercel.app |
| News Automation | Google Cloud Run + Cloud Scheduler |
| Content | Markdown in Astro Content Collections |
| Analytics | PostHog |
| Content Generation | Palm v3 API (for betting + casino articles) |
| TopList Widgets | TechOps embed via `cdn-6a4c.australiafootball.com/embed.js` |

### Content Collections (34 Total)

The site uses Astro Content Collections to organize content:

**Sports Teams & Players** (28 collections):
- `afl-teams`, `afl-players`, `nrl-teams`, `nrl-players`
- `a-league-teams`, `a-league-players`, `w-league-teams`, `w-league-players`
- `cricket-teams`, `cricket-players`, `nbl-teams`, `nbl-players`
- `socceroos-players`, `matildas-players`, `npl-clubs`
- `f1-teams`, `f1-players`, `epl-teams`, `epl-players`
- `tennis-players`, `v8-teams`, `v8-players`
- `horse-racing-teams`, `horse-racing-players`
- `rugby-union-teams`, `rugby-union-players`
- `nba-teams`, `nba-players`, `ufc-fighters`

**Content Collections** (7):
- `news` — 163+ articles (auto-generated via Cloud Run + manual)
- `betting` — Palm v3 generated betting reviews
- `casino` — Palm v3 generated casino reviews (added 2026-02-24)
- `videos` — Video embeds

### Directory Structure

```
australiafootball.com/
├── src/
│   ├── content/           # All markdown content
│   │   ├── news/          # 138+ news articles
│   │   ├── betting/       # Betting reviews
│   │   ├── casino/        # Casino reviews (added 2026-02-24)
│   │   ├── afl-teams/     # Team profiles
│   │   └── ...            # 35 collections total
│   ├── pages/             # Route pages
│   │   ├── news/          # /news/ listing + [slug]
│   │   ├── betting/       # /betting/ listing + [slug]
│   │   ├── casino/        # /casino/ listing + [slug]
│   │   ├── afl/           # /afl/ section
│   │   └── ...            # 16 sport sections
│   ├── components/        # 15 Astro components
│   │   ├── Layout.astro   # Main layout (meta, OG, JSON-LD)
│   │   ├── Header.astro   # Navigation
│   │   ├── Footer.astro
│   │   ├── NewsCard.astro
│   │   ├── BettingCard.astro
│   │   ├── CasinoCard.astro
│   │   └── ...
│   └── styles/            # CSS
├── scripts/               # Cloud Run, deploy, monitoring
├── public/                # Static assets (images, favicon)
├── astro.config.mjs       # Astro configuration
├── vercel.json            # Vercel config (headers, redirects)
└── package.json
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `Layout.astro` | Master layout — uses `astro-seo` package for OG/Twitter/robots + JSON-LD |
| `Header.astro` | Main navigation (betting NOT in menu per R-CONTENT-03) |
| `NewsCard.astro` | News article card for listings |
| `BettingCard.astro` | Betting article card with filter tabs |
| `CasinoCard.astro` | Casino article card with filter tabs |
| `NewsListItem.astro` | Compact news list view |
---

## 6. Recent Fixes (Last 48 Hours)

### What I Worked On: 30 Commits, 800+ Files Changed

Here's everything I fixed/built between Feb 23-24, 2026:

### Major Engineering Work

| # | Commit | What I Did | Why |
|---|--------|-----------|-----|
| 1 | `a7c8c39` | **RT-2026-001 Remediation**: Fixed 11 Red Team findings | Sitemap expanded 524→861 URLs, 137 meta descriptions fixed, security headers added |
| 2 | `b9df727` | **R-BRAND-01 violations**: Complete content writer rewrite | Brand references didn't match AU licensing requirements |
| 3 | `9b67b54` | **RT-2026-002 Ribbon Cycle 2**: Fixed 4 more Red Team findings | Second pass of adversarial testing caught additional issues |
| 4 | `ba42cc2` | Added 17 news articles across all 16 sport verticals | Manual content seeding for launch day |
| 5 | `b342a72` | Added Betting section to navigation + sitemap | New section for Palm-generated betting content |
| 6 | `4034294` | **Unpublished illegal offshore betting article** — QA FAIL 18/100 | Article had unlicensed offshore bookmakers, scored 18/100 in QA |
| 7 | `5584703` | Replaced betting article with ClickUp lineup brands (Palm Job #401) | Used approved AU-licensed brand list from ClickUp task |
| 8 | `c8695ad` | Fixed betting article: AU regulatory compliance + SEO + accessibility | ACMA compliance, proper disclaimers, WCAG checks |
| 9 | `e4f38a0` | Removed Betting from main navigation menu | R-CONTENT-03: betting only accessible via in-content links |
| 10 | `439bc28` | Added subtle betting links to 10 sport news articles | Natural anchor text woven into existing content |
| 11 | `0c81331` | **SEO audit P0-P3 fixes**: NPL anchors, sitemap gaps, JSON-LD coverage | 7,416 broken anchor links fixed, 48 missing sitemap pages added |
| 12 | `d91b1ed` | Fixed Vercel build: resolved relative URLs in Cricket Australia RSS | RSS feed had relative image URLs causing build failures |
| 13 | `a8bbde2` | **Live SEO audit**: noindex 404, CSP header, og:image fixes, permanent redirect | 5 live issues fixed after curl/PageSpeed testing |
| 14 | `29a3130` | **RedTeam final remediation**: 6 flagged issues from adversarial challenge | Ghost sitemap URLs, title truncation (125 news articles), WebSite JSON-LD, pagination noindex |

### Automated News (15 Articles via Cloud Run)

The Cloud Run job published 15 articles automatically across 6 sports:
- **AFL** (3): Power signings, Blues signing, hopeful return
- **Cricket** (3): Aussies leadership, T20 WC fixes, next punch
- **Formula 1** (2): Kostecki spy scandal, Mercedes dev driver
- **General** (4): Olympics, Brisbane 2032, referee confrontation, haters response
- **NBL** (1): Road to 2028 era
- **NRL** (1): First woman to call
- **Tennis** (1): Doha title

### Virtual ATeam System Updates (Main Repo)

| Commit | What |
|--------|------|
| `fe124ee` | Added Red Team command (29 personas, 7 Red Gates) + updated A_Virtual_Team + WhiteTeam for ribbon workflow |

### Feb 24 Session 2: Casino Money Page + TechOps TopList Integration

| # | Commit | What I Did | Why |
|---|--------|-----------|-----|
| 15 | `c8930e8` | Switched betting links from Dragon cloaked to raw tracking URLs | Dragon links on `australiafootball.com/go/*` returned 404 (Worker route not configured for www subdomain) |
| 16 | `063dbbc` | **Casino money page**: New /casino/ section — config.ts, index, [slug], CasinoCard component, 15 brands via Palm Job #459 (7,341 words) + 10 news articles with subtle casino internal links | ClickUp task 86afp7upa — mirrors /betting/ structure exactly |
| 17 | `834bde7` | Replaced static "First Look" tables with TechOps TopList embed on both betting and casino pages | TechOps provided embed widget for dynamic brand tables |
| 18 | `91825e9` | **CSP fix**: Added `cdn-6a4c.australiafootball.com` to `script-src`, `style-src`, `connect-src` in vercel.json | TopList embed script was blocked by Content Security Policy |
| 19 | `5a42235` | Fixed casino TopList ID — was reusing betting ID, now uses `best-online-casino-australia-review-yc7ynm` | Both pages were showing same 10 betting brands |

### Casino Money Page Details

| Item | Details |
|------|---------|
| URL | `https://www.australiafootball.com/casino/best-online-casinos-australia/` |
| ClickUp Task | `86afp7upa` — [AU] Best Online Casino Australia Review |
| Palm Job | #459 (`b2bd54cc-5c63-4af3-a103-3ea83c8332bc`) |
| Brands | 15 (Neospin, GoldenCrown, Skycrown, Wild Tokyo, CrownSlots, LuckyVibe, National Casino, Highflybet, Mafia Casino, Kingdom Casino + 5 runners-up) |
| Links | Raw tracking URLs with `campaign=86afp7upa` (NOT Dragon cloaked) |
| TopList ID | `best-online-casino-australia-review-yc7ynm` |
| Word Count | 7,341 |
| Internal Links | 10 news articles link to `/casino/best-online-casinos-australia/` |
| Navigation | NOT in menu (R-CONTENT-03 — accessible via internal links + sitemap only) |

### TechOps TopList Widget (R-TOPLIST-01)

All money pages now use TechOps TopList embeds instead of static markdown tables:

```html
<div data-toplist="{TOPLIST_ID}"></div>
<script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
```

| Page | TopList ID |
|------|-----------|
| `/betting/best-betting-sites-australia/` | `10-best-betting-sites-in-australia-for-2-7ur6rr` |
| `/casino/best-online-casinos-australia/` | `best-online-casino-australia-review-yc7ynm` |

**CSP requirement**: `cdn-6a4c.australiafootball.com` must be in `script-src`, `style-src`, `connect-src` (already configured in `vercel.json`).

**For future money pages**: Ask TechOps for a new TopList ID, add it to the embed div. The rule R-TOPLIST-01 is enforced in `/content_palm`, `/bedrock_agent`, and `PALM_CONTENT_RULES.md`.

### Feb 26 Session: Full SEO Audit (7 Commits)

Comprehensive SEO audit using `/A_Virtual_Team` with all SEO rules (R-SEO-02, R-SEO-03). Addressed GSC-reported issues: 274 pages 404, 656 not indexed, breadcrumb schema errors, sitemap date/empty/404 errors, broken video section.

| # | Commit | Fix | Impact |
|---|--------|-----|--------|
| 1 | `82f67f3` | Casino in sitemap, BreadcrumbList JSON-LD, og:image dimensions | Casino discoverable, breadcrumb schema errors fixed |
| 2 | `91b5313` | Created sitemap-news.xml, video noindex, 248 trailing slash fixes, 13 duplicate breadcrumbs removed, unused @astrojs/sitemap removed | GSC sitemap-news 404 resolved, crawl efficiency |
| 3 | `e1e79c9` | Noindex 28 route files (707 thin pages), sitemap 900→206 URLs | 656 "not indexed" GSC issue resolved |
| 4 | `04a659a` | Removed dead SEOHead.astro (141 lines, zero imports) | Code cleanup |
| 5 | `dff8715` | Self-hosted 52 news images, 36 fabricated URLs set to default | R-SEO-03b compliance for news |
| 6 | `757bee7` | Migrated Layout.astro to astro-seo package | R-SEO-02 compliance |

**Key decisions:**
- 707 player/team/club pages are noindexed (60-75 words avg = too thin). Pages still exist but Google won't index them.
- Sitemap reduced from ~900+ to 206 quality URLs — Google crawl budget focused on real content.
- 35 news articles had fabricated wikimedia image URLs (404 on origin) — set to default OG image.
- GSC "274 pages 404" are the noindexed thin pages. Will self-resolve in 4-8 weeks.

### Mar 02 Session: PostHog Analytics, Web Vitals & Google Pogo Fix

Full PostHog analytics session for australiafootball.com. Three major outcomes:

**1. PostHog Analysis Report (Project ID: 325168)**

First full analytics report generated. Key metrics (7-day window, 2 days of data):

| Metric | Value |
|--------|-------|
| Total Events | 3,678 |
| Unique Users | 581 |
| Sessions | 620 |
| Top Page | /afl/fixtures/ (295 views, 36.4%) |
| #1 Search Engine | Bing (275 visits, 4x more than Google) |
| Geo | 76.1% Australia |
| Top Browser | Edge (38.2%) — confirms Bing dominance |

Reports emailed as branded PDFs (Paradise Media orange theme, Director Rule 18 compliant).

**2. Web Vitals Fix — Was Not Collecting**

PostHog `$web_vitals` events were not being captured despite `autocapture_web_vitals_opt_in: true` in the init call. Root cause: **deprecated config keys**. The current PostHog SDK uses `capture_performance` as an object, not flat boolean flags.

| Before (broken) | After (working) |
|-----------------|----------------|
| `autocapture_web_vitals_opt_in: true` | `capture_performance: {` |
| `capture_performance_opt_in: true` | `  web_vitals: true,` |
| | `  network_timing: true,` |
| | `  web_vitals_allowed_metrics: ['LCP','CLS','INP','FCP','TTFB']` |
| | `}` |

**Result:** Web vitals now collecting. Early readings all **Good**:
- LCP: 335ms, CLS: 0.000, INP: 8ms, FCP: 327ms

Commit: `5cb6863` (Layout.astro)

**3. Google Pogo Rate Investigation & 301 Redirects**

NavBoost data showed **34.1% Google pogo rate** (14/41 sessions) — target is <18%.

Investigation found **6 of 14 pogos (43%) were caused by 404 pages** indexed in Google:

| 404 URL Pattern | Redirect Target | Reason |
|----------------|-----------------|--------|
| `/team/adelaide-united/*` | `/a-league/adelaide-united/` | `/team/` namespace doesn't exist |
| `/team/broadmeadow-magic-fc/*` | `/npl/broadmeadow-magic/` | Teams are under `/npl/` |
| `/team/charlestown-city-blues-fc/*` | `/npl/` | NPL hub catch-all |
| `/team/st-albans-saints-sc/*` | `/npl/` | NPL hub catch-all |
| `/video/nrl-vs-afl-vs-rugby-union-...` | `/news/` | Video slug doesn't exist |
| `/video/from-the-stands-the-moment-...` | `/news/` | Video slug doesn't exist |
| `/team/:slug/*` (wildcard) | `/` | W-EVAN catch-all requirement |

SEO team approved (B-RANK, W-LUNA, W-EVAN). Commit: `4803e4e` (vercel.json)

**Remaining 8 content pogos** (non-404):
- 3x `/news/...australians-in-the-premier-league/` — needs richer content
- 1x `/` homepage — low scroll (13%), engagement 19
- 1x `/rugby-union/fixtures/` — may be incomplete
- 3x various news articles — content/intent mismatch

**Expected impact:** Pogo rate drop from 34.1% → ~19.5% once Google recrawls (3-7 days).

---

### Feb 26 Session (cont): SEO Toolkit Score 75→90 (3 Commits)

After the structural SEO audit above, ran `seo-toolkit audit-static` to measure static build quality. Started at **75/100 (Grade C)** — pushed to **90/100 (Grade A)** in 3 commits.

**Score progression:** 75 → 85 → 88 → 90

| # | Commit | Fix | Score Impact |
|---|--------|-----|-------------|
| 7 | `dc41e47` | Anchor text diversification — 11 news articles updated with unique AU betting keyword anchors (R-CONTENT-03) | Prep for link quality |
| 8 | `e3b572f` | Compressed 22 oversized images (17.5MB saved), added width/height to 887 img tags (42 components), fixed 1 duplicate Matildas title | 75→85 (+10) |
| 9 | `e7b6d09` | Converted 52 images JPG→WebP, updated 88 frontmatter refs, fixed broken links (horse-racing jockeys path, aggregated article filters on 18 hubs, breadcrumb query params), added JSON-LD to 5 pages (betting, casino, search, 404, pagination), removed NPL hash sub-nav (false-positive link checker issue) | 85→90 (+5) |

**5 checks flipped FAIL→PASS:**
- `duplicate_titles` — Fixed Matildas article metaTitle
- `image_file_sizes` — Compressed all images under 200KB
- `image_dimensions` — Added width/height to every `<img>` tag
- `image_formats` — Converted JPG/PNG to WebP (52 images)
- `trailing_slashes` — Already fixed in prior session, now passing

**Final audit: 90/100 Grade A** — 23 pass, 1 fail, 3 warn

**Remaining (diminishing returns):**
- 1 FAIL: `broken_internal_links` — some aggregated article refs remain in edge cases
- 3 WARN: `meta_description_length` (89 short descriptions), `thin_content` (18 pages), `schema_present` (homepage detection quirk)

### Key Patterns from These Fixes

1. **Sitemap drift is real** — Manual `sitemap.xml.ts` gets out of sync. Always check URL count in sitemap vs actual HTML files in `dist/`
2. **isAggregated filter** — Must be applied in BOTH `[slug].astro` (page generation) AND `sitemap.xml.ts`. If only in one, you get ghost URLs
3. **Title truncation** — 125 news articles had `| Australia Football` baked into metaTitle frontmatter, bypassing Layout.astro truncation logic. Strip suffix, truncate base, re-add
4. **RSS relative URLs** — cricket.com.au feeds use relative image paths. Must resolve to absolute before generating markdown
5. **Betting/Casino section strategy** — Money pages are NOT in main nav. Only accessible via subtle in-content links from sport articles (R-CONTENT-03). Both /betting/ and /casino/ follow this pattern.
6. **CSP blocks external scripts** — When adding embed widgets (like TechOps TopList), the CDN domain MUST be whitelisted in `vercel.json` CSP headers (`script-src`, `style-src`, `connect-src`)
7. **TopList embeds replace static tables** — R-TOPLIST-01: All money pages use TechOps widget. Each page needs its OWN unique `data-toplist` ID from TechOps
8. **Palm API lineup format** — `offer_lineup` must be a list of strings like `["1. Brand - URL", "2. Brand - URL"]`, not objects or a single string
9. **Dragon links vs raw links** — Dragon cloaked links (linkaly.net SP domain) work, but `australiafootball.com/go/*` routes returned 404 because the Cloudflare Worker wasn't configured for the www subdomain. Currently using raw tracking links as fallback

---

## 7. Git Workflow — Branch Rules

### Branch Protection (NOW ACTIVE)

I've enabled branch protection on `main` for `ParadiseMediaOrg/australiafootball.com`:

| Rule | Setting |
|------|---------|
| PR required to merge to main | Yes |
| Approving reviews required | 1 (Andre approves) |
| Dismiss stale reviews | Yes |
| Admin bypass | Yes (Andre can push directly when needed) |

### Your Workflow

```
1. Create your branch from main:
   git checkout main
   git pull origin main
   git checkout -b your-name/feature-description

2. Make your changes, commit with clear messages:
   git add <specific files>
   git commit -m "Add/Fix/Update: clear description of what changed"

3. Push your branch:
   git push origin your-name/feature-description

4. Create a Pull Request on GitHub:
   gh pr create --title "Short title" --body "Description of changes"

5. I (Andre) will review and merge to main
```

### Branch Naming Convention

```
glen/fix-npl-anchor-links
martin/add-ufc-news-section
abdiel/update-sitemap-automation
```

### Commit Message Style

Look at my recent commits for the style:
```
Fix SEO audit findings P0-P3: NPL anchors, sitemap gaps, JSON-LD coverage
Add subtle betting links to 10 sport news articles (R-CONTENT-03)
RedTeam remediation: fix 6 flagged issues from adversarial challenge
```

Pattern: `Action verb + what changed + (rule reference if applicable)`

### What NOT to Do

- Do NOT push directly to `main` (branch protection will block you)
- Do NOT force-push to any branch
- Do NOT commit API keys or secrets (R-SEC-01)
- Do NOT modify Cloud Run configs without discussing first
- Do NOT change `Layout.astro` without clearing Astro cache (`rm -rf .astro/astro .astro/collections`)

---

## 8. Your Task List

### Priority 1 — Must Do This Week

| # | GitHub Issue | Task | Branch Name |
|---|-------------|------|-------------|
| 1 | [#1](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/1) | ~~**Enable @astrojs/sitemap**~~ **Superseded** — Manual sitemap.xml.ts rewritten (206 URLs), @astrojs/sitemap removed. Custom sitemap-news.xml.ts added. Commit `91b5313`. | Andre (2026-02-26) |
| 2 | [#2](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/2) | **Add CI/CD pipeline** — GitHub Actions: `npm run build` on every PR. Phase 2: seo-toolkit static audit. | `{name}/add-github-actions` |
| 3 | [#3](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/3) | ~~**Fix Twitter image fallback**~~ **DONE** — astro-seo migration resolves this. Default image always provided. Commit `757bee7`. | Andre (2026-02-26) |
| 4 | [#4](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/4) | **CSP hardening** — Add `object-src 'none'; base-uri 'self'; form-action 'self'` + `frame-src https://www.youtube.com` in `vercel.json`. | `{name}/harden-csp` |
| 13 | [#13](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/13) | **Broken links audit** — Full crawl of 928+ pages. Check internal, external, images, anchors. Fix all. | `{name}/fix-broken-links` |
| 14 | [#14](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/14) | **Wrong images audit** — Verify actual image content matches page topic (R-AUDIT-01). Check Unsplash IDs, duplicates. | `{name}/audit-fix-images` |
| 15 | [#15](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/15) | **Reduce site scope** — Focus on AFL + 3 core sports (Cricket, NRL, A-League). Deprioritize rest in nav + news automation. | `{name}/reduce-sport-scope` |

### Priority 2 — This Sprint

| # | GitHub Issue | Task | Branch Name |
|---|-------------|------|-------------|
| 5 | [#5](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/5) | ~~**Layout props expansion**~~ **DONE** — Layout already had ogType, publishedDate, author props; now handled via astro-seo. Commit `757bee7`. | Andre (2026-02-26) |
| 6 | [#6](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/6) | **NPL state data centralization** — 3 files hardcode states. Extract to single `npl-states.ts`. | `{name}/centralize-npl-states` |
| 7 | [#7](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/7) | **Remove unused `sport` prop** — Layout accepts it but never uses it. Remove from interface + all callers. | `{name}/cleanup-sport-prop` |
| 8 | [#8](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/8) | **News image fallback** — RSS images may 404. `ImageWithFallback` component with sport-specific placeholders. | `{name}/news-image-fallback` |
| 16 | [#16](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/16) | **Betting money page in ClickUp** — Track best-betting-sites-australia in ClickUp with keywords, rankings, update schedule. | N/A (ClickUp task) |
| 17 | [#17](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/17) | ~~**Casino money page**~~ **DONE** — `/casino/best-online-casinos-australia/` live. 15 brands, Palm Job #459, TopList embed. Commit `063dbbc`. | Andre (2026-02-24) |
| 18 | [#18](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/18) | ~~**Casino content links**~~ **DONE** — 10 news articles updated with subtle casino links (R-CONTENT-03). Commit `063dbbc`. | Andre (2026-02-24) |
| 19 | [#19](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/19) | **Ranking monitoring** — Set up Ahrefs + AccuRanker for money pages, core sport keywords, brand terms. Weekly report template. | N/A (external tools) |

### Priority 3 — Nice to Have

| # | GitHub Issue | Task | Branch Name |
|---|-------------|------|-------------|
| 9 | [#9](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/9) | **RSS feed output** — `/rss.xml` endpoint via `@astrojs/rss`. Latest 50 news articles. | `{name}/add-rss-feed` |
| 10 | [#10](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/10) | **Lighthouse audit** — Score 5 key pages, fix anything below 90. | `{name}/lighthouse-audit` |
| 11 | [#11](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/11) | **Dark mode** — CSS custom properties + toggle. Keep `#1C4E2B` brand color in both themes. | `{name}/dark-mode` |
| 12 | [#12](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/12) | **Search with Pagefind** — Client-side search across all content. Zero runtime cost. | `{name}/add-search` |

---

## 9. Key File Paths

### australiafootball.com

| What | Path |
|------|------|
| Project root | `~/australiafootball.com/` |
| Astro config | `~/australiafootball.com/astro.config.mjs` |
| Vercel config | `~/australiafootball.com/vercel.json` |
| Content schema | `~/australiafootball.com/src/content/config.ts` |
| Layout | `~/australiafootball.com/src/layouts/Layout.astro` |
| Header/Nav | `~/australiafootball.com/src/components/Header.astro` |
| News content | `~/australiafootball.com/src/content/news/` |
| Betting content | `~/australiafootball.com/src/content/betting/` |
| Casino content | `~/australiafootball.com/src/content/casino/` |
| Sitemap | `~/australiafootball.com/src/pages/sitemap.xml.ts` |
| News updater | `~/australiafootball.com/scripts/news_updater.py` |
| Deploy script | `~/australiafootball.com/scripts/deploy-news-updater.sh` |
| Monitor | `~/australiafootball.com/scripts/monitor_news_updater.sh` |

### Virtual ATeam System (Reference Only)

| What | Path |
|------|------|
| ATeam root | `~/AS-Virtual_Team_System_v2/` |
| BlackTeam personas | `~/AS-Virtual_Team_System_v2/blackteam/personas/` |
| WhiteTeam personas | `~/AS-Virtual_Team_System_v2/whiteteam/personas/` |
| RedTeam personas | `~/AS-Virtual_Team_System_v2/redteam/personas/` |
| Team config | `~/AS-Virtual_Team_System_v2/TEAM_CONFIG.md` |
| RAG system | `~/.claude/rag/virtual_team_v2/` |
| Commands | `~/.claude/commands/` |

### Secrets (NEVER commit these)

| What | Path |
|------|------|
| All API keys | `~/.keys/.env` |
| PostHog key | In `.env` as `POSTHOG_API_KEY` |
| Palm v3 token | In `.env` as `PALM_API_TOKEN` |
| GitHub token | In GCP Secret Manager (for Cloud Run) |

---

## 10. Troubleshooting

### Build Fails After Editing Layout.astro

```bash
# Clear Astro cache first
rm -rf .astro/astro .astro/collections
npm run build
```

### Cloud Run News Not Publishing

```bash
# Check if scheduler is running
gcloud scheduler jobs describe news-updater-australiafootball-hourly --location=us-central1

# Check recent executions
gcloud run jobs executions list --job=news-updater-australiafootball --region=us-central1 --limit=5

# Check logs for errors
gcloud logging read 'resource.labels.job_name="news-updater-australiafootball"' --limit=20
```

### Vercel Deploy Rate Limit

Free tier has a 5,000 uploads/hour limit. Always use:
```bash
npx vercel --prod --archive=tgz
```

### Sitemap Out of Sync

```bash
# Build the site
npm run build

# Count pages in dist vs sitemap URLs
find dist -name "index.html" | wc -l
# Compare with sitemap URL count
```

### News Article Not Showing on Site

Check the frontmatter:
- `isAggregated: true` articles link to external source (no built page)
- `isAggregated: false` or missing = internal article with its own page
- Sport must match one of the 18 auto-detected categories
- Date format must be valid (YYYY-MM-DD)

---

## Quick Start for Your First PR

```bash
# 1. Clone the repo (if you haven't)
git clone https://github.com/ParadiseMediaOrg/australiafootball.com.git
cd australiafootball.com

# 2. Install dependencies
npm install

# 3. Create your branch
git checkout -b your-name/your-task

# 4. Start the dev server
npm run dev
# Site runs at http://localhost:4321

# 5. Make your changes
# ... edit files ...

# 6. Build to verify nothing breaks
npm run build

# 7. Commit and push
git add <your-files>
git commit -m "Description of your changes"
git push origin your-name/your-task

# 8. Create PR
gh pr create --title "Your PR title" --body "What you changed and why"
```

---

**Questions?** Ping me on Slack or open an issue on the repo.

---

## Changelog & Open Items

> This is a living document. Add your updates below. Keep entries dated and initialed.

### How to Add Updates

1. Add your entry under the right section below
2. Use format: `- [YYYY-MM-DD] [Your initials] Description`
3. Move completed items to the "Done" section with the completion date

### Open Requirements (Andre Will Add More Here)

<!-- Andre: Add new requirements or highlights here. The team will pick them up. -->

| # | Date Added | Requirement | Priority | Assigned To | Status |
|---|-----------|-------------|----------|-------------|--------|
| R1 | 2026-02-24 | Reduce news daily cap from 20 to 5 | P1 | Andre | Done |
| R2 | 2026-02-24 | Focus site on AFL + 3 core sports (see #15) | P1 | TBD | Open |
| R3 | 2026-02-24 | Casino money page + content links (see #17, #18) | P2 | Andre | **Done** (2026-02-24) |
| R4 | 2026-02-24 | Set up Ahrefs + AccuRanker monitoring (see #19) | P2 | TBD | Open |
| R5 | 2026-02-24 | Add betting money page to ClickUp tracking (see #16) | P2 | TBD | Open |
| R6 | 2026-02-24 | Replace raw affiliate links with Dragon cloaked links (ClickUp 86afp6hge) | P1 | Andre | Reverted — using raw links (Dragon /go/ routes 404 on www) |
| R7 | 2026-02-24 | TechOps TopList embeds on all money pages (R-TOPLIST-01) | P1 | Andre | **Done** (2026-02-24) |
| R8 | 2026-02-24 | CSP updated for TopList CDN `cdn-6a4c.australiafootball.com` | P1 | Andre | **Done** (2026-02-24) |
| R9 | 2026-02-24 | R-TOPLIST-01 rule added to /content_palm + /bedrock_agent + PALM_CONTENT_RULES | P1 | Andre | **Done** (2026-02-24) |
| R10 | 2026-02-26 | Full SEO audit — 7 commits: BreadcrumbList JSON-LD, sitemap fixes, noindex thin content, news sitemap, wikimedia image migration, astro-seo migration | P0 | Andre | **Done** (2026-02-26) |
| R11 | 2026-02-26 | GSC actions: resubmit sitemap.xml (206 URLs), submit sitemap-news.xml, request indexing for money pages, validate breadcrumb fix | P1 | Andre | Manual (in GSC) |
| R12 | 2026-02-26 | SEO Toolkit static audit: 75→90 (Grade C→A). Image compression, WebP conversion, width/height, broken link fixes, JSON-LD on 5 pages | P0 | Andre | **Done** (2026-02-26) |
| R13 | 2026-03-02 | PostHog analytics: web vitals enabled, NavBoost tracking live. First report generated (3,678 events, 581 users, 620 sessions in 2 days) | P0 | Andre | **Done** (2026-03-02) |
| R14 | 2026-03-02 | Google pogo rate fix: 301 redirects for 6 indexed 404 URLs (/team/*, /video/*). Expected pogo drop 34.1%→~19.5% | P0 | Andre | **Done** (2026-03-02) — monitor 7 days |
| R15 | 2026-03-02 | PostHog web vitals config fix: deprecated `autocapture_web_vitals_opt_in` replaced with `capture_performance` object in Layout.astro | P0 | Andre | **Done** (2026-03-02) |
| R16 | 2026-03-02 | Deploy CTA tracking on /casino/ and /betting/ money pages — CTA visible/click currently 0 | P1 | TBD | Open |
| R17 | 2026-03-02 | Investigate "Australians in the Premier League" content (3 Google pogos) — content may need richer data | P1 | TBD | Open |
| R18 | 2026-03-02 | Monitor Malta traffic (8.9% of events) for bot/VPN activity | P2 | TBD | Open |
| R19 | 2026-03-02 | **API Leak Diagnosis**: Full Tier 1+2 analysis completed using SEO Strategy Knowledge Base (206 params, 4,123 atoms). Overall risk: YELLOW. Key risks: low siteAuthority (RED), NavBoost badClicks 20% pogo (YELLOW), rhubarb quality delta on betting page (YELLOW). Key strengths: gambling ratio 0.97% (GREEN), freshboxArticleScores daily (GREEN), CWV all Good (GREEN) | P0 | Andre | **Done** (2026-03-02) |
| R20 | 2026-03-03 | **API Leak Remediation A1**: Quick Picks card + StickyCtaBar + inline TOC on all money pages. Fixes 0% CTA CTR and 22% scroll depth. | P0 | Andre | **Done** (2026-03-03) |
| R21 | 2026-03-03 | **API Leak Remediation A2**: Key Players sections (top 6 by rating) + 6 news items on 16 sport hubs. Fixes 60% pogo rate. | P0 | Andre | **Done** (2026-03-03) |
| R22 | 2026-03-03 | **API Leak Remediation A5**: Review JSON-LD schema on money pages (no fabricated ratings — TechOps TopList is source of truth for ratings) | P1 | Andre | **Done** (2026-03-03) |
| R23 | 2026-03-03 | **API Leak Remediation A6**: PostHog key moved from hardcoded to env var (R-SEC-01). australiafootball.com added to PostHog Registry. | P0 | Andre | **Done** (2026-03-03) |
| R24 | 2026-03-03 | **API Leak Remediation A8 Batch 1**: Removed 200 formulaic casino link spam from news articles. 91 thin RSS stubs + 109 editorial articles cleaned. 0 casino links remain in news. 35 contextual betting links retained. Fixes spamBrain/lowQuality signals. | P0 | Andre | **Done** (2026-03-03) |
| R25 | 2026-03-03 | **API Leak Remediation A7**: Pokies 2% scroll confirmed fixed by A1 template changes. Casino #4 gated on A3 (indexed >300). | P1 | Andre | **Done** (2026-03-03) |
| R26 | 2026-03-03 | **A8 Casino Link Redistribution**: Added 18 natural casino links woven into existing sentences across 10 sports. 9 unique anchors (R-ANCHOR-01), covers all 6 casino pages. Horse racing (6), NRL Vegas (2), motorsport (2), AFL (2), cricket/F1/WC/UFC/NBL/rugby (1 each). Per CEO R-CONTENT-03 directive. | P1 | Andre | **Done** (2026-03-03) |
| R27 | 2026-03-03 | **GSC Assessment (Mar 3 session)**: NO GSC action required. No new URLs created, no URLs removed, no redirects needed. All changes were content-only (internal link edits, template additions, schema updates) on existing pages. Sitemap unchanged at 935 URLs + 5 news. Googlebot will pick up content changes on next regular crawl. Optional: request re-indexing for 7 money pages (1 betting + 6 casino) to accelerate schema/Quick Picks pickup. | P2 | Andre | Info only |
| R20 | 2026-03-02 | **P1 Fix**: Homepage scroll depth — currently 21%, target 50%+. Add editorial picks, breaking news teaser, popular articles above fold. Affects 25% of all sessions. NavBoost 13-month window makes this time-sensitive | P1 | TBD | Open |
| R21 | 2026-03-02 | **P1 Fix**: Betting page quality delta — 15% scroll, 17s dwell vs 51% site avg. Enrich with unique data, comparison tables, sticky TOC. Closes `rhubarb` quality gap | P1 | TBD | Open |
| R22 | 2026-03-02 | **P0 Fix** (upgraded from P2): Add author markup + About page + responsible gambling — YMYL gambling = highest E-E-A-T scrutiny. Red Team elevated this to P0. | **P0** | TBD | Open |
| R23 | 2026-03-02 | ~~Increase original editorial ratio~~ — **REMOVED**: actual ratio is 71.1% (126/177), not 40%. Already exceeds 60% target. | — | — | **Cancelled** (Red Team F1.3) |
| R24 | 2026-03-02 | **P1 Fix** (upgraded from P3): Build direct traffic channel (newsletter, social) — `directFrac` (ID 112) RED. CEO: link building is priority. | **P1** | TBD | Open |
| R25 | 2026-03-02 | **P4 Monitor**: Gambling ratio — keep below 2% (CEO: Firefly safety). Currently 0.97% (2/206). Re-index pages to keep denominator >400 | P4 | Andre | Quarterly review |
| R26 | 2026-03-02 | **Done**: SEO Strategy KB integrated as CORE guide into all 4 commands. Red Team: 14 HIGH findings resolved. | P0 | Andre | **Done** (2026-03-02) |
| R27 | 2026-03-02 | **CEO DIRECTIVE**: 4 casino topics + aggressive link building. Drip slowly (1 per 2 weeks). **Casino #2 DONE**: "Best Online Pokies Australia" — Palm Job #579, 7,159 words, 15 Dragon cloaked links, TopList embed, publishes 2026-03-17T10:00. Remaining: #3 Best Payout Casinos (Mar 31), #4 Live Casino (Apr 14). | **P1** | B-NINA + B-RANK | In Progress (2/4 casino topics done) |
| R28 | 2026-03-02 | **CEO DIRECTIVE**: Re-index noindexed pages. Phases 1-3 already done (~828 URLs). Phase 4a adds +105 (64 NPL clubs, 11 V8 teams, 30 Rugby Union players). Total ~933. Gambling ratio with 6 pages = 0.64%. Target 400+ far exceeded. | **P1** | B-RANK + B-TECH | **Done** (2026-03-02) |
| R29 | 2026-03-02 | **P0 Fix**: CTA selector bug — `a[rel="sponsored"]` doesn't match multi-word rel attributes. Fix to `a[rel~="sponsored"]`. Navboost dual event firing (double pogo count). | **P0** | B-TECH | **Done** (2026-03-02) — Triple-Team verified |
| R30 | 2026-03-02 | **P0 Fix**: Anchor text inventory corrected. Old 7x/10x fixed via P1-7 (33 replacements). March article anchor corrected. Inventory v4.1. 0 violations. | **P0** | B-RANK | **Done** (2026-03-02) — Triple-Team verified |
| R31 | 2026-03-02 | **Priority Plan v2.1** saved to `docs/PRIORITY_PLAN_v2.md`. Covers all 206 API leak parameters, 7 Red Gate findings, CEO Firefly directive. Triple sign-off: B-BOB + W-WOL + R-REX. | P0 | Andre | **Done** (2026-03-02) |

### In Progress

| # | Issue | Branch | Owner | Started | Notes |
|---|-------|--------|-------|---------|-------|
| R13 | PostHog web vitals monitoring | main | Andre | 2026-03-02 | Enabled, collecting. Monitor 7 days for stable baselines |
| R14 | Google pogo rate optimization | main | Andre | 2026-03-02 | 301 redirects deployed for 404 pogos. Track rate drop over 3-7 days |
| — | CTA tracking deployment on money pages | — | B-TECH | — | CTA visible/click = 0 on all pages. Needs navboost-tracker.js CTA selector tuning |
| R19 | API Leak Diagnosis completed | — | Andre | 2026-03-02 | Full report: ~/reports/australiafootball/api_leak_diagnosis_20260302.md |
| R26 | API Leak integrated into ALL 4 commands | — | Andre | 2026-03-02 | SEO Strategy KB CORE guide in: /launch_site (10 gates), /bedrock_agent_update (Step 0.5 + Gate 4), /news_update_agent (Rule 11 + Cycle 5), /content_palm (Phase 0 + Phase 10c). Red Team challenged: 3 HIGH findings fixed. 104 total references across 3,840 lines. |
| R20 | Homepage scroll depth fix | — | TBD | — | Currently 21% scroll, 23.9 engagement. Target 50%+ scroll |
| R21 | Betting page quality delta fix | — | TBD | — | 15% scroll vs 51% site avg. rhubarb risk |
| R32 | P2-2 News Hub Engagement | main | Andre | 2026-03-02 | DONE — Featured hero, 2-col layout, Editor's Picks sidebar, pagination (20/page + Load More), sticky filters |
| R33 | P2-3 Money Page Enrichment | main | Andre | 2026-03-02 | DONE — TOC sidebar, FAQPage JSON-LD, "Last reviewed" date on both casino + betting [slug].astro |
| R34 | P2-4 Template Quality Normalization | main | Andre | 2026-03-02 | DONE — Breadcrumbs on casino/betting index, sticky sidebar on news articles, JSON-LD (WebPage+SportsOrganization) on 18 sport hubs |
| R35 | P2-5 AI Content Human Review | main | Andre | 2026-03-02 | DONE — 8 thin articles (<300w) expanded to 400-520w with data tables, stats, broadcast details. 0 thin content remaining. 63 low-enrichment flagged for future enhancement |

### Done

| # | Issue | Branch | Owner | Completed | Commit/PR |
|---|-------|--------|-------|-----------|-----------|
| 17 | [#17](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/17) Casino money page | main (direct) | Andre | 2026-02-24 | `063dbbc` |
| 18 | [#18](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/18) Casino content links | main (direct) | Andre | 2026-02-24 | `063dbbc` |
| — | TechOps TopList embeds (betting + casino) | main (direct) | Andre | 2026-02-24 | `834bde7` |
| — | CSP fix for TopList CDN | main (direct) | Andre | 2026-02-24 | `91825e9` |
| — | Casino TopList ID fix | main (direct) | Andre | 2026-02-24 | `5a42235` |
| — | SEO: Casino in sitemap, BreadcrumbList JSON-LD, og:image dimensions | main (direct) | Andre | 2026-02-26 | `82f67f3` |
| — | SEO: News sitemap, video noindex, trailing slashes, duplicate breadcrumbs | main (direct) | Andre | 2026-02-26 | `91b5313` |
| — | SEO: Noindex 707 thin pages, sitemap 900→206 URLs | main (direct) | Andre | 2026-02-26 | `e1e79c9` |
| — | SEO: Remove dead SEOHead.astro component | main (direct) | Andre | 2026-02-26 | `04a659a` |
| — | SEO: Self-host 52 news images, remove wikimedia hotlinks | main (direct) | Andre | 2026-02-26 | `dff8715` |
| — | SEO: Migrate Layout.astro to astro-seo component (R-SEO-02) | main (direct) | Andre | 2026-02-26 | `757bee7` |
| — | Anchor text diversification: 11 news articles with unique AU betting keywords | main (direct) | Andre | 2026-02-26 | `dc41e47` |
| — | SEO Toolkit: Compress 22 images, add width/height to 887 imgs, fix duplicate title | main (direct) | Andre | 2026-02-26 | `e3b572f` |
| — | SEO Toolkit: WebP conversion (52 imgs), broken link fixes (18 hubs), JSON-LD on 5 pages | main (direct) | Andre | 2026-02-26 | `e7b6d09` |
| — | PostHog project created (ID: 325168), SDK deployed with NavBoost v2.0.0 | main (direct) | Andre | 2026-02-26 | — |
| — | Fix PostHog web vitals: replace deprecated config with capture_performance object | main (direct) | Andre | 2026-03-02 | `5cb6863` |
| — | PostHog web vitals confirmed collecting: LCP 335ms, CLS 0.000, INP 8ms, FCP 327ms (all Good) | — | Andre | 2026-03-02 | — |
| — | Google pogo investigation: 14 pogos analyzed, 6 caused by 404 indexed URLs, 8 content intent | — | Andre | 2026-03-02 | — |
| — | 301 redirects for 6 legacy /team/ and /video/ 404 URLs + wildcard /team/* catch-all | main (direct) | Andre | 2026-03-02 | `4803e4e` |
| — | PostHog analysis PDF v1 + v2 reports generated and emailed | — | Andre | 2026-03-02 | — |
| — | Google API Leak Diagnosis: 206 params, 47 atoms analyzed. YELLOW risk. 0.97% gambling ratio (GREEN), NavBoost 20% pogo (YELLOW), siteAuthority (RED) | — | Andre | 2026-03-02 | PDF + MD report |

### Team Notes & Questions

<!-- Drop questions, blockers, or observations here. Andre reviews daily. -->

-

### Environment Setup Notes

<!-- Document any setup gotchas you hit so the next person doesn't. -->

- Node version: check `.nvmrc` or `package.json` engines field
- Must have `gh` CLI installed and authenticated for PR creation
- GCP access needed for Cloud Run monitoring (ask Andre for IAM)
- Vercel access needed for deployment previews (ask Andre to add you)

### Weekly Check-In Log

<!-- Brief status update each Monday. -->

| Week | Glen | Martin | Abdiel |
|------|------|--------|--------|
| W09 (Feb 24) | | | |
| W10 (Mar 02) | | | |
| W11 (Mar 09) | | | |
| W12 (Mar 16) | | | |

— Andre
