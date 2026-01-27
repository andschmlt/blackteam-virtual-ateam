# SEO & Performance Analysis Framework

**Rule ID:** BLACKTEAM-SEO-001
**Created:** 2026-01-26
**Status:** ACTIVE - MANDATORY
**Applies To:** All SEO, Article, and Domain Performance Analysis Requests

---

## HARD RULES

### Rule 1: Data Source
**ONLY use BigQuery** (paradisemedia-bi project) - NO lakehouse

### Rule 2: Vertical Exclusions
**EXCLUDE from ALL analyses:**
- Adult vertical
- Growth vertical
- Any non-iGaming vertical (unless explicitly requested)

### Rule 3: Default Vertical
**Default to iGaming** for all analysis unless user specifies otherwise

---

## MANDATORY THEORY TESTING

**HARD RULE:** When ANY analysis request involves SEO, articles, domain performance, FTDs, conversions, or traffic - the following THREE THEORIES must be tested and reported on.

---

## THEORY 1: CONTENT GAP ANALYSIS

### What to Test
- Are the RIGHT pages being created vs what's in Airtable Topics DB?
- Is there sufficient content volume on the sites?
- Cross-reference published content against Airtable approved topics

### Data Sources (BigQuery)
- `paradisemedia-bi.analytics.ARTICLE_PERFORMANCE` - Published content
- Airtable Topics DB - Approved topics (external)

### Query Template
```sql
SELECT 
    DOMAIN,
    COUNT(DISTINCT DYNAMIC) as published_articles,
    COUNT(DISTINCT URL) as unique_urls,
    SUM(CONVERSIONS) as total_ftds
FROM `paradisemedia-bi.analytics.ARTICLE_PERFORMANCE`
WHERE VERTICAL = 'iGaming'  -- EXCLUDE Adult, Growth
  AND DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
GROUP BY 1
ORDER BY total_ftds DESC
```

### Metrics to Report
| Metric | How to Calculate |
|--------|------------------|
| Published Articles | COUNT(DISTINCT DYNAMIC) |
| Active Domains | COUNT(DISTINCT DOMAIN) |
| Content Coverage | Published / Approved Topics |

### Status Options
- **VALIDATED** - Content matches approved topics
- **GAP IDENTIFIED** - Missing content found
- **PENDING** - Requires Airtable cross-reference

---

## THEORY 2: RANKING/SEO ISSUES

### What to Test
- Are pages ranking for target keywords?
- What is the average rank position?
- Are there backlink/authority issues?

### Data Source (BigQuery)
```sql
SELECT 
    DOMAIN,
    AVG(RANK) as avg_rank,
    SUM(CASE WHEN RANK <= 10 THEN 1 ELSE 0 END) as top10_keywords,
    AVG(DOMAIN_RATING) as domain_rating,
    SUM(DOMAIN_BACKLINKS) as backlinks,
    SUM(PAGE_ORG_TRAFFIC) as total_traffic
FROM `paradisemedia-bi.reporting.REPT_SEO_AHREFS`
WHERE VERTICAL = 'iGaming'  -- EXCLUDE Adult, Growth
  AND LAST_MONTH_DATE = TRUE
GROUP BY 1
HAVING COUNT(DISTINCT KEYWORD) >= 10
ORDER BY total_traffic DESC
```

### Metrics to Report
| Metric | Threshold | Status |
|--------|-----------|--------|
| Avg Rank | ≤20 = Good, >30 = Poor | Required |
| Domain Rating | ≥50 = Good | Required |
| Top 10 Keywords | Trending up = Good | Required |

### Status Options
- **NO ISSUE** - Rankings healthy (avg ≤20)
- **PARTIAL ISSUE** - Some domains need work (avg 20-40)
- **CRITICAL** - Rankings blocking growth (avg >40)

### Benchmark (iGaming Jan 2026)
| Ranking Tier | % of Domains |
|--------------|--------------|
| Good (≤20) | 13% |
| Moderate (20-30) | 20% |
| Poor (>30) | 67% |

---

## THEORY 3: AI SEARCH MARKET SHARE

### What to Test
- Is AI capturing search traffic?
- What percentage of organic traffic is AI-attributed?
- Are estimated traffic and actual FTDs diverging?

### Data Source (BigQuery)
```sql
SELECT 
    DOMAIN,
    SUM(KW_ORG_TRAFFIC) as total_org_traffic,
    SUM(KW_AI_DAILY_ORG_TRAFFIC) as ai_traffic,
    SAFE_DIVIDE(SUM(KW_AI_DAILY_ORG_TRAFFIC), SUM(KW_ORG_TRAFFIC)) * 100 as ai_traffic_pct,
    SUM(TRAFFIC_POTENTIAL) as traffic_potential
FROM `paradisemedia-bi.reporting.REPT_SEO_ACCURANKER`
WHERE VERTICAL = 'iGaming'  -- EXCLUDE Adult, Growth
  AND LAST_MONTH_DATE = TRUE
GROUP BY 1
HAVING total_org_traffic > 100
ORDER BY ai_traffic_pct DESC
```

### Metrics to Report
| Metric | Threshold | Status |
|--------|-----------|--------|
| AI Traffic % | <20% = Low, >50% = Critical | Required |
| Domains with AI >100% | Count | Required |

### Status Options
- **LOW IMPACT** - AI capture <20%
- **MODERATE IMPACT** - AI capture 20-50%
- **CRITICAL** - AI capture >50%

### Benchmark Reference
| Vertical | AI Traffic % | Status |
|----------|-------------|--------|
| **iGaming** | **10.3%** | LOW - Protected |
| Adult | 75%+ | CRITICAL (excluded) |

---

## REPORT TEMPLATE (MANDATORY)

Every SEO/Performance analysis MUST include:

```markdown
## THEORY VALIDATION

### Theory 1: Content Gap
| Status | [STATUS] |
|--------|----------|
| Finding | [Brief finding] |
| Data | BigQuery ARTICLE_PERFORMANCE |

### Theory 2: Ranking/SEO
| Status | [STATUS] |
|--------|----------|
| Avg Rank | [X] |
| Domain Rating | [X] |
| Top 10 KWs | [X] |
| Data | BigQuery REPT_SEO_AHREFS |

### Theory 3: AI Search Impact
| Status | [STATUS] |
|--------|----------|
| AI Traffic % | [X]% |
| Data | BigQuery REPT_SEO_ACCURANKER |
```

---

## VERTICAL FILTER (MANDATORY)

**Always include this WHERE clause:**
```sql
WHERE VERTICAL = 'iGaming'
-- OR for explicit request:
WHERE VERTICAL IN ('iGaming', 'Technology', 'Finance')
-- NEVER include:
-- AND VERTICAL NOT IN ('Adult', 'Growth', 'Growth NA')
```

---

## PERSONAS RESPONSIBLE

| Persona | Role |
|---------|------|
| **Elias Thorne** | Run queries, primary analysis |
| **SEO Commander** | Interpret rankings, recommend actions |
| **Data Analyst** | Validate data, cross-reference |
| **Director** | Verify all 3 theories addressed |

---

## ENFORCEMENT

1. **Director** verifies all 3 theories before approving report
2. Missing theory = incomplete = rejected
3. **BigQuery ONLY** - no lakehouse
4. **iGaming default** - exclude Adult/Growth
5. All queries must include vertical filter

---

*Framework created by BlackTeam*
*Based on BT-2026-012 FTD Analysis*
*Date: 2026-01-26*
