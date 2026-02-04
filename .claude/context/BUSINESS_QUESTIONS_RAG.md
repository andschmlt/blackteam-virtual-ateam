# Business Questions RAG Reference

**Purpose:** Quick-lookup reference for Pitaya, BI-Chatbot, and Virtual ATeam agents to answer business questions.

---

## MANDATORY: Use bi.reporting Schema ONLY

**Per MASTER_LIST v1.0 Rule R7:** `paradisemedia-bi.reporting.*` is the ONLY approved source.

**NEVER USE:** `bi_playground`, `lakehouse`, `analytics`, `testing`

### Core Tables for Business Questions

| Question Type | Primary Table | Key Columns |
|---------------|---------------|-------------|
| Revenue/FTDs | ARTICLE_PERFORMANCE | TOTAL_COMMISSION_USD, GOALS, CLICKS, SIGNUPS |
| Article info | ARTICLE_INFORMATION | TASK_ID, LIVE_URL, DOMAIN, VERTICAL, STATUS |
| Brand metrics | BRAND_PERFORMANCE | BRAND, FTD, CLICKS, TOTAL_COMMISSION_USD |
| High-level financials | FINANCIAL_REPORT | PROGRAM, BRAND, TOTAL_COMMISSION_USD |
| Costs | COSTS_INFORMATION | COST_USD, TYPE, DYNAMIC |
| Fixed fees | DIM_FIXED_FEE | FIXED_FEE_USD (join via LINK_FK) |
| SEO authority | REPT_SEO_AHREFS | DOMAIN_RATING, DOMAIN_BACKLINKS |
| Rankings | REPT_SEO_ACCURANKER | POSITION, KW_AI_DAILY_ORG_TRAFFIC |
| Production TAT | ARTICLE_CHANGELOG | STATUS, STATUS_START_DATE |

### Critical Join (Rule R9)

```sql
ARTICLE_INFORMATION.TASK_ID = ARTICLE_PERFORMANCE.DYNAMIC
```

---

## Quick Answer Lookup

### PERFORMANCE & REVENUE

**Q: Top 5% revenue generators?**
- Tables: ARTICLE_PERFORMANCE, FINANCIAL_REPORT
- Use PERCENT_RANK() with ORDER BY TOTAL_COMMISSION_USD
- Can filter by: articles, programs, brands, verticals

**Q: Average EPC/EPF by entity?**
- EPC = TOTAL_COMMISSION_USD / CLICKS
- EPF = TOTAL_COMMISSION_USD / GOALS (GOALS = FTDs)
- Tables: ARTICLE_PERFORMANCE, BRAND_PERFORMANCE

**Q: Best converting traffic sources?**
- PostHog: navboost:session_start → $referring_domain
- Gap: No direct link to BigQuery FTDs

**Q: ROI per article?**
- Revenue = Commission + Fixed Fees
- Costs = COSTS_INFORMATION by DYNAMIC
- ROI = (Revenue - Costs) / Costs

---

### CONTENT & SEO

**Q: High traffic, no conversions?**
- Ahrefs: REPT_SEO_AHREFS for traffic estimates
- BigQuery: ARTICLE_PERFORMANCE for GOALS
- JOIN on DOMAIN, filter WHERE GOALS = 0

**Q: Best converting keywords?**
- Use TARGET_KEYWORDS from ARTICLE_INFORMATION
- WARNING: DataForSEO keywords CANNOT link to revenue (Rule R21)

**Q: Low CTR affiliate links?**
- PostHog: navboost:cta_visible vs navboost:cta_click
- CTR = clicks / impressions

**Q: Best content formats?**
- Gap: No CONTENT_FORMAT field
- Workaround: Infer from URL patterns (best=Listicle, review=Review, etc.)

---

### TRAFFIC & BEHAVIOR

**Q: Traffic by geography/device?**
- PostHog: $geoip_country_name, $device_type
- Event: navboost:session_start

**Q: Best referral sources?**
- PostHog: $referring_domain
- Engagement: dwell_time, max_scroll_depth, outbound_click

**Q: Mobile vs desktop conversion?**
- PostHog: $device_type with outbound_click as proxy
- Gap: No direct FTD tracking by device

---

### AFFILIATE PROGRAMS

**Q: Highest margin programs?**
- Tables: FINANCIAL_REPORT
- Commission is NET (we receive net commission)

**Q: Underperforming programs?**
- Compare period-over-period growth
- Flag declining programs

**Q: Program term changes?**
- Gap: Not tracked
- Manual process needed

---

### SEO PERFORMANCE

**Q: Rankings/positions?**
- Table: REPT_SEO_ACCURANKER
- Fields: POSITION, KEYWORD, DOMAIN

**Q: Top 10/3/1 counts?**
```sql
COUNT(CASE WHEN POSITION <= 10 THEN 1 END) as TOP_10
COUNT(CASE WHEN POSITION <= 3 THEN 1 END) as TOP_3
COUNT(CASE WHEN POSITION = 1 THEN 1 END) as TOP_1
```

**Q: DR/backlinks?**
- Table: REPT_SEO_AHREFS
- Fields: DOMAIN_RATING, DOMAIN_BACKLINKS, DOMAIN_REFDOMAINS

---

### COSTS & ROI

**Q: Total costs?**
- Table: COSTS_INFORMATION
- Filter by TYPE: CONTENT, SP, GP, BACKLINK, etc.

**Q: SP cost per post?**
- Total SP Cost / Count of new posts

**Q: Break even / 3X / 10X ROI %?**
```sql
Break Even: REVENUE >= COSTS
3X ROI: REVENUE >= COSTS * 3
10X ROI: REVENUE >= COSTS * 10
```

---

### PRODUCTION

**Q: Articles published?**
- Table: ARTICLE_INFORMATION
- Filter: STATUS = 'LIVE', DATE_ID range

**Q: TAT (turnaround time)?**
- Table: ARTICLE_CHANGELOG
- Publisher TAT: READY_TO_PUBLISH → LIVE_NEEDS_QC
- Content TAT: SETUP → READY_TO_PUBLISH

**Q: Bottleneck status?**
```sql
SELECT FROM_STATUS, TO_STATUS, AVG(DAYS_IN_STATUS)
FROM ARTICLE_CHANGELOG
GROUP BY FROM_STATUS, TO_STATUS
ORDER BY AVG(DAYS_IN_STATUS) DESC
```

---

### BACKLINKS

**Q: Backlinks built?**
- Ahrefs: DOMAIN_BACKLINKS for total
- Costs: Filter TYPE IN ('GP', 'PBN', 'SP') for built links

**Q: Backlink spend?**
```sql
SELECT SUM(COST_USD) FROM COSTS_INFORMATION
WHERE TYPE IN ('GP', 'PBN', 'SP', 'BACKLINK')
```

---

## Key Formulas

| Metric | Formula | Source |
|--------|---------|--------|
| EPC | TOTAL_COMMISSION_USD / CLICKS | ARTICLE_PERFORMANCE |
| EPF | TOTAL_COMMISSION_USD / GOALS | ARTICLE_PERFORMANCE |
| CVR | GOALS / CLICKS | ARTICLE_PERFORMANCE |
| ROI | (Revenue - Costs) / Costs | AP + CI + FF |
| Total Revenue | Commission + Fixed Fees | AP + FF |
| Pogo Rate | Pogo sessions / Google sessions | PostHog |
| CTA CTR | CTA clicks / CTA visible | PostHog |

---

## Data Source Codes

| Code | Table | Use For |
|------|-------|---------|
| BQ-AP | reporting.ARTICLE_PERFORMANCE | Revenue, FTDs, clicks |
| BQ-AI | reporting.ARTICLE_INFORMATION | Article metadata |
| BQ-BP | reporting.BRAND_PERFORMANCE | Brand metrics |
| BQ-FR | reporting.FINANCIAL_REPORT | High-level financials |
| BQ-CI | reporting.COSTS_INFORMATION | Costs |
| BQ-FF | reporting.DIM_FIXED_FEE | Fixed fees |
| BQ-AR | reporting.REPT_SEO_ACCURANKER | Rankings |
| BQ-AH | reporting.REPT_SEO_AHREFS | DR, backlinks |
| BQ-AC | reporting.ARTICLE_CHANGELOG | Production TAT |
| PH | PostHog Events | User behavior |
| DF | DataForSEO API | Live SEO data |

---

## Critical Rules

1. **GOALS = FTDs** in ARTICLE_PERFORMANCE
2. **TASK_ID = DYNAMIC** for joins
3. **Never use lakehouse** - only reporting schema
4. **DataForSEO keywords ≠ revenue** - no join possible
5. **DATE_ID format = YYYYMMDD** (integer)

---

## Known Data Gaps

| Question Type | Gap | Workaround |
|---------------|-----|------------|
| Traffic source conversion | No PostHog-BQ link | Use affiliate clicks as proxy |
| Content format | No field | Infer from URL |
| Device conversion | No device in BQ | PostHog clicks only |
| Uptime monitoring | Not tracked | Manual/external |
| Deals metrics | Limited in BQ | ClickUp custom fields |

---

*RAG Reference v1.0 | Compliant with MASTER_LIST v1.0*
