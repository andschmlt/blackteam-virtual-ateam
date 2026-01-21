# Deployment Guide - godisageek.com Conversion Tracking

**Generated:** January 21, 2026
**PostHog Project ID:** 295222

---

## Quick Deployment (Recommended)

### Option 1: Code Snippets Plugin (Easiest)

1. Install "Code Snippets" plugin in WordPress
2. Add new snippet → Run in Header
3. Paste this code:

```html
<!-- PostHog + NavBoost + Conversion Tracking -->
<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('phc_LAFbPCUQJXmQ0KpWjasr1VdddjGFdlzQFyHVjVW6iMB',{api_host:'https://us.i.posthog.com',capture_pageview:true,capture_pageleave:true,autocapture:true});
</script>
<script src="https://raw.githubusercontent.com/ParadiseMediaOrg/posthog-trackers/main/godisageek_com/navboost-tracker.min.js"></script>
<script src="https://raw.githubusercontent.com/ParadiseMediaOrg/posthog-trackers/main/godisageek_com/conversion-tracker.min.js"></script>
```

### Option 2: Theme functions.php

Add to your theme's `functions.php`:

```php
// Copy contents of posthog-full-tracking.php here
```

### Option 3: Custom Plugin

1. Create folder: `/wp-content/plugins/posthog-tracking/`
2. Create file: `posthog-tracking.php`
3. Copy `posthog-full-tracking.php` contents
4. Add plugin header at top
5. Activate plugin

---

## Conversion Events Created

| Conversion Type | Event Name | Trigger | Value |
|-----------------|------------|---------|-------|
| **Newsletter Signup** | `conversion:newsletter_signup` | Form submit on newsletter forms | 5 |
| **Ad Click** | `conversion:ad_click` | Click on ad units | 1 |
| **Affiliate Click** | `conversion:affiliate_click` | Click on affiliate links | 3-10 |
| **Article Completion** | `conversion:article_completion` | Scroll 90%+ on article | 2 |
| **Return Visit** | `conversion:return_visit` | Visitor returns after 24h | 1-3 |

---

## PostHog Dashboard Queries

### Overall Conversion Rate

```sql
SELECT
    count(DISTINCT CASE WHEN event LIKE 'conversion:%' THEN properties.$session_id END) as converting_sessions,
    count(DISTINCT properties.$session_id) as total_sessions,
    round(count(DISTINCT CASE WHEN event LIKE 'conversion:%' THEN properties.$session_id END) * 100.0 /
          nullIf(count(DISTINCT properties.$session_id), 0), 2) as conversion_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Conversion by Type

```sql
SELECT
    properties.conversion_type as type,
    count() as conversions,
    uniqExact(distinct_id) as unique_users
FROM events
WHERE event = '$conversion'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY type
ORDER BY conversions DESC
```

### Newsletter Conversion Rate

```sql
SELECT
    count(CASE WHEN event = 'conversion:newsletter_signup' THEN 1 END) as signups,
    count(CASE WHEN event = 'newsletter:email_focus' THEN 1 END) as email_focus,
    count(DISTINCT properties.$session_id) as total_sessions,
    round(count(CASE WHEN event = 'conversion:newsletter_signup' THEN 1 END) * 100.0 /
          nullIf(count(DISTINCT properties.$session_id), 0), 2) as signup_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Affiliate Conversion Performance

```sql
SELECT
    properties.affiliate_domain as domain,
    properties.affiliate_category as category,
    count() as clicks,
    sum(properties.value) as total_value
FROM events
WHERE event = 'conversion:affiliate_click'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY domain, category
ORDER BY clicks DESC
```

### Article Completion Rate

```sql
SELECT
    count(CASE WHEN event = 'article:article_started' THEN 1 END) as started,
    count(CASE WHEN event = 'article:article_engaged' THEN 1 END) as engaged,
    count(CASE WHEN event = 'article:article_consumed' THEN 1 END) as consumed,
    count(CASE WHEN event = 'conversion:article_completion' THEN 1 END) as completed,
    round(count(CASE WHEN event = 'conversion:article_completion' THEN 1 END) * 100.0 /
          nullIf(count(CASE WHEN event = 'article:article_started' THEN 1 END), 0), 2) as completion_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
```

### Return Visitor Value

```sql
SELECT
    properties.visit_number as visit,
    count() as visitors,
    avg(properties.value) as avg_value
FROM events
WHERE event = 'conversion:return_visit'
AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY visit
ORDER BY visit
```

---

## Expected Events After Deployment

Once deployed, you should see these events in PostHog:

### NavBoost Events
- `navboost:session_start`
- `navboost:scroll_zone`
- `navboost:cta_visible`
- `navboost:cta_click`
- `navboost:outbound_click`
- `navboost:session_end`

### Conversion Events
- `conversion:newsletter_signup`
- `conversion:ad_click`
- `conversion:affiliate_click`
- `conversion:article_completion`
- `conversion:return_visit`
- `$conversion` (generic, for funnels)

### Progress Events
- `newsletter:email_focus`
- `ad:impression`
- `article:article_started`
- `article:article_engaged`
- `article:article_consumed`
- `conversion:session_summary`

---

## Verification Steps

1. **Deploy code** to godisageek.com
2. **Open browser DevTools** → Console
3. **Look for logs:**
   - `[PostHog] Loaded for godisageek.com`
   - `[NavBoost] Session started`
   - `[ConversionTracker] Enhanced Conversion Tracker fully initialized`
4. **Check PostHog Live Events** → Should see events flowing
5. **Test conversions:**
   - Scroll to bottom of article → Should see `article:article_completed`
   - Click affiliate link → Should see `conversion:affiliate_click`
   - Submit newsletter form → Should see `conversion:newsletter_signup`

---

## Troubleshooting

### Events not appearing
1. Check browser console for errors
2. Verify PostHog API key is correct
3. Check if ad blockers are blocking PostHog

### Conversions not tracking
1. Verify form selectors match your actual forms
2. Check if links have expected affiliate patterns
3. Enable DEBUG mode in tracker

### Low conversion rates
1. This is expected initially - baseline is being established
2. Check that conversion elements exist on pages
3. Verify visitors are reaching conversion points

---

## Files Reference

| File | Purpose |
|------|---------|
| `navboost-tracker.js` | NavBoost KPI tracking |
| `conversion-tracker.js` | 5 conversion types |
| `posthog-full-tracking.php` | WordPress integration |
| `DEPLOYMENT_GUIDE.md` | This document |

---

*Generated by Virtual ATeam - Head of Product + Tech Lead*
