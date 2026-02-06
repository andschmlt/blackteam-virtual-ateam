# /FTD_DEEPDIVE_ANALYSIS - Locked Framework Command

**Version:** 1.0
**Created:** 2026-01-28
**Owner:** Head of Analytics (Elias Thorne)
**Purpose:** Generate comprehensive FTD Deep Dive Analysis with MANDATORY sections

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before analysis.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings
- `~/.claude/standards/VALIDATION_STANDARDS.md` — Pre-response checklist

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("FTD analysis deep dive revenue", top_k=5)
learnings = rag.query("FTD data accuracy numerical validation", collection_name="learnings", top_k=3)
rules = rag.query("data sanity checks comparison validation", collection_name="rules", top_k=3)
```

---

## CRITICAL: THIS FRAMEWORK IS LOCKED

```
┌─────────────────────────────────────────────────────────────────┐
│  ⛔ MANDATORY COMPLIANCE - NO EXCEPTIONS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  This command generates the FTD Deep Dive Analysis report.      │
│  ALL sections listed below are MANDATORY.                       │
│                                                                  │
│  ❌ DO NOT skip any section                                     │
│  ❌ DO NOT summarize sections - include FULL detail             │
│  ❌ DO NOT omit Parts A, B, C, D from theories                  │
│  ❌ DO NOT reduce table rows to "top N" unless specified        │
│  ❌ DO NOT hallucinate data - validate against BigQuery         │
│                                                                  │
│  ✅ ALWAYS include all 19+ sections                             │
│  ✅ ALWAYS include per-domain breakdowns                        │
│  ✅ ALWAYS include URL-level analysis                           │
│  ✅ ALWAYS include specialist findings                          │
│  ✅ ALWAYS validate against BigQuery ARTICLE_PERFORMANCE        │
│                                                                  │
│  FAILURE TO COMPLY = REPORT REJECTED                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## DATA VALIDATION REQUIREMENTS

Before generating ANY data in this report:

1. **Source of Truth**: BigQuery `paradisemedia-bi.reporting.ARTICLE_PERFORMANCE`
2. **FTDs**: Use GOALS column (NOT SIGNUPS!)
3. **Signups**: Use SIGNUPS column (typically 3-5x higher than FTDs)
4. **Revenue**: Use TOTAL_COMMISSION_USD column
5. **Cross-check**: Validate row counts and totals before reporting

### BigQuery Configuration (MANDATORY)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/andre/secrets/bi-chatbot-sa.json
# Account: andre-claude@paradisemedia-bi.iam.gserviceaccount.com
```

**DO NOT USE:** `/home/andre/secrets/paradisemedia-bi-sa.json` (papaya-drive-uploader - NO BigQuery access)

### Primary Tables

| Table | Purpose |
|-------|---------|
| `reporting.ARTICLE_PERFORMANCE` | FTDs (GOALS), Signups, Commission |
| `reporting.ARTICLE_INFORMATION` | Article metadata, TASK_ID, LIVE_URL |
| `reporting.REPT_SEO_ACCURANKER` | Rankings, keyword positions |
| `reporting.REPT_SEO_AHREFS` | DR, backlinks, referring domains |

### Metric Definitions (MEMORIZE)

| Term | Aliases | Definition |
|------|---------|------------|
| FTD | Goals, Conversions | First-Time Deposit - actual money deposited |
| Signup | NRC, Registration | Account creation - NO money involved |
| Conversion Rate | Conv% | FTDs / Signups * 100 |

**CRITICAL**: Signups are typically 3-5x higher than FTDs. NEVER confuse them.

---

## MANDATORY REPORT SECTIONS

The report MUST contain ALL of the following sections in order:

### SECTION 1: TITLE PAGE
- Report title: "FTD DEEP DIVE ANALYSIS"
- Subtitle: "iGaming Vertical - O&O Domains Only"
- Analysis period
- Data sources (BigQuery primary, DataForSEO)
- Version number
- Lead Analyst: Elias Thorne
- BlackTeam consultation status

### SECTION 2: EXECUTIVE SUMMARY
- Overview paragraph
- Key Finding (one sentence)
- Root Cause identification
- Recommendation summary
- Key metrics grid (8 boxes minimum)

### SECTION 3: KEY METRICS TABLE
- Two-column metrics table
- Include: Total FTDs, Revenue, Domain count, URL count, Trends, Risk metrics

### SECTION 4: CONVERSION FUNNEL ANALYSIS
- Funnel definition: Impressions → Clicks → Signups → FTDs → Revenue
- Monthly funnel data table (Signups, FTDs, Conv Rate per month)
- Funnel visualization (professional chart)
- Conversion rate trend analysis

### SECTION 5: THEORY TEST SUMMARY
- Summary table with all theories
- Status, Impact, Priority for each

### SECTION 6: BLACKTEAM CONSULTATION SUMMARY
- Table of ALL personas engaged
- Columns: Persona, Role, Status, Key Contribution
- Minimum personas: Lead Analyst, SEO Commander, Head of Content, Content Manager, DataViz, Data Analyst, DataForge, Tech Lead

### SECTION 7: KEY SPECIALIST FINDINGS
- Individual finding blocks for each specialist
- Format: [PERSONA NAME - Role]: Finding text

### SECTION 8: THEORY 1 - CONTENT GAP ANALYSIS
**MUST INCLUDE ALL PARTS:**
- Part A: Available Metrics (table)
- Part B: Domain-Level Content Observations (list)
- Part C: Opportunity Scoring (table or pending note)
- Part D: Actionable Recommendations

### SECTION 9: THEORY 2 - SEO/AUTHORITY ISSUES
**MUST INCLUDE ALL PARTS:**
- Part A: Comprehensive SEO Metrics Table
  - Columns: Domain, Pages, Keywords, #1-3, #4-10, #11-20, UR, DR, UR/DR%, Zero UR
  - ALL domains, not just top N
- Part B: Domain-Specific Insights
  - Per-domain analysis with Authority Status
  - ACTION items per domain
- Part C: Opportunity Scoring (95th Percentile)
  - Elias Thorne Formula: Score = (Revenue Impact × 40%) + (Authority Deficit × 25%) + (Traffic Gap × 20%) + (Trend Impact × 15%)
  - Table with: Domain, FTDs, Revenue, Opp Score, Priority, Rev Gap, Auth Score, Traffic Gap
- Part D: Actionable Recommendations
  - P1 and P2 actions with specific targets

### SECTION 10: THEORY 3 - AI TRAFFIC EROSION
**MUST INCLUDE ALL PARTS:**
- AI Erosion Risk Classification Definitions (HIGH, MEDIUM, LOW)
- Part A: AI Erosion Risk Analysis Table
  - Columns: Domain, AvgRank, Top10%, Traffic, Capture%, FTDs, Risk, Explanation
- Part B: Domain-Specific AI Erosion Analysis
  - Per-domain recommendations
- Part C: AI-Adjusted Opportunity Scoring
  - Risk multiplier table
- Part D: Actionable Recommendations

### SECTION 11: THEORY 4 - "FREE" KEYWORD INTENT (NEW)
- Hypothesis explanation
- Supporting evidence (Signup vs FTD growth disparity)
- Keyword intent categories (HIGH vs LOW intent)
- Validation required
- Recommended actions

### SECTION 12: CONTENT TEAM ANALYSIS
- Content Freshness Analysis Table (by year)
- Winning Content Patterns Table (top keywords driving FTDs)
- Declining Content - Requires Refresh Table

### SECTION 13: SEO COMMANDER ANALYSIS
- Competitive Keyword Gaps Table
  - Columns: Keyword, Search Vol, Competitor, Their Rank, Our Domain, Our Rank, Gap
- Keyword Cannibalization Issues Table
  - Columns: Keyword, Domain, URLs Competing, Best Rank, Worst Rank, Search Vol

### SECTION 14: COMPREHENSIVE ACTION MATRIX
- Priority 1: Immediate Actions (7 Days)
- Priority 2: Short-Term Actions (30 Days)
- Priority 3: Medium-Term Actions (60 Days)
- Each action with: Target, Action, Owner, Success Metric, Expected Impact

### SECTION 15: CONTENT REFRESH QUEUE
- Domains Requiring Immediate Content Refresh Table
  - Columns: Domain, URLs to Refresh, FTD Decline, Total FTDs, Priority
- Top 20 URLs for Immediate Refresh Table
  - Columns: URL, Domain, Brand, Oct FTDs, Jan FTDs, Decline, Cause

### SECTION 16: DOMAIN-LEVEL ANALYSIS
- Root Cause Classification Legend
- FULL table of ALL O&O domains (43+)
  - Columns: Domain, FTDs, Revenue, Trend, Root Cause, Recommended Action
- DO NOT truncate to "top N" - include ALL domains

### SECTION 17: URL-LEVEL ANALYSIS - SEO PERFORMANCE
- Top URLs by SEO Metrics Table
  - Columns: Domain, URL Path, Keywords, AvgRank, Top3%, Top10%, Pg2%, Traffic, Authority Status
- Include 40+ URLs minimum

### SECTION 18: 95TH PERCENTILE URL ANALYSIS
- High Performers - Maintain & Optimize
  - Top 5 with specific actions to maintain
- Underperformers - Urgent Fix Required
  - Top 7+ with specific actions to fix
  - Include UR targets and backlink recommendations

### SECTION 19: QUICK WIN OPPORTUNITIES - PAGE 2 KEYWORDS
- Table of keywords ranked 11-20
  - Columns: Domain, Keyword, Rank, Traffic Potential, Difficulty, Opportunity
- Include 30+ keywords minimum
- Revenue opportunity calculation

### SECTION 20: RECOMMENDATIONS & ACTION PLAN
- Elias Thorne Root Cause Analysis Summary
- Funnel analysis result
- Priority 1: Immediate Actions (30 Days)
  - Specific URLs listed
  - Specific metrics and targets
- Priority 2: High Priority Actions (60 Days)
- Action Summary Table

### SECTION 21: DATA INTEGRITY CERTIFICATION
- Version comparison table (v4.1 invalid vs v6.0 correct)
- DataGuard v2.0 compliance checklist
- Sign-off block

### APPENDIX A: SOURCE DATA VALIDATION
- BigQuery source validation table
- Report metadata

---

## DESIGN REQUIREMENTS

Use PixelPerfect Design Standards:
- WCAG 2.1 AA compliant colors
- Professional matplotlib charts (not ASCII)
- Consistent table formatting
- Alert boxes for key insights
- Section headers with numbering

### Color Palette
```python
COLORS = {
    'primary': (0, 51, 102),      # Headers
    'secondary': (51, 51, 51),    # Body text
    'accent': (0, 122, 204),      # Highlights
    'success': (34, 139, 34),     # Positive
    'danger': (178, 34, 34),      # Negative/Warning
    'warning': (184, 134, 11),    # Caution
    'light_bg': (248, 249, 250),  # Backgrounds
    'table_header': (0, 51, 102), # Table headers
    'table_alt': (240, 248, 255), # Alt rows
}
```

---

## EXECUTION CHECKLIST

Before delivering the report, verify:

```
□ All 21 sections present
□ Theory 1 has Parts A, B, C, D
□ Theory 2 has Parts A, B, C, D with full SEO metrics table
□ Theory 3 has Parts A, B, C, D with AI risk analysis
□ Theory 4 (Free keyword) included
□ Conversion Funnel included with Signups data
□ BlackTeam consultation table included
□ Specialist findings included
□ All 43+ domains in domain-level analysis
□ 40+ URLs in URL-level analysis
□ 95th percentile analysis included
□ Quick win opportunities included
□ Content refresh queue included
□ Professional charts (not ASCII)
□ Data validated against BigQuery ARTICLE_PERFORMANCE
□ FTDs ≠ Signups verified
□ DataGuard certification complete
```

---

## HISTORICAL CONTEXT

### Why This Framework Exists

On 2026-01-28, multiple versions of the FTD report were delivered with missing sections:
- v4.1: Correct structure but WRONG DATA (used Signups instead of FTDs)
- v5.0-v5.2: Correct data but MISSING SECTIONS (theories, URL analysis, etc.)
- v5.3: Added funnel but still MISSING detailed breakdowns

This framework ensures the complete report is delivered every time.

### Data Correction Summary

| Metric | v4.1 (INVALID) | v6.0 (CORRECT) |
|--------|----------------|----------------|
| "Total FTDs" | 68,803 | 17,895 |
| Actual metric | Signups | FTDs |
| Source | BigQuery SIGNUPS (wrong) | BigQuery GOALS (correct) |

---

## TEMPLATE LOCATION

The report generation script is located at:
```
/home/andre/reports/FTD_DEEP_DIVE_ANALYSIS_v6.0_TEMPLATE.py
```

Use this as the base for all future FTD Deep Dive reports.

---

## OWNER & ACCOUNTABILITY

- **Owner**: Head of Analytics (Elias Thorne)
- **Reviewers**: Director, DataGuard
- **Approval Required**: Director sign-off before delivery
- **Rule Violations**: Escalate to Director immediately

---

**/FTD_DEEPDIVE_ANALYSIS v1.0 | Head of Analytics | BlackTeam**
