# ROOT CAUSE ANALYSIS
## FTD Report Data Integrity Failure

**Date:** 2026-01-28
**Analyst:** Head of Analytics (Elias Thorne)
**Reviewed By:** Director, BlackTeam

---

## INCIDENT SUMMARY

| Field | Value |
|-------|-------|
| **Incident Date** | 2026-01-27 |
| **Report Affected** | FTD_DEEP_ANALYSIS_v4.1 |
| **Severity** | CRITICAL |
| **Impact** | Report showed ~4x inflated FTD numbers |

---

## DISCREPANCY DETAILS

### What the Report Claimed:
- October 2025: 10,698 FTDs
- January 2026: 23,254 FTDs
- Total (4 months): 68,803 FTDs
- Trend: "Declined 117.4%" (also wrong - this would be increase)

### Actual Data (Power BI 18_iGaming_360v1.11):
- September 2025: 2,105 FTDs
- October 2025: 3,373 FTDs
- November 2025: 4,429 FTDs
- December 2025: 4,767 FTDs
- January 2026 MTD: 3,221 FTDs
- Total: ~17,895 FTDs

### Variance:
- Reported: 68,803 FTDs
- Actual: 17,895 FTDs
- Inflation Factor: **3.85x** (~4x)

---

## ROOT CAUSE ANALYSIS

### Primary Cause: METRIC CONFUSION (High Confidence)

**Finding:** The query most likely used the `SIGNUPS` field instead of the `FTD` or `CONVERSIONS` field.

**Evidence:**
1. Signups are typically 3-5x higher than FTDs in the iGaming funnel
2. The 3.85x inflation factor aligns with typical Signup:FTD ratios
3. Both fields exist in the same BigQuery tables
4. Field names can be confused without careful verification

**Conversion Funnel:**
```
Clicks → Signups (registrations) → FTDs (first deposits) → Revenue
           ↑                           ↑
        ~17,000/period              ~4,500/period
        (3-4x higher)               (actual goal metric)
```

### Contributing Factors:

1. **No Source of Truth Validation**
   - BigQuery results were not cross-checked against Power BI dashboard
   - No sanity check against expected ranges

2. **Missing Field Verification**
   - Query did not confirm which field was being summed
   - No sample data review to catch the error

3. **No Sanity Check Thresholds**
   - 68,803 FTDs over 4 months (~17,000/month) should have triggered review
   - Expected range is 2,000-6,000 FTDs/month

4. **Direction Error Compounded Issue**
   - "Declined" stated when math showed increase
   - Suggests rushed review without calculation verification

---

## TIMELINE OF ERRORS

```
1. Query executed with wrong field (SIGNUPS instead of FTD)
                    ↓
2. Result: 68,803 (inflated ~4x)
                    ↓
3. No sanity check performed (should have flagged >10k/month)
                    ↓
4. No Power BI cross-check performed
                    ↓
5. Direction error: "declined" written despite increase in numbers
                    ↓
6. Report published with multiple critical errors
                    ↓
7. User (Andre) identified discrepancy vs Power BI
                    ↓
8. Root cause investigation initiated
```

---

## CORRECTIVE ACTIONS TAKEN

### Immediate:
1. ✅ Marked v4.1 and v4.2 reports as INVALID
2. ✅ Created deprecation notice
3. ✅ Updated DataGuard with Rules 28-32

### Short-term:
4. ✅ Creating corrected report v5.0 with actual data
5. ⏳ Implementing dual-source verification process

### Preventive (DataGuard v2.0):
- **Rule 28:** Source of Truth Validation (Power BI mandatory check)
- **Rule 29:** Metric Field Verification (confirm FTD vs SIGNUPS)
- **Rule 30:** Sanity Check Thresholds (flag if >10k/month)
- **Rule 31:** Dual-Source Verification (BigQuery + Power BI must match)
- **Rule 32:** Report Sign-off Checklist (mandatory before publishing)

---

## LESSONS LEARNED

1. **Always verify the metric field being queried**
   - FTD ≠ SIGNUPS - these are different funnel stages
   - Print sample data to confirm values are reasonable

2. **Cross-check against official dashboard**
   - Power BI 18_iGaming_360v1.11 is the source of truth
   - Never publish without this validation

3. **Apply sanity checks**
   - O&O iGaming FTDs: 2,000-6,000/month is normal
   - Anything >10,000/month should trigger investigation

4. **Verify calculations match narrative**
   - "Declined" vs "Increased" must match the math
   - Review direction words explicitly

---

## SIGN-OFF

| Role | Name | Status |
|------|------|--------|
| Head of Analytics | Elias Thorne | Confirmed |
| Head of Tech | DataForge | Confirmed |
| Director | BlackTeam | Approved |

**Date:** 2026-01-28

---

*BlackTeam Data Integrity | Root Cause Analysis | Paradise Media Group*
