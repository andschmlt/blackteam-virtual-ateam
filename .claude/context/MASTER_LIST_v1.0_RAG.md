# MASTER LIST v1.1 - RAG DATABASE ENTRY

## Virtual ATeam v2 - Data Source Knowledge Base
**Type:** RAG Reference Document | **Priority:** CRITICAL | **Version:** 1.1 (Updated 2026-02-11)

---

## ⚠️ GOVERNANCE RULES (MANDATORY FOR ALL AGENTS)

### RULE G1: MASTER LIST COMPLIANCE (CRITICAL)

| Role | Requirement |
|------|-------------|
| **WOL (WhiteTeam Head of Tech)** | MUST always reference this Master List. NEVER assume, change, or go beyond this document without Andre's approval |
| **BOB (BlackTeam Head of Tech)** | MUST always reference this Master List. NEVER assume, change, or go beyond this document without Andre's approval |
| **QA Team** | MUST validate all SQL and data model references against this Master List. Any deviation = FAIL review |
| **Directors** | MUST ensure all data catalog references follow these rules. Non-compliance = FAIL task review |
| **All Virtual ATeam Agents** | MUST use this document as the ONLY source of truth for data architecture |

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

## QUICK REFERENCE: APPROVED DATA SOURCES

### BigQuery Schema: `paradisemedia-bi.reporting` (PRIMARY)

| Table | Use Case |
|-------|----------|
| ARTICLE_PERFORMANCE | Article/URL revenue, clicks, signups, FTDs, commission |
| ARTICLE_INFORMATION | Article metadata, status, vertical, geo, ClickUp data |
| BRAND_PERFORMANCE | Brand-level metrics (secondary/QA) |
| COSTS_INFORMATION | Costs, spending, fixed fee linkage |
| FINANCIAL_REPORT | High-level financial (Voonix - the bible) |
| CLOAKING_TRAFFIC | Clickout data, redirects, @dragon |
| DIM_BRAND | Brand names lookup |
| DIM_VERTICAL | Vertical > Niche > Sub-Niche hierarchy |
| DIM_DATE | Date dimension |
| DIM_FIXED_FEE | Fixed fee amounts |

### BigQuery Schema: `paradisemedia-bi.summary` (SUPPLEMENTARY - added 2026-02-11)

| Table | Use Case | Priority |
|-------|----------|----------|
| DOMAIN_PERFORMANCE | Domain daily metrics (iGaming + Growth + GA + CWV + costs) | **PRIMARY for domain queries (R25)** |
| BRAND_PERFORMANCE | Brand metrics with pre-calculated EPC/EPF | Supplementary |
| SEO_PERFORMANCE | Consolidated GSC + Accuranker + Ahrefs (35M rows) | **PRIMARY for SEO overview** |
| PRODUCTION_CYCLE | Production workflow (status changes, TAT) | Supplementary |

**BLOCKED:** `summary.ARTICLE_PERFORMANCE` — NEVER USE (R24: 54% row loss, FTD data loss)

**Important:** Summary tables use native `DATE` type (`'2026-01-15'`), NOT `DATE_ID` integers (R22).
Summary monetary fields use FLOAT64, not NUMERIC — accept up to 0.05% variance (R23).

### External APIs

| API | Use Case |
|-----|----------|
| DataForSEO | SEO data ONLY (rankings, volume, backlinks) |
| ClickUp | Task management |

---

## CRITICAL RULES SUMMARY

| Rule | Description |
|------|-------------|
| **R1** | FTDs = GOALS column in ARTICLE_PERFORMANCE |
| **R2** | DYNAMIC = ClickUp Task ID |
| **R7** | Use `reporting` schema ONLY - **NEVER lakehouse** |
| **R9** | Join: ARTICLE_INFORMATION.TASK_ID = ARTICLE_PERFORMANCE.DYNAMIC |
| **R11** | Total Revenue = Commission + Fixed Fees |
| **R12** | Fixed Fee Join: COSTS_INFORMATION (SOURCE='FIXED_FEES') → DIM_FIXED_FEE (LINK_FK = FIXED_FEE_SK) |
| **R20** | **NEVER** use lakehouse for revenue/ROI queries |
| **R21** | DataForSEO keywords CANNOT be linked to revenue |
| **R22** | Summary tables use DATE type ('YYYY-MM-DD'), NOT DATE_ID integers |
| **R23** | Summary monetary FLOAT64 — accept up to 0.05% variance vs NUMERIC |
| **R24** | **NEVER** use summary.ARTICLE_PERFORMANCE (54% data loss) |
| **R25** | Prefer summary.DOMAIN_PERFORMANCE for domain-level aggregations |

---

## FORBIDDEN SOURCES (NEVER USE)

- `paradisemedia-bi.lakehouse.*`
- `paradisemedia-bi.analytics.*`
- `paradisemedia-bi.testing.*`
- `paradisemedia-bi.summary.ARTICLE_PERFORMANCE` (R24: data loss)
- Domain-level aggregation for task ROI
- DataForSEO keywords → revenue linkage

---

## RAG RETRIEVAL KEYWORDS

data source, bigquery, reporting, summary, article performance, article information, brand performance, domain performance, seo performance, production cycle, costs information, financial report, cloaking traffic, dim brand, dim vertical, dim date, dim fixed fee, task id, dynamic, goals, ftds, signups, clicks, commission, fixed fees, total revenue, epf, epc, dataforseo, clickup, lakehouse, forbidden, rules, join, query, date format, float64, numeric

---

*Full document: `/home/andre/.claude/MASTER_LIST_v1.0.md`*
*RAG Entry: `/home/andre/.claude/context/MASTER_LIST_v1.0_RAG.md`*
