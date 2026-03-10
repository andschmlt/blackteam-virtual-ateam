#!/usr/bin/env python3
"""
Article Scraper — Phase 2
Collect top articles per journalist from the registry.

Sources (priority order):
  1. DataForSEO SERP: "[journalist name]" site:[outlet]
  2. Author page scraping via httpx
  3. Google News via DataForSEO
  4. Personal sites / Substacks

Stack: httpx + beautifulsoup4
Rate limiting: 2-second delay per domain, respects robots.txt

Usage:
  python3 article_scraper.py [--registry path] [--max-per-journalist 100] [--skip-scrape]
"""

import argparse
import base64
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────

load_dotenv(os.path.expanduser("~/.keys/.env"))

DATAFORSEO_LOGIN = os.environ.get("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.environ.get("DATAFORSEO_PASSWORD")
BASE_URL = "https://api.dataforseo.com/v3"

OUTPUT_DIR = Path.home() / "AS-Virtual_Team_System_v2" / "data" / "journalist_research"
ARTICLES_DIR = OUTPUT_DIR / "articles"

if DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD:
    credentials = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
    HEADERS = {
        "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}",
        "Content-Type": "application/json",
    }
else:
    HEADERS = {}

# Rate limiting — track last request time per domain
_domain_last_request: dict[str, float] = {}
RATE_LIMIT_SECONDS = 2.0

# Robots.txt cache
_robots_cache: dict[str, RobotFileParser] = {}

USER_AGENT = "ParadiseMediaResearchBot/1.0"
SCRAPE_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8,fr;q=0.7",
}

# ── Rate Limiting & Robots ──────────────────────────────────────────────────

def rate_limit(domain: str) -> None:
    """Enforce per-domain rate limiting."""
    now = time.time()
    last = _domain_last_request.get(domain, 0)
    wait = RATE_LIMIT_SECONDS - (now - last)
    if wait > 0:
        time.sleep(wait)
    _domain_last_request[domain] = time.time()


def check_robots(url: str) -> bool:
    """Check if URL is allowed by robots.txt."""
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain not in _robots_cache:
        rp = RobotFileParser()
        robots_url = f"{parsed.scheme}://{domain}/robots.txt"
        try:
            rp.set_url(robots_url)
            rp.read()
        except Exception:
            # If we can't read robots.txt, assume allowed
            rp = RobotFileParser()
        _robots_cache[domain] = rp

    return _robots_cache[domain].can_fetch(USER_AGENT, url)


# ── DataForSEO Functions ────────────────────────────────────────────────────

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
                return result
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                print(f"    API error: {e}")
                return None
    return None


def discover_articles_serp(journalist: dict, max_articles: int = 100) -> list[dict]:
    """Discover article URLs via DataForSEO SERP search."""
    if not HEADERS:
        return []

    name = journalist["name"]
    outlet = journalist.get("primary_outlet", "")
    articles = []

    queries = []

    # Query 1: Name + outlet site search
    if outlet:
        queries.append({
            "keyword": f'"{name}" site:{outlet}',
            "location_code": 2840,
            "language_code": "en",
            "depth": min(100, max_articles),
        })

    # Query 2: Name + sports keywords
    sports = journalist.get("sports", [])
    if sports:
        sport = sports[0]
        queries.append({
            "keyword": f'"{name}" {sport} article',
            "location_code": 2840,
            "language_code": "en",
            "depth": 50,
        })

    # Query 3: Name as author
    queries.append({
        "keyword": f'"{name}" author sports',
        "location_code": 2840,
        "language_code": "en",
        "depth": 50,
    })

    for query in queries[:3]:
        result = make_request("serp/google/organic/live/advanced", [query])
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
                    url = item.get("url", "")
                    if not url or url in {a["url"] for a in articles}:
                        continue
                    articles.append({
                        "url": url,
                        "title": item.get("title", ""),
                        "snippet": item.get("description", ""),
                        "serp_position": item.get("rank_absolute"),
                        "estimated_traffic": item.get("estimated_paid_traffic_cost", 0),
                        "outlet_domain": urlparse(url).netloc,
                        "discovery_method": "dataforseo_serp",
                    })

        time.sleep(1)

    return articles[:max_articles]


# ── Article Scraping ────────────────────────────────────────────────────────

def scrape_article(url: str) -> dict:
    """Scrape a single article URL, extracting text, headings, and metadata."""
    result = {
        "url": url,
        "title": "",
        "body_text": "",
        "word_count": 0,
        "h2_structure": [],
        "h3_structure": [],
        "publish_date": None,
        "scrape_status": "pending",
        "paywalled": False,
    }

    domain = urlparse(url).netloc

    # Check robots.txt
    if not check_robots(url):
        result["scrape_status"] = "robots_blocked"
        return result

    # Rate limit
    rate_limit(domain)

    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            resp = client.get(url, headers=SCRAPE_HEADERS)
            if resp.status_code == 403 or resp.status_code == 451:
                result["scrape_status"] = "blocked"
                return result
            if resp.status_code != 200:
                result["scrape_status"] = "failed"
                return result

            soup = BeautifulSoup(resp.text, "html.parser")

            # Paywall detection
            paywall_indicators = [
                soup.find(class_=re.compile(r"paywall|subscribe|premium-content|locked", re.I)),
                soup.find(attrs={"data-paywall": True}),
                soup.find("meta", {"name": "robots", "content": re.compile(r"noindex", re.I)}),
            ]
            if any(paywall_indicators):
                result["paywalled"] = True
                result["scrape_status"] = "paywall"
                # Still extract what we can (title, snippet)
                result["title"] = extract_title(soup)
                return result

            # Title
            result["title"] = extract_title(soup)

            # Body text
            article_body = find_article_body(soup)
            if article_body:
                # Extract headings before stripping
                result["h2_structure"] = [h2.get_text(strip=True) for h2 in article_body.find_all("h2")]
                result["h3_structure"] = [h3.get_text(strip=True) for h3 in article_body.find_all("h3")]

                # Extract text
                for tag in article_body.find_all(["script", "style", "nav", "aside", "footer", "header"]):
                    tag.decompose()
                paragraphs = article_body.find_all(["p", "li"])
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                result["body_text"] = text
                result["word_count"] = len(text.split())

            # Publish date
            result["publish_date"] = extract_publish_date(soup)

            result["scrape_status"] = "success" if result["word_count"] > 50 else "thin"

    except Exception as e:
        result["scrape_status"] = "failed"
        result["error"] = str(e)

    return result


def extract_title(soup: BeautifulSoup) -> str:
    """Extract article title from page."""
    # Try og:title first
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    # Try h1
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    # Fallback to <title>
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(strip=True)
    return ""


def find_article_body(soup: BeautifulSoup) -> BeautifulSoup | None:
    """Find the main article content container."""
    # Priority selectors for article body
    selectors = [
        ("article", {}),
        (None, {"class": re.compile(r"article-body|article-content|story-body|post-content", re.I)}),
        (None, {"role": "main"}),
        ("main", {}),
        (None, {"class": re.compile(r"entry-content|content-body", re.I)}),
        (None, {"itemprop": "articleBody"}),
    ]
    for tag, attrs in selectors:
        found = soup.find(tag, attrs) if tag else soup.find(attrs=attrs)
        if found:
            return found
    return None


def extract_publish_date(soup: BeautifulSoup) -> str | None:
    """Extract publish date from meta tags or structured data."""
    # Meta tags
    for meta_name in ["article:published_time", "datePublished", "date", "pubdate"]:
        tag = soup.find("meta", property=meta_name) or soup.find("meta", {"name": meta_name})
        if tag and tag.get("content"):
            return tag["content"][:10]  # YYYY-MM-DD

    # Time tag
    time_tag = soup.find("time", {"datetime": True})
    if time_tag:
        return time_tag["datetime"][:10]

    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                data = data[0]
            date = data.get("datePublished") or data.get("dateCreated")
            if date:
                return date[:10]
        except (json.JSONDecodeError, TypeError, AttributeError):
            continue

    return None


# ── Article Ranking ──────────────────────────────────────────────────────────

def rank_article(article: dict) -> float:
    """Compute composite article ranking score."""
    score = 0.0

    # Estimated traffic (30%)
    traffic = article.get("estimated_traffic", 0) or 0
    score += min(30, traffic / 100)

    # SERP position (20%) — lower is better
    pos = article.get("serp_position") or 100
    score += max(0, 20 - (pos * 0.2))

    # Word count / depth (15%)
    wc = article.get("word_count", 0) or 0
    if wc >= 2000:
        score += 15
    elif wc >= 1000:
        score += 10
    elif wc >= 500:
        score += 5

    # Recency (15%) — prefer last 2 years
    pub_date = article.get("publish_date")
    if pub_date:
        try:
            pub_year = int(pub_date[:4])
            current_year = 2026
            age = current_year - pub_year
            if age <= 1:
                score += 15
            elif age <= 2:
                score += 10
            elif age <= 3:
                score += 5
        except (ValueError, TypeError):
            pass

    # Social engagement (10%)
    social = article.get("social_engagement", 0) or 0
    score += min(10, social / 50)

    # Domain authority (10%)
    da = article.get("domain_authority", 0) or 0
    score += min(10, da / 10)

    return round(score, 3)


# ── Pipeline ─────────────────────────────────────────────────────────────────

def process_journalist(journalist: dict, max_articles: int, skip_scrape: bool) -> dict:
    """Process a single journalist: use existing URLs from registry, scrape content."""
    jid = journalist["journalist_id"]
    name = journalist["name"]
    print(f"\n  [{jid}] {name} ({journalist.get('geo', '?')})")

    # Use article URLs already discovered by pipeline v2 (no re-discovery needed)
    existing_urls = journalist.get("article_urls", [])
    articles = []
    for url_entry in existing_urls[:max_articles]:
        articles.append({
            "url": url_entry["url"],
            "title": url_entry.get("title", ""),
            "snippet": url_entry.get("snippet", ""),
            "serp_position": url_entry.get("serp_position"),
            "outlet_domain": urlparse(url_entry["url"]).netloc,
            "discovery_method": "registry_v2",
        })

    if not articles:
        print(f"    No article URLs in registry — skipping")
        return {
            "journalist_id": jid, "name": name,
            "total_discovered": 0, "scraped_success": 0, "paywalled": 0, "top_score": 0,
        }

    print(f"    {len(articles)} article URLs from registry")

    # Scrape articles
    if not skip_scrape:
        scraped = 0
        paywalled = 0
        failed = 0
        for i, article in enumerate(articles):
            result = scrape_article(article["url"])
            article.update(result)
            if article["scrape_status"] == "success":
                scraped += 1
            elif article["scrape_status"] == "paywall":
                paywalled += 1
            else:
                failed += 1
        print(f"    Scraped: {scraped} success, {paywalled} paywalled, {failed} failed")

    # Rank articles
    for article in articles:
        article["composite_score"] = rank_article(article)
    articles.sort(key=lambda a: a["composite_score"], reverse=True)

    # Save per-journalist JSONL
    jid_dir = ARTICLES_DIR / jid
    jid_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = jid_dir / "articles_scraped.jsonl"
    with open(jsonl_path, "w") as f:
        for article in articles:
            summary = {k: v for k, v in article.items() if k != "body_text"}
            summary["has_body"] = bool(article.get("body_text"))
            f.write(json.dumps(summary, default=str) + "\n")

    # Save full articles with body text
    full_path = jid_dir / "articles_full.jsonl"
    with open(full_path, "w") as f:
        for article in articles:
            f.write(json.dumps(article, default=str) + "\n")

    return {
        "journalist_id": jid,
        "name": name,
        "total_discovered": len(articles),
        "scraped_success": sum(1 for a in articles if a.get("scrape_status") == "success"),
        "paywalled": sum(1 for a in articles if a.get("scrape_status") == "paywall"),
        "top_score": articles[0]["composite_score"] if articles else 0,
    }


def run_scraper(registry_path: str, max_per_journalist: int, skip_scrape: bool) -> None:
    """Run article scraper across all journalists in the registry."""
    print("=" * 60)
    print("ARTICLE SCRAPER v1.0")
    print(f"Registry: {registry_path}")
    print(f"Max articles per journalist: {max_per_journalist}")
    print(f"Scrape enabled: {not skip_scrape}")
    print("=" * 60)

    # Load registry
    with open(registry_path) as f:
        registry = json.load(f)
    journalists = registry["journalists"]
    print(f"Loaded {len(journalists)} journalists from registry")

    # Process each journalist
    results = []
    for journalist in journalists:
        result = process_journalist(journalist, max_per_journalist, skip_scrape)
        results.append(result)

    # Save summary
    summary_path = OUTPUT_DIR / "scraper_summary.json"
    summary = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_journalists": len(results),
            "total_articles_discovered": sum(r["total_discovered"] for r in results),
            "total_scraped_success": sum(r["scraped_success"] for r in results),
            "total_paywalled": sum(r["paywalled"] for r in results),
        },
        "results": results,
    }
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n── Scraper Complete ─────────────────────────")
    print(f"  Journalists processed: {len(results)}")
    print(f"  Total articles discovered: {summary['metadata']['total_articles_discovered']}")
    print(f"  Successfully scraped: {summary['metadata']['total_scraped_success']}")
    print(f"  Paywalled (snippet only): {summary['metadata']['total_paywalled']}")
    print(f"  Output: {OUTPUT_DIR}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Article Scraper for Journalist Research")
    parser.add_argument("--registry", type=str,
                        default=str(OUTPUT_DIR / "journalist_registry_v2.json"),
                        help="Path to journalist_registry.json")
    parser.add_argument("--max-per-journalist", type=int, default=100,
                        help="Max articles to collect per journalist (default: 100)")
    parser.add_argument("--skip-scrape", action="store_true",
                        help="Only discover URLs, don't scrape content")
    args = parser.parse_args()
    run_scraper(args.registry, args.max_per_journalist, args.skip_scrape)


if __name__ == "__main__":
    main()
