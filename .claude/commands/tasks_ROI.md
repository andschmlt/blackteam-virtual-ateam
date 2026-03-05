# Tasks ROI Analysis Command

## Command: /tasks_ROI

**Purpose:** Analyze ClickUp task or domain performance with ROI metrics. Shows actual $ values AND %GT (percentage of Grand Total).

**Input:** Task ID (e.g., `86aej4yvf`) OR Domain (e.g., `snjtoday.com`) OR ClickUp List URL

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before ROI analysis.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/.claude/standards/VALIDATION_STANDARDS.md` — Pre-response checklist

**RAG Query:**
```python
import sys; sys.path.insert(0, "/home/andre/AS-Virtual_Team_System_v2/rag")
from rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("ROI analysis tasks revenue FTD", top_k=5)
learnings = rag.query("data accuracy corrections numerical comparison", collection_name="learnings", top_k=3)
```

---

## Production Engine (v2.0.0 - Feb 3, 2026)

**Engine:** `/home/andre/scripts/tasks_roi_engine.py`
- Complete Python implementation with all rules locked
- **Master List v1.0 COMPLIANT** - uses `summary` schema
- Tables: `ARTICLE_PERFORMANCE`, `ARTICLE_SEO`, `SEO_PERFORMANCE`
- FTDs column: `FTD` (summary naming)
- Join: `ARTICLE_KEY` + `DATE` (summary surrogate keys)
- ClickUpAPI client with LIVE status filtering
- PDF report generation with reportlab
- CLI entry point for automation

**Weekly Scheduler:** Cloud Run Job `tasks-roi-engine-v2` via `tasks-roi-weekly-v2`
- Schedule: Monday 16:00 UTC
- Auto-processes ClickUp list `901323685943`
- Posts ROI comments with ACTUAL BigQuery data (no estimates)
- ALWAYS posts full YTD comment regardless of changes

**Daily Delta Scheduler:** Same Cloud Run Job via `tasks-roi-daily-v2`
- Schedule: Daily 22:00 Europe/Malta (10pm Malta time, auto CET/CEST)
- Compares current YTD metrics against previous day snapshot (GCS)
- If metrics changed: posts full ROI comment
- If no change: posts "Nothing changed from yesterday"
- Snapshot stored at `gs://paradisemedia-bi-tasks-roi/snapshots/latest.json`
- Sanity guards: aborts if grand totals drop >50% (likely BQ data issue)

**Grand Totals (YTD 2026 - from summary schema):**
- Commission: **$2,836,102.96**
- Clicks: **716,842**
- FTDs: **5,418**

**MASTER LIST REFERENCE:** `/home/andre/.claude/MASTER_LIST_v1.0.md`

---

## HARD RULES (MANDATORY)

### Rule 0: BlackTeam Execution (MANDATORY)
- **ALWAYS execute /tasks_ROI under BlackTeam Director oversight**
- Follow all /blackteam workflow phases (Brief → Approval → Execution → Delivery)
- Director must confirm workflow before execution begins
- Log activities to team activity system when available
- Post completion summary to ClickUp as per BlackTeam rules

### Rule 1: BigQuery ONLY - Master List v1.0 Compliant
- **ONLY use BigQuery (`paradisemedia-bi.summary`)** for all data queries
- **NEVER use `lakehouse` or `reporting` schema** (Rule R7, R20 from Master List)
- All queries must target `summary.*` tables
- Tables: `ARTICLE_PERFORMANCE`, `ARTICLE_SEO`, `SEO_PERFORMANCE`, `DOMAIN_PERFORMANCE`
- FTDs stored in `FTD` column | Signups in `NRC` column | Date in `DATE` (DATE type, not INT)

### Rule 2: URL Discovery Workflow
For each task, follow this sequence to find the LIVE URL:
1. Check `LIVE_URL` custom field in ClickUp task
2. If not found, scan task **description** for URLs (look for "Content Draft: domain.com/path")
3. If not found, fetch task **comments** and scan for URLs
4. If URL found is a staging/preview URL (contains "staging", "preview", "draft"), mark as **PRE-LIVE** and skip analysis
5. If LIVE URL found, proceed to data lookup

### Rule 3: Revenue Lookup Workflow
When LIVE URL is found:
1. First try: Match via `ARTICLE_PERFORMANCE` using `TASK_ID`
2. If not found: Query by LIVE_URL path match in `ARTICLE_PERFORMANCE`
3. If not found: Query by domain via `DOMAIN_PERFORMANCE`
4. If still not found: Report as "No tracking data - verify tracking links are implemented"

### Rule 4: Pre-Publication Handling
- If task has no LIVE URL and no tracking data → Status: **PRE-LIVE**
- Do NOT run performance analysis for PRE-LIVE tasks
- Show benchmark data only with "POTENTIAL" label
- State clearly: "Task is PRE-LIVE - no actual performance data available"

### Rule 5: Revenue Display Prompt (MANDATORY)
**ALWAYS prompt user before analysis:**
```
AskUserQuestion:
- question: "How should revenue metrics be displayed?"
- header: "Display"
- options:
  1. "Both $ and %GT (Recommended)" - Shows actual dollars AND percentage of grand total
  2. "%GT Only" - Only percentage of grand total (hides actual values)
  3. "$ Only" - Only actual dollar amounts
```
Applies to: Commission, Fixed Fees, Costs, Revenue

### Rule 6: LIVE Status Filter (MANDATORY)
- **ONLY analyze tasks where status CONTAINS "live"** (case-insensitive)
- This includes: "LIVE", "Live", "live", "Live needs SEO Check", "LIVE - Review", etc.
- **EXCLUDE** tasks with status: "Draft", "In Progress", "Ready for Review", "Archived", etc.
- When fetching from ClickUp list, filter by status before processing

### Rule 7: Efficiency First
- Use parallel BigQuery queries where possible
- Cache Grand Totals at start of session
- Skip WebFetch for PRE-LIVE tasks
- Target < 5 minutes for single task analysis
- Target < 15 minutes for list of 20 tasks

### Rule 8: Analysis Folder Output (MANDATORY)
- **ALL PDF analysis files MUST be saved to `/home/andre/analysis/`**
- This folder is symlinked to Windows: `C:\Users\andre\analysis\`
- **Exception:** Project-specific deliverables go to the project folder
- Naming convention: `YYYY-MM-DD_description.pdf` or `{Report_Name}_YTD{YEAR}.pdf`
- Do NOT save analysis PDFs to CU_TASK_ROI or other working directories

---

## OPTIMIZED WORKFLOW

### Phase 0: Input Validation & Setup (< 30 seconds)

#### Step 0.1: Parse Input
Determine input type:
- **Task ID**: Alphanumeric string (e.g., `86aej4yvf`)
- **Domain**: Contains `.` (e.g., `abc.com`)
- **ClickUp List URL**: Contains `clickup.com` with list ID

#### Step 0.2: Load Config & Cache Grand Totals

```bash
# Read ClickUp API key
cat ~/.claude/clickup_config.json
```

```sql
-- Cache Grand Totals ONCE at session start (run immediately)
SELECT
  SUM(TOTAL_COMMISSION_USD) as gt_commission,
  SUM(CLICKS) as gt_clicks,
  SUM(FTD) as gt_ftd
FROM `paradisemedia-bi.summary.ARTICLE_PERFORMANCE`
WHERE DATE BETWEEN '{START_DATE}' AND '{END_DATE}'
```

#### Step 0.3: Prompt for Date Range

```
AskUserQuestion:
- question: "Select the date range for analysis:"
- options:
  1. "YTD - Year to Date (Recommended)" - January 1 to today
  2. "MTD - Month to Date" - Current month only
  3. "Last 2 Weeks" - Past 14 days
```

#### Step 0.4: Prompt for Revenue Display (MANDATORY - Rule 5)

```
AskUserQuestion:
- question: "How should revenue metrics (Commission, Fixed Fees, Costs) be displayed?"
- header: "Display"
- options:
  1. "Both $ and %GT (Recommended)" - Shows actual dollars AND percentage of grand total
  2. "%GT Only" - Only percentage of grand total (hides actual values)
  3. "$ Only" - Only actual dollar amounts
```

#### Step 0.5: Filter Tasks by LIVE Status (MANDATORY - Rule 6)

When processing a ClickUp list, filter tasks:
```python
# Filter for LIVE status only
live_tasks = [
    task for task in all_tasks
    if "live" in task['status']['status'].lower()
]
# This captures: "LIVE", "Live needs SEO Check", "LIVE - Review", etc.
```

---

### Phase 1: Task Data Collection (< 1 minute per task)

#### Step 1.1: Fetch ClickUp Task Details

```bash
curl -s "https://api.clickup.com/api/v2/task/{TASK_ID}" \
  -H "Authorization: {CLICKUP_API_KEY}"
```

Extract:
- `name` - Task name
- `description` - Scan for URLs
- `custom_fields` - Look for LIVE_URL, DOMAIN
- `status` - Current status

#### Step 1.2: URL Discovery (MANDATORY WORKFLOW)

```python
# URL Discovery Priority:
1. live_url = custom_fields.get('LIVE_URL')
2. if not live_url:
     live_url = extract_url_from_description(description)
3. if not live_url:
     comments = fetch_task_comments(task_id)
     live_url = extract_url_from_comments(comments)
4. if live_url and is_staging_url(live_url):
     status = 'PRE-LIVE'
     skip_analysis = True
5. if not live_url:
     status = 'PRE-LIVE'
     skip_analysis = True
```

#### Step 1.3: Fetch Task Comments (if needed)

```bash
curl -s "https://api.clickup.com/api/v2/task/{TASK_ID}/comment" \
  -H "Authorization: {CLICKUP_API_KEY}"
```

---

### Phase 2: Performance Data Query (BigQuery ONLY)

#### Step 2.1: Find Article in BigQuery

```sql
-- Try to match by TASK_ID or LIVE URL
SELECT DISTINCT ARTICLE_KEY, TASK_ID, VERTICAL
FROM `paradisemedia-bi.summary.ARTICLE_PERFORMANCE`
WHERE TASK_ID = '{task_id}'
   OR LOWER(TASK_ID) LIKE LOWER('%{url_path}%')
LIMIT 1
```

#### Step 2.2: Revenue Lookup (Follow Rule 3)

```sql
-- Method 1: By ARTICLE_KEY (primary)
SELECT
  SUM(CLICKS) as clicks,
  SUM(NRC) as signups,
  SUM(FTD) as ftds,
  SUM(TOTAL_COMMISSION_USD) as commission
FROM `paradisemedia-bi.summary.ARTICLE_PERFORMANCE`
WHERE ARTICLE_KEY = {article_key}
  AND DATE BETWEEN '{START_DATE}' AND '{END_DATE}'
```

```sql
-- Method 2: By TASK_ID (if ARTICLE_KEY not found)
SELECT
  SUM(CLICKS) as clicks,
  SUM(NRC) as signups,
  SUM(FTD) as ftds,
  SUM(TOTAL_COMMISSION_USD) as commission
FROM `paradisemedia-bi.summary.ARTICLE_PERFORMANCE`
WHERE TASK_ID = '{task_id}'
  AND DATE BETWEEN '{START_DATE}' AND '{END_DATE}'
```

```sql
-- Method 3: By DOMAIN_KEY (domain-level fallback)
SELECT
  SUM(CLICKS) as clicks,
  SUM(NRC) as signups,
  SUM(FTD) as ftds,
  SUM(TOTAL_COMMISSION_USD) as commission
FROM `paradisemedia-bi.summary.ARTICLE_PERFORMANCE`
WHERE DOMAIN_KEY = {domain_key}
  AND DATE BETWEEN '{START_DATE}' AND '{END_DATE}'
```

#### Step 2.3: Get SEO/Keyword Data

```sql
-- Keyword positions and traffic (summary.SEO_PERFORMANCE)
SELECT
  COUNT(DISTINCT KEYWORD) as keywords_tracked,
  SUM(CASE WHEN ACCURANKER_RANK = 1 THEN 1 ELSE 0 END) as pos_1,
  SUM(CASE WHEN ACCURANKER_RANK BETWEEN 2 AND 5 THEN 1 ELSE 0 END) as pos_2_5,
  SUM(CASE WHEN ACCURANKER_RANK BETWEEN 6 AND 10 THEN 1 ELSE 0 END) as pos_6_10,
  SUM(GSC_CLICKS) as organic_traffic,
  SUM(ACCURANKER_SEARCH_VOLUME) as search_volume
FROM `paradisemedia-bi.summary.SEO_PERFORMANCE`
WHERE ARTICLE_KEY = {article_key}
  AND DATE >= '{START_DATE}'
```

---

### Phase 3: Generate Report

#### For LIVE Tasks (with data):

```markdown
## ROI Analysis: {TASK_NAME}

**Status:** LIVE
**Task ID:** {task_id}
**Live URL:** {live_url}

### ACTUAL PERFORMANCE (YTD 2026)

| Metric | Value | %GT |
|--------|-------|-----|
| Traffic | {N} | {X.XX%} |
| Clicks | {N} | {X.XX%} |
| Signups | {N} | {X.XX%} |
| FTDs | {N} | {X.XX%} |
| Commission | ${N} | {X.XX%} |

### SEO METRICS

| Metric | Value |
|--------|-------|
| Keywords Tracked | {N} |
| #1 Positions | {N} |
| #2-5 Positions | {N} |
| #6-10 Positions | {N} |
| Organic Traffic | {N} |

### BENCHMARK COMPARISON
[Include similar article benchmarks]
```

#### For PRE-LIVE Tasks (no data):

```markdown
## ROI Analysis: {TASK_NAME}

**Status:** PRE-LIVE
**Task ID:** {task_id}
**Live URL:** Not yet published

### ACTUAL PERFORMANCE
No data available - task is in pre-publication stage.

### POTENTIAL (Based on Similar Articles)

| Metric | Benchmark Potential |
|--------|---------------------|
| Keywords | {N} potential |
| Organic Traffic | {N} potential |
| Commission | Based on niche average |

**Next Steps:**
1. Publish content
2. Generate tracking links
3. Re-run analysis after 7 days
```

---

### Phase 4: ClickUp Comment Posting

Only post if user approves. Use markdown tables for clean formatting.

```bash
curl -X POST "https://api.clickup.com/api/v2/task/{TASK_ID}/comment" \
  -H "Authorization: {CLICKUP_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"comment_text": "{COMPACT_REPORT}"}'
```

---

## BigQuery Tables Reference (ONLY USE THESE — summary schema)

| Table | Purpose |
|-------|---------|
| `summary.ARTICLE_PERFORMANCE` | Revenue, clicks, FTDs, commission, TASK_ID, BRAND, VERTICAL |
| `summary.ARTICLE_SEO` | Core Web Vitals (LCP, INP, CLS), GA sessions, page views |
| `summary.SEO_PERFORMANCE` | Keyword rankings (Accuranker), GSC clicks, Ahrefs DR/backlinks |
| `summary.DOMAIN_PERFORMANCE` | Domain-level aggregated metrics, iGaming vs Growth splits |
| `summary.ARTICLE_INVOICES` | Article costs, DLC, ClickUp invoice, Fixed Fee |
| `summary.BRAND_PERFORMANCE` | Brand-level metrics (standalone — no article/domain joins) |
| `summary.PRODUCTION_CYCLE` | Article production workflow, cycle times |

**DO NOT USE:** `lakehouse`, `reporting`, Databricks, or Datalake tables.

---

## BigQuery Configuration

### Service Account (Required)
```bash
# CORRECT - Use this for BigQuery access
export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/bi-chatbot-sa.json
# Account: andre-claude@paradisemedia-bi.iam.gserviceaccount.com
```

### DO NOT USE
```bash
# WRONG - This is for Google Drive only, NO BigQuery access
# /home/andre/secrets/paradisemedia-bi-sa.json (papaya-drive-uploader)
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Task not in ClickUp | Verify task ID format |
| No LIVE_URL found | Mark as PRE-LIVE, show benchmarks only |
| URL not in DIM_PAGE | Try DYNAMIC or TASK_ID lookup |
| No revenue data | Check if tracking links implemented |
| BigQuery auth fail | Run `gcloud auth login` |

---

## Performance Targets

| Scope | Target Time |
|-------|-------------|
| Single task | < 5 minutes |
| List of 10 tasks | < 10 minutes |
| List of 20 tasks | < 15 minutes |
| Domain analysis | < 5 minutes |

---

## Changelog

- **2026-02-02 (v4):** Added Production Engine v1.0.0 (`/home/andre/scripts/tasks_roi_engine.py`)
- **2026-02-02 (v4):** Deployed Cloud Run Job `tasks-roi-weekly` for automated Monday submissions
- **2026-02-02 (v4):** Added 10 benchmark categories with topic detection
- **2026-02-02 (v4):** Updated Grand Totals: $1,707,391.23 commission | 269,742 clicks | 3,321 FTDs
- **2026-01-23 (v3):** Added Rule 0 - BlackTeam Director execution mandatory
- **2026-01-23 (v2):** Added MANDATORY prompt for revenue display ($ vs %GT vs both)
- **2026-01-23 (v2):** Added LIVE Status Filter - only tasks with status containing "live"
- **2026-01-23:** Added HARD RULES for BigQuery-only, URL discovery workflow, revenue lookup workflow
- **2026-01-23:** Added PRE-LIVE handling, efficiency optimizations
- **2026-01-23:** Added $ + %GT display option
- **2026-01-19:** Initial version with %GT-only display
