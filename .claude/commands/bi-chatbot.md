# /BI-Chatbot - Paradise Media BI Data Assistant

## Command: /BI-Chatbot

**Purpose:** Natural language interface to query Paradise Media BI data from BigQuery with deep SEO and revenue analysis.

**Dataset:** `paradisemedia-bi.chatbot`
**Learning Context:** `/home/andre/.claude/context/BI-Chatbot_Context.md`

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before answering queries.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/.claude/context/BI-Chatbot_Context.md` — BI-Chatbot learning context
- `~/.claude/standards/VALIDATION_STANDARDS.md` — Pre-response checklist

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("BI chatbot bigquery data accuracy", top_k=5)
learnings = rag.query("data accuracy corrections numerical validation", collection_name="learnings", top_k=3)
```

---

## BigQuery Configuration

### Service Account
```bash
# CORRECT - Use this for BigQuery access
export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/bi-chatbot-sa.json
# Account: andre-claude@paradisemedia-bi.iam.gserviceaccount.com
```

### DO NOT USE
```bash
# WRONG - No BigQuery access
# /home/andre/secrets/paradisemedia-bi-sa.json (papaya-drive-uploader)
```

---

## IMPORTANT: Learning Protocol

After EVERY analysis session:
1. **Read** the learning context file
2. **Update** with new patterns, insights, or data gaps discovered
3. **Log** the session with query type and findings
4. **Flag** any missing data that would have improved the analysis

---

## Quick Start

```
/BI-Chatbot How many articles are published on snjtoday.com?
/BI-Chatbot What are the top 10 performing URLs by commission?
/BI-Chatbot Analyze why thesunpapers.com performs so well
/BI-Chatbot Show me FTD vs Legacy revenue breakdown
/BI-Chatbot Which URLs have high DR backlinks but low revenue?
```

---

## Analysis Framework (MANDATORY)

For ANY performance analysis, include ALL applicable dimensions:

### 1. Revenue Attribution (CRITICAL)

**Always distinguish New Player vs Legacy Revenue:**

```sql
-- FTD / New Player vs Legacy Analysis
SELECT
  a.LIVE_URL,
  d.DOMAIN,
  SUM(p.TOTAL_COMMISSION_USD_NP) as new_player_revenue,
  SUM(p.TOTAL_COMMISSION_USD_LP) as legacy_revenue,
  SUM(p.TOTAL_COMMISSION_USD) as total_revenue,
  ROUND(SUM(p.TOTAL_COMMISSION_USD_NP) * 100.0 /
    NULLIF(SUM(p.TOTAL_COMMISSION_USD), 0), 1) as np_percentage,
  SUM(p.CONVERSIONS) as ftds
FROM `paradisemedia-bi.chatbot.ARTICLE_PERFORMANCE` p
JOIN `paradisemedia-bi.chatbot.ARTICLE_INFORMATION` a ON p.ARTICLE_KEY = a.ARTICLE_KEY
JOIN `paradisemedia-bi.chatbot.DIM_DOMAIN` d ON a.DOMAIN_KEY = d.DOMAIN_KEY
WHERE p.DATE >= '2026-01-01'
GROUP BY a.LIVE_URL, d.DOMAIN
```

**Revenue Classification:**
- **High NP% (>70%):** New content acquiring players - GROWTH asset
- **High LP% (>70%):** Legacy content monetizing existing players - STABLE asset
- **Mixed (30-70% split):** Balanced portfolio - MATURE asset

### 2. SEO Deep Dive

#### Domain-Level Metrics
```sql
SELECT
  d.DOMAIN,
  ad.DOMAIN_RATING as DR,
  ad.DOMAIN_ORG_TRAFFIC as organic_traffic,
  ad.DOMAIN_ORG_KEYWORDS as ranking_keywords,
  ad.DOMAIN_TOP3_KEYWORDS as top3_keywords,
  ad.DOMAIN_BACKLINKS as total_backlinks,
  ad.DOMAIN_REFDOMAINS as referring_domains,
  ROUND(ad.DOMAIN_BACKLINKS * 1.0 / NULLIF(ad.DOMAIN_REFDOMAINS, 0), 1) as links_per_refdom
FROM `paradisemedia-bi.chatbot.AHREFS_DOMAIN` ad
JOIN `paradisemedia-bi.chatbot.DIM_DOMAIN` d ON ad.DOMAIN_KEY = d.DOMAIN_KEY
WHERE ad.DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.chatbot.AHREFS_DOMAIN`)
```

#### Page-Level Metrics
```sql
SELECT
  a.LIVE_URL,
  ap.URL_RATING as UR,
  ap.PAGE_ORG_TRAFFIC as page_traffic,
  ap.PAGE_ORG_KEYWORDS as page_keywords,
  ap.PAGE_BACKLINKS as page_backlinks,
  ap.PAGE_REFDOMAINS as page_refdomains,
  ap.PAGE_ALL_TIME_BACKLINKS as historical_backlinks,
  ap.PARENT_TOPIC as topic
FROM `paradisemedia-bi.chatbot.AHREFS_PAGE` ap
JOIN `paradisemedia-bi.chatbot.ARTICLE_INFORMATION` a ON ap.ARTICLE_KEY = a.ARTICLE_KEY
WHERE ap.DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.chatbot.AHREFS_PAGE`)
```

#### Backlink Quality Assessment

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| Domain DR | 50+ | 30-49 | <30 |
| Page UR | 20+ | 10-19 | <10 |
| Links per RefDom | 1.5-3 | 3-10 | 10+ (spammy) |
| RefDomains | 50+ | 10-49 | <10 |

### 3. Content Quality Signals

**Keyword Intent Classification:**

| Intent | Keywords | Value |
|--------|----------|-------|
| Transactional | "best", "top", "bonus code", "promo" | HIGH |
| Commercial | "review", "vs", "compare", "alternative" | MEDIUM-HIGH |
| Informational | "how to", "what is", "guide" | MEDIUM |
| Navigational | Brand names, site names | LOW |

**Content Quality Flags:**
- **Thin Content:** <1000 words (flag for expansion)
- **Missing H1:** No primary heading
- **Poor Structure:** No H2 subheadings
- **Stale Content:** Not refreshed in 6+ months

### 4. Competitive Analysis

When analyzing top performers, ALWAYS ask:
- What keywords are they ranking for?
- Who else ranks for these keywords?
- What's the backlink gap vs competitors?
- What content structure do competitors use?

**Competitor Identification Query:**
```sql
-- Find competing URLs by niche + geo
SELECT
  a.LIVE_URL,
  d.DOMAIN,
  v.NICHE,
  a.TARGET_GEO,
  SUM(p.TOTAL_COMMISSION_USD) as revenue
FROM `paradisemedia-bi.chatbot.ARTICLE_INFORMATION` a
JOIN `paradisemedia-bi.chatbot.DIM_DOMAIN` d ON a.DOMAIN_KEY = d.DOMAIN_KEY
JOIN `paradisemedia-bi.chatbot.DIM_VERTICAL` v ON a.VERTICAL_KEY = v.VERTICAL_KEY
LEFT JOIN `paradisemedia-bi.chatbot.ARTICLE_PERFORMANCE` p ON a.ARTICLE_KEY = p.ARTICLE_KEY
WHERE v.NICHE = '{TARGET_NICHE}'
  AND a.TARGET_GEO = '{TARGET_GEO}'
GROUP BY a.LIVE_URL, d.DOMAIN, v.NICHE, a.TARGET_GEO
ORDER BY revenue DESC
```

---

## Dataset Schema

### Core Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `ARTICLE_INFORMATION` | Article metadata (52K+ rows) | ARTICLE_KEY, TASK_NAME, LIVE_URL, STATUS, PUBLISH_DATE, TARGET_GEO |
| `ARTICLE_PERFORMANCE` | Revenue & conversion data | CLICKS, SIGNUPS, CONVERSIONS, TOTAL_COMMISSION_USD, TOTAL_COMMISSION_USD_NP, TOTAL_COMMISSION_USD_LP, BRAND, PROGRAM |
| `DIM_DOMAIN` | Domain dimension | DOMAIN_KEY, DOMAIN, IS_CLOAKING, PUBLISHING_GROUP |
| `DIM_VERTICAL` | Vertical dimension | VERTICAL_KEY, DEPARTMENT, NICHE, SUBNICHE |
| `DIM_ARTICLE_LABELS` | Article flags | IS_TEST_KEYWORD, IS_NEW_PUBLISHER |
| `AHREFS_DOMAIN` | Domain SEO metrics | DOMAIN_RATING, DOMAIN_ORG_TRAFFIC, DOMAIN_BACKLINKS, DOMAIN_REFDOMAINS |
| `AHREFS_PAGE` | Page SEO metrics | URL_RATING, PAGE_ORG_TRAFFIC, PAGE_BACKLINKS, PAGE_REFDOMAINS, PARENT_TOPIC |

### Key Revenue Fields

| Field | Description | Use For |
|-------|-------------|---------|
| `TOTAL_COMMISSION_USD` | Total revenue | Overall performance |
| `TOTAL_COMMISSION_USD_NP` | New Player commission | Growth/acquisition analysis |
| `TOTAL_COMMISSION_USD_LP` | Legacy Player commission | Retention/stable revenue |
| `CONVERSIONS` | FTDs (First Time Deposits) | New player acquisition |
| `SIGNUPS` | Registrations | Funnel top |
| `EPC` | Earnings per click | Efficiency metric |

---

## Learned Patterns (from Context File)

### High-Performance Indicators

| Pattern | Threshold | Confidence |
|---------|-----------|------------|
| Domain DR | 50+ | HIGH |
| Australia geo-targeting | /au/ path | HIGH |
| Multi-brand strategy | 15+ brands | HIGH |
| REVENUE_NETWORK program | Primary program | HIGH |
| Commercial intent keywords | "fast payout", "real money" | HIGH |
| Page backlinks | 50+ | MEDIUM |

### Top Brands by EPC

| Brand | EPC | Best For |
|-------|-----|----------|
| MYBOOKIE | $725 | Premium betting |
| CAFECASINO | $61 | US casino |
| SLOTS_LV | $33 | US slots |
| IGNITIONCASINO | $25 | Volume |

### Geographic Performance

| Geo | Revenue Share | Key Domains |
|-----|---------------|-------------|
| Australia | ~40% | thesunpapers, pokerology |
| US State-specific | ~25% | newgamenetwork, metrotimes |
| Europe | ~15% | europeangaming, esports.gg |

---

## Query Execution

```bash
bq query --use_legacy_sql=false --format=prettyjson "YOUR_SQL_HERE"
```

**Connection:**
- Project: `paradisemedia-bi`
- Dataset: `chatbot`

---

## Analysis Templates

### Full URL Performance Analysis

```sql
WITH latest_domain_seo AS (
  SELECT * FROM `paradisemedia-bi.chatbot.AHREFS_DOMAIN`
  WHERE DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.chatbot.AHREFS_DOMAIN`)
),
latest_page_seo AS (
  SELECT * FROM `paradisemedia-bi.chatbot.AHREFS_PAGE`
  WHERE DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.chatbot.AHREFS_PAGE`)
),
perf AS (
  SELECT
    ARTICLE_KEY,
    SUM(CLICKS) as clicks,
    SUM(SIGNUPS) as signups,
    SUM(CONVERSIONS) as ftds,
    SUM(TOTAL_COMMISSION_USD) as total_rev,
    SUM(TOTAL_COMMISSION_USD_NP) as np_rev,
    SUM(TOTAL_COMMISSION_USD_LP) as lp_rev,
    STRING_AGG(DISTINCT BRAND, ', ') as brands,
    STRING_AGG(DISTINCT PROGRAM, ', ') as programs
  FROM `paradisemedia-bi.chatbot.ARTICLE_PERFORMANCE`
  WHERE DATE >= '2026-01-01'
  GROUP BY ARTICLE_KEY
)
SELECT
  a.LIVE_URL,
  d.DOMAIN,
  v.NICHE,
  a.PUBLISH_DATE,
  DATE_DIFF(CURRENT_DATE(), a.PUBLISH_DATE, DAY) as days_live,
  -- SEO
  lds.DOMAIN_RATING as dr,
  lds.DOMAIN_ORG_TRAFFIC as domain_traffic,
  lps.URL_RATING as ur,
  lps.PAGE_BACKLINKS as page_backlinks,
  lps.PAGE_REFDOMAINS as page_refdoms,
  -- Revenue
  p.total_rev,
  p.np_rev,
  p.lp_rev,
  ROUND(p.np_rev * 100.0 / NULLIF(p.total_rev, 0), 1) as np_pct,
  p.ftds,
  p.clicks,
  ROUND(p.total_rev / NULLIF(DATE_DIFF(CURRENT_DATE(), a.PUBLISH_DATE, DAY), 0), 2) as daily_velocity,
  -- Brands
  p.brands,
  p.programs
FROM perf p
JOIN `paradisemedia-bi.chatbot.ARTICLE_INFORMATION` a ON p.ARTICLE_KEY = a.ARTICLE_KEY
JOIN `paradisemedia-bi.chatbot.DIM_DOMAIN` d ON a.DOMAIN_KEY = d.DOMAIN_KEY
JOIN `paradisemedia-bi.chatbot.DIM_VERTICAL` v ON a.VERTICAL_KEY = v.VERTICAL_KEY
LEFT JOIN latest_domain_seo lds ON d.DOMAIN_KEY = lds.DOMAIN_KEY
LEFT JOIN latest_page_seo lps ON a.ARTICLE_KEY = lps.ARTICLE_KEY
WHERE a.LIVE_URL IS NOT NULL
  AND a.LIVE_URL NOT LIKE '%NotApplicable%'
ORDER BY p.total_rev DESC
LIMIT 25
```

### Revenue Velocity Leaders

```sql
SELECT
  a.LIVE_URL,
  d.DOMAIN,
  a.PUBLISH_DATE,
  DATE_DIFF(CURRENT_DATE(), a.PUBLISH_DATE, DAY) as days_live,
  SUM(p.TOTAL_COMMISSION_USD) as total_rev,
  ROUND(SUM(p.TOTAL_COMMISSION_USD) /
    NULLIF(DATE_DIFF(CURRENT_DATE(), a.PUBLISH_DATE, DAY), 0), 2) as daily_velocity
FROM `paradisemedia-bi.chatbot.ARTICLE_PERFORMANCE` p
JOIN `paradisemedia-bi.chatbot.ARTICLE_INFORMATION` a ON p.ARTICLE_KEY = a.ARTICLE_KEY
JOIN `paradisemedia-bi.chatbot.DIM_DOMAIN` d ON a.DOMAIN_KEY = d.DOMAIN_KEY
WHERE p.DATE >= '2026-01-01'
  AND a.PUBLISH_DATE IS NOT NULL
GROUP BY a.LIVE_URL, d.DOMAIN, a.PUBLISH_DATE
HAVING SUM(p.TOTAL_COMMISSION_USD) > 5000
ORDER BY daily_velocity DESC
LIMIT 20
```

---

## Data Gaps to Flag

When analysis is limited by missing data, ALWAYS note:

| Missing Data | Impact | Workaround |
|--------------|--------|------------|
| Page Ahrefs (NULL) | Can't assess page authority | Use domain metrics |
| Word count | Can't flag thin content | Manual check |
| SERP position | Can't track rankings | Use traffic as proxy |
| Competitor URLs | No competitive analysis | Manual research |
| Content structure | No H1/H2 analysis | Manual audit |

---

## Security Rules

1. **Internal Analysis OK**: Show actual commission values for internal analysis
2. **Stakeholder Reports**: Use %GT for external stakeholders
3. **Query Limits**: Always include LIMIT clause
4. **No PII**: Never expose user-level data

---

## Post-Analysis Protocol

After completing analysis:

### 1. Store Results
**Location:** `/home/andre/.claude/context/bi-chatbot_results/`

Save analysis results for future reference:
```
Filename: YYYY-MM-DD_[query-type]_[description].md
Example: 2026-01-22_top-urls_commission-2026.md
```

Include:
- Query summary
- Data tables
- Key patterns
- Recommendations
- Data gaps found

### 2. Log Prompts
**Location:** `/home/andre/.claude/context/bi-chatbot_prompts/`

Log user prompts and instructions:
```
Filename: YYYY-MM-DD_session-[N]_[topic].md
```

Include:
- User prompts verbatim
- User corrections/feedback
- Learnings from session
- Command updates made

### 3. Update Context File
**Location:** `/home/andre/.claude/context/BI-Chatbot_Context.md`

- Add new patterns discovered
- Log data gaps encountered
- Update brand/program performance
- Note any anomalies

### 4. Update Index Files
- `bi-chatbot_results/INDEX.md` - Add new result entry
- `bi-chatbot_prompts/INDEX.md` - Add prompt log entry

---

## Folder Structure

```
/home/andre/.claude/context/
├── BI-Chatbot_Context.md           # Learning context & patterns
├── bi-chatbot_results/
│   ├── INDEX.md                    # Results index
│   └── YYYY-MM-DD_*.md             # Analysis results
└── bi-chatbot_prompts/
    ├── INDEX.md                    # Prompts index
    └── YYYY-MM-DD_*.md             # Session logs
```

---

## Referencing Previous Analysis

In future queries, check previous results:
```bash
# List recent results
ls -la /home/andre/.claude/context/bi-chatbot_results/

# Read previous analysis
cat /home/andre/.claude/context/bi-chatbot_results/2026-01-22_top-urls_commission-2026.md
```

Use learnings from prompts log:
```bash
# Check what users commonly ask for
cat /home/andre/.claude/context/bi-chatbot_prompts/INDEX.md
```

---

## CONTENT TEAM TEMPLATES (REMINDER)

When the user asks for **infographics** or **visual reports**, remind them:

> **Template Available:** FTD Decline Infographic template is available for monthly sendouts.
> Location: `/home/andre/virtual-ateam/BlackTeam/templates/content-team/FTD_DECLINE_INFOGRAPHIC_TEMPLATE.py`

**Use this template for:**
- Monthly FTD performance reports
- SEO analysis visuals
- Page decline analysis infographics

**Template includes:**
- DataForSEO metrics integration
- SERP rankings display
- Alarms section
- Root cause analysis
- Comparison bar chart
- PixelPerfect QA checklist

**Review Chain Required:**
```
PixelPerfect (creates) -> Product Manager (reviews) -> Head of SEO -> Director
```

---

*BI-Chatbot v2.0 | Paradise Media Group | Self-Learning Enabled*
