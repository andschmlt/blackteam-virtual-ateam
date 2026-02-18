#!/usr/bin/env python3
"""
PostHog Monitoring Script - hudsonreporter.com
Director: BlackTeam
Runs every 30 minutes per stakeholder request

Follows:
- Director Rule 1: PDF Generation (MANDATORY)
- Director Rule 2: No Broken Tables
- Director Rule 8: Head of Product Assignment
- /posthog_analysis command standards
"""

import json
import urllib.request
import os
from datetime import datetime
from fpdf import FPDF

# Configuration
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.keys/.env"))
API_KEY = os.environ.get("POSTHOG_PERSONAL_API_KEY")
if not API_KEY:
    raise ValueError("POSTHOG_PERSONAL_API_KEY not found in ~/.keys/.env")
PROJECT_ID = 295222
DOMAIN = "hudsonreporter.com"
BASE_URL = f"https://us.i.posthog.com/api/projects/{PROJECT_ID}/query/"
OUTPUT_DIR = "/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/reports/all_projects"

def run_query(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({"query": {"kind": "HogQLQuery", "query": query}}).encode()
    req = urllib.request.Request(BASE_URL, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_value(result, default=0):
    """Safely extract value from query result"""
    if "results" in result and result["results"] and result["results"][0]:
        return result["results"][0][0] if result["results"][0][0] is not None else default
    return default

# ============================================================
# HOGQL QUERIES - Full KPI Suite
# ============================================================

QUERIES = {
    # Overall Stats
    "overall": """
        SELECT count() as total_events, 
               uniqExact(distinct_id) as unique_users, 
               uniqExact(properties.$session_id) as sessions 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY
    """,
    
    # Event Breakdown
    "events": """
        SELECT event, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY event ORDER BY count DESC LIMIT 20
    """,
    
    # NavBoost Events
    "navboost_events": """
        SELECT event, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        AND event LIKE 'navboost:%' 
        GROUP BY event ORDER BY count DESC
    """,
    
    # Session Start/End
    "session_start": "SELECT count() FROM events WHERE event = 'navboost:session_start' AND timestamp >= now() - INTERVAL 7 DAY",
    "session_end": "SELECT count() FROM events WHERE event = 'navboost:session_end' AND timestamp >= now() - INTERVAL 7 DAY",
    
    # Init Events (v1.1.1)
    "init_start": "SELECT count() FROM events WHERE event = 'navboost:init_start' AND timestamp >= now() - INTERVAL 7 DAY",
    "init_complete": "SELECT count() FROM events WHERE event = 'navboost:init_complete' AND timestamp >= now() - INTERVAL 7 DAY",
    
    # Tracker Errors
    "tracker_errors": """
        SELECT properties.error_context as context, 
               properties.error_message as message, 
               count() as count 
        FROM events 
        WHERE event = 'navboost:tracker_error' 
        AND timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY context, message 
        ORDER BY count DESC
    """,
    
    # Scroll Zones
    "scroll_zones": "SELECT count() FROM events WHERE event = 'navboost:scroll_zone' AND timestamp >= now() - INTERVAL 7 DAY",
    
    # CTA Events
    "cta_visible": "SELECT count() FROM events WHERE event = 'navboost:cta_visible' AND timestamp >= now() - INTERVAL 7 DAY",
    "cta_click": "SELECT count() FROM events WHERE event = 'navboost:cta_click' AND timestamp >= now() - INTERVAL 7 DAY",
    
    # Pogo Rate (Google referrer sessions with quick bounce)
    "pogo_rate": """
        SELECT 
            countIf(toFloat64OrNull(properties.dwell_time_seconds) < 10) as pogo_sessions,
            count() as total_sessions,
            round(countIf(toFloat64OrNull(properties.dwell_time_seconds) < 10) * 100.0 / nullIf(count(), 0), 2) as pogo_rate
        FROM events 
        WHERE event = 'navboost:session_end' 
        AND timestamp >= now() - INTERVAL 7 DAY
    """,
    
    # Dwell Time
    "dwell_time": """
        SELECT 
            avg(toFloat64OrNull(properties.dwell_time_seconds)) as avg_dwell,
            median(toFloat64OrNull(properties.dwell_time_seconds)) as median_dwell,
            min(toFloat64OrNull(properties.dwell_time_seconds)) as min_dwell,
            max(toFloat64OrNull(properties.dwell_time_seconds)) as max_dwell,
            count() as samples
        FROM events 
        WHERE event = 'navboost:session_end' 
        AND timestamp >= now() - INTERVAL 7 DAY
        AND properties.dwell_time_seconds IS NOT NULL
    """,
    
    # Scroll Depth Distribution
    "scroll_depth": """
        SELECT 
            properties.zone as zone,
            count() as count
        FROM events 
        WHERE event = 'navboost:scroll_zone' 
        AND timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY zone 
        ORDER BY zone
    """,
    
    # Web Vitals
    "web_vitals": """
        SELECT 
            avg(properties.$web_vitals_LCP_value) as avg_LCP,
            avg(properties.$web_vitals_CLS_value) as avg_CLS,
            avg(properties.$web_vitals_INP_value) as avg_INP,
            median(properties.$web_vitals_LCP_value) as median_LCP,
            median(properties.$web_vitals_CLS_value) as median_CLS,
            median(properties.$web_vitals_INP_value) as median_INP,
            count() as samples
        FROM events 
        WHERE event = '$web_vitals' 
        AND timestamp >= now() - INTERVAL 7 DAY
    """,
    
    # Top Pages
    "top_pages": """
        SELECT properties.$pathname as page, count() as views 
        FROM events 
        WHERE event = '$pageview' 
        AND timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY page ORDER BY views DESC LIMIT 15
    """,
    
    # Traffic Sources
    "traffic": """
        SELECT properties.$referring_domain as referrer, count() as count 
        FROM events 
        WHERE event = '$pageview' 
        AND timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY referrer ORDER BY count DESC LIMIT 10
    """,
    
    # Geographic Distribution
    "geo": """
        SELECT properties.$geoip_country_name as country, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY country ORDER BY count DESC LIMIT 10
    """,
    
    # Device Breakdown
    "device": """
        SELECT properties.$device_type as device, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY device ORDER BY count DESC
    """,
    
    # Browser Breakdown
    "browser": """
        SELECT properties.$browser as browser, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY browser ORDER BY count DESC LIMIT 10
    """,
    
    # OS Breakdown
    "os": """
        SELECT properties.$os as os, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY os ORDER BY count DESC LIMIT 10
    """,
    
    # Daily Trend
    "daily": """
        SELECT toDate(timestamp) as date, count() as events, uniqExact(distinct_id) as users 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        GROUP BY date ORDER BY date DESC
    """,
    
    # Hourly Pattern (Today)
    "hourly": """
        SELECT toHour(timestamp) as hour, count() as events 
        FROM events 
        WHERE toDate(timestamp) = today() 
        GROUP BY hour ORDER BY hour
    """,
    
    # Conversion Events
    "conversions": """
        SELECT event, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        AND event LIKE 'conversion:%' 
        GROUP BY event ORDER BY count DESC
    """,
    
    # Article Events
    "article_events": """
        SELECT event, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        AND event LIKE 'article:%' 
        GROUP BY event ORDER BY count DESC
    """,
    
    # Ad Events
    "ad_events": """
        SELECT event, count() as count 
        FROM events 
        WHERE timestamp >= now() - INTERVAL 7 DAY 
        AND event LIKE 'ad:%' 
        GROUP BY event ORDER BY count DESC
    """,
    
    # Outbound Clicks
    "outbound": "SELECT count() FROM events WHERE event = 'navboost:outbound_click' AND timestamp >= now() - INTERVAL 7 DAY",
    
    # Recent Sessions (Last Hour)
    "recent_sessions": """
        SELECT count() as sessions, uniqExact(distinct_id) as users
        FROM events 
        WHERE event = 'navboost:session_start'
        AND timestamp >= now() - INTERVAL 1 HOUR
    """,
    
    # v1.1.1 Init Results
    "init_results": """
        SELECT 
            properties.init_results as results,
            count() as count
        FROM events 
        WHERE event = 'navboost:init_complete'
        AND timestamp >= now() - INTERVAL 7 DAY
        GROUP BY results
        ORDER BY count DESC
        LIMIT 10
    """
}

def generate_report():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_str = datetime.now().strftime('%Y%m%d_%H%M')
    
    print(f"\n{'='*70}")
    print(f"POSTHOG FULL ANALYTICS REPORT - {DOMAIN}")
    print(f"{'='*70}")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Generated: {timestamp}")
    print(f"Assigned: Head of Product (Director Rule 8)")
    print(f"{'='*70}")
    
    # Run all queries
    results = {}
    for name, query in QUERIES.items():
        results[name] = run_query(query)
    
    # ============================================================
    # EXECUTIVE SUMMARY
    # ============================================================
    print("\n## EXECUTIVE SUMMARY")
    
    overall = results["overall"]["results"][0] if "results" in results["overall"] else [0,0,0]
    total_events = overall[0]
    unique_users = overall[1]
    sessions = overall[2]
    
    session_starts = get_value(results["session_start"])
    session_ends = get_value(results["session_end"])
    capture_rate = (session_ends / session_starts * 100) if session_starts > 0 else 0
    
    init_starts = get_value(results["init_start"])
    init_completes = get_value(results["init_complete"])
    
    print(f"Total Events: {total_events:,}")
    print(f"Unique Users: {unique_users:,}")
    print(f"Sessions: {sessions:,}")
    print(f"Session Capture Rate: {capture_rate:.1f}% (Target: 80%+)")
    
    # v1.1.1 Status
    print(f"\n### v1.1.1 Deployment Status")
    if init_starts > 0:
        print(f"  ✅ DEPLOYED - {init_starts} init_start, {init_completes} init_complete events")
    else:
        print(f"  ❌ NOT DEPLOYED - No init events detected")
    
    # ============================================================
    # NAVBOOST METRICS
    # ============================================================
    print("\n## NAVBOOST METRICS")
    
    # Events
    print("\n### NavBoost Events")
    if "results" in results["navboost_events"]:
        print(f"{'Event':<45} {'Count':>10}")
        print("-" * 57)
        for r in results["navboost_events"]["results"]:
            print(f"{r[0]:<45} {r[1]:>10,}")
    
    # Session Capture
    print(f"\n### Session Capture Analysis")
    print(f"Session Starts: {session_starts:,}")
    print(f"Session Ends: {session_ends:,}")
    print(f"Capture Rate: {capture_rate:.1f}%")
    if capture_rate < 80:
        print(f"  ⚠️ BELOW TARGET by {80 - capture_rate:.1f}%")
    else:
        print(f"  ✅ ON TARGET")
    
    # Tracker Errors
    print(f"\n### Tracker Errors")
    if "results" in results["tracker_errors"] and results["tracker_errors"]["results"]:
        for r in results["tracker_errors"]["results"]:
            print(f"  ⚠️ {r[0]}: {r[1]} ({r[2]} occurrences)")
    else:
        print("  ✅ No errors detected")
    
    # Pogo Rate
    print(f"\n### Pogo Rate (Target: <18%)")
    if "results" in results["pogo_rate"] and results["pogo_rate"]["results"][0][0] is not None:
        pogo = results["pogo_rate"]["results"][0]
        pogo_sessions, total_pogo, pogo_rate_val = pogo[0], pogo[1], pogo[2]
        print(f"Pogo Sessions (<10s): {pogo_sessions}")
        print(f"Total Sessions: {total_pogo}")
        print(f"Pogo Rate: {pogo_rate_val}%")
        if pogo_rate_val and float(pogo_rate_val) > 18:
            print(f"  ⚠️ ABOVE TARGET")
        else:
            print(f"  ✅ Within target")
    else:
        print("  No pogo data available yet")
    
    # Dwell Time
    print(f"\n### Dwell Time (Target: >90s)")
    if "results" in results["dwell_time"] and results["dwell_time"]["results"][0][0] is not None:
        dwell = results["dwell_time"]["results"][0]
        print(f"Average: {dwell[0]:.1f}s" if dwell[0] else "Average: N/A")
        print(f"Median: {dwell[1]:.1f}s" if dwell[1] else "Median: N/A")
        print(f"Min: {dwell[2]:.1f}s" if dwell[2] else "Min: N/A")
        print(f"Max: {dwell[3]:.1f}s" if dwell[3] else "Max: N/A")
        print(f"Samples: {dwell[4]}")
        if dwell[0] and dwell[0] >= 90:
            print(f"  ✅ ON TARGET")
        elif dwell[0]:
            print(f"  ⚠️ BELOW TARGET by {90 - dwell[0]:.1f}s")
    else:
        print("  No dwell time data available yet")
    
    # Scroll Depth
    print(f"\n### Scroll Depth Zones")
    scroll_zones = get_value(results["scroll_zones"])
    print(f"Total Scroll Events: {scroll_zones:,}")
    if "results" in results["scroll_depth"] and results["scroll_depth"]["results"]:
        for r in results["scroll_depth"]["results"]:
            print(f"  Zone {r[0]}: {r[1]:,}")
    
    # CTA Performance
    print(f"\n### CTA Performance (Target: >5% CTR)")
    cta_visible = get_value(results["cta_visible"])
    cta_click = get_value(results["cta_click"])
    cta_ctr = (cta_click / cta_visible * 100) if cta_visible > 0 else 0
    print(f"CTA Visible: {cta_visible:,}")
    print(f"CTA Clicks: {cta_click:,}")
    print(f"CTR: {cta_ctr:.2f}%")
    if cta_ctr >= 5:
        print(f"  ✅ ON TARGET")
    else:
        print(f"  ⚠️ BELOW TARGET")
    
    # Outbound Clicks
    outbound = get_value(results["outbound"])
    print(f"\n### Outbound Clicks: {outbound:,}")
    
    # ============================================================
    # WEB VITALS
    # ============================================================
    print("\n## WEB VITALS")
    if "results" in results["web_vitals"] and results["web_vitals"]["results"][0][0]:
        wv = results["web_vitals"]["results"][0]
        lcp, cls_val, inp = wv[0], wv[1], wv[2]
        lcp_med, cls_med, inp_med = wv[3], wv[4], wv[5]
        samples = wv[6]
        
        lcp_rating = "Good" if lcp <= 1200 else ("Needs Improvement" if lcp <= 2500 else "Poor")
        cls_rating = "Good" if cls_val <= 0.1 else ("Needs Improvement" if cls_val <= 0.25 else "Poor")
        inp_rating = "Good" if inp <= 200 else ("Needs Improvement" if inp <= 500 else "Poor")
        
        print(f"{'Metric':<10} {'Average':>12} {'Median':>12} {'Rating':<20}")
        print("-" * 56)
        print(f"{'LCP':<10} {lcp:>10.0f}ms {lcp_med:>10.0f}ms {lcp_rating:<20}")
        print(f"{'CLS':<10} {cls_val:>12.3f} {cls_med:>12.3f} {cls_rating:<20}")
        print(f"{'INP':<10} {inp:>10.0f}ms {inp_med:>10.0f}ms {inp_rating:<20}")
        print(f"Samples: {samples:,}")
    else:
        print("No Web Vitals data")
    
    # ============================================================
    # TRAFFIC ANALYSIS
    # ============================================================
    print("\n## TOP PAGES")
    if "results" in results["top_pages"]:
        print(f"{'Views':>8} | Page")
        print("-" * 70)
        for r in results["top_pages"]["results"][:10]:
            page = r[0][:55] if r[0] else "(none)"
            print(f"{r[1]:>8,} | {page}")
    
    print("\n## TRAFFIC SOURCES")
    if "results" in results["traffic"]:
        print(f"{'Count':>10} | Source")
        print("-" * 50)
        for r in results["traffic"]["results"]:
            ref = r[0] if r[0] else "(direct)"
            print(f"{r[1]:>10,} | {ref}")
    
    print("\n## GEOGRAPHIC DISTRIBUTION")
    if "results" in results["geo"]:
        for r in results["geo"]["results"]:
            if r[0]:
                print(f"  {r[0]}: {r[1]:,}")
    
    print("\n## DEVICE BREAKDOWN")
    if "results" in results["device"]:
        for r in results["device"]["results"]:
            if r[0]:
                print(f"  {r[0]}: {r[1]:,}")
    
    print("\n## BROWSER BREAKDOWN")
    if "results" in results["browser"]:
        for r in results["browser"]["results"][:5]:
            if r[0]:
                print(f"  {r[0]}: {r[1]:,}")
    
    print("\n## OS BREAKDOWN")
    if "results" in results["os"]:
        for r in results["os"]["results"][:5]:
            if r[0]:
                print(f"  {r[0]}: {r[1]:,}")
    
    # ============================================================
    # TRENDS
    # ============================================================
    print("\n## DAILY TREND (Last 7 Days)")
    if "results" in results["daily"]:
        print(f"{'Date':<12} {'Events':>12} {'Users':>10}")
        print("-" * 36)
        for r in results["daily"]["results"]:
            print(f"{r[0]:<12} {r[1]:>12,} {r[2]:>10,}")
    
    print("\n## HOURLY PATTERN (Today)")
    if "results" in results["hourly"] and results["hourly"]["results"]:
        print(f"{'Hour':>6} | {'Events':>10}")
        print("-" * 20)
        for r in results["hourly"]["results"]:
            print(f"{r[0]:>6} | {r[1]:>10,}")
    
    # ============================================================
    # CONVERSION & ENGAGEMENT
    # ============================================================
    print("\n## CONVERSION EVENTS")
    if "results" in results["conversions"] and results["conversions"]["results"]:
        for r in results["conversions"]["results"]:
            print(f"  {r[0]}: {r[1]:,}")
    else:
        print("  No conversion events")
    
    print("\n## ARTICLE EVENTS")
    if "results" in results["article_events"] and results["article_events"]["results"]:
        for r in results["article_events"]["results"]:
            print(f"  {r[0]}: {r[1]:,}")
    else:
        print("  No article events")
    
    print("\n## AD EVENTS")
    if "results" in results["ad_events"] and results["ad_events"]["results"]:
        for r in results["ad_events"]["results"]:
            print(f"  {r[0]}: {r[1]:,}")
    else:
        print("  No ad events")
    
    # ============================================================
    # REAL-TIME
    # ============================================================
    print("\n## REAL-TIME (Last Hour)")
    if "results" in results["recent_sessions"]:
        recent = results["recent_sessions"]["results"][0]
        print(f"Sessions: {recent[0]:,}")
        print(f"Users: {recent[1]:,}")
    
    # ============================================================
    # PRODUCT INSIGHTS (Director Rule 8)
    # ============================================================
    print("\n## PRODUCT INSIGHTS (Head of Product)")
    print("-" * 50)
    
    # Calculate engagement score
    dwell_score = min((results["dwell_time"]["results"][0][0] or 0) / 90 * 100, 100) if "results" in results["dwell_time"] and results["dwell_time"]["results"][0][0] else 0
    pogo_score = 100 - (float(results["pogo_rate"]["results"][0][2] or 0)) if "results" in results["pogo_rate"] and results["pogo_rate"]["results"][0][2] else 50
    cta_score = min(cta_ctr / 5 * 100, 100)
    
    engagement_score = (0.35 * dwell_score) + (0.25 * pogo_score) + (0.25 * cta_score) + (0.15 * min(capture_rate, 100))
    
    print(f"Engagement Score: {engagement_score:.1f}/100")
    print(f"  - Dwell Component (35%): {dwell_score:.1f}")
    print(f"  - Pogo Component (25%): {pogo_score:.1f}")
    print(f"  - CTA Component (25%): {cta_score:.1f}")
    print(f"  - Capture Component (15%): {min(capture_rate, 100):.1f}")
    
    if engagement_score >= 70:
        print(f"\n  ✅ Engagement Score ON TARGET (≥70)")
    else:
        print(f"\n  ⚠️ Engagement Score BELOW TARGET ({70 - engagement_score:.1f} points needed)")
    
    # Key Recommendations
    print("\n### Recommendations")
    if capture_rate < 80:
        print(f"  1. Session capture rate critical ({capture_rate:.1f}%) - monitor v1.1.1 deployment")
    if cta_ctr < 5:
        print(f"  2. CTA CTR below target ({cta_ctr:.2f}%) - review CTA placement/copy")
    if "results" in results["web_vitals"] and results["web_vitals"]["results"][0][0]:
        if results["web_vitals"]["results"][0][2] > 500:
            print(f"  3. INP is Poor ({results['web_vitals']['results'][0][2]:.0f}ms) - reduce JS blocking")
    
    print(f"\n{'='*70}")
    print(f"END OF REPORT - {timestamp}")
    print(f"{'='*70}\n")
    
    return results, {
        "total_events": total_events,
        "unique_users": unique_users,
        "sessions": sessions,
        "capture_rate": capture_rate,
        "init_starts": init_starts,
        "init_completes": init_completes,
        "engagement_score": engagement_score
    }

if __name__ == "__main__":
    generate_report()

# ============================================================
# EMAIL FUNCTION
# ============================================================

def send_email_report(summary):
    """Send report via email using global email utility"""
    import subprocess
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    subject = f"PostHog Report - hudsonreporter.com - {timestamp}"
    
    body = f"""PostHog Analytics Report - hudsonreporter.com
Generated: {timestamp}
Assigned: Head of Product (Director Rule 8)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Events:     {summary['total_events']:,}
Unique Users:     {summary['unique_users']:,}
Sessions:         {summary['sessions']:,}
Capture Rate:     {summary['capture_rate']:.1f}% (Target: 80%+)
Engagement Score: {summary['engagement_score']:.1f}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
v1.1.1 DEPLOYMENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Init Start Events:    {summary['init_starts']}
Init Complete Events: {summary['init_completes']}
Status: {'✅ DEPLOYED' if summary['init_starts'] > 0 else '❌ NOT DEPLOYED'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Capture Rate: {'⚠️ BELOW TARGET' if summary['capture_rate'] < 80 else '✅ ON TARGET'}
Engagement:   {'⚠️ BELOW TARGET' if summary['engagement_score'] < 70 else '✅ ON TARGET'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full report available at:
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/reports/

-- BlackTeam (Head of Product)
"""
    
    # Use the global email utility
    email_script = "/home/andre/.keys/send_email.py"
    recipient = "andre@paradisemedia.com"
    
    try:
        result = subprocess.run(
            ["python3", email_script, recipient, subject, body],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ Email sent to {recipient}")
        else:
            print(f"⚠️ Email error: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Email failed: {e}")

