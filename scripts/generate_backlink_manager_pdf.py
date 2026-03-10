#!/usr/bin/env python3
"""Generate PDF: Paradise Backlink Manager — Stakeholder Review & Decision Document."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

OUTPUT_PATH = os.path.expanduser("~/projects/paradise-backlink-manager/BACKLINK_MANAGER_Stakeholder_Review_2026-02-25.pdf")

# Colors
DARK_GREEN = HexColor("#1a5c2e")
MED_GREEN = HexColor("#2d8a4e")
LIGHT_GREEN = HexColor("#e8f5e9")
HEADER_BG = HexColor("#1a5c2e")
ROW_ALT = HexColor("#f5f5f5")
BORDER_COLOR = HexColor("#cccccc")
RED_ACCENT = HexColor("#c0392b")
ORANGE_ACCENT = HexColor("#e67e22")
BLUE_ACCENT = HexColor("#2980b9")
LIGHT_RED = HexColor("#fdecea")
LIGHT_ORANGE = HexColor("#fef5e7")
LIGHT_BLUE = HexColor("#eaf2f8")

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm,
        leftMargin=2*cm,
        rightMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=DARK_GREEN,
        spaceAfter=4*mm,
    ))
    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=HexColor("#555555"),
        spaceAfter=2*mm,
    ))
    styles.add(ParagraphStyle(
        name='SectionH1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=DARK_GREEN,
        spaceBefore=8*mm,
        spaceAfter=4*mm,
    ))
    styles.add(ParagraphStyle(
        name='SectionH2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=MED_GREEN,
        spaceBefore=5*mm,
        spaceAfter=3*mm,
    ))
    styles.add(ParagraphStyle(
        name='SectionH3',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=HexColor("#333333"),
        spaceBefore=3*mm,
        spaceAfter=2*mm,
    ))
    styles.add(ParagraphStyle(
        name='BodyText2',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=HexColor("#333333"),
        spaceAfter=2*mm,
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=white,
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name='AnswerCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=HexColor("#999999"),
    ))
    styles.add(ParagraphStyle(
        name='FooterNote',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=HexColor("#888888"),
        spaceAfter=2*mm,
    ))
    styles.add(ParagraphStyle(
        name='CriticalTag',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=RED_ACCENT,
    ))

    story = []
    avail_width = A4[0] - 4*cm

    def hr():
        return HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=3*mm, spaceBefore=2*mm)

    def make_table(headers, rows, col_widths=None, has_answer_col=False):
        """Build a styled table with header row and alternating colors."""
        header_cells = [Paragraph(h, styles['TableHeader']) for h in headers]
        data = [header_cells]
        for row in rows:
            cells = []
            for i, cell in enumerate(row):
                if has_answer_col and i == len(row) - 1:
                    cells.append(Paragraph(cell, styles['AnswerCell']))
                elif i == 0:
                    cells.append(Paragraph(cell, styles['TableCellBold']))
                else:
                    cells.append(Paragraph(cell, styles['TableCell']))
            data.append(cells)

        if col_widths is None:
            col_widths = [avail_width / len(headers)] * len(headers)

        t = Table(data, colWidths=col_widths, repeatRows=1)
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), ROW_ALT))
        t.setStyle(TableStyle(style_cmds))
        return t

    def question_table(questions, section_label):
        """Build a question table with # | Question | Options | Answer columns."""
        headers = ["#", "Question", "Options", "Your Answer"]
        col_w = [1.2*cm, avail_width*0.42, avail_width*0.30, avail_width*0.18]
        rows = []
        for q in questions:
            rows.append([q[0], q[1], q[2], ""])
        return make_table(headers, rows, col_widths=col_w, has_answer_col=True)

    # ===== COVER PAGE =====
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Paradise Backlink Manager", styles['DocTitle']))
    story.append(Paragraph("Stakeholder Review & Decision Document", ParagraphStyle(
        'SubTitle2', parent=styles['DocTitle'], fontSize=14, textColor=MED_GREEN
    )))
    story.append(Spacer(1, 1*cm))
    story.append(hr())

    cover_info = [
        ["Project Code:", "BT-2026-012"],
        ["Date:", "2026-02-25"],
        ["Prepared by:", "Andre (BI Engineering Lead) via Virtual ATeam"],
        ["For:", "Ian, Nabil (Stakeholders) | Marta (Head) | Dev Team"],
        ["Status:", "PENDING APPROVAL"],
    ]
    cover_data = [[Paragraph(r[0], styles['TableCellBold']), Paragraph(r[1], styles['TableCell'])] for r in cover_info]
    ct = Table(cover_data, colWidths=[4*cm, avail_width - 4*cm])
    ct.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(ct)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("<b>Repos Analyzed:</b>", styles['BodyText2']))
    story.append(Paragraph("&bull; <b>ParadiseMediaOrg/BACKLINK-MANAGER</b> &mdash; New web app (FastAPI + Next.js)", styles['BodyText2']))
    story.append(Paragraph("&bull; <b>ParadiseMediaOrg/Backlinks</b> &mdash; Existing Python automation (URL prioritization + anchor text AI)", styles['BodyText2']))

    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(
        "<i>This document contains the full overlap analysis, build status assessment, "
        "and all open questions requiring stakeholder decisions before development can proceed.</i>",
        styles['FooterNote']
    ))

    story.append(PageBreak())

    # ===== SECTION 1: EXECUTIVE SUMMARY =====
    story.append(Paragraph("1. Executive Summary", styles['SectionH1']))
    story.append(Paragraph(
        "We have <b>two separate codebases</b> that need to work together. This document maps "
        "what exists, what overlaps, what's missing, and what decisions are needed.",
        styles['BodyText2']
    ))

    summary_rows = [
        ["", "Backlinks (Existing)", "BACKLINK-MANAGER (New)"],
        ["Purpose", "Automated URL prioritization + AI anchor text", "Web UI + pipeline management + reporting"],
        ["Stack", "Python scripts, SQLite, Airtable", "FastAPI, Next.js, PostgreSQL, Cloud SQL"],
        ["Status", "Production (running every 15 min)", "27% built (foundation only, no working API)"],
        ["Team using it", "Marta's team (via Airtable)", "Nobody yet (mock data only)"],
        ["Lines of code", "~13,900 Python", "~5,870 (TypeScript + Python)"],
    ]
    st = make_table(summary_rows[0], summary_rows[1:], col_widths=[3*cm, (avail_width-3*cm)/2, (avail_width-3*cm)/2])
    story.append(st)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "<b>Key finding:</b> The existing Backlinks repo already solves several features planned as new work. "
        "These should be migrated/integrated, not rebuilt from scratch &mdash; saving ~12 dev days.",
        styles['BodyText2']
    ))

    # ===== SECTION 2: OVERLAP ANALYSIS =====
    story.append(Paragraph("2. Overlap Analysis", styles['SectionH1']))
    story.append(Paragraph("Features the Backlinks repo ALREADY handles:", styles['SectionH2']))

    overlap_rows = [
        ["URL Priority Scoring", "Full engine: FTD + rank + trend + deadline + geo", "Task 2.2: Build auto-prioritization", "100%"],
        ["Anchor Text AI", "Gemini 2.5 Pro with full ruleset + safety checks", "Task 3.1: Build anchor text AI (Claude)", "90%"],
        ["ClickUp Integration", "Full client: poll, extract, comment, dedup", "Tasks 3.3-3.4: webhook + daemon", "80%"],
        ["DataForSEO Integration", "Domain metrics, spam, backlink validation", "Task 3.9: Build DataForSEO", "100%"],
        ["BigQuery FTD Data", "Queries FTD revenue per domain", "Task 2.1: Build BigQuery integration", "100%"],
        ["GEO Detection", "Full geo mapper (US, CA, DACH, SE, NO, RO, AU)", "Task 2.4: GEO auto-detection", "100%"],
        ["Publisher Vetting", "DR + spam + traffic scoring", "Task 3.6: Publisher vetting automation", "60%"],
        ["Ahrefs Integration", "Backlink data, DR, traffic", "Task 3.8: Ahrefs API integration", "70%"],
        ["SmartMatcher", "3-layer: rule + LLM verify + LLM disambiguate", "Task 3.2: Publisher auto-matching", "40%"],
        ["Slack Notifications", "Heartbeat + completion notifications", "Task 3.5: Slack integration", "30%"],
        ["Resilience/Retry", "Circuit breaker, exponential backoff", "Implicit in all tasks", "100%"],
    ]
    ot = make_table(
        ["Feature", "Backlinks (Existing)", "BACKLINK-MANAGER (Planned)", "Overlap"],
        overlap_rows,
        col_widths=[2.8*cm, (avail_width-5.6*cm)/2, (avail_width-5.6*cm)/2, 1.5*cm]
    )
    story.append(ot)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Features ONLY in BACKLINK-MANAGER (must be built new):", styles['SectionH2']))

    new_rows = [
        ["Web UI (Pipeline View)", "35% built", "Frontend solid, needs backend API"],
        ["User Auth (IAP + RBAC)", "Middleware ready", "5 roles defined, not enforced yet"],
        ["Order Management + $700 Approval", "Not started", "Critical workflow for Marta"],
        ["Publisher Hub UI", "Empty stub", "API + UI needed"],
        ["Agency Management", "Not started", "Dropdown, formats, tracking"],
        ["Reporting Dashboard", "Empty stub", "7 reports planned"],
        ["CSV/PDF Export", "Not started", "Phase 4"],
        ["Link Health Monitoring", "Not started", "HTTP checks on live links"],
        ["Encrypted Credential Storage", "Not started", "AES-256 for marketplace logins"],
        ["Airtable \u2192 PostgreSQL Migration", "Not started", "Highest risk item"],
    ]
    nt = make_table(
        ["Feature", "Status", "Notes"],
        new_rows,
        col_widths=[4.5*cm, 2.5*cm, avail_width-7*cm]
    )
    story.append(nt)

    story.append(PageBreak())

    # ===== SECTION 3: BUILD STATUS =====
    story.append(Paragraph("3. Build Status \u2014 BACKLINK-MANAGER Repo", styles['SectionH1']))
    story.append(Paragraph(
        "Overall: <b>13 of 48 tasks complete (27%)</b>. "
        "Critical blocker: <b>zero backend API routes exist</b>. "
        "Frontend works with mock data only.",
        styles['BodyText2']
    ))

    status_rows = [
        ["\u2705 PostgreSQL schema (13 tables)", "100%", "Deployed to Cloud SQL"],
        ["\u2705 IAP auth middleware (JWT)", "100%", "Ready but not attached to routes"],
        ["\u2705 ClickUp API client", "100%", "497 lines, standalone CLI"],
        ["\u2705 DataForSEO API client", "100%", "389 lines, standalone CLI"],
        ["\u2705 ClickUp ingestion poller", "100%", "274 lines, ready for Cloud Run Job"],
        ["\u2705 Pipeline Kanban view", "100%", "Drag-drop, 8 columns (mock data)"],
        ["\u2705 Pipeline Table view", "100%", "Sort, filter, pagination (mock data)"],
        ["\u2705 Request Form + Detail panel", "100%", "Validation + slide-over tabs"],
        ["\u2705 8 API contracts (JSON Schema)", "100%", "Defined but 0 implemented"],
        ["\u26a0\ufe0f Workers service", "Stub", "Health endpoint only, no jobs"],
        ["\u26a0\ufe0f Publisher / Agency / Reports pages", "Stubs", "Empty placeholder pages"],
        ["\u274c Backend API routes", "0%", "CRITICAL \u2014 0 of ~60 routes"],
        ["\u274c ORM models", "0%", "No SQLAlchemy models defined"],
        ["\u274c Order + approval workflow", "0%", "Not started"],
        ["\u274c All Phase 2\u20135 work", "0%", "Not started"],
    ]
    bt = make_table(
        ["Component", "Status", "Notes"],
        status_rows,
        col_widths=[5.5*cm, 1.8*cm, avail_width-7.3*cm]
    )
    story.append(bt)

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Summary Scorecard:", styles['SectionH2']))

    score_rows = [
        ["Database Schema", "13 tables", "13 tables", "None", "Low"],
        ["Backend API Routes", "~60 routes", "0 routes", "CRITICAL", "High"],
        ["Frontend UI", "10 pages", "3 + 5 stubs", "Medium", "Medium"],
        ["Priority Engine", "P0\u2013P5 scoring", "Built in Backlinks repo", "Port needed", "Low"],
        ["Anchor Text AI", "Claude-based", "Built in Backlinks (Gemini)", "Port needed", "Low"],
        ["Reporting", "7 dashboards", "0 built", "CRITICAL", "High"],
        ["Order + Approval", "$700 threshold", "0 built", "HIGH", "High"],
        ["Airtable Migration", "Full export", "0 built", "HIGH", "High"],
    ]
    sct = make_table(
        ["Area", "Planned", "Built", "Gap", "Risk"],
        score_rows,
        col_widths=[3*cm, 2.5*cm, 3*cm, 2.5*cm, avail_width-11*cm]
    )
    story.append(sct)

    story.append(PageBreak())

    # ===== SECTION 4: INTEGRATION RECOMMENDATION =====
    story.append(Paragraph("4. Recommendation \u2014 Integration Strategy", styles['SectionH1']))
    story.append(Paragraph(
        "Instead of rebuilding what Backlinks already does, port existing Python modules into BACKLINK-MANAGER:",
        styles['BodyText2']
    ))

    port_rows = [
        ["url_prioritization.py", "Backlinks repo", "Task 2.2 (3 days saved)", "1 day (swap Airtable \u2192 DB)"],
        ["anchor_automation.py", "Backlinks repo", "Task 3.1 (4 days saved)", "2 days (Gemini \u2192 Claude)"],
        ["src/matching/*", "Backlinks repo", "Task 3.2 (3 days saved)", "1 day (already modular)"],
        ["clickup_cache.py", "Backlinks repo", "Part of Tasks 3.3-3.4", "0.5 days"],
        ["resilience.py", "Backlinks repo", "Implicit", "0.5 days"],
        ["geo_mapper.py", "Backlinks repo", "Task 2.4 (1 day saved)", "0 days (drop-in)"],
    ]
    pt = make_table(
        ["Module", "Source", "Saves", "Effort to Port"],
        port_rows,
        col_widths=[3.5*cm, 2.5*cm, (avail_width-6*cm)/2, (avail_width-6*cm)/2]
    )
    story.append(pt)

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>Total time saved: ~12 days</b> by porting instead of rebuilding.", styles['BodyText2']))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Focus new development on:", styles['SectionH2']))
    story.append(Paragraph("1. <b>Backend API routes</b> (the critical 0% gap)", styles['BodyText2']))
    story.append(Paragraph("2. <b>Order management + approval workflow</b> (new business logic)", styles['BodyText2']))
    story.append(Paragraph("3. <b>Reporting dashboard</b> (no equivalent in Backlinks)", styles['BodyText2']))
    story.append(Paragraph("4. <b>Encrypted credential vault</b> (new requirement)", styles['BodyText2']))
    story.append(Paragraph("5. <b>Airtable \u2192 PostgreSQL migration</b> (one-time, highest risk)", styles['BodyText2']))

    story.append(PageBreak())

    # ===== SECTION 5: ALL QUESTIONS =====
    story.append(Paragraph("5. Open Questions \u2014 Requiring Your Answers", styles['SectionH1']))
    story.append(Paragraph(
        "Below are all open questions from the dev team. Your answers will unblock development. "
        "Please fill in the <b>\"Your Answer\"</b> column and return this document.",
        styles['BodyText2']
    ))

    # ---- Section A: Need Before Kickoff ----
    story.append(hr())
    story.append(Paragraph("\U0001f6a8  SECTION A: NEED BEFORE KICKOFF", styles['SectionH2']))
    story.append(Paragraph("<i>Answer these first \u2014 they block development.</i>", styles['FooterNote']))

    story.append(Paragraph("A1. UI Decisions", styles['SectionH3']))
    story.append(question_table([
        ("A1.1", "Default pipeline view?", "Kanban / Table / Both with toggle (which default?)"),
        ("A1.2", "Table density?", "Comfortable (modern SaaS) / Dense (spreadsheet-like)"),
        ("A1.3", "Can status be changed inline in the table?", "Inline (click cell \u2192 dropdown) / Detail panel only"),
        ("A1.4", "Any company brand guidelines to follow?", "Yes (share them) / No, use defaults"),
        ("A1.5", "Custom domain confirmed?", "Yes (e.g. backlinks.paradisemedia.com) / Not yet"),
    ], "A1"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("A2. Workflow Decisions", styles['SectionH3']))
    story.append(question_table([
        ("A2.1", "$700 approval threshold?", "Fixed / Configurable by Admin in settings"),
        ("A2.2", "Can a request skip statuses? (e.g. 'new' \u2192 'order placed')", "Yes / No, must follow sequence"),
        ("A2.3", "Can a request go backwards? (e.g. 'order placed' \u2192 'anchor selected')", "Yes / No"),
        ("A2.4", "Cancelled requests?", "Hidden / Visible but greyed out / Separate archive"),
        ("A2.5", "Expected monthly volume?", "~500 / ~1,000 / Other: ___"),
    ], "A2"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("A3. Roles & Access", styles['SectionH3']))
    story.append(question_table([
        ("A3.1", "Can PMs see only their own requests, or full pipeline?", "Own only / Full pipeline"),
        ("A3.2", "Can Builders see unassigned requests and self-assign?", "Yes / No"),
        ("A3.3", "Can Viewers see spend/pricing data in reports?", "Yes / No"),
        ("A3.4", "Can Marta reassign requests between builders?", "Yes / No"),
        ("A3.5", "Can Marta set max capacity per builder? (e.g. max 20 active)", "Yes / No"),
        ("A3.6", "Does Marta need a dedicated Approval Queue page?", "Yes / No / Just filter existing tables"),
    ], "A3"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("A4. Permissions (Y/N each)", styles['SectionH3']))
    story.append(question_table([
        ("A4.1", "Only Admin + Head can approve orders >$700?", "Y / N"),
        ("A4.2", "Only Admin + Head can approve/blacklist publishers?", "Y / N"),
        ("A4.3", "Only Admin + Head can add agencies?", "Y / N"),
        ("A4.4", "Only Admin can add marketplace credentials?", "Y / N"),
        ("A4.5", "Only Admin can create users and change roles?", "Y / N"),
    ], "A4"))

    story.append(PageBreak())

    # ---- Section B: Data Engineering ----
    story.append(Paragraph("\U0001f527  SECTION B: DATA ENGINEERING", styles['SectionH2']))
    story.append(question_table([
        ("B1", "Link health monitoring \u2014 Do links have an assigned LIVE duration? Or just check if still online?", "Duration / Just online check"),
        ("B2", "What is 'pipeline health'? Task progress tracking? Stale orders?", "Free text"),
        ("B3", "Bulk CSV import of what?", "Publishers / Requests / Both"),
        ("B4", "What is the 'Marketplace'? (context: encrypted credential storage for marketplace logins)", "Free text"),
    ], "B"))
    story.append(Spacer(1, 4*mm))

    # ---- Section C: Backend Workflows ----
    story.append(Paragraph("\u2699\ufe0f  SECTION C: BACKEND WORKFLOW QUESTIONS", styles['SectionH2']))

    story.append(Paragraph("Workflow 1 \u2014 PM Submits Request", styles['SectionH3']))
    story.append(question_table([
        ("C1.1", "What are 'Tier' and 'Page Status'? Are these ClickUp fields?", "Free text"),
        ("C1.2", "Should duplicate check be blocking (prevent creation) or just a warning?", "Block / Warning only"),
        ("C1.3", "GEO auto-detected \u2014 from ClickUp Target GEO field?", "Yes / No / Other source"),
        ("C1.4", "If article is already in production, doesn't it already have a Publisher planned?", "Yes / No"),
    ], "C1"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Workflow 2 \u2014 ClickUp Automated Requests", styles['SectionH3']))
    story.append(question_table([
        ("C2.1", "Which ClickUp list for backlink requests? (Dev team needs access)", "List ID needed"),
        ("C2.2", "'Pull live URL data from BigQuery' \u2014 this is ClickUp data, right?", "Yes / No"),
        ("C2.3", "How are SERP competitors determined?", "Free text"),
        ("C2.4", "What is a 'backlink gap'? Fewer backlinks (count)? Fewer DoFollow?", "Free text"),
        ("C2.5", "Link count calculation: fixed formula or predictive model?", "Fixed / Predictive"),
        ("C2.6", "Should we ignore ClickUp tasks with missing data? (No Target_GEO, Keyword, LIVE_URL)", "Yes / No"),
    ], "C2"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Workflow 3 \u2014 Agency Order Flow", styles['SectionH3']))
    story.append(question_table([
        ("C3.1", "Need the Agency list \u2014 is it in ClickUp?", "Yes / No / Where?"),
        ("C3.2", "'Agency-specific format' for orders \u2014 how do we get these?", "Free text"),
        ("C3.3", "'DR matches quoted?' \u2014 where is the quote for matching?", "Free text"),
    ], "C3"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Workflow 4 \u2014 Publisher Vetting", styles['SectionH3']))
    story.append(question_table([
        ("C4.1", "Vetting score format?", "0\u2013100 / Yes\u2013No / Other"),
        ("C4.2", "What are the 'issues' in publisher performance tracking?", "Free text"),
    ], "C4"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Workflow 5 \u2014 Reporting", styles['SectionH3']))
    story.append(question_table([
        ("C5.1", "Budget utilization \u2014 how do we know the spend target/budget?", "Free text"),
    ], "C5"))

    story.append(PageBreak())

    # ---- Section D: Need Before Phase 2 ----
    story.append(Paragraph("\U0001f552  SECTION D: NEED BEFORE PHASE 2", styles['SectionH2']))
    story.append(Paragraph("<i>Can wait a few weeks, but needed before reporting &amp; notifications.</i>", styles['FooterNote']))

    story.append(Paragraph("D1. Reports", styles['SectionH3']))
    story.append(question_table([
        ("D1.1", "Can Builders see other builders' performance stats?", "Yes / No"),
        ("D1.2", "Can Builders see aggregate spend dashboards?", "Yes / No"),
        ("D1.3", "Can PMs see how much is spent on their domains' backlinks?", "Yes / No"),
        ("D1.4", "Should Viewers see team performance + agency pricing?", "Full / High-level only"),
        ("D1.5", "How define which domains 'belong to' a PM?", "A) Any they submitted for / B) Pre-assigned by Admin"),
        ("D1.6", "Can we launch with 3 reports and add the rest after?", "Yes (Overview, Domain, Spend) / Must have all 7"),
    ], "D1"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("D2. Notifications & Slack", styles['SectionH3']))
    story.append(question_table([
        ("D2.1", "Weekly Slack report format?", "Shared (#backlinks) / Personalized DMs / Both"),
        ("D2.2", "Should the weekly Slack message link to the full report in the app?", "Yes / No"),
        ("D2.3", "Should PMs get a separate weekly summary for their domains?", "Yes / No"),
        ("D2.4", "Can users choose which domains they get notified about?", "Yes / No / Not needed"),
        ("D2.5", "In-app notifications needed for v1?", "In-app / Slack only / Both"),
    ], "D2"))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("D3. Marta's Approvals", styles['SectionH3']))
    story.append(question_table([
        ("D3.1", "How should Marta be notified of pending approvals?", "Slack DM / In-app badge / Both"),
        ("D3.2", "Can Marta approve/reject directly from Slack?", "Yes / No, must use app"),
        ("D3.3", "Auto-reminder if Marta doesn't respond after 24hrs?", "Yes / No"),
        ("D3.4", "Same approval flow for publisher vetting reviews?", "Yes / No"),
    ], "D3"))

    story.append(Spacer(1, 5*mm))
    story.append(hr())

    # ---- Project Questions ----
    story.append(Paragraph("\u2753  PROJECT-LEVEL QUESTIONS", styles['SectionH2']))
    story.append(question_table([
        ("P1", "Who are the 3 developers (names)?", "Names needed"),
        ("P2", "What is the project kickoff date?", "Date needed"),
        ("P3", "Should the publisher vetting dashboard on Render be decommissioned?", "Yes / No"),
        ("P4", "Are there agency spreadsheet formats we need to support for export?", "Yes (share) / No"),
        ("P5", "Weekly report: Slack only or also email?", "Slack only / Email too / Both"),
    ], "P"))

    story.append(Spacer(1, 1*cm))
    story.append(hr())

    # ===== SECTION 6: NEXT STEPS =====
    story.append(Paragraph("6. Next Steps", styles['SectionH1']))
    story.append(Paragraph("1. <b>Stakeholders</b> \u2014 Answer Section A questions (blocks kickoff)", styles['BodyText2']))
    story.append(Paragraph("2. <b>Marta</b> \u2014 Answer Section D questions (blocks Phase 2)", styles['BodyText2']))
    story.append(Paragraph("3. <b>Dev Team</b> \u2014 Answer Sections B + C (blocks implementation details)", styles['BodyText2']))
    story.append(Paragraph("4. <b>Andre</b> \u2014 Assign developer names, confirm kickoff date", styles['BodyText2']))
    story.append(Paragraph("5. <b>Architecture Decision</b> \u2014 Confirm integration strategy (port Backlinks \u2192 BACKLINK-MANAGER)", styles['BodyText2']))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "<i>Generated 2026-02-25 by Virtual ATeam (B-BOB + W-WOL) | "
        "Repos: BACKLINK-MANAGER (60 commits, 13 PRs) + Backlinks (20 modules, 13,900 LOC)</i>",
        styles['FooterNote']
    ))

    # Build PDF
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")
    print(f"Size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
