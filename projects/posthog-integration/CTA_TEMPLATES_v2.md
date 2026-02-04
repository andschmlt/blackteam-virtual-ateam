# NavBoost CTA Selector Templates v2.0

**Project:** PostHog NavBoost Integration
**Maintained by:** Virtual ATeam - BlackTeam (B-RANK + B-FORG)
**Created:** 2026-01-28
**Last Updated:** 2026-02-04
**Version:** 2.0.0

---

## Purpose

This document provides REFINED CTA selector templates to fix tracking issues identified in the PostHog Diagnostic Report (2026-02-03). Version 2.0 addresses:

- **False positives** - Overly broad selectors catching non-CTA elements
- **Missing CTAs** - Important affiliate/action links not being detected
- **Low engagement** - Selectors targeting decorative elements instead of actionable CTAs

---

## Change Summary (v1.0 to v2.0)

| Template | Issue | Fix Applied |
|----------|-------|-------------|
| CTA_TEMPLATE_003 (hudsonreporter.com) | 220k visible, 3 clicks - too broad | Added EXCLUSION list, narrowed to actual CTAs |
| CTA_TEMPLATE_004 (dotesports.com) | 14k visible, 3 clicks - generic | Focused on affiliate promo boxes only |
| CTA_TEMPLATE_005 (europeangaming.eu) | 0 visible - no detection | Added B2B iGaming news selectors |
| CTA_TEMPLATE_002 (culture.org) | 791 visible, 0 clicks | Refined to engagement-driving CTAs |

---

## CTA_TEMPLATE_003_v2: Newspaper Theme (hudsonreporter.com)

**Domain:** hudsonreporter.com
**Theme:** tagDiv Newspaper (Newspaper-HR variant)
**Issue:** 220,066 CTA visible but only 3 clicks - generic news theme selectors catching metadata, bylines, tags, and decorative elements as CTAs.

### Root Cause Analysis

The v1.0 template included selectors like:
- `.td-post-category` - Catches category labels (non-actionable)
- `.td-tags a` - Catches all tag links (low-value)
- `.td-author-name a` - Catches author bylines (not CTAs)
- `.td-module-meta-info a` - Catches timestamps and metadata

These elements are visible on every article but are NOT primary CTAs.

### v2.0 INCLUSION Selectors (Use These)

```javascript
CTA_SELECTORS: [
    // PRIORITY 1: Affiliate Links (if present)
    'a[href*="/go/"]',
    'a[href*="/out/"]',
    'a[href*="/visit/"]',
    'a[href*="?ref="]',
    'a[href*="affiliate"]',
    'a[rel="sponsored"]',
    'a[rel="nofollow"][target="_blank"][href^="http"]',

    // PRIORITY 2: Newsletter Signups (HIGH VALUE)
    '.td-newsletter input[type="submit"]',
    '.td_block_newsletter button',
    '.td_block_newsletter input[type="submit"]',
    '#mc4wp-form-1 input[type="submit"]',
    'form.mc4wp-form button[type="submit"]',
    '.newsletter-form button',
    '.newsletter-signup-btn',

    // PRIORITY 3: Social Sharing (Article-specific only)
    '.td-post-sharing-top a',
    '.td-post-sharing-bottom a',
    '.td-post-sharing a[data-action="share"]',
    'a.td-social-sharing-button',

    // PRIORITY 4: Content Engagement (Limited scope)
    '.td-read-more a',
    'a.more-link',
    '.td-post-next-prev a.td-post-next',
    '.td-post-next-prev a.td-post-prev',

    // PRIORITY 5: Search (User intent signal)
    '.td-header-search-wrap button',
    'form.tdb-search-form button[type="submit"]',
    '.search-submit'
]
```

### v2.0 EXCLUSION Selectors (Filter These Out)

```javascript
CTA_EXCLUSIONS: [
    // Meta elements (NOT actionable CTAs)
    '.td-post-category',
    '.td-module-meta-info a',
    '.td-post-author-name a',
    '.td-author-name a',
    '.entry-category a',

    // Tag clouds and taxonomies
    '.td-tags a',
    '.tagcloud a',
    '.td-post-tags a',

    // Breadcrumbs and navigation
    '.entry-crumbs a',
    '.td-crumb-container a',
    '.td-header-menu-wrap a',
    'nav a',

    // Footer links (site navigation, not CTAs)
    '.td-footer-wrapper a',
    '.td-sub-footer-copy a',

    // Related posts in sidebar (low intent)
    '.td-related-span4 a',
    '.widget_popular_post a',
    '.widget_recent_entries a',

    // Ad containers (tracked separately)
    '.td-adspot-title a',
    '.google-auto-placed a',
    '.adsbygoogle a',

    // Social profile links (not sharing actions)
    '.td-social-icon-wrap a',
    '.td-header-social-wrap a'
]
```

### Affiliate URL Patterns to Detect

```javascript
AFFILIATE_PATTERNS: [
    // Standard affiliate paths
    /\/go\/[a-zA-Z0-9-]+\/?$/,
    /\/out\/[a-zA-Z0-9-]+\/?$/,
    /\/visit\/[a-zA-Z0-9-]+\/?$/,

    // Query-based tracking
    /\?ref=[a-zA-Z0-9-]+/,
    /\?aff=[a-zA-Z0-9-]+/,
    /\?partner=[a-zA-Z0-9-]+/,

    // Common affiliate networks
    /shareasale\.com/,
    /impact\.com/,
    /cj\.com/,
    /linksynergy\.com/
]
```

### Expected Outcome

| Metric | Before (v1.0) | After (v2.0) |
|--------|---------------|--------------|
| CTA Visible | 220,066 | ~5,000-10,000 |
| False Positive Rate | ~99.9% | <10% |
| Expected CTR | 0.001% | 2-5% |

---

## CTA_TEMPLATE_004_v2: GAMURS/Esports Theme (dotesports.com)

**Domain:** dotesports.com
**Theme:** GAMURS WordPress Blocks
**Issue:** 14,630 CTA visible, only 3 clicks - span elements and generic blocks being captured instead of actual affiliate CTAs.

### Root Cause Analysis

The v1.0 template included:
- `.wp-block-gamurs-icon` - Catches all icons (decorative)
- `a[rel="nofollow noreferrer"]` - Too broad, catches all external links
- `.wp-block-gamurs-article-tile__link` - Catches related article tiles (low-value)

The CTA IDs show `span__p3ys`, `span__asv4` - indicating span elements are being tracked, not buttons.

### v2.0 INCLUSION Selectors (Use These)

```javascript
CTA_SELECTORS: [
    // PRIORITY 1: Paradise Media Affiliate System (HIGHEST VALUE)
    '.pm-promo-code-container a',
    '.pm-play-now',
    '.pm-play-now-link',
    'a.pm-play-now',
    '.pm-review a.pm-visit-site',
    '.pm-cta-button',
    '.pm-bonus-claim',

    // PRIORITY 2: Affiliate link patterns
    'a[href*="/go/"]',
    'a[href*="/out/"]',
    'a[href*="/aff/"]',
    'a[href*="track."]',
    'a[href*="record."]',
    'a[rel="sponsored"]',

    // PRIORITY 3: Gaming-specific CTAs
    'a[href*="store.steampowered.com"]',
    'a[href*="play.google.com"]',
    'a[href*="apps.apple.com"]',
    'a[href*="epicgames.com/store"]',
    'a[href*="gog.com/game"]',

    // PRIORITY 4: Sportsbook/Casino affiliate links
    'a[href*="draftkings.com"]',
    'a[href*="fanduel.com"]',
    'a[href*="betmgm.com"]',
    'a[href*="bet365.com"]',
    'a[href*="caesars.com"]',

    // PRIORITY 5: Social Sharing (article actions only)
    'a[data-share-type="twitter"]',
    'a[data-share-type="facebook"]',
    'a[data-share-type="reddit"]',
    'button[data-action="share"]',

    // PRIORITY 6: Newsletter/Subscribe
    'form.newsletter button[type="submit"]',
    '.newsletter-cta button',
    '.email-capture button'
]
```

### v2.0 EXCLUSION Selectors (Filter These Out)

```javascript
CTA_EXCLUSIONS: [
    // Icon elements (decorative only)
    '.wp-block-gamurs-icon',
    'span.icon',
    'i.icon',
    'svg.icon',

    // Article tiles (internal navigation, not CTAs)
    '.wp-block-gamurs-article-tile__link',
    '.article-tile a',
    '.related-article a',

    // Navigation elements
    '.wp-block-gamurs-nav a',
    'header a',
    'nav a',
    '.breadcrumb a',

    // Footer links
    'footer a',
    '.site-footer a',

    // Author/meta info
    '.author-info a',
    '.byline a',
    '.post-meta a',

    // Generic external links without affiliate intent
    'a[rel="nofollow noreferrer"]:not([href*="go/"]):not([href*="track"]):not(.pm-play-now)',

    // Comment section links
    '.comments-area a',
    '.comment-content a'
]
```

### Affiliate URL Patterns to Detect

```javascript
AFFILIATE_PATTERNS: [
    // Paradise Media tracking
    /pm\.link\/[a-zA-Z0-9]+/,
    /go\.paradise\.media/,

    // Gaming store referrals
    /store\.steampowered\.com.*\?curator/,
    /humble\.com.*\?partner/,

    // Sportsbook affiliates
    /draftkings\.com.*\?promo/,
    /fanduel\.com.*\?promocode/,

    // Standard patterns
    /\/go\/[a-zA-Z0-9-]+/,
    /\/aff\/[a-zA-Z0-9-]+/,
    /\?ref=[a-zA-Z0-9-]+/
]
```

### Expected Outcome

| Metric | Before (v1.0) | After (v2.0) |
|--------|---------------|--------------|
| CTA Visible | 14,630 | ~500-1,500 |
| CTA Quality | Tier 3 (fingerprint) | Tier 1/2 (explicit) |
| Expected CTR | 0.02% | 3-8% |

---

## CTA_TEMPLATE_005_v2: iGaming News Theme (europeangaming.eu)

**Domain:** europeangaming.eu
**Theme:** Custom iGaming/B2B News
**Issue:** 0 CTA visible despite 141 outbound clicks - selectors completely missing the site's CTA patterns.

### Root Cause Analysis

europeangaming.eu is a B2B iGaming news site, NOT a consumer casino affiliate site. The v1.0 template assumed consumer-facing casino CTAs (`.casino-cta`, `.bonus-button`, `.visit-casino`) which don't exist on a B2B trade publication.

Actual CTA types on europeangaming.eu:
- Press release source links
- Company website links
- Conference/event registration
- Job listings
- Advertiser banners
- Social media follows

### v2.0 INCLUSION Selectors (Use These)

```javascript
CTA_SELECTORS: [
    // PRIORITY 1: Sponsor/Advertiser CTAs
    '.sponsored-content a',
    '.partner-logo a',
    '.advertiser-banner a',
    'a[href*="sponsor"]',
    '.banner-ad a',
    '.ad-slot a:not(.adsbygoogle a)',

    // PRIORITY 2: Press Release/Source Links
    'a[href*="prnewswire.com"]',
    'a[href*="globenewswire.com"]',
    'a[href*="businesswire.com"]',
    '.press-release-source a',
    '.source-link',
    'a.external-source',

    // PRIORITY 3: Company Website Links (outbound to iGaming companies)
    'a[href*="playtech.com"]',
    'a[href*="microgaming.co.uk"]',
    'a[href*="netent.com"]',
    'a[href*="evolutiongaming.com"]',
    'a[href*="pragmaticplay.com"]',
    'a[href*="yggdrasilgaming.com"]',
    'a[href*="scientific-games.com"]',
    'a[href*="igt.com"]',

    // PRIORITY 4: Event/Conference Links
    'a[href*="icegaming.com"]',
    'a[href*="sigma.world"]',
    'a[href*="igb.com"]',
    'a[href*="sbcevents.com"]',
    '.event-registration a',
    '.conference-cta a',
    'a[href*="register"]',
    'a[href*="event"]',

    // PRIORITY 5: Job Board CTAs
    '.job-listing a',
    'a[href*="careers"]',
    'a[href*="jobs."]',
    '.careers-cta a',

    // PRIORITY 6: Newsletter/Subscribe
    'form.newsletter button',
    '.newsletter-signup button',
    '.subscribe-form button[type="submit"]',
    '#mc_embed_signup input[type="submit"]',

    // PRIORITY 7: Social Sharing
    'a[href*="twitter.com/intent/tweet"]',
    'a[href*="facebook.com/sharer"]',
    'a[href*="linkedin.com/shareArticle"]',
    '.share-buttons a',
    '.social-share a',

    // PRIORITY 8: External article links (tracked as outbound)
    'article a[target="_blank"]',
    '.post-content a[rel="nofollow"]',
    '.entry-content a[href^="http"]:not([href*="europeangaming.eu"])'
]
```

### v2.0 EXCLUSION Selectors (Filter These Out)

```javascript
CTA_EXCLUSIONS: [
    // Site navigation
    'header a',
    'nav a',
    '.main-menu a',
    '.mobile-menu a',

    // Footer links
    'footer a',
    '.footer-widgets a',
    '.site-info a',

    // Pagination
    '.pagination a',
    '.nav-links a',
    '.page-numbers',

    // Internal category/tag links
    '.category-link',
    '.tag-link',
    'a[rel="category tag"]',

    // Comment section
    '.comments a',
    '#respond a',

    // Author profiles
    '.author-bio a',
    '.post-author a'
]
```

### Affiliate/Outbound URL Patterns to Detect

```javascript
OUTBOUND_PATTERNS: [
    // iGaming company domains
    /\.(playtech|netent|evolution|pragmatic|microgaming|igt)\.com/,

    // Press release sources
    /(prnewswire|globenewswire|businesswire|prgaming)\.com/,

    // Events
    /(icegaming|sigma\.world|igbaffiliate|sbcevents)\.com/,

    // Regulator sites
    /(mga\.org\.mt|gamblingcommission\.gov\.uk|njdge\.org)/,

    // Any external domain (general outbound tracking)
    /^https?:\/\/(?!europeangaming\.eu)/
]
```

### Expected Outcome

| Metric | Before (v1.0) | After (v2.0) |
|--------|---------------|--------------|
| CTA Visible | 0 | ~500-2,000 |
| Outbound Captured | 141 (missed) | ~141+ (as CTA events) |
| B2B Link Tracking | None | Full coverage |

---

## CTA_TEMPLATE_002_v2: Culture Theme (culture.org)

**Domain:** culture.org
**Theme:** Custom Culture.org theme
**Issue:** 791 CTA visible, 0 clicks - selectors may be targeting placeholder elements or invisible CTAs.

### Root Cause Analysis

Potential issues:
- CTAs may be dynamically loaded (JS-rendered after initial load)
- Forminator forms may not be interactive
- "Related article" sections might be below the fold and never clicked
- Social icons may be missing href attributes

The very low dwell time (20s) and high pogo rate (9.1%) suggest users leave quickly, so above-the-fold CTAs are most important.

### v2.0 INCLUSION Selectors (Use These)

```javascript
CTA_SELECTORS: [
    // PRIORITY 1: Primary Action Buttons (above the fold)
    '.global-btn:not(.disabled)',
    'button.global-btn',
    'a.global-btn[href]',
    '.cta-button',
    '.action-btn',

    // PRIORITY 2: Newsletter/Email Signup (HIGH VALUE)
    '.forminator-button-submit',
    '.forminator-button:not(.forminator-button-back)',
    'form.forminator-ui button[type="submit"]',
    'input.forminator-button-submit',
    '.email-signup-btn',

    // PRIORITY 3: Social Sharing (with valid href)
    '.frame-a-social a[href*="twitter.com/intent"]',
    '.frame-a-social a[href*="facebook.com/sharer"]',
    'a.share-twitter[href]',
    'a.share-facebook[href]',
    '.social-share-btn[href]',

    // PRIORITY 4: Content Engagement (visible, interactive)
    '.related-article-wrapper a.article-link',
    '.related-article-card a:first-child',
    '.also-like-wrapper a.article-link',
    'a.read-article-btn',

    // PRIORITY 5: Category/Topic Exploration
    '.topic-tag a',
    '.explore-topic a',
    '.featured-category a.view-all',

    // PRIORITY 6: Search (user intent)
    '.search-btn[type="submit"]',
    'button.search-btn',
    'form.search-form button',

    // PRIORITY 7: Load More / Pagination
    '.load-more-button:not(.loading)',
    'button.load-more',
    '.pagination-next a'
]
```

### v2.0 EXCLUSION Selectors (Filter These Out)

```javascript
CTA_EXCLUSIONS: [
    // Disabled/inactive states
    '.disabled',
    '.loading',
    '[disabled]',
    '.btn-inactive',

    // Back/Cancel buttons (low value)
    '.back-btn',
    '.cancel-btn',
    '.forminator-button-back',

    // Navigation (not CTAs)
    'header nav a',
    '.main-navigation a',
    '.breadcrumb a',

    // Footer navigation
    '.footer-nav a',
    '.site-footer a',
    '.footer-social-icon a',

    // Comment section
    '.comment-reply-link',
    '.comment-content a',

    // Internal article links in body (tracked as pageviews)
    '.article-content a[href*="culture.org"]',
    '.post-body a[href^="/"]',

    // Author/byline
    '.author-name a',
    '.byline a'
]
```

### Expected Outcome

| Metric | Before (v1.0) | After (v2.0) |
|--------|---------------|--------------|
| CTA Visible | 791 | ~200-400 |
| CTAs Above Fold | Unknown | Prioritized |
| Expected CTR | 0% | 1-3% |

---

## Implementation Notes

### Selector Priority System

When multiple selectors match, use this priority order:

1. **Tier 1 - Explicit Attributes**: `data-cta-id`, `data-track`, `data-analytics`
2. **Tier 2 - URL Patterns**: `/go/`, `/out/`, `affiliate`, `?ref=`
3. **Tier 3 - CSS Classes**: `.pm-play-now`, `.cta-button`, `.subscribe-btn`
4. **Tier 4 - Contextual**: Based on parent container + element type

### Exclusion Implementation

```javascript
// In NavBoost tracker, apply exclusions AFTER inclusions
function shouldTrackElement(element) {
    // Check if element matches any inclusion selector
    const isIncluded = CTA_SELECTORS.some(sel => element.matches(sel));
    if (!isIncluded) return false;

    // Check if element matches any exclusion selector
    const isExcluded = CTA_EXCLUSIONS.some(sel => element.matches(sel));
    if (isExcluded) return false;

    // Additional checks
    // - Element must be visible (offsetHeight > 0)
    // - Element must have href or be button
    // - Element must not be inside excluded container

    return true;
}
```

### CSS Selector Best Practices

1. **Be specific**: Use `.parent .child` instead of just `.child`
2. **Use attribute selectors**: `a[href*="/go/"]` is more reliable than class names
3. **Avoid tag-only selectors**: `button` catches too much; use `button.cta-class`
4. **Test in DevTools**: Run `document.querySelectorAll(selector)` before deploying

### Testing Procedure

For each domain after updating selectors:

1. Open browser DevTools (F12)
2. Run: `document.querySelectorAll('YOUR_SELECTOR').length`
3. Verify count is reasonable (not 0, not thousands)
4. Check sample elements are actual CTAs
5. Deploy updated tracker
6. Wait 24h and verify CTA visible count in PostHog

---

## Domain Mapping (v2.0)

| Domain | Template | Status | Action |
|--------|----------|--------|--------|
| hudsonreporter.com | CTA_TEMPLATE_003_v2 | UPDATE REQUIRED | Apply v2 selectors + exclusions |
| dotesports.com | CTA_TEMPLATE_004_v2 | UPDATE REQUIRED | Focus on PM affiliate only |
| europeangaming.eu | CTA_TEMPLATE_005_v2 | UPDATE REQUIRED | Add B2B iGaming selectors |
| culture.org | CTA_TEMPLATE_002_v2 | UPDATE REQUIRED | Prioritize above-fold CTAs |
| pokerology.com | CTA_TEMPLATE_005 | NO CHANGE | Working correctly (2.1% CTR) |
| northeasttimes.com | CTA_TEMPLATE_003 | NO CHANGE | Working correctly (2.2% CTR) |
| snjtoday.com | CTA_TEMPLATE_006 | NO CHANGE | Monitor for volume |

---

## Rollout Plan

### Phase 1: High-Impact Fixes (Week 1)

1. **hudsonreporter.com** - Highest volume, worst false positive rate
   - Deploy CTA_TEMPLATE_003_v2
   - Expected: 95% reduction in false positives

2. **europeangaming.eu** - Currently 0 detection
   - Deploy CTA_TEMPLATE_005_v2
   - Expected: 500+ CTA detections

### Phase 2: Quality Improvements (Week 2)

3. **dotesports.com** - High volume, low quality
   - Deploy CTA_TEMPLATE_004_v2
   - Expected: 90% reduction, higher quality IDs

4. **culture.org** - Low engagement
   - Deploy CTA_TEMPLATE_002_v2
   - Expected: Improved CTR from 0% to 1-3%

### Phase 3: Validation (Week 3)

- Run diagnostic queries on all 4 domains
- Compare before/after metrics
- Document lessons learned
- Update NAVBOOST_v1.3.0_SPEC.md if needed

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-28 | BlackTeam | Initial templates |
| 2.0 | 2026-02-04 | B-RANK + B-FORG | Refined selectors for 4 problem domains |

---

## References

- PostHog Diagnostic Report: `/home/andre/projects/posthog-integration/reports/POSTHOG_DIAGNOSTIC_REPORT_2026-02-03.md`
- Original Templates: `/home/andre/projects/posthog-integration/CTA_TEMPLATES.md`
- NavBoost KPI Framework: `/home/andre/projects/posthog-integration/NAVBOOST_KPI_FRAMEWORK.md`

---

*Generated by BlackTeam: B-RANK (SEO Commander) + B-FORG (DataForge)*
*Task: CTA Selector Audit and Refinement*
*"Precision in tracking leads to precision in optimization."*
