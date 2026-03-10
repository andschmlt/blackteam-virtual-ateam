#!/usr/bin/env python3
"""
HudsonReporter.com PostHog Analytics Report Generator
Runs every 30 minutes and sends email report

Version: 2.0.0
Updated: 2026-01-22
Changes: Added conversions, NavBoost calculated metrics, daily trends, browser/OS breakdown
"""

import os
import sys
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration
PROJECT_ID = 295222
PROJECT_NAME = "hudsonreporter.com"
BASE_URL = "https://us.i.posthog.com"

# Load environment variables from .keys/.env
def load_env():
    env_file = "/home/andre/.keys/.env"
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

ENV = load_env()
API_KEY = ENV.get('POSTHOG_PERSONAL_API_KEY', '')
SMTP_HOST = ENV.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(ENV.get('SMTP_PORT', '587'))
SMTP_USER = ENV.get('SMTP_USER', '')
SMTP_PASSWORD = ENV.get('SMTP_PASSWORD', '')
FROM_EMAIL = ENV.get('BI_UPDATE_FROM_EMAIL', SMTP_USER)
TO_EMAILS = ['andre@paradisemedia.com']  # Hardcoded recipient

def run_query(query):
    """Execute HogQL query against PostHog API"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/api/projects/{PROJECT_ID}/query/"
    payload = {"query": {"kind": "HogQLQuery", "query": query}}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.text, "results": []}
    except Exception as e:
        return {"error": str(e), "results": []}

def get_lcp_rating(lcp):
    if lcp is None: return "N/A", "⚪"
    if lcp <= 1200: return "Good", "🟢"
    if lcp <= 2500: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_cls_rating(cls):
    if cls is None: return "N/A", "⚪"
    if cls <= 0.1: return "Good", "🟢"
    if cls <= 0.25: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_inp_rating(inp):
    if inp is None: return "N/A", "⚪"
    if inp <= 200: return "Good", "🟢"
    if inp <= 500: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_pogo_rating(pogo):
    if pogo is None: return "N/A", "⚪"
    if pogo < 10: return "Excellent", "🟢"
    if pogo < 18: return "Good", "🟢"
    if pogo < 25: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_dwell_rating(dwell):
    if dwell is None: return "N/A", "⚪"
    if dwell >= 180: return "Excellent", "🟢"
    if dwell >= 90: return "Good", "🟢"
    if dwell >= 30: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_cta_ctr_rating(ctr):
    if ctr is None: return "N/A", "⚪"
    if ctr >= 10: return "Excellent", "🟢"
    if ctr >= 5: return "Good", "🟢"
    if ctr >= 2: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def get_engagement_rating(score):
    if score is None: return "N/A", "⚪"
    if score >= 80: return "Excellent", "🟢"
    if score >= 70: return "Good", "🟢"
    if score >= 50: return "Needs Improvement", "🟡"
    return "Poor", "🔴"

def generate_report():
    """Generate the full analytics report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Overall Stats
    stats = run_query("""
    SELECT
        count() as total_events,
        uniqExact(distinct_id) as unique_users,
        uniqExact(properties.$session_id) as sessions
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    """)

    # 2. Event Breakdown
    events = run_query("""
    SELECT event, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY event ORDER BY count DESC LIMIT 10
    """)

    # 3. Web Vitals
    vitals = run_query("""
    SELECT
        avg(properties.$web_vitals_LCP_value) as avg_LCP,
        avg(properties.$web_vitals_CLS_value) as avg_CLS,
        avg(properties.$web_vitals_INP_value) as avg_INP
    FROM events
    WHERE event = '$web_vitals' AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # 4. Top Pages
    pages = run_query("""
    SELECT properties.$pathname as page, count() as views
    FROM events
    WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 7 DAY
    GROUP BY page ORDER BY views DESC LIMIT 10
    """)

    # 5. Traffic Sources
    sources = run_query("""
    SELECT properties.$referring_domain as referrer, count() as count
    FROM events
    WHERE event = '$pageview' AND timestamp >= now() - INTERVAL 7 DAY
    GROUP BY referrer ORDER BY count DESC LIMIT 10
    """)

    # 6. Geographic Distribution
    geo = run_query("""
    SELECT properties.$geoip_country_name as country, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY country ORDER BY count DESC LIMIT 10
    """)

    # 7. Device Breakdown
    devices = run_query("""
    SELECT properties.$device_type as device, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY device ORDER BY count DESC
    """)

    # 8. Hourly Trend (last 24h)
    hourly = run_query("""
    SELECT toStartOfHour(timestamp) as hour, count() as events, uniqExact(distinct_id) as users
    FROM events
    WHERE timestamp >= now() - INTERVAL 24 HOUR
    GROUP BY hour ORDER BY hour DESC LIMIT 24
    """)

    # 9. NavBoost Events (raw counts)
    navboost = run_query("""
    SELECT event, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    AND event LIKE 'navboost:%'
    GROUP BY event
    ORDER BY count DESC
    """)

    # =====================================================
    # NEW: CONVERSIONS (5 types)
    # =====================================================
    conversions = run_query("""
    SELECT event, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    AND event LIKE 'conversion:%'
    GROUP BY event
    ORDER BY count DESC
    """)

    # =====================================================
    # NEW: NAVBOOST CALCULATED METRICS
    # =====================================================

    # Pogo Rate
    pogo_data = run_query("""
    SELECT
        countIf(properties.is_pogo = true) as pogo_sessions,
        count() as total_google_sessions,
        round(countIf(properties.is_pogo = true) * 100.0 / nullIf(count(), 0), 2) as pogo_rate
    FROM events
    WHERE event = 'navboost:session_end'
    AND properties.is_google_referrer = true
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # Dwell Time
    dwell_data = run_query("""
    SELECT
        avg(properties.dwell_time_seconds) as avg_dwell,
        median(properties.dwell_time_seconds) as median_dwell,
        countIf(properties.dwell_time_seconds < 10) as very_bad,
        countIf(properties.dwell_time_seconds >= 10 AND properties.dwell_time_seconds < 30) as weak,
        countIf(properties.dwell_time_seconds >= 30 AND properties.dwell_time_seconds < 90) as normal,
        countIf(properties.dwell_time_seconds >= 90) as strong
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # Scroll Depth Distribution
    scroll_data = run_query("""
    SELECT
        countIf(properties.max_scroll_percent >= 25) as reached_25,
        countIf(properties.max_scroll_percent >= 50) as reached_50,
        countIf(properties.max_scroll_percent >= 75) as reached_75,
        countIf(properties.max_scroll_percent >= 100) as reached_100,
        avg(properties.max_scroll_percent) as avg_scroll,
        count() as total
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # CTA Performance
    cta_data = run_query("""
    SELECT
        count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
        round(count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
              nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0), 2) as cta_ctr
    FROM events
    WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # Good Abandonment Rate
    good_abandon_data = run_query("""
    SELECT
        countIf(properties.is_good_abandonment = true) as good_abandonment_sessions,
        count() as total_google_sessions,
        round(countIf(properties.is_good_abandonment = true) * 100.0 / nullIf(count(), 0), 2) as good_abandonment_rate
    FROM events
    WHERE event = 'navboost:session_end'
    AND properties.is_google_referrer = true
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # =====================================================
    # NEW: DAILY TREND (7 days)
    # =====================================================
    daily_trend = run_query("""
    SELECT toDate(timestamp) as date, count() as events, uniqExact(distinct_id) as users
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY date ORDER BY date DESC
    """)

    # =====================================================
    # NEW: BROWSER BREAKDOWN
    # =====================================================
    browsers = run_query("""
    SELECT properties.$browser as browser, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    AND properties.$browser IS NOT NULL
    GROUP BY browser ORDER BY count DESC LIMIT 10
    """)

    # =====================================================
    # NEW: OPERATING SYSTEM BREAKDOWN
    # =====================================================
    os_data = run_query("""
    SELECT properties.$os as os, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL 7 DAY
    AND properties.$os IS NOT NULL
    GROUP BY os ORDER BY count DESC LIMIT 10
    """)

    # =====================================================
    # NEW: SESSION DURATION
    # =====================================================
    session_duration = run_query("""
    SELECT
        avg(properties.session_duration_seconds) as avg_duration,
        median(properties.session_duration_seconds) as median_duration
    FROM events
    WHERE event = '$pageleave'
    AND timestamp >= now() - INTERVAL 7 DAY
    AND properties.session_duration_seconds > 0
    """)

    # =====================================================
    # NEW: BOUNCE RATE (single page sessions)
    # =====================================================
    bounce_data = run_query("""
    SELECT
        uniqExact(properties.$session_id) as total_sessions,
        uniqExactIf(properties.$session_id, properties.$session_pageview_count = 1) as single_page_sessions
    FROM events
    WHERE event = '$pageview'
    AND timestamp >= now() - INTERVAL 7 DAY
    """)

    # Build Report
    report = []
    report.append(f"# PostHog Analytics Report - {PROJECT_NAME}")
    report.append(f"Generated: {timestamp}")
    report.append(f"Period: Last 7 Days\n")

    # Overview
    report.append("## Overview")
    if stats.get('results') and len(stats['results']) > 0:
        s = stats['results'][0]
        report.append(f"- **Total Events:** {s[0]:,}")
        report.append(f"- **Unique Users:** {s[1]:,}")
        report.append(f"- **Sessions:** {s[2]:,}")
    report.append("")

    # =====================================================
    # NEW: CONVERSIONS SECTION
    # =====================================================
    report.append("## Conversions")
    if conversions.get('results') and len(conversions['results']) > 0:
        report.append("| Conversion Type | Count |")
        report.append("|-----------------|-------|")
        total_conversions = 0
        for c in conversions['results']:
            event_name = c[0].replace('conversion:', '').replace('_', ' ').title()
            count = c[1]
            total_conversions += count
            report.append(f"| {event_name} | {count:,} |")
        report.append(f"| **TOTAL** | **{total_conversions:,}** |")
        report.append("")
        report.append("**Status:** Conversion Tracker DEPLOYED ✅")
    else:
        report.append("**Status:** ⚠️ NO CONVERSION DATA")
        report.append("*Conversion tracker may not be deployed or no conversions recorded*")
    report.append("")

    # Web Vitals
    report.append("## Web Vitals (Core Web Vitals)")
    if vitals.get('results') and len(vitals['results']) > 0:
        v = vitals['results'][0]
        lcp = v[0]
        cls = v[1]
        inp = v[2]

        lcp_rating, lcp_icon = get_lcp_rating(lcp)
        cls_rating, cls_icon = get_cls_rating(cls)
        inp_rating, inp_icon = get_inp_rating(inp)

        report.append(f"| Metric | Value | Rating |")
        report.append(f"|--------|-------|--------|")
        report.append(f"| LCP | {lcp:.0f}ms | {lcp_icon} {lcp_rating} |" if lcp else "| LCP | N/A | - |")
        report.append(f"| CLS | {cls:.3f} | {cls_icon} {cls_rating} |" if cls else "| CLS | N/A | - |")
        report.append(f"| INP | {inp:.0f}ms | {inp_icon} {inp_rating} |" if inp else "| INP | N/A | - |")
    report.append("")

    # =====================================================
    # NEW: NAVBOOST CALCULATED METRICS
    # =====================================================
    report.append("## NavBoost Metrics (Calculated)")

    has_navboost_data = False

    # Pogo Rate
    if pogo_data.get('results') and len(pogo_data['results']) > 0:
        p = pogo_data['results'][0]
        if p[1] and p[1] > 0:
            has_navboost_data = True
            pogo_rate = p[2] if p[2] else 0
            pogo_rating, pogo_icon = get_pogo_rating(pogo_rate)
            report.append(f"### Pogo Rate (Target: < 18%)")
            report.append(f"- **Pogo Sessions:** {p[0]:,}")
            report.append(f"- **Total Google Sessions:** {p[1]:,}")
            report.append(f"- **Pogo Rate:** {pogo_rate:.1f}% {pogo_icon} {pogo_rating}")
            report.append("")

    # Dwell Time
    if dwell_data.get('results') and len(dwell_data['results']) > 0:
        d = dwell_data['results'][0]
        if d[0]:
            has_navboost_data = True
            avg_dwell = d[0] if d[0] else 0
            median_dwell = d[1] if d[1] else 0
            dwell_rating, dwell_icon = get_dwell_rating(avg_dwell)
            report.append(f"### Dwell Time (Target: > 90s)")
            report.append(f"- **Average:** {avg_dwell:.1f}s {dwell_icon} {dwell_rating}")
            report.append(f"- **Median:** {median_dwell:.1f}s")
            report.append(f"- **Distribution:**")
            report.append(f"  - Very Bad (<10s): {d[2]:,}")
            report.append(f"  - Weak (10-30s): {d[3]:,}")
            report.append(f"  - Normal (30-90s): {d[4]:,}")
            report.append(f"  - Strong (>90s): {d[5]:,}")
            report.append("")

    # Scroll Depth
    if scroll_data.get('results') and len(scroll_data['results']) > 0:
        sc = scroll_data['results'][0]
        if sc[5] and sc[5] > 0:
            has_navboost_data = True
            total = sc[5]
            report.append(f"### Scroll Depth (Target: 70% reach CTA zone)")
            report.append(f"- **Average Scroll:** {sc[4]:.1f}%")
            report.append(f"- **Reached 25%:** {sc[0]:,} ({sc[0]*100/total:.1f}%)")
            report.append(f"- **Reached 50% (CTA Zone):** {sc[1]:,} ({sc[1]*100/total:.1f}%)")
            report.append(f"- **Reached 75%:** {sc[2]:,} ({sc[2]*100/total:.1f}%)")
            report.append(f"- **Reached 100%:** {sc[3]:,} ({sc[3]*100/total:.1f}%)")
            report.append("")

    # CTA CTR
    if cta_data.get('results') and len(cta_data['results']) > 0:
        ct = cta_data['results'][0]
        if ct[0] and ct[0] > 0:
            has_navboost_data = True
            cta_ctr = ct[2] if ct[2] else 0
            ctr_rating, ctr_icon = get_cta_ctr_rating(cta_ctr)
            report.append(f"### CTA Performance (Target: > 5% CTR)")
            report.append(f"- **CTA Visible:** {ct[0]:,}")
            report.append(f"- **CTA Clicks:** {ct[1]:,}")
            report.append(f"- **CTA CTR:** {cta_ctr:.2f}% {ctr_icon} {ctr_rating}")
            report.append("")

    # Good Abandonment
    if good_abandon_data.get('results') and len(good_abandon_data['results']) > 0:
        ga = good_abandon_data['results'][0]
        if ga[1] and ga[1] > 0:
            has_navboost_data = True
            ga_rate = ga[2] if ga[2] else 0
            report.append(f"### Good Abandonment (Target: > 15%)")
            report.append(f"- **Good Abandonment Sessions:** {ga[0]:,}")
            report.append(f"- **Rate:** {ga_rate:.1f}%")
            report.append("")

    if not has_navboost_data:
        report.append("**Status:** ⚠️ NO NAVBOOST DATA")
        report.append("*NavBoost tracker may not be deployed or no data recorded yet*")
        report.append("")

    # NavBoost Raw Events
    report.append("## NavBoost Events (Raw Counts)")
    if navboost.get('results') and len(navboost['results']) > 0:
        report.append("| Event | Count |")
        report.append("|-------|-------|")
        for n in navboost['results']:
            report.append(f"| {n[0]} | {n[1]:,} |")
        report.append("")
        report.append("**Status:** NavBoost Tracker DEPLOYED ✅")
    else:
        report.append("**Status:** ⚠️ NavBoost Tracker NOT DEPLOYED or NO DATA")
    report.append("")

    # =====================================================
    # NEW: DAILY TREND (7 days)
    # =====================================================
    report.append("## Daily Trend (Last 7 Days)")
    report.append("| Date | Events | Users |")
    report.append("|------|--------|-------|")
    if daily_trend.get('results'):
        for dt in daily_trend['results']:
            report.append(f"| {dt[0]} | {dt[1]:,} | {dt[2]:,} |")
    report.append("")

    # Top Events
    report.append("## Event Breakdown")
    report.append("| Event | Count |")
    report.append("|-------|-------|")
    if events.get('results'):
        for e in events['results']:
            report.append(f"| {e[0]} | {e[1]:,} |")
    report.append("")

    # Top Pages
    report.append("## Top Pages")
    report.append("| Page | Views |")
    report.append("|------|-------|")
    if pages.get('results'):
        for p in pages['results']:
            page_name = p[0] if p[0] else "(none)"
            report.append(f"| {page_name[:60]} | {p[1]:,} |")
    report.append("")

    # Traffic Sources
    report.append("## Traffic Sources")
    report.append("| Referrer | Count |")
    report.append("|----------|-------|")
    if sources.get('results'):
        for s in sources['results']:
            ref = s[0] if s[0] else "(direct)"
            report.append(f"| {ref} | {s[1]:,} |")
    report.append("")

    # Geographic Distribution
    report.append("## Geographic Distribution")
    report.append("| Country | Events |")
    report.append("|---------|--------|")
    if geo.get('results'):
        for g in geo['results']:
            country = g[0] if g[0] else "(unknown)"
            report.append(f"| {country} | {g[1]:,} |")
    report.append("")

    # Device Breakdown
    report.append("## Device Breakdown")
    report.append("| Device | Count |")
    report.append("|--------|-------|")
    if devices.get('results'):
        for d in devices['results']:
            device = d[0] if d[0] else "(unknown)"
            report.append(f"| {device} | {d[1]:,} |")
    report.append("")

    # =====================================================
    # NEW: BROWSER BREAKDOWN
    # =====================================================
    report.append("## Browser Breakdown")
    report.append("| Browser | Count |")
    report.append("|---------|-------|")
    if browsers.get('results'):
        for b in browsers['results']:
            browser = b[0] if b[0] else "(unknown)"
            report.append(f"| {browser} | {b[1]:,} |")
    report.append("")

    # =====================================================
    # NEW: OPERATING SYSTEM BREAKDOWN
    # =====================================================
    report.append("## Operating System Breakdown")
    report.append("| OS | Count |")
    report.append("|----|-------|")
    if os_data.get('results'):
        for o in os_data['results']:
            os_name = o[0] if o[0] else "(unknown)"
            report.append(f"| {os_name} | {o[1]:,} |")
    report.append("")

    # =====================================================
    # NEW: SESSION METRICS
    # =====================================================
    report.append("## Session Metrics")

    # Session Duration
    if session_duration.get('results') and len(session_duration['results']) > 0:
        sd = session_duration['results'][0]
        if sd[0]:
            report.append(f"- **Avg Session Duration:** {sd[0]:.1f}s")
            report.append(f"- **Median Session Duration:** {sd[1]:.1f}s")
        else:
            report.append("- **Avg Session Duration:** N/A ⚠️")
    else:
        report.append("- **Avg Session Duration:** N/A ⚠️")

    # Bounce Rate
    if bounce_data.get('results') and len(bounce_data['results']) > 0:
        bd = bounce_data['results'][0]
        if bd[0] and bd[0] > 0:
            bounce_rate = (bd[1] / bd[0]) * 100
            report.append(f"- **Bounce Rate:** {bounce_rate:.1f}% ({bd[1]:,} single-page / {bd[0]:,} total sessions)")
        else:
            report.append("- **Bounce Rate:** N/A ⚠️")
    else:
        report.append("- **Bounce Rate:** N/A ⚠️")
    report.append("")

    # Hourly Activity (last 24h)
    report.append("## Hourly Activity (Last 24h)")
    report.append("| Hour | Events | Users |")
    report.append("|------|--------|-------|")
    if hourly.get('results'):
        for h in hourly['results'][:12]:  # Show last 12 hours
            report.append(f"| {h[0]} | {h[1]:,} | {h[2]:,} |")
    report.append("")

    # =====================================================
    # STILL MISSING (flagged)
    # =====================================================
    report.append("## ⚠️ Statistics Still Missing")
    report.append("*These metrics require additional tracking or are not yet available:*")
    report.append("")
    report.append("| Metric | Reason |")
    report.append("|--------|--------|")
    report.append("| New vs Returning Users | Requires person identification setup |")
    report.append("| Engagement Score (composite) | Requires all NavBoost components active |")
    report.append("| Page Load Time (TTFB) | Not captured in current Web Vitals setup |")
    report.append("| Exit Pages | Requires pageleave event analysis |")
    report.append("| User Flow / Funnel | Requires funnel configuration in PostHog |")
    report.append("")

    report.append("---")
    report.append(f"*Report generated by PostHog Analytics Automation v2.0*")
    report.append(f"*Next report in 30 minutes*")

    return "\n".join(report)

def send_email(subject, body):
    """Send email report via SMTP"""
    if not SMTP_USER or not SMTP_PASSWORD:
        print("ERROR: SMTP credentials not configured")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = ', '.join(TO_EMAILS)

        # Plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        # HTML version (convert markdown to basic HTML)
        html_body = body.replace('\n', '<br>\n')
        html_body = html_body.replace('# ', '<h1>').replace('<br>\n<h1>', '</h1>\n<h1>')
        html_body = html_body.replace('## ', '<h2>').replace('<br>\n<h2>', '</h2>\n<h2>')
        html_body = html_body.replace('### ', '<h3>').replace('<br>\n<h3>', '</h3>\n<h3>')
        html_body = f"<html><body style='font-family: monospace; font-size: 14px;'>{html_body}</body></html>"
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Connect and send
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())
        server.quit()

        print(f"Email sent successfully to: {', '.join(TO_EMAILS)}")
        return True
    except Exception as e:
        print(f"ERROR sending email: {e}")
        return False

def main():
    print(f"[{datetime.now()}] Starting PostHog report generation for {PROJECT_NAME}")

    # Generate report
    report = generate_report()

    # Save to file
    report_dir = "/home/andre/reports/hudsonreporter"
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_file = f"{report_dir}/posthog_report_{timestamp}.md"

    with open(report_file, 'w') as f:
        f.write(report)

    print(f"Report saved to: {report_file}")

    # Send email
    subject = f"[PostHog] {PROJECT_NAME} Analytics Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    if send_email(subject, report):
        print("Email delivery successful")
    else:
        print("Email delivery failed")

    print(f"[{datetime.now()}] Report generation complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
