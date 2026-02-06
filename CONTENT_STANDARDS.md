# BlackTeam Content Standards

**Effective Date:** 2026-01-19
**Version:** 1.0
**Author:** The Director

---

## Core Principle

**100% Quality Pass Rate is Mandatory**

All content created or updated by BlackTeam must achieve 100% pass rate on quality checks. Rejection is only acceptable for truly unfixable issues (e.g., untrusted sources).

---

## Standard: Iterative Content Improvement

### Overview

When content fails quality assurance, the system must **automatically iterate** to fix issues and re-test until passing. This applies to:

- News articles
- Content updates
- Documentation
- Any written output

### Implementation

```
┌─────────────────────────────────────────────────────────────────────┐
│              ITERATIVE QA WORKFLOW (PARALLEL EXECUTION)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Content Created                                                   │
│         │                                                           │
│         ▼                                                           │
│   ┌─────────────────────────────────────────┐                       │
│   │  CYCLE 1: Director Review (SEQUENTIAL)  │                       │
│   │  • Source verification                  │                       │
│   │  • Fact-checking                        │                       │
│   │  Must pass FIRST (80+ score)            │                       │
│   └──────────────────┬──────────────────────┘                       │
│                      │                                              │
│                 PASS │                                              │
│                      │                                              │
│      ┌───────────────┴───────────────┐                              │
│      │                               │                              │
│      ▼                               ▼                              │
│   ┌─────────────────┐         ┌─────────────────┐                   │
│   │ CYCLE 2         │         │ CYCLE 3         │                   │
│   │ Content Review  │         │ SEO/QA Review   │                   │
│   │ (Head of Content)│  PARALLEL  │ (SEO + PPM)    │                   │
│   │ 80+ to pass     │         │ 80+ to pass     │                   │
│   └────────┬────────┘         └────────┬────────┘                   │
│            │                           │                            │
│            └───────────┬───────────────┘                            │
│                        │                                            │
│                   ALL PASS                                          │
│                        │                                            │
│                        ▼                                            │
│   ┌─────────────────────────────────────────┐                       │
│   │  CYCLE 4: Internal Link Gate (HARD)     │                       │
│   │  • ALL THREE sign off                   │                       │
│   │  • 0 broken links = PASS                │                       │
│   └──────────────────┬──────────────────────┘                       │
│                      │                                              │
│                 PASS │                                              │
│                      ▼                                              │
│            ┌─────────────────┐                                      │
│            │    APPROVED     │                                      │
│            │  Content saved  │                                      │
│            └─────────────────┘                                      │
│                                                                     │
│   ─────────────────────────────────────────────────────────────     │
│   FAIL HANDLING: Fix issues, re-run ONLY the failed cycle(s)       │
│   Cycles 2 & 3 can be re-run independently (not together)          │
│   ─────────────────────────────────────────────────────────────     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Max Iterations

- **Maximum:** 3 iterations per content item
- If content cannot pass after 3 iterations, it is rejected
- Rejected content requires manual review

### Fixable vs Unfixable Issues

| Issue Type | Fixable? | Action |
|------------|----------|--------|
| Summary too long | YES | Auto-truncate to 280 chars |
| Missing SEO keywords | YES | Auto-add relevant keyword |
| Missing category tag | YES | Add default category |
| Missing section headers | YES | Add ## Summary header |
| Unbalanced markdown | YES | Fix bracket/paren balance |
| Placeholder text | YES | Remove TBD/TODO markers |
| Untrusted source | NO | **REJECT** |
| Missing source citation | NO | **REJECT** |

---

## Quality Cycles (Ralph Loops)

### Cycle 1: Director Review
**Reviewer:** The Director
**Focus:** Strategic & Factual Integrity

| Check | Threshold | Fixable |
|-------|-----------|---------|
| Has source citation | Required | No |
| Trusted source | Required | No |
| Publication date | Required | Partial |
| No placeholders | Required | Yes |
| Quality title | Required | Yes |

### Cycle 2: Content Review
**Reviewer:** Head of Content
**Focus:** Quality & Structure

| Check | Threshold | Fixable |
|-------|-----------|---------|
| Adequate length | 500+ chars | No |
| Has structure | ## headers | Yes |
| Valid internal links | All working | **No** |
| Valid markdown | Balanced | Yes |
| Has summary | Required | Yes |

**IMPORTANT (2026-01-19):** "Valid internal links" is now a HARD REQUIREMENT. See Cycle 4 below.

### Cycle 3: SEO/QA Review
**Reviewer:** SEO Commander + Post Production Manager
**Focus:** Optimization & Validation

| Check | Threshold | Fixable |
|-------|-----------|---------|
| SEO meta ready | <300 chars | Yes |
| Has category | Required | Yes |
| Images valid | All exist | No |
| SEO keywords | In title | Yes |
| URL-friendly | NNN_slug | Yes |

### Cycle 4: Internal Link Quality Gate (Added: 2026-01-19)
**Reviewer:** SEO Commander + Head of Content + Post Production Manager (ALL THREE)
**Focus:** Internal Link Verification
**Status:** MANDATORY - NO EXCEPTIONS

| Check | Threshold | Fixable |
|-------|-----------|---------|
| Link map generated | Required | N/A |
| All link targets exist | 100% | No |
| No broken links | 0 broken | No |
| Anchors resolve | If used | No |

**Background:** WC 2026 project shipped with broken internal links. This was a shared failure by SEO Commander, Head of Content, and Post Production Manager. This cycle now exists to ensure this NEVER happens again.

**Process:**
1. **Generate Link Map:**
   ```
   Source File                 → Target Link                 → Status
   /players/messi.md           → /teams/argentina.md         → [CHECK]
   /tournaments/wc-2022.md     → /players/mbappe.md          → [CHECK]
   ```

2. **Verify Each Link:**
   - For markdown files: `[ -f "$target" ]` - file must exist
   - For URLs: HTTP 200 response required
   - For anchors (#section): heading must exist in target

3. **Report Results:**
   ```
   INTERNAL LINK VERIFICATION
   ==========================
   Total: 150 links
   Valid: 150 (100%)
   Broken: 0 (0%)

   STATUS: PASS ✓
   ```

4. **Gate Decision:**
   - **0 broken links** → PASS → May proceed to release
   - **>0 broken links** → FAIL → MUST fix before release (NO EXCEPTIONS)

**Accountability:**
| Role | When to Check | Sign-off Required |
|------|---------------|-------------------|
| SEO Commander | During link architecture review | Yes |
| Head of Content | During editorial review | Yes |
| Post Production Manager | During final QA | Yes |

**If any broken link ships to production, ALL THREE roles have failed.**

---

## Minimum Quality Score

**Threshold:** 80/100 per cycle

- Score = (Passed Checks / Total Checks) × 100
- All 3 cycles must achieve ≥80 to pass
- If <80, apply fixes and iterate

---

## Implementation Reference

### News Updates (BT-2026-001)

```python
# From wc_news_daily_update.py

class ContentImprover:
    """
    BLACKTEAM STANDARD: Iterative Content Improvement

    Automatically fixes content issues identified by Ralph Loops QA
    until 100% quality pass rate is achieved.
    """

    MAX_ITERATIONS = 3

    @staticmethod
    def improve_content(content, article_path, qa_report):
        # Route to appropriate fixer based on cycle
        if qa_report.cycle == 1:
            return ContentImprover._fix_director_issues(content, qa_report)
        elif qa_report.cycle == 2:
            return ContentImprover._fix_content_issues(content, qa_report)
        elif qa_report.cycle == 3:
            return ContentImprover._fix_seo_issues(content, article_path, qa_report)
```

### Key Locations

| Resource | Path |
|----------|------|
| Implementation | `WC_2026_Project/main/scripts/wc_news_daily_update.py` |
| Content Standards | `BlackTeam/CONTENT_STANDARDS.md` |
| Project Registry | `BlackTeam/PROJECT_REGISTRY.json` |

---

## Reporting

All content operations must report:

1. **Articles Fetched** - Total items processed
2. **Passed First Try** - No iteration needed
3. **Passed After Improvement** - Required iteration
4. **Rejected (Unfixable)** - Could not fix
5. **Fixes Applied** - List of automatic fixes

### Email Report Example

```
✅ WC 2026 Daily News Update Report
==================================================

Status: SUCCESS
Date: 2026-01-19

SUMMARY
-------
Articles Fetched: 2
Articles Passed QA: 2
  - First try: 1
  - After improvement: 1
Articles Added: 2
Articles Rejected: 0 (unfixable)

IMPROVEMENTS APPLIED (BlackTeam Standard)
-----------------------------------------

112_moroccos_regragui_calls_thiaw_shameful:
  Iterations: 2
    - Shortened summary from 500 to 281 chars
    - Added 'Football' keyword to title
```

---

## Compliance

This standard applies to ALL BlackTeam projects:

- [x] BT-2026-001: World Cup 2026 Content Hub
- [x] BT-2026-002: PostHog Analytics Platform Migration
- [x] BT-2026-003: Dragon - Cloak_Track_Agent

**All future projects must implement iterative content improvement.**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-19 | Initial standard established |
| 1.1 | 2026-01-19 | Added Cycle 4: Internal Link Quality Gate (MANDATORY) |
| 1.2 | 2026-01-21 | Parallel execution: Cycles 2 & 3 now run simultaneously after Cycle 1 passes. Failed cycles re-run independently. ~50% QA time reduction. |

---

*BlackTeam - Quality Without Compromise*
