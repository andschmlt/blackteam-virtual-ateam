# NavBoost + PostHog Integration - esports.gg

**PostHog Project ID:** 291582
**Site Type:** Esports/Gaming News
**GitHub Repo:** ParadiseMediaOrg/esports.gg
**Generated:** 2026-01-21

## Overview

This package contains everything needed to deploy NavBoost engagement tracking for esports.gg. NavBoost tracks user engagement signals that correlate with Google's ranking system.

## Files Included

| File | Purpose |
|------|---------
| `navboost-tracker.js` | Frontend JavaScript tracker (deploy to theme) |
| `posthog-functions.php` | WordPress integration code |
| `dashboard-queries.sql` | PostHog HogQL queries for dashboard |
| `cohorts-funnels.json` | Cohort and funnel definitions for PostHog |
| `RELEASE_NOTES.md` | Deployment release notes |

## Installation Steps

### Step 1: Deploy NavBoost Tracker

Copy `navboost-tracker.js` to your theme's JS directory:

```bash
# Clone repo and add file
git clone git@github.com:ParadiseMediaOrg/esports.gg.git
cp navboost-tracker.js esportsgg/wp-content/themes/[your-theme]/js/
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
Description: PostHog + NavBoost tracking for esports.gg
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
2. Select project: esports.gg (291582)
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

## Key Metrics & Targets (Esports/Gaming News)

| Metric | Target | Critical |
|--------|--------|----------|
| Pogo Rate | < 15% | > 20% |
| Dwell Time | > 90s | < 45s |
| Scroll Depth (50%+) | > 50% | < 30% |
| CTA CTR | > 5% | < 2% |
| Good Abandonment | > 15% | < 8% |
| Engagement Score | > 70 | < 55 |

## Support

- PostHog Docs: https://posthog.com/docs
- NavBoost Framework: See NAVBOOST_KPI_FRAMEWORK.md
- Contact: Virtual ATeam - Head of Product

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-21 | Initial release |
