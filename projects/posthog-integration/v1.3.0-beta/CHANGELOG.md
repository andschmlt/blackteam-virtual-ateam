# NavBoost Tracker Changelog

## [1.3.0] - 2026-02-04

### Codename: "Smart CTA Detection"

### Summary
NavBoost v1.3.0 introduces a **3-tier CTA identification system** that generates consistent, meaningful CTA IDs instead of random fingerprints. This enables accurate tracking of specific CTAs across sessions and users.

### Problem Solved
- **Previous Issue (v1.2.1):** CTA IDs like `span__p3ys` or `a_IEM_Krakow_2026:_Tea_z4ai` were generated using random suffixes, making it impossible to:
  - Track the same CTA across sessions
  - Answer "Which specific CTA drives the most conversions?"
  - Compare CTA performance over time

### New Features

#### 3-Tier CTA Identification System

| Tier | Priority | Method | Example Output |
|------|----------|--------|----------------|
| **Tier 1** | Highest | HTML Attributes | `header-signup-betway` |
| **Tier 2** | Medium | URL Pattern Derivation | `affiliate_betway` |
| **Tier 3** | Fallback | Position + Fingerprint | `link_play_now_article_pos3` |

#### Tier 1: Explicit HTML Attributes
Checks for (in priority order):
1. `data-cta-id` attribute (recommended)
2. `data-cta-name` attribute
3. `data-track-id` attribute
4. `id` attribute (if not auto-generated)

Validation:
- Rejects auto-generated IDs (WordPress blocks, React components, UUIDs)
- Requires alphanumeric with dashes/underscores only
- Length between 3-100 characters

#### Tier 2: URL Pattern Derivation
Detects CTA identity from URL patterns:

| Pattern | Result |
|---------|--------|
| `/go/betway` | `affiliate_betway` |
| `/out/draftkings` | `outbound_draftkings` |
| `/aff/888casino` | `affiliate_888casino` |
| `?ref=poker` | `referral_poker` |
| `twitter.com/intent` | `social_twitter` |
| Known affiliate domain | `affiliate_{domain}` |
| External domain | `external_{domain}` |

#### Tier 3: Position + Element Fingerprint
Generates consistent fingerprint using:
- CTA type (link, button, social_twitter, etc.)
- Normalized text (first 20 chars, lowercase, alphanumeric)
- Container region (header, footer, sidebar, article, etc.)
- Position index within container

Format: `{type}_{text}_{region}_pos{n}`

### New Event Properties

| Property | Type | Description |
|----------|------|-------------|
| `cta_id` | string | Smart CTA identifier (improved) |
| `cta_id_tier` | number | Which tier generated the ID (1, 2, or 3) |
| `cta_id_method` | string | Specific method used |
| `cta_region` | string | Container region (header, footer, sidebar, etc.) |
| `cta_position` | number | Position index in region |
| `cta_href_pattern` | string | Detected URL pattern type |

### Example Event Payload (v1.3.0)

```json
{
    "event": "navboost:cta_click",
    "properties": {
        "cta_id": "affiliate_betway",
        "cta_id_tier": 2,
        "cta_id_method": "url-affiliate-pattern",
        "cta_type": "link",
        "cta_text": "Play Now at Betway",
        "cta_href": "/go/betway",
        "cta_region": "article",
        "cta_position": 3,
        "cta_href_pattern": "/go/",
        "tracker_version": "1.3.0"
    }
}
```

### Diagnostic Mode

New diagnostic function for CTA detection analysis:

```javascript
// Run in browser console
window.navboostDiagnostic()
```

Returns:
- Total links vs detected CTAs
- Detection rate percentage
- Tier distribution (how many Tier 1/2/3 IDs)
- CTA breakdown by type
- Potential undetected CTAs (affiliate links not in selectors)
- Full CTA details table

### Session End Data Enhancement

Added `cta_tier_distribution` to session end events:
```json
{
    "cta_tier_distribution": { "1": 2, "2": 5, "3": 3 }
}
```

### Configuration Updates

New configurable options in CONFIG:

```javascript
CONFIG.AFFILIATE_URL_PATTERNS = [
    { pattern: /\/go\/([a-zA-Z0-9_-]+)/i, prefix: 'affiliate', capture: 1 },
    { pattern: /\/out\/([a-zA-Z0-9_-]+)/i, prefix: 'outbound', capture: 1 },
    // ... more patterns
];

CONFIG.KNOWN_AFFILIATE_DOMAINS = [
    'betonlineaffiliates.com',
    'masteraffiliates.com',
    // ... more domains
];
```

### Backward Compatibility

- All v1.2.1 events remain valid
- New properties are additive (no breaking changes)
- Existing PostHog queries continue to work
- Tier 3 fingerprints are more deterministic than v1.2.1 random IDs

### Migration Notes

1. **No action required** - Deploy v1.3.0 and it works immediately
2. **Recommended** - Add `data-cta-id` to key CTAs for Tier 1 detection
3. **Optional** - Run diagnostic to identify undetected CTAs

### Files Changed

- `navboost-tracker-v1.3.0.js` - New tracker with 3-tier system
- `CHANGELOG.md` - This file

### Reference

- Specification: `NAVBOOST_v1.3.0_SPEC.md`
- Authors: B-TECH (Tech Lead), B-CODY (CodeGuard)
- Based on: WhiteTeam specification by W-IVAN

---

## [1.2.1] - 2026-01-28

### CTA Template Integration

- Replaced generic CTA selectors with site-specific templates
- Added CTA_TEMPLATE_004 for GAMURS/Esports theme
- Fixed CTA Visible = 0 issue on dotesports.com
- Added affiliate promo selectors (.pm-promo-code-container, .pm-play-now)
- Added GAMURS block selectors
- Manual browser audit verification by Director

---

## [1.2.0] - 2026-01-26

### Error Logging & Heartbeat

- Added comprehensive error logging with telemetry
- Added heartbeat events every 30 seconds
- Added visibilitychange/pagehide handlers for mobile

---

## [1.1.0] - 2026-01-21

### Conversion Tracking

- Added newsletter signup tracking
- Added content consumed conversion
- Added affiliate click detection

---

## [1.0.0] - 2026-01-16

### Initial Release

- Session tracking (start/end)
- Scroll depth tracking
- CTA visibility and click tracking
- Outbound link tracking
- Google referrer detection
- Pogo-stick detection
