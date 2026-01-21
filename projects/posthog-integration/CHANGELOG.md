# PostHog Integration - Changelog

**Project:** PostHog NavBoost Integration
**Maintained by:** Virtual ATeam - BlackTeam
**Last Updated:** 2026-01-21

---

## Overview

This changelog tracks all commits, versions, and updates across all domains in the PostHog integration project.

---

## Domain Status Summary

| Domain | Version | Status | PostHog ID | Last Update |
|--------|---------|--------|------------|-------------|
| hudsonreporter.com | 1.1.0 | Active | 295222 | 2026-01-21 |
| northeasttimes.com | 1.1.0 | Active | - | 2026-01-21 |
| lover.io | 1.0.0 | Active | - | 2026-01-16 |
| bestdaily.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| betanews.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| centraljersey.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| countryqueer.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| culture.org | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| dotesports.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| esports.gg | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| europeangaming.eu | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| godisageek.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| iogames.space | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| lowerbuckstimes.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| management.org | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| metrotimes.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| mrracy.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| newgamenetwork.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| ostexperte.de | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| philadelphiaweekly.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| pokerology.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| pokertube.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| silvergames.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| snjtoday.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| southphillyreview.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| sport-oesterreich.at | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| starnewsphilly.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| theroanokestar.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| thesunpapers.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| topdocumentaryfilms.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |
| warcraftmovies.com | 1.1.0 | Pending Deploy | - | 2026-01-21 |

---

## Changelog by Domain

### Bulk Update - 28 Domains (2026-01-21)

**ClickUp Task:** [86aepuk2b](https://app.clickup.com/t/86aepuk2b)
**Type:** Conversion Tracking
**Assignees:** Joshua, Malcolm

**Domains Updated:**
- bestdaily.com
- betanews.com
- centraljersey.com
- countryqueer.com
- culture.org
- dotesports.com
- esports.gg
- europeangaming.eu
- godisageek.com
- iogames.space
- lowerbuckstimes.com
- management.org
- metrotimes.com
- mrracy.com
- newgamenetwork.com
- ostexperte.de
- philadelphiaweekly.com
- pokerology.com
- pokertube.com
- silvergames.com
- snjtoday.com
- southphillyreview.com
- sport-oesterreich.at
- starnewsphilly.com
- theroanokestar.com
- thesunpapers.com
- topdocumentaryfilms.com
- warcraftmovies.com

**Changes:**
- Added enhanced conversion tracking (5 types)
  - Newsletter Signup tracking
  - Ad Click tracking
  - Affiliate Click tracking
  - Article Completion tracking
  - Return Visit tracking
- Created `conversion-tracker.js` (28KB each)
- Created `posthog-full-tracking.php` with WordPress integration
- Created `DEPLOYMENT_GUIDE.md` with SQL queries for conversion rates

---

### hudsonreporter.com

#### v1.1.0 (2026-01-21)
**Type:** Feature Update
**ClickUp Task:** [86aeprpck](https://app.clickup.com/t/86aeprpck) (Sub-task of 86aepf7r3)
**Git Commit:** `eda7350`

**Changes:**
- Added enhanced conversion tracking (5 types)
- Created `conversion-tracker.js`
- Created `posthog-full-tracking.php`
- Created `DEPLOYMENT_GUIDE.md`

#### v1.0.0 (2026-01-21)
**Type:** Initial Setup
**ClickUp Task:** [86aepf7r3](https://app.clickup.com/t/86aepf7r3)

**Changes:**
- Initial PostHog NavBoost integration

---

### northeasttimes.com

#### v1.1.0 (2026-01-21)
**Type:** Feature Update
**ClickUp Task:** [86aeptbq3](https://app.clickup.com/t/86aeptbq3) (Sub-task of 86aepf41p)
**Git Commit:** `aeba50ef`

**Changes:**
- Added enhanced conversion tracking (5 types)
- Created `conversion-tracker.js`
- Created `posthog-full-tracking.php`
- Created `DEPLOYMENT_GUIDE.md`

#### v1.0.0 (2026-01-16)
**Type:** Initial Setup
**Status:** Deployed

**Changes:**
- Initial PostHog NavBoost integration
- Daily cron report configured (09:05)

---

### lover.io

#### v1.0.0 (2026-01-16)
**Type:** Initial Setup
**Status:** Deployed

**Changes:**
- Initial PostHog NavBoost integration
- Daily cron report configured (09:00)

---

## Commit Log

| Date | Domain | Version | Commit Message | Author |
|------|--------|---------|----------------|--------|
| 2026-01-21 | 28 domains | 1.1.0 | Bulk add conversion tracking | Virtual ATeam |
| 2026-01-21 | northeasttimes.com | 1.1.0 | Add conversion tracking (5 types) | Virtual ATeam |
| 2026-01-21 | hudsonreporter.com | 1.1.0 | Add conversion tracking (5 types) | Virtual ATeam |
| 2026-01-21 | hudsonreporter.com | 1.0.0 | Initial PostHog NavBoost setup | Virtual ATeam |
| 2026-01-16 | lover.io | 1.0.0 | Initial PostHog NavBoost setup | Virtual ATeam |
| 2026-01-16 | northeasttimes.com | 1.0.0 | Initial PostHog NavBoost setup | Virtual ATeam |

---

## Version History

### Version Numbering

- **Major (X.0.0):** Breaking changes or complete rewrites
- **Minor (1.X.0):** New features (e.g., conversion tracking)
- **Patch (1.0.X):** Bug fixes and minor updates

### Feature Versions

| Version | Features |
|---------|----------|
| 1.0.0 | NavBoost tracking, WordPress integration, dashboard queries |
| 1.1.0 | + Enhanced conversion tracking (5 types) |

---

## ClickUp Task Reference

| Scope | Task ID | Description |
|-------|---------|-------------|
| Bulk (28 domains) | [86aepuk2b](https://app.clickup.com/t/86aepuk2b) | Add Conversion Tracking to 28 Domains |
| hudsonreporter.com | [86aepf7r3](https://app.clickup.com/t/86aepf7r3) | PostHog Configuration |
| northeasttimes.com | [86aepf41p](https://app.clickup.com/t/86aepf41p) | PostHog Configuration |

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/posthog_setup` | Initial PostHog setup for new domains |
| `/posthog_update` | Update existing PostHog configurations |
| `/posthog_analysis` | Generate PostHog analytics reports |

---

## Files Structure

```
posthog-integration/
├── CHANGELOG.md              # This file
├── [domain]/
│   ├── navboost-tracker.js
│   ├── conversion-tracker.js     # v1.1.0+
│   ├── posthog-functions.php
│   ├── posthog-full-tracking.php # v1.1.0+
│   ├── dashboard-queries.sql
│   ├── cohorts-funnels.json
│   ├── README.md
│   └── DEPLOYMENT_GUIDE.md       # v1.1.0+
```

---

*Generated by Virtual ATeam - BlackTeam*
*Last Updated: 2026-01-21*
