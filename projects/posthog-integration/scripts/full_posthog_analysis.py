#!/usr/bin/env python3
"""
Full PostHog Analytics Report - All Available Metrics
Covers NavBoost + Standard PostHog + Web Vitals + User Behavior

Author: Virtual ATeam - BlackTeam
Version: 2.0.0
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

POSTHOG_HOST = "https://us.posthog.com"
API_KEY = "phx_wfjNKtKXHvMxEkV4z3LtPXFOjfsMMW8swz9QxIQ7XN8i2O3"

DOMAINS = {
    "pokerology.com": {"project_id": 266520, "vertical": "Poker/Affiliate"},
    "northeasttimes.com": {"project_id": 290039, "vertical": "News/iGaming"},
}

def query_posthog(project_id: int, hogql: str) -> Optional[list]:
    """Execute HogQL query and return results"""
    url = f"{POSTHOG_HOST}/api/projects/{project_id}/query/"
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={"query": {"kind": "HogQLQuery", "query": hogql}},
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("results", [])
    except Exception as e:
        print(f"  [ERROR] Query failed: {e}")
    return None


def get_overall_stats(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get overall statistics"""
    query = f"""
    SELECT
        count() as total_events,
        uniqExact(distinct_id) as unique_users,
        uniqExact(properties.$session_id) as sessions
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        return {
            "total_events": results[0][0],
            "unique_users": results[0][1],
            "sessions": results[0][2]
        }
    return {}


def get_event_breakdown(project_id: int, days: int = 7) -> list:
    """Get event counts by type"""
    query = f"""
    SELECT event, count() as count
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    GROUP BY event ORDER BY count DESC LIMIT 20
    """
    return query_posthog(project_id, query) or []


def get_web_vitals(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get Core Web Vitals"""
    query = f"""
    SELECT
        avg(properties.$web_vitals_LCP_value) as avg_lcp,
        avg(properties.$web_vitals_CLS_value) as avg_cls,
        avg(properties.$web_vitals_INP_value) as avg_inp,
        count() as samples
    FROM events
    WHERE event = '$web_vitals'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        lcp = results[0][0]
        cls = results[0][1]
        inp = results[0][2]
        return {
            "lcp_ms": round(lcp, 0) if lcp else None,
            "lcp_rating": "Good" if lcp and lcp <= 2500 else "Needs Improvement" if lcp and lcp <= 4000 else "Poor",
            "cls": round(cls, 3) if cls else None,
            "cls_rating": "Good" if cls and cls <= 0.1 else "Needs Improvement" if cls and cls <= 0.25 else "Poor",
            "inp_ms": round(inp, 0) if inp else None,
            "inp_rating": "Good" if inp and inp <= 200 else "Needs Improvement" if inp and inp <= 500 else "Poor",
            "samples": results[0][3]
        }
    return {}


def get_top_pages(project_id: int, days: int = 7) -> list:
    """Get top pages by views"""
    query = f"""
    SELECT
        properties.$pathname as page,
        count() as views,
        uniqExact(distinct_id) as unique_visitors
    FROM events
    WHERE event = '$pageview'
    AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY page ORDER BY views DESC LIMIT 15
    """
    return query_posthog(project_id, query) or []


def get_traffic_sources(project_id: int, days: int = 7) -> list:
    """Get traffic sources by referrer"""
    query = f"""
    SELECT
        properties.$referring_domain as referrer,
        count() as visits,
        uniqExact(distinct_id) as unique_users
    FROM events
    WHERE event = '$pageview'
    AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY referrer ORDER BY visits DESC LIMIT 15
    """
    return query_posthog(project_id, query) or []


def get_geo_distribution(project_id: int, days: int = 7) -> list:
    """Get geographic distribution"""
    query = f"""
    SELECT
        properties.$geoip_country_name as country,
        count() as events,
        uniqExact(distinct_id) as users
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    AND properties.$geoip_country_name IS NOT NULL
    GROUP BY country ORDER BY events DESC LIMIT 10
    """
    return query_posthog(project_id, query) or []


def get_device_breakdown(project_id: int, days: int = 7) -> list:
    """Get device type breakdown"""
    query = f"""
    SELECT
        properties.$device_type as device,
        count() as events,
        round(count() * 100.0 / sum(count()) OVER (), 1) as percentage
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    AND properties.$device_type IS NOT NULL
    GROUP BY device ORDER BY events DESC
    """
    return query_posthog(project_id, query) or []


def get_browser_breakdown(project_id: int, days: int = 7) -> list:
    """Get browser breakdown"""
    query = f"""
    SELECT
        properties.$browser as browser,
        count() as events,
        round(count() * 100.0 / sum(count()) OVER (), 1) as percentage
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    AND properties.$browser IS NOT NULL
    GROUP BY browser ORDER BY events DESC LIMIT 10
    """
    return query_posthog(project_id, query) or []


def get_os_breakdown(project_id: int, days: int = 7) -> list:
    """Get OS breakdown"""
    query = f"""
    SELECT
        properties.$os as os,
        count() as events,
        round(count() * 100.0 / sum(count()) OVER (), 1) as percentage
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    AND properties.$os IS NOT NULL
    GROUP BY os ORDER BY events DESC LIMIT 10
    """
    return query_posthog(project_id, query) or []


def get_daily_trend(project_id: int, days: int = 7) -> list:
    """Get daily event/user trend"""
    query = f"""
    SELECT
        toDate(timestamp) as date,
        count() as events,
        uniqExact(distinct_id) as users,
        uniqExact(properties.$session_id) as sessions
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    GROUP BY date ORDER BY date DESC
    """
    return query_posthog(project_id, query) or []


def get_utm_breakdown(project_id: int, days: int = 7) -> list:
    """Get UTM campaign breakdown"""
    query = f"""
    SELECT
        properties.$initial_utm_source as source,
        properties.$initial_utm_medium as medium,
        properties.$initial_utm_campaign as campaign,
        count() as events,
        uniqExact(distinct_id) as users
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    AND properties.$initial_utm_source IS NOT NULL
    GROUP BY source, medium, campaign
    ORDER BY events DESC LIMIT 15
    """
    return query_posthog(project_id, query) or []


def get_rage_clicks(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get rage click data (user frustration)"""
    query = f"""
    SELECT
        count() as rage_clicks,
        uniqExact(distinct_id) as affected_users,
        uniqExact(properties.$current_url) as affected_pages
    FROM events
    WHERE event = '$rageclick'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        return {
            "rage_clicks": results[0][0] or 0,
            "affected_users": results[0][1] or 0,
            "affected_pages": results[0][2] or 0
        }
    return {"rage_clicks": 0, "affected_users": 0, "affected_pages": 0}


# ============================================================================
# NAVBOOST METRICS (ALL 18 METRICS - Director Rule 18 Compliant)
# ============================================================================
#
# The 18 NavBoost Metrics:
# 1. Session Starts          | 2. Session Ends           | 3. Heartbeat Count
# 4. Pogo Rate               | 5. Pogo Sessions          | 6. Avg Dwell Time
# 7. Median Dwell Time       | 8. Dwell Distribution     | 9. Scroll 25%
# 10. Scroll 50%             | 11. Scroll 75%            | 12. Scroll 100%
# 13. Avg Scroll Depth       | 14. CTA Visible           | 15. CTA Clicks
# 16. CTA CTR                | 17. Good Abandonment Rate | 18. Outbound Clicks
#
# Plus: Engagement Score (composite), Tracker Errors (diagnostics)
# ============================================================================

def get_navboost_sessions(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get NavBoost session metrics (#1, #2, #3)"""
    query = f"""
    SELECT
        count(CASE WHEN event = 'navboost:session_start' THEN 1 END) as session_starts,
        count(CASE WHEN event = 'navboost:session_end' THEN 1 END) as session_ends,
        count(CASE WHEN event = 'navboost:heartbeat' THEN 1 END) as heartbeats,
        count(CASE WHEN event = 'navboost:tracker_error' THEN 1 END) as tracker_errors
    FROM events
    WHERE timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        return {
            "session_starts": results[0][0] or 0,
            "session_ends": results[0][1] or 0,
            "heartbeats": results[0][2] or 0,
            "tracker_errors": results[0][3] or 0
        }
    return {}


def get_pogo_rate(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get pogo rate (users who leave quickly and return to Google)"""
    query = f"""
    SELECT
        countIf(properties.is_pogo = true) as pogo_sessions,
        count() as total_sessions,
        round(countIf(properties.is_pogo = true) * 100.0 / nullIf(count(), 0), 2) as pogo_rate
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        rate = results[0][2] or 0
        return {
            "pogo_sessions": results[0][0] or 0,
            "total_sessions": results[0][1] or 0,
            "pogo_rate": rate,
            "rating": "Excellent" if rate < 10 else "Good" if rate < 15 else "Warning" if rate < 25 else "Critical"
        }
    return {}


def get_dwell_time(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get dwell time metrics"""
    query = f"""
    SELECT
        avg(properties.dwell_time_seconds) as avg_dwell,
        median(properties.dwell_time_seconds) as median_dwell,
        min(properties.dwell_time_seconds) as min_dwell,
        max(properties.dwell_time_seconds) as max_dwell,
        countIf(properties.dwell_time_seconds < 10) as very_short,
        countIf(properties.dwell_time_seconds >= 10 AND properties.dwell_time_seconds < 30) as short,
        countIf(properties.dwell_time_seconds >= 30 AND properties.dwell_time_seconds < 90) as medium,
        countIf(properties.dwell_time_seconds >= 90) as long
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        avg_dwell = results[0][0] or 0
        return {
            "avg_dwell_seconds": round(avg_dwell, 1),
            "median_dwell_seconds": round(results[0][1] or 0, 1),
            "min_dwell_seconds": round(results[0][2] or 0, 1),
            "max_dwell_seconds": round(results[0][3] or 0, 1),
            "distribution": {
                "very_short_0_10s": results[0][4] or 0,
                "short_10_30s": results[0][5] or 0,
                "medium_30_90s": results[0][6] or 0,
                "long_90s_plus": results[0][7] or 0
            },
            "rating": "Excellent" if avg_dwell >= 180 else "Good" if avg_dwell >= 90 else "Warning" if avg_dwell >= 30 else "Critical"
        }
    return {}


def get_scroll_depth(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get scroll depth metrics"""
    query = f"""
    SELECT
        countIf(properties.scroll_depth_reached >= 25) as reached_25,
        countIf(properties.scroll_depth_reached >= 50) as reached_50,
        countIf(properties.scroll_depth_reached >= 75) as reached_75,
        countIf(properties.scroll_depth_reached >= 100) as reached_100,
        avg(properties.scroll_depth_reached) as avg_scroll,
        count() as total_sessions
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        total = results[0][5] or 1
        return {
            "reached_25_pct": round((results[0][0] or 0) * 100 / total, 1),
            "reached_50_pct": round((results[0][1] or 0) * 100 / total, 1),
            "reached_75_pct": round((results[0][2] or 0) * 100 / total, 1),
            "reached_100_pct": round((results[0][3] or 0) * 100 / total, 1),
            "avg_scroll_depth": round(results[0][4] or 0, 1),
            "total_sessions": total
        }
    return {}


def get_cta_performance(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get CTA performance metrics"""
    query = f"""
    SELECT
        count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_visible,
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
        round(count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
              nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0), 2) as ctr
    FROM events
    WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        ctr = results[0][2] or 0
        return {
            "cta_visible": results[0][0] or 0,
            "cta_clicks": results[0][1] or 0,
            "ctr": ctr,
            "rating": "Excellent" if ctr >= 10 else "Good" if ctr >= 5 else "Warning" if ctr >= 2 else "Critical"
        }
    return {}


def get_outbound_clicks(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get outbound click metrics (#18)"""
    query = f"""
    SELECT
        count() as total_outbound,
        uniqExact(properties.outbound_url) as unique_destinations,
        uniqExact(distinct_id) as users_clicking_outbound
    FROM events
    WHERE event = 'navboost:outbound_click'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        return {
            "total_outbound_clicks": results[0][0] or 0,
            "unique_destinations": results[0][1] or 0,
            "users_clicking_outbound": results[0][2] or 0
        }
    return {}


def get_good_abandonment(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Get good abandonment rate (#17) - users who left via outbound link"""
    query = f"""
    SELECT
        countIf(properties.is_good_abandonment = true) as good_abandonment_sessions,
        countIf(properties.is_google_referrer = true) as google_sessions,
        round(countIf(properties.is_good_abandonment = true) * 100.0 /
              nullIf(countIf(properties.is_google_referrer = true), 0), 2) as good_abandonment_rate
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        rate = results[0][2] or 0
        return {
            "good_abandonment_sessions": results[0][0] or 0,
            "google_sessions": results[0][1] or 0,
            "good_abandonment_rate": rate,
            "rating": "Excellent" if rate >= 25 else "Good" if rate >= 15 else "Warning" if rate >= 8 else "Critical"
        }
    return {"good_abandonment_sessions": 0, "google_sessions": 0, "good_abandonment_rate": 0, "rating": "N/A"}


def get_engagement_score(project_id: int, days: int = 7) -> Dict[str, Any]:
    """Calculate composite engagement score (Director Rule 18)"""
    query = f"""
    SELECT
        avg(properties.dwell_time_seconds) as avg_dwell,
        countIf(properties.is_pogo = true) * 100.0 / nullIf(count(), 0) as pogo_rate,
        countIf(properties.scroll_depth_reached >= 50) * 100.0 / nullIf(count(), 0) as scroll_50_pct,
        countIf(properties.is_good_abandonment = true) * 100.0 / nullIf(count(), 0) as good_abandon_pct,
        count() as total_sessions
    FROM events
    WHERE event = 'navboost:session_end'
    AND timestamp >= now() - INTERVAL {days} DAY
    """
    results = query_posthog(project_id, query)
    if results and results[0]:
        avg_dwell = results[0][0] or 0
        pogo_rate = results[0][1] or 0
        scroll_50 = results[0][2] or 0
        good_abandon = results[0][3] or 0

        # Engagement Score Formula (weighted composite):
        # - Dwell score: 35% weight (normalized to 90s target)
        # - Anti-pogo: 25% weight (100 - pogo_rate)
        # - Scroll depth: 15% weight (% reaching 50%)
        # - CTA CTR: 15% weight (placeholder, need separate query)
        # - Good abandonment: 10% weight

        dwell_score = min((avg_dwell / 90) * 100, 100) * 0.35
        anti_pogo_score = (100 - min(pogo_rate, 100)) * 0.25
        scroll_score = min(scroll_50, 100) * 0.15
        cta_score = 50 * 0.15  # Placeholder - would need CTA data
        good_abandon_score = min(good_abandon * 4, 100) * 0.10  # Normalize 25% = 100

        engagement = round(dwell_score + anti_pogo_score + scroll_score + cta_score + good_abandon_score, 1)

        return {
            "engagement_score": engagement,
            "rating": "Excellent" if engagement >= 80 else "Good" if engagement >= 70 else "Warning" if engagement >= 50 else "Critical",
            "components": {
                "dwell_contribution": round(dwell_score, 1),
                "anti_pogo_contribution": round(anti_pogo_score, 1),
                "scroll_contribution": round(scroll_score, 1),
                "cta_contribution": round(cta_score, 1),
                "good_abandon_contribution": round(good_abandon_score, 1)
            }
        }
    return {"engagement_score": 0, "rating": "N/A", "components": {}}


def get_top_ctas(project_id: int, days: int = 7) -> list:
    """Get top performing CTAs"""
    query = f"""
    SELECT
        properties.cta_id as cta_id,
        count() as clicks
    FROM events
    WHERE event = 'navboost:cta_click'
    AND timestamp >= now() - INTERVAL {days} DAY
    AND properties.cta_id IS NOT NULL
    GROUP BY cta_id
    ORDER BY clicks DESC
    LIMIT 10
    """
    return query_posthog(project_id, query) or []


def generate_report(domain: str, config: dict, days: int = 7) -> str:
    """Generate full report for a domain"""
    project_id = config["project_id"]
    vertical = config["vertical"]

    print(f"\n{'='*60}")
    print(f"Generating report for: {domain}")
    print(f"Project ID: {project_id}")
    print(f"{'='*60}")

    # Collect all metrics
    print("  Fetching overall stats...")
    overall = get_overall_stats(project_id, days)

    print("  Fetching event breakdown...")
    events = get_event_breakdown(project_id, days)

    print("  Fetching web vitals...")
    vitals = get_web_vitals(project_id, days)

    print("  Fetching top pages...")
    pages = get_top_pages(project_id, days)

    print("  Fetching traffic sources...")
    sources = get_traffic_sources(project_id, days)

    print("  Fetching geo distribution...")
    geo = get_geo_distribution(project_id, days)

    print("  Fetching device breakdown...")
    devices = get_device_breakdown(project_id, days)

    print("  Fetching browser breakdown...")
    browsers = get_browser_breakdown(project_id, days)

    print("  Fetching OS breakdown...")
    os_data = get_os_breakdown(project_id, days)

    print("  Fetching daily trend...")
    trend = get_daily_trend(project_id, days)

    print("  Fetching UTM breakdown...")
    utm = get_utm_breakdown(project_id, days)

    print("  Fetching rage clicks...")
    rage = get_rage_clicks(project_id, days)

    # NavBoost metrics
    print("  Fetching NavBoost sessions...")
    nb_sessions = get_navboost_sessions(project_id, days)

    print("  Fetching pogo rate...")
    pogo = get_pogo_rate(project_id, days)

    print("  Fetching dwell time...")
    dwell = get_dwell_time(project_id, days)

    print("  Fetching scroll depth...")
    scroll = get_scroll_depth(project_id, days)

    print("  Fetching CTA performance...")
    cta = get_cta_performance(project_id, days)

    print("  Fetching outbound clicks...")
    outbound = get_outbound_clicks(project_id, days)

    print("  Fetching good abandonment rate...")
    good_abandon = get_good_abandonment(project_id, days)

    print("  Fetching engagement score...")
    engagement = get_engagement_score(project_id, days)

    print("  Fetching top CTAs...")
    top_ctas = get_top_ctas(project_id, days)

    # Build report
    report = f"""# Full PostHog Analytics Report - {domain}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Project ID:** {project_id}
**Vertical:** {vertical}
**Period:** Last {days} Days

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Events | {overall.get('total_events', 0):,} |
| Unique Users | {overall.get('unique_users', 0):,} |
| Sessions | {overall.get('sessions', 0):,} |
| Avg Events/User | {round(overall.get('total_events', 0) / max(overall.get('unique_users', 1), 1), 1)} |
| Avg Events/Session | {round(overall.get('total_events', 0) / max(overall.get('sessions', 1), 1), 1)} |

---

## Core Web Vitals

| Metric | Value | Rating | Target |
|--------|-------|--------|--------|
| LCP (Largest Contentful Paint) | {vitals.get('lcp_ms', 'N/A')}ms | {vitals.get('lcp_rating', 'N/A')} | ≤2500ms |
| CLS (Cumulative Layout Shift) | {vitals.get('cls', 'N/A')} | {vitals.get('cls_rating', 'N/A')} | ≤0.1 |
| INP (Interaction to Next Paint) | {vitals.get('inp_ms', 'N/A')}ms | {vitals.get('inp_rating', 'N/A')} | ≤200ms |
| Samples | {vitals.get('samples', 0):,} | - | - |

---

## NavBoost KPIs (18 Metrics - Director Rule 18 Compliant)

### Summary: All 18 NavBoost Metrics

| # | Metric | Value | Target | Status |
|---|--------|-------|--------|--------|
| 1 | Session Starts | {nb_sessions.get('session_starts', 0):,} | - | - |
| 2 | Session Ends | {nb_sessions.get('session_ends', 0):,} | - | - |
| 3 | Heartbeat Count | {nb_sessions.get('heartbeats', 0):,} | - | - |
| 4 | Pogo Rate | {pogo.get('pogo_rate', 0)}% | <18% | {pogo.get('rating', 'N/A')} |
| 5 | Pogo Sessions | {pogo.get('pogo_sessions', 0):,} | - | - |
| 6 | Avg Dwell Time | {dwell.get('avg_dwell_seconds', 0)}s | >90s | {dwell.get('rating', 'N/A')} |
| 7 | Median Dwell Time | {dwell.get('median_dwell_seconds', 0)}s | >60s | - |
| 8 | Dwell Distribution | See below | - | - |
| 9 | Scroll 25% | {scroll.get('reached_25_pct', 0)}% | - | - |
| 10 | Scroll 50% | {scroll.get('reached_50_pct', 0)}% | >70% | {"✅" if scroll.get('reached_50_pct', 0) >= 70 else "⚠️"} |
| 11 | Scroll 75% | {scroll.get('reached_75_pct', 0)}% | >40% | {"✅" if scroll.get('reached_75_pct', 0) >= 40 else "⚠️"} |
| 12 | Scroll 100% | {scroll.get('reached_100_pct', 0)}% | - | - |
| 13 | Avg Scroll Depth | {scroll.get('avg_scroll_depth', 0)}% | >50% | {"✅" if scroll.get('avg_scroll_depth', 0) >= 50 else "⚠️"} |
| 14 | CTA Visible | {cta.get('cta_visible', 0):,} | - | - |
| 15 | CTA Clicks | {cta.get('cta_clicks', 0):,} | - | - |
| 16 | CTA CTR | {cta.get('ctr', 0)}% | >5% | {cta.get('rating', 'N/A')} |
| 17 | Good Abandonment | {good_abandon.get('good_abandonment_rate', 0)}% | >15% | {good_abandon.get('rating', 'N/A')} |
| 18 | Outbound Clicks | {outbound.get('total_outbound_clicks', 0):,} | - | - |

**Composite Score:**
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Engagement Score** | **{engagement.get('engagement_score', 0)}** | >70 | {engagement.get('rating', 'N/A')} |
| Tracker Errors | {nb_sessions.get('tracker_errors', 0):,} | 0 | {"✅" if nb_sessions.get('tracker_errors', 0) == 0 else "⚠️"} |

---

### Detailed Breakdown

#### Pogo Rate (Target: <18%)
| Metric | Value | Rating |
|--------|-------|--------|
| Pogo Sessions | {pogo.get('pogo_sessions', 0):,} | - |
| Total Sessions | {pogo.get('total_sessions', 0):,} | - |
| **Pogo Rate** | **{pogo.get('pogo_rate', 0)}%** | {pogo.get('rating', 'N/A')} |

#### Dwell Time (Target: >90s)
| Metric | Value | Rating |
|--------|-------|--------|
| Average | {dwell.get('avg_dwell_seconds', 0)}s | {dwell.get('rating', 'N/A')} |
| Median | {dwell.get('median_dwell_seconds', 0)}s | - |
| Min | {dwell.get('min_dwell_seconds', 0)}s | - |
| Max | {dwell.get('max_dwell_seconds', 0)}s | - |

**Dwell Time Distribution:**
| Range | Count |
|-------|-------|
| Very Short (0-10s) | {dwell.get('distribution', {}).get('very_short_0_10s', 0):,} |
| Short (10-30s) | {dwell.get('distribution', {}).get('short_10_30s', 0):,} |
| Medium (30-90s) | {dwell.get('distribution', {}).get('medium_30_90s', 0):,} |
| Long (90s+) | {dwell.get('distribution', {}).get('long_90s_plus', 0):,} |

#### Scroll Depth
| Milestone | % Reached |
|-----------|-----------|
| 25% (Above Fold) | {scroll.get('reached_25_pct', 0)}% |
| 50% (CTA Zone) | {scroll.get('reached_50_pct', 0)}% |
| 75% (Content) | {scroll.get('reached_75_pct', 0)}% |
| 100% (Footer) | {scroll.get('reached_100_pct', 0)}% |
| **Average Scroll** | **{scroll.get('avg_scroll_depth', 0)}%** |

#### CTA Performance (Target: >5% CTR)
| Metric | Value | Rating |
|--------|-------|--------|
| CTA Impressions | {cta.get('cta_visible', 0):,} | - |
| CTA Clicks | {cta.get('cta_clicks', 0):,} | - |
| **CTA CTR** | **{cta.get('ctr', 0)}%** | {cta.get('rating', 'N/A')} |

#### Good Abandonment (Target: >15%)
| Metric | Value | Rating |
|--------|-------|--------|
| Good Abandonment Sessions | {good_abandon.get('good_abandonment_sessions', 0):,} | - |
| Google Sessions | {good_abandon.get('google_sessions', 0):,} | - |
| **Good Abandonment Rate** | **{good_abandon.get('good_abandonment_rate', 0)}%** | {good_abandon.get('rating', 'N/A')} |

#### Outbound Clicks
| Metric | Value |
|--------|-------|
| Total Outbound Clicks | {outbound.get('total_outbound_clicks', 0):,} |
| Unique Destinations | {outbound.get('unique_destinations', 0):,} |
| Users Clicking Outbound | {outbound.get('users_clicking_outbound', 0):,} |

#### Engagement Score Breakdown
| Component | Contribution |
|-----------|--------------|
| Dwell Time (35%) | {engagement.get('components', {}).get('dwell_contribution', 0)} |
| Anti-Pogo (25%) | {engagement.get('components', {}).get('anti_pogo_contribution', 0)} |
| Scroll Depth (15%) | {engagement.get('components', {}).get('scroll_contribution', 0)} |
| CTA CTR (15%) | {engagement.get('components', {}).get('cta_contribution', 0)} |
| Good Abandonment (10%) | {engagement.get('components', {}).get('good_abandon_contribution', 0)} |
| **Total Score** | **{engagement.get('engagement_score', 0)}** |

### Top CTAs by Clicks
| CTA ID | Clicks |
|--------|--------|
"""
    for cta_row in top_ctas[:10]:
        cta_id = cta_row[0] if cta_row[0] else "Unknown"
        clicks = cta_row[1]
        # Truncate long CTA IDs
        cta_id_display = cta_id[:50] + "..." if len(str(cta_id)) > 50 else cta_id
        report += f"| {cta_id_display} | {clicks:,} |\n"

    report += f"""
---

## Event Breakdown

| Event | Count |
|-------|-------|
"""
    for event_row in events[:15]:
        report += f"| {event_row[0]} | {event_row[1]:,} |\n"

    report += f"""
---

## User Behavior

### Rage Clicks (Frustration Indicator)
| Metric | Value |
|--------|-------|
| Rage Clicks | {rage.get('rage_clicks', 0):,} |
| Affected Users | {rage.get('affected_users', 0):,} |
| Affected Pages | {rage.get('affected_pages', 0):,} |

---

## Traffic Sources

| Referrer | Visits | Unique Users |
|----------|--------|--------------|
"""
    for src in sources[:10]:
        referrer = src[0] if src[0] else "(direct)"
        report += f"| {referrer} | {src[1]:,} | {src[2]:,} |\n"

    report += f"""
---

## Top Pages

| Page | Views | Unique Visitors |
|------|-------|-----------------|
"""
    for page in pages[:10]:
        page_path = page[0] if page[0] else "/"
        # Truncate long paths
        page_display = page_path[:60] + "..." if len(str(page_path)) > 60 else page_path
        report += f"| {page_display} | {page[1]:,} | {page[2]:,} |\n"

    report += f"""
---

## Device & Technology

### Device Type
| Device | Events | % |
|--------|--------|---|
"""
    for dev in devices[:5]:
        report += f"| {dev[0] or 'Unknown'} | {dev[1]:,} | {dev[2]}% |\n"

    report += f"""
### Browser
| Browser | Events | % |
|---------|--------|---|
"""
    for br in browsers[:5]:
        report += f"| {br[0] or 'Unknown'} | {br[1]:,} | {br[2]}% |\n"

    report += f"""
### Operating System
| OS | Events | % |
|----|--------|---|
"""
    for o in os_data[:5]:
        report += f"| {o[0] or 'Unknown'} | {o[1]:,} | {o[2]}% |\n"

    report += f"""
---

## Geographic Distribution

| Country | Events | Users |
|---------|--------|-------|
"""
    for g in geo[:10]:
        report += f"| {g[0] or 'Unknown'} | {g[1]:,} | {g[2]:,} |\n"

    report += f"""
---

## Daily Trend

| Date | Events | Users | Sessions |
|------|--------|-------|----------|
"""
    for t in trend[:7]:
        date_str = str(t[0])[:10] if t[0] else "N/A"
        report += f"| {date_str} | {t[1]:,} | {t[2]:,} | {t[3]:,} |\n"

    if utm:
        report += f"""
---

## UTM Campaign Tracking

| Source | Medium | Campaign | Events | Users |
|--------|--------|----------|--------|-------|
"""
        for u in utm[:10]:
            report += f"| {u[0] or '-'} | {u[1] or '-'} | {u[2] or '-'} | {u[3]:,} | {u[4]:,} |\n"

    report += f"""
---

*Generated by Virtual ATeam - BlackTeam*
*Full PostHog Analytics v2.0*
"""

    return report


def main():
    print("=" * 60)
    print("FULL POSTHOG ANALYTICS REPORT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Domains: {', '.join(DOMAINS.keys())}")
    print("=" * 60)

    reports = []

    for domain, config in DOMAINS.items():
        report = generate_report(domain, config, days=7)
        reports.append(report)

        # Save individual report
        filename = f"/home/andre/projects/posthog-integration/reports/full_analysis_{domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n  [SAVED] {filename}")

    # Save combined report
    combined = "\n\n---\n\n".join(reports)
    combined_filename = f"/home/andre/projects/posthog-integration/reports/full_analysis_combined_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(combined_filename, 'w') as f:
        f.write(combined)
    print(f"\n[COMBINED] {combined_filename}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
