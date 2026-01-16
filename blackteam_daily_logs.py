#!/usr/bin/env python3
"""
BlackTeam Daily Log Generator
Generates team-wide and individual daily activity logs with ClickUp integration.

Usage:
    python3 blackteam_daily_logs.py           # Generate all logs (team + individual)
    python3 blackteam_daily_logs.py team      # Generate team log only
    python3 blackteam_daily_logs.py member    # Generate individual logs only
"""

import os
import sys
import json
import re
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CLICKUP_API_KEY = os.environ.get('CLICKUP_API_KEY')
CLICKUP_BASE_URL = "https://api.clickup.com/api/v2"
BLACKTEAM_DIR = Path("/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam")
LOGS_DIR = BLACKTEAM_DIR / "logs"
PROJECT_REGISTRY_PATH = BLACKTEAM_DIR / "PROJECT_REGISTRY.json"

# Team member configuration with aliases
TEAM_MEMBERS = {
    "director": {
        "id": "DIR",
        "name": "The Director",
        "role": "Director of AI, Data & BI",
        "track": "Leadership",
        "aliases": ["Director", "The Director", "DIR"]
    },
    "dataforge": {
        "id": "DF",
        "name": "DataForge",
        "role": "Senior Data Engineer",
        "track": "Data",
        "aliases": ["DataForge", "DF", "Data Engineer"]
    },
    "codeguard": {
        "id": "CG",
        "name": "CodeGuard",
        "role": "Senior Code Reviewer",
        "track": "Data",
        "aliases": ["CodeGuard", "CG", "Code Reviewer"]
    },
    "elias_thorne": {
        "id": "ET",
        "name": "Elias Thorne",
        "role": "ML Engineer / Chief Data Scientist",
        "track": "Analytics",
        "aliases": ["Elias Thorne", "ET", "Elias", "ML Engineer"]
    },
    "dataviz": {
        "id": "BID",
        "name": "DataViz",
        "role": "Senior BI Developer",
        "track": "Analytics",
        "aliases": ["DataViz", "BID", "BI Developer"]
    },
    "insight": {
        "id": "DA",
        "name": "Insight",
        "role": "Senior Data Analyst",
        "track": "Analytics",
        "aliases": ["Insight", "DA", "Data Analyst"]
    },
    "seo_commander": {
        "id": "SEO",
        "name": "SEO Commander",
        "role": "Head of SEO",
        "track": "Content",
        "aliases": ["SEO Commander", "SEO", "Head of SEO"]
    },
    "head_of_content": {
        "id": "HOC",
        "name": "Head of Content",
        "role": "Content Strategy",
        "track": "Content",
        "aliases": ["Head of Content", "HOC", "Content Lead"]
    },
    "affiliate_manager": {
        "id": "AM",
        "name": "Affiliate Manager",
        "role": "Partnership Management",
        "track": "Content",
        "aliases": ["Affiliate Manager", "AM"]
    },
    "post_production": {
        "id": "PPM",
        "name": "Post Production Manager",
        "role": "Production Operations",
        "track": "Content",
        "aliases": ["Post Production Manager", "PPM", "Post Production"]
    }
}


def load_project_registry():
    """Load the project registry JSON."""
    try:
        with open(PROJECT_REGISTRY_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading project registry: {e}")
        return {"projects": []}


def get_clickup_headers():
    """Get headers for ClickUp API requests."""
    return {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }


def fetch_task_comments(task_id):
    """Fetch comments for a ClickUp task."""
    try:
        url = f"{CLICKUP_BASE_URL}/task/{task_id}/comment"
        response = requests.get(url, headers=get_clickup_headers())
        if response.status_code == 200:
            return response.json().get('comments', [])
    except Exception as e:
        print(f"  Error fetching comments for {task_id}: {e}")
    return []


def fetch_task_details(task_id):
    """Fetch task details from ClickUp."""
    try:
        url = f"{CLICKUP_BASE_URL}/task/{task_id}"
        response = requests.get(url, headers=get_clickup_headers())
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"  Error fetching task {task_id}: {e}")
    return None


def get_today_date_range():
    """Get Unix timestamps for today's date range."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    return int(today.timestamp() * 1000), int(tomorrow.timestamp() * 1000)


def identify_author(author_text):
    """Identify which team member authored something based on text."""
    if not author_text:
        return None
    author_lower = author_text.lower()
    for key, member in TEAM_MEMBERS.items():
        for alias in member['aliases']:
            if alias.lower() in author_lower:
                return key
    return None


def fetch_all_project_activity():
    """Fetch activity from all projects in the registry."""
    registry = load_project_registry()
    all_activity = []
    today_start, today_end = get_today_date_range()
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"\nFetching ClickUp activity for {today_str}...")

    for project in registry.get('projects', []):
        project_id = project.get('internal_id', 'Unknown')
        project_name = project.get('name', 'Unknown')
        clickup_info = project.get('clickup', {})
        main_task_id = clickup_info.get('main_task_id')

        if not main_task_id:
            continue

        print(f"\n  Project: {project_name} ({project_id})")
        print(f"  Main Task: {main_task_id}")

        # Fetch main task details
        task_details = fetch_task_details(main_task_id)
        if task_details:
            project_activity = {
                'project_id': project_id,
                'project_name': project_name,
                'main_task_id': main_task_id,
                'main_task_url': clickup_info.get('main_task_url', ''),
                'status': task_details.get('status', {}).get('status', 'unknown'),
                'comments': [],
                'sub_tasks': []
            }

            # Fetch comments on main task
            comments = fetch_task_comments(main_task_id)
            for comment in comments:
                comment_date = int(comment.get('date', 0))
                if today_start <= comment_date <= today_end:
                    project_activity['comments'].append({
                        'text': comment.get('comment_text', '')[:200],
                        'user': comment.get('user', {}).get('username', 'Unknown'),
                        'date': datetime.fromtimestamp(comment_date/1000).strftime('%H:%M'),
                        'task_id': main_task_id
                    })

            # Fetch sub-task activity
            for sub_task in clickup_info.get('sub_tasks', []):
                sub_task_id = sub_task.get('id')
                if sub_task_id:
                    sub_comments = fetch_task_comments(sub_task_id)
                    for comment in sub_comments:
                        comment_date = int(comment.get('date', 0))
                        if today_start <= comment_date <= today_end:
                            project_activity['comments'].append({
                                'text': comment.get('comment_text', '')[:200],
                                'user': comment.get('user', {}).get('username', 'Unknown'),
                                'date': datetime.fromtimestamp(comment_date/1000).strftime('%H:%M'),
                                'task_id': sub_task_id,
                                'sub_task_name': sub_task.get('name', '')
                            })

            print(f"  Found {len(project_activity['comments'])} comments today")
            all_activity.append(project_activity)

    return all_activity


def generate_team_daily_log(activity_data):
    """Generate the team-wide daily log."""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    formatted_date = today.strftime("%B %d, %Y")

    registry = load_project_registry()

    # Count total activity
    total_comments = sum(len(p['comments']) for p in activity_data)

    # Track member contributions
    member_contributions = {key: [] for key in TEAM_MEMBERS.keys()}

    md_content = f"""# BlackTeam Daily Log - {formatted_date}

**Generated:** {today.strftime("%Y-%m-%d %H:%M:%S")}
**Managed By:** The Director
**Report Type:** Team Activity Summary

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Active Projects | {len([p for p in registry.get('projects', []) if p.get('status') in ['active', 'in_progress']])} |
| ClickUp Updates Today | {total_comments} |
| Team Members Active | TBD |

---

## Project Activity

"""

    for project in activity_data:
        md_content += f"""### {project['project_name']}
**Project ID:** {project['project_id']}
**ClickUp Task:** [{project['main_task_id']}]({project['main_task_url']})
**Status:** {project['status'].title()}

"""
        if project['comments']:
            md_content += "| Time | Update | Author | Task |\n"
            md_content += "|------|--------|--------|------|\n"
            for comment in sorted(project['comments'], key=lambda x: x['date'], reverse=True):
                task_ref = comment.get('sub_task_name', comment['task_id'])
                # Truncate and escape pipe characters
                text = comment['text'].replace('|', '/').replace('\n', ' ')[:80]
                md_content += f"| {comment['date']} | {text}... | {comment['user']} | {task_ref} |\n"

                # Track member contributions
                author = identify_author(comment['user'])
                if author:
                    member_contributions[author].append({
                        'project': project['project_name'],
                        'action': text[:50],
                        'time': comment['date']
                    })
        else:
            md_content += "*No activity recorded today*\n"

        md_content += "\n---\n\n"

    # Add Team Performance section
    md_content += """## Team Performance by Member

| Member | Role | Contributions Today |
|--------|------|---------------------|
"""

    for key, member in TEAM_MEMBERS.items():
        contrib_count = len(member_contributions.get(key, []))
        contrib_text = f"{contrib_count} updates" if contrib_count > 0 else "No activity"
        md_content += f"| {member['name']} | {member['role']} | {contrib_text} |\n"

    # Add Project Registry Reference
    md_content += """
---

## Project Registry Reference

| Project ID | Project Name | ClickUp Task | Status |
|------------|--------------|--------------|--------|
"""

    for project in registry.get('projects', []):
        clickup = project.get('clickup', {})
        md_content += f"| {project['internal_id']} | {project['name']} | {clickup.get('main_task_id', 'N/A')} | {project['status']} |\n"

    md_content += f"""
---

## ClickUp Task Reference

| Task ID | Task Name | Project |
|---------|-----------|---------|
"""

    for project in registry.get('projects', []):
        clickup = project.get('clickup', {})
        if clickup.get('main_task_id'):
            md_content += f"| {clickup['main_task_id']} | Main Task | {project['internal_id']} |\n"
        for sub in clickup.get('sub_tasks', []):
            md_content += f"| {sub['id']} | {sub['name']} | {project['internal_id']} |\n"

    md_content += f"""
---

*Generated by BlackTeam Daily Log System*
*— The Director, BlackTeam*
"""

    return md_content, date_str, member_contributions


def generate_individual_log(member_key, member_info, contributions, activity_data):
    """Generate an individual team member's daily log."""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    formatted_date = today.strftime("%B %d, %Y")

    md_content = f"""# {member_info['name']} - Daily Activity Log

**Date:** {formatted_date}
**Role:** {member_info['role']}
**Track:** {member_info['track']}
**Member ID:** {member_info['id']}

---

## Today's Contributions

"""

    if contributions:
        md_content += "| Time | Project | Activity |\n"
        md_content += "|------|---------|----------|\n"
        for contrib in sorted(contributions, key=lambda x: x['time'], reverse=True):
            md_content += f"| {contrib['time']} | {contrib['project']} | {contrib['action']}... |\n"
        md_content += f"\n**Total Contributions:** {len(contributions)}\n"
    else:
        md_content += "*No recorded activity for today*\n"

    md_content += """
---

## Projects Assigned

"""

    registry = load_project_registry()
    assigned_projects = []
    for project in registry.get('projects', []):
        specialists = project.get('specialists_assigned', [])
        for alias in member_info['aliases']:
            if alias in specialists:
                assigned_projects.append(project)
                break

    if assigned_projects:
        md_content += "| Project ID | Project Name | Status | ClickUp Task |\n"
        md_content += "|------------|--------------|--------|---------------|\n"
        for project in assigned_projects:
            clickup = project.get('clickup', {})
            md_content += f"| {project['internal_id']} | {project['name']} | {project['status']} | {clickup.get('main_task_id', 'N/A')} |\n"
    else:
        md_content += "*No projects currently assigned*\n"

    md_content += f"""
---

*Individual log for {member_info['name']}*
*Generated: {today.strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return md_content, date_str


class DailyLogPDF:
    """PDF generator for BlackTeam Daily Logs - matches PostHog report style."""

    def __init__(self):
        try:
            from fpdf import FPDF
            self.FPDF = FPDF
            self.available = True
        except ImportError:
            self.available = False

    def create_pdf(self):
        """Create a new PDF instance with proper styling."""
        if not self.available:
            return None

        pdf = self.FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        return pdf

    def add_header(self, pdf):
        """Add page header."""
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, 'BlackTeam Daily Activity Log', align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def add_footer(self, pdf):
        """Footer is handled per-page in fpdf."""
        pass

    def chapter_title(self, pdf, title):
        """Add chapter title with colored background."""
        if pdf.get_y() + 50 > 270:
            pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_fill_color(41, 128, 185)  # Blue
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)

    def section_title(self, pdf, title):
        """Add section title with colored text."""
        if pdf.get_y() + 40 > 270:
            pdf.add_page()
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    def body_text(self, pdf, text):
        """Add body text."""
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, text)
        pdf.ln(2)

    def add_info_line(self, pdf, label, value):
        """Add a label: value line."""
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(50, 6, f"{label}:", align='L')
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 6, str(value), new_x="LMARGIN", new_y="NEXT")

    def add_table(self, pdf, headers, data, col_widths=None):
        """Add a table with proper styling (Director Rule 2: no split tables)."""
        if not data or not headers:
            return

        num_cols = len(headers)
        if col_widths is None:
            col_widths = [190 // num_cols] * num_cols

        # DIRECTOR RULE 2: Check if table fits on current page
        num_rows = min(len(data), 20)
        table_height = 7 + (num_rows * 6) + 10
        if pdf.get_y() + table_height > 270:
            pdf.add_page()

        # Header row
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_fill_color(52, 73, 94)  # Dark blue
        pdf.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 7, str(header)[:25], border=1, fill=True, align='C')
        pdf.ln()

        # Data rows
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(0, 0, 0)
        fill = False
        for row in data[:20]:
            if fill:
                pdf.set_fill_color(236, 240, 241)  # Light gray
            else:
                pdf.set_fill_color(255, 255, 255)  # White
            for i, cell in enumerate(row):
                cell_text = str(cell)[:35] if cell else '-'
                pdf.cell(col_widths[i], 6, cell_text, border=1, fill=True, align='L')
            pdf.ln()
            fill = not fill
        pdf.ln(3)


def generate_team_pdf(activity_data, member_contributions, output_path):
    """Generate team daily log PDF with PostHog-style formatting."""
    generator = DailyLogPDF()
    if not generator.available:
        print("  Warning: fpdf2 not installed, skipping PDF generation")
        return False

    try:
        pdf = generator.create_pdf()
        pdf.add_page()

        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")

        registry = load_project_registry()
        total_comments = sum(len(p['comments']) for p in activity_data)
        active_members = sum(1 for k, v in member_contributions.items() if v)

        # Title
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 15, 'BlackTeam Daily Log', align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, formatted_date, align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, 'Managed by The Director', align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        # Executive Summary
        generator.chapter_title(pdf, 'Executive Summary')
        generator.add_table(pdf,
            ['Metric', 'Value'],
            [
                ['Active Projects', str(len([p for p in registry.get('projects', []) if p.get('status') in ['active', 'in_progress']]))],
                ['ClickUp Updates Today', str(total_comments)],
                ['Team Members Active', str(active_members)]
            ],
            [95, 95]
        )

        # Project Activity
        generator.chapter_title(pdf, 'Project Activity')
        for project in activity_data:
            generator.section_title(pdf, project['project_name'])
            generator.add_info_line(pdf, 'Project ID', project['project_id'])
            generator.add_info_line(pdf, 'ClickUp Task', project['main_task_id'])
            generator.add_info_line(pdf, 'Status', project['status'].title())
            pdf.ln(2)

            if project['comments']:
                generator.add_table(pdf,
                    ['Time', 'Update', 'Author'],
                    [[c['date'], c['text'][:40] + '...' if len(c['text']) > 40 else c['text'], c['user']] for c in project['comments']],
                    [25, 120, 45]
                )
            else:
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(128, 128, 128)
                pdf.cell(0, 6, 'No activity recorded today', new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

        # Team Performance
        generator.chapter_title(pdf, 'Team Performance by Member')
        team_data = []
        for key, member in TEAM_MEMBERS.items():
            contrib_count = len(member_contributions.get(key, []))
            contrib_text = f"{contrib_count} updates" if contrib_count > 0 else "No activity"
            team_data.append([member['name'], member['role'][:25], contrib_text])
        generator.add_table(pdf, ['Member', 'Role', 'Contributions'], team_data, [55, 85, 50])

        # Project Registry
        generator.chapter_title(pdf, 'Project Registry Reference')
        registry_data = []
        for project in registry.get('projects', []):
            clickup = project.get('clickup', {})
            registry_data.append([
                project['internal_id'],
                project['name'][:30],
                clickup.get('main_task_id', 'N/A'),
                project['status']
            ])
        generator.add_table(pdf, ['Project ID', 'Name', 'ClickUp Task', 'Status'], registry_data, [35, 75, 40, 40])

        # ClickUp Task Reference
        generator.chapter_title(pdf, 'ClickUp Task Reference')
        task_data = []
        for project in registry.get('projects', []):
            clickup = project.get('clickup', {})
            if clickup.get('main_task_id'):
                task_data.append([clickup['main_task_id'], 'Main Task', project['internal_id']])
            for sub in clickup.get('sub_tasks', [])[:5]:  # Limit subtasks
                task_data.append([sub['id'], sub['name'][:35], project['internal_id']])
        generator.add_table(pdf, ['Task ID', 'Task Name', 'Project'], task_data, [45, 100, 45])

        # Footer note
        pdf.ln(10)
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, f'Generated by BlackTeam Daily Log System | {today.strftime("%Y-%m-%d %H:%M")}', align='C')

        pdf.output(str(output_path))
        return True
    except Exception as e:
        print(f"  Error generating team PDF: {e}")
        return False


def generate_individual_pdf(member_key, member_info, contributions, output_path):
    """Generate individual member daily log PDF with PostHog-style formatting."""
    generator = DailyLogPDF()
    if not generator.available:
        return False

    try:
        pdf = generator.create_pdf()
        pdf.add_page()

        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")

        registry = load_project_registry()

        # Title
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 15, member_info['name'], align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, 'Daily Activity Log', align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, formatted_date, align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        # Member Info
        generator.chapter_title(pdf, 'Member Information')
        generator.add_info_line(pdf, 'Role', member_info['role'])
        generator.add_info_line(pdf, 'Track', member_info['track'])
        generator.add_info_line(pdf, 'Member ID', member_info['id'])
        pdf.ln(5)

        # Today's Contributions
        generator.chapter_title(pdf, "Today's Contributions")
        if contributions:
            contrib_data = [[c['time'], c['project'][:30], c['action'][:40]] for c in contributions]
            generator.add_table(pdf, ['Time', 'Project', 'Activity'], contrib_data, [25, 65, 100])
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 8, f'Total Contributions: {len(contributions)}', new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 6, 'No recorded activity for today', new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Projects Assigned
        generator.chapter_title(pdf, 'Projects Assigned')
        assigned_projects = []
        for project in registry.get('projects', []):
            specialists = project.get('specialists_assigned', [])
            for alias in member_info['aliases']:
                if alias in specialists:
                    clickup = project.get('clickup', {})
                    assigned_projects.append([
                        project['internal_id'],
                        project['name'][:30],
                        project['status'],
                        clickup.get('main_task_id', 'N/A')
                    ])
                    break

        if assigned_projects:
            generator.add_table(pdf, ['Project ID', 'Name', 'Status', 'ClickUp'], assigned_projects, [35, 75, 40, 40])
        else:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 6, 'No projects currently assigned', new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)

        # Footer
        pdf.ln(10)
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, f'Individual log for {member_info["name"]} | Generated: {today.strftime("%Y-%m-%d %H:%M")}', align='C')

        pdf.output(str(output_path))
        return True
    except Exception as e:
        print(f"  Error generating individual PDF: {e}")
        return False


def main():
    """Main entry point."""
    if not CLICKUP_API_KEY:
        print("ERROR: CLICKUP_API_KEY not set")
        print("Run: export CLICKUP_API_KEY=$(cat /home/andre/.claude/clickup_config.json | python3 -c \"import json,sys; print(json.load(sys.stdin)['CLICKUP_API_KEY'])\")")
        sys.exit(1)

    # Determine mode
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    print("=" * 60)
    print("BlackTeam Daily Log Generator")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {mode}")

    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (LOGS_DIR / "team").mkdir(exist_ok=True)
    (LOGS_DIR / "individual").mkdir(exist_ok=True)

    # Fetch all activity
    activity_data = fetch_all_project_activity()

    if mode in ['all', 'team']:
        print("\n" + "=" * 40)
        print("Generating Team Daily Log")
        print("=" * 40)

        team_md, date_str, member_contributions = generate_team_daily_log(activity_data)

        # Save markdown
        team_md_path = LOGS_DIR / "team" / f"TEAM_DAILY_LOG_{date_str}.md"
        with open(team_md_path, 'w') as f:
            f.write(team_md)
        print(f"Markdown saved: {team_md_path}")

        # Save PDF (Director Rule 1) - Using new PostHog-style generator
        team_pdf_path = LOGS_DIR / "team" / f"TEAM_DAILY_LOG_{date_str}.pdf"
        if generate_team_pdf(activity_data, member_contributions, team_pdf_path):
            print(f"PDF saved: {team_pdf_path}")
    else:
        # Need to generate team log anyway to get member contributions
        _, _, member_contributions = generate_team_daily_log(activity_data)

    if mode in ['all', 'member']:
        print("\n" + "=" * 40)
        print("Generating Individual Logs")
        print("=" * 40)

        for key, member in TEAM_MEMBERS.items():
            contributions = member_contributions.get(key, [])
            ind_md, date_str = generate_individual_log(key, member, contributions, activity_data)

            # Create member directory
            member_dir = LOGS_DIR / "individual" / key
            member_dir.mkdir(exist_ok=True)

            # Save markdown
            ind_md_path = member_dir / f"{key.upper()}_LOG_{date_str}.md"
            with open(ind_md_path, 'w') as f:
                f.write(ind_md)
            print(f"  {member['name']}: {ind_md_path}")

            # Save PDF (Director Rule 1) - Using new PostHog-style generator
            ind_pdf_path = member_dir / f"{key.upper()}_LOG_{date_str}.pdf"
            if generate_individual_pdf(key, member, contributions, ind_pdf_path):
                print(f"    PDF: {ind_pdf_path}")

    print("\n" + "=" * 60)
    print("Daily Log Generation Complete!")
    print("=" * 60)
    print(f"\nLogs saved to: {LOGS_DIR}")


if __name__ == "__main__":
    main()
