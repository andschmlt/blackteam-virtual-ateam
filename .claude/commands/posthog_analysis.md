# /posthog_analysis - PostHog Analytics Report Generator

Generate comprehensive PostHog analytics reports for Paradise Media properties.

## HARD RULES (MANDATORY - NO EXCEPTIONS)

### Director Rule 8: Head of Product Assignment
**Head of Product MUST be involved in ALL PostHog analytics work.**

When this command is invoked:
1. Head of Product is automatically assigned to the task
2. Analysis reports MUST include a "Product Insights" section
3. HoP reviews metric interpretation and strategic implications

### Director Rule 1: PDF Output (MANDATORY)
**All analysis reports MUST be generated as PDF in addition to markdown.**
- Use ReportLab with Paradise Media branding (orange #f97316, black #1a1a1a)
- Professional headers/footers with BlackTeam branding
- Tables must use alternating row colors
- Tables MUST NOT be split across pages (Rule 2)

### Director Rule 18: Mandatory NavBoost Metrics (Updated: 2026-01-28)
**HARD RULE - NO EXCEPTIONS:** ALL reports MUST include the complete 18-metric NavBoost inventory with Source column.

**REFERENCE:** `~/virtual-ateam/BlackTeam/NAVBOOST_METRICS_MAP.md` - Full extraction queries

**MANDATORY METRICS (18 Total) - EVERY REPORT MUST INCLUDE:**

| # | Metric | Source Event | Source Property | Target |
|---|--------|--------------|-----------------|--------|
| 1 | Dwell Time (avg) | `navboost:session_end` | `properties.dwell_time_seconds` | >90s |
| 2 | Pogo Rate | `navboost:session_end` | `properties.is_pogo` | <18% |
| 3 | Scroll Depth (25%) | `navboost:scroll_zone` | count where depth=25 | - |
| 4 | Scroll Depth (50%) | `navboost:scroll_zone` | count where depth=50 | - |
| 5 | Scroll Depth (75%) | `navboost:scroll_zone` | count where depth=75 | - |
| 6 | Scroll Depth (100%) | `navboost:scroll_zone` | count where depth=100 | - |
| 7 | CTA Visible | `navboost:cta_visible` | event count | - |
| 8 | CTA Clicks | `navboost:cta_click` | event count | - |
| 9 | CTA CTR | Calculated | #8 / #7 * 100 | >5% |
| 10 | Good Abandonment | `navboost:session_end` | `properties.is_good_abandonment` | >15% |
| 11 | Session Starts | `navboost:session_start` | event count | - |
| 12 | Session Ends | `navboost:session_end` | event count | - |
| 13 | SERP Return Rate | `navboost:session_end` | = Pogo Rate (Google traffic) | <25% |
| 14 | Engagement Score | Calculated | See NAVBOOST_METRICS_MAP.md | >70 |
| 15 | Outbound Clicks | `navboost:session_end` | `properties.outbound_clicks` | - |
| 16 | Heartbeat Events | `navboost:heartbeat` | event count | - |
| 17 | Toplist Row Visible | `navboost:toplist_row_visible` | event count (if applicable) | N/A |
| 18 | Session Time (avg) | `navboost:session_end` | = Dwell Time (#1) | >60s |

**CRITICAL: Never show "NOT TRACKED" if data exists in event properties.**
- Query event COUNTS first, then query PROPERTIES from session_end
- Show "0" if metric tracked but no data, "N/A" if not applicable

**Reports missing ANY metric are flagged as INCOMPLETE.**

See: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/DIRECTOR_RULES.md` - Rules 1, 8, 18

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
| pokerology.com | 294549 | Active |
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

### 1. Load Configuration
```bash
export POSTHOG_PERSONAL_API_KEY=$(grep POSTHOG_PERSONAL_API_KEY /home/andre/.keys/.env | cut -d'=' -f2)
export CLICKUP_API_KEY=$(grep CLICKUP_API_KEY /home/andre/.keys/.env | cut -d'=' -f2 2>/dev/null || cat /home/andre/.claude/clickup_config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['CLICKUP_API_KEY'])")
export DATAFORSEO_LOGIN=$(grep DATAFORSEO_LOGIN /home/andre/.keys/.env | cut -d'=' -f2)
export DATAFORSEO_PASSWORD=$(grep DATAFORSEO_PASSWORD /home/andre/.keys/.env | cut -d'=' -f2)
```

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

**Library Location:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/lib/`
- `dataforseo_client.py` - DataForSEO API client
- `navboost_metrics.py` - Unified metrics collector (PostHog + DataForSEO)

**Credentials:** Set in `/home/andre/.keys/.env`:
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
    "pokerology.com": {"id": 294549, "name": "Pokerology.com"},
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

## NAVBOOST METRICS (MANDATORY)

**CRITICAL:** NavBoost metrics MUST be included in every report. If no data exists, report "NavBoost Tracker Not Deployed" status.

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
```sql
SELECT
    properties.scroll_depth_percent as depth,
    count() as sessions
FROM events
WHERE event = 'navboost:scroll_zone'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY depth
ORDER BY depth
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

## Related
- **NavBoost KPI Framework:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/NAVBOOST_KPI_FRAMEWORK.md`
- Main report script: `/home/andre/posthog_all_projects_report.py`
- Daily report script (lover.io): `/home/andre/lover.io/scripts/posthog_daily_report.py`
- Director Rules: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/DIRECTOR_RULES.md`
- ClickUp Analytics Task: 86aeh5bp9
