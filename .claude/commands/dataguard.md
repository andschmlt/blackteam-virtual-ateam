# /dataguard - Data Terminology & Integrity Standards

**Version:** 1.0
**Created:** 2026-01-28
**Purpose:** Enforce consistent data terminology and calculation integrity across all analytics reports

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

| BigQuery Field | Standard Term | Report Label |
|----------------|---------------|--------------|
| `CONVERSIONS` | FTDs | First Time Deposits |
| `FTD` | FTDs | First Time Deposits |
| `SIGNUPS` | Signups | Registrations |
| `NRC` | Signups | New Registered Customers |
| `CLICKS` | Clicks | Outbound Clicks |
| `TOTAL_COMMISSION_USD` | Revenue | Total Commission |
| `TOTAL_COMMISSION_USD_NP` | NP Revenue | New Player Revenue |
| `TOTAL_COMMISSION_USD_LP` | LP Revenue | Legacy Player Revenue |

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
/dataguard check [report.pdf]    # Validate existing report
/dataguard validate              # Run validation checklist
/dataguard terms                 # Show terminology standards
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

**/dataguard v2.0 | BlackTeam Data Integrity | Paradise Media Group**
