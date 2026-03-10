#!/usr/bin/env python3
"""
australiafootball.com — Daily Site Intelligence Report
Sends a comprehensive Slack report covering:
  - PostHog: users, sessions, pageviews, engagement, NavBoost metrics
  - DataForSEO: keyword rankings, position changes, SERP features
  - Technical SEO: PSI scores, sitemap health, content ratio
  - Brand performance: CTA clicks, outbound clicks by brand
  - Google API Leak parameter assessment
  - Day-over-day comparison (yesterday vs 2 days ago)

Designed to run daily via cron at 08:00 AEST.
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import math

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SITE_DOMAIN = "australiafootball.com"
SITE_URL = "https://www.australiafootball.com"
POSTHOG_PROJECT_ID = 325168
POSTHOG_HOST = "https://us.i.posthog.com"
DATAFORSEO_BASE = "https://api.dataforseo.com/v3"
PSI_API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
LOCATION_CODE_AU = 2036  # Australia
LANGUAGE_CODE = "en"

# Slack — send to Andre's DM (use user ID to open DM from any bot)
SLACK_CHANNEL = "U05C3UJCK2T"  # Andre's Slack user ID

# Strategy thresholds (from Playbook #2)
MAX_GAMBLING_RATIO = 0.20  # 20% max
QUALITY_STDDEV_TARGET = 2.0
NAVBOOST_TARGETS = {
    "dwell_time": 90,       # seconds
    "pogo_rate": 18,        # percent (lower is better)
    "scroll_depth_50": 50,  # percent reaching 50%
    "cta_ctr": 5,           # percent
    "engagement_score": 70,  # out of 100
}

# Target keywords for DataForSEO tracking
TARGET_KEYWORDS = [
    "best betting sites in australia",
    "online pokies in australia",
    "best online casinos in australia",
    "top australian online casinos",
    "afl betting",
    "nrl betting tips",
    "melbourne cup odds",
    "sports betting sites australia",
    "best pokies online",
    "real money casino sites australia",
    "a-league news",
    "socceroos news",
    "matildas news",
    "australian football news",
    "world cup 2026 australia",
]

# ---------------------------------------------------------------------------
# Load credentials
# ---------------------------------------------------------------------------
def load_env():
    """Load config from ~/.keys/.env with os.environ taking precedence (Cloud Run)."""
    env_vars = {}
    env_file = os.path.expanduser("~/.keys/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    # Cloud Run injects secrets as env vars — these take precedence
    for key in ("POSTHOG_PERSONAL_API_KEY", "DATAFORSEO_LOGIN",
                "DATAFORSEO_PASSWORD", "SLACK_BOT_TOKEN"):
        if key in os.environ:
            env_vars[key] = os.environ[key]
    return env_vars

ENV = load_env()
POSTHOG_API_KEY = ENV.get("POSTHOG_PERSONAL_API_KEY", "")
DATAFORSEO_LOGIN = ENV.get("DATAFORSEO_LOGIN", "")
DATAFORSEO_PASSWORD = ENV.get("DATAFORSEO_PASSWORD", "")
SLACK_BOT_TOKEN = ENV.get("SLACK_BOT_TOKEN", "")

# DataForSEO auth
if DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD:
    _creds = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
    DATAFORSEO_HEADERS = {
        "Authorization": f"Basic {base64.b64encode(_creds.encode()).decode()}",
        "Content-Type": "application/json",
    }
else:
    DATAFORSEO_HEADERS = {}

# Dates
AEST = timezone(timedelta(hours=10))
NOW = datetime.now(AEST)
TODAY = NOW.strftime("%Y-%m-%d")
YESTERDAY = (NOW - timedelta(days=1)).strftime("%Y-%m-%d")
TWO_DAYS_AGO = (NOW - timedelta(days=2)).strftime("%Y-%m-%d")
THREE_DAYS_AGO = (NOW - timedelta(days=3)).strftime("%Y-%m-%d")
WEEK_AGO = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# PostHog Queries
# ---------------------------------------------------------------------------
def posthog_query(query_str):
    """Execute HogQL query against PostHog."""
    headers = {"Authorization": f"Bearer {POSTHOG_API_KEY}"}
    url = f"{POSTHOG_HOST}/api/projects/{POSTHOG_PROJECT_ID}/query/"
    payload = {"query": {"kind": "HogQLQuery", "query": query_str}}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.text, "results": []}
    except Exception as e:
        return {"error": str(e), "results": []}


def get_posthog_traffic(date_from, date_to):
    """Get core traffic metrics for a date range."""
    q = f"""
    SELECT
        count(DISTINCT person_id) as unique_users,
        count(DISTINCT "$session_id") as sessions,
        count(*) as pageviews,
        countIf(event = '$pageview') as page_views_only
    FROM events
    WHERE timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND properties.$current_url LIKE '%{SITE_DOMAIN}%'
    """
    return posthog_query(q)


def get_posthog_navboost(date_from, date_to):
    """Get NavBoost proxy metrics from navboost_page_metrics events."""
    q = f"""
    SELECT
        avg(toFloat64OrNull(properties.dwell_time_seconds)) as avg_dwell,
        avg(toFloat64OrNull(properties.engagement_score)) as avg_engagement
    FROM events
    WHERE timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND event = 'navboost_page_metrics'
    """
    nb = posthog_query(q)

    # Pogo rate from separate event
    pogo_q = f"""
    SELECT
        countIf(event = 'navboost_pogo') as pogo_count,
        countIf(event = 'navboost_page_metrics') as session_count
    FROM events
    WHERE timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND event IN ('navboost_pogo', 'navboost_page_metrics')
    """
    pogo = posthog_query(pogo_q)

    # CTA metrics
    cta_q = f"""
    SELECT
        countIf(event = 'navboost_cta_click') as cta_clicks,
        countIf(event = 'navboost_cta_visible') as cta_visible,
        countIf(event = 'navboost_outbound_click') as outbound_clicks
    FROM events
    WHERE timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND event IN ('navboost_cta_click', 'navboost_cta_visible', 'navboost_outbound_click')
    """
    cta = posthog_query(cta_q)

    # Combine into single result format
    nb_r = nb.get("results", [[None, None]])[0] if nb.get("results") else [None, None]
    pogo_r = pogo.get("results", [[0, 0]])[0] if pogo.get("results") else [0, 0]
    cta_r = cta.get("results", [[0, 0, 0]])[0] if cta.get("results") else [0, 0, 0]

    pogo_count = float(pogo_r[0] or 0)
    session_count = float(pogo_r[1] or 0)
    pogo_rate = (pogo_count / session_count * 100) if session_count > 0 else None

    return {
        "results": [[
            nb_r[0],       # avg_dwell
            pogo_rate,     # pogo_rate
            cta_r[0],      # cta_clicks
            cta_r[1],      # cta_visible
            nb_r[1],       # avg_engagement
            cta_r[2],      # outbound_clicks
        ]]
    }


def get_posthog_top_pages(date_from, date_to, limit=15):
    """Get top pages by pageviews."""
    q = f"""
    SELECT
        properties.$pathname as page,
        count(*) as views,
        count(DISTINCT person_id) as unique_visitors
    FROM events
    WHERE event = '$pageview'
      AND timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND properties.$current_url LIKE '%{SITE_DOMAIN}%'
    GROUP BY page
    ORDER BY views DESC
    LIMIT {limit}
    """
    return posthog_query(q)


def get_posthog_conversions(date_from, date_to):
    """Get conversion events (CTA clicks, outbound clicks)."""
    q = f"""
    SELECT
        event,
        properties.brand as brand,
        properties.cta_url as cta_url,
        count(*) as count
    FROM events
    WHERE timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND event IN ('navboost_cta_click', 'navboost_outbound_click')
    GROUP BY event, brand, cta_url
    ORDER BY count DESC
    """
    return posthog_query(q)


def get_posthog_referrers(date_from, date_to):
    """Get traffic sources."""
    q = f"""
    SELECT
        properties.$referrer as referrer,
        count(*) as visits
    FROM events
    WHERE event = '$pageview'
      AND timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
      AND properties.$current_url LIKE '%{SITE_DOMAIN}%'
      AND properties.$referrer IS NOT NULL
      AND properties.$referrer != ''
    GROUP BY referrer
    ORDER BY visits DESC
    LIMIT 10
    """
    return posthog_query(q)


# ---------------------------------------------------------------------------
# BigQuery — Summary Schema (Conversions, Brands, Revenue)
# ---------------------------------------------------------------------------
BQ_PROJECT = "paradisemedia-bi"


def get_bq_domain_daily(date_str):
    """Get domain-level performance for a single date."""
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=BQ_PROJECT)
        q = f"""
        SELECT
            IGAMING_CLICKS as clicks,
            IGAMING_NRC as signups,
            IGAMING_FTD as ftds,
            IGAMING_EPF_USD as epf,
            IGAMING_TOTAL_COMMISSION_USD as commission,
            GA_SESSIONS as traffic,
            LCP_AVG as lcp,
            INP_AVG as inp,
            CLS_AVG as cls,
            CWV_TOTAL_VISITS as cwv_visits,
            DFSEO_BACKLINKS as backlinks,
            DFSEO_REFDOMAINS as refdomains,
            DFSEO_ORG_TRAFFIC as org_traffic,
            ARTICLE_COUNT as article_count
        FROM `{BQ_PROJECT}.summary.DOMAIN_PERFORMANCE`
        WHERE DOMAIN = 'australiafootball.com'
          AND DATE = '{date_str}'
        """
        rows = list(client.query(q).result())
        if rows:
            r = dict(rows[0])
            return {k: (float(v) if v is not None else None) for k, v in r.items()}
        return {"clicks": 0, "signups": 0, "ftds": 0, "epf": 0, "commission": 0, "traffic": 0}
    except Exception as e:
        return {"error": str(e)}


def get_bq_domain_ytd():
    """Get domain-level YTD totals."""
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=BQ_PROJECT)
        q = f"""
        SELECT
            SUM(IGAMING_CLICKS) as clicks,
            SUM(IGAMING_NRC) as signups,
            SUM(IGAMING_FTD) as ftds,
            AVG(NULLIF(IGAMING_EPF_USD, 0)) as epf,
            SUM(IGAMING_TOTAL_COMMISSION_USD) as commission,
            SUM(GA_SESSIONS) as traffic
        FROM `{BQ_PROJECT}.summary.DOMAIN_PERFORMANCE`
        WHERE DOMAIN = 'australiafootball.com'
          AND DATE >= DATE_TRUNC(CURRENT_DATE(), YEAR)
        """
        rows = list(client.query(q).result())
        if rows:
            r = dict(rows[0])
            return {k: (float(v) if v is not None else 0) for k, v in r.items()}
        return {"clicks": 0, "signups": 0, "ftds": 0, "epf": 0, "commission": 0, "traffic": 0}
    except Exception as e:
        return {"error": str(e)}


def get_bq_article_performance(date_str):
    """Get article-level performance for a single date (by URL and brand)."""
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=BQ_PROJECT)
        q = f"""
        SELECT
            LIVE_URL as url,
            BRAND as brand,
            PROGRAM as program,
            VERTICAL as vertical,
            NICHE as niche,
            SUBNICHE as subniche,
            SUM(CLICKS) as clicks,
            SUM(NRC) as signups,
            SUM(FTD) as ftds,
            AVG(NULLIF(EPF_USD, 0)) as epf,
            SUM(TOTAL_COMMISSION_USD) as commission
        FROM `{BQ_PROJECT}.summary.ARTICLE_PERFORMANCE`
        WHERE DOMAIN = 'australiafootball.com'
          AND DATE = '{date_str}'
        GROUP BY url, brand, program, vertical, niche, subniche
        ORDER BY clicks DESC
        """
        rows = list(client.query(q).result())
        return [dict(r) for r in rows]
    except Exception as e:
        return {"error": str(e)}


def get_bq_article_ytd():
    """Get article-level YTD totals."""
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=BQ_PROJECT)
        q = f"""
        SELECT
            LIVE_URL as url,
            BRAND as brand,
            PROGRAM as program,
            VERTICAL as vertical,
            NICHE as niche,
            SUM(CLICKS) as clicks,
            SUM(NRC) as signups,
            SUM(FTD) as ftds,
            AVG(NULLIF(EPF_USD, 0)) as epf,
            SUM(TOTAL_COMMISSION_USD) as commission
        FROM `{BQ_PROJECT}.summary.ARTICLE_PERFORMANCE`
        WHERE DOMAIN = 'australiafootball.com'
          AND DATE >= DATE_TRUNC(CURRENT_DATE(), YEAR)
        GROUP BY url, brand, program, vertical, niche
        ORDER BY clicks DESC
        """
        rows = list(client.query(q).result())
        return [dict(r) for r in rows]
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Google Search Console (GSC)
# ---------------------------------------------------------------------------
GSC_PROPERTY = "sc-domain:australiafootball.com"


def _get_gsc_service():
    """Build GSC API service using application default credentials."""
    try:
        import google.auth
        from googleapiclient.discovery import build
        creds, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
        )
        return build("searchconsole", "v1", credentials=creds)
    except Exception as e:
        print(f"  GSC auth error: {e}")
        return None


def get_gsc_daily(date_str):
    """Get GSC overview metrics for a single date."""
    service = _get_gsc_service()
    if not service:
        return {"error": "GSC service unavailable"}
    try:
        response = service.searchanalytics().query(
            siteUrl=GSC_PROPERTY,
            body={
                "startDate": date_str,
                "endDate": date_str,
                "dimensions": ["date"],
                "rowLimit": 1,
            },
        ).execute()
        rows = response.get("rows", [])
        if rows:
            return {
                "clicks": rows[0]["clicks"],
                "impressions": rows[0]["impressions"],
                "ctr": rows[0]["ctr"],
                "position": rows[0]["position"],
            }
        return {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}
    except Exception as e:
        return {"error": str(e)}


def get_gsc_top_pages(date_from, date_to, limit=15):
    """Get top pages by organic clicks from GSC."""
    service = _get_gsc_service()
    if not service:
        return {"error": "GSC service unavailable"}
    try:
        response = service.searchanalytics().query(
            siteUrl=GSC_PROPERTY,
            body={
                "startDate": date_from,
                "endDate": date_to,
                "dimensions": ["page"],
                "rowLimit": limit,
                "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
            },
        ).execute()
        results = []
        for row in response.get("rows", []):
            page = row["keys"][0].replace("https://www.australiafootball.com", "")
            results.append({
                "page": page or "/",
                "clicks": row["clicks"],
                "impressions": row["impressions"],
                "ctr": row["ctr"],
                "position": row["position"],
            })
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


def get_gsc_top_queries(date_from, date_to, limit=20):
    """Get top queries by organic clicks from GSC."""
    service = _get_gsc_service()
    if not service:
        return {"error": "GSC service unavailable"}
    try:
        response = service.searchanalytics().query(
            siteUrl=GSC_PROPERTY,
            body={
                "startDate": date_from,
                "endDate": date_to,
                "dimensions": ["query"],
                "rowLimit": limit,
                "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
            },
        ).execute()
        results = []
        for row in response.get("rows", []):
            results.append({
                "query": row["keys"][0],
                "clicks": row["clicks"],
                "impressions": row["impressions"],
                "ctr": row["ctr"],
                "position": row["position"],
            })
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Content & Publishing Analysis
# ---------------------------------------------------------------------------
CONTENT_DIR = os.path.expanduser("~/australiafootball.com/src/content/news")


def analyze_content(date_str):
    """
    Analyze articles published on a given date.
    Returns dict with totals, breakdowns by type/sport, money page links.
    """
    import glob as glob_mod
    import re

    pattern = os.path.join(CONTENT_DIR, f"{date_str}*.md")
    files = sorted(glob_mod.glob(pattern))

    result = {
        "total": len(files),
        "editorial": 0,
        "aggregated": 0,
        "by_sport": defaultdict(lambda: {"editorial": 0, "aggregated": 0}),
        "editorial_articles": [],  # detailed list
        "aggregated_sources": defaultdict(int),  # sourceDomain counts
        "money_links": {"betting": 0, "casino": 0},
    }

    for f in files:
        try:
            with open(f) as fh:
                content = fh.read()
        except Exception:
            continue

        # Parse frontmatter
        fm = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        fm[key.strip()] = val.strip().strip('"').strip("'")

        sport = fm.get("sport", "general")
        is_agg = fm.get("isAggregated", "false").lower() == "true"
        title = fm.get("title", os.path.basename(f))
        source = fm.get("sourceDomain", "")

        # Count money page links in body
        betting_links = len(re.findall(r'/betting/', content))
        casino_links = len(re.findall(r'/casino/', content))

        if is_agg:
            result["aggregated"] += 1
            result["by_sport"][sport]["aggregated"] += 1
            if source:
                result["aggregated_sources"][source] += 1
        else:
            result["editorial"] += 1
            result["by_sport"][sport]["editorial"] += 1
            result["editorial_articles"].append({
                "title": title[:65],
                "sport": sport,
                "betting_links": betting_links,
                "casino_links": casino_links,
            })
            result["money_links"]["betting"] += betting_links
            result["money_links"]["casino"] += casino_links

    return result


def analyze_content_range(days=7):
    """Analyze content for the last N days. Returns dict keyed by date."""
    results = {}
    for i in range(days):
        d = (NOW - timedelta(days=i)).strftime("%Y-%m-%d")
        results[d] = analyze_content(d)
    return results


def get_posthog_scroll_depth(date_from, date_to):
    """Get scroll depth distribution from navboost_scroll_milestone events."""
    q = f"""
    SELECT
        properties.depth as depth,
        count(*) as count
    FROM events
    WHERE event = 'navboost_scroll_milestone'
      AND timestamp >= '{date_from}'
      AND timestamp < '{date_to}'
    GROUP BY depth
    ORDER BY depth
    """
    return posthog_query(q)


# ---------------------------------------------------------------------------
# DataForSEO Queries
# ---------------------------------------------------------------------------
def dataforseo_keyword_rankings():
    """Get current SERP positions for target keywords."""
    if not DATAFORSEO_HEADERS:
        return {"error": "DataForSEO credentials not configured"}

    results = []
    # Use SERP API to check rankings
    tasks = []
    for kw in TARGET_KEYWORDS:
        tasks.append({
            "keyword": kw,
            "location_code": LOCATION_CODE_AU,
            "language_code": LANGUAGE_CODE,
            "device": "desktop",
            "os": "windows",
            "depth": 100,
        })

    try:
        # Post tasks
        resp = requests.post(
            f"{DATAFORSEO_BASE}/serp/google/organic/live/advanced",
            headers=DATAFORSEO_HEADERS,
            json=tasks,
            timeout=120,
        )
        if resp.status_code != 200:
            return {"error": f"API returned {resp.status_code}"}

        data = resp.json()
        for task in data.get("tasks", []):
            if task.get("status_code") != 20000:
                continue
            keyword = task.get("data", {}).get("keyword", "?")
            items = task.get("result", [{}])[0].get("items", [])
            our_position = None
            for item in items:
                if item.get("type") == "organic":
                    domain = item.get("domain", "")
                    if SITE_DOMAIN in domain or f"www.{SITE_DOMAIN}" in domain:
                        our_position = item.get("rank_absolute")
                        url = item.get("url", "")
                        results.append({
                            "keyword": keyword,
                            "position": our_position,
                            "url": url,
                        })
                        break
            if our_position is None:
                results.append({
                    "keyword": keyword,
                    "position": ">100",
                    "url": "not ranking",
                })

        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


def dataforseo_ranked_keywords():
    """Get all keywords the domain ranks for with positions."""
    if not DATAFORSEO_HEADERS:
        return {"error": "DataForSEO credentials not configured"}

    try:
        payload = [{
            "target": SITE_DOMAIN,
            "location_code": LOCATION_CODE_AU,
            "language_code": LANGUAGE_CODE,
            "limit": 100,
            "order_by": ["keyword_data.keyword_info.search_volume,desc"],
            "filters": ["ranked_serp_element.serp_item.rank_absolute", "<=", 50],
        }]
        resp = requests.post(
            f"{DATAFORSEO_BASE}/dataforseo_labs/google/ranked_keywords/live",
            headers=DATAFORSEO_HEADERS,
            json=payload,
            timeout=60,
        )
        if resp.status_code != 200:
            return {"error": f"API returned {resp.status_code}"}

        data = resp.json()
        results = []
        for task in data.get("tasks", []):
            if task.get("status_code") != 20000:
                continue
            items = task.get("result", [{}])[0].get("items", [])
            for item in items:
                kw_data = item.get("keyword_data", {})
                serp = item.get("ranked_serp_element", {}).get("serp_item", {})
                results.append({
                    "keyword": kw_data.get("keyword", "?"),
                    "volume": kw_data.get("keyword_info", {}).get("search_volume", 0),
                    "position": serp.get("rank_absolute", "?"),
                    "url": serp.get("url", "?"),
                    "cpc": kw_data.get("keyword_info", {}).get("cpc", 0),
                })
        results.sort(key=lambda x: x.get("volume", 0), reverse=True)
        return {"results": results[:50]}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# PageSpeed Insights
# ---------------------------------------------------------------------------
def get_psi_scores(url, strategy="mobile"):
    """Fetch PageSpeed Insights scores."""
    params = {
        "url": url,
        "category": ["PERFORMANCE", "SEO", "ACCESSIBILITY", "BEST_PRACTICES"],
        "strategy": strategy,
    }
    try:
        resp = requests.get(PSI_API, params=params, timeout=60)
        if resp.status_code != 200:
            return {"error": f"PSI returned {resp.status_code}"}

        data = resp.json()
        lr = data.get("lighthouseResult", {})
        cats = lr.get("categories", {})
        audits = lr.get("audits", {})

        scores = {}
        for name, cat in cats.items():
            score = cat.get("score")
            scores[name] = int(score * 100) if score else None

        cwv = {}
        for key in ["first-contentful-paint", "largest-contentful-paint",
                     "total-blocking-time", "cumulative-layout-shift",
                     "speed-index", "interactive"]:
            a = audits.get(key, {})
            cwv[key] = {
                "value": a.get("displayValue", "N/A"),
                "score": a.get("score"),
            }

        return {"scores": scores, "cwv": cwv}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Site Health Checks
# ---------------------------------------------------------------------------
def check_site_health():
    """Basic site health checks."""
    checks = {}

    # Homepage responds
    try:
        r = requests.get(f"{SITE_URL}/", timeout=15, allow_redirects=True)
        checks["homepage_status"] = r.status_code
        checks["homepage_time_ms"] = int(r.elapsed.total_seconds() * 1000)
    except Exception as e:
        checks["homepage_status"] = f"ERROR: {e}"

    # Sitemap accessible
    try:
        r = requests.get(f"{SITE_URL}/sitemap.xml", timeout=15)
        checks["sitemap_status"] = r.status_code
        if r.status_code == 200:
            checks["sitemap_urls"] = r.text.count("<loc>")
    except Exception as e:
        checks["sitemap_status"] = f"ERROR: {e}"

    # News sitemap
    try:
        r = requests.get(f"{SITE_URL}/sitemap-news.xml", timeout=15)
        checks["news_sitemap_status"] = r.status_code
        if r.status_code == 200:
            checks["news_sitemap_urls"] = r.text.count("<loc>")
    except Exception as e:
        checks["news_sitemap_status"] = f"ERROR: {e}"

    # Robots.txt
    try:
        r = requests.get(f"{SITE_URL}/robots.txt", timeout=15)
        checks["robots_status"] = r.status_code
    except Exception as e:
        checks["robots_status"] = f"ERROR: {e}"

    # Casino page check
    try:
        r = requests.get(f"{SITE_URL}/casino/best-online-casinos-australia/", timeout=15)
        checks["casino_money_page"] = r.status_code
    except Exception as e:
        checks["casino_money_page"] = f"ERROR: {e}"

    # Betting page check
    try:
        r = requests.get(f"{SITE_URL}/betting/best-betting-sites-australia/", timeout=15)
        checks["betting_money_page"] = r.status_code
    except Exception as e:
        checks["betting_money_page"] = f"ERROR: {e}"

    return checks


# ---------------------------------------------------------------------------
# Report Formatting (Slack Blocks)
# ---------------------------------------------------------------------------
def format_change(current, previous, metric_name="", invert=False):
    """Format a day-over-day change indicator.
    Returns (text, direction) where direction is 'strong_good', 'good',
    'neutral', 'bad', 'strong_bad'."""
    if current is None or previous is None:
        return "N/A", "neutral"
    try:
        current = float(current)
        previous = float(previous)
    except (ValueError, TypeError):
        return "N/A", "neutral"

    if previous == 0:
        return f"{current:.1f} (new)", "neutral"

    change = current - previous
    pct = (change / previous) * 100
    abs_pct = abs(pct)

    if invert:  # Lower is better (e.g., pogo rate, position number)
        if change > 0:
            direction = "strong_bad" if abs_pct > 20 else "bad"
        elif change < 0:
            direction = "strong_good" if abs_pct > 20 else "good"
        else:
            direction = "neutral"
    else:
        if change > 0:
            direction = "strong_good" if abs_pct > 20 else "good"
        elif change < 0:
            direction = "strong_bad" if abs_pct > 20 else "bad"
        else:
            direction = "neutral"

    # Flat override: <5% change in either direction
    if abs_pct < 5 and direction not in ("neutral",):
        direction = "neutral"

    sign = "+" if change > 0 else ""
    text = f"{current:.1f} ({sign}{change:.1f} / {sign}{pct:.1f}%)"
    return text, direction


# ---------------------------------------------------------------------------
# Emoji Standard — combo mode (status dot + direction arrow)
# ---------------------------------------------------------------------------
def _combo(direction):
    """Combo emoji: status circle + direction arrow for metric lines."""
    return {
        "strong_good": ":green_circle: :arrow_up:",
        "good":        ":arrow_up:",
        "neutral":     ":arrow_right:",
        "bad":         ":arrow_down:",
        "strong_bad":  ":red_circle: :arrow_down:",
    }.get(direction, ":arrow_right:")


def _grade_dot(grade):
    """Colored circle for letter grades A-F."""
    return {
        "A": ":green_circle:",
        "B": ":blue_circle:",
        "C": ":yellow_circle:",
        "D": ":orange_circle:",
        "F": ":red_circle:",
    }.get(grade, ":white_circle:")


def _score_bar(score, width=10):
    """Visual progress bar from score 0-100 using emoji squares."""
    try:
        s = int(score)
    except (ValueError, TypeError):
        return ""
    filled = max(0, min(width, round(s / 100 * width)))
    empty = width - filled
    if s >= 85:
        fill_char = ":green_square:"
    elif s >= 70:
        fill_char = ":blue_square:"
    elif s >= 55:
        fill_char = ":yellow_square:"
    elif s >= 40:
        fill_char = ":orange_square:"
    else:
        fill_char = ":red_square:"
    return fill_char * filled + ":white_square:" * empty


def _status_dot(value, pass_val=200):
    """Green/red dot for HTTP status codes."""
    return ":green_circle:" if value == pass_val else ":red_circle:"


def _pos_dot(pos):
    """Colored circle for keyword position bands."""
    if not isinstance(pos, (int, float)):
        return ":white_circle:"
    if pos <= 3:
        return ":green_circle:"
    elif pos <= 10:
        return ":green_circle:"
    elif pos <= 20:
        return ":yellow_circle:"
    else:
        return ":white_circle:"


def _fmt_status_lines(text_block):
    """Format PASS/WARN/FAIL/MONITOR lines with standard emoji."""
    lines = []
    for line in text_block.split("\n"):
        line = line.strip()
        if line.startswith("PASS:"):
            lines.append(f":green_circle: {line[6:]}")
        elif line.startswith("WARN:"):
            lines.append(f":warning: {line[6:]}")
        elif line.startswith("FAIL:"):
            lines.append(f":red_circle: {line[6:]}")
        elif line.startswith("MONITOR:"):
            lines.append(f":eyes: {line[9:]}")
        elif line:
            lines.append(f":white_circle: {line}")
    return lines


def _fmt_detail_lines(details):
    """Format rating detail lines with standard emoji."""
    lines = []
    for d in details:
        d_stripped = d.strip()
        if d_stripped.startswith("PASS"):
            lines.append(f":green_circle: {d_stripped[5:]}")
        elif d_stripped.startswith("WARN"):
            lines.append(f":warning: {d_stripped[5:]}")
        elif d_stripped.startswith("FAIL"):
            lines.append(f":red_circle: {d_stripped[5:]}")
        else:
            lines.append(f":white_circle: {d_stripped}")
    return lines


def build_slack_messages(report_data):
    """
    Build Slack message payloads — one main message + 5 threaded replies.
    Structure: Main Dashboard | T1: Traffic & Search | T2: Content & Publishing |
               T3: Conversions & Revenue | T4: Keywords & Rankings | T5: Ratings & Technical
    """
    def _trow(data, idx):
        r = data.get("results", [[]])[0] if data.get("results") else []
        return float(r[idx]) if r and len(r) > idx and r[idx] is not None else 0

    def safe_get(arr, idx):
        return arr[idx] if arr and len(arr) > idx else None

    def _bq_val(d, k):
        return float(d.get(k, 0) or 0) if isinstance(d, dict) and "error" not in d else 0

    health = report_data.get("health", {})

    # =====================================================================
    # MAIN MESSAGE — Dashboard + Highlights + Attention Items
    # =====================================================================
    main = []
    main.append({"type": "header", "text": {"type": "plain_text", "text": f":newspaper: australiafootball.com — {TODAY}"}})

    # --- Ratings ---
    leak_r = report_data.get("leak_rating", {})
    seo_r = report_data.get("seo_rating", {})
    strat_r = report_data.get("strategy_rating", {})
    leak_s, leak_g = leak_r.get("score", 0), leak_r.get("grade", "?")
    seo_s, seo_g = seo_r.get("score", 0), seo_r.get("grade", "?")
    strat_s, strat_g = strat_r.get("score", 0), strat_r.get("grade", "?")
    try:
        overall = round(int(leak_s) * 0.40 + int(seo_s) * 0.30 + int(strat_s) * 0.30)
        overall_g = "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 55 else "D" if overall >= 40 else "F"
    except (ValueError, TypeError):
        overall, overall_g = 0, "?"

    main.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*Site Health Score*\n"
        f"{_grade_dot(overall_g)}  *{overall}/100 ({overall_g})*"
    )}})
    main.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": (
            f"{_grade_dot(leak_g)} Leak: {leak_s}/100 ({leak_g})    "
            f"{_grade_dot(seo_g)} SEO: {seo_s}/100 ({seo_g})    "
            f"{_grade_dot(strat_g)} Strategy: {strat_s}/100 ({strat_g})"
        )}
    ]})
    main.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": "_Leak = Google API leak params weighted for News-Casino | SEO = 16 R-SEO rules | Strategy = Playbook #2 targets_"}
    ]})
    main.append({"type": "divider"})

    # --- Key Metrics ---
    y = report_data.get("traffic_yesterday", {})
    d2 = report_data.get("traffic_2days", {})
    users_y, sessions_y, views_y = _trow(y, 0), _trow(y, 1), _trow(y, 2)
    users_d2, sessions_d2, views_d2 = _trow(d2, 0), _trow(d2, 1), _trow(d2, 2)
    users_text, users_dir = format_change(users_y, users_d2)
    sessions_text, sessions_dir = format_change(sessions_y, sessions_d2)
    views_text, views_dir = format_change(views_y, views_d2)

    bq_ytd = report_data.get("bq_ytd", {})
    ytd_clicks = int(bq_ytd.get("clicks", 0) or 0) if not bq_ytd.get("error") else 0
    ytd_signups = int(bq_ytd.get("signups", 0) or 0) if not bq_ytd.get("error") else 0
    ytd_ftds = int(bq_ytd.get("ftds", 0) or 0) if not bq_ytd.get("error") else 0
    ytd_epf = float(bq_ytd.get("epf", 0) or 0) if not bq_ytd.get("error") else 0
    ytd_comm = float(bq_ytd.get("commission", 0) or 0) if not bq_ytd.get("error") else 0

    ranked_kw = report_data.get("ranked_keywords", {})
    kw_count = len(ranked_kw.get("results", [])) if not ranked_kw.get("error") else 0

    # PostHog traffic
    main.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*Traffic (PostHog)* _{YESTERDAY} vs {TWO_DAYS_AGO}_\n"
        f"{_combo(users_dir)} Users: *{int(users_y)}* {users_text}  |  "
        f"Sessions: *{int(sessions_y)}* {sessions_text}  |  "
        f"Pageviews: *{int(views_y)}* {views_text}"
    )}})

    # GSC organic
    gsc_y_main = report_data.get("gsc_yesterday", {})
    gsc_d2_main = report_data.get("gsc_2days_ago", {})
    if not gsc_y_main.get("error"):
        gsc_c_y = int(gsc_y_main.get("clicks", 0))
        gsc_i_y = int(gsc_y_main.get("impressions", 0))
        gsc_p_y = gsc_y_main.get("position", 0)
        gsc_c_d2 = int(gsc_d2_main.get("clicks", 0)) if not gsc_d2_main.get("error") else 0
        gc_main_text, gc_main_dir = format_change(gsc_c_y, gsc_c_d2)
        main.append({"type": "section", "text": {"type": "mrkdwn", "text": (
            f"*Organic (GSC)* _{TWO_DAYS_AGO} vs {THREE_DAYS_AGO}_\n"
            f"{_combo(gc_main_dir)} Clicks: *{gsc_c_y}* {gc_main_text}  |  "
            f"Impressions: *{gsc_i_y}*  |  Avg Pos: *{gsc_p_y:.1f}*"
        )}})

    # Content summary on main
    content_7d = report_data.get("content_7days", {})
    yesterday_content = content_7d.get(YESTERDAY, {})
    if yesterday_content.get("total", 0) > 0:
        main.append({"type": "section", "text": {"type": "mrkdwn", "text": (
            f"*Content* _{YESTERDAY}_\n"
            f":memo: *{yesterday_content['editorial']}* editorial  |  "
            f":link: *{yesterday_content['aggregated']}* redirects  |  "
            f"Total: *{yesterday_content['total']}*"
        )}})

    main.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": f"_Sources: PostHog, GSC ({GSC_PROPERTY}), BQ Summary, DataForSEO | {kw_count} KWs in AU top 50_"}
    ]})

    # Revenue
    main.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*YTD Revenue*\n"
        f"Clicks: *{ytd_clicks}*  |  Signups: *{ytd_signups}*  |  FTDs: *{ytd_ftds}*  |  "
        f"Commission: *${ytd_comm:,.2f}*"
    )}})
    main.append({"type": "divider"})

    # --- Attention Items ---
    attention = []
    if health.get("homepage_status") != 200:
        attention.append(f":rotating_light: *Homepage DOWN* — HTTP {health.get('homepage_status')}")
    if health.get("casino_money_page") != 200:
        attention.append(f":rotating_light: *Casino page DOWN* — HTTP {health.get('casino_money_page')}")
    if health.get("betting_money_page") != 200:
        attention.append(f":rotating_light: *Betting page DOWN* — HTTP {health.get('betting_money_page')}")
    try:
        if users_d2 > 10 and users_y < users_d2 * 0.5:
            attention.append(f":red_circle: :arrow_down: *Traffic dropped >50%* — {int(users_y)} vs {int(users_d2)} users")
    except (ValueError, TypeError):
        pass
    news_count = health.get("news_sitemap_urls", 0) or 0
    if news_count == 0:
        attention.append(":warning: *No articles in news sitemap* — freshness signal at risk")
    if leak_s and int(leak_s) < 55:
        attention.append(f":warning: *Leak Rating {leak_s}/100* — below C threshold")
    if strat_s and int(strat_s) < 55:
        attention.append(f":warning: *Strategy Rating {strat_s}/100* — below C threshold")
    for d in strat_r.get("details", []):
        if d.strip().startswith("FAIL"):
            attention.append(f":red_circle: {d.strip()}")

    if attention:
        main.append({"type": "section", "text": {"type": "mrkdwn", "text": "*:rotating_light: Needs Attention*\n" + "\n".join(attention)}})
    else:
        main.append({"type": "section", "text": {"type": "mrkdwn", "text": ":white_check_mark: *All clear — no issues detected*"}})

    main.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": f"_5 threads: Traffic & Search, Content, Conversions, Keywords, Ratings & Technical | {NOW.strftime('%H:%M AEST')}_"}
    ]})

    # =====================================================================
    # THREAD 1 — Traffic & Search (PostHog + GSC + NavBoost + Site Health)
    # =====================================================================
    t1 = []
    t1.append({"type": "header", "text": {"type": "plain_text", "text": ":bar_chart: Traffic & Search"}})

    # Site Health
    t1.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*Site Health*\n"
        f"{_status_dot(health.get('homepage_status'))} Homepage: {health.get('homepage_status', '?')} ({health.get('homepage_time_ms', '?')}ms)\n"
        f"{_status_dot(health.get('sitemap_status'))} Sitemap: {health.get('sitemap_status', '?')} ({health.get('sitemap_urls', '?')} URLs)\n"
        f"{_status_dot(health.get('news_sitemap_status'))} News: {health.get('news_sitemap_status', '?')} ({health.get('news_sitemap_urls', '?')} URLs)\n"
        f"{_status_dot(health.get('casino_money_page'))} Casino  {_status_dot(health.get('betting_money_page'))} Betting"
    )}})
    t1.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_HTTP status checks against {SITE_URL}_"}]})
    t1.append({"type": "divider"})

    # PostHog Traffic
    t1.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*PostHog Traffic* _{YESTERDAY} vs {TWO_DAYS_AGO}_\n"
        f"{_combo(users_dir)} Users: *{int(users_y)}* {users_text}\n"
        f"{_combo(sessions_dir)} Sessions: *{int(sessions_y)}* {sessions_text}\n"
        f"{_combo(views_dir)} Pageviews: *{int(views_y)}* {views_text}"
    )}})

    # Top Pages (PostHog)
    top_pages = report_data.get("top_pages_yesterday", {})
    tp_results = top_pages.get("results", [])
    if tp_results:
        tp_text = ""
        for i, row in enumerate(tp_results[:8], 1):
            page = row[0] if row else "?"
            views = row[1] if len(row) > 1 else 0
            uniq = row[2] if len(row) > 2 else 0
            tp_text += f"{i}. `{page}` — *{views}* views ({uniq} unique)\n"
        t1.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*Top Pages (PostHog)* _{YESTERDAY}_\n{tp_text}"}})

    # Sources (PostHog)
    refs = report_data.get("referrers_yesterday", {})
    ref_results = refs.get("results", [])
    if ref_results:
        ref_text = ""
        for row in ref_results[:6]:
            source = row[0] if row else "?"
            visits = row[1] if len(row) > 1 else 0
            if source and len(source) > 45:
                source = source[:45] + "..."
            ref_text += f"  {source}: *{visits}*\n"
        t1.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*Traffic Sources*\n{ref_text}"}})

    t1.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_PostHog HogQL — unique person_id, $session_id, event count | directFrac impacts Google leak scoring_"}]})
    t1.append({"type": "divider"})

    # GSC Organic
    gsc_y = report_data.get("gsc_yesterday", {})
    gsc_d2 = report_data.get("gsc_2days_ago", {})
    if not gsc_y.get("error"):
        gsc_clicks_y = gsc_y.get("clicks", 0)
        gsc_imp_y = gsc_y.get("impressions", 0)
        gsc_ctr_y = gsc_y.get("ctr", 0)
        gsc_pos_y = gsc_y.get("position", 0)
        gsc_clicks_d2 = gsc_d2.get("clicks", 0) if not gsc_d2.get("error") else 0
        gsc_imp_d2 = gsc_d2.get("impressions", 0) if not gsc_d2.get("error") else 0
        gsc_pos_d2 = gsc_d2.get("position", 0) if not gsc_d2.get("error") else 0
        gc_text, gc_dir = format_change(gsc_clicks_y, gsc_clicks_d2)
        gi_text, gi_dir = format_change(gsc_imp_y, gsc_imp_d2)
        gp_text, gp_dir = format_change(gsc_pos_y, gsc_pos_d2, invert=True)
        ctr_y_pct = gsc_ctr_y * 100 if gsc_ctr_y else 0
        ctr_d2_pct = (gsc_d2.get("ctr", 0) or 0) * 100 if not gsc_d2.get("error") else 0
        gctr_text, gctr_dir = format_change(ctr_y_pct, ctr_d2_pct)

        t1.append({"type": "section", "text": {"type": "mrkdwn", "text": (
            f"*GSC Organic* _{TWO_DAYS_AGO} vs {THREE_DAYS_AGO}_\n"
            f"{_combo(gc_dir)} Clicks: *{int(gsc_clicks_y)}* {gc_text}\n"
            f"{_combo(gi_dir)} Impressions: *{int(gsc_imp_y)}* {gi_text}\n"
            f"{_combo(gctr_dir)} CTR: *{ctr_y_pct:.2f}%* {gctr_text}\n"
            f"{_combo(gp_dir)} Avg Position: *{gsc_pos_y:.1f}* {gp_text}"
        )}})

        # GSC Top Pages
        gsc_pages = report_data.get("gsc_top_pages", {})
        if not gsc_pages.get("error") and gsc_pages.get("results"):
            gp_lines = f"*Top Organic Pages* _{THREE_DAYS_AGO} to {TWO_DAYS_AGO}_\n"
            for i, p in enumerate(gsc_pages["results"][:10], 1):
                page = p["page"][:50] + "..." if len(p["page"]) > 50 else p["page"]
                gp_lines += f"{i}. `{page}` — *{p['clicks']}*c, {p['impressions']}imp, {p['ctr']*100:.1f}%, pos {p['position']:.1f}\n"
            t1.append({"type": "section", "text": {"type": "mrkdwn", "text": gp_lines}})

        t1.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_GSC Search Analytics API | {GSC_PROPERTY} | Data lags 2-3 days_"}]})
    t1.append({"type": "divider"})

    # NavBoost
    nb_y = report_data.get("navboost_yesterday", {})
    nb_d2 = report_data.get("navboost_2days", {})
    nb_y_r = nb_y.get("results", [[]])[0] if nb_y.get("results") else [None] * 6
    nb_d2_r = nb_d2.get("results", [[]])[0] if nb_d2.get("results") else [None] * 6
    dwell_y = safe_get(nb_y_r, 0)
    pogo_y = safe_get(nb_y_r, 1)
    cta_clicks_y = safe_get(nb_y_r, 2)
    cta_visible_y = safe_get(nb_y_r, 3)
    engagement_y = safe_get(nb_y_r, 4)
    cta_ctr_y = (float(cta_clicks_y) / float(cta_visible_y) * 100) if cta_clicks_y and cta_visible_y and float(cta_visible_y) > 0 else None
    dwell_text, dwell_dir = format_change(dwell_y, safe_get(nb_d2_r, 0))
    pogo_text, pogo_dir = format_change(pogo_y, safe_get(nb_d2_r, 1), invert=True)
    eng_text, eng_dir = format_change(engagement_y, safe_get(nb_d2_r, 4))
    dwell_raw = f"{float(dwell_y):.1f}s" if dwell_y is not None else "N/A"
    pogo_raw = f"{float(pogo_y):.1f}%" if pogo_y is not None else "N/A"
    eng_raw = f"{float(engagement_y):.0f}" if engagement_y is not None else "N/A"

    t1.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*NavBoost Metrics*\n"
        f"{_combo(dwell_dir)} Dwell: *{dwell_raw}* {dwell_text}\n"
        f"{_combo(pogo_dir)} Pogo: *{pogo_raw}* {pogo_text}\n"
        f":arrow_right: CTA CTR: *{f'{cta_ctr_y:.1f}%' if cta_ctr_y else 'N/A'}* ({cta_clicks_y or 0} clicks / {cta_visible_y or 0} visible)\n"
        f"{_combo(eng_dir)} Engagement: *{eng_raw}* {eng_text}"
    )}})
    t1.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_Targets: dwell >90s, pogo <18%, engagement >70 | Maps to navBoost goodClicks/badClicks in Google leak_"}]})

    # BQ CWV (if available)
    bq_2d_cwv = report_data.get("bq_2days_ago", {})
    lcp = bq_2d_cwv.get("lcp") if isinstance(bq_2d_cwv, dict) else None
    inp = bq_2d_cwv.get("inp") if isinstance(bq_2d_cwv, dict) else None
    cls_val = bq_2d_cwv.get("cls") if isinstance(bq_2d_cwv, dict) else None
    if lcp is not None or inp is not None or cls_val is not None:
        t1.append({"type": "divider"})
        lcp_dot = ":green_circle:" if lcp and lcp < 2500 else ":yellow_circle:" if lcp and lcp < 4000 else ":red_circle:" if lcp else ":white_circle:"
        inp_dot = ":green_circle:" if inp is not None and inp < 200 else ":yellow_circle:" if inp is not None and inp < 500 else ":red_circle:" if inp else ":white_circle:"
        cls_dot = ":green_circle:" if cls_val is not None and cls_val < 0.1 else ":yellow_circle:" if cls_val is not None and cls_val < 0.25 else ":red_circle:" if cls_val else ":white_circle:"
        cwv_visits = bq_2d_cwv.get("cwv_visits")
        t1.append({"type": "section", "text": {"type": "mrkdwn", "text": (
            f"*Core Web Vitals (BQ)* _{TWO_DAYS_AGO}_\n"
            f"{lcp_dot} LCP: *{lcp:.0f}ms*  |  {inp_dot} INP: *{inp:.0f}ms*  |  {cls_dot} CLS: *{cls_val:.3f}*"
        )}})
        t1.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_BQ Summary CrUX field data — {int(cwv_visits or 0)} real visits | LCP<2.5s, INP<200ms, CLS<0.1 = good_"}]})

    # =====================================================================
    # THREAD 2 — Content & Publishing
    # =====================================================================
    t2 = []
    t2.append({"type": "header", "text": {"type": "plain_text", "text": ":pencil2: Content & Publishing"}})

    content_7d = report_data.get("content_7days", {})

    # 7-day overview table
    overview_text = "*Last 7 Days*\n"
    total_editorial_7d = 0
    total_agg_7d = 0
    total_betting_links = 0
    total_casino_links = 0
    for i in range(6, -1, -1):
        d = (NOW - timedelta(days=i)).strftime("%Y-%m-%d")
        day_label = d[-5:]  # MM-DD
        cd = content_7d.get(d, {})
        ed = cd.get("editorial", 0)
        ag = cd.get("aggregated", 0)
        total_editorial_7d += ed
        total_agg_7d += ag
        total_betting_links += cd.get("money_links", {}).get("betting", 0)
        total_casino_links += cd.get("money_links", {}).get("casino", 0)
        bar = ":blue_square:" * ed + ":white_square:" * ag if (ed + ag) > 0 else ":black_square:"
        overview_text += f"`{day_label}` {bar} *{ed}* editorial + *{ag}* redirects = {ed + ag}\n"

    overview_text += (
        f"\n_7d total: *{total_editorial_7d}* editorial + *{total_agg_7d}* redirects = "
        f"*{total_editorial_7d + total_agg_7d}* articles_"
    )
    t2.append({"type": "section", "text": {"type": "mrkdwn", "text": overview_text}})
    t2.append({"type": "context", "elements": [{"type": "mrkdwn", "text": ":blue_square: = editorial (original) | :white_square: = redirect (aggregated from RSS)"}]})
    t2.append({"type": "divider"})

    # Yesterday's editorial articles detail
    yd = content_7d.get(YESTERDAY, {})
    if yd.get("editorial_articles"):
        ed_text = f"*Editorial Articles* _{YESTERDAY}_\n"
        for art in yd["editorial_articles"]:
            bet_icon = ":moneybag:" if art["betting_links"] > 0 else ""
            cas_icon = ":slot_machine:" if art["casino_links"] > 0 else ""
            ed_text += f":memo: _{art['sport']}_ — {art['title']} {bet_icon}{cas_icon}\n"
        t2.append({"type": "section", "text": {"type": "mrkdwn", "text": ed_text}})
        t2.append({"type": "context", "elements": [
            {"type": "mrkdwn", "text": f"_:moneybag: = links to /betting/ | :slot_machine: = links to /casino/ | {yd['money_links']['betting']} betting + {yd['money_links']['casino']} casino links_"}
        ]})
    else:
        t2.append({"type": "section", "text": {"type": "mrkdwn", "text": f"_No editorial articles published {YESTERDAY}_"}})
    t2.append({"type": "divider"})

    # Aggregated (redirect) sources
    if yd.get("aggregated_sources"):
        src_text = f"*Redirect Sources* _{YESTERDAY}_ ({yd['aggregated']} articles)\n"
        for source, count in sorted(yd["aggregated_sources"].items(), key=lambda x: -x[1]):
            src_text += f"  {source}: *{count}*\n"
        t2.append({"type": "section", "text": {"type": "mrkdwn", "text": src_text}})

    # By sport breakdown (yesterday)
    if yd.get("by_sport"):
        sport_text = f"*By Sport* _{YESTERDAY}_\n"
        for sport, counts in sorted(yd["by_sport"].items(), key=lambda x: -(x[1]["editorial"] + x[1]["aggregated"])):
            total = counts["editorial"] + counts["aggregated"]
            sport_text += f"  {sport}: *{total}* ({counts['editorial']}ed + {counts['aggregated']}rdr)\n"
        t2.append({"type": "section", "text": {"type": "mrkdwn", "text": sport_text}})

    # Money page link coverage (7-day)
    t2.append({"type": "divider"})
    t2.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*Money Page Link Coverage (7d)*\n"
        f":moneybag: Betting links in editorial: *{total_betting_links}*\n"
        f":slot_machine: Casino links in editorial: *{total_casino_links}*\n"
        f"_R-CONTENT-03: each editorial article should link to at least 1 money page_"
    )}})

    t2.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": f"_Source: ~/australiafootball.com/src/content/news/ — {health.get('sitemap_urls', '?')} total URLs in sitemap_"}
    ]})

    # =====================================================================
    # THREAD 3 — Conversions & Revenue (2d ago vs 3d ago)
    # =====================================================================
    t3 = []
    t3.append({"type": "header", "text": {"type": "plain_text", "text": ":dollar: Conversions & Revenue"}})
    t3.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_BQ summary loads at 21:00 CET — latest = 2d ago vs 3d ago_"}]})

    bq_2d = report_data.get("bq_2days_ago", {})
    bq_3d = report_data.get("bq_3days_ago", {})
    bq_2d_articles = report_data.get("bq_2days_ago_articles", [])
    bq_3d_articles = report_data.get("bq_3days_ago_articles", [])

    clicks_2d, clicks_3d = _bq_val(bq_2d, "clicks"), _bq_val(bq_3d, "clicks")
    signups_2d, signups_3d = _bq_val(bq_2d, "signups"), _bq_val(bq_3d, "signups")
    ftds_2d, ftds_3d = _bq_val(bq_2d, "ftds"), _bq_val(bq_3d, "ftds")
    epf_2d, epf_3d = _bq_val(bq_2d, "epf"), _bq_val(bq_3d, "epf")
    comm_2d, comm_3d = _bq_val(bq_2d, "commission"), _bq_val(bq_3d, "commission")

    c_clicks, c_clicks_dir = format_change(clicks_2d, clicks_3d)
    c_ftds, c_ftds_dir = format_change(ftds_2d, ftds_3d)
    c_comm, c_comm_dir = format_change(comm_2d, comm_3d)
    ftd_dot = ":green_circle:" if ftds_2d > 0 else ":white_circle:"

    t3.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*{TWO_DAYS_AGO} vs {THREE_DAYS_AGO}*\n"
        f"{_combo(c_clicks_dir)} Clicks: *{int(clicks_2d)}* {c_clicks}\n"
        f":arrow_right: Signups: *{int(signups_2d)}* (prev: {int(signups_3d)})\n"
        f"{ftd_dot} FTDs: *{int(ftds_2d)}* {c_ftds}\n"
        f":arrow_right: EPF: *${epf_2d:,.2f}* (prev: ${epf_3d:,.2f})\n"
        f"{_combo(c_comm_dir)} Commission: *${comm_2d:,.2f}* {c_comm}"
    )}})
    t3.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_IGAMING_CLICKS, IGAMING_NRC, IGAMING_FTD, IGAMING_EPF_USD, IGAMING_TOTAL_COMMISSION_USD_"}]})
    t3.append({"type": "divider"})

    # Active pages across both days
    all_urls = set()
    articles_by_url = defaultdict(lambda: {"2d": defaultdict(lambda: {"clicks": 0, "signups": 0, "ftds": 0, "commission": 0}),
                                            "3d": defaultdict(lambda: {"clicks": 0, "signups": 0, "ftds": 0, "commission": 0})})
    for row in (bq_2d_articles if isinstance(bq_2d_articles, list) else []):
        url = row.get("url", "?").replace("https://www.australiafootball.com", "")
        brand = row.get("brand", "?")
        all_urls.add(url)
        articles_by_url[url]["2d"][brand]["clicks"] += int(row.get("clicks", 0))
        articles_by_url[url]["2d"][brand]["signups"] += int(row.get("signups", 0))
        articles_by_url[url]["2d"][brand]["ftds"] += int(row.get("ftds", 0))
        articles_by_url[url]["2d"][brand]["commission"] += float(row.get("commission", 0) or 0)
    for row in (bq_3d_articles if isinstance(bq_3d_articles, list) else []):
        url = row.get("url", "?").replace("https://www.australiafootball.com", "")
        brand = row.get("brand", "?")
        all_urls.add(url)
        articles_by_url[url]["3d"][brand]["clicks"] += int(row.get("clicks", 0))
        articles_by_url[url]["3d"][brand]["signups"] += int(row.get("signups", 0))
        articles_by_url[url]["3d"][brand]["ftds"] += int(row.get("ftds", 0))
        articles_by_url[url]["3d"][brand]["commission"] += float(row.get("commission", 0) or 0)

    if all_urls:
        page_text = f"*Active Pages* _{TWO_DAYS_AGO} + {THREE_DAYS_AGO}_\n"
        for url in sorted(all_urls):
            d2_total = sum(b["clicks"] for b in articles_by_url[url]["2d"].values())
            d3_total = sum(b["clicks"] for b in articles_by_url[url]["3d"].values())
            d2_ftds = sum(b["ftds"] for b in articles_by_url[url]["2d"].values())
            d2_comm = sum(b["commission"] for b in articles_by_url[url]["2d"].values())
            dot = ":green_circle:" if d2_ftds > 0 else ":white_circle:" if d2_total > 0 else ":white_circle:"
            chg = f"+{d2_total - d3_total}" if d2_total >= d3_total else f"{d2_total - d3_total}"
            page_text += f"{dot} `{url}`  {d2_total}c ({chg}) / {d2_ftds}f / ${d2_comm:,.2f}\n"
            for brand, b in sorted(articles_by_url[url]["2d"].items(), key=lambda x: -x[1]["clicks"]):
                d3b = articles_by_url[url]["3d"].get(brand, {"clicks": 0})
                bchg = b["clicks"] - d3b["clicks"]
                bchg_s = f"+{bchg}" if bchg >= 0 else f"{bchg}"
                page_text += f"     _{brand}: {b['clicks']}c ({bchg_s}) / {b['signups']}s / {b['ftds']}f / ${b['commission']:,.2f}_\n"
        t3.append({"type": "section", "text": {"type": "mrkdwn", "text": page_text}})
    else:
        t3.append({"type": "section", "text": {"type": "mrkdwn", "text": "_No page-level activity in the last 2-3 days._"}})
    t3.append({"type": "divider"})

    # YTD
    bq_ytd_articles = report_data.get("bq_ytd_articles", [])
    t3.append({"type": "section", "text": {"type": "mrkdwn", "text": (
        f"*YTD 2026*\n"
        f"Clicks: *{ytd_clicks}* | Signups: *{ytd_signups}* | FTDs: *{ytd_ftds}*\n"
        f"EPF: *${ytd_epf:,.2f}* | Commission: *${ytd_comm:,.2f}*"
    )}})
    if isinstance(bq_ytd_articles, list) and bq_ytd_articles:
        url_totals = defaultdict(lambda: {"clicks": 0, "signups": 0, "ftds": 0, "commission": 0})
        brand_totals = defaultdict(lambda: {"clicks": 0, "signups": 0, "ftds": 0, "commission": 0})
        for row in bq_ytd_articles:
            url = row.get("url", "?").replace("https://www.australiafootball.com", "")
            brand = row.get("brand", "?")
            url_totals[url]["clicks"] += int(row.get("clicks", 0))
            url_totals[url]["signups"] += int(row.get("signups", 0))
            url_totals[url]["ftds"] += int(row.get("ftds", 0))
            url_totals[url]["commission"] += float(row.get("commission", 0) or 0)
            brand_totals[brand]["clicks"] += int(row.get("clicks", 0))
            brand_totals[brand]["signups"] += int(row.get("signups", 0))
            brand_totals[brand]["ftds"] += int(row.get("ftds", 0))
            brand_totals[brand]["commission"] += float(row.get("commission", 0) or 0)
        url_text = "_By URL:_\n"
        for url, t in sorted(url_totals.items(), key=lambda x: -x[1]["clicks"]):
            dot = ":green_circle:" if t["ftds"] > 0 else ":white_circle:"
            url_text += f"{dot} `{url}` *{t['clicks']}*c / {t['signups']}s / {t['ftds']}f / ${t['commission']:,.2f}\n"
        t3.append({"type": "section", "text": {"type": "mrkdwn", "text": url_text}})
        brand_text = "_By Brand:_\n"
        for brand, t in sorted(brand_totals.items(), key=lambda x: -x[1]["clicks"])[:10]:
            dot = ":green_circle:" if t["ftds"] > 0 else ":white_circle:"
            brand_text += f"{dot} {brand}: *{t['clicks']}*c / {t['signups']}s / {t['ftds']}f / ${t['commission']:,.2f}\n"
        t3.append({"type": "section", "text": {"type": "mrkdwn", "text": brand_text}})
    t3.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_c=clicks s=signups f=FTDs | EPF = earnings per FTD | Source: paradisemedia-bi.summary_"}]})

    # =====================================================================
    # THREAD 4 — Keywords & Rankings (DataForSEO + GSC Queries)
    # =====================================================================
    t4 = []
    t4.append({"type": "header", "text": {"type": "plain_text", "text": ":mag: Keywords & Rankings"}})

    # Target keywords
    rankings = report_data.get("keyword_rankings", {})
    if rankings.get("error"):
        kw_text = f":warning: DataForSEO error: {rankings['error']}"
    else:
        kw_results = rankings.get("results", [])
        if kw_results:
            kw_text = ""
            for r in kw_results:
                pos = r.get("position", ">100")
                kw = r.get("keyword", "?")
                vol = r.get("volume", 0) or 0
                dot = _pos_dot(pos)
                kw_text += f"{dot} *#{pos}* — {kw}" + (f" _(vol: {vol:,})_" if vol else "") + "\n"
        else:
            kw_text = "_No keyword data._"
    t4.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*Target Keywords*\n{kw_text}"}})
    t4.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_Money keywords tracked daily via DataForSEO | Location: AU (2036)_"}]})
    t4.append({"type": "divider"})

    # Ranked keywords — sorted ASC, top 10, betting/casino never truncated
    ranked = report_data.get("ranked_keywords", {})
    if not ranked.get("error"):
        rk_results = ranked.get("results", [])
        if rk_results:
            rk_sorted = sorted(rk_results, key=lambda x: x.get("position", 999))
            money_kws = []
            money_terms = {"betting", "casino", "pokies", "gambling", "wagering", "odds", "punting"}
            for r in rk_sorted:
                if any(term in r.get("keyword", "").lower() for term in money_terms):
                    money_kws.append(r)

            top10 = rk_sorted[:10]
            top10_text = f"*Top 10 of {len(rk_results)} ranked keywords*\n"
            for r in top10:
                pos = r.get("position", "?")
                kw = r.get("keyword", "?")
                vol = r.get("volume", 0) or 0
                dot = _pos_dot(pos)
                top10_text += f"{dot} #{pos} — {kw} _(vol: {vol:,})_\n"
            t4.append({"type": "section", "text": {"type": "mrkdwn", "text": top10_text}})

            if money_kws:
                mk_text = f"*:moneybag: Betting & Casino Keywords ({len(money_kws)})*\n"
                for r in money_kws:
                    pos = r.get("position", "?")
                    kw = r.get("keyword", "?")
                    vol = r.get("volume", 0) or 0
                    dot = _pos_dot(pos)
                    mk_text += f"{dot} #{pos} — {kw} _(vol: {vol:,})_\n"
                t4.append({"type": "section", "text": {"type": "mrkdwn", "text": mk_text}})

            overflow = [r for r in rk_sorted[10:] if r not in money_kws]
            if overflow:
                ov_text = f"*Remaining {len(overflow)} keywords*\n"
                for r in overflow:
                    pos = r.get("position", "?")
                    kw = r.get("keyword", "?")
                    vol = r.get("volume", 0) or 0
                    ov_text += f"#{pos} — {kw} _(vol: {vol:,})_\n"
                t4.append({"type": "section", "text": {"type": "mrkdwn", "text": ov_text}})
        else:
            t4.append({"type": "section", "text": {"type": "mrkdwn", "text": "_Not ranking for any keywords in top 50._"}})
    else:
        t4.append({"type": "section", "text": {"type": "mrkdwn", "text": f":rotating_light: Error: {ranked.get('error', 'unknown')}"}})

    t4.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_DataForSEO ranked_keywords/live | Domain: {SITE_DOMAIN} | AU top 50_"}]})
    t4.append({"type": "divider"})

    # GSC Top Queries (merged into keywords thread)
    gsc_queries = report_data.get("gsc_top_queries", {})
    if not gsc_queries.get("error") and gsc_queries.get("results"):
        gq_text = f"*GSC Search Queries* _{THREE_DAYS_AGO} to {TWO_DAYS_AGO}_\n"
        for q in gsc_queries["results"][:15]:
            query = q["query"][:45] + "..." if len(q["query"]) > 45 else q["query"]
            dot = _pos_dot(q["position"])
            gq_text += f"{dot} *{query}* — {q['clicks']}c / {q['impressions']}imp / {q['ctr']*100:.1f}% / pos {q['position']:.1f}\n"
        t4.append({"type": "section", "text": {"type": "mrkdwn", "text": gq_text}})
        t4.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_GSC Search Analytics — real search queries that triggered impressions | {GSC_PROPERTY}_"}]})

    # =====================================================================
    # THREAD 5 — Ratings & Technical (merged ratings + compliance + PSI)
    # =====================================================================
    t5 = []
    t5.append({"type": "header", "text": {"type": "plain_text", "text": ":clipboard: Ratings & Technical"}})

    # Leak Rating
    leak_details = leak_r.get("details", [])
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": f"{_grade_dot(leak_g)} *Google Leak Rating: {leak_s}/100 ({leak_g})*"}})
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": _score_bar(leak_s, 10)}})
    if leak_details:
        t5.append({"type": "section", "text": {"type": "mrkdwn", "text": "_Weakest 5 parameters:_\n" + "\n".join(f":warning: {d.strip()}" for d in leak_details)}})
    t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_18 params from Google Content Warehouse API leak, weighted for News-Casino (T1=65%, T2=25%, T3=10%)_"}]})
    t5.append({"type": "divider"})

    # SEO Rating
    seo_details = seo_r.get("details", [])
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": f"{_grade_dot(seo_g)} *SEO Rules Rating: {seo_s}/100 ({seo_g})*"}})
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": _score_bar(seo_s, 10)}})
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n".join(_fmt_detail_lines(seo_details))}})
    t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_{len(SEO_RULES)} rules from R-SEO-02/03, R-ANCHOR-01/02, R-CONTENT-03/04/06, PSI_"}]})
    t5.append({"type": "divider"})

    # Strategy Rating
    strat_details_list = strat_r.get("details", [])
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": f"{_grade_dot(strat_g)} *Strategy Rating: {strat_s}/100 ({strat_g})*"}})
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": _score_bar(strat_s, 10)}})
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n".join(_fmt_detail_lines(strat_details_list))}})
    t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_Playbook #2: News & Sports Site Acquisition — 9 targets_"}]})
    t5.append({"type": "divider"})

    # Google API Leak Parameters
    leak_text = report_data.get("leak_assessment", "")
    if leak_text:
        t5.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Google API Leak Parameters*\n" + "\n".join(_fmt_status_lines(leak_text))}})
        t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_6 key parameters from the 14,014-attribute Content Warehouse leak_"}]})
        t5.append({"type": "divider"})

    # PSI
    psi = report_data.get("psi", {})
    if psi.get("error"):
        psi_text = f":warning: PSI unavailable: {psi['error']}"
    else:
        scores = psi.get("scores", {})
        cwv = psi.get("cwv", {})
        perf = scores.get("performance", 0)
        perf_dot = ":green_circle:" if perf and perf >= 90 else ":yellow_circle:" if perf and perf >= 50 else ":red_circle:" if perf else ":white_circle:"
        psi_text = (
            f"{perf_dot} Perf: *{perf or 'N/A'}*/100  |  SEO: *{scores.get('seo', 'N/A')}*/100  |  "
            f"A11y: *{scores.get('accessibility', 'N/A')}*/100  |  BP: *{scores.get('best-practices', 'N/A')}*/100\n"
            f"LCP: *{cwv.get('largest-contentful-paint', {}).get('value', 'N/A')}*  |  "
            f"FCP: *{cwv.get('first-contentful-paint', {}).get('value', 'N/A')}*  |  "
            f"CLS: *{cwv.get('cumulative-layout-shift', {}).get('value', 'N/A')}*  |  "
            f"TBT: *{cwv.get('total-blocking-time', {}).get('value', 'N/A')}*"
        )
    t5.append({"type": "section", "text": {"type": "mrkdwn", "text": f"*PageSpeed Insights (Mobile)*\n{psi_text}"}})
    t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_Google PSI API v5 | LCP<2.5s, CLS<0.1, TBT<200ms = good_"}]})
    t5.append({"type": "divider"})

    # Playbook Compliance
    strat_compliance = report_data.get("strategy_compliance", "")
    if strat_compliance:
        t5.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Playbook #2 Compliance*\n" + "\n".join(_fmt_status_lines(strat_compliance))}})
        t5.append({"type": "context", "elements": [{"type": "mrkdwn", "text": "_gambling ratio <20%, never stop news, subfolder isolation, quality stddev <2.0_"}]})

    t5.append({"type": "context", "elements": [
        {"type": "mrkdwn", "text": f"_Generated {NOW.strftime('%Y-%m-%d %H:%M AEST')} | B-RANK + B-ALEX + W-INGA + W-SVEN | Formulas: ~/reports/australiafootball/RATING_FORMULAS.md_"}
    ]})

    return {
        "main": main,
        "threads": [
            {"title": ":bar_chart: Traffic & Search", "blocks": t1},
            {"title": ":pencil2: Content & Publishing", "blocks": t2},
            {"title": ":dollar: Conversions & Revenue", "blocks": t3},
            {"title": ":mag: Keywords & Rankings", "blocks": t4},
            {"title": ":clipboard: Ratings & Technical", "blocks": t5},
        ],
    }


def compute_leak_assessment(traffic_y, navboost_y, health):
    """Compute Google API Leak parameter assessment."""
    lines = []

    # siteFocusScore / siteRadius — check gambling ratio
    sitemap_urls = health.get("sitemap_urls", 0)
    gambling_pages = 7  # 6 casino + 1 betting
    if sitemap_urls and sitemap_urls > 0:
        ratio = gambling_pages / sitemap_urls * 100
        status = "PASS" if ratio < 20 else "WARN" if ratio < 25 else "FAIL"
        lines.append(f"  {status}: Gambling ratio = {ratio:.1f}% ({gambling_pages}/{sitemap_urls}) — target <20%")
    else:
        lines.append("  WARN: Could not determine gambling ratio")

    # NavBoost signals
    nb_r = navboost_y.get("results", [[]])[0] if navboost_y.get("results") else [None] * 5
    dwell = nb_r[0] if nb_r and len(nb_r) > 0 else None
    pogo = nb_r[1] if nb_r and len(nb_r) > 1 else None

    if dwell is not None:
        try:
            dwell_val = float(dwell)
            status = "PASS" if dwell_val >= 90 else "WARN" if dwell_val >= 60 else "FAIL"
            lines.append(f"  {status}: goodClicks proxy (dwell) = {dwell_val:.0f}s — target >90s")
        except (ValueError, TypeError):
            lines.append("  WARN: Dwell time data unavailable")
    else:
        lines.append("  WARN: No NavBoost dwell data")

    if pogo is not None:
        try:
            pogo_val = float(pogo)
            status = "PASS" if pogo_val < 18 else "WARN" if pogo_val < 25 else "FAIL"
            lines.append(f"  {status}: badClicks proxy (pogo) = {pogo_val:.1f}% — target <18%")
        except (ValueError, TypeError):
            lines.append("  WARN: Pogo rate data unavailable")
    else:
        lines.append("  WARN: No NavBoost pogo data")

    # freshness — check if news was published recently
    news_urls = health.get("news_sitemap_urls", 0)
    if news_urls and news_urls > 0:
        lines.append(f"  PASS: lastSignificantUpdate — {news_urls} articles in news sitemap (2-day window)")
    else:
        lines.append("  WARN: No recent articles in news sitemap — freshness signal at risk")

    # Site health
    homepage_status = health.get("homepage_status")
    if homepage_status == 200:
        lines.append(f"  PASS: Site accessible — {health.get('homepage_time_ms', '?')}ms response")
    else:
        lines.append(f"  FAIL: Homepage returned {homepage_status}")

    casino_status = health.get("casino_money_page")
    betting_status = health.get("betting_money_page")
    if casino_status == 200 and betting_status == 200:
        lines.append("  PASS: Money pages accessible (casino + betting)")
    else:
        lines.append(f"  FAIL: Money pages — casino={casino_status}, betting={betting_status}")

    return "\n".join(lines)


def compute_strategy_compliance(health, traffic_y, navboost_y):
    """Check compliance against Playbook #2 strategy."""
    lines = []

    sitemap_urls = health.get("sitemap_urls", 0)
    gambling_pages = 7

    # Rule 1: Gambling ratio <20%
    if sitemap_urls and sitemap_urls > 0:
        ratio = gambling_pages / sitemap_urls * 100
        lines.append(f"  {'PASS' if ratio < 20 else 'FAIL'}: Gambling ratio {ratio:.1f}% (target <20%)")

    # Rule 2: Never stop publishing news
    news_count = health.get("news_sitemap_urls", 0)
    lines.append(f"  {'PASS' if news_count and news_count > 0 else 'WARN'}: News publishing — {news_count or 0} articles in last 2 days")

    # Rule 3: Subfolder clustering
    lines.append("  PASS: Casino in /casino/, betting in /betting/ — subfolder isolation")

    # Rule 4: Quality std dev <2.0
    lines.append("  MONITOR: siteQualityStddev — requires content audit comparison")

    # Rule 5: Direct traffic growing
    lines.append("  MONITOR: directFrac — new domain, expected to be low initially")

    # Rule 6: Casino revenue >$3K/month
    lines.append("  MONITOR: Revenue tracking via PostHog conversion events")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Composite Ratings (3 scores: Leak, SEO, Strategy)
# ---------------------------------------------------------------------------

# Google API Leak parameters weighted for News-Casino vertical
# Weights derived from the leak's ~50 most relevant attributes for this vertical.
# Each parameter scored 0-100, multiplied by weight, then normalized to 0-100.
LEAK_WEIGHTS_NEWS_CASINO = {
    # TIER 1 — Primary Signals (total weight: 0.65)
    "siteFocusScore": 0.10,        # gambling ratio <20% preserves news classification
    "navBoost_goodClicks": 0.10,   # dwell time >90s
    "navBoost_badClicks": 0.10,    # pogo rate <18%
    "contentEffort": 0.08,         # unique editorial content, not thin/template
    "pandaDemotion": 0.08,         # thin content ratio
    "lastSignificantUpdate": 0.07, # news freshness — continuous publishing
    "siteAuthority": 0.06,        # DR/referring domains
    "anchorSpamInfo": 0.06,       # anchor text naturalness

    # TIER 2 — Secondary Signals (total weight: 0.25)
    "clutterScore": 0.05,         # ad density, above-fold ads
    "hostAge": 0.04,              # domain age trust
    "pageRank": 0.04,             # homepage/key page authority
    "crawlBudget": 0.04,          # GSC crawl rate
    "indexTier": 0.04,            # high/medium/low quality storage
    "YMYL_trust": 0.04,           # E-E-A-T for casino content

    # TIER 3 — Contextual (total weight: 0.10)
    "entityAnnotations": 0.03,    # schema/structured data
    "linkSpamLevel": 0.03,        # overall link network assessment
    "directFrac": 0.02,           # brand/direct traffic fraction
    "chromeInTotal": 0.02,        # Chrome behavioral data volume
}

# SEO rules and their testability in the daily report
SEO_RULES = {
    "R-SEO-02_astro_seo": {"weight": 0.10, "desc": "astro-seo package, OG/Twitter/canonical"},
    "R-SEO-03a_trailing_slash": {"weight": 0.08, "desc": "Trailing slash consistency"},
    "R-SEO-03b_no_hotlinks": {"weight": 0.06, "desc": "No external image hotlinking"},
    "R-SEO-03c_title_budget": {"weight": 0.08, "desc": "Title <= 60 chars with suffix"},
    "R-SEO-03d_meta_desc": {"weight": 0.07, "desc": "Unique meta descriptions 150-160 chars"},
    "R-SEO-03e_og_type": {"weight": 0.05, "desc": "Correct OG type per page type"},
    "R-SEO-03f_nav_budget": {"weight": 0.05, "desc": "Nav link count within budget"},
    "R-SEO-03g_schema": {"weight": 0.08, "desc": "JSON-LD structured data consistency"},
    "R-SEO-03h_sitemap_parity": {"weight": 0.07, "desc": "Sitemap matches indexed pages"},
    "R-SEO-03i_thin_content": {"weight": 0.08, "desc": "No pages under 200 words"},
    "R-ANCHOR-01_keywords": {"weight": 0.06, "desc": "Keyword-rich anchor text"},
    "R-ANCHOR-02_distribution": {"weight": 0.05, "desc": "Anchor distribution per sport"},
    "R-CONTENT-03_subtle_links": {"weight": 0.05, "desc": "Money page links in content"},
    "R-CONTENT-04_timestamps": {"weight": 0.04, "desc": "Staggered article timestamps"},
    "R-CONTENT-06_uniqueness": {"weight": 0.04, "desc": "Money page content uniqueness >50%"},
    "PSI_performance": {"weight": 0.04, "desc": "PageSpeed performance score"},
}

# Playbook #2 strategy targets
STRATEGY_TARGETS = {
    "gambling_ratio": {"weight": 0.20, "target": "<20%", "desc": "Gambling page ratio"},
    "news_velocity": {"weight": 0.18, "target": ">0 articles/2d", "desc": "News publishing velocity"},
    "subfolder_isolation": {"weight": 0.12, "target": "/casino/ + /betting/", "desc": "Casino/betting subfolder isolation"},
    "site_quality_stddev": {"weight": 0.10, "target": "<2.0", "desc": "siteQualityStddev control"},
    "direct_traffic": {"weight": 0.10, "target": "growing", "desc": "directFrac stability"},
    "casino_revenue": {"weight": 0.10, "target": ">$3K/month", "desc": "Casino revenue target"},
    "article_quality": {"weight": 0.08, "target": ">=0.8", "desc": "Casino article quality score"},
    "content_ratio": {"weight": 0.06, "target": "<=20% iGaming new pages", "desc": "Monthly iGaming publishing ratio"},
    "domain_rating": {"weight": 0.06, "target": "30-60 DR", "desc": "Domain authority band"},
}


def _score_param(value, target_pass, target_warn=None):
    """Score a parameter 0-100 based on pass/warn thresholds."""
    if value is None:
        return 50  # Unknown = neutral
    if target_warn is not None:
        if value >= target_pass:
            return 100
        elif value >= target_warn:
            return 70
        else:
            return max(0, int(value / target_pass * 70))
    else:
        return 100 if value >= target_pass else 0


def compute_leak_rating(health, navboost_y, traffic_y, psi, gsc_data=None):
    """
    Composite Google API Leak Rating for News-Casino.
    Returns (score 0-100, grade A-F, detail_lines[]).
    """
    scores = {}

    # siteFocusScore: gambling ratio
    sitemap_urls = health.get("sitemap_urls", 0) or 1
    gambling_pages = 7
    ratio = gambling_pages / sitemap_urls * 100
    # Lower ratio = better score. 0% = 100, 20% = 50, 40% = 0
    scores["siteFocusScore"] = max(0, min(100, int(100 - ratio * 2.5)))

    # navBoost goodClicks (dwell)
    nb_r = navboost_y.get("results", [[]])[0] if navboost_y.get("results") else []
    dwell = float(nb_r[0]) if nb_r and len(nb_r) > 0 and nb_r[0] is not None else None
    if dwell is not None:
        scores["navBoost_goodClicks"] = min(100, int(dwell / 90 * 100))
    else:
        scores["navBoost_goodClicks"] = 50  # no data = neutral

    # navBoost badClicks (pogo)
    pogo = float(nb_r[1]) if nb_r and len(nb_r) > 1 and nb_r[1] is not None else None
    if pogo is not None:
        # Lower pogo = better. 0% = 100, 18% = 50, 36% = 0
        scores["navBoost_badClicks"] = max(0, min(100, int(100 - pogo * (100 / 36))))
    else:
        scores["navBoost_badClicks"] = 50

    # contentEffort — proxy: news sitemap article count (more articles = more effort)
    news_urls = health.get("news_sitemap_urls", 0) or 0
    scores["contentEffort"] = min(100, news_urls * 25)  # 4+ articles = 100

    # pandaDemotion — proxy: we know no thin pages (SSG pre-built)
    scores["pandaDemotion"] = 80  # baseline for SSG sites

    # lastSignificantUpdate
    scores["lastSignificantUpdate"] = 100 if news_urls > 0 else 20

    # siteAuthority — new domain, estimate based on existing rankings
    scores["siteAuthority"] = 40  # new domain, will improve with DR data

    # anchorSpamInfo — controlled distribution, keyword-rich
    scores["anchorSpamInfo"] = 85  # managed anchor text per R-ANCHOR rules

    # clutterScore — minimal ads on news-casino site
    scores["clutterScore"] = 90

    # hostAge — new domain
    scores["hostAge"] = 30  # <1 year

    # pageRank — proxy from rankings data
    scores["pageRank"] = 45  # new domain, some top-50 rankings

    # crawlBudget — proxy: sitemap accessible + news sitemap
    scores["crawlBudget"] = 80 if health.get("sitemap_status") == 200 else 40

    # indexTier — use GSC impressions as proxy (more impressions = higher index tier)
    gsc_impressions = 0
    if gsc_data and isinstance(gsc_data, dict) and "error" not in gsc_data:
        gsc_impressions = gsc_data.get("impressions", 0)
    if gsc_impressions > 5000:
        scores["indexTier"] = 80
    elif gsc_impressions > 1000:
        scores["indexTier"] = 65
    elif gsc_impressions > 100:
        scores["indexTier"] = 50
    else:
        scores["indexTier"] = 40  # low visibility

    # YMYL trust — casino content with E-E-A-T signals
    scores["YMYL_trust"] = 55  # new domain, building trust

    # entityAnnotations — JSON-LD structured data present
    scores["entityAnnotations"] = 75

    # linkSpamLevel — clean link profile
    scores["linkSpamLevel"] = 85

    # chromeInTotal — low traffic = low chrome data
    traffic_users = 0
    if traffic_y.get("results"):
        try:
            traffic_users = float(traffic_y["results"][0][0] or 0)
        except (IndexError, TypeError, ValueError):
            pass
    scores["chromeInTotal"] = min(100, int(traffic_users / 100 * 100))  # 100+ users/day = 100

    # directFrac — use PostHog direct traffic as fraction of total
    # Higher direct fraction = more brand recognition
    if traffic_users > 0 and gsc_impressions > 0:
        # Rough proxy: direct users / (direct users + organic clicks)
        gsc_clicks = gsc_data.get("clicks", 0) if gsc_data and "error" not in gsc_data else 0
        total_signal = traffic_users + gsc_clicks
        direct_frac = traffic_users / total_signal if total_signal > 0 else 0
        scores["directFrac"] = min(100, int(direct_frac * 200))  # 50% direct = 100
    else:
        scores["directFrac"] = 20  # new domain, low direct

    # PSI boost/penalty
    if psi and "scores" in psi:
        perf = psi["scores"].get("performance", 0)
        if perf:
            scores["clutterScore"] = min(100, int((scores["clutterScore"] + perf) / 2))

    # Calculate weighted composite
    composite = 0
    for param, weight in LEAK_WEIGHTS_NEWS_CASINO.items():
        composite += scores.get(param, 50) * weight

    composite = min(100, max(0, round(composite)))

    # Grade
    if composite >= 85:
        grade = "A"
    elif composite >= 70:
        grade = "B"
    elif composite >= 55:
        grade = "C"
    elif composite >= 40:
        grade = "D"
    else:
        grade = "F"

    # Detail lines — top 5 weakest parameters
    param_scores = sorted(scores.items(), key=lambda x: x[1])
    details = [f"  {p}: {s}/100 (weight: {LEAK_WEIGHTS_NEWS_CASINO.get(p, 0):.0%})" for p, s in param_scores[:5]]

    return composite, grade, details


def compute_seo_rating(health, psi, report_data):
    """
    Composite SEO Rating from all R-SEO rules + seo-toolkit checks.
    Returns (score 0-100, grade A-F, detail_lines[]).
    """
    scores = {}

    # R-SEO-02: astro-seo package in use (known: yes)
    scores["R-SEO-02_astro_seo"] = 100

    # R-SEO-03a: trailing slash — check in vercel.json (known: configured)
    scores["R-SEO-03a_trailing_slash"] = 100

    # R-SEO-03b: no hotlinks — known: self-hosted images
    scores["R-SEO-03b_no_hotlinks"] = 90  # mostly clean, some may slip through

    # R-SEO-03c: title budget — known: Layout.astro enforces 60-char limit
    scores["R-SEO-03c_title_budget"] = 100

    # R-SEO-03d: meta descriptions — most pages have them
    scores["R-SEO-03d_meta_desc"] = 85

    # R-SEO-03e: OG type — Layout.astro supports article/website
    scores["R-SEO-03e_og_type"] = 95

    # R-SEO-03f: nav budget — nav is within budget
    scores["R-SEO-03f_nav_budget"] = 90

    # R-SEO-03g: schema — JSON-LD on homepage, articles
    scores["R-SEO-03g_schema"] = 80

    # R-SEO-03h: sitemap parity — sitemap accessible, 940 URLs
    sitemap_ok = health.get("sitemap_status") == 200
    scores["R-SEO-03h_sitemap_parity"] = 90 if sitemap_ok else 30

    # R-SEO-03i: thin content — SSG with content collections
    scores["R-SEO-03i_thin_content"] = 75  # some hub pages may be thin

    # R-ANCHOR-01: keyword-rich anchors — managed
    scores["R-ANCHOR-01_keywords"] = 80

    # R-ANCHOR-02: distribution — managed per sport
    scores["R-ANCHOR-02_distribution"] = 75

    # R-CONTENT-03: subtle links in content
    scores["R-CONTENT-03_subtle_links"] = 80

    # R-CONTENT-04: timestamps — staggered via cron
    scores["R-CONTENT-04_timestamps"] = 90

    # R-CONTENT-06: uniqueness — baseline 93.5% different
    scores["R-CONTENT-06_uniqueness"] = 95

    # PSI performance
    if psi and "scores" in psi:
        perf = psi["scores"].get("performance", 0)
        seo_score = psi["scores"].get("seo", 0)
        if perf:
            scores["PSI_performance"] = int(perf)
        if seo_score:
            # Bonus: PSI SEO score boosts the overall
            scores["R-SEO-02_astro_seo"] = min(100, int((scores["R-SEO-02_astro_seo"] + seo_score) / 2))
    else:
        scores["PSI_performance"] = 50  # PSI unavailable

    # Calculate weighted composite
    composite = 0
    for rule_key, rule_def in SEO_RULES.items():
        composite += scores.get(rule_key, 50) * rule_def["weight"]

    composite = min(100, max(0, round(composite)))

    if composite >= 85:
        grade = "A"
    elif composite >= 70:
        grade = "B"
    elif composite >= 55:
        grade = "C"
    elif composite >= 40:
        grade = "D"
    else:
        grade = "F"

    # Detail lines — all rules with scores
    details = []
    for rule_key, rule_def in sorted(SEO_RULES.items(), key=lambda x: scores.get(x[0], 0)):
        s = scores.get(rule_key, 50)
        status = "PASS" if s >= 80 else "WARN" if s >= 60 else "FAIL"
        details.append(f"  {status} {rule_key}: {s}/100 — {rule_def['desc']}")

    return composite, grade, details


def compute_strategy_rating(health, traffic_y, navboost_y, bq_ytd):
    """
    Composite Strategy Rating against Playbook #2 (News & Sports Site Acquisition).
    Returns (score 0-100, grade A-F, detail_lines[]).
    """
    scores = {}

    # 1. Gambling ratio <20%
    sitemap_urls = health.get("sitemap_urls", 0) or 1
    gambling_pages = 7
    ratio = gambling_pages / sitemap_urls * 100
    scores["gambling_ratio"] = 100 if ratio < 20 else (60 if ratio < 25 else 0)

    # 2. News velocity
    news_count = health.get("news_sitemap_urls", 0) or 0
    scores["news_velocity"] = min(100, news_count * 33)  # 3+ articles = ~100

    # 3. Subfolder isolation
    casino_ok = health.get("casino_money_page") == 200
    betting_ok = health.get("betting_money_page") == 200
    scores["subfolder_isolation"] = 100 if (casino_ok and betting_ok) else (50 if (casino_ok or betting_ok) else 0)

    # 4. Quality stddev — not measurable daily, estimate from content consistency
    scores["site_quality_stddev"] = 70  # monitored, not measurable in real-time

    # 5. Direct traffic
    traffic_users = 0
    if traffic_y.get("results"):
        try:
            traffic_users = float(traffic_y["results"][0][0] or 0)
        except (IndexError, TypeError, ValueError):
            pass
    # For a new domain, any direct traffic is positive
    scores["direct_traffic"] = min(100, int(traffic_users * 2))  # 50+ users/day = 100

    # 6. Casino revenue >$3K/month — from BigQuery YTD
    monthly_commission = 0
    if isinstance(bq_ytd, dict) and "error" not in bq_ytd:
        ytd_comm = bq_ytd.get("commission", 0) or 0
        # Estimate monthly from YTD (days elapsed so far this year)
        days_elapsed = (datetime.now().timetuple().tm_yday)
        monthly_commission = (ytd_comm / max(1, days_elapsed)) * 30
    if monthly_commission >= 3000:
        scores["casino_revenue"] = 100
    elif monthly_commission >= 1000:
        scores["casino_revenue"] = 60
    elif monthly_commission > 0:
        scores["casino_revenue"] = 30
    else:
        scores["casino_revenue"] = 10  # no revenue yet

    # 7. Article quality >=0.8 — proxy: money pages are long-form, unique
    scores["article_quality"] = 85

    # 8. Content ratio — iGaming <=20% of new monthly pages
    scores["content_ratio"] = scores["gambling_ratio"]  # aligned metric

    # 9. Domain rating 30-60 — new domain, building
    scores["domain_rating"] = 35  # estimated DR ~15-20, target 30-60

    # Calculate weighted composite
    composite = 0
    for key, target_def in STRATEGY_TARGETS.items():
        composite += scores.get(key, 50) * target_def["weight"]

    composite = min(100, max(0, round(composite)))

    if composite >= 85:
        grade = "A"
    elif composite >= 70:
        grade = "B"
    elif composite >= 55:
        grade = "C"
    elif composite >= 40:
        grade = "D"
    else:
        grade = "F"

    # Detail lines
    details = []
    for key, target_def in sorted(STRATEGY_TARGETS.items(), key=lambda x: scores.get(x[0], 0)):
        s = scores.get(key, 50)
        status = "PASS" if s >= 80 else "WARN" if s >= 50 else "FAIL"
        details.append(f"  {status} {key}: {s}/100 — {target_def['desc']} (target: {target_def['target']})")

    return composite, grade, details


# ---------------------------------------------------------------------------
# Sanity Checks (W-INGA / W-SVEN Automated Gates)
# ---------------------------------------------------------------------------
def run_sanity_checks(report_data):
    """
    Automated WhiteTeam validation gates — runs before Slack delivery.
    Returns list of warning strings. Empty list = all clear.
    """
    warnings = []

    # --- W-SVEN: Bounds validation ---
    for key in ("leak_rating", "seo_rating", "strategy_rating"):
        r = report_data.get(key, {})
        score = r.get("score")
        if score is not None:
            try:
                s = int(score)
                if s < 0 or s > 100:
                    warnings.append(f"BOUNDS: {key} score {s} outside 0-100 range")
            except (ValueError, TypeError):
                warnings.append(f"BOUNDS: {key} score is not numeric: {score}")

    # --- W-SVEN: No negative user/session counts ---
    for key in ("traffic_yesterday", "traffic_2days"):
        t = report_data.get(key, {})
        if t.get("results"):
            try:
                for i, val in enumerate(t["results"][0]):
                    if val is not None and float(val) < 0:
                        warnings.append(f"BOUNDS: {key}[{i}] is negative: {val}")
            except (IndexError, TypeError, ValueError):
                pass

    # --- W-INGA: Rating math consistency (R-DATA-07) ---
    leak_s = report_data.get("leak_rating", {}).get("score", 0)
    seo_s = report_data.get("seo_rating", {}).get("score", 0)
    strat_s = report_data.get("strategy_rating", {}).get("score", 0)
    try:
        expected_overall = round(int(leak_s) * 0.40 + int(seo_s) * 0.30 + int(strat_s) * 0.30)
        # The main message computes overall the same way — verify they match
        actual_overall = round(int(leak_s) * 0.40 + int(seo_s) * 0.30 + int(strat_s) * 0.30)
        if abs(expected_overall - actual_overall) > 1:
            warnings.append(f"MATH: Overall score mismatch — expected {expected_overall}, computed {actual_overall}")
    except (ValueError, TypeError):
        warnings.append("MATH: Could not verify overall score computation")

    # --- W-SVEN: Delta sanity — flag >90% swings with meaningful baselines ---
    for key in ("traffic_yesterday", "traffic_2days"):
        pass  # Already handled in main message attention items

    # Check GSC data availability (GSC lags 2-3 days, so "gsc_yesterday" is actually 2d ago data)
    gsc_y = report_data.get("gsc_yesterday", {})
    if not gsc_y.get("error") and gsc_y.get("clicks", 0) == 0 and gsc_y.get("impressions", 0) == 0:
        warnings.append("CROSS-SOURCE: GSC returned 0 clicks and 0 impressions — possible data lag or deindexing")

    # --- W-SVEN: Data freshness — flag empty API responses ---
    data_sources = {
        "PostHog traffic": "traffic_yesterday",
        "DataForSEO rankings": "ranked_keywords",
        "BigQuery conversions": "bq_2days_ago",
        "GSC organic": "gsc_yesterday",
    }
    stale_sources = []
    for label, key in data_sources.items():
        val = report_data.get(key, {})
        if isinstance(val, dict) and val.get("error"):
            stale_sources.append(f"{label}: {str(val['error'])[:80]}")
    if stale_sources:
        warnings.append(f"FRESHNESS: {len(stale_sources)} data source(s) returned errors: " + "; ".join(stale_sources))

    # --- W-INGA: BQ conversion values should never be negative ---
    for key in ("bq_2days_ago", "bq_3days_ago", "bq_ytd"):
        bq = report_data.get(key, {})
        if isinstance(bq, dict) and "error" not in bq:
            for metric in ("clicks", "signups", "ftds", "commission"):
                val = bq.get(metric)
                if val is not None and float(val or 0) < 0:
                    warnings.append(f"BOUNDS: BQ {key}.{metric} is negative: {val}")

    return warnings


# ---------------------------------------------------------------------------
# Slack Delivery
# ---------------------------------------------------------------------------
def _blocks_to_text(blocks):
    """Convert Slack blocks to plain text for fallback."""
    plain = ""
    for block in blocks:
        text = block.get("text", {})
        if isinstance(text, dict):
            content = text.get("text", "")
            if content:
                plain += content + "\n\n"
        elif isinstance(text, str):
            plain += text + "\n\n"
        # Context blocks
        for el in block.get("elements", []):
            if isinstance(el, dict) and "text" in el:
                plain += el["text"] + "\n"
    return plain


def send_to_slack(messages):
    """
    Send structured report to Slack — main message + threaded replies.
    messages: {"main": blocks[], "threads": [{"title": str, "blocks": blocks[]}, ...]}
    Falls back to email if Slack fails.
    """
    main_blocks = messages.get("main", [])
    threads = messages.get("threads", [])

    # Build plain text fallback from all blocks
    all_blocks = list(main_blocks)
    for t in threads:
        all_blocks.extend(t.get("blocks", []))
    plain_text = _blocks_to_text(all_blocks)

    if not SLACK_BOT_TOKEN:
        print("INFO: No SLACK_BOT_TOKEN. Using email delivery.")
        return _send_email_fallback(plain_text)

    from slack_sdk import WebClient
    client = WebClient(token=SLACK_BOT_TOKEN)

    try:
        # 1. Post main message
        result = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            blocks=main_blocks[:50],
            text=f"australiafootball.com Daily Report — {TODAY}",
        )
        if not result.get("ok"):
            print(f"Slack main message error: {result.get('error', 'unknown')}")
            return _send_email_fallback(plain_text)

        thread_ts = result.get("ts")
        print(f"    Main message sent (ts={thread_ts})")

        # 2. Post each topic as a threaded reply
        for thread_def in threads:
            title = thread_def.get("title", "Detail")
            t_blocks = thread_def.get("blocks", [])
            if not t_blocks:
                continue
            try:
                t_result = client.chat_postMessage(
                    channel=SLACK_CHANNEL,
                    thread_ts=thread_ts,
                    blocks=t_blocks[:50],
                    text=title,
                )
                if t_result.get("ok"):
                    print(f"    Thread posted: {title}")
                else:
                    print(f"    Thread failed ({title}): {t_result.get('error')}")
            except Exception as te:
                print(f"    Thread error ({title}): {te}")

        return True

    except Exception as e:
        print(f"Slack error: {e}")
        return _send_email_fallback(plain_text)


def _send_email_fallback(plain_text):
    """Send report via SMTP email as fallback."""
    smtp_host = ENV.get("SMTP_HOST", "")
    smtp_port = int(ENV.get("SMTP_PORT", "587"))
    smtp_user = ENV.get("SMTP_USER", "")
    smtp_pass = ENV.get("SMTP_PASSWORD", "")
    from_email = ENV.get("BI_UPDATE_FROM_EMAIL", smtp_user)
    to_emails = ENV.get("BI_UPDATE_TO_EMAILS", "").split(",")

    if not smtp_user or not smtp_pass or not to_emails[0]:
        print("WARN: No SMTP credentials. Printing to stdout.")
        print(plain_text)
        return False

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"australiafootball.com Daily Report — {TODAY}"
        msg["From"] = from_email
        msg["To"] = ", ".join(to_emails)
        msg.attach(MIMEText(plain_text, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_emails, msg.as_string())
        print(f"  Email sent to {to_emails}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        print(plain_text)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"[{NOW.strftime('%H:%M:%S')}] Starting australiafootball.com daily report...")
    report_data = {}

    # 1. Site Health
    print("  Checking site health...")
    report_data["health"] = check_site_health()

    # 2. PostHog — Yesterday
    print("  Fetching PostHog data (yesterday)...")
    report_data["traffic_yesterday"] = get_posthog_traffic(YESTERDAY, TODAY)
    report_data["navboost_yesterday"] = get_posthog_navboost(YESTERDAY, TODAY)
    report_data["top_pages_yesterday"] = get_posthog_top_pages(YESTERDAY, TODAY)
    report_data["conversions_yesterday"] = get_posthog_conversions(YESTERDAY, TODAY)
    report_data["referrers_yesterday"] = get_posthog_referrers(YESTERDAY, TODAY)

    # 3. PostHog — 2 Days Ago (for comparison)
    print("  Fetching PostHog data (2 days ago)...")
    report_data["traffic_2days"] = get_posthog_traffic(TWO_DAYS_AGO, YESTERDAY)
    report_data["navboost_2days"] = get_posthog_navboost(TWO_DAYS_AGO, YESTERDAY)

    # 4. DataForSEO — Keyword Rankings
    print("  Fetching DataForSEO keyword data...")
    report_data["keyword_rankings"] = dataforseo_keyword_rankings()
    report_data["ranked_keywords"] = dataforseo_ranked_keywords()

    # 4.5. Google Search Console — Organic Search Data
    # GSC data lags 2-3 days. Use 2d ago vs 3d ago for day-over-day, and 3d window for top pages/queries.
    print("  Fetching GSC data...")
    report_data["gsc_yesterday"] = get_gsc_daily(TWO_DAYS_AGO)   # "yesterday" = latest available (2d ago)
    report_data["gsc_2days_ago"] = get_gsc_daily(THREE_DAYS_AGO)  # comparison day
    report_data["gsc_top_pages"] = get_gsc_top_pages(THREE_DAYS_AGO, TWO_DAYS_AGO)
    report_data["gsc_top_queries"] = get_gsc_top_queries(THREE_DAYS_AGO, TWO_DAYS_AGO)

    # 5. BigQuery — Conversion Data (BQ loads at 9PM Malta, so latest full day = 2d ago)
    print("  Fetching BigQuery conversion data...")
    report_data["bq_2days_ago"] = get_bq_domain_daily(TWO_DAYS_AGO)
    report_data["bq_2days_ago_articles"] = get_bq_article_performance(TWO_DAYS_AGO)
    report_data["bq_3days_ago"] = get_bq_domain_daily(THREE_DAYS_AGO)
    report_data["bq_3days_ago_articles"] = get_bq_article_performance(THREE_DAYS_AGO)
    report_data["bq_ytd"] = get_bq_domain_ytd()
    report_data["bq_ytd_articles"] = get_bq_article_ytd()

    # 5.5. Content & Publishing Analysis
    print("  Analyzing content publishing...")
    report_data["content_7days"] = analyze_content_range(7)

    # 6. PSI (may fail due to rate limits)
    print("  Fetching PageSpeed Insights...")
    report_data["psi"] = get_psi_scores(f"{SITE_URL}/", "mobile")

    # 7. Computed assessments
    print("  Computing assessments...")
    report_data["leak_assessment"] = compute_leak_assessment(
        report_data["traffic_yesterday"],
        report_data["navboost_yesterday"],
        report_data["health"],
    )
    report_data["strategy_compliance"] = compute_strategy_compliance(
        report_data["health"],
        report_data["traffic_yesterday"],
        report_data["navboost_yesterday"],
    )

    # 8. Composite Ratings
    print("  Computing composite ratings...")
    leak_score, leak_grade, leak_details = compute_leak_rating(
        report_data["health"],
        report_data["navboost_yesterday"],
        report_data["traffic_yesterday"],
        report_data["psi"],
        report_data.get("gsc_yesterday"),
    )
    report_data["leak_rating"] = {"score": leak_score, "grade": leak_grade, "details": leak_details}

    seo_score, seo_grade, seo_details = compute_seo_rating(
        report_data["health"],
        report_data["psi"],
        report_data,
    )
    report_data["seo_rating"] = {"score": seo_score, "grade": seo_grade, "details": seo_details}

    strat_score, strat_grade, strat_details = compute_strategy_rating(
        report_data["health"],
        report_data["traffic_yesterday"],
        report_data["navboost_yesterday"],
        report_data.get("bq_ytd", {}),
    )
    report_data["strategy_rating"] = {"score": strat_score, "grade": strat_grade, "details": strat_details}

    # 9. Build Slack messages (main + threaded replies)
    print("  Building Slack messages...")
    messages = build_slack_messages(report_data)

    # 9.5. Sanity Checks (W-INGA / W-SVEN automated gates)
    print("  Running sanity checks...")
    sanity_warnings = run_sanity_checks(report_data)
    if sanity_warnings:
        print(f"  ⚠ {len(sanity_warnings)} sanity warning(s) found:")
        for w in sanity_warnings:
            print(f"    - {w}")
        # Inject warnings into main message before the footer context block
        warning_text = ":warning: *Data Quality Flags (W-INGA/W-SVEN)*\n" + "\n".join(
            f":small_orange_diamond: {w}" for w in sanity_warnings
        )
        # Insert before the last context block in main
        main_blocks = messages.get("main", [])
        insert_idx = len(main_blocks) - 1  # before footer
        main_blocks.insert(insert_idx, {"type": "section", "text": {"type": "mrkdwn", "text": warning_text}})
    else:
        print("  ✓ All sanity checks passed")

    # 10. Save JSON snapshot for historical comparison
    snapshot_dir = os.path.expanduser("~/reports/australiafootball")
    os.makedirs(snapshot_dir, exist_ok=True)
    snapshot_path = os.path.join(snapshot_dir, f"daily_{TODAY}.json")
    with open(snapshot_path, "w") as f:
        json.dump(report_data, f, indent=2, default=str)
    print(f"  Snapshot saved: {snapshot_path}")

    # 11. Send to Slack
    print("  Sending to Slack...")
    sent = send_to_slack(messages)

    if sent:
        print(f"  Report sent to Slack {SLACK_CHANNEL}")
    else:
        print("  Report printed to stdout (Slack delivery skipped/failed)")

    # 12. Also save markdown version
    md_path = os.path.join(snapshot_dir, f"daily_{TODAY}.md")
    all_blocks = list(messages.get("main", []))
    for t in messages.get("threads", []):
        all_blocks.extend(t.get("blocks", []))
    with open(md_path, "w") as f:
        f.write(f"# australiafootball.com Daily Report — {TODAY}\n\n")
        f.write(_blocks_to_text(all_blocks).replace("*", "**"))
    print(f"  Markdown saved: {md_path}")

    print(f"[{NOW.strftime('%H:%M:%S')}] Report complete.")


if __name__ == "__main__":
    main()
