# MASTER LIST v1.0 - Data Source Architecture

## Paradise Media BI - Approved Data Sources
**Version:** 1.2 | **Date:** 2026-02-13 | **Status:** APPROVED | **Owner:** Andre

---

## ⚠️ GOVERNANCE RULES (MANDATORY)

### RULE G1: MASTER LIST COMPLIANCE (CRITICAL)

| Role | Requirement |
|------|-------------|
| **WOL (WhiteTeam Head of Tech)** | MUST always reference this Master List. NEVER assume, change, or go beyond this document without Andre's approval |
| **BOB (BlackTeam Head of Tech)** | MUST always reference this Master List. NEVER assume, change, or go beyond this document without Andre's approval |
| **QA Team** | MUST validate all SQL and data model references against this Master List. Any deviation = FAIL review |
| **Directors** | MUST ensure all data catalog references follow these rules. Non-compliance = FAIL task review |

### RULE G2: NO ASSUMPTIONS

- **NEVER** assume data relationships not documented here
- **NEVER** invent joins or mappings not in this Master List
- **NEVER** modify queries without referencing approved patterns
- **ALWAYS** fail reviews for tasks that violate these rules

### RULE G3: CHANGE CONTROL

- Any changes to this Master List require **Andre's explicit approval**
- Proposed changes must be documented and reviewed before implementation
- Unapproved changes = automatic task failure

---

## SECTION 1: BigQuery - paradisemedia-bi.reporting (LEGACY — use summary schema instead)

### Approved Tables (10)

| # | Table | Purpose | Row Count | Scope | Keywords |
|---|-------|---------|-----------|-------|----------|
| 1 | **ARTICLE_PERFORMANCE** | Affiliate revenue per article - clicks, signups, conversions | 6,952,728 | Use when users ask for article or URL performance | URL, Article, Task ID, Daily, Monthly, Weekly, Date range, Period, Clicks, Signups, FTDs, Conversions, Goals, EPF, Article with Brand performance |
| 2 | **ARTICLE_INFORMATION** | Production management of the Article - statuses, site manager, content team, word count, published date, last updated date | 52,305 | Dimension table - any requests for information inside the article should come from here | Article information, URL, Status, Publishing, Content team, Content, Live_URL, Vertical, Geo targeting, Target keywords, ClickUp |
| 3 | **BRAND_PERFORMANCE** | Brand-level metrics - clicks, FTD, revenue | 320,519 | Secondary table - use for brand/program generic questions without detail. Can join with ARTICLE_INFORMATION or ARTICLE_PERFORMANCE. Last resort or QA cross-check at high level | Brand analysis, Program analysis, High level overview of revenue metrics |
| 4 | **COSTS_INFORMATION** | Article/link costs - payments, assignments | 150,827 | Central hub for costs at domain or article/taskid/dynamic level. Crucial for ROI whenever user asks for costs information | Costs, Spent, Spending |
| 5 | **FINANCIAL_REPORT** | Financial data - revenue, commissions by program/brand (Voonix source) | 1,038,801 | PRIMARY source for high level performance (Month, Week, Quarter, YTD, MTD, WTD). Most accurate revenue metrics - used by Financial Team (the bible). Lacks URL/Domain level data | Brand Analysis, Program Analysis, Financial Analysis, Revenue Analysis, High Level Analysis, Commission Analysis |
| 6 | **CLOAKING_TRAFFIC** | Only source for clickout data - stores all clicks users make from pages redirecting to casino/partner pages | 12,387,164 | Use for cloaking data, redirections, @dragon references in ClickUp. Analyze broken cloaking/tracking links, 404 errors. Crucial for cloaking analysis and conversion tracking | Cloaking, Redirect, Tracking, Dragon |
| 7 | **DIM_BRAND** | Brand as a dimension - brand names and identifiers | 3,308 | Dimension table - use for getting brand names only. Limited use beyond name lookups | Brand name, Program name, Brand information |
| 8 | **DIM_VERTICAL** | Data hierarchy for Vertical > Niche > Sub-Niche | 731 | Dimension table - used in all BI reporting. Can be joined with ARTICLE_INFORMATION or ClickUp data | Vertical, Vertical Analysis, Niche, Sub-Niche, Niche analysis, Sub-Niche Analysis, Keywords by Niche, Keywords by Vertical, Keywords by Sub-Niche |
| 9 | **DIM_DATE** | Date dimension for time-based analysis | 3,653 | Dimension table - standard date dimension for all date filtering and period analysis | Date ID, From Date, To Date, Month, MTD, YTD, Last quarter, Last month, LY, Last year, All time, Time, Date Period |
| 10 | **DIM_FIXED_FEE** | Fixed fee agreements and amounts | 873 | Source for Fixed Fee data. Join via COSTS_INFORMATION (SOURCE='FIXED_FEES') using LINK_FK = FIXED_FEE_SK | Fixed fees, Fixed fee agreements, Fee amount, Monthly fees |

---

## SECTION 1B: BigQuery - paradisemedia-bi.summary (SUPPLEMENTARY)

**Added:** 2026-02-11 | **Updated:** 2026-02-13 | **Status:** APPROVED (7 of 7 tables) | **Approved By:** Andre

> **NOTE:** The `summary` schema is a denormalized reporting layer optimised for LLM/chatbot
> consumption. It pre-joins dimensions and consolidates sources. Uses native `DATE` type (not
> `DATE_ID` integers) and `FLOAT64` for monetary fields (not `NUMERIC`). Refreshed daily.
> See rules R22-R27 below.
>
> **Source documentation:** `BI-REPO-PARADISEMEDIA/exports/chatbot/CHATBOT_TABLES_DOCUMENTATION.md`

### Approved Tables (7)

| # | Table | Grain | Purpose | Scope | Keywords |
|---|-------|-------|---------|-------|----------|
| 1 | **ARTICLE_PERFORMANCE** | Article × Brand × Program × Date | Article-level revenue with full brand/program attribution. Fixes the old `sfmax("BRAND_FK")` brand misattribution bug. Multiple rows per article per day (one per brand/program) | Use for article revenue analysis. Aggregate across brands for article totals. Join to ARTICLE_SEO/ARTICLE_INVOICES via ARTICLE_KEY + DATE | Article revenue, Brand attribution, FTD, EPC, EPF, Clicks, Commission |
| 2 | **ARTICLE_SEO** | Article × Date | Article-level Core Web Vitals (LCP, INP, CLS) and Google Analytics metrics (sessions, users, bounces, engagement) | Companion to ARTICLE_PERFORMANCE. SEO metrics are article-level, not brand-level | CWV, Core Web Vitals, GA sessions, Bounce rate, LCP, INP, CLS |
| 3 | **ARTICLE_INVOICES** | Article × Payment Date | Article-level costs split by DLC, ClickUp Invoice, and Fixed Fee. Date is DATE_PAID, not invoice creation date | Use for article cost/ROI analysis. TOTAL_ARTICLE_COST_USD = DLC + ClickUp (excludes Fixed Fee) | Costs, DLC, Invoice, Fixed Fee, ROI |
| 4 | **BRAND_PERFORMANCE** | Brand × Date | Brand-level metrics - clicks, FTD, commission, EPC, EPF (pre-calculated). Standalone — NO joins to articles or domains | Use for brand/program analysis only. Cannot be linked to articles or domains | Brand analysis, Program analysis, EPF, EPC |
| 5 | **DOMAIN_PERFORMANCE** | Domain × Date | Domain-level daily metrics - separate iGaming + Growth columns, GA, CWV, costs, article counts (consolidated) | **PRIMARY for domain-level queries** — replaces multi-table joins. Splits iGaming vs Growth metrics. Includes acquisition costs | Domain analysis, Domain performance, Domain ROI, GA sessions |
| 6 | **PRODUCTION_CYCLE** | Task × Status Change | Article production workflow - status changes, cycle times, production stage mapping | Track article lifecycle. PRODUCTION_CYCLE integer = revision count. Current status has NULL MINUTES_IN_STATUS | Production, TAT, Status changes, Workflow, Bottleneck |
| 7 | **SEO_PERFORMANCE** | Keyword × Article × Date × Device × Country | Consolidated SEO - GSC + Accuranker + Ahrefs in single table. Metrics prefixed by source (GSC_*, ACCURANKER_*, AHREFS_*) | Consolidates 3 SEO sources. Not all keywords have data from all sources | SEO, Rankings, Keywords, Traffic, Backlinks |

### Summary Schema Table Details

#### Table 1: ARTICLE_PERFORMANCE — Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `ARTICLE_KEY` | INTEGER | Surrogate key — join to ARTICLE_SEO, ARTICLE_INVOICES, SEO_PERFORMANCE |
| `DOMAIN_KEY` | INTEGER | Surrogate key — join to DOMAIN_PERFORMANCE |
| `DATE` | DATE | Calendar date (YYYY-MM-DD) |
| `TASK_ID` | STRING | ClickUp task ID (= reporting.DYNAMIC) |
| `BRAND` | STRING | Affiliate brand name (each brand = separate row) |
| `PROGRAM` | STRING | Affiliate program/network |
| `VERTICAL` | STRING | "iGaming" or "Growth" |
| `CLICKS` | INTEGER | Affiliate link clicks |
| `NRC` | INTEGER | New Registered Customers |
| `FTD` | INTEGER | First Time Depositors (Growth = 0) |
| `DEPOSIT_VALUE_USD` | NUMERIC | Total deposit value |
| `NET_REVENUE_USD` | NUMERIC | Net revenue after deductions |
| `CPA_COMMISSION_USD` | FLOAT | CPA commission |
| `REVSHARE_COMMISSION_USD` | FLOAT | Revenue share commission |
| `TOTAL_COMMISSION_USD` | NUMERIC | CPA + RevShare combined |
| `EPC_USD` | FLOAT | Earnings Per Click |
| `EPF_USD` | FLOAT | Earnings Per FTD |

#### Table 2: ARTICLE_SEO — Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `ARTICLE_KEY` + `DATE` | PK | Article × Date grain |
| `LCP_AVG` | FLOAT | Largest Contentful Paint (ms). Good: < 2500ms |
| `INP_AVG` | FLOAT | Interaction to Next Paint (ms). Good: < 200ms |
| `CLS_AVG` | FLOAT | Cumulative Layout Shift. Good: < 0.1 |
| `GA_SESSIONS` | INTEGER | Google Analytics sessions |
| `GA_TOTAL_USERS` | INTEGER | Unique visitors |
| `GA_PAGE_VIEWS` | INTEGER | Page view count |
| `GA_BOUNCES` | INTEGER | Bounced sessions |
| `GA_AVG_ENGAGEMENT_TIME` | NUMERIC | Avg engagement time (seconds) |

#### Table 3: ARTICLE_INVOICES — Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `ARTICLE_KEY` + `DATE` | PK | Article × Payment Date grain |
| `DLC_COST_USD` | NUMERIC | External content provider costs |
| `CLICKUP_INVOICE_COST_USD` | NUMERIC | Internal production costs |
| `FIXED_FEE_EARNINGS_USD` | NUMERIC | Monthly retainer earnings |
| `TOTAL_ARTICLE_COST_USD` | NUMERIC | DLC + ClickUp (excludes Fixed Fee) |

### Cross-Table Join Keys (summary schema)

| Table A | Join Column(s) | Table B | Join Column(s) | Relationship |
|---------|----------------|---------|----------------|--------------|
| ARTICLE_PERFORMANCE | `ARTICLE_KEY` + `DATE` | ARTICLE_SEO | `ARTICLE_KEY` + `DATE` | Many:1 (multi-brand → single article-date) |
| ARTICLE_PERFORMANCE | `ARTICLE_KEY` + `DATE` | ARTICLE_INVOICES | `ARTICLE_KEY` + `DATE` | Many:1 (multi-brand → single article-date) |
| ARTICLE_PERFORMANCE | `TASK_ID` | PRODUCTION_CYCLE | `TASK_ID` | Many:Many (brands × status changes) |
| ARTICLE_PERFORMANCE | `DOMAIN_KEY` | DOMAIN_PERFORMANCE | `DOMAIN_KEY` | Many:1 (articles → domain) |
| ARTICLE_PERFORMANCE | `ARTICLE_KEY` | SEO_PERFORMANCE | `ARTICLE_KEY` | Many:Many (brands × keywords) |
| ARTICLE_SEO | `ARTICLE_KEY` + `DATE` | ARTICLE_INVOICES | `ARTICLE_KEY` + `DATE` | 1:1 (different date coverage) |
| ARTICLE_SEO | `DOMAIN_KEY` | DOMAIN_PERFORMANCE | `DOMAIN_KEY` | Many:1 (articles → domain) |
| SEO_PERFORMANCE | `DOMAIN_KEY` | DOMAIN_PERFORMANCE | `DOMAIN_KEY` | Many:1 (keywords → domain) |
| PRODUCTION_CYCLE | `PRODUCT_KEY` | DOMAIN_PERFORMANCE | `DOMAIN_KEY` | Many:1 (status changes → domain) |
| BRAND_PERFORMANCE | — | (No joins) | — | **Standalone** — cannot link to articles/domains |

### Default Query Filters (summary schema)

**Always apply these filters unless the user explicitly asks to include:**

1. **Exclude internal pages:** `WHERE LIVE_URL NOT LIKE '%paradisemedia.com%'`
2. **Exclude placeholders:** `AND LIVE_URL != 'https://Not Applicable'`

### Key Column Mappings (summary vs reporting)

| summary Column | reporting Equivalent | Notes |
|----------------|---------------------|-------|
| `DATE` (DATE type) | `DATE_ID` (INT64 YYYYMMDD) | **R22**: Use `DATE >= '2026-01-01'` format, NOT `DATE_ID >= 20260101` |
| `TASK_ID` | `DYNAMIC` | Same data, cleaner name |
| `ARTICLE_KEY` | No equivalent | Surrogate key in summary — primary join key |
| `DOMAIN_KEY` | No equivalent | Surrogate key in summary — primary join key |
| `FTD` | `FTD` (BRAND_PERF) / `GOALS` (ARTICLE_PERF) | Consistent naming in summary |
| `IGAMING_FTD` | Derived from VERTICAL filter | DOMAIN_PERFORMANCE pre-splits by vertical |
| `PRODUCTION_STAGE` | `PRODUCTION_CYCLE_STATUS` | Renamed in summary |
| `ARTICLE_STATUS_START_DATE` | `STATUS_START_DATE` | Renamed in summary |
| `NRC` | `SIGNUPS` | New Registered Customers = Signups |
| `PRODUCT_KEY` | No equivalent | Same as DOMAIN_KEY in PRODUCTION_CYCLE |

---

## SECTION 2: Column Definitions & Rules

### Key Columns

| # | Column | Table(s) | Data Type | Definition | Rule ID |
|---|--------|----------|-----------|------------|---------|
| 1 | **GOALS** | ARTICLE_PERFORMANCE | INT | First Time Depositors (FTDs) - users who made their first deposit | **R1** |
| 2 | **FTD** | BRAND_PERFORMANCE | INT | First Time Depositors (same as GOALS) | **R1** |
| 3 | **SIGNUPS** | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE | INT | New user registrations (accounts created) | |
| 4 | **CLICKS** | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE, CLOAKING_TRAFFIC | INT | Affiliate tracking clicks | |
| 5 | **DYNAMIC** | ARTICLE_PERFORMANCE, COSTS_INFORMATION, CLOAKING_TRAFFIC | STRING | ClickUp Task ID - business key for article tracking | **R2** |
| 6 | **TASK_ID** | ARTICLE_INFORMATION | STRING | ClickUp Task ID (same as DYNAMIC) | **R2** |
| 7 | **TOTAL_COMMISSION_USD** | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE, FINANCIAL_REPORT | DECIMAL | Total commission in USD (NP + LP combined) | |
| 8 | **TOTAL_COMMISSION_USD_NP** | ARTICLE_PERFORMANCE | DECIMAL | Commission from **New Player** data split | **R3** |
| 9 | **TOTAL_COMMISSION_USD_LP** | ARTICLE_PERFORMANCE | DECIMAL | Commission from **Legacy Player** data split | **R4** |
| 10 | **EPC** | ARTICLE_PERFORMANCE | DECIMAL | Earnings Per Click (TOTAL_COMMISSION_USD / CLICKS) | |
| 11 | **EPF** | Calculated | DECIMAL | Earnings Per FTD (TOTAL_COMMISSION_USD / GOALS) | **R5** |
| 12 | **DATE_ID** | All fact tables | INT | Date dimension key in YYYYMMDD format | **R6** |
| 13 | **LIVE_URL** | ARTICLE_INFORMATION, COSTS_INFORMATION | STRING | Published URL of the article | |
| 14 | **STATUS** | ARTICLE_INFORMATION | STRING | Current article status | |
| 15 | **VERTICAL** | ARTICLE_INFORMATION, DIM_VERTICAL | STRING | Top-level business vertical | |
| 16 | **NICHE** | ARTICLE_INFORMATION, DIM_VERTICAL | STRING | Niche category | |
| 17 | **SUB_NICHE** | ARTICLE_INFORMATION, DIM_VERTICAL | STRING | Sub-niche category | |
| 18 | **DOMAIN** | Multiple tables | STRING | Domain name | |
| 19 | **BRAND** | BRAND_PERFORMANCE, FINANCIAL_REPORT, DIM_BRAND | STRING | Brand name | |
| 20 | **COST_USD** | COSTS_INFORMATION | DECIMAL | Cost/spending amount in USD | |
| 21 | **TYPE** | COSTS_INFORMATION | STRING | Cost type classification | |
| 22 | **SOURCE** | COSTS_INFORMATION | STRING | Source type filter (e.g., "FIXED_FEES") | **R12** |
| 23 | **LINK_FK** | COSTS_INFORMATION | BIGINT | Foreign key to link to DIM_FIXED_FEE | **R12** |
| 24 | **FIXED_FEE_SK** | DIM_FIXED_FEE | BIGINT | Surrogate key for fixed fee record | **R12** |
| 25 | **FIXED_FEE_USD** | DIM_FIXED_FEE | DECIMAL | Fixed fee payment amount in USD | |

---

## SECTION 3: Business Rules

### Data Rules

| Rule ID | Rule Name | Description |
|---------|-----------|-------------|
| **R1** | FTDs = GOALS | In ARTICLE_PERFORMANCE, FTDs are stored in the GOALS column. In BRAND_PERFORMANCE, use FTD column |
| **R2** | DYNAMIC = Task ID | DYNAMIC field = ClickUp Task ID. Use for exact task matching |
| **R3** | Commission NP | `TOTAL_COMMISSION_USD_NP` = New Player commission split |
| **R4** | Commission LP | `TOTAL_COMMISSION_USD_LP` = Legacy Player commission split |
| **R5** | EPF Calculation | EPF = `TOTAL_COMMISSION_USD / GOALS` |
| **R6** | Date Format | DATE_ID format is YYYYMMDD integer (e.g., 20260202) |
| **R7** | Schema Rule | Use `paradisemedia-bi.summary` ONLY - **NEVER use lakehouse or reporting** |
| **R8** | Task-Level Analysis | Always query at TASK_ID level for /tasks_ROI, NOT domain or keyword level |
| **R9** | Join Key | ARTICLE_INFORMATION.TASK_ID = ARTICLE_PERFORMANCE.DYNAMIC |
| **R10** | Commission Tables | Commission data comes from ARTICLE_PERFORMANCE, BRAND_PERFORMANCE, FINANCIAL_REPORT |
| **R11** | Total Revenue | Total Revenue = Commission + Fixed Fees |
| **R12** | Fixed Fee Join | To get Fixed Fees at article/URL/dynamic level: Filter COSTS_INFORMATION WHERE SOURCE = 'FIXED_FEES', then JOIN on LINK_FK = DIM_FIXED_FEE.FIXED_FEE_SK |

### Summary Schema Rules

| Rule ID | Rule Name | Description |
|---------|-----------|-------------|
| **R22** | Summary Date Format | Summary tables use native `DATE` type (`'2026-01-15'`). Use `WHERE DATE >= '...'` format. **NEVER** mix DATE_ID integers with summary table queries |
| **R23** | Summary FLOAT64 Warning | Summary monetary columns use FLOAT64 (not NUMERIC). Accept up to 0.05% variance in cross-validation. For exact financial totals, prefer `reporting.FINANCIAL_REPORT` |
| **R24** | Summary ARTICLE_PERFORMANCE Grain | `summary.ARTICLE_PERFORMANCE` has **multiple rows per article per day** (one per Brand × Program). When joining to single-grain tables (ARTICLE_SEO, ARTICLE_INVOICES), **always aggregate revenue first** via `SUM(...) GROUP BY ARTICLE_KEY, DATE`. The old sfmax brand bug is fixed — this table now preserves correct brand attribution |
| **R25** | Summary Domain Priority | For domain-level aggregations, prefer `summary.DOMAIN_PERFORMANCE` over building from base reporting tables. It pre-joins iGaming revenue, GA, CWV, and costs |
| **R26** | Summary Default Filters | Always apply: `WHERE LIVE_URL NOT LIKE '%paradisemedia.com%' AND LIVE_URL != 'https://Not Applicable'` unless the user explicitly asks to include internal/placeholder pages |
| **R27** | Summary BRAND_PERFORMANCE Standalone | `summary.BRAND_PERFORMANCE` has **NO joins** to articles, domains, or other summary tables. Use for brand-level analysis only. Cannot attribute brand revenue to specific articles or domains |

### API Rules

| Rule ID | Rule Name | Description |
|---------|-----------|-------------|
| **R13** | SEO Data Source | SEO data (rankings, volume, backlinks) ALWAYS comes from DataForSEO API, **NEVER BigQuery** |
| **R14** | Live Data Only | DataForSEO provides live/real-time data - use for current state analysis |
| **R15** | API Rate Limits | Respect API rate limits - batch requests where possible |
| **R16** | Task ID Format | ClickUp Task IDs are alphanumeric (e.g., `86aembwf3`) |
| **R17** | Task ID = DYNAMIC | ClickUp Task ID matches BigQuery DYNAMIC field exactly |
| **R18** | ClickUp Rate Limiting | Respect ClickUp API rate limits (100 requests/min) |
| **R19** | Comment Format | Use markdown formatting for ROI comments posted to tasks |

### Forbidden Rules

| Rule ID | Rule Name | Description |
|---------|-----------|-------------|
| **R20** | NEVER Lakehouse | **NEVER** use `paradisemedia-bi.lakehouse` for any revenue, ROI, or reporting queries |
| **R21** | Keywords ≠ Revenue | DataForSEO keywords **cannot** be linked to revenue data. Use keywords only for "Target Keywords" in ARTICLE_INFORMATION |

---

## SECTION 4: DataForSEO API (SEO Data Only)

| # | Endpoint | Purpose | Key Fields | Scope |
|---|----------|---------|------------|-------|
| 1 | `/v3/serp/google/organic/live` | Live SERP rankings | keyword, position, url, domain, title, description | Use for live keyword ranking checks |
| 2 | `/v3/keywords_data/google/search_volume/live` | Search volume data | keyword, search_volume, cpc, competition, competition_level | Use for keyword research and volume analysis |
| 3 | `/v3/backlinks/summary/live` | Backlink metrics | target, backlinks, referring_domains, domain_rank, broken_backlinks | Use for backlink analysis and link building |
| 4 | `/v3/on_page/instant_pages` | On-page SEO audit | url, meta_title, meta_description, h1, h2, word_count, images | Use for technical SEO and on-page analysis |
| 5 | `/v3/domain_analytics/technologies/domain_technologies` | Tech stack detection | domain, technologies, categories | Use for competitor tech analysis |

### Keywords for DataForSEO

Rankings, SERP, Position, Keyword ranking, Search volume, CPC, Competition, Keyword difficulty, Backlinks, Referring domains, Domain rating, DR, On-page SEO, Meta tags, Title tags, H1, Technical SEO, Tech stack, CMS, Technologies

---

## SECTION 5: ClickUp API (Task Management)

| # | Endpoint | Method | Purpose | Key Fields |
|---|----------|--------|---------|------------|
| 1 | `/api/v2/task/{task_id}` | GET | Get task details | id, name, status, custom_fields, assignees, due_date |
| 2 | `/api/v2/task/{task_id}/comment` | POST | Post comment to task | comment_text |
| 3 | `/api/v2/task/{task_id}/comment` | GET | Get task comments | comments[], id, comment_text, user |
| 4 | `/api/v2/list/{list_id}/task` | GET | Get all tasks from list | tasks[], id, name, status |
| 5 | `/api/v2/task/{task_id}` | PUT | Update task | status, assignees, custom_fields |
| 6 | `/api/v2/list/{list_id}` | GET | Get list details | id, name, folder, space |

### Configuration

| Setting | Value |
|---------|-------|
| API Key Location | `/home/andre/.claude/clickup_config.json` |
| Base URL | `https://api.clickup.com` |
| Auth Header | `Authorization: {API_KEY}` |

### Keywords for ClickUp

Task, Task ID, ClickUp, List, Folder, Space, Status, Assignee, Due date, Comment, Post comment, Task comment, Custom fields, @dragon

---

## SECTION 6: Locked Query Patterns

### Query 1: Task-Level ROI Analysis
```sql
-- Task-Level ROI (DYNAMIC = ClickUp Task ID)
SELECT
    ai.TASK_ID,
    ai.TASK_NAME,
    ai.LIVE_URL,
    ai.DOMAIN,
    SUM(ap.CLICKS) as CLICKS,
    SUM(ap.SIGNUPS) as SIGNUPS,
    SUM(ap.GOALS) as FTDS,                              -- R1: GOALS = FTDs
    SUM(ap.TOTAL_COMMISSION_USD) as COMMISSION,
    SUM(ap.TOTAL_COMMISSION_USD_NP) as COMMISSION_NP,   -- R3: New Player Split
    SUM(ap.TOTAL_COMMISSION_USD_LP) as COMMISSION_LP    -- R4: Legacy Player Split
FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
LEFT JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap
    ON ai.TASK_ID = ap.DYNAMIC                          -- R9: Join Key
WHERE ai.TASK_ID IN ('{task_ids}')
    AND ap.DATE_ID BETWEEN {start_date} AND {end_date}  -- R6: YYYYMMDD format
GROUP BY ai.TASK_ID, ai.TASK_NAME, ai.LIVE_URL, ai.DOMAIN
ORDER BY COMMISSION DESC
```

### Query 2: Fixed Fees at Task Level
```sql
-- Fixed Fee data at article/task level (R12)
SELECT
    ci.DYNAMIC,
    ci.LIVE_URL,
    ci.DOMAIN,
    dff.FIXED_FEE_USD
FROM `paradisemedia-bi.reporting.COSTS_INFORMATION` ci
JOIN `paradisemedia-bi.reporting.DIM_FIXED_FEE` dff
    ON ci.LINK_FK = dff.FIXED_FEE_SK
WHERE ci.SOURCE = 'FIXED_FEES'
    AND ci.DYNAMIC IN ('{task_ids}')
```

### Query 3: Total Revenue (Commission + Fixed Fees)
```sql
-- Total Revenue = Commission + Fixed Fees (R11)
WITH commission_data AS (
    SELECT
        ai.TASK_ID,
        ai.TASK_NAME,
        SUM(ap.TOTAL_COMMISSION_USD) as COMMISSION
    FROM `paradisemedia-bi.reporting.ARTICLE_INFORMATION` ai
    LEFT JOIN `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE` ap
        ON ai.TASK_ID = ap.DYNAMIC
    WHERE ai.TASK_ID IN ('{task_ids}')
        AND ap.DATE_ID BETWEEN {start_date} AND {end_date}
    GROUP BY ai.TASK_ID, ai.TASK_NAME
),
fixed_fee_data AS (
    SELECT
        ci.DYNAMIC as TASK_ID,
        SUM(dff.FIXED_FEE_USD) as FIXED_FEES
    FROM `paradisemedia-bi.reporting.COSTS_INFORMATION` ci
    JOIN `paradisemedia-bi.reporting.DIM_FIXED_FEE` dff
        ON ci.LINK_FK = dff.FIXED_FEE_SK
    WHERE ci.SOURCE = 'FIXED_FEES'
        AND ci.DYNAMIC IN ('{task_ids}')
    GROUP BY ci.DYNAMIC
)
SELECT
    c.TASK_ID,
    c.TASK_NAME,
    c.COMMISSION,
    COALESCE(f.FIXED_FEES, 0) as FIXED_FEES,
    c.COMMISSION + COALESCE(f.FIXED_FEES, 0) as TOTAL_REVENUE
FROM commission_data c
LEFT JOIN fixed_fee_data f ON c.TASK_ID = f.TASK_ID
ORDER BY TOTAL_REVENUE DESC
```

### Query 4: High-Level Financial Report (Voonix)
```sql
-- High-Level Financial Performance (Financial Report is the bible)
SELECT
    BRAND,
    PROGRAM,
    SUM(TOTAL_COMMISSION_USD) as COMMISSION,
    DATE_ID
FROM `paradisemedia-bi.reporting.FINANCIAL_REPORT`
WHERE DATE_ID BETWEEN {start_date} AND {end_date}
GROUP BY BRAND, PROGRAM, DATE_ID
ORDER BY COMMISSION DESC
```

---

## SECTION 7: Forbidden Sources

| # | Source | Reason | Alternative |
|---|--------|--------|-------------|
| 1 | `paradisemedia-bi.lakehouse.*` | Internal ETL layer - NOT for reporting | Use `paradisemedia-bi.summary.*` |
| 2 | `paradisemedia-bi.reporting.*` | Deprecated — replaced by summary schema | Use `paradisemedia-bi.summary.*` |
| 3 | `paradisemedia-bi.analytics.*` | ML/analytics only - not for revenue data | Use `summary.ARTICLE_PERFORMANCE` |
| 4 | `paradisemedia-bi.testing.*` | Development/testing only | Use `summary.*` tables |
| 5 | `paradisemedia-bi.bi_playground.*` | Experimentation area - unstable | Use `summary.*` tables |
| 6 | Domain-level aggregation for /tasks_ROI | Wrong granularity - loses task attribution | Use ARTICLE_KEY + DATE level |
| 6 | DataForSEO keywords for revenue linkage | Keywords from DataForSEO **cannot be linked to revenue** | Use only for "Target Keywords" field |
| 7 | BigQuery for live SEO data | Stale data - not real-time | Use DataForSEO API |
| 8 | ~~`paradisemedia-bi.summary.ARTICLE_PERFORMANCE`~~ | **R24 UPDATED (v1.2)**: Table restructured — brand attribution bug fixed. Now APPROVED. See Section 1B | N/A — table is now approved |

### Critical Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Matching by task NAME keywords | Causes false matches, aggregates wrong data | Match by exact TASK_ID = DYNAMIC |
| Using FCT_* tables from lakehouse | Bypasses reporting layer, inconsistent data | Use reporting.* equivalents |
| Summing commission at domain level for task ROI | Inflates numbers, loses attribution | Filter by specific TASK_ID |
| Hardcoding API keys in scripts | Security risk | Use config files (`clickup_config.json`) |
| Linking DataForSEO keywords to revenue | No join key exists | Use keywords for SEO analysis only |

---

## APPROVAL & AUDIT LOG

| Date | Version | Approved By | Notes |
|------|---------|-------------|-------|
| 2026-02-02 | 1.0 | Andre | Initial approval with governance rules G1-G3 |
| 2026-02-11 | 1.1 | Andre | Added Section 1B: summary schema (4 tables approved, ARTICLE_PERFORMANCE blocked). Added rules R22-R25. Blocked summary.ARTICLE_PERFORMANCE in Forbidden Sources |
| 2026-02-13 | 1.2 | Andre | Full summary schema update from CHATBOT_TABLES_DOCUMENTATION. Expanded to 7 approved tables (unblocked ARTICLE_PERFORMANCE after brand fix, added ARTICLE_SEO + ARTICLE_INVOICES). Added cross-table join matrix, default query filters, table detail columns. Added rules R26-R27. Updated R24 (grain awareness replaces block). Removed summary.ARTICLE_PERFORMANCE from Forbidden Sources |

---

## COMPLIANCE CHECKLIST

Before any SQL query or data model reference:

- [ ] Referenced Master List v1.2
- [ ] Used `summary` schema tables ONLY (NEVER reporting or lakehouse)
- [ ] Used correct join keys (ARTICLE_KEY + DATE for article joins; TASK_ID for production joins)
- [ ] Applied correct column definitions (FTD = FTDs, NRC = signups, TOTAL_COMMISSION_USD)
- [ ] Used correct date format (DATE type, YYYY-MM-DD — R22)
- [ ] Applied default query filters for summary tables (R26 — exclude paradisemedia.com and placeholder URLs)
- [ ] Aggregated summary.ARTICLE_PERFORMANCE before joining to single-grain tables (R24 — multi-brand rows)
- [ ] Did NOT join BRAND_PERFORMANCE to articles/domains (R27 — standalone table)
- [ ] No invented relationships
- [ ] No assumptions beyond this document

**Failure to comply = AUTOMATIC TASK REVIEW FAILURE**

---

*Document Location: `/home/andre/.claude/MASTER_LIST_v1.0.md`*
*Source Reference: `BI-REPO-PARADISEMEDIA/exports/chatbot/CHATBOT_TABLES_DOCUMENTATION.md`*
*Owner: Andre | Maintained by: WOL & BOB (with approval)*
