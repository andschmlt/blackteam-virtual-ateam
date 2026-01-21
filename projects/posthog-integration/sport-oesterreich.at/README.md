# NavBoost + PostHog Integration - sport-oesterreich.at

**PostHog Project ID:** 295253
**Site Type:** Sports News
**Generated:** 2026-01-21

## Files Included

| File | Purpose |
|------|---------
| `navboost-tracker.js` | Frontend JavaScript tracker |
| `posthog-functions.php` | WordPress integration code |
| `RELEASE_NOTES.md` | Deployment release notes |

## Installation

1. Copy `navboost-tracker.js` to `/wp-content/themes/[theme]/js/`
2. Add code from `posthog-functions.php` to your theme's `functions.php`
3. Clear caches and verify in PostHog Live Events

## Target Metrics (Sports News)

| Metric | Target | Critical |
|--------|--------|----------|
| Pogo Rate | < 20% | > 25% |
| Dwell Time | > 60s | < 30s |
| CTA CTR | > 3% | < 1% |
| Engagement Score | > 65 | < 50 |
