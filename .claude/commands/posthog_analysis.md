# /posthog_analysis - PostHog Analytics Report Generator

Generate comprehensive PostHog analytics reports for Paradise Media properties.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before generating reports.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings
- `~/.claude/standards/VALIDATION_STANDARDS.md` — Pre-response checklist

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("posthog analytics navboost", top_k=5)
learnings = rag.query("posthog report corrections", collection_name="learnings", top_k=3)
```

---

## PREFERRED: Use Full Analysis Script

**Run the comprehensive analysis script for ALL metrics:**
```bash
python3 /home/andre/projects/posthog-integration/scripts/full_posthog_analysis.py
```

This script fetches ALL available PostHog metrics including:
- Standard PostHog metrics (events, users, sessions, web vitals)
- All 18 NavBoost KPIs (Director Rule 18 compliant)
- Traffic, geographic, device, browser breakdowns
- Engagement score and composite metrics

## Quick Reference

| Rule | Requirement |
|------|-------------|
| R1 | PDF output with Paradise Media branding |
| R2 | Tables must not split across pages |
| R8 | Head of Product must be involved |
| R18 | All 18 NavBoost metrics required |
| R27 | Discover projects via API, not hardcoded list |
| R32 | Use canonical query template |

## Usage

```
/posthog_analysis run              # Generate reports for ALL projects
/posthog_analysis run all          # Generate reports for ALL projects
/posthog_analysis run domain.com   # Generate report for specific domain
```

## Arguments
- **run** or **run all**: Generate reports for all 6 PostHog projects
- **run [domain]**: Generate report for a specific domain (e.g., `run lover.io`, `run pokerology.com`)

### Director Rule 27: PostHog Project Discovery (Added: 2026-01-28)
**HARD RULE - NO EXCEPTIONS:** ALWAYS query PostHog API to discover projects. NEVER rely on the hardcoded list below.

```bash
# ALWAYS run this first to get current projects
curl -s "https://us.i.posthog.com/api/projects/" \
  -H "Authorization: Bearer $POSTHOG_PERSONAL_API_KEY" | python3 -c "
import json,sys
for p in json.load(sys.stdin):
    print(f'ID: {p[\"id\"]} | Name: {p[\"name\"]}')"
```

## Known Projects (MAY BE OUTDATED - Always verify with API)
| Domain | Project ID | Status |
|--------|-----------|--------|
| hudsonreporter.com | 295222 | Active (NavBoost v1.1.1) |
| lover.io | 290016 | Active |
| northeasttimes.com | 290039 | Active |
| pokerology.com | 266520 | Active (NavBoost) - NOTE: 294549 is EMPTY duplicate |
| europeangaming.eu | 290042 | Project exists |
| esports.gg | 291582 | Project exists |
| dotesports.com | 291573 | Active (NavBoost) |
| culture.org | 295239 | Active (NavBoost) |
| pokertube.com | 295249 | Project exists |
| bestdaily.com | 295235 | Project exists |
| betanews.com | 295236 | Project exists |
| centraljersey.com | 295237 | Project exists |
| godisageek.com | 295240 | Project exists |
| silvergames.com | 295250 | Project exists |
| snjtoday.com | 295251 | Project exists |
| *+ 15 more* | - | Query API for full list |

## Instructions

When this command is invoked:

### 1. Load Configuration & Library (MANDATORY - Rule 32)

**CRITICAL:** Always use the canonical PostHog metrics library:

```python
import sys
sys.path.insert(0, '/home/andre/virtual-ateam/BlackTeam/projects/posthog-integration/lib')
from posthog_metrics_lib import PostHogMetrics

# Initialize metrics client (auto-loads API key from ~/.keys/.env)
metrics = PostHogMetrics()

# Get ALL metrics for a domain in one call
data = metrics.get_complete_metrics(project_id=291573, days=7)

# Or get specific metric groups:
stats = metrics.get_overall_stats(project_id, days=7)
web_vitals = metrics.get_web_vitals(project_id, days=7)
navboost = metrics.get_all_navboost_metrics(project_id, days=7)
```

**Canonical Files (MUST USE):**
| File | Location | Purpose |
|------|----------|---------|
| Query Template | `~/virtual-ateam/BlackTeam/projects/posthog-integration/POSTHOG_QUERY_TEMPLATE.md` | All correct HogQL patterns |
| Metrics Library | `~/virtual-ateam/BlackTeam/projects/posthog-integration/lib/posthog_metrics_lib.py` | Python extraction functions |
| PDF Converter | `/tmp/claude/.../scratchpad/md_to_pdf_9domains_v2.py` | Rule-compliant PDF with page breaks |

### 1a. DataForSEO Integration (Metrics 12-14)
**DataForSEO is the PRIMARY source for SERP metrics.**

```python
# Use the unified NavBoost metrics collector
from lib.navboost_metrics import collect_navboost_metrics

# Get all 18 metrics (PostHog + DataForSEO combined)
metrics = collect_navboost_metrics("domain.com", project_id, days=7)

# Access SERP metrics specifically
serp_ctr = metrics["dataforseo_metrics"]["serp_ctr"]
impressions = metrics["dataforseo_metrics"]["impressions"]
avg_position = metrics["dataforseo_metrics"]["avg_position"]
```

**Library Location:** `/home/andre/virtual-ateam/BlackTeam/projects/posthog-integration/lib/`
- `posthog_metrics_lib.py` - **CANONICAL** PostHog metrics extraction (Rule 32)
- `dataforseo_client.py` - DataForSEO API client
- `navboost_metrics.py` - Unified metrics collector (PostHog + DataForSEO)

**Credentials:** Set in `/home/andre/.keys/.env`:
- `POSTHOG_PERSONAL_API_KEY` - PostHog API key (auto-loaded by library)
- `DATAFORSEO_LOGIN` - Your DataForSEO account email
- `DATAFORSEO_PASSWORD` - Your DataForSEO API password

### 2. Determine Scope
- If argument is `run` or `run all` → Process ALL projects
- If argument is `run [domain]` → Process only that domain
- Match domain case-insensitively (e.g., `Pokerology.com` = `pokerology.com`)

### 3. Project Mapping
```python
PROJECTS = {
    "hudsonreporter.com": {"id": 295222, "name": "HudsonReporter.com"},
    "lover.io": {"id": 290016, "name": "lover.io"},
    "northeasttimes.com": {"id": 290039, "name": "Northeastimes.com"},
    "pokerology.com": {"id": 266520, "name": "Pokerology.com"},  # CORRECT ID (294549 is empty duplicate)
    "europeangaming.eu": {"id": 290042, "name": "europeangaming.eu"},
    "esports.gg": {"id": 291582, "name": "Esports.gg"},
    "dotesports.com": {"id": 291573, "name": "Dotesports.com"},
}
```

### 4. Execute Report Generation
Run the PostHog report generator script:
```bash
python3 /home/andre/posthog_all_projects_report.py
```

Or for a single domain, query PostHog API directly and generate a markdown report.

### 5. Report Contents
Each report includes:
- **Web Analytics Overview:** Total events, unique users, sessions
- **Event Breakdown:** Top 10 events by count
- **Web Vitals:** LCP, CLS, INP with ratings (Good/Needs Improvement/Poor)
- **Scroll Depth:** Max scroll %, last scroll %
- **Top Pages:** Top 15 pages by views
- **Traffic Sources:** Referrer breakdown
- **Geographic Distribution:** Top 10 countries
- **Device Breakdown:** Mobile/Desktop/Tablet
- **Daily Trend:** Last 7 days
- **NAVBOOST METRICS (MANDATORY):** Pogo Rate, Dwell Time, Scroll Depth, CTA CTR, Good Abandonment, Engagement Score

### 6. Output Location
Reports are saved to:
```
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/reports/all_projects/
```

### 7. Web Vitals Thresholds
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤1200ms | ≤2500ms | >2500ms |
| CLS | ≤0.1 | ≤0.25 | >0.25 |
| INP | ≤200ms | ≤500ms | >500ms |

## HogQL Queries Reference

### Overall Stats
```sql
SELECT count() as total_events, uniqExact(distinct_id) as unique_users, uniqExact(properties.$session_id) as sessions
FROM events WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Event Breakdown
```sql
SELECT event, count() as count FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY event ORDER BY count DESC LIMIT 10
```

### Web Vitals
```sql
SELECT avg(properties.$web_vitals_LCP_value) as avg_LCP,
       avg(properties.$web_vitals_CLS_value) as avg_CLS,
       avg(properties.$web_vitals_INP_value) as avg_INP
FROM events WHERE event = '$web_vitals' AND timestamp >= now() - INTERVAL 7 DAY
```

### Top Pages
```sql
SELECT properties.$pathname as page, count() as views
FROM events WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY page ORDER BY views DESC LIMIT 15
```

### Traffic Sources
```sql
SELECT properties.$referring_domain as referrer, count() as count
FROM events WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY referrer ORDER BY count DESC LIMIT 10
```

### Geographic Distribution
```sql
SELECT properties.$geoip_country_name as country, count() as count
FROM events WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY country ORDER BY count DESC LIMIT 10
```

### Device Breakdown
```sql
SELECT properties.$device_type as device, count() as count
FROM events WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY device ORDER BY count DESC
```

### Daily Trend
```sql
SELECT toDate(timestamp) as date, count() as events, uniqExact(distinct_id) as users
FROM events WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY date ORDER BY date DESC
```

## NAVBOOST METRICS (MANDATORY - All 18 Required)

**CRITICAL:** NavBoost metrics MUST be included in every report. If no data exists, report "NavBoost Tracker Not Deployed" status.

### The 18 NavBoost Metrics (Director Rule 18)

| # | Metric | Target | Query Source |
|---|--------|--------|--------------|
| 1 | Session Starts | - | navboost:session_start count |
| 2 | Session Ends | - | navboost:session_end count |
| 3 | Heartbeat Count | - | navboost:heartbeat count |
| 4 | Pogo Rate | <18% | is_pogo=true / google_sessions |
| 5 | Pogo Sessions | - | is_pogo=true count |
| 6 | Avg Dwell Time | >90s | avg(dwell_time_seconds) |
| 7 | Median Dwell Time | >60s | median(dwell_time_seconds) |
| 8 | Dwell Distribution | - | countIf by range buckets |
| 9 | Scroll 25% | - | scroll_depth_reached >= 25 |
| 10 | Scroll 50% | >70% | scroll_depth_reached >= 50 |
| 11 | Scroll 75% | >40% | scroll_depth_reached >= 75 |
| 12 | Scroll 100% | - | scroll_depth_reached >= 100 |
| 13 | Avg Scroll Depth | >50% | avg(scroll_depth_reached) |
| 14 | CTA Visible | - | navboost:cta_visible count |
| 15 | CTA Clicks | - | navboost:cta_click count |
| 16 | CTA CTR | >5% | clicks / visible * 100 |
| 17 | Good Abandonment Rate | >15% | is_good_abandonment=true / google |
| 18 | Outbound Clicks | - | navboost:outbound_click count |

**Composite Metric:**
- **Engagement Score** (target >70): Weighted composite of dwell, pogo, scroll, CTA, abandonment

### NavBoost Event Check
```sql
SELECT event, count() as count
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
AND event LIKE 'navboost:%'
GROUP BY event
ORDER BY count DESC
```

### Pogo Rate (Target: < 18%)
```sql
SELECT
    countIf(properties.is_pogo = true) as pogo_sessions,
    count() as total_google_sessions,
    round(countIf(properties.is_pogo = true) * 100.0 / count(), 2) as pogo_rate
FROM events
WHERE event = 'navboost:session_end'
AND properties.is_google_referrer = true
AND timestamp >= now() - INTERVAL 7 DAY
```

### Dwell Time (Target: > 90s)
```sql
SELECT
    avg(properties.dwell_time_seconds) as avg_dwell,
    median(properties.dwell_time_seconds) as median_dwell,
    countIf(properties.dwell_time_seconds < 10) as very_bad,
    countIf(properties.dwell_time_seconds >= 10 AND properties.dwell_time_seconds < 30) as weak,
    countIf(properties.dwell_time_seconds >= 30 AND properties.dwell_time_seconds < 90) as normal,
    countIf(properties.dwell_time_seconds >= 90) as strong
FROM events
WHERE event = 'navboost:session_end'
AND timestamp >= now() - INTERVAL 7 DAY
```

### Scroll Depth (Target: 70% CTA Zone, 40% Below Fold)
**CORRECT PROPERTY:** `scroll_depth_reached` (NOT scroll_depth_percent)

```sql
-- Rule 32 compliant query
SELECT
    countIf(properties.scroll_depth_reached >= 25) as depth_25,
    countIf(properties.scroll_depth_reached >= 50) as depth_50,
    countIf(properties.scroll_depth_reached >= 75) as depth_75,
    countIf(properties.scroll_depth_reached >= 100) as depth_100,
    avg(properties.scroll_depth_reached) as avg_scroll,
    count() as total_sessions
FROM events
WHERE event = 'navboost:session_end'
AND timestamp >= now() - INTERVAL 7 DAY
```

### CTA Performance (Target: > 5% CTR)
```sql
SELECT
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    round(count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
          nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0), 2) as cta_ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
```

### Good Abandonment Rate (Target: > 15%)
```sql
SELECT
    countIf(properties.is_good_abandonment = true) as good_abandonment_sessions,
    count() as total_google_sessions,
    round(countIf(properties.is_good_abandonment = true) * 100.0 / count(), 2) as good_abandonment_rate
FROM events
WHERE event = 'navboost:session_end'
AND properties.is_google_referrer = true
AND timestamp >= now() - INTERVAL 7 DAY
```

### Engagement Score Calculation
```sql
SELECT
    round(
        (0.35 * least(avg(properties.dwell_time_seconds) / 90 * 100, 100)) +
        (0.25 * (100 - (countIf(properties.is_pogo = true) * 100.0 / count()))) +
        (0.15 * (countIf(properties.scroll_depth_reached >= 50) * 100.0 / count())) +
        (0.15 * 50) +  -- CTA CTR placeholder (calculate separately)
        (0.10 * (countIf(properties.is_good_abandonment = true) * 100.0 / count()))
    , 1) as engagement_score
FROM events
WHERE event = 'navboost:session_end'
AND properties.is_google_referrer = true
AND timestamp >= now() - INTERVAL 7 DAY
```

### NavBoost Thresholds Reference
| Metric | Target | Good | Excellent | Critical |
|--------|--------|------|-----------|----------|
| Pogo Rate | < 18% | < 15% | < 10% | > 25% |
| Dwell Time | > 90s | > 120s | > 180s | < 30s |
| Scroll (CTA Zone) | > 70% | > 75% | > 85% | < 50% |
| Scroll (Below Fold) | > 40% | > 50% | > 60% | < 25% |
| CTA CTR | > 5% | > 7% | > 10% | < 2% |
| Good Abandonment | > 15% | > 20% | > 25% | < 8% |
| Engagement Score | > 70 | > 75 | > 80 | < 50 |

## Example Output

### For ALL projects:
```
PostHog Analytics Reports Generated
====================================
Date: January 16, 2026

Projects Analyzed:
✅ lover.io - 2,207 events, 51 users
✅ northeasttimes.com - 37,713 events, 13,161 users
✅ pokerology.com - 160,402 events, 52,232 users
⏳ europeangaming.eu - No data
⏳ esports.gg - No data
⏳ dotesports.com - No data

Reports saved to: /mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/reports/all_projects/
```

### For single domain:
```
PostHog Analytics Report - pokerology.com
=========================================
Period: Last 7 Days

Total Events: 160,402
Unique Users: 52,232
Sessions: 55,942

Web Vitals:
- LCP: 3,093ms (Poor)
- CLS: 0.037 (Good)
- INP: 581ms (Poor)

Report saved to: pokerology_com_report_20260116.md
```

## API Configuration
- **PostHog Host:** https://us.i.posthog.com
- **API Key Location:** /home/andre/.keys/.env (POSTHOG_PERSONAL_API_KEY)
- **Organization:** PM (Paradise Media)

## NavBoost Tracker Deployment Status

| Domain | Tracker Status | Version | Setup Files | Next Action |
|--------|----------------|---------|-------------|-------------|
| hudsonreporter.com | DEPLOYED | v1.1.1 | READY | Deploy v1.1.2 fix |
| lover.io | NOT DEPLOYED | - | Not Created | Run /posthog_setup |
| northeasttimes.com | NOT DEPLOYED | - | READY | Deploy to WordPress |
| pokerology.com | NOT DEPLOYED | - | READY | Deploy to WordPress |
| europeangaming.eu | NOT DEPLOYED | - | READY | Deploy to WordPress |
| esports.gg | NOT DEPLOYED | - | Not Created | Run /posthog_setup |
| dotesports.com | NOT DEPLOYED | - | Not Created | Run /posthog_setup |

**Setup Files Location:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup/[domain]/`

## PDF Generation (MANDATORY - Rule 1, Rule 2)

**Every report MUST be generated as PDF with these requirements:**

### PDF Rules Compliance
| Rule | Requirement | Implementation |
|------|-------------|----------------|
| Rule 1 | Professional headers/footers | Paradise Media branding (orange #f97316) |
| Rule 2 | Tables MUST NOT split across pages | Use KeepTogether wrapper |
| - | Page breaks per domain | Each domain starts on new page |
| - | Alternating row colors | Gray #f3f4f6 for even rows |

### PDF Converter Location
```
~/virtual-ateam/BlackTeam/projects/posthog-integration/lib/md_to_pdf_posthog.py
```

### PDF Generation Command
```python
# After generating markdown report
from md_to_pdf_posthog import create_pdf

create_pdf(
    md_path="/home/andre/reports/posthog_report.md",
    pdf_path="/home/andre/reports/posthog_report.pdf"
)
```

### PDF Features (Current Implementation)
- Orange header bar with report title and timestamp
- Gray footer with "BlackTeam | Paradise Media Group | Director Rule 18 Compliant"
- Page numbers (Page X of Y)
- Page break before each domain section
- Tables with KeepTogether (no splitting)
- Alternating row colors for readability

## Related

### Canonical Reference Files (Rule 32 - MUST USE)
| File | Location | Purpose |
|------|----------|---------|
| **Query Template** | `~/virtual-ateam/BlackTeam/projects/posthog-integration/POSTHOG_QUERY_TEMPLATE.md` | All correct HogQL patterns |
| **Metrics Library** | `~/virtual-ateam/BlackTeam/projects/posthog-integration/lib/posthog_metrics_lib.py` | Python extraction functions |
| **Director Rules** | `~/virtual-ateam/BlackTeam/DIRECTOR_RULES.md` | Rule 1, 2, 8, 18, 27, 32 |

### Other References
- **NavBoost KPI Framework:** `~/virtual-ateam/BlackTeam/projects/posthog-integration/NAVBOOST_KPI_FRAMEWORK.md`
- **PostHog Registry:** `~/virtual-ateam/BlackTeam/projects/posthog-integration/POSTHOG_REGISTRY.md`
- ClickUp Analytics Task: 86aeh5bp9
