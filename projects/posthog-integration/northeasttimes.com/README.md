# NavBoost + PostHog Integration - northeasttimes.com

**PostHog Project ID:** 290039
**Site Type:** News/Media
**Generated:** 2026-01-21

## Overview

This package contains everything needed to deploy NavBoost engagement tracking for northeasttimes.com. NavBoost tracks user engagement signals that correlate with Google's ranking system.

## Files Included

| File | Purpose |
|------|---------|
| `navboost-tracker.js` | Frontend JavaScript tracker (deploy to theme) |
| `posthog-functions.php` | WordPress integration code |
| `dashboard-queries.sql` | PostHog HogQL queries for dashboard |
| `cohorts-funnels.json` | Cohort and funnel definitions for PostHog |

## Installation Steps

### Step 1: Deploy NavBoost Tracker

Copy `navboost-tracker.js` to your theme's JS directory:

```bash
# Via FTP/SFTP
Upload to: /wp-content/themes/[your-theme]/js/navboost-tracker.js

# Or via WordPress admin
Appearance → Theme File Editor → Create new file in /js/ folder
```

### Step 2: Add WordPress Integration

Add the code from `posthog-functions.php` to your theme:

**Option A: Add to functions.php**
```php
// Add to your theme's functions.php
// Copy contents of posthog-functions.php
```

**Option B: Create a custom plugin**
```php
<?php
/*
Plugin Name: NavBoost PostHog Integration
Description: PostHog + NavBoost tracking for northeasttimes.com
Version: 1.0.0
*/

// Copy contents of posthog-functions.php here
```

### Step 3: Verify Installation

After deployment, verify events are being captured:

1. Open browser DevTools (F12) → Console
2. Visit your site
3. Look for `[NavBoost]` log messages (if DEBUG is enabled)
4. Check PostHog Live Events dashboard

### Step 4: Configure PostHog Dashboard

1. Log into PostHog: https://us.i.posthog.com
2. Select project: northeasttimes.com (290039)
3. Create new Insights using queries from `dashboard-queries.sql`
4. Create Cohorts from `cohorts-funnels.json`
5. Set up Funnels from `cohorts-funnels.json`
6. Configure Alerts from `cohorts-funnels.json`

## Events Tracked

| Event | Description |
|-------|-------------|
| `navboost:session_start` | Session begins with referrer info |
| `navboost:session_end` | Session ends with engagement metrics |
| `navboost:scroll_zone` | User reaches scroll depth milestones (25%, 50%, 75%, 100%) |
| `navboost:cta_visible` | CTA enters viewport |
| `navboost:cta_click` | User clicks CTA |
| `navboost:outbound_click` | User clicks external link |

## Key Metrics & Targets (News/Media)

| Metric | Target | Critical |
|--------|--------|----------|
| Pogo Rate | < 20% | > 25% |
| Dwell Time | > 60s | < 30s |
| Scroll Depth (50%+) | > 40% | < 25% |
| CTA CTR | > 3% | < 1% |
| Good Abandonment | > 10% | < 5% |
| Engagement Score | > 65 | < 50 |

## CTA Selectors Tracked

The tracker monitors these elements for visibility and clicks:

- Newsletter: `.newsletter-signup`, `.subscribe-btn`, `.email-signup`
- Social: `.share-button`, `.social-share`, share links
- Articles: `.read-more`, `.related-article a`, `.latest-news a`
- Comments: `.comment-form`, `.reply-link`
- Generic: `.cta-button`, `.btn-primary`, `button[type="submit"]`

## Troubleshooting

### Events not appearing in PostHog

1. Check browser console for errors
2. Verify PostHog API key is correct in `posthog-functions.php`
3. Ensure scripts are loading (Network tab → filter "posthog")
4. Check for ad blockers (may block PostHog)

### Pogo rate too high

1. Check page load speed (target < 3s)
2. Review above-fold content (is it engaging?)
3. Check mobile experience separately
4. Analyze pogo rate by page template

### Low scroll depth

1. Check content length vs. quality
2. Review internal linking
3. Check for engagement barriers (popups, ads)

## Support

- PostHog Docs: https://posthog.com/docs
- NavBoost Framework: See NAVBOOST_KPI_FRAMEWORK.md
- Contact: Virtual ATeam - Head of Product

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-21 | Initial release |
