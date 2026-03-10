"""
DataForSEO Canada iGaming/Poker SERP Research
Virtual ATeam: B-RANK (SEO Commander) + B-ALEX (Insight) + B-FORG (DataForge)

Research targets:
- Poker news & tournaments
- iGaming industry news
- Casino updates & openings
- Online gambling legislation & politics
- Player statistics & trends
- Sports betting (related vertical)

GEO: Canada (location_code=2124)
"""

import httpx
import base64
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.keys/.env"))

LOGIN = os.environ.get("DATAFORSEO_LOGIN")
PASSWORD = os.environ.get("DATAFORSEO_PASSWORD")

if not LOGIN or not PASSWORD:
    raise ValueError("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set in ~/.keys/.env")

credentials = f"{LOGIN}:{PASSWORD}"
encoded = base64.b64encode(credentials.encode()).decode()
HEADERS = {
    "Authorization": f"Basic {encoded}",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.dataforseo.com/v3"
LOCATION_CODE_CANADA = 2124

# ============================================================
# SEED KEYWORDS - Organized by research topic group
# ============================================================
SEED_KEYWORDS = {
    "poker_news": [
        "poker news",
        "poker news today",
        "poker tournament results",
        "wsop 2026",
        "wsop results",
        "world series of poker",
        "poker player rankings",
        "online poker news",
        "poker strategy news",
        "poker industry news",
    ],
    "poker_tournaments": [
        "poker tournaments canada",
        "poker tournaments near me",
        "poker tournaments ontario",
        "live poker tournaments",
        "online poker tournaments",
        "poker tournament schedule 2026",
        "wsop schedule",
        "wpt tournaments",
        "poker championship",
        "freeroll poker tournaments",
    ],
    "igaming_industry": [
        "igaming news",
        "igaming industry",
        "online gambling industry",
        "igaming companies",
        "igaming market size",
        "igaming trends 2026",
        "online gambling market",
        "gaming industry news",
        "gambling news",
        "igaming revenue",
    ],
    "casino_updates": [
        "new casino opening",
        "casino news",
        "casino news canada",
        "online casino news",
        "new casino canada",
        "casino updates",
        "casino industry news",
        "casino expansion",
        "resort casino opening",
        "casino reviews",
    ],
    "legislation_politics": [
        "online gambling legislation canada",
        "igaming regulation canada",
        "online casino laws ontario",
        "gambling regulation news",
        "online gambling bill",
        "single event betting canada",
        "igaming ontario",
        "gambling politics",
        "online gambling legalization",
        "gambling regulation 2026",
    ],
    "player_statistics": [
        "online gambling statistics canada",
        "poker statistics",
        "casino statistics canada",
        "gambling demographics canada",
        "online gambling growth",
        "igaming statistics 2026",
        "poker player stats",
        "gambling revenue canada",
        "sports betting statistics canada",
        "online casino players",
    ],
    "sports_betting_related": [
        "sports betting canada",
        "sports betting news",
        "online sports betting ontario",
        "best sportsbooks canada",
        "sports betting legislation",
        "bet365 canada",
        "proline sports betting",
        "nhl betting",
        "cfl betting",
        "sports betting tips",
    ],
}


def make_request(endpoint, data, retries=2):
    """Make DataForSEO API request with retry."""
    url = f"{BASE_URL}/{endpoint}"
    for attempt in range(retries + 1):
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, headers=HEADERS, json=data)
                response.raise_for_status()
                result = response.json()
                if result.get("status_code") == 20000:
                    return result
                else:
                    print(f"  API warning: {result.get('status_message', 'unknown')}")
                    return result
        except Exception as e:
            if attempt < retries:
                print(f"  Retry {attempt+1}/{retries} after error: {e}")
                time.sleep(2)
            else:
                print(f"  FAILED after {retries} retries: {e}")
                return None
    return None


def get_search_volumes(keywords, location_code=LOCATION_CODE_CANADA):
    """Get search volume + keyword difficulty for a batch of keywords."""
    data = [{
        "keywords": keywords,
        "location_code": location_code,
        "language_code": "en",
        "date_from": "2025-08-01",
        "date_to": "2026-02-01",
    }]
    return make_request("keywords_data/google_ads/search_volume/live", data)


def get_keyword_suggestions(seed_keyword, location_code=LOCATION_CODE_CANADA, limit=20):
    """Get related keyword suggestions from DataForSEO."""
    data = [{
        "keyword": seed_keyword,
        "location_code": location_code,
        "language_code": "en",
        "include_seed_keyword": True,
        "limit": limit,
    }]
    return make_request("keywords_data/google_ads/keywords_for_keywords/live", data)


def get_serp_top10(keyword, location_code=LOCATION_CODE_CANADA):
    """Get top 10 SERP results for a keyword."""
    data = [{
        "keyword": keyword,
        "location_code": location_code,
        "language_code": "en",
        "depth": 10,
    }]
    return make_request("serp/google/organic/live/regular", data)


def extract_search_volume_data(response):
    """Extract search volume data from API response."""
    results = []
    if not response or "tasks" not in response:
        return results

    for task in response.get("tasks", []):
        if task.get("result"):
            for item in task["result"]:
                results.append({
                    "keyword": item.get("keyword", ""),
                    "search_volume": item.get("search_volume", 0),
                    "competition": item.get("competition", 0),
                    "competition_level": item.get("competition_level", ""),
                    "cpc": item.get("cpc", 0),
                    "monthly_searches": item.get("monthly_searches", []),
                })
    return results


def extract_keyword_suggestions(response):
    """Extract keyword suggestions from API response."""
    results = []
    if not response or "tasks" not in response:
        return results

    for task in response.get("tasks", []):
        if task.get("result"):
            for item in task["result"]:
                results.append({
                    "keyword": item.get("keyword", ""),
                    "search_volume": item.get("search_volume", 0),
                    "competition": item.get("competition", 0),
                    "competition_level": item.get("competition_level", ""),
                    "cpc": item.get("cpc", 0),
                })
    return results


def extract_serp_results(response):
    """Extract SERP top 10 results from API response."""
    results = []
    if not response or "tasks" not in response:
        return results

    for task in response.get("tasks", []):
        if task.get("result"):
            for result_set in task["result"]:
                items = result_set.get("items", [])
                for item in items:
                    if item.get("type") == "organic":
                        results.append({
                            "position": item.get("rank_absolute", 0),
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "domain": item.get("domain", ""),
                            "description": item.get("description", ""),
                        })
    return results[:10]


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    print("=" * 70)
    print("DataForSEO Canada iGaming/Poker SERP Research")
    print(f"GEO: Canada (location_code={LOCATION_CODE_CANADA})")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    all_results = {}
    all_suggestions = {}
    serp_analyses = {}

    # ---- STEP 1: Search Volumes for all seed keyword groups ----
    print("\n[STEP 1] Fetching search volumes for all keyword groups...")

    for group_name, keywords in SEED_KEYWORDS.items():
        print(f"\n  Group: {group_name} ({len(keywords)} keywords)")
        response = get_search_volumes(keywords)
        data = extract_search_volume_data(response)
        all_results[group_name] = sorted(data, key=lambda x: x.get("search_volume", 0) or 0, reverse=True)

        for kw in all_results[group_name]:
            vol = kw.get("search_volume", 0) or 0
            comp = kw.get("competition_level", "N/A")
            cpc = kw.get("cpc", 0) or 0
            print(f"    {kw['keyword']:45s} Vol: {vol:>8,}  Comp: {comp:>8}  CPC: ${cpc:.2f}")

        time.sleep(0.5)  # Rate limiting

    # ---- STEP 2: Keyword suggestions for top keywords per group ----
    print("\n\n[STEP 2] Fetching keyword suggestions for top keywords...")

    top_seeds = []
    for group_name, kw_data in all_results.items():
        if kw_data:
            top_kw = kw_data[0]["keyword"]
            top_seeds.append((group_name, top_kw))

    for group_name, seed_kw in top_seeds:
        print(f"\n  Suggestions for '{seed_kw}' (group: {group_name}):")
        response = get_keyword_suggestions(seed_kw, limit=15)
        suggestions = extract_keyword_suggestions(response)
        all_suggestions[group_name] = suggestions

        for s in suggestions[:10]:
            vol = s.get("search_volume", 0) or 0
            print(f"    {s['keyword']:45s} Vol: {vol:>8,}")

        time.sleep(0.5)

    # ---- STEP 3: SERP analysis for highest volume keywords ----
    print("\n\n[STEP 3] SERP Top 10 analysis for highest-volume keywords...")

    # Pick top keyword from each group for SERP analysis
    serp_targets = []
    for group_name, kw_data in all_results.items():
        for kw in kw_data[:2]:  # Top 2 per group
            if (kw.get("search_volume") or 0) > 0:
                serp_targets.append((group_name, kw["keyword"], kw.get("search_volume", 0)))

    # Sort by volume, take top 10 overall
    serp_targets.sort(key=lambda x: x[2] or 0, reverse=True)
    serp_targets = serp_targets[:10]

    for group_name, keyword, vol in serp_targets:
        print(f"\n  SERP for '{keyword}' (Vol: {vol:,}, Group: {group_name}):")
        response = get_serp_top10(keyword)
        serp_items = extract_serp_results(response)
        serp_analyses[keyword] = {
            "group": group_name,
            "volume": vol,
            "results": serp_items,
        }

        for item in serp_items:
            print(f"    #{item['position']:>2} | {item['domain']:35s} | {item['title'][:60]}")

        time.sleep(0.5)

    # ---- STEP 4: Save comprehensive results ----
    output = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "geo": "Canada",
            "location_code": LOCATION_CODE_CANADA,
            "total_keywords_researched": sum(len(v) for v in all_results.values()),
        },
        "search_volumes_by_group": {
            group: [
                {
                    "keyword": kw["keyword"],
                    "search_volume": kw.get("search_volume", 0),
                    "competition": kw.get("competition", 0),
                    "competition_level": kw.get("competition_level", ""),
                    "cpc": kw.get("cpc", 0),
                }
                for kw in kw_data
            ]
            for group, kw_data in all_results.items()
        },
        "keyword_suggestions_by_group": {
            group: [
                {
                    "keyword": s["keyword"],
                    "search_volume": s.get("search_volume", 0),
                    "competition_level": s.get("competition_level", ""),
                }
                for s in suggestions
            ]
            for group, suggestions in all_suggestions.items()
        },
        "serp_analyses": {
            kw: {
                "group": data["group"],
                "volume": data["volume"],
                "top_10": [
                    {
                        "position": r["position"],
                        "domain": r["domain"],
                        "title": r["title"],
                        "url": r["url"],
                    }
                    for r in data["results"]
                ],
            }
            for kw, data in serp_analyses.items()
        },
    }

    output_path = os.path.expanduser("~/reports/dataforseo_canada_igaming_research.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n\nFull results saved to: {output_path}")

    # ---- STEP 5: Print summary analysis ----
    print("\n\n" + "=" * 70)
    print("SUMMARY: Top Keywords by Group (Canada GEO)")
    print("=" * 70)

    for group_name, kw_data in all_results.items():
        print(f"\n### {group_name.upper().replace('_', ' ')}")
        for kw in kw_data[:5]:
            vol = kw.get("search_volume", 0) or 0
            comp = kw.get("competition_level", "N/A")
            cpc = kw.get("cpc", 0) or 0
            print(f"  {kw['keyword']:45s} | Vol: {vol:>8,} | Comp: {comp:>8} | CPC: ${cpc:.2f}")

    print("\n\n" + "=" * 70)
    print("DOMINANT DOMAINS in Canada iGaming SERPs")
    print("=" * 70)

    domain_frequency = {}
    for kw, data in serp_analyses.items():
        for r in data["results"]:
            domain = r["domain"]
            if domain not in domain_frequency:
                domain_frequency[domain] = {"count": 0, "keywords": []}
            domain_frequency[domain]["count"] += 1
            domain_frequency[domain]["keywords"].append(kw)

    sorted_domains = sorted(domain_frequency.items(), key=lambda x: x[1]["count"], reverse=True)
    for domain, info in sorted_domains[:20]:
        kws = ", ".join(info["keywords"][:3])
        print(f"  {domain:40s} | Appears {info['count']:>2}x | Keywords: {kws}")

    print("\n\n" + "=" * 70)
    print("ADDITIONAL SUGGESTED TOPICS (from keyword suggestions)")
    print("=" * 70)

    all_new_suggestions = []
    existing_keywords = set()
    for kw_data in all_results.values():
        for kw in kw_data:
            existing_keywords.add(kw["keyword"].lower())

    for group, suggestions in all_suggestions.items():
        for s in suggestions:
            if s["keyword"].lower() not in existing_keywords and (s.get("search_volume") or 0) > 0:
                all_new_suggestions.append({
                    "keyword": s["keyword"],
                    "search_volume": s.get("search_volume", 0),
                    "source_group": group,
                })

    all_new_suggestions.sort(key=lambda x: x.get("search_volume", 0) or 0, reverse=True)
    for s in all_new_suggestions[:30]:
        vol = s.get("search_volume", 0) or 0
        print(f"  {s['keyword']:45s} | Vol: {vol:>8,} | From: {s['source_group']}")

    print(f"\n\nResearch complete. Total API calls estimated: ~{len(SEED_KEYWORDS) + len(top_seeds) + len(serp_targets)}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
