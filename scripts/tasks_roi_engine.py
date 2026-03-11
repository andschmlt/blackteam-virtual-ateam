#!/usr/bin/env python3
"""
=============================================================================
TASKS ROI ENGINE v2.0
=============================================================================
Comprehensive Python script for /tasks_ROI command execution.
All queries, rules, templates, and workflows are locked in this file.

Author: BlackTeam Director / WhiteTeam Validated
Created: 2026-02-02
Updated: 2026-02-03 (Master List v1.0 compliance - reporting schema)
Version: 2.0.0

IMPORTANT: DO NOT MODIFY QUERIES WITHOUT WHITETEAM APPROVAL
MASTER LIST: /home/andre/.claude/MASTER_LIST_v1.0.md
=============================================================================
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum

# =============================================================================
# CONFIGURATION - LOCKED
# =============================================================================

class Config:
    """Locked configuration - do not modify without approval"""

    # ClickUp API
    CLICKUP_CONFIG_PATH = os.path.expanduser("~/.claude/clickup_config.json")

    # BigQuery Project - MASTER LIST v1.0: Use summary ONLY
    BQ_PROJECT = "paradisemedia-bi"
    BQ_DATASET = "summary"  # NEVER use lakehouse or reporting (Rule R7, R20)

    # Output paths
    ANALYSIS_OUTPUT_DIR = os.path.expanduser("~/analysis")

    # Date format for BigQuery DATE column
    DATE_FORMAT = "%Y-%m-%d"

    @classmethod
    def get_clickup_api_key(cls) -> str:
        """Load ClickUp API key from environment or config file"""
        # Priority 1: Environment variable (Cloud Run Secret Manager)
        api_key = os.environ.get("CLICKUP_API_KEY")
        if api_key:
            return api_key

        # Priority 2: Config file (local development)
        try:
            with open(cls.CLICKUP_CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return config.get("CLICKUP_API_KEY")
        except FileNotFoundError:
            raise ValueError(
                "CLICKUP_API_KEY not found. Set environment variable or "
                f"create config file at {cls.CLICKUP_CONFIG_PATH}"
            )


# =============================================================================
# HARD RULES - LOCKED (from /tasks_ROI command spec)
# =============================================================================

class Rules:
    """
    HARD RULES - These rules are MANDATORY and must not be bypassed.
    Reference: /tasks_ROI command specification v3
    """

    RULE_0 = """
    Rule 0: BlackTeam Execution (MANDATORY)
    - ALWAYS execute /tasks_ROI under BlackTeam Director oversight
    - Follow all /blackteam workflow phases (Brief → Approval → Execution → Delivery)
    - Director must confirm workflow before execution begins
    """

    RULE_1 = """
    Rule 1: BigQuery ONLY - MASTER LIST v1.0 Compliant
    - ONLY use BigQuery (`paradisemedia-bi.summary`) for all data queries
    - NEVER use lakehouse or reporting schema (Rule R7, R20)
    - All queries must target `summary.*` tables
    - Tables: ARTICLE_PERFORMANCE (Rule R9) - single table, no joins needed
    """

    RULE_2 = """
    Rule 2: URL Discovery Workflow
    For each task, follow this sequence to find the LIVE URL:
    1. Check `LIVE_URL` custom field in ClickUp task
    2. If not found, scan task description for URLs
    3. If not found, fetch task comments and scan for URLs
    4. If URL is staging/preview, mark as PRE-LIVE and skip analysis
    5. If LIVE URL found, proceed to data lookup
    """

    RULE_3 = """
    Rule 3: Revenue Lookup Workflow - CRITICAL
    Match data by EXACT ClickUp Task ID:
    1. Primary: DYNAMIC field in DIM_ARTICLE = ClickUp Task ID
    2. Secondary: Query tracking parameters containing task ID
    3. NEVER match by task name keywords or domain aggregation
    """

    RULE_4 = """
    Rule 4: Pre-Publication Handling
    - If task has no LIVE URL and no tracking data → Status: PRE-LIVE
    - Do NOT run performance analysis for PRE-LIVE tasks
    - Show benchmark data only with "POTENTIAL" label
    """

    RULE_5 = """
    Rule 5: Revenue Display Prompt (MANDATORY)
    Always prompt user before analysis for display preference:
    - Both $ and %GT (default)
    - %GT Only
    - $ Only
    """

    RULE_6 = """
    Rule 6: LIVE Status Filter (MANDATORY)
    - ONLY analyze tasks where status CONTAINS "live" (case-insensitive)
    - EXCLUDE tasks with status: Draft, In Progress, Ready for Review, Archived
    """

    RULE_7 = """
    Rule 7: Efficiency First
    - Use parallel BigQuery queries where possible
    - Cache Grand Totals at start of session
    - Skip WebFetch for PRE-LIVE tasks
    """

    RULE_8 = """
    Rule 8: Analysis Folder Output (MANDATORY)
    - ALL PDF analysis files MUST be saved to ~/analysis/
    - Naming: YYYY-MM-DD_description.pdf
    """


# =============================================================================
# BIGQUERY QUERIES - LOCKED
# =============================================================================

class Queries:
    """
    LOCKED BigQuery queries - DO NOT MODIFY without WhiteTeam approval.
    All queries use exact ClickUp Task ID matching.

    MASTER LIST v1.0 COMPLIANCE:
    - Schema: paradisemedia-bi.summary (Rule R7)
    - Table: ARTICLE_PERFORMANCE (single table, no joins)
    - FTDs column: FTD
    - Signups column: NRC
    - Date column: DATE (DATE type)
    - Task ID: TASK_ID (direct match)
    """

    # -------------------------------------------------------------------------
    # Query 1: Grand Totals (for %GT calculations)
    # -------------------------------------------------------------------------
    GRAND_TOTALS = """
    SELECT
        SUM(TOTAL_COMMISSION_USD) as gt_commission,
        SUM(CLICKS) as gt_clicks,
        SUM(FTD) as gt_ftd,
        SUM(NRC) as gt_signups
    FROM `{project}.{dataset}.ARTICLE_PERFORMANCE`
    WHERE DATE BETWEEN '{start_date}' AND '{end_date}'
    """

    # -------------------------------------------------------------------------
    # Query 2: Task Performance by EXACT ClickUp Task ID
    # Single table query against summary.ARTICLE_PERFORMANCE
    # -------------------------------------------------------------------------
    TASK_PERFORMANCE_BY_ID = """
    WITH clickup_tasks AS (
        {task_id_unions}
    )
    SELECT
        ct.task_id as CLICKUP_TASK_ID,
        ap.TASK_ID,
        ap.TASK_NAME as BQ_TASK_NAME,
        ap.LIVE_URL,
        ap.DOMAIN,
        ap.NICHE,
        ap.VERTICAL,
        COALESCE(SUM(ap.CLICKS), 0) as clicks,
        COALESCE(SUM(ap.NRC), 0) as signups,
        COALESCE(SUM(ap.FTD), 0) as ftds,
        COALESCE(SUM(ap.TOTAL_COMMISSION_USD), 0) as commission
    FROM clickup_tasks ct
    LEFT JOIN `{project}.{dataset}.ARTICLE_PERFORMANCE` ap
        ON ct.task_id = ap.TASK_ID
        AND ap.DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY 1, 2, 3, 4, 5, 6, 7
    ORDER BY commission DESC
    """

    # -------------------------------------------------------------------------
    # Query 3: Article Lookup by TASK_ID (backup)
    # -------------------------------------------------------------------------
    ARTICLE_BY_TASK_ID = """
    SELECT DISTINCT
        TASK_ID,
        TASK_NAME,
        LIVE_URL,
        DOMAIN,
        NICHE,
        VERTICAL,
        STATUS
    FROM `{project}.{dataset}.ARTICLE_PERFORMANCE`
    WHERE TASK_ID = '{task_id_value}'
    LIMIT 1
    """

    # -------------------------------------------------------------------------
    # Query 4: SEO/Keyword Data - REMOVED per Master List Rule R13
    # SEO data (rankings, volume, backlinks) ALWAYS comes from DataForSEO API
    # NEVER from BigQuery. This query is deprecated and should not be used.
    # -------------------------------------------------------------------------
    # KEYWORD_STATS = DEPRECATED - Use DataForSEO API instead (Rule R13)

    @classmethod
    def build_task_id_unions(cls, task_ids: List[str]) -> str:
        """Build UNION ALL statement for task IDs"""
        unions = []
        for i, task_id in enumerate(task_ids):
            if i == 0:
                unions.append(f"SELECT '{task_id}' as task_id")
            else:
                unions.append(f"SELECT '{task_id}'")
        return " UNION ALL ".join(unions)

    @classmethod
    def get_grand_totals_query(cls, start_date: str, end_date: str) -> str:
        """Get formatted Grand Totals query"""
        return cls.GRAND_TOTALS.format(
            project=Config.BQ_PROJECT,
            dataset=Config.BQ_DATASET,
            start_date=start_date,
            end_date=end_date
        )

    @classmethod
    def get_task_performance_query(cls, task_ids: List[str],
                                    start_date: str, end_date: str) -> str:
        """Get formatted Task Performance query"""
        task_unions = cls.build_task_id_unions(task_ids)
        return cls.TASK_PERFORMANCE_BY_ID.format(
            project=Config.BQ_PROJECT,
            dataset=Config.BQ_DATASET,
            task_id_unions=task_unions,
            start_date=start_date,
            end_date=end_date
        )


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TaskPerformance:
    """Task performance data container - Master List v1.0 compliant"""
    clickup_task_id: str
    clickup_task_name: str
    bq_task_id: Optional[str]  # TASK_ID from ARTICLE_PERFORMANCE
    bq_task_name: Optional[str]
    live_url: Optional[str]
    domain: Optional[str]
    niche: Optional[str]
    vertical: Optional[str]
    clicks: int
    signups: int
    ftds: int  # FTD column (summary schema)
    commission: float

    @property
    def epf(self) -> float:
        """Earnings Per FTD"""
        return self.commission / self.ftds if self.ftds > 0 else 0.0

    @property
    def status(self) -> str:
        """Task status based on performance"""
        if self.commission > 0:
            return "GENERATING"
        elif self.clicks > 0:
            return "PRE-REVENUE"
        else:
            return "NO_DATA"


@dataclass
class GrandTotals:
    """Grand totals for %GT calculations"""
    commission: float
    clicks: int
    ftds: int
    signups: int


class DisplayMode(Enum):
    """Revenue display modes"""
    BOTH = "both"  # $ and %GT
    PCT_ONLY = "pct"  # %GT only
    DOLLAR_ONLY = "dollar"  # $ only


class DateRange(Enum):
    """Predefined date ranges"""
    YTD = "ytd"
    MTD = "mtd"
    LAST_30_DAYS = "last_30"
    LAST_14_DAYS = "last_14"


# =============================================================================
# BIGQUERY EXECUTOR
# =============================================================================

class BigQueryExecutor:
    """Execute BigQuery queries via google-cloud-bigquery Python client"""

    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy-init BigQuery client (reused across queries)"""
        if cls._client is None:
            from google.cloud import bigquery
            cls._client = bigquery.Client(project=Config.BQ_PROJECT)
        return cls._client

    @staticmethod
    def execute(query: str) -> List[Dict]:
        """Execute a BigQuery query and return results as list of dicts"""
        client = BigQueryExecutor._get_client()
        query_job = client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]

    @classmethod
    def get_grand_totals(cls, start_date: str, end_date: str) -> GrandTotals:
        """Get grand totals for the date range"""
        query = Queries.get_grand_totals_query(start_date, end_date)
        results = cls.execute(query)

        if not results:
            raise Exception("Failed to get grand totals")

        row = results[0]
        return GrandTotals(
            commission=float(row.get('gt_commission', 0) or 0),
            clicks=int(float(row.get('gt_clicks', 0) or 0)),
            ftds=int(float(row.get('gt_ftd', 0) or 0)),
            signups=int(float(row.get('gt_signups', 0) or 0))
        )

    @classmethod
    def get_task_performance(cls, task_ids: List[str],
                             start_date: str, end_date: str) -> List[Dict]:
        """Get performance data for specific task IDs"""
        query = Queries.get_task_performance_query(task_ids, start_date, end_date)
        return cls.execute(query)


# =============================================================================
# GCS SNAPSHOT STORAGE (for daily delta mode)
# =============================================================================

GCS_BUCKET = "paradisemedia-bi-tasks-roi"
GCS_SNAPSHOT_BLOB = "snapshots/latest.json"


class SnapshotStore:
    """Read/write daily metric snapshots to GCS for delta comparison."""

    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            from google.cloud import storage
            cls._client = storage.Client(project=Config.BQ_PROJECT)
        return cls._client

    @classmethod
    def load(cls) -> Optional[Dict]:
        """Load the previous day's snapshot. Returns None if no snapshot exists."""
        try:
            client = cls._get_client()
            bucket = client.bucket(GCS_BUCKET)
            blob = bucket.blob(GCS_SNAPSHOT_BLOB)
            if not blob.exists():
                return None
            return json.loads(blob.download_as_text())
        except Exception as e:
            print(f"Warning: Could not load snapshot from GCS: {e}")
            return None

    @classmethod
    def save(cls, snapshot: Dict) -> bool:
        """Save current metrics as the latest snapshot."""
        try:
            client = cls._get_client()
            bucket = client.bucket(GCS_BUCKET)
            blob = bucket.blob(GCS_SNAPSHOT_BLOB)
            blob.upload_from_string(
                json.dumps(snapshot, indent=2),
                content_type="application/json"
            )
            print(f"Snapshot saved to gs://{GCS_BUCKET}/{GCS_SNAPSHOT_BLOB}")
            return True
        except Exception as e:
            print(f"Error saving snapshot to GCS: {e}")
            return False

    @staticmethod
    def build_snapshot(performances: List['TaskPerformance']) -> Dict:
        """Build a snapshot dict from current performance data."""
        return {
            "timestamp": datetime.now().isoformat(),
            "tasks": {
                p.clickup_task_id: {
                    "clicks": p.clicks,
                    "signups": p.signups,
                    "ftds": p.ftds,
                    "commission": p.commission,
                }
                for p in performances
            }
        }

    @staticmethod
    def task_changed(current: Dict, previous: Dict) -> bool:
        """Compare a single task's metrics between snapshots."""
        return (
            current["clicks"] != previous.get("clicks", 0)
            or current["signups"] != previous.get("signups", 0)
            or current["ftds"] != previous.get("ftds", 0)
            or abs(current["commission"] - previous.get("commission", 0.0)) > 0.005
        )


# =============================================================================
# DATA SANITY GUARDS (lightweight WT-style validation for daily cron)
# =============================================================================

class SanityGuards:
    """Catch anomalous data before posting comments."""

    @staticmethod
    def check_grand_totals(current: 'GrandTotals', previous_snapshot: Optional[Dict]) -> Optional[str]:
        """Flag if grand totals dropped >50% vs previous snapshot (likely BQ data issue)."""
        if previous_snapshot is None:
            return None
        prev_tasks = previous_snapshot.get("tasks", {})
        if not prev_tasks:
            return None
        prev_commission = sum(t.get("commission", 0) for t in prev_tasks.values())
        if prev_commission > 0 and current.commission < prev_commission * 0.5:
            return (
                f"ANOMALY: Grand total commission ${current.commission:,.2f} is "
                f"<50% of previous snapshot ${prev_commission:,.2f}. "
                f"Possible BQ data issue — skipping daily post."
            )
        return None

    @staticmethod
    def check_ytd_regression(current_task: Dict, previous_task: Dict) -> Optional[str]:
        """Flag if YTD FTDs decreased (cumulative metric should never go down)."""
        if current_task["ftds"] < previous_task.get("ftds", 0):
            return (
                f"FTDs decreased from {previous_task['ftds']} to {current_task['ftds']} "
                f"(YTD should be cumulative)"
            )
        return None


# =============================================================================
# CLICKUP API
# =============================================================================

class ClickUpAPI:
    """ClickUp API client"""

    BASE_URL = "https://api.clickup.com/api/v2"

    def __init__(self):
        self.api_key = Config.get_clickup_api_key()
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def get_list_tasks(self, list_id: str, include_closed: bool = True) -> List[Dict]:
        """Get all tasks from a ClickUp list (handles pagination)"""
        url = f"{self.BASE_URL}/list/{list_id}/task"
        all_tasks = []
        page = 0

        while True:
            params = {"include_closed": str(include_closed).lower(), "page": str(page)}
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            response.raise_for_status()

            data = response.json()
            tasks = data.get('tasks', [])
            all_tasks.extend(tasks)

            if data.get('last_page', True) or not tasks:
                break
            page += 1

        return all_tasks

    def get_task(self, task_id: str) -> Dict:
        """Get a single task by ID"""
        url = f"{self.BASE_URL}/task/{task_id}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_task_comments(self, task_id: str) -> List[Dict]:
        """Get comments for a task"""
        url = f"{self.BASE_URL}/task/{task_id}/comment"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json().get('comments', [])

    def post_comment(self, task_id: str, comment_text: str) -> bool:
        """Post a comment to a task"""
        url = f"{self.BASE_URL}/task/{task_id}/comment"
        data = {"comment_text": comment_text}

        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            return response.status_code == 200
        except Exception as e:
            print(f"Error posting comment to {task_id}: {e}")
            return False

    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment by ID"""
        url = f"{self.BASE_URL}/comment/{comment_id}"
        try:
            response = requests.delete(url, headers=self.headers, timeout=30)
            return response.status_code == 200
        except Exception:
            return False

    def filter_live_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """Filter tasks by LIVE status (Rule 6)"""
        live_tasks = []
        for task in tasks:
            status = task.get('status', {}).get('status', '').lower()
            if 'live' in status or 'complete' in status:
                live_tasks.append(task)
        return live_tasks


# =============================================================================
# COMMENT TEMPLATES - LOCKED
# =============================================================================

class CommentTemplates:
    """
    Locked comment templates for ClickUp posting.
    DO NOT MODIFY without approval.
    """

    TASK_ROI_COMMENT = """📊 **ROI Analysis - {period_label}**

**Task ID:** {task_id}
**Task:** {task_name}
**Status:** {status}

### Performance Metrics ({date_range})

| Metric | Value |{pct_header}
|--------|-------|{pct_dashes}
| Clicks | {clicks:,} |{clicks_pct}
| Signups | {signups:,} |{signups_pct}
| FTDs | {ftds:,} |{ftds_pct}
| Commission | ${commission:,.2f} |{commission_pct}
| EPF | ${epf:,.2f} |

### Notes
{notes}

---
_Data Source: BigQuery reporting (TASK_ID={task_id}) | {timestamp}_"""

    PRE_LIVE_COMMENT = """📊 **ROI Analysis - {period_label}**

**Task ID:** {task_id}
**Task:** {task_name}
**Status:** PRE-LIVE / NO DATA

❌ **No performance data found**

**Possible reasons:**
- Task not yet published to LIVE URL
- Tracking links not yet implemented
- TASK_ID not registered in ARTICLE_INFORMATION

**Next Steps:**
1. Verify task has been published
2. Ensure tracking links contain task ID: {task_id}
3. Re-run analysis after 7 days

---
_Data Source: BigQuery reporting | {timestamp}_"""

    DAILY_NO_CHANGE_COMMENT = """📊 **Daily ROI Check — Nothing changed from yesterday.**
_Data Source: BigQuery reporting | {timestamp}_"""

    @classmethod
    def generate_task_comment(cls, perf: TaskPerformance,
                              grand_totals: GrandTotals,
                              display_mode: DisplayMode,
                              date_range_label: str) -> str:
        """Generate ROI comment for a task"""

        if perf.clicks == 0 and perf.ftds == 0 and perf.commission == 0:
            return cls.PRE_LIVE_COMMENT.format(
                period_label="YTD 2026",
                task_id=perf.clickup_task_id,
                task_name=perf.clickup_task_name,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
            )

        # Calculate percentages
        clicks_pct = (perf.clicks / grand_totals.clicks * 100) if grand_totals.clicks > 0 else 0
        signups_pct = (perf.signups / grand_totals.signups * 100) if grand_totals.signups > 0 else 0
        ftds_pct = (perf.ftds / grand_totals.ftds * 100) if grand_totals.ftds > 0 else 0
        commission_pct = (perf.commission / grand_totals.commission * 100) if grand_totals.commission > 0 else 0

        # Build percentage columns based on display mode
        if display_mode == DisplayMode.BOTH:
            pct_header = " %GT |"
            pct_dashes = "-----|"
            clicks_pct_str = f" {clicks_pct:.4f}% |"
            signups_pct_str = f" {signups_pct:.4f}% |"
            ftds_pct_str = f" {ftds_pct:.4f}% |"
            commission_pct_str = f" {commission_pct:.4f}% |"
        elif display_mode == DisplayMode.PCT_ONLY:
            pct_header = " %GT |"
            pct_dashes = "-----|"
            clicks_pct_str = f" {clicks_pct:.4f}% |"
            signups_pct_str = f" {signups_pct:.4f}% |"
            ftds_pct_str = f" {ftds_pct:.4f}% |"
            commission_pct_str = f" {commission_pct:.4f}% |"
        else:  # DOLLAR_ONLY
            pct_header = ""
            pct_dashes = ""
            clicks_pct_str = ""
            signups_pct_str = ""
            ftds_pct_str = ""
            commission_pct_str = ""

        # Generate notes
        if perf.commission > 0:
            notes = "✅ Task is generating revenue"
        elif perf.clicks > 0:
            notes = "⚠️ Task has clicks but no commission yet - verify tracking links & LIVE URL"
        else:
            notes = "❌ No tracking data - verify implementation"

        return cls.TASK_ROI_COMMENT.format(
            period_label="YTD 2026",
            task_id=perf.clickup_task_id,
            task_name=perf.clickup_task_name,
            status=perf.status,
            date_range=date_range_label,
            clicks=perf.clicks,
            signups=perf.signups,
            ftds=perf.ftds,
            commission=perf.commission,
            epf=perf.epf,
            pct_header=pct_header,
            pct_dashes=pct_dashes,
            clicks_pct=clicks_pct_str,
            signups_pct=signups_pct_str,
            ftds_pct=ftds_pct_str,
            commission_pct=commission_pct_str,
            notes=notes,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
        )


# =============================================================================
# PDF REPORT GENERATOR
# =============================================================================

class PDFReportGenerator:
    """Generate PDF reports using reportlab"""

    @staticmethod
    def generate_roi_report(performances: List[TaskPerformance],
                           grand_totals: GrandTotals,
                           list_name: str,
                           date_range_label: str,
                           output_path: str):
        """Generate comprehensive PDF report"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, cm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.enums import TA_CENTER
        except ImportError:
            print("reportlab not installed - skipping PDF generation")
            return None

        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1*cm
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a365d')
        )

        story = []

        # Title
        story.append(Paragraph("Tasks ROI Analysis Report", title_style))
        story.append(Paragraph(f"{date_range_label}", styles['Heading3']))
        story.append(Paragraph(f"List: {list_name} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))

        # Summary
        total_commission = sum(p.commission for p in performances)
        total_ftds = sum(p.ftds for p in performances)
        total_signups = sum(p.signups for p in performances)
        total_clicks = sum(p.clicks for p in performances)

        summary_data = [
            ['Metric', 'List Total', '% of Grand Total'],
            ['Commission', f'${total_commission:,.2f}', f'{total_commission/grand_totals.commission*100:.4f}%'],
            ['FTDs', f'{total_ftds:,}', f'{total_ftds/grand_totals.ftds*100:.2f}%'],
            ['Signups', f'{total_signups:,}', f'{total_signups/grand_totals.signups*100:.2f}%'],
            ['Clicks', f'{total_clicks:,}', f'{total_clicks/grand_totals.clicks*100:.2f}%'],
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        # Task details table
        task_data = [['Task ID', 'Task Name', 'Clicks', 'Signups', 'FTDs', 'Commission', 'EPF']]
        for p in sorted(performances, key=lambda x: x.commission, reverse=True):
            task_data.append([
                p.clickup_task_id,
                p.clickup_task_name[:30],
                f'{p.clicks:,}',
                f'{p.signups:,}',
                f'{p.ftds:,}',
                f'${p.commission:,.2f}',
                f'${p.epf:,.2f}'
            ])

        task_table = Table(task_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 0.8*inch, 0.6*inch, 1.2*inch, 1*inch])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#edf2f7')]),
        ]))
        story.append(task_table)

        doc.build(story)
        return output_path


# =============================================================================
# MAIN ENGINE
# =============================================================================

class TasksROIEngine:
    """
    Main engine for /tasks_ROI command execution.
    Orchestrates all components following locked rules and queries.
    """

    def __init__(self):
        self.clickup = ClickUpAPI()
        self.grand_totals: Optional[GrandTotals] = None
        self.performances: List[TaskPerformance] = []

    def get_date_range(self, date_range: DateRange) -> Tuple[str, str]:
        """Get start and end DATE strings (YYYY-MM-DD) for the selected range"""
        today = datetime.now()

        if date_range == DateRange.YTD:
            start = datetime(today.year, 1, 1)
            end = today
        elif date_range == DateRange.MTD:
            start = datetime(today.year, today.month, 1)
            end = today
        elif date_range == DateRange.LAST_30_DAYS:
            start = today - timedelta(days=30)
            end = today
        elif date_range == DateRange.LAST_14_DAYS:
            start = today - timedelta(days=14)
            end = today
        else:
            start = datetime(today.year, 1, 1)
            end = today

        return start.strftime(Config.DATE_FORMAT), end.strftime(Config.DATE_FORMAT)

    def analyze_list(self, list_id: str,
                     date_range: DateRange = DateRange.YTD,
                     display_mode: DisplayMode = DisplayMode.DOLLAR_ONLY) -> List[TaskPerformance]:
        """
        Analyze all LIVE tasks in a ClickUp list.

        This method follows all locked rules:
        - Rule 1: Uses BigQuery only
        - Rule 3: Matches by exact task ID (DYNAMIC field)
        - Rule 6: Filters for LIVE status only
        """

        # Get date range
        start_date, end_date = self.get_date_range(date_range)

        # Get grand totals (Rule 7: Cache at start)
        print("Loading Grand Totals...")
        self.grand_totals = BigQueryExecutor.get_grand_totals(start_date, end_date)
        print(f"  Commission: ${self.grand_totals.commission:,.2f}")
        print(f"  FTDs: {self.grand_totals.ftds:,}")

        # Get tasks from ClickUp
        print(f"\nFetching tasks from list {list_id}...")
        all_tasks = self.clickup.get_list_tasks(list_id)
        print(f"  Total tasks: {len(all_tasks)}")

        # Filter for LIVE status (Rule 6)
        live_tasks = self.clickup.filter_live_tasks(all_tasks)
        print(f"  LIVE tasks: {len(live_tasks)}")

        if not live_tasks:
            print("No LIVE tasks found.")
            return []

        # Extract task IDs and names
        task_map = {t['id']: t['name'] for t in live_tasks}
        task_ids = list(task_map.keys())

        # Query BigQuery with EXACT task IDs (Rule 3 - CRITICAL)
        print("\nQuerying BigQuery by exact task IDs...")
        bq_results = BigQueryExecutor.get_task_performance(task_ids, start_date, end_date)

        # Build performance objects (Master List v1.0 compliant — summary schema)
        self.performances = []
        for row in bq_results:
            clickup_id = row.get('CLICKUP_TASK_ID')
            perf = TaskPerformance(
                clickup_task_id=clickup_id,
                clickup_task_name=task_map.get(clickup_id, 'Unknown'),
                bq_task_id=row.get('TASK_ID'),
                bq_task_name=row.get('BQ_TASK_NAME'),
                live_url=row.get('LIVE_URL'),
                domain=row.get('DOMAIN'),
                niche=row.get('NICHE'),
                vertical=row.get('VERTICAL'),
                clicks=int(float(row.get('clicks', 0) or 0)),
                signups=int(float(row.get('signups', 0) or 0)),
                ftds=int(float(row.get('ftds', 0) or 0)),  # FTD column (summary)
                commission=float(row.get('commission', 0) or 0)
            )
            self.performances.append(perf)

        return self.performances

    def post_comments(self, display_mode: DisplayMode = DisplayMode.DOLLAR_ONLY,
                      date_range_label: str = "Jan 1 - Feb 2, 2026") -> Tuple[int, int]:
        """Post ROI comments to all analyzed tasks"""

        if not self.performances or not self.grand_totals:
            raise Exception("Run analyze_list first")

        success = 0
        failed = 0

        for perf in self.performances:
            comment = CommentTemplates.generate_task_comment(
                perf, self.grand_totals, display_mode, date_range_label
            )

            if self.clickup.post_comment(perf.clickup_task_id, comment):
                print(f"✓ Posted to {perf.clickup_task_id}: {perf.clickup_task_name[:40]}")
                success += 1
            else:
                print(f"✗ Failed: {perf.clickup_task_id}")
                failed += 1

            import time
            time.sleep(0.5)

        return success, failed

    def post_daily_delta(self, display_mode: DisplayMode = DisplayMode.DOLLAR_ONLY,
                         date_range_label: str = "YTD 2026") -> Tuple[int, int, int]:
        """
        Daily delta mode: compare current YTD metrics against previous snapshot.
        Posts full comment if changed, short 'nothing changed' if not.
        Returns (changed_count, unchanged_count, failed_count).
        """
        if not self.performances or not self.grand_totals:
            raise Exception("Run analyze_list first")

        # Load previous snapshot
        previous = SnapshotStore.load()

        # Sanity check: grand totals anomaly detection
        if previous is not None:
            anomaly = SanityGuards.check_grand_totals(self.grand_totals, previous)
            if anomaly:
                print(f"\n*** {anomaly}")
                print("*** Daily delta posting ABORTED. Monday run is unaffected.")
                return (0, 0, 0)

        # Build current snapshot
        current_snapshot = SnapshotStore.build_snapshot(self.performances)
        prev_tasks = previous.get("tasks", {}) if previous else {}

        changed = 0
        unchanged = 0
        failed = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        for perf in self.performances:
            task_id = perf.clickup_task_id
            current_metrics = current_snapshot["tasks"].get(task_id, {})
            prev_metrics = prev_tasks.get(task_id, {})

            # Sanity: check for YTD regression
            if prev_metrics:
                regression = SanityGuards.check_ytd_regression(current_metrics, prev_metrics)
                if regression:
                    print(f"  ! {task_id}: {regression} — posting anyway with warning")

            if not prev_metrics or SnapshotStore.task_changed(current_metrics, prev_metrics):
                # Metrics changed (or first run) — post full comment
                comment = CommentTemplates.generate_task_comment(
                    perf, self.grand_totals, display_mode, date_range_label
                )
                if self.clickup.post_comment(task_id, comment):
                    print(f"  + {task_id}: metrics changed — full comment posted")
                    changed += 1
                else:
                    print(f"  x {task_id}: FAILED to post")
                    failed += 1
            else:
                # No change — post short comment
                short = CommentTemplates.DAILY_NO_CHANGE_COMMENT.format(timestamp=timestamp)
                if self.clickup.post_comment(task_id, short):
                    print(f"  = {task_id}: nothing changed — short comment posted")
                    unchanged += 1
                else:
                    print(f"  x {task_id}: FAILED to post")
                    failed += 1

            import time
            time.sleep(0.5)

        # Save current snapshot for tomorrow's comparison
        SnapshotStore.save(current_snapshot)

        print(f"\nDaily delta summary: {changed} changed, {unchanged} unchanged, {failed} failed")
        return (changed, unchanged, failed)

    def generate_report(self, list_name: str,
                       date_range_label: str = "YTD 2026") -> Optional[str]:
        """Generate PDF report"""

        if not self.performances or not self.grand_totals:
            raise Exception("Run analyze_list first")

        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_path = os.path.join(
            Config.ANALYSIS_OUTPUT_DIR,
            f"{timestamp}_Tasks_ROI_Analysis.pdf"
        )

        return PDFReportGenerator.generate_roi_report(
            self.performances,
            self.grand_totals,
            list_name,
            date_range_label,
            output_path
        )

    def print_summary(self):
        """Print summary table to console"""

        if not self.performances:
            print("No data to display")
            return

        print("\n" + "="*80)
        print("TASKS ROI SUMMARY (Task-Level Data)")
        print("="*80)

        # Sort by commission descending
        sorted_perfs = sorted(self.performances, key=lambda x: x.commission, reverse=True)

        print(f"\n{'Task ID':<12} {'Task Name':<35} {'Clicks':>8} {'FTDs':>6} {'Commission':>12} {'EPF':>10}")
        print("-"*80)

        total_clicks = 0
        total_ftds = 0
        total_commission = 0

        for p in sorted_perfs:
            print(f"{p.clickup_task_id:<12} {p.clickup_task_name[:35]:<35} {p.clicks:>8,} {p.ftds:>6,} ${p.commission:>11,.2f} ${p.epf:>9,.2f}")
            total_clicks += p.clicks
            total_ftds += p.ftds
            total_commission += p.commission

        print("-"*80)
        print(f"{'TOTAL':<12} {'':<35} {total_clicks:>8,} {total_ftds:>6,} ${total_commission:>11,.2f}")
        print("="*80)

        if self.grand_totals:
            pct = total_commission / self.grand_totals.commission * 100
            print(f"\nList contribution: {pct:.4f}% of Grand Total (${self.grand_totals.commission:,.2f})")


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """CLI entry point for tasks_roi_engine.py"""
    import argparse

    parser = argparse.ArgumentParser(description='Tasks ROI Analysis Engine')
    parser.add_argument('--list-id', '-l', required=True, help='ClickUp list ID')
    parser.add_argument('--date-range', '-d', default='ytd',
                       choices=['ytd', 'mtd', 'last_30', 'last_14'],
                       help='Date range for analysis')
    parser.add_argument('--display', default='dollar',
                       choices=['both', 'pct', 'dollar'],
                       help='Revenue display mode')
    parser.add_argument('--post-comments', '-p', action='store_true',
                       help='Post comments to ClickUp tasks')
    parser.add_argument('--daily-delta', action='store_true',
                       help='Daily delta mode: only post full comment if metrics changed')
    parser.add_argument('--generate-pdf', '-g', action='store_true',
                       help='Generate PDF report')
    parser.add_argument('--list-name', default='ClickUp List',
                       help='List name for report')

    args = parser.parse_args()

    # Map args to enums
    date_range_map = {
        'ytd': DateRange.YTD,
        'mtd': DateRange.MTD,
        'last_30': DateRange.LAST_30_DAYS,
        'last_14': DateRange.LAST_14_DAYS
    }
    display_map = {
        'both': DisplayMode.BOTH,
        'pct': DisplayMode.PCT_ONLY,
        'dollar': DisplayMode.DOLLAR_ONLY
    }

    # Run analysis
    engine = TasksROIEngine()

    print("="*60)
    print("TASKS ROI ENGINE v2.0 (Master List v1.0 Compliant)")
    print("Schema: paradisemedia-bi.reporting")
    print("="*60)

    performances = engine.analyze_list(
        args.list_id,
        date_range=date_range_map[args.date_range],
        display_mode=display_map[args.display]
    )

    engine.print_summary()

    if args.daily_delta:
        print("\nRunning daily delta comparison...")
        changed, unchanged, failed = engine.post_daily_delta(
            display_mode=display_map[args.display]
        )
        print(f"Changed: {changed}, Unchanged: {unchanged}, Failed: {failed}")
    elif args.post_comments:
        print("\nPosting comments to ClickUp...")
        success, failed = engine.post_comments(
            display_mode=display_map[args.display]
        )
        print(f"Posted: {success}, Failed: {failed}")

    if args.generate_pdf:
        print("\nGenerating PDF report...")
        pdf_path = engine.generate_report(args.list_name)
        if pdf_path:
            print(f"Report saved: {pdf_path}")


if __name__ == "__main__":
    main()
