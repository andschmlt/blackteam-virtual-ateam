# R-TOPLIST-01: TechOps TopList Embed Rules

**Priority:** P1 High
**Created:** 2026-02-24
**Applies To:** All money pages (betting, casino, affiliate roundups)

---

## Rule

ALL money pages MUST use TechOps TopList embed widget instead of static markdown tables.

---

## Embed Format

```html
<div data-toplist="{TOPLIST_ID}"></div>
<script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
```

Each money page gets its **OWN unique TopList ID** from TechOps. If no ID is provided, **ASK the user** before proceeding.

---

## Current TopList IDs

| Page | TopList ID |
|------|-----------|
| Betting | `10-best-betting-sites-in-australia-for-2-7ur6rr` |
| Casino | `best-online-casino-australia-review-yc7ynm` |

---

## CSP Requirements

The CDN domain `cdn-6a4c.australiafootball.com` MUST be whitelisted in Content Security Policy:

```
script-src: cdn-6a4c.australiafootball.com
style-src: cdn-6a4c.australiafootball.com
connect-src: cdn-6a4c.australiafootball.com
```

---

## Replaces

The static "First Look" markdown table from Palm output. During `/content_palm` Phase 10a, transform #7 replaces the Palm table with the TopList embed.

---

## Enforcement

| System | How Enforced |
|--------|-------------|
| `/content_palm` | Phase 10a transform #7 |
| `/bedrock_agent` | Quality Gates check |
| `PALM_CONTENT_RULES.md` | Rule 6 |
| WhiteTeam | W-VERA validates embed presence |

---

## MUST-DOs

1. Use the EXACT TopList ID assigned to the page
2. Include both `<div>` and `<script>` elements
3. Verify CSP allows the CDN domain
4. Test embed loads in built page

## MUST-DON'Ts

1. NEVER use static markdown tables for brand lineups on money pages
2. NEVER hardcode brand lists inline when a TopList ID exists
3. NEVER guess a TopList ID — ask user if not provided

---

**Version:** 1.0.0
