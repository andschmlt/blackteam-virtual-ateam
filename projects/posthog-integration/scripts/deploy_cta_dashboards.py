#!/usr/bin/env python3
"""
PostHog CTA Performance Dashboard Deployment Script

Deploys CTA Performance dashboards with HogQL insights to PostHog for:
- pokerology.com (Project ID: 266520)
- northeasttimes.com (Project ID: 290039)

Author: B-DASH (BI Developer) | BlackTeam
Version: 1.0.0
Created: 2026-02-04

Reference: /home/andre/projects/posthog-integration/dashboards/CTA_PERFORMANCE_DASHBOARD.md
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

POSTHOG_HOST = "https://us.i.posthog.com"

# Domain configurations
DOMAINS = {
    "pokerology.com": {
        "project_id": 266520,
        "description": "Poker affiliate site - 119,896 CTA visible, 2,556 clicks, 2.1% CTR"
    },
    "northeasttimes.com": {
        "project_id": 290039,
        "description": "Regional news site - 28,016 CTA visible, 617 clicks, 2.2% CTR"
    }
}

# Dashboard insights to create (based on CTA_PERFORMANCE_DASHBOARD.md)
INSIGHTS = {
    "overall_cta_metrics": {
        "name": "Overall CTA Metrics (7-Day)",
        "description": "Executive summary of CTA performance - impressions, clicks, CTR",
        "query": """SELECT
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as total_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as total_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as overall_ctr,
    uniqExact(properties.cta_id) as unique_ctas_tracked,
    uniqExact(properties.page_path) as pages_with_ctas
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY""",
        "display_type": "BoldNumber"
    },
    "cta_by_type": {
        "name": "CTA Performance by Type",
        "description": "Compare CTA types (affiliate, social, newsletter, etc.)",
        "query": """SELECT
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr,
    uniqExact(properties.page_path) as pages_appearing
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY cta_type
ORDER BY impressions DESC""",
        "display_type": "ActionsBarValue"
    },
    "cta_by_url": {
        "name": "CTA Performance by URL (Page-Level)",
        "description": "Identify which pages have best/worst CTA performance",
        "query": """SELECT
    properties.page_path as page_url,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as cta_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as cta_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as page_cta_ctr,
    uniqExact(properties.cta_type) as cta_types_on_page
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY page_url
HAVING cta_impressions > 10
ORDER BY page_cta_ctr DESC
LIMIT 50""",
        "display_type": "ActionsTable"
    },
    "top_performing_ctas": {
        "name": "Top Performing CTAs",
        "description": "Best performing CTA elements by text/href and CTR",
        "query": """SELECT
    properties.cta_text as cta_text,
    properties.cta_href as cta_href,
    properties.cta_type as cta_type,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
AND properties.cta_text != ''
GROUP BY cta_text, cta_href, cta_type
HAVING impressions >= 10
ORDER BY ctr DESC
LIMIT 25""",
        "display_type": "ActionsTable"
    },
    "affiliate_cta_performance": {
        "name": "Affiliate CTA Performance",
        "description": "Track affiliate/monetization CTAs with /go/ URL patterns",
        "query": """SELECT
    properties.cta_text as cta_text,
    properties.cta_href as affiliate_url,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as ctr,
    uniqExact(properties.page_path) as pages_appearing
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
AND (
    properties.cta_href LIKE '%/go/%'
    OR properties.cta_href LIKE '%/out/%'
    OR properties.cta_href LIKE '%affiliate%'
    OR properties.cta_type IN ('affiliate', 'social_twitter', 'social_facebook')
)
GROUP BY cta_text, affiliate_url
ORDER BY clicks DESC
LIMIT 30""",
        "display_type": "ActionsTable"
    },
    "daily_cta_trend": {
        "name": "Daily CTA Trend (7-Day)",
        "description": "Track CTA impressions, clicks, and CTR over time",
        "query": """SELECT
    toDate(timestamp) as date,
    count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END) as daily_impressions,
    count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) as daily_clicks,
    round(
        count(CASE WHEN event = 'navboost:cta_click' THEN 1 END) * 100.0 /
        nullIf(count(CASE WHEN event = 'navboost:cta_visible' THEN 1 END), 0)
    , 2) as daily_ctr
FROM events
WHERE event IN ('navboost:cta_visible', 'navboost:cta_click')
AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY date
ORDER BY date ASC""",
        "display_type": "ActionsLineGraph"
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_api_key() -> str:
    """Load PostHog API key from environment file."""
    env_file = Path.home() / ".keys" / ".env"

    # First try environment variable
    api_key = os.environ.get("POSTHOG_PERSONAL_API_KEY")
    if api_key:
        return api_key

    # Try loading from .env file
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("POSTHOG_PERSONAL_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return api_key

    raise ValueError(
        f"POSTHOG_PERSONAL_API_KEY not found in environment or {env_file}"
    )


def get_headers(api_key: str) -> dict:
    """Get request headers with authorization."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


# Default timeout for all HTTP requests (seconds)
HTTP_TIMEOUT = 60


def check_existing_dashboard(
    api_key: str,
    project_id: int,
    dashboard_name: str
) -> Optional[dict]:
    """
    Check if a dashboard with the given name already exists.

    Args:
        api_key: PostHog personal API key
        project_id: PostHog project ID
        dashboard_name: Name of the dashboard to search for

    Returns:
        Existing dashboard dict if found, None otherwise
    """
    url = f"{POSTHOG_HOST}/api/projects/{project_id}/dashboards/"

    try:
        response = requests.get(
            url,
            headers=get_headers(api_key),
            timeout=HTTP_TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            dashboards = data.get("results", []) if isinstance(data, dict) else data

            for dashboard in dashboards:
                if dashboard.get("name") == dashboard_name:
                    return dashboard

        return None
    except requests.exceptions.Timeout:
        print(f"  [WARNING] Timeout checking existing dashboards")
        return None
    except Exception as e:
        print(f"  [WARNING] Error checking existing dashboards: {e}")
        return None


def create_dashboard(
    api_key: str,
    project_id: int,
    domain: str,
    force: bool = False
) -> Optional[dict]:
    """
    Create a new dashboard in PostHog, or return existing one if it exists.

    Args:
        api_key: PostHog personal API key
        project_id: PostHog project ID
        domain: Domain name for the dashboard
        force: If True, create new dashboard even if one exists

    Returns:
        Dashboard response dict or None on failure
    """
    dashboard_name = f"CTA Performance Dashboard - {domain}"

    # Idempotency check: look for existing dashboard with same name
    if not force:
        print(f"\n[Checking] Existing dashboard for {domain}...")
        existing = check_existing_dashboard(api_key, project_id, dashboard_name)
        if existing:
            print(f"  [FOUND] Dashboard already exists: ID {existing.get('id')}")
            print(f"  [SKIP] Use --force to create a new dashboard anyway")
            return existing

    url = f"{POSTHOG_HOST}/api/projects/{project_id}/dashboards/"

    payload = {
        "name": dashboard_name,
        "description": (
            f"CTA Performance Analysis for {domain}\n"
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Insights: Overall Metrics, By Type, By URL, Top Performers, Affiliate, Daily Trend\n"
            f"Author: B-DASH (BI Developer) | BlackTeam"
        ),
        "pinned": True,
        "tags": ["navboost", "cta", "performance", domain]
    }

    print(f"\n[Creating Dashboard] {domain}")
    print(f"  URL: {url}")
    print(f"  Name: {payload['name']}")

    try:
        response = requests.post(
            url,
            headers=get_headers(api_key),
            json=payload,
            timeout=HTTP_TIMEOUT
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"  [SUCCESS] Dashboard ID: {result.get('id')}")
            return result
        else:
            print(f"  [ERROR] Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print(f"  [ERROR] Request timed out after {HTTP_TIMEOUT}s")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Request failed: {e}")
        return None


def create_insight(
    api_key: str,
    project_id: int,
    dashboard_id: int,
    domain: str,
    insight_key: str,
    insight_config: dict
) -> Optional[dict]:
    """
    Create a HogQL insight in PostHog.

    Args:
        api_key: PostHog personal API key
        project_id: PostHog project ID
        dashboard_id: Dashboard ID to attach insight to
        domain: Domain name for context
        insight_key: Internal key for the insight
        insight_config: Configuration dict with name, description, query

    Returns:
        Insight response dict or None on failure
    """
    url = f"{POSTHOG_HOST}/api/projects/{project_id}/insights/"
    display_type = insight_config.get("display_type", "ActionsTable")

    payload = {
        "name": f"{insight_config['name']} - {domain}",
        "description": insight_config["description"],
        "dashboards": [dashboard_id],
        "query": {
            "kind": "DataTableNode",
            "source": {
                "kind": "HogQLQuery",
                "query": insight_config["query"]
            }
        },
        "tags": ["navboost", "cta", domain, insight_key]
    }

    print(f"\n  [Creating Insight] {insight_key}")
    print(f"    Name: {insight_config['name']}")
    print(f"    Display: {display_type}")

    try:
        response = requests.post(
            url,
            headers=get_headers(api_key),
            json=payload,
            timeout=HTTP_TIMEOUT
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"    [SUCCESS] Insight ID: {result.get('id')}")
            return result
        else:
            print(f"    [ERROR] Status: {response.status_code}")
            print(f"    Response: {response.text[:500]}")
            return None
    except requests.exceptions.Timeout:
        print(f"    [ERROR] Request timed out after {HTTP_TIMEOUT}s")
        return None
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] Request failed: {e}")
        return None


# =============================================================================
# MAIN DEPLOYMENT FUNCTION
# =============================================================================

def deploy_dashboards(dry_run: bool = False, force: bool = False) -> dict:
    """
    Deploy CTA Performance dashboards to PostHog for configured domains.

    Args:
        dry_run: If True, only print what would be done without making API calls
        force: If True, create new dashboards even if they already exist

    Returns:
        Summary dict with deployment results
    """
    print("=" * 70)
    print("PostHog CTA Performance Dashboard Deployment")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Host: {POSTHOG_HOST}")
    print(f"Domains: {', '.join(DOMAINS.keys())}")
    print(f"Insights per dashboard: {len(INSIGHTS)}")
    print(f"Dry Run: {dry_run}")
    print(f"Force: {force}")
    print("=" * 70)

    if dry_run:
        print("\n[DRY RUN MODE] No API calls will be made\n")
        for domain, config in DOMAINS.items():
            print(f"\nWould create dashboard for: {domain}")
            print(f"  Project ID: {config['project_id']}")
            print(f"  Description: {config['description']}")
            print(f"\n  Would create {len(INSIGHTS)} insights:")
            for key, insight in INSIGHTS.items():
                print(f"    - {insight['name']} ({insight['display_type']})")
        return {"status": "dry_run", "domains": list(DOMAINS.keys())}

    # Load API key
    try:
        api_key = load_api_key()
        print(f"\n[OK] API key loaded successfully")
    except ValueError as e:
        print(f"\n[FATAL] {e}")
        return {"status": "error", "message": str(e)}

    results = {
        "status": "completed",
        "timestamp": datetime.now().isoformat(),
        "domains": {}
    }

    # Deploy for each domain
    for domain, config in DOMAINS.items():
        project_id = config["project_id"]
        print(f"\n{'='*70}")
        print(f"DEPLOYING: {domain} (Project: {project_id})")
        print(f"{'='*70}")

        domain_result = {
            "project_id": project_id,
            "dashboard_id": None,
            "insights": []
        }

        # Step 1: Create dashboard (or get existing)
        dashboard = create_dashboard(api_key, project_id, domain, force=force)
        if not dashboard:
            print(f"\n[FAILED] Could not create dashboard for {domain}")
            domain_result["error"] = "Dashboard creation failed"
            results["domains"][domain] = domain_result
            continue

        dashboard_id = dashboard["id"]
        domain_result["dashboard_id"] = dashboard_id

        # Step 2: Create insights
        for insight_key, insight_config in INSIGHTS.items():
            insight = create_insight(
                api_key,
                project_id,
                dashboard_id,
                domain,
                insight_key,
                insight_config
            )

            if insight:
                domain_result["insights"].append({
                    "key": insight_key,
                    "id": insight["id"],
                    "name": insight_config["name"],
                    "status": "created"
                })
            else:
                domain_result["insights"].append({
                    "key": insight_key,
                    "name": insight_config["name"],
                    "status": "failed"
                })

        results["domains"][domain] = domain_result

    # Summary
    print("\n" + "=" * 70)
    print("DEPLOYMENT SUMMARY")
    print("=" * 70)

    for domain, result in results["domains"].items():
        success_count = sum(1 for i in result.get("insights", []) if i.get("status") == "created")
        total_count = len(result.get("insights", []))
        dashboard_id = result.get("dashboard_id", "N/A")

        print(f"\n{domain}:")
        print(f"  Dashboard ID: {dashboard_id}")
        print(f"  Insights: {success_count}/{total_count} created successfully")

        if dashboard_id and dashboard_id != "N/A":
            print(f"  View: {POSTHOG_HOST}/project/{result['project_id']}/dashboard/{dashboard_id}")

    print("\n" + "=" * 70)

    return results


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Deploy CTA Performance dashboards to PostHog"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without making API calls"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Create new dashboards even if they already exist"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path for deployment results JSON"
    )

    args = parser.parse_args()

    # Run deployment
    results = deploy_dashboards(dry_run=args.dry_run, force=args.force)

    # Save results if output path specified
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")

    # Exit with appropriate code
    if results.get("status") == "error":
        exit(1)
    exit(0)
