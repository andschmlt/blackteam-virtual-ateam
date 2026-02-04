# Business Questions Framework v1.0

**Version:** 1.0 | **Date:** 2026-02-04 | **Status:** DRAFT - PENDING APPROVAL | **Owner:** Andre

---

## Overview

This framework maps 106 business questions to data sources, query patterns, and calculations. It serves as the authoritative reference for Pitaya, BI-Chatbot, and all Virtual ATeam agents.

**MANDATORY:** All queries MUST comply with MASTER_LIST v1.0 governance rules.

---

## IMPORTANT: Use bi.reporting Schema ONLY

**Per MASTER_LIST v1.0 Rule R7:** Use `paradisemedia-bi.reporting` ONLY

**FORBIDDEN:** `bi_playground`, `lakehouse`, `analytics`, `testing` schemas

### Approved Tables (10 Core Tables)

| Table | Rows | Primary Use |
|-------|------|-------------|
| **ARTICLE_PERFORMANCE** | 6.9M | Revenue, FTDs, clicks, conversions per article |
| **ARTICLE_INFORMATION** | 52K | Article metadata, status, keywords, vertical |
| **BRAND_PERFORMANCE** | 320K | Brand-level metrics (high-level overview) |
| **COSTS_INFORMATION** | 150K | Costs by type, domain, article |
| **FINANCIAL_REPORT** | 1M | High-level financials (Voonix - THE BIBLE) |
| **CLOAKING_TRAFFIC** | 12M | Clickout/redirect data, broken links |
| **REPT_SEO_AHREFS** | 5M | DR, backlinks, referring domains |
| **REPT_SEO_ACCURANKER** | 6M | Rankings, positions, traffic |
| **ARTICLE_CHANGELOG** | 210K | Production cycles, TAT |
| **DIM_* tables** | Various | Dimensions (DATE, BRAND, VERTICAL, FIXED_FEE, PRODUCT) |

### Critical Join Rules

```sql
-- Article-level joins (MANDATORY)
ARTICLE_INFORMATION.TASK_ID = ARTICLE_PERFORMANCE.DYNAMIC

-- Fixed fees (Rule R12)
COSTS_INFORMATION.SOURCE = 'FIXED_FEES'
COSTS_INFORMATION.LINK_FK = DIM_FIXED_FEE.FIXED_FEE_SK

-- Date format (Rule R6)
DATE_ID = YYYYMMDD (integer, e.g., 20260204)
```

### Bot Suite (for operational use, not authoritative reporting)

| Bot | Port | Use Case |
|-----|------|----------|
| **Kumquat** | 8000 | Quick commission alerts |
| **Pomelo** | 3003 | Domain monitoring dashboards |
| **Apple** | 5050 | PDF report generation |

**Note:** Bots may use `bi_playground` views for speed, but authoritative answers MUST come from `reporting` schema.

---

## Data Source Reference

| Code | Source | Tables/Endpoints | Purpose |
|------|--------|------------------|---------|
| **BQ-AP** | BigQuery | `reporting.ARTICLE_PERFORMANCE` | Revenue, FTDs, clicks, conversions per article |
| **BQ-AI** | BigQuery | `reporting.ARTICLE_INFORMATION` | Article metadata, status, keywords, vertical |
| **BQ-BP** | BigQuery | `reporting.BRAND_PERFORMANCE` | Brand-level metrics |
| **BQ-CI** | BigQuery | `reporting.COSTS_INFORMATION` | Costs by type, domain, article |
| **BQ-FR** | BigQuery | `reporting.FINANCIAL_REPORT` | High-level financial (Voonix) |
| **BQ-CT** | BigQuery | `reporting.CLOAKING_TRAFFIC` | Clickout/redirect data |
| **BQ-AH** | BigQuery | `reporting.REPT_SEO_AHREFS` | DR, backlinks, referring domains |
| **BQ-AR** | BigQuery | `reporting.REPT_SEO_ACCURANKER` | Rankings, positions, traffic |
| **BQ-AC** | BigQuery | `reporting.ARTICLE_CHANGELOG` | Production cycles, TAT |
| **BQ-DV** | BigQuery | `reporting.DIM_VERTICAL` | Vertical/Niche hierarchy |
| **BQ-DB** | BigQuery | `reporting.DIM_BRAND` | Brand dimension |
| **BQ-DD** | BigQuery | `reporting.DIM_DATE` | Date dimension |
| **BQ-FF** | BigQuery | `reporting.DIM_FIXED_FEE` | Fixed fee agreements |
| **PH** | PostHog | Events API | User behavior, engagement, CTAs |
| **DF** | DataForSEO | Various endpoints | Live SEO data, rankings, backlinks |
| **CU** | ClickUp | Tasks API | Task management, status, comments |
| **MANUAL** | Manual Input | N/A | Requires manual data entry |
| **EXTERNAL** | External Tool | Varies | Ahrefs UI, Google Search Console, etc. |

---

## Category 1: Performance & Revenue (4 Questions)

### Q1.1: What are the top 5% of revenue-generating articles, programs, brands, or verticals?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI, BQ-BP, BQ-FR |
| **Availability** | FULL |
| **Query Pattern** | Percentile calculation with GROUP BY entity type |

**SQL Pattern:**
```sql
-- Top 5% Articles by Revenue
WITH ranked AS (
  SELECT
    ai.TASK_ID,
    ai.LIVE_URL,
    SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
    PERCENT_RANK() OVER (ORDER BY SUM(ap.TOTAL_COMMISSION_USD)) as pct_rank
  FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
  JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
  WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
  GROUP BY ai.TASK_ID, ai.LIVE_URL
)
SELECT * FROM ranked WHERE pct_rank >= 0.95 ORDER BY REVENUE DESC;

-- Top 5% Programs by Revenue (use FINANCIAL_REPORT)
SELECT PROGRAM, SUM(TOTAL_COMMISSION_USD) as REVENUE
FROM `paradisemedia-bi.reporting.FINANCIAL_REPORT`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY PROGRAM
QUALIFY PERCENT_RANK() OVER (ORDER BY SUM(TOTAL_COMMISSION_USD)) >= 0.95;

-- Top 5% Brands by Revenue
SELECT BRAND, SUM(TOTAL_COMMISSION_USD) as REVENUE
FROM `paradisemedia-bi.reporting.BRAND_PERFORMANCE`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY BRAND
QUALIFY PERCENT_RANK() OVER (ORDER BY SUM(TOTAL_COMMISSION_USD)) >= 0.95;

-- Top 5% Verticals by Revenue
SELECT ai.VERTICAL, SUM(ap.TOTAL_COMMISSION_USD) as REVENUE
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.VERTICAL
QUALIFY PERCENT_RANK() OVER (ORDER BY SUM(ap.TOTAL_COMMISSION_USD)) >= 0.95;
```

---

### Q1.2: What's the average EPC and/or EPF by vertical/brand/article?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI, BQ-BP |
| **Availability** | FULL |
| **Calculations** | EPC = TOTAL_COMMISSION_USD / CLICKS, EPF = TOTAL_COMMISSION_USD / GOALS |

**SQL Pattern:**
```sql
-- Average EPC/EPF by Vertical
SELECT
  ai.VERTICAL,
  SUM(ap.TOTAL_COMMISSION_USD) / NULLIF(SUM(ap.CLICKS), 0) as AVG_EPC,
  SUM(ap.TOTAL_COMMISSION_USD) / NULLIF(SUM(ap.GOALS), 0) as AVG_EPF
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.VERTICAL;

-- Average EPC/EPF by Brand
SELECT
  bp.BRAND,
  SUM(bp.TOTAL_COMMISSION_USD) / NULLIF(SUM(bp.CLICKS), 0) as AVG_EPC,
  SUM(bp.TOTAL_COMMISSION_USD) / NULLIF(SUM(bp.FTD), 0) as AVG_EPF
FROM `paradisemedia-bi.reporting.BRAND_PERFORMANCE` bp
WHERE bp.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY bp.BRAND;

-- Average EPC/EPF by Article
SELECT
  ai.TASK_ID,
  ai.LIVE_URL,
  SUM(ap.TOTAL_COMMISSION_USD) / NULLIF(SUM(ap.CLICKS), 0) as EPC,
  SUM(ap.TOTAL_COMMISSION_USD) / NULLIF(SUM(ap.GOALS), 0) as EPF
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.TASK_ID, ai.LIVE_URL;
```

---

### Q1.3: Which traffic sources are converting best?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH (PostHog), BQ-AP |
| **Availability** | PARTIAL - PostHog for traffic source, BigQuery for conversions |
| **Gap** | Need to link PostHog traffic source with BigQuery conversions (session attribution) |

**Notes:**
- PostHog tracks `navboost:session_start` with `utm_source`, `utm_medium`, `referrer`
- BigQuery ARTICLE_PERFORMANCE tracks conversions but NOT traffic source
- **RECOMMENDATION:** Build attribution model linking PostHog sessions to BQ conversions via URL matching

**PostHog Query:**
```sql
-- Traffic sources from PostHog (HogQL)
SELECT
  properties.$referring_domain as traffic_source,
  COUNT(DISTINCT session_id) as sessions,
  SUM(CASE WHEN event = 'navboost:outbound_click' THEN 1 ELSE 0 END) as affiliate_clicks
FROM events
WHERE event = 'navboost:session_start'
  AND timestamp >= {start_date}
GROUP BY traffic_source
ORDER BY sessions DESC;
```

**Data Gap:** No direct join between PostHog traffic source and BigQuery FTDs/revenue.

---

### Q1.4: What is the ROI per traffic channel or campaign? (Net Profit/Loss per article)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-CI, BQ-FF |
| **Availability** | FULL for article-level ROI |
| **Calculations** | ROI = (Revenue - Costs) / Costs |

**SQL Pattern:**
```sql
-- ROI per Article
WITH revenue AS (
  SELECT
    ai.TASK_ID,
    ai.LIVE_URL,
    ai.DOMAIN,
    SUM(ap.TOTAL_COMMISSION_USD) as COMMISSION
  FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
  LEFT JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
  WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
  GROUP BY ai.TASK_ID, ai.LIVE_URL, ai.DOMAIN
),
costs AS (
  SELECT
    DYNAMIC as TASK_ID,
    SUM(COST_USD) as TOTAL_COSTS
  FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
  WHERE DATE_ID BETWEEN {start_date} AND {end_date}
  GROUP BY DYNAMIC
),
fixed_fees AS (
  SELECT
    ci.DYNAMIC as TASK_ID,
    SUM(dff.FIXED_FEE_USD) as FIXED_FEES
  FROM `paradisemedia-bi.reporting.COSTS_INFORMATION` ci
  JOIN `paradisemedia-bi.reporting.DIM_FIXED_FEE` dff ON ci.LINK_FK = dff.FIXED_FEE_SK
  WHERE ci.SOURCE = 'FIXED_FEES'
  GROUP BY ci.DYNAMIC
)
SELECT
  r.TASK_ID,
  r.LIVE_URL,
  r.DOMAIN,
  r.COMMISSION,
  COALESCE(f.FIXED_FEES, 0) as FIXED_FEE_REVENUE,
  r.COMMISSION + COALESCE(f.FIXED_FEES, 0) as TOTAL_REVENUE,
  COALESCE(c.TOTAL_COSTS, 0) as TOTAL_COSTS,
  (r.COMMISSION + COALESCE(f.FIXED_FEES, 0)) - COALESCE(c.TOTAL_COSTS, 0) as NET_PROFIT,
  CASE WHEN COALESCE(c.TOTAL_COSTS, 0) > 0
    THEN ((r.COMMISSION + COALESCE(f.FIXED_FEES, 0)) - COALESCE(c.TOTAL_COSTS, 0)) / c.TOTAL_COSTS
    ELSE NULL END as ROI
FROM revenue r
LEFT JOIN costs c ON r.TASK_ID = c.TASK_ID
LEFT JOIN fixed_fees f ON r.TASK_ID = f.TASK_ID
ORDER BY NET_PROFIT DESC;
```

**Note for Traffic Channel ROI:** Requires PostHog-to-BigQuery attribution (see Q1.3 gap).

---

## Category 2: Content & SEO (4 Questions)

### Q2.1: Which articles get the most organic traffic but no conversions? (CVR, CTR and Clicks to Conversions)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AR (rankings/traffic), BQ-AP (conversions), PH (CTR) |
| **Availability** | PARTIAL - Ahrefs has traffic estimates, BQ has conversions, CTR needs PostHog |

**SQL Pattern:**
```sql
-- High traffic, low conversion articles
WITH traffic AS (
  SELECT
    DOMAIN,
    SUM(ORGANIC_TRAFFIC) as EST_TRAFFIC
  FROM `paradisemedia-bi.reporting.REPT_SEO_AHREFS`
  WHERE DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.reporting.REPT_SEO_AHREFS`)
  GROUP BY DOMAIN
),
conversions AS (
  SELECT
    ai.DOMAIN,
    SUM(ap.CLICKS) as TOTAL_CLICKS,
    SUM(ap.SIGNUPS) as TOTAL_SIGNUPS,
    SUM(ap.GOALS) as TOTAL_FTDS,
    SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
    SAFE_DIVIDE(SUM(ap.GOALS), SUM(ap.CLICKS)) as CVR
  FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
  JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
  WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
  GROUP BY ai.DOMAIN
)
SELECT
  t.DOMAIN,
  t.EST_TRAFFIC,
  c.TOTAL_CLICKS,
  c.TOTAL_FTDS,
  c.CVR,
  c.REVENUE
FROM traffic t
LEFT JOIN conversions c ON t.DOMAIN = c.DOMAIN
WHERE c.TOTAL_FTDS = 0 OR c.TOTAL_FTDS IS NULL
ORDER BY t.EST_TRAFFIC DESC;
```

**PostHog CTR Query:**
```sql
-- CTR by page (HogQL)
SELECT
  properties.$pathname as page,
  COUNT(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
  COUNT(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
  SAFE_DIVIDE(COUNT(CASE WHEN event = 'navboost:cta_click' THEN 1 END),
              COUNT(CASE WHEN event = 'navboost:cta_visible' THEN 1 END)) as CTR
FROM events
WHERE timestamp >= {start_date}
GROUP BY page;
```

---

### Q2.2: What keywords are driving the highest-converting traffic?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI (Target Keywords), BQ-AP (Conversions), DF (Live rankings) |
| **Availability** | PARTIAL - Target keywords in BQ, live rankings from DataForSEO |
| **Gap** | Keywords from DataForSEO CANNOT be linked to revenue (Rule R21) |

**Important:** Per MASTER_LIST rule R21, DataForSEO keywords cannot be linked to revenue data. Use Target Keywords from ARTICLE_INFORMATION instead.

**SQL Pattern:**
```sql
-- Keywords by conversion (using TARGET_KEYWORDS from article info)
SELECT
  ai.TARGET_KEYWORDS,
  ai.LIVE_URL,
  SUM(ap.CLICKS) as CLICKS,
  SUM(ap.GOALS) as FTDS,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
  SAFE_DIVIDE(SUM(ap.GOALS), SUM(ap.CLICKS)) as CVR
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
  AND ai.TARGET_KEYWORDS IS NOT NULL
GROUP BY ai.TARGET_KEYWORDS, ai.LIVE_URL
ORDER BY REVENUE DESC;
```

---

### Q2.3: Which affiliate links have low CTR despite high visibility?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH (CTA visibility, clicks), BQ-CT (cloaking traffic) |
| **Availability** | FULL via PostHog |

**PostHog Query:**
```sql
-- Low CTR affiliate links (HogQL)
SELECT
  properties.cta_id as affiliate_link,
  properties.$pathname as page,
  COUNT(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
  COUNT(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
  SAFE_DIVIDE(
    COUNT(CASE WHEN event = 'navboost:cta_click' THEN 1 END),
    COUNT(CASE WHEN event = 'navboost:cta_visible' THEN 1 END)
  ) as CTR
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
  AND timestamp >= {start_date}
GROUP BY affiliate_link, page
HAVING impressions > 100 AND CTR < 0.01
ORDER BY impressions DESC;
```

---

### Q2.4: What content formats perform best across verticals?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI, BQ-AP, MANUAL |
| **Availability** | PARTIAL - No "content format" field in BQ |
| **Gap** | Need to add CONTENT_FORMAT field to ARTICLE_INFORMATION |

**Workaround:** Infer format from URL patterns or task name:
- `/best-*` = Listicle
- `/review-*` = Review
- `/guide-*` = Guide
- `/how-to-*` = How-To

**SQL Pattern (inference based):**
```sql
-- Content format performance (inferred)
SELECT
  CASE
    WHEN LOWER(ai.LIVE_URL) LIKE '%best%' OR LOWER(ai.TASK_NAME) LIKE '%best%' THEN 'Listicle'
    WHEN LOWER(ai.LIVE_URL) LIKE '%review%' OR LOWER(ai.TASK_NAME) LIKE '%review%' THEN 'Review'
    WHEN LOWER(ai.LIVE_URL) LIKE '%guide%' OR LOWER(ai.TASK_NAME) LIKE '%guide%' THEN 'Guide'
    WHEN LOWER(ai.LIVE_URL) LIKE '%how-to%' OR LOWER(ai.TASK_NAME) LIKE '%how%' THEN 'How-To'
    ELSE 'Other'
  END as CONTENT_FORMAT,
  ai.VERTICAL,
  COUNT(DISTINCT ai.TASK_ID) as ARTICLE_COUNT,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
  AVG(ap.TOTAL_COMMISSION_USD) as AVG_REVENUE_PER_ARTICLE
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY CONTENT_FORMAT, ai.VERTICAL
ORDER BY REVENUE DESC;
```

**RECOMMENDATION:** Add CONTENT_FORMAT field to ARTICLE_INFORMATION for accurate tracking.

---

## Category 3: Affiliate Partner & Program (3 Questions)

### Q3.1: Which affiliate programs provide the highest net margin?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-FR, BQ-BP |
| **Availability** | PARTIAL - Commission data available, payout terms may need manual entry |
| **Note** | "Net margin" requires knowing payout structure per program |

**SQL Pattern:**
```sql
-- Program performance (commission = net since we receive net)
SELECT
  PROGRAM,
  SUM(TOTAL_COMMISSION_USD) as TOTAL_COMMISSION,
  COUNT(DISTINCT BRAND) as BRAND_COUNT,
  SUM(TOTAL_COMMISSION_USD) / COUNT(DISTINCT BRAND) as AVG_PER_BRAND
FROM `paradisemedia-bi.reporting.FINANCIAL_REPORT`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY PROGRAM
ORDER BY TOTAL_COMMISSION DESC;
```

---

### Q3.2: Are there underperforming programs with better alternatives?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-FR, BQ-BP, EXTERNAL |
| **Availability** | PARTIAL - Internal performance available, alternatives need market research |
| **Gap** | No competitor program data in system |

**SQL Pattern (internal analysis):**
```sql
-- Underperforming programs (low commission, low growth)
WITH program_perf AS (
  SELECT
    PROGRAM,
    SUM(CASE WHEN DATE_ID BETWEEN {prev_start} AND {prev_end} THEN TOTAL_COMMISSION_USD ELSE 0 END) as PREV_PERIOD,
    SUM(CASE WHEN DATE_ID BETWEEN {curr_start} AND {curr_end} THEN TOTAL_COMMISSION_USD ELSE 0 END) as CURR_PERIOD
  FROM `paradisemedia-bi.reporting.FINANCIAL_REPORT`
  GROUP BY PROGRAM
)
SELECT
  PROGRAM,
  PREV_PERIOD,
  CURR_PERIOD,
  SAFE_DIVIDE(CURR_PERIOD - PREV_PERIOD, PREV_PERIOD) as GROWTH_RATE
FROM program_perf
WHERE CURR_PERIOD < PREV_PERIOD  -- Declining programs
ORDER BY GROWTH_RATE ASC;
```

**RECOMMENDATION:** Add market research for alternative programs (manual/external).

---

### Q3.3: How often are program terms/payouts updated?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | MANUAL, CU |
| **Availability** | NOT AVAILABLE - No automated tracking |
| **Gap** | Need to track program term changes |

**RECOMMENDATION:** Create ClickUp tracking for program term updates or add tracking table in BQ.

---

## Category 4: Traffic & User Behavior (3 Questions)

### Q4.1: Where is most of the traffic coming from by geography and device?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH, BQ-AI (geo targeting) |
| **Availability** | FULL via PostHog |

**PostHog Query:**
```sql
-- Traffic by geography and device (HogQL)
SELECT
  properties.$geoip_country_name as country,
  properties.$device_type as device,
  COUNT(DISTINCT session_id) as sessions
FROM events
WHERE event = 'navboost:session_start'
  AND timestamp >= {start_date}
GROUP BY country, device
ORDER BY sessions DESC;
```

---

### Q4.2: Which referral sources have the highest engagement?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH |
| **Availability** | FULL via PostHog |

**PostHog Query:**
```sql
-- Referral source engagement (HogQL)
SELECT
  properties.$referring_domain as referrer,
  COUNT(DISTINCT session_id) as sessions,
  AVG(properties.dwell_time) as avg_dwell_time,
  AVG(properties.max_scroll_depth) as avg_scroll_depth,
  COUNT(CASE WHEN event = 'navboost:outbound_click' THEN 1 END) as affiliate_clicks,
  SAFE_DIVIDE(
    COUNT(CASE WHEN event = 'navboost:outbound_click' THEN 1 END),
    COUNT(DISTINCT session_id)
  ) as click_rate
FROM events
WHERE timestamp >= {start_date}
GROUP BY referrer
HAVING sessions > 100
ORDER BY affiliate_clicks DESC;
```

---

### Q4.3: Are mobile users converting at the same rate as desktop?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH, BQ-AP |
| **Availability** | PARTIAL - PostHog has device, BQ has conversions, no direct link |

**PostHog Query:**
```sql
-- Conversion proxy by device (using affiliate clicks as proxy)
SELECT
  properties.$device_type as device,
  COUNT(DISTINCT session_id) as sessions,
  COUNT(CASE WHEN event = 'navboost:outbound_click' THEN 1 END) as affiliate_clicks,
  SAFE_DIVIDE(
    COUNT(CASE WHEN event = 'navboost:outbound_click' THEN 1 END),
    COUNT(DISTINCT session_id)
  ) as click_rate
FROM events
WHERE timestamp >= {start_date}
GROUP BY device;
```

**Data Gap:** Full conversion tracking (FTDs) not available by device - only affiliate clicks as proxy.

---

## Category 5: Compliance, Legal & Risk (3 Questions)

### Q5.1: Are we following all local affiliate disclosure and ad regulations?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | MANUAL, EXTERNAL |
| **Availability** | NOT AVAILABLE - Requires manual compliance audit |
| **Gap** | No automated compliance tracking |

**RECOMMENDATION:** Create compliance checklist in ClickUp, track by geo/vertical.

---

### Q5.2: Is there a risk of being de-indexed for specific verticals?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | DF (site audit), EXTERNAL (GSC) |
| **Availability** | PARTIAL - DataForSEO site audit, Google Search Console for manual actions |

**DataForSEO Endpoint:** `/v3/on_page/instant_pages` for technical issues

**Manual Check Required:** Google Search Console for manual actions, penalties.

---

### Q5.3: Are cookie tracking durations long enough for our user journey?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | MANUAL, PH |
| **Availability** | PARTIAL - PostHog can measure session duration |

**PostHog Query:**
```sql
-- User journey duration (session to conversion)
SELECT
  properties.$pathname as landing_page,
  PERCENTILE_CONT(properties.session_duration, 0.5) as median_session_duration,
  PERCENTILE_CONT(properties.session_duration, 0.9) as p90_session_duration
FROM events
WHERE event = 'navboost:session_end'
  AND timestamp >= {start_date}
GROUP BY landing_page;
```

**Note:** Cookie duration tracking requires affiliate program documentation (30/60/90 day cookies).

---

## Category 6: Strategic/Operational (4 Questions)

### Q6.1: Are we diversifying enough across verticals to avoid overdependence?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI, BQ-FR |
| **Availability** | FULL |

**SQL Pattern:**
```sql
-- Revenue diversification by vertical
SELECT
  ai.VERTICAL,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
  SUM(ap.TOTAL_COMMISSION_USD) * 100.0 / SUM(SUM(ap.TOTAL_COMMISSION_USD)) OVER () as PCT_OF_TOTAL
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.VERTICAL
ORDER BY REVENUE DESC;
```

**Interpretation:** If any vertical > 50%, consider diversification.

---

### Q6.2: What's the % revenue distribution by niche—are we overweight anywhere?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI, BQ-DV |
| **Availability** | FULL |

**SQL Pattern:**
```sql
-- Revenue distribution by niche
SELECT
  ai.VERTICAL,
  ai.NICHE,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
  SUM(ap.TOTAL_COMMISSION_USD) * 100.0 / SUM(SUM(ap.TOTAL_COMMISSION_USD)) OVER () as PCT_OF_TOTAL
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.VERTICAL, ai.NICHE
ORDER BY REVENUE DESC;
```

---

### Q6.3: What's the % revenue distribution by Program—are we overweight anywhere?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-FR |
| **Availability** | FULL |

**SQL Pattern:**
```sql
-- Revenue distribution by program
SELECT
  PROGRAM,
  SUM(TOTAL_COMMISSION_USD) as REVENUE,
  SUM(TOTAL_COMMISSION_USD) * 100.0 / SUM(SUM(TOTAL_COMMISSION_USD)) OVER () as PCT_OF_TOTAL
FROM `paradisemedia-bi.reporting.FINANCIAL_REPORT`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY PROGRAM
ORDER BY REVENUE DESC;
```

---

### Q6.4: What processes are in place for updating or removing underperforming content?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | CU, MANUAL |
| **Availability** | PARTIAL - ClickUp tracks task status |
| **Gap** | No automated underperformer identification trigger |

**RECOMMENDATION:** Create automated alert for articles with 0 FTDs after X days.

---

## Category 7: Vertical-Specific (12 Questions)

### Q7.1: Which games or betting types convert best by region? (iGaming)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | PARTIAL - No "game type" or "betting type" field |
| **Gap** | Need GAME_TYPE or BETTING_TYPE field |

**Workaround:** Infer from brand or URL patterns.

---

### Q7.2: Are there regulatory changes affecting iGaming partners?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | EXTERNAL, MANUAL |
| **Availability** | NOT AVAILABLE - Requires manual research |

---

### Q7.3: Which health conditions/topics convert best? (Health)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | PARTIAL - Use SUB_NICHE for health topics |

**SQL Pattern:**
```sql
SELECT ai.SUB_NICHE, SUM(ap.TOTAL_COMMISSION_USD) as REVENUE
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ai.VERTICAL = 'Health' AND ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.SUB_NICHE ORDER BY REVENUE DESC;
```

---

### Q7.4: Are there seasonal spikes in demand (e.g. weight loss in Jan)?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI, BQ-DD |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  FORMAT_DATE('%B', PARSE_DATE('%Y%m%d', CAST(ap.DATE_ID AS STRING))) as MONTH,
  ai.SUB_NICHE,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ai.VERTICAL = 'Health' AND ap.DATE_ID >= 20250101
GROUP BY MONTH, ai.SUB_NICHE
ORDER BY MONTH, REVENUE DESC;
```

---

### Q7.5: Which financial tools or calculators lead to the most conversions? (Finance)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | PARTIAL - No "tool type" field |
| **Gap** | Need TOOL_TYPE field or URL pattern matching |

---

### Q7.6: What's the trust factor or bounce rate for financial product reviews?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | PH |
| **Availability** | FULL via PostHog (pogo rate = bounce proxy) |

---

### Q7.7: Which B2B services bring recurring commissions? (B2B)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-FR |
| **Availability** | PARTIAL - Commission data available, recurring vs one-time not tracked |
| **Gap** | Need COMMISSION_TYPE (recurring/one-time) field |

---

### Q7.8: Which industries or business sizes convert best? (B2B)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI |
| **Availability** | PARTIAL - No industry or business size tracking |

---

### Q7.9: Are there legal risks in content about psychedelics or nootropics?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | EXTERNAL, MANUAL |
| **Availability** | NOT AVAILABLE - Requires legal review |

---

### Q7.10: Which product types (supplements, guides, etc.) perform best?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | PARTIAL - Use SUB_NICHE or URL pattern matching |

---

### Q7.11: What adult content types (cams, clips, etc.) monetize better? (Adult)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | PARTIAL - Use SUB_NICHE for adult content types |

---

### Q7.12: Are we flagged or filtered in ad platforms or SEO for adult content?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | EXTERNAL, MANUAL |
| **Availability** | NOT AVAILABLE - Requires manual platform checks |

---

## Category 8: Content Performance (4 Questions)

### Q8.1: Number of new posts

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI, BQ-AC |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  COUNT(*) as NEW_POSTS,
  FORMAT_DATE('%Y-%m', PARSE_DATE('%Y%m%d', CAST(MIN(DATE_ID) AS STRING))) as MONTH
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION`
WHERE STATUS = 'LIVE'
  AND DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY MONTH;
```

---

### Q8.2: Content costs

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  TYPE,
  SUM(COST_USD) as TOTAL_COST
FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
WHERE TYPE IN ('CONTENT', 'WRITER', 'EDITOR')
  AND DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY TYPE;
```

---

### Q8.3: SP Cost (Service Provider Cost)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT SUM(COST_USD) as SP_COST
FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
WHERE TYPE = 'SP'
  AND DATE_ID BETWEEN {start_date} AND {end_date};
```

---

### Q8.4: SP Cost per post

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CI, BQ-AI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
WITH sp_costs AS (
  SELECT SUM(COST_USD) as TOTAL_SP_COST
  FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
  WHERE TYPE = 'SP' AND DATE_ID BETWEEN {start_date} AND {end_date}
),
post_count AS (
  SELECT COUNT(*) as NEW_POSTS
  FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION`
  WHERE STATUS = 'LIVE' AND DATE_ID BETWEEN {start_date} AND {end_date}
)
SELECT sp.TOTAL_SP_COST / pc.NEW_POSTS as SP_COST_PER_POST
FROM sp_costs sp, post_count pc;
```

---

## Category 9: Revenue & Conversion (6 Questions)

### Q9.1: Revenue

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-FR, BQ-FF |
| **Availability** | FULL |
| **Formula** | Total Revenue = Commission + Fixed Fees |

---

### Q9.2: Revenue per post

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-AI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  SUM(ap.TOTAL_COMMISSION_USD) / COUNT(DISTINCT ai.TASK_ID) as REVENUE_PER_POST
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date};
```

---

### Q9.3: Affiliate link clicks

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-CT, PH |
| **Availability** | FULL |

---

### Q9.4: Revenue per click

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP |
| **Availability** | FULL |
| **Formula** | EPC = TOTAL_COMMISSION_USD / CLICKS |

---

### Q9.5: Revenue per order (Per Conversion or Goal)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP |
| **Availability** | FULL |
| **Formula** | EPF = TOTAL_COMMISSION_USD / GOALS |

---

### Q9.6: CVR (Conversion Rate)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP |
| **Availability** | FULL |
| **Formula** | CVR = GOALS / CLICKS |

---

## Category 10: Site Operations (3 Questions)

### Q10.1: Cloaking site downtime (incidents per month)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | MANUAL, CU |
| **Availability** | NOT AVAILABLE - No automated uptime monitoring in BQ |
| **Gap** | Need uptime monitoring integration |

---

### Q10.2: Cloaking links broken or with issues (incidents per month)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CT |
| **Availability** | PARTIAL - Can detect 404s in cloaking traffic |

**SQL Pattern:**
```sql
SELECT
  COUNT(*) as BROKEN_LINKS,
  FORMAT_DATE('%Y-%m', PARSE_DATE('%Y%m%d', CAST(DATE_ID AS STRING))) as MONTH
FROM `paradisemedia-bi.reporting.CLOAKING_TRAFFIC`
WHERE STATUS_CODE = 404
  AND DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY MONTH;
```

---

### Q10.3: OO site downtime (incidents per month)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | MANUAL |
| **Availability** | NOT AVAILABLE - No uptime monitoring |

---

## Category 11: SEO Performance (9 Questions)

### Q11.1: Ahrefs Traffic Value

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AH |
| **Availability** | FULL |

---

### Q11.2: Ahrefs Traffic

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AH |
| **Availability** | FULL |

---

### Q11.3-Q11.8: Number of new posts in top 10/3/1, Top X Hit %

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AR |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  COUNT(CASE WHEN POSITION <= 10 THEN 1 END) as TOP_10,
  COUNT(CASE WHEN POSITION <= 3 THEN 1 END) as TOP_3,
  COUNT(CASE WHEN POSITION = 1 THEN 1 END) as TOP_1,
  COUNT(*) as TOTAL_KEYWORDS,
  COUNT(CASE WHEN POSITION <= 10 THEN 1 END) * 100.0 / COUNT(*) as TOP_10_HIT_PCT,
  COUNT(CASE WHEN POSITION <= 3 THEN 1 END) * 100.0 / COUNT(*) as TOP_3_HIT_PCT,
  COUNT(CASE WHEN POSITION = 1 THEN 1 END) * 100.0 / COUNT(*) as TOP_1_HIT_PCT
FROM `paradisemedia-bi.reporting.REPT_SEO_ACCURANKER`
WHERE DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.reporting.REPT_SEO_ACCURANKER`);
```

---

## Category 12: Testing & ROI (14 Questions)

### Q12.1-Q12.6: Testing metrics (Top positions, Hit %)

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AR, BQ-AP |
| **Availability** | FULL |

---

### Q12.7-Q12.9: Break even %, 3X ROI %, 10X ROI %

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AP, BQ-CI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
WITH article_roi AS (
  SELECT
    ai.TASK_ID,
    SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
    SUM(ci.COST_USD) as COSTS
  FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
  LEFT JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap ON ai.TASK_ID = ap.DYNAMIC
  LEFT JOIN `paradisemedia-bi.reporting.COSTS_INFORMATION` ci ON ai.TASK_ID = ci.DYNAMIC
  WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
  GROUP BY ai.TASK_ID
)
SELECT
  COUNT(CASE WHEN REVENUE >= COSTS THEN 1 END) * 100.0 / COUNT(*) as BREAK_EVEN_PCT,
  COUNT(CASE WHEN REVENUE >= COSTS * 3 THEN 1 END) * 100.0 / COUNT(*) as THREE_X_ROI_PCT,
  COUNT(CASE WHEN REVENUE >= COSTS * 10 THEN 1 END) * 100.0 / COUNT(*) as TEN_X_ROI_PCT
FROM article_roi;
```

---

### Q12.10: Rank #1 for Premium Keywords

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AR, BQ-AI |
| **Availability** | PARTIAL - Need "premium keyword" flag |
| **Gap** | Need KEYWORD_TIER field (premium/standard/long-tail) |

---

## Category 13: Backlinks (5 Questions)

### Q13.1: Total number of backlinks built

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AH, BQ-CI |
| **Availability** | FULL |

---

### Q13.2-Q13.4: Number of GP/PBN/SP links built

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CI |
| **Availability** | PARTIAL - Depends on cost TYPE classification |

---

### Q13.5: Backlink spend

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-CI |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT SUM(COST_USD) as BACKLINK_SPEND
FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
WHERE TYPE IN ('GP', 'PBN', 'SP', 'BACKLINK')
  AND DATE_ID BETWEEN {start_date} AND {end_date};
```

---

## Category 14: Deals & Outreach (27 Questions)

### Q14.1-Q14.27: Deals & Outreach metrics

| Attribute | Value |
|-----------|-------|
| **Data Sources** | CU, MANUAL |
| **Availability** | PARTIAL - ClickUp tracks deals, some metrics need manual entry |

**Available via ClickUp:**
- Number of Leads (task count in Leads list)
- Sites contacted (tasks with "contacted" status)
- Deals closed (tasks with "closed" status)

**Manual Entry Required:**
- Emails sent
- Success rates
- Acquisition costs
- Migration metrics
- Profitability periods

**RECOMMENDATION:** Create custom fields in ClickUp for all deal metrics.

---

## Category 15: Content Production (5 Questions)

### Q15.1: How many articles were published in a period?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI, BQ-AC |
| **Availability** | FULL |

---

### Q15.2: Which team is producing and publishing articles the most in a period?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AI |
| **Availability** | PARTIAL - Depends on CONTENT_TEAM field |

---

### Q15.3: In which production cycle do articles take most time?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AC |
| **Availability** | FULL |

**SQL Pattern:**
```sql
SELECT
  FROM_STATUS,
  TO_STATUS,
  AVG(DAYS_IN_STATUS) as AVG_DAYS
FROM `paradisemedia-bi.reporting.ARTICLE_CHANGELOG`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY FROM_STATUS, TO_STATUS
ORDER BY AVG_DAYS DESC;
```

---

### Q15.4: In which grouped status are articles taking most time?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AC |
| **Availability** | FULL |

---

### Q15.5: How long do articles take from start to published?

| Attribute | Value |
|-----------|-------|
| **Data Sources** | BQ-AC |
| **Availability** | FULL (TAT metrics) |

---

## Questions Mapped to bi.reporting Tables

| Question Category | Primary Table | Secondary Tables |
|-------------------|---------------|------------------|
| **Revenue (article-level)** | ARTICLE_PERFORMANCE | ARTICLE_INFORMATION (for metadata) |
| **Revenue (brand/program)** | FINANCIAL_REPORT | BRAND_PERFORMANCE |
| **FTDs/Conversions** | ARTICLE_PERFORMANCE | (GOALS column = FTDs) |
| **Costs** | COSTS_INFORMATION | DIM_FIXED_FEE, DIM_INVOICE |
| **SEO Authority** | REPT_SEO_AHREFS | (DR, backlinks) |
| **SEO Rankings** | REPT_SEO_ACCURANKER | (positions, traffic) |
| **Production/TAT** | ARTICLE_CHANGELOG | ARTICLE_INFORMATION |
| **Cloaking/Tracking** | CLOAKING_TRAFFIC | (broken links, redirects) |
| **Vertical/Niche** | ARTICLE_INFORMATION | DIM_VERTICAL |
| **User Behavior** | PostHog API | (not in BigQuery) |

### Sample Query Patterns (reporting schema)

**Revenue by Domain:**
```sql
SELECT
  ai.DOMAIN,
  SUM(ap.TOTAL_COMMISSION_USD) as REVENUE,
  SUM(ap.GOALS) as FTDS
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap
  ON ai.TASK_ID = ap.DYNAMIC
WHERE ap.DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY ai.DOMAIN
ORDER BY REVENUE DESC;
```

**Costs by Type:**
```sql
SELECT
  TYPE,
  SUM(COST_USD) as TOTAL_COST
FROM `paradisemedia-bi.reporting.COSTS_INFORMATION`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY TYPE;
```

**SEO Metrics:**
```sql
SELECT
  DOMAIN,
  AVG(DOMAIN_RATING) as AVG_DR,
  SUM(DOMAIN_BACKLINKS) as TOTAL_BACKLINKS
FROM `paradisemedia-bi.reporting.REPT_SEO_AHREFS`
WHERE DATE = (SELECT MAX(DATE) FROM `paradisemedia-bi.reporting.REPT_SEO_AHREFS`)
GROUP BY DOMAIN;
```

---

## Summary: Data Availability Matrix

| Category | Total Questions | FULL | PARTIAL | NOT AVAILABLE |
|----------|-----------------|------|---------|---------------|
| Performance & Revenue | 4 | 3 | 1 | 0 |
| Content & SEO | 4 | 1 | 3 | 0 |
| Affiliate Partner | 3 | 1 | 1 | 1 |
| Traffic & Behavior | 3 | 2 | 1 | 0 |
| Compliance & Risk | 3 | 0 | 1 | 2 |
| Strategic/Operational | 4 | 3 | 1 | 0 |
| Vertical-Specific | 12 | 1 | 7 | 4 |
| Content Performance | 4 | 4 | 0 | 0 |
| Revenue & Conversion | 6 | 6 | 0 | 0 |
| Site Operations | 3 | 0 | 1 | 2 |
| SEO Performance | 9 | 9 | 0 | 0 |
| Testing & ROI | 14 | 12 | 2 | 0 |
| Backlinks | 5 | 3 | 2 | 0 |
| Deals & Outreach | 27 | 0 | 20 | 7 |
| Content Production | 5 | 4 | 1 | 0 |
| **TOTAL** | **106** | **49 (46%)** | **41 (39%)** | **16 (15%)** |

---

## Data Gaps Summary

### High Priority Gaps (Recommended to fix)

| Gap | Questions Affected | Recommendation |
|-----|-------------------|----------------|
| PostHog-to-BigQuery attribution | Q1.3, Q1.4, Q4.3 | Build session-to-conversion attribution model |
| Content format field | Q2.4 | Add CONTENT_FORMAT to ARTICLE_INFORMATION |
| Program term tracking | Q3.3 | Create ClickUp tracking for program terms |
| Commission type (recurring) | Q7.7 | Add COMMISSION_TYPE field |
| Uptime monitoring | Q10.1, Q10.3 | Integrate uptime tool (Pingdom, UptimeRobot) |
| Deals & Outreach CRM | Q14.* | Enhance ClickUp with custom fields |

### Medium Priority Gaps

| Gap | Questions Affected | Recommendation |
|-----|-------------------|----------------|
| Game/betting type | Q7.1 | Add PRODUCT_TYPE field |
| Premium keyword flag | Q12.10 | Add KEYWORD_TIER field |
| Industry/business size | Q7.8 | Add INDUSTRY, COMPANY_SIZE fields |

### Low Priority / Manual Only

| Gap | Questions Affected | Notes |
|-----|-------------------|-------|
| Regulatory tracking | Q7.2, Q7.9 | Requires manual legal research |
| Competitor programs | Q3.2 | Market research needed |
| Platform flags | Q7.12 | Manual platform checks |

---

## Pitaya Routing Keywords

For Pitaya agent routing, use these keywords:

```python
QUESTION_ROUTING = {
    # Performance & Revenue
    "top revenue": "BQ-AP, BQ-FR",
    "top 5%": "BQ-AP, BQ-FR",
    "EPC": "BQ-AP",
    "EPF": "BQ-AP",
    "ROI": "BQ-AP, BQ-CI",
    "net profit": "BQ-AP, BQ-CI, BQ-FF",

    # Content & SEO
    "organic traffic": "BQ-AR, BQ-AH",
    "no conversions": "BQ-AP",
    "CTR": "PH",
    "content format": "BQ-AI",

    # Traffic
    "traffic source": "PH",
    "geography": "PH",
    "device": "PH",
    "mobile": "PH",
    "desktop": "PH",

    # SEO
    "rankings": "BQ-AR",
    "backlinks": "BQ-AH, BQ-CI",
    "DR": "BQ-AH",
    "top 10": "BQ-AR",
    "top 3": "BQ-AR",

    # Production
    "TAT": "BQ-AC",
    "published": "BQ-AI",
    "production cycle": "BQ-AC",

    # Costs
    "costs": "BQ-CI",
    "spend": "BQ-CI",
    "SP cost": "BQ-CI",
}
```

---

## Approval & Audit Log

| Date | Version | Status | Reviewer | Notes |
|------|---------|--------|----------|-------|
| 2026-02-04 | 1.0 | DRAFT | - | Initial framework creation |
| - | - | PENDING | Andre | Awaiting user verification |

---

*Document Location: `/home/andre/.claude/context/BUSINESS_QUESTIONS_FRAMEWORK_v1.0.md`*
*Compliant with: MASTER_LIST v1.0*
*Owner: Andre | Maintained by: Virtual ATeam (B-BOB, W-WOL)*
