# /seo_audit_engine - Technical SEO Audit Orchestrator

Run comprehensive technical SEO audits using R-SEO-03 (Astro Technical SEO), R-SEO-04 (Google API Leak Diagnosis), and R-CSS-01 (CSS validation).

## Arguments

Arguments: $ARGUMENTS

---

## Standards Enforced

- **R-SEO-03:** 9 sub-rules (a-i) from Screaming Frog audit
- **R-SEO-04:** Google API leak diagnosis (3 tiers)
- **R-CSS-01:** No :global() in imported CSS files
- **R-SEO-02:** astro-seo package, OG tags, Twitter Cards, canonical URLs

---

## Modes

### 1. `full` — Complete Technical SEO Audit

Runs all checks against target site. Default mode.

**Phase 1: Build & Static Analysis**

```bash
# Build the site
cd ~/[site-directory] && npm run build

# Check for :global() leaks in built CSS (R-CSS-01)
grep -r ":global" dist/_astro/*.css

# Count pages in sitemap vs built HTML
find dist -name "*.html" | wc -l
```

**Phase 2: R-SEO-03 Sub-Rules (9 checks)**

| Rule | Check | Command/Method |
|------|-------|----------------|
| **a) Trailing slash** | All internal links end with `/` | `grep -rn 'href="/' src/ --include="*.astro" --include="*.md"` — filter missing trailing slashes |
| **b) No hotlinking** | All images self-hosted | `grep -rn 'src="http' src/ --include="*.astro" --include="*.md"` — flag external image URLs |
| **c) Title budget** | Titles 50-60 chars | Extract all `<title>` from built HTML, measure length |
| **d) Meta descriptions** | 120-160 chars, unique | Extract meta descriptions, check length + uniqueness |
| **e) OG type** | Correct og:type per page | Articles = `article`, pages = `website` |
| **f) Nav budget** | Max links in navigation | Count `<nav>` links in built HTML |
| **g) Schema consistency** | JSON-LD matches page content | Validate structured data against page |
| **h) Sitemap parity** | sitemap.xml matches built pages | Compare sitemap URLs vs. `dist/*.html` files |
| **i) Thin content** | Pages >200 words | Extract text content, count words per page |

**Phase 3: R-SEO-02 Compliance**

```bash
# Check astro-seo is installed
grep "astro-seo" package.json

# Verify OG tags in built HTML (sample 5 pages)
grep -l "og:title\|og:type\|og:image" dist/**/*.html | head -5

# Verify Twitter Cards
grep -l "twitter:card" dist/**/*.html | head -5

# Verify canonical URLs
grep -l "canonical" dist/**/*.html | head -5
```

**Phase 4: R-CSS-01 Validation**

```bash
# Check source CSS files for :global() (INVALID in standalone .css)
grep -rn ":global(" src/**/*.css

# Check Astro style blocks (VALID usage)
grep -rn ":global(" src/**/*.astro

# Verify built CSS has no leaked :global()
grep ":global(" dist/_astro/*.css
```

**Phase 5: Output Report**

```markdown
## Technical SEO Audit Report

**Site:** [domain]
**Date:** [today]
**Build Status:** [pass/fail]
**Pages Audited:** [count]

### R-SEO-03 Results (9 sub-rules)

| Rule | Status | Issues | Details |
|------|--------|--------|---------|
| a) Trailing slash | PASS/FAIL | [count] | [details] |
| b) No hotlinking | PASS/FAIL | [count] | [details] |
| c) Title budget | PASS/FAIL | [count] | [over/under budget titles] |
| d) Meta descriptions | PASS/FAIL | [count] | [missing/wrong length] |
| e) OG type | PASS/FAIL | [count] | [mismatched types] |
| f) Nav budget | PASS/FAIL | [count] | [excess links] |
| g) Schema consistency | PASS/FAIL | [count] | [mismatches] |
| h) Sitemap parity | PASS/FAIL | [count] | [orphans/missing] |
| i) Thin content | PASS/FAIL | [count] | [pages <200 words] |

### R-SEO-02 Compliance
- [ ] astro-seo installed
- [ ] OG tags present (title, type, image, image.alt)
- [ ] Twitter Cards configured (summary_large_image)
- [ ] Canonical URLs set
- [ ] JSON-LD structured data present

### R-CSS-01 Validation
- [ ] No :global() in standalone .css files
- [ ] Built CSS clean (no leaked :global)
- [ ] Scoped :global() in .astro files only

### Score: [X]/100

### Priority Fixes
1. [P0] [specific issue + file path]
2. [P1] [specific issue + file path]
```

---

### 2. `diagnose` — Traffic Drop Diagnosis (R-SEO-04)

Use the Google API Leak Diagnosis Framework when traffic drops are detected.

**Triggers:**
- >10% traffic drop: Run Tier 1 + Tier 2
- >25% traffic drop: Run Tier 1-3 + comparison analysis
- Google core update: Focus on Panda/authority/NavBoost parameters
- Monthly routine: Tier 1 quick-check only

**Tier 1 — Content Quality & NavBoost:**
1. Check PostHog NavBoost metrics:
   - `goodClicks` (dwell time) — users staying?
   - `badClicks` (pogo-sticking) — users bouncing immediately?
   - `serpDemotion` — SERP return rate
2. Content freshness audit (R-CONTENT-05 thresholds)
3. Link spam indicators
4. Thin content scan (<200 words)

**Tier 2 — Technical & Crawl:**
1. Crawl budget analysis (sitemap size, orphan pages)
2. Core Web Vitals (if Lighthouse available)
3. Mobile usability
4. YMYL signals (if applicable)

**Tier 3 — Entity & Link Network:**
1. Entity authority signals
2. Link network analysis (internal + external)
3. Commercial intent alignment

**Output:** Diagnosis report with recommended actions per tier.

---

### 3. `quick` — Quick Health Check

Fast scan of critical issues only:
- Sitemap parity (h)
- Trailing slashes (a)
- Title budget (c)
- :global() leaks (R-CSS-01)

---

### 4. `fix` — Auto-Fix Common Issues

Auto-fix specific categories:
- `fix trailing-slash` — Add missing trailing slashes
- `fix titles` — Trim titles to 60 chars
- `fix meta` — Generate missing meta descriptions
- `fix css` — Remove :global() from .css files

---

## Team Assignments

| Persona | Role |
|---------|------|
| B-RANK | Runs audit, prioritizes fixes |
| B-TECH | Technical implementation of fixes |
| W-LUNA | Validates SEO audit results |
| W-EVAN | Validates compliance (white hat) |
| W-IVAN | Validates technical fixes |

---

## Integration Points

- **PostHog:** NavBoost metrics for traffic diagnosis
- **Screaming Frog:** External crawl data (when available)
- **Google Search Console:** Indexing + performance data
- **`/anchor_manager`:** Anchor text validation (R-ANCHOR-01/02)
- **`/launch_site`:** Phase 8B baseline check uses this engine

---

## Quality Gates

- [ ] All 9 R-SEO-03 sub-rules checked
- [ ] R-SEO-02 compliance verified
- [ ] R-CSS-01 no :global() leaks
- [ ] Score calculated out of 100
- [ ] Priority fixes listed with file paths
- [ ] R-AUDIT-01 depth: source-level verification, not surface checks

---

**Version:** 1.0.0
**Created:** 2026-03-02
