#!/usr/bin/env python3
"""
PostHog Conversion Funnel Deployment Script
============================================

Deploys pre-configured conversion funnels to PostHog for specified domains.

Target Domains:
- pokerology.com (Project ID: 266520) - Affiliate/Poker
- northeasttimes.com (Project ID: 290039) - News/iGaming

Funnels Deployed:
1. Affiliate Conversion Funnel - Landing -> CTA Visible -> CTA Click -> Affiliate Click
2. Article Engagement Funnel - Pageview -> 25% Scroll -> 50% Scroll -> 75% Scroll
3. CTA Effectiveness Funnel - CTA Visible -> CTA Click -> Outbound Click

Reference: CONVERSION_FUNNEL_TEMPLATES.md

Usage:
    python deploy_conversion_funnels.py [--dry-run] [--domain DOMAIN] [--verbose]

    # Deploy to all configured domains
    python deploy_conversion_funnels.py

    # Dry run (show what would be created)
    python deploy_conversion_funnels.py --dry-run

    # Deploy to specific domain only
    python deploy_conversion_funnels.py --domain pokerology.com

Author: B-DANA (DataViz) | BlackTeam
Created: 2026-02-04
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Any

# ============================================================================
# CONFIGURATION
# ============================================================================

POSTHOG_HOST = "https://us.i.posthog.com"

# Target domains with their PostHog project IDs
DOMAINS = {
    "pokerology.com": {
        "project_id": "266520",
        "vertical": "Affiliate/Poker",
        "description": "Poker affiliate site with /go/ URL pattern"
    },
    "northeasttimes.com": {
        "project_id": "290039",
        "vertical": "News/iGaming",
        "description": "News site with iGaming affiliate links"
    }
}

# ============================================================================
# FUNNEL CONFIGURATIONS
# ============================================================================

def get_funnel_configs(domain: str) -> List[Dict]:
    """
    Return funnel configurations for a given domain.

    Each funnel follows the PostHog Insight API structure with FunnelsQuery kind.
    """

    funnels = []

    # -------------------------------------------------------------------------
    # Funnel 1: Affiliate Conversion Funnel (Most Important)
    # -------------------------------------------------------------------------
    # Purpose: Track the complete affiliate conversion journey
    # Question: "What percentage of visitors end up clicking an affiliate link?"

    affiliate_funnel = {
        "name": f"Affiliate Conversion Funnel - {domain}",
        "description": "Tracks visitor journey from landing to affiliate click. "
                      "Steps: Pageview -> CTA Visible -> CTA Click -> Affiliate Outbound",
        "tags": ["navboost", "affiliate", "conversion", "funnel", domain],
        "query": {
            "kind": "FunnelsQuery",
            "series": [
                {
                    "kind": "EventsNode",
                    "event": "$pageview",
                    "name": "Page View"
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:cta_visible",
                    "name": "CTA Seen"
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:cta_click",
                    "name": "CTA Clicked"
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:outbound_click",
                    "name": "Affiliate Click",
                    "properties": [
                        {
                            "key": "is_affiliate",
                            "value": True,
                            "operator": "exact",
                            "type": "event"
                        }
                    ]
                }
            ],
            "funnelsFilter": {
                "funnelWindowInterval": 1,
                "funnelWindowIntervalUnit": "day",
                "funnelOrderType": "ordered",
                "funnelVizType": "steps"
            },
            "breakdownFilter": {
                "breakdown": "$pathname",
                "breakdown_type": "event"
            },
            "filterTestAccounts": True,
            "dateRange": {
                "date_from": "-7d",
                "date_to": None
            },
            "properties": {
                "type": "AND",
                "values": [
                    {
                        "type": "AND",
                        "values": [
                            {
                                "key": "$host",
                                "value": domain,
                                "operator": "exact",
                                "type": "event"
                            }
                        ]
                    }
                ]
            }
        }
    }
    funnels.append(affiliate_funnel)

    # -------------------------------------------------------------------------
    # Funnel 2: Article Engagement Funnel
    # -------------------------------------------------------------------------
    # Purpose: Track content consumption depth
    # Question: "How many visitors actually read our articles vs. bounce?"

    engagement_funnel = {
        "name": f"Article Engagement Funnel - {domain}",
        "description": "Tracks how deep users scroll into article content. "
                      "Steps: Pageview -> 25% Scroll -> 50% Scroll -> 75% Scroll",
        "tags": ["navboost", "engagement", "scroll", "content", "funnel", domain],
        "query": {
            "kind": "FunnelsQuery",
            "series": [
                {
                    "kind": "EventsNode",
                    "event": "$pageview",
                    "name": "Article View",
                    "properties": [
                        {
                            "key": "$pathname",
                            "value": "^/\\d{4}/|/news/|/article/",
                            "operator": "regex",
                            "type": "event"
                        }
                    ]
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:scroll_zone",
                    "name": "Scrolled to 25%",
                    "properties": [
                        {
                            "key": "scroll_depth_percent",
                            "value": 25,
                            "operator": "exact",
                            "type": "event"
                        }
                    ]
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:scroll_zone",
                    "name": "Scrolled to 50%",
                    "properties": [
                        {
                            "key": "scroll_depth_percent",
                            "value": 50,
                            "operator": "exact",
                            "type": "event"
                        }
                    ]
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:scroll_zone",
                    "name": "Scrolled to 75%",
                    "properties": [
                        {
                            "key": "scroll_depth_percent",
                            "value": 75,
                            "operator": "exact",
                            "type": "event"
                        }
                    ]
                }
            ],
            "funnelsFilter": {
                "funnelWindowInterval": 1,
                "funnelWindowIntervalUnit": "day",
                "funnelOrderType": "ordered",
                "funnelVizType": "steps"
            },
            "filterTestAccounts": True,
            "dateRange": {
                "date_from": "-7d",
                "date_to": None
            },
            "properties": {
                "type": "AND",
                "values": [
                    {
                        "type": "AND",
                        "values": [
                            {
                                "key": "$host",
                                "value": domain,
                                "operator": "exact",
                                "type": "event"
                            }
                        ]
                    }
                ]
            }
        }
    }
    funnels.append(engagement_funnel)

    # -------------------------------------------------------------------------
    # Funnel 4: CTA Effectiveness Funnel
    # -------------------------------------------------------------------------
    # Purpose: Measure CTA-to-conversion journey
    # Question: "How effective are our CTAs at driving outbound clicks?"

    cta_funnel = {
        "name": f"CTA Effectiveness Funnel - {domain}",
        "description": "Measures how effectively CTAs convert to outbound clicks. "
                      "Steps: CTA Visible -> CTA Click -> Outbound Click",
        "tags": ["navboost", "cta", "effectiveness", "funnel", domain],
        "query": {
            "kind": "FunnelsQuery",
            "series": [
                {
                    "kind": "EventsNode",
                    "event": "navboost:cta_visible",
                    "name": "CTA Viewed"
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:cta_click",
                    "name": "CTA Clicked"
                },
                {
                    "kind": "EventsNode",
                    "event": "navboost:outbound_click",
                    "name": "Outbound Click"
                }
            ],
            "funnelsFilter": {
                "funnelWindowInterval": 1,
                "funnelWindowIntervalUnit": "day",
                "funnelOrderType": "ordered",
                "funnelVizType": "steps"
            },
            "breakdownFilter": {
                "breakdown": "cta_type",
                "breakdown_type": "event"
            },
            "filterTestAccounts": True,
            "dateRange": {
                "date_from": "-7d",
                "date_to": None
            },
            "properties": {
                "type": "AND",
                "values": [
                    {
                        "type": "AND",
                        "values": [
                            {
                                "key": "$host",
                                "value": domain,
                                "operator": "exact",
                                "type": "event"
                            }
                        ]
                    }
                ]
            }
        }
    }
    funnels.append(cta_funnel)

    return funnels


# ============================================================================
# API UTILITIES
# ============================================================================

def get_api_key() -> str:
    """Get PostHog API key from environment or file."""
    # Check multiple environment variable names
    for key_name in ['POSTHOG_PERSONAL_API_KEY', 'POSTHOG_API_KEY', 'POSTHOG_PROJECT_API_KEY']:
        api_key = os.environ.get(key_name)
        if api_key:
            return api_key

    # Try to load from ~/.keys/.env file
    env_file = os.path.expanduser('~/.keys/.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Check multiple key names in file
                for key_name in ['POSTHOG_PERSONAL_API_KEY', 'POSTHOG_API_KEY', 'POSTHOG_PROJECT_API_KEY']:
                    if line.startswith(f'{key_name}='):
                        value = line.split('=', 1)[1].strip('"\'')
                        return value

    raise ValueError(
        "PostHog API key not found. Set POSTHOG_PERSONAL_API_KEY environment variable "
        "or add it to ~/.keys/.env"
    )


def posthog_api_request(
    method: str,
    endpoint: str,
    project_id: str,
    api_key: str,
    data: Optional[Dict] = None
) -> Dict:
    """Make an authenticated request to the PostHog API."""

    url = f"{POSTHOG_HOST}/api/projects/{project_id}/{endpoint}"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    body = json.dumps(data).encode('utf-8') if data else None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            response_body = response.read().decode()
            if response_body:
                return json.loads(response_body)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else 'No error body'
        raise Exception(f"PostHog API error {e.code}: {error_body}")


def create_insight(
    project_id: str,
    api_key: str,
    insight_config: Dict,
    verbose: bool = False
) -> Dict:
    """Create a new insight (funnel) in PostHog."""

    # Build the insight payload
    payload = {
        "name": insight_config["name"],
        "description": insight_config.get("description", ""),
        "tags": insight_config.get("tags", []),
        "query": insight_config["query"],
        "saved": True
    }

    if verbose:
        print(f"    Payload: {json.dumps(payload, indent=2)[:500]}...")

    result = posthog_api_request(
        method="POST",
        endpoint="insights/",
        project_id=project_id,
        api_key=api_key,
        data=payload
    )

    return result


def list_existing_insights(
    project_id: str,
    api_key: str,
    search: Optional[str] = None
) -> List[Dict]:
    """List existing insights in a project."""

    endpoint = "insights/"
    if search:
        endpoint += f"?search={urllib.parse.quote(search)}"

    result = posthog_api_request(
        method="GET",
        endpoint=endpoint,
        project_id=project_id,
        api_key=api_key
    )

    return result.get("results", [])


# Need to import urllib.parse for URL encoding
import urllib.parse


# ============================================================================
# DEPLOYMENT LOGIC
# ============================================================================

class FunnelDeployer:
    """Handles deployment of funnels to PostHog."""

    def __init__(self, api_key: str, verbose: bool = False, dry_run: bool = False):
        self.api_key = api_key
        self.verbose = verbose
        self.dry_run = dry_run
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "mode": "dry_run" if dry_run else "deploy",
            "domains": {}
        }

    def log(self, message: str, level: str = "info"):
        """Print log message."""
        prefix = {
            "info": "  ",
            "success": "  [OK]",
            "error": "  [ERROR]",
            "warning": "  [WARN]",
            "debug": "  [DEBUG]"
        }.get(level, "  ")

        if level == "debug" and not self.verbose:
            return

        print(f"{prefix} {message}")

    def check_existing_funnels(self, project_id: str, domain: str) -> Dict[str, bool]:
        """Check which funnels already exist for a domain."""

        existing = {}

        try:
            insights = list_existing_insights(project_id, self.api_key, search=domain)

            for insight in insights:
                name = insight.get("name", "")
                if "Affiliate Conversion Funnel" in name:
                    existing["affiliate"] = True
                elif "Article Engagement Funnel" in name:
                    existing["engagement"] = True
                elif "CTA Effectiveness Funnel" in name:
                    existing["cta"] = True
        except Exception as e:
            self.log(f"Could not check existing funnels: {e}", "warning")

        return existing

    def deploy_domain(self, domain: str, domain_config: Dict) -> Dict:
        """Deploy funnels to a single domain."""

        project_id = domain_config["project_id"]
        vertical = domain_config["vertical"]

        print(f"\n{'='*60}")
        print(f"DEPLOYING: {domain}")
        print(f"Project ID: {project_id}")
        print(f"Vertical: {vertical}")
        print('='*60)

        domain_results = {
            "project_id": project_id,
            "vertical": vertical,
            "funnels_created": [],
            "funnels_skipped": [],
            "errors": []
        }

        # Check for existing funnels
        self.log("Checking for existing funnels...", "info")
        existing = self.check_existing_funnels(project_id, domain)

        if existing:
            self.log(f"Found existing funnels: {list(existing.keys())}", "info")

        # Get funnel configurations
        funnels = get_funnel_configs(domain)

        for funnel in funnels:
            funnel_name = funnel["name"]
            funnel_type = funnel_name.split(" - ")[0]  # e.g., "Affiliate Conversion Funnel"

            print(f"\n  Funnel: {funnel_name}")

            # Check if already exists
            type_key = None
            if "Affiliate" in funnel_type:
                type_key = "affiliate"
            elif "Engagement" in funnel_type:
                type_key = "engagement"
            elif "CTA" in funnel_type:
                type_key = "cta"

            if type_key and existing.get(type_key):
                self.log(f"Skipping - already exists", "warning")
                domain_results["funnels_skipped"].append(funnel_name)
                continue

            # Deploy or dry run
            if self.dry_run:
                self.log(f"[DRY RUN] Would create funnel", "info")
                self.log(f"Steps: {len(funnel['query']['series'])}", "debug")
                domain_results["funnels_created"].append({
                    "name": funnel_name,
                    "status": "dry_run",
                    "steps": len(funnel['query']['series'])
                })
            else:
                try:
                    self.log("Creating funnel...", "info")
                    result = create_insight(
                        project_id=project_id,
                        api_key=self.api_key,
                        insight_config=funnel,
                        verbose=self.verbose
                    )

                    insight_id = result.get("id") or result.get("short_id")
                    self.log(f"Created successfully (ID: {insight_id})", "success")

                    domain_results["funnels_created"].append({
                        "name": funnel_name,
                        "status": "created",
                        "id": insight_id,
                        "short_id": result.get("short_id")
                    })

                except Exception as e:
                    self.log(f"Failed: {e}", "error")
                    domain_results["errors"].append({
                        "funnel": funnel_name,
                        "error": str(e)
                    })

        # Summary for domain
        print(f"\n  Summary for {domain}:")
        print(f"    Created: {len([f for f in domain_results['funnels_created'] if f.get('status') != 'dry_run'])}")
        print(f"    Skipped: {len(domain_results['funnels_skipped'])}")
        print(f"    Errors: {len(domain_results['errors'])}")

        return domain_results

    def deploy_all(self, domains: Optional[List[str]] = None) -> Dict:
        """Deploy funnels to all configured domains."""

        target_domains = domains or list(DOMAINS.keys())

        print("\n" + "="*60)
        print("POSTHOG CONVERSION FUNNEL DEPLOYMENT")
        print("="*60)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'DEPLOY'}")
        print(f"Target Domains: {', '.join(target_domains)}")
        print(f"Funnels per Domain: 3")

        for domain in target_domains:
            if domain not in DOMAINS:
                self.log(f"Unknown domain: {domain}", "error")
                continue

            domain_results = self.deploy_domain(domain, DOMAINS[domain])
            self.results["domains"][domain] = domain_results

        # Final summary
        print("\n" + "="*60)
        print("DEPLOYMENT SUMMARY")
        print("="*60)

        total_created = 0
        total_skipped = 0
        total_errors = 0

        for domain, results in self.results["domains"].items():
            created = len([f for f in results['funnels_created'] if f.get('status') != 'dry_run'])
            skipped = len(results['funnels_skipped'])
            errors = len(results['errors'])

            total_created += created
            total_skipped += skipped
            total_errors += errors

            status = "[OK]" if errors == 0 else "[ERRORS]"
            print(f"  {domain}: {created} created, {skipped} skipped, {errors} errors {status}")

        print(f"\n  TOTAL: {total_created} created, {total_skipped} skipped, {total_errors} errors")

        if self.dry_run:
            print("\n  NOTE: This was a dry run. No changes were made.")
            print("  Run without --dry-run to deploy funnels.")

        return self.results


# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Deploy PostHog Conversion Funnels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run (preview what will be created)
    python deploy_conversion_funnels.py --dry-run

    # Deploy to all domains
    python deploy_conversion_funnels.py

    # Deploy to specific domain
    python deploy_conversion_funnels.py --domain pokerology.com

    # Verbose output
    python deploy_conversion_funnels.py --verbose

Configured Domains:
    - pokerology.com (Project ID: 266520) - Affiliate/Poker
    - northeasttimes.com (Project ID: 290039) - News/iGaming

Funnels Deployed:
    1. Affiliate Conversion Funnel
       Steps: Pageview -> CTA Visible -> CTA Click -> Affiliate Outbound

    2. Article Engagement Funnel
       Steps: Article View -> 25% Scroll -> 50% Scroll -> 75% Scroll

    3. CTA Effectiveness Funnel
       Steps: CTA Visible -> CTA Click -> Outbound Click
"""
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be created without making changes'
    )
    parser.add_argument(
        '--domain',
        type=str,
        help='Deploy to a specific domain only'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output including API payloads'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Save results to JSON file'
    )
    parser.add_argument(
        '--list-domains',
        action='store_true',
        help='List configured domains and exit'
    )

    args = parser.parse_args()

    # List domains option
    if args.list_domains:
        print("Configured Domains:")
        for domain, config in DOMAINS.items():
            print(f"  - {domain}")
            print(f"      Project ID: {config['project_id']}")
            print(f"      Vertical: {config['vertical']}")
            print(f"      Description: {config['description']}")
        sys.exit(0)

    # Get API key
    try:
        api_key = get_api_key()
        if args.verbose:
            print(f"API Key loaded: {api_key[:8]}...{api_key[-4:]}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Determine target domains
    target_domains = None
    if args.domain:
        if args.domain not in DOMAINS:
            print(f"Error: Unknown domain '{args.domain}'")
            print(f"Available domains: {', '.join(DOMAINS.keys())}")
            sys.exit(1)
        target_domains = [args.domain]

    # Deploy funnels
    deployer = FunnelDeployer(
        api_key=api_key,
        verbose=args.verbose,
        dry_run=args.dry_run
    )

    results = deployer.deploy_all(domains=target_domains)

    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    # Exit code based on errors
    total_errors = sum(len(d.get('errors', [])) for d in results.get('domains', {}).values())
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
