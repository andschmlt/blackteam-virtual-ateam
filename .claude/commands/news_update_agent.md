# /news_update_agent - Bedrock Agent News Update System

Multi-project news aggregation system for all bedrock_agent sports verticals with Ralph Loops quality assurance.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before news updates.**

Read these files for prior learnings:
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings
- `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` — **R-IMG-01: Google Image Optimization (MANDATORY)**
- `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md` — **R-SEO-04: API Leak Diagnosis Framework (MANDATORY)**

**RAG Query:**
```python
import sys; sys.path.insert(0, "/home/andre/AS-Virtual_Team_System_v2/rag")
from rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("news update agent sports content", top_k=5)
learnings = rag.query("news content quality corrections", collection_name="learnings", top_k=3)
```

---

## Usage

```
/news_update_agent                      # Show available projects
/news_update_agent all                  # Update news for ALL projects
/news_update_agent wc2026               # World Cup 2026 only
/news_update_agent premier-league       # Premier League only
/news_update_agent serie-a              # Italian Serie A only
/news_update_agent bundesliga           # Bundesliga only
/news_update_agent ligue1               # French Ligue 1 only
/news_update_agent tennis               # Tennis Grand Slams only
/news_update_agent six-nations          # Six Nations Rugby only
/news_update_agent f1                   # Formula 1 only
/news_update_agent australiafootball     # Australia Football (8 verticals)
/news_update_agent status               # Check status of all projects
/news_update_agent --dry-run [project]  # Test run without saving
```

Arguments: $ARGUMENTS

---

## Supported Projects

| Project ID | Name | Path | News Sources |
|------------|------|------|--------------|
| `wc2026` | World Cup 2026 | `WC_2026_Astro` | FIFA, ESPN, BBC Sport |
| `premier-league` | Premier League 2025-26 | `Premier_League_2025-26_Astro` | Sky Sports, BBC Sport, ESPN |
| `serie-a` | Italian Serie A | `Italian_Serie_A_Astro` | Football Italia, ESPN, Goal |
| `bundesliga` | Bundesliga 2025-26 | `Bundesliga_2025-26_Astro_V2` | Bundesliga.com, Kicker, ESPN |
| `ligue1` | Ligue 1 2025-26 | `Ligue_1_2025-26_Astro` | L'Equipe, ESPN, BBC Sport |
| `tennis` | Tennis Grand Slams | `Tennis_Grand_Slams_Astro` | ATP, WTA, ESPN, Tennis.com |
| `six-nations` | Six Nations 2026 | `Six_Nations_2026_Astro` | Six Nations Rugby, BBC Sport |
| `f1` | Formula 1 2026 | `F1_2026_Astro` | F1.com, Autosport, Motorsport |
| `australiafootball` | Australia Football | `~/australiafootball.com` | AFL.com.au, NRL.com, A-Leagues, ESPN AU, Fox Sports, The Guardian AU, ABC Sport, SBS Sport |

**Base Path:** `/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/`

---

## Writer Selection Per Project (CW-R9 + CW-R10)

Before generating news content, select a content writer persona:
1. Identify the site's target GEO (e.g., australiafootball.com → AU)
2. Apply **CW-R9** (GEO routing) to get primary writer pool
3. Rotate writers per article — check `data/writer_rotation.json`, no 3x consecutive
4. Apply writer's `[Grammatical_Error_%_Allowance]` and `[Sentiment]` variables to content

| Site GEO | Primary News Writers | Style |
|----------|---------------------|-------|
| AU | B-FINN (Aussie Voice), B-JACK (Breaking) | Conversational/Direct |
| DACH | B-NINW (Weekly Digest), B-HANA (Precision) | Measured/Analytical |
| FR | B-CLEO (Cultural), B-OLGA (Investigative) | Provocative/Narrative |
| IT | B-MARC (Mediterranean), B-DAVI (Transfer) | Storytelling/Direct |
| ES | B-LEON (Hard News), B-RAJA (Column) | Direct/Passionate |
| UK | B-MILA (Narrative), B-ROSA (Feature) | Storytelling/Empathetic |
| US | B-JACK (Breaking), B-SURI (Data) | Direct/Factual |

Full writer roster: `AS-Virtual_Team_System_v2/blackteam/rules/CONTENT_WRITER_RULES.md`

---

## Quality Assurance: Ralph Loops (4 Cycles)

All news articles MUST pass 4 quality review cycles:

| Cycle | Reviewer | Focus | Threshold |
|-------|----------|-------|-----------|
| 1 | **Director** | Fact-checking, source verification | 80+ |
| 2 | **Head of Content** | Quality, readability, structure | 80+ |
| 3 | **SEO Commander + PPM** | SEO optimization, validation | 80+ |
| 4 | **ALL THREE** | Internal link verification | 0 broken |

---

## CRITICAL RULES

1. **ONLY add REAL news** - Never invent or fabricate articles
2. **Source verification** - All news must come from trusted sources
3. **Fact-checking** - Cross-reference with official sources
4. **No placeholders** - No TBD, TODO, or Lorem ipsum content
5. **Working links** - All internal links must be valid
6. **Valid images** - All images must exist and be properly linked
7. **If no news exists, add nothing** - Zero additions is acceptable
8. **Project-specific sources** - Use only sources relevant to each vertical
9. **R-CONTENT-04: No timestamp clustering** - Use `date: "YYYY-MM-DDTHH:MM"` (with time), NOT just `YYYY-MM-DD`. Minimum 2-hour gap between articles on the same day. Never push multiple articles in one commit. Check existing articles for today before assigning a time.
10. **R-ANCHOR-02: Menu-priority anchor distribution** - Anchor text distribution MUST reflect the site's navigation hierarchy. Top-level nav sports (A-League, Matildas, W-League, Socceroos, World Cup) get anchor priority over "More" dropdown sports. Top-level nav sports MUST have anchors before any "More" dropdown sport gets a second anchor. No sport should have more than 3x the anchor density (anchors/articles) of any top-level nav sport. Zero-anchor sports are BLOCKED — every sport with 3+ articles MUST have at least 1 betting and 1 casino anchor. When adding new articles, check anchor distribution per sport BEFORE choosing which article gets the link.
11. **R-SEO-04: API Leak Compliance** — Every news article affects Google's classification signals. Reference: SEO Strategy KB (`seo-strategy-hphbw.sevalla.app/api-leak`). Key parameters:
    - `siteFocusScore` — Articles MUST stay within the site's declared vertical. Off-topic articles dilute focus score.
    - `contentEffort` — Every article must have > 500 words, subheadings, and factual sourcing. Thin aggregated content with no original analysis scores low.
    - `racterScores` — AI-generated articles must include at least 2 unique data points or human analysis not in the source material.
    - `freshboxArticleScores` — Consistent daily publishing cadence maintains favorable freshness signals. Gaps > 3 days degrade this score.
    - `numOfGamblingPages` — When adding R-CONTENT-03 betting/casino links to articles, the article itself does NOT count as a gambling page. Only pages IN `/betting/` or `/casino/` paths count toward the ratio.
    - `badClicks` / NavBoost — Articles that cause high pogo rates (users return to Google immediately) accumulate `badClicks` in a 13-month rolling window. Ensure articles answer the headline promise.

**MANDATORY:** After any anchor text additions or changes to australiafootball.com, update `docs/ANCHOR_TEXT_INVENTORY.md` with the new anchors.

---

## Security Gates (MANDATORY)

### Pre-Deploy Gate: R-DEBUG-01 — Local Dry-Run Test

**MANDATORY before ANY Cloud Run deploy or `gcloud builds submit`:**

```bash
# 1. Test news_updater.py locally
cd ~/australiafootball.com
LOCAL_REPO=~/australiafootball.com NEWS_DRY_RUN=true python3 scripts/news_updater.py
# Verify: exits cleanly, no import errors, candidate count > 0

# 2. Test editorial_generator.py locally
cd ~/australiafootball.com
LOCAL_REPO=~/australiafootball.com EDITORIAL_DRY_RUN=true python3 scripts/editorial_generator.py
# Verify: exits cleanly, no import errors, RSS feeds fetched

# 3. R-SEC-01 scan — no hardcoded keys in source
grep -rn 'phx_\|phc_\|pk_\|sk-\|ntn_\|AIzaSy\|xoxb-\|ghp_\|ghs_' scripts/*.py
# Verify: returns ZERO matches
```

**BLOCKED:** Deploy is blocked until local dry-run passes with zero errors.

### Pre-Deploy Gate: Secret Validation

```bash
# Verify all required secrets exist in Secret Manager BEFORE deploy
for secret in "github-token" "anthropic-api-key"; do
  if ! gcloud secrets versions list "$secret" --project=paradisemedia-bi > /dev/null 2>&1; then
    echo "ERROR: Secret '$secret' not found in Secret Manager"
    echo "DEPLOY BLOCKED — create secret first: gcloud secrets create $secret --data-file=-"
    exit 1
  fi
done
echo "All secrets verified."
```

### Post-Deploy Gate: R-DEPLOY-01 — Security Audit Checklist

**MANDATORY after EVERY Cloud Run deploy:**

```
Checks:
- [ ] IAM Policy: `gcloud run jobs get-iam-policy news-updater-australiafootball --region=us-central1`
      → Only `domain:paradisemedia.com` and service accounts. No `allUsers`.
- [ ] Secrets: Cloud Run job uses `--set-secrets` (not `--set-env-vars`) for GITHUB_TOKEN
- [ ] R-SEC-01 Scan: `grep -rn 'ghp_\|ghs_\|sk-\|phx_' scripts/*.py` → 0 matches
- [ ] Log Check: `gcloud logging read "resource.type=cloud_run_job" --limit=20 --project=paradisemedia-bi`
      → No token/key leakage in logs (sanitize_output covers this)
- [ ] Network: Cloud Run job only needs outbound HTTPS to GitHub, RSS feeds, foxsports.com.au
- [ ] Error Handling: Token validation raises ValueError if GITHUB_TOKEN missing when GIT_PUSH=true
```

**DEPLOY STATUS:** Only mark as `PRODUCTION READY` after all 6 checks pass.

### Credential Security (R-SEC-01)

| Credential | Source | Validated |
|---|---|---|
| GITHUB_TOKEN | Secret Manager `github-token:latest` | Yes — raises ValueError if missing when GIT_PUSH=true |
| ANTHROPIC_API_KEY | Secret Manager `anthropic-api-key:latest` | Yes — editorial_generator raises ValueError if missing |
| GIT_EMAIL | Env var with safe default `bot@paradisemedia.com` | Yes — no personal email in source |

**Log safety:** All subprocess stderr output sanitized via `_sanitize_output()` — tokens replaced with `***REDACTED***`.

---

## Trusted News Sources by Vertical

### Football (WC2026, Premier League, Serie A, Bundesliga)
- FIFA.com (Official - WC only)
- UEFA.com
- ESPN FC
- BBC Sport
- Sky Sports
- Goal.com
- The Guardian Football
- Reuters Sports
- AP News Sports

### Premier League Specific
- premierleague.com (Official)
- Sky Sports Premier League
- BBC Sport Football

### Serie A Specific
- legaseriea.it (Official)
- Football Italia
- Gazzetta dello Sport

### Bundesliga Specific
- bundesliga.com (Official)
- Kicker
- Sport1

### Ligue 1 Specific
- ligue1.com (Official)
- L'Equipe
- RMC Sport
- France Football
- So Foot

### Tennis
- atptour.com (Official ATP)
- wtatennis.com (Official WTA)
- ausopen.com, rolandgarros.com, wimbledon.com, usopen.org (Slams)
- Tennis.com
- ESPN Tennis

### Six Nations Rugby
- sixnationsrugby.com (Official)
- BBC Sport Rugby
- Rugby World
- World Rugby

### Australia Football (australiafootball.com) — 30 feeds across 4 source types

**RSS Feeds (19 direct feeds):**
- afl.com.au (Official AFL) — Tier 1
- Cricket Australia (Official) — Tier 1
- aleagues.com.au (Official A-Leagues) — Tier 1
- Formula1.com (Official) — Tier 1
- ATP Tour (Official Tennis) — Tier 1
- ABC Sport, The Guardian Sport, SMH Sport, The Age Sport, ESPN Australia — Tier 2
- UFC.com — Tier 2
- 7NEWS Sport, Sportal AU, PerthNow Sport, Speedcafe, League Freak, Soccer Scene AU — Tier 3

**Google News RSS (6 feeds for underserved verticals):**
- Matildas, Socceroos, NBL, Rugby Union (Wallabies), Horse Racing, V8 Supercars — Tier 4
- Uses `<source url="">` element to extract original publisher URL and name

**Reddit Atom (7 community feeds):**
- r/AFL, r/nrl, r/Aleague, r/Cricket, r/Matildas, r/socceroos, r/rugbyunion — Tier 5
- Filtered: Match Threads, Daily Threads, Mod Posts, short titles excluded
- External news URLs extracted from link posts

**Web Scrape (1 source):**
- foxsports.com.au — Tier 4 (scraper_foxsports.py, requires requests+bs4)

**Source Quality Weights:** Tier 1 (Official)=5, Tier 2 (Quality)=4, Tier 3 (Tabloid)=3, Tier 4 (Aggregated)=2, Tier 5 (Community)=1
**Article selection:** `weight = sport_diversity_weight * source_quality_weight`

**Sport verticals (all 12 covered):** AFL, NRL, A-League, W-League, Cricket/BBL, Socceroos, Matildas, NBL, Horse Racing, V8 Supercars, Rugby Union, UFC, NPL, World Cup, EPL, Tennis, F1, NBA
**Output format:** Astro markdown with frontmatter matching newsSchema (title, sport, date, author, excerpt, tags, source, externalUrl, sourceDomain, isAggregated)
**Path:** `~/australiafootball.com/src/content/news/`
**Implementation:** `~/australiafootball.com/scripts/news_updater.py` (Cloud Run Job, hourly)
**Cron:** Hourly via Cloud Scheduler (publishes ~1 article/hour with random jitter)

### Formula 1
- formula1.com (Official)
- Autosport
- Motorsport.com
- RaceFans
- The Race

---

## Execution Process

### Step 1: Parse Arguments

Based on `$ARGUMENTS`:
- No args or empty: Show project list and ask which to update
- `all`: Queue all projects for update
- `[project-id]`: Update specific project
- `status`: Show status of all projects
- `--dry-run [project]`: Test mode

### Step 1.5: Content Scope Intake (MANDATORY)

**BEFORE generating any content, ALWAYS ask the user two questions:**

1. **How many articles per site?** Present the site's available sections/categories and ask how many articles they want. Default suggestion: 1 per active section (full coverage).

2. **Which topics/sections to cover?** Show all available sections for each selected site with current article counts, and let the user choose which to cover. Default: all sections.

**Intake format:**
```
For [SITE NAME] ([N] sections available):
  Sections: [list all sections with article counts]
  Suggested: [N] articles (1 per section)

  How many articles? ___
  Which sections? (all / specific list) ___
```

**Why this is mandatory:** Each site has 10-15+ sections/categories. Without explicit scoping, the agent defaults to 3 articles covering only 2-3 sections, leaving the majority of the site stale. Full-coverage runs should target at minimum 1 article per section where real news exists.

### Step 2: For Each Selected Project

```bash
# Set project path
BASE_PATH="/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent"
PROJECT_PATH="$BASE_PATH/[PROJECT_FOLDER]"

# Use the shared news scripts
python3 "$BASE_PATH/scripts/cloud_news_updater.py" --project [project-id]

# Or for Astro-based aggregation:
# python3 "$BASE_PATH/scripts/astro_news_aggregator.py" --project [project-id]
```

### Step 2.5: Data Freshness Check (R-CONTENT-05 — MANDATORY for sports sites)

Before generating news articles, check if any standings/ladder/fixture pages are stale:

```
Checks:
- [ ] All ladder/standings pages show data from current round/matchweek
- [ ] No false freshness claims ("being updated") on pages without active pipelines (R-CONTENT-05a)
- [ ] "Last Updated" dates on data pages are within 7 days (R-CONTENT-05d)
- [ ] Off-season leagues correctly labelled "Final [YEAR] Standings" (R-CONTENT-05e)
```

**Data sources for verification:**
| League | Source | API/Method |
|--------|--------|------------|
| EPL | Football-Data.org | `X-Auth-Token` API v4 (TIER_ONE) |
| A-League Men/Women | Wikipedia | MediaWiki API parse |
| AFL, NRL, NBL, Cricket | Wikipedia | MediaWiki API parse |
| F1 | Ergast/Jolpica | REST API |

**If stale data found:** Flag to user BEFORE proceeding with news generation. Stale standings undermine site credibility more than missing news articles.

### Step 3: Ralph Loops QA (Per Article)

#### Cycle 1: Director Review
```
Checks:
- [ ] Has valid source citation with URL
- [ ] Source is from trusted news outlet for this vertical
- [ ] Has proper publication date (within 7 days)
- [ ] No placeholder text (TBD, TODO, etc.)
- [ ] Title is specific and meaningful
- [ ] Content is factually accurate
```

#### Cycle 2: Content Review
```
Checks:
- [ ] Adequate content length (500+ characters)
- [ ] Proper markdown structure with headers
- [ ] All internal links are valid
- [ ] Valid markdown syntax
- [ ] Has summary section
- [ ] Appropriate tone for sports journalism
```

#### Cycle 3: SEO/QA Review
```
Checks:
- [ ] Summary is SEO meta-ready (under 300 chars)
- [ ] Has category/sport tag
- [ ] All images exist and are linked
- [ ] Title contains relevant keywords
- [ ] Filename is URL-friendly
- [ ] No duplicate content across projects
```

#### Cycle 4: Internal Link Gate
```
Checks:
- [ ] ALL internal links return 200
- [ ] No broken image links
- [ ] Cross-links to related content work
- HARD GATE: Must pass with 0 broken links
```

#### Cycle 5: API Leak Compliance (R-SEO-04)
```
HARD checks (block if fail):
- [ ] Article stays within site's declared vertical (siteFocusScore) — HARD
- [ ] Article fulfills headline promise — no clickbait (badClicks prevention) — HARD
- [ ] If money page link added: gambling ratio still < 5% (numOfGamblingPages) — HARD

SOFT checks (flag for review):
- [ ] Article has > 500 words with subheadings (contentEffort)
- [ ] If AI-assisted: contains ≥ 2 unique data points not in source (racterScores)
- [ ] R-CONTENT-03 money page link uses keyword-rich anchor (R-ANCHOR-01)
- [ ] ISO datetime with R-CONTENT-04 stagger (freshboxArticleScores)

GATE: HARD checks must pass. SOFT checks flagged for manual review.
```

### Step 4: Report Results

```markdown
## News Update Agent Report

**Date:** [Date]
**Time:** [Time]
**Trigger:** Manual via /news_update_agent

### Projects Updated

| Project | Fetched | Passed QA | Added | Rejected |
|---------|---------|-----------|-------|----------|
| WC 2026 | X | X | X | X |
| Premier League | X | X | X | X |
| Serie A | X | X | X | X |
| ... | ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** | **X** |

### Ralph Loops Summary
- Cycle 1 (Director): X/X passed
- Cycle 2 (Content): X/X passed
- Cycle 3 (SEO/QA): X/X passed
- Cycle 4 (Links): X/X passed (0 broken)

### Rejected Articles
[List by project with rejection reasons]

### Git Status
- Branch: main
- Commits: [list]
- Pushed: Yes/No

---
News Update Agent v1.0 | Bedrock Agent System
```

---

## Project Paths Reference

| Project | News Output | Images | QA Reports |
|---------|-------------|--------|------------|
| WC 2026 | `WC_2026_Astro/src/content/news/` | `WC_2026_Astro/public/images/news/` | - |
| Premier League | `Premier_League_2025-26_Astro/src/content/news/` | `Premier_League_2025-26_Astro/public/images/news/` | - |
| Serie A | `Italian_Serie_A_Astro/src/content/news/` | `Italian_Serie_A_Astro/public/images/news/` | - |
| Bundesliga | `Bundesliga_2025-26_Astro_V2/src/content/news/` | `Bundesliga_2025-26_Astro_V2/public/images/news/` | - |
| Ligue 1 | `Ligue_1_2025-26_Astro/src/content/news/` | `Ligue_1_2025-26_Astro/public/images/news/` | - |
| Tennis | `Tennis_Grand_Slams_Astro/src/content/news/` | `Tennis_Grand_Slams_Astro/public/images/news/` | - |
| Six Nations | `Six_Nations_2026_Astro/src/content/news/` | `Six_Nations_2026_Astro/public/images/news/` | - |
| F1 | `F1_2026_Astro/src/content/news/` | `F1_2026_Astro/public/images/news/` | - |
| Australia Football | `~/australiafootball.com/src/content/news/` | `~/australiafootball.com/public/images/news/` | - |

---

## Status Command

When `status` is passed, show:

```bash
# For each project, show:
# 1. Total news articles
# 2. Last update date
# 3. News from last 7 days

for project in wc2026 premier-league serie-a bundesliga ligue1 tennis six-nations f1; do
    echo "=== $project ==="
    # Count files, show last modified, etc.
done
```

---

## Cron Integration

This agent can be scheduled:

```bash
# australiafootball.com - 09:00 AEST daily (editorial generator + news aggregator)
0 23 * * * /home/andre/scripts/australiafootball_daily_cron.sh

# Individual project news updates (use cloud_news_updater.py or astro_news_aggregator.py)
# Example: python3 ~/AS-Virtual_Team_System_v2/projects/bedrock_agent/scripts/cloud_news_updater.py --project wc2026
# Example: python3 ~/AS-Virtual_Team_System_v2/projects/bedrock_agent/scripts/astro_news_aggregator.py --site australiafootball
```

---

## Notes

- Always confirm with user before pushing to main
- Each project may have different news frequencies
- Some projects may have no news on certain days - this is OK
- Cross-check for duplicate stories across verticals
- Email report sent to: andre@paradisemedia.com
- Part of the Bedrock Agent ecosystem

---

*News Update Agent v2.0 | Bedrock Agent System | Paradise Media Group*
*Updated: 2026-03-03 — Expanded to 30 feeds (RSS+Google News+Reddit+FoxSports scrape), added security gates (R-SEC-01, R-DEBUG-01, R-DEPLOY-01), source quality weights*
