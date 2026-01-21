# PostHog + NavBoost Setup - pokerology.com

**Setup Date:** 2026-01-20
**Project:** BT-2026-002-NB (NavBoost Implementation)
**Platform:** WordPress
**Site Type:** Affiliate/Casino (Poker)
**Project ID:** 294549

---

## Quick Start

### 1. Install PostHog Base Tracking

Add the following to your theme's `functions.php`:

```php
// Include the PostHog functions
require_once get_stylesheet_directory() . '/inc/posthog-functions.php';
```

Or copy the contents of `posthog-functions.php` directly into your `functions.php`.

### 2. Install NavBoost Tracker

1. Copy `navboost-tracker.js` to your theme's `/js/` directory
2. The tracker is automatically enqueued by the functions.php code

### 3. Verify Installation

Open browser console and run:
```javascript
// Check PostHog is loaded
posthog.get_distinct_id()

// Check NavBoost is loaded (after page interaction)
getNavBoostMetrics()
```

---

## Files Included

| File | Purpose |
|------|---------|
| `posthog-functions.php` | WordPress integration code for functions.php |
| `navboost-tracker.js` | NavBoost engagement tracking module |
| `dashboard-queries.sql` | HogQL queries for PostHog dashboards |
| `cohorts-funnels.json` | Cohort definitions and funnel configurations |
| `HOP_REVIEW_CONFIG.md` | Head of Product review document |
| `README.md` | This file |

---

## Events Tracked

### Base PostHog Events (Automatic)
- `$pageview` - Page views
- `$pageleave` - Page exits with scroll data
- `$web_vitals` - LCP, CLS, INP metrics
- `$autocapture` - Click tracking

### NavBoost Events (Custom)
| Event | Description |
|-------|-------------|
| `navboost:session_start` | Session initialization with referrer data |
| `navboost:session_end` | Session end with dwell time, pogo detection |
| `navboost:scroll_zone` | Scroll depth milestones (25%, 50%, 75%, 100%) |
| `navboost:cta_visible` | CTA enters viewport |
| `navboost:cta_click` | CTA clicked |
| `navboost:outbound_click` | External/affiliate link clicked |
| `navboost:toplist_row_visible` | Poker room toplist row visible |

---

## NavBoost Targets

| Metric | Target | Current |
|--------|--------|---------|
| Pogo Rate | < 18% | TBD |
| CTA Zone Reach (50%) | > 70% | TBD |
| Below Fold Reach (75%) | > 40% | TBD |
| Average Dwell Time | > 90s | TBD |
| CTA CTR | > 5% | TBD |
| Good Abandonment | > 15% | TBD |
| Engagement Score | > 70 | TBD |

---

## Dashboard Setup

1. Go to PostHog → Dashboards → New Dashboard
2. Name: "pokerology.com - NavBoost Metrics"
3. Add insights using queries from `dashboard-queries.sql`

### Recommended Dashboard Layout

**Row 1: Core Metrics**
- Engagement Score (Query #10)
- Pogo Rate (Query #1)
- Average Dwell Time (Query #2)

**Row 2: Scroll & CTA**
- Scroll Depth Distribution (Query #3)
- CTA Performance (Query #4)
- Good Abandonment Rate (Query #5)

**Row 3: Poker/Affiliate Specific**
- Top Affiliate Destinations (Query #7)
- Toplist Row Visibility (Query #8)
- Affiliate Clicks by Template (Query #6)

**Row 4: Trends**
- Daily NavBoost Trend (Query #11)
- Device Breakdown (Query #13)

---

## Cohorts to Create

Create these cohorts in PostHog for segmentation:

1. **Google Organic Users** - SEO traffic analysis
2. **High Engagement Users** - Quality visitors
3. **Pogo Users** - Users to reduce
4. **Affiliate Clickers** - Conversion tracking
5. **Review Page Visitors** - Content type analysis
6. **Comparison Page Visitors** - High-intent users

See `cohorts-funnels.json` for full definitions.

---

## Funnels to Create

1. **Google → CTA Zone → Affiliate Click** (Primary conversion)
2. **Landing → CTA Visibility → Click** (CTA effectiveness)
3. **Scroll Depth Progression** (Content engagement)
4. **Toplist Engagement Funnel** (Poker room discovery)
5. **Review Page Conversion** (Review effectiveness)

---

## CTA Selectors (Poker/Affiliate)

The following selectors are tracked as CTAs:

```css
/* Affiliate Links */
.affiliate-link, .casino-link, .poker-room-link
.bonus-btn, .bonus-link, .play-now, .visit-site
.claim-bonus, .get-bonus

/* Tracking Patterns */
a[rel="sponsored"], a[href*="/go/"], a[href*="/out/"]
a[href*="/redirect/"], a[href*="?ref="]

/* Toplist Items */
.toplist-item a, .poker-room-row a, .ranking-item a

/* Poker Specific */
.poker-bonus, .rakeback-link, .freeroll-link
```

---

## Head of Product Review

Before deployment, Head of Product must review and approve:

1. CTA selectors (completeness)
2. Engagement score weights
3. Pogo threshold (8s standard)
4. Dwell time benchmarks
5. Page template classification

See `HOP_REVIEW_CONFIG.md` for review checklist.

---

## Testing Checklist

- [ ] PostHog loads on all pages
- [ ] `navboost:session_start` fires on page load
- [ ] `navboost:scroll_zone` fires at 25%, 50%, 75%, 100%
- [ ] `navboost:cta_visible` fires when CTAs enter viewport
- [ ] `navboost:cta_click` fires on CTA clicks
- [ ] `navboost:outbound_click` fires on affiliate links
- [ ] `navboost:session_end` fires on page exit
- [ ] Google referrer detection works
- [ ] Pogo detection works (< 8s exits)
- [ ] Good abandonment detection works

---

## Support

**Project:** BT-2026-002 (PostHog Analytics Platform Migration)
**Sub-project:** BT-2026-002-NB (NavBoost Implementation)
**Owner:** BlackTeam - Paradise Media Group

**Related Commands:**
- `/posthog_analysis pokerology.com` - Generate analytics report
- `/posthog_setup` - Setup documentation

---

*Generated by BlackTeam PostHog Setup*
*Director Rule 8: Head of Product mandatory for all PostHog projects*
