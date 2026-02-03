# CTA Performance Dashboard - HogQL Queries

**Project:** PostHog NavBoost Integration
**Dashboard:** CTA Performance Analysis
**Version:** 1.0.0
**Created:** 2026-02-03
**Author:** W-DASH (BI Developer) + W-FLUX (DataForge)

---

## Dashboard Overview

This dashboard provides URL-level CTA performance analysis including:
- CTA impressions, clicks, and CTR by type
- Per-URL CTA breakdown
- Affiliate link performance
- Top/bottom performing CTAs
- Trend analysis

---

## Query 1: Overall CTA Metrics (Last 7 Days)

**Purpose:** Executive summary of CTA performance

```sql
SELECT
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as total_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as total_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as overall_ctr,
    uniqExact(properties.cta_id) as unique_ctas_tracked,
    uniqExact(properties.page_path) as pages_with_ctas
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
```

---

## Query 2: CTA Performance by Type

**Purpose:** Compare CTA types (affiliate, social, newsletter, etc.)

```sql
SELECT
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr,
    uniqExact(properties.page_path) as pages_appearing
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY cta_type
ORDER BY impressions DESC
```

---

## Query 3: CTA Performance by URL (Page-Level)

**Purpose:** Identify which pages have best/worst CTA performance

```sql
SELECT
    properties.page_path as page_url,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as page_cta_ctr,
    uniqExact(properties.cta_type) as cta_types_on_page
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY page_url
HAVING cta_impressions > 10
ORDER BY page_cta_ctr DESC
LIMIT 50
```

---

## Query 4: Top Performing Individual CTAs

**Purpose:** Identify best performing CTA elements by text/href

```sql
SELECT
    properties.cta_text as cta_text,
    properties.cta_href as cta_href,
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
AND properties.cta_text != ''
GROUP BY cta_text, cta_href, cta_type
HAVING impressions >= 10
ORDER BY ctr DESC
LIMIT 25
```

---

## Query 5: Bottom Performing CTAs (Optimization Opportunities)

**Purpose:** Find CTAs with high impressions but low clicks

```sql
SELECT
    properties.cta_text as cta_text,
    properties.cta_href as cta_href,
    properties.cta_type as cta_type,
    properties.page_path as sample_page,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
AND properties.cta_text != ''
GROUP BY cta_text, cta_href, cta_type, sample_page
HAVING impressions >= 50 AND ctr < 2
ORDER BY impressions DESC
LIMIT 25
```

---

## Query 6: Affiliate CTA Performance (High Value)

**Purpose:** Track affiliate/monetization CTAs specifically

```sql
SELECT
    properties.cta_text as cta_text,
    properties.cta_href as affiliate_url,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr,
    uniqExact(properties.page_path) as pages_appearing
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
AND (
    properties.cta_href LIKE '%/go/%'
    OR properties.cta_href LIKE '%/out/%'
    OR properties.cta_href LIKE '%affiliate%'
    OR properties.cta_type IN ('affiliate', 'social_twitter', 'social_facebook')
)
GROUP BY cta_text, affiliate_url
ORDER BY clicks DESC
LIMIT 30
```

---

## Query 7: Outbound Click Analysis (/go/ Pattern Detection)

**Purpose:** Track all outbound clicks with affiliate detection

```sql
SELECT
    properties.outbound_domain as destination,
    properties.link_type as link_type,
    countIf(properties.is_affiliate = true) as affiliate_clicks,
    countIf(properties.is_affiliate = false OR properties.is_affiliate IS NULL) as non_affiliate_clicks,
    count() as total_clicks,
    round(countIf(properties.is_affiliate = true) * 100.0 / count(), 2) as affiliate_pct,
    uniqExact(properties.page_path) as source_pages
FROM events
WHERE event = 'navboost:outbound_click'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY destination, link_type
ORDER BY total_clicks DESC
LIMIT 30
```

---

## Query 8: CTA Performance by URL + CTA Type (Detailed Matrix)

**Purpose:** Full breakdown of which CTA types perform best on which pages

```sql
SELECT
    properties.page_path as page_url,
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY page_url, cta_type
HAVING impressions >= 5
ORDER BY page_url, impressions DESC
```

---

## Query 9: CTA Visibility to Click Time Analysis

**Purpose:** How long does it take users to click after seeing a CTA?

```sql
SELECT
    properties.cta_type as cta_type,
    avg(properties.time_to_click) as avg_time_to_click_sec,
    median(properties.time_to_click) as median_time_to_click_sec,
    min(properties.time_to_click) as min_time_to_click_sec,
    max(properties.time_to_click) as max_time_to_click_sec,
    count() as total_clicks
FROM events
WHERE event = 'navboost:cta_click'
AND timestamp >= now() - INTERVAL 7 DAY
AND properties.time_to_click IS NOT NULL
GROUP BY cta_type
ORDER BY avg_time_to_click_sec ASC
```

---

## Query 10: Daily CTA Trend (7-Day)

**Purpose:** Track CTA performance trend over time

```sql
SELECT
    toDate(timestamp) as date,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as daily_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as daily_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as daily_ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY date
ORDER BY date ASC
```

---

## Query 11: Pages With Zero CTA Clicks (Attention Needed)

**Purpose:** Find pages where CTAs are seen but never clicked

```sql
SELECT
    properties.page_path as page_url,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY page_url
HAVING cta_impressions >= 20 AND cta_clicks = 0
ORDER BY cta_impressions DESC
LIMIT 25
```

---

## Query 12: CTA ID Analysis (For v1.3.0 Validation)

**Purpose:** Analyze current CTA ID patterns to identify improvement opportunities

```sql
SELECT
    properties.cta_id as cta_id,
    properties.cta_text as cta_text,
    properties.cta_href as cta_href,
    count() as occurrences,
    uniqExact(properties.page_path) as unique_pages
FROM events
WHERE event = 'navboost:cta_click'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY cta_id, cta_text, cta_href
ORDER BY occurrences DESC
LIMIT 50
```

---

## Dashboard Layout Recommendation

```
┌─────────────────────────────────────────────────────────────────┐
│  CTA PERFORMANCE DASHBOARD                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Impressions │  │   Clicks    │  │  Overall    │  │ Unique  │ │
│  │   45,230    │  │   2,156     │  │  CTR: 4.8%  │  │ CTAs: 89│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Daily CTA Trend (Line Chart - Query 10)                    │ │
│  │  [Chart: impressions, clicks, CTR over 7 days]              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────┐  ┌───────────────────────────────┐ │
│  │  CTA by Type (Query 2)   │  │  Top CTAs by CTR (Query 4)    │ │
│  │  [Bar chart by cta_type] │  │  [Table: text, href, CTR]     │ │
│  └──────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Affiliate Performance   │  │  Outbound Destinations        │ │
│  │  (Query 6)               │  │  (Query 7)                    │ │
│  └──────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  CTA Performance by URL (Query 3)                           │ │
│  │  [Table: page_url, impressions, clicks, ctr]                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────┐  ┌───────────────────────────────┐ │
│  │  Zero-Click Pages        │  │  Bottom Performers            │ │
│  │  (Query 11)              │  │  (Query 5)                    │ │
│  └──────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### Creating Dashboard in PostHog

1. Go to PostHog → Dashboards → New Dashboard
2. Name: "CTA Performance Analysis"
3. Add insights using the HogQL queries above
4. Set refresh interval: 1 hour
5. Share with team

### Filters to Add

- **Domain filter:** `properties.$host = 'domain.com'`
- **Date range:** Adjustable (default 7 days)
- **CTA type filter:** Dropdown for cta_type
- **Device filter:** `properties.device_type`

---

*Generated by W-DASH (BI Developer) | WhiteTeam | WT-2026-007*
