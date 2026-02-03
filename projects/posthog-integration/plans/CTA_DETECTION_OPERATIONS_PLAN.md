# W-WOL CTA Detection Operations Plan

**Project:** PostHog NavBoost Integration
**Document:** CTA Detection & Remediation Workflow
**Version:** 1.0.0
**Created:** 2026-02-03
**Author:** W-WOL (Director)

---

## Overview

This plan defines the operational workflow for detecting, diagnosing, and fixing CTA tracking issues using the 3-tier CTA identification system introduced in NavBoost v1.3.0.

---

## The 3-Tier CTA Detection Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CTA DETECTION WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  START: Is CTA data being captured?                                 │
│         │                                                           │
│         ├─── YES ──► Are CTAs identifiable (not random IDs)?        │
│         │            │                                              │
│         │            ├─── YES ──► ✅ TIER 1 or 2 working            │
│         │            │                                              │
│         │            └─── NO ───► Apply TIER 1 (data-cta-id)        │
│         │                         or TIER 2 (/go/ patterns)         │
│         │                                                           │
│         └─── NO ───► Run Diagnostic                                 │
│                      │                                              │
│                      ├─── Selectors don't match? ──► Update         │
│                      │    CTA_TEMPLATES.md                          │
│                      │                                              │
│                      ├─── Wrong element type? ──► Add new selectors │
│                      │                                              │
│                      └─── JS error? ──► Check tracker_error events  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Weekly CTA Health Check

### Automated Monitoring Query

Run this HogQL query weekly to identify domains with CTA tracking issues:

```sql
-- CTA Health Check by Domain
SELECT
    properties.$host as domain,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    count(CASE WHEN event = 'navboost:session_start' THEN 1 END) as sessions,
    round(
        count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:session_start' THEN 1 END), 0)
    , 1) as cta_visibility_rate
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
AND event IN ('navboost:cta_visible', 'navboost:cta_click', 'navboost:session_start')
GROUP BY domain
ORDER BY cta_visibility_rate ASC
```

### Health Thresholds

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| CTA Visibility Rate | > 50% | 20-50% | < 20% |
| CTA Click Rate | > 2% | 1-2% | < 1% |
| Unique CTA Types | > 3 | 2-3 | < 2 |

### Alert Triggers

- **Critical:** Domain with sessions but 0 CTA visible events
- **Warning:** Domain with < 20% CTA visibility rate
- **Info:** Domain using only Tier 3 IDs (improvement opportunity)

---

## Phase 2: Diagnostic Workflow

### When to Run Diagnostics

1. **New domain onboarded** - After tracker deployment
2. **CTA visibility = 0** - No CTAs being detected
3. **Low CTA CTR** - CTAs visible but not clicked (< 1%)
4. **ID quality check** - Monthly review of CTA ID patterns

### Diagnostic Steps

#### Step 2.1: Check for Tracker Errors

```sql
-- Check for tracker errors
SELECT
    properties.error_context as error_context,
    properties.error_message as error_message,
    count() as occurrences,
    max(timestamp) as last_seen
FROM events
WHERE event = 'navboost:tracker_error'
AND properties.$host = 'domain.com'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY error_context, error_message
ORDER BY occurrences DESC
```

#### Step 2.2: Analyze CTA ID Distribution

```sql
-- CTA ID Tier Distribution (v1.3.0+)
SELECT
    properties.cta_id_tier as tier,
    properties.cta_id_method as method,
    count() as occurrences,
    uniqExact(properties.cta_id) as unique_ids
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND properties.$host = 'domain.com'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY tier, method
ORDER BY tier, occurrences DESC
```

**Interpretation:**
- **High Tier 1:** Excellent - HTML attributes being used
- **High Tier 2:** Good - URL patterns detected
- **High Tier 3:** Acceptable - Fingerprinting working, but consider adding attributes

#### Step 2.3: Find Potential Missing CTAs

```sql
-- Outbound clicks that MIGHT be CTAs but weren't detected as CTA_visible first
SELECT
    properties.outbound_url as url,
    properties.outbound_domain as domain,
    properties.is_affiliate as is_affiliate,
    count() as clicks,
    countIf(properties.link_type = 'affiliate') as affiliate_clicks
FROM events
WHERE event = 'navboost:outbound_click'
AND properties.$host = 'domain.com'
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY url, domain, is_affiliate
HAVING affiliate_clicks > 0
ORDER BY clicks DESC
LIMIT 30
```

**Action:** If affiliate URLs have clicks but no corresponding `cta_visible` events, the CTA selectors are missing those elements.

#### Step 2.4: Browser Console Diagnostic

**On-Site Testing (for developers):**

```javascript
// Run in browser console on the target page
if (window.navboostDiagnostic) {
    var report = window.navboostDiagnostic();
    console.log('Detection Rate:', report.detection_rate + '%');
    console.log('Tier Distribution:', report.tier_distribution);
    console.log('Undetected Potential CTAs:', report.undetected_potential_ctas);
}
```

---

## Phase 3: Remediation Actions

### Remediation Matrix

| Issue | Root Cause | Action | Owner |
|-------|------------|--------|-------|
| 0 CTA events | Selectors don't match | Update CTA_TEMPLATES.md | Tech |
| Low detection rate | Missing selector patterns | Add new selectors | Tech |
| Random CTA IDs | No attributes/patterns | Add data-cta-id to HTML | Content |
| Affiliate not tracked | /go/ not used | Add affiliate domain to patterns | Tech |
| Social not tracked | Wrong URL patterns | Update social URL regex | Tech |

### Action 3.1: Update CTA Selectors

**File:** `/home/andre/projects/posthog-integration/CTA_TEMPLATES.md`

**Process:**
1. Identify missing elements via diagnostic
2. Inspect element in browser DevTools (F12)
3. Extract class names, IDs, or href patterns
4. Add to appropriate CTA_TEMPLATE
5. Re-deploy tracker to affected domains

**Example Addition:**

```javascript
// NEW: Casino promo boxes (identified via diagnostic)
'.casino-promo-box a',
'.bonus-claim-button',
'a[href*="bonus."]',
```

### Action 3.2: Add data-cta-id Attributes (Tier 1)

**For Content Team:**

```html
<!-- BEFORE: No CTA tracking -->
<a href="/go/betway" class="btn">Play Now</a>

<!-- AFTER: Explicit CTA tracking -->
<a href="/go/betway" class="btn" data-cta-id="betway-play-now-article">Play Now</a>
```

**Naming Convention:**

```
{brand/action}-{cta-type}-{location}

Examples:
- betway-play-now-hero
- draftkings-bonus-sidebar
- newsletter-subscribe-footer
- share-twitter-article
```

### Action 3.3: Configure /go/ Patterns (Tier 2)

**For domains using custom outbound paths:**

```javascript
// Add to CONFIG.AFFILIATE_URL_PATTERNS in tracker
{ pattern: /\/visit\/([a-zA-Z0-9_-]+)/i, prefix: 'affiliate', capture: 1 },
{ pattern: /\/recommend\/([a-zA-Z0-9_-]+)/i, prefix: 'referral', capture: 1 },
```

### Action 3.4: Add Known Affiliate Domains (Tier 2)

**For direct affiliate links without /go/:**

```javascript
// Add to CONFIG.KNOWN_AFFILIATE_DOMAINS
'newaffiliate.com',
'trackingdomain.net',
```

---

## Phase 4: Validation & Verification

### Post-Remediation Checklist

After applying fixes, verify within 24-48 hours:

```sql
-- Verification Query
SELECT
    toDate(timestamp) as date,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    uniqExact(properties.cta_id) as unique_ctas,
    -- v1.3.0 tier breakdown
    countIf(properties.cta_id_tier = 1) as tier1_events,
    countIf(properties.cta_id_tier = 2) as tier2_events,
    countIf(properties.cta_id_tier = 3) as tier3_events
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND properties.$host = 'domain.com'
AND timestamp >= now() - INTERVAL 3 DAY
GROUP BY date
ORDER BY date DESC
```

### Success Criteria

| Metric | Before Fix | Target After Fix |
|--------|------------|------------------|
| CTA Visible Events | 0 or low | > 100/day |
| CTA Click Events | 0 or low | > 5/day |
| Unique CTA IDs | Random patterns | Consistent IDs |
| Tier 1 + Tier 2 % | < 20% | > 60% |

---

## Phase 5: Ongoing Maintenance

### Weekly Tasks

| Task | Owner | Query/Action |
|------|-------|--------------|
| Run CTA Health Check | W-DASH | See Phase 1 query |
| Review new domains | W-IVAN | Check tracker deployment |
| Check error events | W-FLUX | See Step 2.1 query |

### Monthly Tasks

| Task | Owner | Action |
|------|-------|--------|
| CTA ID Quality Review | W-WOL | Review Tier distribution |
| Template Audit | W-IVAN | Verify selectors still valid |
| Dashboard Update | W-DASH | Add new insights as needed |

### Per-Deployment Tasks

| When | Task | Owner |
|------|------|-------|
| New domain onboarded | Run diagnostic after 48h | W-IVAN |
| Tracker version upgrade | Verify CTA events continue | W-IVAN |
| Site redesign | Re-audit CTA selectors | Tech + Content |

---

## Escalation Path

```
┌─────────────────────────────────────────────────────────────────┐
│  ESCALATION MATRIX                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 1: W-DASH (BI Developer)                                 │
│  ─────────────────────────────────────────────────────────────  │
│  Handles: Dashboard queries, data analysis, reporting           │
│  Escalates: Technical issues, selector problems                 │
│                                                                  │
│  Level 2: W-IVAN (Tech Lead)                                    │
│  ─────────────────────────────────────────────────────────────  │
│  Handles: Selector updates, tracker fixes, deployments          │
│  Escalates: Architecture decisions, cross-domain issues         │
│                                                                  │
│  Level 3: W-WOL (Director)                                      │
│  ─────────────────────────────────────────────────────────────  │
│  Handles: Strategy decisions, resource allocation, approvals    │
│  Escalates: Business impact issues → Andre (Stakeholder)        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

### CTA Not Being Tracked?

```
1. Check tracker deployed? → navboost:init_complete event
2. Check for errors? → navboost:tracker_error events
3. Selectors match? → Run navboostDiagnostic()
4. Fix → Update CTA_TEMPLATES.md OR add data-cta-id
5. Verify → Check events after 24-48h
```

### Need Specific CTA Tracking?

```
Option A (Best): Add data-cta-id="my-cta-name" to HTML
Option B (Good): Use /go/brand-name URL pattern
Option C (OK):   Add CSS selector to CTA_TEMPLATES.md
```

### Emergency: CTA Events Dropped to Zero

```
1. Check navboost:tracker_error for JS errors
2. Check PostHog status (eu.posthog.com/status)
3. Verify tracker script still on page (view-source)
4. Check browser console for errors
5. Escalate to W-IVAN if unresolved
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-03 | W-WOL | Initial plan |

---

*W-WOL (Director) | WhiteTeam | WT-2026-007*
*"Quality is not negotiable. Build it right the first time."*
