# R-CONTENT-05: Content Freshness & Stale Data Prevention

**Priority:** P1 High
**Enforced Since:** 2026-02-26
**Applies To:** ALL sites with sports data (australiafootball.com, any future sports verticals)
**Origin:** australiafootball.com audit — ladder/fixture pages had stale hardcoded data with misleading "being updated" language

---

## Purpose

Prevent stale sports data (standings, fixtures, results, calendars, rankings) from persisting on production sites. Ensures automated refresh pipelines exist for time-sensitive content and that pages transparently show when data was last updated.

---

## Rules

### R-CONTENT-05a: No False Freshness Claims

**Requirement:** NEVER include text like "being updated", "updated regularly", "live scores", or "updated as the season progresses" unless an automated update pipeline actually exists for that page.

**If no automation exists:**
- Replace with honest language: "Last updated: {date}" or "Season 2025-26 standings as of Round {N}"
- Add a visible "Last Updated" date on every data-driven page

**Enforcement:** B-RANK (SEO Commander) owns. W-VERA (Content QA) validates.

---

### R-CONTENT-05b: Weekly Stale Content Audit

**Requirement:** A scheduled job MUST run weekly to check all data-driven pages for staleness.

**Pages to check:**
- Ladder/standings pages (all sports)
- Fixture/schedule pages (all sports)
- Calendar pages (F1, tennis, V8, horse racing)
- Rankings pages (tennis, UFC)
- Results/scores pages

**Staleness thresholds:**

| Content Type | Stale After | Action |
|-------------|-------------|--------|
| Ladder/standings (in-season) | 7 days without update | CRITICAL — update from API or flag |
| Ladder/standings (off-season) | Acceptable if marked "Final {year} season" | INFO |
| Fixtures (upcoming, in-season) | 7 days before next round starts | HIGH — update from API or flag |
| Fixtures (off-season) | Acceptable if marked "TBC — {year} season dates to be announced" | INFO |
| Calendar/schedule | 30 days without update | MEDIUM — verify dates still correct |
| Rankings | 14 days without update | MEDIUM — update from API or flag |
| Results/scores | 24 hours after match completion | HIGH — update or mark as pending |

**Enforcement:** Scheduled Cloud Run Job (weekly). B-TECH (Tech Lead) owns pipeline. W-IVAN (Architecture) validates.

---

### R-CONTENT-05c: Automated Data Pipeline Required

**Requirement:** Every data-driven page MUST have one of:

1. **Automated API pipeline** — Scheduled job fetches fresh data, updates content, triggers rebuild
2. **Manual update schedule** — Documented weekly responsibility with owner assigned
3. **Static with honest labeling** — Page clearly states the data vintage and is excluded from freshness audit

**Pipeline architecture (when automated):**

```
Cloud Scheduler (weekly)
    → Cloud Run Job (fetch API data)
        → Update Astro content/data files
            → Git commit + push
                → Vercel auto-deploy (rebuild)
```

**Data sources by sport:**

| Sport | API Provider | Competition Code | Endpoint |
|-------|-------------|-----------------|----------|
| EPL | Football-Data.org | `PL` | `/v4/competitions/PL/standings` |
| A-League | Football-Data.org (paid) or SportMonks | `ASL` | `/v4/competitions/ASL/standings` |
| World Cup | Football-Data.org | `WC` | `/v4/competitions/WC/standings` |
| AFL | TBD (not football) | — | — |
| NRL | TBD (not football) | — | — |
| Cricket | TBD (not football) | — | — |
| NBL | TBD (not football) | — | — |
| F1 | Ergast/Jolpica API (free) | — | `ergast.com/api/f1/current` |
| Tennis | TBD | — | — |
| UFC | TBD | — | — |

**Enforcement:** B-TECH (Tech Lead) + B-FORG (DataForge) own pipelines. W-IVAN (Architecture) validates.

---

### R-CONTENT-05d: "Last Updated" Display

**Requirement:** Every page that displays data from an external source (standings, fixtures, scores, rankings) MUST show a visible "Last Updated" timestamp.

**Format:** `Last updated: {DD Mon YYYY}` (e.g., "Last updated: 26 Feb 2026")

**Placement:** Below the page title or above the data table, clearly visible.

**Implementation (Astro):**
```astro
<p class="text-sm text-gray-500">Last updated: {lastUpdated}</p>
```

Where `lastUpdated` comes from:
- Frontmatter field in content collection, OR
- Generated timestamp from the data pipeline

**Enforcement:** B-MAX (UX/UI) owns display. W-MAYA (Accessibility) validates.

---

### R-CONTENT-05e: Off-Season Content Handling

**Requirement:** When a sport is in off-season:

1. **Standings** — Keep final season standings with label: "Final {year} season standings"
2. **Fixtures** — Replace with next season schedule if available, or: "{year} season schedule — to be announced {month}"
3. **Calendar** — Show next season dates if confirmed, or mark as TBC
4. **Rankings** — Keep current rankings (most sports update year-round)

**NEVER** leave off-season pages with in-season language ("being updated", "live", "this week's matches").

**Enforcement:** B-NINA (Content Strategy) owns messaging. W-VERA (Content QA) validates.

---

## Validation Checklist

```markdown
## R-CONTENT-05 FRESHNESS CHECKLIST
- [ ] R-CONTENT-05a: No false freshness claims (no "being updated" without pipeline)
- [ ] R-CONTENT-05b: Weekly stale content audit scheduled
- [ ] R-CONTENT-05c: Every data page has API pipeline, manual schedule, or honest labeling
- [ ] R-CONTENT-05d: "Last Updated" timestamp visible on all data pages
- [ ] R-CONTENT-05e: Off-season pages use correct language
```

---

## Integration with Existing Rules

| Rule | Interaction |
|------|------------|
| R-SEO-03i (thin content) | Stale fixture pages with only "TBC" may trigger thin content — enrich or noindex |
| R-SEO-04 (`contentAge`, `lastSignificantUpdate`) | Stale data pages hurt freshness signals in Google ranking |
| R-SEO-04 (`FreshnessTwiddler`) | Sports queries have high freshness intent — stale pages will rank poorly |
| R-CONTENT-04 (timestamp stagger) | Data pipeline commits should be separate from news article commits |
| R-AUDIT-01 (deep audit) | Weekly audit must verify actual data accuracy, not just presence |

---

## Enforcement Summary

| Sub-Rule | Owner (BlackTeam) | Validator (WhiteTeam) |
|----------|--------------------|-----------------------|
| R-CONTENT-05a | B-RANK | W-VERA |
| R-CONTENT-05b | B-TECH | W-IVAN |
| R-CONTENT-05c | B-TECH + B-FORG | W-IVAN |
| R-CONTENT-05d | B-MAX | W-MAYA |
| R-CONTENT-05e | B-NINA | W-VERA |

---

## Related Files

- **R-SEO-04:** `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md` — freshness signals in ranking
- **R-SEO-03:** `~/.claude/standards/ASTRO_TECHNICAL_SEO_RULES.md` — thin content mitigation
- **Sports API:** `~/paradise_brain/bedrock_agent/.../harvesters/sports.py` — Football-Data.org client
- **API Key:** `~/.keys/.env` → `FOOTBALL_DATA_API_KEY`

---

*Rule R-CONTENT-05 | Created 2026-02-26 | Source: australiafootball.com stale content audit*
*Approved by: B-BOB (BlackTeam Director) + W-WOL (WhiteTeam Director)*
