# PostHog Conversion Funnel Templates

**Project:** PostHog NavBoost Integration
**Document:** Pre-Built Funnel Configurations
**Version:** 1.0.0
**Created:** 2026-02-03
**Author:** W-DASH (BI Developer)

---

## Overview

This document provides ready-to-use funnel configurations for PostHog. Each funnel is designed to answer specific business questions about user conversion paths.

---

## Funnel 1: Landing → CTA → Affiliate Conversion

**Purpose:** Track the complete affiliate conversion journey

**Business Question:** "What percentage of visitors who land on our pages end up clicking an affiliate link?"

### Configuration

```json
{
    "name": "Affiliate Conversion Funnel",
    "steps": [
        {
            "event": "$pageview",
            "name": "Page View",
            "properties": {}
        },
        {
            "event": "navboost:cta_visible",
            "name": "CTA Seen",
            "properties": {}
        },
        {
            "event": "navboost:cta_click",
            "name": "CTA Clicked",
            "properties": {}
        },
        {
            "event": "navboost:outbound_click",
            "name": "Affiliate Click",
            "properties": {
                "is_affiliate": true
            }
        }
    ],
    "conversion_window_days": 1,
    "breakdown": "properties.$pathname"
}
```

### HogQL Equivalent

```sql
-- Affiliate Conversion Funnel
WITH funnel_data AS (
    SELECT
        distinct_id,
        properties.$session_id as session_id,
        min(CASE WHEN event = '$pageview' THEN timestamp END) as step1_time,
        min(CASE WHEN event = 'navboost:cta_visible' THEN timestamp END) as step2_time,
        min(CASE WHEN event = 'navboost:cta_click' THEN timestamp END) as step3_time,
        min(CASE WHEN event = 'navboost:outbound_click' AND properties.is_affiliate = true THEN timestamp END) as step4_time
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY distinct_id, session_id
)
SELECT
    count(CASE WHEN step1_time IS NOT NULL THEN 1 END) as step1_pageview,
    count(CASE WHEN step2_time IS NOT NULL AND step2_time > step1_time THEN 1 END) as step2_cta_seen,
    count(CASE WHEN step3_time IS NOT NULL AND step3_time > step2_time THEN 1 END) as step3_cta_click,
    count(CASE WHEN step4_time IS NOT NULL AND step4_time > step3_time THEN 1 END) as step4_affiliate,
    round(count(CASE WHEN step4_time IS NOT NULL THEN 1 END) * 100.0 /
          nullIf(count(CASE WHEN step1_time IS NOT NULL THEN 1 END), 0), 2) as overall_conversion_rate
FROM funnel_data
```

### Expected Benchmarks

| Step | Conversion Rate | Target |
|------|-----------------|--------|
| Pageview → CTA Seen | 60-80% | > 70% |
| CTA Seen → CTA Click | 3-8% | > 5% |
| CTA Click → Affiliate | 50-80% | > 60% |
| **Overall** | 1-4% | > 2% |

---

## Funnel 2: Article Engagement Funnel

**Purpose:** Track content consumption depth

**Business Question:** "How many visitors actually read our articles vs. bounce?"

### Configuration

```json
{
    "name": "Article Engagement Funnel",
    "steps": [
        {
            "event": "$pageview",
            "name": "Article View",
            "properties": {
                "$pathname": {"regex": "^/\\d{4}/|/news/|/article/"}
            }
        },
        {
            "event": "navboost:scroll_zone",
            "name": "Scrolled to 25%",
            "properties": {
                "scroll_depth_percent": 25
            }
        },
        {
            "event": "navboost:scroll_zone",
            "name": "Scrolled to 50%",
            "properties": {
                "scroll_depth_percent": 50
            }
        },
        {
            "event": "navboost:scroll_zone",
            "name": "Scrolled to 75%",
            "properties": {
                "scroll_depth_percent": 75
            }
        },
        {
            "event": "conversion:content_consumed",
            "name": "Content Consumed (90%+)",
            "properties": {}
        }
    ],
    "conversion_window_days": 1
}
```

### HogQL Equivalent

```sql
-- Article Engagement Funnel
SELECT
    count(CASE WHEN event = '$pageview' THEN 1 END) as step1_view,
    count(CASE WHEN event = 'navboost:scroll_zone' AND properties.scroll_depth_percent = 25 THEN 1 END) as step2_25pct,
    count(CASE WHEN event = 'navboost:scroll_zone' AND properties.scroll_depth_percent = 50 THEN 1 END) as step3_50pct,
    count(CASE WHEN event = 'navboost:scroll_zone' AND properties.scroll_depth_percent = 75 THEN 1 END) as step4_75pct,
    count(CASE WHEN event = 'conversion:content_consumed' THEN 1 END) as step5_consumed,
    round(count(CASE WHEN event = 'conversion:content_consumed' THEN 1 END) * 100.0 /
          nullIf(count(CASE WHEN event = '$pageview' THEN 1 END), 0), 2) as completion_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Expected Benchmarks

| Step | Conversion Rate | Target |
|------|-----------------|--------|
| View → 25% Scroll | 70-90% | > 80% |
| 25% → 50% Scroll | 50-70% | > 60% |
| 50% → 75% Scroll | 40-60% | > 50% |
| 75% → Consumed | 60-80% | > 70% |
| **Overall Completion** | 20-40% | > 30% |

---

## Funnel 3: Newsletter Signup Funnel

**Purpose:** Track newsletter conversion

**Business Question:** "What's our newsletter signup conversion rate?"

### Configuration

```json
{
    "name": "Newsletter Signup Funnel",
    "steps": [
        {
            "event": "$pageview",
            "name": "Page View"
        },
        {
            "event": "navboost:cta_visible",
            "name": "Newsletter Form Seen",
            "properties": {
                "cta_type": "newsletter"
            }
        },
        {
            "event": "navboost:cta_click",
            "name": "Newsletter Interaction",
            "properties": {
                "cta_type": "newsletter"
            }
        },
        {
            "event": "conversion:newsletter_signup",
            "name": "Newsletter Submitted"
        }
    ],
    "conversion_window_days": 7
}
```

### HogQL Equivalent

```sql
-- Newsletter Signup Funnel
SELECT
    count(DISTINCT CASE WHEN event = '$pageview' THEN properties.$session_id END) as sessions,
    count(CASE WHEN event = 'navboost:cta_visible' AND properties.cta_type = 'newsletter' THEN 1 END) as form_visible,
    count(CASE WHEN event = 'navboost:cta_click' AND properties.cta_type = 'newsletter' THEN 1 END) as form_interaction,
    count(CASE WHEN event = 'conversion:newsletter_signup' THEN 1 END) as signups,
    round(count(CASE WHEN event = 'conversion:newsletter_signup' THEN 1 END) * 100.0 /
          nullIf(count(DISTINCT CASE WHEN event = '$pageview' THEN properties.$session_id END), 0), 2) as signup_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Expected Benchmarks

| Step | Conversion Rate | Target |
|------|-----------------|--------|
| Session → Form Seen | 30-50% | > 40% |
| Form Seen → Interaction | 5-15% | > 10% |
| Interaction → Signup | 30-60% | > 40% |
| **Overall** | 0.5-3% | > 1% |

---

## Funnel 4: CTA Effectiveness Funnel

**Purpose:** Measure CTA-to-conversion journey

**Business Question:** "How effective are our CTAs at driving outbound clicks?"

### Configuration

```json
{
    "name": "CTA Effectiveness Funnel",
    "steps": [
        {
            "event": "navboost:cta_visible",
            "name": "CTA Viewed"
        },
        {
            "event": "navboost:cta_click",
            "name": "CTA Clicked"
        },
        {
            "event": "navboost:outbound_click",
            "name": "Outbound Click"
        }
    ],
    "breakdown": "properties.cta_type",
    "conversion_window_days": 1
}
```

### HogQL by CTA Type

```sql
-- CTA Effectiveness by Type
SELECT
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as visible,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicked,
    round(count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
          nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0), 2) as ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY cta_type
ORDER BY visible DESC
```

---

## Funnel 5: Google Traffic → Engagement Funnel

**Purpose:** Track Google visitor engagement quality

**Business Question:** "Are Google visitors engaging or bouncing?"

### Configuration

```json
{
    "name": "Google Traffic Engagement",
    "steps": [
        {
            "event": "navboost:session_start",
            "name": "Google Session Start",
            "properties": {
                "is_google_referrer": true
            }
        },
        {
            "event": "navboost:scroll_zone",
            "name": "Scrolled Past Fold",
            "properties": {
                "scroll_depth_percent": {"gte": 25}
            }
        },
        {
            "event": "navboost:cta_visible",
            "name": "Saw CTA"
        },
        {
            "event": "navboost:session_end",
            "name": "Non-Pogo Exit",
            "properties": {
                "is_pogo": false
            }
        }
    ],
    "conversion_window_days": 1
}
```

### HogQL Equivalent

```sql
-- Google Traffic Quality Funnel
SELECT
    count(CASE WHEN event = 'navboost:session_start' AND properties.is_google_referrer = true THEN 1 END) as google_sessions,
    count(CASE WHEN event = 'navboost:scroll_zone' AND properties.scroll_depth_percent >= 25 THEN 1 END) as scrolled,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as saw_cta,
    count(CASE WHEN event = 'navboost:session_end' AND properties.is_pogo = false AND properties.is_google_referrer = true THEN 1 END) as engaged_exits,
    round(
        count(CASE WHEN event = 'navboost:session_end' AND properties.is_pogo = false AND properties.is_google_referrer = true THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:session_start' AND properties.is_google_referrer = true THEN 1 END), 0)
    , 2) as engagement_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Expected Benchmarks

| Metric | Target |
|--------|--------|
| Non-Pogo Rate | > 80% |
| Scroll Engagement | > 60% |
| CTA Visibility | > 50% |

---

## Funnel 6: Page-Specific Conversion Funnel

**Purpose:** Track conversion for a specific high-value page

**Business Question:** "How well does /best-casinos/ convert?"

### HogQL (Customizable)

```sql
-- Page-Specific Funnel (replace pathname)
WITH page_sessions AS (
    SELECT DISTINCT properties.$session_id as session_id
    FROM events
    WHERE event = '$pageview'
    AND properties.$pathname = '/best-casinos/'
    AND timestamp >= now() - INTERVAL 7 DAY
)
SELECT
    count(DISTINCT ps.session_id) as page_sessions,
    count(CASE WHEN e.event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
    count(CASE WHEN e.event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    count(CASE WHEN e.event = 'navboost:outbound_click' AND e.properties.is_affiliate = true THEN 1 END) as affiliate_clicks,
    round(
        count(CASE WHEN e.event = 'navboost:outbound_click' AND e.properties.is_affiliate = true THEN 1 END) * 100.0 /
        nullIf(count(DISTINCT ps.session_id), 0)
    , 2) as page_conversion_rate
FROM page_sessions ps
LEFT JOIN events e ON e.properties.$session_id = ps.session_id
WHERE e.timestamp >= now() - INTERVAL 7 DAY
```

---

## Implementation Guide

### Creating Funnels in PostHog UI

1. Go to **PostHog** → **Insights** → **New Insight**
2. Select **Funnels** from the visualization type
3. Add steps using the configurations above
4. Set **Conversion Window** (typically 1 day for same-session)
5. Add **Breakdowns** as needed (by URL, device, etc.)
6. Save to dashboard

### Funnel Filters

| Filter | Use Case |
|--------|----------|
| `properties.$host = 'domain.com'` | Single domain analysis |
| `properties.device_type = 'mobile'` | Mobile-specific funnel |
| `properties.is_google_referrer = true` | Google traffic only |
| `properties.page_template = 'article'` | Article pages only |

### Breakdowns

| Breakdown | Use Case |
|-----------|----------|
| `properties.$pathname` | Per-page performance |
| `properties.cta_type` | CTA type comparison |
| `properties.$referring_domain` | Traffic source comparison |
| `properties.device_type` | Device comparison |

---

## Funnel Optimization Tips

### Low Step 1 → Step 2 Conversion

**Problem:** Users see page but don't scroll/engage
**Solutions:**
- Improve above-the-fold content
- Reduce page load time (check LCP)
- Make CTA more prominent

### Low CTA Visible → CTA Click

**Problem:** CTAs are seen but not clicked
**Solutions:**
- Improve CTA copy (test variations)
- Make CTA more visually prominent
- Check CTA placement (use heatmaps)

### Low CTA Click → Outbound

**Problem:** Clicked CTA but didn't follow through
**Solutions:**
- Check for broken links
- Verify landing page quality
- Ensure trust signals present

---

## Scheduled Reports

### Weekly Funnel Summary

```sql
-- Weekly Funnel Performance Summary
SELECT
    'Affiliate Funnel' as funnel,
    count(CASE WHEN event = '$pageview' THEN 1 END) as step1,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as step3,
    count(CASE WHEN event = 'navboost:outbound_click' AND properties.is_affiliate = true THEN 1 END) as step4,
    round(
        count(CASE WHEN event = 'navboost:outbound_click' AND properties.is_affiliate = true THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = '$pageview' THEN 1 END), 0)
    , 2) as conversion_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY

UNION ALL

SELECT
    'Content Consumption' as funnel,
    count(CASE WHEN event = '$pageview' THEN 1 END) as step1,
    count(CASE WHEN event = 'navboost:scroll_zone' AND properties.scroll_depth_percent = 50 THEN 1 END) as step3,
    count(CASE WHEN event = 'conversion:content_consumed' THEN 1 END) as step4,
    round(
        count(CASE WHEN event = 'conversion:content_consumed' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = '$pageview' THEN 1 END), 0)
    , 2) as conversion_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

---

*Generated by W-DASH (BI Developer) | WhiteTeam | WT-2026-007*
