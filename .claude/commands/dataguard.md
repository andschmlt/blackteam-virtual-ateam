# /dataguard - Data Terminology & Integrity Standards

**Version:** 2.2
**Created:** 2026-01-28
**Updated:** 2026-02-13
**Purpose:** Enforce MASTER_LIST v1.2 compliance, data terminology, and calculation integrity

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before enforcing standards.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/.claude/standards/VALIDATION_STANDARDS.md` — Pre-response checklist

**RAG Query:**
```python
import sys; sys.path.insert(0, "/home/andre/AS-Virtual_Team_System_v2/rag")
from rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("data terminology integrity standards master list", top_k=5)
learnings = rag.query("data accuracy corrections comparison validation", collection_name="learnings", top_k=3)
rules = rag.query("dataguard master list compliance", collection_name="rules", top_k=3)
```

---

## MASTER_LIST v1.2 COMPLIANCE (MANDATORY - HIGHEST PRIORITY)

**Reference:** `/home/andre/.claude/MASTER_LIST_v1.0.md`

### APPROVED DATA SOURCES (USE ONLY THESE)

```
┌─────────────────────────────────────────────────────────────────┐
│  APPROVED SCHEMA: paradisemedia-bi.summary (PRIMARY)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TABLE                    │ PURPOSE                              │
│  ─────────────────────────┼──────────────────────────────────────│
│  ARTICLE_PERFORMANCE      │ Revenue, FTDs, clicks per article    │
│  ARTICLE_SEO              │ Core Web Vitals, GA sessions         │
│  ARTICLE_INVOICES         │ Article costs (DLC, ClickUp, Fixed)  │
│  BRAND_PERFORMANCE        │ Brand-level metrics (standalone)     │
│  DOMAIN_PERFORMANCE       │ Domain-level aggregated metrics      │
│  SEO_PERFORMANCE          │ Rankings, backlinks, GSC traffic     │
│  PRODUCTION_CYCLE         │ Article production workflow           │
│  ARTICLE_CHANGELOG        │ Production cycles, TAT               │
│  DIM_BRAND                │ Brand dimension                      │
│  DIM_VERTICAL             │ Vertical/Niche hierarchy             │
│  DIM_DATE                 │ Date dimension                       │
│  DIM_FIXED_FEE            │ Fixed fee agreements                 │
│  DIM_PRODUCT              │ Domain/product dimension             │
│  DIM_INVOICE              │ Invoice details                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  APPROVED SCHEMA: paradisemedia-bi.summary (SUPPLEMENTARY)       │
│  Added v1.2 (2026-02-13) — Denormalized LLM-ready tables        │
│  Uses DATE type (not DATE_ID), FLOAT64 for monetary fields       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TABLE                    │ PURPOSE                              │
│  ─────────────────────────┼──────────────────────────────────────│
│  ARTICLE_PERFORMANCE      │ Revenue by Article×Brand×Program     │
│                           │ (Multi-row grain — aggregate first)  │
│  ARTICLE_SEO              │ CWV + GA metrics per article         │
│  ARTICLE_INVOICES         │ Costs: DLC, ClickUp, Fixed Fee       │
│  BRAND_PERFORMANCE        │ Brand-level (STANDALONE — no joins)  │
│  DOMAIN_PERFORMANCE       │ Domain metrics (iGaming + Growth)    │
│  PRODUCTION_CYCLE         │ Status changes, cycle times          │
│  SEO_PERFORMANCE          │ GSC + Accuranker + Ahrefs keywords   │
│                                                                  │
│  JOIN KEYS:               │                                      │
│  • ARTICLE_KEY + DATE     │ Between article tables               │
│  • DOMAIN_KEY + DATE      │ Article/SEO → Domain                 │
│  • TASK_ID                │ Any article table → PRODUCTION_CYCLE │
│                                                                  │
│  DEFAULT FILTERS (R26):                                          │
│  • LIVE_URL NOT LIKE '%paradisemedia.com%'                       │
│  • LIVE_URL != 'https://Not Applicable'                          │
│                                                                  │
│  RULES:                                                          │
│  • R22: DATE type, not DATE_ID integers                          │
│  • R23: FLOAT64 monetary — accept 0.05% variance                │
│  • R24: ARTICLE_PERFORMANCE has multi-brand rows — aggregate     │
│  • R25: Prefer DOMAIN_PERFORMANCE for domain queries             │
│  • R26: Apply default filters (exclude internal pages)           │
│  • R27: BRAND_PERFORMANCE is standalone (no article/domain join) │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### FORBIDDEN DATA SOURCES (NEVER USE)

```
┌─────────────────────────────────────────────────────────────────┐
│  🚫 FORBIDDEN - AUTOMATIC FAILURE IF USED                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOURCE                   │ REASON                               │
│  ─────────────────────────┼──────────────────────────────────────│
│  bi_playground.*          │ Experimentation area - unstable      │
│  lakehouse.*              │ Internal ETL - NOT for reporting     │
│  analytics.*              │ ML/analytics only - not revenue      │
│  testing.*                │ Development only                     │
│  chatbot.*                │ Deprecated schema                    │
│                                                                  │
│  ANTI-PATTERNS:                                                  │
│  • Matching by task NAME keywords (use TASK_ID = DYNAMIC)        │
│  • Using FCT_* tables from lakehouse                             │
│  • Summing at domain level for task ROI (use TASK_ID)            │
│  • Linking DataForSEO keywords to revenue (NO JOIN EXISTS)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### CRITICAL JOIN RULES (MANDATORY)

```sql
-- REPORTING SCHEMA JOINS --

-- Rule R9: Article join key (reporting)
ARTICLE_INFORMATION.TASK_ID = ARTICLE_PERFORMANCE.DYNAMIC

-- Rule R12: Fixed fee join (reporting)
COSTS_INFORMATION.SOURCE = 'FIXED_FEES'
COSTS_INFORMATION.LINK_FK = DIM_FIXED_FEE.FIXED_FEE_SK

-- Rule R6: Date format (reporting)
DATE_ID = YYYYMMDD (integer, e.g., 20260204)

-- Rule R11: Total revenue calculation
Total Revenue = Commission + Fixed Fees

-- SUMMARY SCHEMA JOINS (Added v2.2) --

-- Rule R24: Summary article joins (aggregate multi-brand rows first)
summary.ARTICLE_PERFORMANCE → summary.ARTICLE_SEO
  ON ARTICLE_KEY + DATE (Many:1 — aggregate revenue first)

summary.ARTICLE_PERFORMANCE → summary.ARTICLE_INVOICES
  ON ARTICLE_KEY + DATE (Many:1 — aggregate revenue first)

-- Summary cross-table joins
summary.*.DOMAIN_KEY = summary.DOMAIN_PERFORMANCE.DOMAIN_KEY
summary.*.TASK_ID = summary.PRODUCTION_CYCLE.TASK_ID
summary.*.ARTICLE_KEY = summary.SEO_PERFORMANCE.ARTICLE_KEY

-- Rule R22: Summary date format
DATE = 'YYYY-MM-DD' (native DATE type, NOT DATE_ID integer)

-- Rule R27: BRAND_PERFORMANCE is standalone
-- NEVER join summary.BRAND_PERFORMANCE to other tables
```

### COLUMN DEFINITIONS (MANDATORY)

| Column | Table | Definition | Rule |
|--------|-------|------------|------|
| **GOALS** | ARTICLE_PERFORMANCE | FTDs (First Time Deposits) | R1 |
| **FTD** | BRAND_PERFORMANCE | FTDs (same as GOALS) | R1 |
| **DYNAMIC** | ARTICLE_PERFORMANCE | ClickUp Task ID | R2 |
| **TASK_ID** | ARTICLE_INFORMATION | ClickUp Task ID | R2 |
| **TOTAL_COMMISSION_USD** | Multiple | Total commission (NP + LP) | |
| **TOTAL_COMMISSION_USD_NP** | ARTICLE_PERFORMANCE | New Player commission | R3 |
| **TOTAL_COMMISSION_USD_LP** | ARTICLE_PERFORMANCE | Legacy Player commission | R4 |

### PRE-QUERY VALIDATION CHECKLIST

Before executing ANY BigQuery query:

```
☐ 1. SCHEMA CHECK
   □ Using paradisemedia-bi.summary.* ONLY ONLY
   □ NOT using bi_playground, lakehouse, analytics, testing

☐ 2. JOIN KEY CHECK (reporting)
   □ Using TASK_ID = DYNAMIC for article joins
   □ NOT matching by task name or keywords

☐ 3. JOIN KEY CHECK (summary)
   □ Using ARTICLE_KEY + DATE for article-to-article joins
   □ Using DOMAIN_KEY + DATE for article-to-domain joins
   □ Using TASK_ID for article-to-production joins
   □ NOT joining BRAND_PERFORMANCE to any other table (R27)
   □ Aggregating ARTICLE_PERFORMANCE before joining to single-grain tables (R24)

☐ 4. COLUMN CHECK
   □ FTDs = GOALS column in reporting (not SIGNUPS)
   □ FTDs = FTD column in summary
   □ DATE_ID in YYYYMMDD format (reporting) OR DATE in YYYY-MM-DD format (summary — R22)

☐ 5. FILTER CHECK (summary)
   □ Applied LIVE_URL NOT LIKE '%paradisemedia.com%' (R26)
   □ Applied LIVE_URL != 'https://Not Applicable' (R26)

☐ 6. CALCULATION CHECK
   □ EPC = TOTAL_COMMISSION_USD / CLICKS
   □ EPF = TOTAL_COMMISSION_USD / GOALS (reporting) or FTD (summary)
   □ Total Revenue = Commission + Fixed Fees

FAILURE TO COMPLY = AUTOMATIC TASK FAILURE
```

### DataForSEO Rules

```
┌─────────────────────────────────────────────────────────────────┐
│  DATAFORSEO USAGE RULES                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ ALLOWED:                                                     │
│  • Live SERP rankings (/v3/serp/google/organic/live)            │
│  • Search volume data (/v3/keywords_data/google/search_volume)  │
│  • Backlink metrics (/v3/backlinks/summary/live)                │
│  • On-page SEO audit (/v3/on_page/instant_pages)                │
│                                                                  │
│  🚫 FORBIDDEN (Rule R21):                                        │
│  • Linking DataForSEO keywords to revenue data                  │
│  • No join key exists between DataForSEO and BigQuery           │
│  • Use only for SEO analysis, NOT revenue attribution           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## HARD RULES (MANDATORY - NO EXCEPTIONS)

### Rule 1: Conversion Funnel Terminology

```
┌─────────────────────────────────────────────────────────────────┐
│  OFFICIAL TERMINOLOGY STANDARDS                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  METRIC          │ ALIASES         │ DEFINITION                 │
│  ────────────────┼─────────────────┼────────────────────────────│
│  FTDs            │ Goals,          │ First Time Deposits        │
│                  │ Conversions     │ (User makes first deposit) │
│  ────────────────┼─────────────────┼────────────────────────────│
│  Signups         │ Registrations,  │ Account Registrations      │
│                  │ NRC             │ (User creates account)     │
│  ────────────────┼─────────────────┼────────────────────────────│
│  Clicks          │ Click Events    │ Outbound link clicks       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

CONVERSION FUNNEL ORDER:
  Clicks → Signups → FTDs → Revenue

NEVER MIX THESE TERMS:
  ✗ "Signups" when referring to FTDs
  ✗ "Goals" when referring to Signups
  ✗ "Conversions" ambiguously (specify FTDs or Signups)
```

### Rule 2: FTDs = Goals (Equivalence)

```
FTDs ≡ Goals ≡ Conversions (in iGaming context)

When reporting:
- Use "FTDs" as primary term in all iGaming reports
- "Goals" acceptable in PostHog/analytics tool context
- "Conversions" acceptable but must clarify = FTDs

NEVER use "Signups" to mean FTDs or vice versa.
```

### Rule 3: Calculation Direction Verification

**MANDATORY CHECK for all percentage changes:**

```python
# CORRECT CALCULATION
change = new_value - old_value
pct_change = (change / old_value) * 100

# DIRECTION VERIFICATION
if new_value > old_value:
    direction = "INCREASED" or "GREW" or "UP"
elif new_value < old_value:
    direction = "DECREASED" or "DECLINED" or "DOWN"
else:
    direction = "UNCHANGED" or "FLAT"
```

**CRITICAL:** The direction word MUST match the math:
- `10,698 → 23,254` = **INCREASED** (+117.4%)
- `23,254 → 10,698` = **DECREASED** (-54.0%)

### Rule 4: Report Title Consistency

Report titles must match the data narrative:
- If metric INCREASED: Use "Growth", "Surge", "Improvement"
- If metric DECREASED: Use "Decline", "Drop", "Stagnation"
- If metric FLAT: Use "Plateau", "Stability", "Maintenance"

**VIOLATION:** Title says "STAGNATION" but data shows +117% growth

---

## DATA VALIDATION CHECKLIST

Before finalizing ANY analytics report, verify:

```
☐ 1. TERMINOLOGY CHECK
   □ FTDs used correctly (not confused with Signups)
   □ Signups used correctly (not confused with FTDs)
   □ Goals = FTDs equivalence maintained
   □ Funnel order respected (Clicks → Signups → FTDs)

☐ 2. CALCULATION CHECK
   □ Percentage calculations are mathematically correct
   □ Direction words match the math (increase/decrease)
   □ Base period clearly stated (e.g., "Oct → Jan")
   □ Comparison periods are equivalent length

☐ 3. NARRATIVE CHECK
   □ Title matches data direction
   □ Executive summary matches detailed data
   □ Key findings are factually accurate
   □ Recommendations align with actual trends

☐ 4. CONSISTENCY CHECK
   □ Same metric uses same terminology throughout
   □ Numbers in summary match numbers in tables
   □ Charts match tabular data
   □ No contradictions between sections
```

---

## BigQuery Field Mapping

### Reporting Schema Fields

| BigQuery Field | Standard Term | Report Label |
|----------------|---------------|--------------|
| `CONVERSIONS` | FTDs | First Time Deposits |
| `FTD` | FTDs | First Time Deposits |
| `GOALS` | FTDs | First Time Deposits (ARTICLE_PERFORMANCE) |
| `SIGNUPS` | Signups | Registrations |
| `NRC` | Signups | New Registered Customers |
| `CLICKS` | Clicks | Outbound Clicks |
| `TOTAL_COMMISSION_USD` | Revenue | Total Commission |
| `TOTAL_COMMISSION_USD_NP` | NP Revenue | New Player Revenue |
| `TOTAL_COMMISSION_USD_LP` | LP Revenue | Legacy Player Revenue |

### Summary Schema Fields (Added v2.2)

| BigQuery Field | Standard Term | Report Label | Table(s) |
|----------------|---------------|--------------|----------|
| `ARTICLE_KEY` | Article Key | Surrogate key (join) | All article tables |
| `DOMAIN_KEY` | Domain Key | Surrogate key (join) | Most tables |
| `FTD` | FTDs | First Time Deposits | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE |
| `NRC` | Signups | New Registered Customers | ARTICLE_PERFORMANCE |
| `EPC_USD` | EPC | Earnings Per Click | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE |
| `EPF_USD` | EPF | Earnings Per FTD | ARTICLE_PERFORMANCE, BRAND_PERFORMANCE |
| `CPA_COMMISSION_USD` | CPA Commission | CPA Payments | ARTICLE_PERFORMANCE |
| `REVSHARE_COMMISSION_USD` | RevShare Commission | Revenue Share | ARTICLE_PERFORMANCE |
| `DLC_COST_USD` | DLC Cost | Content Provider Cost | ARTICLE_INVOICES, DOMAIN_PERFORMANCE |
| `CLICKUP_INVOICE_COST_USD` | ClickUp Cost | Internal Production Cost | ARTICLE_INVOICES, DOMAIN_PERFORMANCE |
| `FIXED_FEE_EARNINGS_USD` | Fixed Fee | Monthly Retainer | ARTICLE_INVOICES, DOMAIN_PERFORMANCE |
| `TOTAL_ARTICLE_COST_USD` | Article Cost | DLC + ClickUp (no FF) | ARTICLE_INVOICES, DOMAIN_PERFORMANCE |
| `LCP_AVG` | LCP | Largest Contentful Paint (ms) | ARTICLE_SEO, DOMAIN_PERFORMANCE |
| `INP_AVG` | INP | Interaction to Next Paint (ms) | ARTICLE_SEO, DOMAIN_PERFORMANCE |
| `CLS_AVG` | CLS | Cumulative Layout Shift | ARTICLE_SEO, DOMAIN_PERFORMANCE |
| `GA_SESSIONS` | Sessions | GA Sessions | ARTICLE_SEO, DOMAIN_PERFORMANCE |
| `PRODUCTION_STAGE` | Production Stage | Workflow stage | PRODUCTION_CYCLE |
| `MINUTES_IN_STATUS` | Time in Status | Minutes spent | PRODUCTION_CYCLE |
| `IGAMING_*` | iGaming metrics | iGaming-prefixed | DOMAIN_PERFORMANCE |
| `GROWTH_*` | Growth metrics | Growth-prefixed | DOMAIN_PERFORMANCE |
| `GSC_*` | GSC metrics | Google Search Console | SEO_PERFORMANCE |
| `ACCURANKER_*` | Accuranker metrics | Accuranker tracker | SEO_PERFORMANCE |
| `AHREFS_*` | Ahrefs metrics | Ahrefs data | SEO_PERFORMANCE |

---

## PostHog Event Mapping

| PostHog Event | Standard Term | Notes |
|---------------|---------------|-------|
| `goal_completed` | FTD | PostHog goal = our FTD |
| `signup_completed` | Signup | Registration event |
| `navboost:cta_click` | Click | Outbound click |
| `navboost:outbound_click` | Click | Affiliate link click |

---

## Validation Queries

### Verify FTD vs Signup Distinction
```sql
-- These should be DIFFERENT numbers
SELECT
  SUM(SIGNUPS) as total_signups,
  SUM(CONVERSIONS) as total_ftds,
  SUM(CONVERSIONS) - SUM(SIGNUPS) as signup_to_ftd_dropoff
FROM `dataset.ARTICLE_PERFORMANCE`
WHERE DATE >= '2025-10-01'
```

### Verify Month-over-Month Direction
```sql
WITH monthly AS (
  SELECT
    FORMAT_DATE('%Y-%m', DATE) as month,
    SUM(CONVERSIONS) as ftds
  FROM `dataset.ARTICLE_PERFORMANCE`
  WHERE DATE >= '2025-10-01'
  GROUP BY 1
)
SELECT
  month,
  ftds,
  LAG(ftds) OVER (ORDER BY month) as prev_ftds,
  ftds - LAG(ftds) OVER (ORDER BY month) as change,
  CASE
    WHEN ftds > LAG(ftds) OVER (ORDER BY month) THEN 'INCREASED'
    WHEN ftds < LAG(ftds) OVER (ORDER BY month) THEN 'DECREASED'
    ELSE 'UNCHANGED'
  END as direction
FROM monthly
ORDER BY month
```

---

## Error Examples

### WRONG (Terminology Confusion)
```
"Signups increased from 10,698 to 23,254"
  ↑ ERROR: These are FTDs, not Signups
```

### WRONG (Direction Mismatch)
```
"FTDs declined 117.4% from October (10,698) to January (23,254)"
  ↑ ERROR: 10,698 → 23,254 is an INCREASE, not decline
```

### WRONG (Title Contradiction)
```
Title: "FTD STAGNATION ANALYSIS"
Data: FTDs grew +117%
  ↑ ERROR: Title contradicts data
```

### CORRECT
```
"FTDs increased 117.4% from October (10,698) to January (23,254)"
Title: "FTD GROWTH ANALYSIS" or "FTD PERFORMANCE ANALYSIS"
```

---

## Integration with Reports

All analytics reports MUST invoke DataGuard validation:

```markdown
## DataGuard Compliance
☑ Terminology verified (FTDs ≠ Signups)
☑ Calculations verified (direction matches math)
☑ Title-to-data consistency verified
☑ Report generated: 2026-01-28
```

---

## Usage

```
/dataguard                       # Show full compliance checklist
/dataguard validate              # Run MASTER_LIST + terminology validation
/dataguard schema                # Show approved tables (reporting only)
/dataguard forbidden             # Show forbidden sources
/dataguard check [report.pdf]    # Validate existing report
/dataguard terms                 # Show terminology standards
/dataguard query [sql]           # Pre-validate a SQL query
```

### Auto-Invocation Rule

**CRITICAL:** DataGuard MUST be invoked automatically before:
- Any BigQuery query execution
- Any analytics report generation
- Any data extraction for business questions
- Any /tasks_ROI, /FTD_DEEPDIVE_ANALYSIS, or similar commands

```python
# Example auto-validation pattern
def execute_query(sql):
    sql_lower = sql.lower()

    # STEP 1: DataGuard forbidden schema check
    if "lakehouse" in sql_lower:
        raise Error("FORBIDDEN: lakehouse schema not allowed")
    if "bi_playground" in sql_lower:
        raise Error("FORBIDDEN: bi_playground schema not allowed")

    # STEP 2: Verify approved schema
    if "reporting." not in sql_lower and "summary." not in sql_lower:
        raise Warning("Query should use reporting or summary schema")

    # STEP 3: Summary-specific checks
    if "summary." in sql_lower:
        # R22: Ensure DATE format, not DATE_ID
        if "date_id" in sql_lower:
            raise Error("R22: summary tables use DATE type, not DATE_ID")
        # R27: BRAND_PERFORMANCE standalone check
        if "summary.brand_performance" in sql_lower and "join" in sql_lower:
            raise Warning("R27: summary.BRAND_PERFORMANCE is standalone - no joins allowed")

    # STEP 4: Execute only if validation passes
    return bigquery.execute(sql)
```

---

## Escalation

If DataGuard violations are found:
1. **STOP** report distribution
2. **FLAG** to Head of Analytics
3. **CORRECT** before any external sharing
4. **LOG** error for process improvement

---

---

## CRITICAL RULES: SOURCE OF TRUTH (Added 2026-01-28)

**INCIDENT:** FTD_DEEP_ANALYSIS_v4.1 reported 68,803 FTDs when actual was ~17,895 (4x inflation).
**ROOT CAUSE:** Query used wrong metric field or wrong data source.

### Rule 28: SOURCE OF TRUTH VALIDATION (MANDATORY)

```
┌─────────────────────────────────────────────────────────────────┐
│  OFFICIAL SOURCE OF TRUTH FOR FTDs/Goals                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRIMARY SOURCE: Power BI Dashboard                             │
│  Dashboard: 18_iGaming_360v1.11                                 │
│                                                                  │
│  ALL FTD/Goals numbers MUST be validated against this           │
│  dashboard BEFORE any report is finalized.                      │
│                                                                  │
│  If BigQuery numbers don't match Power BI → INVESTIGATE         │
│  NEVER publish until discrepancy is resolved.                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Rule 29: METRIC FIELD VERIFICATION (MANDATORY)

Before running ANY FTD query:

```sql
-- STEP 1: Verify you're using the correct field
-- FTDs/Goals should use: FTD, CONVERSIONS, or GOALS field
-- NOT: SIGNUPS, NRC, REGISTRATIONS

-- STEP 2: Print a sample to verify values are reasonable
SELECT
  DATE,
  FTD,        -- Should be ~2000-6000/month for O&O iGaming
  SIGNUPS     -- Typically 3-5x higher than FTD
FROM your_table
WHERE DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)
LIMIT 10;

-- STEP 3: Cross-check one month against Power BI
-- If they don't match, STOP and investigate
```

### Rule 30: SANITY CHECK THRESHOLDS (MANDATORY)

```
┌─────────────────────────────────────────────────────────────────┐
│  O&O iGAMING FTD SANITY THRESHOLDS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EXPECTED MONTHLY RANGE:                                         │
│  • Normal:     2,000 - 6,000 FTDs/month                         │
│  • Good month: 6,000 - 8,000 FTDs/month                         │
│  • Exceptional: 8,000 - 10,000 FTDs/month                       │
│                                                                  │
│  RED FLAGS - STOP AND VERIFY:                                   │
│  ⚠️  > 10,000 FTDs/month → LIKELY WRONG METRIC                  │
│  🚨 > 20,000 FTDs/month → DEFINITELY WRONG                      │
│  🚨 > 50,000 FTDs/month → CRITICAL ERROR (probably Signups)     │
│                                                                  │
│  REFERENCE (Actual 2025-2026 data):                             │
│  • Sep 2025: 2,105 FTDs                                          │
│  • Oct 2025: 3,373 FTDs                                          │
│  • Nov 2025: 4,429 FTDs                                          │
│  • Dec 2025: 4,767 FTDs                                          │
│  • Jan 2026 (MTD): 3,221 FTDs                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Rule 31: DUAL-SOURCE VERIFICATION (MANDATORY)

For ALL critical FTD reports:

```
REQUIRED VERIFICATION PROCESS:

1. Query BigQuery for FTD totals
2. Check Power BI 18_iGaming_360v1.11 for same period
3. Compare values:

   IF difference < 5%:
     → Acceptable variance, proceed

   IF difference 5-20%:
     → Investigate cause before proceeding
     → Document the variance and reason

   IF difference > 20%:
     → STOP - DO NOT PUBLISH
     → Likely using wrong metric or filter
     → Escalate to Head of Analytics
```

### Rule 32: REPORT SIGN-OFF CHECKLIST (MANDATORY)

```
┌─────────────────────────────────────────────────────────────────┐
│  FTD REPORT SIGN-OFF CHECKLIST                                  │
│  (Must complete BEFORE publishing any FTD report)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ☐ 1. METRIC VERIFICATION                                       │
│     □ Confirmed using FTD/CONVERSIONS field (not SIGNUPS)       │
│     □ Sample data reviewed and values reasonable                │
│                                                                  │
│  ☐ 2. SOURCE OF TRUTH CHECK                                     │
│     □ Compared against Power BI 18_iGaming_360v1.11             │
│     □ Variance < 5% OR variance documented and explained        │
│                                                                  │
│  ☐ 3. SANITY CHECK                                              │
│     □ Monthly FTDs within expected range (2,000-6,000)          │
│     □ No unexplained spikes or anomalies                        │
│                                                                  │
│  ☐ 4. CALCULATION VERIFICATION                                  │
│     □ Direction words match math (increase/decrease)            │
│     □ Percentages calculated correctly                          │
│                                                                  │
│  ☐ 5. SIGN-OFF                                                  │
│     □ Head of Analytics reviewed and approved                   │
│     □ DataGuard compliance confirmed                            │
│                                                                  │
│  SIGNATURE: _________________ DATE: _________________           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Deprecated Reports Log

| Report | Version | Date | Status | Reason |
|--------|---------|------|--------|--------|
| FTD_DEEP_ANALYSIS | v4.1 | 2026-01-27 | INVALID | Wrong metric (~4x inflation), direction error |
| FTD_PERFORMANCE_ANALYSIS | v4.2 | 2026-01-28 | INVALID | Used same wrong source data |

---

**/dataguard v2.2 | MASTER_LIST v1.2 Enforcer | BlackTeam Data Integrity | Paradise Media Group**

---

## Compliance Certification

Every data extraction or analysis report MUST include:

```markdown
## DataGuard v2.2 Compliance

### MASTER_LIST v1.2 Verification
☑ Schema: paradisemedia-bi.summary ONLY ONLY
☑ Forbidden sources: None used (bi_playground, lakehouse, etc.)
☑ Join keys: reporting TASK_ID=DYNAMIC / summary ARTICLE_KEY+DATE (verified)
☑ Column definitions: GOALS=FTDs (reporting) / FTD (summary) (verified)
☑ Summary default filters applied: R26 (exclude internal/placeholder URLs)
☑ Summary ARTICLE_PERFORMANCE aggregated before cross-joins: R24 (verified)

### Terminology Verification
☑ FTDs ≠ Signups (verified)
☑ Direction words match math
☑ Title matches data narrative

### Sign-off
Report generated: [DATE]
DataGuard compliant: YES
```
