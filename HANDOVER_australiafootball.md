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

### Key Files

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
| Content Generation | Palm v3 API (for betting articles) |

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

**Content Collections** (6):
- `news` — 138+ articles (auto-generated via Cloud Run + manual)
- `betting` — Palm v3 generated betting reviews
- `videos` — Video embeds

### Directory Structure

```
australiafootball.com/
├── src/
│   ├── content/           # All markdown content
│   │   ├── news/          # 138+ news articles
│   │   ├── betting/       # Betting reviews
│   │   ├── afl-teams/     # Team profiles
│   │   └── ...            # 34 collections total
│   ├── pages/             # Route pages
│   │   ├── news/          # /news/ listing + [slug]
│   │   ├── betting/       # /betting/ listing + [slug]
│   │   ├── afl/           # /afl/ section
│   │   └── ...            # 15 sport sections
│   ├── components/        # 14 Astro components
│   │   ├── Layout.astro   # Main layout (meta, OG, JSON-LD)
│   │   ├── Header.astro   # Navigation
│   │   ├── Footer.astro
│   │   ├── NewsCard.astro
│   │   ├── BettingCard.astro
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
| `Layout.astro` | Master layout — meta tags, OG, JSON-LD, security headers |
| `Header.astro` | Main navigation (betting NOT in menu per R-CONTENT-03) |
| `NewsCard.astro` | News article card for listings |
| `BettingCard.astro` | Betting article card with filter tabs |
| `NewsListItem.astro` | Compact news list view |
| `SEOHead.astro` | SEO meta tags helper |

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

### Key Patterns from These Fixes

1. **Sitemap drift is real** — Manual `sitemap.xml.ts` gets out of sync. Always check URL count in sitemap vs actual HTML files in `dist/`
2. **isAggregated filter** — Must be applied in BOTH `[slug].astro` (page generation) AND `sitemap.xml.ts`. If only in one, you get ghost URLs
3. **Title truncation** — 125 news articles had `| Australia Football` baked into metaTitle frontmatter, bypassing Layout.astro truncation logic. Strip suffix, truncate base, re-add
4. **RSS relative URLs** — cricket.com.au feeds use relative image paths. Must resolve to absolute before generating markdown
5. **Betting section strategy** — Betting pages are NOT in main nav. Only accessible via subtle in-content links from sport articles (R-CONTENT-03)

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
| 1 | [#1](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/1) | **Enable @astrojs/sitemap** — Replace 507-line manual sitemap. Package installed, not configured in `astro.config.mjs`. Exclude `isAggregated` articles. | `{name}/enable-auto-sitemap` |
| 2 | [#2](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/2) | **Add CI/CD pipeline** — GitHub Actions: `npm run build` on every PR. Phase 2: seo-toolkit static audit. | `{name}/add-github-actions` |
| 3 | [#3](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/3) | **Fix Twitter image fallback** — No `twitter:image` when no image prop in Layout.astro. Fallback to `/images/og-default.png`. | `{name}/fix-twitter-image` |
| 4 | [#4](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/4) | **CSP hardening** — Add `object-src 'none'; base-uri 'self'; form-action 'self'` + `frame-src https://www.youtube.com` in `vercel.json`. | `{name}/harden-csp` |
| 13 | [#13](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/13) | **Broken links audit** — Full crawl of 928+ pages. Check internal, external, images, anchors. Fix all. | `{name}/fix-broken-links` |
| 14 | [#14](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/14) | **Wrong images audit** — Verify actual image content matches page topic (R-AUDIT-01). Check Unsplash IDs, duplicates. | `{name}/audit-fix-images` |
| 15 | [#15](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/15) | **Reduce site scope** — Focus on AFL + 3 core sports (Cricket, NRL, A-League). Deprioritize rest in nav + news automation. | `{name}/reduce-sport-scope` |

### Priority 2 — This Sprint

| # | GitHub Issue | Task | Branch Name |
|---|-------------|------|-------------|
| 5 | [#5](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/5) | **Layout props expansion** — Add `ogType`, `datePublished`, `author` props. Articles pass `"article"` + date/author. | `{name}/layout-og-props` |
| 6 | [#6](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/6) | **NPL state data centralization** — 3 files hardcode states. Extract to single `npl-states.ts`. | `{name}/centralize-npl-states` |
| 7 | [#7](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/7) | **Remove unused `sport` prop** — Layout accepts it but never uses it. Remove from interface + all callers. | `{name}/cleanup-sport-prop` |
| 8 | [#8](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/8) | **News image fallback** — RSS images may 404. `ImageWithFallback` component with sport-specific placeholders. | `{name}/news-image-fallback` |
| 16 | [#16](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/16) | **Betting money page in ClickUp** — Track best-betting-sites-australia in ClickUp with keywords, rankings, update schedule. | N/A (ClickUp task) |
| 17 | [#17](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/17) | **Casino money page** — Create /casino/ section via Palm v3. "Best Online Casinos in Australia" + ACMA compliance. ClickUp brand lineup. | `{name}/casino-money-page` |
| 18 | [#18](https://github.com/ParadiseMediaOrg/australiafootball.com/issues/18) | **Casino content links** — Write 5-10 sport articles with natural casino references (R-CONTENT-03 pattern). No nav menu link. | `{name}/casino-content-links` |
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
| Layout | `~/australiafootball.com/src/components/Layout.astro` |
| Header/Nav | `~/australiafootball.com/src/components/Header.astro` |
| News content | `~/australiafootball.com/src/content/news/` |
| Betting content | `~/australiafootball.com/src/content/betting/` |
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
| R3 | 2026-02-24 | Casino money page + content links (see #17, #18) | P2 | TBD | Open |
| R4 | 2026-02-24 | Set up Ahrefs + AccuRanker monitoring (see #19) | P2 | TBD | Open |
| R5 | 2026-02-24 | Add betting money page to ClickUp tracking (see #16) | P2 | TBD | Open |
| R6 | 2026-02-24 | Replace raw affiliate links with Dragon cloaked links (ClickUp 86afp6hge) | P1 | Andre | Done |

### In Progress

| # | Issue | Branch | Owner | Started | Notes |
|---|-------|--------|-------|---------|-------|
| | | | | | |

### Done

| # | Issue | Branch | Owner | Completed | PR Link |
|---|-------|--------|-------|-----------|---------|
| | | | | | |

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
