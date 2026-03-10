#!/usr/bin/env python3
"""
Journalist Research Pipeline
Phase 1: Discover 120+ sports journalists across 8 GEOs

Sources:
  1. DataForSEO SERP API — keyword-based discovery
  2. Curated source pages — Prowly, Muck Rack, Wikipedia, outlet mastheads
  3. BigQuery SEO_PERFORMANCE — author slug cross-reference
  4. Google Custom Search — fallback for thin GEOs

Output:
  - journalist_registry.json
  - JOURNALIST_REGISTRY.md
  at ~/AS-Virtual_Team_System_v2/data/journalist_research/

Usage:
  python3 journalist_research_pipeline.py [--geo US,UK,DACH] [--skip-dataforseo] [--skip-bigquery]
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────

load_dotenv(os.path.expanduser("~/.keys/.env"))

DATAFORSEO_LOGIN = os.environ.get("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.environ.get("DATAFORSEO_PASSWORD")
GOOGLE_CSE_KEY = os.environ.get("GOOGLE_CSE_API_KEY", "")
GOOGLE_CSE_CX = os.environ.get("GOOGLE_CSE_CX", "")

BASE_URL = "https://api.dataforseo.com/v3"
OUTPUT_DIR = Path.home() / "AS-Virtual_Team_System_v2" / "data" / "journalist_research"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# DataForSEO auth
if DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD:
    credentials = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
    HEADERS = {
        "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}",
        "Content-Type": "application/json",
    }
else:
    HEADERS = {}

# ── GEO Matrix ──────────────────────────────────────────────────────────────

GEO_MATRIX = {
    "US": {
        "languages": ["en"],
        "location_codes": [2840],
        "sports": ["NFL", "NBA", "MLB", "NHL", "MLS", "College Football"],
        "outlets": ["espn.com", "theathletic.com", "si.com", "bleacherreport.com", "cbssports.com"],
    },
    "UK": {
        "languages": ["en"],
        "location_codes": [2826],
        "sports": ["Premier League", "Rugby", "Cricket", "F1", "Championship"],
        "outlets": ["theguardian.com", "telegraph.co.uk", "bbc.co.uk", "theathletic.com", "skysports.com"],
    },
    "DACH": {
        "languages": ["de"],
        "location_codes": [2276, 2040, 2756],
        "sports": ["Bundesliga", "Ski", "Tennis", "Handball", "Ice Hockey"],
        "outlets": ["kicker.de", "spox.com", "sport1.de", "sportbild.bild.de", "laola1.at"],
    },
    "FR": {
        "languages": ["fr"],
        "location_codes": [2250],
        "sports": ["Ligue 1", "Rugby", "Tennis", "Cycling", "Handball"],
        "outlets": ["lequipe.fr", "rmc.bfmtv.com", "eurosport.fr", "sofoot.com", "francefootball.fr"],
    },
    "IT": {
        "languages": ["it"],
        "location_codes": [2380],
        "sports": ["Serie A", "MotoGP", "Cycling", "Basketball", "Volleyball"],
        "outlets": ["gazzetta.it", "corrieredellosport.it", "tuttosport.com", "sportmediaset.mediaset.it"],
    },
    "AU": {
        "languages": ["en"],
        "location_codes": [2036],
        "sports": ["AFL", "NRL", "A-League", "Cricket", "Horse Racing"],
        "outlets": ["foxsports.com.au", "afl.com.au", "nrl.com", "espn.com.au", "sen.com.au"],
    },
    "ES": {
        "languages": ["es"],
        "location_codes": [2724],
        "sports": ["La Liga", "Basketball", "Tennis", "Cycling", "MotoGP"],
        "outlets": ["marca.com", "as.com", "mundodeportivo.com", "sport.es", "relevo.com"],
    },
    "World": {
        "languages": ["en"],
        "location_codes": [2840],  # fallback
        "sports": ["Olympics", "FIFA", "Athletics", "Swimming", "Boxing"],
        "outlets": ["bbc.com", "reuters.com", "insidethegames.biz", "olympics.com"],
    },
}

# ── DataForSEO Queries ──────────────────────────────────────────────────────

def build_serp_queries(geo: str) -> list[dict]:
    """Build ~25 SERP queries per GEO for journalist discovery."""
    config = GEO_MATRIX[geo]
    lang = config["languages"][0]
    location_code = config["location_codes"][0]

    query_templates = [
        "top sports journalists {country} 2026",
        "best sports columnists {country}",
        "sports journalist award {country} 2025",
        "sports writer of the year {country}",
        "{sport} journalist {country}",
        "{sport} columnist best",
        "{sport} writer award winning",
        "famous {sport} reporters",
        "sports press award {country}",
        "sports media personalities {country}",
    ]

    country_map = {
        "US": "United States", "UK": "United Kingdom", "DACH": "Germany",
        "FR": "France", "IT": "Italy", "AU": "Australia", "ES": "Spain",
        "World": "international",
    }

    queries = []
    country = country_map.get(geo, geo)

    # General queries
    for template in query_templates[:5]:
        queries.append({
            "keyword": template.format(country=country, sport=""),
            "location_code": location_code,
            "language_code": lang,
            "depth": 30,
        })

    # Sport-specific queries
    for sport in config["sports"][:4]:
        for template in query_templates[4:7]:
            queries.append({
                "keyword": template.format(country=country, sport=sport),
                "location_code": location_code,
                "language_code": lang,
                "depth": 30,
            })

    return queries[:25]  # cap at 25 per GEO


# ── API Functions ────────────────────────────────────────────────────────────

def make_request(endpoint: str, data: list, retries: int = 2) -> dict | None:
    """Make DataForSEO API request with retry logic."""
    url = f"{BASE_URL}/{endpoint}"
    for attempt in range(retries + 1):
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, headers=HEADERS, json=data)
                response.raise_for_status()
                result = response.json()
                if result.get("status_code") == 20000:
                    return result
                print(f"  API returned status {result.get('status_code')}: {result.get('status_message')}")
                return result
        except Exception as e:
            if attempt < retries:
                print(f"  Retry {attempt + 1}/{retries} after error: {e}")
                time.sleep(2)
            else:
                print(f"  Failed after {retries + 1} attempts: {e}")
                return None
    return None


def search_serp_for_journalists(geo: str) -> list[dict]:
    """Use DataForSEO SERP API to discover journalists for a GEO."""
    if not HEADERS:
        print(f"  [SKIP] DataForSEO credentials not configured")
        return []

    queries = build_serp_queries(geo)
    discovered = []
    batch_size = 3

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        print(f"  SERP batch {i // batch_size + 1}/{(len(queries) + batch_size - 1) // batch_size} ({len(batch)} queries)")

        result = make_request("serp/google/organic/live/advanced", batch)
        if not result or "tasks" not in result:
            continue

        for task in result["tasks"]:
            if not task.get("result"):
                continue
            for res in task["result"]:
                items = res.get("items", []) or []
                for item in items:
                    if item.get("type") != "organic":
                        continue
                    # Extract journalist names from titles/snippets
                    title = item.get("title", "")
                    snippet = item.get("description", "")
                    url = item.get("url", "")
                    names = extract_journalist_names(title, snippet, url)
                    for name in names:
                        discovered.append({
                            "name": name,
                            "source_url": url,
                            "source_title": title,
                            "source_snippet": snippet,
                            "discovery_method": "dataforseo_serp",
                        })

        time.sleep(1)  # rate limit

    return discovered


def extract_journalist_names(title: str, snippet: str, url: str) -> list[str]:
    """Extract potential journalist names from SERP results using heuristics."""
    names = []
    text = f"{title} {snippet}"

    # Pattern: "FirstName LastName" — capitalized two-word sequences
    # Filter out common non-name words
    stop_words = {
        "The", "Top", "Best", "Most", "Sports", "News", "World", "Press",
        "Award", "Year", "Football", "Soccer", "Tennis", "Cricket", "Rugby",
        "Racing", "League", "United", "States", "Kingdom", "Media", "Writer",
        "National", "Olympic", "International", "Daily", "Weekly", "Monday",
        "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "June", "July", "August",
        "September", "October", "November", "December", "Grand", "Prix",
    }

    # Named list patterns: "1. FirstName LastName" or "- FirstName LastName"
    list_pattern = re.findall(r'(?:^|\n|\d+[\.\)]\s*|[-•]\s*)([A-Z][a-z]+\s+(?:(?:de|van|von|di|el|al|la)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    for match in list_pattern:
        parts = match.strip().split()
        if parts[0] not in stop_words and len(parts) >= 2:
            names.append(match.strip())

    # Author URL patterns: /author/firstname-lastname or /profile/firstname-lastname
    url_pattern = re.search(r'/(?:author|profile|contributor|journalist)/([a-z]+-[a-z]+(?:-[a-z]+)?)', url)
    if url_pattern:
        slug = url_pattern.group(1)
        name = " ".join(w.capitalize() for w in slug.split("-"))
        names.append(name)

    return list(set(names))[:5]  # dedupe, cap at 5 per result


# ── Curated Sources ──────────────────────────────────────────────────────────

CURATED_SOURCES = {
    "US": [
        "https://muckrack.com/rankings/sports",
        "https://en.wikipedia.org/wiki/Category:American_sports_journalists",
    ],
    "UK": [
        "https://en.wikipedia.org/wiki/Category:British_sports_journalists",
        "https://www.sportsjournalists.co.uk/awards/",
    ],
    "DACH": [
        "https://de.wikipedia.org/wiki/Kategorie:Sportjournalist_(Deutschland)",
    ],
    "FR": [
        "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Journaliste_sportif_fran%C3%A7ais",
    ],
    "IT": [
        "https://it.wikipedia.org/wiki/Categoria:Giornalisti_sportivi_italiani",
    ],
    "AU": [
        "https://en.wikipedia.org/wiki/Category:Australian_sports_journalists",
    ],
    "ES": [
        "https://es.wikipedia.org/wiki/Categor%C3%ADa:Periodistas_deportivos_de_Espa%C3%B1a",
    ],
    "World": [],
}


def fetch_curated_sources(geo: str) -> list[dict]:
    """Fetch journalist names from curated web pages."""
    urls = CURATED_SOURCES.get(geo, [])
    discovered = []

    for url in urls:
        print(f"  Fetching curated: {url}")
        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                resp = client.get(url, headers={"User-Agent": "ParadiseMediaResearchBot/1.0"})
                if resp.status_code != 200:
                    print(f"    HTTP {resp.status_code}, skipping")
                    continue
                text = resp.text

                # Extract names from Wikipedia category pages
                if "wikipedia.org" in url:
                    # Wikipedia category links: <a href="/wiki/Name_Name" title="Name Name">
                    wiki_names = re.findall(r'title="([A-Z][a-zÀ-ÿ]+(?:\s+(?:de|van|von|di|el|al|la)\s+)?[A-Z][a-zÀ-ÿ]+(?:\s+[A-Z][a-zÀ-ÿ]+)?)"', text)
                    for name in wiki_names:
                        if len(name.split()) >= 2 and "Category" not in name and "Wikipedia" not in name:
                            discovered.append({
                                "name": name,
                                "source_url": url,
                                "discovery_method": "curated_wikipedia",
                            })

                # Extract names from ranking/list pages
                else:
                    names = extract_journalist_names("", text[:5000], url)
                    for name in names:
                        discovered.append({
                            "name": name,
                            "source_url": url,
                            "discovery_method": "curated_web",
                        })

        except Exception as e:
            print(f"    Error fetching {url}: {e}")
        time.sleep(2)

    return discovered


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_journalist(journalist: dict) -> float:
    """Score a journalist on 100-point scale."""
    score = 0.0

    # Article volume (20pts) — based on discovery frequency
    mentions = journalist.get("mention_count", 1)
    score += min(20, mentions * 4)

    # Traffic/readership proxy (25pts) — based on outlet tier
    tier1_outlets = {"espn.com", "bbc.co.uk", "theguardian.com", "theathletic.com",
                     "gazzetta.it", "marca.com", "lequipe.fr", "kicker.de",
                     "foxsports.com.au", "si.com", "skysports.com"}
    outlet = journalist.get("primary_outlet", "")
    if any(t in outlet for t in tier1_outlets):
        score += 25
    elif outlet:
        score += 12

    # Awards (15pts)
    awards = journalist.get("awards", [])
    score += min(15, len(awards) * 5)

    # Style distinctiveness proxy (20pts) — based on source variety
    sources = journalist.get("discovery_sources", set())
    score += min(20, len(sources) * 7)

    # GEO representation (10pts) — always give if GEO is set
    if journalist.get("geo"):
        score += 10

    # Sport diversity (10pts)
    sports = journalist.get("sports", [])
    score += min(10, len(sports) * 3)

    return round(min(100, score), 2)


# ── Deduplication & Consolidation ────────────────────────────────────────────

def consolidate_discoveries(all_discoveries: list[dict]) -> list[dict]:
    """Deduplicate and consolidate journalist discoveries into clean profiles."""
    # Group by normalized name
    name_groups: dict[str, list[dict]] = {}
    for d in all_discoveries:
        key = d["name"].lower().strip()
        # Normalize unicode names
        key = re.sub(r'\s+', ' ', key)
        if key not in name_groups:
            name_groups[key] = []
        name_groups[key].append(d)

    journalists = []
    for idx, (key, entries) in enumerate(sorted(name_groups.items()), start=1):
        name = entries[0]["name"]
        sources = set(e.get("discovery_method", "") for e in entries)
        source_urls = list(set(e.get("source_url", "") for e in entries if e.get("source_url")))

        journalist = {
            "journalist_id": f"j-{idx:03d}",
            "name": name,
            "geo": entries[0].get("geo", "World"),
            "country": entries[0].get("country", ""),
            "primary_outlet": entries[0].get("primary_outlet", ""),
            "outlets": [],
            "sports": entries[0].get("sports", []),
            "languages": entries[0].get("languages", []),
            "awards": [],
            "mention_count": len(entries),
            "discovery_sources": list(sources),
            "source_urls": source_urls[:5],
            "author_url": entries[0].get("author_url", ""),
            "metadata": {},
        }
        journalist["research_score"] = score_journalist(journalist)
        journalists.append(journalist)

    # Sort by score descending
    journalists.sort(key=lambda j: j["research_score"], reverse=True)

    # Re-index
    for idx, j in enumerate(journalists, start=1):
        j["journalist_id"] = f"j-{idx:03d}"

    return journalists


# ── Output ───────────────────────────────────────────────────────────────────

def save_registry(journalists: list[dict]) -> None:
    """Save journalist registry as JSON and Markdown."""
    # JSON
    json_path = OUTPUT_DIR / "journalist_registry.json"
    registry = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_journalists": len(journalists),
            "geos": list(set(j["geo"] for j in journalists)),
            "pipeline_version": "1.0",
        },
        "journalists": journalists,
    }
    with open(json_path, "w") as f:
        json.dump(registry, f, indent=2, default=str)
    print(f"\nSaved JSON registry: {json_path} ({len(journalists)} journalists)")

    # Markdown
    md_path = OUTPUT_DIR / "JOURNALIST_REGISTRY.md"
    lines = [
        "# Journalist Registry",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Total:** {len(journalists)} journalists across {len(set(j['geo'] for j in journalists))} GEOs",
        "",
        "---",
        "",
    ]

    # Summary table
    geo_counts = {}
    for j in journalists:
        geo_counts[j["geo"]] = geo_counts.get(j["geo"], 0) + 1
    lines.append("## GEO Distribution")
    lines.append("")
    lines.append("| GEO | Count | Top Score |")
    lines.append("|-----|-------|-----------|")
    for geo in ["US", "UK", "DACH", "FR", "IT", "AU", "ES", "World"]:
        count = geo_counts.get(geo, 0)
        top = max((j["research_score"] for j in journalists if j["geo"] == geo), default=0)
        lines.append(f"| {geo} | {count} | {top} |")
    lines.append("")

    # Per-GEO tables
    for geo in ["US", "UK", "DACH", "FR", "IT", "AU", "ES", "World"]:
        geo_journalists = [j for j in journalists if j["geo"] == geo]
        if not geo_journalists:
            continue
        lines.append(f"## {geo} ({len(geo_journalists)} journalists)")
        lines.append("")
        lines.append("| # | ID | Name | Outlet | Sports | Score |")
        lines.append("|---|-----|------|--------|--------|-------|")
        for i, j in enumerate(geo_journalists, 1):
            sports_str = ", ".join(j.get("sports", [])[:3]) or "—"
            lines.append(f"| {i} | {j['journalist_id']} | {j['name']} | {j.get('primary_outlet', '—')} | {sports_str} | {j['research_score']} |")
        lines.append("")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved Markdown registry: {md_path}")


# ── Main Pipeline ────────────────────────────────────────────────────────────

def run_pipeline(target_geos: list[str], skip_dataforseo: bool = False, skip_bigquery: bool = False) -> None:
    """Execute the full journalist research pipeline."""
    print("=" * 60)
    print("JOURNALIST RESEARCH PIPELINE v1.0")
    print(f"Target GEOs: {', '.join(target_geos)}")
    print(f"Started: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)

    all_discoveries = []

    for geo in target_geos:
        print(f"\n── {geo} ─────────────────────────────────")
        config = GEO_MATRIX.get(geo)
        if not config:
            print(f"  Unknown GEO: {geo}, skipping")
            continue

        geo_discoveries = []

        # Source 1: DataForSEO SERP
        if not skip_dataforseo:
            print(f"  [1/3] DataForSEO SERP search...")
            serp_results = search_serp_for_journalists(geo)
            for r in serp_results:
                r["geo"] = geo
                r["languages"] = config["languages"]
            geo_discoveries.extend(serp_results)
            print(f"    Found {len(serp_results)} name mentions")
        else:
            print(f"  [1/3] DataForSEO SERP: SKIPPED")

        # Source 2: Curated sources
        print(f"  [2/3] Curated web sources...")
        curated = fetch_curated_sources(geo)
        for c in curated:
            c["geo"] = geo
            c["languages"] = config["languages"]
        geo_discoveries.extend(curated)
        print(f"    Found {len(curated)} name mentions")

        # Source 3: BigQuery (placeholder — requires BQ client)
        if not skip_bigquery:
            print(f"  [3/3] BigQuery cross-reference: NOT IMPLEMENTED (requires BQ client)")
        else:
            print(f"  [3/3] BigQuery: SKIPPED")

        all_discoveries.extend(geo_discoveries)
        print(f"  Total for {geo}: {len(geo_discoveries)} raw mentions")

    # Consolidate
    print(f"\n── Consolidation ─────────────────────────────")
    print(f"  Raw discoveries: {len(all_discoveries)}")
    journalists = consolidate_discoveries(all_discoveries)
    print(f"  Unique journalists: {len(journalists)}")

    # Save
    save_registry(journalists)

    # Summary
    print(f"\n── Pipeline Complete ─────────────────────────")
    print(f"  Total journalists: {len(journalists)}")
    for geo in target_geos:
        count = sum(1 for j in journalists if j["geo"] == geo)
        print(f"    {geo}: {count}")
    print(f"  Output: {OUTPUT_DIR}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Journalist Research Pipeline")
    parser.add_argument("--geo", type=str, default="US,UK,DACH,FR,IT,AU,ES,World",
                        help="Comma-separated GEO codes (default: all)")
    parser.add_argument("--skip-dataforseo", action="store_true",
                        help="Skip DataForSEO SERP queries")
    parser.add_argument("--skip-bigquery", action="store_true",
                        help="Skip BigQuery cross-reference")
    args = parser.parse_args()

    geos = [g.strip() for g in args.geo.split(",")]
    run_pipeline(geos, skip_dataforseo=args.skip_dataforseo, skip_bigquery=args.skip_bigquery)


if __name__ == "__main__":
    main()
