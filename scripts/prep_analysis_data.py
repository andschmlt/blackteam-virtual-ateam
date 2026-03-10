#!/usr/bin/env python3
"""
Prep Analysis Data — Bridge between scraper output and style analysis.

For each journalist, creates a unified articles_full.jsonl that:
1. Uses full body_text for successfully scraped articles
2. Falls back to SERP snippets for failed/thin/paywalled articles
3. Ensures every journalist has at least some text for analysis
"""

import json
from pathlib import Path

REGISTRY_PATH = Path.home() / "AS-Virtual_Team_System_v2/data/journalist_research/journalist_registry_v2.json"
ARTICLES_DIR = Path.home() / "AS-Virtual_Team_System_v2/data/journalist_research/articles"


def prep_data():
    # Load registry
    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    stats = {"total": 0, "with_body": 0, "snippet_only": 0, "no_text": 0}

    for journalist in reg["journalists"]:
        jid = journalist["journalist_id"]
        jdir = ARTICLES_DIR / jid
        jdir.mkdir(parents=True, exist_ok=True)

        full_path = jdir / "articles_full.jsonl"

        # Load existing scraped data if available
        existing = {}
        if full_path.exists():
            with open(full_path) as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        existing[data["url"]] = data
                    except (json.JSONDecodeError, KeyError):
                        continue

        # Build unified article list from registry URLs
        articles = []
        for url_entry in journalist.get("article_urls", []):
            url = url_entry["url"]
            title = url_entry.get("title", "")
            snippet = url_entry.get("snippet", "")

            if url in existing:
                article = existing[url]
                # If article was scraped successfully with good body text, use it
                body = article.get("body_text", "")
                wc = article.get("word_count", 0) or 0
                status = article.get("scrape_status", "")

                if status == "success" and wc >= 50:
                    articles.append(article)
                    continue

            # Fallback: use SERP snippet as body text
            if snippet and len(snippet.split()) >= 10:
                articles.append({
                    "url": url,
                    "title": title,
                    "body_text": snippet,
                    "word_count": len(snippet.split()),
                    "scrape_status": "snippet_only",
                    "h2_structure": [],
                    "h3_structure": [],
                    "publish_date": None,
                    "paywalled": False,
                    "composite_score": 0,
                })

        # Save unified articles
        with open(full_path, "w") as f:
            for article in articles:
                f.write(json.dumps(article, default=str) + "\n")

        success_count = sum(1 for a in articles if a.get("scrape_status") == "success")
        snippet_count = sum(1 for a in articles if a.get("scrape_status") == "snippet_only")
        total_words = sum(a.get("word_count", 0) or 0 for a in articles)

        stats["total"] += 1
        if success_count > 0:
            stats["with_body"] += 1
        elif snippet_count > 0:
            stats["snippet_only"] += 1
        else:
            stats["no_text"] += 1

        status_icon = "✓" if success_count >= 3 else ("~" if len(articles) >= 3 else "✗")
        print(f"  {status_icon} {journalist['name']:30} {success_count:2} scraped + {snippet_count:2} snippets = {len(articles):2} articles ({total_words:6} words)")

    print(f"\n{'='*60}")
    print(f"PREP COMPLETE")
    print(f"  Total journalists: {stats['total']}")
    print(f"  With scraped body text: {stats['with_body']}")
    print(f"  Snippet-only: {stats['snippet_only']}")
    print(f"  No text: {stats['no_text']}")


if __name__ == "__main__":
    prep_data()
