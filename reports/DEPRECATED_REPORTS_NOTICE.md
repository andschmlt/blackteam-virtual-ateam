# DEPRECATED REPORTS NOTICE

**Date:** 2026-01-28
**Issued By:** Director, BlackTeam
**Authority:** DataGuard v2.0

---

## INVALID REPORTS - DO NOT USE

The following reports contain **critical data errors** and must NOT be used for any decision-making:

### 1. FTD_DEEP_ANALYSIS_v4.1_2026-01-27.pdf

| Field | Value |
|-------|-------|
| **Status** | INVALID - DO NOT USE |
| **Location** | C:\Users\andre\Downloads\ |
| **Error Type** | Data inflation (~4x), Direction error |
| **Reported FTDs** | 68,803 (WRONG) |
| **Actual FTDs** | ~17,895 (per Power BI) |

**Errors Found:**
1. Report claimed "FTDs declined 117.4%" but numbers showed increase
2. FTD values inflated by approximately 4x actual
3. Likely used SIGNUPS field instead of FTD/CONVERSIONS field
4. Source data not validated against Power BI dashboard

### 2. FTD_PERFORMANCE_ANALYSIS_v4.2_2026-01-28.md

| Field | Value |
|-------|-------|
| **Status** | INVALID - DO NOT USE |
| **Location** | ~/reports/ |
| **Error Type** | Used same incorrect source data |
| **Reported FTDs** | 68,803 (WRONG) |
| **Actual FTDs** | ~17,895 (per Power BI) |

**Note:** This was a "corrected" version that fixed the direction error but still used the same inflated data.

---

## CORRECT DATA (Source: Power BI 18_iGaming_360v1.11)

| Period | FTDs/Goals | Notes |
|--------|------------|-------|
| 4 months ago (Sep 2025) | 2,105 | Baseline |
| 3 months ago (Oct 2025) | 3,373 | +60% growth |
| 2 months ago (Nov 2025) | 4,429 | +31% growth |
| 1 month ago (Dec 2025) | 4,767 | +8% growth (slowing) |
| Current MTD (Jan 2026) | 3,221 | Tracking below prior month |
| **Total** | **17,895** | (Not 68,803) |

---

## ROOT CAUSE

**Most Likely Cause:** Query used SIGNUPS field instead of FTD/CONVERSIONS field.

Signups are typically 3-5x higher than FTDs in the conversion funnel:
- Clicks → Signups → FTDs → Revenue

This would explain the ~4x inflation in reported numbers.

---

## REPLACEMENT REPORT

**Valid Report:** FTD_STAGNATION_ANALYSIS_v5.0_2026-01-28.md
**Status:** DataGuard v2.0 Validated
**Location:** ~/reports/

---

## PREVENTION MEASURES

New DataGuard Rules 28-32 have been implemented to prevent recurrence:
- Rule 28: Source of Truth Validation
- Rule 29: Metric Field Verification
- Rule 30: Sanity Check Thresholds
- Rule 31: Dual-Source Verification
- Rule 32: Report Sign-off Checklist

---

**Director Sign-off:** Confirmed
**Date:** 2026-01-28

*BlackTeam Data Integrity | Paradise Media Group*
