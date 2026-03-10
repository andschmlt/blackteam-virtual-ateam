# PostHog Analysis Rules

Consolidated rules for all PostHog analytics work. Referenced by `/posthog_analysis` command.

**Version:** 1.0
**Last Updated:** 2026-02-04

---

## Rule Index

| Rule # | Name | Category | Added |
|--------|------|----------|-------|
| R1 | PDF Output | Output | Original |
| R2 | Table Page Breaks | Output | Original |
| R8 | Head of Product Assignment | Process | Original |
| R18 | NavBoost Metrics Inventory | Data | 2026-01-28 |
| R27 | Project Discovery | API | 2026-01-28 |
| R32 | Query Template | Technical | 2026-01-29 |

---

## Rule R1: PDF Output (MANDATORY)

All analysis reports MUST be generated as PDF in addition to markdown.

**Requirements:**
- Use ReportLab with Paradise Media branding (orange #f97316, black #1a1a1a)
- Professional headers/footers with BlackTeam branding
- Tables must use alternating row colors (gray #f3f4f6 for even rows)

---

## Rule R2: Table Page Breaks

Tables MUST NOT be split across pages.

**Implementation:**
- Use `KeepTogether` wrapper in ReportLab
- Add page breaks before tables that won't fit
- Each domain section starts on a new page

---

## Rule R8: Head of Product Assignment

Head of Product MUST be involved in ALL PostHog analytics work.

**When Invoked:**
1. Head of Product is automatically assigned to the task
2. Analysis reports MUST include a "Product Insights" section
3. HoP reviews metric interpretation and strategic implications

---

## Rule R18: NavBoost Metrics Inventory (18 Metrics)

ALL reports MUST include the complete 18-metric NavBoost inventory with Source column.

### Mandatory Metrics Table

| # | Metric | Source Event | Source Property | Target |
|---|--------|--------------|-----------------|--------|
| 1 | Dwell Time (avg) | `navboost:session_end` | `properties.dwell_time_seconds` | >90s |
| 2 | Pogo Rate | `navboost:session_end` | `properties.is_pogo` | <18% |
| 3 | Scroll Depth (25%) | `navboost:scroll_zone` | count where depth=25 | - |
| 4 | Scroll Depth (50%) | `navboost:scroll_zone` | count where depth=50 | - |
| 5 | Scroll Depth (75%) | `navboost:scroll_zone` | count where depth=75 | - |
| 6 | Scroll Depth (100%) | `navboost:scroll_zone` | count where depth=100 | - |
| 7 | CTA Visible | `navboost:cta_visible` | event count | - |
| 8 | CTA Clicks | `navboost:cta_click` | event count | - |
| 9 | CTA CTR | Calculated | #8 / #7 * 100 | >5% |
| 10 | Good Abandonment | `navboost:session_end` | `properties.is_good_abandonment` | >15% |
| 11 | Session Starts | `navboost:session_start` | event count | - |
| 12 | Session Ends | `navboost:session_end` | event count | - |
| 13 | SERP Return Rate | `navboost:session_end` | = Pogo Rate (Google traffic) | <25% |
| 14 | Engagement Score | Calculated | See formula below | >70 |
| 15 | Outbound Clicks | `navboost:session_end` | `properties.outbound_clicks` | - |
| 16 | Heartbeat Events | `navboost:heartbeat` | event count | - |
| 17 | Toplist Row Visible | `navboost:toplist_row_visible` | event count (if applicable) | N/A |
| 18 | Session Time (avg) | `navboost:session_end` | = Dwell Time (#1) | >60s |

### Display Rules
- Never show "NOT TRACKED" if data exists in event properties
- Query event COUNTS first, then query PROPERTIES from session_end
- Show "0" if metric tracked but no data
- Show "N/A" if not applicable to domain

**Reports missing ANY metric are flagged as INCOMPLETE.**

---

## Rule R27: Project Discovery

ALWAYS query PostHog API to discover projects. NEVER rely on hardcoded lists.

**Discovery Command:**
```bash
curl -s "https://us.i.posthog.com/api/projects/" \
  -H "Authorization: Bearer $POSTHOG_PERSONAL_API_KEY" | python3 -c "
import json,sys
for p in json.load(sys.stdin):
    print(f'ID: {p[\"id\"]} | Name: {p[\"name\"]}')"
```

---

## Rule R32: Query Template (MANDATORY)

All PostHog queries MUST use the canonical template.

### Reference Files

| File | Location |
|------|----------|
| Query Template | `~/virtual-ateam/BlackTeam/projects/posthog-integration/POSTHOG_QUERY_TEMPLATE.md` |
| Metrics Library | `~/virtual-ateam/BlackTeam/projects/posthog-integration/lib/posthog_metrics_lib.py` |

### Usage

```python
import sys
sys.path.insert(0, '/home/andre/virtual-ateam/BlackTeam/projects/posthog-integration/lib')
from posthog_metrics_lib import PostHogMetrics

metrics = PostHogMetrics()
data = metrics.get_complete_metrics(project_id=291573)
```

### FORBIDDEN Patterns (Cause NULL Results)

```sql
-- WRONG: These patterns return NULL
toFloat64OrNull(toString(properties.X))
toString(properties.X) = 'true'
```

### CORRECT Patterns

```sql
-- CORRECT: Direct property access
properties.X
properties.X = true
```

---

## NavBoost Thresholds Reference

| Metric | Target | Good | Excellent | Critical |
|--------|--------|------|-----------|----------|
| Pogo Rate | < 18% | < 15% | < 10% | > 25% |
| Dwell Time | > 90s | > 120s | > 180s | < 30s |
| Scroll (CTA Zone) | > 70% | > 75% | > 85% | < 50% |
| Scroll (Below Fold) | > 40% | > 50% | > 60% | < 25% |
| CTA CTR | > 5% | > 7% | > 10% | < 2% |
| Good Abandonment | > 15% | > 20% | > 25% | < 8% |
| Engagement Score | > 70 | > 75 | > 80 | < 50 |

---

## Engagement Score Formula

```
Engagement Score = (
  0.35 * min(dwell_time / 90 * 100, 100) +
  0.25 * (100 - pogo_rate) +
  0.15 * scroll_50_percent_rate +
  0.15 * cta_ctr_normalized +
  0.10 * good_abandonment_rate
)
```

---

*Reference: DIRECTOR_RULES.md Rules 1, 2, 8, 18, 27, 32*
