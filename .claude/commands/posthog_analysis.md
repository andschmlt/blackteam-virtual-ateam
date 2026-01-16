# /posthog_analysis - PostHog Analytics Report Generator

Generate comprehensive PostHog analytics reports for Paradise Media properties.

## Usage

```
/posthog_analysis run              # Generate reports for ALL projects
/posthog_analysis run all          # Generate reports for ALL projects
/posthog_analysis run domain.com   # Generate report for specific domain
```

## Arguments
- **run** or **run all**: Generate reports for all 6 PostHog projects
- **run [domain]**: Generate report for a specific domain (e.g., `run lover.io`, `run pokerology.com`)

## Available Domains
| Domain | Project ID | Status |
|--------|-----------|--------|
| lover.io | 290016 | Active |
| northeasttimes.com | 290039 | Active |
| pokerology.com | 266520 | Active |
| europeangaming.eu | 290042 | No Data |
| esports.gg | 291582 | No Data |
| dotesports.com | 291573 | No Data |

## Instructions

When this command is invoked:

### 1. Load Configuration
```bash
export POSTHOG_PERSONAL_API_KEY=$(grep POSTHOG_PERSONAL_API_KEY /home/andre/.keys/.env | cut -d'=' -f2)
export CLICKUP_API_KEY=$(grep CLICKUP_API_KEY /home/andre/.keys/.env | cut -d'=' -f2 2>/dev/null || cat /home/andre/.claude/clickup_config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['CLICKUP_API_KEY'])")
```

### 2. Determine Scope
- If argument is `run` or `run all` → Process ALL projects
- If argument is `run [domain]` → Process only that domain
- Match domain case-insensitively (e.g., `Pokerology.com` = `pokerology.com`)

### 3. Project Mapping
```python
PROJECTS = {
    "lover.io": {"id": 290016, "name": "lover.io"},
    "northeasttimes.com": {"id": 290039, "name": "Northeastimes.com"},
    "pokerology.com": {"id": 266520, "name": "Pokerology.com"},
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

## Director Rule: PDF Output (MANDATORY)
**All analysis reports MUST be generated as PDF in addition to markdown.**

Per Director Rules (2026-01-16): Reports with data/metrics must be converted to PDF format for professional, shareable deliverables.

## Related
- Main report script: `/home/andre/posthog_all_projects_report.py`
- Daily report script (lover.io): `/home/andre/lover.io/scripts/posthog_daily_report.py`
- Director Rules: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/DIRECTOR_RULES.md`
- ClickUp Analytics Task: 86aeh5bp9
