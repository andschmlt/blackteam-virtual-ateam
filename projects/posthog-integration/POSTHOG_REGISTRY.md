# PostHog Integration Registry

**Project:** PostHog NavBoost Integration
**Maintained by:** Virtual ATeam - BlackTeam
**Last Updated:** 2026-01-28
**Last Verified:** 2026-01-28 (PostHog API query)

---

## Purpose

This registry is the source of truth for all PostHog configurations across Paradise Media domains. It tracks:
- Domain configurations and versions
- GitHub repositories and branches
- ClickUp task references (parent and sub-tasks)
- **NEW: Actual deployment status verified against PostHog data**

**Used by:** `/posthog_update` command, `/posthog_analysis`

---

## CRITICAL: Deployment Status Legend

| Status | Meaning |
|--------|---------|
| ✅ LIVE | PostHog events confirmed in last 7 days |
| 📦 PACKAGED | v1.2.0 package ready, awaiting TechOps deployment |
| ⏳ COMMITTED | Code committed to GitHub, not yet deployed to production |
| ❌ NO DATA | No PostHog events found (SDK may not be installed) |

---

## Domain Registry (with Verified Status)

| Domain | Registry Ver | Prod Ver | PostHog SDK | NavBoost | Parent Task | v1.2.1 SubTask | Status |
|--------|--------------|----------|-------------|----------|-------------|----------------|--------|
| hudsonreporter.com | 1.2.1 | **1.2.0** | ✅ 5,315 pv | ✅ 8,431 | 86aepf7r3 | 86aewdj28 | ✅ LIVE |
| dotesports.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf23j | 86aewrha9 | 📦 v1.2.1 READY |
| culture.org | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf1v4 | 86aewrhe0 | 📦 v1.2.1 READY |
| pokertube.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4b4 | 86aewrhjm | 📦 v1.2.1 READY |
| snjtoday.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4et | 86aewrhp5 | 📦 v1.2.1 READY |
| bestdaily.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf1kz | 86aewrhtu | 📦 v1.2.1 READY |
| betanews.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf1nt | 86aewrhwz | 📦 v1.2.1 READY |
| centraljersey.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf1qd | 86aewrhzk | 📦 v1.2.1 READY |
| countryqueer.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf1t9 | 86aewrj32 | 📦 v1.2.1 READY |
| esports.gg | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf24b | 86aewrj6f | 📦 v1.2.1 READY |
| europeangaming.eu | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf25g | 86aewrj90 | 📦 v1.2.1 READY |
| godisageek.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf27r | 86aewrjcc | 📦 v1.2.1 READY |
| iogames.space | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf2a9 | 86aewrjgm | 📦 v1.2.1 READY |
| lover.io | 1.0.0 | N/A | ❌ 0 | ❌ 0 | - | - | ❌ NO DATA |
| lowerbuckstimes.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf3mc | 86aewrjnz | 📦 v1.2.1 READY |
| management.org | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf3pg | 86aewrjvb | 📦 v1.2.1 READY |
| metrotimes.com | 1.1.0 | N/A | ❌ 0 | ❌ 0 | 86aepf7vx | - | ❌ NO REPO |
| mrracy.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf3tn | 86aewrjy9 | 📦 v1.2.1 READY |
| newgamenetwork.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf3y2 | 86aewrk1r | 📦 v1.2.1 READY |
| northeasttimes.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf41p | 86aewrk5f | 📦 v1.2.1 READY |
| ostexperte.de | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf45e | 86aewrk99 | 📦 v1.2.1 READY |
| philadelphiaweekly.com | 1.1.0 | N/A | ❌ 0 | ❌ 0 | 86aepf81y | - | ❌ NO REPO |
| pokerology.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf48h | 86aewrkca | 📦 v1.2.1 READY |
| silvergames.com | 1.1.0 | N/A | ❌ 0 | ❌ 0 | 86aepf886 | - | ❌ NO REPO |
| southphillyreview.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4ht | 86aewrkkb | 📦 v1.2.1 READY |
| sport-oesterreich.at | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4nc | 86aewrkpy | 📦 v1.2.1 READY |
| starnewsphilly.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4rw | 86aewrkuq | 📦 v1.2.1 READY |
| theroanokestar.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf4xc | 86aewrkxn | 📦 v1.2.1 READY |
| thesunpapers.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf51u | 86aewrm2b | 📦 v1.2.1 READY |
| topdocumentaryfilms.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf55v | 86aewrm5c | 📦 v1.2.1 READY |
| warcraftmovies.com | 1.2.1 | N/A | ❌ 0 | ❌ 0 | 86aepf5b2 | 86aewrm9b | 📦 v1.2.1 READY |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Domains in Registry | 29 |
| ✅ LIVE (PostHog data confirmed) | **1** (hudsonreporter.com) |
| 📦 v1.2.1 READY (complete package with attachments) | **26** |
| ❌ NO DATA / NO REPO | **3** (lover.io, metrotimes, philadelphiaweekly, silvergames) |

### v1.2.1 Update (2026-01-28)

All 26 domains now have complete packages with:
- PostHog SDK (`posthog-functions.php`)
- NavBoost Tracker (`navboost-tracker-v1.2.1.js`)
- Deployment Guide (`DEPLOYMENT_GUIDE_v1.2.1.md`)
- Release Notes (`RELEASE_NOTES_v1.2.1.md`)

**Files are ATTACHED to ClickUp subtasks** (not GitHub links)

---

## v1.2.0 Packages Ready for Deployment

These packages are in `/home/andre/projects/posthog-integration/v1.2.0-source/` and attached to ClickUp subtasks:

| Domain | CTA Template | Audit Status | SubTask ID | Files |
|--------|--------------|--------------|------------|-------|
| hudsonreporter.com | CTA_TEMPLATE_003 | ⏳ PENDING | 86aewdj28 | navboost-tracker-v1.2.0.js, RELEASE_NOTES |
| dotesports.com | CTA_TEMPLATE_004 | ✅ VERIFIED | 86aewepp1 | navboost-tracker-v1.2.0.js, RELEASE_NOTES |
| culture.org | CTA_TEMPLATE_002 | ⏳ PENDING | 86aewdnkz | navboost-tracker-v1.2.0.js, RELEASE_NOTES |
| pokertube.com | CTA_TEMPLATE_005 | ⏳ PENDING | 86aewdntp | navboost-tracker-v1.2.0.js, RELEASE_NOTES |
| snjtoday.com | CTA_TEMPLATE_006 | ✅ VERIFIED | 86aewkqxw | navboost-tracker-v1.2.0.js, RELEASE_NOTES |

---

## GitHub Repository Reference

| Domain | GitHub Repo | Branch | Commit (v1.1.0) |
|--------|-------------|--------|-----------------|
| hudsonreporter.com | ParadiseMediaOrg/hudsonreporter.com | main | eda7350 |
| dotesports.com | ParadiseMediaOrg/dotesports.com | staging | 3c0dbb26 |
| culture.org | ParadiseMediaOrg/culture.org | staging | 53a989da |
| pokertube.com | ParadiseMediaOrg/pokertube.com | staging | f034e69 |
| snjtoday.com | ParadiseMediaOrg/snjtoday.com | main | - |
| europeangaming.eu | ParadiseMediaOrg/europeangaming.eu | main | - |
| northeasttimes.com | ParadiseMediaOrg/northeasttimes.com | main | aeba50ef |
| lover.io | ryhats11/lover.io | main | - |

---

## Domains Without GitHub Repos

These domains have ClickUp tasks but no GitHub repository:
- metrotimes.com (Task: 86aepf7vx)
- philadelphiaweekly.com (Task: 86aepf81y)
- silvergames.com (Task: 86aepf886)

---

## Version History

| Version | Date | Features | Domains Affected |
|---------|------|----------|------------------|
| 1.0.0 | 2026-01-16 | NavBoost tracking, WordPress integration | lover.io, northeasttimes.com |
| 1.1.0 | 2026-01-21 | + Enhanced conversion tracking (5 types) | 27 domains (committed) |
| 1.2.0 | 2026-01-28 | + CTA Template System, per-site selectors | 5 domains (packaged) |

### Version Features

**v1.0.0 - NavBoost Integration**
- Core Web Vitals tracking (LCP, CLS, INP)
- NavBoost KPIs (pogo rate, dwell time, scroll depth, CTA CTR)
- Session recording
- Heatmaps
- WordPress integration via posthog-functions.php

**v1.1.0 - Conversion Tracking**
- Newsletter Signup tracking (value: 5)
- Ad Click tracking (value: 1)
- Affiliate Click tracking (value: 3-10)
- Article Completion tracking (value: 2)
- Return Visit tracking (value: 1-3)
- conversion-tracker.js (28KB)
- posthog-full-tracking.php with enhanced WordPress hooks
- DEPLOYMENT_GUIDE.md with HogQL queries

**v1.2.0 - CTA Template System**
- Site-specific CTA selectors (6 templates)
- Mandatory pre-release audit workflow
- Affiliate link pattern detection
- Heartbeat events (30s intervals)
- Enhanced error logging
- Template: CTA_TEMPLATES.md

---

## API Keys Reference

| Domain/Project | PostHog Project ID | API Key Location |
|----------------|-------------------|------------------|
| Default | 295222 | ~/.keys/.env |
| northeasttimes.com | - | POSTHOG_NORTHEASTTIMES_API_KEY |
| europeangaming.eu | - | POSTHOG_EUROPEANGAMING_API_KEY |

---

## Verification Queries

Run these to verify deployment status:

```sql
-- Check PostHog SDK presence (should have $pageview events)
SELECT properties.$host as domain, count() as pageviews
FROM events
WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY domain
ORDER BY pageviews DESC

-- Check NavBoost tracker version
SELECT properties.$host as domain, properties.tracker_version as version, count()
FROM events
WHERE event = 'navboost:init_complete' AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY domain, version
ORDER BY count() DESC
```

---

*Generated by Virtual ATeam - BlackTeam*
*Head of Tech*
*Last Updated: 2026-01-28*
*Verified against PostHog project 295222*
