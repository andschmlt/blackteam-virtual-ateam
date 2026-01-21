# NavBoost + PostHog Integration - pokertube.com

**PostHog Project ID:** 295249
**Site Type:** Gaming/Poker
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

## Target Metrics (Gaming/Poker)

| Metric | Target | Critical |
|--------|--------|----------|
| Pogo Rate | < 12% | > 17% |
| Dwell Time | > 120s | < 60s |
| CTA CTR | > 8% | < 4% |
| Engagement Score | > 75 | < 60 |
