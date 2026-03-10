# R-SEO-03: Astro Technical SEO Rules

**Priority:** P0 Critical
**Enforced Since:** 2026-02-24
**Applies To:** ALL Astro projects (australiafootball.com, europeangaming.eu, any future Astro site)
**Origin:** Screaming Frog audit of australiafootball.com (BT-2026-013)

---

## Purpose

Technical SEO issues identified via Screaming Frog crawl audit of australiafootball.com. These rules prevent duplicate URLs, hotlinked assets, truncated titles, missing metadata, incorrect OG types, bloated navigation, inconsistent schema, sitemap mismatches, and thin content from reaching production.

---

## Sub-Rules

### R-SEO-03a: Trailing Slash Configuration

**Finding:** Trailing slash inconsistency causes duplicate URLs (e.g., `/teams/` and `/teams` both indexed).

**Requirement:** MUST set `trailingSlash: 'always'` or `trailingSlash: 'never'` in `astro.config.mjs`. Pick one and enforce it site-wide. Never leave it as the default `'ignore'`.

**Enforcement:** B-RANK (SEO Commander) owns. W-LUNA validates.

```js
// astro.config.mjs — REQUIRED
export default defineConfig({
  trailingSlash: 'never', // or 'always' — pick one, never 'ignore'
});
```

---

### R-SEO-03b: External Image Hotlinking

**Finding:** Production pages hotlink images from wikimedia.org, unsplash.com, and other external domains. These URLs break without warning, slow page loads, and leak referrer data.

**Requirement:** NEVER hotlink images from external domains in production. All images MUST be self-hosted (downloaded to `public/images/` or `src/assets/`). External URLs are acceptable only during development/prototyping.

**Enforcement:** B-RANK (SEO Commander) owns. W-LUNA validates. Post Production (Loop 3) checks for external `src=` attributes.

```html
<!-- WRONG — hotlinked -->
<img src="https://upload.wikimedia.org/wikipedia/commons/..." alt="..." />

<!-- CORRECT — self-hosted -->
<img src="/images/teams/team-logo.webp" alt="..." />
```

---

### R-SEO-03c: Title Length Budget

**Finding:** metaTitle values include the site suffix (e.g., " | Australian Football"), causing titles to exceed 60 characters and get truncated in SERPs.

**Requirement:** Calculate the title budget as `60 - suffix.length = available characters`. The `metaTitle` field in frontmatter must NOT include the suffix — the layout's `titleTemplate` handles the suffix automatically. Validate that `metaTitle.length + suffix.length <= 60`.

**Enforcement:** B-RANK (SEO Commander) owns. W-LUNA validates. SEO Commander (Loop 2) checks all title lengths.

```astro
<!-- Layout.astro — suffix handled by titleTemplate -->
<SEO
  title={metaTitle}
  titleTemplate="%s | Australian Football"
/>
```

```markdown
---
# CORRECT: 35 chars + " | Australian Football" (24) = 59 chars
metaTitle: "AFL Teams - Complete Club Profiles"

# WRONG: includes suffix manually, will be doubled
metaTitle: "AFL Teams - Complete Club Profiles | Australian Football"
---
```

---

### R-SEO-03d: Meta Description Coverage

**Finding:** Some page types (hub pages, listing pages) lack unique meta descriptions, causing Google to auto-generate snippets.

**Requirement:** Every page type (content pages, listing pages, hub pages) MUST have a unique `description` between 150-160 characters. No two pages may share the same description. Listing pages should describe their content scope. Hub pages should describe their purpose.

**Enforcement:** B-SAM (SEO Manager) owns. W-EVAN validates.

---

### R-SEO-03e: OG Type Differentiation

**Finding:** All pages use `og:type="website"` regardless of content type, reducing social sharing context.

**Requirement:** Use the correct OG type per page:
- Articles, news, player profiles = `og:type="article"`
- Hub pages, listing pages, homepage = `og:type="website"`

**Enforcement:** B-SAM (SEO Manager) owns. W-EVAN validates.

```astro
---
const ogType = entry.collection === 'news' || entry.collection === 'players'
  ? 'article'
  : 'website';
---
```

---

### R-SEO-03f: Navigation Link Budget

**Finding:** Navigation sections with 60+ direct links per page (e.g., all teams listed in nav) dilute PageRank and cause crawl inefficiency.

**Requirement:** No navigation section may contain more than 20 direct links per page. Large taxonomies (e.g., 66 teams) MUST use parent-level links only (e.g., link to `/afl/teams/` not to each individual team). Detail pages are reached via listing pages, not global nav.

**Enforcement:** B-RANK (SEO Commander) owns. W-LUNA validates.

```
<!-- WRONG: 66 team links in nav -->
<nav>
  <a href="/afl/teams/adelaide-crows/">Adelaide Crows</a>
  <a href="/afl/teams/brisbane-lions/">Brisbane Lions</a>
  ... (64 more)
</nav>

<!-- CORRECT: parent links only -->
<nav>
  <a href="/afl/teams/">AFL Teams</a>
  <a href="/nrl/teams/">NRL Teams</a>
  <a href="/cricket/teams/">Cricket Teams</a>
</nav>
```

---

### R-SEO-03g: Schema.org Consistency

**Finding:** Inconsistent or missing structured data across page types. Some teams use Organization instead of SportsTeam; some pages have no schema at all.

**Requirement:** Use the correct Schema.org type per entity:

| Entity Type | Schema.org Type | Required Properties |
|-------------|-----------------|---------------------|
| Team | `SportsTeam` | name, sport, memberOf, url |
| Player | `Person` | name, birthDate, memberOf, jobTitle |
| News Article | `NewsArticle` | headline, datePublished, author, publisher |
| Hub/Listing | `WebPage` (or none) | name, description |

**Enforcement:** B-SAM (SEO Manager) owns. W-EVAN validates.

---

### R-SEO-03h: Sitemap-Build Parity

**Finding:** Sitemap includes URLs for pages that are filtered out during build (e.g., `isAggregated: true` pages appear in sitemap but not in rendered site), creating ghost URLs that return 404.

**Requirement:** Sitemap generation filters MUST exactly match page template filters. If a page template filters by `draft !== true` and `isAggregated !== true`, the sitemap MUST apply the same filters. Test by comparing sitemap URL count against `dist/` page count.

**Enforcement:** B-RANK (SEO Commander) owns. W-LUNA validates.

```typescript
// sitemap.xml.ts — filters MUST match [...slug].astro getStaticPaths()
const pages = await getCollection('teams', ({ data }) =>
  data.draft !== true && data.isAggregated !== true
);
```

---

### R-SEO-03i: Thin Content Mitigation

**Finding:** Player profiles with fewer than 200 words provide little value to search engines and may trigger thin content penalties.

**Requirement:** Player/entity profiles with fewer than 200 words of body content MUST be either:
1. **Enriched** with additional biographical data, career stats, or contextual information, OR
2. **Noindexed** using `<meta name="robots" content="noindex">` and excluded from sitemap

**Enforcement:** B-WALT (SEO White Hat) owns. W-EVAN validates.

---

## Validation Checklist (All Sub-Rules)

Before any Astro deployment, verify:

```markdown
## R-SEO-03 TECHNICAL SEO CHECKLIST
- [ ] R-SEO-03a: trailingSlash set to 'always' or 'never' in astro.config.mjs
- [ ] R-SEO-03b: No external hotlinked images (wikimedia, unsplash) in production
- [ ] R-SEO-03c: All metaTitles + suffix <= 60 characters
- [ ] R-SEO-03d: Every page type has a unique meta description (150-160 chars)
- [ ] R-SEO-03e: OG type = "article" for content, "website" for hubs/listings
- [ ] R-SEO-03f: No nav section exceeds 20 direct links
- [ ] R-SEO-03g: Schema.org types match entity types (SportsTeam, Person, NewsArticle)
- [ ] R-SEO-03h: Sitemap filters match page template filters (no ghost URLs)
- [ ] R-SEO-03i: No player profiles < 200 words without noindex
```

---

## Enforcement Summary

| Sub-Rule | Owner (BlackTeam) | Validator (WhiteTeam) | Ralph Loop |
|----------|--------------------|-----------------------|------------|
| R-SEO-03a | B-RANK | W-LUNA | Loop 2 (SEO) |
| R-SEO-03b | B-RANK | W-LUNA | Loop 3 (Technical) |
| R-SEO-03c | B-RANK | W-LUNA | Loop 2 (SEO) |
| R-SEO-03d | B-SAM | W-EVAN | Loop 2 (SEO) |
| R-SEO-03e | B-SAM | W-EVAN | Loop 2 (SEO) |
| R-SEO-03f | B-RANK | W-LUNA | Loop 2 (SEO) |
| R-SEO-03g | B-SAM | W-EVAN | Loop 2 (SEO) |
| R-SEO-03h | B-RANK | W-LUNA | Loop 3 (Technical) |
| R-SEO-03i | B-WALT | W-EVAN | Loop 1 (Content) |

**Failure to comply = DEPLOYMENT BLOCKED** -- no deployment is considered complete until all R-SEO-03 checks pass.

---

## Related Files

- **R-SEO-02:** `~/.claude/standards/ASTRO_SEO_RULES.md` -- astro-seo component and OG/Twitter standards
- **R-SEO-04:** `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md` -- traffic decline diagnosis using API leak parameters
- **R-IMG-01:** `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` -- image format and optimization
- **VALIDATION_STANDARDS:** `~/.claude/standards/VALIDATION_STANDARDS.md` -- pre-response checklist
- **TEAM_CONFIG:** `~/AS-Virtual_Team_System_v2/TEAM_CONFIG.md` -- persona assignments
- **RALPH_LOOPS:** `~/AS-Virtual_Team_System_v2/RALPH_LOOPS_SPECIFICATION.md` -- QA checkpoint details

---

*Rule R-SEO-03 | Created 2026-02-24 | Source: Screaming Frog audit of australiafootball.com (BT-2026-013)*
*Approved by: B-BOB (BlackTeam Director) + W-WOL (WhiteTeam Director)*
